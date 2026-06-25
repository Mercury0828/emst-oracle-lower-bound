# Component-Mapping Table — SODA paper (structure-clone of NSW SODA'25)

> **Pre-writing alignment artifact** (skill 10 step 4 / writing-prompt step 3.3). Structure-clone
> target = **Naor–Srinivasan–Wajc, "Online Dependent Rounding Schemes…", SODA 2025 (arXiv:2301.08680)**.
> Venue class = **THEORY** (no page limit; ~50–60pp total = body ~10–15 + long proof appendix; full
> proofs of every claim; ~40–80+ refs). 🔴 Send to owner for sign-off BEFORE writing prose; tick
> mechanically while writing (`WRITING_PROGRESS.md`). Every bound copied from the FROZEN proof
> (`docs/webpro_round5_response.md`) at the moment of writing, never from memory.
>
> 🔴 PRECONDITION FLAG (honest): the proof is at §9.4 AI-CONVERGENCE — AI-verified + 3 audits, NOT yet
> human-verified, with ONE residual verification-debt item (the local-WSPD death-time implementation,
> inherited from Driemel et al. Lemmas 23–24). The writeup is the vehicle for human verification; writing
> that primitive's FULL proof in App. A is how we discharge the debt. Paper stays AI-level until a human
> expert signs off (gate #2). Confidence ~80% (ours) / 0.91 (Pro).

## A. Section skeleton (NSW component → our EMST paper)

| NSW component | Our instance | Notes |
|---|---|---|
| §1 Introduction | §1 Introduction | the 10-page merits story |
| §1.1 (results/extensions) | **§1.1 Our Results** | formal statement of Main Theorem (Õ_ε(n^{1/3})) + Support-MST Lemma + the "tight, matches Ω(n^{1/3})" corollary |
| §1.2 Techniques | **§1.2 Techniques** | the empty-cell SPATIAL leader estimator (the new primitive); support-regularization+snapping; range-counting clipped death-time; the cluster-count integral (CRT lineage) |
| §1.3 Further related work | **§1.3 Related work** (FOLDED INTO INTRO — do NOT make a late standalone section) | strands in §D below |
| §2 Preliminaries (+2.1) | **§2 Preliminaries** | model = orthogonal range-counting oracle on P⊆[Δ]², Δ=O(n); EMST weight; cluster-count integral w=∫(c−1)dt; single-linkage components; WSPD/(1+ρ)-spanner basics; word-RAM; randomization (Monte-Carlo, const prob); notation table |
| §3 main technique (3.1 overview/intuition → 3.2 core → 3.3 full) | **§3 The support-MST estimator** (3.1 overview+intuition → 3.2 the empty-cell leader estimator → 3.3 the additive call + removing the guess) | mirror NSW's overview→core→full layering; state Lemma 3; core estimator inline, long proofs → App. B |
| §4 second technique | **§4 The clipped death-time primitive + reduction for P** | death-time multiset identity; (1+ρ)-spanner; support regularization (packing K_h); snapping; A_L/B_L decomposition |
| §5 Applications | **§5 Main theorem: assembling Õ_ε(n^{1/3})** | Ŵ=Â_P+Ŵ_Q−Â_Q; error budget; the W-search; the final theorem |
| §6 Lower Bounds | **§6 Optimality (tightness)** | short: cite Driemel Ω(n^{1/3}); our UB matches ⇒ query complexity resolved up to polylog. (We do NOT re-prove their LB; we state the match.) Possibly fold into §1.1 + a remark if too thin. ← OWNER DECISION |
| §7 Summary & Open Questions | **§7 Open questions** | extend the empty-cell estimator to EMD (same SoCG'25 framework); higher dimensions d≥3; removing polylog; deterministic? |
| App. A (additional prelims) | **App. A: the local-WSPD death-time implementation** (🔴 the residual-debt item — FULL proof here) | representative choice, redundant-pair suppression, tie handling, global cap; tie each query-cost line to a concrete range-count. Highest-scrutiny appendix. |
| App. B (deferred proofs of §3) | **App. B: full proof of Lemma 3** | active cover + packing W_Q≥bδ/16; scale graphs + interleaving; empty-cell leader E[Z]=c, Var≤Mc; the c_j-vs-N_j accounting (candidate-root √K + exploration √K); accuracy (Riemann gap ≤σW_Q); removing the guess; approx-K |
| App. C (deferred proofs of §4) | **App. C: full proofs of §4–§5** | death-time identity; spanner stretch; packing K_h≤8W/h+4; snapping interleaving; |B_L(Q)−B_L(P)|; W_Q≤C_W·W; the assembly error budget; the W-search arithmetic |

## B. Per-claim proof completeness + placement (FIRST-CLASS — one row per claim)

| Claim (from frozen proof) | Body | Full proof | Status |
|---|---|---|---|
| **Main Thm**: Õ_ε(n^{1/3}) (1±ε)-EMST-weight estimator | §1.1 stmt + §5 assembly | App. C | to-write |
| **Lemma 3**: support-MST estimator Õ_η(√K+n/K) | §3 stmt + 3.1 intuition | App. B | to-write |
| Packing W_Q ≥ bδ/16 (4-coloring) | §3.2 inline (short) | App. B | to-write |
| Empty-cell leader: E[Z]=c, Var(Z)=Mc−c²≤Mc | §3.2 inline | App. B | to-write |
| c_j-vs-N_j accounting: candidate-root Σ=Õ(√K) AND exploration Σ=Õ(√K) | §3.3 sketch | App. B | to-write (the round-5 fix — write carefully; cores verified by execution) |
| Filtration interleaving c_Q(r⁺)≤c_Γ(r)≤c_Q(r) | §3.3 stmt | App. B | to-write |
| Accuracy: Riemann gap ≤ σW_Q ⇒ \|Ŵ(G)−W_Q\|≤βG | §3.3 | App. B | to-write |
| Death-time multiset identity {τ(v)}={0}∪MST-weights | §4 stmt | App. C | to-write |
| (1+ρ)-spanner stretch A_L(X)≤A_L(H)≤(1+ρ)A_L(X) | §4 | App. C | to-write |
| Packing K_h ≤ 8W/h+4 | §4 stmt | App. C | to-write |
| Snapping: c_P(t+δ_s)≤c_Q(t)≤c_P(t−δ_s); \|B_L(Q)−B_L(P)\|≤O(γξW); W_Q≤C_W·W | §4 | App. C | to-write |
| **WSPD death-time implementation** (the residual debt) | §4 ref | **App. A (FULL)** | 🔴 highest scrutiny — discharge the debt |
| Assembly error budget \|Ŵ(G)−W\|≤C_*ξG; W-search ⇒ W≤G_0<16W | §5 | App. C | to-write |
| K-estimation (inverse-Bernoulli, Õ(n/K)) | §4/§5 | App. C | to-write |

## C. Prior-bound comparison (table in §1.1, narrative form acceptable)

| Result | Oracle | Bound | Error | Ref |
|---|---|---|---|---|
| Czumaj et al. 2005 | range-emptiness + cone-ANN | Õ(√n) | O(n^{1/4}) rel | SICOMP'05 |
| Driemel et al. 2025 (UB) | orthogonal range counting | Õ(√n) | (1±ε) | SoCG'25 |
| Driemel et al. 2025 (LB) | orthogonal range counting | Ω(n^{1/3}) | const mult | SoCG'25 |
| **This paper** | orthogonal range counting | **Õ_ε(n^{1/3})** | (1±ε) | — |

## D. Literature strands to cover (target ~50–70 refs; NSW=86; resolver-verify EACH before drafting)
1. **Sublinear MST weight** — CRT (ICALP'01/SICOMP), Patlin–van den Brand (SOSA'25), Czumaj–Sohler (SICOMP'09), Chen–Khanna et al. (ICALP'23, arXiv:2203.14798).
2. **Range-counting / sublinear geometric oracles** — Driemel–Monemizadeh–Oh–Staals–Woodruff (SoCG'25, the source), Schibler–Xue–Zhu convex hull (SoCG'26), cell-sampling.
3. **Euclidean MST estimation** — Czumaj et al. (SICOMP'05), Arya–Mount ANN, streaming EMST (STOC'23, arXiv:2212.06546).
4. **Single-linkage clustering cost** — Peng–Sohler–Xu (arXiv:2510.11547).
5. **WSPD / geometric spanners** — Callahan–Kosaraju, Har-Peled book, Narasimhan–Smid.
6. **Distance-oracle MST/clustering** — arXiv:2310.15863; metric Steiner (arXiv:2211.03893).
7. **Connected-components / property testing tools** — components estimation, Berenbrink/CRT-type.
8. **Math tools** — Delaunay/Kruskal MST facts, Chernoff/median-of-means, range-counting data structures.

## E. Figures (SODA = schematic/construction; NO experiment plots — our numerics were verification, not paper experiments)
- **Fig. 1** (self-sufficient): the grid-support Q + active cover + the empty-cell SPATIAL leader estimator (a cell sampled incl. empty; min-rank leader of a component) — the key new idea, must be gettable from the picture + 1-line caption.
- **Fig. 2** (optional): the cluster-count integral w=∫(c−1)dt and the death-time / threshold filtration.
- **Fig. 3** (optional): support regularization + snapping (P → grid-snapped Q).
- NO heatmaps, NO measured-error plots.

## F. Length / density baseline (VERIFIED, not assumed)
- **Total target ~45–60pp** (NSW-class density; official SODA "first 10pp + unlimited appendix"). Body
  ~12–15pp (model + 3 main theorem/lemma statements + technique overview + related work + tightness);
  appendix ~30–45pp of complete proofs (App. A WSPD impl is large).
- **Refs ~50–70** (build by the 8 strands above; NSW=86 is the upper anchor).
- Risk = UNDER-length ⇒ if short, the deficit is missing proof detail or missing strands, never padding.

## G. Open structure decisions for the OWNER (raise now, not in review)
1. **§6 Optimality** as its own short section vs folded into §1.1 + a remark? (We only state the match to
   Driemel's Ω(n^{1/3}); we don't re-prove their LB.) — recommend a short standalone §6 for emphasis.
2. **Anonymization**: SODA 2027 = lightweight double-blind ⇒ write anonymized from day 1 (no "our prior
   work", no author/institution tells). Confirm.
3. **GPT-Pro/codex provenance**: the proof was AI-derived (web GPT-5.5-Pro) + AI-audited. For submission
   this is just "our proof"; the AI-assistance disclosure (if any) is an owner/venue-policy decision.
4. **Title** candidates (to seed): "Tight Range-Counting Query Complexity of Euclidean MST Weight" /
   "Estimating Euclidean MST Weight in Õ(n^{1/3}) Range-Counting Queries".
5. Scope of §7 open questions — push the EMD extension as the headline open direction (the lever that
   raises the contribution per both independent assessments)?
