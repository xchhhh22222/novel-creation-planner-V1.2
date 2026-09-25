# 创造计划机器契约 V1.4

V1.4 当前写入版本为 `schema_version: 4`。

V1/V2/V3 旧计划继续兼容；新开书写 V4。

## 顶层

```json
{
  "schema_version": 4,
  "plan_id": "PLAN:...",
  "status": "candidate",
  "creation_mode": "greenfield",
  "workflow_stage": "scaled",
  "brief": {},
  "shared_library_root": "D:/...",
  "market_benchmark_ref": {},
  "market_structural_lessons": [],
  "library_usage": {},
  "material_dispatch": {},
  "shared_story_core": {},
  "option_board": {},
  "selection": {
    "status": "confirmed",
    "title_option_id": "TITLE:A",
    "opening_option_id": "OPENING:A",
    "golden_finger_option_id": "GFOPT:B"
  },
  "local_scale_1_100": {},
  "scale_gate": {
    "status": "PASS",
    "reasons": []
  },
  "post_selection": {
    "strategic_target_status": "ready",
    "climax_backplan_ref": {}
  },
  "material_gap_orders": [],
  "pending_decisions": []
}
```

`workflow_stage` 允许：

- `material_hold`
- `option_board`
- `selected`
- `scaled`
- `backplanned`

V1.3 的 shared_story_core / option_board / selection 规则继续有效。

## local_scale_1_100

```json
{
  "scale_id": "SCALE:001",
  "scope_label": "当前城市/区域",
  "active_factions": [],
  "external_factions": [],
  "faction_relations": [],
  "systems": [],
  "system_relations": [],
  "progression_scope": {},
  "technique_pool": [],
  "combat_art_pool": [],
  "artifact_pool": [],
  "ordinary_resources": [],
  "local_map_nodes": [],
  "external_map_hooks": [],
  "golden_finger_interfaces": {},
  "handoff_after_100": {}
}
```

### active_factions

必须 4—7 个。

每项：

```text
faction_id
name
role
controlled_assets_or_permissions
current_interest
protagonist_relation
stage_entry
material_refs
```

### faction_relations

至少包含：

- 1 条 `ally / conditional_ally / dependency / regulator`
- 1 条 `competitor / hostile`

每项：

```text
from
to
relation_type
reason
```

### external_factions

0—2 个，仅描述它怎样伸手进当前城市：

```text
faction_id
name
interest
local_touchpoint
future_use
material_refs
```

### systems

必须 2—3 套。

每套：

```text
system_id
name
social_status
entry_condition
power_source
current_revealed_realms
strength
weakness
resource_dependency
can_dual_cultivate
relation_to_protagonist
material_refs
```

`system_relations` 至少1条，说明社会评价、资源竞争、互补/克制/互斥等。

### progression_scope

```text
current_revealed_realms
protagonist_start_realm
climax_1_expected_realm
climax_2_expected_realm
future_realm_hint
```

只展开前100章会看到的层级。

### technique_pool / combat_art_pool / artifact_pool

- technique_pool ≥ 3
- combat_art_pool ≥ 3
- artifact_pool ≥ 2

每项必须带 `material_refs`，不允许无来源临场补造。

### ordinary_resources

3—6 项。每项说明：

```text
resource_id
name
source
controlled_by
used_by
acquisition
consumption
golden_finger_relation
material_refs
```

### local_map_nodes

3—6 个当前城市节点。

`external_map_hooks` 0—2 个，只留后继接口。

### golden_finger_interfaces

必须包含：

```text
can_strengthen
cannot_replace
dependencies
anticipation_loop
resource_loop_protection
```

### handoff_after_100

必须包含：

```text
protagonist_power
formal_status
owned_techniques
owned_combat_arts
owned_artifacts
known_systems
unexpanded_systems
active_factions
external_factions_touched
used_material_ids
remaining_material_directions
unpaid_promises
next_stage_problem
```

## SCALE_GATE

当 `workflow_stage=scaled/backplanned`：

- `scale_gate.status` 必须为 PASS；
- local scale 必须通过全部数量和引用规则；
- `post_selection.strategic_target_status` 才能为 ready。

selection 尚未确认时，local scale 不应被展开。

## 高潮

SCALE_GATE PASS 后，高潮使用 V1.4 backplan 契约：

```bash
python scripts/validate_v14_climax.py climax_backplan.json
```

每个大高潮必须包含：

```text
power_before
power_after
combat_capability_change
key_gain
status_before
status_after
new_permissions
new_responsibilities
new_enemies
next_stage_problem
```

资格/排名/准入默认是 access gate，不作为唯一 strategic target。

## 校验

```bash
python scripts/validate_creation_plan.py plan.json
```

schema_version 4 自动路由到 `validate_v14_plan.py`。
