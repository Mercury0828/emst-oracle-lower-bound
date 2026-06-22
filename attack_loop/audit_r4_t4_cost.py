"""
TASK 4 (COST): does the round-4 spatial estimator's query budget actually sum to Õ(sqrt(K))?
This is where the round-2 failure HID (a cost/variance blowup behind a correct recovery).

We implement the estimator's accounting faithfully and MEASURE the total candidate-cell
range-counts, then compare to sqrt(K).

Per round-4:
  - active cover: b=Theta(sqrt(K)) active delta-blocks; W_Q = Omega(b*delta).  (we compute b,delta directly)
  - per fine scale r_j (a_j ~ sigma r_j): M_j = #candidate a_j-cells in the union of active blocks
                                          = b*(delta/a_j)^2 (eq 6)
  - U_j = C(1 + G/(sigma r_j)) >= N_j  (deterministic upper bd on #occupied cells, eq 3)
  - target additive accuracy alpha_j = eta*G/(C1*T*sigma*r_j)   (eq 7)
  - #trials k_j = Theta(M_j*U_j/alpha_j^2)   (variance Var(Z)<=M_j*c_j<=M_j*U_j, additive alpha_j)
  Claim (eq 8): M_j U_j/alpha_j^2 <= C_eta * T^2 * (delta/r_j); sum_j delta/r_j = O(delta/(sigma r_0)) = O_eta(sqrt K).

We compute b, delta, M_j, U_j, alpha_j, k_j for REAL EMST supports and report:
  total_trials = sum_j k_j   vs   sqrt(K)   (up to the T^2/eta^2 polylog/eta factor).
We separate the genuine scaling (in K) from the (eta,T) constants by taking ratio total/(sqrt(K)).
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
    """First dyadic level with b>=q=ceil(sqrt(K)) nonempty cells. Returns b, delta, and the cover blocks."""
    K=len(Q); q=math.ceil(math.sqrt(K))
    x0,y0=Q[:,0].min(),Q[:,1].min()
    span=max(Q[:,0].max()-x0, Q[:,1].max()-y0)
    # root dyadic cell side = next power of 2 * h covering span
    side=h
    while side<span: side*=2
    delta=side
    while True:
        ci=np.floor((Q[:,0]-x0)/delta).astype(np.int64)
        cj=np.floor((Q[:,1]-y0)/delta).astype(np.int64)
        nb=len(set(zip(ci.tolist(),cj.tolist())))
        if nb>=q or delta<=h:
            return nb, delta, q
        delta/=2

def cost_accounting(name,Q,h=1.0,sigma=0.25,eta=0.25):
    Q=np.asarray(Q,float); K=len(Q)
    edges=mst_edges(Q); WQ=sum(edges)
    b,delta,q = active_cover(Q,h)
    diam=math.hypot(np.ptp(Q[:,0]),np.ptp(Q[:,1]))
    G=WQ  # tight guess G>=W_Q (use WQ; the search gives G_0 in [WQ,4WQ))
    # r_0 = max{h, eta G/(C0 K)}; take C0=1
    r0=max(h, eta*G/(K))
    rs=[]; r=r0
    while r<diam: rs.append(r); r*=(1+sigma)
    T=len(rs)
    C=1.0; C1=1.0
    total_trials=0.0
    total_sumdelta_r=0.0
    # also measure the ACTUAL packing constant: is W_Q >= c*b*delta?
    packing_ratio = WQ/(b*delta) if b*delta>0 else float('inf')
    for r_j in rs:
        a_j=max(h, sigma*r_j/96.0)   # within [sigma r/128, sigma r/64] band (use /96)
        # M_j = b*(delta/a_j)^2  but capped: a_j-cells only where they exist; if a_j>delta, coarse (explicit)
        if a_j>=delta:
            # coarse scale: explicit, O(b) cost, not sampled
            M_j=0.0; k_j= b   # explicit cost ~ b
            total_trials+=k_j
            continue
        M_j = b*(delta/a_j)**2
        U_j = C*(1.0 + G/(sigma*r_j))
        alpha_j = eta*G/(C1*T*sigma*r_j)
        k_j = M_j*U_j/(alpha_j**2)
        total_trials += k_j
        total_sumdelta_r += delta/r_j
    sqrtK=math.sqrt(K)
    print(f"  {name}: K={K} W_Q={WQ:.1f} b={b} delta={delta:.2f} q=ceil(sqrtK)={q} "
          f"packing W_Q/(b*delta)={packing_ratio:.3f}", flush=True)
    print(f"     r0={r0:.3f} T={T} scales | sum_j delta/r_j={total_sumdelta_r:.2f} "
          f"(claim O(delta/(sigma r0))={delta/(sigma*r0):.1f}, O_eta(sqrtK)={sqrtK:.1f})", flush=True)
    print(f"     TOTAL trials sum_j k_j = {total_trials:.3e} | sqrtK={sqrtK:.1f} | "
          f"ratio total/(sqrtK*T^2/eta) = {total_trials/(sqrtK*T*T/eta):.3f}", flush=True)
    return K, total_trials, sqrtK, T, eta, packing_ratio

if __name__=="__main__":
    rng=np.random.default_rng(13)
    def snap(pts,h):
        return np.unique(np.floor(pts/h)*h+h/2,axis=0)
    res=[]
    # uniform supports of growing K
    for npts,scale in [(1200,40),(4500,80),(12000,140),(30000,220)]:
        Q=snap(rng.random((npts,2))*scale,1.0)
        res.append(cost_accounting(f"uniform K~{len(Q)}",Q))
    # satellite supports of growing K
    def sat(s):
        K=s*s; h=float(s); D=float(s*s)
        nA=K-s; side=int(math.isqrt(nA)); nA=side*side
        gx,gy=np.meshgrid(np.arange(side),np.arange(side))
        A=np.column_stack([gx.ravel(),gy.ravel()]).astype(float)*h
        x0=A[:,0].max()+D
        sa=np.array([[x0+j*D,0.0] for j in range(K-nA)])
        return np.vstack([A,sa]),h
    for s in [24,40,64,96]:
        Q,hh=sat(s); res.append(cost_accounting(f"satellite s={s}",Q,h=hh))
    print("\nSCALING CHECK: does total_trials grow like sqrt(K) (up to T^2/eta polylog)?", flush=True)
    print("  K        total_trials   sqrtK    total/(sqrtK*T^2/eta)   packing", flush=True)
    for K,tot,sk,T,eta,pk in res:
        print(f"  {K:7d}  {tot:.3e}   {sk:7.1f}   {tot/(sk*T*T/eta):8.3f}            {pk:.3f}", flush=True)
    print("DONE",flush=True)
