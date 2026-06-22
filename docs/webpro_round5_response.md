# Round 5 — GPT-5.5-Pro response (verbatim, human-relayed 2026-06-21) — CONSOLIDATED CLOSURE PROOF

> Pasted by the owner; LaTeX cleaned, all claims/eqs preserved (condensed where purely mechanical).
> Pro CONFIRMS the c_j fix, adds one further (N_j-exploration) correction, and gives the full
> self-contained proof for human verification. Citation [1]=arXiv:2504.15292 (Thm 30, Lemma 32, uniform
> sampling Lemma 1, WSPD Lemmas 23–24). Final numeric test: `attack_loop/webpro_verify_round5.py`;
> final audit: `docs/webpro_round5_auditFinal.md`.

---

**c_j fix CONFIRMED:** Var(Z_j)=M_j c_j − c_j² ≤ M_j c_j (exactly one occupied cell per component is a
leader); the occupied-cell count N_j is irrelevant to the NUMBER OF TRIALS. **Further correction:** the
expected cost of EXPLORING an occupied sampled cell still depends on N_j; so N_j stays, bounded
separately by N_j ≤ K — and the resulting sum is STILL Õ_η(√K).

## 1. Support-MST Lemma 3 (final)
Q = centers of the K nonempty h-cells; half-open cells. **Lemma 3:** ∀η∈(0,1/4), a randomized algorithm
outputs Ŵ_Q with |Ŵ_Q−W_Q| ≤ ηW_Q w.p. ≥2/3 using **Õ_η(√K + n/K)** range-counting queries to P
(Λ=log(nΔ/(hη)); explicit O(η^{-8}√K·Λ^{O(1)} + η^{-2}(n/K)Λ^{O(1)})). If K known to rel. error O(η),
the n/K term is unnecessary.
- **§1.1 Oracle ops on Q:** Q∩R≠∅ ⟺ P∩R≠∅ (one P-count); uniform point of P in O(log Δ); accept its
  h-cell w.p. 1/m(p) ⇒ uniform support cell, accept prob K/n; K estimable to rel-κ in O(κ^{-2}(n/K)log).
- **§1.2 Active cover:** subdivide to first level with b≥q=⌈√K⌉ nonempty δ-cells; q≤b<4q; found in
  Õ(√K) emptiness queries. **Packing: W_Q ≥ δ(b−4)/8 ≥ bδ/16** (4-coloring + w(MST(S))≤2W_Q ∀S⊆Q) (5).
- **§1.3 Scale graphs Γ_r:** a(r)=Θ(σr) (or h at the floor), σ=β/32; vertices=nonempty a-cells; degree
  O(σ^{-2}); each potential neighbor an aligned rectangle, 1 P-count to test.
- **§1.4 Interleaving:** c_Q(r^+) ≤ c_Γ(r) ≤ c_Q(r), r^+=(1+σ)r (12).
- **§1.5 ⚑ Correct component-count bound:** c_Q(t)−1 = #{MST edges >t} ≤ W_Q/t (13,14) ⇒ c_Γ(r) ≤
  1+W_Q/r; given G≥W_Q, **U(r)=1+G/r ≥ c_Γ(r)** (16). *This bounds the COMPONENT count, not N(r).*
- **§1.6 Empty-cell leader estimator:** sample X uniform from M candidate cells; if empty Z=0; else
  random-leader → Z=M iff X is its component's min-rank cell. **E[Z]=c (17), Var(Z)=Mc−c² ≤ Mc (18) —
  no N appears.** k=O((MU/α²)log(1/δ)) trials ⇒ additive α. **Exploration cost (N matters HERE):** a
  size-s component ⇒ E[examined] ≤ 1+H_{s-1}=O(log K); candidate occupied w.p. N/M ⇒ E[expansions over
  k trials] = O(k(N/M)log K) (21); use **N ≤ K** (22). Each expansion O(σ^{-2}) P-counts.
- **§1.7 Candidate cells:** fine (a≤δ): M(r)=b(δ/a)² ≤ C_M bδ²/(σ²r²) (24); uniform candidate = pick
  active block + a-subcell (offline), 1 P-count for occupancy. Coarse (a>δ): the ≤b distinct a-ancestors
  of B, computed exactly, NO oracle queries, NO recursion.
- **§1.8 Additive estimator given G≥W_Q:** r_0=max{h, βG/(32K)}; r_j=r_0(1+σ)^j; d_j=σr_j; T=O(σ^{-1}
  log(Δ/h)); α_j=βG/(32T σ r_j) (28); U_j=1+G/r_j (29); Ŵ(G)=(K−1)h + Σ d_j(ĉ_j−1) (30).
- **§1.9 ⚑ Correct query accounting (two parts):**
  - **Candidate-root (uses c_j via U_j):** M_jU_j/α_j² ≤ C(T²/β²)(bδ²/G² + bδ²/(Gr_j)); with G≥W_Q≥bδ/16:
    bδ²/G²=O(1/b), bδ²/(Gr_j)=O(δ/r_j); Σ_j 1/r_j=O(1/(σr_0)); δ/r_0=O(K/(βb)). **Σ_j k_j = Õ_β(K/b) =
    Õ_β(√K)** (36). Uses c_j, NOT N_j.
  - **Exploration (uses N_j≤K):** E[expansions at j] = Õ(N_jU_j/α_j²) ≤ C·K(T²σ²r_j²/(β²G²))(1+G/r_j)
    (38); fine ⇒ r_j ≤ 128δ/σ (39), so Σ_fine r_j=O(δ/σ²), Σ_fine r_j²=O(δ²/σ³); total Õ[KT²/β²
    (δ²/(σG²)+δ/G)]; with K δ/G=O(K/b)=O(√K) (42) and Kδ²/G²=O(K/b²)=O(1) (43) ⇒ **Õ_β(√K)** (44).
    Global √K cap + Markov ⇒ worst-case budget. ⇒ **one additive call = Õ_β(√K)** (45,46).
- **§1.10 Accuracy:** W_Q=∫(c_Q−1)dt; ∫_0^h=(K−1)h (48); omitted [h,r_0] ≤ K r_0 ≤ βG/32 (49); Riemann
  gap = Σ d_j(c_Q(r_j)−c_Q(r_{j+1})) ≤ σW_Q ≤ βG/32 (51); statistical Σ d_j α_j ≤ βG/32 (52) ⇒
  **|Ŵ(G)−W_Q| ≤ 3βG/32 < βG** (53).
- **§1.11 Remove the guess:** U_Q=(K−1)diam(Q); β_0=1/32; G=U_Q,U_Q/2,…; stop at first Ŵ(G)≥G/4 ⇒
  W_Q ≤ G_0 < 8W_Q (55); final call β=η/16. Approx K (κ=η/1000) perturbs only by 1+O(κ). ∎

## 2. Clipped death-time primitive
τ(v)=min{bottleneck-dist to root or lower-ranked}; multiset {τ(v)}={0}∪{MST edge weights} (56);
bottleneck-Dijkstra, O(log|V|) expected extractions. X_L=min{τ,L}: |V|E[X_L]=A_L(H) (57), X_L²≤LX_L ⇒
Var ≤ |V|L·w(MST(H))/s (58). On a (1+ρ)-spanner H_X: A_L(X) ≤ A_L(H_X) ≤ (1+ρ)A_L(X) (59), additive
error ≤ ρ·w(MST(X)) (60). WSPD impl via source Lemmas 23–24.

## 3–4. Support regularization + snapping (for P)
W=w(MST(P)), K_0=⌈n^{2/3}⌉, L=G/K_0. **Packing K_h ≤ 8W/h+4** (63). Choose grid so K=K_h ∈ [cK_0, C_ξ K_0]
(65), cost Õ_ξ(n/K_0)=Õ(n^{1/3}) (66). Snapping δ_s=√2 h: **c_P(t+δ_s) ≤ c_Q(t) ≤ c_P(t−δ_s)** (68);
B_L(X)=∫_L^∞(c_X−1)=Σ(|e|−L)_+ (69); **|B_L(Q)−B_L(P)| ≤ O(γξW)** (71). **W_Q ≤ C_W W** (72,73).

## 5–7. Assembly + the theorem
W=A_L(P)+B_L(P) (74); B_L(Q)=W_Q−A_L(Q) (75). Estimate: **A_L(P)** by clipped death-time on a (1+ρ)-
spanner of P, s_P=O(ξ^{-2}n^{1/3}) samples (76) ⇒ Õ_ξ(n^{1/3}) (77); **W_Q** by Lemma 3, Õ_ξ(n^{1/3})
(79); **A_L(Q)** by clipped death-time on Q, s_Q=O_ξ(1) support samples (each Õ(n/K)=Õ(n^{1/3})) (81,82).
**NO cross-threshold seed reuse anywhere.** Return **Ŵ(G)=Â_P + Ŵ_Q − Â_Q** (83); |Ŵ(G)−W| ≤ C_*ξG (85)
⇒ normalized |Ŵ(G)−W| ≤ ζG (86), one call Õ_ζ(n^{1/3}) (87). Geometric search (U=√2(n−1)Δ, W≥n−1 ⇒
O(log n) guesses), stop at first Ŵ(G)≥G/8 ⇒ W ≤ G_0 < 16W (90); final ζ=ε/32.
**FINAL THEOREM:** ∀ fixed ε, P⊆[Δ]² (|P|=n, Δ=O(n)): a randomized orthogonal range-counting algorithm
returns Ŵ with (1−ε)w(MST(P)) ≤ Ŵ ≤ (1+ε)w(MST(P)) w.constant prob using **Õ_ε(n^{1/3})** range-counting
queries. With the published Ω(n^{1/3}), this is optimal up to polylog + ε-factors.

## 8. Verification debt (Pro's own list)
Self-contained at the query-accounting level (candidate-root uses c_j; N_j only in exploration, N_j≤K
suffices; no distinct-support-count oracle; no seed-pool reuse; no nonrectangular query; coarse scales
explicit, no recursion). Standard-but-not-pseudocoded: **(1) [the one substantively important item] the
local WSPD bottleneck search for the clipped death-time primitive** (representative choice, redundant-pair
suppression, tie handling, global cap — source Lemmas 23–24 supply the machinery); (2) approximate-K
constants; (3) failure-probability bookkeeping (assign 1/(100T log n)-type budgets); (4) dyadic boundary
conventions.

## 9. Recommended final numerical audit (Pro's)
Support = fully-occupied √K×√K fine-grid carpet (so at floor scales N_j=Θ(K), c_j=1) + geometric sparse
satellite chains (constant fraction of W_Q). Record separately Σ_j M_jc_j/α_j² (candidate-root, should
follow the c_j-based Õ(√K)) and the actual #neighbor queries by occupied-root explorations (the separate
N_j-dependent behavior, should still sum to Õ(√K) per (38)–(44)). This tests the FINAL correction, not
already-settled recovery.

## Confidence (Pro)
- empty-cell leader E[Z] & M_jc_j variance: **0.995**
- corrected candidate-trial accounting: **0.98**
- separate N_j-based exploration accounting: **0.96**
- scale interleaving + Riemann reconstruction: **0.98**
- complete support-MST Lemma 3: **0.95**
- snapping/heavy-tail assembly: **0.96**
- local WSPD impl of clipped death-time sampling: **0.89** ← the one place for a human expert to attack
- **full unconditional Õ_ε(n^{1/3}) theorem: 0.91**

[1] arXiv:2504.15292
