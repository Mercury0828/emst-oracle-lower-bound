# WRITING_PROGRESS — SODA paper (EMST range-counting Õ_ε(n^{1/3}))

> Update after EVERY section. On long context, re-read THIS + `COMPONENT_MAPPING.md` + the frozen proof
> (`docs/webpro_round5_response.md`) before continuing — never write from memory. Venue = SODA = THEORY.

## Status: SCAFFOLD UP + PRELIMS DRAFTED — compiles clean (4pp). Owner signed off on structure
(full writeup now; §6 standalone). Next = the proof-heavy sections (§3 + App.B, then §4/§5 + App.C, then App.A WSPD).

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
- [ ] W0 preconditions: refs.bib resolver-verified (the 8 strands); copy AI_STYLE_CHECKLIST into `.agent/`.
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
| 1 | Introduction | ☐ | — | ☐ | contribs last; related work folded in |
| 2 | Preliminaries | ☑ draft | — | ☐ | model + cluster-count integral + WSPD + notation table |
| 3 | Support-MST estimator (Lemma 3) | ☐ | App. B ☐ | ☐ | the new primitive |
| 4 | Death-time + reduction for P | ☐ | App. C ☐ | ☐ | |
| 5 | Main theorem (assembly) | ☐ | App. C ☐ | ☐ | |
| 6 | Optimality (tightness) | ☐ | — | ☐ | owner: standalone vs folded |
| 7 | Open questions | ☐ | — | ☐ | EMD extension as headline |
| A | WSPD death-time impl (FULL) | ☐ | — | ☐ | 🔴 residual-debt discharge |
| B | proof of Lemma 3 | ☐ | — | ☐ | |
| C | proofs of §4–§5 | ☐ | — | ☐ | |

## Frozen-source pointer
All theorem/bound text copied from `docs/webpro_round5_response.md` (Pro round-5 consolidated proof) +
its numeric confirmations (`attack_loop/webpro_verify_round5_cores.py`). Dedup/refs: `lit/GATE2_DEDUP_SWEEP.md`.

## Decisions log (mirror to DESIGN_DECISIONS.md)
- (pending owner) §6 standalone vs folded; anonymization; title; AI-provenance disclosure.
