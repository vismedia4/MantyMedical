# -*- coding: utf-8 -*-
"""
Pioneer Crew — retrieval chime candidates.

Brief (Jonathan, 10 Sep): persistent but not annoying. It repeats until a valet
accepts, so it has to survive being heard forty times in a shift.

Design constraints that follow from that:
  · energy concentrated 600 Hz – 3 kHz, which is where a garage is quietest and
    a small tablet speaker is loudest
  · soft attack (no click) and an exponential tail, so it never reads as an alarm
  · under 1.8 s, and it must resolve — an unresolved interval is what makes a
    repeating sound maddening
  · harmonically distinct from a stock phone notification
"""
import wave, struct, math

SR = 48000

def env(n, i, attack=0.008, decay=3.2):
    """Soft attack, exponential decay. i is the sample index, n the total."""
    t = i / SR
    a = min(1.0, t / attack) if attack > 0 else 1.0
    return a * math.exp(-decay * t)

def tone(freq, dur, partials, decay=3.2, attack=0.008, amp=1.0):
    n = int(SR * dur)
    out = [0.0] * n
    for i in range(n):
        t = i / SR
        s = 0.0
        for ratio, pa, pd in partials:
            s += pa * math.sin(2 * math.pi * freq * ratio * t) * math.exp(-pd * t)
        out[i] = s * env(n, i, attack, decay) * amp
    return out

def mix(layers, total):
    """layers = [(offset_seconds, samples)]"""
    buf = [0.0] * int(SR * total)
    for off, sig in layers:
        o = int(SR * off)
        for i, v in enumerate(sig):
            if o + i < len(buf):
                buf[o + i] += v
    return buf

def write(path, buf, peak_dbfs=-3.0):
    m = max(abs(v) for v in buf) or 1.0
    target = 10 ** (peak_dbfs / 20.0)
    g = target / m
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1.0, min(1.0, v * g)) * 32767)) for v in buf))
    return path

# Partial sets -------------------------------------------------------------
CHIME = [(1.0, 1.00, 2.6), (2.0, 0.22, 3.6), (3.0, 0.07, 5.0)]      # clean, woody
WARM  = [(1.0, 1.00, 2.2), (2.0, 0.30, 3.0), (3.0, 0.12, 4.2), (4.0, 0.04, 6.0)]
BELL  = [(1.0, 1.00, 1.7), (2.0, 0.40, 2.4), (2.4, 0.28, 3.0),      # inharmonic
         (3.0, 0.16, 3.8), (4.5, 0.08, 5.2), (5.4, 0.04, 6.5)]

# A · MARKER — two tones, descending fourth. Transit-platform register.
#   Institutional and calm. Reads as "attention", never as "alarm".
A = mix([
    (0.00, tone(784.0, 1.00, CHIME, decay=3.4)),   # G5
    (0.26, tone(587.3, 1.30, CHIME, decay=2.6)),   # D5
], 1.70)

# B · ARRIVAL — three tones rising and resolving. Warmer, reads as good news.
#   The one most likely to be liked on hearing and most likely to tire.
B = mix([
    (0.00, tone(587.3, 0.70, WARM, decay=4.2)),    # D5
    (0.17, tone(784.0, 0.70, WARM, decay=4.2)),    # G5
    (0.34, tone(987.8, 1.35, WARM, decay=2.4)),    # B5
], 1.80)

# C · SIGNAL — one struck bell, then a soft second strike.
#   Minimal, cuts furthest, least fatiguing across a shift.
C = mix([
    (0.00, tone(880.0, 1.40, BELL, decay=2.0)),
    (0.46, tone(880.0, 1.30, BELL, decay=2.2, amp=0.42)),
], 1.80)

for name, buf in (("A-marker", A), ("B-arrival", B), ("C-signal", C)):
    print(write("pioneer-chime-%s.wav" % name, buf))
