# Règle de calibration P14 (HV-aveugle) — écrite le 10 novembre 2026, avant lecture de tout résultat de calibration
Statut : la calibration (p14_calib.py, SC3 × graines 10300–10314) a été LANCÉE quelques minutes avant la rédaction de ce fichier ; aucun résultat n'avait été lu à l'écriture. Incident déclaré : ordre « règle puis exécution » non respecté à la lettre ; la règle ci-dessous est celle codée dans p14_calib.py (code horodaté antérieur) et ne dépend d'aucun résultat.
Aucune HV n'est utilisée. Grille γ (D′_γ) ∈ {1, 1,5, 2, 3, 4, 6} ; γe (E_soft) ∈ {1, 0,75, 0,5, 0,35, 0,25, 0,15}.
Règle γ : parmi les γ qui satisfont G-N sur les moyennes (écart relatif d'entropie de la cible à E ≤ 10 % ET |Δ q_max| ≤ 0,05), choisir celui d'écart relatif d'entropie minimal. Si aucun ne satisfait G-N : G-N échoue, pas de primaire Δ_N ; bras exécutés en descriptif.
Règle γe : γe dont l'entropie de cible est la plus proche de celle de D′ (γ=1), descriptif, sans gate.
Paramètres de base : p10_calib.json (w, ε), DEC non utilisé. Aucune modification après lecture.
