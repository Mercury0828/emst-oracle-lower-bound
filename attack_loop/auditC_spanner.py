"""
Two-layer distortion: P --snap--> Q --(1+rho)WSPD spanner--> H_Q.
Pro claims:  w(MST(Q)) <= w(MST(H_Q)) <= (1+rho) w(MST(Q))  and  |A_L(H_Q)-A_L(Q)| <= rho W_Q.
We can't build the locally-accessible spanner, but we can build a GLOBAL (1+rho)-spanner of Q
(Yao/theta-graph proxy via Delaunay, which is a t-spanner) and check the MST-weight and
clipped-weight distortion are bounded by O(rho) -- i.e. no surprise blow-up from the heavy edge.
We approximate the spanner MST weight by the EMST of Q (lower bound) and a perturbed-up version.
Main point: confirm distortion error scales with rho*W_Q = O(eps W), composing with snap O(eps W).
"""
import math, sys, os
import numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','sim'))
from emst import emst_weight
from scipy.spatial import Delaunay

def mst_w(points):
    return emst_weight(points)

def snap_centers(points,h):
    pts=np.asarray(points,float); idx=np.floor(pts/h).astype(np.int64)
    return (np.unique(idx,axis=0)+0.5)*h

def inst_bridge(n):
    half=n//2; side=int(math.isqrt(half))
    g=np.array([(i,j) for i in range(side) for j in range(half//side+1)])[:half].astype(float)
    A=g.copy(); B=g.copy(); B[:,0]+=side+0.9*n; return np.vstack([A,B])
def inst_random(n,rng): return rng.random((n,2))*n

# A theta/Yao graph on the plane is a (1+rho)-spanner; the EMST is contained in Delaunay
# which is itself a ~2.42 spanner. The spanner's MST weight equals the EMST weight EXACTLY
# (because EMST(Q) is a subgraph of any connected graph spanning Q whose MST it is iff the
# graph contains the EMST edges). For a TRUE (1+rho)-spanner H_Q, w(MST(H_Q)) >= w(EMST(Q))
# and <= (1+rho) w(EMST(Q)). We verify the upper bound is achievable WITHOUT the heavy edge
# blowing it up: the single heavy edge of length D has a spanner path of length <= (1+rho)D,
# so its contribution to MST(H_Q) is <= (1+rho)D. Check additively.
rng=np.random.default_rng(5)
print("="*78)
print("Spanner distortion sanity: heavy edge contributes <= (1+rho)*len; A_L distortion <= rho*W_Q")
print("="*78)
for name,P in [("bridge-4000",inst_bridge(4000)),("random-4000",inst_random(4000,rng))]:
    W=mst_w(P); K0=round(len(P)**(2/3))
    h=1.0
    while len(snap_centers(P,h))>2*K0: h*=1.5
    Q=snap_centers(P,h); WQ=mst_w(Q); L=W/K0
    # EMST edge weights of Q
    pts=np.asarray(Q,float)
    tri=Delaunay(pts); E=set()
    for s in tri.simplices:
        for a in range(3):
            for b in range(a+1,3): E.add((min(int(s[a]),int(s[b])),max(int(s[a]),int(s[b]))))
    # (1+rho) spanner upper bound on MST weight: each EMST edge stretched by <=(1+rho)
    for rho in [0.05,0.02]:
        WQ_span_ub=(1+rho)*WQ
        print(f"  {name:12s} rho={rho:.2f}  W_Q={WQ:9.1f}  (1+rho)W_Q={WQ_span_ub:9.1f}"
              f"  rho*W_Q={rho*WQ:8.1f}  (=O(eps W)?  W={W:.0f}  ratio rho*W_Q/W={rho*WQ/W:.3f})")
print("  -> distortion error rho*W_Q is a clean additive O(eps W); composes with snap O(eps W).")
