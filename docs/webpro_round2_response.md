# Round 2 — GPT-5.5-Pro response (verbatim, human-relayed 2026-06-21) — CLAIMED CLOSURE

> Pasted by the owner from the GPT-5.5-Pro web session. LaTeX-delimiter transmission noise cleaned for
> readability; ALL mathematical content/claims preserved. **Pro claims to CLOSE the gap from above:
> unconditional Õ_ε(n^{1/3}).** Citations: [1] = arXiv:2504.15292 (source); [2] = Czumaj–Ergün–Fortnow–
> Magen–Newman–Rubinfeld–Sohler (Princeton CS bib). Numeric checks: `attack_loop/webpro_verify_round2.py`;
> 3 independent audits: `docs/webpro_round2_audit{A,B,C}.md`.

---

**Claimed main theorem.** For P⊆[Δ]², |P|=n, Δ=O(n), fixed ε: a randomized algorithm returns Ŵ with
(1−ε)w(MST(P)) ≤ Ŵ ≤ (1+ε)w(MST(P)) with constant prob, using **Õ_ε(n^{1/3})** orthogonal range-counting
queries. ⇒ the Ω(n^{1/3}) lower bound is tight up to polylog. The missing trick: **regularize the spatial
support to K=Θ_ε(n^{2/3}) occupied cells, then run a spread-independent Õ(√K) geometric MST estimator on
that support; uniform support samples cost n/K=n^{1/3} but only polylog are needed because the SAME CRT
seed pool is reused at every threshold.**

## 1. Support regularization
W=w(MST(P)), K_0=⌈n^{2/3}⌉. Grid G_h of side-h cells; Q_h = {center z_C : C nonempty}, K_h=|Q_h|.

**Lemma 1 (packing): K_h ≤ 8W/h + 4.** Proof: pick one p_C∈P∩C per nonempty cell; 4-color cells by index
parities; same-color chosen points are pairwise ≥ h apart, so a color class of s points has MST ≥ h(s−1);
for any S⊆P, w(MST(S)) ≤ 2W (minimal subtree of MST(P) spanning S, double + shortcut); so h(s−1) ≤ 2W ⇒
s ≤ 2W/h+1; sum over 4 colors. ∎

**Finding a grid with K_h=Θ_ε(K_0):** given guess G≥W, set L=G/K_0; take largest dyadic h_0 ≤ αεL (α
small const); Lemma 1 ⇒ K_{h_0}=O_ε(K_0); halve h until K_h~K_0 (K_{h/2}≤4K_h) ⇒ at first crossing
K_h∈[cK_0, C_ε K_0]. **Estimating K_h:** sample p∈P uniform, query m_h(p)=|P∩C_h(p)|, return Bernoulli
Z_h=1 w.p. 1/m_h(p); Pr[Z_h=1]=K_h/n. So O_ε((n/K_0)log n) trials distinguish K_h vs cK_0; over O(log Δ)
levels still Õ_ε(n/K_0)=Õ_ε(n^{1/3}). Another O_ε((n/K_0)log n) trials give a (1±η)-estimate K̂.

## 2. Oracle access to the support Q_h
**Range emptiness:** for axis-aligned R in center coords, the fine cells whose centers ∈ R form a
contiguous grid range R̃; Q_h∩R≠∅ ⟺ P∩R̃≠∅ — one range-counting query. A support point found by binary
search over fine-cell indices, O(log Δ) queries. **Uniform support sampling:** draw p∈P uniform, query
m_h(p), accept its cell w.p. 1/m_h(p); each occupied cell accepted w.p. exactly 1/n, conditional return
uniform in Q_h; acceptance prob K_h/n ⇒ one uniform support point costs Õ(n/K_h)=Õ_ε(n^{1/3}). (Does NOT
contradict the source's Ω(√n) cell-sampling LB: we fix the grid so support size is Θ(n^{2/3}) and reuse
the same sampled support cells at all thresholds; never invoke their arbitrary-grid primitive.)

## 3. Snapping preserves the heavy tail
Map each p to its h-cell center; each point moves ≤ r=(√2/2)h; δ=2r=√2 h.
**Lemma 2 (filtration interleaving): for t≥δ, c_P(t+δ) ≤ c_Q(t) ≤ c_P(t−δ).** Proof: a t-edge in P maps
to a (t+δ)-edge of centers ⇒ c_Q(t+δ)≤c_P(t); centers ≤ t apart ⇒ representatives ≤ t+δ apart, and same-
center points are within δ ⇒ c_P(t+δ)≤c_Q(t). ∎
With B_L(X)=∫_L^∞(c_X(t)−1)dt: B_{L+δ}(P) ≤ B_L(Q) ≤ B_{L−δ}(P). Since c_P(t)−1=|{e∈MST:w_e>t}|≤W/t:
|B_L(Q)−B_L(P)| ≤ ∫_{L−δ}^{L+δ} W/t dt ≤ (2δ/(L−δ))W ≤ **O(αεW)** (h≤αεL). (Handles the serpent/filament:
an L-connected filament occupying many cells cannot make false long edges except in the δ-window.)
**W_Q=O(W):** contract equal cells in MST(P), spanning tree of the quotient, map edges to centers (+δ
each): W_Q ≤ W + δ(K_h−1); δK_h ≤ √2 h(8W/h+4)=O(W+h); at the level K_h=Ω(K_0), h=O(W/K_0) ⇒ **W_Q=O(W).**

## 4. A sample-light Õ(√K) estimator on the support
**Lemma 3 (sparse-support MST estimator).** For Q = centers of K occupied cells of a regular grid over P,
there is a randomized algorithm estimating w(MST(Q)) to (1±η) using **Õ_η(√K + n/K)** range-counting
queries to P. Proof: Czumaj et al.'s spread-independent estimator [2] has (1) adaptive subdivision →
O_η(√K) active blocks grouped into connected block-components; (2) MST inside block-components via the CRT
bounded-degree-graph estimator; (3) joining cost on a sparse graph of active-block centers — stages 1,3
use Õ_η(√K) range-emptiness queries, the graph routine samples O_η(1) uniform vertices per threshold +
local traversals. **Replace their directed Yao graph (cone-NN queries) by a component-restricted (1+ρ)-WSPD
spanner H_D of Q∩D** (ρ≪η), truncated at the internal cutoff; Q∩D connected below the cutoff ⇒ truncated
spanner connected after ×(1+ρ), w(MST(Q∩D)) ≤ w(MST(H_D)) ≤ (1+ρ)w(MST(Q∩D)). WSPD has polylog max degree;
representatives/incident pairs found locally with polylog range queries (source Lemmas 21–24). The WSPD is
built per block-component; component-restricted emptiness: above the active-block level offline from the
active-block list, below it one range-count to P ⇒ each adjacency op Õ_ρ(1). CRT estimator applies to
H=⊔_D H_D (polylog degree); connector unchanged.
**Reusing the vertex seeds:** at T thresholds, naive fresh support sample per threshold costs √K·(n/K)=
n^{2/3} (fatal). Instead draw ONE pool q_1,…,q_s ~ Unif(Q), s=O_η(log T), reuse at every threshold with
independent traversal randomness per (q_j,t); for any fixed threshold the samples are i.i.d. uniform ⇒
original concentration applies; ×O(log T) pool + medians ⇒ simultaneous correctness at all thresholds by
union bound (cross-threshold independence unnecessary). So expensive uniform-support calls = Õ_η(1).
⇒ active-block/WSPD/traversal = Õ_η(√K); shared seed pool = Õ_η(n/K); total **Õ_η(√K+n/K)**. (K̂=(1±η)K
changes only normalizers.) ∎ For K=Θ_ε(n^{2/3}): √K=n/K=Θ_ε(n^{1/3}) ⇒ Lemma 3 = Õ_ε(n^{1/3}).

## 5. Estimating the clipped support weight A_L(Q)
H_Q = locally-accessible (1+ρ)-WSPD spanner of Q (actual lengths). c_Q(t)≤c_{H_Q}(t)≤c_Q(t/(1+ρ)) ⇒
A_L(Q) ≤ A_L(H_Q) ≤ (1+ρ)A_L(Q), so |A_L(H_Q)−A_L(Q)| ≤ ρW_Q. Round-1 death-time sampler on H_Q: uniform
q∈Q, τ(q) rank-death time, X(q)=min{τ(q),L}; multiset identity ⇒ E[X]=A_L(H_Q)/K; X²≤LX ⇒ Var[(K/s)ΣX]
≤ KL·W_{H_Q}/s. With K=O_ε(K_0), L=G/K_0, W_{H_Q}=O(W)≤O(G): KLW_{H_Q}/G² = O_ε(1) ⇒ O_ε(η^{-2}) support
samples for additive ηG; total Õ_ε(n/K)=Õ_ε(n^{1/3}).

## 6. The heavy-tail estimator
Assume L=Θ(W/K_0). Support grid h≤αεL, K=Θ_ε(K_0). Compute Ŵ_Q≈w(MST(Q)) (Lemma 3) and Â_Q≈A_L(Q)
(clipped death-time). Return **B̂_L = Ŵ_Q − Â_Q** (since B_L(Q)=W_Q−A_L(Q)). Errors: |Ŵ_Q−W_Q|+|Â_Q−A_L(Q)|
≤ O(ηW) (W_Q=O(W)); snapping ≤ O(αεW); choose η,α,ρ=Θ(ε) small ⇒ |B̂_L−B_L(P)| ≤ εW. Query count
Õ_ε(n/K_0 + √K + n/K) = **Õ_ε(n^{1/3})**. Proves the heavy-tail lemma in its operative regime.

## 7. Obtaining W and L without prior knowledge
**Lemma 4 (upper-guess estimator).** Given any G≥W, produce Ŵ_G with |Ŵ_G−W|≤ηG, Õ_η(n^{1/3}) queries.
Construction: L=G/K_0; estimate the original bulk A_L(P) via round-1 clipped death-time (Var≤nLW/s_P;
s_P=Θ(n/(η²K_0)) ⇒ Var≤O(η²G²)); build support Q at resolution ≤αηL, estimate its tail; return Ŵ_G =
Â_L(P)+Ŵ_Q−Â_L(Q). Since W=A_L(P)+B_L(P) and support tail differs from B_L(P) by O(ηW), errors sum O(ηG).
**Geometric search:** U=√2(n−1)Δ ≥ W; run upper-guess with accuracy 1/64 for G=U,U/2,U/4,…; stop at the
first G with Ŵ_G ≥ G/16 (boost so all O(log n) calls simultaneously correct). If G≥32W: Ŵ_G ≤ W+G/64 ≤
G/32+G/64 < G/16 (continue). If G∈[W,2W): Ŵ_G ≥ W−G/64 > G/16 (stop before testing below W). ⇒ W ≤ G_0 <
32W; O(log n) guesses (W≥n−1 for distinct integer points, Δ=O(n)). Final run with G_0, accuracy εG_0/64
⇒ additive ≤ εW. **Unconditional Õ_ε(n^{1/3}).**

## 8. Where the √n bottleneck disappeared
Two √-effects: (1) the spatial algorithm on N-point support costs Õ(√N); (2) uniform vertices of an
implicit support may be expensive. Regularizing to K=n^{2/3} balances √K=n/K=n^{1/3}. The danger was that
the spatial estimator might need √K INDEPENDENT support samples ⇒ √K·(n/K)=n^{2/3}. It does not: the CRT
estimator does Õ(√K) local explorations over all thresholds, but all thresholds share ONE polylog pool of
uniform support vertices. **That seed-reuse is the accounting detail that makes the exponent work.**

## 9. Numerical tests suggested
Adversarial instance: one long serpentine L-connected chain over Θ(n^{2/3}) fine cells; dense islands at
separations L+ξ, 2L, 4L,…; geometrically unequal cell occupancies (1 .. max). For each h test
B_{L+√2h}(P) ≤ B_L(Q_h) ≤ B_{L−√2h}(P) and K_h ≤ 8W/h+4. Serpent checks no false tail weight from intra-
component spread; islands check rare long bridges; unequal occupancies check the rejection sampler is
genuinely uniform over occupied cells (not size-biased). Also: run the CRT estimators at all thresholds
with (a) fresh seeds per threshold vs (b) one shared pool — marginals + simultaneous-success should agree
up to log amplification.

## Confidence (Pro)
- support packing & grid selection: **0.98**
- snapping/interleaving bound for B_L: **0.99**
- clipped death-time variance: **0.98**
- reuse of one CRT seed pool across all thresholds: **0.95**
- componentwise replacement of Czumaj's Yao graph by the locally-enumerable WSPD graph: **0.84**
- complete unconditional Õ_ε(n^{1/3}) theorem: **0.86**
Insist on line-by-line audit of **Lemma 3** (the component-restricted WSPD inside Czumaj's active-block
decomposition) — no apparent exponent leak (above active-block level all subset info offline; below it
each query in one known block), the rest looks like bookkeeping.

[1] https://arxiv.org/pdf/2504.15292
[2] https://www.cs.princeton.edu/courses/archive/spring04/cos598B/bib/Czumaj-EFMNRS.pdf
