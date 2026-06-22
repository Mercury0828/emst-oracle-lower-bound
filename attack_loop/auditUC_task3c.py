"""
Task 3c: Try HARD to force the slab route back to Omega(sqrt n).

The slab estimator's query cost ~ sqrt(#nonempty slabs on the SAMPLED axis), because
it estimates a 1-D occupancy count among #slabs cells (U-B1: Omega(sqrt(#nonempty))).
With only N = sqrt(n) islands, #nonempty slabs per axis <= N = sqrt(n), so the cost
<= sqrt(sqrt(n)) = n^{1/4}.  We test: is there ANY way to make the slab-count itself
cost sqrt(n)?

Two adversarial levers:
 (L1) MANY islands. If the filament had M >> sqrt(n) islands, each contributing persistence
      < lambda, total could still be Theta(n) with M=n^{2/3}, lambda=n^{1/3} (so M*lambda=n).
      Then #nonempty slabs could be up to M = n^{2/3}, and slab-count cost ~ sqrt(M)=n^{1/3}.
      STILL o(sqrt n). Push further: M = n, lambda = 1 -> but lambda=1 means persistence O(1)
      each, that's the trivial (n-Delta) term, not the Sum lambda c term. The PERSISTENCE
      budget Sum = M*lambda = Theta(n) with M islands each pairwise >= lambda in a Delta x Delta
      box FORCES M*lambda^2 <= Delta^2 = n^2, i.e. M <= n^2/lambda^2 = n^2/(n/M)^2...
      Let's just SCAN (M, lambda) with M*lambda=n and the packing constraint and report
      the worst-case slab-count cost sqrt(#nonempty slabs).

 (L2) FRACTAL/2-D spread to maximize nonempty slabs on BOTH axes simultaneously while
      keeping consecutive ~lambda (no blowup). We measure #nonempty slabs per axis for the
      packing-limited regimes.

Constraint algebra (the crux):
  - M islands, pairwise >= lambda, inside Delta x Delta, Delta = Theta(sqrt(n)*sqrt(M_per_axis))...
    Actually Delta is FIXED = Theta(n). Packing M points pairwise>=lambda in [0,Delta]^2
    requires M*lambda^2 <= O(Delta^2) = O(n^2).
  - Persistence budget Theta(n): roughly M*lambda = Theta(n)  (each persists ~lambda).
  - #nonempty width-lambda slabs per axis <= min(M, Delta/lambda) = min(M, n/lambda).
  - Slab-count estimation cost (U-B1, 1-D) ~ sqrt(#nonempty slabs)  -- but ONLY if we must
    estimate the COUNT to rel error. The persistence estimate needs (#nonempty)*lambda to
    rel error eps, and #nonempty is a 1-D occupancy count over (n/lambda) cells ->
    cost ~ sqrt(#nonempty) by U-B1.
"""
import numpy as np


def analyze(n):
    """Scan lambda (= n^a) with M = n/lambda islands (persistence budget Theta(n))."""
    print(f"\n n = {n} = sqrt-domain Delta ~ {n}")
    print(f"{'lambda':>10} {'M=n/lam':>10} {'pack:M*lam^2/n^2':>16} "
          f"{'#slabs/axis=n/lam':>16} {'#ne<=min(M,n/lam)':>17} "
          f"{'slabcost~sqrt(ne)':>17} {'/sqrt(n)':>9}")
    for a in [1/6, 1/4, 1/3, 1/2, 2/3, 3/4, 5/6]:
        lam = n ** a
        M = n / lam                       # persistence budget M*lam = n
        pack = M * lam**2 / n**2          # must be <= O(1) to fit pairwise>=lam in Delta=n box
        slabs_axis = n / lam              # number of width-lam slabs spanning Delta=n
        ne = min(M, slabs_axis)           # nonempty slabs per axis <= both
        slabcost = np.sqrt(ne)            # U-B1 1-D occupancy-count cost
        print(f"{lam:>10.1f} {M:>10.1f} {pack:>16.4f} "
              f"{slabs_axis:>16.1f} {ne:>17.1f} "
              f"{slabcost:>17.1f} {slabcost/np.sqrt(n):>9.4f}")


def main():
    print("=== Task 3c: can the slab-count route be forced to sqrt(n)? (analytic scan) ===")
    print("Constraints: persistence budget M*lambda = Theta(n);")
    print("             packing M*lambda^2 <= Delta^2 = n^2 (pairwise >= lambda in n x n box).")
    print("             #nonempty slabs/axis = min(M, n/lambda); slab-count cost ~ sqrt(#nonempty).")
    for n in [10**4, 10**6, 10**9, 10**12]:
        analyze(n)
    print()
    print("VERDICT TEST: the column 'slabcost/sqrt(n)' -- if it is < 1 for ALL feasible lambda")
    print("(rows with pack <= 1), then NO persistence-Theta(n) filament forces the slab route")
    print("to sqrt(n); the slab/projection repair is structurally o(sqrt n).")
    print()
    print("The WORST feasible row is where #nonempty is MAXIMIZED subject to pack<=1.")
    print("min(M, n/lam) is maximized at M = n/lam, i.e. when lam <= sqrt(n) (M>=sqrt(n)),")
    print("there #ne = n/lam, maximized as lam->small; but pack = M*lam^2/n^2 = lam/n <=1 always.")
    print("Wait: at small lam, M=n/lam is huge; #ne=min(M, n/lam)=n/lam; cost=sqrt(n/lam).")
    print("Max over lam>=1 at lam=1: cost=sqrt(n) !!  -> lam=1 IS the danger. But lam=1 means")
    print("persistence per island = O(1), which is the trivial (n-Delta) term, NOT Sum lambda c.")
    print("For the Sum-lambda-c term we need lambda >= (1+eps) i.e. lambda growing; the dangerous")
    print("lonely-LONG-persistence stratum has lambda = n^Omega(1).  Re-examine with lam>=n^delta.")


if __name__ == "__main__":
    main()
