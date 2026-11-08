# Fish Audio — inventaire, sans appel

Cette phase n’a pas demandé de clé, n’a pas lu de fichier d’identifiants, n’a pas appelé l’API, n’a pas dépensé de crédit. Minutes facturées : **0**. Requêtes : **0**.

La voix reste interdite tant que la porte G0 est ouverte, et ensuite tant que les scripts ne sont pas gelés (porte G1). Le cache doit exister avant la première requête, pour ne jamais payer deux fois le même triplet (texte, voix, réglages).

## Voix

- Bibliothèque Fish Audio, voix « Ethan », créée par Fish Audio.
- `reference_id` : `536d3a5e000945adb7038665781a4aca`.
- La même voix pour l’anglais et pour le français.
- Interdit : tout clone, toute imitation d’une personne réelle, toute autre `reference_id` non décidée par l’auteur.
- Le kit futur ne change que ce paramètre, puis recale les scènes sur les repères nommés.

## Requête prévue (non envoyée)

- `POST https://api.fish.audio/v1/tts`
- En-tête `model: drama-3`
- Corps : `temperature` 0.1, `format` mp3, `mp3_bitrate` 192, `sample_rate` 44100, `latency` normal, `normalize` true, `condition_on_previous_chunks` true
- `prosody` : `speed` 1.0, `normalize_loudness` true
- Une requête par paragraphe
- Une seule indication de jeu, au début du film : `[calm, natural narrator voice]`
- `[long pause]` seulement entre paragraphes principaux
- Pas de balise `<emphasis>` ni `<stress>`
- Pour ralentir : `atempo` ffmpeg, jamais `speed` < 1

La clé viendra de l’environnement, hors dépôt, sous le nom que l’auteur aura choisi au moment des fondations. Ce nom n’est pas cherché ici. Aucun `.env` n’est lu.

## Mots à épingler plus tard

Les chaînes phonémiques ne sont pas écrites dans cette phase : une mauvaise chaîne serait une narration déguisée. La liste à traiter, avec `<|phoneme_start|>…<|phoneme_end|>`, avant la première synthèse :

MilaDy, MHD, ABC, VKS, DRESDYN, SFEMaNS, LATU, Gissinger (prononciation française), Reynolds, Rm, Re, Pm, Leray, Heun, Liouville, Rice, Cowling, Ponomarenko, Karlsruhe, Cadarache, Zel'dovich, Poincaré, Kazantsev, Wasserstein, Fokker–Planck, TorchDA, GENCI, Jean Zay, CEREA, ENPC, LISN, DQVU, PySINDy, FunDiff, Cheng, Lucor, Nore, Ponty, Pétrélis, Glatzmaier seulement si la revue science débloque le nom.

Le français d’Ethan utilise la même voix et une liste phonémique séparée là où l’orthographe française divergerait (Gissinger déjà imposé en prononciation française dans les deux pistes).

## Volume futur, non mesuré

On ne connaît pas le nombre de paragraphes : les scripts n’existent pas. Estimation interdite. Après G1, le journal `STATS.md` comptera les requêtes réellement envoyées, les succès de cache, et les minutes facturées si l’API les renvoie. Si l’API ne renvoie pas de coût, la case reste `unavailable`.

Contrôle prévu, plus tard : faster-whisper `base` ou `small`, anglais et français, comparaison au script, resynthèse des paragraphes fautifs seulement.

## Ce qui ne sera jamais commité

La clé, les fichiers `.env`, un export de compte Fish, un extrait audio d’une personne réelle.
