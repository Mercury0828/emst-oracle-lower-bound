# Round 4 — GPT-5.5-Pro response (verbatim, human-relayed 2026-06-21) — NEW CLAIMED CLOSURE (spatial-cell estimator)

> Pasted by the owner. LaTeX cleaned; all claims/math preserved. **Pro presents a REPAIRED support-MST
> lemma that defeats the round-3 counterexample via a NEW primitive — sample SPATIAL candidate cells
> (incl. empty), not support points.** Citation [1]=arXiv:2504.15292. Decisive numeric test:
> `attack_loop/webpro_verify_round4.py`. Independent audit: `webpro_round4_audit.md`.

---

**Claim:** complete repair, but NOT via polylog support-point samples (that remains false). The
replacement: **sample uniformly from spatial candidate cells, INCLUDING EMPTY cells, and attach a
random-leader estimator to each occupied sampled cell.** A significant collection of rare MST edges must
occupy enough spatial cells at its own length scale ⇒ a variance bound.

**Repaired support-MST lemma:** estimate W_Q=w(MST(Q)) within (1±η) w.constant prob using
**Õ_η(√K + n/K)** range-counting queries to P (Õ_η(√K) if K known to relative accuracy). Does NOT invoke
the source's occupied-cell sampler (which spends Õ(√n) — the prior obstruction).

## 1. The active spatial cover
K known; q=⌈√K⌉. From the root dyadic cell, repeatedly subdivide every nonempty cell into 4 children;
stop at the first level with b≥q nonempty cells, side δ, collection B. Then q≤b<4q. Found with
O(q·log(Δ/h)) support-emptiness queries = that many P-counts (the useful part of Czumaj's active-block
construction, STRIPPED of support-point sampling).
**Packing lower bound: W_Q ≥ δ(b−4)/8 = Ω(bδ).** (Pick one Q-point per active block; 4-color blocks by
index parities; same-color ≥δ apart; one class has ≥b/4 points ⇒ MST ≥ δ(b/4−1); and w(MST(S))≤2W_Q for
any S⊆Q.)

## 2. Approximate component graphs at one length scale
c(t) = #components of the complete Euclidean threshold graph on Q (edges ≤ t). Fix σ=Θ(η), threshold
r≥h. Pick dyadic a=a(r): if σr ≲ h use the h-cells (≤1 point each); else a dyadic multiple of h with
σr/128 ≤ a ≤ σr/64. Graph Γ_r: vertices = nonempty a-cells; for a=h adjacency = centers within r; for
a>h, cells C,D adjacent iff dist(C,D)≤r (min Euclidean sq distance). **Degree O(σ^{-2})** (only cells
within r adjacent, side Ω(σr)) ⇒ every neighbor enumerable by O(σ^{-2}) rectangle-emptiness queries.
NO cone/WSPD/component-restricted query.
**Filtration interleaving (a>h):** c(r+2√2 a) ≤ c̃(r) ≤ c(r), where c̃(r)=#components of Γ_r. (Euclidean
edge ≤r joins cells ≤r apart; cell-graph adjacency lifts to a Euclidean path at threshold r+2√2 a.) For
a=h exact. With geometric r_{j+1}=(1+σ)r_j and r_j+2√2 a_j ≤ r_{j+1}: **c(r_{j+1}) ≤ c̃_j ≤ c(r_j)** (1).
Replaces the WSPD-spanner distortion argument entirely.

## 3. Packing the occupied cells
N_j = #nonempty a_j-cells. 4-coloring ⇒ N_j ≤ 8W_Q/a_j + 4; small scale a_j=h uses W_Q≥(K−1)h. Either
way: **N_j ≤ C(1 + W_Q/(σr_j))** (2). Given guess G≥W_Q: deterministic U_j = C(1+G/(σr_j)) ≥ N_j (3).

## 4. The empty-cell random-leader estimator (THE NEW PRIMITIVE)
Family U of M candidate grid cells containing all vertices of a graph, only N occupied, occupied-cell
graph has c components + bounded-degree local access. One trial: (1) pick X uniform from all M candidate
cells; (2) if X empty → Z=0; (3) else lazy random ranks on occupied cells; (4) explore X's component in
fixed BFS order, stop on a lower-ranked cell; (5) if found → Z=0, if exhausted → Z=M.
**E[Z]=c, Var(Z)≤Mc** (4) (exactly c of the M cells are component minima). If c≤N≤U, k=Θ(MU/α²) trials
estimate c to additive α w.constant prob (median amplification for polylog failure).
**Exploration cost:** sampled occupied cell in a size-s component ⇒ E[examined] ≤ 1+H_{s-1}=O(log s).
P(candidate occupied)=N/M ⇒ expected local expansions over k trials = Õ(k·N/M) ≤ Õ(U²/α²) (5). **Empty
candidate trials dominate** — and emptiness is exactly what is cheap from P.

## 5. Candidate cells inside the active cover
Scale a_j ≤ δ: every nonempty a_j-cell lies in one of the b active δ-blocks; #possible a_j-cells in their
union = M_j = b(δ/a_j)² ≤ C·bδ²/(σ²r_j²) (6). A uniform candidate cell: pick an active block uniformly +
a uniform dyadic subcell (free); emptiness = one P-count. If a_j>δ: all nonempty a_j-cells are the ≤b
distinct dyadic ancestors of active blocks; c̃_j computed EXACTLY in O_η(b). **Coarse scales explicit;
fine scales sampled; NO recursion.**

## 6. Additive estimator given an upper guess
G≥W_Q. r_0=max{h, ηG/(C_0 K)}; r_j=r_0(1+σ)^j until > diam(Q); d_j=σr_j; T=O_η(log(Δ/h)) scales. For each
fine scale estimate c̃_j to additive **α_j = ηG/(C_1 T σ r_j)** (7), using U_j (3).
**Query accounting:** M_j U_j / α_j² ≤ C·(bδ²/σ²r_j²)(G/σr_j)(T²σ²r_j²/η²G²) = C(T²/η²σ)(bδ²/(G r_j)).
Since G≥W_Q=Ω(bδ): **M_j U_j/α_j² ≤ C_η T² (δ/r_j)** (8). Σ_j δ/r_j = O(δ/(σr_0)); with r_0=ηG/(C_0 K):
δ/r_0 ≤ C_0 K δ/(ηG) ≤ O(K/(ηb)) = O_η(√K). (r_0=h case: G≥(K−1)h & G=Ω(bδ) ⇒ δ/h=O(K/b)=O(√K).) So
all candidate-cell trials over all scales use **Õ_η(√K)** range counts. Explorations: U_j/α_j=O(T/η) ⇒
polylog local expansions/scale (global cap + Markov). Coarse scales O_η(bT)=Õ_η(√K).

## 7. Recovering the MST weight
W_Q = ∫_0^∞ (c(t)−1)dt; ∫_0^h(c−1)=(K−1)h (distinct centers ≥h apart). **Ŵ_G = (K−1)h + Σ_j d_j(ĉ_j−1)**
(9). Interval [h,r_0] contributes ≤ K r_0 ≤ ηG/C_0 (10). By (1) the Riemann sums sandwich the tail
integral; their gap = Σ d_j(c(r_j)−c(r_{j+1})) — each MST edge of length ℓ∈(r_j,r_{j+1}] contributes d_j
≤ σℓ ⇒ **Riemann gap ≤ σW_Q** (11). On the good event Σ d_j|ĉ_j−c̃_j| ≤ Σ d_j α_j ≤ ηG/C_1 (12). Choose
C_0,C_1 large, σ=Θ(η) ⇒ **|Ŵ_G − W_Q| ≤ ηG** when G≥W_Q (13).

## 8. Removing the upper guess
U=(K−1)diam(Q); run with additive 1/20 for G=U,U/2,…; stop at first Ŵ_G ≥ G/3 (amplify all calls). G≥4W_Q
⇒ Ŵ_G ≤ W_Q+G/20 ≤ G/4+G/20 < G/3 (continue); G∈[W_Q,2W_Q) ⇒ Ŵ_G ≥ W_Q−G/20 > G/3 (stop). ⇒ W_Q ≤ G_0 <
4W_Q; final call additive Θ(η) ⇒ (1±η). Log #guesses hidden in Õ.

## 9. Estimating K
Sample uniform p∈P, m(p)=#points in its h-cell, X(p)=n/m(p): E[X]=K, E[X²]=nΣ1/m_C ≤ nK ⇒ relative
estimate of K in Õ_η(n/K) samples. Accurate K changes q=√K, baseline (K−1)h, cutoff r_0 by 1+O(η).
⇒ **Õ_η(√K + n/K).**

## 10. Why the satellite obstruction disappears
The round-3 counterexample defeats support-POINT sampling (satellite cells have tiny support mass). The
new estimator NEVER samples by support mass — at scale r it samples uniformly among M_r=O(bδ²/(η²r²))
SPATIAL cells. If c_r contributes materially to the MST integral, r·c_r is large; every component
occupies ≥1 spatial cell ⇒ P(sampling a component leader) is correspondingly large. Var(Z_r)≤M_r c_r,
and W_Q=Ω(bδ) turns this into the δ/r cost (8), summing to √K. **A rare feature can be support-mass-rare
OR spatially-hidden-at-its-scale, but NOT both while contributing a constant fraction of the MST weight.**

## 11. Consequence for the original problem
Insert into the validated round-2 reduction; K=Θ_ε(n^{2/3}) ⇒ support-MST estimate Õ_ε(√K+n/K)=
**Õ_ε(n^{1/3})**. Other pieces: A_L(P) clipped death-time; A_L(Q) with O_ε(1) genuine support samples;
B_L(Q)=W_Q−A_L(Q); snapping transfers B_L(Q)→B_L(P); upper-guess search sets L=Θ(W/n^{2/3}). **NO support
seeds reused across thresholds; every scale uses independent candidate-cell trials; summed error via the
explicit additive allocation (7),(12).** ⇒ believed complete result **Õ_ε(n^{1/3})**, matching Ω(n^{1/3}).

### Answers to the four questions
(a) Yes — first-crossing quadtree has b=Θ(√K) active blocks, found with Õ(√K) emptiness queries.
(b) **An explicit MST on active-block representatives alone is NOT sufficient** [⇐ refutes the
orchestrator's round-4-brief suggestion]; instead compute every scale coarser than the active blocks
explicitly and estimate every finer scale with the cell-leader estimator.
(c) Polylog support-point sampling still has unbounded variance; REPLACED by spatial candidate-cell
sampling, variance ≤ M_r c_r.
(d) NO recursion — one active cover; coarse cells explicit; finer cells sampled; geometric sum Õ(√K).

### Numerical audit target (Pro's)
The round-3 dense-grid + satellites instance, with multiplicity 1 on every satellite fine cell and almost
all P-points in the dense core cells. At each r_j record M_j, c̃_j, Z_j∈{0,M_j}; empirical E[Z_j]=c̃_j,
Var(Z_j)=M_j c̃_j − c̃_j². The full estimator should stay accurate despite essentially never drawing a
satellite by uniform P-sampling.

### Updated confidence (Pro)
- empty-cell leader identity & variance: **0.99**
- active-cover & packing accounting: **0.98**
- scale-graph filtration interleaving: **0.97**
- Õ_η(√K) summation: **0.94**
- repaired support-MST lemma: **0.91**
- full unconditional Õ_ε(n^{1/3}) after insertion into round 2: **0.86**
Most important human audit point: the transition from interleaving (1) to the Riemann-sum estimate (11),
then the MU/α² accounting in (8).

[1] arXiv:2504.15292
