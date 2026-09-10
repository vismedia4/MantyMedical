# 16 — Website Refresh (Workstream 2)

> Source: [00 — Client Requirements](00-client-requirements.md) §2 and the brief's §4.
> Secondary to the app, but **fast**, and on the same Tuesday decision point.

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
| **Corporate video** | ~2.5 minutes. **The site centrepiece** | File received was blurry and too large for web delivery. Jonathan to resend the high-quality source via Google Drive; VisMedAI to downsample and optimise |
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

The site cannot be finished until the high-quality source arrives. Flag that dependency
explicitly in Tuesday's timeline rather than absorbing it.

## Technical

| Item | Position |
|---|---|
| Current stack | **WordPress on GoDaddy** — outdated, requires a full refresh |
| Administration model | To be reviewed — who edits the site after launch, and how often |
| Relationship to the app | **Separate brand and separate property.** *"Keep the website separate from the reservation app."* |

### Recommendation *(proposed)*

**A static-generated marketing site** — Astro, Next.js static export, or similar — on a
CDN host, with a lightweight headless CMS for the handful of things that actually change
(testimonials, team, proof points).

Rationale, in the client's terms:

- **Performance is credibility.** An HOA board opening the site on a phone in a meeting
  is the exact evaluation moment. A static site with an optimised video beats WordPress
  on GoDaddy by an order of magnitude on that page load.
- **Security and maintenance drop to near zero.** No plugin surface, no PHP updates, no
  compromised-WordPress incident on the property the client is using to look credible.
- **It scales the way VisMedAI argued for.** Adding a property is a content entry.

Counter-argument worth stating fairly: if Pioneer's team expects to edit the site
themselves frequently, WordPress-with-a-modern-theme has lower training cost. **Resolve
by answering "who edits this, how often?"** — that is the administration-model question
already flagged for review. If the honest answer is "quarterly, by VisMedAI," go static.

### Keep it separate from the app

The app is designed for licensing to other operators and must not hard-bind to Pioneer
branding (doc 00 §6.3). The website is the opposite: it is **entirely** Pioneer's brand.
Keeping them separate properties — separate repos, separate hosting, separate deploy
cadence — is what lets both be true at once.

The only integration point is the QR / download link pointing at the app's store
listings.

## Structure *(proposed — for Tuesday)*

```
  Home            Hero + corporate video · positioning · proof points
                  · testimonials · CTA "Discuss your property"
  Services        Valet · monthly parking · property partnerships
  Why Pioneer     Private ownership · operational expertise · technology
  Our Team        Headshots, credibility, the team as an asset
  Properties      Portfolio scale, presented WITHOUT specific locations
  Contact         Enquiry form aimed at HOA boards and property managers
```

Single primary CTA throughout: **start a conversation about a property.** Not "find
parking." The site has one job, and it is lead generation from a small, high-value
audience.

## Deliverables for Tuesday, September 15

Per the brief, VisMedAI presents:

1. **Proposed direction** — positioning, visual approach
2. **Site structure** — the map above, agreed
3. **Turnaround time**
4. **Cost**

Plus, recommended additions to that agenda:

5. **Stack recommendation** with the edit-frequency question answered
6. **The video dependency** stated as a date-driven blocker
7. **Administration model** — who owns the site after launch

## Open items

| # | Item | Recommendation |
|---|---|---|
| W1 | Who administers the site post-launch, and how often does it change? | Answer this first — it decides the stack |
| W2 | Are Google reviews pulled live or curated? | Curated with attribution. Live pulls surface bad days on your credibility page |
| W3 | Domain strategy — one domain for site and app, or separate? | Separate. The app is licensable; the site is Pioneer's |
| W4 | Is there a contact/lead-routing workflow, or just email? | At minimum, a routed enquiry form with acknowledgement |
| W5 | Does the site need to serve existing monthly parkers at all? | A single "sign in to the app" link. Nothing more — it is not their destination |
| W6 | Accessibility standard for the site? | WCAG 2.2 AA, same as the app. Some HOA and municipal clients will ask |
