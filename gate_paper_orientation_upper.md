# Gate — Paper-Orientation Check (Upper-Bound Pivot)

**Role:** independent, fresh-context referee (SODA PC member spirit). **Date:** 2026-06-21.
**Mandate:** judge HONESTLY whether the current contribution is SODA-level as a standalone paper.
Not a rubber-stamp; not defeatist. Evidence read: `research_line_emst.md`, `research_line_emst_upper.md`,
`gate1_paper_orientation_audit.md`, and the round-by-round briefs/responses/audits in `attack_loop/`
(esp. `round2_auditC.md`, `round4_upper_auditUD.md`, `round6_upper_brief.md`, `round6_upper_response.md`).
**Caveat that colors everything below:** all results are AI-attacker + AI-audit; "AI-verified ≠ proved";
human verification pending. A PC reads the *claimed theorems*, but a referee discounts unproven internals.

---

## VERDICT (a): **NO** — not SODA-level as a standalone paper right now. (Borderline-NO; a clear ESA/workshop note today.)

This is a "NO for SODA *now*" with a genuinely promising core, not a "this is junk." Be precise about *why*.

### The package = three pieces; weigh each against the SODA bar.

**Piece 1 — the lower-bound BARRIER (P1/P2): "gadget-packing can't beat n^{1/3}".**
This is the weakest piece *as a SODA contribution*, for one structural reason the prompt already flags:
**the source (Driemel et al.) already achieved Ω(n^{1/3}) by exactly this gadget-packing technique.** A
barrier that says "the technique that gives the *known* bound cannot give more" is not surprising — it is
close to the default expectation. SODA-grade barrier results (natural proofs, the 3SUM/APSP fine-grained
web, communication-complexity barriers for data structures) earn their keep by ruling out a *broad and
genuinely tempting* class of approaches to a problem where people had real hope. Here:
  - The barrier is honestly labeled **NEAR-proof-of-death, not a proof** (Audit C). The one surviving
    loophole (the "new primitive," Step 6) is open and *evidence-against*, but un-closed. A PC will not
    credit a barrier whose own authors say a fully-general version *cannot* hold (it is barred by the
    existing Ω(n^{1/3})).
  - It rules out a *natural-for-this-problem* technique but not a *recognized-hard-open* class. The scope
    is "single-needle + multi-needle gadget packing with O(1)-coverage," which is essentially "the source's
    own method, pushed." That is a useful *internal* negative result; it is not a standalone surprising
    barrier.
  - Net: a solid **§ of a paper / a clarifying lemma**, not a headline. Worth ~half a page of a real paper.

**Piece 2 — the CONDITIONAL UPPER BOUND (U-P5): Õ(n^{1/3}) IF the component-size primitive is polylog.**
This is the strongest-looking piece and the cleanest writing. The reduction is genuinely nice:
`w(MST) = (n−Δ) + ∫(c(t)−1)dt`, the scalar cluster-count framing (U-P4) that kills the false per-bucket
lemma, and the `min(Õ(n/c), Õ(√c)) ≤ Õ(n^{1/3})` cost model peaking at `c=n^{2/3}`. If the cost model
and all-regime handling survive human proof, this is a real, quotable reduction.
  - **But the condition IS the crux.** This is the decisive SODA objection. U-N4 — "estimate single-linkage
    component size / connectivity from additive range counts in polylog" — is not a *clean side-assumption*
    (like "assume SETH" or "assume an oblivious adversary"); it is **essentially the entire difficulty of
    the open problem**, restated. Round 6's own response is blunt: the naive primitives provably fail (box
    counts give local degree, singleton-tests are biased, 2-axis counts give support not component count),
    and chain-exploration costs `n^{2/3}` on the `n^{2/3}×n^{1/3}` instance. A conditional theorem whose
    hypothesis is "assume we can do the one thing nobody knows how to do" is, for SODA, a **problem
    reduction**, not a result. It is valuable as *orientation* — it tells the community exactly where the
    hardness concentrates — but a PC will read it as "they reduced the open problem to a slightly more
    specific open problem," which is below the bar for a top-tier *algorithms* venue that "wants new PROVEN
    theorems/bounds."
  - For a conditional result to clear SODA, the condition should be *interesting and independently
    plausible/standard*, and the *reduction itself* should be the contribution (fine-grained complexity does
    this well). Here the reduction is clean but short, and the condition is the crux — the worst case for the
    "conditional" framing.

**Piece 3 — the OPEN CRUX (U-N4) + numerics + the "weight-red-herring" pattern.**
This is genuinely the most *scientifically* interesting content (the repeated pattern that several
sub-problems are √n-hard but don't make the *weight* hard is a real insight, and the cluster-count integral
is the right lens). But it is, by definition, **the unresolved part.** Strong numerical evidence that the
truth is "plausibly Θ(n^{1/3})" is not a theorem; SODA does not accept "we have simulations and a clean
conjecture about where the gap closes."

### Why the sum is still < SODA.
A barrier that reproduces the known bound + a reduction whose hypothesis is the crux + numerics ≈ a
**well-orientated problem study with two partial structural results**. It honestly *maps* the open problem
better than the source did (the cluster-count integral + the min-cost model + the "connectivity-from-counts"
isolation of the crux is real intellectual progress). But it does not *move a proven number*: the proven
frontier is still Ω(n^{1/3}) (theirs, a barrier on a technique) and Õ(√n) (the source's, unimproved). **No
unconditional bound changed.** SODA's unsentimental read: "you neither improved the upper bound nor the
lower bound; you have a barrier on one technique and a conditional algorithm whose condition is the open
problem." That is a NO for SODA, today.

---

## (b) MINIMAL additional result that makes it clearly SODA-level.

Any ONE of the following, *proven* (human-level, not AI-audited):

1. **Resolve U-N4 positively** → an unconditional **Õ(n^{1/3})** (or any proven **o(√n)**) range-counting
   algorithm for (1±ε)-EMST-weight. This **closes (or narrows) the Driemel et al. gap from above** and is
   an instant, clean, headline SODA/SoCG result. This is the whole ballgame; everything else in the repo is
   scaffolding for it. (Even a proven `Õ(n^{1/3+δ})` or `Õ(n^{0.45})` unconditional would likely clear the
   bar as "first sub-√n.")

2. **Resolve U-N4 negatively** → a proven **Ω(√n)** range-counting lower bound for the component-size /
   connectivity primitive *that lifts to the EMST-weight problem itself* (i.e., shows the truth is **Θ̃(√n)**,
   closing the gap from below). A genuine new Ω(√n) for the *weight* (not just the sub-primitive) would be a
   strong SODA result — but note the project's own P1/P2 + numerics are *evidence against* this, so this is
   the less likely door.

3. **A different conditional/barrier with a clean, recognized condition** — e.g., prove EMST-weight under
   range-counting is **hard-under-a-standard-assumption** (a real reduction from a recognized problem), or
   prove a barrier that rules out a *broad, not-just-the-source's* class. The current barrier is too narrow
   for this on its own.

Bluntly: **(1) is the target the whole project is built toward, and it is the minimal clearly-SODA result.**
Until U-N4 falls in some direction with a human proof, the contribution is sub-threshold.

---

## (c) Is there an honest framing under which the CURRENT material is already a real (weaker) paper?

**Yes — at the ESA / SoCG-short / workshop tier, NOT SODA-main.** Honest headline:

> **"On the range-counting query complexity of Euclidean MST weight: a min-cost reduction, a
> gadget-packing barrier, and the connectivity-from-counts crux."**

What such a paper would honestly claim, and where it fits:
  - **Tier: ESA / SoCG (as a borderline/short contribution), or a strong workshop/CCCG, or arXiv.** The
    cluster-count integral + min(n/c, √c) cost model is a clean, reusable framing; the "weight-red-herring"
    phenomenon (sub-problems √n-hard but weight not) is a genuine, citable observation; the barrier is a
    legitimate (if unsurprising) technique-limitation. SoCG/ESA reviewers are more receptive than SODA to a
    well-structured *problem study* that reduces a recognized open gap to a single crisp primitive and
    proves the surrounding cost model — provided the framing is honest that the crux is open.
  - **Honest headline must NOT say "we close/narrow the gap."** It must say "we reduce the open gap to a
    single primitive (connectivity-from-counts), prove the conditional algorithm and a matching cost model,
    and show the natural lower-bound technique cannot beat n^{1/3}." That is a true and respectable, if
    modest, contribution.
  - **Even this tier requires human-verified proofs first.** The cluster-count integral (claimed verified to
    ratio 1.0001) and the P1 `O(s√p)` cap are the load-bearing lemmas; they must be actually proved. The
    cost model's "adaptive branch selection never invokes a √n estimate" must be a theorem, not a numeric.

So: **a real ESA/SoCG-tier note exists in this material today (modulo human proof); a SODA-main paper does
not, yet.**

---

## (d) Drift / over-claim risk in current framing.

Several, and they matter because the gate-1 audit *already* flagged the project's tendency to read sim
evidence one notch too generously. Watch list:

1. **"Conditional THEOREM (clean)" overstates U-P5.** The ledger's HEADLINE calls U-P5 a proven conditional
   theorem and says "the COST MODEL is PROVEN." But Round 6's *own* response says it "cannot honestly return
   the claimed theorem as proved" (80% there is a real implementability gap), and the sparse branch *also*
   lacks a proved primitive ("small c(λ) does not imply only O(c(λ)) nonempty cells"). The honest status is
   "conditional reduction with a numerically-supported cost model, modulo two un-implemented primitives,"
   not "the cost model is PROVEN." **Risk: the word "PROVEN" hardening into a claim the internals don't
   support.** Calling the hypothesis a "clean condition" is itself drift — it is the crux, not clean.

2. **The barrier P1/P2 phrased as near-"impossibility."** It is honestly hedged as NEAR-proof-of-death in
   Audit C, but the ledger HEADLINE ("the entire gadget-packing LB approach is (near-)refuted ... provably
   cap at n^{1/3}") risks being quoted as a clean impossibility. The surviving Step-6 loophole means it is
   *not* a theorem ruling out the technique; it is "every constructive variant we tried is dead, and the
   only escape is evidence-against." A referee will catch any over-statement here immediately.

3. **Numerics framed as near-proofs.** "Verified ratio 1.0001," "flat to n=10^9," etc. are *cost-model and
   identity sanity checks over a simulated oracle*, not proofs of the (1±ε) variance/error-budget or the
   hitting/coupling lemmas. The repo is mostly careful to label these as evidence, but the HEADLINE-level
   confidence numbers ("o(√n) ~55%, Õ(n^{1/3}) ~30%") can read as more banked than they are. (Gate-1
   already caught one such case: the "slope ≈0.53 / √m" grid-coverage figure was an under-powered-adversary
   artifact.)

4. **Repo/name + contribution drift (process).** The repo is named `emst-oracle-lower-bound` while the live
   contribution is an *upper*-bound pivot; the ledger flags the own-work dedup loop was not re-closed after
   the lower→upper switch (`scripts/own_work_corpus.py` absent). Minor, but a real gate item: confirm no
   overlap with prior own-works and re-run the scoop scan before any submission.

5. **"Equally SODA-worthy pivot" framing.** The lower-bound ledger calls the upper-bound pivot "a different
   but equally publishable SODA result." That is only true *if U-N4 is resolved*. As currently standing
   (conditional + barrier + numerics), it is **not** equally SODA-worthy — it is sub-threshold. The framing
   should not pre-suppose the SODA outcome the project has not yet earned.

---

## Bottom line for the owner

- **(a) NO** for SODA-main as a standalone paper *today*. The barrier reproduces the known bound (not
  surprising); the conditional upper bound's condition IS the open problem (a reduction, not a result); no
  unconditional bound moved. Package = a well-oriented problem study + two partial structural results.
- **(b)** Resolve **U-N4** (preferably positively → unconditional o(√n)/Õ(n^{1/3}), closing the gap from
  above) with a *human* proof. That single result is clearly SODA-level and is exactly what the whole
  project is scaffolding.
- **(c)** **Yes, at ESA / SoCG-short / workshop tier** (modulo human-verified proofs), honest headline:
  "reduce the recognized open gap to the connectivity-from-counts primitive + a proven min-cost reduction +
  a gadget-packing barrier." Must NOT claim to close/narrow the gap.
- **(d)** Main risks: "PROVEN cost model" / "clean conditional theorem" (Round 6 itself says unproved with
  an implementability gap), the near-impossibility phrasing of the barrier, numerics read as proofs, and the
  "equally SODA-worthy" pre-supposition. Tighten all four before any external framing.

**One-line referee summary:** *A genuinely insightful map of where the EMST-counting-oracle gap concentrates
— the connectivity-from-counts crux — but a map of the open problem is not a solution to it; come back when
U-N4 is proved in either direction.*
