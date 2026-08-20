"""Shared vocabulary, evidence matching, and exposure scoring for the demand signal loop.

Imported by extract-demand-signals.py, build-demand-signal-brief.py, and
backfill-demand-signals.py. The theme keyword lists live here so there is exactly one place
that decides what a capability theme means — a second copy would drift and split themes.

The piece that matters most here is exposure scoring. A count of who asked for what is an
inventory; nobody prioritizes from an inventory. Exposure crosses demand against PROOF —
what the evidence ledger can actually substantiate — because the decision Vincent owns is
not "what did customers say" but "where are we exposed."
"""

import json
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent
THEMES_FILE = WORKSPACE_ROOT / "reference" / "capability-themes.md"
LEDGER_FILE = WORKSPACE_ROOT / "my-company" / "evidence-ledger.json"
ALIASES_FILE = WORKSPACE_ROOT / "reference" / "customer-aliases.tsv"

OPEN_STATUSES = {"gap", "no-plan"}
# Statuses where we are asserting a capability rather than admitting we lack one. These are
# the rows that become claim risk when the ledger cannot back them.
CLAIMING_STATUSES = {"shipping", "prototype", "roadmap"}

THEME_KEYWORDS: dict[str, tuple[str, ...]] = {
    "air-gap-ddil-deployment": (
        "air-gap", "air gap", "airgap", "ddil", "disconnected", "denied", "degraded",
        "offline", "no connectivity", "bandwidth-limited", "fly-away", "forward deploy",
        "tactical edge", "intermittent", "without cloud", "on-prem",
    ),
    "model-serving-api-interop": (
        "openai-compatible", "openai compatible", "serving api", "model-serving",
        "standard api", "interoperable api", "api gateway", "endpoint", "sdk",
        "hosting platform", "interoperab",
    ),
    "multi-model-hosting-byom": (
        "multi-model", "multiple models", "byom", "bring your own model", "model choice",
        "side-by-side", "compare outputs", "monolith", "single-vendor", "single vendor",
        "model agnostic", "model-agnostic", "diversified architecture", "vendor lock",
        "model weights", "open-weight", "open weight",
    ),
    "tevv-eval-harness": (
        "tevv", "t&e", "test and evaluation", "benchmark", "eval harness", "evaluation harness",
        "red team", "red-team", "acceptance criteria", "measur", "scorecard", "assess performance",
        "mil-bench", "mildeflect", "mil-deflect",
    ),
    "output-verification-attribution": (
        "hallucinat", "citation", "cited", "attribut", "provenance", "verif", "ground truth",
        "traceab", "auditab", "icd 203", "icd-203", "confidence", "claim-level", "receipt",
        "wbom", "warrant",
    ),
    "agentic-orchestration": (
        "agentic", "agent", "orchestrat", "workflow automation", "tool call", "tool use",
        "autonomous task", "multi-step", "agentic-orchestration",
    ),
    "mission-mos-finetuning": (
        "fine-tun", "finetun", "lora", "adapter", "mission-specific", "mission specific",
        "domain-specific model", "tuned", "tuning", "mos", "doctrine-calibrat", "purpose-built",
        "mission adaptation", "military-specific", "custom model",
    ),
    "non-refusal-behavior": (
        "refus", "abliterat", "decensor", "unchained", "guardrail", "over-align", "deflect",
        "answer-rate", "answer rate",
    ),
    "multimodal-imagery-fmv": (
        "imagery", "fmv", "full motion video", "full-motion video", "video", "object detect",
        "target identif", "target id", "annotat", "geospatial", "eo/ir", "isr", "computer vision",
        "sar ", "atr", "computer-vision",
    ),
    "multimodal-audio": (
        "audio", "speech", "transcri", "voice", "radio traffic", "sigint audio", "speaker",
    ),
    "data-labeling-curation": (
        "label", "annotation pipeline", "synthetic data", "data curation", "data clean",
        "human-in-the-loop", "training data pipeline", "corpus construction", "data prep",
        "ontolog", "coco", "dota", "6-dof",
    ),
    "ato-accreditation-artifacts": (
        "ato", "accredit", "rmf", "cato", "stig", "authorization to operate", "impact level",
        "il4", "il5", "il6", "il-4", "il-5", "il-6", "fedramp", "cmmc", "control evidence",
        "authoriz", "iatt", "800-171", "zero trust",
    ),
    "hardware-footprint-compression": (
        "quantiz", "compress", "swap", "footprint", "on-device", "gpu", "hardware",
        "latency", "memory", "edge device", "laptop", "tegra", "jetson", "throughput on",
        "dgx", "vllm", "tensorrt",
    ),
    "utilization-telemetry-metrics": (
        "utilization", "telemetry", "adoption", "usage metric", "dashboard", "monitor",
        "transparent", "reporting to", "query volume", "power-bi", "power bi",
    ),
    "cross-domain-model-update": (
        "upgrade", "update path", "progressive", "future iteration", "patch", "sneakernet",
        "one-way transfer", "model refresh", "across the air gap", "cross-air-gap",
    ),
    "federation-cross-enclave": (
        "federat", "cross-domain", "cross domain", "multi-enclave", "coalition",
        "partner nation shar", "multi-classification", "enclave-to-enclave", "jwics", "siprnet",
    ),
    "retrieval-over-doctrine": (
        "rag", "retrieval", "doctrine", "oporder", "opord", "local document", "knowledge base",
        "document ingest", "vector", "corpus search", "regulation", "mdmp",
    ),
    "multilingual-translation": (
        "translat", "multilingual", "language coverage", "low-resource language",
        "foreign language", "transliterat",
    ),
    "token-cost-economics": (
        "cost per", "per-token", "per token", "licensing model", "seat", "price",
        "metering", "cost model", "affordab",
    ),
    "training-data-rights": (
        "data right", "government purpose right", "gpr", "intellectual property", "ip ",
        "patent", "license terms", "ownership of",
    ),
    "sustainment-training-support": (
        "training", "onboard", "help desk", "cdrl", "sustainment", "operator train",
        "user support", "pm reporting", "status report",
    ),
    "platform-integration-embedded": (
        "integrat", "embed", "plugin", "program of record", "existing system", "c2 system",
        "advana", "maven", "genai.mil", "chatdia", "module",
    ),
    "staff-product-generation": (
        "annex", "collection plan", "course of action", "coa", "bda", "battle damage",
        "decision brief", "staff product", "overlay", "mcoo", "target folder", "orders production",
        "situational template", "event template", "doctrinal template", "planning cycle",
        "mdmp", "brevity",
    ),
    "wargame-simulation-personas": (
        "wargam", "war game", "simulat", "persona", "red/blue", "red team force", "blue force",
        "adversary representation", "scenario", "injection", "role-play", "agent-based",
    ),
    "robotic-autonomy-control": (
        "motion planning", "path planning", "slam", "navigat", "rigging", "manipulat",
        "robotic", "actuat", "platform control", "autonomous vehicle",
    ),
}


def load_valid_themes(themes_file: Path | None = None) -> list[str]:
    """Parse theme IDs from the vocabulary table. Fails closed — a missing file is fatal."""
    path = themes_file or THEMES_FILE
    if not path.exists():
        raise FileNotFoundError(f"missing capability theme vocabulary: {path}")
    themes = [
        m.group(1)
        for m in (re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|", line)
                  for line in path.read_text(encoding="utf-8", errors="replace").splitlines())
        if m
    ]
    if not themes:
        raise ValueError(f"no themes parsed from {path.name}")
    return themes


_ALIAS_CACHE: dict[str, str] | None = None


def load_customer_aliases(path: Path | None = None, refresh: bool = False) -> dict[str, str]:
    """Parse reference/customer-aliases.tsv into {raw_lowercased: canonical}.

    A missing file is NOT fatal — every name simply passes through unchanged. This is the
    opposite of the capability-theme vocabulary, which fails closed: an unknown theme
    corrupts the ranking silently, whereas an unmapped customer name is merely un-merged
    and visible as itself.
    """
    global _ALIAS_CACHE
    if _ALIAS_CACHE is not None and not refresh and path is None:
        return _ALIAS_CACHE
    src = path or ALIASES_FILE
    aliases: dict[str, str] = {}
    if src.exists():
        for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            raw, canonical = parts[0].strip(), parts[1].strip()
            if raw and canonical:
                aliases[raw.lower()] = canonical
    if path is None:
        _ALIAS_CACHE = aliases
    return aliases


def canonical_customer(name: str, aliases: dict[str, str] | None = None) -> str:
    """Map a raw customer string to its canonical name for counting purposes.

    Chases one level of indirection so an alias may point at another alias without the file
    needing to be topologically sorted, but stops rather than looping on a cycle.
    """
    if not name:
        return name
    aliases = load_customer_aliases() if aliases is None else aliases
    seen: set[str] = set()
    current = name.strip()
    while True:
        key = current.lower()
        if key in seen:
            return current
        seen.add(key)
        nxt = aliases.get(key)
        if nxt is None or nxt.strip().lower() == key:
            return current
        current = nxt.strip()


def suggest_theme(text: str, valid: list[str]) -> tuple[str | None, int]:
    """Best keyword match for a block of text, or (None, hits) when it cannot decide."""
    lowered = text.lower()
    scores: dict[str, int] = {}
    for theme, keywords in THEME_KEYWORDS.items():
        if theme not in valid:
            continue
        hits = sum(1 for kw in keywords if kw in lowered)
        if hits:
            scores[theme] = hits
    if not scores:
        return None, 0
    best_score = max(scores.values())
    top = [t for t, s in scores.items() if s == best_score]
    if len(top) > 1:
        # A tie is a classification the keywords cannot make; a human decides.
        return None, best_score
    return top[0], best_score


# ---------------------------------------------------------------------------
# Evidence ledger crossing
# ---------------------------------------------------------------------------

PROOF_RANK = {"highest": 3, "high": 2, "medium": 1, "low": 0}

# Which ledger tags count as evidence for which theme. Curated against the ledger's actual
# tag vocabulary and matched EXACTLY.
#
# The obvious approach — reuse THEME_KEYWORDS against the ledger's prose — was tried and
# abandoned: generic keywords ("gpu", "verif", "integrat") matched 60 of 81 items, every theme
# read as fully proven, and the exposure ranking collapsed to zero. Loose matching does not
# produce a slightly noisy answer here; it produces a confidently wrong one that hides exactly
# the themes we cannot substantiate. Empty tuples are meaningful: they say the ledger holds
# nothing for that theme.
EVIDENCE_TAGS: dict[str, tuple[str, ...]] = {
    "air-gap-ddil-deployment": (
        "air-gapped", "ddil", "disconnected", "offline", "zero-connectivity",
        "no-cloud-dependency", "on-device", "on-prem", "fly-away", "edge", "in-enclave", "no-egress",
    ),
    "model-serving-api-interop": (
        "openai-compatible", "api", "local-endpoint", "interoperability", "drop-in", "connectors",
    ),
    "multi-model-hosting-byom": (
        "model-tiers", "light-medium-heavy", "frontier-parity", "frontier-model",
        "silicon-agnostic", "separable",
    ),
    "tevv-eval-harness": (
        "tevv", "benchmark", "mil-bench-5k", "mil-deflect", "military-test-sets", "test-harness",
        "test-evidence", "conformance-testing", "measurement", "measured", "scorecards", "rubric",
        "statistical-significance", "validation", "model-quality", "peer-review", "reproducibility",
    ),
    "output-verification-attribution": (
        "ground-truth", "wbom", "icd-203", "icd-206", "attribution", "claim-level", "auditable",
        "verification", "verification-evidence", "receipts", "tamper-evident", "signed-manifest",
        "no-model-in-loop", "determinism", "deterministic", "doctrine-ledger", "untrusted-oracle",
    ),
    "agentic-orchestration": (
        "agentic", "agents", "orchestration", "roles-as-agents", "agentic-orchestration", "governed-workflow",
    ),
    "mission-mos-finetuning": (
        "fine-tuning", "lora", "adapters", "mos-adapters", "domain-specific", "custom-model",
        "model-specialization", "mission-adaptation", "combat-arms", "combat-medic",
    ),
    "non-refusal-behavior": ("refusal", "answer-rate", "military-queries", "mil-deflect"),
    "multimodal-imagery-fmv": (
        "computer-vision", "machine-vision", "target-id", "drone-detection", "multi-object-tracking",
        "yolo", "infrared", "night-vision", "c-uas", "counter-uas",
    ),
    "multimodal-audio": (),
    "data-labeling-curation": (
        "data-labeling", "labeling", "dataset", "notional-data", "seeded-not-trained",
        "human-in-the-loop", "pipelines", "generated-artifacts",
    ),
    "ato-accreditation-artifacts": (
        "ato", "ato-integration", "accreditation", "accredited-environment", "iatt", "il5", "il6",
        "rmf", "cui", "capco", "certification", "security-architecture", "government-environment",
        "azure-ilz", "classification-marking", "portion-marking", "ts-sci", "secret",
    ),
    "hardware-footprint-compression": (
        "compression", "quantization", "commodity-hardware", "hardware-fit", "gpu", "cpu", "vram",
        "silicon", "form-factor", "ruggedized", "toughbook", "tablets", "throughput",
        "edge-infrastructure", "multi-platform",
    ),
    "utilization-telemetry-metrics": ("metrics", "power-bi", "operator-ui"),
    "cross-domain-model-update": (
        "upgrades", "edge-sync", "30-day-delivery", "rapid-fielding", "versioned", "adaptation-cycle",
    ),
    "federation-cross-enclave": (
        "cross-domain", "coalition", "mission-partner-environment", "foreign-disclosure",
        "distributed", "converged", "spillage", "leakage-prevention",
    ),
    "retrieval-over-doctrine": (
        "rag", "retrieval-scoping", "mdmp", "embedding-space", "intel-production",
    ),
    "multilingual-translation": ("multilingual", "translation", "language", "language-id", "low-resource"),
    "token-cost-economics": (
        "cost", "no-per-token", "zero-marginal", "delivery-economics", "licensing", "firm-fixed-price",
    ),
    "training-data-rights": ("data-return", "built-to-spec", "licensing"),
    "sustainment-training-support": (
        "onboarding", "maintenance", "operator", "configuration-management", "work-ready", "logistician",
    ),
    "platform-integration-embedded": (
        "integration", "integrators", "advana", "maven", "tak", "cjadc2", "ngc2",
        "c2-modernization", "webapp", "oem", "hardware-partner", "defense-prime",
    ),
    "staff-product-generation": (
        "coa", "mdmp", "intel-production", "generated-artifacts", "sop-as-software", "tradecraft", "toc",
    ),
    "wargame-simulation-personas": ("roles-as-agents", "jrtc"),
    "robotic-autonomy-control": (),
}


def load_ledger(ledger_file: Path | None = None) -> list[dict]:
    """Approved, non-retired ledger items only. Restricted and retired items cannot carry a
    claim in a proposal, so they cannot count as proof here either."""
    path = ledger_file or LEDGER_FILE
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return []
    items = data.get("items", []) if isinstance(data, dict) else data
    return [i for i in items if isinstance(i, dict) and i.get("approval_status") == "approved"]


def evidence_by_theme(ledger: list[dict], valid: list[str]) -> dict[str, list[dict]]:
    """Map ledger items onto themes by exact tag match.

    An item can support several themes — a Space Force IL5 deployment is evidence for both
    accreditation and air-gapped deployment — so this is deliberately not a partition.
    """
    out: dict[str, list[dict]] = {t: [] for t in valid}
    for item in ledger:
        # Re-check approval here, not only in load_ledger(): a caller passing items directly
        # would otherwise let a retired or restricted item stand as proof, which is the exact
        # failure the ledger's approval field exists to prevent.
        if item.get("approval_status") != "approved":
            continue
        item_tags = {
            str(t).strip().lower()
            for t in (item.get("relevance_tags") or []) + (item.get("tags") or [])
        }
        for theme in valid:
            if item_tags & set(EVIDENCE_TAGS.get(theme, ())):
                out[theme].append(item)
    return out


def untagged_themes(valid: list[str]) -> list[str]:
    """Themes with no evidence-tag mapping at all. These read as 'no proof' by construction,
    which is right when the ledger genuinely holds nothing and wrong if the mapping was simply
    never written — so the brief states them explicitly rather than letting them rank silently."""
    return [t for t in valid if not EVIDENCE_TAGS.get(t)]


def proof_level(items: list[dict]) -> str:
    """How well the ledger can substantiate a theme: 'strong', 'weak', or 'none'.

    Depth matters as much as strength. A single high-strength item is one anecdote — enough to
    answer one evaluator's question, not enough to call a theme proven across five customers'
    varied asks. 'strong' therefore needs three or more corroborating items, at least one of
    them high or better.
    """
    if not items:
        return "none"
    best = max((PROOF_RANK.get(i.get("proof_strength") or "low", 0) for i in items), default=0)
    if len(items) >= 3 and best >= 2:
        return "strong"
    return "weak"


# ---------------------------------------------------------------------------
# Exposure
# ---------------------------------------------------------------------------
# Exposure answers one question: where would we most regret the current state?
#
#   demand   how many distinct customers asked, and how many of those asks were scored
#   proof    what the evidence ledger can substantiate for that theme
#   hedges   how many times a bid actually paid for the shortfall
#
# The score is intentionally simple arithmetic on visible columns. A weighting nobody can
# reproduce by eye gets argued with instead of acted on.

PROOF_DEFICIT = {"none": 1.0, "weak": 0.5, "strong": 0.0}


def classify_signal(signal: dict, theme_proof: str) -> str:
    """Which decision class a signal belongs to. The three are owned differently.

    hard-gap        we told the customer no, and the ledger has nothing for the theme.
                    Build-or-team decision, engineering owns it.
    unproven-claim  we said yes and the ledger cannot back it. Claim risk: engineering owns
                    whether it is real, BD owns how it is worded.
    enablement      BD recorded a gap in a theme the ledger evidences well. Probably a
                    communication problem rather than an engineering one — routing these to
                    engineering wastes their time, which is how demand reviews lose their
                    audience. Theme-level inference, so it needs a human to confirm against
                    the specific ask.
    proven          asked, answered, provable. No action.
    unclassified    status was never resolved (backfill artifact). Not an action item.
    """
    status = signal["our_status"]
    if status in OPEN_STATUSES:
        return "enablement" if theme_proof == "strong" else "hard-gap"
    if status in CLAIMING_STATUSES and theme_proof == "none":
        return "unproven-claim"
    if status == "unknown":
        return "unclassified"
    return "proven"


def compute_exposure(signals: list[dict], valid: list[str],
                     ledger: list[dict] | None = None) -> list[dict]:
    """Per-theme exposure rows, highest exposure first."""
    ledger = ledger if ledger is not None else load_ledger()
    ev = evidence_by_theme(ledger, valid)

    aliases = load_customer_aliases()
    themes: dict[str, dict] = {}
    for sig in signals:
        theme = sig["capability_theme"]
        row = themes.setdefault(theme, {
            "theme": theme, "signals": 0, "customers": set(), "mandatory": 0,
            "open": 0, "hedges": 0, "verbal": 0, "rubric_pts": 0.0,
            "classes": {}, "examples": [],
        })
        row["signals"] += 1
        # Count the CANONICAL name: customer breadth is the primary ranking dimension, so
        # two spellings of one organization would silently double its apparent reach.
        row["customers"].add(canonical_customer(sig["customer"], aliases))
        if sig["demand_strength"].startswith("mandatory"):
            row["mandatory"] += 1
        if sig["our_status"] in OPEN_STATUSES:
            row["open"] += 1
        if sig.get("bid_impact"):
            row["hedges"] += 1
            row["examples"].append(sig)
        row["rubric_pts"] += float(sig.get("rubric_weight_pct") or 0)

    rows = []
    for theme, row in themes.items():
        items = ev.get(theme, [])
        proof = proof_level(items)
        classes: dict[str, int] = {}
        for sig in signals:
            if sig["capability_theme"] != theme:
                continue
            classes[classify_signal(sig, proof)] = classes.get(classify_signal(sig, proof), 0) + 1
        breadth = len(row["customers"])
        mandatory_share = row["mandatory"] / row["signals"] if row["signals"] else 0.0
        score = breadth * (1 + mandatory_share) * PROOF_DEFICIT[proof] + 2 * row["hedges"]
        rows.append({
            **row,
            "customers": sorted(row["customers"]),
            "customer_count": breadth,
            "mandatory_share": round(mandatory_share, 2),
            "proof": proof,
            "evidence_ids": [i["id"] for i in items][:4],
            "evidence_count": len(items),
            "classes": classes,
            "exposure": round(score, 1),
        })
    rows.sort(key=lambda r: (-r["exposure"], -r["customer_count"], r["theme"]))
    return rows


# ── Submission mechanics ─────────────────────────────────────────────────────
# Lines describing HOW TO RESPOND rather than what the customer needs. Shared so
# the matrix extractor and the capture-pipeline ingest cannot drift apart about
# what belongs in the register.
#
# TWO TOKENS ARE CONTEXT-SENSITIVE AND WERE OVER-MATCHING. Found 2026-08-02 by
# cross-checking against the capture pipeline's export:
#
#   `address` — intended as the proposal-metadata field (mailing address), but
#     it is also the commonest verb in requirement prose. It alone dropped 16 of
#     38 rows, including "Address operability within A2/AD-constrained
#     environments" and "Proposals must address specific Spiral-level
#     requirements" — both real technical requirements.
#   `signature` — intended as a signature block. In defense it is at least as
#     often a technical term (radar, acoustic, RF signature).
#
# Both now require the metadata sense. A rule that silently eats a real
# requirement is worse than one that lets a mechanics row through: the row is
# visible and can be dropped at confirmation, the missing requirement is not.
MECHANICAL_PATTERNS = re.compile(
    r"\b(cover page|cover sheet|page limit|page count|word (count|limit)|font|margin|"
    r"file nam|pdf|docx|upload|portal|email submission|format compliance|"
    r"point of contact|poc\b|cage\b|uei\b|naics|company name|"
    r"(?:mailing|company|business|street|e-?mail)\s+address|address\s*:|"
    r"table of contents|classification marking|distribution statement|"
    r"signature block|signature page|authori[sz]ed signature|"
    r"due date|deadline|submission instructions?)\b",
    re.IGNORECASE,
)


def is_mechanics(text: str) -> bool:
    """Whether a line describes how to respond rather than what is needed."""
    return bool(MECHANICAL_PATTERNS.search(text or ""))
