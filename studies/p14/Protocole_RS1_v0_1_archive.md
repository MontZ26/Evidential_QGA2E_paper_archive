# RS1 v0.1 — Recherche bibliographique systématique : évidentiel (Dempster-Shafer) et probabiliste dans les algorithmes génétiques / quantum-inspired sous incertitude — CANDIDAT
**Statut :** brouillon, NON lancé, 10 novembre 2026, 10:53. Claude n'a pas accès à Scopus, Web of Science ni IEEE Xplore : l'auteur exécute les requêtes et exporte les résultats (RIS ou CSV) ; Claude peut dédupliquer, classer, extraire et résumer ces exports dans l'espace de travail. Aucune nouveauté n'est revendiquée avant la fin de RS1. Instruction permanente de l'auteur : ne pas citer Salama & Uhde ; si un enregistrement de ces auteurs apparaît, il est signalé à l'auteur et non cité.

## 1. Questions de recherche
RQ1 : quels travaux combinent théorie des fonctions de croyance (Dempster-Shafer, évidence) et algorithmes génétiques ou évolutionnaires multiobjectifs sous incertitude ? RQ2 : lesquels utilisent la population comme source d'évidence (règle de combinaison pour guider la recherche) ? RQ3 : lesquels portent sur les algorithmes génétiques quantum-inspired avec incertitude épistémique ? RQ4 : lesquels traitent la dépendance entre sources lors de la combinaison (règles prudentes, évidences dépendantes) dans un cadre évolutionnaire ? RQ5 : lesquels appliquent ces approches à l'affectation d'équipes ou au routage en soins à domicile ?

## 2. Bases et champs
Scopus, Web of Science Core Collection, IEEE Xplore ; titre + résumé + mots-clés ; 2000 – 10 nov. 2026 ; anglais (et français noté) ; articles de revue, actes de conférences ; littérature grise exclue (arXiv noté séparément).

## 3. Chaînes de requête (adaptées à la syntaxe de chaque base ; à consigner telles qu'exécutées avec date et nombre de résultats)
- S1 : ("Dempster-Shafer" OR "belief function*" OR "evidence theory" OR "evidential") AND ("genetic algorithm*" OR "evolutionary algorithm*" OR "NSGA" OR "multi-objective evolutionary") AND (uncertain* OR imprecis* OR epistemic)
- S2 : ("quantum-inspired" OR "quantum inspired" OR "quantum genetic") AND ("genetic algorithm*" OR evolutionary) AND (uncertain* OR "belief function*" OR "Dempster-Shafer" OR fuzzy OR "possibility")
- S3 : ("Dempster-Shafer" OR "belief function*" OR "evidence theory") AND (population OR "individuals") AND ("combination rule" OR "evidence combination" OR "Dempster") AND (evolutionary OR "genetic algorithm*" OR "swarm")
- S4 : ("conflicting evidence" OR "dependent evidence" OR "cautious rule" OR "conjunctive rule") AND ("genetic algorithm*" OR evolutionary OR "metaheuristic*")
- S5 : ("home health care" OR "home healthcare" OR "home care") AND (routing OR scheduling OR assignment OR "team") AND (uncertain* OR robust OR stochastic) AND (multi-objective OR multiobjective OR "genetic algorithm*")
Reproductibilité : chaque chaîne, base, date, nombre brut de résultats sont consignés dans un tableau (journal de recherche) ; aucune chaîne n'est modifiée après exécution sans nouvelle ligne datée.

## 4. Sélection
Étape 1 : déduplication (DOI, titre normalisé). Étape 2 : titre/résumé par un relecteur (l'auteur) avec Claude comme second classeur sur l'export, accords et désaccords consignés. Étape 3 : texte intégral des retenus. Inclusion : méthode combinant évidence/croyance ET algorithme évolutionnaire/génétique/quantum-inspired, avec incertitude explicite, ou application HHC aux mêmes méthodes. Exclusion : évidence utilisée seulement pour un classement hors optimisation, sans algorithme évolutionnaire ; hors anglais/français ; texte intégral indisponible (noté). Diagramme de flux de type PRISMA des comptes à chaque étape.

## 5. Extraction (une ligne par travail retenu)
Référence ; problème ; algorithme (GA, QGA, NSGA-II…) ; rôle de l'évidence (données, recherche, les deux) ; règle de combinaison ; traitement de la dépendance ; comparaison avec un équivalent probabiliste (oui/non, résultat) ; budget égal ; évaluation oracle ; statistique ; données ; limites déclarées ; lien avec RQ1–RQ5.

## 6. Livrables et règles de lecture
Tableau des travaux proches avec colonne « ce que ce travail ne fait pas par rapport à notre étude » ; carte des recouvrements par RQ ; une conclusion écrite sur la nouveauté seulement d'après ce tableau, avec sa limite (bases et dates). Un résultat « aucun travail proche » est à rapporter avec la prudence de la couverture de recherche, non comme preuve d'absence.

## 7. Décisions à confirmer
D-RS-1 questions RQ1–RQ5 ; D-RS-2 bases et période ; D-RS-3 chaînes S1–S5 ; D-RS-4 critères d'inclusion et d'exclusion ; D-RS-5 rôle de Claude (classement second et extraction sur exports fournis) oui/non ; D-RS-6 livrables §6.
