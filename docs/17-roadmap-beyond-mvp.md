# 17 — Roadmap Beyond MVP (Workstream 3)

> Source: [00 — Client Requirements](00-client-requirements.md) §2, from the brief's §5.
> **Explicitly outside MVP scope.** Documented so the boundary is deliberate and the MVP
> architecture does not preclude it.

## Why this document exists

The client set this boundary himself, and framed the sequencing:

> *"Jonathan frames the reservation app as the quick win that precedes this larger,
> operationally critical project."*

Two failure modes this document guards against:

1. **Scope creep.** Ticketing is bigger than the retrieval app and touches money. If it
   leaks into MVP, the "quick win" stops being quick and the premise of the sequencing
   collapses.
2. **Architectural dead ends.** Building MVP as if ticketing will never exist can force
   an expensive rewrite. A few cheap decisions now keep the door open.

---

## Transient ticketing digitization

Digitising the current paper-based transient ticket system.

### Scope discussed

| Area | Detail |
|---|---|
| **Ticketing** | Replace paper transient tickets |
| **Digital payments** | Card payment at exit or in-app |
| **QR scanning** | Entry / exit validation |
| **Tax records** | Reporting obligations on transient revenue |
| **Shift reporting** | Per-shift reconciliation for attendants |

### Coupon management — a separate module

> *"Treated as a separate module or add-on. Requires serialization and governance
> controls to expand safely across many garages."*

The serialization requirement is the tell: coupons are bearer instruments with real
fraud exposure. Each coupon needs a unique serial, a redemption record, and controls over
who can issue and how many. That is a compliance-shaped problem, not a UI problem, and it
is correctly scoped as its own module.

### Client commitments to enable this

Jonathan agreed to:

- Provide existing transient-parking report formats and process details
- Demonstrate the end-to-end ticketing and coupon-processing workflow in a dedicated
  future session

**Neither has happened yet.** Do not estimate this project before that session. The
report formats are the requirements document for the reporting half of it.

---

## What the MVP should do now to avoid a dead end

Cheap decisions that keep the door open, all already reflected in the MVP docs:

| Decision | Where | Why it matters later |
|---|---|---|
| **Multi-tenant model from day one** | doc 03, doc 13 §0 | Ticketing is per-operator too; retrofitting tenancy across a payments system is far worse than across this one |
| **`Location` as the operational root with typed configuration** | doc 03 | Ticketing config (rates, validation rules, coupon issuance) hangs off the same root |
| **Permanent `ActivityEvent` archive** | doc 03, doc 04 §8 | Tax records and shift reporting need an immutable event log. Building one now for disputes means it already exists |
| **Roles as data, not as code branches** | doc 02 | A ticketing "attendant" role slots in without touching the permission engine |
| **Customer type distinguishable** | doc 03 | MVP serves `monthly` parkers only; make the field exist so `transient` can join it |

**What the MVP must NOT do:**

- Do not build a payments integration "just in case." It is the largest cost in workstream
  3 and every assumption made now without requirements will be wrong.
- Do not model rates, validation or coupons speculatively.
- Do not widen the customer model to accommodate transient parkers. They have a different
  identity model (often none at all) and a different lifecycle.

The rule: **build the seams, not the features.**

---

## Sequencing rationale — worth restating

The retrieval app is the right first project, and it is worth being explicit about why,
because the pressure to do the bigger thing first is real:

| | Retrieval app | Ticketing |
|---|---|---|
| Users | ~10s–100s of approved monthly parkers per location | Every transient driver |
| Money | **None** — not a billing system | Cash, cards, tax, reconciliation |
| Failure mode | A customer waits longer | **Revenue loss, tax exposure, fraud** |
| Replaces | ElimaWait, ~$165/mo | An entrenched paper process with staff habits |
| Time to value | Weeks | Months |

The retrieval app proves the working relationship, the architecture and the operational
model on a low-stakes surface. Ticketing then inherits a proven platform instead of
being the place where the platform is discovered.

---

## Also parked

Named in the brief or in the prototype as future, not MVP:

| Item | Source | Note |
|---|---|---|
| **Location-level average fulfilment time reporting** | Brief §3.6 — *"future consideration"* | Data model already captures the timestamps. Reporting surface deferred |
| **Advanced analytics dashboards** | Prototype UI — *"out of scope"* | The activity feed is for review and disputes, not BI |
| **White-label theming, operator-facing admin** | Brief risk §1 | Deferred with the licensing surface; the seam is built |
| **Broadcast / location-wide messaging** | Brief §3.1 — explicitly excluded | Jonathan narrowed this himself |
| **Dark mode, localisation** | doc 14 Q24–Q25 | Externalise strings now; translate later |

---

## Open commercial question that gates everything

From the brief's risk register:

> *"If Jonathan funds the build and intends to license the product, IP ownership, license
> terms and revenue share need to be settled in the commercial agreement — **before code
> exists, not after.**"*

This is not an engineering item, but it gates the licensing architecture that engineering
is being asked to build. If the ownership answer changes, the multi-tenancy mandate may
change with it. Settle it alongside Tuesday's scope conversation.
