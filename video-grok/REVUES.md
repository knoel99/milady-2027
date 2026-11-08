# Relectures adverses du plan

Statut au 2026-11-08, après lecture des rapports et un correctif : **G0 non close**. Les rapports indépendants sont sur d’autres branches. Ils n’ont pas été modifiés. `G0-CORRECTIONS.md` répond à S18–S25 et aux six réserves pédagogiques. Une nouvelle revue indépendante doit relire le commit de correctif. Cette note n’est pas une approbation.

Les deux relecteurs travaillent sans se lire l’un l’autre, sans ouvrir `video/`, sans modifier `PLAN.md`. Chacun écrit un fichier neuf :

- `video-grok/revues/SCIENCE.md`
- `video-grok/revues/PEDAGOGIE.md`

Branche suggérée : `grok/video-revue-science` et `grok/video-revue-pedagogie`, à fusionner plus tard dans `grok/video` ou, à défaut, dans `grok/video-plan` par pull request non mergée vers `main`.

Un défaut est **bloquant** s’il mettrait un chiffre faux, une surenchère, ou une falaise pédagogique à l’écran. Les bloquants doivent être corrigés dans le plan avant toute narration.

## Revue science — périmètre exact

Relire seulement, contre le commit `4e42429716c093df34ba05b47ada542a13d39c50` :

1. `INVENTAIRE.md` en entier.
2. `INCERTITUDES.md` en entier.
3. `MANQUES.md` en entier.
4. Dans `PLAN.md`, chaque cellule « Sources » et chaque pastille.
5. `QUESTIONS.md`, colonne « À lire » et les défauts.
6. `STYLE.md` §6 (symbole qui changerait un énoncé).

Ne pas relire le style graphique, les durées, ni Fish, sauf si un choix visuel contredit une pastille.

### Vérifications obligatoires

- Chaque nombre du plan qui n’est pas dans `INVENTAIRE.md` est un bloquant.
- Chaque nombre de l’inventaire est rouvert à la ligne citée. Si la ligne ne dit pas ce nombre, bloquant.
- Tables E1 test : `experiences/resultats/digest.md:11-26` contre `en/rapport/index.qmd:834-853`. Distinguer σ absolu et σ/σ_ref.
- 14 %, 65 %, 42 % : `en/rapport/index.qmd:883` et les cellules `digest.md:94-103`. Le 65 % ne doit pas être « au seuil ».
- ×9 : 0,0231 / 0,00257. ×3,6 : 2,52 / 0,699 contre le **témoin**, pas contre V0.
- Seuils JSON `e3_abc.json:167-171` et l’incertitude de signe à Rm = 17,5.
- E2 n’est pas une dynamo. E3 n’a pas de générateur. Aucune scène waiting ne dessine un champ 3D généré.
- Rm VKS : pas d’axe unique. ABC : Rm = 1/η contre √3/η.
- Courbes `vks-en.png` : schematic.
- « Aucun modèle génératif de dynamo » daté du 2026-11-06, confiance non haute.
- Scores 4,10 et 3,90 : jugement de l’auteur du site, pas un fait.
- Noms d’encadrants : titres et DOI déjà dans `en/encadrants/index.qmd`, aucune opinion ajoutée par le plan.
- §E : bandes océaniques, dernier renversement, disque, Larmor, Glatzmaier–Roberts. Confirmer qu’aucun nombre n’a fuité dans `PLAN.md`.
- Paris : chaque issue `result-unmet` reste dicible ; aucune issue ne dit « renversements 3D générés ».
- Budget 1,1×10⁴ h avec facteur deux, hypothèses non mesurées sur GPU.
- Le rapport est prospectif et non endossé (`en/index.qmd:43-45`).

### Hors périmètre science

Ne pas réécrire les métaphores. Ne pas proposer un autre découpage, sauf si l’ordre actuel force une affirmation fausse (alors bloquant, avec la ligne). Ne pas lancer de calcul. Ne pas ouvrir `video/`.

### Forme du rapport

Tableau : `fichier:ligne du plan` | affirmation | `fichier:ligne source` | verdict `ok` / `bloquant` / `réserve`. Puis une liste des bloquants, vide s’il n’y en a pas. Pas de correctif appliqué.

## Revue pédagogie — périmètre exact

Relire :

1. `PLAN.md` en entier, y compris les horloges.
2. `STYLE.md` §4, §8, §11 (motifs, cartes, rythme).
3. `QUESTIONS.md` (longueur des lignes d’écran, une décision par carte).
4. `LOTS.md` section pilote, seulement pour dire si g10 est représentatif.

Ne pas refaire la vérification arithmétique des chiffres, sauf si une durée oblige à empiler deux idées.

### Vérifications obligatoires

- Les 30 premières secondes : `g00` dure 50 s et la bascule est vers 7 s, avec la légende hors échelle. Si la bascule n’est pas dans les 30 premières secondes du **film**, bloquant.
- Une idée par scène. Repérer tout plan qui en contient deux.
- Aucune formule avant le plan qui la motive. Contrôler l’ordre : Rm en g02, équations de Gissinger en g07, Rice en g08, corollaire 6 en g10.
- Pas de falaise : le saut L2 → L3 est g07–g08, avec g06 juste avant. Le saut L3 → L4 est préparé par g10 avant g11–g12.
- Récapitulatif L0–L2 présent (g06). Le retour au niveau public en g15 ne réintroduit pas de symbole nouveau.
- Les deux unités d’état de l’art sont dans le **cœur** : g04 = 2:30 après g03 ; g12 = 4:00 après g11. g12 est dans la fourchette 4–5 min. g04 est à 2:30 comme demandé (~2,5 min).
- Cœur autonome : pour chaque couture x01, x02, x03, x04, x05, la scène cœur suivante se comprend sans le module. Tester mentalement le montage qui saute les x.
- Durées : somme cœur 41:00, somme étendu 60:00, g14 entre 2 et 3 min. Chaque chapitre a une carte 6–10 s **incluse**. Les pauses predict sont nommées et incluses.
- Budget de mots 125–130 / min compatible avec la durée (pas un texte à écrire : juger si la liste d’idées tient dans le budget, en comptant environ 127 mots par minute). Une scène dont l’idée demande visiblement le double est un bloquant de durée.
- Cartes ≤ 18 mots anglais, une décision, un défaut. `q.g07` a 11 mots : le recompter.
- Predict avant les pourcentages de Rice, avant la barre écrasée, avant la formule de Rm.
- Visuels anglais, voix EN et FR, mêmes `cue.*`.
- g00 et g15 se répondent. Le générique ne prête pas d’opinion.
- Le pilote g10 contient bien une pastille, une formule, une mesure, une question et un piège (E2 n’est pas une dynamo).

### Hors périmètre pédagogie

Ne pas « améliorer » le style pour le plaisir. Ne pas écrire les phrases dites. Ne pas déplacer un chapitre sans montrer la falaise que l’ordre actuel crée.

### Forme du rapport

Pour chaque chapitre : `tient` ou `bloquant`, avec le repère `cue` concerné. Puis : accroche des 30 s, falaise, autonomie du cœur, réalisme des durées. Liste des bloquants.

## Après les deux rapports

L’auteur du plan corrige uniquement les bloquants, dans `grok/video-plan`, sans absorber les suggestions hors périmètre. Une troisième passe n’est requise que si un correctif change un chiffre ou l’ordre des niveaux. Ensuite seulement, G0 est close et `LOTS.md` autorise les fondations et les scripts.
