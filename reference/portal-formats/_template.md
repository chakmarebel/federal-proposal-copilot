# [Portal Name] Portal Format Reference
**Source:** [URL or document name, e.g., "Portal instructions page, viewed YYYY-MM-DD after registration"]
**Portal platform:** [e.g., custom agency portal, Valid Evaluation, Challenge.gov, Salesforce-based, proprietary]
**Applies to:** [which opportunities / challenge types on this portal]
**Last verified against live portal:** YYYY-MM-DD by [who]

---

## Portal Metadata (required fields at submission)

| Field | Type | Limit / Enum | Notes |
|---|---|---|---|
| Proposal Title | text | ≤N chars | |
| TRL Level | select | 1–9 | |
| System Type | select | {Hardware, Software, Both} | |
| [Other metadata field] | [text/select/enum] | [limit] | |

---

## Sections and Limits

**CRITICAL:** Confirm whether the limit is *characters* (including or excluding spaces) or *words*. Test against the portal with filler text if unclear — client-side counters sometimes disagree with server-side enforcement.

| Section ID | Portal Label | Char/Word Limit | Instructions Summary |
|---|---|---|---|
| [e.g., SF-1] | [e.g., Technical Solution] | [e.g., 1,500 chars inc. spaces] | [1–2 sentence summary of what goes here] |
| ... | ... | ... | ... |

### Per-section detailed guidance

#### [Section ID]: [Label] ([limit])
[What the portal instructions say this section must cover. Include any "must address ALL of" lists and any keywords the evaluator is looking for.]

#### [Section ID]: [Label] ([limit])
...

---

## Images and Attachments

- Images per section: [N, or "not allowed"]
- Image format: [.png, .jpg, etc.]
- Max file size: [e.g., 5 MB per image]
- Content rules: [e.g., "diagrams only, no narrative text in images"]
- Additional attachments allowed: [e.g., "1 PDF ≤10 MB" or "none"]
- Optional video: [format, length, size limits, or "not supported"]

---

## Formatting quirks

Things that burned someone the first time:

- Markdown rendering: [supported / not supported / partial — e.g., "renders `**bold**` and line breaks but not tables or lists"]
- Line breaks: [preserved / stripped / one-per-paragraph]
- Unicode / special characters: [em-dash handling, curly quotes, etc.]
- Whitespace collapsing: [single-space enforced / preserved]
- HTML comments / `<!-- evidence: -->` markers: [stripped before submission? visible in portal?]

---

## Agreements and Declarations (required at submission)

Things a human must click or sign:

- [ ] [e.g., Terms & Conditions agreement]
- [ ] [e.g., Company identity confirmation]
- [ ] [e.g., Key personnel availability commitment]

## Optional Opt-Outs (decisions required)

Choices the portal asks that have strategic implications — flag these so a human decides before submission:

- [ ] [e.g., Bidder identity sharing with Allied stakeholders]
- [ ] [e.g., Bidder documentation sharing]

---

## Submission Mechanics

- Save-and-resume: [yes / no]
- Character counters: [client-side live / server-side on submit / none]
- Preview before submit: [yes / no]
- Editable after submit: [yes until deadline / no]
- Confirmation: [email / in-portal receipt / both]

---

## Known pitfalls

- [Pitfall 1 — e.g., "client-side counter includes HTML markup in 'rich text' fields; paste plain text to avoid silent overruns"]
- [Pitfall 2]
- [Pitfall 3]
