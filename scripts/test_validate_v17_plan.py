#!/usr/bin/env python3
"""Regression tests for V1.7 dual entry modes."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from test_validate_v16_plan import build as build_v16

VALIDATOR = Path(__file__).with_name("validate_creation_plan.py")
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


def cards(prefix: str, material_id: str) -> list[dict]:
    return [
        {
            "candidate_id": f"{prefix}:{i:02d}",
            "material_ids": [material_id],
            "source_kind": "cluster" if i % 2 else "per_book",
            "mechanism_summary": f"{prefix} mechanism {i}",
        }
        for i in range(1, 10)
    ]


def build(mode: str = "inspiration_draw") -> dict:
    plan = build_v16()
    plan["schema_version"] = 7
    ids = plan["library_usage"]["dna_candidate_ids"]
    material_id = str(ids[0])
    plan["entry_mode"] = mode
    plan["entry_context"] = {
        "domain": "urban_gaowu",
        "default_relationship_mode": "multi_heroine",
        "world_card_window": {
            "status": "confirmed",
            "window_size": 9,
            "cards": cards("WORLD", material_id),
            "selected_candidate_ids": ["WORLD:01"],
            "selection_mode": "single",
        },
        "golden_finger_card_window": {
            "status": "confirmed",
            "window_size": 9,
            "cards": cards("GF", material_id),
            "selected_candidate_ids": ["GF:01"],
            "selection_mode": "single",
        },
        "assembly_order": ASSEMBLY_ORDER,
        "market_furnace": None,
    }
    if mode == "fusion_furnace":
        plan["entry_context"]["market_furnace"] = {
            "benchmark_id": "MK:20260928:都市高武",
            "selected_sample_ids": ["S01", "S04", "S09"],
            "structural_lesson_ids": ["MK:LESSON:001"],
            "fusion_recipe": {
                "pace": "S01",
                "hook": "S04",
                "emotion": "S04+S09",
                "goal_relay": "S01+S09",
                "payoff": "S01",
                "supporting_character_usage": "S09",
                "opening_loop": "S01+S04",
            },
            "copy_boundary": "structure only",
        }
    return plan


def validate(payload: dict) -> bool:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "plan.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.returncode == 0


def main() -> int:
    cases: list[tuple[str, dict, bool]] = [
        ("valid inspiration draw", build(), True),
        ("valid fusion furnace", build("fusion_furnace"), True),
    ]

    bad = copy.deepcopy(build())
    bad["entry_context"]["world_card_window"]["cards"] = bad["entry_context"]["world_card_window"]["cards"][:-1]
    cases.append(("reject fewer than nine world cards", bad, False))

    bad = copy.deepcopy(build())
    bad["entry_context"]["golden_finger_card_window"]["selection_mode"] = "hybrid"
    cases.append(("hybrid requires two selected cards", bad, False))

    bad = copy.deepcopy(build("fusion_furnace"))
    bad["entry_context"]["market_furnace"]["selected_sample_ids"] = ["S01", "S04"]
    cases.append(("furnace requires three samples", bad, False))

    failures = [name for name, payload, expected in cases if validate(payload) != expected]
    print(json.dumps({"ok": not failures, "cases": len(cases), "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
