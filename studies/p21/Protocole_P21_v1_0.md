# P21 v0.1 — (A) Comparaison confirmatoire appariée NSGA-II / MOEA/D contre les bras QGA2-E ; (B) γ autour de 1 pour la cible évidentielle — CANDIDAT

Dr M. Zaghdoud · rédigé 2026-11-12 (demande de l'auteur, 06:48 : « 1 et 2 » parmi les quatre pistes proposées). **Statut : brouillon, NON gelé, NON autorisé à l'exécution.** Aucun code, test ni exécution tant que l'auteur n'a pas confirmé par écrit le texte et les décisions D21-1 à D21-8 (§6). Deux parties indépendantes, deux analyses, deux familles de contrastes.

## 0. Constat préalable sur la demande 1
Les références NSGA-II et MOEA/D **ont déjà été rejouées et appariées** en P14 : mêmes instances et mêmes graines (10400–10599, n = 200, SC6) que les bras E, Dp, Dg, avec HV oracle ; E − NSGA-II = −0,1240, E − MOEA/D = −0,1322, E − C0 = −0,1047 (descriptif, sans test préenregistré). Elles existent aussi dans P2 étape 2, P3, P4 et P5 sur d'autres graines (NSGA-II − QGA2 de −0,13 à −0,16). Ce qui **manque** : (i) un contraste confirmatoire préenregistré, avec IC, entre ces références et les bras les plus récents (DA, Dg, DA+SELR) sur les mêmes graines que ces bras (P17 Tier 1, graines 11200–11299) ; (ii) un nombre de graines et des familles d'analyse alignés sur P17–P19. C'est l'objet de la partie A.

## 1. Partie A — NSGA-II et MOEA/D contre les bras QGA2-E sur les graines de P17 Tier 1
**Question :** à budget identique (6 040 évaluations ; MOEA/D : 6 030, déclaré), l'écart de HV entre les algorithmes évolutionnaires classiques et les bras QGA2-E récents est-il confirmé, quelle est sa taille avec un IC, et dépend-il du bras QGA2-E considéré ?
**Bras nouveaux (2) :** NSGA-II et MOEA/D, exécutés par le module P14 inchangé (`run_arm14`, bras « NSGA2 » et « MOEAD », monde évidentiel nominal, compteur d'évaluation enregistreur, même HV oracle de référence 1,2). **Références stockées (P17 Tier 1, mêmes instances et graines 11200–11299, déterministes, identité vérifiée par test) :** E, DA, Dp, Dg(6), DA+SEL4, DA+SELR.
**Données :** SC6 × graines 11200–11299 (n = 100). Calcul estimé : environ 25 min (NSGA-II ≈ 3,1 s, MOEA/D ≈ 1,5 s par run).
**Contrastes primaires** (HV oracle moyen sur SC6 par graine ; bootstrap percentile, B = 20 000, rééchantillonnage conjoint des graines ; IC 99 % pour 5 primaires ; marge δ = 0,005) :
A1 NSGA-II − MOEA/D ; A2 NSGA-II − E ; A3 NSGA-II − Dg ; A4 MOEA/D − Dg ; A5 NSGA-II − DA+SELR (meilleur bras QGA2-E de P17).
Secondaires (IC 95 %) : NSGA-II − DA, − Dp, − DA+SEL4 ; MOEA/D − E, − DA, − DA+SELR ; par scénario ; temps d'exécution moyens. Décisions : supériorité si borne inf > 0 ; infériorité si borne sup < 0 ; équivalence si l'IC est entièrement dans ±0,005 ; sinon non concluant.
**Gates :** A-G1 non-régression bit à bit de NSGA-II et MOEA/D contre les fichiers P14 stockés (graine technique 10400) ; A-G2 budget exact (6 040 / 6 030) et archive enregistrant toutes les solutions évaluées ; A-G3 reproductibilité, non-fuite de l'oracle ; A-G4 références P17 : HV recalculable à partir du front stocké et empreintes archivées ; A-G5 graines autorisées.
**Lecture préenregistrée :** la comparaison porte sur un montage (SC6, budget 6 040, implémentations de P3) ; elle ne dit rien de la compétitivité hors de ce cadre. Aucune revendication de nouveauté.

## 2. Partie B — γ autour de 1 pour la cible évidentielle (compléter la courbe de P10 v3)
**Question :** où se situe l'optimum de HV en γ autour de la concentration naturelle de E (γ = 1) ? P10 v3 a montré Eg1,5 ≈ E (+0,0016 [−0,0008 ; +0,0040]), Eg2 −0,0046, Eg4 −0,013, Eg6 −0,016.
**Bras nouveaux (4) :** Eg1.1, Eg1.25 (γ entre 1 et 1,5, demandés) et Eg0.9, Eg0.8 (assouplissement léger, **ajout de Claude** pour situer l'optimum des deux côtés de E ; supprimable, voir D21-3). Même opération que Dg et Eg (puissance, renormalisation, plancher P10 ; module P14, bras « Es » avec γ_e). Références stockées : E, Dp, Dg (P14), Eg1.5, Eg2, Eg4, Eg6 (P10 v3), mêmes graines 10400–10499.
**Données :** SC6 × graines 10400–10499 (n = 100) ; environ 58 min.
**Contrastes primaires** (même agrégation ; famille de 4, IC à 99 %, marge 0,005) : B1 Eg1.1 − E ; B2 Eg1.25 − E ; B3 Eg0.9 − E ; B4 Eg0.8 − E. Secondaires (IC 95 %) : Eg1.25 − Eg1.5 ; Eg1.1 − Eg1.5 ; courbe HV(γ) sur {0,8 ; 0,9 ; 1 ; 1,1 ; 1,25 ; 1,5 ; 2 ; 4 ; 6} avec diagnostics q_max et q_ent ; Eg(γ) − Dg ; par scénario. Aucun γ n'est choisi d'après la HV ; l'optimum se lit sur la courbe, comme description, non comme un nouveau réglage.
**Gates :** B-G1 γ = 1 reproduit E stocké bit à bit ; B-G2 opération de durcissement identique à Dg (test d'identité à 1e-15) ; B-G3 budget, reproductibilité, non-fuite, patch restauré ; B-G4 valeurs finies ; B-G5 non-régression de Eg1.5, Eg2 sur une graine technique contre P10 v3.
**Lecture :** courbe non monotone avec un maximum entre 0,9 et 1,25 = E est près de l'optimum de ce réglage ; maximum à γ < 0,9 ou > 1,25 = la concentration naturelle de E n'est pas optimale ; plateau = insensible. Aucune causalité au-delà d'un montage ; w = 0,3 hérité de P10 (informé par la HV, déclaré).

## 3. Données et séparation
A : graines 11200–11299 ; B : 10400–10499 ; techniques : 10400–10401, 10290–10299. Les HV des références ont déjà été vues (P14, P10 v3, P17) ; déclaré. Une seule analyse par partie ; aucun fichier manquant imputé ni relancé.

## 4. Règles communes
HV lue seulement à l'analyse unique ; pas de relance pour améliorer ; incidents déclarés ; résultats « préenregistrés, un montage » ; pas de revendication de nouveauté (RS1 non faite) ; la session reste active pendant les calculs (deux redémarrages de conteneur en P18 ont montré que sinon le calcul s'arrête).

## 5. Estimation globale
Partie A ≈ 25 min + partie B ≈ 58 min, analyses et rapport ≈ 30 min : environ 2 h au total sur 2 cœurs.

## 6. Décisions à confirmer (défauts proposés)
D21-1 deux parties indépendantes, une analyse chacune ; D21-2 partie A : NSGA-II et MOEA/D sur les graines 11200–11299, références P17 stockées, cinq primaires A1–A5 (IC 99 %, marge 0,005) ; D21-3 partie B : quatre γ = {1,1 ; 1,25 ; 0,9 ; 0,8} (supprimer 0,9 et 0,8 si tu veux seulement « entre 1 et 1,5 ») ; D21-4 partie B : n = 100, graines 10400–10499, quatre primaires B1–B4, IC 99 % ; D21-5 références stockées, appariées, empreintes archivées ; D21-6 gates §1 et §2 ; D21-7 lecture préenregistrée §1 et §2 ; D21-8 autorisation d'enchaîner implémentation, tests, gel, exécution continue, analyse unique et rapport sans arrêt si les gates passent.

## 7. Confirmation et déclarations (v1.0, avant tout résultat)
**Autorisation de l'auteur, 2026-11-12 06:52 :** « Exécuter alors avec mon autorisation complète et sans arrêt ». Lecture : confirmation de D21-1 à D21-8 avec les défauts proposés (une seule numérotation P21, parties A et B, γ = 1,1 ; 1,25 ; 0,9 ; 0,8, n = 100 par partie). La question sur la promotion de Eg − Dg en contraste primaire est restée sans réponse : **non promu**, reste secondaire (Eg(γ) − Dg, IC 95 %). Ordre : partie A puis partie B, une analyse par partie, rapport unique.
**Déclarations d'implémentation :** modules P14 inchangés ; `p21.py` ajoute seulement une liste blanche de graines ; 20 gates passés avant gel (`p21_tests_stdout.txt`) ; BG5 et AG1 comparent bit à bit aux fichiers P14/P20 stockés. Information non-gate : q_max moyen sur un run de contrôle (S4-RC101, 10400) Eg0.8 0,734 ; E 0,841 ; Eg1.1 0,806 ; Eg1.25 0,850 (non monotone pour Eg1.1, observation descriptive d'un seul run). Pour la partie B, la graine de bootstrap est `sub_rng("p21_final_B", 11996)`, pour A `sub_rng("p21_final_A", 11995)`. Diagnostics q_max/q_ent de la partie B lus sur les 9 niveaux de γ (E, Eg0.8…Eg6, Dg, Dp) aux générations 1, 25, 50, 100, 150.
