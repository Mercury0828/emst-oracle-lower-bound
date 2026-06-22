# Round 6 (UPPER-bound line) — Brief to attacker (add the DENSE-regime branch; complete the proof)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> Your Round-5 counterexample was correct and valuable: it killed the cost bound "c(λ)=O(n/λ)". This
> brief adds the missing branch that handles exactly your counterexample, and asks you to complete the
> proof. Read §2–§3; the fix re-parameterizes the per-scale cost by c(λ), not by λ.

---

## 1. Setting + target (frozen)

P ⊂ [Δ]² integer grid, |P|=n, Δ=O(n). Orthogonal range-COUNTING oracle: query R → exact integer |P∩R|.
Uniform point-sample p∈P: O(log Δ) queries. A point's "isolation scale" (largest λ with |P ∩
(λ-box around p)| = 1, or more generally the death scale of p's single-linkage component) and a point's
nearest-neighbour distance are computable by binary search on box size: O(log Δ) counts. Want a
randomized **(1±ε)** estimate of w(MST(P)), success ≥2/3, in **Õ(n^{1/3})** queries (closes the Driemel
et al. gap from above; any proven o(√n) is also a result). Floor: Ω(n^{1/3}).

---

## 2. The frame (frozen, VERIFIED) + YOUR Round-5 counterexample (the gap to fix)

**w(MST) = (n − Δ) + ∫₀^∞ (c(t) − 1) dt**, c(t) = #single-linkage components at threshold t (verified
ratio 1.0001). c(λ)−1 = #(MST edges ≥ λ) — a SCALAR per scale. Estimate the Õ(1) scalars {c(λ_i)}.

**Your Round-5 counterexample (accepted as `U-N3`):** uniform q×q grid (n=q²) spacing d=2λ, λ=q/4=Θ(√n):
nearest-neighbour = 2λ ⇒ **c(λ)=n** (all isolated) at a weight-relevant scale (band [0,λ] contributes
λ(n−1)=Θ(n^{3/2}) = const. fraction). So **c(λ) = n ≫ n/λ = Θ(√n)**, and the large-λ 2-axis estimator
costs √(#nonempty cells) = √n, NOT √(n/λ). The Round-4/5 cost bound is dead in this **DENSE regime**.

---

## 3. The fix — re-parameterize per-scale cost by c(λ), add a DENSE branch (frozen direction; verify+prove)

There are TWO complementary estimators for the scalar c(λ) (equivalently the scale-λ persistence
contribution), and the right one depends on c(λ):

- **(DENSE branch — point-sampling, NEW) cost ~ Õ(n / c(λ)).** When c(λ) is LARGE, a large fraction
  (≈ c(λ)/n for singletons; in general the points in small components at scale λ) are "isolated/small
  at scale λ", so uniform point-sampling hits them with probability ≈ c(λ)/n and estimates their
  contribution (via each sampled point's isolation/death scale, by range-counting binary search) in
  **Õ(n/c(λ))** samples. 🔑 This is CHEAP exactly in your counterexample: uniform grid has c(λ)=n ⇒ cost
  Õ(1) (every point isolated, NN distance d trivially measured ⇒ w ≈ n·d). This is the branch Round 5
  lacked.
- **(SPARSE branch — 2-axis λ-cells) cost ~ Õ(√(c(λ))).** When c(λ) is SMALL, the live components are
  spread over ≈ c(λ) nonempty λ-cells; random 2-axis cell probing estimates c(λ) in Õ(√(c(λ))) queries
  (verified ratio→1 in this regime). (When components are singletons #nonempty cells ≈ c(λ).)
- **⇒ per-scale cost ≤ min( Õ(n/c(λ)) , Õ(√(c(λ))) ).** This min over c(λ)∈[1,n] is **MAXIMIZED at
  c(λ)=n^{2/3}, where both equal n^{1/3}** (n/c = √c ⇔ c=n^{2/3}). For c(λ) larger (dense) the point-
  sampling branch is cheaper; for c(λ) smaller (sparse) the 2-axis branch is cheaper. So **every scale,
  every regime, costs ≤ Õ(n^{1/3})** — including your dense counterexample. Over Õ(1) scales ⇒ Õ(n^{1/3}).
  (The algorithm picks the branch adaptively, e.g. by a cheap O(1)-relative pre-estimate of c(λ) at a
  coarse resolution, or by running both at a budget and taking the valid one.)
- **(dense-gadget stratum, unchanged) Õ(n^{1/3}).** A single dense block is ONE component (Õ(1)
  persistence); weight-relevant dense anomalies tile into a Θ(n^{1/3}) family (the vise); a 1-D coarse
  scan finds them.

---

## 4. Barriers (B*) the proof must respect
- **Ω(n^{1/3}) floor** — any query count < n^{1/3} is WRONG.
- **No N_i to relative error** as a black box (= cell sampling = Ω(√n)). NOTE: the DENSE branch does NOT
  estimate N_i to relative error — it point-samples and aggregates per-point isolation scales (a sum,
  not a relative-error cell count). The SPARSE branch uses √(c(λ)) hitting, valid only when c(λ) small;
  show the adaptive choice never invokes a √n-cost estimate.
- **No √n wall** (VERIFIED, the spread-vs-concentrate vise): a constant-fraction weight gap is coarsely
  visible at all λ; do not produce a √n hard instance (it would contradict U-P1 and the vise).

---

## 5. The task — assemble + PROVE the complete theorem

> **Theorem (state + prove): a randomized algorithm (1±ε)-estimates w(MST(P)) for P⊂[Δ]² (|P|=n,
> Δ=O(n)) with prob ≥2/3 using Õ(n^{1/3}) orthogonal range-counting queries.**

Establish rigorously:
- **(P1) Query bound Õ(n^{1/3}):** the per-scale cost = min(Õ(n/c(λ)), Õ(√(c(λ)))) ≤ Õ(n^{1/3}); the
  adaptive branch-selection (and its own cost); the Õ(1) scales; the dense-gadget scan; sampling +
  edge-test costs. CONFIRM your Round-5 counterexample (uniform grid) is now Õ(1) per scale via the
  DENSE branch.
- **(P2) (1±ε)-correctness:** for BOTH branches give the estimator, its unbiasedness/debiasing, and a
  variance bound ⇒ each c(λ) (or its persistence contribution) to additive ≤ its ε·OPT/(Õ(1)) share;
  median-of-means for success prob; truncation of low-weight strata; the error budget summing to ε·OPT;
  the (n−Δ) term and the spanner (1+ε) distortion. **Crucially: prove the DENSE point-sampling branch's
  variance is bounded — the isolation-scale value per sampled point is ≤ λ_max and the fraction is
  c(λ)/n, so the estimator does NOT revert to √n (contrast the Round-2 uniform-point-estimator U-N2,
  whose Θ(√n) variance came from rare HIGH-value points; here the dense regime has COMMON LOW-value
  points — the opposite).** Handle components of all sizes, not just singletons.
- **(P3) Range-counting implementability** of every primitive (uniform sampling; isolation/death-scale &
  NN-distance by binary search; the 2-axis λ-cell test; the coarse scan; the adaptive c(λ) pre-estimate).

If a step still cannot close, identify it precisely (it must not re-introduce a √n cost given §3/§4) —
a precise residual is valuable. Otherwise give the clean theorem + full proof.

---

## 6. What we need back
1. **Theorem statement** (exact Õ(n^{1/3}) bound, hypotheses, success prob).
2. **Full proof**: (P1) query bound incl. the c(λ)-parameterized min and the dense-branch handling of
   the uniform-grid counterexample; (P2) (1±ε) correctness with both branches' variance/debiasing and
   the dense-branch low-variance argument; (P3) implementability.
3. **Confidence %** the proof is complete + audit-surviving (and for any residual).
4. **Verdict** (proved / proved-modulo-precise-residual / obstruction / open).
5. *(If sandbox allows Python)* re-confirm end-to-end query = Õ(n^{1/3}) + accuracy → (1±ε) on islands,
   diagonal-filament, **uniform-grid (your counterexample)**, dense-gadget, random; else say so.

We will run ≥3 independent adversarial audits (hunting: a √n cost smuggled into either branch or the
adaptive selection; an unbounded/biased estimator; a scale whose error exceeds its share; an N_i
relative-error count; a floor violation; a non-implementable primitive; a new c(λ) regime not covered).
A clean, audit-surviving proof CLOSES the gap.
