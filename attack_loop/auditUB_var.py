"""
PART 1 variance (fast, vectorized): point estimator X(p) = n * sum_i lambda_i/|comp_i(p)|
on the islands+bulk instance. Verify Var[X]/E[X]^2 = Theta(sqrt(n)) (codex's claim).

Uses scipy.sparse.csgraph.connected_components (fast union-find) per scale.
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

rng = np.random.default_rng(7)

def point_estimator(P, eps=0.3):
    n = len(P)
    rmax = np.ptp(P, axis=0).max()
    s = int(np.ceil(np.log(2*rmax)/np.log(1+eps)))
    tree = cKDTree(P)
    Xacc = np.zeros(n)
    for i in range(s+1):
        lam = (1+eps)**i
        pairs = tree.query_pairs(lam, output_type='ndarray')
        if len(pairs)==0:
            ncomp, labels = n, np.arange(n)
        else:
            data = np.ones(len(pairs))
            g = coo_matrix((data, (pairs[:,0], pairs[:,1])), shape=(n,n))
            ncomp, labels = connected_components(g, directed=False)
        _, inv, counts = np.unique(labels, return_inverse=True, return_counts=True)
        size = counts[inv]
        Xacc += eps*lam/size
        if ncomp == 1:
            break
    return n*Xacc

print("PART 1 variance: islands+bulk, point estimator X(p)")
print(f"{'n':>7} {'M':>4} {'E[X]':>12} {'Var/E^2':>10} {'sqrt(n)':>9} {'ratio/sqrtn':>11}")
for n in (256, 1024, 4096, 16384):
    M = int(round(np.sqrt(n)))
    L = np.sqrt(n)
    islands = np.column_stack([np.arange(M)*L, np.zeros(M)])
    nb = n - M
    bulk = rng.random((nb,2))*1.0 + np.array([0.0, -5*L])  # tight bulk, far below
    P = np.vstack([islands, bulk])
    X = point_estimator(P)
    E = X.mean(); V = X.var()
    r = V/E**2
    print(f"{n:7d} {M:4d} {E:12.1f} {r:10.3f} {np.sqrt(n):9.1f} {r/np.sqrt(n):11.3f}")
