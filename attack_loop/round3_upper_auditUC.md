# Round 3 (UPPER) — Audit U-C: filament verification + the cost-vs-λ tradeoff

**Status:** the U-C subagent was cut off by a server-side rate limit before writing its verdict, but it
produced 9 runnable scripts (`attack_loop/auditUC_task*.py`). The orchestrator **re-ran all of them**
and synthesizes the verified numerics below. Numerical facts are labeled [VERIFIED]; the algorithmic
reading is labeled [SYNTHESIS — to be proven by the attacker], per the orchestrator's referee role.

## Task 1 — codex's filament obstruction is REAL [VERIFIED]
Instance: n=N², λ=N=√n, N singletons spaced ~λ along a diagonal + dense bulk. Exact EMST:
- minNN(island) ≈ √2·λ ⇒ isolated until scale Θ(λ). persist ≈ N·λ, **persist/n = 1.414 (constant)** ⇒
  constant-fraction contribution. w_MST/n = O(1) (3.66→3.25) ⇒ **NO scatter-blowup**.
- uniform 2D λ-box probe **hit-rate ≈ 1/N = Θ(1/√n)** (0.048→0.023). ✓ codex's filament defeats the
  *uniform 2D-box* importance-sampling primitive of [[U-P2]].

## Task 2/3b — codex's λ=√n filament is REPAIRED by slabs [VERIFIED]
Only N islands exist ⇒ ≤ N nonempty width-λ slabs per axis ⇒ 1-D slab-count cost ≤ O(√N)=O(n^{1/4}).
Measured slab estimator on the diagonal: ratio≈0.70 (constant, tightenable), **queries ~√N = n^{1/4} ≪
√n** (128/226/384/633 for n=256…16384). So codex's specific λ=√n filament is NOT a √n obstruction.

## Task 3d/3e — the REAL crux: a SMALL-λ filament, and the cost-vs-λ tradeoff [VERIFIED + SYNTHESIS]
For a diagonal of M=n/λ singletons spaced λ (persist M·λ=Θ(n), no blowup, lonely-fraction = M/n = **1/λ**):
- [VERIFIED] uniform-2D-box cost ~ M = n/λ; slab cost ~ √M = √(n/λ). Both → √n as λ→polylog. The
  auditor flagged small-λ as "the genuine all-sparse obstruction candidate."
- [VERIFIED by the orchestrator — `attack_loop/orch_check_pointsample.py`] the auditor measured
  *2D-box* (~n/λ) and *slab* (~√(n/λ)) cost but MISSED the third primitive: **uniform POINT-sampling**
  (sample an actual point p∈P — available via range-counting + binary search on cumulative counts,
  O(log Δ)/sample — and test "is p lonely at scale λ?" via a λ-box/disk count). The lonely-fraction is
  **1/λ**, and point-sampling **recovers it** (measured est_f tracks 1/λ across λ=2…√n, all n) in
  **~λ·polylog** queries — point samples land ON points (hit a lonely one w.p. 1/λ), NOT in empty space
  (1/M). (My first check had a box-size bug giving est_f=0 — consecutive islands at spacing λ fell in
  each other's λ-box; fixed with a Euclidean-NN>λ test, after which est_f≈1/λ.) Then per scale:
  > **cost(λ) ≤ min( point-sample ~ λ , slab ~ √(n/λ) ).** [VERIFIED] the two branches cross at
  > **λ = n^{1/3}** (λ=√(n/λ) ⇔ λ^{3/2}=√n), where both equal **n^{1/3}** (measured min-column peaks at
  > λ=n^{1/3}: 16/25/40 for n=4096/16384/65536). Away from n^{1/3}, one branch is cheaper.
  Over the Õ(1) scales, worst-case total **Õ(n^{1/3})** — matching the Ω(n^{1/3}) floor. **[SYNTHESIS]
  This is the candidate closing algorithm for the SINGLETON stratum; the attacker must (a) extend it to
  all component sizes/strata, (b) integrate the dense-block (Lemma-32) stratum, (c) prove variance +
  (1±ε), (d) give the counting-oracle implementation of point-sampling + loneliness.**

## Task 3f/3g — does a SMALL-λ filament give a √n LOWER bound? [VERIFIED numerics, SYNTHESIS leaning NO]
- [VERIFIED] coarse g×g grid counts cannot recover persistence (need cell side ~λ ⇒ g~n/λ ⇒ g²≫√n
  queries) — coarse counts see "mass on the diagonal" but not whether it is lonely (persist λ) or
  clustered (persist O(1)); the Euler/[[U-P2]] cancellation. So persistence is NOT coarsely readable.
- [VERIFIED] task3g hard-pair test: at box side ≥ λ, **max|c_A − c_B| = 1** (a single-cell difference),
  NOT 0. [SYNTHESIS] A constant-fraction MST gap requires the A/B difference SPREAD over Θ(M)=Θ(n/λ)
  cells (each ±1); a uniformly-placed λ-box then hits a *differing* cell with **constant probability**,
  so A,B are **coarsely distinguishable in O(1/ε²) queries** ⇒ NOT a hard pair. To make them hard
  (concentrate the difference) collapses the MST gap to o(OPT). **Same spread-vs-concentrate vise as
  [[P1]]/[[U-P2]] ⇒ no √n lower bound survives** (consistent with [[U-P1]] and the paper proving only
  Ω(n^{1/3})). (This needs a rigorous hitting/coupling argument from the attacker to be certain.)

## Verdict
- **(I)-leaning: the obstruction is REPAIRABLE; the pivot is alive and pointed at Õ(n^{1/3}).** codex's
  filament is real but only defeats the 2D-box primitive; combining **point-sampling (small λ) + slab
  (large λ)** balances at n^{1/3}. No √n lower bound survives the spread-vs-concentrate vise.
- **Confidence (orchestrator):** o(√n) exists **~60%**; Õ(n^{1/3}) **~35%** (up from 45%/25% — the
  cost-vs-λ balance is concrete and lands exactly at the floor, but the full multi-stratum (1±ε) proof
  is unbuilt and is the real remaining work).
- **Caveat:** this synthesis is the orchestrator refereeing the numerics; the algorithm + variance +
  (1±ε) + all-strata + dense-block integration must be ORIGINATED and PROVEN by the attacker (Round 4),
  then independently audited. Scripts: `attack_loop/auditUC_task*.py` (run via `sim/.venv`).
