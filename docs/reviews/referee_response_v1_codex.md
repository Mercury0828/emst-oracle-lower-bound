VERDICT: BLOCKER-REMAINS

1(a) STILL-BROKEN. The new text correctly avoids equality, but the containment proof is not complete: “The standard recursion outputs a pair $(c,c')$ only after descending strictly past its predecessor $(c,p(c'))$...” This is not justified for equal-size/tie cases or for outputs whose last recursion step split the other cell. The proof must define the recursion orientation/tie rule to match this predecessor, or change the predicate to accept the actual split-side predecessor.

1(b) FIXED conditional on 1(a). The graph argument is correct: “Since $\mathcal W\subseteq\widehat{\mathcal W}$ we have $S_{\mathcal W}\subseteq S$, and a supergraph of a $(1+\rho)$-spanner is a $(1+\rho)$-spanner...” Also: “a supergraph has a no-heavier MST.”

1(c) FIXED. The inequalities survive the larger edge set: “every $S$-edge is a true $X$-pair...” and “if $\|x-y\|\le t/(1+\rho)$ then the spanner path... has every edge... $\le t$.”

1(d) PARTIAL. The intended direct partner-count proof is present: “since $(c,p(c'))$ is not well separated... $d(c,c')=O(s/\rho)$.” But it is written only for the orientation where fixed $c$ is the smaller cell: “Any ... partner $c'$ has $r(c')\in[s,2s]”; incident enumeration later uses the correct symmetric range “[s/2,2s].” Tighten the partner-count paragraph.

1(e) FIXED/PARTIAL. The oracle does enumerate local-family edges and checks genuineness: “testing them in both orientations” and “only genuine edges are emitted.” No operative proof assumes $\widehat{\mathcal W}=\mathcal W$. Minor wording remains in the overview/at-glance (“one edge per well-separated pair”) but the formal section uses $\widehat{\mathcal W}$.

2. PARTIAL. Inverse-binomial concentration is the right fix: “needs no a-priori knowledge of $K$” and “an $\Otil(n/K)$ query bound that holds with high probability.” But the abort line uses an underspecified lower bound: “$K_{\min}\ge1$ of interest”; if $K_{\min}=1$, the deterministic budget is $O(n)$, not $O(n/K)$. Also the exact-small-$K$ branch is asserted via a cover that normally needs $K$: “the cover construction has already found all support cells explicitly.”

3. FIXED. The order is now rank-independent: leader exploration uses “a fixed order independent of the ranks,” and Dijkstra tie-breaking is “by vertex identity, independent of ranks.” The harmonic probability is correct as $1/(j-1)$, though the WSPD prose should say “$v$ is minimum among the first $j-1$ vertices” rather than “smaller rank than all of them.”

4. FIXED. The independence claim is gone in the main assembly: “does not need the three errors to be independent... apply a union bound... no independence is assumed.” Overview matches: “combined by a union bound.”

5. FIXED. The $\xi$-dependence is now tracked: “$K$ may be as large as... $\Theta(K_0/\xi)$,” variance “$O(\xi^{-1}G^2/s_Q)$,” hence “$s_Q=O(\xi^{-3})$.” Appendix repeats: “raises $s_Q$ from $O(\xi^{-2})$ to $O(\xi^{-3})$.”

6. PARTIAL. Most minors are fixed: tail transfer is consistently “$4\delta_s/L$”; degenerate scales are handled; model agreement is explicit. Remaining minor issue: support guess removal writes exact “$U_Q=\sqrt2(K-1)\Delta$” while later only “$\widehat K=(1\pm\kappa)K$” is available; if $\widehat K<K$, this may not be a valid upper bound unless inflated.

FINDINGS:

1. [BLOCKER] [app_wspd.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_wspd.tex:91) — The proof of $\mathcal W\subseteq\widehat{\mathcal W}$ assumes the recursion reached every output pair by descending from $(c,p(c'))$. That is not established for all CK recursion outputs, especially equal-size/tie cases. Concrete fix: define the standard recursion with an orientation/tie rule that always splits the eventual second/larger cell used by the predicate, or change the predicate to accept “at least one relevant predecessor is not well-separated” and redo the partner bound symmetrically.

2. [MAJOR] [support_mst.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/support_mst.tex:48) — The K-estimation abort budget is written in terms of $K_{\min}$, not $K$; this avoids circularity but does not by itself give the claimed deterministic $O(n/K)$ budget unless $K_{\min}=\Theta(K)$. Concrete fix: state the lemma as high-probability query complexity, or add a doubling/pilot scheme that sets a safe cap within a constant factor of $n/K$.

3. [MINOR] [app_lemma3.tex](E:/Project-git/emst-oracle-lower-bound/paper/sections/app_lemma3.tex:217) — Guess removal uses exact $K$ in $U_Q=\sqrt2(K-1)\Delta$, then later swaps in $\widehat K$. Concrete fix: use a high-confidence upper bound, e.g. $\sqrt2(\widehat K/(1-\kappa)-1)\Delta$, or inflate by a fixed $(1+O(\kappa))$ factor.