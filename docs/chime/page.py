# -*- coding: utf-8 -*-
import base64

def b64(f):
    return "data:audio/wav;base64," + base64.b64encode(open(f, 'rb').read()).decode()

A = b64('pioneer-chime-A-marker.wav')
B = b64('pioneer-chime-B-arrival.wav')
C = b64('pioneer-chime-C-signal.wav')

CANDIDATES = [
    ("A", "Marker", "Two tones, falling a fourth",
     "G5 → D5", "784 → 587 Hz", "1.70 s",
     "The register of a station announcement. Institutional, unhurried, clearly "
     "<em>attention</em> rather than <em>alarm</em>.",
     "Wears best of the three. The falling interval resolves, so the ear stops "
     "expecting anything after it.",
     "Reads as neutral rather than warm. Nobody will love it on first hearing."),
    ("B", "Arrival", "Three tones, rising and resolving",
     "D5 → G5 → B5", "587 → 988 Hz", "1.80 s",
     "Warmer and more melodic. Sounds like good news, which is what it usually is "
     "&mdash; a car is ready and someone is about to be pleased.",
     "The one most likely to be liked in the room on Tuesday.",
     "Also the one most likely to grate by the fortieth repeat. Rising phrases "
     "keep asking for an answer."),
    ("C", "Signal", "One struck bell, then a soft second",
     "A5", "880 Hz", "1.80 s",
     "Minimal. A single inharmonic strike with a long tail, and a quieter echo of "
     "itself half a second later.",
     "Cuts furthest through engine noise and carries best on a small speaker. "
     "Least fatiguing across a shift.",
     "Closest of the three to a generic phone notification &mdash; the one a valet "
     "might learn to tune out."),
]

rows = []
for key, name, sub, notes, hz, dur, char, win, risk in CANDIDATES:
    rows.append(f'''
      <article class="cand" id="cand-{key}">
        <div class="cand-id"><span class="letter">{key}</span><span class="cand-name">{name}</span></div>
        <div class="cand-main">
          <p class="cand-sub">{sub}</p>
          <p class="cand-char">{char}</p>
          <dl class="tradeoff">
            <div class="win"><dt>Where it wins</dt><dd>{win}</dd></div>
            <div class="risk"><dt>Where it risks</dt><dd>{risk}</dd></div>
          </dl>
        </div>
        <div class="cand-side">
          <button type="button" class="play" id="play-{key}" data-k="{key}"
                  aria-label="Play candidate {key}, {name}">
            <svg viewBox="0 0 24 24" aria-hidden="true" width="19" height="19"><path d="M8 5.5v13l10-6.5z"/></svg>
            <span class="play-t">Play</span>
          </button>
          <dl class="spec">
            <div><dt>Notes</dt><dd class="mono">{notes}</dd></div>
            <div><dt>Pitch</dt><dd class="mono">{hz}</dd></div>
            <div><dt>Length</dt><dd class="mono">{dur}</dd></div>
          </dl>
        </div>
      </article>''')

HTML = '''<title>Pioneer Stand Chime</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Overpass:wght@600;700;800;900&family=Overpass+Mono:wght@400;600;700&family=Source+Sans+3:wght@400;600;700&display=swap">

<style>
:root{
  --ground:#F2F4F8; --surface:#FFFFFF; --sunk:#E9ECF2;
  --ink:#1A1F33; --muted:#5A6478; --faint:#8A93A6;
  --line:#E2E4E8; --line-soft:#EDEFF4;
  --navy:#0B2C5D; --accent:#0048A8; --accent-soft:#E3ECF8; --accent-ink:#FFFFFF;
  --red:#FD2F38;
  --go:#15803D; --go-soft:#DEEFE4;
  --warn:#8A4B00; --warn-soft:#F7EBD9; --warn-line:#D9B57A;
  --shadow:0 1px 2px rgba(11,44,93,.07);
  --shadow-lift:0 6px 20px rgba(11,44,93,.10);
  --display:"Overpass","Arial Narrow",Arial,sans-serif;
  --body:"Source Sans 3","Segoe UI",Arial,sans-serif;
  --mono:"Overpass Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0B1220; --surface:#141D33; --sunk:#1C2740;
    --ink:#E8ECF4; --muted:#9AA6BC; --faint:#7A8599;
    --line:#27324C; --line-soft:#1E2840;
    --navy:#C9D8F0; --accent:#6BA5F2; --accent-soft:#152546; --accent-ink:#08122A;
    --red:#FF5A61;
    --go:#4FA86A; --go-soft:#13271B;
    --warn:#D9A05A; --warn-soft:#2A2114; --warn-line:#5A4526;
    --shadow:0 1px 2px rgba(0,0,0,.35);
    --shadow-lift:0 6px 20px rgba(0,0,0,.45);
  }
}
:root[data-theme="dark"]{
  --ground:#0B1220; --surface:#141D33; --sunk:#1C2740;
  --ink:#E8ECF4; --muted:#9AA6BC; --faint:#7A8599;
  --line:#27324C; --line-soft:#1E2840;
  --navy:#C9D8F0; --accent:#6BA5F2; --accent-soft:#152546; --accent-ink:#08122A;
  --red:#FF5A61;
  --go:#4FA86A; --go-soft:#13271B;
  --warn:#D9A05A; --warn-soft:#2A2114; --warn-line:#5A4526;
  --shadow:0 1px 2px rgba(0,0,0,.35);
  --shadow-lift:0 6px 20px rgba(0,0,0,.45);
}

*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--body);
     font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding-inline:24px;padding-block:0 72px}
@media (max-width:640px){.wrap{padding-inline:16px}}
h1,h2,h3{font-family:var(--display);color:var(--navy);margin:0;letter-spacing:-.015em;text-wrap:balance}
p,dd,dl,dt{margin:0}
em{font-style:italic;color:var(--muted)}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.eyebrow{font-family:var(--display);font-size:.6875rem;font-weight:800;
         letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}

/* masthead */
.mast{border-bottom:2px solid var(--navy);padding-block:34px 24px;margin-bottom:34px}
.mast-top{display:flex;flex-wrap:wrap;gap:10px 28px;justify-content:space-between;align-items:baseline}
.mast h1{font-size:clamp(1.9rem,5vw,3rem);font-weight:900;line-height:1.03;margin-block:14px 14px}
.mast .lede{font-size:1.0625rem;color:var(--muted);max-width:62ch}

/* brief */
.brief{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--red);
       border-radius:2px;padding:18px 22px;display:grid;gap:10px;box-shadow:var(--shadow)}
.brief .q{font-family:var(--display);font-size:1.0625rem;font-weight:700;color:var(--navy)}
.brief p{font-size:.9375rem;max-width:74ch}
.brief .constraints{display:flex;flex-wrap:wrap;gap:8px;margin-top:3px}
.brief .constraints span{font-family:var(--mono);font-size:.6875rem;letter-spacing:.05em;
       background:var(--sunk);color:var(--muted);padding:4px 9px;border-radius:2px}

/* section heads */
.sec-head{display:flex;align-items:baseline;gap:16px;border-bottom:1px solid var(--line);
          padding-bottom:10px;margin:48px 0 22px}
.sec-head h2{font-size:1.375rem;font-weight:800;flex:1}

/* candidates */
.cands{display:flex;flex-direction:column;gap:14px}
.cand{background:var(--surface);border:1px solid var(--line);border-radius:2px;
      box-shadow:var(--shadow);padding:20px 22px;
      display:grid;grid-template-columns:1fr 232px;gap:22px 26px;align-items:start}
.cand.on{border-color:var(--accent);box-shadow:var(--shadow-lift)}
@media (max-width:720px){.cand{grid-template-columns:1fr}}
.cand-id{grid-column:1/-1;display:flex;align-items:baseline;gap:12px}
.letter{font-family:var(--display);font-size:.75rem;font-weight:800;letter-spacing:.1em;
        background:var(--navy);color:var(--surface);width:26px;height:26px;border-radius:2px;
        display:inline-flex;align-items:center;justify-content:center;flex:none;align-self:center}
:root[data-theme="dark"] .letter,
:root:not([data-theme="light"]) .letter{color:var(--ground)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .letter{color:#FFFFFF}}
.cand-name{font-family:var(--display);font-size:1.375rem;font-weight:800;color:var(--navy)}
.cand-sub{font-size:.8125rem;color:var(--faint);font-family:var(--mono);letter-spacing:.02em}
.cand-char{font-size:.9375rem;margin-top:9px;max-width:60ch}
.tradeoff{margin-top:15px;display:grid;gap:9px}
.tradeoff div{padding-left:15px;position:relative}
.tradeoff div::before{content:"";position:absolute;left:0;top:.62em;width:7px;height:2px}
.tradeoff .win::before{background:var(--go)}
.tradeoff .risk::before{background:var(--warn)}
.tradeoff dt{font-family:var(--mono);font-size:.625rem;letter-spacing:.12em;text-transform:uppercase;
             color:var(--faint);margin-bottom:2px}
.tradeoff dd{font-size:.875rem;color:var(--muted)}

.cand-side{display:flex;flex-direction:column;gap:14px}
.spec{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:2px;overflow:hidden}
.spec > div{background:var(--surface);padding:8px 11px;display:flex;justify-content:space-between;gap:12px}
.spec dt{font-family:var(--mono);font-size:.625rem;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.spec dd{font-size:.8125rem;color:var(--ink)}

/* buttons */
button{font-family:var(--body);cursor:pointer;border-radius:2px;transition:border-color .12s,background .12s,color .12s}
button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.play{display:inline-flex;align-items:center;justify-content:center;gap:9px;
      background:var(--accent);color:var(--accent-ink);border:1px solid var(--accent);
      font-size:1rem;font-weight:700;padding:11px 16px;width:100%}
.play svg{fill:currentColor;flex:none}
.play:hover{filter:brightness(1.08)}
.play.playing{background:var(--go);border-color:var(--go)}

/* stand test */
.stand{background:var(--surface);border:1px solid var(--line);border-radius:2px;
       box-shadow:var(--shadow);padding:24px;display:grid;gap:20px}
.stand-top{display:grid;gap:7px}
.stand-top h3{font-size:1.125rem;font-weight:800}
.stand-top p{font-size:.9375rem;color:var(--muted);max-width:70ch}
.controls{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media (max-width:640px){.controls{grid-template-columns:1fr}}
.field{display:grid;gap:8px}
.field-label{font-family:var(--mono);font-size:.625rem;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.seg{display:flex;gap:6px;flex-wrap:wrap}
.seg button{background:var(--surface);border:1px solid var(--line);color:var(--navy);
            font-size:.9375rem;font-weight:700;padding:8px 14px}
.seg button:hover{border-color:var(--accent);color:var(--accent)}
.seg button[aria-pressed="true"]{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}

.runner{display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;
        background:var(--sunk);border-radius:2px;padding:16px 18px}
.readout{display:flex;gap:26px;flex-wrap:wrap}
.readout div{display:grid;gap:2px}
.readout dt{font-family:var(--mono);font-size:.625rem;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.readout dd{font-family:var(--display);font-size:1.75rem;font-weight:800;color:var(--navy);line-height:1;
            font-variant-numeric:tabular-nums}
.runner-btns{display:flex;gap:9px}
#start{background:var(--navy);color:var(--surface);border:1px solid var(--navy);font-size:1rem;font-weight:700;padding:12px 20px}
:root[data-theme="dark"] #start,:root:not([data-theme="light"]) #start{color:var(--ground)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) #start{color:#FFFFFF}}
#accept{background:var(--surface);color:var(--go);border:1px solid var(--go);font-size:1rem;font-weight:700;padding:12px 20px}
#accept:disabled{opacity:.4;cursor:not-allowed}
#start.live{background:var(--red);border-color:var(--red);color:#FFFFFF}
.status{font-size:.875rem;color:var(--muted);min-height:1.4em}
.status b{color:var(--ink);font-weight:600}

footer{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);font-size:.8125rem;color:var(--faint);max-width:76ch;display:grid;gap:9px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">

<header class="mast">
  <div class="mast-top">
    <div class="eyebrow">VisualMedia, Ltd. &nbsp;/&nbsp; Pioneer Parking</div>
    <div class="eyebrow">Three candidates &nbsp;·&nbsp; 15 September</div>
  </div>
  <h1>The stand chime</h1>
  <p class="lede">Three candidates for the sound that tells a valet a car has been
  requested. Play them, then run one the way the stand will actually run it &mdash;
  repeating until somebody accepts.</p>
</header>

<div class="brief">
  <p class="q">&ldquo;Persistent, but not annoying.&rdquo;</p>
  <p>That was the brief, and it is harder than it sounds. The chime repeats until a valet
  accepts, so it is not judged on one hearing &mdash; it is judged on the fortieth, at the end
  of a shift, through a tablet speaker, over an engine. Every choice below follows from that.</p>
  <div class="constraints">
    <span>600 Hz &ndash; 3 kHz</span><span>soft attack, no click</span>
    <span>under 1.8 s</span><span>resolves</span><span>matched at &minus;3 dBFS</span>
  </div>
</div>

<div class="sec-head"><h2>Three candidates</h2><div class="eyebrow">A &middot; B &middot; C</div></div>
<div class="cands">__ROWS__</div>

<div class="sec-head"><h2>Hear it the way the stand does</h2><div class="eyebrow">The real test</div></div>
<div class="stand">
  <div class="stand-top">
    <h3>Repeat until accepted</h3>
    <p>Pick a candidate and start it. It will repeat on the interval you choose until you
    press Accept, exactly as it will at the stand. Let it run past six or seven repeats
    before deciding &mdash; that is where the three separate.</p>
  </div>

  <div class="controls">
    <div class="field">
      <span class="field-label" id="lab-c">Candidate</span>
      <div class="seg" role="group" aria-labelledby="lab-c">
        <button type="button" class="pick" data-k="A" aria-pressed="true">A &middot; Marker</button>
        <button type="button" class="pick" data-k="B" aria-pressed="false">B &middot; Arrival</button>
        <button type="button" class="pick" data-k="C" aria-pressed="false">C &middot; Signal</button>
      </div>
    </div>
    <div class="field">
      <span class="field-label" id="lab-i">Repeat interval</span>
      <div class="seg" role="group" aria-labelledby="lab-i">
        <button type="button" class="ivl" data-s="3" aria-pressed="false">3 s</button>
        <button type="button" class="ivl" data-s="5" aria-pressed="true">5 s</button>
        <button type="button" class="ivl" data-s="8" aria-pressed="false">8 s</button>
      </div>
    </div>
  </div>

  <div class="runner">
    <dl class="readout">
      <div><dt>Repeats</dt><dd id="count">0</dd></div>
      <div><dt>Waiting</dt><dd id="elapsed">0:00</dd></div>
    </dl>
    <div class="runner-btns">
      <button type="button" id="start">Start the stand</button>
      <button type="button" id="accept" disabled>Accept</button>
    </div>
  </div>
  <p class="status" id="status">Nothing waiting.</p>
</div>

<footer>
  <p>Synthesised to the constraints above rather than licensed from a library, so the
  chosen candidate can be tuned rather than replaced &mdash; pitch, interval and tail are
  all parameters. Whichever is chosen gets a final pass measured on the actual tablet at
  the actual stand, since a speaker in a concrete garage is the only opinion that counts.</p>
  <p>Set in the Pioneer Parking identity, Edition 1.1.</p>
</footer>

</div>

<script>
(function () {
  var SRC = { A: "__A__", B: "__B__", C: "__C__" };
  var NAME = { A: "Marker", B: "Arrival", C: "Signal" };
  var pool = {}, pick = "A", ivl = 5, timer = null, tick = null, n = 0, t0 = 0, live = false;

  Object.keys(SRC).forEach(function (k) { pool[k] = new Audio(SRC[k]); pool[k].preload = "auto"; });

  function play(k) {
    var a = pool[k];
    try { a.currentTime = 0; a.play(); } catch (e) {}
  }

  // one-shot buttons on each candidate
  document.querySelectorAll(".play").forEach(function (btn) {
    var k = btn.dataset.k;
    btn.addEventListener("click", function () {
      play(k);
      btn.classList.add("playing");
      btn.querySelector(".play-t").textContent = "Playing";
      setTimeout(function () {
        btn.classList.remove("playing");
        btn.querySelector(".play-t").textContent = "Play";
      }, 1800);
    });
  });

  function markCand() {
    document.querySelectorAll(".cand").forEach(function (el) {
      el.classList.toggle("on", el.id === "cand-" + pick);
    });
  }

  document.querySelectorAll(".pick").forEach(function (b) {
    b.addEventListener("click", function () {
      pick = b.dataset.k;
      document.querySelectorAll(".pick").forEach(function (o) {
        o.setAttribute("aria-pressed", o === b ? "true" : "false");
      });
      markCand();
      if (live) { stop(); start(); }
    });
  });

  document.querySelectorAll(".ivl").forEach(function (b) {
    b.addEventListener("click", function () {
      ivl = parseInt(b.dataset.s, 10);
      document.querySelectorAll(".ivl").forEach(function (o) {
        o.setAttribute("aria-pressed", o === b ? "true" : "false");
      });
      if (live) { stop(); start(); }
    });
  });

  function fmt(ms) {
    var s = Math.floor(ms / 1000);
    return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
  }

  function start() {
    live = true; n = 0; t0 = Date.now();
    document.getElementById("count").textContent = "0";
    document.getElementById("elapsed").textContent = "0:00";
    var s = document.getElementById("start");
    s.textContent = "Stop"; s.classList.add("live");
    document.getElementById("accept").disabled = false;
    fire();
    timer = setInterval(fire, ivl * 1000);
    tick = setInterval(function () {
      document.getElementById("elapsed").textContent = fmt(Date.now() - t0);
    }, 250);
  }

  function fire() {
    play(pick);
    n++;
    document.getElementById("count").textContent = String(n);
    document.getElementById("status").innerHTML =
      "Candidate <b>" + pick + " &middot; " + NAME[pick] + "</b> is repeating every " +
      ivl + " seconds. A car is waiting until someone accepts.";
  }

  function stop(accepted) {
    live = false;
    clearInterval(timer); clearInterval(tick);
    var s = document.getElementById("start");
    s.textContent = "Start the stand"; s.classList.remove("live");
    document.getElementById("accept").disabled = true;
    document.getElementById("status").innerHTML = accepted
      ? "Accepted after <b>" + n + "</b> " + (n === 1 ? "repeat" : "repeats") +
        " and <b>" + fmt(Date.now() - t0) + "</b> waiting."
      : "Stopped.";
  }

  document.getElementById("start").addEventListener("click", function () {
    if (live) { stop(false); } else { start(); }
  });
  document.getElementById("accept").addEventListener("click", function () {
    if (live) stop(true);
  });

  markCand();
})();
</script>'''

HTML = HTML.replace("__ROWS__", "".join(rows))
HTML = HTML.replace("__A__", A).replace("__B__", B).replace("__C__", C)
open("pioneer-stand-chime.html", "w", encoding="utf-8").write(HTML)
print("bytes", len(HTML))
