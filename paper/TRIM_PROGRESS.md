# TRIM_PROGRESS — SODA freeze-后 trim / 排版收尾

> 维护纪律：每步更新；长上下文回读本文件 + 实测 PDF 再继续。trim = 编辑不削弱（红线）：
> 不改 claim/假设/界/常数/scope，下沉证明必留"见附录 X"指针且附录有完整证明。

## 起点状态 (2026-06-25, commit 9277024)
- 42pp, 编译干净, 0 undefined, **68 refs** (43 + 25 new).
- 🔴 结构问题：前一轮"40pp push"把 Lemma 3 全证明 (app_lemma3) + §4–§5 证明 (app_assembly)
  **提进了正文**。导致 merits 被埋：
  - p3 §1.2 techniques；p9–21 = Lemma 3 全证明 accounting；p23 才出现 Main Theorem (Alg.2)；
    p30 optimality；p31 open。**前 10 页装不下 merits**（到 p11 已深陷 median-of-means 细节）。

## 前 10 页现状 vs 目标
- 现状：前 10 页 = intro + overview + prelims + 一部分 Lemma 3 证明。Main Thm / optimality 在 p23/p30。
- 目标：前 ~10–12 页 = 问题动机 + prior 表 + 形式化定理 (Lemma 3, Thm main, Cor tight) + technique
  overview + key proof sketch；**完整证明全部下沉附录**。

## 子任务清单（按 prompt 顺序，逐个执行，一步一编译）
- [ ] S1. 预-trim 写作全量复检（AI banned-token=0 / 无 limitation-future-work / 逻辑链 / 符号一致 /
      acronym 仅首次给全程 / 界回声 abstract=定理=表=concl 一致 / proof 复核）。
- [ ] S2. 🔴 引用真实性核验：自审 + **Codex 联网全量复查 68 refs**（红线=Codex，非 Claude subagent）。
      出错误清单 → 修/删。错误引用 = desk reject，最高优先级。
- [ ] S3. 🔵 R2 冷读者面板 (Codex R-W1/2/3) → 冻结 **protect-list**（§1.2 intuition / §1.1 takeaway /
      worked example / 构造图标注 / formal-block 铺垫）。BLOCKER+SHOULD-FIX 先修。
- [ ] S4. 🔴 主杠杆：把 app_lemma3 + app_assembly **下沉回附录**（reverse body-promotion）；正文 §4/§5/§6
      只留定理陈述 + sketch + 关键引理简短证明 + "见附录"指针。
- [ ] S5. 排版收尾：caption 砍到一句；图表不越单栏宽 (pdftoppm 实看)；子图横向并列压竖向；float 间距。
- [ ] S6. 复述/防御段：删只复述定理的句子（**不删定向句/protect-list**）；删任何 limitation/future-work。
- [ ] S7. 组件长度：abstract 150–200 词；Our Results ~1–2pp；§1.2/§1.3 惯常篇幅。
- [ ] S8. (仅必要) 内容删减：Codex 并行 reviewer 出 top-5 候选，按优先级逐个试。
- [ ] S9. 退出闸 R3：完整冷读者面板无 BLOCKER + 前 10 页装下 merits + protect-list 完好（JOINT 不动点）。

## 待 owner 决策
- ⚠️ S4 下沉证明会 reverse 上一轮"40pp 正文证明"。SODA trim 明确要求证明在附录。已在 plan 模式请 owner 确认。

## 已做
- +25 refs (68 total, cited, builds 42pp).
- **S1 DONE** (commit 94845b8): banned tokens 0; WSPD acronym 定义一次(§1.2)、余处 bare、删 prelims/app_wspd
  重复定义；d>=3 scope 改自信措辞；word RAM 统一。编译干净 42pp 0 undefined。
- **S3 DONE**：R2 panel = R-W1 clean / R-W2,R-W3 OK-with-notes，**无 BLOCKER**。51-item
  **protect-list 已冻结** → docs/reviews/trim_R2_panel_protectlist.md（下沉/trim 不许删这些）。
  3 个 SHOULD-FIX 已修：①overview satellite count 显式化 s=Θ(√K)、point-sample 需 Θ(K/s)=Θ(√K)；
  ②worked-example 去掉误导的 Θ(1/K0)，改用 scale candidate-universe + Lemma 3 accounting；
  ③lem:kwindow 的 window+cost 已 inline 在 §5（满足，无需重复 statement）。
- **S2 still running**（refverify web）。

## 待办
- S2 出错误清单 → 修/删 refs（先于 trim）。然后 S4 下沉证明 → S5-S7 → S9 R3。

## protect-list 摘要（trim 红线，不许删/不许精炼掉）
abstract 单行贡献+技术总结；intro §1.1 定理/tightness 单句/对比表+caption/support-lemma balance/scope;
§1.2 技术 intuition；roadmap；overview 全部 map+barrier 例+leader 实验+E/Var 推导+两部分+reduction+
WSPD map+balance/novelty；prelims model+CRT 证明+death-time view+两张表；§4 warmup+cover+leader alg+
scale-graph 图+candidate universe+additive call；§5 small map+death-time intuition+3 张图(staircase/
search/snapping)+regularization+snapping+decomposition；§6 thm+Alg+三件套+amp+k0 remark+W-search+
worked example punchline；optimality 两段+qualifiers；open EMD+cost-of-K；app_wspd WSPD 图标注。
