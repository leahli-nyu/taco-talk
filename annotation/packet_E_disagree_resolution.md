# Packet E · Match Task（统一）

> 75 个 case：disagree + consensus + both-none + 隐藏 fake control。
> 你不知道每条属于哪种——intentional 防 priming。

选项：
- 写 `[N]` = 这个 event 最匹配
- 写 `tie [N]/[M]` = 两个都对，难分
- 写 `none` = 没一个合理匹配

**注意**：候选事件按日期排序。`Δd` = event 距首帖天数。

---

## Case 1 · Episode 32

**Episode first-post date**: 2025-03-11

**Episode first-post text** (EN):
> Despite the fact that Canada is charging the USA from 250% to 390% Tariffs on many of our farm products, Ontario just announced a 25% surcharge on “electricity,” of all things, and your not even allowed to do that. Because our Tariffs are reciprocal, we’ll just get it all back on April 2. Canada is a Tariff abuser, and always has been, but the United States is not going to be subsidizing Canada any longer. We don’t need your Cars, we don’t need your Lumber, we don’t your Energy, and very soon, you will find that out. MAKE AMERICA GREAT AGAIN!!!

**ZH 翻译**:
> 尽管加拿大对我们很多农产品征收高达250%到390%的关税（Tariff），安大略省居然还宣布要对"电力"加征25%的附加税，这种事你们根本就不被允许干！因为我们的关税是对等的，4月2日我们会把这些全部讨回来。加拿大是个关税（Tariff）剥削者，一直都是，但美国不会再补贴加拿大了！我们不需要你们的汽车，不需要你们的木材，不需要你们的能源，很快，你们就会明白这一点。**让美国再次伟大**！！！

**Candidate events in [-10d, +60d] window:**

- **[8]** `2025-03-01` Δ-10d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ-7d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+22d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+22d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+23d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+24d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+29d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+29d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+42d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+49d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+53d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 2 · Episode 98

**Episode first-post date**: 2026-01-29

**Episode first-post text** (EN):
> Based on the fact that Canada has wrongfully, illegally, and steadfastly refused to certify the Gulfstream 500, 600, 700, and 800 Jets, one of the greatest, most technologically advanced airplanes ever made, we are hereby decertifying their Bombardier Global Expresses, and all Aircraft made in Canada, until such time as Gulfstream, a Great American Company, is fully certified, as it should have been many years ago. Further, Canada is effectively prohibiting the sale of Gulfstream products in Canada through this very same certification process. If, for any reason, this situation is not immediately corrected, I am going to charge Canada a 50% Tariff on any and all Aircraft sold into the United States of America. Thank you for your attention to this matter!DONALD J. TRUMPPRESIDENT OF THE UNITED STATES OF AMERICA

**ZH 翻译**:
> 鉴于加拿大**错误地、非法地、顽固地**拒绝认证湾流500、600、700和800型喷气机——这是有史以来最伟大、技术最先进的飞机之一——我们在此宣布，取消对他们庞巴迪环球快车系列以及所有在加拿大制造的飞机的认证，直到湾流——一家**伟大的美国公司**——获得完全认证为止，这个认证早在多年前就应该完成了！此外，加拿大正是通过这套认证流程，实际上禁止了湾流产品在加拿大的销售！如果这一问题因为任何原因没有被**立即**纠正，我将对所有销往美利坚合众国的加拿大飞机征收**50%**的关税（Tariff）！感谢你们对此事的关注！

唐纳德·J·特朗普
美利坚合众国总统

**Candidate events in [-10d, +60d] window:**

- **[37]** `2026-02-02` Δ+4d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+22d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+22d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+41d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 3 · Episode 54

**Episode first-post date**: 2025-05-23

**Episode first-post text** (EN):
> The European Union, which was formed for the primary purpose of taking advantage of the United States on TRADE, has been very difficult to deal with. Their powerful Trade Barriers, Vat Taxes, ridiculous Corporate Penalties, Non-Monetary Trade Barriers, Monetary Manipulations, unfair and unjustified lawsuits against Americans Companies, and more, have led to a Trade Deficit with the U.S. of more than $250,000,000 a year, a number which is totally unacceptable. Our discussions with them are going nowhere! Therefore, I am recommending a straight 50% Tariff on the European Union, starting on June 1, 2025. There is no Tariff if the product is built or manufactured in the United States. Thank you for your attention to this matter!

**ZH 翻译**:
> 欧盟，这个**主要就是为了占美国便宜**而成立的组织，跟他们打交道简直难得要命。他们那些强势的贸易壁垒、增值税（VAT）、离谱的企业罚款、非货币性贸易壁垒、货币操纵，还有针对美国企业的那些不公平、毫无道理的诉讼，等等等等，导致美国对欧贸易逆差每年超过**两亿五千万美元**，这个数字完全不可接受！我们和他们的谈判根本毫无进展！因此，我建议从2025年6月1日起，对欧盟直接征收**50%的关税（Tariff）**。如果产品是在美国本土建造或生产的，则无需缴纳任何关税。感谢您关注此事！

**Candidate events in [-10d, +60d] window:**

- **[19]** `2025-05-30` Δ+7d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+20d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+42d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+46d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+46d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 4 · Episode 0

**Episode first-post date**: 2024-11-25

**Episode first-post text** (EN):
> As everyone is aware, thousands of people are pouring through Mexico and Canada, bringing Crime and Drugs at levels never seen before. Right now a Caravan coming from Mexico, composed of thousands of people, seems to be unstoppable in its quest to come through our currently Open Border. On January 20th, as one of my many first Executive Orders, I will sign all necessary documents to charge Mexico and Canada a 25% Tariff on ALL products coming into the United States, and its ridiculous Open Borders. This Tariff will remain in effect until such time as Drugs, in particular Fentanyl, and all Illegal Aliens stop this Invasion of our Country! Both Mexico and Canada have the absolute right and power to easily solve this long simmering problem. We hereby demand that they use this power, and until such time that they do, it is time for them to pay a very big price!

**ZH 翻译**:
> 众所周知，数千人正通过墨西哥和加拿大涌入，带来了前所未有水平的犯罪和毒品。目前一支来自墨西哥、由数千人组成的大篷车，似乎在穿过我们目前开放的边境的过程中势不可挡。在1月20日，作为我众多首批行政命令之一，我将签署所有必要文件，对所有进入美国的产品以及荒谬的开放边境向墨西哥和加拿大征收25%的关税(Tariff)，并将保持这一政策直到毒品，特别是芬太尼(Fentanyl)，和所有非法移民停止对我们国家的【这种入侵】！墨西哥和加拿大【绝对】拥有权利和力量轻易解决这个长期存在的问题。我们【明确要求】他们使用这种力量，在他们这样做之前，现在是他们付出【非常高昂代价】的时候！

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+56d | target: `general` | status: `in_effect` | note: inaugural pledge

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 5 · Episode 40

**Episode first-post date**: 2025-04-07

**Episode first-post text** (EN):
> Yesterday, China issued Retaliatory Tariffs of 34%, on top of their already record setting Tariffs, Non-Monetary Tariffs, Illegal Subsidization of companies, and massive long term Currency Manipulation, despite my warning that any country that Retaliates against the U.S. by issuing additional Tariffs, above and beyond their already existing long term Tariff abuse of our Nation, will be immediately met with new and substantially higher Tariffs, over and above those initially set. Therefore, if China does not withdraw its 34% increase above their already long term trading abuses by tomorrow, April 8th, 2025, the United States will impose ADDITIONAL Tariffs on China of 50%, effective April 9th. Additionally, all talks with China concerning their requested meetings with us will be terminated! Negotiations with other countries, which have also requested meetings, will begin taking place immediately. Thank you for your attention to this matter!

**ZH 翻译**:
> 昨天，中国对美国加征了34%的**报复性关税**，叠加在他们已经创历史纪录的关税、非货币性壁垒、对企业的非法补贴，以及长达多年的**大规模**货币操纵之上——这一切都发生在我明确警告之后！我早就说过，任何国家如果胆敢对美国采取报复行动、在其已经长期滥用的关税基础上再加码，都将**立即**迎来更高、更猛的新关税！因此，如果中国不在明天——2025年4月8日——之前撤回这34%的加税，美国将对中国**额外**再加征50%的关税，自4月9日起生效！除此之外，所有中国方面请求与我们会谈的谈判，全部**立即终止**！而其他同样请求会谈的国家，谈判将马上启动！感谢你们关注此事！

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ-5d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ-5d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ-4d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ-3d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+2d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+2d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+15d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+22d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+26d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+53d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 6 · Episode 100

**Episode first-post date**: 2026-02-02

**Episode first-post text** (EN):
> It was an Honor to speak with Prime Minister Modi, of India, this morning. He is one of my greatest friends and, a Powerful and Respected Leader of his Country. We spoke about many things, including Trade, and ending the War with Russia and Ukraine. He agreed to stop buying Russian Oil, and to buy much more from the United States and, potentially, Venezuela. This will help END THE WAR in Ukraine, which is taking place right now, with thousands of people dying each and every week! Out of friendship and respect for Prime Minister Modi and, as per his request, effective immediately, we agreed to a Trade Deal between the United States and India, whereby the United States will charge a reduced Reciprocal Tariff, lowering it from 25% to 18%. They will likewise move forward to reduce their Tariffs and Non Tariff Barriers against the United States, to ZERO. The Prime Minister also committed to "BUY AMERICAN," at a much higher level, in addition to over $500 BILLION DOLLARS of U.S. Energy, Tech

**ZH 翻译**:
> 今天早上能与印度总理莫迪通话，是我的荣幸。他是我最好的朋友之一，是他国家一位**强有力、备受尊敬**的领导人。我们谈了很多事情，包括贸易，以及结束俄乌战争。他同意停止购买俄罗斯石油，转而从美国购买更多石油，还有可能从委内瑞拉购买。这将有助于【终结】乌克兰的战争——那场战争就在眼前，每周都有成千上万的人在死去！出于对莫迪总理的友谊和尊重，也应他的请求，我们即时生效地达成了一项美印贸易协议，美国将征收降低后的对等关税（Reciprocal Tariff），从25%降至18%。印度同样也将推进把他们对美国的关税及非关税壁垒（Non Tariff Barriers）降至【零】。总理还承诺"买美国货"，采购量将大幅提升，此外还有超过**5000亿美元**的美国能源、科技、农产品、煤炭及其他众多产品。我们与印度**了不起的**关系将在未来变得更加牢固。莫迪总理和我，都是那种【把事情办成】的人——这可不是谁都能说的！感谢你们关注此事！美利坚合众国总统 唐纳德·J·特朗普

**Candidate events in [-10d, +60d] window:**

- **[38]** `2026-02-20` Δ+18d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+18d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+37d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation
- **[41]** `2026-04-02` Δ+59d | target: `metal_products_clarified` | status: `modified` | note: tier-based clarification
- **[42]** `2026-04-02` Δ+59d | target: `pharmaceuticals_patented` | status: `in_effect` | note: lower rates for EU/Japan/Korea/Switzerland (15%), UK (10%); generics exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 7 · Episode 21

**Episode first-post date**: 2025-02-13

**Episode first-post text** (EN):
> We want a level playing field for all American workers — I have instructed my Secretary of State, my Secretary of Commerce, Secretary of Treasury, and U.S. Trade Representative to do all necessary work to deliver reciprocity…

**ZH 翻译**:
> 我们希望为所有美国工人创造一个公平的竞争环境——我已经指示我的国务卿、商务卿、财政卿和美国贸易代表进行所有必要的工作来实现互惠原则(Reciprocity)……

**Candidate events in [-10d, +60d] window:**

- **[4]** `2025-02-10` Δ-3d | target: `steel_aluminum` | status: `in_effect` | note: removed exemptions
- **[5]** `2025-02-13` Δ+0d | target: `all_countries` | status: `struck_down` | note: reciprocal tariffs framework
- **[6]** `2025-02-14` Δ+1d | target: `autos` | status: `in_effect` | note: auto tariffs
- **[7]** `2025-02-25` Δ+12d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+16d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+19d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+48d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+48d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+49d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+50d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+55d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+55d | target: `China` | status: `modified` | note: retaliatory escalation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 8 · Episode 57

**Episode first-post date**: 2025-05-27

**Episode first-post text** (EN):
> Nobody has done more for Alaska than your Favorite President, DONALD J. TRUMP. However, the Biden/Harris Administration terminated MUCH of our good, JOB producing product. I am working very hard to gain it all back (and actually, MUCH MORE!), but need the support of your Political Leaders to make this happen. Without their commitment, it wonât happen. With it, Alaska will become the Economic and Job producing MIRACLE of our Country!

**ZH 翻译**:
> 没有人为阿拉斯加州做过比你最喜欢的总统唐纳德·J·特朗普更多的事情。然而，拜登/哈里斯政府终止了我们**许多**优质的、**产生就业机会的产品**。我正在非常努力地争取把它们全部夺回来（实际上，**更多得多！**），但需要你们的政治领导人的支持来实现这一点。没有他们的承诺，这不会发生。有了它，阿拉斯加州将成为我们国家的经济和就业创造**奇迹**！

**Candidate events in [-10d, +60d] window:**

- **[19]** `2025-05-30` Δ+3d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+16d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+38d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+42d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+42d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 9 · Episode 33

**Episode first-post date**: 2025-03-13

**Episode first-post text** (EN):
> The European Union, one of the most hostile and abusive taxing and tariffing authorities in the World, which was formed for the sole purpose of taking advantage of the United States, has just put a nasty 50% Tariff on Whisky. If this Tariff is not removed immediately, the U.S. will shortly place a 200% Tariff on all WINES, CHAMPAGNES, &amp; ALCOHOLIC PRODUCTS COMING OUT OF FRANCE AND OTHER E.U. REPRESENTED COUNTRIES. This will be great for the Wine and Champagne businesses in the U.S.

**ZH 翻译**:
> 欧盟，这个世界上最敌对、最无耻的征税和关税机构，它成立的唯一目的就是占美国的便宜，刚刚对威士忌征收了恶毒的50%关税。如果这个关税不立即取消，美国很快将对所有来自法国及其他欧盟成员国的**葡萄酒、香槟及酒精产品**征收200%的关税！这对美国的葡萄酒和香槟行业来说将是一件大好事！

**Candidate events in [-10d, +60d] window:**

- **[9]** `2025-03-04` Δ-9d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+20d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+20d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+21d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+22d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+27d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+27d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+40d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+47d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+51d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 10 · Episode 97

**Episode first-post date**: 2026-01-26

**Episode first-post text** (EN):
> Our Trade Deals are very important to America. In each of these Deals, we have acted swiftly to reduce our TARIFFS in line with the Transaction agreed to. We, of course, expect our Trading Partners to do the same.  South Korea's Legislature is not living up to its Deal with the United States. President Lee and I reached a Great Deal for both Countries on July 30, 2025, and we reaffirmed these terms while I was in Korea on October 29, 2025. Why hasn't the Korean Legislature approved it? Because the Korean Legislature hasn't enacted our Historic Trade Agreement, which is their prerogative, I am hereby increasing South Korean TARIFFS on Autos, Lumber, Pharma, and all other Reciprocal TARIFFS, from 15% to 25%. Thank you for your attention to this matter! DONALD J. TRUMPPRESIDENT OF THE UNITED STATES OF AMERICA

**ZH 翻译**:
> 我们的贸易协议对美国来说非常重要。在每一项协议中，我们都迅速行动，按照达成的交易降低了我们的**关税（TARIFFS）**。我们当然也期待我们的贸易伙伴照做。韩国议会没有履行与美国的协议。李总统和我于2025年7月30日为两国达成了一项【伟大的协议】，2025年10月29日我在韩国期间，我们再次确认了这些条款。韩国议会为什么还没批准？因为韩国议会没有通过我们这项【历史性贸易协定】——这是他们的权力——我在此宣布，将韩国汽车、木材、制药以及所有其他对等**关税（Reciprocal TARIFFS）**，从15%上调至25%。感谢你们关注此事！唐纳德·J·特朗普美利坚合众国总统

**Candidate events in [-10d, +60d] window:**

- **[36]** `2026-01-17` Δ-9d | target: `8_european_countries` | status: `withdrawn` | note: Greenland Crisis; retracted Jan 21
- **[37]** `2026-02-02` Δ+7d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+25d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+25d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+44d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 11 · Episode 35

**Episode first-post date**: 2025-03-24

**Episode first-post text** (EN):
> President Donald J. Trump announced today that the United States of America will be putting what is known as a Secondary Tariff on the Country of Venezuela, for numerous reasons, including the fact that Venezuela has purposefully and deceitfully sent to the United States, undercover, tens of thousands of high level, and other, criminals, many of whom are murderers and people of a very violent nature. Among the gangs they sent to the United States, is Tren de Aragua, which has been given the designation of âForeign Terrorist Organization.â We are in the process of returning them to Venezuela â It is a big task! In addition, Venezuela has been very hostile to the United States and the Freedoms which we espouse. Therefore, any Country that purchases Oil and/or Gas from Venezuela will be forced to pay a Tariff of 25% to the United States on any Trade they do with our Country. All documentation will be signed and registered, and the Tariff will take place on April 2nd, 2025, LIBERATIO

**ZH 翻译**:
> 唐纳德·J·特朗普总统今天宣布，美利坚合众国将对委内瑞拉这个国家征收所谓的二级关税（Secondary Tariff），原因有很多，其中包括一个事实：委内瑞拉【故意且欺骗性地】秘密向美国输送了数以万计的高级罪犯以及其他各类罪犯，其中许多人是杀人犯，是极其暴力的危险人物。他们送到美国来的黑帮当中，就有阿拉瓜列车帮（Tren de Aragua），该组织已被认定为"境外恐怖组织"。我们正在把他们遣返委内瑞拉——这是个【大工程】！此外，委内瑞拉长期以来对美国以及我们所捍卫的自由抱有极大的敌意。因此，任何从委内瑞拉购买石油和/或天然气的国家，在与我国进行任何贸易往来时，都将被强制缴纳25%的关税（Tariff）。所有文件将完成签署并登记备案，该关税将于2025年4月2日正式生效——**美国解放日（LIBERATION DAY IN AMERICA）**！请以此通告正式知会国土安全部、边境巡逻队以及我国境内所有执法机构。感谢您对此事的关注！

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ+9d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+9d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+10d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+11d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+16d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+16d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+29d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+36d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+40d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 12 · Episode 58

**Episode first-post date**: 2025-06-01

**Episode first-post text** (EN):
> With the help of Patriots like you, we're going to produce our own metal, unleash our own energy, secure our own future, build our Country, control our destiny and we are once again going to put Pennsylvania steel into the backbone of America like never before!

**ZH 翻译**:
> 在像你这样的爱国者的帮助下，我们将生产自己的金属，释放自己的能源，保护自己的未来，建设我们的国家，控制我们的命运，我们将再次把宾夕法尼亚州的钢铁放入美国的脊梁中，**像从未有过的那样**！

**Candidate events in [-10d, +60d] window:**

- **[19]** `2025-05-30` Δ-2d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+11d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+33d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+37d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+37d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+59d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 13 · Episode 78

**Episode first-post date**: 2025-09-25

**Episode first-post text** (EN):
> Starting October 1st, 2025, we will be imposing a 100% Tariff on any branded or patented Pharmaceutical Product, unless a Company IS BUILDING their Pharmaceutical Manufacturing Plant in America. "IS BUILDING" will be defined as, "breaking ground" and/or "under construction." There will, therefore, be no Tariff on these Pharmaceutical Products if construction has started. Thank you for your attention to this matter!

**ZH 翻译**:
> 从2025年10月1日起，我们将对所有品牌或专利药品征收**100%**的关税（Tariff）——除非某家公司**正在美国境内建设**他们的制药生产工厂。"**正在建设**"的定义是：已经"破土动工"和/或"正在施工"。因此，只要建设已经启动，这些药品就**不会**被征收关税！感谢你们关注此事！

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ+5d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ+5d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+6d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+15d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+35d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+50d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 14 · Episode 71

**Episode first-post date**: 2025-07-30

**Episode first-post text** (EN):
> We are very busy in the White House today working on Trade Deals. I have spoken to the Leaders of many Countries, all of whom want to make the United States "extremely happy." I will be meeting with the South Korean Trade Delegation this afternoon. South Korea is right now at a 25% Tariff, but they have an offer to buy down those Tariffs. I will be interested in hearing what that offer is.We have just concluded a Deal with the Country of Pakistan, whereby Pakistan and the United States will work together on developing their massive Oil Reserves. We are in the process of choosing the Oil Company that will lead this Partnership. Who knows, maybe they'll be selling Oil to India some day!Likewise, other Countries are making offers for a Tariff reduction. All of this will help reduce our Trade Deficit in a very major way. A full report will be released at the appropriate time. Thank you for your attention to this matter. MAKE AMERICA GREAT AGAIN!

**ZH 翻译**:
> 今天白宫里我们忙得不可开交，全力处理贸易协议。我已经和很多国家的领导人通过话，他们全都想让美国"极度满意"。今天下午我将会见韩国贸易代表团。韩国现在面临25%的关税（Tariff），但他们提出了一个压低这些关税的方案。我很期待听听他们到底开出什么条件。我们刚刚和巴基斯坦敲定了一笔协议，巴基斯坦将与美国携手开发他们**巨量的**石油储备。我们正在筛选将主导这一合作的石油公司。谁知道呢，也许有一天他们会把石油卖给印度！同样地，其他国家也在纷纷开价争取降低关税。这一切都将以**极其重大的**方式帮助我们压缩贸易逆差。完整报告将在适当时机对外发布。感谢大家关注此事。【让美国再次伟大】！

**Candidate events in [-10d, +60d] window:**

- **[24]** `2025-07-30` Δ+0d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+20d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+28d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 15 · Episode 50

**Episode first-post date**: 2025-05-11

**Episode first-post text** (EN):
> I am very proud of the strong and unwaveringly powerful leadership of India and Pakistan for having the strength, wisdom, and fortitude to fully know and understand that it was time to stop the current aggression that could have lead to to the death and destruction of so many, and so much. Millions of good and innocent people could have died! Your legacy is greatly enhanced by your brave actions. I am proud that the USA was able to help you arrive at this historic and heroic decision. While not even discussed, I am going to increase trade, substantially, with both of these great Nations. Additionally, I will work with you both to see if, after a âthousand years,â a solution can be arrived at concerning Kashmir. God Bless the leadership of India and Pakistan on a job well done!!!

**ZH 翻译**:
> 我为印度和巴基斯坦的强大和【坚定不移】的强势领导力感到非常骄傲，他们拥有力量、智慧和决心来充分认知和理解，现在是时候停止当前的侵略行为了，这些行为本可能导致许多人和许多东西的死亡和毁灭。数百万善良无辜的人民本可能丧生！你们的遗产因你们的勇敢行动而大大提升。我为美国能够帮助你们做出这个历史性和英勇的决定而感到骄傲。虽然甚至没有讨论过，但我打算与这两个伟大的国家大幅**增加贸易**。此外，我将与你们两国合作，看看是否在"一千年"后，能够就克什米尔问题找到一个解决方案。祝福印度和巴基斯坦领导层工作出色!!!

**Candidate events in [-10d, +60d] window:**

- **[18]** `2025-05-03` Δ-8d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+19d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+32d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+54d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+58d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+58d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 16 · Episode 96

**Episode first-post date**: 2026-01-24

**Episode first-post text** (EN):
> If Governor Carney thinks he is going to make Canada a "Drop Off Port" for China to send goods and products into the United States, he is sorely mistaken. China will eat Canada alive, completely devour it, including the destruction of their businesses, social fabric, and general way of life. If Canada makes a  deal with China, it will immediately be hit with a 100% Tariff against all Canadian goods and products coming into the U.S.A. Thank you for your attention to this matter!President DJThttps://justthenews.com/government/diplomacy/deal-devil-canada-tries-trade-us-partnership-chinese-business/

**ZH 翻译**:
> 如果卡尼省长以为他能把加拿大变成中国向美国输送商品和产品的"中转港"，他就**大错特错**了。中国会把加拿大**活生生吞掉**，彻底吃干抹净，包括摧毁他们的企业、社会结构和整体生活方式。如果加拿大和中国达成协议，将**立即**对所有进入美国的加拿大商品和产品征收**100%的关税（Tariff）**！感谢您关注此事！总统 DJT https://justthenews.com/government/diplomacy/deal-devil-canada-tries-trade-us-partnership-chinese-business/

**Candidate events in [-10d, +60d] window:**

- **[35]** `2026-01-14` Δ-10d | target: `semiconductors` | status: `in_effect` | note: advanced computing chips
- **[36]** `2026-01-17` Δ-7d | target: `8_european_countries` | status: `withdrawn` | note: Greenland Crisis; retracted Jan 21
- **[37]** `2026-02-02` Δ+9d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+27d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+27d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+46d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 17 · Episode 34

**Episode first-post date**: 2025-03-17

**Episode first-post text** (EN):
> After years of being held captive by Environmental Extremists, Lunatics, Radicals, and Thugs, allowing other Countries, in particular China, to gain tremendous Economic advantage over us by opening up hundreds of all Coal Fire Power Plants, I am authorizing my Administration to immediately begin producing Energy with BEAUTIFUL, CLEAN COAL.

**ZH 翻译**:
> 经过多年被环境极端分子、疯子、激进分子和暴徒所控制，允许其他国家，特别是中国，通过开设数百家煤炭火力发电厂而获得对我们的巨大经济优势，我授权我的政府立即开始用**美丽、清洁的煤炭**生产能源。

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ+16d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+16d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+17d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+18d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+23d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+23d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+36d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+43d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+47d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 18 · Episode 27

**Episode first-post date**: 2025-03-03

**Episode first-post text** (EN):
> To the Great Farmers of the United States: Get ready to start making a lot of agricultural product to be sold INSIDE of the United States. Tariffs will go on external product on April 2nd. Have fun!

**ZH 翻译**:
> 致全美伟大的农民们：准备好大干一场吧，你们生产的农产品将在美国**国内**销售！关税（Tariff）将于4月2日对外国产品正式开征。好好享受吧！

**Candidate events in [-10d, +60d] window:**

- **[7]** `2025-02-25` Δ-6d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ-2d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+1d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+30d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+30d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+31d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+32d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+37d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+37d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+50d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+57d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 19 · Episode 83

**Episode first-post date**: 2025-10-14

**Episode first-post text** (EN):
> I believe that China purposefully not buying our Soybeans, and causing difficulty for our Soybean Farmers, is an Economically Hostile Act. We are considering terminating business with China having to do with Cooking Oil, and other elements of Trade, as retribution. As an example, we can easily produce Cooking Oil ourselves, we don't need to purchase it from China.

**ZH 翻译**:
> 我相信中国故意不购买我们的大豆，对我们的大豆农民造成困难，这是一种【经济上的】敌对行为。我们正在考虑终止与中国在食用油(Cooking Oil)和其他贸易要素方面的业务往来，作为报复。例如，我们完全可以自己生产食用油(Cooking Oil)，我们不需要从中国购买。

**Candidate events in [-10d, +60d] window:**

- **[30]** `2025-10-10` Δ-4d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+16d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[33]** `2025-12-01` Δ+48d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 20 · Episode 84

**Episode first-post date**: 2025-10-24

**Episode first-post text** (EN):
> The Ronald Reagan Foundation has just announced that Canada has fraudulently used an advertisement, which is FAKE, featuring Ronald Reagan speaking negatively about Tariffs. The ad was for $75,000. They only did this to interfere with the decision of the U.S. Supreme Court, and other courts. TARIFFS ARE VERY IMPORTANT TO THE NATIONAL SECURITY, AND ECONOMY, OF THE U.S.A. Based on their egregious behavior, ALL TRADE NEGOTIATIONS WITH CANADA ARE HEREBY TERMINATED. Thank you for your attention to this matter! President DJT

**ZH 翻译**:
> Ronald Reagan基金会刚刚宣布，加拿大欺诈性地使用了一则**虚假**广告，其中Ronald Reagan对Tariffs进行了负面评论。该广告耗资75,000美元。他们这样做仅仅是为了干扰美国最高法院和其他法院的决定。**TARIFFS对美国的国家安全和经济至关重要**。基于他们的严重不当行为，与加拿大的**所有贸易谈判均已终止**。感谢您对此事的关注！总统 DJT

**Candidate events in [-10d, +60d] window:**

- **[31]** `2025-10-30` Δ+6d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+21d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits
- **[33]** `2025-12-01` Δ+38d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 21 · Episode 49

**Episode first-post date**: 2025-05-08

**Episode first-post text** (EN):
> Today is an incredible day for America as we deliver our first Fair, Open, and Reciprocal Trade Deal â Something our past Presidents never cared about. Together with our strong Ally, the United Kingdom, we have reached the first, historic Trade Deal since Liberation Day. As part of this Deal, America will raise $6 BILLION DOLLARS in External Revenue from 10% Tariffs, $5 BILLION DOLLARS in new Export Opportunities for our Great Ranchers, Farmers, and Producers, and enhance the National Security of both the U.S. and the UK through the creation of an Aluminum and Steel Trading Zone, and a secure Pharmaceutical Supply Chain. This Deal shows that if you respect America, and bring serious proposals to the table, America is OPEN FOR BUSINESS. Many more to come â STAY TUNED!

**ZH 翻译**:
> 今天对美国来说是【无比辉煌】的一天，因为我们达成了第一份公平、开放、对等的贸易协议——这是我们过去那些总统根本不在乎的事！和我们强大的盟友英国携手，我们在"解放日"之后达成了第一份具有历史意义的贸易协议。作为协议的一部分，美国将从10%关税（Tariffs）中获得**60亿美元**的外部收入，为我们伟大的牧场主、农民和生产商创造**50亿美元**的出口新机遇，同时通过建立铝钢贸易区（Aluminum and Steel Trading Zone）以及安全的药品供应链（Pharmaceutical Supply Chain），全面强化美国和英国的国家安全！这份协议说明了一件事——只要你尊重美国，带着诚意来谈，美国就**对外开放、欢迎合作**！后面还有更多——**敬请期待！**

**Candidate events in [-10d, +60d] window:**

- **[17]** `2025-04-29` Δ-9d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ-5d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+22d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+35d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+57d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 22 · Episode 49

**Episode first-post date**: 2025-05-08

**Episode first-post text** (EN):
> Today is an incredible day for America as we deliver our first Fair, Open, and Reciprocal Trade Deal â Something our past Presidents never cared about. Together with our strong Ally, the United Kingdom, we have reached the first, historic Trade Deal since Liberation Day. As part of this Deal, America will raise $6 BILLION DOLLARS in External Revenue from 10% Tariffs, $5 BILLION DOLLARS in new Export Opportunities for our Great Ranchers, Farmers, and Producers, and enhance the National Security of both the U.S. and the UK through the creation of an Aluminum and Steel Trading Zone, and a secure Pharmaceutical Supply Chain. This Deal shows that if you respect America, and bring serious proposals to the table, America is OPEN FOR BUSINESS. Many more to come â STAY TUNED!

**ZH 翻译**:
> 今天对美国来说是【无比辉煌】的一天，因为我们达成了第一份公平、开放、对等的贸易协议——这是我们过去那些总统根本不在乎的事！和我们强大的盟友英国携手，我们在"解放日"之后达成了第一份具有历史意义的贸易协议。作为协议的一部分，美国将从10%关税（Tariffs）中获得**60亿美元**的外部收入，为我们伟大的牧场主、农民和生产商创造**50亿美元**的出口新机遇，同时通过建立铝钢贸易区（Aluminum and Steel Trading Zone）以及安全的药品供应链（Pharmaceutical Supply Chain），全面强化美国和英国的国家安全！这份协议说明了一件事——只要你尊重美国，带着诚意来谈，美国就**对外开放、欢迎合作**！后面还有更多——**敬请期待！**

**Candidate events in [-10d, +60d] window:**

- **[17]** `2025-04-29` Δ-9d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ-5d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[20]** `2025-06-12` Δ+35d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+57d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 23 · Episode 68

**Episode first-post date**: 2025-07-22

**Episode first-post text** (EN):
> President Ferdinand Marcos, of the Philippines, is just leaving the White House, with all of his many Representatives. It was a beautiful visit, and we concluded our Trade Deal, whereby The Philippines is going OPEN MARKET with the United States, and ZERO Tariffs. The Philippines will pay a 19% Tariff. In addition, we will work together Militarily. It was a Great Honor to be with the President. He is Highly Respected in his Country, as he should be. He is also a very good, and tough, negotiator. We extend our warmest regards to the wonderful people of The Philippines!

**ZH 翻译**:
> 菲律宾总统费迪南德·马科斯，带着他所有的众多代表，刚刚离开白宫。这是一次**美好**的访问，我们完成了贸易协议，根据该协议，菲律宾将对美国实行【开放市场】，关税（Tariff）为零！菲律宾将支付19%的关税。此外，我们将在军事上携手合作。能与这位总统会面是莫大的荣耀！他在自己的国家受到【高度尊重】，这是理所应当的。他也是一位非常出色、非常强硬的谈判者。我们向菲律宾的**伟大人民**致以最热烈的问候！

**Candidate events in [-10d, +60d] window:**

- **[24]** `2025-07-30` Δ+8d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+28d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+36d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 24 · Episode 66

**Episode first-post date**: 2025-07-10

**Episode first-post text** (EN):
> I am announcing a 50% TARIFF on Copper, effective August 1, 2025, after receiving a robust NATIONAL SECURITY ASSESSMENT. Copper is necessary for Semiconductors, Aircraft, Ships, Ammunition, Data Centers, Lithium-ion Batteries, Radar Systems, Missile Defense Systems, and even, Hypersonic Weapons, of which we are building many. Copper is the second most used material by the Department of Defense! Why did our foolish (and SLEEPY!) âLeadersâ decimate this important Industry? This 50% TARIFF will reverse the Biden Administrationâs thoughtless behavior, and stupidity. America will, once again, build a DOMINANT Copper Industry. THIS IS, AFTER ALL, OUR GOLDEN AGE!

**ZH 翻译**:
> 我宣布，自2025年8月1日起，对铜征收50%的**关税**（TARIFF），这一决定是在收到一份分量十足的**国家安全评估**报告后作出的。铜是半导体、飞机、舰船、弹药、数据中心、锂离子电池、雷达系统、导弹防御系统，乃至——我们正在大量建造的——高超音速武器所必不可少的材料。铜是国防部使用量**第二大**的材料！那些愚蠢（而且**【昏昏欲睡】**！）的所谓"领导人"，为什么要把这个重要产业搞得一塌糊涂？这50%的**关税**（TARIFF）将扭转拜登政府那鲁莽、愚蠢的行为。美国将再次建立起一个**【强大无比】**的铜业！毕竟，这是我们的**【黄金时代】**！

**Candidate events in [-10d, +60d] window:**

- **[21]** `2025-07-04` Δ-6d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ-2d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ-2d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+20d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+40d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+48d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 25 · Episode 66

**Episode first-post date**: 2025-07-10

**Episode first-post text** (EN):
> I am announcing a 50% TARIFF on Copper, effective August 1, 2025, after receiving a robust NATIONAL SECURITY ASSESSMENT. Copper is necessary for Semiconductors, Aircraft, Ships, Ammunition, Data Centers, Lithium-ion Batteries, Radar Systems, Missile Defense Systems, and even, Hypersonic Weapons, of which we are building many. Copper is the second most used material by the Department of Defense! Why did our foolish (and SLEEPY!) âLeadersâ decimate this important Industry? This 50% TARIFF will reverse the Biden Administrationâs thoughtless behavior, and stupidity. America will, once again, build a DOMINANT Copper Industry. THIS IS, AFTER ALL, OUR GOLDEN AGE!

**ZH 翻译**:
> 我宣布，自2025年8月1日起，对铜征收50%的**关税**（TARIFF），这一决定是在收到一份分量十足的**国家安全评估**报告后作出的。铜是半导体、飞机、舰船、弹药、数据中心、锂离子电池、雷达系统、导弹防御系统，乃至——我们正在大量建造的——高超音速武器所必不可少的材料。铜是国防部使用量**第二大**的材料！那些愚蠢（而且**【昏昏欲睡】**！）的所谓"领导人"，为什么要把这个重要产业搞得一塌糊涂？这50%的**关税**（TARIFF）将扭转拜登政府那鲁莽、愚蠢的行为。美国将再次建立起一个**【强大无比】**的铜业！毕竟，这是我们的**【黄金时代】**！

**Candidate events in [-10d, +60d] window:**

- **[21]** `2025-07-04` Δ-6d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[23]** `2025-07-08` Δ-2d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+20d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+40d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+48d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 26 · Episode 24

**Episode first-post date**: 2025-02-25

**Episode first-post text** (EN):
> Like our Steel and Aluminum Industries, our Great American Copper Industry has been decimated by global actors attacking our domestic production. To build back our Copper Industry, I have requested my Secretary of Commerce and USTR to study Copper Imports, and end Unfair Trade putting Americans out of work. Tariffs will help build back our American Copper Industry, and strengthen our National Defense. American Industries depend on Copper, and it should be MADE IN AMERICA - No exemptions, no exceptions! America First creates American jobs, and protects our National Security. It’s time for Copper to “come home.”

**ZH 翻译**:
> 就像我们的钢铁和铝业一样，我们**伟大的美国铜业**已经被那些攻击我们国内生产的全球势力**彻底摧毁**了。为了重建我们的铜业，我已经要求商务部长和美国贸易代表对铜进口展开调查，终结那些让美国人失业的不公平贸易！关税（Tariff）将帮助重建我们的美国铜业，并增强我们的国家防御能力！美国工业依赖铜，而铜就应该**在美国制造（MADE IN AMERICA）** — 没有豁免，没有例外！美国优先创造美国就业岗位，保护我们的国家安全。是时候让铜"回家"了！

**Candidate events in [-10d, +60d] window:**

- **[8]** `2025-03-01` Δ+4d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+7d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+36d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+36d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+37d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+38d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+43d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+43d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+56d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 27 · Episode 39

**Episode first-post date**: 2025-04-06

**Episode first-post text** (EN):
> We have massive Financial Deficits with China, the European Union, and many others. The only way this problem can be cured is with TARIFFS, which are now bringing Tens of Billions of Dollars into the U.S.A. They are already in effect, and a beautiful thing to behold. The Surplus with these Countries has grown during the âPresidencyâ of Sleepy Joe Biden. We are going to reverse it, and reverse it QUICKLY. Some day people will realize that Tariffs, for the United States of America, are a very beautiful thing!

**ZH 翻译**:
> 我们和中国、欧盟还有很多其他国家之间存在**巨额**贸易逆差。解决这个问题的唯一办法就是关税（Tariffs）——它现在已经给美国带来了数百亿美元！它们已经生效了，简直美不胜收。在"瞌睡乔"拜登的"总统任期"里，这些国家对我们的顺差一直在增长。我们要把它扭转过来，而且要【迅速】扭转！总有一天，人们会明白，关税（Tariffs）对美利坚合众国来说，是一件非常美妙的事！

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ-4d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ-4d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ-3d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ-2d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+3d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+3d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+16d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+23d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+27d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+54d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 28 · Episode 94

**Episode first-post date**: 2026-01-17

**Episode first-post text** (EN):
> We have subsidized Denmark, and all of the Countries of the European Union, and others, for many years by not charging them Tariffs, or any other forms of remuneration. Now, after Centuries, it is time for Denmark to give back — World Peace is at stake! China and Russia want Greenland, and there is not a thing that Denmark can do about it. They currently have two dogsleds as protection, one added recently. Only the United States of America, under PRESIDENT DONALD J. TRUMP, can play in this game, and very successfully, at that! Nobody will touch this sacred piece of Land, especially since the National Security of the United States, and the World at large, is at stake. On top of everything else, Denmark, Norway, Sweden, France, Germany, The United Kingdom, The Netherlands, and Finland have journeyed to Greenland, for purposes unknown. This is a very dangerous situation for the Safety, Security, and Survival of our Planet. These Countries, who are playing this very dangerous game, have pu

**ZH 翻译**:
> 多年来，我们一直在补贴丹麦、欧盟所有国家以及其他国家——不向他们征收关税(Tariff)，也没有收取任何其他形式的报酬。现在，经过几个世纪之后，是时候让丹麦回报了——世界和平岌岌可危！中国和俄罗斯都盯着格陵兰，丹麦根本拿他们没辙。他们现在就靠两架狗拉雪橇来保护，其中一架还是最近才加的。只有美利坚合众国，在**唐纳德·J·特朗普总统**的领导下，才能参与这场博弈，而且还能玩得非常漂亮！没有人敢动这片神圣的土地，尤其是美国的国家安全以及整个世界的安全都押在这上面。更重要的是，丹麦、挪威、瑞典、法国、德国、英国、荷兰和芬兰已经跑去格陵兰了，目的不明。这对我们星球的安全、保障和生存来说是一个**极其危险**的局面。这些国家正在玩一个非常危险的游戏，把风险推到了一个根本站不住脚、也不可持续的地步。因此，为了保护全球和平与安全，必须采取强硬措施，让这个潜在的危险局面尽快、毫无疑问地结束！从2026年2月1日起，上述所有国家（丹麦、挪威、瑞典、法国、德国、英国、荷兰和芬兰）向美利坚合众国出口的一切商品，都将被征收10%的关税(Tariff)！到2026年6月1日，关税将提高到25%！这个关税会一直收下去，直到达成一项关于**完整、彻底**收购格陵兰的协议为止。美国为这笔交易已经努力了超过150年了。很多总统都试过，理由充分，但丹麦一直拒绝。现在，由于黄金穹顶(Golden Dome)以及现代武器系统——无论是进攻性的还是防御性的——【收购】的必要性变得尤为重要。数千亿美元的

**Candidate events in [-10d, +60d] window:**

- **[35]** `2026-01-14` Δ-3d | target: `semiconductors` | status: `in_effect` | note: advanced computing chips
- **[37]** `2026-02-02` Δ+16d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+34d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+34d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+53d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 29 · Episode 77

**Episode first-post date**: 2025-09-25

**Episode first-post text** (EN):
> We will be imposing a 50% Tariff on all Kitchen Cabinets, Bathroom Vanities, and associated products, starting October 1st, 2025. Additionally, we will be charging a 30% Tariff on Upholstered Furniture. The reason for this is the large scale "FLOODING" of these products into the United States by other outside Countries. It is a very unfair practice, but we must protect, for National Security and other reasons, our Manufacturing process. Thank you for your attention to this matter!

**ZH 翻译**:
> 从2025年10月1日起，我们将对所有厨柜、浴室梳妆台及相关产品征收50%的关税（Tariff）！此外，软垫家具将被征收30%的关税（Tariff）！原因是其他国家正在大规模【"洪水式"倾销】这些产品进入美国市场。这是一种极其不公平的做法，但为了国家安全以及其他原因，我们必须保护我们自己的制造业！感谢大家关注这件事！

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ+5d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ+5d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+6d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+15d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+35d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+50d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 30 · Episode 25

**Episode first-post date**: 2025-02-27

**Episode first-post text** (EN):
> Drugs are still pouring into our Country from Mexico and Canada at  very high and unacceptable levels. A large percentage of these Drugs, much of them in the form of Fentanyl, are made in, and supplied by, China. More than 100,000 people died last year due to the distribution of these dangerous and highly addictive POISONS. Millions of people have died over the last two decades. The families of the victims are devastated and, in many instances, virtually destroyed. We cannot allow this scourge to continue to harm the USA, and therefore, until it stops, or is seriously limited, the proposed TARIFFS scheduled to go into effect on MARCH FOURTH will, indeed, go into effect, as scheduled. China will likewise be charged an additional 10% Tariff on that date. The April Second Reciprocal Tariff date will remain in full force and effect. Thank you for your attention to this matter. GOD BLESS AMERICA!

**ZH 翻译**:
> 毒品仍在以【极高且不可接受】的水平从墨西哥和加拿大大量涌入我们国家。这些毒品中有很大一部分，很多是以芬太尼（Fentanyl）的形式，由中国制造并供应。去年，超过10万人因这些危险且【极具成瘾性】的**毒药**的流通而死亡。过去二十年里，已有数百万人因此丧命。受害者的家庭被彻底摧毁，很多情况下已经支离破碎。我们不能允许这场祸害继续荼毒美国！因此，在这一问题得到遏制或严格限制之前，原定于**三月四日**生效的**【关税】（Tariffs）**将如期生效，一分不差！中国同样将在当天被加征额外10%的关税。四月二日的对等关税（Reciprocal Tariff）日期依然完全有效，雷打不动。感谢你们关注此事。**愿上帝保佑美国！**

**Candidate events in [-10d, +60d] window:**

- **[7]** `2025-02-25` Δ-2d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+2d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+5d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+34d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+34d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+35d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+36d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+41d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+41d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+54d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 31 · Episode 82

**Episode first-post date**: 2025-10-10

**Episode first-post text** (EN):
> It has just been learned that China has taken an extraordinarily aggressive position on Trade in sending an extremely hostile letter to the World, stating that they were going to, effective November 1st, 2025, impose large scale Export Controls on virtually every product they make, and some not even made by them. This affects ALL Countries, without exception, and was obviously a plan devised by them years ago. It is absolutely unheard of in International Trade, and a moral disgrace in dealing with other Nations.Based on the fact that China has taken this unprecedented position, and speaking only for the U.S.A., and not other Nations who were similarly threatened, starting November 1st, 2025 (or sooner, depending on any further actions or changes taken by China), the United States of America will impose a Tariff of 100% on China, over and above any Tariff that they are currently paying. Also on November 1st, we will impose Export Controls on any and all critical software.It is impossibl

**ZH 翻译**:
> 刚刚获悉，中国在贸易问题上采取了一个【极其】激进的立场，向全世界发出了一封极具敌意的信，声称将于2025年11月1日起，对他们生产的几乎每一种产品——甚至包括一些根本不是他们生产的产品——实施大规模出口管制（Export Controls）。这波及**所有**国家，无一例外，而且很明显这是他们几年前就精心谋划好的。这在国际贸易中简直闻所未闻，在与其他国家的往来中更是一种道德上的**耻辱**！

鉴于中国采取了这一史无前例的立场，我仅代表美利坚合众国发言，而非其他同样遭受威胁的国家——从2025年11月1日起（或更早，具体取决于中国的进一步行动或变化），美利坚合众国将对中国加征**100%**的关税（Tariff），叠加在他们目前已经支付的所有关税之上。同样在11月1日，我们将对任何及所有关键软件实施出口管制！

真难以置信中国居然会做出这样的举动，但他们就是这么干了，剩下的，就交给历史去评判吧。感谢你关注此事！

**唐纳德·J·特朗普**
**美利坚合众国总统**

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ-10d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ-10d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ-9d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+0d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+20d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+35d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits
- **[33]** `2025-12-01` Δ+52d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 32 · Episode 80

**Episode first-post date**: 2025-09-29

**Episode first-post text** (EN):
> In order to make North Carolina, which has completely lost its furniture business to China, and other Countries, GREAT again, I will be imposing substantial Tariffs on any Country that does not make its furniture in the United States. Details to follow!!! President DJT

**ZH 翻译**:
> 为了让北卡罗来纳州——那个把家具生意【完全】拱手让给中国和其他国家的地方——再次**伟大**，我将对所有不在美国本土生产家具的国家征收**巨额**关税（Tariff）。详情随后公布！！！总统 DJT

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ+1d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ+1d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+2d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+11d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+31d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+46d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 33 · Episode 74

**Episode first-post date**: 2025-08-26

**Episode first-post text** (EN):
> As the President of the United States, I will stand up to Countries that attack our incredible American Tech Companies. Digital Taxes, Digital Services Legislation, and Digital Markets Regulations are all designed to harm, or discriminate against, American Technology. They also, outrageously, give a complete pass to China's largest Tech Companies. This must end, and end NOW! With this TRUTH, I put all Countries with Digital Taxes, Legislation, Rules, or Regulations, on notice that unless these discriminatory actions are removed, I, as President of the United States, will impose substantial additional Tariffs on that Country's Exports to the U.S.A., and institute Export restrictions on our Highly Protected Technology and Chips. America, and American Technology Companies, are neither the "piggy bank" nor the "doormat" of the World any longer. Show respect to America and our amazing Tech Companies or, consider the consequences! Thank you for your attention to this matter.DONALD J. TRUMP, 

**ZH 翻译**:
> 作为美利坚合众国总统，我将挺身而出，对抗那些攻击我们**无与伦比**的美国科技公司的国家。数字税、数字服务立法、数字市场监管——这些全都是为了打压、歧视美国科技而设计的。更**无耻**的是，这些规定对中国最大的科技公司完全网开一面。这种事必须终止，而且**现在就终止**！通过这条 TRUTH，我正式警告所有搞数字税、立法、规则或监管的国家：除非立刻撤销这些歧视性行动，否则我，作为美利坚合众国总统，将对该国出口到美国的商品征收**大幅额外关税**（Tariffs），并对我们**受到严格保护**的技术和芯片实施出口限制！美国，以及美国的科技公司，再也不是世界的"提款机"，也不是世界的"门垫"了。给美国和我们**了不起**的科技公司应有的尊重，否则——自己掂量后果！感谢您关注此事。美利坚合众国总统 唐纳德·J·特朗普

**Candidate events in [-10d, +60d] window:**

- **[25]** `2025-08-19` Δ-7d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+1d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%
- **[27]** `2025-09-30` Δ+35d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ+35d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+36d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+45d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 34 · Episode 102

**Episode first-post date**: 2026-02-21

**Episode first-post text** (EN):
> What happened today with the two United States Supreme Court Justices that I appointed against great opposition, Neil Gorsuch and Amy Coney Barrett, whether people like it or not, never seems to happen with Democrats. They vote against the Republicans, and never against themselves, almost every single time, no matter how good a case we have. At least I didn't appoint Roberts, who led the effort to allow Foreign Countries that have been ripping us off for years to continue to do so — But we won't let it happen. The new TARIFFS, totally tested and accepted as Law, are on their way! PRESIDENT DONALD J. TRUMP

**ZH 翻译**:
> 今天发生了什么事——我任命的两位美国最高法院大法官，尽管遭到巨大反对，Neil Gorsuch 和 Amy Coney Barrett，不管人们是否喜欢，这种事似乎从来不会发生在民主党人身上。他们投票反对共和党人，而从不反对他们自己，几乎每一次都是这样，无论我们的案件有多好。至少我没有任命 Roberts，他领导了一场努力，允许那些多年来一直在掠夺我们的外国继续这样做——但我们不会让这种事发生。新的关税（TARIFFS），【完全】经过测试和被接受为法律，正在路上！总统 Donald J. Trump

**Candidate events in [-10d, +60d] window:**

- **[38]** `2026-02-20` Δ-1d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ-1d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+18d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation
- **[41]** `2026-04-02` Δ+40d | target: `metal_products_clarified` | status: `modified` | note: tier-based clarification
- **[42]** `2026-04-02` Δ+40d | target: `pharmaceuticals_patented` | status: `in_effect` | note: lower rates for EU/Japan/Korea/Switzerland (15%), UK (10%); generics exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 35 · Episode 7

**Episode first-post date**: 2024-12-10

**Episode first-post text** (EN):
> It was a pleasure to have dinner the other night with Governor Justin Trudeau of the Great State of Canada. I look forward to seeing the Governor again soon so that we may continue our in depth talks on Tariffs and Trade, the results of which will be truly spectacular for all! DJT

**ZH 翻译**:
> 前几天与加拿大伟大州的州长贾斯汀·特鲁多共进晚餐，【真是】一种荣幸。我期待【很快】再次见到州长，以便我们可以继续就关税(Tariff)和贸易进行【深入】的谈话，其结果对所有人来说将【真正】是壮观的！DJT

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+41d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+53d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+53d | target: `China` | status: `struck_down` | note: fentanyl tariff

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 36 · Episode 43

**Episode first-post date**: 2025-04-16

**Episode first-post text** (EN):
> Japan is coming in today to negotiate Tariffs, the cost of military support, and âTRADE FAIRNESS.â I will attend the meeting, along with Treasury &amp; Commerce Secretaries. Hopefully something can be worked out which is good (GREAT!) for Japan and the USA!

**ZH 翻译**:
> 日本今天来谈判关税（Tariff）、军事支持费用，还有"贸易公平"的问题。我会亲自出席会议，财政部长和商务部长也会一起来。希望能谈出一个对日本和美国都好（【超级好！】）的结果！

**Candidate events in [-10d, +60d] window:**

- **[14]** `2025-04-09` Δ-7d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ-7d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+6d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+13d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+17d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+44d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+57d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 37 · Episode 62

**Episode first-post date**: 2025-07-07

**Episode first-post text** (EN):
> I am pleased to announce that the UNITED STATES TARIFF Letters, and/or Deals, with various Countries from around the World, will be delivered starting 12:00 P.M. (Eastern), Monday, July 7th. Thank you for your attention to this matter! DONALD J. TRUMP, President of The United States of America.

**ZH 翻译**:
> 我很高兴地宣布，美利坚合众国的【关税】信函，和/或与世界各地不同国家达成的协议，将于7月7日星期一东部时间下午12:00起开始送达。感谢你们对此事的关注！唐纳德·J·特朗普，美利坚合众国总统。

**Candidate events in [-10d, +60d] window:**

- **[21]** `2025-07-04` Δ-3d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+1d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+1d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+23d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+43d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+51d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 38 · Episode 82

**Episode first-post date**: 2025-10-10

**Episode first-post text** (EN):
> It has just been learned that China has taken an extraordinarily aggressive position on Trade in sending an extremely hostile letter to the World, stating that they were going to, effective November 1st, 2025, impose large scale Export Controls on virtually every product they make, and some not even made by them. This affects ALL Countries, without exception, and was obviously a plan devised by them years ago. It is absolutely unheard of in International Trade, and a moral disgrace in dealing with other Nations.Based on the fact that China has taken this unprecedented position, and speaking only for the U.S.A., and not other Nations who were similarly threatened, starting November 1st, 2025 (or sooner, depending on any further actions or changes taken by China), the United States of America will impose a Tariff of 100% on China, over and above any Tariff that they are currently paying. Also on November 1st, we will impose Export Controls on any and all critical software.It is impossibl

**ZH 翻译**:
> 刚刚获悉，中国在贸易问题上采取了一个【极其】激进的立场，向全世界发出了一封极具敌意的信，声称将于2025年11月1日起，对他们生产的几乎每一种产品——甚至包括一些根本不是他们生产的产品——实施大规模出口管制（Export Controls）。这波及**所有**国家，无一例外，而且很明显这是他们几年前就精心谋划好的。这在国际贸易中简直闻所未闻，在与其他国家的往来中更是一种道德上的**耻辱**！

鉴于中国采取了这一史无前例的立场，我仅代表美利坚合众国发言，而非其他同样遭受威胁的国家——从2025年11月1日起（或更早，具体取决于中国的进一步行动或变化），美利坚合众国将对中国加征**100%**的关税（Tariff），叠加在他们目前已经支付的所有关税之上。同样在11月1日，我们将对任何及所有关键软件实施出口管制！

真难以置信中国居然会做出这样的举动，但他们就是这么干了，剩下的，就交给历史去评判吧。感谢你关注此事！

**唐纳德·J·特朗普**
**美利坚合众国总统**

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ-10d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ-10d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ-9d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[31]** `2025-10-30` Δ+20d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+35d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits
- **[33]** `2025-12-01` Δ+52d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 39 · Episode 30

**Episode first-post date**: 2025-03-06

**Episode first-post text** (EN):
> Massive Trade Deficit with the World, just announced, compliments of Sleepy Joe Biden! I will change that!!!

**ZH 翻译**:
> **巨大的贸易赤字(Trade Deficit)与世界，刚刚宣布，多亏了瞌睡乔拜登!我会改变那个!!!**

**Candidate events in [-10d, +60d] window:**

- **[7]** `2025-02-25` Δ-9d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ-5d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ-2d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+27d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+27d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+28d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+29d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+34d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+34d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+47d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+54d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+58d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 40 · Episode 69

**Episode first-post date**: 2025-07-23

**Episode first-post text** (EN):
> I will always give up Tariff points if I can get major countries to OPEN THEIR MARKETS TO THE USA. Another great power of Tariffs. Without them, it would be impossible to get countries to OPEN UP!!! ALWAYS, ZERO TARIFFS TO AMERICA!!!

**ZH 翻译**:
> 只要能让主要国家**对美国开放市场**，我随时愿意在关税（Tariff）上让步。这就是关税的另一大威力。没有关税，根本不可能让那些国家**开放**！！！永远都是这样，给美国**零关税**！！！

**Candidate events in [-10d, +60d] window:**

- **[24]** `2025-07-30` Δ+7d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+27d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+35d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 41 · Episode 42

**Episode first-post date**: 2025-04-15

**Episode first-post text** (EN):
> Our farmers are GREAT, but because of their GREATNESS, they are always put on the Front Line with our adversaries, such as China, whenever there is a Trade negotiation or, in this case, a Trade War. The same thing happened in my First Term. China was brutal to our Farmers, I these Patriots to just hold on, and a great trade deal was made. I rewarded our farmers with a payment of $28 Billion Dollars, all through the China deal. It was a great transaction for the USA, until Crooked Joe Biden came in and didnât enforce it. China largely reneged on the deal (although they behaved during the Trump Administration), only buying a portion of what they agreed to buy. They had ZERO respect for the Crooked Biden Administration, and who can blame them for that? Interestingly, they just reneged on the big Boeing deal, saying that they will ânot take possessionâ of fully committed to aircraft. The USA will PROTECT OUR FARMERS!!!

**ZH 翻译**:
> 我们的农民是【伟大的】，但正因为他们的【伟大】，每当与我们的对手（如中国）进行贸易谈判或（在这种情况下）贸易战时，他们总是被放在前线。我的第一任期发生过同样的事情。中国对我们的农民很残酷，我告诉这些爱国者们坚持住，随后达成了一项伟大的贸易协议。我通过中国协议用280亿美元的支付奖励了我们的农民。这对美国来说是一项伟大的交易，直到腐败的乔·拜登上台，他没有执行它。中国在很大程度上违反了协议（尽管他们在特朗普政府期间表现得很好），只购买了他们同意购买的一部分。他们对腐败的拜登政府【完全没有】尊重，谁能责怪他们呢？有趣的是，他们刚刚违反了波音的大协议，说他们将"不接收"承诺的飞机。美国将【保护我们的农民】！！！

**Candidate events in [-10d, +60d] window:**

- **[14]** `2025-04-09` Δ-6d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ-6d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+7d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+14d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+18d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+45d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+58d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 42 · Episode 45

**Episode first-post date**: 2025-04-27

**Episode first-post text** (EN):
> When Tariffs cut in, many peopleâs Income Taxes will be substantially reduced, maybe even completely eliminated. Focus will be on people making less than $200,000 a year. Also, massive numbers of jobs are already being created, with new plants and factories currently being built or planned. It will be a BONANZA FOR AMERICA!!! THE EXTERNAL REVENUE SERVICE IS HAPPENING!!!

**ZH 翻译**:
> 当关税（Tariff）开始发挥作用，很多人的所得税将大幅降低，甚至可能完全取消。重点针对年收入不到20万美元的人群。而且，**大量**就业岗位已经在创造之中，新的工厂和生产基地正在建设或规划当中。这对美国来说将是一场【天降横财】！！！【对外税务局】就要来了！！！

**Candidate events in [-10d, +60d] window:**

- **[16]** `2025-04-22` Δ-5d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+2d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+6d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+33d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+46d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 43 · Episode 48

**Episode first-post date**: 2025-05-04

**Episode first-post text** (EN):
> The Movie Industry in America is DYING a very fast death. Other Countries are offering all sorts of incentives to draw our filmmakers and studios away from the United States. Hollywood, and many other areas within the U.S.A., are being devastated. This is a concerted effort by other Nations and, therefore, a National Security threat. It is, in addition to everything else, messaging and propaganda! Therefore, I am authorizing the Department of Commerce, and the United States Trade Representative, to immediately begin the process of instituting a 100% Tariff on any and all Movies coming into our Country that are produced in Foreign Lands. WE WANT MOVIES MADE IN AMERICA, AGAIN!

**ZH 翻译**:
> 美国电影产业正在**极速**走向死亡。其他国家提供各种各样的优惠条件，把我们的电影人和制片公司从美国挖走。好莱坞，还有美国境内的许多其他地方，都在遭受**毁灭性**打击。这是其他国家精心策划的行动，因此，这是一个国家安全威胁。而且，除了别的一切，这还是一种信息操控和宣传！因此，我授权商务部和美国贸易代表，立即启动程序，对所有在外国生产、进入我国的电影征收**100%关税（Tariff）**！【我们要让电影再次在美国制造！】

**Candidate events in [-10d, +60d] window:**

- **[17]** `2025-04-29` Δ-5d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ-1d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+26d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+39d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 44 · Episode 36

**Episode first-post date**: 2025-03-27

**Episode first-post text** (EN):
> If the European Union works with Canada in order to do economic harm to the USA, large scale Tariffs, far larger than currently planned, will be placed on them both in order to protect the best friend that each of those two countries has ever had!

**ZH 翻译**:
> 如果欧盟跟加拿大联手来损害美国的经济利益，我会对他们两个都征收关税（Tariffs），而且比现在计划的**大得多、大得多**，这是为了保护这两个国家有史以来最好的朋友！

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ+6d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+6d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+7d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+8d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+13d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+13d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+26d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+33d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+37d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 45 · Episode 40

**Episode first-post date**: 2025-04-07

**Episode first-post text** (EN):
> Yesterday, China issued Retaliatory Tariffs of 34%, on top of their already record setting Tariffs, Non-Monetary Tariffs, Illegal Subsidization of companies, and massive long term Currency Manipulation, despite my warning that any country that Retaliates against the U.S. by issuing additional Tariffs, above and beyond their already existing long term Tariff abuse of our Nation, will be immediately met with new and substantially higher Tariffs, over and above those initially set. Therefore, if China does not withdraw its 34% increase above their already long term trading abuses by tomorrow, April 8th, 2025, the United States will impose ADDITIONAL Tariffs on China of 50%, effective April 9th. Additionally, all talks with China concerning their requested meetings with us will be terminated! Negotiations with other countries, which have also requested meetings, will begin taking place immediately. Thank you for your attention to this matter!

**ZH 翻译**:
> 昨天，中国对美国加征了34%的**报复性关税**，叠加在他们已经创历史纪录的关税、非货币性壁垒、对企业的非法补贴，以及长达多年的**大规模**货币操纵之上——这一切都发生在我明确警告之后！我早就说过，任何国家如果胆敢对美国采取报复行动、在其已经长期滥用的关税基础上再加码，都将**立即**迎来更高、更猛的新关税！因此，如果中国不在明天——2025年4月8日——之前撤回这34%的加税，美国将对中国**额外**再加征50%的关税，自4月9日起生效！除此之外，所有中国方面请求与我们会谈的谈判，全部**立即终止**！而其他同样请求会谈的国家，谈判将马上启动！感谢你们关注此事！

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ-5d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ-5d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ-4d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ-3d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+2d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[16]** `2025-04-22` Δ+15d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+22d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+26d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+53d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 46 · Episode 11

**Episode first-post date**: 2024-12-20

**Episode first-post text** (EN):
> I told the European Union that they must make up their tremendous deficit with the United States by the large scale purchase of our oil and gas. Otherwise, it is TARIFFS all the way!!!

**ZH 翻译**:
> 我告诉欧盟，他们必须通过大规模购买我们的石油和天然气来弥补与美国之间【巨大的】赤字。否则就是关税(Tariffs)一切！！！

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+31d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+43d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[2]** `2025-02-01` Δ+43d | target: `Canada` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+43d | target: `China` | status: `struck_down` | note: fentanyl tariff
- **[4]** `2025-02-10` Δ+52d | target: `steel_aluminum` | status: `in_effect` | note: removed exemptions
- **[5]** `2025-02-13` Δ+55d | target: `all_countries` | status: `struck_down` | note: reciprocal tariffs framework
- **[6]** `2025-02-14` Δ+56d | target: `autos` | status: `in_effect` | note: auto tariffs

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 47 · Episode 83

**Episode first-post date**: 2025-10-14

**Episode first-post text** (EN):
> I believe that China purposefully not buying our Soybeans, and causing difficulty for our Soybean Farmers, is an Economically Hostile Act. We are considering terminating business with China having to do with Cooking Oil, and other elements of Trade, as retribution. As an example, we can easily produce Cooking Oil ourselves, we don't need to purchase it from China.

**ZH 翻译**:
> 我相信中国故意不购买我们的大豆，对我们的大豆农民造成困难，这是一种【经济上的】敌对行为。我们正在考虑终止与中国在食用油(Cooking Oil)和其他贸易要素方面的业务往来，作为报复。例如，我们完全可以自己生产食用油(Cooking Oil)，我们不需要从中国购买。

**Candidate events in [-10d, +60d] window:**

- **[30]** `2025-10-10` Δ-4d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+16d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+31d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits
- **[33]** `2025-12-01` Δ+48d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 48 · Episode 73

**Episode first-post date**: 2025-08-22

**Episode first-post text** (EN):
> I am pleased to announce that we are doing a major Tariff Investigation on Furniture coming into the United States. Within the next 50 days, that Investigation will be completed, and Furniture coming from other Countries into the United States will be Tariffed at a Rate yet to be determined. This will bring the Furniture Business back to North Carolina, South Carolina, Michigan, and States all across the Union. Thank you for your attention to this matter!

**ZH 翻译**:
> 我很高兴宣布，我们正在对进入美国的家具展开一项**重大**关税（Tariff）调查。在接下来的50天内，这项调查将会完成，从其他国家进入美国的家具将被征收关税（Tariff），具体税率有待确定。这将把家具产业带回北卡罗来纳州、南卡罗来纳州、密歇根州，以及全国各地的州！感谢你们对此事的关注！

**Candidate events in [-10d, +60d] window:**

- **[25]** `2025-08-19` Δ-3d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+5d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%
- **[27]** `2025-09-30` Δ+39d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ+39d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+40d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+49d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 49 · Episode 3

**Episode first-post date**: 2024-12-04

**Episode first-post text** (EN):
> I am pleased to announce that Peter Navarro, a man who was treated horribly by the Deep State, or whatever else you would like to call it, will serve as my Senior Counselor for Trade and Manufacturing. During my First Term, few were more effective or tenacious than Peter in enforcing my two sacred rules, Buy American, Hire American. He helped me renegotiate unfair Trade Deals like NAFTA and the Korea-U.S. Free Trade Agreement (KORUS), and moved every one of my Tariff and Trade actions FAST….

**ZH 翻译**:
> 我很高兴地宣布，彼得·纳瓦罗(Peter Navarro)，一位曾遭受Deep State或其他任何你想称呼它的东西可怕对待的人，将担任我的贸易和制造业高级顾问。在我的第一任期内，很少有人比彼得更有效率或更坚定地执行我的两条神圣规则，**Buy American, Hire American**。他帮助我重新谈判了不公平的Trade Deals，如NAFTA和Korea-U.S. Free Trade Agreement (KORUS)，并迅速推进了我的每一项Tariff和Trade行动……

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+47d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+59d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[2]** `2025-02-01` Δ+59d | target: `Canada` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+59d | target: `China` | status: `struck_down` | note: fentanyl tariff

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 50 · Episode 65

**Episode first-post date**: 2025-07-08

**Episode first-post text** (EN):
> We will be releasing a minimum of 7 Countries having to do with trade, tomorrow morning, with an additional number of Countries being released in the afternoon. Thank you for your attention to this matter!

**ZH 翻译**:
> 我们明天上午将发布与贸易有关的**至少7个国家**，下午还将发布额外数量的国家。感谢您对此事的关注！

**Candidate events in [-10d, +60d] window:**

- **[21]** `2025-07-04` Δ-4d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+0d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+0d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+22d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+42d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+50d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 51 · Episode 20

**Episode first-post date**: 2025-02-13

**Episode first-post text** (EN):
> On Trade, I have decided, for purposes of Fairness, that I will charge a RECIPROCAL Tariff meaning, whatever Countries charge the United States of America, we will charge them - No more, no less!For purposes of this United States Policy, we will consider Countries that use the VAT System, which is far more punitive than a Tariff, to be similar to that of a Tariff. Sending merchandise, product, or anything by any other name through another Country, for purposes of unfairly harming America, will not be accepted. In addition, we will make provision for subsidies provided by Countries in order to take Economic advantage of the United States. Likewise, provisions will be made for Nonmonetary Tariffs and Trade Barriers that some Countries charge in order to keep our product out of their domain or, if they do not even let U.S. businesses operate. We are able to accurately determine the cost of these Nonmonetary Trade Barriers. It is fair to all, no other Country can complain and, in some case

**ZH 翻译**:
> 关于贸易问题，为了公平起见，我已决定对其他国家征收**对等**关税（Reciprocal Tariff），意思就是——不管哪个国家向美利坚合众国收多少，我们就向他们收多少——一分不多，一分不少！就美国的这一政策而言，我们将把使用增值税（VAT）体系的国家视同征收关税——那套增值税玩法比关税狠多了。任何国家妄图把商品、产品或任何东西绕道第三国转运，以此不公平地坑害美国，我们绝不接受！此外，我们还会把那些国家为了占美国经济便宜而发放的补贴统统纳入考量。同样，对于某些国家为了把我们的产品挡在门外、甚至不让美国企业在当地运营而设置的非货币性关税（Nonmonetary Tariffs）和贸易壁垒（Trade Barriers），我们也会一并应对。这些非货币性贸易壁垒的成本，我们完全可以精准核算。这对所有人都公平，没有哪个国家能有话说——而且，如果哪个国家觉得美国的关税定得太高，他们要做的就一件事：降低或取消他们针对我们的关税。如果你在美国本土制造或生产产品，关税为零。

多少年来，美国被其他国家不公平对待，不管是盟友还是对手，都一个德行。这套新体系将立即把公平与繁荣带回到此前那个复杂又不公平的贸易体系中来。多年来，美国帮助了无数国家，付出了【巨大的财务代价】。现在，该是这些国家记住这一点、公平对待我们的时候了——**给美国工人一个公平的竞争环境**！我已责令我的国务卿、商务部长、财政部长，以及美国贸易代表（USTR），做一切必要的工作，把**对等**原则（Reciprocity）落实到我们的贸易体系中去！

**Candidate events in [-10d, +60d] window:**

- **[4]** `2025-02-10` Δ-3d | target: `steel_aluminum` | status: `in_effect` | note: removed exemptions
- **[5]** `2025-02-13` Δ+0d | target: `all_countries` | status: `struck_down` | note: reciprocal tariffs framework
- **[6]** `2025-02-14` Δ+1d | target: `autos` | status: `in_effect` | note: auto tariffs
- **[7]** `2025-02-25` Δ+12d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+16d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+19d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+48d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+48d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+49d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+50d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+55d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+55d | target: `China` | status: `modified` | note: retaliatory escalation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 52 · Episode 55

**Episode first-post date**: 2025-05-23

**Episode first-post text** (EN):
> I am proud to announce that, after much consideration and negotiation, US Steel will REMAIN in America, and keep its Headquarters in the Great City of Pittsburgh. For many years, the name, âUnited States Steelâ was synonymous with Greatness, and now, it will be again. This will be a planned partnership between United States Steel and Nippon Steel, which will create at least 70,000 jobs, and add $14 Billion Dollars to the U.S. Economy. The bulk of that Investment will occur in the next 14 months. This is the largest Investment in the History of the Commonwealth of Pennsylvania. My Tariff Policies will ensure that Steel will once again be, forever, MADE IN AMERICA. From Pennsylvania to Arkansas, and from Minnesota to Indiana, AMERICAN MADE is BACK. I will see you all at US Steel, in Pittsburgh, on Friday, May 30th, for a BIG Rally. CONGRATULATIONS TO ALL!

**ZH 翻译**:
> 我荣幸地宣布，经过深思熟虑和谈判，美国钢铁公司将保留在美国，并将其总部保留在伟大的匹兹堡市。多年来，"美国钢铁"这个名字是【伟大】的代名词，现在它将再次成为代名词。这将是美国钢铁公司和日本新日铁公司之间的战略性合作伙伴关系，将创造至少70,000个工作岗位，并为美国经济增加140亿美元。大部分投资将在未来14个月内进行。这是宾夕法尼亚州历史上【最大】的投资。我的关税(Tariff)政策将确保钢铁将再次永远地【美国制造】。从宾夕法尼亚到阿肯色州，从明尼苏达到印第安纳州，【美国制造回归】了！我将在5月30日星期五在匹兹堡的美国钢铁公司与大家见面，参加一场【盛大】的集会。向所有人表示祝贺！

**Candidate events in [-10d, +60d] window:**

- **[19]** `2025-05-30` Δ+7d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+20d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+42d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+46d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+46d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 53 · Episode 14

**Episode first-post date**: 2025-01-14

**Episode first-post text** (EN):
> For far too long, we have relied on taxing our Great People using the Internal Revenue Service (IRS). Through soft and pathetically weak Trade agreements, the American Economy has delivered growth and prosperity to the World, while taxing ourselves. It is time for that to change. I am today announcing that I will create the EXTERNAL REVENUE SERVICE to collect our Tariffs, Duties, and all Revenue that come from Foreign sources. We will begin charging those that make money off of us with Trade, and they will start paying, FINALLY, their fair share. January 20, 2025, will be the birth date of the External Revenue Service. MAKE AMERICA GREAT AGAIN!

**ZH 翻译**:
> 长期以来，我们一直依赖通过国税局(Internal Revenue Service, IRS)对我们伟大的人民征税。通过软弱和可悲的贸易协议，美国经济为世界带来了增长和繁荣，同时我们却在对自己征税。改变的时候到了。我今天宣布，我将创建**外部收入局(External Revenue Service)**来征收我们的关税(Tariff)、税款和所有来自外国来源的收入。我们将开始向那些通过贸易从我们身上赚钱的人征费，他们将开始支付，**【终于】**，他们公平的份额。2025年1月20日将是外部收入局的诞生日期。**让美国再次伟大！**

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+6d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+18d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[2]** `2025-02-01` Δ+18d | target: `Canada` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+18d | target: `China` | status: `struck_down` | note: fentanyl tariff
- **[4]** `2025-02-10` Δ+27d | target: `steel_aluminum` | status: `in_effect` | note: removed exemptions
- **[5]** `2025-02-13` Δ+30d | target: `all_countries` | status: `struck_down` | note: reciprocal tariffs framework
- **[6]** `2025-02-14` Δ+31d | target: `autos` | status: `in_effect` | note: auto tariffs
- **[7]** `2025-02-25` Δ+42d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+46d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+49d | target: `China` | status: `modified` | note: increased from 10%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 54 · Episode 77

**Episode first-post date**: 2025-09-25

**Episode first-post text** (EN):
> We will be imposing a 50% Tariff on all Kitchen Cabinets, Bathroom Vanities, and associated products, starting October 1st, 2025. Additionally, we will be charging a 30% Tariff on Upholstered Furniture. The reason for this is the large scale "FLOODING" of these products into the United States by other outside Countries. It is a very unfair practice, but we must protect, for National Security and other reasons, our Manufacturing process. Thank you for your attention to this matter!

**ZH 翻译**:
> 从2025年10月1日起，我们将对所有厨柜、浴室梳妆台及相关产品征收50%的关税（Tariff）！此外，软垫家具将被征收30%的关税（Tariff）！原因是其他国家正在大规模【"洪水式"倾销】这些产品进入美国市场。这是一种极其不公平的做法，但为了国家安全以及其他原因，我们必须保护我们自己的制造业！感谢大家关注这件事！

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ+5d | target: `lumber` | status: `in_effect` | note: softwood
- **[29]** `2025-10-01` Δ+6d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+15d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+35d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+50d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 55 · Episode 7

**Episode first-post date**: 2024-12-10

**Episode first-post text** (EN):
> It was a pleasure to have dinner the other night with Governor Justin Trudeau of the Great State of Canada. I look forward to seeing the Governor again soon so that we may continue our in depth talks on Tariffs and Trade, the results of which will be truly spectacular for all! DJT

**ZH 翻译**:
> 前几天与加拿大伟大州的州长贾斯汀·特鲁多共进晚餐，【真是】一种荣幸。我期待【很快】再次见到州长，以便我们可以继续就关税(Tariff)和贸易进行【深入】的谈话，其结果对所有人来说将【真正】是壮观的！DJT

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+41d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+53d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[2]** `2025-02-01` Δ+53d | target: `Canada` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+53d | target: `China` | status: `struck_down` | note: fentanyl tariff

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 56 · Episode 63

**Episode first-post date**: 2025-07-07

**Episode first-post text** (EN):
> Any Country aligning themselves with the Anti-American policies of BRICS, will be charged an ADDITIONAL 10% Tariff. There will be no exceptions to this policy. Thank you for your attention to this matter!

**ZH 翻译**:
> 任何国家，只要跟金砖国家（BRICS）那套反美政策站在一起，就要被加收**额外**10%的关税（Tariff）。这条政策没有任何例外。感谢你们关注此事！

**Candidate events in [-10d, +60d] window:**

- **[21]** `2025-07-04` Δ-3d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+1d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+1d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+23d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+43d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+51d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 57 · Episode 86

**Episode first-post date**: 2025-12-08

**Episode first-post text** (EN):
> Mexico continues to violate our comprehensive Water Treaty, and this violation is seriously hurting our BEAUTIFUL TEXAS CROPS AND LIVESTOCK. Mexico still owes the U.S over 800,000 acre-feet of water for failing to comply with our Treaty over the past five years. The U.S needs Mexico to release 200,000 acre-feet of water before December 31st, and the rest must come soon after. As of now, Mexico is not responding, and it is very unfair to our U.S. Farmers who deserve this much needed water. That is why I have authorized documentation to impose a 5% Tariff on Mexico if this water isn't released, IMMEDIATELY. The longer Mexico takes to release the water, the more our Farmers are hurt. Mexico has an obligation to FIX THIS NOW. Thank you for your attention to this matter!

**ZH 翻译**:
> 墨西哥持续违反我们全面的水资源条约，这种违约行为正在严重损害我们**美丽的德克萨斯州农作物和牲畜**！过去五年里，墨西哥一直没有履行条约，现在还欠着美国超过80万英亩·英尺的水！美国要求墨西哥在12月31日之前放水20万英亩·英尺，剩下的也必须紧接着补上。就目前来看，墨西哥根本没有回应，这对我们美国农民极其不公平，他们理应得到这些急需的水！正因如此，我已授权相关文件——如果这些水【立刻】放不出来，就对墨西哥加征5%的关税（Tariff）！墨西哥拖得越久，我们的农民受到的伤害就越大！墨西哥有义务【现在就解决这个问题】！感谢大家对此事的关注！

**Candidate events in [-10d, +60d] window:**

- **[33]** `2025-12-01` Δ-7d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement
- **[34]** `2026-01-01` Δ+24d | target: `wooden_furniture` | status: `in_effect` | note: increased from 25%
- **[35]** `2026-01-14` Δ+37d | target: `semiconductors` | status: `in_effect` | note: advanced computing chips
- **[36]** `2026-01-17` Δ+40d | target: `8_european_countries` | status: `withdrawn` | note: Greenland Crisis; retracted Jan 21
- **[37]** `2026-02-02` Δ+56d | target: `India` | status: `modified` | note: reduced from 50%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 58 · Episode 94

**Episode first-post date**: 2026-01-17

**Episode first-post text** (EN):
> We have subsidized Denmark, and all of the Countries of the European Union, and others, for many years by not charging them Tariffs, or any other forms of remuneration. Now, after Centuries, it is time for Denmark to give back — World Peace is at stake! China and Russia want Greenland, and there is not a thing that Denmark can do about it. They currently have two dogsleds as protection, one added recently. Only the United States of America, under PRESIDENT DONALD J. TRUMP, can play in this game, and very successfully, at that! Nobody will touch this sacred piece of Land, especially since the National Security of the United States, and the World at large, is at stake. On top of everything else, Denmark, Norway, Sweden, France, Germany, The United Kingdom, The Netherlands, and Finland have journeyed to Greenland, for purposes unknown. This is a very dangerous situation for the Safety, Security, and Survival of our Planet. These Countries, who are playing this very dangerous game, have pu

**ZH 翻译**:
> 多年来，我们一直在补贴丹麦、欧盟所有国家以及其他国家——不向他们征收关税(Tariff)，也没有收取任何其他形式的报酬。现在，经过几个世纪之后，是时候让丹麦回报了——世界和平岌岌可危！中国和俄罗斯都盯着格陵兰，丹麦根本拿他们没辙。他们现在就靠两架狗拉雪橇来保护，其中一架还是最近才加的。只有美利坚合众国，在**唐纳德·J·特朗普总统**的领导下，才能参与这场博弈，而且还能玩得非常漂亮！没有人敢动这片神圣的土地，尤其是美国的国家安全以及整个世界的安全都押在这上面。更重要的是，丹麦、挪威、瑞典、法国、德国、英国、荷兰和芬兰已经跑去格陵兰了，目的不明。这对我们星球的安全、保障和生存来说是一个**极其危险**的局面。这些国家正在玩一个非常危险的游戏，把风险推到了一个根本站不住脚、也不可持续的地步。因此，为了保护全球和平与安全，必须采取强硬措施，让这个潜在的危险局面尽快、毫无疑问地结束！从2026年2月1日起，上述所有国家（丹麦、挪威、瑞典、法国、德国、英国、荷兰和芬兰）向美利坚合众国出口的一切商品，都将被征收10%的关税(Tariff)！到2026年6月1日，关税将提高到25%！这个关税会一直收下去，直到达成一项关于**完整、彻底**收购格陵兰的协议为止。美国为这笔交易已经努力了超过150年了。很多总统都试过，理由充分，但丹麦一直拒绝。现在，由于黄金穹顶(Golden Dome)以及现代武器系统——无论是进攻性的还是防御性的——【收购】的必要性变得尤为重要。数千亿美元的

**Candidate events in [-10d, +60d] window:**

- **[35]** `2026-01-14` Δ-3d | target: `semiconductors` | status: `in_effect` | note: advanced computing chips
- **[36]** `2026-01-17` Δ+0d | target: `8_european_countries` | status: `withdrawn` | note: Greenland Crisis; retracted Jan 21
- **[37]** `2026-02-02` Δ+16d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+34d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+34d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+53d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 59 · Episode 56

**Episode first-post date**: 2025-05-25

**Episode first-post text** (EN):
> I received a call today from Ursula von der Leyen, President of the European Commission, requesting an extension on the June 1st deadline on the 50% Tariff with respect to Trade and the European Union. I agreed to the extension â July 9, 2025 â It was my privilege to do so. The Commission President said that talks will begin rapidly. Thank you for your attention to this matter!

**ZH 翻译**:
> 今天我接到了欧盟委员会主席乌尔苏拉·冯德莱恩的电话，她请求延长6月1日关于欧盟贸易**50%关税（Tariff）**截止日期的期限。我同意了延期——**2025年7月9日**——这是我的荣幸！委员会主席表示谈判将迅速展开。感谢你们关注此事！

**Candidate events in [-10d, +60d] window:**

- **[19]** `2025-05-30` Δ+5d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt
- **[20]** `2025-06-12` Δ+18d | target: `household_appliances_metal` | status: `in_effect` | note: refrigerators, dishwashers, etc.
- **[21]** `2025-07-04` Δ+40d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+44d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+44d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 60 · Episode 25

**Episode first-post date**: 2025-02-27

**Episode first-post text** (EN):
> Drugs are still pouring into our Country from Mexico and Canada at  very high and unacceptable levels. A large percentage of these Drugs, much of them in the form of Fentanyl, are made in, and supplied by, China. More than 100,000 people died last year due to the distribution of these dangerous and highly addictive POISONS. Millions of people have died over the last two decades. The families of the victims are devastated and, in many instances, virtually destroyed. We cannot allow this scourge to continue to harm the USA, and therefore, until it stops, or is seriously limited, the proposed TARIFFS scheduled to go into effect on MARCH FOURTH will, indeed, go into effect, as scheduled. China will likewise be charged an additional 10% Tariff on that date. The April Second Reciprocal Tariff date will remain in full force and effect. Thank you for your attention to this matter. GOD BLESS AMERICA!

**ZH 翻译**:
> 毒品仍在以【极高且不可接受】的水平从墨西哥和加拿大大量涌入我们国家。这些毒品中有很大一部分，很多是以芬太尼（Fentanyl）的形式，由中国制造并供应。去年，超过10万人因这些危险且【极具成瘾性】的**毒药**的流通而死亡。过去二十年里，已有数百万人因此丧命。受害者的家庭被彻底摧毁，很多情况下已经支离破碎。我们不能允许这场祸害继续荼毒美国！因此，在这一问题得到遏制或严格限制之前，原定于**三月四日**生效的**【关税】（Tariffs）**将如期生效，一分不差！中国同样将在当天被加征额外10%的关税。四月二日的对等关税（Reciprocal Tariff）日期依然完全有效，雷打不动。感谢你们关注此事。**愿上帝保佑美国！**

**Candidate events in [-10d, +60d] window:**

- **[7]** `2025-02-25` Δ-2d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+2d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[10]** `2025-04-02` Δ+34d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+34d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+35d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+36d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+41d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+41d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+54d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 61 · Episode 105

**Episode first-post date**: 2026-04-11

**Episode first-post text** (EN):
> I am watching fertilizer prices CLOSELY during our FIGHT FOR FREEDOM in Iran. The United States will not accept PRICE GOUGING from the fertilizer monopoly! American Farmers, we have your back! President DONALD J. TRUMP

**ZH 翻译**:
> 我正在密切关注伊朗自由战争期间的肥料价格。美国不会接受来自肥料垄断企业的**PRICE GOUGING**！美国农民们，我们支持你们！总统 唐纳德·J·特朗普

**Candidate events in [-10d, +60d] window:**

- **[41]** `2026-04-02` Δ-9d | target: `metal_products_clarified` | status: `modified` | note: tier-based clarification
- **[42]** `2026-04-02` Δ-9d | target: `pharmaceuticals_patented` | status: `in_effect` | note: lower rates for EU/Japan/Korea/Switzerland (15%), UK (10%); generics exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 62 · Episode 95

**Episode first-post date**: 2026-01-21

**Episode first-post text** (EN):
> Based upon a very productive meeting that I have had with the Secretary General of NATO, Mark Rutte, we have formed the framework of a future deal with respect to Greenland and, in fact, the entire Arctic Region. This solution, if consummated, will be a great one for the United States of America, and all NATO Nations. Based upon this understanding, I will not be imposing the Tariffs that were scheduled to go into effect on February 1st. Additional discussions are being held concerning The Golden Dome as it pertains to Greenland. Further information will be made available as discussions progress. Vice President JD Vance, Secretary of State Marco Rubio, Special Envoy Steve Witkoff, and various others, as needed, will be responsible for the negotiations — They will report directly to me. Thank you for your attention to this matter!DONALD J. TRUMPPRESIDENT OF THE UNITED STATES OF AMERICA

**ZH 翻译**:
> 基于我与北约秘书长马克·吕特所进行的一次**极具成效**的会谈，我们已就格陵兰岛、乃至整个北极地区的未来协议搭建好了框架。这个方案一旦落地，对美利坚合众国以及全体北约国家来说都将是**巨大的**胜利！基于这一共识，我将不会对原定于2月1日生效的关税（Tariff）进行征收。目前还在就"黄金穹顶"（Golden Dome）与格陵兰岛相关事宜展开进一步磋商。随着谈判推进，更多信息将适时公布。副总统JD万斯、国务卿马科·卢比奥、特别使节史蒂夫·威特科夫，以及其他必要人员，将负责主导谈判——他们将直接向我汇报。感谢大家关注此事！唐纳德·J·特朗普美利坚合众国总统

**Candidate events in [-10d, +60d] window:**

- **[35]** `2026-01-14` Δ-7d | target: `semiconductors` | status: `in_effect` | note: advanced computing chips
- **[36]** `2026-01-17` Δ-4d | target: `8_european_countries` | status: `withdrawn` | note: Greenland Crisis; retracted Jan 21
- **[37]** `2026-02-02` Δ+12d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+30d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+30d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+49d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 63 · Episode 2

**Episode first-post date**: 2024-12-03

**Episode first-post text** (EN):
> I am totally against the once great and powerful U.S. Steel being bought by a foreign company, in this case Nippon Steel of Japan. Through a series of Tax Incentives and Tariffs, we will make U.S. Steel Strong and Great Again, and it will happen FAST! As President, I will block this deal from happening. Buyer Beware!!!

**ZH 翻译**:
> 我完全反对曾经伟大强大的U.S. Steel被外国公司收购，在这个案例中是日本的Nippon Steel。通过一系列的Tax Incentives和Tariffs，我们将使U.S. Steel强大和伟大再现，这将**快速发生**！作为总统，我将阻止这笔交易。买家小心!!!

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+48d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+60d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[2]** `2025-02-01` Δ+60d | target: `Canada` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+60d | target: `China` | status: `struck_down` | note: fentanyl tariff

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 64 · Episode 41

**Episode first-post date**: 2025-04-08

**Episode first-post text** (EN):
> I just had a great call with the Acting President of South Korea. We talked about their tremendous and unsustainable Surplus, Tariffs, Shipbuilding, large scale purchase of U.S. LNG, their joint venture in an Alaska Pipeline, and payment for the big time Military Protection we provide to South Korea. They began these Military payments during my first term, Billions of Dollars, but Sleepy Joe Biden, for reasons unknown, terminated the deal. That was a shocker to all! In any event, we have the confines and probability of a great DEAL for both countries. Their top TEAM is on a plane heading to the U.S., and things are looking good. We are likewise dealing with many other countries, all of whom want to make a deal with the United States. Like with South Korea, we are bringing up other subjects that are not covered by Trade and Tariffs, and getting them negotiated also. âONE STOP SHOPPINGâ is a beautiful and efficient process!!! China also wants to make a deal, badly, but they donât k

**ZH 翻译**:
> 我刚刚和韓國代理總統通了一個很好的電話。我們談論了他們龐大且不可持續的貿易順差、關稅(Tariff)、造船業、大規模購買美國液化天然氣、他們在阿拉斯加管道的合資企業，以及他們為我們提供給韓國的大規模軍事保護所支付的費用。他們在我第一任期間開始支付這些軍事費用，數十億美元，但昏睡喬·拜登(Sleepy Joe Biden)因未知原因終止了該協議。這令所有人感到震驚！無論如何，我們有【很大的】DEAL機率，對兩個國家都有利。他們的頂級TEAM正在飛往美國的飛機上，情況看起來很不錯。我們同樣在與許多其他國家進行談判，他們都想與美國達成協議。就像與韓國一樣，我們正在提出其他不受貿易和關稅(Tariff)涵蓋的主題，並將它們也協商好。「一站式購物」是一個【非常】美妙和高效的過程！！！中國也想【非常】想達成協議，但他們不知道如何開始。我們在等他們的電話。這肯定會發生！願上帝保佑美國。

**Candidate events in [-10d, +60d] window:**

- **[10]** `2025-04-02` Δ-6d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ-6d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ-5d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ-4d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+1d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+1d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+14d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+21d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+25d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted
- **[19]** `2025-05-30` Δ+52d | target: `steel_aluminum` | status: `in_effect` | note: doubled from 25%, UK exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 65 · Episode 24

**Episode first-post date**: 2025-02-25

**Episode first-post text** (EN):
> Like our Steel and Aluminum Industries, our Great American Copper Industry has been decimated by global actors attacking our domestic production. To build back our Copper Industry, I have requested my Secretary of Commerce and USTR to study Copper Imports, and end Unfair Trade putting Americans out of work. Tariffs will help build back our American Copper Industry, and strengthen our National Defense. American Industries depend on Copper, and it should be MADE IN AMERICA - No exemptions, no exceptions! America First creates American jobs, and protects our National Security. It’s time for Copper to “come home.”

**ZH 翻译**:
> 就像我们的钢铁和铝业一样，我们**伟大的美国铜业**已经被那些攻击我们国内生产的全球势力**彻底摧毁**了。为了重建我们的铜业，我已经要求商务部长和美国贸易代表对铜进口展开调查，终结那些让美国人失业的不公平贸易！关税（Tariff）将帮助重建我们的美国铜业，并增强我们的国家防御能力！美国工业依赖铜，而铜就应该**在美国制造（MADE IN AMERICA）** — 没有豁免，没有例外！美国优先创造美国就业岗位，保护我们的国家安全。是时候让铜"回家"了！

**Candidate events in [-10d, +60d] window:**

- **[7]** `2025-02-25` Δ+0d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+4d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+7d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+36d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+36d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+37d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+38d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+43d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+43d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+56d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 66 · Episode 13

**Episode first-post date**: 2025-01-06

**Episode first-post text** (EN):
> Members of Congress are getting to work on one powerful Bill that will bring our Country back, and make it greater than ever before. We must Secure our Border, Unleash American Energy, and Renew the Trump Tax Cuts, which were the largest in History, but we will make it even better - NO TAX ON TIPS. IT WILL ALL BE MADE UP WITH TARIFFS, AND MUCH MORE, FROM COUNTRIES THAT HAVE TAKEN ADVANTAGE OF THE U.S. FOR YEARS. Republicans must unite, and quickly deliver these Historic Victories for the American People. Get smart, tough, and send the Bill to my desk to sign as soon as possible. MAKE AMERICA GREAT AGAIN!

**ZH 翻译**:
> 国会议员们正在着手制定一项强大的法案，将使我们的国家重振雄风，比以往任何时候都更加伟大。我们必须【确保】我们的边境安全，【释放】美国能源，并【延续】特朗普减税政策，这是历史上【最大规模】的减税，但我们将把它做得更好——**没有小费税(No Tax on Tips)**。**这一切将通过关税(Tariff)和更多其他手段来弥补，针对那些多年来一直在利用美国的国家**。共和党人必须团结一致，快速为美国人民争取这些【历史性】胜利。要聪明，要强硬，尽快把法案送到我的办公桌前签署。**让美国再次伟大(MAKE AMERICA GREAT AGAIN)！**

**Candidate events in [-10d, +60d] window:**

- **[0]** `2025-01-20` Δ+14d | target: `general` | status: `in_effect` | note: inaugural pledge
- **[1]** `2025-02-01` Δ+26d | target: `Mexico` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[2]** `2025-02-01` Δ+26d | target: `Canada` | status: `struck_down` | note: fentanyl tariff; USMCA-compliant goods suspended
- **[3]** `2025-02-01` Δ+26d | target: `China` | status: `struck_down` | note: fentanyl tariff
- **[4]** `2025-02-10` Δ+35d | target: `steel_aluminum` | status: `in_effect` | note: removed exemptions
- **[5]** `2025-02-13` Δ+38d | target: `all_countries` | status: `struck_down` | note: reciprocal tariffs framework
- **[6]** `2025-02-14` Δ+39d | target: `autos` | status: `in_effect` | note: auto tariffs
- **[7]** `2025-02-25` Δ+50d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ+54d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+57d | target: `China` | status: `modified` | note: increased from 10%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 67 · Episode 81

**Episode first-post date**: 2025-10-01

**Episode first-post text** (EN):
> The Soybean Farmers of our Country are being hurt because China is, for "negotiating" reasons only, not buying. We've made so much money on Tariffs, that we are going to take a small portion of that money, and help our Farmers. I WILL NEVER LET OUR FARMERS DOWN! Sleepy Joe Biden didn't enforce our Agreement with China, where they were going to purchase Billions of Dollars of our Farm Product, but Soybeans, in particular. It's all going to work out very well. I LOVE OUR PATRIOTS, AND EVERY FARMER IS EXACTLY THAT! I'll be meeting with President Xi, of China, in four weeks, and Soybeans will be a major topic of discussion. MAKE SOYBEANS, AND OTHER ROW CROPS, GREAT AGAIN!

**ZH 翻译**:
> 我们国家的大豆农民正在遭受损失，因为中国出于所谓"谈判"目的，故意停止采购。我们从关税（Tariff）上已经赚了那么多钱，现在要拿出一小部分，来帮助我们的农民。**我绝对不会让我们的农民失望！** 瞌睡乔·拜登根本没有执行我们跟中国签的协议——那个协议要求他们购买数十亿美元的美国农产品，尤其是大豆。这一切最终都会有个好结果的。**我爱我们的爱国者，每一个农民都是爱国者！** 四周后我将与中国习主席会面，大豆将是【重大】议题之一。**让大豆和其他大田作物再次伟大！**

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ-1d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ-1d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+0d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+9d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+29d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+44d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 68 · Episode 92

**Episode first-post date**: 2026-01-12

**Episode first-post text** (EN):
> Effective immediately, any Country doing business with the Islamic Republic of Iran will pay a Tariff of 25% on any and all business being done with the United States of America. This Order is final and conclusive. Thank you for your attention to this matter!PRESIDENT DONALD J. TRUMP

**ZH 翻译**:
> 即刻起，任何与伊斯兰共和国伊朗有业务往来的国家，在与美利坚合众国进行任何及所有交易时，都将被征收25%的关税（Tariff）。此命令是最终且不可撤销的。感谢你们关注此事！美国总统唐纳德·J·特朗普

**Candidate events in [-10d, +60d] window:**

- **[35]** `2026-01-14` Δ+2d | target: `semiconductors` | status: `in_effect` | note: advanced computing chips
- **[36]** `2026-01-17` Δ+5d | target: `8_european_countries` | status: `withdrawn` | note: Greenland Crisis; retracted Jan 21
- **[37]** `2026-02-02` Δ+21d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+39d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+39d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+58d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 69 · Episode 28

**Episode first-post date**: 2025-03-04

**Episode first-post text** (EN):
> IF COMPANIES MOVE TO THE UNITED STATES, THERE ARE NO TARIFFS!!!

**ZH 翻译**:
> 如果公司迁移到美国，就没有关税！！！

**Candidate events in [-10d, +60d] window:**

- **[7]** `2025-02-25` Δ-7d | target: `copper` | status: `investigation` | note: investigation due Nov 22 2025
- **[8]** `2025-03-01` Δ-3d | target: `lumber` | status: `investigation` | note: investigation due Nov 26 2025
- **[9]** `2025-03-04` Δ+0d | target: `China` | status: `modified` | note: increased from 10%
- **[10]** `2025-04-02` Δ+29d | target: `all_countries` | status: `struck_down` | note: Liberation Day universal baseline
- **[11]** `2025-04-02` Δ+29d | target: `China_HK_de_minimis` | status: `modified` | note: EO 14256 closed exemption
- **[12]** `2025-04-03` Δ+30d | target: `autos` | status: `in_effect` | note: applied to USMCA partners
- **[13]** `2025-04-04` Δ+31d | target: `aluminum_cans_beer` | status: `in_effect` | note: aluminum tariff expansion
- **[14]** `2025-04-09` Δ+36d | target: `57_countries` | status: `paused` | note: paused for 90 days, except China
- **[15]** `2025-04-09` Δ+36d | target: `China` | status: `modified` | note: retaliatory escalation
- **[16]** `2025-04-22` Δ+49d | target: `heavy_trucks_buses` | status: `in_effect` | note: investigation due Jan 16 2026
- **[17]** `2025-04-29` Δ+56d | target: `tariff_stacking` | status: `in_effect` | note: hierarchy preventing overlap
- **[18]** `2025-05-03` Δ+60d | target: `auto_parts` | status: `in_effect` | note: USMCA parts exempted

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 70 · Episode 101

**Episode first-post date**: 2026-02-21

**Episode first-post text** (EN):
> Those members of the Supreme Court who voted against our very acceptable and proper method of TARIFFS should be ashamed of themselves. Their decision was ridiculous but, now the adjustment process begins, and we will do everything possible to take in even more money than we were taking in before!

**ZH 翻译**:
> 那些在最高法院投票反对我们完全合理、完全正当的**关税（TARIFFS）**征收方式的法官，应该为自己感到羞耻。他们的裁决荒唐透顶，但是，现在调整过程开始了，我们会尽一切可能，征收比以前**更多**的钱！

**Candidate events in [-10d, +60d] window:**

- **[38]** `2026-02-20` Δ-1d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ-1d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+18d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation
- **[41]** `2026-04-02` Δ+40d | target: `metal_products_clarified` | status: `modified` | note: tier-based clarification
- **[42]** `2026-04-02` Δ+40d | target: `pharmaceuticals_patented` | status: `in_effect` | note: lower rates for EU/Japan/Korea/Switzerland (15%), UK (10%); generics exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 71 · Episode 76

**Episode first-post date**: 2025-09-25

**Episode first-post text** (EN):
> In order to protect our Great Heavy Truck Manufacturers from unfair outside competition, I will be imposing, as of October 1st, 2025, a 25% Tariff on all "Heavy (Big!) Trucks" made in other parts of the World. Therefore, our Great Large Truck Company Manufacturers, such as Peterbilt, Kenworth, Freightliner, Mack Trucks, and others, will be protected from the onslaught of outside interruptions. We need our Truckers to be financially healthy and strong, for many reasons, but above all else, for National Security purposes!

**ZH 翻译**:
> 为了保护我们【伟大的】重型卡车制造商免受不公平的外部竞争，我将从2025年10月1日起，对世界其他地方生产的所有"重型（大块头！）卡车"征收25%的关税（Tariff）！因此，我们【伟大的】大型卡车制造商，比如Peterbilt、Kenworth、Freightliner、Mack Trucks等等，将受到保护，免遭外部冲击的猛烈侵袭！我们需要我们的卡车行业在财务上保持健康和强壮，原因很多，但最最重要的，是为了**国家安全**！

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ+5d | target: `lumber` | status: `in_effect` | note: softwood
- **[28]** `2025-09-30` Δ+5d | target: `furniture_cabinets` | status: `in_effect` | note: delayed increases paused to Jan 2027
- **[29]** `2025-10-01` Δ+6d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+15d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+35d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+50d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 72 · Episode 100

**Episode first-post date**: 2026-02-02

**Episode first-post text** (EN):
> It was an Honor to speak with Prime Minister Modi, of India, this morning. He is one of my greatest friends and, a Powerful and Respected Leader of his Country. We spoke about many things, including Trade, and ending the War with Russia and Ukraine. He agreed to stop buying Russian Oil, and to buy much more from the United States and, potentially, Venezuela. This will help END THE WAR in Ukraine, which is taking place right now, with thousands of people dying each and every week! Out of friendship and respect for Prime Minister Modi and, as per his request, effective immediately, we agreed to a Trade Deal between the United States and India, whereby the United States will charge a reduced Reciprocal Tariff, lowering it from 25% to 18%. They will likewise move forward to reduce their Tariffs and Non Tariff Barriers against the United States, to ZERO. The Prime Minister also committed to "BUY AMERICAN," at a much higher level, in addition to over $500 BILLION DOLLARS of U.S. Energy, Tech

**ZH 翻译**:
> 今天早上能与印度总理莫迪通话，是我的荣幸。他是我最好的朋友之一，是他国家一位**强有力、备受尊敬**的领导人。我们谈了很多事情，包括贸易，以及结束俄乌战争。他同意停止购买俄罗斯石油，转而从美国购买更多石油，还有可能从委内瑞拉购买。这将有助于【终结】乌克兰的战争——那场战争就在眼前，每周都有成千上万的人在死去！出于对莫迪总理的友谊和尊重，也应他的请求，我们即时生效地达成了一项美印贸易协议，美国将征收降低后的对等关税（Reciprocal Tariff），从25%降至18%。印度同样也将推进把他们对美国的关税及非关税壁垒（Non Tariff Barriers）降至【零】。总理还承诺"买美国货"，采购量将大幅提升，此外还有超过**5000亿美元**的美国能源、科技、农产品、煤炭及其他众多产品。我们与印度**了不起的**关系将在未来变得更加牢固。莫迪总理和我，都是那种【把事情办成】的人——这可不是谁都能说的！感谢你们关注此事！美利坚合众国总统 唐纳德·J·特朗普

**Candidate events in [-10d, +60d] window:**

- **[37]** `2026-02-02` Δ+0d | target: `India` | status: `modified` | note: reduced from 50%
- **[38]** `2026-02-20` Δ+18d | target: `IEEPA_tariffs` | status: `struck_down` | note: Learning Resources v. Trump; $166B refund
- **[39]** `2026-02-20` Δ+18d | target: `global` | status: `in_effect` | note: replacement for IEEPA; expires ~150 days
- **[40]** `2026-03-11` Δ+37d | target: `16_countries_excess_capacity` | status: `investigation` | note: China, EU, Asia investigation
- **[41]** `2026-04-02` Δ+59d | target: `metal_products_clarified` | status: `modified` | note: tier-based clarification
- **[42]** `2026-04-02` Δ+59d | target: `pharmaceuticals_patented` | status: `in_effect` | note: lower rates for EU/Japan/Korea/Switzerland (15%), UK (10%); generics exempt

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 73 · Episode 85

**Episode first-post date**: 2025-11-10

**Episode first-post text** (EN):
> All money left over from the $2000 payments made to low and middle income USA Citizens, from the massive Tariff Income pouring into our Country from foreign countries, which will be substantial, will be used to SUBSTANTIALLY PAY DOWN NATIONAL DEBT. Thank you for your attention to this matter! President DJT

**ZH 翻译**:
> 从外国大量涌入我国的【巨额】关税（Tariff）收入中，拨出2000美元发给美国中低收入公民之后，所有剩余资金——这将是一笔**相当可观**的数目——将用于**大幅**偿还国家债务。感谢您关注此事！总统 DJT

**Candidate events in [-10d, +60d] window:**

- **[32]** `2025-11-14` Δ+4d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits
- **[33]** `2025-12-01` Δ+21d | target: `UK_pharmaceuticals` | status: `in_effect` | note: first major reduction agreement
- **[34]** `2026-01-01` Δ+52d | target: `wooden_furniture` | status: `in_effect` | note: increased from 25%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 74 · Episode 64

**Episode first-post date**: 2025-07-08

**Episode first-post text** (EN):
> As per letters sent to various countries yesterday, in addition to letters that will be sent today, tomorrow, and for the next short period of time, TARIFFS WILL START BEING PAID ON AUGUST 1, 2025. There has been no change to this date, and there will be no change. In other words, all money will be due and payable starting AUGUST 1, 2025 - No extensions will be granted. Thank you for your attention to this matter!

**ZH 翻译**:
> 根据昨天向各国发出的信函，以及今天、明天和接下来这段时间将陆续发出的信函，**关税（TARIFFS）将从2025年8月1日起开始征收**。这个日期没有任何变化，也不会有任何变化。换句话说，所有款项将从**2025年8月1日**起到期并须全额缴纳——【不会给予任何延期】。感谢你们关注此事！

**Candidate events in [-10d, +60d] window:**

- **[21]** `2025-07-04` Δ-4d | target: `global_de_minimis` | status: `in_effect` | note: Big Beautiful Bill Act; accelerated
- **[22]** `2025-07-08` Δ+0d | target: `copper` | status: `in_effect` | note: raw materials exempt
- **[23]** `2025-07-08` Δ+0d | target: `pharmaceuticals` | status: `modified` | note: originally threatened 200%, finally 100% Apr 2026
- **[24]** `2025-07-30` Δ+22d | target: `Brazil` | status: `in_effect` | note: Bolsonaro penalty
- **[25]** `2025-08-19` Δ+42d | target: `407_metal_products` | status: `in_effect` | note: construction materials, furniture
- **[26]** `2025-08-27` Δ+50d | target: `India` | status: `modified` | note: Russia oil penalty; later reduced to 18%

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---

## Case 75 · Episode 80

**Episode first-post date**: 2025-09-29

**Episode first-post text** (EN):
> In order to make North Carolina, which has completely lost its furniture business to China, and other Countries, GREAT again, I will be imposing substantial Tariffs on any Country that does not make its furniture in the United States. Details to follow!!! President DJT

**ZH 翻译**:
> 为了让北卡罗来纳州——那个把家具生意【完全】拱手让给中国和其他国家的地方——再次**伟大**，我将对所有不在美国本土生产家具的国家征收**巨额**关税（Tariff）。详情随后公布！！！总统 DJT

**Candidate events in [-10d, +60d] window:**

- **[27]** `2025-09-30` Δ+1d | target: `lumber` | status: `in_effect` | note: softwood
- **[29]** `2025-10-01` Δ+2d | target: `pharmaceuticals_branded` | status: `modified` | note: exemption for US-manufacturers; some at 15%
- **[30]** `2025-10-10` Δ+11d | target: `China_additional` | status: `withdrawn` | note: threatened 100% retaliation, withdrawn
- **[31]** `2025-10-30` Δ+31d | target: `China_fentanyl` | status: `modified` | note: reduced fentanyl tariff to 10%
- **[32]** `2025-11-14` Δ+46d | target: `agricultural_products` | status: `modified` | note: exemptions: coffee, tea, tropical fruits

**Your pick**: `[N]` / `tie [N]/[M]` / `none` → __

**Notes**: __

---
