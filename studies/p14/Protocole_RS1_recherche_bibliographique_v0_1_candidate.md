# RS1 v0.2 — Recherche bibliographique systématique : évidentiel (Dempster-Shafer) et probabiliste dans les algorithmes génétiques / quantum-inspired sous incertitude — CANDIDAT
**Statut :** brouillon, NON lancé. v0.2 : 10 novembre 2026, 11:25, après relecture externe de 11:07 (entrée évaluée, corrections intégrées ; la v0.1 est archivée sans changement ; aucune décision D-RS n'est confirmée). Version initiale : 10 novembre 2026, 10:53. Claude n'a pas accès à Scopus, Web of Science ni IEEE Xplore : l'auteur exécute les requêtes et exporte les résultats (RIS ou CSV) ; Claude traite les exports et textes fournis dans l'espace de travail. Aucune nouveauté n'est revendiquée avant la fin de RS1. Instruction permanente de l'auteur : ne pas citer Salama & Uhde ; si un enregistrement de ces auteurs apparaît dans un export, il est consigné au journal de recherche, signalé en privé à l'auteur, et exclu des références et de la discussion bibliographique du manuscrit.

## 1. Questions de recherche
- **RQ1 :** quels travaux combinent théorie des fonctions de croyance (Dempster-Shafer, évidence) et algorithmes génétiques ou évolutionnaires multiobjectifs sous incertitude ?
- **RQ2 (distincte de RQ1) :** lesquels utilisent la population comme ensemble de sources d'évidence, leur combinaison guidant la génération suivante ? RQ1 vise toute combinaison générale ; RQ2 vise cette architecture précise. Un travail peut être pertinent pour RQ1 sans l'être pour RQ2 : la grille d'extraction les sépare.
- **RQ3 :** lesquels portent sur les algorithmes génétiques quantum-inspired avec incertitude épistémique ?
- **RQ4 :** lesquels traitent la dépendance entre sources lors de la combinaison (règles prudentes, évidences dépendantes) dans un cadre évolutionnaire ?
- **RQ5 :** lesquels appliquent ces approches (ou des approches proches) à l'affectation d'équipes ou au routage en soins à domicile ?

## 2. Bases et champs
Scopus, Web of Science Core Collection, IEEE Xplore ; titre + résumé + mots-clés ; 2000 – 10 nov. 2026 ; anglais (et français noté) ; articles de revue, actes de conférences ; littérature grise exclue (arXiv noté séparément).

## 3. Chaînes de requête (adaptées à la syntaxe de chaque base ; consignées telles qu'exécutées avec date et nombre de résultats)
- S1 : ("Dempster-Shafer" OR "belief function*" OR "evidence theory" OR "evidential") AND ("genetic algorithm*" OR "evolutionary algorithm*" OR "NSGA" OR "multi-objective evolutionary") AND (uncertain* OR imprecis* OR epistemic)
- S2 : ("quantum-inspired" OR "quantum inspired" OR "quantum genetic") AND ("genetic algorithm*" OR evolutionary) AND (uncertain* OR "belief function*" OR "Dempster-Shafer" OR fuzzy OR "possibility")
- S3 : ("Dempster-Shafer" OR "belief function*" OR "evidence theory") AND (population OR "individuals") AND ("combination rule" OR "evidence combination" OR "Dempster") AND (evolutionary OR "genetic algorithm*" OR "swarm")
- S4 : ("conflicting evidence" OR "dependent evidence" OR "cautious rule" OR "conjunctive rule") AND ("genetic algorithm*" OR evolutionary OR "metaheuristic*")
- S5 : ("home health care" OR "home healthcare" OR "home care") AND (routing OR scheduling OR assignment OR "team") AND (uncertain* OR robust OR stochastic) AND (multi-objective OR multiobjective OR "genetic algorithm*")
**Termes complémentaires à intégrer avant exécution (chaînes élargies, nouvelle ligne datée au journal pour chaque variante) :** évidence : mass function, basic probability assignment, belief structure, belief mass, evidential reasoning ; combinaison : conjunctive combination, belief fusion, evidence fusion, Dempster's rule ; optimisation : evolutionary computation, population-based optimization, metaheuristic, multiobjective optimization ; quantum-inspired : quantum-inspired evolutionary algorithm, QIEA, quantum chromosome, qubit representation ; dépendance : source dependence, evidence dependence, non-independent evidence, correlated sources. Précautions : « fuzzy » et « possibility » ne sont pas des synonymes de théorie de l'évidence (travaux voisins, distingués au classement) ; « Dempster » seul est ambigu.
**Recherche par citations, documentée séparément des chaînes :** pour chaque travail de niveau A ou B (§6) : références citées (backward), citations reçues (forward), travaux réutilisant son mécanisme ; surtout pour RQ2 et RQ4.
Reproductibilité : chaque chaîne, base, date et nombre brut de résultats sont consignés dans le journal de recherche (modèle fourni) ; aucune chaîne n'est modifiée après exécution sans nouvelle ligne datée.

## 4. Sélection
Étape 1 : déduplication (DOI, titre normalisé). Étape 2 : titre/résumé : décision de l'auteur, décision proposée par Claude, décision finale après résolution des désaccords (motif consigné). Étape 3 : texte intégral des retenus.
**Deux corpus.** Corpus principal : théorie de l'évidence ET algorithme évolutionnaire/génétique/quantum-inspired, avec incertitude explicite. Corpus applicatif complémentaire : affectation d'équipes ou routage en soins à domicile sous incertitude, même sans théorie de l'évidence (positionne l'application sans diluer la question centrale).
Exclusion : évidence utilisée seulement pour un classement hors optimisation, sans algorithme évolutionnaire ; hors anglais/français ; texte intégral indisponible (noté).
Flux de sélection présenté selon PRISMA 2020 (sans prétendre à une revue systématique exhaustive) : doublons supprimés, exclusions après titre/résumé, exclusions après texte intégral avec raisons, textes intégraux indisponibles, travaux repérés par recherche de citations.
**Rôle de Claude :** second classeur, extracteur structuré, comparaison avec les critères, détection d'incohérences et d'informations manquantes sur les exports et textes fournis. Claude n'est PAS un second évaluateur humain indépendant. On distingue « information absente de l'article » et « non extraite par l'outil ».

## 5. Extraction (une ligne par travail retenu ; grille fournie)
Référence ; corpus ; problème ; algorithme ; rôle de l'évidence (données, recherche, les deux) ; règle de combinaison ; traitement de la dépendance ; comparaison avec un équivalent probabiliste (oui/non, résultat) ; budget égal ; évaluation oracle ; statistique ; données ; limites déclarées ; lien avec RQ1–RQ5 (RQ1 et RQ2 séparés) ; niveau de proximité.

## 6. Livrables et règles de lecture
**Niveaux de proximité :** A très proche (plusieurs mécanismes centraux de notre approche) ; B proche (même mécanisme d'intégration ou de guidage) ; C connexe (même théorie, algorithme ou application, pas l'architecture centrale) ; D contexte.
**Matrice de nouveauté par mécanisme (une ligne par travail A–C) :** représentation par fonctions de croyance ; individus de la population comme sources ; règle de combinaison ; distribution guidant les générations suivantes ; dépendance entre sources mesurée ou contrôlée ; équivalent probabiliste expérimentalement apparié ; application à un GA quantum-inspired ; budgets, graines, références et évaluations comparables ; application à l'affectation d'équipes ou au routage HHC.
La conclusion distingue la nouveauté de : (i) l'usage de Dempster-Shafer en optimisation évolutionnaire, (ii) la population comme ensemble de sources, (iii) le mécanisme de guidage de la génération suivante, (iv) le traitement de la dépendance, (v) leur combinaison. Elle est écrite seulement d'après ce tableau, avec sa limite (bases, dates). Un résultat « aucun travail proche » est rapporté avec la prudence de la couverture de recherche, non comme preuve d'absence.

## 7. Décisions à confirmer
D-RS-1 questions RQ1–RQ5 (RQ1 et RQ2 distinctes) ; D-RS-2 bases et période ; D-RS-3 chaînes S1–S5 élargies ; D-RS-4 critères d'inclusion et d'exclusion ; D-RS-5 rôle de Claude (second classeur et extraction, désaccords tracés) oui/non ; D-RS-6 livrables §6 (niveaux A–D, matrice par mécanisme, recherche de citations) ; D-RS-7 deux corpus (principal / applicatif).
