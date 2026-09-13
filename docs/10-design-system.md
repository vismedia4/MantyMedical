# 10 — Design System

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

> **Superseded by the Pioneer Parking Identity, Edition 1.1.** The palette and typefaces
> below are now taken from that document, not sampled from the prototype. The earlier
> prototype values (`#B13832` red, `#1B1F31` navy, Poppins / IBM Plex) are **retired** —
> do not use them anywhere.
>
> Machine-readable tokens: [`design-tokens.css`](design-tokens.css).

## The rule that governs everything else

> *"Each color has one job. Red is rare, which is why it is noticed."*

Three usage rules from Edition 1.1 are non-negotiable and are the ones most likely to be
broken by accident:

1. **Text is never in Pioneer Red.** Red is 3.7:1 on white — the mark and display type at
   24px and up, nothing else.
2. **Signal Blue is the only actionable colour on screens.** Every button and link a person
   acts on. One blue button per view.
3. **The valet screens hold 7:1**, not 4.5:1. A higher bar than the rest of the product,
   for a tablet read at arm's length in a garage.

---

## Colour — Edition 1.1

### Primary

| Token | Name | Hex | RGB | Job |
|---|---|---|---|---|
| `--red` | **Pioneer Red** | `#FD2F38` | 253 47 56 | The mark and brand accents. **Never body text** — 3.7:1 on white |
| `--navy` | **Pioneer Navy** | `#0B2C5D` | 11 44 93 | The logo's words, headings, sign panels, uniforms. 13.7:1 with white |
| `--blue` | **Signal Blue** | `#0048A8` | 0 72 168 | **Screens only.** Every button and link people act on. 8.4:1 with white |

CMYK starting points: Red `0 81 78 1` · Navy `88 53 0 64` · Blue `100 57 0 34`.
Pantone references are matched on press and recorded in the guidelines once proofed.

### Neutrals

| Token | Name | Hex | Job |
|---|---|---|---|
| `--ink` | Asphalt | `#1A1F33` | Text |
| `--muted` | Concrete | `#5A6478` | Secondary text |
| `--line` | Line | `#E2E4E8` | Dividers |
| `--ground` | Paper | `#F2F4F8` | Ground |

### Lane colours — one per product

| Product | Colour | Hex | Audience |
|---|---|---|---|
| **Passport** | Signal Blue | `#0048A8` | Residents — *built, in pilot* |
| **Crew** | Curb Amber | `#F2A900` | Valets and attendants — *proposed name* |
| **Console** | Pioneer Navy | `#0B2C5D` | Managers and the office — *proposed name* |
| **Record** | Ledger Teal | `#0E7C7B` | Verified Custody Record™ — *full pilot* |

**Lane colours appear on the app icon, the launch screen and marketing only.** Inside the
apps, everything uses the shared interface colours. Do not tint a screen by role.

### Signals — screens and signs only

| Token | Hex | Meaning |
|---|---|---|
| `--ready` | `#15803D` | Done |
| `--alert` | `#D91E36` | Waiting |
| `--caution` | `#8A4B00` | Caution — **text** |
| `--error` | `#C0271E` | Error — **text** |

Note the split: `#D91E36` is the alert *fill*; `#8A4B00` and `#C0271E` are the text-safe
equivalents. Using the fill colour as text is the easy mistake.

### Proportion

```
White and Paper  ████████████████████████████  58
Pioneer Navy     █████████████                 26
Signal Blue      ████                           8
Pioneer Red      ███                            6
```

Lane colours and signals share the last sliver. If a screen looks more red than this, it
is wrong.

### Contrast pairs — verified in the guidelines

| Pair | Ratio | Use |
|---|---|---|
| White on navy | **13.7:1** | Anything, any size. Signs and reversed panels |
| Navy on white | **13.7:1** | Headings and the logo's words |
| White on blue | **8.4:1** | Buttons — including the valet screen's 7:1 standard |
| Navy on amber | **6.8:1** | Crew materials. **Never white on amber** (2.0:1) |
| White on teal | **5.0:1** | Record materials; large text on screens |
| Red on white | **3.7:1** | Logo and display type 24px and up **only** |

---

## Typography — Edition 1.1

> *"Road-sign lettering for the name and the numbers, a clear sans for reading, a serif for
> letters."*

| Role | Face | Weights | Notes |
|---|---|---|---|
| **Display and wayfinding** | **Overpass** | 700 · 800 · 900 | Drawn from Highway Gothic, the lettering on American road and garage signs. Headings, the logo, signage, level markers. Capitals +0.04em, labels +0.16em |
| **Figures and codes** | **Overpass Mono** | 400 · 600 | Ticket numbers, plates, stalls, times — even width so they line up |
| **Reading and interface** | **Source Sans 3** | 400 · 600 · 700 · italic | Body, the apps, forms, captions. Legible at 13px on a phone in a dim garage |
| **Correspondence** | **Source Serif 4** | 400 · 600 · italic | Letters, proposals, long reports — where Pioneer speaks to owners and boards |

All four are **SIL Open Font License** — free for print, web and apps, and bundled with the
apps so they render offline.

**Fallbacks** where the brand fonts cannot be installed: Arial for Overpass and Source
Sans, Georgia for Source Serif.

### Scale — screens

| Role | Size / weight | Example |
|---|---|---|
| Display | 56 / 900 | *Every car* |
| Heading | 32 / 800 | *Your vehicles* |
| Title | 20 / 700 | *Request history* |
| Body | 17 / 400 | *Ready at the front desk.* |
| Label | 12 / 800, +.16em | `BY LOCATION` |

### Rules

- Overpass capitals carry names and wayfinding. **Never set paragraphs in capitals.**
- **Buttons are 19px bold or larger**, which counts as large text for accessibility.

---

## Graphic language

Three devices, taken from the mark and the garage. **Use one at a time.**

| Device | Spec |
|---|---|
| **The 3-in-5 hatch** | Bay-line stripes at the flag's **31°**, stripe-to-gap ratio **3 : 5**. Card backs, sign bands, report covers, clearance bars |
| **Level markers** | A navy square, Overpass Black numerals, the red flag. Garage levels first; also chapters, report sections, app onboarding steps |
| **Icons** | **Lucide** outline, 24px grid, **1.75 stroke**, round joins, navy or the current text colour. **Always paired with a word** |

The icon spec confirms what this document previously only proposed — Lucide, always
labelled. No change needed to the screen specs.

---

## Product naming

> *"Always two words: **Pioneer Passport**, never 'Passport by Pioneer' or 'the Pioneer app'."*

- Product lockups: small `PIONEER` tracked above the product name, both navy, beside the red
  mark. The name sits on the line of the mark's bowl.
- App icons: the white mark on the lane colour; navy on Crew's amber.
- **One app store developer account in Pioneer's name publishes the whole family.**
- Today valets and managers use **Passport** through their own roles. Crew and Console are
  ready for when those become separate apps — see [05 — Information Architecture](05-information-architecture.md).
- **Crew, Console and Record are proposals** pending trademark clearance in Illinois and
  federally before first use.

---

## Digital

| Item | Spec |
|---|---|
| Grid | 12 columns, 24px gutters, 1200px maximum |
| Header | The corporate lockup, 34–40px tall, 1× clear space |
| Buttons | **One blue button per view.** Links are navy, underlined |
| Focus | 3px blue ring |
| Accessibility | **WCAG 2.2 AA** across the site; **the valet screens hold 7:1** |
| Email signature | Text, not an image. The mark is the only graphic |
| Favicon / avatar | White mark on red — the one place red fills a whole shape on screen |

---

## Retired — the prototype palette

The values previously sampled from the Pioneer Connect prototype (`#B13832`, `#CA3A31`,
`#E94643`, `#1B1F31`, `#3B7E44`, `#A75823`) are **superseded by Edition 1.1** and must not
be used. The reference screenshots under [`screens/`](screens/) still show them; read those
for layout and behaviour, never for colour.

Two open items the prototype palette raised are resolved by Edition 1.1:

- **Three reds** → one. `#FD2F38` is the mark; there is no second or third red.
- **Danger and primary sharing a colour** → they no longer do. Primary action is Signal
  Blue, alert is `#D91E36`, and destructive text takes `#C0271E`.

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

### Vehicle image tile

Fixed square (~72px board / ~88px detail), `--bg` fill, `radius-md`. Appears on **every**
vehicle reference across all four roles — build it once.

**There is no photo upload.** The client replaced customer uploads with **generic images
derived from make + model + colour** (doc 03), for data load and privacy. The tile
renders:

| State | Rendering |
|---|---|
| Resolved | The mapped generic vehicle asset, tinted or selected by colour |
| Unresolved make/model | Neutral silhouette in the vehicle's colour — never an error, never a broken image |
| No colour | Neutral grey silhouette |

The prototype's `No photo` placeholder is retired. Design the assets as flat
side-profile silhouettes in the system palette so a colour swap is a fill change, not
150 × 12 rendered files.

**Asset set is a real deliverable** — VisMedAI action item 04. Recommend body-style ×
colour (~150 assets) over make × model (unbounded). Start it in parallel with build.

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
