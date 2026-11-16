# Rapport final P17 — Tier 1 (analyse pré-enregistrée unique)

Dr M. Zaghdoud · 2026-11-11 · Protocole : `Protocole_P17_v0_2.md` · Gel : `p17_freeze1.txt` (2026-11-11T06:14:34Z)
Analyse : `p17_final_analysis.json` (SHA256 380f983b9ffbe1b75360ab40959918089f06d4ff643f1e8ffe063e6abc790f79), lancée une seule fois après contrôle préalable OK (600 fichiers, 100 graines 11200–11299 × 6 scénarios × 8 bras, budget 6040 exact).

## 1. Réponse courte
- **Évidentiel vs probabiliste (P4, DA−Dp)** : l'évidentiel (DA) bat le probabiliste de Dempster-lissé (Dp) : +0,0427 [+0,0401 ; +0,0454], supériorité, 100 % des graines positives, les 6 scénarios. Il est équivalent à E (E−DA = −0,00003).
- **DA vs Dg (P5)** : le probabiliste « global » (Dg) fait mieux que DA : DA−Dg = −0,0036 [−0,0064 ; −0,0009], infériorité (sous la marge 0,005 mais exclut 0). Dg ≥ DA dans 4 scénarios sur 6 (R et RC), DA légèrement meilleur sur C101.
- **Ignorance comme 4ᵉ objectif (P1, DA+SEL4−DA)** : +0,0077 [+0,0049 ; +0,0107], supériorité statistique.
- **Mais le contrôle aléatoire invalide l'attribution à l'ignorance (P2, DA+SEL4−DA+SELR)** : −0,0042 [−0,0070 ; −0,0015], infériorité. Un 4ᵉ objectif tiré au hasard (indépendant des génotypes) fait mieux (+0,0120 sur DA) qu'un 4ᵉ objectif d'ignorance. Le gain de P1 vient donc de l'ajout d'un objectif (modification du tri non dominé / de la diversité de sélection), pas du contenu « ignorance ».
- **Spécificité évidentielle (P3)** : (DA+SEL4−DA) − (Dp+SEL4−Dp) = +0,0073 [+0,0043 ; +0,0104], supériorité ; mais Dp+SEL4−Dp = +0,0004 [−0,0007 ; +0,0016] (aucun effet côté probabiliste). Compte tenu de P2, la lecture prudente : l'effet d'un 4ᵉ objectif existe pour DA, pas pour Dp, sans qu'il soit démontré que l'ignorance en est la cause.

## 2. Contrastes primaires (IC 99 % Bonferroni, marge 0,005, bootstrap B=20000 sur les graines)
| Contraste | Moyenne | IC 99 % | Décision |
|---|---|---|---|
| P1 DA+SEL4 − DA | +0,0077 | [+0,0049 ; +0,0107] | supériorité |
| P2 DA+SEL4 − DA+SELR | −0,0042 | [−0,0070 ; −0,0015] | infériorité |
| P3 spécificité DA vs Dp | +0,0073 | [+0,0043 ; +0,0104] | supériorité |
| P4 DA − Dp | +0,0427 | [+0,0401 ; +0,0454] | supériorité |
| P5 DA − Dg | −0,0036 | [−0,0064 ; −0,0009] | infériorité |

HV moyen (oracle) : E 0,5264 · DA 0,5264 · Dp 0,4837 · Dg 0,5300 · DA+SEL4 0,5342 · DA+SELW 0,5320 · DA+SELR 0,5384 · Dp+SEL4 0,5341 (0,4841).

Par scénario : P1 > 0 dans 5/6 (S4-C101 −0,0020) ; P2 < 0 dans 6/6 ; P4 > 0 dans 6/6 ; P5 < 0 dans 4/6, > 0 dans les 2 scénarios C101.

## 3. Secondaires (descriptifs, IC 95 %)
DA+SELW−DA +0,0056 [+0,0033 ; +0,0080] · DA+SELR−DA +0,0120 [+0,0101 ; +0,0139] · E−DA −0,00003 [−0,0012 ; +0,0012] · E−Dg −0,0036 · E−Dp +0,0427 · DA+SEL4−E +0,0078 · Dg−Dp +0,0463.
La pondération (SELW, λ=0,5) fait moins bien que le 4ᵉ objectif et que le contrôle aléatoire.

## 4. Diagnostics (génération 150, moyennes)
| Bras | m̄(Θ) | K | Dep | N_eff | q_max |
|---|---|---|---|---|---|
| E | 0,004 | 0,779 | 0,468 | 17,0 | 0,853 |
| DA | 0,047 | 0,775 | 0,267 | 22,1 | 0,709 |
| DA+SEL4 | 0,068 | 0,671 | 0,226 | 23,1 | 0,695 |
| DA+SELW | 0,017 | 0,779 | 0,065 | 34,3 | 0,854 |
| DA+SELR | 0,071 | 0,680 | 0,340 | 17,1 | 0,685 |

Sélection : front à 4 objectifs ≈ 0,44 de la population (SEL4), divergence avec la sélection à 3 objectifs ≈ 0,13 ; gain marginal d'ignorance G des sélectionnés ≈ 0,0065 (SEL4) contre 0 pour SELR (et ≈ −0,0003 pour Dp+SEL4).
Lecture : SEL4 n'a pas réduit l'ignorance finale de DA (m̄(Θ) 0,068 vs 0,047) ; le contrôle aléatoire donne le même niveau. Ignorance faible = consensus, non qualité. Aucun lien causal ignorance → HV n'est établi ; les corrélations brutes concentration–HV restent des artefacts de scénario.

## 5. Ce qui est établi / non établi
- Établi (une configuration, 6 scénarios, budget 6040) : DA ≫ Dp ; DA ≈ E ; Dg légèrement > DA ; un 4ᵉ objectif améliore DA d'environ +0,008 et un 4ᵉ objectif aléatoire d'environ +0,012.
- Non établi : que l'ignorance soit le bon critère de sélection ; l'effet de la régulation DEC adaptative (phase P de P16, non autorisée) ; tout résultat hors du cadre du Tier 1.
- Rappel : NSGA-II/MOEA/D dépassent tous les bras QGA2-E de 0,12–0,13 (résultats préliminaires antérieurs).

## 6. Incidents et transparence
1. Test vacuant `... or True` (7b) retiré avant le gel, suite relancée (17 contrôles PASS) puis gel ; même type d'incident que P15.
2. Lecture de l'autorisation : « sans arrêt » (07:06) lue comme implémentation, gel, exécution du Tier 1, analyse unique et rapport. Le message « Je vous autorise » (09:30), sans objet précisé, n'a été lu que comme confirmation de ce périmètre.
3. Deux surveillances en arrière-plan ont expiré par limite de temps ; l'exécution n'a pas été interrompue.
4. Aucun code gelé modifié ; GitHub non touché ; aucune relance ; analyse exécutée une seule fois.
5. w=0,3 hérité de P10 est informé par le HV (déclaré).

## 7. Décisions en attente (aucune exécutée)
Tier 2 de P17 (p. ex. SELR à plusieurs réalisations, variantes de 4ᵉ objectif) ; phase P de P16 ; addendum P16 (DA+L−DA+S) ; diagnostic à propositions communes ; erratum « m(∅)=K » dans le rapport P15 ; RS1 (recherche de nouveauté par l'auteur). Pour un article immédiat, le résultat net et publiable est : comparaison évidentiel/probabiliste (P4, P5) et résultat négatif/nuancé sur l'ignorance en sélection (P2).
