# Proposal Agent Redesign — Closing the 70%→95% Prose Gap

**Date:** 2026-05-16
**Author:** Claude (design session)
**Question on the table:** The pre-writing controls work. The prose doesn't. What architectural change closes the gap between a validated draft and a *compelling* one?
**Scope:** Read-only. This is a design document — no code, skills, or proposals were modified.

---

## Executive summary

The pipeline produces robotic prose for one structural reason: **by the time prose is generated, every decision that makes prose feel alive has already been made and frozen in a structured artifact.** The writer doesn't compose — it fills connective tissue between pre-validated atoms. That is the textbook recipe for stilted writing, and the evidence in the workspace shows it cleanly.

The fix is not another skill or another rubric pass. It is to **change the order of operations**: let the agent write a confident, in-voice draft *first*, from a one-page narrative spine, and run the validation machinery *after* as an audit-and-patch step rather than as a cage the writer builds inside. The agent demonstrably can write at 90%+ — three artifacts in the repo prove it. It just never gets the chance, because the current architecture spends the writer's whole budget on slot-filling.

- **Diagnosed pattern:** validation-first / structure-first generation, compounded by a missing narrative spine and a "write-to-the-rubric" instruction.
- **Track A (ship now):** insert a narrative-spine stage; split the writer into draft-loose + bind passes; add a real voice anchor.
- **Track B (Q3):** a narrative-first drafting tool — spine → voice draft → evidence bind → audit → patch — built first for white papers.
- **The one move for this week:** the narrative spine stage. Every piece of evidence points at the missing spine as the 70→95 gap.

---

# Part 1 — The current pipeline, characterized honestly

## 1.1 The lifecycle

The workspace runs a 20-step lifecycle (CLAUDE.md "Standard Workflow"). Collapsing the read-only and capture-triage steps, the spine of it is:

```
new-proposal
  → proposal-manager        plan + compliance matrix seed
  → customer-intel          customer profile
  → competitor-assessment   competitor chart
  → capture-scorecard       go/no-go
  → capture-intent          strategic intent layer
  → proposal-solution-architect   requirement/capability matrices, architecture
  → past-performance        PP narratives
  → pricing-analyst         pricing artifact
  → proposal-storyboard     section-by-section writing plan
  → technical-review (approach)   feasibility gate
  → proposal-graphics       graphics brief
  → proposal-writer         >>> THE ONLY PROSE-GENERATION STEP <<<
  → proposal-editor         editorial pass
  → compliance-check        coverage diff
  → evidence-check          citation audit
  → technical-review (drafts)     claim-truthfulness audit
  → red-team-review         red / gold / white-glove
  → export-proposal         .docx/.xlsx/.pptx
```

## 1.2 Stage-by-stage — what each stage does, what it prevents, what it costs

| Stage | What it does | Failure mode it exists to prevent | Cost to voice / naturalness |
|---|---|---|---|
| **proposal-manager** | Extracts requirements, eval factors, win themes, bid/no-bid → `proposal-plan.md` + `.json` + seeds `compliance-matrix.md` | Missing a "shall," misreading eval weighting, bidding a loser | Win themes are reduced to a 3-column table (`Theme \| Eval Factor \| Proof Point`). The *reason* a theme is compelling is never written down — only the theme, the factor, and a proof token. |
| **solution-architect** | Builds `requirement-matrix.md`, `capability-matrix.md`, `solution-strategy.md`, `architecture-concept.md` | Designing narrative before solution; inventing capabilities | Output is explicitly "tables over long narrative." The architecture exists as a fielded concept, never as an argument. |
| **capture-intent** | Strategic layer: why we bid, customer beliefs, posture, prohibited claims, ghosting → `capture-intent.md` | Strategically confused proposals, generic capability dumps | This is the closest thing to a "spine" the pipeline has — but its own Final Rule says *"It should not read like proposal prose. It should read like internal capture leadership alignment."* It is deliberately **not** narrative. |
| **storyboard** | Per-section plan: evaluator question, required answer, claims allowed, claims prohibited, proof points, do-not-say, target length, tone → `storyboard.md` | Rambling, over-marketing, wrong depth | Decomposes the proposal into a **table of fields per section** before any sentence exists. Pre-commits the answer, the claims, the length, and the tone of every section. |
| **proposal-writer** | Drafts `drafts/<section>.md` from the storyboard + matrices | Unsupported claims, missed requirements, untraceable evidence | **This is where the damage concentrates — see §1.4.** |
| **proposal-editor** | "Editorial pass — not a rewrite from scratch." Light polish / structural / compression / technical-preservation modes → `drafts/edited/` | AI smell, marketing language, redundancy | `conflicts_with: proposal-writer` — explicitly forbidden from re-deriving claims or proof points. It can tighten and reorder; it cannot re-conceive. |
| **compliance-check** | Diffs requirements vs. draft coverage; recomputes matrix | A "shall" with no home → disqualification | Pure audit. Touches no prose. |
| **evidence-check** | Audits `<!-- evidence: -->` markers vs. the ledger | Unsupported claims surviving to submission | Pure audit. |
| **technical-review** | Feasibility (approach) + claim-truthfulness (drafts) | Magical integrations, ATO hand-waving | Pure audit. |
| **red-team-review** | Red (narrative quality), Gold (rubric mock-eval), White Glove (QA) | Losing on score | Gold scores the four "winning patterns." The writer is told upstream to *write to pass Gold* — see §1.5. |
| **export-proposal** | md → Office formats | Format non-compliance | No prose effect (the formatting bugs are covered by the separate 2026-05-15 diagnosis). |

## 1.3 Where prose is generated vs. transformed

This is the single most important fact about the architecture:

> **Prose is generated in exactly one place — `proposal-writer`. Every stage before it produces structured artifacts (matrices, tables, plans, field-lists). Every stage after it audits or lightly transforms.**

There is no stage that *composes*. There is no rough-draft stage. The writer's first token is expected to be production-grade, and it is expected to be production-grade while simultaneously satisfying the compliance matrix, the storyboard's per-section field list, the four winning patterns, the eight-element Section Standard, the editorial voice guide, the evidence-citation protocol, and the proposal-conventions file. (`proposal-writer/SKILL.md` lists seven mandatory inputs and four conditional ones before the word "draft" appears.)

## 1.4 How control flows between stages — the translation problem

The writer's mandatory inputs (`proposal-writer/SKILL.md` §Inputs) are: `proposal-type.md`, `compliance-matrix.md`, `proposal-plan.md`, `solution-strategy.md`, `architecture-concept.md`, the section-pattern file, and the editorial voice guide. Conditionally it reads `requirement-matrix.md`, `capability-matrix.md`, `storyboard.md`, `capture-intent.md`.

Note what is **not** on that list: the solicitation itself. The customer's own documents. The customer's own words. By the time the writer runs, it has never read the thing it is responding to — only digested matrices *about* it. The customer's problem reaches the writer as a row in a requirement matrix and a proof-point token in a win-theme table.

This is the **lost-in-translation** flow. Bill's own mental model is "take the capability matrix, derive win themes, develop a story of *why this is compelling against the customer's actual problem*." The pipeline does the first two steps and writes them to disk as tables. The third step — the story, the *why* — is never written down anywhere. The storyboard comes closest, but the storyboard is a *table of fields per section* (`Evaluator Question`, `Required Answer`, `Claims Allowed`...), not a flowing argument. A spine is a cross-section through the whole document; the storyboard is a stack of per-section cells. Nobody ever writes the sentence "this proposal argues X, and here is why that beats the alternative."

## 1.5 The writer's actual job, precisely stated

By the time `proposal-writer` starts a section, the following are already decided and frozen upstream:

- **The answer** — `storyboard.md` → "Required Answer" and "Primary Takeaway"
- **The claims** — "Claims Allowed" and "Claims Prohibited or Must Be Qualified"
- **The proof** — "Proof Points / Evidence"
- **The structure** — the eight-element "Section Standard" (`proposal-writer/SKILL.md` §Section Standard): theme statement → point → how it works → discriminator proof → tie to requirement → credibility → evaluator takeaway → graphic refs, *in that order*
- **The length** — "Target Length"
- **The tone** — "Control Tone" ("concise and executive-readable," etc.)
- **The opening sentence's job** — a theme statement, mandated, with a litmus test it must pass

With all of that frozen, the writer's actual remaining task is: *generate grammatical connective tissue that threads the pre-decided atoms together in the pre-decided order.* That is slot-filling. Slot-filling cannot produce rhythm, because rhythm is a property of how a writer *moves between ideas* — and the moves are all pre-specified.

The SKILL even instructs: *"Write for completeness and clarity. Do not optimize for brevity or tone polish; that is handled by `/proposal-editor`."* The writer is told, in writing, not to care about how it sounds.

And then `proposal-editor` is told it is *"not a rewrite from scratch"* and `conflicts_with: proposal-writer`. So the one stage allowed to care about voice is forbidden from re-conceiving anything. It is asked to humanize prose that was generated with humanization explicitly deferred. That is doing surgery where a transplant was needed.

One more loop worth naming. `proposal-writer/SKILL.md`: *"Write to pass Gold Team the first time."* `proposal-writing-patterns.md`: *"If the writer produces these patterns ... Gold Team finds them present and scores higher."* The writer is told what rubric will score it and told to optimize for the rubric's pattern-detector. Meanwhile `proposal-editor`'s anti-pattern list includes *"every section opening with the same formula"* and *"repetitive theme statements."* The pipeline **mandates** the formula (every scoring section opens with a theme statement) and then asks the editor to remove the monotony the mandate created.

---

# Part 2 — Feeling the problem: the evidence

I read three generated white papers and the human-review record behind one of them. The workspace happens to contain a near-perfect natural experiment: the same company, the same product, the same voice target, at three different levels of pipeline processing.

## 2.1 Exhibit A — pipeline cold output (`socpac/drafts/full-white-paper.md`)

This is an early SOCPAC pipeline draft. It is the symptom in its purest form.

> "EdgeRunner AI provides a distributed tactical layer enabling secure, on-device execution of open-weight models in DDIL environments while capturing structured, mission-relevant data for GCC-level and enterprise refinement."

That sentence is four nouns deep before it does anything. It reuses the same "distributed tactical layer enabling..." frame three more times in the section. The Representative Capabilities table contains a row literally labeled **"Scalable"** — a word banned by name in *both* `style-guide.md` and `editorial-voice-guide.md`. There is a concatenation typo, **"improvedbetter data management."** The closing line of the exec summary — *"It's a mature, deployable capability that integrates with current enterprise and GCC ecosystems, delivering immediate measurable workflow and mission execution improvements"* — is a press release.

Mark the failure modes the prompt asked me to look for:
- **Robotic / press-release-y:** the exec summary, throughout.
- **Repeating the requirement back:** §2 restates the three challenges, then §3 restates them again as solutions, then §4 restates the lifecycle a third time. Section 3 and Section 4 substantially overlap.
- **No spine:** ask "what is this paper *arguing*?" and there is no answer. It is a tour of capabilities. It describes EdgeRunner; it does not make a case.

The damning detail: the rules to prevent every one of these failures already exist in the reference files. "Scalable" is on the banned list. "No redundancy across sections" is a writing rule. The pipeline produced a draft that violates its own rulebook — because **rules applied as a checklist to slot-filled content don't survive contact with slot-filling.**

## 2.2 Exhibit B — pipeline + four revision passes (`socpac/drafts/white-paper-v4-revised.md`)

Same paper, four revisions later. Markedly better. It now has problem-first framing:

> "Enterprise and GCC AI capabilities assume reliable connectivity. Across contested and distributed operational environments ... that assumption fails."

That is a real sentence with a real edge. But residue remains. §5.1: *"...multi-model agentic workflows through standardized interfaces for seamless interaction with existing software"* — "seamless" is banned. §5 still substantially re-states §4. It took four human-driven revision cycles to get from 70% to roughly 80%, and it plateaus there. Revision is grinding the symptom down, not removing the cause.

## 2.3 Exhibit C — light pipeline + heavy human editing (`vulcan-jatf/drafts/whitepaper.md`)

This is the recent one. It is roughly 90%+. It opens:

> "The proliferation of low-cost autonomous systems has shifted the limiting factor in tactical UxS employment from platform availability to operator cognitive bandwidth."

It has a spine, stated in one line and held for nine sections: *"disconnected adaptive autonomy infrastructure for tactical UxS operations — not another AI platform."* It is confident where it has earned it ("EVELYN is TRL 8 and ready for immediate integration") and honestly hedged where it has not ("the specific reduction ratio will be characterized during Vulcan integration testing"). It teaches without padding.

Now the critical fact. From `vulcan-jatf/working/activity.md`, this proposal **never ran the full pipeline.** It ran `new-proposal`, then `manual-review-adjudication` and `manual-review-incorporation` — and `proposal-editor` only in `executive-compression` mode. There is no `proposal-manager`, no `storyboard`, no `proposal-writer` entry. What it had instead: **62 accepted in-person human review edits.**

## 2.4 The natural experiment

| Exhibit | Processing | Quality |
|---|---|---|
| A — `full-white-paper.md` | Full pipeline, cold | ~70% |
| B — `white-paper-v4-revised.md` | Full pipeline + 4 revision passes | ~80% |
| C — `vulcan-jatf/whitepaper.md` | Light pipeline + 62 human line edits | ~90%+ |

**The more pipeline, the worse the prose. The more human narrative editing, the better.** That is the empirical heart of this document.

## 2.5 What the human actually did — `vulcan-jatf/reviews/manual-review-adjudication.md`

This file adjudicates ~75 in-person review comments. It is, in effect, a labeled dataset of *what the pipeline produced vs. what a human knew it needed.* The recurring themes:

- **W18 — the spine came from the human.** The repositioning to *"disconnected adaptive autonomy infrastructure ... rather than 'AI autonomy platform'"* is review comment W18. The single most important sentence in Exhibit C — the one that makes it cohere — was supplied by the human reviewer. The pipeline produced a draft with no spine; the human installed one.
- **W1/W2/G1 — the human supplied the "Why Now."** The pipeline draft's exec summary was flagged "missing urgency, measurable outcomes, transition framing." The reviewer's own sentence was adopted "near-verbatim as the new first line."
- **G8 (and W8, B4, B10, P4, P13) — feature-language, not benefit-language, in every document.** The recurring fix: *"OpenAI-compatible API" → "allows rapid integration of existing AI-enabled applications without custom protocol development."* The `proposal-writing-patterns.md` reference contains an entire Features-Advantages-Benefits hierarchy telling the writer to do exactly this. The pipeline output still stopped at Feature, six documents deep.
- **G11/W17 — "the single most valuable theme": add measurable success criteria.** The pipeline draft read as a "capable concept," not the "experimentation program" the JATF Build-Measure-Learn evaluation posture wanted. The pipeline never grasped the customer's actual evaluation frame.

Every one of these is a *narrative / strategic* miss, not a fact miss. The facts were right. The compliance was tracked. What was missing was the argument — and a human had to hand-install it.

## 2.6 Proof the agent can write — `socpac/drafts/section-3-4-rewrite.md`

This is a focused rewrite of three sections. It is dramatically better than the surrounding `full-white-paper.md`:

> "AI systems fielded without feedback mechanisms become static. Their performance degrades as mission conditions evolve, and lessons learned at the edge never reach the teams refining models at the GCC or enterprise level."

Declarative. Confident. A point of view. It is headed by a one-line narrative instruction: *"Section 3 is a concise 'what is it' introduction; Sections 4.1–4.3 carry all the operational detail ... No content appears in both."* Given a spine and one bounded job, the agent writes at 90%. The capability is there. The architecture starves it.

## 2.7 Bill's voice

The cleanest sample of Bill unfiltered is `socpac/inputs/06_notes/socpac-context-notes.md`: terse, factual, concrete — *"Bill committed to delivering SF, PSYOP, and CA LoRA adapters within 90 days of PaceSetter award. Conditions: SME vetting pool within 30 days; unclassified doctrine only (FM 3-05, FM 3-53, FM 3-57)."* Specific identifiers, no adjectives, every clause load-bearing. That is exactly the `style-guide.md` voice ("clinical, not clever ... let facts do the talking"). Exhibit C, after 62 of his edits, hits it. Exhibit A misses it by a mile — not because the style guide is wrong, but because a style guide is a filter and the pipeline gives it slot-filled prose to filter. You cannot filter rhythm into existence.

---

# Part 3 — Diagnosis: the architectural pattern

Of the candidate patterns, **four fit the evidence and reinforce each other.** One is the root; three are accelerants. Two candidates I dismiss.

## 3.1 ROOT — Validation-first / structure-first generation

**The pattern:** facts are gathered, structured, and frozen into artifacts *before prose exists.* When the writer starts, every slot is filled (§1.5). The writer's job collapses to connective tissue.

**Why it produces stilted prose, mechanically:** natural writing invents its rhythm by *deciding how to move between ideas* — what to lead with, what to subordinate, where to compress, where to dwell, where to surprise. The storyboard pre-decides all of those moves: order (the 8-element Section Standard), emphasis ("Primary Takeaway"), length ("Target Length"), depth ("Control Depth"). The only freedom left is word choice inside a fixed lattice. Prose written under those constraints reads exactly like Exhibit A reads — because that is what it is.

**Evidence:** the quality gradient inverts with pipeline depth (§2.4). Exhibit C skipped storyboard + writer and scored highest. The section-3-4-rewrite, given a *prose* instruction instead of a field table, scored 90%. The pipeline draft violates its own banned-words list — the signature of generation that is busy satisfying a lattice and has no spare attention for the rulebook.

This is the root because the other three accelerants all *operate through* it.

## 3.2 ACCELERANT — The missing narrative spine ("lost in translation")

The writer never sees the solicitation, only matrices about it (§1.4). The *reason a win theme is compelling* is never written anywhere — it is compressed to a `Theme | Factor | Proof` row before any prose exists. Bill's step 3 — "the story of why this beats the alternative" — has no artifact, no stage, no owner.

The storyboard is not that artifact. A spine runs *lengthwise* through the whole document ("here is the argument, start to finish"); the storyboard is a *crosswise* stack of per-section field tables. You cannot reconstruct a melody from a spreadsheet of which notes go in which bar.

**Evidence:** W18. The spine of the one good paper was hand-installed by a human reviewer as comment #18. The pipeline had no slot for it because the pipeline has no spine stage.

## 3.3 ACCELERANT — Rubric-as-prompt (teaching to the test)

The writer is told the rubric in advance and told to optimize for it: *"Write to pass Gold Team the first time."* Gold scores four named patterns; the patterns reference promises higher scores if the writer emits them. So the writer emits them — every scoring section opens with a mandated theme statement in mandated three-part structure. The result is the formulaic monotony that `proposal-editor`'s own anti-pattern list flags. **The pipeline manufactures the defect the next stage is assigned to remove.**

**Evidence:** Exhibit A's sections open near-identically; `editorial-voice-guide.md` itself warns "Do not open every section with the same formula" — a warning that exists only because the upstream mandate guarantees the violation.

## 3.4 ACCELERANT — Compose-then-edit, in the wrong order, with a disarmed editor

Humanization is explicitly deferred from the writer ("Do not optimize for ... tone polish; that is handled by `/proposal-editor`") to an editor that is explicitly forbidden from re-conceiving ("not a rewrite from scratch"; `conflicts_with: proposal-writer`). Voice is everyone's job at the moment no one is allowed to do it. The editor can tighten a stiff sentence; it cannot install a missing spine or re-conceive a slot-filled section. Surgery where a transplant was needed.

**Evidence:** Exhibit B — four editor-class passes moved 70%→80% and plateaued. Editing recovers the recoverable; it cannot recover what was never composed.

## 3.5 Two patterns I considered and dismiss

- **"Anti-hallucination overreach."** Plausible on its face, but the evidence says no. The audit stack (compliance-check, evidence-check, technical-review, red-team) is *good* — and Exhibit C is both well-validated *and* well-written. The validators don't strip confidence; they run after prose and they work. The problem is the *order and the framing* of generation, not the existence or strength of validation. Keep the validators. (This matters: the prompt explicitly bars "add more validation" — correctly — but the converse, *removing* validation, is also wrong. Validation isn't the disease.)
- **"One-size-fits-all writer."** Real but minor. One `proposal-writer` does serve both a 2-page white paper and a 30-page FAR volume, and the 8-element Section Standard is genuinely wrong for a white paper. But the convention files already partially override this, and fixing it alone would not move the needle — Exhibit A *is* a white paper and still failed. It is a Track A tidy-up, not the diagnosis.

## 3.6 The diagnosis in one paragraph

The agent is asked to *compose* at the exact moment it has the *least* freedom to compose — after every structural, claim-level, length, and tone decision has been frozen into upstream tables, with no narrative spine ever written down, while optimizing for a rubric's pattern-detector, knowing a downstream editor it is told not to need will "fix the voice." It cannot fix the voice, because voice is not a finish; it is a consequence of who got to make the moves. In this pipeline, the writer makes none of them. **70% is the ceiling of excellent slot-filling. 95% requires composition, and the architecture has no stage where composition is allowed to happen.**

---

# Part 4 — The redesign

## Track A — Incremental (shippable in 1–2 weeks)

Six moves. They share one principle: **give composition a place to happen, and stop freezing the moves before it does.**

### A1 — Insert a narrative-spine stage *(highest impact — ship this first)*

**Where:** a new step between `solution-architect`/`capture-intent` and `proposal-storyboard`.

**What:** the agent writes — *in prose, not a table* — a ~1-page document answering: *What is this proposal arguing? Why is that compelling against the customer's actual problem? What is the through-line a reader should still feel in section 8?* One paragraph per major movement, plus a single positioning sentence (the W18 sentence). Output: `working/narrative-spine.md`. **The human signs off on it before anything downstream runs.** This is the W18 moment promoted to a first-class, mandatory step — and it is the cheapest possible place to get Bill's judgment into the loop, because a 1-page prose spine takes him three minutes to read and redirect.

**Then:** `storyboard` decomposes the *approved spine* into sections instead of inventing per-section answers from matrices. `proposal-writer` reads the spine first, as its primary orienting input.

**Risk:** another artifact to maintain. Mitigate by keeping it short, prose-only, and explicitly disposable after drafting — it is a thinking tool, not a deliverable.

### A2 — Split the writer: `draft-loose` then `bind`

**Where:** `proposal-writer` becomes two passes.

**Pass 1 — `draft-loose`:** write the section from the spine + storyboard as a confident argument, in voice. *Suspended* during this pass: compliance-matrix maintenance, the eight-element Section Standard, the four-pattern enforcement, evidence-marker insertion. The instruction is "make the case; sound like a person." Unsupported claims are *allowed* here and simply left for Pass 2.

**Pass 2 — `bind`:** a separate pass over the loose draft that attaches `<!-- evidence: -->` markers, verifies every claim against the architecture and ledger, marks anything unsupported `CLAIM-UNSUPPORTED`, and updates the compliance matrix. This is the *existing* machinery — just run as a second pass over real prose instead of as a cage built during generation.

**Effect:** composition happens in Pass 1 with full freedom; verification happens in Pass 2 without touching rhythm. This is the smallest change that moves slot-filling back to composing.

**Risk:** the loose draft over-claims. That is fine and intended — Pass 2 is mandatory and catches it. The risk to *manage* is anyone shipping a Pass-1 draft; enforce that `bind` always runs.

### A3 — A real voice anchor (few-shot, not a banned-words list)

**Where:** `proposal-writer` inputs.

**What:** create `reference/voice-anchors/` holding 2–3 *excerpts of the target voice* — `vulcan-jatf/whitepaper.md` §1–3, `socpac/section-3-4-rewrite.md`, and one passage Bill wrote himself. Put them in the writer's context as exemplars to imitate. `editorial-voice-guide.md` tells the model what *not* to do; it never shows it what *good* sounds like. Models match cadence far better from examples than from prohibitions.

**Risk:** stale anchors. Mitigate: one small file, refreshed when a proposal wins or Bill praises a draft.

### A4 — Stop mandating uniform section openings

**Where:** `proposal-writer/SKILL.md` §Section Standard and `proposal-writing-patterns.md`.

**What:** make the theme statement a property the *section must contain*, not the sentence it *must open with*. Let openings vary — a scene, a number, the customer's problem, a blunt claim. The litmus test stays; the position rule goes. This directly removes the monotony the editor currently exists to clean up.

**Risk:** an evaluator on a skim misses the theme. Mitigate: keep "theme statement within the first two sentences" for FAR scoring sections; relax fully for white papers.

### A5 — Document-type writing posture, not just section list

**Where:** `proposal-writer` dispatch.

**What:** the writer already dispatches section *lists* by type. Make it also dispatch *cognitive posture*: white-paper mode drops the 8-element Section Standard entirely and writes to the `white-paper.md` convention (compressed, narrative, four-finding exec summary); FAR/OTA mode keeps the scoring template. The convention files already exist — wire posture to them.

**Risk:** low. This is mostly making an existing latent split explicit.

### A6 — Invert the rubric instruction

**Where:** `proposal-writer/SKILL.md`.

**What:** delete "Write to pass Gold Team the first time." Replace with: "Write the most compelling honest argument for this section. Gold Team and compliance-check run afterward as audits; they will return a patch list; you will patch only the gaps." Stop telling the writer the test. Let the rubric catch what's missing instead of shaping every sentence pre-emptively.

**Risk:** a pattern genuinely gets missed and patched late. Acceptable — patching 3 flagged gaps is cheaper than de-formularizing 20 sections, and the audit still runs.

**Track A sequencing:** A1 this week. A2 + A3 next. A4–A6 are small edits that can ride along. A1 alone, even without the others, should move white papers meaningfully — it is the missing-spine fix and the missing-spine fix is the core of the diagnosis.

---

## Track B — Reimagine: a narrative-first drafting tool

### B.1 The direction, and why this one

Of the Track B candidates, the right one is the **narrative-first generation tool** — invert the order so voice draft comes *before* evidence and compliance — scoped initially as a **smaller, focused tool for white papers**, run alongside the existing pipeline rather than replacing it.

Why this and not the others:
- A *multi-voice ensemble* or *voice-aware reviewer* treats voice as a selection/scoring problem. The evidence says voice is an *order* problem — pick the wrong order and no amount of choosing or scoring among bad drafts helps.
- A *two-track parallel drafter* (voice draft ∥ compliance draft, then merge) is elegant but the merge step is where stilted prose would creep back in — merging is slot-filling by another name.
- *Narrative-first, sequential* — spine → voice → bind → audit → patch — is what the evidence actually endorses: it is exactly how Exhibit C succeeded (human spine, loose human-edited prose, then audits), just made into a repeatable tool instead of a heroic manual effort.

Scoping it to white papers first is deliberate. White papers are where voice matters most, where the current pipeline most clearly underperforms (all three exhibits are white papers), and where the blast radius of a new tool is smallest — a white paper has no Section M, no formal compliance matrix, less to break. Prove it there; extend later.

### B.2 The architecture, in plain terms

Think of it as **five stages, and the order is the whole point.**

1. **Spine.** The agent reads the solicitation and the customer material *directly* — not matrices — and drafts a one-page argument in prose: what we're saying, why it beats the alternative, the through-line. **Bill reads it and signs off or redirects.** This is the collaboration moment — the agent and Bill align on the *argument*, which is the part that actually needs his judgment. Three minutes of his time, spent where it matters.

2. **Voice draft.** The agent writes the entire white paper, start to finish, from the approved spine — loose, confident, in character, no compliance scaffolding, no per-section template, no evidence markers. Its only job is to make the case and sound like EdgeRunner. It is allowed to be wrong about facts here.

3. **Bind.** A separate pass walks the voice draft and does the verification: every factual claim checked against the architecture and the evidence ledger; evidence markers attached; anything unsupported flagged `CLAIM-UNSUPPORTED`; numbers checked. Prose is touched *only* to soften a claim that failed verification — never for style.

4. **Audit.** The existing skills run unchanged as gates: `compliance-check` (where applicable), `evidence-check`, `technical-review`, `red-team-review` Gold/White-Glove. They produce a **patch list** — specific, located findings.

5. **Patch.** The agent applies *only* the patch-list fixes. No global rewrite. The spine and the voice survive.

The artifacts that pass between stages: a **prose spine** (stage 1→2), a **voice draft** (2→3), a **bound draft** with evidence markers (3→4), a **patch list** (4→5), a **final draft** (5→export).

### B.3 What gets reused, and what gets dropped

**Reused wholesale:** `proposal-manager` (planning/bid-no-bid still valuable), `solution-architect` (the architecture must still be designed before the spine), `capture-intent` (strategic guidance feeds the spine), the entire audit stack (`compliance-check`, `evidence-check`, `technical-review`, `red-team-review`), the evidence ledger, the convention files, `export-proposal`.

**Dropped or demoted — and these are real losses, stated plainly:**

- **The per-section storyboard field-table is dropped for white papers.** *Loss:* the storyboard's per-section discipline — "Claims Prohibited," "Do Not Say," explicit evaluator-question mapping — is genuinely useful, and it goes away. *Why the trade is worth it:* for a white paper there is no Section M to map to, the prohibited-claims list is better carried by the spine and the bind pass, and the field table is precisely the lattice that produces slot-filling. The discipline is preserved where it earns its keep (see B.4). For white papers, it costs more than it pays.

- **The eight-element Section Standard is dropped for white papers.** *Loss:* a guaranteed, uniform, evaluator-skimmable structure. *Why worth it:* uniform structure is exactly the monotony problem; a white paper is read, not scored on a rubric, and the `white-paper.md` convention already specifies a better structure (four-finding exec summary, self-positioning last).

- **The separate `drafts/edited/` editor stage is folded into bind + patch.** *Loss:* a discrete, inspectable editorial diff. *Why worth it:* a standalone humanize-after-the-fact editor is the compose-then-edit anti-pattern; if the voice draft is composed in voice, there is nothing to humanize, only facts to bind and gaps to patch.

- **"Write to the rubric" is dropped entirely.** *Loss:* none worth keeping. The rubric still runs — as an audit, in stage 4, which is where a rubric belongs.

### B.4 How it differs from the current tool

The current tool: **structure → validate → generate → audit.** Prose is the *last* creative act, performed inside a finished cage.

Track B: **align → generate → verify → audit.** Prose is the *first* creative act; verification and audit come after, on real prose.

For **FAR/OTA/SBIR volumes**, the current pipeline largely stays — compliance-heavy, rubric-scored work genuinely needs the matrix and the per-section discipline, and the blast radius of changing it is high. Track B is not "rip out the pipeline." It is "build the right tool for the document class the pipeline serves worst, and let the two coexist." Over time, if Track A's spine stage proves out inside the existing pipeline, the FAR path converges toward the same order — but that is a later decision, made on evidence.

### B.5 Cost and risk

- **Build cost:** moderate. Three of the five stages already exist (planning, audit, export). The new build is the spine stage, the loose voice-draft mode, and the bind pass — and Track A's A1/A2 are literally prototypes of those. Track A is not throwaway work; it is Track B's first two components, shipped early inside the old tool.
- **Risk — the voice draft drifts from fact.** Mitigated structurally: the bind pass is mandatory and is the existing, trusted verification machinery. The order change does not weaken verification; it just stops verification from running *during* composition.
- **Risk — Bill becomes a bottleneck at the spine sign-off.** This is a feature, not a bug: it is one 1-page review, at the cheapest possible point, replacing 62 line-edits at the most expensive point. If he wants to skip it, the agent proceeds on its own spine — same as today, no worse.
- **Risk — two tools to maintain.** Real. Accept it: one tool cannot be optimal for a 2-page narrative brief and a 30-page rubric-scored volume. The current single tool is optimal for neither.

---

## Recommendation

**Ship Track A now. Commit to Track B as a Q3 project, scoped to white papers.**

Track A is not a holding action — A1 and A2 *are* Track B's spine stage and draft-loose/bind split, shipped early inside the existing tool. Doing Track A first de-risks Track B: if the spine stage measurably lifts white-paper quality inside the old pipeline, Track B is validated before a line of it is built. If it doesn't, the diagnosis is wrong and Q3 should be spent differently.

Do **not** skip straight to Track B. The spine stage is testable in days inside the current tool; building the whole narrative-first tool before confirming the spine hypothesis would be betting the quarter on an untested premise.

**This week:** ship **A1, the narrative-spine stage.** Every strand of evidence — W18, the section-3-4-rewrite, the pipeline-depth quality gradient, Bill's own description of how he writes — converges on the same point: the missing artifact is the spine, and a human currently has to hand-install it. Make it a stage. Make Bill sign off on one page. That is the highest-leverage change available, and it is a few days of work.

### The experiment that would settle the open question

One thing I cannot determine from the artifacts alone: is the 70% ceiling caused by the *frozen structure* (the lattice) or by the *translation loss* (writer never sees the solicitation)? They co-occur in every sample. The test: take SOCPAC, give the writer the **raw solicitation + a one-paragraph human-written spine**, and have it draft loose — no matrices, no storyboard. Then compare to `full-white-paper.md`.

- If loose+spine ≈ 90% → the lattice is the problem; A1+A2 are sufficient and Track B is high-confidence.
- If loose+spine still ≈ 75% → translation loss matters independently; Track B's stage 1 must include direct solicitation reading, not just a spine handoff.

Exhibit C already suggests the answer is the former — but it cost 62 human edits, so it does not cleanly isolate the variable. The experiment above does, and it costs one afternoon.

---

*End of design document.*
