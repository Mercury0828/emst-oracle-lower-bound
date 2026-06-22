# Gate-1 Independent Audit — Paper Orientation & Second Opinion

**Auditor role:** fresh-context, adversarial second opinion at the end of Phase 0 (screening, not
attacking). Mandate: do not rubber-stamp. **Scope of evidence I could actually verify:** the repo
docs (`research_line_emst.md`, `PROJECT_STATE.md`, `guide.md`, `DESIGN_DECISIONS.md`), the four
simulation modules under `sim/`, `sim/results.json`, plus independent re-runs of my own stress
tests and four web spot-checks. **Date:** 2026-06-20. **Target venue:** SODA 2027 (deadline
2026-07-09).

---

## 0. A verification gap that must be stated up front

The draft verdict and `PROJECT_STATE.md` both reference two artifacts as the *source of record* for
the kill-scan and the Phase-0 conclusion:

- `lit/SCAN_REPORT.md` (the four web-thread kill-scan, exact cites, version/lemma numbers)
- `PHASE0_REPORT.md` (the consolidated verdict)

**Neither file exists in the repo** (`lit/` is absent; `PHASE0_REPORT.md` is absent). The kill-scan
findings exist *only* as prose inside the audit prompt. I therefore cannot independently verify the
kill-scan as a written, frozen artifact — I can only re-derive its central claims from the web,
which I did (Section 1). **Gate-1 housekeeping requirement:** before the human signs off, the
kill-scan and Phase-0 verdict must be committed as files with the exact citations (Czumaj SIAM
J. Comput. 35(1):91–109 2005; arXiv:2504.15292 version + Thm 30 / Lemma 32; arXiv:2603.20943). A
verdict whose evidence lives only in a chat prompt is not auditable and is not a gate artifact.

This does **not** by itself downgrade the scientific verdict, but it is a process red flag worth
recording.

---

## 1. Second opinion on the KILL verdict → I concur: GREEN (with the caveat above)

I independently spot-checked the three kill axes by web search and source fetch:

- **No RED scoop.** The only paper improving/closing the counting-oracle EMST lower bound past
  n^{1/3} would have to be a follow-up to arXiv:2504.15292. Searches surface the source itself, the
  ICALP 2023 general-metric MST/TSP paper (Chen–Khanna–Tan, arXiv:2203.14798), the classic
  Czumaj–Sohler sublinear-EMST line, and the 2026 convex-hull paper — **none** proves a
  range-counting EMST lower bound above n^{1/3}. The ICALP 2023 paper is a *distance-query*, *general
  metric* model (Õ(n^{1.5}) queries, n/α space) — a different oracle and regime; it does not transfer.
  **Agree: no scoop.**

- **No RED ceiling.** No sub-√n *counting* upper bound surfaced (the upper bound everywhere is
  Õ(√n), the source's Thm 30), and no barrier ruling out n^{1/2−o(1)}. I fetched arXiv:2603.20943:
  it is convex-hull approximation via range-**emptiness** oracles (tight Θ(q^{−1/d}) tradeoffs), and
  explicitly **does not** address MST counting-query complexity. Not a ceiling. **Agree.**

- **No preemption of C1/C2.** Nothing found pre-empts a point-efficient MST gadget or an
  RS/induced-matching O(1)-coverage counting packing. **Agree (to the limit of a spot-check).**

- **Boundary correctly stated.** The literature Ω(√n) is for **emptiness** queries, **deterministic**
  algorithms, **O(n^{1/4})-relative error** — the web result confirms this verbatim. The draft's
  insistence that this is *motivation only* and does **not** transfer to a *counting*, *randomized*,
  *(1±ε)* bound is correct and is exactly the boundary (B3, "counting ⊋ emptiness") that keeps the
  problem open. Not mis-stated.

**Residual scan risk (why GREEN, not GREEN-certified):** a single auditor web pass cannot rule out a
very recent or non-indexed manuscript. The verdict rests on a clean negative, which is inherently
soft. Recommend one more targeted pass close to submission (search arXiv listings cs.CG/cs.DS
2026-04→2026-07 for "range counting" + "spanning tree"). But on present evidence: **GREEN is the
honest call.** No reason to downgrade to YELLOW/RED on the literature axis.

---

## 2. Second opinion on the SCREENS → mostly sound, but the optimism on C2 needs two corrections

I re-ran the C2 screen under a **stronger adversary** than the one in `c2_coverage.py` (200k random
rectangles per configuration with edges snapped to actual point coordinates, vs. the structured
half-plane/slab/coarse-quadrant family in the committed screen). Results:

| layout | m=16 | m=64 | m=144 | m=256 | committed screen (adv_max_counting) |
|---|---|---|---|---|---|
| grid | 12 | 28 | 44 | 60 | 7 / 15 / 23 / 31 |
| permutation | 4 | 4 | 4 | 4 | 2 / 2 / 2 / 2 |

**Finding 2a — the committed C2 screen UNDERSTATES grid coverage.** My stronger adversary finds grid
coverage growing *roughly linearly* (12→60 over m=16→256), not the √m (slope ≈0.53) the screen
reports. The qualitative conclusion ("grid is polynomial, caps the exponent") is unchanged and in
fact *strengthened* — the grid baseline is worse than advertised. But it means the screen's specific
"slope ≈0.53" number is an artifact of a too-weak rectangle family and should not be quoted as a
characterization. **The committed adversary is not tight; the reported coverage figures are lower
bounds on the true worst case.** This is the kind of thing that, left in a paper draft as a
positive-sounding "√m", would be wrong.

**Finding 2b — permutation O(1) is REAL and robust, but I located its exact mechanism, and it is in
direct tension with C1.** The permutation coverage stays flat at 4 (not 2) even under the stronger
adversary — so O(1) is genuine and not a coarse-family artifact. *Why?* I verified the mechanism
directly:
- Full bounding-box query over all cells → **coverage = 0** (a fully-contained cell is invisible
  because heavy and sparse gadgets have **equal point cardinality**).
- A quadrant with two interior edges → coverage = 2; general rects → ≤4.
- So coverage is driven *entirely* by how many cells a rectangle **edge straddles**, and in a
  permutation layout each axis-parallel line meets O(1) cells. The interior is free **only because of
  equal cardinality.**

**This is the crux the draft under-weights.** C2's O(1) coverage is not a property of the layout
alone — it is a property of *(layout) × (equal-cardinality invisibility)*. But **C1's whole burden is
to make the heavy gadget shift global MST weight by a constant fraction at the n^{1/2} budget**, and
the naive way to do that (which the C1 screen shows is already failing — heavy/sparse MST ratio ~√p
falls short of the needed ~m) pressures the construction toward a *more aggressive* heavy gadget. If
the point-efficient gadget achieves its larger MST cost by using **unequal cardinality** (e.g. more
points in the heavy cell), then contained cells become **visible to counting** and coverage
**explodes** — exactly the B3 danger. The draft says "coupling is the open problem," which is
correct, but it presents the permutation O(1) as nearly-banked good news. **It is not bankable: the
same equal-cardinality assumption that buys O(1) coverage is what the source already uses, and the
source is stuck at n^{1/3}.** The novelty must come from a gadget that is *both* point-efficient
*and* equal-cardinality (or that keeps coverage O(1) despite a cardinality signal) — and there is
currently zero evidence such a gadget exists.

**Finding 2c — the Δ=O(n) budget for the permutation layout has ZERO slack.** I checked the budget
arithmetic. With m = n^{1/2} cells and cell side s = n^{1/2}:
- Grid layout: Δ ≈ 0.01–0.03·n — comfortable.
- Permutation layout (cells placed on a line, m×m slot grid, m occupied): **Δ = exactly 1.00·n** at
  s = n^{1/2}, and this is *before* C1 is allowed to demand a larger cell to spread its points for a
  bigger MST cost. Any increase in cell side to satisfy C1 pushes Δ past O(n). So the permutation
  layout that delivers O(1) coverage sits *on the boundary* of B1, and the C1×C2 coupling is even
  tighter than the draft conveys: it is a **simultaneous** three-way squeeze (point-efficiency ×
  equal-cardinality × Δ=O(n)-with-no-slack), not two loosely-coupled obligations.

**On C1 specifically:** the draft's read ("naive gadget insufficient, not dead") is sound and
honestly hedged in the code's pre-registration. The gap_frac declining with scale at θ=1/2
(0.128→0.086→0.064) is a real warning, correctly labelled a *construction obligation* rather than a
barrier. The negative control (0.0) is clean. No objection there — except to note that "detectable
survives down to ~n^{0.54}" is a finite-n curiosity, not asymptotic evidence; at θ=0.54 you do not
have m=n^{1/2} candidates, you have m=n^{0.46}, which would cap the bound at **n^{0.46}, i.e. an
"improves," not a "closes."** That row should not be read as encouraging for the full target.

**Net on Section 2:** the draft is **not** fabricating optimism, but it is **explaining away the
permutation result one notch too generously.** The correct framing: *permutation shows O(1) coverage
is attainable in isolation under equal cardinality, but the equal-cardinality assumption is exactly
what C1's point-efficiency requirement threatens, and the layout that gives O(1) coverage has no
Δ-budget slack. The coupled object — point-efficient + equal-cardinality + O(1)-coverage + Δ=O(n) —
has no positive evidence yet; the screens neither support nor refute its existence.* That is weaker
than "evidence SUPPORTS attempting the full target"; it is "no proof-of-death, but the central
positive object is entirely unconstructed and faces a genuine three-way squeeze."

---

## 3. §10 Paper-Orientation — three questions

**① Is the contribution (if C1+C2+C3 close) enough for SODA, and on-topic? What is missing?**
Yes, conditionally. *Closing* the Ω(n^{1/3})→Õ(√n) gap for a clean, recently-published (SoCG 2025)
geometric oracle model with a tight Ω(n^{1/2−o(1)}) lower bound is a crisp, on-topic, clearly-SODA
result — a single decisive theorem against a named open gap is exactly the kind of contribution the
first ~10 pages can sell. The topic (sublinear geometric oracle complexity) is squarely in scope.
**What is missing is the entire mathematical content:** C1 (point-efficient equal-cardinality
gadget) and C2 (O(1)-coverage counting packing compatible with C1 under Δ=O(n)) are *both
unconstructed*, and C3 (the Yao/hitting packaging that reaches Ω(m), dodging the B2 Ω(log m) trap)
is unwritten. Nothing is proven yet (the ledger says so honestly). So: the *shape* is SODA-worthy;
the *substance* is 0%. The screens are de-risking, not results.

**② Has the thinking DRIFTED?** Largely no — and this is a genuine strength. The frozen model, the
three barriers (B1 budget / B2 log-m trap / B3 counting⊋emptiness), and the "closes vs improves"
strength gate are all kept front-and-center, and the team explicitly rejected the dyadic/round-
elimination axis as misaligned. Two minor drift risks to flag: (a) the MI-ratio measurements are
pedagogically nice (they illustrate B2) but are *not* load-bearing for the result and should not
expand into a sub-investigation — coverage, not bits, is the operative quantity, and the screen
already shows MI misses the polynomial growth; keep MI as a one-paragraph illustration, no more.
(b) The "permutation layout" is a *probe*, explicitly "NOT the RS proof obligation" (per the code
comment) — there is a latent risk of the attack loop sliding from "permutation works in sim" toward
treating permutation-with-equal-cardinality as the construction, which Section 2b shows is not
banked. Watch that.

**③ Other problems — boundary / over-claiming / Czumaj.**
- *Czumaj boundary:* correctly stated (emptiness / deterministic / O(n^{1/4})-error / Ω(√n)); the
  web result confirms it; the "does not transfer to counting" framing is right. No mis-statement.
- *Over-claiming:* the one place the draft leans past its evidence is the C2 conclusion ("evidence
  SUPPORTS attempting the full n^{1/2−o(1)}"). Per Section 2, the honest statement is weaker: no
  proof-of-death, but the central positive object is unconstructed and triple-squeezed. Do not let
  this sentence harden into a claim.
- *Numbers that should not be quoted as-is:* the grid "slope ≈0.53 / √m" is an under-powered-adversary
  artifact (true worst-case grows faster — Section 2a); and "detectable down to n^{0.54}" is an
  improves-regime, not a closes-regime, signal (Section 2b). Neither belongs in a paper as positive
  evidence for n^{1/2}.
- *Process:* the missing `lit/SCAN_REPORT.md` and `PHASE0_REPORT.md` (Section 0).

---

## 4. Bottom-line recommendation for human gate #1

**Pursue the full n^{1/2−o(1)} ("closes") target as the primary objective, but enter Phase 1 with the
C1×C2×B1 coupling as a single, explicitly time-boxed kill-experiment — and a pre-committed
"improves" fallback.** Reasoning:

1. The *upside is the whole point*: only "closes" is a clean, headline SODA result against a named
   gap. "Improves" (e.g. n^{0.46} from the θ=0.54 regime, or some intermediate exponent) is a
   weaker, harder-to-sell contribution and should be the fallback, not the aim.
2. **No proof-of-death fired**, and the literature is GREEN — so attempting the full target is
   legitimate, not reckless.
3. **But the optimism is one notch too high.** The decisive open object is the *coupled* gadget
   (point-efficient **and** equal-cardinality **and** O(1)-coverage **and** Δ=O(n)-with-no-slack),
   and there is currently *zero* positive evidence it exists — the permutation O(1) result is real
   but rests on exactly the equal-cardinality assumption that C1's point-efficiency threatens, on a
   layout with no budget slack. So the first Phase-1 milestone must be the **construction of a single
   point-efficient equal-cardinality heavy gadget that shifts w(P) by ε at the n^{1/2} budget** — if
   that cannot be built (or forces unequal cardinality, blowing up coverage), the "closes" target is
   effectively dead and the team should fall back to the best provable "improves" exponent without
   sinking the full timeline (deadline 2026-07-09 is tight).
4. Before sign-off: commit the kill-scan and Phase-0 verdict as files (Section 0), and tighten the C2
   adversary in any re-run so reported coverage numbers are worst-case, not artifacts (Section 2a).

**Confidence note:** I would revise the inherited ~50% "closes is reachable" down to roughly
**35–40%** on the basis of the three-way squeeze in Section 2 — not because anything is refuted, but
because the central construction is unconstructed and the one piece of positive sim evidence
(permutation O(1)) is less load-bearing than it looks. This is an *attack-harder* signal (per the
guide's §9.0b), not a downgrade.

---

## VERDICT

**ON-TRACK** — orientation is correct, the gap is real and unclaimed (GREEN literature confirmed by
independent spot-check), no proof-of-death fired, and the goal has not drifted. The one substantive
correction: the C2 permutation O(1) is genuine but **not bankable** — it rides on an
equal-cardinality assumption in direct tension with C1's point-efficiency, on a Δ=O(n) layout with
zero slack, so the *coupled* construction is the entire (unconstructed) ballgame.

**Gate-1 recommendation:** Approve GREEN and proceed to Phase 1 targeting full **n^{1/2−o(1)}
("closes")**, with the C1×C2×B1 coupled gadget as a *time-boxed first kill-experiment* and a
pre-committed "improves"-exponent fallback; first commit the missing kill-scan / Phase-0 artifacts
to make the verdict auditable.
