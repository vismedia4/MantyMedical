# 09 — Screens: Office Admin

Desktop, left sidebar + content. Five screens. Same chrome as Manager, except the
header location control is a **dropdown** rather than a static label.

---

## A1 · Office Console
`screens/admin/01-console.png`

Title **Office Console**; subtitle *"Cross-location operational overview for office staff."*

### KPI row — four tiles

| Tile | Icon | Value |
|---|---|---|
| Locations | 🏢 | 5 |
| Active requests | 🚗 | 6 |
| Pending approvals | ☑ | 6 |
| Total customers | 👥 | 10 |

Large navy numeral over a slate label. Icon top-left, muted. Equal-width cards.

### By location

Card `BY LOCATION`, containing a responsive grid of per-location tiles:

```
┌───────────────────────────────────┐
│ Wacker Drive Garage               │  ← navy bold
│ 225 N. Wacker Dr, Chicago, IL     │  ← slate
│    3          3          4        │  ← navy numerals
│  ACTIVE   APPROVALS  CUSTOMERS    │  ← uppercase slate micro-labels
└───────────────────────────────────┘
```

Three metrics per location: active requests, pending approvals, customers. Zero-value
locations render identically with `0`s — no special empty treatment.

**Not shown:** tiles are not links. They should be *(proposed)* — drilling from a
portfolio number into the location is the obvious next action.

**Note the scoping subtlety:** the header shows a location dropdown, but this screen is
explicitly cross-location. Either the dropdown is inert here, or the console is
portfolio-wide regardless. Recommendation *(proposed)*: an **"All locations"** option in
the dropdown, selected by default on this screen.

---

## A2 · Users
`screens/admin/02-users.png`

Title **Users**; subtitle *"Manage staff and customer accounts across all locations."*

**Segmented control:** `Staff` (active, filled red, white text) | `Customers` (inactive,
white). The Customers tab is not captured — build it to the same table pattern.

**Action:** **+ Add staff** — bordered, right-aligned above the table.

**Table:** `Name` · `Role` · `Location(s)` · `Status` · `Action`

| Column | Rendering |
|---|---|
| Name | Navy bold. Station accounts read as posts: *"Wacker Drive Valet Station"* |
| Role | Slate. `Valet Account` · `Garage Manager` · `Office Admin` |
| Location(s) | Comma-joined, **wraps to multiple lines** — Paula Bennett lists all five |
| Status | `active` green pill |
| Action | `Reset password` (slate) · `Suspend` (red) |

The multi-location cells are the visible proof of the many-to-many model in doc 02.

**Must be built:** search/filter (unusable past ~50 staff), role filter, the Customers
tab, an edit-user view, confirmation on Suspend, and reactivation of a suspended user
(the action label must toggle to *Reactivate*).

---

## A3 · Locations
`screens/admin/03-locations-add.png` · `screens/admin/04-locations-list.png`

Title **Locations**; subtitle *"Manage Pioneer Parking properties across states. Each
location has an identifier type that drives what customers are asked for at sign-up,
plus an assigned garage manager."*

### Add a location

Card `ADD A LOCATION`.

| Field | Type | Notes |
|---|---|---|
| Location name | text | placeholder *"Location name (e.g., Aster Hall)"* |
| Address | text | |
| State | text | placeholder *"State (e.g., Illinois)"* |
| `Identifier` | select | **`Decal number`** default — drives customer sign-up |
| `Manager` | select | **`Unassigned`** default — pick an existing manager |
| **MANAGER ACCOUNT (OPTIONAL)** | fieldset | Manager name · Manager username · Manager password |
| **VALET ACCOUNT (OPTIONAL)** | fieldset | Valet station name · Valet username · Valet password |
| Submit | **+ Add location** — full-width filled red | |

Footnote, verbatim and load-bearing:

> A 6-digit Location Access Code is generated automatically — share it with customers to
> enroll. Manager and valet credentials you set here are provisioned immediately and
> handed over directly; nothing is emailed. Disabled locations are hidden from customer
> registration.

Two ways to staff a new location: assign an **existing** manager via the dropdown, or
create a **new** manager account inline. Both paths must work; the optional fieldsets
are for the second.

Passwords are set by the admin in a plain form and handed over verbally or on paper.
That is a deliberate operational choice for staff who may not have work email — but it
has real security consequences. See doc 13.

### Location cards

Two-column grid of cards.

```
┌────────────────────────────────────────────┐
│ WACKER DRIVE GARAGE                        │  ← uppercase navy
│ Illinois                                   │
│ 📍 225 N. Wacker Dr, Chicago, IL           │
│ ┌────────────────────────────────────────┐ │
│ │ 🔑 Access code  481027                 │ │  ← code in mono, tracked
│ │ ⧉ Copy  ↻ Regenerate      ⏻ Deactivate │ │
│ └────────────────────────────────────────┘ │
│ 👤 Manager: Karen Reed                     │
│ ┌────────────────────────────────────────┐ │
│ │ 🛡 SITE ACCOUNTS                        │ │
│ │ [Valet]  Wacker Drive Valet Station     │ │
│ │          @wacker-valet     Credentials  │ │
│ │ [Manager] Karen Reed                    │ │
│ │          @wacker-manager   Credentials  │ │
│ └────────────────────────────────────────┘ │
│   3            5         Decal number      │
│ ACTIVE USERS  VEHICLES    IDENTIFIER       │
│ ✎ Edit                        ⏻ Disable    │
└────────────────────────────────────────────┘
```

Observed identifier types across the portfolio: **Decal number** (garages),
**Apartment number** (River North Condos), **Stall number** (South Park Residences).

**Two different off-switches** — do not conflate them:

| Control | Scope | Effect |
|---|---|---|
| **Deactivate** | The access code | Stops new enrollment; existing customers unaffected |
| **Disable** | The whole location | Hidden from customer registration; service impact TBD |

Both need confirmation dialogs and a clear reactivation path. **Regenerate** must
invalidate the old code immediately and warn that printed codes will stop working.

The **Credentials** links reveal or reset station credentials — spec exactly what they
show, and log every reveal as an `ActivityEvent`.

---

## A4 · Activity History
`screens/admin/05-activity-history.png`

Title **Activity History**; subtitle *"Recent requests, status changes, and completed
pickups across all locations — for review and dispute resolution. (Advanced analytics
dashboards are out of scope.)"*

Card `RECENT ACTIVITY`, sort indicator `newest first` (right).

Each row: **status icon** (left, colour-coded) · **summary sentence** (navy) ·
**metadata line** (`{Location} · {actor role} · {relative time}`, muted).

| Icon | Colour | Verb |
|---|---|---|
| ⊕ | slate | `request.created` |
| ⇄ | amber | `request.accepted`, `request.ready` |
| ✓ | green | `request.completed` |

Summaries are natural-language sentences, not field dumps:

- *"Michael Torres requested their Toyota Camry"* — Wacker Drive Garage · customer · 12 minutes ago
- *"Denise Johnson's Ford Escape marked ready for pickup"* — State Street Garage · valet · 16 minutes ago
- *"Valet accepted Linda Nguyen's Honda CR-V"* — Wacker Drive Garage · valet · 18 minutes ago
- *"Pickup completed for Michael Torres"* — Wacker Drive Garage · manager · 23 hours ago

**Note the last one:** completed by *manager*, not valet — evidence that the manager
status override is the path to `completed` in the prototype. See doc 04, gap (a).

The parenthetical *"(Advanced analytics dashboards are out of scope.)"* is a scope
boundary written by the product owner into the UI. Respect it: this is a legible feed,
not a BI surface.

**Must be built:** filters (location, role, verb, date range), search by customer or
vehicle, pagination, and — given the dispute-resolution mandate — a permalink per event
*(proposed)*.

---

## A5 · Settings & Operational Policies
`screens/admin/06-settings-policies.png`

Title **Settings & Operational Policies**; subtitle *"System-wide operational settings.
(Policy toggles are representative; sound settings are saved.)"*

> The parenthetical is an admission that the policy toggles were **not functional in the
> prototype**. They are still specified behavior — build them.

### Card `OPERATIONAL POLICIES` — four toggles, all default on

| Toggle | Sub-copy | Governs |
|---|---|---|
| **Require manager approval for new customers** | *"New registrations stay pending until a garage manager approves."* | Onboarding, doc 04 §2 |
| **Require approval for vehicle changes** | *"Customer-submitted vehicle changes need manager approval before taking effect."* | Approvals, doc 04 §3 |
| **Retain completed requests ~7 days** | *"Completed request history is visible to staff for about a week."* | Retention, doc 04 §6 |
| **Internal operational notes** | *"Staff-only notes on customers/vehicles, visible to valet and manager."* | Notes feature flag |

The third is a toggle in the prototype but its label carries a number ("~7 days"). It
should be a **numeric setting**, not a boolean *(proposed)* — otherwise "off" has no
defined meaning (retain forever? never?).

Note the fourth toggle's copy says notes are on *"customers/vehicles"*, while the valet
UI renders notes inside the *request* modal. Corroborates the doc 03 recommendation to
attach notes to the vehicle.

### Card `VALET REQUEST CHIME`

Identical to the Manager settings block (doc 08 · M6): enabled toggle, repeat interval,
volume, and the same governing note about valets being unable to disable it.

**Scope question:** policies read as system-wide; the chime block sits under a header
location dropdown. Recommendation *(proposed)*: implement everything as **system default
with per-location override**, and label each control with its effective scope. This
satisfies both screens and avoids a migration when the first location asks for an
exception.
