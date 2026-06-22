r"""
Single entry point for the Phase-0 de-risking screens (guide.md section 7).

Regenerates EVERY figure and number:
  - C1 gadget-detectability sweep  -> figures/c1_gap_fraction.png
  - C2 per-query coverage sweep    -> figures/c2_coverage.png
  - a machine-readable dump        -> results.json   (frozen into PROJECT_STATE.md)

Run (PowerShell):  sim\.venv\Scripts\Activate.ps1 ; python sim\run_all.py
or directly:       sim\.venv\Scripts\python.exe sim\run_all.py

Fixed seeds throughout. Phase-0 internal de-risking only -- NOT a paper result.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

try:  # make stdout robust to non-ASCII on the Windows console (cp1252)
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import c1_gadget_detect as c1  # noqa: E402
import c2_coverage as c2  # noqa: E402
from emst import emst_weight, _brute_force_mst_weight  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)


def _selfcheck_emst():
    rng = np.random.default_rng(0)
    for n in (5, 25, 120):
        pts = rng.random((n, 2)) * 50.0
        assert abs(emst_weight(pts) - _brute_force_mst_weight(pts)) < 1e-6
    return "emst exact-vs-bruteforce self-check OK"


def _fig_c1(c1res):
    rows = c1res["rows"]
    ns = sorted({r["n_target"] for r in rows})
    plt.figure(figsize=(7, 5))
    for n in ns:
        rs = sorted([r for r in rows if r["n_target"] == n], key=lambda r: r["theta"])
        thetas = [r["theta"] for r in rs]
        fracs = [r["gap_frac"] for r in rs]
        plt.plot(thetas, fracs, "o-", label=f"n~{n}")
    ctrl = sorted(c1res["control"], key=lambda r: r["theta"])
    plt.plot([r["theta"] for r in ctrl], [r["gap_frac"] for r in ctrl], "x--",
             color="gray", label="neg-control (heavy:=strip)")
    plt.axhline(c1res["eps"], color="red", ls=":", label=f"eps={c1res['eps']}")
    plt.gca().invert_xaxis()  # p shrinks toward n^{1/2} to the RIGHT
    plt.xlabel("theta  (p = n^theta);  ->  thinner gadget / p -> n^{1/2}")
    plt.ylabel("heavy-vs-sparse gap fraction of w(P)")
    plt.title("(C1) gadget detectability: gap fraction as p -> n^{1/2}")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
    path = os.path.join(FIGDIR, "c1_gap_fraction.png")
    plt.savefig(path, dpi=120); plt.close()
    return path


def _fig_c2(c2res):
    ms = c2res["ms"]
    gc = [r["adv_max_counting"] for r in c2res["grid"]]
    pc = [r["adv_max_counting"] for r in c2res["permutation"]]
    ge = [r["adv_max_emptiness"] for r in c2res["grid"]]
    plt.figure(figsize=(7, 5))
    plt.plot(ms, gc, "o-", label=f"grid, counting (slope≈{c2res['grid_counting_slope']:.2f})")
    plt.plot(ms, pc, "s-", label=f"permutation, counting (slope≈{c2res['perm_counting_slope']:.2f})")
    plt.plot(ms, ge, "^--", label=f"grid, emptiness (slope≈{c2res['grid_emptiness_slope']:.2f})")
    plt.plot(ms, np.sqrt(ms), "k:", label="sqrt(m) reference")
    plt.xlabel("m  (number of candidate cells)")
    plt.ylabel("adversarial MAX per-query coverage")
    plt.title("(C2) per-query candidate-distinguishing-power (the kill metric)")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
    path = os.path.join(FIGDIR, "c2_coverage.png")
    plt.savefig(path, dpi=120); plt.close()
    return path


def main():
    sc = _selfcheck_emst()
    print(sc)
    print("running C1 gadget-detectability screen ...")
    c1res = c1.run()
    print("running C2 coverage screen ...")
    c2res = c2.run()

    fig_c1 = _fig_c1(c1res)
    fig_c2 = _fig_c2(c2res)

    out = dict(
        selfcheck=sc,
        c1=c1res,
        c2=c2res,
        figures=dict(c1=os.path.relpath(fig_c1, HERE), c2=os.path.relpath(fig_c2, HERE)),
    )
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=2)

    # ---- console summary (for freezing into PROJECT_STATE.md) ----
    print("\n==== C1 (gadget detectability) ====")
    print(f"eps threshold = {c1res['eps']}")
    for r in c1res["rows"]:
        flag = "DETECTABLE" if r["detectable"] else "below-eps"
        print(f"  n~{r['n_target']:5d}  theta={r['theta']:.3f}  p={r['p']:5d}  m={r['m']:4d}  "
              f"gap_frac={r['gap_frac']:.4f}  [{flag}]")
    print("  smallest detectable budget per n:", json.dumps(c1res["smallest_detectable_budget"]))

    print("\n==== C2 (per-query coverage; ADVERSARIAL max is the kill metric) ====")
    print(f"  grid counting slope (vs m)        = {c2res['grid_counting_slope']:.3f}  "
          f"(~0.5 => polynomial sqrt(m) growth; ~0 => O(1))")
    print(f"  permutation counting slope (vs m) = {c2res['perm_counting_slope']:.3f}")
    print(f"  grid emptiness slope (vs m)       = {c2res['grid_emptiness_slope']:.3f}")
    for r in c2res["grid"]:
        print(f"  [grid] m={r['m']:4d} sqrt_m={r['sqrt_m']:.1f}  adv_max_count={r['adv_max_counting']:4d}"
              f"  adv_max_empty={r['adv_max_emptiness']:3d}  MI/log_m={r['mi_ratio_worst']:.3f}"
              f"  rand_mean={r['random_mean']:.2f}")
    for r in c2res["permutation"]:
        print(f"  [perm] m={r['m']:4d} sqrt_m={r['sqrt_m']:.1f}  adv_max_count={r['adv_max_counting']:4d}"
              f"  adv_max_empty={r['adv_max_emptiness']:3d}  MI/log_m={r['mi_ratio_worst']:.3f}")
    print(f"\nfigures: {fig_c1}\n         {fig_c2}")
    print("results dumped to sim/results.json")


if __name__ == "__main__":
    main()
