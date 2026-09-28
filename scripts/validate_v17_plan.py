#!/usr/bin/env python3
"""Validate V1.7 dual-entry metadata while preserving V1.6 plan gates."""

from __future__ import annotations

import copy
from typing import Any

from validate_v16_plan import validate_plan as validate_v16

ENTRY_MODES = {"inspiration_draw", "fusion_furnace"}
SELECTION_MODES = {"single", "hybrid"}
CARD_SOURCE_KINDS = {"cluster", "per_book", "hybrid"}
CARD_FIELDS = {"candidate_id", "material_ids", "source_kind", "mechanism_summary"}
WINDOW_FIELDS = {"status", "window_size", "cards", "selected_candidate_ids", "selection_mode"}
ENTRY_FIELDS = {
    "domain",
    "default_relationship_mode",
    "world_card_window",
    "golden_finger_card_window",
    "assembly_order",
    "market_furnace",
}
FURNACE_FIELDS = {
    "benchmark_id",
    "selected_sample_ids",
    "structural_lesson_ids",
    "fusion_recipe",
    "copy_boundary",
}
FUSION_RECIPE_FIELDS = {
    "pace",
    "hook",
    "emotion",
    "goal_relay",
    "payoff",
    "supporting_character_usage",
    "opening_loop",
}
ASSEMBLY_ORDER = [
    "selected_world_core",
    "character_ecology",
    "faction_ecology",
    "faction_character_links",
    "cultivation_systems",
    "technique_combat_art_artifact_resources",
    "golden_finger",
    "narrative_layers",
    "local_scale_1_100",
    "scale_gate",
    "strategic_targets",
    "climax_backplanning",
    "story_spine_1_100",
]


def empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def require_obj(errors: list[str], value: Any, fields: set[str], where: str) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{where} must be an object")
        return False
    missing = sorted(fields - set(value))
    if missing:
        errors.append(f"{where} missing: {', '.join(missing)}")
        return False
    return True


def known_material_ids(data: dict[str, Any]) -> set[str]:
    usage = data.get("library_usage")
    if not isinstance(usage, dict):
        return set()
    ids: set[str] = set()
    for key in ("formal_card_ids", "dna_candidate_ids"):
        values = usage.get(key)
        if isinstance(values, list):
            ids.update(str(x) for x in values if not empty(x))
    return ids


def validate_card_window(
    errors: list[str],
    value: Any,
    where: str,
    known_ids: set[str],
) -> None:
    if not require_obj(errors, value, WINDOW_FIELDS, where):
        return
    if value.get("status") != "confirmed":
        errors.append(f"{where}.status must be confirmed for a schema_version 7 final plan")
    if value.get("window_size") != 9:
        errors.append(f"{where}.window_size must be 9")
    cards = value.get("cards")
    if not isinstance(cards, list) or len(cards) != 9:
        errors.append(f"{where}.cards must contain exactly 9 candidates")
        cards = []
    card_ids: set[str] = set()
    for index, card in enumerate(cards):
        cwhere = f"{where}.cards[{index}]"
        if not require_obj(errors, card, CARD_FIELDS, cwhere):
            continue
        cid = str(card.get("candidate_id") or "")
        if not cid or cid in card_ids:
            errors.append(f"{cwhere}.candidate_id must be non-empty and unique")
        card_ids.add(cid)
        if card.get("source_kind") not in CARD_SOURCE_KINDS:
            errors.append(f"{cwhere}.source_kind must be cluster/per_book/hybrid")
        if empty(card.get("mechanism_summary")):
            errors.append(f"{cwhere}.mechanism_summary cannot be empty")
        mids = card.get("material_ids")
        if not isinstance(mids, list) or not mids:
            errors.append(f"{cwhere}.material_ids must be a non-empty list")
        else:
            unknown = sorted({str(x) for x in mids if not empty(x)} - known_ids)
            if unknown:
                errors.append(f"{cwhere}.material_ids absent from library_usage: {', '.join(unknown)}")
    selected = value.get("selected_candidate_ids")
    if not isinstance(selected, list):
        errors.append(f"{where}.selected_candidate_ids must be a list")
        selected_ids: set[str] = set()
    else:
        selected_ids = {str(x) for x in selected if not empty(x)}
        if len(selected_ids) != len(selected):
            errors.append(f"{where}.selected_candidate_ids must be unique/non-empty")
        missing = sorted(selected_ids - card_ids)
        if missing:
            errors.append(f"{where}.selected_candidate_ids not present in cards: {', '.join(missing)}")
    mode = value.get("selection_mode")
    if mode not in SELECTION_MODES:
        errors.append(f"{where}.selection_mode must be single or hybrid")
    elif mode == "single" and len(selected_ids) != 1:
        errors.append(f"{where}: single selection requires exactly 1 selected candidate")
    elif mode == "hybrid" and len(selected_ids) != 2:
        errors.append(f"{where}: hybrid selection requires exactly 2 selected candidates")


def validate_furnace(errors: list[str], value: Any, where: str) -> None:
    if not require_obj(errors, value, FURNACE_FIELDS, where):
        return
    if empty(value.get("benchmark_id")):
        errors.append(f"{where}.benchmark_id cannot be empty")
    samples = value.get("selected_sample_ids")
    if not isinstance(samples, list) or len(samples) != 3 or len(set(map(str, samples))) != 3:
        errors.append(f"{where}.selected_sample_ids must contain exactly 3 unique ids")
    lessons = value.get("structural_lesson_ids")
    if not isinstance(lessons, list) or not lessons or any(empty(x) for x in lessons):
        errors.append(f"{where}.structural_lesson_ids must be a non-empty list")
    recipe = value.get("fusion_recipe")
    if require_obj(errors, recipe, FUSION_RECIPE_FIELDS, f"{where}.fusion_recipe"):
        for field in FUSION_RECIPE_FIELDS:
            if empty(recipe.get(field)):
                errors.append(f"{where}.fusion_recipe.{field} cannot be empty")
    if empty(value.get("copy_boundary")):
        errors.append(f"{where}.copy_boundary cannot be empty")


def validate_plan(data: dict[str, Any]) -> list[str]:
    if data.get("schema_version") != 7:
        return ["schema_version must be 7"]

    base = copy.deepcopy(data)
    base["schema_version"] = 6
    errors = validate_v16(base)

    mode = data.get("entry_mode")
    if mode not in ENTRY_MODES:
        errors.append("entry_mode must be inspiration_draw or fusion_furnace")

    context = data.get("entry_context")
    if not require_obj(errors, context, ENTRY_FIELDS, "entry_context"):
        return errors

    if context.get("domain") != "urban_gaowu":
        errors.append("entry_context.domain must be urban_gaowu in V1.7")
    if context.get("default_relationship_mode") != "multi_heroine":
        errors.append("entry_context.default_relationship_mode must be multi_heroine in V1.7")

    order = context.get("assembly_order")
    if order != ASSEMBLY_ORDER:
        errors.append("entry_context.assembly_order must match the V1.7 planner chain exactly")

    known_ids = known_material_ids(data)
    validate_card_window(errors, context.get("world_card_window"), "entry_context.world_card_window", known_ids)
    validate_card_window(
        errors,
        context.get("golden_finger_card_window"),
        "entry_context.golden_finger_card_window",
        known_ids,
    )

    furnace = context.get("market_furnace")
    if mode == "fusion_furnace":
        validate_furnace(errors, furnace, "entry_context.market_furnace")
    elif furnace not in (None, {}):
        errors.append("inspiration_draw requires entry_context.market_furnace to be null/empty")

    return errors
