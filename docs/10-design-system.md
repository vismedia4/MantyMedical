# 10 — Design System

All hex values were **sampled directly from the prototype screenshots** at full
resolution. They are exact, not approximations, unless marked.

Machine-readable version: [`design-tokens.css`](design-tokens.css) — drop it in and
consume the custom properties directly.

---

## Colour

### Brand

| Token | Hex | Where observed |
|---|---|---|
| `--brand-red` | `#B13832` | Primary buttons (Sign In, Accept, Submit change), active toggle fill, sidebar active text, column header "INCOMING" |
| `--brand-red-bright` | `#CA3A31` | Card left rail (active), Reject text, link red |
| `--brand-red-logo` | `#E94643` | The "P" logo mark only |
| `--brand-navy` | `#1B1F31` | Headings, customer names, KPI numerals, wordmark "Pioneer" |

Three reds is one too many for a production system. Recommendation *(proposed)*:
keep `#B13832` as the single interactive red and `#E94643` for the logo mark;
retire `#CA3A31` or fold it into the bright ramp.

### Semantic

| Token | Hex | Meaning |
|---|---|---|
| `--success` | `#3B7E44` | **Ready** button, Approve text, `active` pill text |
| `--success-rail` | `#498955` | Completed card left rail |
| `--warning` | `#A75823` | `pending` pill text, `Accepted` badge, approvals callout, prototype banner text |
| `--danger` | `#B13832` | Same as brand red — destructive and primary share a colour |

> **`--danger` and `--brand-red` being identical is a real risk.** "Submit change" and
> "Suspend" render in the same red. Recommendation *(proposed)*: keep primary at
> `#B13832` and shift destructive to a distinctly darker red, or reserve filled-red for
> primary and outline-red for destructive. Decide before component work starts.

### Neutrals

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#1B1F31` | Primary text |
| `--ink-muted` | `#5C6376` | Body, labels, secondary text, sidebar idle, table headers |
| `--surface` | `#FFFFFF` | Cards, sidebar, modals, header |
| `--bg` | `#F2F2F2` | Page background, dividers |
| `--border` | `#E2E3E7` | Input and card borders *(approx.)* |
| `--border-subtle` | `#EBECEF` | Hairline rules *(approx.)* |

### Tinted fills

Every status colour has a pale companion used as a background.

| Token | Hex | Paired text | Where |
|---|---|---|---|
| `--red-tint` | `#F2DFDF` | `#B13832` | Sidebar active pill |
| `--red-tint-soft` | `#F6EAE9` | `#B13832` | `IMMEDIATE` badge |
| `--red-tint-bg` | `#EEE8E8` | — | Incoming column background |
| `--red-tint-banner` | `#EDE6E6` | `#B13832` | Alert banner |
| `--red-tint-btn` | `#F1E3E5` | `#CA3A31` | Reject button |
| `--green-tint` | `#D8E5DE` | `#3B7E44` | Approve button |
| `--green-tint-pill` | `#CADACE` | `#3B7E44` | `active` pill |
| `--amber-tint` | `#F6DED0` | `#A75823` | `Accepted` badge |
| `--amber-tint-pill` | `#E2D2C5` | `#A75823` | `pending` pill |
| `--neutral-tint` | `#E7E9EE` | `#5C6376` | `FUTURE` badge |
| `--proto-banner` | `#EAE2DC` | `#A75823` | "PROTOTYPE — NOT PRODUCTION" bar — **remove in production** |

### Accessibility check

`#5C6376` on `#FFFFFF` ≈ **6.2:1** — passes AA for body text.
`#FFFFFF` on `#B13832` ≈ **6.6:1** — passes AA.
`#FFFFFF` on `#3B7E44` ≈ **5.3:1** — passes AA for normal text.
`#3B7E44` on `#CADACE` ≈ **3.6:1** — **fails AA for body text**; acceptable only at
pill sizes ≥ 14px semibold (AA large). Verify each tint pair against its real type size
during component build; the tint/text pairs are the weakest link in this palette.

Status is never communicated by colour alone anywhere in the prototype — every pill and
badge carries a word. Hold that line.

### Dark mode

Not present in the prototype. If required, note that the valet board's red/green
semantics carry operational meaning and must retain their contrast relationships.
Recommendation *(proposed)*: defer dark mode; the tablet lives under garage lighting
where a bright board is an asset.

---

## Typography

The prototype's typefaces cannot be identified with certainty from raster images.
Observed characteristics and a recommended stack:

| Role | Observed | Recommended *(proposed)* |
|---|---|---|
| Headings / wordmark | Geometric sans, tight tracking, heavy weight at large sizes | **Poppins** or **Outfit**, 600–700 |
| UI / body | Neutral grotesque, high x-height | **Inter**, 400–600 |
| Codes & identifiers | Monospace, letter-spaced — `481027`, `@wacker-valet` | **JetBrains Mono** or `ui-monospace` |

### Scale *(measured from the screenshots, rounded to a 4px-friendly ramp)*

| Token | Size / weight | Use |
|---|---|---|
| `display` | 32px / 700 | Landing wordmark |
| `h1` | 24px / 700 | Page titles — "Manager Dashboard", "Office Console" |
| `h2` | 20px / 700 | Section headings — "My vehicles", "Your request" |
| `h3` | 17px / 600 | Card titles, customer names |
| `body` | 15px / 400 | Default |
| `body-sm` | 13px / 400 | Secondary lines, metadata |
| `label` | 12px / 600, `letter-spacing: .06em`, **uppercase** | Section labels — `ACTIVE REQUESTS`, `BY LOCATION`, `PARKING LOCATION · STAFF ONLY` |
| `caption` | 12px / 400 | Helper text under toggles |
| `numeral` | 30px / 700 | KPI values |

The **uppercase tracked micro-label** is the most distinctive typographic device in the
system. It marks every section boundary on every screen. Build it as one component and
use it everywhere.

---

## Space, radius, elevation

| Token | Value | Notes |
|---|---|---|
| Base unit | **4px** | All spacing is a multiple |
| Card padding | 20–24px | |
| Card gap | 16px | |
| Section gap | 24–32px | |
| `radius-sm` | 6px | Badges, pills, inputs |
| `radius-md` | 10px | Buttons, cards |
| `radius-lg` | 14px | Modals, outer containers |
| `radius-full` | 999px | Toggles, avatars, status pills |
| Elevation | Effectively flat | Cards are separated by **fill + 1px border**, not shadow. Modals get one soft shadow + a dimmed backdrop |

Flatness is a deliberate characteristic of this system. Do not introduce shadows on
cards; the border-and-fill separation is what makes the dense valet board readable.

---

## Components

### Button

| Variant | Fill | Text | Border | Used for |
|---|---|---|---|---|
| Primary | `--brand-red` | white | none | Sign In, Accept, Submit for approval, Add location |
| Success | `--success` | white | none | **Ready** |
| Tinted-success | `--green-tint` | `--success` | none | Approve |
| Tinted-danger | `--red-tint-btn` | `--brand-red-bright` | none | Reject |
| Secondary | white | `--ink` | `--border` | Create Account, Cancel, Add a vehicle, Add staff |
| Ghost/link | none | `--brand-red` | none | Create account, Add valet, Copy, Regenerate |
| Outline-danger | `--red-tint-soft` | `--brand-red` | `--brand-red` | **Cancel Request**, **Move to active** |
| Disabled | `--brand-red` @ ~45% | white | none | Schedule pickup, before a date is chosen |

Heights: 44px default; 52px full-width primary; **56px on the valet board** *(proposed —
tablet touch targets)*.

### Status pill / badge

`radius-full`, 12px/600, ~4px×10px padding, tinted fill + matching text. Two families:

- **Account/record status** — `active`, `pending` (lowercase)
- **Request badges** — `IMMEDIATE`, `FUTURE` (uppercase, type) and `Pending`,
  `Accepted` (title case, status)

The casing distinction is consistent across every screen; preserve it.

### Card

White, `radius-lg`, 1px `--border`, 20–24px padding. Optional uppercase micro-label
header, optional right-aligned caption or action link.

**Queue card variant:** adds a 4px left rail — red for active work, green for
completed. This is the board's primary scanning cue.

### Table

Uppercase tracked slate headers with a `↕` sort affordance, 1px row dividers in
`--bg`, generous row height (~56px), no zebra striping, no outer border.

### Toggle

`radius-full`, ~46×26px, `--brand-red` when on with a white knob, `--border` when off.
Right-aligned in a row with a bold label and a caption underneath.

### Progress stepper (customer)

Horizontal, three nodes joined by a 2px rule. Completed/current: filled `--brand-red`
dot and red connector. Future: `--ink-muted` dot, grey connector. Labels below, 13px,
centred.

### Photo tile

Fixed square (~72px board / ~88px detail), `--bg` fill, `radius-md`, centred 🚗 icon
over the words `No photo` in 11px muted. Appears on **every** vehicle reference across
all four roles — build it once.

### Modal

Centred, max ~640px, white, `radius-lg`, title left / ✕ right, dimmed backdrop,
footer action row right-aligned with the primary action rightmost.

### Empty state

Single muted sentence in place of content — *"No scheduled pickups yet."*,
*"No notes yet. …"*. No illustrations anywhere in the prototype. Keep it plain.

---

## Iconography

Line icons, ~1.5px stroke, rounded caps — consistent with **Lucide** *(proposed)*.

Observed: `car`, `calendar-clock`, `bell`, `eye`, `map-pin`, `clock`, `user`,
`user-plus`, `users`, `phone`, `file-text`, `shield`, `key`, `power`, `copy`,
`refresh-cw`, `rotate-ccw`, `check`, `check-circle`, `x`, `x-circle`, `plus`,
`arrow-up-circle`, `pencil`, `search`, `settings`, `history`, `activity`,
`layout-grid`, `building`, `clipboard-check`, `volume-2`, `image-plus`, `chevron-right`.

Icons are always paired with a text label except in three places: the header bell, the
card-level ↺ revert, and the ⋮ kebab. Those three need `aria-label`s.

---

## Motion *(proposed — none observable in static captures)*

| Interaction | Treatment |
|---|---|
| Card moves between columns | 200ms ease-out translate + fade |
| New incoming card | Brief red pulse on the left rail, synced to the first chime |
| Status change | 150ms cross-fade on the badge |
| Modal | 150ms fade + 8px rise |
| Toggle | 120ms knob slide |

Respect `prefers-reduced-motion`: disable the pulse and the card-move animation, keep
the state change instantaneous.
