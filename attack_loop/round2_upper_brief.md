# Round 2 (UPPER-bound line) — Brief to attacker (rectangle-native estimator, avoiding cell sampling)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> Round 1 fixed the diagnosis: the source's √n is NOT the BFS depth — it is the **CellSampling**
> primitive, which has its OWN Ω(√n) lower bound. But MST-weight is provably **not** √n-hard. This
> brief asks for an estimator that exploits that gap. Read §3 (proven substrate) before designing.

---

## 1. The setting (frozen)

P ⊂ [Δ]² integer grid, **|P| = n**, spread **Δ = O(n)**. w(P) = Euclidean MST weight. Orthogonal
range-**counting** oracle: query R (axis-aligned rectangle) → exact integer **|P ∩ R|**. Cost =
#queries. Want: a randomized algorithm outputting a **(1±ε)** estimate of w(P) (fixed ε∈(0,1)) with
constant success probability, in **o(√n)** queries — ideally **Õ(n^{1/3})**.

**Known:** upper Õ(√n) (Driemel et al., SoCG 2025, arXiv:2504.15292, Thm 30); lower Ω(n^{1/3})
(their Lemma 32, a HARD FLOOR — no algorithm beats n^{1/3}).

---

## 2. The CRT reduction (frozen — this is the quantity to estimate)

w(MST) is captured by a sum over **Õ(1)** dyadic scales. With λ_i = (1+ε)^i and **c_i = number of
connected components of the spanner when only edges of length ≤ λ_i are kept** (i = 0,…,s,
s = log_{1+ε}(2Δ)):

> **OPT = (n − Δ) + Σ_i λ_i · c_i**, within a (1±ε) factor (Czumaj–Sohler / CRT identity, their Lemma 25).

A spanner edge "is there one of length ≤ r between two cells?" is testable in O(ε^{-2}) range-counting
queries (their Lemma 24). So the algorithmic task is: **estimate the weighted aggregate Σ_i λ_i c_i to
additive error ≤ ε·OPT**, using o(√n) range-counting queries.

---

## 3. What is ALREADY PROVEN (substrate — use freely; do NOT re-attempt the dead routes)

**Verified in Round 1 (codex + independent audit, against the paper + numerics):**

- **U-B1 — CellSampling is Ω(√n) (this is the REAL bottleneck).** arXiv:2504.15292 §4 proves Ω(√n/c)
  queries are needed to (a) draw a *near-uniform* non-empty λ-cell, and (b) estimate **N_i = #non-empty
  λ-cells to O(1)-relative error** — even in 1-D. The source's Thm-30 algorithm pays √n precisely
  because its CRT estimator calls this for seeds + the scale factor. **🔴 Consequence: estimating any
  single c_i (or any single N_i) to relative error is Ω(√n). A sub-√n algorithm must NOT do that for
  each scale.**
- **U-P1 — MST-weight is NOT √n-hard.** The Ω(√n) cell-sampling instance does NOT reduce to MST: its
  hardest case is 1-D, where w(MST) = x_max − x_min **telescopes and is invariant to cell occupancy**
  (uniform vs non-uniform occupancy ⇒ identical MST weight). So a (1±ε)-MST estimator cannot solve cell
  sampling; the only proven MST floor is Ω(n^{1/3}). **This is exactly the slack to exploit: the
  *weighted aggregate* Σ_i λ_i c_i can be estimated with cross-scale cancellation even though no single
  c_i is cheaply (relative-)estimable.** (In 1-D the whole sum collapses to 2 queries.)

**Refuted routes (N*) — do NOT propose:**
- **U-N1:** the CRT estimator with a smaller BFS depth t. Even t = O(polylog) does not help: the
  estimator still needs near-uniform cell *seeds* and N_i, i.e. CellSampling = Ω(√n).
- **U-N2:** "sample a point uniformly, reweight by inverse cell multiplicity (Z = n·β(v)/a_v)." Dead by
  variance: on M = √n singleton cells + one bulk at scale λ=√n, Var[Z] = Θ(nM) ⇒ Ω(√n) samples.

---

## 4. Barriers in force (B*)

- **B-floor: Ω(n^{1/3}) (Lemma 32).** Any claimed query count below n^{1/3} is WRONG.
- **B-cellsampling: do not estimate any single N_i or c_i to relative error** (Ω(√n), U-B1). The
  estimator of Σ_i λ_i c_i must exploit aggregate cancellation, NOT term-by-term relative accuracy.
- **B-multiscale:** the per-scale errors sum over the Õ(1) scales; the total must be ≤ ε·OPT.
- **B-honesty:** neither "o(√n) is easy" nor "√n is necessary for MST" is assumed (U-P1 shows MST is
  not √n-hard, but that is not a guarantee an o(√n) algorithm exists). If a step resists, name it.

---

## 5. The open question (method-agnostic — use ANY method)

> **Design a randomized orthogonal range-counting-oracle algorithm that (1±ε)-estimates w(MST) in
> o(√n) (ideally Õ(n^{1/3})) queries, by estimating the weighted aggregate Σ_i λ_i c_i WITHOUT
> per-scale near-uniform cell sampling and WITHOUT estimating any single N_i / c_i to relative error.**

Candidate direction (a DIRECTION, not mandated; discard freely):
- **Planar Euler / occupancy aggregate.** For each scale, the contracted graph on occupied λ_i-cells is
  planar, so **c_i = V_i − E_i + Z_i** (V_i = #occupied cells, E_i = #adjacent occupied-cell pairs that
  carry a spanner edge, Z_i = cycle rank). Then Σ_i λ_i c_i = Σ_i λ_i(V_i − E_i + Z_i). Even though each
  V_i to relative error is √n-hard, the **weighted aggregate** Σ_i λ_i V_i (and Σ_i λ_i E_i) might be
  estimable directly from exact range-COUNT sums over regions, with cross-scale cancellation — e.g. a
  point/edge contributes to V_i/E_i across a contiguous range of scales, so the scale-weighted sum may
  telescope into a per-point/per-local-feature quantity that coarse counts reveal. (Is Z_i, the cycle
  rank, negligible or separately controllable? Is Σλ_i E_i tied to short-edge structure that O(1)-cover
  counting sees?) Pursue, modify, or abandon freely.
- Other rectangle-native ideas welcome: importance sampling by point (not by cell) with bounded
  variance via geometric spreading; multi-resolution count summaries; estimating Σλ_i c_i via the
  distribution of inter-point gaps that counting queries expose; etc.

Give the algorithm + query-count bound (show o(√n)) + (1±ε)-correctness (per-scale errors sum to
≤ ε·OPT, with success probability), OR a precise obstruction (which step forces √n, and whether it is
a genuine barrier or just this approach). If you can prove a *new* obstruction stronger than
CellSampling — e.g. that estimating Σ_i λ_i c_i to ε·OPT itself needs Ω(√n) for MST — that would settle
the question negatively and is equally valuable (but beware: it must not contradict U-P1 / the 1-D
triviality, and must respect that MST is not cell-sampling-hard).

---

## 6. What we need back

1. **Algorithm** (pseudocode) + **query bound** (o(√n), ideally Õ(n^{1/3})) + **(1±ε)-correctness**
   (every per-scale error ≤ its share of ε·OPT; success prob) — OR the precise resisting step.
2. **Achievable query exponent** (Õ(n^{1/3}) closes-from-above, or best o(√n)).
3. **Updated confidence %** that an o(√n) (resp. Õ(n^{1/3})) range-counting EMST algorithm exists.
4. **Verdict** (algorithm / partial / obstruction / open).
5. *(Optional)* small-scale numerics: exact EMST (scipy), simulate the estimator over a counting
   oracle, plot measured query count vs accuracy vs n.

We will adversarially audit (looking for: a hidden per-scale relative-error estimate = secret cell
sampling = Ω(√n); an undercounted query bound; a scale whose error exceeds its ε·OPT share; a variance
gap; an Ω(n^{1/3})-floor violation). A precise "here is where √n returns" beats an over-claim.
