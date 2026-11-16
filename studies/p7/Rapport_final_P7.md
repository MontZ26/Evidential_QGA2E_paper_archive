# Rapport final P7 — Agrégation évidentielle basée sur les individus (9 nov. 2026)
Protocole : P7 v0.3 + Amendement décisions D7-1…D7-8 (SHA-256 14adba48…2b69) + Addendum M2 descriptif + Amendement n = 200 (01:38). Auteur : Dr Montassar Zaghdoud. Exécution : Claude, sur autorisation écrite de l'auteur (« do all, code, confirmatory, without stop », « all decisions are confirmed », « ok put n=200 »).
## 1. Conclusion
**H7.1 (primaire) est rejetée dans le sens contraire à l'hypothèse de recherche : V2 (règle prudente de Denœux) est significativement moins bon que le contrôle probabiliste apparié V0c.** ΔHV = HV(V2) − HV(V0c) = **−0,0092**, IC bootstrap 95 % [−0,0100 ; −0,0084], p bootstrap-t bilatéral = 0,00005 (valeur plancher 1/20 001), n = 200 graines, V2 < V0c pour 94,5 % des graines. Sensibilités (Wilcoxon, inversion de signes) concordantes. La règle prudente ne procure aucun avantage d'optimisation sur la moyenne de probabilités.
## 2. Secondaires (Holm sur 3, une fois)
| Hypothèse | Différence de HV | IC 95 % | p ajusté Holm |
|---|---|---|---|
| H7.2 V2 − V1 | −0,0342 | [−0,0355 ; −0,0330] | 0,00015 |
| H7.3 V1 − V0c | +0,0250 | [+0,0238 ; +0,0262] | 0,00015 |
| H7.4 V2 − V0 (C2c de P5) | −0,0598 | [−0,0615 ; −0,0581] | 0,00015 |
Toutes rejetées. **Dempster (V1) bat le contrôle probabiliste (+0,025) et la règle prudente (+0,034).**
## 3. HV moyen par bras (200 graines, six scénarios)
V0 0,617 ; V0c 0,566 ; V1 0,591 ; V2 0,557 ; V0c-M2 0,562 ; V1-M2 0,621 ; V2-M2 0,567.
## 4. M2 (descriptif seulement, aucun test, aucune p-valeur)
Effet de M2 sur chaque règle (M2 − M1, IC bootstrap) : V0c −0,0043 [−0,0051 ; −0,0035] ; V1 +0,0295 [+0,0282 ; +0,0309] ; V2 +0,0102 [+0,0093 ; +0,0110]. Sous M2 : V2 − V0c = +0,0052 ; V1 − V0c = +0,0588. V1-M2 (0,621) est descriptivement proche de V0 (0,617), non testé. La part d'individus portant une évidence M2 : 74 % (V0c), 46 % (V1), 73 % (V2).
## 5. Diagnostics (descriptifs)
V1 : conflit moyen m(∅) = 0,98, entropie finale 0,37 contre 1,45 pour V0c, divergence BetP–fréquence (L1) 0,64 : concentration forte, cohérente avec G0 (Dempster dégénère en point de masse). V2 : m(∅) = 0,68, m(Θ) = 0,078, entropie ≈ V0c (1,47), divergence BetP–fréquence 0,31 : distribution plus étalée, sans information de fréquence (G0). Aucun repli (fallback) significatif. Coût de calcul des bras évidentiels ≈ celui de V0c.
## 6. Interprétation prudente (hypothèses, non résultats)
Le résultat est compatible avec l'hypothèse de G0 : la règle prudente n'utilise que le support (quelles équipes sont présentes), pas la fréquence, donc donne un signal d'apprentissage plus faible qu'une moyenne de probabilités. Que l'avantage de V1 vienne de sa pression d'exploitation (concentration) n'est pas démontré par ce plan. V0 (P5 C2c) reste supérieur à tous les bras M1, mais V0 et les bras P7 n'ont ni la même configuration calibrée (N, taux de LS) ni le même nombre de générations (≈ 8,7 contre 32,6) : H7.4 compare des architectures calibrées, pas des mécanismes isolés.
## 7. Déviations et incident (déclarés)
(i) n = 200 par amendement de l'auteur (dimensionnement : n = 100, puissance 100 % partout ; écart-type du pilote 0,0058). (ii) Les 93 coquilles produites avant l'amendement ont été conservées sans être lues. (iii) Incident : le premier lancement de l'analyse unique a échoué (TypeError, diagnostic descriptif de diversité) avant d'écrire toute sortie ; aucun résultat n'a été vu ; la clé de lecture a été corrigée, les tests inchangés, l'analyse relancée une fois (gel 5, Incident_P7_analyse_finale.md). (iv) Deux défauts de script corrigés en G0 avant toute interprétation. (v) P7 a utilisé l'engin P5 gelé sans modification ; aucun shard P5 ou P6 n'a servi de donnée.
## 8. Limites
Une famille d'instances (dérivées de Solomon), ordre de visite fixe, modèle factorisé, M1 par population entière reconstruite à chaque génération, calibration partagée sur S4, M2 descriptif, nouveauté non établie (recherche systématique à faire par l'auteur). Les conclusions se limitent à cette architecture.
## 9. Fichiers (chemins absolus, dossier /tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7/)
p7_final_analysis.json (SHA-256 266e0051…fed402), p7_final_stdout.txt (181a0b3f…8867977), runs/conf (1200 coquilles), runs/sizing/p7_pilot_report.json, p7_g0_results.json, p7_g1_results.json, p7_tests_engine.json, p7_tests_m2.json, p7_freeze5.txt.
