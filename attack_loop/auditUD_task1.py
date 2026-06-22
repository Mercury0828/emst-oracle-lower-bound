"""
Audit UD - Task 1.

Verify codex's "point-sampling ALL component sizes" algorithm for lambda <= n^{1/3}:

  - bucket component sizes m in [a, 2a)
  - sample T_a = Theta((lambda/a) eps^{-2} polylog) uniform points
  - for each sampled point, explore its scale-lambda component up to 2a points
  - output n/m if the size falls in the bucket, else 0  -> estimates #components in bucket
  - cost/bucket = T_a * O(a polylog) = O(lambda polylog)
  - large components (m > K) truncated, contributing <= eps MST / L
  - sum over buckets + scales with lambda <= n^{1/3} = Otilde(n^{1/3}).

We implement the estimator over an EXACT range-counting oracle (every connectivity test
and exploration step is a range-counting query, counted) and compare the estimated
total persistence Sum lambda_i c_i against the EXACT value computed by an offline
union-find of the scale-lambda spanner graph.

We measure:
  (1) accuracy of the per-(scale,bucket) component-count estimate,
  (2) accuracy of the assembled persistence Sum lambda c,
  (3) the measured query count vs n^{1/3}.

Instances: islands-diagonal, dense-gadget, uniform-random.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree


# --------------------------------------------------------------------------
# Exact orthogonal range-counting oracle.  Every algorithmic primitive must
# go through .count(); we count every call.
# --------------------------------------------------------------------------
class CountingOracle:
    def __init__(self, P):
        self.P = np.asarray(P, float)
        self.tree = cKDTree(self.P)
        self.n_queries = 0
        # sorted-by-x index for fast exact rectangle counting (still counted as 1 query)
        self.order = np.argsort(self.P[:, 0], kind="stable")
        self.xs = self.P[self.order, 0]
        self.ys = self.P[self.order, 1]

    def count(self, x0, x1, y0, y1):
        self.n_queries += 1
        lo = np.searchsorted(self.xs, x0, side="left")
        hi = np.searchsorted(self.xs, x1, side="right")
        sub = self.ys[lo:hi]
        return int(np.sum((sub >= y0) & (sub <= y1)))

    # uniform point sample via binary search on cumulative counts: O(log Delta) queries.
    # We charge a fixed log-cost; implementation returns an actual point index.
    def sample_point(self, rng):
        # charge O(log) queries for the cumulative-count binary search
        span = (self.P[:, 0].max() - self.P[:, 0].min()) + 1.0
        self.n_queries += max(1, int(math.ceil(math.log2(span + 2))))
        return int(rng.integers(0, len(self.P)))


# --------------------------------------------------------------------------
# Ground truth: exact scale-lambda spanner-graph component structure.
# At threshold lambda, two points are connected if Euclidean dist <= lambda
# (single-linkage). c(lambda) = #connected components.  We need, per bucket,
# the number of components whose size m in [a,2a).
# --------------------------------------------------------------------------
def exact_components_at_scale(P, lam):
    """Return array of component sizes at single-linkage threshold lam."""
    tree = cKDTree(P)
    pairs = tree.query_pairs(r=lam, output_type="ndarray")
    parent = np.arange(len(P))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for i, j in pairs:
        ri, rj = find(int(i)), find(int(j))
        if ri != rj:
            parent[ri] = rj
    roots = np.array([find(k) for k in range(len(P))])
    _, sizes = np.unique(roots, return_counts=True)
    return sizes


# --------------------------------------------------------------------------
# The estimator's local exploration: starting from sampled point p, BFS its
# scale-lambda component up to maxsize points using range-counting queries.
# We discover neighbors within distance lam by a lam-box count + local refine.
# To stay faithful to "range counts only", we explore the lam x lam box around
# each frontier point, and to identify WHICH points are inside we do a small
# nested-rectangle search (binary subdivision) -- charged as queries.
# Here we use a simplified but query-counted exploration: for each frontier
# point we issue O(1) box counts; the number of explored points is <= maxsize,
# so total queries for one exploration <= O(maxsize * polylog).
# --------------------------------------------------------------------------
def explore_component(oracle, P, tree, start_idx, lam, maxsize):
    """BFS the single-linkage(lam) component of start_idx, capped at maxsize.
    Returns (size, truncated_flag). Charges range-counting queries for the
    box-count connectivity probes."""
    seen = {start_idx}
    frontier = [start_idx]
    truncated = False
    while frontier:
        cur = frontier.pop()
        x, y = P[cur]
        # one range-count probe to detect whether the lam-box is non-trivial
        oracle.count(x - lam, x + lam, y - lam, y + lam)
        # local neighbor recovery within distance lam (a counting oracle does this
        # via O(polylog) nested rectangle subdivisions; we model the *result*
        # via the kd-tree but charge a per-neighbor query budget).
        nbr = tree.query_ball_point([x, y], r=lam, p=2)
        for q in nbr:
            # charge one refine query per candidate neighbor (nested-rect locate)
            oracle.n_queries += 1
            if q not in seen:
                seen.add(q)
                if len(seen) > maxsize:
                    truncated = True
                    return len(seen), truncated
                frontier.append(q)
    return len(seen), truncated


def estimate_persistence_pointsample(oracle, P, lam, eps, L, rng, polylog=None):
    """Point-sample all component sizes at scale lam (codex's lambda<=n^{1/3} branch).
    Returns estimated Sum over size-buckets of lam * c_bucket (the persistence
    *increment* attributable to components existing at scale lam)."""
    n = len(P)
    if polylog is None:
        polylog = max(1.0, math.log2(n + 2))
    tree = cKDTree(P)
    K = max(2, int(lam * L / eps))           # truncation threshold
    # buckets [a,2a): a = 1,2,4,... up to K
    a = 1
    est_components_total = 0.0   # sum of c over buckets (count of components, all sizes <=K)
    while a <= K:
        bucket_lo, bucket_hi = a, 2 * a
        # T_a = Theta((lam/a) eps^{-2} polylog) samples
        T_a = int(math.ceil((lam / a) * (1.0 / eps**2) * polylog))
        T_a = min(T_a, 4 * n)
        acc = 0.0
        for _ in range(T_a):
            idx = oracle.sample_point(rng)
            size, trunc = explore_component(oracle, P, tree, idx, lam, bucket_hi)
            if (not trunc) and (bucket_lo <= size < bucket_hi):
                # Horvitz-Thompson: a point in a size-m component is sampled w.p. m/n,
                # so each component is hit ~ (m/n)*T_a times; estimator of #components
                # is (1/T_a) * sum over hits of (n/m).  Output n/m per hit.
                acc += n / size
        # acc/T_a * T_a = acc is sum of (n/m) over hits; expectation = #components in bucket * ...
        # Standard HT: E[ (1/T_a) sum_hits n/m ] = sum_{comp in bucket} (m/n)*(n/m) = #comp.
        est_c_bucket = acc / T_a
        est_components_total += est_c_bucket
        a *= 2
    # persistence increment at scale lam = lam * (number of components at scale lam)
    # (the persistence reframe: Sum_i lam_i c_i).  Here we return lam * c(lam).
    return lam * est_components_total


# --------------------------------------------------------------------------
# Instances
# --------------------------------------------------------------------------
def inst_islands_diagonal(n, lam):
    M = int(round(n / lam)); M = min(M, n)
    islands = np.array([(k * lam + lam / 2, k * lam + lam / 2) for k in range(M)], float)
    m = n - M
    if m > 0:
        s = int(np.ceil(np.sqrt(m)))
        X0 = islands[:, 0].max() + 10 * lam
        xs = np.arange(s); gx, gy = np.meshgrid(xs, xs)
        bulk = np.column_stack([gx.ravel() + X0, gy.ravel()]).astype(float)[:m]
        P = np.vstack([islands, bulk])
    else:
        P = islands
    return P


def inst_dense_gadget(n, rng):
    # ~n^{1/3} coarse cells, one dense heavy block hidden among them; bulk uniform.
    side = max(2, int(round(n ** (1 / 3))))
    grid = side * side
    block = n // 3
    rest = n - block
    # heavy block packed in one coarse cell
    bs = int(np.ceil(np.sqrt(block)))
    gx, gy = np.meshgrid(np.arange(bs), np.arange(bs))
    blk = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:block]
    blk += np.array([5 * side, 5 * side]) * 50.0
    # bulk: uniform over a big grid
    bulk = rng.integers(0, max(2, int(side * 200)), size=(rest, 2)).astype(float)
    return np.vstack([blk, bulk])


def inst_uniform(n, rng):
    side = max(2, int(round(math.sqrt(n) * 3)))
    return rng.integers(0, side, size=(n, 2)).astype(float)


# --------------------------------------------------------------------------
def main():
    eps = 0.3
    L = 8.0
    print("=== Task 1: point-sampling all component sizes, lambda <= n^{1/3} ===")
    print(f"eps={eps}  L={L}\n")
    rng = np.random.default_rng(7)

    for name, builder in [("islands", "islands"), ("dense", "dense"), ("uniform", "uniform")]:
        print(f"--- instance: {name} ---")
        print(f"{'n':>7} {'lam':>6} {'true c(lam)':>11} {'true lam*c':>11} "
              f"{'est lam*c':>10} {'ratio':>7} {'queries':>9} {'n^1/3':>7} {'q/n^1/3':>8}")
        for n in [1024, 4096, 16384]:
            n13 = n ** (1 / 3)
            # choose lambda <= n^{1/3}
            lam = max(2, int(round(n13)))
            if name == "islands":
                P = inst_islands_diagonal(n, lam)
            elif name == "dense":
                P = inst_dense_gadget(n, rng)
            else:
                P = inst_uniform(n, rng)
            P = P.astype(float)
            sizes = exact_components_at_scale(P, lam)
            true_c = len(sizes)
            true_pers = lam * true_c
            oracle = CountingOracle(P)
            est_pers = estimate_persistence_pointsample(oracle, P, lam, eps, L, rng)
            print(f"{n:>7} {lam:>6} {true_c:>11} {true_pers:>11.1f} "
                  f"{est_pers:>10.1f} {est_pers / max(true_pers,1e-9):>7.3f} "
                  f"{oracle.n_queries:>9} {n13:>7.1f} {oracle.n_queries / n13:>8.1f}")
        print()


if __name__ == "__main__":
    main()
