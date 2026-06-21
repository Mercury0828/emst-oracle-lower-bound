# Phase-0 Bootstrap — Tight EMST Range-Counting-Oracle Lower Bound (target: SODA)

You are starting a fresh, independent execution of one idea: a **query lower bound** proving
**Ω(n^{1/2−o(1)})** range-counting-oracle queries are necessary to (1±ε)-estimate the Euclidean MST
weight, closing the Ω(n^{1/3}) vs Õ(√n) gap of Driemel et al. (SoCG 2025, arXiv:2504.15292). Your
constitution is **`guide.md`** in this same folder. Read it **in full** before anything. It is
**READ-ONLY** — never edit it; all amendments go to `docs/guide_amendments.md`.

## 🧭 Your role — orchestrator / referee / archivist, NOT a solo prover (read first)

This is a theory project run as an **external-solver attack loop** (`guide.md` §9). The division of
labor is fixed from day 0:

- **The mathematics (the gadget C1, the O(1)-coverage packing C2, the hitting reduction C3,
  counterexamples) is originated by an external attacker: codex GPT-5.5-xhigh by default, escalating
  to web GPT-5.5-Pro (human-relayed) on a defined stall.** You do **not** try to prove C1/C2/C3
  yourself.
- **You are the orchestrator / referee / archivist:** you write method-free briefs (freeze FACTS,
  free METHODS), run independent **fresh-context** adversarial audits of every attacker reply,
  classify findings FATAL/GAP/MINOR, maintain the frozen **research-line ledger**, catch drift and
  circularity — above all the **Ω(log m) trap** (`guide.md` §0 framing note: a bit-accounting
  mis-packaging of the hitting argument), and decide escalate-vs-continue-vs-stop.
- You must **never smuggle an unproven implication into a brief** — e.g. "the gadget is sparse ⇒
  coverage is O(1)", "O(1) bits/query ⇒ the lower bound", or "Czumaj's emptiness Ω(√n) ⇒ a counting
  bound". State what is **known**, pose the open question cleanly, let the attacker reason.

**Phase 0 itself is mostly screening, not attacking** — but set the roles, the ledger, and the repo
up now so the attack loop (Phase 1+) runs correctly.

## Step 0 — Enter plan mode first

Before any action: **enter plan mode.** Read `guide.md` end to end, then decompose the Phase-0 tasks
below into an **ordered sub-task checklist**. **Then exit plan mode and execute Phase 0
autonomously** — once the plan is set, do not stop for per-step approval. The **only mandatory stop
is human gate #1 at the very end** (after the verdict report). Do not scaffold or scan before the
plan is set.

**Working directory:** scaffold the repo **inside this deepdive folder**
(`deepdive/emst-oracle-lower-bound/`) unless the owner says otherwise.

## Target venue & the 5 SODA constraints to keep in view from day 0

- **Target venue = SODA** (ACM-SIAM Symposium on Discrete Algorithms). Full-paper deadline
  **2026-07-09** (re-confirm against the official SODA 2027 CFP in the scan — format/blind/deadline
  change by year). **Pure-theory venue: results = theorems + proofs + bounds, NOT experiments.**
  SoCG is the sibling venue (the source paper's home), near-identical conventions.
- **Writing pipeline already exists at `venue-prompts/soda/`** (4 stages). You do NOT use it in
  Phase 0 — it's for the writing phase. Just know it's there.

1. **Strength gate: "closes" vs "improves" (decisive).** Reaching **Ω(n^{1/2−o(1)})** matching Õ(√n)
   up to n^{o(1)} *closes/tightens* the gap (strongest headline); a weaker exponent (e.g. Ω(n^{2/5}))
   merely *improves* it (still publishable, weaker headline). A SODA PC polices this. Which you get is
   decided by the two load-bearing cruxes (C1)/(C2) — **your Phase-0 job includes assessing the best
   achievable exponent.** (Per `guide.md` §9.0b this is the *science*, decided by the construction —
   NOT a difficulty-driven downgrade.)
2. **The per-query coverage bound is live-or-die (the residual risk).** The lower bound is a
   **hitting/coverage argument** (a random hidden "needle" cell; each query rectangle is sensitive to
   O(1) candidate cells ⇒ Ω(#cells) queries to hit it), **NOT a bit-counting argument** — see
   `guide.md` §0 FRAMING NOTE (naive mutual-information accounting only gives Ω(log #cells), the
   trap). A range-**counting** query returns an **exact integer count** (a sum over the cells a
   rectangle covers), not a 0/1 emptiness bit, so a large rectangle's count may be **jointly sensitive
   to ω(1) candidate cells** — which would let o(#cells) queries cover all candidates and cap the
   exponent **below 1/2**. Keeping per-query **candidate-distinguishing-power O(1)** (via an
   induced-matching / Ruzsa–Szemerédi packing) is the single point the headline lives or dies on
   (`guide.md` §6 Component 2, §9, §11 risk 1). **Your Phase-0 (C2) screen measures exactly this
   coverage quantity (not raw bits).**
3. **Pure theory, no experiments.** Your Phase-0 screens (gadget detectability; per-query coverage)
   are **internal de-risking only** — they decide whether the n^{1/2} target is worth attacking; they
   are *not* paper results. **Adversarial input is the kill metric; a clean plot on random input is
   not evidence.**
4. **No defensive writing / no hard guarantees.** Scope (the (1±ε) error regime, the Δ=O(n) budget,
   the n^{o(1)} slack) is stated as **confident model definitions inside the theorem**, not a
   "Limitations" section. Never claim "tight/closes" unless n^{1/2−o(1)} is actually proven. Cite
   Czumaj's Ω(√n) only as motivation (weaker **emptiness** oracle, deterministic, O(n^{1/4}) error) —
   never as if it proves the counting-oracle claim.
5. **Blind/format per the current CFP.** Re-confirm SODA 2027 format (single-column, 11pt, 1-inch
   margins; first ~10 pages convey the merits; no hard page limit; appendix unlimited; refs not
   counted) and blind policy against the official CFP.

## This session does Phase 0 ONLY, then STOP at human gate #1

Do **only** Phase 0, then stop. Deliverables:

1. **Repo scaffold (day-0 products).** Create:
   - `PROJECT_STATE.md` — current progress / frozen results & numbers (+ artifact paths) / current
     phase / TODO + pending human decisions / confidence trend.
   - `DESIGN_DECISIONS.md` — append-only decision log.
   - `docs/guide_amendments.md` — append-only (the only place guide changes are recorded).
   - **`research_line_emst.md` — the append-only research-line ledger (`guide.md` §9.5 format):**
     frozen model/notation; **proven `P*`** ("use freely, do not re-derive"); **refuted `N*`** ("do
     NOT attempt" + reason); **barriers `B*`**; the exact open problem as currently reduced; a
     confidence trend with dates; a HEADLINE line at top. Seed it now with the known barriers
     (the n-point/Δ=O(n) budget; the Ω(log m) trap as a proof barrier; counting ⊋ emptiness so
     coverage can exceed 1) — the attack loop (Phase 1+) lives or dies on this ledger. 🔴 Re-read it +
     frozen artifacts before continuing — never work from memory.
   - `PROOF_REVIEW/` — created **empty** with a one-line stub (`PROOF_REVIEW/README.md`: "populated
     from the attack loop on; holds frozen proofs + proof-review tables"). NOT populated in Phase 0.
   - `sim/` — the two de-risking screens (Python): `sim/c1_gadget_detect.py` (C1), `sim/c2_coverage.py`
     (C2), `sim/run_all.py` (single entry point regenerating every figure/number), `sim/README.md`.
     Local venv at `sim/.venv` (don't touch the system env); on Windows/PowerShell activate with
     `.venv\Scripts\Activate.ps1`. Exact-EMST dependency: `scipy` (Delaunay + Kruskal/union-find over
     Delaunay edges).

2. **Literature kill-scan** (apply `guide.md` §3 criteria — frozen; do not re-invent). For each query
   in §3's mandatory coverage list:
   - Record every query + what was found (a per-query log in `lit/SCAN_REPORT.md`).
   - Sweep the required sources/venues + DBLP pages in §3 (Driemel, Monemizadeh, Woodruff, Czumaj,
     Har-Peled, Indyk; SODA/SoCG/STOC/FOCS/ICALP/ESA 2024–2026; arXiv cs.CG/cs.DS/cs.CC).
   - **Special assignment (three threads):** one hunts a paper that *already* improves the
     counting-oracle EMST lower bound past n^{1/3} (the **RED scoop**); one hunts an **o(√n) upper
     bound or sub-√n impossibility barrier** (the **RED ceiling** — would mean n^{1/2} is
     unreachable); one hunts any prior **space-efficient MST-distinguishing gadget** or **per-query
     O(1)-cell-coverage packing for COUNTING (not emptiness) queries**.
   - Check the **latest arXiv version of 2504.15292** (v2/v3 with a tightened bound?) and **all papers
     citing it**. Confirm arXiv:2603.20943 (convex hull, range-emptiness) does NOT touch the MST
     counting-oracle bound. Get the **exact Czumaj et al. citation** and confirm its
     oracle/regime/error.
   - Produce a **concern table** + a **GREEN/YELLOW/RED verdict** per §3's kill criteria (including the
     strength-gate assessment: is the full n^{1/2} reachable, or only a weaker exponent?).
   - **Spawn one independent fresh-context subagent** for a second opinion on the verdict — and have it
     ALSO answer the §10 paper-orientation three questions (is the contribution on track for SODA / has
     the thinking drifted / any other problem), writing `gate1_paper_orientation_audit.md`.

3. **Load-bearing-crux de-risking screens** (`guide.md` §7 — read it; it specifies exactly what to
   build). **Pre-register the expected trend + a falsifier before running each. Adversarial input is
   the kill metric.**
   - **(C1) Gadget-detectability screen.** Build candidate heavy/sparse gadgets; compute **exact EMST
     weight** (scipy Delaunay + Kruskal, or direct for tiny n) for all-sparse vs one-heavy; measure
     the **heavy-vs-sparse gap as a fraction of total w(P)**, checked against the **§4 target
     inequality** Θ(n^a)−Θ(n^b) ≥ ε·w(P). **Swept variable:** fix m cells, p points/cell, global
     n=m·p; sweep p between p≈n^{2/3} (m≈n^{1/3}) and p≈n^{1/2} (m≈n^{1/2}). Pre-registered
     expectation: gap fraction stays **≥ a fixed ε**. **Kill signal:** fraction shrinks below ε and
     keeps shrinking as p→n^{1/2}. Record the smallest point-budget at which (1±ε)-detectability
     survives. **Scale caveat (put in the report):** at a few thousand points m≈50 and the budgets
     differ by only a small factor — the screen shows the **trend**, not the asymptotic crossover.
   - **(C2) Per-query coverage screen (THE decisive measurement).** Build the **baseline packing** (m
     candidate gadgets on a √m × √m subgrid, one heavy — the RS-optimal packing is a later proof
     obligation, not Phase 0); enumerate axis-aligned query rectangles; for each measure its
     **candidate-distinguishing-power = #candidate cells whose heavy/sparse flip changes the COUNT**;
     report the **max over rectangles**, swept as m grows. Pre-registered expectation: **flat / O(1)**.
     **Kill/strength signal:** max coverage **growing polynomially with m** (m^{Ω(1)}) → exponent capped
     below 1/2 (m^{o(1)} growth still supports n^{1/2−o(1)}); a baseline screen showing growth ⇒
     redesign/escalate/human gate, NOT an auto-kill of the target (the residual-risk realization). **Measure the COUNT, not emptiness.** **Secondary
     proxy:** count↔hidden-index mutual information **as a ratio to the log m baseline** (raw bits
     grow like log m trivially; only a *climbing ratio* is a signal — never treat raw small
     bit-counts as a pass). **For contrast** measure emptiness-query coverage on the same packing
     (hypothesis, not guaranteed: ≤ counting coverage; if equal, that is itself informative).
   - **Protocol:** fixed seeds; **random placements = smoke/sanity check ONLY (never de-risk
     evidence); adversarial placements = the only de-risk evidence** (adversarial = placements
     designed to make a single rectangle straddle many candidates, stress-testing C2); report
     mean ± CI **and the tail (max) — the adversarial max is the kill metric, the mean is secondary**;
     every figure regenerated by `sim/run_all.py`; freeze all numbers in `PROJECT_STATE.md`.
   - **Scope of evidence:** a clean small-scale screen is a **necessary kill-screen, NOT sufficient
     proof.** Asymptotic detectability and asymptotic O(1)-coverage are *proof obligations* (the
     attack loop), not established by simulation. The screens only decide whether to *attempt* the
     proof.

4. **Verdict report** — write to **`PHASE0_REPORT.md`** (mirror the headline verdict into
   `PROJECT_STATE.md` + the ledger HEADLINE). Tight but **do not truncate the analysis** (project red
   line). Cover: kill-scan GREEN/YELLOW/RED + the independent second opinion (scoop? ceiling?); the
   (C1) gap-fraction trend as p→n^{1/2} (+ smallest detectable budget); the (C2) per-query coverage
   trend as m grows (flat O(1) vs growing), adversarial max emphasized, random AND adversarial; the
   **best achievable exponent** the screens support (n^{1/2−o(1)} "closes" vs a weaker "improves");
   and the open items for human gate #1. **End with one line:** "given what we see, how far is a
   submittable SODA paper, and has the thinking drifted?" (the paper-orientation check — `guide.md`
   §10).

**Then STOP at human gate #1.** Do not start the attack loop (the C1 gadget proof etc.). The human
decides: pursue the full n^{1/2−o(1)} target vs settle for the best supportable exponent; and, if a
RED kill fired, pivot-vs-stop (`guide.md` §9.6).

## The three human gates (Phase 0 hits only #1; know all three exist)

- **Gate #1 (end of Phase 0, here):** strength decision (closes vs improves) / kill / pivot.
- **Gate #2 (end of the attack loop):** AI-convergence handoff — **"AI-verified ≠ proved"**: any
  converged result is conditional pending human-expert verification of the full argument (esp. the C3
  counting-transcript coupling) + independent human check of AI-produced substrate (C1 exponents, C2
  RS layout) + a final preprint priority sweep.
- **Gate #3:** venue / scope / pre-submission.

## Operating rules

- **Highly autonomous — minimize interrupting the human.** Once Phase 0 is broken into subtasks,
  execute the whole list straight through. **Stop to ask the human ONLY at** the three gates above, an
  irreversible/outward action, or a true blocker (missing critical info you cannot proceed without).
  **Never** pause after each subtask to ask "next I'll do X — continue?" — default to continuing until
  human gate #1. Record decision points in `DESIGN_DECISIONS.md` / `PROJECT_STATE.md` and keep moving.
- **🔴 NO-RETREAT red line (`guide.md` §9.0b).** Target = SODA, contribution = closing (or, only on
  proof-of-death, honestly improving) the gap. **Difficulty / being stuck / time pressure are NEVER
  grounds to weaken the contribution or retarget to an easier venue** — hard ⇒ escalate the attack
  (codex-xhigh → web-Pro → fresh-context attacker) at full force. The ONLY thing that changes the
  target is the science being **provably dead** (refutation / proven impossibility / confirmed scoop),
  surfaced at a human gate. ("closes"→"improves" because the construction provably caps below 1/2 is
  proof-of-death for the n^{1/2} target, NOT a difficulty downgrade — report it honestly.)
- **kill→pivot self-awareness (`guide.md` §9.6).** If Phase 0 triggers a RED kill (scoop / ceiling),
  don't just "STOP": in the verdict, assess whether the substrate already built points at an adjacent
  open problem (e.g. the EMD range-counting-oracle bound) and present kill + candidate pivot + rough
  budget at gate #1. Kill fires on **proof-of-death only**, never on difficulty.
- **Never fabricate.** No invented results, bounds, exponents, or citations. If a web source is
  inaccessible or a paper can't be retrieved, list it explicitly and continue. If you cannot retrieve
  arXiv:2504.15292 to re-confirm the §4 construction numbers, say so — those numbers are load-bearing.
- **Pre-register before measuring:** expected trend + a falsifier first, then run. Mismatch → diagnose
  (bug vs real finding), record honestly. **Never shape-force** a gadget/packing to make a plot clean.
- **Confidence trend is a first-class signal:** record a % per round; a sustained drop ⇒ escalate /
  fresh-agent reset (attack harder), never a downgrade.
- **Progress discipline (critical):** update `PROJECT_STATE.md` + the research-line ledger at every
  step. **When context grows long, re-read the ledger + `PROJECT_STATE.md` + frozen artifacts before
  continuing — never from memory** (memory ⇒ exponent drift n^{1/2} vs n^{1/2−o(1)}, Δ/ε/a/b notation
  collisions, repeated labor).
- **Local env only:** project venv/conda for all simulation; don't modify the system environment.
- **Honesty rail:** "AI-verified ≠ proved" — even a converged attack loop yields only a
  human-pending result; never present AI output as a finished theorem.
- **🌐 Language discipline:** your **dialogue / verdict reports / the ≤15-line summary to the owner**
  are in **Chinese** (unless the owner says otherwise); but **work-products** — `PROJECT_STATE.md`,
  the research-line ledger, `lit/SCAN_REPORT.md`, `PHASE0_REPORT.md`, briefs, the paper, code — stay
  in **English** (the working language, aligned to SODA). Said briefly: spoken-to-the-human → Chinese;
  written-to-the-archive / to-be-submitted → English.

End with a **≤15-line Chinese summary** + the explicit list of pending human decisions for gate #1.
