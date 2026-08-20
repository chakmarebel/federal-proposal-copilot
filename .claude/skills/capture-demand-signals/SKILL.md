---
name: capture-demand-signals
description: Capture what customers are asking for into the workspace-global demand signal register, from a pursuit's requirement matrix or from conference / one-on-one / trial / debrief notes. Confirms a controlled capability theme and BD's status for each ask, then appends to signals/demand-signals.jsonl for the BD-to-CTO sync loop. Run after proposal-solution-architect on an active pursuit, and within 48 hours of any customer conversation.
phase: capture
composes: [opportunity-quick-look, proposal-solution-architect]
conflicts_with: []  # unique: the only skill that writes the workspace-global demand register; compliance-check tracks requirements WITHIN one bid, this aggregates demand ACROSS bids
---

# Capture Demand Signals

## Purpose

Turn requirements the customer stated — in a solicitation, at a conference, across a table, during
a trial — into structured records in `signals/demand-signals.jsonl`, the workspace-global register
that feeds the CTO shop's view of demand.

This skill is the only writer of that register. It exists because the demand signal already lives in
this workspace and never aggregates: forty pursuits hold their own requirement matrices, each with an
honest Gap/Risk column, and none of them roll up. Engineering ends up hearing requirements as
anecdotes from whoever was in the room last.

Read [docs/BD-CTO-DEMAND-SIGNAL-SYNC.md](../../../docs/BD-CTO-DEMAND-SIGNAL-SYNC.md) for the whole
loop. This skill is the capture half; `scripts/build-demand-signal-brief.py` is the reporting half.

## When to run

| Trigger | Mode | Timing |
|---|---|---|
| A pursuit's requirement matrix is written | `--from-proposal <slug>` | Right after `/proposal-solution-architect`, before drafting |
| Conference, industry day, one-on-one, trial, demo, or debrief | `--from-notes <path>` | Within 48 hours |
| A pursuit closes (win, loss, or no-bid) | `--from-proposal <slug>` | At close, to record `bid_impact` truthfully |

The 48-hour window on conversations is not bureaucratic. Verbal asks are the most valuable class in
the register — they precede the written requirement by 6 to 18 months — and their value is in the
customer's own words, which are gone from memory within a week.

## Not this skill's job

- **Tracking requirements inside one bid.** That is `/compliance-check` and the compliance matrix.
  This register is cross-pursuit and exists for the roadmap conversation, not for the bid.
- **Recording submission mechanics.** Page limits, cover pages, and POC blocks are not demand
  signals. They tell engineering nothing and dilute the channel.
- **Deciding what engineering builds.** BD records the ask and its cost to the bid. The disposition
  is engineering's, captured through the brief, never guessed here.

## Inputs

1. `reference/capability-themes.md` — the controlled vocabulary. **Required.** Never invent a theme
   inline; if nothing fits, say so in the run summary and propose the addition as a separate edit.
2. `reference/schemas/demand-signal.schema.json` — field contract.
3. `signals/demand-signals.jsonl` — the existing register, to continue `signal_id` numbering.
4. Mode-specific source:
   - `--from-proposal <slug>`: `proposals/<slug>/working/requirement-matrix.md` (primary),
     `working/quick-look.md`, `working/assumptions-and-risks.md`, `working/proposal-type.md`
   - `--from-notes <path>`: the note file, typically under `proposals/<slug>/inputs/06_notes/` or
     `scrubs/`

## Procedure — `--from-proposal <slug>`

**Step 1. Run the mechanical extractor.**

```bash
python scripts/extract-demand-signals.py --proposal <slug>
```

It parses the requirement matrix's tables, drops submission mechanics and internal pitch framing,
suggests a `capability_theme` by keyword, and infers `our_status` from the Gap/Risk prose. Output
lands in `signals/candidates/<date>-candidates.jsonl`.

**Step 2. Confirm each candidate.** The extractor is a first pass and says so: `theme_suggestion`
may be null, and `our_status_inferred` is `unknown` whenever the gap prose does not support an
inference. For each candidate, settle four things:

- **Theme.** Confirm the suggestion or replace it with a theme from the vocabulary. A null suggestion
  means classify it yourself. If the ask genuinely fits no theme, drop the candidate rather than
  forcing it.
- **`our_status`.** `shipping` only when a ledger item could prove it today. `prototype` when it
  exists but is not productized. `roadmap` when BD believes it is planned. `gap` when we could not
  answer. `no-plan` for a gap with no known intent to close it. Never leave `unknown` in the
  register — resolve it or drop the row.
- **`demand_strength`.** Scored criterion, pass/fail, stated preference, or conversational.
- **`bid_impact`.** The most load-bearing field. What did this ask actually cost: prose hedged,
  criteria scored low, a teammate brought in, a question declined, a no-bid. Write it plainly and
  leave it null when the ask cost nothing. "Customer wanted X" is a wish; "we hedged 3.2 and teamed
  it to Scale" is a requirement.

**Step 3. Merge duplicates against the existing register.** The same customer asking the same thing
in a new solicitation is a **new signal** — recurrence is the point of the register. The same ask
appearing twice in one matrix is not. Check `source_ref` before appending.

**Step 4. Append.** One JSON object per line, `signal_id` continuing from the register's maximum,
never renumbering. Set `schema_version` to `demand-signal.v1` and leave every `cto_*` field null —
those belong to engineering.

**Step 5. Validate.**

```bash
python scripts/build-demand-signal-brief.py --validate-only
```

An unknown theme is a hard failure: a typo silently splits a theme in two and understates its
weight, which is the one error that corrupts the ranking the CTO shop is reading.

## Procedure — `--from-notes <path>`

Same confirmation discipline, different extraction. There is no table to parse, so read the note and
pull out only the sentences where the customer stated a need. Rules that matter here:

- **Quote, do not paraphrase.** Put the customer's words in `requirement`. Verbatim language is what
  engineering trusts and what makes a recurring ask recognizable across three different agencies.
- **`date_observed` is the date of the conversation**, not today. The lead time between a verbal ask
  and its appearance in a solicitation is a number worth being able to compute later.
- **Attribute to the organization, not the individual.** `customer` is the agency or command; put the
  person in `notes` if it matters.
- **`demand_strength: curiosity` is normal and valuable here.** An ask nobody has funded yet is
  exactly the signal with the most roadmap lead time. Do not inflate it to `desired` to make it look
  more important.
- **`proposal_slug` may be null.** Relationship conversations often precede any pursuit.
- Separate what the customer asked for from what we pitched. A note recording our own demo script is
  not a demand signal.

## Output

Appended records in `signals/demand-signals.jsonl`. Report in the run summary:

- how many signals were appended, and the `signal_id` range
- the theme breakdown
- how many carry `our_status: gap` or `no-plan` (these become the CTO shop's queue)
- any ask that fit no theme, with a proposed vocabulary addition
- anything intentionally dropped, and why

## Activity trail

`--from-proposal` appends to that proposal's `working/activity.md` and `working/ai-runs.jsonl` per
the workspace contract. `--from-notes` with no `proposal_slug` has no proposal-level trail; note the
run in the register itself through each record's `source_ref`, which is the audit path that matters.

## After capture

Nothing in this skill notifies anyone. The register is inert until someone builds the brief:

```bash
python scripts/build-demand-signal-brief.py
```

The brief crosses each theme's demand against what `my-company/evidence-ledger.json` can
substantiate and leads with the five themes where that gap is widest. Two capture habits feed it
directly, and both are worth the extra seconds:

- **`bid_impact` drives the ranking.** Each hedged bid adds materially to a theme's exposure, and it
  is the field engineering reacts to. A theme with real demand and an empty `bid_impact` column reads
  as academic.
- **`evidence_id` closes the loop.** When an ask is answered by something already in the ledger,
  cite it. That is what separates "BD did not know we can do this" from "we genuinely cannot" — and
  the brief routes those two to different owners.

Distribute the generated `.docx`, never the `.md` — Drive does not take markdown, and the brief's
gap queue is the write-back surface the CTO shop fills in.
