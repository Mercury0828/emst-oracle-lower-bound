"""
Check the regularization step: dyadic halving of h gives K_{h/2} <= 4 K_h (so the first
crossing of K_0 lands in [c K_0, C K_0]).  Also: at the operative grid is K_h really
Theta(K_0) across diverse instances, and what is the achieved [c, C] band?
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from emst import emst_weight

def snap_count(points,h):
    pts=np.asarray(points,float); idx=np.floor(pts/h).astype(np.int64)
    return len(np.unique(idx,axis=0))

def inst_random(n,rng): return rng.random((n,2))*n
def inst_bridge(n):
    half=n//2; side=int(math.isqrt(half))
    g=np.array([(i,j) for i in range(side) for j in range(half//side+1)])[:half].astype(float)
    A=g.copy(); B=g.copy(); B[:,0]+=side+0.9*n; return np.vstack([A,B])
def inst_clustered(n,rng):
    # geometrically unequal occupancy: heavy power-law cluster sizes
    k=int(n**(2/3)); sizes=rng.zipf(1.6,k); sizes=np.minimum(sizes,n);
    sizes=(sizes/sizes.sum()*n).astype(int); sizes[sizes<1]=1
    centers=rng.random((k,2))*n; pts=[]
    for c,s in zip(centers,sizes): pts.append(c+rng.random((s,2))*0.5)
    return np.vstack(pts)

print("="*78)
print("Dyadic halving monotonicity:  K_{h/2} <= 4 K_h  (used for clean crossing)")
print("="*78)
rng=np.random.default_rng(3)
worst=0
for name,P in [("random",inst_random(4000,rng)),("bridge",inst_bridge(4000)),
               ("clustered",inst_clustered(4000,rng))]:
    h=float(P.max())
    seq=[]
    for _ in range(22):
        seq.append((h,snap_count(P,h))); h/=2
    ratios=[seq[i+1][1]/max(1,seq[i][1]) for i in range(len(seq)-1)]
    mr=max(ratios); worst=max(worst,mr)
    print(f"  {name:10s} max K_{{h/2}}/K_h over halvings = {mr:.2f}  (claim: <=4)")
print(f"  >>> worst halving ratio overall = {worst:.2f}  {'OK (<=4)' if worst<=4.0001 else 'VIOLATED'}")

print("\n"+"="*78)
print("Operative band: first dyadic crossing of K_0=n^{2/3}, report K_h/K_0")
print("="*78)
for name,maker in [("random",lambda n:inst_random(n,rng)),("bridge",inst_bridge),
                   ("clustered",lambda n:inst_clustered(n,rng))]:
    for n in [2000,4000,8000]:
        P=maker(n); K0=round(n**(2/3))
        h=float(P.max()); prev=None
        while True:
            K=snap_count(P,h)
            if K>=K0: break
            prev=(h,K); h/=2
            if h<1e-9: break
        print(f"  {name:10s} n={n:5d} K0={K0:4d}  crossing K_h={K:5d}  K_h/K0={K/K0:.2f}")
