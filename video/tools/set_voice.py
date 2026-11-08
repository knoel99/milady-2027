#!/usr/bin/env python3
"""set_voice.py: choose the narrator voice for every cut without editing the unit scripts (narration swap).

  python3 -I tools/set_voice.py <reference_id>   writes audio/voice.json; tools/assemble_cut.py then uses this
                                                 voice instead of the scripts' voice.reference_id
  python3 -I tools/set_voice.py default          removes audio/voice.json (back to the scripts' voice)
  python3 -I tools/set_voice.py                  shows the current choice
Only an original Fish Audio library voice, or a voice you hold the rights to, may be used: never a clone or
an imitation of a real person (BRIEF D1). The TTS cache is keyed by voice, so going back to a previous voice
costs nothing: its paragraphs are still in audio/cache/.
"""
import datetime, json, os, re, sys

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio", "voice.json")
arg = sys.argv[1] if len(sys.argv) > 1 else None
if arg is None:
    print(open(P).read() if os.path.exists(P) else "no override: the voice of the unit scripts (voice.reference_id) is used")
elif arg == "default":
    if os.path.exists(P):
        os.remove(P)
    print("voice override removed: the unit scripts' voice.reference_id is used")
elif re.fullmatch(r"[0-9a-f]{32}", arg):
    json.dump({"reference_id": arg, "set": datetime.datetime.now().isoformat(timespec="seconds"),
               "note": "narration swap (make narration VOICE=...); remove with: make narration VOICE=default"}, open(P, "w"), indent=1)
    print(f"voice override set: {arg}")
else:
    sys.exit(f"not a Fish Audio reference_id (32 hex characters): {arg!r}")
