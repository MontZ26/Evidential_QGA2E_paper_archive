# P11 — règle de calibration de DEC (écrite AVANT toute exécution de calibration ; 9 nov. 2026)
Autorisation : Dr Montassar Zaghdoud, 22:10 (D11-6 : calibration de σ, n_max sur 9920–9934 après diagnostic réel). Diagnostic réel (graines techniques 9910–9919, DEC éteint, fichier p11_diag_raw.json) : à σ = 0,7, E0 présente n_max moyen ≈ 15 sur N = 44 (Dep ≈ 0,25) en milieu et fin de run, P0 ≈ 1,2 (Dep ≈ 0,002), C0b ≈ 13 ; à σ = 0,5 la mesure sature, à σ ≥ 0,9 elle devient presque nulle pour E0.
Règle HV-aveugle (aucun HV n'est utilisé pour choisir) :
1. σ = 0,7 (valeur à laquelle le diagnostic sépare nettement le régime V1 du régime V0c ; sensibilité σ ∈ {0,6 ; 0,8} descriptive seulement, hors confirmatoire).
2. Grille (n_max, ρ_max) ∈ {2, 3, 5} × {0,2 ; 0,4}, r_max = 3. Calibration : DEC allumé, bras E1, SC3 × graines 9920–9934 (45 runs par point).
3. Éligible si : taux de violation (violations / candidats) ≤ 5 % ; nombre moyen de régénérations par candidat ≤ 1 ; Dep moyen de la population en fin de run ≤ 0,10.
4. Choix : parmi les éligibles, le plus petit n_max, puis le plus petit ρ_max. Si aucun point n'est éligible : le point à taux de violation minimal parmi n_max = 5, et l'écart est déclaré. Les mêmes paramètres sont appliqués à E1, P1 et C1 (comparabilité).
Les paramètres sont gelés au gel P11 ; aucun ajustement ultérieur.
