# V1.7 创作入口：素材抽卡与三书熔炉

V1.7 只改变“怎么开始选材”，不推翻 Planner 后半段的组装逻辑。

当前素材域固定为：

- 题材：都市高武；
- 当前素材来源：Nova 素材库；
- 当前关系默认：多女主；
- 暂不提供男频/女频频道切换，也不为尚未建立素材库的赛道制造空入口。

两种入口最终都必须汇入同一条正式规划链。

---

## 1. 总原则

```text
入口只负责确定世界核心与参考结构
→ 后续继续使用 Planner 自己的规划链
→ 所有核心组件继续从素材库召回
→ AI 不得因为 UI 需要凑数而临场发明核心素材
```

“9 张卡”是展示窗口，不是数据库上限。未来素材库扩大后，先从更大的候选池检索、去重、兼容性筛选，再向用户展示 9 张。

若当前素材库没有 9 个真正不同、证据合格的候选：

```text
PARTIAL / HOLD
```

优先于复制同义卡、把一个 cluster 改九个名字，或用模型原创凑满。

---

## 2. MODE A：素材抽卡（inspiration_draw）

### 2.1 世界观先行

从 Nova 的 `03_世界观` 开始：

```text
worldbuilding cluster
→ 回读 per_book / rule_chain / faction / resource circuit
→ 去掉同义与表面题材重复
→ 形成候选池
→ 展示 9 个世界观候选
```

每张卡至少显示：

- `candidate_id`
- 核心运行结构；
- 世界持续制造什么问题；
- 资源/资格/权限怎样流动；
- 可制造的主要冲突；
- 来源 material_id / record_id / book_id / qa_status；
- 与其它候选最关键的机制差异。

用户可执行：

- 选中 1 张；
- 融合 2 张；
- 换掉单张；
- 整批重抽；
- 明确排除某种机制。

融合不是把两段简介拼起来，必须重新设计资源、制度、势力与规则接口。

### 2.2 世界观确认门

世界未确认前：

- 不进入正式人物生态；
- 不生成正式势力图；
- 不生成正式修炼体系；
- 不生成金手指最终候选；
- 不生成高潮和 100 章脊柱。

确认后生成 `selected_world_core`，两种入口从此进入同一条 Planner 主链。

---

## 3. MODE B：三书熔炉（fusion_furnace）

熔炉复用已有 `market-benchmark.md`，不另造一套扫榜逻辑。

标准流程：

```text
都市高武同一快照 Top10
→ 合法读取前 10 章
→ 横向结构比较
→ 选出 3 本互补样本
→ 深拆前 20 章
→ structural lessons
→ 三书结构熔炉
→ 回到 Nova 素材库选择世界核心
```

### 3.1 三本书如何进入熔炉

选择理由只能来自结构学习价值，例如：

- 冲突启动速度；
- 首次兑现速度；
- 目标接力；
- 章末钩子；
- 情绪曲线；
- 4—10 章循环；
- 配角利用；
- 结构清晰度。

不因为“更像我们准备写的书”优先入选。

### 3.2 熔炉只负责“怎么讲”

生成 `market_fusion_recipe`，至少覆盖：

- pace；
- hook；
- emotion；
- goal_relay；
- payoff；
- supporting_character_usage；
- opening_loop。

可以记录三书全局参考权重，但权重只表示结构参考优先级，不表示“复制剧情百分比”。

禁止：

```text
A 剧情 50% + B 剧情 30% + C 剧情 20%
```

允许：

```text
A 主导首次兑现节奏
B 主导钩子链
C 主导目标接力与配角使用
```

### 3.3 熔炉结束后仍回素材库

市场三书不直接提供新书的：

- 世界前提；
- 男女主人物卡；
- 势力；
- 修炼体系；
- 功法/武技/装备；
- 金手指；
- 战略目标物。

熔炉完成后：

```text
market_fusion_recipe
+
Nova 03_世界观
→ 9 个世界观候选
→ 用户确认 selected_world_core
```

如果榜单中的某本书本来就已经是 Nova 正式素材来源，仍需通过素材库中的正式 record/cluster 引用它，不能用市场样本身份绕过素材 QA。

---

## 4. 两种入口合流后的正式 Planner 链

世界核心一旦确认，两种入口完全合流。顺序固定为：

```text
selected_world_core
→ 主角 + 多女主候选
→ 势力生态
→ 人物 × 势力绑定
→ 修炼体系候选池
→ 功法 / 武技 / 装备 / 普通资源
→ 金手指候选与选择
→ 情绪 / 剧情线 / 开篇 / 篇章结构 / 剧情机制
→ Local Scale 1-100
→ SCALE_GATE
→ strategic targets
→ 两个大高潮
→ 高潮倒推
→ 1-100 章故事脊柱
→ handoff_after_100
```

不得因为新增“抽卡/熔炉”入口，把后半段简化成“世界 + 金手指 → 直接生成立项”。

---

## 5. 主角、多女主与人物生态

读取：

- `05_人物功能`；
- heroine_character；
- long_arc_villain；
- relationship_engine。

主角至少确定：

- 初始身份；
- 社会位置；
- 核心欲望；
- 核心缺口；
- 当前资源；
- 与已选世界的结构性矛盾；
- 初始势力状态。

多女主仍遵守 V1.6 人物生态门。人物卡先确定独立目标、资源、边界、关键选择与关系发动机，不能先用“高冷/活泼/温柔”代替人物结构。

---

## 6. 势力生态先于人物归属

从世界观素材召回 faction / institution / resource control。

先建立：

- 4—7 个当前 active factions；
- 0—2 个 external factions；
- ally / conditional_ally / competitor / hostile / regulator / dependency 等关系；
- 每个势力控制的资源、资格、权限或信息；
- 势力之间争夺什么。

然后再建立 `faction_character_links`：

- 主角属于/依附/敌对/受管制于谁；
- 每位 active 女主属于或连接哪个势力；
- 长线反派和关键配角绑定哪个势力；
- 每个 active faction 至少有一名代表人物。

人物与势力不得分别生成后互不相干。

---

## 7. 修炼体系与表现层

势力—人物网络稳定后，才进入 `04_修炼体系`：

- system candidate 4—6 → active 2—3；
- technique 6—10 → active 3—5；
- combat art 8—12 → active 4—6；
- artifact 5—8 → active 2—4；
- ordinary resource 3—6。

所有候选必须保留素材来源并做原创重命名。

体系、功法、武技、装备和资源必须解释它们与：

- 世界规则；
- 势力控制；
- 人物身份；
- 资源竞争

之间的接口。

---

## 8. 金手指 9 张卡放在正式链中的正确位置

V1.7 仍保留“9 个金手指供用户选择”，但不在世界刚选完时盲抽。

当世界、人物、势力、体系和资源框架已经明确后：

```text
02_金手指 cluster / per_book
→ 宽召回
→ 检查世界接口
→ 检查体系接口
→ 检查资源循环
→ 检查人物利益
→ 检查是否会消灭中心矛盾
→ 去重
→ 展示 9 个金手指候选
```

用户可：

- 选 1 个；
- 融合 2 个；
- 换单张；
- 重抽；
- 排除某类机制。

若素材不足 9 个真正不同候选，则明确 PARTIAL，不允许原创凑满。

金手指只能改变效率、选择、代价或信息结构，不能无代价消灭世界的主要问题、势力资源循环和人物利益冲突。

---

## 9. 剧情层调用 01 / 06 / 07 / 08 / 09

静态世界与成长接口稳定后，再调用：

- 01 章节情绪：promise / rhythm / payoff；
- 06 剧情线：目标、阻力、选择、代价、状态变化；
- 07 开篇：前三章、4—10 章循环与 continuation driver；
- 08 篇章结构：arc boundary、pressure、turning point、after state；
- 09 剧情机制：可重复运行的 trigger → operation → decision → consequence。

这些层负责让已经搭好的世界真正“跑起来”，不得反向覆盖前面已确认的世界、人、势力和体系事实。

---

## 10. V1.7 入口状态建议

正式计划可保存：

```json
{
  "entry_mode": "inspiration_draw",
  "entry_context": {
    "domain": "urban_gaowu",
    "default_relationship_mode": "multi_heroine",
    "world_card_window": {
      "status": "confirmed",
      "window_size": 9,
      "candidate_ids": [],
      "selected_candidate_ids": [],
      "selection_mode": "single"
    },
    "golden_finger_card_window": {
      "status": "confirmed",
      "window_size": 9,
      "candidate_ids": [],
      "selected_candidate_ids": [],
      "selection_mode": "single"
    },
    "market_furnace": null
  }
}
```

熔炉模式下 `market_furnace` 至少保存：

- benchmark_id；
- selected_sample_ids（恰好 3 本）；
- structural_lesson_ids；
- fusion_recipe；
- copy_boundary。

---

## 11. 与 V0.9 cross-book clustering 的关系

V1.7 优先把 cluster 当作“方向索引”，再回读 per_book/component 做证据确认。

cluster 若仍是 candidate-only：

- 可以在当前运行明确允许 provisional use 时参与候选召回；
- 不得自动晋升 active material；
- 必须保留 run_id / cluster_id / QA / gap；
- 若当前 run 仍标 NOT_PLANNER_READY，则维持 HOLD，不得绕过运行门。

新书加入 Nova 后仍按 Nova 规则全量 recluster，Planner 不把旧 cluster ID 当永久母型。
