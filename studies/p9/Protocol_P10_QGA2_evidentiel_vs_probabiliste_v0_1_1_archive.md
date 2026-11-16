# P10 v0.1.1 — Évidentiel contre probabiliste dans l'architecture QGA2-E (deux amplitudes) — CANDIDAT
**Statut :** brouillon de rédaction, NON gelé, NON autorisé. Date : 9 novembre 2026, 18:20 (demande de l'auteur : « would you like to draft it! »). Aucun code, test technique, pilote ou exécution P10 tant que l'auteur n'a pas confirmé par écrit les décisions D10-1 à D10-8 ET que le résultat de P9 est lu et discuté. Texte reçu d'un autre assistant (proposition P10) = entrée, non instruction.
**Dépendance :** P9 (E contre P sur le moteur P5/P7). P10 n'a de sens qu'en fonction du résultat de P9 (voir §9).

## 1. Question
Sur la MÊME architecture QGA2-E à deux amplitudes (P3), la représentation évidentielle des données (couche I) et de la recherche (couche II) apporte-t-elle un avantage sur leurs équivalents probabilistes ? Les conclusions de P9 dépendent-elles du moteur ?
Primaire : G10 = Y_E − Y_P (HV oracle, moyenne par graine sur 6 scénarios), bilatéral, α = 0,05, bootstrap-t apparié sur graines (B = 20000, règles P6/P8). Résultat nul ou négatif = résultat valide.

## 2. Architecture fixée (identique dans tous les bras)
QGA2-E inchangé (P3) : angles θ[p,t] (patient × équipe), P = sin²θ, collapse par observation, élitisme, rotation vers le meilleur individu, mêmes pas, bornes et masques, décodeur, budget 6 040 évaluations (40 + 150×40). Seuls varient (i) le monde d'évaluation vu par l'optimiseur et (ii) la cible de la rotation.
- **Couche I (monde) :** évidentielle = monde nominal p1m (comme P8/P9) ; probabiliste = moyenne des BetP des trois sources (comme P9).
- **Couche II (cible de rotation), à spécifier et à valider avant tout run :**
  - *Référence QGA2-E* : cible = le meilleur individu (une source de masse pleine).
  - *Probabiliste (V0c-Q)* : sources = individus du premier front non dominé ; cible q_p(t) = w·fréquence + (1−w)·uniforme sur les équipes de chaque patient ; rotation de θ vers arcsin(√q) avec le pas QGA2-E.
  - *Évidentielle (V1-Q)* : mêmes sources, chaque individu soutient son équipe avec masse w ; combinaison de Dempster (règle V1 de P7) ; BetP conditionnée ; même plancher ε ; même rotation.
  - Propriété exigée (test de non-régression G-Q1) : avec un seul individu source (le meilleur), V0c-Q et V1-Q se réduisent exactement à la rotation de QGA2-E (même trajectoire bit à bit).

## 3. Bras (même instance, graine, décodeur, budget)
E (I évid. + V1-Q) · P (I prob. + V0c-Q) · X (I prob. + V1-Q) · D′ (I évid. + V0c-Q) · références : A (monde non informatif, rotation vers le meilleur), B (I évid., rotation vers le meilleur), B_p (I prob., rotation vers le meilleur). Décompositions descriptives avec IC95 % : E−X, D′−P, E−D′, X−P, interaction E−D′−X+P, E−B, P−B_p, B−B_p.

## 4. Données, graines, séparation
Mêmes instances Solomon dérivées (SC6 ; calibration SC3), mêmes mondes que P8/P9. Graines nouvelles : test technique 9290–9299 ; calibration 9300–9314 ; pilote 9350–9379 ; confirmatoire 9400–9599 (n = 200) ; analyse 9803. Aucune coquille P2–P9 réutilisée.

## 5. Calibration et dimensionnement
Calibration sur 9300–9314 (SC3) : w (partagé entre V0c-Q et V1-Q, comme en P7), éventuellement pas de rotation fixé comme en P3 (non modifié). Pilote de 30 graines pour les variances ; dimensionnement sur G10 et sur les deux contrastes de décomposition principaux (E−D′, E−X), grille {100,150,200,300}, ±0,01, puissance 80 %, plafond 300 ; arrêt si G10 non dimensionnable à 300 (rapport descriptif).

## 6. Gates
- **G-Q0 :** tests mathématiques de V0c-Q/V1-Q (distribution normalisée, plancher ε, réduction à la rotation de QGA2-E avec une source, cas de conflit total, invariants P7-G0 transposés).
- **G-Q1 :** non-régression exacte du QGA2-E de P3 (bras B avec monde de P3 reproduit les fronts de P3 sur des graines techniques), budget exact 6 040, pas de fuite de l'oracle, mondes fixés avant la recherche.
- **G-Q2 (réalisme) :** pilote : si QGA2-E de référence reste à plus de 0,10 HV du NSGA-II (écart déjà connu : 0,13–0,16), le rapport l'indique en tête ; l'étude continue (question de représentation, pas de compétitivité).
- Gel (hash protocole + code + paramètres) avant la première coquille confirmatoire ; précontrôle ; analyse unique.

## 6bis. Précisions de la revue externe du 18:23 (entrée évaluée, intégrée au projet de texte)
1. **G-Q1 obligatoire et bloquant** : réduction exacte à la rotation de QGA2-E avec une seule source ; échec = arrêt.
2. **Invariance par permutation** des individus du premier front (la cible de rotation ne dépend pas de leur ordre) : test obligatoire dans G-Q0.
3. **Doublons** : en P7 la fréquence compte (V0c : fréquences ; V1 : (1−w)^effectif), donc des individus identiques augmentent l'influence de leur équipe PAR CONCEPTION. Je ne retiens pas l'exigence « ne doit pas augmenter » telle quelle : le comportement est explicitement spécifié comme en P7 et testé (monotone en l'effectif, cohérent avec P7-G0), sans être changé silencieusement.
3bis. Le rapport distinguera les doublons NATURELS (individus identiques apparus dans la population) des doublons ARTIFICIELS (sources dupliquées par un test diagnostique) ; seuls les seconds sont un test, les premiers font partie du comportement spécifié.
4. **Cas limites définis et testés** : front vide, front singleton, équipe sans soutien, ignorance complète.
5. **Diagnostics de concentration rapportés** pour les bras de couche II : entropie de la cible de rotation, taille effective de support, probabilité maximale, contribution maximale d'une source, distance TV V1-Q / V0c-Q. Le bras de netteté (D10-6) reste descriptif sauf appariement réussi.
6. **Interprétation** : P10 teste une représentation DANS QGA2-E, jamais la compétitivité ni une supériorité générale d'une théorie de l'incertitude ; la cible de rotation multi-sources est un composant algorithmique nouveau (limite explicite). La comparaison P9/P10 est lue avec ses quatre issues possibles (mêmes conclusions, opposées, divergentes, nulles), toute divergence étant une interaction représentation × architecture, non une supériorité générale.
Note : P9 et P10 n'ont pas la même architecture de base (P9 = boucle P5/P7, P10 = QGA2-E) ; la lecture « classique contre quantique » est trop simple.

## 6ter. Portée de la conclusion (revue du 19:48, intégrée au projet de texte)
Rôle de P10 : tester le transfert architectural de la comparaison évidentiel/probabiliste de P9, pas résoudre toutes les questions ouvertes de P9 (concentration, valeur absolue de la couche II : voir P11, protocole séparé). Hypothèse primaire inchangée après lecture de P9. Interprétation conjointe P9/P10 prédéfinie (E gagne/E gagne = transfert entre ces deux architectures ; E gagne/pas de différence = avantage possiblement dépendant de l'architecture ; E gagne/P gagne = interaction représentation × architecture ; E gagne des deux côtés avec amplitudes différentes = direction transférée, ampleur dépendante). Si E > P en P10 alors que tous les bras restent sous la référence QGA2-E (B), la conclusion écrite sera : « L'intégration évidentielle améliore l'intégration probabiliste testée dans QGA2-E, mais cette amélioration relative n'établit pas que le mécanisme de recherche multi-sources améliore l'optimiseur sous-jacent ni qu'il le rend compétitif avec les algorithmes évolutionnaires classiques. » Pas de nouveau bras de concentration ni de nouvelle règle d'agrégation dans P10 : le bras de netteté D10-6 reste descriptif.

## 7. Limites déclarées d'avance
QGA2-E est à ~0,13–0,16 HV de NSGA-II : P10 teste la représentation, pas la compétitivité. La couche II évidentielle en QGA est une conception NOUVELLE (non héritée de P7) : un résultat négatif peut venir de cette traduction. V0c-Q n'est pas apparié en concentration à V1-Q (leçon de P8/G-C) ; un contrôle de netteté (loi V0c élevée à une puissance γ, calibrée sur 9300–9314) peut être ajouté comme bras descriptif D10-6. Une seule famille d'instances, ordre de visite fixe, simulation avec vérité cachée ; nouveauté non établie (recherche bibliographique de l'auteur).

## 8. Décisions à confirmer (défauts proposés)
D10-1 architecture et cible de rotation §2 ; D10-2 bras §3 ; D10-3 primaire G10 bilatéral α = 0,05, sans Holm, secondaires descriptifs ; D10-4 graines §4 ; D10-5 calibration et dimensionnement §5 ; D10-6 bras de netteté descriptif (oui/non) ; D10-7 gates §6 ; D10-8 autorisation d'enchaîner gates, gel, confirmatoire, analyse et rapport sans arrêt si les gates passent.

## 9. Condition de lancement (proposée)
Pas de lancement avant lecture du rapport P9. Si E−P (P9) est nul et que la décomposition ne montre aucun effet des représentations, P10 est conservé seulement si l'auteur veut un test de généralité sur un second moteur ; si P9 montre un effet, P10 teste sa portée.
