# Rapport final P8 (confirmatoire) — 2026-11-09
Protocole v0.2.1 + amendements (décisions, n=200). Gel : p8_freeze3.txt. Graines 8200–8399 (n=200), 6 scénarios, 8 bras, budget 6040 exact (precheck OK, 1200 shards, aucune graine exclue). Analyse unique (graine 9801) : `p8_final_analysis.json` SHA ff6fbf62…7228.
## HV oracle moyen
A 0,5898 · B 0,6348 · C 0,5383 · D 0,5769 · C' 0,5307 · D' 0,5570 · D_τ 0,5731 · D_V2 0,5504.
## Famille de Holm (bootstrap-t apparié sur graines, B=20000, p minimal atteignable 5e-5, Holm ×3 = 1,5e-4)
| Contraste | Moyenne | IC95 % | p Holm | Graines > 0 |
|---|---|---|---|---|
| I_V1 = D−B−C+A | −0,0064 | [−0,0086 ; −0,0043] | 0,00015 | 34,5 % |
| I_V0c = D'−B−C'+A | −0,0188 | [−0,0206 ; −0,0169] | 0,00015 | 8 % |
| G_τ = D−D_τ | +0,0038 | [0,0025 ; 0,0051] | 0,00015 | 67 % |
## Secondaires (descriptifs, IC95 %)
D−B −0,0579 · C−A −0,0515 · B−A +0,0451 · D−C +0,0386 · D−D' (V1−V0c, nominal) +0,0200 · D'−D_τ −0,0162 · D_V2−D' −0,0066 · C−C' +0,0076.
## Lecture
1. **Interaction négative** pour V1 et V0c : les effets des deux couches sont sous-additifs ; l'hypothèse « bénéfice supplémentaire » n'est pas soutenue. 
2. **Couche I (évidence externe) utile** pour le GA classique (B−A +0,045) et pour les arms avec modèle (D−C +0,039).
3. **Couche II (modèle de population P7) défavorable ici** : D−B −0,058, C−A −0,052. Attention : ce contraste confond l'évidence de recherche avec le changement d'opérateur et de configuration (config P7 partagée vs C0b réglé séparément, moins de générations ; déjà observé en P7 où V0 battait tous les bras M1). Il ne prouve pas que l'évidence en soi nuit.
4. **V1 > V0c** (+0,020 dans le bras nominal, +0,0076 sans couche I) et V2 < V0c, cohérents avec P7.
5. **G_τ > 0** : V1 > V0c-τ, mais V0c-τ n'est pas apparié en concentration (G-C : entropie 0,31 vs 1,18 minimum) ; la concentration n'est donc pas isolée. Entropies observées : V1 0,36 ; V0c 1,45.
6. Les contrastes HV portent sur une simulation (vérité cachée) ; effets faibles en valeur absolue, très précis (n=200).
## Écarts et limites déclarés
- Contrôles de dépendance, ablations et B-cal (amendement item 6) NON encore exécutés au moment de ce rapport ; addendum descriptif à suivre. 
- n=200 fixé par l'auteur (sizing : 100). 
- Pas de ré-exécution, pas de modification des hypothèses après lecture des résultats.
