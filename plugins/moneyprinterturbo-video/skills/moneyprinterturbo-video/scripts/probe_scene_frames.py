#!/usr/bin/env python3
"""Probe a rendered Short against its scene contract.

Checks stream geometry, frame rate, duration, optional audio, every scene
boundary and midpoint, a contact sheet, and FFmpeg freeze detection. The script
does not edit the video. It prints JSON and exits nonzero on a required failure.
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
from typing import Any


def finite(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def ratio(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text in {"0/0", "N/A"}:
        return None
    try:
        if "/" in text:
            result = float(Fraction(text))
        else:
            result = float(text)
    except (ValueError, ZeroDivisionError):
        return None
    return result if math.isfinite(result) else None


def run(command: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )


def executable(name: str, override: str | None) -> str | None:
    if override:
        path = Path(override).expanduser().resolve()
        return str(path) if path.is_file() else None
    return shutil.which(name)


def load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"manifest_missing:{path}"]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"manifest_unreadable:{exc}"]
    if not isinstance(manifest, dict):
        return None, ["manifest_root_not_object"]
    errors: list[str] = []
    canvas = manifest.get("canvas")
    timeline = manifest.get("timeline")
    scenes = manifest.get("scenes")
    if not isinstance(canvas, dict) or not isinstance(canvas.get("output"), dict):
        errors.append("manifest_canvas_output_missing")
    if not isinstance(timeline, dict) or not isinstance(timeline.get("boundaries_s"), list):
        errors.append("manifest_boundaries_missing")
    if not isinstance(scenes, list) or not scenes:
        errors.append("manifest_scenes_missing")
    if errors:
        return manifest, errors
    boundaries = [finite(value) for value in timeline["boundaries_s"]]
    if any(value is None for value in boundaries):
        errors.append("manifest_boundaries_non_numeric")
    elif len(boundaries) != len(scenes) + 1:
        errors.append("manifest_boundary_count_mismatch")
    elif any(boundaries[index + 1] <= boundaries[index] for index in range(len(boundaries) - 1)):  # type: ignore[operator]
        errors.append("manifest_boundaries_not_increasing")
    return manifest, errors


def probe_metadata(
    ffprobe: str,
    video: Path,
    manifest: dict[str, Any],
    duration_tolerance: float,
    require_audio: bool,
) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(video),
    ]
    try:
        result = run(command, 90)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"pass": False}, [f"ffprobe_failed:{exc}"], warnings
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        return {"pass": False}, [f"ffprobe_failed:{detail[-500:]}"], warnings
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {"pass": False}, [f"ffprobe_invalid_json:{exc}"], warnings
    streams = data.get("streams", []) if isinstance(data, dict) else []
    video_streams = [stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "audio"]
    if not video_streams:
        return {"pass": False}, ["video_stream_missing"], warnings
    stream = video_streams[0]
    actual_width = stream.get("width")
    actual_height = stream.get("height")
    actual_fps = ratio(stream.get("avg_frame_rate")) or ratio(stream.get("r_frame_rate"))
    format_data = data.get("format", {}) if isinstance(data, dict) else {}
    actual_duration = finite(stream.get("duration")) or finite(format_data.get("duration"))

    canvas = manifest["canvas"]
    expected_output = canvas["output"]
    expected_width = expected_output.get("width")
    expected_height = expected_output.get("height")
    expected_fps = finite(canvas.get("fps"))
    expected_duration = finite(canvas.get("duration_s"))
    if actual_width != expected_width or actual_height != expected_height:
        errors.append(f"resolution_mismatch:{actual_width}x{actual_height}")
    if actual_fps is None or expected_fps is None or abs(actual_fps - expected_fps) > 0.02:
        errors.append(f"fps_mismatch:{actual_fps}")
    if actual_duration is None:
        errors.append("duration_missing")
    elif expected_duration is not None and abs(actual_duration - expected_duration) > duration_tolerance:
        errors.append(f"duration_mismatch:{actual_duration:.3f}s")
    elif expected_duration is not None and abs(actual_duration - expected_duration) > 0.05:
        warnings.append(f"duration_delta:{actual_duration - expected_duration:+.3f}s")
    if require_audio and not audio_streams:
        errors.append("audio_stream_required")
    elif not audio_streams:
        warnings.append("audio_stream_missing")
    payload = {
        "pass": not errors,
        "expected": {
            "width": expected_width,
            "height": expected_height,
            "fps": expected_fps,
            "duration_s": expected_duration,
            "audio_required": require_audio,
        },
        "actual": {
            "width": actual_width,
            "height": actual_height,
            "fps": actual_fps,
            "duration_s": actual_duration,
            "video_codec": stream.get("codec_name"),
            "pixel_format": stream.get("pix_fmt"),
            "audio_present": bool(audio_streams),
            "audio_codec": audio_streams[0].get("codec_name") if audio_streams else None,
        },
    }
    return payload, errors, warnings


def sample_plan(manifest: dict[str, Any], actual_duration: float | None, actual_fps: float | None) -> list[dict[str, Any]]:
    boundaries = [float(value) for value in manifest["timeline"]["boundaries_s"]]
    scenes = manifest["scenes"]
    duration = actual_duration or finite(manifest["canvas"].get("duration_s")) or boundaries[-1]
    fps = actual_fps or finite(manifest["canvas"].get("fps")) or 30.0
    last_frame = max(0.0, duration - 2.0 / fps)
    samples: list[dict[str, Any]] = []
    for index, timestamp in enumerate(boundaries):
        probe_time = min(max(timestamp, 0.0), last_frame)
        samples.append(
            {
                "kind": "boundary",
                "scene_id": str(scenes[min(index, len(scenes) - 1)].get("id", index + 1)),
                "manifest_time_s": timestamp,
                "probe_time_s": probe_time,
                "clamped": abs(probe_time - timestamp) > 1e-6,
            }
        )
    for index, scene in enumerate(scenes):
        start = finite(scene.get("start_s"))
        end = finite(scene.get("end_s"))
        if start is None or end is None:
            continue
        midpoint = (start + end) / 2.0
        samples.append(
            {
                "kind": "midpoint",
                "scene_id": str(scene.get("id", index + 1)),
                "manifest_time_s": midpoint,
                "probe_time_s": min(max(midpoint, 0.0), last_frame),
                "clamped": midpoint > last_frame,
            }
        )
    return samples


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def extract_frame(ffmpeg: str, video: Path, output: Path, timestamp: float) -> tuple[bool, str | None]:
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{timestamp:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-an",
        str(output),
    ]
    try:
        result = run(command, 90)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    if result.returncode != 0 or not output.is_file() or output.stat().st_size == 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        return False, detail[-500:] or "empty frame output"
    return True, None


def write_concat_list(paths: list[Path], output: Path) -> None:
    lines: list[str] = []
    for path in paths:
        normalized = str(path.resolve()).replace("\\", "/").replace("'", "'\\''")
        lines.extend([f"file '{normalized}'", "duration 1"])
    if paths:
        normalized = str(paths[-1].resolve()).replace("\\", "/").replace("'", "'\\''")
        lines.append(f"file '{normalized}'")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_contact_sheet(ffmpeg: str, frames: list[Path], output: Path) -> tuple[bool, str | None]:
    if not frames:
        return False, "no_frames_for_contact_sheet"
    concat = output.parent / ".scene-probe-contact-input.txt"
    write_concat_list(frames, concat)
    columns = min(5, len(frames))
    rows = int(math.ceil(len(frames) / columns))
    command = [
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
        str(concat),
        "-vf",
        f"fps=1,scale=216:-2:force_original_aspect_ratio=decrease,tile={columns}x{rows}:padding=8:margin=8:color=black",
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output),
    ]
    try:
        result = run(command, 120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        result = None
        detail = str(exc)
    else:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
    finally:
        try:
            concat.unlink(missing_ok=True)
        except OSError:
            pass
    if result is None or result.returncode != 0 or not output.is_file() or output.stat().st_size == 0:
        return False, detail[-500:] or "contact_sheet_failed"
    return True, None


FREEZE_START = re.compile(r"freeze_start:\s*([0-9]+(?:\.[0-9]+)?)")
FREEZE_END = re.compile(r"freeze_end:\s*([0-9]+(?:\.[0-9]+)?)(?:\s+freeze_duration:\s*([0-9]+(?:\.[0-9]+)?))?")


def detect_freezes(ffmpeg: str, video: Path, threshold: float) -> tuple[dict[str, Any], list[str]]:
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
    errors: list[str] = []
    events: list[dict[str, Any]] = []
    try:
        result = run(command, 300)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"pass": False, "threshold_s": threshold, "events": []}, [f"freezedetect_failed:{exc}"]
    current: dict[str, Any] | None = None
    log = "\n".join((result.stdout, result.stderr))
    for line in log.splitlines():
        start_match = FREEZE_START.search(line)
        if start_match:
            current = {"start_s": float(start_match.group(1))}
        end_match = FREEZE_END.search(line)
        if end_match:
            end_s = float(end_match.group(1))
            event = current or {"start_s": end_s}
            event["end_s"] = end_s
            event["duration_s"] = float(end_match.group(2)) if end_match.group(2) else end_s - float(event["start_s"])
            events.append(event)
            current = None
    if current is not None:
        current["unclosed"] = True
        events.append(current)
        errors.append("freeze_event_unclosed")
    for index, event in enumerate(events):
        duration = finite(event.get("duration_s"))
        if duration is None or duration >= threshold:
            errors.append(f"freeze_{index}_at_least_{threshold:.2f}s")
    if result.returncode != 0 and not events:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        errors.append(f"freezedetect_failed:{detail[-500:]}")
    return {"pass": not errors, "threshold_s": threshold, "events": events}, errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    parser.add_argument("--freeze-threshold", type=float, default=1.0)
    parser.add_argument("--duration-tolerance", type=float, default=0.5)
    parser.add_argument("--require-audio", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    video = args.video.expanduser().resolve()
    manifest_path = args.manifest.expanduser().resolve()
    output_dir = (args.out_dir or video.parent / f"{video.stem}.scene-probe").expanduser().resolve()
    payload: dict[str, Any] = {
        "schema_version": "shorts-scene-probe-v1",
        "video": str(video),
        "manifest": str(manifest_path),
        "out_dir": str(output_dir),
        "pass": False,
        "checks": {},
        "errors": [],
        "warnings": [],
    }
    errors: list[str] = payload["errors"]
    warnings: list[str] = payload["warnings"]
    if not video.is_file() or video.stat().st_size == 0:
        errors.append(f"video_missing_or_empty:{video}")
    manifest, manifest_errors = load_manifest(manifest_path)
    errors.extend(manifest_errors)
    ffmpeg = executable("ffmpeg", args.ffmpeg)
    ffprobe = executable("ffprobe", args.ffprobe)
    if ffmpeg is None:
        errors.append("ffmpeg_not_found")
    if ffprobe is None:
        errors.append("ffprobe_not_found")
    if errors or manifest is None or ffmpeg is None or ffprobe is None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata, metadata_errors, metadata_warnings = probe_metadata(
        ffprobe,
        video,
        manifest,
        max(0.0, args.duration_tolerance),
        args.require_audio,
    )
    payload["checks"]["metadata"] = metadata
    errors.extend(metadata_errors)
    warnings.extend(metadata_warnings)
    actual = metadata.get("actual", {})
    samples = sample_plan(manifest, finite(actual.get("duration_s")), finite(actual.get("fps")))
    expected_samples = 2 * len(manifest["scenes"]) + 1
    payload["checks"]["sample_plan"] = {
        "pass": len(samples) == expected_samples,
        "expected_count": expected_samples,
        "actual_count": len(samples),
        "samples": samples,
    }
    if len(samples) != expected_samples:
        errors.append(f"sample_count_mismatch:{len(samples)}")

    extracted: list[Path] = []
    results: list[dict[str, Any]] = []
    for index, sample in enumerate(samples):
        filename = (
            f"sample_{index:03d}_{sample['kind']}_{safe_name(sample['scene_id'])}_"
            f"t{sample['manifest_time_s']:07.3f}.png"
        )
        output = output_dir / filename
        ok, detail = extract_frame(ffmpeg, video, output, sample["probe_time_s"])
        row = dict(sample)
        row.update({"path": str(output), "pass": ok})
        if detail:
            row["error"] = detail
            errors.append(f"frame_{index}:{detail}")
        if ok:
            extracted.append(output)
        results.append(row)
    payload["checks"]["frame_extraction"] = {
        "pass": len(extracted) == len(samples),
        "expected_count": len(samples),
        "actual_count": len(extracted),
        "samples": results,
    }

    contact = output_dir / "contact-sheet.jpg"
    contact_ok, contact_error = make_contact_sheet(ffmpeg, extracted, contact)
    payload["checks"]["contact_sheet"] = {"pass": contact_ok, "path": str(contact)}
    if contact_error:
        payload["checks"]["contact_sheet"]["error"] = contact_error
        errors.append(f"contact_sheet:{contact_error}")

    freezes, freeze_errors = detect_freezes(ffmpeg, video, max(0.01, args.freeze_threshold))
    payload["checks"]["freezes"] = freezes
    errors.extend(freeze_errors)
    payload["pass"] = not errors
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    report = args.report.expanduser().resolve() if args.report else output_dir / "scene-probe-report.json"
    try:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"could not write report: {exc}", file=sys.stderr)
        return 1
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
