# 前100章人物生态与多女主硬门 V1.6

## 1. 目标

人物层不是在世界搭完后塞几个NPC。顺序是：势力与资源 → 人物候选池 → 独立目标/边界/关键选择 → 与主角的长期绑定或敌对原因 → 关系发动机 → 入场节奏 → 两个高潮中的主动作用。

人物功能记录回答角色在剧情里做什么；novel-character-card-miner 的 heroine / long_arc_villain 卡回答这个人为什么这么做、如何选择、如何变化。两者不能互相替代。

## 2. relationship_mode

必须明确 multi_heroine / single_heroine / non_romance。用户明确多女主时固定 multi_heroine，不得为了简化自动改成单女主。

## 3. 多女主候选池

multi_heroine 时：heroine_candidate_pool 4—8；active 3—4；latent 0—2；rejected 保留原因。

每项至少包含 candidate_id、source_character_descriptor、new_character_name、role_label、independent_goal、decision_pattern、resources、limits、boundaries、protagonist_binding_reason、why_cannot_swap_out、binding_break_condition、faction_id、first_entry_window、arc_1_100、status、selection_reason、differentiation_signature、material_refs。

differentiation_signature 至少包含 goal_domain、faction_domain、resource_domain、combat_role、binding_reason、conflict_mode、relationship_progression。任意两位 active 女主至少3项不同。

## 4. 多女主入场

active 女主 first_entry_window 至少分布在2个不同窗口。推荐按主线需要逐步进入，例如 1-15 / 16-35 / 36-65 / 66-100；不要求固定窗口，但禁止所有女主在前20章一次性报菜名式登场。

## 5. 反派池

antagonist_candidate_pool 3—6，active 2—4。antagonist_layer 可取 competitor / interest_enemy / long_arc / boss_disaster。候选池至少覆盖3类，active 至少覆盖2类。

每项至少包含 candidate_id、new_character_name、antagonist_layer、goal、levers、limits、plan_1_100、necessary_opposition_reason、strategy_update_rule、faction_id、status、selection_reason、material_refs。long_arc 优先引用 long_arc_villain 个体卡。

## 6. 配角与势力代表

supporting_character_pool 3—6。每个 active faction 必须在 faction_character_links 中绑定至少1名代表人物。代表人物可以是女主、反派或配角，但必须真正代表该势力的资源、立场或行动。

## 7. 关系发动机

relationship_engine_pool 4—8。每项包含 engine_id、character_ids、engine_type、mutual_need_or_conflict、recurring_plot_generation、escalation_trigger、break_condition、material_refs。

每位 active 女主至少有1条与主角的长期关系发动机；至少另有1条反派/官方/竞争者关系发动机，避免所有人物只围绕恋爱。

## 8. 来源与原创距离

来源优先级：heroine_character / long_arc_villain 个体卡 → character_function → worldbuilding faction → cultivation/combat assets → 原创适配。不得复制来源人物姓名、标志性造型、独特遭遇、台词或完整关系链。

## 9. CHARACTER_GATE

PASS 至少要求：relationship_mode 明确；multi_heroine 时4—8候选、3—4 active、0—2 latent；active 女主至少2本来源书；女主两两差异化≥3项；active 女主至少2种入场窗口；反派3—6候选、2—4 active且层级覆盖达标；配角3—6；关系发动机4—8；每位active女主有主角关系发动机；faction_character_links 覆盖全部 active faction；heroine / long_arc_villain 有个体卡来源或明确 GAP。