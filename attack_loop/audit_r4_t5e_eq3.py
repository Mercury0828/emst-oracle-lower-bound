"""
Pin down eq(3): is there a K-INDEPENDENT C with N_j <= C*(1 + W_Q/(sigma r_j)) for ALL scales j,
INCLUDING the small-scale floor a_j=h?  Measure C_needed = max_j N_j/(1+W_Q/(sigma r_j)) and decompose
by whether the scale is in the a_j=h floor regime or the a_j=sigma r_j/96 regime.

KEY: the cost eq(8) uses M_j*U_j/alpha_j^2 with U_j>=N_j. If U_j must be ~sqrt(K)*(W_Q/(sigma r_j))
at some scale, the cost at THAT scale inflates by sqrt(K) -> would break Õ(sqrt K).
BUT note: M_j = b*(delta/a_j)^2 and the eq(8) algebra REPLACES U_j by C(1+G/(sigma r_j)) -- if the TRUE
N_j needs a sqrt(K) larger U_j only in the a_j=h regime, we must check the a_j=h regime cost separately
(Pro's §8 'r_0=h case' and the coarse-scale O(bT) handling).

Decompose max N_j/U_j by regime and report which scale achieves the max.
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
    Q=np.asarray(Q,float); K=len(Q); WQ=sum(mst_edges(Q))
    x0,y0=Q[:,0].min(),Q[:,1].min()
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    # r0 = max(h, eta*G/K) with G=WQ, eta=sigma
    r0=max(h,sigma*WQ/K)
    rs=[]; r=r0
    while r<diam: rs.append(r); r*=(1+sigma)
    best=(0.0,None,None,None,None)
    for r_j in rs:
        a=max(h,sigma*r_j/96.0)
        floor = a<=h+1e-12 and sigma*r_j/96.0 < h
        ci=np.floor((Q[:,0]-x0)/a).astype(np.int64)
        cj=np.floor((Q[:,1]-y0)/a).astype(np.int64)
        Nj=len(set(zip(ci.tolist(),cj.tolist())))
        U=(1.0+WQ/(sigma*r_j))
        ratio=Nj/U
        if ratio>best[0]:
            best=(ratio,r_j,a,floor,Nj)
    ratio,r_j,a,floor,Nj=best
    print(f"  {name}: K={K} sqrtK={math.sqrt(K):.1f} r0={r0:.2f} | "
          f"max N/U={ratio:.2f} (={ratio/math.sqrt(K):.3f}*sqrtK) at r={r_j:.2f} a={a:.2f} "
          f"floor(a=h)={floor} N_j={Nj}", flush=True)
    return K, ratio

if __name__=="__main__":
    rng=np.random.default_rng(61)
    def snap(pts,h): return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    print("Where does max N/U occur, and is it in the a=h floor regime?", flush=True)
    for s in [40,80,160,260]:
        g=np.array([[i,j] for i in range(s) for j in range(s)],float)
        probe(f"grid{s}",g)
    for (npt,sc) in [(2000,45),(8000,90),(20000,140),(50000,220)]:
        probe(f"uniform K~{npt}", snap(rng.random((npt,2))*sc,1.0))
    print("DONE",flush=True)
