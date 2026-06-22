# Round 5 (UPPER-bound line) — Brief to attacker (write the COMPLETE rigorous Õ(n^{1/3}) theorem + proof)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> Every algorithmic branch below is ALREADY NUMERICALLY VALIDATED over an exact range-counting oracle
> (independent audit, exact EMST). What remains is the rigorous (1±ε) proof. Your job: state the clean
> theorem and PROVE it. Build on §2–§3; do not re-derive the validated structure.

---

## 1. Setting + target (frozen)

P ⊂ [Δ]² integer grid, |P|=n, Δ=O(n). Orthogonal range-**counting** oracle: query R → exact integer
|P∩R|. Uniform point-sampling p∈P costs O(log Δ) queries (binary search on cumulative counts). Want a
randomized **(1±ε)** estimate of w(MST(P)), success prob ≥ 2/3, in **Õ(n^{1/3})** queries. Õ(n^{1/3})
matches the lower bound Ω(n^{1/3}) (Driemel et al., SoCG 2025, Lemma 32) up to n^{o(1)} ⇒ **closes** the
Ω(n^{1/3}) vs Õ(√n) gap from above. (Any rigorously-proven o(√n) is also a result.)

---

## 2. The reframe that makes it work (frozen, VERIFIED) — the SCALAR cluster-count integral

**w(MST) = (n − Δ) + ∫₀^∞ (c(t) − 1) dt**, where **c(t) = #single-linkage components of P at threshold t**
(points within distance ≤ t are connected). Equivalently, on the (1+ε)-spanner S (MST(S) ≤ (1+ε)·EMST,
edge tests via O(ε⁻²) range counts, source Lemma 24), discretize to scales λ_i=(1+ε)^i (i=0…s,
s=Õ(1)): **w ≈ (n−Δ) + Σ_i (λ_{i+1}−λ_i)·(c(λ_i) − 1)**. VERIFIED: the integral identity holds to ratio
1.0001; **c(λ) − 1 = #(MST edges of length ≥ λ) is a SINGLE SCALAR per scale** — NOT a per-size-bucket
vector. So estimating w reduces to estimating the Õ(1) scalars {c(λ_i)} to a summed error ≤ ε·OPT.

🔴 This is the crux that defeats the Round-4 obstruction: the per-size-bucket component-counting lemma
(which is genuinely false / not range-count-implementable on dense slabs) is **not needed** — the weight
telescopes onto the scalar c(λ).

---

## 3. The validated algorithm (frozen substrate — prove it rigorously)

Estimate each scalar c(λ) (equivalently c(λ)−1 = #long MST edges ≥ λ) with the cheaper of two branches:

- **(small-λ branch, λ ≤ n^{1/3}) — point-sampling.** [VERIFIED Õ(λ), accuracy→1] Bucket component
  sizes m∈[a,2a); draw T_a=Θ((λ/a)ε⁻²·polylog) uniform points; explore each sampled point's scale-λ
  component up to 2a points (range-count probes + local spanner-edge tests); Horvitz–Thompson estimate
  (output n/m on a size-[a,2a) hit, 0 else); truncate components of size m>K=Θ(λL/ε) (they contribute
  ≤ λ·n/K ≤ εOPT/L). Sum over buckets gives c(λ). Cost/bucket = T_a·O(a·polylog)=Õ(λ).
- **(large-λ branch, λ > n^{1/3}) — 2-axis λ-cell estimator.** [VERIFIED Õ(√(n/λ)), accuracy→1] estimate
  the scalar c(λ) directly by random 2-axis λ-cell probing (a nonempty λ-cell that is a separate blob =
  one component); cost ~ √(#nonempty λ-cells). For every WEIGHT-RELEVANT scale (λ·c(λ)/n = Ω(1)) it
  holds that **c(λ)=O(n/λ)**, so the cost is Õ(√(n/λ)); strata with c(λ) large but λ·c(λ)/n=o(1) carry
  o(OPT) weight and are truncatable.
- **min(Õ(λ), Õ(√(n/λ))) ≤ Õ(n^{1/3})** per scale (peak at λ=n^{1/3}); over Õ(1) scales ⇒ **Õ(n^{1/3})**.
- **(dense-gadget stratum) — coarse scan.** [VERIFIED Õ(n^{1/3})] A single dense block is ONE component
  (Õ(1) persistence; its B−1 internal edges go into the (n−Δ) term), so weight-relevant dense anomalies
  must TILE into a Θ(n^{1/3}) family (the vise); a 1-D scan of the Θ(n^{1/3}) coarse cells finds them.

---

## 4. Barriers (B*) / what the proof must respect
- **Ω(n^{1/3}) floor** — any query count < n^{1/3} is WRONG.
- **No relative-error N_i / per-bucket counts** (= cell sampling = Ω(√n), U-B1). c(λ) is a scalar
  recovered by a HITTING estimator (point-sampling or 2-axis cells), NOT N_i to relative error.
- **No √n wall** (VERIFIED): a constant-fraction large-λ weight gap is coarsely visible (random λ-box
  hit-frac ≈0.27, 2λ-box ≈0.996), so the spread-vs-concentrate vise forbids a √n hard instance; do not
  produce one (it would contradict U-P1 and the verified vise).

---

## 5. The task — state and PROVE the theorem

> **Theorem (to state + prove): there is a randomized algorithm that, given range-counting-oracle access
> to P⊂[Δ]² (|P|=n, Δ=O(n)), outputs a (1±ε)-multiplicative estimate of w(MST(P)) with probability ≥2/3
> using Õ(n^{1/3}) = n^{1/3}·poly(log n, 1/ε) orthogonal range-counting queries.**

Provide the COMPLETE proof. The validated structure (§2–§3) is the algorithm; you must rigorously
establish:
- **(P1) Query bound Õ(n^{1/3}):** the per-scale min(Õ(λ), Õ(√(n/λ))) accounting; the Õ(1) scale count;
  the dense-gadget scan; the spanner-edge-test cost (O(ε⁻²)/test, Lemma 24); uniform-sampling cost
  (O(log Δ)). Sum to n^{1/3}·polylog.
- **(P2) (1±ε)-correctness — the real remaining work:**
  - **small-λ branch:** Horvitz–Thompson unbiasedness + variance ⇒ each c(λ) (resp. its bucketed pieces)
    estimated to additive error ≤ its share of ε·OPT/(λL); median-of-means for the success probability;
    the truncation error bound (≤ εOPT/L).
  - **large-λ branch:** the 2-axis λ-cell estimator for the SCALAR c(λ): prove a clean (1±ε) (or small
    additive) bound — **debias the small constant bias** (audit measured ratio ≈1.01 on grid-blobs) and
    bound its variance; prove the **hitting/coupling lemma** that turns "weight-relevant ⇒ c(λ)=O(n/λ)
    and the live cells are spread over Ω(c(λ)) distinct λ-cells" into a worst-case √(n/λ) sample bound
    (the audit measured constant hit-frac; you must prove it in the worst case). Handle the
    c(λ)-large-but-low-weight strata by truncation.
  - **error budget:** the Õ(1) per-scale additive errors sum to ≤ ε·OPT; combine the (n−Δ) term and the
    spanner (1+ε) distortion; give the overall (1±O(ε)) guarantee and rescale ε.
  - **dense-gadget stratum:** its contribution is estimated to within its ε·OPT share and integrated.
- **(P3) Range-counting implementability** of every primitive (uniform sampling; the scale-λ component
  exploration up to size 2a; the 2-axis λ-cell nonempty/blob test; the coarse scan).

If a step genuinely cannot be closed, identify it precisely (it must not re-introduce per-bucket
component counting or a √n hitting cost, given §2/§4) — a precise residual is valuable. Otherwise, give
the clean theorem statement (with the exact poly-log/ε exponents) and the full proof.

---

## 6. What we need back
1. **The theorem statement** (exact Õ(n^{1/3}) bound, hypotheses, success prob).
2. **The full proof**: (P1) query bound, (P2) (1±ε) correctness with all variance/error-budget/coupling
   lemmas proved, (P3) implementability.
3. **Confidence %** that the proof is complete and audit-surviving (and separately for any residual gap).
4. **Verdict:** theorem-proved / proved-modulo-precisely-stated-residual / obstruction / open.
5. *(If your sandbox allows Python)* re-confirm the end-to-end query count = Õ(n^{1/3}) and accuracy
   → (1±ε) on the islands, diagonal-filament, dense-gadget, and random instances; else say so.

We will run ≥3 independent adversarial audits (each hunting: a hidden relative-error N_i / per-bucket
count = cell sampling = √n; an unbounded-variance or biased estimator; a scale whose error exceeds its
ε·OPT share; a √n hitting cost smuggled into the large-λ coupling; an Ω(n^{1/3})-floor violation; a
non-implementable primitive). A clean, audit-surviving proof CLOSES the Driemel et al. gap from above.
