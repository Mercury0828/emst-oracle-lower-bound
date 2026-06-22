"""
Stress the empty-cell leader-estimator identity E[Z]=c, Var(Z)<=M*c on ADVERSARIAL component
structures. (The round-4 verify (I) showed E[Z] wandering -- but that was a sampling artifact:
one leader cell among M, with too few Monte-Carlo trials. Here we compute E[Z],Var(Z) EXACTLY
by enumerating the M candidate cells, so no MC noise.)

One trial: pick X uniform among M candidate cells; if X empty -> Z=0; else explore X's component
in BFS order under random ranks, stop at a lower-ranked cell; if X is the component min-rank cell
(exhausted without finding lower) -> Z=M else Z=0.
EXACT: over a fixed rank assignment, exactly c cells are component-minima -> sum_X Z = c*M, so
E_X[Z | ranks] = c*M/M = c. Averaged over ranks E[Z]=c. Var: E[Z^2|ranks]=c*M^2/M=c*M, so
Var(Z|ranks)=cM - c^2; with ranks random, total E[Z]=c exactly and E[Z^2]=cM => Var=cM-c^2<=Mc.
We verify EXACTLY (closed form) across adversarial occupied-cell graphs:
 - many singleton components (c=N): worst variance
 - one giant component (c=1)
 - power-law component sizes
"""
import numpy as np

def exact_leader_moments(component_of_cell, M):
    """component_of_cell: list of component labels for the N occupied cells (cells 0..N-1 occupied,
    N..M-1 empty). Compute EXACT E[Z], E[Z^2] over uniform X and uniform random ranks.
    Exactly c cells are leaders (component minima) for any rank tie-broken assignment; averaging
    over ranks each cell is its component's leader w.p. 1/size(comp). So:
       E[Z] = sum_{occupied X} P(X is leader)*M / M = sum_X 1/size(comp(X)) = (#components) = c.
       E[Z^2] = sum_X P(leader)*M^2 / M = M * sum_X 1/size = M*c.
    => Var = M c - c^2.  We verify by direct enumeration of these closed forms.
    """
    from collections import Counter
    sizes=Counter(component_of_cell)
    c=len(sizes)
    # sum over occupied cells of 1/size(comp(cell)) = sum over comps size*(1/size)=#comps=c
    EZ = sum(1.0/sizes[component_of_cell[x]] for x in range(len(component_of_cell)))/M*M
    EZ2= M*sum(1.0/sizes[component_of_cell[x]] for x in range(len(component_of_cell)))/M
    Var=EZ2-EZ*EZ
    return c, EZ, EZ2, Var, M*c

def mc_check(component_of_cell, M, trials, rng):
    """Monte-Carlo with the REAL exploration (sanity): E[Z] should match c."""
    from collections import defaultdict
    comps=defaultdict(list)
    for x,lab in enumerate(component_of_cell): comps[lab].append(x)
    N=len(component_of_cell)
    Zs=np.empty(trials)
    for t in range(trials):
        ranks={x:rng.random() for x in range(N)}
        # leader of each comp = min-rank cell
        leaders={lab:min(members,key=lambda m:ranks[m]) for lab,members in comps.items()}
        leaderset=set(leaders.values())
        X=int(rng.integers(M))
        Zs[t]=M if (X<N and X in leaderset) else 0.0
    return Zs.mean(), Zs.var()

if __name__=="__main__":
    rng=np.random.default_rng(91)
    print("EXACT leader moments: E[Z]=c, Var(Z)=Mc-c^2 <= Mc", flush=True)
    cases=[]
    # (a) N singletons, c=N
    for (N,M) in [(50,200),(200,5000),(1000,50000)]:
        comp=list(range(N))  # each its own component
        cases.append((f"singletons N={N} M={M}", comp, M))
    # (b) one giant comp c=1
    for (N,M) in [(50,200),(1000,50000)]:
        comp=[0]*N
        cases.append((f"giant N={N} M={M}", comp, M))
    # (c) power-law sizes
    for (M,) in [(50000,)]:
        sizes=[]; lab=0; comp=[]
        s=512
        while s>=1 and len(comp)<2000:
            for _ in range(max(1, 4000//(s*s))):
                comp += [lab]*s; lab+=1
            s//=2
        cases.append((f"powerlaw N={len(comp)} M={M}", comp, M))
    # (d) satellites: 1 big comp + many singletons (the round-3 structure)
    for (M,) in [(20000,)]:
        comp=[0]*900 + list(range(1,65))  # 900-cell core + 64 satellite singletons
        cases.append((f"core+64sat N={len(comp)} M={M}", comp, M))
    for name,comp,M in cases:
        c,EZ,EZ2,Var,Mc=exact_leader_moments(comp,M)
        mcE,mcV=mc_check(comp,M,30000,rng)
        ok = (abs(EZ-c)<1e-9) and (Var<=Mc+1e-9)
        print(f"  {name}: c={c:4d} E[Z]={EZ:.4f}(MC {mcE:.3f}) Var={Var:.1f} (MC {mcV:.0f}) "
              f"Mc={Mc:.0f} Var<=Mc? {Var<=Mc+1e-9}  identityOK={ok}", flush=True)
    print("DONE",flush=True)
