# Round-2 Audit A — Lemma 3 (component-restricted WSPD inside Czumaj's active-block decomposition)

Auditor: independent adversarial reviewer (fresh context). Target: **Lemma 3** of
`docs/webpro_round2_response.md` (Pro's self-confidence 0.84 — the least-verified, most load-bearing
step). Ground-truth sources read in full from the actual PDFs (text extracted with `pypdf` into
`docs/_extract/{source_2504,czumaj}.txt`), not from a summarizer.

## VERDICT: **NEEDS-REPAIR** (one GAP that is repairable, one MINOR mis-citation, plus one
accounting subtlety that survives scrutiny). **Not FLAWED-FATAL**, but **not as-written valid** either.

Confidence in this verdict: **0.78**.

Net: Lemma 3 *can* be made to deliver Õ_η(√K + n/K) range-COUNTING queries, but **as written it
imports the wrong engine and mis-describes the cost ownership.** The honest construction does **not**
need Czumaj [2] at all — the source paper [1] (Driemel–Monemizadeh–Oh–Staals–Woodruff, SoCG'25)
*already* proves the exact thing Pro is trying to rebuild, and proves it *natively* in the
orthogonal-range-COUNTING model. Pro's detour through Czumaj's Yao-graph algorithm introduces a
**non-orthogonal-oracle dependence (cone-approximate-nearest-neighbour queries)** that Pro then has to
"replace," and the replacement is exactly [1]'s Theorem 30. So the substance is salvageable, but the
proof as phrased contains a real gap and an unnecessary, error-prone import.

---

## 1. What Czumaj et al. [2] actually is, and in what oracle model (Pro's Q1)

Fetched `Czumaj-EFMNRS.pdf` and read the structural prose (the math glyphs are garbled by the 2004
PDF encoding, but the algorithm description, theorem statements, and oracle list are legible).

**Oracle model (their §2.1, verbatim list):** their spread-independent (3rd) algorithm assumes access to
1. a **minimal bounding-cube oracle**,
2. an **orthogonal range *emptiness* oracle** ("tests if [a cube] contains a point" — emptiness, not
   counting), and
3. a **cone (1+δ)-approximate-nearest-neighbour oracle** (given point p and cone W, returns a
   (1+δ)-approx NN of p inside p+W), plus implicit uniform point sampling.

**Cost:** `Õ(√N · poly(1/ε))` *time/queries*, where N is the number of points, **spread-independent**
(this is the headline of their 3rd algorithm). It is a **(1±ε) multiplicative** estimate of the EMST
**weight**. ✔ (Pro's "√N", "(1±η)-multiplicative", and "spread-independent" claims about [2] are
faithful.)

**3-stage structure (their §6) — Pro's description is essentially faithful but the cost ownership is
mislabelled:**
- §6.1 **Partition the bounding cube into active blocks** by iterated 2^d-way subdivision, keeping only
  non-empty blocks, stopping at a level where #active-blocks ≤ B* = Θ̃(√N·…) or block side ≤ ε. Group
  blocks into **connected block-components** (transitive closure of "centres close in a spanner of block
  centres"). This is the **√N driver** and is **range-(emptiness)-only**. ✔ matches Pro's "stages 1,3".
- §6.3 **MST inside block-components** (= MSF of edges internal to components): estimated via the
  **directed (1+δ)-Yao graph J** (built from the **cone-NN oracle**) fed into the **CRT [13]
  bounded-degree connected-components estimator**. **This stage is where the cone-NN / Yao graph is
  load-bearing.** ← This is precisely the part Pro wants to replace.
- §6.4 **Connecting the components** (the graph H_min / set M): a variant of their **range-only 1st
  algorithm** on the sparse graph of block-component representatives.

So Pro's "(1) subdivision → O(√K) active blocks/components; (2) MST inside via CRT; (3) joining on a
sparse graph" is a **faithful** rendering of Czumaj §6. ✔ And Pro correctly identifies that **only stage
2 uses cone-NN** and must be swapped out for the range-counting model.

**Finding 1 (MINOR, mis-citation/redundant-import).** Czumaj's √N is in **time**, in a model with
**cone-NN + range-*emptiness***, not range-*counting*. The CRT-style component estimator they invoke is
their **own** §6.3 cone-NN routine — **NOT** the round-1 death-time sampler, and **NOT** automatically a
range-counting routine. Pro treats "Czumaj's CRT estimator" as if it were already a range-counting
primitive; it is not. (This is the seed of Finding 2.) It is MINOR only because the fix is available
off-the-shelf (see §3).

## 2. Is the Yao→WSPD replacement valid in the range-COUNTING model? (Pro's Q2)

This is the crux, and here is the **good news for substance / bad news for the write-up**:

The source paper [1] **already did exactly this replacement, and proved it rigorously in the
orthogonal-range-COUNTING model.** I read [1] §5 in full (`source_2504.txt` lines 775–1078):

- **[1] §5.1** builds a **quadtree/WSPD spanner S** of P (Callahan–Kosaraju WSPD, separation ε). Edges
  join the **lexicographically-smallest representatives** of each well-separated pair, with Euclidean
  edge length d(c,c′).
- **[1] Lemma 21 (verbatim):** "Each point of [Δ]² is contained in O(ε⁻² log Δ) pairs of W." → this is
  the **polylog-degree** claim Pro needs. ✔ It is a *real, cited* lemma (attributed to [32] =
  Callahan–Kosaraju), not hand-waved.
- **[1] Lemma 22:** for (c,c′)∈W, r(c′)/2 ≤ r(c) ≤ 2r(c′) (balanced pair radii).
- **[1] Lemma 23 (verbatim):** "The cost of the minimum spanning tree of S is at most (1+ε) times the
  cost of the Euclidean MST of P." → this is **exactly** Pro's "w(MST(Q)) ≤ w(MST(H_D)) ≤
  (1+ρ)w(MST(Q))". ✔ (and W ≤ W_S is immediate since S ⊆ complete graph).
- **[1] Lemma 24 (verbatim):** "Consider a grid cell c of Q of side length r/2. We can find all grid
  cells c′ of side length r/2 such that there is an edge in S between a point in c and a point in c′ of
  length ≤ r using **O(ε⁻²) range counting queries**." → this is **exactly** Pro's "incident pairs found
  locally with polylog orthogonal range queries", and it is a **range-COUNTING** lemma with a full proof
  (lines 819–857). ✔✔

**So Pro's Q2(a) is YES, and stronger than Pro states: [1] Lemmas 21–24 do prove polylog-degree + local
WSPD adjacency via *range-counting* queries, with proofs.** Pro is right to cite them. The WSPD spanner
truncated at an internal cutoff stays connected within a component (Pro's argument) and `w(MST)` is
preserved to (1+ρ) — and I numerically reproduced Lemma 23 (see §5: W ≤ W_H ≤ (1+ρ)W, ratio → 1 as
separation grows, always connected).

**BUT — Finding 2 (GAP, the real defect of Lemma 3).** Pro phrases the construction as *"import Czumaj
[2], then replace their directed Yao graph by a component-restricted (1+ρ)-WSPD spanner."* That framing
is **logically inverted and creates an unproven step.** Two problems:

  (2a) **The thing Pro is "replacing into" already exists as a clean theorem and does not need Czumaj.**
  [1] **Theorem 30 (verbatim):** "we can estimate the cost of a minimum spanning tree of P within a
  factor (1+ε) … using **Õ(√n) range counting queries**." That is the *whole* of Lemma 3 with K in place
  of n — **proved natively in the range-counting model, with the WSPD spanner, with no Yao graph, no
  cone-NN, no Czumaj.** Pro should be invoking **[1] Thm 30 applied to the support point set Q** (Q is
  itself a set of ≤K points in [Δ]², so Thm 30 gives w(MST(Q)) to (1±η) in Õ(√K) range-counting queries
  *on Q*). The import of [2] is **redundant and is what injects the cone-NN hazard.**

  (2b) Where Pro *does* need to do genuine new work is the bridge "**range-counting queries on the
  implicit support Q ⇄ range-counting queries on the real input P**," because [1] Thm 30 assumes a
  range-counting oracle **on the point set it is estimating**, i.e. on Q. Pro's "component-restricted
  emptiness/counting" paragraph is **precisely this bridge**, and it is **under-proved**:

  > "above the active-block level offline from the active-block list; below it, a query cell lies in one
  > active block, so one range-count answers emptiness."

  This is **mostly correct but glosses one case.** §2 of Pro's own response already established the clean
  fact: a range-counting query on Q over an axis-aligned box R reduces to **one** range-counting query on
  P over the snapped fine-cell box R̃ (since Q∩R ↔ P∩R̃, cell centres lying in R form a contiguous
  fine-grid range). **That reduction is unconditional and orthogonal** — it does **not** require
  restricting to a block-component, and it does **not** need a non-rectangular oracle. ✔ So the honest
  statement is: *"every range-counting query on Q costs exactly one range-counting query on P (§2);
  therefore [1] Thm 30 on Q runs in Õ(√K) range-counting queries on P."* That is clean and correct.

  **The hazard Pro introduces is the phrase "component-restricted."** Restricting a WSPD adjacency /
  emptiness query to **"the part of R inside block-component D"** is **NOT in general an orthogonal-box
  query**, because a connected block-component is a union of cells that need not be an axis-aligned
  rectangle (it can be an L-shape, a staircase, the serpent of §9). If the algorithm genuinely needed
  "is there a support point of Q in (box R) ∩ (component D)?", that is a **non-orthogonal range query we
  do NOT have.** Pro's defense ("above the active-block level it's offline; below it the query cell lies
  in one active block") is correct **only because** at the cutoff each leaf-query cell sits inside a
  single active block, so the intersection with D degenerates to either "all of the cell" or "none of it"
  — i.e. the component-restriction becomes trivial at query time and the actual oracle call is the plain
  orthogonal one. **This is true for [1]'s construction (their Lemma 24 cutoff i\* makes every witness
  query a plain orthogonal count) — but Pro never proves it; Pro asserts it.** Since Pro is *not* using
  [1]'s machinery verbatim (Pro claims to be inside Czumaj's *block-component* decomposition, which is a
  *different*, coarser, non-rectangular grouping than [1]'s quadtree cutoff), **the "one range-count
  answers emptiness" claim is not established for Czumaj's block-components and is the load-bearing
  unproven step.**

  **Repair:** drop Czumaj entirely; state Lemma 3 as "apply [1] Theorem 30 to Q, executing each of its
  range-counting queries on Q via the one-to-one §2 reduction to a range-counting query on P." Then
  there is **no** component-restriction, **no** non-orthogonal oracle, and the polylog-degree /
  local-adjacency facts are [1] Lemmas 21–24 used as-is. This is a clean repair and I believe it goes
  through — but **it is a repair, not what is written.**

## 3. Does the CRT component estimator port? Is it the round-1 routine? (Pro's Q3)

**Finding 3 (MINOR/clarifying, but exposes a real conflation).** Pro writes "the graph routine samples
O_η(1) uniform vertices per threshold + local traversals" and "CRT estimator applies to H=⊔_D H_D." Two
distinct estimators are being conflated:

- **Round-1's** estimator is the **death-time / rank-bottleneck multiset sampler** (verified). It does
  **O(log) expected local expansions per sample** and avoids BFS depth.
- **Czumaj §6.3 / [1] §5.3** uses the **CRT [13] (Chazelle–Rubinfeld–Trevisan) bounded-degree
  connected-components estimator**, which is **different**: it samples O(1/ε²) seed vertices and runs a
  **truncated BFS up to a threshold of t = √(#vertices) visited vertices** per seed (cf. [1] §5.3:
  "threshold t = √n … apply BFS … until we visit t vertices"). **That BFS truncation at √(#cells) is the
  source of the √K cost** — and it is a *per-component / per-threshold* BFS, **not** O(1) work.

So Pro's sentence "the graph routine samples O_η(1) uniform vertices per threshold + local traversals"
is **imprecise**: the CRT estimator does **O(1/ε²) seeds × up-to-√K BFS steps × O(log Δ) thresholds**.
In [1] this is honestly accounted as the **Õ(√K)** term (the √K BFS-truncation is *the* √-cost, paid
once across thresholds via the contraction-graph trick S′_i, Lemma 26). **Pro's "Õ(√K)" bottom line is
therefore correct, but its stated reason ("O(1) vertices per threshold + local traversals") is wrong —
the √K lives in the BFS truncation, exactly where [1] puts it.** Crucially, **this is NOT the round-1
death-time sampler**; Pro should not imply the round-1 machinery supplies stage-2. It is the heavier CRT
routine, but its cost is genuinely Õ(√K) and genuinely range-counting (via Lemma 24 for each BFS edge
expansion). No exponent leak here once stated correctly.

## 4. Total accounting for Lemma 3 (Pro's Q4)

Walking the corrected construction:
- **Active-block / quadtree decomposition + WSPD spanner traversal + CRT BFS:** Õ_η(√K) range-counting
  queries on Q = Õ_η(√K) on P (each via the §2 one-query reduction). ✔ This is [1] Thm 30 with n→K.
  **No smuggled √N·(n/K).** The √K is the BFS truncation, correctly owned (Finding 3).
- **Uniform support samples:** each uniform draw from Q costs Õ(n/K) range-counting queries on P (§2
  rejection sampler). The CRT estimator needs **uniformly random vertices of S′_i (= occupied cells)** as
  seeds, O(1/ε²) per threshold over O(log Δ) thresholds = **Õ(1)** seeds total. The **seed-reuse**
  trick (one pool of s = O_η(log T) uniform support points, reused across all thresholds with independent
  per-(seed,threshold) traversal randomness) is what keeps the expensive uniform-support calls at
  **Õ_η(1) × Õ(n/K) = Õ_η(n/K)** instead of √K × (n/K) = n^{2/3}.

  **Sub-check on seed reuse (sound):** for any *fixed* threshold the s pooled points are i.i.d. uniform
  over Q, so per-threshold concentration is unchanged; correctness at all T = O(log Δ) thresholds
  simultaneously follows from a union bound after O(log T) amplification. **Cross-threshold independence
  is genuinely unnecessary** (only marginal-per-threshold concentration is used). This matches the
  orchestrator-verified round-1 reasoning and is the correct accounting. ✔ This is the one piece I am
  most comfortable with (independent of the Czumaj/[1] confusion).
- **Active-block decomposition computable in Õ(√K)?** Yes: [1] §5 / Czumaj §6.1 both find the O(√K)
  active blocks/cells using O(√K·polylog) range queries (Cell-Sampling / Algorithm 1 of [1], which
  itself is the Õ(√n) cell-counter applied to the support). ✔

**Conclusion on Q4:** the **total is genuinely Õ_η(√K + n/K)** range-COUNTING queries, with **no hidden
√N·(n/K) blow-up and no √n**, *provided the construction is the [1]-Thm-30-on-Q one.* The exponent is
clean. The danger Pro flagged in §8 (needing √K *independent* support samples → n^{2/3}) is correctly
avoided by seed reuse. ✔

## 5. Numerical sanity checks (Pro's Q5) — all PASS

Using the repo's exact EMST (`sim/emst.py`, self-checked against brute force) and the venv:

1. **WSPD-spanner MST tracks true MST (source Lemma 23 / Pro's w(MST(Q)) ≤ w(MST(H)) ≤ (1+ρ)w(MST(Q))).**
   Built a real WSPD spanner (split-tree + separation s, lex-smallest representatives), Kruskal'd it:
   ```
   sep= 4.0  W_H/W in [1.033,1.056]  connected=True
   sep= 8.0  W_H/W in [1.004,1.016]  connected=True
   sep=16.0  W_H/W in [1.000,1.002]  connected=True
   ```
   Always ≥ 1, always connected, → 1 as separation grows. **Lemma 23 numerically confirmed.**

2. **Snapping to K≈n^{2/3} occupied cells tracks w(MST) and the heavy tail.** Adversarial instance
   (serpentine L-connected chain + 3 dense islands), n=2000, target K=159:
   ```
   chosen h=76.6  K=160   w(MST(Q))/w(MST(P)) = 0.904   (W_Q = Θ(W), as Lemma-2/§3 require)
   L=200: B_(L+δ)(P)=1375 ≤ B_L(Q)=1729 ≤ B_(L-δ)(P)=2025   ok
   L=400: B_(L+δ)(P)= 782 ≤ B_L(Q)=1129 ≤ B_(L-δ)(P)=1425   ok
   L=800: B_(L+δ)(P)=   7 ≤ B_L(Q)= 245 ≤ B_(L-δ)(P)= 416   ok
   ```
   The interleaving B_{L+δ}(P) ≤ B_L(Q) ≤ B_{L-δ}(P) holds at every threshold, including on the serpent
   (no false tail weight from intra-component spread). **Consistent with Lemma 3 being run on a support Q
   that faithfully tracks the tail.** (These are the foundations Lemma 3 sits on; the orchestrator
   already verified Lemma 2 — this is corroboration, not the contested step.)

## Summary of findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | MINOR | Czumaj [2]'s √N is *time*, in a **cone-NN + range-emptiness** model; its stage-2 estimator is its own cone-NN/Yao routine, **not** a range-counting primitive and **not** the round-1 sampler. Pro treats it as if already range-counting. |
| 2 | **GAP (repairable)** | The import of [2] + "replace the Yao graph" is **redundant and hazardous**: [1] **Theorem 30** *already* proves Õ(√K) range-**counting** EMST estimation via the WSPD spanner ([1] Lemmas 21–24, which *do* give polylog degree + local adjacency by range counts). Pro's "**component-restricted** emptiness" is the only genuinely new step and is **asserted, not proved**; restricting an emptiness/adjacency query to a (non-rectangular) block-component is **not an orthogonal query** in general. It is salvageable only because at the quadtree cutoff each query degenerates to a plain orthogonal count — true for [1]'s construction but **never proved for Czumaj's coarser block-components**. **Repair:** state Lemma 3 as "[1] Thm 30 on Q, each Q-query = one P-query via §2"; drop Czumaj. |
| 3 | MINOR | The stage-2 estimator is the **CRT bounded-degree component estimator with √K-truncated BFS**, not "O(1) vertices + local traversals." The √K cost lives in the BFS truncation (correctly, as in [1] §5.3). Pro's stated *reason* for Õ(√K) is wrong; the *bound* is right. |
| — | OK | Seed-reuse → Õ(n/K) expensive calls; total **Õ_η(√K + n/K)** is genuinely clean, no √N·(n/K), no √n, no non-orthogonal oracle **in the repaired version**. Active-block decomposition computable in Õ(√K). Both numerical sub-claims pass. |

## Does Lemma 3 as WRITTEN deliver Õ(√K) range-counting queries, or hide a cost?

**As written: it does not cleanly deliver it** — it routes through Czumaj [2], whose stage-2 engine is a
**cone-approximate-nearest-neighbour (non-orthogonal) oracle** routine, and Pro's one-paragraph
"component-restricted emptiness" replacement **asserts** (does not prove) that the restriction collapses
to a single orthogonal range-count. For Czumaj's *block-components* (non-rectangular) that collapse is
**not justified in the text**, so a referee can legitimately call this a non-orthogonal-oracle hole.

**However, the cost is NOT actually hidden:** the correct object Pro is reaching for — [1] **Theorem
30** — delivers precisely Õ(√K) range-**counting** queries on Q, and Pro's own §2 reduction turns each
Q-query into exactly one P-query, giving Õ(√K + n/K) on P with **no smuggled √N·(n/K) and no
non-orthogonal oracle.** So there is **no exponent leak** in the intended statement; the defect is a
**proof gap / wrong-engine import**, not a fatal complexity blow-up.

**Recommended disposition:** Lemma 3 = **NEEDS-REPAIR.** Replace the Czumaj-Yao-graph import with a
direct invocation of [1] Theorem 30 on the support Q (Q is a ≤K-point set; its range-counting oracle is
realized query-for-query on P via §2). With that substitution the lemma is, in my assessment, **correct
and delivers Õ_η(√K + n/K)** — but that substitution is mathematical work the response does not perform,
and the "component-restricted, non-orthogonal" phrasing it does perform is the unproven (and, taken
literally, oracle-illegal) step. Confidence the *repaired* lemma holds: **0.82**; confidence the lemma
**as literally written** is airtight: **0.45**.

## Claims I could NOT fully verify
- The Czumaj [2] PDF's **equations/constants** are garbled by 2004-era PDF encoding; I verified the
  **oracle list, algorithm structure, theorem prose, and which stage uses cone-NN** from legible prose,
  but could not machine-read the exact ε-dependence of their √N. (Not needed for the verdict — [1] Thm 30
  supersedes it in the range-counting model.)
- I did **not** re-derive that [1]'s Lemma 24 cutoff makes *every* witness query a plain orthogonal box
  on P for the **specific snapped support Q** of round 2 (as opposed to a generic P); [1] proves it for
  generic P and I judge it transfers, but the round-2 response does not contain this argument — it is
  part of the recommended repair.
- The Callahan–Kosaraju WSPD polylog-degree bound ([1] Lemma 21, cited to [32]) I took as established
  (standard, and the orchestrator pre-verified the round-1 WSPD machinery); I did not re-prove it.
