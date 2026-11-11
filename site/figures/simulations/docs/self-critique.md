# Critique (passe personnelle)

## Fidélité (P28)
- E1 : 11 Γ d'entraînement (0,80 à 1,00 par 0,02), 10 de test (0,81 à 0,99) ; courbe = 41 valeurs de la grille fine ; seuil entre 0,86 et 0,865 : conforme au JSON.
- E2 : 6 η d'entraînement, 5 de test, sur une échelle logarithmique : conforme à e2_donnees.py. La courbe E_B(η) est recalculée (même solveur, mêmes réglages, autres graines) : dit dans la légende ; ce n'est pas une donnée de E2.
- E3 : 24 valeurs de Rm, seuils 8,87 / 17,6 / 26,8, fenêtres λ > 0 teintées : conforme. **Erreur corrigée** : le premier rendu marquait les 24 valeurs de Rm comme « entraînement » ; E3 n'entraîne aucun modèle, ces points sont retirés. **Erreur corrigée** : l'échelle de λ, écrasée par λ(2) = −0,50, cachait les fenêtres ; axe restreint à ±0,012, trois points hors échelle signalés.
- Correspondances avec l'infrastructure : E2 → palier1_mhd2d (même solveur, `mhd2d_numpy`), E3 → palier2_abc3d (même écoulement, autre solveur et autre résolution) ; E1 sans campagne : conforme.

## Grille
| Critère | Note | Commentaire |
|---|---|---|
| Lisible | 4 | |
| Message en 5 s | 5 | trois rangées sur un gabarit |
| Fidèle | 5 | après corrections |
| Correct | 5 | |
| Liens | 5 | vignettes identiques à plan-these ; couleurs : vert = paramètre, vermillon = grandeur magnétique |
| Économie | 4 | axes verticaux sans graduations (ordres de grandeur dans la légende) |
| Facture | 4 | |
