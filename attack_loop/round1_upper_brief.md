# Round 1 (UPPER-bound line) — Brief to attacker (a sub-√n range-counting EMST algorithm)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> This is an ALGORITHM-DESIGN task (an upper bound), not a lower bound. Goal: estimate the Euclidean
> MST weight with FEWER range-counting queries than the known Õ(√n).

---

## 1. The setting (frozen)

Points P ⊂ [Δ]² (integer grid), **|P| = n**, spread **Δ = O(n)** (a preprocessing step lets us assume
Δ = O(n/ε)). w(P) = Euclidean MST weight. An **orthogonal range-counting oracle** answers a query
rectangle R (axis-aligned) with the **exact integer count |P ∩ R|**. Cost = number of queries. We want
a randomized algorithm that, with constant success probability, outputs a **(1±ε)-multiplicative
estimate of w(P)** for a fixed constant ε ∈ (0,1), using as **few queries** as possible.

**Known bounds (Driemel–Monemizadeh–Oh–Staals–Woodruff, SoCG 2025, arXiv:2504.15292):**
- **Upper: Õ(√n)** queries (their Theorem 30). ← the bound we want to beat.
- **Lower: Ω(n^{1/3})** queries (their Lemma 32; any o(n^{1/3})-query algorithm has constant
  multiplicative error). ← a HARD FLOOR: no algorithm can beat n^{1/3}.

**Target of THIS task:** an algorithm using **o(√n)** queries — ideally **Õ(n^{1/3})** (which would
close the gap up to n^{o(1)} factors). Any polynomial improvement over √n is a result; reaching
Õ(n^{1/3}) is the headline.

---

## 2. The known Õ(√n) algorithm and EXACTLY where its √n comes from (frozen — verified from the PDF)

The source algorithm is a **Chazelle–Rubinfeld–Trevisan (CRT) reduction on a geometric spanner**:

1. **Spanner (implicit).** A quadtree/WSPD spanner S on P with **MST(S) ≤ (1+ε)·EMST(P)**; edge lengths
   quantized to scales (1+ε)^i. S is never built explicitly: given a cell-pair, "is there a spanner
   edge of length ≤ r?" is testable in **O(ε^{-2}) range-counting queries** (their Lemma 24).

2. **MST-weight = a sum of per-scale component counts (CRT / Czumaj–Sohler identity, their Lemma 25).**
   Let **c_i = number of connected components of S_i**, where S_i keeps only spanner edges of length
   ≤ (1+ε)^i, for i = 0,…,s with **s = log_{1+ε}(2Δ) = Õ(1) scales**. Then
   > **OPT = Σ_i (1+ε)^i · (c_{i−1} − c_i) = (n − Δ) + Σ_i (1+ε)^i · c_i**, within a (1±ε) factor.
   (Uses |M_i| = c_{i−1} − c_i = #MST edges in length band [(1+ε)^i, (1+ε)^{i+1}], cut property.)
   So estimating w(P) reduces to estimating each **c_i** to sufficient accuracy.

3. **Per-scale component-count estimation (the cost driver).** At scale i: vertices = **non-empty cells
   of a grid of side (1+ε)^i** (grid-contraction, their Lemma 26 — all points in such a cell are one
   vertex without changing c_i). It uses the **CRT component-count estimator** (#components = Σ_v φ(v),
   φ(v) = d(v)/(2m(v)), φ=1 if isolated): draw **r = O(ε^{-2}) random seed cells**; for each seed run
   **BFS in the cell-adjacency graph until it visits t vertices**; if BFS exceeds t, the component is
   "large" → contributes 0; else compute its size exactly. Each visited vertex costs O(ε^{-2}) range
   queries (Lemma 24). Return ĉ_i = (n̂/r)·Σ φ_j (n̂ = O(1)-relative estimate of #non-empty cells).

4. **🔑 WHERE THE √n COMES FROM (the exact bottleneck — this is the slack to remove).** The number of
   scales is Õ(1) and the seed count is r = O(ε^{-2}); both are cheap. The cost is dominated by the
   **per-seed BFS exploration depth t, which the source hard-codes to t = √n**:
   - total queries ≈ (#scales) · r · **t** · O(ε^{-2}) = **Õ(t) = Õ(√n)**.
   - Why t = √n: the CRT estimator's additive error in c_i is **O(n / t)** (the points in "large"
     components it truncates), which becomes weight error (1+ε)^i·(n/t); the requirement is
     (1+ε)^i·(n/t) ≤ ε·OPT, met via OPT ≥ (#non-empty cells)/4·(1+ε)^i (planar 4-coloring). **Error ∝ n/t,
     cost ∝ t ⇒ balanced at t = √n.** The source sets t = √n UNIFORMLY across all scales and does NOT
     optimize it per scale or per instance.

---

## 3. The slack (frozen facts — the bottlenecks do NOT coincide)

- The **upper-bound** √n is the BFS depth t = √n inside the component-count estimator, applied
  **uniformly at every scale** — a worst-case error-vs-cost balance n/t.
- The **lower-bound** n^{1/3} (Lemma 32) is about **locating one anomalous cell among 16·n^{1/3} cells at
  a single coarse scale** (≈ n^{5/6}; a hitting/needle-in-haystack argument about query *placement*) —
  it says NOTHING about estimator variance or BFS depth. So the √n is not forced by the known lower
  bound; the gap is genuinely open.
- The component-count estimator (CRT, Lemma 27) was designed for a **bounded-degree graph-adjacency
  oracle** (you may only walk edges). Here the available primitive is a **range-COUNTING oracle** —
  it returns exact integer counts |P∩R| for any axis-aligned rectangle, which is far richer than
  edge-walking (e.g. it counts points/occupied sub-cells in a region in O(1) queries). The source's
  estimator does not exploit this richer primitive beyond the per-edge test of Lemma 24.

---

## 4. Barriers in force (B*) — any algorithm must respect these

- **B-floor: Ω(n^{1/3}) (Lemma 32).** No algorithm uses o(n^{1/3}) queries; any claim below n^{1/3} is
  WRONG. The best achievable is Õ(n^{1/3}).
- **B-CRT-tradeoff.** In the CRT estimator as stated, additive count error ∝ n/t and cost ∝ t; naively
  lowering t below √n increases the weight error above ε·OPT. A faster algorithm must genuinely reduce
  *error-per-query* (a better/ different estimator, or scale-/instance-adaptive accuracy), not merely
  set t smaller. Show the (1±ε) guarantee still holds.
- **B-multiscale.** w(P) = Σ over Õ(1) scales; the estimate must be (1±ε) at EVERY scale simultaneously
  (the per-scale errors sum). An improvement at one scale that breaks another is not a win.
- **B-honesty.** Neither "o(√n) is easy" nor "√n is necessary" is assumed. If your method cannot beat
  √n, say so and state precisely which step resists.

---

## 5. The open question (method-agnostic — use ANY method)

> **Design a randomized orthogonal range-counting-oracle algorithm that (1±ε)-estimates the Euclidean
> MST weight of n points in [Δ]² using o(√n) queries — ideally Õ(n^{1/3}).**

Equivalently (given §2): estimate every per-scale component count c_i to additive error ≤ ε·OPT/(1+ε)^i,
for all Õ(1) scales simultaneously, in **n^{1/3+o(1)}** total range-counting queries — i.e. remove the
t=√n CRT truncation cost.

Candidate attack surfaces (DIRECTIONS, not mandated, not claimed to work — discard freely):
- **Scale-adaptive depth.** t=√n is uniform; the required accuracy ε·OPT/(1+ε)^i and the number of
  non-empty cells both vary strongly with scale. Is a scale-dependent t_i (deep only where needed) — or
  a different per-scale estimator — enough to make Σ_i (cost at scale i) = n^{1/3+o(1)}?
- **Counting-native component estimation.** Exploit that the range-counting oracle gives exact
  occupied-(sub)cell counts in O(1) queries (unlike the graph-adjacency model CRT assumes). Can c_i (or
  c_{i−1}−c_i directly) be estimated to the needed accuracy from counts/occupancies without √n-deep BFS?
- **Instance-adaptive / hierarchical** exploration that pays deep exploration only on the few hard
  (coarse, few-cell) scales where exact counting is cheap.

Give the algorithm, its query-count analysis, and the (1±ε)-correctness proof — OR, if you conclude the
CRT route (or all routes) cannot beat √n, state the precise obstruction (which step forces √n, and
whether a non-CRT estimator could evade it). A clean obstruction is also valuable.

---

## 6. What we need back

1. **An algorithm** (pseudocode) + **query-count bound** (show it is o(√n), ideally Õ(n^{1/3})) +
   **(1±ε)-correctness** (show every per-scale error sums to ≤ ε·OPT, with the success probability) —
   OR a precise statement of which step resists and why.
2. **The achievable query exponent** (Õ(n^{1/3}) "closes from above", or the best o(√n) you can prove).
3. **An updated confidence %** that an o(√n) (resp. Õ(n^{1/3})) range-counting EMST algorithm exists.
4. **A clear verdict** (algorithm-found / partial / obstruction / open).
5. *(Optional)* a small-scale numeric sanity check: build point sets, compute exact EMST (scipy
   Delaunay + Kruskal), simulate your estimator over a range-counting oracle, and report measured
   query count vs accuracy as n grows.

Be rigorous and concrete. We will independently adversarially audit the reply (looking for: an
underestimated query count, a hidden Ω(n^{1/3})-violating claim, a scale whose error is not actually
≤ ε·OPT/(1+ε)^i, a variance/Chebyshev gap, or an estimator that silently needs the √n-deep BFS after
all). A precise "here is exactly where √n is unavoidable" beats an over-claimed algorithm.
