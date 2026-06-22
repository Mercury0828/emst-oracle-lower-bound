# DESIGN_DECISIONS — emst-oracle-lower-bound (append-only)

> Append-only decision log. New entries at the bottom. Guide changes go ONLY to
> `docs/guide_amendments.md`; this file records *our* operating decisions.

## 2026-06-20 — Phase 0 bootstrap

- **D0.1 — Scaffold at repo root, not a nested `deepdive/` folder.** The bootstrap prompt names
  `deepdive/emst-oracle-lower-bound/` "unless the owner says otherwise," but the cloned repo root
  (`e:\Project-git\emst-oracle-lower-bound`) already IS the project (contains `guide.md`, `README.md`,
  `start_up_for_claude_code.md`; no `deepdive/` subtree exists). README says "Open this directory."
  Decision: scaffold at root. Reversible if the owner wants the nested layout.

- **D0.2 — Roles fixed day-0 (guide.md §9.0).** Math attacker = codex GPT-5.5-xhigh → web GPT-5.5-Pro
  (human-relayed). Claude (this session) = orchestrator / referee / archivist, NOT solo prover.
  Auditors = fresh-context agents. Decider = human (owner). Phase 0 invokes NO attacker — it is
  screening only.

- **D0.3 — Attack axis = needle-in-haystack** (locate the hidden heavy cell under the space budget),
  NOT scale-by-scale / dyadic round-elimination (the rejected, misaligned framing). Round-elimination,
  if ever used, applies to LOCATING the hidden cell and must reach Ω(m), not Ω(log m). (From guide
  §11 decision log; restated here as our operating commitment.)

- **D0.4 — Strength gate (closes vs improves) is decided by the science (C1+C2), not venue fit nor
  difficulty.** SODA fit is genuine either way. Never claim "tight/closes" unless n^{1/2−o(1)} is
  actually proven. A provable cap below 1/2 is proof-of-death for the n^{1/2} target (report
  honestly), NOT a difficulty downgrade. (guide §0, §9.0b.)

- **D0.5 — Brief rails (never smuggle unproven implications).** Forbidden in any attacker brief:
  "sparse gadget ⇒ O(1) coverage"; "O(1) bits/query ⇒ the lower bound" (the Ω(log m) trap);
  "Czumaj emptiness Ω(√n) ⇒ a counting bound." State what is known; pose the open question cleanly.
  (guide §9.2.)

- **D0.6 — Simulation env: local `sim/.venv` (py3.12), numpy/scipy/matplotlib.** Exact EMST via
  `scipy.spatial.Delaunay` + Kruskal/union-find over Delaunay edges (direct all-pairs for tiny n).
  Do not touch the system environment. Fixed seeds; `sim/run_all.py` regenerates every figure/number.

- **D0.7 — Screen evidence discipline.** Adversarial placements are the ONLY de-risk evidence; random
  placements are a smoke/sanity check only. The adversarial **max** (tail), not the mean, is the C2
  kill metric. Pre-register expected trend + a falsifier BEFORE running each screen (see
  pre-registrations below). Never shape-force a gadget/packing to make a plot clean. A screen that
  contradicts the pre-registration is a *finding*, not a failure.

### Pre-registrations (written BEFORE running the screens — guide §7)

- **PR-C1 (gadget detectability).** Build the source n^{2/3}-point uniform(heavy)/strip(sparse)
  gadgets as a frozen anchor; reconfirm their heavy/sparse EMST-cost separation; then thin the heavy
  gadget's point budget p toward ~n^{1/2} (m cells, p pts/cell, n=m·p, sweeping p between p≈n^{2/3}
  and p≈n^{1/2}). Measure the **heavy-vs-sparse global w(P) gap as a fraction of total w(P)**
  (all-sparse vs one-heavy). **Expectation:** the gap fraction stays **≥ a fixed ε threshold** as p
  shrinks toward the n^{1/2} regime (form: gap is a constant fraction of w(P); constants may differ).
  **Falsifier / kill signal:** the gap fraction shrinks below ε and **keeps shrinking** as p→n^{1/2}
  (gadget cannot be both sparse and MST-distinguishable). **Negative control:** confirm the gap
  *breaks* when the gadget is made far too sparse. **Scale caveat:** at a few-thousand points m≈50 and
  p≈n^{2/3} vs p≈n^{1/2} differ by only a small factor — the screen shows the TREND, not the
  asymptotic crossover.

- **PR-C2 (per-query coverage — decisive).** Build the baseline packing (m candidate gadgets on a
  √m×√m subgrid of cells, one heavy); enumerate axis-aligned query rectangles; for each measure its
  **candidate-distinguishing-power = #candidate cells whose heavy/sparse flip changes the exact
  COUNT |P∩R|**; report the **max over rectangles**, swept as m grows. **Expectation:** max coverage
  stays **flat / O(1)** (at worst m^{o(1)}) as m grows. **Falsifier / kill (strength) signal:** max
  coverage **grows polynomially with m** (m^{Ω(1)}) ⇒ exponent capped below 1/2 ⇒ "improves" not
  "closes" (m^{o(1)} growth still supports n^{1/2−o(1)}). **Adversarial placements are the kill
  metric**, random are smoke only. **Secondary proxy:** max mutual information between a query's count
  and the hidden index, reported as a **ratio to the log m baseline** (only a *climbing ratio* is a
  signal; raw bits grow like log m trivially). **Contrast:** measure emptiness-query coverage on the
  same packing — *hypothesis* (not guaranteed) that it is ≤ counting coverage; equality is itself
  informative. ⚠️ A baseline screen showing growth is a RED/YELLOW SCREEN (→ redesign packing /
  escalate / human gate), NOT by itself proof the target is dead (only a *proof* that every feasible
  packing has polynomial coverage is proof-of-death).

### Post-run notes (after the screens + the independent gate-1 audit)

- **D0.8 — C2 adversary strengthened to coordinate-snapped rectangles (audit-driven).** The first
  committed C2 adversary (half-planes / slabs / cell-centre frames) reported grid coverage ≈ 2√m. The
  independent gate-1 auditor's stronger adversary (coordinate-snapped random rectangles) found ≈ 4√m —
  because a *centre* cut splits the strip symmetrically (heavy-count = sparse-count ⇒ not covered);
  the true worst case needs OFF-CENTRE edges snapped to actual point coordinates. `sim/c2_coverage.py`
  was updated to use the coordinate-snapped adversary and now **reproduces the auditor's numbers**
  (grid ≈ 3.5–4·√m; slope ≈0.55). The exponent/conclusion is unchanged (and strengthened); only the
  constant moved. Reported coverage is worst-case over our family = a *lower bound* on the true optimum.
- **PR-C1 outcome:** expectation partially met — detectability holds at moderate thinning but DECLINES
  toward the full n^{1/2} budget (gap_frac at θ=1/2 falls with n). A *finding*, not a failure: the
  naive gadget is insufficient at n^{1/2}; a more point-efficient (ratio ~m) gadget is the C1
  obligation. Negative control = 0 (clean).
- **PR-C2 outcome:** expectation **falsified on the baseline grid** (coverage grows √m, not O(1)) —
  exactly the residual risk. The permutation variant gives O(1), but the audit showed this is **not
  bankable** (it rides on equal-cardinality invisibility — in tension with C1 point-efficiency — on a
  Δ=1.00·n layout with zero slack). Net: the open object is a three-way squeeze (point-efficient ×
  equal-cardinality × O(1)-coverage × Δ=O(n)); recorded as the C2 attack-loop target. No shape-forcing.
- **D0.9 — Confidence revised 50%→38% (audit-adopted), and Phase-1 entry plan.** Per §9.0b a drop is
  an *attack-harder* signal, not a target downgrade (n^{1/2−o(1)} unchanged). Phase-1 first milestone =
  a **time-boxed kill-experiment**: construct one point-efficient, equal-cardinality heavy gadget that
  shifts w(P) by ≥ε at the n^{1/2} budget; if impossible (or it forces unequal cardinality, which the
  C2 screen shows blows up coverage), fall back to the best provable "improves" exponent. Deferred to
  the human at gate #1 to approve (the strength decision).

## 2026-06-21 — Phase 1 attack loop + the §9.6 PIVOT

- **D1.0 — Gate #1 PASSED; attacker = codex GPT-5.5-xhigh** (local `codex` CLI, ChatGPT auth,
  `model=gpt-5.5`, `model_reasoning_effort=xhigh`). Math routed via `codex exec -s read-only`; Claude
  stays orchestrator/referee. Round artifacts under `attack_loop/`.
- **D1.1 — Round 1 (C1) result: REFUTATION (P1).** The single-needle equal-cardinality gadget route
  caps at n^{1/3} (= source, no improvement). codex + Audits A (rigor: SOUND) & B (escape: one credible
  multi-needle escape). Banked P1/N1/B4.
- **D1.2 — Round 2 (escape) result: NEAR-REFUTATION (P2).** The multi-needle/planted-pattern escape
  also caps at n^{1/3} under O(1) coverage; bulk-parity quantitatively dead. codex + Audit C
  (NEAR-PROOF-OF-DEATH). Banked P2/N2. One narrow, evidence-against "new primitive" loophole survives.
- **D1.3 — 🔴 PIVOT (§9.6 human gate): LOWER bound → UPPER bound.** Owner chose (2026-06-21) to pivot to
  proving a **sub-√n / Õ(n^{1/3}) UPPER bound** (close the same Driemel gap from above), over
  escalate-to-web-Pro / pivot-EMD / barrier-paper / stop. Rationale: the LB obstruction is essentially
  *algorithmic* (constant EMST gap is coarsely count-estimable) ⇒ truth likely Θ(n^{1/3}) ⇒ the matching
  algorithm is the natural, equally-SODA-worthy target. **NOT a difficulty downgrade** — the LB route is
  provably (near-)dead (the science), and the new target still closes the same gap at the same venue.
  - New ledger opened: `research_line_emst_upper.md`. LB ledger `research_line_emst.md` frozen as the
    refuted record. Repo/idea name `emst-oracle-lower-bound` now partially STALE (flagged, not renamed).
  - TODO: re-close own-work dedup for the upper-bound contribution (`scripts/own_work_corpus.py` not in
    this isolated repo — flag to owner / parent research-os).
  - First action: extract the source's Õ(√n) algorithm mechanism + the √n bottleneck (facts subagent),
    then write the algorithm-design brief for codex.

- **D1.4 — GPT-5.5-Pro escalation: adopt the `dynamic-weighted-mis-fat-objects` archiving convention
  (owner-requested).** The Pro conversation is human-relayed and multi-round, so it gets a dedicated
  living ledger `docs/webpro_thread_state.md` (modeled on that project's `docs/caching_thread_state.md`)
  + per-round artifact files `webpro_round{N}_{brief|response|audit}.md` (Pro replies pasted VERBATIM by
  the owner; never paraphrased/fabricated). The convention is documented at the top of the thread-state
  file. Codex (xhigh) rounds stay in `attack_loop/`; the Pro thread is tracked separately.

- **D1.5 — Owner steer on the Pro brief: give the RAW original problem; treat our own conclusions as
  possibly WRONG.** Revised `attack_loop/escalation_webpro_brief.md` so **Part I = the self-sufficient
  raw open problem** (Pro can solve from it alone) and **Part II = an optional, UNVERIFIED, "may be
  wrong" appendix** — with *published* facts (source paper, §A) separated from *our* AI-derived claims
  (§B–§D), all explicitly fallible and ignorable. Rationale (owner): some of our automated conclusions
  may be erroneous and must not anchor/mislead Pro; a fresh approach or a refutation of our claims is
  welcome. Pushes §9.2 "freeze FACTS, free METHODS" harder — do not present AI-derived claims as
  established (ties to the corrected U-P5 over-claim; honesty rail).
