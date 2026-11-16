# Règle de réglage du NSGA-II — P2 étape 2 (écrite AVANT tout résultat de réglage)
Autorisation : auteur, 5 nov. 2026, graines 3810-3819 uniquement, 3 jeux de paramètres, règle écrite avant le réglage.
Seul le NSGA-II standard (élitiste) est réglé ; le QGA2 est inchangé ; la variante appariée reçoit les paramètres retenus.
Jeux (fixés ici) : J1 = (p_c 0,9 ; p_m 1/n_p) [jeu a priori du §3.2] ; J2 = (p_c 0,9 ; p_m 2/n_p) ; J3 = (p_c 0,7 ; p_m 1/n_p).
Mesure : monde de recherche F0|N, front évalué comme en §5.3 (front du monde de recherche réévalué dans le monde vrai), HV_T ; agrégat par graine = moyenne des 6 scénarios ; seule une graine dont les 6 scénarios sont faisables compte ; critère = moyenne de l'agrégat sur les graines 3810-3819.
Choix : le jeu au critère le plus élevé. Si l'écart entre le meilleur et J1 est < 0,001, on garde J1 (jeu a priori). Aucun autre critère, aucune seconde passe, aucun jeu ajouté.
Sorties : p2s2_tuned.json (jeu retenu), figé avant le pilote. Le QGA2 n'est pas évalué dans cette phase.
