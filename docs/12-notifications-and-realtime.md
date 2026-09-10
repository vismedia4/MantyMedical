# 12 — Notifications & Real-Time

Two audiences with opposite needs: the customer wants a quiet status that stays
correct, the valet needs an alert that cannot be ignored.

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
| Scope | Per location — *"silences incoming-request alerts on every valet screen at this location"* |
| Visual pair | Banner: *"{n} request awaiting acceptance — Accept to stop the alert."* |

### Why the design is right

A car-retrieval request has a hard real-world deadline: someone is standing in a lobby
waiting. A notification that can be dismissed will be dismissed. Making the chime
un-silenceable by the person it inconveniences, and configurable only by their manager,
is a correct control decision on a shared kiosk. Build it exactly as specified.

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

### Audio asset

Not recoverable from screenshots. Recommendation *(proposed)*: a short two-tone chime,
~700ms, 800–1200Hz — audible over garage noise, distinct from a phone ringtone,
non-alarming to nearby customers. Ship one asset at three gain levels rather than
scaling in code, so "Low" is still audible.

---

## 2. Live board updates

The valet board and the manager dashboard must reflect reality without a refresh.
The customer status screen says so explicitly: *"Updates automatically as the valet
works your request."*

### Transport *(proposed)*

**WebSocket, with polling fallback.**

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

## 3. Customer notifications

The customer header carries a **🔔 bell**, but no notification list is shown. It is
required scope.

### Events the customer should receive *(proposed)*

| Event | Channel | Copy |
|---|---|---|
| Request accepted | In-app + push | "A valet is retrieving your Silver Toyota Camry." |
| **Ready for pickup** | In-app + push | "Your Silver Toyota Camry is ready at Wacker Drive Garage." |
| Registration approved | In-app + email | "You're all set at Wacker Drive Garage." |
| Registration rejected | In-app + email | With a reason, if captured |
| Vehicle change approved / rejected | In-app | |
| Scheduled pickup reminder | Push | ~30 min before `scheduled_for` |
| Request cancelled by staff | In-app + push | With a reason |

**Ready for pickup is the one that matters.** It is the moment the product delivers its
value. It should be a push notification, and it should be reliable enough that a
customer trusts it enough to stop watching the progress bar.

### Channels

| Channel | Status | Notes |
|---|---|---|
| In-app | Required | The bell's list |
| Web push | Recommended | The QR flow implies an installable PWA; web push works on modern iOS/Android |
| SMS | Consider | Phone numbers are already collected. Highest reliability, real per-message cost |
| Email | Required for account lifecycle | Approvals, password resets |

Note the tension with the enrollment copy — *"nothing is emailed"* applies to **staff
credential provisioning**, not to customer notifications. Do not over-apply it.

---

## 4. Manager and admin notifications *(proposed)*

Nothing observed. Recommended minimum:

| Event | Recipient | Channel |
|---|---|---|
| New approval submitted | Managers of that location | In-app badge + daily email digest |
| Request pending > 5 min | Managers of that location | In-app + push — the escalation above |
| Valet board offline > 5 min in hours | Managers + admin | Email |
| Access code regenerated / location disabled | Admins | Activity feed |

The dashboard's approvals callout is a pull mechanism; a manager who does not open the
app does not see it. At least one push channel is needed for time-sensitive items.
