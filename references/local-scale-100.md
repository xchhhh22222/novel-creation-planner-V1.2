# 前100章局部 Scale 规划 V1.5

本文件只规划**当前100章真正会使用的世界信息**。

原则：**不做世界百科。只搭当前城市/区域的冲突闭环；更大世界只允许少量势力或线索伸进来。**

## 1. 运行时机

只有用户已经确认书名、开篇、金手指之后运行：

```text
selected_story_variant
→ local_scale_1_100
→ SCALE_GATE
→ strategic targets
→ two major climaxes
→ story spine 1-100
```

SCALE_GATE 未通过，不得进入高潮倒推。

## 2. 势力：当前冲突闭环

默认只构造：

- 4—7 个当前城市/区域真正参与前100章的 active factions；
- 0—2 个更高层 external factions，只描述它们怎样“伸一只手进来”。

每个 active faction 至少回答：

```text
控制什么资源/资格/信息
当前要什么
与主角是什么关系
盟友是谁
冲突对象是谁
冲突原因是什么
最早在哪个阶段介入
```

必须输出 `faction_relations[]`，关系可用：
`ally / conditional_ally / competitor / hostile / regulator / dependency`。

至少形成一个冲突闭环，而不是几个互不相干的组织名字。

## 3. 修炼体系：先建4—6套候选池，再激活2—3套

先读取 [material-pool-expansion.md](material-pool-expansion.md)，从素材库建立4—6套 `system_candidate_pool`，再选择2—3套 active systems；允许1—2套 latent systems 只留伏笔。不要因为用户举例“武道+异能”就停止检索。

每套体系至少写：

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

体系之间必须写 `system_relations[]`，可包含：
`social_hierarchy / competition / complement / restraint / conversion / exclusivity`。

允许制造身份压迫，例如“异能觉醒者社会评价高于纯武者”，但必须来自素材结构或用户确认。

## 4. 境界：只写当前100章看得到的层级

只保存：

```text
current_revealed_realms
protagonist_start_realm
climax_1_expected_realm
climax_2_expected_realm
future_realm_hint
```

`future_realm_hint` 只需一句，不展开完整规则。

## 5. 功法 / 武技 / 法宝：只揭露当前三档

默认只设计当前可见的三档，例如：
`基础档 / 精英档 / 稀有档`。

### technique_pool

先建立6—10项候选池，再用 `active_technique_ids` 选3—5项当前真正会用的。说明：
`适配体系 / 训练方式 / 核心效果 / 限制 / 资源消耗 / 当前谁能获得 / material_refs`。

### combat_art_pool

先建立8—12项候选池，再用 `active_combat_art_ids` 选4—6项。说明：
`适配体系 / 使用场景 / 战斗功能 / 限制 / 首次可能出现阶段 / material_refs`。

### artifact_pool

先建立5—8项候选池，再用 `active_artifact_ids` 选2—4项。说明：
`适配体系 / 激活方式 / 效果 / 消耗 / 限制 / 获取入口 / material_refs`。

更高级别只写 `future_tier_hint`，不展开清单。

## 6. 普通资源：只做当前循环

前100章只列3—6种真实参与循环的资源：

```text
资源来源
谁控制
谁需要
怎么获得
怎么消耗
和金手指有什么关系
```

积分/学分/战功可以存在，但必须说明能兑换什么真实资源。

## 7. 地图：只完整设计一个城市/区域

默认：

- 3—6 个本地节点；
- 0—2 个外部节点/更高地图入口。

本地节点必须服务剧情。外部地图只写：
`name / why_it_touches_current_city / which_faction_reaches_in / future_use`。

不要提前设计全国地图。

## 8. 金手指接口

必须单独写 `golden_finger_interfaces`：

```text
它能强化什么
它不能替代什么
它怎样依赖训练/资源/任务
它怎样制造下一章期待
它怎样避免取代外部资源循环
```

例如每日随机预算类金手指，必须进一步读取 [golden-finger-menu-engine.md](golden-finger-menu-engine.md)，落成“10项菜单 + 明码标价 + 10点内多选 + 每日刷新”的可执行商品系统，而不是只列抽象强化类别。

不能每章都只靠刷新菜单做钩子，要和任务、关系、资源、危机交替。

## 9. 前100章 handoff

必须输出 `handoff_after_100`：

```text
主角当前实力
当前正式身份
已获得功法/武技/法宝
已知体系
尚未展开体系
已登场势力
只露手的外部势力
已经使用的素材
仍可调用的素材方向
未兑现伏笔
下一阶段最大问题
```

101章以后不在本次 scale 展开。

## 10. SCALE_GATE

PASS 至少要求：

- 4—7 个 active factions，并有明确盟友/冲突/依赖关系；
- 0—2 个 external factions；
- system_candidate_pool 4—6套，最终active systems 2—3套，并有 system_relations；
- 当前境界足以覆盖两个高潮；
- technique_pool 6—10，active_technique_ids 3—5；
- combat_art_pool 8—12，active_combat_art_ids 4—6；
- artifact_pool 5—8，active_artifact_ids 2—4；
- ordinary_resources 3—6 种；
- local_map_nodes 3—6 个；
- golden_finger_interfaces 完整；
- handoff_after_100 完整。

缺失时 HOLD，不得直接跳高潮。


所有功法、武技、法宝候选都必须执行原创重命名：保留来源机制，禁止直接沿用来源书专名。具体规则见 `material-pool-expansion.md`。
