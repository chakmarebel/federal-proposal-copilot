#!/usr/bin/env python3
"""Generate a per-proposal team review briefing.

Pairs with reference/team-review-rubric.md (the general guide). The briefing
extracts the proposal-specific answer key — discriminators, Gold Team
Significant Strengths, quantified claims with evidence, and already-known
risks — so internal reviewers know which specifics NOT to soften.

Usage:
  python scripts/build-team-review-brief.py --proposal <slug>
  python scripts/build-team-review-brief.py --proposal extic-26-2
  python scripts/build-team-review-brief.py --proposal nato-diana-decision-superiority --out reviews/team-brief.md

The output is a markdown file you share alongside the draft when posting to
Google Drive for team review.
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import date

# Force utf-8 on stdout/stderr so unicode in console output (e.g. → arrows)
# doesn't crash on Windows cp1252 terminals.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass


def read(p: Path) -> str:
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def _clean(s: str) -> str:
    """Strip markdown emphasis markers and stray punctuation from a single line."""
    s = re.sub(r"\*+", "", s)
    s = re.sub(r"^[-*\s]+", "", s)
    return s.strip().rstrip(".")


def extract_significant_strengths(scorecard_text: str) -> list[dict]:
    """Pull each Significant Strength with its Basis line from a Gold Team scorecard."""
    if not scorecard_text:
        return []
    strengths = []
    pattern = re.compile(
        r"^#{1,6}\s+(Significant Strength[^\n]*)\n+"        # full header (captured)
        r"(?:[-*]\s*)?\*{0,2}Basis\*{0,2}:\s*(.+?)\n"        # Basis line
        r"(?:[-*]\s*)?\*{0,2}Benefit[^:]*\*{0,2}:\s*(.+?)\n",  # Benefit line
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(scorecard_text):
        title = _clean(m.group(1))
        basis = _clean(m.group(2).split("\n")[0])
        benefit = _clean(m.group(3).split("\n")[0])
        strengths.append({"title": title, "basis": basis, "benefit": benefit})
    return strengths


def extract_discriminators(plan_text: str) -> list[dict]:
    """Pull the Discriminators table from working/proposal-plan.md."""
    if not plan_text:
        return []
    # Find the "## Discriminators" section, capture the table that follows
    m = re.search(
        r"^#+\s+Discriminators\s*(?:\(.*?\))?\s*\n(.*?)(?=\n#+\s+|\Z)",
        plan_text,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return []
    body = m.group(1)
    rows = []
    for line in body.split("\n"):
        # Skip headers / separators / blanks
        if not line.strip().startswith("|"):
            continue
        if "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0].lower() in ("id", "#", "no.", ""):
            continue
        rows.append({
            "id": cells[0],
            "claim": cells[1] if len(cells) > 1 else "",
            "proof": cells[2] if len(cells) > 2 else "",
        })
    return rows


def extract_high_findings(redteam_text: str) -> list[dict]:
    """Pull HIGH / CRITICAL / P0 / P1 findings from red-team-notes.md or white-glove-checklist.md.

    Looks at every pipe-table row in the file and keeps those where any cell
    contains a high-severity token. Skips summary-of-counts tables.
    """
    if not redteam_text:
        return []
    findings = []
    seen_issues = set()
    for line in redteam_text.split("\n"):
        if not line.strip().startswith("|"):
            continue
        if "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        # Skip headers
        header_tokens = {"id", "#", "issue", "severity", "section", "finding"}
        if cells[0].lower() in header_tokens:
            continue
        joined = " ".join(cells)
        # Need to find an explicit high-severity token
        if not re.search(r"\b(HIGH|CRITICAL|P0|P1)\b", joined):
            continue
        # Skip summary-counts rows (rows where one cell is just an integer)
        if any(re.fullmatch(r"\d+", c) for c in cells[1:]):
            continue
        # Take first cell as ID, second as issue
        finding_id = _clean(cells[0])
        issue = _clean(cells[1])
        if not issue or issue.lower() in seen_issues:
            continue
        seen_issues.add(issue.lower())
        findings.append({"id": finding_id, "issue": issue})
        if len(findings) >= 15:
            break
    return findings


def extract_quantified_evidenced_claims(drafts_dir: Path) -> list[str]:
    """Pull lines from drafts that have both a number and an evidence marker."""
    if not drafts_dir.exists():
        return []
    claims: list[str] = []
    number_pattern = re.compile(r"\b(\d+(?:\.\d+)?(?:%|x|hrs|h|min|s|ms|GB|TB|M|B|years|year)?\b|TRL\s*\d|IL[-\s]?\d|[A-Z][a-zA-Z]+\s+\d+B)")
    evidence_pattern = re.compile(r"<!--\s*evidence:\s*EV-")
    for md_file in sorted(drafts_dir.glob("*.md")):
        for raw in md_file.read_text(encoding="utf-8", errors="replace").splitlines():
            if evidence_pattern.search(raw) and number_pattern.search(raw):
                # Strip the evidence HTML comment, trim leading list markers / bold
                clean = re.sub(r"<!--.*?-->", "", raw).strip()
                clean = re.sub(r"^[-*\s]+", "", clean)  # drop leading "- " / "* "
                clean = re.sub(r"\*+", "", clean)        # drop **bold** markers
                clean = clean.strip()
                if 20 < len(clean) < 350:
                    claims.append(clean)
    # Dedup while preserving order
    seen: set[str] = set()
    uniq: list[str] = []
    for c in claims:
        key = c[:100]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(c)
    return uniq[:15]


def render_briefing(slug: str, prop_dir: Path) -> str:
    plan = read(prop_dir / "working" / "proposal-plan.md")
    scorecard = read(prop_dir / "reviews" / "gold-team-scorecard.md")
    redteam = read(prop_dir / "reviews" / "red-team-notes.md")
    whiteglove = read(prop_dir / "reviews" / "white-glove-checklist.md")
    proposal_brief = read(prop_dir / "working" / "proposal-brief.md")

    strengths = extract_significant_strengths(scorecard)
    discriminators = extract_discriminators(plan)
    high_findings = extract_high_findings(redteam + "\n\n" + whiteglove)
    evidenced_claims = extract_quantified_evidenced_claims(prop_dir / "drafts")

    # Try to pull a title / customer line
    title_match = re.search(r"^#\s+(.+)$", proposal_brief or plan, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else slug

    out = []
    out.append(f"# Team Review Briefing — {title}")
    out.append("")
    out.append(f"**Proposal slug:** `{slug}`")
    out.append(f"**Briefing generated:** {date.today().isoformat()}")
    out.append(f"**Pair this briefing with:** [`reference/team-review-rubric.md`](../../../reference/team-review-rubric.md) — the general team-review rubric. **Read that first** if you haven't.")
    out.append("")
    out.append("This document is the proposal-specific **answer key**: the discriminators, Significant Strengths, and evidenced claims you should NOT soften. Bill has already run internal AI reviews — your job is to validate facts, not to smooth tone.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Discriminators — do NOT soften")
    out.append("")
    if discriminators:
        out.append("These are the specific competitive differentiators this proposal is built around. If you read prose that describes one of these and your instinct is to make it sound 'more professional' or 'less aggressive' — **stop**. The specificity IS the discriminator.")
        out.append("")
        out.append("| ID | Claim | Proof Point |")
        out.append("|---|---|---|")
        for d in discriminators:
            out.append(f"| {d['id']} | {d['claim']} | {d['proof']} |")
    else:
        out.append("⚠️ Could not auto-extract discriminators from `working/proposal-plan.md`. Bill: please populate manually before sharing this briefing.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Gold Team Significant Strengths — do NOT soften")
    out.append("")
    if strengths:
        out.append("These claims/sections were specifically called out in the Gold Team mock evaluation as the **load-bearing strengths** of the proposal. They are what drive the proposal's competitive position. The sections cited below are the ones an evaluator would weight most heavily.")
        out.append("")
        out.append("**If you find yourself wanting to edit one of these for tone or 'professionalism': flag it for Bill instead. Don't change it.**")
        out.append("")
        for i, s in enumerate(strengths, 1):
            basis = s["basis"]
            benefit = s["benefit"]
            out.append(f"**{i}. {s['title']}**")
            out.append(f"- *Where it lives:* {basis}")
            out.append(f"- *Why it matters:* {benefit}")
            out.append("")
    else:
        out.append("⚠️ Could not auto-extract Significant Strengths from `reviews/gold-team-scorecard.md`. Either the file doesn't exist yet, or the header pattern doesn't match. Bill: confirm `/red-team-review --mode=gold` has run, then re-generate.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Quantified claims that ARE evidenced — do NOT soften")
    out.append("")
    if evidenced_claims:
        out.append("These claims pair a specific number / name / credential with an evidence-ledger citation. The number is defensible. If you think 'we can't really say that' — we can; check the evidence ledger.")
        out.append("")
        for c in evidenced_claims:
            out.append(f"- {c}")
    else:
        out.append("_(No claims found with both numbers and evidence-ledger citations in `drafts/`. This is unusual — either drafts don't yet use the `<!-- evidence: EV-XXX -->` pattern, or no quantified claims are evidenced. Worth investigating before submission.)_")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Already-known risks (Bill is handling — please skip)")
    out.append("")
    if high_findings:
        out.append("The Red Team / White Glove reviews already identified these. **Bill is resolving them.** Don't flag them again in your review; focus your attention elsewhere.")
        out.append("")
        for f in high_findings[:12]:
            out.append(f"- **{f['id']}** — {f['issue']}")
    else:
        out.append("_(No HIGH/CRITICAL findings extracted from `reviews/red-team-notes.md`. Either the file doesn't exist or no high-severity findings are open.)_")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## What I'm asking you to do (your task)")
    out.append("")
    out.append("1. **Read [`reference/team-review-rubric.md`](../../../reference/team-review-rubric.md)** — the 5-minute briefing on how federal evaluators score proposals. This is the most important reading for first-time reviewers.")
    out.append("2. **Pick your reviewer role** — research engineer / BD owner / SME-with-context / general. Stay in your lane.")
    out.append("3. **Validate facts in your lane** — customer names, technical claims, partnership characterizations, doctrine references.")
    out.append("4. **Use the flagging structure**, not direct edits, for anything you're uncertain about (template at the bottom of the rubric).")
    out.append("5. **Spelling, grammar, broken cross-references, undefined acronyms** — fix directly.")
    out.append("6. **Do NOT** soften specific claims, restructure sections, add internal-audience clarity, or add hedging language. See the 'What NOT to do' section of the rubric for examples.")
    out.append("")
    out.append("## Time budget")
    out.append("")
    out.append("- 10 min: read the general rubric (skip if already familiar)")
    out.append("- 5 min: read this briefing")
    out.append("- 30–60 min: read the draft and validate claims in your lane")
    out.append("- 15 min: write up findings using the structured flagging template")
    out.append("- **Total: ~60–90 min**")
    out.append("")
    out.append("If you're spending more than this on tone/style suggestions, something has gone wrong — please stop and ask Bill what would actually help.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--proposal", required=True, help="Proposal slug (the directory name under proposals/)")
    ap.add_argument("--proposals-dir", default="proposals", help="Path to proposals root (default: proposals)")
    ap.add_argument("--out", help="Output path (default: proposals/<slug>/reviews/team-review-brief.md)")
    args = ap.parse_args()

    prop_dir = Path(args.proposals_dir) / args.proposal
    if not prop_dir.exists():
        print(f"No proposal at {prop_dir}", file=sys.stderr)
        return 1

    rendered = render_briefing(args.proposal, prop_dir)
    out_path = Path(args.out) if args.out else prop_dir / "reviews" / "team-review-brief.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out_path} ({len(rendered.splitlines())} lines)")

    # Auto-render to .docx so the briefing is sharable in Word without an extra step.
    docx_path = out_path.with_suffix(".docx")
    workspace_root = Path(__file__).parent.parent
    sys.path.insert(0, str(workspace_root / "tools"))
    try:
        from md_to_docx import convert_md_to_doc, setup_document  # type: ignore
        from docx import Document
        doc = Document()
        setup_document(doc)
        convert_md_to_doc(out_path, doc)
        doc.save(docx_path)
        print(f"Wrote {docx_path}")
    except Exception as e:
        print(f"  (docx render skipped: {e})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
