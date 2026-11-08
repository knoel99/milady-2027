#!/usr/bin/env python3
"""Build outline.json and outline.md from outline_data.py, with totals, status counts and path checks.

Usage: python3 -I outline_src/build_outline.py   (run from anywhere; paths are absolute)
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
PAUSE_S = 1.5


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


def narration_stats(block):
    w = words(block["tts_text"])
    pauses = block["tts_text"].count("[long pause]")
    est = w / WPM * 60 + pauses * PAUSE_S
    return {"words": w, "long_pauses": pauses, "est_seconds_at_150wpm": round(est, 1)}


def main():
    chapters = D.CHAPTERS
    problems = []
    status_all = {"READY": 0, "PROVISIONAL": 0, "PENDING": 0}
    per_cut = {"core": {"duration_s": 0, "scenes": 0, "READY": 0, "PROVISIONAL": 0, "PENDING": 0, "render_s": 0.0},
               "extension": {"duration_s": 0, "scenes": 0, "READY": 0, "PROVISIONAL": 0, "PENDING": 0, "render_s": 0.0}}
    regen_index = []
    seen = set()
    for ch in chapters:
        tot = 0
        counts = {"READY": 0, "PROVISIONAL": 0, "PENDING": 0}
        for s in ch["scenes"]:
            if s["id"] in seen:
                problems.append(f"duplicate scene id {s['id']}")
            seen.add(s["id"])
            tot += s["duration_s"]
            counts[s["status"]] += 1
            status_all[s["status"]] += 1
            c = per_cut[ch["cut"]]
            c["scenes"] += 1
            c[s["status"]] += 1
            c["render_s"] += s["duration_s"] * 30 / FPS_CLASS[s["render_class"]]
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
            if s["regen"]:
                regen_index.append({"scene": s["id"], "title": s["title"], "chapter": ch["id"], "cut": ch["cut"],
                                    "status": s["status"], "scene_data": s["regen"]["scene_data"],
                                    "exists_now": all(path_exists(x.strip()) for x in s["regen"]["scene_data"].split("+")),
                                    "provisional_run": s["regen"]["provisional_run"], "final_run": s["regen"]["final_run"]})
        ch["target_duration_s"] = tot
        ch["target_duration"] = mmss(tot)
        ch["status_counts"] = counts
        per_cut[ch["cut"]]["duration_s"] += tot

    core_ids = [c["id"] for c in chapters if c["cut"] == "core"]
    ext_ids = [c["id"] for c in chapters if c["cut"] == "extension"]
    by_id = {c["id"]: c for c in chapters}
    part1 = sum(by_id[i]["target_duration_s"] for i in ["C0", "C1", "C2", "C3", "C4", "C5", "C6"])
    part2_core = sum(by_id[i]["target_duration_s"] for i in ["C7", "C8", "C9", "C10"])
    # extended running order: extensions inserted after their anchor
    order = []
    for cid in core_ids:
        order.append(cid)
        anchor = cid
        while True:
            nxt = [x for x in ext_ids if by_id[x].get("insert_after") == anchor]
            if not nxt:
                break
            order.append(nxt[0])
            anchor = nxt[0]
    # C10 must stay last: move any extension placed after C10 (none expected)
    for pc in per_cut.values():
        pc["duration"] = mmss(pc["duration_s"])
        pc["render_estimate_h_1080p30"] = round(pc["render_s"] / 3600, 2)
        pc["render_s"] = round(pc["render_s"])

    out = {
        "title": D.TITLE, "subtitle": D.SUBTITLE, "title_options": D.TITLE_OPTIONS,
        "version": "2026-11-08", "language": "en", "status": "outline (to be validated by the user)",
        "logline": D.LOGLINE, "synopsis": D.SYNOPSIS,
        "logline_synopsis_words": words(D.LOGLINE) + words(D.SYNOPSIS),
        "conventions": {
            "levels": {"L0": "anyone", "L1": "curious high school / early undergraduate", "L2": "science undergraduate",
                       "L3": "M1 physics or ML", "L4": "M2 / early PhD", "L5": "supervisors and specialists"},
            "status": {"READY": "all data exist (repository results, site assets, or nothing data-driven)",
                       "PROVISIONAL": "a reduced or CPU run can produce the data now; replaced later by the HPC result",
                       "PENDING": "needs HPC, GPU or consortium results; ships now as an 'empty seat' (bet + criterion)"},
            "registers": {"NIGHT": "#0B0F14, default", "PAPER": "#F4F1EA, derivations", "BLUEPRINT": "dark + grey grid, infrastructure"},
            "render_class": {k: f"{v} frames/s measured at 1080p30 on 4 cores" for k, v in FPS_CLASS.items()},
            "colour_key_night": {"param": "#1BAF7A", "u": "#3987E5", "B": "#EB6834", "model": "#B49CF0", "metric": "#EDA100",
                                 "infra": "#6B7A8C"},
            "paths": {"assets_and_data": SITE + " (read-only)", "proto/...": PROTO, "data/...": PROTO + "/data (scene data written by tools/extract_data.py)"},
            "run_env": D.RUNENV,
            "pending_device": "empty seat: dashed chart frame, labelled axes, shaded success band, data tag; two narration variants (pending / result)",
        },
        "cuts": {
            "core": {"chapters": core_ids, **per_cut["core"]},
            "extensions": {"modules": ext_ids, **per_cut["extension"]},
            "extended": {"running_order": order,
                         "duration_s": per_cut["core"]["duration_s"] + per_cut["extension"]["duration_s"],
                         "duration": mmss(per_cut["core"]["duration_s"] + per_cut["extension"]["duration_s"])},
            "two_episode_option": {"part1": {"chapters": ["C0", "C1", "C2", "C3", "C4", "C5", "C6"], "duration": mmss(part1)},
                                   "part2": {"chapters": ["C7", "X2", "X3", "C8", "X4", "C9", "X5", "X6", "C10"],
                                             "duration": mmss(part2_core + sum(by_id[i]["target_duration_s"] for i in ["X2", "X3", "X4", "X5", "X6"])),
                                             "note": "X1 (E3 in depth) goes after C2 in Part 1 if wanted"}},
        },
        "status_counts": status_all,
        "chapters": chapters,
        "narration_drafts": {
            "opening_60s": {**D.OPENING, **narration_stats(D.OPENING)},
            "closing_60s": {**D.CLOSING, **narration_stats(D.CLOSING)},
            "tts_settings": "Fish Audio drama-3, temperature 0.1, prosody.speed 1.0, one acting cue at the start, [long pause] only between paragraphs",
        },
        "regenerable_index": regen_index,
        "decisions": D.DECISIONS,
        "production_notes": D.NOTES,
        "checks": {"problems": problems},
    }
    with open(os.path.join(VP, "outline.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(os.path.join(VP, "outline.md"), "w") as f:
        f.write(render_md(out, by_id))
    print(json.dumps({"core": per_cut["core"], "extension": per_cut["extension"], "status": status_all,
                      "extended": out["cuts"]["extended"]["duration"], "two_episodes": out["cuts"]["two_episode_option"],
                      "opening": out["narration_drafts"]["opening_60s"]["words"], "opening_s": out["narration_drafts"]["opening_60s"]["est_seconds_at_150wpm"],
                      "closing": out["narration_drafts"]["closing_60s"]["words"], "closing_s": out["narration_drafts"]["closing_60s"]["est_seconds_at_150wpm"],
                      "logline_synopsis_words": out["logline_synopsis_words"], "problems": problems}, indent=1, ensure_ascii=False))


def code(p):
    return f"`{p}`"


def render_scene(s):
    L = []
    head = f"#### {s['id']} {s['title']}  \n`{s['level']}` · {s['duration_s']} s · **{s['status']}** · {s['register']} · render {s['render_class']}"
    L.append(head)
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
    if s["flags"]:
        L.append(f"- **Flags.** {'; '.join(s['flags'])}")
    if s["sources"]:
        L.append(f"- **Sources.** {', '.join(s['sources'])}")
    if s["regen"]:
        r = s["regen"]
        L.append(f"- **Regeneration hook.**")
        L.append(f"  - scene data: {code(r['scene_data'])}")
        L.append(f"  - upstream: {r['upstream']}")
        if r["provisional_run"]:
            L.append(f"  - provisional run (now, CPU): {r['provisional_run']}")
        L.append(f"  - final run: {r['final_run']}")
        L.append(f"  - extractor: {r['extractor']}")
        if r.get("criterion"):
            L.append(f"  - criterion: {r['criterion']}")
        L.append(f"  - ships now as: {r['shippable_now']}")
        L.append(f"  - narration: {r['narration']}")
    L.append("")
    return "\n".join(L)


def render_md(o, by_id):
    c = o["cuts"]
    L = []
    L.append(f"# Chaptered outline: {o['title']}")
    L.append("")
    L.append(f"*{o['subtitle']}.* Long English explainer about the MilaDy 2027 site. Outline version {o['version']}, "
             f"generated from `outline_src/outline_data.py` by `outline_src/build_outline.py` (the same data as `outline.json`). "
             f"Sources: `inventory.md`, `pedagogy.md`, `styles.md`, `pipeline.md` and the site under `/home/user/milady-2027/en/`. "
             f"Source references use the inventory's abbreviations (R report, T thesis proposal, S supervisors, C computing, H home, "
             f"P4 = prep module 4, D digest, X experiments page, IR infra README, CFG configs).")
    L.append("")
    L.append("## 0. At a glance")
    L.append("")
    L.append("| Cut | Chapters | Duration | Scenes | READY | PROVISIONAL | PENDING | Render estimate, 1080p30, 4 cores |")
    L.append("|---|---|---|---|---|---|---|---|")
    co, ex = c["core"], c["extensions"]
    L.append(f"| Core cut | {', '.join(co['chapters'])} | **{co['duration']}** | {co['scenes']} | {co['READY']} | {co['PROVISIONAL']} | {co['PENDING']} | {co['render_estimate_h_1080p30']} h |")
    L.append(f"| Extension modules | {', '.join(ex['modules'])} | **{ex['duration']}** | {ex['scenes']} | {ex['READY']} | {ex['PROVISIONAL']} | {ex['PENDING']} | {ex['render_estimate_h_1080p30']} h |")
    sc_all = o["status_counts"]
    L.append(f"| Extended cut | {' → '.join(c['extended']['running_order'])} | **{c['extended']['duration']}** | {co['scenes'] + ex['scenes']} | {sc_all['READY']} | {sc_all['PROVISIONAL']} | {sc_all['PENDING']} | {round(co['render_estimate_h_1080p30'] + ex['render_estimate_h_1080p30'], 2)} h |")
    L.append("")
    t2 = c["two_episode_option"]
    L.append(f"Two-episode option: Part 1 = {', '.join(t2['part1']['chapters'])} ({t2['part1']['duration']}, L0 to L3); "
             f"Part 2 = {', '.join(t2['part2']['chapters'])} ({t2['part2']['duration']}, L3 to L5); {t2['part2']['note']}.")
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
    L.append("- **Levels.** " + "; ".join(f"{k}: {v}" for k, v in o["conventions"]["levels"].items()) + ". "
             "An altitude rail on the right edge shows the level; it only climbs, except in the closing.")
    L.append("- **Status.** " + "; ".join(f"**{k}**: {v}" for k, v in o["conventions"]["status"].items()) + ".")
    L.append("- **Pending device.** Each PENDING scene is an *empty seat*: " + o["conventions"]["pending_device"].split(": ", 1)[1] +
             ". It is shippable. The hatched AWAITING preview of the pipeline is for drafts only.")
    L.append("- **Colour key (NIGHT values).** green `#1BAF7A` control parameter, blue `#3987E5` velocity u, vermillion `#EB6834` "
             "magnetic field B, violet `#B49CF0` generative model, amber `#EDA100` distribution-level metrics, grey `#6B7A8C` "
             "infrastructure. On PAPER: the site values `#009E73`, `#0072B2`, `#D55E00`, `#6C4BA0`, `#E69F00`. Matter is grey. "
             "Polarity is a shade of vermillion, never a new hue.")
    L.append("- **Paths.** Assets and data are relative to `/home/user/milady-2027` (read-only) unless they start with `proto/` "
             f"(`{PROTO}`) or `data/` (scene data files written by `tools/extract_data.py` into `{PROTO}/data`).")
    L.append(f"- **Run environment for every regeneration run.** {o['conventions']['run_env']}")
    L.append("- **Motifs** (M1 needle and flip, M2 knob, M3 two inks, M4 violet cloud, M5 amber histogram, M6 projector, "
             "M7 staircase, M8 altitude rail, M9 pen, M10 mirror) and transitions (T1 morph, T2 scale dive, T3 ink change, "
             "T4 chapter card, T5 hard cut, T6 equation morph) follow `styles.md` §3.5-3.6. Every chapter opens with T4.")
    L.append("")
    L.append("## 3. Running order")
    L.append("")
    L.append("| Id | Chapter | Cut | Levels | Duration | Scenes | R / P / N | Takeaway |")
    L.append("|---|---|---|---|---|---|---|---|")
    for cid in c["extended"]["running_order"]:
        ch = by_id[cid]
        cut = "core" if ch["cut"] == "core" else f"ext. (after {ch['insert_after']})"
        sc = ch["status_counts"]
        L.append(f"| {cid} | {ch['title']} | {cut} | {ch['levels']} | {ch['target_duration']} | {len(ch['scenes'])} | "
                 f"{sc['READY']} / {sc['PROVISIONAL']} / {sc['PENDING']} | {ch['takeaway']} |")
    L.append("")
    nd = o["narration_drafts"]
    L.append("## 4. Narration drafts: the first and the last minute")
    L.append("")
    L.append(f"Written for TTS ({nd['tts_settings']}). Short sentences; `[long pause]` only between paragraphs.")
    L.append("")
    for key, label in [("opening_60s", "Opening 60 seconds"), ("closing_60s", "Closing 60 seconds")]:
        b = nd[key]
        L.append(f"### {label} (scenes {', '.join(b['scenes'])})")
        L.append("")
        L.append(f"{b['words']} words, {b['long_pauses']} long pauses, about {b['est_seconds_at_150wpm']} s at 150 words per minute.")
        L.append("")
        L.append("```text")
        L.append(b["tts_text"].replace(" [long pause] ", " [long pause]\n\n"))
        L.append("```")
        L.append("")
        L.append("Cue map: " + "; ".join(f"\"{a}\" → {b2}" for a, b2 in b["cue_map"]) + ".")
        L.append("")
        L.append(f"Note: {b['notes']}")
        L.append("")
    L.append("## 5. Core cut: chapters and scenes")
    L.append("")
    for ch in o["chapters"]:
        if ch["cut"] != "core":
            continue
        L.extend(render_chapter(ch))
    L.append("## 6. Extension modules")
    L.append("")
    L.append("Each module is self-contained and slots in after its anchor chapter; the core cut never refers to them.")
    L.append("")
    for ch in o["chapters"]:
        if ch["cut"] != "extension":
            continue
        L.extend(render_chapter(ch))
    L.append("## 7. Regenerable sections index")
    L.append("")
    L.append("| Scene | Cut | Status | Scene data | Exists now | Provisional run (CPU, now) | Final run |")
    L.append("|---|---|---|---|---|---|---|")
    for r in o["regenerable_index"]:
        L.append(f"| {r['scene']} {r['title']} | {r['cut']} | {r['status']} | `{r['scene_data']}` | {'yes' if r['exists_now'] else 'no'} | "
                 f"{r['provisional_run'] or 'none'} | {r['final_run']} |")
    L.append("")
    L.append("Cheapest-first order for the provisional runs: X5.4 X-points (minutes) → X4.2 Rice levels (minutes) → C9.3 / X5.3 "
             "palier1 sweep (~30 min) → C9.4 ABC 32³ (~1-1.5 h, estimate) → C9.5 Taylor-Green 32³ subset (~1-1.5 h, estimate) → "
             "C9.6 fm3d smoke training (after C9.5) → X4.5 E1 with three seeds (2-3 h). CPU times marked 'estimate' are "
             "extrapolations from solver benchmarks; none of these runs has been launched.")
    L.append("")
    L.append("## 8. Decisions that need your input")
    L.append("")
    for d in o["decisions"]:
        L.append(f"**{d['id']}. {d['topic']}.** {d['question']}  ")
        L.append(f"Options: {' / '.join(d['options'])}. Default if you say nothing: {d['default']}. Blocks: {d['blocks']}.")
        L.append("")
    L.append("## 9. Production notes")
    L.append("")
    for n in o["production_notes"]:
        L.append(f"- {n}")
    L.append("")
    if o["checks"]["problems"]:
        L.append("## Build checks")
        L.append("")
        for p in o["checks"]["problems"]:
            L.append(f"- {p}")
        L.append("")
    return "\n".join(L)


def render_chapter(ch):
    L = []
    where = "" if ch["cut"] == "core" else f" · inserted after {ch['insert_after']}"
    L.append(f"### {ch['id']}. {ch['title']}")
    L.append("")
    sc = ch["status_counts"]
    L.append(f"`{ch['levels']}` · {ch['target_duration']} ({ch['target_duration_s']} s){where} · "
             f"{len(ch['scenes'])} scenes: {sc['READY']} READY, {sc['PROVISIONAL']} PROVISIONAL, {sc['PENDING']} PENDING")
    L.append("")
    L.append(f"- **Learning goal.** {ch['learning_goal']}")
    L.append(f"- **Takeaway (one sentence).** {ch['takeaway']}")
    L.append("")
    for s in ch["scenes"]:
        L.append(render_scene(s))
    return L


if __name__ == "__main__":
    main()
