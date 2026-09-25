# novel-creation-planner V1.6

面向网文开书的 **市场结构学习 + 素材来源硬门 + 单书选项板 + 素材候选池扩展 + 每日预算菜单引擎 + 高潮状态跃迁** Codex Skill。

当前版本：**1.6.0**

> 仓库名保留历史名称 `novel-creation-planner-V1.2`，实际代码版本已升级为 V1.5。

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


## V1.4：100章局部 Scale

用户完成书名/开篇/金手指选择后，先构造 `local_scale_1_100`：

```text
4-7 当前势力 + 明确盟友/冲突
0-2 外部势力接口
2-3 套当前体系
当前境界
≥3 功法
≥3 武技
≥2 法宝/装备
3-6 普通资源
3-6 本地地图节点
金手指接口
```

更大世界不展开，只留 future hooks。

每个大高潮必须明确：

```text
实力前 → 实力后
拿到什么核心东西
身份前 → 身份后
获得什么新权限
新增什么责任/敌人
下一阶段最大问题
```

前100章结束生成 `handoff_after_100`，后继 plan 再调用剩余素材继续扩展。


## V1.5：素材池不是最低配清单

V1.5 强制“先广泛召回，再筛选”：

- 体系候选 4—6，最终 active 2—3；
- 功法候选 6—10，最终 active 3—5；
- 武技候选 8—12，最终 active 4—6；
- 法宝/装备候选 5—8，最终 active 2—4。

所有功法、武技、法宝都必须保留素材来源，但新书名称必须原创重命名，不能直接复制来源书专名。

每日10点预算型金手指必须进一步落成菜单系统：

- 每天随机展示10个商品；
- 每个商品1—10点明码标价；
- 当天可购买多个，总价不得超过10；
- 建立至少24个商品原型；
- 每个商品效果可量化/验证；
- 至少3张阶段示例菜单；
- 菜单购买必须明确“选择了什么、放弃了什么”。

这样金手指本身承担持续追读，而不是只剩“气血控制/悟性/适应”几个抽象词。


## V1.6：人物生态成为 SCALE_GATE

V1.6 修复四本 Nova pilot 暴露出的两个问题：

1. 人物功能记录不能代替女主/长线反派人物卡。Planner 必须优先调用 novel-character-card-miner 派生出的 heroine / long_arc_villain 卡，再用人物功能卡补充叙事职责。
2. V1.5 校验器误把每日10点菜单当成所有金手指的默认格式。V1.6 改为条件触发：只有选中的金手指 engine_type=daily_priced_random_menu 时才执行24+商品硬门，其它金手指按自身机制运行。

多女主模式前100章默认：heroine候选4—8、active 3—4、latent 0—2；反派候选3—6、active 2—4；配角3—6；关系发动机4—8。

每位 active 女主必须有独立目标、资源/限制、边界、与主角不可一次性替代的绑定原因、关系变化路径和独立入场窗口。任意两位 active 女主的差异化签名至少在3个维度不同。每个 active 势力至少绑定1名代表人物。