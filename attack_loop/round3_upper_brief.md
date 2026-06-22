# Round 3 (UPPER-bound line) — Brief to attacker (assemble the full sub-√n algorithm)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> Round 2's √n "variance barrier" was shown to be an artifact of UNIFORM sampling — importance
> sampling breaks it (proven on the hard instance). This brief asks you to turn that crack into a
> full algorithm. Read §3 (proven substrate) before designing; build on it, do not re-derive it.

---

## 1. The setting + target (frozen)

P ⊂ [Δ]² integer grid, |P|=n, Δ=O(n). Orthogonal range-**counting** oracle: query R → exact integer
|P∩R|. Want a randomized **(1±ε)** estimate of w(MST(P)), constant success prob, in **o(√n)** queries
— ideally **Õ(n^{1/3})** (which closes the Driemel et al. Ω(n^{1/3}) vs Õ(√n) gap from above).

w(MST) = (n − Δ) + **Σ_i λ_i c_i**, λ_i=(1+ε)^i, c_i = #connected components of the spanner keeping
edges of length ≤ λ_i, over Õ(1) scales. A spanner edge "∃ edge ≤ r between two regions?" costs
O(ε^{-2}) range-counting queries (source Lemma 24). **Task: estimate Σ_i λ_i c_i to ±ε·OPT in o(√n).**

---

## 2. Reframe Σ_i λ_i c_i as total component "persistence" (frozen, useful)

For a component that first merges into a larger one at scale λ*, its contribution to Σ_i λ_i c_i is
∫ over the scales it stays separate ≈ Θ(λ*) (it is counted in every c_i with λ_i < λ*). So
**Σ_i λ_i c_i = Σ_{components, all scales} (persistence length of that component)** — dominated by
"small, long-lived" components (a singleton that stays isolated until scale λ* contributes Θ(λ*)).
The algorithmic problem is to estimate this total persistence WITHOUT estimating any single c_i or
N_i to relative error.

---

## 3. PROVEN substrate (Rounds 1–2 + independent audits + exact-EMST numerics — use freely)

- **U-B1 (cell-sampling Ω(√n)).** Estimating, at a scale, a near-uniform non-empty cell OR N_i =
  #non-empty cells to O(1)-relative error costs Ω(√n) (paper §4, even 1-D). 🔴 Do NOT estimate any
  single c_i / N_i to relative error — that IS cell sampling.
- **U-P1 (MST is NOT √n-hard).** The cell-sampling hard instance is 1-D, where w(MST)=x_max−x_min is
  occupancy-invariant; so a (1±ε)-MST estimator cannot solve cell sampling. Only floor is Ω(n^{1/3}).
- **U-P2 (THE CRACK + the tile-or-blowup vise — verified numerically).**
  - The "uniform point estimator" X(p)=n·Σ_i λ_i/|comp_i(p)| has Var/E²=Θ(√n) on the islands instance
    (M=√n singletons at pairwise distance L=√n + bulk). **This is an artifact of UNIFORM sampling.**
  - **Importance sampling defeats it:** localized random width-λ probes estimate the **lonely-fraction**
    (cells with |P∩(λ-box)|=1, i.e. occupancy-1 sites) in **O(1/ε²·log Δ) = polylog** queries,
    n-independent (verified: flat ~200 probes, n=10³…10⁵, accuracy →1.0). No near-uniform cell sampling.
  - **The tile-or-blowup vise (why no √n hard instance survives):** a stratum of "lonely-at-scale-λ"
    sites needs disjoint empty λ-neighborhoods, total measure ≥ (#sites)·λ^d. To contribute a constant
    fraction to Σλc the sites are many/long-lived ⇒ EITHER they **tile** their active region (so a
    localized probe finds one with Θ(1/polylog) probability ⇒ probe-estimable in o(√n)) OR an adversary
    **scatters** them to hide each at 1/√n measure — but then their pairwise distances blow up, their
    MST contribution becomes ≫ OPT (a >100× signal, trivially distinguishable, NOT a constant-factor
    pair) AND a polylog coarse grid already sees them. **A constant-fraction low-mass stratum cannot be
    both hard-to-find and weight-significant.** (This is the algorithmic twin of the LB-side P1/P2 fact
    "a correlated Θ(w) gap is coarsely estimable.")
  - 🔑 Why U-B1 does NOT block this: U-B1 hides N only when the signal is **concentrated** in one
    1/√n-measure witness — but there MST's lonely term is **small**; MST's lonely term is **large** only
    when sites are **spread**, where the lonely-fraction is cheaply probe-estimable. The regimes are
    anti-correlated.

- **Dead routes (N*) — do NOT propose:** **U-N1** CRT with smaller BFS depth t (still needs cell
  sampling). **U-N2** uniform point-sampling + inverse-multiplicity reweight (Var=Θ(nM)=√n). **Euler
  totals**: c_i = V_i−E_i+Z_i but for a filled k×k block V=k², E=2k(k−1), Z=(k−1)² all cancel to c=1;
  estimating V_i,E_i separately to coarse accuracy gives error Θ(k²λ) ≫ true Θ(λ) — the cycle-rank /
  connectivity is the whole content, occupancy totals alone are insufficient.

---

## 4. Barriers (B*)
- **Ω(n^{1/3}) floor (Lemma 32).** Any claimed query count < n^{1/3} is WRONG. The known hard instance
  hides a **DENSE heavy gadget** (a block whose internal MST cost ≠ a strip's) in one of 16n^{1/3}
  coarse cells; each query hits ≤4 cells; hit-prob 1/(4n^{1/3}). This gadget is NOT an occupancy-1
  feature — the lonely-fraction primitive of U-P2 does **not** see it. Your algorithm must still detect
  this stratum, which is exactly why the floor is n^{1/3}.
- No per-scale relative-error N_i/c_i (= cell sampling, U-B1). Per-scale errors sum over Õ(1) scales;
  total ≤ ε·OPT. Honesty: if a stratum forces √n, name it precisely.

---

## 5. The open question (method-agnostic — assemble the algorithm)

> **Turn U-P2 into a complete algorithm: estimate Σ_i λ_i c_i (the total component persistence) to
> ±ε·OPT in o(√n) — ideally Õ(n^{1/3}) — range-counting queries, by STRATIFIED IMPORTANCE SAMPLING
> over component types (not uniform over points), using localized probes, never near-uniform cell
> sampling.**

The crux you must resolve (the one missing lemma + the dense stratum):
- **(a) Generalize the localized-probe primitive from "lonely singletons" to ALL component-persistence
  strata.** Stratify components by (mass × persistence-scale). For each high-value stratum, prove a
  **concentration/tiling lemma**: the components contributing the top fraction of Σλc at each scale
  occupy ≥ Ω(1/polylog) measure of an identifiable region (the tile-or-blowup vise of U-P2 suggests
  they cannot all hide), so a localized probe hits one with probability ≥ 1/polylog and a counting
  query reveals its local mass/persistence ⇒ bounded importance-sampling variance. Prove this lemma or
  find the precise stratum where it fails.
- **(b) The dense-block stratum (the n^{1/3} floor).** A hidden heavy gadget among 16n^{1/3} coarse
  cells is found by O(n^{1/3}) coarse range counts (it perturbs the count/MST of its cell). Integrate
  this with (a) so the TOTAL is o(√n) and respects the Ω(n^{1/3}) floor.
- **(c) (1±ε) and the query bound.** Assemble per-stratum estimates into a (1±ε) estimate of Σλc
  (the current localized-probe estimate is ~1.3×; tighten via proper occupied-cell normalization +
  variance bounds). State the exact query exponent achieved (Õ(n^{1/3}), or the best o(√n)).

Use any method (stratified/importance sampling, multi-resolution count summaries, the persistence
reframe of §2, geometric concentration, etc.). If you conclude a particular stratum genuinely forces
√n despite U-P2, prove it (a √n lower bound must evade the tile-or-blowup vise AND not contradict U-P1
— so it would be a major surprise; treat such a claim with suspicion and check it against the vise).

---

## 6. What we need back

1. **The algorithm** (pseudocode), per-stratum, with the **concentration/tiling lemma** stated and
   proved (or the precise failing stratum), the **query-count bound** (show o(√n), ideally Õ(n^{1/3})),
   and the **(1±ε)-correctness** (every stratum's error ≤ its ε·OPT share; success probability).
2. **The achievable query exponent.**
3. **Updated confidence %** that o(√n) (resp. Õ(n^{1/3})) is achievable.
4. **Verdict** (algorithm-complete / algorithm-modulo-stated-lemma / specific-stratum-obstruction / open).
5. *(Strongly encouraged)* numerics: implement your estimator over an exact range-counting oracle
   (scipy exact EMST in the repo), and show measured query count stays o(√n) while accuracy → (1±ε),
   across several n — including on BOTH hard instances (islands; and the dense-gadget Lemma-32 instance).

We will adversarially audit (looking for: a hidden per-scale relative-error N_i = secret cell sampling;
an unbounded-variance stratum; the dense-gadget instance silently ignored; an undercounted query bound;
a per-scale error exceeding its ε·OPT share; an Ω(n^{1/3})-floor violation). A precise
"stratum X forces √n because …" is as valuable as an algorithm.
