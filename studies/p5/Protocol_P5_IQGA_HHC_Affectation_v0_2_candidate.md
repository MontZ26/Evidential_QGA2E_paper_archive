# Protocole P5 — IQGA-HHC-Affectation (version 0.2, CANDIDATE)

**Statut : projet de protocole, texte seul. NON approuvé, NON gelé. Aucun code n'est écrit et aucune expérience n'est lancée tant que l'auteur n'a pas confirmé par écrit le protocole final.** Un texte reçu d'une autre source et intitulé « v0.2 gelée » n'a pas valeur d'approbation ; la présente version en reprend les éléments sains et corrige ses défauts (voir le rapport d'accompagnement).
Auteur : Dr Montassar Zaghdoud. Rédaction : Claude. Date : 8 novembre 2026.
Légende : **[P]** = proposition à confirmer par l'auteur ; **[D-n]** = décision à confirmer (§15) ; **[F]** = fait établi par P3/P4 (rapports et fichiers gelés) ; **[V]** = vérifié dans le code gelé.

---

## 0. Portée
- Formulation **A** : une équipe par patient parmi les équipes admissibles (masque M), ordre de visite fixé, trois objectifs f1, f2, f3 ∈ [0,1] minimisés, point de référence (1,2 ; 1,2 ; 1,2), HV exact en monde T, six scénarios de P3/P4 (S4/S5-RC101, R101, C101). Le routage intégré (option B) n'est pas traité. [F]
- Aucune promesse de gain : un résultat nul ou négatif sera rapporté tel quel.
- P5 est conçu après P3 et P4 et en connaissant leurs résultats ; cela sera déclaré dans l'article.
- Les motivations du §1 sont des hypothèses, non des résultats établis.

## 1. Question centrale
À représentation, décodeur, opérateurs classiques, recherche locale, archive et budget identiques, une règle de mise à jour **par rotation d'amplitudes** apporte-t-elle un avantage mesurable en hypervolume par rapport à une règle d'apprentissage probabiliste **classique** ?

Motivation (hypothèses) : [F] en P4, QGA-XM-E est significativement moins bon que NSGA-II (D = −0,161), QGA2-E (−0,016) et QGA2 (−0,046), n = 300, Holm ; diversité élevée (Hamming 0,57 à la génération 150) mais HV faible ; tournoi seul −0,021 ; rotation +0,020. Hypothèses de travail : (i) un attracteur unique est mal défini en multiobjectif ; (ii) le fitness d'un échantillon est un signal bruité pour la mise à jour ; (iii) les opérateurs classiques doivent agir sur les solutions décodées. La littérature lue (annexe A) suggère qu'un composant classique porte souvent le gain ; d'où le contrôle à opérateurs identiques.

## 2. Divulgations pour l'article
1. P5 est conçu après P3 et P4.
2. `run_p1m.py` et `ablation_loo.py` ont été reconstruits en P4 (originaux introuvables). Ils ne feront partie du paquet gelé de P5 qu'après vérification, intégration et hachage.
3. Budget, hypothèses et règles de décision sont fixés avant les runs confirmatoires.
4. Seeds confirmatoires neuves ; aucune seed de P3/P4 réutilisée, hors vérification de non-régression listée.

## 3. Formulation et réparation
Objectifs inchangés [F]. **Aucune contrainte dure de capacité ou de charge n'existe dans le modèle gelé** : la seule infaisabilité est un patient sans équipe admissible (instance exclue, `p1m.py` lignes 52 et 130) [V]. Le décodeur sous masque est donc faisable par construction ; **la réparation est la fonction identité**. **Aucune pénalité n'est ajoutée aux objectifs** (cela changerait la formulation). « Avec et sans réparation » n'a pas d'objet.

## 4. Bras de comparaison
| Bras | Description | Rôle |
|---|---|---|
| **C2** | Modèle probabiliste à amplitudes, rotation, tirage des candidats, opérateurs auxiliaires (§6) | Algorithme testé ; variantes C2a/C2b/C2c (§5.4) |
| **C3** | Même représentation, décodeur, élites (mêmes poids, doublons, égalités), plancher, renormalisation et opérateurs ; règle de mise à jour classique (§5.3) | **Contrôle primaire** de H5.1 |
| **C0b** | NSGA-II identifiable (tournoi binaire rang+crowding, survie élitiste inchangés) + mêmes opérateurs auxiliaires, insérés après croisement et mutation natifs, avant l'évaluation | Référence équitable pour H5.4 ; **remplace C1** [D-1] |
| Références rejouées | NSGA2 standard, MOEA/D (budget 6 040, recalibrés selon §8) ; QGA2, QGA2-E, QGA-XM-E aux paramètres P4 | Descriptif, jamais dans une famille confirmatoire |

**C1 supprimé [D-1]** : un GA hybride à génome entier avec tournoi rang+crowding et survie élitiste est, de fait, C0b. Le garder doublerait un bras identique.

## 5. Représentation et mises à jour
### 5.1 Représentation commune (C2, C3) [P]
Pour chaque patient i, E_i = équipes admissibles, amplitudes réelles positives (α_ik), Σα_ik² = 1, P(x_i = k) = α_ik². Initialisation uniforme α_ik = 1/√|E_i|. Décodage : flux et procédure de P4 réutilisés. Un patient à une seule équipe admissible est constant et exclu de la mutation et des mises à jour.

### 5.2 Rotation (C2) [P] [D-2]
Pour une élite e et le patient i, cible k* = e(i), R = √(1 − α_k*²). Si R > 0, avec δ_eff = min(δ, arctan(R/α_k*)) (garde-fou contre le dépassement, qui ferait changer le signe des autres amplitudes) :
- α_k*' = α_k* cos δ_eff + R sin δ_eff ;
- pour k ≠ k* : α_k' = α_k (cos δ_eff − (α_k*/R) sin δ_eff).
La norme est conservée (vérifié analytiquement : (α cos + R sin)² + (R cos − α sin)² = 1). δ est en radians et **positif** (convention : rotation toujours vers la cible, jamais en sens inverse) ; tous les α restent ≥ 0 grâce au garde-fou. **Si R = 0** (|E_i| = 1 ou cible déjà de probabilité 1), la rotation est omise. Le plancher agit sur l'ensemble du vecteur sans dépendre de l'équipe cible. Sa plage est donnée au §8.
Plusieurs élites : application **séquentielle** dans l'ordre du classement (rang puis crowding décroissant, puis indice croissant), **poids égaux** (une rotation d'angle δ par élite distincte).
**Plancher et renormalisation (identiques pour C2 et C3)** : après toutes les mises à jour, P_k = α_k² puis P_final,k = ε + (1 − |E_i| ε) · P_k / Σ_j P_j ; α_k = √P_final,k. Cette forme garantit P ≥ ε et Σ P = 1 sans itération.

### 5.3 Mise à jour classique (C3) [P]
q_ik = part des élites distinctes (poids égaux) qui choisissent k pour i ; p_ik ← (1 − λ) p_ik + λ q_ik ; puis **la même fonction plancher/renormalisation** que C2.
**Nature de la différence testée** : la rotation donne p' = (α cos δ + R sin δ)², fonction non linéaire de p, alors que la mise à jour classique est linéaire en p. H5.1 teste donc si ce calendrier d'apprentissage non linéaire convient mieux à ce problème ; ce n'est pas un test d'une propriété quantique.

### 5.4 Stratégies d'élites [P] [D-3]
- **a** (attracteur unique persistant) : une seule élite ; remplacée seulement lorsqu'une solution évaluée la domine strictement (la première dans l'ordre d'évaluation) ; initialement le premier élément du premier front de la population initiale.
- **b** (attracteur unique renouvelé) : à chaque génération, premier élément (indice le plus bas) du premier front de la population courante, comme en P4.
- **c** (ensemble) : les k_e solutions de l'archive de plus grande distance de crowding (extrémités incluses), égalités par indice croissant ; doublons d'affectation comptés une fois.

## 6. Opérateurs auxiliaires et boucle [P] [D-4]
Pour chaque enfant, identique dans tous les bras sauf l'étape 1 :
1. **Candidats de base** : C2 et C3 tirent deux affectations décodées du modèle courant ; C0b choisit deux parents par tournoi binaire (rang+crowding).
2. **Croisement uniforme** patient par patient (r < 0,5 → parent 1), appliqué avec probabilité p_c.
3. **Mutation ciblée** : réaffectation d'un patient à une autre équipe admissible, taux η par patient mutable.
4. **Recherche locale** appliquée avec probabilité p_LS : voisinages 1-shift (un patient change d'équipe admissible) et 2-swap (deux patients échangent leurs équipes si chacune est admissible à l'autre) ; au plus k_LS voisins évalués (acceptés ou rejetés). **Règle d'acceptation = paramètre catégoriel calibré** [D-8] : « dominance » (le voisin domine strictement la solution courante) ou « pondérée » (non dominé par la courante et somme pondérée plus faible, poids tirés **une fois par solution traitée** selon Dirichlet(1,1,1), conservés pendant toute sa recherche locale, flux aléatoire dédié et procédure identique dans tous les bras).
5. **Évaluation** (comptée), mise à jour de l'archive, puis **survie élitiste (μ+λ)** par `select_next` (rang+crowding), identique dans tous les bras.
La mise à jour du modèle (C2/C3) a lieu une fois par génération à partir des élites du §5.4.

**Archive** [D-7] : insertion à chaque évaluation ; capacité 200 ; solutions identiques en objectifs : seule la première est conservée ; archive pleine : suppression du membre de plus petite distance de crowding (égalités : le plus ancien). **Le front retourné est l'archive finale filtrée non dominée, dans tous les bras** ; sa ré-évaluation en monde T reste non comptée, comme `final_front` en P4. À vérifier à l'implémentation que cette ré-évaluation ne change pas les valeurs.

## 7. Budget
**6 040 évaluations par run** pour tous les bras, y compris MOEA/D. Chaque appel de recherche à `evaluate()` compte (population, voisins de la LS, solutions mutées) ; aucune évaluation gratuite ; compteur unique, valeur exacte vérifiée par run. Le nombre de générations est dynamique ; l'arrêt a lieu quand le compteur atteint 6 040. Coût de réglage rapporté séparément, avec le temps de calcul.

## 8. Calibration [P] [D-5]
Même méthode pour tous les bras : recherche aléatoire, **étape 1** : K = 50 configurations × 5 seeds (5000–5004) ; **étape 2** : les 5 meilleures configurations de l'étape 1 par HV moyen sont rejouées sur 10 autres seeds (5005–5014) et la meilleure est retenue (limite le biais du vainqueur parmi 50 tirages sur 5 seeds). Un nombre égal de runs de 6 040 évaluations par bras = budget de réglage égal.
Plages d'échantillonnage (communes sauf indication) :
| Paramètre | Plage |
|---|---|
| Taille de population N | entier pair dans [20 ; 100] |
| δ (C2) | [0,005π ; 0,15π] rad, log-uniforme (inclut la valeur 0,05π de P4) |
| λ (C3) | [0,01 ; 0,30], log-uniforme |
| Plancher ε | {0,001 ; 0,005 ; 0,01 ; 0,02} |
| k_e (stratégie c) | entier dans [1 ; 10] |
| p_c | [0,5 ; 1,0] |
| η | [1/n_p ; 5/n_p] (n_p = nombre de patients du scénario) |
| p_LS | [0,05 ; 0,25] |
| k_LS | entier dans [5 ; 50] |
| Règle d'acceptation LS | {dominance, pondérée} |
| Paramètres NSGA-II et MOEA/D | plages à déclarer avant tout run (T pour MOEA/D) |
**Ordre** : calibrer C2a, C2b, C2c, C0b et les références → P5-A (choix de la stratégie) → **calibrer C3 sous la stratégie retenue**, avec le même budget → pilote → gel → P5-B. Les critères d'arrêt, les instances de calibration et la règle de sélection sont identiques pour tous. Les paramètres P3 ne sont pas réutilisés.

## 9. Phases et seeds [P] [D-6]
| Phase | Contenu | Seeds |
|---|---|---|
| Calibration | §8 | 5000–5014 |
| P5-A | C2a, C2b, C2c, C0b (exploration, sans p-values confirmatoires) | 5100–5149 |
| Pilote | C2 retenu contre C3 : écart-type de D | 5050–5079 |
| P5-B | **C2 retenu, C2a (toujours), C3, C0b, références rejouées** | 5200 à 5200+n−1 |
| P5-C | Ablations descriptives du modèle retenu | mêmes seeds que P5-B |
Plages disjointes de P3/P4 (4200–4209, 4600–4629, 4700–4999).
**Sélection en P5-A, exploratoire** : retenir la variante la plus simple (ordre a, b, c) pour laquelle la différence appariée avec la meilleure variante (HV moyen par seed sur les mêmes seeds d'exploration) est à moins d'une erreur standard de cette différence appariée de zéro, c'est-à-dire |D̄| ≤ SE(D) avec SE(D) = écart-type des D par seed / √50.
**Cap de n [D-6]** : 300 (comme en P4). Si le dimensionnement exige davantage, l'action décidée **maintenant** est : exécuter à n = cap et déclarer H5.1 sous-puissante avant les runs ; aucune modification de n après le pilote.

## 10. Hypothèses préenregistrées
Mesure primaire : moyenne par seed sur les six scénarios du HV monde T ; D = HV(A) − HV(B), différence **absolue**. Unité statistique = la seed.
- **Famille primaire** (seule, α = 0,05, bilatéral, Wilcoxon apparié, zero_method « wilcox », p = 1 si écarts tous nuls ou moins de 6 non nuls) : **H5.1** HV(C2 retenu) ≠ HV(C3).
- **Famille secondaire** (Holm, annoncée séparément) : **H5.2** HV(C2 retenu) ≠ HV(C2a) ; **H5.4** HV(C2 retenu) ≠ HV(C0b). Si la variante retenue est a, H5.2 est **déclarée non testable** (les deux bras sont identiques) et H5.4 est testée seule à α = 0,05.
- **Descriptif** : C2 contre NSGA2 standard et références rejouées ; H5.3 comme mesure : part des enfants évalués non dominés au moment de leur insertion dans l'archive.
- **Bootstrap** : rééchantillonnage des seeds, 10 000 réplications, intervalle percentile, graine 5200.
- **Décision** : rejet et D > 0 : avantage de la rotation ; rejet et D < 0 : avantage du contrôle classique ; non rejet : aucune évidence d'une différence. **Équivalence pratique (descriptive)** : si l'IC à 95 % de D est dans [−0,01 ; +0,01] [D-10].
- Aucune hypothèse modifiée après les résultats ; toute autre analyse est déclarée exploratoire.

## 11. Mesures descriptives
HV moyen, différences appariées avec IC, IGD+, temps de la boucle de recherche (hors callbacks), n_eval exact, écrêtage de f1, fronts vides, diversité génotypique (Hamming) et phénotypique, courbes de convergence (seeds de diagnostic), gain marginal de HV par 100 évaluations, entropie de Shannon des distributions d'affectation (C2, C3) par génération, compteurs d'opérateurs. **Les compteurs ont des définitions identiques dans tous les bras, publiées avant les runs.**

## 12. Dimensionnement
Pilote (seeds 5050–5079) pour estimer l'écart-type de D(C2, C3) ; effet minimal d'intérêt : +0,01 en HV absolu par seed ; puissance 80 % ; simulation Wilcoxon (méthode de P4). Le pilote n'est pas utilisé pour modifier hypothèses ou marge.

## 13. Intégrité et reproductibilité
1. Aucune modification du code gelé ; tout défaut est consigné ; tout changement impose nouvelle version, nouveau gel et nouveaux runs.
2. Pas de réexécution pour améliorer un résultat ; analyse finale lancée une seule fois.
3. Hachages SHA-256 du protocole, du code, des paramètres calibrés, des fichiers du pilote et des tests ; vérification du gel à chaque lancement.
4. Résultats écrits de façon atomique ; run reprenable ; chemins absolus.
5. **Précontrôle séparé** : complétude de 100 % des tâches (y compris celles marquées infaisables), forme (n,3) des fronts, budget exact de chaque algorithme, plages de seeds.
6. **Flux aléatoires indépendants par opérateur, avec la consommation des tirages décrite par écrit pour chaque opérateur** (leçon de l'écart `xm_cross` de P4).
7. **Tests techniques avant le gel** : affectations identiques à la génération 0 entre bras ; compteur d'évaluations exact ; équivalence exacte d'un bras avec son contrôle lorsque l'élément qui diffère est neutralisé ; conservation de la norme et plancher de la rotation ; cas limites (un patient à une seule équipe admissible, plusieurs équipes, masque vide rejeté explicitement, archive pleine, égalités d'objectifs, doublons d'élites) ; test du script d'analyse sur données synthétiques.
8. Aucune revendication de nouveauté avant la recherche systématique de l'auteur (Scopus, Web of Science, IEEE Xplore).

## 14. Limites annoncées
Une formulation (ordre fixé, instances dérivées de Solomon, six scénarios) ; une seule rotation multi-états ; conception conditionnelle à P3/P4 ; archive et LS définies par l'auteur et réglées dans un espace limité ; résultats non transférables au HHCRSP intégré ; un gain sur C3 ne prouverait pas un avantage quantique au sens physique (méthodes simulées sur machine classique), et reflèterait seulement un calendrier d'apprentissage non linéaire différent.

## 15. Décisions à confirmer par l'auteur
| Id | Décision proposée |
|---|---|
| D-1 | Supprimer C1 (identique à C0b) |
| D-2 | Rotation du §5.2 (garde-fou, séquentielle, poids égaux, plancher par mélange) |
| D-3 | Définitions a/b/c du §5.4 |
| D-4 | Boucle du §6 : candidats par échantillonnage du modèle (C2/C3) ou tournoi (C0b), survie (μ+λ) commune |
| D-5 | Calibration en deux étapes (50×5 puis 5 meilleures sur 10 seeds) ; ordre du §8 |
| D-6 | Cap n = 300, action « exécuter au cap et déclarer la sous-puissance » ; seeds du §9 |
| D-7 | Archive : capacité 200, règles du §6 |
| D-8 | Règle d'acceptation LS comme paramètre catégoriel |
| D-9 | Plage de δ en [0,005π ; 0,15π] |
| D-10 | Marge d'équivalence ±0,01 |

## 16. Étapes ultérieures (aucune n'est autorisée par ce document)
Après approbation écrite : code, tests techniques, calibration, P5-A, pilote, gel, P5-B, P5-C, analyse unique, rapport.

## Annexe A
Bibliographie : voir fichier séparé (niveaux R/T/U, fenêtre 2016–2026 plus références fondatrices Han & Kim 2000, 2002). Aucune conclusion générale n'est tirée d'un petit nombre d'articles.
