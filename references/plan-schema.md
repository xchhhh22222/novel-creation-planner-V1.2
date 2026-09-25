# 创造计划机器契约 V1.3

V1.3 当前写入版本为 `schema_version: 3`。

V1/V2 旧计划仍由 `scripts/validate_creation_plan.py` 兼容读取；新开书一律写 V3。

## 1. 顶层

```json
{
  "schema_version": 3,
  "plan_id": "PLAN:...",
  "status": "candidate",
  "creation_mode": "greenfield",
  "workflow_stage": "option_board",
  "brief": {},
  "shared_library_root": "D:/...",
  "market_benchmark_ref": {
    "benchmark_id": "MK:...",
    "path": "market_benchmark.json",
    "status": "complete"
  },
  "market_structural_lessons": ["MK:LESSON:001"],
  "library_usage": {
    "formal_card_ids": [],
    "dna_candidate_ids": [],
    "gaps": []
  },
  "material_dispatch": {
    "status": "complete",
    "slots": [],
    "source_concentration_risks": [],
    "compatibility_checks": [],
    "stop_reason": ""
  },
  "shared_story_core": {},
  "option_board": {
    "title_options": [],
    "opening_options": [],
    "golden_finger_options": []
  },
  "selection": {
    "status": "pending",
    "title_option_id": "",
    "opening_option_id": "",
    "golden_finger_option_id": ""
  },
  "post_selection": {
    "strategic_target_status": "blocked",
    "climax_backplan_ref": {}
  },
  "material_gap_orders": [],
  "pending_decisions": []
}
```

`workflow_stage` 允许：

- `material_hold`：核心素材不足，停止；
- `option_board`：已生成三类选项，等待用户；
- `selected`：用户已选书名/开篇/金手指；
- `backplanned`：已继续完成高潮倒推。

## 2. Shared Story Core

V1.3 只有一个故事核心：

```json
{
  "core_id": "CORE:001",
  "reader_promise": "读者核心承诺",
  "protagonist_baseline": "主角基础身份与初始困境",
  "longline_problem": "长线中心问题",
  "world_premise": {},
  "primary_system": {},
  "faction_ecology": {},
  "resource_loop": {},
  "story_engine": "持续故事发动机"
}
```

其中以下四项必须是素材支撑对象：

`world_premise / primary_system / faction_ecology / resource_loop`

统一结构：

```json
{
  "candidate_text": "用于本书的候选设定",
  "source_mode": "DIRECT|ADAPT|HYBRID",
  "material_refs": [
    {
      "material_id": "WB:...",
      "module": "worldbuilding",
      "record_id": "WB:BOOK:...",
      "book_id": "BOOK_...",
      "qa_status": "PASS"
    }
  ],
  "retained_structure": "从素材保留的结构",
  "adaptations": ["为本书做了什么兼容重设"]
}
```

默认不允许 `ORIGINAL`。

## 3. Required Material Roles

`material_dispatch.slots` 至少包含：

```text
world_premise
primary_system
faction_ecology
resource_loop
golden_finger_candidates
```

`option_board` 阶段要求前四项至少各有一个可用来源，`golden_finger_candidates` 至少有3个不同 material_id。

素材不足时把 `workflow_stage` 设为 `material_hold`，不要伪造选项。

## 4. 三个书名

`title_options` 恰好3项：

```json
{
  "option_id": "TITLE:A",
  "title": "候选书名",
  "promise_focus": "标题承诺",
  "same_core_id": "CORE:001"
}
```

书名可以原创。

## 5. 三个开篇

`opening_options` 恰好3项，全部引用同一个 core：

```json
{
  "option_id": "OPENING:A",
  "same_core_id": "CORE:001",
  "benchmark_lesson_ids": ["MK:LESSON:001"],
  "opening_pattern": "危机→解法→兑现",
  "chapter_1_3": [
    {
      "chapter": 1,
      "goal": "目标",
      "obstacle": "阻碍",
      "payoff": "兑现",
      "hook": "钩子"
    }
  ],
  "chapter_4_10_loop": "4-10章循环",
  "what_stays_fixed": ["世界", "主角", "体系", "主线"],
  "risk": "风险"
}
```

每个 `chapter_1_3` 必须恰好覆盖1、2、3章。

市场 lesson 只改变结构，不得改变 story core。

## 6. 三个金手指

`golden_finger_options` 恰好3项：

```json
{
  "option_id": "GF:A",
  "same_core_id": "CORE:001",
  "name_candidate": "候选名",
  "source_mode": "DIRECT|ADAPT|HYBRID",
  "material_refs": [],
  "retained_mechanism": "保留机制",
  "adaptations": [],
  "input": "输入",
  "process": "处理",
  "output": "输出",
  "limits": [],
  "costs": [],
  "growth": "成长",
  "first_validation_plan": "首次验证",
  "compatibility_with_core": "与世界/体系/资源如何兼容",
  "risk": "风险"
}
```

硬规则：

- 不允许 `ORIGINAL`；
- 所有 material ref 的 `module` 必须是 `golden_finger`；
- DIRECT/ADAPT 至少1个真实素材；
- HYBRID 至少2个真实素材；
- 三个选项合计至少3个不同 material_id；
- 所有 material_id 必须存在于顶层 `library_usage`。

## 7. 用户选择门

`selection.status=pending` 时：

- 三个选择 ID 必须为空；
- `post_selection.strategic_target_status=blocked`；
- `climax_backplan_ref` 必须为空；
- 不允许继续写正式高潮和100章脊柱。

`selection.status=confirmed` 时：

- 必须各选择一个有效 title/opening/golden_finger option；
- 才允许进入 `selected` 或 `backplanned`。

## 8. 市场层防火墙

市场结果只允许贡献：

`pace / hook / emotion / goal_relay / payoff / supporting_character / opening_loop / structural_lesson`

不得把市场样本里的具体金手指、世界、体系、势力、法宝、战略目标物写入本计划作为创作来源。

## 9. 校验

```bash
python scripts/validate_creation_plan.py plan.json
```

V3 会自动路由到：

```text
scripts/validate_v13_plan.py
```
