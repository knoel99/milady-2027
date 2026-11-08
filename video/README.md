# Film « How Often Does the Field Flip? » : dossier de production

Ce dossier fabrique le film explicatif du projet MilaDy 2027, en deux coupes tirées des mêmes scènes :
la **coupe longue** (`extended`, ≈ 60 min, version de référence) et la **coupe courte** (`core`, ≈ 41 min).
Tout est produit sur cette machine, de façon reproductible : chaque scène est une page HTML déterministe,
filmée image par image ; la narration (voix Fish Audio « Ethan ») est synthétisée paragraphe par
paragraphe ; la musique et les bruitages sont synthétisés par le code. `BRIEF.md` fait foi pour toutes
les décisions ; `CONTRACT.md` décrit le contrat technique entre le pipeline et les scènes.

## Organisation

| Dossier | Contenu |
|---|---|
| `script/<unité>.json` | texte de la narration et description des scènes (schéma 2), une unité par chapitre ou module |
| `script/fr/<unité>.json` | narration française de l'unité (surcouche : mêmes identifiants de phrases, mêmes repères ; voir « Version française ») |
| `script/_build/` | coupes assemblées (`film_core.json`, `film_extended.json`), temps de chaque phrase (`<coupe>_cues.json`), liste des questions (`questions_<coupe>.json`) |
| `scenes/<unité>/` | une page HTML par scène ; `runtime/` : moteur déterministe et composants partagés |
| `data/` | données des scènes, extraites des résultats existants du dépôt (`make data`) |
| `audio/` | synthèse vocale (`tts.py`), minutage des phrases (`align.py`), mixage (`mix.py`), prononciations (`lexicon.json`, `lexicon_fr.json`), cache des voix déjà payées (`cache/`, à conserver), pistes de narration par scène (`scenes/`, `scenes_fr/`) |
| `subs/` | sous-titres `.srt`, `.vtt`, `.ass` de chaque coupe, tirés du texte du script |
| `out/` | rendus : `film_<coupe>.mp4`, pistes séparées `stems/`, brouillons `draft/`, vérifications `check/` |

## Commandes

```bash
make plan CUT=extended        # ce qui serait synthétisé (mots, paragraphes) et re-rendu, sans rien calculer
make film CUT=extended        # construction complète : voix (cache), scènes modifiées, mixage, MP4
make films                    # les deux coupes
make draft CUT=core           # brouillon 960x540 à 15 i/s pour relecture (n'appelle pas l'API)
make scene S=04.3             # refaire une scène puis réassembler
make check U=ch04             # images autour de chaque repère des scènes d'une unité + erreurs de page + contrôle de mise en page
                              # (n'écrit jamais dans audio/ : minutage de la narration lu tel quel s'il correspond au script,
                              #  sinon estimé à 146 mots/min ; TIMING=estimate force l'estimation ; sorties dans out/check/unit_ch04/)
make draft U=ch04             # brouillon vidéo d'une seule unité, narration ajoutée quand elle existe (out/draft/unit_ch04/)
make det U=ch04               # déterminisme des scènes d'une unité (après make check)
make data                     # régénérer data/*.json depuis les résultats existants du dépôt
make film CUT=update          # épisode « Results update » (scènes dont les résultats sont arrivés)
make test                     # test complet du pipeline sur script/_test (voix factice, sans API)
make serve                    # prévisualiser une scène : http://127.0.0.1:8765/scenes/<unité>/<page>.html
make film CUT=extended LANG=fr   # la même chose avec la narration française (LANG=fr vaut pour toutes les commandes)
make test LANG=fr             # test complet de la version française sur script/_test (voix factice, sans API)
```

Le film sort en `out/film_<coupe>.mp4` (H.264 1080p30, moins de 1,9 Go, AAC 192 kb/s), avec deux pistes
audio : 1 = narration + musique + effets, 2 = musique et effets sans narration. Les chapitres sont inscrits
dans le MP4 et listés dans `out/film_<coupe>_chapters.txt` (format des descriptions YouTube). Mixage
à −16 LUFS, crête vraie ≤ −1 dBTP. Rien n'est refait inutilement : une scène n'est re-rendue que si sa
page, ses données, son texte, son minutage ou les réglages changent, et un paragraphe déjà synthétisé
n'est jamais refacturé.

## Version française

La narration française (BRIEF §9) passe sur **les mêmes images** : textes à l'écran, étiquettes et formules
restent en anglais ; seuls la voix et les sous-titres changent. Toutes les commandes ci-dessus acceptent
`LANG=fr` (`LANG=en` par défaut) :

```bash
make plan  CUT=core LANG=fr      # phrases encore non traduites, mots à synthétiser, scènes à rendre
make draft CUT=core LANG=fr      # brouillon français (voix du cache ou factice, jamais l'API)
make film  CUT=extended LANG=fr  # out/film_extended_fr.mp4
make check U=ch04 LANG=fr        # une image par repère avec le minutage français
```

- **Texte** : `script/fr/<unité>.json` (une surcouche par unité, les scripts anglais ne sont pas modifiés) :
  `{"schema": 2, "unit", "lang": "fr", "voice", "sentences": {identifiant: texte}, "variants": {scène:
  {identifiant: texte}}, "notes"}`, et un `"title"` facultatif (nom du chapitre dans le MP4). Chaque phrase
  garde son identifiant et son repère : les scènes s'animent sur les noms de repères, jamais sur des temps.
  Le balisage des sous-titres (`{u}…{/}`, `{b}…{/}`, `{param}…{/}`, `{model}…{/}`, `{metric}…{/}`) entoure
  les mots français correspondants et les champs `{{…}}` sont gardés tels quels (l'assembleur signale tout
  écart avec la phrase anglaise). À défaut de surcouche, un champ `text_fr` du script anglais est repris ;
  sinon la phrase reste en anglais, signalée « untranslated » par `make plan` (et `make film` refuse de la
  facturer). Les cartes-questions sans paragraphe sont dites à partir de `question.fr`.
- **Résultats** : les champs `{{…}}` des variantes `result` sont dits en français (« zéro virgule
  quatre-vingt-six ») ; un champ texte des convertisseurs est pris dans sa version `<champ>_fr` s'il existe.
- **Voix** : « Ethan » parlant français (même voix, mêmes réglages drama-3, corps `"language": "fr"`),
  lue dans la surcouche (`voice`), puis `voice_fr` du script ; `make narration LANG=fr VOICE=<id>` la remplace
  pour tout le film français (`audio/voice_fr.json`, voir `NARRATION.md`).
- **Prononciation** : `audio/lexicon_fr.json` (réécritures, la voix française n'accepte pas les phonèmes
  ARPAbet) : sigles épelés à la française (MHD, ABC, VKS, ENPC, LISN), noms dits comme un physicien français
  (Gissinger, Reynolds, Prandtl, Kármán, Rice, Leray), termes d'apprentissage automatique gardés en anglais
  (*flow matching*).
- **Sorties séparées**, suffixe `_fr` : `out/film_<coupe>_fr.mp4` (piste 1 marquée française), pistes
  `out/stems/<coupe>_fr_*.m4a`, sous-titres français `subs/<coupe>_fr.{srt,vtt,ass}` incrustés dans les
  rendus de `out/scenes_fr/`, minutage `script/_build/<coupe>_fr_cues.json`, pistes de narration
  `audio/scenes_fr/`. Rien de la version anglaise n'est recalculé ni re-rendu par une construction française.
- **Cache** : indexé par (langue, texte, voix, réglages) ; les clés anglaises sont inchangées.
- **Cache versionné** : les `audio/cache/*.mp3` et leurs `.json` sont dans git (≈ 245 Mo, 751 paragraphes EN + FR). Après un nouveau clone, `make film` redécode les `.wav` depuis les mp3 sans appel à Fish ; seuls les paragraphes dont le texte a changé sont resynthétisés (clé `FISH` requise, voir `NARRATION.md`). Pensez à committer les nouveaux mp3 du cache après une modification.
- Le minutage français est plus long (+15 à 20 % attendus) : `make plan LANG=fr` ne signale une scène qu'au-delà
  de +40 % de sa durée cible.

## Quand les résultats du cloud arrivent

Les scènes PENDING sont des « places vides » : elles montrent le pari, le raisonnement, le critère de
succès et la question à trancher avec les encadrants. Chacune déclare ses fichiers de données (`deps`)
et porte deux narrations : `pending` (aujourd'hui) et `result` (écrite pour les deux issues, avec des
champs `{{…}}` remplis depuis les données).

1. Rapatrier les sorties de calcul à côté du projet (voir `plan/outline.md`, `run_env`) puis les convertir
   avec `python3 -I tools/data_cloud.py <convertisseur> …` (un convertisseur par campagne, liste dans
   `CONTRACT.md` §5) : les fichiers `data/*.json` correspondants apparaissent, avec le verdict et les
   champs de la narration `result` (un fichier inchangé ne déclenche rien).
2. `make plan CUT=extended` : les scènes dont toutes les données sont là passent en **provisional** avec
   leur narration `result` ; le plan indique les paragraphes à synthétiser et les scènes à re-rendre.
3. `make films` : seules ces scènes sont resynthétisées et re-rendues, le reste est réutilisé.
4. Relire (`make check U=ch10`, `make draft`), puis passer la scène à `"status": "ready"` dans le script
   (le tampon PROVISIONAL DATA disparaît).
5. Épisode « Results update » : `make film CUT=update` (scènes de `plan/outline.json`,
   `results_update_episode`, en version résultat ; celles dont les données manquent encore sont écartées).

## Changer la voix ou enregistrer une narration

Voir **`NARRATION.md`** : `make narration VOICE=<reference_id>` pour une autre voix Fish Audio
(`make narration LANG=fr VOICE=<reference_id>` pour la version française),
`make narration-script` puis `make fit DIR=prises/` pour ajuster une narration enregistrée ailleurs
(étirement phrase par phrase dans ±12 %, ou re-minutage des scènes).

## À savoir

- Clé Fish Audio : injectée par le proxy réseau pour `api.fish.audio` (aucune clé dans les fichiers).
  `make film` appelle l'API pour les paragraphes absents du cache ; `make plan` et `make draft` jamais.
- Garde-fou de coût : au-delà de 15 000 mots nouveaux d'un coup, la synthèse refuse de partir
  (`TTS_MAX_NEW_WORDS=…` pour le relever).
- `audio/cache/` contient l'audio payé : le conserver (il n'est pas suivi par git).
- Aucune simulation, aucun entraînement, aucun benchmark n'est lancé par ce dossier.
