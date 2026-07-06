---
name: adversarial-review
description: Run a context-blind adversarial review loop on the finished proposal — fresh-context reviewer agents read only what an outsider would see, return scoring-relevant findings, and feed a converging patch cycle. Run after red-team-review (main pipeline) or proposal-patcher (Track B), before export-proposal. Replaces the manual "paste the finished draft into an external AI" step with a native, repeatable loop.
phase: review
composes: [proposal-writer, red-team-review]
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

This skill is optional for every proposal type and never appears in a type's `required_skills`.
Run it when the stakes justify extra rounds, or when you would otherwise reach for an external
reviewer. Do not run it *instead of* Red/Gold — it deliberately lacks the internal context those
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
on the same draft state and diff the findings.

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

## Round Procedure

### 1. Assemble the review packet

Concatenate the submission-facing drafts (`drafts/*.md`, top level only — `drafts/loose/` is
never part of the packet) in final reading order into
`reviews/adversarial/packet-round-<N>.md`, with a generated header noting round number,
timestamp, and file order. If `/export-proposal` has already run, prefer the exported document
text — review what will actually be submitted.

### 2. Select the panel

Default panel is 3 personas from `reference/adversarial-personas.md`: **Skeptical Evaluator**,
**Cold Reader**, **Competitor's Capture Manager**. Add the **Compliance Hawk** when the type has
`compliance_sources` (FAR RFP, SBIR, OTA). White papers / RFIs default to Cold Reader +
Competitor only — there is no rubric for the Evaluator to hold. The user can override the panel.

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

In the main context: merge the panel's findings, dedupe (same location + same substance = one
finding, note which personas converged on it), drop findings that restate anything in
`reviews/adversarial-dismissed.md`, and drop Polish findings from the patch candidates (list
them in an appendix). Write `reviews/adversarial/round-<N>-findings.md` with a severity-ranked
table:

| # | Personas | Severity | Location | Finding | Proposed Fix |
|---|---|---|---|---|---|

Findings flagged by 2+ independent personas are marked **convergent** and sort first within
their severity band.

### 5. Triage (human gate — mandatory)

Present the table and stop: *"Round <N>: <M> findings (<m> Material, <i> Improvement, <p>
Polish excluded). Accept / reject / defer each — or 'accept all Material'."* The user's judgment
here is the loop's steering wheel; never auto-apply.

- **Rejected** findings append to `reviews/adversarial-dismissed.md` with a one-line reason —
  this is the anti-relitigation ledger; future rounds dedupe against it
- **Deferred** findings carry to the round log unapplied and are re-surfaced (not re-derived)
  next round

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

**Converged when:** a round yields **zero new accepted Material findings** and **≤1 new
accepted Improvement finding**. Also stop at `--max-rounds` (default 3) or on user request —
report unconverged state honestly rather than quietly stopping.

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

## Outputs

| Artifact | Purpose |
|---|---|
| `reviews/adversarial/packet-round-<N>.md` | What the reviewers actually saw (auditability) |
| `reviews/adversarial/round-<N>-findings.md` | Consolidated, triaged findings + patch log for the round |
| `reviews/adversarial-review.md` | Running summary: rounds, counts, convergence state, link per round |
| `reviews/adversarial-dismissed.md` | Append-only rejected-findings ledger (anti-relitigation) |
| `reviews/adversarial-history.jsonl` | Append-only round snapshots (convergence + native-vs-external evidence) |
| `reviews/adversarial/external-review-packet.md` | `export-prompt` mode only — paste-ready packet for an external model |

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
