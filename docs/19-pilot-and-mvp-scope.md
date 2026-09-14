# 19 — Pilot & Full MVP: Scope and Timeline *(proposed)*

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

> For the **Tuesday 15 September** decision. Two things are being priced, and they are
> not the same purchase. This document says what each one contains, what it deliberately
> does not, and when it lands.
>
> Effort derivation is in [18 — Cost & Effort Model](18-cost-model.md).

---

## 1. The two purchases at a glance

| | **Pilot** | **Full MVP** |
|---|---|---|
| **Price** | **$26,000 – $28,000** | **$55,000 – $60,000** *(inclusive of the pilot)* |
| Conventional-delivery benchmark | ~$60,000 | **$150,000 – $200,000** |
| Effort, AI-augmented | ~72 person-days | ~155 person-days |
| Duration | **7 weeks** | **18 weeks**, plus store review |
| Locations | **One** — Wacker Drive Garage | All five |
| Roles live | Customer + Valet | All four |
| App distribution | Internal build (TestFlight / internal track) | **Public, both stores** |
| Ends with | A measured gate decision | A production system |

The pilot is not a demo and not a prototype. It is the real system, running a real
garage, narrowed to the one loop that justifies the whole project.

---

## 2. Pilot — 7 weeks

**Objective:** prove the retrieval loop is more reliable than ElimaWait, in a real
garage, with real valets, before spending the rest of the budget.

### Timeline

Assumes a **21 September start** — the Monday after the decision. Every date shifts
one-for-one with the decision date.

| Week | Dates | Work | Milestone |
|---|---|---|---|
| **1** | Sep 21 – 25 | Blocking decisions locked. Tablet procured. Foundations gap-fill against the existing codebase: tenancy, auth scoping, serializer tiers | Tablet on a desk |
| **2** | Sep 28 – Oct 2 | Customer: Request Now, live status, cancel-while-pending. Request lifecycle and audit events | Request reaches the board |
| **3** | Oct 5 – 9 | Valet board: Incoming and Active columns, Accept / Ready / Complete / Revert, request detail with parking location and notes | Loop closes end to end |
| **4** | Oct 12 – 16 | Real-time channel, reconnection, stale-board banner. The chime and its manager settings | Board holds under a dropped connection |
| **5** | Oct 19 – 23 | Push notification on Ready. Device reliability matrix on the real tablet: sleep, backgrounding, Wi-Fi drop, overnight reboot, audio permission | **Internal build ready** |
| **6** | Oct 26 – 30 | **Pilot at Wacker Drive Garage.** Observe a full shift. Same-week fixes | **Live in a garage** |
| **7** | Nov 2 – 6 | Measure, iterate, report | **Gate decision** |

**Gate metrics, agreed in advance:** requests completed without a phone call to the
valet stand · median request-to-ready time · time-to-acceptance (how long the chime
rings) · Ready push delivery rate · board uptime during operating hours.

### Pilot includes

**Customer**
- Sign in
- Home with vehicle card and **Request Now**
- Live request status — Pending · Retrieving Vehicle · Ready for Pickup
- Cancel while pending
- Push notification when the vehicle is ready

**Valet**
- Queue board: Incoming and Active Queue, with Recently Completed
- Accept · Ready · Complete · Revert to Pending
- Request detail: customer name, parking location, internal notes — **no phone number**
- The chime: repeats until accepted, manager-configurable, valet cannot disable

**Manager**
- Status override on any request, with an audit event

**Platform**
- Multi-tenant data model and location scoping
- Real-time updates with reconnection and an honest stale-state banner
- Append-only activity log
- One location, one valet station account, seeded customers and vehicles

### Pilot excludes — deliberately

| Excluded | Why | Lands in |
|---|---|---|
| **Approvals workflow** | Only needed if self-registration is switched on — see the option below | Phase 2 |
| **Manager-absence backup** | Depends on approvals | Phase 2 |
| **Scheduled and future pickups** | Immediate retrieval is the core promise; scheduling is an enhancement | Phase 3 |
| **Request history and archive UI** | Seven weeks of data is not a history problem | Phase 3 |
| **Notification preferences** | Ready-only, on by default, is the pilot configuration | Phase 3 |
| **Manager and admin consoles** | One location administered by hand | Phases 2 & 4 |
| **The other four locations** | One garage is the test | Phase 4 |
| **Public app store release** | Internal distribution only — removes two review cycles from the critical path | Phase 5 |
| **Kiosk hardening** | Basic lock only. Full device binding and PIN lock follow | Phase 5 |
| **Accessibility audit, pen test, privacy review** | External and formal; premature before the loop is proven | Phase 5 |
| **Assisted (no-smartphone) customers** | Pending decision D1 | Phase 2 |

### Pilot option — self-registration by QR code

**This one is Pioneer's call, not ours.** It is the only item in the pilot that we
recommend the client decide rather than us, because it changes what the pilot proves.

| | **Without it** (base pilot) | **With it** |
|---|---|---|
| How customers get in | We seed them by hand for one garage | A resident scans a printed code and registers themselves |
| What the pilot proves | The retrieval loop works | The retrieval loop works **and** residents can self-serve |
| Also required | — | Access codes, the approval step, manager-absence backup |
| Timeline | 7 weeks | **9 weeks** |
| Price | **$26,000 – $28,000** | **$33,000 – $35,000** |

**Our read:** the base pilot is the faster, cleaner test. Hand-seeding fifty residents in
one garage takes an afternoon, and registration is not the thing anyone doubts — the
retrieval loop is. Self-registration is real work that will have to be built either way,
and it is already scoped into Phase 2 at no loss if deferred.

**The case for including it now:** if Pioneer intends to show this to other operators
during the pilot, a garage where residents enroll themselves demonstrates the product;
a garage where we typed everyone in demonstrates a demo. That is a business judgement
about who sees the pilot, which is why it belongs to the client.

Either answer is fine. We need it before week 1 — after that it costs more than $7,000
to add, because approvals reach into the data model.

**What the exclusions buy:** the pilot answers one question — *does this work in a
garage* — in seven weeks instead of eighteen, for 15% of the conventional cost. Every
excluded item is deferred, not cancelled.

---

## 3. Full MVP — 18 weeks

**Objective:** all five locations, all four roles, live in both app stores, running
unattended.

### Timeline

Continues from the gate. Dates assume the pilot proceeds without a stop.

| Weeks | Dates | Phase | Milestone |
|---|---|---|---|
| **1 – 7** | Sep 21 – Nov 6 | *Pilot, as above* | Gate decision |
| **8 – 11** | Nov 9 – Dec 4 | **Identity & approvals** — QR enrollment with per-location identifier, access codes, the three approval kinds, manager-absence backup with SLA and escalation, customers and vehicles management | A resident enrolls from a printed code and is serving-ready after one approval |
| **12 – 13** | Dec 7 – Dec 18 | **Scheduling & history** — future and tomorrow pickups, auto-promotion, timezone correctness, notification preferences, retention split and written policy | A pickup booked three days out surfaces at the right local time |
| **14 – 15** | Jan 4 – Jan 15 | **Administration** — locations, users, access codes, activity archive, operational policies, valet accounts | The office opens a sixth location without engineering |
| **16 – 18** | Jan 18 – Feb 5 | **Hardening & launch** — kiosk security, accessibility audit, security and privacy review, store submission prep, runbook | **Submitted to both stores** |
| **+2 – 4** | Feb – Mar | *Store review* | **Public release** |

> **Weeks 14 – 15 skip 21 December – 1 January.** A build running November to January
> loses roughly two weeks to the holidays. That is in the schedule above rather than
> discovered in January.

> **Store review is not ours to schedule.** Two submissions, each with at least one
> likely rejection cycle. Budget 2–4 weeks after week 18 and treat it as a date range,
> not a deadline.

### Full MVP adds, on top of the pilot

**Customer** — QR enrollment with the location's own identifier (decal / apartment /
stall) · multiple vehicles with add and edit under approval · scheduled pickups with
quick options · notification preferences · notification list

**Valet** — Tomorrow and Future Pickups columns with Move to Active · the read-only
directory with first-name search · recent pickups

**Garage Manager** — dashboard · pending approvals across all three kinds ·
customers and vehicles with first-name search · customer detail · request history ·
valet account management · chime settings · **availability switch**

**Office Admin** — cross-location console · locations with identifier types, access
codes and inline account provisioning · staff and customer users · permanent activity
archive · operational policies and approval SLAs · **escalated-approvals queue**

**Platform** — all five locations · full push suite · permanent retention behind
windowed views · kiosk hardening · WCAG 2.2 AA · security and privacy review · both
app stores · operator runbook

### Full MVP excludes — permanently, by client decision

These are not deferred. They were ruled out in the 10 September session and should not
be reopened mid-build.

| Excluded | Client's words |
|---|---|
| Billing and payments | *"Not a billing system"* |
| Guests and transient parkers | Separate payment workflow — [workstream 3](17-roadmap-beyond-mvp.md) |
| Broadcast and location-wide messaging | *"Not universal location-wide alerts"* |
| Customer photo uploads | Generic images from make, model and colour |
| SMS notifications | *"In-app push notifications only. No SMS."* |
| Advanced analytics dashboards | *"(Advanced analytics dashboards are out of scope.)"* |
| Named-valet rostering and dispatch | Shared station accounts only |
| Vehicle telematics | Parking location is free text |

### Deferred beyond MVP, not excluded

| Item | Note |
|---|---|
| Location-level average fulfilment time | Named in the brief as a future consideration. The timestamps are captured from day one |
| White-label theming, operator-facing admin | The tenant seam is built in the MVP; the surface is not |
| Transient ticketing and coupon management | [Workstream 3](17-roadmap-beyond-mvp.md). Not estimable until the workflow session happens |

---

## 4. Not in either price

Quote these separately so neither figure reads as all-in.

| Item | Estimate | Whose |
|---|---|---|
| Valet tablets | ~$400–600 each, per location plus two for the team | Client capex |
| External penetration test | ~$10,000–20,000 | Third party |
| Legal counsel | Counsel's fee | Third party — retention policy, IP and licence agreement |
| Apple + Google developer accounts | $99/yr + $25 once | Client |
| Infrastructure, running | ~$400–900/month at five locations | Ongoing |
| Hosting and maintenance | Retainer, terms TBD | VisualMedia |
| Website refresh | Separate — [workstream 2](16-website-refresh.md) | |

---

## 5. Assumptions

Both timelines depend on these. Any that breaks moves the dates.

1. **Decision on 15 September**, contracts signed that week, start 21 September.
2. **Blocking decisions D1–D5 answered at that meeting.** Late answers on D1
   (no-smartphone customers) or the platform split cause rework in the data model,
   not just the UI.
3. **The existing codebase and the client-supplied specification carry forward.** The
   compression assumes we are not starting from zero — the app, the brand system and
   the Docker backend already exist.
4. **A pilot garage and a cooperative shift** are available in week 6, with Pioneer
   staff present to observe.
5. **Client review inside one week** for the chime candidates, the vehicle image
   direction, and the gate report.
6. **Two store submissions pass within two cycles each.**
7. Scope as specified in docs 01–15, with the exclusions above held.

---

## 6. The recommendation

**Commit to the pilot. Decide the rest at the gate.**

Seven weeks and $26–28K buys a measured answer to the only question that matters:
does this beat ElimaWait in a real garage. The remaining ~$30K is then a decision made
on evidence rather than on a specification — and if the answer at the gate is no, the
exposure was seven weeks, not eighteen.

It costs nothing to structure the engagement that way, and it puts the reliability
question that justifies the entire project first rather than last.
