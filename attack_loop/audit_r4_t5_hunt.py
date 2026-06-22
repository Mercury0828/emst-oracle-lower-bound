"""
TASK 5: NEW-COUNTEREXAMPLE HUNT against the round-4 spatial estimator.

The whole Õ(sqrt K) hinges on (eq8 derivation):
  (P1) active cover b in [sqrt K, 4 sqrt K)  (first-crossing dyadic rule)
  (P2) PACKING: W_Q = Omega(b*delta)
  (P3) M_j = b*(delta/a_j)^2  (candidate cells confined to the union of the b active delta-blocks)
  (P4) §10 dichotomy: a feature is support-rare OR spatially-hidden-at-its-scale, never both while
       carrying constant MST fraction.

ATTACK ANGLES tested here:
 (A) Try to make PACKING FAIL: W_Q << b*delta. If W_Q/(b*delta) -> 0 as K grows, cost blows up.
     Candidate: features that occupy MANY active blocks but are cheaply connected (small MST).
 (B) Fractal / hierarchical Cantor-like arrangement: occupy few spatial cells at each scale but
     carry weight across many scales (test §10).
 (C) An instance where a constant-MST-fraction feature occupies FEW spatial cells at its scale
     (spatially hidden) -> would make M_r small but c_r contribution large yet sampling miss it.
     Measure: at the satellite-tail scale, #spatial a-cells occupied by the rare component vs M_j;
     and whether the leader estimator's variance M_j*c_j stays controlled.

For each instance: build exact EMST, compute b, delta, W_Q, packing ratio across growing K, and the
per-scale "spatial occupancy fraction" of the heaviest rare feature. Report if packing -> 0.
"""
import math, sys
import numpy as np
sys.path.insert(0,'sim')
from scipy.spatial import Delaunay

def mst_edges(pts):
    n=len(pts)
    if n<=1: return []
    pts=np.asarray(pts,float)
    # collinear fallback: if all points lie on a line, MST = sorted consecutive gaps
    rng_x=np.ptp(pts[:,0]); rng_y=np.ptp(pts[:,1])
    if rng_y<1e-9 or rng_x<1e-9:
        coord = pts[:,0] if rng_y<1e-9 else pts[:,1]
        sc=np.sort(coord)
        return list(np.diff(sc))
    try:
        tri=Delaunay(pts)
    except Exception:
        tri=Delaunay(pts, qhull_options="QJ")
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

def report(name,Q,h=1.0):
    Q=np.asarray(Q,float); K=len(Q)
    if K<4:
        print(f"  {name}: K<4 skip"); return
    edges=mst_edges(Q); WQ=sum(edges)
    b,delta,q=active_cover(Q,h)
    pack=WQ/(b*delta) if b*delta>0 else float('inf')
    print(f"  {name}: K={K} W_Q={WQ:.1f} b={b}(q={q}) delta={delta:.1f} "
          f"PACKING W_Q/(b*delta)={pack:.3f} {'<<< PACKING SMALL!' if pack<0.1 else ''}", flush=True)
    return pack

if __name__=="__main__":
    rng=np.random.default_rng(21)
    def snap(pts,h):
        return np.unique(np.floor(pts/h)*h+h/2,axis=0)

    print("=== (A) Try to break PACKING W_Q=Omega(b*delta): many active blocks, cheap MST ===", flush=True)
    # A1: a SINGLE thin line of points spanning a huge box -> occupies many delta-blocks along a line,
    #     but MST = just the line length. b ~ sqrt(K) blocks all on a 1D line; W_Q ~ length.
    for L in [2000,8000,32000,128000]:
        # K points on a horizontal line, spacing 1 -> they fill one row of cells; cheap MST=K-1
        Q=np.column_stack([np.arange(L,dtype=float), np.zeros(L)])
        report(f"thin-line L={L}",Q)
    # A2: sqrt(K) x sqrt(K) GRID (the canonical packing-tight case) for reference
    for s in [30,60,120,200]:
        g=np.array([[i,j] for i in range(s) for j in range(s)],float)
        report(f"grid {s}x{s}",g)

    print("\n=== (B) FRACTAL / hierarchical (Cantor-dust): weight across many scales, few cells/scale ===", flush=True)
    # Build a 2D Cantor-like set: at each of L levels, each surviving cell spawns 4 children in corners,
    # separated by growing gaps. Weight spread across log scales.
    def cantor(levels, gap0=3.0, h=1.0):
        pts=np.array([[0.0,0.0]])
        gap=gap0
        for lvl in range(levels):
            off=gap
            newp=[]
            for (x,y) in pts:
                for dx in (0,off):
                    for dy in (0,off):
                        newp.append((x+dx,y+dy))
            pts=np.array(newp)
            gap*=4.0
        return snap(pts,h)
    for lv in [4,5,6,7]:
        Q=cantor(lv)
        report(f"cantor levels={lv}",Q)

    print("\n=== (C) Hierarchical 'satellites at every scale' (recursive rare features) ===", flush=True)
    # At each scale, add a few far points (rare features) so EACH dyadic scale has a satellite-like tail.
    def multiscale(levels, base=64, h=1.0):
        # dense core of `base` points + at each level a handful of satellites at distance ~ 4^level
        core=snap(rng.random((base,2))*math.sqrt(base),1.0)
        pts=[core]
        d=4.0*math.sqrt(base)
        for lvl in range(levels):
            nsat=4
            sat=np.array([[d*(1+0.3*k), 0.0] for k in range(nsat)])
            pts.append(sat)
            d*=4.0
        return snap(np.vstack(pts),h)
    for lv in [3,5,7,9]:
        Q=multiscale(lv, base=400)
        report(f"multiscale-sat levels={lv}",Q)
    print("DONE",flush=True)
