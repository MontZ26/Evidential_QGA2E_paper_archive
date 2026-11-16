# Rapport final P24 — Sensibilité locale à w, σ et γ > 6 (QGA2-E)
Date : 15 novembre 2026. Protocole : `Protocole_P24_v0_2_candidat.md` + `Mise_en_oeuvre_P24_v0_2.md`. Autorisation : « Décisions confirmées et autorisation de lancer le Protocole_P24_v0_2 sans arrêt » (Dr M. Zaghdoud, 14 nov., 22:47) ; décisions D24-1 à D24-9 prises telles que proposées. Gel : `p24_freeze1.txt` (18 fichiers, vérifié à chaque lancement et reprise). Analyse unique : `p24_final_analysis.json`. Précontrôle OK : 600 tâches (SC6 × 12000–12099), 20 bras, budget 6 040 partout, journaux et npz complets ; relances DA(1) et Dg(6) égales bit à bit aux HV stockées de P23. Aucune revendication de nouveauté (RS1 non faite). Conclusions limitées à QGA2-E, SC6, budget 6 040 et aux valeurs testées.

## 1. Paramètres sélectionnés (calibration SC3 × 13700–13714, sans HV)
γ pour apparier DA(1) : w = 0,15 → 8 ; w = 0,3 → 6 ; w = 0,5 → 4 ; w = 0,7 → 3 ; (w = 0,3) σ = 0,6 → 4 ; σ = 0,8 → 6. Seuil de calibration atteint pour w = 0,15 / 0,3 / 0,5 ; **non atteint** pour w = 0,7, σ = 0,6, σ = 0,8 (meilleur essai déclaré). γ de référence = 6, intérieur à la grille jusqu'à 16 (la limite du bord notée dans P23 ne se reproduit pas ici). 20 familles exécutées.

## 2. Appariement vérifié sur SC6 (obligatoire avant lecture des contrastes)
| Contraste | Écart relatif d'entropie | Écart |q_max| | Conforme |
|---|---|---|---|
| DA−Dg w = 0,15 (γ = 8) | 3,7 % | 0,022 | oui |
| DA−Dg w = 0,5 (γ = 4) | 14,1 % | 0,042 | **non** |
| DA−Dg w = 0,7 (γ = 3) | 35,0 % | 0,089 | **non** |
| DA−Dg σ = 0,6 (γ = 4) | 24,7 % | 0,141 | **non** |
| DA−Dg σ = 0,8 (γ = 6) | 8,2 % | 0,026 | oui |
| DA−Dg(6), w = 0,3 (référence) | 4,5 % | 0,024 | oui |
| DA−Dg(8), w = 0,3 | 34,6 % | 0,146 | **non** |
| DA−Dg(12), w = 0,3 | 50,9 % | 0,208 | **non** |
Règle préenregistrée : aucun recalage sur SC6. Les contrastes DA−Dg non conformes **ne se lisent pas** comme des comparaisons à concentration comparable (ils restent rapportés). Dg(8) et Dg(12) sont des bras fixes volontairement plus concentrés que DA(1) : ils testent la sensibilité à γ, pas un appariement. Descriptif : les concentrations initiales (génération 1) diffèrent (q_max DA 0,447 contre Dg 0,535 à w = 0,3), comme dans P23.

## 3. Contrastes (HV oracle, moyenne sur SC6 par graine, IC 99 % marginal, B = 20 000, δ = 0,005)
| Contraste | Moyenne | IC 99 % | Décision | Bonferroni | Conforme | Robustesse (dir./classe/ampl.) → verdict |
|---|---|---|---|---|---|---|
| DA−Dg w = 0,15 | +0,0032 | [+0,0010 ; +0,0052] | supériorité | supériorité | oui | non/non/non → modifié |
| DA−E w = 0,15 | −0,0011 | [−0,0022 ; −0,0000] | infériorité (limite) | équivalence | — | non/non/oui → partiel |
| DA−Dg w = 0,5 | −0,0062 | [−0,0090 ; −0,0033] | infériorité | infériorité | non | oui/oui/oui → maintenu |
| DA−E w = 0,5 | +0,0019 | [+0,0004 ; +0,0034] | supériorité | supériorité | — | non/non/oui → modifié |
| DA−Dg w = 0,7 | −0,0105 | [−0,0131 ; −0,0079] | infériorité | infériorité | non | oui/oui/non → partiel |
| DA−E w = 0,7 | +0,0039 | [+0,0024 ; +0,0055] | supériorité | supériorité | — | non/non/oui → modifié |
| DA−Dg σ = 0,6 | +0,0152 | [+0,0132 ; +0,0172] | supériorité | supériorité | non | non/non/non → modifié |
| DA−E σ = 0,6 | −0,0068 | [−0,0090 ; −0,0047] | infériorité | infériorité | — | non/non/non → modifié |
| DA−Dg σ = 0,8 | −0,0028 | [−0,0053 ; −0,0004] | infériorité | non concluant | oui | oui/oui/oui → maintenu |
| DA−E σ = 0,8 | +0,0002 | [−0,0007 ; +0,0012] | équivalence | équivalence | — | non/oui/oui → modifié (signe de l'estimation) |
| DA−Dg(8) w = 0,3 | −0,0071 | [−0,0098 ; −0,0043] | infériorité | infériorité | non | oui/oui/oui → maintenu |
| DA−Dg(12) w = 0,3 | +0,0026 | [−0,0001 ; +0,0053] | non concluant | non concluant | non | non/non/non → modifié |
| E−Dp w = 0,15 | +0,0279 | [+0,0258 ; +0,0299] | supériorité | supériorité | — | descriptif |
| E−Dp w = 0,3 | +0,0425 | [+0,0400 ; +0,0452] | supériorité | supériorité | — | descriptif |
| E−Dp w = 0,5 | +0,0387 | [+0,0358 ; +0,0417] | supériorité | supériorité | — | descriptif |
| E−Dp w = 0,7 | +0,0281 | [+0,0255 ; +0,0308] | supériorité | supériorité | — | descriptif |
Référence P23 (w = 0,3, σ = 0,7) : DA(1)−Dg(6) = −0,0039 [−0,0066 ; −0,0014] (infériorité) ; DA(1)−E = −0,0009 [−0,0025 ; +0,0007] (équivalence). Les verdicts du tableau sont ceux de l'opérationnalisation écrite avant le gel ; ils doivent être lus avec la colonne « Conforme » : le « maintenu » de DA−Dg w = 0,5 et de DA−Dg(8) porte sur des contrastes non appariés en concentration.
HV moyennes par bras : E 0,5281 (w = 0,3), 0,5120 (0,15), 0,5269 (0,5), 0,5202 (0,7) ; DA(1) 0,5108 / 0,5273 / 0,5288 / 0,5241 ; Dg(γ_w) 0,5076 / 0,5312 / 0,5349 / 0,5346 ; Dp 0,4841 / 0,4856 / 0,4881 / 0,4920 ; DA(σ = 0,6) 0,5213, DA(σ = 0,8) 0,5284 ; Dg(4, w = 0,3) 0,5061 ; Dg(8) 0,5343 ; Dg(12) 0,5247.

## 4. Lecture
1. **E > Dp tient partout** (+0,028 à +0,043), avec un maximum autour de w = 0,3 et une baisse aux deux bords testés. C'est le résultat le plus robuste de P24.
2. **La conclusion de P23 « DA légèrement inférieur à Dg apparié » ne se généralise pas en tant que telle.** Parmi les contrastes appariés (conformes) : à w = 0,15, DA(1) est **supérieur** à Dg(8) (+0,0032 ; la différence avec la référence est de +0,0071 [+0,0046 ; +0,0095], descriptif) ; à σ = 0,8 et au baseline, l'infériorité faible de DA est retrouvée (−0,0028 et −0,0039). Pour w = 0,5 et 0,7, DA est inférieur à Dg (−0,006 et −0,011), mais ces contrastes ne sont pas appariés (14 % et 35 % d'écart d'entropie) : on ne peut pas attribuer cet écart à la représentation.
3. **DA(1) vs E dépend de w** : équivalent à w = 0,3 et σ = 0,8, légèrement supérieur à w = 0,5 (+0,0019) et 0,7 (+0,0039 ; estimation < δ), légèrement inférieur à w = 0,15 (−0,0011, limite de zéro) ; inférieur à σ = 0,6 (−0,0068). Ces écarts sont petits, sauf σ = 0,6 qui dépasse δ.
4. **σ = 0,6** : DA(1) est nettement moins performant (0,5213 contre 0,5281 pour E), mais le Dg(4) apparié par la calibration est encore plus faible (0,5061) et le contraste n'est pas conforme sur SC6 : la supériorité de DA (+0,0152) reflète surtout un Dg(4) mal adapté ici, pas un avantage établi de DA.
5. **γ > 6** : à w = 0,3, la HV de Dg croît jusqu'à γ = 8 (0,5343, contre 0,5312 pour γ = 6) puis baisse à γ = 12 (0,5247). Le γ calibré par concentration (6) n'est donc pas celui qui maximise la HV dans cette grille : cela confirme que l'appariement par concentration et la performance sont deux objectifs distincts (aucun γ n'a été choisi sur la HV). Dg(8) et Dg(12) ne sont pas conformes à l'appariement.
6. **Distributions effectives** (descriptif, non inférentiel) : à la génération 150, la distance JS entre DA(1) et Dg est de 0,09 à w = 0,15, 0,21–0,24 à w ≥ 0,3 ; entre DA(1) et E elle reste petite (0,016 à 0,061). Les corrélations de rang entre JS et écart de HV, par scénario, sont de signe et d'amplitude variables (ρ de −0,43 à +0,47 selon contraste et scénario) : aucun lien systématique mis en évidence.
7. **Hétérogénéité** : les écarts DA−Dg diffèrent selon le type d'instance (par ex. w = 0,15 : C101 +0,0064, R101 −0,0033 ; σ = 0,8 : RC101/R101 négatifs, C101 ≈ 0 ; DA−Dg(8) : −0,0095 sur RC101, −0,0049 sur C101). Pas de test d'interaction.

## 5. Incidents et limites
1. Premier lancement détaché de la calibration : faux signalement d'un arrêt (le processus tournait) et lancement d'un doublon, arrêté en quelques secondes sans rien écrire ; erreur et rectification déclarées en cours de séance.
2. L'exécution détachée principale s'est arrêtée à 278/600 vers 01:47, puis le suivi en arrière-plan a atteint sa limite à 542/600 ; relances reprenant sans rien refaire (tâches déterministes, gel vérifié à chaque reprise) ; précontrôle OK.
3. Essai à sec sur données synthétiques : erreur d'ordre des arguments de `save` détectée et corrigée avant le gel.
4. Le test T1 a comparé des HV stockées de P23 (booléen seulement), avant la calibration ; HV du pilote jamais affichées.
5. Seuil de calibration non atteint pour w = 0,7, σ = 0,6, σ = 0,8 ; contrastes correspondants non conformes sur SC6 ; DA−Dg(8) et DA−Dg(12) non conformes par construction.
6. E à w = 0,3 provient de P23 (sans journal par patient) : les distances JS/L1 avec E à w = 0,3 ne sont pas disponibles.
7. Les graines 12000–12099 sont réutilisées de P23 (non indépendantes) ; w = 0,3 reste HV-informé (P10) ; w, σ, γ ne sont variés que localement (un paramètre à la fois) ; 16 décisions avec IC marginaux (Bonferroni en sensibilité : DA−E w = 0,15 devient équivalence, DA−Dg σ = 0,8 devient non concluant).
8. Aucune revendication de nouveauté ; aucune conclusion hors QGA2-E, SC6, budget 6 040.

## 6. Fichiers
`p24_final_analysis.json`, `p24_final_stdout.txt`, `p24_calib.json`, `p24_params.json`, `p24_pilot.json`, `p24_tests_results.json`, `p24_seedcheck.json`, `p24_freeze1.txt`, `runs/main/` (600 json + 600 npz), `code/`.
