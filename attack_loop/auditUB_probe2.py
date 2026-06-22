"""
Audit UB probe 2: directly compute the CRT sum Sum_i lambda_i c_i via component
counts at dyadic scales, and the point-estimator variance.

A component at scale r = #connected comps of the graph keeping edges <= r.
We compute c(r) over a geometric grid of scales and the CRT integral
Sum_i (1+eps)^i c_i ~ integral c(r) dr (the (n-Delta)+Sum lambda c identity, up to (1+-eps)).
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from emst import emst_weight
from scipy.spatial import cKDTree

rng = np.random.default_rng(7)

def comp_count_at_scale(P, r):
    """#connected components keeping edges of length <= r. Union-find over pairs within r."""
    tree = cKDTree(P)
    pairs = tree.query_pairs(r, output_type='ndarray')
    n = len(P)
    parent = np.arange(n)
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for i,j in pairs:
        ri,rj=find(i),find(j)
        if ri!=rj: parent[ri]=rj
    return len(set(find(i) for i in range(n)))

def crt_sum(P, eps=0.3, rmax=None):
    """Sum_i lambda_i c_i, lambda_i=(1+eps)^i, i=0..s with lambda_s ~ rmax.
       This equals Sum over edges-as-components band; we approximate the integral
       int c(r) d(log r)/... Actually CRT: w ~ (n-Delta)+sum_i lambda_i c_i where
       c_i counts comps at scale lambda_i. We just compute that sum for diagnosis."""
    if rmax is None:
        rmax = np.ptp(P,axis=0).max()
    s = int(np.ceil(np.log(2*rmax)/np.log(1+eps)))
    total=0.0
    contrib=[]
    for i in range(s+1):
        lam=(1+eps)**i
        c=comp_count_at_scale(P,lam)
        # the CRT weighting: each scale-band contributes (lambda_{i}-lambda_{i-1})*c_i
        # approx; codex uses lambda_i*c_i with the understanding lambda spans a (1+eps) band.
        # band width ~ eps*lambda_i.
        total += eps*lam*c
        contrib.append((lam,c,eps*lam*c))
        if c==1: break
    return total, contrib

print("="*78)
print("PART 1 (CRT): island contribution to Sum lambda_i c_i, and MST cross-check")
print("="*78)
for n in (256, 1024, 4096):
    M = int(round(np.sqrt(n)))
    L = np.sqrt(n)
    islands = np.column_stack([np.arange(M)*L, np.zeros(M)])  # spaced L on a line
    nb = n - M
    bulk = rng.random((nb,2))*1.0 + np.array([0.0, -5*L])  # bulk far below, tight
    P = np.vstack([islands, bulk])
    w = emst_weight(P)
    tot, contrib = crt_sum(P, eps=0.3)
    # island band: islands are singletons until scale ~ L. They contribute, per island,
    # roughly integral_1^L dr = L  -> M*L = n... but they connect as a PATH so once
    # scale>=L they merge. Count: at scale r<L, #island-comps = M. So band [1,L] each
    # scale has c >= M, contributing eps*lam*M summed over lam in [1,L] ~ M*L = n.
    print(f"n={n:5d} M={M:3d} L={L:6.1f}  MST={w:10.1f}  CRTsum={tot:10.1f}  MST/CRT={w/tot:.3f}")
    # show the scale profile near the island band
    for lam,c,band in contrib:
        if lam<=2*L:
            tag = " <-- island band" if c>=M else ""
            #print(f"    lam={lam:8.2f} c={c:5d} band={band:9.1f}{tag}")

print()
print("="*78)
print("PART 1 (variance): point estimator X(p)=n*sum_i lambda_i/|comp_i(p)|")
print("="*78)
# Build X(p) for each point on a fixed island+bulk instance, compute Var/E^2.
def point_estimator_values(P, eps=0.3):
    n=len(P)
    rmax=np.ptp(P,axis=0).max()
    s=int(np.ceil(np.log(2*rmax)/np.log(1+eps)))
    # For each scale, get component label and size; accumulate per-point sum lambda*(band)/size
    Xacc=np.zeros(n)
    tree=cKDTree(P)
    for i in range(s+1):
        lam=(1+eps)**i
        pairs=tree.query_pairs(lam,output_type='ndarray')
        parent=np.arange(n)
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        for a,b in pairs:
            ra,rb=find(a),find(b)
            if ra!=rb: parent[ra]=rb
        labels=np.array([find(x) for x in range(n)])
        _,inv,counts=np.unique(labels,return_inverse=True,return_counts=True)
        size=counts[inv]
        Xacc += eps*lam/size
        if len(counts)==1: break
    return n*Xacc

for n in (256, 1024, 4096):
    M=int(round(np.sqrt(n))); L=np.sqrt(n)
    islands=np.column_stack([np.arange(M)*L, np.zeros(M)])
    nb=n-M; bulk=rng.random((nb,2))*1.0+np.array([0.0,-5*L])
    P=np.vstack([islands,bulk])
    X=point_estimator_values(P)
    E=X.mean(); V=X.var()
    print(f"n={n:5d} M={M:3d}  E[X]={E:11.1f}  Var/E^2={V/E**2:8.3f}  (claim ~ sqrt(n)={np.sqrt(n):6.1f})"
          f"  q=Var/E^2/eps^2~{V/E**2/0.09:8.1f}")
