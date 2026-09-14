# Stand chime — three candidates

**🔒 INTERNAL — VisualMedia, Ltd.** · Safe to play for the client.

The sound that tells a valet a car has been requested. Jonathan raised the sound design
personally on 10 September: *"persistent, but not annoying."*

| File | Candidate | Character |
|---|---|---|
| `pioneer-chime-A-marker.wav` | **A · Marker** | Two tones falling a fourth, G5 → D5. Station-announcement register |
| `pioneer-chime-B-arrival.wav` | **B · Arrival** | Three tones rising, D5 → G5 → B5. Warm, reads as good news |
| `pioneer-chime-C-signal.wav` | **C · Signal** | One struck bell at A5 with a soft second strike. Minimal |

48 kHz, 16-bit mono, all matched at −3 dBFS peak so a comparison is fair.

**Comparison page:** https://claude.ai/code/artifact/39e8f764-93a8-4708-b9ec-f2e84d0a543e —
plays each one and runs the chosen candidate on a repeat cycle with an Accept button, which
is the test that actually separates them.

## Why these three, and what constrains them

The chime repeats until a valet accepts, so it is never judged on one hearing. It is judged
on the fortieth, at the end of a shift, through a tablet speaker, over an engine.

- **600 Hz – 3 kHz.** Where a garage is quietest and a small speaker is loudest.
- **Soft attack, exponential tail.** A hard onset reads as an alarm and fatigues fast.
- **Under 1.8 s**, and it must **resolve.** An unresolved phrase keeps asking for an
  answer, which is precisely what makes a repeating sound maddening.
- **Harmonically unlike a stock phone notification**, or valets learn to ignore it.

## Our read

**A · Marker** wears best. The falling fourth resolves, so the ear stops anticipating.
**B · Arrival** is the one most likely to be liked in the room and least likely to survive a
shift. **C · Signal** cuts furthest but sits closest to a generic notification tone.

Expect the room to prefer B. Worth saying out loud that first-hearing appeal and
fortieth-hearing tolerance are different tests, and only the second one matters.

## Regenerating

```bash
python3 docs/chime/synth.py    # → the three .wav files
python3 docs/chime/page.py     # → the comparison page, audio inlined
```

Pure stdlib additive synthesis — pitch, interval, partials and decay are all parameters in
`synth.py`. The chosen candidate gets tuned there rather than replaced, then measured on the
actual tablet at the actual stand.
