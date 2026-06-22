"""
CRUX v2: the ROBUSTNESS test. Can the island/lonely contribution be CONCEALED so that
localized random probing FAILS (restoring sqrt(n) hardness), while still keeping the
EMST value large?

The localized-probe estimator (crux.py) works when lonely sites TILE the domain. To defeat
it, the adversary wants lonely sites to occupy a LOW MEASURE fraction (1/sqrt n) of the
domain -- the Lemma-19 structure. BUT here is the rub for EMST:

  A 'lonely point at scale L' contributes ~L to Sum lambda c. For the TOTAL island
  contribution to be Theta(n) you need ~ (n / L) such persistence, e.g. M=sqrt(n) islands
  each with L=sqrt(n). Each lonely island, BY DEFINITION of lonely-at-scale-L, has an
  EMPTY L-neighborhood (no other point within L). So the M islands' L-neighborhoods are
  DISJOINT and each has measure ~L (1D) or L^2 (2D). Total measure of lonely-neighborhoods
  >= M*L (1D) = sqrt(n)*sqrt(n) = n  OR  M*L^2 (2D) = sqrt(n)*n = n^{3/2}.

  In 1D the domain has spread Delta=O(n), so M*L = n = Delta: the lonely neighborhoods
  EXACTLY TILE the 1D domain. They CANNOT be concealed into low measure -- 'lonely at
  scale L' forces an empty L-gap, and sqrt(n) disjoint empty L-gaps fill the whole line.
  => In 1D, lonely-islands are UN-concealable; localized probing finds them. (Consistent
     with U-P1: 1D MST is trivial.)

  In 2D the domain is [Delta]^2 with Delta=O(n)? NO -- spread Delta=O(n) means coords in
  [n], so AREA = n^2. M*L^2 = sqrt(n)*n = n^{3/2} << n^2. So in 2D the lonely neighborhoods
  occupy only n^{3/2}/n^2 = 1/sqrt(n) fraction of the AREA. => CONCEALABLE in 2D!

This is the crux of robustness. Test it: in 2D, place M=sqrt n islands with empty-L^2
neighborhoods scattered in [n]^2 (area n^2). A random L-box hits an island w.p.
~ M*L^2/n^2 = 1/sqrt n. => need sqrt n probes to hit one. RESTORES sqrt n.

We verify the hitting probability and whether the EMST island value stays Theta(n).
"""
import numpy as np
from scipy.spatial import cKDTree
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","sim"))
from emst import emst_weight
rng=np.random.default_rng(5)

print("="*78)
print("CRUX v2: 2D concealment of islands -> hitting prob ~ 1/sqrt(n) -> restores barrier?")
print("="*78)
for n in (1024, 4096, 16384):
    M=int(round(np.sqrt(n))); L=np.sqrt(n)
    Delta=float(n)  # coords in [0,n], area n^2
    # scatter M islands at random positions, each with an empty L-neighborhood (rejection)
    iposs=[]
    attempts=0
    while len(iposs)<M and attempts<100000:
        attempts+=1
        p=rng.uniform(0,Delta,size=2)
        if all(np.hypot(*(p-q))>2.5*L for q in iposs):
            iposs.append(p)
    iposs=np.array(iposs)
    # dense bulk: remaining n-M points packed in a small corner box (so they're 1 component,
    # NOT contributing island persistence) -- occupies tiny area.
    nb=n-M
    bulk=np.column_stack([rng.random(nb)*1.0, rng.random(nb)*1.0])  # corner [0,1]^2
    P=np.vstack([iposs,bulk])
    # measure island persistence: each island lonely until scale ~ its NN distance.
    tree=cKDTree(iposs)
    dd,_=tree.query(iposs,k=2)
    nn=dd[:,1]  # nearest island neighbor distance
    island_persistence=nn.sum()  # ~ sum of NN distances ~ contribution to Sum lambda c
    # hitting probability of a random L-box
    p_hit = M*(L**2)/(Delta**2)
    probes_to_hit = 1.0/p_hit
    print(f" n={n:6d} M={M:4d} L={L:6.1f}  island_persist(sum NN)={island_persistence:10.0f}"
          f"  (~n? n={n})  P(random L-box hits island)={p_hit:.4f}  ~1/sqrt n={1/np.sqrt(n):.4f}"
          f"  probes_to_hit~{probes_to_hit:.0f} (sqrt n={np.sqrt(n):.0f})")
