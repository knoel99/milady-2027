# Changer la voix

Ce kit remplace `reference_id`, recalcule les clés de cache, et recale une prise externe sur les repères nommés. Il n'envoie aucune requête.

La voix en cours dans le plan est Ethan, `536d3a5e000945adb7038665781a4aca`. Le manifeste garde ce paramètre, le texte, et les repères. Les temps des scènes restent dans les repères.

## Préparer le manifeste

Écrivez un fichier JSON avec la voix et les paragraphes.

```json
{
  "reference_id": "536d3a5e000945adb7038665781a4aca",
  "paragraphs": [
    {
      "id": "ouverture",
      "text": "The field flips.",
      "cues": ["start", "show"]
    }
  ]
}
```

`cues` reprend les identifiants de la scène. Le kit ne les remplace pas par des secondes.

## Changer reference_id

Lancez la commande depuis `video-grok/tools`.

```bash
node kit-voix/changer.mjs \
  --manifest manifeste.json \
  --vers 0123456789abcdef0123456789abcdef \
  --cache /tmp/voix-cache
```

La sortie JSON a `requests` à 0. Chaque paragraphe a `stale: true` quand le cache n'a pas encore la nouvelle clé. Un paragraphe déjà en cache pour cette voix a `stale: false`.

Pour écrire le manifeste à la nouvelle voix, ajoutez `--ecrire manifeste-nouveau.json`. Les textes et les repères sont copiés. Le fichier d'origine reste en place.

Le cache garde le premier fichier reçu pour une clé. Une deuxième écriture de la même clé ne le remplace pas. La clé est le SHA-256 du texte, de `reference_id`, et des réglages de synthèse. Ces réglages sont `drama-3`, température 0,1, mp3 à 192 kilobits par seconde, 44,1 kHz, et `speed` 1. Pour ralentir un fichier déjà synthétisé, utilisez `atempo` dans ffmpeg. Ne baissez pas `speed` sous 1.

## Aligner une prise externe

Préparez les durées prévues, une par phrase, dans l'ordre de la prise.

```json
[
  { "id": "ouverture", "cue": "start", "duration": 2.4 }
]
```

```bash
node kit-voix/aligner.mjs --wav prise.wav --phrases phrases.json
```

Le programme coupe la prise sur les silences. Il compare chaque morceau à la durée prévue.

Si l'écart tient dans 12 %, la ligne dit `action` `atempo` et donne le facteur ffmpeg. `atempo` supérieur à 1 accélère. `atempo` inférieur à 1 ralentit. Les deux restent dans la bande de 12 %.

Si l'écart dépasse 12 %, la ligne dit `action` `reminutage` et donne `at`, le début du morceau en secondes. Placez ce temps sur le repère `cue`. Ne réécrivez pas l'animation avec une constante de temps.

Le wav attendu est PCM 16 bits, mono.
