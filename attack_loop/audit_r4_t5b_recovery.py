"""
TASK 5 (recovery hunt): run the FULL spatial-cell leader estimator with a budget tied to the
TRUE variance bound (k_j set by the eq(7) additive target, but CAPPED for tractability) and check
whether recovery breaks on adversarial families where a rare feature is spatially hidden.

Hardest targets:
 (C1) multiscale-satellites: a rare tail at EVERY dyadic scale (stress the per-scale estimator).
 (C2) "single hidden bridge": two dense blobs + ONE far blob connected by a single long edge; at the
      bridge scale the rare component is essentially 1 cell among M_j -> can the leader estimator
      recover a component that is 1-in-M? (the satellite case had s cells; this is the extreme 1 cell.)
 (C3) "graded satellites": satellites whose count shrinks while their length grows, so the tail mass is
      spread thin across scales AND across few cells.

We reconstruct What = (K-1)h + sum_j d_j(chat_j - 1) with chat_j from REAL leader sampling, and compare
What/W_Q. We use k_j = min(cap, round(M_j*U_j/alpha_j^2)) trials. If recovery FAILS (What/W_Q far from 1)
even with the full intended k_j (not the cap), that is a round-5 counterexample.
"""
import math, sys
import numpy as np
sys.path.insert(0,'sim')
from scipy.spatial import Delaunay

def mst_edges_and_labels(pts):
    n=len(pts)
    pts=np.asarray(pts,float)
    if n<=1: return [], None
    if np.ptp(pts[:,1])<1e-9 or np.ptp(pts[:,0])<1e-9:
        coord=pts[:,0] if np.ptp(pts[:,1])<1e-9 else pts[:,1]
        order=np.argsort(coord)
        return list(np.diff(coord[order])), None
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
    return out, None

def comp_labels(pts,r):
    n=len(pts); pts=np.asarray(pts,float)
    par=list(range(n))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    if np.ptp(pts[:,1])<1e-9 or np.ptp(pts[:,0])<1e-9:
        coord=pts[:,0] if np.ptp(pts[:,1])<1e-9 else pts[:,1]
        order=np.argsort(coord)
        for k in range(1,n):
            if coord[order[k]]-coord[order[k-1]]<=r:
                a,b=f(order[k]),f(order[k-1])
                if a!=b: par[a]=b
        return np.array([f(i) for i in range(n)])
    try: tri=Delaunay(pts)
    except Exception: tri=Delaunay(pts,qhull_options="QJ")
    for s in tri.simplices:
        for a in range(3):
            for b in range(a+1,3):
                u,v=int(s[a]),int(s[b])
                if math.dist(pts[u],pts[v])<=r:
                    ru,rv=f(u),f(v)
                    if ru!=rv: par[ru]=rv
    return np.array([f(i) for i in range(n)])

def est_c_spatial(Q,labels,a,origin,M_index, k, rng):
    """Leader estimator at cell-side a. M = #candidate cells in bounding box. Sample k cells uniformly."""
    ci=np.floor((Q[:,0]-origin[0])/a).astype(np.int64)
    cj=np.floor((Q[:,1]-origin[1])/a).astype(np.int64)
    ncx,ncy=M_index
    M=ncx*ncy
    occ={}
    cid=ci*ncy+cj
    for idx in range(len(Q)):
        c=int(cid[idx]); lab=int(labels[idx])
        if c not in occ: occ[c]=lab
        else: occ[c]=min(occ[c],lab)
    cells=list(occ.keys())
    rank={c:rng.random() for c in cells}
    comp_min={}
    for c in cells:
        lab=occ[c]
        if lab not in comp_min or rank[c]<rank[comp_min[lab]]:
            comp_min[lab]=c
    leaders=set(comp_min.values()); occset=set(cells)
    if k>=M:
        # exact: chat = #leaders
        return float(len(leaders))
    hit=0
    rc=rng.integers(0,M,size=k)
    for X in rc:
        X=int(X)
        if X in occset and X in leaders: hit+=1
    return (hit/k)*M

def recover(name,Q,h=1.0,sigma=0.25,cap=200000):
    Q=np.asarray(Q,float); K=len(Q)
    edges,_=mst_edges_and_labels(Q); WQ=sum(edges)
    origin=(Q[:,0].min()-1e-9,Q[:,1].min()-1e-9)
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    rs=[]; r=h
    while r<diam: rs.append(r); r*=(1+sigma)
    T=len(rs)
    What=(K-1)*h
    rng=np.random.default_rng(7)
    worst_scale=None; worst_rel=0.0
    for r_j in rs:
        d=sigma*r_j; a=max(h,sigma*r_j/96.0)
        labels=comp_labels(Q,r_j)
        ncx=int((Q[:,0].max()-origin[0])/a)+2
        ncy=int((Q[:,1].max()-origin[1])/a)+2
        M=ncx*ncy
        # intended k_j ~ M*U/alpha^2; cap for tractability
        U=(1.0+WQ/(sigma*r_j)); alpha=sigma*WQ/(T*sigma*r_j)  # eta=sigma here
        k_int=int(M*U/(alpha**2)) if alpha>0 else cap
        k=min(cap,max(400,k_int))
        chat=est_c_spatial(Q,labels,a,origin,(ncx,ncy),k,rng)
        # exact c at this scale for diagnostics
        c_ex=1+sum(1 for e in edges if e>r_j)
        What+=d*(chat-1)
    rel=What/WQ if WQ>0 else float('nan')
    print(f"  {name}: K={K} W_Q={WQ:.1f} T={T} -> What/W_Q={rel:.3f}", flush=True)
    return rel

if __name__=="__main__":
    rng=np.random.default_rng(31)
    def snap(pts,h):
        return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    print("=== (C2) single hidden bridge: rare component = 1 cell at bridge scale ===", flush=True)
    for D in [500,2000,8000]:
        b1=snap(rng.random((400,2))*20,1.0)
        b2=snap(rng.random((400,2))*20,1.0)+np.array([40.0,0.0])
        far=snap(rng.random((4,2))*3,1.0)+np.array([D,0.0])  # tiny far blob => 1 long bridge
        Q=np.vstack([b1,b2,far])
        recover(f"hidden-bridge D={D}",Q)

    print("\n=== (C3) graded satellites: count shrinks, length grows (thin tail across scales) ===", flush=True)
    def graded(nlev, core=600, h=1.0):
        A=snap(rng.random((core,2))*math.sqrt(core),1.0)
        x0=A[:,0].max()
        pts=[A]; d=4.0*math.sqrt(core)
        for lvl in range(nlev):
            nsat=max(1, 8>>lvl)   # 8,4,2,1,...
            sat=np.array([[x0+d*(k+1),0.0] for k in range(nsat)])
            pts.append(sat); x0=x0+d*nsat; d*=2.0
        return snap(np.vstack(pts),h)
    for nl in [3,5,7]:
        recover(f"graded-sat lev={nl}",graded(nl))

    print("\n=== (C1) multiscale satellites (rare tail at every scale) ===", flush=True)
    def multiscale(levels, base=600, h=1.0):
        core=snap(rng.random((base,2))*math.sqrt(base),1.0)
        pts=[core]; d=4.0*math.sqrt(base)
        for lvl in range(levels):
            sat=np.array([[d*(1+0.3*k),0.0] for k in range(4)])
            pts.append(sat); d*=4.0
        return snap(np.vstack(pts),h)
    for lv in [4,6,8]:
        recover(f"multiscale lev={lv}",multiscale(lv))
    print("DONE",flush=True)
