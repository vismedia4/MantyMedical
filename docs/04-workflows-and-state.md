# 04 — Workflows & State Machines

> Requirements authority is [00 — Client Requirements](00-client-requirements.md).
> The cancellation window (§1) is now client-decided; §6 (manager-absence backup) and
> §7 (no-smartphone path) are new requirements from the brief.

## 1. Retrieval request lifecycle

### The state machine

```
                    customer cancels
        ┌──────────────────────────────────────┐
        │                                      ▼
   ┌────┴────┐   valet     ┌──────────┐   ┌───────────┐
   │ PENDING │───Accept───►│ ACCEPTED │──►│   READY   │
   └────┬────┘             └────┬─────┘   └─────┬─────┘
        ▲                       │               │
        │      Revert to Pending│               │ customer collects
        └───────────────────────┘               ▼
                                          ┌───────────┐
                                          │ COMPLETED │
                                          └───────────┘
```

| Transition | Actor | Trigger |
|---|---|---|
| → `pending` | Customer | Taps request / a scheduled request comes due |
| `pending` → `accepted` | Valet | **Accept** button on the Incoming card |
| `accepted` → `pending` | Valet | ↺ icon on card, or **Revert to Pending** in detail modal |
| `accepted` → `ready` | Valet | **Ready** button (card or detail modal) |
| `ready` → `completed` | *unobserved* | See below |
| `pending` → `cancelled` | Customer | **Cancel Request** — **only while `pending`** (client-decided) |
| *any* → *any* | Manager / Admin | **Override status** dropdown on Manager Dashboard |

### Two gaps you must close before building

**(a) Nothing observed moves a request from `ready` to `completed`.** The valet board
shows a *Recently Completed* section and Request History shows completed rows, so the
state exists — but no screen shows the button that produces it. Three candidates:

| Option | Implication |
|---|---|
| Valet taps a **Complete/Picked up** action | Most accurate; one more tap per car |
| `ready` auto-completes after a timeout | Zero friction; history becomes approximate |
| Customer confirms collection in-app | Best data; requires the customer to act after they have their car — they won't |

**Recommendation *(proposed)*: valet action, with an auto-complete safety net after N
hours.** Not addressed in the September 10 session; still open (doc 14, Q4).
 Operational history is the product's dispute-resolution backbone; it should
reflect a human confirming the handoff, but must not accumulate stuck `ready` rows
when a valet forgets. Log auto-completions distinctly in the activity feed.

**(b) The cancellation window is now decided.** The client resolved it:

> *"Cancellation is required. Customers must be able to cancel a request **before it is
> accepted**. The request-state flow was tested in-session to determine when the cancel
> option should surface."*

So: **Cancel is available in `pending` and disappears the moment a valet accepts.** The
customer status screen must hide the button on the `accepted` transition — which, because
the board updates live, means it can vanish while the customer is looking at it. Handle
that gracefully: replace it with the "a valet is retrieving your vehicle" state rather
than letting a dead button sit there.

Still to decide: whether a cancelled request is visible to staff in history. It must
be — otherwise a valet who already walked toward the car has no explanation. Doc 14, Q11.

### Customer-facing vs. staff-facing status vocabulary

These are **different labels for the same states** and must be mapped, not merged:

| Internal state | Customer sees | Valet sees | Manager sees |
|---|---|---|---|
| `pending` | **Pending** | `Pending` badge, Incoming column | `Pending` |
| `accepted` | **Retrieving Vehicle** | `Accepted` badge, Active Queue | `Accepted` |
| `ready` | **Ready for Pickup** | Green card, Recently Completed | — |

The customer progress bar renders exactly three nodes — *Pending · Retrieving Vehicle ·
Ready for Pickup* — under the caption *"Updates automatically as the valet works your
request."* Keep the mapping in one place; do not let "Accepted" leak into a customer
view.

### Request type and queue bucketing

```
  type = immediate  ──► requested now, "needs it ASAP", labeled IMMEDIATE / Now
  type = scheduled  ──► scheduled_for set, labeled FUTURE
                        │
                        ├─ scheduled_for is today      ──► Active Queue (once due)
                        ├─ scheduled_for is tomorrow   ──► Tomorrow's Pickups
                        └─ scheduled_for is later      ──► Future Pickups
```

A valet can pull a scheduled request forward with **Move to active** — visible on both
the Tomorrow and Future columns. This is a manual promotion; whether requests *also*
auto-promote when their time arrives is unresolved *(see doc 14)*. Recommendation
*(proposed)*: auto-promote at `scheduled_for` minus a configurable lead time, keeping
**Move to active** as a manual early pull.

---

## 2. Customer onboarding

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 1. Property hands the customer a 6-digit Location Access Code       │
  │    (in person, in a welcome packet, or via the QR landing page)     │
  └────────────────────────────┬────────────────────────────────────────┘
                               ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 2. Customer taps Create Account, enters the code                    │
  │    → code resolves to a Location                                    │
  │    → Location.identifier_type decides the next question:            │
  │        garage      → "Decal number"                                 │
  │        condo       → "Apartment number"                             │
  │        residence   → "Stall number"                                 │
  └────────────────────────────┬────────────────────────────────────────┘
                               ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 3. Customer submits registration details:                           │
  │       name · vehicle information · unit / decal number              │
  │    → User.status = pending                                          │
  │    → ApprovalRequest(kind = new_registration) created               │
  └────────────────────────────┬────────────────────────────────────────┘
                               ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 4. Garage Manager sees it under NEW REGISTRATIONS                   │
  │    Review · Approve · Reject                                        │
  └───────────┬─────────────────────────────────┬───────────────────────┘
              │ approve                         │ reject
              ▼                                 ▼
     User.status = active               User.status = rejected
     Customer can request a car         Customer notified  (mechanism TBD)
```

This flow is client-confirmed step for step. Two details it settles:

- Step 2's branching is why `identifier_type` must be configuration. The enrollment form
  is **generated from the location record**, not hard-coded.
- **The customer supplies the identifier**, not staff. The manager's job at approval is
  to *verify* the decal / unit number is real, not to assign one.

Gate: step 3→4 only applies while `require_manager_approval_new_customers` is on. With
the policy off, registration should activate immediately. Build both paths.

A manager can also skip the whole flow — **Add customer** on the Customers & Vehicles
screen creates an account directly, presumably pre-approved *(inferred)*.

---

## 3. Vehicle change approval

```
  Customer edits make/model/color        Customer adds a vehicle
  on My Vehicles                         via ADD A VEHICLE
        │                                       │
        │  "Approval required"                  │  "New vehicles require garage-manager
        │  [Submit change]                      │   approval before they become active."
        ▼                                       ▼
  ApprovalRequest(vehicle_change)        ApprovalRequest(new_vehicle)
  payload = field diff                   payload = proposed vehicle
        │                                       │
        └───────────────┬───────────────────────┘
                        ▼
        Manager → Pending Approvals → Approve / Reject
                        │
            approve ────┴──── reject
              │                 │
    Apply diff to Vehicle    Discard; vehicle stays
    Vehicle.status = active  pending_approval / unchanged
```

**The live record must not be mutated on submit.** The customer's My Vehicles screen
keeps showing the *current* values (Toyota / Camry / Silver) while an amber banner
reports the pending item separately: *"Awaiting manager approval — New vehicle: Forest
Green Rivian R1S."* Pending state is additive and non-destructive.

**There is no photo upload.** The client removed it: vehicle images are generic assets
derived from make + model + colour (doc 03). Changing the colour therefore changes the
rendered image — which means a **vehicle-change approval implicitly approves an image
change**, with no separate moderation path and no user-supplied media anywhere in the
system. That is the point of the decision: *"reduces data load and avoids privacy
exposure."*

---

## 4. Location provisioning (Office Admin)

```
  Add a Location form
    ├─ name, address, state
    ├─ identifier  → decal | apartment | stall
    ├─ manager     → assign existing, or create inline:
    │                  manager name / username / password
    └─ valet       → create inline:
                       station name / username / password
                              │
                              ▼
    On submit:
      • 6-digit access code generated automatically
      • manager + valet credentials provisioned immediately
      • nothing is emailed — credentials handed over directly
```

Post-creation controls on each location card: **Copy** code, **Regenerate** code,
**Deactivate** code, **Edit** location, **Disable** location, and per-account
**Credentials** links.

Two distinct off-switches, and the difference matters:

| Control | Effect |
|---|---|
| **Deactivate** (access code) | Stops *new* enrollment. Existing customers unaffected. |
| **Disable** (location) | *"Disabled locations are hidden from customer registration."* |

Whether **Disable** also suspends service for existing customers at that location is
unresolved *(doc 14)*. Recommendation *(proposed)*: disabling suspends new requests but
preserves history and existing accounts, and is reversible.

Regenerating a code should invalidate the previous one immediately *(proposed)* — that
is the whole point of the control, since it exists to recover from a leaked code.

---

## 5. The chime loop

```
  request enters PENDING
        │
        ├──► banner: "1 request awaiting acceptance — Accept to stop the alert."
        │
        └──► chime plays  ──► wait repeat_interval (6s default)  ──┐
                    ▲                                              │
                    └──── still pending? ──────────────────────────┘
                                 │
                          valet taps Accept
                                 │
                                 ▼
                          chime stops, banner clears
```

*"The chime repeats until a valet accepts the request."* This is an escalating,
un-ignorable alert by design, and the reason valets cannot disable it. Full
implementation guidance in [12 — Notifications & Real-Time](12-notifications-and-realtime.md).

---

## 6. Manager-absence backup — the client's flagged gap

> *"Must be able to intervene when a garage manager is unavailable — Jonathan's single
> flagged gap in the prototype. **Pending approvals must not stall on manager absence.**"*

The only substantive objection raised in the entire prototype walkthrough. A new
customer who cannot get approved cannot park; an approval sitting behind an absent
manager is a customer standing in a lobby.

### Required design

```
  ApprovalRequest created
        │
        ├── manager acts within SLA ──────────────► resolved, normal path
        │
        └── SLA breached (no decision in N hours)
                    │
                    ├──► mark approval "escalated"      ← visible state, not silent
                    ├──► notify Office Admin
                    ├──► surface on the Admin console as an actionable queue
                    └──► Office Admin approves / rejects with full manager authority
```

Four decisions the client must make — put them on Tuesday's agenda:

| Decision | Recommendation *(proposed)* |
|---|---|
| **SLA before an approval is "stalled"** | 4 business hours for registrations; 24h for vehicle changes. A new parker is time-sensitive; a colour change is not |
| **Who is notified** | Office Admin, plus any co-manager assigned to the location |
| **Automatic or manual escalation** | **Automatic.** A pull-only model reproduces the exact failure being fixed — it depends on someone noticing |
| **Does the manager keep the ability to act after escalation?** | Yes. Escalation widens the set of people who can act; it never locks the manager out |

Add a **planned-absence switch** *(proposed)*: a manager going on leave marks themselves
away and approvals route to the admin immediately, with no SLA delay. Cheap, and it
converts the common case from an exception into a normal path.

Requires a visible **escalated** state on `ApprovalRequest`, an admin-facing queue, and
an `ActivityEvent` on every escalation and admin decision.

---

## 7. Customers without smartphones — unresolved, and blocking

> *"Discussed at length. QR-code assistance and manager-supported setup were considered,
> and a manual override path was identified as a likely requirement. Not resolved. Needs
> a decision before build — it affects the data model, the manager UI and the retrieval
> workflow."*

This is not a screen. It is a **data-model question**, which is why it blocks.

The whole system assumes a customer record *is* an authenticated user who taps a button
in an app. A monthly parker without a smartphone breaks that assumption at three layers:

| Layer | What breaks |
|---|---|
| **Data model** | A customer record with no login, no push token, no notification target |
| **Manager UI** | Someone must create and maintain the record on their behalf |
| **Retrieval workflow** | Who taps "Request Now"? And how is the customer told the car is ready, when push is the only channel? |

### Three viable paths

| Option | How it works | Cost | Verdict |
|---|---|---|---|
| **A · Staff-proxied request** | Customer phones or walks up; valet or manager raises the request on their behalf. Record exists, no login | Low — one new action on the staff side | **Recommended.** Preserves the queue's integrity: every car in the garage is on the board regardless of how it got there |
| **B · Call-ahead only, outside the app** | These customers stay on the current manual process entirely | Zero build | Rejected — the board stops being the single source of truth, which is the product's value |
| **C · Phone-based request (IVR / keypad)** | Customer calls a number, enters their unit number | High; and the client ruled out SMS, so a telephony channel is off-thesis | Defer |

**Recommendation *(proposed)*: Option A.** Add a `contact_mode` field to the customer
record (`app` \| `assisted`), let staff raise requests for `assisted` customers, and
mark those requests on the board so the valet knows to walk out and tell the person
rather than relying on a push notification that will never arrive.

That last part matters: **the notification design assumes push.** For assisted
customers, "Ready" has to become a physical hand-off, and the board must say so.

---

## 8. Data retention

The client split this cleanly into two independent things. The prototype's
"approximately 7 days" copy describes only the first.

```
  request COMPLETED
        │
        ├──► valet board "Recently Completed"  ──► drops off after 2–3 days
        │    manager Request History               (client-stated window)
        │
        └──► backend repository                ──► retained PERMANENTLY
                                                   metrics · complaints
                                                   legal · vehicle disputes
```

> *"Full historical activity retained permanently in the backend repository."*
> *"Records older than two or three days can drop off the valet view, since the platform
> is not doing billing."*

**Nothing is deleted.** The UI window is a view concern; retention is indefinite behind
it. Make `valet_history_visible_days` configurable (default 3) and keep it entirely
separate from any deletion policy.

This creates an obligation the brief itself flags as a risk: indefinite retention is
defensible for disputes and legal support, but it **needs a written retention and access
policy** — particularly given the deliberate decision to withhold phone numbers from
valets. Drafting that policy is in scope, not an afterthought. See doc 13 §4.
