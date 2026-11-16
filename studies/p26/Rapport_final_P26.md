# Rapport final P26 — cible probabiliste à exposant variable (séparer représentation et calendrier)

Étude préenregistrée, 60 graines × 6 géographies de benchmark (360 instances), HV oracle (réf. 1,2), budget 6040, IC 99 % marginaux, marge 0,005, une seule analyse (p26_final_analysis.json), aucun rerun.

## Conformité de la trajectoire (vérifiée sans recalibration)
| w | référence | calendrier γ_t | écart d'entropie moyen | |Δq_max| moyen | conforme |
|---|---|---|---|---|---|
| 0,3 | E | 3→6 sur 90 gén. | 4,8 % | 0,031 | oui |
| 0,3 | DA | 3→6 sur 90 gén. | 5,0 % | 0,032 | oui |
| 0,7 | E | 3→6 sur 30 gén. | 5,9 % | 0,015 | oui |
| 0,7 | DA | 3→6 sur 30 gén. | 21,7 % | 0,061 | non (descriptif) |

## Contrastes (différence, IC 99 %, décision ; Bonferroni identique partout)
| w | L1 E−Dgt | L2 DA−Dgt | L3 DA−E | L4 DA−Dp | L5 DA−Dg(6) |
|---|---|---|---|---|---|
| 0,3 | +0,0066 [+0,0035 ; +0,0095] sup. | +0,0061 [+0,0031 ; +0,0089] sup. | −0,0005 équiv. | +0,0224 sup. | −0,0071 inf. |
| 0,7 | −0,0050 [−0,0084 ; −0,0017] inf. | −0,0045 (descriptif) | +0,0006 équiv. | +0,0248 sup. | −0,0001 équiv. |

HV moyens : w=0,3 E 0,2013, DA 0,2008, Dp 0,1783, Dgt 0,1947, Dg(6) 0,2078 ; w=0,7 : 0,2066 / 0,2072 / 0,1824 / 0,2117 / 0,2073.

## Lecture (selon la règle préenregistrée)
- w=0,3 (trajectoire conforme) : E supérieur à Dgt → l'avantage n'est pas expliqué par le calendrier d'entropie/q_max seul (positif dans 4 géographies sur 6).
- w=0,7 (référence E conforme) : Dgt supérieur à E dans les 6 géographies → un calendrier probabiliste fait mieux que la règle de Dempster.
- Le signe change avec w : ni avantage ni désavantage général de la représentation. Dg(6) fixe bat Dgt et DA à w=0,3.
- Limites : appariement sur deux diagnostics seulement (JS des distributions décodées à g=150 : 0,17–0,33 ; L1 0,74–0,96) ; mêmes géographies que P25b ; une seule référence non conforme ; les deux bras Dgt sont identiques pour E et DA.

## Incidents déclarés
Dry run initial en échec (clé de paramètre inexistante) corrigé avant le gel, diagnostics ajoutés avant le gel ; lancement détaché accidentel arrêté puis relancé en tâche surveillée ; porte de calibration non satisfaite pour (w=0,7, DA) ; pilote sans problème ; aucun rerun.
