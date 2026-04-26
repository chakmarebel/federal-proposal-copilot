# Graphics Brief

One figure for a 10-page CSO Solution Brief. Graphics discipline: each must *prove* something the evaluator will score.

---

## Figure 1 — System Architecture

### Graphic objective
Show that on-device inference is the architectural foundation, not a retrofit — connecting directly to AoI-1 (on-device) and AoI-2 (disconnected operation).

### Figure title
Three-Tier Architecture — Edge, Garrison, Enterprise

### One-paragraph explanation
Three horizontal bands: **Edge** (ruggedized edge device, tactical network, on-device inference), **Garrison** (optional tactical ops center, local model updates), **Enterprise** (optional cloud, model training and adapter build). Arrows show that inference flows entirely at the Edge tier; Garrison and Enterprise connections are shown as dashed lines to emphasize they are *optional* for operation.

### ASCII wireframe

```
┌──────────────────────────────────────────────────────────────────┐
│ ENTERPRISE (OPTIONAL — MODEL BUILD ONLY)                          │
│  [Training cluster] ─ build adapters ─ [Model registry]           │
└────────────┬──────────── (dashed, optional) ─────────────────────┘
             │
┌────────────┴──────────────────────────────────────────────────────┐
│ GARRISON (OPTIONAL — ADAPTER DISTRIBUTION)                        │
│  [TOC node] ─ syncs adapters when available                       │
└────────────┬──────────── (dashed, optional) ─────────────────────┘
             │
┌────────────┴──────────────────────────────────────────────────────┐
│ EDGE (MISSION-CRITICAL — OPERATES DISCONNECTED)                   │
│  [Ruggedized device] ◄─► [On-device inference] ◄─► [Operator UI]  │
│   • 14-month demonstrated disconnected operation                  │
└───────────────────────────────────────────────────────────────────┘
```

### Component list
- Edge device (NUC-class or ruggedized laptop)
- On-device inference engine (shown as green box — always-on, always-local)
- Operator UI
- Garrison TOC node (shown as blue, dashed outline — optional)
- Enterprise training cluster (shown as gray, dashed outline — optional)
- Model registry (Enterprise tier)

### Layout instructions
- Three horizontal bands, Edge at bottom (emphasizes criticality)
- Green = Edge / always operational
- Blue = Garrison / optional
- Gray = Enterprise / optional
- Dashed lines between tiers convey optionality
- Callout on Edge band: "14-month demonstrated disconnected operation"

### Color / grouping logic
Per Acme brand palette: Edge tier uses `#2F9E44` (signal green), Garrison uses `#2D5F9E` (navy), Enterprise uses `#6C757D` (slate). Tier labels in 28pt, body in 17pt minimum per half-page-print standard.

### Action caption (goes in the Word doc, NOT embedded in HTML)

*Figure 1. Three-tier architecture — mission-critical operations run disconnected at the Edge.* All inference (generation, summarization, Q&A) executes on the Edge device without enterprise connectivity; Garrison and Enterprise tiers are shown as optional because they carry only model updates, not mission traffic. Demonstrated in a 14-month deployment at [redacted DoD customer] operating zero-connectivity.

### What this graphic proves
The architecture is disconnected-by-design, not cloud-retrofit. This directly supports AoI-1 (on-device inference) and AoI-2 (disconnected operation ≥14 days) — and implicitly ghosts the cloud-retrofit competitor pattern.
