# 08 — Screens: Garage Manager

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
> **Changed:** first-name search is the named requirement (§6.5); vehicle photo editing
> removed (§4.1); history window is 2–3 days (§4.3); a planned-absence switch is added
> for the manager-absence backup (§6.1).

Desktop, left sidebar + content, **operable remotely** — the client requires managers to
*"work remotely without being on site."* Nothing in this role may assume presence at the
garage. Seven screens.

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
- **Identifier verification.** The customer supplies the decal / unit number at
  registration (client-confirmed). The manager's job here is to *verify* it against the
  property's records, and correct it if wrong — so the field must be **editable at
  approval**, not read-only.
- A rejection reason, captured and shown to the customer *(proposed)*.
- **Escalation state.** An approval past its SLA renders as `escalated` and is visible to
  the Office Admin (doc 04 §6). Show the manager that it escalated — silently
  reassigning their work is worse than the delay.
- Empty state — *"Nothing awaiting approval."*

---

## M3 · Customers & Vehicles
`screens/manager/03-customers-vehicles.png`

Title **Customers & Vehicles**; subtitle *"Approve changes, edit vehicle details and
photos, and manage customer accounts for this location."*

| Element | Spec |
|---|---|
| Search | Full-width, 🔍 placeholder *"Search customers, vehicles, parking location…"*. **First-name match is the primary path** — client-named behavior (see below) |
| Action | **👤+ Add customer** — bordered, right of search |
| Table | Columns `CUSTOMER` · `STATUS` · `VEHICLES`, **all sortable** (↕ affordance in each header) |

| Column | Rendering |
|---|---|
| Customer | Full name, navy |
| Status | Pill — `active` green / `pending` amber |
| Vehicles | Comma-joined list: *"Subaru Outback, Tesla Model Y"* |

Search spans customers, vehicles, **and parking location** — meaning it queries the
staff-only field on requests. That is the "where did we put the Camry?" lookup.

**First name is the fast path.** The client called this out specifically:

> *"Simple first-name search — Jonathan emphasized this specifically as the search
> behavior he wants."*

Rank first-name matches above everything else; keep the broader fields as fallback. A
manager on the phone with "Grace from 12B" types *Grace*.

**Vehicle photo editing is removed.** The prototype subtitle promises editing *"vehicle
details and photos"* — photos no longer exist. Images are generic assets derived from
make/model/colour (doc 03). Update the subtitle to *"Approve changes, edit vehicle and
customer details, and manage customer accounts for this location."*

**Not shown:** row actions or a customer detail view. A customer detail screen is
**required scope** — it is where the manager edits vehicle and customer information and
sees phone numbers, which valets cannot. Listed in doc 05 as a screen the prototype
does not show.

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

**Correct the window.** The client stated 2–3 days for the staff-facing view:
*"records older than two or three days can drop off the valet view, since the platform is
not doing billing."* Backend retention is **permanent and separate** (doc 04 §8) — the
subtitle should say what the view shows, not imply anything is deleted. Suggested copy:
*"Recent completed requests. Full history is retained in the system of record."*

Table, all columns sortable: `CUSTOMER` · `VEHICLE` · `DECAL` · `TYPE` · `COMPLETED`

| Column | Example | Note |
|---|---|---|
| Customer | Michael Torres | |
| Vehicle | Toyota Camry | Make + model, no color |
| Decal | PP-1042 | **Header is hard-coded "DECAL"** — must follow `location.identifier_type` (*"decal number, apartment number or unit number, whichever that property uses"*) |
| Type | `Now` | `Now` for immediate, presumably the scheduled datetime otherwise |
| Completed | Sep 9, 2026 at 5:18 PM | Absolute, location-local |

The `DECAL` header is a concrete bug to avoid: at River North Condos this column is
apartment numbers. Label it from the location.

**Must be built:** date-range filter, first-name search, pagination or infinite scroll,
export *(proposed — dispute resolution frequently ends in "send me the record")*, and an
empty state.

**Open design question:** the valet board window is 2–3 days, but the manager's purpose
here is *operational review*, and the business retains everything for complaints, legal
and vehicle disputes. Recommendation *(proposed)*: give managers a **longer window than
valets** — 30 days with date-range search into the full archive. The 2–3 day rule was
stated about the *valet* view specifically.

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

**Sound design is a client-reviewed deliverable.** *"The chime must be persistent but not
annoying … the sound design matters to him."* Add a **test tone** control here so the
manager hears what they are setting, and put the candidate assets in front of Jonathan
before build rather than after.

---

## M7 · Availability *(new — client requirement)*

Not in the prototype. Required by the manager-absence backup (doc 04 §6), which was the
client's single flagged gap.

| Control | Type | Behavior |
|---|---|---|
| **I'm available** / **I'm away** | Toggle | While away, new approvals route to the Office Admin immediately, with no SLA delay |
| Away until | Date (optional) | Auto-restores availability |
| Backup contact | Read-only | Shows who is covering — the assigned Office Admin |

Add a persistent banner on every manager screen while away: *"You're marked away.
Approvals are routing to the office."* — so nobody forgets they set it.

This converts the common case (planned leave) from an SLA exception into a normal path,
and it costs almost nothing to build.
