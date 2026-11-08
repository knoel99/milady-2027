#!/usr/bin/env python3
"""align.py: sentence-level timings WITHOUT a forced aligner.

Because every TTS request is one scene's spoken sequence, the chunk duration is exact (decoded
sample count). Inside a chunk, sentence boundaries are found with ffmpeg `silencedetect`:
  1. detect pauses >= 0.18 s below -38 dBFS;
  2. predict where each sentence boundary should fall from the script (characters, with a
     paragraph bonus for [long pause]);
  3. choose, by dynamic programming, the K-1 pauses that best match the predictions in order,
     preferring long pauses (sentence ends are longer than commas);
  4. sentence start = end of the preceding chosen pause, end = start of the next one.
Falls back to the character-proportional estimate if too few pauses are found.
With a word-level aligner later (e.g. a Fish ASR call with timestamps, or ctc-forced-aligner /
faster-whisper on CPU) only this file changes; its output format stays the same.
Usage: python3 -I audio/align.py script/demo_script.json   -> audio/chunks/<scene>.align.json
"""
import json, os, re, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))


def silences(wav, noise_db=-38, min_d=0.18):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af",
                        f"silencedetect=noise={noise_db}dB:d={min_d}", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def align(scene, wav):
    with wave.open(wav) as w:
        dur = w.getnframes() / w.getframerate()
    sil = [(a, b if b is not None else dur) for a, b in silences(wav)]
    edge = [(a, b if b is not None else dur) for a, b in silences(wav, min_d=0.03)]   # short leading/trailing silences
    speech0 = edge[0][1] if edge and edge[0][0] <= 0.01 else 0.0
    speech1 = edge[-1][0] if edge and edge[-1][1] >= dur - 0.01 else dur
    inner = [(a, b) for a, b in sil if a > speech0 + 0.05 and b < speech1 - 0.05]
    sents, weights = [], []
    for pi, para in enumerate(scene["paragraphs"]):
        for si, s in enumerate(para):
            sents.append(s)
            n = len(re.sub(r"\{(u|b|param|model|metric)\}(.*?)\{/\}", r"\2", s["text"]))
            weights.append(n + (12 if pi and si == 0 else 0))
    K = len(sents)
    total = sum(weights)
    exp, c = [], 0
    for wgt in weights[:-1]:
        c += wgt
        exp.append(speech0 + (speech1 - speech0) * c / total)
    method = "silencedetect+dp"
    if K == 1:
        cuts = []
    elif len(inner) < K - 1:
        cuts, method = [(e, e) for e in exp], "proportional-fallback"
    else:
        # DP: pick K-1 pauses in order; cost = |mid - expected| - 0.8 * pause length
        INF = 1e18
        M = len(inner)
        cost = lambda j, i: abs((inner[i][0] + inner[i][1]) / 2 - exp[j]) - 0.8 * (inner[i][1] - inner[i][0])
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
                    D[j][i] = best + cost(j, i); P[j][i] = arg
        i = min(range(M), key=lambda i: D[K - 2][i])
        idx = [i]
        for j in range(K - 2, 0, -1):
            i = P[j][i]; idx.append(i)
        cuts = [inner[i] for i in reversed(idx)]
    out, t = [], speech0
    for k, s in enumerate(sents):
        end = cuts[k][0] if k < len(cuts) else speech1
        out.append({"id": s["id"], "cue": s.get("cue"), "text": s["text"], "start": round(t, 3), "end": round(end, 3)})
        if k < len(cuts):
            t = cuts[k][1]
    return {"scene": scene["id"], "duration": round(dur, 4), "method": method, "sentences": out}


def main():
    script = json.load(open(sys.argv[1]))
    errs = []
    for sc in script["scenes"]:
        wav = os.path.join(HERE, "chunks", sc["id"] + ".wav")
        res = align(sc, wav)
        meta = json.load(open(os.path.join(HERE, "chunks", sc["id"] + ".meta.json")))
        if meta.get("truth"):
            tr = {x["id"]: x for x in meta["truth"]}
            e = [abs(s["start"] - tr[s["id"]]["start"]) for s in res["sentences"]] + \
                [abs(s["end"] - tr[s["id"]]["end"]) for s in res["sentences"]]
            res["error_vs_truth_ms"] = {"mean": round(1000 * sum(e) / len(e), 1), "max": round(1000 * max(e), 1)}
            errs += e
        json.dump(res, open(os.path.join(HERE, "chunks", sc["id"] + ".align.json"), "w"), indent=2, ensure_ascii=False)
        print(sc["id"], res["method"], res.get("error_vs_truth_ms"))
    if errs:
        print(f"all scenes: mean boundary error {1000 * sum(errs) / len(errs):.1f} ms, max {1000 * max(errs):.1f} ms")


if __name__ == "__main__":
    main()
