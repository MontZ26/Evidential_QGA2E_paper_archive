# Protocole P5 — IQGA-HHC-Affectation (version 0.3)

**Statut : GELÉ (SHA-256 consigné dans le fichier p5_protocol_v03_hash.txt) sur autorisation écrite de l'auteur.** Message de l'auteur du 8 novembre 2026, 10:32 (Africa/Lagos) : « Je valide les 14 décisions et je suis d'accord, continuer sans arrêt en passant par l'exécution du code et même l'étape confirmatoire ». Les 14 décisions sont D-1 à D-10 de la v0.2 et D-11 à D-14 (v0.3, ci-dessous). Les valeurs concrètes que cette version fixe sans que l'auteur les ait vues sont listées au §16 (choix d'implémentation) et seront déclarées dans l'article.
Auteur : Dr Montassar Zaghdoud. Rédaction : Claude. Date : 8 novembre 2026.
Légende : [F] fait établi par P3/P4 ; [V] vérifié dans le code gelé de P4.

## 0. Portée
Formulation **A** : une équipe par patient parmi les équipes admissibles (masque M), ordre de visite fixé, trois objectifs f1, f2, f3 ∈ [0,1] minimisés, point de référence (1,2 ; 1,2 ; 1,2), HV exact en monde T, six scénarios de P3/P4 (S4/S5 × RC101, R101, C101). Routage intégré non traité. Aucune promesse de gain ; résultats nuls ou négatifs rapportés tels quels. P5 est conçu après P3 et P4 et en connaissant leurs résultats.

## 1. Question centrale
À représentation, décodeur, opérateurs classiques, recherche locale, archive et budget identiques, une règle de mise à jour **par rotation d'amplitudes** apporte-t-elle un avantage en HV sur une règle **classique** (PBIL) ? Les motivations (échec de QGA-XM-E en P4 : D = −0,161 contre NSGA-II ; hypothèses : attracteur unique mal défini en multiobjectif, signal de fitness bruité, opérateurs devant agir sur solutions décodées) sont des **hypothèses**, non des résultats établis.

## 2. Divulgations
1. P5 est conçu après P3/P4. 2. `run_p1m.py` et `ablation_loo.py` sont des reconstructions de P4 (originaux introuvables), hachés dans le paquet gelé. 3. Budget, hypothèses et règles de décision fixés avant les runs confirmatoires. 4. Seeds neuves ; aucune seed de P3/P4 réutilisée hors vérification de non-régression listée au §13.

## 3. Formulation et réparation
Objectifs inchangés [F]. Pas de contrainte dure de capacité ou de charge dans le modèle gelé ; seule infaisabilité : patient sans équipe admissible, instance exclue [V]. Décodage sous masque faisable par construction : **réparation = identité**, **aucune pénalité**. Un masque vide est rejeté explicitement (jamais transformé en affectation).

## 4. Bras
| Bras | Description | Rôle |
|---|---|---|
| C2 (a/b/c) | Modèle à amplitudes, rotation, candidats tirés du modèle, opérateurs auxiliaires | Algorithme testé |
| C3 | Même représentation, décodeur, élites, plancher/renormalisation, opérateurs ; mise à jour PBIL | Contrôle primaire |
| C0b | NSGA-II identifiable (tournoi binaire rang+crowding, survie (μ+λ)) + mêmes opérateurs auxiliaires | Référence pour H5.4 |
| NSGA2, MOEAD | Implémentés dans le moteur P5, budget 6 040, recalibrés (§8) ; sans LS | Références |
| QGA2, QGA2-E, QGA-XM-E | Code et paramètres gelés de P4 rejoués, budget 6 040, sortie native de P4 | Références descriptives |
C1 supprimé (identique à C0b) [D-1]. Aucune référence n'entre dans une famille confirmatoire.

## 5. Représentation et mises à jour
**5.1** Patient i, E_i équipes admissibles, amplitudes α_ik ≥ 0, Σα² = 1, P(x_i = k) = α_ik². Initialisation uniforme. Patient à une seule équipe : constant, exclu de la mutation et des mises à jour.
**5.2 Rotation (C2) [D-2]** : cible k* = e(i), R = √(1 − α_k*²). Si R > 0 : δ_eff = min(δ, atan2(R, α_k*)) ; α_k*' = α_k* cos δ_eff + R sin δ_eff ; pour k ≠ k* : α_k' = α_k (cos δ_eff − (α_k*/R) sin δ_eff). δ > 0 en radians. Si R = 0 : omise. Quand δ_eff atteint la borne, les autres amplitudes s'annulent avant le plancher (effet documenté). Plusieurs élites : application **séquentielle** par élite distincte, dans l'ordre rang croissant (meilleur d'abord), puis crowding décroissant, puis indice croissant, **poids égaux** ; deux élites visant la même équipe pour un patient produisent deux rotations vers cette équipe (**intentionnel**).
**Plancher et renormalisation (C2 et C3)** appliqués une fois par génération après toutes les mises à jour : P_k = α_k² ; P_final,k = ε + (1 − |E_i| ε) P_k/Σ_j P_j ; α_k = √P_final,k. L'algorithme C2 est donc « rotation suivie d'une projection probabiliste ».
**5.3 PBIL (C3)** : q_ik = part des élites **distinctes** choisissant k ; p ← (1 − λ) p + λ q ; puis la même fonction plancher. La différence testée est un calendrier de mise à jour non linéaire (rotation) contre linéaire ; ce n'est pas un test de propriété quantique.
**5.4 Élites [D-3]** : **a** persistante (une élite, remplacée dès qu'une solution évaluée la domine strictement, première dans l'ordre chronologique d'évaluation ; initiale = premier élément du premier front de la population initiale) ; **b** renouvelée (premier élément, indice le plus bas, du premier front de la population après survie) ; **c** ensemble : les k_e membres de l'archive de plus grande distance de crowding (extrémités incluses ; égalités par indice croissant d'insertion), doublons d'affectation comptés une fois.

## 6. Boucle [D-4, D-12, D-13]
Population évaluée de taille N (μ = λ = N), maintenue dans **tous** les bras. **Population initiale commune** à tous les bras : N affectations tirées uniformément parmi les équipes admissibles par le flux dédié « init » (tirage de 100 lignes, N premières utilisées) ; comptée dans le budget.
Par génération, N enfants produits **séquentiellement** :
1. Candidats de base : C2/C3 tirent deux affectations décodées du modèle courant ; C0b/NSGA2 choisissent deux parents par tournoi binaire (rang puis crowding, égalités aléatoires).
2. Croisement uniforme avec probabilité p_c (tirage r < 0,5 → parent 1, par patient).
3. Mutation ciblée : chaque patient mutable est réaffecté avec probabilité η = η_k/n_p à une autre équipe admissible tirée uniformément.
4. **Évaluation** de l'enfant (comptée) et insertion dans l'archive.
5. **Recherche locale** avec probabilité p_LS (tirage de porte toujours effectué) : point de départ = l'enfant évalué ; solution courante = dernière solution acceptée. Les mouvements sont l'union des 1-shift (patient, équipe admissible différente) et des 2-swap (paire de patients d'équipes différentes, chacun admissible à l'équipe de l'autre), parcourus dans un ordre aléatoire sans remise (flux dédié), appliqués à la solution courante ; un mouvement sans effet sur la courante est ignoré sans évaluation ; au plus k_LS mouvements évalués (acceptés ou rejetés) ; chaque voisin évalué entre dans l'archive. Règle « **dominance** » : accepté si au moins un objectif est strictement meilleur et aucun moins bon. Règle « **pondérée** » : accepté si la courante ne domine pas le voisin ET si w·f(voisin) < w·f(courante) strictement ; w ~ Dirichlet(1,1,1) tiré **une fois par solution traitée**, flux dédié ; le tirage est effectué quelle que soit la règle. Acceptation par première amélioration. La solution finale de la LS (ou l'enfant si rien n'est accepté) entre dans le pool de survie ; l'enfant initial reste dans l'archive.
6. Après les N enfants : survie (μ+λ) par `select_next` (rang+crowding) sur population + pool ; mise à jour du modèle (C2/C3) une fois par génération à partir des élites du §5.4.
**Budget [D-12]** : compteur unique ; avant chaque évaluation, arrêt strict si le compteur est à 6 040. La LS est interrompue ; la dernière génération, éventuellement partielle, passe en survie avec ce qui est évalué ; aucune mise à jour du modèle après la dernière génération (sans effet sur la sortie, qui provient de l'archive).
**Archive [D-7]** : reçoit la population initiale et **chaque** solution évaluée, y compris les voisins de LS rejetés ; capacité 200 ; une solution dominée par un membre ou identique en objectifs n'est pas insérée (la première est conservée) ; les membres qu'elle domine sont supprimés ; si > 200, on supprime le membre de plus petite distance de crowding (égalité : le plus ancien). **Le front final est l'archive finale**, avec les objectifs stockés (évaluation déjà en monde T) ; aucune ré-évaluation. Test pré-gel : égalité exacte avec la ré-évaluation de P4 (`final_front`). Pour QGA2, QGA2-E et QGA-XM-E (code P4 gelé) la sortie native de P4 est conservée.

## 7. Budget
6 040 évaluations par run pour tous les bras (y compris MOEA/D), `evaluate()` compté une seule fois par appel de recherche. n_eval exact vérifié par run.

## 8. Calibration [D-5, D-11]
Recherche aléatoire par bras ; **étape 1** : 50 configurations × 5 seeds (5000–5004) ; **étape 2** : les 5 meilleures (HV moyen) rejouées sur 10 seeds (5005–5014) ; la meilleure sur ces 10 seeds est retenue. **Instances de calibration : les trois scénarios S4** (S4-RC101, S4-R101, S4-C101) pour tous les bras. Les 50 configurations de chaque bras sont tirées par un générateur initialisé par le nom du bras (crc32 de « calib|bras »), dédoublonnées (configuration identique après arrondi : retirage). C3 reçoit exactement le même processus (50 × 5 puis 5 × 10), sous la stratégie retenue en P5-A.
| Paramètre | Plage | Bras |
|---|---|---|
| N | entier pair [20 ; 100] | tous sauf MOEAD |
| δ | [0,005π ; 0,15π] log-uniforme | C2 |
| λ | [0,01 ; 0,30] log-uniforme | C3 |
| ε | {0,001 ; 0,005 ; 0,01 ; 0,02} | C2, C3 |
| k_e | entier [1 ; 10] | C2c, C3c |
| p_c | [0,5 ; 1,0] | tous |
| η_k | [1 ; 5] (η = η_k/n_p) | tous |
| p_LS | [0,05 ; 0,25] | C2, C3, C0b |
| k_LS | entier [5 ; 50] | C2, C3, C0b |
| règle LS | {dominance, pondérée} | C2, C3, C0b |
| MOEAD : H (vecteurs de poids, N = (H+1)(H+2)/2) | {6, 8, 10, 12} | MOEAD |
| MOEAD : T (voisinage) | entier [5 ; 20] | MOEAD |
| MOEAD : remplacement max, probabilité de voisinage | 2 ; 0,9 (fixes) ; décomposition de Tchebychev | MOEAD |
**Ordre** : calibrer C2a, C2b, C2c, C0b, NSGA2, MOEAD → P5-A → calibrer C3 → pilote → gel → P5-B. Les paramètres P3/P4 ne sont pas réutilisés pour les bras P5. Coût de réglage rapporté.

## 9. Phases et seeds [D-6, D-14]
Calibration 5000–5014 ; pilote 5050–5079 ; P5-A 5100–5149 ; P5-B 5200…5200+n−1 ; P5-C : les 100 premières seeds de P5-B ; tests techniques 5900–5909 ; **graine d'analyse du bootstrap 9001** [D-14]. Plages disjointes de P3/P4.
**P5-A (exploratoire, sans p-values)** : C2a, C2b, C2c, C0b sur 50 seeds × 6 scénarios, paramètres calibrés. Sélection : variante la plus simple (a, b, c) avec |D̄| ≤ SE(D), D = HV(meilleure variante) − HV(variante) par seed, SE = sd(D)/√50.
**Pilote** : C2 retenu contre C3 calibré, 30 seeds × 6 scénarios. **Dimensionnement** (méthode de P4) : effet minimal 0,01 en HV absolu ; n_f = ⌈((z_{0,975} + z_{0,80}) sd_haut/0,01)²⌉ avec sd_haut borne supérieure à 80 % (khi-deux) ; simulation de puissance (1 500 rééchantillonnages des écarts centrés sur la médiane, décalage +0,01, Wilcoxon bilatéral à 0,05) sur la grille {100, 150, 200, 300} ; n = plus petite valeur de grille ≥ max(n_f, n_s). **Cap 300** : si n > 300, exécuter 300 et déclarer H5.1 sous-puissante ; jamais d'augmentation du cap.
**P5-B** : C2 retenu, C2a (si différent), C3, C0b, NSGA2, MOEAD, QGA2, QGA2-E, QGA-XM-E (P4) sur n seeds × 6 scénarios. **P5-C (descriptif)** : C2, C3 et C0b sans LS (p_LS = 0, autres paramètres inchangés) sur les 100 premières seeds de P5-B.
Une seed est exclue de l'analyse si l'un de ses six scénarios est infaisable (liste publiée) ; si plus de 5 % des seeds sont exclues, signalement.

## 10. Hypothèses préenregistrées
Mesure : moyenne par seed sur les six scénarios du HV (monde T) ; D = HV(A) − HV(B), absolue ; unité = la seed. Wilcoxon apparié bilatéral, zero_method « wilcox », p = 1 si écarts tous nuls ou moins de 6 non nuls.
- **Primaire (α = 0,05)** : **H5.1** HV(C2 retenu) ≠ HV(C3).
- **Secondaire (Holm sur 2)** : **H5.2** C2 retenu ≠ C2a (non testable si a est retenu) ; **H5.4** C2 retenu ≠ C0b (alors testée seule à 0,05).
- **Descriptif** : C2 contre NSGA2, MOEAD et références P4 ; **H5.3** = part des enfants évalués qui sont insérés dans l'archive au moment de leur évaluation ; P5-C.
- Bootstrap sur les seeds, 10 000 réplications, percentile, graine 9001. **Équivalence pratique descriptive** : IC 95 % de D dans [−0,01 ; +0,01] [D-10] ; absence de rejet ≠ preuve d'équivalence.
- Décision : rejet et D > 0 : avantage de la rotation ; rejet et D < 0 : avantage du contrôle ; sinon aucune évidence d'une différence. Aucune hypothèse modifiée après les résultats.

## 11. Mesures descriptives
HV, IGD+ (front de référence = non dominés de l'union des bras de la tâche), temps de la boucle de recherche, n_eval, écrêtage de f1, fronts vides, diversité (Hamming, générations 0, 50, 100, 150 équivalentes en évaluations : aux évaluations 40·g), convergence (HV de l'archive toutes les 100 évaluations, 20 premières seeds de P5-B), entropie de Shannon moyenne des distributions d'affectation (C2, C3) toutes les 10 générations, compteurs d'opérateurs de définitions identiques dans tous les bras : enfants créés, croisements effectifs, gènes mutés, LS déclenchées, voisins évalués, voisins acceptés, insertions dans l'archive.

## 12. Intégrité
1. Code, protocole, paramètres calibrés, sorties de pilote et tests hachés SHA-256 ; **gel du code avant la calibration**, vérifié à chaque lancement ; toute modification invalide les données et impose nouvelle version et relance depuis l'origine.
2. Pas de réexécution pour améliorer un résultat ; analyse finale lancée une seule fois.
3. Écriture atomique, runs reprenables, chemins absolus.
4. Précontrôle séparé avant l'analyse : complétude 100 % des tâches (infaisables comptées et listées), forme (n,3), n_eval exact par bras, plages de seeds, gel.
5. Flux aléatoires indépendants par opérateur (init, sampling, tour, tie, cross, mut, ls_gate, ls_order, ls_w), dérivés de (scénario, seed, nom) ; la consommation de chaque flux est décrite dans le code (en-tête de `p5.py`).
6. Un incident (erreur, écart au protocole) est consigné, le run concerné arrêté et rapporté.
7. Aucune revendication de nouveauté avant la recherche systématique de l'auteur.

## 13. Tests techniques pré-gel (`p5_tests.py`, seeds 5900–5909)
Population initiale identique entre bras ; n_eval = 6 040 exact (N = 20 et 100, LS maximale, MOEAD H = 12) ; équivalence exacte C2 (δ = 0) = C3 (λ = 0) ; indépendance des flux (règle LS inopérante si p_LS = 0) ; conservation de la norme et plancher ; garde-fou de δ_eff ; cas limites (équipe unique, masque vide rejeté, archive pleine, égalités d'objectifs, doublons d'élites) ; règles de LS (dominance, pondérée, plafond k_LS) ; égalité exacte archive / ré-évaluation P4 ; non-régression des références P4 (QGA2 sur la seed 4200 contre `p3_pilot.json`) ; script d'analyse sur données synthétiques.

## 14. Limites
Une formulation ; instances dérivées de Solomon ; une géométrie de rotation ; conception conditionnelle à P3/P4 ; archive et LS définies par l'auteur ; calibration sur les trois scénarios S4 seulement (coût de calcul) ; sélection de la stratégie d'élite sur P5-A (trois variantes de C2 contre une de C3) qui peut favoriser légèrement C2 ; plage de δ non démontrée exhaustive ; gain éventuel = calendrier non linéaire, pas avantage quantique physique.

## 15. Décisions D-1 à D-14 — confirmées par l'auteur le 8 novembre 2026
D-1 suppression de C1 ; D-2 rotation ; D-3 élites a/b/c ; D-4 boucle ; D-5 calibration deux étapes (y compris C3) ; D-6 cap 300 ; D-7 archive ; D-8 règles LS ; D-9 plage de δ ; D-10 marge ±0,01 ; **D-11** plages NSGA-II/MOEA/D du §8 ; **D-12** règle de budget partiel du §6 ; **D-13** règle de LS complète du §6 ; **D-14** graine d'analyse 9001.

## 16. Choix d'implémentation introduits par cette version (à déclarer)
Calibration sur les trois scénarios S4 ; P5-C limité aux 100 premières seeds de P5-B ; valeurs des plages de MOEA/D (H, T) ; sortie native des références P4 ; seeds techniques 5900–5909 ; entropie et convergence échantillonnées.
