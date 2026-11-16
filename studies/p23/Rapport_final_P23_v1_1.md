# Rapport final P23 (v1.1, corrections rédactionnelles) — λ dans DA contre cibles probabilistes appariées en concentration (QGA2-E)
Date : 14 novembre 2026. Protocole : `Protocole_P23_v1_0.md`. Autorisation : « Autorisation sans arrêt ! » (Dr M. Zaghdoud, 18:58). Gel : `p23_freeze1.txt` (vérifié, 14 fichiers). Analyse unique (`p23_final_analysis.json`), précontrôle OK : 600 tâches, 100 graines (12000–12099) × 6 scénarios, 9 bras, budget 6 040 pour chaque run, aucune instance infaisable. Aucune revendication de nouveauté (RS1 non faite).
**Version 1.1 : aucune analyse nouvelle, aucun résultat modifié.** Seules la rédaction et la qualification des conclusions changent (voir §1, §7, §9, §10). L'analyse unique (`p23_final_analysis.json`) est inchangée. Le rapport initial est conservé (`Rapport_final_P23.md`).

## 1. Résultat principal
Contrastes confirmatoires (HV oracle moyenne sur SC6 par graine, IC 99 %, bootstrap apparié B = 20 000, δ = 0,005) :
| Contraste | Moyenne | IC 99 % | Décision |
|---|---|---|---|
| C1 DA25-Dg25 | -0,0029 | [-0,0055 ; -0,0003] | infériorité statistique (borne sup. < 0) |
| C2 DA50-Dg50 | -0,0032 | [-0,0058 ; -0,0007] | infériorité statistique (borne sup. < 0) |
| C3 DA100-Dg100 | -0,0039 | [-0,0066 ; -0,0014] | infériorité statistique (borne sup. < 0) |
| C4 DA100-E | -0,0009 | [-0,0025 ; +0,0007] | équivalence |

Lecture : à concentration appariée (conforme sur SC6, §3), les trois configurations DA(λ) présentent une différence de HV **statistiquement négative** par rapport à la cible probabiliste durcie : de −0,0029 à −0,0039, soit environ 0,6 à 0,7 % de la HV moyenne (≈ 0,53). La règle préenregistrée teste l'infériorité avant l'équivalence ; elle classe donc C1 à C3 en « infériorité statistique » (borne supérieure < 0).

**Portée exacte (statistique et pratique).** Les IC recouvrent la limite de la marge δ = 0,005 : les bornes basses (−0,0055 ; −0,0058 ; −0,0066) sont sous −δ, mais les bornes hautes (−0,0003 ; −0,0007 ; −0,0014) sont proches de zéro. Aucun IC n'est entièrement sous −0,005. Les résultats ne démontrent donc ni l'équivalence pratique ni une infériorité pratique dépassant 0,005. Aucun avantage de DA(λ) sur la cible probabiliste appariée n'est observé. C4 : DA(1) équivaut à E (IC dans ±0,005).

**Référence commune.** Le même exposant γ = 6 a été retenu pour les trois λ : Dg25, Dg50 et Dg100 sont le même bras (HV identiques). C1 à C3 comparent donc trois configurations DA à un comparateur probabiliste commun, non à trois cibles probabilistes calibrées indépendamment ; ce ne sont pas trois confirmations indépendantes. γ = 6 est au bord supérieur de la grille et aucun γ > 6 n'a été exécuté : Dg n'est pas présenté comme l'appariement le plus précis possible ni comme la cible probabiliste optimale.

**Multiplicité.** Les quatre IC primaires sont des IC à 99 % marginaux, sans correction supplémentaire (règle déclarée) ; ils ne garantissent pas une couverture simultanée à 99 % de toute la famille.

HV oracle moyenne par bras (100 graines) :
| Bras | Moyenne | Écart-type |
|---|---|---|
| E | 0,5281 | 0,0298 |
| DA25 | 0,5283 | 0,0291 |
| DA50 | 0,5279 | 0,0289 |
| DA100 | 0,5273 | 0,0287 |
| Dg25 | 0,5312 | 0,0298 |
| Dg50 | 0,5312 | 0,0298 |
| Dg100 | 0,5312 | 0,0298 |
| RHO | 0,5280 | 0,0300 |
| MIX | 0,5132 | 0,0276 |

## 2. Q1 (descriptive) : évolution avec λ
HV : E (λ = 0) 0,5281 ; λ = 0,25 : 0,5283 ; 0,5 : 0,5279 ; 1 : 0,5273. Courbe plate, différences de l'ordre de 0,001 (exploratoire, DA(0,25) − E et DA(0,5) − E dans l'IC 95 % de zéro). Pourtant la concentration de la cible change nettement : q_max passe de 0.845 (E) à 0.709 (DA(1)) et l'entropie de 0.542 à 0.842 à la génération 150. Dans ce montage, une baisse forte de concentration entre E et DA ne se traduit pas par un changement de HV.

Diagnostics à la génération 150 (moyennes sur 600 runs) :
| Bras | q_max | entropie | Dep | N_eff |
|---|---|---|---|---|
| E | 0.845 | 0.542 | 0.440 | 18.3 |
| DA25 | 0.754 | 0.753 | 0.356 | 19.8 |
| DA50 | 0.728 | 0.805 | 0.304 | 21.1 |
| DA100 | 0.709 | 0.842 | 0.258 | 22.8 |
| Dg25 | 0.797 | 0.664 | 0.323 | 22.4 |
| Dg50 | 0.797 | 0.664 | 0.323 | 22.4 |
| Dg100 | 0.797 | 0.664 | 0.323 | 22.4 |
| RHO | 0.761 | 0.735 | 0.284 | 24.3 |
| MIX | 0.629 | 1.061 | 0.067 | 35.2 |

## 3. Conformité de l'appariement sur SC6 (obligatoire)
| Contraste | Réf. / autre | Entropie | Écart relatif | q_max | Écart absolu | Conforme |
|---|---|---|---|---|---|---|
| C1 | DA25 / Dg25 | 0,8363 / 0,8478 | 1.4 % | 0,7072 / 0,7051 | 0.002 | oui |
| C2 | DA50 / Dg50 | 0,8675 / 0,8478 | 2.3 % | 0,6919 / 0,7051 | 0.013 | oui |
| C3 | DA100 / Dg100 | 0,8879 / 0,8478 | 4.5 % | 0,6814 / 0,7051 | 0.024 | oui |
| RHO_vs_DA100 | DA100 / RHO | 0,8879 / 0,9015 | 1.5 % | 0,6814 / 0,6743 | 0.007 | oui |
| MIX_vs_DA100 | DA100 / MIX | 0,8879 / 1,1460 | 29.1 % | 0,6814 / 0,5693 | 0.112 | NON |
C1, C2 et C3 sont conformes aux deux seuils (10 % ; 0,05) sur SC6 : leur lecture comme comparaison à concentration comparable est licite pour l'entropie et q_max de la cible. Rmix est non conforme (écart d'entropie 29 %) : MIX − Dg ne doit pas être lu comme effet de représentation.

## 4. Distribution effective induite (diagnostic §8, descriptif)
| Bras | Fréquence de décodage maximale (gén. 1 / 50 / 150) | L1 décodage–cible (150) | Concentration normalisée des angles (150) |
|---|---|---|---|
| E | 0.335 / 0.537 / 0.676 | 0.403 | 0.645 |
| DA25 | 0.335 / 0.529 / 0.635 | 0.377 | 0.613 |
| DA50 | 0.335 / 0.525 / 0.621 | 0.379 | 0.602 |
| DA100 | 0.335 / 0.521 / 0.608 | 0.387 | 0.592 |
| Dg25 | 0.342 / 0.498 / 0.638 | 0.398 | 0.613 |
| Dg50 | 0.342 / 0.498 / 0.638 | 0.398 | 0.613 |
| Dg100 | 0.342 / 0.498 / 0.638 | 0.398 | 0.613 |
| RHO | 0.334 / 0.483 / 0.610 | 0.405 | 0.593 |
| MIX | 0.331 / 0.418 / 0.490 | 0.408 | 0.498 |
Lecture prudente : à la génération 150, E décode de façon plus concentrée (0,676) que Dg (0,638), lui-même plus que DA(1) (0,608), alors que les HV ordonnent Dg > E ≈ DA. La concentration de décodage seule n'explique donc pas l'ordre des HV dans ce montage. Les différences de décodage restent modestes. Aucune analyse inférentielle n'est préenregistrée sur ces diagnostics.

## 5. Exploratoires (IC 95 %, aucune décision)
| Contraste | Moyenne | IC 95 % |
|---|---|---|
| DA25-E | +0,0002 | [-0,0009 ; +0,0012] |
| DA50-E | -0,0002 | [-0,0013 ; +0,0009] |
| RHO-E | -0,0001 | [-0,0021 ; +0,0019] |
| RHO-DA100 | +0,0007 | [-0,0012 ; +0,0027] |
| RHO-Dg100 | -0,0032 | [-0,0053 ; -0,0011] |
| MIX-E | -0,0149 | [-0,0171 ; -0,0128] |
| MIX-Dg100 | -0,0180 | [-0,0200 ; -0,0159] |
Rρ (ρ₀ = 0,05) : HV indiscernable de E et de DA(1) (écarts ≤ 0,001), conforme sur SC6 (écart d'entropie 1,5 %), inférieur à Dg (−0,0032), comme DA. Rmix (γ_mix = 0,75, simplifié, non fidèle à la méthode publiée) : nettement inférieur à E (−0,015), cible beaucoup moins concentrée (q_max 0,629), appariement non conforme.

## 6. Par scénario (écart moyen de HV)
| Contraste | S4-RC101 | S4-R101 | S4-C101 | S5-RC101 | S5-R101 | S5-C101 |
|---|---|---|---|---|---|---|
| C1 DA25-Dg25 | -0,0047 | +0,0018 | +0,0025 | -0,0085 | -0,0089 | +0,0006 |
| C2 DA50-Dg50 | -0,0043 | +0,0014 | +0,0011 | -0,0076 | -0,0103 | +0,0003 |
| C3 DA100-Dg100 | -0,0071 | -0,0025 | +0,0033 | -0,0076 | -0,0102 | +0,0006 |
| C4 DA100-E | -0,0032 | -0,0057 | +0,0043 | -0,0013 | -0,0000 | +0,0007 |
Les écarts négatifs sont portés par S5-RC101, S5-R101, S4-RC101 (et S4-R101 pour C3) ; ils s'inversent légèrement pour S4-C101 et S5-C101. Effet hétérogène. **Aucun test d'interaction scénario × représentation n'était préenregistré** : l'hypothèse d'une interaction avec le type de scénario (R et RC contre C) est une observation descriptive, non démontrée.

## 7. Incidents et limites (à déclarer)
1. Chronologie avant le gel (ordre des événements) : tests T1 à T13 (T12a corrigé), calibration sans HV, sélection des paramètres, pilote technique, essai à blanc de l'analyse sur données synthétiques, gel (18:24:13 UTC), exécution, analyse unique. Un test de fumée du moteur, exécuté avant la calibration sur la graine technique 12900 avec des paramètres provisoires, a affiché une fois des valeurs de HV dans la sortie de l'assistant ; elles n'ont servi à choisir aucun paramètre. Seuls l'assistant (dans la session) et l'auteur, s'il a consulté la sortie, ont pu les voir.
2. Test T12a : première version de l'expression de test trop large (échec), corrigée avant tout résultat ; tous les tests T1–T13 passent (`p23_tests_results.json`).
3. Ordre : la calibration a démarré avant le pilote technique (les deux avant le gel).
4. Le premier script de surveillance a échoué (arithmétique shell) ; l'exécution n'a pas été affectée.
5. **γ = 6 choisi pour les trois λ** (bord de la grille ; conformité satisfaite). Dg25, Dg50 et Dg100 sont donc le même bras (HV identiques) et C1–C3 partagent la même référence : ce ne sont pas trois preuves indépendantes côté Dg. Un meilleur appariement à γ > 6 n'a pas été exploré.
6. Rρ (ρ₀ = 0,05) non conforme à la calibration de justesse (10,1 % > 10 %), mais conforme sur SC6. Rmix non conforme (meilleur essai déclaré).
7. §3 du protocole listait DA(λ) − Dg(6) en exploratoire : Dg(6) est le bras Dg unique ; ces contrastes sont C1–C3.
8. La durée mesurée de l'exécution (≈ 2 h 10) dépasse l'estimation du pilote (1,95 h) : sans conséquence.
9. Limites : un seul montage (QGA2-E, SC6, budget 6 040, w = 0,3, σ = 0,7) ; l'appariement porte sur la cible, pas sur la distribution effective ; Rmix simplifié ; aucune conclusion hors de ces configurations ; aucune revendication de nouveauté.

## 8. Tests T1 à T13 (objectifs ; supplément)
T1 λ = 0 reproduit E bit à bit (cible). T2 DA(1) et E reproduisent des HV P17 stockées (graine 11200, S4-C101). T3 cibles normalisées, finies, nulles hors masque. T4 m(Θ) non décroissant en λ. T5 invariance par permutation des sources et par duplication exacte (λ = 1). T6 cas limites (une source, une équipe admissible). T7 budget exact de 6 040 pour les 9 bras. T8 aucune fuite de l'oracle (la recherche ne dépend pas du monde oracle ; HV oracle recalculée depuis l'archive). T9 reproductibilité. T10 code et protocoles gelés des études antérieures inchangés (hachages P18 à P22). T11 identités de Rρ (ρ₀ = 0 donne E ; cas binaire donne DA) et de Rmix (γ_mix = 1 donne E ; γ_mix = 0 donne la cible prudente, vérifiée par forme fermée indépendante). T12 le script de calibration ne contient aucun champ HV et le moteur sans oracle n'en produit pas. T13 la journalisation des diagnostics ne modifie pas la recherche (HV, archive identiques). Résultats : `p23_tests_results.json` (18 contrôles, tous réussis). Les tests vérifient des propriétés de cohérence ; ils ne prouvent pas que la couverture est complète.

## 9. Niveaux de conclusion
- **Soutenue (dans ce montage)** : faire varier λ modifie nettement la concentration de la cible (q_max 0,845 → 0,709 à la génération 150) sans variation notable de la HV (0,5273 à 0,5283).
- **Soutenue (dans ce montage)** : les trois configurations DA présentent une différence statistiquement négative avec la référence probabiliste commune, d'ampleur modeste, sans démonstration d'une infériorité pratique au-delà de 0,005.
- **Soutenue avec réserve** : DA(1) et E sont équivalents en HV dans la marge de 0,005.
- **Non démontrée** : une supériorité intrinsèque de la représentation probabiliste. L'appariement porte sur l'entropie et q_max de la cible ; les distributions de décodage effectives ne sont pas identiques (§4), et l'ordre des HV ne suit pas celui de la concentration de décodage.

## 10. Lien avec l'audit des paramètres
Les conclusions valent pour w = 0,3 (HV-informé, hérité de P10), σ = 0,7, ε = 0,02, rotation 0,05π, budget 6 040, γ = 6. Aucun de ces paramètres, sauf λ, n'a été varié dans P23 ; voir `Audit_parametres_P23_v0_1.md`.

## 11. Fichiers
`p23_final_analysis.json`, `p23_final_stdout.txt`, `p23_calib.json`, `p23_params.json`, `p23_pilot.json`, `p23_tests_results.json`, `p23_freeze1.txt`, `p23_seedcheck.json`, `runs/main/`, `code/`.
