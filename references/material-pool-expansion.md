# 素材候选池扩展与原创重命名 V1.5

V1.5 的目标不是“满足最少数量”，而是**充分扫描素材库，再从候选池中选出当前100章真正使用的部分**。

## 1. 两层结构：candidate pool 与 active set

禁止：

```text
需要3个武技
→ 搜到3个
→ 停止
```

正确：

```text
先广泛召回
→ 去重 / 回读来源 / 抽象机制
→ 形成候选池
→ 原创重命名
→ 再挑当前100章 active set
```

## 2. 体系池

`system_candidate_pool`：4—6套。

要求尽量来自至少3本不同来源书。

每项至少：

```text
candidate_id
source_system_name_or_descriptor
new_system_name
material_refs
core_mechanism
social_role
resource_dependency
conflict_value
fit_with_current_world
status = active|latent|rejected
selection_reason
```

最终：

- active systems：2—3套；
- latent systems：1—2套，可只留伏笔；
- 其余明确 rejected_reason。

用户说“加武道和异能”不等于只搜武道和异能。AI必须继续看素材库里还有哪些与当前世界兼容的体系，例如精神、古法、机械、御兽、修仙等；只有素材确实存在且兼容时才能入池。

## 3. 功法候选池

`technique_pool`：6—10项。

`active_technique_ids`：3—5项。

每项必须：

```text
item_id
source_name_or_descriptor
name
naming_style
rename_rationale
tier
system_id
training_method
core_effect
limitation
resource_cost
access
material_refs
```

### 名称规则

`name` 是新书原创名。

禁止：

```text
name == source_name_or_descriptor
```

也禁止只在原名后加“真”“改”“新版”等机械改名。

重命名依据至少包含两项：

- 新世界术语；
- 功能；
- 体系风格；
- 使用意象；
- 阶段定位。

## 4. 武技候选池

`combat_art_pool`：8—12项。

`active_combat_art_ids`：4—6项。

每项必须保留：

```text
source_name_or_descriptor
name
naming_style
rename_rationale
system_id
use_case
combat_function
limitation
first_stage
material_refs
```

武技池应覆盖不同功能，而不是十个同类攻击技。至少覆盖其中5类：

```text
爆发
身法
防御
控制
远程/投射
感知
破甲
群战
追击
撤退
环境适应
```

## 5. 法宝 / 装备候选池

`artifact_pool`：5—8项。

`active_artifact_ids`：2—4项。

至少覆盖两类：

- 普通可持续使用装备；
- 稀有/成长/剧情关键装备。

同样要求原创重命名，不直接沿用来源书专名。

## 6. 素材多样性门

候选池不能几乎全来自一本书。

最低建议：

- system_candidate_pool：≥3本来源书；
- technique_pool：≥3本来源书；
- combat_art_pool：≥3本来源书；
- artifact_pool：≥2本来源书。

同一本书可以贡献多个组件，但必须报告来源集中风险。

## 7. 输出方式

给用户审核时先展示：

1. 候选池；
2. 每个候选从哪本书抽了什么机制；
3. 新书改成什么名字；
4. 为什么适合当前世界；
5. 哪些进入 active set；
6. 哪些只是 latent/rejected。

不要只展示最后3个结果，让用户看不到素材库到底被调用了多少。
