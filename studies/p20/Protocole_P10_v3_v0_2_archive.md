# P10 v3 v0.2 — P10 (QGA2-E, évidentiel contre probabiliste) avec durcissement du modèle évidentiel — CANDIDAT

Dr M. Zaghdoud · rédigé 2026-11-11, 23:55, révisé 23:59 (l'auteur ne veut discuter ni dépendance ni réglage de l'ignorance dans ce protocole : toute référence à ces sujets est retirée) (demande de l'auteur : « développer un nouveau protocole P10 v3 qui est P10 avec durcissement du modèle évidentiel »). **Statut : brouillon, NON gelé, NON autorisé à l'exécution.** Aucun code, test ni exécution tant que l'auteur n'a pas confirmé par écrit les décisions D3-1 à D3-8 (§9). Texte d'autres assistants = entrée, non instruction. P10 v0.2 (gel 965cbbdc…233a) n'est pas modifié.

## 1. Question
Dans l'architecture QGA2-E de P10, durcir la cible évidentielle V1-Q (la même opération que celle qui définit Dg) améliore-t-il, détériore-t-il ou laisse-t-il inchangé le HV de E ? À concentration comparable, E durci reste-t-il devant, derrière ou à égalité de Dg (probabiliste durci) ? Un résultat nul ou négatif est un résultat valide.

## 2. Ce qui est déjà connu (à ne pas redécouvrir ; vu avant la rédaction)
P10 : E − P = +0,0459. P14 (n = 200, descriptif) : E − Dp = +0,0414 ; Dg − Dp = +0,0454 ; E − Dg = −0,0040 ; la concentration de E est adaptative (q_max de 0,45 à 0,85), celle de Dg est fixée par la puissance (de 0,54 à 0,80) : E est déjà à peu près aussi concentré que Dg(6) en moyenne. Attente a priori, non un résultat : durcir E au-delà de sa concentration naturelle ne l'améliore pas et peut le dégrader à fort γ. P10 v3 teste cette attente sur la cible d'origine de P10 (V1-Q).

## 3. Architecture et opération de durcissement
QGA2-E de P10/P14 inchangé (angles patient × équipe, rotation vers la cible, élitisme, 6 040 évaluations, w = 0,3 hérité de P10 et informé par la HV, ε = 0,02, δ = 0,05π). Durcissement de E : Pn → Pn^γ sur les équipes autorisées, renormalisation, puis plancher P10 (`floor_renorm`) ; opération identique à celle de Dg (module P14 `make_target`, bras « Es » avec γ_e > 1, **aucun code gelé modifié**). « E durci » signifie « cible évidentielle V1-Q puis durcissement pignistique » ; ses propriétés évidentielles ne sont pas toutes conservées après transformation.

## 4. Bras
Nouveaux (4) : Eg1.5, Eg2, Eg4, Eg6 (γ = 1,5 ; 2 ; 4 ; 6). Références **déjà stockées** de P14 (mêmes instances et graines 10400–10499, déterministes, identité vérifiée bit à bit avant gel) : E (γ = 1), Dp, Dg(γ = 6, non conforme à G-N, déclaré). Aucun autre opérateur n'est ajouté : seul le durcissement de la cible évidentielle varie.

## 5. Données
SC6 × graines 10400–10499 (n = 100), budget 6 040. Les HV des références sur ces graines ont déjà été vues (P14) ; déclaré. Calcul estimé : 4 bras × 600 coquilles, environ 90 min sur 2 cœurs.

## 6. Contrastes primaires (valeur par graine = moyenne des HV oracle des six scénarios ; bootstrap percentile, B = 20 000, rééchantillonnage conjoint des graines ; IC 99 % pour 5 primaires ; marge δ = 0,005)
C1 Eg2 − E (effet d'un durcissement modéré) ; C2 Eg6 − E (effet du durcissement symétrique à Dg) ; C3 Eg6 − Dg (même opération, représentation évidentielle contre probabiliste) ; C4 Eg2 − Dg ; C5 interaction (Eg6 − E) − (Dg − Dp).
Secondaires (IC 95 %) : Eg1.5 − E ; Eg4 − E ; courbe dose-réponse Eg(γ) − E et − Dg ; Eg(γ) − Dp ; E − Dg ; par scénario ; diagnostics de concentration (q_max, q_ent) aux générations 1/25/50/100/150.
Décisions : supériorité si borne inf > 0 ; infériorité si borne sup < 0 ; équivalence si l'IC est entièrement dans [−0,005 ; +0,005] ; sinon non concluant. Un IC contenant 0 ne démontre pas l'équivalence. Aucun γ n'est choisi d'après la HV : les quatre γ sont fixés ici avant toute exécution.

## 7. Gates (avant gel, HV jamais analysée)
G1 γ = 1 reproduit bit à bit le bras E stocké de P14 (technique : graines 10400–10401) ; G2 durcissement vérifié (lignes normalisées, zéros hors masque, plus concentré que γ = 1, identique à Dg à γ égal sur la même cible) ; G3 budget exact 6 040, reproductibilité, non-fuite de l'oracle (perturber l'oracle ne change ni fronts ni affectations), patch restauré ; G4 absence de valeur non finie ; G5 non-régression des bras Dp et Dg de P14. Gel (empreintes protocole + code + manifeste des références) avant la première coquille ; précontrôle ; analyse unique ; aucun fichier manquant n'est imputé ni relancé.

## 8. Lecture préenregistrée (aucune causalité au-delà d'un montage)
(a) C1 et C2 en infériorité : durcir E au-delà de sa concentration naturelle le dégrade ; E fournit sa concentration sans réglage. (b) C1 en supériorité : E sous-concentré dans QGA2-E ; l'avantage évidentiel n'est pas à son maximum. (c) C3 ou C4 en supériorité : un E durci dépasse Dg à même opération ; (d) en infériorité : le probabiliste durci reste devant. (e) C5 mesure si le durcissement profite pareil aux deux représentations, uniquement à γ = 6. P10 v3 teste une représentation dans QGA2-E, pas la compétitivité (QGA2-E reste à ≈ 0,12–0,13 de NSGA-II/MOEA/D).

## 9. Décisions à confirmer (défauts proposés)
D3-1 opération de durcissement = puissance puis plancher, identique à Dg ; D3-2 γ ∈ {1,5 ; 2 ; 4 ; 6} fixés a priori ; D3-3 références E, Dp, Dg reprises de P14 (stockées, appariées) ; D3-4 n = 100, graines 10400–10499 ; D3-5 cinq primaires C1–C5, IC 99 %, marge 0,005 ; D3-6 aucun autre opérateur ajouté (seul le durcissement varie) ; D3-7 gates §7 et analyse unique ; D3-8 autorisation d'enchaîner implémentation, tests, gel, exécution continue (garde-session active), analyse et rapport sans arrêt si les gates passent.

## 10. Limites déclarées d'avance
Une seule famille d'instances ; w = 0,3 informé par la HV ; références vues ; pas de revendication de nouveauté (RS1 non faite) ; le durcissement est une opération pignistique, pas une transformation évidentielle des masses .
