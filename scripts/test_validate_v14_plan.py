#!/usr/bin/env python3
"""Regression tests for V1.4 local-scale plan validator."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATOR = Path(__file__).with_name("validate_creation_plan.py")


def ref(mid: str, module: str = "worldbuilding") -> dict:
    return {
        "material_id": mid,
        "record_id": f"REC:{mid}",
        "book_id": f"BOOK:{mid}",
        "module": module,
        "qa_status": "PASS",
    }


def base_plan() -> dict:
    mats = [
        "F:1","F:2","F:3","F:4","S:1","S:2",
        "T:1","T:2","T:3","C:1","C:2","C:3",
        "A:1","A:2","R:1","R:2","R:3"
    ]
    factions = [
        {
            "faction_id": f"F{i}", "name": f"Faction{i}", "role": "local actor",
            "controlled_assets_or_permissions": "resource/permission",
            "current_interest": "gain local advantage",
            "protagonist_relation": "mixed",
            "stage_entry": "1-100",
            "material_refs": [ref(f"F:{i}")],
        }
        for i in range(1,5)
    ]
    systems = [
        {
            "system_id": f"S{i}", "name": f"System{i}", "social_status": "high" if i == 2 else "common",
            "entry_condition": "entry", "power_source": "energy",
            "current_revealed_realms": ["R1","R2","R3"],
            "strength": "strength", "weakness": "weakness",
            "resource_dependency": "resources", "can_dual_cultivate": False,
            "relation_to_protagonist": "primary" if i == 1 else "social contrast",
            "material_refs": [ref(f"S:{i}", "cultivation_system")],
        }
        for i in (1,2)
    ]
    def tech(i):
        return {
            "item_id": f"T{i}", "name": f"Technique{i}", "tier": "current",
            "system_id": "S1", "training_method": "train", "core_effect": "effect",
            "limitation": "limit", "resource_cost": "cost", "access": "access",
            "material_refs": [ref(f"T:{i}", "cultivation_system")],
        }
    def combat(i):
        return {
            "item_id": f"C{i}", "name": f"Combat{i}", "tier": "current",
            "system_id": "S1", "use_case": "fight", "combat_function": "function",
            "limitation": "limit", "first_stage": "1-100",
            "material_refs": [ref(f"C:{i}", "cultivation_system")],
        }
    def artifact(i):
        return {
            "item_id": f"A{i}", "name": f"Artifact{i}", "tier": "current",
            "system_id": "S1", "activation": "activate", "effect": "effect",
            "consumption": "consume", "limitation": "limit", "acquisition": "gain",
            "material_refs": [ref(f"A:{i}", "cultivation_system")],
        }
    def resource(i):
        return {
            "resource_id": f"R{i}", "name": f"Resource{i}", "source": "source",
            "controlled_by": "F1", "used_by": "S1", "acquisition": "task",
            "consumption": "training", "golden_finger_relation": "cannot replace",
            "material_refs": [ref(f"R:{i}")],
        }
    return {
        "schema_version": 4,
        "plan_id": "PLAN:V14:TEST",
        "status": "candidate",
        "creation_mode": "greenfield",
        "workflow_stage": "scaled",
        "brief": {},
        "shared_library_root": str(Path.cwd().resolve()),
        "market_benchmark_ref": {"benchmark_id": "MK:1"},
        "market_structural_lessons": ["MK:L1"],
        "library_usage": {"formal_card_ids": [], "dna_candidate_ids": mats, "gaps": []},
        "material_dispatch": {},
        "shared_story_core": {},
        "option_board": {},
        "selection": {
            "status": "confirmed",
            "title_option_id": "TITLE:A",
            "opening_option_id": "OPENING:A",
            "golden_finger_option_id": "GF:B",
        },
        "local_scale_1_100": {
            "scale_id": "SCALE:1",
            "scope_label": "city",
            "active_factions": factions,
            "external_factions": [],
            "faction_relations": [
                {"from":"F1","to":"F2","relation_type":"conditional_ally","reason":"shared access"},
                {"from":"F2","to":"F3","relation_type":"competitor","reason":"resource conflict"},
            ],
            "systems": systems,
            "system_relations": [
                {"from":"S1","to":"S2","relation_type":"social_hierarchy","reason":"different social prestige"}
            ],
            "progression_scope": {
                "current_revealed_realms": ["R1","R2","R3"],
                "protagonist_start_realm": "R1",
                "climax_1_expected_realm": "R2",
                "climax_2_expected_realm": "R3",
                "future_realm_hint": "higher realm exists",
            },
            "technique_pool": [tech(i) for i in (1,2,3)],
            "combat_art_pool": [combat(i) for i in (1,2,3)],
            "artifact_pool": [artifact(i) for i in (1,2)],
            "ordinary_resources": [resource(i) for i in (1,2,3)],
            "local_map_nodes": [
                {"node_id":f"M{i}","name":f"Map{i}","function":"story node","controlled_by":"F1","conflict_use":"conflict"}
                for i in (1,2,3)
            ],
            "external_map_hooks": [],
            "golden_finger_interfaces": {
                "can_strengthen": ["growth conditions"],
                "cannot_replace": ["equipment","qualification","resources"],
                "dependencies": ["training","tasks"],
                "anticipation_loop": "refresh-choice-validation-consequence-next refresh",
                "resource_loop_protection": "still needs external resources",
            },
            "handoff_after_100": {
                "protagonist_power": "R3",
                "formal_status": "local recognized actor",
                "owned_techniques": ["T1"],
                "owned_combat_arts": ["C1"],
                "owned_artifacts": ["A1"],
                "known_systems": ["S1","S2"],
                "unexpanded_systems": ["future system"],
                "active_factions": ["F1","F2","F3","F4"],
                "external_factions_touched": ["none yet"],
                "used_material_ids": mats[:5],
                "remaining_material_directions": ["higher map","new system"],
                "unpaid_promises": ["larger network"],
                "next_stage_problem": "expand beyond city",
            },
        },
        "scale_gate": {"status":"PASS","reasons":[]},
        "post_selection": {"strategic_target_status":"ready","climax_backplan_ref":{}},
        "material_gap_orders": [],
        "pending_decisions": [],
    }


def validate(payload: dict) -> bool:
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "plan.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        p = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True, encoding="utf-8")
        return p.returncode == 0


def main() -> int:
    base = base_plan()
    cases = [("valid scale", base, True)]

    few_factions = copy.deepcopy(base)
    few_factions["local_scale_1_100"]["active_factions"] = few_factions["local_scale_1_100"]["active_factions"][:3]
    cases.append(("reject too few factions", few_factions, False))

    no_conflict = copy.deepcopy(base)
    no_conflict["local_scale_1_100"]["faction_relations"] = [
        {"from":"F1","to":"F2","relation_type":"ally","reason":"same goal"}
    ]
    cases.append(("require conflict relation", no_conflict, False))

    one_system = copy.deepcopy(base)
    one_system["local_scale_1_100"]["systems"] = one_system["local_scale_1_100"]["systems"][:1]
    cases.append(("require 2 systems", one_system, False))

    missing_techniques = copy.deepcopy(base)
    missing_techniques["local_scale_1_100"]["technique_pool"] = missing_techniques["local_scale_1_100"]["technique_pool"][:2]
    cases.append(("require 3 techniques", missing_techniques, False))

    missing_artifact = copy.deepcopy(base)
    missing_artifact["local_scale_1_100"]["artifact_pool"] = missing_artifact["local_scale_1_100"]["artifact_pool"][:1]
    cases.append(("require 2 artifacts", missing_artifact, False))

    bypass_scale = copy.deepcopy(base)
    bypass_scale["workflow_stage"] = "selected"
    bypass_scale["scale_gate"] = {"status":"HOLD","reasons":["incomplete"]}
    bypass_scale["post_selection"]["strategic_target_status"] = "ready"
    cases.append(("block strategic target before scale pass", bypass_scale, False))

    failures=[]
    for name,payload,expected in cases:
        if validate(payload) != expected:
            failures.append(name)
    print(json.dumps({"ok":not failures,"cases":len(cases),"failures":failures},ensure_ascii=False,indent=2))
    return 0 if not failures else 1

if __name__ == "__main__":
    raise SystemExit(main())
