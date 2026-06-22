I cannot honestly complete §5 from the stated substrate. The missing concentration/tiling lemma is false as stated.

**Verdict:** specific-stratum obstruction to the localized-probe algorithm; global upper bound remains open.

The failing stratum is a **1-dimensional filament of low-mass, long-persistence components**.

Construction: let `n = N^2`, `Delta = Theta(n)`, and set `lambda = N`. Put `N` singleton “islands” at spacing `Theta(lambda)` along a diagonal or snake-like path through an `N x N` grid of `lambda`-cells. Add the remaining `n - N` points as a dense connected bulk with MST cost `Theta(n)`.

At scale `~lambda`, each island is a singleton component with death scale `Theta(lambda)`, so its persistence contribution is `Theta(lambda)`. The filament contributes

```text
N * lambda = N^2 = Theta(n),
```

a constant fraction of the total MST weight. Consecutive islands are only `Theta(lambda)` apart, so there is no “scatter blowup”; the MST cost does not become an easy huge signal.

But the certifying `lambda`-neighborhoods occupy only

```text
N * lambda^2
```

area inside an axis-aligned bounding region of area

```text
N^2 * lambda^2.
```

So a localized `lambda`-box probe hits the stratum with probability only `Theta(1/N) = Theta(1/sqrt(n))`. Thus the desired lemma

```text
high-value stratum => probe-hit probability at least 1/polylog(n)
```

is false. This is not the dense Lemma-32 gadget, and the `n^{1/3}` coarse-cell scan does not address it.

A partial algorithm works under an added **thickness condition**:

```text
For every high-value stratum H at scale lambda, its certifying lambda-neighborhoods
occupy at least rho >= 1/polylog(n) of some identifiable probe region R.
```

Then `O(rho^{-1} eps^{-2} log(1/delta))` localized probes estimate that stratum by standard bounded Horvitz-Thompson / median-of-means concentration, without estimating any per-scale `N_i` or `c_i` to relative error. The dense Lemma-32 stratum can be integrated by scanning the `Theta(n^{1/3})` coarse cells, matching the lower bound.

But without a new lemma handling 1D filaments, the worst-case query count of the localized-probe route reverts to `Theta(sqrt(n))`.

A plausible repair would need projection- or slab-based sampling: if area density is small but MST persistence is large, maybe some axis projection has large density. I do not have a proof that range-counting slab probes can recover component persistence with bounded variance and without reintroducing cell sampling.

I also could not run the requested Python numerics because this session’s policy blocks Python execution. Analytically, the filament instance predicts exactly the bad behavior: localized probe hit rate `~ n^{-1/2}` despite `Theta(n)` MST contribution.

**Achievable exponent from the proved argument:** not `o(sqrt n)`; only conditional `Õ(n^{1/3})` if a new filament/projection lemma is proved.

**Confidence update:** `o(sqrt n)` achievable: ~45%. `Õ(n^{1/3})` achievable: ~25%.