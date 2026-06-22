# Independent Adversarial Audit C — Round 2, the multi-needle / planted-pattern escape

**Auditor:** independent fresh-context adversarial mathematics auditor.
**Date:** 2026-06-21.
**Subject:** the solver's Round-2 obstruction argument (`round2_escape_response.md`), claiming the
multi-needle / planted-pattern escape from the Round-1 `n^{1/3}` cap also fails, capping the
gadget-packing approach at `n^{1/3}` (`n^{1/4}` at `M=√n`).
**Method:** rigorous re-derivation + exact-EMST and brute-force-coverage numerics
(`sim/.venv`, `sim/emst.py`, plus six purpose-built probes `sim/auditC_*.py`).
**P1 treated as sound** (independently verified in Round 1).

**Bottom line.** The obstruction is substantially stronger than a heuristic: every one of its five
load-bearing steps survived adversarial probing, and two of the steps the solver stated only
heuristically (locality/parity, Step 5; and the projection⇒coverage link inside Step 1) I was able
to upgrade to quantitatively-supported claims. I found **no live escape to `n^{1/2}`**. The single
genuine gap is the narrow "new primitive" of Step 6, which is open but which my search actively
fails to realise (large EMST gap forces `≥ Ω(√p)` count-discrepancy in every design I could build).
Classification: **(a) NEAR-PROOF-OF-DEATH**.

---

## Step 1 — "O(1) coverage ⇒ disjoint projections ⇒ M·s ≤ O(n) ⇒ s ≤ O(p)" → **VALID (with a constant-factor restatement)**

This was flagged as the most likely hole; I probed it hardest. Two findings.

**(1a) The literal word "disjoint" is too strong, but harmlessly so.** O(1) coverage does NOT require
projection *multiplicity exactly 1*; multiplicity `t = O(1)` suffices. The hierarchical/fractal layout
I built (`auditC_step1.py`, `auditC_step1b.py`) has x- and y-projection multiplicity = 2 and yet
adversarial coverage = 2 (flat as `m` grows, `m` up to 64). So the solver's "disjoint-projection
packing" should read "**O(1)-projection-multiplicity packing**." This is a cosmetic relaxation: covering
the length-`Δ` x-axis with cell-widths of multiplicity `≤ t` gives `M·s ≤ t·Δ = O(n)` for any `t=O(1)`.
The conclusion `M·s ≤ O(n)` is unchanged.

**(1b) The decisive implication "O(1) coverage ⇒ O(1) projection multiplicity" is numerically tight.**
The audit's central worry was a non-disjoint layout (hierarchical/multi-grid/randomized) escaping
`M·s ≤ O(n)` while keeping coverage O(1). I built exactly these and measured both quantities
(`auditC_step1c.py`). The result is a clean monotone law:

| layout | x-proj multiplicity `t` | adversarial max coverage |
|---|---|---|
| permutation (spread) | 1 | 4 |
| staircase, x-overlap 0.8 / 0.9 / 0.95 | 6 / 11 / 20 | 8 / 16 / 30 |
| diagonal forced into x_extent 16 / 8 / 4 | 5 / 9 / 17 | 10 / 16 / 25 |
| grid / random box | `√m` | `~1.5√m` |

**Coverage ≈ 1.5–2 × projection multiplicity, always.** The mechanism is exactly as the C2 screen's
pre-registration warned: a single vertical rectangle-edge dropped in a column where `t` cells overlap
in x straddles all `t`, and with off-centre (count-snapped) placement the heavy 4×4 grid and the strip
disagree in each → coverage `≈ t`. Every attempt to pack cells more tightly (raise `t`, shrink the
x-extent below `M·s`) raised coverage proportionally. **I could not find any O(1)-coverage layout with
`ω(1)` projection multiplicity**, and the 2-D area `Δ²=O(n²)` does not relax the constraint because the
straddle obstruction is a **1-D projection** fact on each axis (length `Δ=O(n)`), not an area fact.

**The escape that survives marginal-matching is still count-visible (relevant to 1b).** I also tested
the subtler escape: a per-cell heavy/sparse design whose straddles are *invisible* because the two share
both 1-D marginals (`auditC_step1d.py`). The monotone-diagonal sparse set matches the heavy grid's x- and
y-marginals exactly, yet a *2-D corner rectangle* still sees a discrepancy of `Θ(p)` (it catches the
whole diagonal cluster). So marginal-matching does not buy invisibility; the joint count betrays it.

**Verdict: VALID.** Restate "disjoint projection" as "O(1) projection multiplicity"; the `M·s ≤ O(n)`
hence `s ≤ O(n/M) = O(p)` conclusion is correct and numerically robust.

---

## Step 2 — "Total EMST gap ≤ O(k·s·√p) when k cells active (additive)" → **VALID (additive; no super-additivity)**

Direct exact-EMST test (`auditC_step2.py`), `M=36`, `p=36`, both a spread permutation layout and an
adversarial **adjacent-diagonal** layout (active cells packed contiguously so heavy gadgets could
interact through the backbone):

- Spread: `gap/(k·s√p)` = 0.75, 0.83, 0.75, 0.82, 0.79, 0.81, 0.80 for `k`=1,2,4,8,16,24,36.
- Adjacent-diagonal: 0.83, 0.79, 0.78, 0.77, 0.76, 0.76.

`gap/k` is constant (≈ 4.6–5.0) across the whole range; if anything adjacency *lowers* the per-cell gap
(shared backbone), never raises it. **No super-additive coupling exists** — the P1 cap telescopes
additively, as claimed. **Verdict: VALID.**

---

## Step 3 — "w(P) ≥ Ω(max{sM, n})" → **VALID**

`w ≥ Ω(sM)` is the Round-1 backbone bound (verified, audit A, even layout-independent via the disjoint-
cell area argument). `w ≥ n−1` is the integer-grid floor. With the Step-1 binding value `s = n/M`,
`sM = n` exactly, so the bound collapses to the clean `w ≥ Ω(n)`. **Verdict: VALID.**

---

## Step 4 — "k ≥ Ω(M/√p), hitting M/k ≤ O(√(n/M)), capped at n^{1/3}" → **VALID**

Verified symbolically (`sympy`, `auditC` shell). With `p=n/M`, `s=n/M`:
constant gap needs `k·s√p ≥ Ω(n)` ⇒ `k ≥ M^{3/2}/√n = M/√p` (matches solver). Hitting bound
`M/k = √(n/M) = √p`. Overall lower bound `min{M, √(n/M)}` is maximised at `M=n^{1/3}` giving `n^{1/3}`;
at `M=√n` it is `√(n/√n)=n^{1/4}`. Every number in the solver's optimisation checks out.
**Verdict: VALID.** The active-subset multi-needle route is genuinely capped at `n^{1/3}`.

---

## Step 5 — "EMST is a sum of O(1)-local terms ⇒ parity/XOR hides but cannot move EMST by Θ(w)" → **VALID (upgraded from heuristic to quantitative)**

The solver stated this as a plausibility ("EMST too local/Lipschitz to see a Θ(n) parity signal"). I
made it quantitative (`auditC_parity.py`, `auditC_step56.py`), spread permutation layout, `M=25`:

- The additive model `f_lin(x)=w0+Σ a_i x_i` (with `a_i` = single-flip increments from all-sparse)
  predicts the **full-heavy gap to within 1.3%** (`97.16` predicted vs `98.43` actual).
- Residual `R(x)=f(x)−f_lin(x)` over random states: `std/gap = 0.24%`, `max|R|/gap = 1.1%`.
- **Direct parity test:** `E[EMST | even parity] − E[EMST | odd parity]` over states with matched
  per-coordinate marginals = `0.11`, i.e. **0.11% of the full gap.**
- Single-cell flip-increment has `std/mean ≈ 2%` across random backgrounds (`auditC_step56.py`): EMST
  is *approximately*, not exactly, local — but the non-local energy is `O(1%)` of the gap, far below
  the `Θ(1)` fraction a parity escape would need.

So a LOW/HIGH coupling that matches all low-order (incl. adjacent-pair) marginals and differs only in a
global parity moves EMST by `~0.1%` of `w` — **not** `Θ(w)`. The locality/parity obstruction is real.
*Caveat:* this is verified in the spread (disjoint-projection) layout the construction is forced into by
Step 1, which is precisely the relevant regime; I did not prove it for all conceivable layouts, but the
construction has nowhere else to live. **Verdict: VALID (within the forced layout family).**

---

## Step 6 — "the new primitive: gap ~Θ(s√p) with class-independent counts" → **OPEN, but actively unsupported (the only real gap)**

This is the loophole the solver names and cannot close. I attacked it directly (`auditC_step56.py`,
`auditC_primitive.py`): search per-cell designs for one with **large EMST gap AND small max rectangle
count-discrepancy** vs the heavy grid. Result (max over count-snapped rectangles):

| design | gap/(s√p) | max rect count-discrepancy |
|---|---|---|
| strip | 0.90 | `~p` (34, 95, 178) |
| monotone-diagonal (matches both 1-D marginals) | 0.84–0.87 | `~√p` (9, 25, 49) |
| two-strips / L-shape / half-grid | 0.5–0.84 | `~p/2 … p` |

**Every design with gap `= Θ(s√p)` has max count-discrepancy `≥ Ω(√p) = ω(1)`.** The best
(monotone-diagonal) drives it down to `Θ(√p)` — but `√p` is still polynomially large, so the cell is
revealed by a *single* coarse rectangle query (the unequal-cardinality trap of §3/§2, re-armed at the
sub-rectangle level). I found no design reaching `o(√p)`, let alone `O(1)`, discrepancy while keeping a
constant-fraction gap. This is empirical evidence, not a theorem: the primitive is **genuinely open**,
but **unsupported** — all obvious max-gap versions are coarsely count-visible, exactly as the solver
asserts. A constructor would need a fundamentally non-obvious primitive that my search did not touch.

**Verdict: OPEN (not provably impossible), but actively unsupported by construction.**

---

## Overall classification: **(a) NEAR-PROOF-OF-DEATH**

Round 2 + P1 rigorously cap the **gadget-packing / planted-pattern** family at `n^{1/3}`:

- **Step 1** forces `s ≤ O(n/M)` via the numerically-tight law *coverage ≈ projection multiplicity*
  (the audit's prime suspect for a hole — hierarchical, multi-grid, randomized, marginal-matched
  layouts all tested; none escapes).
- **Step 2** (additive, no super-additivity), **Step 3** (`w ≥ Ω(n)`), and **Step 4** (algebra) are
  all clean and verified, giving the `min{M, √(n/M)} = n^{1/3}` ceiling, `n^{1/4}` at `M=√n`.
- **Step 5** (the parity/coding escape) is killed quantitatively: a marginal-matched parity coupling
  moves EMST by `~0.1%` of `w`, because EMST is additive-to-1% over cell-states in the forced layout.
- **Step 6**, the lone surviving loophole — a `Θ(s√p)`-gap cell with `O(1)` count-discrepancy — is
  genuinely **open**, but my construction search drives the discrepancy no lower than `Θ(√p)` for any
  near-maximal gap, so it is unsupported.

This is **not** a full proof-of-death: as the solver correctly notes, the existing `Ω(n^{1/3})` lower
bound forbids any blanket "polylog queries distinguish every constant EMST gap" theorem, so no clean
general obstruction can be true, and Step 6's primitive cannot be ruled out by these methods. But every
*constructive* route examined is dead, and the only escape is a narrow, unbuilt, evidence-against
primitive. I concur with the solver's ~35% confidence that an `Ω(n^{1/2−o(1)})` counting-oracle lower
bound exists at all; if anything the count-visibility floor `≥ Ω(√p)` I measured nudges me slightly
lower (~30%). I found **no live escape** (not (b)); the obstruction is rigorous on Steps 1–5 and only
suggestive on Step 6, which is the defining shape of **(a)**, not (c).

### Reproducibility
Probes added under `sim/`: `auditC_step1.py` (layout coverage), `auditC_step1b.py`
(coverage vs projection multiplicity vs density), `auditC_step1c.py` (tight-packing scaling),
`auditC_step1d.py` (marginal-matching), `auditC_step2.py` (additivity), `auditC_step56.py`
(locality + count-visibility tradeoff), `auditC_parity.py` (parity-induced gap), `auditC_primitive.py`
(new-primitive search). All use exact EMST (`sim/emst.py`) and the project venv.
