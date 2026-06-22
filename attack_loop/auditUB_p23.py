"""
PART 2: Euler cancellation for a filled k x k occupied-cell block.
  V=k^2, E=2k(k-1), Z=(k-1)^2, c=V-E+Z=1. Verify and the error-amplification claim.
PART 3: n^{1/3} LB re-derivation sanity (S sqrt(m)=n^{3/2}/K vs K S = n sqrt K => K<=n^{1/3}).
"""
import numpy as np

print("="*70); print("PART 2: Euler cancellation, filled k x k block"); print("="*70)
print(f"{'k':>4} {'V=k^2':>8} {'E=2k(k-1)':>10} {'Z=(k-1)^2':>10} {'c=V-E+Z':>8} {'V+E scale':>10}")
for k in (2,4,8,16,32,64):
    V=k*k; E=2*k*(k-1); Z=(k-1)**2; c=V-E+Z
    print(f"{k:4d} {V:8d} {E:10d} {Z:10d} {c:8d} {'~'+str(k*k):>10}")
print("=> c=1 always; V,E,Z all Theta(k^2) and cancel.")
print("=> estimating V,E separately to additive err delta*k^2 gives c-error ~ delta*k^2 >> true 1.")
print("   (lambda-weighted: error Theta(k^2 lambda) vs true Theta(lambda)). Euler-aggregate route")
print("   needs the cycle-rank/connectivity, NOT just occupancy+adjacency totals. CONFIRMED.")

print()
print("="*70); print("PART 3: n^{1/3} LB re-derivation"); print("="*70)
print(f"{'n':>12} {'K':>6} {'S=n/sqrtK':>12} {'m=n/K':>10} {'S*sqrt(m)':>14} {'K*S=n sqrtK':>14} {'ratio':>8}")
for n in (10**6, 10**9, 10**12):
    for K in (int(n**(1/4)), int(n**(1/3)), int(n**(0.4))):
        S=n/np.sqrt(K); m=n/K
        internal=S*np.sqrt(m)       # = n^{3/2}/K
        connect=K*S                 # = n*sqrt(K)
        print(f"{n:12d} {K:6d} {S:12.1f} {m:10.1f} {internal:14.3e} {connect:14.3e} {internal/connect:8.3f}")
    print(f"   crossover internal>=connect: n^{{3/2}}/K >= n sqrt(K) <=> K <= n^{{1/3}}={n**(1/3):.1f}")
    print()
