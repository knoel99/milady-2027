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

Usage
  python3 -I tools/assemble_cut.py --cut core|extended [--name N] [--units script] [--cuts plan/outline.json]
                                    [--voice REFERENCE_ID] [--variant auto|pending|result] [--strict]
  python3 -I tools/assemble_cut.py --unit ch04
Outputs script/_build/film_<name>.json and script/_build/questions_<name>.json (question register).
"""
import argparse, datetime, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTION_CARD_FILE = "scenes/_shared/question_card.html"   # default page of a question-card scene without "file"
RAW_WPM = 146.0          # measured raw pace of the Ethan voice incl. [long pause] (BRIEF D21)
LONG_PAUSE_S = 0.9       # silence standing for [long pause] between two paragraphs (see audio/tts.py)
EXTRA_UNITS = [{"unit": "ch10q", "before": "ch11"}]
MARK = re.compile(r"\{(u|b|param|model|metric)\}(.*?)\{/\}")
CUE_RE = re.compile(r"^[A-Za-z_][\w-]*$")

warnings, errors = [], []


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
                return str(v)
            if mod and mod.isdigit():
                return speak_number(float(v), int(mod))
            return speak_number(v)
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


def resolve_scene(sc, unit, opts):
    sid = sc["id"]
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
    if tgt and not sc.get("question") and abs(est - tgt) > 0.15 * tgt:
        warn(f"{sid}: about {est:.0f} s for {w} words, target {tgt} s +-15 % (BRIEF D21)")
    if sc.get("question") and not (5 <= est <= 11):
        warn(f"{sid}: question card about {est:.1f} s, the brief asks 6-10 s")
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
    return u


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
    ap.add_argument("--strict", action="store_true", help="missing units and lint warnings are errors")
    global OPTS
    OPTS = opts = ap.parse_args()
    if not opts.cut and not opts.unit:
        ap.error("--cut or --unit")
    units_dir = os.path.join(ROOT, opts.units)
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
    vfile = os.path.join(ROOT, "audio", "voice.json")
    for u in units:
        v = u.get("voice")
        if v and voice and v.get("reference_id") != voice.get("reference_id"):
            err(f"unit {u['unit']}: voice {v.get('reference_id')} differs from {voice.get('reference_id')}")
        voice = voice or v
    voice = dict(voice or {"provider": "fish", "model": "drama-3", "reference_id": None})
    if os.path.exists(vfile) and not opts.voice:
        ov = json.load(open(vfile))
        if ov.get("reference_id"):
            voice["reference_id"], voice["override"] = ov["reference_id"], "audio/voice.json"
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
    film = {
        "schema": 2, "kind": "film", "name": name, "cut": cut,
        "title": outline.get("title"), "subtitle": outline.get("subtitle"),
        "built": datetime.datetime.now().isoformat(timespec="seconds"),
        "fps": 30, "voice": voice,
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
    out = os.path.join(ROOT, opts.out)
    os.makedirs(out, exist_ok=True)
    json.dump(film, open(os.path.join(out, f"film_{name}.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({"name": name, "questions": questions}, open(os.path.join(out, f"questions_{name}.json"), "w"),
              indent=1, ensure_ascii=False)
    t = film["totals"]
    print(f"[assemble] {name}: {len(units)} units, {t['scenes']} scenes, {t['words']} words, "
          f"~{t['estimated_s'] / 60:.1f} min estimated, status {t['status']}, {t['question_cards']} question cards"
          f" -> {opts.out}/film_{name}.json")
    for w in warnings:
        print("[assemble] warning:", w)
    for e in errors:
        print("[assemble] ERROR:", e)
    if errors or (opts.strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
