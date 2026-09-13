# 06 — Screens: Customer

> ## 🔒 INTERNAL — VisMedAI Advisory
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
> **Changed against the prototype:** photo upload removed (§4.1); Request Now confirmed
> (§5); cancel is `pending`-only (§5); notification preferences added (§6.4).

Mobile shell, ~390pt wide. **Ships as a native app to both stores.** Every screen shares
the same header and bottom tab bar.

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
| Vehicle card | **Generic vehicle image** (derived from make/model/colour — never uploaded) · `{color} {make} {model}` · 🚗 `{identifier}` |
| Request strip | Only when a request is live. Status label left, `View status ›` right, red-tinted background |
| Repeat | One card per vehicle |

**The primary action — now confirmed.** The prototype screen shows no request control
because the pictured vehicle already has a live request. The client confirmed the action
exists: *"Customer taps **Request Now**."*

Spec: a full-width primary **Request Now** button inside each vehicle card, replaced by
the live-status strip while a request is open. One tap, no confirmation dialog, no
intermediate screen — this is the action the entire product exists to serve, and it is
performed by someone walking toward a lobby door.

Only `active` vehicles get the button. A vehicle still `pending_approval` shows the
reason instead.

**Empty states to build:** no vehicles yet (→ prompt to add one), vehicle pending
approval (→ blocked, with the reason), account still `pending` (→ "awaiting approval
from the garage manager"), no active request (→ the **Request Now** button).

---

## C4 · Request status
`screens/customer/03-request-status.png`

Reached from `View status ›`.

| Element | Spec |
|---|---|
| Header row | **Your request** (navy, bold) · `↻ Refresh` (slate, right) |
| Vehicle card | Generic vehicle image · `{color} {make} {model}` · `{identifier_label} {id} · {Location name}` · status pill right-aligned |
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

**Cancel is `pending`-only — client-decided.**

> *"Customers must be able to cancel a request **before it is accepted**."*

The button renders only while `status = pending` and must disappear on the `accepted`
transition. Because status updates live, it can vanish while the customer is looking at
it — replace it in place with the retrieving state rather than leaving a button that
will fail. If a cancel request loses the race with an accept, return `409` and show
*"A valet has already started retrieving your vehicle."*

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
(Grace Kim has two — multiple vehicles per customer is client-confirmed) this screen
needs a vehicle selector. Doc 14, Q26.

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

**Vehicle card** — note the prototype's `Add photo` control is **removed**:

```
┌──────────────────────────────────────────────┐
│ Silver Toyota Camry           PP-1042        │  ← name bold navy, id muted
│ ┌──────┐                                     │
│ │ 🚗   │   ← generic image, derived from     │
│ │ img  │      make + model + colour          │
│ └──────┘                                     │
│ [ Toyota ] [ Camry  ] [ Silver ]             │  ← 3 inline editable inputs
│ (Approval required)          [Submit change] │  ← pill + filled red button
└──────────────────────────────────────────────┘
```

Changing the colour changes the rendered image. Preview the new image live as the
customer edits *(proposed)* — it makes the generic-image system legible instead of
surprising.

Fields are directly editable inline — no separate edit mode. The `Approval required`
pill sits to the left of **Submit change** as a persistent reminder that edits are not
immediate.

Critical behavior *(see doc 04)*: submitting a change does **not** alter the displayed
values. The card keeps showing the live record; the pending change surfaces only in
the banner and in the manager's approval queue.

**No photo upload exists.** *"Generic vehicle images. No customer photo uploads."* —
client requirement, for data load and privacy exposure. See doc 03.

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

On the prototype's approval card, `PP-1310` appears against a vehicle the customer
submitted — consistent with the client's statement that the customer provides the
identifier at registration.

**The customer enters the identifier.** Client-confirmed: registration collects *"name,
vehicle information, unit / decal number."* The field is labelled from
`location.identifier_type` — "Decal number" at Wacker Drive, "Apartment number" at River
North. The manager **verifies** it at approval rather than assigning it.

Add the identifier field to this form; the prototype omits it.


---

## C8 · Notification preferences *(new — client requirement)*

Not in the prototype. Added from the brief:

> *"Notify on 'Ready' as the default. The customer's required notification is when the
> vehicle is ready."*
> *"Optional earlier updates. Customers may opt in to 'Retrieving Vehicle' status updates
> via a notification-preference toggle."*
> *"In-app push notifications only. No SMS."*

| Control | Type | Default | Copy |
|---|---|---|---|
| **Vehicle ready for pickup** | Toggle | **on** | *"We'll let you know the moment your vehicle is at the door."* |
| **Retrieving your vehicle** | Toggle | **off** | *"Get an earlier update when a valet accepts your request."* |

**Recommendation *(proposed)*: make the Ready toggle non-disableable in MVP** — render it
on and locked with an explanatory caption. It is the notification the product exists to
deliver, and push is the only channel. A customer who switches it off has silently
downgraded themselves to the experience they were trying to escape.

Reachable from the customer's account/profile area and from the bell. Requires push
permission priming on first launch — ask *after* the first successful request, not on
cold start, so the ask has context.
