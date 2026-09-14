# 03 — Domain Model

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

> Requirements authority is [00 — Client Requirements](00-client-requirements.md).
> Changes made against the prototype: vehicle photos replaced by generic images (§4.1),
> permanent backend retention (§4.4), tenant layer for licensing (§6.3), notification
> preferences (§6.4).

## Entity relationship

```
                          ┌──────────────┐
                          │    Tenant    │  operator (Pioneer = tenant #1)
                          └──────┬───────┘
                                 │
                          ┌──────▼───────┐
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

## Tenant

The licensing root. **Required from day one** — the client's mandate is to design the
product for licensing to other parking operators, and tenant isolation is cheap now and
expensive later.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `name` | string | "Pioneer Parking" — tenant #1 |
| `slug` | string | Used for scoping, never shown to customers |
| `theme` | json | **Seam only.** Populate with Pioneer's palette; do not build a theming UI in MVP |
| `status` | enum | `active` \| `suspended` |

Every table below carries `tenant_id`, and every query is scoped to it. Enforce at the
data-access layer, not in controllers — a single missed `WHERE` in a licensed product is
a cross-operator data leak.

**Do not name anything after Pioneer.** Not tables, not API paths, not enum values, not
CSS classes. Brand lives in `Tenant.theme` and nowhere else. *"Company structure, product
name and branding must stay flexible."*

---

## Location

The operational root within a tenant. Everything operational hangs off it.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `tenant_id` | fk Tenant | |
| `name` | string | "Wacker Drive Garage" |
| `address` | string | "225 N. Wacker Dr, Chicago, IL" |
| `state` | string | Surfaced as a grouping label on the location card |
| `identifier_type` | enum | `decal_number` \| `apartment_number` \| `stall_number` — **drives the customer sign-up form** |
| `access_code` | string(6) | 6-digit numeric, auto-generated, regenerable |
| `access_code_active` | bool | "Deactivate" hides the location from customer registration |
| `manager_id` | fk User | Primary assigned manager, shown as `Manager: Karen Reed` |
| `status` | enum | `active` \| `disabled` |
| `created_at` | ts | |

`identifier_type` is client-confirmed: *"Simple location setup with one primary
identifier per location: decal number, apartment number or unit number, whichever that
property uses."* **Model it as a lookup table, not a hard enum** *(proposed)* — a
licensed operator will bring a label Pioneer never used.

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
screen shows one attendant at two locations and another at every location.

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
| `identifier` | string | `PP-1042` — semantics come from `location.identifier_type`. **Entered by the customer at registration**, verified by the manager at approval |
| `image_key` | string | **Derived, never uploaded.** Resolved from make + model + colour against the generic-image mapping set |
| `status` | enum | `pending_approval` \| `active` \| `rejected` |
| `created_at` | ts | |

Display name is composed, not stored: **`{color} {make} {model}`** → *"Silver Toyota
Camry"*, *"Forest Green Rivian R1S"*. Consistent across all four roles' screens.

Identifiers observed follow `PP-####` at garage locations. Whether that prefix is a
Pioneer Parking convention or free text is unresolved — see doc 14.

A customer may hold multiple vehicles (Grace Kim: *Subaru Outback, Tesla Model Y*) —
client-confirmed.

### Generic vehicle images — a client requirement, and a real deliverable

> *"Generic vehicle images. No customer photo uploads. The system auto-generates or maps
> a generic image from make, model and color. Rationale: reduces data load and avoids
> privacy exposure. VisualMedia to define the brand / model / color to image mapping set."*

There is **no photo upload anywhere in this product.** The prototype's `Add photo`
control and `No photo` placeholder are both removed.

```
  (make, model, color)  ──►  resolver  ──►  image_key  ──►  rendered asset
     "Toyota","Camry","Silver"          "sedan/silver"
```

Design the resolver as **body-style + colour**, not make + model *(proposed)*. A
per-model asset library is unbounded and will never be complete; a dozen body styles
(sedan, SUV, pickup, van, coupe, hatchback, wagon, EV-crossover…) crossed with a
standard colour set covers the entire vehicle population with ~150 assets and degrades
gracefully to a neutral silhouette on an unknown input.

Store the *inputs* and resolve at render time so the mapping can improve without a data
migration. This is VisualMedia action item 04 and has a long tail — start it early.

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
Bucketing, the *"Later today"* quick option, and the history view window must all
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

### Retention is permanent — the UI window is not

> *"Full historical activity retained **permanently** in the backend repository.
> Purposes: metrics and reporting, customer complaints, legal support, and
> vehicle-related disputes."*
> *"Split from the UI: the valet-facing interface shows only recent activity (2–3 days);
> retention happens behind it."*

Two independent settings, not one:

| Setting | Value | Meaning |
|---|---|---|
| `valet_history_visible_days` | **2–3** (client-stated) | What drops off the valet board |
| Backend retention | **Indefinite** | What the business keeps for disputes and legal |

The prototype's "~7 days" copy is superseded. Nothing is deleted; the *view* is
windowed. This obligates a written retention and access policy — see doc 13 §4.

---

## NotificationPreference

New scope from the brief. Per customer.

| Field | Type | Default | Notes |
|---|---|---|---|
| `user_id` | fk User | | |
| `notify_ready` | bool | `true` | **Required notification.** Consider making it non-disableable |
| `notify_retrieving` | bool | `false` | Opt-in — *"customers may opt in to 'Retrieving Vehicle' status updates"* |
| `push_token` | string? | | Device token; push is the only channel |

> *"Notify on 'Ready' as the default. The customer's required notification is when the
> vehicle is ready."* — treat `notify_ready` as effectively mandatory; a customer who
> disables it defeats the product's purpose. Recommendation *(proposed)*: not toggleable
> in MVP.

---

**`OperationalPolicy`** — system-wide, Admin only. All four default to on.

| Key | Effect |
|---|---|
| `require_manager_approval_new_customers` | New registrations stay `pending` until approved |
| `require_approval_vehicle_changes` | Customer vehicle edits need approval before taking effect |
| `valet_history_visible_days` | Completed history visible on the valet board — **client says 2–3 days**, not 7. Backend retention is separate and permanent |
| `internal_operational_notes_enabled` | Staff-only notes feature flag |

The Admin settings page carries the caveat *"Policy toggles are representative; sound
settings are saved."* — meaning the policy toggles were **not wired up in the
prototype**. They are nonetheless specified behavior; build them.

Scope is ambiguous: policies read system-wide, chime reads per-location.
Recommendation *(proposed)*: make all of them **system default + per-location
override**, which satisfies both screens without a schema change later.
