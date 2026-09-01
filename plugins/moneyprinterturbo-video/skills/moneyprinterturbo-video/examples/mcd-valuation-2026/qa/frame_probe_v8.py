"""Probe a rendered MCD v8 short against the frozen scene manifest.

This is a small, dependency-free (apart from the FFmpeg binaries) gate for
the render output.  It deliberately does not render or edit the video: it
checks the stream contract, samples every scene boundary and midpoint, builds
a contact sheet, and runs FFmpeg's ``freezedetect`` filter.

Usage::

    python qa/frame_probe_v8.py output.mp4 scene-manifest-v8.json \
        --out-dir qa/frame-probe-v8

The command prints a JSON report and exits non-zero when a required check
fails.  Sample images and the contact sheet are the only generated artifacts.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "scene-manifest-v8.json"
EXPECTED_BOUNDARIES = (
    0.0,
    4.0,
    7.45,
    10.95,
    15.15,
    19.75,
    23.95,
    29.05,
    33.3,
    38.35,
    41.55,
    45.75,
    50.0,
    54.0,
    58.5,
)
EXPECTED_OUTPUT = (1080, 1920)
EXPECTED_FPS = 30.0
FPS_TOLERANCE = 0.01
BOUNDARY_TOLERANCE = 1e-6


def _float(value: Any) -> float | None:
    """Return a finite float, or ``None`` for missing/non-numeric values."""

    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _ratio(value: Any) -> float | None:
    """Parse FFprobe's decimal or ``num/den`` frame-rate fields."""

    if value is None:
        return None
    text = str(value).strip()
    if not text or text in {"0/0", "N/A"}:
        return None
    try:
        if "/" in text:
            numerator, denominator = text.split("/", 1)
            denominator_value = float(denominator)
            if denominator_value == 0:
                return None
            result = float(Fraction(numerator) / Fraction(denominator))
        else:
            result = float(text)
    except (ValueError, ZeroDivisionError):
        return None
    return result if math.isfinite(result) else None


def _tool_path(name: str, override: str | None) -> str | None:
    if override:
        candidate = Path(override)
        return str(candidate) if candidate.exists() else None
    return shutil.which(name)


def _run(
    command: list[str],
    *,
    timeout_s: float,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run an external probe without invoking a shell."""

    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_s,
        check=False,
    )


def _load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return None, [f"manifest_missing:{path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"manifest_unreadable:{exc}"]
    if not isinstance(data, dict):
        return None, ["manifest_not_object"]

    canvas = data.get("canvas")
    output = canvas.get("output") if isinstance(canvas, dict) else None
    timeline = data.get("timeline")
    boundaries = timeline.get("boundaries_s") if isinstance(timeline, dict) else None
    scene_count = timeline.get("scene_count") if isinstance(timeline, dict) else None
    if not isinstance(output, dict):
        errors.append("manifest_canvas_output_missing")
    else:
        if output.get("width") != EXPECTED_OUTPUT[0] or output.get("height") != EXPECTED_OUTPUT[1]:
            errors.append(f"manifest_output_must_be_{EXPECTED_OUTPUT[0]}x{EXPECTED_OUTPUT[1]}")
        manifest_fps = _float(canvas.get("fps")) if isinstance(canvas, dict) else None
        if manifest_fps is None or abs(manifest_fps - EXPECTED_FPS) > FPS_TOLERANCE:
            errors.append("manifest_fps_must_be_30")
    if not isinstance(boundaries, list) or len(boundaries) != len(EXPECTED_BOUNDARIES):
        errors.append("manifest_must_have_15_boundaries")
    else:
        numeric_boundaries = [_float(value) for value in boundaries]
        for index, (actual, expected) in enumerate(zip(boundaries, EXPECTED_BOUNDARIES)):
            actual_float = _float(actual)
            if actual_float is None or abs(actual_float - expected) > BOUNDARY_TOLERANCE:
                errors.append(f"manifest_boundary_{index}_mismatch")
        if all(value is not None for value in numeric_boundaries) and any(
            numeric_boundaries[i + 1] <= numeric_boundaries[i]  # type: ignore[operator]
            for i in range(len(numeric_boundaries) - 1)
        ):
            errors.append("manifest_boundaries_not_strictly_increasing")
    if scene_count != 14:
        errors.append("manifest_scene_count_must_be_14")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or len(scenes) != 14:
        errors.append("manifest_must_have_14_scenes")
    else:
        for index, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                errors.append(f"manifest_scene_{index}_not_object")
                continue
            if scene.get("id") != f"s{index + 1:02d}":
                errors.append(f"manifest_scene_{index}_id_mismatch")
    return data, errors


def _probe_metadata(
    ffprobe: str,
    video: Path,
    manifest: dict[str, Any],
    *,
    duration_tolerance: float,
) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    check: dict[str, Any] = {
        "pass": False,
        "expected": {
            "width": EXPECTED_OUTPUT[0],
            "height": EXPECTED_OUTPUT[1],
            "fps": EXPECTED_FPS,
            "duration_s": manifest.get("canvas", {}).get("duration_s"),
        },
    }
    command = [
        ffprobe,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(video),
    ]
    try:
        result = _run(command, timeout_s=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(f"ffprobe_failed:{exc}")
        check["errors"] = errors[:]
        return check, errors, warnings
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        errors.append(f"ffprobe_failed:{detail[:500]}")
        check["errors"] = errors[:]
        return check, errors, warnings
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"ffprobe_json_invalid:{exc}")
        check["errors"] = errors[:]
        return check, errors, warnings

    streams = data.get("streams") if isinstance(data, dict) else None
    streams = streams if isinstance(streams, list) else []
    video_streams = [stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "audio"]
    if not video_streams:
        errors.append("video_stream_missing")
        check["audio_present"] = bool(audio_streams)
        check["errors"] = errors[:]
        return check, errors, warnings

    stream = video_streams[0]
    width = stream.get("width")
    height = stream.get("height")
    fps = _ratio(stream.get("avg_frame_rate")) or _ratio(stream.get("r_frame_rate"))
    stream_duration = _float(stream.get("duration"))
    format_data = data.get("format") if isinstance(data, dict) else None
    format_duration = _float(format_data.get("duration")) if isinstance(format_data, dict) else None
    duration = stream_duration if stream_duration is not None else format_duration
    check["actual"] = {
        "width": width,
        "height": height,
        "fps": fps,
        "duration_s": duration,
        "codec": stream.get("codec_name"),
        "pix_fmt": stream.get("pix_fmt"),
        "audio_present": bool(audio_streams),
    }
    if width != EXPECTED_OUTPUT[0] or height != EXPECTED_OUTPUT[1]:
        errors.append(f"output_dimensions_mismatch:{width}x{height}")
    if fps is None or abs(fps - EXPECTED_FPS) > FPS_TOLERANCE:
        errors.append(f"output_fps_mismatch:{fps}")
    expected_duration = _float(manifest.get("canvas", {}).get("duration_s"))
    if duration is None:
        errors.append("output_duration_missing")
    elif expected_duration is not None:
        difference = abs(duration - expected_duration)
        if difference > duration_tolerance:
            errors.append(f"output_duration_mismatch:{duration:.3f}s")
        elif difference > 0.05:
            warnings.append(f"output_duration_delta:{duration - expected_duration:+.3f}s")
    if not audio_streams:
        warnings.append("audio_stream_missing")
    check["pass"] = not errors
    if errors:
        check["errors"] = errors[:]
    if warnings:
        check["warnings"] = warnings[:]
    return check, errors, warnings


def _scene_samples(manifest: dict[str, Any], actual_duration: float | None, fps: float | None) -> list[dict[str, Any]]:
    """Build deterministic boundary + midpoint samples from the manifest."""

    timeline = manifest.get("timeline", {})
    raw_boundaries = timeline.get("boundaries_s", []) if isinstance(timeline, dict) else []
    boundaries = [_float(value) for value in raw_boundaries]
    boundaries = [value for value in boundaries if value is not None]
    scenes = manifest.get("scenes", [])
    duration = actual_duration or _float(manifest.get("canvas", {}).get("duration_s")) or boundaries[-1]
    frame_step = 1.0 / (fps or EXPECTED_FPS)
    # FFmpeg may round an exact duration to the timestamp immediately after
    # the final decodable frame.  Keep two frame intervals of headroom for the
    # endpoint probe; this is still a deterministic probe of the final scene.
    last_safe_time = max(0.0, duration - 2.0 * frame_step)
    samples: list[dict[str, Any]] = []

    for index, time_s in enumerate(boundaries):
        probe_time = min(max(time_s, 0.0), last_safe_time)
        samples.append(
            {
                "kind": "boundary",
                "scene_id": f"s{min(index + 1, 14):02d}",
                "manifest_time_s": time_s,
                "probe_time_s": probe_time,
                "clamped": abs(probe_time - time_s) > BOUNDARY_TOLERANCE,
            }
        )
    for index, scene in enumerate(scenes[:14]):
        if not isinstance(scene, dict):
            continue
        start = _float(scene.get("start_s"))
        end = _float(scene.get("end_s"))
        if start is None or end is None:
            continue
        midpoint = (start + end) / 2.0
        probe_time = min(max(midpoint, 0.0), last_safe_time)
        samples.append(
            {
                "kind": "midpoint",
                "scene_id": str(scene.get("id", f"s{index + 1:02d}")),
                "manifest_time_s": midpoint,
                "probe_time_s": probe_time,
                "clamped": abs(probe_time - midpoint) > BOUNDARY_TOLERANCE,
            }
        )
    return samples


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _extract_frame(ffmpeg: str, video: Path, output: Path, time_s: float) -> tuple[bool, str | None]:
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{time_s:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-an",
        str(output),
    ]
    try:
        result = _run(command, timeout_s=90)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        return False, detail[:500]
    if not output.is_file() or output.stat().st_size == 0:
        return False, "frame_output_missing_or_empty"
    return True, None


def _concat_list(samples: Iterable[Path], path: Path) -> None:
    """Write a temporary FFmpeg concat list, escaping absolute Windows paths."""

    items = list(samples)
    lines: list[str] = []
    for image in items:
        normalized = str(image.resolve()).replace("\\", "/").replace("'", "'\\''")
        lines.extend([f"file '{normalized}'", "duration 1"])
    if items:
        normalized = str(items[-1].resolve()).replace("\\", "/").replace("'", "'\\''")
        lines.append(f"file '{normalized}'")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _make_contact_sheet(ffmpeg: str, samples: list[Path], output: Path) -> tuple[bool, str | None, str | None]:
    if not samples:
        return False, "no_extracted_frames", None
    pattern = str(output.parent / "sample_*.png")
    primary = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-framerate",
        "1",
        "-pattern_type",
        "glob",
        "-i",
        pattern,
        "-vf",
        "scale=240:-2:force_original_aspect_ratio=decrease,tile=5x6:padding=8:margin=8:color=black",
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output),
    ]
    try:
        result = _run(primary, timeout_s=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        result = None
        primary_error = str(exc)
    else:
        primary_error = (result.stderr or result.stdout).strip().replace("\n", " ")[:500]
    if result is not None and result.returncode == 0 and output.is_file() and output.stat().st_size:
        return True, None, "glob"

    # Some Windows FFmpeg builds omit the image2 glob demuxer.  The concat
    # fallback is still deterministic and keeps the probe portable.
    list_path = output.parent / ".contact-input-v8.txt"
    try:
        _concat_list(samples, list_path)
        fallback = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-vf",
            "fps=1,scale=240:-2:force_original_aspect_ratio=decrease,tile=5x6:padding=8:margin=8:color=black",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(output),
        ]
        fallback_result = _run(fallback, timeout_s=120)
        fallback_error = (fallback_result.stderr or fallback_result.stdout).strip().replace("\n", " ")[:500]
    except (OSError, subprocess.TimeoutExpired) as exc:
        fallback_result = None
        fallback_error = str(exc)
    finally:
        try:
            list_path.unlink(missing_ok=True)
        except OSError:
            pass
    if fallback_result is not None and fallback_result.returncode == 0 and output.is_file() and output.stat().st_size:
        return True, None, "concat"
    return False, f"contact_sheet_failed:{fallback_error or primary_error or 'unknown'}", None


FREEZE_START = re.compile(r"freeze_start:\s*([0-9]+(?:\.[0-9]+)?)")
FREEZE_END = re.compile(
    r"freeze_end:\s*([0-9]+(?:\.[0-9]+)?)(?:\s+freeze_duration:\s*([0-9]+(?:\.[0-9]+)?))?"
)


def _detect_freezes(ffmpeg: str, video: Path, threshold_s: float) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    check: dict[str, Any] = {"pass": False, "threshold_s": threshold_s, "events": []}
    threshold = max(0.01, threshold_s)
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "info",
        "-i",
        str(video),
        "-vf",
        f"freezedetect=n=0.003:d={threshold:.3f}",
        "-an",
        "-f",
        "null",
        "-",
    ]
    try:
        result = _run(command, timeout_s=300)
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(f"freezedetect_failed:{exc}")
        check["errors"] = errors[:]
        return check, errors
    log = "\n".join(part for part in (result.stdout, result.stderr) if part)
    current: dict[str, Any] | None = None
    for line in log.splitlines():
        start_match = FREEZE_START.search(line)
        if start_match:
            if current is not None:
                check["events"].append(current)
            current = {"start_s": float(start_match.group(1))}
            continue
        end_match = FREEZE_END.search(line)
        if end_match:
            end_s = float(end_match.group(1))
            duration = float(end_match.group(2)) if end_match.group(2) else None
            event = current or {}
            event["end_s"] = end_s
            event["duration_s"] = duration if duration is not None else end_s - float(event.get("start_s", end_s))
            check["events"].append(event)
            current = None
    if current is not None:
        current["unclosed"] = True
        check["events"].append(current)
    if current is not None:
        errors.append("freeze_event_unclosed")
    for index, event in enumerate(check["events"]):
        duration = _float(event.get("duration_s"))
        if duration is None or duration >= threshold:
            errors.append(f"freeze_{index}_at_least_{threshold:.2f}s")
    if result.returncode != 0 and not check["events"]:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        errors.append(f"freezedetect_failed:{detail[:500]}")
    check["pass"] = not errors
    if errors:
        check["errors"] = errors[:]
    return check, errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="rendered MP4 to probe")
    parser.add_argument("manifest", type=Path, nargs="?", default=DEFAULT_MANIFEST, help="frozen scene manifest")
    parser.add_argument("--out-dir", type=Path, help="directory for samples and contact sheet")
    parser.add_argument("--ffmpeg", help="path to ffmpeg executable")
    parser.add_argument("--ffprobe", help="path to ffprobe executable")
    parser.add_argument("--freeze-threshold", type=float, default=1.0, help="freeze duration gate in seconds (default: 1.0)")
    parser.add_argument("--duration-tolerance", type=float, default=0.5, help="allowed duration delta in seconds")
    parser.add_argument("--require-audio", action="store_true", help="fail when the MP4 has no audio stream")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    video = args.video.resolve()
    manifest_path = args.manifest.resolve()
    output_dir = (args.out_dir or video.parent / f"{video.stem}.frame-probe-v8").resolve()
    report: dict[str, Any] = {
        "schema_version": "mcd-frame-probe-v8",
        "video": str(video),
        "manifest": str(manifest_path),
        "out_dir": str(output_dir),
        "pass": False,
        "checks": {},
        "errors": [],
        "warnings": [],
    }
    errors: list[str] = report["errors"]
    warnings: list[str] = report["warnings"]

    if not video.is_file():
        errors.append(f"video_missing:{video}")
    manifest, manifest_errors = _load_manifest(manifest_path)
    errors.extend(manifest_errors)
    ffmpeg = _tool_path("ffmpeg", args.ffmpeg)
    ffprobe = _tool_path("ffprobe", args.ffprobe)
    if ffmpeg is None:
        errors.append("ffmpeg_not_found")
    if ffprobe is None:
        errors.append("ffprobe_not_found")
    if manifest is None or not video.is_file() or ffmpeg is None or ffprobe is None:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        errors.append(f"output_dir_unwritable:{exc}")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    metadata, metadata_errors, metadata_warnings = _probe_metadata(
        ffprobe,
        video,
        manifest,
        duration_tolerance=max(0.0, args.duration_tolerance),
    )
    report["checks"]["metadata"] = metadata
    errors.extend(metadata_errors)
    warnings.extend(metadata_warnings)
    actual = metadata.get("actual", {}) if isinstance(metadata, dict) else {}
    actual_duration = _float(actual.get("duration_s")) if isinstance(actual, dict) else None
    actual_fps = _float(actual.get("fps")) if isinstance(actual, dict) else None
    if args.require_audio and not bool(actual.get("audio_present")):
        errors.append("audio_stream_required")

    samples = _scene_samples(manifest, actual_duration, actual_fps)
    report["checks"]["sample_plan"] = {
        "pass": len(samples) == 29,
        "expected_count": 29,
        "actual_count": len(samples),
        "samples": samples,
    }
    if len(samples) != 29:
        errors.append(f"sample_plan_count:{len(samples)}")

    extracted: list[Path] = []
    sample_results: list[dict[str, Any]] = []
    for index, sample in enumerate(samples):
        filename = (
            f"sample_{index:03d}_{sample['kind']}_{_safe_name(str(sample['scene_id']))}_"
            f"t{float(sample['manifest_time_s']):07.3f}.png"
        )
        path = output_dir / filename
        ok, detail = _extract_frame(ffmpeg, video, path, float(sample["probe_time_s"]))
        result = dict(sample)
        result["path"] = str(path)
        result["pass"] = ok
        if detail:
            result["error"] = detail
            errors.append(f"frame_extract_{index}:{detail}")
        if ok:
            extracted.append(path)
        sample_results.append(result)
    report["checks"]["frame_extraction"] = {
        "pass": len(extracted) == len(samples),
        "expected_count": len(samples),
        "actual_count": len(extracted),
        "samples": sample_results,
    }

    contact_path = output_dir / "contact-sheet-v8.jpg"
    contact_ok, contact_error, contact_method = _make_contact_sheet(ffmpeg, extracted, contact_path)
    contact_check: dict[str, Any] = {
        "pass": contact_ok,
        "path": str(contact_path),
        "method": contact_method,
    }
    if contact_error:
        contact_check["error"] = contact_error
        errors.append(contact_error)
    report["checks"]["contact_sheet"] = contact_check

    freeze_check, freeze_errors = _detect_freezes(ffmpeg, video, max(0.01, args.freeze_threshold))
    report["checks"]["freezes"] = freeze_check
    errors.extend(freeze_errors)

    report["pass"] = not errors
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
