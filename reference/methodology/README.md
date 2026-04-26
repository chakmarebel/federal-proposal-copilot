# Proposal Methodology Library

Industry-standard methodologies and frameworks that govern how the proposal lifecycle is run — from market positioning through lessons learned. Distinct from the **calibration libraries** (`reference/proposal-conventions/`, `reference/section-patterns/`, `reference/graphic-templates/`), which capture *what winning proposals look like*. Methodology covers *how the work is organized*.

**Where these come from:** structural and methodological extraction from canonical published references (Shipley Proposal Guide, BD-CMM, etc.) plus calibration against author-owned winning proposals. **No source-text reproduction** — patterns are abstracted into the framework's own language and cite the source generally.

## Files

| File | Topic | Source basis |
|---|---|---|
| [shipley-alignment.md](shipley-alignment.md) | Cross-walk between Shipley conventions and this framework — alignments, divergences, gaps | Shipley Proposal Guide, 2026-04-25 |
| [color-teams.md](color-teams.md) | The canonical 6-team color review model (Blue / Black Hat / Pink / Red / Gold / Lessons Learned) | Shipley Proposal Guide §Reviews |
| [capture-planning.md](capture-planning.md) | Capture-management methodology for federal opportunities (5-phase structure + Integrated Solution Worksheet + Bidder Comparison Matrix) | Shipley Proposal Guide §Capture Planning |
| [bd-process.md](bd-process.md) | 6-phase business development process with 5 milestone decision points (Interest / Pursuit / Pre-Bid / Bid / Submit) | Shipley Proposal Guide §Process |

## How skills consume methodology

| Methodology doc | Skills informed |
|---|---|
| `color-teams.md` | `red-team-review` (mode definitions, sequencing) |
| `capture-planning.md` | `capture-scorecard`, `opportunity-quick-look`, `competitor-assessment`, `customer-intel` |
| `bd-process.md` | `opportunity-quick-look`, `proposal-manager`, `capture-scorecard` |

## Shipley alignment posture

This framework was originally calibrated against author-owned winning proposals (FAR / SBIR / GSA MAS). On 2026-04-25 we cross-checked the resulting conventions against the Shipley Proposal Guide. Result: **strong alignment overall**; **three meaningful divergences** documented in [shipley-alignment.md](shipley-alignment.md) and reflected in the relevant skill / pattern files.

The framework's posture: **align with Shipley naming and discipline by default** (because evaluators trained on Shipley will read the framework's outputs more easily), but document deliberate divergences with rationale.

## Source-content protection

Same discipline as the calibration libraries:
- No verbatim quotes from Shipley or other commercial references
- Methodology described in the framework's own language
- Citations are general (chapter-level), never page-specific reproductions
- The Shipley book itself is not stored in the repo — only patterns extracted from it

## Adding a new methodology source

If you have another canonical reference (Capture Guide, Color Team Review Guide, etc.):

1. Read the source for structural/methodological patterns
2. Cross-check against existing framework files
3. Add to `shipley-alignment.md` (or create a parallel alignment doc for the new source)
4. Update or create methodology docs as needed
5. Cite the source by name + chapter-level reference; never reproduce text

See the calibration changelog at the bottom of [shipley-alignment.md](shipley-alignment.md) for the working pattern.
