# Tuesday deck — Pioneer Parking, Inc Projects

**VisualMedia, Ltd. presenting to Pioneer Parking, Inc** · 15 September 2026, 12:00 noon.

- **`Pioneer-Parking-Projects-VisualMedia-15Sep2026.pdf`** — 21 slides, 1920 × 1080. Present from this.
- `slides/s01.png … s21.png` — the same slides as images. Drop them into Canva, Keynote or
  Google Slides if the deck needs to live there.
- `contact-sheet.png` — all twenty-one on one page, for a quick read-through.

## Why it is built rather than authored in Canva

Canva's API cannot set a font family, so a deck assembled through it cannot be held in
Overpass, and the identity section would have argued for a typeface the deck itself did not
use. These slides are HTML rendered headlessly, so every colour, weight and contrast pair
comes from Identity 1.1 directly.

## Structure

| | Slides | |
|---|---|---|
| Title & agenda | 1 – 2 | |
| **1 · Corporate identity** | 3 – 8 | **The foundation**, not an optional extra. A standard had to exist to ship four products that read as one company; we wrote it on our own initiative. What Pioneer decides is how far it reaches — slide 8 sets out the reach across products, website, signage, vehicles, print and correspondence. |
| **2 · The platform** | 9 – 18 | What is live, pilot scope in and out, timelines, the self-registration decision, price, and what we need from Pioneer |
| **3 · The website** | 19 – 20 | Built; waiting on the foundation. Deliberately unpriced |
| Close | 21 | The four decisions, and contact |

**Slide 15 is the one to slow down on.** Self-registration is Pioneer's decision, presented
as two priced options rather than a recommendation dressed as a fact:

- Option A — $26,000 – $28,000, seven weeks, residents seeded by us. **Our recommendation.**
- Option B — $33,000 – $35,000, nine weeks, residents register themselves.

## Product imagery

Slides 7 and 11 use `docs/mockups/as-built/` — real captures of the running application. No
stock art, no invented mockups, and nothing from the other provider's prototype. The dev-only
note under the QR block is cropped out of the sign-in capture.

## Rebuilding

```bash
docs/deck/render.sh          # pages/*.html → slides/*.png
```

`build.py` and `build2.py` generate the slide HTML; `split.py` writes one file per slide.
Fonts are inlined, so rendering is offline and byte-stable. Edit a slide's HTML and re-run.

## Standing rule — never name another provider

Nothing in the client-facing material refers to the prior spec vendor, the prototype they
built, or the fact that Pioneer already owns a specification. It is not our place to comment
on another firm's work in Pioneer's own presentation, and pointing at a spec we did not write
volunteers that part of the value did not come from us.

Where the pricing argument needs a reason the gap is closeable, it cites **our own**
foundation: the identity standard, the data model and a working retrieval loop.

The same rule applies to the client page in `scratchpad/pioneer-build-review.html`.
