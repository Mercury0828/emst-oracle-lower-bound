# Research-Line Ledger — emst-oracle-lower-bound

> **Append-only.** The single most valuable artifact (guide.md §9.5). Re-read this ledger +
> `PROJECT_STATE.md` + frozen artifacts BEFORE continuing any round — never work from memory
> (memory ⇒ exponent drift n^{1/2} vs n^{1/2−o(1)}, Δ/ε/a/b notation collisions, repeated labor).

## HEADLINE
**[2026-06-21] 🔴 Phase 1 Rounds 1–2 DONE — the entire gadget-packing LB approach is (near-)refuted;
AT A §9.6 HUMAN KILL/PIVOT GATE.** The Ω(n^{1/2−o(1)}) **lower-bound** target via the planned approach
is near-dead: BOTH the single-needle ([[P1]]/[[N1]], Round 1) AND the multi-needle/planted-pattern
escape ([[P2]]/[[N2]], Round 2) **provably cap at n^{1/3}** — exactly the existing source bound, NO
improvement (not even "improves"). Verified by codex GPT-5.5-xhigh + **3 independent audits**
(analytic + 16+ exact-EMST/coverage probes; Audit C = NEAR-PROOF-OF-DEATH). Not a *full* proof-of-death
(one narrow, evidence-against "new primitive" loophole survives; a blanket impossibility is barred by
the existing Ω(n^{1/3})). **Confidence an Ω(n^{1/2−o(1)}) LB even exists: ~30%** (the obstruction is
essentially algorithmic ⇒ the truth is likely Θ(n^{1/3}) and Õ(√n) is loose). 🔑 **Substrate-supported
pivot:** prove a **sub-√n / Õ(n^{1/3}) UPPER bound**, closing the gap *from above* (different, equally
SODA-worthy). **Owner decision needed** (§9.6): escalate-to-web-Pro on the loophole vs pivot-to-upper-
bound vs pivot-to-EMD vs barrier-paper vs stop. Phase-0 kill-scan remains GREEN; no scoop/ceiling.

---

## Frozen model / notation (from guide.md §4 — freeze to avoid drift)

- **Point set:** P ⊂ [Δ]² integer grid, |P| = n, **spread/domain Δ = O(n)** (source's budget;
  the lower bound must respect it).
- **EMST weight:** w(P) = total Euclidean length of the MST of P. Target = a **(1±ε)
  multiplicative** estimate of w(P), fixed constant ε ∈ (0,1).
- **Oracle:** orthogonal range-**counting** oracle — query = axis-aligned rectangle R; returns the
  **exact integer** |P ∩ R| (NOT a 0/1 emptiness bit). Cost = #queries. Contrast: emptiness oracle
  returns only 1{P∩R≠∅}. **Counting ⊋ emptiness** (the boundary that keeps this open).
- **Hard-instance template:** domain split into equal cells; one uniformly-random "hidden" cell gets
  a **heavy** gadget, the rest get **sparse** gadgets; the heavy cell shifts w(P) by ≥ ε·w(P).
  - Source params (re-confirm from arXiv:2504.15292 §6): **16·n^{1/3} cells**, **n^{2/3} pts/gadget**,
    heavy EMST cost **Θ(n^{7/6})**, sparse **Θ(n^{5/6})**, each query hits **≤4 cells**.
  - Target params (to construct): **Θ(n^{1/2}) cells**, **~n^{1/2+o(1)} pts/gadget**, heavy/sparse
    EMST-cost separation still **(1±ε)-detectable** on w(P).
- **Hard distribution (Yao):** YES = one heavy gadget at uniformly-random hidden cell among
  m=Θ(n^{1/2}) candidates + sparse elsewhere; NO = all-sparse. A query that does NOT *hit* the
  hidden cell returns an identical answer under YES and NO.
- **Coverage / candidate-distinguishing-power (operative quantity):** for a query rectangle R, the
  #candidate cells whose heavy/sparse flip can change |P∩R|. Target claim **(C2): O(1)** per query.
  Hitting bound = **Ω(m / coverage)**: coverage O(1) — indeed any m^{o(1)} — yields Ω(n^{1/2−o(1)});
  only polynomial coverage h(m)=m^{Ω(1)} caps the exponent below 1/2.
- **(C1) target cost inequality (exact exponents are an attack-loop obligation):** at the n^{1/2}
  budget, heavy per-cell cost Θ(n^a), sparse Θ(n^b) (a>b), Θ(n^{1/2}) cells. Require
  **Θ(n^a) − Θ(n^b) ≥ ε·w(P)** (heavy excess a constant fraction of the *global* MST weight).
  Source worked example a=7/6, b=5/6 is at the n^{2/3} budget and does NOT carry over unchanged.

---

## Proven results `P*` — "use freely, do not re-derive"
- **P1 [2026-06-21] — Single-cell gadget-swap cap (a verified impossibility for the planned route).**
  In the model of **m pairwise-disjoint, equal-cardinality gadget cells** (each = p points in a region
  of side s; one "heavy", rest "sparse") on the integer grid [Δ]², Δ=O(n), mp=n:
  - **(UB)** a single-cell heavy↔sparse swap changes the global EMST by **|Δw(P)| ≤ O(s√p)**
    (geometry-agnostic — fractal/hierarchical/nested cannot beat it; the `EMST ≤ Cs√p` grid/snake
    bound + a splice argument; the "MST monotonicity" phrasing in the attacker reply is technically
    wrong but the inequality holds — Audit A stress-tested |gap|/(s√p) ≤ 1.0 on adversarial configs).
  - **(LB)** **w(P) ≥ Ω(s·m)** (needs only disjointness — total cell area ≥ m·s² — NOT tiling; covering
    + tube-area O(rL+r²) argument; Audit A strengthened "tiling" → "disjoint").
  - **⇒** single-needle relative gap **gap/w(P) ≤ O(√p/m) = n^{3c/2−1}** (p=n^c, m=n^{1−c}); the **s
    cancels** (verified symbolically) so it is scale-invariant (spread vs packed). A constant-fraction
    detectable gap requires **c ≥ 2/3 ⇒ m ≤ n^{1/3}**, i.e. EXACTLY the source Ω(n^{1/3}) — **NO
    improvement.** Sharp at c=2/3 (the source uniform-grid/strip construction).
  - **Verified by:** attacker codex GPT-5.5-xhigh (`attack_loop/round1_C1_response.md`) + 2 independent
    fresh-context audits — Audit A (rigor, `round1_C1_auditA.md`) + Audit B (escape, `round1_C1_auditB.md`)
    — analytically and with exact-EMST numerics (`attack_loop/auditB_probe*.py`).
- **P2 [2026-06-21] — Multi-needle / active-subset cap (extends P1 to the escape route).** Under the
  O(1)-coverage requirement (which forces O(1) projection-multiplicity ⇒ M·s ≤ O(Δ) = O(n) ⇒ s ≤ O(p),
  p=n/M; verified numerically: adversarial coverage ≈ 1.5–2× projection multiplicity, a 1-D per-axis
  fact the 2-D area cannot escape), if k of the M candidate cells are class-active then the total EMST
  gap ≤ O(k·s·√p) (additivity of [[P1]] — verified, no super-additivity), while w(P) ≥ Ω(max{sM, n}) =
  Ω(n). A constant relative gap forces **k ≥ Ω(M/√p)**, so the hitting bound **M/k ≤ O(√(n/M))**;
  maximizing min{M, √(n/M)} gives **M = n^{1/3}, bound n^{1/3}** (at M=√n only n^{1/4}). The
  bulk-parity/coding escape is *quantitatively* dead: in the forced spread layout EMST is additive to
  ~1.3% and a marginal-matched global-parity coupling shifts EMST by 0.11% of w (not Θ(w)).
  - **Verified by:** codex GPT-5.5-xhigh (`attack_loop/round2_escape_response.md`) + independent Audit C
    (`attack_loop/round2_auditC.md`, classification **(a) NEAR-PROOF-OF-DEATH**, 8 exact-EMST/coverage
    probes). **Caveat (not a FULL proof-of-death):** the existing Ω(n^{1/3}) bound forbids any blanket
    "polylog queries distinguish every constant EMST gap" theorem, so a *fully general* impossibility
    cannot hold; one narrow loophole survives — see the open problem below.

## Refuted routes `N*` — "do NOT attempt" + killing reason
- **N1 [2026-06-21] — The guide's core lever is DEAD: "raise hidden cells from Θ(n^{1/3}) to Θ(n^{1/2})
  via a single hidden heavy gadget among m disjoint equal-cardinality cells."** (guide §1 "the lever",
  §6 Components 1–3 as written.) Killing reason = **[[P1]]**: this single-needle route provably caps at
  c=2/3 (m=n^{1/3}), giving NOT EVEN an "improves" — it reproduces the existing bound. **Do NOT** retry
  via: a cleverer heavy gadget geometry (UB is geometry-agnostic); a non-tiling / packed layout (s
  cancels); coincident/cluster-sparse points (w(P) is backbone-dominated); or unequal cardinality (that
  escapes C1 only by making the needle visible to one coarse counting query ⇒ [[B2]] Ω(log m) collapse).
- **N2 [2026-06-21] — The multi-needle / planted-pattern escape is (near-)DEAD too.** Killing reason =
  **[[P2]]**: the active-subset multi-needle caps at n^{1/3} under O(1) coverage; the bulk-parity/coding
  variant is quantitatively dead (EMST too local to carry a Θ(w) marginal-hidden signal). **Do NOT**
  retry via active-subsets or low-order-marginal-matched parity patterns. The ONLY thing P1+P2 do NOT
  refute is the narrow "new primitive" (open problem below) — and the evidence runs against it.
- Candidate to watch (NOT yet refuted, from guide.md decision log): the **scale-by-scale / dyadic
  round-elimination** framing was the *rejected, misaligned* attack axis in the idea-refine; the
  frozen axis is **needle-in-haystack**. Round-elimination, if used, must reach Ω(m), not Ω(log m).

## Barriers `B*` (in force — every brief must respect these)
- **B1 — n-point / Δ=O(n) budget.** Total points |P|=n and domain spread Δ=O(n). #cells × pts/cell
  ≤ O(n). This is what caps the source at Θ(n^{1/3}) cells (16·n^{1/3} × n^{2/3} = 16n) and what any
  denser packing must still respect (Θ(n^{1/2}) cells × ~n^{1/2} pts = n^{1+o(1)}).
- **B2 — the Ω(log m) trap (a PROOF barrier).** Locating 1-of-m candidates is only log m bits, so a
  naive mutual-information / bit-accounting argument gives only Ω(log m) — exponentially short of the
  Ω(m) target. The lower bound is a **geometric hitting/coverage** argument, NOT bit-accounting. Any
  INDEX / augmented-indexing / round-elimination formalization MUST be checked to deliver Ω(m), not
  Ω(log m). 🔴 Never write "O(1) bits/query ⇒ the lower bound" into a brief.
- **B3 — counting ⊋ emptiness, so coverage can exceed 1.** A counting query returns an exact integer
  (a sum over whatever cells R covers), not a 0/1 bit, so a large rectangle's count may be jointly
  sensitive to ω(1) candidate cells. This is the genuine danger for (C2): if coverage grows
  polynomially with m, the exponent caps below 1/2. 🔴 Never write "Czumaj emptiness Ω(√n) ⇒ a
  counting Ω(√n)" or "sparse gadget ⇒ O(1) coverage" into a brief.
- **B4 [2026-06-21] — single-cell gap cap (from [[P1]]).** Any hard distribution that routes its w(P)
  difference through a **single** changed cell of side s with p points is capped at gap ≤ O(s√p), hence
  (with the backbone LB) at m ≤ n^{1/3} candidates. ⇒ A route to m=ω(n^{1/3}) candidates MUST make the
  detectable difference **correlated across ω(1) cells** (a multi-needle / planted pattern). But then a
  new obstruction bites: a bulk/correlated Θ(w(P)) shift is **cheaply estimable by O(polylog) coarse
  counting queries**, so the Ω(m) information must hide in a pattern that *aggregate rectangle counts
  cannot reveal* (re-winning C2/C3 informationally). 🔴 Never write "a big global gap ⇒ a query lower
  bound" — a big gap that is coarsely estimable gives NO lower bound (it is the [[B2]] trap at the
  query level).

---

## The exact open problem, as currently reduced
**[2026-06-21] REDUCED after the round-1 refutation [[N1]]/[[P1]].** The single-needle gadget-packing
route (the guide's original §1/§6 plan) is DEAD. The ONLY surviving direction toward Ω(n^{1/2−o(1)}) is:

> **Construct a MULTI-NEEDLE / PLANTED-PATTERN hard distribution** over [Δ]² (Δ=O(n), |P|=n): a
> distribution over *which coordinated subset / multi-scale pattern of cells is "heavy"* such that
> (i) the global Euclidean MST gap between the two pattern-classes is **Θ(w(P))** even at the
> p≈n^{1/2} budget (already shown achievable — a Θ(m)-cell coordinated difference gives gap fraction
> 2–4, [[S2]]/Audit B probe3), AND (ii) the *pattern* encodes **Ω(m)=Ω(n^{1/2}) bits** of which any
> single axis-aligned range-**counting** query reveals only **o(1)** (low coverage), so locating/learning
> the pattern still costs **Ω(m) = Ω(n^{1/2−o(1)})** queries — dodging the [[B2]]/[[B4]] "Ω(log m), not
> Ω(m)" trap at the query level (a bulk shift that is coarsely estimable gives NO bound).

The hard part has moved from **C1-geometric** (now easy — a correlated gap is trivial) to
**C2/C3-informational**: hide Ω(m) bits in a pattern that *no* rectangle's exact count can cheaply
reveal.

**[2026-06-21 UPDATE — this escape is now (near-)refuted too ([[N2]]/[[P2]]).** Round 2 + Audit C
(NEAR-PROOF-OF-DEATH) cap the active-subset multi-needle at n^{1/3} and quantitatively kill the
bulk-parity variant. The ENTIRE gadget-packing/planted-pattern lower-bound approach caps at n^{1/3}.
The ONLY surviving sliver is:

> **Open (narrow, evidence-against):** does there exist a "new primitive" — a p-point cell of side
> s=Θ(p) whose LOW/HIGH EMST gap is near the [[P1]] maximum Θ(s√p), while every axis-aligned rectangle's
> exact count is class-independent unless it hits a low-coverage (O(1)) hidden subconfiguration? All
> tested near-max-gap cells have count-discrepancy ≥ Ω(√p)=ω(1) (coarsely visible), so the evidence
> runs against existence. Not formally impossible (a fully general impossibility is barred — the
> existing Ω(n^{1/3}) forbids a blanket "polylog distinguishes every constant gap" theorem).

🔑 **The insight that flips the project (key for the pivot decision):** the reason the lower bound caps
is that **a constant-fraction EMST gap is cheaply estimable by O(polylog) coarse range-counting queries**
— this is essentially an *algorithmic* statement. It is strong evidence the TRUTH is **Θ(n^{1/3})** and
the **Õ(√n) upper bound is loose**, pointing at the natural pivot: **prove a sub-√n (ideally Õ(n^{1/3}))
UPPER bound**, closing the Driemel et al. gap *from above* — a different but equally publishable SODA
result the substrate (P1/P2 + coverage machinery) directly motivates. **This is a §9.6 human kill/pivot
gate** (presented to the owner; not started autonomously).

## Phase-0 screen findings `S*` (de-risking evidence, NOT proofs — guide.md §7)
- **S1 (C1).** With the faithful source gadget (heavy uniform grid / sparse strip, equal cardinality),
  the heavy-vs-sparse global-w(P) gap fraction is Θ(1) at p≈n^{2/3} but **declines as p→n^{1/2}** and,
  at the full n^{1/2} budget, **decreases with n** (0.128→0.086→0.064 at n=2025/4096/8100; ε=0.10).
  Survives detectability only to ~p≈n^{0.54}. Negative control (heavy:=strip) = 0. ⇒ the *naive*
  gadget does not support n^{1/2}; a more point-efficient heavy gadget (heavy/sparse ratio ~m, not
  ~√p) is the C1 attack obligation. Necessary screen, not a kill. Artifact: `sim/results.json`.
- **S2 (C2).** Baseline **grid** packing: adversarial max per-query COUNTING coverage grows like
  **√m** (slope ≈0.55, const ≈3.5–4; tight coordinate-snapped adversary) — a rectangle's edges slice
  √m-cell columns/rows. ⇒ grid layout caps the bound at Ω(m/√m)=Ω(√m)=~n^{1/4} (realizes the residual
  risk on the baseline). **Permutation** (general position, disjoint x- AND y-bands): coverage **flat
  O(1)** (=4, slope ≈0.00) ⇒ √m is a grid artifact. Counting coverage ≈ 2× emptiness (confirms
  counting ≥ emptiness). The **MI/log-m ratio declines** (0.54→0.16) as m grows even while coverage
  grows √m — empirical proof bit-accounting misses the growth ([[B2]] Ω(log m) trap). Artifact:
  `sim/figures/c2_coverage.png`. ⚠️ **NOT bankable (gate-1 audit):** permutation O(1) rides entirely
  on **equal-cardinality invisibility** (a fully-contained cell is invisible only because heavy &
  sparse have equal point count) — exactly what [[S1]] point-efficiency threatens (an unequal-card.
  heavy gadget makes contained cells visible ⇒ coverage explodes, the [[B3]] danger) — AND the
  permutation layout sits at **Δ=1.00·n, zero slack** vs [[B1]]. ⇒ the open C2 object is a
  **three-way squeeze**: point-efficient × equal-cardinality × O(1)-coverage × Δ=O(n), no positive
  evidence yet.

## Confidence trend (% that the full n^{1/2−o(1)} "closes" target is reachable, with dates)
- **[2026-06-20] (pre-screen, inherited):** ~50% (idea `conditional`, refine-flipped fail→pass; the
  two cruxes unverified). This is a first-class signal: a sustained drop ⇒ escalate / attack harder
  (per §9.0b), never a downgrade.
- **[2026-06-20] (post Phase-0, pre-audit):** ~50%.
- **[2026-06-20] (post-gate-1 audit, ADOPTED):** **~38%.** Three-way squeeze; no positive evidence
  the coupled object exists.
- **[2026-06-21] (post Round-1 refutation, ADOPTED):** **~18%** (probability of a tractable route to
  the full target). Single-needle route provably dead ([[P1]]).
- **[2026-06-21] (post Round-2 + Audit C, ADOPTED):** **~30% that an Ω(n^{1/2−o(1)}) LB even EXISTS**
  (re-based to the existence question, matching codex's ~35% and Audit C's ~30%). The whole
  gadget-packing/planted-pattern approach caps at n^{1/3} ([[P2]]/[[N2]]); only a narrow,
  evidence-against loophole survives. The obstruction is essentially *algorithmic* (a constant EMST gap
  is coarsely count-estimable) ⇒ the truth is likely Θ(n^{1/3}), Õ(√n) loose. Per §9.0b this is the
  **science** (route(s) refuted), NOT a difficulty-driven downgrade. **Now at the §9.6 human gate** —
  the owner decides escalate-vs-pivot-vs-stop; I do NOT start a new line autonomously.
