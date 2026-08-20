# Preventable Gold-Team Findings — the bind-pass completeness sweep

Most of what a Gold/Red Team catches is **preventable** — the draft produces it not
because the problem is hard but because, in advocate stance, the writer does not
self-police placeholders, evidence, definitions, and named resources. Generalized from
the Gold/Red Team findings of 10 real proposals, ~70% of recorded findings are
"fill-the-field" or "show-your-work" failures the company could have closed at draft
time. The remaining ~30% genuinely need an evaluator's frame (see "What stays for Gold
Team" below).

This reference is a **`bind`-pass sweep**, read by `proposal-writer` (Pass 2 — Bind,
Step 2) and cross-checked by `red-team-review` Gold Team. It is deliberately **not** a
`draft-loose` input: loose composes the argument freely; this sweep runs in `bind`,
where verification and completeness already live, so it never stilts composition. If the
writer closes these in bind, Gold Team finds them already closed and spends its judgment
on the residue that needs it.

> **Why bind, not loose.** `draft-loose` explicitly suspends "writing to pass Gold Team"
> to protect cadence. These items are *completeness and grounding* checks, not style —
> they belong with the other bind-pass verification, applied to real prose after the
> argument exists.

---

## What this sweep adds (vs. what other references already cover)

Several preventable categories are **already enforced elsewhere** — do not re-litigate
them here; this file points at their home and covers only the gap:

| Already covered | Where it lives |
|---|---|
| Unsupported / uncited claims; superlatives; marketing language | `bind` Step 1 (evidence verify + `CLAIM-UNSUPPORTED`); `reference/editorial-voice-guide.md` |
| Theme statement, discriminator proof point, action caption (incl. uncited-figure), ghosting | `reference/proposal-writing-patterns.md` (bind Step 2) |
| Dashes, self-narration, prohibited accreditation/ATO claims | `reference/editorial-voice-guide.md`; `prose-lint` (HIGH, blocks export) |
| `[TBD]`/`[TO BE PROVIDED]`/`[INSERT]` left in the package; acronyms undefined at submit | `red-team-review` White Glove (pre-submit QA) |

**The net-new sweep — five checks to run in `bind`, before the package reaches Gold
Team.** These are categories the current flow catches only *late* (Gold/Red/White-Glove)
or not explicitly, and that are cheap to close in bind:

### 1. A scored or required field is never left a placeholder — escalate it, don't bury it
The single most common **controlling** finding: a blank or bracketed value on a scored or
required element (ROM/price `$[X–X]M`, NAICS, contract number, point of contact, period
of performance, a required certification). An unscorable required field **caps pWin and
can read as non-responsive**, regardless of how strong the rest is.

- In bind, if a required datum is missing, **surface it to the user as a blocker** (a
  `[NEEDS: …]` carried from loose becomes a flagged blocker, not a silent `[TBD]`).
- Do not launder the gap into confident prose, and do not leave a bracketed blank in the
  body. White Glove catching `[TBD]` at submit is too late — by then the score is set.
- This is stricter than a generic placeholder scan: it is *scored/required* fields that
  cap the score. Distinguish "missing nice-to-have" (note it) from "missing required"
  (block it).

### 2. Name key personnel with a one-line credential — never ship a role-only "team"
A generic "our experienced team" where the solicitation expects named key personnel is a
high-impact, frequently "#1 priority" Gold-Team fix: delivery capability reads as
unverifiable. In bind, for any section the type expects to name personnel (key personnel,
PI/Co-PI, management approach, technical leads), confirm each is named with a one-line
relevant credential. If a name is genuinely not yet assigned, carry it as a `[NEEDS:
named <role>]` blocker — do not paper over it with role-only prose.

### 3. Define each acronym / term of art on first use; one canonical term
An undefined acronym or a concept that is double-labeled (the same thing called two
names across sections) reads as hedging an unfamiliar word and costs clarity points. White
Glove checks this pre-submit; pull it into bind so the draft is clean earlier. On first
use in each major section, define the acronym; pick one canonical term per concept and
use it throughout.

### 4. Name the specific comparator or benchmark — not "state-of-the-art"
"Outperforms state-of-the-art models," "leading approaches," "industry-standard" — a
vague comparator is unscoreable and reads as a claim the writer can't back. In bind,
replace each vague comparator with the **specific** named baseline and the measured
result ("matches GPT-class accuracy on <named test set> at <number>"), or soften to what
the evidence proves. If the specific number isn't held, it is a `CLAIM-UNSUPPORTED` (Step
1), not a "state-of-the-art."

### 5. Preempt the evaluator's obvious unasked question
For each scoring section, name the one reflexive question a GS-14 evaluator will ask and
answer it in the prose: the security/impact level, *who* validates or accredits the work,
*how* it is tested, what the transition path is. Leaving the obvious question for the
reviewer to raise turns a preventable note into a recorded Weakness. (This one straddles
the line — a sharp draft preempts it; Gold Team still verifies the answer landed.)

---

## Applicability by proposal type

The sweep tracks the same `proposal-type.md` dispatch the patterns use. Required-field and
acronym discipline apply everywhere; personnel and comparator checks apply where the type
scores them.

| Type | Scored-field blocker (1) | Name personnel (2) | Define jargon (3) | Specific comparator (4) | Preempt question (5) |
|---|---|---|---|---|---|
| `far-rfp`, `idiq-to`, `ota-proposal`, `cso-full` | Required | Required | Required | Required | Required |
| `cso-brief`, `ota-white-paper`, `white-paper` | Required | Where named | Required | Required | Required |
| `baa`, `sbir-phase1`, `sbir-phase2` | Required | Required (PI/Co-PI) | Required | Required | Required |
| `rfi`, `sources-sought` | Required (eligibility/identity fields) | Not applicable | Required | Recommended | Recommended |
| `rom` | Required (the ROM range itself) | Not applicable | Recommended | Not applicable | Not applicable |

---

## What stays for Gold Team (do not try to prevent these in bind)

The adversarial pass earns its keep on the ~30% that need the evaluator's frame and
external authority — the advocate structurally cannot do these on itself:

- **Compliance / eligibility audit** against the solicitation + company facts (wrong
  NAICS, uncertified vehicle, non-responsiveness) — `compliance-check` + Gold Team.
- **"Reads as a vendor pitch"** in a context that punishes it (RFI, policy paper), and
  **discriminator captured-not-live / roadmap-only** that draws the "show me it live"
  Q&A — these need the reader's stance.
- **The scoring judgment itself** — which blank actually caps pWin, which fix moves a
  factor Good → Outstanding. That is the rating call, and it must *emerge* from the S/W/D
  analysis (`red-team-review` Gold Team), not be asserted at draft.

The payoff: closing the preventable five in bind means the Gold Team and the human
reviewer spend their judgment on this residue, not on chasing placeholders and uncited
claims — the floor is raised so the "Gold Team fixes 90%" shrinks toward the insight-level
findings only an evaluator can surface.
