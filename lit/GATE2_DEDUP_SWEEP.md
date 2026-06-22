# Gate-#2 Priority / Dedup Sweep — UPPER-bound result (Õ_ε(n^{1/3}) range-counting EMST weight)

> Run 2026-06-21 at the §9.4 AI-convergence handoff, BEFORE any writeup/submission. The Phase-0 scan
> (`lit/SCAN_REPORT.md`, 2026-06-20) was framed for the LOWER bound; this sweep is the focused re-check
> for OUR candidate UPPER-bound result: an unconditional **Õ_ε(n^{1/3})** orthogonal-range-counting
> algorithm for (1±ε)-estimating Euclidean MST weight (closing Driemel et al.'s Ω(n^{1/3}) vs Õ(√n) gap
> from above). No citation/bound below was fabricated; items not read first-hand are flagged.

## VERDICT: **GREEN — NO SCOOP.**
No published or preprinted **sub-√n** (let alone Õ(n^{1/3})) query bound for Euclidean MST weight under
the **orthogonal-range-counting** oracle exists. The source paper's **Õ(√n)** (Driemel et al., Thm 30)
remains the state of the art on the upper side; our result would be the **first to close the gap from
above**. The newly-surfaced 2025 works are in **different oracle models** (graph adjacency / distance
oracle) — related work to cite, NOT pre-emptions. Residual risk: brand-new (last-few-days) preprints and
DB-indexing lag — RE-SWEEP immediately before submission.

## Scoop check (the decisive question)
| Threat | Finding | Status |
|---|---|---|
| A sub-√n / Õ(n^{1/3}) UPPER bound for EMST weight under **range counting** | None found across 8+ targeted searches (2025–2026). Õ(√n) (source Thm 30) is SOTA. | **NO SCOOP** |
| A follow-up to Driemel et al. closing the gap (either side) | Citations of arXiv:2504.15292 = still only the convex-hull/**emptiness** paper (arXiv:2603.20943, SoCG'26) — does not touch the MST counting bound. No Driemel-group 2026 follow-up. | **NONE** |
| Our specific new primitive (empty-cell SPATIAL leader estimator for component counts under range counting) appearing elsewhere | Not found; the "cell sampling" primitive in the source samples NONEMPTY cells, not the empty-cell spatial estimator we use. | **NOVEL (appears)** |

## Related work to CITE (NOT scoops — different model/quantity; they sharpen our contribution boundary)
- **Chazelle–Rubinfeld–Trevisan** (ICALP'01 / SICOMP): the cluster-count-integral / connected-components
  reduction for MST weight. **GRAPH adjacency-degree model.** We ADOPT (and cite) this reduction; we do
  NOT claim it. Õ(d̄·W·ε^{-2}) with matching LB.
- **Patlin & van den Brand, "Sublinear-Time Algorithm for MST-Weight Revisited," SOSA 2025**
  (epubs.siam.org/doi/10.1137/1.9781611978315.3). Simpler analysis + improved query count for CRT
  MST-weight. **GRAPH adjacency model**, not range counting. Cite as the latest CRT-model refinement.
- **Peng, Sohler, Xu, "Sublinear Algorithms for Estimating Single-Linkage Clustering Costs,"
  arXiv:2510.11547 (Oct 2025).** Estimates the single-linkage hierarchy cost Σ_k cost_k (spanning-forest
  weights) to (1±ε) on average, **adjacency-list queries on a weighted graph** (avg degree d, weights
  {1..W}), Õ(d√W/ε³), extended to metric spaces, with near-matching LBs. **NOT range counting, NOT the
  Euclidean geometric n^{1/3}**, and a different quantity (the full hierarchy cost, not w(MST)). Closely
  related framing (single-linkage = our cluster-count picture; Sohler is a key sublinear-MST author) —
  cite prominently as related; contribution boundary stays clean (model + quantity + geometry differ).
- **Czumaj, Ergün, Fortnow, Magen, Newman, Rubinfeld, Sohler (SICOMP 2005):** range-**emptiness** +
  cone-ANN, deterministic, Õ(√n) queries, O(n^{1/4}) relative error, Ω(√n) emptiness LB. Motivation only
  (emptiness ⊊ counting). [n^{1/4}/Ω(√n) not read first-hand — flagged in Phase-0 scan.]
- **Czumaj–Sohler (SICOMP 2009):** metric MST, distance-oracle model. Related; different oracle.
- **"Metric Clustering and MST with Strong and Weak Distance Oracles," arXiv:2310.15863:** distance-oracle
  MST/clustering. Related; different oracle. (Abstract-level; not read first-hand.)
- **"Streaming Euclidean MST to a Constant Factor," STOC 2023 (arXiv:2212.06546):** o(√n)-SPACE streaming
  EMST LB via Boolean Hidden Matching. Different model (streaming space). Citable √n-threshold context.

## Contribution boundary (clean)
Our claimed novelty, after the sweep, is precise and uncontested:
1. **The first sub-√n — and tight Õ(n^{1/3}) — query bound for Euclidean MST weight under the PURE
   orthogonal-range-counting oracle** (no cone-ANN, unlike Czumaj'05), closing Driemel et al.'s gap from
   above and matching their Ω(n^{1/3}).
2. **The new primitive:** the empty-cell SPATIAL leader estimator for single-linkage component counts via
   range counting (+ the active-cover 4-coloring packing W_Q=Ω(bδ) that makes its variance sum to √K).
3. **The support-regularization/snapping reduction** turning the implicit grid-support MST into a
   range-countable object, and the clipped death-time estimator adapted to range-counting queries.
The cluster-count integral, the death-time multiset identity's CRT lineage, and single-linkage cost
estimation are PRIOR ART (CRT; Peng–Sohler–Xu; Patlin–van den Brand) — cited, not claimed.

## Honest residual / not-read-first-hand
- Brand-new preprints (last few days) and citation-DB lag cannot 100% exclude a same-week scoop —
  **RE-SWEEP at submission** (the Phase-0 scan flagged this; it stands).
- arXiv:2510.11547 and the SOSA'25 paper bodies were not text-extractable via fetch; model/bounds taken
  from the arXiv abstract (2510.11547, read verbatim) and the SOSA/SIAM listing — flagged.
- Citation completeness relies on web search + Semantic-Scholar-style listing; a full Google Scholar
  "cited by" pass is advisable at submission.

## Sources
- Source: arXiv:2504.15292 (Driemel, Monemizadeh, Oh, Staals, Woodruff), SoCG 2025.
- Peng–Sohler–Xu: arXiv:2510.11547 (abstract read verbatim).
- Patlin–van den Brand: SOSA 2025, doi 10.1137/1.9781611978315.3.
- Only citing paper: arXiv:2603.20943 (convex hull / emptiness, SoCG 2026).
- Distance-oracle MST: arXiv:2310.15863. Streaming EMST LB: arXiv:2212.06546.
