# /setup-company

One-time setup skill that creates the `my-company/` directory with company-specific boilerplate files. Run this once when first cloning the repository, or again to update company information.

## Trigger

User runs `/setup-company` or asks to set up their company profile.

## Workflow

Ask the user for each piece of information below, one section at a time. Wait for their response before moving to the next section. Be conversational but efficient.

### Step 1: Company Identity

Ask the user:
> What is your company's legal name and headquarters location (city, state)?

### Step 2: Company Description

Ask the user:
> In one paragraph (3-5 sentences), describe what your company does. Focus on: what problem you solve, for whom, and what makes your approach different.

### Step 3: Core Capabilities

Ask the user:
> List your 3-5 core capabilities as bullet points. These should be the things your company does best -- the capabilities you lead with in proposals.

### Step 4: Products and Services

Ask the user:
> List your products and services. For each, provide:
> - Product/service name
> - One-line description
> - Category (e.g., Software, Hardware, Professional Services, Managed Service)
>
> You can paste a table or just list them.

### Step 5: SAM.gov Registration

Ask the user:
> Provide your SAM.gov registration details:
> - CAGE Code
> - Unique Entity ID (UEI)
> - Primary NAICS codes (list all that apply)
>
> If you don't have these yet, type "skip" and you can fill them in later.

### Step 6: Contract Vehicles

Ask the user:
> What contract vehicles and procurement pathways do you use? Examples:
> - GSA Schedule (include contract number)
> - Tradewinds
> - SEWP V
> - NASA SEWP
> - CIO-SP3 / CIO-SP4
> - Other GWACs or BPAs
>
> List each vehicle with its contract number if available. If none, type "none yet."

### Step 7: Past Performance

Ask the user:
> List your past performance -- customers, programs, and current status. For each entry, provide:
> - Customer/agency name
> - Program or project name
> - Brief description (1-2 sentences)
> - Status (active, completed, ongoing)
> - Contract type if known (FFP, T&M, CPFF, etc.)
>
> Also list any CRADAs, research agreements, or partnerships with government labs.

### Step 9: Capture Profile

Ask the user:
> What types of government contracts does your company primarily pursue? Select all that apply:
>
> **Innovation-focused / Responsive (shorter timelines, less formal):**
> - SBIR / STTR
> - CSO (Commercial Solution Opening)
> - OTA (Other Transaction Authority prototype agreements)
> - BAA (Broad Agency Announcement)
> - White papers / unsolicited proposals
>
> **Formal Competitive (longer capture cycles, full Shipley process):**
> - Competitive RFP / RFQ (FAR-based)
> - IDIQ / Task Order competitions (e.g., STARS, OASIS, SeaPort)
> - GWAC / BPA
> - Recompetes
>
> Based on your answer, we'll set a default capture mode that scales the depth of competitive analysis, pricing, and past performance work automatically. You can override it on any individual proposal.

**Determine the default capture mode from their answer:**
- Primarily responsive vehicles (SBIR/CSO/OTA/BAA/white papers) → `Responsive`
- Primarily formal competitive (RFP/IDIQ/task orders/recompetes) → `Full Capture`
- Mix of both → `Ask Per Proposal`

### Step 8: Brand Palette (Optional)

Ask the user:
> Optionally, provide your brand color palette with hex codes:
> - Primary color (main brand color)
> - Accent color (secondary/highlight)
> - Background color
> - Text color
> - Any additional brand colors
>
> If you don't have these or want to skip, type "skip" and we'll use a professional default palette (navy/white/gold).

## File Generation

After collecting all information, generate the following files in `my-company/`:

### my-company/company-description.md

```markdown
# Company Description

## One-Paragraph Description
[Full paragraph from Step 2]

## Three-Bullet Summary
- [Distill paragraph into bullet 1: what you do]
- [Distill paragraph into bullet 2: for whom]
- [Distill paragraph into bullet 3: differentiator]

## One-Sentence Description
[Compress to a single sentence suitable for headers and footers]

## Company Details
- **Legal Name:** [from Step 1]
- **Headquarters:** [from Step 1]
```

### my-company/capabilities.md

```markdown
# Capabilities

## Core Capabilities
[Bullets from Step 3]

## Products and Services

| Product/Service | Description | Category |
|----------------|-------------|----------|
| [Name] | [Description] | [Category] |
[... one row per item from Step 4]

## Capability Summary
[Generate a 2-3 sentence summary combining core capabilities and product portfolio, suitable for proposal introductions]
```

### my-company/contract-vehicles.md

```markdown
# Contract Vehicles and Registration

## SAM.gov Registration
- **CAGE Code:** [from Step 5]
- **Unique Entity ID (UEI):** [from Step 5]

## NAICS Codes

| NAICS Code | Description |
|-----------|-------------|
| [Code] | [Standard NAICS description] |
[... one row per code from Step 5]

## Contract Vehicles

| Vehicle | Contract Number | Status | Notes |
|---------|----------------|--------|-------|
| [Name] | [Number] | Active | [Any relevant details] |
[... one row per vehicle from Step 6]

## Proposal Footer Format
[Company Name] | CAGE: [Code] | UEI: [ID]
```

### my-company/past-performance.md

```markdown
# Past Performance

## Deployments and Programs

| Customer | Program | Description | Status | Contract Type |
|----------|---------|-------------|--------|---------------|
| [Agency] | [Program] | [Description] | [Status] | [Type] |
[... one row per entry from Step 7]

## Research Agreements and Partnerships
[List any CRADAs, OTAs, research partnerships, or lab collaborations from Step 7. If none, write "None currently."]

## Past Performance Summary
[Generate a 2-3 sentence summary of past performance breadth and depth, suitable for proposal past performance introductions]
```

### my-company/capture-profile.md

```markdown
# Capture Profile

## Default Capture Mode
[Full Capture / Responsive / Ask Per Proposal]

## Typical Proposal Types
[List of vehicles checked by the user — e.g., SBIR, OTA, Competitive RFP, IDIQ]

## Mode Definitions
- **Full Capture**: Complete competitive analysis (Bidder Comparison Chart, weighted scoring), formal BOE and cost volume, PPQ-format past performance blocks. Use for competitive RFPs, IDIQ task orders, recompetes.
- **Responsive**: Lightweight competitive landscape overview, vehicle-appropriate pricing (ROM / SBIR template / milestone schedule), relevant experience narratives instead of formal PPQs. Use for SBIR, CSO, OTA, BAA, white papers.
- **Ask Per Proposal**: Prompted to select mode each time `/new-proposal` runs.

## Override Instructions
To override the default for a specific proposal, edit the `Capture Mode` field in `working/proposal-brief.md` after running `/new-proposal`.
```

### my-company/brand-palette.md

If the user provided colors:

```markdown
# Brand Palette

## Colors
| Role | Hex | Usage |
|------|-----|-------|
| Primary | [hex] | Headers, title bars, primary buttons |
| Accent | [hex] | Highlights, callout boxes, links |
| Background | [hex] | Page background, table backgrounds |
| Text | [hex] | Body text, labels |
[... any additional colors]

## Tier Treatments
- **Tier 1 (Headers):** Primary color background, white text
- **Tier 2 (Subheaders):** White background, primary color text
- **Tier 3 (Body):** White background, text color

## Element Patterns
- **Tables:** Primary header row, alternating white/light-gray body rows
- **Callout Boxes:** Accent color left border, light background
- **Diagrams:** Primary for main elements, accent for highlights, text color for labels
```

If the user skipped or didn't provide colors, use this default:

```markdown
# Brand Palette

## Colors
| Role | Hex | Usage |
|------|-----|-------|
| Primary | #1B3A5C | Headers, title bars, primary buttons |
| Accent | #C5962E | Highlights, callout boxes, links |
| Light Accent | #E8D5A3 | Subtle highlights, table accents |
| Background | #FFFFFF | Page background |
| Light Gray | #F5F5F5 | Alternating table rows, card backgrounds |
| Text | #2D2D2D | Body text, labels |
| Muted Text | #6B6B6B | Captions, secondary labels |

## Tier Treatments
- **Tier 1 (Headers):** Primary (#1B3A5C) background, white text
- **Tier 2 (Subheaders):** White background, primary (#1B3A5C) text
- **Tier 3 (Body):** White background, text (#2D2D2D) color

## Element Patterns
- **Tables:** Primary header row with white text, alternating white/#F5F5F5 body rows
- **Callout Boxes:** Accent (#C5962E) left border, #F5F5F5 background
- **Diagrams:** Primary for main elements, accent for highlights, text color for labels
```

## Completion

After generating all files, confirm to the user:
> Company profile created in `my-company/`. Files generated:
> - `company-description.md`
> - `capabilities.md`
> - `contract-vehicles.md`
> - `past-performance.md`
> - `brand-palette.md`
> - `capture-profile.md`
>
> You can edit these files directly at any time. To update your profile, run `/setup-company` again.
> Your default capture mode is set to **[mode]**. You can override this per proposal when you run `/new-proposal`.
