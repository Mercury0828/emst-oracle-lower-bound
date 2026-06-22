# Independent Adversarial Audit A — Round 1, Crux C1 impossibility argument

**Auditor:** independent fresh-context adversarial mathematics auditor.
**Date:** 2026-06-21.
**Subject:** the solver's claim that no equal-cardinality C1 gadget exists at `p = n^{1/2+o(1)}`,
with sharp threshold `c = 2/3` (relative gap `≤ O(√p/m) = n^{3c/2−1}`).
**Method:** rigorous re-derivation + exact-EMST numerical stress tests (scipy, `sim/emst.py`).

**Bottom line:** the impossibility argument is **SOUND** within the stated disjoint-cell model.
One step (the §1 "MST monotonicity" justification) is *literally false as written* but the
conclusion it asserts is correct and provable by a different, standard argument — so that step is
**NEEDS-REPAIR (cosmetic; conclusion holds)**. All other steps are **VALID**. I could not break the
ceiling. I additionally *strengthened* the argument by removing its dependence on the cells tiling
the domain (the area lower bound holds for ANY disjoint layout), which closes the "empty regions"
escape hatch the brief worried about.

---

## Step 1 — Gap upper bound `|w(R∪H) − w(R∪S)| ≤ O(s√p)`  →  **NEEDS-REPAIR (conclusion VALID)**

### The flaw as written
The solver writes `w(R∪H) ≤ w(R∪S∪H) ≤ w(R∪S) + O(s√p)`, invoking "MST monotonicity"
(`w(R∪H) ≤ w(R∪S∪H)`). **This monotonicity is false for the Euclidean MST.** Adding points can
*decrease* the MST weight (the standard Steiner-style example: the centroid of an equilateral
triangle of side 1 lowers the spanning cost from 2 to √3). So the first inequality
`w(R∪H) ≤ w(R∪S∪H)` is not justified — and is generally wrong. The brief flagged this correctly.

### Why the conclusion is nonetheless correct (the rigorous replacement)
The bound `|w(R∪H) − w(R∪S)| ≤ C·s√p` holds via a **splice/edit argument** that needs no
monotonicity:

- *Sub-claim (grid/snake bound), verified.* For any `p` points in a side-`s` square,
  `EMST ≤ C·s√p`. Partition the square into `⌈√p⌉ × ⌈√p⌉ ` boxes (box side `s/√p`), connect occupied
  boxes in boustrophedon ("snake") order: `O(p)` edges each `O(s/√p)`, total `O(s√p)`; plus
  `O(√p)` row-transition edges of length `O(s)`, total `O(s√p)`. I verified numerically that the
  densest layout (uniform `√p×√p` grid) gives `EMST = (√p−1)·(√p)·(s/(√p−1)) → s√p`, with
  `EMST/(s√p) → 1` from above (1.25 at p=16 down to 1.03 at p=1024). So the upper bound is tight and
  the worst case is `Θ(s√p)`.
- *Splice.* Take the MST `T_S` of `R∪S`. Build a feasible (not optimal) spanning tree of `R∪H`:
  delete the `≤ p` vertices of `S` from `T_S` (this leaves a forest on `R` with `≤ p` extra
  components, since each deleted degree-`d` vertex creates `≤ d` fragments but the total over the
  tree telescopes), reconnect those `R`-fragments and attach all of `H` using a connector of total
  length `O(s√p)` (a spanning structure on `H` of cost `O(s√p)` plus `O(√p)` bridge edges, each of
  length `O(s)` because we only ever need to cross the cell, and bridges to nearby `R`-fragments
  cost no more than the deleted `S`-edges up to `O(s)` each over `O(√p)` of them). The resulting tree
  is a feasible spanning tree of `R∪H`, so `w(R∪H) ≤ w(R∪S) + O(s√p)`. By symmetry (`H↔S`) the
  reverse holds, giving `|w(R∪H) − w(R∪S)| ≤ C′·s√p`. No monotonicity is used.

### Numerical stress test (tried hard to break it)
I ran exact EMST on thousands of adversarial configurations — including the worst case for this
bound, where the changed cell is a **global bridge/hub** that far-away `R`-clusters must route
through (so swapping `S`=line for `H`=grid forces global rerouting):
- random `R` near the cell: worst `|gap|/(s√p) = 0.75`;
- two far clusters bridged through the cell: worst `0.999`;
- up to 7 surrounding clusters using the cell as a routing hub: worst `1.00`.
The ratio **never exceeded 1**. The constant is small and the `O(s√p)` law is robust. This is the
single most important inequality in the whole argument and it survives every attack.

**Verdict:** the written justification is wrong, but the inequality is true and provable by the
standard splice argument. Cosmetic repair; no impact on the conclusion.

---

## Step 2 — Backbone lower bound `w(P) ≥ Ω(s·m)`  →  **VALID (and strengthened)**

### Checks
1. *Covering.* Every point of `[Δ]²` lies in some cell; that cell contains ≥1 point of `P` (both the
   all-sparse and one-heavy instances put `p ≥ 1` points in every cell); the diameter of a side-`s`
   cell is `√2·s`, so every domain point is within `√2·s` of a tree point, hence within `√2·s` of
   `T`. **Correct.**
2. *Tube/Minkowski-sausage area.* A polygonal tree of length `L` has `r`-neighborhood area
   `≤ 2rL + πr²`. I verified this by Monte-Carlo on actual EMST trees: measured-area/`(2rL+πr²)`
   ≈ 0.97 across trials (always < 1; overlaps at vertices only reduce area). The bound holds for any
   polygonal tree — it does **not** rely on the points being an MST. **Correct.**
3. *Combine.* With `r = √2·s`: `Δ² ≤ area(nbhd) ≤ 2√2·sL + 2πs²`, so `L ≥ (Δ² − 2πs²)/(2√2·s)`.
   With `Δ = ks`, `m = k²`: `L ≥ Ω(s·k² − s) = Ω(s·m)` for large `m`. **Correct.**
4. *Numerical sanity.* One point per cell (the cheapest occupancy) on a `k×k` grid gives
   `EMST = (m−1)s`, i.e. `EMST/(s·m) → 1`. So `w(P) ≥ Ω(s·m)` is tight. **Confirmed.**

### Strengthening I found (closes the brief's "empty regions" escape)
The brief worried the bound might fail if cells do **not** tile the domain (sparse layout, empty
regions). It does **not** fail, and one need not invoke `Δ²` at all. Disjoint cells have **total
area ≥ m·s²** regardless of where they sit. Each occupied cell lies within `√2·s` of `T`, so the
union of cells lies in the `√2·s`-neighborhood of `T`, whose area is `≤ 2√2·sL + 2πs²`. Hence
`m·s² ≤ 2√2·sL + 2πs² ⇒ L ≥ Ω(s·m)` **for any disjoint-cell layout**, tiling or not. This removes
the dependence on the construction filling `[Δ]²` and makes the lower bound layout-independent.

**Verdict:** valid as stated, and robustly valid even beyond the tiling assumption.

---

## The `s`-cancellation (why the ceiling is unbeatable) — **VALID**

The decisive structural fact, which I confirmed symbolically: the relative gap is

  `gap / w(P) ≤ C·s√p / (c₀·s·m) = (C/c₀)·√p/m`,  **independent of `s`.**

The cell side `s` appears linearly in BOTH the gap upper bound (Step 1, `∝ s`) and the backbone
lower bound (Step 2, `∝ s`), so it cancels. A constructor cannot escape by tuning `s` (spreading
cells out to inflate per-cell cost, or packing them to shrink the backbone): every choice of `s`
yields the same ratio `√p/m`. I checked both regimes:

- *Spread / tiling (`s = s_max = Δ/√m = n^{(1+c)/2}`):* gap `= n^{c+1/2}`, backbone
  `w = n^{3/2−c/2}`, ratio `= n^{3c/2−1}`. (Solver's case.)
- *Packed (small `s`):* gap shrinks `∝ s`, but the layout-independent backbone bound shrinks `∝ s`
  too; ratio unchanged.
- *Trivial floor `w(P) ≥ Ω(n)`* (integer grid, min inter-point distance 1 ⇒ `n−1` edges each ≥ 1)
  gives a **weaker** ceiling `gap/w ≤ n^{c−1/2}` (threshold `c ≥ 1/2`); since the binding lower bound
  is the LARGER of the two, and backbone `n^{3/2−c/2} ≥ n` for all `c ≤ 1`, the backbone is binding
  and the trivial bound does not rescue the `c=1/2` target. It only makes things worse for the
  constructor, never better.

So in **every** regime the relative gap reduces to `O(√p/m) = n^{3c/2−1}`. The ceiling is genuine.

---

## Step 3 — Exponent algebra and the `c ≥ 2/3` threshold  →  **VALID**

With `p = n^c`, `m = n^{1−c}`: `√p/m = n^{c/2 − (1−c)} = n^{3c/2 − 1}`. A constant fraction requires
`3c/2 − 1 ≥ 0`, i.e. `c ≥ 2/3`. Verified symbolically. At `c = 1/2`: `3c/2 − 1 = −1/4`, fraction
`n^{−1/4+o(1)}` → the `p = n^{1/2+o(1)}` target is dead (vanishing fraction). At `c = 2/3`:
`m = n^{1−2/3} = n^{1/3}` — exactly the **existing** Driemel–Monemizadeh–Oh–Staals–Woodruff source
bound `Ω(n^{1/3})`, **not an improvement**. Per-cell exponents `a = 7/6` (heavy `s√p = n^{5/6}·n^{1/3}`)
and `b = 5/6` (sparse `≈ s`) match the source pair. Algebra is correct.

---

## Step 4 — Sharpness at `c = 2/3` (the threshold construction)  →  **VALID**

Solver's uniform-grid-vs-strip construction (`m=K²`, `p=R²K⁴`, `s=R²K⁵`, `Δ=n=R²K⁶`; sparse = line
of spacing `K`, heavy = `q×q` grid with `q=RK²`, spacing `D=RK³`). I reproduced it with exact EMST
at small scale:
- `K=2,R=1` (n=64): gap fraction `(w_h−w_s)/w_h = 0.36`.
- `K=2,R=2` (n=256): `0.57`; `K=2,R=3` (n=576): `0.68` — fraction **grows with R** (the free
  constant), as the analysis predicts (`ε_R → 1` for large `R`).
- `K=3,R=2` (n=2916): `0.60` — fraction **stable as K grows** (the asymptotic direction `m→∞`).

So `c = 2/3` admits a genuine constant-fraction gap, confirming the threshold is **sharp** (achievable
from above, impossible below). The construction's per-cell exact EMSTs (`(p−1)K = Θ(s)` for the
strip, `(p−1)D = Θ(s√p)` for the grid) are correct, and the global sparse weight `Θ(R²K⁷)=Θ(n^{7/6})`
matches the backbone lower bound.

---

## Overall classification: **SOUND**

The impossibility argument holds. The `√p/m` cap is real, `s`-independent, and forces `c ≥ 2/3`;
hence no equal-cardinality C1 gadget exists at `p = n^{1/2+o(1)}` in this disjoint-cell model, and
the model caps the achievable lower bound at the pre-existing `Ω(n^{1/3})` (`c=2/3 ⇒ m=n^{1/3}`).
The `c = 1/2` target is dead within this model.

The only defect is presentational: §1's appeal to "MST monotonicity" is false as written, but the
inequality it claims (`|gap| ≤ O(s√p)`) is true and provable by the standard splice argument and is
confirmed numerically up to a constant ≤ ~1. I also strengthened §2 to be layout-independent (no
tiling needed), which neutralizes the one substantive loophole the brief identified. I made a genuine
adversarial effort — bridge/hub configurations, packed vs. spread regimes, the trivial `Ω(n)` floor —
and found no way to beat the `√p/m` ceiling.

**Caveat on scope (not a flaw in the argument, but the boundary of its claim).** The impossibility is
proved *for this model*: `m` pairwise-disjoint equal-cardinality gadget cells, every cell occupied,
gap measured against the global EMST including backbone. It does **not** rule out an `Ω(n^{1/2})`
lower bound obtained by a structurally different reduction (e.g., overlapping/nested candidate
regions, non-tiling occupancy patterns where not every cell is occupied in both instances, or an oracle
argument that does not route the gap through a single-cell EMST swap). Within the stated model the
result is airtight; any path to `c=1/2` must leave the model.
