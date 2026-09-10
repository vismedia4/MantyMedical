# 01 — Product Overview

## The problem

At a parking garage or a residential building with valet service, retrieving a car is
a queue managed by shouting, paper tickets, and a phone at the valet stand. The
customer has no visibility into where their car is in that queue. The valet has no
reliable inbound signal. The manager has no record of what happened when a customer
disputes a wait.

Pioneer Connect replaces the ticket and the phone call with a shared, real-time
request queue.

## The core loop

```
  CUSTOMER                    VALET                       OUTCOME
  ────────                    ─────                       ───────
  Tap "request my car"  ──►   Card lands in INCOMING
                              Chime repeats until accepted
                        ◄──   Tap ACCEPT
  Status: Retrieving          Card moves to ACTIVE QUEUE
                        ◄──   Tap READY
  Status: Ready for pickup    Card moves to COMPLETED     Car at the door
```

Everything else in the product exists to make that loop trustworthy: identity
(who owns which car), approvals (only real residents get service), history (what
happened, for disputes), and configuration (which property, which alert settings).

## What it is not

Explicitly out of scope in the prototype, stated on-screen:

- **Advanced analytics dashboards** — the Activity History screen says so in its own
  subtitle. History exists for *review and dispute resolution*, not BI.
- **Payments / billing** — no pricing, invoice, tip, or payment surface anywhere in
  22 screens. Valet service is presumably bundled into rent or a parking contract.
- **Valet dispatch / assignment** — there is no concept of assigning a request to a
  named individual valet. A location has a *shared station account*, not a roster.
- **Vehicle location tracking / telematics** — parking location is a free-text field
  a valet types (`e.g. Level 3 East, Red Zone, Charging Station A`).

Treat all four as deliberate scope boundaries, not as gaps.

## Property portfolio (from the prototype's seed data)

Pioneer Parking operates two property *types* under one app, which is the key
architectural pressure in the product:

| Location | Type | City | Identifier asked at sign-up |
|---|---|---|---|
| Wacker Drive Garage | Garage | Chicago, IL | Decal number |
| State Street Garage | Garage | Chicago, IL | Decal number |
| River North Condos | Residential | Chicago, IL | **Apartment number** |
| South Park Residences | Residential | Orlando, FL | **Stall number** |
| Aster Hall | Residential | New York, NY | — |

**This is the single most important product fact in the documentation.** A commercial
garage identifies a customer's car by a windshield decal; a condo building identifies
it by the resident's apartment; another by their assigned stall. The identifier type
is **per-location configuration**, chosen by the Office Admin when the location is
created, and it changes what the customer is asked for at enrollment.

Build the customer identifier as a configured label over a generic value. Do not
hard-code "decal number" anywhere in the codebase.

## Scale signals

The prototype's Office Console reports 5 locations, 10 total customers, 6 active
requests, 6 pending approvals. Seed data, not a forecast — but it does tell you the
shape: **many locations, tens-to-hundreds of customers per location, single-digit
concurrent requests per location.** This is a low-throughput, high-visibility system.
Optimize for correctness, auditability, and never dropping a request. Do not
prematurely optimize for scale.

## Three device contexts, one product

| Role | Device | Session model |
|---|---|---|
| Customer | Phone (mobile web / installable app) | Personal login, short sessions |
| Valet | **Tablet at the valet stand** | Shared station account, *stays signed in* |
| Garage Manager | Desktop | Personal login |
| Office Admin | Desktop | Personal login |

The valet tablet is a kiosk. The Valet Account screen states it plainly: *"one login
stays signed in on the tablet."* That single sentence drives real requirements —
see [13 — Non-Functional Requirements](13-nonfunctional-requirements.md).

## Distribution

The landing page offers **Sign In**, **Create Account**, and a **QR code** captioned
*"Scan to download or open Pioneer Connect — one app for every Pioneer property."*

Enrollment is gated by a **6-digit Location Access Code** the property hands out
(*"Your Location Access Code links you to your garage at sign-up"*). Codes are
generated per location, can be copied, regenerated, and deactivated. Deactivating a
location hides it from customer registration entirely.
