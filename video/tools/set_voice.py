#!/usr/bin/env python3
"""set_voice.py: choose the narrator voice for every cut without editing the unit scripts (narration swap).

  python3 -I tools/set_voice.py <reference_id>   writes audio/voice.json; tools/assemble_cut.py then uses this
                                                 voice instead of the scripts' voice.reference_id
  python3 -I tools/set_voice.py default          removes audio/voice.json (back to the scripts' voice)
  python3 -I tools/set_voice.py                  shows the current choice
  --lang fr (before the argument)                the same for the French narration: audio/voice_fr.json, which
                                                 overrides the overlays' "voice" (script/fr/<unit>.json) and the
                                                 scripts' "voice_fr" (make narration LANG=fr VOICE=...)
Only an original Fish Audio library voice, or a voice you hold the rights to, may be used: never a clone or
an imitation of a real person (BRIEF D1). The TTS cache is keyed by voice (and language), so going back to a
previous voice costs nothing: its paragraphs are still in audio/cache/.
"""
import datetime, json, os, re, sys

args = sys.argv[1:]
lang = "en"
if args[:1] == ["--lang"]:
    lang, args = (args[1] if len(args) > 1 else ""), args[2:]
if lang not in ("en", "fr"):
    sys.exit(f"--lang {lang!r}: en or fr")
AUDIO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio")
P = os.path.join(AUDIO, "voice.json" if lang == "en" else f"voice_{lang}.json")
what = "" if lang == "en" else f" ({lang} narration)"
src = "voice.reference_id" if lang == "en" else f"overlay 'voice' (script/{lang}/<unit>.json) or 'voice_{lang}'"
arg = args[0] if args else None
if arg is None:
    print(open(P).read() if os.path.exists(P) else f"no override{what}: the scripts' {src} is used")
elif arg == "default":
    if os.path.exists(P):
        os.remove(P)
    print(f"voice override removed{what}: the scripts' {src} is used")
elif re.fullmatch(r"[0-9a-f]{32}", arg):
    json.dump({"reference_id": arg, "lang": lang, "set": datetime.datetime.now().isoformat(timespec="seconds"),
               "note": f"narration swap (make narration{'' if lang == 'en' else ' LANG=' + lang} VOICE=...); "
                       f"remove with: make narration{'' if lang == 'en' else ' LANG=' + lang} VOICE=default"},
              open(P, "w"), indent=1)
    print(f"voice override set{what}: {arg}")
else:
    sys.exit(f"not a Fish Audio reference_id (32 hex characters): {arg!r}")
