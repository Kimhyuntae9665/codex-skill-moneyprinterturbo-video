"""Validate the truthful aggregate status for an evidence-motion delivery."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


PASS_FIELDS = (
    "video_qa",
    "audio_listening",
    "visual_review",
    "claim_lock",
    "layout_qa",
    "semantic_cut_qa",
    "thumbnail_qa",
    "official_video_qa",
)
ARTIFACT_FIELDS = (
    "video",
    "thumbnail",
    "production",
    "scene_manifest",
    "layout_report",
    "video_report",
    "upload_package",
    "official_video_report",
)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be an object")
    return value


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = load_json(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"could not load status: {exc}"]

    if payload.get("schema_version") != "mpt-delivery-status-v1":
        errors.append("schema_version must be mpt-delivery-status-v1")
    for field in PASS_FIELDS:
        if payload.get(field) != "PASS":
            errors.append(f"{field} must be PASS")

    share = payload.get("official_video_share")
    if (
        isinstance(share, bool)
        or not isinstance(share, (int, float))
        or not math.isfinite(share)
        or not 0.60 <= share <= 1.0
    ):
        errors.append("official_video_share must be a finite fraction between 0.60 and 1.0")

    planned = payload.get("emphasis_plan_count")
    actual = payload.get("emphasis_cue_count")
    if not isinstance(planned, int) or planned < 0:
        errors.append("emphasis_plan_count must be a non-negative integer")
    if not isinstance(actual, int) or actual < 0:
        errors.append("emphasis_cue_count must be a non-negative integer")
    if isinstance(planned, int) and isinstance(actual, int) and actual < planned:
        errors.append("emphasis_cue_count is lower than emphasis_plan_count")

    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
    else:
        for field in ARTIFACT_FIELDS:
            raw = artifacts.get(field)
            if not isinstance(raw, str) or not raw:
                errors.append(f"artifacts.{field} is required")
                continue
            artifact = Path(raw)
            if not artifact.is_absolute():
                errors.append(f"artifacts.{field} must be absolute")
            elif not artifact.exists() or artifact.stat().st_size == 0:
                errors.append(f"artifacts.{field} does not exist or is empty")
        for field in ("layout_report", "video_report", "official_video_report"):
            raw = artifacts.get(field)
            if isinstance(raw, str) and Path(raw).is_file():
                try:
                    report = load_json(Path(raw))
                    if report.get("pass") is not True:
                        errors.append(f"artifacts.{field} does not report pass=true")
                    if field == "official_video_report":
                        reported_share = report.get("official_video_share")
                        if (
                            isinstance(reported_share, bool)
                            or not isinstance(reported_share, (int, float))
                            or not math.isfinite(reported_share)
                            or not 0.60 <= reported_share <= 1.0
                        ):
                            errors.append("official_video_report share must be between 0.60 and 1.0")
                        elif reported_share != share:
                            errors.append("official_video_report share does not match delivery status")
                except (OSError, json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"artifacts.{field} is not valid JSON: {exc}")

    reviews = payload.get("reviews")
    if not isinstance(reviews, dict):
        errors.append("reviews must be an object")
    else:
        for kind in ("audio", "visual"):
            review = reviews.get(kind)
            if not isinstance(review, dict):
                errors.append(f"reviews.{kind} must be an object")
                continue
            observations = review.get("observations")
            if not isinstance(observations, list) or not any(
                isinstance(item, str) and item.strip() for item in observations
            ):
                errors.append(f"reviews.{kind}.observations must contain a concrete observation")
        visual = reviews.get("visual")
        if isinstance(visual, dict):
            stamps = visual.get("timestamps_s")
            if not isinstance(stamps, list) or not stamps:
                errors.append("reviews.visual.timestamps_s must not be empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("status", type=Path)
    args = parser.parse_args()
    errors = validate(args.status.expanduser().resolve())
    result = {"pass": not errors, "error_count": len(errors), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
