from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


REQUIRED_COMMANDS = ("git", "uv", "ffmpeg", "ffprobe")
REQUIRED_FILES = (
    "SKILL.md",
    "assets/fonts/NotoSansKR-Bold.ttf",
    "scripts/mpt_agent.py",
    "scripts/validate_video.py",
    "scripts/burn_subtitles.py",
    "scripts/validate_scene_manifest.py",
    "scripts/probe_scene_frames.py",
)


def candidate_skill_roots() -> list[Path]:
    roots: list[Path] = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        roots.append(Path(codex_home) / "skills")
    home = Path.home()
    roots.extend((home / ".codex" / "skills", home / ".agents" / "skills"))
    unique: list[Path] = []
    for root in roots:
        resolved = root.expanduser()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def find_skill(name: str, roots: list[Path]) -> str | None:
    for root in roots:
        candidate = root / name / "SKILL.md"
        if candidate.is_file():
            return str(candidate.parent.resolve())
    return None


def inspect(mode: str) -> dict[str, object]:
    skill_root = Path(__file__).resolve().parents[1]
    commands = {name: shutil.which(name) for name in REQUIRED_COMMANDS}
    files = {
        relative: (skill_root / Path(relative)).is_file()
        for relative in REQUIRED_FILES
    }
    roots = candidate_skill_roots()
    companions = {
        "us-stock-research": find_skill("us-stock-research", roots),
        "infographic-creator": find_skill("infographic-creator", roots),
    }
    errors: list[str] = []
    warnings: list[str] = []
    if sys.version_info < (3, 11):
        errors.append("Python 3.11 or newer is required")
    errors.extend(f"missing command: {name}" for name, path in commands.items() if not path)
    errors.extend(f"missing bundled file: {name}" for name, present in files.items() if not present)
    if mode == "us-equity" and not companions["us-stock-research"]:
        errors.append("missing companion Skill: us-stock-research")
    if mode == "us-equity" and not companions["infographic-creator"]:
        warnings.append(
            "infographic-creator is unavailable; use a validated custom chart or install the companion Skill"
        )
    return {
        "status": "pass" if not errors else "fail",
        "mode": mode,
        "python": sys.version.split()[0],
        "skill_root": str(skill_root),
        "commands": commands,
        "bundled_files": files,
        "skill_search_roots": [str(path) for path in roots],
        "companions": companions,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check MoneyPrinterTurbo Video portability prerequisites")
    parser.add_argument("--mode", choices=("basic", "us-equity"), default="basic")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()
    report = inspect(args.mode)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"MPT_ENV_{str(report['status']).upper()}")
        for error in report["errors"]:
            print(f"ERROR: {error}")
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
