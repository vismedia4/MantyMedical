# -*- coding: utf-8 -*-
import os, html

TOTAL = 20
slides = []

def page(body, cls="", num=None, foot=True):
    f = ""
    if foot:
        f = ('<div class="foot"><div class="who"><b>VisualMedia, Ltd.</b>'
             '<span>&middot; Pioneer Parking, Inc &middot; 15 September 2026</span></div>'
             f'<div class="pg">{num:02d} / {TOTAL}</div></div>') if num else ""
    return (f'<div class="slide {cls}"><div class="rail"><i></i></div>{body}{f}</div>')

def tick(color="#0048A8"):
    return (f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')

def cross():
    return ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#98A0B0" '
            'stroke-width="2.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>')

def arrow():
    return ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#5A6478" '
            'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M12 5l7 7-7 7"/></svg>')

# ── 01 title ────────────────────────────────────────────────────────────
slides.append(page('''
<div class="pad" style="justify-content:center">
  <div class="kicker">VisualMedia, Ltd. &middot; 15 September 2026</div>
  <h1 style="font-size:106px;margin-top:34px">Pioneer Parking,&nbsp;Inc<br>Projects</h1>
  <div class="lede" style="font-size:34px;max-width:1080px">Corporate identity, the parking platform,
  and the website &mdash; where each one stands, what it costs, and the four decisions we need from you today.</div>
  <div style="margin-top:64px;display:flex;gap:16px;align-items:center">
    <div style="width:64px;height:8px;background:#FD2F38;border-radius:4px"></div>
    <div style="width:180px;height:8px;background:#0B2C5D;border-radius:4px"></div>
  </div>
</div>''', num=1))

# ── 02 agenda ───────────────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="kicker q">Today</div>
  <h1 class="sm">Three projects, one&nbsp;hour</h1>
  <div class="cols c3" style="margin-top:76px">
    <div class="card"><div class="n">01</div><h3>Corporate identity</h3>
      <p>We built Pioneer a design standard so the products had something to follow. It is yours to adopt, or not.</p></div>
    <div class="card acc"><div class="n">02</div><h3>The platform</h3>
      <p>Pioneer Passport is running. Today we agree the pilot scope, the timeline and the price.</p></div>
    <div class="card"><div class="n">03</div><h3>The website</h3>
      <p>Built, and waiting on the identity. A separate, smaller piece of work.</p></div>
  </div>
  <div class="note" style="margin-top:auto;padding-top:44px">Most of the hour belongs to the platform. It is the only
  item with a decision attached to a date.</div>
</div>''', num=2))

# ── 03 divider: identity ────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="num">01</div>
  <div class="kicker">Section one</div>
  <h1>Corporate identity</h1>
  <div class="lede">A standard we wrote on our own initiative, because the products needed one.</div>
</div>''', cls="divider", num=3))

# ── 04 why ──────────────────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="kicker q">Why this exists</div>
  <h1 class="sm">Nobody asked us for this</h1>
  <div class="lede">You cannot build four connected products without deciding what they look like. Rather than
  invent something per screen and reconcile it later, we wrote the standard first &mdash; <b>Pioneer Identity,
  Edition 1.1</b> &mdash; and built the platform against it.</div>
  <div class="cols c3" style="margin-top:70px">
    <div class="card"><div class="n">THE WORK</div><h3>Already done</h3>
      <p>Mark, colour, typography, iconography, contrast standards and digital tokens. In use in the running
      application today.</p></div>
    <div class="card"><div class="n">THE POSITION</div><h3>Yours to accept</h3>
      <p>If Pioneer wants it as the company&rsquo;s actual identity, it becomes yours. If not, it stays an internal
      build standard and costs you nothing.</p></div>
    <div class="card acc"><div class="n">THE OFFER</div><h3>We can complete it</h3>
      <p>Logo files in every format, licensed type, stationery, signage, vehicle and garage applications, and a
      guidelines document. Quoted separately.</p></div>
  </div>
</div>''', num=4))

# ── 05 colour ───────────────────────────────────────────────────────────
def swatch(hexv, name, use, dark=False):
    return (f'<div class="s"><div class="chip" style="background:{hexv}"></div>'
            f'<div class="meta"><div class="nm">{name}</div><div class="hx">{hexv}</div>'
            f'<div class="use">{use}</div></div></div>')

slides.append(page(f'''
<div class="pad">
  <div class="kicker">Identity &middot; Edition 1.1</div>
  <h1 class="sm">Colour, and the rule that governs&nbsp;it</h1>
  <div class="lede" style="font-size:26px;margin-top:20px">Red is rare, which is why it is noticed. It appears in the
  mark and in display type at 24px and above &mdash; never as body text, never as a button.</div>
  <div class="sw">
    {swatch("#FD2F38","Pioneer Red","Mark and display only")}
    {swatch("#0B2C5D","Pioneer Navy","Headings, sign panels")}
    {swatch("#0048A8","Signal Blue","Screens. Anything actionable")}
    {swatch("#1A1F33","Asphalt","Body text")}
    {swatch("#5A6478","Concrete","Secondary text")}
    {swatch("#E2E4E8","Line","Dividers and rules")}
    {swatch("#F2F4F8","Paper","The ground")}
  </div>
  <div style="margin-top:40px;display:flex;align-items:center;gap:26px">
    <div style="font-family:var(--disp);font-size:15px;font-weight:800;letter-spacing:.17em;text-transform:uppercase;color:var(--concrete)">Proportion</div>
    <div style="flex:1;display:flex;height:34px;border-radius:8px;overflow:hidden;border:1px solid var(--line)">
      <div style="width:58%;background:#F2F4F8"></div><div style="width:26%;background:#0B2C5D"></div>
      <div style="width:10%;background:#0048A8"></div><div style="width:6%;background:#FD2F38"></div>
    </div>
    <div class="note" style="font-size:19px">Paper 58 &middot; Navy 26 &middot; Blue 8 &middot; Red 6</div>
  </div>
</div>''', num=5))

# ── 06 typography ───────────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="kicker">Identity &middot; Edition 1.1</div>
  <h1 class="sm">Typography</h1>
  <div class="cols c2" style="margin-top:56px;gap:44px">
    <div class="card" style="padding:40px">
      <div class="n">DISPLAY</div>
      <div style="font-family:var(--disp);font-weight:900;font-size:82px;color:var(--navy);line-height:1;margin-top:18px;letter-spacing:-.02em">Overpass</div>
      <p style="font-size:21px;margin-top:20px">Drawn from Highway Gothic &mdash; the lettering on American road
      signs. It belongs on a parking structure. Headings, wayfinding, buttons, labels.</p>
    </div>
    <div class="card" style="padding:40px">
      <div class="n">CODES</div>
      <div style="font-family:var(--mono);font-weight:700;font-size:62px;color:var(--navy);line-height:1;margin-top:22px;letter-spacing:.02em">PP&#8209;1248</div>
      <p style="font-size:21px;margin-top:26px">Overpass Mono for decal numbers, ticket codes and times. Every digit
      the same width, so nothing shifts as a number changes.</p>
    </div>
  </div>
  <div class="card" style="margin-top:34px;padding:36px 40px;display:flex;gap:48px;align-items:center">
    <div style="flex:0 0 auto">
      <div class="n">INTERFACE</div>
      <div style="font-family:var(--body);font-weight:600;font-size:52px;color:var(--navy);line-height:1;margin-top:14px">Source&nbsp;Sans&nbsp;3</div>
    </div>
    <p style="font-size:21px;margin-top:0">Everything a person reads rather than scans. Source Serif 4 handles
    correspondence. All four families are open-licensed &mdash; <b style="color:var(--navy)">no licence fees, ever,
    on any number of devices</b>.</p>
  </div>
</div>''', num=6))

# ── 07 identity in use ──────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="kicker">Identity &middot; in use</div>
  <h1 class="sm">Not a moodboard &mdash; a running&nbsp;product</h1>
  <div class="shots" style="margin-top:40px">
    <div class="shot">
      <div class="ph" style="width:300px"><img src="img/01-passport-landing-phone.webp"></div>
      <div class="cap">Passport &middot; sign in</div>
    </div>
    <div class="shot">
      <div class="ph" style="width:300px"><img src="img/02-passport-home-phone.webp"></div>
      <div class="cap">Passport &middot; vehicle status</div>
    </div>
    <div class="shot" style="flex:1;max-width:760px">
      <div class="dt" style="width:100%"><img src="img/03-valet-vehicles-desktop.png"></div>
      <div class="cap">Valet station &middot; vehicles</div>
    </div>
  </div>
  <div class="note" style="margin-top:44px">Every colour, every typeface and every contrast pair on these screens
  comes from the standard. It was applied as the product was built, not retrofitted onto it.</div>
</div>''', cls="paper", num=7))

# ── 08 divider: platform ────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="num">02</div>
  <div class="kicker">Section two</div>
  <h1>The platform</h1>
  <div class="lede">Pioneer Passport. What is built, what the pilot covers, what it costs.</div>
</div>''', cls="divider", num=8))

# ── 09 what it is ───────────────────────────────────────────────────────
slides.append(page(f'''
<div class="pad">
  <div class="kicker q">The platform</div>
  <h1 class="sm">One system, four&nbsp;audiences</h1>
  <div class="cols c4" style="margin-top:70px">
    <div class="card acc"><div class="n">LIVE</div><h3>Passport<br>&mdash; residents</h3>
      <p>Request the car. Watch it come. Three states, one estimate, nothing else to learn.</p></div>
    <div class="card acc"><div class="n">LIVE</div><h3>Valet<br>station</h3>
      <p>The queue, the vehicles, the recent history. Names and decals &mdash; never a phone number.</p></div>
    <div class="card"><div class="n">PHASE 2</div><h3>Manager<br>console</h3>
      <p>Approvals, overrides, staff, reports. One place to run a garage.</p></div>
    <div class="card"><div class="n">PHASE 2</div><h3>Custody<br>record</h3>
      <p>Every action signed and time-stamped. The answer when a customer disputes a scratch.</p></div>
  </div>
  <div class="note" style="margin-top:auto;padding-top:44px"><b style="color:var(--navy)">The data model is
  multi-tenant from day one.</b> That is deliberate: it is what would let Pioneer license this platform to other
  operators rather than only run it.</div>
</div>''', num=9))

# ── 10 built today ──────────────────────────────────────────────────────
slides.append(page('''
<div class="pad">
  <div class="kicker">Working today</div>
  <h1 class="sm">The retrieval loop, end to&nbsp;end</h1>
  <div style="display:flex;gap:60px;margin-top:44px;flex:1;min-height:0">
    <div style="flex:0 0 330px;display:flex;flex-direction:column;align-items:center">
      <div class="ph" style="width:330px"><img src="img/02-passport-home-phone.webp"></div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
      <ul class="tick">
        <li>''' + tick() + '''<div>A resident opens Passport and sees <b>their own vehicle</b>, by make, model and colour, with the decal masked.</div></li>
        <li>''' + tick() + '''<div>One tap requests it. The request lands on the valet station queue immediately.</div></li>
        <li>''' + tick() + '''<div>The stepper moves &mdash; <b>Pending &rarr; Retrieving vehicle &rarr; Ready for pickup</b> &mdash; with an honest estimate rather than a spinner.</div></li>
        <li>''' + tick() + '''<div>An attendant sees the name, the decal, the parking location and any internal note. <b>Never a phone number.</b></div></li>
        <li>''' + tick() + '''<div>Every state change is written to an append-only log.</div></li>
      </ul>
      <div class="card acc" style="margin-top:44px">
        <h3 style="font-size:24px">What the pilot is actually testing</h3>
        <p style="font-size:20px">Not whether the screens work &mdash; they do. Whether a resident trusts the
        estimate enough to stop calling the front desk. That is the only question worth seven weeks.</p>
      </div>
    </div>
  </div>
</div>''', cls="paper", num=10))

open("_part1.html","w").write("\n".join(slides))
print("part 1:", len(slides), "slides")
