# Round 1 — C1 Independent Audit B (adversarial "is there an escape?")

**Auditor:** fresh-context, independent. **Date:** 2026-06-21.
**Mandate:** the solver's impossibility (`round1_C1_response.md`) says C1 is dead *"under the stated
cell-tiling assumptions."* Determine whether the impossibility is FUNDAMENTAL to the Ω(n^{1/2−o(1)})
counting-oracle goal or an artifact of OVER-CONSTRAINED frozen assumptions.

---

## The impossibility, distilled to its two load-bearing inequalities

The whole proof is one ratio:

- **(UB) one-cell gap ≤ O(s·√p).** Replacing the contents of ONE side-`s` cell can change the global
  EMST by at most `C·s√p`, because `EMST(p points in a side-s square) ≤ C·s√p` and MST is monotone
  under add/delete. This is geometry-agnostic — fractal, hierarchical, nested, anything — so **no clever
  heavy gadget can beat it.** This is the harder, more general half, and it is correct.
- **(LB) backbone w(P) ≥ c₀·s·m.** If `m` side-`s` cells tile `[Δ]²` (Δ=`ks`) and every cell is
  occupied, then `[Δ]²` lies in the √2·s-neighborhood of the MST, and an `r`-neighborhood of a length-`L`
  tree has area `O(rL+r²)`, so `Δ² ≤ O(sL)` ⇒ `L ≥ c₀sm`. Correct.

Ratio: `gap/w(P) ≤ O(s√p / sm) = O(√p/m)`. With `p=n^c, m=n^{1−c}`: `n^{3c/2−1}`. Constant fraction
needs `c ≥ 2/3`. At `c=1/2` the best fraction is `n^{−1/4+o(1)}` → C1 impossible. **I reproduced the
n^{−1/4} decline numerically** (probe1: gap_frac 0.143→0.112→0.092→0.078 for k=4..10 at the p≈m≈n^{1/2}
regime, tracking √p/m = 1/k). The arithmetic is sound. The audit question is whether the *assumptions*
A–E are necessary for the GOAL, or merely frozen into the brief.

---

## Per-assumption verdict

### A. Cells tile the full domain, every cell occupied (used in the backbone LB)
- **LOAD-BEARING in the proof?** YES — it is the entire source of the `sm` denominator. Without it the
  `√p/m` cap does not follow.
- **NECESSARY for the goal?** NO, not literally — the candidates need not tile; they could be packed
  into a sub-region of side `L<Δ`, or laid out hierarchically.
- **ESCAPE-PLAUSIBLE?** **NO.** The s-dependence cancels exactly, as the brief warned. Packing the `m`
  centers into a region of side `L=Δ/t` forces the inter-center spacing — and hence the maximum
  legitimate cell side `s` — to shrink by the same factor `t` (if a gadget's footprint exceeds the
  spacing, gadgets collide and the "m disjoint candidate cells" structure, plus the downstream counting
  argument, breaks). Both numerator (`s√p`) and denominator (`sm`) carry one factor of `s`, so the
  fraction is **scale-invariant**. Numerically confirmed (probe2 CLUSTER rows): shrinking the region
  2×/4×/8× leaves gap_frac **identically 0.1121 / 0.0918 / 0.0776** — unchanged to 4 digits. The only
  way to raise the fraction was to keep a large cell footprint while packing centers densely (probe2
  DECOUPLE rows, frac up to 0.26) — but that **physically overlaps neighboring gadgets** and is invalid.
  Hierarchical "tight cluster" sparse gadgets (probe3) make the fraction *lower*, not higher, because
  the backbone is set by the centers spanning the domain, not by per-cell internal cost. An analogous
  `sm` obstruction recurs under every legitimate spread.

### B. Equal cardinality (heavy and sparse both have p points)
- **LOAD-BEARING in the proof?** NO. The UB `O(s√p)` and the LB `c₀sm` never use equal cardinality;
  the impossibility holds for unequal cardinality too (with `p` = the larger count, `s√p` only grows).
- **NECESSARY for the goal?** This is the frozen downstream coupling (B-eq). It is necessary *for the
  C2 counting argument as currently conceived*, not for the EMST gap itself.
- **ESCAPE-PLAUSIBLE?** **NO (it is a trap, not an escape).** Relaxing to an unequal-cardinality heavy
  cell (more points) *does* enlarge the per-cell EMST and could raise the C1 gap — but it simultaneously
  makes the heavy cell **visible to a single coarse counting query**: a rectangle enclosing the cell
  returns a larger integer count under YES than NO. The needle is then locatable by O(log m) binary-search
  counting queries (or O(1) coarse ones), collapsing the query lower bound to Ω(log m) — precisely the
  B2 trap recorded in the ledger. So B trades a C1 win for a fatal C2/C3 loss. The C1↔C2 coupling the
  ledger flags as a "three-way squeeze" is real and tight: equal-cardinality is what *forces* the gap to
  come from geometry alone, which is exactly what the `√p/m` cap kills.

### C. Distinct integer-grid points, min distance 1 (could coincident points help?)
- **LOAD-BEARING in the proof?** NO. The UB is an upper bound on `EMST(H)` so a *smaller* sparse EMST
  (even 0 from coincident points) does not raise the gap UB; it only lowers the `w_sparse` floor inside
  a single cell, which is dwarfed by the backbone.
- **NECESSARY for the goal?** The grid/min-distance-1 model is the source model; coincident points are a
  measure-zero degeneracy the range-counting framework can technically tolerate but they don't change
  asymptotics.
- **ESCAPE-PLAUSIBLE?** **NO.** Making SPARSE's internal EMST ≈ 0 (cluster all p points) does not help:
  the denominator `w(P)` is **backbone-dominated** (`Θ(sm)`), not sparse-cell-dominated, so killing the
  per-cell sparse cost changes `w(P)` by a lower-order term. Numerically the cluster-sparse gap fraction
  is *lower* than strip-sparse (probe1: 0.082/0.081/0.073/0.065 vs 0.143/0.112/0.092/0.078), because the
  heavy excess is unchanged while `w_sparse` barely moves. The backbone LB survives coincidence (it only
  needs one occupied point per cell). No escape.

### D. ONE heavy needle among m identical candidates
- **LOAD-BEARING in the proof?** YES — the UB is a *single-cell* replacement bound. The proof says
  nothing about a coordinated, many-cell difference.
- **NECESSARY for the goal?** **This is the one genuinely interesting relaxation.** The goal needs
  Ω(m) *queries*, which the standard Yao route gets from a *single* hidden needle. A correlated /
  multi-needle / multi-scale hidden structure is NOT covered by the single-cell UB.
- **ESCAPE-PLAUSIBLE? from the √p/m CAP: yes. From the GOAL: maybe — but with a different, harder
  obstruction.** Numerically (probe3): making ~m/2 cells heavy (YES) vs all-sparse (NO) yields a global
  gap fraction of **2.06 / 3.01 / 3.98** for k=6/8/10 — a *constant (indeed growing)* fraction at the
  p≈m≈n^{1/2} budget. So a coordinated bulk difference trivially clears (1±ε) detectability while each
  individual cell still contributes only ≈ √p/m. The single-cell cap is escaped. **HOWEVER** the cap is
  the wrong question for this route: a bulk/correlated shift of `Θ(w(P))` is **estimable by a handful of
  coarse counting queries** (a few big rectangles already reveal the aggregate excess), so it does NOT
  force Ω(m) queries under any obvious distribution — it reintroduces the B2 "Ω(log m), not Ω(m)" trap at
  the query-complexity level rather than the gap level. To convert a multi-needle gap into an Ω(m) query
  bound one needs a distribution where the *pattern* of which cells differ carries Ω(m) bits AND each
  counting query reveals o(1) of those bits (low coverage) — i.e. one must re-win C2/C3 on a
  fundamentally different (coding-theoretic / planted-pattern) hard distribution, not the
  single-needle-in-haystack the brief froze. **This is the only credible escape direction, and the
  solver was never asked to consider it** (the brief froze "ONE heavy cell").

### E. Detectability captured by gap ≥ ε·w(P)
- **LOAD-BEARING in the proof?** YES (implicitly) — the proof bounds the *deterministic* gap; the
  "constant fraction" threshold is the multiplicative-estimation requirement.
- **NECESSARY for the goal?** Mostly yes, but slightly conservative. A (1±ε) estimator must separate the
  two worlds; for a *deterministic* one-shot adversary `gap ≥ Ω(ε·w(P))` is the right condition.
- **ESCAPE-PLAUSIBLE? maybe (weak).** For a *randomized* hard distribution one can sometimes get a query
  lower bound from a sub-constant per-instance gap if the gap *concentrates* differently across the two
  worlds (estimator variance / total-variation distance, not raw multiplicative gap). But this loosens
  the threshold by at most a sub-polynomial / constant factor and cannot turn `n^{−1/4}` into `Θ(1)` — a
  polynomial shortfall remains. No polynomial escape via E alone; at best it shaves the `o(1)` and pairs
  with D.

---

## Overall judgment

**The impossibility is FUNDAMENTAL to the single-needle gadget-packing route, and the `√p/m` cap is NOT
an artifact of the tiling assumption.** The cap survives every *single-cell* relaxation the brief
allowed (A sparse/hierarchical placement, C coincident points) because the cell side `s` cancels between
the `s√p` gap-UB and the `sm` backbone-LB — confirmed analytically and numerically (scale-invariant
gap fraction). Relaxing equal cardinality (B) escapes C1 only by breaking C2 (the needle becomes
count-visible → B2 Ω(log m) trap). So along the frozen "one heavy cell among m equal-cardinality tiling
candidates" axis, the n^{1/2} target is dead and `c=2/3` is sharp. The solver's verdict is correct and
its single-cell UB is robust against fractal/hierarchical cleverness.

**BUT there is ONE credible escape direction the solver was never asked to consider — assumption D.**
Name it precisely:

> **MULTI-NEEDLE / PLANTED-PATTERN hard distribution.** Drop "one heavy cell." Use a distribution over
> *which subset (or coordinated multi-scale pattern) of cells is heavy*, engineered so that (i) the
> global EMST gap between two pattern-classes is `Θ(w(P))` even at p=n^{1/2} (numerically confirmed: a
> Θ(m)-cell coordinated difference gives gap fraction 2–4, not n^{−1/4}), while (ii) the *pattern*
> encodes Ω(m) bits that a single range-counting query reveals only o(1) of (low coverage), so locating
> it still costs Ω(m) queries.

This escapes the `√p/m` single-cell cap outright (the cap is a single-cell theorem; it says nothing
about correlated differences). The new, harder obstruction it must defeat is no longer C1-geometric but
C2/C3-informational: a bulk shift is cheaply *estimable* by coarse counting queries, so the construction
must hide the Ω(m) information in a *pattern* that aggregate counts cannot reveal — re-winning C2 (O(1)
coverage) and C3 (Ω(m), dodging the B2 Ω(log m) trap) on a coding-theoretic distribution rather than the
frozen single-needle-in-haystack one. Whether such a distribution exists is open and is **not refuted by
the solver's argument**, which is a single-cell theorem.

**Recommendation:** the `c=2/3` impossibility correctly KILLS the single-needle equal-cardinality
gadget-packing route — bank it as a refuted route (N*) for that axis. It does **not** kill the
Ω(n^{1/2−o(1)}) target. A fresh attacker brief on the **multi-needle / planted-pattern** distribution
(target: a 2-class pattern hard distribution with Θ(w(P)) inter-class gap + low counting-coverage +
Ω(m) locating cost) is the live next move.

---

### Numerical artifacts (exact EMST, Delaunay+Kruskal, self-checked)
- `attack_loop/auditB_probe.py` — gap_frac vs n at p≈m≈n^{1/2}; strip-vs-grid and cluster-vs-grid (C).
- `attack_loop/auditB_probe2.py` — sparse-placement (A): region-shrink leaves gap_frac invariant;
  decouple only "helps" via invalid footprint overlap.
- `attack_loop/auditB_probe3.py` — multi-needle (D): m/2-heavy gives gap_frac 2–4 (constant); per-needle
  unchanged at √p/m. Hierarchical tight-cluster sparse (A): lower fraction (backbone-dominated).
All confirm: single-cell fraction tracks √p/m; only the correlated multi-cell difference clears Θ(1).
