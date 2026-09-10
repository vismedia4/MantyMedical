# 15 — Delivery Plan *(proposed)*

A sequencing recommendation, not a commitment. Sizes are relative (S/M/L), not
estimates — calibrate against your own team's velocity.

## Sequencing principle

Build **the core loop first, end to end, for one location**, and get it into a real
garage. Everything else — approvals, multi-location administration, policy
configuration — is scaffolding around a loop that either works in the field or does not.
A valet who will not use the tablet invalidates every other feature.

---

## Phase 0 — Foundations
*Goal: the team can build in parallel.*

| Work | Size |
|---|---|
| Decide Q1–Q5 in doc 14 (blocking questions) | — |
| Choose and procure the valet tablet | S |
| Repo, CI, environments, IaC skeleton | M |
| Auth: sign-in, sessions, RBAC middleware, location scoping | L |
| Data model + migrations (doc 03) | M |
| Design tokens + core components: button, card, pill, table, modal, toggle, photo tile | L |
| Seed data mirroring the prototype's five locations | S |

**Exit criteria:** a signed-in user of each role lands on an empty shell of the right
screen, and location scoping is proven by an authorization test suite.

---

## Phase 1 — The core loop
*Goal: one location can retrieve cars through the app.*

| Work | Size |
|---|---|
| Customer: Home, vehicle card, **request my car** (Q1) | M |
| Customer: request status + three-node progress stepper | M |
| Valet: queue board — Incoming and Active columns only | L |
| Valet: Accept, Ready, Complete (Q2), Revert | M |
| Valet: request detail modal — parking location, notes | M |
| Real-time channel + reconnection + stale-board banner | L |
| **The chime** — loop, settings plumbing, autoplay handling | M |
| ActivityEvent write path | S |

**Deliberately deferred to later phases:** scheduling, approvals, multi-location, admin.
Phase 1 assumes customers and vehicles are seeded by hand.

**Exit criteria:** a pilot at one real garage. Measure: requests completed without a
phone call, time from request to ready, and how often a valet reports the board wrong.

> This is the decision gate for the whole programme. If the loop does not hold in a real
> garage, fix it here — do not build Phase 2 on top of it.

---

## Phase 2 — Identity & approvals
*Goal: customers can onboard themselves; managers can control who gets service.*

| Work | Size |
|---|---|
| Enrollment: access code → dynamic identifier → profile → first vehicle | L |
| Location access codes: generate, copy, regenerate, deactivate + rate limiting | M |
| Customer: My vehicles, inline edit, add vehicle, photo upload | M |
| ApprovalRequest model + the three kinds, with diff storage | M |
| Manager: Pending Approvals, Approve/Reject, identifier assignment (Q3) | M |
| Manager: Review detail (Q13), rejection reason (Q14) | S |
| Manager: Customers & Vehicles, search, sort, Add customer | M |
| Manager: customer detail view | M |
| Password reset flows | M |

**Exit criteria:** a new resident enrolls with a printed code and is serving-ready after
one manager approval, with no engineer involved.

---

## Phase 3 — Scheduling & history
*Goal: the product handles planned pickups and answers "what happened?"*

| Work | Size |
|---|---|
| Customer: Schedule a pickup, quick options, upcoming list, vehicle selector (Q27) | M |
| Valet board: Tomorrow and Future columns, Move to active, auto-promotion (Q6) | M |
| Timezone correctness across bucketing, scheduling, and retention | M |
| Recently Completed section | S |
| Manager: Request History with filters, search, sort, pagination | M |
| Retention job for the ~7-day window | S |
| Cancellation semantics (Q7, Q17) | S |

**Exit criteria:** a scheduled pickup made three days out surfaces to the right valet at
the right local time without anyone remembering to look.

---

## Phase 4 — Multi-location administration
*Goal: the office runs the portfolio without engineering.*

| Work | Size |
|---|---|
| Admin: Office Console, KPIs, per-location rollups | M |
| Admin: Locations — create, edit, disable, identifier types, inline account creation | L |
| Admin: Users — staff tab, customers tab, suspend/reactivate/reset | L |
| Manager: Valet Account management | M |
| Manager location picker (Q10) | S |
| Admin: Activity History with filters and pagination | M |
| Admin: Settings & Operational Policies, wired for real (Q4) | M |
| Manager: Settings — chime, with a test tone | S |

**Exit criteria:** the office opens a sixth location, staffs it, and enrolls its first
resident with no engineering involvement.

---

## Phase 5 — Hardening & launch
*Goal: safe to run unattended across the portfolio.*

| Work | Size |
|---|---|
| Kiosk hardening: device binding, PIN lock, revocation, timeout (doc 13 §1) | L |
| Customer notifications: bell list, web push, email lifecycle (Q19) | L |
| Escalation + tablet heartbeat monitoring (doc 12) | M |
| Offline action queueing on the valet board | M |
| Accessibility audit and remediation to WCAG 2.2 AA | M |
| Security review, pen test, privacy/retention review with counsel | L |
| Load and soak testing; backup/restore drill | M |
| Operator runbook: tablet setup, credential rotation, code distribution, incident response | M |

**Exit criteria:** a signed-off security and privacy review, and a runbook an operations
manager can follow without calling engineering.

---

## Critical path

```
Q1–Q5 decisions ─► Auth + RBAC ─► Data model ─► Core loop ─► PILOT GATE
                                                                │
                                         ┌──────────────────────┴──────────┐
                                         ▼                                 ▼
                                  Approvals + enrollment          Scheduling + history
                                         └──────────────┬──────────────────┘
                                                        ▼
                                              Multi-location admin
                                                        ▼
                                                Hardening & launch
```

Phases 2 and 3 are largely parallelisable across two streams once the loop is proven.

---

## Risks worth naming now

| Risk | Impact | Mitigation |
|---|---|---|
| **Valets don't adopt the tablet** | Product fails regardless of software quality | Phase 1 pilot before building anything else; observe a real shift; design with the valets, not for them |
| **Tablet choice made late** | Rework across audio, kiosk, offline, PWA | Decide in Phase 0 (Q5) |
| **Shared-kiosk PII exposure** | Serious harm to residents; reputational and legal | Phase 5 hardening is non-negotiable scope, not a stretch goal |
| **Access-code brute force** | Unauthorised enrollment | Rate limiting from day one; keep approval-required on by default |
| **Timezone bugs** | Cars retrieved at the wrong hour; silent and embarrassing | Location-local logic centralised and unit-tested in Phase 3 |
| **Scope creep into analytics** | Dilutes a deliberately narrow product | The prototype's own copy is the defence: analytics is out of scope |
| **Blocking questions answered late** | Rework in the customer flow and approvals | Get Q1–Q3 answered in the first week |

---

## What success looks like

The metrics worth instrumenting from Phase 1:

- **Requests completed without a phone call to the valet stand** — the product's reason to exist
- **Median request → ready time**, per location
- **Time to acceptance** — how long the chime rings before someone taps Accept
- **Manager override rate** — a high rate means the board is not reflecting reality
- **Board uptime during operating hours** — the systemic failure mode from doc 13 §5
