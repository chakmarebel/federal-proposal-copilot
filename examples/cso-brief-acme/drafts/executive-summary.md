# Executive Summary

<!-- INTERNAL TRAINING NOTE: Pattern annotations removed for production use -->

---

**On-device inference is not a product feature — it is the architectural foundation of Acme AI, validated by 14 months of disconnected operation at a DoD customer at the scale JED requires.**

The Joint Expeditionary Directorate operates in DDIL environments where commercial AI tooling fails not because it is poorly designed, but because it was never designed to operate without a cloud to call home. Solutions that require persistent cloud connectivity — even intermittently, even for "telemetry" or "updates" — cannot support the operational tempo of forward-deployed units. Acme AI's platform was built disconnected-first: every mission-critical capability, from generation to adapter loading, executes entirely on the edge device.

**We offer JED four specific capabilities mapped to your Areas of Interest:**

1. **Proven DDIL deployment.** Our platform has operated at [redacted DoD customer] for 14 months in fully disconnected mode, supporting 18 operators across 4 forward locations with zero cloud dependency (AoI-1, AoI-2).

2. **On-device adapter specialization in 60 days.** Our LoRA adapter pipeline delivered four specialized adapter sets for prior customer mission sets within 60 days of tasking, measured from adapter spec to operational deployment (AoI-3). Detail in Technical Approach §4.

3. **90-day path to IOC on hardware JED already fields.** Our platform runs on ruggedized NUC-class devices currently in JED's tactical hardware inventory. First operational capability at 10 endpoints is achievable within 90 days of Phase 2 award, with no new hardware acquisition required.

4. **IL5 roadmap with FedRAMP Moderate in hand.** Acme AI's FedRAMP Moderate ATO is in final stages; IL5 assessment roadmap is defined with a target completion of 18 months (AoI-4). This is a credible path, not a paper claim.

Acme AI is a commercial company. Our platform generates $4M ARR across non-government customers in regulated commercial sectors (financial services, healthcare). JED would be acquiring a proven commercial capability under FAR 2.101, not funding a research project.

See **Figure 1 (Three-tier architecture)** — Edge operations execute entirely disconnected; Garrison and Enterprise tiers carry only optional model updates.

**What Acme AI commits to at Phase 1 selection:**
- Submit a full Phase 2 proposal within 30 days of invitation
- ROM range for Phase 2 engagement: $2.1M-$3.4M for initial 10-endpoint deployment with one adapter set (detail in ROM section)
- Named technical lead (Dr. [PI] — PI on three DARPA programs in adjacent topics) committed through Phase 2 delivery

We are ready to begin.
