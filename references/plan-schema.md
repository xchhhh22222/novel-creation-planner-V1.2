# 创造计划机器契约 V1.5

V1.5 使用 `schema_version: 5`，在 V1.4 local scale 基础上增加“候选池扩展 + 原创重命名 + 金手指菜单引擎”。

V1—V4 继续兼容。

## V1.5 local_scale_1_100 新增字段

```json
{
  "system_candidate_pool": [],
  "active_system_ids": [],
  "latent_system_ids": [],
  "technique_pool": [],
  "active_technique_ids": [],
  "combat_art_pool": [],
  "active_combat_art_ids": [],
  "artifact_pool": [],
  "active_artifact_ids": [],
  "golden_finger_detail_pack": {}
}
```

## 体系候选池

`system_candidate_pool`：4—6项。

至少来自3本不同来源书。

每项：

```text
candidate_id
source_system_name_or_descriptor
new_system_name
core_mechanism
social_role
resource_dependency
conflict_value
fit_with_current_world
status = active|latent|rejected
selection_reason
material_refs
```

最终：

- `active_system_ids`：2—3；
- `latent_system_ids`：0—2；
- active id 必须对应 local scale 正式 `systems[].system_id`。

## 功法池

`technique_pool`：6—10项。

`active_technique_ids`：3—5项。

每项在 V1.4 字段基础上增加：

```text
source_name_or_descriptor
naming_style
rename_rationale
```

`name` 必须是新书原创名，不得等于来源名称/描述。

至少来自3本不同来源书。

## 武技池

`combat_art_pool`：8—12项。

`active_combat_art_ids`：4—6项。

新增：

```text
source_name_or_descriptor
naming_style
rename_rationale
function_category
```

至少覆盖5种 function_category，至少来自3本不同来源书。

## 法宝 / 装备池

`artifact_pool`：5—8项。

`active_artifact_ids`：2—4项。

新增：

```text
source_name_or_descriptor
naming_style
rename_rationale
```

至少来自2本不同来源书。

## 原创重命名硬门

对 technique/combat/artifact：

```text
normalize(name) != normalize(source_name_or_descriptor)
```

禁止直接沿用来源书专名。

## 每日预算菜单引擎

`golden_finger_detail_pack`：

```json
{
  "engine_type": "daily_priced_random_menu",
  "base_budget": 10,
  "menu_size": 10,
  "daily_reset": true,
  "point_carryover": false,
  "can_buy_multiple": true,
  "offer_pool": [],
  "sample_daily_menus": [],
  "progression_unlocks": [],
  "reader_hook_mechanism": ""
}
```

### offer_pool

至少24项。

每项：

```text
offer_id
source_name_or_descriptor
name
category
price
effect_value
effect_unit
effect_description
duration
prerequisite
external_dependency
material_refs
```

规则：

- price 为1—10整数；
- effect_value 为数字；
- effect_unit 非空；
- name 必须做新书化重命名；
- 至少覆盖6种 category；
- 价格带必须同时覆盖1—3、4—6、7—10；
- 整个 offer_pool 至少引用4个不同 material_id。

### sample_daily_menus

至少3张，每张：

```json
{
  "menu_id": "DAY:OPENING",
  "stage": "opening",
  "offer_ids": ["O01","...共10项"],
  "purchase_example": {
    "selected_offer_ids": ["O01","O07"],
    "total_spend": 10,
    "why_this_choice": "",
    "sacrifice": ""
  }
}
```

要求：

- 每张恰好10个不同 offer；
- 低/中/高价至少各1项；
- selected_offer_ids 必须来自当日菜单；
- total_spend 与实际价格和一致；
- total_spend <= 10；
- why_this_choice / sacrifice 非空。

### progression_unlocks

至少3项，说明商品池如何扩展、稀有类别怎样解锁，避免只有“每天重复同一批属性”。

## 校验

```bash
python scripts/validate_creation_plan.py plan.json
```

schema_version 5 自动路由到 `validate_v15_plan.py`。
