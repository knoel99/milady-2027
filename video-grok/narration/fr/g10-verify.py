#!/usr/bin/env python3
"""Vérifie la narration française de g10 contre le fichier anglais gelé.

Mêmes repères, dans le même ordre, avec les mêmes rôles et les mêmes
marqueurs de temps. Le débit compte les mots tels qu'on les dit, chiffres
épelés, et refuse un beat au-dessus de 156 mots par minute. Ce plafond est
celui du vérificateur anglais. La forme « à la puissance » ajoute un mot par
nombre en puissances de dix. Un plafond plus haut masquerait un beat qui ne
tient pas dans son créneau.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EN_PATH = HERE.parent / "en" / "g07-g11-verify.py"
FR_CHAPTER = HERE / "g10.md"
EN_CHAPTER = HERE.parent / "en" / "g10.md"
CAVEAT_FILE = HERE / "g10.law.caveat.md"
QUESTIONS = ROOT / "video-grok" / "QUESTIONS.md"

SPEECH_WPM = 156
PLAN_WPM = 130

_ONES = (
    "zéro un deux trois quatre cinq six sept huit neuf dix onze douze "
    "treize quatorze quinze seize"
).split()
_TENS = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante"]
LETTER = "0-9A-Za-zÀ-ÖØ-öø-ÿŒœ"
WORD = re.compile(rf"[{LETTER}]+(?:['’-][{LETTER}]+)*")
GREEK_IN_SPEECH = re.compile(r"[μνΓηλσ∞]|\\[A-Za-z]+")


def _load_english():
    spec = importlib.util.spec_from_file_location("g07_g11_verify", EN_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"vérificateur anglais illisible: {EN_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def words(text: str) -> list[str]:
    return WORD.findall(text)


def _under_hundred(value: int) -> str:
    if value < 17:
        return _ONES[value]
    if value < 20:
        return "dix-" + _ONES[value - 10]
    if value < 70:
        ten, one = divmod(value, 10)
        if one == 0:
            return _TENS[ten]
        if one == 1:
            return f"{_TENS[ten]} et un"
        return f"{_TENS[ten]}-{_ONES[one]}"
    if value < 80:
        rest = value - 60
        if rest == 11:
            return "soixante et onze"
        return "soixante-" + _under_hundred(rest)
    if value == 80:
        return "quatre-vingts"
    rest = value - 80
    return "quatre-vingt-" + _under_hundred(rest)


def _int_words(value: int) -> str:
    if value < 100:
        return _under_hundred(value)
    if value < 1000:
        hundreds, rest = divmod(value, 100)
        head = "cent" if hundreds == 1 else f"{_ONES[hundreds]} cent"
        if hundreds > 1 and rest == 0:
            head += "s"
        return head if rest == 0 else f"{head} {_under_hundred(rest)}"
    raise ValueError(f"entier hors narration: {value}")


def _decimal_words(token: str) -> str:
    whole, frac = token.split(",")
    digits = " ".join(_ONES[int(char)] for char in frac)
    return f"{_int_words(int(whole))} virgule {digits}"


def expand_spoken(text: str) -> str:
    """Épelle les chiffres comme la voix française doit les dire."""

    def scientific(match: re.Match[str]) -> str:
        token = match.group(1)
        if "," not in token:
            token = token + ",0"
        return (
            f"{_decimal_words(token)} fois dix à la puissance moins "
            f"{_int_words(int(match.group(2)))}"
        )

    def about(match: re.Match[str]) -> str:
        return f"environ dix à la puissance moins {_int_words(int(match.group(1)))}"

    text = re.sub(r"(\d+,\d+) fois 10 à la puissance moins (\d+)", scientific, text)
    text = re.sub(r"(?<!\d)(\d+) fois 10 à la puissance moins (\d+)", scientific, text)
    text = re.sub(r"environ 10 à la puissance moins (\d+)", about, text)
    text = re.sub(
        rf"(?<![{LETTER}])(\d+,\d+)(?!\d)",
        lambda m: _decimal_words(m.group(1)),
        text,
    )
    text = re.sub(
        rf"(?<![{LETTER}])(\d+)(?![{LETTER}])",
        lambda m: _int_words(int(m.group(1))),
        text,
    )
    return text


def speech_rate(said: str, duration: int, pause: int) -> float:
    speaking = duration - pause
    if speaking <= 0:
        return float("inf")
    return len(words(expand_spoken(said))) / speaking * 60


def spoken_count(said: str) -> int:
    return len(words(expand_spoken(said)))


def consume(pattern: re.Pattern[str], text: str, sink: set[str], build) -> str:
    def sub(match: re.Match[str]) -> str:
        sink.add(build(match))
        return " " * len(match.group(0))

    return pattern.sub(sub, text)


def narration_numbers(text: str) -> set[str]:
    found: set[str] = set()
    prepared = consume(
        re.compile(r"environ 10 à la puissance moins (\d+)"),
        text,
        found,
        lambda m: f"~1e-{m.group(1)}",
    )
    prepared = consume(
        re.compile(r"(\d+),(\d+) fois 10 à la puissance moins (\d+)"),
        prepared,
        found,
        lambda m: f"{m.group(1)}.{m.group(2)}e-{m.group(3)}",
    )
    prepared = consume(
        re.compile(r"(?<!\d)(\d+) fois 10 à la puissance moins (\d+)"),
        prepared,
        found,
        lambda m: f"{m.group(1)}e-{m.group(2)}",
    )
    prepared = consume(
        re.compile(rf"(?<![{LETTER}])(\d+),(\d+)(?!\d)"),
        prepared,
        found,
        lambda m: f"{m.group(1)}.{m.group(2)}",
    )
    prepared = consume(
        re.compile(rf"(?<![{LETTER}])(\d+)(?![{LETTER}])"),
        prepared,
        found,
        lambda m: m.group(1),
    )
    return found


def pause_seconds(beat: dict) -> int:
    total = 0
    for cue in beat["cues"]:
        pause = cue["preamble"].get("pause")
        if pause:
            total += int(str(pause).rstrip("s"))
    return total


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


def clock_s(token: str) -> int:
    minutes, seconds = token.split(":")
    return int(minutes) * 60 + int(seconds)


def marker(preamble: dict, keys: tuple[str, ...]) -> dict:
    return {key: preamble.get(key) for key in keys}


def rate_payload(text: str, duration: int, pause: int = 0) -> dict:
    count = spoken_count(text)
    rate = speech_rate(text, duration, pause)
    return {"count": count, "rate": round(rate, 1), "pause": pause, "duration": duration}


def check_parity(english: list[dict], french: list[dict], errors: list[str]) -> None:
    en_ids = [beat["id"] for beat in english]
    fr_ids = [beat["id"] for beat in french]
    if en_ids != fr_ids:
        errors.append(f"ordre des beats {fr_ids} != {en_ids}")
        return
    for en_beat, fr_beat in zip(english, french):
        beat_id = en_beat["id"]
        if marker(en_beat["preamble"], ("duration", "badge", "class")) != marker(
            fr_beat["preamble"], ("duration", "badge", "class")
        ):
            errors.append(f"{beat_id}: durée, pastille ou classe différente")
        en_cues = [cue["id"] for cue in en_beat["cues"]]
        fr_cues = [cue["id"] for cue in fr_beat["cues"]]
        if en_cues != fr_cues:
            errors.append(f"{beat_id}: ordre des repères {fr_cues} != {en_cues}")
            continue
        for en_cue, fr_cue in zip(en_beat["cues"], fr_beat["cues"]):
            if marker(en_cue["preamble"], ("role", "pause", "screen")) != marker(
                fr_cue["preamble"], ("role", "pause", "screen")
            ):
                errors.append(f"{en_cue['id']}: rôle, pause ou écran différent")
            if en_cue["preamble"].get("role") == "unread" and en_cue["text"] != fr_cue["text"]:
                errors.append(f"{en_cue['id']}: la ligne non lue n'est plus celle de l'anglais")


def check_rates(french: list[dict], errors: list[str]) -> list[str]:
    lines = []
    for beat in french:
        said = spoken_text(beat)
        duration = clock_s(beat["preamble"].get("duration", "0:00"))
        pause = pause_seconds(beat)
        payload = rate_payload(said, duration, pause)
        lines.append(
            f"{beat['id']}: {payload['count']} mots dits, {payload['rate']} mots/min, "
            f"pause {pause}s, créneau {duration}s"
        )
        if payload["rate"] > SPEECH_WPM:
            errors.append(
                f"débit: {beat['id']} a {payload['count']} mots dits en {duration - pause}s "
                f"après {pause}s de pause, soit {payload['rate']} mots/min, plafond {SPEECH_WPM}"
            )
        compact = len(words(said))
        limit = 2 * duration * PLAN_WPM / 60
        if compact > limit:
            errors.append(f"R3-budget: {beat['id']} a {compact} mots, plus du double de son créneau")
    return lines


def check_figures(english, french, inventory: set[str], en, errors: list[str]) -> None:
    for en_beat, fr_beat in zip(english, french):
        expected = en.narration_numbers(en.cited_text(en_beat))
        found = narration_numbers(cited_text(fr_beat))
        if found != expected:
            errors.append(
                f"{en_beat['id']}: chiffres {sorted(found)} != anglais {sorted(expected)}"
            )
        unknown = sorted(token for token in found if token not in inventory)
        if unknown:
            errors.append(f"{en_beat['id']}: chiffre absent de l'inventaire: {', '.join(unknown)}")


def check_science(french: list[dict], caveat: str, errors: list[str]) -> None:
    cues = {cue["id"]: cue for beat in french for cue in beat["cues"]}

    def text(cue_id: str) -> str:
        cue = cues.get(cue_id)
        return cue["text"] if cue else ""

    e2 = text("cue.g10.sample.e2")
    e1 = text("cue.g10.sample.e1")
    close = text("cue.g10.close.show")
    if "écart-type de dissipation" not in e2 or "écart-type de référence" not in e2:
        errors.append("science: 8,64e-4 n'est pas le rapport des écarts-types de dissipation")
    if "bilan" in e2:
        errors.append("science: g10.sample.e2 mélange le bilan d'énergie et la dissipation")
    if "D est la dissipation" not in e2 or "dipôle" not in e2:
        errors.append("science: D n'est pas dit comme la dissipation, pas le dipôle")
    if "bilan d’énergie" not in e1 and "bilan d'énergie" not in e1:
        errors.append("science: g10.sample.e1 ne nomme pas l'écart-type du bilan d'énergie")
    if "ne prouve pas" not in e1 or "masse en 0" not in e1:
        errors.append("science: la variance positive ne reste pas distinguée de l'absence de masse")
    if "probabilité nulle" not in close or "exactement sur zéro" not in close:
        errors.append("science: la masse en zéro n'est pas une probabilité nulle d'arriver exactement sur zéro")
    if "valeur de la contrainte" not in close:
        errors.append("science: la probabilité nulle ne porte pas sur la valeur de la contrainte")
    if "L’ancrage limite" not in close and "L'ancrage limite" not in close:
        errors.append("science: l'ancrage ne limite plus le déplacement du réglage fin")
    if "modèle de départ" not in close or "réglage fin" not in close:
        errors.append("science: l'ancrage ne dit plus depuis quel modèle le réglage fin part")
    if "ne les prouve pas" not in close:
        errors.append("couture: g10.close ne dit pas qu'il énonce sans prouver")
    law = text("cue.g10.law.caveat")
    if law != caveat:
        errors.append("caveat: cue.g10.law.caveat diffère de narration/fr/g10.law.caveat.md")
    formula = cues.get("cue.g10.sample.formula")
    if not formula or formula["text"] != "Hypothesis: no mass at 0.":
        errors.append("S19: la ligne non lue n'est pas l'hypothèse anglaise no mass at 0")
    spoken = "\n".join(spoken_text(beat) for beat in french)
    if GREEK_IN_SPEECH.search(spoken) or "(" in spoken or ")" in spoken or ":" in spoken or "\u2014" in spoken:
        errors.append("oral: le parlé contient un symbole, des parenthèses, deux-points, ou un tiret long")
    if "KL" in spoken or "±" in spoken:
        errors.append("oral: KL ou ± dans le parlé")
    if "gagnant" not in spoken:
        errors.append("pilote: g10 ne refuse pas le tri par gagnant")


def question_flag(spoken_card: str) -> str | None:
    text = QUESTIONS.read_text()
    start = text.find("### q.g10")
    if start < 0:
        return "FLAG q.g10: section absente de QUESTIONS.md"
    end = text.find("\n### ", start + 1)
    section = text[start:] if end < 0 else text[start:end]
    voice = re.search(r"^- (?:Voix|Français) : `([^`]+)`", section, re.M)
    if voice is None:
        return (
            "FLAG q.g10: QUESTIONS.md n'a pas de phrase française. "
            f"La voix propose « {spoken_card} ». L'écran reste la phrase anglaise."
        )
    if spoken_card != voice.group(1):
        return f"q.g10: la voix {spoken_card!r} != {voice.group(1)!r}"
    return None


def caveat_sentence() -> str:
    lines = CAVEAT_FILE.read_text().splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == "### cue.g10.law.caveat"), -1)
    if start < 0:
        raise SystemExit("caveat: cue.g10.law.caveat absent du fichier d'extrait")
    body = []
    for line in lines[start + 1 :]:
        if line.startswith("## ") or line.startswith("### "):
            break
        stripped = line.strip()
        if stripped == "" or stripped.startswith("role:"):
            continue
        body.append(stripped)
    return " ".join(body)


def self_test() -> list[str]:
    errors = []
    spelled = expand_spoken(
        "divergence 0,408, et 8,27 fois 10 à la puissance moins 6, "
        "environ 10 à la puissance moins 17, facteur 9"
    )
    if "zéro virgule quatre zéro huit" not in spelled:
        errors.append(f"self-test épelage décimal: {spelled}")
    if "huit virgule deux sept fois dix à la puissance moins six" not in spelled:
        errors.append(f"self-test épelage puissance: {spelled}")
    if "dix-sept" not in spelled or "environ dix à la puissance moins dix-sept" not in spelled:
        errors.append(f"self-test épelage environ: {spelled}")
    if "neuf" not in spelled:
        errors.append(f"self-test épelage entier: {spelled}")
    figures = narration_numbers(
        "0,408 et 8,27 fois 10 à la puissance moins 6, environ 10 à la puissance moins 17, "
        "facteur 9, E2, V0"
    )
    expected = {"0.408", "8.27e-6", "~1e-17", "9"}
    if figures != expected:
        errors.append(f"self-test chiffres: {sorted(figures)} != {sorted(expected)}")
    if speech_rate(" ".join(["mot"] * 100), 30, 0) <= SPEECH_WPM:
        errors.append("self-test débit: 100 mots en 30 s passe le plafond")
    if speech_rate("un deux trois", 30, 0) > SPEECH_WPM:
        errors.append("self-test débit: trois mots en 30 s dépassent le plafond")
    if _int_words(17) != "dix-sept" or _int_words(71) != "soixante et onze" or _int_words(80) != "quatre-vingts":
        errors.append("self-test entiers français")
    return errors


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        errors = self_test()
        if errors:
            print("\n".join(errors))
            return 1
        print("self-test: épelage français et plafond 156 tenus")
        return 0
    if "--rate" in argv:
        payload = json.loads(sys.stdin.read())
        print(json.dumps(rate_payload(payload["text"], int(payload["duration"]), int(payload.get("pause", 0)))))
        return 0
    errors = self_test()
    if errors:
        print("\n".join(errors))
        return 1
    en = _load_english()
    english = en.parse_chapter(EN_CHAPTER)
    french = en.parse_chapter(FR_CHAPTER)
    inventory = en.inventory_numbers((ROOT / "video-grok" / "INVENTAIRE.md").read_text())
    errors = []
    check_parity(english, french, errors)
    rates = check_rates(french, errors)
    check_figures(english, french, inventory, en, errors)
    caveat = caveat_sentence()
    check_science(french, caveat, errors)
    card = ""
    for beat in french:
        for cue in beat["cues"]:
            if cue["id"] == "cue.g10.card":
                card = cue["text"]
    flag = question_flag(card)
    if flag and not flag.startswith("FLAG "):
        errors.append(flag)
    if errors:
        print("\n".join(errors))
        return 1
    print("\n".join(rates))
    if flag:
        print(flag)
    print("g10 français: repères, chiffres, et débit ≤ 156 mots/min tenus")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
