"""
TASK 1: a>h regime, FORCED. Build Q with very large spread so sigma*r/64 >> h at large r.
For each r, pick dyadic a in [sigma*r/128, sigma*r/64], adjacency = min Euclidean cell dist <= r.
Test:  c(r + 2 sqrt2 a) <= c~(r) <= c(r).   (pure geometric lemma, both directions)
"""
import math, sys
import numpy as np
sys.path.insert(0,'sim')
from scipy.spatial import Delaunay, cKDTree

def comp_count_threshold(pts,t):
    n=len(pts)
    if n<=1: return n
    tri=Delaunay(pts); E=set()
    for s in tri.simplices:
        for a in range(3):
            for b in range(a+1,3):
                i,j=int(s[a]),int(s[b]); E.add((min(i,j),max(i,j)))
    we=sorted((math.dist(pts[i],pts[j]),i,j) for (i,j) in E)
    par=list(range(n))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    longe=0; used=0
    for w,i,j in we:
        ri,rj=f(i),f(j)
        if ri!=rj:
            par[ri]=rj
            if w>t: longe+=1
            used+=1
            if used==n-1: break
    return 1+longe

def cell_graph_components(pts,r,a,origin):
    ci=np.floor((pts[:,0]-origin[0])/a).astype(np.int64)
    cj=np.floor((pts[:,1]-origin[1])/a).astype(np.int64)
    key=ci*(10**12)+cj
    uniq=np.unique(key)
    cgx=(uniq//(10**12)); cgy=(uniq%(10**12))
    centers=np.column_stack([(cgx+0.5)*a,(cgy+0.5)*a])
    N=len(uniq); par=list(range(N))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    tree=cKDTree(centers)
    pairs=tree.query_pairs(r+math.sqrt(2)*a+1e-9,output_type='ndarray')
    for u,v in pairs:
        dx=max(0,(abs(cgx[u]-cgx[v])-1))*a
        dy=max(0,(abs(cgy[u]-cgy[v])-1))*a
        if math.hypot(dx,dy)<=r:
            ru,rv=f(int(u)),f(int(v))
            if ru!=rv: par[ru]=rv
    return len({f(k) for k in range(N)})

def run(name,Q,h=1.0,sigma=0.25):
    Q=np.asarray(Q,float)
    origin=(0.0,0.0)
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    rmin=256*h  # ensure sigma*r/64 > h
    rs=[]; r=rmin
    while r<diam: rs.append(r); r*=(1+sigma)
    viol=0; checks=0; lines=[]
    for r_j in rs:
        a_hi=sigma*r_j/64.0
        a_j=h
        while a_j*2<=a_hi: a_j*=2
        if a_j<=h: continue
        t_hi=r_j+2*math.sqrt(2)*a_j
        c_t=cell_graph_components(Q,r_j,a_j,origin)
        c_rj=comp_count_threshold(Q,r_j)
        c_thi=comp_count_threshold(Q,t_hi)
        lo=c_thi<=c_t; hi=c_t<=c_rj
        checks+=1
        tag="ok" if (lo and hi) else "VIOL"
        if checks<=12 or not(lo and hi):
            lines.append(f"   r={r_j:9.1f} a={a_j:8.2f} c(r+2v2a)={c_thi:4d} c~={c_t:4d} c(r)={c_rj:4d} lo={lo} hi={hi} [{tag}]")
        if not(lo and hi): viol+=1
    print(f"  {name}: a>h scales={checks}, violations={viol}", flush=True)
    for L in lines[:14]: print(L,flush=True)

if __name__=="__main__":
    rng=np.random.default_rng(5)
    # big-spread uniform support on integer grid, h=1
    pts=rng.integers(0,200000,size=(4000,2)).astype(float)
    Q=np.unique(pts,axis=0)
    run("big-uniform h=1",Q,h=1.0)
    # clustered: a few dense blobs far apart (forces nontrivial c~ at large a)
    blobs=[]
    centers=[(0,0),(80000,0),(0,80000),(80000,80000),(40000,40000)]
    for cx,cy in centers:
        b=rng.integers(0,3000,size=(700,2))+np.array([cx,cy])
        blobs.append(b)
    Q2=np.unique(np.vstack(blobs).astype(float),axis=0)
    run("5-blobs h=1",Q2,h=1.0)
    print("DONE",flush=True)
