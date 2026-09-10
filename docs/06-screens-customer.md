# 06 — Screens: Customer

Mobile shell, ~390pt wide. Every screen shares the same header and bottom tab bar.

**Shared chrome**

- **Header** — Pioneer "P" logo (left), 🔔 notification bell, `Viewing as` role select
  *(prototype only — do not ship)*. Header sits on white with a hairline bottom rule.
- **Bottom tab bar** — `⊞ Home` · `📅 Schedule` · `🚗 Vehicle`. Active item red, inactive slate.
- Content area scrolls between the two; background is white on customer screens.

---

## C1 · Landing / QR
`screens/customer/00-landing-qr.png`

Public entry point, full-viewport, centered column.

| Element | Content |
|---|---|
| Logo | Large "P" mark |
| Wordmark | **Pioneer** (navy) **Connect** (red) — two-tone, one line |
| Tagline | "Smart Valet Retrieval" |
| Primary CTA | `→] Sign In` — filled brand red, full width |
| Secondary CTA | `👤+ Create Account` — white with border, full width |
| QR card | Heading "Get the app", QR image, caption *"Scan to download or open Pioneer Connect — one app for every Pioneer property."* |
| Helper | 🔑 *"Your Location Access Code links you to your garage at sign-up."* |

The QR card is the physical-world bridge: printed in elevators, lobbies, and valet
stands. The QR should deep-link to the installable app *(inferred)*.

Below a divider, a `PROTOTYPE DEMO — JUMP TO A ROLE` block with four buttons. **Remove.**

---

## C2 · Sign in
`screens/customer/01-sign-in.png`

Centered card on the neutral page background.

| Element | Spec |
|---|---|
| Logo | Centered above the card |
| Heading | "Sign in to your account" — regular weight, slate |
| Field | `Email or username`, placeholder `you@example.com` |
| Field | `Password`, masked |
| Submit | **Sign In** — filled brand red, full width |
| Footer row | `Forgot password?` (slate, left) · `Create account` (red, right) |

Below the card, a `PROTOTYPE DEMO ACCOUNTS — TAP TO FILL` panel listing four roles.
**Remove.**

**Not shown, must be built:** validation errors, invalid-credentials error, rate
limiting / lockout, loading state on submit.

---

## C3 · Home
`screens/customer/02-home.png`

The default landing tab. Deliberately sparse — one job, one glance.

```
Welcome back,
Michael                                    ← greeting, first name only

┌────────────────────────────────────────┐
│ ┌──────┐  Silver Toyota Camry          │  ← vehicle card
│ │ No   │  🚗 PP-1042                   │
│ │ photo│                                │
│ └──────┘                                │
│ ┌────────────────────────────────────┐ │
│ │ Pending            View status  ›  │ │  ← live request strip, red-tinted
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

| Element | Spec |
|---|---|
| Greeting | "Welcome back," (slate, small) over **First name** (navy, bold, large) |
| Vehicle card | Photo tile or `No photo` placeholder · `{color} {make} {model}` · 🚗 `{identifier}` |
| Request strip | Only when a request is live. Status label left, `View status ›` right, red-tinted background |
| Repeat | One card per vehicle |

**The primary action is missing from this screen.** There is no visible "Request my
car" button anywhere in the customer flow, yet requests plainly originate from the
customer. The vehicle card in the screenshot is fully occupied by an *existing*
request. Resolve before building — recommendation *(proposed)*: a full-width primary
**Request my car** button inside each vehicle card, which the live-request strip
replaces while a request is open. See doc 14, Q1.

**Empty states to build:** no vehicles yet (→ prompt to add one), vehicle pending
approval (→ blocked with explanation), no active request (→ the request button).

---

## C4 · Request status
`screens/customer/03-request-status.png`

Reached from `View status ›`.

| Element | Spec |
|---|---|
| Header row | **Your request** (navy, bold) · `↻ Refresh` (slate, right) |
| Vehicle card | Photo tile · `{color} {make} {model}` · `Decal {id} · {Location name}` · status pill right-aligned |
| Progress card | `PROGRESS` label; three-node horizontal stepper |
| Caption | *"Updates automatically as the valet works your request."* |
| Action | **⊗ Cancel Request** — full width, red text on a pale red fill, red border |

**Progress stepper** — three nodes, connected by a rule. Completed/current nodes and
their connectors render brand red; future nodes render slate.

```
   ●━━━━━━━━━━━━    ○────────────    ○
   Pending          Retrieving       Ready for
                    Vehicle          Pickup
```

Node labels are the customer vocabulary from doc 04 — never show "Accepted".

The `↻ Refresh` control plus *"updates automatically"* implies polling with a manual
override. Prefer real-time updates and keep Refresh as the fallback — see doc 12.

**Undefined:** whether Cancel remains available after a valet accepts. Recommendation
*(proposed)*: allow it in `pending`, require a confirm dialog in `accepted`, hide it in
`ready` (the car is already at the door).

---

## C5 · Schedule a pickup
`screens/customer/04-schedule-pickup.png`

| Element | Spec |
|---|---|
| Title | `📅 Schedule a pickup` (calendar-clock icon + navy bold) |
| Card | `Quick options` label |
| Quick buttons | 2×2 grid: **Later today** · **Tomorrow** · **In 2 days** · **In 3 days** |
| Field | `Date & time` — native datetime input |
| Submit | **Schedule pickup** — full width; **disabled state shown** (muted red fill) |
| Section | `YOUR UPCOMING PICKUPS` — uppercase slate label |
| Empty | *"No scheduled pickups yet."* |

Submit is disabled until a date/time is chosen. The quick options are shortcuts that
populate the datetime field *(inferred)* — "Later today" needs a defined default hour.

**Not shown:** which vehicle a scheduled pickup applies to. With multiple vehicles
(Grace Kim has two) this screen needs a vehicle selector. Doc 14, Q2.

Times must be interpreted in **location-local** time, not device time — a Chicago
resident scheduling from a phone set to New York time must not get an 8am car at 7am.

---

## C6 · My vehicles
`screens/customer/05-my-vehicles.png`

| Element | Spec |
|---|---|
| Title | `🚗 My vehicles` |
| Pending banner | Amber-tinted, ⏱ icon: **Awaiting manager approval** / *"New vehicle: Forest Green Rivian R1S"* |
| Vehicle card | See below |
| Add | `+ Add a vehicle` — bordered white button |

**Vehicle card**

```
┌──────────────────────────────────────────────┐
│ Silver Toyota Camry           PP-1042        │  ← name bold navy, id muted
│ ┌──────┐  ┌──────────────┐                   │
│ │ No   │  │ 🖼 Add photo  │                   │
│ │ photo│  └──────────────┘                   │
│ └──────┘                                     │
│ [ Toyota ] [ Camry  ] [ Silver ]             │  ← 3 inline editable inputs
│ (Approval required)          [Submit change] │  ← pill + filled red button
└──────────────────────────────────────────────┘
```

Fields are directly editable inline — no separate edit mode. The `Approval required`
pill sits to the left of **Submit change** as a persistent reminder that edits are not
immediate.

Critical behavior *(see doc 04)*: submitting a change does **not** alter the displayed
values. The card keeps showing the live record; the pending change surfaces only in
the banner and in the manager's approval queue.

**Add photo** sits outside the approval row and appears to apply immediately.

---

## C7 · Add a vehicle
`screens/customer/06-add-vehicle.png`

Same screen as C6 with an expanded form appended — `+ Add a vehicle` reveals it inline
rather than navigating away.

| Element | Spec |
|---|---|
| Section label | `ADD A VEHICLE` — uppercase slate |
| Fields | `Make` · `Model` · `Color` — three inputs in a row |
| Notice | 🛡 *"New vehicles require garage-manager approval before they become active."* |
| Actions | **Submit for approval** (filled red) · **Cancel** (bordered white) |

The customer never enters the identifier (decal / apartment / stall). That value is
assigned by staff — `PP-1310` appears on the manager's approval card for a vehicle the
customer submitted without it. **Identifier assignment is a staff responsibility**, and
the manager's approval UI needs a field for it. Doc 14, Q3.

Photo upload is not offered at creation, only on an existing vehicle. Consider adding
it *(proposed)* — the photo is what a valet uses to find the car.
