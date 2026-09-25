#!/usr/bin/env python3
"""Validate novel-creation-planner V1.3 single-story plans."""

from __future__ import annotations

from pathlib import Path
from typing import Any


REQUIRED_ROLES = {
    "world_premise",
    "primary_system",
    "faction_ecology",
    "resource_loop",
    "golden_finger_candidates",
}
SOURCE_MODES = {"DIRECT", "ADAPT", "HYBRID"}
ALLOWED_CORE_MODULES = {
    "world_premise": {"worldbuilding"},
    "primary_system": {"cultivation_system"},
    "faction_ecology": {"worldbuilding"},
    "resource_loop": {"worldbuilding", "cultivation_system"},
}
REF_FIELDS = {"material_id", "module", "record_id", "book_id", "qa_status"}
CORE_COMPONENT_FIELDS = {
    "candidate_text", "source_mode", "material_refs", "retained_structure", "adaptations"
}
CORE_FIELDS = {
    "core_id", "reader_promise", "protagonist_baseline", "longline_problem",
    "world_premise", "primary_system", "faction_ecology", "resource_loop", "story_engine"
}
TITLE_FIELDS = {"option_id", "title", "promise_focus", "same_core_id"}
OPENING_FIELDS = {
    "option_id", "same_core_id", "benchmark_lesson_ids", "opening_pattern",
    "chapter_1_3", "chapter_4_10_loop", "what_stays_fixed", "risk"
}
CHAPTER_FIELDS = {"chapter", "goal", "obstacle", "payoff", "hook"}
GF_FIELDS = {
    "option_id", "same_core_id", "name_candidate", "source_mode", "material_refs",
    "retained_mechanism", "adaptations", "input", "process", "output", "limits",
    "costs", "growth", "first_validation_plan", "compatibility_with_core", "risk"
}
TOP_FIELDS = {
    "schema_version", "plan_id", "status", "creation_mode", "workflow_stage", "brief",
    "shared_library_root", "market_benchmark_ref", "market_structural_lessons",
    "library_usage", "material_dispatch", "shared_story_core", "option_board",
    "selection", "post_selection", "material_gap_orders", "pending_decisions"
}


def empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def require_obj(errors: list[str], value: Any, fields: set[str], where: str) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{where} must be an object")
        return False
    missing = sorted(fields - set(value))
    if missing:
        errors.append(f"{where} missing: {', '.join(missing)}")
    return True


def material_ids(data: dict[str, Any]) -> set[str]:
    usage = data.get("library_usage")
    if not isinstance(usage, dict):
        return set()
    ids: set[str] = set()
    for key in ("formal_card_ids", "dna_candidate_ids"):
        values = usage.get(key)
        if isinstance(values, list):
            ids.update(str(x) for x in values if not empty(x))
    return ids


def validate_ref(
    errors: list[str],
    ref: Any,
    where: str,
    known_ids: set[str],
    allowed_modules: set[str] | None = None,
) -> str | None:
    if not require_obj(errors, ref, REF_FIELDS, where):
        return None
    for field in REF_FIELDS:
        if empty(ref.get(field)):
            errors.append(f"{where}.{field} cannot be empty")
    mid = str(ref.get("material_id") or "")
    if mid and mid not in known_ids:
        errors.append(f"{where}.material_id absent from library_usage")
    if ref.get("qa_status") in {"FAIL", "HOLD"}:
        errors.append(f"{where}.qa_status must be PASS or another non-blocked status")
    if allowed_modules is not None and ref.get("module") not in allowed_modules:
        errors.append(f"{where}.module must be one of {sorted(allowed_modules)}")
    return mid or None


def validate_core_component(
    errors: list[str],
    value: Any,
    where: str,
    known_ids: set[str],
    allowed_modules: set[str],
) -> None:
    if not require_obj(errors, value, CORE_COMPONENT_FIELDS, where):
        return
    if value.get("source_mode") not in SOURCE_MODES:
        errors.append(f"{where}.source_mode must be DIRECT/ADAPT/HYBRID")
    for field in ("candidate_text", "retained_structure"):
        if empty(value.get(field)):
            errors.append(f"{where}.{field} cannot be empty")
    if not isinstance(value.get("adaptations"), list):
        errors.append(f"{where}.adaptations must be a list")
    refs = value.get("material_refs")
    if not isinstance(refs, list) or not refs:
        errors.append(f"{where}.material_refs must be non-empty")
        return
    for index, ref in enumerate(refs):
        validate_ref(errors, ref, f"{where}.material_refs[{index}]", known_ids, allowed_modules)
    if value.get("source_mode") == "HYBRID" and len(refs) < 2:
        errors.append(f"{where}: HYBRID requires at least 2 material refs")


def validate_dispatch(errors: list[str], data: dict[str, Any], known_ids: set[str]) -> dict[str, list[str]]:
    dispatch = data.get("material_dispatch")
    roles: dict[str, list[str]] = {}
    if not isinstance(dispatch, dict):
        errors.append("material_dispatch must be an object")
        return roles
    slots = dispatch.get("slots")
    if not isinstance(slots, list):
        errors.append("material_dispatch.slots must be a list")
        return roles
    for index, slot in enumerate(slots):
        where = f"material_dispatch.slots[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{where} must be an object")
            continue
        role = slot.get("role")
        if not isinstance(role, str) or not role:
            errors.append(f"{where}.role cannot be empty")
            continue
        refs = slot.get("selected_refs")
        ids: list[str] = []
        if isinstance(refs, list):
            for rindex, ref in enumerate(refs):
                mid = validate_ref(errors, ref, f"{where}.selected_refs[{rindex}]", known_ids)
                if mid:
                    ids.append(mid)
        roles[role] = ids
    return roles


def validate_plan(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not require_obj(errors, data, TOP_FIELDS, "plan"):
        return errors
    if data.get("schema_version") != 3:
        errors.append("schema_version must be 3")
    if data.get("status") != "candidate":
        errors.append("status must remain candidate until user confirmation/writeback")
    if data.get("creation_mode") not in {"greenfield", "existing_project"}:
        errors.append("creation_mode must be greenfield or existing_project")
    stage = data.get("workflow_stage")
    if stage not in {"material_hold", "option_board", "selected", "backplanned"}:
        errors.append("workflow_stage is invalid")
    root = data.get("shared_library_root")
    if not isinstance(root, str) or not root.strip() or not Path(root).is_absolute():
        errors.append("shared_library_root must be a non-empty absolute path")

    lessons = data.get("market_structural_lessons")
    if not isinstance(lessons, list) or not all(isinstance(x, str) and x for x in lessons):
        errors.append("market_structural_lessons must be a string list")
        lessons = []
    lesson_ids = set(lessons)

    usage = data.get("library_usage")
    if not isinstance(usage, dict):
        errors.append("library_usage must be an object")
    else:
        for key in ("formal_card_ids", "dna_candidate_ids", "gaps"):
            if not isinstance(usage.get(key), list):
                errors.append(f"library_usage.{key} must be a list")
    known_ids = material_ids(data)

    roles = validate_dispatch(errors, data, known_ids)

    core = data.get("shared_story_core")
    core_id = None
    if require_obj(errors, core, CORE_FIELDS, "shared_story_core"):
        core_id = core.get("core_id")
        for field in ("core_id", "reader_promise", "protagonist_baseline", "longline_problem", "story_engine"):
            if empty(core.get(field)):
                errors.append(f"shared_story_core.{field} cannot be empty")
        for role, modules in ALLOWED_CORE_MODULES.items():
            validate_core_component(errors, core.get(role), f"shared_story_core.{role}", known_ids, modules)

    board = data.get("option_board")
    title_ids: set[str] = set()
    opening_ids: set[str] = set()
    gf_ids: set[str] = set()
    gf_material_ids: set[str] = set()
    if not isinstance(board, dict):
        errors.append("option_board must be an object")
        board = {}

    titles = board.get("title_options")
    openings = board.get("opening_options")
    gfs = board.get("golden_finger_options")

    if stage == "material_hold":
        if any(isinstance(x, list) and x for x in (titles, openings, gfs)):
            errors.append("material_hold must not fabricate option_board choices")
    else:
        missing_roles = sorted(REQUIRED_ROLES - set(roles))
        if missing_roles:
            errors.append(f"material_dispatch missing required roles: {', '.join(missing_roles)}")
        for role in REQUIRED_ROLES - {"golden_finger_candidates"}:
            if not roles.get(role):
                errors.append(f"required material role {role} has no selected refs")
        if len(set(roles.get("golden_finger_candidates", []))) < 3:
            errors.append("golden_finger_candidates requires at least 3 distinct material ids")

        if not isinstance(titles, list) or len(titles) != 3:
            errors.append("option_board.title_options must contain exactly 3 options")
        else:
            seen_titles: set[str] = set()
            for index, item in enumerate(titles):
                where = f"option_board.title_options[{index}]"
                if not require_obj(errors, item, TITLE_FIELDS, where):
                    continue
                oid = str(item.get("option_id") or "")
                if not oid or oid in title_ids:
                    errors.append(f"{where}.option_id must be non-empty and unique")
                title_ids.add(oid)
                title = str(item.get("title") or "")
                if not title or title in seen_titles:
                    errors.append(f"{where}.title must be non-empty and unique")
                seen_titles.add(title)
                if item.get("same_core_id") != core_id:
                    errors.append(f"{where}.same_core_id must match shared_story_core.core_id")
                if empty(item.get("promise_focus")):
                    errors.append(f"{where}.promise_focus cannot be empty")

        if not isinstance(openings, list) or len(openings) != 3:
            errors.append("option_board.opening_options must contain exactly 3 options")
        else:
            for index, item in enumerate(openings):
                where = f"option_board.opening_options[{index}]"
                if not require_obj(errors, item, OPENING_FIELDS, where):
                    continue
                oid = str(item.get("option_id") or "")
                if not oid or oid in opening_ids:
                    errors.append(f"{where}.option_id must be non-empty and unique")
                opening_ids.add(oid)
                if item.get("same_core_id") != core_id:
                    errors.append(f"{where}.same_core_id must match shared_story_core.core_id")
                refs = item.get("benchmark_lesson_ids")
                if not isinstance(refs, list) or not refs:
                    errors.append(f"{where}.benchmark_lesson_ids must be non-empty")
                elif not set(map(str, refs)).issubset(lesson_ids):
                    errors.append(f"{where}.benchmark_lesson_ids contains unknown lesson")
                chapters = item.get("chapter_1_3")
                if not isinstance(chapters, list) or len(chapters) != 3:
                    errors.append(f"{where}.chapter_1_3 must contain exactly 3 chapters")
                else:
                    observed = []
                    for cindex, chapter in enumerate(chapters):
                        cwhere = f"{where}.chapter_1_3[{cindex}]"
                        if not require_obj(errors, chapter, CHAPTER_FIELDS, cwhere):
                            continue
                        observed.append(chapter.get("chapter"))
                        for field in CHAPTER_FIELDS - {"chapter"}:
                            if empty(chapter.get(field)):
                                errors.append(f"{cwhere}.{field} cannot be empty")
                    if observed != [1, 2, 3]:
                        errors.append(f"{where}.chapter_1_3 chapter values must be 1,2,3")
                for field in ("opening_pattern", "chapter_4_10_loop", "risk"):
                    if empty(item.get(field)):
                        errors.append(f"{where}.{field} cannot be empty")
                if not isinstance(item.get("what_stays_fixed"), list) or not item.get("what_stays_fixed"):
                    errors.append(f"{where}.what_stays_fixed must be non-empty list")

        if not isinstance(gfs, list) or len(gfs) != 3:
            errors.append("option_board.golden_finger_options must contain exactly 3 options")
        else:
            for index, item in enumerate(gfs):
                where = f"option_board.golden_finger_options[{index}]"
                if not require_obj(errors, item, GF_FIELDS, where):
                    continue
                oid = str(item.get("option_id") or "")
                if not oid or oid in gf_ids:
                    errors.append(f"{where}.option_id must be non-empty and unique")
                gf_ids.add(oid)
                if item.get("same_core_id") != core_id:
                    errors.append(f"{where}.same_core_id must match shared_story_core.core_id")
                mode = item.get("source_mode")
                if mode not in SOURCE_MODES:
                    errors.append(f"{where}.source_mode must be DIRECT/ADAPT/HYBRID; ORIGINAL is forbidden")
                refs = item.get("material_refs")
                if not isinstance(refs, list) or not refs:
                    errors.append(f"{where}.material_refs must be non-empty")
                    refs = []
                if mode == "HYBRID" and len(refs) < 2:
                    errors.append(f"{where}: HYBRID requires at least 2 material refs")
                for rindex, ref in enumerate(refs):
                    mid = validate_ref(errors, ref, f"{where}.material_refs[{rindex}]", known_ids, {"golden_finger"})
                    if mid:
                        gf_material_ids.add(mid)
                for field in (
                    "name_candidate", "retained_mechanism", "input", "process", "output",
                    "growth", "first_validation_plan", "compatibility_with_core", "risk"
                ):
                    if empty(item.get(field)):
                        errors.append(f"{where}.{field} cannot be empty")
                for field in ("adaptations", "limits", "costs"):
                    if not isinstance(item.get(field), list):
                        errors.append(f"{where}.{field} must be a list")
            if len(gf_material_ids) < 3:
                errors.append("three golden-finger options must cover at least 3 distinct material ids")

    selection = data.get("selection")
    if require_obj(errors, selection, {"status", "title_option_id", "opening_option_id", "golden_finger_option_id"}, "selection"):
        status = selection.get("status")
        if status not in {"pending", "confirmed"}:
            errors.append("selection.status must be pending or confirmed")
        if status == "pending":
            for field in ("title_option_id", "opening_option_id", "golden_finger_option_id"):
                if not empty(selection.get(field)):
                    errors.append(f"selection.{field} must be empty while pending")
            if stage in {"selected", "backplanned"}:
                errors.append("selected/backplanned workflow_stage requires confirmed selection")
        else:
            if selection.get("title_option_id") not in title_ids:
                errors.append("selection.title_option_id must reference title_options")
            if selection.get("opening_option_id") not in opening_ids:
                errors.append("selection.opening_option_id must reference opening_options")
            if selection.get("golden_finger_option_id") not in gf_ids:
                errors.append("selection.golden_finger_option_id must reference golden_finger_options")
            if stage in {"material_hold", "option_board"}:
                errors.append("confirmed selection requires selected/backplanned workflow_stage")

    post = data.get("post_selection")
    if require_obj(errors, post, {"strategic_target_status", "climax_backplan_ref"}, "post_selection"):
        if selection.get("status") == "pending" if isinstance(selection, dict) else True:
            if post.get("strategic_target_status") != "blocked":
                errors.append("pending selection requires strategic_target_status=blocked")
            if not empty(post.get("climax_backplan_ref")):
                errors.append("pending selection requires empty climax_backplan_ref")
        elif stage == "backplanned" and empty(post.get("climax_backplan_ref")):
            errors.append("backplanned stage requires climax_backplan_ref")

    for key in ("material_gap_orders", "pending_decisions"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be a list")

    return errors
