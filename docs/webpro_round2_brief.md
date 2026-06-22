# Round 2 to GPT-5.5-Pro — the heavy-tail lemma (the last gap to Õ(n^{1/3}))

**This continues your round-1 thread.** Your round-1 result stands: we independently **verified it
numerically** (the death-time/MST-edge multiset identity holds exactly; the random-leader exploration is
O(log s); the two-grid bridge gives one heavy edge) and an **independent audit rated it (A): rigorous at
the checkable level, with the heavy-tail lemma as the only remaining gap.** Two things you flagged are
confirmed as the only loose ends — (i) the WSPD redundant-pair enumeration is a correctness-bookkeeping
detail (no √n), and (ii) setting the threshold L needs a constant-factor estimate of W. This brief asks
you to close the one remaining gap. As before: **use any method; the structural notes below are fallible
and non-binding.**

---

## 1. The precise lemma we need

Recall (your round 1) `w(MST) = ∫₀^∞ (c(t)−1) dt`, `c(t)=#single-linkage components at threshold t`;
your death-time estimator estimates the **bulk** `A_L = Σ_e min{w_e, L} = ∫₀^L(c−1)`(roughly) in
`Õ_ε(n^{1/3})` queries. The remaining piece is the **heavy tail**:

> **Heavy-tail lemma (target).** Given orthogonal range-counting-oracle access to `P ⊂ [Δ]²` (`|P|=n`,
> `Δ=O(n)`) and a threshold `L`, estimate
> **`B_L = Σ_{e∈MST(P), w_e > L} (w_e − L) = ∫_L^∞ (c(t)−1) dt`** (the total excess of the long MST edges
> above `L`) to **additive error `ε·W`** (`W = w(MST)`), using **`Õ_ε(n^{1/3})`** range-counting queries.
> The operative regime is `L = Θ(W / n^{2/3})`, where the number of long edges is
> `|{e : w_e>L}| = c(L)−1 ≤ W/L = n^{2/3}`.

Plus the contained sub-issue: obtain a **constant-factor estimate of `W`** (to set `L`) in `Õ(n^{1/3})`
queries — or design the tail estimator so it does not need `L` fixed in advance (e.g. a geometric search
over `L`, or a self-normalizing estimator). Folding this in is part of the lemma.

**If you close this, the worst case is done:** bulk (round 1) + tail (this lemma) ⇒ an **unconditional
`Õ_ε(n^{1/3})`** algorithm for `(1±ε)`-estimating `w(MST)` under the range-counting oracle — closing the
`Ω(n^{1/3})` vs `Õ(√n)` gap from above.

## 2. Why round 1's estimators do NOT reach the tail (your own analysis, confirmed)
The death-time sampler sees one rare heavy value among `n` ⇒ `Ω(n)` independent samples to catch it; the
random-leader `c(t)`-estimator costs `~n/c(t)`, which is `Ω(n)` when `c(t)=O(1)` (the bridge). The long
edges are **rare and geometric**; reaching them needs **spatial range information** — exactly the
ingredient the source's `Õ(√n)` algorithm uses and round 1 does not. So the tail estimator must be a
genuinely different, spatially-aware object.

## 3. Structural notes that MIGHT help (fallible, non-binding — ignore freely)
- **The tail is itself an MST-weight problem on `≤ n^{2/3}` super-clusters.** Contract each scale-`L`
  connected component of `P` to a super-node; the long MST edges (`w_e>L`) are exactly the MST edges of
  these `c(L) ≤ n^{2/3}` super-clusters, and `B_L` is (essentially) the MST weight of the super-cluster
  graph, shifted by `L`. This suggests a possible **recursion** (estimate the MST weight of `≤ n^{2/3}`
  super-points). The super-clusters are queryable spatially: a super-cluster is a maximal set of points
  pairwise within `L`-bottleneck; range counts can probe cluster bounding boxes / separations.
- **Long edges are bridges between well-separated regions.** In the two-grid worst case, a coarse
  spatial scan (a few large rectangle counts) already reveals "two clusters separated by `Θ(n)`", so
  that single bridge's length ≈ the inter-cluster gap is estimable cheaply. The general question is a
  hierarchy of up to `n^{2/3}` such bridges of varying lengths (up to `Δ=O(n)`).
- **A quadtree / hierarchical spatial decomposition** may localize the `≤ n^{2/3}` long edges: at each
  dyadic level, range counts identify nonempty well-separated cells whose connection contributes a long
  edge; the WSPD machinery you already use exposes candidate long pairs.
- **Counting vs summing:** the round-1 estimator can cheaply estimate `c(L)` itself at the boundary
  (`cost ~ n/c(L) = n^{1/3}`); what is hard is the **total excess length** `B_L`, since the lengths can
  be large. An importance/stratified scheme over edge-length scales `> L` (with the cheap `c(t)`
  estimator giving the count at each scale and spatial info giving the lengths) is one option.

## 4. What we'd like back
- **The heavy-tail lemma proved** (estimator + query bound `Õ(n^{1/3})` + the `(1±ε)`/variance analysis +
  range-counting implementability + the `W`-guess), yielding the unconditional `Õ(n^{1/3})` theorem; OR
- **a precise obstruction** (which step resists, and whether it is the same "needs spatial info" wall or
  a genuinely new one); OR
- **a lower bound** showing the tail genuinely needs `ω(n^{1/3})` queries — which, *together with* the
  round-1 bulk algorithm, would pin the query complexity at that exponent (a complete answer the other
  way: the truth would be determined by the rare-long-edge tail, and if it forces `Ω(√n)` you'd have
  closed the gap from BELOW). Note our (fallible) numerics suggested a constant-fraction weight gap is
  coarsely countable (a "spread-vs-concentrate" intuition) — but you may well see past that.

Please state your confidence and flag any concrete construction you'd like us to test numerically (we
can build it as an exact EMST over a simulated range-counting oracle and relay results, as we did for
round 1).
