"""Executable layout gate for the frozen MCD v8 14-scene manifest.

The manifest uses logical coordinates in a 720x1280 frame.  A rectangle is
``[x, y, width, height]``.  A parent may contain its children; that is the
only intentional overlap allowed by this gate.  All other intersections are
errors so that captions, source lines, cards, charts, buildings, and equipment
cannot silently collide.

Usage::

    python qa/layout_qa_v8.py scene-manifest-v8.json

The command is read-only and prints a JSON report.  It exits 0 only when the
manifest passes every contract check.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "scene-manifest-v8.json"
EPSILON_AREA = 0.01
EPSILON_COORD = 1e-6
REQUIRED_ZONES = ("header", "content", "source", "caption_platform")
TEXT_KINDS = {"text", "caption", "source"}


class LayoutQA:
    """Collect deterministic errors and warnings while validating a manifest."""

    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = manifest_path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.scene_reports: list[dict[str, Any]] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def report(self) -> dict[str, Any]:
        return {
            "manifest": str(self.manifest_path),
            "pass": not self.errors,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "scene_reports": self.scene_reports,
        }


def as_number(value: Any, path: str, qa: LayoutQA) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        qa.error(f"{path}: expected a number, got {value!r}")
        return None
    number = float(value)
    if not math.isfinite(number):
        qa.error(f"{path}: number must be finite")
        return None
    return number


def as_rect(value: Any, path: str, qa: LayoutQA) -> tuple[float, float, float, float] | None:
    if not isinstance(value, list) or len(value) != 4:
        qa.error(f"{path}: bbox must be [x, y, width, height]")
        return None
    numbers = [as_number(item, f"{path}[{index}]", qa) for index, item in enumerate(value)]
    if any(item is None for item in numbers):
        return None
    x, y, width, height = (float(item) for item in numbers if item is not None)
    if width <= 0 or height <= 0:
        qa.error(f"{path}: width and height must be > 0, got {value!r}")
        return None
    return x, y, width, height


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=0.0, abs_tol=EPSILON_COORD)


def contains(outer: tuple[float, float, float, float], inner: tuple[float, float, float, float]) -> bool:
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner
    return (
        ix >= ox - EPSILON_COORD
        and iy >= oy - EPSILON_COORD
        and ix + iw <= ox + ow + EPSILON_COORD
        and iy + ih <= oy + oh + EPSILON_COORD
    )


def intersection_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    width = min(ax + aw, bx + bw) - max(ax, bx)
    height = min(ay + ah, by + bh) - max(ay, by)
    return max(0.0, width) * max(0.0, height)


def exact_list(value: Any, expected: list[float], path: str, qa: LayoutQA) -> None:
    rect = as_rect(value, path, qa)
    if rect is None:
        return
    for index, (actual, wanted) in enumerate(zip(rect, expected)):
        if not close(actual, wanted):
            qa.error(f"{path}[{index}]: expected {wanted}, got {actual}")


def text_line_count(text: Any) -> int:
    if not isinstance(text, str):
        return 0
    return max(1, text.count("\n") + 1)


def ancestor(element_id: str, possible_ancestor: str, parents: dict[str, str | None]) -> bool:
    """Return true when possible_ancestor is an ancestor of element_id."""

    current = parents.get(element_id)
    visited: set[str] = set()
    while current is not None and current not in visited:
        if current == possible_ancestor:
            return True
        visited.add(current)
        current = parents.get(current)
    return False


def intentionally_allowed_overlap(
    first_id: str,
    second_id: str,
    parents: dict[str, str | None],
    elements: dict[str, dict[str, Any]],
) -> bool:
    if ancestor(first_id, second_id, parents) or ancestor(second_id, first_id, parents):
        return True
    first = elements[first_id]
    second = elements[second_id]
    first_allow = first.get("allow_overlap_with", [])
    second_allow = second.get("allow_overlap_with", [])
    return second_id in first_allow or first_id in second_allow


def load_manifest(path: Path, qa: LayoutQA) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        qa.error(f"manifest not found: {path}")
        return None
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        qa.error(f"could not read JSON manifest {path}: {exc}")
        return None
    if not isinstance(value, dict):
        qa.error("manifest root must be an object")
        return None
    return value


def validate_contract(manifest: dict[str, Any], qa: LayoutQA) -> tuple[dict[str, tuple[float, float, float, float]], list[float]]:
    if manifest.get("schema_version") != "mcd-layout-v8":
        qa.error(f"schema_version: expected 'mcd-layout-v8', got {manifest.get('schema_version')!r}")

    canvas = manifest.get("canvas")
    if not isinstance(canvas, dict):
        qa.error("canvas: required object is missing")
        canvas = {}
    logical = canvas.get("logical")
    if not isinstance(logical, dict):
        qa.error("canvas.logical: required object is missing")
        logical = {}
    for key, wanted in (("width", 720), ("height", 1280)):
        actual = as_number(logical.get(key), f"canvas.logical.{key}", qa)
        if actual is not None and not close(actual, wanted):
            qa.error(f"canvas.logical.{key}: expected {wanted}, got {actual}")
    output = canvas.get("output")
    if not isinstance(output, dict):
        qa.error("canvas.output: required object is missing")
        output = {}
    for key, wanted in (("width", 1080), ("height", 1920)):
        actual = as_number(output.get(key), f"canvas.output.{key}", qa)
        if actual is not None and not close(actual, wanted):
            qa.error(f"canvas.output.{key}: expected {wanted}, got {actual}")
    fps = as_number(canvas.get("fps"), "canvas.fps", qa)
    if fps is not None and not close(fps, 30):
        qa.error(f"canvas.fps: expected 30, got {fps}")

    expected_zones = {
        "header": [0, 0, 720, 236],
        "content": [48, 250, 624, 750],
        "source": [48, 930, 624, 50],
        "caption_platform": [0, 1000, 720, 240],
    }
    reserved = manifest.get("reserved_bboxes")
    if not isinstance(reserved, dict):
        qa.error("reserved_bboxes: required object is missing")
        reserved = {}
    zone_rects: dict[str, tuple[float, float, float, float]] = {}
    for zone, expected in expected_zones.items():
        if zone not in reserved:
            qa.error(f"reserved_bboxes.{zone}: missing")
            continue
        exact_list(reserved[zone], expected, f"reserved_bboxes.{zone}", qa)
        parsed = as_rect(reserved[zone], f"reserved_bboxes.{zone}", qa)
        if parsed is not None:
            zone_rects[zone] = parsed

    exact_list(manifest.get("content_bbox"), expected_zones["content"], "content_bbox", qa)
    exact_list(manifest.get("safe_bbox"), expected_zones["content"], "safe_bbox", qa)

    safe = manifest.get("safe_bboxes")
    if not isinstance(safe, dict):
        qa.error("safe_bboxes: required object is missing")
        safe = {}
    expected_safe = {
        "header": [32, 16, 656, 204],
        "content": [48, 250, 624, 750],
        "source": [48, 930, 624, 50],
        "caption_platform": [48, 1000, 624, 240],
    }
    for zone, expected in expected_safe.items():
        if zone not in safe:
            qa.error(f"safe_bboxes.{zone}: missing")
        else:
            exact_list(safe[zone], expected, f"safe_bboxes.{zone}", qa)
            if zone in zone_rects:
                parsed = as_rect(safe[zone], f"safe_bboxes.{zone}", qa)
                if parsed is not None and not contains(zone_rects[zone], parsed):
                    qa.error(f"safe_bboxes.{zone}: safe bbox must be inside its reserved bbox")

    zone_parents = manifest.get("zone_parents", {})
    if not isinstance(zone_parents, dict):
        qa.error("zone_parents: expected object")
        zone_parents = {}
    for child, parent in zone_parents.items():
        if child not in zone_rects or parent not in zone_rects:
            qa.error(f"zone_parents.{child}: unknown zone parent {parent!r}")
        elif not contains(zone_rects[parent], zone_rects[child]):
            qa.error(f"zone_parents.{child}: child zone is not contained by {parent}")

    timeline = manifest.get("timeline")
    if not isinstance(timeline, dict):
        qa.error("timeline: required object is missing")
        timeline = {}
    expected_boundaries = [0.0, 4.0, 7.45, 10.95, 15.15, 19.75, 23.95, 29.05, 33.3, 38.35, 41.55, 45.75, 50.0, 54.0, 58.5]
    boundaries_raw = timeline.get("boundaries_s")
    boundaries: list[float] = []
    if not isinstance(boundaries_raw, list):
        qa.error("timeline.boundaries_s: required list is missing")
    else:
        for index, item in enumerate(boundaries_raw):
            parsed = as_number(item, f"timeline.boundaries_s[{index}]", qa)
            if parsed is not None:
                boundaries.append(parsed)
        if len(boundaries) != len(expected_boundaries):
            qa.error(f"timeline.boundaries_s: expected {len(expected_boundaries)} boundaries, got {len(boundaries)}")
        for index, wanted in enumerate(expected_boundaries[: len(boundaries)]):
            if not close(boundaries[index], wanted):
                qa.error(f"timeline.boundaries_s[{index}]: expected {wanted}, got {boundaries[index]}")
    scene_count = as_number(timeline.get("scene_count"), "timeline.scene_count", qa)
    if scene_count is not None and not close(scene_count, 14):
        qa.error(f"timeline.scene_count: expected 14, got {scene_count}")
    duration = as_number(canvas.get("duration_s"), "canvas.duration_s", qa)
    if duration is not None and boundaries and not close(duration, boundaries[-1]):
        qa.error(f"canvas.duration_s: expected final boundary {boundaries[-1]}, got {duration}")

    return zone_rects, boundaries


def validate_fixed_elements(
    manifest: dict[str, Any],
    qa: LayoutQA,
    zone_rects: dict[str, tuple[float, float, float, float]],
) -> list[dict[str, Any]]:
    fixed = manifest.get("fixed_elements")
    if not isinstance(fixed, list) or not fixed:
        qa.error("fixed_elements: non-empty list is required")
        return []
    return validate_elements(
        fixed,
        "fixed_elements",
        qa,
        zone_rects,
        safe_bboxes=manifest.get("safe_bboxes", {}),
        require_caption=False,
    )


def validate_elements(
    raw_elements: Any,
    path: str,
    qa: LayoutQA,
    zone_rects: dict[str, tuple[float, float, float, float]],
    safe_bboxes: Any,
    require_caption: bool,
) -> list[dict[str, Any]]:
    if not isinstance(raw_elements, list):
        qa.error(f"{path}: expected list")
        return []
    elements: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, raw in enumerate(raw_elements):
        item_path = f"{path}[{index}]"
        if not isinstance(raw, dict):
            qa.error(f"{item_path}: expected object")
            continue
        element = dict(raw)
        element_id = element.get("id")
        if not isinstance(element_id, str) or not element_id:
            qa.error(f"{item_path}.id: required non-empty string")
            continue
        if element_id in ids:
            qa.error(f"{item_path}.id: duplicate id {element_id!r}")
        ids.add(element_id)
        zone = element.get("zone")
        if zone not in REQUIRED_ZONES:
            qa.error(f"{item_path}.zone: expected one of {REQUIRED_ZONES}, got {zone!r}")
        if zone not in zone_rects:
            qa.error(f"{item_path}.zone: zone bbox is unavailable for {zone!r}")
        bbox = as_rect(element.get("bbox"), f"{item_path}.bbox", qa)
        if bbox is None:
            continue
        element["_path"] = item_path
        element["_bbox"] = bbox
        elements.append(element)
        if bbox[0] < -EPSILON_COORD or bbox[1] < -EPSILON_COORD or bbox[0] + bbox[2] > 720 + EPSILON_COORD or bbox[1] + bbox[3] > 1280 + EPSILON_COORD:
            qa.error(f"{item_path}.bbox: out of 720x1280 canvas bounds")
        if zone in zone_rects and not contains(zone_rects[zone], bbox):
            qa.error(f"{item_path}.bbox: not contained by reserved {zone!r} zone")
        if isinstance(safe_bboxes, dict) and zone in safe_bboxes:
            safe_rect = as_rect(safe_bboxes[zone], f"safe_bboxes.{zone}", qa)
            if safe_rect is not None and not contains(safe_rect, bbox):
                qa.error(f"{item_path}.bbox: outside safe_bboxes.{zone}")

        kind = element.get("kind")
        if not isinstance(kind, str) or not kind:
            qa.error(f"{item_path}.kind: required non-empty string")
        if kind in TEXT_KINDS:
            text = element.get("text")
            if not isinstance(text, str) or not text.strip():
                qa.error(f"{item_path}.text: required non-empty string for {kind}")
            actual_lines = text_line_count(text)
            lines = as_number(element.get("lines"), f"{item_path}.lines", qa)
            max_lines = as_number(element.get("max_lines"), f"{item_path}.max_lines", qa)
            if lines is not None and not close(lines, actual_lines):
                qa.error(f"{item_path}.lines: declared {lines:g}, actual newline count is {actual_lines}")
            if lines is not None and lines < 1:
                qa.error(f"{item_path}.lines: must be >= 1")
            if max_lines is not None and max_lines < 1:
                qa.error(f"{item_path}.max_lines: must be >= 1")
            if lines is not None and max_lines is not None and lines > max_lines:
                qa.error(f"{item_path}: line count {lines:g} exceeds max_lines {max_lines:g}")
            if kind == "caption" and max_lines is not None:
                qa_contract = max_lines
                if qa_contract > 2:
                    qa.error(f"{item_path}.max_lines: caption lane allows at most 2 lines")
        claim_ids = element.get("claim_ids", [])
        if claim_ids is not None and not isinstance(claim_ids, list):
            qa.error(f"{item_path}.claim_ids: expected list")
        if zone == "caption_platform" and kind not in {"caption", "platform_guard"}:
            qa.error(f"{item_path}: only caption/platform_guard may enter caption_platform zone")
        if zone != "caption_platform" and intersection_area(bbox, zone_rects.get("caption_platform", (0, 1000, 720, 240))) > EPSILON_AREA:
            qa.error(f"{item_path}.bbox: caption/platform lane intrusion")
        if zone == "source" and kind != "source":
            qa.error(f"{item_path}: source zone elements must use kind='source'")
        if zone == "source" and intersection_area(bbox, zone_rects.get("content", (48, 250, 624, 750))) <= EPSILON_AREA:
            qa.error(f"{item_path}.bbox: source element must sit in the declared content/source strip")
        if kind == "caption" and zone != "caption_platform":
            qa.error(f"{item_path}: caption kind must use caption_platform zone")

    element_by_id = {item["id"]: item for item in elements}
    parents: dict[str, str | None] = {}
    for element in elements:
        parent_id = element.get("parent_id")
        if parent_id is None:
            parents[element["id"]] = None
            continue
        if not isinstance(parent_id, str) or not parent_id:
            qa.error(f"{element['_path']}.parent_id: expected an existing element id")
            parents[element["id"]] = None
            continue
        if parent_id not in element_by_id:
            qa.error(f"{element['_path']}.parent_id: unknown parent {parent_id!r}")
            parents[element["id"]] = None
            continue
        if parent_id == element["id"]:
            qa.error(f"{element['_path']}.parent_id: an element cannot parent itself")
            parents[element["id"]] = None
            continue
        parents[element["id"]] = parent_id
        if not contains(element_by_id[parent_id]["_bbox"], element["_bbox"]):
            qa.error(f"{element['_path']}.bbox: child is not contained by parent {parent_id!r}")

    for element in elements:
        current = element["id"]
        seen: set[str] = set()
        while current in parents and parents[current] is not None:
            if current in seen:
                qa.error(f"{element['_path']}: parent cycle detected")
                break
            seen.add(current)
            parent = parents[current]
            if parent is None:
                break
            current = parent

    for index, first in enumerate(elements):
        for second in elements[index + 1 :]:
            area = intersection_area(first["_bbox"], second["_bbox"])
            if area <= EPSILON_AREA:
                continue
            if not intentionally_allowed_overlap(first["id"], second["id"], parents, element_by_id):
                qa.error(
                    f"{path}: illegal overlap {first['id']!r} × {second['id']!r} "
                    f"({area:.2f} logical px²); declare an explicit parent-child relationship"
                )

    caption_count = sum(1 for item in elements if item.get("kind") == "caption")
    if require_caption and caption_count != 1:
        qa.error(f"{path}: expected exactly one caption element, got {caption_count}")
    return elements


def validate_state_changes(scene: dict[str, Any], start: float, end: float, qa: LayoutQA) -> None:
    path = f"scene {scene.get('id', '?')}.state_changes"
    states = scene.get("state_changes")
    if not isinstance(states, list) or not states:
        qa.error(f"{path}: at least one state change is required")
        return
    ids: set[str] = set()
    meaningful = 0
    for index, state in enumerate(states):
        item_path = f"{path}[{index}]"
        if not isinstance(state, dict):
            qa.error(f"{item_path}: expected object")
            continue
        state_id = state.get("id")
        if not isinstance(state_id, str) or not state_id:
            qa.error(f"{item_path}.id: required non-empty string")
        elif state_id in ids:
            qa.error(f"{item_path}.id: duplicate state id {state_id!r}")
        else:
            ids.add(state_id)
        at = as_number(state.get("at_s"), f"{item_path}.at_s", qa)
        if at is not None and (at < start - EPSILON_COORD or at > end + EPSILON_COORD):
            qa.error(f"{item_path}.at_s: {at:g} is outside scene interval [{start:g}, {end:g}]")
        before = state.get("from")
        after = state.get("to")
        if before is None or after is None:
            qa.error(f"{item_path}: from and to are required")
        elif before != after:
            meaningful += 1
    if meaningful == 0:
        qa.error(f"{path}: at least one state change must change from != to")


def validate_scenes(
    manifest: dict[str, Any],
    qa: LayoutQA,
    zone_rects: dict[str, tuple[float, float, float, float]],
    boundaries: list[float],
    fixed_elements: list[dict[str, Any]],
) -> None:
    claims = manifest.get("claims")
    if not isinstance(claims, dict):
        qa.error("claims: required object is missing")
        claims = {}
    scenes = manifest.get("scenes")
    if not isinstance(scenes, list):
        qa.error("scenes: required list is missing")
        return
    if len(scenes) != 14:
        qa.error(f"scenes: expected 14 scenes, got {len(scenes)}")
    fixed_by_id = {item["id"]: item for item in fixed_elements}
    for index, raw_scene in enumerate(scenes):
        scene_path = f"scenes[{index}]"
        if not isinstance(raw_scene, dict):
            qa.error(f"{scene_path}: expected object")
            continue
        scene = raw_scene
        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id:
            qa.error(f"{scene_path}.id: required non-empty string")
            scene_id = f"index-{index + 1}"
        expected_start = boundaries[index] if index < len(boundaries) else None
        expected_end = boundaries[index + 1] if index + 1 < len(boundaries) else None
        start = as_number(scene.get("start_s"), f"{scene_path}.start_s", qa)
        end = as_number(scene.get("end_s"), f"{scene_path}.end_s", qa)
        if expected_start is not None and start is not None and not close(start, expected_start):
            qa.error(f"{scene_path}.start_s: expected {expected_start}, got {start}")
        if expected_end is not None and end is not None and not close(end, expected_end):
            qa.error(f"{scene_path}.end_s: expected {expected_end}, got {end}")
        if start is not None and end is not None and end <= start:
            qa.error(f"{scene_path}: end_s must be greater than start_s")
        if index and start is not None:
            previous_end = as_number(scenes[index - 1].get("end_s"), f"scenes[{index - 1}].end_s", qa) if isinstance(scenes[index - 1], dict) else None
            if previous_end is not None and not close(previous_end, start):
                qa.error(f"{scene_path}: scene interval is not contiguous with previous scene")

        raw_scene_claims = scene.get("claim_ids")
        if not isinstance(raw_scene_claims, list) or not raw_scene_claims:
            qa.error(f"{scene_path}.claim_ids: at least one claim id is required")
            raw_scene_claims = []
        claim_ids = [item for item in raw_scene_claims if isinstance(item, str)]
        for claim_id in claim_ids:
            if claim_id not in claims:
                qa.error(f"{scene_path}.claim_ids: unknown claim {claim_id!r}")
        validate_state_changes(scene, start if start is not None else 0.0, end if end is not None else 0.0, qa)

        raw_scene_elements = scene.get("elements")
        safe_bboxes = manifest.get("safe_bboxes", {})
        scene_elements = validate_elements(
            raw_scene_elements,
            f"{scene_path}.elements",
            qa,
            zone_rects,
            safe_bboxes=safe_bboxes,
            require_caption=True,
        )
        # Fixed elements are outside the scene list by design.  Check their
        # overlaps with scene elements as well, so a future content change
        # cannot collide with the permanent header rails.
        combined = fixed_elements + scene_elements
        combined_by_id = {item["id"]: item for item in combined}
        parents: dict[str, str | None] = {item["id"]: item.get("parent_id") for item in combined}
        for first_index, first in enumerate(combined):
            for second in combined[first_index + 1 :]:
                area = intersection_area(first["_bbox"], second["_bbox"])
                if area <= EPSILON_AREA:
                    continue
                if not intentionally_allowed_overlap(first["id"], second["id"], parents, combined_by_id):
                    qa.error(
                        f"{scene_path}: illegal fixed/scene overlap {first['id']!r} × {second['id']!r} "
                        f"({area:.2f} logical px²)"
                    )

        visible_claims: set[str] = set()
        for element in scene_elements:
            element_claims = element.get("claim_ids", [])
            if isinstance(element_claims, list):
                visible_claims.update(item for item in element_claims if isinstance(item, str))
        for claim_id in claim_ids:
            if claim_id not in visible_claims:
                qa.error(f"{scene_path}.claim_ids: claim {claim_id!r} has no mapped visible element")

        qa.scene_reports.append(
            {
                "id": scene_id,
                "index": index + 1,
                "start_s": start,
                "end_s": end,
                "claim_count": len(claim_ids),
                "state_change_count": len(scene.get("state_changes", [])) if isinstance(scene.get("state_changes"), list) else 0,
                "element_count": len(scene_elements),
                "pass": not any(message.startswith(f"{scene_path}") or message.startswith(f"scene {scene_id}") for message in qa.errors),
            }
        )


def run(manifest_path: Path) -> int:
    qa = LayoutQA(manifest_path)
    manifest = load_manifest(manifest_path, qa)
    if manifest is not None:
        zone_rects, boundaries = validate_contract(manifest, qa)
        fixed_elements = validate_fixed_elements(manifest, qa, zone_rects)
        validate_scenes(manifest, qa, zone_rects, boundaries, fixed_elements)
    print(json.dumps(qa.report(), ensure_ascii=False, indent=2))
    return 0 if not qa.errors else 1


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args(list(argv) if argv is not None else None)


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(run(arguments.manifest.resolve()))
