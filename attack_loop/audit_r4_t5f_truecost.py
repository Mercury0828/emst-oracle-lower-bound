"""
CRITICAL: recompute the eq(8) per-scale cost using the TRUE occupied-cell count N_j (and TRUE c_j)
instead of the bound U_j = C(1+W_Q/(sigma r_j)).  The leader-estimator variance is Var(Z)<=M_j*c_j
(c_j = #components at scale r_j), NOT M_j*N_j.  So the correct sample count is k_j = M_j*c_j/alpha_j^2.
Pro bounds c_j<=N_j<=U_j; if the true c_j is small even where N_j~sqrt(K), the cost is fine.

So the REAL question: at the floor scales where N_j ~ sqrt(K)*(W_Q/(sigma r_j)), what is c_j (the
component count that actually drives the variance)?  If c_j ~ W_Q/(sigma r_j) (i.e. c_j << N_j there),
the cost uses c_j and stays Õ(sqrt K). If c_j ~ N_j ~ sqrt(K)*(...), cost blows up.

Compute, per scale: M_j, N_j, c_j (exact), alpha_j; k_j^{N}=M_j N_j/alpha^2 ; k_j^{c}=M_j c_j/alpha^2.
Sum each over scales; compare totals/(sqrt(K) T^2 / eta) for growing K.  The estimator needs the
c_j version (that's the actual variance). Report both; the c_j total is what matters.
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

def active_cover(Q,h):
    K=len(Q); q=math.ceil(math.sqrt(K))
    x0,y0=Q[:,0].min(),Q[:,1].min()
    span=max(Q[:,0].max()-x0,Q[:,1].max()-y0)
    side=h
    while side<span: side*=2
    delta=side
    while True:
        ci=np.floor((Q[:,0]-x0)/delta).astype(np.int64)
        cj=np.floor((Q[:,1]-y0)/delta).astype(np.int64)
        nb=len(set(zip(ci.tolist(),cj.tolist())))
        if nb>=q or delta<=h: return nb,delta,q
        delta/=2

def probe(name,Q,h=1.0,sigma=0.25,eta=0.25):
    Q=np.asarray(Q,float); K=len(Q)
    edges=sorted(mst_edges(Q)); WQ=sum(edges); G=WQ
    b,delta,q=active_cover(Q,h)
    x0,y0=Q[:,0].min(),Q[:,1].min()
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    r0=max(h,eta*G/K)
    rs=[]; r=r0
    while r<diam: rs.append(r); r*=(1+sigma)
    T=len(rs)
    edges_arr=np.array(edges)
    totN=0.0; totc=0.0
    for r_j in rs:
        a=max(h,sigma*r_j/96.0)
        if a>=delta:
            totN+=b; totc+=b; continue
        ci=np.floor((Q[:,0]-x0)/a).astype(np.int64)
        cj=np.floor((Q[:,1]-y0)/a).astype(np.int64)
        Nj=len(set(zip(ci.tolist(),cj.tolist())))
        cj_exact=1+int(np.sum(edges_arr>r_j))   # exact component count of Q at threshold r_j
        Mj=b*(delta/a)**2
        alpha=eta*G/(T*sigma*r_j)
        totN += Mj*Nj/alpha**2
        totc += Mj*cj_exact/alpha**2
    sk=math.sqrt(K); norm=sk*T*T/eta
    print(f"  {name}: K={K:6d} sqrtK={sk:6.1f} T={T} | "
          f"cost[useN]/norm={totN/norm:10.1f}  cost[use c_j]/norm={totc/norm:8.3f}", flush=True)
    return K, totN/norm, totc/norm

if __name__=="__main__":
    rng=np.random.default_rng(71)
    def snap(pts,h): return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    print("Compare cost using N_j (Pro's U_j bound) vs the TRUE variance driver c_j:", flush=True)
    print("If cost[use c_j]/norm is FLAT in K => genuine Õ(sqrt K). cost[useN] is a loose over-count.", flush=True)
    print("\nGRID:", flush=True)
    rows=[]
    for s in [40,80,160,240]:
        g=np.array([[i,j] for i in range(s) for j in range(s)],float)
        rows.append(probe(f"grid{s}",g))
    print("\nUNIFORM:", flush=True)
    for (npt,sc) in [(2000,45),(8000,90),(20000,140),(50000,220)]:
        rows.append(probe(f"uniform~{npt}", snap(rng.random((npt,2))*sc,1.0)))
    print("\nSATELLITE:", flush=True)
    def sat(s):
        K=s*s; h=float(s); D=float(s*s); nA=K-s; side=int(math.isqrt(nA)); nA=side*side
        gx,gy=np.meshgrid(np.arange(side),np.arange(side))
        A=np.column_stack([gx.ravel(),gy.ravel()]).astype(float)*h
        x0=A[:,0].max()+D; sa=np.array([[x0+j*D,0.0] for j in range(K-nA)])
        return np.vstack([A,sa]),h
    for s in [32,48,64,96]:
        Q,hh=sat(s); rows.append(probe(f"sat{s}",Q,h=hh))
    print("\nFLATNESS of cost[use c_j]/norm (the real cost):", flush=True)
    cvals=[r[2] for r in rows];
    print(f"  min={min(cvals):.3f} max={max(cvals):.3f}", flush=True)
    print("DONE",flush=True)
