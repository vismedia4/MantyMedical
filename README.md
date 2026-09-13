# Valet Retrieval Platform

> ## 🔒 INTERNAL — VisMedAI Advisory
>
> This documentation set is **internal working material**. It contains effort estimates,
> day-rate-revealing figures, commercial positioning, and analysis of the client written
> for our own use. **None of it goes to Pioneer Parking** unless a specific piece is
> deliberately prepared for that purpose.
>
> `docs/source/` holds the **confidential** 10 September Build Brief, including an
> appendix on commercial matters unrelated to this engagement. **Do not place this
> directory in any repository the client can read.**
>
> The only client-facing deliverable produced from this material is the Tuesday review
> page, which is written separately and carries none of the above.

A multi-property valet request and retrieval system, built for **Pioneer Parking** and
architected from day one for **licensing to other parking operators**. Prototyped as
*Pioneer Connect — Smart Valet Retrieval*; the product name is provisional.

This repository holds the **design and development specification**. No application code yet.

## Start here

[**`docs/README.md`**](docs/README.md) — the documentation index.

Fastest path in, depending on what you need:

| You are | Read |
|---|---|
| New to the product | [01 — Product Overview](docs/01-product-overview.md) |
| Building the backend | [03 — Domain Model](docs/03-domain-model.md) → [04 — Workflows](docs/04-workflows-and-state.md) → [11 — API Contract](docs/11-api-contract.md) |
| Building the frontend | [05 — Information Architecture](docs/05-information-architecture.md) → [06–09 — Screen Specs](docs/06-screens-customer.md) → [10 — Design System](docs/10-design-system.md) |
| Planning the work | [15 — Delivery Plan](docs/15-delivery-plan.md) → [14 — Open Questions](docs/14-open-questions.md) |
| The product owner | [00 — Client Requirements](docs/00-client-requirements.md), then [14 — Open Questions](docs/14-open-questions.md) — five decisions block sprint 1 |
| Working on the website | [16 — Website Refresh](docs/16-website-refresh.md) |

## Sources, in priority order

1. **Client requirements session, September 10, 2026** — Jonathan Cohen (Pioneer Parking)
   with VisMedAI Advisory. Archived at [`docs/source/`](docs/source/). **This is the
   authority.**
2. **22 prototype screenshots**, checked in under [`docs/screens/`](docs/screens/) as
   reference art. Colour values in the design system were sampled from the original
   pixels and are exact.

Where the two disagree, the brief wins.
[`docs/00-client-requirements.md`](docs/00-client-requirements.md) records every such
correction.

Every claim is marked *(observed)*, *(inferred)*, or *(proposed)* so the team can tell
requirements from recommendations.

## Scope in one line

Approved recurring monthly parkers only. No billing, no guests or transient parkers, no
broadcast messaging, no SMS, no photo uploads — each a client-stated boundary. Transient
ticketing is [workstream 3](docs/17-roadmap-beyond-mvp.md), deliberately deferred.
