# Critique (passe personnelle)

## Fidélité (P28) — chaque compte, sens, ordre et lien, vérifié contre facts.md

- Sept étapes, dans l'ordre du tableau de la page Calcul : conforme.
- Grille 4 × 3 : 4 valeurs de Re en colonnes (25, 50, 100, 200), 3 valeurs de Pm en rangées (0,5 ; 1 ; 2, vers le haut) : conforme à palier2_tg3d.yaml, et la même orientation dans les vignettes 1 et 5.
- Découpage : validation (Re = 100, Pm = 1) en colonne 3, rangée 2 ; test (Re = 50, Pm = 2) en colonne 2, rangée du haut : conforme à train_fm3d.yaml.
- ×12 tâches, UUID v5 : conforme (sweep.py).
- Cube : |u| de l'écoulement de Taylor–Green initial, kf = 2, calculé ; 64³ : conforme. Le champ turbulent ultérieur n'est pas dessiné (dit dans la légende).
- Prises du catalogue : table de chaque étape, comme la colonne « Où c'est enregistré » de la page : conforme.
- Fichiers : `fields.h5` (étape 4) et `last.pt` (étape 6) : conforme (storage.py, fm3d.py).
- **Erreur trouvée et corrigée** : le premier rendu tirait une flèche « ingest » du SQLite du cluster vers PostgreSQL. `milady.catalog ingest` lit les fichiers MFF, pas le catalogue SQLite (api.py `ingest_mff`). La flèche part désormais des fichiers copiés (MinIO) vers PostgreSQL, sur la VM. Le même défaut existe dans `docs/ARCHITECTURE.md` (diagramme de déploiement) : signalé pour la revue de cohérence.
- Spectres de la vignette 7 : forme illustrative (aucune évaluation 3D n'a tourné) ; dit dans la légende (P29).

## Grille (style.md § 4)

| Critère | Note | Commentaire |
|---|---|---|
| Lisible à la taille finale | 4 | médiane 5,8 pt à 183 mm (avertissement du contrôle) : figure de référence technique, dense par nature ; même gamme que les autres figures du site |
| Message en 5 s | 5 | une ligne d'étapes, deux rails, trois colonnes |
| Fidèle | 5 | après la correction de l'ingestion |
| Correct | 5 | sens des flèches, ordre, comptes |
| Liens | 4 | grille 4 × 3 reprise en 1, 2 et 5 ; rails et rangées Fichiers / Catalogue de même teinte ; la rangée Exécution n'a pas d'équivalent dessiné en a (les modules en tiennent lieu) |
| Économie | 4 | 0,74 mot/cm² (avertissement) : commandes et ports renvoyés à la légende ; le reste nomme des objets |
| Facture | 4 | alignements vérifiés ; deux polices (Arial et chasse fixe pour le code : convention du domaine, acceptée) |

## Avertissements du contrôle laissés

- Texte petit pour la largeur : assumé (figure de référence, P12 « when not »).
- Deux familles de polices : chasse fixe réservée aux identifiants de code (convention des figures d'informatique, lib-cs.md).
- Densité de mots : idem, après retrait des commandes et des ports.
