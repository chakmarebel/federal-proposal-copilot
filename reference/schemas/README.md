# JSON Schemas

Structured sidecar formats that live alongside the markdown artifacts. Introduced in **v1.5 Phase A** (see [docs/v1.5-plan.md](../../docs/v1.5-plan.md)).

## Why sidecars

Markdown is the human-readable view. JSON is the machine-readable view. Both are written by the same skill on the same invocation. Downstream consumers (dashboard, smoke test, compliance-check heuristic, future v2 migration) read the JSON; humans read the markdown.

This avoids the brittle "re-parse prose on every run" pattern while preserving everything that makes markdown proposals reviewable and git-trackable.

## Schemas

| Schema | Sidecar file | Produced by | Purpose |
|---|---|---|---|
| [compliance-matrix.schema.json](compliance-matrix.schema.json) | `working/compliance-matrix.json` | `/compliance-check` | Requirement tracking — all rows + summary counters |
| [proposal-plan.schema.json](proposal-plan.schema.json) | `working/proposal-plan.json` | `/proposal-manager` | Eval factors, win themes, discriminators, bid/no-bid |
| [activity-entry.schema.json](activity-entry.schema.json) | `working/activity.md` (each line maps to one entry) | all content-producing skills | Machine view of the activity trail |
| [ai-run.schema.json](ai-run.schema.json) | `working/ai-runs.jsonl` | all AI-invoking skills | One JSON line per model call with token + cost estimates |

## Schema versioning

Each schema carries a `$id` with a version suffix (e.g., `compliance-matrix.v1`). Breaking changes bump to v2 with a separate file. Consumer code should check the `schema_version` field in sidecar files and warn-or-degrade on mismatch.

## Writing a sidecar

Skills that emit sidecars must:

1. Include a `schema_version` field matching the schema's `$id` version
2. Include a `generated_by` field (skill name)
3. Include a `generated_at` ISO-8601 timestamp
4. Write the sidecar on every invocation (atomic — full rewrite, not patch)
5. The skill owns the schema; humans can edit the markdown, but skills own the JSON

## Reading a sidecar

Consumers (dashboard, smoke test, other skills) should:

1. Prefer the JSON sidecar over re-parsing the markdown
2. Check `schema_version` compatibility; warn if unknown
3. Fall back to markdown parse if JSON sidecar is missing (backward compatibility during v1.5 rollout)

## Validation

The smoke test (`bash scripts/smoke-test.sh`) validates:
- All schemas parse as valid JSON
- Required top-level fields are present
- Schema `$id` matches filename

Deep schema validation (e.g., via `jsonschema` Python lib) is performed by the Phase B dashboard when it ingests sidecars for rendering.

## Adding a new schema

1. Create `reference/schemas/<name>.schema.json` following Draft-07 + the conventions above
2. Add a row to the table in this README
3. Update the producing skill to emit the sidecar alongside its markdown output
4. Add a row to the smoke test's schema-validation block
