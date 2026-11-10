#!/usr/bin/env python3
"""qa.py: listening QA of the synthesized narration, without listening: speech recognition of every
paragraph compared to the script, pronunciation of the lexicon terms, pace, loudness, silences, and the
accuracy of the sentence cues found by align.py.

  python3 -I audio/qa.py transcribe [--model small.en] [--threads 4]   ASR of every cached paragraph
                                                                        -> audio/cache/asr/<key>.json
  python3 -I audio/qa.py report [--out audio/qa_report.json]           comparison, measures, flags
  python3 -I audio/qa.py hints                                         audio/align_hints.json for align.py

Paragraphs = the union of script/_build/film_core.json and film_extended.json (run assemble_cut.py first),
each paragraph identified by its TTS cache key (audio/tts.py). The recognizer (faster-whisper, CPU, int8) is
an optional QA dependency, never used by the build. Subtitles never come from it (BRIEF D16).

Word error rate: both texts lower-cased, markup and punctuation removed, hyphens split; numbers written in
digits by the recognizer are expanded to the spoken form that best matches the script ("0.86" -> "zero point
eight six", "2012" -> "twenty twelve" or "two thousand twelve"); runs of single letters are joined when the
script has the acronym ("v k s" -> "vks"); lexicon terms are accepted under the spellings listed in TERM_OK.
A lexicon term the recognizer wrote otherwise is listed with what it heard (a hint to listen, not a verdict:
Gissinger is said in French on purpose).
"""
import argparse, glob, json, os, re, subprocess, sys, wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tts  # noqa: E402
from align import silences, split_sentences, read_wav, hints_for  # noqa: E402

ASR = os.path.join(tts.CACHE, "asr")
SR = tts.SR

# accepted recognizer spellings of the lexicon terms (normalized: lower case, no punctuation, single letters joined)
TERM_OK = {
    "mhd": ["mhd"], "abc": ["abc"], "vks": ["vks"], "phd": ["phd"],
    "dresdyn": ["dresdyn", "dresdine", "dresdyne", "dress dine", "dress dyne", "dressdine", "dresdin"],
    "sfemans": ["sfemans", "s femans", "sfeman", "s fem ans", "ess femans", "s femans"],
    "milady": ["milady", "my lady", "mylady", "m'lady", "milady's"],
    "gissinger": ["gissinger", "gisanger", "jisanje", "gisange", "gissange"],
    "reynolds": ["reynolds", "reynold's", "reynold"],
    "rm": ["rm", "r m", "are m", "our m"], "pm": ["pm", "p m"],
    "karman": ["karman", "kármán", "carmen", "carman"],
    "kac": ["kac", "katz", "kats", "kotz"],
    "latu": ["latu", "latoo", "la tu", "lattu"],
    "genci": ["genci", "jean see", "jensi", "gensi", "jansi"],
    "jean zay": ["jean zay", "jean-zay", "jeanzay", "john zay", "jean zey"],
    "rice": ["rice"],
    "zeldovich": ["zeldovich", "zel'dovich"],
    "lyapunov": ["lyapunov", "lyapunoff"],
    "navier": ["navier"], "saclay": ["saclay"], "cerea": ["cerea"], "enpc": ["enpc"], "lisn": ["lisn"],
    "alfven": ["alfven", "alfvén"], "brunhes": ["brunhes", "bruns", "brune"], "matuyama": ["matuyama", "matsuyama"],
    "slurm": ["slurm"], "torchda": ["torchda", "torch da"], "ohmic": ["ohmic"],
}
# spelling variants and homophones the recognizer cannot tell apart (both sides mapped to the first form)
EQUIV = {"disk": "disc", "disks": "discs", "breaks": "brakes", "break": "brake", "favorite": "favourite",
         "liters": "litres", "liter": "litre", "spiraling": "spiralling", "neighboring": "neighbouring",
         "pore": "poor", "weight": "wait", "right": "write", "color": "colour", "colors": "colours",
         "behavior": "behaviour", "center": "centre", "modeling": "modelling", "labeled": "labelled",
         "analyze": "analyse", "toward": "towards", "okay": "ok", "gray": "grey", "meter": "metre",
         "meters": "metres", "per cent": "percent", "fiber": "fibre", "traveling": "travelling",
         "programme": "program", "catalog": "catalogue", "whirlpool's": "whirlpools",
         "%": "percent", "plane": "plain", "planes": "plains", "peek": "peak", "peeks": "peaks", "favor": "favour"}
READ_ALOUD = ["calm natural narrator", "narrator voice", "long pause", "phoneme", "natural narrator"]
STOP = set("a an the of to and or in on at is are be it its this that as by for with from we so but not".split())

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
ORD = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth", "nine": "ninth",
       "twelve": "twelfth"}


def card(n, uk=False):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    for v, w in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand"), (100, "hundred")):
        if n >= v:
            hi, lo = divmod(n, v)
            s = card(hi, uk) + " " + w
            if lo:
                s += (" and " if uk and lo < 100 else " ") + card(lo, uk)
            return s
    return str(n)


def number_forms(tok):
    """Spoken candidates for a digit token of the recognizer ('17', '0.86', '2012', '17th', '45%', '1,000')."""
    m = re.fullmatch(r"(\d[\d,]*)(?:\.(\d+))?(st|nd|rd|th|s)?(%)?", tok)
    if not m:
        return [re.sub(r"\d", lambda d: " " + ONES[int(d.group())] + " ", tok).split()]
    ip, frac, suf, pct = m.group(1).replace(",", ""), m.group(2), m.group(3), m.group(4)
    n = int(ip)
    outs = [card(n), card(n, uk=True)]
    if re.match(r"one (hundred|thousand|million|billion)", outs[0]):
        outs.append("a" + outs[0][3:])
    if 1100 <= n <= 2099 and not frac:
        hi, lo = divmod(n, 100)
        if lo == 0:
            outs.append(card(hi) + " hundred")
        else:
            outs.append(card(hi) + " " + (("oh " + ONES[lo]) if lo < 10 else card(lo)))
    if len(ip) > 1 and not frac:
        outs.append(" ".join(ONES[int(c)] for c in ip))
    if frac:
        tail = " point " + " ".join(ONES[int(c)] for c in frac)
        outs = [o + tail for o in outs] + (["point " + " ".join(ONES[int(c)] for c in frac)] if n == 0 else [])
    if suf in ("st", "nd", "rd", "th"):
        new = []
        for o in outs:
            w = o.split()
            last = w[-1]
            w[-1] = ORD.get(last, (last[:-1] + "ieth") if last.endswith("y") else last + "th")
            new.append(" ".join(w))
        outs = new
    elif suf == "s":
        outs = [o + "s" if not o.endswith("y") else o[:-1] + "ies" for o in outs]
    if pct:
        outs = [o + " percent" for o in outs]
    seen, res = set(), []
    for o in outs:
        if o not in seen:
            seen.add(o)
            res.append(o.split())
    return res


def tokens(text):
    t = tts.plain(text).replace("’", "'").replace("‘", "'")
    t = t.replace("²", " squared").replace("³", " cubed")
    t = re.sub(r"[‐‑‒–—―/-]", " ", t)
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)
    t = re.sub(r"(?<!\d)%", " % ", t)
    t = re.sub(r"(?<!\d)\.(?!\d)|(?<=\d)\.(?!\d)|(?<!\d)\.(?=\d)", " ", t)
    t = t.lower()
    t = re.sub(r"(?<=[a-z])(?=\d)", " ", t)          # "rm12" -> "rm 12"
    t = re.sub(r"[^a-z0-9'%.áàâäçéèêëíïîóôöúùûüñ ]", " ", t)
    out = []
    for w in t.split():
        w = w.strip("'.")
        if w.endswith("'s") and w[:-2] in TERM_OK:
            w = w[:-2]
        w = EQUIV.get(w, w)
        if w:
            out.append(w)
    return out


def join_letters(toks, refset):
    out, i = [], 0
    while i < len(toks):
        j = i
        while j < len(toks) and len(toks[j]) == 1 and toks[j].isalpha():
            j += 1
        if j - i >= 2:
            run = toks[i:j]
            if "".join(run) in refset:
                out.append("".join(run))
            elif run[0] == "a" and "".join(run[1:]) in refset and j - i >= 3:
                out += ["a", "".join(run[1:])]
            else:
                out += run
            i = j
        else:
            out.append(toks[i])
            i += 1
    return out


def apply_terms(toks, canon):
    """Replace accepted multi-word spellings of lexicon terms by the canonical token."""
    out, i = [], 0
    while i < len(toks):
        hit = None
        for k, vs in canon:
            for v in vs:
                n = len(v)
                if toks[i:i + n] == v:
                    hit = (k, n)
                    break
            if hit:
                break
        if hit:
            out.append(hit[0])
            i += hit[1]
        else:
            out.append(toks[i])
            i += 1
    return out


def ref_tokens(text):
    t = tokens(text)
    s = " ".join(t)
    for k in TERM_OK:
        if " " in k:
            s = re.sub(rf"\b{re.escape(k)}\b", k.replace(" ", "_"), s)
    return [w.replace("_", " ") if w.replace("_", " ") in TERM_OK else w for w in s.split()]


def stem(w):
    w = w.replace("'", "")
    return w[:-1] if len(w) > 3 and w.endswith("s") else w


def merge_compounds(ops, r, h):
    """'out paces' vs 'outpaces', 'co signed' vs 'cosigned': a split or joined compound is a match."""
    out, k = [], 0
    while k < len(ops):
        a = ops[k]
        b = ops[k + 1] if k + 1 < len(ops) else None
        if b:
            if a[0] == "s" and b[0] == "i" and stem(h[a[2]] + h[b[2]]) == stem(r[a[1]]) or \
               a[0] == "i" and b[0] == "s" and stem(h[a[2]] + h[b[2]]) == stem(r[b[1]]):
                i = a[1] if a[0] == "s" else b[1]
                out.append(("=", i, a[2]))
                k += 2
                continue
            if a[0] == "s" and b[0] == "d" and stem(r[a[1]] + r[b[1]]) == stem(h[a[2]]) or \
               a[0] == "d" and b[0] == "s" and stem(r[a[1]] + r[b[1]]) == stem(h[b[2]]):
                j = a[2] if a[0] == "s" else b[2]
                out += [("=", a[1], j), ("=", b[1], j)]
                k += 2
                continue
        if a[0] == "s" and {r[a[1]], h[a[2]]} == {"a", "one"}:
            a = ("=", a[1], a[2])
        out.append(a)
        k += 1
    return out


def edit_align(r, h):
    r0, h0 = r, h
    r, h = [stem(x) for x in r], [stem(x) for x in h]
    n, m = len(r), len(h)
    D = np.zeros((n + 1, m + 1), dtype=np.int32)
    D[:, 0] = np.arange(n + 1)
    D[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = min(D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    ops, i, j = [], n, m
    while i or j:
        if i and j and D[i, j] == D[i - 1, j - 1] + (r[i - 1] != h[j - 1]):
            ops.append(("=" if r[i - 1] == h[j - 1] else "s", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i and D[i, j] == D[i - 1, j] + 1:
            ops.append(("d", i - 1, None))
            i -= 1
        else:
            ops.append(("i", None, j - 1))
            j -= 1
    ops = merge_compounds(ops[::-1], r0, h0)
    return sum(op != "=" for op, _, _ in ops), ops


def hyp_tokens(words, refset, ref):
    """Recognizer words -> normalized tokens, numbers expanded to the best-matching spoken form.
    Returns (tokens, origin index of each token in `words`)."""
    merged = []                           # the recognizer may split "0.86" into "0" + ".86"
    for w in words:
        if merged and re.search(r"\d$", merged[-1]["w"]) and re.match(r"[.,]\d", w["w"]):
            merged[-1] = dict(merged[-1], w=merged[-1]["w"] + w["w"], end=w.get("end"))
        else:
            merged.append(w)
    words[:] = merged
    toks, orig = [], []
    for wi, w in enumerate(words):
        for t in tokens(w["w"]):
            toks.append(t)
            orig.append(wi)
    groups, k = [], 0                     # digit tokens: candidates
    for i, t in enumerate(toks):
        if re.search(r"\d", t):
            groups.append((i, number_forms(t)))
    choice = [0] * len(groups)

    def build(ch):
        out, og, gi = [], [], 0
        gmap = {i: g for i, g in groups}
        idx = {i: n for n, (i, _) in enumerate(groups)}
        for i, t in enumerate(toks):
            if i in gmap:
                ws = gmap[i][ch[idx[i]]]
                out += ws
                og += [orig[i]] * len(ws)
            else:
                out.append(t)
                og.append(orig[i])
        return out, og

    for _ in range(2):
        for gi, (i, cands) in enumerate(groups):
            best = None
            for c in range(len(cands)):
                ch = list(choice)
                ch[gi] = c
                out, _ = build(ch)
                d, _ = edit_align(ref, apply_terms(join_letters(out, refset), CANON))
                if best is None or d < best[0]:
                    best = (d, c)
            choice[gi] = best[1]
    out, og = build(choice)
    # joining letters / terms changes indices: rebuild origins alongside
    j1 = join_letters(out, refset)
    og1, p = [], 0
    for t in j1:                          # each joined token consumed len(t) single letters or one token
        if p < len(out) and out[p] == t:
            og1.append(og[p])
            p += 1
        else:
            og1.append(og[p])
            p += len(t)
    j2, og2, p = [], [], 0
    while p < len(j1):
        hit = None
        for kk, vs in CANON:
            for v in vs:
                if j1[p:p + len(v)] == v:
                    hit = (kk, len(v))
                    break
            if hit:
                break
        if hit:
            j2.append(hit[0])
            og2.append(og1[p])
            p += hit[1]
        else:
            j2.append(j1[p])
            og2.append(og1[p])
            p += 1
    return j2, og2


CANON = sorted(((k, [v.split() for v in vs]) for k, vs in TERM_OK.items()), key=lambda kv: -max(len(v) for v in kv[1]))


# ----------------------------------------------------------------------------- paragraphs
def paragraphs():
    lex = tts.load_lexicon()
    seen, out = {}, []
    for cut in ("extended", "core"):
        p = os.path.join(ROOT, "script", "_build", f"film_{cut}.json")
        film = json.load(open(p))
        voice = (film.get("voice") or {}).get("reference_id")
        for r in tts.plan_requests(film, lex, voice):
            if r["key"] in seen:
                seen[r["key"]]["cuts"].add(cut)
                continue
            r["cuts"] = {cut}
            r["unit"] = next(s["unit"] for s in film["scenes"] if s["id"] == r["scene"])
            seen[r["key"]] = r
            out.append(r)
    return out


def transcribe(a):
    from faster_whisper import WhisperModel
    os.makedirs(ASR, exist_ok=True)
    model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=a.threads,
                         download_root=a.model_dir)
    todo = [r for r in paragraphs() if tts.cached(r["key"]) and not os.path.exists(os.path.join(ASR, r["key"] + ".json"))]
    if a.reverse:                         # a second process can work from the other end
        todo = todo[::-1]
    print(f"[qa] {len(todo)} paragraphs to transcribe with {a.model}", flush=True)
    for n, r in enumerate(todo):
        if os.path.exists(os.path.join(ASR, r["key"] + ".json")):
            continue
        wav = os.path.join(tts.CACHE, r["key"] + ".wav")
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        segs, info = model.transcribe(np.frombuffer(pcm, dtype="<f4"), language="en", beam_size=5, word_timestamps=True,
                                      condition_on_previous_text=False, vad_filter=False, temperature=0.0)
        words, text = [], []
        for s in segs:
            text.append(s.text)
            for w in s.words or []:
                words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
                              "p": round(w.probability, 3)})
        json.dump({"key": r["key"], "model": a.model, "text": " ".join(x.strip() for x in text), "words": words},
                  open(os.path.join(ASR, r["key"] + ".json"), "w"), indent=0, ensure_ascii=False)
        if n % 20 == 0:
            print(f"[qa] {n + 1}/{len(todo)} {r['scene']} p{r['para'] + 1}", flush=True)


# ----------------------------------------------------------------------------- measures
def ebur128(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = p.stderr[p.stderr.rfind("Summary:"):]
    g = lambda rx: (float(m.group(1)) if (m := re.search(rx, s)) and m.group(1) != "-inf" else None)
    return {"I": g(r"I:\s+(-?[\d.]+|-inf) LUFS"), "TP": g(r"Peak:\s+(-?[\d.]+|-inf) dBFS"), "LRA": g(r"LRA:\s+(-?[\d.]+) LU")}


def report(a):
    paras = paragraphs()
    lex_terms = {k.lower() for k in tts.load_lexicon()}
    res, missing_audio = [], []
    for r in paras:
        wav = tts.cached(r["key"])
        if not wav:
            missing_audio.append(f"{r['scene']} p{r['para'] + 1}")
            continue
        meta = json.load(open(os.path.join(tts.CACHE, r["key"] + ".json")))
        x = read_wav(wav)
        dur = len(x) / SR
        sents = r["paragraph"]["sentences"]
        bounds, s0, s1, method = split_sentences(sents, x, hints=hints_for(r["key"], len(sents)))
        bounds_nohint = split_sentences(sents, x)[0]
        sil, thr = silences(x)
        inner = [(round(u, 2), round(v, 2)) for u, v in sil if u > s0 + 0.05 and v < s1 - 0.05]
        # sentence gaps vs pauses inside a sentence
        gaps = [round(bounds[k + 1][0] - bounds[k][1], 3) for k in range(len(bounds) - 1)]
        cut_pts = {(round(bounds[k][1], 2), round(bounds[k + 1][0], 2)) for k in range(len(bounds) - 1)}
        long_inside = [(u, v) for u, v in inner if (v - u) > 0.9 and (u, v) not in cut_pts]
        speech = s1 - s0
        e = {"key": r["key"], "scene": r["scene"], "unit": r["unit"], "para": r["para"] + 1, "cuts": sorted(r["cuts"]),
             "words": r["words"], "duration": round(dur, 3), "speech_s": round(speech, 3),
             "raw_wpm": round(r["words"] / speech * 60, 1) if speech > 0 else None,
             "lead_sil": round(s0, 3), "trail_sil": round(dur - s1, 3), "sentence_gaps": gaps, "align_method": method,
             "long_pauses_inside": long_inside, "peak": round(float(np.max(np.abs(x))), 4),
             "hint_moved": [round(bounds[k][0] - bounds_nohint[k][0], 2) for k in range(1, len(bounds))
                            if abs(bounds[k][0] - bounds_nohint[k][0]) > 0.05],
             "created": meta.get("created")}
        e.update({"loud_" + k: v for k, v in ebur128(wav).items()})
        ap = os.path.join(ASR, r["key"] + ".json")
        if os.path.exists(ap):
            asr = json.load(open(ap))
            ref_text = " ".join(s["text"] for s in sents)
            ref = ref_tokens(ref_text)
            refset = set(ref)
            hyp, og = hyp_tokens(asr["words"], refset, ref)
            d, ops = edit_align(ref, hyp)
            e["wer"] = round(d / max(1, len(ref)), 3)
            e["asr_text"] = asr["text"]
            low = " ".join(tokens(asr["text"]))
            e["read_aloud"] = [p for p in READ_ALOUD if p in low]
            dels, ins, subs, terms = [], [], [], []
            run_d, run_i = [], []
            for op, i, j in ops + [("=", None, None)]:
                if op == "d":
                    run_d.append(ref[i])
                elif run_d:
                    dels.append(" ".join(run_d))
                    run_d = []
                if op == "i":
                    run_i.append(hyp[j])
                elif run_i:
                    ins.append(" ".join(run_i))
                    run_i = []
                if op == "s":
                    subs.append(f"{ref[i]} -> {hyp[j]}")
            for op, i, j in ops:
                if i is not None and ref[i] in TERM_OK and ref[i] in lex_terms | {"mhd", "abc", "vks", "rm", "pm", "jean zay"}:
                    terms.append({"term": ref[i], "ok": op == "=", "heard": hyp[j] if j is not None else None})
            e.update(deletions=dels, insertions=ins, substitutions=subs, terms=terms)
            # cue check: first recognized word of each sentence vs align.py start
            ref_sent = []
            for si, s in enumerate(sents):
                ref_sent += [si] * len(ref_tokens(s["text"]))
            first = {}
            for op, i, j in ops:
                if op == "=" and ref_sent[i] not in first:
                    first[ref_sent[i]] = (i, j)
            dev = []
            for si, (u, v) in enumerate(bounds):
                if si in first:
                    i, j = first[si]
                    off = sum(1 for q in range(i) if ref_sent[q] == si)      # words before the matched one
                    if off == 0:
                        w = asr["words"][og[j]]
                        dev.append(round(u - w["start"], 3))
            e["cue_dev"] = dev
        res.append(e)
    out = {"paragraphs": res, "missing_audio": missing_audio}
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"[qa] {len(res)} paragraphs measured, {len(missing_audio)} without audio -> {os.path.relpath(a.out, ROOT)}")


def first_word_starts(r, asr):
    """Recognizer start of the first word of each sentence, when that word was recognized as written."""
    sents = r["paragraph"]["sentences"]
    ref = ref_tokens(" ".join(s["text"] for s in sents))
    words = [dict(w) for w in asr["words"]]
    hyp, og = hyp_tokens(words, set(ref), ref)
    _, ops = edit_align(ref, hyp)
    rs = []
    for si, s in enumerate(sents):
        rs += [si] * len(ref_tokens(s["text"]))
    out = [None] * len(sents)
    seen = set()
    for op, i, j in ops:
        if i is None or rs[i] in seen:
            continue
        seen.add(rs[i])
        if op == "=" and (i == 0 or rs[i - 1] != rs[i]):
            out[rs[i]] = words[og[j]]
    return out


def hints(a):
    """audio/align_hints.json: for every paragraph of 2+ sentences, the start of sentences 2..K as heard by the
    recognizer, kept only where it sits inside a pause or within 0.45 s of a pause's end (align.py then takes
    that pause as the boundary; an unreliable hint is left out and the silence DP decides)."""
    out, kept, dropped = {}, 0, 0
    for r in paragraphs():
        sents = r["paragraph"]["sentences"]
        ap = os.path.join(ASR, r["key"] + ".json")
        wav = tts.cached(r["key"])
        if len(sents) < 2 or not wav or not os.path.exists(ap):
            continue
        x = read_wav(wav)
        sil, _ = silences(x)
        ends = [b for u, b in sil if b - u >= 0.18 and u > 0.001 and b < len(x) / SR - 0.001]
        fw = first_word_starts(r, json.load(open(ap)))
        h = []
        for w in fw[1:]:
            if w is None or w.get("p", 1) < 0.3:
                h.append(None)
                dropped += 1
                continue
            t = w["start"]
            inside = any(u - 0.001 <= t <= b for u, b in sil)
            near = min((abs(b - t) for b in ends), default=9)
            if inside or near <= 0.45:
                h.append(round(t, 3))
                kept += 1
            else:
                h.append(None)
                dropped += 1
        if any(v is not None for v in h):
            out[r["key"]] = h
    json.dump({"comment": "Approximate sentence starts (s, in each paragraph's cache wav) from a speech-recognition pass "
                          "(audio/qa.py hints, faster-whisper " + a.model + "). Read by audio/align.py to choose between "
                          "pauses; timings remain silence-based. Keyed by paragraph cache key; null = no hint.",
               "hints": out}, open(os.path.join(HERE, "align_hints.json"), "w"), indent=0)
    print(f"[qa] align hints: {kept} sentence starts kept, {dropped} left to the silence DP, {len(out)} paragraphs")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["transcribe", "report", "hints"])
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--model-dir", default=None)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--reverse", action="store_true", help="transcribe from the last paragraph backwards")
    ap.add_argument("--out", default=os.path.join(HERE, "qa_report.json"))
    a = ap.parse_args()
    {"transcribe": transcribe, "report": report, "hints": hints}[a.cmd](a)


if __name__ == "__main__":
    main()
