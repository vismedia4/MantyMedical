# 11 — API Contract *(proposed)*

The prototype is a client-side demo with no observable network layer. Everything here
is an engineering proposal derived from the screens and the domain model. It is meant
to be argued with, then frozen.

**Conventions**

- REST over JSON. `/api/v1`.
- Bearer token auth. Every request is scoped server-side by the principal's role and
  locations — **never trust a `location_id` supplied by the client** except as a filter
  within the authorized set.
- Timestamps: ISO-8601 UTC. Every response that renders a date also returns the
  location's IANA timezone so the client formats locally.
- Errors: RFC 9457 problem-details.
- Mutations that can be retried (accept, ready, create request) accept an
  `Idempotency-Key` header. This matters on a tablet with flaky garage Wi-Fi.

---

## Serializers: the staff/customer split

The single most important rule in this contract.

```
VehicleCustomer          VehicleStaff
  id                       id
  make model color         make model color
  identifier               identifier
  photo_url                photo_url
  status                   status
                        +  notes[]              ← STAFF ONLY
                        +  customer { name, phone }

RequestCustomer          RequestStaff
  id status type           id status type
  requested_at             requested_at accepted_at ready_at
  scheduled_for            scheduled_for
  vehicle (customer)       vehicle (staff)
  progress[]               customer { name, phone }
                        +  parking_location      ← STAFF ONLY
                        +  notes[]               ← STAFF ONLY
```

`parking_location` and `notes` must be **structurally absent** from customer
serializers, not merely null. Enforce with a serializer test per role.

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
POST   /me/vehicles                       { make, model, color }
                                          → 202 + ApprovalRequest
PATCH  /me/vehicles/:id                   { make?, model?, color? }
                                          → 202 + ApprovalRequest  (live record unchanged)
POST   /me/vehicles/:id/photo             multipart → { photo_url }

GET    /me/requests?status=active         → RequestCustomer[]
POST   /me/requests                       { vehicle_id, type: "immediate" }
POST   /me/requests                       { vehicle_id, type: "scheduled",
                                            scheduled_for }
GET    /me/requests/:id                   → RequestCustomer
DELETE /me/requests/:id                   → cancel

GET    /me/notifications
POST   /me/notifications/:id/read
```

`202` on vehicle create/update is the contract expression of "this needs approval" —
the response body carries the pending `ApprovalRequest` so the client can render the
amber banner immediately.

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

GET    /valet/directory/customers?q=
GET    /valet/directory/vehicles?q=
GET    /valet/directory/recent-pickups
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
current state so the losing tablet can show *"Already accepted by another valet"*
rather than appearing broken.

---

## Manager

```
GET    /manager/dashboard                 → { approvals_count, active[], upcoming[] }
PATCH  /manager/requests/:id              { status }   ← the override; writes an audit event

GET    /manager/approvals                 → grouped by kind
GET    /manager/approvals/:id             → full submission  ("Review")
POST   /manager/approvals/:id/approve     { identifier? }
POST   /manager/approvals/:id/reject      { reason? }

GET    /manager/customers?q=&sort=&dir=
POST   /manager/customers                 { name, email, phone, identifier,
                                            vehicle? }   ← "Add customer", pre-approved
GET    /manager/customers/:id
PATCH  /manager/vehicles/:id              { make?, model?, color?, identifier? }
POST   /manager/vehicles/:id/photo

GET    /manager/history?from=&to=&q=&sort=
GET    /manager/valet-accounts
POST   /manager/valet-accounts            { station_name, username, password }
POST   /manager/valet-accounts/:id/suspend
POST   /manager/valet-accounts/:id/reactivate
POST   /manager/valet-accounts/:id/reset-password → { temporary_password }

GET    /manager/settings/chime
PUT    /manager/settings/chime            { enabled, repeat_interval_seconds, volume }
```

`approve` optionally carries `identifier` because the manager assigns the decal /
apartment / stall at approval time — the customer never enters it (doc 06 · C7).

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
GET    /admin/settings/policies
PUT    /admin/settings/policies
```

`GET /admin/console` shape:

```json
{ "totals": { "locations": 5, "active_requests": 6,
              "pending_approvals": 6, "customers": 10 },
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
→ { "event": "chime.updated",    "chime": {...} }
```

Customer-scope sockets receive the **customer** serializer of the same events. One
event bus, two serializers, enforced at the boundary.
