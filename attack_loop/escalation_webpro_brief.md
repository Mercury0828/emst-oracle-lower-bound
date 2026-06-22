# Brief to GPT-5.5-Pro — Query complexity of estimating the Euclidean MST weight under a range-counting oracle

**PART I below is the actual open problem — solve THAT, fresh, by any method.** PART II is optional
context from our own automated exploration; it is **UNVERIFIED and may contain errors** — use it only
to avoid repeating dead ends, feel free to ignore all of it, and please challenge anything that looks
wrong. Do not let it anchor you; a fresh approach (or a refutation of our claims) is very welcome.

---

# PART I — The problem (this is the ask)

Let `P` be a set of `n` points in the integer grid `[Δ]²`, with spread `Δ = O(n)`. You may access `P`
**only** through an **orthogonal range-counting oracle**: each query is an axis-aligned rectangle `R`,
and the oracle returns the **exact integer `|P ∩ R|`**. Design a randomized algorithm that, with
constant success probability, outputs a **`(1 ± ε)`-multiplicative estimate of the Euclidean
minimum-spanning-tree weight `w(MST(P))`** (fixed constant `ε ∈ (0,1)`), using **as few oracle queries
as possible**. (Equivalently, also of interest: prove a lower bound on the number of queries any such
algorithm needs.)

**Known (Driemel, Monemizadeh, Oh, Staals, Woodruff, "Range Counting Oracles for Geometric Problems,"
SoCG 2025, arXiv:2504.15292):** `Õ(√n)` queries suffice (their Thm 30); `Ω(n^{1/3})` queries are
necessary (their Lemma 32). **The gap between `Ω(n^{1/3})` and `Õ(√n)` is open.**

**What we want:** settle or improve the query complexity, in **either** direction —
- an algorithm using `o(√n)` queries (ideally `Õ(n^{1/3})`, closing the gap from above up to `n^{o(1)}`); or
- a lower bound above `Ω(n^{1/3})` (ideally `Ω(√n)`, closing it from below).

A full proof either way is the goal; a rigorous partial result plus a precise statement of the
remaining obstruction is also valuable. **Use any method.** Please also state your confidence in the
final claim, and flag any concrete construction/counterexample you'd like us to test numerically (we
can run exact-EMST + range-counting-oracle simulations and relay results back).

That is the entire problem. You can stop reading here and just solve it. PART II is optional.

---

# PART II — Optional context (UNVERIFIED — our automated exploration; may be wrong)

> ⚠️ Everything in Part II except §A was produced by an automated solver + automated audits + small
> exact-EMST numerics. It is internally consistent and numerically spot-checked, but **NOT human-
> refereed, and some of it may be wrong**. We give it only so you don't re-walk paths we think are
> dead. Treat it as hypotheses, not facts. If any item is mistaken, telling us is as valuable as a
> construction. Do not feel bound by any of it.

## §A. Reliable background (from the published source paper, not from us)
The source's `Õ(√n)` algorithm uses a Chazelle–Rubinfeld–Trevisan (CRT) reduction on a geometric
`(1+ε)`-spanner, via the cluster-count identity (with `c(λ)=#connected components of P at single-linkage
threshold λ`): `w(MST) = (n−Δ) + Σ_i λ_i·c(λ_i) = ∫₀^∞ (c(t)−1) dt`. It estimates each `c(λ)` with a
CRT component-count estimator that needs near-uniform sampling of non-empty `λ`-cells plus an estimate
of `N(λ)=#non-empty λ-cells`; the source proves (their §4) that this **cell-sampling sub-primitive
costs `Ω(√n)` even in 1-D**. (A separate `Ω(√n)` of Czumaj et al. is for the weaker *emptiness* oracle,
deterministic, `O(n^{1/4})` error — it does not transfer to this counting / randomized / `(1±ε)`
setting.) The `Ω(n^{1/3})` lower bound is a geometric *hitting* bound, not an information/bit count.

## §B. What our automated exploration believes it found (UNVERIFIED — may be wrong)
These are claims, each with the reason we currently believe it. **Any could be mistaken** — in
particular the "dead route" reasons are exactly the kind of thing a stronger solver might route around.

1. **(LB) The gadget-packing lower-bound technique seems to cap at `Ω(n^{1/3})`.** We believe: hiding a
   single special "heavy" cell among `m` disjoint equal-cardinality cells changes `w(MST)` by only
   `O(s√p)` (`s`=cell side, `p`=points/cell), while the inter-cell backbone forces `w(MST) ≥ Ω(s·m)`;
   `s` cancels ⇒ relative gap `≤ O(√p/m)`, forcing `m ≤ n^{1/3}`. A multi-needle/planted-pattern
   version seemed to cap the same way under an `O(1)`-per-query-coverage requirement. **Caveat: this is
   only a barrier against ONE technique and is itself only "near"-proved (a loophole remains); a `√n`
   lower bound by a different mechanism is not excluded.** If you can build one, great.
2. **(reduction) The weight reduces to estimating the scalars `c(λ)`.** Via the cluster-count integral
   (§A), the whole task is estimating the `Õ(1)` scalars `{c(λ_i)}` to summed error `≤ ε·OPT`.
3. **(cost arithmetic, elementary) An idealized two-branch estimator would give `Õ(n^{1/3})`.** For a
   uniform random point `p`, `Y_λ(p)=1/|C_λ(p)|` has `E=c(λ)/n`, `Var≤c(λ)/n`, so `~n/c(λ)` samples
   estimate `c(λ)`; a complementary localized estimator would cost `~√(c(λ))`. `min(n/c, √c) ≤ n^{1/3}`
   (max at `c=n^{2/3}`). **But the IMPLEMENTATION of these estimators in range-counting queries is open
   — see §C; this is just arithmetic assuming the estimators exist.** (We earlier over-stated this as a
   "proven cost model"; it is not — it is conditional on §C.)
4. **(possible obstruction to lower bounds) "spread-vs-concentrate".** In our small numerics, any two
   instances whose `w(MST)` differs by a constant fraction differed in a way *spread* over many cells,
   hence detectable by a few large rectangle counts; concentrating the difference shrank the weight gap.
   This *suggests* (does not prove) that a `√n` lower bound for the weight cannot come from hiding a
   low-measure needle. **This is numerical intuition only and could be wrong.**
5. **(suggestive) The cell-sampling `Ω(√n)` does not obviously transfer to the weight.** In 1-D the MST
   weight is `x_max−x_min`, independent of cell occupancy, so the source's cell-sampling hardness does
   not by itself lower-bound the weight. Several sub-problems we hit are `√n`-hard yet the weight seemed
   recoverable another way. (Again: a pattern in examples, not a theorem.)

## §C. Where our own attempt is currently STUCK (the crux, as we see it — you may see past it)
Following the CRT/`c(λ)` route (§A, §B.2–3), our difficulty concentrates into one primitive we could
not implement: **estimate, in `polylog(n)` (or any `o(√n)`) range-counting queries, a point `p`'s
single-linkage component size `|C_λ(p)|` (or an unbiased `1/|C_λ(p)|`, or the scalar `c(λ)` itself).**
Naive attempts fail in our hands: a box count gives `p`'s local degree, not its whole component or its
death scale; "is `p` isolated?" is biased (size-2 components already make `c(λ)=n/2`); exploring a
component costs its size (an instance of `n^{2/3}` chains of length `n^{1/3}` forces `n^{2/3}`); counting
non-empty cells measures spatial support, not component count (one filament = 1 component over many
cells). This "**cheap connectivity from additive counts**" question may be the real crux — or our whole
CRT framing may be the wrong route and a different estimator of `w(MST)` (or a lower bound) avoids it
entirely. **You are explicitly invited to abandon this framing.**

## §D. Routes our automated process believes are dead (reasons may be wrong — overturn if you can)
- Speeding up the source CRT by lowering its per-component exploration depth (the binding cost is the
  cell-sampling `Ω(√n)`, not the depth).
- A uniform (non-importance) point estimator `n·Σλ/|C_λ(p)|` (variance `Θ(√n)` on a rare-high-value
  instance).
- "weight-relevant scale ⇒ `c(λ)=O(n/λ)`" — false (a uniform grid has `c(λ)=n` at a weight-relevant
  scale); but that grid's weight is itself trivially `~√(n·Area)`.
- Estimating `Σλ·V`, `Σλ·E` (occupied cells, adjacencies) separately and subtracting — the cycle-rank
  term cancels them (occupancy totals lose connectivity).
- The single-needle and active-subset multi-needle lower-bound constructions (cap at `n^{1/3}`, §B.1).

---

**Bottom line:** Part I is the real, original open problem; please attack it with your full power and
your own ideas. Part II is a fallible map of where we got stuck — useful only if it saves you time, and
worth correcting if we got something wrong.
