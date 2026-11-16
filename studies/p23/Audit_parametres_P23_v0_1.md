# Audit historique des paramètres — couverture expérimentale avant/avec P23 (v0.1)
Date : 14 novembre 2026. Autorisation : « OK pour les trois, dans cet ordre » (Dr M. Zaghdoud, 22:16). Travail documentaire : **aucun calcul, aucune relance**, aucun fichier existant modifié. Source : protocoles, rapports et JSON déjà produits (P3, P4, P7, P10, P11, P14, P16 à P23). Ce que je n'ai pas pu confirmer est signalé « non vérifié ». Aucune revendication de nouveauté.

## 1. Matrice de couverture
Niveaux : **Jamais** (jamais varié dans un contexte comparable) ; **Partiel** (varié, mais autre architecture, autre critère, calibration seule ou descriptif) ; **Couvert** (varié dans un plan préenregistré comparable).

| Paramètre | Valeur de P23 | Ce qui a été varié et où | Origine / HV-informé | Niveau | Risque pour les conclusions de P23 |
|---|---|---|---|---|---|
| w (poids de la source) | 0,3 | P10, calibration seule : w ∈ {0,3 ; 0,5 ; 0,7 ; 0,9}, bras E et P, SC3 × graines 9300–9314 (45 runs), critère = moyenne de HV(E) et HV(P). w = 0,3 retenu, **bord de grille** (déclaré). Jamais varié ensuite. | Oui : **informé par la HV** (déclaré dans P15, P17, P19, P23) | Partiel | **Élevé.** Dans la calibration P10, l'écart E − P dépend fortement de w (tableau §2). w règle aussi la concentration de Dp, Dg et DA. |
| σ (seuil de similarité de DA et de Dep) | 0,7 | Aucun résultat à σ ≠ 0,7. La règle P11 prévoyait une sensibilité σ ∈ {0,6 ; 0,8} « descriptive », mais le rapport P11 écrit qu'elle **n'a pas été testée**. σ = 0,7 a été choisi parce que le diagnostic sépare E de Dp (σ = 0,5 sature, σ ≥ 0,9 dévie, d'après P11). | Choix par diagnostic, pas par HV | Jamais | **Élevé** pour la famille DA (le seuil définit les sources « dépendantes »). |
| ε (plancher de probabilité) | 0,02 | Aucune variation retrouvée. Hérité de P5/P7 (même ε pour les contrôles et pour E, Dp, DA). | Choix de conception | Jamais | Moyen à élevé pour les cibles durcies (γ = 6) : le plancher borne la concentration maximale. |
| δ (amplitude de rotation) | 0,05π | P3 : trois jeux par algorithme, deux au bord de grille (QGA2 : 0,025π ; QGA2-E : 0,1π). P10 et suivants ont utilisé 0,05π **a priori**, non l'amplitude réglée en P3, avec une cible multi-sources (pas q − onehot) différente de celle de P3. | A priori | Partiel (autre architecture de cible) | Moyen. L'amplitude fixe la vitesse à laquelle une cible concentrée est suivie. |
| Budget | 6 040 | P3 : budget ×4 sur 20 graines (4300–4319), **descriptif**, QGA2-E classique : l'ordre entre QGA2-E et NSGA-II change de signe pour une hypothèse. Jamais avec les cibles évidentielles de P10 et suivants. | Conception | Partiel | Moyen. Les écarts de P23 (≈ 0,003) pourraient changer avec le budget. |
| γ (durcissement de Dg) | 6 (bord de grille) | P14 : grille {1 ; 1,5 ; 2 ; 3 ; 4 ; 6}, aucune valeur conforme à l'appariement, γ = 6 retenu comme meilleure tentative. P19/P22/P23 : grille jusqu'à 6. P17 « Tier 2 » (Dg pour γ ∈ {2 ; 4 ; 8 ; 12}) **non autorisé, non exécuté**. | Calibration sans HV (concentration) | Partiel | **Élevé.** Aucun Dg à γ > 6 n'a été exécuté. Le rapport P20 évoque un optimum probabiliste « γ ≈ 6–8 » (**non vérifié** : je n'ai pas retrouvé la courbe qui l'étaie). |
| γ (durcissement évidentiel) | — | P20 : γ ∈ {1,5 ; 2 ; 4 ; 6} sur E ; P21-B : γ autour de 1 (0,8 à 1,5) ; P19 (DAg6, DAgm) ; P22 (GEg6, GEgm). | Préenregistré | Couvert | Faible : durcir E ne l'améliore pas (Eg(6) − E = −0,016). |
| λ (dépendance de DA) | {0 ; 0,25 ; 0,5 ; 1} | P23 seulement (avant : λ = 1 fixé). | Préenregistré | Couvert pour ces 4 valeurs | Faible. |
| Plafond de dépendance (DEC) | sans DEC | P11 : (n_max = 2 ; ρ_max = 0,2), point le plus strict de la grille HV-aveugle ; **sensibilité σ et n_max non testée**. P16 : niveaux S = (5 ; 0,2), L = (2 ; 0,4), Fixe-P11, sans lecture de HV. P18 : régulation adaptative et niveaux fixes, avec HV : A1 à A5 en équivalence. | Règle HV-aveugle (P11), HV lue (P18) | Couvert pour les niveaux testés | Faible à moyen. |
| Taille de population et générations | 40 × 150 | Jamais variées indépendamment (liées au budget). | Conception | Jamais | Moyen. |
| Famille d'instances | SC6 | Six scénarios (S4/S5 × RC101/R101/C101), une famille de problèmes, un seul décodeur (P3). | Conception | Jamais | Limite de généralisation, pas de robustesse locale. |

## 2. Constat principal : l'écart E − P dépend de w (calibration P10, HV-informée)
SC3 × 9300–9314, 45 runs, descriptif, avec HV (donnée déjà connue ; non reproduite) :
| w | HV E | HV P | E − P |
|---|---|---|---|
| 0.3 | 0.6396 | 0.5811 | +0.0585 |
| 0.5 | 0.6305 | 0.5864 | +0.0442 |
| 0.7 | 0.6219 | 0.5860 | +0.0359 |
| 0.9 | 0.6175 | 0.5972 | +0.0203 |
L'avantage de E sur le probabiliste simple se réduit de 0,0585 à 0,0203 quand w passe de 0,3 à 0,9, parce que HV(P) augmente avec w tandis que HV(E) baisse. Cela rejoint l'idée que w pilote la concentration de la cible. Ces valeurs ne sont qu'un indice descriptif sur SC3 (autres graines, autres scénarios que SC6, pas d'IC), et la direction d'un éventuel changement sur les comparaisons DA contre Dg de P23 n'est pas déductible de ce tableau.

## 3. Lacunes prioritaires (si l'on veut tester la robustesse locale)
1. **w** : jamais varié hors calibration P10 ; critère de choix HV-informé ; w = 0,3 au bord de la grille. Les conclusions de P10 à P23 (E ≥ Dp, DA ≈ E, Dg légèrement devant DA) n'ont pas été vérifiées à d'autres w.
2. **σ** : aucune sensibilité ; seuil central pour DA.
3. **γ > 6** pour Dg : le meilleur appariement possible et l'éventuel optimum probabiliste n'ont pas été explorés.
4. **ε et δ** (amplitude de rotation) sous la cible multi-sources : jamais variés.
5. **Budget** : seul un test descriptif de P3, sur une autre cible.

## 4. Ce qui est déjà couvert (pas besoin de nouvelle expérience)
Durcissement de E (P20, P21-B), plan représentation × concentration (P19), GA classique guidé (P22), plafond de dépendance fixe et adaptatif (P11, P16, P18), balayage de λ (P23).

## 5. Limites de l'audit
Lecture des rapports et protocoles, pas relecture de tout le code. Je n'ai pas retrouvé de justification chiffrée de ε = 0,02 ni de la taille de population. Si un essai non archivé dans les fichiers de la session existe, il n'apparaît pas ici. Aucune de ces lignes n'autorise une nouvelle expérience : un éventuel protocole de sensibilité exigera votre décision écrite.
