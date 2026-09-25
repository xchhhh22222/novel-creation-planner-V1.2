#!/usr/bin/env python3
"""Regression tests for V1.4 climax validator."""

from __future__ import annotations

import copy,json,subprocess,sys,tempfile
from pathlib import Path

VALIDATOR=Path(__file__).with_name("validate_v14_climax.py")

def target(i):
    return {
        "target_id":f"TARGET:{i}","name":f"Target{i}","target_type":"artifact",
        "reader_promise":"wanted prize","known_function":"changes combat",
        "protagonist_need":"needed now","rival_needs":["rival needs it"],
        "clue_entry":"clue","location_or_holder":"site",
        "competing_factions":["F1","F2"],"failure_cost":"lose opportunity",
        "payoff_if_obtained":"new capability","irreversible_change":"status changes",
        "next_stage_seed":"opens next problem",
        "material_refs":[{"material_id":f"M{i}A"},{"material_id":f"M{i}B"}],
    }

def beat(cid,i,start):
    return {
        "beat_id":f"{cid}:B{i}","chapter_window":f"{start}-{start+2}",
        "required_state":"state","objective":"objective","obstacle_function":"gate",
        "supporting_character_function":"pressure","mini_payoff":"progress",
        "hook_function":"next question","leads_to":cid if i==4 else f"{cid}:B{i+1}",
        "benchmark_lesson_ids":[],
    }

def climax(cid,target_id,window,dep,power_before,power_after,status_before,status_after,start):
    return {
        "climax_id":cid,"chapter_window":window,"strategic_target_id":target_id,
        "protagonist_goal":"obtain target","why_now":"window closes",
        "qualification_or_access_gate":"entry qualification",
        "competing_factions":["F1","F2"],"obstacles":["rival","environment"],
        "payoff":"wins target","cost":"pays cost","irreversible_change":"world notices",
        "next_stage_seed":"next stage","previous_climax_dependency":dep,
        "benchmark_lesson_ids":[],
        "backward_beats":[beat(cid,i,start+(i-1)*3) for i in range(1,5)],
        "climax_state_transition":{
            "power_before":power_before,"power_after":power_after,
            "combat_capability_change":"new combat layer",
            "key_gain":{"name":"core prize","gain_type":"artifact","why_it_matters":"opens stronger route"},
            "status_before":status_before,"status_after":status_after,
            "new_permissions":["higher mission access"],
            "new_responsibilities":["protect team"],
            "new_enemies":[],
            "next_stage_problem":"larger threat",
        },
    }

def plan():
    c1=climax("CLIMAX:01","TARGET:1","35-42","ROOT","R1","R2","student","recognized fighter",10)
    c2=climax("CLIMAX:02","TARGET:2","86-96","CLIMAX:01 result opens main rift","R2","R3","recognized fighter","local team leader",55)
    spine=[]
    for w,link in [("1-10","CLIMAX:01"),("11-20","CLIMAX:01"),("21-34","CLIMAX:01"),("35-42","CLIMAX:01"),("43-70","CLIMAX:02"),("71-85","CLIMAX:02"),("86-96","CLIMAX:02"),("97-100","CLIMAX:02")]:
        spine.append({
            "chapter_window":w,"stage_objective":"goal","main_obstacle":"obstacle",
            "supporting_character_functions":["pressure"],"payoff":"payoff","emotion_goal":"anticipation",
            "hook_function":"new goal","strategic_target_progress":"progress",
            "climax_link":link,"benchmark_lesson_ids":[],"state_change":"changed",
        })
    return {
        "schema_version":2,"backplan_id":"BP:V14","status":"complete","horizon_chapters":100,
        "target_major_climax_count":2,"scale_plan_ref":{"scale_id":"SCALE:1","status":"PASS"},
        "benchmark_lesson_ids":[],"strategic_targets":[target(1),target(2)],
        "major_climaxes":[c1,c2],"story_spine_1_100":spine,"future_climax_seeds":[],
    }

def validate(payload):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"c.json"; p.write_text(json.dumps(payload),encoding="utf-8")
        r=subprocess.run([sys.executable,str(VALIDATOR),str(p)],capture_output=True,text=True)
        return r.returncode==0

def main():
    base=plan()
    cases=[("valid",base,True)]
    qualification=copy.deepcopy(base)
    qualification["strategic_targets"][0]["target_type"]="qualification"
    cases.append(("qualification cannot be sole target",qualification,False))
    same_power=copy.deepcopy(base)
    same_power["major_climaxes"][0]["climax_state_transition"]["power_after"]="R1"
    cases.append(("power must change",same_power,False))
    same_status=copy.deepcopy(base)
    same_status["major_climaxes"][0]["climax_state_transition"]["status_after"]="student"
    cases.append(("status must change",same_status,False))
    no_permission=copy.deepcopy(base)
    no_permission["major_climaxes"][0]["climax_state_transition"]["new_permissions"]=[]
    cases.append(("permission required",no_permission,False))
    no_scale=copy.deepcopy(base)
    no_scale["scale_plan_ref"]["status"]="HOLD"
    cases.append(("scale pass required",no_scale,False))
    failures=[name for name,payload,expected in cases if validate(payload)!=expected]
    print(json.dumps({"ok":not failures,"cases":len(cases),"failures":failures},ensure_ascii=False,indent=2))
    return 0 if not failures else 1

if __name__=="__main__":
    raise SystemExit(main())
