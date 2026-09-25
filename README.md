# novel-creation-planner V1.2

面向网文开书的 **市场结构学习 + 素材调度 + 高潮倒推** Codex Skill。

它不是“根据几本书模仿内容”，而是把实时赛道样本、既有 DNA 素材库和创造层规划连接成一条可审计工作流。

## 核心流程

```text
确定赛道
↓
扫描同赛道新书榜 Top10
↓
在合法可访问范围内分析 10 本前 10 章
↓
比较冲突启动 / 首次兑现 / 目标接力 / 情绪 / 钩子 / 4-10章循环
↓
按结构学习价值选 3 本，不按与未来故事的相似度选
↓
3 本继续深拆前 20 章
↓
提取 structural lessons
↓
调度共享素材库
↓
世界前提 / 势力池 / 1-N套体系 / 金手指 / 功法 / 法宝 / 普通资源
↓
创建 strategic_target 战略目标物
↓
设计前 100 章约 2 个大高潮
↓
每个高潮建立 4-8 个 backward beats
↓
反推前 100 章故事脊柱
```

## V1.2 重点

### 1. 市场样本只学结构

Top10 是同赛道实时样本池。选择 3 本深拆书时，依据的是：

- 节奏速度；
- 章末钩子；
- 情绪兑现；
- 目标接力；
- 配角功能效率；
- 前 10 章故事循环。

不因为某本书“更像我们准备写的故事”而优先选择。

### 2. 素材库组件级调度

支持从 V1.4 DNA 素材库中按组件召回：

- faction
- rule_chain
- cultivation_system
- realm
- system_relation
- technique
- artifact
- resource_asset

组件保留来源 record、book、QA 与 evidence，跨书组合属于新的创作候选，不回写来源记录。

### 3. 普通资源与战略目标物分离

`resource_asset` 用于日常成长循环，例如晶核、丹药、材料、积分。

`strategic_target` 用于阶段高潮，例如秘典、传承、神兵、稀有核心、唯一资格、世界秘密或开启下一地图的关键入口。

战略目标物必须回答：

- 主角为什么必须得到；
- 竞争者为什么也需要；
- 谁控制它；
- 进入争夺需要什么门槛；
- 拿不到会失去什么；
- 拿到后发生什么不可逆变化；
- 如何推出下一阶段。

### 4. 高潮倒推

默认优先把前 100 章做实：

- 高潮 1：约 30-45 章；
- 高潮 2：约 80-100 章。

第二高潮必须由第一高潮的结果推出。每个高潮再反推 4-8 个前置节点，而不是从第 1 章一路顺推到第 100 章。

## 项目结构

```text
.
├── README.md
├── VERSION
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── market-benchmark.md
│   ├── climax-backplanning.md
│   ├── material-dispatch.md
│   ├── execution-pipeline.md
│   ├── creation-kernel.md
│   ├── plan-schema.md
│   ├── audit-and-output.md
│   ├── shared-library.md
│   ├── source-first-book-design.md
│   ├── market-opening-synthesis.md
│   └── architecture-300.md
└── scripts/
    ├── search_dna_candidates.py
    ├── validate_creation_plan.py
    ├── validate_v12_artifacts.py
    ├── test_search_dna_candidates.py
    ├── test_validate_creation_plan.py
    └── test_validate_v12_artifacts.py
```

## 快速开始

把仓库目录作为一个 Codex Skill 使用，入口是 `SKILL.md`。

典型任务：

> 使用 novel-creation-planner V1.2，我要开一本都市高武新书。先只执行市场对标阶段：扫描同赛道新书榜 Top10，在合法范围内分析前10章，完成结构横评，选3本结构最值得学习且长处互补的作品；暂时不要调用素材库，也不要开始设计新书剧情。

市场对标完成后，再进入素材调度与高潮倒推。

## 校验

运行全部核心回归：

```bash
python -m py_compile scripts/*.py
python scripts/test_validate_creation_plan.py
python scripts/test_search_dna_candidates.py
python scripts/test_validate_v12_artifacts.py
```

校验 V1.2 市场对标产物：

```bash
python scripts/validate_v12_artifacts.py benchmark market_benchmark.json
```

校验 V1.2 高潮倒推产物：

```bash
python scripts/validate_v12_artifacts.py climax climax_backplan.json
```

## 外部依赖

完整实时工作流可能需要外部采集 Skill，例如：

- `fanqie-ranking-scan`：获取目标赛道当前榜单；
- `fanqie-novel-downloader`：读取合法公开的前 1-10 章样本；
- `fanqie-desktop-operator`：在用户拥有合法访问/导出权限时处理第 11 章以后的深拆样本。

这些采集能力不包含在本仓库中。不可用时应标记 `PARTIAL/HOLD`，不得伪造榜单或章节结论。

共享 DNA 素材库也是外部数据源，本仓库只提供调度和检索逻辑，不包含小说正文或私人素材库。

## 安全与版权边界

- 只使用公开试读、用户提供文本或用户明确授权的内容。
- 不绕过登录、付费墙、验证码、DRM、风控或访问控制。
- 学习参考书的节奏、钩子、情绪和结构，不复制人物、专名、独特设定组合、标志性表达或完整事件链。
- 市场样本、DNA candidate 和创作候选必须保持来源与状态边界。

## Version

Current version: **1.2.0**
