"""
TASK 4 (COST scaling, isolated): hold sigma,eta,C constants FIXED; vary K only;
measure total_trials / sqrt(K) for the satellite family (the adversarial one). If the
estimator is genuinely Õ(sqrt K), total_trials/sqrt(K) should be ~constant (flat) in K,
modulo T=O(log diam) growth. We divide by T^2 to remove that, and check flatness.

We ALSO directly test eq(8): per-scale M_j*U_j/alpha_j^2 <= C_eta * T^2 * (delta/r_j).
And eq accounting: sum_j (delta/r_j) <= C * delta/(sigma r_0), bounded by O_eta(sqrt K).
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

def per_scale_eq8(Q,h,sigma,eta):
    """Verify eq(8): M_j U_j / alpha_j^2 <= C_eta T^2 (delta/r_j) per scale (return max ratio)."""
    Q=np.asarray(Q,float); K=len(Q); edges=mst_edges(Q); WQ=sum(edges)
    b,delta,q=active_cover(Q,h)
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    G=WQ; r0=max(h,eta*G/K)
    rs=[]; r=r0
    while r<diam: rs.append(r); r*=(1+sigma)
    T=len(rs)
    maxratio=0.0; total=0.0; sdr=0.0
    for r_j in rs:
        a_j=max(h,sigma*r_j/96.0)
        if a_j>=delta:
            total+=b; continue
        M_j=b*(delta/a_j)**2
        U_j=(1.0+G/(sigma*r_j))
        alpha_j=eta*G/(T*sigma*r_j)
        kj=M_j*U_j/alpha_j**2
        total+=kj
        sdr+=delta/r_j
        # eq8 RHS (Pro): C_eta * T^2 * delta/r_j ; LHS/( T^2 delta/r_j )=:ratio, want O_eta(1)
        lhs=kj
        rhs_base=T*T*(delta/r_j)
        maxratio=max(maxratio, lhs/rhs_base)
    return K,WQ,b,delta,T,total,math.sqrt(K),maxratio,sdr,r0

if __name__=="__main__":
    print("SATELLITE family, sigma=eta=0.25 FIXED, K growing:", flush=True)
    print(" K      sqrtK   T   total/(sqrtK*T^2)   eq8 max[k_j/(T^2 delta/r_j)]   sumdelta_r/(delta/(sigma r0))", flush=True)
    def sat(s):
        K=s*s; h=float(s); D=float(s*s)
        nA=K-s; side=int(math.isqrt(nA)); nA=side*side
        gx,gy=np.meshgrid(np.arange(side),np.arange(side))
        A=np.column_stack([gx.ravel(),gy.ravel()]).astype(float)*h
        x0=A[:,0].max()+D
        sa=np.array([[x0+j*D,0.0] for j in range(K-nA)])
        return np.vstack([A,sa]),h
    rows=[]
    for s in [16,24,32,48,64,96,128]:
        Q,hh=sat(s)
        K,WQ,b,delta,T,total,sk,mr,sdr,r0=per_scale_eq8(Q,hh,0.25,0.25)
        norm_total=total/(sk*T*T)
        sdr_ratio=sdr/(delta/(0.25*r0))
        print(f" {K:6d}  {sk:6.1f}  {T:3d}   {norm_total:12.4f}        {mr:10.4f}                  {sdr_ratio:.3f}", flush=True)
        rows.append((K,norm_total,mr))
    print("\nFLATNESS: if total/(sqrtK*T^2) is ~constant in K => genuine Õ(sqrt K). "
          "If it GROWS in K => hidden blowup (round-2-style).", flush=True)
    ks=[r[0] for r in rows]; nt=[r[1] for r in rows]
    print(f"  total/(sqrtK*T^2): min={min(nt):.3f} max={max(nt):.3f} ratio max/min={max(nt)/min(nt):.2f} "
          f"over K range {min(ks)}..{max(ks)} ({max(ks)/min(ks):.0f}x)", flush=True)
    print("DONE",flush=True)
