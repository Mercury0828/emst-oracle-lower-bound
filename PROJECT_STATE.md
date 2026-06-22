# PROJECT_STATE — emst-oracle-lower-bound

> Running state. Update every round. **Re-read this + `research_line_emst_upper.md` +
> `docs/webpro_thread_state.md` + frozen artifacts before continuing — never from memory.** Frozen
> tables are **append-only**.

---

## ❄️ COLD-START / RESUME (read this block first — frozen 2026-06-22)

**Where we are in one line:** the project PIVOTED from a lower bound to an UPPER bound and **reached
§9.4 AI-CONVERGENCE on a candidate closure**: an unconditional **Õ_ε(n^{1/3})** orthogonal-range-counting
algorithm for (1±ε)-estimating Euclidean MST weight — closing Driemel et al.'s (SoCG 2025) Õ(√n) vs
Ω(n^{1/3}) gap **from above**, tight. The proof is **AI-verified, NOT human-proved.** Next gate = human.

**To resume, read in this order:**
1. `docs/webpro_thread_state.md` — the GPT-5.5-Pro thread ledger (the math lives here; top HEADLINE = current).
2. `research_line_emst_upper.md` — the upper-bound research line (HEADLINE = converged).
3. `docs/webpro_round5_response.md` — the CONSOLIDATED self-contained proof (final Lemma 3 + Theorem).
4. This file's history below — full pivot/lower-bound trail.

**Status snapshot (frozen 2026-06-22):**
- **Result (candidate):** Õ_ε(n^{1/3}) range-counting EMST-weight estimator, matching Ω(n^{1/3}); the
  genuinely-new primitive is the **empty-cell SPATIAL leader estimator** (+ active-cover 4-coloring
  packing W_Q=Ω(bδ), support-regularization/snapping, range-counting clipped death-time estimator).
- **Verification:** 5 GPT-5.5-Pro rounds (1 self-refutation at round 2→3, repaired round 4–5) + **3
  independent clean audits** (round-4 cost & assembly [Claude, cross-model]; round-5 final [codex
  GPT-5.5-xhigh, CONVERGED]); the round-5 N_j-exploration cores (K/b, Kδ/W_Q) confirmed **O(√K) by
  execution** (`attack_loop/webpro_verify_round5_cores.py`, K=272..4160). No FATAL, no counterexample.
  Residual = ONE inherited verification-debt item: the **local-WSPD death-time implementation** (source
  Lemmas 23–24) + routine constants/failure-budgets/boundary conventions.
- **Confidence the full closure holds:** **~80% (ours)**, 0.91 (Pro). 🔴 "AI-verified ≠ proved."
- **Dedup/priority sweep (gate #2):** `lit/GATE2_DEDUP_SWEEP.md` = **GREEN, NO SCOOP** (no sub-√n
  range-counting EMST upper bound exists; new leads Peng–Sohler–Xu arXiv:2510.11547 & Patlin–van den
  Brand SOSA'25 are in DIFFERENT oracle models → cite, not scoop). **RE-SWEEP at submission.**
- **Contribution level (two independent reads agree, `docs/contribution_level_assessment_codex.md`):**
  **solid-to-strong SoCG accept; borderline-to-solid SODA accept.** Tight resolution in sublinear
  geometry; not a broad-TCS breakthrough. Lever to raise it: extend the new estimator to EMD / other
  range-counting estimation in the writeup.
- **NOT overlapping** with the sibling `dynamic-weighted-mis-fat-objects` project (that = weighted
  caching with predictions / online algorithms; only the research-PROCESS scaffolding was reused).

**Pending owner decisions at HUMAN GATE #2 (none auto-started):**
- (a) [optional belt-and-suspenders] cross-model **Claude round-5 audit** (the round-5 final audit was
  codex = same family as Pro; the Anthropic API was 529-throttled at the time — rerun when healthy).
- (b) **Human-expert verification** (esp. the WSPD death-time impl + the full Lemma 3 query accounting) —
  the step that turns "candidate" into "proved."
- (c) **Formal writeup** → `venue-prompts/soda/` (target SODA 2027, deadline **2026-07-09**; SoCG sibling).
- (d) Final preprint priority RE-SWEEP + own-work dedup, immediately before submission.

**Repo-name note:** `emst-oracle-lower-bound` is STALE (we pivoted to the upper bound) — rename deferred.

---

## HEADLINE
**[2026-06-22] ✅ §9.4 AI-CONVERGENCE on the Õ_ε(n^{1/3}) upper-bound closure → frozen at HUMAN GATE #2.**
5 GPT-5.5-Pro rounds (round-2 closure self-refuted at round 3; repaired round 4 via the empty-cell
spatial estimator; consolidated round 5) + 3 independent clean audits (codex final = CONVERGED) + cores
verified √K by execution + dedup GREEN (no scoop) + contribution = solid SoCG / borderline-solid SODA
accept (two independent reads). Residual = the inherited WSPD death-time impl + human verification.
Confidence ~80% (ours) / 0.91 (Pro). 🔴 candidate closure of a PUBLISHED open problem — NOT proved until
human-referee-checked. Full thread: `docs/webpro_thread_state.md`. Prior status below.

**[2026-06-21] (prior) ESCALATING to web GPT-5.5-Pro on the full original problem (owner-approved).** Paper-
orientation verdict (mine + independent audit `gate_paper_orientation_upper.md`): current contribution
is **NOT SODA-level standalone** (ESA/workshop-tier) — it hinges entirely on resolving the crux. Per
owner: escalate to web GPT-5.5-Pro, giving it the COMPLETE original problem with NO method constraints.
Self-contained brief ready at **`attack_loop/escalation_webpro_brief.md`** (target = settle the query
complexity either direction; all our verified facts P1/P2/U-P1/U-P5 + dead routes + the U-N4 crux + the
spread-vs-concentrate vise given as free context, explicitly non-binding). **Awaiting the owner to relay
it to web GPT-5.5-Pro; reply will be independently audited.** Also corrected an over-claim (U-P5 is a
reduction-to-two-unproven-primitives, NOT a "proven cost model"). Prior status below.

**[2026-06-21] (prior) UPPER-bound attack at a §9.1 escalation juncture (human decision).** 5 upper rounds + 5
audits: the closing Õ(n^{1/3}) algorithm is sound in the SPARSE regime (cluster-count integral
w=∫(c−1)dt; scalar c(λ) via point-sampling small-λ + 2-axis large-λ; dense-gadget scan) but Round 5
found a REAL gap — the DENSE large-λ regime (uniform grid: c(λ)=n≫n/λ refutes the cost bound, [[U-N3]]).
Likely another weight-red-herring (uniform weight ~√(n·Area)) but unproven. **Confidence o(√n) ~65%,
Õ(n^{1/3}) ~30%.** What's solid: LB barrier P1/P2 (gadget-packing caps at n^{1/3}) + the UB algorithm
skeleton + reframe. **Decision needed (web-Pro escalation / more codex / consolidate-to-paper / handoff).**
Details: `research_line_emst_upper.md`. Prior status below.

**[2026-06-21] (prior) 🔴 PIVOTED (§9.6): LOWER bound → UPPER bound.** Owner chose to **prove a sub-√n /
Õ(n^{1/3}) upper bound**, closing the same Driemel et al. gap *from above* (after Rounds 1+2 + 3 audits
near-refuted the lower-bound approach at n^{1/3}). Same problem, same model, same venue (SODA); opposite
side. New ledger `research_line_emst_upper.md` (LB ledger frozen as refuted record). Repo name
`emst-oracle-lower-bound` now partially STALE (flagged). **Now starting the upper-bound attack loop:**
extracting the source's Õ(√n) algorithm + √n bottleneck (facts subagent), then an algorithm-design brief
to codex GPT-5.5-xhigh. Confidence an improvement exists: ~30–40%. Prior LB status below.

**[2026-06-21] (superseded) AT A §9.6 HUMAN KILL/PIVOT GATE — Rounds 1+2 (near-)refute the whole LB approach.**
BOTH the single-needle ([[P1]]/N1) and the multi-needle/planted-pattern escape ([[P2]]/N2) **provably
cap the gadget-packing lower bound at n^{1/3} = the existing source bound** (codex GPT-5.5-xhigh + 3
independent audits; Audit C = NEAR-PROOF-OF-DEATH; 16+ exact-EMST/coverage probes). Not a *full*
proof-of-death (one narrow, evidence-against "new primitive" loophole survives). **Confidence an
Ω(n^{1/2−o(1)}) LB even exists: ~30%** — the obstruction is essentially algorithmic ⇒ truth likely
Θ(n^{1/3}), Õ(√n) loose. 🔑 **Substrate-supported pivot: prove a sub-√n / Õ(n^{1/3}) UPPER bound**
(close the gap from above — equally SODA-worthy). **Owner decision needed** (escalate-to-web-Pro /
pivot-upper-bound / pivot-EMD / barrier-paper / stop); not started autonomously. Details: ledger +
`attack_loop/`. Prior status below.

**[2026-06-21] Phase 1, Round 1 (C1) DONE — guide's core route REFUTED; target alive only via a harder
escape.** codex GPT-5.5-xhigh + 2 independent audits **proved** (analytic+numeric) that the
single-needle equal-cardinality gadget-packing route — the guide's entire §1/§6 plan, and the
pre-committed "improves" fallback — **caps at m=n^{1/3} = the existing source bound (NO improvement)**:
single-cell swap shifts w(P) by ≤O(s√p), backbone forces w(P)≥Ω(sm), s cancels ⇒ gap/w(P)≤O(√p/m),
needs c≥2/3. Banked as ledger **P1** (impossibility) / **N1** (dead route) / **B4** (barrier). The
**n^{1/2−o(1)} target is NOT dead** (§9.0b: a route died, not the target) — the sole surviving path is a
**multi-needle / planted-pattern** distribution (hard part moves from C1-geometry to C2/C3-information).
**Round 2 = attacker brief on that escape** (construct OR prove a general obstruction). Confidence in a
*tractable* route to the full target: **~18%** (attack-harder, not a downgrade). ⚠️ **Decision flag for
the owner:** the pre-committed kill-experiment fired; if the escape also dies, that is a proof-of-death
candidate for a human kill/pivot gate. Prior status below.

**[2026-06-20] Phase 0 COMPLETE — at human gate #1.** Kill-scan = **GREEN** (no scoop, no ceiling,
no pre-emption; gap still open; C1 & C2 constructions appear novel; independent audit concurs GREEN).
De-risking screens = **YELLOW, no kill fired**: the *naive/baseline* constructions are insufficient at
n^{1/2} (C1 gap fraction declines as p→n^{1/2}; C2 baseline grid coverage grows ~√m). A general-position
layout drives C2 coverage to O(1), but (per the audit) this is **not bankable** — it rides on
equal-cardinality + zero Δ-slack, so the open object is a **three-way squeeze** (point-efficient ×
equal-cardinality × O(1)-coverage × Δ=O(n)) with no positive evidence yet. **No proof-of-death ⇒
recommend pursuing the full n^{1/2−o(1)} ("closes") target as primary, with a time-boxed first
kill-experiment + pre-committed "improves" fallback.** Confidence ~38% (attack-harder signal, not a
downgrade). Verdict → `PHASE0_REPORT.md`. **STOP at human gate #1.** Nothing proven yet (screens are
necessary kill-screens, NOT proofs).

## Current phase
- **Phase 1 (attack loop) — STARTED 2026-06-20.** Human **gate #1 PASSED**: owner approved pursuing the
  full **n^{1/2−o(1)} ("closes")** target as primary, with a time-boxed first kill-experiment +
  pre-committed "improves" fallback (kill-scan GREEN; no RED ⇒ no pivot).
- **Attacker confirmed:** `codex` CLI present, logged in, configured `model="gpt-5.5"`,
  `model_reasoning_effort="xhigh"` — i.e. **codex GPT-5.5-xhigh**, exactly the guide's default attacker.
  Math routed out via `codex exec`; I remain orchestrator/referee/archivist (no solo proving).
- **Round 1 = crux C1 (the kill-experiment): DONE.** Result = REFUTATION of the single-needle route
  (ledger P1/N1/B4). codex reply + Audit A (rigor: SOUND) + Audit B (escape: FUNDAMENTAL to that route,
  one credible escape). Artifacts: `attack_loop/round1_C1_{brief,response,auditA,auditB}.md`,
  `attack_loop/auditB_probe*.py`.
- **Round 2 = the escape: multi-needle / planted-pattern distribution** (the reduced open problem in the
  ledger). Fresh attacker brief → codex. The C1→C2→C3 ordering is superseded: in the escape, C1
  (correlated gap) is easy; the crux is C2/C3-informational (hide Ω(m) bits from coarse counts).
- 🔴 **Pre-committed kill-experiment fired.** Per the gate-1 plan, a failed kill-experiment was a
  decision point. The single-needle gadget is *impossible* at n^{1/2} (and even the "improves" fallback
  is dead via this route). Continuing autonomously to the escape (§9.0b attack-harder), but flagging
  this to the owner — if the escape also dies it is a proof-of-death → human kill/pivot gate.

## Progress log
- **2026-06-20** — Read `guide.md` end-to-end. Confirmed repo is bare (only the 3 source docs);
  scaffolding at repo root (no nested `deepdive/` folder). Created `sim/.venv` (py3.12; numpy 2.4.6,
  scipy 1.18.0). Wrote day-0 docs (this file, `DESIGN_DECISIONS.md`, `docs/guide_amendments.md`,
  `research_line_emst.md`, `PROOF_REVIEW/README.md`, `lit/SCAN_REPORT.md`, `sim/README.md`).
  Launched 4 background literature-scan threads (RED-scoop, RED-ceiling, prior-gadget/packing,
  source+citation verification). Wrote sim screens.
- **2026-06-21** — Human **gate #1 PASSED** (owner: "continue per your suggestion" → full target
  primary + time-boxed kill-experiment). Confirmed codex GPT-5.5-xhigh attacker available. **Round 1
  (C1) attack:** briefed codex → it REFUTED the single-needle route (caps at n^{1/3}); 2 independent
  audits (rigor + escape) confirmed analytically + numerically. Banked P1/N1/B4. Reduced the open
  problem to the multi-needle/planted-pattern escape. Confidence 38%→18%. Launching Round 2.

## Frozen results & numbers (append-only)
Source: `sim/results.json` (regenerate via `sim/run_all.py`, fixed seeds). EMST is EXACT
(Delaunay+Kruskal, self-checked vs brute force). **Screens are necessary kill-screens, NOT proofs.**

**C1 — gadget detectability** (heavy "uniform" grid vs sparse "strip", ε=0.10; gap_frac =
(w_heavy − w_sparse)/w_sparse):

| date | quantity | value | artifact |
|---|---|---|---|
| 2026-06-20 | gap_frac at θ=2/3 (p≈n^{2/3}, source regime) | 0.97 / 0.70 / 0.88 (n=2025/4096/8100) — large, detectable | `sim/results.json` |
| 2026-06-20 | gap_frac at θ=1/2 (p≈n^{1/2}, target regime) | 0.128 / 0.086 / 0.064 (n=2025/4096/8100) — **declines with n** | `sim/figures/c1_gap_fraction.png` |
| 2026-06-20 | smallest detectable budget (gap≥ε) | survives to θ≈0.54 (p≈n^{0.54}); below-ε at full θ=0.5 for n≥4096 | `sim/results.json` |
| 2026-06-20 | negative control (heavy:=strip) | gap_frac = 0.000 (all θ) — sanity OK | `sim/results.json` |

**C2 — per-query coverage** (ADVERSARIAL max candidate-distinguishing-power of a range-COUNTING
query; the kill metric. m = #candidate cells, p=16/cell):

Adversary = tight **coordinate-snapped** rectangles (gate-1 audit correction; centre-cut family
understated the constant). Reported coverage is worst-case over our family = a **lower bound** on the
true optimum.

| date | quantity | value | artifact |
|---|---|---|---|
| 2026-06-20 | baseline **grid** packing, counting coverage vs m | adv max = 12,20,28,36,42,48,57 (m=16…256); **slope ≈ 0.55 ⇒ polynomial √m (const ≈ 3.5–4)** | `sim/figures/c2_coverage.png` |
| 2026-06-20 | **permutation** (general-position) packing, counting coverage | adv max = **4 (flat) for all m; slope ≈ 0.00 ⇒ O(1)** (robust under tight adversary) | `sim/results.json` |
| 2026-06-20 | grid emptiness coverage vs m | adv max = 2√m (8…32); slope 0.50 | `sim/results.json` |
| 2026-06-20 | counting vs emptiness contrast (grid) | counting ≈ 2×emptiness ⇒ counting coverage ≥ emptiness (hypothesis confirmed) | `sim/results.json` |
| 2026-06-20 | MI/log-m ratio (grid, worst rect) | **declines** 0.54→0.16 as m grows even though coverage grows √m ⇒ bit-accounting MISSES the growth (the Ω(log m) trap, empirical) | `sim/results.json` |

**Implication of the C2 numbers:** on the grid layout the hitting bound Ω(m/coverage)=Ω(√m); with
m=Θ(n^{1/2}) that is only ~n^{1/4}. The permutation O(1)-coverage result shows the √m is a *grid
artifact* — but it is **NOT bankable** (gate-1 audit): the O(1) rides on **equal-cardinality
invisibility** (in tension with C1's point-efficiency) on a layout with **Δ=1.00·n, zero slack**. The
open problem (C2 attack) is a **three-way squeeze** — a packing keeping coverage O(1)/m^{o(1)} *while*
preserving C1 detectability *and* equal cardinality *and* Δ=O(n) — with no positive evidence yet.

## Frozen bibliographic facts (append-only, from the kill-scan; full detail in `lit/SCAN_REPORT.md`)
- **Source:** Driemel, Monemizadeh, Oh, Staals, Woodruff, "Range Counting Oracles for Geometric
  Problems," SoCG 2025, **arXiv:2504.15292 (v1 only)**. Upper = **Thm 30** (Õ(√n)); lower =
  **Lemma 32** (o(n^{1/3}) ⇒ const. mult. error); Lemma 31 = MST(I)≥2·MST(I′). Hard instance:
  **16·n^{1/3} cells, side 4·n^{5/6}; n^{2/3} pts/gadget; heavy Θ(n^{7/6}) / sparse Θ(n^{5/6});
  ≤4 cells/query** (all verified from the PDF).
- **Czumaj boundary:** Czumaj–Ergün–Fortnow–Magen–Newman–Rubinfeld–Sohler, SIAM J. Comput.
  **35(1):91–109, 2005**, DOI 10.1137/S0097539703435297 — range-**emptiness**, deterministic,
  **O(n^{1/4})** error, **Ω(√n)**. Motivation ONLY (emptiness ⊊ counting).
- **Only citing paper:** arXiv:2603.20943 (Schibler–Xue–Zhu, convex hull, emptiness, SoCG 2026) —
  does NOT touch the MST counting bound.
- **SODA 2027:** deadline **2026-07-09**; single-col 11pt 1-inch; no hard page limit (first ~10pp
  convey merits); **light double-blind**; conf. Jan 24–27 2027.

## TODO + pending human decisions (for gate #1)
- [ ] **Decision (gate #1, decisive):** pursue full **n^{1/2−o(1)} ("closes")** vs settle for the
  **best supportable exponent ("improves")** — driven by the C1/C2 screens.
- [ ] **Decision (gate #1):** approve the GREEN/YELLOW/RED kill verdict (incl. RED-scoop &
  RED-ceiling searches) + the independent second-opinion subagent's read.
- [ ] **Decision (gate #1):** if any RED kill fired, pivot-vs-stop (§9.6 — e.g. EMD
  range-counting-oracle bound). *(None fired — informational.)*
- [ ] **Endorse Phase-1 entry plan (audit rec.):** first milestone = a time-boxed kill-experiment —
  build ONE point-efficient, **equal-cardinality** heavy gadget shifting w(P) by ≥ε at the n^{1/2}
  budget; if impossible / forces unequal cardinality → fall back to best "improves" exponent.
- [x] (internal) Run `sim/run_all.py`; froze all numbers here (re-run with the tight coordinate-snapped
  C2 adversary per the audit).
- [x] (internal) Consolidated the 4 scan threads into `lit/SCAN_REPORT.md` (concern table + GREEN
  verdict); ran the independent paper-orientation audit → `gate1_paper_orientation_audit.md`
  (process flag it raised — missing artifacts — now resolved; both files committed).

## Confidence trend
- **2026-06-20 (pre-screen):** ~50% that the full n^{1/2−o(1)} "closes" target is reachable
  (inherited; both cruxes unverified).
- **2026-06-20 (post Phase-0, pre-audit draft):** ~50%.
- **2026-06-20 (post-audit, ADOPTED):** **~38%.** Revised down per the independent gate-1 audit: the
  permutation O(1)-coverage signal is **less load-bearing than it looked** (it rides on
  equal-cardinality + zero Δ-slack — a three-way squeeze with no positive evidence the coupled object
  exists). Held up by kill-scan GREEN + no proof-of-death. **Per §9.0b this is an attack-harder
  signal, NOT a target downgrade** — the n^{1/2−o(1)} target is unchanged.

## Artifact index
- Ledger: `research_line_emst.md` · Decisions: `DESIGN_DECISIONS.md` · Guide amendments:
  `docs/guide_amendments.md`
- Lit: `lit/SCAN_REPORT.md` · Paper-orientation audit: `gate1_paper_orientation_audit.md`
- Screens: `sim/` (`run_all.py` is the single entry point) · Figures: `sim/figures/` · Results:
  `sim/results.json`
- Verdict: `PHASE0_REPORT.md`
