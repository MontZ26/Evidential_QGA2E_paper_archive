# Protocole P5 — IQGA-HHC-Affectation (version 0.1, CANDIDATE)

**Statut : projet de protocole, texte seul. Non approuvé, non gelé. Aucun code n'est écrit et aucune expérience n'est lancée tant que l'auteur n'a pas confirmé par écrit le protocole final.**
Auteur : Dr Montassar Zaghdoud. Rédaction : Claude. Date de rédaction : 8 novembre 2026.
Légende : **[P]** = proposition à confirmer ; **[O-n]** = décision ouverte listée au §15 ; **[F]** = fait établi par P3/P4 (rapports et fichiers gelés).

---

## 0. Ce que ce protocole est et n'est pas

- Il vise la formulation **A** : affectation de chaque patient à une équipe admissible (masque M), ordre de visite fixé, trois objectifs, point de référence (1,2 ; 1,2 ; 1,2), HV exact en monde T (valeurs vraies), mêmes six scénarios que P3 et P4 (S4/S5-RC101, R101, C101). Le routage intégré (option B) n'est pas traité ici.
- Il ne promet pas de gain. Un résultat nul ou négatif sera rapporté tel quel, comme pour P3 et P4.
- Il est conçu **après** P3 et P4 et en connaissant leurs résultats. Cette conception conditionnelle sera déclarée dans l'article.
- Les hypothèses de conception (§1) sont des hypothèses issues de P4 et d'une lecture partielle de la littérature (annexe A en cours de mise à jour) ; elles ne sont pas des résultats établis.

## 1. Question centrale et motivation

**Question centrale.** À représentation, décodeur, réparation, opérateurs classiques, recherche locale et budget identiques, une règle de mise à jour **par rotation d'amplitudes** apporte-t-elle un avantage mesurable en hypervolume par rapport à une règle d'apprentissage probabiliste **classique** ?

Motivation (hypothèses, non démontrées) :
- [F] P4 : QGA-XM-E est significativement moins bon que NSGA-II (D = −0,161), QGA2-E (−0,016) et QGA2 (−0,046), n = 300, Holm.
- [F] P4, descriptif : forte diversité (Hamming 0,57 à la génération 150) mais HV faible ; QGA2 sans élitisme meilleur que QGA2-E ; tournoi seul : −0,021 ; rotation : +0,020.
- Hypothèses de travail (à tester, pas à supposer) : (i) un attracteur unique est mal défini en multiobjectif ; (ii) le fitness d'un échantillon est un signal bruité pour mettre à jour les amplitudes ; (iii) les opérateurs classiques doivent travailler sur les solutions décodées et exploiter la structure d'affectation.
- Lecture de la littérature (voir annexe A) : peu de comparaisons à budget égal, références réglées et tests appariés ; un composant classique (recherche locale, archive, croisement guidé par les élites) semble souvent porter le gain. **Conséquence de conception : tout gain éventuel doit être attribué à la composante quantique-inspirée par un contrôle à opérateurs identiques.**

## 2. Divulgations à reprendre dans l'article

1. P5 est conçu après P3 et P4.
2. Les modules `run_p1m.py` et `ablation_loo.py` ont été reconstruits en P4 (originaux introuvables) ; les versions reconstruites font partie du paquet gelé de P5 [P].
3. Le choix du budget (6 040 évaluations), des hypothèses et des règles de décision est fixé avant les runs confirmatoires.
4. Les seeds confirmatoires sont neuves (§9) ; aucune seed utilisée en P3/P4 n'est réutilisée, sauf pour une vérification de non-régression explicitement listée.

## 3. Formulation (inchangée)

Une équipe par patient parmi les équipes admissibles (masque M) ; objectifs f1, f2, f3 ∈ [0,1], minimisés ; HV exact 3D de référence (1,2 ; 1,2 ; 1,2) ; évaluation en monde T. [F]

**Réparation.** Dans cette formulation, le décodeur sous masque produit toujours une affectation faisable par construction. La réparation est donc la fonction identité. **[O-1]** À confirmer au regard du modèle (contraintes éventuelles de capacité ou de charge). Si aucune contrainte dure ne s'ajoute, « avec et sans réparation » n'a pas d'objet en P5.

## 4. Les bras de comparaison

| Bras | Description | Rôle |
|---|---|---|
| **C2** (IQGA) | Modèle probabiliste à amplitudes, mise à jour par rotation, enfants décodés, opérateurs auxiliaires (§6) | Algorithme testé |
| **C3** (contrôle EDA) | Même représentation à amplitudes, même décodeur, mêmes opérateurs auxiliaires, mêmes élites ; règle de mise à jour **classique** dans l'espace des probabilités (§5.3) | **Contrôle primaire** de H5.1 |
| **C1** (contrôle génome entier) | GA hybride à génome entier (équipe par patient), mêmes opérateurs auxiliaires, même archive | Contrôle de la représentation probabiliste |
| **C0b** | NSGA-II identifiable (classement par rang et crowding, tournoi binaire, survie élitiste inchangés) + mêmes opérateurs auxiliaires | Référence équitable pour H5.4 |
| Références historiques | NSGA2 (standard, P3), NSGA2p, MOEA/D, QGA2, QGA2-E, QGA-XM-E | Continuité avec P3 et P4 |

- C0b est décrit explicitement : les mécanismes ajoutés ne modifient pas la sélection ni la survie de NSGA-II. **[O-2]** À valider : où et comment les opérateurs auxiliaires s'insèrent dans la boucle NSGA-II (par exemple après le croisement et la mutation, avant l'évaluation).
- Les références historiques sont rapportées à part, sans être mélangées aux résultats confirmatoires de P5.

## 5. Représentation et règles de mise à jour

### 5.1 Représentation commune à C2 et C3 [P]
Pour chaque patient i, avec E_i l'ensemble de ses équipes admissibles, un vecteur d'amplitudes réelles (α_ik)_{k∈E_i}, avec Σ α_ik² = 1. La probabilité d'affectation est P(x_i = k) = α_ik². Initialisation uniforme (α_ik = 1/√|E_i|). Décodage : tirage de l'équipe sous le masque, avec les flux aléatoires et la procédure de décodage de P4 réutilisés.

Note : cette paramétrisation est mathématiquement équivalente à une distribution catégorielle. Ce qui sépare C2 de C3 est **uniquement la règle de mise à jour**. **[O-3]** Choisir l'écriture exacte de la rotation multi-états (par exemple rotation dans le plan engendré par l'amplitude de l'équipe cible et du reste, avec normalisation, et plancher sur α_ik pour éviter la disparition prématurée) ; à fixer et à documenter avant tout code.

### 5.2 Règle de mise à jour de C2 (rotation) [P]
À chaque génération, à partir d'un ensemble d'élites E_g (§5.4) : pour chaque patient i, pour chaque élite e, rotation des amplitudes vers l'équipe choisie par e, d'un angle δ (paramètre calibré, §8) pondéré par la qualité relative de e (règle exacte [O-3]). Les enfants sont obtenus par tirage dans le modèle mis à jour **puis** par les opérateurs auxiliaires.

### 5.3 Règle de mise à jour de C3 (contrôle classique) [P]
Mise à jour dans l'espace des probabilités, de type PBIL : p_ik ← (1 − λ)·p_ik + λ·fréquence de k parmi les élites E_g pour le patient i, avec λ calibré (§8), plancher identique à celui de C2, puis renormalisation. Aucune notion d'angle ou de rotation. Mêmes élites, même décodeur, mêmes opérateurs auxiliaires, même budget.

### 5.4 Stratégies d'attracteur (facteur testé en P5-A)
- **a** : attracteur unique persistant (reproduit la logique de QGA2-E).
- **b** : attracteur renouvelé à chaque génération.
- **c** : ensemble de solutions élites non dominées (taille k_e calibrée).
Les trois stratégies sont des variantes de C2 (C2a, C2b, C2c). C3 hérite de la stratégie d'élites retenue pour C2 (§9).

## 6. Opérateurs auxiliaires communs (C1, C2, C3, C0b)

Appliqués aux solutions **décodées**, identiques dans tous les bras ; leur coût d'évaluation est compté (§7).
1. **Croisement d'affectations** : croisement uniforme patient par patient entre deux parents sélectionnés par la règle du bras ; [O-4] variante par groupes de patients (par équipe) à décider.
2. **Mutation ciblée** : réaffectation d'un patient à une autre équipe admissible. Taux calibré (§8).
3. **Recherche locale (LS)** : mouvements de réaffectation d'un patient et d'échange de deux patients entre équipes ; **règle d'acceptation Pareto** : un voisin remplace la solution seulement s'il la domine ; au plus k_LS évaluations par solution traitée, appliquée à une fraction p_LS des enfants. k_LS et p_LS sont calibrés (§8). **[O-5]** Valider cette règle d'acceptation et la liste des voisinages.
4. **Archive externe** de solutions non dominées, de taille bornée, mise à jour après chaque évaluation de façon identique dans tous les bras. Elle sert à la sélection des élites et à la sortie finale ; **[O-6]** décider si l'archive, ou la population finale, fournit le front évalué (identique dans tous les bras).

## 7. Budget et comptage des évaluations [P]

- **6 040 évaluations par run**, identiques pour tous les bras, y compris MOEA/D en P5 (qui recevait 6 030 en P4 ; son résultat P4 reste une référence historique distincte).
- **Chaque évaluation compte** : individus de la population, solutions de la recherche locale, solutions réparées puis évaluées. Aucune recherche locale gratuite. Le compteur est un compteur unique `evaluate()`, vérifié à la fin de chaque run (valeur exacte rapportée, comme en P4).
- Conséquence : le nombre de générations dépend de la dépense en LS. L'arrêt se fait quand le budget est atteint.
- Le coût de réglage (§8) est rapporté séparément et ne s'ajoute pas au budget confirmatoire.

## 8. Calibration des paramètres (budget égal) [P]

- Même méthode pour tous les bras : recherche aléatoire sur des plages pré-déclarées, même nombre de configurations K et de seeds de calibration s par algorithme. Comme chaque run consomme 6 040 évaluations, un nombre égal de runs équivaut à un budget de réglage égal en évaluations. **[O-7]** Valeurs de K et s.
- Mêmes instances de calibration pour tous les bras ; seeds de calibration distinctes des seeds d'exploration et de confirmation (§9).
- Sélection : configuration au HV moyen le plus élevé sur les seeds de calibration ; même règle de départage pour tous.
- Plages à déclarer avant tout run pour chaque bras (liste des paramètres) : δ, λ, k_e, taux de mutation, p_c, p_LS, k_LS, taille de population, plancher d'amplitude, et paramètres NSGA-II/MOEA/D. **[O-8]** Plages exactes.
- **Re-réglage de toutes les références** (NSGA-II, MOEA/D, C0b, C1, C2, C3) selon ce protocole commun ; les paramètres P3 ne sont pas réutilisés pour les résultats confirmatoires de P5.
- Les paramètres sont gelés avant les phases suivantes (hash dans le fichier de gel).

## 9. Phases et seeds [P]

| Phase | Contenu | Statut | Seeds [P] |
|---|---|---|---|
| Calibration | §8 | Réglage | 5000–5019 |
| P5-A | C2a/C2b/C2c, C3, C1, C0b sur seeds d'exploration ; **choix** de la variante C2 retenue | Exploration et sélection | 5100–5149 |
| P5-B | C2 retenu, C3, C1, C0b, références, seeds neuves | **Confirmation** | 5200–5200+n−1 (n ≤ cap) |
| P5-C | Ablations du modèle retenu | Descriptif | mêmes seeds que P5-B |

Plages disjointes de celles de P3/P4 (4200–4209, 4600–4629, 4700–4999). **[O-9]** Plages exactes et cap de n.

**Règle de sélection en P5-A (fixée d'avance).** Retenir la variante de C2 avec le HV moyen le plus élevé sur les seeds d'exploration ; si l'écart avec la variante a (attracteur unique) est inférieur à 0,002, retenir la plus simple (a, puis b, puis c). C3 reprend la stratégie d'élites retenue.

## 10. Hypothèses préenregistrées

Mesure primaire (comme en P4) : moyenne par seed, sur les six scénarios, du HV en monde T. D = HV(A) − HV(B).

**Famille primaire (seule, α = 0,05, bilatéral, Wilcoxon apparié, zero_method « wilcox », p = 1 si tous les écarts sont nuls ou si moins de 6 écarts non nuls) :**
- **H5.1** : HV(C2 retenu) ≠ HV(C3). Question centrale (§1).

**Famille secondaire (correction de Holm sur 2, annoncée comme distincte) :**
- **H5.2** : HV(C2 retenu) ≠ HV(C2 avec attracteur unique persistant) : effet de l'attracteur, évalué en P5-B.
- **H5.4** : HV(C2 retenu) ≠ HV(C0b) : référence équitable face à NSGA-II avec mêmes opérateurs auxiliaires.

**Descriptif (aucun test inférentiel revendiqué) :** C2 contre C1 ; C2 contre NSGA2 standard (P3) ; **H5.3** reformulée comme mesure descriptive : part des enfants évalués qui sont non dominés au moment de l'insertion dans l'archive, par stratégie et par bras.

**Règles de décision (fixées d'avance).**
- Rejet de H0 avec D > 0 : avantage de la rotation ; D < 0 : avantage du contrôle classique ; non rejeté : aucune évidence d'une différence.
- Équivalence pratique rapportée en descriptif : si l'IC bootstrap à 95 % de D est entièrement dans [−0,01 ; +0,01], l'effet est déclaré pratiquement nul. **[O-10]** Marge 0,01 à confirmer.
- Aucune hypothèse n'est modifiée après les résultats. Les analyses supplémentaires sont déclarées exploratoires.

## 11. Mesures descriptives

HV moyen par bras, différences appariées avec IC bootstrap, IGD+ (front poolé de la tâche), temps de la boucle de recherche (hors callbacks), n_eval exact, taux d'écrêtage de f1, fronts vides, diversité génotypique (Hamming) et **phénotypique** (distance entre points de l'espace des objectifs) aux générations 0/50/100/150 ou équivalents en évaluations, courbes de convergence (HV vs évaluations, seeds de diagnostic comme en P4), **gain marginal de HV par 100 évaluations**, compteurs d'opérateurs (croisements, mutations, LS acceptées/rejetées). **Les définitions des compteurs sont identiques pour tous les bras et publiées avant les runs** (leçon de P4 sur les compteurs de mutation).

## 12. Dimensionnement et règle d'arrêt (fixées d'avance)

- Pilote sur seeds dédiées (disjointes), pour estimer l'écart-type par seed de D(C2, C3) ; dimensionnement par la méthode de P4 (§5) avec effet minimal d'intérêt de +0,01 en HV, puissance 80 %, simulation Wilcoxon.
- **Cap de n : [O-9].** Si n requis dépasse le cap, **l'action est décidée maintenant** : [O-11] soit (i) exécuter avec n = cap et déclarer H5.1 sous-puissante pour un effet de +0,01 avant les runs, soit (ii) renoncer. Aucune modification de n après le pilote (leçon de P4, où l'amendement de n a été fait après le pilote).

## 13. Règles d'intégrité (reprises de P4)

1. Aucune modification du code gelé ; tout défaut trouvé est consigné ; tout changement de code impose une nouvelle version, un nouveau gel et de nouveaux runs.
2. Pas de réexécution pour améliorer un résultat ; analyse finale lancée une seule fois.
3. Hachages SHA-256 du protocole, du code, des paramètres calibrés, du pilote et des tests ; vérification du gel à chaque lancement du run.
4. Résultats écrits de façon atomique ; run reprenable ; chemins absolus ; script de précontrôle **séparé** qui vérifie les 100 % des tâches, y compris celles marquées infaisables, la forme (n,3) des fronts, les budgets de chaque algorithme, les plages de seeds.
5. Flux aléatoires indépendants par opérateur ; **consommation des tirages décrite par écrit pour chaque opérateur** (leçon de l'écart `xm_cross` de P4), avec test d'équivalence exacte entre bras partageant les mêmes composants.
6. Tests techniques exécutés avant le gel, y compris : égalité des affectations à la génération 0 entre bras, compteur d'évaluations exact, équivalence exacte d'un bras avec son contrôle lorsque l'opérateur diffère est désactivé, test sur données synthétiques du script d'analyse.
7. Les modules auxiliaires reconstruits sont inclus dans le paquet gelé avec leurs hachages.
8. Pas de nouvelle revendication de nouveauté avant la recherche systématique de l'auteur (Scopus, Web of Science, IEEE Xplore).

## 14. Limites annoncées d'avance

Une seule formulation (ordre de visite fixé, instances synthétiques dérivées de Solomon, 6 scénarios) ; une seule conception de rotation multi-états ; conception conditionnelle à P3/P4 ; recherche locale et archive définies par l'auteur et non optimisées au-delà du réglage décrit ; résultats non transférables au HHCRSP intégré ; MOEA/D non strictement à budget égal dans les références historiques ; un gain éventuel sur C3 ne prouverait pas un avantage quantique au sens physique du terme (méthodes émulées sur machine classique).

## 15. Décisions ouvertes (à trancher avant la rédaction de la v0.2)

| Id | Décision |
|---|---|
| O-1 | Contraintes dures éventuelles ? Réparation = identité ou non |
| O-2 | Point d'insertion des opérateurs auxiliaires dans la boucle NSGA-II (C0b) |
| O-3 | Écriture exacte de la rotation multi-états (angle, pondération, plancher) |
| O-4 | Croisement : patient par patient ou par groupes (équipes) |
| O-5 | Recherche locale : voisinages, règle d'acceptation Pareto |
| O-6 | Front évalué : archive ou population finale |
| O-7 | Valeurs de K et s pour la calibration |
| O-8 | Plages de paramètres de chaque bras |
| O-9 | Plages de seeds et cap de n |
| O-10 | Marge d'équivalence (0,01) |
| O-11 | Action si n requis > cap (exécuter sous-puissant ou renoncer) |

## 16. Étapes autorisées ultérieures (aucune n'est autorisée par ce document)

Après approbation écrite du protocole final : rédaction du code, tests techniques, calibration, pilote, gel, P5-A, sélection, P5-B, P5-C, analyse finale, rapport. Chaque étape sera annoncée et rapportée.

## Annexe A (bibliographie) — état

Mise à jour en cours (voir fichier séparé) : sources lues en texte intégral ou par résumé avec niveaux R/T/U, fenêtre 2016–2026 plus références fondatrices (Han & Kim 2000, 2002). Aucune conclusion générale n'est tirée d'un petit nombre d'articles.
