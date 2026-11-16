# Rapport final P10 v3 — durcissement du modèle évidentiel dans QGA2-E

Dr M. Zaghdoud · 2026-11-12 · protocole `Protocole_P10_v3_v1_0.md` (confirmé par l'auteur à 00:04, « Je confirme [le] texte [du] protocole et [les] décisions », puis « exécuter sans arrêt » à 00:07) · gel `p20_freeze1.txt` · analyse `p20_final_analysis.json` (SHA256 aff9466b…, voir fichier), exécutée une seule fois après contrôle préalable OK (600 fichiers, 100 graines 10400–10499 × 6 scénarios × 4 bras, budget 6 040 exact). Références E, Dp, Dg : fichiers P14 stockés, mêmes graines (HV déjà vues, déclaré).

## 1. Réponse courte
Durcir la cible évidentielle V1-Q ne l'améliore pas : le HV baisse quand γ augmente. À γ = 1,5 l'effet est nul dans la précision de l'étude (+0,0016 [−0,0008 ; +0,0040]), à γ = 2 il est faible mais négatif (−0,0046), à γ = 4 et 6 il est net (−0,013 ; −0,016). E durci reste en dessous de Dg à tous les niveaux testés. La concentration naturelle de E, qui n'a aucun réglage, est donc au voisinage du meilleur niveau parmi ceux essayés.

## 2. Contrastes primaires (IC 99 %, marge 0,005, bootstrap par graine, n = 100)
| Contraste | Moyenne | IC 99 % | Décision |
|---|---|---|---|
| C1 Eg2 − E | −0,0046 | [−0,0076 ; −0,0016] | infériorité (effet inférieur à la marge de 0,005) |
| C2 Eg6 − E | −0,0160 | [−0,0188 ; −0,0130] | infériorité |
| C3 Eg6 − Dg | −0,0204 | [−0,0231 ; −0,0177] | infériorité |
| C4 Eg2 − Dg | −0,0090 | [−0,0119 ; −0,0061] | infériorité |
| C5 (Eg6 − E) − (Dg − Dp) | −0,0615 | [−0,0654 ; −0,0577] | infériorité |

HV moyen : Dp 0,4792 · E 0,5204 · Eg1,5 0,5220 · Eg2 0,5157 · Eg4 0,5073 · Eg6 0,5044 · Dg 0,5247.
Secondaires (IC 95 %) : Eg1,5 − E +0,0016 [−0,0008 ; +0,0040] ; Eg4 − E −0,0130 ; Eg1,5 − Dg −0,0028 [−0,0049 ; −0,0006] ; E − Dg −0,0044 [−0,0066 ; −0,0022] (reproduit P14 : −0,0040) ; Dg − Dp +0,0455 ; E − Dp +0,0411 ; tous les Eg(γ) restent au-dessus de Dp (+0,025 à +0,043).
Par scénario : C1 est négatif dans 4 scénarios sur 6 et positif dans S5-RC101 et S5-R101 (+0,007) ; C2 et C3 sont négatifs dans les 6.

## 3. Concentration (génération 150 : q_max / entropie)
E 0,851 / 0,525 · Dg 0,805 / 0,646 · Eg1,5 0,911 / 0,388 · Eg2 0,922 / 0,362 · Eg4 0,927 / 0,350 · Eg6 0,928 / 0,349 · Dp 0,281 / 1,452.
Point à signaler : le protocole supposait que Eg2 serait moins durci que Dg(6). C'est faux : tous les bras Eg sont **plus** concentrés que Dg, dès γ = 1,5 (q_max 0,911 contre 0,805). C3 et C4 comparent donc des bras E plus concentrés à un Dg moins concentré ; ils ne sont pas à concentration comparable et ne se lisent pas comme des effets de représentation. Les bras Eg4 et Eg6 atteignent la même concentration finale (0,927 ; 0,928) mais diffèrent de 0,003 en HV : l'écart vient surtout du début de run (q_max à la génération 1 : 0,72 contre 0,77).

## 4. Lecture préenregistrée (§8 du protocole)
- C1 et C2 en infériorité : durcir E au-delà de sa concentration naturelle le dégrade, aux deux niveaux testés (pour C1 l'effet est inférieur à la marge de 0,005). Cela ne démontre pas que la concentration naturelle est optimale : Eg1,5 est indistinguable de E, et γ < 1,5 non testé ne peut pas être exclu.
- C3, C4 : comparaisons de performance entre bras, non à concentration comparable (§3 ci-dessus).
- C5 : interaction à γ = 6 seulement : le durcissement à γ = 6 profite fortement à Dp (+0,046) et nuit à E.
- Cadre : un montage, SC6, budget 6 040 ; QGA2-E reste à environ 0,12–0,13 de NSGA-II/MOEA/D (non rejoués ici).
- Ce que cela change pour la question « E contre Dg » : à γ = 1 (E) et γ = 1,5, E est à −0,0044 et −0,0028 de Dg(6). Dg(6) étant calibré sur E, on ne gagne pas à durcir E davantage ; le meilleur probabiliste durci (γ ≈ 6–8) reste légèrement devant E.

## 5. Incidents et transparence
1. Test G2b (identité de l'opération de durcissement) : la première rédaction contenait une disjonction (`… or …`) qui l'affaiblissait ; elle a été remplacée avant le gel par une condition stricte (un seul appel à `make_target(g)` dans `run_arm14` et même table des γ pour Dg et Es), puis les 14 contrôles ont été relancés (14 PASS) ; sortie du premier passage conservée (`p20_tests_stdout_run1.txt`).
2. Test G0b : le recalcul du HV à partir du front stocké et le budget ont été vérifiés sur un échantillon (1 fichier sur 37, soit 17 fichiers sur 600), pas sur les 600 ; l'existence des 600 fichiers et leurs empreintes (manifeste de gel) sont vérifiées pour tous.
3. Aucun incident d'exécution : pas de redémarrage du conteneur, attente active maintenue, 600 fichiers en 3 470 s.
4. Références E, Dp, Dg : HV déjà vues en P14 (déclaré) ; w = 0,3 hérité de P10 (informé par la HV, déclaré).
5. Aucun code gelé modifié ; GitHub non touché ; aucune relance destinée à améliorer un résultat ; analyse exécutée une seule fois.
6. Lecture de l'autorisation : confirmation du 00:04 (texte v0.3 et décisions D3-1 à D3-8 tels qu'écrits) et message du 00:07 (« exécuter sans arrêt »).

## 6. Décisions en attente (aucune exécutée)
Tester γ < 1,5 et entre 1 et 1,5 pour situer l'optimum autour de E ; rejouer NSGA-II/MOEA/D sur ces graines ; choix de l'angle du papier ; export de littérature (RS1).
