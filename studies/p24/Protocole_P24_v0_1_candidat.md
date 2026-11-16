# P24 v0.1 — Sensibilité locale des conclusions de P23 à w, σ et γ > 6 (QGA2-E) — CANDIDAT

**Statut : PROTOCOLE CANDIDAT, NON LANCÉ.** Date : 14 novembre 2026. Aucune implémentation, aucun calcul, aucun fichier existant modifié.
**Autorisation.** Message du Dr Montassar Zaghdoud, 14 nov. 2026, 22:40 : « Ok pour un protocole de sensibilité (w, σ, γ > 6) », en réponse à ma question « Voulez-vous que je rédige ce protocole en candidat, sans le lancer ? ». **Lecture retenue : rédaction seulement.** Implémenter, tester, calibrer, geler et exécuter exigent une autorisation écrite distincte. Les propositions d'autres assistants sont des entrées.
**Aucune revendication de nouveauté** (RS1 non faite). Le code et les protocoles gelés (P3 à P23) ne sont pas modifiés ; P24 n'ajoute que de nouveaux fichiers.

## 1. Question
Les conclusions de P23 (et, à w = 0,3, de P10 à P22) tiennent-elles quand on change raisonnablement trois paramètres figés : w (poids de la source ; 0,3 est HV-informé et au bord de la grille de P10), σ (seuil de similarité de DA, jamais testé) et γ de Dg (plafonné à 6, bord de la grille) ?
Il s'agit de **robustesse locale** : ce protocole ne démontre pas la généralisation à d'autres problèmes ou algorithmes, et il ne rend pas indépendant de la HV le choix historique de w = 0,3.

## 2. Référence et appariement
Référence = les résultats de P23 (w = 0,3, σ = 0,7, γ = 6, λ = 1) sur SC6 × graines 12000–12099. Les bras déjà exécutés en P23 (E, DA(1), Dg(γ = 6)) sont **réutilisés tels quels** (déterministes ; vérification bit à bit sur un échantillon de tâches avant gel). Les nouveaux bras sont exécutés sur les **mêmes** 100 graines et instances : toutes les comparaisons entre réglages sont appariées. Les HV de ces graines ont déjà été vues (P23) ; déclaré. Ce n'est pas une réplication indépendante ; c'est un test de robustesse sur les mêmes instances.

## 3. Bras
Cible : première front non dominé, QGA2-E inchangé, budget 6 040, HV oracle, comme P23.
- **Bloc w** (σ = 0,7, λ = 1) : w ∈ {0,15 ; 0,5 ; 0,7} (D24-1). Pour chaque w : E, Dp, DA(1), Dg(γ_w), où γ_w est calibré sans HV pour apparier la cible de DA(1) à ce w (§5). Au baseline w = 0,3 : ajout de Dp(w = 0,3) (absent de P23).
- **Bloc σ** (w = 0,3, λ = 1) : σ ∈ {0,6 ; 0,8} (D24-2). Pour chaque σ : DA(1, σ) et Dg(γ_σ) calibré pour l'apparier (si γ_σ = 6, le bras Dg(6) de P23 est réutilisé). E ne dépend pas de σ (réutilisé).
- **Bloc γ** (w = 0,3, σ = 0,7) : Dg(8) et Dg(12) (D24-3), comparés à DA(1) de P23. Si la calibration (§5) retient un γ > 6 pour apparier DA(1), ce γ_cal est celui du contraste correspondant.
Nombre de familles de 600 runs nouvelles : 12 (bloc w) + 1 (Dp à w = 0,3) + 2 (DA aux σ) + jusqu'à 2 (Dg aux σ) + 2 (Dg(8), Dg(12)) = **au plus 19**. Avec une grille w réduite à {0,5 ; 0,7} : au plus 13.
Hors périmètre (priorité secondaire, aucun essai) : ε, amplitude de rotation, budget, taille de population, autres familles d'instances, Rρ et Rmix.

## 4. Contrastes et critère de robustesse
Marge δ = 0,005 ; IC à 99 % marginaux, bootstrap percentile B = 20 000 sur les graines (conjoint), règle de décision de P23 (supériorité, infériorité, équivalence, non concluant ; infériorité et supériorité testées d'abord).
**Famille confirmatoire** (D24-5 : 15 contrastes en 3 sous-familles, IC marginaux sans correction, comme P23 ; la limite de couverture simultanée est déclarée) :
- w, pour chaque w ∈ {0,15 ; 0,3 ; 0,5 ; 0,7} : DA(1) − Dg(γ_w) ; DA(1) − E ; E − Dp (12 contrastes ; au baseline, les deux premiers sont ceux de P23).
- σ, pour chaque σ ∈ {0,6 ; 0,8} : DA(1, σ) − Dg(γ_σ) ; DA(1, σ) − E (4 contrastes).
- γ : DA(1) − Dg(8) ; DA(1) − Dg(12) (2 contrastes). [Total 18 avec le baseline w ; les deux contrastes DA − Dg et DA − E du baseline sont déjà établis en P23 et sont rapportés comme référence, non recomptés : 15 nouveaux contrastes.]
**Critère de robustesse (préenregistré)** : pour chaque contraste, la conclusion de P23 est « maintenue » si la décision (classe) au nouveau réglage est identique à celle du baseline ; « modifiée » sinon ; « non concluante » si l'IC contient à la fois le signe du baseline et zéro sans classe nette.
**Secondaires (IC 95 %, descriptifs)** : écarts par scénario et par type R/RC/C (agrégation : moyenne arithmétique des deux écarts S4 et S5 par graine) ; différence de contraste entre réglages (écart de DA − Dg entre w et le baseline, apparié) ; tendance descriptive selon w, σ, γ (aucune hypothèse de monotonie).

## 5. Calibration sans HV (avant gel)
Graines de calibration SC3 × 13700–13714 (plage distincte de P23 ; à vérifier contre le registre), tests techniques 13900–13909. Pour chaque w (et chaque σ), la cible de DA(1) est comparée à Dg(γ) sur la grille γ ∈ {1 ; 1,5 ; 2 ; 3 ; 4 ; 6 ; 8 ; 10 ; 12 ; 16} (D24-3) avec la règle de P23 : conforme si écart relatif d'entropie ≤ 10 % et |Δq_max| ≤ 0,05 ; parmi les conformes, plus petit écart d'entropie puis plus petit |Δq_max| ; sinon meilleur essai (J = gap² + (qgap/0,05)²), déclaré. Pour w = 0,3, la calibration vise à dire si un γ > 6 apparie mieux DA(1) que γ = 6. Le script de calibration ne calcule ni ne lit aucune HV (test dédié). Aucun γ n'est ajusté sur la HV ; l'objectif de calibration (appariement) est distinct de l'objectif de performance (ordre des HV).
Si γ_cal est un bord de grille (γ = 16 ou 1), c'est déclaré comme limite et aucune extension n'est faite après coup.

## 6. Instrumentation de la distribution effective (nouveauté par rapport à P23)
Journalisation inerte (sans RNG, sans effet sur la recherche), pour tous les nouveaux bras, aux générations 1, 25, 50, 100, 150 : **fréquences de décodage empiriques par patient** (matrice patients × équipes), en plus des indicateurs agrégés de P23. Analyse descriptive : distance moyenne (L1 et Jensen-Shannon) entre les distributions de décodage de DA(1) et de Dg apparié, à chaque génération ; relation avec l'écart de HV. Pour les bras réutilisés de P23, ces fréquences n'existent pas : seuls les nouveaux runs en disposent ; pour comparer DA(1) et Dg(6) de P23, il faudra exécuter de nouveau ces deux bras en mode journalisé (2 familles supplémentaires, **identiques** en HV aux résultats stockés, vérification bit à bit) (D24-4). Total possible : au plus 21 familles.

## 7. Tests (avant gel)
T1 reproduction bit à bit de tâches P23 stockées (E, DA(1), Dg(6) au baseline) avec le nouveau code. T2 w et σ n'agissent que par les paramètres déclarés (E à w ≠ 0,3 ≠ E de P23 ; DA(λ = 0) = E à chaque w). T3 cibles normalisées, finies, nulles hors masque pour toute la grille de γ jusqu'à 16. T4 budget exact de 6 040 pour tous les bras. T5 aucune fuite de l'oracle. T6 reproductibilité. T7 code et protocoles antérieurs inchangés (hachages P18 à P23). T8 le script de calibration ne contient aucun champ HV. T9 la journalisation des fréquences ne modifie pas la recherche (HV et archive identiques). T10 contrôle automatique des graines contre le registre complet. T11 cas limites (une équipe admissible, N = 1) pour tous les réglages.

## 8. Plan d'exécution et règles
Protocole confirmé → code et tests → pilote technique (13900–13909, durée mesurée) → calibration sans HV → sélection → gel avec hachages → exécution sous surveillance → précontrôle → analyse unique → rapport. Pas de relance pour améliorer un résultat ; hypothèses, marges et règles inchangées après lecture ; incidents déclarés (y compris toute lecture de HV avant gel) ; dépôt GitHub intact. **Durée estimée** : environ 15 minutes par famille de 600 runs sur 2 cœurs (mesuré en P23), soit environ 4 à 5 h pour 19 à 21 familles, plus calibration (environ 10 minutes par réglage), à confirmer au pilote.

## 9. Lecture des issues
- Conclusions maintenues : l'absence d'avantage de DA sur Dg apparié et l'équivalence DA ≈ E tiennent dans le voisinage testé.
- Conclusions modifiées pour certains w ou σ : le papier devra présenter les conditions de fonctionnement des représentations, non une supériorité de l'une.
- γ_cal > 6 apparie mieux DA(1) : les contrastes C1 à C3 de P23 sont à reconsidérer, sans jamais sélectionner γ sur la HV.
- Dans tous les cas : aucune conclusion hors de QGA2-E, SC6, budget 6 040 et plages testées.

## 10. Décisions à confirmer
D24-1 grille w {0,15 ; 0,5 ; 0,7} (ou {0,5 ; 0,7}) ; D24-2 grille σ {0,6 ; 0,8} ; D24-3 grille γ étendue jusqu'à 16 et Dg(8), Dg(12) ; D24-4 relance journalisée de DA(1) et Dg(6) pour obtenir les fréquences de décodage ; D24-5 famille de 15 contrastes, IC à 99 % marginaux sans correction (ou correction de Holm par sous-famille) ; D24-6 graines (12000–12099 réutilisées, calibration 13700–13714, tests 13900–13909, contrôle de registre) ; D24-7 critère « maintenu / modifié » ; D24-8 ordre par rapport au papier et à RS1.
