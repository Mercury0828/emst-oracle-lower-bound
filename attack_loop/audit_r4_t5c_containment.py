"""
TASK 5 (containment): the load-bearing M_j claim (§5): for scale a_j <= delta, EVERY nonempty
a_j-cell lies inside the union of the b active delta-blocks. (Then M_j = b*(delta/a_j)^2.)
This is automatic IF the active blocks are the nonempty delta-cells (every point is in some nonempty
delta-cell = an active block). VERIFY directly. Also verify N_j <= b*(delta/a_j)^2 and the
packing-driven N_j <= C(1+W_Q/(sigma r_j)) (eq 2/3).

Then a SHARPER attack: make the support so that at some scale the #occupied a_j-cells N_j is LARGE
relative to U_j = C(1+G/(sigma r_j)), which would break eq(3) U_j>=N_j and inflate the variance.
We search for max_j N_j / (1 + W_Q/(sigma r_j)).
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
        blocks=set(zip(ci.tolist(),cj.tolist()))
        nb=len(blocks)
        if nb>=q or delta<=h: return nb,delta,q,blocks,(x0,y0)
        delta/=2

def check(name,Q,h=1.0,sigma=0.25):
    Q=np.asarray(Q,float); K=len(Q)
    edges=mst_edges(Q); WQ=sum(edges)
    b,delta,q,blocks,(x0,y0)=active_cover(Q,h)
    # containment + N_j vs U_j over fine scales
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    rs=[]; r=max(h,sigma);
    r=h
    while r<diam: rs.append(r); r*=(1+sigma)
    maxNU=0.0; contain_ok=True; maxMratio=0.0
    for r_j in rs:
        a=max(h,sigma*r_j/96.0)
        if a>delta: continue
        ci=np.floor((Q[:,0]-x0)/a).astype(np.int64)
        cj=np.floor((Q[:,1]-y0)/a).astype(np.int64)
        acells=set(zip(ci.tolist(),cj.tolist()))
        Nj=len(acells)
        # containment: every a-cell's delta-parent must be an active block
        for (gx,gy) in acells:
            par=(int(gx*a//delta), int(gy*a//delta))
            if par not in blocks:
                contain_ok=False; break
        Uj=(1.0+WQ/(sigma*r_j))
        maxNU=max(maxNU, Nj/Uj)
        Mj_formula=b*(delta/a)**2
        maxMratio=max(maxMratio, Nj/Mj_formula)
    print(f"  {name}: K={K} b={b} delta={delta:.1f} | containment_OK={contain_ok} | "
          f"max N_j/U_j={maxNU:.3f} (want <=O(1)) | max N_j/M_j_formula={maxMratio:.4f} (<=1)", flush=True)

if __name__=="__main__":
    rng=np.random.default_rng(41)
    def snap(pts,h): return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    # diverse instances
    check("uniform", snap(rng.random((5000,2))*70,1.0))
    g=np.array([[i,j] for i in range(100) for j in range(100)],float); check("grid100",g)
    def sat(s):
        K=s*s; h=float(s); D=float(s*s); nA=K-s; side=int(math.isqrt(nA)); nA=side*side
        gx,gy=np.meshgrid(np.arange(side),np.arange(side))
        A=np.column_stack([gx.ravel(),gy.ravel()]).astype(float)*h
        x0=A[:,0].max()+D; sa=np.array([[x0+j*D,0.0] for j in range(K-nA)])
        return np.vstack([A,sa]),h
    Q,hh=sat(48); check("satellite48",Q,h=hh)
    # adversarial: dense thin strips (high occupancy at some scale)
    strips=[]
    for k in range(40):
        strips.append(np.column_stack([np.arange(200,dtype=float), np.full(200,k*3.0)]))
    check("strips", snap(np.vstack(strips),1.0))
    # adversarial: one super-dense delta-block + sparse rest (occupancy skew)
    dense=snap(rng.random((4000,2))*8,1.0)
    sparse=snap(rng.random((400,2))*400,1.0)+np.array([200,0.0])
    check("skew-density", np.vstack([dense,sparse]))
    print("DONE",flush=True)
