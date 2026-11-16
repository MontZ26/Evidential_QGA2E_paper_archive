# Amendement P7 v0.3 — décisions D7-1…D7-8 et autorisation (texte opérationnel)
Date : 9 novembre 2026, 00:01–00:10 (Africa/Lagos). Base : Protocol_P7_Evidential_QIGA_v0_3_candidate.md (SHA-256 4af4f7c45dfa817771ae50ce1a2c71c363bb018f7bc10f3a5c896318f7baf71f).
Autorisation écrite de l'auteur : « so could you do all, code, confirmatory, without stop » (00:01) ; « all decisions are confirmed » (00:01). Les valeurs ci-dessous sont les propositions de Claude confirmées par l'auteur ; celles qui n'avaient pas de proposition antérieure (D7-5, D7-8, plan statistique, graines) sont fixées ici **avant** G0 et avant tout résultat, et couvertes par « all decisions are confirmed ».
Les portes restent contraignantes : un échec de G0 ou de G1 produit l'arrêt ou l'abandon prévu par le protocole, pas un contournement.

## Décisions
- D7-1 : force w constante, fiabilité r_j = 1 ; w ∈ [0,10 ; 0,95] (w_max = 0,95), paramètre commun calibré. Aucune fiabilité fondée sur le rang.
- D7-2 : reconstruction du modèle à chaque génération (sans mémoire) à partir de la population courante après survie ; pas de mise à jour après la dernière génération (complète ou partielle).
- D7-3 : source primaire = population entière P_t (N individus) ; élites seules/pondération = hors étape 1.
- D7-4 : V0 = configuration C2c retenue en P5 (tuned P5, avec LS), exécutée par le code P5 gelé, descriptif seulement.
- D7-5 : couverture M2 = fraction des individus de la population, en fin de génération, portant ≥ 1 observation M2 non vide (voisin 1-shift évalué non dominé par son parent, patient concerné) ; M2 n'est retenu que si la médiane de cette fraction (sur générations, puis moyenne des scénarios, graines 7000–7009) est ≥ 30 %. Sinon M2 est abandonné sans modifier w ni ajouter de sources ; le test principal reste M1.
- D7-6 : test primaire = bootstrap-t apparié sur la moyenne (règles de P6 v2.6 §7 : B = 20 000, Bv/B < 0,99 → non calculable p = 1, p = (1+#)/(1+Bv), sd nul), bilatéral α = 0,05 pour H7.1 ; famille secondaire H7.2–H7.4 par Holm une fois ; sous-flux dérivés de la graine d'analyse 9701. Dimensionnement : méthode de P6 v2.6 §8 pour le contraste H7.1 seul (n_f, n_s, grille {100,150,200,300}, ±0,01, 80 %, 1 500 simulations, cap 300, règle sur la simulation principale m = 1,0, sensibilité m = 1,25 et 1,5 rapportée), pilote de 30 graines.
- D7-8 : tous les voisins 1-shift évalués non dominés par leur parent entrent dans L_i, qu'ils aient été acceptés ou rejetés par la LS.
## Plan d'exécution (séquentiel)
G0 (script de validation mathématique indépendant) → G1 (audit instrumenté, graines 7000–7009) → implémentation M1 (V0c, V1, V2 ; boucle de P5 : deux parents échantillonnés, croisement uniforme, mutation ciblée, LS de P5, archive 200, survie (μ+λ), budget 6040) → calibration à configuration partagée par V0c, V1, V2 (critère commun = moyenne des HV des trois bras, 50 cfg × 5 graines puis 5 finalistes × 10 graines, scénarios S4) → pilote → dimensionnement → confirmation → analyse unique → rapport.
Plages de graines : G1 7000–7009 ; calibration 7100–7114 ; pilote 7150–7179 ; confirmation 7200 … ; tests techniques 7900–7909 ; graine d'analyse 9701. Aucun shard P5 ni P6 n'est utilisé comme donnée P7. Code P4/P5/P6 gelé inchangé ; fichiers P7 ajoutés.
## Hypothèses (préenregistrées avant résultats)
H7.1 (primaire) : ΔHV = HV(V2) − HV(V0c) ≠ 0 (bilatéral). H7.2 V2 vs V1 ; H7.3 V1 vs V0c ; H7.4 V2 vs V0 (Holm sur 3). Descriptif : masse d'ignorance, conflit, entropie, divergence BetP–fréquence, couverture, surcoût.
