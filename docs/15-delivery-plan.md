# 15 — Delivery Plan *(proposed)*

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

> Written to feed the **Tuesday, September 15, 12:00 noon** decision point, at which
> VisMedAI presents MVP scope, timeline and cost. Requirements authority is
> [00 — Client Requirements](00-client-requirements.md).

Sizes below are relative (S/M/L), and the phase structure here is the *engineering* plan.
The **client-facing** version — what the pilot and the full MVP each include, exclude, and
when they land — is [19 — Pilot & Full MVP Scope](19-pilot-and-mvp-scope.md). Costed effort
is in [18 — Cost & Effort Model](18-cost-model.md).

## Sequencing principle

Build **the core loop first, end to end, for one location**, and get it into a real
garage. Everything else — approvals, multi-location administration, policy configuration
— is scaffolding around a loop that either works in the field or does not.

This is not a generic agile preference. Pioneer is leaving ElimaWait **because it is
unreliable**. A valet who will not use the tablet, or a *Ready* push that does not
arrive, invalidates every other feature in the plan. Prove the loop in a garage before
building on top of it.

---

## Phase 0 — Foundations
*Goal: the team can build in parallel, and Tuesday's decisions are locked.*

| Work | Size |
|---|---|
| Close Q1–Q5 in [14 — Open Questions](14-open-questions.md) — two are the client's own blockers | — |
| Choose and procure the valet tablet; buy two for the team | S |
| Decide the native/hybrid split (Q5) — it drives the cost estimate | S |
| Repo, CI, environments, IaC skeleton | M |
| **Multi-tenant data model** + migrations, with cross-tenant isolation tests in CI | L |
| Auth: sign-in, sessions, RBAC middleware, tenant + location scoping | L |
| **Three-tier serializers** (customer / valet / manager) with contract tests — the valet tier must fail the build if `phone` appears | M |
| Design tokens + core components, bound to `Tenant.theme` not hard-coded | L |
| **Generic vehicle image mapping — start it now**, it has a long tail | M |
| Enrol in both app-store developer programmes | S |
| Seed data mirroring the five Pioneer locations | S |

**Exit criteria:** a signed-in user of each role lands on an empty shell of the right
screen; tenant and location scoping are proven by a passing negative-test suite; the
tablet is on a desk.

> **Two items here are unusual to front-load and both are deliberate.** Tenant isolation
> is the client's licensing mandate and is cheap now, expensive later. Store enrolment
> takes calendar days that are outside anyone's control and sits on the critical path.

---

## Phase 1 — The core loop
*Goal: one location retrieves cars through the app, more reliably than ElimaWait.*

| Work | Size |
|---|---|
| Customer: Home, vehicle card, **Request Now** | M |
| Customer: request status, three-node progress, cancel-while-pending | M |
| Valet: queue board — Incoming and Active columns | L |
| Valet: Accept, Ready, Complete (Q4), Revert | M |
| Valet: request detail — parking location, notes, **no phone number** | M |
| Real-time channel + reconnection + stale-board banner | L |
| **The chime** — loop, settings plumbing, audio-permission handling | M |
| **Chime sound design**, three candidates to Jonathan for review | S |
| **Push notifications** — *Ready* delivery, permission priming, delivery telemetry | L |
| **Tablet reliability matrix** on the real device: sleep, backgrounding, Wi-Fi drop, overnight reboot | M |
| ActivityEvent write path | S |

**Deferred to later phases:** scheduling, approvals, multi-location, admin. Phase 1
assumes customers and vehicles are seeded by hand.

**Exit criteria — a pilot at one real garage, measured:**
requests completed without a phone call to the valet stand; time from request to ready;
*Ready* push delivery rate; how often a valet reports the board wrong; board uptime
during operating hours.

> **This is the decision gate for the whole programme.** If the loop does not hold in a
> real garage, fix it here. Do not build Phase 2 on top of a loop that has not been
> proven against the product's own premise.

---

## Phase 2 — Identity & approvals
*Goal: customers onboard themselves; managers control who gets service, remotely.*

| Work | Size |
|---|---|
| Enrollment: QR → access code → dynamic identifier → profile → first vehicle | L |
| Location access codes: generate, copy, regenerate, deactivate + rate limiting | M |
| Customer: My vehicles, inline edit, add vehicle (no photo upload) | M |
| ApprovalRequest model + three kinds, with diff storage | M |
| Manager: Pending Approvals, Approve/Reject, identifier **verification** | M |
| Manager: Review detail (Q13), rejection reason (Q14) | S |
| **Manager-absence backup**: SLA timers, auto-escalation, admin queue (A6), availability switch (M7) | L |
| Manager: Customers & Vehicles, **first-name search**, sort, Add customer | M |
| Manager: customer detail view — where phone numbers live | M |
| **Assisted-customer path** if Q1 lands on staff-proxied requests | M |
| Password reset flows | M |

**Exit criteria:** a new resident enrolls from a printed QR code and is serving-ready
after one manager approval, with no engineer involved — **and** an approval left
untouched for four hours reaches the office by itself.

---

## Phase 3 — Scheduling & history
*Goal: planned pickups work, and "what happened?" has an answer.*

| Work | Size |
|---|---|
| Customer: Schedule a pickup, quick options, upcoming list, vehicle selector (Q26) | M |
| Customer: **notification preferences** — Ready locked, Retrieving opt-in | S |
| Valet board: Tomorrow and Future columns, Move to active, auto-promotion (Q8) | M |
| Timezone correctness across bucketing, scheduling and view windows | M |
| Recently Completed — 2–3 day window | S |
| Manager: Request History, filters, first-name search, pagination | M |
| **Permanent backend retention** + windowed views, cleanly separated | M |
| **Written retention and access policy** — client-flagged risk, in scope | M |
| Cancellation semantics (Q11) | S |

**Exit criteria:** a pickup scheduled three days out surfaces to the right valet at the
right local time without anyone remembering to look; and the retention policy is written
and reviewed.

---

## Phase 4 — Multi-location administration
*Goal: the office runs the portfolio without engineering.*

| Work | Size |
|---|---|
| Admin: Office Console, KPIs (incl. escalated approvals), per-location rollups | M |
| Admin: Locations — create, edit, disable, identifier types, inline account creation | L |
| Admin: Users — staff tab, customers tab, suspend/reactivate/reset | L |
| Manager: Valet Account management | M |
| Manager location picker (Q18) | S |
| Admin: Activity History — the permanent archive, filters, pagination over years | M |
| Admin: Settings & Operational Policies, wired for real, incl. approval SLAs | M |
| Manager: Settings — chime, with a test tone | S |

**Exit criteria:** the office opens a sixth location, staffs it, and enrolls its first
resident with no engineering involvement.

---

## Phase 5 — Hardening & launch
*Goal: safe to run unattended, and shipped to both stores.*

| Work | Size |
|---|---|
| Kiosk hardening: device binding, PIN lock, revocation, wake locks (doc 13 §1) | L |
| **App-store submission prep**: privacy labels, in-app account deletion, push consent copy | M |
| **Two store submissions + at least one rejection cycle each** — outside our control | M |
| Escalation + tablet heartbeat monitoring | M |
| Offline action queueing on the valet board | M |
| Accessibility audit to WCAG 2.2 AA | M |
| Security review, pen test, **cross-tenant isolation review** | L |
| Privacy review with counsel — permanent retention vs. erasure rights | M |
| Load and soak testing; backup/restore drill | M |
| Operator runbook: tablet setup, credential rotation, code distribution, incident response | M |

**Exit criteria:** signed-off security and privacy reviews, both apps live, and a runbook
an operations manager can follow without calling engineering.

---

## Critical path

```
Q1–Q5 decisions ──┐
Store enrolment ──┼─► Tenancy + Auth ─► Data model ─► CORE LOOP ─► PILOT GATE
Tablet procured ──┘                                                     │
                                          ┌─────────────────────────────┴────────┐
                                          ▼                                      ▼
                              Approvals + enrollment                  Scheduling + history
                              + absence backup                        + retention policy
                                          └──────────────┬───────────────────────┘
                                                         ▼
                                               Multi-location admin
                                                         ▼
                                      Hardening ─► STORE REVIEW ─► launch
                                                   (not ours to schedule)
```

Phases 2 and 3 parallelise across two streams once the loop is proven. Store review
brackets the end and cannot be compressed — plan around it rather than through it.

---

## Risks — client's register, plus engineering's

The first five are reproduced from the brief and belong in Tuesday's proposal verbatim.

| Risk | Impact | Mitigation |
|---|---|---|
| **Licensing ambition vs. MVP cost** *(client)* | Multi-tenancy is not free in the MVP | Tenant isolation in the data model now; white-label theming and operator admin deferred. **State the tradeoff so it is Jonathan's call** |
| **Permanent retention vs. privacy posture** *(client)* | Legal exposure; inconsistent with withholding phone numbers from valets | Written retention and access policy, in scope, Phase 3. Counsel review Phase 5 |
| **App-store review timelines** *(client)* | Two submissions outside our control, on the critical path | Enrol in Phase 0; budget a rejection cycle per platform; do not absorb as slippage |
| **Valet tablet reliability** *(client)* | *"The entire premise for replacing ElimaWait"* | Explicit line item: pin the device Phase 0, reliability matrix Phase 1, heartbeat Phase 5 |
| **IP ownership** *(client)* | Funded build + licensing intent, unresolved | Settle ownership, licence terms and revenue share in the commercial agreement — **before code exists** |
| **Valets don't adopt the tablet** | Product fails regardless of software quality | Phase 1 pilot before building anything else; observe a real shift; design with the valets |
| **Push is the only customer channel** | A missed *Ready* is an invisible failure | Permission priming with context, denied-state repair, delivery telemetry, in-app state always correct |
| **Blocking questions answered late** | Rework in the data model, not just the UI | Q1 and Q2 are on Tuesday's agenda; Q3–Q5 in the first week |
| **Scope creep into ticketing** | Dilutes a deliberately narrow MVP | The client set the boundary himself — hold it, and point at workstream 3 |

---

## What success looks like

Instrument from Phase 1:

- **Requests completed without a phone call to the valet stand** — the product's reason to exist
- **Median request → ready time**, per location
- **Time to acceptance** — how long the chime rings before someone taps Accept
- ***Ready* push delivery rate** — the only channel to the customer
- **Manager override rate** — high means the board is not reflecting reality
- **Board uptime during operating hours** — the systemic failure mode
- **Approval time-to-decision, and escalation rate** — whether the absence backup is working

The first and the last are the two the client will actually judge this on: *does the app
make retrieval visible*, and *does anything stall when a manager is away*.
