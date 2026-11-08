#!/usr/bin/env python3
"""Check English narration g12-g15 against the frozen plan.

The tokenizer is the one in g07-g11-verify.py. Spoken numbers must be
figures that file already accepts from video-grok/INVENTAIRE.md.
"""

from __future__ import annotations

import importlib.util
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("g07_g11_verify", HERE / "g07-g11-verify.py")
g07 = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(g07)

words = g07.words
expand_spoken = g07.expand_spoken
speech_rate = g07.speech_rate
pause_seconds = g07.pause_seconds
clock_s = g07.clock_s
narration_numbers = g07.narration_numbers
inventory_numbers = g07.inventory_numbers
parse_chapter = g07.parse_chapter
spoken_text = g07.spoken_text
cited_text = g07.cited_text
beat_map = g07.beat_map
cue_map = g07.cue_map
slice_between = g07.slice_between
GREEK_IN_SPEECH = g07.GREEK_IN_SPEECH
SPEECH_WPM = g07.SPEECH_WPM
PLAN_WPM = g07.PLAN_WPM

ROOT = HERE.parents[2]
PLAN = ROOT / "video-grok" / "PLAN.md"
INVENTORY = ROOT / "video-grok" / "INVENTAIRE.md"
QUESTIONS = ROOT / "video-grok" / "QUESTIONS.md"
NARRATION = HERE
CHAPTERS = ("g12", "g13", "g14", "g15")

# Figures the plan requires on these beats. Each token is checked against
# the inventory before a chapter is read.
BEAT_FIGURES = {
    "g12.learn": ("100", "2023", "2025"),
    "g12.lawlit": ("100",),
    "g12.gaps": ("6", "2026"),
    "g13.bets": ("10", "12", "64", "100"),
    "g13.cost": ("100",),
    "g14.a": ("1",),
    "g14.c": ("48", "2026"),
}

REQUIRED_CUES = {
    "g12.learn": ("cue.g12.learn.show",),
    "g12.gen": ("cue.g12.gen.show",),
    "g12.lawlit": ("cue.g12.lawlit.show",),
    "g12.people": ("cue.g12.people.show",),
    "g12.gaps": ("cue.g12.gaps.show", "cue.g12.gaps.caveat"),
    "g12.place": ("cue.g12.place.show",),
    "g12.close": ("cue.g12.close.show",),
    "g12.card": ("cue.g12.card",),
    "g13.ladder": ("cue.g13.ladder.show",),
    "g13.bets": (
        "cue.g13.bets.show",
        "cue.g13.bets.blur",
        "cue.g13.bets.tg",
        "cue.g13.bets.anchor",
    ),
    "g13.cost": ("cue.g13.cost.show", "cue.g13.cost.caveat"),
    "g13.close": ("cue.g13.close.show",),
    "g13.card": ("cue.g13.card",),
    "g14.a": ("cue.g14.a.show",),
    "g14.b": ("cue.g14.b.show",),
    "g14.c": ("cue.g14.c.show",),
    "g14.close": ("cue.g14.close.show",),
    "g14.card": ("cue.g14.card",),
    "g15.needle": ("cue.g15.needle.show",),
    "g15.close": ("cue.g15.close.show",),
    "g15.card": ("cue.g15.card",),
}

EXTENDED_SLOTS = {
    "g12": ("16", "43:07", "47:07"),
    "g13": ("17", "47:07", "49:17"),
    "g14": ("19", "53:17", "55:37"),
    "g15": ("21", "59:07", "60:02"),
}


def parse_plan(text: str) -> tuple[dict, dict, str]:
    clock: dict[str, dict] = {}
    clock_region = slice_between(text, "## Horloge du cœur", "## Horloge de l’étendu")
    for line in clock_region.splitlines():
        match = re.match(
            r"^\| (g1[2-5]) \| [^|]+ \| [^|]+ \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+)\u2013([0-9]+:[0-9]+) \| ([0-9]+)\u2013([0-9]+) \|",
            line,
        )
        if match:
            clock[match.group(1)] = {
                "duration": clock_s(match.group(2)),
                "start": clock_s(match.group(3)),
                "end": clock_s(match.group(4)),
                "words": (int(match.group(5)), int(match.group(6))),
            }
    beats: dict[str, list[dict]] = {chapter: [] for chapter in CHAPTERS}
    beat_region = slice_between(text, "## g12 ", "## Modules")
    for line in beat_region.splitlines():
        match = re.match(
            r"^\| ((g1[2-5])\.([a-z0-9]+)) \| ([0-9]+:[0-9]+) \| ([^|]+) \|",
            line,
        )
        if match:
            beats[match.group(2)].append(
                {
                    "id": match.group(1),
                    "duration": clock_s(match.group(4)),
                    "badge": match.group(5).strip(),
                }
            )
    extended = slice_between(text, "## Horloge de l’étendu", "## Statuts")
    return clock, beats, extended


def parse_questions(text: str) -> dict[str, dict]:
    found: dict[str, dict] = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"^### (q\.(g1[2-5])) .* ([ABC])\s*$", line)
        if match:
            current = match.group(2)
            found[current] = {"id": match.group(1), "class": match.group(3), "screen": ""}
            continue
        if current and not found[current]["screen"]:
            screen = re.match(r"^- Écran : `([^`]+)`", line)
            if screen:
                found[current]["screen"] = screen.group(1)
    return found


def check_clocks(clock: dict, beats: dict, extended_text: str, errors: list[str]) -> None:
    if set(clock) != set(CHAPTERS):
        errors.append(f"horloge: chapitres {sorted(clock)} != {list(CHAPTERS)}")
        return
    for chapter, rows in beats.items():
        total = sum(row["duration"] for row in rows)
        if total != clock[chapter]["duration"]:
            errors.append(f"plan: {chapter} somme {total}s, horloge {clock[chapter]['duration']}s")
    for chapter, (order, start, end) in EXTENDED_SLOTS.items():
        row = re.search(
            rf"\| {order} \| {chapter} \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+) \|",
            extended_text,
        )
        if not row or row.group(1) != start or row.group(2) != end:
            errors.append(f"horloge: créneau étendu de {chapter} absent ou déplacé")
            continue
        span = clock_s(row.group(2)) - clock_s(row.group(1))
        if span != clock[chapter]["duration"]:
            errors.append(f"horloge: {chapter} étendu {span}s, cœur {clock[chapter]['duration']}s")


def check_chapter(
    chapter: str,
    parsed: list[dict],
    plan_beats: list[dict],
    clock: dict,
    questions: dict,
    inventory: set[str],
    errors: list[str],
    rates: list[str],
) -> None:
    found = beat_map(parsed)
    expected_ids = [row["id"] for row in plan_beats]
    if [beat["id"] for beat in parsed] != expected_ids:
        errors.append(f"{chapter}: ordre des repères {[beat['id'] for beat in parsed]} != {expected_ids}")
    spoken_all = []
    for row in plan_beats:
        beat = found.get(row["id"])
        if beat is None:
            errors.append(f"{chapter}: repère manquant {row['id']}")
            continue
        actual = clock_s(beat["preamble"].get("duration", "0:00"))
        if actual < row["duration"]:
            errors.append(
                f"{row['id']}: durée {beat['preamble'].get('duration')} plus courte que le plan {row['duration']}s"
            )
        if beat["preamble"].get("badge") != row["badge"]:
            errors.append(f"{row['id']}: pastille {beat['preamble'].get('badge')!r} != {row['badge']!r}")
        cue_ids = [cue["id"] for cue in beat["cues"]]
        if tuple(cue_ids) != REQUIRED_CUES[row["id"]]:
            errors.append(f"{row['id']}: repères {cue_ids} != {list(REQUIRED_CUES[row['id']])}")
        said = spoken_text(beat)
        spoken_all.append(said)
        count = len(words(said))
        limit = 2 * row["duration"] * PLAN_WPM / 60
        if count > limit:
            errors.append(f"R3-budget: {row['id']} a {count} mots, plus du double de son créneau")
        pause = pause_seconds(beat)
        rate = speech_rate(said, actual, pause)
        spoken_n = len(words(expand_spoken(said)))
        rates.append(
            f"débit {row['id']}: {spoken_n} mots dits, {rate:.1f} mots/min, plafond {SPEECH_WPM}"
        )
        if rate > SPEECH_WPM:
            errors.append(
                f"débit: {row['id']} a {spoken_n} mots dits en {actual - pause}s "
                f"après {pause}s de pause, soit {rate:.0f} mots/min, plafond {SPEECH_WPM}"
            )
        cited = narration_numbers(cited_text(beat))
        unknown = sorted(token for token in cited if token not in inventory)
        if unknown:
            errors.append(f"{row['id']}: chiffre absent de l'inventaire: {', '.join(unknown)}")
        for token in BEAT_FIGURES.get(row["id"], ()):
            if token not in cited:
                errors.append(f"{row['id']}: chiffre du plan absent du texte: {token}")
            if token not in inventory:
                errors.append(f"contrat: {token} n'est pas dans l'inventaire")
    chapter_words = len(words("\n".join(spoken_all)))
    narr_seconds = sum(clock_s(beat["preamble"].get("duration", "0:00")) for beat in parsed)
    low, high = clock[chapter]["words"]
    extra = narr_seconds - clock[chapter]["duration"]
    if extra > 0:
        high += math.ceil(extra * PLAN_WPM / 60)
    if not low <= chapter_words <= high:
        errors.append(f"{chapter}: {chapter_words} mots parlés, cible {low}-{high}")
    else:
        print(f"{chapter}: {chapter_words} mots parlés, cible {low}-{high}")
    if chapter in questions:
        card = found.get(f"{chapter}.card")
        if card is None:
            errors.append(f"{chapter}: carte absente")
        else:
            screen = questions[chapter]["screen"]
            cue = next((item for item in card["cues"] if item["id"] == f"cue.{chapter}.card"), None)
            said = cue["text"] if cue else ""
            if said != screen or card["preamble"].get("class") != questions[chapter]["class"]:
                errors.append(f"{chapter}.card: phrase ou classe != {questions[chapter]['id']}")
            if cue and cue["preamble"].get("screen") != screen:
                errors.append(f"{chapter}.card: écran != registre")
            if len(words(screen)) > 18:
                errors.append(f"{chapter}.card: plus de 18 mots")
    joined = "\n".join(spoken_all)
    if GREEK_IN_SPEECH.search(joined) or "(" in joined or ")" in joined or ":" in joined or "\u2014" in joined:
        errors.append(f"{chapter}: le parlé contient un symbole, des parenthèses, deux-points, ou un tiret long")
    if "KL" in joined or "we obtained" in joined.lower() or "±" in joined:
        errors.append(f"{chapter}: KL, we obtained, ou ± dans le parlé")
    if re.search(r"\bx0[1-5]\b", joined):
        errors.append(f"{chapter}: le cœur annonce un module x")


def need(cues: dict, cue_id: str, phrase: str, code: str, errors: list[str]) -> None:
    cue = cues.get(cue_id)
    if cue is None or phrase not in cue["text"]:
        errors.append(f"{code}: {cue_id} ne contient pas {phrase!r}")


def forbid(cues: dict, cue_id: str, phrase: str, code: str, errors: list[str]) -> None:
    cue = cues.get(cue_id)
    if cue and phrase in cue["text"]:
        errors.append(f"{code}: {cue_id} contient encore {phrase!r}")


def check_reservations(chapters: dict, errors: list[str]) -> None:
    cues: dict = {}
    for parsed in chapters.values():
        cues.update(cue_map(parsed))
    need(cues, "cue.g12.learn.show", "map of families, not a catalog", "R3-g12", errors)
    need(cues, "cue.g12.learn.show", "compressed representation of the field", "pedagogy-g12", errors)
    need(cues, "cue.g12.learn.show", "not one paper by its name", "R3-g12", errors)
    need(cues, "cue.g12.gen.show", "Leray projection", "pedagogy-g12", errors)
    need(cues, "cue.g12.gen.show", "No strategy wins everywhere.", "plan-g12", errors)
    need(cues, "cue.g12.lawlit.show", "dimension 100", "plan-g12", errors)
    need(cues, "cue.g12.lawlit.show", "changes the weight of the samples", "pedagogy-g12", errors)
    need(cues, "cue.g12.lawlit.show", "changes the probabilities under an existing law", "science-g12", errors)
    need(cues, "cue.g12.lawlit.show", "weak residual", "plan-g12", errors)
    forbid(cues, "cue.g12.lawlit.show", "does not draw a new field", "science-g12", errors)
    forbid(cues, "cue.g12.gen.show", "FunDiff", "pedagogy-g12", errors)
    forbid(cues, "cue.g12.gen.show", "PIDM", "pedagogy-g12", errors)
    forbid(cues, "cue.g12.gen.show", "PCDM", "pedagogy-g12", errors)
    if cues.get("cue.g12.gen.show", {}).get("preamble", {}).get("screen") != "FunDiff, PIDM, PCDM":
        errors.append("pedagogy-g12: FunDiff, PIDM et PCDM ne sont pas à l'écran")
    if cues.get("cue.g13.cost.show", {}).get("preamble", {}).get("screen") != "A100":
        errors.append("pedagogy-g13: A100 n'est pas à l'écran")
    need(cues, "cue.g12.people.show", "TorchDA", "plan-g12", errors)
    need(cues, "cue.g12.people.show", "SFEMaNS", "plan-g12", errors)
    need(cues, "cue.g12.people.show", "LATU", "plan-g12", errors)
    need(cues, "cue.g12.people.show", "Taylor-Green", "plan-g12", errors)
    need(cues, "cue.g12.gaps.show", "MHD works that were examined", "science-g12", errors)
    need(cues, "cue.g12.gaps.show", "magnetic energy budgets", "science-g12", errors)
    need(cues, "cue.g12.gaps.caveat", "November 6, 2026", "caveat-g12", errors)
    need(cues, "cue.g12.gaps.caveat", "medium confidence", "caveat-g12", errors)
    need(cues, "cue.g12.gaps.caveat", "cannot be proved", "caveat-g12", errors)
    need(cues, "cue.g12.gaps.caveat", "do not close these gaps", "caveat-g12", errors)
    need(cues, "cue.g12.gaps.caveat", "high confidence", "caveat-g12", errors)
    need(cues, "cue.g12.place.show", "coupled three-dimensional MHD generator with walls", "science-g12", errors)
    need(cues, "cue.g12.place.show", "kinematic dynamo", "science-g12", errors)
    forbid(cues, "cue.g12.place.show", "do not scale to three dimensions", "science-g12", errors)
    need(cues, "cue.g12.place.show", "mechanisms on toys", "plan-g12", errors)
    need(cues, "cue.g12.place.show", "conditional generator", "plan-g12", errors)
    need(cues, "cue.g12.place.show", "Rice frequency", "plan-g12", errors)
    need(cues, "cue.g12.place.show", "not a result already obtained", "plan-g12", errors)
    need(cues, "cue.g12.close.show", "not one method by name", "R3-g12", errors)
    need(cues, "cue.g12.close.show", "cannot sign", "plan-g12", errors)
    need(cues, "cue.g13.ladder.show", "walled cylinder", "couture-g13", errors)
    need(cues, "cue.g13.ladder.show", "first rung dropped", "plan-g13", errors)
    need(cues, "cue.g13.bets.show", "10 to the minus 12", "plan-g13", errors)
    need(cues, "cue.g13.bets.show", "periodic decoder built from potentials", "science-g13", errors)
    need(cues, "cue.g13.bets.show", "discrete operators", "science-g13", errors)
    need(cues, "cue.g13.bets.show", "Coulomb gauge alone does not guarantee", "science-g13", errors)
    need(cues, "cue.g13.bets.show", "numerical check", "science-g13", errors)
    forbid(cues, "cue.g13.bets.show", "code fault", "science-g13", errors)
    need(cues, "cue.g13.bets.blur", "miss the jump", "plan-g13", errors)
    need(cues, "cue.g13.bets.blur", "only medium", "plan-g13", errors)
    forbid(cues, "cue.g13.bets.blur", "Still empty", "pedagogy-g13", errors)
    need(cues, "cue.g13.bets.tg", "No Taylor-Green threshold is stated.", "plan-g13", errors)
    need(cues, "cue.g13.bets.tg", "spectra decay", "plan-g13", errors)
    forbid(cues, "cue.g13.bets.tg", "Still empty", "pedagogy-g13", errors)
    need(cues, "cue.g13.bets.anchor", "Anchoring limits how far fine-tuning can move from the starting model.", "pedagogy-g13", errors)
    need(cues, "cue.g13.bets.anchor", "Do not say the loss works in three dimensions.", "plan-g13", errors)
    forbid(cues, "cue.g13.bets.anchor", "Still empty", "pedagogy-g13", errors)
    need(cues, "cue.g13.cost.show", "about eleven thousand", "pedagogy-g13", errors)
    need(cues, "cue.g13.cost.show", "factor of two", "plan-g13", errors)
    need(cues, "cue.g13.cost.caveat", "No GPU measurement", "caveat-g13", errors)
    need(cues, "cue.g13.cost.caveat", "purchase order", "caveat-g13", errors)
    need(cues, "cue.g13.close.show", "one after another", "R3-g13", errors)
    need(cues, "cue.g13.close.show", "No three-dimensional field has been generated.", "oral-g13", errors)
    forbid(cues, "cue.g13.close.show", "one sentence", "pedagogy-g13", errors)
    need(cues, "cue.g14.b.show", "does not rewrite them", "plan-g14", errors)
    need(cues, "cue.g14.b.show", "A snapshot is one moment.", "pedagogy-g14", errors)
    forbid(cues, "cue.g14.b.show", "This chapter names", "pedagogy-g14", errors)
    need(cues, "cue.g14.c.show", "48 months", "plan-g14", errors)
    need(cues, "cue.g14.c.show", "No price is read out.", "plan-g14", errors)
    forbid(cues, "cue.g14.c.show", "euro table", "pedagogy-g14", errors)
    need(cues, "cue.g14.a.show", "trajectory count to 1", "plan-g14", errors)
    need(cues, "cue.g14.a.show", "stationarity-loss weight set to zero", "science-g14", errors)
    forbid(cues, "cue.g14.a.show", "witness at zero weight", "pedagogy-g14", errors)
    need(cues, "cue.g14.close.show", "A, then B, then C", "plan-g14", errors)
    forbid(cues, "cue.g14.close.show", "not read aloud", "pedagogy-g14", errors)
    need(cues, "cue.g15.needle.show", "not to time scale", "plan-g15", errors)
    need(cues, "cue.g15.needle.show", "has not been made", "plan-g15", errors)
    need(cues, "cue.g15.needle.show", "No three-dimensional field has been generated.", "plan-g15", errors)
    need(cues, "cue.g15.close.show", "Sibo Cheng", "credits", errors)
    need(cues, "cue.g15.close.show", "Didier Lucor", "credits", errors)
    need(cues, "cue.g15.close.show", "Caroline Nore", "credits", errors)
    need(cues, "cue.g15.close.show", "Yannick Ponty", "credits", errors)
    need(cues, "cue.g15.close.show", "grant number stays on screen", "pedagogy-g15", errors)
    forbid(cues, "cue.g15.close.show", "ANR-25", "pedagogy-g15", errors)
    if cues.get("cue.g15.close.show", {}).get("preamble", {}).get("screen") != "ANR-25-CE51-0077":
        errors.append("credits: le numéro ANR n'est pas à l'écran")
    need(cues, "cue.g15.close.show", "prospective", "oral-g15", errors)
    need(cues, "cue.g15.close.show", "not endorsed", "oral-g15", errors)
    need(cues, "cue.g15.close.show", "No logo.", "plan-g15", errors)
    need(cues, "cue.g15.close.show", "No opinion.", "plan-g15", errors)


def load_chapters(only: str | None) -> dict[str, list[dict]]:
    loaded = {}
    missing = []
    for chapter in CHAPTERS:
        if only and chapter != only:
            continue
        path = NARRATION / f"{chapter}.md"
        if not path.exists():
            missing.append(chapter)
            continue
        loaded[chapter] = parse_chapter(path)
    if missing:
        raise SystemExit("chapitres manquants: " + ", ".join(missing))
    return loaded


def self_test() -> list[str]:
    errors = []
    if speech_rate is not g07.speech_rate or words is not g07.words:
        errors.append("self-test: le tokenizer n'est pas celui de g07-g11")
    spelled = expand_spoken("Reynolds number 100, and 1.1 times 10 to the 4")
    if "one hundred" not in spelled or "one point one" not in spelled or "ten" not in spelled:
        errors.append(f"self-test épelage: {spelled}")
    if speech_rate(" ".join(["word"] * 100), 30, 0) <= SPEECH_WPM:
        errors.append("self-test débit: 100 mots en 30 s passent le plafond")
    inventory = inventory_numbers(INVENTORY.read_text())
    for tokens in BEAT_FIGURES.values():
        for token in tokens:
            if token not in inventory:
                errors.append(f"self-test: ancre {token} absente de l'inventaire")
    return errors


def main(argv: list[str]) -> int:
    only = None
    if "--chapter" in argv:
        only = argv[argv.index("--chapter") + 1]
    if "--self-test" in argv:
        errors = self_test()
        if errors:
            print("\n".join(errors))
            return 1
        print("self-test: tokenizer g07 et ancres conformes à l'inventaire")
        if "--chapter" not in argv:
            return 0
    else:
        errors = self_test()
        if errors:
            print("\n".join(errors))
            return 1
    inventory = inventory_numbers(INVENTORY.read_text())
    plan = PLAN.read_text()
    clock, plan_beats, extended = parse_plan(plan)
    questions = parse_questions(QUESTIONS.read_text())
    errors: list[str] = []
    check_clocks(clock, plan_beats, extended, errors)
    if set(questions) != set(CHAPTERS):
        errors.append(f"registre: cartes {sorted(questions)} incomplètes")
    chapters = load_chapters(only)
    rates: list[str] = []
    for chapter, parsed in chapters.items():
        check_chapter(chapter, parsed, plan_beats[chapter], clock, questions, inventory, errors, rates)
    if only is None:
        check_reservations(chapters, errors)
    if errors:
        print("\n".join(errors))
        return 1
    print("\n".join(rates))
    scope = only or "g12-g15"
    print(f"{scope}: chiffres, repères, cartes et horloges tenus")
    print("tokenizer: un mot est un jeton [A-Za-z0-9] avec point, virgule interne, ou trait d'union")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
