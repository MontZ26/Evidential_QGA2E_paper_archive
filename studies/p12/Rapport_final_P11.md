# Rapport final P11 — DEC (nettoyage de dépendance) avant la combinaison de Dempster, moteur P5/P7
Date : 10 novembre 2026. Autorisation : Dr Montassar Zaghdoud (option A, 22:09 ; « I confirm all decisions related to P11 », 22:10). Analyse unique, graine 9805, n = 200 graines (10000–10199) × 6 scénarios, budget 6 040 évaluations, HV oracle moyen sur SC6 par graine, bootstrap-t apparié (B = 20 000, plancher p = 5e-5), Holm sur 2, bilatéral, α = 0,05.
Fichiers : p11_final_analysis.json (SHA 0178537389560c07922dc0e29e11416fe7b0abf221cabfe7f6524b851f814059), p11_final_stdout.txt (bff7a1d3…2f03), p11_freeze1.txt, Regle_calibration_P11.md, Amendement_P11_parametres_et_n.md.

## Résultats confirmatoires
| Test | Moyenne | IC95 % | p Holm | Décision |
|---|---|---|---|---|
| Δ1 = HV(E1) − HV(P1) | +0,0147 | [+0,0135 ; +0,0159] | 1,0e-4 (plancher) | rejet de H0 |
| Δ2 = [E1−E0] − [P1−P0] | −0,0040 | [−0,0049 ; −0,0031] | 1,0e-4 (plancher) | rejet de H0 |

HV moyens : E0 0,5761 ; E1 0,5718 ; P0 0,5573 ; P1 0,5571 ; C0b 0,6344 ; C1 0,5966.
Secondaires (descriptifs) : E1−E0 −0,0043 ; P1−P0 −0,0002 ; C1−C0 −0,0378 ; E0−P0 +0,0187 (rappel P9, reproduit) ; E1−C1 −0,0248 ; E0−C0 −0,0584.
Diagnostics de dépendance en fin de run (σ = 0,7) : Dep E0 0,284 → E1 0,016 ; P0 0,007 → P1 0,004 ; C0 0,578 → C1 0,116. Taux de violation du plafond ≤ 1,4 % ; E1 : ~7 800 mutations DEC par run, ~0,12 régénération par candidat.

## Lecture
1. Le Dempster nettoyé reste supérieur au probabiliste nettoyé (+0,0147, soit ~78 % de l'avantage non nettoyé de +0,0187) : l'avantage évidentiel de P9 n'est pas expliqué entièrement par la redondance génotypique entre sources.
2. DEC ne profite pas à Dempster : il le dégrade (−0,0043) et réduit son avantage (Δ2 < 0, significatif). Une partie de l'avantage évidentiel est donc associée à la présence de sources quasi-dupliquées. Cette réduction ne peut toutefois pas être attribuée à la seule « correction de dépendance » : DEC modifie aussi la recherche (mutations forcées, évaluations de recherche locale écartées).
3. Le contrôle C1−C0 (−0,0378) montre que, avec les paramètres calibrés, DEC pénalise fortement le GA classique ; il est un opérateur de diversité contraignant, pas neutre.
4. Aucun bras évidentiel, nettoyé ou non, n'égale le GA classique sans couche II (E0−C0 −0,058), comme dans P8/P9.

## Limites et incidents déclarés
- La dépendance mesurée est génotypique (proxy) ; aucune garantie d'indépendance statistique des sources, ni de validité des hypothèses de Dempster.
- Paramètres calibrés par la règle HV-aveugle : la règle a retenu le point le plus strict (n_max = 2, ρ_max = 0,2) ; ~87 % des candidats sont réparés. La sensibilité à σ et n_max n'a pas été testée (aucun ré-ajustement après résultats, par règle).
- n : le dimensionnement du pilote donne 100 ; n = 200 appliqué selon D11-7 (amendement écrit).
- D11-8 (suivi ancestral, « oui ») : le diagnostic est codé (option anc de p11.py) mais n'a pas été activé dans l'exécution confirmatoire ; il n'a donc pas été produit. Omission déclarée ; non prérequis selon le protocole.
- Plancher du p bootstrap (5e-5) atteint : p exact non informatif au-delà. Une seule famille d'instances, simulation à vérité cachée ; nouveauté non établie (recherche bibliographique de l'auteur requise). Dépôt GitHub intact ; code P4/P5/P7 gelé inchangé.
