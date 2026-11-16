# Addendum P8 — contrôles descriptifs de la couche I (exploratoire, 30 graines 8200–8229, 6 scénarios)
Ne modifie pas les résultats confirmatoires. Résultats : `p8_controls_summary.json` SHA 7c6abf52…757af. Différence de HV oracle par graine, variante moins monde nominal de référence (même instance, mêmes arms B = GA classique, D = V1) ; IC95 % bootstrap sur graines.
| Variante de couche I | B | D | K moyen | largeur Pl−Bel |
|---|---|---|---|---|
| sans supervision | −0,0131 [−0,0161 ; −0,0097] | −0,0111 [−0,0135 ; −0,0087] | 0,060 | 0,471 |
| sans historique | −0,0062 [−0,0102 ; −0,0026] | −0,0038 [−0,0069 ; −0,0010] | 0,065 | 0,423 |
| règle prudente (Denœux) | −0,0030 [−0,0066 ; +0,0004] | −0,0031 [−0,0060 ; −0,0004] | 0,120 | 0,427 |
| historique dupliquée | +0,0009 [−0,0018 ; +0,0037] | +0,0009 [−0,0019 ; +0,0038] | 0,176 | 0,306 |
| B-cal (affine, calibrée sur 8100–8114 avec la vérité simulée) | +0,0062 [+0,0032 ; +0,0089] | +0,0039 [+0,0010 ; +0,0071] | — | — |
Lecture (descriptive) : chaque source apporte de l'information (retirer la supervision coûte le plus) ; la duplication de l'historique, qui double-compte la même information et fait passer K de 0,127 (monde nominal) à 0,176, ne change pas le HV de façon détectable ; la règle prudente est légèrement inférieure ; une recalibration affine donne un faible gain (+0,004 à +0,006), qui utilise la vérité simulée en calibration et n'est pas transférable à un déploiement réel. Les effets restent petits devant l'écart couche II (−0,058).


**Correction (9 nov., après relecture)** : la version précédente écrivait que la duplication faisait passer K de 0,06 à 0,18 ; 0,06 est le K de la variante « sans supervision », pas celui de la référence. K moyen du monde nominal (3 sources, cellules certifiées, graines 8200–8229, 4 005 cellules) = 0,127, largeur Pl−Bel = 0,329 (`p8_nominal_K.json`). La duplication augmente donc K de 0,127 à 0,176 (+39 % en valeur relative) sans effet détectable sur le HV. Les retraits de source réduisent K (0,060 ; 0,065) parce qu'il reste moins de sources pouvant se contredire ; la règle prudente produit une quantité K différente.
