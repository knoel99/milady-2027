#!/usr/bin/env python3
"""mix.py: the film's sound: narration + an original music bed + sound effects, all synthesized in code
(no samples, no third-party recordings), mixed to -16 LUFS integrated with true peak <= -1 dBTP.

Input: the timeline written by build.js (script/_build/<name>_timeline.json): per scene its start and
duration on the film clock, lead_in, level (L0..L5), the narration track (audio/scenes/<id>.wav or an
external fit), optional "music" override, and the resolved sound-effect events (scene time, id, gain).

  narration  each scene track placed at start + lead_in, cut at the scene end (frame-exact, 48 kHz).
  music      a slow pad (two detuned voices per note, soft harmonics, sub-bass root) over 4-chord
             progressions in D dorian / F lydian colours, one progression per unit, chords every 8 s with
             2.5 s crossfades, plus sparse soft bell notes. Level by scene: L0-L1 1.0, L2 0.8, L3 0.35,
             L4-L5 0 (silence), smoothed over 3 s; a scene may set "music": false or {"gain": x}. Ducked by
             12 dB under the voice (side-chain on the narration envelope, attack 60 ms, release 600 ms).
             The bed sits 15 LU under the narration in the gaps.
  effects    synthesized events (EFFECTS below): needle (two-note flip), tick (zero crossing), detent
             (knob), whoosh (chapter card), impact, hiss (sample cloud), squeal (feedback), chime
             (question card), pop. gain_db = peak level in dBFS in a -16 LUFS mix. Ducked 6 dB under speech.
  master     one gain for everything (stems stay additive: full = narration + music + effects), then a
             look-ahead peak limiter on the full mix only (1-ms blocks, ceiling -2 dBFS), loudness re-checked,
             true peak measured on the encoded AAC (ebur128, 4x oversampled) and the ceiling lowered if needed.
             Everything is streamed to ffmpeg in 30-s chunks (a 60-min film mixes in a few minutes).
Outputs (AAC 192 kb/s, 48 kHz stereo): <outdir>/stems/<name>_{narration,music,effects,nonarration}.m4a,
<outdir>/stems/<name>_full.m4a, and <outdir>/stems/<name>_mix.json (loudness report, cache key).
Usage: python3 -I audio/mix.py script/_build/core_timeline.json --outdir out [--force]
       python3 -I audio/mix.py --demo out/sfx_demo.m4a    (every effect once, for listening)
"""
import argparse, hashlib, json, math, os, re, subprocess, sys, threading, wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SR = 48000
TARGET_I, CEIL_TP, LIMIT_DBFS = -16.0, -1.0, -2.0
MUSIC_UNDER_VOICE_LU, MUSIC_DUCK_DB, FX_DUCK_DB = 15.0, 12.0, 6.0
LEVEL_GAIN = {"L0": 1.0, "L1": 1.0, "L2": 0.8, "L3": 0.35, "L4": 0.0, "L5": 0.0}
SEG, XF = 8.0, 2.5
MUSIC_CACHE = os.path.join(HERE, "cache", "music")
MIX_VERSION = 4


# ----------------------------------------------------------------------------- ffmpeg helpers (streamed)
CHUNK = SR * 30                 # 30 s per chunk (a multiple of the 1-ms limiter block)


def chunks_of(x):
    for i in range(0, len(x), CHUNK):
        yield x[i:i + CHUNK]


def ff_pipe(args, chunks, ch):
    """Feed float32 chunks to ffmpeg's stdin; returns its stderr (drained in a thread: no deadlock)."""
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "pipe:0", *args],
                         stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    err = []
    th = threading.Thread(target=lambda: err.append(p.stderr.read()))
    th.start()
    try:
        for c in chunks:
            p.stdin.write(np.ascontiguousarray(c, dtype=np.float32).tobytes())
    finally:
        p.stdin.close()
        p.wait()
        th.join()
    s = err[0].decode("utf8", "replace") if err else ""
    if p.returncode:
        raise SystemExit("[mix] ffmpeg failed: " + s[-600:])
    return s


def parse_ebur(s):
    s = s[s.rfind("Summary:"):]
    v = lambda m: float(m.group(1)) if m else None
    return {"I": v(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", s)), "TP": v(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", s)),
            "LRA": v(re.search(r"LRA:\s+(-?[\d.]+) LU", s))}


def ff_loudness(chunks, ch, peak=False):
    """EBU R128 integrated loudness (and true peak if asked) of a stream of chunks."""
    return parse_ebur(ff_pipe(["-af", "ebur128=framelog=verbose" + (":peak=true" if peak else ""), "-f", "null", "-"], chunks, ch))


def ff_measure(x):
    """(integrated LUFS, -inf) of an array (n,) or (n, 2); -inf for silence (true peak: ff_measure_file)."""
    if not np.any(x):
        return float("-inf"), float("-inf")
    r = ff_loudness(chunks_of(x), 1 if x.ndim == 1 else x.shape[1], peak=False)
    return (r["I"] if r["I"] is not None else float("-inf")), (r["TP"] if r["TP"] is not None else float("-inf"))


def ff_encode(chunks, ch, path):
    tmp = path + ".part.m4a"
    ff_pipe(["-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2", "-movflags", "+faststart", "-y", tmp], chunks, ch)
    os.replace(tmp, path)


def ff_measure_file(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=framelog=verbose:peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    return parse_ebur(p.stderr)


# ----------------------------------------------------------------------------- limiter (look-ahead, 1-ms blocks)
LB = 48                          # block = 1 ms


def limiter_env(chunk_iter, n, ceiling_dbfs, release_s=0.08):
    """Gain per 1-ms block so that |x * gain| stays under the ceiling: block peaks -> required gain ->
    minimum over -3..+2 blocks (look-ahead) -> one-pole recovery (release). None if nothing exceeds."""
    lim = 10 ** (ceiling_dbfs / 20)
    nb = -(-n // LB)
    peaks = np.zeros(nb, dtype=np.float32)
    k = 0
    for c in chunk_iter:
        m = len(c)
        pad = (-m) % LB
        a = np.abs(c).max(axis=1) if c.ndim == 2 else np.abs(c)
        if pad:
            a = np.concatenate([a, np.zeros(pad, dtype=a.dtype)])
        bp = a.reshape(-1, LB).max(axis=1)
        peaks[k:k + len(bp)] = bp
        k += len(bp)
    if float(peaks.max(initial=0)) <= lim:
        return None
    req = np.minimum(1.0, lim / np.maximum(peaks, 1e-9))
    req = np.lib.stride_tricks.sliding_window_view(np.pad(req, (3, 2), constant_values=1.0), 6).min(axis=1)
    env = np.empty(nb, dtype=np.float32)
    a_rel = 1 - math.exp(-1 / (release_s * 1000))
    g = 1.0
    idx = np.flatnonzero(req < 1.0)
    env[:] = 1.0
    # recovery only matters after a reduction: walk from each reduced block until the gain is back to ~1
    i, last = 0, -1
    for b0 in idx:
        if b0 <= last:
            continue
        g = float(env[b0 - 1]) if b0 > 0 else 1.0
        b = b0
        while b < nb:
            g = min(float(req[b]), g + (1 - g) * a_rel)
            env[b] = g
            if g > 0.9999 and req[b] >= 1.0:
                break
            b += 1
        last = b
    return env


def env_gain(env, i, j):
    """Per-sample gain for samples [i, j) from the block envelope (linear between block centres)."""
    if env is None:
        return None
    pos = (np.arange(i, j, dtype=np.float64) + 0.5) / LB - 0.5
    return np.interp(pos, np.arange(len(env)), env).astype(np.float32)


def read_wav(path):
    with wave.open(path) as w:
        n, sr, ch = w.getnframes(), w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        raise SystemExit(f"{path}: {sr} Hz, expected {SR}")
    return x


# ----------------------------------------------------------------------------- sound effects (synthesized)
def _t(d):
    return np.arange(int(d * SR)) / SR


def _norm(x):
    m = np.max(np.abs(x)) or 1.0
    return (x / m).astype(np.float32)


def _svf(x, fc, q=0.7, mode="bp"):
    """Chamberlin state-variable filter with a per-sample cutoff array (small buffers only)."""
    lo = bp = 0.0
    out = np.empty_like(x)
    fc = np.broadcast_to(fc, x.shape)
    damp = 1.0 / q
    for i in range(len(x)):
        f = 2 * math.sin(math.pi * min(fc[i], SR / 6) / SR)
        hi = x[i] - lo - damp * bp
        bp += f * hi
        lo += f * bp
        out[i] = bp if mode == "bp" else (lo if mode == "lp" else hi)
    return out


def fx_needle(rng, dur=None):
    """M1, the flip: two soft bell notes, E5 then B4."""
    out = np.zeros(int(1.3 * SR))
    for k, (f, t0) in enumerate(((659.25, 0.0), (493.88, 0.2))):
        t = _t(1.0)
        e = np.exp(-t / 0.32) * np.minimum(1, t / 0.004)
        s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / 0.12) \
            + 0.08 * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t / 0.05)
        i = int(t0 * SR)
        out[i:i + len(t)] += (0.9 if k else 1.0) * e * s
    return _norm(out)


def fx_tick(rng, dur=None):
    t = _t(0.05)
    return _norm(np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.006) + 0.35 * rng.normal(0, 1, len(t)) * np.exp(-t / 0.0015))


def fx_detent(rng, dur=None):
    t = _t(0.04)
    return _norm(np.sin(2 * np.pi * 1050 * t) * np.exp(-t / 0.007) + 0.5 * rng.normal(0, 1, len(t)) * np.exp(-t / 0.001))


def fx_whoosh(rng, dur=0.9):
    t = _t(dur)
    p = t / dur
    fc = 350 + 2600 * np.sin(np.pi * np.clip(p * 1.1, 0, 1)) ** 2
    x = _svf(rng.normal(0, 1, len(t)), fc, q=2.6)
    env = np.sin(np.pi * np.clip(p, 0, 1)) ** 2 * (0.4 + 0.6 * p)
    return _norm(x * env)


def fx_impact(rng, dur=None):
    t = _t(1.6)
    f = 42 + 70 * np.exp(-t / 0.09)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.33)
    click = _svf(rng.normal(0, 1, len(t)), 900.0, q=0.8) * np.exp(-t / 0.012) * 0.6
    tail = _svf(rng.normal(0, 1, len(t)), 500.0, q=0.6, mode="lp") * np.exp(-t / 0.55) * 0.08
    return _norm(body + click + tail)


def fx_hiss(rng, dur=2.0):
    n = int(dur * SR)
    out = np.zeros(n)
    for _ in range(int(140 * dur)):
        L = int(rng.uniform(0.008, 0.025) * SR)
        i = int(rng.uniform(0, max(1, n - L)))
        g = rng.normal(0, 1, L)
        g = g - np.convolve(g, np.ones(6) / 6, mode="same")          # crude high-pass: brighter grains
        out[i:i + L] += g * np.hanning(L) * rng.uniform(0.3, 1.0)
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.3 * SR), (n - np.arange(n)) / (0.4 * SR)))
    return _norm(out * fade)


def fx_squeal(rng, dur=1.6):
    t = _t(dur)
    f = 2550 + 180 * (t / dur) + 14 * np.sin(2 * np.pi * 5.5 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = 10 ** ((-36 + 36 * np.clip(t / (0.75 * dur), 0, 1)) / 20) * np.minimum(1, (dur - t) / 0.08)
    return _norm((np.sin(ph) + 0.18 * np.sin(2 * ph)) * env)


def fx_chime(rng, dur=None):
    t = _t(1.6)
    out = np.zeros(len(t) + int(0.15 * SR))
    for f, t0, a in ((880.0, 0.0, 1.0), (1318.5, 0.12, 0.7)):
        s = (np.sin(2 * np.pi * f * t) + 0.15 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.2)) * np.exp(-t / 0.55)
        s *= np.minimum(1, t / 0.003)
        i = int(t0 * SR)
        out[i:i + len(t)] += a * s
    return _norm(out)


def fx_pop(rng, dur=None):
    t = _t(0.03)
    return _norm(np.sin(2 * np.pi * np.cumsum(700 - 300 * t / 0.03) / SR) * np.sin(np.pi * t / 0.03))


EFFECTS = {  # id: (synth, default peak dBFS in a -16 LUFS mix)
    "needle": (fx_needle, -12.0), "flip": (fx_needle, -12.0), "tick": (fx_tick, -20.0), "detent": (fx_detent, -24.0),
    "whoosh": (fx_whoosh, -16.0), "impact": (fx_impact, -11.0), "hiss": (fx_hiss, -27.0), "squeal": (fx_squeal, -22.0),
    "chime": (fx_chime, -16.0), "pop": (fx_pop, -24.0),
}


# ----------------------------------------------------------------------------- music (synthesized)
def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


PROGRESSIONS = [  # MIDI notes; the lowest note is the root (sub-bass one octave below)
    [[50, 57, 60, 64, 65], [46, 53, 57, 60, 62], [53, 57, 60, 64, 67], [48, 55, 60, 62, 67]],   # Dm9 Bbmaj9 Fmaj9 Csus2
    [[45, 52, 55, 60, 59], [41, 48, 53, 57, 64], [43, 50, 55, 59, 62], [40, 47, 55, 59, 62]],   # Am(add9) Fmaj7 G Em7
    [[53, 60, 64, 67, 69], [55, 62, 67, 69, 71], [50, 57, 60, 64, 65], [48, 55, 60, 64, 67]],   # F6 G6/9 Dm9 C
    [[50, 57, 62, 64, 65], [55, 62, 65, 69, 72], [46, 53, 58, 62, 65], [45, 52, 57, 60, 64]],   # Dm9 Gm9 Bb Am
]


_PAD_MEM = {}


def chord_segment(notes):
    """The pad of one chord, SEG + XF seconds, stereo: synthesized at 24 kHz (all partials < 3.5 kHz),
    upsampled to 48 kHz, cached in memory and on disk (float16, ~2 MB per chord, 16 chords at most)."""
    key = hashlib.sha256(json.dumps([MIX_VERSION, notes, SEG, XF]).encode()).hexdigest()[:16]
    if key in _PAD_MEM:
        return _PAD_MEM[key]
    p = os.path.join(MUSIC_CACHE, key + ".npy")
    if os.path.exists(p):
        out = np.load(p).astype(np.float32)
        _PAD_MEM[key] = out
        return out
    rng = np.random.default_rng(int(key[:8], 16))
    L, sr2 = SEG + XF, SR // 2
    t = np.arange(int(L * sr2)) / sr2
    out = np.zeros((len(t), 2))
    for m in notes:
        f = hz(m)
        for c in (0, 1):
            lfo = 1 + 0.18 * np.sin(2 * np.pi * rng.uniform(0.04, 0.11) * t + rng.uniform(0, 6.28))
            det = (1 if c else -1) * rng.uniform(1.5, 4.0) / 1200
            acc = np.zeros(len(t))
            for h in range(1, 6):
                if f * h > 3500:
                    break
                acc += 0.22 / h ** 1.7 * np.sin(2 * np.pi * f * h * (1 + det) * t + rng.uniform(0, 6.28))
            out[:, c] += lfo * acc
    root = min(notes)
    sub = hz(root - 12 if root > 45 else root)
    out += (0.16 * np.sin(2 * np.pi * sub * t))[:, None]
    env = np.minimum(1, t / 1.6) ** 1.5
    rel = t > SEG
    env[rel] *= 0.5 * (1 + np.cos(np.pi * (t[rel] - SEG) / XF))
    out *= env[:, None]
    n2 = int(L * SR)
    x2 = np.arange(n2) / SR
    up = np.stack([np.interp(x2, t, out[:, 0]), np.interp(x2, t, out[:, 1])], axis=1).astype(np.float32)
    os.makedirs(MUSIC_CACHE, exist_ok=True)
    np.save(p, up.astype(np.float16))
    _PAD_MEM[key] = up
    return up


def bells(notes, seed):
    """0-2 soft bell notes (upper chord tones, an octave up) inside one chord segment; cheap, varied by seed."""
    rng = np.random.default_rng(seed)
    out = np.zeros((int((SEG + XF) * SR), 2), dtype=np.float32)
    tt = _t(2.5)
    for _ in range(int(rng.integers(0, 3))):
        t0 = rng.uniform(0.8, SEG - 1.0)
        f = hz(int(rng.choice(notes[1:])) + 12)
        b = (np.sin(2 * np.pi * f * tt) + 0.2 * np.sin(2 * np.pi * 2.0 * f * tt) * np.exp(-tt / 0.3)) * np.exp(-tt / 0.9) * np.minimum(1, tt / 0.01)
        i = int(t0 * SR)
        j = min(len(out), i + len(tt))
        pan = rng.uniform(-0.6, 0.6)
        out[i:j, 0] += 0.05 * math.cos((pan + 1) * math.pi / 4) * b[:j - i]
        out[i:j, 1] += 0.05 * math.sin((pan + 1) * math.pi / 4) * b[:j - i]
    return out


def control_curve(values_per_scene, scenes, n_ctl, rate=100):
    g = np.zeros(n_ctl, dtype=np.float32)
    for v, sc in zip(values_per_scene, scenes):
        a, b = int(round(sc["start"] * rate)), int(round((sc["start"] + sc["duration"]) * rate))
        g[a:b] = v
    return g


def smooth_box(g, width):
    if width <= 1:
        return g
    c = np.cumsum(np.concatenate([[0], np.pad(g, (width // 2, width - width // 2 - 1), mode="edge")]))
    return ((c[width:] - c[:-width]) / width).astype(np.float32)


def duck_curve(narr, n_ctl, rate=100, thr_db=-45.0, att=0.06, rel=0.6):
    """Speech activity 0..1 at the control rate (one-pole attack/release on a voiced/unvoiced gate)."""
    hop = SR // rate
    m = (len(narr) // hop) * hop
    e = np.sqrt(np.mean(narr[:m].reshape(-1, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(e)
    ref = np.percentile(db[db > -70], 90) if np.any(db > -70) else -20
    gate = (db > max(thr_db, ref - 30)).astype(np.float32)
    act = np.zeros(n_ctl, dtype=np.float32)
    a_up, a_dn = 1 - math.exp(-1 / (att * rate)), 1 - math.exp(-1 / (rel * rate))
    v = 0.0
    for i in range(min(n_ctl, len(gate))):
        tgt = gate[i]
        v += (tgt - v) * (a_up if tgt > v else a_dn)
        act[i] = v
    return act


def level_of(sc):
    m = re.search(r"L[0-5]", str(sc.get("level") or ""))
    return m.group(0) if m else "L2"


# ----------------------------------------------------------------------------- main mix
def mix_key(tl):
    src = open(os.path.abspath(__file__), "rb").read()
    parts = [MIX_VERSION, hashlib.sha256(src).hexdigest(), tl["total_s"]]
    for sc in tl["scenes"]:
        parts.append([sc["id"], sc["start"], sc["duration"], sc["lead_in"], level_of(sc), sc.get("music"),
                      sc["audio"].get("key"), sc["audio"].get("wav"), sc.get("sfx"), sc.get("unit")])
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()[:20]


def run(tl, outdir, force=False):
    name = tl["name"]
    sd = os.path.join(outdir, "stems")
    os.makedirs(sd, exist_ok=True)
    outs = {k: os.path.join(sd, f"{name}_{k}.m4a") for k in ("full", "narration", "music", "effects", "nonarration")}
    rep_p = os.path.join(sd, f"{name}_mix.json")
    key = mix_key(tl)
    if not force and os.path.exists(rep_p) and all(os.path.exists(p) for p in outs.values()):
        old = json.load(open(rep_p))
        if old.get("key") == key:
            print(f"[mix] {name}: unchanged (key {key})")
            return old
    N = int(round(tl["total_s"] * SR))
    scenes = tl["scenes"]
    # narration
    narr = np.zeros(N, dtype=np.float32)
    for sc in scenes:
        w = sc["audio"].get("wav")
        if not w:
            raise SystemExit(f"[mix] {sc['id']}: no narration audio")
        x = read_wav(os.path.join(ROOT, w))
        a = int(round((sc["start"] + sc["lead_in"]) * SR))
        b = min(int(round((sc["start"] + sc["duration"]) * SR)), N)
        n = max(0, min(len(x), b - a))
        narr[a:a + n] += x[:n]
    I_n, _ = ff_measure(narr)
    if not np.isfinite(I_n):
        I_n = TARGET_I
    rate = 100
    n_ctl = int(math.ceil(tl["total_s"] * rate)) + 1
    act = duck_curve(narr, n_ctl, rate)
    # music
    gains = []
    for sc in scenes:
        m = sc.get("music")
        g = LEVEL_GAIN[level_of(sc)]
        if m is False:
            g = 0.0
        elif isinstance(m, dict) and "gain" in m:
            g = float(m["gain"])
        gains.append(g)
    gm = smooth_box(control_curve(gains, scenes, n_ctl, rate), 3 * rate)
    music = np.zeros((N, 2), dtype=np.float32)
    units = []
    for sc in scenes:
        if sc.get("unit") not in units:
            units.append(sc.get("unit"))
    nseg = int(math.ceil(tl["total_s"] / SEG))
    for k in range(nseg):
        t0 = k * SEG
        c0, c1 = int(t0 * rate), min(n_ctl, int((t0 + SEG + XF) * rate) + 1)
        if c1 <= c0 or float(np.max(gm[c0:c1])) <= 1e-4:
            continue
        sc = next((s for s in scenes if s["start"] <= t0 < s["start"] + s["duration"]), scenes[-1])
        ui = units.index(sc.get("unit")) if sc.get("unit") in units else 0
        prog = PROGRESSIONS[ui % len(PROGRESSIONS)]
        notes = prog[k % len(prog)]
        seg = chord_segment(notes) + bells(notes, seed=k)
        a = int(round(t0 * SR))
        n = min(len(seg), N - a)
        music[a:a + n] += seg[:n]
    ref = chord_segment(PROGRESSIONS[0][0])[:int(SEG * SR)]
    I_m, _ = ff_measure(ref)
    music_scale = 10 ** ((I_n - MUSIC_UNDER_VOICE_LU - I_m) / 20)
    duck_m = 10 ** (-MUSIC_DUCK_DB * act / 20) * gm * music_scale
    step = SR * 10
    for i in range(0, N, step):
        j = min(N, i + step)
        music[i:j] *= np.interp((np.arange(i, j) / SR) * rate, np.arange(n_ctl), duck_m).astype(np.float32)[:, None]
    # effects
    fx = np.zeros((N, 2), dtype=np.float32)
    cache, n_ev, unknown = {}, 0, set()
    off = 10 ** ((I_n - TARGET_I) / 20)       # effects levels are given for a -16 LUFS mix
    for sc in scenes:
        for ev in sc.get("sfx") or []:
            fid = ev.get("id")
            if fid not in EFFECTS:
                unknown.add(fid)
                continue
            synth, g0 = EFFECTS[fid]
            ck = (fid, ev.get("dur"))
            if ck not in cache:
                seed = int(hashlib.sha256(repr(ck).encode()).hexdigest()[:8], 16)
                cache[ck] = synth(np.random.default_rng(seed), **({"dur": float(ev["dur"])} if ev.get("dur") else {}))
            s = cache[ck] * (10 ** ((ev.get("gain_db", g0)) / 20) * off)
            pan = float(ev.get("pan", 0.0))
            a = int(round((sc["start"] + float(ev["t"])) * SR))
            if a >= N or a < 0:
                continue
            n = min(len(s), N - a)
            fx[a:a + n, 0] += s[:n] * math.cos((pan + 1) * math.pi / 4) * math.sqrt(2)
            fx[a:a + n, 1] += s[:n] * math.sin((pan + 1) * math.pi / 4) * math.sqrt(2)
            n_ev += 1
    duck_f = 10 ** (-FX_DUCK_DB * act / 20)
    for i in range(0, N, step):
        j = min(N, i + step)
        fx[i:j] *= np.interp((np.arange(i, j) / SR) * rate, np.arange(n_ctl), duck_f).astype(np.float32)[:, None]
    # master: one gain for all stems; the look-ahead limiter acts on the full mix only
    def full_chunks(g=1.0, env=None):
        for i in range(0, N, CHUNK):
            j = min(N, i + CHUNK)
            y = music[i:j] + fx[i:j]
            y += narr[i:j, None]
            if g != 1.0:
                y *= g
            if env is not None:
                y *= env_gain(env, i, j)[:, None]
            yield y
    I0 = ff_loudness(full_chunks(), 2)["I"]
    g = 10 ** ((TARGET_I - I0) / 20)
    ceiling, passes = LIMIT_DBFS, []
    for it in range(4):
        env = limiter_env(full_chunks(g), N, ceiling)
        I1 = ff_loudness(full_chunks(g, env), 2)["I"]
        passes.append({"gain_db": round(20 * math.log10(g), 2), "ceiling_dbfs": round(ceiling, 2), "limited_blocks": 0 if env is None
                       else int(np.sum(env < 0.999)), "I": I1})
        if abs(I1 - TARGET_I) > 0.15:
            g *= 10 ** ((TARGET_I - I1) / 20)
            continue
        ff_encode(full_chunks(g, env), 2, outs["full"])
        fin = ff_measure_file(outs["full"])
        passes[-1]["aac"] = fin
        if fin["TP"] is not None and fin["TP"] > CEIL_TP - 0.2:
            ceiling -= fin["TP"] - (CEIL_TP - 0.2) + 0.2
            continue
        break
    else:
        env = limiter_env(full_chunks(g), N, ceiling)
        ff_encode(full_chunks(g, env), 2, outs["full"])
        fin = ff_measure_file(outs["full"])
    if fin["TP"] is not None and fin["TP"] > CEIL_TP:
        raise SystemExit(f"[mix] true peak {fin['TP']} dBTP after AAC > {CEIL_TP}")
    gm_ = g                                    # the master gain actually used (stems: same gain, no limiter)

    def scaled(x):
        for c in chunks_of(x):
            yield c * gm_

    def nonarr():
        for i in range(0, N, CHUNK):
            j = min(N, i + CHUNK)
            yield (music[i:j] + fx[i:j]) * gm_
    jobs = [threading.Thread(target=ff_encode, args=a_) for a_ in (
        (scaled(narr), 1, outs["narration"]), (scaled(music), 2, outs["music"]), (scaled(fx), 2, outs["effects"]),
        (nonarr(), 2, outs["nonarration"]))]
    for th in jobs:
        th.start()
    for th in jobs:
        th.join()
    for k in ("narration", "music", "effects", "nonarration"):
        if not os.path.exists(outs[k]):
            raise SystemExit(f"[mix] stem {k} was not written")
    report_iter = passes
    rep = {"key": key, "name": name, "duration_s": tl["total_s"], "target": {"I": TARGET_I, "TP_max": CEIL_TP},
           "narration_premaster_I": round(I_n, 2), "music_under_voice_lu": MUSIC_UNDER_VOICE_LU,
           "music_duck_db": MUSIC_DUCK_DB, "fx_duck_db": FX_DUCK_DB, "effects_placed": n_ev,
           "unknown_effects": sorted(x for x in unknown if x), "master_gain_db": round(20 * math.log10(gm_), 2),
           "limiter_passes": report_iter, "full_mix_aac": fin,
           "files": {k: os.path.relpath(v, ROOT) for k, v in outs.items()}}
    json.dump(rep, open(rep_p, "w"), indent=1)
    print(f"[mix] {name}: full mix {fin['I']} LUFS, true peak {fin['TP']} dBTP, LRA {fin['LRA']} LU; "
          f"{n_ev} effects; stems in {os.path.relpath(sd, ROOT)}")
    if unknown:
        print(f"[mix] warning: unknown effect ids {sorted(x for x in unknown if x)}; known: {sorted(EFFECTS)}")
    return rep


def demo(path):
    rng = np.random.default_rng(1)
    parts = []
    for k, (synth, g0) in EFFECTS.items():
        if k == "flip":
            continue
        s = synth(rng) * 10 ** (g0 / 20)
        parts += [s, np.zeros(int(0.6 * SR))]
    x = np.concatenate(parts).astype(np.float32)
    ff_encode(chunks_of(x), 1, path)
    print("[mix] effects demo:", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("timeline", nargs="?")
    ap.add_argument("--outdir", default="out")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--demo")
    a = ap.parse_args()
    if a.demo:
        return demo(a.demo)
    tl = json.load(open(a.timeline))
    run(tl, os.path.join(ROOT, a.outdir) if not os.path.isabs(a.outdir) else a.outdir, a.force)


if __name__ == "__main__":
    main()
