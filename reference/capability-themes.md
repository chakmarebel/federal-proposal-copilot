# Capability Themes — controlled vocabulary

**Version:** 3 · **Adopted:** 2026-08-06 · **Consumers:** `signals/demand-signals.jsonl`
(`capability_theme` field), `scripts/build-demand-signal-brief.py`, `/capture-demand-signals`

This is the join key of the BD ↔ CTO demand signal loop (see
[docs/BD-CTO-DEMAND-SIGNAL-SYNC.md](../docs/BD-CTO-DEMAND-SIGNAL-SYNC.md)). Without a fixed
vocabulary the register becomes several hundred unique strings and nobody reads it. With one, the
same twenty rows accumulate weight across the whole pipeline and the ranking becomes an argument.

**Two rules govern additions.** A theme must be something the CTO shop could plausibly own as a work
item — `air-gap-ddil-deployment` is ownable, `works-better` is not. And a theme must be
distinguishable from its neighbors by the "Not this" column below; if it is not, the signal belongs
in the existing theme.

**Adding a theme** is a deliberate edit to this file, with the version bumped and the date noted.
Version 2 added `staff-product-generation`, `wargame-simulation-personas`, and
`robotic-autonomy-control` during the 2026-07-31 backfill, when 40-odd asks across ITDX26, NATO
DIANA, the Digital Guardian SOW, and the unmanned ground recovery RFI fit no existing theme.
The scripts validate against this table and reject unknown themes, so a typo fails loudly rather
than silently splitting a theme in two.

Version 3 added `adversarial-ai-security`, `anomaly-detection-analytics`, and
`human-oversight-control`. All three surfaced the same way: the 2026-08-06 capture-pipeline ingest
adjudicated 454 candidates and could not place seven of them, so `promote-crm-candidates.py` **held**
them rather than forcing a fit — a DARPA TS//SAP program asking us to secure AI models and AI
hardware, CBP and Air Force JAG asking for risk detection over their own records, and two efforts
asking who keeps a hand on an autonomous system. Holding is the mechanism working: a forced theme
is silent and permanent, while a held ask sits in the run report until someone decides.

They enter thin, and unevenly so. `anomaly-detection-analytics` and `human-oversight-control` each
open with two customers; `adversarial-ai-security` opens with two asks from a **single** DARPA
pursuit. There is no minimum-customer bar for admission — `robotic-autonomy-control` was added at
version 2 on one customer and is now the register's top exposure item at six. The test is the one
stated above: could the CTO shop own it, and is it distinguishable in the "Not this" column. A
single-customer theme is a claim about a category, not evidence of a trend, and the brief already
says so by ranking on customer breadth.

## Themes

| Theme ID | Scope — the customer is asking for | Not this |
|---|---|---|
| `air-gap-ddil-deployment` | Running inference with no connectivity: air-gapped enclaves, disconnected/intermittent/limited-bandwidth operation, fly-away kits, forward deployment | Cross-enclave movement of models or data (`federation-cross-enclave`, `cross-domain-model-update`) |
| `model-serving-api-interop` | A standard, interoperable serving interface: OpenAI-compatible APIs, integration into a government-owned AI hosting platform, SDK and endpoint parity | Hosting many models behind that interface (`multi-model-hosting-byom`) |
| `multi-model-hosting-byom` | Hosting and switching among multiple models, bring-your-own-model, side-by-side output comparison, escaping single-vendor monoculture | The single tuned anchor model itself (`mission-mos-finetuning`) |
| `tevv-eval-harness` | Test, evaluation, verification and validation as a repeatable process: benchmarks, scorecards, red-teaming protocols, acceptance criteria the government can rerun | Per-answer verification of claims at runtime (`output-verification-attribution`) |
| `output-verification-attribution` | Trusting an individual answer: claim-level grounding against authoritative sources, citation and attribution, hallucination gating, portable receipts, ICD 203 alignment | Aggregate model quality measurement (`tevv-eval-harness`) |
| `agentic-orchestration` | Multi-step autonomous task execution, tool and system calls, agent-to-source connectors, workflow automation on top of a model | Retrieval alone (`retrieval-over-doctrine`) |
| `mission-mos-finetuning` | Making the model militarily competent: domain and MOS tuning, LoRA and adapter workflows, on-prem fine-tuning, doctrine calibration, mission adaptation speed | Curating the data that feeds it (`data-labeling-curation`) |
| `non-refusal-behavior` | Models that answer legitimate military questions instead of refusing: refusal-rate reduction, abliteration, safety tuning calibrated for defense use | General model accuracy or bias measurement (`tevv-eval-harness`) |
| `multimodal-imagery-fmv` | Imagery, video and FMV: object detection and classification, target identification, annotation, geospatial and sensor exploitation | Audio and speech (`multimodal-audio`) |
| `multimodal-audio` | Speech and audio: transcription, translation of speech, radio and comms audio processing, speaker analysis | Text translation (`multilingual-translation`) |
| `data-labeling-curation` | Building the training corpus: labeling and annotation pipelines, synthetic data, data cleaning, human-in-the-loop review, export into training formats | Tuning the model on it (`mission-mos-finetuning`) |
| `ato-accreditation-artifacts` | Getting authorized to operate: RMF and cATO artifacts, IL-level accreditation, STIG and control evidence, support through the customer's ATO process | Defending the AI system against attack rather than documenting controls for it (`adversarial-ai-security`) |
| `hardware-footprint-compression` | Fitting the target hardware: quantization and compression, SWaP-constrained devices, edge accelerators, on-device latency and memory budgets | Where it is deployed logically (`air-gap-ddil-deployment`) |
| `utilization-telemetry-metrics` | Visibility into use: adoption and utilization dashboards, query telemetry, transparent system-utilization metrics for the workforce, usage reporting to the PMO | Evaluating output quality (`tevv-eval-harness`) |
| `cross-domain-model-update` | Moving models and updates across a boundary: progressive model upgrades through a period of performance, sneakernet and one-way transfer, patching in a classified enclave | Running federated instances on both sides (`federation-cross-enclave`) |
| `federation-cross-enclave` | Multiple instances working as one: enclave-to-enclave federation, multi-classification deployment, coalition and partner-nation sharing, cross-domain query routing | One-time or periodic model movement (`cross-domain-model-update`) |
| `retrieval-over-doctrine` | Grounded answers over the customer's own corpus: RAG over doctrine, OPORDs, regulations and local documents; document ingestion; citation-backed retrieval | Verifying the resulting claims (`output-verification-attribution`) |
| `multilingual-translation` | Language coverage in text: translation, low-resource and partner-nation languages, transliteration, foreign-document exploitation | Speech (`multimodal-audio`) |
| `token-cost-economics` | The money and throughput argument: cost per token or per seat, licensing model, throughput and concurrency at a given price, avoiding per-query cloud metering | Hardware sizing (`hardware-footprint-compression`) |
| `training-data-rights` | Who owns what: government purpose rights, data rights on models trained with government data, IP allocation, commercial license terms on the harness | Security classification of the data (`ato-accreditation-artifacts`) |
| `sustainment-training-support` | Standing the capability up and keeping it running: operator training, onboarding, help desk, CDRLs and PM reporting, sustainment over the period of performance | Utilization measurement (`utilization-telemetry-metrics`) |
| `platform-integration-embedded` | Living inside something else: embedding into a customer or partner platform, integration with an existing C2 or intel system, plugin and module delivery into a program of record | A generic serving API (`model-serving-api-interop`) |
| `staff-product-generation` | Producing the military staff product itself: IPB annexes and templates, collection plans, COAs, BDA, targeting products, decision briefs, orders and planning-cycle outputs in doctrinal format | Answering questions from a corpus (`retrieval-over-doctrine`) |
| `wargame-simulation-personas` | Simulating the environment or the people in it: red/blue force representation, agent-based force models, persona and role-play engines, scenario generation, COA wargaming and injection handling | Generating the staff product that comes out of planning (`staff-product-generation`) |
| `robotic-autonomy-control` | Moving or manipulating something physical: motion planning, SLAM and navigation, manipulation and rigging, platform control | Perceiving from a platform's sensors (`multimodal-imagery-fmv`) · Who authorizes the movement (`human-oversight-control`) |
| `adversarial-ai-security` | Defending the AI system itself as an attack surface: model and weight protection, resistance to poisoning, evasion and prompt injection, AI supply-chain integrity, securing the hardware the model runs on | Documenting controls to get authorized (`ato-accreditation-artifacts`) · Building the corpus, even when poisoning resistance is one of its properties (`data-labeling-curation`) |
| `anomaly-detection-analytics` | Finding the signal in the customer's own operational records: anomaly, risk and fraud detection over transactions, logs and case data; predictive scoring; pattern-of-life over structured data | Detection in imagery or video (`multimodal-imagery-fmv`) · Answering questions from a document corpus (`retrieval-over-doctrine`) · Producing the doctrinal staff product that follows (`staff-product-generation`) |
| `human-oversight-control` | Keeping a human in command of an autonomous or AI-driven action: human-on-the-loop review and approval interfaces, bounded autonomy under a named authority, override and abort, compliance with DoD direction on human control of AI-enabled systems | Verifying that an individual answer is grounded (`output-verification-attribution`) · Controlling the platform itself (`robotic-autonomy-control`) |

## Themes deliberately excluded

Mechanical submission requirements (cover pages, page limits, formatting, POC blocks) are **not**
demand signals and must not be captured. They tell engineering nothing. The extractor drops rows
whose requirement text matches submission-formatting patterns; if one slips through, delete it rather
than inventing a theme for it.

Requirements that are purely about our corporate posture (small business status, facility clearance,
contract vehicle access) are likewise excluded. They are real constraints, but they belong to the
capture pipeline, not the CTO shop's backlog.
