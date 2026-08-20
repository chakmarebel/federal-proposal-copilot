# Company neutralization table for federal-proposal-copilot.
#
# copilot is the company-neutral, publicly distributable mirror. Its upstreams
# (federal-proposal-assistant, proposal-workbench) are single-company working
# repos, so synced content arrives carrying one company's identity. This file is
# the single place that identity is stripped.
#
# Why a mechanical transform and not a hand-edit: a file neutralized by hand has
# to be frozen off the sync surface forever, or the next sync overwrites the
# rewording. A file neutralized by this table can stay on the surface and keep
# receiving upstream improvements. See docs/fpa-sync-model.md.
#
# Consumed by tools/sync-from-fpa.sh, tools/sync-voice-anchors.sh, and checked
# by tools/leak-scan.sh. When leak-scan reports a survivor, add a rule here
# rather than editing the synced file.
#
# Rules run in order: longer / more specific patterns first. Every rule must be
# idempotent -- no replacement may re-match its own pattern.

# ---- Repo and service identity ----
s#bd\.edgerunner-pipeline\.com#bd.example-pipeline.com#g
s#github\.com/chakmarebel/federal-proposal-assistant#github.com/<you>/federal-proposal-copilot#g
s#chakmarebel/federal-proposal-assistant#<you>/federal-proposal-copilot#g
# NOTE: the bare repo name "federal-proposal-assistant" is deliberately NOT
# rewritten. It is a repo name, not a company identifier, and the shared
# doctrine names all three sibling repos in one sentence -- rewriting it
# there produced "copilot, and copilot".
s#my-company/edgerunner-profile\.md#my-company/company-profile.md#g
s#edgerunner-warrant#verification-ledger#g

# ---- Operator-local filesystem paths ----
s#[A-Za-z]:\\Users\\wbal9[^"'`]*#<local-path>#g
s#[A-Za-z]:/Users/wbal9[^ "'`]*#<local-path>#g
s#/c/Users/wbal9[^ "'`]*#<local-path>#g

# ---- Company and product names ----
s#\bEdgeRunner AI\b#[Your Company]#g
s#\bEdgeRunner\b#[Your Company]#g
s#\bedgerunner\b#your-company#g
s#\bWarClaw\b#[Runtime Product]#g
s#\bWarclaw\b#[Runtime Product]#g
s#\bwarclaw\b#agentic-orchestration#g
s#\bEVELYN\b#[Reasoning Product]#g
s#\bEvelyn\b#[Reasoning Product]#g
s#\bevelyn\b#computer-vision#g

# ---- Registration identifiers ----
s#\b9Z176\b#<CAGE>#g
s#\bSLZTJUA8DBD3\b#<UEI>#g
s#carries 541511 primary#carries <primary NAICS>#g

# ---- Location ----
s#11011 NE 9th St[^.]*#<company address>#g
s#\bBellevue, Washington\b#<City, State>#g
s#\bBellevue, WA\b#<City, ST>#g
s#\bBellevue WA\b#<City ST>#g

# ---- Standing corporate facts ----
# These appear in the "Standing content to reuse" blocks of the section
# patterns, where the upstream repo inlines its own facts as a drafting
# shortcut. In copilot they must read as slots the operator fills from
# my-company/.
s#veteran-founded small business#<business size and socioeconomic status>#g
s#founded February 2024, 22 full-time#founded <year>, <N> full-time#g
s#Series A \$17\.5M closed May 2025#<funding stage, amount, and date>#g

# ---- Leadership names ----
s#\bTyler Saltsman\b#<CEO>#g
s#\bColton Malkerson\b#<COO>#g
s#\bJack FitzGerald\b#<Chief Science Officer>#g
s#\bVincent Lu\b#<CTO>#g
