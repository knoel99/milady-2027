#!/usr/bin/env python3
"""extract_data.py: kept for compatibility with the plan documents and BRIEF section 4.

The prototype extractor (e1_rate.json, the palier1 E2 stand-in) is superseded by foundation engineer B's
converters (CONTRACT.md section 5):
  tools/data_existing.py   READY scenes: the repository's existing results -> data/*.json
  tools/data_cloud.py      PENDING scenes: cloud outputs -> data/*.json (run by hand, see its docstring)
This wrapper only runs tools/data_existing.py with the same arguments (`make data` does the same).
Usage: python3 -I tools/extract_data.py [--repo /home/user/milady-2027] [--check]
"""
import os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
conv = os.path.join(here, "data_existing.py")
if not os.path.exists(conv):
    sys.exit("[extract_data] tools/data_existing.py is not in this film yet: nothing to convert")
sys.exit(subprocess.call([sys.executable, "-I", conv, *sys.argv[1:]]))
