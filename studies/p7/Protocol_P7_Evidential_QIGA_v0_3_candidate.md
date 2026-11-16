# Protocole P7 — Agrégation évidentielle basée sur les individus (v0.3, CANDIDAT)

**Statut : texte candidat. NON approuvé, NON gelé. Aucun code (y compris le script G0), aucune calibration, aucune allocation de graines, aucun run.**
Remplace v0.2 (SHA-256 14d586cf…c37cbb) sans l'effacer; v0.1 : 7b88f214…765a24. Rédigé le 8 nov. 2026 à la demande de l'auteur.
Sources : décision d'architecture écrite de l'auteur (P7_architecture_decision_record_2026-11-08.md, SHA-256 ab049c19…2021c6); note conceptuelle de l'auteur
(texte reçu tronqué au §3.1); confirmations de l'auteur du 8 nov. 17:07 (cinq points, §3 ci-dessous). Les avis d'autres assistants sont des entrées, non des autorisations.
P5-B est en cours et n'est pas lu; aucun shard P5 n'est utilisé comme donnée P7. P6 reste candidat non approuvé.
**[OUVERT]** = décision écrite de l'auteur requise avant gel. Les recommandations citées ne sont pas des décisions.

## 1. Question et portée
Un algorithme évolutionnaire évidentiel à échantillonnage pignistique offre-t-il un avantage opérationnel sur un contrôle probabiliste apparié recevant les mêmes observations,
les mêmes forces de soutien, la même ignorance et le même budget ? Aucune supériorité quantique n'est présupposée.
Portée : affectation patient→équipe éligible, ordre de visite fixe, 3 objectifs à minimiser, HV exact 3D (réf. (1.2,1.2,1.2)), budget 6040 évaluations strictement comptées,
modèle factorisé par patient (corrélations inter-patients non traitées), routage intégré hors portée.

## 2. Architecture en trois étapes (évidence → agrégation → échantillonnage)
Cadre Θ_i = E_i, K_i = |Θ_i|. Masse m_i : 2^Θ_i → [0,1].

## 3. Décisions et confirmations de l'auteur
Décision d'architecture (16:19) : individus comme unité d'évidence; règle prudente primaire; Dempster en référence; grappes d'élites en alternative séparée; recherche locale
en observations ensemblistes contextuelles; évidence négative différée; comparateur à information et budget appariés. Réserve : la règle prudente n'est pas une solution universelle à la dépendance.
Confirmations (17:07) : (1) la transformation pignistique conditionnée est appliquée une seule fois à la masse combinée finale dans V1 et V2; (2) seul V0c convertit l'évidence individuelle
en probabilités avant agrégation; (3) Dempster et la règle prudente conservent leurs définitions mathématiques propres; (4) G0 doit valider la règle prudente contre la définition de Denœux
sur les structures focales réelles de P7, pas seulement sur le cas de soutiens simples disjoints; (5) v0.3 peut spécifier le script G0, ses tests et sorties attendues sans l'écrire ni l'exécuter.

## 4. Masses individuelles
**Force w et fiabilité r_j sont distinctes** (jamais appliquées deux fois). w ∈ (0, w_max], w_max < 1. Configuration proposée pour G0 (non décision) : w constant, r_j = 1.
Toute fiabilité fondée sur le rang de dominance/crowding (jamais sur la fitness scalaire) est reportée jusqu'à ce que G0 établisse son application équivalente en évidentiel (escompte, force
effective ≈ r_j·w) et en probabiliste (poids de moyenne normalisé) **[OUVERT D7-1]**.
**M1.** m_i^(j)({x_j(i)}) = w ; m_i^(j)(Θ_i) = 1 − w.
**M2.** A_i(x) = {x_i} ∪ L_i(x), L_i(x) = équipes de voisins évalués dont le mouvement modifie l'équipe du patient i (1-shift de i) et dont le voisin n'est pas dominé par le parent.
Donc A_i(x) ≠ ∅ par construction. m_i^(j)(A_i) = w ; m_i^(j)(Θ_i) = 1 − w. **Si A_i = Θ_i, les focales fusionnent : m_i^(j)(Θ_i) = 1.** Sans observation éligible : m_i^(j)(Θ_i) = 1.
Les échanges de deux patients sont **exclus** de M2 dans la première étude (observations conjointes, non attribuables à un seul patient); extension distincte éventuelle.
Les voisins évalués et rejetés : règle d'inclusion à fixer **avant G1** et appliquée uniformément **[OUVERT D7-8]**.
Interprétation : alternatives observées localement en contexte, non aptitude intrinsèque de l'équipe; un voisin non dominé par son parent n'est pas non dominé globalement.

## 5. Combinaison et échantillonnage — trois étapes distinctes
| Étape | V1 — Dempster | V2 — Prudente |
|---|---|---|
| 1. Combinaison | Règle de Dempster, avec sa normalisation | Règle prudente de Denœux (décompositions canoniques, poids combinés par minimum), définition propre |
| 2. Enregistrement | m(∅) avant normalisation, événements de conflit total | m(∅) après combinaison, événements de conflit total |
| 3. Distribution d'échantillonnage | BetP conditionnée (ci-dessous) | même BetP conditionnée |
BetP_i(k) = [ Σ_{A≠∅, A∋k} m_i(A)/|A| ] / (1 − m_i(∅)), si m_i(∅) < 1. Pour V1 la normalisation de Dempster a déjà supprimé m(∅) : la transformation est neutre. Pour V2 le conditionnement est appliqué
après la combinaison et ne modifie pas la définition de la règle. Il s'applique à la masse finale, jamais à des masses intermédiaires. Aucune double normalisation.
Repli algorithmique (non théorique) si m_i(∅) = 1 : m_i(Θ_i) = 1 ; sa fréquence est rapportée séparément.
Plancher ε : combinaisons sans plancher; ε appliqué une seule fois aux probabilités finales d'échantillonnage; mêmes ε, renormalisation et moment d'application dans V0c, V1, V2.
Aucune règle n'établit l'indépendance des individus. Exemple d'illustration (à recalculer en G0) : trois copies de m({A})=0,8, m(Θ)=0,2 → m({A})=0,992 sous Dempster.
Pour {A} et {B} disjoints, de même force de soutien w : la combinaison non normalisée donne m(∅)=w², m({A})=m({B})=w(1−w), m(Θ)=(1−w)² ; ceci illustre la nécessité de calculer les masses complètes.

## 6. Contrôle apparié V0c
q_i^(j) = transformation pignistique individuelle de m_i^(j), ignorance comprise :
M1 : q = w·δ_{x_j(i)} + (1−w)·U_{Θ_i} ; M2 : q = w·U_{A_i} + (1−w)·U_{Θ_i} (cas A_i = Θ_i : q = U_{Θ_i}).
p_i(k) = Σ_j r_j q_i^(j)(k) / Σ_j r_j (r_j = 1 : moyenne simple), puis ε. Mêmes observations, w, r_j, LS, budget, opérateurs auxiliaires. Un contrôle ponctuel sans ignorance est exclu.
L'écart V1/V2 vs V0c porte sur l'ordre des opérations (combiner puis BetP vs BetP puis moyenne).

## 7. Boucle algorithmique
Reprise de P5 (population initiale commune, enfants séquentiels par échantillonnage + mutation ciblée, évaluation, archive cap 200, LS comptée, survie (μ+λ), mise à jour une fois par génération,
front final = archive, budget strict, génération partielle autorisée). Fichiers gelés P4/P5 inchangés; instrumentation sur copie avec registre des modifications.
Propositions pour la première expérience (non décisions) : reconstruction du modèle à chaque génération **[OUVERT D7-2]** ; population entière comme source primaire, élites seules en alternative **[OUVERT D7-3]**.

## 8. Bras
V0 : meilleur modèle probabiliste du rapport final P5-B **[OUVERT D7-4]** ; V0c : contrôle primaire ; V1 : Dempster ; V2 : prudente (candidat primaire).
V3 (pondération population/élites) et V4 (masses de grappes d'élites, espace de décision; espace objectif = autre alternative) : extensions hors étape 1.
NSGA-II, C0b et autres références P5 : descriptif, configurations gelées.

## 9. Porte G0 — validation mathématique (script spécifié, NON écrit, NON exécuté, non autorisé)
**Nature :** artefact de validation mathématique indépendant du moteur évolutionnaire gelé; aucune donnée expérimentale; son écriture et son exécution exigent une approbation écrite distincte.
**Spécification du script (10 exigences) :**
1. M1 et M2 implémentées indépendamment (incl. A_i = Θ_i, absence d'observation).
2. Règle de Dempster. 3. Règle prudente de Denœux par décomposition canonique.
4. m(∅) enregistrée avant tout conditionnement. 5. BetP conditionnée commune. 6. V0c par distributions pignistiques individuelles avec ignorance.
7. Même ε et même renormalisation sur toutes les distributions d'échantillonnage.
8. Cas déterministes : 1 source/1 équipe ; sources identiques répétées ; sources d'équipes différentes ; ensembles focaux chevauchants ; ignorance totale ; preuves conflictuelles ;
   poids inégaux ; A_i = Θ_i ; **exemple 30 contre 5** (30 sources identiques pour A, 5 pour B, même w, K_i explicite).
9. Contrôles : conservation de la masse, masses ≥ 0, normalisation des probabilités, idempotence là où applicable, reproductibilité.
   **Validation de la règle prudente contre la définition de Denœux sur les structures focales effectivement utilisées** (le cas disjoint de soutiens simples n'est pas suffisant).
10. Sorties : fichier de résultats lisible par machine, hash du script, journal d'exécution.
**Questions :** perte d'information de fréquence (hypothèse, non résultat : V2 traite A et B plus symétriquement que V0c); sort de l'ignorance et du conflit; équivalence éventuelle avec V0c; équivalence des rôles de r_j.
Un écart numérique n'est pas en soi une valeur scientifique : il doit avoir une interprétation défendable et des conséquences utiles plausibles. Si V2 se réduit à V0c ou n'apporte aucun avantage plausible,
la justification d'une étude expérimentale est faible; un résultat défavorable à V2 est un résultat scientifique utile.

## 10. Porte G1 — audit instrumenté (approbation écrite séparée, après G0)
Copie du moteur; les shards existants ne contiennent ni mouvements de LS ni affectations (vérifié). Journaliser : type de mouvement, patient, équipe ancienne/nouvelle, vecteurs d'affectation et objectifs du parent et du voisin,
accepté/rejeté, mouvement à un ou plusieurs patients. Couverture rapportée séparément par scénario, patient, individus avec observation pertinente, nombre d'alternatives, 1-shift vs 2-swap,
cas sans évidence, similarité espace de décision vs objectif, quasi-doublons. Seuil de couverture fixé avant G1 **[OUVERT D7-5]** ; en deçà, M2 est abandonné sans modifier w ni ajouter de sources. Graines proposées 7000–7009 (non allouées).

## 11. Plan statistique (à figer après G0)
H7.1 (primaire) : ΔHV = HV(V2) − HV(V0c) > 0, apparié par graine, résultat par graine = moyenne du HV sur les scénarios. Test candidat : bootstrap-t apparié sur la moyenne **[OUVERT D7-6]** ;
à fixer avant gel : unité d'appariement, procédure et réplicats, graine d'analyse, écart-type nul, hypothèses de puissance, multiplicité.
Famille secondaire (Holm candidate) : H7.2 V2 vs V1 ; H7.3 V1 vs V0c ; H7.4 V2 vs V0. Descriptif : masse d'ignorance, conflit, entropie, divergence BetP–fréquence, couverture, surcoût, équivalence ±0,01 non formelle.
Dimensionnement par pilote et règle gelée, selon G0 et la faisabilité, sans copie mécanique de P6. Plages de graines à fixer en v0.4.

## 12. Limites déclarées
Modèle factorisé; dépendance entre individus non éliminée; règle prudente possiblement trop faible comme signal d'apprentissage (risque falsifiable); couverture de M2 possiblement insuffisante; évidence M2 contextuelle;
une seule famille d'instances (Solomon dérivées); nouveauté non établie (recherche systématique Scopus/WoS/IEEE Xplore à faire par l'auteur); conclusions limitées à cette architecture.

## 13. Gouvernance et séquence
1. Terminer P5-B, lire et valider le rapport final. 2. Décision sur P6 (indépendante). 3. Approuver par écrit l'écriture puis l'exécution de G0. 4. Évaluer G0 ; décider de poursuivre ou d'arrêter.
5. Si poursuite : résoudre D7-1…D7-8, approuver et geler P7. 6. Autoriser G1 séparément. 7. Seulement ensuite : implémentation, calibration, pilote, confirmation.
Aucun résultat ou shard P5-B n'est utilisé comme donnée P7. Rien dans ce texte n'autorise du code, des graines ou des exécutions.

## 14. Décisions ouvertes
D7-1 force/fiabilité ; D7-2 mémoire du modèle ; D7-3 source (population entière / nondominés / pondérée) ; D7-4 identité de V0 ; D7-5 seuil de couverture M2 ;
D7-6 test primaire et dimensionnement ; D7-8 règle d'inclusion des voisins rejetés. (D7-7 est traité par le §5 : trois étapes distinctes, conventions de repli déclarées.)
