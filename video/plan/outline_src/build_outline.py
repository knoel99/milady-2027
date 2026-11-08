#!/usr/bin/env python3
"""Build outline.json and outline.md from outline_data.py (version 2), with totals, status counts and checks.

Usage: python3 -I outline_src/build_outline.py   (run from anywhere; paths are absolute)
Version 1 of this script and of its outputs is kept in outline_src/v1/.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import outline_data as D  # noqa: E402

VP = os.path.dirname(HERE)
SITE = "/home/user/milady-2027"
PROTO = os.path.join(VP, "proto")
FPS_CLASS = {"flat": 44.18, "dense2d": 7.46, "webgl": 4.09}  # measured 1080p30 throughput (pipeline.md §7)
WPM = 150.0
WPM_EFFECTIVE = 130.0
PAUSE_S = 1.5
VERSION = "2026-11-08 (v2, after review)"
LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5"]


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def path_exists(p):
    p = p.split("#")[0].strip()
    if p.startswith("proto/"):
        return os.path.exists(os.path.join(VP, p))
    if p.startswith("data/"):
        return os.path.exists(os.path.join(PROTO, p))
    return os.path.exists(os.path.join(SITE, p))


def words(t):
    t = re.sub(r"\[[^\]]*\]", " ", t)
    return len(re.findall(r"[A-Za-z0-9'\-]+", t))


def narration_stats(text):
    w = words(text)
    pauses = text.count("[long pause]")
    return {"words": w, "long_pauses": pauses,
            "est_seconds_at_150wpm": round(w / WPM * 60 + pauses * PAUSE_S, 1),
            "est_seconds_at_130wpm_effective": round(w / WPM_EFFECTIVE * 60 + pauses * PAUSE_S, 1)}


def render_s(scene, dur=None):
    return (dur if dur is not None else scene["duration_s"]) * 30 / FPS_CLASS[scene["render_class"]]


def main():
    core, modules = D.CORE, D.MODULES
    problems = []
    parent, scene_by_id = {}, {}
    for unit in core + modules:
        for s in unit["scenes"]:
            if s["id"] in scene_by_id:
                problems.append(f"duplicate scene id {s['id']}")
            scene_by_id[s["id"]] = s
            parent[s["id"]] = unit["id"]
    unit_by_id = {u["id"]: u for u in core + modules}

    # ---- per-scene checks
    for s in scene_by_id.values():
        for a in s["assets"]:
            if not path_exists(a):
                problems.append(f"{s['id']}: asset not found: {a}")
        for d in s["data"]:
            if not path_exists(d) and s["status"] == "READY":
                problems.append(f"{s['id']}: READY scene with missing data: {d}")
        if s["status"] != "READY" and not s["regen"]:
            problems.append(f"{s['id']}: {s['status']} without regeneration hook")
        if s["status"] == "READY" and s["regen"]:
            problems.append(f"{s['id']}: READY with a regeneration hook")
        if s["status"] == "PENDING" and s["duration_result_s"] < s["duration_s"]:
            problems.append(f"{s['id']}: result variant shorter than the pending variant")
        ev = s["extended_variant"]
        if ev and ev.get("skip"):
            for r in ev["replaced_by"]:
                if r not in scene_by_id:
                    problems.append(f"{s['id']}: replaced_by unknown scene {r}")
    for m in modules:
        if m["insert_after"] not in scene_by_id and m["insert_after"] not in unit_by_id:
            problems.append(f"{m['id']}: unknown anchor {m['insert_after']}")

    # ---- unit totals
    for u in core + modules:
        u["target_duration_s"] = sum(s["duration_s"] for s in u["scenes"])
        u["target_duration_result_s"] = sum(s["duration_result_s"] for s in u["scenes"])
        u["target_duration"] = mmss(u["target_duration_s"])
        u["status_counts"] = {k: sum(1 for s in u["scenes"] if s["status"] == k) for k in ("READY", "PROVISIONAL", "PENDING")}

    # ---- running orders
    core_order = [s["id"] for c in core for s in c["scenes"]]

    def modules_after(anchor):
        out = []
        for m in modules:
            if m["insert_after"] == anchor:
                out.append(m)
        return out

    ext_items = []  # (scene_id, played_id, duration_now, duration_result)

    def add_modules(anchor):
        for m in modules_after(anchor):
            for s in m["scenes"]:
                ext_items.append((s["id"], s["id"], s["duration_s"], s["duration_result_s"]))
            add_modules(m["id"])

    for c in core:
        for s in c["scenes"]:
            ev = s["extended_variant"]
            if ev and ev.get("skip"):
                pass
            elif ev:
                ext_items.append((s["id"], ev["id"], ev["duration_s"], ev["duration_s"]))
            else:
                ext_items.append((s["id"], s["id"], s["duration_s"], s["duration_result_s"]))
            add_modules(s["id"])
        add_modules(c["id"])
    played = [x[0] for x in ext_items]
    for m in modules:
        for s in m["scenes"]:
            if s["id"] not in played:
                problems.append(f"{s['id']}: extension scene never placed in the extended cut")

    # segments of the extended running order
    segments = []
    for sid, pid, dn, dr in ext_items:
        p = parent[sid]
        if segments and segments[-1]["unit"] == p:
            segments[-1]["scenes"].append(pid)
            segments[-1]["duration_s"] += dn
        else:
            segments.append({"unit": p, "scenes": [pid], "duration_s": dn})
    for g in segments:
        u = unit_by_id[g["unit"]]
        g["label"] = u["id"] if len(g["scenes"]) == len(u["scenes"]) else f"{u['id']} ({g['scenes'][0]}-{g['scenes'][-1]})" \
            if len(g["scenes"]) > 1 else f"{u['id']} ({g['scenes'][0]})"
        g["duration"] = mmss(g["duration_s"])

    # ---- cut totals
    def cut_stats(items):
        st = {"scenes": 0, "READY": 0, "PROVISIONAL": 0, "PENDING": 0, "duration_s": 0, "duration_result_s": 0, "render_s": 0.0,
              "level_s": {k: 0 for k in LEVELS}}
        for sid, pid, dn, dr in items:
            s = scene_by_id[sid]
            st["scenes"] += 1
            st[s["status"]] += 1
            st["duration_s"] += dn
            st["duration_result_s"] += dr
            st["render_s"] += render_s(s, dn)
            st["level_s"][s["level"]] += dn
        st["duration"] = mmss(st["duration_s"])
        st["duration_with_results"] = mmss(st["duration_result_s"])
        st["render_estimate_h_1080p30"] = round(st["render_s"] / 3600, 2)
        st["render_s"] = round(st["render_s"])
        st["level_time"] = {k: mmss(v) for k, v in st["level_s"].items()}
        return st

    core_items = [(s["id"], s["id"], s["duration_s"], s["duration_result_s"]) for c in core for s in c["scenes"]]
    mod_items = [(s["id"], s["id"], s["duration_s"], s["duration_result_s"]) for m in modules for s in m["scenes"]]
    cs, ms, es = cut_stats(core_items), cut_stats(mod_items), cut_stats(ext_items)

    # ---- predict beats in film order
    def predicts(order):
        out = []
        for sid in order:
            p = scene_by_id[sid]["predict"]
            if p:
                out.append({"scene": sid, "q": p.split(":")[0]})
        return out

    core_pred = predicts(core_order)
    for i, p in enumerate(core_pred, 1):
        if p["q"] != f"Q{i}":
            problems.append(f"predict beats out of order: {p['scene']} is {p['q']}, expected Q{i}")

    # ---- two episodes, results update
    te = D.TWO_EPISODES
    p1 = sum(unit_by_id[c]["target_duration_s"] for c in te["part1"])
    first_p2 = unit_by_id[te["part2"][0]]["scenes"][0]["id"]
    idx = played.index(first_p2)
    p2_ext = te["part2_recap_s"] + sum(x[2] for x in ext_items[idx:])
    p2_core = te["part2_recap_s"] + sum(unit_by_id[c]["target_duration_s"] for c in te["part2"])
    ru = D.RESULTS_UPDATE
    ru_s = ru["recap_s"] + sum(scene_by_id[s]["duration_result_s"] for s in ru["scenes"])

    # ---- regenerable index
    regen_index = []
    for sid in played + [s for s in core_order if s not in played]:
        s = scene_by_id[sid]
        if s["regen"]:
            r = s["regen"]
            regen_index.append({"scene": s["id"], "title": s["title"], "unit": parent[sid],
                                "cut": "core" if unit_by_id[parent[sid]]["cut"] == "core" else "extension",
                                "status": s["status"], "scene_data": r["scene_data"],
                                "exists_now": all(path_exists(x.strip()) for x in r["scene_data"].split("+")),
                                "duration_now_s": s["duration_s"], "duration_result_s": s["duration_result_s"],
                                "provisional_run": r["provisional_run"], "final_run": r["final_run"], "requires": r["requires"]})

    # ---- version-1 comparison
    v1 = None
    v1p = os.path.join(HERE, "v1", "outline.json")
    if os.path.exists(v1p):
        with open(v1p) as f:
            o1 = json.load(f)
        v1 = {"core": o1["cuts"]["core"]["duration"], "core_scenes": o1["cuts"]["core"]["scenes"],
              "extended": o1["cuts"]["extended"]["duration"], "scenes": o1["cuts"]["core"]["scenes"] + o1["cuts"]["extensions"]["scenes"],
              "status": o1["status_counts"]}

    status_all = {k: sum(1 for s in scene_by_id.values() if s["status"] == k) for k in ("READY", "PROVISIONAL", "PENDING")}
    change_counts = {}
    for c in D.CHANGES:
        change_counts.setdefault(c["review"], {}).setdefault(c["outcome"], 0)
        change_counts[c["review"]][c["outcome"]] += 1

    out = {
        "title": D.TITLE, "subtitle": D.SUBTITLE, "title_options": D.TITLE_OPTIONS,
        "version": VERSION, "language": "en", "status": "outline v2 (reviews applied; to be validated by the user)",
        "logline": D.LOGLINE, "synopsis": D.SYNOPSIS,
        "logline_synopsis_words": words(D.LOGLINE) + words(D.SYNOPSIS),
        "conventions": {
            "levels": {"L0": "anyone", "L1": "curious high school / early undergraduate", "L2": "science undergraduate",
                       "L3": "M1 physics or ML", "L4": "M2 / early PhD", "L5": "supervisors and specialists"},
            "status": {"READY": "all data exist, or are computed at build time with no external run (repository results, site assets, "
                                "live integrations, random-weight decoder)",
                       "PROVISIONAL": "a reduced or CPU run can produce the data now; replaced later by the HPC result",
                       "PENDING": "needs HPC, GPU or consortium results; ships now as an 'empty seat' (READY anchor + bet + criterion)"},
            "durations": "duration_s = as shipped now (pending variant / provisional data); duration_result_s = with final data; "
                         f"targets assume about {int(WPM_EFFECTIVE)} effective words per minute (speech at about {int(WPM)} + visual breathing room)",
            "registers": {"NIGHT": "#0B0F14, default", "PAPER": "#F4F1EA, derivations", "BLUEPRINT": "dark + grey grid, infrastructure"},
            "render_class": {k: f"{v} frames/s measured at 1080p30 on 4 cores" for k, v in FPS_CLASS.items()},
            "colour_key_night": {"param": "#1BAF7A", "u": "#3987E5", "B": "#EB6834", "model": "#B49CF0", "metric": "#EDA100",
                                 "infra": "#6B7A8C"},
            "paths": {"assets_and_data": SITE + " (read-only)", "proto/...": PROTO, "data/...": PROTO + "/data (scene data written by tools/extract_data.py)"},
            "run_env": D.RUNENV,
            "pending_device": "empty seat: READY anchor visual, dashed chart frame, labelled axes, shaded success band, data tag; two narration variants (pending / result); vary the frame type (curve, map, lamp panel, gauge)",
            "symbols": D.SYMBOLS,
        },
        "cuts": {
            "core": {"chapters": [c["id"] for c in core], **cs},
            "extensions": {"modules": [m["id"] for m in modules], **ms},
            "extended": {"running_order": [g["label"] for g in segments], "segments": segments, "scene_order": [x[1] for x in ext_items], **es},
            "two_episode_option": {"part1": {"chapters": te["part1"], "duration": mmss(p1)},
                                   "part2": {"chapters": te["part2"], "recap_s": te["part2_recap_s"],
                                             "duration_with_extensions": mmss(p2_ext), "duration_core_only": mmss(p2_core)},
                                   "note": te["note"]},
            "results_update_episode": {"scenes": ru["scenes"], "recap_s": ru["recap_s"], "duration": mmss(ru_s), "note": ru["note"]},
        },
        "status_counts": status_all,
        "predict_beats_core_order": core_pred,
        "chapters": core, "modules": modules,
        "narration_drafts": {
            "opening": {**D.OPENING, **narration_stats(D.OPENING["tts_text"])},
            "closing": {**D.CLOSING, **narration_stats(D.CLOSING["tts_text"])},
            "tts_settings": "Fish Audio drama-3, temperature 0.1, prosody.speed 1.0, one acting cue at the start, [long pause] only "
                            "between paragraphs; predict holds via hold_after (production notes)",
        },
        "regenerable_index": regen_index,
        "production_notes": D.NOTES,
        "changes_after_review": {"counts": change_counts, "version_1": v1, "items": D.CHANGES},
        "questions_for_user": D.QUESTIONS,
        "checks": {"problems": problems},
    }
    with open(os.path.join(VP, "outline.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(os.path.join(VP, "outline.md"), "w") as f:
        f.write(render_md(out, unit_by_id, scene_by_id))
    print(json.dumps({"core": {k: cs[k] for k in ("duration", "duration_with_results", "scenes", "READY", "PROVISIONAL", "PENDING", "render_estimate_h_1080p30", "level_time")},
                      "modules": {k: ms[k] for k in ("duration", "duration_with_results", "scenes", "READY", "PROVISIONAL", "PENDING")},
                      "extended": {k: es[k] for k in ("duration", "duration_with_results", "scenes", "READY", "PROVISIONAL", "PENDING", "render_estimate_h_1080p30", "level_time")},
                      "two_episodes": out["cuts"]["two_episode_option"], "results_update": mmss(ru_s),
                      "opening": out["narration_drafts"]["opening"]["words"], "closing": out["narration_drafts"]["closing"]["words"],
                      "logline_synopsis_words": out["logline_synopsis_words"], "changes": change_counts, "v1": v1,
                      "predicts": core_pred, "problems": problems}, indent=1, ensure_ascii=False))


def code(p):
    return f"`{p}`"


def dur_label(s):
    if s["duration_result_s"] != s["duration_s"]:
        return f"{s['duration_s']} s now / {s['duration_result_s']} s with results"
    return f"{s['duration_s']} s"


def render_scene(s):
    L = []
    was = f" · was {s['was']}" if s["was"] else ""
    L.append(f"#### {s['id']} {s['title']}  \n`{s['level']}` · {dur_label(s)} · **{s['status']}** · {s['register']} · "
             f"render {s['render_class']}{was}")
    L.append("")
    L.append(f"- **Key idea.** {s['key_idea']}")
    L.append(f"- **Visual.** {s['visual']}")
    L.append(f"- **On screen.** {s['on_screen']}")
    if s.get("predict"):
        L.append(f"- **Predict beat.** {s['predict']}")
    if s["motifs"]:
        L.append(f"- **Motifs.** {', '.join(s['motifs'])}")
    L.append(f"- **Assets.** {', '.join(code(a) for a in s['assets']) if s['assets'] else 'none (new animation)'}")
    L.append(f"- **Data.** {', '.join(code(d) for d in s['data']) if s['data'] else 'none'}")
    if s["depends_on"]:
        L.append(f"- **Re-render when these change.** {', '.join(code(d) for d in s['depends_on'])}")
    ev = s["extended_variant"]
    if ev:
        if ev.get("skip"):
            L.append(f"- **Extended cut.** Skipped; {', '.join(ev['replaced_by'])} play in full instead.")
        else:
            L.append(f"- **Extended cut.** Replaced by the entry `{ev['id']}` ({ev['duration_s']} s): {ev['note']}.")
    if s["flags"]:
        L.append(f"- **Flags.** {'; '.join(s['flags'])}")
    if s["sources"]:
        L.append(f"- **Sources.** {', '.join(s['sources'])}")
    if s["regen"]:
        r = s["regen"]
        L.append("- **Regeneration hook.**")
        L.append(f"  - scene data: {code(r['scene_data'])}")
        L.append(f"  - upstream: {r['upstream']}")
        if r["provisional_run"]:
            L.append(f"  - provisional run (now, CPU): {r['provisional_run']}")
        L.append(f"  - final run: {r['final_run']}")
        if r["requires"]:
            L.append(f"  - requires: {'; '.join(r['requires'])}")
        L.append(f"  - extractor: {r['extractor']}")
        if r.get("criterion"):
            L.append(f"  - criterion: {r['criterion']}")
        L.append(f"  - ships now as: {r['shippable_now']}")
        L.append(f"  - narration: {r['narration']}")
    L.append("")
    return "\n".join(L)


def render_unit(u):
    L = []
    where = "" if u["cut"] == "core" else f" · inserted after {u['insert_after']}"
    L.append(f"### {u['id']}. {u['title']}")
    L.append("")
    sc = u["status_counts"]
    res = f" ({mmss(u['target_duration_result_s'])} with results)" if u["target_duration_result_s"] != u["target_duration_s"] else ""
    L.append(f"`{u['levels']}` · {u['target_duration']}{res}{where} · was {u['was']} · "
             f"{len(u['scenes'])} scenes: {sc['READY']} READY, {sc['PROVISIONAL']} PROVISIONAL, {sc['PENDING']} PENDING")
    L.append("")
    L.append(f"- **Learning goal.** {u['learning_goal']}")
    L.append(f"- **Takeaway (one sentence).** {u['takeaway']}")
    L.append("")
    for s in u["scenes"]:
        L.append(render_scene(s))
    return L


def render_md(o, unit_by_id, scene_by_id):
    c = o["cuts"]
    co, ex, ext = c["core"], c["extensions"], c["extended"]
    L = []
    L.append(f"# Chaptered outline: {o['title']}")
    L.append("")
    L.append(f"*{o['subtitle']}.* Long English explainer about the MilaDy 2027 site. Outline version {o['version']}, "
             f"generated from `outline_src/outline_data.py` by `outline_src/build_outline.py` (the same data as `outline.json`). "
             f"This version applies the accuracy review (`critique_accuracy.md`) and the pedagogy and production review "
             f"(`critique_pedagogy.md`); every change is listed in section 9 and version 1 is kept in `outline_src/v1/`. "
             f"Sources: `inventory.md`, `pedagogy.md`, `styles.md`, `pipeline.md` and the site under `/home/user/milady-2027/en/`. "
             f"Source references use the inventory's abbreviations (R report, T thesis proposal, S supervisors, C computing, H home, "
             f"P3/P4 prep modules 3/4, D digest, X experiments page, IR infra README, CFG configs). Ids: chapters ch00-ch11, "
             f"core scenes NN.k, extension scenes X…; each scene shows its version-1 id ('was').")
    L.append("")
    L.append("## 0. At a glance")
    L.append("")
    L.append("| Cut | Units | Duration now | With all results | Scenes | READY | PROVISIONAL | PENDING | Render estimate, 1080p30, 4 cores |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    L.append(f"| Core cut | {', '.join(co['chapters'])} | **{co['duration']}** | {co['duration_with_results']} | {co['scenes']} | {co['READY']} | {co['PROVISIONAL']} | {co['PENDING']} | {co['render_estimate_h_1080p30']} h |")
    L.append(f"| Extension modules | {', '.join(ex['modules'])} | **{ex['duration']}** | {ex['duration_with_results']} | {ex['scenes']} | {ex['READY']} | {ex['PROVISIONAL']} | {ex['PENDING']} | {ex['render_estimate_h_1080p30']} h |")
    L.append(f"| Extended cut (core + modules; 10.8 skipped, 10.9 as bridge) | see section 3 | **{ext['duration']}** | {ext['duration_with_results']} | {ext['scenes']} | {ext['READY']} | {ext['PROVISIONAL']} | {ext['PENDING']} | {ext['render_estimate_h_1080p30']} h |")
    L.append("")
    t2 = c["two_episode_option"]
    L.append(f"Two-episode option: Part 1 = {', '.join(t2['part1']['chapters'])} ({t2['part1']['duration']}, L0 to L4); "
             f"Part 2 = {t2['part2']['recap_s']}-s recap + {', '.join(t2['part2']['chapters'])} + all modules "
             f"({t2['part2']['duration_with_extensions']}; {t2['part2']['duration_core_only']} without modules). {t2['note']}")
    L.append("")
    ru = c["results_update_episode"]
    L.append(f"Results update episode (when the HPC results arrive): {ru['duration']} with every result in. {ru['note']}")
    L.append("")
    L.append("Time per level (as shipped now):")
    L.append("")
    L.append("| Cut | " + " | ".join(LEVELS) + " |")
    L.append("|---|" + "---|" * len(LEVELS))
    L.append("| Core | " + " | ".join(co["level_time"][k] for k in LEVELS) + " |")
    L.append("| Extended | " + " | ".join(ext["level_time"][k] for k in LEVELS) + " |")
    L.append("")
    L.append("Render estimates use the measured throughput per scene class (flat 44 fps, dense 2D 7.5 fps, WebGL 4.1 fps) and "
             "exclude narration and assembly (a few minutes). Durations are targets; final durations come from the narration audio.")
    L.append("")
    L.append("## 1. Logline and synopsis")
    L.append("")
    L.append(f"**Logline.** {o['logline']}")
    L.append("")
    L.append(f"**Synopsis.** {o['synopsis']}")
    L.append("")
    L.append(f"({o['logline_synopsis_words']} words.)")
    L.append("")
    L.append("## 2. Conventions")
    L.append("")
    cv = o["conventions"]
    L.append("- **Levels.** " + "; ".join(f"{k}: {v}" for k, v in cv["levels"].items()) + ". "
             "An altitude rail on the left edge shows the level at chapter cards and checkpoints only (3 s). The climb only goes up, "
             "except in the closing; the one declared side-step is the ch08 chapter card ('new test bench', L4 -> L3). Extension "
             "modules are asides: the rail marks them and returns.")
    L.append("- **Status.** " + "; ".join(f"**{k}**: {v}" for k, v in cv["status"].items()) + ".")
    L.append(f"- **Durations.** {cv['durations']}.")
    L.append("- **Pending device.** Each PENDING scene is an *empty seat*: " + cv["pending_device"].split(": ", 1)[1] +
             ". It is shippable. The hatched AWAITING preview of the pipeline is for drafts only.")
    L.append("- **Formula layer.** Exact values and statements that the ladder does not allow in narration sit on a separate "
             "formula layer (small type, never in subtitles, never narrated) (decision D8).")
    L.append("- **Colour key (NIGHT values).** green `#1BAF7A` control parameter, blue `#3987E5` velocity u, vermillion `#EB6834` "
             "magnetic field B, violet `#B49CF0` generative model, amber `#EDA100` distribution-level metrics, grey `#6B7A8C` "
             "infrastructure. On PAPER: the site values `#009E73`, `#0072B2`, `#D55E00`, `#6C4BA0`, `#E69F00`. Matter is grey. "
             "Polarity is a shade of vermillion, never a new hue.")
    L.append("- **Paths.** Assets and data are relative to `/home/user/milady-2027` (read-only) unless they start with `proto/` "
             f"(`{PROTO}`) or `data/` (scene data files written by `tools/extract_data.py` into `{PROTO}/data`).")
    L.append(f"- **Run environment for every regeneration run.** {cv['run_env']}")
    L.append("- **Motifs** (M1 needle and flip, M2 knob, M3 two inks, M4 violet cloud, M5 amber histogram, M6 projector, "
             "M7 staircase, M8 altitude rail, M9 pen, M10 mirror) and transitions (T1 morph, T2 scale dive, T3 ink change, "
             "T4 chapter card, T5 hard cut, T6 equation morph) follow `styles.md` §3.5-3.6. Every chapter opens with T4. The corner "
             "needle (M1) shows only while the dipole D is on screen. Recurring devices: the two shelves (07.1 -> 08.6), the "
             "shoebox (04.6 -> 06.4), the toll counter (05.1 -> 09.1), the three promise cards (03.7 -> 05.3, 08.6, 09.1).")
    L.append("- **Symbol sheet** (one meaning per mark; lint the script against it):")
    for s in cv["symbols"]:
        L.append(f"  - {s}")
    L.append("")
    L.append("## 3. Running order")
    L.append("")
    L.append("Extended cut, segment by segment. Rows marked *core* make up the core cut on their own (in the core cut, 10.8 plays "
             "and 10.9 runs at full length).")
    L.append("")
    L.append("| # | Segment | Cut | Title | Levels | Duration (extended) | Takeaway |")
    L.append("|---|---|---|---|---|---|---|")
    for i, g in enumerate(ext["segments"], 1):
        u = unit_by_id[g["unit"]]
        cut = "core" if u["cut"] == "core" else f"ext. (after {u['insert_after']})"
        L.append(f"| {i} | {g['label']} | {cut} | {u['title']} | {u['levels']} | {g['duration']} | {u['takeaway']} |")
    L.append("")
    L.append("Core chapters on their own:")
    L.append("")
    L.append("| Id | Chapter | Levels | Duration now | With results | Scenes | R / P / N | Was |")
    L.append("|---|---|---|---|---|---|---|---|")
    for ch in o["chapters"]:
        sc = ch["status_counts"]
        L.append(f"| {ch['id']} | {ch['title']} | {ch['levels']} | {ch['target_duration']} | {mmss(ch['target_duration_result_s'])} | "
                 f"{len(ch['scenes'])} | {sc['READY']} / {sc['PROVISIONAL']} / {sc['PENDING']} | {ch['was']} |")
    L.append("")
    L.append("Predict beats in film order: " + ", ".join(f"{p['q']} ({p['scene']})" for p in o["predict_beats_core_order"]) + ".")
    L.append("")
    nd = o["narration_drafts"]
    L.append("## 4. Narration drafts: the first and the last minute")
    L.append("")
    L.append(f"Written for TTS ({nd['tts_settings']}). Short sentences; `[long pause]` only between paragraphs.")
    L.append("")
    for key, label in [("opening", "Opening"), ("closing", "Closing")]:
        b = nd[key]
        L.append(f"### {label} (scenes {', '.join(b['scenes'])})")
        L.append("")
        L.append(f"{b['words']} words, {b['long_pauses']} long pauses: about {b['est_seconds_at_150wpm']} s at 150 words per minute, "
                 f"{b['est_seconds_at_130wpm_effective']} s at 130 effective words per minute.")
        L.append("")
        L.append("```text")
        L.append(b["tts_text"].replace(" [long pause] ", " [long pause]\n\n"))
        L.append("```")
        L.append("")
        if b.get("variant_results_in"):
            L.append(f"Results-in variant: {b['variant_results_in']}")
            L.append("")
        L.append("Cue map: " + "; ".join(f"\"{a}\" → {b2}" for a, b2 in b["cue_map"]) + ".")
        L.append("")
        L.append(f"Note: {b['notes']}")
        L.append("")
    L.append("## 5. Core cut: chapters and scenes")
    L.append("")
    for ch in o["chapters"]:
        L.extend(render_unit(ch))
    L.append("## 6. Extension modules")
    L.append("")
    L.append("Each module is self-contained and slots in after its anchor (a scene or another module); the core cut never refers "
             "to them. Order of appearance in the extended cut: " + " → ".join(
                 g["label"] for g in ext["segments"] if unit_by_id[g["unit"]]["cut"] != "core") + ".")
    L.append("")
    ext_order = []
    for g in ext["segments"]:
        if unit_by_id[g["unit"]]["cut"] != "core" and g["unit"] not in ext_order:
            ext_order.append(g["unit"])
    for mid in ext_order:
        L.extend(render_unit(unit_by_id[mid]))
    L.append("## 7. Regenerable sections index")
    L.append("")
    L.append("| Scene | Cut | Status | Scene data | Exists now | Now / with results | Provisional run (CPU, now) | Final run | Requires |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in o["regenerable_index"]:
        L.append(f"| {r['scene']} {r['title']} | {r['cut']} | {r['status']} | `{r['scene_data']}` | {'yes' if r['exists_now'] else 'no'} | "
                 f"{r['duration_now_s']} s / {r['duration_result_s']} s | {r['provisional_run'] or 'none'} | {r['final_run']} | "
                 f"{'; '.join(r['requires']) or '-'} |")
    L.append("")
    L.append("Cheapest-first order for the provisional runs: X5.4 X-points (minutes) → X4.2 Rice levels (minutes) → 10.3 / X5.3 "
             "palier1 sweep (~30 min) → 10.5 Taylor-Green 32^3 subset with stationarity flags (~1-1.5 h, estimate) → 10.4 ABC at "
             "48^3 near the thresholds (hours, unmeasured: time one point first) → X4.5 E1 with three seeds (~3-4.5 h). CPU times "
             "marked 'estimate' are extrapolations from solver benchmarks; none of these runs has been launched. 10.6 needs no run "
             "(random-weight decoder computed at build time).")
    L.append("")
    L.append("## 8. Production notes")
    L.append("")
    for n in o["production_notes"]:
        L.append(f"- {n}")
    L.append("")
    if o["checks"]["problems"]:
        L.append("### Build checks")
        L.append("")
        for p in o["checks"]["problems"]:
            L.append(f"- {p}")
        L.append("")
    # ---- changes after review
    ca = o["changes_after_review"]
    L.append("## 9. Changes after review")
    L.append("")
    v1 = ca["version_1"]
    if v1:
        L.append(f"**In numbers.** Version 1: core cut {v1['core']} ({v1['core_scenes']} scenes), extended cut {v1['extended']}, "
                 f"{v1['scenes']} scenes ({v1['status']['READY']} READY, {v1['status']['PROVISIONAL']} PROVISIONAL, "
                 f"{v1['status']['PENDING']} PENDING). Version 2: core cut {co['duration']} now, {co['duration_with_results']} with "
                 f"results ({co['scenes']} scenes), extended cut {ext['duration']} now, {ext['duration_with_results']} with results, "
                 f"{co['scenes'] + ex['scenes']} scenes defined ({o['status_counts']['READY']} READY, {o['status_counts']['PROVISIONAL']} "
                 f"PROVISIONAL, {o['status_counts']['PENDING']} PENDING), of which the extended cut plays {ext['scenes']} "
                 f"(10.8 is replaced there by X6.1-X6.2).")
        L.append("")
    cnt = ca["counts"]
    L.append("**Outcome counts.** " + "; ".join(
        f"{rv} review: " + ", ".join(f"{n} {k}" for k, n in sorted(v.items())) for rv, v in cnt.items()) + ".")
    L.append("")
    L.append("**How the accuracy review was checked.** Each item was verified against the cited site lines, configs, code or "
             "result files before it was applied (the note says what was checked). No item was found wrong in substance. Two "
             "carried a wrong detail, corrected here: A8 cites T:992, which is about the variance of the stationarity loss, but the "
             "concern stands on the Taylor-Green config alone; C13 says `ref|0.9` holds 4,000 points, but it holds 8,000 (about 21 "
             "in the Rice strip), and the cache has no 20,000-sample reference set. One item (B15) exposed an inconsistency in the "
             "site itself (P3:1167 vs P3:1202), raised as question D19; the site was not modified.")
    L.append("")
    L.append("**Structural changes.**")
    L.append("")
    L.append("- Ids renamed: chapters ch00-ch11 (no collision with the report's classes C1-C4), core scenes NN.k; each scene keeps 'was'.")
    L.append("- Hook: the needle flips at about 7 s, the two questions arrive at about 0:34; the opening narration fits the scene budgets.")
    L.append("- Old C2 and C3 interleaved so the ladder climbs: ch02 (race, Rm, sodium, three tanks, VKS flips; all L1), ch03 "
             "(equation, windows, knob panel, the question; all L2). The disclaimer card became a lower-third inside 03.7.")
    L.append("- Old C7 split in two chapters, known system first: ch07 'The mirror and the crowd' (E1, opens with the lopsided "
             "machine moved from C6), ch08 'Fields have stricter laws' (E2, opens with the new scene 08.1 that introduces the 2D "
             "test bench). The taxonomy shelves start empty and become the payoff (08.6).")
    L.append("- ch10: 10.6 'What is guaranteed' is READY (no longer a fake bet); new READY core scene 10.8 'Walls and iron' (L5); "
             "10.3 shortened to 15 s; every seat has a READY anchor and two durations.")
    L.append("- Extensions re-anchored at scene level so the ladder only climbs: X2 → X3a after ch08; X4a after ch09; X5a → X1 "
             "after 10.3; X4b after 10.5; X3b after 10.7; X6 → X5b after 10.9 (bridge). X1.4 moved to X6.0; new X3.0 holds the "
             "distance formula.")
    L.append("- Release model for pending results: a stand-alone 'Results update' episode plus a v2 of the film; the closing has "
             "a results-in variant.")
    L.append("")
    for rv, label in [("accuracy", "Accuracy review (`critique_accuracy.md`)"), ("pedagogy", "Pedagogy and production review (`critique_pedagogy.md`)")]:
        L.append(f"### {label}")
        L.append("")
        L.append("| Item | Where (v2 ids) | Outcome | What was checked or changed |")
        L.append("|---|---|---|---|")
        for it in ca["items"]:
            if it["review"] == rv:
                L.append(f"| {it['item']} | {it['where']} | {it['outcome']} | {it['note']} |")
        L.append("")
    L.append("### Rejected, modified or partly applied, and why")
    L.append("")
    others = [it for it in ca["items"] if it["outcome"] != "applied"]
    if not any(it["outcome"] == "rejected" for it in ca["items"]):
        L.append("No item was rejected outright. These were applied differently:")
        L.append("")
    for it in others:
        L.append(f"- **{it['review']} {it['item']}** ({it['outcome']}): {it['note']}")
    L.append("")
    L.append("### Id map, version 1 → version 2")
    L.append("")
    for u in o["chapters"] + o["modules"]:
        L.append(f"- **{u['id']}**: " + ", ".join(f"{s['id']} ← {s['was']}" for s in u["scenes"]))
    L.append("")
    # ---- questions
    L.append("## 10. Questions for the user")
    L.append("")
    L.append("Decisions that remain open. Each has a default that the production will follow if you say nothing.")
    L.append("")
    for d in o["questions_for_user"]:
        L.append(f"**{d['id']}. {d['topic']}** · *{d['status']}*. {d['question']}  ")
        L.append(f"Options: {' / '.join(d['options'])}. Default: {d['default']}. Blocks: {d['blocks']}.")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
