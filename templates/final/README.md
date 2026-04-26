# Final Submission Package

Native Office format deliverables produced by `/export-proposal`. This directory is populated **from** the drafts/working/reviews/graphics content; it is not authored directly.

## Structure

```
final/
├── docx/             ← Word documents (primary deliverable format)
├── xlsx/             ← Excel workbooks (compliance matrix, pricing artifacts)
├── pptx/             ← PowerPoint decks (optional — briefings, kickoff)
├── pdf/              ← User-produced PDFs (Word → Save As PDF)
├── graphics-png/     ← Rendered graphics (2x DPI, for Word embed)
└── PACKAGE.md        ← Manifest of every deliverable
```

## Workflow

1. Finish drafting in `drafts/*.md`
2. Run `/compliance-check` — resolve any Gap rows
3. Run `/red-team-review --mode=gold` — resolve any P0 findings
4. Run `/export-proposal` — produces `final/`
5. Open each `final/docx/*.docx` in Word
6. Review formatting (spot-check page count, graphics legibility, header/footer)
7. In Word: File → Save As → PDF → save to `final/pdf/`
8. Verify xlsx files open without errors; convert to PDF if submission requires

## Do not edit these files directly

Changes made to files in `final/` will be overwritten on the next `/export-proposal` run. If a content change is needed:
- Narrative → edit the `drafts/*.md` source
- Compliance → edit `working/compliance-matrix.md`
- Pricing → edit `working/pricing-inputs.md` or the type-specific draft in `drafts/`
- Graphics → edit `graphics/*.html`

Then re-run `/export-proposal`.

## PDF submission

Word's native "Save As PDF" preserves fonts, embedded graphics, tracked numbering, and table formatting. Do not use command-line markdown-to-PDF converters for federal submission PDFs — they drop styling and produce PDFs that look amateurish alongside competitors' Word-to-PDF submissions.
