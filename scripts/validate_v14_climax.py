#!/usr/bin/env python3
"""Validate V1.4 climax backplans."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


TARGET_TYPES = {
    "manual", "inheritance", "artifact", "rare_resource", "secret",
    "technology", "control_right", "authority", "other",
}
GAIN_TYPES = {
    "technique", "artifact", "resource", "inheritance",
    "authority", "information", "other",
}
TRANSITION_FIELDS = {
    "power_before", "power_after", "combat_capability_change", "key_gain",
    "status_before", "status_after", "new_permissions",
    "new_responsibilities", "new_enemies", "next_stage_problem",
}
KEY_GAIN_FIELDS = {"name", "gain_type", "why_it_matters"}
BEAT_FIELDS = {
    "beat_id", "chapter_window", "required_state", "objective",
    "obstacle_function", "supporting_character_function", "mini_payoff",
    "hook_function", "leads_to", "benchmark_lesson_ids",
}
CLIMAX_FIELDS = {
    "climax_id", "chapter_window", "strategic_target_id", "protagonist_goal",
    "why_now", "qualification_or_access_gate", "competing_factions",
    "obstacles", "payoff", "cost", "irreversible_change", "next_stage_seed",
    "previous_climax_dependency", "benchmark_lesson_ids", "backward_beats",
    "climax_state_transition",
}
TARGET_FIELDS = {
    "target_id", "name", "target_type", "reader_promise", "known_function",
    "protagonist_need", "rival_needs", "clue_entry", "location_or_holder",
    "competing_factions", "failure_cost", "payoff_if_obtained",
    "irreversible_change", "next_stage_seed", "material_refs",
}
SPINE_FIELDS = {
    "chapter_window", "stage_objective", "main_obstacle",
    "supporting_character_functions", "payoff", "emotion_goal",
    "hook_function", "strategic_target_progress", "climax_link",
    "benchmark_lesson_ids", "state_change",
}


def empty(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def require(errors: list[str], value: Any, fields: set[str], where: str) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{where} must be an object")
        return False
    missing = sorted(fields - set(value))
    if missing:
        errors.append(f"{where} missing: {', '.join(missing)}")
    return True


def window(v: Any) -> tuple[int, int] | None:
    if not isinstance(v, str):
        return None
    m = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", v)
    if not m:
        return None
    a,b=map(int,m.groups())
    if a<1 or b<a or b>100:
        return None
    return a,b


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str]=[]
    required={
        "schema_version","backplan_id","status","horizon_chapters",
        "target_major_climax_count","scale_plan_ref","benchmark_lesson_ids",
        "strategic_targets","major_climaxes","story_spine_1_100",
        "future_climax_seeds",
    }
    if not require(errors,data,required,"backplan"):
        return errors
    if data.get("schema_version")!=2:
        errors.append("schema_version must be 2 for V1.4 climax backplan")
    if data.get("status") not in {"complete","partial","hold"}:
        errors.append("status must be complete/partial/hold")
    if data.get("horizon_chapters")!=100:
        errors.append("horizon_chapters must be 100")
    if data.get("target_major_climax_count")!=2:
        errors.append("V1.4 default backplan requires exactly 2 major climaxes")
    scale=data.get("scale_plan_ref")
    if not isinstance(scale,dict) or scale.get("status")!="PASS" or empty(scale.get("scale_id")):
        errors.append("scale_plan_ref must reference a PASS scale plan")

    targets=data.get("strategic_targets")
    target_ids:set[str]=set()
    if not isinstance(targets,list) or len(targets)<2:
        errors.append("strategic_targets must contain at least 2 targets")
        targets=[]
    for i,t in enumerate(targets):
        where=f"strategic_targets[{i}]"
        if not require(errors,t,TARGET_FIELDS,where):
            continue
        tid=str(t.get("target_id") or "")
        if not tid or tid in target_ids:
            errors.append(f"{where}.target_id must be non-empty and unique")
        target_ids.add(tid)
        if t.get("target_type") not in TARGET_TYPES:
            errors.append(f"{where}.target_type invalid; qualification/access_key belong in access gate")
        for f in TARGET_FIELDS-{"material_refs","rival_needs","competing_factions"}:
            if empty(t.get(f)):
                errors.append(f"{where}.{f} cannot be empty")
        if not isinstance(t.get("rival_needs"),list) or not t.get("rival_needs"):
            errors.append(f"{where}.rival_needs must be non-empty")
        if not isinstance(t.get("competing_factions"),list) or len(t.get("competing_factions"))<2:
            errors.append(f"{where}.competing_factions must contain at least 2 factions")
        refs=t.get("material_refs")
        if not isinstance(refs,list) or len(refs)<2:
            errors.append(f"{where}.material_refs must contain at least 2 source refs")

    climaxes=data.get("major_climaxes")
    climax_ids:set[str]=set()
    windows=[]
    if not isinstance(climaxes,list) or len(climaxes)!=2:
        errors.append("major_climaxes must contain exactly 2 climaxes")
        climaxes=[]
    for i,c in enumerate(climaxes):
        where=f"major_climaxes[{i}]"
        if not require(errors,c,CLIMAX_FIELDS,where):
            continue
        cid=str(c.get("climax_id") or "")
        if not cid or cid in climax_ids:
            errors.append(f"{where}.climax_id must be non-empty and unique")
        climax_ids.add(cid)
        w=window(c.get("chapter_window"))
        if w is None:
            errors.append(f"{where}.chapter_window must be within 1-100")
        else:
            windows.append((w[0],w[1],cid))
        if c.get("strategic_target_id") not in target_ids:
            errors.append(f"{where}.strategic_target_id must reference strategic_targets")
        for f in ("protagonist_goal","why_now","qualification_or_access_gate","payoff","cost","irreversible_change","next_stage_seed","previous_climax_dependency"):
            if empty(c.get(f)):
                errors.append(f"{where}.{f} cannot be empty")
        if not isinstance(c.get("competing_factions"),list) or len(c.get("competing_factions"))<2:
            errors.append(f"{where}.competing_factions must contain at least 2 factions")
        if not isinstance(c.get("obstacles"),list) or not c.get("obstacles"):
            errors.append(f"{where}.obstacles must be non-empty")

        tr=c.get("climax_state_transition")
        if require(errors,tr,TRANSITION_FIELDS,f"{where}.climax_state_transition"):
            for f in ("power_before","power_after","combat_capability_change","status_before","status_after","next_stage_problem"):
                if empty(tr.get(f)):
                    errors.append(f"{where}.climax_state_transition.{f} cannot be empty")
            if tr.get("power_before")==tr.get("power_after"):
                errors.append(f"{where}: power_before and power_after must differ")
            if tr.get("status_before")==tr.get("status_after"):
                errors.append(f"{where}: status_before and status_after must differ")
            gain=tr.get("key_gain")
            if require(errors,gain,KEY_GAIN_FIELDS,f"{where}.climax_state_transition.key_gain"):
                for f in KEY_GAIN_FIELDS:
                    if empty(gain.get(f)):
                        errors.append(f"{where}.climax_state_transition.key_gain.{f} cannot be empty")
                if gain.get("gain_type") not in GAIN_TYPES:
                    errors.append(f"{where}.climax_state_transition.key_gain.gain_type invalid")
            if not isinstance(tr.get("new_permissions"),list) or not tr.get("new_permissions"):
                errors.append(f"{where}.climax_state_transition.new_permissions must be non-empty")
            if not isinstance(tr.get("new_responsibilities"),list):
                errors.append(f"{where}.climax_state_transition.new_responsibilities must be list")
            if not isinstance(tr.get("new_enemies"),list):
                errors.append(f"{where}.climax_state_transition.new_enemies must be list")
            if not (tr.get("new_responsibilities") or tr.get("new_enemies")):
                errors.append(f"{where}: climax must create a new responsibility or enemy")

        beats=c.get("backward_beats")
        if not isinstance(beats,list) or not 4<=len(beats)<=8:
            errors.append(f"{where}.backward_beats must contain 4..8 beats")
            beats=[]
        for j,b in enumerate(beats):
            bwhere=f"{where}.backward_beats[{j}]"
            if not require(errors,b,BEAT_FIELDS,bwhere):
                continue
            if window(b.get("chapter_window")) is None:
                errors.append(f"{bwhere}.chapter_window invalid")
            for f in BEAT_FIELDS-{"benchmark_lesson_ids"}:
                if empty(b.get(f)):
                    errors.append(f"{bwhere}.{f} cannot be empty")
            if not isinstance(b.get("benchmark_lesson_ids"),list):
                errors.append(f"{bwhere}.benchmark_lesson_ids must be list")

    windows.sort()
    if len(windows)==2 and windows[1][0]<=windows[0][1]:
        errors.append("major climax windows must not overlap")
    if len(climaxes)==2 and isinstance(climaxes[1],dict):
        dep=str(climaxes[1].get("previous_climax_dependency") or "")
        if climaxes[0].get("climax_id") not in dep:
            errors.append("climax 2 previous_climax_dependency must explicitly reference climax 1")

    spine=data.get("story_spine_1_100")
    if not isinstance(spine,list) or len(spine)<6:
        errors.append("story_spine_1_100 must contain at least 6 nodes")
    else:
        for i,node in enumerate(spine):
            where=f"story_spine_1_100[{i}]"
            if not require(errors,node,SPINE_FIELDS,where):
                continue
            if window(node.get("chapter_window")) is None:
                errors.append(f"{where}.chapter_window invalid")
            if node.get("climax_link") not in climax_ids:
                errors.append(f"{where}.climax_link must reference major_climaxes")
            for f in SPINE_FIELDS-{"supporting_character_functions","benchmark_lesson_ids"}:
                if empty(node.get(f)):
                    errors.append(f"{where}.{f} cannot be empty")
            if not isinstance(node.get("supporting_character_functions"),list):
                errors.append(f"{where}.supporting_character_functions must be list")
            if not isinstance(node.get("benchmark_lesson_ids"),list):
                errors.append(f"{where}.benchmark_lesson_ids must be list")

    if not isinstance(data.get("future_climax_seeds"),list) or len(data.get("future_climax_seeds"))>4:
        errors.append("future_climax_seeds must be list with at most 4 items")
    return errors


def main() -> int:
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv)!=2:
        print("usage: validate_v14_climax.py <climax_backplan.json>")
        return 2
    path=Path(sys.argv[1])
    try:
        data=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(json.dumps({"ok":False,"errors":[str(exc)]},ensure_ascii=False,indent=2))
        return 1
    errors=validate(data if isinstance(data,dict) else {})
    print(json.dumps({"ok":not errors,"errors":errors},ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main())
