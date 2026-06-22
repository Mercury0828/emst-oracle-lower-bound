"""
Verify the bound that ACTUALLY saves the cost: c_j <= C*(1 + W_Q/(sigma r_j)) with K-INDEPENDENT C.
This is the standard c(t)-1 <= W_Q/t identity (#MST edges > t <= W_Q/t). Here t=r_j, and the
estimator's accuracy target is set at scale d_j=sigma r_j, so the relevant ratio is c_j/(1+W_Q/(sigma r_j)).
If this is O(1) (flat in K), then using c_j (not N_j) the variance M_j c_j is bounded and eq(8) holds.
Report max_j c_j/(1+W_Q/(sigma r_j)) and max_j (c_j-1)/(W_Q/r_j) (should be <=1 exactly).
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
    edges=np.array(sorted(mst_edges(Q))); WQ=float(edges.sum())
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    rs=[]; r=h
    while r<diam: rs.append(r); r*=(1+sigma)
    maxcU=0.0; max_identity=0.0
    for r_j in rs:
        cj=1+int(np.sum(edges>r_j))
        maxcU=max(maxcU, cj/(1.0+WQ/(sigma*r_j)))
        max_identity=max(max_identity,(cj-1)*r_j/max(WQ,1e-9))  # (c-1) <= W_Q/r_j  => ratio<=1
    print(f"  {name}: K={K:6d} sqrtK={math.sqrt(K):6.1f} | max c_j/(1+W_Q/(sigma r_j))={maxcU:.3f} "
          f"(={maxcU/math.sqrt(K):.4f}*sqrtK)  | identity max (c-1)r/W_Q={max_identity:.3f}(<=1)", flush=True)

if __name__=="__main__":
    rng=np.random.default_rng(81)
    def snap(pts,h): return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    for s in [40,80,160,240]:
        g=np.array([[i,j] for i in range(s) for j in range(s)],float); probe(f"grid{s}",g)
    for (npt,sc) in [(2000,45),(8000,90),(20000,140),(50000,220)]:
        probe(f"uniform~{npt}", snap(rng.random((npt,2))*sc,1.0))
    def sat(s):
        K=s*s; h=float(s); D=float(s*s); nA=K-s; side=int(math.isqrt(nA)); nA=side*side
        gx,gy=np.meshgrid(np.arange(side),np.arange(side))
        A=np.column_stack([gx.ravel(),gy.ravel()]).astype(float)*h
        x0=A[:,0].max()+D; sa=np.array([[x0+j*D,0.0] for j in range(K-nA)])
        return np.vstack([A,sa]),h
    for s in [32,64,96]:
        Q,hh=sat(s); probe(f"sat{s}",Q,h=hh)
    print("DONE",flush=True)
