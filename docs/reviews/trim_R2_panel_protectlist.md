R-W1 — verdict clean

BLOCKER: none.

The first-page merits are findable: model/gap at `intro.tex:16-24`, theorem at `intro.tex:31-35`, tightness at `intro.tex:38-42`, prior-positioning table at `intro.tex:44-60`, and the support-estimator balance at `intro.tex:63-75`.

The empty-cell spatial leader idea is clear twice before the formal section: compactly in `intro.tex:92-104`, then visually and algebraically in `overview.tex:31-91`. The comparison-to-prior sentence in `overview.tex:194-208` is also very effective and should survive trimming.

R-W2 — verdict OK-with-notes

BLOCKER: none.

The reproduction thread is mostly continuous: §2 gives the map, §4 proves/states the support estimator, §5 splits bulk/tail and snapping, and §6 assembles `A_L(P)+W_Q-A_L(Q)`. The warmup in `support_mst.tex:75-88` and the worked example in `main_theorem.tex:144-171` are important for keeping the construction reproducible.

SHOULD-FIX: `lem:kwindow` is referenced in the body but formally stated only in the appendix. Locations: `overview.tex:143`, `deathtime_reduction.tex:165,188`, `main_theorem.tex:27,156`; statement is in `app_assembly.tex:67-72`. Promote the lemma statement or inline its exact window/cost guarantee in §5.

SHOULD-FIX: the worked example says the estimator hits each satellite with probability `Theta(1/K0)` and reads all `W_Q` in `Otil(sqrt(K0))` queries (`main_theorem.tex:159-163`). As written, that probability sounds too small for the claimed budget. Rephrase in terms of the scale-dependent candidate universe and the packing/accounting bound.

R-W3 — verdict OK-with-notes

BLOCKER: none.

The architecture is coherent: cluster integral → spatial leader estimator → packing/accounting → bulk/tail reduction → WSPD realization → balance point. The overview mirrors the body well.

SHOULD-FIX: `overview.tex:24-29` says a “handful” of satellites forces `Omega(sqrt K)` point samples. That scaling needs the satellite count/parameter made explicit, or it should say the point-sampling cost is `K/s` in the warmup family.

Claim precision is otherwise good. Keep the model qualifiers around optimality: fixed plane, fixed `eps`, range-counting oracle, up to polylogarithmic and `eps` factors. Do not compress these into an unqualified “optimal MST estimator” claim.

PROTECT-LIST

1. `abstract.tex:3-8` — one-line contribution: randomized `(1±eps)` estimator using `Otil_eps(n^{1/3})`, matching the `Omega(n^{1/3})` lower bound and improving `Otil(sqrt n)`.

2. `abstract.tex:10-18` — technique summary: empty-cell spatial leader estimator, samples grid cells including empty ones, variance governed by component count, balance at `K=Theta(n^{2/3})`.

3. `intro.tex:16-24` — model/gap setup ending “We close it.”

4. `intro.tex:28-42` — main theorem plus single-takeaway tightness sentence: lower bound and upper bound agree up to hidden factors.

5. `intro.tex:44-60` — comparison table and caption; keep the four rows and the caption’s “improvement in query exponent under the weaker range-counting oracle.”

6. `intro.tex:63-75` — support-MST lemma and balance sentence: `Otil_eta(sqrt K+n/K)`, balanced at `K=Theta(n^{2/3})`, yields `n^{1/3}`.

7. `intro.tex:77-88` — corollary and scope remarks, especially plane/fixed-dimension qualifier, randomized Monte Carlo, and running-time-not-only-query-bound claim.

8. `intro.tex:92-104` — §1.2 technique intuition: mass sampling misses far-flung heavy points; new primitive samples space, includes empty cells, unique leader, variance `Mc`.

9. `intro.tex:106-112` — one-paragraph roadmap: support estimator, clipped death-time sampler, support regularization/snapping, assembly, WSPD.

10. `overview.tex:3-5` — overview map sentence: formal development can be read against this section.

11. `overview.tex:9-20` — cluster-count integral and the reduced problem: estimate single-linkage component counts using range counts.

12. `overview.tex:22-29` — mass-versus-weight barrier example; keep, but parameterize the satellite count precisely.

13. `overview.tex:33-45` — empty-cell leader one-bit experiment quote: draw from `U`, empty gives `0`, occupied explores ranks, leader returns `M`.

14. `overview.tex:47-76`, Fig. leader — preserve labels/semantics: empty sampled cell `X`, `empty: Z=0`, circled leaders, dense block, far satellites, caption’s “tiny mass never enters.”

15. `overview.tex:79-91` — expectation/variance derivation and harmonic exploration-cost intuition.

16. `overview.tex:96-121` — two costs plus packing inequality: trials see `U,c`; exploration sees `N`; active-cover packing collapses both to `Otil(sqrt K)`.

17. `overview.tex:123-165` — reduction map: choose `G`, `K0`, `L`; split into bulk/tail; estimate `A_L(P)`, `W_Q`, `A_L(Q)`; assemble `W_hat=A_hat_P+W_hat_Q-A_hat_Q`; geometric search.

18. `overview.tex:167-180` — WSPD realization map and warning that this is the implementation part a verifier should read closely.

19. `overview.tex:182-208` — balance point and novelty comparison: `sqrt K` versus `n/K`; leader estimator is the source of the polynomial improvement.

20. `prelims.tex:3-14`, `21-38` — formal oracle model, cost measure, problem statement, and “range count returns a cardinality, not a witness.”

21. `prelims.tex:40-68` — cluster-count integral proof and inequality `c_S(t)-1 <= W/t`.

22. `prelims.tex:70-85` — death-time/spanner view before formal use.

23. `prelims.tex:106-157` — notation and parameter tables; these are essential for `K,Q,W_Q,b,delta,G,K0,L,xi,rho`.

24. `support_mst.tex:3-20` — section opener plus Lemma support-MST estimator.

25. `support_mst.tex:24-44` — support oracle operations, especially uniform support-cell rejection and the `n/K` cost for estimating `K`.

26. `support_mst.tex:48-73` — support overview: rare-heavy structure, sample space not mass, two cost drivers, packing collapse.

27. `support_mst.tex:75-88` — warmup example; keep the block-plus-satellites calculation and packing punchline.

28. `support_mst.tex:92-117` — active cover construction and packing lemma intuition/proof sketch.

29. `support_mst.tex:122-160` — empty-cell leader estimator algorithm, Lemma leader estimator, and “occupied-cell count never enters.”

30. `support_mst.tex:164-212`, Fig. scale graph — preserve labels/semantics: components, isolated satellite cells, `<= r?`, `cG(r)=4`, and interleaving `c_Q(r+) <= cG(r) <= c_Q(r)`.

31. `support_mst.tex:216-230` — candidate universe: sample uniformly from subcells of active blocks, empties cheap, independent of point multiplicity.

32. `support_mst.tex:235-268` — additive call, Riemann-sum decomposition, guess removal, and final `n/K` perturbation.

33. `deathtime_reduction.tex:3-7` — section small map: bulk by death-time sampler, tail through snapped support.

34. `deathtime_reduction.tex:11-15` — death-time intuition: “how heavy is the MST” becomes “how far must a random vertex travel to reach someone more senior.”

35. `deathtime_reduction.tex:17-43`, Fig. cluster staircase — preserve axis labels, shaded area, clip `L`, `A_L`, `B_L`, `bulk (clipped)`, `tail`.

36. `deathtime_reduction.tex:46-68`, Fig. death-time search — preserve seed rank, first lower rank, root, path label, `tau(v)=2.1`, and harmonic-search caption.

37. `deathtime_reduction.tex:71-100` — death-time definition, multiset identity, variance bound, and spanner stretch bound.

38. `deathtime_reduction.tex:104-138`, Fig. snapping — preserve `P (scattered)`, `h-grid`, nonempty `h`-cells, snap arrow, `Q` cell centers, and tail-transfer caption.

39. `deathtime_reduction.tex:141-166` plus `app_assembly.tex:67-72` — regularization search: why search is needed, `K_h <= 8W/h+4`, final `K=Theta_xi(K0)` and `Otil_xi(n/K0)` cost.

40. `deathtime_reduction.tex:170-189` — snapping intuition, interleaving inequality, and tail-transfer error `O(xi W)`.

41. `deathtime_reduction.tex:193-210` — decomposition map: no single estimator handles both ends; estimate `A_L(P)`, `W_Q`, `A_L(Q)`.

42. `main_theorem.tex:5-31` — main theorem and Algorithm 1 skeleton.

43. `main_theorem.tex:36-59` — three pieces under a guess; especially common normalization by `G` and clip-level lever sentence.

44. `main_theorem.tex:61-79` — amplification/failure bookkeeping and `K0=n^{2/3}` cost-balance remark.

45. `main_theorem.tex:84-127` — combining and removing the guess, including stop rule `W_hat(G) >= G/8` and bracket `G0 in [W,16W)`.

46. `main_theorem.tex:144-171` — worked example and punchline; keep the carpet/satellite instance and final sentence contrasting point-mass sampling with spatial leader sampling, but fix the `Theta(1/K0)` phrasing.

47. `optimality.tex:3-18` — lower-bound match and corollary; keep model and hidden-factor qualifiers.

48. `optimality.tex:22-44` — conceptual “why `n^{1/3}`” paragraph; keep the heuristic/formal distinction.

49. `openquestions.tex:13-38` — EMD discussion; preserve “open problems, not claims” and the two needed analogues.

50. `openquestions.tex:46-53` — cost of learning `K`; preserve because it explains why the `n/K` term matters.

51. `app_wspd.tex:18-29` and Fig. WSPD at `app_wspd.tex:161-165` — WSPD navigation labels: `u=rep(c)`, `c side s`, partners at `d=Theta(s/rho)`, `rep(c')`, scanning ancestors.