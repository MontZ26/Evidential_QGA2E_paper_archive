# Protocole P19 v0.1 — Plan factoriel représentation × concentration (évidentiel durci), préenregistré

Dr M. Zaghdoud · rédigé 2026-11-11 · gel : `p19_freeze1.txt` · lancement automatique à la fin de l'exécution de P18.

## A. Autorisation
Message de l'auteur, 13:48 : « Rédiger P19, le discuter, le préparer et juste après que P18 termine, le lancer automatiquement, c'est ma vision ». **Lecture :** rédaction, implémentation, tests, calibration HV-aveugle, gel, puis lancement automatique de l'exécution dès la fin de P18 (partie B), puis analyse unique et rapport. Non autorisé : toute modification de P18, ajout de bras ou de graines après résultat, GitHub, code gelé P3–P5, P7, P10, P11, P14–P18 inchangé. Les décisions ci-dessous sont prises par Claude et déclarées avant résultat.

## B. Question
Q19 : l'écart observé au Tier 1 (Dg ≥ DA) vient-il de la concentration du modèle ou de la représentation ? Le contrôle manquant est le durcissement de l'évidentiel par la même opération que Dg.

## C. Discussion de conception (réponse à la question de l'auteur)
1. **Nature évidentielle conservée.** Dans le moteur, la cible de tous les bras est Pn = m({équipe}) + m(Θ)·uniforme (probabilité pignistique, vérifiée numériquement en P17). Durcir DA = Pn^γ renormalisé puis plancher P10, la même opération que Dg (puissance appliquée avant le plancher). La structure évidentielle intervient en amont (Dempster, correction de dépendance, m(Θ)). Aucune transformation sur les masses n'est définie ; ce choix est déclaré et limite la portée : « évidentiel durci » signifie « cible évidentielle puis durcissement pignistique ».
2. **Deux niveaux de durcissement.** DAg6 : même γ = 6 que Dg (symétrie de l'opération). DAgm : γ choisi par calibration HV-aveugle (SC3, graines 11700–11714) pour apparier l'entropie et q_max de la cible à ceux de Dg(6), même règle de porte que P14 (écart relatif d'entropie ≤ 10 % et |Δq_max| ≤ 0,05 ; sinon meilleur essai, déclaré). Grille : 1 ; 1,25 ; 1,5 ; 2 ; 3 ; 4 ; 6.
3. **Limite.** L'appariement porte sur des moyennes (entropie, q_max), pas sur la distribution complète.

## D. Plan
Bras nouveaux : DAg6, DAgm. Bras de référence repris des fichiers P17 Tier 1 (mêmes instances et graines 11200–11259, déterministes, vérifiés bit à bit) : Dp, Dg(γ=6), DA, E. Données : SC6 × graines 11200–11259 (n = 60), budget 6040. Les HV de référence de ces graines ont déjà été vus ; déclaré.
Contrastes primaires (HV oracle moyen sur SC6 par graine ; bootstrap percentile B = 20000, unité = graine ; IC 99 % pour 5 primaires ; marge δ = 0,005 ; décisions supériorité / infériorité / équivalence / non concluant) :
C1 DAg6 − Dg ; C2 DAgm − Dg (représentation à concentration comparable) ; C3 DAg6 − DA ; C4 DAgm − DA (effet du durcissement évidentiel) ; C5 interaction (DAg6 − DA) − (Dg − Dp).
Secondaires (IC 95 %) : DAg6−Dp, DAgm−Dp, DAg6−E, DAgm−E, interaction avec γ apparié, Dg−DA, Dg−Dp, DAg6−DAgm ; par scénario ; diagnostics q_max, q_ent, m̄(Θ).
Lecture préenregistrée : effet de concentration = C3, C4 et Dg−Dp tous positifs ; effet de représentation = C1 ou C2 décidés en supériorité (évidentiel > probabiliste à concentration comparable) ; infériorité = le probabiliste reste meilleur ; interaction C5 ≠ 0 = le durcissement ne profite pas pareil aux deux. Aucune causalité au-delà d'un montage.

## E. Règles
Une seule analyse, HV lue à ce moment seul ; pas de relance ; incidents déclarés ; résultats « préenregistrés, un montage » ; pas de revendication de nouveauté (RS1 non faite).
