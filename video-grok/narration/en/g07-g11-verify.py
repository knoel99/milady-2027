#!/usr/bin/env python3
"""Check English narration g07-g11 against the frozen plan.

Spoken numbers must be the same figures as video-grok/INVENTAIRE.md.
Inventory decimals use a comma. English narration uses a dot.
Thousands separators go the other way. The two parsers do not share a rule.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "video-grok" / "PLAN.md"
INVENTORY = ROOT / "video-grok" / "INVENTAIRE.md"
QUESTIONS = ROOT / "video-grok" / "QUESTIONS.md"
NARRATION = ROOT / "video-grok" / "narration" / "en"
CHAPTERS = ("g07", "g08", "g09", "g10", "g11")

# Figures the plan requires on these beats. Each token is also checked
# against the inventory, so a typo here fails before any chapter is read.
BEAT_FIGURES = {
    "g07.odes": ("0.11928", "0.9", "0.1", "0.119"),
    "g07.setup": ("0.119", "0.1", "0.80", "1.00", "0", "1"),
    "g07.threshold": ("0.86", "0.865", "0.00194"),
    "g07.inherit": ("0.86", "0.3125", "0.183"),
    "g07.equiv": ("0.0040", "0.0118", "0.00356", "0.00257", "0.00123"),
    "g08.numbers": ("0.2", "4%", "6%", "14%", "65%", "42%", "0.89", "0.905", "0.91"),
    "g09.sizes": ("256", "12000", "1024", "6000", "50"),
    "g10.hard": ("0.408", "0.34", "0.162", "~1e-17", "2.03e-8"),
    "g10.law": ("0.699", "2.52", "0.0304"),
    "g10.sample": ("8.27e-6", "8.64e-4", "0.00257", "0.0231", "9", "4.17e-17"),
    "g11.fails": ("0.287", "0.002"),
    "g11.e3": ("8.87", "17.6", "26.8", "8.9", "17.5", "27", "0.1"),
}

WORD = re.compile(r"[A-Za-z0-9]+(?:[.,'’-][A-Za-z0-9]+)*")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
GREEK_IN_SPEECH = re.compile(r"[μνΓηλσ∞]|\\[A-Za-z]+")


def words(text: str) -> list[str]:
    return WORD.findall(text)


def clock_s(token: str) -> int:
    minutes, seconds = token.split(":")
    return int(minutes) * 60 + int(seconds)


def consume(pattern: re.Pattern[str], text: str, sink: set[str], build) -> str:
    def sub(match: re.Match[str]) -> str:
        sink.add(build(match))
        return " " * len(match.group(0))

    return pattern.sub(sub, text)


def inventory_numbers(text: str) -> set[str]:
    found: set[str] = set()
    prepared = text.translate(SUP).replace("\u2212", "-").replace("×", " * ")
    prepared = consume(
        re.compile(r"~\s*10-(\d+)"),
        prepared,
        found,
        lambda m: f"~1e-{m.group(1)}",
    )
    prepared = consume(
        re.compile(r"(\d+),(\d+)\s*\*\s*(?<!\d)10-(\d+)"),
        prepared,
        found,
        lambda m: f"{m.group(1)}.{m.group(2)}e-{m.group(3)}",
    )
    prepared = consume(
        re.compile(r"(\d+)\s*\*\s*(?<!\d)10-(\d+)"),
        prepared,
        found,
        lambda m: f"{m.group(1)}e-{m.group(2)}",
    )
    prepared = consume(
        re.compile(r"(\d+)\s*%"),
        prepared,
        found,
        lambda m: f"{m.group(1)}%",
    )
    prepared = consume(
        re.compile(r"(?<!\d)(\d{1,3}(?: \d{3})+)(?!\d)"),
        prepared,
        found,
        lambda m: m.group(1).replace(" ", ""),
    )
    prepared = consume(
        re.compile(r"(?<!\d)(\d+),(\d+)(?!\d)"),
        prepared,
        found,
        lambda m: f"{m.group(1)}.{m.group(2)}",
    )
    prepared = consume(
        re.compile(r"(?<![A-Za-z])(\d+)(?![A-Za-z])"),
        prepared,
        found,
        lambda m: m.group(1),
    )
    return found


def narration_numbers(text: str) -> set[str]:
    found: set[str] = set()
    prepared = consume(
        re.compile(r"about 10 to the minus (\d+)", re.IGNORECASE),
        text,
        found,
        lambda m: f"~1e-{m.group(1)}",
    )
    prepared = consume(
        re.compile(r"(\d+(?:\.\d+)?) times 10 to the minus (\d+)", re.IGNORECASE),
        prepared,
        found,
        lambda m: f"{m.group(1)}e-{m.group(2)}",
    )
    prepared = consume(
        re.compile(r"(\d+(?:\.\d+)?)%"),
        prepared,
        found,
        lambda m: f"{m.group(1)}%",
    )
    prepared = consume(
        re.compile(r"(\d+(?:\.\d+)?) percent", re.IGNORECASE),
        prepared,
        found,
        lambda m: f"{m.group(1)}%",
    )
    prepared = consume(
        re.compile(r"(?<!\d)(\d{1,3}(?:,\d{3})+)(?!\d)"),
        prepared,
        found,
        lambda m: m.group(1).replace(",", ""),
    )
    prepared = consume(
        re.compile(r"(?<![A-Za-z])(\d+\.\d+)(?![A-Za-z])"),
        prepared,
        found,
        lambda m: m.group(1),
    )
    prepared = consume(
        re.compile(r"(?<![A-Za-z])(\d+)(?![A-Za-z])"),
        prepared,
        found,
        lambda m: m.group(1),
    )
    return found


def slice_between(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    finish = text.index(end, begin + len(start))
    return text[begin:finish]


def parse_plan(text: str) -> tuple[dict, dict, set[str], str]:
    clock: dict[str, dict] = {}
    clock_region = slice_between(text, "## Horloge du cœur", "## Horloge de l’étendu")
    for line in clock_region.splitlines():
        match = re.match(
            r"^\| (g0[7-9]|g1[01]) \| [^|]+ \| [^|]+ \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+)\u2013([0-9]+:[0-9]+) \| ([0-9]+)\u2013([0-9]+) \|",
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
    beat_region = slice_between(text, "## g07 ", "## g12 ")
    for line in beat_region.splitlines():
        match = re.match(
            r"^\| ((g0[7-9]|g1[01])\.([a-z0-9]+)) \| ([0-9]+:[0-9]+) \| ([^|]+) \|",
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
    cues = set(re.findall(r"cue\.g(?:0[7-9]|1[01])\.[a-z0-9.]+", text))
    extended = slice_between(text, "## Horloge de l’étendu", "## Statuts")
    return clock, beats, cues, extended


def parse_questions(text: str) -> dict[str, dict]:
    found: dict[str, dict] = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"^### (q\.(g0[7-9]|g1[01])) .* ([ABC])\s*$", line)
        if match:
            current = match.group(2)
            found[current] = {"id": match.group(1), "class": match.group(3), "screen": ""}
            continue
        if current and not found[current]["screen"]:
            screen = re.match(r"^- Écran : `([^`]+)`", line)
            if screen:
                found[current]["screen"] = screen.group(1)
    return found


def parse_chapter(path: Path) -> list[dict]:
    beats = []
    current = None
    cue = None
    mode = None
    for raw in path.read_text().splitlines():
        if raw.startswith("## "):
            current = {"id": raw[3:].strip(), "cues": [], "preamble": {}}
            beats.append(current)
            cue = None
            mode = "beat"
            continue
        if raw.startswith("### "):
            if current is None:
                raise SystemExit(f"{path}: cue before a beat: {raw}")
            cue = {"id": raw[4:].strip(), "preamble": {}, "body": []}
            current["cues"].append(cue)
            mode = "cue"
            continue
        if current is None:
            continue
        target = cue if cue else current
        if mode in ("beat", "cue") and raw.strip() == "":
            continue
        if mode in ("beat", "cue") and raw.startswith(("duration:", "badge:", "class:", "role:", "pause:", "screen:")):
            key, value = raw.split(":", 1)
            target["preamble"][key] = value.strip()
            continue
        if cue and raw.strip():
            mode = "body"
            cue["body"].append(raw)
            continue
        if cue and mode == "body":
            cue["body"].append(raw)
    for beat in beats:
        for cue in beat["cues"]:
            cue["text"] = "\n".join(cue["body"]).strip()
    return beats


def spoken_text(beat: dict) -> str:
    parts = []
    for cue in beat["cues"]:
        if cue["preamble"].get("role") == "spoken":
            parts.append(cue["text"])
    return "\n".join(parts)


def cited_text(beat: dict) -> str:
    parts = []
    for cue in beat["cues"]:
        parts.append(cue["text"])
        if "screen" in cue["preamble"]:
            parts.append(cue["preamble"]["screen"])
    return "\n".join(parts)


def beat_map(beats: list[dict]) -> dict[str, dict]:
    return {beat["id"]: beat for beat in beats}


def cue_map(beats: list[dict]) -> dict[str, dict]:
    found = {}
    for beat in beats:
        for cue in beat["cues"]:
            found[cue["id"]] = cue
    return found


def check_clocks(clock: dict, beats: dict, extended_text: str, errors: list[str]) -> None:
    core_end = clock["g08"]["end"]
    row = re.search(r"\| 1\u20139 \| g00 … g08 \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+) \|", extended_text)
    if not row or clock_s(row.group(2)) != core_end:
        errors.append("horloge: g08 ne finit pas à la même seconde dans le cœur et l'étendu")
    pair = re.search(r"\| 11\u201312 \| g09, g10 \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+) \|", extended_text)
    if not pair or clock_s(pair.group(2)) - clock_s(pair.group(1)) != clock["g09"]["duration"] + clock["g10"]["duration"]:
        errors.append("horloge: g09+g10 ne tiennent pas dans le créneau étendu")
    alone = re.search(r"\| 14 \| g11 \| ([0-9]+:[0-9]+) \| ([0-9]+:[0-9]+) \|", extended_text)
    if not alone or clock_s(alone.group(2)) - clock_s(alone.group(1)) != clock["g11"]["duration"]:
        errors.append("horloge: g11 ne tient pas dans le créneau étendu")
    for chapter, rows in beats.items():
        total = sum(row["duration"] for row in rows)
        if total != clock[chapter]["duration"]:
            errors.append(f"plan: {chapter} somme {total}s, horloge {clock[chapter]['duration']}s")


def check_chapter(
    chapter: str,
    parsed: list[dict],
    plan_beats: list[dict],
    clock: dict,
    questions: dict,
    inventory: set[str],
    errors: list[str],
) -> None:
    found = beat_map(parsed)
    expected_ids = [row["id"] for row in plan_beats]
    if [beat["id"] for beat in parsed] != expected_ids:
        errors.append(f"{chapter}: ordre des repères { [beat['id'] for beat in parsed] } != {expected_ids}")
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
        limit = 2 * row["duration"] * 130 / 60
        if count > limit:
            errors.append(f"R3-budget: {row['id']} a {count} mots, plus du double de son créneau")
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
    low, high = clock[chapter]["words"]
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


def check_named_cues(chapters: dict, required: set[str], errors: list[str]) -> None:
    present = {}
    for parsed in chapters.values():
        present.update(cue_map(parsed))
    for cue_id in sorted(required):
        if cue_id not in present:
            errors.append(f"repère nommé absent: {cue_id}")
    predict = {
        "cue.g07.inherit.predict",
        "cue.g08.numbers.predict",
        "cue.g10.sample.predict",
    }
    for cue_id in predict:
        cue = present.get(cue_id)
        if cue is None:
            errors.append(f"pause predict absente: {cue_id}")
            continue
        if cue["preamble"].get("pause") not in ("2s", "3s"):
            errors.append(f"{cue_id}: pause {cue['preamble'].get('pause')!r} hors 2s-3s")
        if cue["preamble"].get("role") != "spoken":
            errors.append(f"{cue_id}: la pause predict doit être dite")


def position(text: str, needle: str) -> int:
    return text.lower().find(needle.lower())


def check_reservations(chapters: dict, errors: list[str]) -> None:
    cues = {}
    spoken = {}
    for chapter, parsed in chapters.items():
        cues.update(cue_map(parsed))
        spoken[chapter] = "\n".join(spoken_text(beat) for beat in parsed)

    def need(cue_id: str, phrase: str, code: str) -> None:
        cue = cues.get(cue_id)
        if cue is None or phrase not in cue["text"]:
            errors.append(f"{code}: {cue_id} ne contient pas {phrase!r}")

    g07 = spoken.get("g07", "")
    odes_order = [cue["id"] for beat in chapters.get("g07", []) for cue in beat["cues"] if beat["id"] == "g07.odes"]
    if "cue.g07.odes.start" not in odes_order or "cue.g07.odes.formula" not in odes_order or odes_order.index("cue.g07.odes.start") > odes_order.index("cue.g07.odes.formula"):
        errors.append("R3-g07: les équations précèdent les noms Q, D, V")
    start = cues.get("cue.g07.odes.start")
    formula = cues.get("cue.g07.odes.formula")
    if not start or not formula or start["preamble"].get("role") != "spoken" or formula["preamble"].get("role") != "unread":
        errors.append("R3-g07: Q, D, V se disent avant une équation non lue")
    elif not all(name in start["text"] for name in ("Q", "D", "V")):
        errors.append("R3-g07: le premier repère ne nomme pas Q, D et V")
    if "three-mode" not in g07 and "three modes" not in g07:
        errors.append("oral: E1 n'est pas dit comme un modèle à trois modes")
    if "prospective" not in g07 or "not endorsed" not in g07:
        errors.append("oral: le rapport prospectif non endossé manque en g07")

    g08 = spoken.get("g08", "")
    if position(g08, "observable") < 0 or g08.find(" F") < 0 or position(g08, "observable") > g08.find(" F"):
        errors.append("R3-g08: F n'a pas de rôle avant le symbole")
    if position(g08, "observable") < 0 or position(g08, "width of that window") < 0:
        errors.append("R3-g08: F ou h n'est pas nommé par son rôle")
    if position(g08, "width of that window") > position(g08, "0.2") or position(g08, "0.2") < 0:
        errors.append("R3-g08: h est chiffré avant son rôle")
    need("cue.g08.rice.caveat", "not guaranteed", "S18")
    need("cue.g08.rice.caveat", "deterministic", "S18")
    need("cue.g08.rice.caveat", "does not cover the percentages", "S18")
    need("cue.g08.numbers.caveat", "numerical check", "S18")
    need("cue.g08.numbers.caveat", "not the theorem", "S18")
    if "zero crossings" not in g08 or "not three-dimensional reversals" not in g08:
        errors.append("oral: les pourcentages de Rice ne sont pas dits comme des passages par zéro")
    close = cues.get("cue.g08.close.show")
    if close and "x03" in close["text"]:
        errors.append("couture: g08.close annonce x03")
    not_beat = cues.get("cue.g08.not.show")
    if not_beat and "x03" not in not_beat["text"]:
        errors.append("plan: g08.not ne dit pas que x03 est facultatif")
    if not_beat and "does not depend" not in not_beat["text"]:
        errors.append("plan: g08.not ne dit pas que le cœur s'en passe")

    g09 = spoken.get("g09", "")
    if position(g09, "integrates the flow") < 0 or position(g09, "integrates the flow") > position(g09, "Heun"):
        errors.append("R3-g09: Heun est nommé avant sa fonction")
    if "flow time" not in g09 or "physical time" not in g09:
        errors.append("R3-g09: le temps du flot n'est pas distingué du temps physique")
    if "digest" in g09.lower():
        errors.append("S17: g09 attribue un chiffre au digest")
    if "toy" not in g09 or "not a measurement" not in g09:
        errors.append("plan: g09.path ne dit pas que le dessin est un jouet")

    sample = spoken_of_beat(chapters.get("g10", []), "g10.sample")
    order = [cue["id"] for beat in chapters.get("g10", []) for cue in beat["cues"] if beat["id"] == "g10.sample"]
    if order != [
        "cue.g10.sample.e2",
        "cue.g10.sample.predict",
        "cue.g10.sample.e1",
        "cue.g10.sample.formula",
    ]:
        errors.append(f"R3-g10: ordre de g10.sample {order}")
    need("cue.g10.law.caveat", "One seed.", "oral-g10")
    need("cue.g10.law.caveat", "interpolation", "oral-g10")
    need("cue.g10.law.caveat", "not a dynamo", "oral-g10")
    need("cue.g10.law.caveat", "two-dimensional", "oral-g10")
    need("cue.g10.law.caveat", "forced", "oral-g10")
    formula = cues.get("cue.g10.sample.formula")
    if not formula or formula["preamble"].get("role") != "unread" or formula["text"] != "Hypothesis: no mass at 0.":
        errors.append("S19: la ligne non lue n'est pas l'hypothèse no mass at 0")
    if formula and ("KL" in formula["text"] or "4.17" in formula["text"] or "8.64" in formula["text"]):
        errors.append("S19: le calque colle une KL ou un quasi-zéro à l'hypothèse")
    if "does not prove" not in sample or "no mass at 0" not in sample:
        errors.append("S19: la voix ne dit pas que la variance mesurée ne prouve pas l'hypothèse")
    if "dissipation" not in cues.get("cue.g10.sample.e2", {"text": ""})["text"]:
        errors.append("STYLE §6: g10.sample.e2 ne dit pas dissipation pour D")
    if "winner" not in spoken.get("g10", ""):
        errors.append("pilote: g10 ne refuse pas le tri par gagnant")
    g10_close = cues.get("cue.g10.close.show")
    if not g10_close or "does not prove" not in g10_close["text"]:
        errors.append("couture: g10.close ne dit pas qu'il énonce sans prouver")
    if "x01" in spoken.get("g10", ""):
        errors.append("couture: g10 annonce x01")

    show = cues.get("cue.g11.e3.show")
    caveat = cues.get("cue.g11.e3.caveat")
    g11_ids = [cue["id"] for beat in chapters.get("g11", []) for cue in beat["cues"]]
    if "cue.g11.e3.show" not in g11_ids or "cue.g11.e3.caveat" not in g11_ids:
        errors.append("S20: show puis caveat manquent")
    elif g11_ids.index("cue.g11.e3.show") > g11_ids.index("cue.g11.e3.caveat"):
        errors.append("S20: le caveat précède le show")
    if (
        not show
        or "1 over eta" not in show["text"]
        or "magnetic diffusivity" not in show["text"]
        or "not a viscosity" not in show["text"]
    ):
        errors.append("S8: Rm = 1/eta n'est pas défini comme diffusivité magnétique")
    if not show or "no generator" not in show["text"]:
        errors.append("oral: E3 ne dit pas l'absence de générateur")
    if not caveat or "not confidence intervals" not in caveat["text"]:
        errors.append("S20: la précision est présentée comme un intervalle, ou la phrase manque")
    if not caveat or "about 0.1" not in caveat["text"] or "one unit" not in caveat["text"]:
        errors.append("S20: environ 0,1 et environ une unité manquent")
    if not caveat or "second half" not in caveat["text"]:
        errors.append("S20: 17,6 n'est pas dit comme l'interpolation de la seconde moitié")
    if "x02" in spoken.get("g11", ""):
        errors.append("R3-g11: g11 renvoie à x02")
    g11_close = cues.get("cue.g11.close.show")
    if not g11_close or "No three-dimensional field has been generated." not in g11_close["text"]:
        errors.append("oral: g11 ne dit pas qu'aucun champ 3D n'a été généré")
    if "confidence interval" in spoken.get("g11", "") and "not confidence intervals" not in spoken.get("g11", ""):
        errors.append("S20: intervalle de confiance affirmé")


def spoken_of_beat(parsed: list[dict], beat_id: str) -> str:
    for beat in parsed:
        if beat["id"] == beat_id:
            return spoken_text(beat)
    return ""


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
    inventory = inventory_numbers(INVENTORY.read_text())
    samples = {
        "0,119": "0.119",
        "0,0040": "0.0040",
        "12 000": "12000",
        "4 %": "4%",
        "4,17×10⁻¹⁷": "4.17e-17",
        "8,27×10⁻⁶": "8.27e-6",
        "8,64×10⁻⁴": "8.64e-4",
        "2,03×10⁻⁸": "2.03e-8",
        "~10⁻¹⁷": "~1e-17",
        "0,80": "0.80",
        "1,00": "1.00",
    }
    parsed = inventory_numbers("\n".join(samples))
    for token in samples.values():
        if token not in parsed:
            errors.append(f"self-test inventaire: {token} non relu")
    english = narration_numbers(
        "mu 0.119, width 256, 12,000 iterations, 4 percent, "
        "4.17 times 10 to the minus 17, about 10 to the minus 17, seeds 0 and 1, E1, 3D"
    )
    expected = {"0.119", "256", "12000", "4%", "4.17e-17", "~1e-17", "0", "1"}
    if english != expected:
        errors.append(f"self-test narration: {sorted(english)} != {sorted(expected)}")
    if "0.999" in inventory:
        errors.append("self-test: 0.999 est dans l'inventaire, le contrôle ne sert à rien")
    fake = narration_numbers("The gap is 0.999.")
    if fake & inventory:
        errors.append("self-test: 0.999 a été accepté")
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
        print("self-test: extracteurs et ancres conformes à l'inventaire")
        if "--chapter" not in argv:
            return 0
    else:
        errors = self_test()
        if errors:
            print("\n".join(errors))
            return 1
    inventory = inventory_numbers(INVENTORY.read_text())
    plan = PLAN.read_text()
    clock, plan_beats, cues, extended = parse_plan(plan)
    questions = parse_questions(QUESTIONS.read_text())
    errors: list[str] = []
    check_clocks(clock, plan_beats, extended, errors)
    if set(questions) != set(CHAPTERS):
        errors.append(f"registre: cartes {sorted(questions)} incomplètes")
    chapters = load_chapters(only)
    for chapter, parsed in chapters.items():
        check_chapter(chapter, parsed, plan_beats[chapter], clock, questions, inventory, errors)
    if only is None:
        check_named_cues(chapters, cues, errors)
        check_reservations(chapters, errors)
    if errors:
        print("\n".join(errors))
        return 1
    scope = only or "g07-g11"
    print(f"{scope}: chiffres, repères, cartes, horloges 41:00 et 60:00 tenus")
    print("tokenizer: un mot est un jeton [A-Za-z0-9] avec point, virgule interne, ou trait d'union")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
