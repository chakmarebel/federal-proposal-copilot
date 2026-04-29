# Corpus Entry Template

These files are the template for each new corpus entry. The `/capture-submission` skill copies and renames them when you snapshot a proposal.

## Files

- `manifest.json.example` → becomes `<slug>/manifest.json`
- `edit-notes.md.template` → becomes `<slug>/edit-notes.md`

The skill does the copying. You shouldn't need to touch these files unless you want to evolve the templates themselves.

## Editing the templates

If you want to change what's collected for every new entry — for example, adding a new edit category or tracking a new metadata field:

1. Edit the template file in this directory
2. Future entries will use the new template
3. Existing entries are NOT migrated automatically — they keep the template version they were created with

This is intentional. Backfilling a new field across old entries is usually not worth the effort. Just start collecting it forward.
