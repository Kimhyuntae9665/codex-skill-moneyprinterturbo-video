from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path


def pcm_rms(raw: bytes, width: int) -> float:
    """RMS of little-endian integer PCM, including unsigned 8-bit WAV.

    Standard-library implementation also supports Python 3.13+, without audioop.
    Channel samples are combined, matching the original window audit.
    """
    if width not in (1, 2, 3, 4):
        raise ValueError("PCM sample width must be 1, 2, 3, or 4 bytes")
    if len(raw) % width:
        raise ValueError("Incomplete PCM sample")
    if not raw:
        return 0.0
    samples = ((value - 128) for value in raw) if width == 1 else (
        int.from_bytes(raw[i:i + width], "little", signed=True)
        for i in range(0, len(raw), width)
    )
    return math.sqrt(sum(sample * sample for sample in samples) / (len(raw) // width))


def main() -> None:
    parser = argparse.ArgumentParser(description="Report silent runs in a PCM WAV without editing it.")
    parser.add_argument("wav", type=Path)
    parser.add_argument("--threshold-dbfs", type=float, default=-55.0)
    parser.add_argument("--min-duration", type=float, default=0.20)
    parser.add_argument("--window-ms", type=float, default=10.0)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.window_ms <= 0 or args.min_duration < 0:
        parser.error("window-ms must be positive and min-duration nonnegative")

    with wave.open(str(args.wav), "rb") as src:
        channels = src.getnchannels()
        width = src.getsampwidth()
        rate = src.getframerate()
        frames = src.getnframes()
        chunk_frames = max(1, round(rate * args.window_ms / 1000))
        full_scale = float((1 << (8 * width - 1)) - 1)
        silent = []
        index = 0
        while True:
            raw = src.readframes(chunk_frames)
            if not raw:
                break
            rms = pcm_rms(raw, width)
            dbfs = -120.0 if rms == 0 else 20 * math.log10(rms / full_scale)
            silent.append((index / rate, min(frames, index + chunk_frames) / rate, dbfs <= args.threshold_dbfs))
            index += chunk_frames

    runs = []
    start = None
    end = None
    for a, b, is_silent in silent:
        if is_silent and start is None:
            start = a
        if is_silent:
            end = b
        elif start is not None:
            if end - start >= args.min_duration:
                runs.append({"start_s": round(start, 4), "end_s": round(end, 4), "duration_s": round(end - start, 4)})
            start = end = None
    if start is not None and end - start >= args.min_duration:
        runs.append({"start_s": round(start, 4), "end_s": round(end, 4), "duration_s": round(end - start, 4)})

    report = {
        "input": str(args.wav.resolve()),
        "duration_s": round(frames / rate, 4),
        "channels": channels,
        "sample_width_bytes": width,
        "sample_rate": rate,
        "threshold_dbfs": args.threshold_dbfs,
        "min_duration_s": args.min_duration,
        "window_ms": args.window_ms,
        "silent_runs": runs,
        "silent_total_s": round(sum(item["duration_s"] for item in runs), 4),
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
