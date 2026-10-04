#!/usr/bin/env python3
"""Validate the minimum evidence and story invariants for Wall Street Edge Shorts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


VALID_GRADES = {"A", "B", "C", "D"}
APPROVED_GRADES = {"A", "B"}
VALID_VERDICTS = {"recommend", "watch", "avoid"}
VALID_STORY_MODES = {"focused_reveal", "connected_dossier"}
VALID_SCAN_STATUSES = {"used", "partial", "unavailable", "not_needed"}
VALID_EDITORIAL_MODES = {"company_story", "investment_story"}
VALID_RENDERERS = {"2d_2.5d_default", "motion_canvas", "remotion_2.5d", "prevalidated_3d_rig", "blender_blockout_gated", "auto"}


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(packet: dict) -> list[str]:
    errors: list[str] = []

    for key in ("story_id", "as_of", "issuer", "ticker", "viewer_question"):
        if not nonempty(packet.get(key)):
            errors.append(f"missing non-empty field: {key}")

    story_mode = packet.get("story_mode", "focused_reveal")
    if story_mode not in VALID_STORY_MODES:
        errors.append("story_mode must be focused_reveal or connected_dossier")

    editorial_mode = packet.get("editorial_mode", "investment_story")
    if editorial_mode not in VALID_EDITORIAL_MODES:
        errors.append("editorial_mode must be company_story or investment_story")

    schema_version = packet.get("schema_version", "")
    duration_plan = packet.get("duration_plan")
    if schema_version == "wallstreet-edge-story-packet-v2":
        if not isinstance(duration_plan, dict):
            errors.append("duration_plan must be an object for v2 packets")
        else:
            target_seconds = duration_plan.get("target_seconds")
            item_floor = duration_plan.get("minimum_seconds_per_dossier_item")
            if not isinstance(target_seconds, (int, float)) or target_seconds <= 0:
                errors.append("duration_plan.target_seconds must be a positive number")
            if not isinstance(item_floor, (int, float)) or not 18 <= item_floor <= 25:
                errors.append("duration_plan.minimum_seconds_per_dossier_item must be between 18 and 25")

    claims = packet.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []

    claim_by_id: dict[str, dict] = {}
    has_primary_a = False
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claim_id = claim.get("id")
        if not nonempty(claim_id):
            errors.append(f"{prefix}.id is required")
        elif claim_id in claim_by_id:
            errors.append(f"duplicate claim id: {claim_id}")
        else:
            claim_by_id[claim_id] = claim

        grade = claim.get("grade")
        if grade not in VALID_GRADES:
            errors.append(f"{prefix}.grade must be A, B, C, or D")
        primary_urls = claim.get("primary_urls", [])
        if not isinstance(primary_urls, list) or any(not is_http_url(url) for url in primary_urls):
            errors.append(f"{prefix}.primary_urls must contain only HTTP(S) URLs")
            primary_urls = []
        if grade == "A" and not primary_urls:
            errors.append(f"{prefix}: A-grade claim requires a primary URL")
        if grade == "A" and primary_urls and claim.get("status") == "approved":
            has_primary_a = True
        if not nonempty(claim.get("text")):
            errors.append(f"{prefix}.text is required")
        if not nonempty(claim.get("period")):
            errors.append(f"{prefix}.period is required")
        if not nonempty(claim.get("unit")):
            errors.append(f"{prefix}.unit is required; use NA when not applicable")

    if not has_primary_a:
        errors.append("at least one approved A-grade claim with a primary URL is required")

    selected = packet.get("selected_story")
    if not isinstance(selected, dict):
        errors.append("selected_story must be an object")
        selected = {}
    for key in (
        "hook",
        "signature_thesis",
        "economic_consequence",
        "counterpoint",
    ):
        if not nonempty(selected.get(key)):
            errors.append(f"selected_story.{key} is required")

    if editorial_mode == "company_story":
        if not nonempty(selected.get("closing_payoff")):
            errors.append("selected_story.closing_payoff is required for company_story")
        if selected.get("verdict_requirement") not in {"not_required", *VALID_VERDICTS}:
            errors.append("company_story verdict_requirement must be not_required, recommend, watch, or avoid")
    else:
        for key in ("valuation_bridge", "invalidation_condition"):
            if not nonempty(selected.get(key)):
                errors.append(f"selected_story.{key} is required for investment_story")
        if selected.get("verdict_requirement") not in VALID_VERDICTS:
            errors.append("investment_story verdict_requirement must be recommend, watch, or avoid")

    steps = selected.get("mechanism_steps")
    if not isinstance(steps, list) or not 3 <= len(steps) <= 6 or any(not nonempty(step) for step in steps):
        errors.append("selected_story.mechanism_steps must contain 3 to 6 non-empty steps")
    dossier_items = packet.get("dossier_items", [])
    if story_mode == "connected_dossier":
        if not isinstance(dossier_items, list) or not 2 <= len(dossier_items) <= 4:
            errors.append("connected_dossier requires 2 to 4 dossier_items")
            dossier_items = []
        for index, item in enumerate(dossier_items):
            prefix = f"dossier_items[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("title", "economic_meaning"):
                if not nonempty(item.get(key)):
                    errors.append(f"{prefix}.{key} is required")
            ids = item.get("claim_ids", [])
            if not isinstance(ids, list) or not ids:
                errors.append(f"{prefix}.claim_ids must be non-empty")
                continue
            item_claims = [claim_by_id.get(claim_id) for claim_id in ids]
            if any(claim is None for claim in item_claims):
                errors.append(f"{prefix}.claim_ids contains an unknown claim")
            if not any(
                claim and claim.get("grade") == "A" and claim.get("status") == "approved"
                for claim in item_claims
            ):
                errors.append(f"{prefix} requires at least one approved A-grade claim")
        if isinstance(duration_plan, dict) and isinstance(duration_plan.get("target_seconds"), (int, float)):
            minimum_by_count = {2: 75, 3: 100, 4: 130}
            required = minimum_by_count.get(len(dossier_items))
            if required and duration_plan["target_seconds"] < required:
                errors.append(
                    f"connected_dossier with {len(dossier_items)} items requires target_seconds >= {required}"
                )

    visuals = packet.get("visuals")
    if not isinstance(visuals, list) or not visuals:
        errors.append("visuals must be a non-empty list")
        visuals = []
    referenced_claims: set[str] = set()
    has_mechanism = False
    for index, visual in enumerate(visuals):
        if not isinstance(visual, dict):
            errors.append(f"visuals[{index}] must be an object")
            continue
        if visual.get("type") == "mechanism":
            has_mechanism = True
            if not nonempty(visual.get("persistent_subject")):
                errors.append(f"visuals[{index}].persistent_subject is required for mechanism scenes")
            states = visual.get("states")
            if not isinstance(states, list) or len(states) < 3 or any(not nonempty(state) for state in states):
                errors.append(f"visuals[{index}].states must contain at least three non-empty explanatory states")
            camera_path = visual.get("camera_path")
            if not isinstance(camera_path, list) or len(camera_path) != len(states or []):
                errors.append(f"visuals[{index}].camera_path must contain one entry per explanatory state")
            elif any(not nonempty(camera) for camera in camera_path):
                errors.append(f"visuals[{index}].camera_path entries must be non-empty")
            if not nonempty(visual.get("transition_purpose")):
                errors.append(f"visuals[{index}].transition_purpose is required for mechanism scenes")
        ids = visual.get("claim_ids", [])
        if not isinstance(ids, list) or not ids:
            errors.append(f"visuals[{index}].claim_ids must be non-empty")
            continue
        for claim_id in ids:
            if claim_id not in claim_by_id:
                errors.append(f"visuals[{index}] references unknown claim id: {claim_id}")
                continue
            referenced_claims.add(claim_id)
            claim = claim_by_id[claim_id]
            if claim.get("grade") not in APPROVED_GRADES or claim.get("status") != "approved":
                errors.append(f"visuals[{index}] uses an unapproved or C/D-grade claim: {claim_id}")
    if not has_mechanism:
        errors.append("at least one visual with type=mechanism is required")

    approved_ids = {
        claim_id
        for claim_id, claim in claim_by_id.items()
        if claim.get("status") == "approved" and claim.get("grade") in APPROVED_GRADES
    }
    if approved_ids and not (approved_ids & referenced_claims):
        errors.append("at least one approved A/B claim must be mapped to a visual")
    if story_mode == "connected_dossier" and isinstance(dossier_items, list):
        for index, item in enumerate(dossier_items):
            if not isinstance(item, dict):
                continue
            ids = item.get("claim_ids", [])
            if isinstance(ids, list) and ids and not (set(ids) & referenced_claims):
                errors.append(f"dossier_items[{index}] must map at least one claim to a visual")

    handoff = packet.get("production_handoff")
    if not isinstance(handoff, dict):
        errors.append("production_handoff must be an object")
    else:
        if handoff.get("standalone_thumbnail_required") is not True:
            errors.append("production_handoff.standalone_thumbnail_required must be true")
        if editorial_mode == "company_story":
            if handoff.get("story_motion_master_required") is not True:
                errors.append("company_story requires production_handoff.story_motion_master_required=true")
        elif handoff.get("ten_year_pe_required") is not True:
            errors.append("investment_story requires production_handoff.ten_year_pe_required=true")
        if schema_version == "wallstreet-edge-story-packet-v2":
            if handoff.get("motion_renderer") not in VALID_RENDERERS:
                errors.append("production_handoff.motion_renderer is not recognized")
            if handoff.get("new_3d_requires_blockout_gate") is not True:
                errors.append("v2 packets require production_handoff.new_3d_requires_blockout_gate=true")
            if not nonempty(handoff.get("three_d_fallback")):
                errors.append("v2 packets require production_handoff.three_d_fallback")

    x_scan = packet.get("x_scan")
    if not isinstance(x_scan, dict):
        errors.append("x_scan must be an object")
    else:
        if x_scan.get("status") not in VALID_SCAN_STATUSES:
            errors.append("x_scan.status must be used, partial, unavailable, or not_needed")
        posts = x_scan.get("posts", [])
        if not isinstance(posts, list):
            errors.append("x_scan.posts must be a list")
        else:
            if x_scan.get("status") == "used" and not posts:
                errors.append("x_scan.posts must be non-empty when x_scan.status=used")
            for index, post in enumerate(posts):
                if not isinstance(post, dict) or not is_http_url(post.get("url")):
                    errors.append(f"x_scan.posts[{index}] requires a valid HTTP(S) URL")

    reddit_scan = packet.get("reddit_scan")
    if reddit_scan is not None:
        if not isinstance(reddit_scan, dict):
            errors.append("reddit_scan must be an object")
        else:
            if reddit_scan.get("status") not in VALID_SCAN_STATUSES:
                errors.append("reddit_scan.status must be used, partial, unavailable, or not_needed")
            items = reddit_scan.get("items", [])
            if not isinstance(items, list):
                errors.append("reddit_scan.items must be a list")
            else:
                if reddit_scan.get("status") == "used" and not items:
                    errors.append("reddit_scan.items must be non-empty when reddit_scan.status=used")
                for index, item in enumerate(items):
                    if not isinstance(item, dict) or not is_http_url(item.get("url")):
                        errors.append(f"reddit_scan.items[{index}] requires a valid HTTP(S) URL")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_story_packet.py <story-packet.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not isinstance(packet, dict):
        print("ERROR: packet root must be a JSON object", file=sys.stderr)
        return 2

    errors = validate(packet)
    if errors:
        print("INVALID STORY PACKET")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID STORY PACKET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
