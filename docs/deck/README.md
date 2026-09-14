# Tuesday deck — Pioneer Parking, Inc Projects

**VisualMedia, Ltd. presenting to Pioneer Parking, Inc** · 15 September 2026, 12:00 noon.

- **`Pioneer-Parking-Projects-VisualMedia-15Sep2026.pdf`** — 20 slides, 1920 × 1080. Present from this.
- `slides/s01.png … s20.png` — the same slides as images. Drop them into Canva, Keynote or
  Google Slides if the deck needs to live there.
- `contact-sheet.png` — all twenty on one page, for a quick read-through.

## Why it is built rather than authored in Canva

Canva's API cannot set a font family, so a deck assembled through it cannot be held in
Overpass, and the identity section would have argued for a typeface the deck itself did not
use. These slides are HTML rendered headlessly, so every colour, weight and contrast pair
comes from Identity 1.1 directly.

## Structure

| | Slides | |
|---|---|---|
| Title & agenda | 1 – 2 | |
| **1 · Corporate identity** | 3 – 7 | Framed as **our initiative**, offered for adoption, with completion quoted separately. Never as a delivered asset. |
| **2 · The platform** | 8 – 17 | What is live, pilot scope in and out, timelines, the self-registration decision, price, and what we need from Pioneer |
| **3 · The website** | 18 – 19 | Built; blocked on the identity decision. Deliberately unpriced |
| Close | 20 | The four decisions, and contact |

**Slide 14 is the one to slow down on.** Self-registration is Pioneer's decision, presented
as two priced options rather than a recommendation dressed as a fact:

- Option A — $26,000 – $28,000, seven weeks, residents seeded by us. **Our recommendation.**
- Option B — $33,000 – $35,000, nine weeks, residents register themselves.

## Product imagery

Slides 7 and 10 use `docs/mockups/as-built/` — real captures of the running application. No
stock art, no invented mockups, and nothing from the other provider's prototype. The dev-only
note under the QR block is cropped out of the sign-in capture.

## Rebuilding

```bash
docs/deck/render.sh          # pages/*.html → slides/*.png
```

`build.py` and `build2.py` generate the slide HTML; `split.py` writes one file per slide.
Fonts are inlined, so rendering is offline and byte-stable. Edit a slide's HTML and re-run.
