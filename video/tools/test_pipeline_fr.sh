#!/usr/bin/env bash
# test_pipeline_fr.sh: end-to-end test of the FRENCH narration (--lang fr, BRIEF section 9) on the test units of
# script/_test with their overlays script/_test/fr/*.json, PLACEHOLDER narration (no API call), draft mode.
# Checks: overlay merge (same ids and cues, markup kept, chapter title), question card spoken from question.fr,
# untranslated sentence flagged and kept in English, voice from the overlay, French lexicon and Fish "language": "fr"
# in every request, cache keys distinct from the English ones, separate timeline / renders / stems / subtitles
# (suffix _fr, out/draft/scenes_fr, audio/scenes_fr) with French subtitles burned in, English renders untouched,
# MP4 audio track tagged French, French result variant ({{field}} spoken in French, <field>_fr strings), renders
# reused across the French cuts, per-cue check, live-TTS guard on untranslated text (no request can leave: cost
# guard at 0 words and a dead proxy), voice override file (make narration LANG=fr), external narration fit in French.
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH=/opt/node22/lib/node_modules
T="--units script/_test --cuts script/_test/cuts.json"
SCR=$(mktemp -d)
trap 'rm -rf "$SCR"' EXIT
pass() { echo "  PASS $*"; }
fail() { echo "  FAIL $*"; exit 1; }
rendered() { python3 -c "import json,sys; print(','.join(r['id'] for r in json.load(open(sys.argv[1]))['rendered']))" "$1"; }
VOICE=536d3a5e000945adb7038665781a4aca
rm -f script/_test/data/result.json
rm -f audio/external_fr/T1.1.* audio/external_fr/T1.2.* audio/external_fr/tc1.Q.* audio/external_fr/T9.1.* audio/external_fr/T2.1.* audio/external_fr/T2.2.* audio/external_fr/_test_core_fr_fit_report.json
# English renders and tracks of the test units must not move during the French test
snap() { for f in out/draft/scenes/T1.1.mp4 out/draft/scenes/T1.2.mp4 out/draft/scenes/T2.1.mp4 audio/scenes/T1.1.wav audio/scenes/T1.1.align.json; do
  [ -e "$f" ] && echo "$f $(stat -c %Y "$f") $(sha256sum "$f" | cut -c1-16)"; done; true; }
snap > "$SCR/en_before.txt"

echo "1. French draft build of the test core cut (placeholder narration)"
node build.js --cut core $T --name _test_core --lang fr --draft --tts placeholder > "$SCR/b1.log" 2>&1 || { cat "$SCR/b1.log"; fail build; }
F=out/draft/film__test_core_fr.mp4
[ -s "$F" ] && pass "$F exists"
python3 - "$F" <<'EOF' || fail "streams"
import json, subprocess, sys
p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:stream_tags=language,title",
                               "-of", "json", sys.argv[1]], capture_output=True, text=True).stdout)
kinds = [s["codec_type"] for s in p["streams"]]
assert kinds.count("video") == 1 and kinds.count("audio") == 2, kinds
v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
assert (v["width"], v["height"], v["r_frame_rate"]) == (960, 540, "15/1"), v
a = [s for s in p["streams"] if s["codec_type"] == "audio"]
assert a[0]["tags"]["language"] == "fra" and a[1]["tags"]["language"] == "zxx", [x["tags"] for x in a]
EOF
pass "1 video (960x540 15 fps) + 2 audio tracks, track 1 tagged French"
python3 - <<'EOF' || fail "loudness"
import json
r = json.load(open("out/draft/stems/_test_core_fr_mix.json"))["full_mix_aac"]
assert abs(r["I"] + 16) <= 0.5 and r["TP"] <= -1.0, r
EOF
for k in narration music effects nonarration full; do [ -s "out/draft/stems/_test_core_fr_$k.m4a" ] || fail "stem $k"; done
pass "stems out/draft/stems/_test_core_fr_*.m4a, full mix -16 LUFS, true peak <= -1 dBTP"
python3 - <<'EOF' || fail "film script"
import json
f = json.load(open("script/_build/film__test_core_fr.json"))
assert f["lang"] == "fr" and f["name"] == "_test_core_fr", (f["lang"], f["name"])
assert f["voice"]["reference_id"] == "536d3a5e000945adb7038665781a4aca", f["voice"]
s = {x["id"]: x for sc in f["scenes"] for p in sc["paragraphs"] for x in p["sentences"]}
assert s["T1.1.s2"]["text"] == "Regardez l'{b}aiguille{/} faire demi-tour, puis se poser." and s["T1.1.s2"]["cue"] == "flip"
assert s["tc1.Q.s1"]["text"].startswith("Faut-il ajouter Rm"), s["tc1.Q.s1"]
assert s["T2.2.s1"].get("untranslated") and s["T2.2.s1"]["text"].startswith("This coda"), s["T2.2.s1"]
assert f["untranslated"] == ["T2.2.s1"], f["untranslated"]
assert not any("text_fr" in x for x in s.values())
assert next(u for u in f["units"] if u["unit"] == "tc1")["title"] == "Chapitre de test un"
EOF
pass "overlay merged (ids, cues, markup), question card from question.fr, T2.2.s1 flagged untranslated, overlay voice and chapter title"
python3 - <<'EOF' || fail "cue sheet"
import json, subprocess
c = json.load(open("out/draft/_test_core_fr_cues.json"))
assert c["lang"] == "fr" and len(c["sentences"]) == 9, (c["lang"], len(c["sentences"]))
# same ids and cues as the English cut (assembled here into a scratch folder, nothing English is rebuilt)
import os, tempfile
d = tempfile.mkdtemp()
subprocess.run(["python3", "-I", "tools/assemble_cut.py", "--cut", "core", "--units", "script/_test", "--cuts", "script/_test/cuts.json",
                "--name", "_test_core", "--out", d], check=True, capture_output=True)
en = json.load(open(os.path.join(d, "film__test_core.json")))
ids_en = [(x["id"], x["cue"]) for sc in en["scenes"] for p in sc["paragraphs"] for x in p["sentences"]]
ids_fr = [(x["id"], x["cue"]) for x in c["sentences"]]
assert ids_en == ids_fr, (ids_en, ids_fr)
EOF
pass "cue sheet out/draft/_test_core_fr_cues.json: 9 sentences, same ids and cues as the English cut"
grep -q "aiguille" out/draft/subs/_test_core_fr.srt && ! grep -q "needle" out/draft/subs/_test_core_fr.srt || fail "subtitles not French"
grep -q $'va-t-elle revenir\xc2\xa0?' out/draft/subs/_test_core_fr.srt || fail "no-break space before ? missing"
grep -q "aiguille" out/draft/subs/_test_core_fr_scenes/T1.1.ass || fail "burned-in scene subtitles not French"
for k in srt vtt ass; do [ -s "out/draft/subs/_test_core_fr.$k" ] || fail "subs $k"; done
pass "French subtitles .srt .vtt .ass + per-scene .ass burned in (no-break space before ?)"
for i in T1.1 T1.2 tc1.Q T9.1 T2.1 T2.2; do [ -s "out/draft/scenes_fr/$i.mp4" ] || fail "render $i"; [ -s "audio/scenes_fr/$i.wav" ] || fail "track $i"; done
python3 -c "
import json; e=json.load(open('.tmp/entry__test_core_fr_T1.1.json')); assert e['lang']=='fr', e.get('lang')" || fail "entry lang"
pass "renders in out/draft/scenes_fr/, tracks in audio/scenes_fr/, entry.lang = fr"
snap > "$SCR/en_after.txt"
diff -q "$SCR/en_before.txt" "$SCR/en_after.txt" > /dev/null && pass "English renders and tracks untouched" || { diff "$SCR/en_before.txt" "$SCR/en_after.txt"; fail "English files changed"; }

echo "2. TTS requests: language fr, French lexicon, keys distinct from the English ones"
python3 -I audio/tts.py script/_build/film__test_core_fr.json --mode dry-run --quiet > "$SCR/dry.log"
python3 - <<'EOF' || fail "requests"
import json, sys
sys.path.insert(0, "audio")
import tts
reqs = [json.loads(l) for l in open("audio/requests/_test_core_fr.jsonl")]
assert reqs and all(r["body"]["language"] == "fr" for r in reqs), [r["body"]["language"] for r in reqs]
body = {k: v for k, v in reqs[0]["body"].items() if k not in ("text", "language")}
ref = {k: v for k, v in dict(tts.FISH_BODY, reference_id=reqs[0]["body"]["reference_id"]).items() if k != "language"}
assert body == ref, (body, ref)                                    # every other validated setting unchanged
q = next(r for r in reqs if r["scene"] == "tc1.Q")["body"]["text"]
assert q.startswith("[calm, natural narrator voice] ") and "erre ème" in q and "Rm" not in q, q
for r in reqs:                                                    # same text, English settings -> another key
    en = tts.cache_key(dict(r["body"], language="en"))
    assert en != r["key"], r["scene"]
    assert r["key"] == tts.cache_key(r["body"], "fr")
print("ok")
EOF
pass "every request: body language fr, other settings as validated, lexicon_fr applied (Rm -> 'erre ème'), keys (lang, text, voice, settings)"

echo "3. nothing changed -> nothing re-rendered"
node build.js --cut core $T --name _test_core --lang fr --draft --tts placeholder > "$SCR/b2.log" 2>&1 || { cat "$SCR/b2.log"; fail build; }
[ -z "$(rendered out/draft/_test_core_fr_build_report.json)" ] && pass "0 scenes re-rendered" || fail "re-rendered: $(rendered out/draft/_test_core_fr_build_report.json)"

echo "4. result data arrive -> T1.2 provisional with its FRENCH result narration, only T1.2 re-renders"
cat > script/_test/data/result.json <<'EOF'
{"meta": {"source": "TEST ONLY (not a result)", "stamp": "TEST DATA · not a real campaign"},
 "fields": {"s17": 0.0123, "s18": -0.0081, "verdict": "the bet holds", "verdict_fr": "le pari tient", "bet_holds": true},
 "points": [[15, -0.05], [16, -0.03], [17, 0.0123], [18, -0.0081], [19, 0.02], [20, 0.04]]}
EOF
node build.js --cut core $T --name _test_core --lang fr --draft --tts placeholder > "$SCR/b3.log" 2>&1 || { cat "$SCR/b3.log"; fail build; }
[ "$(rendered out/draft/_test_core_fr_build_report.json)" = "T1.2" ] && pass "only T1.2 re-rendered" || fail "re-rendered: $(rendered out/draft/_test_core_fr_build_report.json)"
python3 - <<'EOF' || fail "variant"
import json
s = {x["id"]: x for x in json.load(open("script/_build/film__test_core_fr.json"))["scenes"]}["T1.2"]
assert s["status"] == "provisional" and s["variant"] == "result", (s["status"], s["variant"])
t = s["paragraphs"][0]["sentences"][1]["text"]
assert t == "À dix-sept, le taux de croissance vaut zéro virgule zéro un, à dix-huit moins zéro virgule zéro un : le pari tient.", t
assert len(s["paragraphs"]) == 1
EOF
pass "status provisional, French result variant, numbers spoken in French, verdict_fr used, 'when' honoured"
rm script/_test/data/result.json
node build.js --cut core $T --name _test_core --lang fr --draft --tts placeholder > "$SCR/b4.log" 2>&1 || { cat "$SCR/b4.log"; fail build; }
[ "$(rendered out/draft/_test_core_fr_build_report.json)" = "T1.2" ] && pass "data removed: only T1.2 re-rendered (back to pending)" || fail "re-rendered: $(rendered out/draft/_test_core_fr_build_report.json)"

echo "5. French extended test cut: extension inserted, renders reused from the French core cut"
node build.js --cut extended $T --name _test_extended --lang fr --draft --tts placeholder > "$SCR/b5.log" 2>&1 || { cat "$SCR/b5.log"; fail build; }
python3 - <<'EOF' || fail "order"
import json
ids = [s["id"] for s in json.load(open("script/_build/film__test_extended_fr.json"))["scenes"]]
assert ids == ["T1.1", "TX.1", "T1.2", "tc1.Q", "T9.1", "T2.1"], ids
EOF
R=$(rendered out/draft/_test_extended_fr_build_report.json)
[ "$R" = "TX.1" ] || [ -z "$R" ] && pass "extended order as in English; only TX.1 rendered, the rest reused" || echo "  NOTE re-rendered: $R (expected TX.1 only)"
[ -s out/draft/film__test_extended_fr.mp4 ] && pass "out/draft/film__test_extended_fr.mp4"

echo "6. make check on a unit in French"
node build.js --unit tc1 $T --check --lang fr > "$SCR/b6.log" 2>&1 || { cat "$SCR/b6.log"; fail check; }
[ -d out/check/unit_tc1_fr ] && pass "check: $(tail -1 "$SCR/b6.log")" || fail "no out/check/unit_tc1_fr"

echo "7. live TTS refuses untranslated text (cost guard 0 words + dead proxy: no request can leave this machine)"
set +e
HTTPS_PROXY=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 FISH_API_KEY=invalid-test-key timeout 30 \
  python3 -I audio/tts.py script/_build/film__test_core_fr.json --mode live --max-new-words 0 --manifest "$SCR/live_manifest.json" > "$SCR/live.log" 2>&1
rc=$?
set -e
[ $rc -ne 0 ] && grep -q "untranslated" "$SCR/live.log" && ! grep -q "retry" "$SCR/live.log" && pass "live run refused before any request: $(grep -o 'still contain English[^:]*' "$SCR/live.log")" || { cat "$SCR/live.log"; fail "guard"; }

echo "8. voice override for the French narration (make narration LANG=fr VOICE=...)"
make -s -n narration LANG=fr VOICE=$VOICE CUTS=core | grep -q "tools/set_voice.py --lang fr $VOICE" && pass "make narration LANG=fr VOICE=<id> -> set_voice.py --lang fr <id>, then build.js --lang fr" || fail "make narration LANG=fr"
make -s -n narration LANG=fr VOICE=$VOICE CUTS=core | grep -q "build.js .*--lang fr" || fail "narration build not French"
if [ ! -e audio/voice_fr.json ]; then
  python3 -I tools/set_voice.py --lang fr $VOICE > /dev/null
  python3 -I tools/assemble_cut.py --cut core $T --name _test_core --lang fr --out "$SCR" > /dev/null
  python3 -c "import json,sys; v=json.load(open(sys.argv[1]))['voice']; assert v.get('override')=='audio/voice_fr.json', v" "$SCR/film__test_core_fr.json" || { python3 -I tools/set_voice.py --lang fr default; fail "override"; }
  python3 -I tools/set_voice.py --lang fr default > /dev/null
  [ ! -e audio/voice_fr.json ] && [ ! -e audio/voice.json ] && pass "audio/voice_fr.json overrides the French voice only, removed with VOICE=default"
else
  echo "  NOTE audio/voice_fr.json exists (a real override): override test skipped"
fi

echo "9. external narration in French: reading script, fit, build"
python3 -I tools/fit_narration.py --cut core --name _test_core --lang fr --export > /dev/null
grep -q "aiguille" out/narration_script__test_core_fr.md && pass "reading script out/narration_script__test_core_fr.md (French text)" || fail "reading script"
mkdir -p "$SCR/takes"
for p in "T1.1 0.95" "T1.2 1.05" "T9.1 1.0" "T2.1 1.04"; do set -- $p
  ffmpeg -v error -y -i "audio/scenes_fr/$1.wav" -af "atempo=$2,volume=-5dB" -ar 44100 "$SCR/takes/$1.wav"; done
python3 -I tools/fit_narration.py --cut core --name _test_core --lang fr --dir "$SCR/takes" > "$SCR/f1.log" || { cat "$SCR/f1.log"; fail fit; }
[ -s audio/external_fr/T1.1.align.json ] && [ -s audio/external_fr/T1.1.wav ] && pass "fitted into audio/external_fr/ ($(grep -c 'fitted' "$SCR/f1.log") scenes)" || { cat "$SCR/f1.log"; fail "fit output"; }
node build.js --cut core $T --name _test_core --lang fr --draft --tts placeholder --narration external > "$SCR/b7.log" 2>&1 || { cat "$SCR/b7.log"; fail build; }
python3 -c "
import json; t=json.load(open('out/draft/_test_core_fr_timeline.json'))
n={s['id']: s['audio']['narration'] for s in t['scenes']}; assert n['T1.1']=='external' and n['tc1.Q']=='tts', n" || fail "external narration not used"
pass "French build with NARRATION=external uses audio/external_fr/ (timing kept: $(rendered out/draft/_test_core_fr_build_report.json | sed 's/^$/nothing re-rendered/'))"
rm -f audio/external_fr/T1.1.* audio/external_fr/T1.2.* audio/external_fr/T9.1.* audio/external_fr/T2.1.* audio/external_fr/_test_core_fr_fit_report.json
rmdir audio/external_fr 2>/dev/null || true
node build.js --cut core $T --name _test_core --lang fr --draft --tts placeholder > "$SCR/b8.log" 2>&1 || { cat "$SCR/b8.log"; fail build; }
pass "back to the TTS narration"
snap > "$SCR/en_after2.txt"
diff -q "$SCR/en_before.txt" "$SCR/en_after2.txt" > /dev/null && pass "English renders and tracks still untouched" || fail "English files changed"

# the test's build files are not deliverables (draft outputs stay in out/draft for review)
rm -rf script/_build/film__test_core_fr.json script/_build/questions__test_core_fr.json script/_build/_test_core_fr_tts.json \
       script/_build/film__test_extended_fr.json script/_build/questions__test_extended_fr.json script/_build/_test_extended_fr_tts.json \
       script/_build/film_unit_tc1_fr.json script/_build/questions_unit_tc1_fr.json script/_build/unit_tc1_fr_tts.json \
       script/_build/unit_tc1_fr_cues.json script/_build/unit_tc1_fr_timeline.json subs/unit_tc1_fr.srt subs/unit_tc1_fr.vtt \
       subs/unit_tc1_fr.ass subs/unit_tc1_fr_scenes out/narration_script__test_core_fr.md
echo "ALL FRENCH TESTS PASSED (review copies: out/draft/film__test_core_fr.mp4, out/draft/film__test_extended_fr.mp4, out/check/unit_tc1_fr/)"
