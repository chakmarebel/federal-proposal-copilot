---
patterns_id: unsolicited-proposal
display_name: Unsolicited Proposal (FAR Subpart 15.6)
typical_length: 15-30 pages excl. cover, appendices, and cost detail
section_order:
  - title-page
  - letter-of-transmittal
  - basic-information
  - title-and-abstract
  - statement-of-validity
  - problem-and-gap
  - technical-approach
  - operational-use-cases
  - mission-alignment-and-authorities
  - compliance-and-safeguards
  - program-plan
  - cost-and-contract
  - organization-and-past-performance
  - personnel-conflicts-and-contacts
  - next-steps
  - compliance-matrix-appendix
required_sections: [title-page, letter-of-transmittal, basic-information, title-and-abstract, statement-of-validity, problem-and-gap, technical-approach, program-plan, cost-and-contract, organization-and-past-performance, personnel-conflicts-and-contacts, compliance-matrix-appendix]
optional_sections: [operational-use-cases, mission-alignment-and-authorities, compliance-and-safeguards, next-steps]
---

# Unsolicited Proposal Section Patterns (FAR Subpart 15.6)

**This is the shelf template.** Sections marked FIXED are boilerplate that changes only in the
bracketed fields. Sections marked TAILORED are where the BD lead does real work. The intended split
is roughly 60 percent fixed, 40 percent tailored, so a new pursuit starts from a compliant skeleton
rather than from a blank page.

**Order of operations.** Build `statement-of-validity` and `compliance-matrix-appendix` FIRST, before
any narrative. They are the screening gate at FAR 15.606-1, and building them first surfaces the
representations that need reconciling while there is still time to reconcile them.

**Two mandatory pre-draft confirmations.** Neither is a drafting task and both block the draft:

1. **Prior contacts.** Assemble the actual list of agency personnel already contacted on this subject
   matter, with office, telephone, and date, and confirm it against whoever is named anywhere in the
   document. See `personnel-conflicts-and-contacts`.
2. **Commercial availability.** Decide what is being offered that is genuinely not obtainable from a
   catalog, and confirm the split with the business lead. See `cost-and-contract`.

**House style.** Prose lint applies. No section-sign glyph, no em-dashes or double hyphens as sentence
punctuation, no internal process vocabulary. Run `scripts/lint-submission-file.py` on the outgoing
file, not just on the drafts. Its bracket scan is the last defence against a shipped `[Insert name]`.

---

## title-page
**Status:** FIXED
**Purpose:** Tells the coordinator in ten seconds what this is, what authority it arrives under, and
that it carries restricted data.

**Template:**
```
UNSOLICITED PROPOSAL
Submitted under FAR Subpart 15.6 [and <AGENCY DIRECTIVE, e.g. DHS Management Directive 0750.1>]

[Capability Title]
[One-line subtitle naming the mission outcome, not the technology]

Offeror                     | [Your Company], Inc.
Submitted To                | [Agency, component]
Contracting Point of Receipt| [Agency unsolicited proposal coordinator / contracting activity]
Date of Submission          | [DD Month YYYY]
Proposal Validity           | 180 days from date of submission (through [date])
Preferred Contract Type     | [type]
Proposed Base Value         | $[amount]
Proposal Control Number     | ER-[AGENCY]-UP-[YYYY]-[NNN]

USE AND DISCLOSURE OF DATA
[FAR 15.609(a) prescribed legend, verbatim from the current FAR text.
 The sheet range is filled in LAST, after pagination is final.]
```

**Pitfalls:** Do not name an individual program official as a sponsor here. If a program office is the
technical evaluator, name the *office*, not a person, unless that person has agreed in writing and the
contact is disclosed under 15.605(c)(7). This is the most common integrity failure in the format.
Do not fill in the legend's sheet range until the table of contents field has populated and pagination
has stopped moving.

## letter-of-transmittal
**Status:** FIXED skeleton, TAILORED middle
**Purpose:** The only page some readers read. Establishes authority, the offer, and the ask.

**Structure:** Authority and non-responsiveness. Operational premise, three to five sentences. What we
do about it, three to five sentences. What we propose, one sentence with the price and duration.
Routing statement. The CO-binds-the-Government statement. Signature block.

**Template:**
```
SUBJECT: Unsolicited Proposal, [Title] (Control No. [number])

Dear [Reviewing Official or Coordinator]:

[Your Company], Inc. respectfully submits the enclosed unsolicited proposal for [effort in one
clause]. This proposal is submitted under FAR Subpart 15.6 [and <agency directive>]. It is
independently originated and developed by [Your Company], prepared without Government supervision,
endorsement, direction, or involvement, and is not responsive to any published requirement, pending
solicitation, or Broad Agency Announcement.

[TAILORED: the operational premise. Where the mission happens, why the current toolset does not
reach it, in the customer's own vocabulary.]

[TAILORED: what we do about it, concretely. Name the components. Avoid adjectives.]

We propose to prove this in a bounded, measurable [pilot/prototype] [scope] for a [contract type] of
$[amount] over [duration].

[Routing statement: program offices are not the designated receiving point for unsolicited proposals.
This document is submitted formally to [contracting activity] and provided to [program office] as the
cognizant program sponsor for technical evaluation and mission validation.]

Only the cognizant Contracting Officer has authority to bind the Government with respect to this
submission. No response is required, and nothing in this proposal obligates the Government in any way.
```

**Pitfalls:** Do not open with the company. Open with the customer's problem. Do not promise a
capability in the transmittal that the technical section then qualifies.

## basic-information
**Status:** FIXED
**Purpose:** Satisfies FAR 15.605(a)(1) through (a)(6) in one screenable table.

**Template:** A two-column table, one row per citation, with the citation number in the row label so
the coordinator can tick them off. Rows: offeror name and address; type of organization and NAICS;
technical POC with telephone and email; business and contracts POC with telephone and email;
proprietary data identification; other recipients of this proposal; date of submission; signature
reference.

**Standing content to reuse:** [Your Company], Inc., <City, State>. For-profit corporation,
small business concern. CAGE <CAGE>, UEI <UEI>. **Confirm NAICS against the live SAM
registration each time**; the company record carries <primary NAICS>.

**Pitfalls:** The other-recipients row is answered plainly or not at all. A qualifier such as "in this
form and tailored to this requirement" signals that a related submission exists and invites the
question the row is meant to close. Check `my-company/past-proposals/` for adjacent unsolicited
submissions before answering.

## title-and-abstract
**Status:** TAILORED
**Purpose:** FAR 15.605(b)(1). The abstract is the only paragraph guaranteed to be read by everyone
in the routing chain.

**Structure:** What we propose to deploy, to whom, in what conditions. What it comprises, naming the
layers. The measured outcomes. The human-decision boundary. Under 250 words.

**Pitfalls:** Do not put the strongest argument in the body and a generic summary here. Whatever the
customer's most acute current pain is, it belongs in the abstract.

## statement-of-validity
**Status:** FIXED structure, TAILORED criterion 1
**Purpose:** FAR 15.603(c). This is the screening gate. Build it first.

**Template:** A two-column table, six rows, one per criterion, each separately affirmed.

| Criterion | Affirmation |
|---|---|
| (1) Innovative and unique | [TAILORED. The one row that carries real argument. State the specific combination that is not obtainable elsewhere. Claim what the capability does, not what the customer lacks.] |
| (2) Independently originated and developed | [FIXED. Conceived, funded, and developed with internal research and development and private investment. No Government funding contributed to origination. Verify against any CRADA that touches the same technology.] |
| (3) Prepared without Government supervision | [FIXED. No agency official supervised, endorsed, directed, reviewed, or participated in preparation. No Government-furnished information, procurement-sensitive material, or source selection information was used. **Must be consistent with the 15.605(c)(7) contacts disclosure and with every name on the title page.**] |
| (4) Sufficient detail for evaluation | [FIXED. Point to the sections carrying technical approach, schedule, deliverables, metrics, personnel, and cost.] |
| (5) Not an advance proposal for a known requirement | [TAILORED. Name the sources searched and the date. **Retain the search record in the proposal folder.**] |
| (6) Does not address a previously published requirement | [FIXED. Not responsive to any solicitation, RFI, BAA, SBIR topic, or other Government-initiated announcement, published or pending.] |

**Add a commercial-availability note below the table** whenever the agency supplement bars
commercially available items. Distinguish the commercially available baseline from the
Government-specific configuration being proposed, and state where the baseline is separately
identified in the cost section.

**Pitfalls:** Criterion 1 is where a negative claim about the customer's portfolio usually appears.
Do not make one. Criterion 5 is an assertion we may be asked to support, so the search record is part
of the deliverable even though it does not ship.

## problem-and-gap
**Status:** TAILORED
**Purpose:** Establish that the gap is structural rather than incidental, in the customer's language.

**Structure:** The operating environment, with the customer's own force structure and numbers. The
recurring forms the gap takes, three to five, each named and one paragraph. The binding constraint,
which is the single sentence the rest of the proposal answers. What the Government has today, named
system by named system, acknowledging what those systems do well.

**Pattern to apply:** Acknowledge the incumbent capability by name and credit it honestly, then draw
the boundary. Crediting the existing investment is what makes the boundary credible.

**Pitfalls:** Do not assert an absence in the customer's portfolio. Describe the design property of
the systems they have, which they can verify, and let the conclusion follow. Do not use the customer's
internal political pressures as a selling point. Describe the workload, not the politics.

## technical-approach
**Status:** TAILORED, with FIXED architecture boilerplate
**Purpose:** FAR 15.605(b)(2), objectives, method of approach, extent of effort, anticipated results.

**Structure:** Architecture overview as a layer table, component and function per layer. Deployment
tiers if the hardware profile varies. Core capabilities, one paragraph each, each stating what the
capability produces rather than what technology it uses. **Integration posture**, which is a required
subsection for this type: state explicitly what we will and will not connect to, and frame the
decision as accreditation risk reduction.

**Pitfalls:** Every capability listed here becomes a fixed-price deliverable. Before committing, check
`my-company/claim-envelope.md` for the theme, and check whether the claim is provable, bidable as
intent, or prohibited. A capability whose feasibility is genuinely uncertain belongs in the program
plan as a gated research objective with a Government decision point, not in this list as a promise.

## operational-use-cases
**Status:** TAILORED, optional
**Purpose:** Convert the architecture into mission threads the evaluator recognizes.

**Structure:** Per use case, three headed blocks. Operational context, in the customer's vocabulary
with their statutory hooks. The intervention, four to six specific named workflows. Observable
outcome, naming the measurement.

**Pitfalls:** Keep the outcome measures separated into what we control and what we merely observe.
Only the first can appear in a fixed-price commitment. See `program-plan`.

## mission-alignment-and-authorities
**Status:** TAILORED, optional but recommended for regulated customers
**Purpose:** Show that the capability supports existing authority rather than requiring new authority.

**Structure:** Departmental and component priorities, cited to enacted documents. A statutory and
regulatory authority table, citation and relevance. Potential funding lines, offered as an aid with an
explicit disclaimer that availability and applicability are the Government's determination.

**Pitfalls:** Verify every citation is enacted and correctly numbered. A wrong public law number in an
authorities table costs more credibility than the table earns.

## compliance-and-safeguards
**Status:** FIXED skeleton, TAILORED policy rows
**Purpose:** Answer the oversight question before it is asked.

**Structure:** A governing policy table, requirement and our position, covering the customer's AI
governance directive, privacy analysis, security policy, and records management. Then **design
constraints we commit to**, as bounded negative commitments: what the system will not do.

**Standing content:** the local-audit-log posture, the human-adoption gate, and the no-vendor-telemetry
commitment are reusable across customers. **Add the accreditation evidence here**: an active IL-5 ATO
with the U.S. Space Force, and authorization to test at IL-6 under an active IATT, both with ledger
cites and both phrased exactly as `my-company/claim-envelope.md` specifies. Never claim FedRAMP,
SOC 2, or ISO 27001, and never attribute the IL-6 IATT to a named program or unit.

**Pitfalls:** Bounded negative commitments are the most persuasive content in the whole document and
cost nothing when they are true. They are expensive when they are not, so check each against the
product before committing.

## program-plan
**Status:** TAILORED
**Purpose:** FAR 15.605(b)(2) extent of effort and (b)(4) Government support needed.

**Structure:** Why a pilot or prototype rather than an enterprise deployment, three reasons stated in
terms of the Government's interest. Cohorts or scope, as a table. Phased schedule, as a table. Metrics,
as **two separate tables**: contract performance measures, which are things the offeror controls, and
mission outcome indicators, which the pilot observes and reports. Support requested from the
Government, as an enumerated list.

**Mandatory schedule content for this type.** Name every Government-controlled gate: authorization to
operate, agency software approval and technical review board, privacy analysis, facility access,
personnel security processing. State who controls each. Price the accreditation period as a standalone
milestone and make later phases options that do not start until it closes. A schedule that assumes
Government review speed puts that risk on us at fixed price.

**Pitfalls:** Check the support-requested list for anything that is actually the critical path. If a
requested item gates everything else, propose a first pass we produce ourselves for Government
validation instead of waiting to receive it.

## cost-and-contract
**Status:** TAILORED
**Purpose:** FAR 15.605(c)(1) through (c)(4).

**Structure:** Contract structure table: preferred type, base period, option periods, validity,
payment structure. Cost element table: element, scope, amount, with a stated basis for each. Cost
realism note.

**The commercial-availability split, which is the load-bearing decision.** Scope the unsolicited
proposal to the effort that is genuinely not obtainable from a catalog: workflow engineering, domain
adaptation, accreditation support, deployment and training, evaluation. Then add a short subsection
stating that the baseline platform licenses required to execute are separately available to the
Government through NASA SEWP V or through Carahsoft at the Government's election, with an approximate
value, and that [Your Company] takes no position on the instrument. Do not carry a self-labelled
commercially available line item inside the proposed price. It is honest and it is the sentence a
Contracting Officer uses to decline.

**Pitfalls:** Do not publish scale-up or option-year pricing nobody asked for. It exposes a per-seat
delta and invites a cost-realism question about the base. The scaling model belongs in the final phase
deliverable list.

## organization-and-past-performance
**Status:** FIXED skeleton, LEDGER-SOURCED content
**Purpose:** FAR 15.605(c)(5).

**Structure:** Corporate description. Relevant past performance. Facilities.

**Hard rule for this type.** Past performance in a 15.6 submission is a representation to the
Government. Write it from `my-company/past-performance.md` and `my-company/evidence-ledger.json`, never
from recall. Every named customer, contract, and relationship carries an evidence ID. Never fuse two
separate relationships into a single stronger-sounding sentence, and never describe a demonstration as
a program.

**Standing content:** <business size and socioeconomic status>, <City ST>, founded <year>, <N> full-time
employees, <funding stage, amount, and date>. **State company size explicitly**, then answer the scale
question directly rather than leaving it to the evaluator: the deployment model, and how surge is
covered.

**Pitfalls:** A bracketed promise to attach references later is worse than no mention. Resolve it or
remove it.

## personnel-conflicts-and-contacts
**Status:** FIXED structure, MANDATORY pre-draft confirmation
**Purpose:** FAR 15.605(b)(3), (c)(6), and (c)(7).

**Structure:** Key personnel table with name, role, and relevant background, **including at least one
named alternate**. Organizational conflicts of interest. Security clearances. Environmental impact.
Prior agency contacts.

**The prior contacts subsection is the highest-risk paragraph in the document.** It is a signed
representation. Before drafting it, assemble the actual contact list, then check it against every name
that appears anywhere in the document including the title page and transmittal addressee. If any
person is named as a sponsor, the contact that produced that relationship is disclosable. There is no
version of this where naming a sponsor and asserting no contact are both true.

**Pitfalls:** 15.605(b)(3) names alternates in so many words. A placeholder in the key personnel table
is a compliance failure, not a formatting gap. Where a role will be hired or subcontracted on award,
say so plainly with the qualification profile and the hiring mechanism, which is a legitimate answer.

## next-steps
**Status:** FIXED
**Purpose:** Give the coordinator a sequence that respects the 15.604(b) authority boundary.

**Template:** A five-row table. Formal receipt and 15.606-1 initial review by the contracting activity.
No-cost technical demonstration for evaluators at a Government facility. Comprehensive evaluation
against 15.606-2 factors. Scope confirmation with the program office. Acquisition determination by the
Contracting Officer, including whether a FAR 6.302 justification is supportable or a competitive action
is required.

**Pitfalls:** Naming the competitive alternative ourselves reads as confidence and acquisition
literacy. Omitting it reads as though we have not thought about it.

## compliance-matrix-appendix
**Status:** FIXED
**Purpose:** Make the 15.606-1 initial review mechanical.

**Template:** Three-column table, FAR citation, required content, location in this proposal. Cover
15.603(c), all of 15.605(a), (b), and (c), 15.609(a) and (b), and any agency supplement citation.
The citation set is enumerated by the `statement-of-validity`, `basic-information`, `cost-and-contract`,
and `personnel-conflicts-and-contacts` patterns above; `proposal-manager` seeds the matrix from them
and `compliance-check` verifies it before export. Worked example:
`reviews/2026-08-20-hsi-unsolicited-compliance-matrix.md`.

**Pitfalls:** Build it first, verify it last. Verify the 15.609 sheet ranges against the exported file,
because pagination is not stable until the table of contents field populates.
