#!/usr/bin/env python3
"""Validate an evidence-led Shorts scene contract.

The validator is renderer-independent. It checks the canvas, zones, timeline,
claim ledger, element containment, declared text lines, state-change timing,
and illegal rectangle intersections. It prints JSON and exits nonzero when a
required contract fails.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


TEXT_KINDS = {"text", "caption", "source"}
EPSILON = 1e-6


class QA:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.scenes: list[dict[str, Any]] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def payload(self) -> dict[str, Any]:
        return {
            "schema_version": "shorts-scene-qa-v1",
            "manifest": str(self.path),
            "pass": not self.errors,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "scene_reports": self.scenes,
        }


def number(value: Any, path: str, qa: QA) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        qa.error(f"{path}: expected finite number")
        return None
    result = float(value)
    if not math.isfinite(result):
        qa.error(f"{path}: expected finite number")
        return None
    return result


def rect(value: Any, path: str, qa: QA) -> tuple[float, float, float, float] | None:
    if not isinstance(value, list) or len(value) != 4:
        qa.error(f"{path}: expected [x, y, width, height]")
        return None
    parsed = [number(item, f"{path}[{index}]", qa) for index, item in enumerate(value)]
    if any(item is None for item in parsed):
        return None
    x, y, width, height = (float(item) for item in parsed if item is not None)
    if width <= 0 or height <= 0:
        qa.error(f"{path}: width and height must be positive")
        return None
    return x, y, width, height


def contains(outer: tuple[float, float, float, float], inner: tuple[float, float, float, float]) -> bool:
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner
    return (
        ix >= ox - EPSILON
        and iy >= oy - EPSILON
        and ix + iw <= ox + ow + EPSILON
        and iy + ih <= oy + oh + EPSILON
    )


def intersection_area(first: tuple[float, float, float, float], second: tuple[float, float, float, float]) -> float:
    ax, ay, aw, ah = first
    bx, by, bw, bh = second
    width = min(ax + aw, bx + bw) - max(ax, bx)
    height = min(ay + ah, by + bh) - max(ay, by)
    return max(0.0, width) * max(0.0, height)


def load(path: Path, qa: QA) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        qa.error(f"manifest not found: {path}")
        return None
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        qa.error(f"manifest unreadable: {exc}")
        return None
    if not isinstance(value, dict):
        qa.error("manifest root must be an object")
        return None
    return value


def validate_canvas(manifest: dict[str, Any], qa: QA) -> tuple[dict[str, tuple[float, float, float, float]], float | None]:
    schema = manifest.get("schema_version")
    if not isinstance(schema, str) or not schema:
        qa.error("schema_version: required non-empty string")

    canvas = manifest.get("canvas")
    if not isinstance(canvas, dict):
        qa.error("canvas: required object")
        canvas = {}
    logical = canvas.get("logical")
    output = canvas.get("output")
    if not isinstance(logical, dict):
        qa.error("canvas.logical: required object")
        logical = {}
    if not isinstance(output, dict):
        qa.error("canvas.output: required object")
        output = {}
    logical_width = number(logical.get("width"), "canvas.logical.width", qa)
    logical_height = number(logical.get("height"), "canvas.logical.height", qa)
    output_width = number(output.get("width"), "canvas.output.width", qa)
    output_height = number(output.get("height"), "canvas.output.height", qa)
    fps = number(canvas.get("fps"), "canvas.fps", qa)
    duration = number(canvas.get("duration_s"), "canvas.duration_s", qa)
    for label, value in (
        ("logical width", logical_width),
        ("logical height", logical_height),
        ("output width", output_width),
        ("output height", output_height),
        ("fps", fps),
        ("duration", duration),
    ):
        if value is not None and value <= 0:
            qa.error(f"canvas: {label} must be positive")
    if logical_width and logical_height and abs(logical_width / logical_height - 9 / 16) > 0.001:
        qa.warning("canvas.logical is not 9:16")
    if output_width and output_height and abs(output_width / output_height - 9 / 16) > 0.001:
        qa.warning("canvas.output is not 9:16")

    zones_raw = manifest.get("reserved_bboxes")
    safe_raw = manifest.get("safe_bboxes")
    if not isinstance(zones_raw, dict) or not zones_raw:
        qa.error("reserved_bboxes: required non-empty object")
        zones_raw = {}
    if not isinstance(safe_raw, dict) or not safe_raw:
        qa.error("safe_bboxes: required non-empty object")
        safe_raw = {}
    zones: dict[str, tuple[float, float, float, float]] = {}
    safe: dict[str, tuple[float, float, float, float]] = {}
    canvas_rect = (0.0, 0.0, logical_width or 0.0, logical_height or 0.0)
    for name, value in zones_raw.items():
        parsed = rect(value, f"reserved_bboxes.{name}", qa)
        if parsed is not None:
            zones[str(name)] = parsed
            if logical_width and logical_height and not contains(canvas_rect, parsed):
                qa.error(f"reserved_bboxes.{name}: outside logical canvas")
    for name, value in safe_raw.items():
        parsed = rect(value, f"safe_bboxes.{name}", qa)
        if parsed is None:
            continue
        safe[str(name)] = parsed
        if name not in zones:
            qa.error(f"safe_bboxes.{name}: no matching reserved zone")
        elif not contains(zones[str(name)], parsed):
            qa.error(f"safe_bboxes.{name}: not contained by reserved zone")
    for name in zones:
        if name not in safe:
            qa.error(f"safe_bboxes.{name}: missing")

    parents = manifest.get("zone_parents", {})
    if not isinstance(parents, dict):
        qa.error("zone_parents: expected object")
        parents = {}
    for child, parent in parents.items():
        if child not in zones or parent not in zones:
            qa.error(f"zone_parents.{child}: unknown zone {parent!r}")
        elif not contains(zones[parent], zones[child]):
            qa.error(f"zone_parents.{child}: child zone is outside {parent}")
    return safe, duration


def validate_claims(manifest: dict[str, Any], qa: QA) -> set[str]:
    raw = manifest.get("claims", {})
    if not isinstance(raw, dict):
        qa.error("claims: expected object")
        return set()
    required = ("display", "value", "unit", "as_of", "source_url", "definition")
    for claim_id, claim in raw.items():
        if not isinstance(claim_id, str) or not claim_id:
            qa.error("claims: claim IDs must be non-empty strings")
            continue
        if not isinstance(claim, dict):
            qa.error(f"claims.{claim_id}: expected object")
            continue
        for field in required:
            if field not in claim or claim[field] in (None, ""):
                qa.error(f"claims.{claim_id}.{field}: required")
    assets = manifest.get("assets", {})
    if not isinstance(assets, dict):
        qa.error("assets: expected object")
    else:
        for asset_id, asset in assets.items():
            if not isinstance(asset, dict):
                qa.error(f"assets.{asset_id}: expected object")
            elif not asset.get("rights_note"):
                qa.warning(f"assets.{asset_id}: rights_note missing")
    return {key for key in raw if isinstance(key, str)}


def claim_ids(value: Any, path: str, known: set[str], strict: bool, qa: QA) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        qa.error(f"{path}: expected list")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            qa.error(f"{path}[{index}]: expected non-empty string")
        else:
            result.append(item)
            if item not in known:
                message = f"{path}[{index}]: unmapped claim {item!r}"
                qa.error(message) if strict else qa.warning(message)
    return result


def is_ancestor(child: str, possible_parent: str, parents: dict[str, str | None]) -> bool:
    current = parents.get(child)
    visited: set[str] = set()
    while current and current not in visited:
        if current == possible_parent:
            return True
        visited.add(current)
        current = parents.get(current)
    return False


def validate_elements(
    raw: Any,
    path: str,
    fixed: list[dict[str, Any]],
    safe: dict[str, tuple[float, float, float, float]],
    known_claims: set[str],
    contract: dict[str, Any],
    qa: QA,
) -> tuple[list[dict[str, Any]], int]:
    if not isinstance(raw, list):
        qa.error(f"{path}: expected list")
        return [], 0
    elements: list[dict[str, Any]] = [dict(item) for item in fixed]
    elements.extend(dict(item) for item in raw if isinstance(item, dict))
    if len(elements) != len(fixed) + len(raw):
        qa.error(f"{path}: every element must be an object")

    strict_claims = bool(contract.get("fail_on_unmapped_claim", True))
    strict_bounds = bool(contract.get("fail_on_out_of_bounds", True))
    require_lines = bool(contract.get("require_text_line_fields", True))
    require_font_px = bool(contract.get("require_font_px", False))
    require_text_role = bool(contract.get("require_text_role", False))
    minimum_by_role_raw = contract.get("min_font_px_by_role", {})
    minimum_by_role = minimum_by_role_raw if isinstance(minimum_by_role_raw, dict) else {}
    max_caption_lines = int(contract.get("max_caption_lines", 2))
    ids: set[str] = set()
    parsed: dict[str, tuple[float, float, float, float]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    parents: dict[str, str | None] = {}

    for index, element in enumerate(elements):
        item_path = f"{path}[{index - len(fixed)}]" if index >= len(fixed) else f"fixed_elements[{index}]"
        element_id = element.get("id")
        if not isinstance(element_id, str) or not element_id:
            qa.error(f"{item_path}.id: required non-empty string")
            continue
        if element_id in ids:
            qa.error(f"{item_path}.id: duplicate {element_id!r}")
        ids.add(element_id)
        by_id[element_id] = element
        parents[element_id] = element.get("parent_id") if isinstance(element.get("parent_id"), str) else None
        zone = element.get("zone")
        if zone not in safe:
            qa.error(f"{item_path}.zone: unknown zone {zone!r}")
        parsed_rect = rect(element.get("bbox"), f"{item_path}.bbox", qa)
        if parsed_rect is not None:
            parsed[element_id] = parsed_rect
            if zone in safe and not contains(safe[zone], parsed_rect):
                message = f"{item_path}.bbox: outside safe zone {zone!r}"
                qa.error(message) if strict_bounds else qa.warning(message)
        kind = element.get("kind")
        if not isinstance(kind, str) or not kind:
            qa.error(f"{item_path}.kind: required non-empty string")
        if kind in TEXT_KINDS:
            text = element.get("text")
            if not isinstance(text, str) or not text.strip():
                qa.error(f"{item_path}.text: required for {kind}")
            if require_lines:
                lines = element.get("lines")
                max_lines = element.get("max_lines")
                if not isinstance(lines, int) or lines < 1:
                    qa.error(f"{item_path}.lines: positive integer required")
                if not isinstance(max_lines, int) or max_lines < 1:
                    qa.error(f"{item_path}.max_lines: positive integer required")
                if isinstance(lines, int) and isinstance(max_lines, int) and lines > max_lines:
                    qa.error(f"{item_path}: lines {lines} exceed max_lines {max_lines}")
                if kind == "caption" and isinstance(max_lines, int) and max_lines > max_caption_lines:
                    qa.error(f"{item_path}: caption max_lines exceeds {max_caption_lines}")
            font_px = element.get("font_px")
            text_role = element.get("text_role")
            if require_font_px and (not isinstance(font_px, (int, float)) or isinstance(font_px, bool) or font_px <= 0):
                qa.error(f"{item_path}.font_px: positive number required")
            if require_text_role and (not isinstance(text_role, str) or not text_role):
                qa.error(f"{item_path}.text_role: required non-empty string")
            if isinstance(text_role, str) and text_role and text_role in minimum_by_role:
                minimum = minimum_by_role[text_role]
                if not isinstance(minimum, (int, float)) or isinstance(minimum, bool) or minimum <= 0:
                    qa.error(f"qa_contract.min_font_px_by_role.{text_role}: positive number required")
                elif isinstance(font_px, (int, float)) and not isinstance(font_px, bool) and font_px < minimum:
                    qa.error(f"{item_path}.font_px: {font_px} below {text_role!r} minimum {minimum}")
        claim_ids(element.get("claim_ids"), f"{item_path}.claim_ids", known_claims, strict_claims, qa)

    for element_id, parent_id in parents.items():
        if parent_id is None:
            continue
        if parent_id not in by_id:
            qa.error(f"{element_id}.parent_id: unknown {parent_id!r}")
        elif element_id in parsed and parent_id in parsed and not contains(parsed[parent_id], parsed[element_id]):
            qa.error(f"{element_id}: not contained by parent {parent_id}")

    epsilon_area = float(contract.get("overlap_epsilon_px2", 0.01))
    illegal = 0
    identifiers = list(parsed)
    for first_index, first_id in enumerate(identifiers):
        first = by_id[first_id]
        if first.get("collision") == "ignore":
            continue
        for second_id in identifiers[first_index + 1 :]:
            second = by_id[second_id]
            if second.get("collision") == "ignore":
                continue
            area = intersection_area(parsed[first_id], parsed[second_id])
            if area <= epsilon_area:
                continue
            if is_ancestor(first_id, second_id, parents) or is_ancestor(second_id, first_id, parents):
                continue
            first_allow = first.get("allow_overlap_with", [])
            second_allow = second.get("allow_overlap_with", [])
            if isinstance(first_allow, list) and second_id in first_allow:
                continue
            if isinstance(second_allow, list) and first_id in second_allow:
                continue
            illegal += 1
            message = f"{path}: illegal overlap {first_id!r} x {second_id!r} ({area:.2f}px2)"
            qa.error(message) if contract.get("fail_on_illegal_overlap", True) else qa.warning(message)
    return elements, illegal


def validate_timeline(
    manifest: dict[str, Any],
    safe: dict[str, tuple[float, float, float, float]],
    duration: float | None,
    known_claims: set[str],
    qa: QA,
) -> None:
    contract = manifest.get("qa_contract", {})
    if not isinstance(contract, dict):
        qa.error("qa_contract: expected object")
        contract = {}
    timeline = manifest.get("timeline")
    if not isinstance(timeline, dict):
        qa.error("timeline: required object")
        timeline = {}
    raw_boundaries = timeline.get("boundaries_s")
    boundaries: list[float] = []
    if not isinstance(raw_boundaries, list) or len(raw_boundaries) < 2:
        qa.error("timeline.boundaries_s: at least two values required")
    else:
        for index, item in enumerate(raw_boundaries):
            parsed = number(item, f"timeline.boundaries_s[{index}]", qa)
            if parsed is not None:
                boundaries.append(parsed)
        if boundaries and abs(boundaries[0]) > EPSILON:
            qa.error("timeline.boundaries_s: first boundary must be 0")
        if any(boundaries[index + 1] <= boundaries[index] for index in range(len(boundaries) - 1)):
            qa.error("timeline.boundaries_s: values must increase strictly")
        if duration is not None and boundaries and abs(boundaries[-1] - duration) > EPSILON:
            qa.error("timeline.boundaries_s: final boundary must equal canvas.duration_s")

    scenes = manifest.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        qa.error("scenes: required non-empty list")
        return
    declared_count = timeline.get("scene_count")
    if declared_count != len(scenes):
        qa.error(f"timeline.scene_count: expected {len(scenes)}, got {declared_count!r}")
    if boundaries and len(boundaries) != len(scenes) + 1:
        qa.error("timeline.boundaries_s: count must equal scene count + 1")

    fixed_raw = manifest.get("fixed_elements", [])
    if not isinstance(fixed_raw, list):
        qa.error("fixed_elements: expected list")
        fixed_raw = []
    fixed: list[dict[str, Any]] = []
    for index, item in enumerate(fixed_raw):
        if not isinstance(item, dict):
            qa.error(f"fixed_elements[{index}]: expected object")
        else:
            fixed.append(item)

    seen_scenes: set[str] = set()
    require_primary = bool(contract.get("require_primary_visual_bbox", False))
    min_primary_width = float(contract.get("min_primary_visual_width_ratio", 0.0))
    min_primary_height = float(contract.get("min_primary_visual_height_ratio", 0.0))
    content_zone = safe.get("content")
    for index, scene in enumerate(scenes):
        scene_path = f"scenes[{index}]"
        if not isinstance(scene, dict):
            qa.error(f"{scene_path}: expected object")
            continue
        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id:
            qa.error(f"{scene_path}.id: required")
            scene_id = f"scene-{index + 1}"
        elif scene_id in seen_scenes:
            qa.error(f"{scene_path}.id: duplicate {scene_id!r}")
        seen_scenes.add(scene_id)
        start = number(scene.get("start_s"), f"{scene_path}.start_s", qa)
        end = number(scene.get("end_s"), f"{scene_path}.end_s", qa)
        if start is not None and end is not None and end <= start:
            qa.error(f"{scene_path}: end_s must be after start_s")
        if boundaries and index + 1 < len(boundaries):
            if start is not None and abs(start - boundaries[index]) > EPSILON:
                qa.error(f"{scene_path}.start_s: does not match boundary {boundaries[index]}")
            if end is not None and abs(end - boundaries[index + 1]) > EPSILON:
                qa.error(f"{scene_path}.end_s: does not match boundary {boundaries[index + 1]}")

        primary = rect(scene.get("primary_visual_bbox"), f"{scene_path}.primary_visual_bbox", qa) if require_primary else None
        if require_primary and primary is None:
            qa.error(f"{scene_path}.primary_visual_bbox: required")
        elif primary is not None and content_zone is not None:
            if not contains(content_zone, primary):
                qa.error(f"{scene_path}.primary_visual_bbox: outside safe zone 'content'")
            width_ratio = primary[2] / content_zone[2]
            height_ratio = primary[3] / content_zone[3]
            if width_ratio < min_primary_width:
                qa.error(f"{scene_path}.primary_visual_bbox: width ratio {width_ratio:.3f} below {min_primary_width:.3f}")
            if height_ratio < min_primary_height:
                qa.error(f"{scene_path}.primary_visual_bbox: height ratio {height_ratio:.3f} below {min_primary_height:.3f}")

        scene_claims = claim_ids(
            scene.get("claim_ids"),
            f"{scene_path}.claim_ids",
            known_claims,
            bool(contract.get("fail_on_unmapped_claim", True)),
            qa,
        )
        if contract.get("require_claim_for_each_scene", False) and not scene_claims:
            qa.error(f"{scene_path}: at least one claim_id required")
        elements, illegal = validate_elements(
            scene.get("elements"), scene_path + ".elements", fixed, safe, known_claims, contract, qa
        )
        if contract.get("require_source_for_claims", False) and scene_claims:
            if not any(element.get("kind") == "source" for element in elements[len(fixed) :]):
                qa.error(f"{scene_path}: source element required for claims")

        changes = scene.get("state_changes")
        if not isinstance(changes, list):
            qa.error(f"{scene_path}.state_changes: expected list")
            changes = []
        if contract.get("require_state_change_for_each_scene", False) and not changes:
            qa.error(f"{scene_path}: at least one state change required")
        for change_index, change in enumerate(changes):
            change_path = f"{scene_path}.state_changes[{change_index}]"
            if not isinstance(change, dict):
                qa.error(f"{change_path}: expected object")
                continue
            for field in ("id", "from", "to", "motion"):
                if not isinstance(change.get(field), str) or not change.get(field):
                    qa.error(f"{change_path}.{field}: required non-empty string")
            at = number(change.get("at_s"), f"{change_path}.at_s", qa)
            if at is not None and start is not None and end is not None and not (start - EPSILON <= at < end + EPSILON):
                qa.error(f"{change_path}.at_s: outside scene")
        qa.scenes.append(
            {
                "id": scene_id,
                "start_s": start,
                "end_s": end,
                "element_count": len(elements) - len(fixed),
                "state_change_count": len(changes),
                "claim_count": len(scene_claims),
                "illegal_overlap_count": illegal,
            }
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path, help="also write the JSON report")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest_path = args.manifest.expanduser().resolve()
    qa = QA(manifest_path)
    manifest = load(manifest_path, qa)
    if manifest is not None:
        safe, duration = validate_canvas(manifest, qa)
        known_claims = validate_claims(manifest, qa)
        validate_timeline(manifest, safe, duration, known_claims, qa)
    payload = qa.payload()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if args.report:
        report = args.report.expanduser().resolve()
        try:
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(text + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"could not write report: {exc}", file=sys.stderr)
            return 1
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
