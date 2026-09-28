# 素材先行开书组装 V1.7

本文件定义 V1.7 的纯素材入口。它等价于 `creation-entry-modes.md` 中的 `inspiration_draw`，不再使用旧版“先凑 world/system/factions/resource/golden-finger 再生成选项板”的顺序。

## 1. 当前固定域

- 题材：都市高武；
- 素材源：Nova；
- 默认关系模式：多女主；
- 暂不提供男女频/其它赛道入口。

## 2. 第一步只做世界抽卡

```text
03_世界观 cluster
→ per_book / rule_chain / faction / resource circuit
→ 宽召回
→ 去重
→ 证据回查
→ 展示9张世界候选
```

用户可以选1张、融合2张、换单张或整批重抽。

不足9个真正不同且证据合格的候选时，输出 PARTIAL/HOLD，不允许原创凑满。

## 3. 世界确认后进入 Planner 主链

```text
selected_world_core
→ 主角 + 多女主 / 反派 / 配角
→ 势力生态
→ 人物 × 势力绑定
→ 修炼体系候选池
→ 功法 / 武技 / 装备 / 普通资源
→ 金手指9张候选
→ 用户选1个或融合2个
→ 01/06/07/08/09剧情层
→ Local Scale 1-100
→ SCALE_GATE
→ strategic targets
→ 两个大高潮
→ story spine
```

每一步都继续从素材库召回并保留来源，不允许因为使用“灵感抽卡”入口就降低来源硬门。

## 4. 金手指不是第一步

V1.7 金手指必须在世界、人物、势力、体系和资源框架明确后再筛选。这样可以检查：

- 世界接口；
- 修炼体系接口；
- 资源循环；
- 人物利益；
- 是否无代价消灭中心矛盾。

金手指候选展示窗口为9张；9不是素材库上限。

## 5. 包装层

shared_story_core 稳定后可以给书名、开篇等包装候选。旧 schema 若仍要求 `golden_finger_options`，只能映射用户已经确认的金手指机制，不得重新替用户选择。

## 6. 禁止

- AI 随机原创九个世界观凑数；
- AI 随机原创九个金手指凑数；
- 世界刚选完就跳过人物/势力/体系直接生成100章；
- 人物与势力分别生成但没有 faction_character_links；
- 功法、武技、装备脱离所属体系与资源；
- 先写剧情再反向给素材贴来源；
- candidate 自动晋升 active。
