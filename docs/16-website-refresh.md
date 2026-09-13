# 16 — Website (Workstream 2)

> Source: [00 — Client Requirements](00-client-requirements.md) §2 and the brief's §4.
>
> **Status correction:** the site is a **separate project that has already been built**
> — it lives in `PioneerParking/pioneer-website`. The work remaining is **applying the
> Pioneer Parking Identity, Edition 1.1** to it, not designing or rebuilding it.
>
> Everything below about positioning still stands — it is strategy, and it was right. The
> stack and structure sections have been rewritten to match what actually exists.

## Positioning — the site is not a brochure

> *"Not a brochure. A credibility and scalability instrument to win HOA boards and
> private property owners as Pioneer expands."*

That framing settles most of the design questions before they are asked. The audience is
not a driver looking for a garage. It is **an HOA board, a private property owner, or a
property manager deciding who to hand a building to.** They are evaluating whether
Pioneer is a serious operator, not comparing hourly rates.

| Emphasise | De-emphasise |
|---|---|
| Corporate presentation, private ownership, operational expertise | **Specific garage locations** |
| Multi-location success, presented without naming exact locations | Consumer-facing parking search |
| The team — headshots, credibility, and the genuine diversity of the team | Pricing |
| Capacity to take on new properties | Anything that reads as small or local |

The location de-emphasis is a deliberate strategic choice, stated directly:

> *"Jonathan wants to demonstrate capability and success without publishing exact garage
> locations — projecting a larger, more professional footprint."*

Design the proof points as *"multiple properties across Illinois, Florida and New York"*
rather than a map with five pins. A map with five pins makes Pioneer look like five
garages; the same facts stated as a portfolio make Pioneer look like an operator.

**VisMedAI's counter-emphasis, on the record:**

> *"Build the site so it scales as Pioneer adds properties, rather than as a snapshot of
> today."*

Concretely: no hard-coded counts in copy ("we operate 5 properties"), no per-location
pages that create a maintenance burden and undercut the de-emphasis strategy, and a
content model where adding a property is a data entry, not a rebuild.

## Content inventory

| Element | Detail | Status |
|---|---|---|
| **Corporate video** | ~2.5 minutes. **The site centrepiece** | **Low-resolution cut received** — enough to build layout and timing against. The full-resolution master is still needed before launch; encoding and optimisation are ours |
| **Testimonials** | Google reviews, surfaced on-site | Pull live or curate; decide |
| **Team** | Manager headshots and team imagery — *"the diversity of Pioneer's team was noted as a genuine asset"* | Photography to be supplied |
| **Proof points** | Multiple-location success stories, **without naming exact locations** | Needs a writing pass |
| **Photography** | Jonathan to supply | Pending |

### The video is the critical path

A 2.5-minute video as the centrepiece is a real engineering constraint, not a content
slot. Requirements *(proposed)*:

- Multiple encodes (1080p / 720p / 540p) with adaptive delivery, plus a poster frame
- Target under ~8 MB for the initial segment; never ship a single large MP4
- A CDN in front of it, not the origin host
- **The page must be useful with the video unplayed** — headline, positioning and CTA
  above or beside it, never gated behind it
- Captions. HOA board members watch on mute in a meeting

**The low-res cut unblocks the build; only launch waits on the master.** Design and
encode against what we have, and treat the full-resolution file as a launch-gate item
rather than a start-gate one. Say that plainly in Tuesday's timeline instead of presenting
the whole site as blocked.

## The actual work: applying Identity 1.1

The site exists. Edition 1.1 exists. The job is to make the first look like the second.

### What Edition 1.1 specifies for the web, verbatim

| Item | Spec |
|---|---|
| Grid | 12 columns, 24px gutters, 1200px maximum |
| Header | The corporate lockup, 34–40px tall, with 1× clear space |
| Sections | Open with a level marker or the brand line — *"never a stock photo alone"* |
| Buttons | **One blue button per view.** Links are navy, underlined |
| Focus | 3px blue ring |
| Accessibility | **WCAG 2.2 AA** across the site |
| Typography | Overpass display, Source Sans 3 body, Overpass Mono for figures |
| Colour | Navy structure, Signal Blue for anything actionable, **text never in Pioneer Red** |
| Favicon / avatar | White mark on red — the one place red fills a whole shape on screen |
| Email signature | Text, not an image. The mark is the only graphic. No quotes, no banners |
| Footer | *"© Pioneer Parking, Inc. · Family owned & operated · Chicago"* + Privacy, Accessibility |

Edition 1.1 also supplies the hero copy direction the site should carry:

> **Residential and commercial valet · Chicago**
> *Every request answered. Every car accounted for.*
> Pioneer runs the garage the way a good hotel runs its front door, and shows owners and
> boards the record to prove it.
>
> Calls to action: **Request a proposal** · *See the Pioneer Promise*

### Scope of the branding pass *(proposed)*

| Work | Note |
|---|---|
| **Token swap** | Replace the site's colours and typefaces with the Edition 1.1 token set. One style sheet — the guidelines state the site, email and social share the app's tokens |
| **Logo and lockups** | Corporate lockup in the header at 34–40px with correct clear space; favicon and social avatar as the white mark on red |
| **Button and link discipline** | Audit for one blue button per view; links navy and underlined; 3px blue focus rings |
| **Red audit** | Find and remove every instance of text set in Pioneer Red. This is the rule most likely to be broken already |
| **Section openers** | Level markers or the brand line where sections currently open on a photo alone |
| **Accessibility pass** | WCAG 2.2 AA, keyboard reachability, image descriptions |
| **Video integration** | Adaptive encodes, poster frame, captions; page useful with the video unplayed |
| **Email signature template** | Text-only, per the spec above |

**This is a well-bounded piece of work** — a token swap plus a rule audit against a
published specification, not a redesign. Price and schedule it separately from the app,
and separately from whatever built the site in the first place.

### Still to confirm

| # | Question |
|---|---|
| S1 | What is the site built in? That decides whether the token swap is an afternoon or a week |
| S2 | Does it already use a token layer, or are colours hard-coded through the components? |
| S3 | Who administers it after launch, and how often does content change? |
| S4 | Is the domain `pioneerparkinginc.com`, as Edition 1.1 shows? |

## Structure — as specified in Identity 1.1

Edition 1.1 shows the navigation as:

```
  Residents   ·   Properties   ·   Services   ·   About   ·   Resident sign in
```

Note what that ordering does: **Residents first, and a sign-in link** — the site serves
the existing customer as well as the prospect. That is a change from the assumption that
it is purely a lead-generation surface, and it resolves question W5 below.

Single primary CTA throughout: **Request a proposal.** Not "find parking." The secondary
is *See the Pioneer Promise* — the six service commitments, which the guidelines are
explicit carries **no lockup of its own**: it appears in words, in red, on reports, signs
and proposals.

## Deliverables for Tuesday, September 15

The brief asked for direction, structure, turnaround and cost. Direction and structure are
now settled by Identity 1.1, so the session only needs:

1. **Scope of the branding pass** — the table above, agreed
2. **Turnaround** — dependent on S1 and S2
3. **Cost** — quoted separately from the app
4. **The video**: low-res cut is in and the build can proceed; the master is a launch gate,
   not a start gate

## Open items

| # | Item | Recommendation |
|---|---|---|
| W1 | Who administers the site post-launch, and how often does it change? | Answer this first — it decides the stack |
| W2 | Are Google reviews pulled live or curated? | Curated with attribution. Live pulls surface bad days on your credibility page |
| W3 | Domain strategy — one domain for site and app, or separate? | Separate. The app is licensable; the site is Pioneer's |
| W4 | Is there a contact/lead-routing workflow, or just email? | At minimum, a routed enquiry form with acknowledgement |
| W5 | ~~Does the site need to serve existing monthly parkers?~~ | **Resolved.** Identity 1.1 puts *Residents* first in the navigation with a *Resident sign in* link |
| W6 | ~~Accessibility standard?~~ | **Resolved.** WCAG 2.2 AA, stated in Identity 1.1 |
| W7 | Does the built site already carry the Pioneer Promise copy, or is that new content? | The six commitments live on Level 1 of the guidelines |
