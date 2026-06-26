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
- (无 trim 动作；已完成 +25 refs，待 S2 Codex 验证)

## 待办
- 全部 S1–S9。
