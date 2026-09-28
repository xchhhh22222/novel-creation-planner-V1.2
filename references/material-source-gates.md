# 素材来源硬门 V1.3

本文件用于阻止创造层绕过素材库临场发明核心设定。

## 1. 市场层防火墙

实时 Top10 和3本深拆只允许产生以下输出：

```text
pace_pattern
hook_pattern
emotion_pattern
goal_relay_pattern
payoff_pattern
supporting_character_pattern
opening_loop
structural_lesson
```

市场层禁止直接产生：

```text
world_premise
golden_finger
cultivation_system
faction
technique
artifact
resource_asset
strategic_target
specific_story_event
```

一句话：

> **市场榜告诉我们“怎么讲”，素材库告诉我们“拿什么讲”。**

## 1A. V1.7 顺序覆盖

V1.7 继续坚持“核心设定必须有素材来源”，但调整执行顺序：

```text
世界核心
→ 人物生态
→ 势力生态
→ 人物×势力
→ 修炼体系
→ 功法/武技/装备/资源
→ 金手指9张候选
→ 剧情层
```

因此，本文件后续 V1.3 中“世界/体系/势力/资源/金手指全部先于人物与选项板”的旧顺序，不再作为 V1.7 的执行顺序。它们的来源硬门仍然有效，只是分别在对应阶段触发。

抽卡模式与熔炉模式都不能绕过素材来源硬门。熔炉的 Top10 三书只能提供 market structural lessons。

## 2. Greenfield 必须素材支撑的核心槽位

从零开书时，进入单书选项板前至少完成：

1. `world_premise`
2. `primary_system`
3. `faction_ecology`
4. `resource_loop`
5. `golden_finger_candidates`

其中前四项用于冻结 `shared_story_core`；第五项必须提供3个真实候选。

没有真实来源时：

```text
GAP → HOLD → 等用户决定补库/换方向
```

不得用模型常识静默补齐。

## 3. 来源引用最低要求

每个素材支撑对象至少保留：

```text
material_id
module
record_id
book_id
qa_status
```

`qa_status=FAIL` 不能使用。

`HOLD` 只能作为待确认候选，不能支撑通过硬门的核心槽位。

## 4. 核心槽位允许的来源模块

| role | 允许模块 |
|---|---|
| world_premise | worldbuilding |
| primary_system | cultivation_system |
| faction_ecology | worldbuilding |
| resource_loop | worldbuilding / cultivation_system |
| golden_finger_candidates | golden_finger |
| technique | cultivation_system |
| artifact | cultivation_system |
| strategic_target | cultivation_system / worldbuilding / arc_structure / plot_mechanism |
| climax_pattern | arc_structure / plot_mechanism |

## 5. 金手指最高强度门

金手指是 V1.3 的最高优先级来源门。

每个 `golden_finger_option`：

- 必须至少1个真实素材引用；
- `DIRECT/ADAPT` 必须指出 retained_mechanism；
- `HYBRID` 至少2个真实素材引用；
- 不允许 `ORIGINAL`；
- 必须说明与共享世界/主体系/资源循环的兼容性；
- 3个选项合计至少3个不同 material_id。

不满足时：

```text
GOLDEN_FINGER_SOURCE_GATE = FAIL
```

禁止生成完整开书方案。

## 6. 世界与体系也不能“顺手原创”

`world_premise / primary_system / faction_ecology / resource_loop` 都必须先有素材来源，再允许创造层做兼容重设。

创造层可以：

- 改名；
- 重设社会接口；
- 重新组合多个组件；
- 调整限制与资源关系；
- 根据用户偏好裁剪。

创造层不能：

- 在没有任何来源组件时直接发明一个完整世界；
- 为了适配临时原创第二套体系；
- 用市场样本的具体设定替代素材库；
- 先写故事，再反向给素材贴标签。

## 7. 战略目标物与高潮

`strategic_target` 可以是创造层的新对象，但不能凭空产生。

它至少引用：

- 一个“目标本体/收益”素材；
- 一个“稀缺/控制/争夺”素材或高潮机制素材。

如果没有足够素材，保持 `GAP/HOLD`。

## 8. 明确用户授权例外

如果用户之后明确说“这次允许原创某个核心槽位”，应单独记录用户授权并把该槽位标成 `USER_OVERRIDE`。

默认 V1.3 不主动启用这个例外。


## 9. V1.6 人物来源门

当用户明确要求多女主或人物关系是卖点时，heroine 与 antagonist 从可选槽位升级为 local-scale required slots。

- heroine 优先来源 heroine_character 派生卡；人物功能记录只可补充职责，不可独立支撑完整女主；
- long-arc antagonist 优先来源 long_arc_villain 派生卡；
- 一次性Boss/竞争者可以由人物功能、战斗资产和剧情机制补充；
- 没有个体卡时标 CHARACTER_CARD_GAP，不得凭标签生成完整人物；
- 新书人物必须至少重设背景、目标、资源、关系、关键选择、结果中的三项；
- 多女主 active 角色不能全部来自同一本来源书的人物结构。

## 10. V1.7 金手指阶段门

当世界、人物、势力、体系和资源框架已经形成后，才执行 `GOLDEN_FINGER_SOURCE_GATE_V17`：

1. 从 `02_金手指` cluster/per_book 宽召回；
2. 回查 input / process / output / limits / cost / growth；
3. 检查与 selected_world_core、active systems、ordinary resources、active character interests 的接口；
4. 排除会无代价消灭中心矛盾或资源循环的机制；
5. 去重后展示 9 张候选；不足9个真实差异候选则 PARTIAL/HOLD；
6. 用户选1个或融合2个；
7. 选中结果才允许进入剧情层与最终 Local Scale。

9 张卡不得来自 AI 临场原创；HYBRID 必须保留每个来源组件与重新设计的兼容接口。
