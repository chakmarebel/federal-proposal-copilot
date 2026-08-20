# BD ↔ CTO Demand Signal Sync

**Purpose.** Give Vincent and the CTO shop a continuous, evidence-backed view of what customers are
actually asking for, and get a binding answer back on what we can claim. One register, two derived
products, one recurring meeting whose agenda is the disagreements.

**Author:** Bill Bal · **Drafted:** 2026-07-31 · **Status:** built 2026-07-31; register seeded with
131 backfilled signals across 11 customers; first brief generated; awaiting the first round of CTO
dispositions

---

## 1. The failure mode this fixes

Today the demand signal exists, but only inside individual pursuits. This workspace holds 12
`working/requirement-matrix.md` files with a populated **Gap/Risk** column, 23
`working/capability-matrix.md` files, and 28 `inputs/06_notes/` directories with meeting and
conference material. Every one of those is a record of a customer telling us what they need. None of
it aggregates. Consequences:

- Engineering hears requirements as anecdotes from whoever was in the room last.
- The same gap gets rediscovered per bid (audio/multimodal, cross-air-gap update path, ATO
  artifacts, utilization telemetry) and re-hedged in prose each time.
- BD guesses at what is safe to claim, and the guess drifts (the FedRAMP and IL-6 IATT corrections
  are both examples of a claim envelope that lived in people's heads).
- Roadmap prioritization has no frequency or dollar weighting from the pipeline.

The fix is not a better meeting. It is a **normalized register** plus a **written disposition** from
the CTO shop that flows back into what BD is allowed to say.

## 2. The register

One append-only file, workspace root: `signals/demand-signals.jsonl`. One record per atomic customer
ask. Solicitations are one feeder among several — conferences, one-on-ones, trials, and debriefs are
first-class, because unclassified verbal asks are usually 6 to 18 months ahead of the RFP.

```json
{
  "signal_id": "SIG-0042",
  "date_observed": "2026-07-21",
  "source_type": "solicitation",
  "source_ref": "proposals/dia-dma-frontier-llm/working/requirement-matrix.md#R3",
  "customer": "DIA",
  "program": "DMA Frontier-Class LLM Integration",
  "requirement": "Support progressive model upgrades and future iterations across the air gap through the period of performance.",
  "capability_theme": "cross-domain-model-update",
  "demand_strength": "mandatory-scored",
  "pursuit_value_usd": 2500000,
  "our_status": "gap",
  "bid_impact": "Bid the path, not the capability. No concrete cross-air-gap upgrade mechanism to cite.",
  "cto_disposition": null,
  "cto_disposition_date": null,
  "cto_owner": null,
  "evidence_id": null
}
```

Field contracts:

| Field | Owner | Values |
|---|---|---|
| `source_type` | BD | `solicitation`, `rfi`, `industry-day`, `conference`, `one-on-one`, `trial`, `demo-feedback`, `debrief`, `partner` |
| `capability_theme` | BD | controlled vocabulary — see §3. This is the join key. |
| `demand_strength` | BD | `mandatory-passfail`, `mandatory-scored`, `desired`, `curiosity` |
| `our_status` | BD | `shipping`, `prototype`, `roadmap`, `gap`, `no-plan` — BD's read at time of observation |
| `bid_impact` | BD | what we had to hedge, caveat, team for, or no-bid because of this |
| `cto_disposition` | CTO shop | `already-exists-ask-me`, `building`, `planned-<quarter>`, `needs-scoping`, `wont-build` |
| `evidence_id` | BD | `EV-###` once the capability is provable in `my-company/evidence-ledger.json` |

`our_status` is deliberately BD's opinion and `cto_disposition` is deliberately engineering's. Where
they differ, that difference is the meeting agenda. Never overwrite one with the other.

`bid_impact` is the field that earns engineering's attention. "Customer wanted X" is a wish;
"we hedged Section 3.2 and lost 4 rubric points on X" is a requirement.

## 3. Controlled capability themes

Without a fixed vocabulary this becomes 400 unique strings and Vincent reads none of it. Seed the
list from what recurs across the current portfolio, and treat it as a versioned file
(`reference/capability-themes.md`). Adding a theme is a deliberate act, not a typo.

Starting set: `air-gap-ddil-deployment` · `model-serving-api-interop` · `multi-model-hosting-byom` ·
`tevv-eval-harness` · `output-verification-attribution` · `agentic-orchestration` ·
`mission-mos-finetuning` · `non-refusal-behavior` · `multimodal-imagery-fmv` · `multimodal-audio` ·
`data-labeling-curation` · `ato-accreditation-artifacts` · `hardware-footprint-compression` ·
`utilization-telemetry-metrics` · `cross-domain-model-update` · `federation-cross-enclave` ·
`retrieval-over-doctrine` · `multilingual-translation` · `token-cost-economics` ·
`training-data-rights`.

Two rules keep the taxonomy honest: a theme must be something the CTO shop could plausibly own as a
work item, and every theme with three or more open signals must appear in the brief whether or not
anyone asked about it.

## 4. Three products, three cadences

**a. Per-pursuit capture (real time, BD-owned, roughly 10 minutes).** A `/capture-demand-signals`
step runs at two points: after `/opportunity-quick-look` or `/proposal-solution-architect` (mining
the requirement and capability matrices, especially the Gap/Risk column), and within 48 hours of any
conference, one-on-one, trial, or debrief. Signals captured a week later lose the verbatim customer
language, which is the part engineering trusts.

**b. Bi-weekly Demand Signal Brief (generated, read-ahead).**

The first version of this brief led with a 23-row theme leaderboard. That was a mistake worth
recording: a leaderboard is an inventory, and nobody prioritizes from an inventory. Counting who
asked for what tells the CTO shop that demand exists, which they already assumed, and leaves them to
do the distillation themselves — which means it does not get done.

The brief now leads with the decision. Sections, in order:

1. **Decisions** — at most five themes, ranked by exposure, each with the verbatim customer ask, who
   asked, what the evidence ledger can substantiate, what the shortfall has already cost in a bid,
   and the one question engineering needs to answer.
2. **Class triage** — open items split by who owns the fix (see below).
3. **Exposure map** — every theme, with the arithmetic visible so the ranking can be checked by eye.
4. **Open gap queue** — the write-back surface, with the empty disposition column.
5. **Disagreements**, 6. **New signals**, 7. **Diff vs. prior brief**, 8. **How to answer**.

**Exposure** is what makes the ranking a priority rather than a tally. It crosses demand against
proof:

```
exposure = customers × (1 + mandatory share) × proof deficit + 2 × (bids already hedged)
proof deficit: 1.0 = the ledger holds nothing · 0.5 = one or two items · 0 = three or more corroborate
```

The proof side comes from crossing each theme against approved items in
`my-company/evidence-ledger.json` by exact tag match. Two details are load-bearing. Matching on
prose keywords was tried and abandoned — generic terms matched 60 of 81 items, every theme read as
fully proven, and the ranking collapsed to zero, hiding exactly the themes we cannot substantiate.
And `strong` requires three or more corroborating items, not one: a single high-strength item is
enough to answer one evaluator's question, not enough to call a theme proven across five customers'
varied asks.

**Class triage** exists because "open gap" conflates three things the CTO shop treats differently:

| Class | Whose problem | What it means |
|---|---|---|
| Hard gap | Engineering | We told the customer no, and the ledger has nothing for the theme. Build, team, or decline deliberately. |
| Unproven claim | Engineering + BD | We said yes and the ledger cannot back it. Confirm it is real, or BD stops claiming it. |
| Possible enablement miss | BD, not engineering | BD recorded a gap in a theme the ledger evidences well. Usually a communication failure. Theme-level inference, so confirm against the specific ask. |

Sending the third class to engineering is the specific way these reviews lose their audience. On the
first brief it was the largest class — 13 items against 6 hard gaps.

Rendered `.md` → `.docx` through the existing `scripts/render-md-to-docx.py` path, dropped in the
Drive Proposal Repository and linked in Slack. Never distribute the `.md`.

The new-signals appendix shows at most three signals per theme and states the count it withheld;
`--full` prints everything. Sections 1 through 4 are always complete, and Sections 1 and 2 are the
two pages that need reading. The first brief runs longer because it carries the entire backfill.

**c. Quarterly capability-demand review (60 minutes, Vincent + BD + product).** Working session, not
a briefing. Three outputs, all written before anyone leaves: a `cto_disposition` on every aged gap;
kills on stale asks nobody will fund; and an updated claim envelope (§5).

## 5. Closing the loop — where the CTO answer lands

This is the half that most BD/engineering syncs skip, and the reason they decay into a status slide.
Every disposition writes to one of two artifacts BD already consumes:

- **`my-company/evidence-ledger.json`** — when a capability becomes real and provable, it enters the
  ledger as a new `EV-###`. `/evidence-check` then lets proposals cite it, and
  `scripts/check-strengths.py` protects it through team edits. A capability that exists but is not in
  the ledger is invisible to the proposal pipeline, which means we do not get credit for it.
- **`my-company/claim-envelope.md`** (new) — three columns per theme: what BD may state as fact
  today, the exact approved "on our roadmap" phrasing, and what is prohibited. This is the
  counterpart to `reference/doctrine/prohibited-claims-doctrine.md`, but keyed to capability rather
  than to diction, and dated. The FedRAMP and IL-6 IATT corrections both belong here as standing
  entries.

A disposition of `wont-build` is a valid and useful answer: it tells BD to team for that theme
instead of hedging, which is a better bid decision made earlier.

## 5b. The weekly artifact is a workbook, not a document

Corrected 2026-07-31 after the first review. Every section of this brief is a table, and a Word
document is the wrong container for one: it cannot be sorted, filtered, or pivoted, and a reader
looking for "the three things I own" has to build that view in their head. `.xlsx` gives them the
view for free.

`scripts/build-demand-signal-workbook.py` writes five sheets: **Decisions** (the five ranked
exposure calls), **Gap Queue** (the write-back surface, one row per open item, disposition dropdown
enforced by data validation), **Exposure Map**, **All Signals** (the pivot-table source — one row per
ask, autofiltered), and **Themes** (the vocabulary, so a reader can check what a theme means).

The important half is `--ingest`: it reads the returned workbook and applies the dispositions to the
register. That removes BD hand-transcription, which §6 correctly identified as the loop's weakest
link and then accepted. Invalid disposition values are reported and never written, and an unchanged
re-ingest is a no-op rather than a fresh date stamp — so the same file can be passed back and forth
weekly without corrupting the answer history.

The prose brief still generates and is the better read for someone new to the register, or for
forwarding a rationale. The workbook is what goes out weekly.

## 6. Where the CTO shop actually writes

The CTO shop will not clone this repo, and designing around the assumption that they will is how the
process dies in week three. Two supported paths, in order of preference:

1. **Disposition column in the brief's `.docx`** (recommended). The brief ships with an empty
   `CTO Disposition` / `Owner` column on the gap queue. Vincent's shop fills it in Drive comments or
   in the doc. BD transcribes back into the register at the quarterly review, or within a week of any
   ad hoc reply. Friction lands on BD, which is correct — BD needs the answer more.
2. **Slack thread per theme.** Works for high-tempo items; loses the audit trail unless someone
   transcribes. Acceptable for `already-exists-ask-me` replies, not for roadmap commitments.

Either way the register stays single-source in this workspace and BD owns transcription. Do not let
dispositions live only in a Slack thread.

## 7. Keep-alive metrics

Report these in the brief itself, four numbers, every time:

- Signals captured per pursuit (target: at least the count of scored evaluation criteria).
- Percentage of `gap` and `no-plan` signals carrying a `cto_disposition`.
- Median age of an undispositioned gap.
- Pursuits this quarter where a gap forced a hedge, a teaming arrangement, or a no-bid.

The fourth number is the one that moves roadmap priority. Track it from day one, including
retroactively — the Mystic Depot Phase II and UxSAI outcomes are already documented and would
populate it.

## 8. What was built

| Artifact | Purpose |
|---|---|
| [`reference/schemas/demand-signal.schema.json`](../reference/schemas/demand-signal.schema.json) | Field contract, following the existing `reference/schemas/` conventions |
| [`reference/capability-themes.md`](../reference/capability-themes.md) | Controlled vocabulary, versioned. v2 added `staff-product-generation`, `wargame-simulation-personas`, `robotic-autonomy-control` during the backfill |
| [`.claude/skills/capture-demand-signals/SKILL.md`](../.claude/skills/capture-demand-signals/SKILL.md) | `--from-proposal <slug>` and `--from-notes <path>` capture, with the confirmation discipline |
| [`scripts/extract-demand-signals.py`](../scripts/extract-demand-signals.py) | Deterministic first pass: parses matrix tables, drops submission mechanics and internal framing, suggests a theme by keyword, infers status from Gap/Risk prose with header-aware polarity. `--selftest` |
| [`scripts/build-demand-signal-brief.py`](../scripts/build-demand-signal-brief.py) | The brief, plus `--validate-only` and `--full`. Auto-renders `.docx`. `--selftest` |
| [`scripts/backfill-demand-signals.py`](../scripts/backfill-demand-signals.py) | One-time replay of pursuit history with the curation table checked in, so the backfill is auditable and reproducible. Reports dead curation rules. `--selftest` |
| [`scripts/demand_signal_core.py`](../scripts/demand_signal_core.py) | Shared theme keywords, ledger evidence tags, class triage, and exposure scoring. One reader of the vocabulary, so a second copy cannot drift |
| [`my-company/claim-envelope.md`](../my-company/claim-envelope.md) | What BD may state as fact, phrase as intent, or never claim, by theme |

**Backfill result (2026-07-31).** 210 candidate rows from 12 requirement matrices → **128 signals**
across **23 themes** and **11 customers**. 73 rows dropped as submission mechanics, contract
structure, or our own pitch framing; 7 excluded with the `spotter` pursuit (its "requirements" are
needs we inferred for an unsolicited paper, and inferred needs in a demand register are circular);
2 dropped as unclassifiable.

What the first brief puts in front of the CTO shop: **six hard gaps** (three robotics asks declined
in one RFI, three wargaming and simulation asks from NATO DIANA and the Navy SOW in a theme with two
ledger items), and **thirteen probable enablement misses** where BD bid a gap in a theme the ledger
evidences well. The second number being larger than the first is itself the finding.

**Two extraction bugs caught during review, both worth remembering.** The Digital Guardian matrix
heads a column "Gap / Risk" and fills it with coverage grades ("Full"), which inverted every row in
that table — five fully-covered requirements read as top-priority gaps while the real gap read as
unknown. Column polarity is now decided from the column's values, not its header alone. Separately,
the curation table's ID helper split on whitespace, so row IDs containing spaces (`EF-1.2 (IMPL)`)
matched nothing and the rules looked applied while the rows sailed through. The backfill now reports
any curation rule that matched no row.

**Known limitation.** 74 of the 128 backfilled signals carry `our_status: unknown`, because the
source matrix's Gap/Risk cell records a risk rather than a coverage judgment and inferring one would
be inventing it. This is deliberate, and the brief labels the count as a backfill artifact rather
than an action item: unknowns contribute to a theme's demand weight without putting unverified rows
in front of engineering. `/capture-demand-signals` forbids `unknown` on new captures — worth
resolving opportunistically when a pursuit is revisited.

## 9. Open questions for Vincent

1. Who in the CTO shop owns dispositions, and is that one person or one per theme area?
2. Is bi-weekly the right brief cadence, or does monthly match the engineering planning rhythm?
3. Does the CTO shop already maintain a roadmap artifact the register should link to rather than
   duplicate?
4. Will `wont-build` be said out loud? The process only works if it can return that answer.
5. `pursuit_value_usd` is null across the backfill, so dollar-weighted ranking is dark until it is
   populated from HubSpot. Worth wiring, or is customer breadth enough?
