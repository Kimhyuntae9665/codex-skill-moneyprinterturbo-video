#!/usr/bin/env python3
"""Validate a generated short video with FFprobe, FFmpeg, and log checks."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


class ValidationError(RuntimeError):
    """A user-actionable validation failure."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a MoneyPrinterTurbo MP4")
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--log-file", type=Path)
    parser.add_argument("--frames-dir", type=Path)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--min-duration", type=float, default=45.0)
    parser.add_argument("--max-duration", type=float, default=60.0)
    parser.add_argument("--video-codec", default="h264")
    parser.add_argument("--audio-codec", default="aac")
    parser.add_argument("--silence-floor-db", type=float, default=-55.0)
    parser.add_argument(
        "--allow-online-log-activity",
        action="store_true",
        help="skip prepared-local checks for LLM, stock, paid-video, and posting calls",
    )
    return parser.parse_args(argv)


def _tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise ValidationError(f"required executable was not found: {name}")
    return path


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
        check=False,
    )


def probe_video(video: Path) -> dict[str, object]:
    result = _run(
        [
            _tool("ffprobe"),
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(video),
        ]
    )
    if result.returncode != 0:
        raise ValidationError(f"ffprobe failed: {result.stderr.strip()[-500:]}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationError("ffprobe returned invalid JSON") from exc


def summarize_probe(probe: dict[str, object]) -> dict[str, object]:
    streams = probe.get("streams")
    if not isinstance(streams, list):
        raise ValidationError("ffprobe did not return a stream list")
    video_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "video"), None
    )
    audio_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "audio"), None
    )
    if not isinstance(video_stream, dict):
        raise ValidationError("video stream is missing")
    if not isinstance(audio_stream, dict):
        raise ValidationError("audio stream is missing")
    format_data = probe.get("format")
    if not isinstance(format_data, dict):
        raise ValidationError("container metadata is missing")
    try:
        duration = float(format_data["duration"])
        width = int(video_stream["width"])
        height = int(video_stream["height"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValidationError("required video metadata is invalid") from exc
    if not math.isfinite(duration) or duration <= 0:
        raise ValidationError(f"invalid duration: {duration}")
    return {
        "duration": duration,
        "width": width,
        "height": height,
        "video_codec": str(video_stream.get("codec_name") or ""),
        "audio_codec": str(audio_stream.get("codec_name") or ""),
        "video_streams": sum(
            1 for stream in streams if stream.get("codec_type") == "video"
        ),
        "audio_streams": sum(
            1 for stream in streams if stream.get("codec_type") == "audio"
        ),
    }


def validate_metadata(summary: dict[str, object], args: argparse.Namespace) -> None:
    failures: list[str] = []
    if summary["width"] != args.width or summary["height"] != args.height:
        failures.append(
            f"resolution {summary['width']}x{summary['height']} != "
            f"{args.width}x{args.height}"
        )
    duration = float(summary["duration"])
    if not args.min_duration <= duration <= args.max_duration:
        failures.append(
            f"duration {duration:.3f}s is outside "
            f"{args.min_duration:g}-{args.max_duration:g}s"
        )
    if summary["video_codec"] != args.video_codec:
        failures.append(
            f"video codec {summary['video_codec']!r} != {args.video_codec!r}"
        )
    if summary["audio_codec"] != args.audio_codec:
        failures.append(
            f"audio codec {summary['audio_codec']!r} != {args.audio_codec!r}"
        )
    if failures:
        raise ValidationError("; ".join(failures))


def validate_decode(video: Path) -> None:
    result = _run(
        [
            _tool("ffmpeg"),
            "-v",
            "error",
            "-i",
            str(video),
            "-f",
            "null",
            os.devnull,
        ]
    )
    if result.returncode != 0 or result.stderr.strip():
        raise ValidationError(
            f"full FFmpeg decode failed: {result.stderr.strip()[-1000:]}"
        )


def measure_mean_volume(video: Path) -> float:
    result = _run(
        [
            _tool("ffmpeg"),
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-map",
            "0:a:0",
            "-af",
            "volumedetect",
            "-f",
            "null",
            os.devnull,
        ]
    )
    match = re.search(r"mean_volume:\s*(-?inf|-?\d+(?:\.\d+)?)\s*dB", result.stderr)
    if result.returncode != 0 or not match:
        raise ValidationError("could not measure narration volume")
    if match.group(1) in {"inf", "-inf"}:
        return float("-inf")
    return float(match.group(1))


def validate_prepared_local_log(log_file: Path) -> None:
    if not log_file.is_file():
        raise ValidationError(f"generation log does not exist: {log_file}")
    text = log_file.read_text(encoding="utf-8", errors="replace")
    prohibited = {
        "LLM script generation": r"generating video script:\s*subject=",
        "Pexels search": r"searching videos on pexels:",
        "Pixabay search": r"searching videos on pixabay:",
        "Coverr search": r"searching videos on coverr:",
        "paid video generation": r"(?:seedance|wavespeed|loomloom).*(?:submit|paid task|generat)",
        "social cross-post": r"cross-post (?:started|completed|failed)",
    }
    hits = [label for label, pattern in prohibited.items() if re.search(pattern, text, re.I)]
    if hits:
        raise ValidationError(
            "prepared-local log contains prohibited activity: " + ", ".join(hits)
        )


def extract_review_frames(video: Path, duration: float, frames_dir: Path) -> list[Path]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    times = (1.0, duration / 2.0, max(1.0, duration - 1.0))
    paths: list[Path] = []
    for index, timestamp in enumerate(times, start=1):
        output = frames_dir / f"frame-{index}-{timestamp:.1f}s.png"
        result = _run(
            [
                _tool("ffmpeg"),
                "-y",
                "-v",
                "error",
                "-ss",
                f"{timestamp:.3f}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(output),
            ]
        )
        if result.returncode != 0 or not output.is_file() or output.stat().st_size == 0:
            raise ValidationError(
                f"failed to extract QA frame at {timestamp:.3f}s: {result.stderr[-500:]}"
            )
        paths.append(output.resolve())
    return paths


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    video = args.video.expanduser().resolve()
    try:
        if not video.is_file() or video.stat().st_size == 0:
            raise ValidationError(f"video file is missing or empty: {video}")
        summary = summarize_probe(probe_video(video))
        validate_metadata(summary, args)
        validate_decode(video)
        mean_volume = measure_mean_volume(video)
        if not math.isfinite(mean_volume) or mean_volume < args.silence_floor_db:
            raise ValidationError(
                f"narration is silent or too quiet: mean volume {mean_volume} dB"
            )
        if args.log_file and not args.allow_online_log_activity:
            validate_prepared_local_log(args.log_file.expanduser().resolve())
        frames = (
            extract_review_frames(
                video, float(summary["duration"]), args.frames_dir.expanduser().resolve()
            )
            if args.frames_dir
            else []
        )
    except (OSError, ValidationError) as exc:
        print(f"MPT_VIDEO_INVALID={exc}", file=sys.stderr)
        return 1

    payload = {
        "status": "valid",
        "video": str(video),
        **summary,
        "mean_volume_db": mean_volume,
        "review_frames": [str(path) for path in frames],
        "manual_review_required": True,
    }
    print("MPT_VIDEO_VALID")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
