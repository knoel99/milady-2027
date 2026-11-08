# Kit de changement de narration

La narration du film peut être remplacée sans toucher aux animations. Chaque scène s'anime sur des
**noms de repères** (le début de chaque phrase du script : `dials`, `eqs`, `predict`…), jamais sur des
temps écrits en dur. Une nouvelle voix change les durées, le pipeline recalcule les repères et les
scènes suivent toutes seules. Seules les scènes dont le minutage a bougé sont refaites.

## 1. Où se trouve quoi

| Élément | Fichier |
|---|---|
| Voix du script | `voice.reference_id` dans chaque `script/<unité>.json` (aujourd'hui : « Ethan », `536d3a5e000945adb7038665781a4aca`) |
| Voix imposée pour tout le film (prioritaire) | `audio/voice.json`, écrit par `make narration VOICE=…` |
| Prononciations | `audio/lexicon.json` (phonèmes ARPAbet ; Gissinger à la française) |
| Audio déjà payé | `audio/cache/<clé>.mp3` et `.wav`, un fichier par paragraphe (à garder et sauvegarder) |
| Piste de narration de chaque scène | `audio/scenes/<scène>.wav` et `.align.json` (temps de chaque phrase) |
| Narration externe ajustée | `audio/external/<scène>.wav` et `.align.json` |
| Temps de chaque phrase du film | `script/_build/<coupe>_cues.json` |
| Sous-titres (texte du script) | `subs/<coupe>.srt`, `.vtt`, `.ass` |
| Pistes séparées | `out/stems/<coupe>_narration.m4a`, `_music.m4a`, `_effects.m4a`, `_nonarration.m4a` |
| Film | `out/film_<coupe>.mp4` : piste audio 1 = mixage complet, piste audio 2 = musique et effets sans voix |

`<coupe>` vaut `core` (≈ 41 min) ou `extended` (≈ 60 min).

Narration française (`LANG=fr`, §6) : mêmes éléments avec le suffixe `_fr` ou `fr` : texte
`script/fr/<unité>.json`, voix `audio/voice_fr.json` puis `voice` de la surcouche, prononciations
`audio/lexicon_fr.json`, pistes `audio/scenes_fr/`, narration externe `audio/external_fr/`, minutage
`script/_build/<coupe>_fr_cues.json`, sous-titres `subs/<coupe>_fr.*`, pistes séparées
`out/stems/<coupe>_fr_*.m4a`, film `out/film_<coupe>_fr.mp4`. Le cache `audio/cache/` est commun aux deux
langues (la langue fait partie de la clé).

## 2. Changer de voix Fish Audio

```bash
make narration VOICE=<reference_id>          # les deux coupes ; CUTS=core pour une seule
make narration VOICE=default                 # revenir à la voix des scripts
```

Ce que fait la commande :

1. écrit `audio/voice.json` (la voix choisie s'applique à toutes les unités, sans modifier les scripts) ;
2. synthétise **chaque paragraphe** avec la nouvelle voix (une requête par paragraphe, réglages validés :
   drama-3, température 0.1, `[calm, natural narrator voice]` en tête, `[long pause]` entre paragraphes) ;
3. recalcule le temps de chaque phrase (détection des silences), les durées des scènes et les repères ;
4. refait les sous-titres, ne re-rend que les scènes dont le minutage a changé, refait le mixage et le MP4.

Coût : environ 7 700 mots pour la coupe longue (la coupe courte réutilise les mêmes paragraphes).
Avant de lancer, `make plan CUT=extended` affiche le nombre de paragraphes et de mots à synthétiser.
Un garde-fou refuse une synthèse de plus de 15 000 mots nouveaux d'un coup
(`TTS_MAX_NEW_WORDS=20000 make narration …` pour le relever volontairement).

Le cache est indexé par (langue, texte, voix, réglages) : revenir à une voix déjà utilisée ne coûte rien, et un
paragraphe inchangé n'est jamais refacturé. Pour écouter une voix avant de tout lancer, une seule phrase :
`make tts-test SENTENCE="Une phrase en anglais." UNIT=ch00` (avec la voix de `script/ch00.json`), ou
`make narration VOICE=<id>` puis `make draft` sur une seule unité (`make check U=ch00`).

**Règle** : uniquement une voix originale de la bibliothèque Fish Audio ou une voix dont on détient les
droits (narrateur consentant). Jamais un clone ni une imitation d'une personne réelle.

## 3. Enregistrer une narration ailleurs et l'ajuster

1. Préparer le texte pour le narrateur :
   ```bash
   make narration-script CUT=extended     # -> out/narration_script_extended.md
   ```
   Un bloc par scène (= un fichier à enregistrer, nommé `<scène>.wav`), chaque phrase avec sa durée
   actuelle entre crochets. Lire dans l'ordre, marquer une pause d'environ une seconde entre paragraphes,
   pas de musique ni d'effet dans la prise.
2. Déposer les fichiers dans un dossier, par exemple `takes/` (`04.1.wav`, `04.2.wav`, …). Un seul long
   fichier pour toute la coupe est aussi accepté (`AUDIO=prise.wav`), mais un fichier par scène est plus sûr.
3. Ajuster :
   ```bash
   make fit DIR=takes/ CUT=extended              # ajustement phrase par phrase
   make fit DIR=takes/ CUT=extended RETIME=auto  # + re-minutage des scènes hors tolérance
   ```
   Chaque prise est découpée en phrases par détection des silences, puis chaque phrase est étirée ou
   comprimée (rubberband, sans changer la hauteur) pour tomber exactement dans la case de la narration
   actuelle, **dans la limite de ±12 %**. Une phrase plus longue peut aussi mordre sur le début de la pause
   qui la suit.
   - Si toutes les phrases d'une scène tiennent, la scène garde son minutage : rien n'est re-rendu.
   - Sinon, le rapport (`audio/external/<coupe>_fit_report.json` et la console) liste les phrases hors
     tolérance avec le facteur nécessaire (par exemple « 04.3.s2 needs x1.18 »). Deux choix : réenregistrer
     ces phrases plus près de leur durée, ou relancer avec `RETIME=auto`, qui re-minute ces scènes sur le
     rythme naturel de la prise (elles seront re-rendues). `RETIME=all` re-minute tout le film sur la prise.
   - La prise est ramenée au niveau sonore de la narration actuelle (un seul gain pour toute la prise).
4. Construire le film avec la narration externe :
   ```bash
   make film CUT=extended NARRATION=external
   ```
   Les scènes sans enregistrement, ou dont le texte a changé depuis l'ajustement, gardent la voix de
   synthèse (un avertissement le signale).

## 4. Doublage et versions

- La **piste audio 2** du MP4 et `out/stems/<coupe>_nonarration.m4a` contiennent la musique et les effets
  sans voix : c'est la base d'un doublage dans une autre langue.
- Les pistes séparées sont au même gain que le mixage complet : narration + musique + effets = mixage
  (avant le limiteur final). Mixage final : −16 LUFS intégré, crête vraie ≤ −1 dBTP.
- `script/_build/<coupe>_cues.json` donne le début et la fin de chaque phrase sur l'horloge du film, et
  les sous-titres sont toujours tirés du **texte du script**, jamais d'une transcription.

## 5. Prononciation

Corriger une entrée de `audio/lexicon.json` (par exemple MilaDy, DRESDYN, LATU, GENCI, marqués à
vérifier) ne resynthétise que les paragraphes qui contiennent ce mot. Une entrée est soit une suite de
phonèmes ARPAbet, soit `{"say": "réécriture"}` pour une simple réécriture.

Pour la narration française, `audio/lexicon_fr.json` ne contient que des réécritures (les épingles de
phonèmes de Fish Audio ne valent que pour l'anglais) : sigles épelés à la française (« ème hache dé » pour
MHD, « a bé cé », « vé ka esse », « eu ène pé cé »), noms dits comme un physicien français (« Jissinjé »,
« Rénolds », « Prantl », « Karmane », « Raïsse », « Lerè », « Milédi »). Une entrée `{"keep": true}` documente
un mot laissé tel quel, par exemple les termes d'apprentissage automatique gardés en anglais (*flow
matching*) : la voix multilingue les lit en anglais ; `alt` propose une réécriture si une prise sonne mal.
Les entrées de la liste `check` (MilaDy, LATU, LISN, SFEMaNS, GENCI, Gissinger…) attendent une confirmation.

## 6. Narration française

La version française garde les images anglaises et change la voix et les sous-titres. Toutes les commandes
de ce kit prennent `LANG=fr` :

```bash
make plan CUT=extended LANG=fr               # phrases non traduites, mots à synthétiser (rien n'est appelé)
make narration LANG=fr VOICE=<reference_id>  # voix française de tout le film (audio/voice_fr.json), deux coupes
make narration LANG=fr VOICE=default         # revenir à la voix des surcouches (« Ethan », 536d3a5e…)
make tts-test SENTENCE="Une phrase en français." UNIT=ch00 LANG=fr   # une seule requête, voix de script/fr/ch00.json
make narration-script CUT=extended LANG=fr   # texte de lecture français -> out/narration_script_extended_fr.md
make fit DIR=prises_fr/ CUT=extended LANG=fr # ajuster une narration française enregistrée ailleurs
make film CUT=extended LANG=fr NARRATION=external
```

- **Texte** : `script/fr/<unité>.json`, une surcouche par unité, les scripts anglais restent figés.
  `sentences` donne le texte de chaque phrase des paragraphes principaux (même identifiant, même repère :
  ne jamais fusionner ni couper une phrase) ; `variants` celui des variantes `result` des scènes PENDING,
  avec les champs `{{…}}` tels quels (les nombres sont dits en français : « zéro virgule quatre-vingt-six ») ;
  `voice` la voix ; `notes` les choix de traduction ; `title` (facultatif) le nom du chapitre dans le MP4.
  Le balisage des sous-titres entoure les mots français correspondants. Une phrase sans traduction reste en
  anglais : `make plan LANG=fr` la signale et `make film LANG=fr` refuse de la facturer
  (`TTS_ALLOW_UNTRANSLATED=1` pour passer outre).
- **Voix** : « Ethan » parlant français (`536d3a5e000945adb7038665781a4aca`), corps de requête validé
  inchangé sauf `"language": "fr"` (même `[calm, natural narrator voice]` en tête, même `[long pause]` entre
  paragraphes, température 0.1). Priorité : `audio/voice_fr.json` (`make narration LANG=fr VOICE=…`), puis la
  `voice` de la surcouche, puis `voice_fr` du script anglais. La règle de la §2 vaut aussi : jamais un clone.
- **Minutage** : le français est plus long (≈ +15 à 20 %) ; la coupe française a son propre minutage
  (`script/_build/<coupe>_fr_cues.json`) et ses propres rendus (`out/scenes_fr/`, sous-titres français
  incrustés). Une construction française ne touche ni aux rendus ni aux pistes anglaises.
- **Coût** : environ autant de mots que la version anglaise, plus 15 à 20 % ; `make plan LANG=fr` donne le
  compte exact avant de lancer.
- **Doublage depuis la piste 2** : la piste audio 2 du film anglais (musique et effets sans voix) reste la base
  d'un doublage fait ailleurs ; `make fit LANG=fr` ajuste alors une prise française sur le minutage français.
