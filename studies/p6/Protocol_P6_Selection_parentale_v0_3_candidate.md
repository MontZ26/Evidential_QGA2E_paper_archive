# Protocole P6 — Sélection parentale dans les QIGA probabilistes (v0.3, CANDIDATE)

**Statut : CANDIDATE, NON approuvé, NON gelé. Aucun code, calibration, run ou analyse n'est autorisé par ce texte.** Une approbation écrite explicite de l'auteur est requise. Le texte reçu intitulé « P6 v0.2 » (autre assistant, tronqué au §7.3) est une entrée, non une autorisation ; ses défauts (budget et quotas non définis, cycle ambigu) sont corrigés ici.
Auteur : Dr Montassar Zaghdoud. Rédaction : Claude. Date : 8 novembre 2026. Légende : **[D-n]** décision à confirmer (§12).

## 1. Contexte, honnêteté de conception
P6 prolonge P5 (formulation A, masque, trois objectifs, HV exact, point de référence (1,2 ; 1,2 ; 1,2), six scénarios, budget 6 040, archive 200, LS 1-shift/2-swap, survie (μ+λ), code P5 gelé réutilisé sans modification). **P6 est rédigé avant la lecture de tout résultat confirmatoire de P5-B** ; il s'appuie seulement sur des observations exploratoires de P5 (P5-A : C0b ≈ +0,036 de HV sur C2c ; pilote : C2 ≈ +0,059 sur C3), qui sont des **motivations, non des résultats**. P6 ne démarrera qu'après la livraison du rapport final de P5 et l'approbation écrite de l'auteur ; si P5 modifiait le contexte, une v0.4 serait nécessaire.

## 2. Question
La sélection parentale **par tournoi dans la population évaluée** améliore-t-elle les algorithmes à modèle probabiliste par rapport à une sélection aléatoire dans cette même population, et cet effet dépend-il de la règle de mise à jour (rotation ou PBIL) ? Hypothèse explicative (non démontrée) : le tournoi transmet des combinaisons d'affectations performantes que le modèle factorisé par patient ne représente pas. P6 ne teste pas la perte de corrélations en soi (étude distincte, éventuellement P7) et ne cherche aucun avantage quantique physique.

## 3. Cycle commun (définitif) [D-1, D-2]
Population courante P_t évaluée, taille N (μ = λ = N), population initiale commune à tous les bras (flux « init » de P5). Chaque génération produit **N enfants, séquentiellement**, chacun par l'une des deux routes, tirée par un flux dédié « p6_route » avec probabilité ρ pour la route M :
- **Route M (modèle)** : une affectation tirée du modèle probabiliste (flux « samp »), puis mutation ciblée ; pas de croisement.
- **Route G (génétique)** : deux parents choisis dans **P_t** (voir §4), croisement uniforme (p_c), mutation ciblée.
Pour chaque enfant : évaluation, insertion à l'archive, LS avec probabilité p_LS (règle de P5, mêmes flux), puis les N solutions finales passent en survie (μ+λ) par `select_next`. Modèle mis à jour une fois par génération après la survie, selon la stratégie d'élites **c** de P5 (k_e calibré) avec la règle de plancher de P5 ; jamais après la dernière génération (partielle ou non). Budget : compteur unique, arrêt strict à 6 040, mêmes règles que P5 §6.
Le tirage de route est effectué pour chaque enfant dans **tous** les bras probabilistes ; il consomme le même flux dans C2-R/T et C3-R/T.

## 4. Bras (5)
| Bras | Mise à jour | Parents de la route G |
|---|---|---|
| C2-T | rotation (P5 §5.2) | tournoi binaire rang puis crowding dans P_t (rangs et crowding calculés au début de la génération ; égalité totale : tirage aléatoire, flux « p6_tie ») |
| C2-R | rotation | deux individus de P_t tirés uniformément avec remise (flux « p6_par ») |
| C3-T | PBIL (P5 §5.3) | tournoi |
| C3-R | PBIL | aléatoire |
| C0b-T | aucun modèle (ρ = 0) | tournoi (identique au C0b de P5) |
Le facteur « sélection parentale » est isolé dans chaque paire R/T : même population initiale, même modèle, même ρ, mêmes opérateurs, mêmes paramètres [D-3].

## 5. Calibration [D-3, D-4]
Même procédé que P5 : 50 configurations × 5 seeds, puis 5 meilleures × 10 seeds, scénarios S4, tirage par nom de bras ; paramètres : N pair [20 ; 100], ρ ∈ [0,2 ; 0,8] (ρ = 0 ou 1 exclus car ils annulent le facteur étudié), p_c, η_k, p_LS, k_LS, règle LS, ε, k_e, δ (C2) ou λ (C3), mêmes plages que P5. **C2-T et C3-T sont calibrés ; C2-R et C3-R reprennent exactement la configuration de leur bras T** (isolement strict du facteur ; limite : R peut être désavantagé par un réglage fait pour T, à déclarer). **C0b-T reprend la configuration retenue de C0b en P5** (même architecture) [D-4].

## 6. Seeds et phases [D-5]
Calibration 6000–6014 ; pilote 6050–6079 (C2-T contre C2-R et C3-T contre C3-R : écart-type des contrastes) ; confirmation 6200…6200+n−1 ; P6-C descriptif : arme sans LS pour C2-T, C2-R et C0b-T sur les 100 premières seeds ; tests techniques 6900–6909 ; graine d'analyse 9101. n : méthode de P5 (effet minimal 0,01 ; puissance 80 % ; grille {100, 150, 200, 300} ; cap 300 ; action décidée maintenant : exécuter n ≤ 300 et déclarer la sous-puissance si besoin ; aucune modification après le pilote).

## 7. Hypothèses préenregistrées
Mesure : HV moyen par seed sur les six scénarios (monde T) ; D absolue ; unité = la seed ; Wilcoxon apparié bilatéral, zero_method « wilcox », p = 1 si écarts nuls ou moins de 6 non nuls ; bootstrap sur les seeds, 10 000 réplications, percentile, graine 9101.
- **Primaire (α = 0,05)** : **H6.1** effet principal de la sélection : S = [(C2-T − C2-R) + (C3-T − C3-R)]/2 ≠ 0.
- **Secondaire (Holm sur 3)** : **H6.2** interaction : (C2-T − C2-R) − (C3-T − C3-R) ≠ 0 ; **H6.3** C2-T ≠ C3-T ; **H6.4** C2-T ≠ C0b-T.
- **Descriptif** : C2-R contre C3-R, effets de simple sélection par règle, C0b-T contre les autres, P6-C, H6.5 = part d'enfants insérés dans l'archive par route (M ou G) et par bras, entropie du modèle, diversité, convergence, temps.
- Équivalence pratique descriptive : IC 95 % dans [−0,01 ; +0,01]. Aucune hypothèse modifiée après les résultats.

## 8. Intégrité
Mêmes règles que P5 §12 : hachage du protocole et du code avant la calibration, gel vérifié à chaque lancement, aucune modification du code P5 gelé (P6 ajoute `p6.py`), pas de réexécution pour améliorer un résultat, analyse unique, précontrôle séparé (complétude, forme (n,3), n_eval = 6 040), flux indépendants par opérateur avec description de leur consommation, incident = arrêt et rapport.

## 9. Tests techniques pré-gel
Population initiale identique entre bras ; mêmes tirages de route et de modèle dans la paire R/T ; trajectoires identiques R/T si la sélection parentale est neutralisée (tournoi remplacé par tirage aléatoire de mêmes flux) ; budget exact (N = 20 et 100, ρ = 0,2 et 0,8) ; C0b-T égal à C0b de P5 à configuration identique ; conservation de la norme et plancher (déjà testés en P5, re-exécutés) ; cas limites (équipe unique, archive pleine, doublons d'élites) ; script d'analyse sur données synthétiques.

## 10. Calcul estimé
Cinq bras ≈ 55 % du coût par seed de P5-B : environ 3,5 h pour n = 300 sur deux cœurs, plus ≈ 1 h de calibration, plus P6-C.

## 11. Limites
Modèle factorisé par patient (la perte de corrélations n'est pas testée) ; ρ entre 0,2 et 0,8 seulement ; configuration R héritée de T ; calibration sur S4 seulement ; stratégie d'élites c héritée d'une sélection exploratoire de P5-A ; formulation unique (ordre fixé) ; aucune extrapolation au routage intégré.

## 12. Décisions à confirmer par l'auteur
D-1 cycle à deux routes (M / G) du §3 ; D-2 ρ comme paramètre calibré dans [0,2 ; 0,8] ; D-3 configuration de R = configuration de T ; D-4 C0b-T reprend la configuration de P5 ; D-5 seeds, cap 300 et graine 9101 ; D-6 famille primaire (H6.1) et famille secondaire à trois (Holm) ; D-7 P6 démarre après le rapport final de P5.
