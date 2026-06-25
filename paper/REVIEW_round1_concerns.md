# REVIEW round 1 — concerns + triage (all via Codex gpt-5.5 xhigh, 2026-06-25)

Two independent Codex adversarial reviews. Full verdicts archived verbatim below (never truncated).
Routing: Codex only (red line). Triage codes: ACCEPT-FIX (will fix) / AS-SENTENCE (reword) /
COUNTER (defend, no change) / DEFER (acceptable for SODA full version) / NEEDS-PROOF (must add proof).

## Review 1 — App.A proof-correctness + completeness. VERDICT: **FLAWED** (8 BLOCKER, 9 MAJOR, 5 MINOR).
The residual-debt appendix has real errors. Root-cause clusters (my analysis) + fixes:

- **R-A edge-weight convention** (items 1,14,19,27, BLOCKER/MAJOR): App.A weighted edges by center
  distance d(c,c'); §4/App.C need a Euclidean spanner. FIX (ACCEPT-FIX): representatives are concrete
  grid points whose coordinates we learn when computing rep, so weight each edge by the EXACT Euclidean
  distance |rep(c)-rep(c')| (zero queries). Well-separation gives |rep-rep| ∈ (1±2ρ)d(c,c'), so the
  threshold-graph stretch c_X(t)≤c_S(t)≤c_X(t/(1+ρ)) holds; duplicate pairs then carry identical weight,
  killing the suppression-weight issue (14).
- **R-B exact vs rounded bottleneck** (items 3,21,24, BLOCKER): exact rep coords ⇒ exact edge weights ⇒
  run an exact bottleneck priority-queue (Prim/Dijkstra) returning exact τ(v); discovery uses the
  navigability oracle at the matching scale but the PQ orders by exact weight. FIX (ACCEPT-FIX).
- **R-C root handling** (item 4, BLOCKER): §4 ranks V\{r} with a root. FIX (ACCEPT-FIX): fix root = z-first
  point of X (computed once), rank −∞, halt on reaching root OR any lower-ranked vertex.
- **R-D the extraction cap** (items 6,7,8,10,28, BLOCKER×4): my cap argument was WRONG — imputing X_L=L is
  UPWARD-biased, Markov gives 1/δ' not log(1/δ'), and bias n·δ'·L does not absorb at constant δ'. FIX
  (ACCEPT-FIX, the correct design): NO per-search imputation. Use a GLOBAL per-call query budget = C×
  expected total; abort the whole call → FAIL on overrun (Markov on the total, small constant prob). §5's
  W-search already tolerates FAIL (no-stop). This removes the bias entirely.
- **R-E cell-graph vs point-graph oracle** (items 2,9,15,18,26, BLOCKER/MAJOR): source Lemma 24 finds
  neighbor CELLS; the point-graph death-time needs a vertex's INCIDENT spanner edges. FIX (ACCEPT-FIX,
  NEEDS-PROOF): build a vertex-incident-edge oracle on top of Lemma 24 — for vertex u, iterate its
  O(log Δ) quadtree-ancestor cells c with rep(c)=u, apply the cell-neighbor oracle (O(ρ^{-2}) counts each),
  test surviving-pair membership, emit edge u–rep(c'); total O(ρ^{-2} log²Δ) counts/vertex, incident count
  O(ρ^{-2} log Δ) by source Lemma 21. Extra log factor absorbed in Õ.
- **R-F support representatives + seed cost** (items 11,12,20, MAJOR): for X=Q use rep_Q(c)=z-first nonempty
  support h-cell center (P-emptiness descent); A.1 seed cost for Q is Õ(n/K) by rejection, not O(log Δ).
  FIX (ACCEPT-FIX): distinguish P and Q throughout A.1/A.2.
- **R-G smaller** (items 5,13,16,17,22,23,25,29): harmonic 1/(j-1) (5); nested-cell condition for the
  redundant-pair test (13,16); radius-vs-side notation (17); telescoping over a cell union one sentence
  (22); weaken "every step concrete" opening (23); surface n^{1/3}·poly(1/ε)·polylog (25); note
  deterministic-order invariance for the source stretch (29). All ACCEPT-FIX (cheap).

→ ACTION: full rewrite of app_wspd.tex. Plus §4 touch-ups (items 24,27) and an explicit
n^{1/3}·poly(1/ε) note (25).

## Review 2 — whole-paper panel. VERDICT: **MAJOR-REVISION**. Readability R-W1/R-W2/R-W3 all OK-with-notes
(NO BLOCKER → convergence gate (d) is green once notes are addressed).

- **W1 overclaim "resolves/settles"** (item 1, MAJOR): abstract+intro overstate; §6 already qualifies.
  FIX (AS-SENTENCE): use "settles the polynomial query exponent / matches up to polylog+ε factors"
  everywhere.
- **W2 Czumaj row error model** (item 2, MINOR): "O(n^{1/4}) rel." unclear. FIX (AS-SENTENCE): state the
  normalization.
- **W3 §4 K-window/halving search not proved** (item 3 + R-W2 item 10, MAJOR): App.C proves only
  K_h≤8W/h+4, not the halving search / approx-K stopping / total cost. FIX (NEEDS-PROOF): add the full
  regularization-search proof to App.C.
- **W4 input model multiset vs set** (item 4, MAJOR): prelims says multiset, main_theorem uses W≥n-1
  (distinct points). FIX (ACCEPT-FIX): make it a set of distinct points everywhere; n≤1 trivial.
- **W5 refs** (items 6,7,8, MAJOR/MINOR): add Chen–Khanna ICALP'23 (arXiv:2203.14798) [verify], metric
  Steiner (arXiv:2211.03893) [verify], a component-estimation (Berenbrink/CRT-type) ref; explain why each
  is not a range-counting competitor. FIX (ACCEPT-FIX) — also nudges 41→~46.
- item 5 (proof-presence certifications) — no action, confirms App.B/App.C back the body claims.

## Convergence-gate status after round 1 (pre-fix)
(a) proofs complete — NO (App.A flawed; §4 K-window proof missing). (b) length 21pp — under 45-60 target
but appendices grow with fixes. (c) refs 41 — under 50-70, +3 strand refs pending. (d) readability — GREEN
(no BLOCKER). → must re-audit App.A after rewrite.

---

## VERBATIM VERDICT 1 (App.A)
[see scratchpad codex_appA_verdict.md — archived to docs/ below]

## VERBATIM VERDICT 2 (whole paper)
[see scratchpad codex_whole_verdict.md — archived to docs/ below]
