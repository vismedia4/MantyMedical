# Product mockups — Pioneer Parking

**🔒 INTERNAL — VisualMedia, Ltd.** · Safe to show the client. Not the other provider's work.

These are **our own** screens, drawn from scratch in Pioneer Identity 1.1. They are not
screenshots of the prototype in `docs/screens/`, which belongs to another provider and is
reference only.

| File | Product | Frame |
|---|---|---|
| `pioneer-01-passport-status.png` | **Pioneer Passport** — resident, retrieval in progress | Phone, 402 × 900 |
| `pioneer-02-crew-queue.png` | **Pioneer Crew** — attendant queue | Phone, 402 × 900 |
| `pioneer-03-console-floor.png` | **Pioneer Console** — manager live floor | Desktop, 1440 × 900 |

PNGs are transparent-background at 2× and drop straight into Canva, Keynote or the client page.

## What each screen is meant to prove

- **Passport** — the wait becomes visible. Four states, one estimate, one action in Signal Blue.
- **Crew** — the privacy restriction is designed in, not bolted on: attendants see plate, stall,
  key and return point, never a customer name or phone number. Type and contrast hold the 7:1
  valet standard.
- **Console** — the operating picture a manager actually needs, and the surface that makes the
  platform licensable to other operators (tenant is named in the sidebar).

## Identity rules these screens obey

- Red appears only in the mark. Never as body text, never as a button.
- Signal Blue is reserved for things you can act on.
- Overpass for display and labels, Overpass Mono for plates, stalls, keys and ticket codes,
  Source Sans 3 for reading.
- Lucide icons, 24px grid, 1.75 stroke, each paired with a word.

## Rebuilding

```bash
docs/mockups/src/render.sh
```

Needs Chromium. Fonts are inlined in `src/fonts.css`, so rendering works offline and the
output is byte-stable. Edit the HTML, re-run, and the PNGs are regenerated and auto-cropped.
