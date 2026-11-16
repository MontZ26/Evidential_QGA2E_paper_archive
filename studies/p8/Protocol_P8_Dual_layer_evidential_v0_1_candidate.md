# Protocole P8 — Cadre évidentiel à deux couches (données + recherche) pour l'affectation multiobjectif en HHC (v0.1, CANDIDAT)

**Statut : texte candidat. NON approuvé, NON gelé. Aucun code, aucune calibration, aucune allocation de graines, aucun run.**
Rédigé le 8 nov. 2026 à la demande de l'auteur (18:22), à partir de la note conceptuelle P8 v0.1 fournie par l'auteur (rédigée par un autre assistant; entrée, non autorisation),
de P7 v0.3 (SHA-256 4af4f7c4…baf71f, candidat) et des corrections discutées le 8 nov. (étalon commun, ré-établissement de la couche données, puissance de l'interaction, séquencement).
P5-B/P5-C : en cours; aucun résultat confirmatoire lu. P6 et P7 : candidats non approuvés. Cette rédaction n'autorise aucune étape.
**[OUVERT]** = décision écrite de l'auteur requise avant gel.

## 1. Question et contributions à isoler
Un cadre évidentiel à deux couches — (I) incertitude sur l'information du problème, (II) connaissance acquise pendant la recherche — améliore-t-il la qualité, la robustesse et
l'interprétabilité des affectations patient→équipe ? Trois contributions distinctes : (a) preuve sur les données seule; (b) preuve de recherche seule; (c) apport additionnel de leur intégration
(interaction). Une amélioration de l'architecture intégrée n'est attribuable à aucune couche isolément sans ce plan.
Portée : formulation HHC inchangée (3 objectifs à minimiser, ordre de visite fixe, budget d'évaluations strictement compté); routage intégré hors portée.

## 2. Les deux couches
**Couche I (données).** Représente l'incertitude sur compétence des équipes et satisfaction des patients à partir de sources (documents, supervision, historique, votes).
D'après le code existant (lecture partielle, à vérifier) : masses sur {A, non A} par cellule, affaiblissement de Shafer par source, combinaison conjonctive, conflit K enregistré avant transfert, règle de Yager (K→Θ);
mondes d'évaluation nominal (BetP), bas (Bel) et haut (Pl). **Toute définition mathématique, hypothèse de fiabilité des sources et procédure d'évaluation doit être reconstruite et vérifiée contre
l'implémentation d'origine avant le protocole définitif (porte G-D).** Rôle : informer l'évaluation des solutions, pas guider l'échantillonnage.
**Couche II (recherche).** Architecture P7 v0.3 (candidat) : individus comme sources, masses sur les équipes éligibles, règle prudente (primaire) / Dempster (référence), BetP conditionnée, échantillonnage,
contrôle apparié V0c. Sa contribution propre doit d'abord être évaluée sur ses propres termes (G0 puis décision).
**Les deux couches restent distinctes** (cadres, sources, sémantiques, sorties différents). Aucune combinaison de Dempster–Shafer entre elles. Elles sont reliées uniquement par la boucle évaluation→recherche.

## 3. Interface d'intégration
Cycle : (1) évidence sur le problème → représentation tenant compte de l'incertitude; (2) génération de candidats par la recherche; (3) évaluation par la couche I; (4) acquisition d'évidence de recherche à partir des solutions évaluées;
(5) agrégation évidentielle de recherche et échantillonnage; (6) itération jusqu'au budget.
Règles d'interface (à préciser en v0.2) : (i) **non-double comptage** : les observations brutes des données de la couche I ne sont jamais réinjectées comme sources de la couche II; la couche II ne voit que des résultats d'évaluation de solutions;
(ii) **propagation de l'incertitude** : une observation de recherche issue d'objectifs incertains ne doit pas devenir silencieusement équivalente à une observation issue d'objectifs certains — le protocole enregistre le monde d'évaluation utilisé
et ce que la couche II reçoit (objectifs nominaux seuls, ou aussi bornes bas/haut) **[OUVERT P8-D2]** ; (iii) amplification par rétroaction : suivie par diagnostics (population initiale biaisée, concentration du modèle).

## 4. Plan factoriel 2×2 et contrôles appariés
| Architecture | Évidence données | Évidence recherche |
|---|---|---|
| A — Conventionnelle | Non | Non |
| B — Données évidentielles | Oui | Non |
| C — Recherche évidentielle | Non | Oui |
| D — Intégrée | Oui | Oui |
Mêmes instances, mêmes graines (appariement), même budget, mêmes opérateurs auxiliaires, mêmes conditions de calcul.
Contrôles appariés : pour C, le V0c de P7. Pour B, un comparateur qui isole la représentation par fonctions de croyance d'une représentation probabiliste des mêmes sources
(analogue de V0c pour les données : conversion en probabilités de chaque source puis agrégation) **[OUVERT P8-D3]** ; un contrôle apparié pour D est à décider.
Définition précise de A (évaluation conventionnelle : valeurs ponctuelles estimées à partir des mêmes sources, par quelle règle ?) **[OUVERT P8-D4]**.
Comparaisons : B−A, C−A, D−A, D−B, D−C ; interaction I = Y_D − Y_B − Y_C + Y_A (mesurée sur une échelle et dans un sens définis; sa significativité doit être testée, non inférée de D > A).

## 5. Étalon d'évaluation commun (point méthodologique central)
Les architectures B et D optimisent des objectifs évidentiels; A et C des objectifs conventionnels : leurs hypervolumes natifs ne sont pas directement comparables.
Deux niveaux : (1) **évaluation au moment de la recherche** — chaque architecture utilise sa représentation prescrite; (2) **évaluation commune a posteriori** — chaque front final est ré-évalué avec les
valeurs vraies de compétence et de satisfaction (oracle de simulation) sur les mêmes objectifs, même normalisation et même point de référence (1,2;1,2;1,2). Résultat primaire candidat : HV oracle.
L'oracle n'est jamais accessible à l'optimiseur. Il n'existe qu'en simulation : la performance « vérité terrain » est une propriété du dispositif de simulation et ne se transpose pas telle quelle aux déploiements réels,
où l'on évalue sur des résultats observables, des enregistrements disponibles et des mesures d'incertitude/robustesse, sans prétendre à un oracle. Le papier distinguera validation en simulation et évaluation en conditions réelles.
Conséquence technique : l'évaluation commune exige les vecteurs d'affectation des fronts finaux; les shards P5 actuels ne contiennent que les objectifs. Une instrumentation sur copie du moteur sera nécessaire (porte G-Y).
Reste à définir : traitement des trois objectifs sous l'oracle et comparaison de fronts issus de représentations différentes.

## 6. Dimensions d'évaluation
Performance d'optimisation : HV (au moment de la recherche et oracle), convergence, diversité, coût de calcul. Robustesse : sensibilité à l'incertitude des données, stabilité sous preuves incomplètes ou conflictuelles,
stabilité des affectations choisies entre exécutions (HV bas/haut mondes). Qualité de l'évidence : ignorance restante, conflit, sensibilité à la fiabilité des sources, écarts évidentiel vs probabiliste.
Interprétabilité : traçabilité, accord entre évidence du problème et de la recherche, affectations favorisées par la recherche malgré un faible soutien des données. Les métriques non-HV sont descriptives sauf décision contraire.

## 7. Hypothèses (provisoires)
Primaire candidat **[OUVERT P8-D5]** : (a) l'interaction I sur HV oracle (bilatérale, la plus exigeante en puissance) ou (b) D − A sur HV oracle. Famille secondaire (correction préannoncée, Holm candidate) :
B−A, C−A, D−B, D−C. Descriptif : robustesse, ignorance/conflit, traçabilité, surcoût.

## 8. Plan statistique (à figer après les portes)
Appariement par graine et scénario; test candidat bootstrap-t apparié sur la moyenne (comme P6/P7), appliqué au contraste par graine (par exemple Y_D − Y_B − Y_C + Y_A).
**Puissance de l'interaction** : analyse propre; effet scientifiquement significatif minimal à fixer par l'auteur; variance estimée par pilote; dimensionnement qui en résulte (la puissance des effets principaux ne suffit pas). Plafond de n à fixer.
Plages de graines à fixer; proposition non allouée : 8000–8009 pour les contrôles techniques. Aucune augmentation de n après observation du pilote.

## 9. Portes (chacune avec sa propre approbation écrite)
G-P7 : G0 de P7 puis décision de tester ou non la couche II. G-D : reconstruire et vérifier la couche I (masses, règles de combinaison, calculs nominal/Bel/Pl, oracle d'origine, résultats face à un comparateur approprié,
séparation de la contribution des données vs des anciens opérateurs quantiques; le résultat négatif de P4 ne doit pas être attribué à la couche de données). G-I : spécification de l'interface (§3). G-Y : validation de l'étalon oracle et de l'instrumentation.
Sans passage d'une porte, la suite n'est pas engagée; un arrêt est un résultat acceptable.

## 10. Risques et limites
Double comptage; amplification de rétroaction; confusion preuve/fréquence (ascendance commune); propagation de l'incertitude; surcoût; complexité sans sémantique défendable; oracle limité à la simulation; dépendance à P7 non encore validé;
contrôles appariés pour B et D à définir; interaction coûteuse en puissance; nouveauté non établie (recherche systématique Scopus/WoS/IEEE Xplore à faire par l'auteur); conclusions limitées à cette architecture et à ces instances (Solomon dérivées).
Prudence de cadrage : P4 (QGA-XM-E significativement moins bon que NSGA2, QGA2-E, QGA2) ne prédit pas le résultat de P8 et P8 n'est pas présenté comme correction de ce résultat sans preuve expérimentale.

## 11. Séquence et gouvernance
1. Terminer P5-B/P5-C; précheck; analyse unique; rapport final. 2. Décision P6. 3. P7 G0 (si approuvé) et décision. 4. G-D. 5. G-I et G-Y. 6. Approuver et geler P8. 7. Seulement ensuite : implémentation, calibration, pilote, confirmation.
Aucun code, aucun script, aucune graine, aucune exécution n'est autorisé par ce texte. Fichiers gelés P4/P5 inchangés; aucun shard P5 n'est utilisé comme donnée P8.

## 12. Décisions ouvertes
P8-D1 pertinence de poursuivre après G-P7 ; P8-D2 ce que la couche II reçoit des évaluations incertaines ; P8-D3 contrôle apparié de la couche données ; P8-D4 définition de A ;
P8-D5 hypothèse primaire (interaction ou D−A) et effet minimal ; P8-D6 test et dimensionnement ; P8-D7 traitement oracle des trois objectifs et comparaison de fronts.
