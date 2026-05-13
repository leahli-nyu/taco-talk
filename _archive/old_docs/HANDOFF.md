# Handoff: 给下一个 Claude Code 会话

> 写于 2026-05-11 晚 / 12 日早。上下文将耗尽，新会话继续。

## 项目状态：PIPELINE 全部完成

Tariff Talk paper + app 双轨。所有 phase 跑完，paper 重写，figures ready。

## 你（新 Claude）必读 5 个文件

读取顺序：

1. **[MORNING_REPORT.md](MORNING_REPORT.md)** — 当前全状态 + 三个 finding + 用户待办
2. **[DECISIONS.md](DECISIONS.md)** — 所有锁定决策
3. **[paper/draft.md](paper/draft.md)** — paper v2，8 章节
4. **memory 系统**（自动加载）—— `~/.claude/projects/-Users-leahli-Documents-26Spring-TextasData-final-proj/memory/`
5. **此文件** — 用户上下文+协作风格

读完这 5 个，你就和上一会话同步了。

## 用户关键 context

- **NYU CDS Master's**，DS-GA 1015 Text as Data Spring 2026 final project
- **ADHD** — 协作要注意：长信息分段、不要 dump 表格、给 next-3-actions、外置 executive function
- **不是 finance / econ 专业**，但有 ML/NLP 背景
- 偏好严谨度高、honest null result 也接受、不抄袭风格
- **API budget**: $22 共，已用 ~$11，剩 ~$11
- **Deadline**: 5/12（明天），约还 24 小时

## 当前数据状态

```
6,943 帖原创 (Truth Social, 2024-11-06 至今)
  → consensus A class: 141 帖 (Claude+GPT 都说 A)
  → 110 policy episodes (bge-large 聚类)
  → 98% 匹配 PIIE timeline
  → 中位 anticipation 5 天
```

## 三个核心 finding（新 framing）

1. **TACO 市场签名是真的（描述性）**: 平均 30d peak drawdown -4.95% / recovery +3.80%
2. **Outcome 预测 NULL**: Cox PH 没有 feature p<0.05, LLM zero-shot 25-26%（比随机 33% 差）
3. **方法学贡献**: 简单方法找到 HR=8.6 但严谨方法（cross-LLM + bootstrap）显示 HR=0.93 → measurement choice matters

## 用户回来 4 件事

按优先级（用户尚未做）：

1. 看 MORNING_REPORT.md（10 分钟）— 确认 null result framing
2. 看 paper/draft.md（30 分钟）— 改 framing 措辞
3. 标注 30-60 条 [annotation/index.html](annotation/index.html)（30-60 分钟）
4. 选 design A/B/C（5 分钟）

## 关键脚本（你需要时跑）

```bash
# 重新生成 web data
python3 src/build_app_data_v2.py

# 重新生成 paper figures
python3 src/generate_paper_figures.py

# 重跑 Cox PH (慢，1000 bootstrap)
python3 src/cox_with_bootstrap.py

# 添加同学的 annotation 后算 inter-rater
# (TODO: 没写 inter-rater 计算脚本，新会话可补)
```

## 待办（如果用户要做）

- [ ] 人工 validation N=60+
- [ ] (可选) Pairwise Bradley-Terry on 4 features
- [ ] (可选) Multi-actor 扩展（Vance, Cruz, Rubio）
- [ ] (可选) Polymarket implied probabilities 对比
- [ ] Deploy to GitHub Pages
- [ ] CV / README polish

## 协作风格（记忆中规则）

- 用户 ADHD → 短段落、清晰结构、避免信息 dump
- 设计决策（research design）前 STOP 执行
- 高难度 work 放后台 + Monitor，不要 sleep loop
- 不主动 commit 到 git（除非用户要求）
- 用户给反馈时认真考虑，不全盘接受

## API keys

- `.env` 里有 ANTHROPIC_API_KEY + OPENAI_API_KEY，gitignored
- 不要 print key 内容到 transcript
- Claude Code 子进程不能直接读 env，必须显式 load `.env`（脚本里已写好）

## 当前 web preview

- 主 web: [app/index.html](app/index.html)
- 3 design 变体: [app/designs/](app/designs/)
- 标注表单: [annotation/index.html](annotation/index.html)
- design 对比 hub: [app/designs/index.html](app/designs/index.html)

## 总结一句给新 Claude

**用户 5/12 提交作业（约 24 小时）。pipeline 全部完成，只剩用户审核 + 选 design + 评分。你要做的事不多，主要是接收用户回来后的反馈、修改 paper/web 细节、回答方法学问题。** 别再大改 pipeline 除非用户明确要。
