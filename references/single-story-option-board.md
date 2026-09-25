# 单书选项板 V1.3

V1.3 不再同时设计 A/B/C 三本不同的书。

唯一正确模型是：

```text
一个共享故事核心
        ↓
3个书名候选
3个开篇候选
3个金手指候选
        ↓
用户分别选择
        ↓
冻结一个版本
        ↓
继续战略目标物与前100章高潮倒推
```

## 1. 共享故事核心

选项出现前先冻结 `shared_story_core`。三个开篇和三个金手指都必须服务同一个 core，不得偷偷改变：

- 目标赛道；
- 读者承诺；
- 主角基本身份与初始困境；
- 世界前提；
- 主修炼体系；
- 核心势力生态；
- 主要资源循环；
- 长线中心问题。

允许选项改变的是“怎么进入故事”“用哪个金手指接口”“叫什么名字”，不是把故事换成另一套世界和主线。

## 2. 三个书名候选

`title_options` 恰好3项。

每项：

```json
{
  "option_id": "TITLE:A",
  "title": "候选书名",
  "promise_focus": "标题主要承诺什么",
  "same_core_id": "CORE:001"
}
```

书名属于创造层表面包装，可以原创，不要求从素材库直接抽取。

三个书名必须对应同一故事核心，不得通过标题偷换世界、金手指或主线。

## 3. 三个开篇候选

`opening_options` 恰好3项。

每个开篇都引用同一个 `shared_core_id`，并且只能使用市场层的 `structural_lessons` 来改变：

- 第1章从哪里切；
- 冲突多快出现；
- 第一次可执行解法什么时候给；
- 第一次真实兑现在哪；
- 前3章如何接力；
- 第4—10章用什么结构循环；
- 钩子如何连续。

每项至少包含：

```json
{
  "option_id": "OPENING:A",
  "same_core_id": "CORE:001",
  "benchmark_lesson_ids": ["MK:LESSON:001"],
  "opening_pattern": "危机→解法→首次兑现",
  "chapter_1_3": [
    {
      "chapter": 1,
      "goal": "主角当章目标",
      "obstacle": "结构级阻碍",
      "payoff": "可见兑现",
      "hook": "下一章未完成问题"
    }
  ],
  "chapter_4_10_loop": "可重复结构",
  "what_stays_fixed": ["世界前提", "主角身份", "核心势力", "主体系"],
  "risk": "节奏或同质化风险"
}
```

三个开篇不是三条新故事线。它们只测试同一故事的不同入场方式。

## 4. 三个金手指候选

`golden_finger_options` 恰好3项，且全部通过素材来源门。

每项：

```json
{
  "option_id": "GF:A",
  "same_core_id": "CORE:001",
  "name_candidate": "候选名称",
  "source_mode": "DIRECT|ADAPT|HYBRID",
  "material_refs": [
    {
      "material_id": "GF:...",
      "record_id": "GF:BOOK:...",
      "book_id": "BOOK_...",
      "module": "golden_finger",
      "qa_status": "PASS"
    }
  ],
  "retained_mechanism": "从素材保留的核心运行机制",
  "adaptations": [],
  "input": "输入",
  "process": "处理",
  "output": "输出",
  "limits": [],
  "costs": [],
  "growth": "成长方式",
  "first_validation_plan": "在本书如何第一次真实验证",
  "compatibility_with_core": "为什么能接到当前世界/体系/资源",
  "risk": "风险"
}
```

### 4.1 DIRECT

直接使用素材中的核心机制，仅修改：

- 专名；
- 与新世界冲突的接口；
- 必须重设的来源包装。

不为了“显得原创”强行破坏成熟机制。

### 4.2 ADAPT

保留一个素材的核心运行逻辑，但调整限制、资源接口、验证方式、成长路线或暴露风险。

### 4.3 HYBRID

至少引用两个真实素材组件，重新设计兼容接口。

### 4.4 禁止

V1.3 默认不允许：

```text
source_mode = ORIGINAL
```

素材库没有合适候选时，正确结果是 `GAP/HOLD`，不是 AI 临场发明。

三个金手指选项合计至少覆盖3个不同的真实 `material_id`。若素材不足3个，停止选项板并报告缺口。

## 5. 用户选择门

选项板输出后必须停下等待用户。

`selection.status`：

- `pending`：用户尚未选；
- `confirmed`：用户已经分别选定书名、开篇、金手指。

pending 时：

- 不得冻结正式金手指；
- 不得生成正式 strategic_target；
- 不得生成两个大高潮；
- 不得生成前100章故事脊柱；
- 不得把某个选项偷偷当成推荐案继续写。

confirmed 后，才把三个选择合成一个 `selected_story_variant`，继续高潮倒推。

## 6. 输出顺序

V1.3 开书第一轮固定输出：

1. 市场结构 lessons；
2. 共享故事核心；
3. 3个书名；
4. 3个开篇；
5. 3个真实素材来源的金手指；
6. 每个金手指的来源与 DIRECT/ADAPT/HYBRID；
7. 等待用户选择。

不要输出“三个完整故事”。
