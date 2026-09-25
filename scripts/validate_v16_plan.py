#!/usr/bin/env python3
"""Validate V1.6 character ecology while preserving V1.5 material-pool gates."""

from __future__ import annotations
import copy
from typing import Any

from validate_v14_plan import validate_plan as validate_v14
from validate_v15_plan import validate_plan as validate_v15, validate_renamed_pool, validate_refs, require, norm

HEROINE_FIELDS={"candidate_id","source_character_descriptor","new_character_name","role_label","independent_goal","decision_pattern","resources","limits","boundaries","protagonist_binding_reason","why_cannot_swap_out","binding_break_condition","faction_id","first_entry_window","arc_1_100","status","selection_reason","differentiation_signature","material_refs"}
HEROINE_SIGNATURE_FIELDS={"goal_domain","faction_domain","resource_domain","combat_role","binding_reason","conflict_mode","relationship_progression"}
ANTAGONIST_FIELDS={"candidate_id","new_character_name","antagonist_layer","goal","levers","limits","plan_1_100","necessary_opposition_reason","strategy_update_rule","faction_id","status","selection_reason","material_refs"}
SUPPORT_FIELDS={"character_id","new_character_name","role","independent_goal","faction_id","material_refs"}
REL_FIELDS={"engine_id","character_ids","engine_type","mutual_need_or_conflict","recurring_plot_generation","escalation_trigger","break_condition","material_refs"}
LINK_FIELDS={"faction_id","representative_character_ids"}
LAYERS={"competitor","interest_enemy","long_arc","boss_disaster"}

def empty(v:Any)->bool:
    return v is None or v=="" or v==[] or v=={}

def _material_pools(errors:list[str], scale:dict[str,Any])->None:
    candidates=scale.get("system_candidate_pool")
    if not isinstance(candidates,list) or not 4<=len(candidates)<=6:
        errors.append("system_candidate_pool must contain 4..6 items"); candidates=[]
    cids=set(); books=set(); active=set(); latent=set()
    required={"candidate_id","source_system_name_or_descriptor","new_system_name","core_mechanism","social_role","resource_dependency","conflict_value","fit_with_current_world","status","selection_reason","material_refs"}
    for i,c in enumerate(candidates):
        w=f"system_candidate_pool[{i}]"
        if not require(errors,c,required,w): continue
        cid=str(c.get("candidate_id") or "")
        if not cid or cid in cids: errors.append(f"{w}.candidate_id must be unique/non-empty")
        cids.add(cid)
        if norm(c.get("new_system_name"))==norm(c.get("source_system_name_or_descriptor")): errors.append(f"{w}.new_system_name must be original")
        _,b=validate_refs(errors,c.get("material_refs"),f"{w}.material_refs"); books|=b
        st=c.get("status")
        if st=="active": active.add(cid)
        elif st=="latent": latent.add(cid)
        elif st!="rejected": errors.append(f"{w}.status invalid")
    if len(books)<3: errors.append("system_candidate_pool must draw from at least 3 source books")
    active_ids=scale.get("active_system_ids"); latent_ids=scale.get("latent_system_ids")
    if not isinstance(active_ids,list) or not 2<=len(active_ids)<=3: errors.append("active_system_ids must contain 2..3 items")
    elif set(map(str,active_ids))!=active: errors.append("active_system_ids must match status=active")
    if not isinstance(latent_ids,list) or len(latent_ids)>2: errors.append("latent_system_ids must contain 0..2 items")
    elif set(map(str,latent_ids))!=latent: errors.append("latent_system_ids must match status=latent")
    validate_renamed_pool(errors,scale.get("technique_pool"),6,10,scale.get("active_technique_ids"),3,5,"technique_pool",3)
    validate_renamed_pool(errors,scale.get("combat_art_pool"),8,12,scale.get("active_combat_art_ids"),4,6,"combat_art_pool",3,True)
    validate_renamed_pool(errors,scale.get("artifact_pool"),5,8,scale.get("active_artifact_ids"),2,4,"artifact_pool",2)

def _character_ecology(errors:list[str], scale:dict[str,Any])->None:
    eco=scale.get("character_ecology")
    if not isinstance(eco,dict): errors.append("character_ecology must be object"); return
    mode=eco.get("relationship_mode")
    if mode not in {"multi_heroine","single_heroine","non_romance"}: errors.append("character_ecology.relationship_mode invalid")
    heroines=eco.get("heroine_candidate_pool")
    if mode=="multi_heroine" and (not isinstance(heroines,list) or not 4<=len(heroines)<=8): errors.append("multi_heroine heroine_candidate_pool must contain 4..8"); heroines=[]
    elif not isinstance(heroines,list): errors.append("heroine_candidate_pool must be list"); heroines=[]
    hids=set(); active_h=set(); latent_h=set(); entries=set(); active_books=set(); sigs={}
    for i,h in enumerate(heroines):
        w=f"heroine_candidate_pool[{i}]"
        if not require(errors,h,HEROINE_FIELDS,w): continue
        hid=str(h.get("candidate_id") or "")
        if not hid or hid in hids: errors.append(f"{w}.candidate_id must be unique/non-empty")
        hids.add(hid)
        if norm(h.get("new_character_name"))==norm(h.get("source_character_descriptor")): errors.append(f"{w}.new_character_name must be original")
        sig=h.get("differentiation_signature")
        if not require(errors,sig,HEROINE_SIGNATURE_FIELDS,f"{w}.differentiation_signature"): sig={}
        _,books=validate_refs(errors,h.get("material_refs"),f"{w}.material_refs")
        st=h.get("status")
        if st=="active": active_h.add(hid); sigs[hid]=sig; entries.add(str(h.get("first_entry_window") or "")); active_books|=books
        elif st=="latent": latent_h.add(hid)
        elif st!="rejected": errors.append(f"{w}.status invalid")
    ah=eco.get("active_heroine_ids"); lh=eco.get("latent_heroine_ids")
    if mode=="multi_heroine":
        if not isinstance(ah,list) or not 3<=len(ah)<=4: errors.append("active_heroine_ids must contain 3..4")
        elif set(map(str,ah))!=active_h: errors.append("active_heroine_ids must match heroine status=active")
        if not isinstance(lh,list) or len(lh)>2: errors.append("latent_heroine_ids must contain 0..2")
        elif set(map(str,lh))!=latent_h: errors.append("latent_heroine_ids must match heroine status=latent")
        if len(active_books)<2: errors.append("active heroines must draw from at least 2 source books")
        if len(entries)<2: errors.append("active heroines must use at least 2 distinct first_entry_window values")
        ids=sorted(active_h)
        for x in range(len(ids)):
            for y in range(x+1,len(ids)):
                a=sigs.get(ids[x],{}); b=sigs.get(ids[y],{})
                diff=sum(str(a.get(k))!=str(b.get(k)) for k in HEROINE_SIGNATURE_FIELDS)
                if diff<3: errors.append(f"active heroines {ids[x]} and {ids[y]} differ in fewer than 3 signature fields")
    ants=eco.get("antagonist_candidate_pool")
    if not isinstance(ants,list) or not 3<=len(ants)<=6: errors.append("antagonist_candidate_pool must contain 3..6"); ants=[]
    active_a=set(); all_layers=set(); active_layers=set()
    for i,a in enumerate(ants):
        w=f"antagonist_candidate_pool[{i}]"
        if not require(errors,a,ANTAGONIST_FIELDS,w): continue
        layer=a.get("antagonist_layer")
        if layer not in LAYERS: errors.append(f"{w}.antagonist_layer invalid")
        else: all_layers.add(str(layer))
        validate_refs(errors,a.get("material_refs"),f"{w}.material_refs")
        if a.get("status")=="active": active_a.add(str(a.get("candidate_id") or "")); active_layers.add(str(layer))
    aa=eco.get("active_antagonist_ids")
    if not isinstance(aa,list) or not 2<=len(aa)<=4: errors.append("active_antagonist_ids must contain 2..4")
    elif set(map(str,aa))!=active_a: errors.append("active_antagonist_ids must match antagonist status=active")
    if len(all_layers)<3: errors.append("antagonist_candidate_pool must cover at least 3 antagonist layers")
    if len(active_layers)<2: errors.append("active antagonists must cover at least 2 antagonist layers")
    supports=eco.get("supporting_character_pool")
    if not isinstance(supports,list) or not 3<=len(supports)<=6: errors.append("supporting_character_pool must contain 3..6"); supports=[]
    for i,s in enumerate(supports):
        if require(errors,s,SUPPORT_FIELDS,f"supporting_character_pool[{i}]"): validate_refs(errors,s.get("material_refs"),f"supporting_character_pool[{i}].material_refs")
    rels=eco.get("relationship_engine_pool")
    if not isinstance(rels,list) or not 4<=len(rels)<=8: errors.append("relationship_engine_pool must contain 4..8"); rels=[]
    heroine_linked=set()
    for i,r in enumerate(rels):
        w=f"relationship_engine_pool[{i}]"
        if not require(errors,r,REL_FIELDS,w): continue
        chars=r.get("character_ids")
        if isinstance(chars,list) and "PROTAGONIST" in chars: heroine_linked|=(set(map(str,chars)) & active_h)
        validate_refs(errors,r.get("material_refs"),f"{w}.material_refs")
    if mode=="multi_heroine" and heroine_linked!=active_h: errors.append("every active heroine must have a relationship engine with PROTAGONIST")
    factions=scale.get("active_factions")
    fids={str(x.get("faction_id")) for x in factions if isinstance(x,dict) and x.get("faction_id")} if isinstance(factions,list) else set()
    links=eco.get("faction_character_links")
    if not isinstance(links,list): errors.append("faction_character_links must be list"); links=[]
    covered=set()
    for i,l in enumerate(links):
        w=f"faction_character_links[{i}]"
        if not require(errors,l,LINK_FIELDS,w): continue
        fid=str(l.get("faction_id") or "")
        reps=l.get("representative_character_ids")
        if fid not in fids: errors.append(f"{w}.faction_id must reference active_factions")
        if not isinstance(reps,list) or not reps: errors.append(f"{w}.representative_character_ids must be non-empty")
        else: covered.add(fid)
    if fids-covered: errors.append("faction_character_links missing active factions: "+", ".join(sorted(fids-covered)))

def validate_plan(data:dict[str,Any])->list[str]:
    if data.get("schema_version")!=6: return ["schema_version must be 6"]
    scale=data.get("local_scale_1_100")
    gf=scale.get("golden_finger_detail_pack") if isinstance(scale,dict) else None
    if isinstance(gf,dict) and gf.get("engine_type")=="daily_priced_random_menu":
        base=copy.deepcopy(data); base["schema_version"]=5; errors=validate_v15(base)
    else:
        base=copy.deepcopy(data); base["schema_version"]=4; errors=validate_v14(base)
        if isinstance(scale,dict): _material_pools(errors,scale)
    if isinstance(scale,dict): _character_ecology(errors,scale)
    else: errors.append("local_scale_1_100 must be object")
    return errors