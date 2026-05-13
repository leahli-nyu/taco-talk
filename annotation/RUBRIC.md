# Annotation Rubric · 标注指南

> 给你下午回来做的 4 个标注任务的标准。每个 packet 用同一个 rubric。  
> **核心原则**：跟着自己的直觉判断，但参考下面的 anchor。每条估计 30-60 秒。能标多少标多少。

---

## 1. Specificity 0-10 ｜ 具体度

**问的是**：这条帖把"威胁的细节"讲到多具体？（数字、日期、目标、机制）

**Anchor**（参考帖）：

- **0-1（极度模糊）**：纯抱怨/夸耀，没说要做什么。
  > 例："Trade deals are tremendous! USA WINS!"

- **2-3（笼统）**：有大方向但没细节。
  > 例："We will be tough on China. Their unfair practices must end."

- **4-5（中度）**：有 1 个具体元素（一个国家 OR 一个百分比 OR 一个日期），但其他没说。
  > 例："Tariffs on China are coming."（点名 China，没说 % 没说时间）

- **6-7（较具体）**：有 2 个具体元素。
  > 例："25% tariff on Canada starting Feb 1."

- **8-9（高度具体）**：3+ 具体元素 + 实施细节。
  > 例："25% tariff on Mexico and Canada on all goods except USMCA-compliant, effective February 4, citing IEEPA fentanyl emergency."

- **10（极致具体）**：基本可以直接写成 executive order。
  > 例：完整法律条款 + 实施细则 + 例外清单 + 执行机构。

**判断要点**：
- 只看**这条帖说了多具体**，不要预判它会不会被执行。
- 不要被 ALL CAPS 或感叹号迷惑——那是 dramatization，不是 specificity。
- 提到具体国家 ≠ specificity 高（可能只是名义提一下）。

---

## 2. A/B/C 分类 ｜ 是不是经济威胁？

**A 类**（commissive + 经济政策影响）：
- Trump **承诺会做** 一件政府能执行的事
- 这件事**直接影响经济/金融/贸易**（关税、制裁、Fed、贸易协议、商品干预、antitrust、金融监管）

**B 类**（commissive + 非经济影响）：
- Trump 承诺要做，但**主要影响是非经济**（移民、军事、司法起诉、社会文化、外交）

**C 类**（非 commissive）：
- 评论、抱怨、夸耀过去、转发别人、对他人的指令（不是自己承诺）

**判断要点**：
- "**I/We will**" → 通常 commissive
- "**China should**" → 不是 commissive（指令他人）
- "Tariffs are wonderful" → C（夸耀，非承诺）
- 边界 case：政府人员任命算 A（econ impact）还是 B（行政）？我们之前定的是**算 B**（任命本身不直接影响金融，虽然任命的人会）
- "**贸易协议**"是 A（econ）；"**国家安全战略**"通常是 B
- **conditional commitment**（"If X then I will Y"）算 A 但低 commitment_strength

---

## 3. 是否构成 commissive？ ｜ 是不是承诺？

**Yes**：
- 第一人称 + 未来动词（I will / We will / I'm going to / I plan to）
- 主语是 Trump 或他的政府，且 Trump 是 agent

**No**：
- 对别人的命令（"China must"）
- 预测他人行为（"Mexico will pay"）
- 夸耀过去（"We have done"）
- 评论现状（"Tariffs are working"）

**边界**：
- "We are signing tomorrow" → Yes（已经在执行，但仍是承诺）
- "Day One I will end the war" → Yes（条件承诺也算）
- "If Putin doesn't withdraw, we will sanction" → Yes（conditional）

---

## 4. Match 正确性 ｜ Episode 和事件配对对吗？

给你一个 episode 的文本 + 我们 cross-LLM 选的对应 PIIE 事件（target + date + status）。

判断：
- **✓ 正确**：episode 内容明显是关于这个 target/topic
- **⚠ 边缘**：topic 沾边但不是核心（比如帖讲整体贸易，被匹配到具体某个国家的贸易协议）
- **✗ 错配**：topic 完全不对（比如帖讲移民，被匹配到 tariff）

**判断要点**：
- 看 episode 的核心议题——一两句话内出现的关键词
- target 必须沾边（国家或行业）
- 不要要求"主要议题"严格对应——sub-thread 也算

---

## 5. Episode 聚类 ｜ 两个帖是同主题吗？

给你两个帖（同一对），判断：
- **同主题**：两帖都在讨论同一个 policy thread（同一个国家+同一个商品，或同一个议题的连续 update）
- **相关**：有 partial overlap 但不是同一回事
- **不同**：完全不同议题

**判断要点**：
- "同一周对 China 发的两条关税帖" → 通常同主题
- "对 China tariff" + "对 Canada tariff" → 不同（不同国家）
- "Mexico fentanyl 关税" + "Mexico water treaty" → 相关（都 Mexico 但不同 issue）
- "WIN! 经济好！" + "WIN！股市新高！" → 不同（虚 boast 不算 policy episode）

---

## 怎么标

**4 个 packet**：
- `packet_A_specificity.md` ⭐ 最重要——锚定 LLM 测量
- `packet_B_borderline_abc.md` —— 验证 A/B/C 边界
- `packet_C_match_validation.md` —— 验证 27 个 consensus 匹配
- `packet_D_clustering_pairs.md` —— 验证 episode 聚类阈值

**优先级**：A > C > B > D

**做法**：每个 packet 都是 markdown，**直接编辑文件**，在空白处填数字/字母/勾选。完了告诉我哪些填了，我来 parse。

不需要一次填完。看心情可以跳跃。
