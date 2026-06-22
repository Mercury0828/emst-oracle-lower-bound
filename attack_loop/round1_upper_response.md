**Verdict: obstruction / still open.**

I do not have a correct `o(sqrt(n))` EMST estimator. The CRT route cannot be made sub-`sqrt(n)` just by lowering the BFS threshold. The missing primitive is near-uniform sampling of non-empty grid cells, plus estimating their count. In the actual SoCG 2025 paper, the MST estimator calls `CellSampling(r)`, which itself costs `Õ(sqrt(n))`, and the paper proves an `Ω(sqrt(n))` lower bound for that cell-sampling primitive even in 1D. Source: arXiv:2504.15292, §4 and §5.3, especially Algorithm 1 / Lemma 17 / Corollary 18 / Lemma 19 and Theorem 30.

**Why the CRT improvement stalls**

At scale `i`, let `λ=(1+ε)^i`, and let `H_i` be the contracted graph on non-empty `λ`-grid cells. CRT needs:

1. a roughly uniform seed cell `v ∈ V(H_i)`;
2. a constant-factor estimate of `N_i = |V(H_i)|`;
3. local exploration to estimate `β(v)`.

If items 1 and 2 were free, the BFS threshold would not be the fundamental barrier: truncating components larger than `t` loses at most `N_i/t` components, and the planar packing bound gives `OPT >= Ω(λ N_i)`, so weighted bias is `λ N_i/t <= O(OPT/t)`. Constant or polylogarithmic `t` would suffice.

But items 1 and 2 are not free. The known implementation obtains them via cell sampling, and that primitive has an `Ω(sqrt(n))` query lower bound. Therefore any black-box CRT estimator requiring near-uniform non-empty-cell seeds inherits `Ω(sqrt(n))`, regardless of how clever the BFS threshold is.

**Why point sampling does not fix it**

A natural workaround is to sample a point uniformly and reweight by inverse cell multiplicity. For a sampled point in cell `v` with `a_v` points, the unbiased estimator is roughly

`Z = n * β(v) / a_v`.

This has bad variance. At a scale `λ=sqrt(n)`, put `M=sqrt(n)` isolated singleton cells and the remaining `n-M` points in one connected bulk region. Then `c_i=Θ(M)` and `OPT=Θ(λ M)=Θ(n)`, so the allowed additive error in `c_i` is `Θ(M)`. But

`Var[Z] = Θ(nM)`, so `q = Ω(n/M) = Ω(sqrt(n))`

point samples are needed. This is not a full MST lower bound, because a different rectangle-native estimator might exploit geometry, but it kills the obvious “replace cell sampling by point sampling” route.

**Achievable exponent**

The best certified upper bound remains `Õ(n^{1/2})`. I cannot prove an `o(sqrt(n))` algorithm, and the best known lower bound remains `Ω(n^{1/3})`; the gap is still real.

**Confidence**

My updated confidence that some non-CRT, counting-native `o(sqrt(n))` algorithm exists: **35%**.

My confidence that an `Õ(n^{1/3})` algorithm exists: **15%**.

The path would have to avoid near-uniform non-empty-cell sampling entirely and estimate the multiscale connectivity contribution from rectangle-count summaries in a way that does not secretly solve cell sampling.