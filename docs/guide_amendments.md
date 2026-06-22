# Guide Amendments — emst-oracle-lower-bound (append-only)

> `guide.md` is **READ-ONLY**. This is the ONLY place where deviations from it, design changes that
> contradict a plan in it, or results that overturn one of its claims are recorded. Append-only;
> newest at the bottom; every entry dated with who/why.

## 2026-06-20 — Phase 0 bootstrap
- No amendments to `guide.md` yet. Scaffold built per `guide.md` §9 / `start_up_for_claude_code.md`.
- One layout deviation logged in `DESIGN_DECISIONS.md` D0.1 (scaffold at repo root rather than a
  nested `deepdive/emst-oracle-lower-bound/` folder, because the repo root already is the project).
  This does not contradict any `guide.md` claim; recorded here for traceability.

## 2026-06-21 — 🔴 Round-1 refutation: the guide's CORE TECHNICAL PLAN is dead (the science overruled it)
- **What died.** `guide.md` §1 ("the lever: raise the hidden degrees of freedom from Θ(n^{1/3}) to
  Θ(n^{1/2})... via a space-efficient heavy gadget") and §6 Components (1)–(3) **as written** — i.e.
  the **single hidden heavy gadget among m disjoint equal-cardinality cells** route — is **provably
  incapable of any improvement over the source Ω(n^{1/3}).**
- **The proof (ledger `P1`).** A single-cell equal-cardinality swap changes w(P) by ≤ O(s√p)
  (geometry-agnostic); the backbone forces w(P) ≥ Ω(s·m) (needs only disjointness, not tiling); s
  cancels ⇒ relative gap ≤ O(√p/m) = n^{3c/2−1}; a constant fraction needs c≥2/3 ⇒ m≤n^{1/3}. Sharp.
  This DIRECTLY refutes the guide's §0/§1 arithmetic claim that "Θ(n^{1/2}) cells × n^{1/2+o(1)} points
  packs Θ(n^{1/2}) mutually-independent candidate locations [that are detectable]" — they pack, but a
  *single-needle* difference among them is NOT (1±ε)-detectable.
- **Who verified.** Attacker codex GPT-5.5-xhigh + 2 independent fresh-context audits (rigor + escape),
  analytically and with exact-EMST numerics. Artifacts: `attack_loop/round1_C1_{brief,response,auditA,
  auditB}.md`, `attack_loop/auditB_probe*.py`.
- **What this does NOT change (no-retreat red line, §9.0b).** The **target is unchanged**:
  Ω(n^{1/2−o(1)}) for the SAME problem, SAME venue (SODA). This is a *route* refutation (the science),
  not a difficulty-driven downgrade. The guide's §0 FRAMING NOTE (hitting/coverage, NOT bit-counting)
  and the barriers B1–B3 all remain valid; we ADD B4 (single-cell gap cap) and N1 (the dead route).
- **Reduced open problem (ledger).** The only surviving direction is a **multi-needle / planted-pattern**
  hard distribution where the detectable gap is correlated across many cells while each range-counting
  query still reveals o(1) of the Ω(m)-bit pattern. The hard part moves from C1-geometry to
  C2/C3-information. Being pursued in Round 2 (fresh attacker brief). If it too is refuted, that is a
  proof-of-death candidate for a human kill/pivot gate (§9.6).
- **`guide.md` itself is unchanged (READ-ONLY).** This entry is the record of the deviation; the ledger
  `research_line_emst.md` is the live source of truth for P1/N1/B4 and the reduced problem.

## 2026-06-21 — 🔴 Round-2: the escape is ALSO near-refuted ⇒ at a §9.6 human kill/pivot gate
- **What died (further).** The multi-needle / planted-pattern escape — the only route that survived
  Round 1 — is itself near-dead (ledger `P2`/`N2`). Under the O(1)-coverage requirement (⇒ M·s ≤ O(n)),
  the active-subset multi-needle caps at n^{1/3}; the bulk-parity/coding variant is quantitatively dead
  (EMST is too local to carry a Θ(w) marginal-hidden signal). So the WHOLE gadget-packing/planted-
  pattern lower-bound approach in `guide.md` (§1, §4, §6) caps at the existing Ω(n^{1/3}).
- **Verified by.** codex GPT-5.5-xhigh (Round 2) + independent Audit C (NEAR-PROOF-OF-DEATH, 8 probes);
  with Rounds-1 audits that is codex + 3 fresh-context audits total, analytic + 16+ exact-EMST/coverage
  numerics. Not a *full* proof-of-death — one narrow, evidence-against "new primitive" loophole survives
  (a blanket impossibility is barred by the existing Ω(n^{1/3})).
- **Status vs `guide.md`.** This contradicts the guide's central premise that n^{1/2} is reachable by
  raising hidden-cell count under the budget. Per the guide's OWN §9.6/§9.0b, kill fires on
  proof-of-death and is a **human-gate decision** — so the project is paused at that gate (the executing
  agent does NOT autonomously start a new line). The no-retreat red line is respected: this is the
  science (the construction provably caps below 1/2), not a difficulty-driven downgrade.
- **Substrate-supported pivot flagged for the owner.** The obstruction is essentially *algorithmic*
  (a constant-fraction EMST gap is cheaply estimable by O(polylog) coarse range-counting queries) ⇒
  strong evidence the truth is Θ(n^{1/3}) and the Õ(√n) UPPER bound is loose. Natural pivot: prove a
  sub-√n / Õ(n^{1/3}) UPPER bound (close the same Driemel et al. gap *from above*). Alternatives: the
  EMD counting-oracle bound (guide §9.6 pre-scoped pivot); a "technique-barrier" paper (P1+P2
  formalized); escalate the attack to web GPT-5.5-Pro on the narrow loophole; or stop. Owner decides.
- **OWNER DECISION (2026-06-21): PIVOT to the UPPER bound.** Prove a sub-√n / Õ(n^{1/3}) algorithm,
  closing the same gap from above. This **supersedes the lower-bound framing of `guide.md`** (§0–§8 are
  about the *lower* bound). `guide.md` stays READ-ONLY and on record; the live plan is now the upper
  bound. New ledger `research_line_emst_upper.md`; LB ledger `research_line_emst.md` frozen. The
  Phase-0 SODA framing, venue facts, and kill-scan remain valid and reusable. Repo/idea name is now
  partially stale. The no-retreat red line holds: same gap, same venue; the LB route is provably
  (near-)dead, not abandoned for difficulty.
