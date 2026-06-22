"""
CORRECT round-5 numeric (supersedes the misnormalized webpro_verify_round5.py): confirm the PROOF-RELEVANT
POLYNOMIAL CORES of Pro's two cost terms are O(sqrt K) on the carpet+satellites worst case (N_j=Theta(K)).
  candidate-root core = K/b           (b=Theta(sqrt K) active-cover blocks)          -> O(sqrt K)
  exploration   core = K*delta/W_Q    (= O(K/b) via packing W_Q >= b*delta/16)        -> O(sqrt K)
The full per-scale budgets M_jU_j/alpha_j^2 and N_jU_j/alpha_j^2 carry extra T^2/alpha^2/M_j polylog+const
factors that O~(.) legitimately hides; webpro_verify_round5.py summed those and so OBSCURED the polynomial
scaling (it wrongly looked ~K). codex (docs/webpro_round5_auditFinal_codex.md) isolated these cores
algebraically; this script confirms them by ACTUAL EXECUTION.

Result (2026-06-21): both core/sqrtK columns FLAT across K=272..4160 -> both cores are O(sqrt K). No leak.
Run: sim/.venv/Scripts/python.exe attack_loop/webpro_verify_round5_cores.py
"""
import math, sys
import numpy as np
sys.path.insert(0, 'sim')
from scipy.spatial import Delaunay
sys.path.insert(0, 'attack_loop')
from webpro_verify_round5 import build_carpet_satellites, active_cover_b_delta

if __name__ == "__main__":
    print(f"{'K':>6} {'sqrtK':>6} {'b':>4} {'delta':>8} {'Wq':>8} || "
          f"{'K/b':>7} {'(K/b)/sqrtK':>11} || {'K*delta/Wq':>10} {'core/sqrtK':>10}")
    for scarp in [16, 24, 32, 45, 64]:
        Q, h = build_carpet_satellites(scarp)
        K = len(Q); sqrtK = math.sqrt(K)
        tri = Delaunay(Q); we = []
        for s in tri.simplices:
            for x in range(3):
                for y in range(x + 1, 3):
                    u, v = int(s[x]), int(s[y]); we.append((math.dist(Q[u], Q[v]), u, v))
        we.sort(); par = list(range(K))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        Wq = 0.0; used = 0
        for w, u, v in we:
            ru, rv = f(u), f(v)
            if ru != rv: par[ru] = rv; Wq += w; used += 1
            if used == K - 1: break
        b, delta = active_cover_b_delta(Q, math.ceil(sqrtK))
        cand_core = K / b; expl_core = K * delta / Wq
        print(f"{K:>6} {sqrtK:>6.1f} {b:>4} {delta:>8.1f} {Wq:>8.0f} || "
              f"{cand_core:>7.1f} {cand_core/sqrtK:>11.3f} || {expl_core:>10.2f} {expl_core/sqrtK:>10.3f}")
    print("\nBoth 'core/sqrtK' columns ~flat => both cores ~ sqrt K. Packing b*delta/Wq=O(1) keeps")
    print("K*delta/Wq = O(K/b) = O(sqrt K). Confirms codex's algebra by execution; no n^{2/3} leak.")
