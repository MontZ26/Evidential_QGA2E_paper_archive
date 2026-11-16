# Rapport du pilote P15 — DA-DST (plus de dépendance, plus d'ignorance) — DESCRIPTIF
Date : 11 novembre 2026. **Pilote exploratoire, 30 graines (10900–10929) × 6 scénarios SC6 × 6 bras, budget 6 040 ; aucun test confirmatoire ; aucun résultat n'est une preuve.** Autorisation : message du Dr Montassar Zaghdoud (00:34). Gel vérifié (p15_freeze1.txt), précontrôle OK, analyse unique. IC95 % : bootstrap percentile sur les graines (B = 20 000, tag 10990), non ajustés ; pas de p-valeur.
Décisions D-DA appliquées par défaut (non encore tranchées par l'auteur) : définition M, opérateur par puissance du poids d'évidence, λ = 1 (axiome), σ = 0,7 (P11), w = 0,3 (hérité de P10, choix informé par la HV, déclaré), sources = premier front, témoins P-DA, V2, Dg (γ = 6, non conforme à G-N), E, Dp.

## 1. HV oracle moyenne (n = 30 graines)
Dg 0,5306 ; E 0,5254 ; DA 0,5252 ; Dp 0,4822 ; PDA 0,4821 ; V2 0,4803.

## 2. Contrastes descriptifs (moyenne [IC95 %])
- **DA − E : −0,0003 [−0,0024 ; +0,0018]** (DA devant E dans 53 % des graines) : pas de différence détectable.
- DA − PDA : +0,0430 [+0,0394 ; +0,0465] ; DA − V2 : +0,0448 [+0,0416 ; +0,0479] ; DA − Dp : +0,0430.
- DA − Dg : −0,0055 [−0,0085 ; −0,0025] ; E − Dg : −0,0052 [−0,0083 ; −0,0019].
- E − Dp : +0,0432 (reproduit P10/P14) ; E − V2 : +0,0451.
- PDA − Dp : −0,0001 [−0,0006 ; +0,0005] ; V2 − Dp : −0,0018 [−0,0040 ; +0,0004].

## 3. Ignorance, conflit, concentration (moyennes sur 180 runs, générations 1 / 25 / 50 / 100 / 150)
| Bras | m(Θ) | conflit K | q_max |
|---|---|---|---|
| E | 0,068 / 0,008 / 0,003 / 0,003 / 0,002 | 0,70 / 0,90 / 0,89 / 0,82 / 0,79 | 0,45 / 0,67 / 0,75 / 0,82 / 0,86 |
| DA | 0,159 / 0,040 / 0,030 / 0,033 / 0,041 | 0,70 / 0,90 / 0,88 / 0,83 / 0,79 | 0,45 / 0,65 / 0,70 / 0,72 / 0,71 |
| V2 | 0,28 / 0,23 / 0,23 / 0,23 / 0,23 | 0,32 / 0,40 / 0,40 / 0,40 / 0,41 | 0,27 / 0,25 / 0,25 / 0,25 / 0,25 |
Pour Dp, Dg, P-DA, la valeur m(Θ) = 0,7 et le conflit 0 sont nominaux (1 − w), non mesurés : ces bras ne sont pas évidentiels. Rapport d'effectifs ñ / nombre de sources pour DA : 1,00 / 0,97 / 0,86 / 0,72 / 0,64 (la correction n'agit qu'après la génération 50).
- **H1 :** à sources identiques, m(Θ) de DA ≥ m(Θ) de E (test unitaire : vérifié sur 60 jeux de sources aléatoires). Dans les runs, la moyenne de m(Θ) de DA dépasse celle de E à 150 générations sur 150 (descriptif).
- **H2 :** q_max moyen : V2 0,249 ≤ DA 0,685 ≤ E 0,761 (ordre conforme à la conjecture C1 sur ces moyennes).
- **H4 :** corrélation de rang m(Θ) moyen par run contre HV, à l'intérieur de chaque scénario : E 0,10 ; DA 0,06 ; V2 0,06 (faible).

## 4. Lecture autorisée / non autorisée
Autorisé (pilote, n = 30) : (i) l'ignorance de DA est environ dix fois celle de E après la génération 25 (0,03–0,04 contre 0,003) et sa concentration finale est plus basse (0,71 contre 0,86), mais la HV ne diffère pas de façon détectable (|Δ| ≤ 0,0024) ; (ii) le probabiliste à effectifs corrigés (P-DA) n'apporte aucun gain par rapport à Dp, alors que la structure de Dempster en apporte un à correction égale ; (iii) la règle prudente V2, qui garde le plus d'ignorance, n'est pas meilleure que Dp ; (iv) Dg dépasse légèrement E et DA, comme dans P14 ; (v) le conflit n'est pas réduit par la correction de dépendance.
Non autorisé : dire que la correction de dépendance améliore ou n'améliore pas l'optimisation (n = 30, un seul réglage de λ, σ, w) ; dire que l'ignorance n'a pas d'effet ; toute revendication de nouveauté (RS1) ; en faire des hypothèses confirmatoires.
Les tailles d'échantillon indicatives (±0,01, 80 %) pour un éventuel confirmatoire sont très faibles (3 à 12 graines) parce que les écarts de ce pilote sont petits : elles ne sont pas fiables, la marge ±0,01 étant grande devant les IC observés. Un confirmatoire éventuel doit fixer sa marge d'équivalence avant tout calcul.

## 5. Incidents et écarts
Dans la première exécution des tests, une ligne de test contenait « or True » (test vide) : je l'ai retirée avant le gel et réexécuté la suite (16 tests, tous réussis) ; H1 a été reformulée avant le gel (propriété à sources identiques). Les décisions D-DA sont des défauts de ma part. Aucun rerun, dépôt GitHub et code gelé inchangés. SHA256 de p15_final_analysis.json : 57ce112a80abc6022d99bcb70027aaf8d9207042f55e219b383b41ceaf848f79


> **Erratum de nommage (2026-11-11, autorisé par l'auteur).** Dans la version initiale, la quantité notée « m(∅) » est le conflit conjonctif non normalisé K = 1 − e^{−W}(1+Σ_s(e^{W_s}−1)), champ `m_empty` du code. Les valeurs sont inchangées ; seul le nom est corrigé (1 occurrences). Aucun résultat n'est modifié. Original conservé : `Rapport_pilote_P15_original.md`.
