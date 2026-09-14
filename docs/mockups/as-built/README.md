# As-built screens — `pioneer-platform`

**🔒 INTERNAL — VisualMedia, Ltd.** · **These are ours.** Captured from the running
application in `PioneerParking/pioneer-platform`. Unlike `docs/screens/`, which is another
provider's prototype and reference only, these can be shown to the client.

Kept on disk deliberately: screenshots pasted into a chat do not survive the session, and
mockups built from memory drift from the product. Anything drawn for a deck must be checked
against these first.

| File | Screen |
|---|---|
| `01-passport-landing-phone.webp` | Passport landing — sign in, create account, **QR "Get the app"** |
| `02-passport-home-phone.webp` | Passport home — vehicle status, three-state stepper, "About 6–9 minutes" |
| `03-valet-vehicles-desktop.png` | Valet station — Vehicles list |
| `04-valet-vehicles-detail.webp` | Valet station — Vehicles list, closer |

## Facts the deck must not get wrong

**Identity**
- The mark is a **red "P"** with a flag notch, not a slash device.
- The lockup is `PIONEER` in small tracked navy caps **above** `Passport` set large.
- Navy headings, Signal Blue actions, red confined to the mark. Identity 1.1 holds.

**Naming — one product, two faces**
- Both the customer app and the valet station are branded **Pioneer Passport**.
- **Crew**, **Console** and **Record** are our proposed names. They are *not* in the build.
  Do not show them as though they ship.

**Domain vocabulary — use the app's words**
- Vehicles are identified by **decal number** (`PP-1248`) and **customer first name**, not by
  licence plate. Search is "First name, decal, make…".
- **Parking location** is free text (`EV bay 1 — please plug in`), not a stall grid.
- **Internal note** is a distinct field.
- Location reads **Wacker Drive Garage** / **Wacker Valet Station 1**.

> ⚠ **Everything in these captures is synthetic.** Names, vehicles, decal numbers and
> locations are seeded development records. Wacker is not a garage Pioneer has chosen for
> the pilot, and Sofia Alvarez, Grace Kim, Linda Nguyen and Michael Torres are not
> residents. Any client-facing use of these screens must carry a sample-data label — the
> deck does, on slides 7 and 11.

**Privacy — as actually built**
- The valet **does** see the customer's name. The valet does **not** see a phone number.
  Claiming "no names" is wrong and contradicts `docs/02-roles-and-permissions.md`.
- The customer's own decal is masked to `••• 042` on the customer side.

**States**
- Customer stepper is **three** states, horizontal: Pending → Retrieving vehicle → Ready for
  pickup.
- Customer tabs: Home · Vehicles · My details.
- Valet tabs: Queue · Vehicles · Recent.

**Vehicle imagery**
- Each vehicle shows a flat side-view silhouette tinted to the vehicle's colour. This is the
  make/model/colour → image mapping set — VisualMedia action item 04, already partly live.

**QR**
- A QR block already exists on the landing screen. The pilot decision is not "build a QR
  code"; it is whether residents **self-register** through it with a location access code and
  an approval step. See `docs/19-pilot-and-mvp-scope.md`.
