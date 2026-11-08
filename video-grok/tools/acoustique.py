import hashlib
import json
import os
import re
import sys

import numpy as np
import torch

MODELES = {
    "en": "facebook/wav2vec2-base-960h",
    "fr": "jonatasgrosman/wav2vec2-large-xlsr-53-french",
}

EN_UN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
EN_DIX = [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
EN_DIZ = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
FR_UN = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
FR_DIX = [
    "dix",
    "onze",
    "douze",
    "treize",
    "quatorze",
    "quinze",
    "seize",
    "dix-sept",
    "dix-huit",
    "dix-neuf",
]
FR_DIZ = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante", "quatre-vingt", "quatre-vingt"]


def entier_en(nombre):
    if nombre < 10:
        return [EN_UN[nombre]]
    if nombre < 20:
        return [EN_DIX[nombre - 10]]
    if nombre < 100:
        dizaine, unite = divmod(nombre, 10)
        if unite == 0:
            return [EN_DIZ[dizaine]]
        return [EN_DIZ[dizaine], EN_UN[unite]]
    return [EN_UN[int(chiffre)] for chiffre in str(nombre)]


def entier_fr(nombre):
    if nombre < 10:
        return [FR_UN[nombre]]
    if nombre < 20:
        return [FR_DIX[nombre - 10].split("-")]
    if nombre < 70:
        dizaine, unite = divmod(nombre, 10)
        if unite == 0:
            return [FR_DIZ[dizaine]]
        if unite == 1 and dizaine not in (8,):
            return [FR_DIZ[dizaine], "et", "un"]
        return [FR_DIZ[dizaine], FR_UN[unite]]
    if nombre < 80:
        reste = nombre - 60
        return ["soixante"] + [mot for morceau in entier_fr(reste) for mot in (morceau if isinstance(morceau, list) else [morceau])]
    if nombre < 100:
        reste = nombre - 80
        tete = ["quatre", "vingts"] if reste == 0 else ["quatre", "vingt"]
        if reste == 0:
            return tete
        return tete + [mot for morceau in entier_fr(reste) for mot in (morceau if isinstance(morceau, list) else [morceau])]
    if nombre < 1000:
        centaines, reste = divmod(nombre, 100)
        tete = ["cent"] if centaines == 1 else [FR_UN[centaines], "cent"]
        if reste == 0:
            return tete
        return tete + [mot for morceau in entier_fr(reste) for mot in (morceau if isinstance(morceau, list) else [morceau])]
    return [FR_UN[int(chiffre)] for chiffre in str(nombre)]


def aplatir(morceaux):
    plats = []
    for morceau in morceaux:
        if isinstance(morceau, list):
            plats.extend(morceau)
        else:
            plats.append(morceau)
    return plats


def developper(jeton, langue, decimal="chiffres"):
    nu = jeton.strip(".,;:!?…")
    if not nu:
        return [jeton]
    if langue == "fr":
        nu = nu.replace(".", ",")
    else:
        nu = nu.replace(",", ".")
    morceaux = re.findall(r"[A-Za-zÀ-ÿ]+|\d+[.,]\d+|\d+", nu)
    if not morceaux:
        return [nu]
    mots = []
    for morceau in morceaux:
        if re.fullmatch(r"[A-Za-zÀ-ÿ]+", morceau):
            mots.append(morceau)
            continue
        if re.fullmatch(r"\d+[.,]\d+", morceau):
            gauche, droite = re.split(r"[.,]", morceau)
            if langue == "fr":
                mots.extend(aplatir(entier_fr(int(gauche or "0"))))
                mots.append("virgule")
                if decimal == "chiffres" or droite.startswith("0"):
                    mots.extend(FR_UN[int(chiffre)] for chiffre in droite)
                else:
                    mots.extend(aplatir(entier_fr(int(droite))))
            else:
                mots.extend(entier_en(int(gauche or "0")))
                mots.append("point")
                mots.extend(EN_UN[int(chiffre)] for chiffre in droite)
            continue
        nombre = int(morceau)
        if langue == "fr":
            mots.extend(aplatir(entier_fr(nombre)))
        elif nombre < 100:
            mots.extend(entier_en(nombre))
        else:
            mots.extend(EN_UN[int(chiffre)] for chiffre in morceau)
    return mots or [nu]


def variantes(texte, langue):
    jetons = texte.replace("\n", " ").split()
    if langue == "fr":
        modes = ("chiffres", "entier")
    else:
        modes = ("chiffres",)
    phrases = []
    for mode in modes:
        mots = []
        origine = []
        for index, jeton in enumerate(jetons):
            for mot in developper(jeton, langue, mode):
                mots.append(mot)
                origine.append(index)
        phrases.append((mots, origine, jetons))
    return phrases


def decouper(texte):
    trouvees = []
    courant = ""
    for index, caractere in enumerate(texte):
        courant += caractere
        decimal = (
            caractere == "."
            and index > 0
            and texte[index - 1].isdigit()
            and index + 1 < len(texte)
            and texte[index + 1].isdigit()
        )
        if caractere in ".?!" and not decimal:
            if courant.strip():
                trouvees.append(courant.strip())
            courant = ""
    if courant.strip():
        trouvees.append(courant.strip())
    return trouvees


def viterbi(emissions, identifiants, blanc):
    longueur = emissions.shape[0]
    lettres = len(identifiants)
    jetons = torch.tensor(identifiants, dtype=torch.long)
    precedent = emissions.new_full((lettres + 1,), -1e30)
    precedent[0] = 0
    retour = torch.zeros((longueur, lettres + 1), dtype=torch.int8)
    blancs = emissions[:, blanc]
    paroles = emissions[:, jetons]
    for instant in range(longueur):
        courant = emissions.new_full((lettres + 1,), -1e30)
        courant[0] = precedent[0] + blancs[instant]
        choix = torch.stack(
            (
                precedent[1:] + blancs[instant],
                precedent[:-1] + paroles[instant],
                precedent[1:] + paroles[instant],
            ),
        )
        courant[1:] = choix.max(dim=0).values
        retour[instant, 1:] = choix.argmax(dim=0).to(torch.int8)
        precedent = courant
    if float(precedent[lettres]) < -1e20:
        return None, None, -1e30
    premiere = [None] * lettres
    derniere = [None] * lettres
    index = lettres
    for instant in range(longueur - 1, -1, -1):
        if index == 0:
            break
        code = int(retour[instant, index])
        if code == 0:
            continue
        if derniere[index - 1] is None:
            derniere[index - 1] = instant
        premiere[index - 1] = instant
        if code == 1:
            index -= 1
    if index != 0 or any(valeur is None for valeur in premiere):
        return None, None, -1e30
    return premiere, derniere, float(precedent[lettres])


class Aligneur:
    def __init__(self):
        self.charges = {}

    def modele(self, langue):
        garde = self.charges.get(langue)
        if garde:
            return garde
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

        nom = MODELES[langue]
        processeur = Wav2Vec2Processor.from_pretrained(nom)
        modele = Wav2Vec2ForCTC.from_pretrained(nom)
        modele.eval()
        self.charges[langue] = (processeur, modele)
        return processeur, modele

    def charger_audio(self, chemin):
        import subprocess

        brut = subprocess.check_output(
            ["ffmpeg", "-v", "error", "-i", chemin, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        )
        return np.frombuffer(brut, dtype=np.float32).copy()

    def chuchoteur(self, langue):
        gardes = getattr(self, "whispers", None)
        if gardes is None:
            self.whispers = {}
            gardes = self.whispers
        if langue not in gardes:
            from faster_whisper import WhisperModel

            gardes[langue] = WhisperModel("base", device="cpu", compute_type="int8")
        return gardes[langue]

    def aligner(self, chemin, texte, langue):
        empreinte = hashlib.sha256()
        with open(chemin, "rb") as fichier:
            empreinte.update(fichier.read())
        empreinte.update(texte.encode())
        empreinte.update(langue.encode())
        empreinte.update(b"v4")
        dossier = os.environ.get("ACOUSTIQUE_CACHE", "/tmp/acoustique-cache")
        os.makedirs(dossier, exist_ok=True)
        cache = os.path.join(dossier, f"{empreinte.hexdigest()}.json")
        if os.path.exists(cache):
            with open(cache, encoding="utf8") as fichier:
                return json.load(fichier)
        audio = self.charger_audio(chemin)
        if audio.size == 0:
            return []
        phrases = decouper(texte)
        processeur, modele = self.modele(langue)
        regroupes = self.suite(audio, " ".join(phrases), langue, processeur, modele, 0)
        segments = self.segments(audio, langue)
        if len(segments) == len(phrases):
            debuts = []
            curseur = 0
            for phrase in phrases:
                debuts.append(regroupes[curseur]["debut"] if curseur < len(regroupes) else 0)
                curseur += len(phrase.split())
            if any(abs(debut - segment["debut"]) > 0.35 for debut, segment in zip(debuts, segments)):
                regroupes = []
                for phrase, segment in zip(phrases, segments):
                    gauche = max(0, int((segment["debut"] - 0.15) * 16000))
                    droite = min(len(audio), int((segment["fin"] + 0.2) * 16000))
                    regroupes.extend(self.suite(audio[gauche:droite], phrase, langue, processeur, modele, gauche))
        with open(cache, "w", encoding="utf8") as fichier:
            json.dump(regroupes, fichier)
        return regroupes

    def segments(self, audio, langue):
        segments, _info = self.chuchoteur(langue).transcribe(
            audio,
            language=langue,
            word_timestamps=False,
            vad_filter=False,
            beam_size=1,
            temperature=0,
        )
        return [{"debut": segment.start, "fin": segment.end, "texte": segment.text} for segment in segments]

    def suite(self, audio, texte, langue, processeur, modele, decalage_echantillons):
        if audio.size == 0:
            return [{"mot": jeton, "debut": 0.0, "fin": 0.0} for jeton in texte.split()]
        with torch.inference_mode():
            entrees = processeur(audio, sampling_rate=16000, return_tensors="pt")
            emissions = torch.log_softmax(modele(entrees.input_values).logits, dim=-1)[0]
        meilleur = None
        for mots, origine, jetons in variantes(texte, langue):
            places, score = self.caler(emissions, mots, processeur, audio.size)
            if places is None:
                continue
            if meilleur is None or score > meilleur[0]:
                meilleur = (score, places, origine, jetons)
        if meilleur is None:
            return [{"mot": jeton, "debut": decalage_echantillons / 16000, "fin": decalage_echantillons / 16000} for jeton in texte.split()]
        _, places, origine, jetons = meilleur
        decalage = decalage_echantillons / 16000
        regroupes = []
        for index, jeton in enumerate(jetons):
            lies = [places[i] for i, source in enumerate(origine) if source == index and i < len(places)]
            if not lies:
                regroupes.append({"mot": jeton, "debut": decalage, "fin": decalage})
                continue
            regroupes.append({
                "mot": jeton,
                "debut": decalage + min(lieu[0] for lieu in lies),
                "fin": decalage + max(lieu[1] for lieu in lies),
            })
        return regroupes

    def caler(self, emissions, mots, processeur, nb_echantillons):
        vocabulaire = processeur.tokenizer.get_vocab()
        blanc = processeur.tokenizer.pad_token_id
        identifiants = []
        plages = []
        for mot in mots:
            debut = len(identifiants)
            for caractere in mot:
                cle = None
                for candidat in (caractere, caractere.lower(), caractere.upper()):
                    if candidat in vocabulaire:
                        cle = vocabulaire[candidat]
                        break
                if cle is not None:
                    identifiants.append(cle)
            if len(identifiants) == debut:
                continue
            plages.append((debut, len(identifiants)))
        if not identifiants:
            return None, -1e30
        premiere, derniere, accord = viterbi(emissions, identifiants, blanc)
        if premiere is None:
            return None, -1e30
        pas = (nb_echantillons / 16000) / emissions.shape[0]
        places = []
        for debut, fin in plages:
            gauche = premiere[debut]
            droite = derniere[fin - 1]
            if gauche is None or droite is None:
                return None, -1e30
            places.append((gauche * pas, (droite + 1) * pas))
        return places, accord


def main():
    tache = json.loads(sys.stdin.read())
    aligneur = Aligneur()
    sortie = {}
    for item in tache["taches"]:
        sortie[item["id"]] = aligneur.aligner(item["audio"], item["texte"], item["langue"])
    json.dump(sortie, sys.stdout)


if __name__ == "__main__":
    main()
