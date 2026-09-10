# 01 — Product Overview

> Requirements authority is [00 — Client Requirements](00-client-requirements.md),
> from the September 10, 2026 session with Jonathan Cohen (Pioneer Parking).

## The problem

At a parking garage or a residential building with valet service, retrieving a car is a
queue managed by shouting, paper tickets, and a phone at the valet stand. The customer
has no visibility into where their car is in that queue. The valet has no reliable
inbound signal. The manager has no record of what happened when a customer disputes a
wait.

Pioneer Parking runs this today on **ElimaWait** (~$165/month) and is replacing it
because it is unreliable and inflexible, with no ownership of the roadmap.

**Reliability is therefore the product's acceptance criterion, not a quality attribute.**
A feature-complete app that drops a request has failed on the client's own terms.

## The core loop

Confirmed step-by-step in the requirements session:

```
  CUSTOMER                    VALET                       OUTCOME
  ────────                    ─────                       ───────
  Tap "Request Now"     ──►   Card lands in INCOMING
                              Chime repeats until accepted
                        ◄──   Tap ACCEPT
  Status: Retrieving          Card moves to ACTIVE QUEUE
   (push only if opted in)
                        ◄──   Tap READY
  Push: "Ready for pickup"    Card moves to COMPLETED     Car at the door
```

> *"Customer visibility is the point. The driving goal is that customers can see
> retrieval progress and avoid standing around waiting unnecessarily."*

Everything else in the product exists to make that loop trustworthy: identity (who owns
which car), approvals (only approved monthly parkers get service), history (what
happened, for disputes), and configuration (which property, which alert settings).

## Who it serves

**Approved, recurring monthly parkers only** — residents *and* non-residents of the
property. That is the whole customer population in MVP.

**Guests and transient parkers are out of scope.** They stay on physical tickets and the
existing credit-card process. They carry a separate payment workflow that belongs to a
later project — see [17 — Roadmap Beyond MVP](17-roadmap-beyond-mvp.md).

## What it is not

Each of these is a client-stated boundary, not a gap:

| Excluded | Source |
|---|---|
| **Billing / payments** | *"Not a billing system."* This is the stated reason valet history can be short |
| **Guests and transient parkers** | Separate payment workflow; deferred to workstream 3 |
| **Broadcast messaging / location-wide alerts** | *"The application handles reservations / retrieval requests — not universal location-wide alerts"* |
| **Customer photo uploads** | Replaced by generic vehicle images, for data load and privacy |
| **SMS** | In-app push only |
| **Advanced analytics dashboards** | Out of MVP. Location-level average fulfilment time is a named *future* consideration |
| **Valet dispatch / rostering** | No named-individual assignment. A location has a shared station account, not a roster |
| **Vehicle telematics** | Parking location is free text a valet types |

## The three theses that shape the architecture

### 1. Ownership
Jonathan wants to own the platform outright — feature set, data, economics. VisMedAI
provides hosting and maintenance on a scalable backend. No third-party SaaS in the
critical path.

### 2. Licensing — the one that changes the code
> *"The app should be designed as a product other parking operators can license, not a
> Pioneer-only internal tool. Company structure, product name and branding must stay
> flexible to support this."*

Consequences, adopted throughout this documentation set:

- **Multi-tenant data model from day one.** A `Tenant` sits above `Location`. Tenant
  isolation is cheap now and expensive later.
- **White-label theming and any operator-facing admin surface are deferred.** Build the
  seam, not the feature.
- **"Pioneer Connect" is a provisional name.** Brand lives in a theme layer, never in
  business logic, table names, or API paths.

### 3. Sequencing
Retrieval app first — fast, contained, winnable. Transient ticketing digitization
second — larger, higher operational stakes. Do not let the second bleed into the first.

## Property portfolio

Pioneer operates two property *types* under one system, which is the key product
pressure:

| Location | Type | City | Identifier at sign-up |
|---|---|---|---|
| Wacker Drive Garage | Garage | Chicago, IL | Decal number |
| State Street Garage | Garage | Chicago, IL | Decal number |
| River North Condos | Residential | Chicago, IL | **Apartment number** |
| South Park Residences | Residential | Orlando, FL | **Stall number** |
| Aster Hall | Residential | New York, NY | — |

Confirmed by the client as a requirement:

> *"Simple location setup with one primary identifier per location: decal number,
> apartment number or unit number, whichever that property uses."*
> *"Records must carry a location identifier."*
> *"Location-specific customer databases — records are scoped to the garage."*

**Do not hard-code "decal number" anywhere.** The identifier is a configured label over a
generic value, chosen per location, and it changes what the customer is asked for at
enrollment. A customer record belongs to exactly one location.

## Scale signals

The prototype's Office Console reports 5 locations, 10 customers, 6 active requests,
6 pending approvals. Seed data, but the shape is real: **many locations, tens-to-hundreds
of monthly parkers per location, single-digit concurrent requests per location.**

This is a low-throughput, high-visibility system. Optimise for correctness,
auditability, and never dropping a request. Multi-tenancy is for *licensing reach*, not
for load.

## Device contexts

| Role | Device | Session model |
|---|---|---|
| Customer | Phone — **native app, both stores** | Personal login, short sessions |
| Valet | **Dedicated tablet at the valet stand** | Shared station account, stays signed in |
| Garage Manager | Desktop, **remote** — explicitly not required on site | Personal login |
| Office Admin | Desktop | Personal login |

Two constraints from the brief with outsized consequences:

- *"App store deployment required."* Two store submissions sit on the critical path and
  are outside the team's control.
- *"Dedicated valet devices — tablets, touchscreen workflow."* The tablet is a kiosk.
  Device sleep, connectivity loss and background-notification behavior on that specific
  hardware are the difference between beating ElimaWait and repeating it.

## Distribution and enrollment

```
QR code posted at the location
        ↓
Enter the location-specific access code
        ↓
Submit name, vehicle information, unit / decal number
        ↓
Routes to the Garage Manager to approve or reject
        ↓
Approved customer gains access to the request workflow
```

A **manager-supported path** also exists: the Garage Manager can create customer records
directly.

**Unresolved and blocking:** customers without smartphones. QR assistance and
manager-supported setup were discussed; a manual override path was identified as likely
but not decided. It affects the data model, the manager UI and the retrieval workflow —
see [14 — Open Questions](14-open-questions.md) Q1.
