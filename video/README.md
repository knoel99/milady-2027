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
| `script/_build/` | coupes assemblées (`film_core.json`, `film_extended.json`), temps de chaque phrase (`<coupe>_cues.json`), liste des questions (`questions_<coupe>.json`) |
| `scenes/<unité>/` | une page HTML par scène ; `runtime/` : moteur déterministe et composants partagés |
| `data/` | données des scènes, extraites des résultats existants du dépôt (`make data`) |
| `audio/` | synthèse vocale (`tts.py`), minutage des phrases (`align.py`), mixage (`mix.py`), prononciations (`lexicon.json`), cache des voix déjà payées (`cache/`, à conserver) |
| `subs/` | sous-titres `.srt`, `.vtt`, `.ass` de chaque coupe, tirés du texte du script |
| `out/` | rendus : `film_<coupe>.mp4`, pistes séparées `stems/`, brouillons `draft/`, vérifications `check/` |

## Commandes

```bash
make plan CUT=extended        # ce qui serait synthétisé (mots, paragraphes) et re-rendu, sans rien calculer
make film CUT=extended        # construction complète : voix (cache), scènes modifiées, mixage, MP4
make films                    # les deux coupes
make draft CUT=core           # brouillon 960x540 à 15 i/s pour relecture (n'appelle pas l'API)
make scene S=04.3             # refaire une scène puis réassembler
make check U=ch04             # une image par repère de chaque scène d'une unité + erreurs de page
make data                     # régénérer data/*.json depuis les résultats existants du dépôt
make film CUT=update          # épisode « Results update » (scènes dont les résultats sont arrivés)
make test                     # test complet du pipeline sur script/_test (voix factice, sans API)
make serve                    # prévisualiser une scène : http://127.0.0.1:8765/scenes/<unité>/<page>.html
```

Le film sort en `out/film_<coupe>.mp4` (H.264 1080p30, moins de 1,9 Go, AAC 192 kb/s), avec deux pistes
audio : 1 = narration + musique + effets, 2 = musique et effets sans narration. Les chapitres sont inscrits
dans le MP4 et listés dans `out/film_<coupe>_chapters.txt` (format des descriptions YouTube). Mixage
à −16 LUFS, crête vraie ≤ −1 dBTP. Rien n'est refait inutilement : une scène n'est re-rendue que si sa
page, ses données, son texte, son minutage ou les réglages changent, et un paragraphe déjà synthétisé
n'est jamais refacturé.

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

Voir **`NARRATION.md`** : `make narration VOICE=<reference_id>` pour une autre voix Fish Audio,
`make narration-script` puis `make fit DIR=prises/` pour ajuster une narration enregistrée ailleurs
(étirement phrase par phrase dans ±12 %, ou re-minutage des scènes).

## À savoir

- Clé Fish Audio : injectée par le proxy réseau pour `api.fish.audio` (aucune clé dans les fichiers).
  `make film` appelle l'API pour les paragraphes absents du cache ; `make plan` et `make draft` jamais.
- Garde-fou de coût : au-delà de 15 000 mots nouveaux d'un coup, la synthèse refuse de partir
  (`TTS_MAX_NEW_WORDS=…` pour le relever).
- `audio/cache/` contient l'audio payé : le conserver (il n'est pas suivi par git).
- Aucune simulation, aucun entraînement, aucun benchmark n'est lancé par ce dossier.
