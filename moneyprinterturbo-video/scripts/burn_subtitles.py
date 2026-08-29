from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess


class SubtitleBurnError(RuntimeError):
    pass


def escape_filter_path(path: Path) -> str:
    """Escape a filesystem path for FFmpeg's subtitles filter syntax."""
    value = path.resolve().as_posix()
    for source, replacement in (
        ("\\", r"\\"),
        (":", r"\:"),
        ("'", r"\'"),
        (",", r"\,"),
        ("[", r"\["),
        ("]", r"\]"),
    ):
        value = value.replace(source, replacement)
    return value


def subtitle_filter(
    subtitle: Path,
    font_dir: Path,
    *,
    font_name: str,
    font_size: float,
    margin_v: int,
) -> str:
    style = ",".join(
        (
            f"FontName={font_name}",
            f"FontSize={font_size:g}",
            "PrimaryColour=&H00FFFFFF",
            "OutlineColour=&HCC000000",
            "BorderStyle=1",
            "Outline=1.2",
            "Shadow=0",
            "Alignment=2",
            f"MarginV={margin_v}",
        )
    )
    return (
        f"subtitles=filename='{escape_filter_path(subtitle)}'"
        f":fontsdir='{escape_filter_path(font_dir)}'"
        f":force_style='{style}'"
    )


def burn_subtitles(
    video: Path,
    subtitle: Path,
    output: Path,
    font_dir: Path,
    *,
    font_name: str = "Noto Sans KR",
    font_size: float = 11,
    margin_v: int = 66,
    overwrite: bool = False,
) -> dict[str, object]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SubtitleBurnError("ffmpeg is required")

    video = video.resolve()
    subtitle = subtitle.resolve()
    output = output.resolve()
    font_dir = font_dir.resolve()

    for label, path in (
        ("video", video),
        ("subtitle", subtitle),
        ("font directory", font_dir),
    ):
        if not path.exists():
            raise SubtitleBurnError(f"{label} does not exist: {path}")
    if video == output:
        raise SubtitleBurnError("output must not overwrite the source video")
    if output.exists() and not overwrite:
        raise SubtitleBurnError(f"output already exists: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "warning",
        "-i",
        str(video),
        "-map",
        "0:v:0",
        "-map",
        "0:a:0",
        "-vf",
        subtitle_filter(
            subtitle,
            font_dir,
            font_name=font_name,
            font_size=font_size,
            margin_v=margin_v,
        ),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "17",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        "-y" if overwrite else "-n",
        str(output),
    ]
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SubtitleBurnError(f"ffmpeg failed with exit code {result.returncode}")
    if not output.is_file() or output.stat().st_size <= 0:
        raise SubtitleBurnError(f"ffmpeg did not create a non-empty output: {output}")
    return {
        "video": str(video),
        "subtitle": str(subtitle),
        "output": str(output),
        "bytes": output.stat().st_size,
        "font_name": font_name,
        "font_size_ass_units": font_size,
        "margin_v_ass_units": margin_v,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Burn a reviewed SRT into a MoneyPrinterTurbo MP4 with FFmpeg/libass."
    )
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--subtitle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--font-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "fonts",
    )
    parser.add_argument("--font-name", default="Noto Sans KR")
    parser.add_argument("--font-size", type=float, default=11)
    parser.add_argument("--margin-v", type=int, default=66)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        summary = burn_subtitles(
            args.video,
            args.subtitle,
            args.output,
            args.font_dir,
            font_name=args.font_name,
            font_size=args.font_size,
            margin_v=args.margin_v,
            overwrite=args.overwrite,
        )
    except SubtitleBurnError as error:
        print(f"MPT_SUBTITLE_REPAIR_FAILED: {error}")
        return 2
    print("MPT_SUBTITLE_REPAIR_RESULT=" + json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
