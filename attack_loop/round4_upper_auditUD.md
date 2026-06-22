# Round 4 (UPPER) — Audit U-D: the large-λ slab component-counting lemma (decisive)

**Auditor:** independent fresh-context auditor + algorithm-designer (with numerics).
**Date:** 2026-06-21. **Env:** `sim/.venv` python 3 (numpy 2.4.6, scipy 1.18.0), exact EMST `sim/emst.py`.
**Scripts (all runnable):** `attack_loop/auditUD_task1.py`, `…task1b.py`, `…task2.py`, `…task2b.py`,
`…task3.py`, `…task3c.py`, `…task3e.py`, `…task3f.py`, `…task3g.py`, `…task3h.py`.
All numerics go through an **exact orthogonal range-counting oracle** (`CountingOracle.count`,
sorted-x + binary search) that **counts every query**; uniform point samples are charged O(log Δ).

---

## TL;DR

- **Task 1 (point-sampling all sizes, λ ≤ n^{1/3}): SOUND.** Accuracy and the Õ(n^{1/3}) query
  bound both verified numerically and analytically.
- **Task 2 (dense Lemma-32 gadget scan): SOUND, with one stated caveat** (the scan is Õ(n^{1/3})
  only because the weight-relevant anomalous cells form a Θ(n^{1/3}) family — confirmed by the
  persistence accounting + the tile-or-blowup vise; a naïve g×g grid would be n^{2/3}).
- **Task 3 (the 🔴 large-λ gap): classification (B).** codex's *slab component-counting lemma*
  **as literally stated (per-size-bucket component counts) is essentially FALSE / not implementable**
  in Õ(√(n/λ)) on adversarial dense slabs — its objection is correct. **BUT the MST WEIGHT is
  recoverable by a different route** (persistence telescoping onto the **scalar** c(λ), estimated by a
  2-axis cell/slab estimator in Õ(√(n/λ))). The component-count sub-problem being √n-hard does **not**
  make the weight √n-hard. **No (C) hard instance survives the spread-vs-concentrate vise.**
- **Bottom line:** **o(√n) is achievable; Õ(n^{1/3}) is plausible but NOT fully closed** — the
  positive large-λ estimator is verified numerically and analytically for the weight, but the clean
  (1±ε) variance proof for the scalar-c estimator across all strata is not yet a theorem (it is the
  remaining work, and it no longer needs the false per-bucket lemma).

---

## Task 1 — point-sampling ALL component sizes (λ ≤ n^{1/3}): **SOUND**

**Algorithm audited** (codex): bucket sizes m∈[a,2a); draw T_a=Θ((λ/a)ε⁻²polylog) uniform points;
explore each point's scale-λ component up to 2a points via range-count probes; Horvitz–Thompson output
n/m on a bucket hit, 0 otherwise; truncate components with m>K=Θ(λL/ε).

**(i) Accuracy** — `auditUD_task1.py`, exact union-find ground truth for c(λ) and persistence λ·c(λ):

| instance | n | λ | true λ·c | est λ·c | ratio |
|---|---|---|---|---|---|
| islands | 1024 / 4096 / 16384 | 10/16/25 | 1030 / 4112 / 16400 | 875 / 3777 / 16114 | 0.85 → 0.92 → **0.98** |
| dense   | 1024 / 4096 / 16384 | 10/16/25 | 6680 / 39568 / 175575 | 6740 / 40763 / 178181 | **1.01 / 1.03 / 1.01** |
| uniform | 1024 / 4096 / 16384 | 10/16/25 | 10 / 16 / 25 | 0 | correct: one giant component, λ·c≈λ is negligible & truncated |

Ratio → 1 as n grows; the HT estimator is unbiased and the uniform case correctly returns ≈0
(everything is one truncated giant component at this λ).

**(ii) Query bound is Õ(n^{1/3})** — `auditUD_task1b.py` (cost computed from the algorithm's own
formula, n up to 10⁹):
- **(A)** Fixing λ, `cost/(λ·polylog²)` is flat (~225) across n∈[10³,4·10⁶] → per-scale cost is
  Õ(λ), **independent of n** except polylog.
- **(B)** Fixing n, `cost/λ` is ~constant (grows only ~polylog) → per-scale cost **linear in λ**.
- **(C)** Full sum over all geometric scales λ≤n^{1/3}: `total/(n^{1/3}·polylog³)` is **bounded and
  flat (~40–50)** across n∈[2.6·10⁵, 1.07·10⁹]. ⇒ **total = Õ(n^{1/3})**. ✔

**Variance / truncation:** HT with T_a=Θ((λ/a)ε⁻²·polylog) gives relative error ε per bucket
(median-of-means standard); large components m>K=Θ(λL/ε) contribute ≤ λ·n/K ≤ εn/L ≤ εOPT/L, safe.
No step estimates a single N_i/c_i to relative error — the bucket counts are summed, not divided.

**Verdict Task 1: SOUND.** Query bound Õ(n^{1/3}) confirmed; bucketing + truncation correct; HT
variance controlled. (Confidence 90%.)

---

## Task 2 — dense Lemma-32 gadget scan: **SOUND (with a stated caveat)**

`auditUD_task2.py`, `auditUD_task2b.py`.

**The literal scan is Õ(n^{1/3}).** A deterministic scan of the Θ(n^{1/3}) coarse cells of the
lower-bound construction costs exactly that: `scanq/n^{1/3}` is constant (16.0) across n∈[10³,2.6·10⁵],
and the heavy block is always found (`block found? = True`).

**Caveat I flag (and resolve).** A *2-D* coarse grid at side g=n^{1/3} has g²=n^{2/3} cells; a full
g×g scan would be **n^{2/3}, not n^{1/3}**. The "Θ(n^{1/3}) cells" reading is correct **only because**
the weight-relevant anomalies form a Θ(n^{1/3}) family. I verified *why* with exact EMST
(`auditUD_task2b.py`): **a single dense block of B points is ONE component** → it contributes only the
length of its **one** long connector (verified: connector ≈ 1.41·10⁶ regardless of B∈{16…1024}; the
B−1 internal edges go into the (n−Δ) term, not Σλc). So a single 2-D-hidden heavy block adds only
Õ(1) to Σλc. To reach a constant fraction of OPT you need Θ(n/λ) such anomalies, which must **tile**
the domain and are then seen by a coarse 1-D scan (the U-P2 tile-or-blowup vise). So the n^{2/3} fear
does not materialize.

**Verdict Task 2: SOUND**, conditional on the (true) fact that weight-relevant dense anomalies form a
Θ(n^{1/3}) family — which the persistence accounting + the vise establish. (Confidence 80%.)

---

## Task 3 — 🔴 the large-λ slab component-counting lemma: **classification (B)**

### 3.1 codex's objection is CORRECT (the per-bucket lemma is essentially false)

`auditUD_task3.py` (3-B): build a dense x-slab containing K small a-clusters interleaved with heavy
bulk. A single width-λ **slab count returns ≈ n** (e.g. 4096, 16384), carrying **no information** about
K = #a-clusters. Recovering the per-size-bucket count K then requires resolving sub-slab structure;
when target clusters have tiny mass fraction, Horvitz–Thompson reverts to the **point-sampling cost
Θ(λ/a)**, exactly as codex argued. **So the lemma "estimate the per-(size-bucket) component count to
additive O(εn/(λL)) in Õ(√(n/λ))" is NOT implementable from range counts on adversarial dense slabs.**

### 3.2 …but the per-bucket count is the WRONG primitive — the WEIGHT needs only the scalar c(λ)

**The key reframe (verified):** w(MST) = (n−Δ) + Σλ_i c_i is the **cluster-count integral**
w(MST) = ∫₀^∞ (c(t)−1) dt, with c(t) = #single-linkage components at threshold t. `auditUD_task3c.py`
confirms this to ratio **1.0001** on random instances. Crucially:

  c(λ) − 1 = #(MST edges ≥ λ)  — a **single scalar per scale**, not a per-size-bucket vector.

So the large-λ persistence Σ_{λ>n^{1/3}} λ·c(λ) is governed by the scalar c(λ). We never need the
quantity the false lemma tried to produce.

### 3.3 The positive large-λ estimator (scalar c(λ) via 2-axis cells): Õ(√(n/λ))

`auditUD_task3g.py` (S): estimate c(λ) by random 2-axis λ-**cell** probing (a nonempty cell that is a
separate blob = one component). On sparse grid-blobs:

| n | λ | true c(λ) | est c | ratio | √(cells) |
|---|---|---|---|---|---|
| 512 / 2048 / 8192 | 50 | 256 / 1024 / 4096 | 295 / 1057 / 4143 | 1.15 → 1.03 → **1.01** | 32 / 64 / 128 |

Accuracy → 1; cost ~ √(#cells). And `auditUD_task3h.py` pins the budget: **whenever λ·c(λ)/n is a
constant fraction (the only weight-relevant case), c(λ)=O(n/λ)** (measured c/(n/λ) = 1.0 for singleton
diagonals, ~2.5 for grid-blobs) ⇒ √(c) = O(√(n/λ)). Where c(λ) is large but λ·c(λ)/n is tiny
(one-blob, dense-uniform: ratio ≈ 0.01), the stratum carries **no constant-fraction weight** and is
truncatable. ⇒ **the weight-relevant scalar c(λ) is estimable in Õ(√(n/λ)) for every λ>n^{1/3}.**

### 3.4 No (C) hard instance: the spread-vs-concentrate vise holds at large λ

`auditUD_task3f.py` builds a **genuine constant-fraction large-λ weight gap** by halving c(λ): A =
G grid-blobs vs B = G/2 blobs (double mass each, same n). Measured **|wA−wB|/wA ≈ 0.29** (real gap,
driven by c(λ) halving; verified c−1 = 255→127 and 1023→511). The hard-pair concealment test then
shows the gap is **coarsely visible**:

| G | λ | λ-box (maxdiff, hit-frac) | 2λ-box (maxdiff, hit-frac) |
|---|---|---|---|
| 256 | 50 | (3, **0.274**) | (3, **0.996**) |
| 1024 | 50 | (3, **0.262**) | (3, **0.995**) |

A random λ-box sees the A-vs-B difference with **constant probability 0.27**, a 2λ-box with **0.996**.
⇒ **O(1/ε²) coarse probes distinguish A from B.** To drive the hit-frac → 0 you must concentrate the
differing blobs into o(n/λ) cells; since each blob is worth ~λ, that drops the weight gap to o(OPT) —
no longer hard. To hide a cluster from *both* slab axes you must pack it into one λ×λ cell, but then it
is within λ of its neighbors ⇒ it **merges** ⇒ it is no longer a separate component ⇒ **zero weight**
(`auditUD_task3g.py` (D): the dense small-cluster stratum carries 0.91–0.95 of the weight, but the
clusters are λ-separated and hence spread over distinct cells, visible to the y-axis estimator). This
is exactly the U-P2/U-P3 tile-or-blowup vise, and it is consistent with U-P1 (MST not √n-hard).

### 3.5 Classification

**(B) LEMMA FALSE BUT MST-WEIGHT STILL o(√n).** The per-size-bucket component-counting lemma is not
implementable in Õ(√(n/λ)) on dense slabs (codex is right). But the MST **weight** is recovered by a
different route — the cluster-count integral collapses the requirement to the **scalar** c(λ), which
the 2-axis cell/slab estimator gets in Õ(√(n/λ)) for every weight-relevant large-λ scale. The
sub-problem's √n-hardness is a **red herring** for the weight.

---

## Task 4 — achievable unconditional exponent

- **o(√n): YES (high confidence ~80%).** The large-λ branch via scalar c(λ) + 2-axis cells is
  Õ(√(n/λ)); combined with the verified small-λ point-sampling (Õ(λ)) and the dense-gadget scan, the
  per-scale cost is min(λ, √(n/λ)) **for the weight**, summing to a sublinear total. No √n lower bound
  survives the vise.
- **Õ(n^{1/3}): PLAUSIBLE but NOT closed (~40%).** The min(λ, √(n/λ)) balance peaks at n^{1/3}
  (round-3 [VERIFIED]) and every individual branch is now numerically validated for the WEIGHT. What
  is **not** yet a theorem: a clean (1±ε) variance/error-budget proof for the **scalar-c(λ) 2-axis
  estimator** across all strata simultaneously (the estimator I validated empirically has a small
  constant bias on grid-blobs, ratio ≈1.01 but needs a debiasing + median-of-means analysis), and a
  rigorous hitting/coupling lemma turning the measured constant hit-frac into a worst-case bound. These
  are the remaining work — and they **no longer require the false per-bucket lemma**, which is the
  substantive advance of this audit.

---

## Confidence (this auditor)

| claim | confidence |
|---|---|
| Task 1 point-sampling-all-sizes SOUND, Õ(n^{1/3}) | **90%** |
| Task 2 dense-gadget scan SOUND (with the family-size caveat) | **80%** |
| Task 3 = classification **(B)** (lemma false, weight recoverable) | **80%** |
| o(√n) unconditional upper bound | **80%** (was 60% in round 3) |
| Õ(n^{1/3}) unconditional upper bound | **40%** (was 35%) |

**Net effect on codex's report.** codex was right that its stated lemma is not implementable and that
its proof was "complete modulo" a false primitive. It was **over-pessimistic** in inferring
"o(√n) open": the weight does not need that primitive. The correct status is **(B)** — the obstruction
is real for component-COUNTING but is a red herring for MST-WEIGHT, which telescopes onto the scalar
c(λ) recoverable in Õ(√(n/λ)). The path to Õ(n^{1/3}) is open but now blocked only by a *standard*
variance/(1±ε) proof for the scalar-c estimator, not by a missing combinatorial miracle.

---

## Scripts

- `attack_loop/auditUD_task1.py` — point-sampling-all-sizes accuracy (islands/dense/uniform).
- `attack_loop/auditUD_task1b.py` — query-count scaling: per-scale Õ(λ), total Õ(n^{1/3}) to n=10⁹.
- `attack_loop/auditUD_task2.py` — dense-gadget scan query count vs n^{1/3}; g×g vs Θ(n^{1/3}) readings.
- `attack_loop/auditUD_task2b.py` — exact-EMST proof that a dense block is ONE component (Õ(1) persist).
- `attack_loop/auditUD_task3.py` — sparse slab works; dense slab count carries no component info.
- `attack_loop/auditUD_task3c.py` — cluster-count integral identity (ratio 1.0001); c(λ)=#long edges.
- `attack_loop/auditUD_task3e.py`, `…task3f.py` — constant-fraction large-λ weight gap + vise hit-frac.
- `attack_loop/auditUD_task3g.py` — positive scalar-c(λ) 2-axis estimator (ratio→1, √(n/λ)) + dense
  stratum weight check.
- `attack_loop/auditUD_task3h.py` — c(λ),N(λ)=O(n/λ) whenever λ·c(λ)/n is constant ⇒ budget Õ(√(n/λ)).
- (re-ran for reference) `attack_loop/auditUC_task3g.py` — round-3 hard-pair (gap/w≈0.001–0.014, NOT
  constant-fraction; box-diff = 1 per spread cell), corroborating the vise.
