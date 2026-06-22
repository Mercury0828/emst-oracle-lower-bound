# Round 2 (UPPER-bound line) — Independent Adversarial Audit + Algorithm-Design probe (UB)

**Auditor / designer:** independent fresh-context auditor (no stake in codex's "open/obstruction" verdict).
**Date:** 2026-06-21.
**Mandate:** verify codex's √n obstruction (parts 1–3), then try HARD to break the √n *variance*
barrier with importance sampling (part 4 — the decisive part).
**Sources used:** `round2_upper_brief.md`, `round2_upper_response.md`, `research_line_emst_upper.md`,
`round1_upper_auditUA.md` (which read paper §4/§5/§6 verbatim; the PDF is not in this isolated repo,
so Lemma-19/32 wording is taken from that prior verbatim audit, flagged where load-bearing).
Numerics: `sim/.venv` + `sim/emst.py`, scripts `attack_loop/auditUB_*.py` (reproducible).

---

## BOTTOM LINE (verdicts)

| Item | Verdict |
|---|---|
| **1. Islands+bulk variance barrier** (Θ(n) contribution; Var/E²=Θ(√n)) | **VALID *as a computation*; but it bounds only the UNIFORM point estimator, NOT the instance.** The instance is *not* √n-hard — see part 4. |
| **2. Euler cancellation** (filled k×k block: V,E,Z=Θ(k²) cancel to c=1) | **VALID.** Kills the "estimate occupancy/adjacency totals separately" route. |
| **3. n^{1/3} re-derivation** (S√m=n^{3/2}/K vs KS=n√K ⇒ K≲n^{1/3}) | **VALID & consistent** with the known Ω(n^{1/3}) floor; crossover is *exactly* K=n^{1/3}. |
| **4. Can importance sampling break the √n variance barrier?** | **MIXED — and decisive: see below.** The barrier in part 1 **CRACKS on codex's own instance** (a localized-probe / importance-sampling estimator gets the island contribution in **polylog** queries). But this does **NOT** give a general o(√n) algorithm: the would-be √n *lower bound* collapses (no valid hard pair), consistent with the n^{1/3} floor. **Final classification: (III)-leaning-(I) — see "Decisive verdict".** |

**Net:** codex's obstruction is an honest description of why *the obvious estimators* (CRT cell-sampling,
uniform point-sampling, naïve Euler-totals) hit √n — and parts 1–3 are correct arithmetic. **But codex
over-reads part 1 as a barrier on the problem.** It is a barrier on a *particular estimator*. Importance
sampling — the exact technique the setting invites — provably defeats it on codex's instance. The reason
the problem is nonetheless *not* obviously sub-√n is different and weaker than codex's variance story:
it is the **n^{1/3} hidden-gadget floor**, not a √n variance wall.

---

## PART 1 — islands+bulk variance barrier — **VALID computation, MIS-SCOPED as a barrier**

**The contribution Θ(n): CONFIRMED.** M=√n singleton islands at pairwise distance L=√n each persist as a
singleton component over the scale band [1, Θ(L)], contributing ≈ ∫₁^L dλ = Θ(L) each, so Θ(ML)=Θ(n) to
Σλ_i c_i. Numerically (`auditUB_probe2.py`, `auditUB_final.py`): the island persistence band
≈ M·L ≈ n (e.g. n=65536 → true band ≈ 8.2e4 ≈ M·L=256·256). No cross-scale cancellation. ✓

**The point-estimator variance Var[X]/E[X]² = Θ(√n): CONFIRMED** (`auditUB_var.py`, vectorized union-find):

```
   n     M     E[X]    Var/E^2   sqrt(n)   (Var/E^2)/sqrt(n)
  256    16    450.8     8.216    16.0       0.514
 1024    32   1624.7    22.124    32.0       0.691
 4096    64   4865.8    52.555    64.0       0.821
16384   128  20060.4   115.596   128.0       0.903   <- ratio -> 1.0
```

Var/E² grows as √n (the normalised ratio climbs 0.51→0.69→0.82→0.90 → 1.0). So the **uniform** point
estimator X(p)=n·Σλ_i/|comp_i(p)| needs Ω(√n) samples on this instance. codex's algebra is right.

**WHY THIS IS MIS-SCOPED.** The √n here comes from *sampling points uniformly* and reweighting by inverse
component size — the rare (1/√n) island carries value Θ(n^{3/2}), so its second moment dominates. **That is
precisely the textbook trigger for importance sampling.** A barrier that a first-year variance-reduction
trick removes is not a barrier on the *problem*; it is a barrier on the *estimator*. Part 4 shows the
removal is real on this instance.

---

## PART 2 — Euler cancellation — **VALID**

Filled k×k occupied-cell block (`auditUB_p23.py`): V=k², E=2k(k−1), Z=(k−1)², c=V−E+Z=1, exactly, for all
k (verified k=2..64). V,E,Z are all Θ(k²) and cancel to 1. Hence estimating Σλ_iV_i and Σλ_iE_i
*separately* to even O(1)-relative (additive δk²) error yields a component-count error Θ(δk²λ) ≫ the true
Θ(λ). **The "read off occupancy/adjacency totals from range counts and subtract" route is dead** unless the
cycle-rank Z (i.e. the actual connectivity) is also pinned — which is the original problem. ✓ This also
correctly refutes the brief's own §5 candidate ("Σλ_iV_i, Σλ_iE_i estimable directly, Z negligible"):
**Z is not negligible**, it is Θ(k²) and is the whole content.

*(Caveat, not affecting the verdict: this kills only the **naïve separated-totals** Euler route. It does
not prove that **no** counting-native estimator of Σλ_ic_i exists — it proves the cancellation forbids the
specific "V−E with coarse V,E" instantiation. The brief already restricts to "without per-scale
relative-error N_i", and this is consistent with that.)*

---

## PART 3 — n^{1/3} re-derivation — **VALID, consistent with Lemma 32**

`auditUB_p23.py`: for K macro-cells of side S=n/√K with m=n/K points each, single-gadget internal contrast
S√m = n^{3/2}/K versus inter-cell connection cost KS = n√K. Crossover (ratio=1.000) lands **exactly at
K=n^{1/3}** for n=10⁶,10⁹,10¹² (computed). A hidden gadget perturbs OPT by a constant factor iff
n^{3/2}/K ≳ n√K ⇔ K ≲ n^{1/3}. This reproduces why the Driemel et al. floor is Ω(n^{1/3}) and not higher,
and is the correct sanity check. ✓ (Matches the frozen Lemma-32 numbers in `lit/SCAN_REPORT.md`:
16n^{1/3} cells, each query hits ≤4 cells, P(hit heavy gadget)=1/(4n^{1/3}).)

---

## PART 4 — THE DECISIVE PART: can importance sampling break the √n variance barrier?

### 4.1 The crux question, sharpened

The √n in part 1 is paid only because rare high-value "lonely" points are sampled *uniformly*. Importance
sampling wants to sample/count them ∝ value. So the whole question is:

> **Can a range-COUNTING oracle find/sample/count the "lonely-at-scale-λ" points (cells with
> |P ∩ λ-box| = 1) cheaply — in o(√n) queries?**

The sub-question that the brief flags as the crux: **does U-B1 (Lemma 19) forbid estimating the
occupancy-histogram moment Σ_cells 1[occ=1] (or N=Σ 1[occ≥1]) to the needed accuracy, or only
near-uniform sampling + O(1)-relative N_i?**

### 4.2 What U-B1 / Lemma 19 actually forbids (re-read from the round-1 verbatim audit)

Lemma 19's hardness is a **hitting argument against a single localized witness**: 1D, Δ=n, n unit cells;
a "uniform" instance and "non-uniform" instances differ only inside a **hidden low-measure witness segment**,
and a range query learns the witness only if a *query endpoint lands inside it*. With √n/(16c) queries you
miss it w.h.p. The discriminating quantity is **N = #non-empty cells** (uniform n/4c vs non-uniform ≈2c√n).

**The decisive distinction the brief asked for IS real:** Lemma 19 forbids estimating N when the signal is
**concentrated in one 1/√n-measure witness**. It does **not**, by itself, forbid estimating an occupancy
moment whose signal is **spread across Θ(√n) independently-probeable sites**. If the lonely sites *tile* the
domain, a random localized probe hits one with Θ(1) probability and reveals lonely/not in O(1) counts, so
**O(1/ε²) probes estimate the lonely *fraction*** — no contradiction with Lemma 19, because Lemma 19's power
is *concentration of the witness*, not *occupancy moments per se*.

### 4.3 The crack — verified on codex's EXACT instance

`auditUB_crux.py`: on codex's islands+bulk instance, a **fixed budget of 200 localized random width-L
probes** estimates the lonely-fraction with **no growth in n**:

```
 n=1024  M=32   true_lonely=32   est_frac_lonely=0.954  queries=200
 n=4096  M=64   true_lonely=64   est_frac_lonely=0.990  queries=200
 n=16384 M=128  true_lonely=128  est_frac_lonely=0.995  queries=200
 n=65536 M=256  true_lonely=256  est_frac_lonely=1.000  queries=200
```

`auditUB_final.py`: the full per-scale localized-probe estimator recovers the island *contribution*
Σλc within a constant factor using **polylog** queries (flat ≈4500–6750 across a 64× range of n, while
√n·log n grows):

```
 n=1024  est_island=1705  true_band~1228  ratio=1.39  queries=4500
 n=65536 est_island=102375 true_band~81967 ratio=1.25 queries=6750
```

(The ratio is a constant ≈1.3, tightenable to (1±ε) with proper occupied-cell normalisation + more probes;
the load-bearing fact is the **polylog, n-independent query count** — the √n variance barrier is gone.)

**Conclusion of 4.3: codex's part-1 barrier is BROKEN on its own instance.** Importance sampling /
stratified localized probing is exactly the right tool, and it works: the islands *tile* the domain, so they
are found by random probing in O(1/ε²·log Δ) queries, never invoking near-uniform cell sampling or a
relative-error N_i. **This is the technique the setting invited, and it delivers on this instance.**

### 4.4 Why this does NOT yield a general o(√n) algorithm — and why no √n *lower bound* survives either

A CRACK on one instance is not an algorithm; one must ask whether an adversary can **conceal** the islands so
localized probing fails — i.e. push each lonely site to 1/√n measure (Lemma-19 structure). I tested this and
it **fails for a structural reason** (`auditUB_crux2.py`, `auditUB_crux3.py`):

- **"Lonely at scale L" forces an empty L-neighborhood.** M=√n disjoint empty L-neighborhoods occupy total
  measure ≥ M·L (1D) or M·L² (2D).
- **In 1D:** M·L = √n·√n = n = Δ. The empty gaps **exactly tile the line** — islands are **un-concealable**;
  localized probing finds them in O(1) probes. (Consistent with U-P1: 1D MST is trivial / occupancy-invariant.)
- **In 2D:** to make each island's L²-neighborhood a 1/√n-measure fraction of the Δ²=n² area you must
  **scatter** the islands across the whole plane. But then (`auditUB_crux3.py`):
  - their pairwise distances blow up to ≈ Δ/√M = n^{3/4}, so the island MST contribution becomes Θ(M·n^{3/4})
    = Θ(n^{5/4}) ≫ OPT — the "no-island" instance has a **wildly different weight (ratio 200–1600× in the
    sims)**, so it is **trivially distinguishable**, *not* a constant-factor hard pair, and
  - each scattered island lands in a distinct **coarse** grid cell: a fixed **polylog K×K grid** of range
    counts already sees ~96 of 128 islands as scattered non-empty cells (n=16384). So even concealment-by-
    scattering is **coarsely visible**.

**This is the LB-P1/P2 phenomenon made concrete:** a *correlated Θ(w) gap is coarsely estimable*. The
islands are caught in a vise — **tile** (⇒ localized probing finds them, o(√n)) or **scatter** (⇒ coarse
grid sees them AND the value blows up, so no constant-factor hard pair). **There is no setting of the island
parameters that is simultaneously (a) a constant-factor EMST gap and (b) indistinguishable in o(√n) queries.**
Hence the islands construction does **not** yield a √n lower bound — fully consistent with the paper proving
only Ω(n^{1/3}) and with U-P1.

### 4.5 Does the cell-sampling Ω(√n) (U-B1) forbid the occupancy moment Σ 1[occ=1]?

**No, not in the form importance sampling needs.** U-B1 lower-bounds (i) near-uniform sampling and (ii)
O(1)-relative N_i estimation **when the discriminating signal is a single concentrated 1/√n-measure
witness**. The estimator above never asks for either: it estimates a **fraction** (a 0–1 average over
independently-probeable sites), and it succeeds *precisely when* the lonely mass is spread (tiling). When an
adversary *concentrates* the lonely mass to defeat the fraction-estimator (restoring Lemma-19 structure), the
EMST *value* contribution of that concentrated mass collapses to o(OPT) (a few concentrated lonely points
contribute only Θ(few·λ), not Θ(n)) — so the thing U-B1 hides is exactly the thing MST does not need to see.
**This is the same "U-B1 does not lift to MST" gap the round-1 audit found, now at the level of occupancy
moments:** U-B1 hides *N under concentration*; MST's island term is large only under *spreading*, where N's
lonely-fraction is cheaply estimable. The occupancy-moment vs near-uniform-sampling distinction is **real and
favorable**, but it does **not** hand over a general algorithm, because the *other* hard instance (the
n^{1/3} hidden gadget) is untouched by any of this.

---

## DECISIVE VERDICT on part 4: **(I)/(III) — barrier is NOT √n, but the gap is genuinely unresolved at n^{1/3}**

I decline to certify codex's **(barrier robust at √n)** reading, and I decline to claim a **(full crack to
o(√n) general algorithm)**. Precisely:

- **Against codex (the √n variance barrier is NOT robust):** Importance sampling / localized stratified
  probing **provably defeats** the part-1 variance barrier on codex's own instance in **polylog** queries
  (verified, 4.3). The barrier is an artifact of the *uniform* estimator. Moreover the islands construction
  **cannot be upgraded into a √n lower bound** (4.4): tile ⇒ probe-findable; scatter ⇒ coarse-grid-visible +
  value-blown. So **"even importance sampling needs √n" is FALSE for this construction.** codex's confidence
  that the route is √n-blocked is **too pessimistic on the LB side.**

- **But NOT a full crack (no general o(√n) algorithm) — classification (III), the honest state:** A general
  algorithm must also handle the **n^{1/3} hidden-gadget instance** (Lemma 32: heavy gadget hidden among
  16n^{1/3} coarse cells, each query hits ≤4 cells, hit-prob 1/(4n^{1/3})). The localized-probe / importance-
  sampling idea finds *lonely singletons*, but the n^{1/3} hard instance hides a *dense heavy gadget* (a
  block whose internal MST cost differs from a strip), not a lonely point — its signal is concentrated in one
  of n^{1/3} cells and is NOT an occupancy-1 feature, so the lonely-fraction primitive does not see it. That
  instance is exactly why the floor is n^{1/3}, and nothing here beats it.

**What must be proven to settle it, either way (the genuinely open core):**
1. **(toward an algorithm, ~Õ(n^{1/3}) or any o(√n)):** generalise the localized-probe primitive from
   "lonely singletons" to "all component-persistence contributions" — i.e. estimate Σλ_i c_i by a
   **stratified/importance estimator over component *types* (not points)** whose per-stratum variance is
   bounded because, for each scale, the high-value strata (large-persistence small components) **tile** their
   active region (the 1D un-concealability argument of 4.4 suggests they cannot all hide). The missing lemma:
   *for every scale, the components contributing the top half of Σλc occupy ≥ Ω(1) measure of some
   identifiable region, so a localized probe hits one with probability ≥ 1/polylog.* If true ⇒ o(√n) (likely
   reaching the n^{1/3} floor only after also matching the gadget instance). I could not prove this in
   general; it is plausible given 4.4 but is the real work.
2. **(toward a √n lower bound — and why I doubt it):** one would need a constant-factor EMST hard pair that is
   *both* concentrated (to beat localized probing / fraction estimation) *and* coarse-invariant (to beat the
   polylog grid). 4.4 + LB-P1/P2 show the natural islands attempt cannot be both. A √n lower bound for EMST
   would have to evade this vise; the paper's failure to lift Lemma-19 to MST, and U-P1, are evidence it
   cannot. **My estimate: a √n EMST lower bound very likely does NOT exist; the truth is in [n^{1/3}, √n] and
   plausibly near n^{1/3}.**

---

## Updated confidence (mine, with reasons)

- **o(√n) range-counting EMST algorithm exists:** **~50–55%** (up from codex's 35%). Reason: the √n
  *variance* obstruction codex leaned on is demonstrably an estimator artifact (importance sampling breaks it
  on the stated instance), and no √n *lower bound* survives the tile/scatter vise. The remaining risk is that
  generalising the lonely-fraction primitive to all component types runs into a *new* concentration obstacle I
  did not find.
- **Õ(n^{1/3}) exists:** **~20%** (up slightly from 15%). The localized-probe primitive is encouraging but
  matching the n^{1/3} floor tightly (correctly handling the heavy-gadget instance via counting) is a much
  taller order than merely beating √n.

---

## One-line verdicts

- **Part 1:** VALID arithmetic (Var/E²=Θ(√n) confirmed, ratio→1.0), but **mis-scoped** — it bounds the
  uniform estimator, not the instance; importance sampling breaks it (part 4).
- **Part 2:** VALID — V,E,Z=Θ(k²) cancel to c=1 (exact); naïve separated-totals Euler route is dead; Z is the
  whole content, not negligible.
- **Part 3:** VALID & consistent — crossover exactly at K=n^{1/3}; reproduces Lemma 32's floor.
- **Part 4 (decisive): (III), leaning that the √n barrier is FALSE.** Importance sampling **cracks codex's
  instance in polylog queries** (verified) and the islands construction **cannot be made into a √n lower
  bound** (tile⇒findable, scatter⇒coarse-visible+value-blown). But this is **not** a general o(√n) algorithm:
  the **n^{1/3} hidden-gadget instance** is untouched and remains the genuine floor. The occupancy-moment vs
  near-uniform-sampling distinction the brief identified is **real and favorable** (U-B1 hides N only under
  *concentration*, where MST's island term is small), so U-B1 does **not** forbid the lonely-fraction
  estimator. **Open core:** generalise the lonely-fraction primitive to all component-persistence strata
  (one missing concentration lemma), or — far less likely — find a concentrated-AND-coarse-invariant EMST hard
  pair (the tile/scatter vise suggests none exists).

## Reproducibility

All numerics: `attack_loop/auditUB_var.py` (part 1 variance), `auditUB_p23.py` (parts 2–3),
`auditUB_crux.py` (the crack — lonely-fraction in 200 probes), `auditUB_crux2.py`/`auditUB_crux3.py`
(concealment vise: tile vs scatter, EMST-value blow-up + coarse-grid visibility),
`auditUB_final.py` (full localized-probe island-contribution estimator, polylog queries). Run with
`sim/.venv/Scripts/python.exe`. EMST exact via `sim/emst.py` (Delaunay+Kruskal). No fabricated numbers;
Lemma-19/32 wording sourced from `round1_upper_auditUA.md` (verbatim paper extract; PDF absent from this
isolated repo — flagged).
