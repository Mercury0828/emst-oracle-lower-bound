# Round 2 — Independent adversarial audit B: the PROBABILISTIC accounting

> Fresh-context, adversarial audit of `docs/webpro_round2_response.md` (GPT-5.5-Pro's CLAIMED
> closure to unconditional Õ_ε(n^{1/3})). Scope assigned: the **probabilistic accounting** —
> seed-reuse trick (§4/§8), clipped death-time variance (§5), the B̂_L = Ŵ_Q − Â_Q subtraction
> (§6), the W-search stopping rule (§7), and K_h estimation (§1). Auditor = Claude (Opus 4.8, 1M).
> Verifier = `sim/emst.py` (exact EMST) + the venv. New probes:
> `attack_loop/auditB2_reuse.py`, `auditB2_reuse2.py`, `auditB2_unionbound.py`, `auditB2_pipeline.py`.
> Treated as established (per brief): Lemmas 1–2, snapping preserves B_L, round-1 death-time/multiset
> identity + random-leader estimator. External facts checked: Czumaj et al. uses **range + cone-NN**
> queries at Õ(√n); the CRT components estimator runs in time **independent of #vertices** (O(d·w·ε⁻²·log)).

---

## VERDICT SUMMARY

**Overall: the probabilistic accounting is SOUND, with one GAP that is shared with (and contained
in) the already-flagged Lemma-3 spatial step, plus two MINOR presentation hazards.** I found **no
fatal probabilistic error**. The decisive seed-reuse claim is **correct**, but for a reason more
subtle than the §4 one-liner states, and the §4 wording ("for any fixed threshold the samples are
i.i.d. uniform ⇒ original concentration applies; … by union bound; cross-threshold independence
unnecessary") is *true but not self-sufficient* — it needs the clipping/relative-accuracy structure
of §5–§6 to be the thing that actually controls the SUM. I verify that structure holds.

Per target:
- **#1 Seed-reuse (the crux): VALID — GAP (contained), confidence 0.82.** Reuse genuinely avoids the
  n^{2/3} blowup AND keeps (1±ε) of the summed estimator — but *only because* the summed quantity is
  estimated via clipping (§5) + a proper relative-accuracy Czumaj estimator (§6/Lemma 3), NOT by
  naively integrating reused-seed survival counts (which I show blows up). The residual risk is
  entirely inside Lemma 3 (whether Czumaj's √K spatial cost survives the cone-NN→WSPD swap), which
  is out of this audit's scope and is Pro's own 0.84-confidence item.
- **#2 Clipped death-time variance: VALID, confidence 0.97.** Algebra correct; `X²≤LX` holds; the
  O(1) dimensionless ratio needs K=Θ(K₀) (the support), which is the intended regime. Additive ηG,
  not relative. Numerically confirmed.
- **#3 Subtraction B̂_L = Ŵ_Q − Â_Q: VALID, confidence 0.95.** Sound precisely because the target is
  additive εW (not relative to B_L). Errors are additive-in-W and do not amplify.
- **#4 W-search stopping rule: VALID, confidence 0.96.** Arithmetic checks out; boosting keeps Õ(n^{1/3}).
- **#5 K_h estimation: VALID, confidence 0.95.** Unbiased Bernoulli, Var ≤ E[Z]=K_h/n, Õ(n/K₀) over
  levels. Numerically confirmed unbiased.

---

## #1 — THE SEED-REUSE TRICK (§4 "Reusing the vertex seeds" + §8) — **VALID, with a contained GAP**

### (a) Does Czumaj's estimator need √K *independent uniform vertices*, or O_η(1) seeds + √K local ops?

**Answer: O_η(1) (polylog) uniform vertices per threshold; the √K cost is local/spatial. Pro's
claim (a) is structurally correct.**

The Czumaj–Sohler EMST estimator writes w(MST(Q)) via the number-of-connected-components counts
c⁽ⁱ⁾ at a geometric ladder of thresholds, and estimates each c⁽ⁱ⁾ with the **Chazelle–Rubinfeld–
Trevisan (CRT)** estimator. The published CRT result is decisive here: its running time is
`O(d·w·ε⁻²·log(dw/ε))` and **does not depend on the number of vertices** (verified externally;
SIAM J. Comput. 34(6):1370–1379). Concretely CRT draws `r = O(ε⁻²·log)` *independent uniform
vertices per threshold* — a count independent of K — and from each runs a **bounded** local BFS.
So the *number of uniform vertex draws* is O_η(1) per threshold, NOT √K.

Where does √K come from in the *geometric* version? From two places, both non-sampling: (i) the
adaptive spatial subdivision into O_η(√K) active blocks/block-components, and (ii) the per-vertex
local-exploration cost (in Czumaj: cone-NN queries; in Pro: WSPD-adjacency range-emptiness probes).
At the *tail* levels where c⁽ⁱ⁾=O(1), a general-graph CRT would cost ~K/c⁽ⁱ⁾=Ω(K) uniform samples;
Czumaj beats this to Õ(√K) **purely by spatial structure**, never by uniform sampling. Therefore the
expensive primitive — drawing one *uniform support vertex*, which costs n/K via rejection sampling
(§2) — is invoked only O_η(polylog) times total, while all √K work is range-emptiness/adjacency on
already-revealed structure. Reuse cannot fail "because the estimator needs √K independent vertices,"
because it provably does not need them.

This is the genuine content of §8: K=n^{2/3} balances √K = n/K = n^{1/3}, and the danger (√K
independent support draws ⇒ √K·(n/K)=n^{2/3}) is averted because the √K is spatial, not sampled.
**I accept (a).** The only residual risk is whether the cone-NN→WSPD swap preserves Czumaj's √K
bound — that is Lemma 3, explicitly out of this audit's scope (Pro self-rates it 0.84).

### (b) Is "per-threshold marginal i.i.d. + union bound" a VALID substitute for cross-threshold independence, given the final estimate SUMS over thresholds with the SAME seeds?

**This is the decisive question, and the honest answer is: the §4 one-liner is TRUE but INSUFFICIENT
on its own; it is rescued by the clipping/relative-accuracy structure of §5–§6. The closure does not
actually rely on naively summing reused-seed survival counts, so it survives — but the §4 wording
hides the real reason.** Confidence 0.82.

I make the probabilistic statement precise and test it.

**Two notions of "correct," and the proof needs the right one.**

- *(I) Per-threshold w.h.p. correctness via union bound.* For each fixed t, the reused-seed estimate
  ĉ(t) is, marginally, the same i.i.d.-uniform-seed estimator as with fresh seeds (TRUE: a fixed t
  only sees the marginal law of the s seeds, which is i.i.d. Unif(Q) regardless of reuse). Boost to
  failure prob ≤ 1/(10T) (median-of-O(log T)); union bound ⇒ ALL t simultaneously good w.p. ≥ 0.9.
  This needs NO cross-threshold independence. This is exactly Pro's §4 claim, and it is **correct**.

- *(II) Variance of the SUM.* The final answer integrates/sums over thresholds:
  Ŝ = Σ_t ĉ(t)·dt. With reused seeds, Cov(ĉ(t),ĉ(t′)) > 0, so
  Var[Ŝ] = Σ_{t,t′} Cov·dt·dt′ can be inflated by up to a factor T vs fresh seeds.

**The trap.** Framing (I) gives only an L¹/worst-case additive bound: simultaneous goodness ⇒
|Ŝ − S| ≤ Σ_t err(t)·dt. The per-threshold additive errors **do not cancel** — they add. On a
heavy-tailed instance this non-cancelling sum can be ≫ εW even though every ĉ(t) is individually
accurate. So **(I) alone does NOT certify (1±ε) of the SUM.** This is a real and easy mistake, and
the §4 sentence "cross-threshold independence unnecessary" is precisely the sentence that *could*
license that mistake.

**Numerical demonstration that the naive reused-seed SUM blows up** (`auditB2_unionbound.py`, Pro's
own serpentine+islands adversary, support K≈458–908):

| metric | REUSE (r seeds) | FRESH (r seeds × T thresholds) |
|---|---|---|
| max_t |ĉ(t)−c(t)|/(K−1) (the union-bound L∞ quantity) | **0.019** (better) | 0.037 |
| SUM error /W (raw ladder integral) | **0.58** | 0.23 |
| SUM std /W | 0.78 | 0.30 |
| Var(SUM) ratio reuse/fresh | **≈ 7–8×** | 1 |

Two facts jump out: (1) reuse is *no worse, even better,* on the per-threshold L∞ object — so
framing (I) is genuinely satisfied by reuse; (2) the **raw summed/integrated** estimator's variance
is ~7–8× larger under reuse and is *large in absolute terms for both* (≥0.23W). The blowup is the
telescoping identity: for a single seed, ∫₀^∞ 1[τ(q)>t] dt = τ(q) exactly (verified to <0.01 error,
`auditB2_reuse2.py`), so integrating reused-seed survival counts collapses to the **raw death-time
estimator (K/s)Στ(q_j)**, whose variance is dominated by the heavy tail — precisely round-1's
already-known obstruction (one heavy value among K; needs Ω(K) samples).

**Why the closure nevertheless survives.** Pro's actual pipeline (§5–§6) does **not** integrate raw
reused-seed survival counts. It:
- **§5 CLIPS at L:** X = min{τ,L}, estimating A_L(Q)=Σ min{w_e,L}. Clipping caps each contribution at
  L, killing the heavy-tail variance. `auditB2_pipeline.py` (support K≈758–1508): additive
  |ΔA_L|/W = **0.002–0.006 at only s=16 support samples**, std/W ≤ 0.01 — and the §5 bound
  K²·L·E[X]/s safely upper-bounds it. The heavy tail does **not** blow up the clipped estimator.
- **§6 estimates W_Q by a PROPER (1±η)-relative Czumaj estimator (Lemma 3)**, not by the naive
  reused-seed integral. Czumaj's estimator targets each c⁽ⁱ⁾ to *relative* accuracy η (so the
  weighted sum inherits *relative* error η, with cancellation/relative-budget structure), and pays
  the heavy-tail level spatially in Õ(√K). Then B̂_L = Ŵ_Q − Â_Q.

So the "T thresholds with reused seeds" live **inside** (i) Lemma 3's internal CRT ladder, where each
level is estimated to *relative* accuracy and the reused O_η(1)-vertex pool only serves the cheap
many-component levels (the tail is spatial), and (ii) the W-search ladder of §7, each guess
individually additive-accurate. In neither place is the final number a naive non-cancelling sum of
reused-seed survival counts. **Conclusion: reuse avoids the n^{2/3} blowup (a) AND keeps (1±ε) of the
summed estimator (b) — but the load-bearing reason is the clipping + relative-accuracy structure of
§5–§6, NOT the bare union-bound sentence in §4.** The §4 argument as literally written is incomplete;
the surrounding sections supply what it omits.

**Residual GAP (contained, not fatal).** The one place the SUM-variance issue could still bite is
*inside* Lemma 3: if the WSPD-swapped Czumaj estimator did not in fact achieve per-level *relative*
accuracy with O_η(1) reused vertices + Õ(√K) spatial work — i.e., if the tail level secretly needed
many uniform support vertices — then reuse would not save it. That is exactly Pro's self-flagged
Lemma-3 item (confidence 0.84) and is out of this audit's scope. **The probabilistic accounting is
sound conditional on Lemma 3.**

**Classification: GAP (contained in Lemma 3), not FATAL. Confidence 0.82.**

---

## #2 — CLIPPED DEATH-TIME VARIANCE (§5) — **VALID**

The chain X=min{τ,L}; X²≤LX ⇒ E[X²]≤L·E[X] ⇒ Var[(K/s)ΣX] ≤ (K²/s)·E[X²] ≤ K²·L·E[X]/s. Since
K·E[X]=A_L(H_Q)=W_{H_Q} (multiset identity, clipped), this is **K·L·W_{H_Q}/s**. ✓ algebra correct.

Dimensionless check: with K=O(K₀), L=G/K₀, W_{H_Q}=O(G): K·L·W_{H_Q}/G² = O(K₀·(G/K₀)·G/G²)=O(1).
**Numerically confirmed** (`auditB2_reuse2.py`): the O(1) requires K=Θ(K₀)=n^{2/3} (the SUPPORT, not
the full n-point set). With K₀=n^{2/3}: K₀·L/W = **1.000** exactly. With K~n it would be ~10×;
Pro applies it to the support where K=Θ(n^{2/3}), so the regime is correct. ✓

`X²≤LX` verified pointwise (E[X²]=218.89 ≤ L·E[X]=522.50; 407.28 ≤ 664.40; etc., all instances). The
result is **additive ηG** (Var ≤ η²G² ⇒ std ≤ ηG), not relative — confirmed: additive |ΔA_L|/W ≈
0.002–0.006 at small s, and O_ε(η⁻²) samples suffice. **VALID, confidence 0.97.**

---

## #3 — THE SUBTRACTION B̂_L = Ŵ_Q − Â_Q (§6) — **VALID**

B_L(Q)=W_Q−A_L(Q); both Ŵ_Q and Â_Q are ~W-sized with additive error O(ηW), and B_L may be ≪ W.
Subtracting two large noisy estimates to get a small one is **sound here because the target is
additive εW, not relative to B_L** — confirmed against the brief's heavy-tail lemma ("additive error
ε·W"). Error: |B̂_L−B_L| ≤ |Ŵ_Q−W_Q|+|Â_Q−A_L| ≤ O(ηW); choose η=Θ(ε). The errors are additive-in-W
and do not amplify under subtraction (no division by a small B_L). This feeds the final
W=A_L(P)+B_L(P) where additive εW on each half gives (1±ε)W. **VALID, confidence 0.95.** (Minor note:
the standard "estimate both halves to εW/2" decomposition; nothing exotic.)

---

## #4 — THE W-SEARCH (§7, Lemma 4 + geometric search) — **VALID**

Given |Ŵ_G−W| ≤ G/64 (accuracy 1/64), descend G=U,U/2,…, stop at first Ŵ_G ≥ G/16.
- G ≥ 32W: Ŵ_G ≤ W+G/64 ≤ G/32+G/64 = 3G/64 < 4G/64 = G/16 ⇒ **continue**. ✓
- G ∈ [W,2W): Ŵ_G ≥ W−G/64 > G/2−G/64 = 31G/64 > G/16 ⇒ **stop** (before testing below W). ✓

So the loop provably continues while G≥32W and provably stops once G<2W, hence stops at G₀∈[2W,32W),
giving W ≤ G₀ < 32W. ✓ The final run uses G₀ with accuracy εG₀/64 ⇒ additive ≤ εG₀/64 < εW/2 (since
G₀<32W… more precisely additive ε·G₀/64 ≤ ε·(32W)/64 = εW/2). ✓ U=√2(n−1)Δ ≥ W and W≥n−1 (distinct
integer points), Δ=O(n) ⇒ O(log n) guesses; boosting each to failure prob 1/(10 log n) keeps all
simultaneously correct and total Õ(n^{1/3})·O(log n)=Õ(n^{1/3}). **VALID, confidence 0.96.**

---

## #5 — K_h ESTIMATION (§1) — **VALID**

Bernoulli Z=1[U<1/m_h(p)] for uniform p∈P: E[Z]=Σ_p (1/n)(1/m(p))=Σ_C (m(C)/n)(1/m(C))=K_h/n.
**Numerically confirmed unbiased**: h=20 gives Ê[Z]=0.49861 vs K_h/n=0.49875; h=60 gives 0.07197 vs
0.07225; and Var(Z) ≤ E[Z]=K_h/n in both (Bernoulli). Distinguishing K_h~cK₀ from K₀ to constant
relative gap needs O((n/K₀)·log) trials (relative concentration of a Bernoulli mean of size ~K₀/n);
over O(log Δ) levels, union bound, still Õ(n/K₀)=Õ(n^{1/3}). The level search is monotone
(K_{h/2}≤4K_h, Lemma 1) so a clean crossing K_h∈[cK₀,C_ε K₀] exists. No failure-probability subtlety
beyond the standard union bound over O(log Δ) levels (each boosted). **VALID, confidence 0.95.**

---

## THE DECISIVE QUESTION — answered

**Does the seed-reuse genuinely avoid the n^{2/3} blowup while keeping (1±ε) correctness of the
SUMMED estimator? — YES, conditional on Lemma 3.**

- It avoids n^{2/3}: the expensive primitive (uniform support sample, cost n/K) is invoked only
  O_η(polylog) times because the CRT components estimator needs O_η(1) uniform vertices per threshold
  (verified: CRT cost is vertex-count-independent), and the √K cost is purely spatial range-emptiness/
  WSPD-adjacency work — for which reuse of the same revealed support is exactly the right object.
- It keeps (1±ε) of the SUM: **but not via the bare §4 union-bound argument.** I show numerically that
  naively integrating reused-seed survival counts collapses to the raw death-time estimator and
  blows up ~7–8× on the heavy tail (the round-1 obstruction). The closure survives because §5 **clips**
  (killing tail variance, additive ηW with O(η⁻²) support samples — verified) and §6 uses a **proper
  relative-accuracy** Czumaj estimator + subtraction (additive εW — sound). The §4 sentence
  "cross-threshold independence unnecessary" is *true for per-threshold correctness* but is **not by
  itself** what makes the SUM (1±ε); the clipping/relative structure is. This is a presentation GAP,
  not a mathematical error.

**The only place a genuine probabilistic failure could still hide is inside Lemma 3** (whether the
cone-NN→WSPD-swapped Czumaj estimator truly delivers per-level relative accuracy with O_η(1) reused
uniform vertices + Õ(√K) spatial ops). That is Pro's own lowest-confidence item (0.84) and is out of
this audit's scope.

## OVERALL VERDICT

**The closure's PROBABILISTIC accounting is SOUND (has at most a fixable presentation GAP, not a fatal
error), conditional on the unaudited spatial Lemma 3.** Targets #2–#5 are clean VALID. Target #1 is
VALID with a contained GAP: the seed-reuse mechanism is real and the exponent saving is genuine, but
the §4 justification is under-stated and the (1±ε)-of-the-SUM property is actually delivered by the
clipping (§5) and relative-accuracy/subtraction (§6) machinery — which I verified holds. No smuggled
n^{2/3} or √n found in the probabilistic steps.

**Confidence that the probabilistic accounting is sound (given Lemma 3): 0.85.**
**Confidence in the complete unconditional Õ_ε(n^{1/3}) theorem: gated by Lemma 3 (≈0.84, Pro's own),
not by anything in this audit's scope.**

### Recommended repair (cheap, non-fatal)
Rewrite §4's reuse paragraph to state explicitly: *the summed estimate is NOT a naive integral of
reused-seed survival counts (which would inherit Var(τ) and the heavy-tail blowup); reuse serves only
(i) the cheap many-component CRT levels inside Lemma 3, each estimated to relative accuracy η, and
(ii) the W-search ladder, each guess additive-accurate; the heavy tail is handled by clipping (§5) +
the spatial Õ(√K) estimator (§6), not by summing uniform-seed samples.* Add one line noting that
per-threshold union-bound correctness (framing I) is necessary but not sufficient for the SUM, and
cite §5/§6 as supplying the sufficiency.
