import numpy as np, math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))

def build(n, lam):
    M = n // lam
    isl = np.array([[(i + 0.5) * lam, (i + 0.5) * lam] for i in range(M)], float)
    b = int(n - M); side = max(1, int(math.isqrt(b)))
    bx, by = np.meshgrid(np.arange(side), np.arange(side))
    bulk = np.column_stack([bx.ravel(), by.ravel()]).astype(float)[:b]
    bulk[:, 0] += M * lam + 10.0
    return np.vstack([isl, bulk]), M

def lonely_fraction_pointsample(P, lam, nsamp, rng):
    # "lonely at scale lam" = NO other point within EUCLIDEAN distance lam (a singleton component
    # at threshold lam). Implemented as: count points strictly inside the open disk of radius lam
    # around p (== 1 means only p itself). A counting oracle approximates this with a lam-box +
    # refine; here we use the exact Euclidean test as ground truth.
    idx = rng.integers(0, len(P), size=nsamp)
    hits = 0
    for i in idx:
        d = P - P[i]
        within = np.sum(d[:, 0] ** 2 + d[:, 1] ** 2 < lam * lam)  # includes self
        if within == 1:
            hits += 1
    return hits / nsamp

print(f"{'n':>7} {'lam':>6} {'M':>7} {'f=1/lam':>9} {'est_f':>7} {'pt~lam':>7} {'slab~sqrt(n/lam)':>16} {'min':>7} {'n^1/3':>7}")
rng = np.random.default_rng(0)
for n in [4096, 16384, 65536]:
    for lam in sorted(set([2, 4, int(round(n ** (1 / 3))), int(math.isqrt(n))])):
        P, M = build(n, lam)
        f_true = M / n
        nsamp = min(len(P), int(30 / max(f_true, 1e-9)))
        f_est = lonely_fraction_pointsample(P, lam, nsamp, rng)
        pointcost = 1.0 / max(f_true, 1e-9)
        slabcost = math.sqrt(n / lam)
        print(f"{n:>7} {lam:>6} {M:>7} {f_true:>9.4f} {f_est:>7.4f} {pointcost:>7.1f} {slabcost:>16.1f} {min(pointcost, slabcost):>7.1f} {n ** (1 / 3):>7.1f}")
