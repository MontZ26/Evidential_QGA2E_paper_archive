# Rapport P1-M — résultats confirmatoires (3 novembre 2026)

## Verdict
**Les deux hypothèses principales ne sont pas confirmées.** DRI_exp ne bat ni Rand (H-M2) ni Width (H-M3) en hypervolume vrai. L'effet est indistinguable de zéro. Résultat nul, pas négatif net.

## Déroulé (conforme au protocole)
- Pilote (graines techniques 3290-3299) : SD inter-graines 0,0133 / 0,0148 ; n calculé 24 / 29 ; n retenu = 100 (plancher de la grille). Aucune réévaluation déclenchée.
- Gel SHA-256 (p1m_freeze.txt) avant toute donnée confirmatoire. Run : graines 3300-3399, 600 instances, 0 infaisable, 0 ensemble vide.
- Aucune hypothèse, règle ni famille modifiée après les résultats. Aucun re-run.

## Résultats principaux (Wilcoxon unilatéral, Holm sur 2, niveau graine)
| Hypothèse | Diff. moyenne HV | IC95 % bootstrap | p | p Holm | Succès |
|---|---|---|---|---|---|
| H-M2 DRI_exp − Rand | +0,0004 | [−0,0029 ; +0,0037] | 0,49 | 0,99 | non |
| H-M3 DRI_exp − Width | −0,0012 | [−0,0052 ; +0,0028] | 0,82 | 0,99 | non |

Graines positives : 48/100 et 44/100. Sensibilité sur 600 instances : p = 0,36 et 0,76 (même conclusion).

## HV moyen par bras (descriptif)
N 0,5191 ; Rand 0,5203 ; DRI_exp 0,5207 ; Width 0,5219 ; T (oracle) 0,5394.
- T − N = +0,0202 (IC [0,017 ; 0,023], 87/100 positifs) : connaître la vérité aide nettement, donc le banc d'essai est sensible.
- DRI_exp − N = +0,0016 (IC [−0,0018 ; 0,0048], p = 0,17) : l'observation du budget fixé n'améliore pas de façon détectable les fronts.
- Les observations ne comblent qu'environ 8 % de l'écart N → T (0,0016 / 0,0202). Le budget d'observations est petit par rapport à l'ignorance.

## Ignorance (descriptif)
Largeur moyenne wA : N 0,331 → Rand 0,315, DRI_exp 0,306, Width 0,303. Erreur sur A : 0,216 → 0,210 / 0,209 / 0,208. Les observations réduisent l'ignorance de façon modeste, et ces stratégies sont presque équivalentes. DRI_exp ne fait pas mieux que Width.

## H-M5 (l'ignorance prédit-elle l'erreur de la fitness nominale ?), Holm sur 2
- f2 : Δρ = +0,213, IC [0,155 ; 0,273], p Holm = 1e-8 → **confirmée** (l'ignorance prédit mieux l'erreur que la référence).
- f3 : Δρ = −0,213, IC [−0,248 ; −0,178] → **non confirmée, et effet significatif en sens inverse** (la référence prédit mieux).
- Lecture : un résultat partiel et mixte. Les deux effets sont de même amplitude et de signes opposés, ce qui suggère une propriété de construction de f2/f3 plus qu'un effet de l'ignorance. À examiner avant toute conclusion.

## H-M6 (descriptif) : réduction de l'écart optimiste/pessimiste ΓHV
Rand 0,0177 ; Width 0,0309 ; DRI_exp 0,0366 (ICs étroits, bien séparés). DRI_exp réduit le plus l'écart entre fronts optimiste et pessimiste. C'est le seul avantage net de DRI_exp, et il ne se traduit pas en hypervolume vrai.

## Limites et réserves
1. Pouvoir : n = 100 détecte environ 0,0066 (80 %, δ prévu 0,01 ; effet observé ~0,0004). On ne peut pas exclure un effet réel inférieur à 0,005.
2. QGA avec κ = 0 : ce n'est pas le test du QGA à trois amplitudes du manuscrit.
3. Étalonnage de Ā non concluant (convention nominale non calibrée). Six choix d'implémentation encore à valider par vous.
4. Le test b (O17.a) n'est pas discriminant sur les graines techniques.
5. Note : mon indicateur « nombre d'observations identique entre bras » inclut le bras N (0 observation) et sort donc faux ; entre Rand, Width et DRI_exp, il est identique (contrôlé sur un exemple, 30 chacun). Non recalculé sur les 600 instances dans ce rapport.
6. Analyse faite une seule fois, après le gel.

## Ce que ce résultat permet de dire honnêtement
- Peut se dire : sous ce banc d'essai, une acquisition ciblée de l'ignorance (DRI_exp) ne fournit pas de gain détectable en hypervolume par rapport au hasard ou à la largeur ; elle réduit mieux l'écart entre mondes (ΓHV) ; la largeur d'ignorance prédit l'erreur de f2 (pas de f3).
- Ne peut pas se dire : que DRI_exp améliore l'optimisation, ou que l'ignorance explicite apporte un gain de qualité des fronts.
- Décisions qui vous reviennent : donner suite ou non (budget d'observations plus élevé, ignorance dans la fitness, κ ≠ 0 seraient des études nouvelles, non menées ici), et la lecture de H-M5.

Fichiers : p1m_conf.json, p1m_final_analysis.json, p1m_pilot_analysis.json, p1m_freeze.txt, Protocole_P1M_v1_14_gele.md, Plan_puissance_P1M_v0_8_gele.md.
