#!/usr/bin/env python3
"""Rapport de langue parlée d'une narration du film (video/episodes/<épisode>/narration.md).

Seules les lignes qui commencent par un repère entre crochets, « [repère] texte », sont dites ; les lignes
« > écran : » et « > légende : » ne le sont pas. Le rapport compte, sur la voix seule :
  - les phrases de plus de 20 mots (une ligne peut contenir plusieurs phrases : on coupe sur . ! ?) ;
  - les symboles dictés : « d rond », « nabla », « psi », « oméga », « u x », « u y » ;
  - le nombre de mots et la durée à 150 mots par minute, avec le comptage du moteur
    (video/tools/assemble_cut.py : toute suite de lettres, chiffres, apostrophes et traits d'union est un mot).
Le relecteur-langue part de ce rapport (.claude/agents/relecteur-langue.md).

Usage : python3 tools/lint_narration.py <narration.md> […]   [--max-mots 20] [--strict]
Code de sortie 0, sauf avec --strict s'il reste au moins une phrase longue ou un symbole dicté.
"""
import argparse
import re
import sys

VOICE = re.compile(r"^\[([^\]]+)\]\s*(\S.*)$")
WORD = re.compile(r"[\w'’-]+")
SYMBOLS = {
    "d rond": re.compile(r"\bd\s+rond\b", re.I),
    "nabla": re.compile(r"\bnabla\b", re.I),
    "psi": re.compile(r"\bpsi\b", re.I),
    "oméga": re.compile(r"\bom[ée]ga\b", re.I),
    "u x": re.compile(r"\bu\s+x\b", re.I),
    "u y": re.compile(r"\bu\s+y\b", re.I),
}
WPM = 150


def sentences(text):
    """Coupe une ligne dite en phrases, sans couper un nombre décimal comme « 0,5 » ou « 2. »."""
    parts = re.split(r"(?<=[.!?…])\s+(?=[A-ZÀ-ÖØ-Þ«])", text)
    return [p.strip() for p in parts if p.strip()]


def lint(path, max_words):
    rows = []
    for no, line in enumerate(open(path, encoding="utf-8"), 1):
        m = VOICE.match(line.rstrip("\n"))
        if m:
            rows.append((no, m.group(1), m.group(2)))
    total = sum(len(WORD.findall(t)) for _, _, t in rows)
    longs, dict_ = [], []
    nsent = 0
    for no, cue, text in rows:
        for s in sentences(text):
            nsent += 1
            n = len(WORD.findall(s))
            if n > max_words:
                longs.append((no, cue, n, s))
        for name, rx in SYMBOLS.items():
            k = len(rx.findall(text))
            if k:
                dict_.append((no, cue, name, k, text))
    return {"path": path, "lines": len(rows), "sentences": nsent, "words": total, "longs": longs, "dicted": dict_}


def report(r, max_words):
    w = r["words"]
    print(f"== {r['path']}")
    print(f"voix : {r['lines']} lignes, {r['sentences']} phrases, {w} mots, {w / WPM:.1f} min à {WPM} mots/min "
          f"({int(w // WPM)} min {round(w / WPM % 1 * 60):02d} s)")
    print(f"phrases de plus de {max_words} mots : {len(r['longs'])}")
    for no, cue, n, s in r["longs"]:
        print(f"  l. {no} [{cue}] {n} mots : {s}")
    counts = {}
    for _, _, name, k, _ in r["dicted"]:
        counts[name] = counts.get(name, 0) + k
    tot = sum(counts.values())
    print(f"symboles dictés : {tot}" + (" (" + ", ".join(f"{k} {v}" for k, v in counts.items()) + ")" if tot else ""))
    seen = set()
    for no, cue, name, k, text in r["dicted"]:
        if no not in seen:
            seen.add(no)
            names = sorted({nm for n2, _, nm, _, _ in r["dicted"] if n2 == no})
            print(f"  l. {no} [{cue}] {', '.join(names)} : {text}")
    return len(r["longs"]) + tot


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--max-mots", type=int, default=20)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    bad = 0
    for i, f in enumerate(a.files):
        if i:
            print()
        bad += report(lint(f, a.max_mots), a.max_mots)
    sys.exit(1 if a.strict and bad else 0)


if __name__ == "__main__":
    main()
