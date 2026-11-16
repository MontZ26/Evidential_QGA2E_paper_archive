# Annexe post hoc descriptive de P23 (v0.1)
Date : 14 novembre 2026. Autorisation : « OK pour les trois, dans cet ordre » (Dr M. Zaghdoud, 22:16). **Analyses post hoc, descriptives, non préenregistrées, hors du gel.** Elles lisent les 600 fichiers de l'exécution principale (aucun calcul de recherche, aucune relance). Aucun test confirmatoire, aucune p-valeur ; les IC à 95 % (bootstrap sur les graines, B = 5 000, graine fixée) sont **descriptifs**, sans correction de multiplicité. Elles aident à comprendre un mécanisme ; elles ne modifient aucune conclusion du rapport final. Code : `code/p23_posthoc.py` ; sorties : `posthoc/`. Aucune revendication de nouveauté.

## 1. Contrastes par scénario (Δ HV, moyenne [IC 95 % descriptif], n = 100 graines)
Référence Dg = Dg(γ = 6) (bras unique). Figure : `posthoc/fig_contrastes_par_scenario.png`.
| Contraste | S4-RC101 | S4-R101 | S4-C101 | S5-RC101 | S5-R101 | S5-C101 |
|---|---|---|---|---|---|---|
| DA25-Dg | -0,0047 [-0,0099 ; +0,0004] | +0,0018 [-0,0028 ; +0,0062] | +0,0025 [-0,0026 ; +0,0077] | -0,0085 [-0,0146 ; -0,0023] | -0,0089 [-0,0133 ; -0,0047] | +0,0006 [-0,0050 ; +0,0063] |
| DA50-Dg | -0,0043 [-0,0093 ; +0,0008] | +0,0014 [-0,0033 ; +0,0062] | +0,0011 [-0,0042 ; +0,0065] | -0,0076 [-0,0139 ; -0,0013] | -0,0103 [-0,0147 ; -0,0064] | +0,0003 [-0,0055 ; +0,0059] |
| DA100-Dg | -0,0071 [-0,0121 ; -0,0022] | -0,0025 [-0,0071 ; +0,0020] | +0,0033 [-0,0022 ; +0,0087] | -0,0076 [-0,0138 ; -0,0016] | -0,0102 [-0,0145 ; -0,0061] | +0,0006 [-0,0050 ; +0,0063] |
| DA100-E | -0,0032 [-0,0065 ; +0,0002] | -0,0057 [-0,0088 ; -0,0025] | +0,0043 [+0,0000 ; +0,0086] | -0,0013 [-0,0029 ; +0,0002] | -0,0000 [-0,0008 ; +0,0008] | +0,0007 [-0,0016 ; +0,0030] |

## 2. Par type de scénario (R, RC, C ; moyenne de S4 et S5)
| Contraste | R | RC | C |
|---|---|---|---|
| DA25-Dg | -0,0035 [-0,0067 ; -0,0005] | -0,0066 [-0,0104 ; -0,0027] | +0,0015 [-0,0023 ; +0,0055] |
| DA50-Dg | -0,0044 [-0,0078 ; -0,0013] | -0,0060 [-0,0098 ; -0,0022] | +0,0007 [-0,0032 ; +0,0046] |
| DA100-Dg | -0,0063 [-0,0096 ; -0,0032] | -0,0074 [-0,0113 ; -0,0035] | +0,0020 [-0,0021 ; +0,0060] |
| DA100-E | -0,0028 [-0,0045 ; -0,0012] | -0,0022 [-0,0042 ; -0,0003] | +0,0025 [-0,0000 ; +0,0049] |
Lecture descriptive : DA est en dessous de Dg pour R et RC (IC descriptifs entièrement négatifs) ; pour C, l'écart est proche de zéro, de signe positif, IC contenant 0. Les scénarios C ont une journée plus longue (1 236 contre 230 à 240 pour R et RC) et des visites plus longues (90 contre 10), d'après le générateur d'instances (Annexe B du papier) ; cela change la structure du problème, sans que le lien avec l'écart observé soit établi. Aucun test d'interaction ; il s'agit d'une régularité observée sur six scénarios, non démontrée.

## 3. Trajectoires de concentration et de diversité
Figure : `posthoc/fig_trajectoires.png`. Valeurs moyennes (q_max / Dep / N_eff) aux générations 1, 25, 50, 100, 150 :
| Bras | gén. 1 | gén. 25 | gén. 50 | gén. 100 | gén. 150 |
|---|---|---|---|---|---|
| E | 0.447 / 0.000 / 40.0 | 0.661 / 0.029 / 37.8 | 0.745 / 0.126 / 32.3 | 0.810 / 0.318 / 23.3 | 0.845 / 0.440 / 18.3 |
| DA25 | 0.447 / 0.000 / 40.0 | 0.653 / 0.028 / 37.8 | 0.719 / 0.112 / 32.6 | 0.743 / 0.265 / 24.3 | 0.754 / 0.356 / 19.8 |
| DA50 | 0.447 / 0.000 / 40.0 | 0.651 / 0.025 / 38.0 | 0.708 / 0.100 / 33.1 | 0.722 / 0.230 / 25.4 | 0.728 / 0.304 / 21.1 |
| DA100 | 0.447 / 0.000 / 40.0 | 0.649 / 0.023 / 38.1 | 0.699 / 0.089 / 33.4 | 0.708 / 0.196 / 26.6 | 0.709 / 0.258 / 22.8 |
| Dg100 | 0.535 / 0.000 / 40.0 | 0.615 / 0.014 / 38.9 | 0.679 / 0.054 / 36.2 | 0.757 / 0.186 / 28.9 | 0.797 / 0.323 / 22.4 |
| RHO | 0.436 / 0.000 / 40.0 | 0.592 / 0.010 / 39.2 | 0.657 / 0.053 / 36.2 | 0.726 / 0.183 / 29.0 | 0.761 / 0.284 / 24.3 |
| MIX | 0.402 / 0.000 / 40.0 | 0.514 / 0.004 / 39.6 | 0.559 / 0.014 / 38.8 | 0.603 / 0.041 / 36.9 | 0.629 / 0.067 / 35.2 |
Constat important : l'appariement de P23 porte sur la **moyenne de l'entropie et de q_max sur les 150 générations**. Les trajectoires ne se ressemblent pas : q_max de DA(1) plafonne vers 0,71 dès la génération ~70, tandis que celui de Dg continue de monter jusqu'à 0,80 ; E monte jusqu'à 0,85. La conformité de l'appariement moyen n'implique donc pas des trajectoires comparables, ce qui renforce la réserve du rapport (appariement ≠ distribution effective ni dynamique identique). Cette observation est post hoc.

## 4. Distribution de décodage à la génération 150, par type de scénario
(fréquence de décodage maximale / entropie de décodage / L1 décodage–cible)
| Bras | R | RC | C |
|---|---|---|---|
| E | 0.615 / 1.030 / 0.450 | 0.656 / 0.952 / 0.413 | 0.757 / 0.762 / 0.347 |
| DA100 | 0.565 / 1.111 / 0.432 | 0.590 / 1.064 / 0.397 | 0.669 / 0.921 / 0.333 |
| Dg100 | 0.627 / 1.008 / 0.412 | 0.649 / 0.958 / 0.397 | 0.639 / 0.977 / 0.386 |
| RHO | 0.551 / 1.136 / 0.442 | 0.583 / 1.082 / 0.417 | 0.696 / 0.876 / 0.356 |
Les fréquences de décodage par patient n'ont pas été stockées : les distances entre distributions de décodage de DA et de Dg ne sont pas calculables. Seuls ces indicateurs agrégés existent.

## 5. Diversité et HV finale (corrélation de rang de Spearman entre N_eff à la génération 150 et HV finale, sur les 100 graines de chaque scénario)
| Bras | S4-RC101 | S4-R101 | S4-C101 | S5-RC101 | S5-R101 | S5-C101 | Moyenne |
|---|---|---|---|---|---|---|---|
| E | -0.01 | -0.11 | -0.04 | -0.49 | -0.19 | -0.13 | -0.16 |
| DA25 | -0.09 | -0.11 | +0.02 | -0.49 | -0.28 | -0.08 | -0.17 |
| DA50 | -0.02 | -0.07 | -0.14 | -0.47 | -0.18 | -0.00 | -0.15 |
| DA100 | -0.08 | -0.07 | +0.05 | -0.46 | -0.20 | -0.05 | -0.13 |
| Dg100 | -0.20 | -0.15 | -0.10 | -0.50 | -0.28 | -0.19 | -0.24 |
| RHO | -0.18 | -0.20 | -0.10 | -0.31 | -0.06 | -0.17 | -0.17 |
| MIX | -0.09 | +0.01 | -0.05 | -0.22 | +nan | +0.15 | -0.04 |
Les corrélations sont négatives (moins de diversité en fin de run va avec une HV plus élevée, plus fortement dans S5-RC101), pour tous les bras. C'est une association descriptive entre graines, non causale ; elle ne distingue pas les bras entre eux.

## 6. HV selon λ par scénario
Figure : `posthoc/fig_hv_lambda.png` (HV(DA(λ)) − HV(E) par scénario). Pas de tendance commune : les écarts restent de l'ordre de quelques 10⁻³ et changent de signe selon le scénario.

## 7. Ce que ces analyses permettent et ne permettent pas
- Elles suggèrent que l'infériorité statistique de DA se concentre dans les scénarios R et RC et que la trajectoire de concentration de DA diffère de celle de Dg malgré un appariement moyen conforme.
- Elles ne démontrent aucune interaction, aucun mécanisme causal, aucune supériorité d'une représentation.
- Pour tester une interaction scénario × représentation ou l'effet de la trajectoire de concentration, il faudrait un protocole préenregistré distinct, avec stockage des fréquences de décodage par patient. Je ne le lance pas sans votre décision écrite.
