#!/usr/bin/env python3
"""Check English narration g00-g06 against the frozen plan.

Spoken numbers must be the same figures as video-grok/INVENTAIRE.md.
The word tokenizer and the 156 word per minute cap are the g07-g11 verifier.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "video-grok" / "PLAN.md"
INVENTORY = ROOT / "video-grok" / "INVENTAIRE.md"
QUESTIONS = ROOT / "video-grok" / "QUESTIONS.md"
INCERTITUDES = ROOT / "video-grok" / "INCERTITUDES.md"
NARRATION = ROOT / "video-grok" / "narration" / "en"
CHAPTERS = ("g00", "g01", "g02", "g03", "g04", "g05", "g06")
CARD_CHAPTERS = ("g01", "g02", "g03", "g04", "g05", "g06")

# The shared inventory parser glues a trailing superscript ³ onto the digits,
# so the LATU grid written 384³ is stored as 3843. The spoken line says 384.
LATU_GRID = "384"

BEAT_FIGURES = {
    "g02.sodium": ("0.82e-5", "120"),
    "g03.riga": ("1999", "2150", "205", "0.0315", "0.0009", "1.326", "55"),
    "g03.karlsruhe": ("1999", "52"),
    "g03.vks": ("0.6", "31", "16", "22", "120", "50", "5", "0.4"),
    "g03.defs": ("31", "44", "52", "71"),
    "g04.cowling": ("1933",),
    "g04.sim": ("2018", "90", "5", "130", "10", "1.5", "50", LATU_GRID),
    "g04.reduced": ("2000",),
    "g04.stats": ("2012",),
    "g05.project": ("2026", "48", "560612", "25", "0077"),
    "g05.offer": ("2027",),
}

EMPTY_FIGURES = {
    "g00.needle",
    "g00.title",
    "g01.earth",
    "g01.rate",
    "g01.close",
    "g01.card",
    "g02.stretch",
    "g03.dresdyn",
    "g06.recap",
    "g06.card",
}

PREDICT = {
    "cue.g01.rate.predict",
    "cue.g02.ratio.predict",
    "cue.g05.snapshot.predict",
}


def _lot():
    path = Path(__file__).with_name("g07-g11-verify.py")
    spec = importlib.util.spec_from_file_location("g07_g11_verify", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LOT = _lot()
words = LOT.words
expand_spoken = LOT.expand_spoken
speech_rate = LOT.speech_rate
narration_numbers = LOT.narration_numbers
inventory_numbers = LOT.inventory_numbers
parse_chapter = LOT.parse_chapter
spoken_text = LOT.spoken_text
pause_seconds = LOT.pause_seconds
clock_s = LOT.clock_s
beat_map = LOT.beat_map
cue_map = LOT.cue_map
GREEK_IN_SPEECH = LOT.GREEK_IN_SPEECH
SPEECH_WPM = LOT.SPEECH_WPM
PLAN_WPM = LOT.PLAN_WPM


def allowed_numbers(text: str) -> set[str]:
    found = inventory_numbers(text)
    if "384³" in text:
        found.add(LATU_GRID)
    return found


def slice_between(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    finish = text.index(end, begin + len(start))
    return text[begin:finish]


def parse_plan(text: str) -> tuple[dict, dict, set[str]]:
    clock: dict[str, dict] = {}
    clock_region = slice_between(text, "## Horloge du cœur", "## Horloge de l’étendu")
    for line in clock_region.splitlines():
        match = re.match(
            r"^\| (g0[0-6]) \| [^|]+ \| [^|]+ \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+)\u2013([0-9]+:[0-9]+) \| ([0-9]+)\u2013([0-9]+) \|",
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
    beat_region = slice_between(text, "## g00 ", "## g07 ")
    for line in beat_region.splitlines():
        match = re.match(
            r"^\| ((g0[0-6])\.([a-z0-9]+)) \| ([0-9]+:[0-9]+) \| ([^|]+) \|",
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
    cues = set(re.findall(r"cue\.g0[0-6]\.[a-z0-9.]+", beat_region))
    return clock, beats, cues


def stripes_still_unpinned(text: str) -> bool:
    section = slice_between(text, "## E. Faits externes bloqués", "## U8.")
    row = re.search(
        r"\| Bandes magnétiques des fonds océaniques \| ([^|]+) \|",
        section,
    )
    return bool(row and "aucune ligne" in row.group(1))


def apply_stripes(beats: dict, incertitudes: str, errors: list[str]) -> None:
    """Ocean-floor stripes have no pinned source, so PLAN folds their time into g01.rate."""
    rows = beats["g01"]
    stripes = next((row for row in rows if row["id"] == "g01.stripes"), None)
    rate = next((row for row in rows if row["id"] == "g01.rate"), None)
    if stripes is None or rate is None:
        errors.append("plan: g01.stripes ou g01.rate manque dans le tableau")
        return
    if not stripes_still_unpinned(incertitudes):
        errors.append("§E: la coupe des bandes n'est plus le texte d'INCERTITUDES, ne pas deviner")
        return
    if stripes["duration"] != 25 or rate["duration"] != 40:
        errors.append(
            f"plan: g01.stripes {stripes['duration']}s et g01.rate {rate['duration']}s, attendu 25 et 40 avant report"
        )
    rate["duration"] += stripes["duration"]
    beats["g01"] = [row for row in rows if row["id"] != "g01.stripes"]
    if any(row["id"] == "g02.disk" for row in beats["g02"]):
        errors.append("plan: g02.disk a une ligne alors que §E n'a pas de source")


def parse_questions(text: str) -> dict[str, dict]:
    found: dict[str, dict] = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"^### (q\.(g0[1-6])) .* ([ABC])\s*$", line)
        if match:
            current = match.group(2)
            found[current] = {"id": match.group(1), "class": match.group(3), "screen": ""}
            continue
        if current and not found[current]["screen"]:
            screen = re.match(r"^- Écran : `([^`]+)`", line)
            if screen:
                found[current]["screen"] = screen.group(1)
    return found


def cited_text(beat: dict) -> str:
    parts = []
    for cue in beat["cues"]:
        parts.append(cue["text"])
        if "screen" in cue["preamble"]:
            parts.append(cue["preamble"]["screen"])
    return "\n".join(parts)


def check_clocks(clock: dict, beats: dict, errors: list[str]) -> None:
    if set(clock) != set(CHAPTERS):
        errors.append(f"horloge: chapitres {sorted(clock)} incomplets")
        return
    for chapter, rows in beats.items():
        total = sum(row["duration"] for row in rows)
        if total != clock[chapter]["duration"]:
            errors.append(f"plan: {chapter} somme {total}s, horloge {clock[chapter]['duration']}s")
    if clock["g00"]["start"] != 0:
        errors.append("horloge: g00 ne part pas de 0:00")
    for earlier, later in zip(CHAPTERS, CHAPTERS[1:]):
        if clock[earlier]["end"] != clock[later]["start"]:
            errors.append(f"horloge: {earlier} ne touche pas {later}")


def check_chapter(
    chapter: str,
    parsed: list[dict],
    plan_beats: list[dict],
    clock: dict,
    questions: dict,
    inventory: set[str],
    errors: list[str],
    rates: list[dict],
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
        if clock_s(beat["preamble"].get("duration", "0:00")) != row["duration"]:
            errors.append(f"{row['id']}: durée {beat['preamble'].get('duration')} != plan")
        if beat["preamble"].get("badge") != row["badge"]:
            errors.append(f"{row['id']}: pastille {beat['preamble'].get('badge')!r} != {row['badge']!r}")
        said = spoken_text(beat)
        spoken_all.append(said)
        count = len(words(said))
        limit = 2 * row["duration"] * PLAN_WPM / 60
        if count > limit:
            errors.append(f"R3-budget: {row['id']} a {count} mots, plus du double de son créneau")
        pause = pause_seconds(beat)
        rate = speech_rate(said, row["duration"], pause)
        spoken_n = len(words(expand_spoken(said)))
        rates.append(
            {
                "id": row["id"],
                "duration": row["duration"],
                "pause": pause,
                "words": spoken_n,
                "rate": round(rate, 1),
                "cues": [cue["id"] for cue in beat["cues"]],
            }
        )
        if rate > SPEECH_WPM:
            errors.append(
                f"débit: {row['id']} a {spoken_n} mots dits en {row['duration'] - pause}s "
                f"après {pause}s de pause, soit {rate:.0f} mots/min, plafond {SPEECH_WPM}"
            )
        cited = narration_numbers(cited_text(beat))
        unknown = sorted(token for token in cited if token not in inventory)
        if unknown:
            errors.append(f"{row['id']}: chiffre absent de l'inventaire: {', '.join(unknown)}")
        if row["id"] in EMPTY_FIGURES and cited:
            errors.append(f"{row['id']}: chiffre interdit sur ce repère: {', '.join(sorted(cited))}")
        for token in BEAT_FIGURES.get(row["id"], ()):
            if token not in cited:
                errors.append(f"{row['id']}: chiffre du plan absent du texte: {token}")
            if token not in inventory:
                errors.append(f"contrat: {token} n'est pas dans l'inventaire")
    chapter_words = len(words("\n".join(spoken_all)))
    low, high = clock[chapter]["words"]
    if not low <= chapter_words <= high:
        errors.append(f"{chapter}: {chapter_words} mots parlés, cible {low}-{high}")
    else:
        print(f"{chapter}: {chapter_words} mots parlés, cible {low}-{high}", file=sys.stderr)
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
    elif any(beat["id"].endswith(".card") for beat in parsed):
        errors.append(f"{chapter}: carte alors que le registre n'en a pas")
    joined = "\n".join(spoken_all)
    if GREEK_IN_SPEECH.search(joined) or "(" in joined or ")" in joined or ":" in joined or "\u2014" in joined:
        errors.append(f"{chapter}: le parlé contient un symbole, des parenthèses, deux-points, ou un tiret long")
    if "KL" in joined or "we obtained" in joined.lower() or "±" in joined or "170" in joined:
        errors.append(f"{chapter}: KL, we obtained, ±, ou 170 dans le parlé")


def check_named_cues(chapters: dict, required: set[str], errors: list[str]) -> None:
    present = {}
    for parsed in chapters.values():
        present.update(cue_map(parsed))
    for cue_id in sorted(required):
        if cue_id not in present:
            errors.append(f"repère nommé absent: {cue_id}")
    for cue_id in PREDICT:
        cue = present.get(cue_id)
        if cue is None:
            errors.append(f"pause predict absente: {cue_id}")
            continue
        if cue["preamble"].get("pause") not in ("2s", "3s"):
            errors.append(f"{cue_id}: pause {cue['preamble'].get('pause')!r} hors 2s-3s")
        if cue["preamble"].get("role") != "spoken":
            errors.append(f"{cue_id}: la pause predict doit être dite")


def need(cues: dict, cue_id: str, phrase: str, code: str, errors: list[str]) -> None:
    cue = cues.get(cue_id)
    if cue is None or phrase not in cue["text"]:
        errors.append(f"{code}: {cue_id} ne contient pas {phrase!r}")


def check_reservations(chapters: dict, errors: list[str]) -> None:
    cues = {}
    spoken = {}
    for chapter, parsed in chapters.items():
        cues.update(cue_map(parsed))
        spoken[chapter] = "\n".join(spoken_text(beat) for beat in parsed)
        if any(beat["id"] == "g01.stripes" for beat in parsed):
            errors.append("§E: g01.stripes est écrit alors que la source n'est pas épinglée")
        if any(beat["id"] == "g02.disk" for beat in parsed):
            errors.append("§E: g02.disk est écrit alors que la source n'est pas épinglée")

    need(cues, "cue.g00.needle.show", "illustration, not to time scale", "g00", errors)
    need(cues, "cue.g00.needle.start", "south", "g00", errors)
    need(cues, "cue.g01.earth.show", "illustration, not to time scale", "g01", errors)
    need(cues, "cue.g01.earth.show", "No reversal age is pinned", "g01", errors)
    need(cues, "cue.g01.rate.show", "that picture is cut", "g01", errors)
    need(cues, "cue.g01.rate.caveat", "No Earth rate is stated", "g01", errors)
    need(cues, "cue.g01.rate.caveat", "not shown", "g01", errors)
    need(cues, "cue.g02.stretch.show", "No disk threshold is stated", "g02", errors)
    formula = cues.get("cue.g02.ratio.formula")
    predict = cues.get("cue.g02.ratio.predict")
    ratio_ids = [cue["id"] for beat in chapters.get("g02", []) for cue in beat["cues"] if beat["id"] == "g02.ratio"]
    if ratio_ids[:2] != ["cue.g02.ratio.predict", "cue.g02.ratio.formula"]:
        errors.append(f"g02: la formule précède le predict {ratio_ids}")
    if not formula or formula["preamble"].get("role") != "unread":
        errors.append("g02: Rm = UL/η doit être non lu")
    if not predict or predict["preamble"].get("role") != "spoken":
        errors.append("g02: le predict du rapport doit être dit")
    need(cues, "cue.g02.sodium.show", "0.82 times 10 to the minus 5", "g02", errors)
    need(cues, "cue.g02.sodium.show", "several million", "g02", errors)
    need(cues, "cue.g03.riga.caveat", "later machine", "g03", errors)
    need(cues, "cue.g03.riga.show", "two motors of 55 kilowatts", "g03", errors)
    riga_numbers = narration_numbers(spoken_text(next(beat for beat in chapters.get("g03", []) if beat["id"] == "g03.riga")))
    if "100" in riga_numbers or "200" in riga_numbers:
        errors.append("g03.riga: un autre chiffre de motorisation est entré dans le plan")
    need(cues, "cue.g03.vks.caveat", "schematic", "g03", errors)
    need(cues, "cue.g03.vks.caveat", "not the VKS measurements", "g03", errors)
    need(cues, "cue.g03.defs.show", "not the same", "g03", errors)
    need(cues, "cue.g03.dresdyn.show", "no numeric window", "g03", errors)
    need(cues, "cue.g03.dresdyn.show", "not claimed", "g03", errors)
    g04 = spoken.get("g04", "")
    if "Glatzmaier" in g04 or "Larmor" in g04:
        errors.append("§E: g04 date une source encore bloquée")
    need(cues, "cue.g04.sim.caveat", "No source is pinned", "g04", errors)
    need(cues, "cue.g04.reduced.show", "not public", "g04", errors)
    need(cues, "cue.g04.stats.show", "Poissonian", "g04", errors)
    need(cues, "cue.g04.stats.caveat", "not an Earth rate", "g04", errors)
    need(cues, "cue.g05.project.show", "ANR-25-CE51-0077", "g05", errors)
    need(cues, "cue.g05.offer.show", "prospective", "g05", errors)
    need(cues, "cue.g05.offer.show", "not endorsed", "g05", errors)
    snap = [cue["id"] for beat in chapters.get("g05", []) for cue in beat["cues"] if beat["id"] == "g05.snapshot"]
    if snap[:2] != ["cue.g05.snapshot.predict", "cue.g05.snapshot.show"]:
        errors.append(f"g05: la distinction précède le predict {snap}")
    need(cues, "cue.g05.snapshot.show", "time derivative", "g05", errors)
    names = cues.get("cue.g05.names.show", {"text": ""})["text"]
    for name in ("Cheng", "Lucor", "Nore", "Ponty"):
        if name not in names:
            errors.append(f"g05.names: {name} manque")
    if "opinion" not in names:
        errors.append("g05.names: le refus d'opinion manque")
    need(cues, "cue.g06.recap.show", "illustration, not to time scale", "g06", errors)
    need(cues, "cue.g06.recap.show", "Nothing in this recap is a new idea", "g06", errors)


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
    inventory = allowed_numbers(INVENTORY.read_text())
    if LATU_GRID not in inventory:
        errors.append("self-test: 384 n'est pas rétabli depuis 384³")
    if "3843" not in inventory_numbers(INVENTORY.read_text()):
        errors.append("self-test: le parseur partagé ne colle plus 384³")
    if "0.999" in inventory:
        errors.append("self-test: 0.999 est dans l'inventaire")
    if speech_rate(" ".join(["word"] * 100), 30, 0) <= SPEECH_WPM:
        errors.append("self-test débit: 100 mots en 30 s passent le plafond")
    if speech_rate("illustration, not to time scale", 15, 0) > SPEECH_WPM:
        errors.append("self-test débit: la légende dépasse le plafond")
    sample = "0.82 times 10 to the minus 5 at 120 degrees, and 560,612 euros"
    if LOT.narration_numbers(sample) != narration_numbers(sample):
        errors.append("self-test: le parseur de chiffres a divergé")
    if LOT.expand_spoken(sample) != expand_spoken(sample):
        errors.append("self-test: l'épelage a divergé")
    for tokens in BEAT_FIGURES.values():
        for token in tokens:
            if token not in inventory:
                errors.append(f"self-test: ancre {token} absente de l'inventaire")
    return errors


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    only = None
    if "--chapter" in argv:
        only = argv[argv.index("--chapter") + 1]
    errors = self_test()
    if "--self-test" in argv and "--chapter" not in argv and not as_json:
        if errors:
            print("\n".join(errors))
            return 1
        print("self-test: extracteurs, 384, et plafond 156 tenus")
        return 0
    if errors:
        print("\n".join(errors))
        return 1
    inventory = allowed_numbers(INVENTORY.read_text())
    plan = PLAN.read_text()
    clock, plan_beats, cues = parse_plan(plan)
    apply_stripes(plan_beats, INCERTITUDES.read_text(), errors)
    questions = parse_questions(QUESTIONS.read_text())
    check_clocks(clock, plan_beats, errors)
    if set(questions) != set(CARD_CHAPTERS):
        errors.append(f"registre: cartes {sorted(questions)} incomplètes")
    if errors:
        print("\n".join(errors))
        return 1
    chapters = load_chapters(only)
    rates: list[dict] = []
    for chapter, parsed in chapters.items():
        check_chapter(chapter, parsed, plan_beats[chapter], clock, questions, inventory, errors, rates)
    if only is None:
        check_named_cues(chapters, cues, errors)
        check_reservations(chapters, errors)
    if errors:
        print("\n".join(errors))
        return 1
    if as_json:
        print(json.dumps({"chapters": list(CHAPTERS), "beats": rates, "ceiling": SPEECH_WPM}, ensure_ascii=False))
        return 0
    for row in rates:
        print(
            f"{row['id']}: {row['words']} mots dits, {row['rate']:.1f} mots/min, "
            f"{row['duration'] - row['pause']}s de parole"
        )
    scope = only or "g00-g06"
    print(f"{scope}: chiffres, repères, cartes et horloges tenus")
    print("tokenizer: un mot est un jeton [A-Za-z0-9] avec point, virgule interne, ou trait d'union")
    print(f"débit ≤ {SPEECH_WPM}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
