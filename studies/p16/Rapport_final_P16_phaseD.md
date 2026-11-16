# Rapport final P16 — calibration des seuils et phase D (DESCRIPTIF, SANS HV)
Date : 11 novembre 2026. Protocole : `Protocole_P16_v0_4.md`. Autorisation retenue : message du Dr Montassar Zaghdoud du 04:46 (« ok pour nouvelle version de P16 avec confirmation des décisions et exécution sans arrêt ») et du 04:50 (réponse à la question sur l'autorisation). **Phase P, lecture de la HV et confirmatoire : non exécutés et non autorisés.**
Phase D : 6 scénarios SC6 × 30 graines (11000–11029) × 4 bras (DA, DA+S, DA+L, DA+Fixe-P11), budget 6 040 évaluations par run. Unité de rééchantillonnage : la graine (moyenne des 6 scénarios), IC95 % percentile, B = 20 000, sans p-valeur. Précontrôle OK, gel vérifié (`p16_freeze1.txt`), analyse unique. **Aucun champ HV n'a été lu** (le script d'analyse n'en contient pas, test 7a).

## 1. Seuils (calibration HV-aveugle, DA sans DEC, SC3 × 11100–11114, 45 runs)
Médiane des médianes (générations 1–150) : **τ = 0,03415** (m̄(Θ)) et **τ_Δ = 0,03389** (Δm). Médianes par run : m̄(Θ) de 0,0029 à 0,127 ; Δm de 0,0029 à 0,109. Aucun Δm négatif.

## 2. Règle de décision préétablie (avant exécution)
« DEC fort (L) réduit l'ignorance moyenne de DA » est étayée si la borne supérieure de l'IC95 % de m̄(Θ)[DA+L] − m̄(Θ)[DA] est < 0 aux générations 50, 100 et 150 simultanément. **Résultat : étayée dans ce montage** (bornes supérieures −0,0046 ; −0,0208 ; −0,0255).

## 3. Ignorance m̄(Θ), moyennes sur 180 runs (générations 1 / 25 / 50 / 100 / 150)
| Bras | m̄_DA(Θ) | m̄_E(Θ) | Δm |
|---|---|---|---|
| DA | 0,167 / 0,037 / 0,036 / 0,046 / 0,047 | 0,074 / 0,007 / 0,006 / 0,005 / 0,003 | 0,093 / 0,031 / 0,031 / 0,041 / 0,044 |
| DA+S | 0,167 / 0,037 / 0,029 / 0,024 / 0,017 | 0,074 / 0,007 / 0,006 / 0,005 / 0,002 | 0,093 / 0,030 / 0,024 / 0,019 / 0,015 |
| DA+L | 0,167 / 0,036 / 0,028 / 0,019 / 0,015 | 0,074 / 0,007 / 0,006 / 0,004 / 0,003 | 0,093 / 0,029 / 0,022 / 0,014 / 0,012 |
| DA+Fixe-P11 | 0,167 / 0,036 / 0,028 / 0,019 / 0,014 | 0,074 / 0,007 / 0,006 / 0,005 / 0,003 | 0,093 / 0,029 / 0,022 / 0,014 / 0,011 |

Contrastes sur m̄(Θ) (moyenne [IC95 %]) :
- **DA+L − DA :** gén. 25 : −0,0012 [−0,0026 ; −0,0002] ; gén. 50 : −0,0089 [−0,0132 ; −0,0046] ; gén. 100 : −0,0271 [−0,0343 ; −0,0208] ; gén. 150 : −0,0319 [−0,0386 ; −0,0255].
- **DA+S − DA :** gén. 50 : −0,0070 [−0,0101 ; −0,0041] ; gén. 150 : −0,0302 [−0,0368 ; −0,0240].
- DA+Fixe-P11 − DA : gén. 150 : −0,0328 [−0,0394 ; −0,0265] (quasi identique à DA+L).
- À la génération 1, aucune différence (0,0 ; le nettoyage initial n'a presque aucun effet : Dep −0,0001).
- La réduction vient surtout de la part Δm (DA+L − DA : −0,0327 [−0,0390 ; −0,0267] à la gén. 150), pas de m̄_E(Θ) (qui reste proche de 0,003).
- **Hétérogénéité par scénario (DA+L − DA, gén. 150) :** S4-RC101 −0,057 ; S4-R101 −0,056 ; S4-C101 −0,040 ; S5-C101 −0,023 ; S5-R101 −0,009 ; S5-RC101 −0,007. Le signe est négatif partout, mais l'effet est de 2 à 8 fois plus petit dans les scénarios S5.

## 4. Dépendance génotypique, diversité, concentration, conflit
| Bras | Dep (150) | N_eff (150) | frac_dup (150) | q_max (150) | q_ent (150) | K (150) |
|---|---|---|---|---|---|---|
| DA | 0,266 | 22,6 | 0,560 | 0,710 | 0,841 | 0,768 |
| DA+S | 0,100 | 30,9 | 0,378 | 0,806 | 0,636 | 0,852 |
| DA+L | 0,031 | 36,7 | 0,163 | 0,827 | 0,587 | 0,862 |
| DA+Fixe-P11 | 0,031 | 36,8 | 0,162 | 0,829 | 0,582 | 0,867 |

DA+L − DA à la génération 150 : Dep −0,235 [−0,255 ; −0,216] ; N_eff +14,2 [+13,0 ; +15,3] ; q_max +0,117 [+0,103 ; +0,131] ; q_ent −0,254 [−0,282 ; −0,227] ; K +0,094 [+0,077 ; +0,112]. K désigne le conflit conjonctif non normalisé (champ `m_empty`).
**Lecture :** avec DEC, la population est beaucoup plus diverse (Dep, N_eff, frac_dup) alors que la cible d'échantillonnage est plus concentrée (q_max plus haut, q_ent plus bas) et le conflit K plus élevé. Réduire la dépendance génotypique et réduire l'ignorance vont ensemble, mais le conflit et la concentration augmentent : l'ignorance n'est pas le seul phénomène en jeu.

## 5. Intensité effective de DEC (moyenne par run ; 6 040 candidats par run)
| Bras | Gén. 1–50 : part de candidats réparés | Gén. 51–100 | Gén. 101–150 | Violations |
|---|---|---|---|---|
| DA+S | 1,9 % | 13,5 % | 22,4 % | ≈ 0 (0,006 par run et par fenêtre) |
| DA+L | 3,9 % | 19,7 % | 31,3 % | 0 |
| DA+Fixe-P11 | 3,9 % | 19,8 % | 31,4 % | ≈ 0 (0,011) |

S et L produisent donc bien des interventions distinctes (1,4 à 2 fois plus de candidats réparés pour L), et les violations sont quasi nulles : le risque d'un passage à n_max = 2 sur une population regroupée ne s'est pas matérialisé ici. L (2 ; 0,4) et Fixe-P11 (2 ; 0,2) donnent des résultats quasi identiques : dans ce montage, c'est n_max qui compte, pas ρ_max.

## 6. Signaux R1 et R2 évalués passivement (sans agir)
Décisions avec les seuils de la calibration : R1 donne L dans 43,8 % des générations pour DA, R2 dans 42,9 %. **Les deux règles diffèrent dans 1,0 à 1,4 % des générations** ; corrélation de rang des deux signaux 0,996 à 0,999. **R2 est donc quasi redondante avec R1** dans ce montage, comme prévu (m̄_E(Θ) ≈ 0,003 est négligeable devant Δm). Conformément à D16-3, R2 n'est pas retenue comme bras distinct de la phase P.
Sous DEC fixe (S, L, P11), la part de générations en régime L selon R1 descend à 25–28 % : DEC abaisse le signal en dessous du seuil.

## 7. Lecture autorisée et non autorisée
**Autorisé (descriptif, n = 30 graines × 6 scénarios, un montage) :** (i) DEC réduit l'ignorance m̄(Θ) de DA, d'environ 0,03 à la génération 150 (près de 70 %), dans les six scénarios ; (ii) cette réduction va avec une baisse de la dépendance génotypique (Dep) et une hausse de N_eff, ce qui est compatible avec le sens A (« moins de dépendance, moins d'ignorance ») pour la dépendance génotypique mesurée par DA ; (iii) en même temps, la cible est plus concentrée et le conflit K plus élevé ; (iv) S produit déjà l'essentiel de l'effet (−0,030 contre −0,032 pour L à la génération 150) ; (v) R1 et R2 sont quasi redondantes.
**Non autorisé :** conclure sur la HV (non lue) ; affirmer un mécanisme causal (DEC est aussi un opérateur de diversité) ; affirmer que la dépendance entre sources d'information a diminué (seule la dépendance génotypique est mesurée) ; affirmer que réduire l'ignorance améliore l'optimisation ; généraliser à d'autres familles d'instances ; toute revendication de nouveauté (RS1).

## 8. Conséquence pour la phase P
La règle préétablie est satisfaite, donc la phase P **peut être proposée**. Elle n'est pas autorisée et n'a pas été lancée. Avant de la proposer, deux points sont à trancher par l'auteur :
1. L'écart entre S et L étant petit pour m̄(Θ) (≈ 0,002 à la génération 150), une régulation S/L a peu de marge pour modifier l'ignorance : l'intérêt d'une régulation adaptative reste à justifier face à un DEC fixe.
2. L'augmentation de la concentration et du conflit sous DEC suggère que le gain éventuel en HV, s'il existe, ne se lira pas comme une simple réduction d'ignorance.

## 9. Incidents et écarts
- L'autorisation d'exécution est déduite du message du 04:46 (lecture déclarée dans le protocole v0.4, §A) ; l'auteur a confirmé à 04:50 par une question et à 04:52 en attendant le rapport définitif.
- La règle de calibration a été écrite (v0.4, §H) avant la calibration ; la calibration n'est pas soumise à gel (comme en P8), les seuils sont gelés avant la phase D.
- Dix-sept contrôles techniques ont réussi dès la première exécution ; `p16_tests_results.json` est dans le gel.
- Les seuils sont calibrés sur SC3 et appliqués à SC6 (limite déclarée D16-13).
- Aucun rerun, dépôt GitHub et codes gelés P3–P5, P7, P10, P11, P14 et P15 inchangés.

Fichiers : `/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p16/p16_final_analysis.json` (SHA256 b71bc624d676e9c22c0a4459e018403f4c9c7aba64ee1b3153a576bb260f114f), `p16_final_stdout.txt`, `p16_thresholds.json`, `p16_freeze1.txt`, `p16_tests_results.json`, `runs/phaseD` (180 fichiers), `runs/calib` (45 fichiers).
