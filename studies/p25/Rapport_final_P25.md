# Rapport final P25 — Évaluation indépendante sur une nouvelle famille d'instances
Date : 15 nov. 2026. Protocole : /tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p25/Protocole_P25_validation_independante_v0_1.md. Analyse : /tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p25/p25_final_analysis.json (une seule exécution).

## Déroulement
Tests (passés) → calibration HV-aveugle (45 instances, graines 14700–14714) → sélection (γ=6 à w=0,3, **porte non satisfaite**, meilleur essai ; γ=4 à w=0,7, porte satisfaite ; 8 bras car Dg_cal(0,3)=Dg(6)) → pilote 20 tâches (sans problème, 1,12 h estimées) → essai à sec → gel vérifié → exécution 360 tâches (graines 14000–14059, 6 scénarios, 8 bras) → précontrôle OK → analyse unique.

## Résultats (HV oracle, moyenne par graine sur 6 scénarios ; IC 99 % ; δ = 0,005)
| Contraste | Différence | IC 99 % | Décision | Référence antérieure |
|---|---|---|---|---|
| K1 DA−E, w=0,3 | −0,0005 | [−0,0015 ; +0,0005] | équivalence | P23 : équivalence (−0,0009) |
| K1 DA−E, w=0,7 | +0,0001 | [−0,0018 ; +0,0019] | équivalence | P24 : supériorité (+0,0039) |
| K2 DA−Dg(6), w=0,3 (= K5) | −0,0072 | [−0,0099 ; −0,0044] | infériorité | P23 : infériorité (−0,0039) ; **appariement non conforme** |
| K2 DA−Dg(4), w=0,7 | −0,0047 | [−0,0076 ; −0,0019] | infériorité | P24 : infériorité (−0,0105, non apparié) ; **appariement conforme** |
| K3 Dg−E, w=0,3 | +0,0067 | [+0,0038 ; +0,0096] | supériorité | — |
| K3 Dg−E, w=0,7 | +0,0048 | [+0,0018 ; +0,0078] | supériorité | — |
| K4 DA−Dp, w=0,3 / 0,7 | +0,0216 / +0,0216 | [+0,0189 ; +0,0244] / [+0,0188 ; +0,0247] | supériorité | grand effet des études précédentes |

HV moyens : w=0,3 — E 0,3179, DA 0,3174, Dg(6) 0,3246, Dp 0,2959 ; w=0,7 — E 0,3218, DA 0,3219, Dg(4) 0,3266, Dp 0,3003. Niveau absolu plus bas que P23/P24 (≈0,5) : famille plus difficile ; comparaison de niveaux non pertinente (graines et instances différentes).
Appariement (moyennes gens. 1–150, SC6-P25) : w=0,3 écart d'entropie 23 %, |Δq_max| 0,133 → non conforme (K2/K5 à w=0,3 non interprétables comme comparaisons à concentration égalée) ; w=0,7 écart 5,9 %, |Δq_max| 0,020 → conforme.
Par géométrie (K1 w=0,7) : U −0,0011, K +0,0018, M −0,0004 ; K2 négatif dans les six scénarios aux deux w.

## Lecture
1. Dp est nettement inférieur à E et DA (≈ +0,02) : reproduit.
2. DA ≈ E : reproduit à w=0,3 ; **non reproduit à w=0,7** (P24 : DA > E ; ici équivalence).
3. Dg ≥ DA : direction reproduite (infériorité de DA) ; la seule comparaison conforme (w=0,7) donne −0,0047, donc, sur cette famille, la cible probabiliste affûtée n'est pas inférieure à l'évidentielle à concentration appariée.
4. Dg > E (nouveau contraste préenregistré) : supériorité aux deux w.
5. Aucune preuve d'un avantage propre de la représentation évidentielle ; cela ne prouve pas que la concentration est le seul mécanisme.

## Incidents déclarés
(a) premier lancement détaché arrêté après avoir terminé 1 tâche (fichier conservé, même code gelé) ; relance en tâche de fond ; (b) le script de gel a été ré-exécuté après la fin de l'exécution (fichiers inchangés ; la vérification du gel avait été faite avant le lancement) ; (c) porte de calibration non satisfaite à w=0,3 ; (d) un seul jeu de graines, un seul algorithme, un seul générateur d'évidence (synthétique) ; (e) nouveaux scénarios fondés sur géographies synthétiques, non sur les fichiers Solomon.
Aucune revendication de nouveauté.
