# Résultats manquants, paris, deux narrations

Aucun de ces calculs n’est lancé par le film. Chaque scène en attente lit plus tard un JSON sous `video-grok/data/waiting/` (fichier absent aujourd’hui). Tant que le fichier n’a pas de clé, de somme SHA-256 de la source, et de statut `met` | `unmet` | `inconclusive`, la scène joue le créneau `narr.<id>.bet` et montre la prédiction, le critère et la question. Elle ne dessine pas un graphique fictif.

Les créneaux `narr.<id>.result-met`, `.result-unmet`, `.result-inconclusive` sont des **identifiants**. Cette phase ne rédige pas les phrases. Contrainte commune : le créneau « met » ne peut dire que le critère nommé ; le créneau « unmet » ne peut pas transformer l’échec en succès partiel sans le dire ; « inconclusive » dit ce qui manque (graine, résolution, clé absente, signe du taux non résolu).

Chemins de lecture prévus (les nôtres, pas ceux d’une autre production) :

| Scène | Fichier lu | Clés |
|---|---|---|
| `g13.mhd2d-campaign` | `waiting/palier1.json` | séries d’énergie, dissipation, injection par η, issues des diagnostics MFF |
| `g13.abc64` | `waiting/abc64.json` | paires (Rm, λ), divergence, comparaison aux seuils E3 |
| `g13.tg` | `waiting/tg.json` | E_B(t) par (Re, Pm), λ réajusté sur la croissance, pas un taux de saturation pris pour un taux de dynamo |
| `g13.fm3d` | `waiting/fm3d.json` | `div_rel_u`, `div_rel_b`, `err_spectre_*_log10`, `dist_energie`, `plancher_dist_energie` au point test (Re = 50, Pm = 2) |
| `g13.stat3d` | `waiting/fm3d-stat.json` et `waiting/fm3d-control.json` | `residu_bilan_total`, `dist_energie`, et σ(dissipation)/σ_ref si la métrique a été ajoutée |
| `g13.abc-gen` | `waiting/abc-gen.json` | erreurs par Rm, en particulier près de 8,87, 17,6 et 26,8 |
| `g14.bill` | `waiting/bench.json` | secondes par pas, mémoire, heures. Pas de prix inventé |
| `x04.vks` | `waiting/vks.json` | seulement si les partenaires ont transmis des fichiers et autorisé la publication |
| `x05.dresdyn` | `waiting/dresdyn.json` | idem |

Régénération prévue (plus tard, pas dans cette phase) : un convertisseur MFF HDF5 et un convertisseur du JSON de `milady.eval.metrics` (`compare_ensembles`, `milady/eval/metrics.py:588-657`) écrivent ces fichiers en copiant la source et son SHA-256. Une commande ne re-rend que les scènes dont l’empreinte a changé, et seulement le créneau de narration « résultat ». Épisode « Results update » : même montage, créneaux `result-*` à la place de `bet`.

## Paris

Critères de palier : `en/these/index.qmd:917` pour le 3D périodique, `:903` pour le 2D, `:889` pour le palier 0. Les énoncés visés sont ceux du rapport. Chaque verdict doit pouvoir être atteint, non atteint, ou non concluant.

### P-div — divergence exacte en 3D

- Scène : `g13.fm3d` (aussi un insert dans `g10` qui reste un pari, pas une mesure).
- Prédiction : si le décodeur est un potentiel vecteur en jauge de Coulomb, la divergence relative de u et de B est < 10⁻¹², quels que soient les autres scores.
- Raisonnement : proposition 1 (`en/rapport/index.qmd:326-333`) ; E2 V4 atteint ~10⁻¹⁷ (`digest.md:138`) ; E3 en forme rotationnelle reste ≤ 1,6×10⁻¹⁶ (`en/experiences/index.qmd:105`).
- Confiance : haute **conditionnelle** au décodeur. Si le chiffre échoue, c’est un défaut de code, pas une physique nouvelle (`RECOMMANDATION-CLOUD.md:789`).
- Critère : palier 2 (a), `en/these/index.qmd:917`.
- Question qui décide : quel opérateur discret sert de définition (`QUESTIONS.md`, carte `g10`).
- `result-met` : les deux divergences sous 10⁻¹², rien d’autre.
- `result-unmet` : le décodeur ne fait pas ce qu’il annonce.
- `result-inconclusive` : clé absente ou champ non décodé.

### P-field — qualité au point sans donnée

- Scène : `g13.fm3d`.
- Prédiction : au point test (Re = 50, Pm = 2), l’erreur de log-spectre reste lisible contre son plancher ; on ne promet pas < 0,1 décade, parce que E2, même favorable, reste loin du plancher (`en/rapport/index.qmd:1039`).
- Raisonnement : E2 interpole mieux là où le modèle de base est déjà bon, et la perte aide là où le niveau d’énergie est faux (`en/rapport/index.qmd:1135`). Le YAML n’a que 40 instantanés par point si `n_traj` reste 1 (`palier2_tg3d.yaml:45`, `en/calcul/index.qmd:157`).
- Confiance : faible pour le critère (b) du palier 2 à cette taille d’échantillon. Moyenne pour « on verra un écart au plancher, et il faudra le montrer ».
- Critère affiché : (b) erreur de log-spectre < 0,1 décade par bande jusqu’à k_c/2 **aux paramètres d’entraînement**, plus la distance d’énergie comparée à `plancher_dist_energie` (`en/these/index.qmd:917`, `milady/eval/metrics.py:604`).
- Question : `n_traj` et le nombre d’instantanés avant l’entraînement (`RECOMMANDATION-CLOUD.md:255-258`).
- `result-met` : critère (b) tenu et distance au-dessus du plancher quand même dite.
- `result-unmet` : spectres ou distance hors critère, modèle encore faible, comme E2.
- `result-inconclusive` : moins de 12 simulations, ou point test absent du JSON.

### P-stat — perte de stationnarité en 3D

- Scène : `g13.stat3d`.
- Prédiction : lancée seulement depuis un modèle déjà bon, avec ancrage et montée de β, la perte réduit le résidu de budget par rapport au témoin de même ancrage, sans annuler σ(dissipation). Sans ancrage, le risque est la divergence vue en E1.
- Raisonnement : E2 V5 contre témoin (`digest.md:139-140`) ; E1 F contre F0 et échec sur C court (`en/rapport/index.qmd:875-877`) ; ancrage et warmup présents dans le code, désactivés par défaut (`en/calcul/index.qmd:166`). σ par échantillon n’est pas encore enregistré automatiquement (`en/calcul/index.qmd:166`).
- Confiance : moyenne si l’ancrage est imposé ; faible sinon.
- Critère : résidu réduit contre le témoin, distance d’énergie non dégradée, et — à titre indicatif, critère du palier 1 — σ/σ_ref dans [0,8 ; 1,2] (`en/these/index.qmd:903`, `RECOMMANDATION-CLOUD.md:791`).
- Question : impose-t-on l’ancrage avant le premier réglage fin (`QUESTIONS.md`, `g10`).
- `result-met` : les trois comparaisons, témoin inclus.
- `result-unmet` : divergence du réglage, ou variance écrasée, ou distance dégradée. Ne pas dire « la contrainte a réussi » si seule la moyenne est bonne.
- `result-inconclusive` : pas de témoin à ancrage égal, ou σ non calculé. Dans ce dernier cas la moitié de la question reste ouverte (`RECOMMANDATION-CLOUD.md:791`).

### P-blur — flou au seuil ABC

- Scène : `g13.abc-gen`, préparée par `g11.e3` qui, elle, est MEASURED.
- Prédiction : l’erreur du générateur est plus grande près de 8,87, 17,6 et 26,8 que loin des seuils. λ(Rm) à 64³ reste dans les fenêtres publiées à la précision du taux, pas à la troisième décimale.
- Raisonnement : proposition 9 (`en/rapport/index.qmd:543-557`) ; E1 lisse déjà le seuil de renversement (`en/rapport/index.qmd:883`) ; à Rm = 17,5 le signe n’est pas résolu même pour le solveur (`en/rapport/index.qmd:1114`).
- Confiance : haute pour « le générateur régulier ne suit pas un saut » ; moyenne pour la comparaison 64³ contre 32³, parce que le second seuil est déjà flou à 32³.
- Critère : erreur plus grande près des trois seuils ; λ(Rm) comparé à 8,9 < Rm < 17,5 et Rm ≳ 27 (`RECOMMANDATION-CLOUD.md:793`).
- Réserve : 20 instantanés d’une trajectoire ABC renormalisée sont presque le même mode. La diversité réelle est celle des germes, pas celle des instantanés (`infra/configs/palier2_abc3d.yaml:20-21`).
- `result-met` : le flou est localisé aux seuils, et les fenêtres restent les bonnes à la précision dite.
- `result-unmet` : soit le générateur invente une fenêtre, soit l’erreur n’est pas plus grande au seuil (ce serait une surprise au sens de la prop. 9, à montrer, pas à cacher).
- `result-inconclusive` : signe de λ non stable entre moitié et dernier quart, comme à Rm = 17,5 en E3.

### P-tg — seuil Taylor–Green

- Scène : `g13.tg`.
- Prédiction : une dynamo apparaît et le seuil bouge avec Pm. Repère publié : Rm_c = 30 à Pm = 1 (Ponty et al. 2005, `dynamo.md:581`, rappel `en/these/index.qmd:908`). À 64³ et Re ≥ 100, le résultat est provisoire tant que les spectres ne décroissent pas avant la coupure.
- Raisonnement : le YAML lui-même demande cette vérification (`palier2_tg3d.yaml:12-14`). La convention de forçage du dépôt (kf = 2, amplitude « turbulent ») doit être comparée à celle de l’article avant tout chiffre (`palier2_tg3d.yaml:3-8`).
- Confiance : faible sur la valeur numérique du seuil à 64³ ; moyenne sur « on verra ou non une croissance de l’énergie magnétique ».
- Critère : qualitatif à cette échelle (`RECOMMANDATION-CLOUD.md:794`). Pas le critère (c) du palier 2, qui demande un Pm sans donnée et 10 % — hors de portée de 12 points sous-résolus.
- Question : retirer Re = 200, ou monter en résolution (`RECOMMANDATION-CLOUD.md:253-254`).
- `result-met` : carte dynamo / pas dynamo, étiquetée sous-résolue si le pilote le montre, convention de forçage écrite à l’écran.
- `result-unmet` : pas de croissance là où le repère publié en attend une, **ou** croissance partout parce que le forçage n’est pas celui de l’article. Les deux se disent.
- `result-inconclusive` : spectres non décroissants, ou taux lu dans le catalogue au lieu de la phase exponentielle (`RECOMMANDATION-CLOUD.md:904`).

### P-bill — facture

- Scène : `g14.bill` dans le cœur (ordre de grandeur seulement) et `x05.bill` dans l’étendu.
- Prédiction : le plan de thèse annonce ≈ 1,1×10⁴ h GPU, facteur deux (`en/these/index.qmd:972-973`). Une session de location ne mesure qu’une machine, pas ce total.
- Confiance : haute pour « le chiffre du plan est une hypothèse » ; nulle pour un coût en euros tant que le banc n’existe pas.
- Question : un GPU de laboratoire ou un projet Jean Zay existe-t-il déjà (`RECOMMANDATION-CLOUD.md:25-27`). Si oui, la location n’est qu’un essai.
- `result-met` : secondes par pas et heures mesurées, extrapolées avec la fourchette, pas un seul nombre.
- `result-unmet` : le pas est hors de la fourchette utilisée pour décider. Le film dit que le budget est à refaire, il ne le « corrige » pas en silence.
- `result-inconclusive` : pas de GPU dans le JSON. Le créneau reste le pari.

### P-vks — données du consortium

- Scènes : `x04.vks`, question dès `g03` et `g14`.
- Prédiction : sans fichiers transmis, il n’y a pas de générateur VKS. Le repli du plan est SFEMaNS à basse résolution, ou les paliers 0–2 seuls (`en/these/index.qmd:939`).
- Confiance : non applicable (ça n’est pas une prédiction physique).
- `result-met` : seulement des grandeurs présentes dans les fichiers, avec l’autorisation de publication. Jamais un renversement « généré » si seuls des instantanés de simulation sont arrivés.
- `result-unmet` : accès refusé ou trop tard. Le film garde les questions.
- `result-inconclusive` : fichiers reçus mais opérateur de divergence non identifié (`en/rapport/index.qmd:1185`).

### P-dresdyn — palier 4

- Scène : `x05.dresdyn` uniquement (hors cœur).
- Prédiction : on ne promet pas un Rm_c(Po). On promet la question : quelle condition aux limites, et combien de valeurs de Po existent (`en/these/index.qmd:946-953`).
- Confiance : faible sur tout chiffre, parce que la fenêtre numérique n’est pas dans le dépôt (U7).
- `result-*` : même discipline. Le cœur ne contient pas cette scène ; s’il mentionne DRESDYN, c’est comme objectif (ii), CONTEXT, sans taux.

## Ce que aucune issue n’a le droit de dire

- « Le modèle produit des renversements 3D. »
- « Le seuil VKS est 31 » sans la définition.
- « Le budget est de X euros » sans fichier de banc.
- « La perte de stationnarité marche en 3D » à partir d’E2 seul.
- Un graphique de loi future dessiné « pour voir » avant les données.

## Alternative si les résultats n’arrivent jamais

Le cœur et l’étendu sont montables aujourd’hui : les scènes en attente jouent `narr.*.bet`. L’épisode « Results update » est un remplacement de créneaux, pas un autre film. Cette phase ne produit ni l’un ni l’autre.
