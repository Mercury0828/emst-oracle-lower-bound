"""
PART 4 (decisive): can a range-COUNTING oracle estimate the occupancy histogram
  S_j = #cells with occupancy exactly j   (esp. S_1 = #singleton-occupancy cells,
  N   = sum_{j>=1} S_j = #non-empty cells)
to the additive accuracy importance-sampling needs, WITHOUT the near-uniform
cell-sampling that U-B1 (Lemma 19) forbids?

We reconstruct the Lemma-19 hard family (1D, Delta=n, n unit cells) as quoted in the
round1 audit:
  - UNIFORM instance: ~ n/(4c) non-empty cells.
  - NON-UNIFORM instance(s): ~ 2c*sqrt(n) non-empty cells (hides a 'witness segment').
and ask whether (i) N and (ii) S_1 SEPARATE the two families (=> any estimator of them
to small relative/additive error is also Omega(sqrt n) by the SAME Yao argument), or
whether MST-relevant aggregates collapse.

Crucially we also test the SECOND-MOMENT / inclusion-exclusion route the brief proposes:
  Sigma_cells C(occ,2) = #ordered-pairs-in-same-cell = sum over cells of occ*(occ-1)/2,
which IS obtainable from a single global statistic? NO -- per-cell second moment is NOT a
range count. We check what aggregate range counts actually reveal.
"""
import numpy as np

rng = np.random.default_rng(2024)

def occ_histogram(points_cells, ncells):
    """points_cells: array of cell indices (0..ncells-1). Return occupancy array."""
    occ = np.bincount(points_cells, minlength=ncells)
    return occ

def summarize(occ, label):
    N = int((occ>=1).sum())            # #non-empty cells
    S1 = int((occ==1).sum())           # #singleton-occupancy cells
    npts = int(occ.sum())
    m2 = int((occ*(occ-1)//2).sum())   # sum C(occ,2) = #same-cell pairs
    print(f"  [{label}] npts={npts:7d}  N(non-empty)={N:6d}  S1(occ==1)={S1:6d}  "
          f"sum C(occ,2)={m2:9d}")
    return dict(N=N,S1=S1,npts=npts,m2=m2)

print("="*78)
print("PART 4: Lemma-19 family -- does the occupancy histogram separate uniform vs non-uniform?")
print("="*78)
# Reconstruct per the audit's description:
#   length-n interval, n unit cells, n/(4c) 'segments'.
#   uniform: n/(4c) non-empty cells.
#   non-uniform: ~2c sqrt(n) non-empty cells.
# We realize: total points = n. In the audit's construction the points are placed so the
# two families have the stated #non-empty cells.
# Standard realization (the EMD/needle construction): split [n] into B blocks. 'Segments'
# are the unit cells that receive points. To match counts:
#   uniform: spread points over n/(4c) cells (each gets 4c points) -> N=n/(4c), S1=0 (if 4c>1).
#   non-uniform: spread points over ~2c sqrt(n) cells -> each gets ~ n/(2c sqrt n)=sqrt(n)/(2c) pts.
c = 2.0
for n in (10_000, 1_000_000):
    print(f"\n n={n}, c={c}")
    sqn = int(round(np.sqrt(n)))
    # UNIFORM: N_u = n/(4c) non-empty cells, each with 4c points
    Nu = int(round(n/(4*c)))
    per_u = n // Nu
    cells_u = np.repeat(np.arange(Nu)*4, per_u)[:n]   # spaced out, occupancy per_u each
    # pad if rounding lost points
    if len(cells_u)<n:
        cells_u = np.concatenate([cells_u, np.full(n-len(cells_u), cells_u[-1])])
    occ_u = occ_histogram(cells_u%n, n)
    su = summarize(occ_u, "UNIFORM ")
    # NON-UNIFORM: N_nu ~ 2c sqrt(n) non-empty cells
    Nnu = int(round(2*c*sqn))
    per_nu = n // Nnu
    cells_nu = np.repeat(np.arange(Nnu)*7, per_nu)[:n]
    if len(cells_nu)<n:
        cells_nu = np.concatenate([cells_nu, np.full(n-len(cells_nu), cells_nu[-1])])
    occ_nu = occ_histogram(cells_nu%n, n)
    snu = summarize(occ_nu, "NONUNIF ")
    print(f"   --> N ratio nonunif/unif = {snu['N']/su['N']:.2f}   (Lemma-19: these MUST differ ~ sqrt(n)-fold-ish)")
    print(f"   --> S1: unif={su['S1']} nonunif={snu['S1']}  (both ~0 here: occupancy>1 in both => S1 does NOT separate!)")
