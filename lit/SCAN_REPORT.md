# Literature Kill-Scan Report — emst-oracle-lower-bound

> Phase-0 deliverable (guide.md §3). Kill criteria were FROZEN in `guide.md` §3 before this scan.
> Run 2026-06-20 via 4 independent fresh-context web-scan threads + 1 independent second-opinion
> audit (`gate1_paper_orientation_audit.md`). **No citation, bound, or arXiv id below was
> fabricated** — each is from a retrieved abstract/PDF/API; items that could not be verified
> first-hand are flagged.

## VERDICT: **GREEN** (proceed)
No RED scoop, no RED ceiling, no pre-emption. The Ω(n^{1/3}) vs Õ(√n) counting-oracle EMST gap is
**still open**; the two load-bearing constructions (C1 point-efficient gadget, C2 RS/induced-matching
O(1)-coverage packing for COUNTING queries) **appear novel**. Strength-gate (closes vs improves) is
NOT decided by the scan — it is decided by the C1/C2 screens + attack loop (see `PHASE0_REPORT.md`).

---

## Concern table (per `guide.md` §3 kill criteria)

| # | Threat checked | Kill criterion | Finding | Status |
|---|---|---|---|---|
| 1 | **RED scoop** — someone already improved the counting-oracle EMST LB past n^{1/3} | RED if any ω(n^{1/3}) randomized (1±ε) counting-oracle EMST lower bound exists | None found. Only paper citing the source (arXiv:2603.20943) is convex-hull under EMPTINESS — different problem & oracle. Source author (Driemel) has no 2025–26 follow-up on this line. | **GREEN** |
| 2 | **RED ceiling** — an n^{1/2−Ω(1)} counting UPPER bound, or a barrier ruling out n^{1/2−o(1)} | RED if a polynomial (exponent ≤ 1/2−Ω(1)) upper bound, or an impossibility, exists | None found. Best known upper bound is Õ(√n) (which is n^{1/2−o(1)}, NOT a ceiling). No impossibility result. | **GREEN** |
| 3 | **Pre-emption** — prior space-efficient MST-distinguishing gadget (C1) or RS/O(1)-coverage COUNTING packing (C2) | If a prior construction pre-empts C1 or C2 | Neither found. RS/induced-matching in the literature is used only for matching-size estimation under EMPTINESS/pair queries; the source's own EMD argument hides one needle (not an O(1)-coverage counting packing). Both C1 and C2 appear novel. | **GREEN** |
| 4 | **Source still SOTA** (arXiv:2504.15292) | confirm no v2/v3 and no follow-up closes the gap | v1 only (10 Apr 2025); bounds unchanged; no follow-up closes the gap. | **GREEN** |
| 5 | **Czumaj boundary** correctly separated | confirm emptiness / deterministic / O(n^{1/4}) — motivation only | Confirmed (see frozen citations). Strictly weaker oracle; does NOT transfer to counting. | **GREEN** |

---

## Frozen bibliographic facts (load-bearing — freeze; do not re-derive)

- **Source.** Anne Driemel, Morteza Monemizadeh, Eunjin Oh, Frank Staals, David P. Woodruff,
  *"Range Counting Oracles for Geometric Problems,"* **SoCG 2025**, **arXiv:2504.15292** (v1 only,
  submitted 10 Apr 2025; no v2/v3). Verified from the PDF:
  - **Upper bound = Theorem 30:** (1±ε)-estimate EMST weight of n points in [Δ]² with **Õ(√n)**
    range-counting queries.
  - **Lower bound = Lemma 32** (§6): any randomized algorithm using **o(n^{1/3})** queries has at
    least a constant multiplicative error. (Lemma 31 = the MST(I) ≥ 2·MST(I′) separation lemma.)
  - **Hard instance (verbatim, §6 / Fig. 4):** **16·n^{1/3}** equal cells, each of side **4·n^{5/6}**;
    each gadget on [n^{5/6}]² subdivided into n^{4/3} finer cells, **n^{2/3} points/gadget**; heavy
    ("uniform") per-cell EMST cost **Θ(n^{7/6})**, sparse ("strip") **Θ(n^{5/6})**; **each query hits
    ≤ 4 cells**; P(a fixed query hits the heavy gadget) = 1/(4·n^{1/3}).
    - ⚠️ Corrects the guide's prior uncertainty: the numbers are **Theorem 30 / Lemma 32** (NOT
      "Lemma 6.1"); the "16·n^{1/3}" and "≤4 cells" are exact, not approximate.
- **Czumaj boundary.** Artur Czumaj, Funda Ergün, Lance Fortnow, Avner Magen, Ilan Newman, Ronitt
  Rubinfeld, Christian Sohler, *"Approximating the Weight of the Euclidean Minimum Spanning Tree in
  Sublinear Time,"* **SIAM J. Comput. 35(1):91–109, 2005**, DOI **10.1137/S0097539703435297**.
  Their **range-EMPTINESS-only** result is **deterministic**, **O(n^{1/4}) relative error**, lower
  bound **Ω(√n)** emptiness queries. (Confirmed via the source PDF's citation [22] + SIAM abstract;
  the original full text is paywalled — n^{1/4}/Ω(√n) not read first-hand, flagged.) **Cite as
  motivation only** — emptiness ⊊ counting, so it does NOT prove the counting-oracle claim. Do NOT
  conflate with Czumaj–Sohler, *"Estimating the Weight of Metric MSTs in Sublinear Time,"* SIAM J.
  Comput. 39(3):904–922, 2009 (a different, metric/distance-oracle paper).
- **Only citing paper (confirmed not a threat).** Thomas Schibler, Jie Xue, Jiumu Zhu,
  *"Approximating Convex Hulls via Range Queries,"* **arXiv:2603.20943** (submitted 21 Mar 2026, to
  appear SoCG 2026), DOI 10.4230/LIPIcs.SoCG.2026.89. Range-**emptiness**/halfplane oracle, convex
  hull problem; does **not** touch the MST counting-oracle bound. (Abstract/topic confirmed; full
  body not read first-hand — flagged.)
- **SODA 2027 CFP** (re-confirmed). Deadline **2026-07-09** (HotCRP shows the equivalent
  "Fri Jul 10 2026, 7:59 AM EDT"); conference Jan 24–27 2027, Philadelphia. Format: single-column,
  **11pt**, **1-inch margins**, letter paper; **no hard page limit** but the **first ~10 pages after
  the title must convey the merits**; full version/appendix unlimited. Blind: **lightweight
  double-blind** (anonymize from day 1). (Confirmed from HotCRP + SODA25/26 official pages + search;
  the live soda27 SIAM page returned 403 — flagged; no explicit "references not counted" clause found.)

---

## Citable tools surfaced (not threats — useful for the writeup / attack loop)
- Chazelle–Rubinfeld–Trevisan, "Approximating the MST Weight in Sublinear Time," ICALP 2001/SICOMP
  (foundational sublinear-MST; adjacency/degree model).
- Chen–Khanna et al., "Sublinear Algorithms and Lower Bounds for Estimating MST and TSP Cost in
  General Metrics," ICALP 2023, arXiv:2203.14798 (distance-oracle metric MST/TSP LBs).
- "Streaming Euclidean MST to a Constant Factor," STOC 2023, arXiv:2212.06546 — an o(√n)-SPACE
  streaming MST lower bound via Boolean Hidden Matching in high dimension (closest "√n + MST + LB +
  gadget" hit; different model — streaming space, not range-counting queries; citable as a related
  √n-threshold MST barrier).
- Ruzsa–Szemerédi / induced-matching packings (Assadi–Khanna et al.; arXiv:1701.04364, 2108.07187,
  2310.05728) — the canonical hide-one-among-many technique, but used for matching-size under
  EMPTINESS/pair queries, not exact counting. The C2 packing for COUNTING is the novel adaptation.
- Azarmehr–Behnezhad–Roghani–Rubinstein, "Tight Pair Query Lower Bounds for Matching and Earth
  Mover's Distance," arXiv:2510.16351 (sibling EMD pair-query LB; citable; not a counting packing).

---

## Per-query / per-thread search log

### Thread A — RED scoop (improved counting-oracle EMST LB past n^{1/3})
| query | finding |
|---|---|
| "range counting oracle EMST lower bound query complexity" | only the source paper; no improving bound |
| Semantic Scholar citations API for 2504.15292 (limit 100) | **exactly 1** citing paper (convex hull, irrelevant) |
| "MST weight estimation query complexity sublinear 2025/2026" | source + unrelated general-metric/streaming MST |
| "...n^{1/2−o(1)}... range counting tight 2025/2026" | only source + different-model MST/EMD |
| dblp Anne Driemel 2025–2026 | no MST/range-counting follow-up |
| → **VERDICT: NO-SCOOP-FOUND** | |

### Thread B — RED ceiling (sub-√n counting upper bound / impossibility)
| query | finding |
|---|---|
| "sublinear MST weight estimation o(√n) queries upper bound range query" | Õ(√n) is SOTA; no sub-√n |
| "EMST weight approximation o(sqrt n) queries 2025/2026" | none below √n |
| "orthogonal range counting MST polynomially below √n" | no sub-√n result exists |
| general-metric MST/TSP (2203.14798) + streaming (2212.06546) | different models; not a counting ceiling |
| → **VERDICT: NO-CEILING-FOUND** | |

### Thread C — pre-emption (C1 gadget / C2 counting packing)
| query | finding |
|---|---|
| "Ruzsa-Szemeredi induced matching ... counting not emptiness" | RS only for matching-size under emptiness/pair queries |
| "MST weight gadget lower bound sublinear euclidean" | CRT (ICALP'01), 2203.14798; no sub-n^{2/3} geometric gadget |
| "earth mover distance range counting oracle lower bound" | source EMD section hides ONE needle (not an O(1)-coverage packing) |
| "point efficient gadget shift euclidean MST weight constant fraction" | 2212.06546 (streaming, Boolean Hidden Matching); none pre-empts C1 |
| → **Both C1 and C2 appear novel** | |

### Thread D — source + citation verification
- arXiv:2504.15292 v1 only; Thm 30 / Lemma 32; hard-instance numbers verified from the PDF (above).
- Czumaj et al. exact cite + emptiness/deterministic/O(n^{1/4})/Ω(√n) confirmed (above).
- arXiv:2603.20943 resolves, convex-hull/emptiness, not MST (above).
- SODA 2027 CFP details confirmed (above).

---

## Sources that could NOT be fully accessed (honest log)
- Czumaj et al. (2005) original full text — paywalled (SIAM); the n^{1/4} / Ω(√n) figures verified via
  the source PDF's citation + SIAM abstract, not the original body.
- arXiv:2603.20943 full body — HTML encoding error + PDF 403; MST-non-involvement inferred from
  abstract/topic, not a line-by-line read.
- Live SIAM soda27 page — HTTP 403; CFP details corroborated from HotCRP + SODA25/26 official pages.
- A few arXiv month-listing pages returned 404; worked around via keyword/citation search. Brand-new
  (last-few-days) preprints not yet indexed cannot be 100% excluded — a residual scoop/ceiling risk
  to re-sweep at human gate #2 (final priority sweep).
