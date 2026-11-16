# Rapport final P9 (confirmatoire) — évidentiel contre probabiliste — 2026-11-09
Protocole P9 v0.1 + Amendement (confirmation de l'auteur, 18:00). Gel : p9_freeze1.txt. Graines 9000–9199 (n = 200), 6 scénarios, 6 bras, budget 6 040 exact (précontrôle OK, 1 200 coquilles, aucune graine exclue). G-I/G-P passés avant le gel (monde probabiliste = réimplémentation indépendante à 1,1e-16 ; bras E reproduit le bras D de P8 bit à bit). Analyse unique (graine 9802) : `p9_final_analysis.json` SHA c0f03dea…dc02 ; sortie p9_final_stdout.txt f4c7d53f…5d72. Aucun incident ; dépôt GitHub intact (git status propre).
## HV oracle moyen
E 0,5772 · P 0,5497 · X 0,5666 · D′ 0,5567 · B 0,6332 · B_p 0,6216.
## Primaire (confirmatoire)
**G = E − P = +0,0275**, IC95 % [+0,0261 ; +0,0289], p bootstrap-t = 5e-5 (plancher), E > P pour 99,5 % des graines. L'intégration évidentielle (données + recherche V1) surpasse l'intégration probabiliste (moyenne des sources + V0c) dans ce dispositif.
## Secondaires (descriptifs, IC95 %)
| Contraste | Moyenne | Lecture |
|---|---|---|
| E − X (données évid. vs prob., recherche V1) | +0,0106 [0,0093 ; 0,0118] | effet de la représentation des données |
| D′ − P (idem, recherche V0c) | +0,0071 [0,0062 ; 0,0079] | idem |
| E − D′ (V1 vs V0c, données évid.) | +0,0205 [0,0192 ; 0,0217] | effet de la représentation de la recherche |
| X − P (V1 vs V0c, données prob.) | +0,0169 [0,0155 ; 0,0184] | idem |
| Interaction E − D′ − X + P | +0,0035 [0,0020 ; 0,0050] | légèrement positive, petite |
| B − B_p (GA sans couche II) | +0,0117 [0,0100 ; 0,0133] | données évid. > prob. même sans recherche évidentielle |
| E − B | −0,0560 | la couche II (V1) reste inférieure au GA sans couche II |
| P − B_p | −0,0719 | idem pour la version probabiliste |
## Lecture
1. Les deux composants évidentiels s'additionnent à peu près (interaction +0,0035, faible) : E − P ≈ effet données + effet recherche.
2. L'effet de la représentation des données est confirmé dans quatre comparaisons (E−X, D′−P, B−B_p) et converge avec G-D (+0,022 vs moyenne probabiliste, descriptif).
3. L'effet côté recherche (V1 > V0c) est le plus grand mais reste confondu avec la concentration (V0c-τ non apparié, P8/G-C).
4. **Aucun bras avec couche II n'atteint le GA sans couche II** (E−B = −0,056 ; P−B_p = −0,072) : la supériorité évidentielle est relative à l'alternative probabiliste, non à la recherche classique.
## Limites
Une famille d'instances (dérivées de Solomon), ordre de visite fixe, simulation avec vérité cachée ; la moyenne à poids égaux n'est qu'une des alternatives probabiliste (le produit bayésien n'est pas testé) ; V0c non apparié en concentration à V1 ; nouveauté non établie ; P9 compare deux intégrations sur le moteur P5/P7, pas QGA2.
