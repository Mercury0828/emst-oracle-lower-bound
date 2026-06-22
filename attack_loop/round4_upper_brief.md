# Round 4 (UPPER-bound line) — Brief to attacker (formalize the full Õ(n^{1/3}) algorithm)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> The pieces are now in place. A per-scale estimator with cost min(point-sampling, slab) lands EXACTLY
> on the Ω(n^{1/3}) floor (verified numerically). Your job: assemble a COMPLETE, PROVEN Õ(n^{1/3})
> algorithm. Build on §3; do not re-derive it. If correct, this CLOSES the Driemel et al. gap from above.

---

## 1. Setting + target (frozen)

P ⊂ [Δ]² integer grid, |P|=n, Δ=O(n). Orthogonal range-**counting** oracle: query R → exact integer
|P∩R|. Want a randomized **(1±ε)** estimate of w(MST(P)), constant success prob. **TARGET: Õ(n^{1/3})
queries** (or the best o(√n) you can fully prove). Õ(n^{1/3}) matches the lower bound Ω(n^{1/3})
(Lemma 32) up to n^{o(1)} ⇒ closes the gap.

w(MST) = (n − Δ) + **Σ_i λ_i c_i** (λ_i=(1+ε)^i, c_i = #components of the spanner keeping edges ≤ λ_i,
over s = Õ(1) scales). Reframe: **Σ_i λ_i c_i = Σ_{components, all scales} (persistence)** — a component
that first merges at scale λ* contributes Θ(λ*). A spanner edge "∃ edge ≤ r between two cells?" costs
O(ε^{-2}) range-counting queries (source Lemma 24). Uniform point-sampling p∈P (and the count |P∩R|)
are the primitives; a uniform point sample costs O(log Δ) queries (binary search on cumulative counts).

---

## 2. PROVEN substrate (Rounds 1–3 + independent audits + exact-EMST numerics — use freely)

- **U-B1 (cell-sampling Ω(√n)).** Estimating a near-uniform non-empty cell, OR N_i = #non-empty λ-cells
  to O(1)-relative error, is Ω(√n) (even 1-D). 🔴 Do NOT estimate any single N_i/c_i to relative error.
- **U-P1.** MST is NOT √n-hard (cell-sampling does not reduce to MST). Only floor is Ω(n^{1/3}).
- **U-P2.** The "uniform point estimator" X(p)=n·Σλ_i/|comp_i(p)| has Var=Θ(√n) on islands — an artifact
  of UNIFORM sampling. Importance / localized sampling defeats it. The **tile-or-blowup vise**: a
  constant-fraction low-mass stratum either tiles (⇒ findable by localized probes) or scatters (⇒ MST
  value blows up + coarse grid sees it) — so no √n hard instance survives from that structure.
- **🔑 U-P3 (the per-scale cost balance — VERIFIED numerically).** For the persistence contribution at
  a single scale λ:
  - **Point-sampling branch:** the lonely-at-scale-λ fraction is 1/λ; uniform point-sampling + a
    λ-box/disk loneliness test estimates the scale-λ singleton contribution in **O(λ·polylog)** queries
    (verified: the estimated fraction tracks 1/λ for λ=2…√n).
  - **Slab branch:** a scale-λ stratum has ≤ M = n/λ nonempty width-λ slabs per axis, so 1-D slab
    counting localizes/estimates it in **O(√(n/λ)·polylog)** queries (codex's λ=√n filament ⇒ n^{1/4}).
  - **⇒ per-scale cost ≤ min(λ, √(n/λ)), which is MAXIMIZED at λ = n^{1/3} (value n^{1/3})** and is
    smaller for all other λ (verified: the min-column peaks at λ=n^{1/3}). Over Õ(1) scales ⇒ candidate
    **Õ(n^{1/3})**. **No √n lower bound** survives: a constant-fraction MST gap must be SPREAD over
    Θ(n/λ) cells ⇒ a random λ-box hits a differing cell w.p. Θ(1) ⇒ coarsely distinguishable.

- **Dead routes (N*) — do NOT propose:** **U-N1** CRT with smaller BFS depth t (needs cell sampling).
  **U-N2** uniform point estimator alone (Var=Θ(√n)). **Euler totals** Σλ_iV_i, Σλ_iE_i separately
  (V,E,Z=Θ(k²) cancel to c=1; occupancy totals ≠ connectivity).

---

## 3. Barriers (B*)
- **Ω(n^{1/3}) floor (Lemma 32) — now the TARGET to MATCH.** The dense **heavy-gadget** stratum (a
  block, hidden among 16n^{1/3} coarse cells; each query hits ≤4 cells; hit-prob 1/(4n^{1/3})) is NOT a
  lonely-singleton feature; the point-sampling/slab singleton primitive does not see it. Your algorithm
  must detect this stratum too — by **scanning/sampling the Θ(n^{1/3}) coarse cells** — and the TOTAL
  must stay Õ(n^{1/3}). Any claim below n^{1/3} is WRONG.
- No per-scale relative-error N_i/c_i (= cell sampling). Per-scale errors sum over Õ(1) scales ≤ ε·OPT.

---

## 4. The open question (assemble + PROVE the full algorithm)

> **Give a complete randomized algorithm estimating Σ_i λ_i c_i (hence w(MST)) to (1±ε) in Õ(n^{1/3})
> range-counting queries, with full proof: query bound, variance/(1±ε) correctness, success
> probability — handling ALL component strata and the dense-gadget stratum.**

The pieces you must supply (the verified U-P3 handles only the per-scale SINGLETON cost):
- **(a) All component sizes, not just singletons.** Generalize "lonely point" to "point in a small
  (size ≤ k) component at scale λ." Stratify components by (size × scale). For each (size,scale)
  stratum, give the estimator (point-sampling when the stratum is a large fraction; localized slab/box
  probing when it is rare) and bound its cost by the min(λ, √(n/λ))-type tradeoff. Show the SUM over
  all strata and scales stays Õ(n^{1/3}). (Large components contribute little persistence per point and
  are cheap; the cost concentrates on small components at scale ≈ n^{1/3}.)
- **(b) The dense heavy-gadget stratum.** Detect/estimate the contribution of dense anomalous cells by
  scanning the Θ(n^{1/3}) coarse cells (this is the Lemma-32 floor instance). Integrate with (a).
- **(c) (1±ε) assembly + variance.** Bound each stratum's estimator variance (Horvitz–Thompson /
  median-of-means / importance weights) so the assembled estimate of Σλc is (1±ε)·OPT w.p. ≥ 2/3.
  Show per-scale/per-stratum errors sum to ≤ ε·OPT. NO step may estimate a single N_i/c_i to relative
  error (= cell sampling, U-B1).
- **(d) Counting-oracle implementation.** Spell out, in range-counting queries: uniform point sampling
  (O(log Δ)); the loneliness / small-cluster-size test at scale λ (a λ-box count + local refine); the
  slab/localized probes; and the coarse-cell scan. Confirm each primitive's query cost.

Use any method. If some stratum genuinely forces ω(n^{1/3}) (e.g. √n), prove it precisely — but note it
must evade U-P2/U-P3's vise and not contradict U-P1, so treat any √n claim with suspicion and test it
against the spread-vs-concentrate vise.

---

## 5. What we need back

1. **The full algorithm** (pseudocode, all strata + dense gadget + the four primitives of (d)).
2. **Query-count proof:** Õ(n^{1/3}) (or best provable o(√n)), with the per-stratum/per-scale cost
   accounting showing the n^{1/3} balance and where the worst case sits.
3. **(1±ε)-correctness proof:** variance bounds, error budget across strata/scales, success probability.
4. **Verdict + confidence %** (algorithm-complete-and-proven / complete-modulo-stated-lemma / specific
   obstruction / open) for o(√n) and for Õ(n^{1/3}).
5. **Numerics (strongly encouraged):** implement the estimator over an exact range-counting oracle
   (scipy exact EMST in the repo `sim/emst.py`), and show measured query count = Õ(n^{1/3}) while the
   estimate → (1±ε)·w(MST) across several n, on BOTH hard instances — the diagonal filament (all λ) and
   the dense Lemma-32 gadget. (Your sandbox may block Python; if so, give the analysis and say so.)

We will adversarially audit (looking for: a hidden per-scale relative-error N_i = cell sampling = √n; a
stratum with unbounded variance; the dense-gadget stratum ignored; an undercounted query bound; a
per-scale error exceeding its ε·OPT share; an Ω(n^{1/3})-floor violation; a primitive that is not
actually implementable in range counts). A complete, audit-surviving Õ(n^{1/3}) algorithm closes the
Driemel et al. gap from above — state it as a clean theorem with hypotheses.
