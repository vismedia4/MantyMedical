# 14 — Open Questions

> Updated against the **September 10, 2026 requirements session**
> ([00 — Client Requirements](00-client-requirements.md)). Eleven of the original
> twenty-eight questions are now closed — see §Resolved at the bottom.

Two items are **blocking**, and the client's own brief says so about both. Everything
else can be decided as the relevant work comes up. Each item carries a recommendation so
the meeting is a yes/no, not a discussion.

**Tuesday, September 15, 12:00 noon** is the decision point. Q1 and Q2 belong on that
agenda — the brief already puts them there.

---

## Blocking — the client's own list

### Q1. Customers without smartphones
> *"Discussed at length. QR-code assistance and manager-supported setup were considered,
> and a manual override path was identified as a likely requirement. **Not resolved.
> Needs a decision before build** — it affects the data model, the manager UI and the
> retrieval workflow."*

This blocks because it is a **data-model question**, not a screen. The system assumes a
customer record *is* an authenticated user with a push token. A monthly parker without a
smartphone has neither.

**Recommendation: staff-proxied requests.** Add `contact_mode` (`app` | `assisted`) to
the customer record; let valets and managers raise requests on behalf of assisted
customers; flag those requests on the board so the valet knows *Ready* is a physical
hand-off, not a push notification. Full options analysis in [04 — Workflows](04-workflows-and-state.md) §7.

*Impacts: data model, manager UI, valet board, the entire notification design.*

### Q2. Manager-absence backup
> *"Jonathan's only prototype concern. The administrator override path needs an explicit
> design — who is notified, what SLA applies to pending approvals, and whether approvals
> can escalate automatically."*

Four sub-decisions, with recommendations in [04 — Workflows](04-workflows-and-state.md) §6:
SLA of 4 business hours for registrations and 24h for vehicle changes; notify the Office
Admin; **escalate automatically, not on pull**; the manager keeps the ability to act
after escalation. Plus a planned-absence switch, which converts the common case from an
exception into a normal path.

*Impacts: doc 08 · M7, doc 09 · A6, approval state machine, notifications.*

---

## Blocking — engineering, not in the brief

### Q3. Which tablet, exactly?
Audio autoplay, kiosk mode, screen sleep, wake locks, offline queueing and
background-notification behavior all resolve differently on iPadOS vs. Android. The brief
names valet-tablet reliability as a standing risk and reliability is the project's
premise.
**Recommendation:** pin the model before sprint 1 and buy two for the team.
*Impacts: doc 12 §1, doc 13 §1 and §8 — effectively all valet work.*

### Q4. What moves a request from `ready` to `completed`?
Unresolved in the prototype and not raised in the session. The activity feed shows a
completion attributed to a *manager*, suggesting the status override was the only path.
**Recommendation:** an explicit valet **Complete / Picked up** action, plus auto-complete
after N hours to prevent stuck rows, logged distinctly. Note this interacts with the
2–3 day valet window — a request stuck in `ready` will age off the board without ever
completing.
*Impacts: doc 04 §1, valet card actions, history accuracy.*

### Q5. Native, hybrid, or native shell?
App-store deployment is required, so the customer surface is native. The manager and
admin consoles are plainly web. Whether they share a codebase materially changes the
estimate presented Tuesday.
**Recommendation:** React Native for the customer app, responsive web for the consoles
and the valet board, sharing types and API client. Decide before costing.
*Impacts: doc 05, and every number in Tuesday's proposal.*

---

## High — decide during design

### Q6. Manager history window vs. valet history window
The client said 2–3 days about the **valet** view specifically, with the rationale
*"since the platform is not doing billing."* A manager doing operational review and
dispute resolution has a different need, and backend retention is permanent anyway.
**Recommendation:** valets 3 days; managers 30 days plus date-range search into the full
archive; admins unlimited.

### Q7. What replaces the valet's phone escalation?
Phone numbers are now barred at the valet role — correctly. But the phone *was* the path
when the app could not resolve a situation: a car that will not start, a customer who
never showed.
**Recommendation:** a **"Notify manager"** action on the request. The valet raises the
flag; the manager, who holds phone access, makes the call. Endpoint already sketched in
doc 11.

### Q8. Do scheduled requests auto-promote to the active queue?
**Move to active** is manual. If there is no automatic promotion, a scheduled pickup is
only as reliable as a valet remembering to look at the Tomorrow column — which is the
class of failure the product exists to eliminate.
**Recommendation:** auto-promote at `scheduled_for` minus a configurable lead time
(default 30 min); keep **Move to active** as the manual early pull.

### Q9. Is the *Ready* notification toggleable at all?
The client made it the default and required notification, and push is now the only
channel.
**Recommendation:** render it **on and locked** in MVP with an explanatory caption. Revisit
if customers complain, which they will not.

### Q10. Generic vehicle image mapping — what granularity?
VisMedAI owns defining the brand/model/colour mapping set (client action item 04).
**Recommendation:** body-style × colour (~150 assets), not make × model (unbounded).
Store the inputs and resolve at render time so the mapping improves without a migration.
Degrade to a neutral silhouette, never a broken image. Start this early — it has a long tail.

### Q11. Is a `cancelled` request visible to staff?
Cancellation is now `pending`-only, which narrows but does not eliminate the case: a
customer can cancel in the seconds before a valet taps Accept.
**Recommendation:** it disappears from the active board and appears in history. If a valet
had already started walking, the board must say why the card vanished.

### Q12. Trademark clearance on Crew, Console and Record
Identity 1.1 states the three names are proposals and asks for clearance *"in Illinois and
federally before first use."* Passport is already in the codebase, so it is the one
carrying live exposure.
**Recommendation:** clear Passport first and immediately; Crew, Console and Record before
either is used in a store listing or on any customer-facing surface.

### Q13. Where does the bug-reporting widget live?
> *"Reposition it as an internal bug-reporting tool, not a general customer feedback
> channel. Clarify intent and adjust its presentation."*

**Recommendation:** internal and staging builds only, behind a flag, visible to staff
roles. Never in the customer app-store build — an app-store reviewer seeing a
screenshot-capture widget is an avoidable rejection risk.

---

## Medium — decide before the relevant screen is built

### Q13. What does **Review** on a new registration open?
**Recommendation:** the full submission with Approve/Reject in context, and an **editable
identifier field** so the manager can correct the decal / unit number the customer typed.

### Q14. Is a rejection reason captured and shown to the customer?
**Recommendation:** yes — optional free text, surfaced to the customer. Silent rejection
generates support calls to a manager who is deliberately not on site.

### Q15. What are the full option sets for chime interval and volume?
**Recommendation:** interval `3 / 6 / 10 / 15 / 30 seconds`; volume `Low / Medium / High`.
Sound design itself goes to Jonathan for review — he flagged it personally.

### Q16. Does **Disable** on a location stop service for existing customers?
Confirmed: it hides the location from registration. Unconfirmed: whether existing
customers can still request cars.
**Recommendation:** disabling stops new requests and new enrollment, preserves accounts and
history, and is reversible. Warn on the confirmation dialog.

### Q17. Does the manager get a read-only view of the live valet board?
Managers work remotely and hold status-override authority, but cannot see what their
valet sees.
**Recommendation:** yes, read-only, with the override controls they already have.

### Q18. Is the River North `@state-manager` account a seed bug or the intended model?
Consistent with one manager login spanning two locations, which the many-to-many model
assumes.
**Recommendation:** confirm with the client; it is a one-line answer.

### Q19. Location-level average fulfilment time — when?
Named in the brief as a *"future consideration."* Not MVP, but the data model should not
preclude it.
**Recommendation:** ensure `accepted_at` / `ready_at` / `completed_at` are captured from
day one — they are — and defer the reporting surface entirely.

---

## Low — capture, don't block

- **Q20.** Should Office Console location tiles link into the location? *(Recommend: yes.)*
- **Q21.** An "All locations" scope option in the admin header? *(Recommend: yes, default on Console.)*
- **Q22.** Customer profile/settings screen — phone, email, password? *(Recommend: yes. Also required for app-store account deletion.)*
- **Q23.** Export from Request History? *(Recommend: CSV — dispute resolution ends in "send me the record".)*
- **Q24.** Dark mode? *(Recommend: defer.)*
- **Q25.** Spanish localisation for valet staff? *(Recommend: externalise strings now, translate later.)*
- **Q26.** Which vehicle does a scheduled pickup apply to? *(Recommend: vehicle selector on the Schedule screen; multiple vehicles per customer is confirmed, so this is real.)*
- **Q27.** Does the QR code deep-link to the store listing or the installed app? *(Recommend: a smart link that resolves to whichever is available.)*
- **Q28.** Per-tenant custom domains for licensed operators? *(Recommend: defer with the rest of white-label.)*

---

## Resolved by the September 10 session

| Question | Resolution |
|---|---|
| Where does the customer request their car? | **Confirmed** — *"Customer taps Request Now"* |
| Can a customer cancel after acceptance? | **No** — cancellation is permitted *before acceptance only* |
| Who assigns the vehicle identifier? | **The customer**, at registration; the manager verifies at approval |
| Do photo uploads need approval? | **Moot** — no uploads. Generic images only |
| Can a customer belong to more than one location? | **No** — records are scoped to the garage |
| Is `PP-####` a fixed convention? | **No** — one primary identifier per location, whichever that property uses |
| Does the customer bell have a real notification list? | **Yes**, plus a preference toggle |
| Multiple vehicles per customer? | **Yes** |
| Can a manager create customer records directly? | **Yes** — manager-supported provisioning |
| Do managers need to be on site? | **No** — remote operation is an explicit requirement |
| Is SMS a channel? | **No** — in-app push only |
| What is the object store for "evidence uploads"? | **Verified Custody Record** — condition at intake and return, the fourth product in the family. Staff-captured, not customer uploads. Scope it on its own terms: doc 13 §4 |
| Is "Pioneer Connect" the product name? | **No** — the product is **Pioneer Passport**. Crew, Console and Record are proposed sibling names pending trademark clearance |

---

## Confirmed scope exclusions

Client-stated. Listed so nobody re-litigates them mid-build.

| Excluded | Source |
|---|---|
| Billing / payments | *"Not a billing system"* |
| Guests and transient parkers | Separate payment workflow; deferred to workstream 3 |
| Broadcast messaging / location-wide alerts | *"Not universal location-wide alerts"* |
| Customer photo uploads | Generic images instead |
| SMS notifications | Push only |
| Advanced analytics dashboards | Out of MVP; average fulfilment time is a named future item |
| Individual valet identity / rostering / dispatch | Shared station accounts only |
| Vehicle telematics / GPS | Parking location is free text |
| White-label theming, operator-facing admin | Deferred with the licensing surface |
