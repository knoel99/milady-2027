#!/usr/bin/env python3
"""align.py: scene narration tracks and sentence timings, WITHOUT a forced aligner.

Each paragraph is one TTS file (audio/tts.py), so paragraph boundaries are exact. Inside a paragraph,
sentence boundaries are found by silence detection (as prototyped):
  1. pauses = runs >= 0.18 s whose 20-ms RMS stays below -40 dBFS (or 32 dB under the loudest frame);
  2. the script predicts where each sentence boundary should fall (character counts, measured in voiced
     time, i.e. with the detected pauses taken out, so that comma pauses do not skew the prediction);
  3. a dynamic programme picks, in order, the K-1 pauses that best match the predictions, preferring
     long pauses (sentence ends are longer than commas); too few pauses -> proportional fallback.
  3b. audio/align_hints.json (optional, written by `audio/qa.py hints` from a speech-recognition pass)
     gives, per paragraph cache key, the approximate start of each sentence after the first; a hinted
     boundary takes the pause whose END is nearest to the hint. The times stay silence-based and the
     text stays the script's (BRIEF D16); the build never needs the recognizer.
Then each paragraph is trimmed to its speech (+50 ms before, +120 ms after) and the scene track is
    para 1 | LONG_PAUSE_S + hold_after(1) | para 2 | ... | para N | hold_after(N)
written to audio/scenes/<scene>.wav (48 kHz mono) with audio/scenes/<scene>.align.json:
    {scene, key, duration, method, estimated, paragraphs:[{start,end,hold_after}], sentences:[{id,cue,text,start,end}]}
Times are relative to the start of the scene track; build.js adds lead_in, so a scene lasts
lead_in + duration + tail (holds included in duration) and a cue is lead_in + sentence start.
--allow-missing (for `make plan`): a paragraph with no audio yet gets an estimated length (146 raw wpm).
Language: a film with "lang": "fr" (tools/assemble_cut.py --lang fr) writes its tracks to audio/scenes_fr/
instead (same scene ids, French timing); English tracks and keys are untouched.
Usage: python3 -I audio/align.py script/_build/film_core.json [--manifest script/_build/core_tts.json] [--allow-missing]
"""
import argparse, hashlib, json, os, re, sys, wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tts import LONG_PAUSE_S, RAW_WPM, SR, nwords, plain  # noqa: E402

OUT = os.path.join(HERE, "scenes")          # English tracks; other languages: scenes_dir(lang)


def scenes_dir(lang="en"):
    """audio/scenes (English) or audio/scenes_<lang>: one narration track per scene and language."""
    return OUT if lang in (None, "", "en") else os.path.join(HERE, f"scenes_{lang}")
ALIGN_VERSION = 3
LEN_BONUS = 1.5                  # s of prediction error forgiven per s of pause length (sentence ends are long)
HINTS_FILE = os.path.join(HERE, "align_hints.json")
_HINTS = None


def hints_for(key, n):
    """Hinted sentence starts (seconds in the paragraph file, None = no hint) for a paragraph of n sentences."""
    global _HINTS
    if _HINTS is None:
        try:
            _HINTS = json.load(open(HINTS_FILE)).get("hints", {})
        except (FileNotFoundError, ValueError):
            _HINTS = {}
    h = _HINTS.get(key)
    return h if isinstance(h, list) and len(h) == n - 1 else None
PAD0, PAD1 = 0.05, 0.12          # kept before the first and after the last voiced frame of a paragraph
HOP, WIN = 0.010, 0.020


def read_wav(path):
    with wave.open(path) as w:
        n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if sw != 2 or sr != SR:
        raise SystemExit(f"{path}: expected 16-bit {SR} Hz, got {8 * sw}-bit {sr} Hz")
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    tmp = path + ".part"
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    os.replace(tmp, path)


def rms_db(x):
    hop, win = int(HOP * SR), int(WIN * SR)
    n = max(1, 1 + (len(x) - win) // hop)
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    idx = np.minimum(idx, len(x) - 1)
    e = np.sqrt(np.mean(x[idx] ** 2, axis=1) + 1e-12)
    return 20 * np.log10(e)


def silences(x, min_d=0.18, thr=None):
    """[(start, end)] of runs of low-energy frames lasting at least min_d seconds."""
    db = rms_db(x)
    if thr is None:
        thr = max(-40.0, float(np.max(db)) - 32.0)
    quiet = db < thr
    out, i, n = [], 0, len(quiet)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            a, b = i * HOP + WIN / 2, min(j * HOP + WIN / 2, len(x) / SR)
            if i == 0:
                a = 0.0
            if j == n:
                b = len(x) / SR
            if b - a >= min_d or i == 0 or j == n:
                out.append((a, b))
            i = j
        else:
            i += 1
    return out, thr


def split_sentences(sents, x, extra_weight=None, hints=None):
    """Sentence (start, end) inside one paragraph signal x. Returns (bounds, speech0, speech1, method)."""
    dur = len(x) / SR
    sil, thr = silences(x)
    edge, _ = silences(x, min_d=0.0, thr=thr)
    speech0 = edge[0][1] if edge and edge[0][0] <= 0.001 else 0.0
    speech1 = edge[-1][0] if edge and edge[-1][1] >= dur - 0.001 else dur
    if speech1 <= speech0:
        speech0, speech1 = 0.0, dur
    inner = [(a, b) for a, b in sil if a > speech0 + 0.05 and b < speech1 - 0.05 and b - a >= 0.18]
    weights = [len(plain(s["text"])) + (extra_weight[i] if extra_weight else 0) for i, s in enumerate(sents)]
    K, total = len(sents), sum(weights) or 1
    exp, c = [], 0
    for wgt in weights[:-1]:
        c += wgt
        exp.append(speech0 + (speech1 - speech0) * c / total)

    def voiced(t):                                   # speaking time before t (pauses taken out)
        return (t - speech0) - sum(min(b, t) - a for a, b in inner if a < t)
    vtot = voiced(speech1)
    vexp = [vtot * sum(weights[:k + 1]) / total for k in range(K - 1)]
    vpos = [voiced(a) for a, b in inner]
    hints = hints if hints and len(hints) == K - 1 else None
    method = "silence+dp" + ("+hints" if hints and any(h is not None for h in hints) else "")
    if K == 1:
        cuts = []
    elif len(inner) < K - 1:
        cuts, method = [(e, e) for e in exp], "proportional-fallback"
    else:
        INF, M = 1e18, len(inner)
        def cost(j, i):
            if hints and hints[j] is not None:
                return 4.0 * abs(inner[i][1] - hints[j])
            return abs(vpos[i] - vexp[j]) - LEN_BONUS * (inner[i][1] - inner[i][0])
        D = [[INF] * M for _ in range(K - 1)]
        P = [[-1] * M for _ in range(K - 1)]
        for i in range(M):
            D[0][i] = cost(0, i)
        for j in range(1, K - 1):
            best, arg = INF, -1
            for i in range(M):
                if i - 1 >= 0 and D[j - 1][i - 1] < best:
                    best, arg = D[j - 1][i - 1], i - 1
                if arg >= 0:
                    D[j][i] = best + cost(j, i)
                    P[j][i] = arg
        i = min(range(M), key=lambda i: D[K - 2][i])
        idx = [i]
        for j in range(K - 2, 0, -1):
            i = P[j][i]
            idx.append(i)
        cuts = [inner[i] for i in reversed(idx)]
    out, t = [], speech0
    for k in range(K):
        end = cuts[k][0] if k < len(cuts) else speech1
        out.append((t, end))
        if k < len(cuts):
            t = cuts[k][1]
    return out, speech0, speech1, method


def scene_key(sc, entries, lang="en"):
    d = {"v": ALIGN_VERSION, "pause": LONG_PAUSE_S, "pads": [PAD0, PAD1],
         "paras": [[e.get("key"), e.get("source"), e.get("wav"), p["hold_after"],
                    [(s["id"], s.get("cue"), s["text"]) for s in p["sentences"]],
                    hints_for(e.get("key"), len(p["sentences"]))]
                   for p, e in zip(sc["paragraphs"], entries)]}
    if lang not in (None, "", "en"):
        d["lang"] = lang
    blob = json.dumps(d, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:20]


def align_scene(sc, entries, allow_missing):
    out_sents, paras, pieces, t, methods, estimated, errs = [], [], [], 0.0, [], False, []
    n = len(sc["paragraphs"])
    for pi, (p, e) in enumerate(zip(sc["paragraphs"], entries)):
        sents = p["sentences"]
        if e.get("wav"):
            x = read_wav(os.path.join(ROOT, e["wav"]))
            bounds, s0, s1, m = split_sentences(sents, x, hints=hints_for(e.get("key"), len(sents)))
            a, b = max(0.0, s0 - PAD0), min(len(x) / SR, s1 + PAD1)
            clip = x[int(round(a * SR)):int(round(b * SR))]
            for s, (u, v) in zip(sents, bounds):
                out_sents.append({"id": s["id"], "cue": s.get("cue"), "text": s["text"],
                                  "start": round(t + u - a, 3), "end": round(t + v - a, 3)})
            if e.get("truth"):
                tr = {q["id"]: q for q in e["truth"]}
                errs += [abs((u - a) - (tr[s["id"]]["start"] - a)) for s, (u, v) in zip(sents, bounds)]
                errs += [abs((v - a) - (tr[s["id"]]["end"] - a)) for s, (u, v) in zip(sents, bounds)]
            methods.append(m)
        else:
            if not allow_missing:
                raise SystemExit(f"[align] {sc['id']} paragraph {pi + 1}: no audio (run tts.py first, or --allow-missing)")
            w = sum(nwords(s["text"]) for s in sents)
            d = max(0.6, w / RAW_WPM * 60)
            clip = None
            chars = [len(plain(s["text"])) for s in sents]
            c0 = 0
            for s, c in zip(sents, chars):
                u, v = c0 / sum(chars) * d, (c0 + c) / sum(chars) * d - 0.3
                out_sents.append({"id": s["id"], "cue": s.get("cue"), "text": s["text"],
                                  "start": round(t + u, 3), "end": round(t + max(u + 0.3, v), 3)})
                c0 += c
            estimated = True
            methods.append("estimated")
            clip_len = d
        L = len(clip) / SR if clip is not None else clip_len
        gap = p["hold_after"] + (LONG_PAUSE_S if pi < n - 1 else 0.0)
        paras.append({"start": round(t, 3), "end": round(t + L, 3), "hold_after": p["hold_after"], "gap_after": round(gap, 3)})
        pieces.append((clip, L, gap))
        t += L + gap
    res = {"scene": sc["id"], "duration": round(t, 4), "estimated": estimated,
           "method": "estimated" if estimated else (methods[0] if len(set(methods)) == 1 else "mixed:" + ",".join(methods)),
           "paragraphs": paras, "sentences": out_sents}
    if errs:
        res["error_vs_truth_ms"] = {"mean": round(1000 * sum(errs) / len(errs), 1), "max": round(1000 * max(errs), 1)}
    sig = None
    if not estimated:
        parts = []
        for clip, L, gap in pieces:
            parts += [clip, np.zeros(int(round(gap * SR)), dtype=np.float32)]
        sig = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
        res["duration"] = round(len(sig) / SR, 4)
    return res, sig, errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("--manifest")
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    film = json.load(open(a.film))
    name = film.get("name")
    man = json.load(open(a.manifest or os.path.join(ROOT, "script", "_build", f"{name}_tts.json")))
    lang = film.get("lang") or "en"
    out_dir = scenes_dir(lang)
    os.makedirs(out_dir, exist_ok=True)
    allerr, done, skipped, est = [], 0, 0, 0
    for sc in film["scenes"]:
        entries = man["scenes"].get(sc["id"])
        if entries is None or len(entries) != len(sc["paragraphs"]):
            raise SystemExit(f"[align] {sc['id']}: manifest does not match the script (rerun tts.py)")
        key = scene_key(sc, entries, lang)
        jp, wp = os.path.join(out_dir, sc["id"] + ".align.json"), os.path.join(out_dir, sc["id"] + ".wav")
        if not a.force and os.path.exists(jp):
            old = json.load(open(jp))
            if old.get("key") == key and (old.get("estimated") or os.path.exists(wp)):
                skipped += 1
                est += bool(old.get("estimated"))
                continue
        res, sig, errs = align_scene(sc, entries, a.allow_missing)
        res["key"] = key
        if lang != "en":
            res["lang"] = lang
        res["wav"] = None
        if sig is not None:
            write_wav(wp, sig)
            res["wav"] = os.path.relpath(wp, ROOT)
        else:
            est += 1
        res["sources"] = sorted({e.get("source") or "missing" for e in entries})
        json.dump(res, open(jp, "w"), indent=1, ensure_ascii=False)
        allerr += errs
        done += 1
    msg = f"[align] {name}: {done} scenes aligned, {skipped} unchanged, {est} estimated (no audio yet)"
    if allerr:
        msg += f"; placeholder truth check: mean {1000 * sum(allerr) / len(allerr):.1f} ms, max {1000 * max(allerr):.1f} ms"
    print(msg)


if __name__ == "__main__":
    main()
