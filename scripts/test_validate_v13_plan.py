#!/usr/bin/env python3
"""Regression tests for novel-creation-planner V1.3."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_creation_plan.py")


def ref(mid: str, module: str) -> dict:
    return {
        "material_id": mid,
        "module": module,
        "record_id": f"REC:{mid}",
        "book_id": f"BOOK:{mid}",
        "qa_status": "PASS",
    }


def backed(text: str, mid: str, module: str) -> dict:
    return {
        "candidate_text": text,
        "source_mode": "ADAPT",
        "material_refs": [ref(mid, module)],
        "retained_structure": f"retain-{text}",
        "adaptations": ["rename and reconnect interfaces"],
    }


def base_plan() -> dict:
    lessons = ["MK:LESSON:001", "MK:LESSON:002"]
    ids = [
        "WB:WORLD:1", "CS:SYSTEM:1", "WB:FACTION:1", "WB:RESOURCE:1",
        "GF:1", "GF:2", "GF:3",
    ]
    slots = [
        ("world_premise", [ref("WB:WORLD:1", "worldbuilding")]),
        ("primary_system", [ref("CS:SYSTEM:1", "cultivation_system")]),
        ("faction_ecology", [ref("WB:FACTION:1", "worldbuilding")]),
        ("resource_loop", [ref("WB:RESOURCE:1", "worldbuilding")]),
        ("golden_finger_candidates", [
            ref("GF:1", "golden_finger"),
            ref("GF:2", "golden_finger"),
            ref("GF:3", "golden_finger"),
        ]),
    ]
    return {
        "schema_version": 3,
        "plan_id": "PLAN:V13:TEST",
        "status": "candidate",
        "creation_mode": "greenfield",
        "workflow_stage": "option_board",
        "brief": {"category": "都市高武"},
        "shared_library_root": str(Path.cwd().resolve()),
        "market_benchmark_ref": {"benchmark_id": "MK:TEST", "path": "market_benchmark.json", "status": "complete"},
        "market_structural_lessons": lessons,
        "library_usage": {"formal_card_ids": [], "dna_candidate_ids": ids, "gaps": []},
        "material_dispatch": {
            "status": "complete",
            "slots": [
                {
                    "slot_id": f"SLOT:{role.upper()}",
                    "role": role,
                    "required": True,
                    "wave": 1,
                    "modules": [],
                    "component_types": [],
                    "query_groups": ["test"],
                    "target_candidates": 5,
                    "source_strategy": "either",
                    "selected_refs": refs,
                    "rejected_refs": [],
                    "gap_reason": "",
                }
                for role, refs in slots
            ],
            "source_concentration_risks": [],
            "compatibility_checks": [],
            "stop_reason": "required material slots covered",
        },
        "shared_story_core": {
            "core_id": "CORE:001",
            "reader_promise": "fast urban martial growth",
            "protagonist_baseline": "student under pressure",
            "longline_problem": "city power order is changing",
            "world_premise": backed("world", "WB:WORLD:1", "worldbuilding"),
            "primary_system": backed("system", "CS:SYSTEM:1", "cultivation_system"),
            "faction_ecology": backed("factions", "WB:FACTION:1", "worldbuilding"),
            "resource_loop": backed("resources", "WB:RESOURCE:1", "worldbuilding"),
            "story_engine": "goal-obstacle-payoff-next goal",
        },
        "option_board": {
            "title_options": [
                {"option_id": f"TITLE:{x}", "title": f"书名{x}", "promise_focus": f"promise{x}", "same_core_id": "CORE:001"}
                for x in ("A", "B", "C")
            ],
            "opening_options": [
                {
                    "option_id": f"OPENING:{x}",
                    "same_core_id": "CORE:001",
                    "benchmark_lesson_ids": [lessons[0]],
                    "opening_pattern": f"pattern-{x}",
                    "chapter_1_3": [
                        {"chapter": i, "goal": "goal", "obstacle": "obstacle", "payoff": "payoff", "hook": "hook"}
                        for i in (1, 2, 3)
                    ],
                    "chapter_4_10_loop": "repeatable loop",
                    "what_stays_fixed": ["world", "protagonist", "system", "mainline"],
                    "risk": "risk",
                }
                for x in ("A", "B", "C")
            ],
            "golden_finger_options": [
                {
                    "option_id": f"GFOPT:{x}",
                    "same_core_id": "CORE:001",
                    "name_candidate": f"能力{x}",
                    "source_mode": "DIRECT",
                    "material_refs": [ref(f"GF:{i}", "golden_finger")],
                    "retained_mechanism": f"mechanism-{i}",
                    "adaptations": [],
                    "input": "input",
                    "process": "process",
                    "output": "output",
                    "limits": ["limit"],
                    "costs": ["cost"],
                    "growth": "growth",
                    "first_validation_plan": "chapter 1-3 validation",
                    "compatibility_with_core": "fits system and resources",
                    "risk": "risk",
                }
                for x, i in zip(("A", "B", "C"), (1, 2, 3))
            ],
        },
        "selection": {
            "status": "pending",
            "title_option_id": "",
            "opening_option_id": "",
            "golden_finger_option_id": "",
        },
        "post_selection": {"strategic_target_status": "blocked", "climax_backplan_ref": {}},
        "material_gap_orders": [],
        "pending_decisions": ["choose title/opening/golden finger"],
    }


def validate(payload: dict) -> bool:
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "plan.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.returncode == 0


def main() -> int:
    base = base_plan()
    cases: list[tuple[str, dict, bool]] = [("valid v13 option board", base, True)]

    three_stories = copy.deepcopy(base)
    three_stories["option_board"]["opening_options"][1]["same_core_id"] = "CORE:OTHER"
    cases.append(("reject different story core", three_stories, False))

    original_gf = copy.deepcopy(base)
    original_gf["option_board"]["golden_finger_options"][0]["source_mode"] = "ORIGINAL"
    cases.append(("reject original golden finger", original_gf, False))

    missing_source = copy.deepcopy(base)
    missing_source["option_board"]["golden_finger_options"][0]["material_refs"] = []
    cases.append(("reject unsourced golden finger", missing_source, False))

    reused_gf = copy.deepcopy(base)
    for option in reused_gf["option_board"]["golden_finger_options"]:
        option["material_refs"] = [ref("GF:1", "golden_finger")]
    cases.append(("require three distinct source materials", reused_gf, False))

    early_climax = copy.deepcopy(base)
    early_climax["post_selection"]["strategic_target_status"] = "ready"
    early_climax["post_selection"]["climax_backplan_ref"] = {"path": "climax.json"}
    cases.append(("block climax before user selection", early_climax, False))

    confirmed = copy.deepcopy(base)
    confirmed["workflow_stage"] = "selected"
    confirmed["selection"] = {
        "status": "confirmed",
        "title_option_id": "TITLE:A",
        "opening_option_id": "OPENING:B",
        "golden_finger_option_id": "GFOPT:C",
    }
    confirmed["post_selection"] = {"strategic_target_status": "ready", "climax_backplan_ref": {}}
    cases.append(("allow confirmed selection", confirmed, True))

    failures = []
    for name, payload, expected in cases:
        actual = validate(payload)
        if actual != expected:
            failures.append(name)
    print(json.dumps({"ok": not failures, "cases": len(cases), "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
