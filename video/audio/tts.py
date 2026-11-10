#!/usr/bin/env python3
"""tts.py: narration synthesis, ONE Fish Audio request per paragraph, cached so that an unchanged
paragraph is never synthesised (nor billed) twice.

Request (validated settings, /home/user/videobook/BRAINSTORM.md "Parametrage valide", BRIEF D1, D2):
  POST https://api.fish.audio/v1/tts, headers  model: drama-3,  Authorization: Bearer proxy-injected
  (the network proxy injects the real key for api.fish.audio; FISH_API_KEY, if set, is used instead),
  body: temperature 0.1, format mp3, mp3_bitrate 192, sample_rate 44100, latency normal, language en,
        normalize true, condition_on_previous_chunks true, prosody {speed 1.0, normalize_loudness true},
        reference_id = the script's voice.reference_id (never hard-coded here), text.
Text of a request = "[calm, natural narrator voice] " + the paragraph's sentences, subtitle markup
  stripped, technical words pinned with phonemes from audio/lexicon.json. A paragraph is one request, so
  no request contains a paragraph break: the "[long pause]" between paragraphs is realised by align.py as
  LONG_PAUSE_S of silence (+ the paragraph's hold_after). No short/medium pauses, no <emphasis>/<stress>.
Cache: audio/cache/<key>.mp3 (as received), <key>.wav (decoded once to 48 kHz mono PCM: exact durations),
  <key>.json (text, voice, settings, words, duration). key = sha256 of (text, voice, model, settings); the
  settings hold the language, and a non-English key also hashes the language explicitly: key = (lang, text,
  voice, settings). English keys are unchanged, so the paid English cache stays valid.
Language (the film's "lang", set by tools/assemble_cut.py --lang): "en" (default) as above; "fr" = body
  "language": "fr" (every other validated setting unchanged, acting cue included), lexicon audio/lexicon_fr.json
  (respellings: Fish phoneme pins are English-only), and a live run refuses to bill a paragraph that still
  contains an untranslated (English) sentence (TTS_ALLOW_UNTRANSLATED=1 to force).

Modes (--mode):
  live         cached audio, else a request to the API (retries with exponential backoff)
  auto         cached audio, else a speech-like PLACEHOLDER (never calls the API: drafts, checks)
  placeholder  always the placeholder (tests; audio/cache/placeholder/)
  dry-run      no audio: prints every request (text) and word counts, cached or not, and the cost guard
Usage:
  python3 -I audio/tts.py script/_build/film_core.json [--mode live] [--only 04.1,04.2 (synthesise only these)] [--jobs 2]
                          [--max-new-words 15000] [--manifest script/_build/core_tts.json]
  python3 -I audio/tts.py --test "One short sentence." --voice-from script/ch00.json   (one live request)
  python3 -I audio/tts.py --test "Une phrase." --voice-from script/fr/ch00.json --lang fr
Writes the manifest script/_build/<name>_tts.json read by align.py.
"""
import argparse, hashlib, json, math, os, random, re, subprocess, sys, threading, time, urllib.error, urllib.request, wave
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache")
SR = 48000                                   # every narration file is decoded to 48 kHz mono
FISH_URL = "https://api.fish.audio/v1/tts"
MODEL = "drama-3"
FISH_BODY = {
    "temperature": 0.1, "format": "mp3", "mp3_bitrate": 192, "sample_rate": 44100, "latency": "normal",
    "language": "en", "normalize": True, "condition_on_previous_chunks": True,
    "prosody": {"speed": 1.0, "normalize_loudness": True},
}
ACTING_CUE = "[calm, natural narrator voice]"
LANGS = ("en", "fr")
LONG_PAUSE_S = 0.9                           # silence standing for [long pause] between paragraphs (align.py)
RAW_WPM = 146.0                              # measured raw pace of the Ethan voice (BRIEF D21)
MARK = re.compile(r"\{(u|b|param|model|metric)\}(.*?)\{/\}")
RETRY_CODES = {408, 409, 425, 429, 500, 502, 503, 504}


def plain(text):
    return MARK.sub(r"\2", text)


def nwords(text):
    return len(re.findall(r"[\w'’-]+", plain(text)))


# ----------------------------------------------------------------------------- text
def lexicon_path(lang="en"):
    return os.path.join(HERE, "lexicon.json" if lang == "en" else f"lexicon_{lang}.json")


def load_lexicon(lang="en"):
    """{word: (kind, value)}. kind "phonemes" (ARPAbet pin) or "say" (respelling); an entry {"keep": true} is
    documentation only (a word deliberately left as written, e.g. an English ML term in the French narration)."""
    p = lexicon_path(lang)
    if lang != "en" and not os.path.exists(p):
        print(f"[tts] warning: no {os.path.relpath(p, ROOT)}: no pronunciation pins for '{lang}'", file=sys.stderr)
        return {}
    d = json.load(open(p))
    out = {}
    for word, v in d["entries"].items():
        if isinstance(v, str):
            out[word] = ("phonemes", v)
        elif v.get("keep"):
            continue
        elif v.get("phonemes"):
            out[word] = ("phonemes", v["phonemes"])
        elif v.get("say"):
            out[word] = ("say", v["say"])
    return out


def pin(text, lex):
    """Replace lexicon words (case-sensitive, whole words, longest first) by phoneme pins or respellings."""
    keys = sorted(lex, key=len, reverse=True)
    if not keys:
        return text
    rx = re.compile(r"(?<![\w>|])(" + "|".join(re.escape(k) for k in keys) + r")(?![\w<|])")

    def rep(m):
        kind, v = lex[m.group(1)]
        return f"<|phoneme_start|>{v}<|phoneme_end|>" if kind == "phonemes" else v
    return rx.sub(rep, text)


def spoken_text(paragraph, lex):
    s = " ".join(plain(x["text"]).strip() for x in paragraph["sentences"])
    s = re.sub(r"\s+", " ", s).strip()
    return ACTING_CUE + " " + pin(s, lex)


def request_body(text, voice_id, lang="en"):
    """The validated body; only "language" follows the narration language (BRIEF section 9)."""
    return dict(FISH_BODY, text=text, reference_id=voice_id, language=lang)


def cache_key(body, lang="en"):
    """(lang, text, voice, settings). English keys are exactly the historical ones (paid cache)."""
    d = {"v": 1, "url": FISH_URL, "model": MODEL, "body": body}
    if lang != "en":
        d["lang"] = lang
    blob = json.dumps(d, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()[:24]


# ----------------------------------------------------------------------------- audio helpers
def write_wav(path, x):
    x = np.clip(np.asarray(x, dtype=np.float64), -1, 1)
    tmp = path + ".part"
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    os.replace(tmp, path)


def wav_duration(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def decode(mp3, wav):
    tmp = wav + ".part.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", tmp], check=True)
    os.replace(tmp, wav)


# ----------------------------------------------------------------------------- placeholder voice
def placeholder(paragraph, rng):
    """Speech-like bursts (harmonic buzz) at about the measured raw pace, comma pauses ~0.2 s, sentence
    pauses ~0.45 s, -55 dBFS floor. Returns (samples, truth) with the true sentence times (align tests)."""
    out, truth, t = [], [], 0.0

    def add(x):
        nonlocal t
        out.append(x)
        t += len(x) / SR

    def silence(d):
        add(rng.normal(0, 10 ** (-55 / 20), int(d * SR)))

    silence(0.15)
    for si, sent in enumerate(paragraph["sentences"]):
        if si:
            silence(rng.uniform(0.38, 0.55))
        ws = plain(sent["text"]).split()
        start = t
        for wi, w in enumerate(ws):
            n = len(re.sub(r"\W", "", w)) or 1
            d = 0.075 + 0.05 * n
            k = np.arange(int(d * SR)) / SR
            f0 = 105 + 25 * math.sin(2 * math.pi * 0.7 * t) + rng.uniform(-8, 8)
            env = np.sin(np.pi * k / d) ** 0.6 * (0.6 + 0.4 * np.sin(2 * np.pi * 4.5 * k) ** 2)
            v = sum((0.5 / h) * np.sin(2 * np.pi * f0 * h * k) for h in range(1, 10))
            v = v + rng.normal(0, 0.04, len(k))
            add(0.30 * env * v)
            if wi < len(ws) - 1:
                silence(0.2 if re.search(r"[,;:]$", w) else rng.uniform(0.03, 0.07))
        truth.append({"id": sent["id"], "start": round(start, 3), "end": round(t, 3)})
    silence(0.3)
    return np.concatenate(out), truth


# ----------------------------------------------------------------------------- API
class TTSError(Exception):
    pass


class TTSRefused(TTSError):
    """The API refused the account (bad key, no credit, quota): stop the whole run, never loop."""


FATAL_CODES = {401, 402, 403}
ABORT = threading.Event()


def call_fish(body, attempts=6):
    key = os.environ.get("FISH_API_KEY") or "proxy-injected"
    data = json.dumps(body, ensure_ascii=False).encode()
    last = None
    for a in range(attempts):
        req = urllib.request.Request(FISH_URL, data=data, method="POST", headers={
            "authorization": "Bearer " + key, "model": MODEL, "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                audio = r.read()
            if len(audio) < 1000 or not (audio[:3] == b"ID3" or (audio[0] == 0xFF and (audio[1] & 0xE0) == 0xE0)):
                raise TTSError(f"response is not mp3 audio ({len(audio)} bytes): {audio[:200]!r}")
            return audio
        except urllib.error.HTTPError as e:
            msg = e.read()[:400].decode("utf8", "replace")
            if e.code in FATAL_CODES or re.search(r"quota|insufficient|balance|credit", msg, re.I):
                ABORT.set()
                raise TTSRefused(f"HTTP {e.code}: {msg}")
            if e.code not in RETRY_CODES:
                raise TTSError(f"HTTP {e.code}: {msg}")
            last = f"HTTP {e.code}: {msg}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = repr(e)
        wait = min(120, 2 ** (a + 1)) + random.uniform(0, 1.5)
        print(f"[tts] retry {a + 1}/{attempts - 1} in {wait:.0f} s ({last})", file=sys.stderr)
        time.sleep(wait)
    raise TTSError(f"giving up after {attempts} attempts: {last}")


def synth_live(key, body, meta):
    mp3, wav = os.path.join(CACHE, key + ".mp3"), os.path.join(CACHE, key + ".wav")
    t0 = time.time()
    audio = call_fish(body)
    with open(mp3 + ".part", "wb") as f:
        f.write(audio)
    os.replace(mp3 + ".part", mp3)
    decode(mp3, wav)
    dur = wav_duration(wav)
    meta = dict(meta, duration=round(dur, 4), latency_s=round(time.time() - t0, 1),
                created=time.strftime("%Y-%m-%dT%H:%M:%S"), provider="fish", request=body)
    json.dump(meta, open(os.path.join(CACHE, key + ".json"), "w"), indent=1, ensure_ascii=False)
    return dur


def cached(key):
    w = os.path.join(CACHE, key + ".wav")
    if os.path.exists(w) and os.path.exists(os.path.join(CACHE, key + ".json")):
        return w
    mp3 = os.path.join(CACHE, key + ".mp3")
    if os.path.exists(mp3) and os.path.exists(os.path.join(CACHE, key + ".json")):
        decode(mp3, w)                         # the wav was deleted: decode again, never re-request
        return w
    return None


# ----------------------------------------------------------------------------- main
def plan_requests(film, lex, voice_id, only=None, lang="en"):
    reqs = []
    for sc in film["scenes"]:
        if only and sc["id"] not in only:
            continue
        for pi, p in enumerate(sc["paragraphs"]):
            text = spoken_text(p, lex)
            body = request_body(text, voice_id, lang)
            reqs.append({"scene": sc["id"], "para": pi, "key": cache_key(body, lang), "body": body,
                         "words": sum(nwords(x["text"]) for x in p["sentences"]), "paragraph": p,
                         "untranslated": [x["id"] for x in p["sentences"] if x.get("untranslated")]})
    return reqs


def run_test(sentence, voice_from, lang="en"):
    unit = json.load(open(voice_from))
    # an overlay script/fr/<unit>.json carries "voice"; an English script may carry "voice_fr"
    voice_id = ((unit.get(f"voice_{lang}") if lang != "en" else None) or unit.get("voice") or {}).get("reference_id")
    if not voice_id or not re.fullmatch(r"[0-9a-f]{32}", voice_id):
        sys.exit(f"no valid voice.reference_id in {voice_from}")
    os.makedirs(CACHE, exist_ok=True)
    lex = load_lexicon(lang)
    p = {"sentences": [{"id": "test.s1", "text": sentence}]}
    body = request_body(spoken_text(p, lex), voice_id, lang)
    key = cache_key(body, lang)
    print("[tts] test request:", json.dumps({"url": FISH_URL, "headers": {"model": MODEL, "authorization": "Bearer ***"},
                                               "body": body}, ensure_ascii=False))
    src = "cache"
    if not cached(key):
        synth_live(key, body, {"text": body["text"], "voice": voice_id, "lang": lang, "words": nwords(sentence), "test": True})
        src = "live"
    dur = wav_duration(os.path.join(CACHE, key + ".wav"))
    w = nwords(sentence)
    print(json.dumps({"ok": True, "source": src, "key": key, "words": w, "duration_s": round(dur, 2),
                      "raw_wpm": round(w / dur * 60, 1), "wav": os.path.relpath(os.path.join(CACHE, key + ".wav"), ROOT)}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film", nargs="?")
    ap.add_argument("--mode", choices=["live", "auto", "placeholder", "dry-run"], default="auto")
    ap.add_argument("--only", help="comma-separated scene ids")
    ap.add_argument("--jobs", type=int, default=2, help="concurrent API requests")
    ap.add_argument("--max-new-words", type=int, default=int(os.environ.get("TTS_MAX_NEW_WORDS", 15000)),
                    help="refuse a live run that would synthesise more new words than this (cost guard)")
    ap.add_argument("--manifest")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--test", help="one live request for this sentence (setup check)")
    ap.add_argument("--voice-from", help="with --test: the script file whose voice.reference_id is used")
    ap.add_argument("--lang", choices=LANGS, help="with --test: the narration language (else the film's 'lang')")
    a = ap.parse_args()
    if a.test:
        return run_test(a.test, a.voice_from or sys.exit("--voice-from script/<unit>.json is required"), a.lang or "en")
    film = json.load(open(a.film))
    lang = film.get("lang") or "en"
    if lang not in LANGS:
        sys.exit(f"[tts] unknown narration language {lang!r} (one of {LANGS})")
    name = film.get("name") or os.path.basename(a.film).replace("film_", "").replace(".json", "")
    manifest = a.manifest or os.path.join(ROOT, "script", "_build", f"{name}_tts.json")
    voice_id = (film.get("voice") or {}).get("reference_id")
    if a.mode == "live" and (not voice_id or not re.fullmatch(r"[0-9a-f]{32}", str(voice_id))):
        sys.exit(f"[tts] live mode needs a voice.reference_id (32 hex characters) in the script, got {voice_id!r}")
    only = set(a.only.split(",")) if a.only else None
    lex = load_lexicon(lang)
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(os.path.join(CACHE, "placeholder"), exist_ok=True)
    reqs = plan_requests(film, lex, voice_id or "NO_VOICE", None, lang)
    for r in reqs:
        r["cached"] = cached(r["key"]) is not None
    new = [r for r in reqs if not r["cached"] and (not only or r["scene"] in only)]
    nw = sum(r["words"] for r in new)
    summary = {"name": name, "mode": a.mode, "voice": voice_id, **({"lang": lang} if lang != "en" else {}),
               "paragraphs": len(reqs),
               "words": sum(r["words"] for r in reqs), "cached_paragraphs": sum(r["cached"] for r in reqs),
               "new_paragraphs": len(new), "new_words": nw, "new_audio_min_est": round(nw / RAW_WPM, 1)}
    if a.mode == "dry-run":
        os.makedirs(os.path.join(HERE, "requests"), exist_ok=True)
        with open(os.path.join(HERE, "requests", f"{name}.jsonl"), "w") as f:
            for r in reqs:
                f.write(json.dumps({"scene": r["scene"], "para": r["para"], "key": r["key"], "cached": r["cached"],
                                    "words": r["words"], "url": FISH_URL, "headers": {"model": MODEL},
                                    "body": r["body"]}, ensure_ascii=False) + "\n")
                if not a.quiet:
                    print(f"{r['scene']} p{r['para'] + 1} {r['words']:3d} words {'cached' if r['cached'] else 'NEW   '}"
                          f"{' UNTRANSLATED' if r['untranslated'] else ''} | {r['body']['text']}")
    untr = [r for r in new if r["untranslated"]]
    if lang != "en":
        summary["untranslated_paragraphs"] = sum(1 for r in reqs if r["untranslated"])
    if a.mode == "live" and untr and os.environ.get("TTS_ALLOW_UNTRANSLATED") != "1":
        print(json.dumps(summary))
        sys.exit(f"[tts] {len(untr)} new {lang} paragraphs still contain English (untranslated) sentences, e.g. "
                 + ", ".join(i for r in untr[:3] for i in r["untranslated"][:2])
                 + f": translate them in script/{lang}/<unit>.json first (TTS_ALLOW_UNTRANSLATED=1 to bill them anyway)")
    if a.mode == "live" and nw > a.max_new_words:
        print(json.dumps(summary))
        sys.exit(f"[tts] {nw} new words to synthesise > --max-new-words {a.max_new_words}: run --mode dry-run to "
                 "review, then raise the limit (TTS_MAX_NEW_WORDS=...) on purpose")
    if a.mode == "live" and new:
        todo = {}
        for r in new:                     # identical paragraphs share one request
            todo.setdefault(r["key"], r)
        print(f"[tts] {len(todo)} new requests ({nw} words), {a.jobs} at a time")
        fails = []

        def job(r):
            if ABORT.is_set():            # the API refused the account: send nothing more
                fails.append((r["scene"], r["para"], "skipped after refusal"))
                return
            try:
                d = synth_live(r["key"], r["body"], {"text": r["body"]["text"], "voice": voice_id, "words": r["words"],
                                                     "scene": r["scene"], "para": r["para"],
                                                     **({"lang": lang} if lang != "en" else {})})
                print(f"[tts] {r['scene']} p{r['para'] + 1}: {d:.2f} s, {r['words'] / d * 60:.0f} raw wpm")
            except Exception as e:      # keep going: the other paragraphs are paid for and cached
                fails.append((r["scene"], r["para"], str(e)))
                print(f"[tts] FAILED {r['scene']} p{r['para'] + 1}: {e}", file=sys.stderr)
        with ThreadPoolExecutor(max(1, a.jobs)) as ex:
            list(ex.map(job, todo.values()))
        if ABORT.is_set():
            sys.exit(f"[tts] the API refused the request (401/402/403 or quota): run stopped, "
                     f"{len(todo) - len(fails)} paragraphs synthesised and cached, {len(fails)} not done")
        if fails:
            sys.exit(f"[tts] {len(fails)} requests failed; rerun to retry them (successful ones are cached)")
    # manifest
    scenes = {}
    for r in reqs:
        e = {"para": r["para"], "key": r["key"], "words": r["words"], "source": None, "wav": None, "truth": None}
        w = None if a.mode == "placeholder" else cached(r["key"])
        if w:
            e["source"], e["wav"] = "fish", os.path.relpath(w, ROOT)
        elif a.mode in ("auto", "placeholder"):
            pw = os.path.join(CACHE, "placeholder", r["key"] + ".wav")
            pm = pw[:-4] + ".json"
            if not (os.path.exists(pw) and os.path.exists(pm)):
                rng = np.random.default_rng(int(r["key"][:8], 16))
                x, truth = placeholder(r["paragraph"], rng)
                write_wav(pw, x)
                json.dump({"truth": truth, "placeholder": True}, open(pm, "w"))
            e["source"], e["wav"], e["truth"] = "placeholder", os.path.relpath(pw, ROOT), json.load(open(pm))["truth"]
        if e["wav"]:
            e["duration"] = round(wav_duration(os.path.join(ROOT, e["wav"])), 4)
        scenes.setdefault(r["scene"], []).append(e)
    sources = [e["source"] for v in scenes.values() for e in v]
    summary.update(fish=sources.count("fish"), placeholder=sources.count("placeholder"), missing=sources.count(None))
    os.makedirs(os.path.dirname(manifest), exist_ok=True)
    json.dump({"name": name, "voice": voice_id, "mode": a.mode, **({"lang": lang} if lang != "en" else {}),
               "long_pause_s": LONG_PAUSE_S, "summary": summary, "scenes": scenes}, open(manifest, "w"), indent=1)
    print("[tts]", json.dumps(summary))


if __name__ == "__main__":
    main()
