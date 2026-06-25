VERDICT: SOUND-WITH-FIXES

M1: FIXED. The bad implication is gone. Appendix A now says the upper bound comes from the predecessor: “the predecessor pair is not well-separated, so `d(c,p(c'))< r(p(c'))/\rho=O(s/\rho)`,” and then “also `d(c,c')=O(s/\rho)`” at [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:125). With Lemma 22’s `r(c') in [s/2,2s]`, this gives only `O(\rho^{-2})` same-scale candidate cells. The final membership and length checks then keep only real incident edges.

M2: PARTIAL. The local predicate is now sufficient for the theorem, but it is not literally Algorithm 2 on equal-size ties. Appendix A defines “breaking a tie `r(c)=r(c')` by the `z`-order” and says the predecessor is obtained by replacing `c'` with `p(c')` at [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:59). The extracted Algorithm 2 instead only swaps on strict inequality: “if `r(c')<r(c)` then exchange,” then splits `c'` at source lines 806-809. So: predecessor uniqueness and `O(1)` local testing are fixed for the paper’s deterministic tie-broken CK variant, but the text should not claim exact identity with DMOSW Algorithm 2 unless it states this variant explicitly.

M3: FIXED. The stretch language is now internally consistent: “With geometric separation `1/\rho` the WSPD spanner has stretch `1+O(\rho)`” and “the stretch is at most `1+\rho`” at [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:80). This matches `A_L(X)\le A_L(H_X)\le(1+\rho)A_L(X)` at [deathtime_reduction.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/deathtime_reduction.tex:29) and `\rho=\Theta(\xi)` at [main_theorem.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/main_theorem.tex:20).

FINDINGS:

1. [MINOR] [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:59) — Equal-size tie wording is not source-exact. The paper says tie by `z`-order; source Algorithm 2 ties by current argument order because it swaps only under strict size inequality. Defect is presentational, not structural: the paper’s predicate defines a valid deterministic CK variant and makes the predecessor unique. Fix: replace “Algorithm 2 of DMOSW25” with “the following deterministic tie-broken CK variant of Algorithm 2” or define the ordered recursion before claiming exact membership.

2. [MINOR] [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:186) — “A call that does not abort returns the unbiased clipped death-time averages” is too strong if read conditionally. Conditioning on non-abort can bias the sample distribution. The proof only needs: the uncapped averages are unbiased, abort is counted as failure, and `P(abort or inaccurate)` is union-bounded. Fix that sentence to say non-abort returns the exact uncapped sample average, while aborts are handled as bad runs.

3. [MINOR] Certification: [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:113) — `lem:incident` now enumerates all incident edges and only genuine ones under the local WSPD variant. The proof says “Every incident edge of length `<= r` is found” and “only genuine edges are emitted,” with cost `O(\rho^{-2}\log^2\Delta)` and edge count `O(\rho^{-2}\log\Delta)`. No substantive fix.

4. [MINOR] Certification: [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:151) — Exact bottleneck Dijkstra and the `L` cutoff are correct. The text expands “all” incident edges up to `L`, returns `L` only when the queue empties, and argues the first root/lower-rank extraction is exact. No fix beyond Finding 2’s wording.

5. [MINOR] Certification: [app_assembly.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_assembly.tex:37) — `lem:kwindow` is consistent: it proves `h <= h_0 = Theta(\xi L)`, `K in [cK_0/4, C_\xi K_0]`, and total `Otil_\xi(n/K_0)=Otil(n^{1/3})` queries. Snapping then uses `delta_s=sqrt2 h=O(\xi L)`. No fix.

6. [MINOR] Certification: [app_assembly.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_assembly.tex:5) — Death-time identity, variance, and assembly are coherent. The proof derives `|V| E X_L=A_L(H)` and `Var <= |V| L wt(MST(H))/s`; assembly bounds the four errors by `O(\xi G)`. No fix.

No BLOCKER or MAJOR remains.