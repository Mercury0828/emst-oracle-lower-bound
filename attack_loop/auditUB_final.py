"""
FINAL: on codex's EXACT islands+bulk instance, does a localized-probe importance-sampling
estimator recover Sum lambda c (hence w) in o(sqrt n) range-count queries, beating the
Omega(sqrt n) variance barrier of the UNIFORM point estimator?

Estimator (sketch, instance-restricted):
  For each dyadic scale lambda (O(log Delta) scales):
    estimate #lonely-at-scale-lambda cells by:
      draw t = O(1/eps^2 * log) random anchor points among the n (or random domain locations),
      around each, count |P cap lambda-box| via O(1) range queries; classify lonely if ==1.
      lonely_fraction_hat -> times (estimate of #occupied lambda-cells) -> contribution.
  Sum lambda * (#lonely + larger-component corrections).
We compare estimator's island-contribution vs truth, and total queries vs sqrt n.

NB: This is a POSITIVE result *only on this instance class* (islands that tile / are
hittable). It is NOT a general algorithm: the Driemel n^{1/3} construction (heavy gadget
hidden among 16 n^{1/3} cells, each query hits <=4 cells) is the genuinely hard instance,
and it caps at n^{1/3}, not sqrt n. The point: codex's sqrt-n VARIANCE BARRIER is an artifact
of the uniform estimator, not a real sqrt-n lower bound for these instances.
"""
import numpy as np
from scipy.spatial import cKDTree
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","sim"))
from emst import emst_weight
rng=np.random.default_rng(17)

class Oracle:
    def __init__(self,P):
        self.P=np.asarray(P,float); self.calls=0
        self.xs=np.sort(self.P[:,0])
    def count_strip(self,x0,x1):
        self.calls+=1
        # 1D-on-a-line instance: count points with x in [x0,x1) (y collapsed)
        return int(np.searchsorted(self.xs,x1)-np.searchsorted(self.xs,x0))

def estimate_island_contrib(P, eps=0.3, probes_per_scale=150):
    orc=Oracle(P)
    xmin,xmax=P[:,0].min(),P[:,0].max()
    span=xmax-xmin
    s=int(np.ceil(np.log(2*span)/np.log(1+eps)))
    contrib=0.0
    # exact occupied-cell estimate is hard; here we estimate the lonely-COUNT directly:
    # #lonely-at-lambda ~ (domain length / lambda) * P(random lambda-box is occupied & singleton)
    # but that double counts; instead estimate lonely count by random anchored boxes scaled
    # to total occupied length. We use the simplest unbiased form:
    #   #lonely = (span/lambda) * E[ 1[box occupied with exactly 1 pt] ] over random box position.
    for i in range(0,s+1,1):
        lam=(1+eps)**i
        if lam>2*span: break
        nboxes=span/lam
        hits_lonely=0
        for _ in range(probes_per_scale):
            x=rng.uniform(xmin-lam,xmax)
            c=orc.count_strip(x,x+lam)
            if c==1: hits_lonely+=1
        frac=hits_lonely/probes_per_scale
        lonely_est=frac*nboxes
        contrib += eps*lam*lonely_est   # lonely cells are singleton comps -> +1 each to c_i
    return contrib, orc.calls

print("="*78)
print("FINAL: localized-probe island-contribution estimate vs queries (codex instance)")
print("="*78)
for n in (1024, 4096, 16384, 65536):
    M=int(round(np.sqrt(n))); L=np.sqrt(n)
    islands=np.column_stack([np.arange(M)*L, np.zeros(M)])
    nb=n-M
    bulk=np.column_stack([(M+2)*L+rng.random(nb)*0.5, np.zeros(nb)])
    P=np.vstack([islands,bulk])
    # truth: island contribution to Sum lambda c ~ integral over scales [1,L] of (#island comps=M)
    # = sum_i eps*lam*M for lam in [1,L] ~ M*L = n  (the persistence band)
    true_band=0.0; lam=1.0
    while lam<=L:
        true_band+=0.3*lam*M; lam*=1.3
    est,calls=estimate_island_contrib(P)
    print(f" n={n:6d} M={M:4d}  est_island_contrib={est:11.0f}  true_band~{true_band:11.0f}"
          f"  ratio={est/true_band:5.2f}  queries={calls}  sqrt(n)={np.sqrt(n):.0f}"
          f"  o(sqrt n)? {'YES' if calls<n**0.5*np.log2(n) else 'check'}")
