# AI_STYLE_CHECKLIST — copy into each project; run as written
<!-- Origin: CDRO project, extended (copied from dynamic-weighted-mis-fat-objects/.agent, 2026-06-22). Process rule is part of the checklist. -->

## PROCESS RULE (overrides everything)
**Propose-then-approve, one by one.** Run the sweeps, produce a NUMBERED list of candidate edits with before→after snippets, present to the owner, apply ONLY approved items. Never auto-apply. If an item holds up, say "fine" — no forced findings. Never add defensive/justification prose as a "fix".

## A. Grep token sweep (flag every hit; each hit = one numbered proposal)

| # | Pattern | Action |
|---|---------|--------|
| 1 | `—` em-dash as rhetorical glue (`---` in tex) | Restructure the sentence. (Proper-noun en-dashes are fine.) |
| 2 | `such as` | Ask: shorter / more concrete? Often deletable. |
| 3 | `not only ... but also` | Cap ~2/paper; prefer "both X and Y" or "X while Y". |
| 4 | `it is worth noting` `it should be noted` `in this regard` `from this perspective` `this observation is important` | Delete; state the content directly. |
| 5 | `enable` `facilitate` `leverage` `enhance` | Replace with the concrete verb (computes, outputs, reduces, selects…). |
| 6 | `comprehensive` `holistic` `seamless` `significant` `novel` `powerful` `flexible` `general` (as advertising) | Delete or replace with the specific property. |
| 7 | `framework` `paradigm` `mechanism` `module` `strategy` `scheme` (over-broad) | Replace with the concrete noun (controller, formulation, policy, method…). |
| 8 | `we aim to` `we seek to` `we attempt to` | Say what was done. |
| 9 | `in this paper, we propose` `the proposed` `robust and efficient` | Trim; state the result, don't advertise. |
| 10 | `not X, it is Y` / `The real problem is not A, it is B` | Rewrite. EXCEPTION: genuine mathematical disambiguation is exposition — keep. |
| 11 | Defensive hedging: `not a claim` `we do not (claim|interpret)` `this is not intended` `should not be (interpreted|read|taken)` `we make no claim` `we (emphasize|stress|caution)` `does not (imply|claim)`; `rather than` (any use) | Rewrite to plain statements of fact. `rather than` is BANNED outright: restructure or split; state the contrast positively. |

## B. Read-level checks (whole-document pass)
1. Plain and understandable for a non-expert reviewer = top priority; no homemade jargon; define once in full, then use the short form.
2. No stacked abstract-noun strings.
3. Sentence-template repetition — vary or merge.
4. Template openers and rhetorical flourishes — state the mechanism directly.
5. Front-to-back repetition; metaphor/adjective density; excessive passive voice.
6. Cut obvious transition sentences; don't wrap simple things in big words.
7. Contributions: specific, limited, credible — each maps to an existing theorem.
8. Find paragraphs that preemptively defend against criticism; rewrite plainly.

## C. Theory-venue additions (this project)
- Every theorem/lemma/proposition/corollary has a COMPLETE proof (body sketch + appendix full is fine; a sketch alone is a STUB).
- Each bound copied from the frozen proof (`docs/webpro_round5_response.md`) at the moment of writing.
- Captions SHORT (one sentence = what is shown + conditions); takeaways go in the body.
- `orient, don't restate`: add low-information orienting sentences (map / intuition / motivation), never result-restating prose.
