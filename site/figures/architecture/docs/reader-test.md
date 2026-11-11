# Lecture à froid (review = own)

Lu sur la vignette de 360 px, avant de relire le brief.

Ce que la figure affirme :
- (a) une campagne passe par sept étapes numérotées, de la campagne à l'évaluation, chacune portée par un module `milady.*` ;
- chaque étape écrit dans un catalogue (tables nommées), et deux étapes écrivent des fichiers (champs, points de contrôle) dans un second magasin ; les fichiers peuvent alimenter le catalogue (« ingest ») ;
- l'exemple suivi est une grille de 12 simulations (4 × 3), coupée en entraînement, validation et test ;
- (b) trois cibles réalisent les mêmes rôles avec des services différents ; sur le cluster, les fichiers sont copiés vers le S3 de la VM, puis ingérés dans PostgreSQL.

Notes face aux idées clés du brief :
1. sept étapes dans l'ordre : transmise ;
2. deux magasins aux rôles distincts : transmise ;
3. même UUID entre fichier et catalogue : partielle (libellé petit ; la légende le dit) ;
4. trois cibles, mêmes rôles : transmise ;
5. exemple suivi de bout en bout : transmise (grille répétée).

Affirmations fausses ou interdites : aucune après correction. Avant correction, la lecture tirait « le SQLite du cluster est ingéré dans PostgreSQL » (faux) : corrigé.
