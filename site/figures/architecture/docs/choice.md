# Choix entre les deux brouillons

Rendus comparés à la taille d'impression : `figure/out/architecture_a.png` et `figure/out/architecture_b.png`.

## Brouillon A (chaîne, deux rails, trois cibles)

Ce qu'un directeur artistique relèverait :
- soulignés interprétés comme indices (`t1_fields`, `milady_*`, `bootstrap_vm.sh`) ;
- étiquettes `u` et `B` collées au bord du cube, sans flèche ;
- « Pm » chevauche le premier point de la grille ; « ×12 » chevauche la dernière carte ;
- lignes de rappel de la vignette 5 qui traversent des points ;
- flèches tiretées du panneau b qui barrent « $SCRATCH » et « SQLite sur $WORK » ;
- spectres « référence » et « généré » presque confondus ;
- bande vide entre le titre du panneau a et les en-têtes d'étapes ; zone vide à gauche des colonnes du panneau b au-dessus de « Exécution ».

Tous ces défauts sont locaux et se corrigent sans changer la structure.

## Brouillon B (couloirs)

- grandes zones vides (couloir du portable presque vide, moitié gauche du couloir VM) ;
- ordre des étapes en zigzag (1 en haut, 2–4 en bas, 5–7 au milieu) : la lecture gauche-droite ne suit plus la causalité ;
- connecteurs qui traversent les vignettes (grille, réseau, spectre) ;
- impose un scénario de déploiement (simulation sur cluster, entraînement sur VM), contraire aux contraintes négatives du brief ;
- les deux magasins (catalogue / fichiers) ne se lisent plus comme des rôles.

## Choix

**A** : moins de problèmes, tous locaux, et c'est le seul brouillon qui porte les deux moitiés de la phrase à retenir sans laisser croire à un ordre entre les cibles. Copié vers `figure/figure.js` (français) et `figure/figure-en.js` (anglais), sur la même source `draw.js`.
