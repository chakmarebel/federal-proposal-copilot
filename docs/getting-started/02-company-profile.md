# 02 — Populating Your Company Profile

Your company profile is the single most important input to the framework. Every skill reads it. Every draft cites it. **Time spent here pays off on every proposal you ever write.**

## Two layers

| File | Loaded when | Contents |
|---|---|---|
| `CLAUDE.md` (repo root) | Every Claude Code session in this repo | High-level brief: company name, 6-10 lines of identity + 4-6 default positioning bullets |
| `my-company/` directory | Specific skills cite specific files | Detailed source of truth: capabilities, past performance, evidence ledger, vehicles, brand assets |

`CLAUDE.md` is the elevator pitch the AI reads on every turn. `my-company/` is the dossier it pulls from when drafting specifics.

## Running `/setup-company`

The fastest path. From inside Claude Code:
```
/setup-company
```

The skill walks through ~10 prompts and generates skeleton files in `my-company/`. After the skill finishes, you'll want to refine each file by hand — the AI gets you 70% of the way.

## What goes in `my-company/`

```
my-company/
├── company.md              # Identity: name, CAGE, UEI, NAICS, certifications
├── capabilities.md         # What you do — your services and differentiators
├── past-performance.md     # 3-5 contracts you can cite as proof
├── vehicles.md             # GSA MAS, IDIQs, BPAs, OTA agreements
├── brand.json              # Colors, logos, tagline (used by graphics skill)
├── evidence-ledger.json    # Citable claims (Phase C — see below)
└── graphic-templates/      # Optional brand overrides for parametric templates
```

### `company.md`

Top-line identity. The AI references this for boilerplate cover-letter content, capability statements, etc.

**Must include:**
- Legal entity name + DBA if any
- Address, phone, key POC
- CAGE code, UEI, primary NAICS, all NAICS codes you can prime under
- Small business certifications (SDVOSB, 8(a), HUBZone, WOSB, etc.)
- Cyber posture (e.g., CMMC level, FedRAMP if applicable)
- Year founded, employee count

### `capabilities.md`

Your services / products / technical depth. Organized as 3-7 capability headings, each with 2-4 supporting bullets.

**Anti-pattern:** generic marketing copy ("end-to-end solutions for mission success"). Be specific:
- ❌ "We deliver enterprise-grade AI solutions"
- ✅ "We deliver air-gapped LLM inference on tactical hardware (Jetson Orin, x86 ruggedized) with <500ms p95 latency for 8B-parameter models"

### `past-performance.md`

3-5 contracts presented in a structured format the framework can reuse for PPQ narratives.

For each contract, include:
- Contract title, vehicle, contract number, period of performance
- Customer office + contracting officer
- Total value
- 1-paragraph scope description
- 3-5 specific outcomes (quantified where possible)
- 1 challenge encountered + how you resolved it
- Reference contact + phone/email (for PPQ submission)

### `evidence-ledger.json` (Phase C — recommended)

A structured ledger of citable claims. The `proposal-writer` skill embeds `<!-- evidence: EV-022 -->` markers in drafts so reviewers can audit every claim back to its source.

See [reference/schemas/evidence-ledger.schema.json](../../reference/schemas/evidence-ledger.schema.json) for the format and [reference/examples/evidence-ledger.example.json](../../reference/examples/evidence-ledger.example.json) for an example.

If you skip this, the writer falls back to citing past-performance.md as prose reference. Phase C is optional but **dramatically improves Gold Team review quality** because every claim is auditable.

### `brand.json`

```json
{
  "company_name_short": "Your Company",
  "company_name_full": "Your Company, Inc.",
  "tagline": "One-line positioning",
  "website": "yourcompany.com",
  "colors": {
    "bg": "#191c20",
    "accent": "#ee2929",
    "panel": "#2a2d31",
    "text": "#ffffff"
  },
  "fonts": {
    "body": "Inter",
    "display": "Inter"
  }
}
```

The graphics skill reads this to apply your brand to parametric templates. If `my-company/brand.json` is missing, the framework falls back to neutral defaults (dark canvas with red accent).

### `graphic-templates/` (optional)

If you want graphics in a different visual style than the framework default — light canvas, different layout, brand-specific component design — copy templates from `reference/graphic-templates/<pattern>/` to `my-company/graphic-templates/<pattern>/` and modify freely. The graphics skill picks up your overrides automatically.

## How long should this take?

- **First-time setup with `/setup-company`:** ~10 minutes for the skeleton
- **Refining each file by hand:** ~1-2 hours total (one good session)
- **Updating between proposals:** ~10 minutes per quarter as your company evolves

This is a one-time investment that pays off on every proposal.

## Verifying

After setup, run:
```bash
bash scripts/smoke-test.sh
```

The smoke test checks for required `my-company/` files. If any required file is missing, you'll get a clear error pointing at the gap.

## Privacy

`my-company/` is `.gitignore`'d at the repo root. Your company data **does not** get committed if you push your repo back to GitHub — even by accident. Verify with:
```bash
git status my-company/
# Should output: nothing to commit
```
