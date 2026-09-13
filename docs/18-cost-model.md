# 18 — MVP Cost & Effort Model *(proposed)*

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

> Bottom-up effort estimate for **workstream 1**, the valet retrieval MVP, derived from the
> scope in docs 01–15. Prepared for the **Tuesday 15 September** decision point.
>
> **This document estimates effort, not price.** Person-days are derived from the spec and
> are defensible line by line. The day rate, margin and commercial structure are VisMedAI's
> to set — the rate tables below are illustrative anchors, not a quote.

---

## 1. Headline

Two figures matter, and they measure different worlds.

| | Conventional delivery | **AI-augmented delivery** |
|---|---|---|
| **Pilot** — core loop live in one garage | ~185 person-days · ~$60,000 | **~72 days · $26,000 – $28,000 · 7 weeks** |
| **Full MVP** — both stores, all locations | ~505 person-days · **$150,000 – $200,000** | **~155 days · $55,000 – $60,000 · 18 weeks** |

Scope boundaries and week-by-week timelines are in
[19 — Pilot & Full MVP Scope](19-pilot-and-mvp-scope.md).

### Why both numbers belong in the proposal

The bottom-up model in §3 below produces **505 person-days** for the full MVP. At a
conventional blended rate of $300–400/day that is **$151,000–$202,000** — which
independently corroborates the client-side estimate of what this build would have cost
before AI tooling. Two methods, one answer.

That makes the delivered price a *quantified* discount rather than a cheap quote:

```
Conventional delivery, bottom-up:        $150,000 – $200,000
AI-augmented, pilot (Phases 0–1):        $ 26,000 – $ 28,000
AI-augmented, full MVP (Phases 0–5):     $ 55,000 – $ 60,000
```

**Lead with the benchmark.** Quote $27,000 alone and Jonathan values the asset at
$27,000 — which matters more than usual here, because licensing is the ROI (§2) and his
mental model of what he owns is set the day a price is named. Stated against the
benchmark, the same money buys $175,000 of asset at roughly 15 cents on the dollar. That
is also the honest description of what is happening.

### What compresses, and what does not

The discount is not uniform, and pricing as though it were is how a fixed price bleeds.

| Compresses hard | Resists compression |
|---|---|
| Screen implementation from a written spec | Tablet reliability matrix on real hardware |
| CRUD admin surfaces, forms, tables | The pilot itself — a real shift, in a real garage |
| Migrations, boilerplate, test scaffolding | App store review — calendar, not effort |
| Documentation and specification synthesis | Penetration test and legal counsel |
| | Vehicle image asset set — ~150 assets of design labour |
| | Client decision latency |

Phase 4 — locations, users, activity archive, settings — is 75 conventional days of
tables and forms and compresses hardest of anything in the plan. Phase 5 compresses
least, because most of it is other people's calendars.

### Two conditions the price depends on

1. **A client-supplied specification exists**, produced by a previous provider, and it
   carries forward. Discovery is not being repaid.
2. **The codebase is not greenfield** — the app, brand system, screens and Docker backend
   already exist. Phase 0 is a gap-fill, not a build.

If either fails, the compression assumption fails with it. Both belong in the contract
as stated assumptions, alongside a change-control clause naming what triggers a revision.
A fixed price written against someone else's specification absorbs every gap in that
document at your margin.

---

## 2. The number that reframes the conversation

Pioneer is replacing ElimaWait at **~$165/month — $1,980 a year.**

At any rate in the table above, the build does not pay back against that saving in a human
lifetime. **The ElimaWait saving is not the business case and should not be presented as
one.** Jonathan already knows this — he named the real thesis himself:

> *"Jonathan wants to own the platform outright — control the feature set, the data and the
> economics."*
> *"The app should be designed as a product other parking operators can license."*

Three consequences worth stating plainly on Tuesday:

**1. Licensing is the ROI, not a bonus.** The brief frames multi-tenancy as a tension —
*"licensing ambition vs. MVP cost … they pull against each other."* If licensing is the only
path that returns the investment, that framing inverts: **tenant isolation is not a cost to
trade away, it is the asset being bought.** It is also the cheapest it will ever be, at
roughly 15–20 days in Phase 0 versus a multi-month retrofit later.

**2. IP ownership stops being paperwork.** Risk 5 in the brief — *"IP ownership, license
terms and revenue share need to be settled before code exists"* — is not a legal footnote
sitting beside the build. It determines whether the build returns anything at all. It should
be settled in the same conversation as the budget, not after it.

**3. Ownership has standalone value even if licensing never happens.** Control of the
roadmap, the data and the customer relationship across a growing portfolio is worth
something to an operator winning HOA contracts on operational credibility — which is exactly
what the website workstream is being built to sell. That is a defensible reason to proceed
even on a pessimistic licensing view, and it is worth saying out loud so the decision does
not rest on licensing alone.

---

## 3. Phase breakdown

All figures are person-days, all-in: design, engineering, QA and delivery management.

| Phase | Low | Plan | High | What dominates |
|---|---:|---:|---:|---|
| **0 · Foundations** | 75 | **85** | 95 | Multi-tenant model, auth/RBAC, component system, vehicle-image set |
| **1 · Core loop** ⟵ *gate* | 88 | **100** | 115 | Valet board, real-time, chime, push, on-device reliability, pilot |
| **2 · Identity & approvals** | 92 | **105** | 120 | Enrollment, approval engine, absence backup, customer management |
| **3 · Scheduling & history** | 55 | **62** | 72 | Future pickups, timezones, retention split and policy |
| **4 · Administration** | 65 | **75** | 85 | Locations, users, activity archive, policies |
| **5 · Hardening & launch** | 70 | **80** | 95 | Kiosk security, store submission, a11y, security and privacy review |
| **Total** | **445** | **507** | **582** | |

### Discipline split across the full MVP

| Discipline | Days | Share |
|---|---:|---:|
| Backend — API, data, real-time, push infrastructure | ~145 | 29% |
| Frontend web — manager and admin consoles, valet board | ~100 | 20% |
| Mobile — React Native customer app, both platforms | ~80 | 16% |
| Design — UX, UI across ~24 screens, component system, vehicle images | ~55 | 11% |
| QA | ~60 | 12% |
| Delivery management | ~45 | 9% |
| DevOps / infrastructure | ~25 | 5% |

---

## 4. The ten largest line items

Where the money actually goes. Anything here that gets cut changes the number materially;
everything else is rounding.

| # | Item | Days | Why it costs what it costs |
|---|---|---:|---|
| 1 | Valet queue board + card system + actions | 24 | Four columns, five card states, two modals, live updates, multi-tablet contention |
| 2 | Multi-tenant model, auth, RBAC, three-tier serializers | 26 | Tenant + location + ownership scoping, enforced at the data layer, with negative tests |
| 3 | Enrollment flow | 20 | QR → code resolution → **dynamic identifier per location** → profile → first vehicle → approval |
| 4 | Real-time channel, reconnection, stale-state handling | 18 | The reliability backbone. Garage Wi-Fi drops are the normal case, not the edge case |
| 5 | Push end-to-end, both platforms, with delivery telemetry | 18 | The only channel to the customer; SMS was ruled out |
| 6 | Manager-absence backup | 16 | SLA timers, auto-escalation, admin queue, availability switch — the client's flagged gap |
| 7 | Locations administration | 16 | CRUD, identifier types, access codes, inline account provisioning, two distinct off-switches |
| 8 | Users administration | 16 | Staff and customer tabs, roles, multi-location assignment, suspend/reset |
| 9 | Kiosk hardening | 14 | Device binding, PIN lock, revocation, wake locks on an always-signed-in shared tablet |
| 10 | Generic vehicle image system | 14 | Resolver plus ~150 body-style × colour assets. A deliverable with a long tail |

---

## 5. What is *not* in the number

Present these as separate lines so the build figure is not later read as all-in.

| Item | Estimate | Note |
|---|---|---|
| **Valet tablets** | ~$400–600 each | Per location, plus two for the team. Client capex |
| **External penetration test** | ~$10,000–20,000 | Recommended before launch given the shared-kiosk and multi-tenant surface |
| **Legal counsel** | Counsel's fee | Retention/privacy policy, plus the IP and licence agreement |
| **Apple + Google developer accounts** | $99/yr + $25 once | Enrol in Phase 0 — account verification takes calendar days |
| **Website refresh** | Workstream 2 | Separate estimate — see [16 — Website Refresh](16-website-refresh.md) |
| **Transient ticketing** | Workstream 3 | Not estimable until Jonathan demonstrates the workflow. See [17](17-roadmap-beyond-mvp.md) |

### Ongoing, post-launch

| Item | Estimate |
|---|---|
| Infrastructure at ~5 locations | **~$400–900/month** — low throughput; managed Postgres, app hosting, push, CDN, monitoring |
| Hosting + maintenance retainer | **~15–20% of build value per year**, or a fixed monthly retainer with a defined SLA |
| Feature development beyond MVP | Time and materials, or a capacity retainer |

Infrastructure is genuinely cheap here: single-digit concurrent requests per location. The
recurring cost is people, not servers.

---

## 6. Assumptions

The estimate holds only if these hold. Any that breaks moves the number.

1. **Team of 4–5** — one designer, two to three engineers spanning backend/web/mobile, QA
   shared, delivery management part-time.
2. **One codebase family** — React Native customer app, responsive web consoles, shared types
   and API client. **This is decision D5; if it resolves differently, re-cost.**
3. **Design is ours to make** — the prototype is a working reference, not a signed-off design
   system. Screen design is included; a separate brand exercise is not.
4. **Blocking decisions D1–D5 land on Tuesday.** Late answers on D1 (no-smartphone customers)
   or D5 (platform) cause rework in the data model, not just the UI.
5. **One pilot location**, with Pioneer staff available to observe a real shift.
6. **Scope as specified in docs 01–15**, with the exclusions in doc 14 held.
7. **Store review passes within two cycles per platform.**
8. Content and assets — vehicle image direction, chime candidates — are reviewed by the
   client within a week of delivery.

---

## 7. Levers, if the number needs to move

Ranked by value returned per day saved. The first is the recommendation; the last two are
listed to be argued against.

| Lever | Saves | Verdict |
|---|---:|---|
| **Stage the funding at the Phase 1 gate** | — | **Recommended.** Commit ~185 days to a piloted core loop, then decide on the remaining ~320 with evidence in hand. Costs nothing and de-risks everything |
| Defer Phase 4 administration; VisMedAI operates locations manually at first | ~75 d | **Viable.** Five locations is a small enough portfolio to administer by hand for a few months. Delays self-service, not service |
| Defer scheduling (Phase 3) to a fast-follow | ~62 d | Viable. Immediate retrieval is the core promise; scheduled pickups are an enhancement |
| Web/PWA pilot instead of native | ~45 d | **Not recommended.** Push reliability is precisely what the pilot exists to test; testing it on a weaker channel produces a false result |
| Drop multi-tenancy from the MVP | ~15–20 d | **Reject.** It saves the least and costs the most later. Per §2, it *is* the business case |
| Skip the security and privacy review | ~25 d | **Reject.** Shared kiosk, resident home addresses, real-time vehicle locations, permanent retention. Not a defensible saving |

### The recommendation in one line

**Fund the pilot, not the programme.** Seven weeks and $26–28K buys a measured answer to
the only question that matters — requests completed without a phone call, request-to-ready
time, push delivery rate, board uptime. The remaining ~$30K is then a decision made on
evidence rather than on a specification, and if the gate answer is no, the exposure was
seven weeks rather than eighteen. It matches the sequencing thesis Jonathan already set,
and it puts the reliability question that justifies the whole project first rather than
last.

---

## 8. Confidence

| Phase | Confidence | Why |
|---|---|---|
| 0 · Foundations | **High** | Well-understood platform work with a clear spec |
| 1 · Core loop | **Medium** | On-device tablet behaviour and push reliability are empirical. This is where surprises live |
| 2 · Identity & approvals | **Medium-high** | Broad but conventional; the absence backup is newly specified |
| 3 · Scheduling & history | **High** | Contained, and the data model already supports it |
| 4 · Administration | **High** | Forms and tables against a settled model |
| 5 · Hardening & launch | **Low-medium** | Store review, pen-test findings and counsel's retention position are all outside our control |

The ±13% band on the total reflects Phases 1 and 5. Do not present a single point number
without the range attached.
