# Round 1 — Independent adversarial audit of GPT-5.5-Pro's reply

> Fresh-context, adversarial audit of `docs/webpro_round1_response.md`. Numerically-checkable
> load-bearing claims were already established by the orchestrator
> (`attack_loop/webpro_verify_round1.py`): the multiset identity (max error 0.0 / 6 instances),
> the O(log s) exploration cost (empirical 2.9–7.8 for s=10–1000), and the rare-bridge gadget
> (exactly one Θ(G) edge). This audit scrutinizes the NON-numerically-checked parts and re-runs
> independent checks. Auditor = Claude (Opus 4.8). Verifier = `sim/emst.py` (exact EMST) + the
> venv. Scripts run live; results quoted inline.

---

## Verdict summary

**Overall: (A) — the partial result (instance-sensitive Õ_ε(n/N_eff), including Õ(n^{1/3}) for
non-tail-heavy instances) is RIGOROUS at the checkable level, and the heavy-tail lemma is correctly
isolated as the only remaining gap to the worst case.** One MINOR self-flagged correctness item
(WSPD redundant-pair enumeration) and one GAP that lives strictly *inside* the already-open
heavy-tail problem (the constant-factor W_H guess needed to set L) — neither undermines the partial
result. No smuggled √n found in any checked step. Confidence **0.88**.

Per-task: §1 VALID · §2 VALID · §3 NEEDS-REPAIR (minor, self-flagged) · §4 VALID-with-a-contained-GAP
· §5 VALID.

---

## §1 — Cheap unbiased 1/|C_λ(p)| estimator + cell-graph implementation — **VALID**

**Unbiasedness / variance of the vertex version (E[I]=c(λ)/n, Var≤c/n).** Correct. `I(p)=1` iff `p`
is the minimum-ranked vertex of its component `C` (prob `1/|C|`), so for uniform `p`,
`E[I]=Σ_C (|C|/n)(1/|C|)=c(λ)/n`. As a Bernoulli, `Var(I)≤E[I]=c/n`, hence `Var[ĉ(λ)]≤n·c(λ)/k`. ✓

**Size-bias correction `Y=1[z min-ranked]/m(z)` (cell-graph version).** Correct — I verified the
algebra *and* by Monte-Carlo (`/tmp/audit_sizebias.py`):
- `E[Y]=Σ_z (m(z)/n)·(1/|C(z)|)·(1/m(z)) = (1/n)Σ_z 1/|C(z)| = (1/n)Σ_{components}|C|·(1/|C|)=c/n`. ✓
- `E[Y²]=(1/n)Σ_z 1/(|C|·m(z)) ≤ (1/n)Σ_z 1/|C| = c/n` (since `m(z)≥1`), so `Var(Y)≤c/n`. ✓
- MC (random cell forest, random occupancies): `E[Y]=0.06223` vs target `c/n=0.06202`; empirical
  `Var=0.0222 ≤ c/n=0.0620`. ✓

The `1/m(z)` factor exactly cancels the `m(z)/n` size-bias of landing in a cell by sampling a
uniform point. This is the crux and it is right.

**"Õ_ε(1) expected range queries per trial" + does it dodge CellSampling Ω(√n)?** Two pieces:
1. *Cells visited per trial* = the same combinatorial rank-stopping quantity as the vertex version,
   `E[#cells] ≤ 1+H_{|C|-1}=O(log|C|)≤O(log n)`. The orchestrator already verified this object
   numerically at the vertex level (2.9–7.8); the cell-level argument is verbatim. ✓
2. *Queries per visited cell* = enumerate WSPD-incident cells. Pro's §1 phrase "O_ε(1) per visited
   cell" is **loose**; his own §3 gives the honest count `O(δ^{-2}log²Δ) = Õ_ε(1)` (polylog, not
   literal `O(1)`). Consistent provided "Õ" absorbs `log Δ` factors, which is the convention here.

   **Does it genuinely avoid the source's CellSampling Ω(√n)?** YES, and this is a substantive,
   non-obvious point that I independently confirmed. The source's Ω(√n) (Lemma 19/20, Cor 18) is
   specifically for (a) drawing a *near-uniform nonempty cell* and (b) estimating *N_i=#nonempty
   cells* to O(1)-relative error. Pro's estimator does **neither**: it samples a uniform *point*
   (not a uniform cell) and never estimates `N_i`. Critically, it also dodges the project's own
   killed estimator **U-N2** (`Z=n·β(v)/a_v`, which had `Var=Θ(n^{1.5})` on the √n-singletons+bulk
   instance ⇒ Ω(√n) samples). I built that exact worst-case as an EMST instance
   (`/tmp/audit_var_cmp.py`): for n=2500 it gives **Γ≈49.5 ≈ √n**, *not* `n^{1.5}`. The size-bias
   correction divides out occupancy disparity, so Pro's variance object is `Γ=nΣw²/W²` (MST
   geometry), **not** cell-occupancy variance. This is a genuinely different estimator and it
   structurally escapes both Ω(√n)-flavored barriers. ✓

**Verdict §1: VALID.** The §C/U-N4 obstruction ("cheap connectivity from counts is the crux /
exploring a component costs its size") is correctly **REFUTED**. I concur with the refutation.

---

## §2 — Instance-sensitive theorem (the main partial result) — **VALID**

**(a) `Var(Ŵ_H) ≤ (n/k)Σ w_f²` from `E[τ²]=(1/n)Σw_f²`.** Correct and verified numerically
(`/tmp/audit_var.py`). The τ-multiset over all n vertices is `{0}∪{MST edge weights}` (established
identity), so `E[τ]=W_H/n`, `E[τ²]=(1/n)Σw_f²`, `Var(Ŵ_H)=(n²/k)Var(τ)≤(n²/k)E[τ²]=(n/k)Σw_f²`. The
relative variance is `Var(Ŵ_H)/W_H² ≤ Γ/k`. Tested:
- uniform grid n=2500: Γ=1.00, N_eff=2499, relVar(MC)≈0 ✓
- uniform random n=2000: Γ=1.22, N_eff=1644, relVar=0.0011 ≤ Γ/k=0.0061 ✓
- two grids+bridge n=2000: Γ=500.8, N_eff=3.84, relVar=2.33 ≤ Γ/k=2.50 ✓ (bound holds and is tight)

**(b) WSPD square-weight comparison `Σ_{T_H}w_f² ≤ (1+O(δ))²Σ_{T_P}ℓ_e²`.** The full logical chain
is VALID (audited step-by-step in `/tmp/audit_wspd.py`):
- (iv) `Σ_{Q_e}w² ≤ (Σ_{Q_e}w)² ≤ (1+O(δ))²ℓ_e²` — needs weights ≥ 0 (cross terms `2w_iw_j≥0`). ✓
- (iii) `Σ_{T'}w² ≤ Σ_{U}w² ≤ Σ_e Σ_{Q_e}w²` where `U=⋃_e edges(Q_e)`: first ineq because `T'⊆U`
  (set, nonneg terms); second because `U` is a set while the RHS counts with multiplicity. ✓
- (v) **"Kruskal MST minimizes Σ of squared edge weights among spanning trees."** TRUE. The matroid
  greedy selects the same edge SET for any strictly-monotone-increasing `f` (`f(x)=x²` on weights
  ≥ 0 qualifies) because the sorted order is unchanged. I **brute-forced** this over all spanning
  trees of random complete graphs (n=4–7, up to 16807 trees, `/tmp/audit_t2.py`): `mst_sq == min_sq`
  in every case. ✓ Pro's parenthetical justification ("order preserved") is exactly right.

  Combine with `W_H ≥ W`: `nΣ_{T_H}w²/W_H² ≤ (1+O(δ))²·nΣℓ²/W² = (1+O(δ))²Γ(P)`. ✓

**(c) The bound `Õ_ε(n/N_eff)`, `N_eff=W²/Σℓ²`, `o(√n)` iff `N_eff=ω(√n)`; `Õ(n^{1/3})` when
`ℓ_max≤W/n^{2/3}`.** Correct. Chebyshev with `k=O(Γ/ε²)` gives `(1±ε)W`; since `Γ=n/N_eff`, cost is
`Õ_ε(n/N_eff)`, which is `o(√n)` iff `N_eff=ω(√n)`. Corollary: `ℓ_max≤W/n^{2/3} ⇒ Σℓ²≤ℓ_maxΣℓ=ℓ_maxW
≤W²/n^{2/3} ⇒ Γ≤n^{1/3}` (`/tmp/audit_t45.py`). ✓

**Does anything smuggle a √n?** No. The partial result is self-contained: it needs **no** threshold
`L` and **no** `W_H` guess (`/tmp/audit_partial.py`). Honest conditional phrasing ("under promise
Γ≤G, Õ(G)"); an adaptive doubling-on-`k` removes the promise. The variance object is `Γ` (MST
geometry), and `Γ` is provably moderate (≈√n) on the instance that killed U-N2.

**Verdict §2: VALID.** The death-time estimator variance matches numerics, the WSPD comparison and
the sum-of-squares minimality are both rigorous.

---

## §3 — Range-counting implementation — **NEEDS-REPAIR (minor, self-flagged; no √n leak)**

**One bottleneck-Dijkstra expansion = `O(δ^{-2}log²Δ)` queries.** The count is structurally sound:
each dyadic ancestor `a∋p` has `O(δ^{-2})` candidate partner cells (separation `δ`, partner side
within factor 2, center at `Θ(r(a)/δ)`); `O(log Δ)` levels; emptiness/membership/representatives via
polylog range queries (`O(log Δ)` per dyadic-membership predicate). Product is `Õ_ε(1)` per
expansion, `Õ_ε(1)` per τ-sample after the `O(log n)` expansions. No √n appears. ✓ (One nit: a point
lies in `O(log Δ)` dyadic cells each with `O(δ^{-2})` partners ⇒ `O(δ^{-2}log Δ)` *incident pairs*,
i.e. degree is polylog not `O(1)`; this is already what §3 says, only §1's wording is loose.)

**Expected→hard-cap conversion (abort after `c·k log n` expansions, Markov).** VALID. Total expected
expansions over `k` samples is `O(k log n)`; aborting at a large constant multiple adds `O(1)` extra
failure probability by Markov; combine with the median-boost. Standard. ✓

**Hidden cost — the redundant-pair / representative convention (Pro's own 0.85 flag).** This is the
one genuinely-unaudited item. To BFS `G_{≤λ}` from a revealed cell `z` we must enumerate **all**
`z'` with a WSPD edge to `z` of weight `≤λ`, completely and without double-counting, using the
lex-least-representative convention that defines `H`. The worry is *correctness* (completeness +
dedup of incident-edge enumeration), **not** a cost blowup or a √n leak — I could not surface any
mechanism by which it inflates the query count past polylog. Pro's self-assessment (0.85, "only the
redundant-pair convention needs tedious auditing; a compressed WSPD should make it routine") is
honest and, I believe, correct in spirit. Classify **MINOR**: routine-but-unverified bookkeeping, no
identified √n.

**Verdict §3: NEEDS-REPAIR (minor).** The cost arithmetic is sound; the incident-edge enumeration
convention is the one piece needing a careful write-up. No fatal issue.

---

## §4 — Is the heavy-tail lemma genuinely the ONLY remaining gap? — **VALID, with a contained GAP**

**`Var[(n/k)ΣX_{L,j}] ≤ nLW_H/k` (truncated estimator).** VALID (`/tmp/audit_t45.py`):
`Var≤(n²/k)E[X_L²]`; `X_L²≤L·X_L` (since `0≤X_L≤L`) ⇒ `E[X_L²]≤L·E[X_L]`; `n·E[X_L]=A_L≤W_H` ⇒
`Var≤(n/k)L·A_L≤nLW_H/k`. With `L=W_H/n^{2/3}`: relative variance `≤n^{1/3}/k`, so
`k=Θ(n^{1/3}/ε²)` gives additive `εW_H` for `A_L` in **Õ_ε(n^{1/3})**. ✓ So the bulk `A_L` is indeed
the cheap part, and only `B_L=Σ(w_e−L)_+` over `≤W_H/L=n^{2/3}` long edges remains. The reduction is
correctly stated.

**Other potential hidden gaps (all checked, `/tmp/audit_t4_circ.py`):**
- *T_H vs T_P.* The death-time is on `T_H` (the spanner), but the variance is controlled by `Γ(P)`
  (Euclidean MST) through the `(1+O(δ))²` WSPD comparison, and `W↔W_H` within `(1+O(δ))`. Choosing
  `δ≪ε` makes the spanner distortion lower-order. No smuggled error. ✓
- *Spanner-distortion × tail.* A long Euclidean MST edge maps to a spanner *path* summing to
  `(1+O(δ))ℓ`, but the worst-case bridge is a **single** WSPD pair ⇒ a single long `H`-edge; and
  `|{long T_H edges}| ≤ W_H/L ≈ n^{2/3}` regardless. Consistent. ✓
- *Failure boosting.* Median-of-O(log) independent runs; standard. ✓

**The constant-factor `W_H` guess to set `L` (THE one real gap).** Setting `L=W_H/n^{2/3}` needs a
constant-factor estimate of `W_H`. In the **worst case** (`Γ≈n`), even a constant-factor `W` via the
death-time estimator costs `~Γ~n` — *not* cheap — and the cluster-count route hits CellSampling Ω(√n)
per scale. So obtaining `L` is **not proven** to be cheap/non-circular. **However:** (i) this lives
**strictly inside** the heavy-tail problem, which Pro does *not* claim to have solved; (ii) it is
plausibly removable by an `O(log)`-guess sweep over `L=2^j` (only `O(log(nΔ))` candidates) or a
geometric constant-factor `W` bound, provided the heavy-tail lemma is robust to a constant factor in
`L` — but Pro does not spell this out. Classify **GAP (fixable)**, and note it does **not** touch the
partial result (which needs no `L`). So the framing "heavy-tail lemma is the only remaining gap" is
**essentially correct**, with the caveat that "supply a constant-factor `W_H`" should be folded into
the lemma's hypotheses (the round-2 brief already does this: "and a constant-factor estimate of W").

**Worst-case instance.** Two grids + Θ(n) bridge gives `N_eff=Θ(1)` (I measured Γ=500.8, N_eff=3.84
at n=2000 ⇒ Γ=Θ(n)), one heavy τ among n entries ⇒ Ω(n) death-time samples to see it. Correctly the
hard case; spatial range info is the missing ingredient. ✓

**Verdict §4: VALID** that the heavy-tail lemma is the only remaining gap, with the contained
**GAP** that the `W_H`-guess must be supplied to/inside that lemma (as the round-2 brief already
does).

---

## §5 — Pro's assessment of the gadget LB barrier — **VALID**

The arithmetic is correct (`/tmp/audit_t45.py`): with `m` switchable regions of `p` points in a
side-`s` square, one switch perturbs MST weight by `≤O(s√p)`, null weight `Ω(ms)`, `O(1)` regions
per query ⇒ a constant relative gap needs `k=Ω(m/√p)` switches, hitting LB `≤O(m/k)≤O(√p)` and `≤m`;
with `n=mp`, `max_{mp=n} min{m,√p}=n^{1/3}` (optimum `m=√p ⇒ m³=n ⇒ m=n^{1/3}`, both equal `n^{1/3}`,
checked at n=10^6,10^9,10^12). ✓

Pro's caveat is **sound and important**: the `Ω(ms)` baseline and the `O(1)`-regions-per-query
coverage are SUBSTANTIVE assumptions, not consequences of "disjoint cells" alone. Adjacent regions,
cheap fixed skeletons, or globally-correlated gadgets can violate them. So this is a barrier *for the
localized-hitting template*, **not** a universal obstruction to an Ω(√n) lower bound. This correctly
de-escalates the project's own P1/P2 "near-proof" to "a loophole remains." I concur.

**Verdict §5: VALID.**

---

## Orchestrator's own earlier claims that Pro refuted — concurrence

- **U-N4** ("cheap connectivity from counts is the crux"; "exploring a component costs its size";
  the §C categorical obstruction): **REFUTED by Pro, and I CONCUR.** The random-leader / minimum-rank
  exploration estimates `1/|C_λ(p)|` unbiasedly in `O(log s)` inspections, and the size-bias-corrected
  cell version runs in `Õ_ε(1)` queries/trial, dodging CellSampling Ω(√n) (which only bites
  uniform-cell sampling and `N_i` estimation — neither used). Numerically + algebraically confirmed.
- **U-N2** ("inverse-cell-multiplicity estimator has Var=Θ(n^{1.5})"): Pro's estimator is a
  *different* object (size-bias corrected, integrated over scales), with variance `Γ`. On the exact
  U-N2 killer instance I measured `Γ≈√n`, not `n^{1.5}`. So U-N2's variance verdict is correct *for
  U-N2* but does **not** transfer to Pro's estimator. I concur with both.
- **U-P1** (MST not √n-hard; cell-sampling does not reduce to MST) is *consistent with* and
  *reinforced by* Pro's result. Not contradicted.

---

## Findings, classified

| # | Item | Class | Status |
|---|------|-------|--------|
| 1 | §1 unbiasedness + size-bias correction + dodging CellSampling Ω(√n) | — | VALID |
| 2 | §2(a) death-time variance `(n/k)Σw²` | — | VALID (numerics tight) |
| 3 | §2(b) WSPD square-weight chain incl. "MST minimizes Σw²" | — | VALID (brute-forced) |
| 4 | §2(c) `Õ_ε(n/N_eff)`, `Õ(n^{1/3})` corollary | — | VALID |
| 5 | §3 per-expansion `O(δ^{-2}log²Δ)` + Markov hard-cap | — | VALID |
| 6 | §3 WSPD redundant-pair / representative enumeration convention | MINOR | self-flagged 0.85, no √n leak, unaudited bookkeeping |
| 7 | §4 truncated `Var≤nLW_H/k`; A_L cheap, only B_L remains | — | VALID |
| 8 | §4 constant-factor `W_H` guess to set `L` | GAP | fixable; lives *inside* the open heavy-tail lemma; fold into lemma hypotheses |
| 9 | §5 gadget barrier caps at `n^{1/3}` + substantive-assumptions caveat | — | VALID |

No FATAL finding. No smuggled √n / unbounded-variance / floor-violation in any checked step.

---

## Overall classification: **(A)**

**The partial result — instance-sensitive `Õ_ε(n/N_eff)` queries (`N_eff=W²/Σℓ²`), in particular
`Õ_ε(n^{1/3})` for non-tail-heavy instances (`ℓ_max≤W/n^{2/3}`) — is RIGOROUS at the AI-checkable
level, and the heavy-tail lemma is correctly isolated as the only remaining gap to the worst case.**

Caveats that keep this short of "proved theorem" (consistent with "AI-verified ≠ proved"):
- The §3 WSPD incident-edge enumeration (redundant-pair convention) needs a careful manual write-up
  (MINOR, Pro's own 0.85).
- The constant-factor `W_H` guess needed to set `L` is a contained GAP that should be stated as a
  hypothesis of the heavy-tail lemma (the round-2 brief already does this).

These two are exactly the items Pro himself flagged; neither touches the self-contained partial
result. The worst-case `Õ(n^{1/3})` (or any `o(√n)`) genuinely hinges on the single, well-posed,
**geometric** heavy-tail lemma — a far better-isolated crux than the now-refuted U-N4.

**Auditor confidence: 0.88** that classification (A) is correct. (Residual 0.12: the unaudited WSPD
enumeration convention could conceal an implementation subtlety; and the heavy-tail lemma itself
remains genuinely open — its difficulty is correctly *not* claimed resolved.)
