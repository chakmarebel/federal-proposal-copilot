# Distribution Statements

Reference for DoD distribution statements per DoD Directive 5230.24 and DoDI 5230.29. Apply the appropriate statement to the cover page and, for longer documents, to section cover pages.

## Statement A -- Public Release

**Text:**
> Distribution Statement A. Approved for public release; distribution is unlimited.

**When to use:**
- Information cleared for public release by the originating organization's public affairs office.
- Published research, open-source reports, and unclassified general-audience materials.
- Rarely appropriate for proposals (proposals typically contain proprietary content).

## Statement B -- U.S. Government Agencies Only

**Text:**
> Distribution Statement B. Distribution authorized to U.S. Government agencies only; [reason]; [date of determination]. Other requests for this document shall be referred to [controlling DoD office].

**When to use:**
- Contains information that could reveal sensitive technical capabilities or vulnerabilities.
- Common reasons: Foreign Government Information, Contractor Performance Evaluation, Premature Dissemination, Test and Evaluation, Administrative/Operational Use.
- Appropriate for technical proposals containing sensitive-but-unclassified system details.

**Required fields:**
- Reason for restriction (choose from standard reasons list)
- Date of determination
- Controlling DoD office name and address

## Statement C -- U.S. Government Agencies and Contractors

**Text:**
> Distribution Statement C. Distribution authorized to U.S. Government agencies and their contractors; [reason]; [date of determination]. Other requests for this document shall be referred to [controlling DoD office].

**When to use:**
- Information needed by government contractors to perform current contracts.
- Contains technical data with legitimate contractor need-to-know.
- Common for proposals responding to solicitations where contractor teaming is expected.

**Required fields:**
- Reason for restriction
- Date of determination
- Controlling DoD office name and address

## Statement D -- DoD and U.S. DoD Contractors Only

**Text:**
> Distribution Statement D. Distribution authorized to the Department of Defense and U.S. DoD contractors only; [reason]; [date of determination]. Other requests for this document shall be referred to [controlling DoD office].

**When to use:**
- Information restricted to DoD and its contractor base.
- Contains technical data relevant only to defense applications.
- More restrictive than Statement C; excludes non-DoD government agencies.

**Required fields:**
- Reason for restriction
- Date of determination
- Controlling DoD office name and address

## Statement E -- DoD Components Only

**Text:**
> Distribution Statement E. Distribution authorized to DoD components only; [reason]; [date of determination]. Other requests for this document shall be referred to [controlling DoD office].

**When to use:**
- Restricted to DoD military and civilian personnel only.
- Excludes contractors entirely.
- Used for highly sensitive operational or intelligence-related materials.

**Required fields:**
- Reason for restriction
- Date of determination
- Controlling DoD office name and address

## Statement F -- Further Dissemination Only as Directed

**Text:**
> Distribution Statement F. Further dissemination only as directed by [controlling DoD office] or higher DoD authority; [date of determination].

**When to use:**
- Most restrictive unclassified distribution statement.
- Dissemination controlled on a case-by-case basis by the controlling office.
- Typically used for pre-decisional policy documents, acquisition-sensitive materials, or source-selection information.

**Required fields:**
- Controlling DoD office name and address
- Date of determination

## Recommended Defaults by Submission Type

| Submission Type | Recommended Statement | Rationale |
|----------------|----------------------|-----------|
| White paper (open BAA) | B or C | Contains proprietary technical approach |
| RFI response | B | Government-only review of capabilities |
| RFP proposal (full & open) | B | Source-selection sensitive material |
| RFP proposal (limited competition) | B or F | May contain highly sensitive technical data |
| Capability briefing | B or C | Depends on audience and content sensitivity |
| CRADA proposal | B | Government-only evaluation |
| OTA proposal | B | Government-only evaluation |
| Published research | A | Approved for public release |

**Note:** Always check the solicitation for specific distribution statement guidance. The government may specify which statement to use. When in doubt, use Statement B and let the government determine broader distribution.

## CUI Marking Guidance

### Controlled Unclassified Information (CUI)

If the solicitation involves CUI, follow these marking requirements:

**Banner Markings (top and bottom of each page):**
```
CUI
```
or
```
CONTROLLED
```

**CUI Category Markings (when specified):**
```
CUI//SP-CTI
```
(Example: CUI with Specified category of Controlled Technical Information)

**Common CUI Categories in Defense Proposals:**
| Category | Marking | Typical Content |
|----------|---------|----------------|
| Controlled Technical Information | CUI//SP-CTI | Technical data with export control |
| Export Controlled | CUI//SP-EXPT | ITAR/EAR controlled information |
| Procurement and Acquisition | CUI//SP-PROPIN | Source selection, bid/proposal info |
| Privacy | CUI//SP-PRVCY | PII of personnel |

**CUI Designation Indicator Block (cover page):**
```
Controlled by: [Controlling agency]
Controlled by: [Controlling office]
CUI Category: [Category]
Distribution/Dissemination Control: [Distribution statement]
POC: [Name, phone, email]
```

### Best Practices
- Mark every page, not just the cover.
- CUI markings go above distribution statements.
- When in doubt about CUI applicability, ask the contracting officer.
- Proposals containing CUI must be transmitted via approved channels (encrypted email, SAFE, etc.).
- Do not apply CUI markings unless the information qualifies -- overmarking creates compliance issues.
