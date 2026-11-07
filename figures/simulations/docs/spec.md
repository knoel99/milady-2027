# Spec — figure « simulations »

## Structure
Petits multiples (P3) : trois expériences sur un même gabarit ; la variable qui change est le système. Le panneau de balayage partage son axe horizontal avec le paramètre (P24) : les points d'entraînement et de test sont posés sur l'axe de la réponse.

## Concepts
| Concept | Esquisse | 5 s | Fidèle | Comparaison (P3, P13) | Choix |
|---|---|---|---|---|---|
| **A. Une rangée par expérience** | rangées E1, E2, E3 ; colonnes « Système », « Schéma », « Balayage », « Données », « Dans la chaîne » | oui | oui | grille étiquetée par ses deux dimensions | brouillon 1 |
| **B. Une colonne par expérience** | colonnes E1, E2, E3 (vignettes en tête, comme plan-these) ; rangées « Balayage », « Schéma », « Données », « Chaîne » | oui | oui | idem, transposée ; lien visuel fort avec plan-these | brouillon 2 |
| C. Une figure par expérience | trois figures séparées | faible | oui | non | écarté |

## Carte
**Size:** 183 × 100 mm.
**Hero:** none, comparaison de trois bancs (petits multiples, P3) ; vignettes reprises de plan-these (calculées), courbes de réponse tracées à partir des résultats (E1, E3) ou recalculées (E2).

### Composants (communs aux deux concepts)
| Composant | Libellés | Source |
|---|---|---|
| vignette E1 | « Gissinger, 3 modes », « D(t) » | plan_data.json (gissinger) |
| vignette E2 | « MHD 2D forcée » | plan_data.json (mhd2d : j et isolignes de a) |
| vignette E3 | « dynamo ABC » | plan_data.json (abc, Rm = 12) |
| balayage E1 | axe « Γ » 0,80–1,00 ; réponse « passages de D par 0 » ; 11 points d'entraînement, 10 de test ; bande du seuil 0,86–0,865 | e1_gissinger.json |
| balayage E2 | axe « η » log 0,004–0,0226 ; réponse « E_B » (moyenne ± écart-type) ; 6 + 5 points | sim_data.json (recalcul) |
| balayage E3 | axe « Rm » 2–30 ; réponse « λ » ; 24 points ; ligne λ = 0 ; seuils 8,87 / 17,6 / 26,8 ; fenêtres λ > 0 teintées | e3_abc.json |
| schéma | E1 « RK4, Δt = 0,01 » ; E2 « pseudo-spectral 32², 2/3 », « forçage blanc » ; E3 « pseudo-spectral 32³, 2/3 », « RK4 à facteur intégrant » | scripts des expériences |
| données | E1 « 16 trajectoires × 1 500 états par Γ » ; E2 « 16 membres × 150 instantanés par η » ; E3 « λ(Rm), modes propres » | scripts |
| chaîne | E1 « script autonome » ; E2 « → palier1_mhd2d » ; E3 « → palier2_abc3d » | infra/configs |

### Conventions
- Vert : paramètre de contrôle (axes Γ, η, Rm et leurs points). Vermillon : grandeur magnétique (D, E_B, λ). Gris : le reste.
- Points pleins = valeurs d'entraînement ; points vides = valeurs de test (comme les figures du rapport).

### Contraintes négatives
- Pas de courbe sans source ; pas d'unité inventée.
