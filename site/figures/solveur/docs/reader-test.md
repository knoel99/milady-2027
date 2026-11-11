# Lecture à froid (review = own)

Ce que la vignette affirme : (a) l'état est stocké en Fourier ; on prend des rotationnels, on passe en espace physique pour les produits, on revient, on coupe les hautes fréquences, on projette (Leray) ou on prend un rotationnel, et un RK4 « de Lawson » combine le tout avec une décroissance en k, puis la boucle revient à l'état ; (b) une simulation enregistre des diagnostics en continu et 40 instantanés à la fin, survit à une interruption par point de contrôle ; (c) le fichier écrit a des attributs `milady_*` qui correspondent à des colonnes du catalogue.

Face aux idées clés : 1 transmise ; 2 partielle (la divergence nulle n'est pas écrite en toutes lettres : la projection de Leray et la forme rotationnelle le portent ; la légende le dit) ; 3 transmise ; 4 transmise.

Affirmations fausses ou interdites : aucune (pas de projection de B à chaque étage ; points de contrôle non chiffrés en temps simulé).
