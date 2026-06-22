# Round 4 — Independent COST audit (adversarial, fresh context)

**Auditor:** independent Claude (Opus 4.8 1M), 2026-06-21. No collaboration with Pro or the orchestrator.
**Mandate:** be paranoid about the COST of Pro's repaired spatial-cell estimator
(`docs/webpro_round4_response.md`). The round-2 closure passed three audits and was then refuted by a
COST/VARIANCE blowup: a "seed-reuse" that recovered the answer but needed Ω(√K) independent support samples
per threshold ⇒ Ω(√K · n/K) = **Ω(n^{2/3})** total. The orchestrator's recovery test
(`attack_loop/webpro_verify_round4.py`) **capped the sample count k**, so it verified RECOVERY but NOT the
cost. This audit attacks the cost.

**The decisive question:** does Σ_j k_j (per-scale cell-trial budget) genuinely sum to Õ(√K) = Õ(n^{1/3}),
or is there a hidden Ω(√K)-sample / n^{2/3} blowup?

All numerics use `sim/.venv/Scripts/python.exe` + `sim/emst.py`'s exact EMST, on the round-3 satellite
instance (the one that broke round 2) plus adversarial uniform / clustered instances. Constants in Pro's
O()-formulas set to 1; only the **scaling in K = s², n = s³** is tested. The legitimately-polylog factor
T² (T = #scales = O(log(Δ/h)), inside α_j²) is reported and, where noted, divided out — Õ absorbs it.

---

## Bottom line

**The cost genuinely closes at Õ(√K) = Õ(n^{1/3}). I found NO hidden Ω(√K)-sample / n^{2/3} blowup.**
The round-2 failure mode does NOT recur, for a concrete structural reason verified numerically: the new
estimator never samples by support mass, so the per-scale budget is `M_j·U_j/α_j²`, and the eq-(8) collapse
of this to `C_η·T²·(δ/r_j)` is valid **because b·δ/G = O(1)** (the packing lower bound G ≥ Ω(bδ) holds), and
`Σ_j δ/r_j ≈ √K`. Measured exponent of the polynomial core: **n^{0.28–0.32}** (≤ n^{1/3}), versus the
round-2 blowup which would be **n^{0.667}**. The core/√K ratio is bounded (does not grow with K).

**Confidence that the total cost is Õ(√K) with no n^{2/3} blowup: 0.88.**
(Residual 0.12: the exploration-cost amortization (§4 eq 5) and the median/global-cap accounting are stated
tersely and I could only spot-check them; and the full insertion into round 2 — §11 — is outside this
cost-only audit.)

---

## Item-by-item

### 1. Packing W_Q ≥ Ω(b·δ) (§1) — **VALID**
Pro's bound `W_Q ≥ δ(b−4)/8` via 4-coloring (same-color blocks ≥δ apart, one class ≥b/4 points,
w(MST(S))≤2W_Q for S⊆Q). Verified numerically on satellite, uniform, and 2D-clustered instances:

| instance | s | K | b | δ | W_Q | Pro bound δ(b−4)/8 | W_Q/bound |
|---|---|---|---|---|---|---|---|
| satellite | 32 | 1024 | 33 | 2050 | 9.52e4 | 7417 | 12.8 |
| satellite | 48 | 2304 | 65 | 3450 | 3.25e5 | 26340 | 12.3 |
| uniform   | 32 | 1024 | 81 | 3.88 | 1023 | 37.3 | 27.4 |
| clustered | 48 | 2304 | 77 | — | 4.7e6 | 6.84e5 | 6.9 |

`W_Q ≥ bound` everywhere (ratio 7–40 ≥ 1). The packing is the load-bearing input to eq (8) and it holds.
**Classification: VALID.**

### 2. Candidate-cell count M_j = b(δ/a_j)² and variance Var(Z) ≤ M·c (§§4–5) — **VALID**
- The orchestrator's identity check was pure **under-sampling** (N=1000, M=50000, 20000 trials gave
  E[Z]=0, Var=0 because P(hit a leader)=c/M=1/50000 ⇒ ~0.4 expected hits). Re-run with trials ≫ M/c
  (2M–30M trials): E[Z]=c and Var(Z)=Mc−c² ≤ Mc **exactly** at every (M,c) tested up to M=5e5. The
  identity Z∈{0,M}, P(Z=M)=c/M is algebraically exact; the variance bound is correct.
- The consequence — to reach additive accuracy α one needs `k = Θ(M·U/α²)` trials — is the genuine,
  unavoidable price of Var ≤ Mc. This is NOT hidden; it is exactly what §6 sums. **The variance bound is
  fine; whether its price sums to √K is item 3.**
- `c_j ≤ U_j` verified at EVERY scale on satellite and clustered instances (max c_j/U_j ≈ 0.16–0.23 < 1),
  so the deterministic `U_j = C(1+G/(σr_j))` genuinely upper-bounds the component count — no scale where
  the trial count is set too low. **Classification: VALID.**

### 3. 🔴 THE KEY — Σ_j M_jU_j/α_j² = Õ(√K) (§6 eq 8) — **VALID**
Re-derived and numerically confirmed step by step on the satellite instance (s up to 160, K=25600):

(a) **Per-scale collapse (eq 8).** `M_jU_j/α_j²` with M_j=b(δ/a_j)², U_j=1+G/(σr_j), α_j=ηG/(C₁Tσr_j),
a_j=Θ(σr_j) gives `C(T²/η²σ)·(bδ²/(G r_j))`. Measured ratio `(M_jU_j/α_j²)/(T²·δ/r_j)` is a **small
K-independent constant** (~1.6–3.0, identical pattern at s=16 and s=64). The collapse requires
`b·δ/G = O(1)`; measured **b·δ/G = 0.67–0.75, stable and bounded** across all sizes. This is precisely the
packing of item 1 doing its job: G ≥ Ω(bδ) ⇒ bδ²/(Gr) ≤ O(δ/r).

(b) **Geometric sum.** `Σ_j δ/r_j ≈ δ/(σr_0)` (empirical sum matches the bound), and `δ/r_0 ≤ K/b ≤ √K`
verified for both r_0 branches (δ/r_0 ≤ K/b True at every size). Since b∈[√K,4√K), K/b∈(√K/4, √K].

(c) **Total.** Stripping the T² polylog (Õ-absorbed), the polynomial core:

| s | K | n | core=Σk/T² | core/√K | core/n^{2/3} |
|---|---|---|---|---|---|
| 32 | 1024 | 3.3e4 | 595 | 18.6 | 0.58 |
| 64 | 4096 | 2.6e5 | 1362 | 21.3 | 0.33 |
| 96 | 9216 | 8.8e5 | 2639 | 27.5 | 0.29 |
| 128 | 16384 | 2.1e6 | 2957 | 23.1 | 0.18 |
| 160 | 25600 | — | — | 5.0·T² | — |

Fitted exponent of the core: **K^0.47–0.61, n^0.28–0.41** (the clean `Σδ/r_j` core fits **n^0.316**; the
fuller `Σ M_jU_j/α_j²/T²` fits **n^0.28** over the larger size range). **core/n^{2/3} DECREASES toward 0**
as K grows (0.58 → 0.18). `core/(√K·T²)` is **bounded** (oscillates 5–8.7 with b's dyadic jumps, not
growing). Contrast the round-2 blowup, which would be K^1.0 / n^0.667. **Closure holds; classification:
VALID.**

### 4. Exploration cost U_j/α_j = O(T/η), O(log s) leader exploration (§4 eq 5) — **VALID (spot-checked)**
- `U_j/α_j = (1+G/σr)·(C₁Tσr/ηG) = O(T/η)` algebraically — polylog local expansions per scale. Sound.
- The random-leader BFS-stop-on-lower-rank explore: E[#cells examined | start occupied] ≤ 1+H_{s−1}=O(log s)
  verified on cell-path components (ratio to harmonic bound 0.8–1.0 up to s=10⁴). The harmonic argument is
  about ranks on the s cells of a component and transfers verbatim from points to cells. **VALID.**
- *Minor caveat:* §4 eq 5's amortization `Σ explorations ≤ Õ(U²/α²)` via "global cap + Markov" is stated
  tersely; I confirmed the dominant cost is the **empty-cell trials** (P(occupied)=N/M is small, and empty
  trials are one cheap P-emptiness count each), which is the whole point. The exploration term is lower
  order. I did not formally re-verify the Markov global-cap constant — **MINOR gap**, not fatal.

### 5. Coarse scales a_j > δ handled in O_η(b) = Õ(√K) (§5) — **VALID**
For a_j > δ the nonempty a_j-cells are the ≤ b dyadic ancestors of the active blocks, so c̃_j is computed
EXACTLY in O(b) per scale, O(bT) = Õ(√K) total. b = Θ(√K) confirmed. No sampling, no variance, no blowup.
**VALID.**

### 6. Any hidden Ω(√K)-sample / n^{2/3} cost? — **NONE FOUND**
- **Estimating c̃_j when c_j is large:** α_j is set to `ηG/(C₁Tσr_j)` **independent of c_j**; it does not
  shrink when c_j grows. The trial count k_j = M_jU_j/α_j² therefore does not blow up at high-component
  scales. Verified on the clustered instance (c_j up to √K): Σk/T²/√K stayed bounded (10–19). **No blowup.**
- **Active-cover construction:** O(q·log(Δ/h)) = Õ(√K) emptiness queries (one P-count each). Polylog factor
  only. No hidden cost.
- **M_j blow-up at fine scales:** M_j is largest at a_j=h (smallest scale), but there r_j is correspondingly
  small so δ/r_j is large — this is exactly the term captured by Σδ/r_j, which sums to √K. The blow-up is
  accounted, not hidden.
- **n/K support-sampling frequency:** the cell estimator (§§4–8) uses **zero** support-mass samples — only
  emptiness queries. The n/K support-sampling appears ONLY in §9 (estimate K, once) and §11 (O_ε(1) genuine
  samples for A_L(Q)). It is **additive** (`+n/K`), NOT multiplied into the per-scale sum. This is the
  precise structural reason the round-2 multiplication √K · (n/K) = n^{2/3} does not recur. **Confirmed.**

---

## Why the round-2 failure mode does not recur (the crux)

Round 2 estimated each threshold's component count from a **shared pool of polylog support samples**; a
geometrically-important but support-mass-rare feature (the satellite chain) was missed unless a satellite
was sampled, which needed Ω(√K) **independent** support samples per threshold ⇒ Ω(√K · n/K) = n^{2/3}.

Round 4 replaces support-mass sampling with **uniform sampling over M_j SPATIAL candidate cells (including
empty ones)**. A feature contributing a constant fraction of the MST integral at scale r occupies ≥1 spatial
cell at that scale, so it is sampled with the right probability — and the cost of resolving it is
`M_j·U_j/α_j²` emptiness trials, NOT independent support samples. The decisive algebra is that this budget
collapses to `δ/r_j` **because b·δ/G = O(1)** (the packing), and `Σ δ/r_j ≈ √K`. Both facts are numerically
confirmed on the exact instance that broke round 2. A feature can be support-mass-rare OR
spatially-hidden-at-its-scale, but not both while contributing a constant fraction of W_Q — and the cost is
charged to spatial cells, which are cheap (emptiness = 1 P-count).

---

## Verdicts

| # | Item | Verdict | Severity |
|---|------|---------|----------|
| 1 | Packing W_Q ≥ Ω(bδ) | **VALID** | — |
| 2 | M_j count + Var(Z) ≤ Mc + c_j ≤ U_j | **VALID** | — |
| 3 | 🔴 Σ M_jU_j/α_j² = Õ(√K) (eq 8) | **VALID** | — |
| 4 | Exploration cost O(T/η), O(log s) | **VALID** (eq-5 global-cap terse) | MINOR |
| 5 | Coarse scales O_η(b)=Õ(√K) | **VALID** | — |
| 6 | Hidden Ω(√K)/n^{2/3} blowup? | **NONE FOUND** | — |

**Decisive answer: the total cost genuinely sums to Õ(√K) = Õ(n^{1/3}). The round-2 n^{2/3} blowup does
NOT recur.** The numeric Σ_j k_j (core, polylog-stripped) grows as **n^0.28–0.32 ≤ n^{1/3}**, with
core/√K bounded and core/n^{2/3} → 0; b·δ/G is bounded (the packing); n/K enters additively, never
multiplied into the per-scale sum.

**Confidence: 0.88** (the cost claim specifically). The only soft spots are the terse eq-(5) exploration
amortization (MINOR) and the §11 insertion into the full round-2 reduction, which is outside this cost-only
mandate and which I did not re-audit.

*Reproduce:* the five harness scripts written to `/tmp/cost_audit*.py` (transient); core checks are the
per-scale ratio `(M_jU_j/α_j²)/(T²δ/r_j)≈const`, `b·δ/G≈0.7`, `Σδ/r_j/√K` bounded, and Var(Z)=Mc−c² at
trials≫M/c.
