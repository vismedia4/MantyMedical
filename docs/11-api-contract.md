# 11 — API Contract *(proposed)*

> ## 🔒 INTERNAL — VisualMedia, Ltd.
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

The prototype is a client-side demo with no observable network layer. Everything here
is an engineering proposal derived from the screens and the domain model. It is meant
to be argued with, then frozen.

> Requirements authority is [00 — Client Requirements](00-client-requirements.md).
> **Changed:** photo-upload endpoints deleted (§4.1); the staff serializer splits into a
> valet tier without phone numbers (§4.2); notification preferences added (§6.4);
> escalated-approval endpoints added (§6.1); every path is tenant-scoped (§6.3).

**Conventions**

- REST over JSON. `/api/v1`.
- Bearer token auth. Every request is scoped server-side by the principal's **tenant**,
  role and locations — **never trust a `tenant_id` or `location_id` supplied by the
  client** except as a filter within the authorized set. Tenant scoping is enforced at
  the data-access layer; a licensed product cannot rely on controllers remembering.
- Timestamps: ISO-8601 UTC. Every response that renders a date also returns the
  location's IANA timezone so the client formats locally.
- Errors: RFC 9457 problem-details.
- Mutations that can be retried (accept, ready, create request) accept an
  `Idempotency-Key` header. This matters on a tablet with flaky garage Wi-Fi.

---

## Serializers: the staff/customer split

The single most important rule in this contract.

**Three tiers, not two.** The client's privacy restriction on valet phone access splits
the staff serializer.

```
  ── CUSTOMER ──────────    ── VALET ──────────────    ── MANAGER / ADMIN ────────
  VehicleCustomer            VehicleValet               VehicleManager
    id                         id                         id
    make model color           make model color           make model color
    identifier                 identifier                 identifier
    image_key                  image_key                  image_key
    status                     status                     status
                            +  notes[]                 +  notes[]
                            +  customer { name }       +  customer { name, phone, email }
                                       ▲
                            NO PHONE ──┘

  RequestCustomer            RequestValet               RequestManager
    id status type             id status type             id status type
    requested_at               requested_at               requested_at accepted_at
    scheduled_for              scheduled_for ready_at     ready_at completed_at
    vehicle (customer)         vehicle (valet)            vehicle (manager)
    progress[]              +  parking_location        +  parking_location
    can_cancel              +  notes[]                 +  notes[]
                            +  customer { name }       +  customer { name, phone }
```

Three rules, each enforced by a serializer test:

1. `parking_location` and `notes` are **structurally absent** from customer serializers,
   not null.
2. `phone` is **structurally absent** from every valet-tier serializer. Client
   requirement: *"CANNOT … view customer phone numbers."* Doc 02.
3. `image_key` is derived server-side from make/model/colour. It is never writable and
   there is no upload path.

`RequestCustomer.can_cancel` is server-computed (`status == "pending"`) so the client
never has to re-derive the cancellation rule.

---

## Auth

```
POST   /auth/sign-in                { identifier, password }
                                    → { token, user, location(s), role }
POST   /auth/sign-out
POST   /auth/forgot-password        { email }
POST   /auth/reset-password         { token, password }
GET    /auth/me                     → current principal, role, locations, policies
```

```
POST   /enrollment/resolve-code     { access_code }
                                    → { location_id, location_name,
                                        identifier_type, identifier_label }
POST   /enrollment/register         { access_code, name, email, phone, password,
                                      identifier, vehicle: { make, model, color } }
                                    → { user, status: "pending"|"active" }
```

`resolve-code` is what makes the enrollment form dynamic: the client asks the server
what to call the identifier field before rendering it. Rate-limit it — it is a
6-digit-code oracle. See doc 13.

---

## Customer

```
GET    /me/vehicles                       → VehicleCustomer[]
POST   /me/vehicles                       { make, model, color, identifier }
                                          → 202 + ApprovalRequest
PATCH  /me/vehicles/:id                   { make?, model?, color? }
                                          → 202 + ApprovalRequest  (live record unchanged)

GET    /me/requests?status=active         → RequestCustomer[]
POST   /me/requests                       { vehicle_id, type: "immediate" }   ← "Request Now"
POST   /me/requests                       { vehicle_id, type: "scheduled",
                                            scheduled_for }
GET    /me/requests/:id                   → RequestCustomer
DELETE /me/requests/:id                   → cancel  — 409 unless status == "pending"

GET    /me/notifications
POST   /me/notifications/:id/read
GET    /me/notification-preferences       → { notify_ready, notify_retrieving }
PUT    /me/notification-preferences       { notify_ready?, notify_retrieving? }
POST   /me/push-token                     { token, platform }
```

`202` on vehicle create/update is the contract expression of "this needs approval" —
the response body carries the pending `ApprovalRequest` so the client can render the
amber banner immediately.

**No photo endpoint exists.** Vehicle images are derived from make/model/colour; there is
no upload path anywhere in this API. Client requirement, doc 00 §4.1.

**`DELETE /me/requests/:id` returns `409` once a valet has accepted.** Client-decided:
cancellation is permitted *before acceptance only*. The client already knows this from
`can_cancel`, but the server is the authority and the race is real.

`RequestCustomer.progress` is a server-rendered three-node array so the customer
vocabulary lives in exactly one place:

```json
{ "status": "accepted",
  "progress": [
    { "key": "pending",    "label": "Pending",           "state": "done" },
    { "key": "retrieving", "label": "Retrieving Vehicle", "state": "current" },
    { "key": "ready",      "label": "Ready for Pickup",   "state": "upcoming" }
  ] }
```

---

## Valet

```
GET    /valet/board                       → the whole board in one call
POST   /valet/requests/:id/accept         → RequestStaff        (CAS on pending)
POST   /valet/requests/:id/ready          → RequestStaff
POST   /valet/requests/:id/complete       → RequestStaff
POST   /valet/requests/:id/revert         → RequestStaff        (→ pending)
POST   /valet/requests/:id/activate       → RequestStaff        ("Move to active")
PUT    /valet/requests/:id/parking-location   { parking_location }
POST   /valet/requests/:id/notes          { body } → Note
POST   /valet/requests/:id/notify-manager { reason } → escalation to the manager
                                          (replaces direct phone access — doc 07 · V2)

GET    /valet/directory/customers?first_name=   ← client-named search behavior
GET    /valet/directory/vehicles?q=
GET    /valet/directory/recent-pickups          ← 2-3 day window
```

`GET /valet/board` returns the four buckets pre-computed server-side, because bucketing
depends on location-local time and must not be re-derived on a tablet with a wrong clock:

```json
{ "location": { "id": "...", "name": "Wacker Drive Garage", "timezone": "America/Chicago" },
  "chime":    { "enabled": true, "repeat_interval_seconds": 6, "volume": "medium" },
  "awaiting_acceptance": 1,
  "incoming":  [ RequestStaff ],
  "active":    [ RequestStaff ],
  "tomorrow":  [ RequestStaff ],
  "future":    [ RequestStaff ],
  "recently_completed": [ RequestStaff ] }
```

Shipping `chime` and `awaiting_acceptance` in the board payload means the tablet needs
no second call to decide whether to sound the alert.

**`accept` is a compare-and-swap.** If `status != "pending"`, return `409` with the
current state so the losing tablet can show *"Already accepted by another valet"* — or
*"The customer cancelled this request"* — rather than appearing broken. The same CAS
resolves the accept-vs-cancel race.

**No valet response may contain a phone number.** Enforce it in the serializer, and add a
contract test that fails the build if `phone` appears in any `/valet/*` response body.
This is the kind of requirement that gets re-broken six months later by someone adding a
convenience field.

---

## Manager

```
GET    /manager/dashboard                 → { approvals_count, active[], upcoming[] }
PATCH  /manager/requests/:id              { status }   ← the override; writes an audit event

GET    /manager/approvals                 → grouped by kind
GET    /manager/approvals/:id             → full submission  ("Review")
POST   /manager/approvals/:id/approve     { identifier? }
POST   /manager/approvals/:id/reject      { reason? }

GET    /manager/customers?first_name=&q=&sort=&dir=   ← first-name is the primary path
POST   /manager/customers                 { name, email, phone, identifier,
                                            vehicle? }   ← "Add customer", pre-approved
GET    /manager/customers/:id
PATCH  /manager/vehicles/:id              { make?, model?, color?, identifier? }

GET    /manager/history?from=&to=&q=&sort=
GET    /manager/valet-accounts
POST   /manager/valet-accounts            { station_name, username, password }
POST   /manager/valet-accounts/:id/suspend
POST   /manager/valet-accounts/:id/reactivate
POST   /manager/valet-accounts/:id/reset-password → { temporary_password }

GET    /manager/settings/chime
PUT    /manager/settings/chime            { enabled, repeat_interval_seconds, volume }

GET    /manager/availability              → { available, away_until, backup_admin }
PUT    /manager/availability              { available, away_until? }
                                          ← away routes approvals to the office at once
```

`approve` optionally carries `identifier` because the manager **verifies and may
correct** the decal / apartment / unit number the customer supplied at registration. The
customer provides it; the manager confirms it against the property's records.

`reset-password` returns a one-time plaintext value because *nothing is emailed*. Return
it exactly once, never store it in the clear, and log the event.

---

## Office Admin

```
GET    /admin/console                     → KPIs + per-location rollups

GET    /admin/users?type=staff|customer&q=&role=&location_id=
POST   /admin/users                       { name, username, role, location_ids, password }
PATCH  /admin/users/:id
POST   /admin/users/:id/suspend
POST   /admin/users/:id/reactivate
POST   /admin/users/:id/reset-password    → { temporary_password }

GET    /admin/locations
POST   /admin/locations                   { name, address, state, identifier_type,
                                            manager_id?, manager_account?, valet_account? }
                                          → Location (access_code generated)
PATCH  /admin/locations/:id
POST   /admin/locations/:id/regenerate-code   → { access_code }   (old code invalidated)
POST   /admin/locations/:id/deactivate-code
POST   /admin/locations/:id/disable
POST   /admin/locations/:id/enable

GET    /admin/activity?location_id=&role=&verb=&from=&to=&q=&cursor=
       ← permanent archive; page over years, not days

GET    /admin/approvals/escalated         → SLA-breached + manager-away approvals
POST   /admin/approvals/:id/approve       { identifier? }   ← full manager authority
POST   /admin/approvals/:id/reject        { reason? }
POST   /admin/approvals/:id/nudge         → ping the assigned manager

GET    /admin/settings/policies
PUT    /admin/settings/policies           { ..., approval_sla_registration_hours,
                                            approval_sla_vehicle_change_hours,
                                            valet_history_visible_days }
```

`GET /admin/console` shape:

```json
{ "totals": { "locations": 5, "active_requests": 6,
              "pending_approvals": 6, "customers": 10,
              "escalated_approvals": 0 },
  "by_location": [
    { "id": "...", "name": "Wacker Drive Garage",
      "address": "225 N. Wacker Dr, Chicago, IL",
      "active": 3, "approvals": 3, "customers": 4 }
  ] }
```

---

## Real-time channel

See [12 — Notifications & Real-Time](12-notifications-and-realtime.md) for transport
choice and reconnection. Envelope:

```
WS /ws?scope=location:{id}     valet + manager
WS /ws?scope=user:{id}         customer

→ { "event": "request.created",  "request": RequestStaff }
→ { "event": "request.accepted", "request": RequestStaff }
→ { "event": "request.ready",    "request": RequestStaff }
→ { "event": "request.completed","request": RequestStaff }
→ { "event": "request.cancelled","request_id": "..." }
→ { "event": "approval.created", "approval": ApprovalRequest }
→ { "event": "approval.escalated","approval": ApprovalRequest }
→ { "event": "chime.updated",    "chime": {...} }
```

Customer-scope sockets receive the **customer** serializer; valet-scope sockets receive
the **valet** serializer; manager and admin scopes receive the **manager** serializer.
One event bus, three serializers, enforced at the boundary — the same three-tier split
as the REST surface, for the same reason.
