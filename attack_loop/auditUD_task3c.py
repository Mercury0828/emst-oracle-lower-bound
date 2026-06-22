"""
Audit UD - Task 3c: THE DECISIVE DISTINCTION.

A sub-problem (per-bucket component COUNT at large lam) being sqrt(n)-hard does NOT make
MST-WEIGHT sqrt(n)-hard if the WEIGHT is recoverable another way.

We test the WORKAROUND via persistence telescoping.

Reframe:  w(MST) = (n - Delta) + Sum_i lam_i c_i.
Equivalently (single-linkage / Kruskal):  the MST weight equals the integral over
threshold t of (c(t) - 1), i.e.
     w(MST) = integral_0^infty (c(t) - 1) dt        [the 'cluster-count integral']
where c(t) = #connected components of the single-linkage graph at threshold t.
(Each MST edge of length L keeps the graph at >=2 comps for an extra dt across [0,L].)
Discretized over geometric scales lam_i:  w(MST) ~ Sum_i (lam_{i+1}-lam_i)(c(lam_i)-1).

So we do NOT need per-(lam, size-bucket) component COUNTS. We only need the TOTAL
component count c(lam) at each scale lam -- a single scalar per scale.

KEY: c(lam) = (#points) - (#edges of the MST shorter than lam)
            = n - |{MST edges < lam}|.
So  c(lam) - 1 = (n-1) - |{MST edges < lam}|  = |{MST edges >= lam}|.
And  Sum over scales of (lam_{i+1}-lam_i)*(c(lam_i)-1)
   = Sum over MST edges e of (length of e)   [telescoping] = w(MST).  (sanity)

THE LARGE-lam CONTRIBUTION:  Sum_{lam > t} (c(lam)-1) d lam = Sum_{MST edges e: len(e) > t} (len(e) - t)
                                                              + t * |{edges >= t}| ... etc.
The POINT: the large-lam persistence is governed by the NUMBER OF LONG MST EDGES,
|{MST edges >= lam}| = c(lam) - 1.  This is a single scalar per scale, NOT a per-size-bucket
component count.

Can we estimate the SCALAR c(lam) for large lam (lam > n^{1/3}) in Otilde(sqrt(n/lam))?
c(lam)-1 = #MST edges >= lam = #'merges that happen at scale >= lam'.  At large lam there
are FEW long edges: c(lam) <= n/lam-ish? NO -- c(lam) can be up to n/ (min comp size).
BUT the WEIGHT-relevant quantity Sum_{lam>t} lam*(c(lam)) is dominated by ... let's just
TEST numerically whether estimating the SCALAR c(lam) for large lam is easier than the
per-bucket count, and whether the dense-slab hard instance makes c(lam) (hence weight) hard.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree
from emst import emst_weight


def fprint(*a):
    print(*a, flush=True)


def mst_edge_lengths(P):
    """Exact MST edge lengths via Delaunay+Kruskal (mirror emst.py but return lengths)."""
    from scipy.spatial import Delaunay
    pts = np.asarray(P, float)
    n = len(pts)
    if n <= 1:
        return np.array([])
    if n <= 3:
        iu, ju = np.triu_indices(n, 1)
        E = np.column_stack([iu, ju])
    else:
        tri = Delaunay(pts)
        s = tri.simplices
        E = np.vstack([s[:, [0, 1]], s[:, [1, 2]], s[:, [0, 2]]])
        E.sort(axis=1)
        E = np.unique(E, axis=0)
    d = pts[E[:, 0]] - pts[E[:, 1]]
    w = np.sqrt((d * d).sum(1))
    order = np.argsort(w, kind="stable")
    parent = np.arange(n)

    def find(x):
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != r:
            parent[x], x = r, parent[x]
        return r
    used = []
    for idx in order:
        i, j = int(E[idx, 0]), int(E[idx, 1])
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            used.append(w[idx])
            if len(used) == n - 1:
                break
    return np.array(used)


def c_of_lam(edge_lengths, n, lam):
    """c(lam) = n - #MST edges < lam."""
    return n - int(np.sum(edge_lengths < lam))


def inst_dense_slab_hidden(n, lam, a):
    rng = np.random.default_rng(0)
    K = max(1, int((n * 0.5) / a))
    ys = (np.arange(K) * 2.0 * lam).repeat(a)
    jitter = rng.uniform(0, lam * 0.05, size=(K * a, 2))
    cl = np.column_stack([jitter[:, 0], ys + jitter[:, 1]])
    rest = n - len(cl)
    if rest > 0:
        ybulk_base = ys.max() + 10 * lam
        s = int(np.ceil(np.sqrt(rest)))
        gx, gy = np.meshgrid(np.linspace(0, lam * 0.9, s), np.linspace(0, lam * 0.9, s))
        bulk = np.column_stack([gx.ravel(), gy.ravel() + ybulk_base]).astype(float)[:rest]
        P = np.vstack([cl, bulk])
    else:
        P = cl
    return P, K


def main():
    fprint("=== Task 3c: is large-lam MST-WEIGHT recoverable WITHOUT per-bucket comp counts? ===\n")

    fprint("(1) Verify the cluster-count integral identity: w(MST) = integral (c(t)-1) dt")
    fprint("    = Sum over MST edges of length.  And c(lam)-1 = #MST edges >= lam.\n")
    rng = np.random.default_rng(1)
    for n in [500, 2000]:
        P = rng.random((n, 2)) * 1000
        el = mst_edge_lengths(P)
        w = el.sum()
        # reconstruct via integral of (c(t)-1) over a fine grid
        ts = np.linspace(0, el.max() + 1, 20000)
        integ = 0.0
        for k in range(len(ts) - 1):
            c = c_of_lam(el, n, ts[k])
            integ += (c - 1) * (ts[k + 1] - ts[k])
        fprint(f"  n={n:5d}  w(MST)={w:10.1f}  integral(c-1)dt={integ:10.1f}  ratio={integ/w:.4f}")

    fprint("\n(2) THE DENSE-SLAB HARD INSTANCE: per-bucket comp count is hard (3-B).")
    fprint("    But what is the LARGE-lam WEIGHT contribution, and is it recoverable from")
    fprint("    the SCALAR c(lam) (which = n - #short MST edges)?\n")
    fprint(f"{'n':>7} {'lam':>6} {'true K':>7} {'c(lam)':>8} {'#edges>=lam':>11} "
           f"{'large-lam wt frac':>17}")
    for n in [4096, 16384]:
        n13 = n ** (1 / 3)
        lam = int(round(4 * n13))
        a = 4
        P, K = inst_dense_slab_hidden(n, lam, a)
        el = mst_edge_lengths(P)
        w = el.sum()
        c = c_of_lam(el, n, lam)
        nlong = int(np.sum(el >= lam))
        large_wt = el[el >= lam].sum()
        fprint(f"{n:>7} {lam:>6} {K:>7} {c:>8} {nlong:>11} {large_wt/max(w,1e-9):>17.4f}")

    fprint("\n(3) CRUX: does the dense-slab hard instance actually make w(MST) hard, or is the")
    fprint("    weight tiny / coarsely-recoverable?  In the 3-B instance the K a-clusters are")
    fprint("    FAR in y from bulk: each a-cluster is a separate component until a LONG edge")
    fprint("    connects it. Let's see if the long edges (the weight) are FEW and LOCATABLE.")
    fprint(f"{'n':>7} {'lam':>6} {'#edges>=lam':>11} {'#edges>=2lam':>12} {'maxedge/lam':>11}")
    for n in [4096, 16384]:
        n13 = n ** (1 / 3)
        lam = int(round(4 * n13))
        a = 4
        P, K = inst_dense_slab_hidden(n, lam, a)
        el = mst_edge_lengths(P)
        fprint(f"{n:>7} {lam:>6} {int(np.sum(el>=lam)):>11} {int(np.sum(el>=2*lam)):>12} "
               f"{el.max()/lam:>11.2f}")


if __name__ == "__main__":
    main()
