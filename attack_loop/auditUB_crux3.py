"""
CRUX v3: Is the 2D-concealed island instance a valid LOWER-BOUND PAIR for EMST?
A lower bound needs instances P_yes, P_no with:
  (i)  w(P_yes) and w(P_no) differ by a constant factor (so a (1+-eps) estimator must distinguish),
  (ii) indistinguishable by any o(sqrt n) range-counting queries.

Codex's islands give a candidate. BUT for a LOWER BOUND the 'no' instance must look identical
under coarse counts. The Driemel Lemma-32 LB already does exactly this at the n^{1/3} level
(16 n^{1/3} cells, hide ONE heavy gadget). The question: can hiding sqrt(n) islands push the
LB to sqrt(n)?

Key obstruction to that (we test): for a (1+-eps)-RELATIVE estimator, the hidden feature must
change w(P) by a constant FRACTION while being individually small. With M hidden islands each
contributing persistence ~ its NN distance d, total = M*d. For this to be a constant fraction
of OPT, and for each to be individually hidden (measure 1/sqrt n each so a query misses it),
we need M features. But a SINGLE coarse count over a big rectangle SUMS their effect:
  the M islands, even if individually low-measure, COLLECTIVELY occupy measure M/sqrt(n)*...
  Let's measure: can a coarse O(polylog) set of big-rectangle counts SEE the aggregate
  island mass (M points) vs no-island (those M points relocated into bulk)?

If YES -> aggregate coarse counting reveals the island CONTRIBUTION cheaply -> no sqrt n LB
          (consistent with LB-P1/P2: correlated Theta(w) gaps are coarsely estimable).
If NO  -> genuine sqrt n LB candidate (would CONTRADICT U-P1 spirit; suspicious).

Test: P_yes = M scattered islands + bulk(n-M). P_no = bulk(n) only (islands' M points moved
into the bulk corner). Compare (a) EMST weights, (b) whether a coarse grid of range counts
(say a fixed K x K grid of cell-counts, K=polylog) distinguishes them.
"""
import numpy as np
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","sim"))
from emst import emst_weight
rng=np.random.default_rng(3)

def coarse_grid_counts(P, Delta, K):
    """K x K grid of exact cell counts -- a polylog-sized coarse range-count summary."""
    ix=np.clip((P[:,0]/Delta*K).astype(int),0,K-1)
    iy=np.clip((P[:,1]/Delta*K).astype(int),0,K-1)
    H=np.zeros((K,K),dtype=int)
    np.add.at(H,(ix,iy),1)
    return H

print("="*78)
print("CRUX v3: is the 2D concealed-island instance coarsely distinguishable from no-island?")
print("="*78)
for n in (1024, 4096, 16384):
    M=int(round(np.sqrt(n))); L=np.sqrt(n); Delta=float(n)
    # P_yes: M scattered islands (empty-L neighborhoods) + dense bulk in corner
    iposs=[]; att=0
    while len(iposs)<M and att<200000:
        att+=1; p=rng.uniform(0,Delta,2)
        if all(np.hypot(*(p-q))>2.5*L for q in iposs): iposs.append(p)
    iposs=np.array(iposs); nb=n-M
    bulk=np.column_stack([rng.random(nb)*1.0,rng.random(nb)*1.0])
    P_yes=np.vstack([iposs,bulk])
    # P_no: same bulk + M extra points ALSO in the corner bulk (islands dissolved)
    extra=np.column_stack([rng.random(M)*1.0,rng.random(M)*1.0])
    P_no=np.vstack([extra,bulk])
    w_yes=emst_weight(P_yes); w_no=emst_weight(P_no)
    # coarse grid distinguishability: do the histograms differ in a way a few counts see?
    K=max(4,int(round(np.log2(n))))  # polylog grid
    Hy=coarse_grid_counts(P_yes,Delta,K); Hn=coarse_grid_counts(P_no,Delta,K)
    ncells_diff=int(np.count_nonzero(Hy!=Hn))
    yes_nonempty=int(np.count_nonzero(Hy)); no_nonempty=int(np.count_nonzero(Hn))
    print(f" n={n:6d} M={M:4d}  w_yes={w_yes:11.0f}  w_no={w_no:9.0f}  ratio={w_yes/w_no:6.2f}"
          f" | {K}x{K} grid: #nonempty yes={yes_nonempty} no={no_nonempty}"
          f"  (coarse grid SEES islands as scattered nonempty cells)")
