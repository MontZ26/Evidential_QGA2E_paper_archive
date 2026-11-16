# Rapport final — P3 (Paper 1) : QGA2 contre algorithmes évolutionnaires classiques, sans incertitude
Protocole : `Protocol_P3_Paper1_v1_1.md` (v1.0 écrit avant tout code ; v1.1 = v1.0 + enregistrements du §12). Autorisation : message de l'auteur du 7 nov. 2026, 11:53. Dépôt GitHub non touché.

## 1. Déroulement (aucun écart de protocole)
Tests techniques T1-T17 : tous réussis (non-régression exacte contre P2 étape 2, budgets exacts, faisabilité, invariant θ/x/tirages, archive, etc.). Réglage sur 4210-4229 (règle écrite avant). Pilote 4200-4209 : n = 44 calculé, arrondi à 100. Gel SHA-256 (`p3_freeze.txt`, `p3.py` identique à celui d'avant le réglage). Run confirmatoire : graines 4300-4399, 600 tâches, aucun incident, aucune graine exclue, aucun front vide. Analyse exécutée une seule fois (`p3_final_analysis.json`). Intégrité du gel vérifiée après le run.

## 2. Résultat principal (famille confirmatoire, Wilcoxon bilatéral apparié, Holm sur 3, n = 100 graines)
| Hypothèse | Contraste (HV moyen sur 6 scénarios) | Différence moyenne [IC bootstrap 95 %] | + / − | corr. rang-bisériale | p Holm |
|---|---|---|---|---|---|
| H-3.1 | QGA2-E − NSGA-II standard | −0,1475 [−0,1507 ; −0,1441] | 0 / 100 | −1,00 | 1,2e-17 |
| H-3.2 | QGA2 − NSGA-II apparié (non élitiste) | −0,0168 [−0,0197 ; −0,0138] | 13 / 87 | −0,91 | 4,1e-15 |
| H-3.3 | QGA2-E − QGA2 | −0,0296 [−0,0326 ; −0,0265] | 2 / 98 | −1,00 | 1,2e-17 |

Les trois tests sont significatifs, mais **dans le sens défavorable au QGA**. Aucune de nos conjectures de départ n'est confirmée : le QGA2 est battu par le NSGA-II même sans élitisme (H-3.2 réplique, sur de nouvelles graines, le sens vu en P2 étape 2), et l'ajout de l'élitisme **dégrade** le QGA2 au budget principal (H-3.3).

## 3. Descriptifs (non testés)
HV moyen : MOEA/D 0,682 ; NSGA-II 0,678 ; QGA2-A (archive) 0,598 ; NSGA-II apparié 0,577 ; GA pondéré 0,565 ; QGA2 0,560 ; WS-QGA2 0,538 ; QGA2-E 0,530 ; recherche aléatoire 0,492.
- Effet de l'élitisme : NSGA-II +0,101 [+0,099 ; +0,104] ; QGA −0,030. **Interaction** Δ_int = −0,131 [−0,135 ; −0,127], négative sur 100 graines sur 100.
- Paire scalarisée (comparaison « GA classique vs QIGA » à l'identique) : WS-QGA2 − WS-GA = −0,026 [−0,028 ; −0,025].
- Archive : QGA2-A − QGA2 = +0,0385 [+0,0374 ; +0,0395], sans changer la dynamique de recherche (ce gain vient donc de la conservation des meilleurs fronts, pas de la recherche). QGA2-A reste sous NSGA-II standard.
- Tous les algorithmes dépassent la recherche aléatoire ; le QGA2 la dépasse de +0,068.
- IGD+ (plus petit = mieux) : MOEA/D 0,006 ; NSGA-II 0,019 ; QGA2-A 0,049 ; NSGA-II apparié 0,056 ; QGA2 0,064 ; GA pondéré 0,102 ; WS-QGA2 0,117 ; QGA2-E 0,121 ; aléatoire 0,148.
- MOEA/D (45 vecteurs, 6 030 évaluations, T = 20) dépasse légèrement NSGA-II : +0,0038 [+0,0019 ; +0,0057].
- Temps moyen par recherche : 0,7 à 2,7 s ; pas de différence de coût qui change les conclusions.
- Convergence (20 premières graines) : QGA2-E devance QGA2 jusqu'à ≈ 50 générations (0,499 contre 0,483) puis est dépassé (0,529 contre 0,553 à 150) ; NSGA-II est au-dessus des deux à toute génération.
- **Budget ×4 (graines 4300-4319 seulement, descriptif)** : HV QGA2 0,553→0,561, QGA2-E 0,529→0,567, NSGA-II apparié 0,573→0,584, NSGA-II 0,673→0,711. À ×4, H-3.3 change de signe (+0,0056 [+0,0006 ; +0,0107], limite basse à peine au-dessus de zéro) ; H-3.1 reste −0,144 [−0,149 ; −0,139]. L'élitisme semble donc seulement ralentir ou retarder le QGA2-E, sans le rendre compétitif.

## 4. Lecture selon la règle d'interprétation écrite d'avance
- Aucune supériorité du QIGA n'est montrée : élitiste contre élitiste (H-3.1) comme sans élitisme (H-3.2), le NSGA-II gagne.
- L'élitisme explique l'essentiel de l'avantage du NSGA-II (+0,10), mais ne profite pas à la rotation de Q-bits (H-3.3, interaction fortement négative).
- Hypothèse mécanistique, **non testée ici** : la rotation vers un seul « meilleur » individu, combinée à un remplacement élitiste, concentre vite la population (perte de diversité) ; la trace de convergence va dans ce sens (avance précoce puis stagnation), mais la diversité n'a pas été mesurée. À ne pas présenter comme un résultat.

## 5. Limites déclarées (à écrire dans l'article)
Ordre de visite fixe (affectation + ordonnancement, pas routage) ; instances synthétiques dérivées de Solomon ; une famille de problèmes ; un seul décodeur ; κ = 0 ; réglage limité à trois jeux par algorithme, avec **deux valeurs en bord de grille** (QGA2 : 0,025π ; QGA2-E : 0,1π), donc le QGA n'est peut-être pas à son optimum — un réglage plus large est un travail futur, pas un ajout autorisé ici ; budget ×4 sur 20 graines seulement ; les bornes f1 ≥ 0,999 concernent 167 points sur 152 460 (clip actif sur quelques points d'algorithmes faibles) ; comparaison à budget d'évaluations égal ≠ coût égal ; les deux non-QGA secondaires (MOEA/D, GA pondéré) ont des budgets de 6 030 et 6 000.

## 6. Ce que cela permet de publier (sans promesse d'acceptation)
Un article honnête de type « méthode + mécanisme, résultat négatif » : le QGA2 à deux amplitudes n'égale pas le NSGA-II ni le MOEA/D à budget égal sur ce problème ; l'élitisme est le facteur dominant du côté classique et n'aide pas le côté quantique ; l'archive améliore le QGA2 sans le rendre compétitif. Revue ciblée « Q2 » plausible (méthodes/évaluation d'heuristiques), Q1 incertain ; l'étude systématique de la littérature (Scopus, WoS, IEEE Xplore) reste à faire par l'auteur avant toute affirmation de nouveauté. Paper 2 (incertitude/évidence) garde P1-M, P2 étape 1 et P2 étape 2.

## 7. Fichiers
`Protocol_P3_Paper1_v1_0.md`, `Protocol_P3_Paper1_v1_1.md`, `p3.py`, `p3_run.py`, `p3_tests.py` (+ `p3_tests*.json`), `an_p3_tune.py`, `an_p3_pilot.py`, `an_p3_final.py`, `p3_tune.json`, `p3_tuned.json`, `p3_pilot.json`, `p3_pilot_analysis.json`, `p3_n.json`, `p3_freeze.txt`, `p3_pretune_hashes.txt`, `p3_conf.json`, `p3_final_analysis.json`, `p3_final_stdout.txt`, `p3_postrun_hashes.txt`, `p3_run_notes.txt`.
