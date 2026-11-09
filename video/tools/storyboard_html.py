#!/usr/bin/env python3
"""storyboard_html.py: assemble video/storyboard/<unit>.md into one review page (storyboard/storyboard.html).

Each plan is shown with the still of the v2 scene it reuses ("reprend <id>"), taken from the rendered
French extended film (storyboard/stills_v2/<id>.jpg), or with a "new shot" slate. Units follow the
extended-cut running order. Usage: python3 tools/storyboard_html.py
"""
import base64, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SB = os.path.join(ROOT, "storyboard")
STILLS = os.path.join(SB, "stills_v2")

tl = json.load(open(os.path.join(ROOT, "script/_build/extended_fr_timeline.json")))
order = []
for s in tl["scenes"]:
    if s["unit"] not in order:
        order.append(s["unit"])
if "ch10q" in order:              # v4: « Ouvertures » closes the film
    order.remove("ch10q"); order.append("ch10q")
cut = {u: json.load(open(os.path.join(ROOT, "script", u + ".json")))["cut"] for u in order}
still_ids = {f[:-4] for f in os.listdir(STILLS)}


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def block(lines):
    """Small markdown subset: paragraphs, lists, blockquotes (kept as <p> inside a .vo)."""
    out, para, lst = [], [], None
    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst:
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + "</ol>"); lst = None
    for ln in lines:
        s = ln.strip()
        m = re.match(r"^(\d+\.|[-*])\s+(.*)", s)
        if not s:
            flush()
        elif m:
            if para:
                flush()
            lst = (lst or []) + [m.group(2)]
        elif lst and ln.startswith("   "):
            lst[-1] += " " + s
        else:
            if lst:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


FIELDS = [("On voit", "see"), ("Animation", "anim"), ("Textes à l'écran", "text"), ("Voix off", "vo"),
          ("Note", "note"), ("Badge", "text")]


def parse_plan(head, lines):
    parts = [p.strip() for p in head.split("·")]
    pid, title = parts[0], parts[1] if len(parts) > 1 else ""
    rest = " · ".join(parts[2:])
    dur = re.search(r"≈\s*([\d\s,]+(?:min\s*\d*\s*s?|s)?)", rest)
    reuse = re.search(r"reprend\s+(.+)", rest)
    ids = re.findall(r"[A-Za-z0-9]+\.[A-Za-z0-9.\-]+", reuse.group(1)) if reuse else []
    still = next((i.rstrip(".") for i in ids if i.rstrip(".") in still_ids), None)
    fields, cur = {}, None
    for ln in lines:
        m = re.match(r"^\*\*(On voit|Animation|Textes à l'écran(?: \(EN\))?|Voix off|Note|Badge)\s*:\*\*\s*(.*)", ln.strip())
        if m:
            key = next(k for lab, k in FIELDS if m.group(1).startswith(lab))
            cur = key + ("_" + m.group(1) if key in fields else "")
            fields[cur] = [m.group(2)] if m.group(2) else []
            continue
        if cur:
            fields[cur].append(re.sub(r"^>\s?", "", ln) if ln.lstrip().startswith(">") else ln)
    return dict(id=pid, title=title, dur=dur.group(1).strip() if dur else "", reuse=reuse.group(1) if reuse else "",
                new="nouveau" in rest.lower() and not reuse, still=still, fields=fields, head_rest=rest)


def parse_unit(u):
    p = os.path.join(SB, u + ".md")
    if not os.path.exists(p):
        return None
    txt = open(p, encoding="utf-8").read().split("\n")
    title, intro, plans, foot, cur = "", [], [], [], None
    for ln in txt:
        if ln.startswith("# "):
            title = ln[2:].strip(); continue
        if ln.startswith("## "):
            cur = [ln[3:].strip(), []]; plans.append(cur); continue
        if ln.startswith("**Durée totale") or (foot and cur is None):
            cur = None; foot.append(ln); continue
        if cur is None:
            intro.append(ln)
        else:
            cur[1].append(ln)
    return dict(unit=u, title=title, intro=intro, plans=[parse_plan(h, l) for h, l in plans], foot=foot)


def img(sid):
    with open(os.path.join(STILLS, sid + ".jpg"), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def secs(d):
    m = re.match(r"(?:(\d+)\s*min)?\s*(?:(\d+)\s*s)?", d.strip())
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0) if m else 0


units = [x for x in (parse_unit(u) for u in order) if x]
rows, nav, summary = [], [], []
tot = {"core": 0, "ext": 0}
for U in units:
    u = U["unit"]
    m = re.search(r"\(≈\s*([^)]+)\)", U["title"])
    d = secs(m.group(1)) if m else 0
    tot["ext"] += d
    if cut[u] == "core":
        tot["core"] += d
    ttl = re.sub(r"\s*\(≈[^)]*\)", "", U["title"])
    label = ttl.split("·", 1)[-1].strip()
    summary.append(f'<tr><td class="mono"><a href="#u-{u}">{u}</a></td><td>{html.escape(label)}</td>'
                   f'<td>{"courte + longue" if cut[u]=="core" else "longue"}</td><td class="num">{m.group(1) if m else "?"}</td>'
                   f'<td class="num">{len(U["plans"])}</td></tr>')
    nav.append(f'<a href="#u-{u}" class="{"x" if cut[u]!="core" else ""}">{u}</a>')
    cards = []
    for P in U["plans"]:
        f = P["fields"]
        if P["still"]:
            frame = (f'<figure class="frame"><img src="{img(P["still"])}" alt="Image actuelle de la scène {P["still"]}" loading="lazy">'
                     f'<figcaption>image actuelle (v2 {html.escape(P["still"])}){(" · " + html.escape(P["reuse"].split(P["still"],1)[-1].strip(" ,;·"))) if P["reuse"].split(P["still"],1)[-1].strip(" ,;·") else ""}</figcaption></figure>')
        else:
            frame = (f'<figure class="frame slate"><div><span class="tag">{"nouveau plan" if not P["reuse"] else "plan modifié"}</span>'
                     f'{block(f.get("see", []))}</div><figcaption>{html.escape(P["reuse"] or "nouveau")}</figcaption></figure>')
        meta = "".join(f'<div class="f"><h4>{lab}</h4>{block(f[k])}</div>' for lab, k in
                       [("On voit", "see"), ("Animation", "anim"), ("Textes à l'écran (EN)", "text")] if f.get(k))
        extra = "".join(f'<div class="f"><h4>{html.escape(k.split("_",1)[1])}</h4>{block(v)}</div>'
                        for k, v in f.items() if "_" in k)
        note = f'<div class="note"><h4>Note</h4>{block(f["note"])}</div>' if f.get("note") else ""
        cards.append(f'''<article class="plan" id="p-{html.escape(P["id"])}">
  <header><span class="pid mono">{html.escape(P["id"])}</span><h3>{inline(P["title"])}</h3><span class="dur mono">≈ {html.escape(P["dur"])}</span></header>
  <div class="grid">{frame}
    <div class="vo"><h4>Voix off</h4>{block(f.get("vo", []))}</div></div>
  <details class="meta"><summary>Visuel et animation</summary><div class="fields">{meta}{extra}</div></details>{note}
</article>''')
    rows.append(f'''<section class="unit" id="u-{u}">
  <div class="uhead"><span class="mono ucode">{u}</span><h2>{html.escape(ttl.split("·",1)[-1].strip())}</h2>
    <span class="mono">{"version courte et longue" if cut[u]=="core" else "version longue seulement"} · ≈ {m.group(1) if m else "?"}</span></div>
  <div class="intro">{block(U["intro"])}</div>
  {"".join(cards)}
  <div class="foot">{block(U["foot"])}</div>
</section>''')

missing = [u for u in order if u not in {U["unit"] for U in units}]
fmt = lambda s: f"{s//60} min {s%60:02d} s"
page = open(os.path.join(HERE, "storyboard_template.html"), encoding="utf-8").read()
page = (page.replace("{{NAV}}", "".join(nav)).replace("{{SUMMARY}}", "".join(summary))
        .replace("{{CORE}}", fmt(tot["core"])).replace("{{EXT}}", fmt(tot["ext"]))
        .replace("{{NUNITS}}", str(len(units))).replace("{{NPLANS}}", str(sum(len(U["plans"]) for U in units)))
        .replace("{{MISSING}}", ("Unités pas encore écrites : " + ", ".join(missing)) if missing else "")
        .replace("{{UNITS}}", "\n".join(rows)))
out = os.path.join(SB, "storyboard.html")
open(out, "w", encoding="utf-8").write(page)
print(f"{out}: {len(units)} units, {sum(len(U['plans']) for U in units)} plans, {os.path.getsize(out)/1e6:.1f} MB, "
      f"core {fmt(tot['core'])}, extended {fmt(tot['ext'])}, missing {missing}")
