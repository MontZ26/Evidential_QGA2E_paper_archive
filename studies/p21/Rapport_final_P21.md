# Rapport final P21 (v1.0 gelé) — A : NSGA-II / MOEA/D appariés ; B : γ autour de 1 pour E

Dr M. Zaghdoud · 2026-11-12 · une analyse par partie, aucune relance, 20 gates passés avant gel. Résultats préenregistrés, un montage (SC6, budget 6040, HV oracle, réf. 1,2). Aucune revendication de nouveauté (RS1 non faite). Hash des analyses : A 122a8fcf…, B c3d096fc…

## Partie A — graines 11200–11299, n = 100, appariée aux bras P17 Tier 1
HV moyen : MOEA/D 0,6586 ; NSGA-II 0,6522 ; DA+SELR 0,5384 ; DA+SEL4 0,5342 ; Dg 0,5300 ; DA 0,5264 ; E 0,5264 ; Dp 0,4837.
| Contraste | Moyenne | IC 99 % | Décision |
|---|---|---|---|
| A1 NSGA-II − MOEA/D | −0,0065 | [−0,0092 ; −0,0037] | infériorité (IC en partie hors de ±0,005) |
| A2 NSGA-II − E | +0,1258 | [+0,1214 ; +0,1301] | supériorité |
| A3 NSGA-II − Dg | +0,1221 | [+0,1177 ; +0,1265] | supériorité |
| A4 MOEA/D − Dg | +0,1286 | [+0,1239 ; +0,1331] | supériorité |
| A5 NSGA-II − DA+SELR | +0,1138 | [+0,1099 ; +0,1176] | supériorité |
**Lecture :** l'écart de 0,11 à 0,13 entre les algorithmes classiques (sans composante évidentielle) et tous les bras QGA2-E est confirmé, apparié, y compris face au meilleur bras QGA2-E. MOEA/D dépasse légèrement NSGA-II (0,0065). Temps moyen par tâche (6 scénarios-graines, 2 algorithmes) : 4,3 s.

## Partie B — graines 10400–10499, n = 100
HV moyen : Dg 0,5247 ; Eg1.5 0,5220 ; Eg1.1 0,5214 ; Eg1.25 0,5210 ; E 0,5204 ; Eg0.9 0,5196 ; Eg2 0,5157 ; Eg0.8 0,5156 ; Eg4 0,5073 ; Eg6 0,5044 ; Dp 0,4792.
| Contraste | Moyenne | IC 99 % | Décision |
|---|---|---|---|
| B1 Eg1.1 − E | +0,0010 | [−0,0015 ; +0,0036] | équivalence |
| B2 Eg1.25 − E | +0,0006 | [−0,0020 ; +0,0031] | équivalence |
| B3 Eg0.9 − E | −0,0007 | [−0,0031 ; +0,0017] | équivalence |
| B4 Eg0.8 − E | −0,0047 | [−0,0069 ; −0,0025] | infériorité |
Secondaires (IC 95 %) : Eg1.5 − E +0,0016 [−0,0007 ; +0,0040] ; Eg1.25 − Eg1.5 −0,0010 ; Eg1.1 − Eg1.5 −0,0006 (non concluants). Eg(γ) − Dg : Eg1.1 −0,0033 [−0,0057 ; −0,0011] ; Eg1.25 −0,0038 ; Eg0.9 −0,0051 ; Eg0.8 −0,0091 (tous négatifs, IC excluant 0). Tous les Eg − Dp ≈ +0,036 à +0,042.
Diagnostics (génération 150, q_max / entropie) : Eg0.8 0,780/0,679 ; Eg0.9 0,824/0,585 ; E 0,851/0,525 ; Eg1.1 0,875/0,471 ; Eg1.25 0,898/0,419 ; Eg1.5 0,911/0,388 ; Dg 0,805/0,646. Le q_max croît bien avec γ (le run de contrôle isolé faisait exception).
**Lecture :** la courbe HV(γ) est un plateau de γ = 0,9 à 1,5 (écarts ≤ 0,002, équivalents à E), avec un maximum nominal à 1,5 non distinguable de E ; elle baisse nettement en dessous (0,8) et au-dessus (γ ≥ 2). L'optimum se situe donc autour de E, sans gain détectable à durcir légèrement. À concentration comparable, Dg reste légèrement au-dessus de chaque Eg (≈ +0,003 à +0,009 en HV), ce qui ne montre aucun avantage de la représentation évidentielle ; notez que Dg (q_max 0,805) est moins concentré que Eg1.1 et au-delà, donc l'appariement de concentration n'est pas exact. Contraste Eg − Dg resté secondaire.

## Limites et incidents
w = 0,3 hérité de P10 (informé par la HV, déclaré). Références déjà vues (P14, P17, P20). Le watcher a expiré une fois à la limite de temps ; calcul non interrompu. Aucun fichier manquant ni relance. La partie A compare à des algorithmes classiques sans intégration évidentielle : elle ne dit rien d'un GA classique évidentiel.
