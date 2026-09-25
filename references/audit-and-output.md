# 审计与输出 V1.3

## 一、市场结构学习审计

在素材调度前检查：

- Top10 是否来自同一赛道、同一快照；
- 是否尽量完成10本前10章；
- 3本深拆书是否按结构长处与互补性选出，而不是按未来故事相似度；
- 深拆是否覆盖目的、阻碍、配角功能、兑现、情绪、钩子和下一章点击理由；
- structural lesson 是否去掉来源书的专名与具体事件包装；
- 每条 lesson 是否能回指 sample_id 与章节。

市场层只能回答“怎么讲”，不得产出新书的世界、金手指、体系、势力、法宝或战略目标物。

## 二、素材来源硬门审计

生成选项板前必须检查：

- world_premise 有真实素材来源；
- primary_system 有真实素材来源；
- faction_ecology 有真实素材来源；
- resource_loop 有真实素材来源；
- golden_finger_candidates 至少覆盖3个不同真实 material_id；
- component 保留 record_id / book_id / qa_status；
- QA=FAIL/HOLD 的素材不能支撑通过硬门的核心槽位；
- 不允许先写故事再反向给素材贴标签。

任一 required slot 不足时，输出 GAP/HOLD，不得用原创补齐。

## 三、单书选项板审计

V1.3 只有一个 shared_story_core。

选项板只允许：

1. 3个书名；
2. 3个开篇；
3. 3个金手指。

### 书名

书名可以原创，但必须承诺同一个故事，不能通过标题暗示另一套世界或能力。

### 开篇

三个开篇必须：

- same_core_id 相同；
- 只引用 market structural lessons；
- 只改变冲突启动、首次兑现、目标接力和钩子安排；
- 不改变世界前提、主角基线、主体系、核心势力和长线问题。

### 金手指

三个金手指必须：

- 全部有素材来源；
- source_mode 只能 DIRECT / ADAPT / HYBRID；
- 不允许 ORIGINAL；
- 三个选项合计至少3个不同 material_id；
- HYBRID 至少2个真实来源；
- 说明 retained_mechanism；
- 说明与当前世界、体系、资源循环的兼容性。

## 四、用户选择门

selection=pending 时必须停止。

不得提前：

- 替用户选择“推荐金手指”并继续写；
- 把某个开篇当成默认正式版本；
- 生成正式 strategic_target；
- 生成两个大高潮；
- 生成前100章脊柱。

用户分别确认书名、开篇、金手指后，才能进入 selected/backplanned。

## 五、前100章局部 Scale 审计

用户完成选择后，不得直接进入高潮。

先检查：

- active factions 是否4—7个，并有明确盟友/冲突/依赖关系；
- external factions 是否只保留0—2个“伸手进来”的高层势力；
- 当前体系是否2—3套，并明确社会评价、资源竞争与主角关系；
- 境界是否只展开前100章会看到的层级；
- technique_pool 是否至少3项；
- combat_art_pool 是否至少3项；
- artifact_pool 是否至少2项；
- ordinary_resources 是否3—6项；
- local_map_nodes 是否3—6项；
- golden_finger_interfaces 是否说明能做什么、不能替代什么、怎样制造追读期待；
- handoff_after_100 是否可供后继 plan 接续。

缺失则 SCALE_GATE=HOLD。

## 六、选定版本后的完整审计

冻结 selected_story_variant 后检查：

- 金手指—世界—体系—资源闭环；
- 核心势力是否有真实利益；
- strategic_target 是否有素材支撑而非凭空发明；
- 第一高潮是否自然推出第二高潮；
- 每个高潮是否有兑现、代价、不可逆变化；
- 每个高潮是否有4—8个 backward beats；
- 小剧情是否服务阶段目标或高潮前置条件。

## 七、原创性

可以借运行结构，不复制：

- 人物姓名；
- 原组织名；
- 原能力专名；
- 原物品专名；
- 标志性表达；
- 完整连续事件链；
- 独特设定组合。

DIRECT 表示直接保留“机制层”，不是复制原书包装。

## 八、来源集中度

world_premise、golden_finger、primary_system、faction_ecology、climax_pattern 如果3项以上高度依赖同一本来源书，触发 SOURCE_CONCENTRATION_RISK。

同书 system + realm + technique 可以作为一个成长组件包理解，不机械按三次借鉴计算。

## 九、统一债务账本

维护情绪债、成长债、资源债、人物关系债、地图/规则债、反派压力债、主线/伏笔债。

升级、击杀、获奖和拿资源本身不自动算兑现；至少要有公开结果、他人反应、关系动作、代价回响或主角选择被验证。

## 十、输出顺序

### 用户尚未选择

固定输出：

1. 市场结构 lessons；
2. 一个 shared_story_core；
3. 核心素材来源表；
4. 3个书名；
5. 3个开篇；
6. 3个金手指及来源、DIRECT/ADAPT/HYBRID；
7. GAP / 风险；
8. 等待用户选择。

不要输出三个完整故事。

### 用户已选择

再输出：

1. selected_story_variant；
2. local_scale_1_100（势力关系、体系、境界、功法/武技/法宝、资源、地图、金手指接口）；
3. SCALE_GATE 结果；
4. strategic_target；
5. 前100章两个大高潮及每个高潮的实力/收获/身份/权限跃迁；
6. backward beats；
7. story spine；
8. handoff_after_100；
9. 债务与缺口。


## V1.5 素材池利用率审计

SCALE_GATE 之前额外检查：

- system_candidate_pool 是否4—6，并至少来自3本来源书；
- active systems 是否2—3，latent systems 是否0—2；
- technique_pool 是否6—10，active是否3—5；
- combat_art_pool 是否8—12，active是否4—6，且至少覆盖5种战斗功能；
- artifact_pool 是否5—8，active是否2—4；
- 功法/武技池是否至少来自3本来源书，法宝池至少2本；
- 候选是否先展示来源机制，再做当前世界适配；
- 是否因为“用户举例武道+异能”就停止继续检索其它兼容体系。

### 原创命名审计

所有 technique / combat_art / artifact：

- 必须保存 source_name_or_descriptor；
- 新书 name 不得与来源名相同；
- rename_rationale 必须说明按功能、世界术语、意象或体系风格如何重命名；
- 禁止只加“真/改/新版”等机械改名。

### 每日预算菜单审计

若 engine_type=daily_priced_random_menu：

- offer_pool ≥24；
- 每日菜单固定10项；
- 每项1—10点明码标价；
- 当天可以买多个，总花费≤10；
- 每项有数字 effect_value 与 effect_unit；
- 至少覆盖6类效果；
- 低/中/高价格带齐全；
- 至少3张阶段菜单；
- 每张菜单都说明购买组合与放弃项；
- offer_pool 至少引用4个不同 material_id；
- 商品必须有可记忆展示名，不得只写“气血控制/肉身适应/悟性”。

任何一项缺失，不得把“素材库利用充分”判为 PASS。
