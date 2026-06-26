VERDICT: SKIM-PASS

REASON:
The first 10 pages do convey the merits. The problem/model and open gap land in §1: range-counting access is explained, Driemel et al.’s Õ(√n) upper bound vs Ω(n^{1/3}) lower bound is stated, and “We close it” is immediate. The main theorem appears early in §1.1, and Table 1 makes the prior-work position clear. The single takeaway is crisp: the new empty-cell spatial leader estimator samples space rather than point mass, giving Õ(√K+n/K) on a K-cell support and hence Õ(n^{1/3}) at K=Θ(n^{2/3}).

The contribution is graspable without the appendix at a skim level: §2 explains the cluster-count integral, the leader estimator, the packing inequality, the support reduction, the AP+WQ−AQ assembly, and the balance point. I would not claim correctness without the appendices, because the query accounting, snapping/regularization, and WSPD implementation are explicitly deferred, but I would not bury the paper on readability/merits.

Findings:
[SHOULD-FIX] §1.3 Related work, intro.tex:155-179: the paragraph drifts into broad citation terrain before the technical overview, e.g. “alongside sublinear algorithms for sequence and string problems” and “distributionally robust optimization for networked systems.” This is where a 10-minute skimmer gets bored. Compress §1.3 to the MST/range-counting lineage and move peripheral citations later or cut them.

[SHOULD-FIX] §2.3, overview.tex:98-123: the cost discussion introduces too many symbols at once: “needs O(MU/α_r^2) trials,” “exploration can touch up to N,” then “active-cover packing inequality WQ ≥ bδ/16.” The idea is important but easy to lose. Add a small variable table before this paragraph: M = sampled cell universe, U = component-count upper bound, N = occupied cells, α_r = additive target, b,δ = active-cover parameters.

[SHOULD-FIX] §2.4, overview.tex:127-167: the reduction from P to Q is understandable but symbol-heavy. The line “We therefore add the bulk of P to the tail of the snapped support” is good; make it a displayed boxed roadmap before the details:
estimate bulk on P, estimate full support Q, subtract bulk on Q. Then state in one sentence why this preserves the long-edge tail.

[SHOULD-FIX] Appendix dependence, intro.tex:181-185 and overview.tex:3-5: “Full proofs are in … appendices” plus “proofs in the appendices” may worry SODA reviewers. Keep the appendix for details, but ensure the main body contains the load-bearing proof skeletons for the support query bound, snapping/tail transfer, and global budget. The skim is fine; the submission gate is stricter.

[NIT] §2 opening, overview.tex:3-5: “Nothing here is used later; the reader who prefers to start from definitions may skip” undersells the most useful part of the paper. Rephrase to make §2 the intended reader’s map, not optional filler.

[NIT] §2.1, overview.tex:24-30: the dense-block-plus-satellites example is helpful, but the jump from Ω(√K) point samples to the “√n barrier” is a bit fast. Add one sentence tying K to the old support/input scale and to why this cost repeats across scales.