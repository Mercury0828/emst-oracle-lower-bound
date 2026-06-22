# sim/ — Phase-0 de-risking screens

**Internal de-risking only (guide.md §7) — NOT a paper result.** SODA is a pure-theory venue; these
screens decide only whether the n^{1/2} target is worth a full proof effort. A clean small-scale
screen is a *necessary kill-screen, NOT sufficient proof*; asymptotic detectability and asymptotic
O(1)-coverage are proof obligations for the attack loop, not established here. **Adversarial input is
the kill metric; random input is a smoke check only.**

## Files
- `emst.py` — exact Euclidean MST weight (scipy Delaunay candidate edges + Kruskal/union-find;
  complete-graph fallback for tiny/collinear inputs). Self-checks against brute force.
- `gadgets.py` — faithful source gadgets (heavy "uniform" grid / sparse "strip"), equal cardinality;
  global-instance builder (C1) and packing builder (C2: `grid` baseline + `permutation` variant).
- `c1_gadget_detect.py` — **(C1)** gadget-detectability screen. Sweeps p=n^θ (θ∈[1/2,2/3]); measures
  the heavy-vs-sparse global w(P) gap as a fraction of total w(P). Pre-registration in the module
  docstring + `../DESIGN_DECISIONS.md` PR-C1.
- `c2_coverage.py` — **(C2)** per-query coverage screen (the decisive measurement). Adversarial max
  candidate-distinguishing-power of a range-COUNTING query, swept as m grows; emptiness contrast;
  MI-to-log-m ratio. Pre-registration in the module docstring + `../DESIGN_DECISIONS.md` PR-C2.
- `run_all.py` — **single entry point**; regenerates every figure + `results.json` (frozen into
  `../PROJECT_STATE.md`). Fixed seeds.

## Run (Windows / PowerShell)
```powershell
sim\.venv\Scripts\Activate.ps1
python sim\run_all.py
```
or without activating:
```powershell
sim\.venv\Scripts\python.exe sim\run_all.py
```
Outputs: `figures/c1_gap_fraction.png`, `figures/c2_coverage.png`, `results.json`.

## Environment
Local venv `sim/.venv` (Python 3.12; numpy 2.4.6, scipy 1.18.0, matplotlib). Do **not** modify the
system environment. To recreate:
```powershell
py -3.12 -m venv sim\.venv
sim\.venv\Scripts\python.exe -m pip install numpy scipy matplotlib
```

## What the screens measure (and do NOT)
- **C1** shows the *trend* of detectability as the gadget is thinned toward n^{1/2} — not the
  asymptotic crossover (at a few thousand points the p-budgets differ by only a small factor).
- **C2** measures coverage on the **baseline** packing (and an obvious general-position variant). A
  baseline showing polynomial growth is a RED/YELLOW SCREEN (→ redesign packing / escalate / human
  gate), **not** proof the target is dead — only a proof that *every feasible* packing has polynomial
  coverage would be proof-of-death. The RS/induced-matching optimal packing is an attack-loop
  obligation, not built here.
