# Output Discipline — Universal Doctrine

How the workbench expects every drafted section to read, regardless of which
company persona is active. Per-company tone or style notes can adjust prose
voice but do not weaken the structural rules below.

## Structure

- Section drafts are markdown with explicit headings the evaluator can
  navigate. Do not bury structure inside narrative paragraphs.
- Every section ends with a `Gaps and Follow-Ups` block, even when empty
  (`*No open gaps.*` is a valid value). The block makes silent assumptions
  forensically visible.
- When an evidence citation supports a claim, cite the evidence id in line
  (`[EV-901]`) rather than describing the source in prose.

## Voice

- Active voice with concrete verbs. "The system processes" beats "the
  system is designed to process."
- Specific numbers over qualitative adjectives. "Sustained 12 TPS at 4-bit
  quantization" beats "high throughput."
- Address the evaluator's question directly in the opening sentence. Do
  not start sections with company-name boilerplate.

## Evaluator-oriented framing

- Lead each section with the evaluator question the section answers
  (paraphrased from the SOW or PWS).
- Order proof points by how heavily the evaluator weights them, not by
  ease of writing.
- When an evaluator weights criteria explicitly (e.g., "Technical Merit
  60%, Cost 25%, Past Performance 15%"), the section's depth must
  reflect that weighting. Do not over-invest in low-weight sections.

## When doctrine and an active override conflict

The override wins, but the section MUST include a `Doctrine deviations
cited` block naming the override file's deviation entry. Reviewers should
be able to read the section and immediately see which override was relied
on, when it was decided, and why.

## When the active task lacks evidence

Mark the gap in `Gaps and Follow-Ups`. Do not weaken surrounding prose to
fit. An honest gap reviewed at red-team is faster to close than an
invented claim audited at the gold-team review.
