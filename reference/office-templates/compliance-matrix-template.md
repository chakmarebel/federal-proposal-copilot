# Compliance Matrix xlsx Spec

Specification for exporting `working/compliance-matrix.md` to `final/xlsx/compliance-matrix.xlsx`. The xlsx is the form teammates use to share status, filter to their section, and track their open items.

## Workbook structure

### Sheet 1: Matrix

Direct 1:1 export of the 7-column markdown table:

| Req ID | Source | Requirement | Section | Page | Status | Evidence |
|---|---|---|---|---|---|---|

**Formatting:**
- Header row: bold, white text on dark blue (#1F4E79), frozen pane
- Autofilter enabled on all columns
- Column widths: Req ID (12), Source (14), Requirement (60), Section (25), Page (8), Status (14), Evidence (50)
- Word wrap on Requirement and Evidence columns
- Row height: auto

**Conditional formatting on Status column:**
- `Covered` — green fill (#C6EFCE), dark green text (#006100)
- `Drafted` — blue fill (#BDD7EE), dark blue text (#1F4E79)
- `Planned` — yellow fill (#FFEB9C), dark amber text (#9C6500)
- `Partial` — orange fill (#FFC7CE), dark orange text (#9C0006)
- `Exception` — purple fill (#E4DFEC), dark purple text (#5F497A)
- `Gap` — red fill (#FFC7CE), bold dark red text (#9C0006)

### Sheet 2: Summary

A small dashboard showing the counter block. Pull from the counters at the bottom of the matrix markdown.

| Metric | Count | % |
|---|---:|---:|
| Total requirements | [N] | 100% |
| Covered | [N] | [%] |
| Drafted | [N] | [%] |
| Planned | [N] | [%] |
| Partial | [N] | [%] |
| Exception | [N] | [%] |
| Gap | [N] | [%] |

Add a simple bar chart visualizing the distribution. Chart title: "Compliance Coverage by Status."

Below the counter block, add a one-line summary: "Coverage: X% (Covered+Drafted), Open items: Y (Planned+Partial+Gap)."

### Sheet 3: Gaps

Filtered view of rows where `Status` is `Gap`, `Partial`, or `Exception` (but with empty Evidence). This is the open-items list for the team.

Same columns as Sheet 1, but pre-filtered. Add a column header cell: "**OPEN ITEMS — resolve before submission**".

### Sheet 4: By-Section (optional if useful)

Pivot-like view grouping rows by the Section column. Helps team members working on a specific section see only their items.

## File properties

- Author: [Company name from `my-company/company-description.md`]
- Title: "Compliance Matrix — [Proposal Name]"
- Subject: "Compliance traceability for [solicitation number]"
- Keywords: "compliance, matrix, [type_id]"

## When to regenerate

The xlsx should be regenerated on every `/compliance-check` run (not just `/export-proposal`) so team members always have a current spreadsheet. `/compliance-check` writes both `.md` (source of truth) and `.xlsx` (shareable view).
