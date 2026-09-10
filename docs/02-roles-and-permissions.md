# 02 — Roles & Permissions

> Requirements authority is [00 — Client Requirements](00-client-requirements.md) §5–6.
> The valet phone-number restriction and the manager-absence backup below are
> client-stated requirements, not inferences.

Four roles, confirmed in the requirements session with explicit scope and permission
statements for each.

| Role | Prototype account | One-line charter | Scope |
|---|---|---|---|
| **Customer** | `mtorres` | Vehicle owner | Own account + own vehicles, at one location |
| **Valet** | `wacker-valet` | Operational queue | One location, operational data only |
| **Garage Manager** | `wacker-manager` | Location oversight | One or more assigned locations |
| **Office Admin** | `admin` | System administration | All locations |

## Tenancy model

Three scoping axes that must be enforced server-side on every request:

0. **Tenant scoping.** The product is designed for licensing to other parking operators,
   so a `Tenant` sits above `Location`. Pioneer Parking is tenant #1. No query may cross
   a tenant boundary, ever. Build the isolation now; defer per-tenant theming and any
   operator-facing admin surface. *(Client mandate — doc 00 §6.3.)*
1. **Location scoping.** Nearly every record belongs to a `location_id`. Valets and
   customers see exactly one location. Managers see their assigned set — the
   prototype shows Hector Flores assigned to *State Street Garage, River North Condos*,
   so **manager-to-location is many-to-many**. Office Admin sees all.
2. **Ownership scoping.** A customer sees only their own vehicles and requests, never
   another customer's, and never staff-only fields.

A customer record belongs to **exactly one location** — *"location-specific customer
databases; records are scoped to the garage."*

Location scoping is *not* a UI concern. The header location pickers on the Manager and
Admin screens are a view filter over an already-authorized set.

## Permission matrix

Legend: ● full · ◐ limited (see note) · ○ none

| Capability | Customer | Valet | Manager | Admin |
|---|:--:|:--:|:--:|:--:|
| **Requests** | | | | |
| Create retrieval request (own vehicle) | ● | ○ | ○ | ○ |
| Cancel own pending request | ● | ○ | ○ | ○ |
| Schedule a future pickup | ● | ○ | ○ | ○ |
| View own request status | ● | — | — | — |
| View location request queue | ○ | ● | ● | ● |
| Accept a request | ○ | ● | ○ | ○ |
| Mark ready / complete | ○ | ● | ○ | ○ |
| Revert request to pending | ○ | ● | ● | ● |
| **Override** any request status | ○ | ○ | ● | ● |
| Promote future request to active | ○ | ● | ◐ | ◐ |
| **Vehicles & customers** | | | | |
| Add a vehicle | ◐¹ | ○ | ● | ● |
| Edit own vehicle details | ◐¹ | ○ | ● | ● |
| View registered customers at location | ○ | ◐² | ● | ● |
| View registered vehicles at location | ○ | ◐² | ● | ● |
| Create a customer account directly | ○ | ○ | ● | ● |
| Approve / reject registrations | ○ | ○ | ● | ● |
| Approve / reject vehicle changes | ○ | ○ | ● | ● |
| **Act on approvals during manager absence** | ○ | ○ | — | ● |
| **Staff-only operational data** | | | | |
| Read/write parking location field | ○ | ● | ● | ● |
| Read/write internal operational notes | ○ | ● | ● | ● |
| **View customer phone number** | ● own | **○** | ● | ● |
| Set notification preferences | ● | ○ | ○ | ○ |
| **Administration** | | | | |
| View request history | ○ | ◐² (2–3 days) | ● (30 days, proposed) | ● (full archive) |
| View cross-location activity feed | ○ | ○ | ○ | ● |
| Manage valet station accounts | ○ | ○ | ◐³ | ● |
| Manage staff users / roles | ○ | ○ | ○ | ● |
| Create / edit / disable locations | ○ | ○ | ○ | ● |
| Regenerate location access code | ○ | ○ | ○ | ● |
| Change chime settings | ○ | **○** | ● | ● |
| Change system operational policies | ○ | ○ | ○ | ● |

¹ Subject to manager approval when the corresponding policy is on. Customer-submitted
adds and edits enter a pending state; they do not take effect immediately.
² **View only, and phone numbers excluded.** The Valet menu states it outright:
*"View only — valets can review this information but cannot change records or settings."*
The client added a hard restriction on top: valets **cannot view customer phone
numbers**. See below.
³ Manager can suspend, reactivate, reset the password of, and add valet accounts **at
their own location(s)**. Only Admin creates location-level accounts at provisioning time.

## Three permission rules worth calling out

**Valets cannot silence the chime.** Stated verbatim on both the Manager and Admin
settings screens: *"Only Garage Managers and System Administrators can change these
settings — valets cannot turn alerts off."* This is a deliberate anti-abuse control
on a shared kiosk account, not a UI oversight. Enforce it server-side.

**Staff-only fields are staff-only.** Internal notes carry the label *"Visible to
valet, manager, and admin — never to customers."* Parking location is labeled
`PARKING LOCATION · STAFF ONLY`. These must never appear in a customer-facing API
response. See [11 — API Contract](11-api-contract.md) for the serializer split.

**Valets cannot see customer phone numbers.** Client-stated privacy restriction:

> *"CANNOT: edit customer or vehicle data; view customer phone numbers — called out by
> Jonathan as a privacy restriction. Phone access is preserved for authentication and
> management at higher role levels."*

The prototype's valet request-detail modal **shows the phone number**. That is a defect
against this requirement and has been removed from the spec (doc 07 · V2). The staff
serializer must split into a valet tier and a manager tier — see doc 11.

This creates a real operational consequence: the phone was the fallback when the app
fails. The replacement escalation path is an open question — doc 14, Q7.

## Manager-absence backup — the client's one flagged gap

> *"FLAGGED: must be able to intervene when a garage manager is unavailable — Jonathan's
> single flagged gap in the prototype. **Pending approvals must not stall on manager
> absence.**"*

This was the only substantive objection raised across the entire prototype walkthrough,
which makes it the highest-signal requirement in the brief.

The Office Admin already holds every manager permission by scope. What is missing is the
**mechanism**: nothing today tells anyone that a manager has gone quiet, and nothing
routes a stalled approval anywhere else. Required design, specified in
[04 — Workflows](04-workflows-and-state.md) §7:

- An **SLA on pending approvals** — how long before one is considered stalled
- **Who is notified** when the SLA is breached
- Whether approvals **escalate automatically** to the Office Admin or require a pull
- A visible **"awaiting escalation"** state so nothing sits invisibly

Do not treat this as satisfied by the admin merely *having* the permission.

## Account types

The prototype distinguishes **personal accounts** from **shared station accounts**:

- **Personal** — Customers, Garage Managers, Office Admins. One human, one login.
- **Shared station** — Valet accounts. Named for the post, not the person:
  *"Wacker Drive Valet Station"* / `@wacker-valet`. The account is the tablet.

Naming convention across all five locations is `@{location-slug}-valet` and
`@{location-slug}-manager`. Provisioning is manual and offline: *"Manager and valet
credentials you set here are provisioned immediately and handed over directly;
nothing is emailed."*

> **Data inconsistency in the prototype seed:** River North Condos lists its valet as
> `@rivernorth-valet` but its manager account as `@state-manager` — the same account
> shown at State Street Garage. This is consistent with Hector Flores managing both
> locations under one login, which supports the many-to-many manager↔location model
> above. Confirm the intent rather than copying the seed data. Logged in
> [14 — Open Questions](14-open-questions.md).

## Role switching in the prototype

Every screen carries a `Viewing as [role ▾]` control in the header, and the landing
page offers *"PROTOTYPE DEMO — JUMP TO A ROLE."* **This is a demo affordance and must
not ship.** Real role assignment comes from the authenticated principal. If an
impersonation feature is wanted for support, spec it separately with an audit trail.
