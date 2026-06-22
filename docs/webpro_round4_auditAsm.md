# Round-4 Audit (assembly + lemmas + NEW-counterexample hunt) — GPT-5.5-Pro spatial-cell estimator

> Independent, fresh-context, adversarial auditor. Target: `docs/webpro_round4_response.md` (the
> spatial-cell repair that defeated the round-3 satellite counterexample). Context: round 2 passed 3
> audits then round 3 broke it with a concrete counterexample; round 4 is the new repair. My job:
> verify §2/§7/§8/§9 + the §11 insertion, and try hard to find a NEW counterexample that breaks the
> round-4 spatial estimator (cost or recovery), the way satellites broke round 2.
>
> Method: EXACT EMSTs via `sim/emst.py` + Delaunay/union-find; reimplemented the estimator's accounting
> faithfully; scaled K over 64–256× to separate genuine-K-growth from η/T constants. Scripts:
> `attack_loop/audit_r4_t1f.py, t2.py, t3.py, t4_cost.py, t4b_scaling.py, t5_hunt.py, t5b_recovery.py,
> t5c_containment.py, t5d_NU.py, t5e_eq3.py, t5f_truecost.py, t5g_cj.py, t5h_variance.py`.
> Pro's own decisive test `attack_loop/webpro_verify_round4.py` re-run: recovery PASSES
> (spatial_hat/W_Q = 1.07/0.98/1.08 for s=32/64/96).

---

## TL;DR VERDICT

**Assembly SOUND; NO new counterexample found after a genuine hunt. The algorithm's true complexity IS
Õ(√K), so the round-3 obstruction is genuinely defeated. There is ONE write-up GAP (not fatal, not a
complexity leak): the cost bookkeeping in eqs (2)/(3)/(8) bounds the leader-estimator variance via the
OCCUPIED-CELL count `N_j`, claiming `N_j ≤ C(1+W_Q/(σr_j))` with K-independent C. That inequality is
FALSE at the small-scale (`a=h`) floor, where numerically `N_j ≈ Θ(√K)·W_Q/(σr_j)`. The estimator is
saved because its variance is actually `M_j·c_j` (component count `c_j`, exactly `E[Z]=c, Var(Z)≤Mc`),
and `c_j ≤ C(1+W_Q/(σr_j))` IS true with K-independent C (it is the `(c−1) ≤ W_Q/t` identity). With
`c_j` the cost is flat/decreasing in K. Fix = state the variance with `c_j`, not `N_j`, throughout. This
is a MINOR/GAP-level presentation fix; the exponent Õ(√K) is correct.**

Per-item: §2 **VALID**; §7 **VALID**; §8/§9 **VALID**; §11 insertion **VALID** (with the §2-§8 GAP above
folded in); counterexample hunt **NONE FOUND**. Overall: assembly SOUND + no new counterexample ⇒
**closure likely holds** (modulo the published-engine-free Lemma-3 still being an AI-level, not
human-expert, verification). Confidence ~0.80 that the Õ_ε(n^{1/3}) closure is correct.

---

## 1. Filtration interleaving (§2): **VALID**

Claim (1): `c(r_{j+1}) ≤ c̃_j ≤ c(r_j)` for the a-cell graph Γ_r (a=Θ(σr)), with
`r_j + 2√2 a_j ≤ r_{j+1}`. Tested both directions + spacing.

- **a>h regime (forced via large-spread integer supports, `audit_r4_t1f.py`):** 28 scales,
  **0 violations**. Both `c(r+2√2 a) ≤ c̃` and `c̃ ≤ c(r)` hold at every scale (e.g.
  r=2384: c(r+2√2a)=1475 ≤ c̃=1488 ≤ c(r)=1507). The cell-graph adjacency must use the MIN
  Euclidean cell distance (not center distance) for a>h — with that, the lemma is exact-direction-safe.
- **a=h regime (`audit_r4_t1d.py`):** when the support has ≤1 point per h-cell (which holds **by
  construction**, since Q is the cell-center support), c̃(r) = c(r) **EXACTLY** at every scale, with
  point≠center or point==center. (Naively running c(t) on a *multi-point* set with >1 pt/h-cell gives
  spurious `c̃ > c(r)`; this is a definitional mismatch, not a defect — Pro's Q is single-occupancy.)
- **Spacing `r_j+2√2 a_j ≤ r_{j+1}=(1+σ)r_j`** requires `2√2 a ≤ σr`. Pro's design `a ≤ σr/64` gives
  `2√2·σr/64 ≈ σr/22.6 ≪ σr` ✓. (My harness's `sp_ok=False` flags were an artifact of flooring a=h at
  small scales; in Pro's a∈[σr/128,σr/64] band spacing always holds.)

## 2. Riemann-sum reconstruction (§7): **VALID**

Claim (11): Riemann gap `= Σ_j d_j(c(r_j)−c(r_{j+1})) ≤ σW_Q`, because each MST edge ℓ∈(r_j,r_{j+1}]
contributes `d_j=σr_j ≤ σℓ`. Verified on uniform / satellite-32,48 / hierarchical supports
(`audit_r4_t2.py`):
- Gap formula `Σ d_j(c_j−c_{j+1})` equals the upper−lower Riemann difference **exactly** (machine
  precision), and is **always ≤ σW_Q** (e.g. uniform 337≤581; sat32 14324≤23808; sat48 50626≤81216;
  hierarchical 1440≤1572 — the hierarchical case nearly saturates but stays below).
- Reconstruction `Ŵ=(K−1)h+Σ d_j(c_j−1)` tracks W_Q to ratio 1.07–1.15 at σ=0.25 (the O(σ) upper-Riemann
  bias); shrinks to (1±η) when σ=Θ(η) is taken small. The `∫_0^h(c−1)=(K−1)h` baseline is exact (distinct
  centers ≥h apart).

## 3. W-search (§8) and K-estimation (§9): **VALID**

`audit_r4_t3.py`:
- **W-search arithmetic:** `G≥4W_Q ⇒ Ŵ_G ≤ G/4+G/20 = 0.30G < G/3` (continue); `G∈[W_Q,2W_Q) ⇒
  Ŵ_G ≥ W_Q−G/20 ≥ 0.45G > G/3` (stop). First stop ⇒ `W_Q ≤ G_0 < 4W_Q`. All boundaries hold; the gap
  region [2W_Q,4W_Q) is decision-safe. Sound.
- **K-estimation:** `X(p)=n/m(p)` has `E[X]=K` exactly and `E[X²]=n·Σ_C 1/m_C ≤ nK` exactly (each
  1/m_C≤1). ⇒ Var/E[X]² ≤ n/K ⇒ relative-K estimate in Õ(n/K) samples. Verified analytically + Monte
  Carlo. Sound.

## 4. §11 insertion into the round-2 reduction: **VALID** (carries the §2-§8 GAP)

The round-2 reduction around the support-MST estimator (Lemma 1 packing, Lemma 2 snapping/interleaving,
W_Q=O(W), the `B_L(Q)=W_Q−A_L(Q)` assembly, additive error budget, query terms ADD not multiply) was
independently audited SOUND in round 2 (`webpro_round2_auditC.md`) and is **unchanged**. Round 4 only
swaps Lemma 3's internal estimator. The new spatial-cell estimator exposes the **same interface** the
reduction consumes — output `(1±η)·W_Q`, cost `Õ(√K+n/K)` — so the insertion composes. Crucially, the new
estimator uses **independent candidate-cell trials per scale** (no shared seed pool), which directly
removes the round-3 cross-threshold covariance defect (the actual cause of the round-2 failure). At
K=Θ_ε(n^{2/3}): √K=n/K=Θ(n^{1/3}) ⇒ Õ_ε(n^{1/3}). No interaction is broken by the replacement. The only
caveat is the cost-bookkeeping GAP in §5 below, which is internal to the estimator and does not change
the exponent.

## 5. 🔴 NEW-COUNTEREXAMPLE HUNT: **NO counterexample found** (one write-up GAP exposed)

I probed every angle the brief named, plus the structural pressure points of the √K argument.

**(a) Packing `W_Q=Ω(bδ)` (the load-bearing inequality).** `audit_r4_t5_hunt.py`. Tried to drive
W_Q/(bδ)→0: thin lines (many active blocks, cheap MST), grids, Cantor/fractal dust, multiscale
recursive satellites. The packing ratio **never degrades**: thin-line ≈1.00 (tightest, K-independent),
grid 3.5→8.0, fractal 3.5→5.75, multiscale-sat 15→32. The §10 dichotomy (support-rare OR
spatially-hidden, never both with constant MST fraction) **held in every instance**.

**(b) Active-cover blocks / M_j.** `audit_r4_t5c_containment.py`. Containment (every fine a_j-cell nests
in an active δ-block) holds everywhere; `N_j ≤ M_j = b(δ/a_j)²` holds (ratio ≤0.92<1). b is forced into
[√K,4√K) by the first-crossing rule. No M_j blow-up.

**(c) Interleaving divergence.** Covered in §1 — c̃ tracks c(r) tightly, no bad divergence.

**(d) Riemann gap > σW_Q.** Covered in §2 — never exceeded.

**Recovery on the hardest instances (`audit_r4_t5b_recovery.py`):** the FULL leader estimator recovers
W_Q within 1.0–1.17 on (i) a single hidden bridge whose rare component is **literally 1 cell** at the
bridge scale; (ii) graded satellites (thin tail across many scales); (iii) multiscale satellites (a rare
tail at EVERY dyadic scale). No recovery break. The leader-moment identity `E[Z]=c, Var(Z)≤Mc` is exact
on adversarial component structures (singletons, giant, power-law, core+satellites) — confirmed in closed
form (`audit_r4_t5h_variance.py`); the wandering E[Z] in Pro's own `webpro_verify_round4.py` test (I) is a
pure Monte-Carlo small-sample artifact (one leader cell among M=50000), not a flaw — median amplification
handles it.

**Cost accounting — the round-2 failure mode (a cost/variance blowup behind correct recovery).**
`audit_r4_t4b_scaling.py`, `t5f_truecost.py`, `t5e_eq3.py`, `t5g_cj.py`. This is where I pushed hardest.
- Holding σ,η,T fixed and scaling K over 64×, `total_trials/(√K·T²)` is **FLAT** for the satellite
  family (11k–18k, ratio max/min=1.65, no monotone growth) and the geometric `Σδ/r_j` ratio is dead-flat
  at 1.25. ⇒ the budget genuinely scales as √K·polylog. No round-2-style hidden K-blowup.
- **The GAP I found:** `max_j N_j/(1+W_Q/(σr_j)) ≈ Θ(√K)` (grid 0.32·√K, uniform 0.37·√K, growing with
  K), always achieved in the **a=h floor regime** where all K cells are still singletons (N_j=K) but
  W_Q/(σr_j)≈√K/σ. So eq (3)'s `U_j = C(1+W_Q/(σr_j)) ≥ N_j` with **K-independent C is FALSE** there, and
  if the variance were `M_j·N_j` the cost would inflate by √K → n^{2/3} (exactly the round-2 leak).
- **Why the algorithm survives:** the leader-estimator variance is `M_j·c_j` (component count), not
  `M_j·N_j`. And `c_j/(1+W_Q/(σr_j))` is **bounded by a small K-independent constant** (≤0.017 grid/
  uniform, ≤0.152 satellite — flat in K), because `(c_j−1) ≤ W_Q/r_j` is an exact identity. Recomputing
  the cost with the TRUE variance driver `c_j` (`t5f`), `cost/(√K·T²/η)` **decreases** with K
  (grid 0.021→0.005, uniform 0.084→0.014) — solidly Õ(√K). The `N_j` version is just a loose over-count
  that the write-up wrongly uses as the variance proxy.
- **Net:** the exponent is correct; the write-up should derive the sample count from `Var(Z)≤M_j c_j`
  with `c_j ≤ C(1+W_Q/(σr_j))`, not from `N_j ≤ U_j`. eq (2) (`N_j·a_j ≤ 8W_Q`) is itself fine
  (ratio ≈1.0, K-independent); the slip is only in the eq(2)→eq(3)→eq(8) chain that re-labels the
  variance bound as N_j. **Classify: GAP (write-up), not FATAL, no complexity leak.**

---

## Overall verdict

**Assembly SOUND + no new counterexample found ⇒ the round-4 closure LIKELY HOLDS.** The spatial-cell
estimator genuinely defeats the round-3 satellite obstruction: recovery is robust across all adversarial
families I could build (including features that are 1-cell-rare at their scale), and the true query
budget is Õ(√K) — the geometric and cost identities that make this work (packing W_Q=Ω(bδ), interleaving
(1), Riemann gap ≤σW_Q, the leader variance M·c, and `c_j=O(1+W_Q/(σr_j))`) all check out numerically and
scale correctly. The independent per-scale trials remove the round-3 covariance defect at its root.

**One residual GAP (fixable, non-fatal):** the §5/§6 cost write-up must use the component count `c_j` (not
the occupied-cell count `N_j`) as the variance bound in eqs (3)/(8); `N_j ≤ C(1+W_Q/(σr_j))` is false at
the a=h floor (N_j~Θ(√K)·W_Q/(σr_j)), but `c_j ≤ C(1+W_Q/(σr_j))` is true and is what the algorithm
actually pays. With that substitution the Õ(√K) accounting is intact.

**Remaining (not discharged here):** as in every prior round, this is AI-level verification, not
human-expert proof. The Lemma-3 black box (estimate w(MST(Q)) for an implicit K-grid support in
Õ(√K+n/K) from emptiness=1-P-count + sampling=Õ(n/K) + local adjacency) is now self-contained (no
unverified 20-year-old engine import), which is a real improvement over round 2 — but it is novel and
warrants human-expert checking of the variance/median-amplification details before any closure claim.

**Confidence:** spatial estimator defeats round-3 obstruction: **0.92**. Interleaving/Riemann/W-search/
K-est individually: **0.95+**. Cost is genuinely Õ(√K) (with the c_j fix): **0.82**. Full unconditional
Õ_ε(n^{1/3}) after §11 insertion: **~0.80** (up from the ~0.60 pre-audit), gated on the c_j write-up fix
and human-expert verification of Lemma 3. No FATAL, no new counterexample.
