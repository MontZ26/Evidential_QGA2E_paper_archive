# Rapport final P14 — concentration de la cible et références algorithmiques (DESCRIPTIF)
Date : 10 novembre 2026. Statut : **G-N échoué ; aucun test primaire ; tout est descriptif** (amendement D14-9, décision écrite du Dr Montassar Zaghdoud, 11:46/11:51). n = 200 graines (10400–10599) × 6 scénarios SC6, 9 bras, HV oracle (réf. 1,2), budget 6 040 (MOEA/D : 6 030). IC95 % : bootstrap percentile sur les graines (B = 20 000, tag 10803), non ajustés ; aucune p-valeur. Analyse unique, précontrôle OK, gel vérifié (p14_freeze1.txt).
Fichiers : p14_final_analysis.json (SHA256 voir ci-dessous), p14_final_stdout.txt, p14_calib.json, Amendement_P14_D14-9_echec_GN.md, Regle_calibration_P14.md.

## 1. Rappel de l'échec de G-N (calibration SC3 × 10300–10314, sans HV)
Aucun γ de la grille {1 ; 1,5 ; 2 ; 3 ; 4 ; 6} ne satisfait G-N (écart relatif d'entropie ≤ 10 % et |Δq_max| ≤ 0,05). Meilleur : γ = 6 (40 % ; 0,093). γ = 6 est donc « meilleure tentative, non conforme ». γe = 0,15 pour E_soft.

## 2. HV oracle moyenne (SC6, n = 200)
| Bras | HV |
|---|---|
| MOEA/D | 0,6555 |
| NSGA-II | 0,6473 |
| C0 (GA classique) | 0,6280 |
| Dg (probabiliste durci, γ=6) | 0,5273 |
| E (Dempster, QGA2-E) | 0,5233 |
| Bt (QGA2-E de base, δ=0,1π) | 0,5160 |
| B (QGA2-E de base, δ=0,05π) | 0,5005 |
| Es (Dempster adouci) | 0,4822 |
| Dp (probabiliste, γ=1) | 0,4819 |

## 3. Contrastes descriptifs (moyenne [IC95 %])
- E − Dp : +0,0414 [+0,0399 ; +0,0429] (reproduit l'avantage de P10 : +0,0459).
- **Dg − Dp : +0,0454 [+0,0439 ; +0,0469] ; E − Dg : −0,0040 [−0,0055 ; −0,0025].** Le bras probabiliste durci atteint (et dépasse légèrement) E.
- E − Es : +0,0411 ; Es − Dg : −0,0451 (Es ≈ Dp).
- Bt − B : +0,0155 [+0,0142 ; +0,0168] ; E − B : +0,0228 ; Dg − B : +0,0268.
- NSGA-II − C0 : +0,0193 [+0,0174 ; +0,0211] ; MOEA/D − C0 : +0,0275 [+0,0259 ; +0,0292] ; NSGA-II − MOEA/D : −0,0083.
- E − NSGA-II : −0,1240 ; E − MOEA/D : −0,1322 ; E − C0 : −0,1047 ; B − C0 : −0,1275.

## 4. Diagnostics de concentration (moyennes sur les générations, SC6 ; descriptifs)
E : q_ent 0,718, q_max 0,759 ; Dg : 0,840 et 0,708 ; Dp : 1,458 et 0,281 ; Es : 1,453 et 0,294. Dep/N_eff : E 0,226/28,0 ; Dg 0,136/31,9 ; Dp 0,002/39,8 ; B 0,148/30,4 ; Bt 0,366/19,2. Observation post hoc (non un gate) : sur SC6 en dynamique, Dg est plus proche de E que dans la calibration (écart d'entropie ≈ 17 %, |Δq_max| ≈ 0,05), mais toujours hors des seuils préspécifiés.

## 5. Lecture autorisée / non autorisée
Autorisé (descriptif) : (i) l'avantage de E sur le probabiliste standard est reproduit ; (ii) un probabiliste dont la cible est durcie obtient ici une HV comparable à E (E − Dg = −0,004), donc, dans ce montage, l'avantage évidentiel est compatible avec un effet de concentration de la cible ; (iii) NSGA-II et MOEA/D dépassent nettement le GA classique et tous les bras QGA2-E ; (iv) le pas δ = 0,1π améliore le QGA2-E de base.
Non autorisé : affirmer que la structure évidentielle n'apporte rien (G-N non satisfait, cibles non appariées, une famille d'instances, γ choisi sur la seule entropie de cible) ; affirmer que l'évidentiel est supérieur à D′ ; toute conclusion confirmatoire.
## 6. Écarts et incidents
Calibration lancée avant l'écriture de sa règle (aucun résultat lu) ; pilote supprimé (D14-9) ; budget MOEA/D 6 030 ; diagnostics moyennés sur les générations (non à la génération finale) ; dépôt GitHub et code gelé inchangés ; aucun rerun.

SHA256 p14_final_analysis.json : ae46582cd5a95492383de03aad177f7954977917d2f9511a0d94d746dc1f5811
