# 07 — Screens: Valet

One screen and two modals. The valet's whole application is a board.

**Design constraints unique to this role**

- **Tablet, landscape, wall-mounted or counter-mounted.** Large touch targets.
- **Read at arm's length.** Status must be legible without leaning in.
- **Gloved / wet hands, ambient noise, poor lighting.** No hover states, no small text,
  no fine-grained drag interactions.
- **Shared station account that never logs out.** No personal data on screen that isn't
  operationally necessary; no destructive actions without confirmation.

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
│ │ No   │  Toyota Camry · Silver     │      green = completed
│ │ photo│                            │
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
| 1 | Photo tile (or `No photo`) + **customer first name** | Name bold navy |
| 2 | `{Make} {Model} · {Color}` | Slate |
| 3 | `{identifier}` · 🕐 relative time *or* absolute datetime | Slate |
| 4 | Timing note — *"needs it ASAP"* | Slate |
| 5 | 📍 `{parking_location}` — omitted when unset | Slate |
| 6 | Badges — see below | |
| 7 | Action row | |

**Customer first name only.** Deliberate: enough for the valet to greet the customer,
not a directory of residents left on an unattended screen.

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
| Recently completed | None. ✓ check mark, green left rail, completion timestamp |
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
| Header | Photo tile · **{Color} {Make} {Model}** (bold navy) · `{identifier}` · status badge |
| Facts | 👤 `Customer` → full name (**"Grace Kim"** — full name here, unlike the card) |
| | 📞 `Phone` → `(312) 555-0188` |
| | 🕐 `Needs it` → `ASAP` or the scheduled datetime |
| Staff block | `📍 PARKING LOCATION · STAFF ONLY` — text input with placeholder *"e.g. Level 3 East, Red Zone, Charging Station A"* + **Save** |
| Staff block | `📄 INTERNAL NOTES · STAFF ONLY` — dashed-border panel; empty text explains the purpose; input *"Add an operational note…"* + **+ Add** |
| Footer | **↺ Revert to Pending** (bordered) · **Ready** (filled green, wide) |

**Internal notes empty-state copy, verbatim** — it defines the feature:

> No notes yet. Examples: pickup preferences, vehicle reminders (e.g. "plug in EV after
> return", "leave key in vehicle"), and operational instructions. Visible to valet,
> manager, and admin — never to customers.

The phone number is the escalation path when the app fails: the valet calls the
customer. It appears **only** in this modal, not on the board — an intentional
minimum-exposure choice on a shared screen. Preserve that.

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
| **👥 Registered Customers** | Rows: 👤 name · status pill (`active` green / `pending` amber) · phone, right-aligned |
| **🚗 Registered Vehicles** | *(not captured — expect vehicle, owner, identifier)* |
| **🕘 Recent Pickups** | *(not captured — expect the ~7-day completed list)* |

This is the valet's lookup tool: a customer walks up without having used the app, and
the valet finds them by name.

Everything here is read-only — no row actions, no editing, no settings. Enforce it in
the API, not just the UI.

**Recommended addition *(proposed)*:** a search field. Four seed rows fit on screen;
two hundred residents will not, and the manager's equivalent screen already has search.
