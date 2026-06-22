# Round-2 Audit C (independent, adversarial) — GPT-5.5-Pro CLAIMED Õ(n^{1/3}) closure

Auditor: independent fresh-context adversary. Target: `docs/webpro_round2_response.md`.
Method: full re-read of every proof line; re-derivation of each inequality chain; EXACT-EMST
numerics (`sim/emst.py`) on adversarial instances; external check of the cited Czumaj et al.
guarantee and the source paper's access model.

Numeric artifacts produced:
`attack_loop/auditC_round2.py`, `auditC_bridge_deep.py`, `auditC_regularize.py`, `auditC_spanner.py`
(plus the orchestrator's `webpro_verify_round2.py`, re-run: Lemmas 1,2 + snapping all PASS).

---

## TL;DR VERDICT

**The reduction is SOUND and numerically airtight; the closure has ONE residual GAP, not fatal.**

Everything Pro builds *around* the support-MST estimator is correct and verified at the
checkable level:
- Lemma 1 (packing), Lemma 2 (interleaving), snapping-preserves-tail: **VALID**.
- W_Q = O(W): **VALID** (numerically W_Q/W ∈ [0.37, 0.75], always ≤ W).
- The assembly identity B_L(P) ≈ B_L(Q) = W_Q − A_L(Q): **VALID** to <0.001 relative error,
  including on the single-Θ(W)-edge bridge that killed round 1.
- Error budget η,α,ρ=Θ(ε) composes ADDITIVELY to ≤ εW: **VALID**.
- Query terms ADD (n/K_0 + √K + n/K), do not multiply, = Õ(n^{1/3}) at K=Θ(n^{2/3}): **VALID**.

The single load-bearing claim that is **NOT** established at the rigor level of the rest is
**Lemma 3**: that Czumaj et al.'s Õ(√K) Euclidean-MST estimator can be run on the *implicit*
support Q — whose native primitive (cone approximate-NN / Yao graph) is **replaced** by a
"component-restricted, locally-enumerable (1+ρ)-WSPD spanner" — while keeping the total at
Õ(√K + n/K). This is exactly the step Pro self-rated 0.84 and asked to be line-audited.
I confirm it is the only soft spot, and I classify it **NEEDS-REPAIR / GAP** (not fatal).

**Confidence the overall closure is correct: ~0.62.** The reduction is unimpeachable; the
remaining risk is entirely concentrated in whether the cone-NN→WSPD substitution inside
Czumaj's active-block recursion truly costs Õ(√K) range-queries and not more — a claim that
is plausible but rests on the internal details of a 20-year-old algorithm and cannot be
discharged by the geometry-level numerics available here.

---

## Target-by-target

### 1. Lemma 1 (packing) K_h ≤ 8W/h+4 — **VALID (MINOR caveat, not load-bearing)**

The structure is correct:
- 4-coloring by index parities (⌊x/h⌋ mod 2, ⌊y/h⌋ mod 2): two chosen points of the same
  color differ by an even number of cells ≥ 2 in some axis, hence are ≥ h apart in L∞, hence
  ≥ h in L2. **Correct.** (Pairwise-≥h within a class confirmed.)
- "same-color s points pairwise ≥ h ⇒ MST ≥ h(s−1)": correct (every MST edge ≥ min pairwise
  distance ≥ h, and there are s−1 edges).
- "w(MST(S)) ≤ 2W for S⊆P": take the minimal subtree τ of MST(P) spanning S (weight ≤ W);
  an Euler tour doubles it (≤ 2W) and visits all of S; shortcutting to the S-order is a walk
  whose Euclidean length only *decreases* by triangle inequality, and that walk contains a
  spanning path of S, so w(MST(S)) ≤ that walk ≤ 2·w(τ) ≤ 2W. **The chain
  "w(MST(S)) ≤ 2·w(minimal subtree) ≤ 2W" is correct.**
- Therefore h(s−1) ≤ 2W ⇒ s ≤ 2W/h+1; four colors ⇒ K_h ≤ 4(2W/h+1) = 8W/h+4. **Correct.**

Numerics (`webpro_verify_round2.py`, `auditC_regularize.py`): holds on every instance with
large slack; the dyadic halving K_{h/2} ≤ 4K_h is confirmed (worst observed 3.95, exactly the
area-quadrupling constant), so the "first crossing lands in [cK_0, C_ε K_0]" argument is sound,
and the operative grid lands in [1.0, 2.6]·K_0 in practice. (MINOR: the K̂ estimator's
n/K_0 sampling cost is genuinely Õ(n^{1/3}); fine.)

### 2. Lemma 2 (interleaving) + snapping bound — **VALID**

- c_P(t+δ) ≤ c_Q(t) ≤ c_P(t−δ), δ=√2h: both directions correct. A t-edge of P maps to a
  ≤(t+δ)-edge of centers (each endpoint moves ≤ r=δ/2), giving c_Q(t+δ)≤c_P(t) hence the
  left inequality after reindexing; the right one because two centers ≤ t apart have
  representatives ≤ t+δ apart and co-cell points are ≤ δ apart. **Correct.**
- B_{L+δ}(P) ≤ B_L(Q) ≤ B_{L−δ}(P) follows by integrating the survival functions; with
  c_P(t)−1 ≤ W/t (Kruskal: #edges>t ≤ W/t), |B_L(Q)−B_L(P)| ≤ ∫_{L−δ}^{L+δ} W/t dt
  ≤ (2δ/(L−δ))W = O(αεW) since h ≤ αεL ⇒ δ=√2h ≤ √2αεL ≪ L. **Inequality chain is correct.**

Numerics: |ΔB|/W shrinks linearly in h, reaching 4e-4 at αε=0.1; the serpent produces NO
false tail weight; the single-bridge tail survives within 6e-4 relative. **VALID.**

### 3. W_Q = O(W) — **VALID**

W_Q ≤ W + δ(K_h−1); δK_h ≤ √2h(8W/h+4) = O(W + h); at the operative level h=O(W/K_0) and
K_h=Θ(K_0) ⇒ W_Q = O(W). Algebra correct. Numerically W_Q/W ∈ [0.37, 0.75] across random,
serpent, clustered (power-law occupancy), and single-bridge instances; in EVERY case W_Q ≤ W
(snapping shortens the contracted tree), so the constant is ≤ 1 in practice, well inside O(W).
**VALID.**

### 4. Overall assembly + error budget — **VALID (conditional on Lemma 3)**

- **Identity.** B̂_L = Ŵ_Q − Â_Q targets B_L(Q) = W_Q − A_L(Q); the final W is reconstructed
  as A_L(P) + B_L(P) with B_L(P) ≈ B_L(Q) (snap O(εW)). I verified the *exact* identity
  W = A_L(P) + B_L(P) and W_Q = A_L(Q) + B_L(Q) numerically, and that
  Ŵ = A_L(P) + (W_Q − A_L(Q)) reconstructs W to <1e-4 relative on random/serpent/bridge.
  No double-count and no missed Θ(W) band: A and B partition the same MST-edge multiset at L.
- **Budget composition.** Three error sources — snapping O(αεW), estimator O(ηW) (uses
  W_Q=O(W)), spanner distortion O(ρW_Q)=O(ρW) — are ADDITIVE; ρW_Q/W ≈ 0.5ρ numerically, so
  the two (1+·) layers (P→Q snap, Q→H_Q spanner) compose without eroding the ε budget. Set
  η,α,ρ=Θ(ε) ⇒ total ≤ εW. **Correct.**
- **Query additivity.** Stages: K̂/support-sampling Õ(n/K_0); Lemma-3 spatial work Õ(√K);
  shared seed pool Õ(n/K); clipped death-time Õ(n/K). At K=Θ(n^{2/3}): √K=n/K=n/K_0=n^{1/3}.
  They ADD (sequential stages), each individually Õ(n^{1/3}); sum = Õ_ε(n^{1/3}). The §7
  geometric-search wrapper adds an O(log n) factor only. **Correct — no hidden product.**
- The genuinely-multiplicative danger (√K independent support samples × n/K each = n^{2/3})
  is real and is *defused* by the one-shared-seed-pool device (§4 "Reusing the vertex seeds").
  This device is sound IN PRINCIPLE: at any fixed threshold the pool is i.i.d. uniform on Q,
  so per-threshold concentration is unaffected; a union bound over T=O(log Δ) thresholds with
  O(log T) pool size + medians gives simultaneous correctness. Cross-threshold *independence*
  is indeed unnecessary. **This accounting is correct.** (It is the linchpin of the exponent.)

### 5. Adversarial / counterexample hunt — **NO counterexample found; reduction survives**

I attacked along every suggested axis with EXACT EMST:
- **Single rare Θ(W) bridge** (the round-1 killer): the heavy edge SURVIVES snapping
  (max_Q ≈ max_P, B_Q≈B_P within 2e-4), and W_Q≈0.64W. So the *target* W_Q carries the heavy
  edge — the reduction does not destroy or fabricate the tail. **No counterexample here.**
  BUT: in the snapped support, **one edge carries ~74% of W_Q** among K_h≈Θ(n^{2/3}) edges.
  This is exactly the concentration that defeats uniform death-time sampling. Pro's escape is
  that Czumaj's *spatial* (active-block) estimator isolates the heavy edge by the empty gap
  geometry in Õ(√K) blocks, NOT by sampling. That escape is plausible and is precisely the
  unverifiable Lemma-3 claim (see target 6 / GAP below) — I could neither break nor confirm it
  at the geometry level.
- **k-bridge** (tail spread over k medium edges): regularizes cleanly, top-1 fraction drops to
  0.02 at k=32; no problem.
- **Serpent / L-connected filament**: no false long edges outside the δ-window; B_L(Q)≈B_L(P).
- **Power-law / geometrically-unequal occupancy**: rejection sampler is uniform over occupied
  cells (acceptance ∝ 1/m(z)·m(z)/n = 1/n, size-bias cancels — verified analytically in §2 and
  consistent with the round-1 size-bias-corrected estimator); regularization band stays Θ(K_0).
- **K cannot be regularized to Θ(n^{2/3})**: I could not construct such an instance. Dyadic
  halving with K_{h/2}≤4K_h forces a crossing inside [cK_0, 4K_0]; numerically [1.0,2.6]K_0.
- **Bulk/tail split well-defined for w(MST)∈[Ω(n),O(n^{1.5})]**: L=W/K_0=W/n^{2/3} is positive
  and the split A_L+B_L=W partitions the MST-edge multiset for any W; verified across W spanning
  ~1.9e3 (bridge, near Ω(n)) to ~1.7e5 (random, near n^{1.5}). Well-defined.

**Conclusion of the hunt: the REDUCTION has no counterexample.** The only place a √n could
still hide is *inside* Lemma 3's query accounting — which is target 6.

### 6. Headline cross-check + the residual GAP — **NEEDS-REPAIR (GAP, fixable, not fatal)**

External check of the cited primitive: Czumaj et al. (SICOMP 2005) give a (1±ε) EMST-weight
estimator in **Õ(√n)** queries, but it **assumes access to (i) orthogonal range queries AND
(ii) cone approximate-nearest-neighbor (Yao-graph) queries**, and the √n is in the size of the
point set processed. The source paper 2504.15292 (SoCG'25) provides the Õ(√n) *range-counting*
upper bound and the Ω(n^{1/3}) lower bound that define the gap.

Pro's Lemma 3 must therefore (a) run Czumaj on the K-point support Q that is only IMPLICIT
(accessible solely via range-counts to P), and (b) replace the native cone-NN primitive by a
component-restricted, locally-enumerable (1+ρ)-WSPD spanner H_Q, while keeping total cost
Õ(√K + n/K). The geometric correctness of (b) — w(MST(Q)) ≤ w(MST(H_Q)) ≤ (1+ρ)w(MST(Q)),
distortion error ρW_Q=O(εW) — I verified is clean and additive (target 4). What I CANNOT
discharge, and what Pro himself flags at 0.84, is the **query accounting of the substitution
inside Czumaj's active-block recursion**:

> GAP: "each adjacency op Õ_ρ(1)" and "stages 1,3 use Õ(√K) range-emptiness queries" rest on
> the claims that (i) above the active-block level all subset/emptiness info is available
> OFFLINE from the O(√K) active-block list, and (ii) below it each emptiness/representative
> query touches exactly ONE known block ⇒ one range-count to P. These are asserted, not proved,
> and they are the entire reason the exponent stays at √K rather than leaking to K or √K·(n/K).
> The WSPD-max-degree polylog and "source Lemmas 21–24" are invoked but not reproduced. This is
> a genuine, non-trivial verification obligation about Czumaj's internal decomposition, not mere
> bookkeeping.

Because the bridge numerics show w(MST(Q)) can be 74%-dominated by a single edge, the estimator
MUST recover that edge via spatial subdivision in Õ(√K) and not fall back to sampling (which
would need Ω(K) to see one heavy value among K). I found no reason it fails — Czumaj's
active-block recursion does isolate large empty separators — but the formal Õ(√K) bound for the
*range-query* re-implementation of that recursion is the unproved hinge.

**Headline consistency:** IF Lemma 3 holds, the result is Õ_ε(n^{1/3}), matching Ω(n^{1/3}) up
to polylog — a genuine closure and a strict improvement over the published Õ(√n), with NO
contradiction to any published lower bound (the Ω(n^{1/3}) is met, not beaten; Czumaj's Ω(√n)
cell-sampling LB is correctly side-stepped because the grid is fixed so the support is
Θ(n^{2/3}) and the same sampled cells are reused — the arbitrary-grid primitive is never
invoked). So no internal contradiction; the only open point is the GAP above.

---

## Classification summary

| # | Target | Verdict | Severity |
|---|--------|---------|----------|
| 1 | Lemma 1 packing proof | VALID | MINOR |
| 2 | Lemma 2 interleaving + snap bound | VALID | — |
| 3 | W_Q = O(W) | VALID | — |
| 4 | Assembly + error budget (additive, composes) | VALID | — (conditional on 6) |
| 5 | Adversarial / counterexample hunt | VALID (no counterexample) | — |
| 6 | Lemma 3 cone-NN→WSPD query accounting | NEEDS-REPAIR | **GAP** (fixable, not fatal) |

**OVERALL VERDICT: the assembly + Lemmas 1/2 + snapping + error budget are SOUND and the
Õ(n^{1/3}) closure holds AT THE CHECKABLE (reduction) LEVEL, but the claim has a single
fixable GAP — the Õ(√K) range-query re-implementation of Czumaj's active-block estimator with
the cone-NN primitive replaced by a locally-enumerable (1+ρ)-WSPD spanner (Lemma 3) is asserted,
not proved, and is the sole place an exponent leak could hide.** Name of the gap:
**"component-restricted WSPD substitution inside Czumaj's active-block recursion costs Õ(√K)
range queries" — unproven.**

**Confidence the complete closure is correct: ≈0.62.** (Reduction ≈0.97; Lemma-3 substitution
≈0.65, matching Pro's own 0.84 discounted for the unreproduced internal accounting.)

**Recommendation:** demand a self-contained, line-by-line proof of Lemma 3's query budget —
specifically the two assertions that above the active-block level all info is offline from the
O(√K) block list, and below it each adjacency op is a single range-count — reproducing the
relevant content of source Lemmas 21–24 rather than citing them. The numerics in this audit
establish that nothing in the *reduction* can break; the burden is now entirely on that one
algorithmic lemma.
