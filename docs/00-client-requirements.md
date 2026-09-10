# 00 — Client Requirements & Decision Log

**Source:** *Pioneer Parking Build Brief*, requirements session of **September 10, 2026**
— Jonathan Cohen (Owner / Principal, Pioneer Parking) with VisMedAI Advisory
(Dima, Amal Amaskane). Zoom, screen-shared prototype walkthrough.
Archived at [`source/2026-09-10-pioneer-parking-build-brief.pdf`](source/2026-09-10-pioneer-parking-build-brief.pdf).

This document is the **authority**. Where it disagrees with anything inferred from the
prototype screenshots, it wins, and the rest of the documentation set has been updated
to match.

---

## 1. Why this product exists

Pioneer Parking currently runs valet retrieval on **ElimaWait** at ~$165/month.
Jonathan considers it unreliable and inflexible, with no ownership or control over the
roadmap. He is funding a purpose-built replacement.

Three theses drive every architectural decision that follows:

| Thesis | Consequence for the build |
|---|---|
| **Ownership** — own the platform, the feature set, the data, the economics | No third-party SaaS in the critical path. VisMedAI hosts and maintains |
| **Licensing** — design it as a product other parking operators can license, not a Pioneer-only tool | **Multi-tenant from day one.** Product name and branding must not hard-bind to Pioneer Parking |
| **Sequencing** — retrieval app is the fast, contained win; transient ticketing is the larger project behind it | MVP stays narrow. Do not absorb ticketing scope |

**The premise for the whole project is reliability.** Pioneer is leaving ElimaWait
because it does not work dependably. If the new app is not measurably more reliable in
a real garage, the project has failed on its own terms — regardless of feature count.
That is why valet-tablet reliability is called out as a named risk in §6.

## 2. Three workstreams

| # | Workstream | Status |
|---|---|---|
| **1** | **Valet retrieval app** | Primary. This documentation set |
| **2** | **Website refresh** | Secondary, fast. See [16 — Website Refresh](16-website-refresh.md) |
| **3** | **Transient ticketing digitization** | Explicitly deferred. See [17 — Roadmap Beyond MVP](17-roadmap-beyond-mvp.md) |

**Decision point: Tuesday, September 15, 12:00 noon, Zoom.** VisMedAI presents MVP
scope, timeline and cost, plus website direction, structure, turnaround and cost.
[15 — Delivery Plan](15-delivery-plan.md) is written to feed that meeting.

---

## 3. MVP scope boundaries — stated explicitly

### In scope

- **Registered, approved, recurring monthly customers only** — both residents and
  non-residents of the property.
- Reservation / retrieval requests.

### Out of scope — Jonathan's own narrowing

| Excluded | Why |
|---|---|
| **Guests and transient parkers** | Continue on physical tickets and the existing credit-card process. Separate payment workflow; does not belong in MVP |
| **Billing** | *"Not a billing system."* This is the stated reason valet-side history can be short |
| **Universal location-wide alerts / broadcast messaging** | Jonathan explicitly clarified the app handles requests, not broadcasts |
| **Customer photo uploads** | Replaced by generic vehicle images — see §4 |
| **SMS notifications** | In-app push only, stated directly |

---

## 4. What the brief **changed** in this documentation set

These are corrections, not additions. Each one contradicted something previously
specified from the prototype.

### 4.1 No customer photo uploads — generic vehicle images instead

> *"Generic vehicle images. No customer photo uploads. The system auto-generates or maps
> a generic image from make, model and color. Rationale: reduces data load and avoids
> privacy exposure. VisMedAI to define the brand / model / color to image mapping set."*

The prototype's **Add photo** control and the `No photo` placeholder are both gone. The
vehicle image is **derived**, not uploaded.

**Affects:** doc 03 (Vehicle entity), doc 06 · C6/C7, doc 08 · M3, doc 10 (component),
doc 11 (photo endpoints deleted), doc 13 (EXIF/photo-privacy section deleted).
**New work:** VisMedAI owns defining the make/model/colour → image mapping set. This is
a real deliverable with a long tail — it is action item 04 on the VisMedAI list.

### 4.2 Valets must not see customer phone numbers

> *"CANNOT: edit customer or vehicle data; **view customer phone numbers** — called out
> by Jonathan as a privacy restriction. Phone access is preserved for authentication and
> management at higher role levels."*

The prototype's valet request-detail modal displays `Phone (312) 555-0188`. **That is a
privacy violation under the client's stated policy and has been removed from the spec.**

**Affects:** doc 02 (permission matrix), doc 07 · V2, doc 11 (`RequestStaff` serializer
must split — valet tier excludes phone).
**Consequence to resolve:** the phone was the escalation path when the app fails. With
it removed, the valet needs an alternative — see Q7 in §5.

### 4.3 Valet history is 2–3 days, not ~7

> *"Jonathan indicated records older than two or three days can drop off the valet view,
> since the platform is not doing billing."*

The prototype says "approximately 7 days." The client says 2–3.

### 4.4 Backend retention is **permanent**, not 7 days

> *"Full historical activity retained permanently in the backend repository. Purposes:
> metrics and reporting, customer complaints, legal support, and vehicle-related
> disputes."*

The prototype's "~7 days" describes **valet-facing visibility only**. Retention is
indefinite behind it. My earlier recommendation (7 days operational, 12 months audit,
then anonymise) is **wrong** and has been replaced.

**Affects:** doc 03, doc 04 §6, doc 13 §4. Creates a new obligation: a **written
retention and access policy**, named as a risk in the brief.

### 4.5 In-app push only — no SMS

> *"In-app push notifications only. No SMS. Jonathan stated this preference directly."*

My doc 12 listed SMS under "consider." Removed. This raises the reliability bar on push:
it is now the **only** channel to the customer, and *Ready for pickup* is the
notification the product exists to deliver.

### 4.6 The customer supplies the identifier at registration

> *"Customer submits registration details — name, vehicle information, unit / decal
> number."*

This resolves an open question the other way from my recommendation. The customer types
their own decal / apartment / unit number during sign-up; the manager verifies it when
approving rather than assigning it.

### 4.7 The app must ship to app stores

> *"App store deployment required."*

The prototype is a web app and I assumed an installable PWA. Two store submissions now
sit on the critical path and are outside VisMedAI's control.

### 4.8 The feedback widget is an internal bug-reporting tool

The red chat bubble visible in the bottom-right corner of every prototype screenshot is
the prototype's comment-and-screenshot feature. Direction: **reposition as an internal
bug-reporting tool, not a customer feedback channel**, and adjust its presentation.
It must not ship in the customer-facing build.

---

## 5. What the brief **resolved**

Open questions from the earlier documentation set, now closed:

| Was | Resolution |
|---|---|
| Where does the customer request their car? | **Confirmed** — *"Customer taps Request Now."* A dedicated action, as recommended |
| Can a customer cancel after acceptance? | **No.** *"Customers must be able to cancel a request before it is accepted."* Cancel surfaces only while `pending` |
| Who assigns the vehicle identifier? | **The customer**, at registration. Manager verifies at approval — see §4.6 |
| Do photo uploads need approval? | **Moot** — no uploads. See §4.1 |
| Can a customer belong to more than one location? | **No.** *"Location-specific customer databases — records are scoped to the garage"* |
| Is `PP-####` a fixed convention? | **No.** *"One primary identifier per location: decal number, apartment number or unit number, whichever that property uses"* |
| Does the customer bell have a real notification list? | **Yes**, plus a **notification-preference toggle** — new required scope, see §7 |
| Multiple vehicles per customer? | **Yes**, confirmed |
| Can a manager create customer records directly? | **Yes** — *"manager-supported provisioning"* |
| Do managers work on-site? | **No** — *"work remotely without being on site"* is an explicit requirement |
| Is analytics really out of scope? | For MVP yes, but **location-level average fulfilment time** is named as a future consideration |

Still open after this session: **what moves a request from `ready` to `completed`**, and
**which tablet model**. Both remain blocking — see [14 — Open Questions](14-open-questions.md).

---

## 6. What the brief **added**

### 6.1 Manager-absence backup — Jonathan's only flagged prototype gap

> *"FLAGGED: must be able to intervene when a garage manager is unavailable — Jonathan's
> single flagged gap in the prototype. **Pending approvals must not stall on manager
> absence.**"*

This was the one substantive objection raised in the entire walkthrough. It needs an
explicit design: who is notified, what SLA applies to pending approvals, and whether
approvals escalate automatically. Specified in [04 — Workflows](04-workflows-and-state.md) §7.

### 6.2 Customers without smartphones

> *"Discussed at length. QR-code assistance and manager-supported setup were considered,
> and a manual override path was identified as a likely requirement. Not resolved. Needs
> a decision before build — it affects the data model, the manager UI and the retrieval
> workflow."*

A real customer segment with no resolution. It is now the top blocking question, because
it implies **customer records that have no authenticated user** — which touches the data
model, not just a screen.

### 6.3 Multi-tenancy for licensing

Not a feature request; an architectural mandate. The brief's own risk register frames
the tradeoff sharply:

> *"Multi-tenancy, per-tenant branding and per-tenant credentials are architectural
> decisions that are cheap now and expensive later — but they are not free in the MVP.
> Recommendation: build true tenant isolation into the data model from day one; defer
> white-label theming and any operator-facing admin surface."*

**That recommendation is adopted** across this documentation set. See doc 03 (Tenant
entity) and doc 13 (isolation testing).

Practical consequence: **"Pioneer Connect" is a provisional product name.** Do not bake
it, the logo, or the palette into anything but a theme layer.

### 6.4 Notification preferences

*Ready* is the required, default notification. *Retrieving Vehicle* is **opt-in** via a
customer-controlled preference toggle. New screen, new entity, new API surface.

### 6.5 First-name search

> *"Simple first-name search — Jonathan emphasized this specifically as the search
> behavior he wants."*

Not a generic search box. A valet or manager looking at a person standing in front of
them types a first name. Make that the fast path.

### 6.6 Chime sound design

The chime requirement is confirmed and reinforced — *"persistent but not annoying"* — and
the brief notes **the sound design matters to him.** Treat the audio asset as a design
deliverable with client review, not a developer's pick.

---

## 7. Consolidated client action items affecting the build

From the brief's own action list, the items that are engineering scope:

| # | Action |
|---|---|
| 04 | Define generic vehicle-image mappings (brand / model / colour) |
| 05 | Restrict valet access to phone numbers, preserving access for authentication and management |
| 06 | Add customer notification preferences for optional retrieval-status updates |
| 07 | Ensure customers can cancel requests before acceptance |
| 08 | Add a decal / unit-number field to vehicle records |
| 09 | Clarify the comment/screenshot feature as an internal bug-reporting tool; adjust presentation |
| 10 | Consider a manual registration path for customers without smartphones |
| 11 | Design the application with licensing to other operators in mind |
| 12 | Build on a scalable backend with hosting and maintenance support |

All nine are reflected in the updated documentation. Items 10 and 09 remain decisions
rather than implementations — see doc 14.

---

## 8. Risks carried forward from the brief

Reproduced because they are the client-facing framing, and Tuesday's proposal must
address them:

1. **Licensing ambition vs. MVP cost.** Tenant isolation now, white-label theming later.
   State the tradeoff explicitly so it is Jonathan's call.
2. **Permanent retention vs. privacy posture.** Indefinite retention is defensible but
   needs a written retention and access policy — in scope, not an afterthought.
   Particularly given phone numbers are deliberately withheld from valets.
3. **App store review timelines.** Two submissions on the critical path, outside
   VisMedAI's control. Build review cycles into the timeline; do not absorb them as slippage.
4. **Valet tablet reliability.** The persistent chime is the operational backbone. Device
   sleep, connectivity loss and background-notification handling on dedicated tablets
   determine whether the app actually beats ElimaWait — *which is the entire premise for
   replacing it.* Explicit line item.
5. **IP ownership.** If Jonathan funds the build and intends to license the product, IP
   ownership, licence terms and revenue share must be settled in the commercial
   agreement — before code exists.

Risks 1, 2 and 4 are engineering-actionable and are addressed in docs 03, 13 and 12
respectively. Risks 3 and 5 are commercial and belong in Tuesday's proposal.
