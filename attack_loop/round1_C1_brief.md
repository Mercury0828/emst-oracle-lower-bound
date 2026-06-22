# Round 1 — Brief to attacker (Crux C1: the space-efficient heavy gadget)

**To:** external solver (codex GPT-5.5-xhigh). **From:** orchestrator. **Date:** 2026-06-20.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve the open question in §5; report per §6.

---

## 1. The exact target (a precise claim to establish or refute)

Work in the Euclidean plane. Let a "gadget" be a finite multiset of points placed inside one axis-aligned
**cell** (a square). Consider a global instance built from **m = Θ(n^{1/2})** congruent cells tiling a
square domain **[Δ]²** with **Δ = O(n)**, total point budget **|P| = n**, so each cell holds
**p = n^{1/2 + o(1)}** points.

**Construct an explicit pair of gadgets (HEAVY, SPARSE), each using the SAME number p of points
(equal cardinality), such that:** taking all m cells SPARSE versus making exactly ONE cell HEAVY (the
rest SPARSE) changes the global Euclidean MST weight w(P) by at least **ε·w(P)** for a fixed constant
ε ∈ (0,1) — i.e. the single heavy cell's excess is a constant fraction of the *whole* MST weight.

Equivalently: at the equal-cardinality budget p = n^{1/2+o(1)}, with per-cell heavy EMST cost Θ(n^a)
and sparse EMST cost Θ(n^b) (a > b), determine the best achievable (a, b) and decide whether the
single-heavy-cell global excess clears the constant-fraction threshold
**Θ(n^a) − Θ(n^b) ≥ ε·w(P)**, where w(P) includes the inter-cell backbone (the MST edges that connect
the m cells across the domain), not only the per-cell costs.

**If a constant fraction is unreachable at p = n^{1/2+o(1)}**, find and PROVE the smallest exponent
c ∈ [1/2, 2/3] such that p = n^{c} (equal cardinality) admits a constant-fraction detectable gap with
m = n^{1−c} cells. (This c fixes the strength of the eventual lower bound: c = 1/2 ⇒ the full
Ω(n^{1/2−o(1)}) target; larger c ⇒ a weaker Ω(n^{1−c}) result.)

---

## 2. Frozen substrate (P*) — use freely, do NOT re-derive

- **Model.** P ⊂ [Δ]² (integer grid), |P| = n, spread/domain side Δ = O(n). w(P) = Euclidean MST
  weight. Budget identity: (#cells) × (points/cell) ≤ O(n).
- **Source construction** (Driemel–Monemizadeh–Oh–Staals–Woodruff, SoCG 2025, arXiv:2504.15292 §6,
  verified from the PDF). Domain split into **16·n^{1/3} cells, each of side 4·n^{5/6}**. Each gadget
  has **n^{2/3} points** (equal cardinality). Two gadget types:
  - **HEAVY ("uniform"):** the p points spread on a uniform ~√p×√p grid filling the cell of side s.
    Per-cell EMST cost **Θ(n^{7/6})** at p=n^{2/3}, s=n^{5/6} (≈ s·√p: nearest-neighbour spacing
    ≈ s/√p, ≈ p−1 edges).
  - **SPARSE ("strip"):** the p points along a 1D strip (a line segment) of length ≈ s inside the
    cell. Per-cell EMST cost **Θ(n^{5/6})** (≈ s, a path along the segment).
  - This pair, with one hidden heavy cell among 16·n^{1/3}, yields the source's **Ω(n^{1/3})** query
    lower bound. The cell count Θ(n^{1/3}) is forced by the budget (16n^{1/3}·n^{2/3}=16n).
- **The lever (why this is being attempted).** If an equal-cardinality heavy gadget exists at
  p = n^{1/2+o(1)} with a constant-fraction detectable gap, then **m = Θ(n^{1/2})** independent hidden
  candidate cells fit the same Δ=O(n)/|P|=n budget — the prerequisite for an Ω(n^{1/2−o(1)}) lower
  bound (a separate downstream obligation, not your task here).

---

## 3. Refuted / screened routes (N*) — do not simply re-propose these

- **Naive thinning of the source pair** (HEAVY=uniform grid, SPARSE=strip), keeping equal
  cardinality, has per-cell cost ratio (heavy/sparse) ≈ √p (= n^{a−b}). For a single heavy cell among
  m cells to shift w(P) by a constant fraction, the excess Θ(n^a)−Θ(n^b) must be ≳ (per-cell sparse
  cost)·m (the order of the total). With the uniform/strip pair this needs ratio ≈ m, but the pair
  only delivers ratio ≈ √p. At p=n^{1/2} that is √p = n^{1/4} vs the needed m = n^{1/2} — a polynomial
  shortfall. A small-scale EXACT-EMST screen confirms the gap *fraction* declines toward p=n^{1/2}
  (e.g. at n≈8100 the one-heavy/all-sparse w(P) gap fraction falls to ≈0.06 at p≈n^{1/2}, while it is
  Θ(1) at p≈n^{2/3}). **This is a screen TREND, not a proof of impossibility** — but it means the
  uniform-grid-vs-strip geometry is insufficient at p=n^{1/2}. Do not re-submit that exact pair; the
  question is whether a *different* equal-cardinality geometry achieves a larger cost ratio per point.

---

## 4. Barriers in force (B*) — any construction must respect these

- **B1 (budget).** (#cells)×p ≤ O(n) and Δ = O(n). The heavy excess must clear a constant fraction of
  the **global** w(P), which includes the **inter-cell backbone** (the MST cost of connecting the m
  cells across [Δ]²). A construction that spreads cells far apart to gain per-cell cost may inflate the
  backbone and wash out the gap — account for the backbone explicitly.
- **B-eq (equal cardinality — load-bearing; do NOT relax without flagging).** HEAVY and SPARSE must
  hold the *same* number of points p. Reason (a downstream coupling, stated as a constraint, not a
  method): a later per-query range-**counting** argument needs a fully-contained cell to be
  *invisible* to a counting query, which holds only if heavy and sparse have equal point count; an
  unequal-cardinality gap is detectable by counting the points in a large rectangle and would defeat
  the downstream step. So the PRIMARY question is the equal-cardinality one. (You MAY, as a secondary
  report, say whether *relaxing* to unequal cardinality changes the achievable exponent — that informs
  how tightly C1 and the downstream step are coupled — but the primary target is equal cardinality.)
- **B-honesty.** This is genuinely open; neither "impossible" nor "easy" is assumed. If your methods
  cannot settle it, say so plainly and state the precise obstruction.

---

## 5. The open question (method-agnostic — use ANY method)

At the equal-cardinality budget p = n^{1/2+o(1)} (m = Θ(n^{1/2}) cells, Δ = O(n), |P| = n):

> **Does there exist an equal-cardinality (HEAVY, SPARSE) gadget pair whose single-heavy-cell excess
> is a constant fraction of the global Euclidean MST weight w(P)?**

Use any geometry — hierarchical / multi-scale / fractal / nested-cluster / space-filling / lattice /
randomized — anything that maximises the heavy-vs-sparse EMST-cost separation *per point* under equal
cardinality, while respecting B1 (including the backbone). Derive the achievable per-cell exponents
(a, b) and verify Θ(n^a) − Θ(n^b) ≥ ε·w(P). If a constant fraction is unreachable at p=n^{1/2+o(1)},
determine and prove the smallest c ∈ [1/2, 2/3] with p=n^c that works.

A useful sub-question (optional, if it helps): for p points of EQUAL cardinality confined to a cell of
side s, what is the achievable RANGE of EMST cost — the minimum (how small can a p-point gadget's EMST
be?) and the maximum (how large?) — as a function of (p, s)? The heavy/sparse separation is bounded by
this range; characterising it may settle the question directly.

---

## 6. What we need back

1. **A full construction + Euclidean-MST-cost analysis** — explicit HEAVY and SPARSE gadgets (point
   layouts), their per-cell EMST costs Θ(n^a), Θ(n^b), the inter-cell backbone cost, and the resulting
   single-heavy global gap fraction (heavy excess)/w(P) — OR a precise statement of where the
   construction breaks and why.
2. **The achievable exponent:** the full p=n^{1/2+o(1)} constant fraction, or the smallest provable c.
3. **An updated confidence %** that an equal-cardinality C1 gadget exists at p = n^{1/2+o(1)}.
4. **A clear verdict** (constructed / partial / open-with-obstruction).
5. *(Optional but welcome)* a small-scale computational sanity check of your proposed gadget's exact
   EMST (you may write/run code in your working directory).

Be rigorous: state every asymptotic claim with its reasoning. We will independently adversarially
audit your reply (looking for a missing backbone term, a hidden cardinality cheat, an EMST-cost
miscalculation, or an unstated assumption). A precise "here is exactly where it breaks" is more useful
than an over-claimed construction.
