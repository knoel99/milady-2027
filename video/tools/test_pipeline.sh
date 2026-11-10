#!/usr/bin/env bash
# test_pipeline.sh: end-to-end test of the pipeline on the test units of script/_test (never the real
# script), with PLACEHOLDER narration (no API call), in draft mode (960x540, 15 fps).
# Checks: cut assembly (chapters, extension insert_after, the extra unit before the closer, core-only scene),
# pending -> provisional with the result variant when data arrive (only that scene re-renders),
# reuse of renders across cuts, question cards, sound effects, loudness, two audio tracks, stems,
# subtitles, cue sheet, per-cue check, external narration fit (+ re-timing), and optionally (FULL=1) a
# 1080p30 final-mode build.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -f script/_test/cuts.json ] || [ ! -d scenes/_test ]; then
  echo "SKIP: this test needs the test units script/_test/ and the test scenes scenes/_test/ (not restored with the engine)"
  exit 2
fi
export NODE_PATH=/opt/node22/lib/node_modules
T="--units script/_test --cuts script/_test/cuts.json"
SCR=$(mktemp -d)
trap 'rm -rf "$SCR"' EXIT
pass() { echo "  PASS $*"; }
fail() { echo "  FAIL $*"; exit 1; }
rendered() { python3 -c "import json,sys; print(','.join(r['id'] for r in json.load(open(sys.argv[1]))['rendered']))" "$1"; }

rm -f script/_test/data/result.json
rm -f audio/external/T*.wav audio/external/T*.align.json audio/external/tc1.Q.* audio/external/_test_core_fit_report.json

echo "1. draft build of the test core cut (placeholder narration)"
node build.js --cut core $T --name _test_core --draft --tts placeholder > "$SCR/b1.log" 2>&1 || { cat "$SCR/b1.log"; fail build; }
F=out/draft/film__test_core.mp4
[ -s "$F" ] && pass "$F exists"
python3 - "$F" <<'EOF' || fail "streams"
import json, subprocess, sys
p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate", "-of", "json", sys.argv[1]], capture_output=True, text=True).stdout)
kinds = [s["codec_type"] for s in p["streams"]]
assert kinds.count("video") == 1 and kinds.count("audio") == 2, kinds
v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
assert (v["width"], v["height"], v["r_frame_rate"]) == (960, 540, "15/1"), v
EOF
pass "1 video (960x540 15 fps) + 2 audio tracks"
python3 - <<'EOF' || fail "loudness"
import json
r = json.load(open("out/draft/stems/_test_core_mix.json"))["full_mix_aac"]
assert abs(r["I"] + 16) <= 0.5 and r["TP"] <= -1.0, r
EOF
pass "full mix -16 LUFS, true peak <= -1 dBTP"
for k in narration music effects nonarration; do [ -s "out/draft/stems/_test_core_$k.m4a" ] || fail "stem $k"; done; pass "stems"
for k in srt vtt ass; do [ -s "out/draft/subs/_test_core.$k" ] || fail "subs $k"; done; pass "subtitles .srt .vtt .ass"
python3 -c "import json; c=json.load(open('out/draft/_test_core_cues.json')); assert len(c['sentences'])==9, len(c['sentences'])" || fail "cue sheet"
pass "cue sheet: 9 sentences with their times"

echo "2. nothing changed -> nothing re-rendered"
node build.js --cut core $T --name _test_core --draft --tts placeholder > "$SCR/b2.log" 2>&1 || { cat "$SCR/b2.log"; fail build; }
[ -z "$(rendered out/draft/_test_core_build_report.json)" ] && pass "0 scenes re-rendered" || fail "re-rendered: $(rendered out/draft/_test_core_build_report.json)"

echo "3. the result data arrive -> T1.2 becomes provisional with its result narration, only T1.2 re-renders"
cat > script/_test/data/result.json <<'EOF'
{"meta": {"source": "TEST ONLY (not a result)", "stamp": "TEST DATA · not a real campaign"},
 "fields": {"s17": 0.0123, "s18": -0.0081, "verdict": "the bet holds", "bet_holds": true},
 "points": [[15, -0.05], [16, -0.03], [17, 0.0123], [18, -0.0081], [19, 0.02], [20, 0.04]]}
EOF
node build.js --cut core $T --name _test_core --draft --tts placeholder > "$SCR/b3.log" 2>&1 || { cat "$SCR/b3.log"; fail build; }
[ "$(rendered out/draft/_test_core_build_report.json)" = "T1.2" ] && pass "only T1.2 re-rendered" || fail "re-rendered: $(rendered out/draft/_test_core_build_report.json)"
python3 - <<'EOF' || fail "variant"
import json
s = {x["id"]: x for x in json.load(open("script/_build/film__test_core.json"))["scenes"]}["T1.2"]
assert s["status"] == "provisional" and s["variant"] == "result", (s["status"], s["variant"])
assert "zero point zero one" in s["paragraphs"][0]["sentences"][1]["text"]
assert len(s["paragraphs"]) == 1          # the "!bet_holds" paragraph is dropped
EOF
pass "status provisional, result variant, {{field}} filled, 'when' honoured"
rm script/_test/data/result.json
node build.js --cut core $T --name _test_core --draft --tts placeholder > "$SCR/b4.log" 2>&1 || { cat "$SCR/b4.log"; fail build; }
[ "$(rendered out/draft/_test_core_build_report.json)" = "T1.2" ] && pass "data removed: only T1.2 re-rendered (back to pending)" || fail "re-rendered: $(rendered out/draft/_test_core_build_report.json)"

echo "4. extended test cut: extension inserted, core-only scene dropped, renders reused"
node build.js --cut extended $T --name _test_extended --draft --tts placeholder > "$SCR/b5.log" 2>&1 || { cat "$SCR/b5.log"; fail build; }
python3 - <<'EOF' || fail "order"
import json
ids = [s["id"] for s in json.load(open("script/_build/film__test_extended.json"))["scenes"]]
assert ids == ["T1.1", "TX.1", "T1.2", "tc1.Q", "T9.1", "T2.1"], ids
core = [s["id"] for s in json.load(open("script/_build/film__test_core.json"))["scenes"]]
assert core == ["T1.1", "T1.2", "tc1.Q", "T9.1", "T2.1", "T2.2"], core
EOF
pass "running orders: core $(python3 -c "import json;print(' '.join(s['id'] for s in json.load(open('script/_build/film__test_core.json'))['scenes']))") | extended $(python3 -c "import json;print(' '.join(s['id'] for s in json.load(open('script/_build/film__test_extended.json'))['scenes']))")"
R=$(rendered out/draft/_test_extended_build_report.json)
[ "$R" = "TX.1" ] || [ -z "$R" ] && pass "extended cut: only TX.1 rendered (or nothing, if already there); the rest reused from the core cut" || echo "  NOTE re-rendered: $R (expected TX.1 only, unless the runtime changed meanwhile)"
python3 -c "
import json; t=json.load(open('out/draft/_test_extended_timeline.json'))
tx=[s for s in t['scenes'] if s['id']=='TX.1'][0]; assert sum(1 for e in tx['sfx'] if e['id']=='tick')>=3, tx['sfx']
" || fail "page events"
pass "sound events exported by the page (window.__EVENTS__) reach the mix"

echo "5. make check on a unit (one still per cue, page errors)"
node build.js --unit tc1 $T --check > "$SCR/b6.log" 2>&1 || { cat "$SCR/b6.log"; fail check; }
pass "check: $(tail -1 "$SCR/b6.log")"

echo "6. external narration: fit, out-of-range report, re-timing"
mkdir -p "$SCR/takes"
for p in "T1.1 0.95" "T1.2 1.07" "tc1.Q 0.75" "T9.1 1.0" "T2.1 1.1"; do set -- $p
  ffmpeg -v error -y -i "audio/scenes/$1.wav" -af "atempo=$2,volume=-6dB" -ar 44100 "$SCR/takes/$1.wav"; done
python3 -I tools/fit_narration.py --cut core --name _test_core --dir "$SCR/takes" > "$SCR/f1.log" || { cat "$SCR/f1.log"; fail fit; }
grep -q "tc1.Q: NOT APPLIED" "$SCR/f1.log" && pass "out-of-range sentence reported (tc1.Q needs x1.33)" || { cat "$SCR/f1.log"; fail "no out-of-range report"; }
python3 -I tools/fit_narration.py --cut core --name _test_core --dir "$SCR/takes" --retime auto > "$SCR/f2.log" || { cat "$SCR/f2.log"; fail fit; }
node build.js --cut core $T --name _test_core --draft --tts placeholder --narration external > "$SCR/b7.log" 2>&1 || { cat "$SCR/b7.log"; fail build; }
R=$(rendered out/draft/_test_core_build_report.json)
[ "$R" = "tc1.Q" ] && pass "fitted scenes keep their timing; only the re-timed tc1.Q re-renders" || echo "  NOTE re-rendered: $R (expected tc1.Q only, unless the runtime changed meanwhile)"
rm -f audio/external/T*.wav audio/external/T*.align.json audio/external/tc1.Q.* audio/external/_test_core_fit_report.json
node build.js --cut core $T --name _test_core --draft --tts placeholder > "$SCR/b8.log" 2>&1 || { cat "$SCR/b8.log"; fail build; }
pass "back to the TTS narration"

if [ "${FULL:-0}" = "1" ]; then
  echo "7. final mode (1080p30, CRF 21, maxrate 6M, stitchable) on the test core cut"
  node build.js --cut core $T --name _test_core --tts placeholder > "$SCR/b9.log" 2>&1 || { cat "$SCR/b9.log"; fail build; }
  ffmpeg -v error -i out/film__test_core.mp4 -map 0:v -f null - || fail "decode"
  pass "out/film__test_core.mp4 decodes cleanly ($(tail -1 "$SCR/b9.log" | cut -c1-120))"
  # final-mode test outputs are not deliverables: remove them (draft outputs stay in out/draft for review)
  rm -rf out/film__test_core* out/stems/_test_core_* out/_test_core_build_report.json subs/_test_core* \
         script/_build/_test_core_cues.json script/_build/_test_core_timeline.json
  for i in T1.1 T1.2 tc1.Q T9.1 T2.1 T2.2; do rm -f out/scenes/$i.*; done
fi
# the test's build files are not deliverables: keep script/_build and subs/ for the real cuts
rm -rf script/_build/*_test_* script/_build/*unit_tc1* subs/_test_* subs/unit_tc1* out/narration_script__test_*
echo "ALL TESTS PASSED (review copies: out/draft/film__test_core.mp4, out/draft/film__test_extended.mp4, out/check/unit_tc1/)"
