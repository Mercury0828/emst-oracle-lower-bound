You are an adversarial referee for a theory paper submitted to SODA. Your job is to ATTACK, not to be
charitable. Read the actual files in this repository (you have read-only access from the repo root
`e:\Project-git\emst-oracle-lower-bound`):

PRIMARY TARGET (the newly written, highest-scrutiny appendix):
- `paper/sections/app_wspd.tex` — "The local WSPD death-time implementation" (Appendix A).

SUPPORTING CONTEXT you must read to judge App.A in context:
- `paper/sections/deathtime_reduction.tex` — §4, the clipped death-time primitive that App.A implements.
- `paper/sections/main_theorem.tex` — §5, the assembly that consumes the death-time sampler.
- `paper/sections/prelims.tex` — §2, model + cluster-count integral + the spanner/death-time view.
- `paper/macros.tex` — macro definitions.

GROUND TRUTH / SOURCES (do not let the paper contradict these):
- `docs/webpro_round5_response.md` — the frozen consolidated proof (§2 = death-time primitive). App.A must
  be consistent with every bound here. Note this file flags the local-WSPD death-time implementation as
  the one residual debt item, confidence 0.89.
- `docs/_extract/source_2504.txt` — text extract of arXiv:2504.15292 (Driemel et al., SoCG 2025), the
  paper App.A inherits its WSPD machinery from. Its Lemma 1 (telescoping sampling, ~line 216), the WSPD
  construction + Lemmas 21/22/23 (~lines 776-813), and Lemma 24 navigability (~lines 816-857) are the
  source lemmas App.A restates/uses. Check App.A's restatements against these.

WHAT THE PAPER CLAIMS (so you can attack it): an unconditional Õ_ε(n^{1/3}) orthogonal-range-counting
algorithm for (1±ε)-estimating the Euclidean MST weight of n points in [Δ]^2 (Δ=O(n)). App.A's job is to
show the clipped death-time sampler of §4 can be run on a locally-navigable (1+ρ)-spanner realized under
the oracle, at a per-search cost of Õ_ρ(1) range counts and a global cost of Õ_ε(n^{1/3}).

ATTACK ALONG THESE LENSES. For EACH, either find a concrete defect or certify it survives:
1. PROOF-CORRECTNESS. Re-derive each claim in App.A from the definitions. Specifically scrutinize:
   (a) §A.4 "bottleneck death-time search": is the expected number of extracted vertices really O(log|V|)?
       The paper reuses the harmonic argument from the leader estimator. Is the ordering it relies on
       (bottleneck distance from v) the correct one, and is the 1/j probability bound valid for the
       bottleneck Dijkstra halting at the first lower-ranked vertex? Find the gap if there is one.
   (b) the extraction-cap argument: capped searches output X_L=L. Is the claim that this only LOWERS the
       reported value (one-sided error) and that the bias is absorbable into the §5 budget actually
       correct, or could capping bias the death-time estimator in the wrong direction / break unbiasedness?
   (c) the per-search cost O(ρ^{-3} log Δ)·O(log|V|): is the scale count O(ρ^{-1} log Δ) and the
       per-scale Lemma-A.4(navigate) cost O(ρ^{-2}) correctly multiplied? Is anything double-counted or
       under-counted (e.g. expanding every reached vertex at every scale)?
   (d) the global cap §A.5: do s_P=O(ξ^{-2} n^{1/3}) searches at Õ_ρ(1) each, plus the A_L(Q) sampler,
       really sum to Õ_ε(n^{1/3})? Cross-check against main_theorem.tex.
   (e) representative choice / redundant-pair suppression / tie handling: is the spanner a single
       well-defined graph, and does suppression preserve the O(ρ^{-2} n) pair count and the
       O(ρ^{-2} log Δ) per-point degree (source Lemma 21)? Is the suppression test itself implementable
       in the claimed query budget?
   (f) Lemma A.4 (= source Lemma 24) restatement: is the 2^{i*} truncation threshold and the witness
       condition stated faithfully w.r.t. source lines 816-857? Any sign/inequality error?
2. PROOF-COMPLETENESS. List EVERY claim in App.A whose justification is sketched, asserted, or deferred
   rather than proved (e.g. "absorbed into the budget", "standard", citations to source lemmas not
   re-proved). For each, say whether deferring is acceptable for a SODA full version or whether it must
   be filled.
3. OVERCLAIM. Does App.A (or the sentences in §4/§5 that depend on it) claim more than it proves? Is any
   "Õ_ε(n^{1/3})" cost line actually only Õ(n^{1/3} · poly(1/ε)) in a way that hides a 1/ε blowup that
   should be surfaced?
4. CONSISTENCY with the frozen proof and the source paper: any place App.A's bounds, constants, or lemma
   statements disagree with docs/webpro_round5_response.md §2 or with the source extract.

OUTPUT FORMAT (strict):
VERDICT: one of {SOUND, SOUND-WITH-FIXES, FLAWED}. (SOUND only if you found nothing that needs changing.)
Then, under REASON:, a numbered list. Each item: [lens][severity BLOCKER/MAJOR/MINOR] — the specific
location (which subsection/sentence), the precise defect or the certification that it survives, and for
defects a concrete suggested fix. Be exhaustive and do not truncate. Quote the offending text.
