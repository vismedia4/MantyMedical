# 13 — Non-Functional Requirements

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
> **Changed:** retention is permanent, not 7 days (§4.4); no photo uploads, so the
> photo-privacy section is retired (§4.1); valets cannot see phone numbers (§4.2);
> app-store deployment is required (§4.7); tenant isolation is a day-one mandate (§6.3).

## 0. Tenant isolation — the licensing mandate

> *"The app should be designed as a product other parking operators can license, not a
> Pioneer-only internal tool."*

The brief's own risk register frames the tradeoff and lands on the answer:

> *"Multi-tenancy, per-tenant branding and per-tenant credentials are architectural
> decisions that are cheap now and expensive later — but they are not free in the MVP.
> Recommendation: build true tenant isolation into the data model from day one; defer
> white-label theming and any operator-facing admin surface."*

**Adopted.** What that means concretely:

| In MVP | Deferred |
|---|---|
| `tenant_id` on every table | Per-tenant theming UI |
| Tenant scoping enforced at the data-access layer, not in controllers | Operator-facing admin surface |
| Cross-tenant isolation tests in CI | Per-tenant custom domains |
| Brand values in `Tenant.theme`, never hard-coded | Tenant self-service onboarding |

**Test isolation like a security control, because it is one.** In a single-operator app,
a missing `WHERE tenant_id` is a bug. In a licensed product it is one operator reading
another operator's residents. Write the negative tests first: a token from tenant A must
return 404 — not 403 — for every tenant B resource.

And keep the name out of the code. *"Company structure, product name and branding must
stay flexible."* No `pioneer_` table prefixes, no `/api/pioneer/...`, no brand strings
outside the theme layer.

---

## 1. The shared valet tablet — the dominant security problem

*"One login stays signed in on the tablet."*

That single design decision creates most of the security surface in this product. An
always-authenticated device sits in a semi-public garage, holding a directory of resident
names, vehicles, and — via parking location — **where each resident's car is parked right
now**. For a residential building, that is a stalking and vehicle-theft toolkit.

**The client already removed the worst of it.** Phone numbers are barred at the valet
role: *"view customer phone numbers — called out by Jonathan as a privacy restriction."*
That instinct is correct and the remaining controls follow the same logic.

### Required controls

| Control | Requirement |
|---|---|
| **Device binding** | Bind the station session to a registered device. A stolen credential must not open the board from an arbitrary browser |
| **Data minimisation on screen** | First names on cards, full name only inside the detail modal, **no phone numbers at all**. Preserve it — do not "improve" the board by adding surnames or contact details |
| **Phone numbers excluded at the API tier** | Client requirement. Enforce in the valet serializer with a contract test, not in the template (doc 11) |
| **Screen timeout** | Board dims/locks after N minutes idle; a **short PIN** (not the full password) returns to the board. Never sign the station out — the whole point is that it stays available |
| **Immediate revocation** | Suspending a valet account terminates live sessions at once and the tablet drops to a lock screen |
| **No customer PII export** | No download, copy-all, or print on the valet directory |
| **Session audit** | Log station sign-ins with device and IP. Reveal of credentials is itself an audit event |
| **Kiosk mode** | Deploy in managed kiosk/guided-access mode: no other apps, no browser navigation, no address bar |

### Also required, and easy to miss

- **Physical placement guidance for operators.** A board angled toward a public lobby is
  a data leak no software control can fix. Write it into the deployment guide — and note
  that in a licensed product, *the operator* follows that guide, not Pioneer.
- **Rotation on staff turnover.** Shared credentials outlive the people who knew them.
  Force a rotation cadence — quarterly, and on any departure.

### Device reliability is a named client risk, not just a security matter

> *"The persistent chime is the operational backbone of the workflow. Device sleep
> behavior, connectivity loss and background-notification handling on dedicated tablets
> will determine whether the app actually beats ElimaWait on reliability — which is the
> entire premise for replacing it. Worth an explicit line item."*

Treat it as one. Required behaviors on the chosen tablet, all verified on the actual
hardware:

| Behavior | Requirement |
|---|---|
| **Screen sleep** | The board must never sleep during operating hours. Kiosk/guided-access policy plus a wake lock |
| **App backgrounding** | If the OS backgrounds the app, the chime must survive or the app must return to foreground on a new request |
| **Wi-Fi drop** | Reconnect with backoff; unmissable stale-state banner; full board refetch on reconnect |
| **Overnight reboot** | Auto-relaunch into the board, re-arm audio permission, and alert if it cannot |
| **Audio permission lost** | Persistent "tap to enable alerts" bar, and a heartbeat that tells the manager the stand is silent |

This is the single highest-value test matrix in the project. It is also why the tablet
model must be pinned before the first sprint (doc 14, Q3).

---

## 2. Credential handling

The Add Location flow accepts a manager and valet password in a plain form, and the
system *"provisions immediately … nothing is emailed."*

This is a defensible operational choice for staff without work email, but it means an
admin knows every station password. Mitigations:

- **Force a change on first sign-in** for personal manager accounts *(proposed)*. Do
  **not** force it for station accounts — a kiosk that demands a password change on
  reboot will be defeated with a sticky note.
- **Generate, don't type.** Offer a "generate strong password" control, displayed once,
  with a copy button. Typed passwords will be `Wacker2026`.
- **Show once.** Password reveals and resets return plaintext exactly once and are
  written to the audit log with the actor's identity.
- **Enforce a minimum policy** server-side regardless of who is typing.
- **MFA for Office Admin** *(proposed)*. That role can create locations, mint staff
  accounts, and read every customer record across the portfolio. It is the account worth
  attacking.

---

## 3. The 6-digit access code

A 6-digit numeric code is **one million possibilities** and it is the sole gate on
enrollment at a location.

| Risk | Control |
|---|---|
| Brute force via `resolve-code` | Strict rate limiting per IP and per session; exponential backoff; CAPTCHA after a few failures |
| Enumeration across locations | Never reveal *which* location a wrong code doesn't match; uniform error and uniform response time |
| Leaked printed code | **Regenerate** exists — make it prominent and instant |
| Stale codes | *(proposed)* optional expiry; alert an admin on unusual enrollment volume at one location |

Remember the code alone does not grant service: registration still lands in `pending`
and needs manager approval while that policy is on. **Keep that policy on by default** —
it is the compensating control that makes a 6-digit code acceptable.

---

## 4. Privacy & data protection

### Personal data held

| Data | Subjects | Sensitivity |
|---|---|---|
| Name, email, phone | Customers | Standard PII |
| Home address by proxy | Residential customers | **The location *is* their home** |
| Vehicle make/model/colour/identifier | Customers | Identifying; links a person to a car |
| ~~Vehicle photos~~ | — | **Eliminated by design.** Generic images only — *"reduces data load and avoids privacy exposure"* |
| Parking location | Customers | **Real-time physical location of a person's vehicle** |
| Retrieval history | Customers | **A movement pattern** — when they leave and come home |

The last two are the ones to be careful about. Retrieval history over weeks is a
behavioral profile of a resident's comings and goings.

### Requirements

- **Retention is permanent — and that is a client decision, not an oversight.**

  > *"Full historical activity retained permanently in the backend repository. Purposes:
  > metrics and reporting, customer complaints, legal support, and vehicle-related
  > disputes."*

  Two independent windows: the **valet view** shows 2–3 days; the **backend** keeps
  everything indefinitely. Nothing is deleted by the retention job — it only narrows a view.

- **Indefinite retention obligates a written policy.** The brief names this as a risk:

  > *"Indefinite retention for legal and dispute purposes is defensible, but it needs a
  > written retention and access policy — especially given the deliberate restriction of
  > phone numbers from valets. The policy belongs in scope, not as an afterthought."*

  In scope. It must state: what is retained, for how long, who may access it, under what
  authorisation, how access is logged, and how a customer exercises deletion rights
  against a permanent archive. The last one is the hard part and needs counsel —
  "permanent" and "right to erasure" are in tension, and the resolution is usually a
  documented legal-basis carve-out plus pseudonymisation of everything outside it.

- **Purpose limitation.** History exists for metrics, complaints, legal support and
  vehicle disputes — the client enumerated them. Do not repurpose it beyond that list
  without a separate decision and disclosure.
- **Deletion / export.** Customer-initiated account deletion and data export. Multi-state
  operation (IL, FL, NY) means state privacy regimes apply; NY and FL both have active
  consumer-privacy obligations. **Get counsel before launch** — flagged, not resolved,
  here.
- **No *customer-supplied* media.** The generic-image decision removes an entire class of
  privacy exposure — EXIF/GPS leakage, plates and faces in uploads, moderation burden and
  storage cost. It is the cheapest privacy win in the product.

- **Staff-captured custody evidence is a different thing, and it is real.** Identity 1.1
  names a fourth product, **Record — Verified Custody Record™**, *"condition at intake and
  return, sealed,"* and the platform's local stack already runs object storage for
  "evidence uploads." That is staff photographing vehicle condition, not customers
  uploading pictures of their car, and it does not breach the rule above.

  It does need its own treatment before it ships, because it is the most sensitive data in
  the system: dated images of a named resident's vehicle, at a known address, tied to a
  timestamped custody chain. Required decisions — **who captures, who can view, how long
  it is retained, whether it inherits the valet phone-number restriction, and what
  "sealed" means technically** (hashing, write-once, tamper-evidence). Treat "sealed" as a
  product claim that has to be defensible if it is ever produced in a dispute.
- **Cross-location isolation.** A manager at River North must not read State Street
  customers. A customer record belongs to exactly one location — *"location-specific
  customer databases."* Test explicitly.
- **Cross-tenant isolation.** See §0. In a licensed product this is the failure mode that
  turns one bad token into a breach across operators.

---

## 5. Reliability

The customer-visible promise is small and absolute: **a request never disappears.**

| Requirement | Target |
|---|---|
| Request durability | A submitted request is persisted before the client is told it succeeded. No optimistic-only writes |
| Idempotency | Retried accept/ready/create must not double-fire |
| Board availability | Valet board target **99.9%** during operating hours |
| Degraded mode | If real-time fails, the board must still function on polling and say so |
| Offline capture *(proposed)* | A valet tapping **Ready** with no network should queue the action locally and sync on reconnect. Failing silently here loses the customer's car status |
| Backups | Daily, with a tested restore. History is the dispute-resolution record; losing it defeats the purpose |

**Single point of failure to name explicitly:** if the tablet is dead, off, or offline,
customers keep submitting requests into a void and nobody is alerted. The heartbeat and
escalation in doc 12 §2 are not nice-to-haves; they are the mitigation for the product's
one systemic failure mode.

---

## 6. Accessibility

Target **WCAG 2.2 AA**.

| Area | Requirement |
|---|---|
| Contrast | Tinted pill fills are the weak point — see doc 10. Audit every tint/text pair at its real size |
| Colour independence | Already correct: every status has a word, not just a colour. Hold the line |
| Touch targets | ≥ 44×44px everywhere; ≥ 56px on the valet board |
| Keyboard | Full keyboard operability on manager and admin desktop screens; visible focus rings |
| Screen readers | Live regions for board changes and status transitions; `aria-label` on the three icon-only controls (bell, ↺ revert, ⋮ kebab) |
| Motion | Honour `prefers-reduced-motion` — especially the incoming-card pulse |
| Audio | The chime is an alert. Pair it with the persistent visual banner *(already done)* so a deaf or hard-of-hearing valet is fully served |
| Text scaling | Layouts must survive 200% zoom. The 4-column board is the risk — collapse to 2 columns |

---

## 7. Performance

| Metric | Target |
|---|---|
| Customer app LCP (4G, mid-range phone) | < 2.5s |
| Valet board initial paint | < 1.5s on the target tablet |
| Board state update after a websocket event | < 200ms |
| Accept → visible state change | < 300ms including round trip |
| Admin tables (1,000 rows) | Paginated server-side; < 500ms per page |

The customer app is opened in a lobby on garage Wi-Fi or a weak cellular signal, and it
is opened for **one action**. Optimise the cold-start path to "request my car" above
everything else.

---

## 8. Browser & device support

| Surface | Target |
|---|---|
| Customer | **Native apps, iOS and Android — app-store deployment is a client requirement.** Target current and current-1 OS versions |
| Valet | The specific tablet model chosen for deployment — **pin it and test on it**. Assume a long-lived device that may lag on OS updates |
| Manager / Admin | Evergreen Chrome, Edge, Safari, Firefox. Desktop ≥ 1280px, usable to 1024px |

Name the valet tablet model before the first sprint. Every hard constraint in this
document — audio autoplay, kiosk mode, screen timeout, offline behavior — resolves
differently on iPadOS than on Android, and the choice is not reversible cheaply.

### App-store review is on the critical path

> *"Two store submissions sit on the critical path to launch and are outside VisualMedia's
> control. Build review cycles into the timeline presented Tuesday rather than absorbing
> them as slippage."*

Practical consequences: budget 1–2 weeks per platform for first submission plus at least
one rejection cycle; enrol in both developer programmes **now**, since account setup and
verification alone can take days; and plan for review-triggering changes (push
permissions, account deletion requirements, privacy nutrition labels) rather than
discovering them at submission. Apple requires an in-app **account deletion** path for
apps with account creation — that is a build item, not a policy checkbox.

---

## 9. Internationalisation & localisation *(proposed)*

Not present in the prototype; likely relevant.

- **Timezones are already a live requirement**, not a future one — the portfolio spans
  Central and Eastern time today.
- Valet-stand staff in a multilingual market may need **Spanish** at minimum.
  Externalise strings from day one; retrofitting i18n is expensive.
- Currency and payments are out of scope, which removes the hardest part.
