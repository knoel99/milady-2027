import hashlib
import json
import os
import subprocess
import sys

import numpy as np


def charger(chemin):
    brut = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", chemin, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
    )
    return np.frombuffer(brut, dtype=np.float32).copy()


def regions(audio, seuil_db=-40, trou=0.12):
    if audio.size == 0:
        return []
    pas = 160
    seuil = 10 ** (seuil_db / 20)
    actif = []
    for depart in range(0, audio.size - pas, pas):
        fenetre = audio[depart : depart + pas]
        actif.append(float(np.sqrt(np.mean(fenetre * fenetre))) >= seuil)
    trouvees = []
    debut = None
    for index, voix in enumerate([*actif, False]):
        if voix and debut is None:
            debut = index
        if not voix and debut is not None:
            trouvees.append((debut * 0.01, index * 0.01))
            debut = None
    if not trouvees:
        return []
    fusion = [trouvees[0]]
    for gauche, droite in trouvees[1:]:
        if gauche - fusion[-1][1] < trou:
            fusion[-1] = (fusion[-1][0], droite)
        else:
            fusion.append((gauche, droite))
    return [{"debut": gauche, "fin": droite} for gauche, droite in fusion if droite - gauche >= 0.04]


MODELES = {}


def modele(langue):
    if langue not in MODELES:
        from faster_whisper import WhisperModel

        nom = os.environ.get("WHISPER_MODELE", "small")
        MODELES[langue] = WhisperModel(nom, device="cpu", compute_type="int8")
    return MODELES[langue]


def segments(audio, langue):
    resultat, _info = modele(langue).transcribe(
        audio,
        language=langue,
        word_timestamps=False,
        vad_filter=False,
        beam_size=1,
        temperature=0,
        condition_on_previous_text=False,
    )
    return [
        {"debut": float(segment.start), "fin": float(segment.end), "texte": segment.text.strip()}
        for segment in resultat
        if segment.text.strip()
    ]


def ecouter(chemin, langue):
    empreinte = hashlib.sha256()
    with open(chemin, "rb") as fichier:
        empreinte.update(fichier.read())
    empreinte.update(langue.encode())
    empreinte.update(os.environ.get("WHISPER_MODELE", "small").encode())
    empreinte.update(b"oreille-v1")
    dossier = os.environ.get("OREILLE_CACHE", "/tmp/oreille-cache")
    os.makedirs(dossier, exist_ok=True)
    cache = os.path.join(dossier, f"{empreinte.hexdigest()}.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf8") as fichier:
            return json.load(fichier)
    audio = charger(chemin)
    sortie = {"segments": segments(audio, langue), "regions": regions(audio)}
    with open(cache, "w", encoding="utf8") as fichier:
        json.dump(sortie, fichier)
    return sortie


def main():
    demande = json.loads(sys.stdin.read())
    sortie = {}
    for tache in demande["taches"]:
        sortie[tache["id"]] = ecouter(tache["audio"], tache["langue"])
    json.dump(sortie, sys.stdout)


if __name__ == "__main__":
    main()
