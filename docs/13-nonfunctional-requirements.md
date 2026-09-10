# 13 — Non-Functional Requirements

## 1. The shared valet tablet — the dominant security problem

*"One login stays signed in on the tablet."*

That single design decision creates most of the security surface in this product. An
always-authenticated device sits in a semi-public garage, holding a directory of
resident names, phone numbers, vehicles, and — via parking location — **where each
resident's car is parked right now**. For a residential building, that is a stalking
and vehicle-theft toolkit.

### Required controls

| Control | Requirement |
|---|---|
| **Device binding** | Bind the station session to a registered device. A stolen credential must not open the board from an arbitrary browser |
| **Data minimisation on screen** | The prototype already does this well: first names on cards, full name and phone only inside the detail modal. **Preserve it** — do not "improve" the board by adding surnames |
| **Screen timeout** | Board dims/locks after N minutes idle; a **short PIN** (not the full password) returns to the board. Never sign the station out — the whole point is that it stays available |
| **Immediate revocation** | Suspending a valet account terminates live sessions at once and the tablet drops to a lock screen |
| **No customer PII export** | No download, copy-all, or print on the valet directory |
| **Session audit** | Log station sign-ins with device and IP. Reveal of credentials is itself an audit event |
| **Kiosk mode** | Deploy in managed kiosk/guided-access mode: no other apps, no browser navigation, no address bar |

### Also required, and easy to miss

- **Physical placement guidance for operators.** A board angled toward a public lobby is
  a data leak no software control can fix. Write it into the deployment guide.
- **Rotation on staff turnover.** Shared credentials outlive the people who knew them.
  Force a rotation cadence — quarterly, and on any departure.

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
| Vehicle photos | Customers | May capture plates, interiors, faces |
| Parking location | Customers | **Real-time physical location of a person's vehicle** |
| Retrieval history | Customers | **A movement pattern** — when they leave and come home |

The last two are the ones to be careful about. Retrieval history over weeks is a
behavioral profile of a resident's comings and goings.

### Requirements

- **Purpose limitation.** History exists for dispute resolution — the product says so.
  Do not repurpose it for analytics without a separate decision and disclosure.
- **Retention.** Operational visibility is ~7 days. Define separately, and in writing:
  how long the `ActivityEvent` log is kept, and how long request records survive
  deletion from staff views. Recommendation *(proposed)*: operational 7 days, audit 12
  months, then anonymise.
- **Deletion / export.** Customer-initiated account deletion and data export. Multi-state
  operation (IL, FL, NY) means state privacy regimes apply; NY and FL both have active
  consumer-privacy obligations. **Get counsel before launch** — flagged, not resolved,
  here.
- **Photo handling.** Strip EXIF (including GPS) on upload. Serve from signed,
  short-lived URLs, never a public bucket.
- **Cross-location isolation.** A manager at River North must not read State Street
  customers. Test this explicitly — it is the failure mode that turns one bad token into
  a portfolio-wide breach.

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
| Customer | iOS Safari 16+, Chrome Android 110+. Installable PWA |
| Valet | The specific tablet model chosen for deployment — **pin it and test on it**. Assume a long-lived device that may lag on OS updates |
| Manager / Admin | Evergreen Chrome, Edge, Safari, Firefox. Desktop ≥ 1280px, usable to 1024px |

Name the valet tablet model before the first sprint. Every hard constraint in this
document — audio autoplay, kiosk mode, screen timeout, offline behavior — resolves
differently on iPadOS than on Android, and the choice is not reversible cheaply.

---

## 9. Internationalisation & localisation *(proposed)*

Not present in the prototype; likely relevant.

- **Timezones are already a live requirement**, not a future one — the portfolio spans
  Central and Eastern time today.
- Valet-stand staff in a multilingual market may need **Spanish** at minimum.
  Externalise strings from day one; retrofitting i18n is expensive.
- Currency and payments are out of scope, which removes the hardest part.
