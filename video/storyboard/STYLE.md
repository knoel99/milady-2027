# Storyboard v4 : charte d'écriture (à lire en entier avant d'écrire)

Historique. La v2 (texte traduit de l'anglais) a été jugée catastrophique : phrases raides, calques
(« le champ se renverse »). La v3 (ton de vidéaste YouTube : « vous », questions rhétoriques,
analogies, humour) a été écartée par l'auteur le 2026-11-09. **La v4 adopte le registre d'un
article de Wikipédia en français**, lu à voix haute : encyclopédique, neutre, précis, sourcé.
Les visuels restent en anglais (titres, étiquettes, puces) ; la voix off et les sous-titres sont en
français. L'anglais sera adapté du français **après** validation.

## 1. Le registre : Wikipédia lu à voix haute

- **Neutre et impersonnel.** Troisième personne, présent de l'indicatif (passé composé pour
  l'histoire). Pas de « vous », pas de « je ». « On » seulement là où Wikipédia l'emploierait
  (« on appelle… », « on parle de… »). Pas de « nous ».
- **Déclaratif.** Pas de questions rhétoriques, pas de suspense, pas d'interpellation (« regardez »,
  « à votre avis », « attendez »), pas d'exclamations, pas d'humour, pas de familiarités (« le truc »,
  « bon », « sauf que », « du coup »).
- **Définir avant d'employer.** Chaque notion est introduite par une définition en une phrase, sur
  le modèle d'un article : « L'effet dynamo est le mécanisme par lequel un fluide conducteur en
  mouvement entretient un champ magnétique. »
- **Précis et mesuré.** Les nuances épistémiques sont dites avec les mots de l'encyclopédie :
  « est mesuré », « est démontré », « est conjecturé », « n'a pas encore été établi », « selon… ».
  Les badges MEASURED / PROVED / CONJECTURE / PLANNED / CONTEXT restent à l'écran.
- **Sources.** Les faits externes sont attribués (« selon Vine et Matthews (1963) », « d'après
  les mesures de l'expérience VKS »), sobrement : une attribution orale par plan au plus ; la
  référence complète est sur la puce à l'écran.
- **Analogies** : seulement si elles éclairent un mécanisme, formulées sobrement (« le principe est
  comparable à celui d'une dynamo de bicyclette »), sans mise en scène.
- **Phrases complètes mais pas trop longues** : une ou deux propositions, une idée par phrase,
  écrites pour l'oreille (pas de parenthèses, d'abréviations, de « cf. », « i.e. », « etc. ») ;
  sigles épelés ou développés à la première occurrence.
- **Transitions** sobres et logiques : « Ce mécanisme a une conséquence… », « Une seconde
  difficulté tient à… », « La section suivante présente… ».
- Les formules ne sont **jamais lues** : elles s'affichent sur le calque formule ; la voix énonce
  l'idée en mots.
- Chiffres : arrondis à l'oral (« environ deux pour mille »), exacts à l'écran.
- La progression L0 → L5 est conservée : les premiers chapitres définissent tout ; les derniers
  emploient le vocabulaire technique déjà défini.
- Débit visé **≈ 150 mots par minute**. La concision encyclopédique doit **raccourcir** le texte :
  viser au plus la durée cible v2 de chaque scène (`target_s` dans `video/script/<unité>.json`).

## 2. Glossaire imposé (FR oral ↔ visuel EN)

| Concept | Dire (FR) | Ne pas dire | À l'écran (EN) |
|---|---|---|---|
| flip / reversal | **inversion** (de polarité, du champ), **le champ s'inverse** | renversement, se renverser, basculer | flip, reversal |
| how often it flips | **la fréquence des inversions** | taux de renversement | flip rate, how often |
| magnetic field | le champ magnétique, puis **le champ** | | field, B |
| dynamo effect | **l'effet dynamo** ; une dynamo | | dynamo |
| magnetic Reynolds number | **le nombre de Reynolds magnétique**, puis « R M » | | Rm |
| threshold | **le seuil** (de l'effet dynamo) | | threshold, Rm_c |
| flow | **l'écoulement** | le flot, le flux | flow, u |
| liquid sodium / metal | **le sodium liquide**, le métal liquide | | liquid sodium |
| snapshot | **un instantané** (de champ) | une photo, un cliché | snapshot |
| generative model | **un modèle génératif** (réseau de neurones entraîné à produire des instantanés) | une IA qui invente, une machine qui rêve | generative model |
| flow matching | le **flow matching** (terme conservé, défini une fois) | appariement de flots | flow matching |
| divergence-free | **à divergence nulle** (le champ n'a ni source ni puits) | solénoïdal sans définition | div B = 0 |
| constraint, hard / soft | une contrainte **exacte** / une contrainte **statistique** (respectée en moyenne) | dure / molle | hard / soft constraint |
| crowd law / crowd loss | une **loi statistique** ; **le terme de perte statistique** | loi de foule, perte de foule | crowd law, crowd loss |
| induction equation | **l'équation d'induction** | | induction equation |
| kinematic dynamo | **dynamo cinématique** (écoulement imposé) | | kinematic dynamo |
| growth rate | **le taux de croissance** | | growth rate s |
| chaos | la dynamique chaotique, la sensibilité aux conditions initiales | | chaos |
| supervisor | **les encadrants** | les superviseurs | supervisors |
| internship / PhD | **le stage**, **la thèse** | | internship, PhD |
| simulation run | une simulation, un calcul | un run | run |
| mirror symmetry | **la symétrie B ↦ −B** (changement de signe du champ) ; « symétrie miroir » après définition | symétrie de renversement | mirror |
| pending result | **un résultat non encore obtenu** ; une **hypothèse de travail** | siège vide, pari | AWAITING / PLANNED / BET |

Noms propres : Gissinger (à la française), VKS (« V K S », expérience von Kármán Sodium), Cadarache,
Riga, Karlsruhe, DRESDYN (« Dresdyne »), Jean Zay (supercalculateur). Vérifier le nom et l'année de
chaque source dans le JSON de l'unité ; ne rien inventer (règle D7 de `video/BRIEF.md`).

## 3. Structure : les questions aux encadrants vont à la fin

- **Plus aucune carte « Question pour les encadrants » dans les chapitres.** Les plans `<unité>.Q`
  sont supprimés ; leurs questions sont reprises dans l'unité finale **« Ouvertures »** (`ch10q`,
  déplacée en toute fin de film, après la conclusion `ch11`).
- Dans le corps d'un chapitre, un résultat non encore obtenu est énoncé comme dans un article :
  « Ce point n'a pas encore été établi ; l'hypothèse de travail est que… ». Pas de « pari », pas de
  question posée au spectateur.
- L'unité **Ouvertures** clôt le film de manière conclusive, comme la section « Perspectives » d'un
  article : elle regroupe **toutes** les questions du registre
  (`video/script/_shared/question_register.json`, 37 questions) par thème, les présente comme des
  **questions ouvertes** dont dépend la suite du projet (« La question du choix de la grandeur à
  calculer en premier reste ouverte : … »), et indique pour chacune ce qu'elle conditionne. Le
  numéro Qn est affiché à l'écran pour renvoyer à la fiche `video/QUESTIONS-ENCADRANTS.md`.

## 4. Les visuels

Le texte commande l'image : chaque plan a un visuel qui illustre ce que dit la phrase. Avec le
registre encyclopédique, les visuels sont **sobres** : schémas qui se construisent, données réelles,
figures annotées, cartes, frises ; pas de mise en scène comique. Indiquer pour chaque plan s'il
**reprend** une scène v2 (identifiant, et ce qui change) ou s'il est **nouveau**. Préférer réutiliser
les scènes v2 qui marchent (données réelles, figures).

## 5. Format d'un fichier `video/storyboard/<unité>.md`

```
# <unité> · <titre FR> (≈ m min ss s)

**Objectif :** ce que le spectateur doit avoir compris. **À retenir :** une phrase.
**Niveau :** L0–L5. **Version :** courte et longue | longue seulement.

## <n°> · <titre du plan> · ≈ <durée> s · reprend <id v2> | nouveau
**On voit :** le cadre, ce qui est à l'écran.
**Animation :** ce qui bouge, synchronisé sur les mots de la voix (« sur "inverse" : l'aiguille pivote »).
**Textes à l'écran (EN) :** titres, étiquettes, puces, badge, référence.
**Voix off :**
> Le texte dit, tel qu'il sera lu. Paragraphes courts.

(**Note :** seulement si nécessaire : simplification, fait à vérifier, choix à valider.)
```

Le numéro de plan reprend l'identifiant v2 quand le plan en descend ; un plan nouveau prend un
suffixe (00.2b). La durée est estimée à 150 mots/min plus le temps des animations muettes.
En fin de fichier : `**Durée totale estimée :** m min ss s · **Mots :** n` et la liste des **points à
valider** par l'auteur (au plus 5).

## 6. Exemple de référence

`video/storyboard/ch00.md` est l'étalon du registre et du format. S'y conformer.
