# Round 3 — GPT-5.5-Pro response (verbatim, human-relayed 2026-06-21) — REFUTES ITS OWN ROUND-2 CLOSURE

> Pasted by the owner. LaTeX noise cleaned; all claims preserved. **Pro now says the round-2 closure is
> NOT valid:** the [1]-Thm-30 repair fails and the seed-reuse is unsound, with a concrete counterexample.
> Citations: [1]=arXiv:2504.15292; [2]=Chazelle–Rubinfeld–Trevisan (MST approx, SICOMP); [3]=Czumaj et al.
> Decisive numeric test: `attack_loop/webpro_verify_round3_counterexample.py`.

---

**Verdict (Pro):** The Theorem-30 repair does NOT work. Two load-bearing identifications fail:
**range count on Q ≠ range count on P**, and the source algorithm's "constant number of seeds" hides a
Θ̃(√K)-cost occupied-cell sampler. More seriously, **reusing one polylog vertex pool across all CRT
thresholds is not generally valid** — the CRT MST analysis uses independence across threshold calls when
summing their variances; fresh traversal coins do NOT remove the covariance from shared starting
vertices. There is a concrete geometric support instance on which the shared-pool estimator misses a
constant fraction of w(MST(Q)). **So Lemma 3 is NOT repaired; the unconditional Õ(n^{1/3}) theorem is NOT
proved.**

## 1. Why the direct application of Theorem 30 fails
For Q={z_C : P∩C≠∅} and a rectangle R in support-center coords with R↑ = union of fine cells whose
centers lie in R: **emptiness** on Q is one P-count (Q∩R≠∅ ⟺ P∩R↑≠∅). But **exact counting differs**:
|Q∩R| = Σ_{z_C∈R} 1[|P∩C|>0] (occupied-cell count) whereas one P-query gives |P∩R↑| = Σ_{z_C∈R} |P∩C|
(point count). These differ arbitrarily (occupancies 1 and M → support count 2 vs point count M+1).
**What Thm 30 samples:** at scale i the vertices are nonempty cells of a coarser grid; §5.3 uses only
r=O(η⁻²) output seeds but obtains them via **Algorithm 1, the occupied-cell sampler**, which internally
draws **x=Θ(√K log K) uniform input points** + queries their cell occupancies. Simulating those x support
samples by rejection from P costs **Θ̃(√K·n/K)=Θ̃(n/√K)** = **Θ̃(n^{2/3})** for K=n^{2/3}, NOT n^{1/3}.
Reusing the √K internal pool across scales removes only log repetition, not the √K samples; and Algorithm
1 needs coarse-cell occupancies w.r.t. Q (distinct occupied-fine-cell counts), not single P-counts. So
"one range count on Q = one range count on P" is true for emptiness, FALSE for counting, insufficient.

## 2. Why cross-threshold seed reuse is not automatically sound
The CRT estimator samples O(η⁻²) vertices per threshold; its MST proof uses Var(Σĉᵢ)=ΣVar(ĉᵢ) — relying
on **independent threshold calls** (explicit in the CRT MST theorem proof [2]). Reusing the same starts
at every threshold preserves marginals but introduces covariance: Var(Σĉᵢ)=ΣVar(ĉᵢ)+2Σ_{i<j}Cov(ĉᵢ,ĉⱼ).
Fresh BFS/stopping coins do NOT eliminate the covariance of the conditional means E[ĉᵢ|q_1..q_r]. A
per-threshold union bound does not repair this with O(log T) seeds (the per-threshold CRT guarantees are
deliberately much coarser than the accuracy needed after naively summing absolute errors; the proof gets
accuracy from variance AGGREGATION, not per-threshold O(W/T)).

## 3. A geometric counterexample to the shared-pool argument
K=s², h=s, D=s²=K. Q = (A) K−s points on an h-spaced square grid + (u_1..u_s) satellites on a ray with
dist(u_1,A)=D, |u_{j+1}−u_j|=D. w(MST(A))=Θ(Kh)=Θ(s³); satellite chain Θ(sD)=Θ(s³); so W_Q=Θ(s³). For
2h ≤ t ≤ D/2: A connected, every satellite isolated ⇒ c_Q(t)=s+1; ∫_{2h}^{D/2}(c_Q−1)dt = s(D/2−2h) =
Θ(s³)=Θ(W_Q). **Satellites = a constant fraction of the MST weight.**
**What a shared pool sees:** a uniform support point is a satellite w.p. s/K=1/s; a shared pool of
r=polylog(K)=o(s) misses every satellite w.p. (1−1/s)^r=1−o(1). Conditional on that, all sampled vertices
lie in A; the ideal Y_t(q)=1/|C_t(q)| is 1 on satellites, 1/K on A, so K·E[Y_t]=s+1 but the empirical
estimate (no satellite) ≈ 1. The error persists over the length-Θ(D) interval ⇒ additive Θ(sD)=Θ(W_Q).
Var(K·Y_t)=Θ(s³); to estimate c_Q(t)=Θ(s) to additive O(s) needs r=Ω(s)=Ω(√K) uniform starts at that
threshold. Polylog starts cannot. (Traversal randomness can't help: conditional on no satellite start, no
traversal enters a satellite component.)
**Why clipping doesn't rescue it:** in round 2, L=Θ(h); satellite edges have length D≫L, so their excess
contributes Θ(s(D−L))=Θ(W_Q) to the support TAIL. The clipped Â_L(Q) can be perfect while a shared-seed
Ŵ_Q misses the satellites ⇒ Ŵ_Q−Â_L(Q) still has constant relative error.

## 4. Realization as an operative P-instance
n=s³, K=s², h=s, D=s². Inside every occupied h-cell place s distinct integer-grid points on a unit
segment. Then |P|=Ks=s³=n; the occupied-h-cell support = Q. All contributions Θ(n): within-cell Θ(Ks)=
Θ(n), dense support-grid Θ(Kh)=Θ(n), satellite-chain Θ(sD)=Θ(n). So W=Θ(n), W/K=Θ(s)=Θ(h); fits a square
of side Θ(sD)=Θ(s³)=Θ(n) ⇒ Δ=O(n), K=n^{2/3}, problematic scale at the operative support resolution.

## 5. What can still be repaired cleanly (the nonorthogonal-WSPD part — NOT the obstruction)
The cone-approximate-NN call can be replaced by a **nested-cone rectangular search**: nested cones
C_j⁻⊂C_j⁺ (inner cover all directions, outer angular diameter ≤π/4), geometric distance shells
[r,(1+γ)r) (γ=Θ(η)), cover C_j⁻ within each shell by O_η(1) axis-aligned rectangles ⊂ C_j⁺ extending
radially by ≤(1+O(η)); scan shells near→far by support-emptiness. Returned z satisfies z∈C_j⁺ and
|p−z|≤(1+O(η))|p−y| for every target y∈C_j⁻; O_η(log(Δ/h)) support-emptiness queries (polylog P-counts).
Czumaj's reachability proof survives this (common cone ≤π/4 + neighbor no farther). **But this does NOT
remove the support-seed problem.**

## 6. The true remaining Lemma 3 (sharper)
> Given an implicit K-point grid support Q with (1) rectangle EMPTINESS on Q = one P-count, (2) uniform
> support sampling = Õ(n/K), (3) local directional/WSPD adjacency = polylog P-counts, estimate w(MST(Q))
> within (1±η) using Õ_η(√K + n/K) total P-queries.
Neither published engine gives this black box: [1] needs occupied-cell sampling + distinct support
counts (Algorithm 1 = Õ(√K) ops WITH genuine access to Q); Czumaj/CRT can use only actual support
vertices, but threshold-wise independent starts cannot be replaced by one polylog shared pool. A
successful repair must use the explicit spatial active-block info to account for low-mass blocks (the
satellite chain), not hope uniform seeds stumble into them.

## 7. Numerical test (Pro's)
s=32,64,128; K=s², n=s³, h=s, D=s²; (K−s) dense h-spaced cells + s satellite cells spacing D; s points per
occupied cell. Compare: (1) fresh independent seeds per threshold; (2) one shared pool of r=⌈20 log K⌉;
(3) exact ∫_{2h}^{D/2}(c_Q−1)dt. The shared-pool estimator should miss the satellite contribution
whenever its pool has no satellite (prob (1−1/s)^r) — a constant fraction of W_Q and of the tail.

## Updated confidence (Pro)
- Failure of the direct Thm-30 substitution: **0.99**
- Exact occupied-cell sampling accounting from the source: **0.99**
- Failure of generic cross-threshold seed reuse: **0.97**
- Dense-block + satellite-chain counterexample: **0.94**
- Orthogonal nested-cone implementation: **0.87**
- Unconditional Õ_ε(n^{1/3}) theorem: **NOT established.**
The remaining gap is no longer nonrectangular WSPD bookkeeping; it is recovering geometrically important,
low-support-mass components without paying for Θ(√K) genuinely independent support samples.

[1] arXiv:2504.15292 · [2] Chazelle–Rubinfeld–Trevisan, SICOMP · [3] Czumaj et al.
