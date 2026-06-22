**Verdict:** no equal-cardinality C1 gadget exists at `p = n^{1/2+o(1)}` under the stated tiling model. The sharp threshold is `c = 2/3`. The obstruction is not the sparse gadget’s internal cost; it is the unavoidable global backbone.

**1. General Upper Bound On Any One-Cell Gap**

Let the cells have side length `s`, and let two instances differ only inside one cell, replacing `S` by `H`, with `|S| = |H| = p`.

For any `p` points in a square of side `s`,

\[
\operatorname{EMST} \le C s\sqrt p .
\]

This is the standard grid/snake upper bound: partition into about `sqrt(p) x sqrt(p)` boxes and connect occupied boxes in scan order.

Now let `R` be all points outside the changed cell. By MST monotonicity and adding `H` to an MST of `R \cup S`,

\[
w(R\cup H)
\le w(R\cup S\cup H)
\le w(R\cup S) + O(s\sqrt p).
\]

Symmetrically,

\[
|w(R\cup H)-w(R\cup S)| \le C' s\sqrt p.
\]

So no single-cell replacement, no matter how hierarchical or fractal, can change the global EMST by more than `O(s sqrt(p))`.

**2. Global Backbone Lower Bound**

Suppose `m = k^2` square cells of side `s` tile `[Δ]^2`, so `Δ = ks`, and every cell contains at least one point.

Let `T` be the Euclidean MST, length `L`. Every point of `[Δ]^2` is within distance `sqrt(2)s` of some occupied cell point, hence within that distance of `T`. Thus `[Δ]^2` lies in the `sqrt(2)s`-neighborhood of `T`.

A polygonal tree of length `L` has `r`-neighborhood area at most `O(rL+r^2)`. Therefore

\[
\Delta^2 \le O(sL+s^2),
\]

so for large `m`,

\[
w(P)=L \ge c_0 s m.
\]

This lower bound holds for all-sparse and one-heavy instances alike.

Combining the two bounds,

\[
\frac{\text{one-cell gap}}{w(P)}
\le
O\!\left(\frac{s\sqrt p}{sm}\right)
=
O\!\left(\frac{\sqrt p}{m}\right).
\]

If `p = n^c` and `m = n^{1-c}`, then

\[
\frac{\sqrt p}{m}
=
n^{c/2-(1-c)}
=
n^{3c/2-1}.
\]

A constant fraction requires `3c/2 - 1 >= 0`, i.e.

\[
c \ge 2/3.
\]

In particular, at `p = n^{1/2+o(1)}`, the best possible fraction is

\[
n^{-1/4+o(1)},
\]

so the desired constant-fraction C1 gadget is impossible.

**3. Construction At The Sharp Threshold `c = 2/3`**

Take integers `K -> infinity` and a fixed large integer constant `R`. Set

\[
m=K^2,\qquad p=R^2K^4,\qquad n=mp=R^2K^6,
\]
\[
\Delta=n,\qquad s=\Delta/K=R^2K^5.
\]

So `p = Θ(n^{2/3})`, `m = Θ(n^{1/3})`.

Sparse gadget: put the `p` points on one horizontal line with spacing `K`:

\[
(0,s/2),(K,s/2),\ldots,((p-1)K,s/2).
\]

Since `(p-1)K = s-K`, this fits in the cell and has exact EMST

\[
(p-1)K = \Theta(s)=\Theta(n^{5/6}).
\]

All-sparse global MST: connect each row as one long horizontal path and connect adjacent rows by one vertical edge. This gives

\[
w_{\text{sparse}} \le R^2K^7 + O(R^2K^6).
\]

The backbone lower bound gives `w_sparse = Θ(R^2K^7) = Θ(n^{7/6})`.

Heavy gadget: let

\[
q=RK^2,\qquad D=RK^3,
\]

and place a `q x q` grid in the cell with spacing `D`. Then `q^2=p`, and the grid fits because `(q-1)D < s`.

Every pair of distinct heavy points has distance at least `D`, and nearest-neighbor grid edges connect the grid, so the exact heavy-cell EMST is

\[
(p-1)D
=
(R^2K^4-1)RK^3
=
R^3K^7 - O(RK^3)
=
\Theta(s\sqrt p)
=
\Theta(n^{7/6}).
\]

For the one-heavy instance,

\[
w_{\text{heavy}} \ge R^3K^7-o(K^7).
\]

Choosing `R` large enough,

\[
w_{\text{heavy}}-w_{\text{sparse}}
\ge \Omega(R^3K^7)
=
\Omega(n^{7/6}).
\]

Also the replacement upper bound gives `w_heavy = O(R^3K^7)`, so

\[
\frac{w_{\text{heavy}}-w_{\text{sparse}}}{w_{\text{heavy}}}
\ge \varepsilon_R
\]

for a fixed constant `ε_R > 0`.

Thus the source-style `uniform grid` versus `strip` construction is not merely sufficient at `c=2/3`; the previous bounds show `c=2/3` is the smallest possible exponent.

**4. Achievable Exponents**

For general `p=n^c`, `m=n^{1-c}`, with `Δ=Θ(n)`,

\[
s = \Theta(n^{(1+c)/2}).
\]

The maximum possible one-cell heavy cost is

\[
s\sqrt p = \Theta(n^{1/2+c}).
\]

The unavoidable global MST scale is

\[
sm = \Theta(n^{3/2-c/2}).
\]

The inequality `1/2+c >= 3/2-c/2` is exactly `c >= 2/3`.

At the threshold construction:

\[
a=7/6,\qquad b=5/6,
\]

with global sparse/backbone weight also `Θ(n^{7/6})`.

**5. Confidence And Final Status**

Updated confidence that an equal-cardinality C1 gadget exists at `p=n^{1/2+o(1)}`: **~1%**; under the stated cell-tiling assumptions, the argument above rules it out.

Final verdict: **constructed threshold `c=2/3`; refuted the `c=1/2` target.**