"""
Audit UD - Task 3f: the cleanest decisive test.

Vary c(lam) by a constant fraction at a LARGE lam and ask:
  (i)  does w(MST) move by a constant fraction? (it must, by w = integral (c-1) dt)
  (ii) is the difference COARSELY visible (random lam-box hit-frac constant) => vise holds
       => weight recoverable in Otilde(sqrt(n/lam)) => classification (A)/(B), not (C).

Construction that ACTUALLY changes c(lam) and the weight:
  Domain: a big SQUARE region of side S. Scatter G isolated 'blobs' (each 'a' tight points)
  on a sqrt(G) x sqrt(G) GRID with spacing 2*lam (so each blob is a lam-component; the MST
  connects them with edges ~2lam, total ~ G*2lam).
  A: G = G0 blobs  (c(lam) = G0).      w(MST(A)) ~ G0 * 2lam.
  B: G = G0/2 blobs (remove every other GRID node), same a per blob, but DOUBLE 'a' so total
     n is preserved. c(lam) = G0/2. w(MST(B)) ~ (G0/2)*2lam = half.
  => |wA - wB|/wA ~ 1/2: GENUINE constant-fraction gap driven by c(lam).

  Hard-pair concealment test: A and B differ in which GRID nodes are occupied. Removing
  every-other node => the difference is SPREAD over G0/2 grid cells. A random lam-box hits an
  occupied-in-A-but-not-B cell with prob ~ (G0/2)/(#cells in domain). #cells in the bounding
  box at lam-resolution = (S/lam)^2. For a sqrt(G0) x sqrt(G0) grid at spacing 2lam,
  S = 2lam*sqrt(G0), so (S/lam)^2 = 4 G0 cells, of which G0 occupied in A => hit-frac ~ 1/4.
  CONSTANT hit-frac => coarsely distinguishable => vise holds.

We MEASURE all of this with exact EMST.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree
from emst import emst_weight


def fprint(*a):
    print(*a, flush=True)


def grid_blobs(G, a, lam, rng, decimate=1):
    side = int(round(math.sqrt(G)))
    pts = []
    nodes = 0
    for i in range(side):
        for j in range(side):
            if decimate == 2 and ((i + j) % 2 == 1):
                continue   # remove every other grid node (checkerboard)
            cx, cy = i * 2.0 * lam, j * 2.0 * lam
            pts.append(np.column_stack([cx + rng.uniform(0, lam * 0.02, a),
                                        cy + rng.uniform(0, lam * 0.02, a)]))
            nodes += 1
    return np.vstack(pts), nodes, side


def mst_edges_count_ge(P, lam):
    """#MST edges with length >= lam = c(lam)-1 (robust via emst.py-style)."""
    from scipy.spatial import Delaunay
    pts = np.asarray(P, float); n = len(pts)
    # jitter to avoid degeneracy
    pts = pts + np.random.default_rng(1).uniform(-1e-6, 1e-6, pts.shape)
    if n <= 3:
        iu, ju = np.triu_indices(n, 1); E = np.column_stack([iu, ju])
    else:
        try:
            tri = Delaunay(pts); s = tri.simplices
            E = np.vstack([s[:, [0, 1]], s[:, [1, 2]], s[:, [0, 2]]]); E.sort(axis=1); E = np.unique(E, axis=0)
        except Exception:
            iu, ju = np.triu_indices(n, 1); E = np.column_stack([iu, ju])
    d = pts[E[:, 0]] - pts[E[:, 1]]; w = np.sqrt((d * d).sum(1))
    order = np.argsort(w, kind="stable"); parent = np.arange(n)
    def find(x):
        r = x
        while parent[r] != r: r = parent[r]
        while parent[x] != r: parent[x], x = r, parent[x]
        return r
    used = []
    for idx in order:
        i, j = int(E[idx, 0]), int(E[idx, 1]); ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj; used.append(w[idx])
            if len(used) == n - 1: break
    used = np.array(used)
    return int(np.sum(used >= lam))


def box_hit_frac(A, B, lam, sz, n_boxes, rng):
    tA = cKDTree(A); tB = cKDTree(B)
    lo = min(A.min(), B.min()); hi = max(A.max(), B.max())
    w = sz * lam; nz = 0; md = 0
    for _ in range(n_boxes):
        x0 = rng.uniform(lo - lam, hi); y0 = rng.uniform(lo - lam, hi)
        cA = len(tA.query_ball_point([x0 + w / 2, y0 + w / 2], r=w / 2, p=np.inf))
        cB = len(tB.query_ball_point([x0 + w / 2, y0 + w / 2], r=w / 2, p=np.inf))
        if cA != cB: nz += 1
        md = max(md, abs(cA - cB))
    return md, nz / n_boxes


def main():
    fprint("=== Task 3f: c(lam)-driven constant-fraction gap at large lam, vs the vise ===\n")
    rng = np.random.default_rng(0)
    fprint(f"{'n~':>7} {'lam':>5} {'GA':>5} {'GB':>5} {'cA-1':>6} {'cB-1':>6} "
           f"{'wA':>9} {'wB':>9} {'|dw|/wA':>8} {'n^1/3':>7}")
    pairs = {}
    for G0 in [256, 1024]:
        lam = 50.0
        a = 2
        A, nA, side = grid_blobs(G0, a, lam, rng, decimate=1)
        B, nB, _ = grid_blobs(G0, 2 * a, lam, rng, decimate=2)  # half nodes, double mass/blob
        n_approx = len(A)
        n13 = len(A) ** (1 / 3)
        cA1 = mst_edges_count_ge(A, lam)
        cB1 = mst_edges_count_ge(B, lam)
        wA, wB = emst_weight(A), emst_weight(B)
        pairs[G0] = (A, B, lam)
        fprint(f"{len(A):>7} {lam:>5.0f} {nA:>5} {nB:>5} {cA1:>6} {cB1:>6} "
               f"{wA:>9.0f} {wB:>9.0f} {abs(wA-wB)/wA:>8.3f} {n13:>7.1f}")

    fprint("\nVise test: random lam-box and 2lam-box hit-fraction of the A-vs-B difference.")
    fprint(f"{'G0':>6} {'lam':>5} | 1lam (maxdiff,hitfrac)  2lam (maxdiff,hitfrac)")
    for G0 in [256, 1024]:
        A, B, lam = pairs[G0]
        md1, hf1 = box_hit_frac(A, B, lam, 1, 4000, rng)
        md2, hf2 = box_hit_frac(A, B, lam, 2, 4000, rng)
        fprint(f"{G0:>6} {lam:>5.0f} | 1lam=({md1},{hf1:.3f})   2lam=({md2},{hf2:.3f})")

    fprint("\nREADING: if |dw|/wA ~ const (driven by c(lam) halving) AND the lam-box hit-frac is")
    fprint("CONSTANT, the gap is coarsely visible => O(1/eps^2) boxes distinguish => the large-lam")
    fprint("weight is recoverable WITHOUT per-bucket component counts (just coarse occupancy +")
    fprint("the slab branch). That is classification (A)/(B), NOT (C). The component-COUNT")
    fprint("sub-problem may be sqrt(n)-hard, but the WEIGHT is not.")


if __name__ == "__main__":
    main()
