# Brief — figure « simulations »

- **Mode** : design. **Format** : journal, 183 mm (page Expériences, avant « E1 — Gissinger » ; rappelée dans le rapport, section des expériences).
- **Lecteur** : les encadrants ; un lecteur qui veut savoir ce qui a été simulé, comment, à quelles valeurs, et ce qui est repris par l'infrastructure.
- **Phrase à retenir** : les trois bancs du stage simulent des systèmes de complexité croissante (trois modes, MHD 2D, induction 3D) à des valeurs de paramètre choisies de part et d'autre de leurs transitions, et deux d'entre eux sont repris tels quels par les campagnes de l'infrastructure.

## Idées clés
1. Un même gabarit pour les trois expériences (P3) : système, schéma numérique, balayage du paramètre avec la réponse du système, données gardées, place dans la chaîne.
2. Les valeurs d'entraînement et de test encadrent les transitions : seuil des renversements de E1 (entre Γ = 0,86 et 0,865), fenêtres de dynamo de E3 (seuils 8,87 ; 17,6 ; 26,8).
3. E2 et E3 sont repris par `palier1_mhd2d` (même solveur 2D) et `palier2_abc3d` (même physique, solveur 3D, 64³) ; E1 reste un script autonome.

## Ne doit pas laisser croire
- que la courbe E_B(η) vient des données de E2 : elle est recalculée avec le même solveur et les mêmes réglages (dit dans la légende) ;
- que E1 passe par le catalogue ou les fichiers MFF ;
- que les campagnes ont tourné à leur taille réelle.

## Style
Celui de plan-these : mêmes vignettes (mêmes données), même vert pour le paramètre de contrôle, vermillon pour les grandeurs magnétiques (D, E_B, λ), points pleins = entraînement, points vides = test.
