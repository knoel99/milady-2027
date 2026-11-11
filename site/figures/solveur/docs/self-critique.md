# Critique (passe personnelle)

## Fidélité (P28)
- Ordre d'un second membre : rotationnels en Fourier, `irfftn`, produits `u × ω + j × B` et `u × B`, `rfftn`, masque 2/3, puis projection de Leray (quantité de mouvement) ou rotationnel (induction) : conforme à `_rhs` (mhd3d.py l. 487-505).
- Le forçage constant f̂ est ajouté **après** la projection : conforme (l. 500-501).
- B n'est pas projeté à chaque évaluation : son second membre est un rotationnel ; la projection de û et B̂ est un nettoyage tous les `project_every` pas (« projection périodique ») : conforme (l. 547-552).
- RK4 de Lawson, quatre évaluations, facteurs e^{−νk²Δt} et e^{−ηk²Δt} : conforme (`step`, `_factors`).
- Coupure 2/3 : |m| ≤ 21 à 64³ ; le glyphe est une image à 11 points par direction (7 gardés), pas une grille à l'échelle : dit dans la légende.
- Frise : diagnostics depuis t = 0, champs sur ]100, 140] (40), points de contrôle par période de calcul : conforme ; position de l'interruption = exemple (dit dans la légende).
- Correspondances fichier → catalogue : `milady_uuid` → `simulation.id`, `milady_parameters` → `simulation.parameters`, `milady_git_commit` → `simulation.git_commit`, `milady_diagnostics/` → `diagnostic`, fichier → `file` : conforme (api.py `ingest_mff`, run.py étape 5).
- Erreur corrigée en cours de route : l'étiquette « ω̂, ĵ » (chapeau mal placé par la police) a été retirée ; ω et j sont nommés côté physique.

## Grille
| Critère | Note | Commentaire |
|---|---|---|
| Lisible | 4 | médiane 5,5 pt (figure de référence, dense) |
| Message en 5 s | 4 | la boucle se lit ; la double région Fourier / physique porte l'idée |
| Fidèle | 5 | |
| Correct | 5 | |
| Liens | 4 | b et c ne sont reliés que par la légende (la simulation « done » écrit le fichier) |
| Économie | 4 | 0,58 mot/cm² |
| Facture | 4 | glyphe de Leray petit |

Avertissements laissés : texte petit (référence technique), deux polices (code en chasse fixe), libellés de légende jugés longs (« point de contrôle (toutes les 900 s de calcul) », « SIGTERM : … ») : ce sont des entrées de légende, gardées pour ne pas surcharger la légende écrite.
