# 09 — Screens: Office Admin

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
> **Added:** an escalated-approvals queue for the manager-absence backup (§6.1), the
> client's single flagged prototype gap. Retention copy corrected (§4.4).

Desktop, left sidebar + content. Six screens. Same chrome as Manager, except the
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

**Add a fifth tile: `Escalated approvals`** *(client requirement)*. Approvals past their
SLA because a manager is unavailable must be visible to the office at a glance, and
actionable — this is the mechanism behind *"pending approvals must not stall on manager
absence."* Style it as the alarm state: when non-zero, red numeral and a link into A6.

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
| Location(s) | Comma-joined, **wraps to multiple lines** — an office admin may list every location |
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

**Must be built:** filters (location, role, verb, date range), first-name search,
pagination, and — given the dispute-resolution mandate — a permalink per event
*(proposed)*.

**This feed is the permanent record.** The client retains full historical activity
indefinitely for *"metrics and reporting, customer complaints, legal support, and
vehicle-related disputes."* Unlike the valet board and manager history, **nothing here
expires.** Build it to page over years, not days, and log escalations and admin
overrides into it as first-class events.

---

## A5 · Settings & Operational Policies
`screens/admin/06-settings-policies.png`

Title **Settings & Operational Policies**; subtitle *"System-wide operational settings.
(Policy toggles are representative; sound settings are saved.)"*

> The parenthetical is an admission that the policy toggles were **not functional in the
> prototype**. They are still specified behavior — build them.

### Card `OPERATIONAL POLICIES` — four toggles, all default on

Plus two new settings required by the brief *(client requirement)*:

| Setting | Type | Default | Governs |
|---|---|---|---|
| **Approval SLA — new registrations** | Duration | 4 business hours | When an approval escalates to the office (doc 04 §6) |
| **Approval SLA — vehicle changes** | Duration | 24 hours | As above, slower — a colour change is not time-sensitive |

| Toggle | Sub-copy | Governs |
|---|---|---|
| **Require manager approval for new customers** | *"New registrations stay pending until a garage manager approves."* | Onboarding, doc 04 §2. **Keep on by default** — it is the compensating control for a 6-digit access code (doc 13 §3) |
| **Require approval for vehicle changes** | *"Customer-submitted vehicle changes need manager approval before taking effect."* | Approvals, doc 04 §3 |
| **Retain completed requests ~7 days** | *"Completed request history is visible to staff for about a week."* | **Superseded** — 2–3 days for the valet view, permanent in the backend. See below and doc 04 §8 |
| **Internal operational notes** | *"Staff-only notes on customers/vehicles, visible to valet and manager."* | Notes feature flag |

The third is wrong on two counts. It is a toggle whose label carries a number, and the
number is wrong: **the client stated 2–3 days for the valet view**, and backend retention
is **permanent**. Replace it with a numeric `valet_history_visible_days` setting
(default 3) and add a read-only line stating that full history is retained indefinitely
in the system of record — so nobody mistakes a view window for a deletion policy.

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


---

## A6 · Escalated Approvals *(new — client requirement)*

Not in the prototype. This screen exists because of the client's single flagged gap:

> *"Must be able to intervene when a garage manager is unavailable … **Pending approvals
> must not stall on manager absence.**"*

| Element | Spec |
|---|---|
| Title | **Escalated Approvals** |
| Subtitle | *"Approvals that have passed their response window, or whose manager is marked away."* |
| Grouping | By location, most-overdue first |
| Row | Approval kind badge · subject · location · **time overdue** (red) · manager name and availability |
| Actions | **✓ Approve** · **✕ Reject** · **Nudge manager** |

Rules:

- An approval reaches this queue **automatically** on SLA breach, or **immediately** when
  its manager is marked away (doc 08 · M7). Automatic, not pull — a queue that depends on
  someone noticing reproduces the exact failure being fixed.
- The manager keeps the ability to act after escalation. Escalation widens who can act;
  it never locks the manager out. Handle the race: first decision wins, second sees the
  outcome.
- Every escalation and every admin decision writes an `ActivityEvent` naming the actor
  and the reason (`sla_breach` / `manager_away`).
- Notify the Office Admin on escalation — this is one of the few push-worthy staff events.

Also surfaced as a KPI tile on A1 and as a sidebar badge, so an admin who never opens
this screen still sees the count.
