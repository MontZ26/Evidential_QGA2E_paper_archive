# Rapport final P4 — QGA avec croisement et mutation au niveau des angles (QGA-XM-E)

Protocole : v0.5 (SHA 8d0820f1331a…, = v0.4.1 + §9d). Run confirmatoire : seeds 4700–4999 (n = 300) × 6 scénarios = 1 800 tâches, toutes terminées, aucune instance infaisable, aucune seed exclue, 0 front vide. Précontrôle (`p4_precheck.py`) : PASS. Gel vérifié avant et après l'analyse. Analyse finale exécutée une seule fois.

## 1. Résultat confirmatoire (Holm sur 3, Wilcoxon apparié bilatéral, mesure = HV vrai moyen sur 6 scénarios par seed ; D = HV(XM-E) − HV(réf.))

| Hypothèse | Différence moyenne D | IC bootstrap 95 % | D>0 / D<0 | r biserial | p Holm | Verdict |
|---|---|---|---|---|---|---|
| H-4.1 XM-E vs NSGA-II | −0,1613 | [−0,1635 ; −0,1591] | 0 / 300 | −1,00 | 1,8e−50 | XM-E significativement **moins bon** |
| H-4.2 XM-E vs QGA2-E | −0,0162 | [−0,0173 ; −0,0151] | 18 / 282 | −0,985 | 1,8e−49 | XM-E significativement **moins bon** |
| H-4.3 XM-E vs QGA2 | −0,0460 | [−0,0478 ; −0,0443] | 0 / 300 | −1,00 | 1,8e−50 | XM-E significativement **moins bon** |

**Conclusion : l'hypothèse « un QGA avec croisement + mutation d'angles comble l'écart avec NSGA-II » est réfutée dans ce dispositif.** QGA-XM-E est inférieur aux trois références, avec une direction opposée à celle espérée. (Le test étant bilatéral, il s'agit d'un résultat confirmatoire négatif, pas d'un manque de puissance. Le point de puissance de H-4.3, §9d, ne concerne qu'un avantage de +0,01, non pertinent ici.)

## 2. HV moyen (descriptif)
MOEA/D 0,675 ; NSGA-II 0,669 ; NSGA-IIp (générationnel) 0,570 ; QGA2 0,553 ; QGA-XM-G 0,552 ; QGA2-E 0,524 ; **QGA-XM-E 0,507** ; QGA-X-E 0,507 ; QGA-M-E 0,504 ; QGA-T-E 0,502 ; QGA-XM-E-d0 0,488.
Budget : 6 040 évaluations pour toutes les méthodes sauf MOEA/D (6 030).

## 3. Ablations (descriptives, non confirmatoires ; différences moyennes de HV)
- Sélection par tournoi seule (T-E vs QGA2-E) : −0,021 (298/300 négatifs). C'est la plus grande perte parmi les composants.
- Croisement (X-E vs T-E) : +0,0047 (IC [0,0039 ; 0,0056]) ; mutation (M-E vs T-E) : +0,0013 ; XM-E vs X-E : +0,0002 (IC contient 0). Les opérateurs apportent un gain faible, bien inférieur à la perte due au tournoi.
- Rotation (XM-E vs δ=0) : +0,0197 (298/300 positifs).
- Remplacement générationnel (XM-G vs XM-E) : +0,0443 (300/300) ; XM-G ≈ QGA2 (0,5516 vs 0,5533).

## 4. Autres descriptifs
- IGD+ (front poolé de la tâche) : MOEA/D 0,006 < NSGA-II 0,021 < NSGA-IIp 0,057 < QGA2 0,066 < QGA2-E 0,122 < QGA-XM-E 0,132.
- Temps (boucle de recherche, s/run) : XM-E 4,05 ; QGA2 2,12 ; QGA2-E 3,39 ; NSGA-II 3,11 ; MOEA/D 1,50.
- Diversité (Hamming normalisé, gén. 150) : XM-E 0,566 ; QGA2-E 0,435 ; NSGA-II 0,274 ; QGA2 0,168. XM-E maintient la diversité la plus élevée tout en ayant le HV le plus bas : dans ces données, la diversité n'est pas le facteur limitant. Interprétation à traiter comme hypothèse, non testée.
- Convergence (20 premières seeds) : XM-E progresse lentement (0,405 → 0,506) contre NSGA-II qui dépasse 0,60 dès la génération 40.
- Compteurs de mutation (définitions différentes selon l'algorithme, à rapporter séparément, sans comparer les taux) : XM-E ≈ 5 838 gènes sélectionnés/run (dont 1,4 sans effet) ; NSGA-II ≈ 5 998 (dont 162 sans effet). Croisements effectifs XM-E ≈ 5 400/run.
- Écrêtage f1 : 858 points sur 541 931 ≥ 0,999 (max 1,0).

## 5. Limites et divulgations obligatoires
1. P4 a été conçu après P3 (dont le résultat négatif pour QGA2/QGA2-E était connu).
2. n = 300 fixé par l'auteur après un pilote ayant conclu STOP (n > 300 pour H-4.3) : écart post-pilote consigné au §9d de v0.5.
3. `run_p1m.py` et `ablation_loo.py` ont été **reconstruits** (originaux introuvables) à partir de `run_main_experiment.py` et vérifiés par non-régression exacte (HV de P3 retrouvé, −0,1475) ; à signaler dans l'article.
4. Consommation du flux `xm_cross` : le code gelé tire toujours les deux nombres (Bernoulli + vecteur par patient), le protocole décrit le second tirage seulement en cas de succès. Loi du croisement inchangée ; voir `Note_ecarts_P4.md`.
5. Reprises du run : arrêts (limite de 30 min des tâches de fond, redémarrage du conteneur), reprises avec le même code gelé vérifié à chaque lancement ; résultats écrits de façon atomique, aucune valeur modifiée (voir `p4_run_notes.txt`).
6. Une seule conception d'opérateurs testée (échange d'angles, croisement par lignes, rotation vers l'individu a) et trois jeux de paramètres seulement pour le tuning (S1 retenu a priori). Le résultat ne prouve pas qu'aucun QGA avec d'autres opérateurs ne puisse faire mieux.
7. Même famille de problèmes, ordre de visite fixé, instances synthétiques dérivées de Solomon ; MOEA/D à 6 030 évaluations.
8. Compteurs de mutation non comparables directement ; temps d'exécution = boucle de recherche seule.
9. Aucune analyse post-hoc n'a modifié les hypothèses ; les ablations et diagnostics sont descriptifs.

## 6. Fichiers
`p4_conf.json` (résultats bruts), `p4_final_analysis.json`, `p4_final_stdout.txt`, `p4_postrun_hashes.txt`, `p4_freeze.txt`, code et protocole gelés, `Note_ecarts_P4.md`, `p4_run_notes.txt`, `conf.log`.
