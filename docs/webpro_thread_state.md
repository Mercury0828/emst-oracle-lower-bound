# GPT-5.5-Pro thread — running state (EMST range-counting-oracle query complexity)

> **The single source of truth for the human-relayed GPT-5.5-Pro conversation.** Re-read this before
> composing or relaying any Pro round — never work the Pro thread from memory. Frozen facts are
> append-only. Modeled on the archiving convention of the `dynamic-weighted-mis-fat-objects` project
> (`docs/caching_thread_state.md`). Sister ledgers: the main research lines
> `research_line_emst_upper.md` (upper bound, active) and `research_line_emst.md` (lower bound, frozen);
> the codex (xhigh) attack rounds live in `attack_loop/`. This file tracks the **Pro** thread only.

---

## 📋 ARCHIVING CONVENTION (how this thread is kept — follow it every round)

1. **This file = the living ledger.** HEADLINE + Status (dated), per-round log, frozen Model/bounds,
   our (fallible, AI-derived) findings, the open problem, confidence trend, Artifacts. Update it the
   moment a round closes; never edit old frozen entries (append CORRECTIONs instead).
2. **One file per Pro round artifact**, named `webpro_round{N}_{brief|response|audit}.md`:
   - `…_brief.md` — exactly what we send Pro (method-free: raw problem first; our findings demoted to a
     fallible, optional appendix — see the brief rails below).
   - `…_response.md` — Pro's reply **pasted verbatim by the human** (Pro is human-relayed; we never
     fabricate or paraphrase its words).
   - `…_audit.md` — our independent fresh-context adversarial audit of Pro's reply (classify
     FATAL/GAP/MINOR; for an algorithm hunt a smuggled √n / unbounded variance / floor violation /
     non-implementable primitive; for a lower bound hunt evasion-of-vise failure / Ω(log) mis-packaging).
   - (round 1's brief currently lives at `attack_loop/escalation_webpro_brief.md` — the link already
     given to the owner; treat it as `webpro_round1_brief`. Round-2 onward use `docs/webpro_round{N}_…`.)
3. **Brief rails (freeze FACTS, free METHODS; per owner: give the RAW problem, our claims are fallible).**
   - Lead with the original open problem, self-sufficient; Pro should be able to solve from it alone.
   - Our findings go in a clearly-labeled **optional, UNVERIFIED, "may be wrong"** appendix — separate
     *published* facts (source paper) from *our* AI-derived claims; invite Pro to ignore/contradict.
   - Never smuggle unproven implications (no "O(1) bits ⇒ lower bound" Ω(log) trap; no "emptiness Ω(√n)
     ⇒ counting bound"). Never present an AI-derived claim as established.
4. **After every Pro reply:** save `…_response.md`; run an independent audit → `…_audit.md`; update this
   ledger (HEADLINE/Status/findings/confidence + Artifacts); decide continue / rebattle / converge / stop.
5. **Convergence (→ human gate #2):** Pro claims closure + ≥3 independent clean audits + only verification
   debt remaining. "AI-verified ≠ proved" — then HUMAN-expert verification, full writeup, novelty sweep.

---

## ⚑ HEADLINE (2026-06-21) — Round 5: CONSOLIDATED closure proof; ✅ §9.4 AI-CONVERGENCE REACHED → human gate #2
GPT-5.5-Pro round 5 (`webpro_round5_response.md`) (i) **CONFIRMED the c_j fix** (Var(Z)=M_jc_j−c_j²≤M_jc_j;
N_j irrelevant to the trial count), (ii) caught + fixed one further subtlety — the EXPLORATION cost does
use N_j, but N_j≤K + the fine-scale bound make that sum ALSO Õ(√K), (iii) produced the **full clean,
self-contained proof** (final Lemma 3 + final Õ_ε(n^{1/3}) Theorem + the whole assembly), (iv) isolated
the verification debt to essentially ONE inherited item: the **local-WSPD death-time implementation**
(source Lemmas 23–24; conf 0.89); everything else 0.95–0.995; **full theorem 0.91**.
- **✅ §9.4 AI-CONVERGENCE REACHED.** FINAL audit by **codex GPT-5.5-xhigh** (Claude audits were blocked by
  an Anthropic 529 overload; codex uses OpenAI auth — ⚠️ CAVEAT: SAME family as Pro, so a cross-model
  Claude round-5 audit is still OWED as belt-and-suspenders) → `docs/webpro_round5_auditFinal_codex.md`:
  **verdict (CONVERGED)**, all 6 items VALID (only MINOR nits: the r_0=h omitted-interval case-split;
  floor-scale adjacency wording), **NO new counterexample** (re-hunted carpet N_j=Θ(K), satellites,
  hidden one-cell, loose interleaving, active-cover degeneration, exploration blowup), residual = the
  local-WSPD death-time impl + routine bookkeeping, conf **~0.80**.
- **codex RESOLVED the orchestrator's botched numeric:** it isolated the POLYNOMIAL CORES (candidate K/b,
  exploration Kδ/W_Q) — both O(√K); the raw `webpro_verify_round5.py` SUM was obscured by T²/α²/M_j
  polylog+const factors (a misnormalization, not a leak). **Orchestrator then confirmed both cores by
  EXECUTION** (`webpro_verify_round5_cores.py`, K=272..4160): (K/b)/√K=0.97–0.99, (Kδ/W_Q)/√K∈[0.41,0.62]
  (flat) ⇒ both cores √K, NO n^{2/3} leak. The genuinely-new round-5 N_j-exploration term is sound.
- **3 independent clean audits now stand:** round-4 cost (Claude, candidate-root √K), round-4 assembly
  (Claude, sound + caught the c_j fix), round-5 final (codex, CONVERGED + both cores √K). No FATAL, no
  counterexample anywhere. Pro claims closure; residual is verification debt only ⇒ §9.4 convergence met.
- **→ HUMAN GATE #2 (next):** (a) [optional belt-and-suspenders] a cross-model Claude round-5 audit once
  the API is healthy; (b) **human-expert verification** (esp. the WSPD death-time impl + the full Lemma 3
  query accounting); (c) full formal writeup (`venue-prompts/soda/`); (d) final 2025–26 preprint priority
  sweep; (e) own-work dedup re-check. 🔴 "AI-verified ≠ proved" — CANDIDATE closure of a PUBLISHED open
  problem; NOT proved until a human referee checks it (the round-2→3 self-refutation is why we hold this
  line). **Confidence the full closure holds: ~80% (ours, post-convergence), 0.91 (Pro).**

## ⚑ HEADLINE (2026-06-21) — Round 4: NEW repair (spatial-cell estimator) DEFEATS the round-3 counterexample (verified); cost verified
GPT-5.5-Pro round 4 (`webpro_round4_response.md`) replaces the broken seed-reuse with a **new primitive:
sample SPATIAL candidate cells (INCLUDING EMPTY ones) uniformly within an active cover, run the
random-leader estimator on occupied ones** (Z∈{0,M}, E[Z]=c, Var(Z)≤M·c). The active-cover packing
W_Q=Ω(b·δ) turns the variance into a δ/r cost summing geometrically to √K. **§10:** a rare feature can be
support-mass-rare OR spatially-hidden-at-its-scale, but NOT both while contributing a constant fraction —
directly defeating the satellite counterexample.
- **DECISIVE numeric test PASSED (`attack_loop/webpro_verify_round4.py`):** on the EXACT round-3 satellite
  instance, the spatial-cell estimator **recovers W_Q** (spatial_hat/W_Q = 1.07/0.98/1.08 for s=32/64/96),
  **recovering the 67% satellite tail that point-sampling MISSED.** The new primitive works where
  seed-reuse failed. Empty-cell leader identity E[Z]=c, Var≈M·c confirmed.
- **🔴 NOT declaring closure (round-2 lesson: 3 audits passed a closure that round 3 broke).** The
  RECOVERY is verified, but the **COST accounting (§6–§8: does Σ_j M_jU_j/α_j² genuinely = Õ(√K)?)** is
  exactly where the prior failure hid (a cost/variance blowup, not a recovery error) — so it gets the
  hardest scrutiny.
- **✅ COST AUDIT DONE (`webpro_round4_auditCost.md`): the cost genuinely closes at Õ(√K)=Õ(n^{1/3}); NO
  hidden n^{2/3} blowup. Confidence 0.88.** It BUILT the cost test the recovery test skipped and ran it on
  the EXACT satellite instance that broke round 2: packing W_Q≥Ω(bδ) VALID; Var(Z)≤M·c VALID; the
  per-scale budget Σ M_jU_j/α_j² collapses to T²·δ/r_j (bounded, since b·δ/G=0.67–0.75) and sums to √K —
  the polylog-stripped core scales as **n^{0.28–0.32} ≤ n^{1/3}** (round-2's n^{0.667} definitively NOT
  present). Structural reason: cost is charged to SPATIAL cells (emptiness=cheap P-counts), and the n/K
  support-sampling enters ADDITIVELY (§9, once), never multiplied into the per-scale sum. **The exact
  round-2 failure mode is resolved.**
- **✅ ASSEMBLY + COUNTEREXAMPLE-HUNT AUDIT DONE (`webpro_round4_auditAsm.md`), confidence 0.80:**
  interleaving (§2), Riemann (§7), W-search/K-estimation (§8/§9), §11 insertion = ALL VALID (13 scripts,
  K to 256×). **Counterexample hunt: NO new counterexample** (thin-line, grid, fractal/Cantor,
  multiscale-satellites all fail to break it; recovery 1.0–1.17 even when the rare component is 1 cell;
  leader identity exact). **ONE fixable WRITE-UP gap (not fatal, not a leak):** Pro's eqs (2)/(3)/(8)
  bound the variance via the OCCUPIED-CELL count N_j (≈Θ(√K)·W_Q/(σr_j) at the a=h floor — that WOULD be
  the round-2 n^{2/3} leak), but the TRUE leader variance is M_j·**c_j** (COMPONENT count), and
  c_j ≤ C(1+W_Q/(σr_j)) IS true (ratio ≤0.15, flat in K). **Fix = state the variance with c_j, not N_j;**
  recomputed, the cost is genuinely Õ(√K) (consistent with the cost audit). No FATAL.

### ⚑ ROUND-4 CONSOLIDATED VERDICT — STRONG closure candidate (far stronger than round 2)
recovery VERIFIED (defeats the round-3 counterexample), cost VERIFIED Õ(√K)=Õ(n^{1/3}) **on the exact
failure mode**, assembly SOUND, NO new counterexample after a hard hunt, ONE trivial write-up fix (c_j vs
N_j). Self-contained now (no 20-yr-old engine import). This is essentially **AI-convergence modulo the
c_j write-up fix + human-expert verification** → heading to **human gate #2**. 🔴 Still a CANDIDATE
closure of a PUBLISHED open problem — NOT proved until a human referee checks Lemma 3.
- **Confidence:** full Õ_ε(n^{1/3}) closure **~78%** (recovery+cost+assembly all verified; residual =
  the c_j write-up + human verification). Round-1 partial result solid.
- **Next:** round 5 = a FINISHING request to Pro (incorporate the c_j fix; produce the final clean,
  self-contained Lemma 3 + theorem statement for human verification) → one final independent audit → §9.4
  AI-convergence → human gate #2 (human-expert verification + final preprint priority sweep + writeup).
  Brief `docs/webpro_round5_brief.md`.

## ⚑ HEADLINE (2026-06-21) — Round 3: the round-2 CLOSURE is REFUTED (by Pro itself; numerically confirmed)
🔴 **The round-2 "unconditional Õ_ε(n^{1/3})" closure is NOT valid.** A fresh GPT-5.5-Pro pass (round 3,
`webpro_round3_response.md`) refuted its own round-2 claim, and the orchestrator **numerically confirmed
the refutation** (`attack_loop/webpro_verify_round3_counterexample.py`):
- **The seed-reuse trick is unsound.** Estimating `w(MST(Q))` for the K-point support via the sampling
  estimator has the SAME rare-high-value structure (a few long "satellite" edges); a polylog shared pool
  gives per-run relative error 0.28→0.68 (GROWING with K; 63–100% of single runs off by >10%), even √K
  samples give ~0.47 — you need **Ω(√K) samples**, costing `√K·(n/K)=n^{2/3}`, NOT n^{1/3}. Pro's
  dense-grid + rare-satellites counterexample is correct.
- **The [1]-Theorem-30 repair also fails:** range-COUNT on Q ≠ range-count on P (emptiness yes, exact
  count no), and [1] Thm 30's "few seeds" hides Algorithm 1's Θ̃(√K) occupied-cell sampler.
- 🔴 **My 3 round-2 audits (A/B/C) were OVER-CONFIDENT** — they accepted the seed-reuse as sound (Audit B
  even claimed "Czumaj draws O(1) vertices/threshold"); they MISSED that the support's own MST has a rare
  long-edge tail defeating polylog sampling. Honest lesson logged (the same "AI conclusion may be wrong"
  failure the owner repeatedly flagged — it applies to our AUDITS too, not just briefs).
- **What SURVIVES:** the **round-1 partial result stands** (instance-sensitive Õ(n/N_eff) = Õ(n^{1/3})
  for non-tail-heavy instances — verified, unaffected). The FULL Õ(n^{1/3}) closure is **OPEN AGAIN**,
  reduced to the sharper **Lemma 3** (Pro §6): estimate `w(MST(Q))` for an implicit K-point grid support
  in `Õ(√K+n/K)` given emptiness=1-P-count + sampling=Õ(n/K) + local-adjacency=polylog — which NO
  published engine provides; the heavy-tail difficulty has RECURSED onto the support. Repair direction
  (Pro §5/§6): a SPATIAL active-block subdivision finds the rare components via range-EMPTINESS (cheap on
  P) instead of √K expensive samples — plausible but unproven. **Confidence the full closure exists +
  is findable: dropped to ~40%; the round-1 o(√n)-for-non-tail-heavy is solid.**
- **Next:** round 4 to Pro on the sharper Lemma 3 (spatial-first), OR consolidate the round-1 partial
  result. Owner decision (the Pro cadence is owner-relayed). Brief `docs/webpro_round4_brief.md` prepared.

## ⚑ HEADLINE (2026-06-21) — Round 2: GPT-5.5-Pro CLAIMED CLOSURE (unconditional Õ_ε(n^{1/3})) — REFUTED in round 3
Pro's round-2 reply (`webpro_round2_response.md`) **claims to close the heavy-tail lemma and therefore
the whole gap from above: an unconditional `Õ_ε(n^{1/3})` algorithm** ⇒ Ω(n^{1/3}) tight up to polylog.
Mechanism: (i) **support-regularize** to K=Θ_ε(n^{2/3}) occupied cells (Lemma 1 packing K_h≤8W/h+4);
(ii) snapping preserves the tail (Lemma 2 interleaving) and W_Q=O(W); (iii) run **Czumaj's spread-
independent Õ(√K) MST estimator** on the support, with the source's **WSPD spanner replacing Czumaj's
Yao graph** in the range-counting model (Lemma 3 — Pro's own confidence 0.84, the load-bearing risk);
(iv) the **seed-reuse trick** (one polylog pool of uniform support seeds reused across all thresholds) so
the n/K=n^{1/3} sampling is invoked only polylog times, avoiding the √K·(n/K)=n^{2/3} blowup; (v) heavy
tail B̂_L=Ŵ_Q−Â_Q; (vi) a geometric search removes knowing W. Total Õ_ε(n/K_0+√K+n/K)=**Õ_ε(n^{1/3})**.
- **Numerically VERIFIED (orchestrator, `attack_loop/webpro_verify_round2.py`):** Lemma 1 (packing),
  Lemma 2 (interleaving), and snapping-preserves-B_L (|ΔB|/W ≤ 0.004, shrinking with h) — ALL HOLD.
- **3 INDEPENDENT blind adversarial audits RUNNING** (per the claimed-closure protocol):
  **A** = Lemma 3 / Czumaj-import / WSPD-in-range-counting (the deepest risk; fetch [2] + source Lemmas
  21–24); **B** = the seed-reuse + variance/concentration + the B̂_L=Ŵ_Q−Â_Q subtraction + W-search;
  **C** = overall assembly + lemma-proof rigor + adversarial √n / counterexample hunt.
  → `webpro_round2_audit{A,B,C}.md`. 🔴 CANDIDATE closure of a published open problem — NOT proved until
  human-expert verified.

### ⚑ 3-AUDIT CONSOLIDATED VERDICT (all blind, all in) — REDUCTION SOUND; ONE fixable Lemma-3 GAP; NO FATAL
- **Audit A (Lemma 3 / Czumaj import): NEEDS-REPAIR, 0.78 (0.82 repaired).** The defect is a proof gap,
  NOT a complexity leak: Pro imported Czumaj's *non-orthogonal* (cone-NN) engine then "replaced" the Yao
  graph with WSPD; the "restrict a query to a non-rectangular block-component ⇒ one range-count" step is
  ASSERTED, not proved. **Clean repair (read both PDFs):** the source's OWN **Theorem 30 already proves
  Õ(√n) MST-weight estimation NATIVELY in the orthogonal-range-counting model** (Lemmas 21–24 = polylog
  WSPD-degree + local-adjacency-by-range-count); apply [1] Thm 30 to the support Q (each Q-query = one
  P-query, §2). Drops Czumaj; no √n leak. Numerics pass (WSPD MST ≤(1+ρ); snap W_Q/W=0.90).
- **Audit B (seed-reuse / variance / W-search): SOUND, 0.85.** Czumaj's component estimator cost is
  vertex-count-INDEPENDENT (draws O_η(1) seeds/threshold), so reuse of one O(log T) pool genuinely
  avoids the √K·(n/K)=n^{2/3} blowup. Nuance: §4's "cross-threshold independence unnecessary" is true
  but insufficient (naive integration of reused-seed counts telescopes to the raw death-time estimator,
  ~7–8× tail blow-up); the closure survives because the SUM is built via the §5 CLIP at L + §6 relative
  estimator + subtraction, not the bare §4 argument (a presentation fix). Clipped variance, subtraction,
  W-search, K_h estimation ALL VALID. Only a Lemma-3-internal probabilistic failure could remain.
- **Audit C (assembly + lemmas + √n hunt): SOUND reduction, 0.97; complete-closure 0.62.** Lemmas 1/2,
  snapping, W_Q=O(W), the B̂_L=Ŵ_Q−Â_Q assembly (reconstructs W to <1e-4 incl. the round-1-killing
  bridge), the additive error budget, the seed-reuse — all verified. **Adversarial hunt: NO
  counterexample; "the reduction is unbreakable."** Same single GAP = Lemma-3 query accounting.
- **NET:** 3 independent blind audits + orchestrator numerics ⇒ the result is **very likely TRUE**; the
  reduction is SOUND; the ONLY unresolved item is **Lemma 3's query accounting AS WRITTEN**, with a
  precise, agreed repair (use [1] Thm 30 natively). No FATAL, no counterexample, no √n leak. **NOT yet
  §9.4-converged** (one open GAP). **Next = round 3 to Pro: repair Lemma 3 + the §4/stage-2 wording,**
  then re-audit the repaired Lemma 3 → if clean ⇒ convergence ⇒ human gate #2.

## ⚑ HEADLINE (2026-06-21) — Round 1 RETURNED: major advance; our `U-N4` obstruction REFUTED (verified)
GPT-5.5-Pro's round-1 reply (`webpro_round1_response.md`) is excellent and **its load-bearing claims are
numerically VERIFIED** (`attack_loop/webpro_verify_round1.py`):
1. **`U-N4` (our "cheap connectivity from counts is the crux") is FALSE.** A **random-leader /
   minimum-rank exploration** estimates `1/|C_λ(p)|` unbiasedly in **O(log s)** expected vertex
   inspections (stop the moment a lower-ranked vertex appears) — verified empirically (2.9–7.8 for
   s=10–1000, not s). Our "exploring a component costs its size" was WRONG. The source's CellSampling
   `Ω(√n)` is simply unnecessary for this estimator.
2. **Exact multiset identity (Pro Lemma 1):** with random ranks, the "death times" `τ(v)` satisfy
   `{τ(v):v≠r} = {MST edge weights}` EXACTLY (verified, max error 0.0). ⇒ a uniform vertex + a
   bottleneck-Dijkstra search returns a **uniformly random MST-edge weight** in `O(log n)` expected
   expansions, implementable in **Õ_ε(1) range queries per sample** (WSPD machinery).
3. **A real instance-sensitive PARTIAL RESULT:** `Õ_ε(n/N_eff)` queries, `N_eff = W²/Σ_e ℓ_e²` =
   "effective #MST edges"; this is `o(√n)` whenever `N_eff = ω(√n)`, and **`Õ(n^{1/3})`** whenever
   `ℓ_max ≤ W/n^{2/3}` (MST weight not concentrated on a few long edges).
4. **Remaining obstruction precisely isolated = the HEAVY TAIL.** Split at `L=W_H/n^{2/3}`: the bulk
   `A_L=Σ min{w_e,L}` is estimable in `Õ(n^{1/3})`; only `B_L=Σ(w_e−L)_+` over `≤ n^{2/3}` long edges
   remains. The hard instance (two grids + one `Θ(n)` bridge, `N_eff=Θ(1)`, verified) shows death-time
   sampling alone needs `Ω(n)` to catch the rare bridge — the source's `Õ(√n)` uses **spatial range
   info**, the missing ingredient. **"Heavy-tail lemma" needed:** estimate the excess of `≤ n^{2/3}`
   long MST edges above `L` to additive `εW` in `Õ(n^{1/3})` range queries.
5. Pro CONFIRMS our gadget LB barrier caps at `n^{1/3}` for that template, but (rightly) flags the
   `Ω(ms)`-baseline + `O(1)`-coverage as substantive assumptions ⇒ NOT a universal `Ω(√n)` barrier.

**Confidence (big positive update):** the partial result is verified at the checkable level; an
`o(√n)`-for-non-tail-heavy-instances algorithm is essentially in hand; the FULL `Õ(n^{1/3})` now hinges
on the single, well-isolated, GEOMETRIC heavy-tail lemma (a much better-posed crux than `U-N4`).
**Independent audit DONE (`webpro_round1_audit.md`): verdict (A)** — the partial result (Õ_ε(n/N_eff),
incl. Õ(n^{1/3}) off the tail) is RIGOROUS at the checkable level; the heavy-tail lemma is correctly the
ONLY remaining gap. No FATAL; one MINOR (WSPD redundant-pair enumeration = a correctness-bookkeeping
item, not a √n leak) + one contained GAP (setting L needs a constant-factor W guess, not cheap in the
worst case — folds INTO the heavy-tail lemma's hypotheses). Independently brute-forced "Kruskal MST
minimizes Σw²" (TRUE) and re-verified the variance bounds + that the estimator dodges CellSampling Ω(√n).
**Concurs fully that our U-N4 was wrong.** Audit confidence 0.88. "AI-verified ≠ proved." Strongest state
of the project. **Next = round 2 on the heavy-tail lemma (brief `docs/webpro_round2_brief.md`).**

## Status (2026-06-21)
- **Round 1 brief sent (human relays):** `attack_loop/escalation_webpro_brief.md`. Structure: Part I =
  the raw open problem (self-sufficient); Part II = optional, UNVERIFIED context — §A published facts
  (source paper), §B our fallible findings, §C where *we* are stuck, §D routes we *believe* are dead.
- The paper-orientation verdict (independent audit `gate_paper_orientation_upper.md`): the *current*
  contribution is **NOT SODA-level standalone** (ESA/workshop-tier); it hinges on resolving the crux.
  Pro's job is exactly to resolve it (algorithm or lower bound), or to overturn our framing.

---

## Model (frozen, reliable)
Points `P ⊂ [Δ]²` integer grid, `|P|=n`, spread `Δ=O(n)`. Oracle = orthogonal range-COUNTING: query a
rectangle `R`, get the exact integer `|P∩R|`. Goal: a randomized `(1±ε)`-multiplicative estimate of
`w(MST(P))` (Euclidean MST weight), constant success prob, minimizing queries.

## Known bounds (frozen, reliable — from the source paper)
- **Upper `Õ(√n)`** (Driemel–Monemizadeh–Oh–Staals–Woodruff, "Range Counting Oracles for Geometric
  Problems," SoCG 2025, arXiv:2504.15292, Thm 30).
- **Lower `Ω(n^{1/3})`** (same, Lemma 32). **Gap open.** Cluster-count identity used by the source:
  `w(MST)=(n−Δ)+Σ_i λ_i c(λ_i)=∫(c(t)−1)dt`, `c(λ)=#single-linkage components at threshold λ`.
- The source's `Õ(√n)` is bottlenecked by a **cell-sampling `Ω(√n)`** sub-primitive (their §4, even 1-D).

## Our findings so far (⚠️ AI-DERIVED — codex + AI audits + small numerics — NOT human-verified; may be
## wrong; pointers into the research-line ledgers)
*These are carried from `research_line_emst.md` / `research_line_emst_upper.md`. They are the substance
of Part II of the brief. Each MAY be mistaken; we present them to Pro as fallible hypotheses, not facts.*
- **`P1`/`P2` (LB barrier, ~near-proof):** the gadget-packing lower-bound technique seems to cap at
  `n^{1/3}` (single-cell swap ≤ O(s√p), backbone ≥ Ω(sm), `s` cancels; multi-needle caps too under O(1)
  coverage). A loophole remains; a `√n` LB by a different mechanism is not excluded.
- **`U-P5` (reduction, conditional):** IF a `polylog` range-counting primitive for `1/|C_λ(p)|` /
  `c(λ)` exists, THEN `min(n/c,√c)≤n^{1/3}` ⇒ `Õ(n^{1/3})`. **(Corrected: this is a reduction to an
  open primitive, NOT a "proven cost model" — an earlier over-claim, now fixed.)**
- **`U-N4` (the crux):** cheap connectivity from additive counts — estimate `|C_λ(p)|` / `c(λ)` in
  `polylog`/`o(√n)` queries. Naive primitives provably fail in our hands. This is where codex plateaued.
- **spread-vs-concentrate (numerical intuition):** a constant-fraction weight gap seems coarsely
  countable ⇒ *suggests* no `√n` LB from a hidden needle. Numerics only; could be wrong.
- **`U-P1` (suggestive):** cell-sampling `Ω(√n)` does not obviously transfer to the weight (1-D weight is
  occupancy-invariant). A pattern in examples, not a theorem.

## Refuted routes we report to Pro (⚠️ reasons are AI-derived; Pro may overturn)
single-needle & active-subset multi-needle LB (cap n^{1/3}); CRT-with-smaller-exploration-depth (binding
cost is cell-sampling); uniform point estimator (variance √n); `c(λ)=O(n/λ)` (false, uniform grid);
Euler occupancy/adjacency totals (cycle-rank cancels). Each with its killing reason in the brief §D.

## The open problem (as posed to Pro)
PART I of the brief: settle/improve the query complexity — an `o(√n)`/`Õ(n^{1/3})` algorithm, OR a
lower bound `> Ω(n^{1/3})` (ideally `Ω(√n)`). Any method. Our own reduced crux is `U-N4`, but Pro is
explicitly free to abandon our CRT framing.

## Confidence trend (that an `o(√n)` algorithm exists; AI estimate, with dates)
- 2026-06-21: ~55% `o(√n)`, ~30% `Õ(n^{1/3})`. Leaning truth is `Θ̃(n^{1/3})` (LB capped there + the
  weight-red-herring pattern), but `U-N4` has the flavour of the cell-sampling `Ω(√n)` and could be hard.
  **These are AI estimates and may be miscalibrated.**

## Round log
- **Round 1 [2026-06-21] — DONE (major advance).** Brief `attack_loop/escalation_webpro_brief.md` →
  Pro reply `docs/webpro_round1_response.md` (verbatim) → orchestrator numeric verification
  `attack_loop/webpro_verify_round1.py` (multiset identity EXACT; exploration O(log s); rare-bridge
  confirmed) → independent audit `docs/webpro_round1_audit.md` (RUNNING). **Result:** U-N4 refuted;
  death-time estimator + instance-sensitive Õ(n/N_eff) (=Õ(n^{1/3}) off the tail); remaining crux =
  the heavy-tail lemma. **Next: round 2 brief on the heavy-tail lemma** (estimate the excess of ≤n^{2/3}
  long MST edges above L in Õ(n^{1/3}), using spatial range info) — pending the round-1 audit verdict.

- **Round 2 [2026-06-21] — DONE: CLAIMED CLOSURE.** Brief `docs/webpro_round2_brief.md` (heavy-tail
  lemma) → Pro reply `docs/webpro_round2_response.md` (verbatim; claims unconditional Õ_ε(n^{1/3})) →
  orchestrator numerics `attack_loop/webpro_verify_round2.py` (Lemmas 1,2 + snapping HOLD) → **3 blind
  audits DONE** (`webpro_round2_audit{A,B,C}.md`): REDUCTION SOUND, no FATAL, no counterexample, ONE
  fixable Lemma-3 query-accounting GAP (clean repair = use [1] Thm 30 natively).
- **Round 3 [2026-06-21] — DONE: Pro REFUTES its own round-2 closure.** Brief `docs/webpro_round3_brief.md`
  → Pro reply `docs/webpro_round3_response.md` (the [1]-Thm-30 repair fails; seed-reuse unsound; concrete
  counterexample) → orchestrator numeric confirmation `attack_loop/webpro_verify_round3_counterexample.py`
  (polylog seeds give growing per-run error 0.28→0.68; Ω(√K) samples needed). **Round-2 closure NOT
  validated; my 3 round-2 audits were over-confident. Round-1 partial result stands. Full closure open
  again (sharper Lemma 3).**
- **Round 4 [2026-06-21] — DONE: spatial-cell repair.** Brief `docs/webpro_round4_brief.md` → reply
  `docs/webpro_round4_response.md` (empty-cell SPATIAL estimator) → orchestrator recovery test PASSED
  (`webpro_verify_round4.py`) → 2 audits (`webpro_round4_auditCost.md` cost=Õ(√K) verified on the failure
  mode; `webpro_round4_auditAsm.md` assembly sound + no new counterexample + the c_j write-up fix).
- **Round 5 [2026-06-21] — DONE: consolidated proof.** Brief `docs/webpro_round5_brief.md` (c_j fix +
  clean consolidation) → reply `docs/webpro_round5_response.md` (c_j confirmed + N_j-exploration fix +
  the full self-contained Lemma 3 + Theorem + verification-debt list). → orchestrator numeric test
  drafted (`webpro_verify_round5.py`, the c_j-vs-N_j carpet) + FINAL audit (`webpro_round5_auditFinal.md`)
  queued (tooling outage; will run). If clean ⇒ §9.4 convergence ⇒ human gate #2.

## Pending for round 2 (the heavy-tail lemma — well-isolated, geometric)
> Given range-counting access to P, a threshold L=Θ(W/n^{2/3}) (and a constant-factor estimate of W),
> estimate B = Σ_{e∈MST, w_e>L} (w_e − L) to additive εW using Õ(n^{1/3}) queries. There are ≤ n^{2/3}
> such long edges; they are "long" geometrically (≥L); the death-time sampler misses them (needs spatial
> info). This is the ONLY thing between us and a worst-case Õ(n^{1/3}) (= closing the gap from above).

## Artifacts
- Round-1 brief: `attack_loop/escalation_webpro_brief.md` · Pro reply: `docs/webpro_round1_response.md`
  · numeric verification: `attack_loop/webpro_verify_round1.py` · audit: `docs/webpro_round1_audit.md`.
- Paper-orientation (independent): `gate_paper_orientation_upper.md`.
- Main research-line ledgers: `research_line_emst_upper.md` (active), `research_line_emst.md` (frozen).
- Codex (xhigh) attack rounds + audits: `attack_loop/` (`round*_C1/escape/upper_*`, `auditUC/UD_*` etc.).
