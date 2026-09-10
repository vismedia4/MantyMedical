# 08 — Screens: Garage Manager

Desktop, left sidebar + content. Six screens.

**Shared chrome** — page title top-left; `📍 {Location}` and `👁 Viewing as ▾` top-right;
content on the neutral page background with white cards. Sidebar per doc 05.

---

## M1 · Dashboard
`screens/manager/01-dashboard.png`

Title **Manager Dashboard**. Three stacked blocks.

### Approvals callout

Amber-tinted bar, full width:
**`3`** *item(s) awaiting your approval* … `Review Pending Approvals →` (red link, right).
Hidden when the count is zero *(inferred)*.

### Active requests

Card titled `ACTIVE REQUESTS`, with the caption `Override status if needed` right-aligned.

| Column | Content |
|---|---|
| Primary | **{Customer full name}** · {Make} {Model} — name bold navy, vehicle slate |
| Secondary | `{identifier} · {relative time}` — muted |
| Status | Read-only badge (`Accepted` amber / `Pending` grey) |
| Control | **Status dropdown** — the override |

The badge and the dropdown both appear, showing the same value. The badge is the
current truth; the dropdown is the manual override. **This is the manager's core
operational power**: when the board is wrong — a valet forgot to tap Ready, a customer
called the office — the manager corrects it directly.

Every override must write an `ActivityEvent` recording who changed what, from what, to
what. This is precisely the audit case that justifies the log.

### Upcoming pickups

Card titled `UPCOMING PICKUPS`, caption `Tomorrow & future`.

| Column | Content |
|---|---|
| Primary | **{Customer}** · {Vehicle} |
| Secondary | `{identifier}` |
| Badge | `Future` (grey) / `Tomorrow` (amber) |
| Right | Absolute datetime — *"Sep 14, 2026 at 12:00 PM"* |

**Not shown:** any today/completed counts, and no link into the live valet board. A
manager reading "3 pending" has no way to see the board their valet sees.
Recommendation *(proposed)*: give managers read access to the queue board.

---

## M2 · Pending Approvals
`screens/manager/02-pending-approvals.png`

Title **Pending Approvals**. Three cards, one per approval kind, each headed
`{LABEL} ({count})`. Cards render even at zero *(inferred)*.

| Card | Row content | Actions |
|---|---|---|
| `NEW REGISTRATIONS` | 👤+ avatar · **Sofia Alvarez** · `s.alvarez@example.com · submitted 1 hour ago` | **✎ Review** · **✓ Approve** · **✕ Reject** |
| `VEHICLE CHANGE REQUESTS` | 🚗 avatar · **Linda Nguyen** · `color: ~~Blue~~ → Graphite` | **✓ Approve** · **✕ Reject** |
| `NEW VEHICLE REQUESTS` | 🚙 avatar · **Michael Torres** · *Adding* **Forest Green Rivian R1S** `· PP-1310 · submitted 48 minutes ago` | **✓ Approve** · **✕ Reject** |

**Button styling** — Approve: green text on pale green. Reject: red text on pale red.
Both are tinted, not filled: they are peers, and neither should feel like the default.

**The diff rendering is the specification.** `color: ~~Blue~~ → Graphite` — old value
struck through, arrow, new value in navy. Reproduce this for every changed field; a
manager approving a change must see exactly what changes. Multi-field diffs stack.

Circular avatars are tinted by kind (grey / amber / red) — a fast visual sort.

**Must be built:**
- The **Review** destination — full submitted profile with Approve/Reject in context.
- **Identifier assignment.** `PP-1310` is present on the Torres approval but the
  customer never entered it (doc 06 · C7). Either the manager assigns it during
  approval, or the system generates it. Doc 14, Q3.
- A rejection reason, captured and shown to the customer *(proposed)*.
- Empty state — *"Nothing awaiting approval."*

---

## M3 · Customers & Vehicles
`screens/manager/03-customers-vehicles.png`

Title **Customers & Vehicles**; subtitle *"Approve changes, edit vehicle details and
photos, and manage customer accounts for this location."*

| Element | Spec |
|---|---|
| Search | Full-width, 🔍 placeholder *"Search customers, vehicles, parking location…"* |
| Action | **👤+ Add customer** — bordered, right of search |
| Table | Columns `CUSTOMER` · `STATUS` · `VEHICLES`, **all sortable** (↕ affordance in each header) |

| Column | Rendering |
|---|---|
| Customer | Full name, navy |
| Status | Pill — `active` green / `pending` amber |
| Vehicles | Comma-joined list: *"Subaru Outback, Tesla Model Y"* |

Search spans customers, vehicles, **and parking location** — meaning it queries the
staff-only field on requests. That is the "where did we put the Camry?" lookup.

**Not shown:** row actions or a customer detail view, though the subtitle promises
editing vehicle details and photos. A customer detail screen is required scope. Doc 14, Q4.

---

## M4 · Valet Account
`screens/manager/04-valet-account.png`

Title **Valet Account**; subtitle *"Shared valet service account(s) for this location —
one login stays signed in on the tablet. Suspend, reactivate, reset the password, or add
an account."*

Card `VALET ACCOUNTS ({count})` with a **+ Add valet** link (red, top-right).

Row: 👤 avatar · **Wacker Drive Valet Station** / `@wacker-valet` (mono, muted) ·
`active` pill · then three actions: **Edit credentials** · **Reset password** ·
**Suspend** (red).

The subtitle is the architectural statement for this role: the account represents a
*post*, not a person, and it is expected to stay authenticated indefinitely. That drives
the kiosk-security requirements in doc 13.

**Must be built:** confirmation dialogs for Suspend and Reset password; where a reset
password is *displayed* (nothing is emailed — it must be shown once, on screen, to be
handed over); and what happens to a signed-in tablet when its account is suspended
(recommendation *(proposed)*: sessions terminate immediately, the tablet shows a
lock screen with a message).

---

## M5 · Request History
`screens/manager/05-request-history.png`

Title **Request History**; subtitle *"Completed requests are retained for approximately
7 days for operational review."*

Table, all columns sortable: `CUSTOMER` · `VEHICLE` · `DECAL` · `TYPE` · `COMPLETED`

| Column | Example | Note |
|---|---|---|
| Customer | Michael Torres | |
| Vehicle | Toyota Camry | Make + model, no color |
| Decal | PP-1042 | **Header is hard-coded "DECAL"** — must follow `location.identifier_type` |
| Type | `Now` | `Now` for immediate, presumably the scheduled datetime otherwise |
| Completed | Sep 9, 2026 at 5:18 PM | Absolute, location-local |

The `DECAL` header is a concrete bug to avoid: at River North Condos this column is
apartment numbers. Label it from the location.

**Must be built:** date-range filter, search, pagination or infinite scroll, export
*(proposed — dispute resolution frequently ends in "send me the record")*, and an empty
state.

---

## M6 · Settings
`screens/manager/06-settings.png`

Title **Pioneer Connect** *(page heading is the app name here rather than the screen
name — an inconsistency; use "Settings")*. Section heading **Settings**; subtitle
*"Operational settings for this location's valet stand."*

Card `VALET REQUEST CHIME`, with the governing note:

> The chime repeats until a valet accepts the request. Only Garage Managers and System
> Administrators can change these settings — valets cannot turn alerts off.

| Control | Type | Default | Sub-copy |
|---|---|---|---|
| 🔊 **Request chime enabled** | Toggle | on | *"Turning this off silences incoming-request alerts on every valet screen at this location."* |
| **Chime repeat interval** | Select | `6 seconds` | *"How often the alert repeats while a request is awaiting acceptance."* |
| **Chime volume** | Select | `Medium` | *"Noticeable on the valet stand without being disruptive."* |

Managers get **only** the chime — the operational policies block is Admin-only. The
scoping is right: a manager tunes their own stand; policy is a company decision.

Interval and volume option sets are not fully visible. Recommendation *(proposed)*:
interval `3 / 6 / 10 / 15 / 30 seconds`; volume `Low / Medium / High`.
