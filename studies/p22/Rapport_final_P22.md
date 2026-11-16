# Rapport final P22 (v1.0 gelé) — Évidentiel contre probabiliste dans NSGA-II à mutation guidée

Dr M. Zaghdoud · 2026-11-13 · 600 tâches (5 bras, SC6 × graines 10400–10499, n = 100), budget 6 040, HV oracle (réf. 1,2), une seule analyse, aucune relance. Résultats préenregistrés, un montage. Aucune revendication de nouveauté (RS1 non faite). Hash de l'analyse : 4540acb8…

## 1. Résultat principal
Guider la mutation de NSGA-II par une cible évidentielle ou probabiliste **ne modifie presque pas la qualité du front** : tous les bras guidés sont à moins de 0,004 de NSGA-II non guidé (0,6429).
HV moyen : GDp 0,6429 ; GEg6 0,6422 ; GDg6 0,6401 ; GE = GEgm 0,6389 ; NSGA-II 0,6429.

| Contraste primaire (IC 99 %, marge 0,005) | Moyenne | IC 99 % | Décision |
|---|---|---|---|
| P1 GE − GDp (évidentiel contre probabiliste, naturel) | −0,0040 | [−0,0072 ; −0,0008] | infériorité (en partie dans la marge) |
| P2 GEg6 − GDg6 (même durcissement γ = 6) | +0,0021 | [−0,0006 ; +0,0049] | équivalence |
| P3 GEgm − GDg6 | −0,0012 | [−0,0040 ; +0,0017] | équivalence |
| P4 GDp − NSGA-II (le guidage probabiliste aide-t-il ?) | 0,0000 | [−0,0033 ; +0,0033] | équivalence |
| P5 interaction (GEg6 − GDg6) − (GE − GDp) | +0,0061 | [+0,0020 ; +0,0104] | supériorité |
Secondaires (IC 95 %) : GE − NSGA-II −0,0040 ; GDg6 − NSGA-II −0,0028 ; GEg6 − NSGA-II −0,0007 (non distinguable) ; GEg6 − GE +0,0033 ; GDg6 − GDp −0,0028.

## 2. Lecture préenregistrée
- **Aucun avantage de l'évidentiel sur le probabiliste dans NSGA-II.** À concentration naturelle l'évidentiel est légèrement inférieur (P1, −0,004) ; après le même durcissement, équivalent (P2).
- **Le guidage n'aide pas NSGA-II** (P4 = 0 ; GE et GDg6 légèrement en dessous). L'avantage de +0,04 de l'évidentiel sur le probabiliste simple observé dans QGA2 ne se transfère pas : ici la cible ne pilote qu'environ une mutation par enfant, alors que dans QGA2 elle pilote toute la recherche.
- **P5 positive (+0,0061) : limitée à γ = 6 dans ce montage.** Elle vient de ce que le durcissement améliore légèrement l'évidentiel (GEg6 − GE +0,0033) et dégrade légèrement le probabiliste (GDg6 − GDp −0,0028). Les écarts restent de l'ordre du millième de HV, bien en dessous des écarts de QGA2 ou du +0,12 de NSGA-II sur QGA2.
- **GEgm ne remplit pas son rôle.** La calibration HV-aveugle (SC3) n'a trouvé aucun γ passant la porte : la cible évidentielle naturelle (γ = 1, q_max 0,873, entropie 0,446) est déjà plus concentrée que GDg6 (0,809 ; 0,589). La règle fixée à l'avance retient γ_m = 1, meilleur essai déclaré, donc **GEgm est identique à GE** (mêmes résultats) et P3 = GE − GDg6. Sur SC6 l'appariement n'est pas satisfait (écart relatif d'entropie 21,6 %, |Δq_max| 0,057) : P3 n'est pas une mesure de la représentation à concentration comparable (règle §8.4). Il aurait fallu un probabiliste plus concentré, ou un durcissement < 1 du côté évidentiel, ce qui n'était pas prévu.
- Comparaison aux bras QGA2 : descriptive seulement (moteurs différents).

## 3. Contrôles et incidents déclarés
Mutations : 5 998 tirées et 5 864 effectives par run pour tous les bras (mêmes décisions de muter ; les patients à équipe unique ne mutent pas, comme dans NSGA-II stocké). 15 gates passés avant gel ; reproduction bit à bit de NSGA-II sur 3 tâches. Incidents :
1. Test G3b défectueux (la docstring contenait la chaîne testée), corrigé avant gel, première sortie conservée.
2. Le précontrôle d'analyse (G7) a échoué par un défaut du test (recherche de la chaîne « hv » dans une note de la calibration) ; l'analyse s'est arrêtée avant toute lecture de HV (`p22_final_stdout_aborted_precheck_G7.txt`). Test corrigé (recherche de champs « hv ») et gel refait pour ce seul fichier (`p22_freeze2.txt`, tous les autres hash identiques) ; version défectueuse archivée.
3. Le suivi en arrière-plan a expiré deux fois à sa limite de temps ; le calcul n'a pas été interrompu.
Limites : mutation seul point d'intégration testé ; w = 0,3 hérité de P10 (informé par la HV) ; références déjà vues ; un moteur, un montage.
