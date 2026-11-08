# Storyboard v3 : charte d'écriture (à lire en entier avant d'écrire)

Le script v2 a été jugé **catastrophique** par l'auteur : texte traduit de l'anglais, phrases raides,
ton de notice, vocabulaire calqué (« le champ se renverse »). La v3 est **écrite directement en
français**, comme un script de vidéaste scientifique YouTube : un style **parlé, semi-écrit**. Les
visuels restent en anglais (titres, étiquettes, puces) ; la voix off et les sous-titres sont en français.
L'anglais sera adapté du français **après** validation, pas l'inverse.

## 1. Le ton

- On parle à quelqu'un, en face. **« Vous »** pour s'adresser au spectateur, **« on »** pour « nous
  tous / la science ». Jamais « nous passerons par ».
- Phrases courtes. Une idée par phrase. On peut commencer par « Bon. », « Alors », « Et là »,
  « Sauf que », « Le truc, c'est que », « Attendez. », « Petit détour. ». Avec modération : 1 ou 2 par
  plan, pas à chaque phrase.
- **Questions rhétoriques** et **suspense** : on pose la question avant de donner la réponse ; on
  laisse le spectateur deviner (« À votre avis ? »), puis on montre.
- **Analogies concrètes** du quotidien (pâte à crêpe, élastique, dynamo de vélo, pièce de monnaie,
  embouteillage…), puis on dit **où l'analogie s'arrête**.
- **Humour léger**, autodérision, jamais de blague qui fausse la physique.
- **Honnêteté** : quand on ne sait pas, on le dit franchement (« Et ça, honnêtement, on ne sait pas
  encore. C'est justement une des questions de la thèse. »). Les badges MEASURED / PROVED /
  CONJECTURE / PLANNED / CONTEXT restent à l'écran ; la voix les traduit en mots simples (« ça, c'est
  mesuré », « ça, c'est démontré », « ça, c'est un pari »).
- **Transitions** qui tirent vers la suite (« Et c'est là que ça se complique. », « Gardez cette image
  en tête, elle va revenir. »). Rappels des motifs (l'aiguille, la boîte à chaussures de photos, le
  miroir, la foule) comme des running gags.
- Pas de liste à puces lue à voix haute. Pas d'énumération « premièrement, deuxièmement » sauf si c'est
  un effet voulu.
- Les formules ne sont **jamais lues** : elles s'affichent en petit (calque formule) ; la voix dit
  l'idée (« le champ ne doit avoir ni source ni puits »).
- Chiffres : arrondis à l'oral (« à peu près deux pour mille »), exacts à l'écran.
- On garde la montée L0 → L5, mais même en L5 on parle comme un humain : le jargon arrive **après**
  l'image, et on le définit en une phrase la première fois.
- Débit visé : **≈ 150 mots par minute** (voix Ethan FR). Un plan dure 8 à 40 s ; au-delà, on coupe.
  Rythme : alterner plans courts (3–8 s, une phrase-choc) et plans d'explication.
- Écrire pour l'oreille : pas de parenthèses, pas d'incises longues, pas d'abréviations (on dit « le
  nombre de Reynolds magnétique », puis « Rm » prononcé « R M »), sigles épelés s'il le faut.
  Pas de « cf. », « i.e. », « etc. ».

## 2. Glossaire imposé (FR oral ↔ visuel EN)

| Concept | Dire (FR) | Ne pas dire | À l'écran (EN) |
|---|---|---|---|
| flip / reversal | **inversion** (du champ), **le champ s'inverse** | renversement, se renverser, basculer | flip, reversal |
| how often it flips | **la fréquence des inversions**, « combien de fois par… » | taux de renversement | flip rate, how often |
| magnetic field | le champ magnétique, puis **le champ** | | field, B |
| dynamo effect | **l'effet dynamo** ; une dynamo | | dynamo |
| magnetic Reynolds number | **le nombre de Reynolds magnétique**, puis « R M » | | Rm |
| threshold | **le seuil** | la valeur critique (sauf précision) | threshold, Rm_c |
| flow | **l'écoulement** (du métal liquide) | le flot, le flux | flow, u |
| liquid sodium / metal | **le sodium liquide**, le métal liquide | | liquid sodium |
| snapshot | **un instantané**, une « photo » du champ | un cliché, une capture | snapshot |
| generative model | **un modèle génératif**, une IA qui invente des instantanés | une machine qui rêve | generative model |
| flow matching | le **flow matching** (on garde le terme, expliqué une fois) | appariement de flots | flow matching |
| divergence-free | **sans divergence** ; à l'oral : « pas de source, pas de puits » | solénoïdal (sauf L5, défini) | div B = 0 |
| constraint, hard / soft | une contrainte **exacte** / une contrainte **en moyenne** | dure / molle | hard / soft constraint |
| crowd law (statistical law) | une **loi statistique**, une loi « de foule » (images de la foule) | loi de la foule (calque) | crowd law |
| induction equation | **l'équation d'induction** | | induction equation |
| kinematic dynamo | **dynamo cinématique** (écoulement imposé) | | kinematic dynamo |
| growth rate | **le taux de croissance** | | growth rate s |
| chaos / sensitivity | le chaos, la sensibilité aux conditions initiales | | chaos |
| supervisor | **les encadrants** (de thèse) | les superviseurs | supervisors |
| internship / PhD | **le stage**, **la thèse** | | internship, PhD |
| simulation run | une simulation, un calcul | un run | run |
| benchmark | un banc d'essai, un test de référence | | benchmark |
| mirror symmetry | la **symétrie miroir** (B ↦ −B) | | mirror |
| empty seat (pending result) | **une case vide**, un résultat qu'on n'a pas encore | siège vide | AWAITING / PLANNED |
| bet | **un pari** | une conjecture (sauf badge) | BET / CONJECTURE |

Noms propres : Gissinger (à la française), VKS (« V K S », expérience von Kármán Sodium), Cadarache,
Riga, Karlsruhe, DRESDYN (« Dresdyne »), Jean Zay (supercalculateur). Vérifier le nom et l'année de
chaque source dans le JSON de l'unité ; ne rien inventer (règle D7 de `video/BRIEF.md`).

## 3. Ce qui ne change pas

- **Les faits** : tout ce que dit la v3 doit déjà être dans la v2 (`video/script/<unité>.json`,
  champs `paragraphs`, `sources`, `onscreen`) ou dans les sources citées. Aucun chiffre nouveau.
  On peut **retirer**, **simplifier**, **réordonner**, **regrouper**. Un fait externe ajouté exige une
  source déjà présente dans le dépôt (`video/ETAT-DE-L-ART.md`, pages du site) et doit être signalé.
- Les badges d'honnêteté, les cartes « Question pour les encadrants » (numéros Qn du registre
  `video/script/_shared/question_register.json`), les résultats manquants présentés comme **pari +
  question qui tranchera**.
- Les visuels restent en anglais et à fond sombre dominant (BRIEF D9).

## 4. Ce qui change dans les animations

Le texte commande l'image. Pour chaque plan, proposer le visuel qui **porte** la phrase dite à ce
moment : quand la voix dit « regardez », il faut qu'il y ait quelque chose à regarder. Viser le rythme
d'une vidéo YouTube : un changement visuel toutes les 3–6 s (zoom, apparition, surlignage, coupe),
des plans d'illustration simples, des schémas qui se construisent au fil de la phrase, des reprises de
motifs. Indiquer pour chaque plan s'il **reprend** une scène v2 (identifiant, et ce qui change) ou s'il
est **nouveau**. Préférer réutiliser les scènes v2 qui marchent (données réelles, figures) en changeant
le cadrage et le minutage, plutôt que tout refaire.

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

Le numéro de plan reprend l'identifiant v2 quand le plan en descend (00.1, 00.2…) ; un plan nouveau
prend un suffixe (00.2b). La durée est estimée à 150 mots/min plus le temps des animations muettes.
En fin de fichier : `**Durée totale estimée :** m min ss s · **Mots :** n` et la liste des **points à
valider** par l'auteur (au plus 5).

## 6. Exemple de référence

`video/storyboard/ch00.md` est l'étalon du ton et du format. S'y conformer.
