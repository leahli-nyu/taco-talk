# Morning Report v2

> 写于 2026-05-11 晚 / 12 日早。Pipeline 全跑完。

---

## TL;DR

**Pipeline 全部完成**。最重要的发现：**之前 `lm_hedging` HR=8.6 finding 在严谨方法下不复现 → null result**。但这反而让 paper 更有学术价值。

新 paper 主轴变成 **"诚实的 null result + 方法学贡献 + 描述性 TACO 市场签名"**。

---

## ✅ 已完成（全部）

| Phase | 状态 | 关键数字 |
|---|---|---|
| A. Data 重抓 (起点 2024-11-06) | ✅ | 6,943 帖原创 |
| B. Cross-LLM 分类 | ✅ | Claude vs GPT κ=0.45，consensus A = **141 帖** |
| C. Rich features × 3 calls | ✅ | Test-retest r=0.91-0.97（极高），cross-LLM r=0.47-0.80 |
| D. Episode 聚类 (bge-large) | ✅ | 110 episodes，中位 5 天 anticipation |
| E. Event study CAR | ✅ | 主 finding: peak -4.95% / recovery +3.80% (N=118) |
| F. Cox PH + 1000 bootstrap | ✅ | **没有 feature p < 0.05**（null result）|
| G. LLM Zero-shot baseline | ✅ | Claude 25% / GPT 26%（**比随机 33% 差**）|
| H. Web app v2 数据 | ✅ | 141 帖 + episode + Cox 全注入 |
| I. Paper draft 重写 | ✅ | 8 章节，重 framing 为 null result + 方法学贡献 |
| J. 3 个 design variants | ✅ | [app/designs/](/Users/leahli/Documents/26Spring-TextasData/final_proj/app/designs/) |
| K. 双语标注表单 | ✅ | [annotation/](/Users/leahli/Documents/26Spring-TextasData/final_proj/annotation/) |

---

## 🎯 三个核心 finding

### Finding 1: TACO 市场签名是真的（描述性）

| | Value |
|---|---|
| 平均 30-day CAR | +0.4%（接近零）|
| 平均 peak drawdown | **-4.95%** |
| 平均 max recovery | **+3.80%** |
| Net drift | ~0 |

经典 TACO 路径：**先大跌、再大涨、净影响接近零**。这是 paper 的描述性核心 finding。

### Finding 2: Outcome 预测是个 NULL（诚实结果）

Cox PH 模型在 90 episodes / 41 events 上跑，没有 feature 统计显著：

| Feature | HR | 95% CI (bootstrap) | p |
|---|---|---|---|
| hedging_level | 1.24 | [0.92, 1.80] | 0.21 |
| specificity | 1.19 | [0.96, 1.56] | 0.14 |
| commitment_strength | 0.98 | [0.50, 1.65] | 0.94 |

**hedging 和 specificity 指向"加速 resolution"方向，但效应量小、不显著**。

LLM zero-shot 也做不到：Claude 25% / GPT 26% accuracy（vs 随机 33%）。

### Finding 3: 简单方法 vs 严谨方法的差异是 paper 的方法学卖点

之前用简单方法找到：**lm_hedging HR=8.6, p=0.003**
现在严谨方法（cross-LLM consensus + bootstrap）：**HR=0.93, p=0.90**

→ **methodological lesson**：单一 LLM、单一 method、不做 bootstrap 容易 inflate finding。论文 highlight 这一点。

---

## 💰 API 总花费

| 项 | 花费 |
|---|---|
| GPT classification (6943) | ~$2.10 |
| Claude classification (6943) | ~$3.50 |
| Rich features × 3 + retry | ~$1.50 |
| Translation (149 双语) | ~$0.50 |
| 3 designs (Opus + Sonnet) | ~$3.00 |
| Zero-shot baseline | ~$0.15 |
| **累计** | **~$10.75 / $22** |

剩 ~$11 给后续：可选 multi-actor 扩展、pairwise BT、Polymarket 等。

---

## 你回来要做的（按优先级）

### 🔴 必须（提交作业前）

1. **看 [paper/draft.md](paper/draft.md)** —— 确认新 framing 你能接受
2. **拍板 design 选哪个** —— A / B / C / 当前主 app
3. **30-60 条人工标注** —— 论文 limitations 章节可写"我们做了 N 条 human validation"，越多越好

### 🟡 强烈推荐

4. **paper rewrite**（你的语言+口吻润色）
5. **deploy to GitHub Pages**（5 分钟，给 web 一个公网 URL）
6. **README / CV story**（强调"双轨提交 + 跨 LLM 严谨"）

### 🟢 时间允许

7. 同学帮做 inter-rater annotation（你说可以做但不在 deadline 前）
8. Polymarket integration（外部 prediction market 对比）
9. Multi-actor 扩展（Vance + Cruz + Rubio）

---

## 关于 framing 的几个选择

新的"null result + 方法学" framing 是 honest 但偏 negative。你回来可以选：

### 选项 A: 接受 null result framing（当前）
- 最诚实
- workshop 接受率较高（学术界认可 null results with rigorous method）
- 但 viral / 流量较低

### 选项 B: 把 TACO 市场签名 elevate 成主 finding
- 描述性 finding，安全
- 重写 abstract，把市场反应放最前
- Y1 predict 部分 demote 成 secondary 结果

### 选项 C: 两手都要
- 主 finding = market signature
- 次 finding = LLM 作 measurement instrument 的 reliability framework
- 第三 = null on prediction（作为 limitation 但承认其 honesty）

**我推荐 C**。回来确认。

---

## 文件地图

```
final_proj/
├── README.md                          ← project 入口
├── MORNING_REPORT.md                  ← 本文件
├── DECISIONS.md                       ← 所有锁定决策
│
├── paper/
│   ├── draft.md                       ← 重写版 paper (8 章节)
│   └── preliminary_findings.md        ← 旧版（保留作 robustness 对比）
│
├── app/
│   ├── index.html                     ← 主 web 入口（当前迭代）
│   ├── data.json + data.js           ← 数据（v2 pipeline 输出）
│   ├── styles.css
│   ├── app.js
│   ├── DEPLOY.md                      ← GitHub Pages 部署指南
│   └── designs/                       ← 3 个设计变体
│       ├── index.html                 ← 对比 hub
│       ├── a/index.html              ← FT/Bloomberg dashboard (Opus)
│       ├── b/index.html              ← Distill.pub academic (Opus)
│       └── c/index.html              ← Pudding Q&A explainer (Sonnet)
│
├── annotation/
│   ├── index.html                    ← 双语标注表单
│   └── annotation_corpus.json        ← 149 EN+ZH 翻译
│
├── data/processed/
│   ├── consensus_a.parquet           ← 141 cross-LLM 一致的 A 类
│   ├── all_features.parquet          ← 30+ features (LLM + dict + style)
│   ├── episodes_with_outcomes_v2.parquet  ← 110 episodes + Y1
│   ├── event_study_v2.parquet        ← 118 CAR observations
│   ├── cox_v2_summary.parquet        ← Cox 系数
│   ├── cox_v2_bootstrap.parquet      ← 1000 bootstrap samples
│   ├── zero_shot_baseline.parquet    ← LLM zero-shot 对比
│   └── ...
│
├── figures/
│   ├── cox_v2_forest.png             ← Cox PH forest plot (bootstrap CIs)
│   └── (其他 eda 图)
│
└── src/
    ├── llm_classify_v2.py            ← LLM A/B/C 分类（cross-model）
    ├── rich_features.py              ← 10 features × 3 calls
    ├── episode_clustering_v2.py      ← bge-large + threshold 0.82
    ├── cox_with_bootstrap.py         ← Cox PH + 1000 bootstrap
    ├── zero_shot_baseline.py         ← LLM zero-shot 对比
    ├── build_app_data_v2.py          ← 生成 web 数据
    └── ... (其他)
```

---

## 你睡醒最高优先级 5 件事

1. **看 morning report**（这个文件）+ 接受/调整 framing
2. **看 [paper/draft.md](paper/draft.md)** 改任何不喜欢的措辞
3. **从 [app/designs/index.html](app/designs/index.html) 选一个 design**（或保留当前主版）
4. **标注 30-60 条** [annotation/index.html](annotation/index.html) (30 分钟)
5. **deploy to GitHub Pages**（5 分钟）→ 老师可点的 URL

提交作业 = 5 件事都做完。**总耗时 ~3 小时**。

剩下时间留给：你自己润色 paper + README + 投 FinNLP 准备。

🌮
