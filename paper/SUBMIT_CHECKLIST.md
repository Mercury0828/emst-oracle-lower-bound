# SODA 2027 — Pre-submission checklist

Target: **SODA 2027** · portal **soda27.hotcrp.com** · full-paper deadline **2026-07-09 23:59:59 UTC-12 (AoE)** · Philadelphia, Jan 24–27 2027.
Status keys: [x] done/self-verified · [~] in progress · [ ] TODO · [OWNER] needs owner decision/account.

## Deliberate content additions (this stage only)
- [x] **S1 self-citations → 5** (owner strategy). All 5 resolver-verified, third person, grouped in §Related work
  (`sec:intro-related`) as "adjacent efforts under a constrained access budget", not misclaimed as sublinear/PT.
  Keys: Shen26Bilevel (IEEE Systems J. 2026), Zhong25UNIQ (arXiv:2512.00401), Zhong24DP (arXiv:2412.12387),
  Shen26CBAM (arXiv:2605.03304), Shen25JointBidding (PESGM 2025). Compiles clean, 0 undefined.
  ⚠️ none topically related to EMST; de-anon cluster risk → assessed in S5, owner to weigh.
- [x] **S2/S3 R3 cold-reader panel** (Codex, 3 reviewers) + JOINT exit gate **CLOSED**.
  R-W1 SKIM-PASS, R-W2 FOLLOWABLE, R-W3 CLAIMS-INCONSISTENT (1 BLOCKER) → fixed (Δ=O(n) regime in both
  corollaries) + 7 SHOULD-FIX (incl. a real `\Theta_xi` rendering bug). Self-cites reduced 5→1 (owner).
  Re-checks on final text: **R-W3 CLAIMS-CONSISTENT**, **ANON-CLEAN**. Build clean, 0 undefined, 44pp.
  Verdicts frozen: REVIEW_writing_R3.md + docs/reviews/R3_* (incl. *_recheck).

## Format compliance (SODA 2027 CFP: 11pt+, single-column, single-space, 1-inch margins all around, letter; violation = summary rejection)
- [x] documentclass `[11pt]{article}` (≥11pt ✓); `geometry[letterpaper,margin=1in]` (1-inch all around ✓);
  single-column (article default, no `twocolumn` ✓). main.tex:1,6.
- [x] fonts embedded — `pdffonts main.pdf`: every font `emb=yes` (no "no" rows).
- [x] no hard page limit; refs not counted; appendix unlimited (full proofs in App. A/B/C). 44pp total.
- [~] first ~10pp convey merits — R-W1 cold-reader (Codex) verifying; JOINT gate S3.
- [x] ref format consistent (68+5 entries, BibTeX, compiles 0 undefined).

## Anonymization (SODA 2027 CFP: double-blind — names/affiliations/emails must not appear at start or in body)
- [x] empty `\author{}`; no `\thanks`; no acknowledgments/funding section; no "NSF/grant/funded" (the grep
  hits were the substring "nsf" inside "tra-nsf-er"). main.tex:37.
- [x] self-citations in third person (no "our prior work"); grouped, no first-person tell.
- [x] S5 independent Codex audit done + re-check (docs/reviews/R3_anon_audit.md, R3_anon_recheck.md):
  no Houston/email/ORCID/grant/URL, no first-person self-citation, empty PDF metadata. The 5-self-cite
  HIGH-risk cluster was the only finding → owner reduced 5→1 (Shen26CBAM). Re-check: **ANON-CLEAN**, single
  cite = DE-ANON-RISK MEDIUM (acceptable; could drop to 0 to remove the residual).

## Submission mechanics (SODA 2027, confirmed via CFP + HotCRP)
- [x] portal **soda27.hotcrp.com**; deadline **Fri 2026-07-09 23:59:59 UTC-12 (AoE)** = Jul 10 07:59 EDT.
- [~] abstract registration: CFP has an abstract-registration component; no clearly *separate earlier*
  deadline found (recent SODA registers title/abstract within the same flow). [OWNER] confirm inside HotCRP
  whether a title/abstract must be entered before the paper-upload sub-deadline.
- [x] double-blind wording confirmed (SODA 2027 CFP): no author identity at start or in body.
- [x] full version / appendix: SODA allows the full version in the same PDF (appendix unlimited; reviewers
  need not read it). Our full proofs are in App. A/B/C — compliant.
- [OWNER] COI / PC conflict list (HotCRP).
- [OWNER] subject areas / topics selection (HotCRP).
- [OWNER] co-author / author list entry in HotCRP (PC-visible only; does not break blinding of the PDF).
