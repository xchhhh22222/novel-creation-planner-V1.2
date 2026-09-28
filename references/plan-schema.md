# 创造计划机器契约 V1.7

V1.7 使用 schema_version: 7，在 V1.6 人物生态与候选池基础上增加“素材抽卡 / 三书熔炉”入口元数据、9张世界观卡、9张金手指卡与固定 assembly_order。V1.7 不废弃 V1.6 的 Local Scale、人物生态、候选池和条件式金手指细节包。

V1—V6 继续兼容。

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


## V1.6 character_ecology

local_scale_1_100.character_ecology 包含 relationship_mode、heroine_candidate_pool、active_heroine_ids、latent_heroine_ids、antagonist_candidate_pool、active_antagonist_ids、supporting_character_pool、relationship_engine_pool、faction_character_links。

multi_heroine 数量契约：女主候选4—8，active 3—4，latent 0—2；反派候选3—6，active 2—4；配角3—6；关系发动机4—8。女主 active pair 的 differentiation_signature 至少3项不同；active 女主 first_entry_window 至少2种；每个 active faction 必须在 faction_character_links 中出现。

## V1.6 金手指条件校验

golden_finger_detail_pack 不再对所有金手指强制为 daily menu。若 engine_type=daily_priced_random_menu，完整继承 V1.5 的24+商品、10项菜单、明码标价、多选购买、3张示例菜单等硬门；其它金手指只按其自身来源、限制与 golden_finger_interfaces 校验。

## V1.7 entry_mode / entry_context

schema_version 7 在 V1.6 最终计划包基础上新增：

```json
{
  "entry_mode": "inspiration_draw",
  "entry_context": {
    "domain": "urban_gaowu",
    "default_relationship_mode": "multi_heroine",
    "world_card_window": {},
    "golden_finger_card_window": {},
    "assembly_order": [],
    "market_furnace": null
  }
}
```

### entry_mode

只允许：

- `inspiration_draw`
- `fusion_furnace`

V1.7 当前素材域固定为 `urban_gaowu`，默认 `multi_heroine`。暂不为其它频道/赛道制造空 schema。

### world_card_window / golden_finger_card_window

两个窗口都使用：

```json
{
  "status": "confirmed",
  "window_size": 9,
  "cards": [
    {
      "candidate_id": "WORLD:001",
      "material_ids": ["WB:..."],
      "source_kind": "cluster",
      "mechanism_summary": "运行机制摘要"
    }
  ],
  "selected_candidate_ids": ["WORLD:001"],
  "selection_mode": "single"
}
```

最终 schema_version 7 plan 中：

- `window_size` 必须为 9；
- `cards` 必须恰好 9 项且 candidate_id 唯一；
- 每张卡至少引用 1 个存在于 `library_usage` 的 material_id；
- `source_kind` 只能为 `cluster / per_book / hybrid`；
- `single` 必须选 1 张；
- `hybrid` 必须选 2 张；
- 若实际素材不足 9 个真正不同候选，应停在 PARTIAL/HOLD，不应生成一个可通过 schema 7 的“伪完整”计划。

### assembly_order

必须固定为：

```text
selected_world_core
→ character_ecology
→ faction_ecology
→ faction_character_links
→ cultivation_systems
→ technique_combat_art_artifact_resources
→ golden_finger
→ narrative_layers
→ local_scale_1_100
→ scale_gate
→ strategic_targets
→ climax_backplanning
→ story_spine_1_100
```

这个字段用于防止 Agent 因为新增抽卡/熔炉入口而跳过原本的 Planner 组装链。

### market_furnace

`inspiration_draw`：

```json
"market_furnace": null
```

`fusion_furnace` 必须：

```json
{
  "benchmark_id": "MK:...",
  "selected_sample_ids": ["S01", "S04", "S09"],
  "structural_lesson_ids": ["MK:LESSON:001"],
  "fusion_recipe": {
    "pace": "A主导",
    "hook": "B主导",
    "emotion": "B+C",
    "goal_relay": "A+C",
    "payoff": "A",
    "supporting_character_usage": "C",
    "opening_loop": "A+B"
  },
  "copy_boundary": "只迁移结构，不复制人物、专名、能力包装与连续事件链"
}
```

约束：

- selected_sample_ids 恰好 3 个且唯一；
- structural_lesson_ids 非空；
- fusion_recipe 必须覆盖 pace / hook / emotion / goal_relay / payoff / supporting_character_usage / opening_loop；
- market furnace 只解释“怎么讲”，不得替代素材库的世界、人、势力、体系、装备、资源和金手指来源。

### 校验

```bash
python scripts/validate_creation_plan.py plan.json
```

schema_version 7 自动路由到 `scripts/validate_v17_plan.py`，并继续继承 V1.6 的所有 Local Scale / 人物生态 / 候选池门。
