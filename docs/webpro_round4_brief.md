# Round 4 to GPT-5.5-Pro — the sharper Lemma 3 (spatial-first support-MST estimation)

**You were right, and we confirmed it.** Your round-3 refutation of the round-2 closure is accepted: we
numerically reproduced the seed-reuse failure on your dense-grid + satellites instance — a polylog shared
pool gives per-run relative error `0.28→0.68` (growing with `K`; even `√K` samples leave `~0.47` error),
so estimating `w(MST(Q))` by sampling genuinely needs `Ω(√K)` samples, i.e. `n^{2/3}`. The round-2
closure is withdrawn. (Our own three audits wrongly passed the seed-reuse — a good reminder that
"AI-verified ≠ proved.") The **round-1 instance-sensitive `Õ(n/N_eff)` result is unaffected and stands.**

This brief asks the one question that now decides the gap, which is exactly your sharper Lemma 3 (§6):

> **Lemma 3 (sharper).** Given the implicit `K`-point grid support `Q` (centres of nonempty cells of a
> grid over `P`) with: (1) rectangle EMPTINESS on `Q` = one orthogonal range-count on `P`; (2) uniform
> support sampling = `Õ(n/K)` `P`-queries; (3) local directional / WSPD adjacency = polylog `P`-counts —
> estimate `w(MST(Q))` within `(1±η)` using `Õ_η(√K + n/K)` total `P`-queries. (At `K=Θ(n^{2/3})` this is
> `Õ(n^{1/3})`.) The obstruction you isolated: recover the rare, low-support-mass components (your
> satellites) **without** paying for `Ω(√K)` genuinely independent support samples.

## The natural repair (your §5/§6 direction, made explicit — fallible, please confirm/improve/refute)

Your counterexample's satellites are **rare but geometrically DISTINCT** (far-apart cells). That suggests
splitting `w(MST(Q))` into a **spatial** part (the rare long edges, found by EMPTINESS, never sampled)
and a **sampled** part (the dense interiors, where samples are common):

1. **Active-block subdivision by range-EMPTINESS (cheap on `P`).** An adaptive quadtree finds the
   `O(√K)` "active" cells of `Q` (Czumaj's stage-1 subdivision), each located by `O(log Δ)` support-
   emptiness queries = `O(log Δ)` `P`-counts. The satellites sit in their own active cells and are
   **found this way, not sampled** — this is precisely what your shared pool could not do, and what
   range-emptiness can.
2. **Inter-block MST computed EXPLICITLY** on the `O(√K)`-vertex active-block graph (the long edges,
   including all satellites): build the `(1+ρ)`-WSPD on the `O(√K)` active-block representatives (your
   nested-cone §5 makes every adjacency query an orthogonal range-count), and take its MST exactly. This
   is `Õ(√K)` `P`-counts and **involves no support sampling**, so the rare-long-edge variance never
   arises.
3. **Intra-block (dense) MST contribution by SAMPLING** (your round-1 death-time / random-leader
   estimator): a uniform support sample lands in a dense block w.h.p. (the dense interiors carry the
   common mass), so `polylog` samples (each `Õ(n/K)`) estimate the within-block contribution to `(1±η)`
   — the satellites are excluded from this term (they are inter-block, handled in step 2).
4. **Total** `Õ_η(√K + n/K) = Õ_η(n^{1/3})`.

The crux to settle: does this **spatial/sampled split** (rare long edges via explicit subdivision; dense
short edges via sampling) cleanly avoid the `Ω(√K)`-sample obstruction, with the error budget and the
range-counting implementability all checking out? In particular: (a) is the `O(√K)`-active-block bound
genuinely `O(√K)` here (Czumaj's stage-1, but realized by emptiness)? (b) does computing the inter-block
MST explicitly capture ALL edges of length `> ` the active-block scale (so no long edge is missed by the
sampler)? (c) does the within-block sampled term have bounded variance (no rare-high-value edge survives
inside a block, since long edges are inter-block)? (d) does the active-block graph itself avoid a
recursion (its `O(√K)` vertices' MST is computed explicitly, not re-estimated)?

## What we'd like back
- **The sharper Lemma 3 proved** (via this spatial/sampled split or any route), yielding the unconditional
  `Õ_ε(n^{1/3})` theorem; OR
- **the precise obstruction** (if the split still hides an `Ω(√K)` sample or a recursion); OR
- **a lower bound** showing support-MST estimation here genuinely needs `ω(n^{1/3})` `P`-queries — which,
  with the round-1 bulk algorithm, would mean the true query complexity is `>n^{1/3}` (a complete answer
  the other way, and a surprise worth its own scrutiny).

Please give your updated confidence and flag any instance you'd like us to test numerically (we can build
it as an exact EMST over a simulated range-counting oracle, as we did for your round-3 counterexample —
which we confirmed). We will not claim any theorem proved until it survives a fresh independent audit and
human-expert verification.
