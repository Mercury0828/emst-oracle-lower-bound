"""
Audit UD - Task 3: THE DECISIVE PART. large-lambda (lam > n^{1/3}) component counting.

We test the central tension cleanly and FAST.

Claim:  for lam > n^{1/3}, size bucket [a,2a), estimate #G_lam-components of that size
to additive O(eps n/(lam L)) with Otilde(sqrt(n/lam)) range-counting queries.

codex objection: in a DENSE slab the target components are a tiny mass fraction =>
Horvitz-Thompson variance reverts to point-sampling cost Theta(lam/a).

Two regimes:
 (3-A) SPARSE: components are isolated singletons/small clusters; slab-locate works,
       #nonempty slabs = c_lam ~ n/lam, sqrt-search => sqrt(n/lam).
 (3-B) DENSE: small target clusters hidden among heavy bulk; per-slab the target mass
       fraction is tiny.

DECISIVE reframe (the orchestrator hint): use PERSISTENCE TELESCOPING. We do NOT need
per-(lam,a) component counts; we need the total LARGE-lam persistence
   Sum_{lam > n^{1/3}}  lam * c_lam .
c_lam = number of connected components at threshold lam. We show:
  (i) at large lam, c_lam is SMALL (<= n/lam_min_comp_size) and DECREASING;
  (ii) the large-lam persistence = Sum_{lam>t} lam*(c_lam) relates to the EMST weight
       of the points ABOVE scale t, i.e. the contribution of long edges, which is
       recoverable WITHOUT per-bucket component counts.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree


def fprint(*a):
    print(*a, flush=True)


class CountingOracle:
    def __init__(self, P):
        self.P = np.asarray(P, float)
        self.n_queries = 0
        self.order = np.argsort(self.P[:, 0], kind="stable")
        self.xs = self.P[self.order, 0]
        self.ys = self.P[self.order, 1]

    def count(self, x0, x1, y0, y1):
        self.n_queries += 1
        lo = np.searchsorted(self.xs, x0, side="left")
        hi = np.searchsorted(self.xs, x1, side="right")
        sub = self.ys[lo:hi]
        return int(np.sum((sub >= y0) & (sub <= y1)))


def comp_sizes_at_scale(P, lam):
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
    if len(pairs):
        for i, j in pairs:
            ri, rj = find(int(i)), find(int(j))
            if ri != rj:
                parent[ri] = rj
    roots = np.array([find(k) for k in range(len(P))])
    _, sizes = np.unique(roots, return_counts=True)
    return sizes


# ---------------------------------------------------------------------------
# (3-A) sparse islands: estimate #nonempty width-lam slabs by random slab sampling.
# This is the *slab branch* primitive. Cost target sqrt(n/lam).
# ---------------------------------------------------------------------------
def inst_sparse_islands(n, lam):
    M = int(round(n / lam)); M = min(M, n)
    spacing = 2.0 * lam
    isl = np.array([(k * spacing, k * spacing) for k in range(M)], float)
    m = n - M
    if m > 0:
        s = int(np.ceil(np.sqrt(m)))
        X0 = isl[:, 0].max() + 10 * lam
        gx, gy = np.meshgrid(np.arange(s), np.arange(s))
        bulk = np.column_stack([gx.ravel() + X0, gy.ravel()]).astype(float)[:m]
        P = np.vstack([isl, bulk])
    else:
        P = isl
    return P, M


def slab_count_estimator(oracle, P, lam, budget, rng):
    """Estimate #nonempty width-lam slabs over the islands' x-range by random probing."""
    xlo, xhi = P[:, 0].min(), P[:, 0].max()
    M = max(1, int(math.ceil((xhi - xlo) / lam)))
    hits = 0
    for _ in range(budget):
        s = rng.integers(0, M)
        x0 = xlo + s * lam
        c = oracle.count(x0, x0 + lam, P[:, 1].min(), P[:, 1].max())
        if c >= 1:
            hits += 1
    return hits / budget * M


# ---------------------------------------------------------------------------
# (3-B) dense slab: small clusters hidden among heavy bulk in ONE x-slab.
# Build efficiently (vectorized).
# ---------------------------------------------------------------------------
def inst_dense_slab_hidden(n, lam, a, frac_clusters=0.5):
    """ONE dense x-slab of width lam. It contains K small clusters (each 'a' points,
    a lam-component of size a) stacked in y, PLUS heavy bulk in the SAME x-slab so the
    clusters are a tiny mass fraction. Everything is in x in [0,lam)."""
    rng = np.random.default_rng(0)
    K = max(1, int((n * frac_clusters) / a))
    # clusters: K groups of 'a' tight points, separated by > lam in y
    ys = (np.arange(K) * 2.0 * lam).repeat(a)
    jitter = rng.uniform(0, lam * 0.05, size=(K * a, 2))
    cl = np.column_stack([jitter[:, 0], ys + jitter[:, 1]])
    used = len(cl)
    rest = n - used
    if rest > 0:
        # heavy bulk: dense points in the SAME x-slab [0,lam), but in y-gaps between
        # clusters AND beyond, so bulk merges into ONE big component (size huge) and the
        # 'a'-clusters that stay separate (placed in their own y with >lam gap to bulk)
        # remain size-a. To keep clusters size-a we put bulk far in y.
        ybulk_base = ys.max() + 10 * lam
        s = int(np.ceil(np.sqrt(rest)))
        gx, gy = np.meshgrid(np.linspace(0, lam * 0.9, s), np.linspace(0, lam * 0.9, s))
        bulk = np.column_stack([gx.ravel(), gy.ravel() + ybulk_base]).astype(float)[:rest]
        P = np.vstack([cl, bulk])
    else:
        P = cl
    return P, K


def main():
    fprint("=== Task 3: large-lambda component counting ===\n")

    # ---------- (3-A) sparse: slab branch works ----------
    fprint("(3-A) SPARSE islands: slab-count estimator, budget = 8 sqrt(n/lam) log n")
    fprint(f"{'n':>7} {'lam':>6} {'n^1/3':>7} {'true #slabs':>11} {'est':>8} {'ratio':>6} "
           f"{'queries':>8} {'sqrt(n/lam)':>11} {'q/sqrt':>7}")
    rng = np.random.default_rng(5)
    for n in [4096, 16384, 65536]:
        n13 = n ** (1 / 3)
        lam = int(round(4 * n13))
        P, M = inst_sparse_islands(n, lam)
        oracle = CountingOracle(P)
        sq = math.sqrt(n / lam)
        budget = int(8 * sq * math.log2(n))
        est = slab_count_estimator(oracle, P, lam, budget, rng)
        fprint(f"{n:>7} {lam:>6} {n13:>7.1f} {M:>11} {est:>8.1f} {est/max(M,1):>6.3f} "
               f"{oracle.n_queries:>8} {sq:>11.1f} {oracle.n_queries/sq:>7.1f}")

    # ---------- (3-B) dense: does slab COUNT identify component count? ----------
    fprint("\n(3-B) DENSE slab: K small a-clusters hidden among heavy bulk in ONE x-slab.")
    fprint("    The whole stratum is in x in [0,lam): ONE non-empty x-slab. A slab COUNT")
    fprint("    of that slab returns ~n (huge), giving NO information about K = #a-clusters.")
    fprint("    To get K you must resolve y-structure inside the slab.")
    fprint(f"{'n':>7} {'lam':>6} {'a':>4} {'true K(=#a-comp)':>16} {'slab count':>11} "
           f"{'lam/a (pt cost)':>15} {'sqrt(n/lam)':>11}")
    for n in [4096, 16384]:
        n13 = n ** (1 / 3)
        lam = int(round(4 * n13))
        a = 4
        P, K = inst_dense_slab_hidden(n, lam, a)
        sizes = comp_sizes_at_scale(P, lam)
        true_K = int(np.sum((sizes >= a) & (sizes < 2 * a)))
        oracle = CountingOracle(P)
        slabc = oracle.count(0, lam, P[:, 1].min(), P[:, 1].max())
        fprint(f"{n:>7} {lam:>6} {a:>4} {true_K:>16} {slabc:>11} "
               f"{lam/a:>15.1f} {math.sqrt(n/lam):>11.1f}")

    fprint("\nREADING(3-B): the x-slab count alone cannot separate the K a-clusters from bulk;")
    fprint("inside the slab you must do y-subdivision. y-subdivision into width-lam y-slabs")
    fprint("= a SECOND slab axis: #nonempty (x,y) lam-cells containing an a-cluster = K.")
    fprint("If K is large (~n/a) and clusters are interleaved with bulk in y, you cannot tell")
    fprint("an a-cluster cell from a bulk-edge cell by COUNT alone -> need local exploration")
    fprint("(point-sampling cost lam/a). THIS is codex's reversion. Next: task3c weight-hardness.")


if __name__ == "__main__":
    main()
