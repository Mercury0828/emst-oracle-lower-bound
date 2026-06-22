**Verdict: obstruction.**

I cannot give an audit-surviving proof of the requested theorem from the stated substrate. The precise failing point is the large-λ coupling lemma in P2:

> “For every weight-relevant scale, λ·c(λ)/n = Ω(1) implies c(λ)=O(n/λ).”

That statement is false under the stated hypotheses.

**Counterexample**

Let `n = q^2`, with large even `q`. Set

`d = q/2`, `λ = d/2 = q/4`.

Place points on the integer grid

`P = {(1 + id, 1 + jd) : 0 <= i,j < q}`.

Then

`Δ = (q-1)d + 1 <= q^2 = n`,

so `P ⊂ [Δ]^2` with `Δ = O(n)`.

Adjacent points are distance exactly `d = 2λ`, so at threshold `λ` there are no edges. Hence

`c(λ) = n`.

Also `λ > n^{1/3}` for large `q`, and

`λ c(λ) / n = λ = Θ(n^{1/2})`,

so this is strongly weight-relevant. But

`n/λ = Θ(n^{1/2})`, while `c(λ)=n`,

so

`c(λ) / (n/λ) = Θ(n^{1/2})`.

Thus `c(λ)=O(n/λ)` is false.

This is not a low-weight stratum. The EMST has weight

`w(MST(P)) = (n-1)d = Θ(n^{3/2})`,

because every spanning-tree edge has length at least `d`, and the grid adjacency tree attains `(n-1)d`. The interval `[0, λ]` alone contributes

`∫_0^λ (c(t)-1) dt = λ(n-1) = Θ(n^{3/2})`,

a constant fraction of the MST weight.

**Consequence**

The advertised large-scale accounting

`cost = Õ(sqrt(n/λ))`

does not follow from the stated coupling. In this example, the number of nonempty λ-cells is `n`; the claimed intermediate bound via `c(λ)=O(n/λ)` fails by a polynomial factor. A different large-λ estimator might still exist, but it must explicitly handle the regime `c(λ) >> n/λ`; the current proof obligation does not.

The small-λ Horvitz-Thompson part is plausibly provable: bucket estimator `n/|C(p)|` is unbiased, with variance controlled by component-size strata and median-of-means. Range-counting implementability of sampling and bounded exploration is also standard assuming the stated spanner primitive. But those pieces do not repair the missing worst-case large-λ scalar estimator.

**Precise residual gap**

To complete the theorem, one needs a replacement lemma of the form:

For every `P ⊂ [Δ]^2`, every `λ > n^{1/3}`, and every weight-relevant scale, there is a range-counting implementable estimator for the scalar `c(λ)` with additive error compatible with the global `ε OPT` budget, using `Õ(n^{1/3})` queries, including the case `c(λ) >> n/λ`.

That lemma must include its exact estimator, debiasing, and variance proof. The empirical “≈1.01 bias” observation is not a substitute for this worst-case argument.

**Confidence**

- 98% confidence that the stated large-λ proof obligation is false as written.
- 95% confidence that the requested theorem is not proved by §2-§3.
- Verdict: obstruction to the supplied proof route; theorem remains open from this brief.

Python reconfirmation was not possible: the sandbox rejected the inline Python command, so I could not run the requested end-to-end numerical checks.