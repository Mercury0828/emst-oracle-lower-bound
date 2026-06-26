# R3 — Pre-submission cold-reader panel (SODA 2027) + anonymization audit

All four runs are **Codex `gpt-5.5`, `model_reasoning_effort=xhigh`, `--sandbox read-only`** (per the routing
red-line: adversarial review goes through Codex, never a Claude subagent). Raw verdicts archived under
`docs/reviews/`. Date: 2026-06-26. Paper state at review: 44pp, body p1–24, after S1 self-citations.

## Panel verdicts
| Reviewer | Mandate | VERDICT | BLOCKER |
|---|---|---|---|
| R-W1 | first-10-pages skim / merits | **SKIM-PASS** | none |
| R-W2 | hands-on navigability | **FOLLOWABLE** | none |
| R-W3 | narrative + claim precision | **CLAIMS-INCONSISTENT** | **1** |
| Anon | double-blind leak audit | **ANON-LEAK** | (only the S1 self-cites) |

## BLOCKER (R-W3) — FIXED
- Δ=O(n) regime stated in abstract + main theorem but **dropped** in the intro corollary
  (`intro.tex`) and optimality corollary (`optimality.tex:cor:tight`), making them read broader than the
  theorem. → **Fixed**: both corollaries now carry "of $n$ points in $[\Delta]^2$ with $\Delta=O(n)$".

## SHOULD-FIX applied
- [R-W2] **Rendering bug**: 6× malformed `\Theta_xi(K_0)` (missing backslash, rendered "Θ_x i") in
  deathtime_reduction / overview / main_theorem. → all corrected to `\Theta_\xi(K_0)`.
- [R-W3] success probability absent from abstract → abstract now says "with probability at least $2/3$".
- [R-W2] `U_Q` "computable from $n$ alone" → "from the known parameters $n,\Delta$" (support_mst).
- [R-W2] `\rcount\cdot>0` typo → `\rcount{c}>0` (app_wspd).
- [R-W2] `C_*` used before introduced → defined at the head of §6 (main_theorem).
- [R-W2] `C_\xi` used before its dependence stated → "$C_\xi=\Theta(1/\xi)$" added at first use (§5).
- [R-W2] scale-graph interleaving body line only true in scaling regime → pointer to `sec:app-interleave`
  added for the boundary case $a(r)=h$.

## SHOULD-FIX / NIT deferred (non-blocking, optional)
- [R-W1] §2.3/§2.4 add a small variable table / boxed roadmap — layout change, would expand §2; skipped.
- [R-W1] §2 opening "Nothing here is used later" undersells the overview — NIT, left.
- [R-W2] `\rho` introduced before notation paragraph — NIT, left.

## Anonymization audit (Codex) — clean except the self-citations
- [OK] no Houston/affiliation/email/ORCID/grant/repo URL/acknowledgments; no first-person self-citation;
  PDF metadata empty. Double-blind otherwise intact.
- [LEAK]/[DE-ANON-RISK **HIGH**] the **5 S1 self-citations** (Shen26Bilevel, Zhong25UNIQ, Zhong24DP,
  Shen26CBAM, Shen25JointBidding) put the author's name + collaborators in the bibliography as a clustered,
  off-topic, same-group set → points a knowledgeable reviewer to the Shen/Han/Shi/Fan group AND is a
  relevance/credibility risk (they do not support the Euclidean-MST contribution). R-W1 independently
  flagged the same sentence as first-10pp skim-drag.
- **Codex recommendation: remove all 5.** → escalated to owner (the prompt reserved this decision);
  pending owner call before the JOINT exit gate is closed.

## JOINT exit gate status — CLOSED (green)
- Owner decision on self-citations: **keep only the closest one** (Shen26CBAM); removed the other 4.
- Re-checks on final text (Codex, archived docs/reviews/R3_*_recheck.md):
  - **R-W3 RE-CHECK: CLAIMS-CONSISTENT** — Δ=O(n) regime now in both corollaries; no new BLOCKER/SHOULD-FIX/NIT.
  - **ANON RE-CHECK: ANON-CLEAN** — 4 removed refs gone+uncited; single Shen26CBAM = DE-ANON-RISK MEDIUM,
    "probably acceptable" (the keep-1 trade-off the owner chose; could be dropped to 0 to remove the residual).
- No BLOCKER across the panel; first-10pp merits PASS (R-W1); protect-list intact; build clean (0 undefined,
  44pp). Gate closed.
