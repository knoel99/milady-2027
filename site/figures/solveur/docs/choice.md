# Choix entre les deux brouillons

Rendus : `figure/out/solveur_a.png` (pas en tête) et `figure/out/solveur_b.png` (zoom depuis la frise).

## A — pas en tête
- région Fourier surchargée : l'étiquette « RK4 de Lawson » recouvre la forme de l'état, le glyphe de Leray chevauche la courbe du facteur intégrant ;
- région physique à moitié vide (déséquilibre gauche-droite) ;
- les deux équations se touchent ;
- panneau c : tables qui sortent du cadre, traits de correspondance qui se croisent ;
- panneau b : légende coupée en bas.

## B — zoom depuis la frise
- la frise, en tête et très large, prend la place du mécanisme ;
- le coin de zoom part d'un point de l'axe et traverse le panneau c : lien faible ;
- la boucle du pas, comprimée sur 118 mm, accumule davantage de chevauchements ;
- légende de la frise et équations superposées.

## Choix
**A**. Ses défauts sont de mise en page (positions, ordre des tables) et se corrigent sans changer la structure ; B sacrifie le héros (le pas) à la frise. Le brouillon B est gardé tel quel (`figure_b.js`, sur `draw_v0.js`).
