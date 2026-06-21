# Project Constitution — Tight Query Lower Bound for Euclidean MST Weight under Range-Counting Oracles

> **This file is READ-ONLY for the executing agent.** It is the research constitution. Do not
> edit it. All amendments — design decisions, scope changes, results that contradict a plan
> here — go into `docs/guide_amendments.md` (append-only). The agent's running state lives in
> `PROJECT_STATE.md` and `DESIGN_DECISIONS.md` (see §9).
>
> **Status: Phase 0 NOT passed. Nothing in this document is a proven result.** Every theorem,
> lemma, and construction below is a *claim to be established* with a stated verification method
> and a stated failure-logging rule. Treat all bounds as conjectural until the corresponding
> proof is frozen in `PROOF_REVIEW`. The idea is `conditional` (refine-flipped, not delivered):
> its load-bearing crux is unverified and is exactly what Phase 0 must stress-test.
>
> **Regenerated 2026-06-20** (re-run of `/idea-deepdive` after the 2026-06-20 `/idea-refine` flipped feasibility fail→pass). The science (§0–§8) was already aligned with the refined attack; this regeneration installs the **external-solver attack & audit loop** as the standard workflow (§9), replacing the earlier linear "Claude proves it on a fixed Phase 0→5 pipeline" framing — per `guide_feedback/00–02` and `deepdive/_templates/external_solver_attack_playbook.md`.

---

> **🎯 Paper-first discipline + per-phase contribution gate (added 2026-06-18).** This project exists to **produce a paper submittable to the target venue**, not to do open-ended, unlimited research — weigh every phase decision by "does this help get the paper submitted?". **At the gate of every phase, spawn one independent subagent** and give it the current frozen results / contribution summary + the target-venue requirements (`venue-prompts/<venue>/` or the live CFP). It judges: ① is the current contribution **already, or on track to be, enough to submit to this venue/journal** (weighty enough, on-topic, and what is still missing)? ② has the thinking **drifted** — slid into publication-irrelevant open-ended tangents / over-generalization / forgetting the paper goal (**the main agent forgets this easily**)? ③ any other problem (boundary collapsed, claims exceeding what is provable)? **Correct course on its advice** (cut tangents / add the missing load-bearing contribution / narrow to a submittable scope / or escalate a redirect that needs a human decision), and log the check + correction in `PROJECT_STATE.md` and `DESIGN_DECISIONS.md`. Goal: keep converging on a submittable paper, not researching indefinitely.

## §0. Header

- **Working name:** `emst-oracle-lower-bound` — "An Ω(n^{1/2−o(1)}) Query Lower Bound for
  (1±ε)-Estimating the Euclidean MST Weight in the Orthogonal Range-Counting-Oracle Model."
- **One-line thesis:** Close the Ω(n^{1/3}) vs Õ(√n) gap left open by Driemel–Monemizadeh–
  Oh–Staals–Woodruff (SoCG 2025, arXiv:2504.15292) by proving a query lower bound of
  Ω(n^{1/2−o(1)}) — matching their Õ(√n) upper bound up to subpolynomial factors — via a
  **space-efficient heavy gadget** that raises the number of independent hidden cell-locations
  from Θ(n^{1/3}) to Θ(n^{1/2}) within the *same* Δ=O(n) / n-point budget, combined with a
  **per-query O(1)-cell coverage bound** (each range-counting query is jointly sensitive to only
  O(1) candidate cells) packaged as a Yao / distributional hitting argument over the hidden
  locations.
- **Target venue: SODA (ACM-SIAM Symposium on Discrete Algorithms).** Owner-set (explicit at
  invocation) and also the idea's first listed canonical venue. **SoCG is the sibling venue**
  (the source paper's home, and the idea's second listed venue); if at any point the result is
  framed for SoCG instead, the structural conventions are nearly identical (single-column, no
  hard page limit, full proofs in appendix) — but the default and primary target is **SODA**.
  - Venue YAML: `venues/conferences/soda.yaml`. SODA 2027 full-paper deadline **2026-07-09**
    (Philadelphia, 2027-01-24–27). **Phase 0 MUST re-confirm format / blind / deadline against
    the current official SODA 2027 CFP** — page and blind policies change by year.
  - Format (per YAML, to re-verify): **single-column, 11pt, 1-inch margins** (font/margin
    violation = summary rejection — the "shrink font / squeeze margins" lever is FORBIDDEN);
    **no hard page limit** but the **first ~10 pages after the title page must convey the full
    merits** (problem, prior-bound positioning, key technique, formal theorem + proof sketch);
    **appendix unlimited, references not counted** → full proofs sink to the appendix; recent
    SODA (2024+) trends to **light double-blind** — write anonymized from day 1 if double-blind.
  - **Writing pipeline (already built): `venue-prompts/soda/`** — 4 stages used in Phase 5:
    `1-results-selfcheck.md` (freeze theorems/proofs, multi-lens proof review),
    `2-writing-guide.md` (structure-clone a SODA exemplar + component-mapping table),
    `3-page-trim.md` (sink full proofs to appendix; keep first 10 pages tight),
    `4-pre-submission-check.md` (compliance, double-blind, refs). Do NOT use them before Phase 5.
- **🔴 The central quantitative gate ("closes" vs merely "improves").** The idea's verified fit
  analysis is explicit: a top-theory PC distinguishes **"closes the gap"** (reaches Ω(n^{1/2−o(1)})
  matching Õ(√n) up to n^{o(1)}) from **"improves the gap"** (e.g. only reaches Ω(n^{2/5})). Both
  are publishable, but the SODA headline strength depends on which. This is **not** a venue-
  redirect decision (unlike some deepdives) — SODA fit is genuine either way — it is the
  **strength-of-result gate**, and it is driven entirely by the load-bearing residual risk below.
- **🔴 Load-bearing residual risk (idea `extras.residual_risk`, ELEVATED here to the Phase-0 kill
  criterion).** The whole bound rests on TWO coupled, unverified claims: **(C1)** a heavy gadget
  using only **~n^{1/2+o(1)} points per candidate cell** that *still* induces a **(1±ε)-level
  detectable MST-weight gap** vs the sparse gadget (so Θ(n^{1/2}) independent hidden locations
  pack into the same n-point budget); and **(C2)** that under this denser packing a single
  orthogonal **range-COUNTING** query is **jointly sensitive to only O(1) of the candidate cells**
  — i.e. its answer can help distinguish/locate among only O(1) candidates (the *coverage* /
  *candidate-distinguishing-power* quantity; see the framing note below). ⚠️ The genuine danger
  for (C2): a counting query returns an *exact count* (a sum over whatever cells the rectangle
  covers), not a 0/1 emptiness bit, so a large rectangle's count may be **jointly sensitive to
  ω(1) candidate cells** — which would let o(#cells) queries cover/distinguish all candidates and
  cap the achievable exponent **below 1/2**, degrading the result from "closes" to "improves."
  Phase 0 must screen both (C1) and (C2) at small scale **before any full proof effort is sunk.**
- **🔴 FRAMING NOTE — the lower bound is a HITTING/COVERAGE argument, not a bit-counting argument
  (read before §6).** The source Ω(n^{1/3}) is *not* an information-accounting bound. It is a
  **Yao / distributional hitting bound**: under the hard distribution one cell is the heavy
  "needle" at a uniformly-random location (YES) vs all-sparse (NO); a query that does not *hit*
  the heavy cell returns the same answer in both worlds; each query rectangle is sensitive to only
  O(1) cells, so o(#cells) queries fail to hit the random needle ⇒ cannot distinguish YES/NO ⇒
  Ω(#cells). **Naive mutual-information accounting is a TRAP here:** locating 1 of m candidates is
  only log m bits, so "O(1) bits/query" would give only Ω(log n) — exponentially short of the
  target. The operative load-bearing quantity is therefore **geometric: how many candidate cells a
  single rectangle's count is jointly sensitive to (coverage), NOT how many bits it carries.** Any
  INDEX / augmented-indexing / round-elimination *formalization* (§6 Component 3) must be checked
  to actually deliver Ω(#cells), not Ω(log #cells); it is one possible packaging of the hitting
  argument, not a shortcut around it.
- **Own-work dedup (Jason 2026-06-18 rule):** checked against the three sources via
  `python scripts/own_work_corpus.py`. **No overlap.** The two other SODA / discrete-algorithms
  delivered ideas are `mts-sublinear-smoothness` (online metrical task systems with predictions)
  and `dynamic-weighted-mis-fat-objects` (dynamic geometric MWIS) — both different problems with
  no shared contribution. All remaining own work is quantum / energy / DRO. Proceed freely. (If
  Phase 0 pivots scope — e.g. to a different oracle or a different geometric estimation problem —
  re-run `own_work_corpus.py` to re-close the dedup loop. **An exponent downgrade (closes→improves)
  is NOT a scope pivot** — same problem, same model — so it does not require re-running dedup.)

---

## §1. The Idea

### Current state of the art (the gap this paper closes)

Driemel–Monemizadeh–Oh–Staals–Woodruff, *"Range Counting Oracles for Geometric Problems,"*
**SoCG 2025 (arXiv:2504.15292)** introduce the **orthogonal range-counting-oracle** model and,
for **(1±ε)-estimating the weight of the Euclidean minimum spanning tree (EMST)** of n points,
prove:

| bound | value | source |
|---|---|---|
| **upper** | **Õ(√n)** oracle queries | Driemel et al. SoCG 2025, Thm 30 |
| **lower** | **Ω(n^{1/3})** oracle queries | Driemel et al. SoCG 2025, Lemma 32 |
| **THIS paper (TARGET, if proved — not yet established)** | **Ω(n^{1/2−o(1)})** oracle queries | ← the open cell, matching Õ(√n) up to n^{o(1)} |

(The source lower bound is a **constant-factor (multiplicative O(1)) randomized** lower bound, Lemma
32 — which *a fortiori* lower-bounds (1±ε) estimation; state it that way, do **not** claim the source
proves a bound specifically for the (1±ε) regime.) The Ω(n^{1/3}) vs Õ(√n) gap is **real and explicitly left open** by the authors. No follow-up
closes it (verified to 2026-06-18; the only citing paper, arXiv:2603.20943 on convex-hull
approximation, uses a *different* oracle for a *different* problem — see §3).

### Why this path is plausible (the core argument — read the source proof, do not trust this)

- **The source Ω(n^{1/3}) is a "needle-in-haystack," NOT a "resolve-the-scales" bound.** (This
  diagnosis is the entire reason the idea was refined; an earlier scale-by-scale framing was
  rejected as misaligned.) The verified structure of the source hard instance (arXiv:2504.15292
  §6, Lemmas 31–32 — **Phase 0/1 must re-read the PDF and re-confirm every number below**):
  - Domain [Δ]² with **Δ = O(n)**, split into **16·n^{1/3} equal cells**.
  - One uniformly-random cell receives a **heavy "uniform" gadget** (EMST cost Θ(n^{7/6})); every
    other cell receives a **sparse "strip" gadget** (EMST cost Θ(n^{5/6})).
  - Each gadget uses **exactly n^{2/3} points**.
  - **Each query rectangle hits at most 4 cells**, and *"the algorithm cannot get any information
    for the cells not hit by queries."*
  - So a query hits the heavy cell with probability ≤ 1/(4·n^{1/3}) ⇒ **~n^{1/3} queries needed.**
  - **Arithmetic (verify):** 16·n^{1/3} cells × n^{2/3} points/cell = 16n ⇒ the n-point budget
    **caps the number of cells at Θ(n^{1/3})**. The n^{1/3} exponent comes from the *cell count*
    under the space budget, **not** from resolving dyadic scales.
- **The lever: raise the hidden degrees of freedom from Θ(n^{1/3}) to Θ(n^{1/2}) within the same
  budget.** If a heavy gadget could be built with only **~n^{1/2+o(1)} points** while remaining
  (1±ε)-MST-detectable, then **Θ(n^{1/2}) cells × n^{1/2+o(1)} points = n^{1+o(1)}** fits the same
  Δ=O(n) / n-point budget — packing Θ(n^{1/2}) mutually-independent candidate locations. Locating
  one hidden heavy cell among Θ(n^{1/2}), with each query jointly sensitive to only **O(1) candidate
  cells** (the *coverage* quantity, NOT a bit count — see the §0 framing note), forces Ω(n^{1/2−o(1)})
  queries. **(Quantitatively: if per-query coverage is h(m) over m=Θ(n^{1/2}) candidates, the hitting
  bound is Ω(m/h(m)); coverage O(1) — indeed any m^{o(1)} — yields Ω(n^{1/2−o(1)}); only polynomial
  coverage h(m)=m^{Ω(1)} caps the exponent below 1/2.)** **The whole result is this arithmetic plus two hard constructions (§6).**

### Boundary argument (what makes the novelty stand)

- **This is a quantitative tightening of a lower bound in a freshly-introduced model, not a new
  model or a new problem.** The model and the open question both come straight from
  arXiv:2504.15292. *The entire novelty therefore rests on actually proving the improved bound.*
  Be honest about this in the writeup — the contribution is "we close the first open problem
  stated in this model," and the intro must motivate **why the range-counting-oracle model
  matters** (a clean abstraction of range-searching-as-a-model-of-computation, connected to
  sublinear geometry), not oversell a "new technique."
- **The counting oracle is strictly STRONGER than the emptiness oracle — the boundary that makes
  this open.** Czumaj et al. (exact citation a Phase-0 deliverable — *likely* Czumaj, Ergün, Fortnow,
  Magen, Newman, Rubinfeld, Sohler, "Approximating the weight of the Euclidean MST in sublinear
  time," SIAM J. Comput. ~2005; **confirm in Phase 0, do not assert as established**) prove **Ω(√n)**
  for EMST under the **range-EMPTINESS** oracle (deterministic, O(n^{1/4}) relative error). A counting algorithm
  can *simulate* an emptiness query, so a lower bound against the **weaker** oracle does **NOT**
  transfer to the **stronger** counting oracle. The source paper itself treats the counting oracle
  as strictly stronger and lists Czumaj's result as a *different model* (paraphrase — do not attribute
  a verbatim quotation without re-checking the PDF in Phase 0). This three-axis difference
  (emptiness vs counting; deterministic vs randomized; O(n^{1/4}) vs (1±ε) error) is the
  load-bearing boundary: it is *why* the counting-oracle (1±ε) randomized bound must be built from
  scratch, and *why* Czumaj's Ω(√n) is only **motivating evidence that √n is the natural truth**,
  not a proof of it.

### Nearest neighbor and the exact delta

- **vs Driemel et al. (SoCG 2025, arXiv:2504.15292) — the source / nearest neighbor.** Same
  model, same problem, same Õ(√n) upper bound. The delta is the *lower bound exponent*:
  Ω(n^{1/3}) → Ω(n^{1/2−o(1)}). The entire novelty is closing this exponent gap. Real, crisp, and
  a named open problem — but quantitatively narrow, so the proof must actually reach n^{1/2−o(1)}
  (or honestly report a weaker improvement; see the §0 strength gate).

---

## §2. Differentiation / Positioning

Positioning table — the unique row this paper occupies (oracle × error-regime × bound):

| result | oracle | error | bound type | EMST query bound |
|---|---|---|---|---|
| Driemel et al. (SoCG 2025) upper | range-counting | (1±ε), randomized | upper | Õ(√n) |
| Driemel et al. (SoCG 2025) lower | range-counting | **constant-factor**, randomized | lower | Ω(n^{1/3}) |
| Czumaj et al. | range-**emptiness** | O(n^{1/4}), **deterministic** | lower | Ω(√n) |
| **THIS (target, if proved)** | range-**counting** | **(1±ε), randomized** | **lower** | **Ω(n^{1/2−o(1)})** ← matches Õ(√n) |

**Contact surfaces and the mandated defense each forces:**

- **Against Driemel et al.** — "you just pushed our exponent; same model, same problem." *Defense:*
  the n^{1/3}→n^{1/2} jump requires a genuinely new **space-efficient gadget** (their gadget is
  ~n^{2/3} points; ours must be ~n^{1/2}) plus a **per-query O(1)-cell coverage bound under a
  denser packing** that their O(1)-cells-per-query argument does not supply at the finer grid.
  This is not a re-derivation — it confronts the "sparse-yet-MST-distinguishable" tension their
  construction leaves unexploited. Lead with the gadget + information bound; the reduction
  skeleton (INDEX direct-sum) is the scaffolding, not the contribution.
- **Against Czumaj et al.** — "Ω(√n) for EMST already exists." *Defense (must be explicit in the
  paper):* their oracle is **strictly weaker** (emptiness ⊊ counting), their regime is
  **deterministic**, and their error is **O(n^{1/4})**, not (1±ε). None of the three transfers;
  a lower bound against a weaker oracle never implies one against a stronger oracle. Cite it as
  **motivation** ("√n is the conjectured truth"), never as if it proves the counting-oracle claim.

---

## §3. Literature Landscape & Phase-0 Kill Criteria

**Kill criteria are FROZEN here, before the Phase-0 scan runs**, so the scan cannot rationalize
away a scoop or an impossibility barrier. The executing agent applies these verbatim.

### Known nearest neighbors (threat table)

| paper | id | threat | why | action if confirmed |
|---|---|---|---|---|
| Driemel–Monemizadeh–Oh–Staals–Woodruff, SoCG 2025 | arXiv:2504.15292 | **GREEN** | the source; this paper *strengthens* its lower bound | cite as foundation; re-confirm Õ(√n) upper + Ω(n^{1/3}) lower are still the state of the art (no v2/v3 or follow-up closing the gap). **Also nail down the exact lemma numbers** — the source analysis appears as "Lemmas 31–32" in one reading and "Lemma 6.1" in another; re-read the PDF and record the correct numbers in `PROJECT_STATE.md` |
| Czumaj–Ergun–Fortnow–Magen–Newman–Rubinfeld–Sohler (EMST under range-emptiness) | **(UNVERIFIED — exact cite is a hard Phase-0 deliverable)** | **YELLOW** | Ω(√n) for EMST already exists in a sibling model | get the exact citation; confirm it is range-EMPTINESS, deterministic, O(n^{1/4}) error (all three load-bearing for the §2 boundary); keep strictly separated; cite as motivation only |
| Schibler–Xue–Zhu, "Approximating Convex Hulls via Range Queries" | arXiv:2603.20943 **(UNVERIFIED — re-fetch in scan; March-2026 id, plausible but confirm it resolves)** | **GREEN** | different problem (convex hull), different oracle (emptiness) | confirm the id resolves AND that it does NOT touch the MST counting-oracle bound; the "no follow-up closes the gap" completeness claim must be **re-established by your own scan**, not inherited |

### Phase-0 kill criteria (apply after the scan)

- **RED (scooped — kill or major-pivot):** a paper already proves an **improved** randomized
  (1±ε) lower bound for EMST weight under the **orthogonal range-counting** oracle — anything
  ω(n^{1/3}), and especially Ω(n^{1/2−o(1)}) / Θ̃(√n). If it exists the headline is taken; pivot
  only if a strictly different angle survives (e.g. they prove n^{2/5} and the route to n^{1/2}
  is still open, or they leave the (1±ε) randomized case open).
- **🔴 RED (impossibility barrier — kill the n^{1/2} target):** a published result shows the
  counting-oracle EMST query complexity is **n^{1/2−Ω(1)}** — i.e. an n^{1/2−Ω(1)} *upper bound*
  **polynomially** improving Õ(√n), or a proof ruling out any n^{1/2−o(1)} lower bound. Either would
  mean the n^{1/2−o(1)} target is unreachable. **(Note: a √n/polylog or Õ(√n)-type upper bound is
  still n^{1/2−o(1)} and does NOT count as a ceiling — only a polynomial gap below √n does.)** ⚠️ **Czumaj's Ω(√n) is NOT evidence against this ceiling.** Czumaj
  is under the *weaker* emptiness oracle; the counting oracle is *strictly stronger*, so it could
  admit a *better* (n^{1/2−Ω(1)}) algorithm that lowers the true complexity polynomially below √n — exactly this RED
  ceiling. So the scan must hunt for an n^{1/2−Ω(1)} counting-oracle upper bound on its own merits and
  must **not** treat "√n holds under emptiness" as comfort that no sub-√n counting algorithm
  exists. (None known as of the idea's 2026-06-18 check — the authors leave the gap open — but
  freeze this criterion so the scan actively looks for a barrier rather than assuming none.)
- **🔴 STRENGTH-GATE / (C2)-coverage (NOT a kill — the central strength decision, surface to human):**
  if Phase-0 small-scale screening shows a single **range-counting query's coverage grows
  *polynomially*** (h(m)=m^{Ω(1)}) in the number of candidates m under the denser packing (i.e. the
  induced-matching / RS packing does **not** keep per-query candidate-distinguishing-power at m^{o(1)}),
  the achievable exponent is **capped below 1/2** (the hitting bound is Ω(m/coverage): coverage O(1) or
  even m^{o(1)} still yields n^{1/2−o(1)}; only polynomial coverage caps it) and the result becomes "**improves**" (e.g. Ω(n^{2/5})) not "**closes**." (Equivalently in
  information terms, but per the §0 framing note the *coverage* quantity — #candidates per query —
  is the operative one, not raw mutual-information bits.) Report the best exponent the evidence
  supports; the human gate decides whether to pursue the full n^{1/2−o(1)} target or settle for a
  weaker-but-still-publishable improvement. *This is the operational form of the load-bearing
  residual risk (§0).*
- **🔴 GADGET-INFEASIBILITY / (C1) (kill the load-bearing gadget = kill the headline):** if no
  ~n^{1/2+o(1)}-point gadget can induce a **(1±ε)-detectable** EMST-weight gap vs the sparse
  gadget at small scale (the gap vanishes into the (1±ε) tolerance as points are removed), the
  packing argument has no foundation. Record the smallest point-budget at which detectability
  survives; if it is asymptotically ω(n^{1/2}) the n^{1/2} target fails — re-position to the best
  exponent achievable, or escalate.
- **GREEN (strengthens the case):** the model is being actively cited but the exact (1±ε)
  randomized counting-oracle gap is still open — proceed; cite momentum and the freshness of the
  model.

### Mandatory search coverage (Phase-0 scan must cover all)

- **Queries:** "range counting oracle Euclidean minimum spanning tree lower bound"; "MST weight
  estimation query complexity sublinear"; "orthogonal range counting oracle geometric lower
  bound"; "Euclidean MST range emptiness oracle Czumaj"; "round elimination INDEX augmented
  indexing geometric query lower bound"; "Ruzsa-Szemerédi induced matching communication lower
  bound packing"; "needle in haystack cell location query complexity"; "earth mover distance
  range counting oracle" (the source paper's sibling problem — a reusable lemma there strengthens
  the paper).
- **Sources/venues to sweep:** arXiv cs.CG and cs.DS and cs.CC (last 24 months especially — the
  model is one year old and being formalized in real time); **SODA / SoCG / STOC / FOCS / ICALP /
  ESA 2024–2026** proceedings; DBLP pages of **Driemel, Monemizadeh, Woodruff, Czumaj, Har-Peled,
  Indyk**; **the most recent arXiv version of 2504.15292** (check for v2/v3 with a tightened bound)
  and **all papers citing it**.
- **Special assignment:** one subagent does nothing but try to find a paper that *already*
  improves the counting-oracle EMST lower bound past n^{1/3} (the RED scoop); a second tries to
  find an **n^{1/2−Ω(1)} upper bound or a barrier ruling out any n^{1/2−o(1)} lower bound** (the RED ceiling); a third tries
  to find any prior **space-efficient MST-distinguishing gadget** or **per-query O(1)-cell-coverage packing
  for counting (not emptiness) queries** that could be cited or that pre-empts the construction.

---

## §4. Formal Framework / System Model

Define everything the proofs need. (These are the paper's Preliminaries; freeze exact notation in
`PROJECT_STATE.md` to avoid drift.)

- **Point set & spread.** A set P of n points in [Δ]² (integer grid), with **spread / domain
  size Δ = O(n)** (the source's budget; the lower bound must respect it). The point budget is
  **|P| = n** (each gadget consumes part of it).
- **Euclidean MST weight.** w(P) = total Euclidean length of the minimum spanning tree of P. The
  estimation target is a **(1±ε) multiplicative** estimate of w(P) for a fixed constant ε ∈ (0,1).
- **Orthogonal range-counting oracle.** A query is an axis-aligned rectangle R; the oracle returns
  **|P ∩ R|** (the exact count, an integer — *not* a 0/1 emptiness bit). Cost = number of queries.
  **This exactness is the crux of (C2): an integer answer may carry ω(1) bits.** Contrast: the
  range-**emptiness** oracle returns only 1{P ∩ R ≠ ∅}.
- **The hard-instance template (to be re-derived & re-confirmed from arXiv:2504.15292 §6).** Domain
  [Δ]² split into a grid of equal cells; one uniformly-random "hidden" cell receives a **heavy
  gadget**, the rest receive **sparse gadgets**; the heavy cell shifts w(P) by a (1±ε)-detectable
  amount. Source parameters: 16·n^{1/3} cells, n^{2/3} points/gadget, heavy EMST cost Θ(n^{7/6}),
  sparse Θ(n^{5/6}), each query hits ≤4 cells. **Target parameters (to construct): Θ(n^{1/2})
  cells, ~n^{1/2+o(1)} points/gadget, with the heavy/sparse EMST-cost separation still
  (1±ε)-detectable on w(P).**
- **Hard distribution (Yao).** YES = one heavy gadget at a uniformly-random hidden cell among the
  Θ(n^{1/2}) candidates + sparse gadgets elsewhere; NO = all-sparse. The two differ in w(P) by the
  heavy excess, which must be ≥ ε·w(P) (the (C1) requirement). A query that does not *hit* the
  hidden cell returns an identical answer under YES and NO. **Round-elimination / INDEX framing, if
  used, is applied to LOCATING the hidden heavy cell, NOT to dyadic scales** (the corrected attack
  axis) — and must be checked to yield Ω(#cells), not Ω(log #cells) (see §0 framing note, §6 C3).
- **Coverage / candidate-distinguishing-power (the operative quantity).** For a query rectangle R,
  its candidate-distinguishing-power = the number of candidate cells whose presence/absence of the
  heavy gadget can change |P ∩ R| (equivalently, the number of candidates R's count is jointly
  sensitive to). The target claim (C2) is **O(1)** per query. *Mutual information between R's count
  and the hidden index is a secondary proxy; the geometric coverage quantity is load-bearing.*
- **Target cost separation (the (C1) inequality to hit, conjectural — attack-loop C1 fixes exact exponents).**
  At the n^{1/2} budget, let the heavy gadget have per-cell EMST cost Θ(n^{a}) and the sparse
  gadget Θ(n^{b}) (a > b), with Θ(n^{1/2}) cells. The global baseline w(P) ≈ Θ(n^{1/2})·Θ(n^{b}) +
  (backbone across [Δ]²). (C1) requires the single heavy cell's excess to clear the (1±ε)
  threshold: **Θ(n^{a}) − Θ(n^{b}) ≥ ε·w(P)**, i.e. the heavy excess must be a constant fraction
  of the whole MST weight. Phase 1 must derive achievable (a, b) at the ~n^{1/2}-point budget and
  check this inequality holds (the source's worked example is a=7/6, b=5/6 at the n^{2/3} budget —
  these do NOT carry over unchanged).

State the computation/communication model precisely **in the theorem statements** (randomized
algorithm with constant success probability; the reduction is information-theoretic over the
oracle-query transcript) — SODA reviewers reject hidden assumptions.

---

## §5. (reserved — merged into §6; numbering kept stable for amendments)

---

## §6. Theory / Construction Program

Each item: **claim shape → proof skeleton → verification method (declare tolerance first) →
risk / re-positioning if it collapses.** Nothing here is proven; these are the obligations. The
two load-bearing cruxes are Components (1) and (2); the reduction (3) is scaffolding that only
pays off if (1) and (2) hold.

### Component (1) — Space-efficient heavy gadget  ← **LOAD-BEARING (C1)**

- **Claim shape (Lemma A):** there is an arrangement of **~n^{1/2+o(1)} points** in a single cell
  (the "heavy" gadget) whose EMST-weight contribution differs from the **sparse** gadget's by a
  **(1±ε)-detectable** amount on the *global* w(P) — i.e. with Θ(n^{1/2}) cells, the presence of
  one heavy cell vs all-sparse shifts w(P) by ≥ ε·w(P).
- **Proof skeleton:** design heavy and sparse gadgets to satisfy the **§4 target inequality**
  Θ(n^{a}) − Θ(n^{b}) ≥ ε·w(P) (heavy excess a constant fraction of the *global* MST weight, not
  just the per-cell cost); re-derive the per-gadget EMST cost as a function of (#points, geometric
  layout) and choose the layout that maximizes the heavy/sparse separation per point. Must respect
  Δ=O(n) and the global n-point budget (Θ(n^{1/2}) cells × ~n^{1/2} points = n^{1+o(1)}). Derive
  the achievable exponents (a, b) — do NOT assume the source's a=7/6, b=5/6 (those are at the
  n^{2/3} budget and do not transfer).
- **Verification (declare tolerance FIRST):** **brute-force / exact EMST computation on small
  instances** (exact EMST via `scipy.spatial.Delaunay` + Kruskal/union-find on Delaunay edges, or
  direct for tiny n). **First reproduce the source paper's n^{2/3}-point uniform/strip gadget as the
  frozen baseline (`sim/gadgets.py`), reconfirm its heavy/sparse EMST-cost separation, THEN thin
  toward ~n^{1/2} points** — so the sweep is comparable to a verified anchor, not an invented gadget. **Swept variable (be precise):** fix the construction to m cells, p points
  per cell, global n = m·p; sweep the per-cell budget p across the regime between p≈n^{2/3} (so
  m≈n^{1/3}) and p≈n^{1/2} (so m≈n^{1/2}), and at each setting measure the **heavy-vs-sparse global
  w(P) gap as a fraction of total w(P)** (all-sparse vs one-heavy). Pre-register: "as p shrinks
  toward the n^{1/2} regime, the gap fraction stays **above a fixed ε threshold**." **Tolerance:**
  the *form* (gap is a constant fraction of w(P)) must hold; exact constants may differ.
  **Scale caveat (state it in the report):** at a few thousand total points m≈50 and the budgets
  p≈n^{2/3} vs p≈n^{1/2} differ by only a small factor — the screen can show the **direction/trend**
  of the gap fraction, NOT the asymptotic crossover; treat a worsening trend as a warning, a flat
  trend as encouraging, neither as proof. **Kill signal:** the gap fraction **shrinks below ε and
  keeps shrinking as p decreases toward the n^{1/2} regime** (gadget cannot be made both sparse and
  MST-distinguishable — the §3 (C1)-infeasibility kill).
- **Risk / re-positioning:** if detectability survives only down to ~n^{2/3+δ} points, the
  achievable cell count is Θ(n^{1/3-δ'}) and the bound improves only modestly — record the
  smallest point-budget at which (1±ε)-detectability survives and report the corresponding
  exponent honestly. **This is half the strength gate.**

### Component (2) — Per-query O(1)-cell coverage bound  ← **LOAD-BEARING (C2), THE STRENGTH-GATE KILL POINT (kills the n^{1/2} *headline*, not the project)**

- **Claim shape (Lemma B):** in the denser packing (Θ(n^{1/2}) candidate sub-instances), any
  single orthogonal range-**counting** query is **jointly sensitive to only O(1) of the Θ(n^{1/2})
  candidate cells** — i.e. its count |P ∩ R| can be changed by the heavy-vs-sparse status of at
  most O(1) candidates, the rest contributing a candidate-independent background — via an
  **induced-matching / Ruzsa–Szemerédi packing** of the candidate sub-instances. (Mutual
  information O(1) is a *corollary*; the geometric coverage statement is the one the hitting
  argument needs — see §0 framing note.)
- **Proof skeleton:** place the Θ(n^{1/2}) candidate gadgets so any axis-aligned rectangle's count
  decomposes into contributions from O(1) candidates plus a candidate-independent background; an
  RS-type induced-matching layout ensures no rectangle straddles ω(1) candidates' "live" regions.
  Then the Yao hitting argument (Component 3) turns O(1)-cell coverage into Ω(#candidates) =
  Ω(n^{1/2−o(1)}) queries (o(#candidates) queries cover/hit o(#candidates) candidates, missing the
  random needle).
- **Concrete baseline packing to screen in Phase 0 (so the screen is buildable):** place m
  candidate gadgets on a √m × √m subgrid of cells, one cell heavy; this is the **default baseline
  packing to measure**. The RS-optimal / induced-matching packing that *provably* keeps coverage
  O(1) under counting queries is an **attack-loop C2 proof obligation** — Phase 0 screens the baseline (and
  any obvious variants) to see whether O(1) coverage is even plausible, not to prove it.
- **Verification (declare tolerance FIRST):** **small-scale empirical coverage measurement** —
  build the baseline packing for modest m, enumerate axis-aligned rectangles, and for each measure
  its **candidate-distinguishing-power = #candidate cells whose heavy/sparse flip changes the
  count**; report the **max over rectangles**, swept as m grows. Pre-register: "max
  candidate-distinguishing-power per query stays **O(1)** (flat) as m grows." Secondary (proxy):
  also report **max mutual information between a query's count and the hidden index, measured as a
  ratio to the log m baseline** (raw bits grow like log m trivially; the discriminating signal is
  whether the ratio stays bounded or climbs). **Tolerance:** flat/bounded coverage is the pass;
  coverage *growing with m* is the kill. **The adversarial max (not the mean) is the kill metric.**
- **🔴 Risk / re-positioning — THIS IS THE LIVE-OR-DIE POINT (the residual risk):** a counting
  query returns an **exact integer count** (a sum over whatever cells R covers), not a 0/1 bit, so
  a large rectangle's count may be **jointly sensitive to ω(1) candidate cells** under any denser
  packing (the very feature that makes counting strictly stronger than emptiness). If the measured
  coverage **grows polynomially with m** (h(m)=m^{Ω(1)}), the hitting bound Ω(m/coverage) caps the
  achievable exponent below 1/2 → the result degrades to "improves" (e.g. Ω(n^{2/5})); coverage that is
  O(1) or m^{o(1)} still supports n^{1/2−o(1)}. **A small-scale *baseline* screen showing growth is a
  RED/YELLOW SCREEN (→ redesign the packing / escalate / human gate), NOT by itself proof the target
  is dead** — only a *proof* that every feasible packing has polynomial coverage is proof-of-death for
  the n^{1/2} headline. **Do not hide this** — it is the §3 strength-gate (kills the headline, not the
  project). Record the best exponent the packing supports
  and escalate to the human gate. Confronting this tension *is* the core research work; it is not a
  hidden breakthrough dependency, but it is genuinely open.

### Component (3) — Yao hitting argument → main theorem (scaffolding, but mind the Ω(log) trap)

- **Claim shape (Theorem, the headline):** any randomized algorithm that (1±ε)-estimates w(P)
  with constant success probability under the orthogonal range-counting oracle must make
  **Ω(n^{1/2−o(1)})** queries.
- **Primary proof skeleton (hitting / Yao — the one that actually reaches Ω(#cells)):** fix the §4
  hard distribution (YES = random hidden heavy cell among m=Θ(n^{1/2}); NO = all-sparse), which
  differ in w(P) by ≥ ε·w(P) (Lemma A), so any correct (1±ε) estimator distinguishes YES from NO.
  By Lemma B each query is sensitive to O(1) candidates, so after t queries the algorithm has
  "covered" only O(t) candidates; if t = o(m) the hidden cell is uncovered with probability 1−o(1)
  and the query transcript is (statistically) identical under YES and NO ⇒ the algorithm cannot
  distinguish ⇒ **t = Ω(m) = Ω(n^{1/2−o(1)})**. (This is the source's needle argument at the
  finer grid; verify the transcript-coupling step carefully for *counting* answers, where an
  uncovered cell must leave the count unchanged.)
- **Optional formalization (INDEX / augmented-indexing direct-sum + round-elimination on LOCATING
  the hidden cell):** the idea statement names this packaging. ⚠️ **If used, it MUST be checked to
  deliver Ω(m), not Ω(log m)** — naive mutual-information accounting (locating 1 of m candidates is
  only log m bits, O(1) bits/query ⇒ Ω(log m)) is the trap flagged in the §0 framing note. The
  direct-sum has to be over the *m candidate sub-instances jointly* (each a near-independent
  hitting sub-problem) so the bound multiplies up to Ω(m), not over a single log-m-bit index.
  **Prefer the hitting/Yao skeleton as the primary route; treat the INDEX packaging as a
  cross-check, not the main proof, unless it is verified to reach Ω(m).**
- **Verification:** this is a *proof-composition* obligation, not a simulation — write it out fully
  and cross-check against the source paper's own needle/hitting reduction. Pre-register the
  expected exponent (n^{1/2−o(1)}) and **two falsifiers**: (i) the bound only reaching Ω(log m)
  (the INDEX trap → use the hitting route); (ii) a per-candidate coupling loss that erodes Ω(m) to
  Ω(m^{1−c}) (feeds the strength gate).
- **Risk:** the reduction is the most standard part *if* (1) and (2) hold; the two live risks are
  (a) accidentally proving only Ω(log m) by mis-packaging the argument as bit-accounting, and
  (b) a hidden per-candidate coupling loss eroding the exponent. Record either honestly.

### Matching the upper bound (the SODA "tightness" deliverable)

SODA prizes upper+lower tightness. The Õ(√n) **upper bound already exists** (Driemel et al.) —
note the **tilde hides polylog factors**. So delivering Ω(n^{1/2−o(1)}) makes the upper and lower
bounds **meet up to subpolynomial (n^{o(1)}) factors** (the lower bound has an n^{o(1)} slack; the
upper bound carries polylog) — i.e. the query exponent is pinned at 1/2. **Be precise: this is
"tight up to subpolynomial factors," NOT a literally matching Θ̃(√n) characterization** (the
polylog in Õ and the n^{o(1)} slack are not closed). State it that way everywhere — "tight up to
n^{o(1)}," not "complete characterization." If (C1)/(C2) only support a weaker exponent, the honest
result is "improves the gap to Ω(n^{e}) for the best provable e" — still publishable, but the
abstract must say "improves," never "closes/tight" (the §0 strength gate; SODA reviewers police
exactly this distinction).

---

## §7. Numerics / Verification Plan (internal de-risking only — NOT a paper result)

SODA is a **pure-theory venue**: the paper's results are theorems + proofs + bounds, **not**
experiments. The code here is **internal de-risking** to decide whether the n^{1/2} target is
worth a full proof — it never appears as a headline result (at most a tiny illustrative figure if
it genuinely strengthens intuition). Two screens, mapping to the two load-bearing cruxes. **Files:**
`sim/c1_gadget_detect.py` (C1), `sim/c2_coverage.py` (C2), `sim/run_all.py` (single entry point
regenerating every figure/number), `sim/README.md` (the two scripts + how to run). Exact-EMST
dependency: `scipy.spatial.Delaunay` + Kruskal/union-find over Delaunay edges (or direct for tiny
n) — pin it in `sim/.venv`.

- **(C1) Gadget-detectability screen.** Build candidate heavy/sparse gadgets; compute **exact
  EMST weight** for all-sparse vs one-heavy configurations; measure the **gap as a fraction of
  total w(P)** as the per-cell point budget p is swept (m cells, p points each, n=m·p) across the
  regime between p≈n^{2/3} (m≈n^{1/3}) and p≈n^{1/2} (m≈n^{1/2}); check against the §4 target
  inequality. Pre-registered expectation: gap fraction stays ≥ a fixed ε. **Kill signal:** fraction
  shrinks below ε and keeps shrinking as p→n^{1/2}. **Scale caveat:** small scale shows only the
  *trend*, not the asymptotic crossover (state this in the report).
- **(C2) Per-query coverage screen (THE decisive measurement).** Build the **baseline packing**
  (m gadgets on a √m × √m subgrid of cells, one heavy — §6 Component 2); enumerate axis-aligned
  rectangles; for each measure its **candidate-distinguishing-power = #candidate cells whose
  heavy/sparse flip changes the COUNT**; report the **max over rectangles**, swept as m grows.
  Pre-registered expectation: **flat / O(1)** (or at worst m^{o(1)}). **Kill/strength signal:** the max
  coverage **grows polynomially with m** (m^{Ω(1)}) → exponent capped below 1/2 (m^{o(1)} growth still
  supports n^{1/2−o(1)}); a baseline screen showing growth ⇒ redesign/escalate/human gate, NOT an
  auto-kill of the target (the residual-risk realization). *Measure the COUNT, not emptiness —
  the whole point is exact counts may make a rectangle sensitive to more cells.* **Secondary
  proxy:** also report the count↔hidden-index mutual information **as a ratio to the log m
  baseline** (raw bits grow like log m trivially; only a *climbing ratio* is a signal). **For
  contrast** measure emptiness-query coverage on the same packing — *hypothesis* (not a guaranteed
  expectation) that it is ≤ the counting coverage; if they are equal, that is itself informative.
- **Protocol:** fixed seeds; random placements are a **smoke/sanity check ONLY (never de-risk
  evidence)**, adversarial placements are **the only de-risk evidence** (adversarial = placements
  designed to make a single rectangle straddle many candidates, stress-testing (C2)); report
  mean ± CI **and the tail (max) — the adversarial max is the kill metric, the mean is secondary**;
  every figure regenerated by `sim/run_all.py`; freeze all numbers in `PROJECT_STATE.md`
  (append-only frozen-results table).
- **Honest reporting:** a screen that *contradicts* the pre-registered expectation is a **finding,
  not a failure** — record it and escalate to the human gate (it likely means the n^{1/2} target
  must drop to the best supportable exponent, or the gadget must be redesigned). **Never
  shape-force** the gadget or the packing to make a plot look clean.
- **Scope of evidence:** a clean small-scale screen is a **necessary kill-screen, NOT sufficient
  proof** — asymptotic detectability and asymptotic O(1)-coverage are *proof obligations* (§6), not
  established by simulation. Simulation only decides whether to *attempt* the proof.

---

## §8. Paper Plan (SODA structure-clone)

**Use the SODA writing pipeline `venue-prompts/soda/` in Phase 5** (1-results-selfcheck →
2-writing-guide → 3-page-trim → 4-pre-submission-check). Below is the skeleton; the precise
structure-clone target is finalized in Phase 5.

- **Structure-clone target (SODA exemplar).** This is a **pure lower-bound / query-complexity**
  paper, so the most faithful *content* template is the **source paper itself, Driemel et al.
  SoCG 2025 (arXiv:2504.15292)** — same model, same problem, the very construction this paper
  strengthens: study how it organizes the hard-instance construction, the gadget definitions, the
  information-theoretic reduction, and what it sinks to the appendix. For the *overall SODA
  skeleton*, the project default exemplar is **Naor–Srinivasan–Wajc, SODA 2025 (arXiv:2301.08680)**
  (§1.1 Results / §1.2 Techniques / §1.3 Related Work folded into intro / §2 Preliminaries /
  §3–4 inline key proofs / §6 Lower Bounds / §7 Open Questions / Appendix full proofs).
  **Phase 5 MUST read every section of the chosen exemplar(s) and build a component-mapping table
  BEFORE drafting** (per `venue-prompts/soda/2-writing-guide.md` — this is a *structure-clone*
  task, not free writing; the classic failure is "reads like SODA but the section/component
  distribution doesn't match → 10+ rejections, full rebuild").
- **Skeleton (SODA norm — §-numbers below are the PAPER's TOC, not this guide's):** Abstract →
  §1 Intro (§1.1 Results = the formal Ω(n^{1/2−o(1)}) theorem + the prior-bound comparison table;
  §1.2 Techniques — *lead with the space-efficient gadget + per-query O(1)-cell coverage bound*, the
  reduction as scaffolding; §1.3 Related Work folded into intro, **not** a late standalone
  section, with the Czumaj range-emptiness boundary explicitly drawn) → §2 Preliminaries (model,
  range-counting oracle, EMST, spread/budget, randomization) → §3 The space-efficient gadget
  (Lemma A) → §4 **The per-query information bound (Lemma B) — the centerpiece** → §5 The reduction
  + main theorem → §6 Open questions → Appendix: full proofs + full case analysis.
- **Page budget:** SODA has **no hard page limit** but the **first ~10 pages after the title page
  must convey the full merits**; full proofs sink to the appendix (unlimited). Writing-stage
  delivery ≈ first 10 pages tight + complete appendix — **do not pad; do not overflow the first
  10.** SODA's trim lever is *sink proofs to appendix*, NOT shrink-font/squeeze-margins (those =
  summary rejection). ~3 references/page (≈30 in the first 10).
- **Bound consistency:** every bound (abstract = intro = theorem = comparison table = conclusion)
  must be **character-for-character identical** — Ω(n^{1/2−o(1)}) everywhere it appears; pull
  exponents from the frozen proofs, never from memory. **If the proof reaches only a weaker
  exponent, change it EVERYWHERE and switch the verb from "close/tight" to "improve."**
- **Forbidden claims / "what we do NOT claim" (align to SODA + project red lines):** do **not**
  claim "tight" or "closes the gap" unless the proof actually reaches n^{1/2−o(1)} matching Õ(√n)
  up to n^{o(1)} (otherwise say "improves to Ω(n^{e})"); state the (1±ε) error regime and the
  randomized model **in the theorem**; cite Czumaj's Ω(√n) **only** as motivation (weaker
  emptiness oracle, deterministic, O(n^{1/4}) error — never as proving the counting claim).
  **Per `venue-prompts/soda/2-writing-guide.md`: NO defensive "Limitations / Future Work"
  section** — scope (the (1±ε) regime, the Δ=O(n) budget, the o(n^{1/2}) slack) is written as
  **confident model definitions inside the theorem statement**, not a confessional. (The
  project-wide "明确不声明什么" discipline is satisfied here by precise theorem-statement scoping
  — SODA style overrides the generic contribution.md convention.)
- **Title candidates:** "A Tight Query Lower Bound for Estimating the Euclidean MST Weight under
  Range-Counting Oracles"; "Closing the Gap for MST-Weight Estimation in the Range-Counting-Oracle
  Model"; "Ω(n^{1/2−o(1)}) Range-Counting Queries Are Necessary to Estimate the Euclidean MST."
  (Use "tight/closing" titles ONLY if n^{1/2−o(1)} is actually proven.)

---

## §9. External-solver attack & audit loop (STANDARD WORKFLOW — read before §10)

> Embedded from `deepdive/_templates/external_solver_attack_playbook.md` with this project's slots
> filled. This **replaces** any "Claude proves the theorems itself on a fixed 5-phase pipeline"
> reading: that framing wasted the most time on a past project and is retired
> (`guide_feedback/00_project_retrospective.md`). Keep every discipline line below.

### §9.0 Division of labor (establish on day 0, before any proof effort)

| Role | Who | Does | Does NOT |
|---|---|---|---|
| **Attacker** | codex **GPT-5.5-xhigh** (default); web **GPT-5.5-Pro** (escalation, human-relayed) | Originate the mathematics: the space-efficient gadget (C1), the O(1)-coverage packing (C2), the hitting reduction (C3), counterexamples, refutations | — |
| **Orchestrator / referee / archivist** | **Claude Code** (the executing session) | Write method-free briefs; run independent adversarial audits; classify FATAL/GAP/MINOR; maintain the frozen research-line ledger; detect drift/circularity (esp. the Ω(log m) trap); decide escalate vs continue vs stop | Originate the frontier proofs; "solve it itself"; smuggle unproven implications into briefs |
| **Auditor** | independent **fresh-context** agents (Codex or Claude) | Adversarially try to break each attacker reply (find the counterexample / missing term / unstated assumption) | Share context with the attacker or the orchestrator |
| **Decider** | the **human (owner)** | Final verification; approve pivots; the strength-gate (closes-vs-improves) and any venue/scope change | — |

**The orchestrator is a referee, not a relay and not a prover.** Claude's value-add is structuring
briefs, auditing, classifying, ledger-keeping, and catching drift/circularity — above all the **§0
Ω(log m) trap** (a bit-accounting mis-packaging of the hitting argument). It must understand the
problem well enough to referee but must **not** originate the hard math and must **not smuggle
unproven logical implications into briefs** (e.g. "the gadget is sparse" ⇏ "coverage is O(1)";
"emptiness Ω(√n) holds" ⇏ "counting Ω(√n) holds"). State what is **known**; pose the open question
cleanly; let the attacker reason.

### §9.0b 🔴 No-retreat red line (target fixed ⇒ no difficulty-driven downgrade)

Target venue = **SODA** and contribution altitude = **a query lower bound that closes (or, only on
proof-of-death, honestly improves) the Ω(n^{1/3}) vs Õ(√n) gap**. Once fixed, **difficulty / being
stuck / time pressure are NEVER grounds to weaken the contribution or retarget to an easier venue.**
Hard ⇒ escalate the attack (codex-xhigh → web-Pro → fresh-context attacker) at full force. The ONLY
thing that may change the target/contribution is the science being **provably dead** — a refutation,
a proven impossibility (a sub-√n counting-oracle *upper* bound / a proven ceiling), or a confirmed
scoop — surfaced at the **human gate** for the owner to decide.
**Crucial nuance specific to this project — "closes" vs "improves" is NOT a retreat, it is the
science:** the achievable exponent is an *empirical fact about the construction* decided by (C1)+(C2).
Reaching only Ω(n^{2/5}) because the C2 coverage provably grows is a **proof-of-death for the n^{1/2}
target** (an evidence-backed truth outcome), not a difficulty-driven downgrade — report it honestly
at the human gate. What the red line forbids is *giving up on n^{1/2} because it is hard while the
construction has not been shown to cap below 1/2*.

### §9.1 The escalation ladder

```
hard sub-problem ∈ { C1 space-efficient gadget · C2 O(1)-coverage packing · C3 hitting reduction reaching Ω(m) }
   │
   ├─(1) codex GPT-5.5-xhigh ── multi-round attack ──┐
   │     stall = K = 2 consecutive rounds with:      │ stall?
   │       no new VERIFIED lemma, OR circular         │
   │       reasoning, OR a re-tread of an already-    │
   │       refuted route, OR a sustained confidence   │
   │       drop.                                      ▼
   ├─(2) user-mediated web GPT-5.5-Pro ── method-free briefs, human relays each round ──┐
   │     (also, when stuck on the SAME thread: spawn a FRESH-context attacker with a      │
   │      method-free brief — fresh agents leap past dead ends the thread is anchored on) │
   │                                                                                      ▼
   └─(3) converge OR conclude-open ── see §9.4 stop criteria ──► human gate
```

- **Default to (1).** Route the math out immediately; the orchestrator does not burn rounds trying
  to solve C1/C2/C3 itself.
- **Escalate to (2) on the defined stall (K=2), not a vibe.**
- The **fresh-agent move is a first-class lever** — when a thread is anchored on a dead end (e.g.
  keeps trying an RS layout that an audit showed leaks), spawn a fresh-context attacker with a
  method-free brief *before/alongside* escalating.
- **Economics:** web GPT-Pro rounds are slow + human-in-the-loop — batch maximally, keep each brief
  self-contained, never spend a Pro round on what xhigh or an audit agent can do.

### §9.2 The brief — freeze FACTS, free METHODS

Every brief to an attacker has this skeleton:
1. **The exact target** — a precise claim (e.g. "construct a ≤ n^{1/2+o(1)}-point single-cell gadget
   whose presence shifts global w(P) by ≥ ε·w(P) at the Θ(n^{1/2})-cell budget"; or "prove every
   axis-aligned rectangle's count is sensitive to O(1) candidates under packing X").
2. **Frozen substrate** — proven results so far, labeled `P1…Pn`, "use freely, do not re-derive."
3. **Refuted routes** — `N1…Nn`, "do NOT attempt," each with the one-line killing reason.
4. **Barriers in force** — `B1…Bn` (e.g. the n-point/Δ=O(n) budget; the Ω(log m) trap as a *proof*
   barrier the reduction must evade; counting ⊋ emptiness so per-query coverage can exceed 1).
5. **The open question**, posed method-agnostically: "close this; use any method; if these methods
   can't, say so plainly."
6. **What we need back** — the full argument OR a precise statement of where it breaks; an updated
   confidence %; a clear verdict.

**"Free methods" ≠ "no context."** Freeze the FACTS (target + substrate + refuted + barriers); free
the METHODS (zero route prescription). Do not mandate one lemma as the only path (over-constraining
to a single mandated lemma was an observed failure mode).
🔴 **Project-specific brief rail:** never write into a brief any of — "the gadget being sparse
implies O(1) coverage," "O(1) bits/query ⇒ the lower bound" (that is the Ω(log m) trap), or
"Czumaj's emptiness Ω(√n) implies a counting bound." These are exactly the unproven implications the
orchestrator must NOT smuggle.

### §9.3 The audit & rebattle loop (after every attacker reply)

- **Normal reply → 1 independent fresh-context audit agent**, adversarial mandate: "find the
  counterexample / the missing term / the unstated assumption / the Ω(log m) mis-packaging."
- **Major-progress / claimed-closure reply → 3 independent fresh adversarial audits, blind to each
  other.** Pool findings.
- **Classify every finding:** **FATAL** (counterexample / unfixable gap → claim dead or must be
  reformulated); **GAP** (load-bearing step asserted but unproved, often patchable → into the
  rebuttal brief); **MINOR** (wording / "state explicitly" → human writeup, non-blocking).
- **Rebattle:** fold GAP/FATAL into a focused rebuttal brief; loop (repair → re-audit → repair).
- **Confidence trend (a % per round, with dates).** A sustained *drop* ⇒ escalate / fresh-agent
  reset (**attack harder**) — never an incremental round, never a downgrade (per §9.0b a drop is
  difficulty, not a kill trigger).

### §9.4 Stop criteria — when the AI loop is done

Declare **AI convergence** only when ALL hold: (1) the attacker explicitly claims closure with no
further conditions; (2) ≥ 3 independent adversarial audits find no FATAL and no counterexample; (3)
every residual is verification debt (a correct-looking step to write out / a wording fix), NOT a new
obstruction or an unresolved GAP. Then STOP the AI loop and hand to the human gate.

🔴 **"AI-verified" ≠ "proved."** Remaining work is mandatory and human: (a) human-expert
verification of the full argument (especially the C3 transcript-coupling step for *counting*
answers); (b) a full formal writeup; (c) independent human checking of any AI-produced substrate the
closure is conditional on (the C1 gadget exponents, the C2 RS layout); (d) a final novelty/priority
sweep of recent preprints. This is up front, here — not only in an ethics preamble.

### §9.5 Archiving — the orchestrator's bookkeeping duty

- **One append-only research-line ledger per research line** (`research_line_<name>.md`) — the single
  most valuable artifact, a **day-0 deliverable**. Sections: frozen model/notation; **proven results**
  `P1…Pn` ("use freely, do not re-derive"); **refuted routes** `N1…Nn` ("do NOT attempt" + killing
  reason); **barriers** `B1…Bn`; the **exact open problem** as currently reduced; a **confidence
  trend** with dates; a **HEADLINE** line at top with current status.
  🔴 **Re-read this ledger + the frozen artifacts before continuing — never work from memory**
  (memory ⇒ exponent drift n^{1/2} vs n^{1/2−o(1)}, Δ/ε/a/b notation collisions, repeated labor).
- **Per-round artifacts:** every brief, attacker reply, audit verdict, rebuttal — one file each,
  named by round (`round{n}_{brief|response|audit}.md`). Indispensable for the human pass and for
  surviving context resets.

### §9.6 Kill → pivot branch (kill criteria are *meant* to fire — on proof-of-death only)

🔴 Kill fires on **proof-of-death only** — a refutation, a proven impossibility, or a confirmed
scoop — **never on difficulty** (that triggers §9.1 escalation). For THIS project the relevant
proof-of-death events are: the §3 **RED scoop** (someone already improved the counting-oracle EMST
bound), the §3 **RED ceiling** (a proven n^{1/2−Ω(1)} counting-oracle upper bound ⇒ the n^{1/2−o(1)} target unreachable),
or an attack-loop FATAL that kills C1 or C2 outright. On such a kill:
1. Record it in the ledger + `docs/guide_amendments.md` (what died, the proof, who verified).
2. **Assess pivot reachability:** does the substrate already built (the gadget machinery, the
   coverage analysis, the range-counting-oracle model fluency) point at an **adjacent open problem**
   now in reach — e.g. the **Earth-Mover-Distance** range-counting-oracle bound the source paper also
   studies (a reusable lemma/gadget there), or the counting-oracle bound for a different geometric
   estimator? (Note: dropping n^{1/2}→n^{2/5} for the SAME problem is NOT a pivot — it is the
   strength-gate outcome, handled in §10/§11, no new ledger.)
3. **This is a human-gate decision:** present kill + candidate pivot(s) + rough budget; the owner
   chooses pivot-vs-stop. Do not silently start a new line; do not grind the dead one.
4. If pivoting, open a **new** research-line ledger; flag that the repo/idea name is now stale.

### §9.7 De-risking simulations (Phase-0 only; internal, never a paper result)

Pure-theory venue ⇒ no experiments. The C1/C2 screens (§7) are internal de-risking under one rule:
**adversarial input is the kill metric, random input is not evidence** (a past project looked GREEN
on random input and was killed by the adversarial worst case). **Pre-register expected trend + a
falsifier before running.** A clean random-input plot proves nothing; the adversarial max coverage
(C2) and the worsening-trend gap fraction (C1) are the signals.

---

## §10. Workflow = attack loop (NOT a linear pipeline) / Agent operating rules

**Before each milestone/round: enter plan mode** — analyze the tasks, decompose into an ordered
sub-task checklist, then execute the whole list straight through (do not start proving/coding before
planning; but once planned, do not stop after each sub-task to ask "continue?").

**The shape is a loop, not a conveyor belt:**
```
screen (Phase 0: kill-scan + adversarial C1/C2 de-risk)
   → human gate #1 (strength decision / kill / pivot)
   → attack-loop  (brief → codex-xhigh attack → independent audit → rebattle ;
                   escalate per §9.1 ladder ; one loop per crux C1, C2, C3)
   → converge-or-pivot (§9.4 stop criteria / §9.6 kill→pivot)
   → human gate #2 (AI-convergence handoff: "AI-verified ≠ proved")
   → writing (venue-prompts/soda/ stages 1→2→3→4)
   → human gate #3 (venue/scope, pre-submission)
```
This is **not** the assumption "the idea is alive and Claude will find the proof." Each crux may
kill the n^{1/2} target; each has its own brief/attack/audit loop; the de-risk screens (Phase 0)
decide whether to even start the attack on the full target.

- **Milestones & gates.** Phase 0 (screen) ends at **human gate #1** — mandatory stop. The attack
  loop runs C1, then C2 (the kill point), then C3; convergence (or kill→pivot) ends at **human gate
  #2**. Writing ends at **human gate #3**.
- **🎯 Per-gate paper-orientation check (mandatory).** At every gate spawn **one independent
  subagent** with the current frozen contribution + the SODA requirements (`venue-prompts/soda/` or
  the live CFP). It judges: ① is the current contribution already/on-track **enough to submit to
  SODA** (is the exponent strong enough — closes vs improves — and is it on-topic), and what is still
  missing; ② has the work **drifted** into publication-irrelevant tangents / over-generalization
  (the main agent forgets the paper goal easily); ③ any other problem (boundary collapsed, claims
  exceeding what is proved). Correct course on its advice; log in `PROJECT_STATE.md` +
  `DESIGN_DECISIONS.md`.
- **Acceptance / verification style.** Embed *expected trends* not exact numbers ("gap fraction
  stays ≥ ε"; "max coverage flat"); re-run randomized screens; do **positive AND negative**
  verification (confirm detectability at target budget AND that it *breaks* when the gadget is made
  too sparse; confirm counting-query coverage is measurably ≥ emptiness-query coverage on the same
  packing). **Pre-register** before every screen/proof; mismatch → diagnose (bug vs finding), record
  honestly, **never shape-force**. Frozen-results table is **append-only**; pull every
  exponent/constant from frozen proofs, never memory.
- **Progress-recording discipline (MANDATORY).** Maintain `PROJECT_STATE.md` (progress / frozen
  results & numbers + artifact paths / current phase / TODO + pending human decisions) **and the
  per-line research-line ledger (§9.5)**; update every round; record decisions in
  `DESIGN_DECISIONS.md`; amend the guide only via `docs/guide_amendments.md`. **When context grows
  long, re-read the ledger + `PROJECT_STATE.md` + frozen artifacts before continuing — never from
  memory.**
- **Mapping cruxes → attack-loop targets (replaces the old linear "Phase 1/2/3"):** C1 (§6
  Component 1 / Lemma A) and C2 (§6 Component 2 / Lemma B) and C3 (§6 Component 3 / main theorem)
  are each a **brief→attack→audit→rebattle loop** per §9, not solo-proved phases. C2 is the kill
  point; if its coverage provably grows, that is the strength-gate (closes→improves), surfaced to the
  human, not a difficulty downgrade. Writing uses `venue-prompts/soda/` only after AI-convergence +
  human gate #2.

---

## §11. Risk Register / Decision Log / HUMAN INPUT

### Risk register (live; mirror into `PROJECT_STATE.md` and the ledger)

1. **(C2) A counting query is sensitive to ω(1) candidates under the denser packing** → exponent
   capped below 1/2, result degrades "closes"→"improves." *The single live-or-die / strength risk*
   (the elevated `extras.residual_risk`). De-risk in Phase 0 (C2 screen) and attack-loop C2 before
   sinking effort into C3.
2. **(C1) No sparse-yet-MST-detectable gadget at ~n^{1/2} points** → the Θ(n^{1/2})-cell packing has
   no foundation; best exponent drops. De-risk in Phase 0 (C1 screen) + attack-loop C1; record the
   smallest point-budget at which (1±ε)-detectability survives.
3. **The Ω(log m) trap in C3** → the reduction accidentally proves only Ω(log m) (bit-accounting
   mis-packaging) instead of Ω(m). Audits must check the hitting/Yao route reaches Ω(#cells); prefer
   it over the INDEX packaging unless INDEX is verified to reach Ω(m).
4. **Hidden per-candidate coupling loss in the direct-sum** → exponent erodes n^{1/2−o(1)}→n^{1/2−c}.
   Record the real exponent; feeds the strength gate.
5. **"Narrow contribution" perception** (a quantitative exponent tightening in a 1-year-old model) →
   *mitigation:* lead with the gadget (C1) + coverage bound (C2) as genuinely new technique; motivate
   why the range-counting-oracle model matters; frame as **closing the first open problem stated in
   the model** (pinning the exponent at 1/2, tight up to n^{o(1)} against the existing Õ(√n)).
6. **Real-time formalization scoop** → Phase-0 RED-scoop + RED-ceiling special assignments; move
   promptly given the 2026-07-09 deadline.
7. **Czumaj boundary mis-stated** → a reviewer reads "Ω(√n) already known." *Mitigation:* the §2
   mandated defense (emptiness ⊊ counting; deterministic vs randomized; O(n^{1/4}) vs (1±ε)) must be
   explicit and prominent.

### Decision log (seed)

- **Target venue = SODA** (owner-explicit + idea's first canonical venue); **SoCG sibling**,
  near-identical conventions. SODA fit verdict PASS — not a redirect situation.
- **Attack axis = needle-in-haystack (locate the hidden heavy cell under the space budget), NOT
  scale-by-scale / dyadic round-elimination** (the rejected, misaligned framing). Round-elimination,
  if used, applies to LOCATING the hidden cell and must reach Ω(m), not Ω(log m).
- **Strength gate ("closes" vs "improves") is decided by (C1)+(C2), not by venue fit.** Both
  publishable; only the headline verb changes. Never claim "tight/closes" unless n^{1/2−o(1)} is
  actually proven.
- **Roles fixed day-0:** math attacker = codex-xhigh→web-Pro; Claude = orchestrator/referee/
  archivist (not a solo prover); auditors = fresh-context agents; decider = human.
- **Czumaj's Ω(√n) is motivation only** (weaker emptiness oracle); never cited as proving the
  counting claim.

### 🔴 HUMAN INPUT — three gates (NOT a single end-of-Phase-0 stop)

- **Gate #1 — kill / pivot / strength (end of Phase 0 screen).**
  - [ ] Given the (C1)/(C2) screens, pursue the **full n^{1/2−o(1)} ("closes")** target or settle for
    the **best supportable exponent ("improves")**? *(The decisive gate — do not start the attack
    loop on the full target before this.)*
  - [ ] Approve the kill verdict (GREEN/YELLOW/RED incl. the RED-scoop and RED-ceiling searches) +
    the independent second-opinion subagent's read; if a RED kill fired, decide **pivot-vs-stop**
    (§9.6 — e.g. pivot to the EMD range-counting-oracle bound).
- **Gate #2 — AI-convergence handoff (end of the attack loop).**
  - [ ] The attack loop reports convergence (attacker closure + ≥3 clean adversarial audits + only
    verification debt remaining). **Acknowledge "AI-verified ≠ proved":** the result is conditional
    pending human-expert verification of the full argument (esp. the C3 counting-transcript coupling)
    + independent human check of any AI-produced substrate (C1 exponents, C2 RS layout) + a final
    preprint priority sweep.
- **Gate #3 — venue / scope / pre-submission.**
  - [ ] Confirm SODA 2027 CFP details (single-column/11pt/1-inch, no hard page limit, appendix
    unlimited, blind policy, deadline **2026-07-09**) re-verified against the official CFP.
  - [ ] Confirm the final headline verb (closes vs improves) matches the frozen exponent everywhere;
    confirm the no-experiments framing (the C1/C2 screens are internal de-risking, not paper results).
  - [ ] Sanity-check the **exact Czumaj et al. citation** (EMST under range-emptiness, Ω(√n),
    deterministic, O(n^{1/4})) — finding it is a Phase-0 scan deliverable, not a human task; surface
    here only to confirm the oracle/regime/error. If the scan could not confirm it, say so (never
    fabricate a cite).
