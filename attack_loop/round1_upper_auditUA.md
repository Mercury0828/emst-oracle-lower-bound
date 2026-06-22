# Round 1 (UPPER-bound line) — Independent Adversarial Audit (UA)

**Auditor:** independent fresh-context auditor (no stake in codex's answer).
**Date:** 2026-06-21.
**Sources checked directly:** arXiv:2504.15292v1 "Range Counting Oracles for Geometric Problems"
(Driemel, Monemizadeh, Oh, Staals, Woodruff), full PDF extracted via `pdftotext -layout`.
Section 4 (lines ~809–1027 of the text dump) and Section 5.3/5.4 (lines ~1240–1388) read verbatim.
Numerics run with `python` (variance + reduction checks reproduced below).

---

## Bottom line

| Claim | Verdict |
|---|---|
| 1. Paper proves Ω(√n) cell-sampling LB (even 1D); MST estimator invokes it; brief's "√n = BFS depth" is incomplete | **VALID** |
| 2. "If seeds+count were free, constant/polylog t suffices" | **VALID** |
| 3. Variance kill of the point-sampling workaround (Var[Z]=Θ(nM) ⇒ q=Ω(√n)) | **VALID** |
| 4. Decisive: is the open door real? | **(β) DOOR GENUINELY OPEN** — no reduction exists; cell-sampling-hardness provably does NOT transfer to MST weight |

codex's reply is **honest and substantially correct**. The one place the brief (not codex) was wrong is
diagnosing the √n as merely the BFS depth `t`; codex correctly relocates it to the cell-sampling
primitive. But codex's own pessimism in leaving the door "only 35% open" is, if anything, slightly
*under*-stated: I found a clean argument (below) that the cell-sampling lower bound *cannot* be lifted to
MST, so the gap is genuinely structural, not an artifact codex missed.

---

## Claim 1 — FACT-CHECK against the paper — **VALID**

**(a) Is there an Ω(√n) lower bound for cell sampling? Stated precisely:**

YES. Section 4 of the paper ("Sampling a non-empty cell uniformly at random") contains:

- **Algorithm 1 `CellSampling(r)`** (paper p.13): two-step sampler. If ≤√n non-empty cells, enumerate all
  (Lemma 16, O(√n log Δ) queries) and sample uniformly; else draw x=√(n) log n points, reweight by
  inverse cell-multiplicity w(p)=n/(x·n_p), and sample a point by weight.
- **Lemma 17:** `CellSampling(r)` selects a cell almost uniformly using Õ(√n) range-counting queries.
- **Corollary 18:** "We can estimate the number of non-empty cells within an O(1)-relative [error using]
  Õ(√n) counting queries." (Upper bound on *N_i = #non-empty cells*.)
- **Lemma 19 (the lower bound):** "any randomized algorithm that determines whether I is uniform with
  success probability ≥ 2/3 requires Ω(√n/c) range counting queries." Proof by Yao + a hitting argument
  (a query learns the witness segment only if a query endpoint lands in it; with √n/(16c) queries the
  witness is missed w.p. ≥ e^{−1/4} > 1/3).
- **Lemma 20:** "Any algorithm that can perform c-approximate uniform sampling for non-empty cells
  requires Ω(√n/c) range counting queries for any c ≥ 1." (Reduces sampling to the Lemma-19 distinction.)

**It explicitly holds in 1D.** Paper, immediately above Lemma 19 (verbatim): *"Our lower bound holds even
in a discrete one-dimensional space [Δ] with Δ = n."* The construction is a length-n interval, n unit
cells, n/(4c) segments; uniform instance has n/(4c) non-empty cells, each non-uniform instance has
≈2c√n non-empty cells (a constant-factor — 8c²+1 — gap), so even an O(1)-relative estimate of N_i is
Ω(√n). codex's citation set ("Algorithm 1 / Lemma 17 / Corollary 18 / Lemma 19") is **accurate**;
the only label nit is that the sampling LB is finalized in **Lemma 20** (Lemma 19 is the distinguishing
LB it rests on). Not material.

**(b) Does the MST upper-bound algorithm require/call it?** YES — twice, verbatim from §5.3 (paper p.20):
> "We pick r=O(1/ε²) random samples c₁…c_r from V(S_i) uniformly at random… **This can be done using
> O(√n log n) range counting queries as in Algorithm 1. This sampling algorithm also gives an estimator
> n̂ of the number of non-empty cells of G within O(1) relative error by Corollary 18.**"

And the per-scale estimator is `ĉ_i = (n̂/r)·Σ_j ξ_j` (Lemma 28), so **both** load-bearing inputs — the
near-uniform seeds (Lemma 17) **and** the multiplicative scale factor n̂ (Corollary 18) — are cell-sampling
outputs. Each is individually Ω(√n)-hard by Lemma 19/20.

**(c) Is the brief's "the √n is the BFS depth t" claim wrong/incomplete?** **INCOMPLETE / misdiagnosed.**
The brief (§2.4) attributes the √n to the per-seed BFS truncation depth t=√n. That is *a* √n term but not
the binding one: the seed-drawing and n̂-estimation steps are *also* Ω(√n) and are not removable by tuning
t. codex is right to relocate the bottleneck to cell sampling. (See Claim 2: even with t=O(polylog), the
algorithm still pays Õ(√n) for seeds+count.) So the brief's stated "slack" (lower t per scale) does **not**
by itself yield o(√n); codex's correction stands.

---

## Claim 2 — "free seeds+count ⇒ constant/polylog t suffices" — **VALID**

The argument: truncating components larger than t miscounts ≤ N_i/t of them; planar packing gives
OPT ≥ Ω(λ·N_i) (λ=(1+ε)^i); so the *weighted* bias is λ·(N_i/t) ≤ O(OPT/t), and any t=Ω(1/ε) (polylog
overall) makes it ≤ ε·OPT.

This is exactly the paper's own Lemma 28 analysis, which I verified line-by-line:
- "the number of large components is O(n/t)" → with seeds uniform, E[ĉ_i] ≥ c_i − n̂/t.
- planar 4-coloring ⇒ independent set of size N_i/4 ⇒ "OPT ≥ (N_i/4)·(1+ε)^i", i.e. N_i ≤ 4·OPT/(1+ε)^i.
- ⇒ additive bias ≤ O(1)·OPT/(1+ε)^i, which after the Σ_i(1+ε)^i weighting is O(ε·OPT).

The paper sets t=√n only to *balance against the seed cost*, which is itself √n — i.e. t=√n is chosen
because cell sampling already costs √n, so there is no point making t smaller. If seeds+count were free,
nothing in Lemma 28 forces t above polylog. **codex's localization of the entire √n to cell sampling is
correct and matches the paper's algebra.**

---

## Claim 3 — Variance kill of the point-sampling workaround — **VALID**

Hard instance (scale λ=√n): M=√n singleton cells (a_v=1, φ=1, each its own component) + the remaining
n−M points forming one connected bulk. Then c_i=M+1=Θ(M), OPT=Θ(λM)=Θ(n), allowed additive error in
c_i is ε·OPT/λ=Θ(M). Estimator Z=n·β(v)/a_v.

**Verified numerically** (exact first/second moments of single-sample Z; values stable across n):

```
n=1e4 : mean_Z=101    Var=9.90e5  Var/(nM)=0.99  allowed≈30    q=1.10e3  q/√n=11.0
n=1e6 : mean_Z=1001   Var=9.99e8  Var/(nM)=1.00  allowed≈300   q=1.11e4  q/√n=11.1
n=1e8 : mean_Z=10001  Var=1.00e12 Var/(nM)=1.00  allowed≈3000  q=1.11e5  q/√n=11.1
n=1e10: mean_Z=100001 Var=1.00e15 Var/(nM)=1.00  allowed≈30000 q=1.11e6  q/√n=11.1
```

- Unbiased: E[Z]=c_i=M+1. ✓
- **Var[Z]=Θ(nM)** (ratio → 1.000). ✓ Dominated by the M singleton cells: each is hit w.p. 1/n and
  yields Z=n, contributing M·(1/n)·n² = Mn to E[Z²]; the bulk contributes O(1).
- Samples needed q = Var/(allowed)² = Θ(nM)/Θ(M²) = Θ(n/M) = **Θ(√n)** (q/√n pinned at 1/ε²≈11 for
  ε=0.3). ✓

So the "uniform point sample + inverse-multiplicity reweight" route requires Ω(√n) samples on this
instance. **codex's variance computation is correct and the workaround is genuinely killed.** (The reason
is structural: singletons are rare in *point* mass but dominate the *component count*; inverse-weighting
to debias inflates variance to Θ(nM). This is the standard CRT reason cell *sampling*, not point
sampling, is the right primitive.)

---

## Claim 4 — THE DECISIVE ASSESSMENT — **(β) DOOR GENUINELY OPEN**

The pivotal question is whether cell-sampling-hardness *transfers* to MST-weight estimation — i.e.
whether there is a reduction (any (1±ε)-MST estimator ⇒ solve cell sampling), which would flip the
problem to a provable Ω(√n) and **kill** the upper-bound pivot. **I find no such reduction, and I have a
clean argument that the obvious one fails.**

**Why the reduction fails (decisive, verified numerically):** The cell-sampling lower bound (Lemma 19) is
**1D**, and its whole power is that uniform vs non-uniform instances differ in *cell-occupancy structure*
(50 vs 450 non-empty cells in my run). But **1D MST weight = x_max − x_min** (the consecutive-gap sum
telescopes), which is *completely insensitive* to interior occupancy. Direct check on the exact Lemma-19
construction:

```
1D MST  uniform    = 39200.0
1D MST  non-uniform= 39200.0      ratio = 1.000
#non-empty cells:  uniform=50,  non-uniform=450   (a 9× cell-count gap MST cannot see)
```

So a perfect (1±ε)-MST estimator returns the *same* value on both instances and **cannot** decide
uniform vs non-uniform. **The cell-sampling lower bound does NOT reduce to MST-weight estimation.**
Option (α) is therefore **unsupported**: the √n is a property of the *primitive the paper chose*, not of
the MST functional. (Consistent with the paper itself: it proves only Ω(n^{1/3}) for MST in Lemma 32 —
a *different, weaker* hitting argument over 16n^{1/3} coarse cells with strip/uniform gadgets — and makes
no attempt to lift the √n cell-sampling LB to MST. If such a lift existed the authors would surely have
stated Ω(√n) for MST. They do not.)

This is the crucial gap in codex's framing that *favours* the upper-bound pivot: codex correctly notes
"a different rectangle-native estimator might exploit geometry" but treats it as a vague hope. The audit
upgrades this: there is a **provable obstruction to the reduction**, so the door is not merely "not yet
closed" — the natural key to closing it (the cell-sampling LB) **provably does not fit the MST lock.**

**What is and isn't blocked, precisely:**
- Blocked: the *CRT route* (Lemma 25 identity → per-scale component counts via CRT estimator). It needs
  near-uniform seeds (Lemma 17) and an O(1)-relative N_i estimate (Corollary 18); both are Ω(√n) by
  Lemma 19/20. Any black-box CRT instantiation inherits √n. codex is right here.
- **Open:** a non-CRT estimator of OPT = (n−Δ) + Σ_i (1+ε)^i c_i that never asks for a near-uniform cell
  sample or an O(1)-relative N_i. Nothing in §4 lower-bounds *MST weight*; it lower-bounds *cell
  sampling* and *N_i estimation*, and 4(i) shows those are strictly harder than the MST functional on the
  hardest known cell-sampling instance.

**Most promising rectangle-native direction (concrete):**

1. **Exploit exact occupancy, not uniform samples.** A range-count oracle returns the *exact* integer
   |P∩R|. For any rectangle R and any sub-grid, a logarithmic-depth dyadic sweep yields the exact number
   of *non-empty sub-cells* inside R (recurse only into non-empty children; the count is exact, no
   sampling, no relative-error primitive). This sidesteps Corollary 18's *relative-error* framing — the
   Ω(√n) in Lemma 19 is about *near-uniform sampling / distinguishing*, and is paid only if you insist on
   a uniform cell *sample*. A deterministic occupancy *sum* over a region can be cheaper where the region
   is sparse, and the MST sum only needs Σ_i λ_i c_i, an aggregate.
2. **Estimate c_i via Euler-characteristic / inclusion-exclusion on counts, not BFS.** For a planar
   contracted grid graph, #components = #cells − #edges + #independent-cycles. Edges and cell-counts at
   scale i are local occupancy predicates (Lemma 24-style O(ε^{-2}) tests) readable from counts; the
   cycle-rank correction is where geometry (planarity, bounded genus of the grid-adjacency graph) may let
   a few coarse rectangle counts pin Σ_i λ_i c_i without ever sampling a cell. This is the "estimate
   Σ_i λ·c_i directly from coarse rectangle counts" idea, made concrete: aggregate the per-scale
   component count through the planar Euler relation rather than through a CRT uniform-seed estimator.
3. **Hierarchical pay-where-sparse.** Because counts are exact, scales with few non-empty cells (the
   coarse, few-component scales that dominate the (1+ε)^i weight) can be enumerated *exactly* and cheaply
   (Lemma 16 costs Õ(N_i), and N_i is small there); only fine scales have many cells, but there λ_i is
   small so the *allowed* additive error is large. The √n in the paper comes from using one *uniform*
   t=√n / one uniform cell-sampler across all scales; a scale-partitioned exact/aggregate scheme is not
   obviously Ω(√n).

None of these is a proven o(√n) algorithm — they are the live surface. But they do **not** route through
the Lemma-19 hard primitive, and 4(i) shows that hard primitive cannot be smuggled back in via the MST
value. **The upper-bound pivot is alive.**

**Honest caveats (what's missing to make it (β)-with-an-algorithm rather than (β)-open):**
- The Euler/cycle-rank route still has to estimate the *cycle rank* of the contracted graph to additive
  ε·OPT/λ_i; it is not yet shown this is cheaper than component-counting in the worst case.
- The n^{1/3} floor (Lemma 32) is real and unaffected; any rectangle-native scheme must still respect it,
  and the strip-vs-uniform gadget instance is a genuinely hard 2D instance for MST weight (unlike the 1D
  cell-sampling instance, the two gadgets there *do* differ in MST weight by 2×). So the achievable target
  is the band [n^{1/3}, √n], and the gadget instance already forces ≥ n^{1/3}.

**Classification: (β) DOOR GENUINELY OPEN.** A reduction from cell sampling to MST does **not** exist (the
hardest cell-sampling instance is MST-invariant in 1D; the paper never lifts the √n to MST and proves only
n^{1/3}). The CRT route is correctly diagnosed as √n-blocked by codex, but MST-weight estimation is not
itself shown to be √n-hard, and a counting-native estimator of Σ_i λ_i c_i via exact occupancy /
planar Euler relation is a concrete, un-blocked avenue.

---

## Confidence assessment of codex's numbers

codex: 35% that a non-CRT o(√n) algorithm exists; 15% for Õ(n^{1/3}). Given the *positive* finding in
4(i) (the cell-sampling LB provably cannot be lifted to MST), I'd nudge the o(√n) figure slightly **up**
(≈40–45%): the main thing that would have closed the door — a reduction — is now shown not to exist via
the natural instance, so the obstruction is "no one has built the estimator yet," not "it is impossible."
The Õ(n^{1/3}) figure (15%) is reasonable to slightly optimistic; the Euler-relation route would have to
be both correct and tight to the floor, which is a tall order. Neither change is load-bearing for the
verdicts above.

---

## One-line verdicts

- Claim 1: **VALID** — Lemma 19/20 give Ω(√n/c) cell-sampling LB, explicitly 1D; §5.3 calls Algorithm 1 +
  Corollary 18 for seeds *and* the n̂ scale factor. Brief's "√n = BFS depth t" is **incomplete** (the
  removable-by-tuning-t story is wrong; seeds+count are the binding √n).
- Claim 2: **VALID** — matches Lemma 28; with free seeds+count, t=O(polylog) keeps weighted bias ≤ ε·OPT.
- Claim 3: **VALID** — Var[Z]=Θ(nM) confirmed numerically (ratio→1.0); q=Θ(√n); point-sampling route dead.
- Claim 4: **(β) DOOR GENUINELY OPEN** — no reduction (1D cell-sampling instance has identical MST weight,
  ratio 1.000, despite 9× cell-count gap); concrete rectangle-native direction = estimate Σ_i λ_i c_i from
  exact occupancy via the planar Euler relation, paying-where-sparse across scales, never invoking a
  near-uniform cell sample.
