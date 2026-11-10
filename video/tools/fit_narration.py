#!/usr/bin/env python3
"""fit_narration.py: fit an EXTERNAL narration (recorded elsewhere) onto the film, sentence by sentence.

The animations are timed on the current narration (script/_build/<name>_cues.json, audio/scenes/*.align.json).
An external take is segmented into the script's sentences by silence detection (the same dynamic
programme as audio/align.py: the script's character counts predict where each sentence ends, long pauses
are preferred), then every sentence is time-stretched onto the slot of the current timing:

  ratio = recorded length / current length
  0.88 <= ratio <= 1.12   stretched to exactly the current length (rubberband, else atempo): status "fit"
  ratio > 1.12            if a stretch of at most 12 % fits in the sentence + the start of the following
                          pause: status "fit-overhang"; otherwise "OUT OF RANGE"
  ratio < 0.88            slowed down by at most 12 %, placed at the current start (a longer pause follows)

Scenes whose sentences all fit keep their timing: nothing is re-rendered, only the sound is re-mixed.
Scenes with an out-of-range sentence are reported (sentence, ratio needed) and keep the TTS narration,
unless --retime auto: those scenes are RE-TIMED on the take's natural timing (the scene animates on cue
names, so it re-renders with the new durations). --retime all re-times every scene (no stretch at all).

Input: --dir takes/  one file per scene named <scene id>.wav|flac|mp3|m4a|ogg (recommended), or
       --audio take.wav  one file for the whole cut, in script order (segmented over the whole cut).
Output: audio/external/<scene>.wav + <scene>.align.json (same format as audio/align.py), a report
        audio/external/<name>_fit_report.json; then `make film CUT=<cut> NARRATION=external`.
The take is levelled to the loudness of the TTS narration (one gain for the whole take).
French narration: --lang fr works on the French build (<cut>_fr: script/_build/film_<cut>_fr.json, timing in
audio/scenes_fr/, output in audio/external_fr/, out/narration_script_<cut>_fr.md); then
`make film CUT=<cut> LANG=fr NARRATION=external`.
Usage: python3 -I tools/fit_narration.py --cut core --export      (reading script for the narrator: out/narration_script_core.md)
       python3 -I tools/fit_narration.py --cut core (--dir takes/ | --audio take.wav) [--retime none|auto|all]
                                          [--tol 0.12] [--dry-run] [--lang en|fr]
"""
import argparse, hashlib, json, os, subprocess, sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "audio"))
from align import split_sentences, read_wav, write_wav, scenes_dir, PAD0, PAD1  # noqa: E402
from mix import ff_measure  # noqa: E402
from tts import LONG_PAUSE_S, SR  # noqa: E402

EXT = os.path.join(ROOT, "audio", "external")      # English; audio/external_<lang> for another narration language
SCENES = scenes_dir("en")                          # current TTS timing (audio/scenes, or audio/scenes_<lang>)
AUDIO_EXT = (".wav", ".flac", ".mp3", ".m4a", ".ogg", ".aif", ".aiff")


def decode(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True)
    if p.returncode:
        sys.exit(f"cannot decode {path}: {p.stderr.decode()[-300:]}")
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


HAS_RUBBERBAND = "rubberband" in subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout


def stretch(x, factor):
    """factor > 1 speeds up (shorter output). rubberband (formant-preserving) if ffmpeg has it, else atempo."""
    if abs(factor - 1) < 1e-3 or len(x) < 256:
        return x
    af = f"rubberband=tempo={factor:.5f}:pitchq=quality" if HAS_RUBBERBAND else f"atempo={factor:.5f}"
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af,
                        "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], input=x.astype(np.float32).tobytes(), capture_output=True)
    if p.returncode:
        sys.exit("stretch failed: " + p.stderr.decode()[-300:])
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


def script_text(sc):
    return [[p["hold_after"], [[s["id"], s["text"]] for s in p["sentences"]]] for p in sc["paragraphs"]]


def para_bonus(sc_list):
    """extra weight for paragraph and scene starts (longer pauses expected there)"""
    w = []
    for si, sc in enumerate(sc_list):
        for pi, p in enumerate(sc["paragraphs"]):
            for k, _ in enumerate(p["sentences"]):
                w.append((40 if si and pi == 0 and k == 0 else 12 if pi and k == 0 else 0))
    return w


def fit_scene(sc, ref, x, bounds, tol, mode):
    """Returns (track, align, rows, ok). mode: 'fit' or 'retime'."""
    sents = [s for p in sc["paragraphs"] for s in p["sentences"]]
    rows, ok = [], True
    if mode == "fit":
        total = ref["duration"]
        track = np.zeros(int(round(total * SR)) + int(0.5 * SR), dtype=np.float32)
        rs = ref["sentences"]
        # paragraph index of each sentence, to know what follows it
        pidx = [pi for pi, p in enumerate(sc["paragraphs"]) for _ in p["sentences"]]
        for k, (s, (a, b)) in enumerate(zip(sents, bounds)):
            seg = x[int(a * SR):int(b * SR)]
            rec = len(seg) / SR
            T = rs[k]["end"] - rs[k]["start"]
            if k + 1 < len(rs):
                avail = rs[k + 1]["start"] - rs[k]["start"] - (0.08 if pidx[k + 1] == pidx[k] else 0.35)
            else:
                avail = total - rs[k]["start"] + 0.5 * sc["tail"]
            ratio = rec / max(T, 1e-3)
            if 1 - tol <= ratio <= 1 + tol:
                f, st = ratio, "fit"
            elif ratio > 1 + tol:
                need = rec / max(avail, 1e-3)
                if need <= 1 + tol:
                    f, st = max(1.0, need), "fit-overhang"
                else:
                    f, st, ok = None, "OUT OF RANGE", False
            else:
                f, st = max(ratio, 1 - tol), "short"
            rows.append({"id": s["id"], "recorded_s": round(rec, 3), "slot_s": round(T, 3), "available_s": round(avail, 3),
                         "ratio": round(ratio, 3), "tempo": round(f, 3) if f else None, "status": st})
            if f:
                y = stretch(seg, f)
                i = int(round(rs[k]["start"] * SR))
                n = min(len(y), len(track) - i)
                track[i:i + n] += y[:n]
        track = track[:int(round(total * SR))]
        al = dict(ref, method="external-fit")
        return track, al, rows, ok
    # retime: the take's own timing, paragraph by paragraph, with the script's [long pause] + holds
    parts, out_s, paras, t, k = [], [], [], 0.0, 0
    for pi, p in enumerate(sc["paragraphs"]):
        n = len(p["sentences"])
        bs = bounds[k:k + n]
        a0, b1 = max(0.0, bs[0][0] - PAD0), min(len(x) / SR, bs[-1][1] + PAD1)
        clip = x[int(a0 * SR):int(b1 * SR)]
        for s, (a, b) in zip(p["sentences"], bs):
            out_s.append({"id": s["id"], "cue": s.get("cue"), "text": s["text"], "start": round(t + a - a0, 3), "end": round(t + b - a0, 3)})
            rows.append({"id": s["id"], "recorded_s": round(b - a, 3), "status": "retimed"})
        gap = p["hold_after"] + (LONG_PAUSE_S if pi < len(sc["paragraphs"]) - 1 else 0.0)
        paras.append({"start": round(t, 3), "end": round(t + len(clip) / SR, 3), "hold_after": p["hold_after"], "gap_after": round(gap, 3)})
        parts += [clip, np.zeros(int(round(gap * SR)), dtype=np.float32)]
        t += len(clip) / SR + gap
        k += n
    track = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
    al = {"scene": sc["id"], "duration": round(len(track) / SR, 4), "estimated": False, "method": "external-retime",
          "paragraphs": paras, "sentences": out_s}
    return track, al, rows, True


def export(film, scenes, name):
    """A reading script for an external narrator: one block per scene (= one file to record), every
    sentence with the length it has in the current timing, so the take can be fitted within +-12 %."""
    import re
    out = os.path.join(ROOT, "out", f"narration_script_{name}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L = [f"# Reading script: {film.get('title') or name} ({name})", "",
         "One file per scene, named `<scene id>.wav` (48 kHz or 44.1 kHz, mono, no music), read in order.",
         "Leave a clear pause (about one second) between paragraphs; the times in brackets are the length",
         "of each sentence in the current film (+-12 % is absorbed by tools/fit_narration.py).", ""]
    for sc in scenes:
        ap = os.path.join(SCENES, sc["id"] + ".align.json")
        al = {x["id"]: x for x in json.load(open(ap))["sentences"]} if os.path.exists(ap) else {}
        L.append(f"## {sc['id']}  {sc.get('title') or ''}  -> `{sc['id']}.wav`")
        for pi, p in enumerate(sc["paragraphs"]):
            if pi:
                L.append("  (paragraph break: pause about one second)")
            for x in p["sentences"]:
                t = al.get(x["id"])
                d = f"[{t['end'] - t['start']:.1f} s] " if t else ""
                L.append(f"- {d}{re.sub(r'\{(u|b|param|model|metric)\}(.*?)\{/\}', r'\2', x['text'])}")
        L.append("")
    open(out, "w").write("\n".join(L))
    print(f"[fit] reading script: {os.path.relpath(out, ROOT)} ({len(scenes)} scenes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", required=True)
    ap.add_argument("--name", help="build name (default: the cut)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dir")
    g.add_argument("--audio")
    g.add_argument("--export", action="store_true", help="write the reading script for a narrator (sentences + slot lengths)")
    ap.add_argument("--retime", choices=["none", "auto", "all"], default="none")
    ap.add_argument("--tol", type=float, default=0.12)
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    ap.add_argument("--lang", choices=["en", "fr"], default="en", help="narration language (fr: the <cut>_fr build)")
    a = ap.parse_args()
    global EXT, SCENES
    name = a.name or a.cut
    if a.lang != "en":
        EXT, SCENES = os.path.join(ROOT, "audio", f"external_{a.lang}"), scenes_dir(a.lang)
        if not name.endswith("_" + a.lang):
            name += "_" + a.lang
    fp = os.path.join(ROOT, "script", "_build", f"film_{name}.json")
    if not os.path.exists(fp):
        sys.exit(f"{fp} not found: build the cut first (make plan CUT={a.cut} or make film)")
    film = json.load(open(fp))
    scenes = [sc for sc in film["scenes"] if sum(len(p["sentences"]) for p in sc["paragraphs"])]
    if a.export:
        return export(film, scenes, name)
    refs = {}
    for sc in scenes:
        rp = os.path.join(SCENES, sc["id"] + ".align.json")
        if not os.path.exists(rp):
            sys.exit(f"{sc['id']}: no current timing ({rp}); build the cut first")
        refs[sc["id"]] = json.load(open(rp))
        if refs[sc["id"]].get("estimated"):
            print(f"[fit] warning: {sc['id']}: the current timing is an estimate (no TTS audio yet); --retime all is safer")
    # recordings -> per scene (signal, sentence bounds)
    takes, src_hash = {}, hashlib.sha256()
    if a.dir:
        files = {os.path.splitext(f)[0]: os.path.join(a.dir, f) for f in os.listdir(a.dir) if f.lower().endswith(AUDIO_EXT)}
        for sc in scenes:
            if sc["id"] in files:
                x = decode(files[sc["id"]])
                src_hash.update(x.tobytes()[:1 << 20])
                sents = [s for p in sc["paragraphs"] for s in p["sentences"]]
                bounds, s0, s1, method = split_sentences(sents, x, para_bonus([sc]))
                takes[sc["id"]] = (x, bounds, method)
        extra = sorted(set(files) - {sc["id"] for sc in scenes})
        if extra:
            print(f"[fit] files that match no scene of {name}: {extra}")
    else:
        x = decode(a.audio)
        src_hash.update(x.tobytes()[:1 << 20])
        sents = [s for sc in scenes for p in sc["paragraphs"] for s in p["sentences"]]
        print(f"[fit] segmenting {len(x) / SR / 60:.1f} min into {len(sents)} sentences ...")
        bounds, s0, s1, method = split_sentences(sents, x, para_bonus(scenes))
        k = 0
        for sc in scenes:
            n = sum(len(p["sentences"]) for p in sc["paragraphs"])
            takes[sc["id"]] = (x, bounds[k:k + n], method)
            k += n
    if not takes:
        sys.exit("[fit] no recording matches a scene")
    # one gain for the whole take: match the loudness of the current (TTS) narration
    ref_sig = np.concatenate([read_wav(os.path.join(ROOT, refs[s]["wav"])) for s in takes if refs[s].get("wav")]
                             or [np.zeros(1, dtype=np.float32)])
    take_sig = np.concatenate([x[int(b[0][0] * SR):int(b[-1][1] * SR)] for x, b, _ in takes.values()])
    I_ref, _ = ff_measure(ref_sig)
    I_take, _ = ff_measure(take_sig)
    gain = 10 ** ((I_ref - I_take) / 20) if np.isfinite(I_ref) and np.isfinite(I_take) else 1.0
    report = {"name": name, "source": a.dir or a.audio, "retime": a.retime, "tolerance": a.tol, "stretcher": "rubberband" if HAS_RUBBERBAND else "atempo",
              "gain_db": round(20 * np.log10(gain), 2), "scenes": {}}
    os.makedirs(EXT, exist_ok=True)
    n_fit = n_ret = n_bad = 0
    for sc in scenes:
        sid = sc["id"]
        if sid not in takes:
            report["scenes"][sid] = {"result": "no recording: TTS kept"}
            continue
        x, bounds, method = takes[sid]
        mode = "retime" if a.retime == "all" else "fit"
        track, al, rows, ok = fit_scene(sc, refs[sid], x, bounds, a.tol, mode)
        result = "fitted (timing unchanged)" if mode == "fit" else "re-timed"
        if not ok:
            bad = [r for r in rows if r["status"] == "OUT OF RANGE"]
            if a.retime == "auto":
                track, al, rows2, _ = fit_scene(sc, refs[sid], x, bounds, a.tol, "retime")
                result = f"re-timed ({len(bad)} sentences out of range)"
                rows = [dict(r, status=r["status"] + " -> retimed") if r["status"] == "OUT OF RANGE" else r for r in rows]
            else:
                result = f"NOT APPLIED: {len(bad)} sentences out of +-{a.tol:.0%}; TTS kept (re-record them, or --retime auto)"
                n_bad += 1
                report["scenes"][sid] = {"result": result, "segmentation": method, "sentences": rows}
                print(f"[fit] {sid}: {result}: " + ", ".join(f"{r['id']} needs x{r['ratio']:.2f} (slot {r['slot_s']} s)" for r in bad))
                continue
        n_ret += result.startswith("re-timed")
        n_fit += result.startswith("fitted")
        report["scenes"][sid] = {"result": result, "segmentation": method, "sentences": rows}
        print(f"[fit] {sid}: {result}" + ("" if mode == "retime" else f", tempo {min(r['tempo'] or 1 for r in rows):.2f}-{max(r['tempo'] or 1 for r in rows):.2f}"))
        if a.dry_run:
            continue
        track = np.clip(track * gain, -1, 1)
        wp = os.path.join(EXT, sid + ".wav")
        write_wav(wp, track)
        al = dict(al, scene=sid, wav=os.path.relpath(wp, ROOT), script_text=script_text(sc), external_source=a.dir or a.audio,
                  key=hashlib.sha256((src_hash.hexdigest() + json.dumps(rows, sort_keys=True) + str(a.retime)).encode()).hexdigest()[:20],
                  sources=["external"])
        al["duration"] = round(len(track) / SR, 4) if al["method"] == "external-retime" else al["duration"]
        json.dump(al, open(os.path.join(EXT, sid + ".align.json"), "w"), indent=1, ensure_ascii=False)
    report["summary"] = {"fitted": n_fit, "retimed": n_ret, "not_applied": n_bad, "no_recording": sum(1 for v in report["scenes"].values() if v["result"].startswith("no rec"))}
    if not a.dry_run:
        json.dump(report, open(os.path.join(EXT, f"{name}_fit_report.json"), "w"), indent=1, ensure_ascii=False)
    print(f"[fit] {name}: {report['summary']}; gain {report['gain_db']} dB; report {os.path.relpath(EXT, ROOT)}/{name}_fit_report.json")
    if n_bad:
        print(f"[fit] {n_bad} scenes kept the TTS narration: re-record the listed sentences closer to their slot, "
              f"or rerun with --retime auto to re-time those scenes (they will re-render).")
    print(f"[fit] next: make film CUT={a.cut}{'' if a.lang == 'en' else ' LANG=' + a.lang} NARRATION=external")


if __name__ == "__main__":
    main()
