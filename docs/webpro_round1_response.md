# Round 1 — GPT-5.5-Pro response (verbatim, human-relayed 2026-06-21)

> Pasted by the owner from the GPT-5.5-Pro web session. Minor LaTeX-delimiter transmission noise
> cleaned for readability; ALL mathematical content / claims preserved exactly. Citations: [1] =
> arXiv:2504.15292 (the source paper); [2] = a 2025 Georgia Tech thesis (a related vertex→MST-edge
> mapping). This is the response audited in `webpro_round1_audit.md` and numerically checked in
> `attack_loop/webpro_verify_*.py`.

---

**Verdict (Pro):** No valid worst-case closure of the Ω(n^{1/3}) vs Õ(√n) gap. One rare long bridge
remains effective at ruining the estimator below. But a rigorous PARTIAL result:
1. The implementation obstruction in our §C (U-N4) is **not real**.
2. One can locally sample an MST edge weight using only **polylogarithmically many expected range
   queries**.
3. This gives a new **instance-sensitive** bound that is Õ(n^{1/3}) whenever the MST weight is not
   concentrated on a few long edges.
4. It reduces the remaining worst-case problem precisely to **estimating the heavy tail of the
   MST-edge distribution**.

## 1. A cheap unbiased estimator of 1/|C(p)|
Locally navigable graph G, threshold λ; C_λ(p) = component of p in G_{≤λ}. Assign every vertex an
independent continuous random rank π(v). From p, explore C_λ(p) in any deterministic BFS/DFS order
independent of the ranks. **Stop as soon as a vertex u with π(u) < π(p) is encountered → output
I(p)=0.** If the component is exhausted first → output I(p)=1.

If |C_λ(p)|=s, then Pr[I(p)=1 | p] = 1/s, so I(p) is an **unbiased Bernoulli estimator of 1/|C_λ(p)|**.

It is cheap: writing the exploration order p=v_1,…,v_s, vertex v_j is inspected only if p has minimum
rank among v_1,…,v_{j-1}, probability 1/(j-1). So E[#vertices inspected | s] ≤ 1 + Σ_{j=2}^s 1/(j-1) =
1 + H_{s-1} = **O(log s)**. (The rare event where p is the minimum and the whole component is explored
has probability 1/s, exactly compensating its cost.)

For uniform p∈P: E[I(p)] = Σ_C (|C|/n)(1/|C|) = c(λ)/n. So ĉ(λ) = (n/k) Σ_{j=1}^k I(p_j) is unbiased
with **Var[ĉ(λ)] ≤ n·c(λ)/k**; k = O(n/(ε²c(λ))) trials give a relative estimate of c(λ).

**Direct implementation on the paper's contracted cell graph** (size-bias corrected): let z = contracted
cell containing the sampled point, m(z)=|P∩z|. Assign random ranks to nonempty cells; explore the cell
component of z, stop on a lower-ranked cell; return Y = 1[z is min-ranked cell in its component]/m(z).
For a cell component C: Σ_{z∈C} (m(z)/n)(1/m(z))(1/|C|) = 1/n. So E[Y]=c(λ)/n, Var(Y) ≤ c(λ)/n. The
paper's Lemma 24 gives constant-degree local navigation using O_ε(1) range queries per visited cell ⇒
each trial uses **Õ_ε(1) expected queries**. The paper's Ω(√n) lower bound for uniformly sampling a
nonempty cell remains correct, but **that primitive is simply unnecessary for this estimator**. So our
§C categorical obstruction is FALSE: one can obtain an unbiased 1/|C_λ(p)| sample without exploring the
whole component.

## 2. A stronger identity: local sampling of MST edge weights
Connected weighted graph G=(V,E,w); fix a root r; independent random ranks to V\{r}. Bottleneck
distance d_∞(u,v) = min over paths γ:u⤳v of max_{e∈γ} w(e). For v≠r:
  **τ(v) = min{ d_∞(v,u) : u=r or π(u)<π(v) }**, τ(r)=0.

### Lemma 1 (exact multiset identity)
For every fixed assignment of distinct ranks:
  **{τ(v) : v∈V} = {0} ∪ {w(e) : e∈T}** as multisets (T = any MST of G).

*Proof.* G_{≤t} has c(t) components; C_t(v) = component of v. By definition τ(v) > t exactly when (1)
C_t(v) does not contain r, and (2) v is the minimum-ranked vertex of C_t(v). There is exactly one such
vertex in every non-root component, so |{v : τ(v)>t}| = c(t)-1. Kruskal: |{e∈T : w(e)>t}| = c(t)-1.
The two finite multisets have identical survival-count functions for every t ⇒ equal. ∎

### Lemma 2 (τ(v) is locally computable)
Run bottleneck-Dijkstra from v with key D(x)=min over paths v⤳x of max edge; stop when the first
lower-ranked vertex (or r) is extracted; its key is exactly τ(v). The extraction order x_1,x_2,… is
graph/tie-break determined, not rank-determined, so x_j is extracted before stopping only when v has
min rank among the preceding j-1 vertices ⇒ E[#extracted] ≤ 1+H_{n-1} = O(log n). Thus a uniform random
vertex + this search returns a **uniformly random MST-edge weight** (plus one extra zero) using
O(log n) expected local vertex expansions.

(A related 2025 thesis [2] independently gives a different general-graph vertex→MST-edge mapping via a
modified Prim search in expected O(d log n) time, so no priority claim for the bare edge-mapping; the
rank/bottleneck formulation is convenient for the range-oracle setting.)

## 3. Implementing the search with range counts
Standard quadtree WSPD with separation δ=Θ(ε). For each WSPD pair, join the lexicographically least
representatives of its two cells with the actual Euclidean length → graph H. WSPD analysis:
d_H(x,y) ≤ (1+O(δ))|x-y|_2, so with W=w(MST(P)), W_H=w(MST(H)): **W ≤ W_H ≤ (1+O(δ))W**.

Polylog-range-query operations: sample a uniform point of P (recursive range-count splitting); find the
lex-least point in a nonempty quadtree cell; enumerate WSPD edges incident to a revealed point. For the
last: each dyadic ancestor cell a∋p has O(δ^{-2}) candidate partner cells per level (partner side within
factor 2, center at distance Θ(r(a)/δ)); emptiness/membership/representatives via polylog range queries
(paper's bounded-pair + local-membership). So one bottleneck-Dijkstra expansion uses O(δ^{-2} log²Δ)
range queries, and one τ(v) sample uses **Õ_ε(1)** expected queries. Expected→hard cap: abort after a
large constant × k log n total expansions; Markov adds only constant failure prob.

## 4. Instance-sensitive upper bound
T_P = Euclidean MST, edge lengths ℓ_e; **Γ(P) = n·Σ_{e∈T_P} ℓ_e² / W²**. Cauchy–Schwarz: 1 ≲ Γ(P) ≤ n.

### Theorem
For every integer k there is a randomized range-counting algorithm using **Õ_ε(k)** queries returning
Ŵ with Pr[|Ŵ−W| > εW] ≤ O(Γ(P)/(kε²)) + O(1/10) (after choosing WSPD stretch ≪ ε). In particular,
under a promise Γ(P) ≤ G, **Õ_ε(G)** range queries suffice.

*Proof.* T_H = MST of H, weights w_f. Draw k uniform points, compute death times τ_1,…,τ_k; set
Ŵ_H = (n/k)Σ τ_j. By the multiset identity, E[τ_j]=W_H/n, E[τ_j²]=(1/n)Σ_{f∈T_H} w_f². So Var(Ŵ_H) ≤
(n/k)Σ w_f². Compare squared weights: for each e∈T_P take spanner path Q_e with Σ_{f∈Q_e} w_f ≤
(1+O(δ))ℓ_e; the union of all Q_e is connected ⇒ contains a spanning tree T'; Σ_{f∈T'} w_f² ≤ Σ_e
Σ_{f∈Q_e} w_f² ≤ Σ_e (Σ_{f∈Q_e} w_f)² ≤ (1+O(δ))² Σ_e ℓ_e². Kruskal MST minimizes sum of squared
weights among spanning trees (order preserved) ⇒ Σ_{f∈T_H} w_f² ≤ (1+O(δ))² Σ_e ℓ_e². Since W_H ≥ W:
n Σ_{T_H} w_f² / W_H² ≤ (1+O(δ))² Γ(P). Chebyshev gives the bound; small δ + small sampling error
converts the Ŵ_H estimate into a (1±ε)-estimate of W. ∎

### Corollaries
If ℓ_max ≤ W/n^{2/3}, then Σ ℓ_e² ≤ ℓ_max Σ ℓ_e ≤ W²/n^{2/3} ⇒ Γ(P) ≤ n^{1/3}, so this class admits
**Õ_ε(n^{1/3})** queries. More generally, effective #MST-edges N_eff = W²/Σ ℓ_e²; the query bound is
**Õ_ε(n/N_eff)**, which is o(√n) whenever N_eff = ω(√n).

## 5. The precise remaining obstruction (heavy tail, NOT connectivity)
For threshold L use X_L=min{τ,L}. Then n·E[X_L] = Σ_{e∈T_H} min{w_e,L} =: A_L. And X_L² ≤ L·X_L, so
Var[(n/k)Σ X_{L,j}] ≤ n L W_H / k. With a constant-factor guess of W_H, take L=W_H/n^{2/3}: A_L
estimable to additive εW_H in **Õ_ε(n^{1/3})** queries. What remains is **B_L = Σ_{e∈T_H} (w_e−L)_+**,
and |{e : w_e>L}| ≤ W_H/L = n^{2/3}. So a sufficient lemma to close the upper bound:

> **Heavy-tail lemma.** Estimate the total excess weight of at most n^{2/3} long MST edges above a
> supplied threshold L, to additive εW, using Õ(n^{1/3}) range queries.

The death-time method handles everything below L. A successful algorithm must exploit geometric
information about the rare long edges beyond uniform point or component-leader sampling.

### Why the present estimator fails worst-case
Two roughly square unit-grid clusters, each n/2 points, separated horizontally by gap G=Θ(n) (domain
side still O(n)). MST = (n−2) unit edges + 1 edge of length Θ(n). So W=Θ(n), Σℓ_e²=Θ(n²), Γ(P)=Θ(n).
The death-time multiset contains ONE heavy value among n entries ⇒ any algorithm seeing only independent
death-time samples needs Ω(n) samples to observe it. The known Õ(√n) algorithm does better because it
also uses **spatial range information** — exactly the missing ingredient.

## 6. Assessment of our gadget barrier (§B.1 / P1)
The §B.1 calculation is correct **under explicit hypotheses**: m independently switchable regions; each
p points in a side-s square; one region changes MST weight by ≤ O(s√p); null-instance MST weight
Ω(ms); each query gets gadget-dependent info from only O(1) regions. If k regions switched, a constant
relative gap needs k·s√p = Ω(ms) ⇒ k = Ω(m/√p); hitting LB ≤ O(m/k) ≤ O(√p), also ≤ m; with n=mp,
max_{mp=n} min{m,√p} = n^{1/3}. So that template genuinely caps at n^{1/3}. **Caveat:** the baseline
Ω(ms) and the O(1)-regions-per-query condition are SUBSTANTIVE assumptions, not consequences of
"disjoint cells" alone — adjacent regions, cheap fixed skeletons, or globally correlated gadgets can
violate them. So it is a barrier for that localized-hitting template, NOT a universal obstruction to an
Ω(√n) lower bound.

## 7. Numerical checks worth running
1. **Exact multiset identity:** build EMST (or WSPD graph), random ranks, compute every τ(v); check
   sort{τ(v):v≠r} == sorted MST edge weights (with multiplicities).
2. **Chain-component exploration:** on a size-s component, average #inspected vertices → 1+H_{s-1}, not s.
3. **Rare bridge:** two dense grids separated by G=Θ(n); death-time multiset should contain exactly one
   Θ(G) value (demonstrating the tail obstruction).
4. **WSPD square-weight comparison:** Σ_{f∈T_H} w_f² ≤ (1+δ)² Σ_{e∈T_P} ℓ_e² (catches representative/
   tie-handling mistakes).

## Confidence (Pro)
- Random-leader component estimator: **0.99**
- Death-time / MST multiset identity: **0.99**
- Variance & instance-sensitive theorem: **0.95**
- Local WSPD incident-edge enumeration in the exact range-query model: **0.85** (only the redundant-pair
  convention needs tedious auditing; a compressed WSPD should make it routine).
- Worst-case o(√n) upper bound or ω(n^{1/3}) lower bound: **not claimed.** The unresolved object is the
  rare-long-edge tail B_L, not component-size estimation.

[1] https://arxiv.org/pdf/2504.15292
[2] https://repository.gatech.edu/entities/publication/b78483d2-d8fb-4054-913b-24e3d074cdce
