# Contrat de scène

Ce que doit respecter une page de scène pour que le moteur la rende. Chaque règle renvoie au code qui l'impose ; en cas de désaccord, le code fait foi et ce fichier se corrige. Le style (couleurs, tailles, zones) est fixé par `runtime/theme.css` et `runtime/components/` (CLAUDE.md, « Le film »). Les numéros de section sont ceux que citent les commentaires du code (« CONTRACT §9 », « §11 »).

## 1. Une scène = une page HTML

- Chemin : `scenes/<unité>/<nn>_<slug>.html`, par exemple `scenes/ep01/05_carre.html`. Une page par scène. Le même chemin, relatif à `video/`, va dans le champ `"file"` de la scène (§8).
- Scène 1920 × 1080 px CSS : un seul `<div id="stage"></div>`, tout dedans. Sans lui, `Scene.define` lève « no #stage element » (`runtime/scene.js`, `defineImpl`).
- Chemins relatifs depuis `scenes/<unité>/` : `../../runtime/…` et `../../vendor/…`. Le serveur sert `video/` à la racine et le dépôt sous `/site/` (`tools/server.js`). Dans le code, `Scene.url('data/…')`, `'vendor/…'`, `'runtime/…'` se résolvent depuis `video/` quelle que soit la profondeur (`Scene.url`, d'après l'URL de `scene.js`).
- Ordre des scripts : KaTeX si besoin, `runtime/scene.js`, puis `components/kit.js` avant tout autre composant (`kit.js` lève une erreur sinon), puis ceux qu'on utilise. Aucune ressource externe : polices et bibliothèques dans `vendor/` (KaTeX, GSAP, Three.js).

```html
<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>ep01.05 Le petit carré</title>
<link rel="stylesheet" href="../../vendor/katex/katex.min.css">
<link rel="stylesheet" href="../../runtime/theme.css">
<script src="../../vendor/katex/katex.min.js"></script>
<script src="../../runtime/scene.js"></script>
<script src="../../runtime/components/kit.js"></script>
<script src="../../runtime/components/equation.js"></script>  <!-- et les autres au besoin -->
</head><body><div id="stage"></div>
<script>Scene.define({ /* §2 */ });</script></body></html>
```

## 2. `Scene.define` et ses hooks

```js
Scene.define({
  duration: 67,                 // aperçu seulement : le moteur injecte la vraie durée (entry.duration)
  register: 'night',            // défaut d'aperçu ; le "register" du script l'emporte
  cues: { 'e1-formule': 0.4 },  // TOUS les repères utilisés, avec un temps d'aperçu
  data: { x: 'data/x.json' },   // facultatif ; { url, optional: true } pour un fichier qui peut manquer
  params: {},                   // surchargés par entry.params
  setup(ctx) {},                // construit tout une fois : DOM, SVG, KaTeX, composants, géométrie
  render(t, ctx) {},            // facultatif : fonction pure de t, après les composants
  afterRender(t, ctx) {},       // facultatif, attendu avant que l'image soit prise
});
```

- Sans durée (`spec.duration` ni `entry.duration`), erreur de scène (`defineImpl`).
- Ordre à chaque `seek(t)` : animations Web mises à `t`, `render` de chaque composant enregistré par `ctx.add`, `spec.render`, rappels `requestAnimationFrame` en file, `afterRender` (`seek`).
- `ctx` : `at(spec)`, `cue(nom, défaut)`, `data`, `params`, `status`, `variant`, `script` (l'entrée injectée), `stage`, `duration`, `register`, `add(composant)`, `warn`.
- Outils de `Scene` : `seg`, `ease`, `spring` (dépassement ≤ 3 %), `stepper`, `rng(clé)`, `col(jeton)`, `hidpi`, `url`, `f32`, `C` (jetons NIGHT).
- Toute erreur de `setup`, de données ou de police remplit `window.__SCENE_ERROR__` ; le rendu s'arrête (`Scene.define`, `stills.js`, `capture.js`).

## 3. Temps, repères et `window.__ENTRY__`

- Le moteur ouvre la page avec `window.__CAPTURE__ = true` et `window.__ENTRY__` (`stills.js`, `capture.js`, `addInitScript`). Entrée construite par `build.js` (section 3, « timeline ») : `id`, `unit`, `duration`, `fps`, `cues`, `sentences`, `status`, `variant`, `register`, `badge`, `title`, `onscreen`, `data`, `params`, `seed`, `lang`.
- `cues` : un repère par phrase qui en porte un (`"cue"` du script), au début de la phrase, plus `s_<id de phrase>`, `_speech_end` et `_tail` (`build.js`). Durée = `lead_in` + voix + pauses `hold_after` + `tail`, en images entières.
- La scène s'anime sur les noms de repères, jamais sur des secondes en dur : `ctx.at('e1-droit')`, `ctx.at('e1-droit+0.6')`, `ctx.at('e1-droit-0.15')`. Un nom inconnu est une erreur de scène ; un repère déclaré dans `cues` mais absent du script donne un avertissement (`at`, `defineImpl`).
- En aperçu (`make serve`), les temps de `cues` servent, et `_tail`, `_speech_end` se déduisent de la durée.
- Pause de prédiction : la question sur son repère, la réponse sur le repère du paragraphe suivant ; l'attente est le `hold_after` du script, jamais un nombre dans la scène (`cards.js`, `Kit.predictCard`).

## 4. Composants

- Fabriques `Kit.<nom>(ctx, opts)`, appelées dans `setup`. Options communes : `at`, `out` (repères), `parent`. Chacune s'enregistre par `ctx.add` et se redessine comme fonction pure de `t` (`kit.js`, en-tête). La galerie `scenes/_gallery/gallery.html` les montre toutes.
- `kit.js` : DOM, calques, texte (`Kit.upper`, jamais `text-transform`), `Kit.tex`, `Kit.fit`. `hud.js` : badge, bandeaux, rail, calque de formule (un élément à la fois), puces. `equation.js` : `Kit.equation` (termes `\term{id}{…}`, révélation par repères), `Kit.morph`. `field.js` : `Kit.arrows` (options `compress` et `hole`), `Kit.tracers`, `Kit.fieldLines`, `Kit.fieldMap`. `motifs.js` : dont `Kit.pen` (`head: false` pour un trait sans pointe). `plot.js`, `cards.js`, `seat.js`, `threemodes.js`.
- `ep-kit.js`, écarts acceptés pour ep01 : `Kit.readout` (compteur, virgule décimale, jamais « −0 », chiffres tabulaires), `Kit.fmtFr`, `Kit.probe` (cercle-sonde, flux ou circulation par quadrature sur 256 points pondérée par l'élément d'arc), `Kit.paddleWheel` (roue à aubes, angle en forme fermée), `Kit.marchingSquares` et `Kit.levelLines`, `Kit.compressLength`. Ils calculent en coordonnées mathématiques, y vers le haut, et dessinent par le `toPx(x, y)` de la scène. Jeton `--fg-2` pour un champ neutre : classe `.k-fg2`, macro `\cn{…}`, `Kit.cmap('fg-2', v)`.
- Couleurs : uniquement les jetons (`Kit.c('u')`, `var(--u)`), jamais de code hexadécimal dans une scène (`theme.css`, en-tête des jetons).

## 5. Données

- Les nombres de résultats viennent de `data/*.json`, déclarés dans `data`, jamais tapés dans une scène. Les convertisseurs sont `tools/data_existing.py` (`make data`) et `tools/data_cloud.py` ; aucun n'existe encore dans ce film (`tools/extract_data.py`). Une scène qui calcule son champ analytiquement n'a pas de données.
- Fichier manquant non facultatif : erreur de scène, sauf scène `pending` (`loadData`).

## 6. Cadre sûr et bande des sous-titres

- Cadre sûr : x de 96 à 1824, y de 56 à 880 (`Kit.SAFE`). Bande des sous-titres : y ≥ 900, sous-titres incrustés par `capture.js` (option `--ass`) ; rien d'important sous y = 880 (`theme.css`, en-tête).
- Zones fixes : badge, aiguille de coin, rail, bandeau en bas à gauche, calque de formule en bas à droite (`Kit.ZONES`).
- Texte : 28 px au moins après transformations (`theme.css`, `__QA__`). Chiffres qui changent : `.tnum` (`theme.css` : pas de chiffres tabulaires globaux). Échelle z : canvas 5–9, SVG 10–16, équations 20–21, stylo 30, puces 45, calques fixes 50–55 (`theme.css`, « kit layers »).
- Aperçu : touche `g` ou `?safe=1` pour voir le cadre et la bande (`startPreview`).

## 7. Galerie et images fixes

- `make stills S=scenes/<unité>/<page>.html T=0.5,2,4 [ENTRY=entrée.json]` : images fixes aux instants donnés, dans `out/stills/` (`stills.js`). Une planche de la galerie : `S='scenes/_gallery/gallery.html?plate=17'`.
- `make serve` : aperçu sur http://127.0.0.1:8765/ avec barre de lecture (`tools/server.js`, `startPreview`).

## 8. Comment le moteur trouve une scène

- `script/<unité>.json`, schéma 2 : `scenes[]`, chacune avec `id`, `"file"` (chemin de la page depuis `video/`), `paragraphs[{hold_after, sentences[{id, cue, text}]}]`, `target_s`, `register`. Une unité écrite en français déclare `"lang": "fr"` à sa racine et se construit avec `LANG=fr` (`tools/assemble_cut.py`, docstring).
- `plan/outline.json` : `cuts.core.chapters` donne l'ordre des unités.
- `assemble_cut.py` résout la scène et refuse une scène sans `"file"` ; `build.js` refuse un fichier absent (« missing scene file ») et hache la page, son dossier, `runtime/` et l'entrée pour ne rerendre que ce qui a changé (`fileHash`, `runtimeHash`).
- Repères : `cue` doit valoir `^[A-Za-z_][\w-]*$` et rester unique dans la scène (`assemble_cut.py`, `CUE_RE`).

## 9. Déterminisme

- Une image est une fonction pure de `t`, des données et de l'entrée. En capture, `Date.now`, `performance.now` et `requestAnimationFrame` suivent l'horloge virtuelle ; `Math.random` est graine fixée (`entry.seed`) dans tous les modes (`scene.js`, en-tête).
- Pas de `setTimeout`, de `setInterval`, de transition ni d'animation CSS libre. Hasard : `Scene.rng('clé')`. État qui évolue : `Scene.stepper(init, step, dt)`, dont `init` reconstruit tout (retour en arrière). Rotation de la roue, trajectoires, transports : en forme fermée.
- Construire dans `setup`, jamais d'élément créé dans `render`. État d'un contexte Canvas : `Kit.canvasLayer(…, {reset: true})` ou `L.reset()` en tête du rendu (`kit.js`).
- Vérification : `make det U=<unité> LANG=fr` après `make check` (`tools/determinism.js` : deux images directes identiques au bit près, lecture séquentielle sans écart au-delà de l'anticrénelage).
- Première image jamais vide : la scène est collée à la précédente ; poser la mise en place avec un `at` négatif (`stills.js`, « blank first frame »).

## 10. Interdits

- Pas de nombre de résultat dans le code d'une scène, pas de verdict calculé par la scène (§5).
- Pas de texte sous 28 px, rien dans la bande des sous-titres, rien de coupé au bord (§6).
- Pas de couleur hors jetons, pas de `text-transform`, pas de ressource du web.
- Pas de synthèse vocale pour essayer une scène : `make check` et `make draft` n'appellent jamais l'API (CLAUDE.md, « Commandes payantes » ; `build.js`, `UNITBUILD`).

## 11. Contrôle de mise en page et liste de vérification

`make check U=<unité> LANG=fr [S=id] [TIMING=estimate]` (`build.js --check`, puis `stills.js` en mode chronologie) prend, pour chaque scène, la première image, le milieu de l'entrée, 0,2 s avant et 0,6 s après chaque repère, la dernière image ; il relève erreurs de page, de console et de requête, `window.__SCENE_WARNINGS__`, première image vide, et `window.__QA__(t)` à chaque image fixe. Sorties : `out/check/unit_<unité>_fr[_est]/` (images, planche contact, `report.json`). Types de `__QA__` (`scene.js`) : `small-text`, `small-formula`, `clipped`, `subtitle-band`, `overlap`, `under-canvas`, `text-over-data`, `pen-over-text`. `data-qa="ignore"` exclut un sous-arbre ; `data-qa="over-ok"` admet un texte sur des données ; un halo (`paint-order: stroke` ou `text-shadow`) ou un fond suffit à `text-over-data`.

Liste de vérification d'une scène :

1. `make check` sans erreur ni avertissement de scène, `layout_qa` vide.
2. Chaque mouvement part d'un repère du script ; aucun temps en dur ; chaque repère utilisé est déclaré dans `cues`.
3. Cadre sûr respecté, rien sous y = 880, rien de coupé.
4. Texte ≥ 28 px, aucun chevauchement, symboles dans la bonne casse, virgule décimale et signe moins U+2212 dans les compteurs.
5. Couleurs par rôle (storyboard de l'épisode, section 0) ; jetons seulement.
6. Contraintes physiques de l'épisode vérifiées sur les images fixes aux repères qui les portent (storyboard, section 3).
7. Première image non vide ; `make det` sans verdict DIFFERENT.
8. Images fixes regardées une à une, pas seulement le rapport.
