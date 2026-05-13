# 标注 packets 入口

> 5 个 packet。**所有 LLM rating / label / cosine 都已隐藏**，顺序已随机化。

## 5 个 packet 一览

| # | 任务 | 总数 | 组成 | 总耗时 |
|---|---|---|---|---|
| [A](packet_A_specificity.md) | Specificity 0-10 | **48** | 40 真 + **8 隐藏 duplicate** | ~25 min |
| [B](packet_B_borderline_abc.md) | A/B/C 分类 | 55 | 30 disagree + 25 consensus controls | ~80 min |
| [D](packet_D_clustering_pairs.md) | 聚类阈值 | **39** | 5 个 cosine bin × 8 pair | ~40 min |
| [E](packet_E_disagree_resolution.md) ⭐ | Match Task 统一 | **75** | 24 disagree + 27 consensus + 12 both-none + **12 fake** | ~110 min |

**总上限：217 items / 约 4 小时**

## 严谨设计：4 种 control

1. **Packet A duplicate**（4 个）：偷藏 duplicate 测你自己 test-retest r → 给我们 reliability ρ
2. **Packet B consensus control**（25 个）：A/B/C 一致的混进 disagree → 测你的 baseline 判断 sane
3. **Packet E consensus control**（27 个）：LLM 一致 match 的 → 测你的 baseline match precision
4. **Packet E fake control**（5 个）：把真 match 从候选列表偷拿掉，看你会不会从剩下的"硬选"一个 → 测你的 forced-choice bias

## 选项升级

Packet E 现在 3 种回答：
- `[N]` → 这个 event 最匹配
- `tie [N]/[M]` → 两个都对，难分
- `none` → 没一个合理

防止你在边界 case 硬选一个。

## 怎么标

直接编辑 `.md`，找到 `__` 填进去。例：

```markdown
**Your specificity rating (0-10)**: 6
**Notes (optional)**: 提到了 China + 100% 但没日期
```

每个 packet 独立，能填多少填多少。

## 完了告诉我

跟我说 "做完 A" / "A 一半 + C 全部 + E 全部" / etc.，我就 parse。

## RUBRIC

先读 5 分钟 [RUBRIC.md](RUBRIC.md)（5 节，对应 5 个 packet）。

---

## 影响 paper 的程度（实话）

| Packet | 必填? | 价值 |
|---|---|---|
| A | 必填 ≥15 | 写进 paper §3 measurement validity |
| C | 必填 ≥10 | 验证 §5.1 N=27 claim |
| E | 强烈推荐 | **唯一能扩 N 的 packet**，5+ resolved 就能在 paper §5.4 加一个新 spec |
| B | 可选 | 验证 §3.2 classification filter |
| D | 可选 | 验证 §3.3 episode threshold |
