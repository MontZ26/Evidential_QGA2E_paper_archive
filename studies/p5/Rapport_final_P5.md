# Rapport final P5 — IQGA‑HHC‑Affectation : rotation d'amplitudes (C2) contre PBIL (C3) et NSGA‑II avec opérateurs auxiliaires (C0b)

Protocole : P5 v0.3 gelé (SHA‑256 6d951085…d4736), amendement v0.3.1 (n = 300, décision de l'auteur du 8 nov. 12:49, avant lecture de tout résultat de P5‑B). Stratégie d'élites retenue en P5‑A : c.
P5‑B : 1 800 tâches (6 scénarios × 300 graines, 5200–5499), toutes terminées, aucune infaisable, aucune graine exclue, aucun front vide. P5‑C (ablation sans LS) : 600 tâches (6 × 100 graines, 5200–5299).
Précontrôle `p5_precheck.py` : PASS. Analyse exécutée **une seule fois** (`an_p5_final.py`). Gel vérifié avant et après (True). Dépôt GitHub non touché.
Empreintes : p5_final_analysis.json f3922772…0f6def ; p5_final_stdout.txt cc21aad5…bd4c (autres dans p5_postrun_hashes.txt).

## 1. Résultat confirmatoire primaire (H5.1, Wilcoxon apparié bilatéral, α = 0,05, n = 300)
C2 − C3 (HV moyen sur 6 scénarios, par graine) = **+0,0548**, IC bootstrap 95 % [+0,0534 ; +0,0561], médiane +0,0544, 300/300 graines positives, corrélation rang‑bisériale +1,00, p = 6,1e‑51.
**H5.1 rejetée : C2 > C3, avantage de la rotation sur PBIL** dans cette implémentation et ce dispositif.

## 2. Famille secondaire (Holm sur 2)
| Hypothèse | Différence | IC 95 % | + / − | p Holm | Lecture |
|---|---|---|---|---|---|
| H5.2 C2 (stratégie c) − C2a (stratégie a) | +0,0048 | [+0,0034 ; +0,0062] | 196 / 104 | 3,4e‑10 | significatif mais dans la zone d'équivalence descriptive ±0,01 (« pratiquement nul ») |
| H5.4 C2 − C0b | **−0,0384** | [−0,0398 ; −0,0370] | 0 / 300 | 1,2e‑50 | **C0b (NSGA‑II + mêmes opérateurs auxiliaires) significativement meilleur que C2** |
H5.3 est descriptive (§3).

## 3. Descriptif (non confirmatoire)
HV moyen (n = 300) : MOEA/D 0,682 ; NSGA‑II 0,681 ; C0b 0,661 ; **C2 0,622** ; C2a 0,617 ; C3 0,567 ; QGA2 0,562 ; QGA2‑E 0,530 ; QGA‑XM‑E 0,515.
C2 contre les références rejouées de P4 : QGA2 +0,060 ; QGA2‑E +0,092 ; QGA‑XM‑E +0,108 (toutes 300/300). C2 contre NSGA‑II −0,059 et contre MOEA/D −0,060 (300/300 en faveur de ces derniers) ; C0b − NSGA‑II −0,020.
IGD+ (plus petit = mieux) : MOEA/D 0,011 ; NSGA‑II 0,012 ; C0b 0,022 ; C2 0,045 ; C3 0,085. Temps de recherche moyen : C2 1,33 s ; C3 1,46 s ; C0b 1,53 s ; NSGA‑II 3,16 s.
Part des enfants insérés dans l'archive (H5.3) : C2 3,2 % ; C3 0,8 % ; C0b 8,7 % ; NSGA‑II 12,3 %.
Diversité (Hamming, fin de run) : C3 ≈ 0,67 (population presque non convergée), C2 ≈ 0,40, C0b ≈ 0,39. Entropie du modèle (génération 10) : C2 0,27 ; C3 1,24 — le modèle PBIL reste proche de l'uniforme, la rotation converge.

## 4. P5‑C — ablation sans recherche locale (100 graines, descriptif)
HV moyen sans LS : C2 0,525 ; C3 0,559 ; C0b 0,677. Gain de la LS : **C2 +0,097 ; C3 +0,008 ; C0b −0,016**.
C2‑noLS − C3‑noLS = **−0,034** [−0,037 ; −0,031], 0/100 positives : **sans LS, PBIL bat la rotation.** C2‑noLS − C0b‑noLS = −0,152.
Lecture : l'avantage confirmé de la rotation sur PBIL (H5.1) **dépend de la recherche locale**; sans elle il s'inverse. C0b sans LS (0,677) atteint le niveau de NSGA‑II (0,681) et fait mieux qu'avec LS : la LS n'explique pas l'avance de C0b.
Réserve : P5‑C porte sur 100 graines (5200–5299) et est descriptif; les valeurs sans LS sont à budget d'évaluations constant, les évaluations libérées allant aux générations.

## 5. Lecture selon la règle écrite d'avance
- **Confirmé :** la rotation d'amplitudes surpasse le contrôle PBIL apparié (H5.1) et tous les QGA antérieurs de P3/P4 (descriptif).
- **Non atteint :** aucun avantage sur un GA classique : C0b > C2 (H5.4, confirmatoire) et NSGA‑II/MOEA/D > C2. Aucune supériorité du QIGA sur un GA classique n'est montrée.
- **Nuance importante :** l'avantage C2 > C3 passe par l'interaction avec la LS (P5‑C), pas par la rotation seule.
- Hypothèses mécanistiques (non testées) : modèle factorisé qui perd les corrélations inter‑patients ; sélection parentale moins directe ; convergence du modèle (entropie basse). À ne pas présenter comme résultats.

## 6. Écarts et divulgations obligatoires
1. Calibration sur trois scénarios S4 seulement (choix consigné). 2. n = 300 par amendement de l'auteur au lieu de n = 100 (règle gelée), décidé avant lecture des résultats P5‑B. 3. Plages MOEA/D (H ∈ {6,8,10,12}, T ∈ [5,20]) choisies à l'implémentation.
4. Stratégie c choisie sur P5‑A (exploratoire, sans valeur confirmatoire). 5. P5‑C limité à 100 graines. 6. Références P4 rejouées avec leurs sorties natives. 7. Graines techniques 5900–5909.
8. Le run a été interrompu plusieurs fois par les limites des tâches de fond; reprises avec le même code gelé, gel vérifié à chaque lancement, écritures atomiques, aucune valeur modifiée.
Limites : une famille d'instances (dérivées de Solomon), ordre de visite fixe, un seul décodeur, un seul type de modèle factorisé; nouveauté non établie (recherche systématique Scopus/WoS/IEEE Xplore à faire par l'auteur).

## 7. Conséquences pour la suite (décisions de l'auteur)
P6 (tournoi vs aléatoire dans un QIGA probabiliste) reste candidat v1.3 : son hypothèse porte sur une architecture qui, d'après P5, n'atteint pas C0b ni NSGA‑II; l'intérêt de P6 doit être réexaminé par l'auteur à la lumière de ce rapport.
P7/P8 : candidats ; P5 n'a aucune incidence directe sur leur statut, mais il rappelle que les gains des modèles dépendent de l'interaction avec la recherche locale. Aucune étape suivante n'est lancée.
