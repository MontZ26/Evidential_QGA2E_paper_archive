# Protocole P6 — Sélection parentale dans les QIGA probabilistes (v0.5, CANDIDATE)

**Statut : CANDIDATE, NON approuvé, NON gelé. Aucun code, calibration, run ou analyse n'est autorisé par ce texte.** Une approbation écrite explicite de l'auteur est requise. Le texte reçu intitulé « P6 v0.2 » et les avis reçus sur la v0.3 (autres assistants) ; cette v0.5 ne corrige que trois imperfections de rédaction de la v0.4 (renvoi de version au §1, ponctuation au §9, intitulé de D-3 au §12) et ne change aucune règle sont des entrées, non des autorisations ; leurs critiques valides (statistique de H6.1, biais de calibration, budget partiel, flux, statut de H6.4 et de P6-C) sont intégrées ici.
Auteur : Dr Montassar Zaghdoud. Rédaction : Claude. Date : 8 novembre 2026. Légende : **[D-n]** décision à confirmer (§12).

## 1. Contexte, honnêteté de conception
P6 prolonge P5 (formulation A, masque, trois objectifs, HV exact, point de référence (1,2 ; 1,2 ; 1,2), six scénarios, budget 6 040, archive 200, LS 1-shift/2-swap, survie (μ+λ), code P5 gelé réutilisé sans modification). **P6 est rédigé avant la lecture de tout résultat confirmatoire de P5-B** ; il s'appuie seulement sur des observations exploratoires de P5 (P5-A : C0b ≈ +0,036 de HV sur C2c ; pilote : C2 ≈ +0,059 sur C3), qui sont des **motivations, non des résultats**. P6 ne démarrera qu'après la livraison du rapport final de P5 et l'approbation écrite de l'auteur ; si le rapport final de P5 modifiait le contexte, une nouvelle version serait nécessaire avant toute approbation.

## 2. Question
La sélection parentale **par tournoi dans la population évaluée** améliore-t-elle les algorithmes à modèle probabiliste par rapport à une sélection aléatoire dans cette même population, et cet effet dépend-il de la règle de mise à jour (rotation ou PBIL) ? Hypothèse explicative (non démontrée) : le tournoi transmet des combinaisons d'affectations performantes que le modèle factorisé par patient ne représente pas. P6 ne teste pas la perte de corrélations en soi (étude distincte, éventuellement P7) et ne cherche aucun avantage quantique physique.

## 3. Cycle commun (définitif) [D-1, D-2]
Population courante P_t évaluée, taille N (μ = λ = N), population initiale commune à tous les bras (flux « init » de P5). Chaque génération produit **N enfants, séquentiellement**, chacun par l'une des deux routes, tirée par un flux dédié « p6_route » avec probabilité ρ pour la route M :
- **Route M (modèle)** : une affectation tirée du modèle probabiliste (flux « samp »), puis mutation ciblée ; pas de croisement.
- **Route G (génétique)** : deux parents choisis dans **P_t** (voir §4), croisement uniforme (p_c), mutation ciblée.
Pour chaque enfant : évaluation, insertion à l'archive, LS avec probabilité p_LS (règle de P5, mêmes flux), puis les N solutions finales passent en survie (μ+λ) par `select_next`. Modèle mis à jour une fois par génération après la survie, selon la stratégie d'élites **c** de P5 (k_e calibré) avec la règle de plancher de P5 ; jamais après la dernière génération (partielle ou non). Budget : compteur unique ; les voisins de LS consomment chacun une évaluation et entrent dans l'archive qu'ils soient acceptés ou rejetés (règle de P5) ; les enfants sont produits séquentiellement jusqu'à épuisement ; la LS est interrompue si le budget est atteint ; seuls les enfants effectivement produits et évalués entrent dans la dernière survie ; aucune mise à jour du modèle après la dernière génération, partielle ou non [D-8].
Le tirage de route est effectué pour chaque enfant dans **tous** les bras probabilistes ; il consomme le même flux dans C2-R/T et C3-R/T.

## 4. Bras (5)
| Bras | Mise à jour | Parents de la route G |
|---|---|---|
| C2-T | rotation (P5 §5.2) | **deux tournois binaires indépendants** (un par parent, avec remise : les deux parents peuvent être identiques), rang puis crowding dans P_t (calculés au début de la génération ; égalité totale : tirage aléatoire, flux « p6_tie ») |
| C2-R | rotation | deux individus de P_t tirés uniformément avec remise (flux « p6_par ») |
| C3-T | PBIL (P5 §5.3) | tournoi |
| C3-R | PBIL | aléatoire |
| C0b-T | aucun modèle (ρ = 0) | tournoi (identique au C0b de P5) |
Le facteur « sélection parentale » est isolé dans chaque paire R/T : même population initiale, même modèle, même ρ, mêmes opérateurs, mêmes paramètres [D-3].

## 5. Calibration [D-3, D-4]
Même procédé que P5 : 50 configurations × 5 seeds, puis 5 meilleures × 10 seeds, scénarios S4, tirage par nom de bras ; paramètres : N pair [20 ; 100], ρ ∈ [0,2 ; 0,8] (ρ = 0 ou 1 exclus car ils annulent le facteur étudié), p_c, η_k, p_LS, k_LS, règle LS, ε, k_e, δ (C2) ou λ (C3), mêmes plages que P5. **Chaque paire R/T partage une même configuration, choisie sur un critère commun aux deux variantes** : chaque configuration candidate est évaluée dans les deux bras (R et T) et classée par la moyenne de leurs HV ; on retient la meilleure de la paire (isolement strict du facteur sans calibrer en faveur de T seul). Étape 1 : seeds 6000–6004 (50 configurations) ; étape 2 : seeds 6005–6014 (5 finalistes), critère commun inchangé. Limite : ce réglage commun peut ne convenir parfaitement à aucune des deux variantes. **C0b-T reprend la configuration retenue de C0b en P5** (même architecture) [D-4].

## 6. Seeds et phases [D-5]
Calibration 6000–6014 ; pilote 6050–6079 (C2-T contre C2-R et C3-T contre C3-R : écart-type des contrastes) ; confirmation 6200…6200+n−1 ; P6-C descriptif : variantes sans LS pour C2-T, C2-R et C0b-T sur les 100 premières seeds, **ablation à budget d'évaluations constant** (la suppression de la LS libère des évaluations pour davantage d'enfants ; ce n'est pas une mesure isolée de l'effet de la LS) ; tests techniques 6900–6909 ; graine d'analyse 9101. **Dimensionnement de H6.1** : le pilote estime l'écart-type de **S_s** (et, pour information, celui de I_s) ; n : méthode de P5 appliquée à S_s (effet minimal 0,01 ; puissance 80 % ; grille {100, 150, 200, 300} ; cap 300 ; action décidée maintenant : exécuter n ≤ 300 et déclarer la sous-puissance si besoin ; aucune modification après le pilote).

## 7. Hypothèses préenregistrées
Mesure : HV moyen par seed sur les six scénarios (monde T) ; D absolue ; unité = la seed ; Wilcoxon apparié bilatéral, zero_method « wilcox », p = 1 si écarts nuls ou moins de 6 non nuls ; bootstrap sur les seeds, 10 000 réplications, percentile, graine 9101.
- **Définitions par seed s** : D2_s = HV(C2-T)_s − HV(C2-R)_s ; D3_s = HV(C3-T)_s − HV(C3-R)_s ; S_s = (D2_s + D3_s)/2 ; I_s = D2_s − D3_s. Les quatre résultats d'une seed sont appariés ; l'unité statistique est la seed.
- **Primaire (α = 0,05)** : **H6.1** effet moyen du tournoi : médiane des S_s ≠ 0, test de Wilcoxon signé-rang appliqué à la série (S_s). Il s'agit de l'effet moyen du tournoi **dans l'algorithme hybride** (route M + route G, ρ calibré) et non d'une propriété de tous les QIGA.
- **Secondaire (Holm sur 3)** : **H6.2** interaction : série (I_s) ≠ 0 (une interaction n'établit pas que le tournoi aide les deux méthodes ; D2 et D3 sont rapportés séparément avec IC et tailles d'effet)  ; **H6.3** C2-T ≠ C3-T ; **H6.4** C2-T ≠ C0b-T, **déclarée comparaison d'architectures** (sans attribution causale au seul tournoi).
- **Rapportés pour les quatre contrastes fondamentaux (D2, D3, S, I)** : différence moyenne, IC bootstrap, taille d'effet (biais rang-bisériel) et p, pas seulement les p.
- **Descriptif** : C2-R contre C3-R, effets de simple sélection par règle, C0b-T contre les autres, P6-C, H6.5 = part d'enfants insérés dans l'archive au moment de leur évaluation, par route (M ou G) et par bras (distinct de leur présence dans l'archive finale), entropie du modèle, diversité, convergence, temps.
- Équivalence pratique descriptive : IC 95 % dans [−0,01 ; +0,01]. Aucune hypothèse modifiée après les résultats.

## 8. Intégrité
Mêmes règles que P5 §12 : hachage du protocole et du code avant la calibration, gel vérifié à chaque lancement, aucune modification du code P5 gelé (P6 ajoute `p6.py`), pas de réexécution pour améliorer un résultat, analyse unique, précontrôle séparé (complétude, forme (n,3), n_eval = 6 040), flux indépendants par opérateur avec description de leur consommation, incident = arrêt et rapport.

## 9. Tests techniques pré-gel
Population initiale identique entre bras ; mêmes flux et mêmes variates aléatoires (nombres tirés) dans la paire R/T, sans exiger que les affectations échantillonnées restent identiques après la première génération ; trajectoires identiques R/T si la sélection parentale est neutralisée en conservant exactement les mêmes flux, les mêmes appels aléatoires et le même ordre d'exécution ; budget exact (N = 20 et 100, ρ = 0,2 et 0,8) ; C0b-T égal à C0b de P5 à configuration identique, après comparaison explicite du cycle, des opérateurs, des flux, des paramètres et du compteur d'évaluations ; conservation de la norme et plancher (déjà testés en P5, re-exécutés) ; cas limites (équipe unique, archive pleine, doublons d'élites) ; script d'analyse sur données synthétiques.

## 10. Calcul estimé
Estimation indicative (extrapolation, non engagement) : cinq bras ≈ 55 % du coût par seed de P5-B, soit environ 3,5 h pour n = 300 sur deux cœurs, plus ≈ 1 h de calibration (davantage avec le critère commun, qui évalue chaque configuration dans deux bras), plus P6-C.

## 11. Limites
Modèle factorisé par patient (la perte de corrélations n'est pas testée) ; ρ entre 0,2 et 0,8 seulement ; configuration commune à chaque paire R/T ; calibration sur S4 seulement ; stratégie d'élites c héritée d'une sélection exploratoire de P5-A ; formulation unique (ordre fixé) ; aucune extrapolation au routage intégré.

## 12. Décisions à confirmer par l'auteur
D-1 cycle à deux routes (M / G) du §3 ; D-2 ρ comme paramètre calibré dans [0,2 ; 0,8] ; D-3 chaque paire R/T partage une même configuration, choisie sur un critère commun (§5) ; D-4 C0b-T reprend la configuration de P5 ; D-5 seeds, cap 300 et graine 9101 ; D-6 famille primaire (H6.1) et famille secondaire à trois (Holm) ; D-7 P6 démarre après le rapport final de P5, avec vérification que la stratégie d'élites c reste pertinente ; **D-8** règles de budget partiel et d'archive du §3 ; **D-9** calibration par critère commun de chaque paire R/T (§5) ; **D-10** définitions de S_s et I_s et dimensionnement sur S_s (§6, §7).
