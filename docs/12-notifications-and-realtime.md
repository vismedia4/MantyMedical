# 12 — Notifications & Real-Time

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

> Requirements authority is [00 — Client Requirements](00-client-requirements.md).
> **Changed:** in-app push only — **no SMS** (§4.5); *Ready* is the required default and
> *Retrieving Vehicle* is opt-in (§6.4); chime sound design is a client-reviewed
> deliverable (§6.6).

Two audiences with opposite needs: the customer wants a quiet status that stays correct,
the valet needs an alert that cannot be ignored.

**The stakes here are the project's stakes.** Pioneer is leaving ElimaWait because it is
unreliable. The chime and the *Ready* push are the two mechanisms that decide whether
this app is more reliable than the thing it replaces. The brief names valet-tablet
reliability as a standing risk for exactly this reason.

---

## 1. The valet chime — the product's most opinionated feature

### Observed specification

| Property | Value |
|---|---|
| Trigger | A request enters `pending` at this location |
| Behavior | *"The chime repeats until a valet accepts the request."* |
| Stop condition | A valet taps **Accept** — nothing else |
| Repeat interval | Configurable, default **6 seconds** |
| Volume | `Low` / `Medium` / `High`, default **Medium** — *"Noticeable on the valet stand without being disruptive."* |
| Who can change it | Garage Manager, Office Admin. **Not the valet** |
| Sound character | *"Persistent but not annoying"* — client-stated, and *"the sound design matters to him"* |
| Scope | Per location — *"silences incoming-request alerts on every valet screen at this location"* |
| Visual pair | Banner: *"{n} request awaiting acceptance — Accept to stop the alert."* |

### Why the design is right

A car-retrieval request has a hard real-world deadline: someone is standing in a lobby
waiting. A notification that can be dismissed will be dismissed. Making the chime
un-silenceable by the person it inconveniences, and configurable only by their manager,
is a correct control decision on a shared kiosk. The client describes it in the same
terms — *"a deliberate operational forcing function."* Build it exactly as specified.

### Implementation

```
on request.created (websocket) ──► render card in INCOMING
                              ──► show banner
                              ──► start chime loop

chime loop:
    while (count of pending requests at this location) > 0
       and chime.enabled:
        play tone at chime.volume
        wait chime.repeat_interval_seconds
```

Requirements:

- **Drive the loop off live state, not off the event.** Two pending requests must not
  produce two overlapping loops. One loop, gated on `pending_count > 0`.
- **Browser autoplay policy will block audio until a user gesture.** A kiosk that
  reboots overnight comes back silent. Mitigate: on load, if audio is blocked, show a
  persistent *"Tap to enable alerts"* bar and re-arm on the first touch. Then verify
  audibility — see the heartbeat below.
- **Settings changes propagate live** via the `chime.updated` event. A manager turning
  the chime off must silence the tablet without a reload.
- **Test tone** on the settings screen *(proposed)* — a manager setting volume needs to
  hear what they are choosing, and it doubles as an audio-permission check.
- **Escalation** *(proposed)*: if a request stays pending past a threshold (say 5
  minutes), notify the garage manager. Today an unattended tablet chimes into an empty
  garage forever and nobody upstream knows.

### Audio asset — a client-reviewed deliverable, not a developer's pick

> *"The chime must be persistent but not annoying … the sound design matters to him."*

Treat this as a design item with a review cycle, because the tension is real: a sound
that repeats every 6 seconds until someone acts will be heard hundreds of times a shift
by the same person, and by customers standing nearby.

Recommendation *(proposed)*: a short two-tone chime, ~700ms, 800–1200Hz — audible over
garage noise, distinct from a phone ringtone, non-alarming to nearby customers. Ship one
asset at three gain levels rather than scaling in code, so "Low" is still audible.

**Design the repetition, not just the tone.** A sound that is identical on the first and
the fiftieth repeat is the one that gets described as annoying. Escalate gently: soft
first tone, slightly fuller on subsequent repeats, plateau after ~5 — urgent without
being punishing.

Put three candidates in front of Jonathan before build. This is cheap to review and
expensive to re-litigate after deployment.

---

## 2. Live board updates

The valet board and the manager dashboard must reflect reality without a refresh.
The customer status screen says so explicitly: *"Updates automatically as the valet
works your request."*

### Transport *(proposed)*

**WebSocket, with polling fallback.** The tablet is the reliability-critical client;
everything below is written for it.

| Option | Verdict |
|---|---|
| WebSocket | **Recommended.** Bidirectional, low latency, one connection per tablet. Needs reconnect logic |
| SSE | Viable and simpler, but reconnect semantics on flaky garage Wi-Fi are no better |
| Polling only | Fallback only. At 5s intervals across five locations it is affordable, but it makes the chime laggy |

Ship polling first if it accelerates v1 — the request volume is tiny. But design the
client around an event stream so the swap is a transport change, not a rewrite.

### Reconnection — the requirement that actually matters

A garage tablet loses Wi-Fi. This is not an edge case; it is Tuesday.

- Exponential backoff with jitter, capped at ~30s.
- On reconnect, **refetch the whole board** rather than replaying missed events.
- Show a persistent, unmissable **"Reconnecting — this board may be out of date"**
  banner while disconnected. A silently stale valet board is worse than no board.
- Track a **last-updated** timestamp in the board chrome so a valet can tell at a glance
  whether what they are looking at is live.
- **Heartbeat the tablet** *(proposed)*: the client pings the server every 60s; if a
  location's board goes silent for >5 minutes during operating hours, alert the manager.
  Combined with audio-permission state, this answers *"is the valet stand actually
  working right now?"* — which nothing in the current design does.

### Per-role update needs

| Role | What must update live | Acceptable latency |
|---|---|---|
| Valet | Every card, every column, the chime | **< 2s** |
| Customer | Own request status | < 5s |
| Manager | Dashboard active list, approvals count | < 10s |
| Admin | Console KPIs, activity feed | Refresh on navigate is fine |

---

## 3. Customer notifications — push only, no SMS

> *"In-app push notifications only. **No SMS.** Jonathan stated this preference
> directly."*

The customer header carries a **🔔 bell**, but no notification list is shown. Both the
list and a **notification-preferences screen** are required scope (doc 06 · C8).

### The two-tier model — client-specified

| Notification | Default | Client statement |
|---|---|---|
| **Vehicle ready for pickup** | **On — required** | *"Notify on 'Ready' as the default. The customer's required notification is when the vehicle is ready."* |
| **Retrieving your vehicle** | **Off — opt-in** | *"Customers may opt in to 'Retrieving Vehicle' status updates via a notification-preference toggle."* |

**Recommendation *(proposed)*: make Ready non-disableable in MVP.** Render it on and
locked with an explanatory caption. It is the single notification the product exists to
deliver, push is now the only channel, and a customer who turns it off has silently
returned themselves to standing in a lobby watching a door.

### Why push-only raises the engineering bar

Removing SMS removes the fallback. A missed push is now a missed handoff, and the
failure is invisible to everyone: the valet marked the car ready and moved on; the
customer is still upstairs. Compensating controls, all *(proposed)*:

- **Permission priming with context.** Ask for push permission *after* the customer's
  first successful request, not on cold start. A denied prompt at launch is very hard to
  recover, and it silently disables the product's core promise.
- **Detect and repair the denied state.** If push permission is off, show a persistent
  in-app banner explaining what they will miss, with a deep link to system settings.
- **Never rely on push alone for state.** The in-app request screen must always be
  correct on open, so a customer who missed the push and opens the app sees *Ready*
  immediately. Push is an accelerator, not the source of truth.
- **Delivery telemetry.** Track send → delivered → opened for *Ready*. If delivery rates
  sag on a platform, you need to know before the client's customers tell them.
- **The valet board is the backstop.** For assisted customers with no smartphone at all
  (doc 04 §7), *Ready* is a physical hand-off and the board must say so.

### Full event list *(proposed unless marked)*

| Event | Channel | Copy |
|---|---|---|
| **Ready for pickup** *(client: required)* | Push + in-app | "Your Silver Toyota Camry is ready at Wacker Drive Garage." |
| Request accepted *(client: opt-in)* | Push + in-app | "A valet is retrieving your Silver Toyota Camry." |
| Registration approved | Push + in-app + email | "You're all set at Wacker Drive Garage." |
| Registration rejected | In-app + email | With a reason, if captured |
| Vehicle change approved / rejected | In-app | |
| Scheduled pickup reminder | Push | ~30 min before `scheduled_for` |
| Request cancelled by staff | Push + in-app | With a reason |

**Ready for pickup is the one that matters.** It is the moment the product delivers its
value, and with SMS ruled out it has exactly one delivery path. Instrument it, monitor
it, and treat a drop in delivery rate as a production incident.

### Channels

| Channel | Status | Notes |
|---|---|---|
| **Native push** | **Required — the only customer channel** | Client requirement; app-store deployment makes native push available on both platforms |
| In-app list | Required | The bell |
| Email | Required for account lifecycle only | Approvals, password resets |
| **SMS** | **Excluded** | *"In-app push notifications only. No SMS."* — client-stated |

Note the distinction: *"nothing is emailed"* in the enrollment copy applies to **staff
credential provisioning**, not to customer account email. Do not over-apply it.

---

## 4. Manager and admin notifications *(proposed)*

Nothing observed. Recommended minimum:

| Event | Recipient | Channel |
|---|---|---|
| New approval submitted | Managers of that location | In-app badge + daily email digest |
| **Approval past SLA / manager away** | **Office Admin** | **Push + email — client requirement**, doc 04 §6 |
| Request pending > 5 min | Managers of that location | In-app + push — the escalation above |
| Valet board offline > 5 min in hours | Managers + admin | Email |
| Access code regenerated / location disabled | Admins | Activity feed |

The dashboard's approvals callout is a pull mechanism; a manager who does not open the
app does not see it. At least one push channel is needed for time-sensitive items — and
the escalation notification is not optional. It is the mechanism behind the client's one
flagged requirement: *"pending approvals must not stall on manager absence."*
