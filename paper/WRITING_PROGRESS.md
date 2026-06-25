# WRITING_PROGRESS — SODA paper (EMST range-counting Õ_ε(n^{1/3}))

> Update after EVERY section. On long context, re-read THIS + `COMPONENT_MAPPING.md` + the frozen proof
> (`docs/webpro_round5_response.md`) before continuing — never write from memory. Venue = SODA = THEORY.

## Status: FULL DRAFT COMPLETE + REVIEWED — compiles clean, 29pp, 43 verified refs, 0 undefined.
All sections + §2 Technical Overview + 2 figures + 2 algorithm boxes. App.A (residual-debt WSPD impl)
reached Codex SOUND-WITH-FIXES over 5 adversarial rounds. Whole-paper Codex review = MINOR-REVISION, all
round-1 concerns FIXED, readability R-W1 clean / R-W2,R-W3 OK-with-notes (no BLOCKER), length lens
"28pp appropriate, not padded". All minor fixes applied. Convergence gate (owner's revised target):
(a) proofs complete — YES (body claims App.B/C-backed; App.A SOUND); (b) length 29pp — in owner's ideal
25-35 band (Codex endorsed); (c) refs 43 — Codex "adequate, no missing strand" (below original 50-70
heuristic by design, no padding); (d) readability — no BLOCKER. → ready for HUMAN-EXPERT verification
(gate #2), esp. App.A §A.3-A.4 (WSPD incident-edge oracle + bottleneck search) and the App.B two-part
accounting. Review verdicts archived docs/reviews/.

### REVIEW round 1 (Codex gpt-5.5 xhigh, 2026-06-25): App.A=FLAWED (8 BLOCKER), whole=MAJOR-REVISION.
Verdicts archived docs/reviews/; triage paper/REVIEW_round1_concerns.md. Round-1 fixes APPLIED:
- App.A fully REWRITTEN: exact Euclidean rep-edge weights (kills spanner-subgraph BLOCKER + dup-edge issue);
  exact bottleneck PQ (no rounding bias); root rank −∞ matching §4; GLOBAL per-call budget + FAIL (no
  upward-biased imputation — the cap BLOCKER); vertex-incident-edge oracle (Lem incident) over ancestor
  cells on top of Lemma 24; rep_Q + Õ(n/K) seed cost for support; harmonic 1/(j-1); side-length notation;
  n^{1/3}·poly(1/ε)·polylog made explicit.
- §4: regularization now cites Lem kwindow; prelims: set of n≥2 DISTINCT points (was "multiset"), W≥n-1.
- App.C: NEW Lemma kwindow — full halving-search proof (quadrupling overshoot ≤4×, fixed-budget one-sided
  rejection test Õ(n/K_0)/scale × O(log Δ) scales = Õ(n^{1/3})).
- intro/abstract: "settles polynomial query exponent" (qualified); Czumaj row CORRECTED to (1±ε) Õ_ε(√n)
  (web-verified SICOMP'05 — prior "O(n^{1/4}) rel"/"additive error" was wrong); +ChenKhannaTan23
  (2203.14798), +ChenKhanna23Steiner (2211.03893). Refs now 43.
NEXT: re-audit App.A via Codex (was FLAWED → must clear BLOCKERs).

### App.A (WSPD death-time impl) — confidence flags (honesty rail):
- ~90% (matches Pro's 0.89): the bottleneck-search expected-extraction = O(log|V|) coupling to the rank
  order ON THE SPANNER (re-used the leader-estimator harmonic argument; a referee should check the
  ordering is by bottleneck distance from v, not graph-BFS order).
- ~90%: the extraction-cap → additive-error absorption (capped searches report X_L=L; argued one-sided +
  Markov, δ' = const·target accuracy). Folded into §5 budget by assertion, NOT re-derived in App.C.
- ~95%: per-search cost O(ρ^{-3} log Δ)·O(log|V|): conservative (expand every reached vertex at every
  scale via Lemma navigate). Could be tightened but the bound suffices for Õ_ε(n^{1/3}).
- Lemma 24 (neighbor oracle) restated from source verbatim-faithfully; correctness of the 2^{i*}
  truncation cited to [DMOSW25 Lemma 24] not re-proved.
HUMAN-VERIFY TARGET: App.A §A.4 (bottleneck search + cap) is the place a referee will attack hardest.

### Owner decisions (2026-06-22)
- Proceed with full writeup NOW (writeup = the human-verification vehicle); paper stays AI-level until human sign-off.
- §6 Optimality = standalone short section.
- Defaults adopted: double-blind from day 1; EMD extension = headline open question; AI-provenance → DESIGN_DECISIONS, not the paper; title seeded "Estimating Euclidean MST Weight in Õ(n^{1/3}) Range-Counting Queries".

### Build
`cd paper && latexmk -pdf main.tex` → main.pdf (4pp so far). Intermediates gitignored. Toolchain: TeX Live 2025.
Macro note: range-count macro is `\rcount` (`\count` is a TeX primitive — do not use).

## Phase checklist (skill 10 pipeline)
- [x] W-1 venue-class gate: SODA = THEORY; ~50–60pp / full proofs / ~40–80+ refs; numbers verified
      (official SODA norms + NSW exemplar skeleton + 86 refs).
- [x] Read skills 07 / 08 / 10 (cloned `.skill_js`).
- [x] Read structure-clone exemplar (NSW SODA'25) section skeleton.
- [x] Build COMPONENT_MAPPING.md.
- [ ] **OWNER ALIGNMENT on the mapping table (the gate before prose).** ← HERE
- [x] W0 refs.bib: 41 cited entries, all 8 strands covered, all verified (source-bib transcription + dedup-sweep arXiv IDs). Below 50-70 heuristic by design (tight scope; no padding) — Codex REFERENCE-COVERAGE to adjudicate.
- [ ] Scaffold `paper/main.tex` + `sections/*.tex` + latexmk + gitignore intermediates.
- [ ] W1 draft order: prelims → theory(full proofs) → assembly → related → intro(contribs last) → concl → abstract.
- [ ] W3 per-batch style gates (token sweep / acronym order / number echo).
- [ ] W4 reviewer panel (6 lenses: proof-correctness, tightness, TPC/overclaim, style/fresh-reader,
      PROOF-COMPLETENESS, REFERENCE-COVERAGE) — ALL via Codex (red line). 
- [ ] W4 readability panel R-W1/R-W2/R-W3 via Codex gpt-5.5 xhigh.
- [ ] W5 freeze concerns → REVIEW_round1_concerns.md → triage.
- [ ] Convergence gates (a) proofs complete (b) length ~50–60pp (c) refs ~50–70 (d) readability no BLOCKER.

## Section status
| § | title | drafted | proofs-in-appendix | style-gate | notes |
|---|---|---|---|---|---|
| 1 | Introduction | ☑ draft | — | ☐ | results+prior table+techniques+related(8 strands folded); theorem*/lemma* restatements |
| 2 | Preliminaries | ☑ draft | — | ☐ | model + cluster-count integral + WSPD + notation table |
| 3 | Support-MST estimator (Lemma 3) | ☑ draft | App. B ☑ FULL | ☐ | the new primitive; packing+interleaving+leader+2-part accounting+accuracy+guess all proved |
| 4 | Death-time + reduction for P | ☑ draft | App. C ☑ FULL | ☐ | sampler+spanner+regularize+snapping+decomp |
| 5 | Main theorem (assembly) | ☑ draft | App. C ☑ FULL | ☐ | 3 pieces + error budget + W-search |
| 6 | Optimality (tightness) | ☑ draft | — | ☐ | standalone; Cor tight (n^{1/3} up to polylog) |
| 7 | Open questions | ☑ draft | — | ☐ | EMD headline + d>=3 + polylog/determinism |
| A | WSPD death-time impl (FULL) | ☑ draft | — | ☐ | 🔴 residual-debt discharge; telescoping+spanner+navigate+bottleneck-search+global cap; conf flags above |
| B | proof of Lemma 3 | ☑ draft | — | ☐ | committed f4837ae |
| C | proofs of §4–§5 | ☑ draft | — | ☐ | committed f4837ae |

## Frozen-source pointer
All theorem/bound text copied from `docs/webpro_round5_response.md` (Pro round-5 consolidated proof) +
its numeric confirmations (`attack_loop/webpro_verify_round5_cores.py`). Dedup/refs: `lit/GATE2_DEDUP_SWEEP.md`.

## Decisions log (mirror to DESIGN_DECISIONS.md)
- (pending owner) §6 standalone vs folded; anonymization; title; AI-provenance disclosure.
