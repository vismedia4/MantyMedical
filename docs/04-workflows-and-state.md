# 04 — Workflows & State Machines

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
| `pending` → `cancelled` | Customer | **Cancel Request** on the status screen |
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
hours.** Operational history is the product's dispute-resolution backbone; it should
reflect a human confirming the handoff, but must not accumulate stuck `ready` rows
when a valet forgets. Log auto-completions distinctly in the activity feed.

**(b) `cancelled` is inferred.** The customer status screen has a **Cancel Request**
button, but no screen shows a cancelled request. Decide whether cancelled requests
appear on the valet board (they must, if a valet already accepted one) and in history.

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
  │ 3. Customer submits profile + first vehicle (make, model, color)    │
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

Step 2's branching is the reason `identifier_type` must be configuration. The
enrollment form is **generated from the location record**, not hard-coded.

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

**Photo uploads appear to bypass approval** *(inferred)*: **Add photo** sits next to the
editable fields but outside the *"Approval required · Submit change"* row. Confirm —
if photos need moderation, that is a fourth approval kind.

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

## 6. Data retention

*"Completed requests are retained for approximately 7 days for operational review."*

```
  request COMPLETED ──► visible in Manager Request History
                        visible in valet "Recently Completed"
                                │
                          + ~7 days
                                ▼
                        removed from staff-facing views
```

"Retained for ~7 days" describes **staff visibility**, not necessarily deletion. Given
the stated dispute-resolution purpose, the recommendation *(proposed)* is: keep the
`ActivityEvent` audit trail long-term, expire only the operational queue view, and make
the window the configurable `retain_completed_requests_days` policy. Note this
intersects with privacy retention obligations — see doc 13.
