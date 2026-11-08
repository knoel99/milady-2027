# Guide visuel

Indépendant des autres productions. Les couleurs sémantiques sont celles déjà gravées dans les figures du site, pour que le film et le site parlent le même code. La mise en page, la typographie d’écran, les pastilles et le rythme ne recopient aucune scène existante : aucune n’a été lue.

Visuels **anglais** dans les deux versions linguistiques. La narration française ne traduit pas les étiquettes.

## 1. Trois matières

Environ 75 % du temps est sombre. Le reste se partage entre deux matières claires, jamais mélangées dans le même plan.

| Matière | Quand | Fond | Encre |
|---|---|---|---|
| Nuit | récit, expériences, champs, boussole | `#0b0f14` (`assets/paper.css:80`) | `#f5f7fa` (`paper.css:81`) |
| Papier | démonstrations L4–L5, module `x01` | `#ffffff` avec la marge chaude `#f6f4ef` | `#2b2b2b` (`figures/cadre/figure/parts.js:6`) |
| Plan d’architecte | infrastructure, campagnes, budget | `#121821` (`paper.css:93`) avec un quadrillage 32 px, trait `#6b7a8c` à 40 % | `#f5f7fa` |

Le passage d’une matière à l’autre est un fondu de 8 images (environ un quart de seconde à 30 images/s), pas un nouveau sujet.

## 2. Couleurs sémantiques

Une teinte par entité, reprise de `figures/cadre/figure/parts.js:4-5` et de `figures/vks/figure/parts.js:5`.

| Rôle | Hex | Usage |
|---|---|---|
| Paramètre de contrôle (Γ, η, Rm, Re, Pm) | `#009E73` | axes, curseurs, ticks d’entraînement |
| Vitesse u | `#0072B2` | flèches, spectres cinétiques |
| Champ magnétique B | `#D55E00` | lignes de champ, spectres magnétiques, aiguille aimantée |
| Modèle génératif (latent, flot, réseau) | `#6C4BA0` | trajectoires de flow matching, variantes du modèle |
| Mesures sur les lois (distances, résidus, Rice) | `#C98A00` | barres de métrique, pastille d’erreur |
| Infrastructure | `#8d949c` (`parts.js:6`, `metal`) | boîtes, fichiers, GPU |
| Renversement (événement, pas le champ) | `#5E3C99` | trait de passage dans une série temporelle |

Règle ajoutée par ce guide, parce que les figures VKS utilisent `#009E73` à la fois pour une excursion et pour le paramètre (`figures/vks/figure/parts.js:5`) : dans le film, le vert est **seulement** le paramètre. Une excursion est un trait `#5E3C99` en pointillés. On ne réutilise pas le vert « exc ».

Interdit : un dégradé arc-en-ciel sur un champ, une couleur par variante qui contredirait le rôle (V5 reste violet, pas vert, même si elle « gagne »). Le succès n’a pas de couleur. Il a une pastille MEASURED et une barre plus courte vers le plancher.

Texte secondaire sombre : `#c7d0da` (`paper.css:83`). Filet : `#6b7a8c`. Focus : `#fdba74` seulement pour le curseur « vous êtes ici », jamais pour B.

## 3. Cadre

- 1920×1080, 30 images/s, plus tard H.264, BT.709, CRF selon la scène, image clé toutes les 2 s. Chaque MP4 < 1,9 Go. Deux pistes audio. Ceci décrit la cible ; rien n’est rendu.
- Marge de sécurité : 80 px. Aucun texte dans cette marge, y compris les pastilles.
- Corps de texte à l’écran ≥ 28 px. Titres de chapitre : Inter Display, 64 px, graisse 560. Étiquettes : Inter, 32 px. Nombres : JetBrains Mono, 32 px, chiffres tabulaires. Une ligne d’écran ≤ 42 caractères quand elle sert aussi de sous-titre ; les formules ne sont pas dans cette ligne.
- Un plan, une idée. Si deux courbes demandent deux lectures, ce sont deux plans.
- Pas de photo, pas de logo, pas de portrait. Noms des encadrants en texte, générique final et bandeau de sources.

## 4. Motifs qui reviennent

Ils sont introduits à L0–L2 et payés à L3–L5. Les nommer dans les repères, pas les caler sur une seconde absolue.

| Motif | Première fois | Ce qu’il paie |
|---|---|---|
| Aiguille | `g00` bascule vers le sud vers 7 s, légende « illustration, not to time scale » | `g15` la même aiguille, après les questions |
| Deux taches symétriques | polarités, dès `g01`, sans axe | loi de (Q, D), équivariance, corollaire sur les poids |
| Trait vert sur un axe | le paramètre, `g02` | Γ, η, Rm, et les ticks pleins (entraînement) / ouverts (test) |
| Plancher en pointillés ambre | première métrique, `g07` | toute barre se lit contre lui, jamais contre zéro |
| Carte question | fin de chaque chapitre | `g14` les reclasse en A, B, C |
| Bandeau de niveau | coin supérieur droit, `L0` … `L5` | change aux récapitulatifs, pas au milieu d’une idée |

Ticks : disque plein = valeur vue à l’entraînement, cercle ouvert = valeur de test, d’après la légende de `figures/simulations` (`en/experiences/index.qmd:46`).

## 5. Pastilles d’honnêteté

Haut gauche, pilule 28 px de haut, encre `#0b0f14` sur le fond du rôle :

| Pastille | Fond | S’emploie quand |
|---|---|---|
| MEASURED | `#C98A00` | chiffre tiré de E1, E2 ou E3 |
| PROVED | `#f5f7fa` | énoncé démontré dans le rapport |
| CONJECTURE | `#6C4BA0` | confiance écrite à côté : high, medium, low |
| PLANNED | `#8d949c` | palier, campagne, critère non mesuré |
| CONTEXT | `#009E73` | fait externe dont la source est à l’écran (auteur, année) |

Une scène qui porte une affirmation a exactement une pastille principale. Une comparaison « E3 contre Archontis 2003 » a MEASURED sur la courbe et CONTEXT sur la fenêtre publiée, en deux objets, pas une pastille mixte.

## 6. Formules

Calque séparé, au-dessus de l’image, jamais dans les sous-titres, jamais lu par la voix. KaTeX, local, un terme à la fois : le terme dont parle le repère nommé s’allume en la couleur de son rôle, les autres restent à 40 % d’opacité. Corps 36 px. Pas plus d’une formule visible. Les sous-titres occupent une bande basse de 140 px, fond `#0b0f14` à 72 % d’opacité, et ne montent pas dans le calque formule.

Symboles figés (feuille à respecter plus tard, pas une narration) :

| Symbole | Sens dans ce film | Ne pas confondre avec |
|---|---|---|
| u | vitesse du fluide | v_θ, vitesse du flot génératif |
| B | champ magnétique | |
| t dans une intégrale physique | temps | t ∈ [0, 1] du flow matching, toujours étiqueté « flow time » |
| Γ | forçage de Gissinger dans E1 | pas le paramètre générique λ |
| λ | taux de croissance magnétique en E3, ou paramètre générique seulement quand l’étiquette dit « parameter λ » | pas le multiplicateur d’inclinaison |
| η | diffusivité magnétique | pas une viscosité |
| Rm, Re, Pm | toujours avec la définition dans le plan où le nombre apparaît | |
| Q, D, V | modes de Gissinger 2012, μ sur Q | l’article de 2010 échange D et Q |
| D dans E2 | dissipation, seulement dans σ(D) | le dipôle D. Écrire « dissipation » en toutes lettres à l’écran dès que les deux cohabitent dans le film |

## 7. Graphiques

- Fond de graphe : nuit. Axe en `#6b7a8c`. Grille seulement si elle porte une lecture.
- Barres horizontales pour les variantes, ordre stable : A B C, puis F F0, puis D E ; en E2 : V0 V1 V2 V3 V4 V5 témoin, puis le sous-échantillon en gris. Ne pas trier par « gagnant ».
- Échelle logarithmique annoncée dans le titre du panneau quand le digest l’est (divergences).
- Le plancher est une ligne verticale pointillée ambre, légendée « noise floor », avec n écrit.
- Erreurs : ne pas dessiner un point sans son intervalle quand le rapport dit qu’il n’y en a pas. À la place, la légende « one seed » ou « two seeds ».
- Séries temporelles qualitatives (forme normale, schéma VKS) : filigrane « schematic, not a measurement ».

## 8. Cartes de chapitre et questions

Carte de chapitre, 4 s maximum dans la durée du chapitre : numéro, titre anglais, niveau, une ligne « this chapter asks ». Pas de sommaire animé de toutes les parties.

Carte question, 6 à 10 s, fin de chapitre. Dans ce plan elle dure 0:08. Le créneau `*.close` est une synthèse parlée. Il ne garde pas la carte à l’écran. Fond nuit, une phrase anglaise ≤ 18 mots, classe A / B / C en petit, pastille PLANNED ou CONTEXT selon le cas. La voix dit une phrase. Le texte à l’écran n’est pas un paragraphe. Le module `g14` reprend les mêmes phrases, regroupées, sans les réécrire.

## 9. Série « en attente »

Un emplacement de résultat futur est un rectangle en plan d’architecte, titre de la campagne, critère copié du plan de thèse, confiance, et la mention « not yet run ». Pas de courbe en pointillés qui ressemblerait à une mesure. Quand le JSON arrivera, le rectangle est remplacé par le graphe MEASURED et la pastille change. L’empreinte du JSON décide du re-rendu.

## 10. Son (cible, non produite)

- Musique originale synthétisée par le code sous L0–L2. Silence musical en L4–L5. Bruitages synthétiques (aiguille, tops de passage de seuil), jamais une banque qui imite un laboratoire réel.
- Cible : −16 LUFS intégré, crête vraie ≤ −1 dBTP.
- Piste 1 : voix + musique + effets. Piste 2 : musique + effets.
- La voix n’est pas un personnage réel. Voir `FISH.md`.

## 11. Rythme

125 à 130 mots effectifs par minute. Repère du brief : la voix Ethan lit environ 146 mots/min une fois les pauses longues comptées. Les pauses « predict » (2 à 3 s) et les cartes question (6 à 10 s) sont **dans** la durée du plan, pas en plus. Les animations se calent sur des repères nommés `cue.<scene>.<beat>`, jamais sur une constante de temps.

Beats réservés : `start`, `predict`, `show`, `formula`, `caveat`, `card`.

## 12. Ce que le style refuse

- Un décompte de « succès » en vert.
- Une aiguille qui prétend être à l’échelle des temps géologiques ou de VKS.
- Une formule lue, ou un sous-titre qui contient un symbole TeX.
- Le mot « we obtained » sur une campagne non lancée.
- Deux niveaux d’apprentissage dans le même plan.
