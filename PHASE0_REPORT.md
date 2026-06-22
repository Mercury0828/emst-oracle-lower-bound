# PHASE 0 VERDICT REPORT — emst-oracle-lower-bound

**Date:** 2026-06-20 · **Phase:** 0 (screen) complete · **Next:** human **gate #1** (mandatory stop).
**Target:** Ω(n^{1/2−o(1)}) orthogonal-range-counting-oracle queries to (1±ε)-estimate the Euclidean
MST weight — closing the Ω(n^{1/3}) vs Õ(√n) gap of Driemel et al. (SoCG 2025, arXiv:2504.15292).
**Venue:** SODA 2027 (deadline 2026-07-09; pure theory — these screens are internal de-risking, NOT
paper results).

> **Honesty rail (guide.md §9.4):** nothing here is a proof. The screens are *necessary kill-screens,
> not sufficient proof*; asymptotic detectability (C1) and asymptotic O(1)-coverage (C2) are attack-loop
> proof obligations. "AI-verified ≠ proved."

---

## 0. One-paragraph verdict
**No kill fired. Recommend pursuing the full n^{1/2−o(1)} ("closes") target via the attack loop.**
The literature kill-scan is **GREEN**: no one has improved the counting-oracle EMST lower bound past
n^{1/3} (no scoop), there is no sub-√n counting upper bound or impossibility (no ceiling), and neither
load-bearing construction (C1 point-efficient gadget, C2 O(1)-coverage COUNTING packing) is
pre-empted — both appear novel. The de-risking screens are **YELLOW (informative, not a kill)**: the
*naive/baseline* versions of both cruxes are insufficient at n^{1/2} — the source gadget's detectable
gap declines as it is thinned to n^{1/2} (C1), and the baseline √m×√m grid packing has per-query
counting coverage that grows like √m (C2). A general-position ("permutation") layout *does* drive C2
coverage to a flat O(1), showing the √m is a *grid artifact* — **but this is not bankable**: per the
independent gate-1 audit, that O(1) rides entirely on **equal-cardinality invisibility** (which C1's
point-efficiency requirement threatens) on a layout with **zero Δ=O(n) budget slack**. So the full
target hinges on an **unbuilt coupled object facing a three-way squeeze** — point-efficient ×
equal-cardinality × O(1)-coverage × Δ=O(n) — with no positive evidence yet that it exists. **No
proof-of-death fired**, so per §9.0b the honest call is *attack harder*, not retreat: pursue the full
target as primary, with a **time-boxed first kill-experiment** (build one point-efficient
equal-cardinality heavy gadget) and a **pre-committed "improves" fallback**.

---

## 1. Literature kill-scan — **GREEN** (detail: `lit/SCAN_REPORT.md`)
Four independent fresh-context web threads + one independent second-opinion audit. Kill criteria were
frozen in `guide.md` §3 before the scan.

- **RED scoop? NO.** No paper improves the randomized (1±ε) counting-oracle EMST lower bound past
  Ω(n^{1/3}). The source (arXiv:2504.15292) has exactly **one** citing paper — arXiv:2603.20943
  (convex hull, range-emptiness), confirmed irrelevant to the MST counting bound. No author follow-up.
- **RED ceiling? NO.** No sub-√n (exponent ≤ 1/2−Ω(1)) counting-oracle upper bound and no result
  ruling out an n^{1/2−o(1)} lower bound. Õ(√n) (= n^{1/2−o(1)}) remains SOTA and is **not** a ceiling.
- **Pre-emption? NO.** RS/induced-matching packings in the literature serve matching-size estimation
  under EMPTINESS/pair queries; the source's own EMD argument hides a single needle (not an
  O(1)-coverage COUNTING packing). A point-efficient (~n^{1/2}) MST-distinguishing gadget and an
  O(1)-coverage packing for *exact counting* queries both appear novel.
- **Source verified from the PDF.** v1 only; **Thm 30** (Õ(√n) upper), **Lemma 32** (o(n^{1/3}) ⇒
  constant multiplicative error). Hard instance: **16·n^{1/3} cells of side 4·n^{5/6}, n^{2/3}
  pts/gadget, heavy Θ(n^{7/6}) / sparse Θ(n^{5/6}), ≤4 cells/query.**
- **Czumaj boundary nailed down (motivation only).** Czumaj–Ergün–Fortnow–Magen–Newman–Rubinfeld–
  Sohler, SIAM J. Comput. **35(1):91–109, 2005**, DOI 10.1137/S0097539703435297 — range-**emptiness**,
  **deterministic**, **O(n^{1/4})** error, **Ω(√n)**. All three axes differ from our setting; the
  bound does **not** transfer to the stronger counting oracle.
- **Residual scan risk:** brand-new (last-few-days) preprints may not be indexed yet → re-sweep at
  gate #2. A few sources were paywalled/403 (Czumaj full text, soda27 SIAM page) — facts corroborated
  from secondary sources and flagged in `lit/SCAN_REPORT.md`.

**Independent second opinion (`gate1_paper_orientation_audit.md`):** concurs **GREEN** on the kill
verdict via its own web spot-checks (full second opinion + its C1/C2 corrections in §5).

---

## 2. (C1) Gadget-detectability screen — naive gadget insufficient at n^{1/2}, not dead
**Pre-registration (PR-C1, locked before running):** thin the source heavy(uniform-grid)/sparse(strip)
gadgets toward n^{1/2}; expect the heavy-vs-sparse gap fraction of w(P) to stay ≥ ε; kill signal =
fraction shrinks below ε and keeps shrinking as p→n^{1/2}. (A-priori note logged before running: the
naive gadget's heavy/sparse ratio is ~√p while a Θ(1) gap needs ratio ~m, so a decline was expected.)

**Result (exact EMST; ε=0.10; gap_frac = (w_heavy − w_sparse)/w_sparse):**

| n (target) | θ=2/3 (source regime, p≈n^{2/3}) | θ=1/2 (target regime, p≈n^{1/2}) | smallest detectable budget |
|---|---|---|---|
| 2025 | 0.973 | 0.128 | survives to θ≈0.50 (p≈49) |
| 4096 | 0.698 | 0.086 (below ε) | survives to θ≈0.54 (p≈100) |
| 8100 | 0.884 | 0.064 (below ε) | survives to θ≈0.54 (p≈121) |

- **Trend as p→n^{1/2}:** gap fraction falls monotonically from Θ(1) (source budget) toward ε; at the
  *full* n^{1/2} budget it is below ε for n≥4096 and **decreases with n** (0.128→0.086→0.064),
  consistent with the predicted ~n^{−1/4} decay. **Smallest detectable budget:** ~p≈n^{0.54}.
- **Negative control** (heavy:=strip, no separation): gap_frac = **0.000** at every θ — confirms the
  signal is the genuine heavy/sparse geometry, not an artifact.
- **Read:** the *naive source gadget* does not support the full n^{1/2} budget asymptotically. This
  **localizes the C1 burden** — the attacker must design a more point-efficient heavy gadget (raising
  the heavy/sparse cost ratio from ~√p to ~m within the same point budget). It is a construction
  obligation, **not** a proven infeasibility (which would require showing *no* such gadget exists).
- **Caveat (gate-1 audit):** "detectable survives to ~p≈n^{0.54}" is **not** encouragement for the
  full target — at θ≈0.54 there are m=n^{0.46} candidates, which caps the bound at ~n^{0.46}, an
  **"improves" regime, not "closes."** Do not read that row as positive evidence for n^{1/2}.
- **Scale caveat:** at a few-thousand points the p-budgets differ by only a small factor; the screen
  shows the **trend**, not the asymptotic crossover.

Figure: `sim/figures/c1_gap_fraction.png`.

---

## 3. (C2) Per-query coverage screen — THE decisive measurement
**Pre-registration (PR-C2, locked before running):** on the baseline √m×√m grid packing, measure the
adversarial **max** per-query COUNTING coverage (= #candidate cells whose heavy/sparse flip changes the
exact count) as m grows; pass = flat O(1)/m^{o(1)}, kill (strength) signal = polynomial growth m^{Ω(1)}.
Adversarial is the kill metric; random is smoke. (A-priori note logged before running: a rectangle edge
can slice a √m-cell column, so the baseline grid was expected to show ~√m.)

**Result (adversarial max coverage; the kill metric; tight coordinate-snapped adversary — see note):**

| m | baseline **grid** (counting) | **permutation** (counting) | grid (emptiness) | grid MI/log m |
|---|---|---|---|---|
| 16 | 12 | 4 | 8 | 0.54 |
| 64 | 28 | 4 | 16 | 0.32 |
| 144 | 42 | 4 | 24 | 0.20 |
| 256 | 57 | 4 | 32 | 0.16 |
| **log-log slope vs m** | **≈ 0.55 (polynomial √m, const ≈ 3.5–4)** | **≈ 0.00 (flat O(1))** | ≈ 0.50 (=2√m) | (declining) |

> **Adversary-strength note (gate-1 audit correction, now applied).** The first committed adversary
> (half-planes/slabs/centre-cuts only) reported grid coverage ≈ 2√m, because a *centre* cut splits
> the strip symmetrically (heavy-count = sparse-count ⇒ not covered). The independent auditor's
> stronger adversary (coordinate-snapped random rectangles, edges off-centre where the heavy 4×4 grid
> jumps by 4 but the strip increments by ~1) found ≈ 4√m. `sim/c2_coverage.py` now uses the
> coordinate-snapped adversary and **reproduces the auditor's numbers** (grid ≈ 3.5–4·√m). The
> exponent (slope ≈ 0.5) is the robust signal; the reported coverage is a worst-case *over our family*
> — a **lower bound** on the true adversarial optimum, so the polynomial-growth conclusion is, if
> anything, understated.

- **Baseline grid = polynomial coverage (√m).** Falsifies the optimistic "O(1)" expectation *for the
  grid layout*: an axis-aligned rectangle's 4 edges each straddle up to a √m-cell column/row, each
  straddled cell's heavy/sparse flip changing the partial count. On the grid the hitting bound is
  Ω(m/√m)=Ω(√m); with m=Θ(n^{1/2}) that caps at only **~n^{1/4}**. This **realizes the residual risk
  (guide.md §0, §6 C2, risk #1)** on the baseline.
- **Permutation (general-position) layout = O(1) coverage — but NOT bankable.** Placing the m gadgets
  with **disjoint x- AND y-bands** makes every axis-parallel line meet O(1) cells ⇒ adversarial max
  coverage is **flat = 4** across all m (robust under the tight adversary). This shows the √m is a
  **grid artifact**, not fundamental. **HOWEVER** (gate-1 audit, Finding 2b/2c) this O(1) rides
  *entirely* on **equal-cardinality invisibility**: a fully-contained cell contributes 0 to coverage
  only because heavy and sparse gadgets have the *same* point count. That is exactly the assumption
  **C1's point-efficiency requirement threatens** — if a point-efficient heavy gadget needs *unequal*
  cardinality, contained cells become visible and coverage explodes (the B3 danger). And the
  permutation layout sits at **Δ = exactly 1.00·n — zero budget slack** (any cell-side increase C1
  demands pushes Δ past O(n)). So the open object is a **simultaneous three-way squeeze**:
  point-efficient × equal-cardinality × O(1)-coverage × Δ=O(n)-no-slack, with **zero positive evidence
  it exists**. The permutation result is real but must NOT be read as nearly-banked good news.
- **Counting ≥ emptiness (confirmed).** On the grid, counting coverage ≈ 2× the emptiness coverage
  (=2√m) — the exact-integer count is measurably more revealing than the 0/1 bit, as predicted (B3).
- **The Ω(log m) trap, made empirical.** The secondary MI/log-m ratio on the grid **declines**
  (0.54→0.16) even as coverage grows √m. A bit-accounting reviewer would see "few bits per query" and
  miss the polynomial coverage growth entirely — concrete evidence that **coverage, not bits, is the
  operative quantity** (guide.md §0 framing note; barrier B2). (MI stays a one-paragraph illustration,
  not a sub-investigation — per the audit's drift caution.) Random-placement coverage tracks the mean
  (~2√m on grid) and is a smoke check only.

Figure: `sim/figures/c2_coverage.png`.

---

## 4. Best achievable exponent the screens support
- **Naive/baseline constructions alone:** capped well below 1/2 (grid packing ⇒ ~n^{1/4}; naive
  gadget ⇒ detectable only to ~p≈n^{0.54}). **If one were forced to ship only the baseline, the honest
  headline would be "improves," not "closes."**
- **But no proof-of-death fired.** The screens show the obstacles are *constructional*, not barriers:
  the C2 permutation result shows O(1) coverage is attainable in isolation, and C1 detectability is
  robust at modest thinning. The **full n^{1/2−o(1)} ("closes") target is not excluded** — it requires
  the attack loop to deliver the coupled object (point-efficient × equal-cardinality × low-coverage
  general-position/RS packing × Δ=O(n) budget × the Ω(m)-not-Ω(log m) reduction).
- **Honest strength-gate framing (gate-1 audit, applied):** the correct statement is **not** "the
  evidence SUPPORTS attempting the full target" — it is "**no proof-of-death fired, but the central
  positive object is entirely unconstructed and faces a genuine three-way squeeze; the screens neither
  support nor refute its existence.**" The achievable exponent is an empirical fact about the
  construction (guide.md §9.0b). Phase 0 recommends *attempting the full target as primary* (settling
  for "improves" now, absent any proof the construction caps below 1/2, would be a difficulty-driven
  retreat the red line forbids) — but with eyes open and a time-boxed first kill-experiment.

---

## 5. Independent second-opinion audit (paper-orientation, guide.md §10)
Full text: `gate1_paper_orientation_audit.md` (fresh-context, adversarial; it re-ran its own stronger
C2 adversary, verified the C2 mechanism, checked the Δ=O(n) arithmetic, and web-spot-checked the scan).
**Verdict: ON-TRACK.** Summary of what it concurred with and where it pushed back (all corrections
above are folded into §2–§4):
- **Kill verdict: concurs GREEN.** Independent web spot-checks corroborate no scoop / no sub-√n
  counting upper bound / no ceiling; convex-hull paper is emptiness, ICALP'23 MST is a different
  (distance-query, general-metric) model; Czumaj boundary correctly stated and does not transfer.
  Residual: one more targeted preprint pass near submission (deferred to gate #2).
- **C2 correction 1 (applied):** my first adversary understated grid coverage (centre cuts hit the
  symmetric heavy=sparse point); the tight coordinate-snapped adversary gives grid ≈ 4√m (now
  reproduced in the committed screen). Exponent/slope unchanged; conclusion *strengthened*.
- **C2 correction 2 (applied):** the permutation O(1) is real but **not bankable** — it rides on
  equal-cardinality invisibility (in tension with C1's point-efficiency) on a Δ=1.00·n layout with
  zero slack ⇒ the coupled object is a **three-way squeeze** with no positive evidence yet. My draft
  was "one notch too optimistic"; §0/§3/§4 are corrected accordingly.
- **C1:** read is sound; only caveat = the n^{0.54} survival is an "improves" regime, not n^{1/2}
  encouragement (folded into §2).
- **Drift check:** no meaningful drift; barriers + strength gate kept central; Czumaj not mis-stated.
  Two minor cautions logged: keep the MI-ratio as a one-paragraph illustration (not a sub-study); and
  do **not** let the attack loop slide into treating "permutation + equal cardinality" as *the*
  construction (it is a probe, not the RS obligation).
- **Process flag (now resolved):** the audit ran before `lit/SCAN_REPORT.md` and this report existed
  and flagged their absence; both are now committed with the exact citations, so the verdict is
  auditable as required.
- **Gate-1 recommendation (audit):** approve GREEN; pursue full **n^{1/2−o(1)} ("closes")** as primary
  with the C1×C2×B1 coupled gadget as a **time-boxed first kill-experiment** + a pre-committed
  "improves" fallback. It revises "closes is reachable" from ~50% to **~35–40%** — an *attack-harder*
  signal (§9.0b), not a downgrade. **I adopt this**: see the confidence note below.

---

## 6. Open items for human gate #1
1. **Strength decision (decisive):** pursue the full **n^{1/2−o(1)} ("closes")** target — the Phase-0
   + audit recommendation — vs settle for a best-supportable exponent ("improves"). Starting the
   attack loop on the full target requires this sign-off. Recommended framing: **full target as
   primary, with a time-boxed first kill-experiment and a pre-committed "improves" fallback** (below).
2. **Approve the kill verdict:** GREEN (no scoop / no ceiling / no pre-emption) + the independent
   second opinion (concurs GREEN). No RED fired ⇒ no pivot needed; the EMD range-counting-oracle bound
   remains a pre-scoped pivot target only if a later kill fires (guide.md §9.6).
3. **Endorse the Phase-1 entry plan (audit recommendation):** the first milestone is a **single
   time-boxed kill-experiment — construct one point-efficient, *equal-cardinality* heavy gadget that
   shifts w(P) by ≥ ε at the n^{1/2} budget.** If it cannot be built (or forces unequal cardinality,
   which the C2 screen shows blows up coverage), the "closes" target is effectively dead and the team
   falls back to the best provable "improves" exponent — *without* sinking the full timeline (deadline
   2026-07-09 is tight).
4. **Acknowledge the residual scan risk:** a final preprint priority sweep is deferred to gate #2.
5. (No action; FYI) Attack-loop order is C1 → **C2 (the kill point)** → C3; the genuine open problem
   the screens isolated is the **three-way squeeze** (point-efficient × equal-cardinality ×
   O(1)-coverage × Δ=O(n)-no-slack), plus the C3 Ω(m)-not-Ω(log m) packaging (barrier B2).

**Confidence note (adopted from the audit):** "closes is reachable" revised **~50% → ~38%** — driven
*down* by the three-way squeeze (the central object is unconstructed and the one positive sim signal,
permutation O(1), is less load-bearing than it looked), held *up* by the GREEN literature and the
absence of any proof-of-death. Per §9.0b this is an **attack-harder signal, not a target downgrade.**

---

## 7. Paper-orientation one-liner (guide.md §10)
**Given what we see, how far is a submittable SODA paper, and has the thinking drifted?** A
submittable SODA paper is **the full attack loop away** — Phase 0 cleared the prerequisites (the gap
is open and unclaimed, the contribution is on-topic and PC-relevant, the constructions are novel) but
**zero of the load-bearing math is proven**; the paper exists only if the attack loop delivers C1+C2+C3
(realistically a "closes" headline if the coupled construction works, an "improves" headline if C2
coverage provably resists). **No drift detected:** the work stayed on the frozen needle-in-haystack /
coverage axis, did not wander into bit-accounting (the Ω(log m) trap was actively screened *against*),
did not over-generalize, and kept the Czumaj emptiness boundary correctly separated.
