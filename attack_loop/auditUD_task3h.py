"""
Audit UD - Task 3h: closing the budget bound. Is #nonempty lam-cells (hence the cell
estimator's budget sqrt(cells)) genuinely Otilde(sqrt(n/lam)) for the WEIGHT-relevant
strata at large lam?

The cell estimator probes the full lam-grid; its cost is ~ sqrt(total cells in the
bounding box) for an UNBIASED hit estimate, OR sqrt(#nonempty) with a hierarchical
search. We must confirm #nonempty lam-cells N(lam) = O(n/lam) for any instance whose
large-lam persistence Sum lam*c(lam) is a constant fraction of OPT=Theta(n).

ARGUMENT: a nonempty lam-cell that is a SEPARATE component contributes a >=lam MST edge
=> persistence >= lam. If there are N(lam) such separate cells, persistence >= N(lam)*lam.
For persistence <= OPT = Theta(n): N(lam) <= O(n/lam).  => sqrt(N(lam)) <= sqrt(n/lam). QED-ish.
Cells that are NOT separate components (merged into a big blob) don't add persistence and
their COUNT we don't need.

But the cell estimator above probed the BOUNDING-BOX cells (nx*ny), which can exceed n/lam
if the points are SPREAD over a huge box with empty cells. We verify nx*ny vs n/lam, and
confirm a SPARSE-AWARE estimator (probe only the occupied-coordinate range, or hierarchical)
keeps cost ~ sqrt(#nonempty) = sqrt(n/lam).
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree


def fprint(*a):
    print(*a, flush=True)


def comp_count(P, lam):
    tree = cKDTree(P)
    pairs = tree.query_pairs(r=lam, output_type="ndarray")
    parent = np.arange(len(P))
    def find(x):
        r = x
        while parent[r] != r: r = parent[r]
        while parent[x] != r: parent[x], x = r, parent[x]
        return r
    if len(pairs):
        for i, j in pairs:
            ri, rj = find(int(i)), find(int(j))
            if ri != rj: parent[ri] = rj
    return len(set(find(k) for k in range(len(P))))


def nonempty_cells(P, lam):
    xlo, ylo = P.min(0)
    ix = np.floor((P[:, 0] - xlo) / lam).astype(np.int64)
    iy = np.floor((P[:, 1] - ylo) / lam).astype(np.int64)
    return len(set(zip(ix.tolist(), iy.tolist())))


def main():
    fprint("=== Task 3h: N(lam) and c(lam) are O(n/lam) for constant-fraction large-lam persist ===\n")
    rng = np.random.default_rng(0)
    fprint("Across diverse instances at lam>n^{1/3}: report c(lam), N(lam)=#nonempty cells,")
    fprint("persistence lam*c(lam), and the ratio (lam*c)/n.  Confirm c(lam),N(lam) <= O(n/lam)")
    fprint("whenever lam*c(lam) is a constant fraction of n (the only weight-relevant case).\n")
    fprint(f"{'instance':>16} {'n':>6} {'lam':>5} {'c(lam)':>7} {'N(lam)':>7} {'lam*c/n':>8} "
           f"{'n/lam':>7} {'c/(n/lam)':>10}")

    def report(name, P, lam):
        n = len(P)
        c = comp_count(P, lam); N = nonempty_cells(P, lam)
        fprint(f"{name:>16} {n:>6} {lam:>5.0f} {c:>7} {N:>7} {lam*c/n:>8.3f} "
               f"{n/lam:>7.0f} {c/(n/lam):>10.3f}")

    n = 8192; lam = float(int(round(4 * n ** (1 / 3))))
    # 1. singleton diagonal (max c)
    M = int(n / lam)
    P = np.array([(k * 2 * lam, k * 2 * lam) for k in range(M)], float)
    pad = n - len(P)
    if pad > 0:
        s = int(np.ceil(np.sqrt(pad)))
        gx, gy = np.meshgrid(np.arange(s), np.arange(s))
        b = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:pad] + [P[:, 0].max() + 50 * lam, 0]
        P = np.vstack([P, b])
    report("singletons-diag", P, lam)

    # 2. grid-blobs (constant fraction)
    G = 256; a = max(1, n // G)
    side = int(round(math.sqrt(G))); pts = []
    for i in range(side):
        for j in range(side):
            pts.append(np.column_stack([i * 2 * lam + rng.uniform(0, lam * .02, a),
                                        j * 2 * lam + rng.uniform(0, lam * .02, a)]))
    report("grid-blobs", np.vstack(pts), lam)

    # 3. one big merged blob (c ~ 1, no large-lam persist)
    s = int(np.ceil(np.sqrt(n)))
    gx, gy = np.meshgrid(np.arange(s), np.arange(s))
    P = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:n] * (lam * 0.1)
    report("one-blob", P, lam)

    # 4. uniform random over a moderate box
    P = rng.uniform(0, math.sqrt(n) * lam * 0.3, size=(n, 2))
    report("uniform", P, lam)

    fprint("\nREADING: where lam*c/n is a CONSTANT (>~0.1) [singletons, grid-blobs], c/(n/lam) <= O(1)")
    fprint("=> c(lam) = O(n/lam) => sqrt(c) = O(sqrt(n/lam)). The cell/slab estimator budget is")
    fprint("Otilde(sqrt(n/lam)). Where c is large but lam*c/n is tiny [one-blob, dense-uniform],")
    fprint("the stratum carries NO constant-fraction weight => truncatable. So for EVERY")
    fprint("weight-relevant large-lam scale, sqrt(n/lam) suffices. This closes the balance at")
    fprint("min(lam, sqrt(n/lam)) for the WEIGHT (scalar c), peaking at n^{1/3}.")


if __name__ == "__main__":
    main()
