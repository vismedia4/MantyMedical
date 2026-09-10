# 02 — Roles & Permissions

Four roles. The prototype's sign-in screen enumerates them with demo credentials,
which conveniently double as a naming convention.

| Role | Prototype account | One-line charter | Scope |
|---|---|---|---|
| **Customer** | `mtorres` | Vehicle owner | Own account + own vehicles, at one location |
| **Valet** | `wacker-valet` | Operational queue | One location, operational data only |
| **Garage Manager** | `wacker-manager` | Location oversight | One or more assigned locations |
| **Office Admin** | `admin` | System administration | All locations |

## Tenancy model

Two scoping axes that must be enforced server-side on every request:

1. **Location scoping.** Nearly every record belongs to a `location_id`. Valets and
   customers see exactly one location. Managers see their assigned set — the
   prototype shows Hector Flores assigned to *State Street Garage, River North Condos*,
   so **manager-to-location is many-to-many**. Office Admin sees all.
2. **Ownership scoping.** A customer sees only their own vehicles and requests, never
   another customer's, and never staff-only fields.

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
| Upload vehicle photo | ● | ○ | ● | ● |
| View registered customers at location | ○ | ◐² | ● | ● |
| View registered vehicles at location | ○ | ◐² | ● | ● |
| Create a customer account directly | ○ | ○ | ● | ● |
| Approve / reject registrations | ○ | ○ | ● | ● |
| Approve / reject vehicle changes | ○ | ○ | ● | ● |
| **Staff-only operational data** | | | | |
| Read/write parking location field | ○ | ● | ● | ● |
| Read/write internal operational notes | ○ | ● | ● | ● |
| **Administration** | | | | |
| View request history (~7 days) | ○ | ◐² | ● | ● |
| View cross-location activity feed | ○ | ○ | ○ | ● |
| Manage valet station accounts | ○ | ○ | ◐³ | ● |
| Manage staff users / roles | ○ | ○ | ○ | ● |
| Create / edit / disable locations | ○ | ○ | ○ | ● |
| Regenerate location access code | ○ | ○ | ○ | ● |
| Change chime settings | ○ | **○** | ● | ● |
| Change system operational policies | ○ | ○ | ○ | ● |

¹ Subject to manager approval when the corresponding policy is on. Customer-submitted
adds and edits enter a pending state; they do not take effect immediately.
² **View only.** The Valet menu states it outright: *"View only — valets can review
this information but cannot change records or settings."*
³ Manager can suspend, reactivate, reset the password of, and add valet accounts **at
their own location(s)**. Only Admin creates location-level accounts at provisioning time.

## Two permission rules worth calling out

**Valets cannot silence the chime.** Stated verbatim on both the Manager and Admin
settings screens: *"Only Garage Managers and System Administrators can change these
settings — valets cannot turn alerts off."* This is a deliberate anti-abuse control
on a shared kiosk account, not a UI oversight. Enforce it server-side.

**Staff-only fields are staff-only.** Internal notes carry the label *"Visible to
valet, manager, and admin — never to customers."* Parking location is labeled
`PARKING LOCATION · STAFF ONLY`. These must never appear in a customer-facing API
response. See [11 — API Contract](11-api-contract.md) for the serializer split.

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
