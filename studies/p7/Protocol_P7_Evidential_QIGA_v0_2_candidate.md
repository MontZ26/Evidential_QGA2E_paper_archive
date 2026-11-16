# Protocole P7 — Agrégation évidentielle basée sur les individus (v0.2, CANDIDAT)

**Statut : texte candidat. NON approuvé, NON gelé. Aucun code, aucune calibration, aucune allocation de graines, aucun run.**
Remplace v0.1 (SHA-256 7b88f214…765a24) sans l'effacer. Rédigé le 8 nov. 2026 à la demande de l'auteur.
Sources : décision d'architecture écrite de l'auteur (P7_architecture_decision_record_2026-11-08.md, SHA-256 ab049c19…2021c6);
note conceptuelle de l'auteur (texte reçu tronqué au §3.1); corrections de V0c et de la séparation w/r discutées le 8 nov. (entrées, non des autorisations).
P5-B est en cours et n'est pas lu; aucun shard P5 n'est utilisé comme donnée P7. P6 reste candidat non approuvé.
**[OUVERT]** = décision écrite de l'auteur requise avant gel. Les recommandations citées sont des recommandations, pas des décisions.

## 1. Question et portée
Un algorithme évolutionnaire évidentiel à échantillonnage pignistique offre-t-il un avantage opérationnel sur un contrôle probabiliste apparié recevant les
mêmes observations, les mêmes forces de soutien, la même ignorance et le même budget ? Terminologie : « algorithme évolutionnaire évidentiel avec
échantillonnage probabiliste pignistique ». Aucune supériorité quantique n'est présupposée.
Portée inchangée : affectation patient→équipe éligible, ordre de visite fixe, 3 objectifs à minimiser, HV exact 3D (réf. (1.2,1.2,1.2)), budget 6040
évaluations strictement comptées, modèle factorisé par patient (corrélations inter-patients non traitées), routage intégré hors portée.

## 2. Chaîne en trois étapes
(1) Représentation : chaque individu fournit, par patient, une fonction de masse sur 2^Θ_i. (2) Agrégation par règle évidentielle. (3) Transformation pignistique
BetP_i(k) = Σ_{A∋k} m_i(A)/|A|, plancher ε et renormalisation (même ε que P5 et que le contrôle), échantillonnage. Cadre Θ_i = E_i, m_i(∅)=0 après agrégation.

## 3. Décisions d'architecture de l'auteur (8 nov. 2026, 16:19)
Unité d'évidence primaire : individus. Règle primaire : prudente. Référence : Dempster. Alternative : masses de grappes d'élites (séparée).
Recherche locale : observations ensemblistes en contexte. Évidence négative : différée. Comparateur : information et budget appariés.
Réserve de l'auteur : la règle prudente ne résout pas la dépendance en général; hypothèses et comportement à examiner (évidence dogmatique, structures focales différentes).

## 4. Construction des masses individuelles
Notation : K_i = |Θ_i| ; j indexe les individus de la population courante.
**Force de soutien w_j et fiabilité r_j sont distinctes** et ne doivent pas être appliquées deux fois.
- w_j ∈ (0, w_max], w_max < 1 : force de la masse (non dogmatique, nécessaire à la règle prudente).
- r_j : fiabilité de la source. **Étape 1 : r_j = 1 pour tous** (aucun poids de fiabilité); seul w intervient, constant dans tous les bras.
  Toute fiabilité fondée sur le rang de dominance/crowding (jamais sur la fitness scalaire) est reportée tant que G0 n'a pas établi comment elle
  s'applique de façon équivalente en évidentiel (escompte : force effective ≈ r_j·w_j) et en probabiliste (poids de moyenne normalisé) **[OUVERT D7-1]**.
**M1.** m_i^(j)({x_j(i)}) = w ; m_i^(j)(Θ_i) = 1 − w.
**M2.** A_i(x) = {x_i} ∪ L_i(x), L_i(x) = équipes des voisins **évalués** dont le mouvement modifie l'équipe du patient i et dont le voisin n'est pas dominé par le parent.
m_i^(j)(A_i) = w ; m_i^(j)(Θ_i) = 1 − w. Sans observation éligible : m_i(Θ_i) = 1.
Précisions : le résultat d'un voisin dépend du reste de l'affectation (alternatives observées localement en contexte, non aptitude intrinsèque);
un voisin non dominé par son parent n'est pas non dominé globalement; un échange de deux patients est une évidence conjointe, non attribuable à un seul patient
(seuls les mouvements modifiant l'équipe de i et étiquetés par type sont retenus; le traitement des échanges est à fixer avant G1); les voisins évalués
et rejetés peuvent être des observations, à condition que la règle soit spécifiée explicitement avant G1.

## 5. Règles de combinaison
- **V2 (primaire) : règle prudente** (décomposition canonique de Denœux; poids combinés par minimum). Idempotente pour des preuves identiques.
- **V1 (référence) : règle de Dempster.** Accumule l'accord (3 copies de m({A})=0,8, m(Θ)=0,2 → m({A})=0,992); risque de sur-confiance sous dépendance.
- **Convention de conflit [OUVERT D7-7]** : les deux règles sont conjonctives et peuvent produire de la masse sur ∅ (sources aux ensembles disjoints).
  Candidat : normalisation par 1 − m(∅); si m(∅) = 1, retour à m(Θ_i)=1. La convention est fixée avant G0 et identique dans V1 et V2; le conflit m(∅) est enregistré.
- Aucune règle n'établit l'indépendance des individus (lignées communes, sélection conjointe).

## 6. Contrôle apparié V0c (définition mathématique)
Chaque individu induit la distribution pignistique de sa propre masse, **ignorance comprise** :
- M1 : q_i^(j) = w·δ_{x_j(i)} + (1 − w)·U_{Θ_i}, c.-à-d. q(k) = w + (1−w)/K_i pour k = x_j(i) et (1−w)/K_i pour les autres.
- M2 : q_i^(j) = w·U_{A_i(x_j)} + (1 − w)·U_{Θ_i}.
Agrégation : p_i(k) = Σ_j r_j q_i^(j)(k) / Σ_j r_j (avec r_j = 1 à l'étape 1, moyenne simple), puis plancher ε et échantillonnage identique.
(Une version ponctuelle q = δ sans ignorance donnerait un contrôle artificiellement plus concentré et est exclue.)
L'écart entre V2/V1 et V0c tient à l'ordre des opérations : P7 combine les masses puis applique BetP ; V0c applique BetP puis moyenne.
Mêmes observations, mêmes w, mêmes r_j, même LS, même budget, mêmes opérateurs auxiliaires.

## 7. Boucle algorithmique
Reprise de P5 : population initiale commune, enfants séquentiels par échantillonnage du modèle + mutation ciblée, évaluation, archive (cap 200, rejet dominé/doublon,
crowding), LS optionnelle (évaluations comptées), survie (μ+λ), mise à jour du modèle une fois par génération, front final = archive, budget strict, génération
partielle autorisée. Fichiers gelés P4/P5 inchangés; toute instrumentation se fait sur copie avec registre des modifications.
Recommandations (non décisions) : reconstruire le modèle à chaque génération à partir de la population courante **[OUVERT D7-2]** ;
population entière comme source primaire, élites seules en alternative séparée **[OUVERT D7-3]**.

## 8. Bras
| Bras | Description | Statut |
|---|---|---|
| V0 | Meilleur modèle probabiliste du rapport final P5-B **[OUVERT D7-4]** | Référence établie |
| V0c | Contrôle apparié (§6) | Contrôle primaire |
| V1 | Évidentiel, Dempster | Référence évidentielle |
| V2 | Évidentiel, règle prudente | Candidat primaire |
| V3 | Évidence pondérée population/élites | Extension conditionnelle |
| V4 | Masses de grappes d'élites (espace de décision; espace objectif = autre alternative) | Extension séparée |
V3/V4 hors étape 1 tant que la comparaison V0c/V1/V2 n'est pas tranchée et justifiée. NSGA-II, C0b et autres références P5 : descriptif, configurations gelées.

## 9. Porte G0 — faisabilité mathématique (aucune expérience)
Calculer, pour V2, V1 et V0c, la masse combinée complète, la masse de conflit m(∅) selon la convention D7-7 et les probabilités pignistiques, pour :
1 source/1 équipe ; plusieurs sources identiques ; sources d'équipes différentes ; ensembles focaux chevauchants ; ignorance totale ; preuves conflictuelles ;
poids inégaux ; **exemple 30 contre 5** (30 sources identiques pour A, 5 pour B, même w) avec K_i explicite.
Questions : perte d'information de fréquence (hypothèse à vérifier : V2 traite A et B de façon plus symétrique que V0c; non établi); sort de l'ignorance
et du conflit; équivalence éventuelle avec V0c pour les structures de masse réellement utilisées; équivalence des rôles de r_j (§4).
Un écart numérique entre distributions n'est pas en soi une preuve de valeur scientifique : il doit avoir une interprétation défendable et des conséquences
utiles plausibles. Si V2 se réduit à V0c pour les structures utilisées, ou n'apporte aucun avantage plausible, la justification d'une étude expérimentale est faible.
Une trace de calcul reproductible (script indépendant du moteur) et son hash seront produits.

## 10. Porte G1 — audit instrumenté (approbation écrite séparée, après G0)
Courte exécution sur copie du moteur; les shards existants ne contiennent ni les mouvements de LS ni les affectations (vérifié). Journaliser : type de mouvement,
patient concerné, équipe ancienne/nouvelle, vecteurs d'affectation du parent et du voisin, objectifs du parent et du voisin, accepté/rejeté, mouvement à un ou
plusieurs patients. Couverture rapportée séparément par scénario, patient, nombre d'individus avec observation pertinente, nombre d'alternatives, 1-shift vs
2-swap, cas sans évidence, similarité espace de décision vs espace objectif, part de quasi-doublons (un pourcentage global seul peut masquer un déséquilibre).
**Seuil de couverture fixé avant G1 [OUVERT D7-5]** ; en deçà, M2 est abandonné sans modifier w ni ajouter de sources. Graines proposées 7000–7009 (non allouées).

## 11. Plan statistique (à figer après G0)
H7.1 (primaire) : ΔHV = HV(V2) − HV(V0c) > 0, apparié par graine, résultat par graine = moyenne du HV sur les scénarios.
Test candidat : bootstrap-t apparié sur la moyenne, comme P6 **[OUVERT D7-6]**. À fixer avant gel : unité d'appariement, procédure et nombre de réplicats,
graine d'analyse, traitement de l'écart-type nul, hypothèses de dimensionnement et de puissance, correction de multiplicité.
Famille secondaire (correction préannoncée, Holm candidate) : H7.2 V2 vs V1 ; H7.3 V1 vs V0c ; H7.4 V2 vs V0.
Descriptif : masse d'ignorance, conflit, entropie, divergence BetP–fréquence, couverture, surcoût de calcul, équivalence ±0,01 non formelle.
Dimensionnement : par pilote et règle gelée, selon la faisabilité mathématique (G0) et le plan de faisabilité, sans copie mécanique de P6 ; plafond à fixer.
Plages de graines (calibration, pilote, confirmation, analyse) à fixer en v0.3.

## 12. Limites déclarées
Modèle factorisé; dépendance entre individus non éliminée; règle prudente possiblement trop faible comme signal d'apprentissage (risque falsifiable);
couverture de M2 possiblement insuffisante; évidence M2 dépendante du contexte; une seule famille d'instances (Solomon dérivées); nouveauté non établie
(recherche systématique Scopus/WoS/IEEE Xplore à faire par l'auteur); conclusions limitées à cette architecture.

## 13. Gouvernance et séquence
1. Terminer P5-B, lire et valider le rapport final. 2. Décision sur P6 (indépendante). 3. Résoudre la conception mathématique de P7 (M1, M2, V0c, règles, G0).
4. Approuver P7 par écrit et le geler (décisions D7-1…D7-7 résolues). 5. Autoriser G1 séparément. 6. Seulement ensuite : implémentation, calibration, pilote, confirmation.
Aucun résultat ou shard P5-B n'est utilisé comme donnée P7. Rien dans ce texte n'autorise du code, des graines ou des exécutions.

## 14. Décisions ouvertes
D7-1 force/fiabilité (étape 1 : w constant, r_j=1, recommandation non décision) ; D7-2 mémoire du modèle ; D7-3 source : population entière / nondominés / pondérée ;
D7-4 identité de V0 ; D7-5 seuil de couverture M2 ; D7-6 test primaire et dimensionnement ; D7-7 convention de conflit pour les règles conjonctives.
