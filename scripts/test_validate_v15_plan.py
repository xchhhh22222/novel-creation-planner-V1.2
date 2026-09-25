#!/usr/bin/env python3
"""Regression tests for V1.5 material pools and menu engine."""

from __future__ import annotations

import copy,json,subprocess,sys,tempfile
from pathlib import Path
from test_validate_v14_plan import base_plan

VALIDATOR=Path(__file__).with_name("validate_creation_plan.py")


def rr(mid,book,module="cultivation_system"):
    return {"material_id":mid,"record_id":f"REC:{mid}","book_id":book,"module":module,"qa_status":"PASS"}


def build():
    p=base_plan()
    p["schema_version"]=5
    scale=p["local_scale_1_100"]

    extra_ids=[]
    candidates=[]
    for i in range(1,5):
        mid=f"SYSX:{i}"; extra_ids.append(mid)
        candidates.append({
            "candidate_id":f"SC{i}","source_system_name_or_descriptor":f"SourceSystem{i}",
            "new_system_name":f"NewSystem{i}","core_mechanism":"mechanism",
            "social_role":"role","resource_dependency":"resource","conflict_value":"conflict",
            "fit_with_current_world":"fit","status":"active" if i<=2 else ("latent" if i==3 else "rejected"),
            "selection_reason":"reason","material_refs":[rr(mid,f"BOOK:S{i}")],
        })
    scale["system_candidate_pool"]=candidates
    scale["active_system_ids"]=["SC1","SC2"]
    scale["latent_system_ids"]=["SC3"]

    systems=scale["systems"]
    systems[0]["system_id"]="SC1"; systems[1]["system_id"]="SC2"
    scale["system_relations"][0]["from"]="SC1"; scale["system_relations"][0]["to"]="SC2"

    def tech(i):
        mid=f"TX:{i}"; extra_ids.append(mid)
        return {
            "item_id":f"T{i}","source_name_or_descriptor":f"原功法{i}","name":f"临江炼体法{i}",
            "naming_style":"local martial","rename_rationale":"function+world terminology",
            "tier":"current","system_id":"SC1","training_method":"train","core_effect":"effect",
            "limitation":"limit","resource_cost":"cost","access":"access",
            "material_refs":[rr(mid,f"BOOK:T{(i-1)%3+1}")],
        }
    def combat(i):
        mid=f"CX:{i}"; extra_ids.append(mid)
        cats=["burst","movement","defense","control","perception","armor_break","group","pursuit"]
        return {
            "item_id":f"C{i}","source_name_or_descriptor":f"原武技{i}","name":f"临江战式{i}",
            "naming_style":"urban martial","rename_rationale":"function+image",
            "function_category":cats[(i-1)%len(cats)],
            "tier":"current","system_id":"SC1","use_case":"fight","combat_function":"function",
            "limitation":"limit","first_stage":"1-100","material_refs":[rr(mid,f"BOOK:C{(i-1)%3+1}")],
        }
    def artifact(i):
        mid=f"AX:{i}"; extra_ids.append(mid)
        return {
            "item_id":f"A{i}","source_name_or_descriptor":f"原装备{i}","name":f"裂隙装备{i}",
            "naming_style":"rift tech","rename_rationale":"world use+function",
            "tier":"current","system_id":"SC1","activation":"activate","effect":"effect",
            "consumption":"consume","limitation":"limit","acquisition":"gain",
            "material_refs":[rr(mid,f"BOOK:A{(i-1)%2+1}")],
        }
    scale["technique_pool"]=[tech(i) for i in range(1,7)]
    scale["active_technique_ids"]=["T1","T2","T3"]
    scale["combat_art_pool"]=[combat(i) for i in range(1,9)]
    scale["active_combat_art_ids"]=["C1","C2","C3","C4"]
    scale["artifact_pool"]=[artifact(i) for i in range(1,6)]
    scale["active_artifact_ids"]=["A1","A2"]

    # update handoff to active names
    scale["handoff_after_100"]["owned_techniques"]=["T1"]
    scale["handoff_after_100"]["owned_combat_arts"]=["C1"]
    scale["handoff_after_100"]["owned_artifacts"]=["A1"]
    scale["handoff_after_100"]["known_systems"]=["SC1","SC2"]

    offers=[]
    cats=["permanent_stat","cultivation_speed","comprehension","skill_proficiency","perception","resistance","recovery","resource_efficiency"]
    for i in range(1,25):
        mid=f"GFITEM:{(i-1)%4+1}"
        if mid not in extra_ids: extra_ids.append(mid)
        offers.append({
            "offer_id":f"O{i:02d}","source_name_or_descriptor":f"源强化{i}",
            "name":f"预算商品{i}","category":cats[(i-1)%len(cats)],
            "price":((i-1)%10)+1,"effect_value":i,"effect_unit":"%",
            "effect_description":"measurable growth","duration":"permanent",
            "prerequisite":"training","external_dependency":"resource/task",
            "material_refs":[rr(mid,f"BOOK:G{(i-1)%4+1}","golden_finger")],
        })
    menus=[]
    menu_sets=[list(range(1,11)),list(range(8,18)),list(range(15,25))]
    for idx,nums in enumerate(menu_sets,1):
        ids=[f"O{x:02d}" for x in nums]
        # choose 1(price 1), 2(price2), 7(price7) style if present; calculate valid
        selected=[ids[0]]
        spend=offers[nums[0]-1]["price"]
        for oid in ids[1:]:
            price=next(o["price"] for o in offers if o["offer_id"]==oid)
            if spend+price<=10:
                selected.append(oid); spend+=price
        menus.append({
            "menu_id":f"MENU:{idx}","stage":f"stage{idx}","offer_ids":ids,
            "purchase_example":{"selected_offer_ids":selected,"total_spend":spend,
            "why_this_choice":"fits current task","sacrifice":"gives up another attractive offer"},
        })
    scale["golden_finger_detail_pack"]={
        "engine_type":"daily_priced_random_menu","base_budget":10,"menu_size":10,
        "daily_reset":True,"point_carryover":False,"can_buy_multiple":True,
        "offer_pool":offers,"sample_daily_menus":menus,
        "progression_unlocks":["unlock rare offers","unlock new category","improve same-price quality"],
        "reader_hook_mechanism":"menu-choice-validation-consequence-next refresh",
    }

    p["library_usage"]["dna_candidate_ids"]+=extra_ids
    return p


def validate(payload):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"p.json"; path.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
        r=subprocess.run([sys.executable,str(VALIDATOR),str(path)],capture_output=True,text=True,encoding="utf-8")
        return r.returncode==0


def main():
    base=build()
    cases=[("valid v15",base,True)]

    too_few=copy.deepcopy(base)
    too_few["local_scale_1_100"]["combat_art_pool"]=too_few["local_scale_1_100"]["combat_art_pool"][:3]
    cases.append(("reject tiny combat pool",too_few,False))

    copied=copy.deepcopy(base)
    x=copied["local_scale_1_100"]["technique_pool"][0]
    x["name"]=x["source_name_or_descriptor"]
    cases.append(("reject copied source name",copied,False))

    tiny_offer=copy.deepcopy(base)
    tiny_offer["local_scale_1_100"]["golden_finger_detail_pack"]["offer_pool"]=tiny_offer["local_scale_1_100"]["golden_finger_detail_pack"]["offer_pool"][:10]
    cases.append(("require 24 offers",tiny_offer,False))

    vague=copy.deepcopy(base)
    vague["local_scale_1_100"]["golden_finger_detail_pack"]["offer_pool"][0]["effect_value"]="more"
    cases.append(("require measurable effect",vague,False))

    bad_menu=copy.deepcopy(base)
    bad_menu["local_scale_1_100"]["golden_finger_detail_pack"]["sample_daily_menus"][0]["offer_ids"]=bad_menu["local_scale_1_100"]["golden_finger_detail_pack"]["sample_daily_menus"][0]["offer_ids"][:5]
    cases.append(("require ten offers per day",bad_menu,False))

    failures=[name for name,payload,expected in cases if validate(payload)!=expected]
    print(json.dumps({"ok":not failures,"cases":len(cases),"failures":failures},ensure_ascii=False,indent=2))
    return 0 if not failures else 1

if __name__=="__main__":
    raise SystemExit(main())
