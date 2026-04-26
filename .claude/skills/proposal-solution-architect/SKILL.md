---
name: proposal-solution-architect
description: Use this skill when analyzing a solicitation or white paper task to build requirements matrices, capability mappings, solution strategies, and architecture concepts. Reads from inputs/ and writes structured analysis to working/ files.
---

# Proposal Solution Architect Skill

## Purpose
Transform source materials into a defensible technical solution and proposal-ready working structure.

## When to Use
- A new solicitation or white paper is introduced
- Requirements must be extracted from source documents
- Capabilities must be mapped to requirements
- Architecture must be designed
- Gaps and assumptions must be identified

## File Retrieval Rules
Always read from these folders in order:
1. `inputs/00_priority/`
2. `inputs/01_customer/`
3. `inputs/02_yourCompany/`
4. `inputs/03_teammates/`
5. `inputs/04_patterns/`

Do not proceed to solution design until:
- Solicitation is reviewed
- Requirements are extracted
- Customer constraints are understood

If any required input is missing, explicitly state it.

## Workflow
1. Read all relevant source files from `inputs/`
2. Create or update these working files:
   - `working/requirement-matrix.md`
   - `working/capability-matrix.md`
   - `working/assumptions-and-risks.md`
   - `working/solution-strategy.md`
   - `working/architecture-concept.md`

3. Output in this order:
   - Key requirements (table)
   - Implied evaluation logic
   - Capability mapping (table)
   - Gaps and assumptions
   - Recommended solution concept
   - Architecture summary

## Rules
- Do not invent facts
- Reuse repository material where applicable
- Identify missing proof points
- Flag weak differentiators
- Recommend architecture changes when needed
- Prefer tables over long narrative during analysis
- **Write all outputs to working/ files on disk**

## Lessons Learned (Calibration Session — White Paper Architecture)
- **Structure challenges as problems, not solutions.** Frame each challenge around what's broken ("Enterprise AI assumes connectivity — that assumption fails in austere environments") rather than what needs to happen ("Enable disconnected AI"). This is more compelling for evaluators.
- **Three-challenge structure works well for white papers.** Organize around 3 distinct gaps (e.g., on-device execution, model lifecycle, data feedback loop). Each maps to a solution section — clean 1:1 mapping, no overlap.
- **Define the overview vs. detail boundary early.** The overview section (e.g., "[Your Company]: The Tactical Operations Layer") should be a concise "what is it" intro (~200 words). Detail sections carry all the technical depth. Plan this split during architecture to prevent duplication.
- **Include eval/benchmarking as a capability.** Mission-representative evaluation — building statistically significant test sets that reflect warfighter needs — is a differentiator worth calling out in the architecture concept.
- **Position data capture as optional.** When describing operational data feedback loops, frame data capture as an opportunity ("when operational data is available, it can be leveraged") rather than a requirement. This avoids triggering security/privacy concerns.
- **Identify boilerplate blocks early.** Company description, CAGE/UEI/NAICS, past performance, distribution statements — flag these as reusable blocks in the architecture phase so writers don't reinvent them.

## Requirement Matrix Format
| ID | Requirement | Source | Explicit/Implicit | Response Approach | Capability Source | Gap/Risk |
|----|-------------|--------|-------------------|-------------------|-------------------|----------|

## Capability Matrix Format
| Req ID | Needed Capability | Your Company's Contribution | Partner Contribution | Evidence Source | Gap |
|--------|-------------------|----------------------------|---------------------|----------------|-----|

## Architecture Output Format
- Mission objective
- Core components
- Interfaces and integrations
- Data flows
- Control/governance layers
- Deployment model
- Differentiators
- Risks
