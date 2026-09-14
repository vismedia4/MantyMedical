# Pioneer Connect — Design & Development Documentation

> ## 🔒 INTERNAL — VisualMedia, Ltd.
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

**Product:** Valet retrieval platform — prototyped as *Pioneer Connect · Smart Valet Retrieval*
**Client:** Pioneer Parking (multi-property: garages + residential buildings)
**Note on the name:** the product is designed for **licensing to other parking
operators**, so "Pioneer Connect" is provisional and branding lives in a theme layer.
See [00 §6.3](00-client-requirements.md).

---

## What this is

This documentation set reverse-engineers the Pioneer Connect prototype into an
implementation-ready specification: roles, domain model, state machines, screen
specs, design tokens, and a proposed API contract.

It is written for an engineering team that has **not** seen the prototype and needs
to build the production system from these documents alone.

## Two sources, in priority order

| Priority | Source | Status |
|---|---|---|
| **1** | **Client requirements session, September 10, 2026** — Jonathan Cohen with VisualMedia, Ltd. Archived: [`source/`](source/) | **Authority.** Where it disagrees with the prototype, it wins |
| 2 | 22 full-page prototype screenshots, all four roles. Checked in under [`screens/`](screens/) | Reference art. Superseded where the brief says otherwise |

[00 — Client Requirements](00-client-requirements.md) records exactly what the brief
**changed**, **resolved** and **added** relative to the prototype. Read it first if you
have seen an earlier version of these documents.

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
| **00** | **[Client Requirements & Decision Log](00-client-requirements.md)** | **The authority.** What the client asked for; what changed against the prototype |
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
| 15 | [Delivery Plan](15-delivery-plan.md) | Phased scope, milestones, sizing, risk register |
| **18** | **[Cost & Effort Model](18-cost-model.md)** | **Effort, benchmark and pricing for the Sept 15 decision** |
| **19** | **[Pilot & Full MVP Scope](19-pilot-and-mvp-scope.md)** | **What each purchase includes, excludes, and when it lands** |
| 16 | [Website](16-website-refresh.md) | ⚠ **Parked — out of scope.** Tracked separately in `pioneer-website` |
| 17 | [Roadmap Beyond MVP](17-roadmap-beyond-mvp.md) | Workstream 3 — transient ticketing, deferred items |

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

Browser chrome has been cropped; images are downscaled to 1400px wide. Colors quoted in
[10 — Design System](10-design-system.md) were sampled from the uncropped originals and
are exact.

> **The screenshots are not fully current.** Three things visible in them are corrected
> by the brief: the `Add photo` control (no uploads — generic images instead), the phone
> number in the valet request-detail modal (barred at the valet role), and the "~7 days"
> retention copy (2–3 days for the valet view; permanent in the backend). Each screen doc
> flags the delta inline.

## The one-paragraph summary

An approved monthly parker opens the app, taps **Request Now**, and watches a three-step
progress bar. A valet at a tablet in the garage sees the request land in an *Incoming*
column with a chime that will not stop until someone accepts it, retrieves the car, and
taps *Ready* — which sends the customer the one push notification the product exists to
deliver. A garage manager, working remotely, approves new customers and vehicle changes
for their location and can override any request status; if they go quiet, approvals
escalate to the office rather than stalling. An office admin runs the portfolio —
locations, staff accounts, six-digit enrollment codes, and system-wide policy.

## The three decisions that shape everything

1. **Reliability is the acceptance criterion.** Pioneer is leaving ElimaWait (~$165/mo)
   because it is unreliable. A feature-complete app that drops a request has failed.
2. **Multi-tenant from day one.** The product is to be licensed to other parking
   operators. Tenant isolation is cheap now and expensive later; white-label theming is
   deferred.
3. **The MVP is deliberately narrow.** Approved recurring monthly parkers only. No
   billing, no guests, no transient parkers, no broadcast messaging, no SMS, no photo
   uploads. Every one of those is a client-stated boundary.

## Next decision point

**Tuesday, September 15, 12:00 noon** — VisualMedia presents MVP scope, timeline and cost for
the **platform**. [19 — Pilot & Full MVP Scope](19-pilot-and-mvp-scope.md) is the
client-facing answer; [18 — Cost & Effort Model](18-cost-model.md) and
[15 — Delivery Plan](15-delivery-plan.md) are the internal working behind it;
[14 — Open Questions](14-open-questions.md) Q1 and Q2 must be closed in the session.

The website is a separate concern and is not covered here.
