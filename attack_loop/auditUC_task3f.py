"""
Task 3f: Is the small-lambda diagonal a GENUINE hard instance, or coarsely estimable?

Two escape routes a full algorithm could use that bypass box AND slab:

 (R-coarse) A polylog x polylog COARSE GRID of range counts. The small-lambda diagonal
   has M = n/lam islands spread on the line y=x over [0, M*lam] = [0,n]. A coarse grid of
   g x g cells (cell side n/g). Each coarse cell on the diagonal contains ~ M/g islands.
   A coarse count of a diagonal cell vs an off-diagonal cell: diagonal cells have ~M/g
   extra points. Does the coarse grid SEE the filament (distinguish it from no-filament)?
   And can the coarse grid + the (n-Delta) baseline RECOVER the persistence Theta(n)?

 (R-total) The persistence Theta(n) of the small-lambda stratum is just M*lam = n; but the
   TRIVIAL term (n - Delta) is also Theta(n). Is the small-lambda filament's contribution
   actually DISTINGUISHABLE from a bulk rearrangement, or is it absorbed/coarsely visible?

KEY MEASUREMENT: build (A) the small-lambda diagonal filament instance and (B) a "no-filament"
instance where those M points are folded into the bulk (so NO long-persistence singletons).
Compute exact w(MST) for both. If they differ by a constant fraction, the filament is a real
signal. Then test whether a polylog coarse grid distinguishes them (coarse counts differ),
which would mean the small-lambda stratum is COARSELY estimable (escape route exists).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from emst import emst_weight
from scipy.spatial import cKDTree


def build_filament(n, lam):
    M = int(round(n/lam)); M = min(M, n)
    islands = np.array([(k*lam+lam/2, k*lam+lam/2) for k in range(M)], dtype=float)
    m = n - M
    s = int(np.ceil(np.sqrt(max(m,1))))
    X0 = islands[:,0].max()+10*lam if M>0 else 0
    xs = np.arange(s); gx,gy = np.meshgrid(xs,xs)
    bulk = np.column_stack([gx.ravel()+X0, gy.ravel()]).astype(float)[:m]
    P = np.vstack([islands, bulk]) if m>0 else islands
    return P, islands, bulk, M


def build_nofilament(n, lam):
    """Same n; the M island points are instead packed INTO the bulk (no long singletons)."""
    M = int(round(n/lam)); M = min(M, n)
    s = int(np.ceil(np.sqrt(n)))
    xs = np.arange(s); gx,gy = np.meshgrid(xs,xs)
    P = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:n]
    return P


def coarse_grid_signature(P, g, domain_lo, domain_hi):
    """g x g counts over [domain_lo,domain_hi]^2."""
    side = (domain_hi-domain_lo)/g
    ix = np.clip(((P[:,0]-domain_lo)//side).astype(int), 0, g-1)
    iy = np.clip(((P[:,1]-domain_lo)//side).astype(int), 0, g-1)
    grid = np.zeros((g,g), dtype=int)
    np.add.at(grid, (ix,iy), 1)
    return grid


def main():
    n = 4096
    print(f"=== Task 3f: small-lambda filament vs no-filament, exact EMST (n={n}) ===\n")
    print(f"{'lam':>6} {'M':>6} {'w_filament':>11} {'w_nofil':>10} {'diff':>9} "
          f"{'diff/w_nofil':>12} {'persist=M*lam':>13}")
    for lam in [2.0, 4.0, 8.0, 16.0, 32.0, 64.0]:
        Pf, isl, bulk, M = build_filament(n, lam)
        Pn = build_nofilament(n, lam)
        wf = emst_weight(Pf)
        wn = emst_weight(Pn)
        print(f"{lam:>6.0f} {M:>6} {wf:>11.1f} {wn:>10.1f} {wf-wn:>9.1f} "
              f"{(wf-wn)/wn:>12.3f} {M*lam:>13.1f}")

    print()
    print("=== coarse-grid visibility of the small-lambda filament (lam=2, worst) ===")
    lam = 2.0
    Pf, isl, bulk, M = build_filament(n, lam)
    # domain covering the filament line [0, M*lam]
    print(f" filament: M={M} islands on y=x over [0,{M*lam:.0f}]; bulk block far right.")
    print(f"{'g (grid)':>9} {'maxDiagCell':>12} {'#nonemptyDiagCells':>18} {'queries=g^2':>12} {'/sqrt(n)':>9}")
    for g in [4, 8, 16, 32]:
        grid = coarse_grid_signature(isl, g, 0, M*lam)
        diag = np.array([grid[i,i] for i in range(g)])
        nonempty_diag = int((diag>0).sum())
        print(f"{g:>9} {diag.max():>12} {nonempty_diag:>18} {g*g:>12} {g*g/np.sqrt(n):>9.3f}")
    print()
    print("READING:")
    print(" - If w_filament - w_nofil ~ M*lam = Theta(n): the filament IS a constant-fraction")
    print("   real signal (must be estimated).")
    print(" - Coarse g x g grid: a diagonal cell holds ~M/g islands. To RESOLVE the persistence")
    print("   (which is per-singleton, scale ~lam) the grid cell side must be ~lam, i.e. g ~ n/lam,")
    print("   => g^2 ~ (n/lam)^2 queries = way more than sqrt(n). Coarse grid does NOT cheaply")
    print("   recover the PERSISTENCE; it only sees 'there is mass on the diagonal'.")
    print("   The mass on the diagonal is the SAME whether those points are lonely (persist lam)")
    print("   or clustered (persist O(1)) -- so coarse counts can't tell persistence. (Euler/U-P2.)")


if __name__ == "__main__":
    main()
