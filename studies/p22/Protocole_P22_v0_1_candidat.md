# P22 v0.1 — Évidentiel contre probabiliste dans un GA classique (NSGA-II à mutation guidée) — CANDIDAT

Dr M. Zaghdoud · rédigé 2026-11-12 (demande de l'auteur, 10:51). **Numérotation : P21 est déjà pris (rapport final P21 livré) ; ce protocole est donc P22.** Statut : brouillon, NON gelé, NON autorisé à l'exécution. Aucun code, test ni calcul avant confirmation écrite de D22-1 à D22-8 (§7).

## 1. Question
Dans un GA classique (NSGA-II, sans composante quantique), le fait de guider la recherche par un modèle évidentiel plutôt que probabiliste change-t-il la qualité du front (HV oracle) ? Même question que dans QGA2 (P10, P14, P19, P10 v3), posée dans un autre moteur. Elle comble le point resté ouvert après P21 : NSGA-II et MOEA/D n'ont aucune intégration, ni évidentielle ni probabiliste.

## 2. Point d'intégration (décision de conception, à confirmer, D22-1)
Dans QGA2, la cible q (par patient, issue du premier front) déplace les angles de rotation. Dans NSGA-II il n'y a pas d'angles ; l'analogue le plus proche et le moins intrusif est la **mutation guidée** : à chaque génération, la cible q est construite par la même fonction que dans QGA2 (`p10.target`, sources = premier front de la population courante, même plancher P10, w = 0,3, ε = 0,02). Quand le gène d'un patient doit muter (même taux 1/n_p que NSGA-II), la nouvelle équipe est tirée selon q, restreinte aux équipes admissibles autres que l'équipe courante, renormalisée. Rien d'autre ne change : sélection, croisement (pc = 0,9), taille de population (40), 150 générations, budget 6 040 évaluations, élitisme, archive et HV oracle sont identiques à NSGA-II. La différence entre bras est uniquement la loi du tirage de mutation.
Limite déclarée : « évidentiel » signifie ici « cible évidentielle (Dempster puis probabilité pignistique) utilisée comme loi de mutation », comme en P19 la structure évidentielle intervient en amont de la cible. Le choix de la mutation comme point d'intégration est une décision de Claude ; d'autres points (objectif supplémentaire, biais de croisement) ne sont pas testés.

## 3. Bras (5 nouveaux, 1 référence stockée)
Référence stockée (P14, graines 10400–10499, mêmes instances) : NSGA2 (mutation uniforme).
Nouveaux, tous NSGA-II à mutation guidée :
- GDp : cible probabiliste simple (règle V0c).
- GE : cible évidentielle (règle V1).
- GDg6 : probabiliste durci, puissance γ = 6, renormalisation, plancher P10 (opération identique à Dg).
- GEg6 : évidentiel durci, même opération, γ = 6 (symétrie, comme P19).
- GEgm : évidentiel durci avec γ_m choisi HV-aveugle pour apparier la concentration de la cible de mutation (entropie et q_max) à celle de GDg6, sur SC3 × graines 11700–11714, règle de sélection de P19 (J(γ), grille 1 ; 1,25 ; 1,5 ; 2 ; 3 ; 4 ; 6, porte écart relatif d'entropie ≤ 10 % et |Δq_max| ≤ 0,05, sinon meilleur essai déclaré ; égalité : γ le plus petit). Ce bras apporte la comparaison à concentration appariée, car P10 v3 et P19 ont montré que la concentration explique l'avantage apparent de l'évidentiel.
Données : SC6 × graines 10400–10499 (n = 100). Pas de HV lue à la calibration.

## 4. Contrastes primaires (famille de 5, IC à 99 %, marge δ = 0,005)
HV oracle moyen sur SC6 par graine ; bootstrap percentile B = 20 000 avec rééchantillonnage conjoint des graines ; décisions : supériorité (borne inf > 0), infériorité (borne sup < 0), équivalence (IC dans ±0,005), sinon non concluant.
P1 GE − GDp (évidentiel contre probabiliste, concentration naturelle) ;
P2 GEg6 − GDg6 (symétrie, même opération γ = 6) ;
P3 GEgm − GDg6 (concentration appariée, contraste déterminant pour l'effet de la représentation) ;
P4 GDp − NSGA2 (le guidage probabiliste aide-t-il le GA classique ?) ;
P5 interaction (GEg6 − GDg6) − (GE − GDp).
Secondaires (IC 95 %) : GE − NSGA2, GDg6 − NSGA2, GEg6 − NSGA2, GEgm − NSGA2, GEg6 − GE, GDg6 − GDp, GEgm − GEg6 ; par scénario ; diagnostics q_max et entropie de la cible de mutation, taux de mutations effectives ; comparaison descriptive avec les bras QGA2-E de P14/P21 (E, Dp, Dg) sur les mêmes graines.
Lecture préenregistrée : P3 est déterminant pour l'effet propre de la représentation ; P1 et P2 sont complémentaires ; une supériorité de P1 ou P2 seule ne conclut pas à un avantage de représentation ; P5 est limitée à γ = 6 dans ce montage. Aucune causalité au-delà d'un montage.

## 5. Gates (avant gel)
G1 mutation guidée avec cible uniforme sur équipes admissibles hors équipe courante reproduit NSGA-II stocké bit à bit (chemin de tirage inchangé, test sur graine technique 10400) ; G2 test statistique du tirage : fréquences empiriques proches de q restreinte (tolérance fixée dans le code), équipe courante jamais retirée, équipes interdites jamais retirées ; G3 cible de mutation = `p10.target` / `make_target(g)` du module P14 (identité à 1e-15, γ = 1 et γ = 6) ; G4 budget 6 040 exact, archive complète, patchs restaurés, reproductibilité ; G5 non-fuite de l'oracle ; G6 valeurs finies ; G7 γ_m sélectionné avant toute lecture de HV, table de calibration archivée ; G8 graines autorisées ; G9 référence NSGA2 recalculable depuis le front stocké. Modules P14, P10 et P7 inchangés ; un module p22 les patche pendant l'exécution, avec try/finally.

## 6. Données, règles, durée
Graines 10400–10499 (références NSGA2, E, Dp, Dg déjà vues, déclaré) ; techniques 10400–10401, 11700–11714. HV lue à l'analyse unique. Pas de relance pour améliorer ; incidents déclarés ; aucune revendication de nouveauté (RS1 non faite) ; suivi actif pendant le calcul. Durée estimée : 5 bras × 600 tâches, environ 1 h 30 à 2 h 30 sur 2 cœurs (la cible ajoute un calcul par génération à NSGA-II, à mesurer au pilote technique), plus calibration, analyse et rapport : environ 3 h au total.

## 7. Décisions à confirmer
D22-1 mutation guidée comme point d'intégration (§2) ; D22-2 cinq bras GDp, GE, GDg6, GEg6, GEgm avec calibration HV-aveugle de γ_m (retirer GEgm si vous voulez seulement les bras naturel et γ = 6, la famille passe alors à 4 primaires sans P3) ; D22-3 n = 100, graines 10400–10499, SC6 ; D22-4 cinq primaires P1–P5, IC 99 %, marge 0,005 ; D22-5 référence NSGA2 stockée de P14, appariée ; D22-6 gates G1–G9 ; D22-7 lecture préenregistrée §4 ; D22-8 autorisation d'enchaîner implémentation, tests, calibration, gel, calcul continu, analyse unique et rapport sans arrêt si les gates passent.
Nota : le résultat de P21 (NSGA-II ≈ +0,12 au-dessus de QGA2-E) ne dit pas que le guidage aidera NSGA-II ; l'effet peut être nul ou négatif, et le protocole l'accepte.
