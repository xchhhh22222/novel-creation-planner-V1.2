#!/usr/bin/env python3
"""Validate V1.5 material pools, original naming, and priced daily menu engine."""

from __future__ import annotations

import copy
import re
from typing import Any

from validate_v14_plan import validate_plan as validate_v14


SYSTEM_CANDIDATE_FIELDS = {
    "candidate_id","source_system_name_or_descriptor","new_system_name",
    "core_mechanism","social_role","resource_dependency","conflict_value",
    "fit_with_current_world","status","selection_reason","material_refs",
}
NAME_FIELDS = {"source_name_or_descriptor","naming_style","rename_rationale"}
OFFER_FIELDS = {
    "offer_id","source_name_or_descriptor","name","category","price",
    "effect_value","effect_unit","effect_description","duration",
    "prerequisite","external_dependency","material_refs",
}
MENU_FIELDS = {"menu_id","stage","offer_ids","purchase_example"}
PURCHASE_FIELDS = {"selected_offer_ids","total_spend","why_this_choice","sacrifice"}
GF_FIELDS = {
    "engine_type","base_budget","menu_size","daily_reset","point_carryover",
    "can_buy_multiple","offer_pool","sample_daily_menus",
    "progression_unlocks","reader_hook_mechanism",
}


def empty(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def norm(s: Any) -> str:
    return re.sub(r"[\s《》〈〉“”"'·:：._-]+","",str(s or "")).casefold()


def require(errors:list[str], obj:Any, fields:set[str], where:str)->bool:
    if not isinstance(obj,dict):
        errors.append(f"{where} must be an object")
        return False
    missing=sorted(fields-set(obj))
    if missing:
        errors.append(f"{where} missing: {', '.join(missing)}")
    return True


def refs_stats(refs:Any)->tuple[set[str],set[str]]:
    mids:set[str]=set(); books:set[str]=set()
    if isinstance(refs,list):
        for r in refs:
            if isinstance(r,dict):
                if r.get("material_id"): mids.add(str(r["material_id"]))
                if r.get("book_id"): books.add(str(r["book_id"]))
    return mids,books


def validate_refs(errors:list[str], refs:Any, where:str)->tuple[set[str],set[str]]:
    if not isinstance(refs,list) or not refs:
        errors.append(f"{where} must be non-empty list")
        return set(),set()
    for i,r in enumerate(refs):
        if not isinstance(r,dict):
            errors.append(f"{where}[{i}] must be object")
            continue
        for f in ("material_id","record_id","book_id","module","qa_status"):
            if empty(r.get(f)): errors.append(f"{where}[{i}].{f} cannot be empty")
        if r.get("qa_status") in {"FAIL","HOLD"}:
            errors.append(f"{where}[{i}].qa_status cannot be FAIL/HOLD")
    return refs_stats(refs)


def validate_renamed_pool(
    errors:list[str], items:Any, minimum:int, maximum:int,
    active_ids:Any, active_min:int, active_max:int, where:str,
    min_books:int, function_categories:bool=False
)->None:
    if not isinstance(items,list) or not minimum<=len(items)<=maximum:
        errors.append(f"{where} must contain {minimum}..{maximum} items")
        items=[]

    ids:set[str]=set(); books:set[str]=set(); categories:set[str]=set()
    for i,item in enumerate(items):
        w=f"{where}[{i}]"
        if not isinstance(item,dict):
            errors.append(f"{w} must be object"); continue
        required={"item_id","name","material_refs"}|NAME_FIELDS
        if function_categories: required.add("function_category")
        if not require(errors,item,required,w): continue
        iid=str(item.get("item_id") or "")
        if not iid or iid in ids: errors.append(f"{w}.item_id must be unique/non-empty")
        ids.add(iid)
        for f in ("name","source_name_or_descriptor","naming_style","rename_rationale"):
            if empty(item.get(f)): errors.append(f"{w}.{f} cannot be empty")
        if norm(item.get("name"))==norm(item.get("source_name_or_descriptor")):
            errors.append(f"{w}.name must be original, not copied from source")
        _,b=validate_refs(errors,item.get("material_refs"),f"{w}.material_refs")
        books|=b
        if function_categories:
            if empty(item.get("function_category")):
                errors.append(f"{w}.function_category cannot be empty")
            else: categories.add(str(item["function_category"]))

    if len(books)<min_books:
        errors.append(f"{where} must draw from at least {min_books} source books")
    if function_categories and len(categories)<5:
        errors.append(f"{where} must cover at least 5 function categories")

    if not isinstance(active_ids,list) or not active_min<=len(active_ids)<=active_max:
        errors.append(f"active ids for {where} must contain {active_min}..{active_max} items")
    elif len(set(map(str,active_ids)))!=len(active_ids):
        errors.append(f"active ids for {where} must be unique")
    elif not set(map(str,active_ids)).issubset(ids):
        errors.append(f"active ids for {where} must reference pool items")


def validate_plan(data:dict[str,Any])->list[str]:
    base=copy.deepcopy(data)
    base["schema_version"]=4
    errors=validate_v14(base)

    if data.get("schema_version")!=5:
        errors.append("schema_version must be 5")
    scale=data.get("local_scale_1_100")
    if not isinstance(scale,dict):
        errors.append("local_scale_1_100 must be object")
        return errors

    candidates=scale.get("system_candidate_pool")
    if not isinstance(candidates,list) or not 4<=len(candidates)<=6:
        errors.append("system_candidate_pool must contain 4..6 items")
        candidates=[]
    cids:set[str]=set(); books:set[str]=set()
    active_candidate_ids:set[str]=set(); latent_candidate_ids:set[str]=set()
    for i,c in enumerate(candidates):
        w=f"system_candidate_pool[{i}]"
        if not require(errors,c,SYSTEM_CANDIDATE_FIELDS,w): continue
        cid=str(c.get("candidate_id") or "")
        if not cid or cid in cids: errors.append(f"{w}.candidate_id must be unique/non-empty")
        cids.add(cid)
        for f in SYSTEM_CANDIDATE_FIELDS-{"material_refs"}:
            if empty(c.get(f)): errors.append(f"{w}.{f} cannot be empty")
        if c.get("status") not in {"active","latent","rejected"}:
            errors.append(f"{w}.status invalid")
        if norm(c.get("new_system_name"))==norm(c.get("source_system_name_or_descriptor")):
            errors.append(f"{w}.new_system_name must be original")
        _,b=validate_refs(errors,c.get("material_refs"),f"{w}.material_refs"); books|=b
        if c.get("status")=="active": active_candidate_ids.add(cid)
        if c.get("status")=="latent": latent_candidate_ids.add(cid)
    if len(books)<3: errors.append("system_candidate_pool must draw from at least 3 source books")

    active_system_ids=scale.get("active_system_ids")
    latent_system_ids=scale.get("latent_system_ids")
    if not isinstance(active_system_ids,list) or not 2<=len(active_system_ids)<=3:
        errors.append("active_system_ids must contain 2..3 items")
    if not isinstance(latent_system_ids,list) or len(latent_system_ids)>2:
        errors.append("latent_system_ids must contain 0..2 items")
    if isinstance(active_system_ids,list) and set(map(str,active_system_ids))!=active_candidate_ids:
        errors.append("active_system_ids must exactly match system_candidate_pool status=active")
    if isinstance(latent_system_ids,list) and set(map(str,latent_system_ids))!=latent_candidate_ids:
        errors.append("latent_system_ids must exactly match system_candidate_pool status=latent")

    validate_renamed_pool(errors,scale.get("technique_pool"),6,10,scale.get("active_technique_ids"),3,5,"technique_pool",3)
    validate_renamed_pool(errors,scale.get("combat_art_pool"),8,12,scale.get("active_combat_art_ids"),4,6,"combat_art_pool",3,True)
    validate_renamed_pool(errors,scale.get("artifact_pool"),5,8,scale.get("active_artifact_ids"),2,4,"artifact_pool",2)

    gf=scale.get("golden_finger_detail_pack")
    if require(errors,gf,GF_FIELDS,"golden_finger_detail_pack"):
        if gf.get("engine_type")!="daily_priced_random_menu":
            errors.append("golden_finger_detail_pack.engine_type must be daily_priced_random_menu")
        if gf.get("base_budget")!=10 or gf.get("menu_size")!=10:
            errors.append("daily menu engine requires base_budget=10 and menu_size=10")
        if gf.get("daily_reset") is not True or gf.get("point_carryover") is not False or gf.get("can_buy_multiple") is not True:
            errors.append("daily menu engine reset/carryover/multi-buy flags invalid")

        offers=gf.get("offer_pool")
        offer_ids:set[str]=set(); categories:set[str]=set(); mids:set[str]=set()
        prices:dict[str,int]={}
        if not isinstance(offers,list) or len(offers)<24:
            errors.append("offer_pool must contain at least 24 items")
            offers=[]
        for i,o in enumerate(offers):
            w=f"offer_pool[{i}]"
            if not require(errors,o,OFFER_FIELDS,w): continue
            oid=str(o.get("offer_id") or "")
            if not oid or oid in offer_ids: errors.append(f"{w}.offer_id must be unique/non-empty")
            offer_ids.add(oid)
            if norm(o.get("name"))==norm(o.get("source_name_or_descriptor")):
                errors.append(f"{w}.name must be original")
            p=o.get("price")
            if not isinstance(p,int) or not 1<=p<=10:
                errors.append(f"{w}.price must be integer 1..10")
            else: prices[oid]=p
            if not isinstance(o.get("effect_value"),(int,float)):
                errors.append(f"{w}.effect_value must be numeric")
            for f in ("effect_unit","effect_description","duration","prerequisite","external_dependency","category"):
                if empty(o.get(f)): errors.append(f"{w}.{f} cannot be empty")
            if o.get("category"): categories.add(str(o["category"]))
            m,_=validate_refs(errors,o.get("material_refs"),f"{w}.material_refs"); mids|=m

        if len(categories)<6: errors.append("offer_pool must cover at least 6 categories")
        vals=list(prices.values())
        if not any(1<=p<=3 for p in vals): errors.append("offer_pool missing low price band 1..3")
        if not any(4<=p<=6 for p in vals): errors.append("offer_pool missing mid price band 4..6")
        if not any(7<=p<=10 for p in vals): errors.append("offer_pool missing high price band 7..10")
        if len(mids)<4: errors.append("offer_pool must reference at least 4 distinct material_ids")

        menus=gf.get("sample_daily_menus")
        if not isinstance(menus,list) or len(menus)<3:
            errors.append("sample_daily_menus must contain at least 3 menus")
            menus=[]
        for i,m in enumerate(menus):
            w=f"sample_daily_menus[{i}]"
            if not require(errors,m,MENU_FIELDS,w): continue
            ids=m.get("offer_ids")
            if not isinstance(ids,list) or len(ids)!=10 or len(set(map(str,ids)))!=10:
                errors.append(f"{w}.offer_ids must contain 10 unique ids")
                ids=[]
            if not set(map(str,ids)).issubset(offer_ids):
                errors.append(f"{w}.offer_ids contains unknown offer")
            menu_prices=[prices.get(str(x),-1) for x in ids]
            if ids and not (any(1<=p<=3 for p in menu_prices) and any(4<=p<=6 for p in menu_prices) and any(7<=p<=10 for p in menu_prices)):
                errors.append(f"{w} must contain low/mid/high price offers")
            pe=m.get("purchase_example")
            if require(errors,pe,PURCHASE_FIELDS,f"{w}.purchase_example"):
                selected=pe.get("selected_offer_ids")
                if not isinstance(selected,list) or not selected:
                    errors.append(f"{w}.purchase_example.selected_offer_ids must be non-empty list")
                    selected=[]
                if not set(map(str,selected)).issubset(set(map(str,ids))):
                    errors.append(f"{w}.purchase_example selections must come from menu")
                spend=sum(prices.get(str(x),999) for x in selected)
                if pe.get("total_spend")!=spend or spend>10:
                    errors.append(f"{w}.purchase_example total_spend must equal selected prices and be <=10")
                if empty(pe.get("why_this_choice")) or empty(pe.get("sacrifice")):
                    errors.append(f"{w}.purchase_example must explain choice and sacrifice")

        unlocks=gf.get("progression_unlocks")
        if not isinstance(unlocks,list) or len(unlocks)<3 or any(empty(x) for x in unlocks):
            errors.append("progression_unlocks must contain at least 3 non-empty items")
        if empty(gf.get("reader_hook_mechanism")):
            errors.append("reader_hook_mechanism cannot be empty")

    return errors
