#!/usr/bin/env python3
"""tts.py: narration step. One TTS request per *spoken sequence* (here: one scene's narration),
never one request per sentence (prosody would reset) and never the whole film at once (a fix
would force a full re-synthesis).

Modes
  --dry-run (default when FISH_API_KEY is unset): writes the exact Fish Audio requests to
            audio/requests/<scene>.json and synthesises a speech-like PLACEHOLDER (numpy) so the
            rest of the pipeline (durations, alignment, subtitles, loudness) can be tested.
  --live    : POST https://api.fish.audio/v1/tts with the validated drama-3 settings and save
            audio/chunks/<scene>.mp3, then decode to 44.1 kHz WAV (exact sample count).

Text preparation (Videobook brainstorm, validated 2026-11-01):
  * one sober acting cue at the start of the sequence: [calm, natural narrator voice]
  * [long pause] only between main paragraphs, no short/medium pauses, no <emphasis>/<stress>
  * <slow> only for a title; technical words pinned with phonemes from lexicon.json
  * key-term markup {u}...{/} used for subtitle colours is stripped from the spoken text
Usage: python3 -I audio/tts.py script/demo_script.json [--live] [--only scene_id]
"""
import hashlib, json, math, os, re, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SR = 44100

FISH_URL = "https://api.fish.audio/v1/tts"
FISH_HEADERS = {"model": "drama-3", "content-type": "application/json"}   # + authorization: Bearer $FISH_API_KEY
FISH_BODY = {
    "temperature": 0.1, "format": "mp3", "mp3_bitrate": 192, "sample_rate": 44100, "latency": "normal",
    "language": "en", "normalize": True, "condition_on_previous_chunks": True,
    "prosody": {"speed": 1.0, "normalize_loudness": True},
}


def load_lexicon():
    with open(os.path.join(HERE, "lexicon.json")) as f:
        return json.load(f)["entries"]


def spoken_text(scene, lex):
    """Join a scene's paragraphs into one spoken sequence with Fish control tags."""
    paras = []
    for para in scene["paragraphs"]:
        s = " ".join(re.sub(r"\{(u|b|param|model|metric)\}(.*?)\{/\}", r"\2", x["text"]) for x in para)
        paras.append(s)
    text = " [long pause] ".join(paras)
    for word, ph in sorted(lex.items(), key=lambda kv: -len(kv[0])):          # phoneme pinning
        text = re.sub(r"(?<![\w>])" + re.escape(word) + r"(?![\w<])",
                      "<|phoneme_start|>" + ph + "<|phoneme_end|>", text)
    return "[calm, natural narrator voice] " + text


# ---------------- placeholder voice (no API key): speech-like bursts with realistic pauses ----------------
def placeholder(scene, rng):
    """Returns (samples, truth) with word bursts ~150 wpm, comma pauses ~0.2 s, sentence pauses ~0.45 s,
    paragraph pauses ~1.1 s ([long pause]) and a -55 dBFS room-noise floor."""
    out, truth, t = [], [], 0.0

    def add(x):
        nonlocal t
        out.append(x); t += len(x) / SR

    def silence(d):
        add(rng.normal(0, 10 ** (-55 / 20), int(d * SR)))

    silence(0.12)
    for pi, para in enumerate(scene["paragraphs"]):
        if pi:
            silence(1.1)
        for si, sent in enumerate(para):
            if si:   # HARD=1: sentence pauses as short as commas, to stress the aligner
                silence(rng.uniform(0.22, 0.40) if os.environ.get("PLACEHOLDER_HARD") else rng.uniform(0.38, 0.55))
            words = re.sub(r"\{(u|b|param|model|metric)\}(.*?)\{/\}", r"\2", sent["text"]).split()
            start = t
            for wi, w in enumerate(words):
                n = len(re.sub(r"\W", "", w)) or 1
                d = 0.075 + 0.052 * n
                k = np.arange(int(d * SR)) / SR
                f0 = 105 + 25 * math.sin(2 * math.pi * 0.7 * t) + rng.uniform(-8, 8)
                env = np.sin(np.pi * k / d) ** 0.6 * (0.6 + 0.4 * np.sin(2 * np.pi * 4.5 * k) ** 2)
                v = sum((0.5 / h) * np.sin(2 * np.pi * f0 * h * k) for h in range(1, 12))
                v += rng.normal(0, 0.04, len(k))
                add(0.30 * env * v)
                if wi < len(words) - 1:
                    comma = w.endswith(",") or w.endswith(":") or w.endswith(";")
                    hard = os.environ.get("PLACEHOLDER_HARD")
                    silence((rng.uniform(0.2, 0.32) if hard else 0.2) if comma else rng.uniform(0.03, 0.07))
            truth.append({"id": sent["id"], "start": round(start, 3), "end": round(t, 3)})
    silence(0.25)
    return np.concatenate(out), truth


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def main():
    args = sys.argv[1:]
    script = json.load(open(args[0]))
    live = "--live" in args
    only = args[args.index("--only") + 1] if "--only" in args else None
    if live and not os.environ.get("FISH_API_KEY"):
        sys.exit("FISH_API_KEY is not set: run without --live for the dry run")
    lex = load_lexicon()
    os.makedirs(os.path.join(HERE, "requests"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "chunks"), exist_ok=True)
    voice = script["voice"]["reference_id"]
    for sc in script["scenes"]:
        if only and sc["id"] != only:
            continue
        body = dict(FISH_BODY, text=spoken_text(sc, lex), reference_id=voice)
        key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        req = {"url": FISH_URL, "headers": FISH_HEADERS, "body": body, "cache_key": key}
        json.dump(req, open(os.path.join(HERE, "requests", sc["id"] + ".json"), "w"), indent=2, ensure_ascii=False)
        wav = os.path.join(HERE, "chunks", sc["id"] + ".wav")
        meta_p = os.path.join(HERE, "chunks", sc["id"] + ".meta.json")
        if os.path.exists(meta_p) and json.load(open(meta_p)).get("cache_key") == key and os.path.exists(wav):
            continue                                                  # unchanged text: no new TTS call
        if live:
            import urllib.request
            r = urllib.request.Request(FISH_URL, data=json.dumps(body).encode(), method="POST",
                                       headers=dict(FISH_HEADERS, authorization="Bearer " + os.environ["FISH_API_KEY"]))
            mp3 = wav[:-4] + ".mp3"
            with urllib.request.urlopen(r, timeout=600) as resp, open(mp3, "wb") as f:
                f.write(resp.read())
            # decode once to PCM: exact durations (mp3 headers are approximate; encoder delay ~ 1105 samples)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), wav], check=True)
            truth = None
        else:
            rng = np.random.default_rng(int(key[:8], 16))
            x, truth = placeholder(sc, rng)
            write_wav(wav, x)
        with wave.open(wav) as w:
            dur = w.getnframes() / w.getframerate()
        json.dump({"cache_key": key, "duration": round(dur, 4), "placeholder": not live, "truth": truth},
                  open(meta_p, "w"), indent=2)
        print(f"{sc['id']}: {dur:.2f} s ({'live' if live else 'placeholder'})")


if __name__ == "__main__":
    main()
