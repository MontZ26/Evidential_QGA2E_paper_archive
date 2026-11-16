# Synthèse consolidée des protocoles P2 à P22 — version 2 (matrice statut / contraste / IC / portée)

Dr M. Zaghdoud · 2026-11-13 · remplace `Synthese_protocoles_P2_P22.md`. Établie à partir des fichiers d'analyse finale conservés (IC lus dans les fichiers JSON, non recopiés de mémoire, sauf mention). Statut : **C** confirmatoire préenregistré, **D** descriptif/pilote, **A** arrêté, **X** jamais exécuté. HV = hypervolume oracle moyen (réf. 1,2), budget 6 040 évaluations, SC6, un montage. Les protocoles P2 à P11 ont été analysés avec des IC bootstrap à 95 % et des tests Holm, **sans marge d'équivalence** ; à partir de P17, IC à 99 % pour les primaires et marge δ = 0,005 (supériorité / infériorité / équivalence / non concluant).

## 0. Corrections apportées à la v1 (déclarées)
1. **Erreur dans la ligne P10 v3 de la v1** : j'y avais écrit « C2 non concluant ». Le contraste non concluant est le C2 de **P19** (DAgm − Dg). Dans P10 v3, C2 (Eg6 − E) est une infériorité nette. Corrigé ci-dessous, avec les contrastes Eg − Dg que la v1 omettait.
2. **Formulation causale adoucie** : « effet de concentration » devient « compatible avec une explication par la concentration, sans démonstration d'un mécanisme unique ».
3. **« À concentration appariée, aucun avantage détectable »** est retiré : l'appariement n'était pas exact (P19, P22) et P19 C2 est non concluant, non équivalent.
4. **« Aucune option ne fait mieux »** est limité aux variantes évaluées dans des protocoles confirmatoires ; P6 (arrêté) et P13 (jamais exécuté) ne sont pas des résultats négatifs.

## 1. Matrice des résultats (contrastes lus dans les analyses finales)
| Protocole | Statut | Contraste | Moyenne | IC | Décision | Portée |
|---|---|---|---|---|---|---|
| P2 étape 2 | C | QGA2 − NSGA-II | −0,1321 | IC 95 % [−0,1353 ; −0,1290] | défavorable, 100/100 graines | écart de classe, un montage |
| P3 | C | QGA2-E − NSGA-II | −0,1475 | IC 95 % [−0,1507 ; −0,1441] | défavorable, 100/100 | idem |
| P3 | C | QGA2 − NSGA-II apparié | −0,0168 | IC 95 % [−0,0197 ; −0,0138] | défavorable, 87/100 | idem |
| P3 | C | QGA2-E − QGA2 | −0,0296 | IC 95 % [−0,0326 ; −0,0265] | défavorable | l'élitisme dégrade QGA2 |
| P4 | C (n = 300) | XM-E − NSGA-II ; XM-E − QGA2-E ; XM-E − QGA2 | −0,1613 ; −0,0162 ; −0,0460 | IC 95 % [−0,1635 ; −0,1591] ; [−0,0173 ; −0,0151] ; [−0,0478 ; −0,0443] | défavorables | opérateurs d'angles n'aident pas |
| P5 | C (n = 300) | C2 − C3 ; C2 − C0b ; C2 − NSGA-II | +0,055 ; −0,038 ; ≈ −0,059 | non repris ici (voir rapport P5) | — | la rotation bat PBIL, reste sous NSGA-II |
| P6 | A | — | — | — | aucun test confirmatoire | à mentionner dans toute publication |
| P7 | C | V1 − V0c (Dempster contre probabiliste) | +0,0250 | IC 95 % [+0,0238 ; +0,0262] | supérieur (Holm) | règle V2 prudente pire : V2 − V1 −0,0342 [−0,0355 ; −0,0330] |
| P8 | C | interactions ; V1 − V0c | −0,0064 ; −0,0188 ; +0,020 | non repris ici (voir rapport P8) | — | cumul des couches sans bénéfice |
| P9 | C | E − P | +0,0275 | IC [+0,0261 ; +0,0289] | supérieur, 99,5 % des graines | confondu avec la concentration |
| P10 | C | E − P | +0,0459 | IC 95 % [+0,0444 ; +0,0473] | supérieur, 100 % des graines | primaire unique, sans Holm |
| P11 | C | E1 − P1 ; E1 − E0 | +0,0147 ; −0,0043 | non repris ici (voir rapport P11) | — | DEC réduit l'avantage |
| P13 | X | — | — | — | jamais exécuté | pas un résultat |
| P14 | D (porte G-N échouée) | E − Dp ; Dg − Dp ; E − Dg | +0,0414 ; +0,0454 ; −0,0040 | descriptif, pas de test préenregistré | — | γ = 6 « meilleure tentative, non conforme » |
| P15 | D | DA − E ; DA − Dp ; DA − Dg | −0,0003 ; +0,043 ; −0,0055 | descriptif | — | pilote, 30 graines |
| P16 | D | DEC fort réduit m̄(Θ) | −0,032 | HV non lue | — | phase P renvoyée à P18 |
| P17 Tier 1 | C | P1 DA+SEL4 − DA ; P2 DA+SEL4 − DA+SELR ; P4 DA − Dp ; P5 DA − Dg | +0,0077 ; −0,0042 ; +0,0427 ; −0,0036 | 99 % [+0,0049 ; +0,0107] ; [−0,0070 ; −0,0015] ; [+0,0401 ; +0,0454] ; [−0,0064 ; −0,0009] | sup. ; inf. ; sup. ; inf. | le gain n'est pas dû à l'ignorance ; Dg ≥ DA |
| P18 A | C | R1 − S ; R1 − L ; R1 − R1inv ; SCH − S ; S − DA | 0,0000 ; +0,0008 ; +0,0015 ; −0,0002 ; −0,0013 | tous dans ±0,005 (ex. [−0,0008 ; +0,0008]) | équivalence ×5 | aucune régulation ne change la HV |
| P18 B | C | DIV − DA ; SELL − DA ; Dp+SELW − Dp | −0,0094 ; −0,0002 ; −0,0004 | [−0,0129 ; −0,0060] ; [−0,0033 ; +0,0029] ; [−0,0024 ; +0,0015] | inf. ; équiv. ; équiv. | la diversité n'explique pas le gain ; Dg(8) − Dg(6) +0,0031 |
| P19 | C (n = 60) | C1 DAg6 − Dg ; **C2 DAgm − Dg** ; C3 DAg6 − DA ; C4 DAgm − DA | −0,0134 ; **−0,0025** ; −0,0105 ; +0,0003 | [−0,0172 ; −0,0097] ; **[−0,0057 ; +0,0009]** ; [−0,0144 ; −0,0068] ; [−0,0029 ; +0,0038] | inf. ; **non concluant** ; inf. ; équiv. | contraste déterminant non concluant ; appariement de concentration non exact |
| P10 v3 | C | Eg2 − E ; Eg6 − E ; **Eg6 − Dg** ; Eg2 − Dg | −0,0046 ; −0,016 ; **−0,0204** ; −0,0090 | [−0,0076 ; −0,0016] ; [−0,0188 ; −0,0130] ; [−0,0231 ; −0,0177] ; [−0,0119 ; −0,0061] | infériorité ×4 | durcir l'évidentiel le dégrade ; Eg1,5 − E +0,0016 [−0,0007 ; +0,0040] (secondaire) |
| P21 A | C | NSGA-II − MOEA/D ; − E ; − Dg ; MOEA/D − Dg ; NSGA-II − DA+SELR | −0,0065 ; +0,1258 ; +0,1221 ; +0,1286 ; +0,1138 | 99 % ex. [+0,1214 ; +0,1301] pour NSGA-II − E | inf. ; sup. ×4 | écart classique/QGA2 confirmé, apparié |
| P21 B | C | Eg1,1 − E ; Eg1,25 − E ; Eg0,9 − E ; Eg0,8 − E | +0,0010 ; +0,0006 ; −0,0007 ; −0,0047 | [−0,0015 ; +0,0036] ; [−0,0020 ; +0,0031] ; [−0,0031 ; +0,0017] ; [−0,0069 ; −0,0025] | équiv. ×3 ; inf. | plateau 0,9–1,5 ; Eg − Dg −0,003 à −0,009 (secondaire) |
| P22 | C | P1 GE − GDp ; P2 GEg6 − GDg6 ; P3 GEgm − GDg6 ; P4 GDp − NSGA-II ; P5 interaction | −0,0040 ; +0,0021 ; −0,0012 ; 0,0000 ; +0,0061 | [−0,0072 ; −0,0008] ; [−0,0006 ; +0,0049] ; [−0,0040 ; +0,0017] ; [−0,0033 ; +0,0033] ; [+0,0020 ; +0,0104] | inf. (en partie dans la marge) ; équiv. ×3 ; sup. (γ = 6 seulement) | GEgm ≡ GE ; appariement de concentration non satisfait |

Lecture des décisions : une équivalence signifie que l'IC est entièrement dans ±0,005 ; une moyenne proche de zéro ne suffit pas. P1 de P22 est une infériorité au sens de la règle (borne supérieure < 0) mais son IC dépasse en partie la marge : ni nettement négligeable, ni nettement hors marge.

## 2. Ce que les expériences démontrent, rendent plausible, n'établissent pas
**Démontré dans ce montage (confirmatoire, IC et marge) :**
- NSGA-II et MOEA/D donnent un HV supérieur de 0,11 à 0,13 à tous les bras QGA2-E (P2, P3, P21 A).
- Au sein de QGA2-E, la cible évidentielle (Dempster) fait mieux que la cible probabiliste simple (P7, P9, P10 : +0,025 à +0,046).
- Un probabiliste durci (Dg) fait au moins aussi bien que E et que DA (P17 P5 : DA − Dg −0,0036, infériorité) ; durcir l'évidentiel le dégrade (P10 v3, P19) et il fait moins bien que Dg (P10 v3 : Eg6 − Dg −0,0204).
- La courbe en γ de E est un plateau entre 0,9 et 1,5 (équivalence à E), avec baisse en dessous et au-dessus (P21 B).
- Ni la régulation de DEC (P18 A), ni la diversité (P18 B), ni l'ignorance en sélection (P17) n'expliquent ou n'améliorent le HV.
- Dans NSGA-II, guider la mutation n'améliore pas la HV (P22 P4, équivalence) et l'évidentiel n'y dépasse pas le probabiliste (P22 P1, P2).

**Rendu plausible, sans démonstration :**
- L'avantage initial de l'évidentiel est lié à la concentration de la cible : les résultats y sont compatibles (Dg reproduit l'avantage), mais les expériences comparent des transformations de distributions et n'isolent pas la concentration comme unique mécanisme. L'appariement de concentration n'a jamais été exact (P14 porte G-N échouée ; P19 ; P22).
- L'avantage de QGA2 ne se transfère pas à NSGA-II parce que la cible n'y pilote qu'environ une mutation par enfant : interprétation, non testée.

**Non établi :**
- Une équivalence entre représentations évidentielle et probabiliste à concentration comparable (P19 C2 non concluant ; P22 P3 non interprétable pour la représentation).
- Un résultat sur d'autres points d'intégration dans un GA classique, d'autres budgets, d'autres instances.
- Toute nouveauté : RS1 non faite.

## 3. Conclusion consolidée (base de travail pour l'article, vérifiée phrase par phrase)
Dans les configurations étudiées (six scénarios dérivés de Solomon, 6 040 évaluations, HV oracle de référence 1,2), NSGA-II et MOEA/D obtiennent des hypervolumes supérieurs à ceux de QGA2-E de 0,11 à 0,13, de façon cohérente d'un protocole à l'autre.
Au sein de QGA2-E, la cible évidentielle fait mieux que la cible probabiliste simple. Un durcissement de la cible probabiliste par puissance reproduit cet avantage et fait au moins aussi bien que E. Le durcissement de la cible évidentielle ne procure aucun gain et la dégrade lorsqu'il est fort. Ces résultats sont compatibles avec une contribution importante de la concentration de la cible à l'avantage initial, sans démontrer qu'elle en soit l'unique mécanisme. Aucun avantage indépendant de la représentation évidentielle n'a été établi dans les comparaisons réalisées ; le contraste calibré de P19 n'a conclu ni à la supériorité ni à l'équivalence.
Dans NSGA-II à mutation guidée, la cible évidentielle ne dépasse pas la cible probabiliste, et le guidage probabiliste ne change pas le HV : l'avantage observé dans QGA2-E ne se transfère pas dans ce montage.
Parmi les variantes évaluées dans des protocoles confirmatoires, aucune option de raffinement (dépendance, ignorance, régulation, diversité, durcissement de l'évidentiel, réglage de γ) n'a démontré de gain robuste par rapport à E ou au meilleur probabiliste durci. Ces conclusions sont limitées aux instances, scénarios, budgets, paramètres et métriques étudiés. Elles ne constituent ni une démonstration d'équivalence générale entre représentations, ni une conclusion sur l'ensemble des mécanismes d'intégration de l'évidentiel.

## 4. Réserves et priorités
Réserves : w = 0,3 hérité de P10 (informé par la HV, bord de grille) ; références déjà vues avant les protocoles suivants ; P5, P8, P9, P11 : IC non repris ici ; P14 à P16 descriptifs ; P1 et P2 étape 1 absents des fichiers conservés ; RS1 non faite.
Priorités (avis de la relecture externe, que je partage) : 1) section méthodes corrigée ; 2) diagnostic des propositions communes ; 3) angle de l'article et revue ; 4) autres intégrations dans un GA classique, sans nouvelle expérience avant consolidation. Aucun de ces points n'est autorisé à ce stade.
