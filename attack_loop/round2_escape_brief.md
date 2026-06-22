# Round 2 — Brief to attacker (the escape: a multi-needle / planted-pattern hard distribution)

**To:** external solver (codex GPT-5.5-xhigh, FRESH session). **From:** orchestrator. **Date:** 2026-06-21.
**Type:** method-free brief (FACTS frozen, METHODS free). Solve §5; report per §6.

> Round 1 PROVED that the obvious route is dead. This brief asks the one question that survives it.
> Read §3 (what is already proven) carefully — do not re-attempt the refuted route.

---

## 1. The setting (frozen)

Points P ⊂ [Δ]² (integer grid), **|P| = n**, spread **Δ = O(n)**. w(P) = Euclidean MST weight. An
**orthogonal range-counting oracle** answers a query rectangle R (axis-aligned) with the **exact
integer count |P ∩ R|**. Cost = number of queries. Goal model: a randomized algorithm that, with
constant success probability, outputs a **(1±ε)-multiplicative estimate of w(P)** for a fixed constant
ε ∈ (0,1).

**The lower-bound target (unchanged):** prove every such algorithm needs **Ω(n^{1/2−o(1)})** queries.
(The known upper bound is Õ(√n); the known lower bound is Ω(n^{1/3}), both from Driemel et al.,
SoCG 2025 — this would close that gap up to n^{o(1)}.)

**The lower-bound mechanism (frozen, Yao/distributional).** Exhibit a distribution over instances on
which w(P) takes two well-separated values — a "LOW" world with w ≈ w₀ and a "HIGH" world with
w ≥ (1+3ε)·w₀ — each with probability 1/2, such that **any algorithm making o(m) queries produces a
query-answer transcript whose distribution is statistically close (TV = o(1)) under LOW vs HIGH**, and
hence cannot tell which world it is in ⇒ cannot (1±ε)-estimate w. Then the query complexity is Ω(m),
and we want **m = Θ(n^{1/2})**. (Equivalently: a needle/pattern is hidden; until a query "hits"
informative structure, LOW and HIGH give identical counts; one needs Ω(m) queries to hit it.)

---

## 2. The operative quantity (frozen — this is NOT a bit-counting problem)

For each query rectangle R, what matters is its **coverage / candidate-distinguishing-power**: the
number of independent hidden "informative configurations" whose state can change the *exact count*
|P ∩ R|. The hitting bound is **Ω(m / max-coverage)**. To reach Ω(m) = Ω(n^{1/2−o(1)}) the construction
must keep per-query coverage **O(1)** (or m^{o(1)}). ⚠️ **The Ω(log m) trap:** a naive
mutual-information / bit-accounting argument gives only Ω(log m) (locating 1-of-m is log m bits);
the operative quantity is geometric coverage (how many hidden configs a single rectangle's count is
jointly sensitive to), NOT bits. Any formalization must be checked to deliver Ω(m), not Ω(log m).

---

## 3. What is ALREADY PROVEN (substrate P1 — use freely; do NOT re-derive or re-attempt)

In Round 1 the following was proven (attacker + two independent audits, analytic + exact-EMST numerics):

> **P1 (single-cell gap cap).** Partition the difference between the LOW and HIGH worlds so that they
> differ inside exactly ONE region ("cell") of side s holding p points, with the two worlds equal in
> count outside it (equal cardinality). Then |w_HIGH − w_LOW| ≤ O(s·√p) (this UB is geometry-agnostic:
> fractal/hierarchical/nested gadgets cannot beat it). Meanwhile, for m disjoint occupied cells,
> w(P) ≥ Ω(s·m). Since s cancels, the relative gap is ≤ O(√p/m) = n^{3c/2−1} (p=n^c, m=n^{1−c}), so a
> constant-fraction gap needs c ≥ 2/3, i.e. **m ≤ n^{1/3}**. The "raise the number of hidden cells to
> n^{1/2} via a single hidden heavy gadget" route therefore gives **no improvement at all** over n^{1/3}.

**Refuted routes (N*) — do NOT propose these:**
- N1: a single hidden "heavy" cell among m disjoint equal-cardinality cells (any heavy-gadget geometry,
  any tiling/packing/spread layout — s cancels; coincident/cluster sparse — w(P) is backbone-dominated).
- Unequal cardinality to enlarge the single-cell gap: it makes the special cell visible to ONE coarse
  counting query (a rectangle enclosing it returns a different integer count), collapsing the bound to
  Ω(log m) (the trap of §2). So the LOW and HIGH worlds must be **count-indistinguishable in bulk**.

**Consequence (the corner you must turn).** Because a single-cell difference is capped, the
LOW↔HIGH w(P)-difference of Θ(ε·w(P)) **must be CORRELATED across ω(1) cells** (a multi-cell / planted
pattern). A correlated difference of this size is geometrically easy to achieve (making Θ(m) cells
differ in a coordinated way yields a global EMST gap that is a constant fraction of w(P), even at
p=n^{1/2} — numerically confirmed). **That is the easy part and is not the question.**

---

## 4. Barriers in force (B*)

- **B1.** (#cells)×p ≤ O(n); Δ = O(n). w(P) includes the inter-cell backbone.
- **B2 (Ω(log m) trap).** Must reach Ω(m), not Ω(log m). Coverage (geometry), not bits, is operative.
- **B4 (single-cell cap = P1).** No single-cell difference exceeds O(s√p); routes to m=ω(n^{1/3})
  candidates MUST use a correlated/planted pattern.
- **🔴 B-new (the live obstruction — state plainly, do not assume either way).** A LOW↔HIGH global
  w(P)-difference of Θ(ε·w(P)) that is a *correlated/bulk* shift is, a priori, **cheaply estimable by a
  few coarse range-counting queries** — because a handful of large rectangles already return integer
  counts that may track the aggregate, distinguishing LOW from HIGH in O(polylog) queries (which would
  give only Ω(log m), or no bound at all). So the construction must hide the Θ(ε·w(P)) EMST difference
  inside a **pattern whose effect on the EXACT count |P ∩ R| of every axis-aligned rectangle R is
  (nearly) identical under LOW and HIGH**, except via hitting one of Ω(m) low-coverage informative
  configurations. Whether a point configuration can have its EMST weight shifted by a constant fraction
  while keeping all rectangle-counts (nearly) class-independent is **exactly the open question** — do
  NOT assume it is possible OR impossible.

---

## 5. The open question (method-agnostic — use ANY method)

> **Does there exist a distribution over n-point sets in [Δ]² (Δ=O(n)) — a "planted-pattern" / multi-
> needle hard distribution — such that:**
> **(a)** w(P) is, with probability 1/2 each, ≈ w₀ (LOW) or ≥ (1+3ε)w₀ (HIGH) for a constant ε;
> **(b)** the exact range-COUNT |P ∩ R| of every axis-aligned rectangle R has (nearly) the same
>   distribution under LOW and HIGH, except that the class is revealed only by a query "hitting" one of
>   **m = Θ(n^{1/2})** hidden, low-coverage (O(1)-coverage) informative configurations;
> **(c)** hence any o(m)-query algorithm has TV = o(1) between its LOW and HIGH transcripts ⇒
>   **Ω(n^{1/2−o(1)})** queries are required?

Construct such a distribution (give the point layout, the LOW/HIGH coupling, the EMST-gap analysis, the
per-query coverage/count-indistinguishability analysis, and the Ω(m) hitting/round-elimination step,
checked to reach Ω(m) not Ω(log m)). Candidate tools you may use or discard freely: Ruzsa–Szemerédi /
induced-matching packings (so each rectangle meets O(1) informative configs); coding-theoretic /
error-correcting plantings; Fourier/XOR structure; augmented-indexing / round-elimination over the m
configs; the source paper's own needle/EMD machinery. No method is mandated.

**OR**, if no such distribution can exist, **prove the general obstruction** — e.g. a theorem of the
form "any two n-point sets in [Δ]² whose EMST weights differ by ≥ ε·w(P) can be distinguished by
O(polylog n) orthogonal range-counting queries," which would *extend P1 to the correlated case* and
constitute a proof-of-death for the n^{1/2} target via this entire family. Either outcome is decisive.

---

## 6. What we need back

1. **A construction** (point layout + LOW/HIGH coupling) with: (i) the EMST-gap analysis showing
   |w_HIGH − w_LOW| ≥ ε·w(P); (ii) the **count-indistinguishability** analysis showing every rectangle's
   exact count is (nearly) class-independent except on O(1)-coverage informative configs; (iii) the
   **Ω(m)=Ω(n^{1/2−o(1)})** query lower bound (hitting / round-elimination), explicitly checked to beat
   the Ω(log m) trap — **OR** a precise statement of which of (i)/(ii)/(iii) breaks and why.
2. **OR a general obstruction** proving any ε·w(P)-gap is cheaply count-distinguishable (proof-of-death).
3. **An updated confidence %** that an Ω(n^{1/2−o(1)}) counting-oracle lower bound exists at all (i.e.
   that the upper bound Õ(√n) is essentially tight rather than the truth being ~n^{1/3}).
4. **A clear verdict** (constructed / partial-with-precise-gap / general-obstruction / open).
5. *(Optional)* small-scale exact-EMST + brute-force-coverage numerics supporting any claim.

Be rigorous and concrete; we will independently adversarially audit the reply (looking for: a coarse
counting query that distinguishes the classes after all; a coverage that is secretly ω(1); an Ω(log m)
mis-packaging; a hidden cardinality/backbone term; an EMST-gap miscalculation). A precise "here is
exactly where it breaks" is more valuable than an over-claimed construction.
