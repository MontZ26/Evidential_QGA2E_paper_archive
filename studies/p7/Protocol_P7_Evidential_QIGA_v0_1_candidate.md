# Protocole P7 — Agrégation évidentielle basée sur les individus (v0.1, CANDIDAT)

**Statut : texte candidat. NON approuvé, NON gelé. Aucun code, aucune calibration, aucun run, aucune allocation de graines.**
Rédigé le 8 nov. 2026 à partir (i) de la décision d'architecture écrite de l'auteur (P7_architecture_decision_record_2026-11-08.md,
SHA-256 ab049c19…2021c6) et (ii) de la note conceptuelle fournie par l'auteur, dont le texte reçu s'arrête au §3.1
(« où … »); les parties suivantes de cette note n'ont pas été lues et ne sont donc pas reprises ici.
Les textes d'autres assistants sont des entrées, jamais des autorisations. P5-B est en cours et n'est pas lu; P6 est candidat non approuvé.
Les éléments marqués **[OUVERT]** sont des décisions que l'auteur doit prendre par écrit avant gel; rien n'est supposé.

## 1. Question et portée
Un modèle évidentiel (fonctions de croyance) apporte-t-il un avantage opérationnel sur un modèle probabiliste apparié recevant exactement la même
information et le même budget, en représentant explicitement soutien, ambiguïté, ignorance et conflit ?
Portée : formulation HHC inchangée (affectation patient→équipe éligible, ordre de visite fixe, 3 objectifs à minimiser, HV exact 3D,
point de référence (1.2,1.2,1.2), budget 6040 évaluations strictement comptées). Routage intégré hors portée.
Aucune supériorité « quantique » n'est présupposée; la rotation d'amplitudes de P5 n'est pas reprise (la comparaison pertinente est probabiliste/PBIL).

## 2. Représentation évidentielle
Cadre Θ_i = E_i (équipes éligibles du patient i). Masse m_i : 2^Θ_i → [0,1], m_i(∅)=0, Σ m_i = 1.
Ignorance = masse sur Θ_i. Probabilité d'échantillonnage : pignistique BetP_i(k) = Σ_{A∋k} m_i(A)/|A|, puis plancher ε et renormalisation
comme en P5 (même ε que le comparateur). Le modèle reste factorisé par patient : P7 ne prétend pas résoudre la perte des corrélations inter-patients.

## 3. Décisions d'architecture (écrites par l'auteur, 8 nov. 2026 16:19)
| Élément | Décision |
|---|---|
| Unité d'évidence primaire | Solutions individuelles |
| Règle de combinaison primaire | Règle prudente (cautious) |
| Combinaison de référence | Règle de Dempster |
| Architecture alternative | Masses de grappes d'élites (alternative séparée, non une couche supplémentaire) |
| Évidence par recherche locale | Observations à valeurs ensemblistes, en contexte |
| Évidence négative | Différée |
| Comparateur probabiliste | Information et budget d'évaluations appariés |
Réserve de l'auteur : la règle prudente n'est pas une solution universelle à la dépendance; hypothèses et comportement à examiner (évidence dogmatique, structures focales différentes).

## 4. Construction des masses (par individu j et patient i)
**M1 (mono-équipe).** m(\{x_j(i)\}) = w_j ; m(Θ_i) = 1 − w_j, avec 0 < w_j ≤ w_max < 1 (non dogmatique, requis par la règle prudente).
**M2 (ensembliste, recherche locale).** A_i(x) = \{x_i\} ∪ L_i(x), où L_i(x) = équipes de voisins **évalués** dont le mouvement change l'équipe du
patient i et dont le voisin n'est pas dominé par x. Seuls les mouvements modifiant l'équipe de i sont retenus; le type de mouvement est enregistré.
m(A_i)=w, m(Θ_i)=1−w. S'il n'existe aucune observation éligible : m(Θ_i)=1 (absence d'information, non un échec).
L'évidence est décrite comme « alternatives observées localement en contexte » (le résultat dépend du reste de l'affectation), non comme aptitude intrinsèque de l'équipe.
**Poids w.** **[OUVERT D7-1]** w constant (hyperparamètre calibré sur graines dédiées, avec le même budget de calibration que les comparateurs)
ou fonction du rang de dominance/crowding (jamais la fitness scalaire). Aucun réglage arbitraire hors calibration pré-enregistrée.

## 5. Combinaison
Pour chaque patient, combinaison des masses des individus de la génération t (plus mémoire, voir §6).
- **V2 (primaire) : règle prudente** (minimum des poids de la décomposition canonique). Idempotente : des preuves identiques répétées ne s'accumulent pas.
  Risque falsifiable déclaré : l'idempotence peut effacer l'information de fréquence (30 individus identiques pour A donnent le même soutien qu'un seul);
  avec des ensembles focaux ou poids différents le résultat suit les décompositions canoniques et n'est pas généralisable depuis le cas du soutien simple.
- **V1 (référence) : règle de Dempster**. Conserve l'accumulation (ex. 1−0,2³ = 0,992 pour trois copies), au prix du sur-comptage sous dépendance.
Aucune des deux ne rend les individus indépendants : lignées communes, sélection conjointe. Cette limite est déclarée.

## 6. Boucle algorithmique (reprise de P5, seule la mise à jour du modèle change)
Population initiale commune, enfants générés séquentiellement par échantillonnage du modèle (BetP + plancher) puis mutation ciblée, évaluation, archive
(200, rejet dominé/doublon, crowding), LS optionnelle (1-shift/2-swap, évaluations comptées), survie (μ+λ), mise à jour du modèle une fois par génération
(pas après la dernière), front final = archive, budget strict 6040, génération partielle autorisée. Les opérateurs auxiliaires sont communs à tous les bras.
**Mémoire du modèle [OUVERT D7-2]** : (a) reconstruction à chaque génération à partir de la population courante, ou (b) modèle persistant avec érosion
(affaiblissement des poids) puis combinaison avec la nouvelle évidence. Même choix pour le contrôle apparié.
**Population entière ou élites [OUVERT D7-3]** : source d'évidence = tous les individus (poids selon rang) ou nondominés seulement; famille à un paramètre
(poids 0 pour dominés = « élites seulement »), qui évite une seconde couche d'agrégation et le double comptage population/élites.

## 7. Bras (étape 1)
| Bras | Description | Rôle |
|---|---|---|
| V0 | Meilleur bras probabiliste du rapport final P5 (PBIL ou autre, à fixer après ce rapport) **[OUVERT D7-4]** | Référence établie |
| V0c | Contrôle probabiliste apparié : fréquences pondérées des mêmes observations (M1/M2 réparties uniformément sur A), mêmes poids, même LS, même budget | Isole l'effet de la représentation évidentielle |
| V1 | Évidentiel, Dempster | Référence naïve |
| V2 | Évidentiel, règle prudente | Candidat primaire |
Extensions conditionnelles (hors étape 1, nécessitent décision écrite) : V3 = famille pondérée population/élites; V4 = masses de grappes d'élites
(espace de décision, poids égaux par grappe; l'espace objectif est une alternative distincte). Évidence négative : différée.
Comparateurs externes de contexte : NSGA-II et C0b de P5 (configurations gelées de P5), rapportés à titre descriptif.

## 8. Portes de faisabilité (avant tout bras algorithmique)
**G0 — analyse mathématique (sans expérience).** Comportement de V1/V2 sur les structures de masse réelles : preuves répétées, conflit, ignorance,
perte de fréquence, équivalence éventuelle de BetP avec une fréquence (si BetP ≡ fréquence pondérée, aucune contribution évidentielle ⇒ arrêt).
**G1 — audit instrumenté (nécessite approbation écrite séparée).** Courte exécution sur **copie** du moteur (fichiers gelés P4/P5 intacts, registre des modifications),
journalisant type de mouvement, patient concerné, équipe ancienne/nouvelle, vecteurs d'affectation, objectifs. Les shards existants ne contiennent ni les
mouvements de LS ni les affectations; l'audit ne peut donc pas être rétrospectif. Mesures descriptives : fraction de solutions traitées par LS, fraction de
patients avec ≥1 observation pertinente, nombre moyen d'alternatives distinctes par patient, distribution des tailles d'ensemble, fraction sans évidence,
variation par scénario; distances de Hamming vs distances en espace objectif; part de quasi-doublons.
**Règle de rejet pré-définie [OUVERT D7-5]** : seuil de couverture (à fixer par l'auteur avant G1) en dessous duquel M2 est abandonné, sans modifier w ni
ajouter de sources d'évidence non prévues.
Plage de graines proposée (non allouée) : 7000–7009 pour G1. Aucun lien avec P5-B.

## 9. Hypothèses (provisoires, à figer en v0.2 après G0/G1)
- **H7.1 (primaire)** : HV(V2) − HV(V0c) apparié par graine/scénario, test bootstrap-t apparié sur la moyenne comme P6 (α=0,05) **[OUVERT D7-6]**.
- Famille secondaire Holm : H7.2 V2 vs V1 (règle de combinaison); H7.3 V1 vs V0c; H7.4 V2 vs V0.
- Descriptif : masse d'ignorance, conflit, entropie, divergence BetP–fréquence, couverture, surcoût de calcul, zone d'équivalence ±0,01 non formelle.
Dimensionnement de n par pilote et règle gelée (max des exigences, plafond 300), comme P6; calibration commune aux bras appariés sur graines distinctes
de celles du pilote et de la confirmation. Plages de graines à fixer en v0.2.

## 10. Limites déclarées
Modèle factorisé; dépendance entre individus non éliminée; règle prudente possiblement trop faible comme signal d'apprentissage; couverture de M2
possiblement faible; résultat dépendant du contexte pour M2; un seul type de topologie d'instances (Solomon dérivées); nouveauté non établie
(recherche systématique Scopus/WoS/IEEE Xplore à faire par l'auteur); conclusions limitées à cette architecture.

## 11. Gouvernance et séquence
1. Rapport final P5 puis décision sur P6 (inchangé). 2. Approbation écrite des décisions D7-1…D7-6 et de la v0.2 gelée.
3. G0, puis approbation de G1, puis G1. 4. Seulement ensuite : code des bras, calibration, pilote, confirmation.
Rien dans ce texte n'autorise du code, des graines ou des exécutions.

## 12. Décisions ouvertes pour l'auteur
D7-1 poids w ; D7-2 mémoire du modèle ; D7-3 population entière vs nondominés/famille pondérée ; D7-4 identité de V0 ;
D7-5 seuil de rejet de M2 ; D7-6 test primaire et dimensionnement.
