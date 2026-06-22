# Round 5 to GPT-5.5-Pro — finishing: one write-up fix + a clean, referee-ready consolidation

**Strong news.** Your round-4 spatial-cell repair was put through two independent adversarial audits plus
exact-EMST numerics, including the exact dense-grid + satellites instance that broke round 2. Results:

- **Recovery: VERIFIED.** On the round-3 counterexample the spatial-cell estimator recovers `w(MST(Q))`
  (`hat/W_Q ≈ 1.0`), recovering the ~67% satellite tail that support-point sampling missed.
- **Cost: VERIFIED `Õ(√K)=Õ(n^{1/3})`, with no `n^{2/3}` blow-up.** An auditor built the per-scale budget
  `Σ_j M_jU_j/α_j²` with your own formulas and ran it on the satellite instance: the polylog-stripped
  core scales as `n^{0.28–0.32} ≤ n^{1/3}` (round-2's `n^{0.667}` is definitively absent). The packing
  payoff `b·δ/G = O(1)` and the additive (not multiplicative) entry of the `n/K` sampling are the
  structural reasons the leak does not recur.
- **Assembly: SOUND.** Interleaving (§2), Riemann reconstruction (§7, gap `≤ σW_Q`), the `W`-search (§8),
  `K`-estimation (§9), and the §11 re-insertion into the round-2 reduction all check out.
- **Counterexample hunt: NOTHING.** A hard search (thin lines, grids, fractal/Cantor, multiscale
  satellites, rare-component-in-one-cell) found no instance breaking recovery or cost. The estimator is
  now self-contained — no 20-year-old engine import.

There is **one fixable write-up gap**, and then we'd like a clean consolidation for human verification.

## 1. The write-up fix (variance via `c_j`, not `N_j`)

Your eqs (2)/(3)/(8) bound the per-scale sample budget through the **occupied-cell count** `N_j`, via
`N_j ≤ C(1 + W_Q/(σr_j))`. An auditor found this bound is **false at the `a=h` floor**: there `N_j` can be
`≈ Θ(√K)·W_Q/(σr_j)` (measured `0.32·√K`, `0.37·√K` on grid/uniform). If the leader-estimator variance
were `M_j·N_j`, the cost would inflate by `√K` to `n^{2/3}` — exactly the round-2 leak.

The algorithm survives because the **true variance of your empty-cell leader estimator is `M_j·c_j`**,
where `c_j` is the **component count** of `Γ_{r_j}`, not the occupied-cell count `N_j`. And
`c_j ≤ C(1 + W_Q/(σr_j))` IS true (the standard `c(t)−1 = #{MST edges > t} ≤ W_Q/t` identity; the
auditor measured the ratio `≤ 0.15`, flat in `K`). Recomputing (8) with `c_j` keeps the cost `Õ(√K)`.

**Please confirm and restate the cost accounting with `c_j` (component count) in place of `N_j`** in
eqs (2)/(3)/(8) and the `U_j` definition — i.e. use the deterministic upper bound `U_j ≥ c_j` (not
`U_j ≥ N_j`) in the trial-count `k_j = Θ(M_j U_j/α_j²)`. (If for some reason the estimator's variance
genuinely needs `N_j` rather than `c_j` — e.g. if a near-empty exploration can return `Z=M` off a
non-leader — please flag it; the auditor's reading is that exactly `c_j` cells are component minima, so
`Var(Z) ≤ M_j c_j`, but you wrote the lemma and should confirm.)

## 2. The consolidation we'd like (for human-expert verification)

This thread now spans four rounds with corrections; for a human referee we need ONE clean,
self-contained statement and proof. Please produce:

- **The final Lemma 3** (the support-MST estimator) — statement + self-contained proof, with the `c_j`
  fix incorporated, all constants/`σ,η,ρ` dependencies explicit, and each query-cost line tied to a
  concrete range-counting operation (emptiness / count / uniform-point-sample), so the
  `Õ_η(√K + n/K)` bound is line-by-line auditable.
- **The final Theorem** (the unconditional `Õ_ε(n^{1/3})` MST-weight estimator) — statement + the full
  assembly: support regularization (round 2 §1, Lemma 1 packing), snapping/interleaving (round 2 §3 /
  round 4 §2), the bulk `A_L(P)` via the round-1 clipped death-time estimator, `A_L(Q)` with `O(1)`
  support samples, `B_L(Q)=W_Q−A_L(Q)` via Lemma 3, the snapping transfer `B_L(Q)→B_L(P)`, and the
  `W`-search setting `L=Θ(W/n^{2/3})` — with the global `(1±ε)` error budget shown to compose.
- **Explicitly list any step that is "standard but not written out"** (verification debt) vs. any step
  you are less than ~95% sure of — so the human verification can prioritize.
- Your final confidence, and any remaining instance you'd like us to test numerically.

We will run a final independent audit of the consolidated write-up, then hand it to **human-expert
verification** (we do not claim the theorem proved until a human referee has checked it; we will also do
a final 2025–26 preprint priority sweep before any submission). Thank you — this looks like it closes the
Driemel et al. gap from above; we want the write-up to be airtight before saying so.
