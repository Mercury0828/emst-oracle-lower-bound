# Research-Line Ledger — emst-oracle-UPPER-bound (PIVOT, opened 2026-06-21)

> **Append-only.** Opened at the §9.6 human kill/pivot gate after the LOWER-bound line
> (`research_line_emst.md`) was (near-)refuted: the gadget-packing lower-bound approach provably caps
> at n^{1/3} (P1/P2). The owner chose to **pivot to the UPPER bound** — close the same Driemel et al.
> Ω(n^{1/3}) vs Õ(√n) gap *from above*. Same problem, same model, same venue (SODA); opposite side.
> 🔴 Re-read this + `PROJECT_STATE.md` + frozen artifacts before continuing — never from memory.

## HEADLINE
**[2026-06-21] ✅ §9.4 AI-CONVERGENCE REACHED on the unconditional Õ_ε(n^{1/3}) MST-weight closure → HUMAN
GATE #2.** Round 5 (Pro) gave the full self-contained proof (matching Ω(n^{1/3}) up to polylog); the FINAL
audit (codex GPT-5.5-xhigh) returns **(CONVERGED)** — all items VALID, no counterexample, residual = the
inherited local-WSPD death-time impl + routine bookkeeping. 3 independent clean audits stand (round-4
cost+assembly [Claude, cross-model], round-5 final [codex, same-family]); the genuinely-new N_j-exploration
term's polynomial cores (K/b, Kδ/W_Q) confirmed O(√K) by execution (`webpro_verify_round5_cores.py`,
K=272..4160). **Confidence: ~80% (ours), 0.91 (Pro).** Next: optional cross-model Claude round-5 audit
(API was 529-throttled), then human-expert verification + formal writeup + preprint sweep + dedup re-check.
🔴 Candidate closure of a PUBLISHED open problem — NOT proved until human-referee-checked (the round-2→3
self-refutation is why). Full thread: `docs/webpro_thread_state.md`. Prior status below.

**[2026-06-21] (prior) Round-5 consolidated proof; was "final audit pending" — now CONVERGED (above).**

**[2026-06-21] (prior) Round 4 = spatial-cell repair, strong candidate (recovery+cost+assembly verified).
Round 5 consolidated it (above).** After round 3 refuted round 2's seed-reuse, Pro's round 4 replaced it with the
**empty-cell SPATIAL estimator** (sample spatial cells incl. empty; Var(Z)≤M·c; packing W_Q=Ω(bδ) ⇒ cost
sums to √K). 2 independent audits + orchestrator numerics confirm: it RECOVERS w(MST(Q)) on the round-3
satellite counterexample, the cost is genuinely **Õ(√K)=Õ(n^{1/3})** (no n^{2/3} blowup — the round-2
failure mode), the assembly is sound, and a hard counterexample hunt found NOTHING. Only fix: state the
variance via c_j (component count) not N_j. **Confidence the full closure holds: ~78%.** Essentially
AI-convergence modulo the c_j write-up fix + human verification → **human gate #2** (round 5 = finishing
request for the clean write-up, then a final audit). 🔴 Candidate closure of a PUBLISHED open problem —
NOT proved until human-referee-checked. Full thread: `docs/webpro_thread_state.md`. Prior status below.

**[2026-06-21] (history) Round 2 closure → refuted in round 3 → repaired in round 4 (above). The
multi-round + numeric-confirmation discipline caught the round-2 error; "AI-verified ≠ proved".** Pro's round-2 closure relied on a
seed-reuse trick that is **unsound**: estimating w(MST(Q)) for the K-point support has the same rare
long-edge tail, and polylog shared samples give growing per-run error (Ω(√K) samples needed ⇒ n^{2/3},
not n^{1/3}). The [1]-Thm-30 repair also fails (range-count on Q ≠ on P). 🔴 **My 3 round-2 audits were
over-confident** (accepted the seed-reuse) — honest lesson. **SURVIVES:** the round-1 **instance-sensitive
Õ(n/N_eff) = Õ(n^{1/3}) for non-tail-heavy instances** (verified, real partial contribution). **OPEN:**
the full Õ(n^{1/3}), reduced to the sharper Lemma 3 (estimate w(MST(Q)) for an implicit support in
Õ(√K+n/K) catching rare low-mass components via spatial range-emptiness, not √K samples). Confidence the
full closure exists+findable: **~40%** (down from ~72%). Round 4 to Pro prepared, OR consolidate the
partial result. Full thread: `docs/webpro_thread_state.md`. Prior status below.

**[2026-06-21] (REFUTED) Round 2 = candidate closure (unconditional Õ_ε(n^{1/3})). Round 3 broke it (the
seed-reuse is unsound) — see above.** Survived **3 independent blind audits + exact-EMST numerics**: the REDUCTION is SOUND (support
regularize to K=Θ(n^{2/3}) cells [Lemma 1 packing] → snapping preserves the tail [Lemma 2] + W_Q=O(W) →
Czumaj-style Õ(√K) sparse-support MST estimator + the SEED-REUSE trick avoiding the √K·(n/K)=n^{2/3}
blow-up → heavy tail B̂_L=Ŵ_Q−Â_Q → geometric W-search). **No counterexample, no smuggled √n** ("the
reduction is unbreakable"). The ONLY unresolved item = **Lemma 3's query accounting AS WRITTEN** (the
Czumaj-import / WSPD-substitution): a fixable GAP, NOT FATAL, with a clean repair (use the source's own
Theorem 30, which already does Õ(√n) MST estimation natively in range-counting). **Round 3 to Pro =
repair Lemma 3** (`docs/webpro_round3_brief.md`); then re-audit → §9.4 convergence → human gate #2.
🔴 Candidate closure of a PUBLISHED open problem — NOT proved until human-expert verified. Full thread:
`docs/webpro_thread_state.md`. Prior status below.

**[2026-06-21] (prior) Round 1 — U-N4 refuted; instance-sensitive Õ(n/N_eff); heavy-tail crux. (Round 2
turned the heavy-tail lemma into a candidate full closure — above.)** Pro's random-leader estimator + exact death-time/MST-edge
multiset identity (both numerically verified) bypass the cell-sampling Ω(√n) entirely. Remaining: estimate
the excess of ≤n^{2/3} long MST edges above L=Θ(W/n^{2/3}) in Õ(n^{1/3}) (the death-time sampler misses
rare long edges; needs spatial info). Full thread: `docs/webpro_thread_state.md`. Independent audit of
the variance theorem + WSPD implementation RUNNING. "AI-verified ≠ proved." This is the strongest state
yet; closing the heavy-tail lemma ⇒ unconditional Õ(n^{1/3}) ⇒ closes the gap from above (SODA-level).
Prior (now partly superseded) status below.

**[2026-06-21] (prior) Round 6 — whole problem reduced to U-N4 (NOW REFUTED by Pro); paper-orientation
verdict NOT SODA-level (pre-Pro). Superseded by the Pro round-1 advance above.**
The combinatorial cost arithmetic min(n/c,√c)≤n^{1/3} is elementary, but the algorithm is a REDUCTION
conditional on TWO unproven range-counting primitives ([[U-P5]], corrected from an earlier over-claim
of "PROVEN"); the entire open problem is now [[U-N4]]: cheap **connectivity from additive counts** (the
genuine crux of sublinear geometric MST, same family as cell-sampling Ω(√n)). **No unconditional bound
has moved — the proven frontier is still the inherited Ω(n^{1/3}) / Õ(√n).** Independent paper-orientation
audit (`gate_paper_orientation_upper.md`) = **NO for SODA now** (barrier P1/P2 is near-default given the
source already got n^{1/3} that way + has an open loophole; the conditional UB's condition IS the crux ⇒
a reduction, not a result). **SODA-level requires RESOLVING U-N4 (human-verified), either direction.**
**Confidence: o(√n) ~55%, Õ(n^{1/3}) ~30% — hinges ENTIRELY on U-N4.** Decision pending owner. Prior below.

**[2026-06-21] (prior) Round 5 — DENSE large-λ gap (U-N3); §9.1 juncture.** The Round-4 algorithm is sound in the
SPARSE regime but its large-λ cost bound relied on "c(λ)=O(n/λ)", **REFUTED** by a uniform-grid
counterexample ([[U-N3]]): c(λ)=n≫n/λ at a weight-relevant λ=Θ(√n) ⇒ the 2-axis estimator costs √n
there. This is the 4th obstruction in the cycle (islands→filament→all-strata→dense). Each prior one was
a weight-red-herring fixed by a new branch; the dense regime is *likely* the same (uniform-grid weight
is trivially ~√(n·Area) by density) but UNPROVEN. **Confidence: o(√n) ~65%, Õ(n^{1/3}) ~30%** (codex
98% the stated lemma is false; the broader o(√n) thesis plausibly survives). **Decision needed:**
escalate the clean (1±ε) proof — esp. the dense-regime branch — to **web GPT-5.5-Pro** (human-relayed),
vs more codex rounds, vs consolidate (LB barrier P1/P2 + UB skeleton) into a paper, vs handoff. Prior below.

**[2026-06-21] (prior) Round 4 + Audit U-D — closing Õ(n^{1/3}) numerically validated; ~80% o(√n) / ~40% Õ(n^{1/3}).** The one gap
codex flagged (a per-size-bucket component lemma) is FALSE but a RED HERRING: the weight needs only the
**scalar** c(λ) via **w(MST)=∫(c(t)−1)dt** ([[U-P4]]), and c(λ) is estimable in min(λ,√(n/λ))≤n^{1/3}
per scale (point-sampling small λ / 2-axis slab large λ), with the dense-gadget scan Õ(n^{1/3}). No √n
hard instance survives. **Remaining = a STANDARD (1±ε) variance/error-budget proof + hitting/coupling
lemma** (no exotic primitive). **Round 5 = route the full rigorous algorithm + proof to codex** → if it
survives ≥3 audits ⇒ §9.4 AI-convergence ⇒ human gate #2 ("AI-verified ≠ proved"). Prior status below.

**[2026-06-21] (prior) Round 3 + Audit U-C — candidate Õ(n^{1/3}); ~60% o(√n) / ~35% Õ(n^{1/3}).** The filament obstruction is REPAIRABLE
([[U-P3]]): per-scale persistence cost = **min(point-sampling ~λ, slab ~√(n/λ)), which peaks at
λ=n^{1/3}=the floor** (verified numerically). No √n lower bound survives the spread-vs-concentrate vise.
**Round 4 = formalize the full algorithm** (all component strata + dense-block + (1±ε) + variance proof
+ counting-oracle implementation). If it survives audit ⇒ Õ(n^{1/3}) closes the Driemel gap from above
= the headline SODA result. Prior status below.

**[2026-06-21] (prior) Round 2 DONE — the √n variance barrier is BROKEN ([[U-P2]]); ~50% o(√n).** An importance-sampling / localized-probe primitive (verified, polylog queries)
defeats codex's variance obstruction on its own islands instance, via the **tile-or-blowup vise** (a
constant-fraction low-mass signal can't be both hard-to-find and weight-significant). The live route is
**stratified importance sampling** of the component-persistence sum Σ_i λ_i c_i. OPEN (Round 3): extend
the primitive to ALL strata, handle the dense-block n^{1/3} stratum (the genuine floor), and tighten to
(1±ε) — yielding a full o(√n) / ideally Õ(n^{1/3}) algorithm. **Next: Round-3 attacker brief to build it.**

**[2026-06-21] (prior) Round 1 DONE — pivot CONFIRMED ALIVE; reduced to a rectangle-native estimator.** Target: a sub-√n / Õ(n^{1/3}) range-COUNTING algorithm for (1±ε)-EMST-weight (close the
Driemel gap from above). Round 1 (codex GPT-5.5-xhigh + Audit U-A) established: (i) the natural
CRT route is **√n-blocked** by the source's own **CellSampling Ω(√n)** lower bound ([[U-B1]]; corrects
the Round-1 brief's misdiagnosis of "BFS depth t"); (ii) the point-sampling workaround is dead by
variance ([[U-N2]]); BUT (iii) **MST-weight is provably NOT √n-hard** — no reduction from cell-sampling
(1-D MST telescopes, occupancy-invariant) ([[U-P1]]) — so the pivot is **alive**. Reduced open problem:
estimate the weighted aggregate Σ_i λ_i c_i directly (no per-scale cell sampling), e.g. via the planar
Euler relation from exact occupancy/adjacency counts. Confidence: ~35% an o(√n) algorithm exists, ~15%
Õ(n^{1/3}). **Next: Round 2 attacker brief on the rectangle-native / Euler-aggregate estimator.**

## 🔴 Repo / name staleness + dedup
- The repo / idea name **`emst-oracle-lower-bound` is now partially STALE** — the active contribution is
  an UPPER bound (a better algorithm), not a lower bound. The GOAL (close the Driemel gap, SODA) is
  unchanged. Do not rename the repo without owner sign-off; just be aware.
- **TODO (own-work dedup, guide §0):** switching lower→upper is a contribution change ⇒ the own-work
  dedup loop should be re-closed (`scripts/own_work_corpus.py` — NOT present in this isolated repo;
  flag to the owner / re-run in the parent research-os). Provisionally: the upper-bound EMST
  counting-oracle algorithm has no obvious overlap with the two prior SODA own-works
  (`mts-sublinear-smoothness`, `dynamic-weighted-mis-fat-objects`), but confirm.

---

## Frozen model / notation (same as the LB line — freeze)
- P ⊂ [Δ]² integer grid, |P| = n, spread Δ = O(n). w(P) = Euclidean MST weight. Target = a **(1±ε)
  multiplicative** estimate, fixed constant ε ∈ (0,1).
- **Oracle:** orthogonal range-**counting** — query R (axis-aligned rectangle) → exact integer |P∩R|.
  Cost = #queries. (Strictly stronger than emptiness.)
- **Known bounds (Driemel et al., SoCG 2025, arXiv:2504.15292):** upper **Õ(√n)** = **Theorem 30**;
  lower **Ω(n^{1/3})** = **Lemma 32** (any o(n^{1/3})-query algorithm has constant multiplicative error).
  Gap Ω(n^{1/3}) vs Õ(√n) is the open problem; this line attacks the upper side.

## Carried-over PROVEN facts from the LB line (`research_line_emst.md` — use freely)
- **[LB-P1/P2] The gadget-packing lower-bound approach caps at n^{1/3}.** Equivalently (the
  algorithmic reading, which MOTIVATES this line): under the hard distributions of that family, a
  constant-fraction EMST-weight difference is **coarsely estimable** — a single-cell gap ≤ O(s√p) is
  visible to a rectangle, and a correlated Θ(w) gap is estimable by O(polylog) coarse counting queries.
  ⇒ the "hardness" that would be needed for an Ω(√n) lower bound does not materialize ⇒ the truth is
  plausibly Θ(n^{1/3}). **This is evidence, not a proof that an Õ(n^{1/3}) algorithm exists** — building
  it is exactly this line's job.

## Proven results `P*` (this line) — "use freely, do not re-derive"
- **U-P5 [2026-06-21] — A REDUCTION (not a closed theorem): the whole Õ(n^{1/3}) algorithm reduces to
  TWO unproven range-counting primitives.** ⚠️ **Corrected framing (paper-orientation audit caught my
  over-claim "cost model PROVEN / clean conditional theorem"):** only the *combinatorial cost arithmetic*
  is elementary — IF c(λ) is estimable at per-scale cost min(Õ(n/c(λ)), Õ(√c(λ))), then since that min
  ≤ Õ(n^{1/3}) (peak at c=n^{2/3}), summing over Õ(1) scales + dense-gadget scan gives Õ(n^{1/3}). The
  *idealized* dense estimator Y_λ(p)=1/|C_λ(p)| does have E=c(λ)/n, Var≤c(λ)/n (so n/c(λ) samples
  suffice IN PRINCIPLE). **BUT the reduction is CONDITIONAL on two primitives codex itself could NOT
  implement (Round 6, "cannot honestly return the theorem as proved"):** (i) the **dense** primitive —
  an unbiased bounded estimate of 1/|C_λ(p)| (single-linkage component size / death-label) in polylog
  range-counting queries — naive box counts give local degree not component/chain size; (ii) the
  **sparse** primitive — actually estimating c(λ) (component count) in Õ(√c(λ)), whereas a 2-axis
  nonempty-cell count gives spatial SUPPORT not component count. **So U-P5 is "IF primitives (i)+(ii)
  exist, THEN Õ(n^{1/3})" — a reduction of the open problem to [[U-N4]], NOT a proven (even conditional)
  algorithm with a clean side-assumption.** Do NOT write it as a theorem.
- **U-P4 [2026-06-21] — The WEIGHT needs only the SCALAR cluster count c(λ); the per-size-bucket
  component lemma is a RED HERRING (Audit U-D, classification (B)).** codex's Round-4 gap (a per-bucket
  "slab component-counting lemma") is genuinely **false** (uncomputable in dense slabs). BUT the MST
  weight does not need it: **w(MST) = ∫₀^∞ (c(t) − 1) dt** where **c(λ) = #components at scale λ =
  1 + #(MST edges of length ≥ λ)** — a SCALAR per scale (verified: integral ratio 1.0001). The scalar
  c(λ) is estimable in **Õ(√(n/λ))** at large λ by a 2-axis λ-cell estimator (verified ratio→1.01)
  **⚠️ ONLY in the SPARSE regime c(λ)=O(n/λ) — the "weight-relevant ⇒ c(λ)=O(n/λ)" step is REFUTED by
  [[U-N3]]** (dense uniform grid: c(λ)=n≫n/λ at a weight-relevant λ=Θ(√n), estimator costs √n), and in
  **Õ(λ)** at small λ by point-sampling — so in the SPARSE regime per
  scale **min(λ, √(n/λ)) ≤ n^{1/3}**; the DENSE regime (c(λ)≫n/λ) is an OPEN gap ([[U-N3]]; likely a
  weight-red-herring needing a density branch). Sparse-regime branches numerically validated FOR THE
  WEIGHT over an exact range-counting oracle (flat up to n=10⁹). The dense-gadget stratum is Õ(n^{1/3})
  (a dense block is ONE component / Õ(1) persistence, so weight anomalies must tile ⇒ Θ(n^{1/3}) family,
  the [[U-P2]] vise). **No √n hard instance survives at large λ** (a constant-fraction large-λ weight gap
  is coarsely visible: random λ-box hit-frac 0.27, 2λ-box 0.996). Scripts `attack_loop/auditUD_*.py`.
  ⇒ **the closing Õ(n^{1/3}) algorithm now needs only a STANDARD (1±ε) variance/error-budget proof +
  a hitting/coupling lemma** — no exotic primitive. (🔑 c(λ) is NOT estimated as N_i to relative error;
  it is a scalar MST-edge-count recovered by a hitting estimator — does not invoke [[U-B1]].)
- **U-P3 [2026-06-21] — The filament obstruction is REPAIRABLE; per-scale cost = min(point-sample,
  slab) peaks at n^{1/3}.** codex's filament (Round 3) defeats only the *uniform 2D-box* primitive. Two
  facts (verified numerically, `attack_loop/auditUC_*.py` + `orch_check_pointsample.py`):
  - **(large-λ branch — slab):** a scale-λ singleton stratum has ≤ M = n/λ nonempty width-λ slabs per
    axis, so 1-D slab-count localizes/estimates it in **O(√M·polylog) = O(√(n/λ))** queries (codex's
    λ=√n filament ⇒ n^{1/4}).
  - **(small-λ branch — point-sampling):** the lonely-at-scale-λ fraction is **1/λ**, so uniform
    point-sampling (sample p∈P via range-counting; test loneliness with a λ-box/disk count) estimates
    the scale-λ contribution in **O(λ·polylog)** queries (verified: est_f tracks 1/λ).
  - **⇒ per-scale cost ≤ min(λ, √(n/λ)), maximized at λ = n^{1/3} (cost n^{1/3}); over Õ(1) scales,
    worst-case Õ(n^{1/3})** — exactly the floor. The candidate **closing** algorithm. (Open: extend
    from singletons to all component sizes/strata + the dense-block Lemma-32 stratum + (1±ε) + variance
    proof — Round 4.) Also [VERIFIED-leaning] NO √n lower bound survives: a constant-fraction MST gap
    must be SPREAD over Θ(n/λ) cells ⇒ a random λ-box hits a differing cell w.p. Θ(1) ⇒ coarsely
    distinguishable (the spread-vs-concentrate vise; consistent with [[U-P1]]/[[P1]]).
- **U-P2 [2026-06-21] — The √n variance barrier is BREAKABLE by importance sampling (the islands
  instance is NOT hard); the "tile-or-blowup vise".** codex's Round-2 obstruction (the islands+bulk
  variance argument, [[U-N2]]-style) is **mis-scoped**: Var/E²=Θ(√n) bounds the UNIFORM point estimator,
  not the instance. On codex's exact islands instance, a **localized-probe importance-sampling
  estimator** recovers the lonely-fraction (occupancy moment Σ_cells 1[occ=1]) in **O(polylog) queries**,
  n-independent (verified: flat 200 queries for n=1024…65536, accuracy 0.95→1.00; full island
  contribution to ~1.3–1.5× in ~polylog; scripts `attack_loop/auditUB_*.py`). **Why:** hard-to-find
  low-mass structure must **TILE** the domain, so width-L probes find it in O(1/ε²); to CONCEAL it
  (Lemma-19 structure) you must scatter it, which **blows its MST contribution to Θ(n^{5/4})** (a
  trivially-distinguishable >100× signal, NOT a constant-factor pair) AND a polylog grid still sees most
  of it. So no √n MST lower bound survives from the lonely/islands structure. (Audit U-B,
  `round2_upper_auditUB.md`; raises o(√n)-exists confidence above codex's.)
- **U-P1 [2026-06-21] — MST-weight is NOT √n-hard (no reduction from cell-sampling).** The source's
  cell-sampling Ω(√n) lower bound (see [[U-B1]]) does NOT transfer to MST-weight estimation: its
  hardest instance (Lemma 19) is **1-D**, where w(MST) = x_max − x_min **telescopes and is invariant to
  cell occupancy** (verified numerically: uniform vs non-uniform instances have identical MST weight,
  ratio 1.000, despite a 9× gap in #non-empty cells). So a (1±ε)-MST estimator provably **cannot** solve
  cell sampling ⇒ MST-weight is not √n-hard via that route. The only proven MST floor remains
  Ω(n^{1/3}). ⇒ **the upper-bound pivot is alive** (Audit U-A, classification (β) DOOR OPEN). Source:
  `attack_loop/round1_upper_response.md` + `round1_upper_auditUA.md` (paper §4 verbatim + numerics).

## Refuted routes `N*` (this line)
- **U-N3 [2026-06-21] — "weight-relevant scale ⇒ c(λ)=O(n/λ)" is FALSE (codex Round-5 counterexample,
  verified).** Audit U-D's large-λ cost bound relied on this; it fails. **Counterexample:** uniform q×q
  grid (n=q²) with spacing d=2λ, λ=q/4=Θ(√n). Then nearest-neighbour = 2λ ⇒ **c(λ)=n** (all isolated),
  λ>n^{1/3}, and λ·c(λ)/n = λ = Θ(√n) ⇒ strongly weight-relevant (the band [0,λ] contributes
  ∫(c−1)=λ(n−1)=Θ(n^{3/2}) = a constant fraction of w(MST)=Θ(n^{3/2})). But c(λ)=n ≫ n/λ=Θ(√n) by a
  Θ(√n) factor. ⇒ the 2-axis estimator costs √(#nonempty cells)=√n here, NOT √(n/λ). **The large-λ
  branch as specified does NOT achieve Õ(n^{1/3}) in the DENSE regime (c(λ)≫n/λ).** Do NOT re-assert the
  c(λ)=O(n/λ) bound. *(NB: the uniform grid's WEIGHT is itself trivially estimable ~√(n·Area) by
  density — so this is likely another weight-red-herring needing a DENSE/density branch, [[U-OPEN]].)*
- **U-N1 [2026-06-21] — CRT-via-uniform-cell-sampling cannot beat √n.** Lowering the BFS depth t does
  NOT help: even with t=O(polylog), the CRT estimator still needs near-uniform non-empty-cell **seeds**
  and an estimate of **N_i = #non-empty cells**, both supplied by `CellSampling` which is Ω(√n)
  ([[U-B1]]). Do NOT re-attempt "tune t" or any estimator that calls near-uniform cell sampling.
- **U-N2 [2026-06-21] — "uniform point-sample + inverse-multiplicity reweight" is dead.** The unbiased
  estimator Z = n·β(v)/a_v has Var = Θ(n·M) on the hard instance (scale λ=√n: M=√n singleton cells +
  one bulk; c_i=Θ(M), OPT=Θ(n), allowed error Θ(M)), forcing q = Ω(n/M) = Ω(√n) samples. Verified
  numerically (Var ratio → 1.000). Do NOT re-attempt point-sampling-with-reweighting as the route.

## Proven results `P*` — Pro round 1 (verified at the checkable level; "AI-verified ≠ proved")
- **U-Pro1 [2026-06-21] — `U-N4` is REFUTED; cheap component-size + death-time MST-edge sampling EXIST
  (GPT-5.5-Pro round 1, numerically VERIFIED `attack_loop/webpro_verify_round1.py`).**
  - **Random-leader estimator:** assign random ranks; from p, explore p's scale-λ component in any
    fixed order, STOP at the first lower-ranked vertex; output 1 iff component exhausted. E=1/|C_λ(p)|,
    cost **O(log s)** expected (NOT s). ⇒ ĉ(λ) unbiased, Var≤n·c(λ)/k; on the contracted cell graph
    (paper Lemma 24) each trial = **Õ_ε(1) range queries** — the source CellSampling Ω(√n) is bypassed.
  - **Multiset identity (Lemma 1, exact):** `{τ(v):v≠r} = {MST edge weights}` for death times
    τ(v)=min bottleneck-dist to {r or lower-ranked} — VERIFIED exactly. ⇒ uniform vertex + bottleneck-
    Dijkstra (O(log n) expansions) = a **uniform random MST-edge weight** in Õ_ε(1) queries.
  - **Instance-sensitive bound (Thm):** Õ_ε(n/N_eff), N_eff=W²/Σℓ_e²; o(√n) iff N_eff=ω(√n);
    **Õ(n^{1/3})** when ℓ_max ≤ W/n^{2/3}. (Uses Var(Ŵ_H)≤(n/k)Σw_f² + the MST-minimizes-Σw² fact +
    WSPD (1+ε) distortion.) **A real partial upper bound.** (Audit `docs/webpro_round1_audit.md` checks
    the non-numerical parts: the variance theorem + the WSPD range-query implementation.)
- 🔴 **HONESTY CORRECTION:** our codex-derived **`U-N4` (below) was WRONG** — "exploring a component
  costs its size" is false (the random-leader trick is O(log s)). Several codex rounds over-invested in
  a non-obstruction. Lesson logged. (This is exactly the kind of AI-derived claim the owner flagged as
  possibly mistaken; Pro found the fix.)

## Barriers `B*` (this line)
- **~~U-N4~~ [2026-06-21] — REFUTED by [[U-Pro1]] (kept for the record).** We had claimed the crux was
  "cheap connectivity from counts" and that estimating |C_λ(p)| / c(λ) needs ω(polylog). **FALSE:** the
  random-leader / minimum-rank estimator does it in O(log s) per sample (the early-stop compensates the
  rare full exploration). The chains "counterexample" (n^{2/3} chains of length n^{1/3}) does NOT bite —
  you explore O(log) of a chain, not its length. **The real remaining crux is now the HEAVY-TAIL lemma**
  (geometric, well-posed): estimate the excess Σ_{e∈MST,w_e>L}(w_e−L) of the ≤n^{2/3} long MST edges
  above L=Θ(W/n^{2/3}) to additive εW in Õ(n^{1/3}) range queries — the death-time sampler misses the
  rare long edges (needs spatial range info, as the source's Õ(√n) uses). Open.
- **[carried] Ω(n^{1/3}) lower bound (Lemma 32) is a hard floor** — no algorithm can beat n^{1/3}; the
  best achievable is Õ(n^{1/3}). An algorithm claiming o(n^{1/3}) is WRONG — audits must check any
  claimed query count is ≥ n^{1/3}.
- **U-B1 [2026-06-21] — CellSampling is Ω(√n) (the real source bottleneck; CORRECTS the Round-1 brief).**
  arXiv:2504.15292 §4 proves **Ω(√n/c)** queries are needed to (a) draw a near-uniform non-empty
  λ-cell and (b) estimate N_i = #non-empty cells to O(1)-relative error — **even in 1-D** (Δ=n; Lemmas
  17–20, Algorithm 1, Cor 18; verified from the PDF by Audit U-A). The MST estimator (Thm 30 / §5.3)
  invokes it for both seeds and the n̂ scale factor, which is where its √n actually comes from (NOT the
  BFS depth t, as the Round-1 brief wrongly stated). 🔴 Any algorithm that estimates each N_i (or each
  c_i) to relative error inherits Ω(√n); a sub-√n algorithm must AVOID per-scale near-uniform cell
  sampling and instead estimate the *weighted aggregate* Σ_i λ_i c_i with cross-scale cancellation.

## The exact open problem, as currently posed (REFINED after Round 1)
Design an orthogonal range-counting-oracle algorithm that (1±ε)-estimates w(P) in **o(√n)** (ideally
**Õ(n^{1/3})**) queries, **without per-scale near-uniform cell sampling** (which is Ω(√n), [[U-B1]]).
The handle: w(MST) = (n−Δ) + Σ_i λ_i c_i needs only the *weighted aggregate* to ε·OPT — individual c_i
need NOT be relative-error accurate (the 1-D case is exactly 2 queries, [[U-P1]]). So estimate
Σ_i λ_i c_i directly, exploiting cross-scale cancellation + planar structure.

**[2026-06-21 UPDATE 2 after Round 3 — the FILAMENT obstruction].** codex Round 3 assembled the
stratified importance-sampling algorithm for all strata **conditional on a thickness lemma**, handled
the dense Lemma-32 stratum by scanning Θ(n^{1/3}) coarse cells — but **refuted the unconditional
concentration/tiling lemma** with the **filament instance**: N=√n singletons spaced λ=√n apart along a
*diagonal* (+ bulk). It contributes N·λ = Θ(n) persistence (constant fraction); consecutive islands are
only Θ(λ) apart so **no scatter-blowup** (it evades the [[U-P2]] vise — which only considered
2D-tile vs 2D-scatter, missing "tile a 1-D curve"); yet its λ-neighborhoods occupy N·λ² of an N²·λ²
region ⇒ a 2D localized λ-box probe hit-rate is only **Θ(1/√n)**. So 2D-area importance sampling
reverts to √n on filaments. **Proposed repair (codex, UNPROVEN): slab / axis-projection sampling** — a
thin structure with low 2-D area density may have high density in some 1-D axis projection or thin slab.
**OPEN crux:** does projection/slab sampling recover filament persistence in o(√n), OR is there a
filament that is sparse in 2-D area AND in BOTH axis projections (which would defeat the repair and
deepen the obstruction)? (codex could NOT run numerics this round — sandbox blocked Python — so the
filament + repair need independent numeric verification.)

**[2026-06-21 UPDATE 1 after the [[U-P2]] crack].** The Euler-totals route is dead (V,E,Z cancel:
filled k×k block has V=k², E=2k(k−1), Z=(k−1)² ⇒ c=1; occupancy totals ≠ connectivity). The LIVE
route is **stratified importance sampling exploiting the tile-or-blowup vise**:

> Σ_i λ_i c_i = total weighted "component persistence." Stratify components by mass/scale. For each
> stratum, by [[U-P2]] a stratum that contributes a constant fraction is either **coarsely
> countable** (it tiles ⇒ a polylog grid/probe estimates its density) or its **MST contribution is too
> large to hide** (concealing blows it up). So estimate each stratum's contribution by localized
> importance-sampling probes, never by near-uniform cell sampling. **The lonely (occ=1) stratum is
> verified estimable in O(polylog).** OPEN: (a) generalize the primitive to ALL component-persistence
> strata (small components of every size, not just singletons); (b) handle the **dense-block /
> n^{1/3} hidden-gadget** stratum (untouched by the lonely-fraction primitive — it is the genuine
> floor); (c) tighten the assembled estimator to **(1±ε)** (current full estimate is ~1.3–1.5×); (d)
> the total query bound — is it Õ(n^{1/3}), or some o(√n) between n^{1/3} and √n?

## Confidence trend (with dates)
- **[2026-06-21] opened:** ~30–40% that an improvement over Õ(√n) exists and is findable.
- **[2026-06-21] post Round-1 + Audit U-A:** ~35% o(√n) / ~15% Õ(n^{1/3}).
- **[2026-06-21] post Round-2 + Audit U-B:** ~50% o(√n) / ~20% Õ(n^{1/3}). Variance barrier broken
  ([[U-P2]]).
- **[2026-06-21] post Round-3 (filament obstruction):** ~45% o(√n); ~25% Õ(n^{1/3}).
- **[2026-06-21] post Audit U-C:** ~60% o(√n); ~35% Õ(n^{1/3}).
- **[2026-06-21] post Round-4 + Audit U-D:** ~80% o(√n); ~40% Õ(n^{1/3}).
- **[2026-06-21] post GPT-5.5-Pro round 2 (candidate full closure; 3 audits):** ~88% o(√n); ~72%
  Õ(n^{1/3}). **[SUPERSEDED — round 3 refuted the closure.]**
- **[2026-06-21] post round 3 (closure REFUTED; seed-reuse unsound, numerically confirmed):** **~82%
  o(√n) exists; ~40% the full Õ(n^{1/3}) exists+findable.** The round-1 instance-sensitive Õ(n/N_eff)
  (= Õ(n^{1/3}) for non-tail-heavy instances) is solid. The full closure needs the sharper Lemma 3
  (catch rare support components via spatial range-emptiness without Ω(√K) samples) — plausible but
  unproven; the heavy-tail difficulty recursed. 🔴 Honest note: 3 audits passed a closure that a 4th pass
  broke — "AI-verified ≠ proved" is not rhetorical; the multi-pass + numeric-confirmation discipline is
  what caught it.
- **[2026-06-21] post GPT-5.5-Pro round 1 (U-N4 refuted; instance-sensitive bound verified):** ~80%
  o(√n); ~55% Õ(n^{1/3}). Big positive update: an o(√n) algorithm for non-tail-heavy instances is
  essentially in hand (verified), and the remaining gap is a single, well-posed, GEOMETRIC heavy-tail
  lemma — far better than the (mistaken) U-N4 framing. Õ(n^{1/3}) now hinges on that one lemma; the rare
  long edges are a genuine but localized difficulty (≤n^{2/3} of them, geometrically "long"). Pending the
  round-1 audit (variance theorem + WSPD impl) and a round-2 attack on the heavy-tail lemma.
- **[2026-06-21] post Round-6 (codex; reduced to the now-REFUTED U-N4 primitive):** ~55% o(√n); ~30%
  Õ(n^{1/3}). (Superseded — U-N4 was wrong.) The cost model is now a proven conditional theorem ([[U-P5]]) — real progress, the whole
  problem is ONE clean primitive. But that primitive ([[U-N4]], cheap connectivity from counts) is the
  genuine crux and codex-xhigh plateaued on it over 6 rounds. o(√n) is slightly below even odds: the LB
  barrier + the weight-red-herring pattern suggest the truth is Θ(n^{1/3}), but U-N4 has the same flavour
  as the cell-sampling Ω(√n) — it could genuinely be √n-hard, in which case the truth is Θ̃(√n).
- **[2026-06-21] post Round-5 (dense-regime counterexample [[U-N3]]):** ~65% o(√n); ~30% Õ(n^{1/3}).
  Lowered: codex refuted U-D's load-bearing "c(λ)=O(n/λ)" step with a clean uniform-grid counterexample;
  the large-λ DENSE regime is a real, unproven gap. The o(√n) thesis plausibly survives (dense/uniform
  weight is density-estimable — a 4th red-herring) but the clean (1±ε) proof keeps revealing new regimes
  (a signature of a genuinely hard open problem, consistent with Driemel et al. leaving it open). At the
  §9.1 escalation juncture: web-Pro vs more codex vs consolidate vs handoff — human decision.

## Cross-reference
- LOWER-bound line (frozen, refuted): `research_line_emst.md` (P1/P2/N1/N2/B4; the n^{1/3} cap).
- Per-round artifacts: `attack_loop/roundN_upper_*` (briefs / responses / audits).
