"""
THE CRUX (Part 4): can localized random range-COUNTING probes estimate the island
(lonely-point) contribution to Sum lambda c in o(sqrt n), breaking the variance barrier?

Estimator idea (importance sampling by RANDOM LOCALIZED PROBE, not uniform point sample):
  At each relevant scale lambda, the island contribution is lambda * (#lonely cells at lambda).
  Estimate the FRACTION of occupied lambda-cells that are lonely (occ resolvable by counting
  a lambda-box vs a (small) sub-box), by probing RANDOM occupied locations.
  If lonely sites TILE the domain, a random lambda-box hits an occupied site w.p. Theta(1)
  and reveals lonely/not in O(1) counts => O(1/eps^2) probes => o(sqrt n).

We test TWO instances:
 (A) ISLANDS-TILE: M=sqrt(n) lonely islands spaced L=sqrt(n) over domain [0, M*L]=[0,n].
     (codex's instance). Sites tile the domain.
 (B) ISLANDS-HIDDEN: same M islands but CONCEALED inside a dense bulk of side ~sqrt(n)*L
     region so each island occupies only a 1/sqrt(n) fraction -> Lemma-19-style low measure.

Question: does random localized probing estimate #lonely cheaply on (A)? on (B)?
This decides whether codex's specific instance (A) is actually hard, and whether a HIDDEN
variant (B) restores hardness.
"""
import numpy as np
from scipy.spatial import cKDTree
rng = np.random.default_rng(11)

def range_count(tree, lo, hi):
    """exact #points in axis-aligned rectangle [lo,hi] via KDTree. (counts queries elsewhere)"""
    # cKDTree has no native box count; emulate with two-sided via query_ball is slow.
    # Use a sorted structure instead for speed: caller passes precomputed arrays.
    raise NotImplementedError

class CountOracle:
    """Exact orthogonal range count on a 2D point set, O(log n) per query via sorted+BIT-ish.
       For test scale we just use boolean masks (correct, not query-optimal) and COUNT calls."""
    def __init__(self, P):
        self.P = np.asarray(P, float)
        self.calls = 0
    def count(self, x0,x1,y0,y1):
        self.calls += 1
        P=self.P
        return int(np.count_nonzero((P[:,0]>=x0)&(P[:,0]<x1)&(P[:,1]>=y0)&(P[:,1]<y1)))

def lonely_fraction_estimate(oracle, domain, L, nprobes):
    """Probe nprobes random lambda(=L)-boxes; among those that are OCCUPIED, estimate the
       fraction that are LONELY (a smaller centered sub-box of side L/4 contains the SAME
       count, and that count==1 within the L-box => isolated singleton at scale L).
       Returns (frac_lonely_among_occupied, n_occupied_probes)."""
    (X0,X1,Y0,Y1)=domain
    occ=0; lonely=0
    for _ in range(nprobes):
        x=rng.uniform(X0,X1-L); y=rng.uniform(Y0,Y1) if Y1>Y0 else 0.0
        c=oracle.count(x,x+L,-1e9,1e9)   # vertical strip of width L (1D-ish domain on a line)
        if c>=1:
            occ+=1
            if c==1:
                lonely+=1
    return (lonely/occ if occ>0 else 0.0), occ

print("="*78)
print("CRUX: localized-probe estimate of lonely-fraction. INSTANCE A (islands tile).")
print("="*78)
for n in (1024, 4096, 16384, 65536):
    M=int(round(np.sqrt(n))); L=np.sqrt(n)
    # islands spaced L on a line; plus a dense bulk also on the SAME line far away so that
    # both bulk and islands are 'occupied sites' but only islands are lonely.
    islands=np.column_stack([np.arange(M)*L, np.zeros(M)])
    nb=n-M
    # bulk packed densely into ONE L-box region (occ=nb there): NOT lonely
    bulk=np.column_stack([ (M+1)*L + rng.random(nb)*0.5, rng.random(nb)*0.5])
    P=np.vstack([islands,bulk])
    orc=CountOracle(P)
    true_lonely=M
    true_occ_sites=M+1  # M island-boxes + 1 bulk box (roughly)
    domain=(-L, (M+2)*L, 0.0,0.0)
    nprobes=200
    frac,occ=lonely_fraction_estimate(orc,domain,L,nprobes)
    est_lonely = frac*true_occ_sites   # frac of occupied sites that are lonely * #occupied
    print(f" n={n:6d} M={M:4d}  true_lonely={true_lonely:4d}  est_frac_lonely={frac:.3f}"
          f"  queries={orc.calls}  (nprobes={nprobes}, o(sqrt n)? sqrt n={np.sqrt(n):.0f})")
