"""
Audit B - Escape A: SPARSE PLACEMENT (do not tile the full domain).

Solver's backbone LB w(P) >= c0*s*m requires cells tiling [Delta]^2 with Delta=ks.
What if we pack the m cells into a SMALL sub-region (side L << Delta)? Then the
backbone shrinks. But does the gap survive, and does the *fraction* rise above sqrt(p)/m?

Key counter-pressure to test: shrinking the packed region forces cells closer, so cell
side s must shrink too (cells of side s, k x k of them, packed in side L => s = L/k).
A smaller s shrinks the heavy gadget's EMST (~ s*sqrt(p)) PROPORTIONALLY. Does s cancel?

We DECOUPLE: keep heavy gadget at a FIXED large physical scale s_h (its own cell can be
large), but pack the *centers* into a region of side L. I.e. ask: is there ANY freedom
in (region size L, cell side s) that raises gap/w above sqrt(p)/m?

We test three layouts at the target p~m regime:
  (1) TILING (baseline): centers fill [Delta]^2, Delta=ks.
  (2) CLUSTERED centers: centers packed in side L = Delta/t (t>1 shrink factor),
      cell footprint s also = L/k (cells shrink with region).
  (3) CLUSTERED centers, cell footprint FIXED at original s (cells overlap-packed densely
      but gadget keeps large internal scale) -- the 'cheat' attempt.
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from emst import emst_weight


def heavy_grid(p, s, off):
    side = int(round(math.sqrt(p)))
    sp = s * 0.98 / side
    xs, ys = np.meshgrid(np.arange(side) * sp, np.arange(side) * sp)
    pts = np.column_stack([xs.ravel(), ys.ravel()])[:p]
    return pts + off


def sparse_strip(p, s, off):
    xs = np.linspace(0, s * 0.98, p)
    return np.column_stack([xs, np.full(p, s * 0.5)]) + off


def centers_in_region(k, L):
    c = (np.arange(k) + 0.5) * (L / k)
    xs, ys = np.meshgrid(c, c)
    return np.column_stack([xs.ravel(), ys.ravel()])


def build(centers, s, p, heavy_idx):
    blocks = []
    for i, c in enumerate(centers):
        off = c - np.array([s / 2, s / 2])
        blocks.append(heavy_grid(p, s, off) if i == heavy_idx else sparse_strip(p, s, off))
    return np.vstack(blocks)


def trial(k, p, L, s, label):
    centers = centers_in_region(k, L)
    Ps = build(centers, s, p, -1)
    Ph = build(centers, s, p, 0)
    ws, wh = emst_weight(Ps), emst_weight(Ph)
    frac = (wh - ws) / ws if ws > 0 else float("inf")
    print(f"[{label}] k={k} p={p} L={L:.0f} s={s:.1f} | w_s={ws:.3e} w_h={wh:.3e} "
          f"gap_frac={frac:.4f}")
    return frac


if __name__ == "__main__":
    for k in (6, 8, 10):
        p = k * k
        m = k * k
        Delta = float(m * p)        # n
        s_tile = Delta / k          # tiling cell side
        print(f"\n=== k={k} m=p={m} n={int(Delta)} ; tiling s={s_tile:.0f} ===")
        # (1) tiling baseline
        trial(k, p, Delta, s_tile, "TILE")
        # (2) clustered centers, cells shrink with region (t = 4x shrink)
        for t in (2.0, 4.0, 8.0):
            L = Delta / t
            s = L / k
            trial(k, p, L, s, f"CLUSTER t={t} (cells shrink, s={s:.0f})")
        # (3) clustered centers but KEEP large cell footprint (gadget overlaps neighbors!)
        #     -- only physically valid if footprints don't collide; here we shrink region
        #        but keep s=s_tile to see if decoupling helps the FRACTION (ignoring overlap).
        for t in (2.0, 4.0):
            L = Delta / t
            trial(k, p, L, s_tile, f"DECOUPLE t={t} (region/{t}, s=tile -- footprints overlap!)")
