"""
TASK 5 (sharpest cost probe): is N_j <= C*(1 + W_Q/(sigma r_j)) (eq 2/3) with a K-INDEPENDENT C?
eq(2): N_j <= 8 W_Q/a_j + 4 ; small scale a_j=h uses W_Q >= (K-1)h => N_j <= C(1+W_Q/(sigma r_j)).
Note a_j ~ sigma r_j /96, so 8 W_Q/a_j ~ 768 W_Q/(sigma r_j). So the CONSTANT C in eq(3) is ~768
(from the /96 choice) -- large but K-INDEPENDENT. The danger is if max_j N_j/(1+W_Q/(sigma r_j)) GROWS in K.

We measure max_j N_j/(1+W_Q/(sigma r_j)) as K grows for the worst families (strips, grid, uniform).
Flat => eq(3) holds with constant C (fine, folds into Õ). Growing => a real leak.

Also report the eq(2) form: max_j N_j*a_j/W_Q (should be <= 8, the packing constant, K-independent).
"""
import math, sys
import numpy as np
sys.path.insert(0,'sim')
from scipy.spatial import Delaunay

def mst_edges(pts):
    n=len(pts); pts=np.asarray(pts,float)
    if n<=1: return []
    if np.ptp(pts[:,1])<1e-9 or np.ptp(pts[:,0])<1e-9:
        coord=pts[:,0] if np.ptp(pts[:,1])<1e-9 else pts[:,1]
        return list(np.diff(np.sort(coord)))
    try: tri=Delaunay(pts)
    except Exception: tri=Delaunay(pts,qhull_options="QJ")
    E=set()
    for s in tri.simplices:
        for a in range(3):
            for b in range(a+1,3):
                i,j=int(s[a]),int(s[b]); E.add((min(i,j),max(i,j)))
    we=sorted((math.dist(pts[i],pts[j]),i,j) for (i,j) in E)
    par=list(range(n))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    out=[]; used=0
    for w,i,j in we:
        ri,rj=f(i),f(j)
        if ri!=rj:
            par[ri]=rj; out.append(w); used+=1
            if used==n-1: break
    return out

def probe(name,Q,h=1.0,sigma=0.25):
    Q=np.asarray(Q,float); K=len(Q)
    WQ=sum(mst_edges(Q))
    x0,y0=Q[:,0].min(),Q[:,1].min()
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    rs=[]; r=h
    while r<diam: rs.append(r); r*=(1+sigma)
    maxNU=0.0; max_eq2=0.0
    for r_j in rs:
        a=max(h,sigma*r_j/96.0)
        ci=np.floor((Q[:,0]-x0)/a).astype(np.int64)
        cj=np.floor((Q[:,1]-y0)/a).astype(np.int64)
        Nj=len(set(zip(ci.tolist(),cj.tolist())))
        denom=(1.0+WQ/(sigma*r_j))
        maxNU=max(maxNU, Nj/denom)
        max_eq2=max(max_eq2, Nj*a/max(WQ,1e-9))   # eq(2): N_j*a_j <= 8 W_Q  -> ratio <= 8
    return K, WQ, maxNU, max_eq2

if __name__=="__main__":
    rng=np.random.default_rng(51)
    def snap(pts,h): return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    print("max_j N_j/(1+W_Q/(sigma r_j))  and  max_j N_j*a_j/W_Q (eq2, want <=8) vs K:", flush=True)
    print("\nGRID family:", flush=True)
    for s in [40,80,160,260]:
        g=np.array([[i,j] for i in range(s) for j in range(s)],float)
        K,WQ,nu,e2=probe(f"grid{s}",g)
        print(f"  grid {s}x{s}: K={K:6d} maxN/U={nu:7.3f}  max N*a/W_Q(eq2)={e2:.3f}", flush=True)
    print("\nSTRIPS family (high occupancy at one scale):", flush=True)
    for (nrow,L) in [(40,200),(80,400),(140,700),(220,1100)]:
        strips=[np.column_stack([np.arange(L,dtype=float),np.full(L,k*3.0)]) for k in range(nrow)]
        Q=snap(np.vstack(strips),1.0)
        K,WQ,nu,e2=probe(f"strips{nrow}x{L}",Q)
        print(f"  strips {nrow}x{L}: K={K:6d} maxN/U={nu:7.3f}  max N*a/W_Q(eq2)={e2:.3f}", flush=True)
    print("\nUNIFORM family:", flush=True)
    for (npt,sc) in [(2000,45),(8000,90),(20000,140),(50000,220)]:
        Q=snap(rng.random((npt,2))*sc,1.0)
        K,WQ,nu,e2=probe(f"u{npt}",Q)
        print(f"  uniform K={K:6d}: maxN/U={nu:7.3f}  max N*a/W_Q(eq2)={e2:.3f}", flush=True)
    print("DONE",flush=True)
