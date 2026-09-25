# 每日预算金手指菜单引擎 V1.5

本文件针对“每日固定预算 + 随机商品菜单”类型金手指。

目标不是写一句“每天10点，可以买气血控制”，而是把它做成一个**可持续制造选择压力和下一章期待的游戏化发动机**。

## 1. 基础契约

默认当前方案：

```text
每日基础预算：10点
每日菜单：10项
预算不可跨日保存
菜单每日刷新
同一天可以买多个项目
当日总花费不得超过10点
商品价格明示
商品效果必须可量化或可验证
```

如果用户以后修改这些规则，以用户确认值为准。

## 2. 商品原型池

`offer_pool` 至少24项。

不是每天只有24项，而是系统从原型池中随机抽10项组成当天菜单。

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

`price` 必须为1—10整数。

`effect_value` 必须是数字，`effect_unit` 必须明确，例如：

```text
气血值
%
分钟
小时
熟练度点
恢复率%
抗性%
```

这样读者能一眼判断“值不值”。

## 3. 商品类别

候选池至少覆盖6类：

- permanent_stat：永久属性；
- cultivation_speed：修炼速度；
- comprehension：悟性/理解；
- skill_proficiency：武技熟练；
- perception：感知；
- resistance：环境/伤害抗性；
- recovery：恢复；
- resource_efficiency：药力/资源利用率；
- temporary_combat：短时战斗强化；
- special_unlock：特殊条件解锁。

不要求每类都出现，但不能24项全是“气血+X”。

## 4. 价格带

offer_pool 必须覆盖：

- 低价：1—3点；
- 中价：4—6点；
- 高价：7—10点。

同一天菜单至少各有一项低/中/高价商品。

这会产生自然选择：

```text
买一个8点稀有强化 + 一个2点小强化
vs
买3+3+4三个中小强化
vs
为了当前任务只买针对性强化
```

## 5. 每日菜单

`sample_daily_menus` 至少3张：

- 开篇期；
- 第一高潮前；
- 第二高潮前。

每张必须包含10个不同 offer_id。

同时给出一个 `purchase_example`：

```json
{
  "selected_offer_ids": ["O03", "O11", "O18"],
  "total_spend": 10,
  "why_this_choice": "为什么为了当前任务这么买",
  "sacrifice": "因此放弃了什么更诱人的选项"
}
```

`total_spend <= 10`。

## 6. 期待机制

必须明确：

```text
今日菜单出现什么
→ 主角根据今天/近期任务做取舍
→ 有些好东西买不起或买了就放弃其他组合
→ 当日/近期训练与实战验证
→ 选择正确/错误产生可见后果
→ 下一次刷新重新制造期待
```

预算即使长期保持10点，也可以通过：

- 商品池扩容；
- 稀有商品解锁；
- 更高质量同价商品；
- 新类别解锁；
- 与功法/装备/任务形成组合；

持续成长，不必一味提高每日预算。

## 7. 素材调用

金手指主体仍以已选定来源机制为核心。

但商品设计必须继续检索：

- golden_finger；
- cultivation_system 的 technique / realm / resource；
- artifact / resource_asset；
- 其它可转译为“可购买成长效果”的素材组件。

`offer_pool` 至少引用4个不同 material_id，不能24项全部由 AI 凭空写出。

## 8. 命名

商品必须有读者可记忆的展示名，而不是只有：

```text
气血控制
肉身适应
感官强化
```

允许同时保留技术描述，例如：

```text
【赤血增幅】 3点
效果：气血上限 +0.4

【悟法一刻】 4点
效果：指定功法理解效率 +35%，持续60分钟
```

以上只示范“可读格式”，不是固定名称或数值。正式内容必须结合本书境界与素材库重新生成。

## 9. GATE

PASS 至少要求：

- offer_pool ≥24；
- 每日菜单大小 = 10；
- 允许一次购买多个；
- 每个商品明码标价；
- 每个商品有量化/可验证效果；
- 覆盖至少6类；
- 覆盖低/中/高价格带；
- sample_daily_menus ≥3；
- 每张菜单10项且无重复；
- 每张有合法 purchase_example；
- 至少4个不同 material_id；
- 商品名已做新书化重命名。
