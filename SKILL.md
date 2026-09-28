---
name: novel-creation-planner
description: V1.7 素材池驱动小说创造规划器：在V1.6人物生态与候选池基础上新增“素材抽卡 / 三书熔炉”双入口；入口只负责确定世界核心与市场结构参考，后续继续按世界→人物→势力→人物势力绑定→体系→功法武技装备资源→金手指→剧情层→Local Scale→高潮倒推的既有规划链执行。
---

# 小说创造规划总控 V1.7

本 Skill 是创造层，不是拆书层。它把用户意图、近期市场信号和已经整理好的素材转化为可写的新书计划：

`抽卡 / 熔炉入口 → selected_world_core → 主角与多女主 → 势力生态 → 人物×势力绑定 → 修炼体系 → 功法/武技/装备/资源 → 金手指候选与选择 → 情绪/剧情线/开篇/篇章结构/剧情机制 → Local Scale 1-100 → SCALE_GATE → strategic target → 两个大高潮 → 高潮倒推 → 100章handoff`

拆书 Agent 独立运行，只向素材库补充经审核的材料。本 Skill 不调度专项拆书、不生成逐章拆书档案、不新建 BOOK DNA，也不把临时热点样本自动升级为正式素材。

## 模式路由

- **V1.7 开新书必须先读取 [references/creation-entry-modes.md](references/creation-entry-modes.md)，在 `inspiration_draw` 与 `fusion_furnace` 中二选一；两种入口只改变开头，不改变后续 Planner 主链。**
- 需要扫榜、筛书、获取前10章：读取 [references/execution-pipeline.md](references/execution-pipeline.md)。
- **需要开新书的实时赛道学习：必须读取 [references/market-benchmark.md](references/market-benchmark.md)，执行 Top10 前10章比较 → 选3本 → 前20章深拆。**
- `market-opening-synthesis.md` 仅作为旧版轻量开篇横评参考，不再定义 V1.2 标准流程。
- 需要创造金手指、人物关系、世界观、修炼和资源循环：读取 [references/creation-kernel.md](references/creation-kernel.md)。
- 需要规划前300章：读取 [references/architecture-300.md](references/architecture-300.md)。
- 需要单书选项板、原创性、兼容性、来源硬门、债务和素材覆盖审核：读取 [references/audit-and-output.md](references/audit-and-output.md)。
- 需要落盘机器可检验的计划包：读取 [references/plan-schema.md](references/plan-schema.md)，并运行 `scripts/validate_creation_plan.py`。
- 保存 V1.2 市场对标包或高潮倒推包时，分别运行 `python scripts/validate_v12_artifacts.py benchmark <market_benchmark.json>` 与 `python scripts/validate_v12_artifacts.py climax <climax_backplan.json>`。
- **需要从素材库选材、决定先查什么/查多少/何时停止：必须读取 [references/material-dispatch.md](references/material-dispatch.md)。**
- **需要检查世界/体系/势力/资源/金手指是否真的来自素材库：必须读取 [references/material-source-gates.md](references/material-source-gates.md)。**
- **需要在 V1.7 已确认世界/人物/势力/体系/资产/金手指后输出书名与开篇包装候选：读取 [references/single-story-option-board.md](references/single-story-option-board.md)。旧 schema 中的3个金手指选项仅作兼容映射，不得替换用户已在9张卡中确认的机制。**
- 需要定位、迁移或复用跨书素材库：读取 [references/shared-library.md](references/shared-library.md)。
- **用户选定后，需要补当前100章局部世界：必须读取 [references/local-scale-100.md](references/local-scale-100.md)。**
- **需要扩充体系/功法/武技/法宝并做原创重命名：必须读取 [references/material-pool-expansion.md](references/material-pool-expansion.md)。**
- **若金手指属于每日预算/随机菜单型：必须读取 [references/golden-finger-menu-engine.md](references/golden-finger-menu-engine.md)。**
- **需要设计多女主、长线反派、配角和人物—势力关系：必须读取 [references/character-ecology-100.md](references/character-ecology-100.md)。**
- **需要设计战略目标物、前100章两个大高潮并反推：必须读取 [references/climax-backplanning.md](references/climax-backplanning.md)。**
- 需要纯素材先行的备用模式：读取 [references/source-first-book-design.md](references/source-first-book-design.md)。

按任务读取相关 reference，不要为了保险一次加载全部内容。

## 创作模式先判定

- **从零开书（默认）**：用户说“开新书”“根据榜单给我一个规划”或未指定现有书时，只使用用户本次要求、实时榜单前10本的合格前10章、共享素材库和原创推演。不得读取或继承当前工作目录中的总纲、人物库、世界观、角色姓名、金手指或硬约束，也不得以“兼容现有小说”为卖点。
- **现有项目改版（仅显式触发）**：只有用户明确指定某本书、要求续作、改版或兼容现有资料时，才读取该书正式资料并执行项目兼容审计。

工作目录属于某本小说，不代表用户正在改这本小说。模式不明但用户使用“新书”措辞时，一律按从零开书处理。

## 输入优先级

从零开书：

1. 用户本次确认的题材、平台、读者、核心偏好和禁区；
2. 带日期、榜单和来源的实时市场数据；
3. 新书榜前10本中质量合格的前10章；
4. 用户指定的共享素材库中的正式 active 卡与有证据路径的 DNA candidate；
5. 原创推演与模型常识。

现有项目改版：

1. 用户当前明确确认的题材、平台、读者、核心想法和禁区；
2. 当前项目的正式总纲、世界观、人物库和硬约束；
3. 带日期、榜单和来源的实时市场数据；
4. 合法公开、试读、用户提供或已获授权的开篇样本；
5. 正式 active 素材卡；
6. 有证据路径的 DNA candidate；
7. 模型常识与创作推断。

低优先级输入不能覆盖高优先级事实。市场热门只证明近期存在某种信号，不自动证明因果，也不能覆盖用户的核心创意。

## 执行与思考分层

用户要求多代理且环境可用时，优先分成两个互不越权的角色：

- **执行代理（优先 Luna）**：扫榜、规范化榜单、筛选样本、获取允许读取的章节、检查文件质量并生成样本包。不得替创作层作结论。
- **思考代理（优先 Sol）**：研究市场信号、匹配素材、构造三案、推演300章并审计持续性。不得把执行代理的主观判断当事实。

主代理负责冻结输入、处理冲突、整合结果和最终验收。指定模型不可用时按同一角色契约由当前代理完成，不阻断任务。

## 总工作流 V1.7

### 0. 入口只二选一

当前 Nova 素材域固定为都市高武，默认人物关系模式为多女主。暂不增加男频/女频频道切换，也不为尚未建立素材库的赛道制造空入口。

- `inspiration_draw`：直接从 Nova 的世界观 cluster/per_book 中宽召回、去重，向用户展示 9 个世界候选；用户选 1 个或融合 2 个。
- `fusion_furnace`：先执行 Top10 → 选 3 本 → 前20章深拆 → structural lessons → market fusion recipe，再回 Nova 展示 9 个世界候选；市场三书只回答“怎么讲”，不能直接提供新书核心设定。

若素材不足 9 个真正不同且证据合格的候选，返回 PARTIAL/HOLD，不得把同一机制换名字凑 9 张。

### 1. 冻结 selected_world_core

世界观候选必须来自 `03_世界观` 的 cluster / per_book / component，并保留 material_id、record_id、book_id、qa_status。用户未确认世界核心前，不进入正式人物、势力、体系和高潮规划。

### 2. 先搭主角与多女主人物生态

读取 `05_人物功能`、heroine_character、long_arc_villain、relationship_engine。先确定主角的初始身份、社会位置、欲望、缺口和世界矛盾，再建立女主/反派/配角候选。人物不能只用性格标签代替独立目标、资源、边界和关键选择。

### 3. 建立势力生态

从 `03_世界观` 召回 faction / institution / resource control，建立 4—7 个 active factions、0—2 个 external factions，并明确控制资源、当前利益以及 ally / competitor / hostile / regulator / dependency 等关系。

### 4. 再做人物 × 势力绑定

建立 `faction_character_links`。主角、active 女主、长线反派和关键配角必须进入势力网络；每个 active faction 至少绑定 1 名代表人物。禁止“人物一套、势力一套，互不相干”。

### 5. 修炼体系候选池

读取 `04_修炼体系`：先建 4—6 套 system candidate，再选 2—3 套 active，允许 0—2 套 latent。体系必须解释其社会地位、资源依赖、准入条件与势力控制关系。

### 6. 功法 / 武技 / 装备 / 普通资源

继续按 V1.5/V1.6 候选池门执行：

- 功法 6—10 → active 3—5；
- 武技 8—12 → active 4—6；
- 法宝/装备 5—8 → active 2—4；
- 普通资源 3—6。

所有候选从素材库召回并原创重命名，必须适配已选人物、势力、体系与资源循环。

### 7. 金手指 9 张卡

这一步才从 `02_金手指` 宽召回。先检查世界接口、体系接口、资源循环、人物利益与中心矛盾，再去重并向用户展示 9 个候选。用户可选 1 个、融合 2 个、换单张或重抽。

9 是展示窗口，不是数据库上限；素材不足时 PARTIAL/HOLD，不允许模型原创凑满。选中的金手指不能无代价消灭世界主要问题、势力资源循环或人物冲突。

### 8. 剧情层让世界跑起来

在静态世界、人物、势力、成长与金手指接口稳定后，再调用：

- 01 章节情绪；
- 06 剧情线；
- 07 开篇；
- 08 篇章结构；
- 09 剧情机制。

这里解决 promise / rhythm / payoff、目标与代价、开篇接力、arc 状态变化、可重复剧情发动机，不得反向覆盖前面已经确认的世界事实。

### 9. 形成 shared_story_core 与包装选项

在上述组件已经有素材来源和兼容接口后，形成一个 shared_story_core。书名、开篇等包装层可以继续提供候选供用户确认，但不能再把“3个金手指”当作早于人物/势力/体系的入口硬门。若为了旧 schema 兼容保留 option_board，必须映射到用户已经从 9 张金手指卡中确认的机制，不得偷偷换机制。

### 10. 构造 Local Scale 1-100

把已确认的世界、人物、势力、体系、资产、资源、金手指和剧情发动机写入 `local_scale_1_100`。继续执行 V1.6 的人物生态数量门、候选池利用率门、原创重命名门与 `handoff_after_100`。

### 11. SCALE_GATE

Scale 不完整时 HOLD。必须先验证：

- 势力闭环；
- 人物—势力覆盖；
- 多女主差异化；
- 体系关系；
- 功法/武技/装备/资源；
- 金手指接口；
- 本地地图；
- 可重复剧情发动机。

### 12. strategic target 与两个大高潮

SCALE_GATE=PASS 后，在当前 scale 内继续调度战略目标物和高潮母型。默认前100章约两个大高潮，每个都必须有实力、核心收获、身份/权限、责任/敌人与下一阶段问题的状态跃迁；高潮2由高潮1后果推出。

### 13. 高潮倒推与 1—100 章故事脊柱

每个高潮先做 4—8 个 backward beats，再填中间小目标、小高潮、钩子、情绪兑现和资源变化。最后输出 `handoff_after_100`，供后继计划继续调用剩余素材。

## 不可省略的边界

- 不绕过登录、付费墙、验证码、robots 或访问控制。权限不明时只保留 metadata，不能下载正文。
- **证据硬门**：未读过榜单作品正文时，不得断言其开篇剧情或按其正文节奏推荐；仍可基于已核验的素材库给出标明“市场未验证”的候选方案。市场结论必须回指 sample_id 与实际章节范围；样本少于6本时标 `partial`，不宣称完整横评。
- 不复制参考书人物、专名、标志性表达、独特设定组合或完整事件链。每次借鉴至少重设四个关键维度。
- 跨书组合时必须区分 `来源事实 → 抽象组件 → 新书候选`；不得把 A 书体系 + B 书功法 + C 书法宝的组合描述成任何来源书本来就有的结构。
- 不允许先写方案再反向给素材贴标签。必须先完成市场结构学习与素材槽位，再形成候选组合。
- Top10→3本的筛选理由只能是结构学习价值与互补性，不能是“更像我们准备写的书”。
- 市场样本只提供结构 lesson；具体羞辱、测试、秘境、人物、能力、奖励等事件包装不得直接搬进新书。
- 普通 `resource_asset` 与创造层 `strategic_target` 必须分开：前者支撑日常成长，后者支撑阶段高潮。
- 核心组件来源过度集中时必须报告 `SOURCE_CONCENTRATION_RISK`；同源 system+realm+technique 可作为一个成长组件包理解，但世界、金手指、高潮继续同源时必须额外重构。
- 临时市场样本、candidate 和工作方案都不是本书事实。重大设定进入正式资料前必须由用户确认。
- `candidate` 并非不可用于构思：已通过 QA 且章节证据足够的单书候选可明确标注来源与缺口后供用户选择；`HOLD`、未知项及章节覆盖外内容不得冒充已验证事实。
- 候选阶段可以原创书名、角色名和表面包装，但世界前提、主体系、势力生态、资源循环、金手指和战略目标物必须服从素材来源硬门。不能因为标记了 `【候选设定】` 就绕过来源要求。
- 金手指必须先通过 `GOLDEN_FINGER_SOURCE_GATE`，再检查与世界输入、修炼验证、资源消耗、人物利益和长期主线的闭环；素材不足时 HOLD，不允许临场原创。
- 300章规划必须存在至少两次结构刷新；不能只靠换地图、抬数值和更强敌人延长。
- 对素材不足的阶段标记 `GAP` 并输出需求，不用无来源内容伪装成素材支持。
- 默认只在对话中展示候选。写入章纲、小说资料、素材库或调用记录仍需用户明确授权。

## 完成标准

- 市场样本带平台、榜单、日期、来源和访问边界；Top10 排名位置全部保留，合格前10章正文样本通常不少于6本，否则标记偏差；完整 V1.2 对标还要求3本深拆至前20章。
- 市场证据必须包含新书榜前10名清单、逐书前10章下载状态、逐书开篇卡和横向信号矩阵；不能只有排名、书名、简介或标签。
- 不再要求三个完整故事。V1.7 的 9 张世界卡与 9 张金手指卡是素材筛选窗口；后续书名和开篇包装候选必须服务同一个 shared_story_core。
- 抽卡模式必须能回答“9张世界卡分别来自哪里、为什么不同”；熔炉模式还必须回答“Top10学到了什么结构、3本为什么入选、fusion recipe是什么”。进入金手指阶段后必须展示9张有来源且已做兼容检查的候选。世界、人物、势力、体系、资源和金手指未确认前，不得跳到高潮。
- 选定方案的金手指必须有名称、输入、处理、输出、限制、代价、失败状态、克制方式和阶段成长；只有每日预算型才必须有24+商品原型与3张10项示例菜单。前100章 local scale 必须包含4—7个势力闭环、4—6套体系候选/2—3套active、6—10功法候选、8—12武技候选、5—8法宝装备候选、3—6种普通资源、3—6个本地地图节点；人物生态必须满足所选 relationship_mode，对多女主方案要求4—8女主候选/3—4 active、3—6反派候选/2—4 active、3—6配角、4—8关系发动机，并通过女主差异化与势力代表人物检查。
- 只有用户要求七阶段或前300章规划时，七个阶段才逐一包含目标、冲突、成长、资源、人物、情绪兑现、主线进展、疲劳刷新和不可逆状态变化。
- V1.7 第一轮只执行入口：抽卡直接给9张世界卡；熔炉先给三书 structural fusion，再给9张世界卡。用户确认世界后才按人物→势力→绑定→体系→资产/资源→9张金手指→剧情层逐步推进。SCALE_GATE 通过后才输出战略目标物、两个高潮倒推锚点、债务账本、风险和待确认项。
- 素材缺口订单只描述所需功能、阶段、情绪和验收标准，不指定照搬某本书。
