"""
TASK 3: (A) W-search stopping rule arithmetic (round-4 §8).
   U=(K-1)diam; run additive-1/20 estimator for G=U,U/2,...; stop at first What_G >= G/3.
   Claim: G>=4W_Q => What_G <= W_Q + G/20 <= G/4 + G/20 < G/3 (continue);
          G in [W_Q,2W_Q) => What_G >= W_Q - G/20 > G/3 (stop).
   => on stop, W_Q <= G_0 < 4 W_Q.
(B) K-estimation (§9): X(p)=n/m(p), p~Unif(P), m(p)=#points in p's h-cell.
   E[X]=K, E[X^2]=n*sum_C 1/m_C <= nK. => relative estimate of K in Õ(n/K) samples.
   Verify E[X]=K and E[X^2] <= nK numerically on random multiplicity profiles.
"""
import numpy as np

def check_wsearch_arithmetic():
    print("(A) W-search arithmetic:", flush=True)
    # additive accuracy eps_add = 1/20 relative to G (i.e. |What_G - W_Q| <= G/20)
    eps=1/20.0
    ok_all=True
    # symbolic-style numeric sweep over W_Q and G multiples
    for WQ in [1.0, 7.3, 100.0]:
        # case G>=4WQ : pick G=4WQ exactly (worst, boundary) and larger
        for mult in [4.0, 5.0, 8.0, 16.0]:
            G=mult*WQ
            What_hi = WQ + G*eps          # max possible estimate
            cont = What_hi < G/3.0        # want CONTINUE (not >= G/3)
            # bound used by Pro: What_hi <= G/4 + G/20  (since WQ <= G/4)
            bound = G/4.0 + G*eps
            if not (cont and bound < G/3.0 and What_hi<=bound+1e-12):
                # at mult=4 boundary WQ=G/4 exactly so What_hi=bound
                if not (What_hi < G/3.0+1e-12):
                    print(f"   [FAIL continue] WQ={WQ} G={G} What_hi={What_hi:.4f} G/3={G/3:.4f}")
                    ok_all=False
        # case G in [WQ, 2WQ): What_G >= WQ - G/20 must be > G/3 to STOP
        for mult in [1.0, 1.5, 1.99]:
            G=mult*WQ
            What_lo = WQ - G*eps          # min possible estimate
            stop = What_lo > G/3.0
            if not stop:
                print(f"   [FAIL stop] WQ={WQ} G={G} What_lo={What_lo:.4f} G/3={G/3:.4f}")
                ok_all=False
    print(f"   continue-when-G>=4WQ and stop-when-G<2WQ: {'ALL HOLD' if ok_all else 'VIOLATION'}", flush=True)
    # the GAP region G in [2WQ, 4WQ): either decision is acceptable -> on stop G_0<4WQ, on continue next G halves into [WQ,2WQ)
    print("   gap region [2WQ,4WQ): either action acceptable; guarantees W_Q<=G_0<4W_Q on first stop.", flush=True)

def check_K_estimation(rng):
    print("\n(B) K-estimation unbiasedness + second moment E[X^2]<=nK:", flush=True)
    for trial in range(5):
        K=rng.integers(20,200)
        # multiplicities m_C >=1 summing to n
        m=rng.integers(1,40,size=K)
        n=int(m.sum())
        # p ~ Unif(P): point in cell C w.p. m_C/n; X = n/m_C
        # E[X] = sum_C (m_C/n)*(n/m_C) = K
        EX = sum((mc/n)*(n/mc) for mc in m)
        # E[X^2] = sum_C (m_C/n)*(n/m_C)^2 = n * sum_C 1/m_C
        EX2 = sum((mc/n)*((n/mc)**2) for mc in m)
        nsum_inv = n*sum(1.0/mc for mc in m)
        nK = n*K
        # Monte-Carlo confirm
        cells=np.repeat(np.arange(K), m)
        draws=rng.choice(cells, size=200000)
        Xs = n/m[draws]
        print(f"   K={K} n={n}: E[X]={EX:.3f}(MC {Xs.mean():.3f}) target {K} | "
              f"E[X^2]={EX2:.1f}(=n*sum1/m={nsum_inv:.1f}) <= nK={nK}? {EX2<=nK+1e-6}", flush=True)

if __name__=="__main__":
    rng=np.random.default_rng(2)
    check_wsearch_arithmetic()
    check_K_estimation(rng)
    print("DONE",flush=True)
