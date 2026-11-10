#!/usr/bin/env python3
"""assemble_cut.py: build one resolved film script (schema 2) from the unit scripts.

    script/<unit>.json  +  plan/outline.json "cuts"  +  data/*.json   ->   script/_build/film_<name>.json

Running order
  core      : cuts.core.chapters, plus the extra unit ch10q placed before ch11 (BRIEF section 3.3).
  extended  : the same chapters, then every module of cuts.extensions.modules inserted, in that order,
              right after its anchor: the unit's own "insert_after" (else the outline's). An anchor is a
              scene id ("09.6"), a question card ("ch08.Q") or a unit id ("X5a" = after that unit's last
              scene as placed so far). A chapter's question card therefore stays after the modules that
              were inserted inside the chapter (the card ends the chapter, extensions included).
  unit      : --unit ch04 -> every scene of one unit (for `make check`), name unit_ch04.
  Per scene, "cuts": ["core"] / ["extended"] restricts it to one cut; without it the outline's
  extended_variant applies (10.8 skipped in the extended cut, 10.9 replaced there by 10.9-bridge).

Per scene
  * paragraphs: [{"hold_after": s, "sentences": [{"id", "cue", "text"}]}]  (legacy: a list of sentence lists)
  * variant: a scene with "variants": {"result": {...}} switches to the result narration as soon as every
    data file in "deps" exists and is not flagged pending ({"pending": true} or meta.pending); its
    {{field}} placeholders are filled from those files (see fill()); a pending scene whose data arrived
    gets the effective status "provisional" (stamped on screen until a human marks it ready).
  * question cards: "question": {...}; without paragraphs, the spoken sentence is question.en.
  * lint: ids, cues, markup, TTS tags, parentheses, word budget against target_s (BRIEF D21, section 6).

French narration (--lang fr, BRIEF section 9; the visuals stay in English)
  * overlay <units>/fr/<unit>.json: {"schema": 2, "unit", "lang": "fr", "voice": {...}, "sentences": {id: text},
    "variants": {scene id: {id: text}}, "notes", optional "title" (chapter name in the MP4)}. Every sentence keeps
    its id and cue (the scenes animate on cue names); the French text replaces the English one, before {{field}}
    filling for result variants. Fallbacks, in order: the overlay, an inline "text_fr" in the English script, then
    the English text (flagged "untranslated": true, warned; audio/tts.py refuses to bill such a paragraph live).
  * question card without paragraphs: overlay "<scene>.s1", else question.say_fr, else question.fr.
  * {{field}}: numbers spoken in French ("zéro virgule quatre-vingt-six"), a string field <name>_fr first.
  * voice: audio/voice_fr.json (make narration LANG=fr VOICE=...), else the overlay's "voice", else the
    script's "voice_fr", else the English voice (warned). --voice overrides all.
  * lint: markup kinds and {{field}} names must match the English sentence; length checked against target_s
    with the French allowance (+15-20 % expected, warned beyond +40 %).
  * outputs are suffixed: film_<name>_fr.json, questions_<name>_fr.json.

Usage
  python3 -I tools/assemble_cut.py --cut core|extended [--name N] [--units script] [--cuts plan/outline.json]
                                    [--voice REFERENCE_ID] [--variant auto|pending|result] [--lang en|fr] [--strict]
  python3 -I tools/assemble_cut.py --unit ch04 [--lang fr]
Outputs script/_build/film_<name>.json and script/_build/questions_<name>.json (question register).
"""
import argparse, datetime, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTION_CARD_FILE = "scenes/_shared/question_card.html"   # default page of a question-card scene without "file"
RAW_WPM = 146.0          # measured raw pace of the Ethan voice incl. [long pause] (BRIEF D21)
LONG_PAUSE_S = 0.9       # silence standing for [long pause] between two paragraphs (see audio/tts.py)
# extra units placed in every cut before a given chapter: the outline's "extra_units"
# ([{"unit": "...", "before": "..."}]); none by default (the old film's list went with its chapters)
EXTRA_UNITS = []
MARK = re.compile(r"\{(u|b|param|model|metric)\}(.*?)\{/\}")
CUE_RE = re.compile(r"^[A-Za-z_][\w-]*$")

warnings, errors = [], []
LANG = "en"              # narration language (--lang); "en" builds exactly the same film as before
LANGS = ("en", "fr")
UNTRANSLATED = []        # sentence ids of the cut still in English in a non-English build
FR_TARGET_BAND = (0.85, 1.40)   # French narration vs target_s: +15-20 % expected (BRIEF section 9)


def warn(msg):
    warnings.append(msg)


def err(msg):
    errors.append(msg)


def plain(text):
    return MARK.sub(r"\2", text)


def words(text):
    return len(re.findall(r"[\w'’-]+", plain(text)))


def rel(p):
    return os.path.relpath(p, ROOT)


# ----------------------------------------------------------------------------- numbers as spoken
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def int_words(n):
    if n < 0:
        return "minus " + int_words(-n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + int_words(n % 100))
    for div, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= div:
            return int_words(n // div) + " " + name + ("" if n % div == 0 else " " + int_words(n % div))
    return str(n)


def speak_number(x, digits=None):
    """0.86 -> 'zero point eight six'; 17 -> 'seventeen'; 17.25 -> 'seventeen point two five'."""
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer() and digits is None):
        return int_words(int(x))
    s = f"{x:.{digits}f}" if digits is not None else repr(float(x))
    if "e" in s or "E" in s:
        s = f"{x:.6f}".rstrip("0")
    neg = s.startswith("-")
    s = s.lstrip("-")
    a, _, b = s.partition(".")
    out = ("minus " if neg else "") + int_words(int(a))
    if b:
        out += " point " + " ".join(ONES[int(c)] for c in b)
    return out


FR_ONES = ("zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize "
           "dix-sept dix-huit dix-neuf").split()
FR_TENS = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def int_words_fr(n):
    """French cardinal, traditional spelling: 21 'vingt et un', 71 'soixante et onze', 80 'quatre-vingts'."""
    if n < 0:
        return "moins " + int_words_fr(-n)
    if n < 20:
        return FR_ONES[n]
    if n < 100:
        t, u = divmod(n, 10)
        if t in (7, 9):
            base = "soixante" if t == 7 else "quatre-vingt"
            return base + (" et " if t == 7 and u == 1 else "-") + FR_ONES[10 + u]
        if t == 8:
            return "quatre-vingts" if u == 0 else "quatre-vingt-" + FR_ONES[u]
        return FR_TENS[t] + ("" if u == 0 else " et un" if u == 1 else "-" + FR_ONES[u])
    if n < 1000:
        h, r = divmod(n, 100)
        head = "cent" if h == 1 else FR_ONES[h] + (" cents" if r == 0 else " cent")
        return head + ("" if r == 0 else " " + int_words_fr(r))
    if n < 10 ** 6:
        k, r = divmod(n, 1000)
        head = "mille" if k == 1 else re.sub(r"(cent|vingt)s$", r"\1", int_words_fr(k)) + " mille"
        return head + ("" if r == 0 else " " + int_words_fr(r))
    div, word = (10 ** 9, "milliard") if n >= 10 ** 9 else (10 ** 6, "million")
    q, r = divmod(n, div)
    return int_words_fr(q) + " " + word + ("s" if q > 1 else "") + ("" if r == 0 else " " + int_words_fr(r))


def speak_number_fr(x, digits=None):
    """0.86 -> 'zéro virgule quatre-vingt-six'; 0.0123 -> 'zéro virgule zéro cent vingt-trois'; 17 -> 'dix-sept'.
    The decimal part is read as a number (leading zeros said) up to three digits, digit by digit beyond."""
    if isinstance(x, bool):
        return "oui" if x else "non"
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer() and digits is None):
        return int_words_fr(int(x))
    s = f"{x:.{digits}f}" if digits is not None else repr(float(x))
    if "e" in s or "E" in s:
        s = f"{x:.6f}".rstrip("0")
    neg = s.startswith("-")
    a, _, b = s.lstrip("-").partition(".")
    out = ("moins " if neg else "") + int_words_fr(int(a))
    if b:
        z = len(b) - len(b.lstrip("0"))
        r = b[z:]
        if r and len(r) <= 3:
            out += " virgule " + " ".join(["zéro"] * z + [int_words_fr(int(r))])
        else:
            out += " virgule " + " ".join(FR_ONES[int(c)] for c in b)
    return out


def say_number(x, digits=None):
    return speak_number_fr(x, digits) if LANG == "fr" else speak_number(x, digits)


# ----------------------------------------------------------------------------- data files
def load_data(dep):
    """Returns the parsed data file, or None if it is missing or flagged pending."""
    p = os.path.join(ROOT, dep)
    if not os.path.exists(p):
        return None
    if not dep.endswith(".json"):
        return {}
    try:
        d = json.load(open(p))
    except Exception as e:   # a broken data file must not pass silently
        err(f"data file {dep} is not valid JSON: {e}")
        return None
    if isinstance(d, dict) and (d.get("pending") is True or (d.get("meta") or {}).get("pending") is True):
        return None
    return d


def lookup(datas, name):
    """{{name}}: first in each file's "fields" object, then as a dotted path from the file root."""
    for d in datas:
        if not isinstance(d, dict):
            continue
        f = d.get("fields")
        if isinstance(f, dict) and name in f:
            return True, f[name]
        cur, ok = d, True
        for part in name.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
                cur = cur[int(part)]
            else:
                ok = False
                break
        if ok:
            return True, cur
    return False, None


PLACE = re.compile(r"\{\{\s*([\w.\-]+)\s*(?::\s*(\w+))?\s*\}\}")


def fill(text, datas, sid):
    """{{field}} -> spoken words for numbers, the string itself otherwise;
       {{field:digits}} -> the raw number; {{field:1}}, {{field:2}} -> spoken with that many decimals."""
    missing = []

    def rep(m):
        ok, v = lookup(datas, m.group(1))
        if not ok:
            missing.append(m.group(1))
            return m.group(0)
        mod = m.group(2)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if mod == "digits":
                return str(v) if LANG == "en" else str(v).replace(".", ",")
            if mod and mod.isdigit():
                return say_number(float(v), int(mod))
            return say_number(v)
        if LANG != "en":                       # a string field: its translation <name>_<lang> first
            ok_l, v_l = lookup(datas, f"{m.group(1)}_{LANG}")
            if ok_l and isinstance(v_l, str):
                return v_l
            if isinstance(v, str):
                warn(f"{sid}: string field '{m.group(1)}' has no '{m.group(1)}_{LANG}': English text in the {LANG} narration")
            elif isinstance(v, bool):
                return say_number(v)
        return str(v)

    out = PLACE.sub(rep, text)
    return out, missing


def cond_ok(when, datas):
    if not when:
        return True
    neg = when.startswith("!")
    ok, v = lookup(datas, when.lstrip("!"))
    val = bool(v) if ok else False
    return (not val) if neg else val


# ----------------------------------------------------------------------------- scenes
def norm_paragraphs(paras, sid):
    out = []
    for p in paras or []:
        if isinstance(p, list):          # legacy schema 1: a paragraph is a list of sentences
            p = {"hold_after": 0.0, "sentences": p}
        out.append({"hold_after": float(p.get("hold_after") or 0.0), "when": p.get("when"),
                    "sentences": [dict(s) for s in p.get("sentences", [])]})
    return out


MARK_OPEN = re.compile(r"\{(u|b|param|model|metric)\}")


def translate(paras, table, sid, unit_name, implicit_ids=True):
    """Non-English build: put the translation into each sentence's "text" (same id, same cue). Source order:
    the overlay table {sentence id: text}, then an inline "text_<lang>" of the English script; otherwise the
    English text stays, flagged "untranslated" (collected in UNTRANSLATED, warned per unit in main())."""
    n = 0
    for p in paras:
        for x in p["sentences"]:
            n += 1
            key = x.get("id") or (f"{sid}.s{n}" if implicit_ids else None)
            en = x.get("text", "")
            tr = (table or {}).get(key) if key else None
            if tr is None:
                tr = x.get(f"text_{LANG}")
            x.pop(f"text_{LANG}", None)
            if not isinstance(tr, str) or not tr.strip():
                x["untranslated"] = True
                UNTRANSLATED.append((unit_name, key or f"{sid}.?"))
                continue
            if sorted(MARK_OPEN.findall(en)) != sorted(MARK_OPEN.findall(tr)):
                warn(f"{key}: subtitle markup differs from the English ({sorted(MARK_OPEN.findall(en))} -> "
                     f"{sorted(MARK_OPEN.findall(tr))})")
            fe, ft = sorted({m.group(1) for m in PLACE.finditer(en)}), sorted({m.group(1) for m in PLACE.finditer(tr)})
            if fe != ft:
                warn(f"{key}: {{{{field}}}} placeholders differ from the English ({fe} -> {ft})")
            x["text"] = tr


def resolve_scene(sc, unit, opts):
    sid = sc["id"]
    ov = unit.get("_overlay") or {}
    s = dict(sc)
    s["unit"] = unit["unit"]
    s["status_script"] = sc.get("status", "ready")
    if s["status_script"] not in ("ready", "pending"):
        warn(f"{sid}: status '{s['status_script']}' is not ready|pending (BRIEF D4); treated as pending")
        s["status_script"] = "pending"
    deps = list(sc.get("deps") or [])
    datas = [load_data(d) for d in deps]
    have = bool(deps) and all(d is not None for d in datas)
    for d, dd in zip(deps, datas):
        if dd is None and s["status_script"] == "ready":
            warn(f"{sid}: data file {d} is missing for a ready scene: rendered as pending")
    status = s["status_script"]
    if status == "ready" and deps and not have:
        status = "pending"
    elif status == "pending" and have:
        status = "provisional"
    variants = sc.get("variants") or {}
    variant = "main"
    paras = norm_paragraphs(sc.get("paragraphs"), sid)
    if LANG != "en":
        translate(paras, ov.get("sentences"), sid, unit["unit"])
    if status == "pending" and variants:
        variant = "pending"
    want = opts.variant
    if variants.get("result") and (want == "result" or (want == "auto" and have)):
        r = variants["result"]
        rp = norm_paragraphs(r.get("paragraphs"), sid)
        rp = [p for p in rp if cond_ok(p.get("when"), datas)]
        for p in rp:
            p["sentences"] = [x for x in p["sentences"] if cond_ok(x.get("when"), datas)]
        rp = [p for p in rp if p["sentences"]]
        if LANG != "en":
            translate(rp, (ov.get("variants") or {}).get(sid), sid, unit["unit"], implicit_ids=False)
        miss = []
        for p in rp:
            for x in p["sentences"]:
                x["text"], m = fill(x.get("text", ""), datas, sid)
                miss += m
        for f in r.get("data_fields") or []:
            if not lookup(datas, f)[0]:
                miss.append(f)
        if want == "result" and not have:
            warn(f"{sid}: --variant result forced but data missing ({', '.join(d for d, x in zip(deps, datas) if x is None)})")
        if miss:
            warn(f"{sid}: result variant kept back, fields missing in the data: {sorted(set(miss))}")
        elif rp:
            paras, variant = rp, "result"
    if not paras and sc.get("question"):            # spoken: question.say if given (numbers as read), else question.en
        q = sc["question"]
        paras = [{"hold_after": 0.0, "when": None,
                  "sentences": [{"id": f"{sid}.s1", "cue": "q", "text": q.get("say") or q.get("en", "")}]}]
        if LANG != "en":                            # overlay "<scene>.s1", else question.say_<lang>, else question.<lang>
            spoken = q.get(f"say_{LANG}") or q.get(LANG)
            if spoken:
                paras[0]["sentences"][0][f"text_{LANG}"] = spoken
            translate(paras, ov.get("sentences"), sid, unit["unit"])
    # ids, cues and lint
    cues = set()
    n = 0
    for p in paras:
        p.pop("when", None)
        for x in p["sentences"]:
            n += 1
            x.pop("when", None)
            x.setdefault("id", f"{sid}.s{n}")
            x.setdefault("cue", None)
            t = x.get("text", "")
            if not t.strip():
                err(f"{sid}/{x['id']}: empty sentence")
            if x["cue"]:
                if not CUE_RE.match(x["cue"]):
                    err(f"{sid}/{x['id']}: cue name '{x['cue']}' must match {CUE_RE.pattern}")
                if x["cue"] in cues:
                    err(f"{sid}: cue '{x['cue']}' used twice")
                cues.add(x["cue"])
            if re.search(r"[\[\]<>]", plain(t)):
                warn(f"{sid}/{x['id']}: TTS tags or brackets in the text (the tool adds the acting cue and [long pause])")
            if re.search(r"[()]", plain(t)):
                warn(f"{sid}/{x['id']}: parentheses in narration (writing rules, BRIEF section 6)")
            if re.search(r"\d|[=%/^_]", plain(re.sub(r"\{\{.*?\}\}", "", t))):
                warn(f"{sid}/{x['id']}: digits or symbols in narration: write numbers as they are read (BRIEF section 6)")
            if "{{" in t:
                err(f"{sid}/{x['id']}: unfilled placeholder in '{t}'")
            opened = len(re.findall(r"\{(?:u|b|param|model|metric)\}", t))
            if opened != t.count("{/}"):
                err(f"{sid}/{x['id']}: unbalanced subtitle markup")
    s["paragraphs"] = paras
    s["status"] = status
    s["stamp"] = next((d.get("meta", {}).get("stamp") for d in datas if isinstance(d, dict) and isinstance(d.get("meta"), dict)
                       and d["meta"].get("stamp")), None) if status == "provisional" else None
    s["variant"] = variant
    s["deps"] = deps
    s["data_present"] = have
    s["lead_in"] = float(sc.get("lead_in", 0.4))
    s["tail"] = float(sc.get("tail", 0.8))
    s["entry"] = sc.get("entry") or {"data": {}, "params": {}}
    if not sc.get("file"):
        if sc.get("question"):
            s["file"] = QUESTION_CARD_FILE
        else:
            err(f"{sid}: no 'file'")
    w = sum(words(x["text"]) for p in paras for x in p["sentences"])
    s["words"] = w
    est = w / RAW_WPM * 60 + sum(p["hold_after"] for p in paras) + LONG_PAUSE_S * max(0, len(paras) - 1) \
        + s["lead_in"] + s["tail"]
    s["estimated_s"] = round(est, 1)
    tgt = sc.get("target_s")
    if LANG == "en":
        if tgt and not sc.get("question") and abs(est - tgt) > 0.15 * tgt:
            warn(f"{sid}: about {est:.0f} s for {w} words, target {tgt} s +-15 % (BRIEF D21)")
        if sc.get("question") and not (5 <= est <= 11):
            warn(f"{sid}: question card about {est:.1f} s, the brief asks 6-10 s")
    else:                       # the French timeline absorbs +15-20 % (BRIEF section 9): warn only beyond the band
        lo, hi = FR_TARGET_BAND
        if tgt and not sc.get("question") and not (lo * tgt <= est <= hi * tgt):
            warn(f"{sid}: about {est:.0f} s for {w} {LANG} words, target {tgt} s (expected +15-20 %, "
                 f"band {lo:.2f}-{hi:.2f} x target)")
        if sc.get("question") and not (5 <= est <= 13):
            warn(f"{sid}: question card about {est:.1f} s in {LANG}, the brief asks 6-10 s (+20 % allowed)")
    if sc.get("question"):
        q = sc["question"]
        if len(plain(q.get("en", "")).split()) > 18:
            warn(f"{sid}: question card longer than 18 words on screen")
        for k in ("en", "fr", "why", "unblocks", "ask_who"):
            if not q.get(k):
                warn(f"{sid}: question.{k} is empty")
    for k in ("variants",):
        s.pop(k, None)
    return s


# ----------------------------------------------------------------------------- cuts
def load_unit(units_dir, name, required=True):
    p = os.path.join(units_dir, name + ".json")
    if not os.path.exists(p):
        (err if required and OPTS.strict else warn)(f"unit {name}: {rel(p)} does not exist yet (skipped)")
        return None
    u = json.load(open(p))
    if u.get("schema") != 2:
        warn(f"unit {name}: schema {u.get('schema')} (expected 2)")
    u.setdefault("unit", name)
    u["_sha"] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    u["_path"] = rel(p)
    if LANG != "en":
        u["_overlay"] = load_overlay(units_dir, u)
    return u


def unit_sentence_ids(u):
    """{"main": ids of the main paragraphs (+ the generated '<scene>.s1' of a bare question card),
        "variants": {scene id: ids of its result variant}} of every scene of the unit, whatever the cut."""
    main, var = set(), {}
    for sc in u.get("scenes", []):
        paras = norm_paragraphs(sc.get("paragraphs"), sc["id"])
        n = 0
        for p in paras:
            for x in p["sentences"]:
                n += 1
                main.add(x.get("id") or f"{sc['id']}.s{n}")
        if not paras and sc.get("question"):
            main.add(f"{sc['id']}.s1")
        r = (sc.get("variants") or {}).get("result")
        if r:
            var[sc["id"]] = {x.get("id") for p in norm_paragraphs(r.get("paragraphs"), sc["id"]) for x in p["sentences"]}
    return {"main": main, "variants": var}


def load_overlay(units_dir, u):
    """<units>/<lang>/<unit>.json (translation overlay, BRIEF section 9), checked against the English unit."""
    name = u["unit"]
    p = os.path.join(units_dir, LANG, name + ".json")
    if not os.path.exists(p):
        inline = sum(1 for sc in u.get("scenes", []) for x in
                     [x for pp in norm_paragraphs(sc.get("paragraphs"), sc["id"]) for x in pp["sentences"]] if x.get(f"text_{LANG}"))
        warn(f"unit {name}: no {LANG} overlay {rel(p)}"
             + (f" ({inline} inline text_{LANG} used)" if inline else ": the English text is kept"))
        return {"_path": None}
    try:
        ov = json.load(open(p))
    except Exception as e:
        err(f"overlay {rel(p)} is not valid JSON: {e}")
        return {"_path": None}
    if ov.get("schema") != 2:
        warn(f"overlay {rel(p)}: schema {ov.get('schema')} (expected 2)")
    if ov.get("unit") not in (None, name):
        warn(f"overlay {rel(p)}: unit '{ov.get('unit')}' (expected '{name}')")
    if ov.get("lang") not in (None, LANG):
        warn(f"overlay {rel(p)}: lang '{ov.get('lang')}' (expected '{LANG}')")
    ids = unit_sentence_ids(u)
    for k, v in (ov.get("sentences") or {}).items():
        if k not in ids["main"]:
            warn(f"overlay {rel(p)}: sentence id {k} is not in the unit's main paragraphs (ignored)")
        if not isinstance(v, str):
            err(f"overlay {rel(p)}: sentence {k} is not a string")
    for scid, tab in (ov.get("variants") or {}).items():
        if scid not in ids["variants"]:
            warn(f"overlay {rel(p)}: variants of {scid}, which has no result variant (ignored)")
            continue
        for k in tab or {}:
            if k not in ids["variants"][scid]:
                warn(f"overlay {rel(p)}: variant sentence id {k} is not in {scid}'s result variant (ignored)")
    ov["_path"] = rel(p)
    ov["_sha"] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    return ov


def in_cut(sc, cut, ext_rules, unit_ids):
    if cut == "unit":
        return True
    if sc.get("cuts"):
        return cut in sc["cuts"]
    r = ext_rules.get(sc["id"])
    if cut == "extended":
        if r and r.get("skip"):
            return False
        if r and r.get("id") and r["id"] in unit_ids:
            return False                            # replaced by its extended variant
        if sc["id"] in ext_rules.get("_variant_ids", set()):
            return True
    if cut == "core" and sc["id"] in ext_rules.get("_variant_ids", set()):
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", choices=["core", "extended", "update"],
                    help="update = the 'Results update' episode (cuts.results_update_episode): its scenes in their "
                         "result variant, scenes whose data are still missing dropped")
    ap.add_argument("--unit")
    ap.add_argument("--name")
    ap.add_argument("--units", default="script")
    ap.add_argument("--cuts", default="plan/outline.json")
    ap.add_argument("--out", default="script/_build")
    ap.add_argument("--voice", help="override voice.reference_id (narration swap); default: audio/voice.json, else the units")
    ap.add_argument("--variant", choices=["auto", "pending", "result"], default="auto")
    ap.add_argument("--lang", choices=LANGS, default="en",
                    help="narration language: fr merges <units>/fr/<unit>.json (BRIEF section 9); outputs suffixed _fr")
    ap.add_argument("--strict", action="store_true", help="missing units and lint warnings are errors")
    global OPTS, LANG
    OPTS = opts = ap.parse_args()
    LANG = opts.lang
    if not opts.cut and not opts.unit:
        ap.error("--cut or --unit")
    units_dir = os.path.join(ROOT, opts.units)
    if not os.path.exists(os.path.join(ROOT, opts.cuts)):
        sys.exit(f"[assemble] {opts.cuts} does not exist: write the film's outline (\"cuts\": {{\"core\": {{\"chapters\": [...]}}}}) "
                 "or pass --cuts <file>")
    outline = json.load(open(os.path.join(ROOT, opts.cuts)))
    cuts = outline["cuts"]
    ext_rules = {}
    for ch in outline.get("chapters", []):
        for sc in ch.get("scenes", []):
            ev = sc.get("extended_variant")
            if ev:
                ext_rules[sc["id"]] = ev
    ext_rules["_variant_ids"] = {v["id"] for k, v in ext_rules.items() if isinstance(v, dict) and v.get("id")}
    alias = {k: v["id"] for k, v in ext_rules.items() if isinstance(v, dict) and v.get("id")}
    modules_meta = {m["id"]: m for m in outline.get("modules", [])}
    extra = outline.get("extra_units", EXTRA_UNITS)

    if opts.unit:
        cut, name = "unit", opts.name or f"unit_{opts.unit}"
        chapters, modules = [opts.unit], []
    else:
        cut, name = opts.cut, opts.name or opts.cut
        chapters = list(cuts["core"]["chapters"])
        for e in extra:
            if e["unit"] not in chapters:
                i = chapters.index(e["before"]) if e["before"] in chapters else len(chapters)
                chapters.insert(i, e["unit"])
        modules = list(cuts.get("extensions", {}).get("modules", [])) if cut == "extended" else []
    if LANG != "en" and not name.endswith("_" + LANG):     # separate builds per language: film_core_fr.json ...
        name += "_" + LANG

    seq, units = [], []          # seq: list of (unit_id, raw scene)

    def unit_scenes(u):
        ids = {s["id"] for s in u.get("scenes", [])}
        return [s for s in u.get("scenes", []) if in_cut(s, cut, ext_rules, ids)]

    if cut == "update":                      # D5: the "Results update" episode, from every unit
        want = (cuts.get("results_update_episode") or {}).get("scenes", [])
        pool = {}
        for un in chapters + list(cuts.get("extensions", {}).get("modules", [])):
            u = load_unit(units_dir, un, required=False)
            if u:
                units.append(u)
                for s in u.get("scenes", []):
                    pool.setdefault(s["id"], (u["unit"], s))
        for sid in want:
            if sid not in pool:
                warn(f"update episode: scene {sid} has no script yet (skipped)")
                continue
            un, s = pool[sid]
            if s.get("deps") and any(load_data(d) is None for d in s["deps"]):
                warn(f"update episode: {sid} dropped, its data are still missing")
                continue
            seq.append((un, s))
        opts.variant = "result"
        units = [u for u in units if any(un == u["unit"] for un, _ in seq)]
        chapters, modules = [], []
    for ch in chapters:
        u = load_unit(units_dir, ch)
        if not u:
            continue
        units.append(u)
        seq += [(u["unit"], s) for s in unit_scenes(u)]
    for mid in modules:
        u = load_unit(units_dir, mid)
        if not u:
            continue
        anchor = u.get("insert_after") or modules_meta.get(mid, {}).get("insert_after")
        ids = [s["id"] for _, s in seq]
        pos = None
        if anchor in ids:
            pos = ids.index(anchor)
        elif anchor in alias and alias[anchor] in ids:
            pos = ids.index(alias[anchor])
        elif any(un == anchor for un, _ in seq):
            pos = max(i for i, (un, _) in enumerate(seq) if un == anchor)
        if pos is None:
            (err if opts.strict else warn)(f"module {mid}: anchor '{anchor}' not found in the running order (skipped)")
            continue
        units.append(u)
        seq[pos + 1:pos + 1] = [(u["unit"], s) for s in unit_scenes(u)]

    # check the extended order against the outline (question cards and ch10q are new, ignored here)
    if cut == "extended" and cuts.get("extended", {}).get("scene_order"):
        ref = cuts["extended"]["scene_order"]
        got = [s["id"] for _, s in seq if s["id"] in set(ref)]
        refp = [x for x in ref if x in {s["id"] for _, s in seq}]
        if got != refp:
            warn("extended running order differs from plan/outline.json cuts.extended.scene_order: "
                 + ", ".join(f"{a}!={b}" for a, b in zip(got, refp) if a != b)[:400])

    voice = None
    vfile = os.path.join(ROOT, "audio", "voice.json" if LANG == "en" else f"voice_{LANG}.json")
    for u in units:
        v = u.get("voice") if LANG == "en" else ((u.get("_overlay") or {}).get("voice") or u.get(f"voice_{LANG}"))
        if v and voice and v.get("reference_id") != voice.get("reference_id"):
            err(f"unit {u['unit']}: voice {v.get('reference_id')} differs from {voice.get('reference_id')}")
        voice = voice or v
    if LANG != "en" and not voice:
        voice = next((u.get("voice") for u in units if u.get("voice")), None)
        if voice:
            warn(f"no voice_{LANG} in the overlays or scripts: the English voice {voice.get('reference_id')} is used")
    voice = dict(voice or {"provider": "fish", "model": "drama-3", "reference_id": None})
    if os.path.exists(vfile) and not opts.voice:
        ov = json.load(open(vfile))
        if ov.get("reference_id"):
            voice["reference_id"], voice["override"] = ov["reference_id"], rel(vfile)
    if opts.voice:
        voice["reference_id"], voice["override"] = opts.voice, "--voice"

    scenes, seen, sent_ids = [], set(), set()
    for un, sc in seq:
        if sc["id"] in seen:
            err(f"scene id {sc['id']} appears twice")
        seen.add(sc["id"])
        u = next(x for x in units if x["unit"] == un)
        r = resolve_scene(sc, u, opts)
        for p in r["paragraphs"]:
            for x in p["sentences"]:
                if x["id"] in sent_ids:
                    err(f"sentence id {x['id']} appears twice")
                sent_ids.add(x["id"])
        scenes.append(r)

    questions = [{"scene": s["id"], "unit": s["unit"], **s["question"]} for s in scenes if s.get("question")]
    if LANG != "en" and UNTRANSLATED:
        per = {}
        for un, k in UNTRANSLATED:
            per.setdefault(un, []).append(k)
        for un, ks in per.items():
            warn(f"unit {un}: {len(ks)} sentences not translated into {LANG} (English kept): "
                 + ", ".join(ks[:6]) + (" ..." if len(ks) > 6 else ""))
    film = {
        "schema": 2, "kind": "film", "name": name, "cut": cut,
        "title": outline.get("title"), "subtitle": outline.get("subtitle"),
        "built": datetime.datetime.now().isoformat(timespec="seconds"),
        "fps": 30, "lang": LANG, "voice": voice,
        "units": [{"unit": u["unit"], "title": u.get("title"), "level_range": u.get("level_range"),
                   "cut": u.get("cut"), "insert_after": u.get("insert_after"), "path": u["_path"], "sha": u["_sha"],
                   "scenes": [s["id"] for s in scenes if s["unit"] == u["unit"]]} for u in units],
        "scenes": scenes,
        "totals": {"scenes": len(scenes), "words": sum(s["words"] for s in scenes),
                   "estimated_s": round(sum(s["estimated_s"] for s in scenes), 1),
                   "status": {k: sum(1 for s in scenes if s["status"] == k) for k in ("ready", "pending", "provisional")},
                   "question_cards": len(questions)},
        "warnings": warnings, "errors": errors,
    }
    if LANG != "en":            # chapter names of the MP4 from the overlay's optional "title"; overlay provenance
        for fu, u in zip(film["units"], units):
            ov = u.get("_overlay") or {}
            fu.update(title_en=u.get("title"), title=ov.get("title") or u.get("title"),
                      overlay=ov.get("_path"), overlay_sha=ov.get("_sha"))
        film["totals"]["untranslated"] = len(UNTRANSLATED)
        film["untranslated"] = [k for _, k in UNTRANSLATED]
    out = os.path.join(ROOT, opts.out)
    os.makedirs(out, exist_ok=True)
    json.dump(film, open(os.path.join(out, f"film_{name}.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({"name": name, "questions": questions}, open(os.path.join(out, f"questions_{name}.json"), "w"),
              indent=1, ensure_ascii=False)
    t = film["totals"]
    print(f"[assemble] {name}: {len(units)} units, {t['scenes']} scenes, {t['words']} words, "
          f"~{t['estimated_s'] / 60:.1f} min estimated, status {t['status']}, {t['question_cards']} question cards"
          + (f", {t['untranslated']} sentences untranslated" if LANG != "en" else "")
          + f" -> {opts.out}/film_{name}.json")
    for w in warnings:
        print("[assemble] warning:", w)
    for e in errors:
        print("[assemble] ERROR:", e)
    if errors or (opts.strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
