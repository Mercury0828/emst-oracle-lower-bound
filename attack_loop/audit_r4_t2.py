"""
TASK 2: Riemann-sum reconstruction (round-4 §7).
W_Q = int_0^inf (c(t)-1) dt.  Geometric thresholds r_{j+1}=(1+sigma) r_j, d_j=sigma*r_j.
Lower/upper Riemann sums sandwich the tail; claimed gap = sum_j d_j (c(r_j)-c(r_{j+1})) <= sigma*W_Q
because each MST edge length ell in (r_j, r_{j+1}] contributes d_j = sigma*r_j <= sigma*ell.

We compute the EXACT W_Q (= sum of MST edge lengths) and:
  - the lower Riemann sum  L = (K-1)*r_0 + sum_j d_j (c(r_{j+1}) - 1)    [under tail]
  - the upper Riemann sum  U = (K-1)*r_0 + sum_j d_j (c(r_j) - 1)        [over tail]
  - check  U - L  (the Riemann gap)  <=  sigma * W_Q   exactly.
Also check the §7 reconstruction What = (K-1)h + sum_j d_j (c(r_j)-1) tracks W_Q to within O(sigma) W_Q
when r_0=h (so the [h,r_0] term vanishes).
"""
import math, sys
import numpy as np
sys.path.insert(0,'sim')
from scipy.spatial import Delaunay

def mst_edges(pts):
    n=len(pts)
    if n<=1: return []
    tri=Delaunay(pts); E=set()
    for s in tri.simplices:
        for a in range(3):
            for b in range(a+1,3):
                i,j=int(s[a]),int(s[b]); E.add((min(i,j),max(i,j)))
    we=sorted((math.dist(pts[i],pts[j]),i,j) for (i,j) in E)
    par=list(range(n));
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

def comp_count_from_edges(edges,K,t):
    return 1 + sum(1 for w in edges if w>t)

def run(name,Q,h=1.0,sigma=0.25):
    Q=np.asarray(Q,float); K=len(Q)
    edges=mst_edges(Q); WQ=sum(edges)
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    # thresholds from r0=h
    rs=[]; r=h
    while r<diam*1.5: rs.append(r); r*=(1+sigma)
    # lower/upper Riemann of the tail int_{r0}^inf (c-1)
    Llow=0.0; Uup=0.0; What=(K-1)*h
    gap_formula=0.0
    for idx in range(len(rs)):
        r_j=rs[idx]; d_j=sigma*r_j
        r_next=rs[idx+1] if idx+1<len(rs) else r_j*(1+sigma)
        c_rj=comp_count_from_edges(edges,K,r_j)
        c_rn=comp_count_from_edges(edges,K,r_next)
        Uup += d_j*(c_rj-1)
        Llow+= d_j*(c_rn-1)
        What+= d_j*(c_rj-1)
        gap_formula += d_j*(c_rj-c_rn)
    riemann_gap = Uup-Llow
    # exact tail integral int_{h}^inf (c-1) dt = sum over edges of max(0, ell - h)
    tail_exact = sum(max(0.0, e-h) for e in edges)
    print(f"  {name}: K={K} W_Q={WQ:.1f}", flush=True)
    print(f"    tail_exact(int_h^inf)={tail_exact:.1f}  upperRiemann={Uup:.1f}  lowerRiemann={Llow:.1f}", flush=True)
    print(f"    Riemann gap (U-L)={riemann_gap:.1f}   sigma*W_Q={sigma*WQ:.1f}   gap<=sigma*WQ? {riemann_gap<=sigma*WQ+1e-6}", flush=True)
    print(f"    gap_formula sum d_j(c(r_j)-c(r_{{j+1}}))={gap_formula:.1f}  (== U-L? {abs(gap_formula-riemann_gap)<1e-6})", flush=True)
    print(f"    What=(K-1)h+sum d_j(c_j-1) = {What:.1f}   What/W_Q={What/WQ:.4f}", flush=True)

if __name__=="__main__":
    rng=np.random.default_rng(9)
    def snap(pts,h):
        return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    run("uniform-Q", snap(rng.random((2000,2))*80,1.0))
    def sat(s):
        K=s*s; h=float(s); D=float(s*s)
        nA=K-s; side=int(math.isqrt(nA)); nA=side*side
        gx,gy=np.meshgrid(np.arange(side),np.arange(side))
        A=np.column_stack([gx.ravel(),gy.ravel()]).astype(float)*h
        x0=A[:,0].max()+D
        sa=np.array([[x0+j*D,0.0] for j in range(K-nA)])
        return np.vstack([A,sa]),h
    Q,hh=sat(32); run("satellite-32",Q,h=hh)
    Q,hh=sat(48); run("satellite-48",Q,h=hh)
    # power-law edge lengths via hierarchical clusters
    pts=[]
    for lvl,(cnt,sp) in enumerate([(200,1.0),(20,30.0),(4,900.0)]):
        base=rng.random((cnt,2))*sp*5
        pts.append(base)
    run("hierarchical", snap(np.vstack(pts),1.0))
    print("DONE",flush=True)
