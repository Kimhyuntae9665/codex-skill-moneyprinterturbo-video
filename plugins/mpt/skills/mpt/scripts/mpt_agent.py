#!/usr/bin/env python3
"""Pinned, cross-platform MoneyPrinterTurbo runner for the Codex Skill.

Derived from MoneyPrinterTurbo's official ``docs/skill/mpt_agent.py`` at
commit eb8c23757e098a07bbcd93b3b50e252fc8d1869a.
Copyright (c) 2024 Harry. Licensed under the MIT License.
Modifications copyright (c) 2026 Kim Hyuntae.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path


UPSTREAM_REPOSITORY = "https://github.com/harry0703/MoneyPrinterTurbo.git"
UPSTREAM_COMMIT = "eb8c23757e098a07bbcd93b3b50e252fc8d1869a"
DEFAULT_ROOT = (
    Path.home() / ".codex" / "runtimes" / "moneyprinterturbo" / UPSTREAM_COMMIT
)
DEFAULT_VOICE_NAME = "zh-CN-XiaoxiaoNeural-Female"
NEEDS_INPUT_EXIT_CODE = 10
SUPPORTED_SOURCES = {
    "pexels",
    "pixabay",
    "coverr",
    "volcengine_seedance",
    "local",
}
VOLCENGINE_ARK_API_KEY_URL = (
    "https://console.volcengine.com/ark/region:ark+cn-beijing/apikey"
)
LOCAL_MATERIAL_EXTENSIONS = {
    ".avi",
    ".flv",
    ".jpeg",
    ".jpg",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".png",
    ".webm",
    ".webp",
}
PAID_VIDEO_SOURCES = {"volcengine_seedance", "wavespeed", "loomloom"}
PEXELS_API_KEY_URL = "https://www.pexels.com/api/"
PEXELS_VALIDATION_URL = "https://api.pexels.com/v1/collections?per_page=1"
PEXELS_API_KEY_HELP_URL = (
    "https://help.pexels.com/hc/en-us/articles/"
    "900004904026-How-do-I-get-an-API-key"
)

# Keep the recommended list focused on commonly used providers. When an LLM
# key is missing, the helper emits all choices at once to avoid extra turns.
RECOMMENDED_LLM_PROVIDERS = {
    "moonshot": (
        "Kimi / Moonshot AI",
        "https://platform.kimi.com?track_id=track-2f5441d6ffd84c509dd079d78e9db5dc&aff=moneyprinterturbo",
    ),
    "openai": ("OpenAI", "https://platform.openai.com/api-keys"),
    "gemini": ("Google Gemini", "https://aistudio.google.com/app/apikey"),
    "deepseek": ("DeepSeek", "https://platform.deepseek.com/api_keys"),
    "volcengine": (
        "ByteDance VolcEngine Ark / Doubao",
        "https://www.volcengine.com/activity/ai618?utm_source=MoneyPrinterTurbo",
    ),
    "minimax": ("MiniMax", "https://platform.minimax.io/"),
    "mimo": (
        "Xiaomi MiMo",
        "https://platform.xiaomimimo.com/docs/zh-CN/quick-start/first-api-call",
    ),
}
KEYLESS_LLM_PROVIDERS = {"ollama", "litellm"}
CUSTOM_OPENAI_PROVIDER = "oneapi"

# Hidden providers such as Qwen, Azure, and Grok remain usable when already
# selected, but are not automatic fallback candidates. A fully configured
# generic OpenAI-compatible endpoint can be reused safely.
ADDITIONAL_REUSABLE_PROVIDERS = (CUSTOM_OPENAI_PROVIDER,)


class SkillError(RuntimeError):
    """An actionable Skill error that can be reported without a traceback."""


def log(message: str) -> None:
    """Flush concise progress so the agent knows the long-running job started."""
    print(f"[MoneyPrinterTurbo] {message}", flush=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install MoneyPrinterTurbo and generate a final video from a topic."
    )
    parser.add_argument("--subject", required=True, help="video topic")
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"MoneyPrinterTurbo installation directory (default: {DEFAULT_ROOT})",
    )
    parser.add_argument(
        "--script-file",
        type=Path,
        help="UTF-8 file containing a complete prepared narration script",
    )
    parser.add_argument(
        "--material",
        type=Path,
        action="append",
        default=[],
        help="local image/video material; repeat this option for multiple files",
    )
    parser.add_argument(
        "--materials-dir",
        type=Path,
        help="directory of local image/video materials, sorted by filename",
    )
    parser.add_argument(
        "--font-file",
        type=Path,
        help="TTF/TTC subtitle font to stage inside the isolated runtime",
    )
    parser.add_argument(
        "--confirm-paid-provider",
        action="store_true",
        help="explicit confirmation that the user authorized the selected paid provider",
    )
    parser.add_argument(
        "cli_args",
        nargs=argparse.REMAINDER,
        help="additional MoneyPrinterTurbo CLI arguments placed after --",
    )
    args = parser.parse_args(argv)
    args.subject = args.subject.strip()
    if not args.subject:
        parser.error("--subject cannot be empty")
    if args.cli_args and args.cli_args[0] == "--":
        args.cli_args = args.cli_args[1:]
    return args


def _run_git(args: list[str], *, cwd: Path | None = None) -> str:
    """Run one bounded Git command and return stdout without leaking config."""
    git = shutil.which("git")
    if not git:
        raise SkillError("git was not found; install Git and retry")
    result = subprocess.run(
        [git, *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        tail = (result.stdout or "").splitlines()[-20:]
        if tail:
            print("\n".join(tail), file=sys.stderr)
        raise SkillError(
            f"git command failed with exit code {result.returncode}: {args[0]}"
        )
    return (result.stdout or "").strip()


def ensure_project(root: Path) -> None:
    """Reuse or install the exact reviewed upstream commit in an isolated root."""
    root = root.expanduser().resolve()
    if (root / "cli.py").is_file() and (root / "config.example.toml").is_file():
        if not (root / ".git").is_dir():
            raise SkillError(
                f"runtime project is not a Git checkout and cannot be verified: {root}"
            )
        head = _run_git(["-C", str(root), "rev-parse", "HEAD"])
        if head.lower() != UPSTREAM_COMMIT:
            raise SkillError(
                "runtime commit mismatch; expected "
                f"{UPSTREAM_COMMIT}, found {head or '<unknown>'}"
            )
        log(f"using existing project: {root}")
        return
    if root.exists() and any(root.iterdir()):
        raise SkillError(f"installation directory exists but is not a valid project: {root}")

    root.parent.mkdir(parents=True, exist_ok=True)
    log(
        "first-time installation: fetching reviewed upstream commit "
        f"{UPSTREAM_COMMIT} to {root}"
    )
    with tempfile.TemporaryDirectory(prefix="mpt-install-") as temp_dir_value:
        temp_dir = Path(temp_dir_value)
        candidate = temp_dir / "MoneyPrinterTurbo"
        _run_git(["init", str(candidate)])
        _run_git(["-C", str(candidate), "remote", "add", "origin", UPSTREAM_REPOSITORY])
        _run_git(
            [
                "-C",
                str(candidate),
                "fetch",
                "--depth",
                "1",
                "origin",
                UPSTREAM_COMMIT,
            ]
        )
        _run_git(["-C", str(candidate), "checkout", "--detach", "FETCH_HEAD"])
        head = _run_git(["-C", str(candidate), "rev-parse", "HEAD"])
        if head.lower() != UPSTREAM_COMMIT:
            raise SkillError(
                f"checked-out commit mismatch: expected {UPSTREAM_COMMIT}, found {head}"
            )
        if not (candidate / "cli.py").is_file():
            raise SkillError("Git checkout completed without MoneyPrinterTurbo cli.py")
        if root.exists():
            root.rmdir()
        shutil.move(str(candidate), str(root))
    log("pinned project checkout completed")


def ensure_config(root: Path) -> Path:
    """Create the initial configuration without overwriting an existing file."""
    config_path = root / "config.toml"
    if not config_path.exists():
        shutil.copy2(root / "config.example.toml", config_path)
        log(f"created configuration file: {config_path}")
    return config_path


def _plain_config_value(text: str, key: str) -> str:
    """Read a simple top-level TOML value without printing its contents."""
    match = re.search(rf"(?m)^{re.escape(key)}\s*=\s*(.*)$", text)
    if not match:
        return ""
    value = match.group(1).split("#", 1)[0].strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def _replace_config_value(text: str, key: str, value: object) -> str:
    """Replace one active field while preserving the configuration layout."""
    pattern = re.compile(rf"(?m)^({re.escape(key)}\s*=\s*).*$")
    if not pattern.search(text):
        raise SkillError(f"configuration field not found in config.toml: {key}")
    encoded = json.dumps(value, ensure_ascii=False)
    return pattern.sub(lambda match: f"{match.group(1)}{encoded}", text, count=1)


def _has_configured_value(value: str) -> bool:
    """Treat empty strings and whitespace-only key arrays as unconfigured."""
    if not value:
        return False
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return bool(value.strip())
    if isinstance(parsed, list):
        return any(str(item).strip() for item in parsed)
    return bool(str(parsed).strip())


def _parse_string_list(value: str) -> list[str]:
    """Parse a configured string list while removing blanks and duplicates."""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return list(dict.fromkeys(str(item).strip() for item in parsed if str(item).strip()))


def enforce_no_upload(config_path: Path) -> None:
    """Disable every automatic social publishing switch in the isolated runtime."""
    text = config_path.read_text(encoding="utf-8")
    for key, value in (
        ("upload_post_enabled", False),
        ("upload_post_auto_upload", False),
        ("upload_post_platforms", []),
    ):
        text = _replace_config_value(text, key, value)
    config_path.write_text(text, encoding="utf-8")
    log("automatic social publishing is disabled for this runtime")


def _read_prepared_script(script_file: Path) -> str:
    script_path = script_file.expanduser().resolve()
    if not script_path.is_file():
        raise SkillError(f"prepared script file does not exist: {script_path}")
    script = script_path.read_text(encoding="utf-8-sig").strip()
    if not script:
        raise SkillError(f"prepared script file is empty: {script_path}")
    return script


def _validated_material_path(raw_path: Path) -> Path:
    material_path = raw_path.expanduser().resolve()
    if not material_path.is_file():
        raise SkillError(f"local material does not exist: {material_path}")
    if material_path.suffix.lower() not in LOCAL_MATERIAL_EXTENSIONS:
        raise SkillError(f"unsupported local material type: {material_path.suffix}")
    if "," in str(material_path):
        raise SkillError(
            f"local material paths cannot contain commas: {material_path}"
        )
    return material_path


def collect_local_materials(
    material_args: list[Path], materials_dir: Path | None
) -> list[Path]:
    """Resolve, validate, sort, and de-duplicate prepared local materials."""
    candidates = list(material_args)
    if materials_dir is not None:
        directory = materials_dir.expanduser().resolve()
        if not directory.is_dir():
            raise SkillError(f"materials directory does not exist: {directory}")
        candidates.extend(
            sorted(
                (
                    path
                    for path in directory.iterdir()
                    if path.is_file()
                    and path.suffix.lower() in LOCAL_MATERIAL_EXTENSIONS
                ),
                key=lambda path: path.name.casefold(),
            )
        )
    resolved: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        material_path = _validated_material_path(candidate)
        key = str(material_path).casefold()
        if key not in seen:
            resolved.append(material_path)
            seen.add(key)
    if (material_args or materials_dir is not None) and not resolved:
        raise SkillError("no supported local materials were found")
    return resolved


def stage_subtitle_font(root: Path, font_file: Path) -> str:
    """Copy a user-approved subtitle font into the isolated MPT runtime."""
    source = font_file.expanduser().resolve()
    if not source.is_file():
        raise SkillError(f"subtitle font does not exist: {source}")
    if source.suffix.lower() not in {".ttf", ".ttc"}:
        raise SkillError(f"unsupported subtitle font type: {source.suffix}")
    destination = root / "resource" / "fonts" / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or destination.read_bytes() != source.read_bytes():
        shutil.copy2(source, destination)
    log(f"staged subtitle font: {destination.name}")
    return destination.name


def apply_environment_config(config_path: Path) -> None:
    """Write supplied credentials while logging field names only."""
    provider = os.environ.get("MPT_LLM_PROVIDER", "").strip().lower()
    if provider == "openai_compatible":
        provider = CUSTOM_OPENAI_PROVIDER
    llm_key = os.environ.get("MPT_LLM_API_KEY", "").strip()
    base_url = os.environ.get("MPT_LLM_BASE_URL", "").strip()
    model_name = os.environ.get("MPT_LLM_MODEL_NAME", "").strip()
    pexels_key = os.environ.get("MPT_PEXELS_API_KEY", "").strip()
    seedance_key = os.environ.get("MPT_VOLCENGINE_ARK_API_KEY", "").strip()
    if not any((provider, llm_key, base_url, model_name, pexels_key, seedance_key)):
        return

    text = config_path.read_text(encoding="utf-8")
    current_provider = _plain_config_value(text, "llm_provider") or "moonshot"
    provider = provider or current_provider
    changes: list[str] = []
    if os.environ.get("MPT_LLM_PROVIDER", "").strip():
        text = _replace_config_value(text, "llm_provider", provider)
        changes.append("llm_provider")
    if llm_key:
        text = _replace_config_value(text, f"{provider}_api_key", llm_key)
        changes.append(f"{provider}_api_key")
    if base_url:
        text = _replace_config_value(text, f"{provider}_base_url", base_url)
        changes.append(f"{provider}_base_url")
    if model_name:
        text = _replace_config_value(text, f"{provider}_model_name", model_name)
        changes.append(f"{provider}_model_name")
    if pexels_key:
        text = _replace_config_value(text, "pexels_api_keys", [pexels_key])
        changes.append("pexels_api_keys")
    if seedance_key:
        text = _replace_config_value(
            text, "volcengine_seedance_api_key", seedance_key
        )
        changes.append("volcengine_seedance_api_key")
    config_path.write_text(text, encoding="utf-8")
    log("updated configuration fields: " + ", ".join(changes))


def _provider_is_ready(text: str, provider: str) -> bool:
    """Return whether a provider has enough configuration to generate."""
    if provider in KEYLESS_LLM_PROVIDERS:
        return True
    if not _has_configured_value(
        _plain_config_value(text, f"{provider}_api_key")
    ):
        return False
    if provider == CUSTOM_OPENAI_PROVIDER:
        return all(
            _has_configured_value(_plain_config_value(text, f"{provider}_{suffix}"))
            for suffix in ("base_url", "model_name")
        )
    return True


def reuse_existing_llm_provider(config_path: Path) -> str:
    """
    Reuse existing LLM credentials before asking the user for another key.

    Keep the current provider when it is ready. Otherwise, scan configured
    recommended providers in UI order and update ``llm_provider``. Credential
    values are inspected in memory and are never logged.
    """
    text = config_path.read_text(encoding="utf-8")
    current_provider = _plain_config_value(text, "llm_provider") or "moonshot"
    if _provider_is_ready(text, current_provider):
        return current_provider

    reusable_providers = (
        *RECOMMENDED_LLM_PROVIDERS,
        *ADDITIONAL_REUSABLE_PROVIDERS,
    )
    for provider in reusable_providers:
        if _provider_is_ready(text, provider):
            text = _replace_config_value(text, "llm_provider", provider)
            config_path.write_text(text, encoding="utf-8")
            log(f"reusing configured LLM provider: {provider}")
            return provider
    return current_provider


def selected_video_source(cli_args: list[str]) -> str:
    """Read the effective material source from forwarded CLI arguments."""
    source = "pexels"
    for index, item in enumerate(cli_args):
        if item == "--video-source" and index + 1 < len(cli_args):
            source = cli_args[index + 1].strip().lower()
        elif item.startswith("--video-source="):
            source = item.split("=", 1)[1].strip().lower()
    return source


def has_cli_option(cli_args: list[str], option: str) -> bool:
    """Return whether forwarded arguments explicitly set a CLI option."""
    return any(item == option or item.startswith(f"{option}=") for item in cli_args)


def cli_option_value(cli_args: list[str], option: str) -> str:
    """Return the final explicit value for a forwarded CLI option."""
    value = ""
    for index, item in enumerate(cli_args):
        if item == option and index + 1 < len(cli_args):
            value = cli_args[index + 1].strip()
        elif item.startswith(f"{option}="):
            value = item.split("=", 1)[1].strip()
    return value


def is_prepared_local(cli_args: list[str]) -> bool:
    """Return whether this run can avoid both LLM and stock-material APIs."""
    return (
        selected_video_source(cli_args) == "local"
        and bool(cli_option_value(cli_args, "--video-script"))
        and bool(cli_option_value(cli_args, "--video-materials"))
    )


def build_forwarded_cli_args(
    args: argparse.Namespace, root: Path
) -> list[str]:
    """Translate file-oriented Skill inputs into safe upstream CLI arguments."""
    cli_args = list(args.cli_args)
    for forbidden in ("--task-id", "--batch-file"):
        if has_cli_option(cli_args, forbidden):
            raise SkillError(f"the Skill controls {forbidden}; do not pass it manually")

    if args.script_file is not None:
        if has_cli_option(cli_args, "--video-script"):
            raise SkillError("use either --script-file or --video-script, not both")
        cli_args.extend(["--video-script", _read_prepared_script(args.script_file)])

    materials = collect_local_materials(args.material, args.materials_dir)
    if materials:
        source = selected_video_source(cli_args)
        if has_cli_option(cli_args, "--video-source") and source != "local":
            raise SkillError("local materials require --video-source local")
        if has_cli_option(cli_args, "--video-materials"):
            raise SkillError("use either --material/--materials-dir or --video-materials")
        if not has_cli_option(cli_args, "--video-source"):
            cli_args.extend(["--video-source", "local"])
        cli_args.extend(
            ["--video-materials", ",".join(str(path) for path in materials)]
        )

    if args.font_file is not None:
        if has_cli_option(cli_args, "--font-name"):
            raise SkillError("use either --font-file or --font-name, not both")
        cli_args.extend(["--font-name", stage_subtitle_font(root, args.font_file)])

    source = selected_video_source(cli_args)
    if source in PAID_VIDEO_SOURCES and not args.confirm_paid_provider:
        raise SkillError(
            f"paid video source {source!r} requires explicit --confirm-paid-provider"
        )
    if source == "volcengine_seedance" and not has_cli_option(
        cli_args, "--confirm-seedance-charge"
    ):
        raise SkillError(
            "volcengine_seedance also requires --confirm-seedance-charge"
        )
    return cli_args


def missing_config(config_path: Path, cli_args: list[str]) -> tuple[str, list[str]]:
    """Return the active provider and only the fields required by this run."""
    text = config_path.read_text(encoding="utf-8")
    provider = _plain_config_value(text, "llm_provider") or "moonshot"
    missing: list[str] = []
    if not is_prepared_local(cli_args):
        if provider not in KEYLESS_LLM_PROVIDERS and not _has_configured_value(
            _plain_config_value(text, f"{provider}_api_key")
        ):
            missing.append(f"{provider}_api_key")
        if provider == CUSTOM_OPENAI_PROVIDER:
            for suffix in ("base_url", "model_name"):
                field = f"{provider}_{suffix}"
                if not _has_configured_value(_plain_config_value(text, field)):
                    missing.append(field)

    source = selected_video_source(cli_args)
    if source not in SUPPORTED_SOURCES:
        raise SkillError(f"unsupported video source: {source}")
    if source == "volcengine_seedance":
        # 与运行时 Provider 保持完全一致的凭据优先级，避免 Skill 预检通过后
        # 主程序却读取了另一把 Key。ARK_API_KEY 语义过于宽泛，明确不再兼容。
        value = (
            _plain_config_value(text, "volcengine_seedance_api_key")
            or os.environ.get("VOLCENGINE_ARK_API_KEY", "").strip()
            or _plain_config_value(text, "volcengine_api_key")
        )
        if not _has_configured_value(value):
            missing.append("volcengine_seedance_api_key")
        if not has_cli_option(cli_args, "--confirm-seedance-charge"):
            missing.append("confirm_seedance_charge")
    elif source != "local":
        value = _plain_config_value(text, f"{source}_api_keys")
        if not _has_configured_value(value):
            missing.append(f"{source}_api_keys")
    return provider, missing


def report_missing_config(provider: str, missing: list[str]) -> int:
    """Tell the agent exactly which credentials must be requested."""
    print("MPT_NEEDS_INPUT")
    print(f"LLM_PROVIDER={provider}")
    for field in missing:
        print(f"MISSING={field}")
    if f"{provider}_api_key" in missing:
        print("LLM_PROVIDER_OPTIONS_BEGIN")
        for provider_id, (label, url) in RECOMMENDED_LLM_PROVIDERS.items():
            print(f"LLM_PROVIDER_OPTION={provider_id}|{label}|{url}")
        print(
            "LLM_PROVIDER_OPTION=oneapi|Other OpenAI-compatible provider|"
            "requires an API key, API base URL, and model name"
        )
        print("LLM_PROVIDER_OPTIONS_END")
    if any(field.startswith(f"{CUSTOM_OPENAI_PROVIDER}_") for field in missing):
        print(
            "OPENAI_COMPATIBLE_REQUIRED="
            "API key, API base URL, model name"
        )
    if "pexels_api_keys" in missing:
        print(f"PEXELS_API_KEY_URL={PEXELS_API_KEY_URL}")
        print(f"PEXELS_API_KEY_HELP_URL={PEXELS_API_KEY_HELP_URL}")
    if "volcengine_seedance_api_key" in missing:
        print(f"VOLCENGINE_ARK_API_KEY_URL={VOLCENGINE_ARK_API_KEY_URL}")
        print("VOLCENGINE_ARK_API_KEY_ENV=MPT_VOLCENGINE_ARK_API_KEY")
    if "confirm_seedance_charge" in missing:
        print("SEEDANCE_CHARGE_CONFIRMATION_REQUIRED=--confirm-seedance-charge")
    print("Request only the listed values, set the environment variables, and rerun the same command.")
    return NEEDS_INPUT_EXIT_CODE


def report_invalid_pexels_config() -> int:
    """Request only a new Pexels key when every configured key is rejected."""
    print("MPT_NEEDS_INPUT")
    print("INVALID=pexels_api_keys")
    print(f"PEXELS_API_KEY_URL={PEXELS_API_KEY_URL}")
    print(f"PEXELS_API_KEY_HELP_URL={PEXELS_API_KEY_HELP_URL}")
    print("All configured Pexels API keys were rejected or are unavailable. Provide a new key.")
    return NEEDS_INPUT_EXIT_CODE


def _validate_pexels_key(api_key: str) -> str:
    """
    Return ``valid``, ``rejected``, or ``unknown`` for a Pexels key.

    HTTP 401, 403, and rate-limited 429 responses make a key unusable for this
    run. Network and server errors return unknown so the configuration is kept.
    """
    # Curated and popular search requests may hit a public cache and return 200
    # without valid authorization. My Collections is account-specific, requires
    # authentication, and still returns 200 for an empty collection list.
    request = urllib.request.Request(
        PEXELS_VALIDATION_URL,
        headers={
            "Authorization": api_key,
            "User-Agent": "MoneyPrinterTurbo-Agent-Skill",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return "valid" if 200 <= response.status < 300 else "unknown"
    except urllib.error.HTTPError as exc:
        if exc.code in {401, 403, 429}:
            return "rejected"
        return "unknown"
    except (TimeoutError, urllib.error.URLError):
        return "unknown"


def validate_pexels_config(config_path: Path, cli_args: list[str]) -> bool:
    """
    Validate all Pexels keys used by the default material source.

    Downstream code selects configured keys randomly. Keeping rejected keys can
    cause intermittent 401 responses and missing material results. If at least
    one key is verified, retain only verified keys. If validation is impossible
    because of a transient network failure, keep the original configuration.
    """
    if selected_video_source(cli_args) != "pexels":
        return True

    text = config_path.read_text(encoding="utf-8")
    keys = _parse_string_list(_plain_config_value(text, "pexels_api_keys"))
    if not keys:
        return False

    valid_keys: list[str] = []
    rejected_count = 0
    unknown_count = 0
    for api_key in keys:
        status = _validate_pexels_key(api_key)
        if status == "valid":
            valid_keys.append(api_key)
        elif status == "rejected":
            rejected_count += 1
        else:
            unknown_count += 1

    if valid_keys:
        if valid_keys != keys:
            text = _replace_config_value(text, "pexels_api_keys", valid_keys)
            config_path.write_text(text, encoding="utf-8")
        log(
            "Pexels key validation completed: "
            f"valid={len(valid_keys)}, rejected={rejected_count}, "
            f"unknown={unknown_count}"
        )
        return True
    if unknown_count:
        log("Pexels keys could not be verified due to a network or service error; keeping the existing configuration")
        return True

    log(f"Pexels key validation failed: all {rejected_count} configured keys are unusable")
    return False


def result_manifest_path(root: Path) -> Path:
    return root / ".agent-logs" / "moneyprinterturbo-video" / "latest-result.json"


def write_result_manifest(root: Path, payload: dict[str, object]) -> Path:
    """
    Atomically write the stable result file for agents that cannot wait.

    The file contains task status and result paths only, never configuration
    contents, credentials, or full logs.
    """
    result_path = result_manifest_path(root)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    unique_suffix = str(uuid.uuid4()).replace("-", "")
    temp_path = result_path.with_name(
        f".{result_path.name}.{os.getpid()}.{unique_suffix}.tmp"
    )
    temp_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temp_path.replace(result_path)
    return result_path.resolve()


def run_checked(command: list[str], *, cwd: Path) -> None:
    """Run dependency sync quietly and show only the last 30 lines on failure."""
    log("installing or verifying project dependencies with uv")
    result = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        output_tail = (result.stdout or "").splitlines()[-30:]
        if output_tail:
            print("\n".join(output_tail), file=sys.stderr)
        raise SkillError(f"dependency installation failed with exit code {result.returncode}")


def generate_video(
    root: Path,
    subject: str,
    cli_args: list[str],
) -> tuple[list[Path], Path, Path, Path]:
    """Run one traceable CLI task and return only its final video files."""
    uv = shutil.which("uv")
    if not uv:
        raise SkillError("uv was not found; reopen the terminal or add uv to PATH")
    run_checked([uv, "sync", "--frozen", "--python", "3.11"], cwd=root)

    task_id = str(uuid.uuid4())
    task_dir = root / "storage" / "tasks" / task_id
    log_dir = root / ".agent-logs" / "moneyprinterturbo-video"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"run-{task_id}.log"
    write_result_manifest(
        root,
        {
            "status": "running",
            "subject": subject,
            "task_id": task_id,
            "task_dir": str(task_dir.resolve()),
            "log_file": str(log_path.resolve()),
            "video_files": [],
        },
    )
    voice_args = (
        []
        if has_cli_option(cli_args, "--voice-name")
        else ["--voice-name", DEFAULT_VOICE_NAME]
    )
    command = [
        uv,
        "run",
        "--python",
        "3.11",
        "python",
        "cli.py",
        *cli_args,
        "--video-subject",
        subject,
        "--task-id",
        task_id,
        # Older CLI versions leave voice_name empty and fail during Edge TTS
        # with ``Invalid voice ''``. Supply a stable Chinese voice unless the
        # user has explicitly selected another voice.
        *voice_args,
        # A Skill request must produce a finished video. Force the final stage
        # so forwarded options cannot stop at script, audio, or materials.
        "--stop-at",
        "video",
    ]
    log(f"starting video generation, task ID: {task_id}")
    log(f"full generation log: {log_path}")
    with log_path.open("w", encoding="utf-8") as log_file:
        result = subprocess.run(
            command,
            cwd=root,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    if result.returncode != 0:
        tail = log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-30:]
        if tail:
            print("\n".join(tail), file=sys.stderr)
        error = (
            f"video generation failed with exit code {result.returncode}; "
            f"log: {log_path}"
        )
        write_result_manifest(
            root,
            {
                "status": "failed",
                "subject": subject,
                "task_id": task_id,
                "task_dir": str(task_dir.resolve()),
                "log_file": str(log_path.resolve()),
                "video_files": [],
                "error": error,
            },
        )
        raise SkillError(error)

    videos = sorted(
        path.resolve()
        for path in task_dir.glob("final-*.mp4")
        if path.is_file() and path.stat().st_size > 0
    )
    if not videos:
        error = f"generation completed without a valid final MP4; log: {log_path}"
        write_result_manifest(
            root,
            {
                "status": "failed",
                "subject": subject,
                "task_id": task_id,
                "task_dir": str(task_dir.resolve()),
                "log_file": str(log_path.resolve()),
                "video_files": [],
                "error": error,
            },
        )
        raise SkillError(error)
    result_path = write_result_manifest(
        root,
        {
            "status": "completed",
            "subject": subject,
            "task_id": task_id,
            "task_dir": str(task_dir.resolve()),
            "log_file": str(log_path.resolve()),
            "video_files": [str(video) for video in videos],
        },
    )
    return videos, task_dir.resolve(), log_path.resolve(), result_path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.expanduser().resolve()
    try:
        ensure_project(root)
        config_path = ensure_config(root)
        apply_environment_config(config_path)
        enforce_no_upload(config_path)
        cli_args = build_forwarded_cli_args(args, root)
        reuse_existing_llm_provider(config_path)
        provider, missing = missing_config(config_path, cli_args)
        if missing:
            write_result_manifest(
                root,
                {
                    "status": "needs_input",
                    "subject": args.subject,
                    "missing": missing,
                },
            )
            return report_missing_config(provider, missing)
        if not validate_pexels_config(config_path, cli_args):
            write_result_manifest(
                root,
                {
                    "status": "needs_input",
                    "subject": args.subject,
                    "invalid": ["pexels_api_keys"],
                },
            )
            return report_invalid_pexels_config()
        videos, task_dir, log_path, result_path = generate_video(
            root, args.subject, cli_args
        )
    except (OSError, SkillError, UnicodeError, urllib.error.URLError) as exc:
        print(f"MPT_ERROR={exc}", file=sys.stderr)
        return 1

    print("MPT_RESULT")
    for video in videos:
        print(f"VIDEO_FILE={video}")
    print(f"TASK_DIR={task_dir}")
    print(f"LOG_FILE={log_path}")
    print(f"RESULT_FILE={result_path}")
    print(f"UPSTREAM_COMMIT={UPSTREAM_COMMIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
