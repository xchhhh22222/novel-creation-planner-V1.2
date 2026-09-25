#!/usr/bin/env python3
"""Validate V1.4 local-scale creation plans."""

from __future__ import annotations

from pathlib import Path
from typing import Any


TOP_FIELDS = {
    "schema_version", "plan_id", "status", "creation_mode", "workflow_stage",
    "brief", "shared_library_root", "market_benchmark_ref",
    "market_structural_lessons", "library_usage", "material_dispatch",
    "shared_story_core", "option_board", "selection", "local_scale_1_100",
    "scale_gate", "post_selection", "material_gap_orders", "pending_decisions",
}
FACTION_FIELDS = {
    "faction_id", "name", "role", "controlled_assets_or_permissions",
    "current_interest", "protagonist_relation", "stage_entry", "material_refs",
}
EXTERNAL_FACTION_FIELDS = {
    "faction_id", "name", "interest", "local_touchpoint", "future_use", "material_refs",
}
RELATION_FIELDS = {"from", "to", "relation_type", "reason"}
SYSTEM_FIELDS = {
    "system_id", "name", "social_status", "entry_condition", "power_source",
    "current_revealed_realms", "strength", "weakness", "resource_dependency",
    "can_dual_cultivate", "relation_to_protagonist", "material_refs",
}
SYSTEM_RELATION_FIELDS = {"from", "to", "relation_type", "reason"}
PROGRESSION_FIELDS = {
    "current_revealed_realms", "protagonist_start_realm",
    "climax_1_expected_realm", "climax_2_expected_realm", "future_realm_hint",
}
TECHNIQUE_FIELDS = {
    "item_id", "name", "tier", "system_id", "training_method", "core_effect",
    "limitation", "resource_cost", "access", "material_refs",
}
COMBAT_FIELDS = {
    "item_id", "name", "tier", "system_id", "use_case", "combat_function",
    "limitation", "first_stage", "material_refs",
}
ARTIFACT_FIELDS = {
    "item_id", "name", "tier", "system_id", "activation", "effect",
    "consumption", "limitation", "acquisition", "material_refs",
}
RESOURCE_FIELDS = {
    "resource_id", "name", "source", "controlled_by", "used_by",
    "acquisition", "consumption", "golden_finger_relation", "material_refs",
}
MAP_FIELDS = {"node_id", "name", "function", "controlled_by", "conflict_use"}
EXTERNAL_MAP_FIELDS = {"name", "why_it_touches_current_city", "which_faction_reaches_in", "future_use"}
GF_INTERFACE_FIELDS = {
    "can_strengthen", "cannot_replace", "dependencies",
    "anticipation_loop", "resource_loop_protection",
}
HANDOFF_FIELDS = {
    "protagonist_power", "formal_status", "owned_techniques",
    "owned_combat_arts", "owned_artifacts", "known_systems",
    "unexpanded_systems", "active_factions", "external_factions_touched",
    "used_material_ids", "remaining_material_directions",
    "unpaid_promises", "next_stage_problem",
}
SCALE_FIELDS = {
    "scale_id", "scope_label", "active_factions", "external_factions",
    "faction_relations", "systems", "system_relations", "progression_scope",
    "technique_pool", "combat_art_pool", "artifact_pool", "ordinary_resources",
    "local_map_nodes", "external_map_hooks", "golden_finger_interfaces",
    "handoff_after_100",
}
ALLIANCE_RELATIONS = {"ally", "conditional_ally", "dependency", "regulator"}
CONFLICT_RELATIONS = {"competitor", "hostile"}
ALL_FACTION_RELATIONS = ALLIANCE_RELATIONS | CONFLICT_RELATIONS
SYSTEM_RELATIONS = {
    "social_hierarchy", "competition", "complement", "restraint",
    "conversion", "exclusivity",
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


def known_material_ids(data: dict[str, Any]) -> set[str]:
    usage = data.get("library_usage")
    ids: set[str] = set()
    if isinstance(usage, dict):
        for key in ("formal_card_ids", "dna_candidate_ids"):
            values = usage.get(key)
            if isinstance(values, list):
                ids.update(str(x) for x in values if not empty(x))
    return ids


def validate_refs(errors: list[str], refs: Any, where: str, known: set[str]) -> None:
    if not isinstance(refs, list) or not refs:
        errors.append(f"{where} must be a non-empty list")
        return
    for index, ref in enumerate(refs):
        rwhere = f"{where}[{index}]"
        if not isinstance(ref, dict):
            errors.append(f"{rwhere} must be an object")
            continue
        for field in ("material_id", "record_id", "book_id", "module", "qa_status"):
            if empty(ref.get(field)):
                errors.append(f"{rwhere}.{field} cannot be empty")
        mid = str(ref.get("material_id") or "")
        if mid and mid not in known:
            errors.append(f"{rwhere}.material_id absent from library_usage")
        if ref.get("qa_status") in {"FAIL", "HOLD"}:
            errors.append(f"{rwhere}.qa_status cannot be FAIL/HOLD")


def validate_pool(
    errors: list[str],
    items: Any,
    minimum: int,
    maximum: int | None,
    fields: set[str],
    where: str,
    known: set[str],
    system_ids: set[str] | None = None,
) -> None:
    if not isinstance(items, list):
        errors.append(f"{where} must be a list")
        return
    if len(items) < minimum or (maximum is not None and len(items) > maximum):
        range_text = f"{minimum}..{maximum}" if maximum is not None else f">={minimum}"
        errors.append(f"{where} must contain {range_text} items")
    ids: set[str] = set()
    for index, item in enumerate(items):
        iwhere = f"{where}[{index}]"
        if not require_obj(errors, item, fields, iwhere):
            continue
        item_id = str(item.get("item_id") or item.get("resource_id") or "")
        if item_id:
            if item_id in ids:
                errors.append(f"{iwhere} id must be unique")
            ids.add(item_id)
        for field in fields - {"material_refs"}:
            if empty(item.get(field)) and field not in {"can_dual_cultivate"}:
                errors.append(f"{iwhere}.{field} cannot be empty")
        if "material_refs" in fields:
            validate_refs(errors, item.get("material_refs"), f"{iwhere}.material_refs", known)
        if system_ids is not None:
            sid = item.get("system_id")
            if sid not in system_ids:
                errors.append(f"{iwhere}.system_id must reference systems")


def validate_plan(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not require_obj(errors, data, TOP_FIELDS, "plan"):
        return errors
    if data.get("schema_version") != 4:
        errors.append("schema_version must be 4")
    if data.get("status") != "candidate":
        errors.append("status must remain candidate")
    if data.get("creation_mode") not in {"greenfield", "existing_project"}:
        errors.append("creation_mode must be greenfield or existing_project")
    stage = data.get("workflow_stage")
    if stage not in {"material_hold", "option_board", "selected", "scaled", "backplanned"}:
        errors.append("workflow_stage is invalid")
    root = data.get("shared_library_root")
    if not isinstance(root, str) or not root.strip() or not Path(root).is_absolute():
        errors.append("shared_library_root must be a non-empty absolute path")

    known = known_material_ids(data)
    selection = data.get("selection")
    confirmed = isinstance(selection, dict) and selection.get("status") == "confirmed"
    if stage in {"selected", "scaled", "backplanned"} and not confirmed:
        errors.append("selected/scaled/backplanned requires confirmed selection")

    scale = data.get("local_scale_1_100")
    gate = data.get("scale_gate")
    if not isinstance(gate, dict) or gate.get("status") not in {"blocked", "HOLD", "PASS"}:
        errors.append("scale_gate.status must be blocked/HOLD/PASS")
    else:
        if not isinstance(gate.get("reasons"), list):
            errors.append("scale_gate.reasons must be a list")

    if not confirmed:
        if not empty(scale):
            errors.append("local_scale_1_100 must be empty before selection confirmation")
        if isinstance(gate, dict) and gate.get("status") != "blocked":
            errors.append("unconfirmed selection requires scale_gate.status=blocked")
        return errors

    if stage == "selected" and empty(scale):
        if isinstance(gate, dict) and gate.get("status") == "PASS":
            errors.append("scale_gate cannot PASS without local_scale_1_100")
    else:
        if not require_obj(errors, scale, SCALE_FIELDS, "local_scale_1_100"):
            return errors
        for field in ("scale_id", "scope_label"):
            if empty(scale.get(field)):
                errors.append(f"local_scale_1_100.{field} cannot be empty")

        factions = scale.get("active_factions")
        faction_ids: set[str] = set()
        if not isinstance(factions, list) or not 4 <= len(factions) <= 7:
            errors.append("active_factions must contain 4..7 items")
            factions = []
        for index, faction in enumerate(factions):
            where = f"active_factions[{index}]"
            if not require_obj(errors, faction, FACTION_FIELDS, where):
                continue
            fid = str(faction.get("faction_id") or "")
            if not fid or fid in faction_ids:
                errors.append(f"{where}.faction_id must be non-empty and unique")
            faction_ids.add(fid)
            for field in FACTION_FIELDS - {"material_refs"}:
                if empty(faction.get(field)):
                    errors.append(f"{where}.{field} cannot be empty")
            validate_refs(errors, faction.get("material_refs"), f"{where}.material_refs", known)

        external = scale.get("external_factions")
        external_ids: set[str] = set()
        if not isinstance(external, list) or len(external) > 2:
            errors.append("external_factions must contain 0..2 items")
            external = []
        for index, faction in enumerate(external):
            where = f"external_factions[{index}]"
            if not require_obj(errors, faction, EXTERNAL_FACTION_FIELDS, where):
                continue
            fid = str(faction.get("faction_id") or "")
            if not fid or fid in faction_ids or fid in external_ids:
                errors.append(f"{where}.faction_id must be unique")
            external_ids.add(fid)
            for field in EXTERNAL_FACTION_FIELDS - {"material_refs"}:
                if empty(faction.get(field)):
                    errors.append(f"{where}.{field} cannot be empty")
            validate_refs(errors, faction.get("material_refs"), f"{where}.material_refs", known)

        relations = scale.get("faction_relations")
        relation_types: set[str] = set()
        if not isinstance(relations, list) or not relations:
            errors.append("faction_relations must be non-empty")
            relations = []
        valid_fids = faction_ids | external_ids
        for index, relation in enumerate(relations):
            where = f"faction_relations[{index}]"
            if not require_obj(errors, relation, RELATION_FIELDS, where):
                continue
            if relation.get("from") not in valid_fids or relation.get("to") not in valid_fids:
                errors.append(f"{where} endpoints must reference factions")
            rtype = relation.get("relation_type")
            if rtype not in ALL_FACTION_RELATIONS:
                errors.append(f"{where}.relation_type invalid")
            else:
                relation_types.add(rtype)
            if empty(relation.get("reason")):
                errors.append(f"{where}.reason cannot be empty")
        if not (relation_types & ALLIANCE_RELATIONS):
            errors.append("faction_relations requires at least one ally/dependency/regulator relation")
        if not (relation_types & CONFLICT_RELATIONS):
            errors.append("faction_relations requires at least one competitor/hostile relation")

        systems = scale.get("systems")
        system_ids: set[str] = set()
        if not isinstance(systems, list) or not 2 <= len(systems) <= 3:
            errors.append("systems must contain 2..3 items")
            systems = []
        for index, system in enumerate(systems):
            where = f"systems[{index}]"
            if not require_obj(errors, system, SYSTEM_FIELDS, where):
                continue
            sid = str(system.get("system_id") or "")
            if not sid or sid in system_ids:
                errors.append(f"{where}.system_id must be non-empty and unique")
            system_ids.add(sid)
            for field in SYSTEM_FIELDS - {"material_refs", "can_dual_cultivate"}:
                if empty(system.get(field)):
                    errors.append(f"{where}.{field} cannot be empty")
            if not isinstance(system.get("can_dual_cultivate"), bool):
                errors.append(f"{where}.can_dual_cultivate must be boolean")
            validate_refs(errors, system.get("material_refs"), f"{where}.material_refs", known)

        sysrels = scale.get("system_relations")
        if not isinstance(sysrels, list) or not sysrels:
            errors.append("system_relations must be non-empty")
            sysrels = []
        for index, relation in enumerate(sysrels):
            where = f"system_relations[{index}]"
            if not require_obj(errors, relation, SYSTEM_RELATION_FIELDS, where):
                continue
            if relation.get("from") not in system_ids or relation.get("to") not in system_ids:
                errors.append(f"{where} endpoints must reference systems")
            if relation.get("relation_type") not in SYSTEM_RELATIONS:
                errors.append(f"{where}.relation_type invalid")
            if empty(relation.get("reason")):
                errors.append(f"{where}.reason cannot be empty")

        progression = scale.get("progression_scope")
        if require_obj(errors, progression, PROGRESSION_FIELDS, "progression_scope"):
            for field in PROGRESSION_FIELDS:
                if empty(progression.get(field)):
                    errors.append(f"progression_scope.{field} cannot be empty")
            if not isinstance(progression.get("current_revealed_realms"), list) or len(progression.get("current_revealed_realms", [])) < 2:
                errors.append("progression_scope.current_revealed_realms must contain at least 2 realms")

        validate_pool(errors, scale.get("technique_pool"), 3, None, TECHNIQUE_FIELDS, "technique_pool", known, system_ids)
        validate_pool(errors, scale.get("combat_art_pool"), 3, None, COMBAT_FIELDS, "combat_art_pool", known, system_ids)
        validate_pool(errors, scale.get("artifact_pool"), 2, None, ARTIFACT_FIELDS, "artifact_pool", known, system_ids)
        validate_pool(errors, scale.get("ordinary_resources"), 3, 6, RESOURCE_FIELDS, "ordinary_resources", known)

        maps = scale.get("local_map_nodes")
        if not isinstance(maps, list) or not 3 <= len(maps) <= 6:
            errors.append("local_map_nodes must contain 3..6 items")
        else:
            map_ids: set[str] = set()
            for index, node in enumerate(maps):
                where = f"local_map_nodes[{index}]"
                if not require_obj(errors, node, MAP_FIELDS, where):
                    continue
                nid = str(node.get("node_id") or "")
                if not nid or nid in map_ids:
                    errors.append(f"{where}.node_id must be non-empty and unique")
                map_ids.add(nid)
                for field in MAP_FIELDS:
                    if empty(node.get(field)):
                        errors.append(f"{where}.{field} cannot be empty")

        hooks = scale.get("external_map_hooks")
        if not isinstance(hooks, list) or len(hooks) > 2:
            errors.append("external_map_hooks must contain 0..2 items")
        else:
            for index, hook in enumerate(hooks):
                where = f"external_map_hooks[{index}]"
                if not require_obj(errors, hook, EXTERNAL_MAP_FIELDS, where):
                    continue
                for field in EXTERNAL_MAP_FIELDS:
                    if empty(hook.get(field)):
                        errors.append(f"{where}.{field} cannot be empty")

        gf = scale.get("golden_finger_interfaces")
        if require_obj(errors, gf, GF_INTERFACE_FIELDS, "golden_finger_interfaces"):
            for field in GF_INTERFACE_FIELDS:
                if empty(gf.get(field)):
                    errors.append(f"golden_finger_interfaces.{field} cannot be empty")

        handoff = scale.get("handoff_after_100")
        if require_obj(errors, handoff, HANDOFF_FIELDS, "handoff_after_100"):
            for field in HANDOFF_FIELDS:
                if empty(handoff.get(field)):
                    errors.append(f"handoff_after_100.{field} cannot be empty")

    if stage in {"scaled", "backplanned"}:
        if not isinstance(gate, dict) or gate.get("status") != "PASS":
            errors.append("scaled/backplanned requires scale_gate.status=PASS")
    post = data.get("post_selection")
    if not isinstance(post, dict):
        errors.append("post_selection must be an object")
    else:
        if stage in {"selected"} and post.get("strategic_target_status") != "blocked":
            errors.append("strategic_target_status must remain blocked before SCALE_GATE PASS")
        if stage in {"scaled", "backplanned"} and post.get("strategic_target_status") not in {"ready", "complete"}:
            errors.append("scaled/backplanned requires strategic_target_status ready/complete")
        if stage == "backplanned" and empty(post.get("climax_backplan_ref")):
            errors.append("backplanned requires climax_backplan_ref")

    for key in ("material_gap_orders", "pending_decisions"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be a list")
    return errors
