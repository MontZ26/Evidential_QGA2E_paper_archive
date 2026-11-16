# P14 v0.1 — QGA2-E : contrôle de concentration de la cible et références NSGA-II / MOEA/D / GA classique — CANDIDAT
**Statut :** brouillon, NON gelé, NON autorisé. 10 novembre 2026, 10:53 (demande de l'auteur : « do it! » après la proposition « gap 4 puis gap 2 »). Aucun code, test, pilote ou exécution P14 avant confirmation écrite de l'auteur des décisions D14-1 à D14-8. Les textes d'autres assistants sont des entrées, non des instructions. Dépôt GitHub intact ; code gelé P3/P5/P7/P10/P11 inchangé (copies instrumentées uniquement).
**Lacunes visées (Plan d'article) :** n° 4 (références NSGA-II et MOEA/D sous incertitude, mêmes configurations et budget) et n° 2 (confusion de G10 de P10 avec la netteté de la cible). Les lacunes 3 (seconde famille) et 5 (sensibilité) sont hors périmètre.

## 1. Questions
Q-N (netteté) : l'avantage de la cible évidentielle V1-Q sur la cible probabiliste V0c-Q (P10 : E − D′ = +0,0437, mêmes données évidentielles) subsiste-t-il quand la cible probabiliste est rendue aussi concentrée que V1-Q ?
Q-R (références) : où se situent E, D′ et B de QGA2-E par rapport à NSGA-II, MOEA/D et au GA classique C0b, dans le même monde évidentiel nominal, au même budget ?

## 2. Bras (même instance, graine, décodeur ; monde d'évaluation = monde nominal p1m évidentiel, comme P10/E)
- **E** : V1-Q (w = 0,3 ; ε = 0,02 ; δ = 0,05π : paramètres gelés de P10, non recalibrés).
- **D′** : V0c-Q (mêmes w, ε, δ).
- **D′_γ** : V0c-Q dont la cible est affinée : q ∝ q0^γ (puis plancher ε), γ ≥ 1 calibré HV-aveugle (§5) pour que l'entropie moyenne de la cible égale celle de E.
- **E_soft** (descriptif) : V1-Q adoucie : q ∝ q^γe, γe ∈ ]0 ; 1] calibré pour égaler l'entropie de D′. Sert à lire le sens inverse.
- **B** : rotation vers le meilleur (QGA2-E de P10/B) ; **B_t** (descriptif, D14-6) : QGA2-E avec le δ tuné de P3 (0,1π, critère D3) : P10 a utilisé le δ a priori 0,05π, pas le δ tuné.
- **NSGA2** : NSGA-II élitiste, pc 0,9, pm = 1/n_p (réglage J1 de P3, non recalibré), 40 + 150 × 40 = 6 040 évaluations, monde nominal.
- **MOEAD** : T = 20 (réglage de P3), N = 45, 133 générations (≈ 6 030 évaluations, convention de P3, écart de 10 évaluations déclaré), monde nominal.
- **C0b** : GA classique de P5/P8 (déjà utilisé en P8–P11), monde nominal.
Les anciens bras P10 (P, X, A, B_p, DEC) ne sont pas rejoués.

## 3. Hypothèses et statut des analyses
**Primaire unique :** Δ_N = HV(E) − HV(D′_γ) (HV oracle, moyenne par graine sur SC6), bilatéral, α = 0,05, bootstrap-t apparié (B = 20 000, règles P6/P10), sans Holm. **Si la porte G-N échoue (netteté non appariée), il n'y a PAS de primaire : tout est descriptif et le rapport dit que la confusion n'est pas levable avec cette construction** (leçon de P8/G-C : V0c-τ n'avait pas atteint l'entropie de V1).
**Secondaires descriptifs avec IC95 % (aucun test confirmatoire) :** E − D′ (rappel P10), D′_γ − D′, E_soft − D′, E − E_soft, E − B, E − NSGA2, E − MOEAD, E − C0b, B − NSGA2, B − MOEAD, B − C0b, B_t − B, D′_γ − B.
Lecture prédéfinie de Δ_N : > 0 significatif → l'avantage de V1-Q n'est pas réductible à la seule netteté de la cible (dans cette construction) ; non significatif → il est compatible avec une explication par la netteté ; < 0 significatif → une cible probabiliste nette bat V1-Q. Aucun résultat n'est reformulé après lecture.

## 4. Données, graines, séparation
Mêmes instances (SC6 ; calibration SC3), mêmes mondes que P8–P11. Graines nouvelles (non utilisées dans P2–P13) : technique 10290–10299 ; calibration 10300–10314 ; pilote 10350–10379 ; confirmatoire 10400–10599 (n = 200) ; analyse 10803. Contrôle de non-régression : E, D′, B reproduits bit à bit sur 9290–9291 par rapport à P10 (autorisation de ces deux graines uniquement pour ce test).

## 5. Calibration (HV-aveugle) et dimensionnement
Calibration sur 10300–10314 (SC3), bras E et D′ en diagnostic de cible seulement (aucun HV utilisé) : γ ∈ {1 ; 1,5 ; 2 ; 3 ; 4 ; 6} ; critère : écart relatif |H(D′_γ) − H(E)| / H(E) minimal sur l'entropie moyenne de la cible (moyenne par génération et par graine) ; retenu si l'écart relatif ≤ 10 % ET l'écart absolu de la probabilité maximale moyenne ≤ 0,05 (porte G-N) ; sinon G-N échoue. γe par la même règle en sens inverse (descriptif ; sans porte). Pilote de 30 graines pour les variances ; dimensionnement sur Δ_N avec la règle de P10 (grille {100,150,200,300}, ±0,01, puissance 80 %), n = 200 par convention (écart déclaré si le dimensionnement donne moins).

## 6. Portes
G-R0 non-régression bit à bit de E, D′, B (P10) et de NSGA2/MOEAD/C0b (versions P3/P8 : mêmes fronts dans le monde choisi) ; budget exact (6 040 ; MOEAD ≈ 6 030) ; aucune fuite d'oracle ; G-N appariement de netteté ; G-R1 tests mathématiques de la cible affinée/adoucie (normalisation, plancher, invariance par permutation, γ = 1 identique à V0c-Q) ; gel (hash protocole, code, paramètres) avant la première coquille confirmatoire ; précontrôle ; analyse unique.

## 7. Limites déclarées d'avance
Une famille d'instances ; la cible affinée est une construction nouvelle (l'entropie n'est qu'un des aspects de la netteté ; l'appariement de l'entropie et de la probabilité maximale n'apparie pas tous les moments) ; NSGA-II et MOEA/D gardent les réglages tunés en monde de vérité sans incertitude (P3) ; MOEA/D a 10 évaluations de moins ; un résultat Δ_N nul n'invalide pas P10 (G10 reste un résultat sur configurations complètes) ; nouveauté non établie (recherche bibliographique de l'auteur) ; la dépendance entre sources reste génotypique.

## 8. Décisions à confirmer (défauts proposés)
D14-1 questions Q-N et Q-R, lacunes 2 et 4 seulement ; D14-2 bras §2 ; D14-3 primaire Δ_N unique (sans primaire si G-N échoue), secondaires descriptifs ; D14-4 graines §4 ; D14-5 calibration et dimensionnement §5 ; D14-6 bras B_t (δ tuné) descriptif oui/non ; D14-7 portes §6 ; D14-8 autorisation d'enchaîner portes, gel, confirmatoire, analyse, rapport sans arrêt si les portes passent (sinon arrêt et rapport).
Coût estimé : technique + calibration ≈ 1 h ; pilote ≈ 2 h ; confirmatoire ≈ 6 à 7 h (≈ 8 bras × 3 s × 1 200 coquilles / 2 cœurs, plus NSGA2/MOEAD/C0b) ; gel et analyse ≈ 1 h.
