# 03 — Domain Model

## Entity relationship

```
                          ┌──────────────┐
                          │   Location   │  identifier_type, access_code
                          └──────┬───────┘
             ┌───────────────────┼───────────────────┬──────────────────┐
             │                   │                   │                  │
      ┌──────▼──────┐    ┌───────▼────────┐   ┌──────▼──────┐   ┌───────▼───────┐
      │  UserRole   │    │ StationAccount │   │  Customer   │   │ ChimeSettings │
      │ (M:N staff) │    │ valet | manager │   │  (profile)  │   │  (per-loc)    │
      └──────┬──────┘    └────────────────┘   └──────┬──────┘   └───────────────┘
             │                                       │
      ┌──────▼──────┐                         ┌──────▼──────┐
      │    User     │                         │   Vehicle   │ make, model, color,
      │ (principal) │                         │             │ identifier, photo
      └─────────────┘                         └──────┬──────┘
                                                     │
                          ┌──────────────────────────┼───────────────────┐
                          │                          │                   │
                 ┌────────▼────────┐        ┌────────▼────────┐  ┌───────▼───────┐
                 │ RetrievalRequest│        │ ApprovalRequest │  │ VehicleNote   │
                 │ status, type,   │        │ kind, payload,  │  │ (staff only)  │
                 │ scheduled_for   │        │ decision        │  └───────────────┘
                 └────────┬────────┘        └─────────────────┘
                          │
                 ┌────────▼────────┐
                 │  ActivityEvent  │  append-only audit log
                 └─────────────────┘
```

---

## Location

The tenancy root. Everything hangs off it.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `name` | string | "Wacker Drive Garage" |
| `address` | string | "225 N. Wacker Dr, Chicago, IL" |
| `state` | string | Surfaced as a grouping label on the location card |
| `identifier_type` | enum | `decal_number` \| `apartment_number` \| `stall_number` — **drives the customer sign-up form** |
| `access_code` | string(6) | 6-digit numeric, auto-generated, regenerable |
| `access_code_active` | bool | "Deactivate" hides the location from customer registration |
| `manager_id` | fk User | Primary assigned manager, shown as `Manager: Karen Reed` |
| `status` | enum | `active` \| `disabled` |
| `created_at` | ts | |

`identifier_type` is presented in the Add Location form as a simple `Identifier`
dropdown and rendered on the location card as a labeled stat. **Model it as a
lookup table, not a hard enum** *(proposed)* — new property types will want new
labels, and this is the cheapest possible extension point.

Access codes must be **unique across active locations** *(inferred)* — a customer
enters only the code at sign-up, so a collision would route them to the wrong
property. Reuse of a deactivated code should be blocked *(proposed)*.

---

## User

One principal table with a role, rather than four tables *(proposed)*.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `name` | string | "Karen Reed" / "Wacker Drive Valet Station" |
| `username` | string | `@wacker-valet`, `mtorres` |
| `email` | string | Present for customers (`s.alvarez@example.com`); optional for stations |
| `phone` | string | Customers: `(312) 555-0142`. Shown to valets on request detail |
| `role` | enum | `customer` \| `valet` \| `garage_manager` \| `office_admin` |
| `account_kind` | enum | `personal` \| `station` *(inferred — see §Account types in doc 02)* |
| `status` | enum | `pending` \| `active` \| `suspended` |
| `password_reset_required` | bool | *(proposed)* — supports the "Reset password" action |

**`UserLocation`** join table: `user_id`, `location_id`. Required because the Users
screen shows Hector Flores at two locations and Paula Bennett at all five.

Status transitions observed: new customers land in `pending` and become `active` on
manager approval. Staff have `Suspend` / reactivate. `Reset password` is an action on
every staff row.

---

## Vehicle

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `customer_id` | fk User | |
| `location_id` | fk Location | Denormalized from customer *(proposed)* — simplifies queue queries |
| `make` | string | "Toyota" |
| `model` | string | "Camry" |
| `color` | string | "Silver" |
| `identifier` | string | `PP-1042` — semantics come from `location.identifier_type` |
| `photo_url` | string? | Optional. Empty state renders a `No photo` placeholder tile |
| `status` | enum | `pending_approval` \| `active` \| `rejected` |
| `created_at` | ts | |

Display name is composed, not stored: **`{color} {make} {model}`** → *"Silver Toyota
Camry"*, *"Forest Green Rivian R1S"*. Consistent across all four roles' screens.

Identifiers observed follow `PP-####` at garage locations. Whether that prefix is a
Pioneer Parking convention or free text is unresolved — see doc 14.

A customer may hold multiple vehicles (Grace Kim: *Subaru Outback, Tesla Model Y*).

---

## RetrievalRequest

The central operational record.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `vehicle_id` | fk Vehicle | |
| `customer_id` | fk User | Denormalized for the queue |
| `location_id` | fk Location | |
| `type` | enum | `immediate` \| `scheduled` |
| `status` | enum | `pending` \| `accepted` \| `ready` \| `completed` \| `cancelled` |
| `requested_at` | ts | Drives *"5 minutes ago"* on queue cards |
| `scheduled_for` | ts? | Set when `type = scheduled` |
| `accepted_at` | ts? | |
| `ready_at` | ts? | |
| `completed_at` | ts? | Shown in Request History: *"Sep 9, 2026 at 5:18 PM"* |
| `parking_location` | string? | **Staff-only.** Free text: *"2F · Red zone"*, *"Level 2 West"* |
| `cancelled_by` | fk User? | |

**Timing labels.** Immediate requests display *"needs it ASAP"* on the queue and
`Now` in Request History. Scheduled requests display the absolute datetime.

**Bucketing is derived, not stored.** The valet board's `Tomorrow's Pickups` and
`Future Pickups` columns are computed from `scheduled_for` against the location's
local date. Do not persist a bucket column — it goes stale at midnight.

**Timezone matters.** Locations span Chicago (CT), Orlando (ET), and New York (ET).
Bucketing, the *"Later today"* quick option, and the ~7-day retention window must all
evaluate in **location-local time**. Store UTC, render and bucket local.

---

## ApprovalRequest

One table, three kinds — the Pending Approvals screen groups by exactly these:

| `kind` | Trigger | Payload | Prototype example |
|---|---|---|---|
| `new_registration` | Customer signs up while the policy is on | Prospective customer profile | Sofia Alvarez, `s.alvarez@example.com`, *submitted 1 hour ago* |
| `vehicle_change` | Customer edits an existing vehicle | Field-level diff | Linda Nguyen — `color: ~~Blue~~ → Graphite` |
| `new_vehicle` | Customer adds a vehicle | Full proposed vehicle | Michael Torres — *Adding Forest Green Rivian R1S · PP-1310* |

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `kind` | enum | above |
| `location_id` | fk Location | Routes it to the right manager's queue |
| `subject_user_id` | fk User | Who it's about |
| `subject_vehicle_id` | fk Vehicle? | Null for `new_registration` |
| `payload` | json | Proposed values / diff |
| `status` | enum | `pending` \| `approved` \| `rejected` |
| `submitted_at` | ts | Rendered as *"submitted 48 minutes ago"* |
| `decided_by` | fk User? | |
| `decided_at` | ts? | |

**Store the diff, not just the result.** The prototype renders vehicle changes as a
strikethrough old value → new value. That presentation requires the before-state to be
retained on the approval record — the live row must not be mutated until approval.

`new_registration` offers three actions — **Review**, Approve, Reject — where the other
two kinds offer only Approve/Reject. Review opens the full submitted profile
*(inferred; the prototype does not show the destination)*.

---

## Staff-only annotations

**`VehicleNote` / `RequestNote`** — free-text operational notes. Placeholder text in
the prototype defines the intent: *"pickup preferences, vehicle reminders (e.g. 'plug
in EV after return', 'leave key in vehicle'), and operational instructions."*

| Field | Type |
|---|---|
| `id` | uuid |
| `request_id` **or** `vehicle_id` | fk |
| `author_id` | fk User |
| `body` | text |
| `created_at` | ts |

> **Unresolved and worth deciding early:** the note UI is rendered inside the *request*
> detail modal, but the example content ("plug in EV after return") is clearly about the
> *vehicle* and should outlive any single request. Recommendation *(proposed)*: attach
> notes to the **vehicle**, and surface them in request detail. See doc 14.

---

## ActivityEvent

Append-only audit log powering the Admin activity feed and, by extension, dispute
resolution.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `location_id` | fk Location | Feed line 2: *"Wacker Drive Garage"* |
| `actor_id` | fk User | |
| `actor_role` | enum | Feed line 2: *"customer"* / *"valet"* / *"manager"* |
| `verb` | enum | `request.created`, `request.accepted`, `request.ready`, `request.completed`, `approval.decided`, … |
| `subject_type` / `subject_id` | polymorphic | |
| `summary` | string | Denormalized display string |
| `occurred_at` | ts | Feed sorts newest first |

Observed feed entries map cleanly to verbs:

| Rendered | Verb |
|---|---|
| "Michael Torres requested their Toyota Camry" | `request.created` |
| "Denise Johnson's Ford Escape marked ready for pickup" | `request.ready` |
| "Valet accepted Linda Nguyen's Honda CR-V" | `request.accepted` |
| "Pickup completed for Michael Torres" | `request.completed` |

**Denormalize `summary` at write time.** Names and vehicles change; the audit log must
show what was true when the event happened.

---

## Configuration entities

**`ChimeSettings`** — per location (the Manager settings screen scopes to one
location; the Admin screen shows the same block under a location selector).

| Field | Type | Default observed |
|---|---|---|
| `location_id` | fk | |
| `enabled` | bool | `true` |
| `repeat_interval_seconds` | int | `6` |
| `volume` | enum | `low` \| `medium` \| `high` → `medium` |

**`OperationalPolicy`** — system-wide, Admin only. All four default to on.

| Key | Effect |
|---|---|
| `require_manager_approval_new_customers` | New registrations stay `pending` until approved |
| `require_approval_vehicle_changes` | Customer vehicle edits need approval before taking effect |
| `retain_completed_requests_days` | Completed history visible to staff (~7 days) |
| `internal_operational_notes_enabled` | Staff-only notes feature flag |

The Admin settings page carries the caveat *"Policy toggles are representative; sound
settings are saved."* — meaning the policy toggles were **not wired up in the
prototype**. They are nonetheless specified behavior; build them.

Scope is ambiguous: policies read system-wide, chime reads per-location.
Recommendation *(proposed)*: make all of them **system default + per-location
override**, which satisfies both screens without a schema change later.
