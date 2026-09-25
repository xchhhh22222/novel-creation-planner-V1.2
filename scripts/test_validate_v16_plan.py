#!/usr/bin/env python3
"""Regression tests for V1.6 character ecology."""
from __future__ import annotations
import copy,json,subprocess,sys,tempfile
from pathlib import Path
from test_validate_v15_plan import build as build_v15
VALIDATOR=Path(__file__).with_name("validate_creation_plan.py")
def rr(mid,book): return {"material_id":mid,"record_id":f"REC:{mid}","book_id":book,"module":"character_card","qa_status":"PASS"}
def build():
    p=build_v15(); p["schema_version"]=6; s=p["local_scale_1_100"]; extra=[]
    sigs=[("investigation","official","information","sensor","mutual_access","safety_conflict","trust"),("business","merchant","equipment","support","resource_exchange","profit_conflict","contract_to_affection"),("escape","hostile","enemy_intel","assassin","mutual_survival","loyalty_conflict","enemy_to_ally"),("research","academy","knowledge","controller","shared_mystery","method_conflict","rival_to_partner")]
    heroines=[]
    for i,sg in enumerate(sigs,1):
        mid=f"HERO:{i}"; extra.append(mid)
        heroines.append({"candidate_id":f"H{i}","source_character_descriptor":f"source heroine {i}","new_character_name":f"新女主{i}","role_label":"heroine","independent_goal":sg[0],"decision_pattern":"acts under pressure","resources":sg[2],"limits":"limit","boundaries":"boundary","protagonist_binding_reason":sg[4],"why_cannot_swap_out":"unique access","binding_break_condition":"goal resolved","faction_id":s["active_factions"][(i-1)%len(s["active_factions"])]["faction_id"],"first_entry_window":["1-15","16-35","36-65","66-100"][i-1],"arc_1_100":"changes through choices","status":"active" if i<=3 else "latent","selection_reason":"distinct engine","differentiation_signature":{"goal_domain":sg[0],"faction_domain":sg[1],"resource_domain":sg[2],"combat_role":sg[3],"binding_reason":sg[4],"conflict_mode":sg[5],"relationship_progression":sg[6]},"material_refs":[rr(mid,f"BOOK:H{i}")]})
    layers=["competitor","interest_enemy","long_arc"]; ants=[]
    for i,layer in enumerate(layers,1):
        mid=f"ANT:{i}"; extra.append(mid); ants.append({"candidate_id":f"V{i}","new_character_name":f"新反派{i}","antagonist_layer":layer,"goal":"goal","levers":"levers","limits":"limits","plan_1_100":"plan","necessary_opposition_reason":"cannot both win","strategy_update_rule":"learn after loss","faction_id":s["active_factions"][i%len(s["active_factions"])]["faction_id"],"status":"active" if i<=2 else "latent","selection_reason":"layer coverage","material_refs":[rr(mid,f"BOOK:V{i}")]})
    supports=[]
    for i in range(1,4):
        mid=f"SUP:{i}"; extra.append(mid); supports.append({"character_id":f"S{i}","new_character_name":f"配角{i}","role":"mentor","independent_goal":"own goal","faction_id":s["active_factions"][(i-1)%len(s["active_factions"])]["faction_id"],"material_refs":[rr(mid,f"BOOK:S{i}")]})
    rels=[]
    for i in range(1,4):
        mid=f"REL:H{i}"; extra.append(mid); rels.append({"engine_id":f"R{i}","character_ids":["PROTAGONIST",f"H{i}"],"engine_type":"mutual_need","mutual_need_or_conflict":"need/conflict","recurring_plot_generation":"choices","escalation_trigger":"stakes rise","break_condition":"goal ends","material_refs":[rr(mid,f"BOOK:R{i}")]})
    mid="REL:V1"; extra.append(mid); rels.append({"engine_id":"R4","character_ids":["PROTAGONIST","V1"],"engine_type":"opposition","mutual_need_or_conflict":"exclusive goals","recurring_plot_generation":"countermoves","escalation_trigger":"loss","break_condition":"one side loses access","material_refs":[rr(mid,"BOOK:RV")]})
    reps=["H1","H2","H3","V1","V2","S1"]; links=[]
    for i,f in enumerate(s["active_factions"]): links.append({"faction_id":f["faction_id"],"representative_character_ids":[reps[i%len(reps)]]})
    s["character_ecology"]={"relationship_mode":"multi_heroine","heroine_candidate_pool":heroines,"active_heroine_ids":["H1","H2","H3"],"latent_heroine_ids":["H4"],"antagonist_candidate_pool":ants,"active_antagonist_ids":["V1","V2"],"supporting_character_pool":supports,"relationship_engine_pool":rels,"faction_character_links":links}
    p["library_usage"]["dna_candidate_ids"]+=extra; return p
def validate(payload):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"p.json"; path.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
        r=subprocess.run([sys.executable,str(VALIDATOR),str(path)],capture_output=True,text=True,encoding="utf-8"); return r.returncode==0
def main():
    base=build(); cases=[("valid v16 multi heroine",base,True)]
    x=copy.deepcopy(base); x["local_scale_1_100"]["character_ecology"]["active_heroine_ids"]=["H1"]; cases.append(("reject too few active heroines",x,False))
    x=copy.deepcopy(base); x["local_scale_1_100"]["character_ecology"]["heroine_candidate_pool"][1]["differentiation_signature"]=copy.deepcopy(x["local_scale_1_100"]["character_ecology"]["heroine_candidate_pool"][0]["differentiation_signature"]); cases.append(("reject heroine overlap",x,False))
    x=copy.deepcopy(base); x["local_scale_1_100"]["character_ecology"]["faction_character_links"]=x["local_scale_1_100"]["character_ecology"]["faction_character_links"][:-1]; cases.append(("require every faction representative",x,False))
    failures=[name for name,payload,expected in cases if validate(payload)!=expected]
    print(json.dumps({"ok":not failures,"cases":len(cases),"failures":failures},ensure_ascii=False,indent=2)); return 0 if not failures else 1
if __name__=="__main__": raise SystemExit(main())