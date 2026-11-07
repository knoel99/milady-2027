# Spec — figure « solveur »

## Structure
Une boucle (le pas de temps, P11) puis deux panneaux d'appui : la vie d'une simulation sur un axe de temps littéral (P8) et la correspondance entre le fichier écrit et le catalogue (P2 : la même information sous deux formes, reliée trait pour trait).

## Concepts
| Concept | Esquisse | 5 s | Fidèle | État dessiné (P1) | Liens (P2, P9) | Choix |
|---|---|---|---|---|---|---|
| **A. Pas en tête** | a : boucle Fourier ↔ espace physique sur toute la largeur ; b (bas gauche) : frise d'une simulation ; c (bas droite) : fichier ↔ catalogue | oui : la boucle est le héros, aérée | oui | oui : plan de modes avec la coupure 2/3, tranche de champ, décomposition de Leray | b et c reliés par « done → écrit » | brouillon 1 |
| **B. Zoom** | a : frise pleine largeur ; coin de zoom d'un pas vers b (la boucle, bas gauche) ; c (bas droite, étroit) : fichier au-dessus du catalogue | moyen : on lit la frise avant le mécanisme | oui | oui | zoom explicite (P9) | brouillon 2 |
| C. Tableau d'opérations | liste numérotée des opérations d'un pas, sans boucle | faible | oui | non | non | écarté |

## Carte (concept A)
**Takeaway (one sentence):** voir brief.md.
**Size:** 183 × ≈ 112 mm.
**Hero:** none, boucle de calcul dessinée à plat (P25 : logique et données à plat) ; glyphes d'état calculés (tranche de |u| de Taylor–Green, analytique ; facteur intégrant, analytique).

### Panneaux
| Panel | Job | Position |
|---|---|---|
| a | un pas : ce qui se fait en Fourier, ce qui se fait en espace physique, la boucle RK4 | haut, pleine largeur |
| b | une simulation dans le temps : diagnostics, champs gardés, points de contrôle, reprise, statuts | bas gauche |
| c | ce qui est écrit : arbre du fichier MFF ↔ lignes du catalogue | bas droite |

### Composants principaux
| Panel | Composant | Libellé | Aspect | Source |
|---|---|---|---|---|
| a | deux régions | « Espace de Fourier », « Espace physique » | fond gris bleuté pâle / blanc, séparés par une ligne tiretée | draw |
| a | état | « û, B̂ » | deux plans de modes 11 × 11 (bleu, vermillon), modes hors du cube 2/3 en gris pâle | draw (structure : coupure |m| ≤ 21 à 64³, montrée à l'échelle 11 points) |
| a | rotationnel | « ik× » → « ω̂, ĵ » | pastille | draw |
| a | passage | « irfftn » (haut, →), « rfftn » (bas, ←) | flèches qui franchissent la séparation | draw |
| a | champs physiques | « u, B, ω, j » | tranche carrée (|u| de Taylor–Green, gris) | compute |
| a | produits | « u × ω + j × B », « u × B » | boîte, symboles colorés | draw |
| a | désaliasage | « désaliasage 2/3 » | plan de modes avec les modes coupés en anneaux vides | draw |
| a | Leray | « P = I − kkᵀ/|k|² » | k (gris), vecteur projeté (bleu), part retirée (tiretée) | draw |
| a | induction | « ik × (u × B) » | pastille | draw |
| a | RK4 | « RK4 de Lawson · ×4 » | grande flèche de retour vers l'état | draw |
| a | facteur intégrant | « e^{−νk²Δt}, e^{−ηk²Δt} » | petite courbe décroissante en k | compute (forme analytique) |
| b | axe | « t », « 0 », « 100 », « 140 » | axe littéral | draw (palier2_tg3d) |
| b | diagnostics | « diagnostics tous les 0,1 » | peigne fin sur tout l'axe | draw |
| b | champs gardés | « 40 instantanés » | 40 traits sur ]100, 140] | draw |
| b | interruption | « SIGTERM », « point de contrôle », « reprise » | coupure de la barre, éclair, losanges | draw (exemple, dit dans la légende) |
| b | statuts | « queued », « running », « done » | pastilles | draw |
| c | arbre MFF | voir facts.md | arbre en chasse fixe ; accolades « The Well » et « MilaDy » | draw |
| c | tables | `simulation`, `file`, `diagnostic`, `job` | cartes de tables (gris bleuté du catalogue) | draw |
| c | correspondances | — | traits fins de l'attribut à la colonne | draw |

### Relations
| From | To | Kind | Drawn as |
|---|---|---|---|
| état | ik× → irfftn → champs physiques | flux | flèches |
| champs | produits → rfftn → désaliasage → Leray / ik× | flux | flèches |
| seconds membres | état | RK4 (boucle) | flèche de retour épaisse, distincte |
| simulation (b, done) | fichier (c) | écrit | flèche |
| attributs du fichier | colonnes du catalogue | correspondance | traits |

### Conventions
- u et ses dérivés en bleu, B et ses dérivés en vermillon ; opérations en gris.
- Fourier à gauche (fond gris bleuté), espace physique à droite (fond blanc).

### Contraintes négatives
- Pas de projection de B à chaque étage (seulement un nettoyage périodique).
- Pas de positions chiffrées des points de contrôle sur l'axe simulé.
- Pas de temps de calcul GPU.
