---
artifact_id: cso-commercial
output_file: drafts/cso-pricing.md
companion_file: working/pricing-inputs.md
mental_model: Commercial-item pricing backed by market references — not a government cost buildup
must_not_produce:
  - FAR Part 15 cost volume
  - Fringe / overhead / G&A rate disclosures
  - CLIN structure with detailed labor categories
  - DCAA-style BOE narratives
  - Certified cost or pricing data (CSOs use commercial item determination, not cost/price analysis)
---

# CSO Commercial Pricing

## Mental model
The Contracting Officer is making a commercial-item determination under FAR 2.101 and negotiating a fair and reasonable price based on **market comparables**, not cost realism. They care about: is this price consistent with what non-government customers pay, and are the terms standard commercial terms?

If your pricing reads like a FAR cost volume, you're telling the CO you don't actually sell this commercially — which undermines the commercial-item claim.

## Required inputs (ask the user)

### Commercial-item basis
- How is this product / service sold commercially today?
- Named commercial customers (if disclosable)
- Standard commercial price list or SKU structure (if available)
- Any volume discounts, tiers, or negotiated enterprise pricing

### What's being priced
- Deliverable type: software license, SaaS subscription, professional services, hardware, or mix
- Units of measure: per-user, per-device, per-endpoint, per-instance, flat fee, hourly
- Duration: one-time, annual, multi-year

### Pricing model
- Fixed price, subscription, usage-based, or hybrid
- Term (1 year, 3 years, etc.)
- Payment schedule (annual up front, quarterly, milestone)

### Government-specific adjustments (if any)
- GSA Schedule pricing reference (if applicable)
- Most Favored Customer comparison
- Any government-specific security or compliance work being priced separately

## What NOT to ask
- Fringe / overhead / G&A rates
- Labor hour buildups
- Indirect rate certifications
- DCAA rate history

If these come up, ask: "This is a CSO — pricing should be market-based. Do you have a commercial price list or enterprise quote we can reference?"

## Calculation approach

**Market comparables first.** Anchor pricing to what non-government customers pay. If you have a standard commercial price list, start there. Adjust only for:

- Volume (enterprise / federal scale discount)
- Term length (multi-year discount)
- Government-specific add-ons (if separately priced)

If you have no commercial price list (rare for a CSO — it calls commercial-item status into question), document a **parametric commercial pricing model**: unit economics that a commercial buyer would recognize (e.g., $X/seat/month, $Y/inference-call, $Z/TB/month).

## Output structure (`drafts/cso-pricing.md`)

```markdown
# Pricing — [Solution Name] for [Customer]

**Vehicle:** CSO [reference]
**Commercial-item basis:** See Commercial Item Determination below.

## Pricing Summary

| Item | Unit | Qty | Unit Price | Period | Extended |
|---|---|---:|---:|---|---:|
| [SKU or service line] | [per-user / per-device / per-mo] | [N] | $[X] | [Year 1] | $[X] |
| [SKU] | ... | ... | $[X] | [Year 1] | $[X] |
| **Total Year 1** | | | | | **$[X]** |
| [SKU] | ... | ... | $[X] | [Year 2] | $[X] |
| **Total Year 2** | | | | | **$[X]** |
| ... | | | | | |
| **Total Contract Value** | | | | [N years] | **$[Total]** |

## Pricing Model
[1 paragraph: fixed / subscription / usage-based / hybrid. Payment schedule. Term length. Any included support.]

## Commercial Item Determination

This offering qualifies as a commercial item under FAR 2.101 based on the following:

- **Commercial sales history:** [Describe — customers, volume, revenue without disclosing proprietary detail]
- **Commercial price list:** [Reference — standard SKU pricing, enterprise tiers]
- **Standard commercial terms:** This offering is sold under the same terms and conditions to non-government customers, with the following government-specific modifications: [list or "none"]

## Price Reasonableness

Price is supported by [choose applicable basis]:
- Commercial catalog / price list: [reference]
- Prior sales to non-government customers at comparable or higher prices
- GSA Schedule [number] with approved pricing
- Most Favored Customer pricing analysis available upon request

Any volume or multi-year discount offered to the Government is identified above.

## Proposed Terms (negotiable)

| Term | Proposed | Notes |
|---|---|---|
| Payment | [Annual in advance / Quarterly / Monthly] | [Standard commercial] |
| Renewal | [Auto-renew / Opt-in] | [Standard commercial] |
| Warranty | [Period and scope] | [Standard commercial] |
| Support | [Tier — business hours / 24x7] | [Included / separately priced] |
| Data rights | [Commercial computer software — FAR 27.405-1] | |
| SLA | [e.g., 99.9% uptime] | [If cloud/SaaS] |

Government-specific modifications to commercial terms are limited to those necessary for federal compliance (e.g., FedRAMP, ATO support, CUI handling).

## Assumptions and Exclusions

[List. Examples:]
- Pricing assumes [N] endpoints / users / inferences per [period]
- Volume above [threshold] priced at [tier]
- Hardware not included unless separately stated
- On-site support not included; remote support during business hours
```

## `working/pricing-inputs.md` (companion)

```markdown
# CSO Pricing Inputs

## Commercial pricing references
- [Source — price list, prior contract, enterprise quote]
- [Source]

## Government adjustments applied
- [Volume discount: X%]
- [Multi-year discount: Y%]
- [Other]

## Margin / profitability (internal)
[Don't share externally. Enough to confirm the price is not below cost.]

## Competitive considerations
[What other commercial / CSO bidders might price this at. Informs negotiation stance.]
```

## Pitfalls
- **Cost buildup language** — "fringe rate of 28%" tells the CO this isn't actually commercial. Don't include.
- **No commercial sales history** — if truly none, the commercial-item claim is weak; consider whether this should be an OTA or FAR procurement instead.
- **GSA Schedule mismatch** — if you have a GSA Schedule, your CSO price must be ≤ your GSA price (Most Favored Customer rule). Verify.
- **Priced too precisely** — commercial pricing is typically round ($10/user/month, not $9.87). Precision signals cost buildup.
- **Forgetting the commercial-item justification** — the CO needs it to make the determination. Don't bury it.
