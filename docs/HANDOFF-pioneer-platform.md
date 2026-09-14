# Handoff — Pioneer Passport development

Written at the close of the design/documentation phase, to carry continuity into
development sessions on `PioneerParking/pioneer-platform`.

**This file is the authority on what was decided and why. Read it before touching code.**

---

## 1. What the product is

**Pioneer Passport** — a resident requests their vehicle, a valet retrieves it.

| Surface | Build | Status |
|---|---|---|
| Resident app | Native, iOS + Android | Live |
| Valet station | Web, on a tablet at the stand | Live |
| Garage manager console | Web | Phase 2 |
| Office admin console | Web | Phase 2 |

The retrieval loop runs end to end today: a resident requests a car, it reaches the
valet station, status moves through to ready. Pioneer Identity 1.1 is already applied.
What remains is to prove it in a garage and finish it.

### The four roles

- **Resident** — requests the vehicle, watches status, maintains their own vehicle details
- **Valet** — works the queue on a station screen. Sees name, decal, parking location,
  internal note. **Never a phone number.**
- **Garage manager** (phase 2) — approves registrations, overrides status with an audit
  event, manages staff and vehicles at their location
- **Office admin** (phase 2) — administers every location: access codes, users, reports,
  activity archive

---

## 2. Hard constraints — do not violate

These were established by the client-facing work and several were corrections after
mistakes. They are not stylistic preferences.

### Privacy and data
- **Valets must never see customer phone numbers.** They do see names.
- Vehicles are identified by **decal number, not licence plate.**
- The website must not publish garage addresses or anything about residents.

### Facts vs. seed data
- Anything visible in the running app is **synthetic seed data**, not fact.
- Specifically NOT true: "Wacker Drive garage", the resident names, and **"five locations"**.
  That number was counted off prototype seed data. Pioneer runs considerably more.
- Refer to "multiple locations". **Do not state a location count.**

### Client-facing language
- **Never name the other provider**, their prototype, or the specification Pioneer
  already owns, in any client-facing material.
- **Never say the identity was "delivered."** It was VisualMedia's own initiative,
  offered to Pioneer for adoption. They did not ask for it or accept it.
- The **$150–200K benchmark is VisualMedia's own estimate**, never Pioneer's. The client
  has never stated a figure.
- No person-day counts alongside prices in client-facing material.
- The **Sept 10 Build Brief is internal** and must never reach the client.

### Reference material
- `docs/screens/` are another provider's prototype screenshots — **reference only**.
- `docs/mockups/as-built/` are the real application screenshots. These are authoritative
  on: the red P mark, Passport branding on both surfaces, decal numbers, the 3-state
  stepper, and the Queue / Vehicles / Recent navigation.

---

## 3. Pioneer Identity 1.1

Governs the **product and Pioneer's materials** — app, valet station, website, signage,
decals, invoices, correspondence. (It does not govern VisualMedia's own presentation
materials; those use the VisualMedia brand.)

### Colour

| Token | Hex | Use |
|---|---|---|
| Pioneer Red | `#FD2F38` | The mark, and display type 24px and above. **Never body text. Never a button.** |
| Pioneer Navy | `#0B2C5D` | Foundational — logo, headings |
| Signal Blue | `#0048A8` | Actionable elements only: buttons, links |
| Asphalt | `#1A1F33` | Body text |
| Concrete | `#5A6478` | Secondary text |
| Line | `#E2E4E8` | Rules, borders |
| Paper | `#F2F4F8` | Ground |

Proportion target: **Paper 58 / Navy 26 / Blue 8 / Red 6**.

### Typography

| Face | Role |
|---|---|
| Overpass | Display, headings, signage, level markers |
| Overpass Mono | Decal numbers and codes — figures must align column on column |
| Source Sans 3 | Interface — apps, forms, captions. Legible small, in a dim garage. |
| Source Serif 4 | Correspondence — letters and notices a resident receives on paper |

Design tokens: `docs/design-tokens.css`. Full system: `docs/10-design-system.md`.

---

## 4. Commercials

| Item | Price | Notes |
|---|---|---|
| Pilot | **$33,000 – $35,000** | Nine weeks. Includes QR self-registration. |
| Full build | **$55,000 – $60,000** | Everything deferred from the pilot |
| Website | **$9,500 fixed** | Planning range $7,500–$12,500 if scope or assets change |

Do not present these as a prior quote being revised — as of the 15 Sep 2026 session,
Jonathan Cohen had received nothing from us about cost.

---

## 5. Pilot scope

**In scope — enough to run one garage end to end:**
- Resident self-registration by QR code (manager approves before the account goes live)
- Live vehicle status
- The valet queue on a station screen
- Notifications a manager can configure

**Deliberately out of the pilot:**
- Scheduled pickups
- Request history
- Public app store release

These exclusions are what keep the pilot to a timeline the client can hold us to.
Full detail: `docs/19-pilot-and-mvp-scope.md`.

### Success metrics
1. Share of requests that complete without anyone picking up a phone
2. Median minutes from request to vehicle ready
3. Proportion of status notifications that actually reach the resident

---

## 6. Open decisions — not settled

| # | Decision | Our recommendation | Needs |
|---|---|---|---|
| 1 | Residents without smartphones | Staff register and raise requests on their behalf at the desk | Pioneer to confirm |
| 2 | Manager coverage during absences | Approvals escalate automatically when a manager is away | Pioneer to confirm who they escalate to |
| 3 | Valet station tablet | — | Model, mounting, and who purchases. Settled week one — hardware must be on site before testing. |
| 4 | What counts as "complete" | Valet taps Complete at handover | Pioneer to confirm nothing else must happen first |
| 5 | **Which garage pilots** | — | Not established. Needed before week one. |

Full list with context: `docs/14-open-questions.md`.

---

## 7. The specification set

`docs/00` through `docs/19`. `00-client-requirements.md` is the authority and carries the
decision log. Note the warning blocks inside `18-cost-model.md` and
`19-pilot-and-mvp-scope.md` — they record corrections to earlier mistakes.

`docs/16-website-refresh.md` is **parked** — it carries an out-of-scope banner. The
settled website fee is recorded above that banner.

Supporting assets: `docs/mockups/` (rendered product screens + `as-built/` real
screenshots), `docs/deck/` (the client deck source and renders), `docs/chime/` (three
synthesised stand-chime candidates: Marker, Arrival, Signal), `docs/source/`.

`docs/deck/README.md` carries a standing rule: **never name another provider.**

---

## 8. Where things live

| Thing | Location |
|---|---|
| Specification set + assets | `vismedia4/MantyMedical`, branch `claude/app-design-docs-harvest-2k0i9c`, under `docs/` — **to be ported into this repo** |
| Client deck | Canva design `DAHVICM3P5E` — "Pioneer Parking, Inc - Three Project Proposals - VisualMedia", 32 pages |
| Application code | `PioneerParking/pioneer-platform` |
| Website | `PioneerParking/pioneer-website` |

**A Claude Code session cannot hold repos from two different owners** (`vismedia4` and
`PioneerParking`). The specification set must be physically copied into this repository;
it cannot be reached across the boundary.

---

## 9. Context

Presented to Pioneer Parking, Inc. (principal: **Jonathan Cohen**) on
**Tuesday 15 September 2026**, by **VisualMedia, Ltd.** Three proposals: corporate
identity, the platform, the website.
