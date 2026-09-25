# novel-creation-planner V1.3

面向网文开书的 **市场结构学习 + 素材来源硬门 + 单书选项板 + 高潮倒推** Codex Skill。

当前版本：**1.3.0**

> 仓库名保留历史名称 `novel-creation-planner-V1.2`，实际代码版本已升级为 V1.3。

## 核心变化

V1.2 会生成三个完整开书方向。V1.3 已取消这种模式。

现在固定为：

```text
同赛道 Top10
↓
学习节奏 / 情绪 / 钩子 / 目标接力
↓
选3本深拆前20章
↓
structural lessons
↓
素材来源硬门
↓
world / system / factions / resource loop
↓
一个 shared_story_core
↓
3个书名
3个开篇
3个素材溯源金手指
↓
等待用户选择
↓
selected_story_variant
↓
strategic target
↓
前100章约2个大高潮
↓
高潮倒推
```

## 最重要的边界

### 市场只负责“怎么讲”

市场层可以学习：

- 节奏；
- 钩子；
- 情绪；
- 目标接力；
- 兑现频率；
- 配角功能；
- 开篇循环。

市场层不能提供新书的：

- 世界前提；
- 金手指；
- 修炼体系；
- 势力；
- 功法法宝；
- 战略目标物。

### 素材库负责“拿什么讲”

以下核心槽位默认必须有真实素材来源：

- world_premise
- primary_system
- faction_ecology
- resource_loop
- golden_finger_candidates

素材不足就 GAP/HOLD，不让 AI 临场补造。

### 金手指最高强度来源门

三个金手指候选：

- 必须全部来自素材库；
- 只能 DIRECT / ADAPT / HYBRID；
- 不允许 ORIGINAL；
- 三个选项合计至少3个不同 material_id；
- HYBRID 至少2个真实素材来源。

## 项目结构

```text
.
├── README.md
├── VERSION
├── SKILL.md
├── agents/
├── references/
│   ├── market-benchmark.md
│   ├── material-source-gates.md
│   ├── material-dispatch.md
│   ├── single-story-option-board.md
│   ├── climax-backplanning.md
│   └── ...
└── scripts/
    ├── search_dna_candidates.py
    ├── validate_creation_plan.py
    ├── validate_v13_plan.py
    └── test_validate_v13_plan.py
```

## 典型使用

> 使用 novel-creation-planner V1.3。保留已经完成的都市高武市场 structural lessons。现在进入素材调度阶段：先从素材库检索并回查 world_premise、primary_system、faction_ecology、resource_loop 和至少3个真实金手指候选。只建立一个 shared_story_core，然后给我3个书名、3个开篇、3个金手指选择。金手指必须标明素材ID与 DIRECT/ADAPT/HYBRID。不要设计三个完整故事，也不要在我选择前生成正式高潮。

## 校验

```bash
python -m py_compile scripts/*.py
python scripts/test_validate_creation_plan.py
python scripts/test_search_dna_candidates.py
python scripts/test_validate_v12_artifacts.py
python scripts/test_validate_v13_plan.py
```

V3 plan：

```bash
python scripts/validate_creation_plan.py plan.json
```

`validate_creation_plan.py` 会自动把 schema_version 3 路由到 `validate_v13_plan.py`。

## 外部依赖

实时榜单/章节采集能力和共享 DNA 素材库不包含在本仓库中。

采集或素材不可用时必须 PARTIAL/HOLD，不得伪造证据或绕过访问控制。
