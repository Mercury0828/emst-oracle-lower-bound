You are a referee panel for a theory paper submitted to SODA 2027 (full version, double-blind). You have
read-only access from the repo root `e:\Project-git\emst-oracle-lower-bound`. Build the paper mentally
from these sources and review the WHOLE paper (do NOT re-audit Appendix A's internal proof — that is
covered by a separate review; you may assume App.A's mechanics and focus on the body + framing + refs).

READ (in order):
- `paper/sections/abstract.tex`, `paper/sections/intro.tex` (§1 results/techniques/related work),
  `paper/sections/prelims.tex` (§2), `paper/sections/support_mst.tex` (§3 + Lemma 3),
  `paper/sections/deathtime_reduction.tex` (§4), `paper/sections/main_theorem.tex` (§5 Main Theorem),
  `paper/sections/optimality.tex` (§6), `paper/sections/openquestions.tex` (§7).
- `paper/sections/app_lemma3.tex` (App.B, full proof of Lemma 3) and
  `paper/sections/app_assembly.tex` (App.C, proofs of §4–§5) — skim for whether body claims are actually
  backed by a complete proof somewhere.
- `paper/refs.bib` — the 41-entry bibliography.
- GROUND TRUTH: `docs/webpro_round5_response.md` (frozen consolidated proof; copy/compare bounds) and
  `paper/COMPONENT_MAPPING.md` (§C prior-bound table, §D the 8 literature strands, the structure-clone
  plan). The lower bound being matched is Ω(n^{1/3}) from arXiv:2504.15292 (Driemel et al., SoCG 2025).

CLAIM UNDER REVIEW: unconditional Õ_ε(n^{1/3}) orthogonal-range-counting (1±ε)-estimator of planar
Euclidean MST weight, matching Driemel et al.'s Ω(n^{1/3}) up to polylog/ε factors. The new primitive is
an "empty-cell spatial leader estimator".

REVIEW ALONG THESE LENSES. For each, find concrete defects or certify:
1. TIGHTNESS / OVERCLAIM (TPC). Is the prior-bound comparison (Table in §1.1) honest — is Õ(√n) really
   the strongest prior upper bound, and is the Ω(n^{1/3}) lower bound stated correctly (it is a query
   lower bound for constant-factor estimation)? Does the abstract/intro claim "resolve / settle the query
   complexity" in a way the polylog/ε gap does not support? Flag any sentence that overclaims.
2. PROOF-COMPLETENESS (body-level). List every theorem/lemma stated in §1–§6 whose full proof is NOT
   present in App.B/App.C (or §-body). A "sketch in body with no appendix proof" is a defect. In
   particular check: Lemma 3 (support estimator), Lemma packing W_Q≥bδ/16, leader estimator E[Z]=c /
   Var≤Mc, the additive-call accuracy, the death-time multiset identity, snapping interleaving + tail
   transfer, W_Q≤C_W·W, the assembly error budget, the W-search arithmetic, K-estimation.
3. REFERENCE-COVERAGE. The target is ~50-70 refs across 8 strands (see COMPONENT_MAPPING §D); this draft
   has 41. Name any literature strand that is genuinely MISSING or thin (not merely "could add more").
   Is any cited bound attributed to the wrong paper? Is the related-work framing (folded into §1.3)
   missing an obvious competitor a SODA referee would expect?
4. READABILITY PANEL (simulate three readers; report each separately):
   - R-W1 (one-pass skim): after reading only §1 + theorem statements, is the contribution and the
     n^{1/3} rate clear? What confuses a skimming PC member?
   - R-W2 (onboarding / a grad student reproducing it): can they follow §3→§4→§5 without getting lost?
     Where is the narrative thread dropped, a symbol used before definition, or a step unmotivated?
   - R-W3 (narrative architecture + claim precision): is the overview→core→full layering coherent? Are
     "intuition before formal block" and confident scope (no hedging/defensive writing) maintained? Any
     imprecise claim ("clearly", undefined constant, mismatched quantifier)?

OUTPUT FORMAT (strict):
VERDICT: one of {ACCEPT, MINOR-REVISION, MAJOR-REVISION, REJECT}.
Then under REASON: a numbered list. Each item: [lens][severity BLOCKER/MAJOR/MINOR] — specific location,
the precise issue or certification, and a concrete fix for defects. For the readability panel give R-W1 /
R-W2 / R-W3 verdicts explicitly (each: BLOCKER / OK-with-notes / clean). Be exhaustive; do not truncate.
