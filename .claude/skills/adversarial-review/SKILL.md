---
name: adversarial-review
description: Run a context-blind adversarial review loop on the finished proposal — fresh-context reviewer agents read only what an outsider would see, return scoring-relevant findings, and feed a converging patch cycle. Run after red-team-review (main pipeline) or proposal-patcher (Track B), before export-proposal. Replaces the manual "paste the finished draft into an external AI" step with a native, repeatable loop.
phase: review
composes: [proposal-writer, red-team-review, proposal-storyboard]
conflicts_with: [red-team-review, proposal-editor]  # red-team scores context-rich against internal artifacts and rubrics — do not duplicate S/W/D scoring here; proposal-editor is a global style pass — adversarial patches are surgical
---

# Adversarial Review Skill

## Purpose

Institutionalize the external-reviewer loop. The observed workflow this replaces: after White
Glove, the finished product is pasted into an external AI with no workspace context, it returns
a list of improvements, and applying them measurably improves the proposal. That step works for
three reasons, and this skill preserves all three:

1. **The cold read.** The external reviewer sees only what an evaluator sees — the document.
   Every in-workspace review (Red, Gold, White Glove) is context-rich: it reads
   `working/proposal-plan.md`, the narrative spine, the competitor assessment. Context-rich
   review scores the proposal *you meant to write*; it silently fills gaps with knowledge the
   evaluator will not have. Only a context-starved reader finds the places where the document
   does not stand on its own.
2. **No authorship bias.** The reviewer did not write the prose, so it is not anchored to its
   own phrasing, structure, or claims. The main session that drafted the text cannot provide
   this — its context window contains the rationale for every sentence it would need to doubt.
3. **The loop.** One round of critique is a review; critique → patch → *fresh* re-critique
   until a round comes back dry is a convergence process. Each round uses new reviewer agents
   so round N+1 is as cold as round 1.

The mechanism: spawn **fresh-context subagents** (via the Agent tool), one per reviewer persona,
whose prompts contain *only* the review packet and the persona brief. Findings are consolidated,
triaged by the user, applied surgically under `proposal-patcher` rules, and the loop repeats
with new agents against the patched drafts until it converges.

## Position in the Pipeline

**Main pipeline:** after `/red-team-review` (all gates passed), before `/export-proposal`.
**Track B (white paper):** after `/proposal-patcher`, before `/export-proposal`.

**Required** for the short-form types where a cold read is cheapest and most decisive:
`ota-white-paper`, `white-paper`, and `cso-brief`. Optional for every other type; run it there
when the stakes justify extra rounds, or when you would otherwise reach for an external reviewer.

For the required types, `--tier=quick` (one round, Cold Reader + Skeptical Evaluator) is the
proportionate default; seat the **Staff-Writing Editor** as well whenever the drafting pass ran
with an evaluation-model injection, because writing toward a rubric is what produces the register
this persona exists to catch. Escalate to `--tier=full` only if the quick pass returns Material
findings.

*Why required (2026-07-27, army-brevity-companion).* A single blind round found three required
submission elements that `/compliance-check` had marked `Covered` because a heading existed, two
internal self-contradictions that Red Team, Gold Team, and technical review all passed, and a
flagship proof figure showing the tool generating a recommendation absent from its own input.
Context-rich review scores the proposal you meant to write. Nothing else in the pipeline reads
what is actually on the page.

Do not run it *instead of* Red/Gold — it deliberately lacks the internal context those
gates use, so it cannot check win-theme deployment, compliance coverage, or discriminator
strategy. It checks the one thing they structurally cannot: whether the document survives a
reader who knows nothing you know.

## Modes

| Mode | What it does |
|---|---|
| `--mode=loop` (default) | Full converging loop: panel → triage → patch → re-review, until converged or `--max-rounds` (default 3) |
| `--mode=single` | One round: panel → consolidated findings → triage table. No patching — user applies via `/proposal-patcher` or manually |
| `--mode=export-prompt` | Write a self-contained review packet + persona prompt to `reviews/adversarial/external-review-packet.md` for pasting into **any external model**. Preserves the manual ChatGPT workflow inside the same pipeline |
| `--mode=ingest` | Parse externally-produced findings (pasted text or a file the user points to) into the standard findings format, then continue at the triage step. Pair with `export-prompt` |

`export-prompt` + `ingest` exist so native and external reviewers produce artifacts in the same
format and history. That makes them A/B-comparable: run one round native and one round external
on the same draft state and diff the findings. (Run the external A/B at least once per flagship
pursuit: the live run proved the external reader catches a class the native panel structurally
cannot — see "Stages" and the rendered-artifact rule.)

## Tiers (how much loop to run)

Cost scales with rounds × personas (~80k tokens per reviewer). Match the tier to the stakes.

| Tier | What runs | Use for |
|---|---|---|
| `--tier=quick` | **One round, two personas** (Cold Reader + Skeptical Evaluator), findings-only, **no patch loop** — reviewers report, you triage, done | Routine pursuits; a fast spot-check after a late edit; the default when stakes are modest |
| `--tier=full` (default for flagship) | The converging loop below (panel → triage → patch → re-review), to convergence or `--max-rounds` | Submission-grade, high-value, or contested documents |

When unsure, quick-tier first; escalate to full only if the quick pass returns Material findings.
Do not run a multi-round loop on a document a quick pass would clear, and do not one-round a
flagship submission.

## Stages (what the reviewers read)

| Stage | Reviewers read | Panel | Loop |
|---|---|---|---|
| `--stage=doc` (default) | the finished document (or exported artifact) | full panel | full loop or quick tier |
| `--stage=plan` | a one-page **as-planned abstract** rendered from `working/storyboard.md` (per section: the claim it will make, the proof it will cite, the evaluator takeaway) — **no prose exists yet** | Skeptical Evaluator + Competitor only | one round, no patch loop; findings feed storyboard revision |

`--stage=plan` is context-blind Pink Team: run it **after `/proposal-storyboard`, before
`/proposal-writer`**, so argument-level defects (an unsupported planned claim, a requirement
assigned to no section, a fit-tier inflated past what the evidence will support, a risk the plan
never acknowledges) are caught before a drafting token is spent. The reviewers cannot judge prose
that does not exist; they attack the *plan*. Write findings to
`reviews/adversarial/plan-findings.md`; the human revises the storyboard, not a draft. This is the
highest-ROI insertion the retrospective identified: three of the live run's Material findings were
planning errors that existed in the storyboard before any prose was written.

## The Blind-Reviewer Contract (hard rules)

Each reviewer agent's context is constructed, not inherited. Violating any of these rules
reintroduces the contamination this skill exists to remove.

1. **Reviewers are always fresh subagents.** Never perform the review in the main conversation
   context, even "just this once" — the main context wrote the prose and carries every internal
   artifact.
2. **A reviewer sees only what its persona would see in the real world** (defined per persona in
   [`reference/adversarial-personas.md`](../../../reference/adversarial-personas.md)):
   - The assembled review packet (the draft, in reading order)
   - For solicitation-holding personas only: the solicitation / evaluation criteria from
     `inputs/00_priority/`
   - The persona brief and the findings-format contract
3. **A reviewer never sees:** anything in `working/`, `reviews/`, `my-company/`,
   `inputs/01_customer/` through `inputs/06_notes/`, prior rounds' findings, other personas'
   findings, or the conversation history. The spawn prompt must name the exact file(s) the
   reviewer may read and state: *"Do not read, search, or explore any other file in this
   workspace. Your review is valid only if it is based solely on the files named above."*
4. **Reviewers in the same round run independently.** Convergent findings from independent
   readers are the strongest signal in this skill — do not let them see each other.
5. **Dismissed-finding hygiene happens at consolidation, not in the reviewer prompt.** Do not
   "warn" reviewers off previously rejected findings — that leaks history. Dedupe afterward.
6. **Review the artifact the customer receives, not a proxy for it.** When `/export-proposal`
   has run, assemble the packet from the **exported document's text** (extract the `.docx`) and
   attach the **rendered figures as images**, not `[FIGURE: ...]` descriptions of them. Numbering
   behavior, table pagination, and figure legibility exist only in the rendered artifact; a
   markdown-only packet is blind to an entire defect class — proven live, where a Word
   list-numbering bug and a muddy figure got past the whole native panel and only the external
   reviewer (reading the rendered document) caught them. Run the export polish step before
   assembling the packet; it is not optional.
7. **Every persona brief carries the intake context.** Inline the one-line intake framing from
   `reference/adversarial-personas.md` ("this is one of roughly a dozen submissions triaged in
   one sitting, on a screen, under time pressure") into every spawn prompt. A reviewer told how
   the document will actually be consumed reads like the real reader, not a careful proofreader.

## Round Procedure

### 1. Assemble the review packet(s)

Concatenate the submission-facing drafts (`drafts/*.md`, top level only — `drafts/loose/` is
never part of the packet) in final reading order into
`reviews/adversarial/packet-round-<N>.md`, with a generated header noting round number,
timestamp, and file order. **If `/export-proposal` has run, build the packet from the exported
document's text** (extract the `.docx`) and attach the rendered figure PNGs — review what will
actually be submitted (Contract rule 6).

Also build a **skim packet** (`packet-round-<N>-skim.md`): title, section headings, figure
captions, bold text, and the first sentence of each paragraph. Real triage readers skim before
they read; each reviewer records a provisional triage verdict from the skim **before** receiving
the full packet, and tags each finding "lost at skim" or "lost on close read" — a buried thesis is
a skim failure, a hand-waved integration is a close-read failure, and they need different fixes.

### 2. Select the panel

Default full-tier panel is 3 personas from `reference/adversarial-personas.md`: **Skeptical
Evaluator**, **Cold Reader**, **Competitor's Capture Manager**. Add:
- **Compliance Hawk** when the type has `compliance_sources` (FAR RFP, SBIR, OTA).
- **Accreditation Reviewer** whenever the document makes security, authorization, ATO/IATT,
  cross-domain, or clearance claims. It reads from the approver's seat (the AO staffer, ISSM, or
  CDS owner whose reflex is "that determination is mine to make, not yours to assert") — the one
  seat no win-seeking persona occupies. Added because the live A/B showed the panel's correction
  pressure pushes claims *up* and nothing pushes toward regulatory humility; two overclaims were
  introduced by the panel's own patches.
- **Staff-Writing Editor** for a deliberate register/tone pass (marketing and advisory voice),
  as a one-time seating rather than every round (a new persona guarantees new findings, so it
  cannot converge — see per-dimension convergence).

`--tier=quick` runs **Cold Reader + Skeptical Evaluator** only. White papers / RFIs at
`--stage=doc` drop the Evaluator and Hawk (no rubric to hold); at `--stage=plan` the panel is
Skeptical Evaluator + Competitor. The user can override the panel.

### 3. Spawn the panel (one fresh agent per persona)

Each agent's prompt contains: the persona brief (inlined), the packet path (plus solicitation
path for solicitation-holding personas), the file-access prohibition from the contract, and the
findings-format block below. Instruct each reviewer that its job is to find problems — a review
that returns "this is strong" without locating specific costs is a failed review — but that
every finding must name its cost. Nitpicks with no stated cost are excluded by contract.

**Findings format (per finding, mandatory):**

```markdown
### <persona>-<n>: <short label>
- **Location:** <section heading + paragraph, as findable in the packet>
- **Severity:** Material | Improvement | Polish
- **What the reader experiences:** <the problem as encountered cold — confusion, doubt, an unanswered question>
- **Cost:** <what it costs: a rating, credibility, the reader's next action>
- **Proposed fix:** <specific, minimal; rewritten text where practical>
```

Severity definitions (reviewers apply these, consolidation enforces them):
- **Material** — would change an evaluator's rating, a reader's decision, or leaves a claim an
  evaluator could not verify from the document alone
- **Improvement** — measurably clearer, more credible, or more scorable, but no rating change
- **Polish** — wording preference. Collected, reported, and by default **not patched** — polish
  churn is how loops fail to converge

### 4. Consolidate

In the main context: merge the panel's findings and dedupe (same location + same substance = one
finding; note which personas converged). Then classify each finding against **two** ledgers:

- `reviews/adversarial-dismissed.md` (previously rejected findings) → **drop silently**.
- `reviews/adversarial-settled.md` (findings already accepted-and-patched, plus standing
  **posture decisions** the capture lead has made — e.g. "prime-solo, no partner named"; "no
  financial-management past performance, by structural reality") → mark **carried**, surfaced
  **once** with only *new fix options*, and **never counted as new Material**. This is the fix
  for re-litigation: a blind reader re-finds a settled posture every round, and without this
  ledger it inflates the Material count and breaks convergence (the live loop's single biggest
  noise source).

Drop Polish from the patch candidates (list in an appendix). Write
`reviews/adversarial/round-<N>-findings.md` with the severity-ranked table (columns: `# | Personas
| Dimension | Severity | Location | Finding | Proposed Fix`). Findings flagged by 2+ independent
personas are **convergent** and sort first within their severity band. Tag each finding's
**dimension** (substance / readability / register / accreditation) for per-dimension convergence.

**Fact-request channel.** Any finding whose fix needs a fact only the capture lead holds (a date,
a metric, an event anchor, a clearance count) goes to
`reviews/adversarial/round-<N>-fact-requests.md` as *claim → what a reviewer needs → proposed
honest fallback if no fact exists*. Answered facts flow to `my-company/evidence-ledger.json`
**first**, then into patches — the loop is an evidence-elicitation engine, not only a prose fixer
(the live run created two ledger items and corrected one wrong claim this way).

**Claims register.** Append every finding that would **raise or lower a claim's confidence** to
`reviews/adversarial/claims-register.md` (claim, direction, round). Correction pressure is
directional — the skeptic and competitor push claims *up*, nothing pushes toward humility — so any
confidence-raising patch must pass **both** the Skeptical Evaluator and the Accreditation Reviewer
next round before it stands. This generalizes "if two rounds disagree, show both" from reactive to
preventive.

### 5. Triage (human gate — mandatory)

Present the table and stop: *"Round <N>: <M> new findings (<m> Material, <i> Improvement, <p>
Polish excluded; <c> carried). Accept / reject / defer each — or 'accept all Material'."* The
user's judgment here is the loop's steering wheel; never auto-apply.

- **Rejected** findings append to `reviews/adversarial-dismissed.md` with a one-line reason —
  future rounds dedupe against it.
- **Accepted-and-patched** findings, and any **posture decision** the user states during triage
  ("we are not naming a partner"), append to `reviews/adversarial-settled.md` with the residual
  in one line — this is what stops the next round re-finding them.
- **Deferred** findings carry to the round log unapplied and are re-surfaced (not re-derived)
  next round.
- **Fact-request answers** the user supplies update the evidence ledger first, then unblock their
  findings.

### 6. Patch (accepted findings only)

Apply under **`proposal-patcher` rules** ([SKILL.md](../proposal-patcher/SKILL.md)): back up
each file to be modified to `reviews/pre-patch/`, minimum effective dose, match the surrounding
voice, one finding one fix, never touch sections with no accepted findings, never fabricate a
capability or fact to satisfy a finding (`<!-- PATCH-BLOCKED -->` instead). Log applied patches
in the round file.

### 7. Verify the patches didn't regress the document

```bash
python scripts/prose-lint.py --proposal <slug>          # patched prose meets voice doctrine
python scripts/lint-document-structure.py --proposal <slug>
python scripts/check-strengths.py --proposal <slug>     # Gold Team Significant Strengths survived the patches
```

A `check-strengths.py` failure means a patch stripped a load-bearing claim — restore from
`reviews/pre-patch/` and re-patch smaller. Do not proceed to the next round with a failing gate.

**Patch-regression micro-check.** Before the next round, spawn **one** fresh agent that reads
*only the changed passages plus every passage that references them* and checks internal
consistency: a caption that now contradicts a table, a claim a patch strengthened past what
another section supports, a cross-reference a renumber broke. This costs ~5% of a round and
catches the defect class where a patch introduces the next round's finding — observed live twice
(a deferral phrasing that read as evasive, a figure caption that contradicted a table row). Fold
any confirmed regression into the current patch set rather than carrying it a full round.

### 8. Snapshot the round

Append exactly one JSON line to `reviews/adversarial-history.jsonl`, conforming to
[`reference/schemas/adversarial-round.schema.json`](../../../reference/schemas/adversarial-round.schema.json):

```json
{"schema_version":"adversarial-round.v1","timestamp":"<ISO-8601>","proposal_id":"<slug>","round":1,"reviewer":"native","personas":["skeptical-evaluator","cold-reader","competitor-capture-manager"],"counts":{"material":2,"improvement":5,"polish":4},"convergent_findings":1,"accepted":6,"rejected":1,"deferred":0,"patches_applied":6,"converged":false,"notes":null}
```

Append-only, like `gold-team-history.jsonl` — the series is the evidence that the loop
converges (or that it doesn't and should be re-tuned). `"reviewer"` is `"native"` or
`"external"` so A/B comparisons fall out of the history for free.

### 9. Converge or go again

Convergence is measured **per dimension**, not across the whole panel — adding a persona
guarantees new findings and would break a whole-panel measure by construction:

- **substance** — Skeptical Evaluator + Competitor + Accreditation Reviewer
- **readability** — Cold Reader
- **register** — Staff-Writing Editor

A dimension is **converged** when its round yields **zero new accepted Material** and **≤1 new
accepted Improvement** (carried findings do not count). A newly seated persona starts its **own**
two-round mini-loop; other dimensions converge independently. The loop as a whole stops when every
seated dimension has converged, at `--max-rounds` (default 3), or on user request. **Report the
per-dimension state honestly** — "substance converged in round 3; register newly seated, one round
in" — rather than claiming a dry round a mid-loop panel change makes impossible.

Next round spawns **new** agents (never reuse a reviewer — it has seen the previous draft)
against a freshly assembled packet of the patched drafts.

## Anti-Churn Discipline

The failure mode of any critique loop is oscillation: round 2 "fixes" round 1's fixes. Rules:

- **Polish findings are never patched by default.** If the user wants a polish pass, that is
  `/proposal-editor`'s job (main pipeline) or a deliberate one-time decision — not loop fuel.
- **The dismissed ledger is binding.** A finding substantively identical to a dismissed one is
  dropped at consolidation, silently. The user rejected it once; the loop does not re-ask.
- **A finding must name its cost.** "This sentence could be smoother" fails the contract.
  "The reader cannot tell whether the 14-month figure is measured or projected, and an
  evaluator cannot credit an unverifiable claim" passes.
- **Strengths stay.** Same rule as the patcher: never "improve" text the Gold Team scored as a
  Strength unless an accepted Material finding lands in that exact passage — and then run
  `check-strengths.py` before continuing.
- **If two rounds disagree** (round 2 flags what round 1's accepted patch introduced), stop and
  show the user both findings side by side instead of patching back and forth.

## Realism passes (optional, high-value)

Two passes that make the panel read more like the real intake, added because the base loop reviews
a proxy (a text packet, in isolation) for how a document is actually consumed (a rendered
artifact, third in a stack, under time pressure).

**Visual pass.** Rasterize the exported `docx → PDF` pages to images and seat a **vision-capable**
reviewer whose only input is the page images, hunting for what lives only in the rendered artifact:
figure legibility, table rows breaking across pages, wall-of-text pages, lists that mis-render, and
whether the document is skimmable as a physical object. This is **not optional for any document
with figures or dense tables** — a text-only panel is structurally blind to it (the live A/B's
list-numbering bug and muddy figure were both visual-only defects). Findings →
`reviews/adversarial/visual-findings.md`.

**Comparative decoy triage.** Real evaluation is a ranking, not an absolute read. Generate 2–3
synthetic competitor submissions in distinct voices (a big-integrator incumbent, a generic
AI-startup) and have the Skeptical Evaluator **force-rank the stack and write the triage memo**.
"Would an evaluator invite us?" becomes "did we beat the decoys, and on what line?" — which also
operationalizes the Competitor persona's counter-pitch by feeding it in as one of the decoys.
Findings → `reviews/adversarial/decoy-triage.md`.

## Outputs

| Artifact | Purpose |
|---|---|
| `reviews/adversarial/packet-round-<N>.md` (+ `-skim.md`) | What the reviewers actually saw — full packet and skim packet (auditability) |
| `reviews/adversarial/round-<N>-findings.md` | Consolidated, dimension-tagged, triaged findings + patch log for the round |
| `reviews/adversarial/round-<N>-fact-requests.md` | Facts a fix needs that only the capture lead holds → answered into the evidence ledger |
| `reviews/adversarial/claims-register.md` | Every confidence-raising / lowering patch; must pass skeptic + accreditation next round |
| `reviews/adversarial/plan-findings.md` | `--stage=plan` output — argument-level defects against the storyboard, before drafting |
| `reviews/adversarial/visual-findings.md` | Visual-pass output — rendered-artifact defects (figures, pagination, list rendering) |
| `reviews/adversarial/decoy-triage.md` | Comparative-decoy output — force-ranked triage memo vs. synthetic competitors |
| `reviews/adversarial-review.md` | Running summary: rounds, per-dimension convergence state, link per round |
| `reviews/adversarial-dismissed.md` | Append-only rejected-findings ledger (anti-relitigation) |
| `reviews/adversarial-settled.md` | Append-only accepted-and-patched + posture-decision ledger (stops re-litigation) |
| `reviews/adversarial-history.jsonl` | Append-only round snapshots (per-dimension convergence + native-vs-external evidence) |
| `reviews/adversarial/external-review-packet.md` | `export-prompt` mode only — paste-ready packet for an external model |

Snapshot lines may carry optional `tier`, `stage`, and `dimensions` fields alongside the base
schema; keep them backward-compatible (extra keys, never renamed base keys).

**Critical rule: always write to files — never just display in chat.**

## Activity Trail

On completion (per invocation, not per round), append to `working/activity.md`:

```
## <timestamp> — adversarial-review [<mode>] — <R> rounds, <A> findings applied, <D> dismissed, converged: <yes/no> → reviews/adversarial-review.md
```

Append one JSON line to `working/ai-runs.jsonl` per reviewer agent spawned **plus one** for the
orchestrating pass, per [`reference/schemas/ai-run.schema.json`](../../../reference/schemas/ai-run.schema.json)
(`"job_type":"review"`, notes like `"round 2 persona: cold-reader"`). The panel is the dominant
token cost of this skill; the ledger should show it.

## Final Rule

This skill's value is exactly proportional to how cold its reviewers are. Every convenience that
leaks context to a reviewer — reusing an agent, summarizing the win themes "for efficiency,"
reviewing in the main session — converts it back into the in-house review it was built to
escape. When in doubt, the reviewer knows less.
