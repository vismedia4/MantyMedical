# 07 — Screens: Valet

> Requirements authority is [00 — Client Requirements](00-client-requirements.md).
> **Corrected against the prototype:** the customer phone number is removed from the
> request-detail modal (§4.2) — the client made valet phone access a privacy
> restriction. Generic vehicle images replace photo tiles (§4.1). Recent-completion
> history is 2–3 days, not 7 (§4.3).

One screen and two modals. The valet's whole application is a board.

**Design constraints unique to this role**

- **Tablet, landscape, wall-mounted or counter-mounted.** Large touch targets.
- **Read at arm's length.** Status must be legible without leaning in.
- **Gloved / wet hands, ambient noise, poor lighting.** No hover states, no small text,
  no fine-grained drag interactions.
- **Shared station account that never logs out.** No personal data on screen that isn't
  operationally necessary; no destructive actions without confirmation.
- **Phone numbers are off-limits at this role.** Client privacy restriction — see V2.

---

## V1 · Queue board
`screens/valet/01-queue.png`

```
┌───────────────────────────────────────────────────────────────────────────┐
│ [P]                       📍 Wacker Drive Garage   👁 Viewing as ▾   ⋮    │
├───────────────────────────────────────────────────────────────────────────┤
│ Valet Queue                                                                │
├───────────────────────────────────────────────────────────────────────────┤
│ 🔔 1 request awaiting acceptance   Accept to stop the alert.               │  ← alert
├──────────────┬──────────────────┬─────────────────┬───────────────────────┤
│ INCOMING  1  │ ACTIVE QUEUE  3  │ TOMORROW'S  1   │ FUTURE PICKUPS  1     │
│              │                  │                 │                       │
│ [card]       │ [card]           │ [card]          │ [card]                │
│              │ [card]           │                 │                       │
│              │ RECENTLY         │                 │                       │
│              │ COMPLETED        │                 │                       │
│              │ [card]           │                 │                       │
└──────────────┴──────────────────┴─────────────────┴───────────────────────┘
```

### Alert banner

Renders only while ≥1 request is `pending`. Pale red fill, red bell icon.
**`{n} request(s) awaiting acceptance`** in bold red, then muted *"Accept to stop the
alert."* — the copy explicitly ties the visual banner to the audible chime.

### Columns

| Column | Contents | Header count |
|---|---|---|
| **INCOMING** | `pending` requests. Column header in **red**; whole column gets a red-tinted background and red border while non-empty | badge |
| **ACTIVE QUEUE** | `accepted` requests, plus a `RECENTLY COMPLETED` sub-section below | badge |
| **TOMORROW'S PICKUPS** | scheduled for the next local day | badge |
| **FUTURE PICKUPS** | scheduled beyond tomorrow | badge |

Empty columns keep their header and count and render an empty body — the four-column
frame is constant so muscle memory holds.

### Request card

```
┌─────────────────────────────────────┐  ← 4px left rail:
│ ┌──────┐  Michael                   │      red   = incoming/active
│ │ 🚗   │  Toyota Camry · Silver     │      green = completed
│ │ img  │                            │      (generic image, derived)
│ └──────┘                            │
│ PP-1042  🕐 5 minutes ago           │
│ needs it ASAP                       │
│ 📍 2F · Red zone                    │
│ [IMMEDIATE] [Pending]               │
│ ┌─────────────────────────────────┐ │
│ │        ✓ Accept                 │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

| Line | Content | Style |
|---|---|---|
| 1 | Generic vehicle image + **customer first name** | Name bold navy |
| 2 | `{Make} {Model} · {Color}` | Slate |
| 3 | `{identifier}` · 🕐 relative time *or* absolute datetime | Slate |
| 4 | Timing note — *"needs it ASAP"* | Slate |
| 5 | 📍 `{parking_location}` — omitted when unset | Slate |
| 6 | Badges — see below | |
| 7 | Action row | |

**Customer first name only.** Deliberate: enough for the valet to greet the customer,
not a directory of residents left on an unattended screen. It also matches the client's
stated search behavior — *"simple first-name search"* — so the board and the lookup use
the same handle.

**Badges**

| Badge | Fill | Text | Meaning |
|---|---|---|---|
| `IMMEDIATE` | pale red | red | `type = immediate` |
| `FUTURE` | pale blue-grey | slate | `type = scheduled` |
| `Pending` | neutral grey | slate | `status = pending` |
| `Accepted` | pale amber | amber | `status = accepted` |

Type badge and status badge are **independent** and render side by side.

**Actions by column**

| Column / state | Actions |
|---|---|
| Incoming (`pending`) | **✓ Accept** — full-width filled red |
| Active (`accepted`) | **↺** icon button (revert to pending) + **Ready** — filled green, wide |
| Recently completed | None. ✓ check mark, green left rail, completion timestamp. **Drops off the board after 2–3 days** (client-stated) — backend retention is permanent and separate |
| Tomorrow / Future | **⊕ Move to active** — full-width, red text on pale red |

Tapping anywhere on a card body opens **V2 · Request detail**.

**Colour carries meaning here and it is load-bearing**: red = needs you now, green =
done. That mapping must survive dark mode, sunlight, and colour-blind users — always
pair it with the text label, which the prototype does.

**Not shown, must be built:** connection-lost banner, a request cancelled by the
customer while sitting in the queue, more cards than fit a column (scroll within
column), and multi-valet contention — see below.

> **Concurrency.** A location has one shared account but may have several valets and
> several tablets. Two people can tap **Accept** on the same card. Handle it: accept
> should be a compare-and-swap on `status = pending`, and a losing tap should show
> *"Already accepted"* rather than silently doing nothing.

---

## V2 · Request detail
`screens/valet/02-request-detail.png`

Modal, centered, dimmed board behind. Title **Request detail**, ✕ close top-right.

| Section | Content |
|---|---|
| Header | Generic vehicle image · **{Color} {Make} {Model}** (bold navy) · `{identifier}` · status badge |
| Facts | 👤 `Customer` → full name (**"Grace Kim"** — full name here, unlike the card) |
| | 🕐 `Needs it` → `ASAP` or the scheduled datetime |
| Staff block | `📍 PARKING LOCATION · STAFF ONLY` — text input with placeholder *"e.g. Level 3 East, Red Zone, Charging Station A"* + **Save** |
| Staff block | `📄 INTERNAL NOTES · STAFF ONLY` — dashed-border panel; empty text explains the purpose; input *"Add an operational note…"* + **+ Add** |
| Footer | **↺ Revert to Pending** (bordered) · **Ready** (filled green, wide) |

**Internal notes empty-state copy, verbatim** — it defines the feature:

> No notes yet. Examples: pickup preferences, vehicle reminders (e.g. "plug in EV after
> return", "leave key in vehicle"), and operational instructions. Visible to valet,
> manager, and admin — never to customers.

### ⚠ The phone number must be removed

The prototype's modal displays `📞 Phone (312) 555-0188`. **Delete it.** This is a
client-stated privacy restriction, not a preference:

> *"CANNOT: edit customer or vehicle data; **view customer phone numbers** — called out
> by Jonathan as a privacy restriction. Phone access is preserved for authentication and
> management at higher role levels."*

Enforce it in the API, not the template: the valet serializer must not carry the field
at all (doc 11). A shared, always-signed-in tablet in a semi-public garage is exactly
the wrong place to expose a resident's phone number, and the client saw that before we
did.

**This removes the valet's escalation path.** The phone was how a valet resolved a
problem the app could not — a car that will not start, a customer who did not show.
That gap needs an answer before build; see doc 14, Q7. The likely shape *(proposed)*: a
**"Notify manager"** action on the request that pings the garage manager, who *does*
hold phone access. The valet raises the flag; the manager makes the call.

Both staff blocks carry an explicit `STAFF ONLY` suffix in their labels. Keep it: on a
tablet a customer can see over, that label is the control that stops a valet typing
something they shouldn't.

---

## V3 · Valet menu
`screens/valet/03-valet-menu.png`

Modal opened from the header **⋮**. Title **Valet menu**, ✕ close.

Leading notice, 👁 icon, muted:

> View only — valets can review this information but cannot change records or settings.

Three segmented tabs, active tab filled red with white text:

| Tab | Contents |
|---|---|
| **👥 Registered Customers** | Rows: 👤 name · status pill (`active` green / `pending` amber). **The phone column shown in the prototype must be removed** — same restriction as V2 |
| **🚗 Registered Vehicles** | *(not captured — expect vehicle, owner, identifier)* |
| **🕘 Recent Pickups** | *(not captured — the 2–3 day completed list)* |

This is the valet's lookup tool: a customer walks up without having used the app, and
the valet finds them by name.

Everything here is read-only — no row actions, no editing, no settings. Enforce it in
the API, not just the UI.

**Required addition:** a **first-name search** field. Four seed rows fit on screen; two
hundred monthly parkers will not. The client named the behavior specifically:

> *"Simple first-name search — Jonathan emphasized this specifically as the search
> behavior he wants."*

Make first name the fast path — a valet is looking at a person standing in front of them
and types "Grace". Match on first name first, surface those results above any
substring matches elsewhere, and keep it forgiving of typos.
