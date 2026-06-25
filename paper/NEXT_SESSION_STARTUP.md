# START-UP PROMPT — continue the SODA paper writeup (paste this into a fresh session)

You are continuing a theory-paper writeup in the repo `e:\Project-git\emst-oracle-lower-bound`. The math
is frozen and AI-verified; your job now is to finish drafting the SODA paper, run adversarial review, and
hand off for human verification. Read this whole prompt, then the pointer files, before doing anything.

## 0. Your role and the hard rules (read FIRST — these override defaults)

- **You are orchestrator / referee / archivist, not a solo prover.** The proof already exists (frozen).
- 🔴 **SUBAGENT ROUTING RED LINE (highest priority).** EVERY adversarial subagent — paper review, proof
  check, refutation/audit, reference fact-check, writing cold-reader — **goes through Codex**
  (`gpt-5.5`, `model_reasoning_effort="xhigh"`), **never** a Claude Task subagent. You write the
  self-contained prompt → call Codex → capture the full `VERDICT` + full `REASON` (never truncate) →
  archive. Two routes (either counts): ① MCP — `claude mcp list` should show `codex ✔ Connected` (it was
  registered for this project); ② CLI inline —
  `codex exec --sandbox read-only --skip-git-repo-check -m gpt-5.5 -c model_reasoning_effort="xhigh" [-c tools.web_search=true] --output-last-message <out.md> - < <prompt.md>`.
  If BOTH routes are down: STOP, tell the owner, paste the install steps (`codex login` →
  `claude mcp add codex -- codex mcp-server`), wait. **Never** fall back to a Claude subagent for any
  judging/attacking/auditing/scoring task. The ONLY exception: NON-adversarial forensic deep-reading
  (just reading a paper/PDF, no judgement) may use your own read tools. See memory
  `subagent-routing-codex-only`.
- 🔴 **Honesty rail.** The result is at §9.4 **AI-convergence — AI-verified, NOT human-proved**, with one
  residual verification-debt item (the WSPD death-time implementation). Never write or claim "proved".
  Never fabricate a citation, bound, or page count.
- **Language discipline.** Talk to the owner / write reports in **Chinese**; all work-products (the
  paper, ledgers, code, commit messages) in **English**.
- **No defensive writing** (owner standing rule): no Limitations / Future Work section, no "we do not /
  cannot / leave to future work". State scope as a confident model definition. (skill 07 / skill 10.)
- **Push to the project's GitHub after milestones.** Commit per section; the remote is `origin/main`.

## 1. What the paper proves (one paragraph)

An unconditional **$\widetilde O_\eps(n^{1/3})$** orthogonal-range-counting algorithm for
$(1\pm\eps)$-estimating the Euclidean MST weight of $n$ points in $[\Delta]^2$ ($\Delta=O(n)$), matching
the $\Omega(n^{1/3})$ lower bound of Driemel et al.\ (SoCG 2025, arXiv:2504.15292) up to polylog — i.e.\
resolving the query complexity, closing their $\widetilde O(\sqrt n)$ vs $\Omega(n^{1/3})$ gap from above.
The one new primitive is the **empty-cell spatial leader estimator** (sample spatial cells incl. empty
ones; min-rank leader gives $\E Z=c$, $\Var\le Mc$), plus active-cover packing $W_Q\ge b\delta/16$,
support-regularization/snapping, and a range-counting clipped death-time estimator.

## 2. Read these before writing (in order)

1. `paper/WRITING_PROGRESS.md` — exact section status + build instructions + owner decisions.
2. `paper/COMPONENT_MAPPING.md` — the structure-clone plan (target = NSW SODA'25, arXiv:2301.08680) +
   per-claim proof-placement table + prior-bound table + the 8 literature strands + length baseline.
3. `docs/webpro_round5_response.md` — **the frozen consolidated proof** (copy every bound from here, never
   from memory). §1.1–1.11 = Lemma 3; §2 = death-time; §3–4 = regularization/snapping; §5–7 = assembly.
4. `.skill_js/skills/10_paper_production_pipeline.md` and `07_writing_and_style.md` — the writing
   methodology (skill 10 **Phase W-1 venue gate** is the spine). `.agent/AI_STYLE_CHECKLIST.md` = the
   per-batch style sweep.
5. `lit/GATE2_DEDUP_SWEEP.md` — the dedup/novelty sweep (refs + contribution boundary).
6. (context) `docs/webpro_thread_state.md`, `research_line_emst_upper.md` — how the proof was reached.

## 3. Venue model (already decided — do NOT re-derive, just obey)

**SODA = THEORY class.** No page limit; first ~10pp convey merits; **full proofs of every claim** (a
"sketch in body" is a STUB to finish); total **~45–60pp** (body ~12–15 + long proof appendix); **~50–70
references** built by literature strand. The failure mode is UNDER-length / sketchy proofs / thin refs,
never "too long". Lightweight double-blind: anonymized (no author/affiliation/self-citation).

## 4. What is already done (≈12pp, compiles clean)

Build: `cd paper && latexmk -pdf -interaction=nonstopmode main.tex` (TeX Live 2025). Intermediates are
gitignored. **Macro note: the range-count macro is `\rcount`, NOT `\count` (a TeX primitive).**

- Scaffold: `paper/main.tex`, `macros.tex`, `sections/*.tex` (11 files), `refs.bib` (8 core entries).
- **§2 Preliminaries** — full (model, oracle, cluster-count integral, death-time view, notation table).
- **§3 Support-MST estimator** + **App.B (full proof of Lemma 3)** — DONE, no sketches (packing,
  interleaving, leader-estimator variance, the c_j-vs-N_j two-part accounting both $\widetilde O(\sqrt
  K)$, accuracy, guess removal, approx-K).
- **§4 death-time + reduction** + **§5 assembly (Main Theorem)** + **App.C (full proofs)** — DONE
  (sampler, spanner stretch, $K_h$ packing, snapping, tail transfer, error budget, W-search).
- §1 intro / §6 / §7 / App.A are STUBS with TODO maps.

## 5. What remains — do in this order

**(a) 🔴 App.A — the WSPD death-time implementation (`sections/app_wspd.tex`).** This is the residual
verification-debt item (Pro deferred it to "source Lemmas 23–24"). FIRST forensically read
arXiv:2504.15292 §on WSPD + its Lemmas 23–24 + the uniform-sampling Lemma 1 (this is non-adversarial
reading → your own WebFetch/read tools are fine). THEN write the FULL implementation: uniform point
sampling under the oracle (label `sec:prelim-sample`, referenced from §3), the WSPD construction realized
by range counts, local navigability / bottleneck search, representative choice, redundant-pair
suppression, tie handling, the global query cap, with **each query-cost line tied to a concrete
range-count**. Goal: a self-contained, line-by-line-auditable appendix that discharges the debt. This is
the part a human referee will scrutinize most — be maximally explicit, flag anything you are < ~95% sure
of in `WRITING_PROGRESS.md`.

**(b) §1 Introduction (`sections/intro.tex`) — write LAST (per W1 order; the theorems it points to now
exist).** §1.1 Our Results (state Thm `thm:main` + Lemma `lem:support` + the tightness corollary; include
the prior-bound comparison table from COMPONENT_MAPPING.md §C). §1.2 Techniques (the empty-cell spatial
leader estimator as the headline idea; support-regularization/snapping; range-counting death-time; the
cluster-count integral with CRT lineage). §1.3 Related work **folded into the intro** (the 8 strands).
Contributions are pointers to existing theorems, hierarchical, not pre-narrated.

**(c) §6 Optimality (standalone short section — owner decided) + §7 Open questions** (headline: extend the
empty-cell estimator to EMD in the same SoCG'25 framework — this is the lever both contribution
assessments named for raising the result from borderline to solid SODA).

**(d) refs.bib → ~50–70 entries** by the 8 strands in COMPONENT_MAPPING.md §D; **every entry
resolver-verified** (arXiv ID or DOI) before use — no placeholders. (Resolving refs is forensic → own
tools OK.)

**(e) Adversarial review — ALL via Codex (red line).** Run the panel from skill 10/08:
6 lenses (proof-correctness "re-derive from the definitions"; tightness/rigor; TPC/overclaim — is the
compared prior bound the true strongest; style/fresh-reader; **PROOF-COMPLETENESS** "list every claim
whose proof is sketched/deferred"; **REFERENCE-COVERAGE" "name missing strands; flag if refs < venue
norm"), plus the **readability panel R-W1/R-W2/R-W3** (one-pass skim / onboarding / narrative-architecture
+ claim-precision). Freeze all concerns in `paper/REVIEW_round1_concerns.md`, triage (ACCEPT / AS-SENTENCE
/ COUNTER-STRENGTHEN / DECLINE / NEEDS-PROOF), fix, re-audit.

**Convergence gate (all four, checked against the NSW exemplar, not assumed):** (a) every claim has a
COMPLETE proof; (b) total ~45–60pp; (c) refs ~50–70 and no missing strand; (d) readability panel returns
no BLOCKER. Do NOT declare "writing done" without reporting measured pages, proof-completeness count, ref
count, and readability-panel result.

**(f)** Then report to the owner (Chinese) and hand the consolidated PDF for **human-expert verification**
(gate #2) — especially App.A (WSPD) + the full Lemma 3 accounting. Final pre-submission: re-run the
preprint priority sweep (`lit/GATE2_DEDUP_SWEEP.md` flagged a same-week-scoop residual).

## 6. Discipline reminders

- Copy every bound from `docs/webpro_round5_response.md` at the moment of writing; never from memory.
- Update `paper/WRITING_PROGRESS.md` after every section; on long context, re-read it + the frozen proof
  before continuing.
- Per-batch style sweep (`.agent/AI_STYLE_CHECKLIST.md`): em-dash≈0, no `rather than`, no advertising
  adjectives, intuition before every formal block, short captions.
- Commit per section with the `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
  trailer; push after milestones.
