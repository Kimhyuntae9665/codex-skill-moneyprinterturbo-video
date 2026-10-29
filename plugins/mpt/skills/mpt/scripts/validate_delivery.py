"""Validate the truthful aggregate status for an evidence-motion delivery."""
from __future__ import annotations

import argparse
import hashlib
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
    "scene_probe_report",
)

ROUTES = {"news-explainer", "investment-analysis", "general-explainer"}
CONTENT_KINDS = {"company", "stock", "ai", "technology", "general"}


def finite_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)


def union_seconds(intervals: list[tuple[float, float]]) -> float:
    end = -math.inf
    total = 0.0
    for start, stop in sorted(intervals):
        total += max(0.0, stop - max(start, end))
        end = max(end, stop)
    return total


def checked_intervals(rows: object, start_key: str, end_key: str,
                      duration: float, label: str, errors: list[str],
                      required: tuple[str, ...] = ()) -> list[tuple[float, float]]:
    if not isinstance(rows, list) or not rows:
        errors.append(f"{label} must contain measured intervals")
        return []
    result = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        start, end = row.get(start_key), row.get(end_key)
        if not (finite_number(start) and finite_number(end) and 0 <= start < end <= duration):
            errors.append(f"{label}[{index}] must satisfy 0 <= start < end <= final duration")
            continue
        for field in required:
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{label}[{index}].{field} is required review evidence")
        result.append((float(start), float(end)))
    return result


def check_total(report: dict, key: str, actual: float, errors: list[str], label: str) -> None:
    value = report.get(key)
    if not finite_number(value) or not math.isclose(value, actual, rel_tol=1e-7, abs_tol=1e-6):
        errors.append(f"{label}.{key} does not match recomputed value {actual:.9g}")


def validate_share_reports(official: dict, news: dict | None, duration: float,
                           errors: list[str]) -> None:
    rows = checked_intervals(official.get("intervals"), "output_start_s", "output_end_s",
        duration, "official.intervals", errors,
        ("scene_id", "asset_id", "official_publisher", "source_page_url", "source_media_url",
         "narration_match", "review_evidence"))
    for index, row in enumerate(official.get("intervals", []) if isinstance(official.get("intervals"), list) else []):
        if not isinstance(row, dict):
            continue
        a, b = row.get("source_in_s"), row.get("source_out_s")
        if not (finite_number(a) and finite_number(b) and 0 <= a < b):
            errors.append(f"official.intervals[{index}] needs valid source in/out times")
    used = union_seconds(rows)
    check_total(official, "duration_s", duration, errors, "official")
    check_total(official, "official_video_s", used, errors, "official")
    check_total(official, "official_video_share", used / duration, errors, "official")
    if used / duration < 0.60 - 1e-9:
        errors.append("recomputed official-video share is below 0.60")
    if news is None:
        return
    narrated = checked_intervals(news.get("narrated_intervals"), "start_s", "end_s",
                                duration, "news.narrated_intervals", errors)
    context = checked_intervals(news.get("intervals"), "start_s", "end_s", duration,
        "news.intervals", errors, ("spoken_point", "source_url", "source_date", "review_evidence"))
    for start, end in context:
        intersection = [(max(start, a), min(end, b)) for a, b in narrated if max(start, a) < min(end, b)]
        if not math.isclose(union_seconds(intersection), end - start, abs_tol=1e-6):
            errors.append("news interval extends outside measured narrated intervals")
    spoken, used_news = union_seconds(narrated), union_seconds(context)
    check_total(news, "duration_s", duration, errors, "news")
    check_total(news, "narrated_s", spoken, errors, "news")
    check_total(news, "news_context_s", used_news, errors, "news")
    share = used_news / spoken if spoken else 0.0
    check_total(news, "news_context_share", share, errors, "news")
    if share < 0.30 - 1e-9:
        errors.append("recomputed news-context share is below 0.30")


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

    if payload.get("schema_version") != "mpt-delivery-status-v2":
        errors.append("schema_version must be mpt-delivery-status-v2; migrate old status/report evidence")
    route = payload.get("editorial_route")
    kind = payload.get("content_kind")
    if not isinstance(route, str) or route not in ROUTES:
        errors.append("editorial_route must select news-explainer, investment-analysis, or general-explainer")
    if not isinstance(kind, str) or kind not in CONTENT_KINDS:
        errors.append("content_kind must select company, stock, ai, technology, or general")
    news_required = isinstance(kind, str) and kind in CONTENT_KINDS - {"general"}
    if news_required and payload.get("news_context_qa") != "PASS":
        errors.append("news_context_qa must be PASS for company/stock/AI/technology content")
    if route == "investment-analysis" and payload.get("verdict_qa") != "PASS":
        errors.append("investment-analysis requires performed verdict_qa=PASS")
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
    if type(planned) is not int or planned < 0:
        errors.append("emphasis_plan_count must be a non-negative integer")
    if type(actual) is not int or actual < 0:
        errors.append("emphasis_cue_count must be a non-negative integer")
    if type(planned) is int and type(actual) is int and actual < planned:
        errors.append("emphasis_cue_count is lower than emphasis_plan_count")

    artifacts = payload.get("artifacts")
    reports: dict[str, dict] = {}
    production: dict = {}
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
    else:
        for field in ARTIFACT_FIELDS + (("news_context_report",) if news_required else ()):
            raw = artifacts.get(field)
            if not isinstance(raw, str) or not raw:
                errors.append(f"artifacts.{field} is required")
                continue
            artifact = Path(raw)
            if not artifact.is_absolute():
                errors.append(f"artifacts.{field} must be absolute")
            elif not artifact.is_file() or artifact.stat().st_size == 0:
                errors.append(f"artifacts.{field} does not exist or is empty")
        for field in ("layout_report", "video_report", "official_video_report", "scene_probe_report") + (("news_context_report",) if news_required else ()):
            raw = artifacts.get(field)
            if isinstance(raw, str) and Path(raw).is_file():
                try:
                    report = load_json(Path(raw))
                    reports[field] = report
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

        video_path = artifacts.get("video")
        if isinstance(video_path, str) and Path(video_path).is_file():
            with Path(video_path).open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            for field in ("video_report", "scene_probe_report", "official_video_report") + (("news_context_report",) if news_required else ()):
                if reports.get(field, {}).get("video_sha256") != digest:
                    errors.append(f"{field}.video_sha256 must match the actual final MP4")
        production_path = artifacts.get("production")
        if isinstance(production_path, str) and Path(production_path).is_file():
            try:
                production = load_json(Path(production_path))
                if production.get("editorial_route") != route or production.get("content_kind") != kind:
                    errors.append("production route/content_kind differs from delivery status")
            except (OSError, ValueError) as exc:
                errors.append(f"could not read production: {exc}")

    duration = reports.get("video_report", {}).get("duration")
    if not finite_number(duration) or duration <= 0:
        errors.append("video_report must record a positive finite measured duration")
        duration = None
    if duration is not None and "official_video_report" in reports:
        validate_share_reports(reports["official_video_report"], reports.get("news_context_report"), duration, errors)
    strategy = production.get("strategy")
    strategy = strategy if isinstance(strategy, dict) else {}
    profile = strategy.get("duration_profile")
    if profile not in ("focused", "full", "custom"):
        errors.append("production strategy must select a duration_profile")
    elif reports.get("video_report", {}).get("duration_profile") != profile:
        errors.append("video_report duration_profile differs from production")
    bounds = {"focused": [25.0, 35.0], "full": [45.0, 60.0]}.get(profile) if isinstance(profile, str) else None
    if profile == "custom":
        bounds = strategy.get("duration_bounds_s")
    if profile in ("focused", "full", "custom"):
        if (not isinstance(bounds, list) or len(bounds) != 2 or
                not all(finite_number(value) for value in bounds) or not 0 < bounds[0] <= bounds[1]):
            errors.append("production duration bounds must be positive finite [minimum, maximum]")
        elif duration is not None and not bounds[0] <= duration <= bounds[1]:
            errors.append("measured duration is outside the canonical production profile/bounds")

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
            if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
                errors.append(f"reviews.{kind}.reviewer must identify who actually performed the review")
            if not isinstance(observations, list) or not any(
                isinstance(item, str) and item.strip() for item in observations
            ):
                errors.append(f"reviews.{kind}.observations must contain a concrete observation")
        visual = reviews.get("visual")
        if isinstance(visual, dict):
            stamps = visual.get("timestamps_s")
            if not isinstance(stamps, list) or not stamps:
                errors.append("reviews.visual.timestamps_s must not be empty")
            elif any(not finite_number(stamp) or stamp < 0 or (duration is not None and stamp > duration) for stamp in stamps):
                errors.append("reviews.visual.timestamps_s must be finite and within the final video")

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
