# -*- coding: utf-8 -*-
exec(open('build.py').read().split('# \xe2\x94\x80\xe2\x94\x80 01 title'.encode().decode('utf-8'))[0]) if False else None
import os
TOTAL = 20
def page(body, cls="", num=None):
    f = ('<div class="foot"><div class="who"><b>VisualMedia, Ltd.</b>'
         '<span>&middot; Pioneer Parking, Inc &middot; 15 September 2026</span></div>'
         f'<div class="pg">{num:02d} / {TOTAL}</div></div>') if num else ""
    return f'<div class="slide {cls}"><div class="rail"><i></i></div>{body}{f}</div>'
def tick(c="#0048A8"):
    return (f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
def cross():
    return ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#98A0B0" stroke-width="2.6" '
            'stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>')
s=[]

# 11 pilot in scope
s.append(page('''
<div class="pad">
  <div class="kicker">Pilot MVP &middot; seven weeks &middot; one garage</div>
  <h1 class="sm">What the pilot&nbsp;includes</h1>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:56px;margin-top:48px;flex:1;min-height:0">
    <div>
      <h2 style="font-size:26px;color:var(--concrete);letter-spacing:.16em;text-transform:uppercase;font-size:16px">Resident</h2>
      <ul class="tick" style="margin-top:20px">
        <li>''' + tick() + '''<div>Sign in, vehicles, request retrieval</div></li>
        <li>''' + tick() + '''<div>Live status with an honest estimate</div></li>
        <li>''' + tick() + '''<div>Push notification when the car is ready</div></li>
        <li>''' + tick() + '''<div>Native app, iOS and Android, internal distribution</div></li>
      </ul>
      <h2 style="margin-top:44px;color:var(--concrete);letter-spacing:.16em;text-transform:uppercase;font-size:16px">Attendant</h2>
      <ul class="tick" style="margin-top:20px">
        <li>''' + tick() + '''<div>Queue, vehicles and recent history</div></li>
        <li>''' + tick() + '''<div>Accept &middot; Ready &middot; Complete &middot; Revert</div></li>
        <li>''' + tick() + '''<div>The chime &mdash; repeats until accepted, cannot be disabled</div></li>
      </ul>
    </div>
    <div>
      <h2 style="color:var(--concrete);letter-spacing:.16em;text-transform:uppercase;font-size:16px">Platform</h2>
      <ul class="tick" style="margin-top:20px">
        <li>''' + tick() + '''<div>Multi-tenant data model and location scoping</div></li>
        <li>''' + tick() + '''<div>Real-time updates, with an honest stale-state banner on reconnect</div></li>
        <li>''' + tick() + '''<div>Append-only activity log</div></li>
        <li>''' + tick() + '''<div>Manager status override, with an audit event</div></li>
      </ul>
      <div class="card acc" style="margin-top:46px">
        <h3 style="font-size:25px">One garage, seeded by hand</h3>
        <p style="font-size:20px">One location, one valet station account, residents and vehicles entered by us.
        That is what keeps it to seven weeks &mdash; and it is the subject of the decision two slides from now.</p>
      </div>
    </div>
  </div>
</div>''', num=11))

# 12 out of scope
s.append(page('''
<div class="pad">
  <div class="kicker q">Pilot MVP</div>
  <h1 class="sm">What the pilot leaves&nbsp;out &mdash; on purpose</h1>
  <table>
    <tr><th style="width:38%">Excluded</th><th style="width:44%">Why</th><th>Lands in</th></tr>
    <tr><td class="k">Manager &amp; admin consoles</td><td>One location, administered by hand</td><td class="m">Phase 2</td></tr>
    <tr><td class="k">Approvals &amp; manager-absence backup</td><td>Only needed once residents register themselves</td><td class="m">Phase 2</td></tr>
    <tr><td class="k">Scheduled and future pickups</td><td>Immediate retrieval is the promise; scheduling is an enhancement</td><td class="m">Phase 3</td></tr>
    <tr><td class="k">Notification preferences</td><td>Ready-only, on by default, is the pilot configuration</td><td class="m">Phase 3</td></tr>
    <tr><td class="k">The other four locations</td><td>One garage is the test</td><td class="m">Phase 4</td></tr>
    <tr><td class="k">Public app-store release</td><td>Internal distribution removes two review cycles from the critical path</td><td class="m">Phase 5</td></tr>
    <tr><td class="k">Accessibility audit, pen test, privacy review</td><td>External and formal &mdash; premature before the loop is proven</td><td class="m">Phase 5</td></tr>
  </table>
  <div class="note" style="margin-top:auto;padding-top:36px"><b style="color:var(--navy)">Every excluded item is
  deferred, not cancelled.</b> The exclusions are what buy you an answer in seven weeks instead of eighteen.</div>
</div>''', num=12))

# 13 pilot timeline
def row(wk,t,d):
    return f'<div class="tlrow"><div class="wk">{wk}</div><div><div class="ti">{t}</div><div class="ds">{d}</div></div></div>'
s.append(page(f'''
<div class="pad">
  <div class="kicker">Pilot MVP</div>
  <h1 class="sm">Seven weeks to an answer</h1>
  <div class="tl">
    {row("Week 1","Foundations and sign-off","Environments, tenancy, identity tokens, the seeded garage. Self-registration decision closes here.")}
    {row("Weeks 2 &ndash; 3","The retrieval loop","Request, queue, state machine, the chime, the activity log. The core of the product.")}
    {row("Week 4","Real time and push","Live status, reconnection, stale-state banner, native push on both platforms.")}
    {row("Week 5","Hardening","Edge cases, offline behaviour, the valet 7:1 contrast standard, device testing.")}
    {row("Week 6","Garage rehearsal","On-site with real attendants and real vehicles. The week that finds what a desk cannot.")}
    {row("Week 7","Pilot live","Residents onboarded, monitoring in place, daily readout to Pioneer.")}
  </div>
  <div class="note" style="margin-top:auto;padding-top:34px">Start within a week of sign-off and the pilot is running
  before the first week of November.</div>
</div>''', num=13))

# 14 THE DECISION
s.append(page('''
<div class="pad">
  <div class="kicker" style="color:#D91E36">Decision required &mdash; before week one</div>
  <h1 class="sm">Should residents register themselves<br>during the pilot?</h1>
  <div class="lede" style="font-size:25px;margin-top:18px;max-width:1560px">A QR block already sits on the Passport
  sign-in screen. The question is not whether to build a QR code &mdash; it is whether the pilot carries
  <b>self-registration</b>: a location access code, an account the resident creates, and an approval step behind it.</div>
  <div class="price" style="margin-top:46px">
    <div class="pbox">
      <div class="t">Option A &middot; base pilot</div>
      <div class="v">$26,000 &ndash; $28,000</div>
      <div class="w">Seven weeks &middot; residents seeded by us</div>
      <div class="d">Proves the retrieval loop. Seeding fifty residents in one garage takes an afternoon.
      Registration is not the thing anyone doubts.</div>
    </div>
    <div class="pbox sel">
      <div class="t">Option B &middot; with self-registration</div>
      <div class="v">$33,000 &ndash; $35,000</div>
      <div class="w">Nine weeks &middot; residents register themselves</div>
      <div class="d">Proves the loop <b>and</b> that residents can self-serve. If you intend to show the pilot to
      other operators, this is the difference between a product and a demo.</div>
    </div>
  </div>
  <div class="note" style="margin-top:auto;padding-top:34px"><b style="color:var(--navy)">Our recommendation is
  Option A</b> &mdash; unless the pilot has an audience beyond Pioneer. Either way we need the answer before week one:
  approvals reach into the data model, and retrofitting costs more than the difference.</div>
</div>''', cls="paper", num=14))

# 15 full MVP
s.append(page(f'''
<div class="pad">
  <div class="kicker">Full MVP &middot; eighteen weeks</div>
  <h1 class="sm">From one garage to the whole&nbsp;operation</h1>
  <div style="display:grid;grid-template-columns:1.15fr 1fr;gap:56px;margin-top:44px;flex:1;min-height:0">
    <div class="tl" style="margin-top:0">
      {row("Weeks 1 &ndash; 7","Everything in the pilot","Carried forward, not rebuilt.")}
      {row("Weeks 8 &ndash; 11","Identity and approvals","Self-registration with per-location codes, the three approval kinds, manager-absence backup with an escalation SLA.")}
      {row("Weeks 12 &ndash; 14","Manager console","Overrides, staff, vehicles, the custody record, reports in your existing formats.")}
      {row("Weeks 15 &ndash; 16","All five locations","Location administration, cross-location reporting, staff moves.")}
      {row("Weeks 17 &ndash; 18","Release","Public app-store submission, accessibility audit, penetration test, privacy review.")}
    </div>
    <div>
      <div class="card acc"><h3>Scheduled pickups</h3><p>Future and recurring retrieval &mdash; the commuter case.</p></div>
      <div class="card" style="margin-top:26px"><h3>Verified Custody Record</h3><p>Condition captured at check-in and hand-back. Signed, time-stamped, and the answer to a disputed scratch.</p></div>
      <div class="card" style="margin-top:26px"><h3>Reports in your formats</h3><p>Not ours. We need your current report layouts to build against.</p></div>
    </div>
  </div>
</div>''', num=15))

# 16 price
s.append(page('''
<div class="pad">
  <div class="kicker q">Commercials</div>
  <h1 class="sm">What this would have cost, and what it&nbsp;costs</h1>
  <div class="price" style="margin-top:52px;grid-template-columns:1fr 1fr">
    <div class="pbox" style="background:var(--paper)">
      <div class="t">Conventional build</div>
      <div class="v" style="color:var(--concrete)">$150,000 &ndash; $200,000</div>
      <div class="w">Eighteen months ago, with a conventional team</div>
      <div class="d">The same scope, estimated line by line, at ordinary agency day rates. This is the benchmark,
      not a scare number &mdash; it is the figure you arrived at independently.</div>
    </div>
    <div class="pbox sel">
      <div class="t">VisualMedia &middot; pilot</div>
      <div class="v">$26,000 &ndash; $28,000</div>
      <div class="w">Seven weeks &middot; $33,000 &ndash; $35,000 with self-registration</div>
      <div class="d">Two things close the gap: <b>you already own a specification</b>, which removes the most
      expensive phase of any build, and we work AI-augmented, which compresses the rest.</div>
    </div>
  </div>
  <div class="cols c3" style="margin-top:44px">
    <div class="card"><div class="n">NOT INCLUDED</div><h3>Hosting and maintenance</h3><p>A monthly retainer, quoted separately once the pilot scope is fixed.</p></div>
    <div class="card"><div class="n">NOT INCLUDED</div><h3>Identity completion</h3><p>The full asset and guidelines package, if Pioneer adopts the standard.</p></div>
    <div class="card"><div class="n">NOT INCLUDED</div><h3>The website</h3><p>Separate and smaller. Section three.</p></div>
  </div>
</div>''', num=16))

# 17 what we need
s.append(page('''
<div class="pad">
  <div class="kicker q">From Pioneer</div>
  <h1 class="sm">What we need from&nbsp;you</h1>
  <div class="cols c2" style="margin-top:60px;gap:36px">
    <div class="card"><div class="n">01</div><h3>Your existing report formats</h3>
      <p>We will build reporting to match what your managers already use. We need the current layouts to do that.</p></div>
    <div class="card"><div class="n">02</div><h3>The corporate video at full resolution</h3>
      <p>We are working from a low-resolution copy.</p></div>
    <div class="card"><div class="n">03</div><h3>Photography of staff and garages</h3>
      <p>For the website and the identity applications. Real people in real locations beats anything we could buy.</p></div>
    <div class="card"><div class="n">04</div><h3>Trademark clearance on the product names</h3>
      <p><b>Crew</b>, <b>Console</b> and <b>Record</b> are our proposals. They are not in the build and should not be
      used publicly until your counsel clears them. <b>Passport</b> is already in use.</p></div>
  </div>
  <div class="note" style="margin-top:auto;padding-top:40px">None of these block the pilot starting. All four block
  something later, so the sooner the better.</div>
</div>''', num=17))

# 18 divider website
s.append(page('''
<div class="pad">
  <div class="num">03</div>
  <div class="kicker">Section three</div>
  <h1>The website</h1>
  <div class="lede">Built. Waiting on one decision, not on development.</div>
</div>''', cls="divider", num=18))

# 19 website
s.append(page('''
<div class="pad">
  <div class="kicker q">Website</div>
  <h1 class="sm">Where it stands</h1>
  <div class="cols c3" style="margin-top:70px">
    <div class="card"><div class="n">STATUS</div><h3>The build is done</h3>
      <p>Structure, content and pages are complete. This is not a project waiting to start.</p></div>
    <div class="card warn"><div class="n">BLOCKED ON</div><h3>The identity decision</h3>
      <p>Applying a standard Pioneer has not adopted would be premature. Section one decides this.</p></div>
    <div class="card acc"><div class="n">NEXT</div><h3>Branding applied</h3>
      <p>Once the identity is settled, applying it to the site is a short, contained piece of work. We will quote it
      against the agreed standard.</p></div>
  </div>
  <div class="note" style="margin-top:auto;padding-top:44px">We are deliberately not putting a number on this today.
  The scope depends entirely on which way the identity decision goes, and quoting before that would be guesswork.</div>
</div>''', num=19))

# 20 decisions + contact
s.append(page('''
<div class="pad">
  <div class="kicker">Before we leave</div>
  <h1 class="sm">Four decisions</h1>
  <div class="cols c4" style="margin-top:64px">
    <div class="card acc"><div class="n">DECISION 01</div><h3>Self-registration in the pilot?</h3>
      <p>Option A at $26&ndash;28K over seven weeks, or Option B at $33&ndash;35K over nine. We recommend A.</p></div>
    <div class="card"><div class="n">DECISION 02</div><h3>Adopt the identity standard?</h3>
      <p>Yes, no, or yes-with-changes. A no costs nothing; it stays our internal build standard.</p></div>
    <div class="card"><div class="n">DECISION 03</div><h3>Which garage runs the pilot?</h3>
      <p>We need the location, the attendants and roughly fifty residents.</p></div>
    <div class="card"><div class="n">DECISION 04</div><h3>Start date</h3>
      <p>Sign-off plus one week. Everything downstream moves with this.</p></div>
  </div>
  <div style="margin-top:auto;padding-top:56px;border-top:1px solid var(--line);display:flex;align-items:flex-end;justify-content:space-between">
    <div>
      <div style="font-family:var(--disp);font-weight:900;font-size:40px;color:var(--navy);letter-spacing:-.015em">VisualMedia, Ltd.</div>
      <div class="note" style="margin-top:12px;font-size:22px">dima@vismed3d.com</div>
    </div>
    <div style="display:flex;gap:14px;align-items:center">
      <div style="width:52px;height:8px;background:#FD2F38;border-radius:4px"></div>
      <div style="width:150px;height:8px;background:#0B2C5D;border-radius:4px"></div>
    </div>
  </div>
</div>''', num=20))

open("_part2.html","w").write("\n".join(s))
print("part 2:", len(s), "slides")
