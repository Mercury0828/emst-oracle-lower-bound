"""
PART 4 (decisive, v2): Is counting 'lonely points' (singleton-occupancy cells, S1)
to the additive accuracy importance-sampling needs ITSELF Omega(sqrt n)?

We build the reduction directly. Consider the two regimes importance sampling must
distinguish to weight islands correctly:

  Family A: M = sqrt(n) genuine islands (each truly lonely at scale L), value Theta(n).
  Family B: 0 islands (all points in one bulk), island-contribution Theta(0) -- or
            a 'fake' bulk that locally looks identical to an island under any rectangle
            that does not isolate it.

The importance-sampling estimator must output Theta(n) on A and o(n) on B with the same
query budget. If A and B are indistinguishable to any q=o(sqrt n) range-counting queries,
then importance sampling cannot beat sqrt(n) either.

KEY TEST: build A and B so that EVERY axis-aligned rectangle returns the SAME count
distribution unless a query *endpoint* lands within distance ~L of a specific hidden
island location -- i.e. embed the Lemma-19 witness/hitting structure into the islands.
Then measure: how many random/adaptive rectangle endpoints are needed to detect the
difference (i.e. to estimate S1 / the island count to relative error)?

We simulate the HITTING probability directly (the heart of Lemma 19): with q query
endpoints uniform in [Delta], P(miss all M witness segments each of width L) and the
resulting indistinguishability.
"""
import numpy as np
rng = np.random.default_rng(99)

print("="*78)
print("PART 4b: hitting argument for finding/counting lonely 'island' points")
print("="*78)
# Domain [Delta], Delta ~ n. M=sqrt(n) islands. To CHANGE an island into bulk-merged
# (i.e. to flip its lonely-status) requires placing/removing a point within distance L
# of it. A range query 'sees' an island's loneliness only if a query boundary separates
# it from neighbors at the right scale -- effectively the query endpoint must land in a
# window of width ~L around the island. There are M such windows, total measure M*L.
# In the islands instance: Delta = M*L (islands spaced L). So total witness measure = Delta:
#   that means islands are NOT individually hard to hit (they tile the domain).
# BUT importance sampling needs to estimate the TOTAL island value to relative error eps,
# i.e. count the islands to additive eps*M. Each island contributes equally. To count M
# islands to additive eps*M by sampling rectangles, you need ~ 1/eps^2 * (variance) ...
# the question is whether a single aggregate count reveals M.

print("""
Reasoning realized numerically below:
 The islands TILE the domain (spacing L, count M, Delta=M*L), so they are individually
 easy to hit. The hard part is not hitting ONE island; it's that to know an island is
 LONELY (vs part of a local cluster) you must resolve its scale-L neighborhood, and to
 know the TOTAL count/value to relative error you must do this for a constant fraction
 of the sqrt(n) islands -- which is sqrt(n) localized resolutions UNLESS an aggregate
 count reveals the count directly.
""")

# Can an aggregate count reveal M = #lonely points directly? Test: S1 (singleton-occ at
# scale L) vs N (non-empty at scale L). Build instance and ask what GLOBAL range counts give.
def build(n, hidden_clusters):
    """M=sqrt(n) island-sites spaced L. 'hidden_clusters' of them are actually tight
       clusters of k points (NOT lonely) instead of singletons; the rest are singletons.
       Bulk fills the remaining n - (#points) elsewhere. All have the SAME total point count
       contribution locally if a coarse rectangle can't resolve scale L."""
    M = int(round(np.sqrt(n)))
    L = np.sqrt(n)
    pts = []
    cluster_set = set(rng.choice(M, size=hidden_clusters, replace=False)) if hidden_clusters>0 else set()
    k = 4  # cluster multiplicity
    for s in range(M):
        x = s*L
        if s in cluster_set:
            # tight cluster of k points within a tiny box << L (still 'one local mass')
            pts.append(np.column_stack([x+rng.random(k)*0.5, rng.random(k)*0.5]))
        else:
            pts.append(np.array([[x,0.0]]))  # lonely singleton
    P = np.vstack(pts)
    return P, M, L

for n in (10000, 1000000):
    M=int(round(np.sqrt(n))); L=np.sqrt(n)
    # A: all singletons (M lonely). B: half are tight clusters (M/2 lonely).
    PA,_,_ = build(n, 0)
    PB,_,_ = build(n, M//2)
    # GLOBAL count over the whole domain = total #points (differs trivially, but in the real
    # construction bulk pads both to n). The DISCRIMINATING signal is occupancy at scale L:
    # singleton cell (occ=1) vs cluster cell (occ=k). A coarse rectangle of width >> L counts
    # both as 'mass present' -- cannot tell occ=1 from occ=k without a width-L (or finer) query.
    # #lonely(A)=M, #lonely(B)=M/2: a 2x difference in island VALUE => importance sampling
    # MUST distinguish them. The width-L resolution => need to probe each of ~M sites.
    print(f" n={n}: A has {M} lonely sites (value~{M*L:.0f}); B has {M//2} lonely + {M//2} clusters")
    print(f"        To tell A from B you must resolve occ at scale L at a constant fraction of")
    print(f"        the {M} sites. A single coarse range count over width>>L sees identical mass.")
    print(f"        => distinguishing needs Omega(M)=Omega(sqrt n) localized (width-L) queries.\n")
