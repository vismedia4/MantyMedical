# 14 — Open Questions

Everything the screenshots could not settle. Work through the **Blocking** section with
the product owner before sprint 1; the rest can be decided as the relevant work comes up.

Each item carries a recommendation so the meeting is a yes/no, not a discussion.

---

## Blocking — decide before writing code

### Q1. Where does the customer actually request their car?
No screen shows a "Request my car" control, yet requests plainly originate with the
customer. The Home screen's vehicle card is fully occupied by an existing request.
**Recommendation:** a full-width primary button inside each vehicle card, replaced by
the live-status strip while a request is open.
*Impacts: doc 06 · C3, the customer's entire primary flow.*

### Q2. What moves a request from `ready` to `completed`?
No observed control produces it, but the state exists in history — and the activity
feed shows a completion attributed to a *manager*, suggesting the override was the only
path in the prototype.
**Recommendation:** an explicit valet **Complete / Picked up** action, plus auto-complete
after N hours to prevent stuck rows, logged distinctly.
*Impacts: doc 04 §1, valet card actions, history accuracy.*

### Q3. Who assigns the vehicle identifier (decal / apartment / stall)?
The customer never enters it, yet `PP-1310` appears on a pending approval for a vehicle
the customer submitted.
**Recommendation:** the manager assigns it during approval; the approval UI needs an
identifier field. Consider auto-suggesting the next sequential value per location.
*Impacts: doc 06 · C7, doc 08 · M2, the approve endpoint.*

### Q4. Is per-location configuration or system-wide configuration the source of truth?
Operational policies present as system-wide (Admin only); chime settings present as
per-location (Manager + Admin). The Admin settings screen shows both under a location
dropdown, which is ambiguous.
**Recommendation:** implement everything as **system default + per-location override**,
and label each control's effective scope. Satisfies both screens; avoids a migration.
*Impacts: doc 03 config entities, both settings screens, the policy API.*

### Q5. Which tablet, exactly?
Audio autoplay, kiosk mode, screen timeout, offline queueing, and PWA install all
resolve differently on iPadOS vs. Android.
**Recommendation:** pin the model before sprint 1 and buy two for the team.
*Impacts: doc 12 §1, doc 13 §1 and §8, essentially all valet work.*

---

## High — decide during design

### Q6. Do scheduled requests auto-promote to the active queue?
**Move to active** is manual. Whether a request also appears automatically at its
scheduled time is unspecified — and if it does not, a scheduled pickup is only as
reliable as a valet remembering to look at the Tomorrow column.
**Recommendation:** auto-promote at `scheduled_for` minus a configurable lead time
(default 30 min); keep **Move to active** as the manual early pull.

### Q7. Can a customer cancel after a valet has accepted?
**Recommendation:** yes in `pending`; yes with a confirmation dialog in `accepted`
(the valet must be told); no in `ready` — the car is already at the door.

### Q8. Do notes attach to the vehicle or the request?
The UI puts them in the request modal; the example content ("plug in EV after return")
and the Admin policy copy ("notes on customers/vehicles") both point at the vehicle.
**Recommendation:** attach to the **vehicle**, surface in request detail.

### Q9. What does **Disable** on a location do to existing customers?
Confirmed: it hides the location from registration. Unconfirmed: whether existing
customers can still request cars.
**Recommendation:** disabling stops new requests and new enrollment, preserves accounts
and history, and is reversible. Warn on the confirmation dialog.

### Q10. Can a manager switch between their assigned locations?
Hector Flores manages two locations; the prototype header is a static label.
**Recommendation:** yes — the header must be a picker for managers with more than one.
*(Treated as a requirement in doc 05, not a question, but confirm.)*

### Q11. Does the manager get a view of the live valet board?
A manager sees active requests on their dashboard but never the board their valet sees.
**Recommendation:** yes, read-only, with the override controls they already have.

### Q12. Do vehicle photo uploads need approval?
**Add photo** sits outside the approval row, implying immediate effect.
**Recommendation:** immediate, but visible in the activity log. Revisit if operators
report abuse.

---

## Medium — decide before the relevant screen is built

### Q13. What does the **Review** action on a new registration open?
**Recommendation:** a full submission detail view with Approve/Reject in context.

### Q14. Is a rejection reason captured and shown to the customer?
**Recommendation:** yes — optional free text, surfaced to the customer. Silent rejection
generates support calls.

### Q15. Is `PP-####` a Pioneer convention or free text?
**Recommendation:** free text with a per-location prefix template and sequence, so
garages get `PP-1042` and condos get `4B`.

### Q16. What are the full option sets for chime interval and volume?
**Recommendation:** interval `3 / 6 / 10 / 15 / 30 seconds`; volume `Low / Medium / High`.

### Q17. Is a `cancelled` request visible to staff?
**Recommendation:** yes — it must vanish from the active board but appear in history,
otherwise a valet who already walked to the car has no explanation.

### Q18. Can a customer be attached to more than one location?
The model assumes one. A resident with a condo and an office garage would need two.
**Recommendation:** allow one for v1; design the schema (`UserLocation` already exists)
so many is possible later.

### Q19. Does the customer bell have a real notification list?
The icon exists; the screen does not.
**Recommendation:** yes — required scope, see doc 12 §3.

### Q20. Is the River North `@state-manager` account a seed bug or the intended model?
Consistent with one manager login spanning two locations.
**Recommendation:** confirm; the many-to-many model in doc 02 assumes it is intentional.

---

## Low — capture, don't block

- **Q21.** Should Office Console location tiles link into the location? *(Recommend: yes.)*
- **Q22.** Does the app need an "All locations" scope option in the admin header? *(Recommend: yes, default on Console.)*
- **Q23.** Is there a customer profile/settings screen? *(Recommend: yes — phone, email, password.)*
- **Q24.** Export from Request History? *(Recommend: CSV — dispute resolution ends in "send me the record".)*
- **Q25.** Dark mode? *(Recommend: defer.)*
- **Q26.** Spanish localisation for valet staff? *(Recommend: externalise strings now, translate later.)*
- **Q27.** Multi-vehicle scheduling — which vehicle does a scheduled pickup apply to? *(Recommend: vehicle selector on the Schedule screen; blocking only for customers with >1 vehicle.)*
- **Q28.** Does the QR code deep-link to an installed app, a store listing, or the web app? *(Recommend: a smart link that resolves to whichever is available.)*

---

## Confirmed scope exclusions

Stated in the prototype UI or absent by consistent design. Listed so nobody
re-litigates them mid-build.

| Excluded | Evidence |
|---|---|
| Advanced analytics dashboards | *"(Advanced analytics dashboards are out of scope.)"* — Activity History subtitle |
| Payments, billing, tipping | No pricing, invoice, or payment surface in 22 screens |
| Individual valet identity / rostering / dispatch | Shared station accounts only; no assignment concept |
| Vehicle telematics / GPS | Parking location is free text a valet types |
| Customer-to-valet chat | No messaging surface; phone is the escalation path |
