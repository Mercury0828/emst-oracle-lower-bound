"""
Deep dive on the BRIDGE worst-case (round-1 killer): two dense clusters + one Theta(W) edge.
Pro's claim: regularize to K=Theta(n^{2/3}) support cells, run Õ(sqrt K) estimator on Q.
Question: in Q, is w(MST(Q)) genuinely ~ W (so estimating w(MST(Q)) to (1+-eta) gives the
tail)?  AND does the support estimator (Czumaj) actually 'see' the single heavy bridge edge
without Omega(n) work?  We can't simulate the query algorithm, but we CAN check that:
   - w(MST(Q)) carries the heavy edge (so it is in the *target* W_Q, not lost),
   - the heavy edge is a single edge among K_h ~ n^{2/3} support edges => the SAME
     concentration obstruction from round-1 reappears for the support estimator IF it
     relied on uniform death-time sampling. Pro claims the Czumaj spatial estimator avoids
     this via active-block subdivision (spatial info). Check magnitude of the gap.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from emst import emst_weight
from scipy.spatial import Delaunay

def mst_edge_weights(points):
    pts = np.asarray(points, float); n = len(pts)
    if n <= 3:
        cand = [(i, j) for i in range(n) for j in range(i + 1, n)]
    else:
        tri = Delaunay(pts); E = set()
        for s in tri.simplices:
            for a in range(3):
                for b in range(a+1,3):
                    i,j=int(s[a]),int(s[b]); E.add((min(i,j),max(i,j)))
        cand = list(E)
    we = sorted((math.dist(pts[i], pts[j]), i, j) for (i, j) in cand)
    parent=list(range(n))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    w=[]
    for wt,i,j in we:
        ri,rj=find(i),find(j)
        if ri!=rj:
            parent[ri]=rj; w.append(wt)
            if len(w)==n-1: break
    return np.array(w)

def snap_centers(points,h):
    pts=np.asarray(points,float); idx=np.floor(pts/h).astype(np.int64)
    return (np.unique(idx,axis=0)+0.5)*h

def inst_bridge(n, gapfac=0.9):
    half=n//2; side=int(math.isqrt(half))
    g=np.array([(i,j) for i in range(side) for j in range(half//side+1)])[:half].astype(float)
    A=g.copy(); B=g.copy(); B[:,0]+=side+gapfac*n
    return np.vstack([A,B])

# many-bridges instance: k clusters in a line, each gap Theta(W/k). Tests whether the
# tail is many medium edges (regularizes well) vs one huge edge (concentration).
def inst_kbridge(n, k, gapfac=1.0):
    per=n//k; side=int(math.isqrt(per))
    blocks=[]
    x=0.0
    for c in range(k):
        g=np.array([(i,j) for i in range(side) for j in range(per//side+1)])[:per].astype(float)
        g[:,0]+=x; blocks.append(g)
        x += side + gapfac*(n/k)
    return np.vstack(blocks)

print("="*80)
print("BRIDGE: does snapped support Q keep w(MST(Q))~W and the heavy edge, at K~n^{2/3}?")
print("="*80)
for n in [1000,2000,4000,8000]:
    P=inst_bridge(n); W=emst_weight(P); K0=round(n**(2/3))
    # operative grid: smallest dyadic giving K_h>=K0 then check K_h<=4K0
    h=1.0
    while len(snap_centers(P,h))>2*K0: h*=1.5
    Q=snap_centers(P,h); wQ=mst_edge_weights(Q); Kh=len(Q)
    L=W/K0
    nlong=int(np.sum(wQ>L))
    print(f"  n={n:5d} W={W:9.1f} K0={K0:4d} h={h:7.2f} K_h={Kh:5d} W_Q={wQ.sum():9.1f}"
          f" W_Q/W={wQ.sum()/W:.3f} maxedge={wQ.max():8.1f} #edges>L={nlong}"
          f" frac_W_in_top1={wQ.max()/wQ.sum():.3f}")
print()
print("  -> If 'frac_W_in_top1' ~ 0.5, ONE support edge carries half of W_Q.")
print("     The support estimator MUST find that single edge among ~K_h spatial blocks.")
print("     Czumaj's active-block subdivision isolates it by GEOMETRY (the gap is a huge")
print("     empty region) -> O(sqrt K) blocks, not O(K). This is the load-bearing claim.")

print("\n"+"="*80)
print("K-BRIDGE: tail spread over k medium edges (regularizes cleanly)")
print("="*80)
for k in [2,8,32]:
    n=4000; P=inst_kbridge(n,k); W=emst_weight(P); K0=round(n**(2/3))
    h=1.0
    while len(snap_centers(P,h))>2*K0: h*=1.5
    Q=snap_centers(P,h); wQ=mst_edge_weights(Q); L=W/K0
    print(f"  k={k:3d} W={W:9.1f} K_h={len(Q):5d} W_Q={wQ.sum():9.1f} #edges>L={int(np.sum(wQ>L))}"
          f" top1frac={wQ.max()/wQ.sum():.3f}")
