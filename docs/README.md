# Pioneer Connect — Design & Development Documentation

**Product:** Pioneer Connect — *Smart Valet Retrieval*
**Operator:** Pioneer Parking (multi-property: parking garages + residential buildings)
**Status of source material:** Interactive click-through prototype, banner-marked `PROTOTYPE — NOT PRODUCTION`

---

## What this is

This documentation set reverse-engineers the Pioneer Connect prototype into an
implementation-ready specification: roles, domain model, state machines, screen
specs, design tokens, and a proposed API contract.

It is written for an engineering team that has **not** seen the prototype and needs
to build the production system from these documents alone.

## How this was produced

Source of record was a set of 22 full-page screenshots of the prototype covering all
four roles. Every factual claim below traces to a pixel in those screenshots, which
are checked in under [`screens/`](screens/) as normative reference art.

**Read this convention before using the docs:**

| Marker | Meaning |
|---|---|
| *(observed)* | Directly visible in the prototype. Treat as a requirement. |
| *(inferred)* | Not visible, but strongly implied by observed behavior. Treat as a strong default — cheap to change. |
| *(proposed)* | Our engineering recommendation. No prototype basis. Debate freely. |

Anything not marked is observed. Unresolved items are collected in
[14 — Open Questions](14-open-questions.md); that document is the one to work through
with the product owner before sprint 1.

## Document index

| # | Document | Read it for |
|---|---|---|
| 01 | [Product Overview](01-product-overview.md) | What the product is, who it serves, the core loop |
| 02 | [Roles & Permissions](02-roles-and-permissions.md) | The four roles, RBAC matrix, tenancy scoping |
| 03 | [Domain Model](03-domain-model.md) | Entities, fields, relationships, ERD |
| 04 | [Workflows & State Machines](04-workflows-and-state.md) | Request lifecycle, approvals, onboarding |
| 05 | [Information Architecture](05-information-architecture.md) | Route map, navigation, form factors |
| 06 | [Screens — Customer](06-screens-customer.md) | Mobile app screen specs |
| 07 | [Screens — Valet](07-screens-valet.md) | Tablet queue-board specs |
| 08 | [Screens — Garage Manager](08-screens-manager.md) | Location console specs |
| 09 | [Screens — Office Admin](09-screens-admin.md) | Cross-location admin specs |
| 10 | [Design System](10-design-system.md) | Tokens, type, components, states — ships with [`design-tokens.css`](design-tokens.css) |
| 11 | [API Contract](11-api-contract.md) | Proposed REST surface + payloads |
| 12 | [Notifications & Real-Time](12-notifications-and-realtime.md) | The chime, live updates, push |
| 13 | [Non-Functional Requirements](13-nonfunctional-requirements.md) | Security, privacy, retention, a11y |
| 14 | [Open Questions](14-open-questions.md) | Decisions blocking or shaping the build |
| 15 | [Delivery Plan](15-delivery-plan.md) | Phased scope, milestones, sizing |

## Reference screenshots

```
screens/
  customer/   00-landing-qr · 01-sign-in · 02-home · 03-request-status
              04-schedule-pickup · 05-my-vehicles · 06-add-vehicle
  valet/      01-queue · 02-request-detail · 03-valet-menu
  manager/    01-dashboard · 02-pending-approvals · 03-customers-vehicles
              04-valet-account · 05-request-history · 06-settings
  admin/      01-console · 02-users · 03-locations-add · 04-locations-list
              05-activity-history · 06-settings-policies
```

Browser chrome has been cropped; images are downscaled to 1400px wide. Colors quoted
in [10 — Design System](10-design-system.md) were sampled from the uncropped originals
and are exact.

## The one-paragraph summary

A resident or tenant opens the app, taps to request their car, and watches a
three-step progress bar. A valet standing at a tablet in the garage sees the request
land in an *Incoming* column with a chime that will not stop until someone accepts
it, retrieves the car, and taps *Ready*. A garage manager approves new customers and
vehicle changes for their location and can override any request status. An office
admin runs the property portfolio — locations, staff accounts, six-digit enrollment
codes, and system-wide policy.
