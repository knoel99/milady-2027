# Épisode 01 : avis et arbitrages

Ordre d'arbitrage (CLAUDE.md) : exactitude, compréhension, rythme, style. Le détail de chaque correction est dans `traitement.md`, section 8.

## Traitement

| Avis | Source | Arbitrage |
|---|---|---|
| Cercle « promené » : flèches qui ne traversent pas seulement si le cercle est centré | physicien | retenu (exactitude) |
| Divergence coulombienne nulle hors de la charge, source concentrée au point | physicien | retenu |
| Cercles de `fig-monopole-dipole.png` = sphères en coupe, pas de compteur 2D | physicien | retenu |
| Dipôle ponctuel de la figure : lignes qui semblent converger | physicien | retenu : petit aimant étendu dessiné |
| « somme des divergences × aire », sens trigonométrique, tourbillon défini (1/r), quart de tour horaire, Green–Riemann | physicien | retenus |
| La contrainte garantit la divergence, pas le réalisme | ml | retenu, sans chiffre |
| FunDiff : vitesse d'un fluide, pas champ magnétique | ml | retenu ; nom en légende seulement (cf. apprenant) |
| B = ∇^⊥a pour refermer la question de départ | ml | retenu |
| « projeter, à la fin ou à chaque pas » | ml | écarté au profit de l'apprenant : une phrase concrète, sans mécanismes de génération |
| Citer les divergences d'E2 (1,78e-17) | ml | écarté : aucun chiffre d'expérience dans la voix d'un épisode de L1 |
| Flux non défini, formule de la divergence sans intuition, ω/2 sans raison, sens du cisaillement | apprenant | retenus (compréhension) |
| Saut 2D → 3D, 4π inexpliqué, « dipôle » non défini | apprenant | retenus ; 4π expliqué par 1/R² × 4πR² |
| FunDiff, E2, « projeter » hors profil | apprenant | retenus |
| Idée 3 trop dense | apprenant | retenu : 3 min 30, total 14 min |
| Stabilisation du rapport sur l'écoulement cellulaire (mon arbitrage) | scénariste | corrigé par le scénariste : ce champ a un flux nul ; stabilisation montrée sur la circulation (idée 2), énigme à l'idée 1 résolue à l'idée 4 |

## Narration

Mesure après correction : 165 phrases, 2 189 mots (comptage du moteur), 14 min 36 s à 150 mots/min ; 0 phrase identique à une phrase du module ; 5 phrases (3 %) partagent un segment de six mots avec lui, toutes des tournures courantes (« dans le sens des aiguilles d'une montre », « nacelle de grande roue », « concentrée au point »).

| Avis | Source | Arbitrage |
|---|---|---|
| Une ligne seule ne porte pas de flux ; carte plane sans surface fermée ; aubes « sur la ligne du milieu » ; champ traversant la sphère « bien en face » | physicien | retenus (exactitude) |
| Monopôle « gerbe de lignes », limite du carrelage, « un petit aimant est un dipôle » | physicien | retenus, bible mise à jour |
| Légende FunDiff avec la revue, « écoulements bien plus agités », « physiquement crédibles » | ml | retenus |
| Flux par côté × longueur puis ÷ aire ; cercle déplacé ; raison de l'incompressibilité ; formules à l'écran ; tourbillon en 1/r, vitesse infinie au centre ; formule de l'écoulement cellulaire à l'écran ; nabla point B nommé | apprenant | retenus (compréhension), compensés par des coupes dans P2, la clôture et la liste d'exercices dite |
| Gradient hors du niveau de départ | apprenant | non retenu : la carte de randonnée suffit, et le gradient figure dans les acquis de L1 visés par le module |
| L'apprenant a ouvert `continuite.md` malgré la consigne | — | ses décrochages restent valables (relevés sur la narration seule) ; noté pour le bilan |

## Storyboard

Les deux relecteurs ont vérifié que les images ne disent rien de faux. Tous leurs points sont retenus (détail : `storyboard.md`, « Journal des corrections », points 1 à 27).

- relecteur-physicien : 2 erreurs (déplacement de 100 px qui ne fait entrer aucune part ; Ω_roue affiché +½ au lieu de −½), 7 imprécisions (coupe plane de la sphère déplacée qui contredit le 0, dérivée partielle montrée sur un cas nul, Stokes illustré sur 0 = 0, « 1 tour » contre « 2 », plafond de longueur des flèches, ligne de niveau de Q non tracée, « sommet à gauche » faux dans les cellules ψ < 0), 11 suggestions.
- relecteur-ml : 3 points importants sur le plan [c-machines] (badge de scène qui attribuait 52 s de calcul à Wang et al., bandeau sous la mauvaise carte, chip « schéma » ambigu), 4 mineurs.
- Repère [r-pales] renommé [r-aubes] par la session principale (mot proscrit par la bible).
