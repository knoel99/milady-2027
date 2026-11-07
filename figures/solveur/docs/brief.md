# Brief — figure « solveur »

- **Mode** : design. **Format** : journal, 183 mm (page Calcul et données, section « Le solveur, les campagnes et l'entraînement » ; le panneau sur le fichier est cité depuis la section « Le format de données »).
- **Lecteur** : les encadrants (méthodes spectrales, MHD), la personne qui lancera ou modifiera le solveur.
- **Phrase à retenir** : le solveur avance l'état spectral (û, B̂) par un RK4 à facteur intégrant dont les termes non linéaires sont calculés en espace physique, désaliasés et projetés ; une simulation enregistre ses diagnostics depuis t = 0 et ses champs sur la fenêtre gardée, survit aux interruptions par points de contrôle, puis écrit un fichier MFF dont chaque partie a sa ligne au catalogue.

## Idées clés
1. Un pas : rotationnels en Fourier (ik×), passage en espace physique (irfftn), produits u×ω + j×B et u×B, retour (rfftn), désaliasage 2/3, projection de Leray du terme de quantité de mouvement, rotationnel du terme d'induction ; RK4 de Lawson : la diffusion νk², ηk² est intégrée exactement ; quatre évaluations du second membre par pas.
2. Les deux divergences restent nulles : projection de Leray (u), forme rotationnelle (B), nettoyage périodique des deux.
3. Une simulation dans le temps : diagnostics tous les `diag_every` depuis t = 0, champs tous les `every` sur ]t_burn, t_burn + t_keep] ; point de contrôle toutes les 900 s de calcul et à la réception de SIGTERM ; reprise automatique ; statuts queued → running → done (ou failed).
4. Ce qui est écrit : un fichier MFF (partie The Well + partie `milady_*`) et des lignes au catalogue reliées par l'UUID.

## Ne doit pas laisser croire
- qu'un temps GPU a été mesuré ; qu'un point de contrôle tombe à des instants simulés fixes (c'est une période de calcul) ;
- que B est projeté à chaque étage RK (le second membre de B est un rotationnel ; la projection de B est un nettoyage périodique) ;
- que le fichier ne peut jamais être réécrit.

## Exemple suivi
`palier2_tg3d` (64³, mode dynamique, t_burn = 100, t_keep = 40, every = 1, diag_every = 0,1).

## Style
Celui des figures du site (bleu u, vermillon B, gris pour les opérations ; Fourier sur fond gris bleuté, espace physique sur fond blanc).
