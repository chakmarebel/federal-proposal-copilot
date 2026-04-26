# Section Patterns Library

One pattern set per proposal-type category. The registry's `section_patterns` field selects which file applies. `proposal-writer` reads `working/proposal-type.md` → pulls `section_patterns` → loads `reference/section-patterns/<id>.md` → produces sections per that file's structure.

## Mapping

| section_patterns id | File | Used by proposal types |
|---|---|---|
| `full-proposal` | [full-proposal.md](full-proposal.md) | `far-rfp`, `idiq-to`, `cso-full` |
| `white-paper` | [white-paper.md](white-paper.md) | `white-paper`, `cso-brief`, `ota-white-paper` |
| `baa` | [baa.md](baa.md) | `baa` |
| `ota` | [ota.md](ota.md) | `ota-proposal` |
| `sbir` | [sbir.md](sbir.md) | `sbir-phase1`, `sbir-phase2` |
| `rfi` | [rfi.md](rfi.md) | `rfi` |
| `sources-sought` | [sources-sought.md](sources-sought.md) | `sources-sought` |
| `rom` | [rom.md](rom.md) | `rom` |
| `gsa-mas-task-order` | [gsa-mas-task-order.md](gsa-mas-task-order.md) | `gsa-mas-task-order` (NEW — multi-volume technical/price/security submissions for GSA MAS-flighted BPA / IDIQ task-order competitions) |
| `security-volume` | [security-volume.md](security-volume.md) | Reusable supplement — used by ANY proposal type with cleared-contract requirements (FAR full proposal, IDIQ TO, OTA, GSA MAS task-order, SBIR with classified work). Not tied to a single proposal type. |

## File structure (every pattern file)

Each file declares:

```yaml
---
patterns_id: <id>
display_name: <human name>
typical_length: <pages>
section_order: [ordered list of section ids]
required_sections: [list of ids — writer must produce these]
optional_sections: [list of ids — writer includes if material exists]
---
```

Then a body section per section id, with:
- Purpose (what scoring point it makes)
- Structure (paragraph/table/bullet outline)
- Template (`[PLACEHOLDER]`-marked starter)
- Patterns to apply (theme statement? discriminator proof? action caption? — per `reference/proposal-writing-patterns.md`)
- Common pitfalls

## How `proposal-writer` consumes these

1. Read `working/proposal-type.md`. Extract `section_patterns`.
2. Read `reference/section-patterns/<section_patterns>.md`.
3. For each section in the pattern file's `section_order`:
   - If required → produce a draft file in `drafts/<section-id>.md` with the structure + applicable winning patterns
   - If optional → produce only if relevant source material exists
4. Update the compliance matrix per each drafted section.

**Output filenames derive from pattern section ids, not hardcoded.** Older versions of proposal-writer declared a fixed output set (executive-summary.md, technical-approach.md, etc.) — deprecated. The type-aware flow uses the section ids from the pattern file.

## Adding a new pattern set

Add a `<id>.md` here with the frontmatter + body structure above. Add a row to the table. Reference it from a proposal type's `section_patterns` field. That's it.
