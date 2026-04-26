# Rough Order of Magnitude — Phase 2 Deployment

**To:** Joint Expeditionary Directorate, Office of Emerging Capabilities
**From:** Acme AI
**Date:** 2026-04-22
**Validity:** This ROM is valid for 60 days from the date above.

## Scope

Acme AI will deliver an initial operational capability on **10 ruggedized edge endpoints** for a single JED operational unit, with one mission-specialized adapter set, supporting 18-24 operators. Scope includes platform deployment, one adapter fine-tuning cycle, operator training, and 6 months of sustainment. Excludes any hardware procurement (JED-furnished ruggedized edge devices) and any classified network engineering.

## Estimated Investment

**$2.1M – $3.4M** over **9-12 months** (Phase 2 engagement)
*(range ±25%, based on expert judgment decomposition of prior comparable engagements)*

## Basis of Estimate

Method: **Expert judgment with analogous anchoring.** Derived by decomposing the engagement into five workstreams and anchoring each to the cost of comparable Acme AI commercial and government deployments in 2024-2025. Range width reflects uncertainty in adapter complexity and integration scope, which Phase 2 will refine.

## Key Cost Drivers

1. **Adapter fine-tuning cycle.** One mission-specialized adapter set (approx 60-day pipeline). Complexity of the mission set drives ±$300K swing.
2. **Deployment engineering on 10 endpoints.** Integration with JED tactical network and existing operator workflows. Geographic concentration of endpoints drives ±$200K swing.
3. **Operator training.** 18-24 operators across forward locations. Travel and on-site training load drive ±$150K swing.
4. **Sustainment period.** 6 months of incident response, model refresh, and minor adapter tuning. Longer period shifts toward upper bound.
5. **IL5 gap work (if required during Phase 2).** If JED requires IL5 earlier than our roadmap, accelerating adds $400K-$600K to the upper bound.

## Key Assumptions

These assumptions materially affect the range. If any are false, this ROM must be revisited before Phase 2 proposal.

1. **Hardware is JED-furnished.** 10 ruggedized NUC-class or Dell Latitude Rugged devices provided by JED. If Acme AI must procure hardware, add $150K-$250K.
2. **Single adapter set.** One mission specialization in Phase 2. Each additional adapter set: $300K-$500K.
3. **Existing FedRAMP Moderate posture is sufficient for Phase 2 operations.** If IL5 is required during Phase 2 execution (not as a follow-on), add $400K-$600K.
4. **Tactical network is accessible for integration testing.** If classified network engineering is required, scope expands materially.
5. **No classified algorithm work.** This Phase 2 scope is commercial-item deployment, not classified model development.

## Risks to the Estimate

- **Scope creep from added adapters.** A common path — JED sees value in one adapter and wants three. Each adds $300-500K.
- **Integration with legacy tactical systems.** Scope-dependent; we assume modern endpoint deployment, not integration with 15-year-old BMS/C2 systems.
- **IL5 compression.** JED may require IL5 sooner than our roadmap. This is the single largest upside risk to cost.

## Next Steps

To firm this ROM into a Phase 2 proposal, we will need:

1. Confirmed hardware plan (JED-furnished vs. Acme-procured)
2. Target mission set for the Phase 2 adapter (driver of fine-tuning scope)
3. IL5 timing requirement (before vs. after Phase 2 deployment)
4. Number of forward locations and operator count to size training load
