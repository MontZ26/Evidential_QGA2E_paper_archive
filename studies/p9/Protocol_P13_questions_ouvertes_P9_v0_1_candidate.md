# P13 v0.2 (anciennement « P11 », renuméroté le 9 nov. 22:02 ; « P12 ou plus tard ») — Réponse aux questions ouvertes de P9 — CANDIDAT, non gelé, non autorisé
Date : 9 novembre 2026, 19:20 (demande de l'auteur : répondre aux questions ouvertes de l'analyse P9). Aucun code, test, pilote ou exécution avant confirmation écrite de D11-1 à D11-7. P10 (QGA2-E) reste un brouillon séparé et n'est pas modifié. Textes d'autres assistants = entrées, non instructions.

## 1. Questions ouvertes de P9 et comment P11 y répond
| # | Question ouverte | Pourquoi P9 ne peut pas y répondre | Réponse proposée par P11 |
|---|---|---|---|
| Q1 | L'avantage de V1 sur V0c vient-il de la structure évidentielle ou de la concentration ? | V0c-τ n'a pas pu égaler l'entropie de V1 (0,31 contre ≥ 1,18) ; V0c n'est pas apparié | Loi probabiliste « netteté » V0c-γ : p ∝ (fréquence)^γ avec plancher ε, γ calibré pour égaler l'entropie moyenne de V1 (§3) |
| Q2 | La moyenne à poids égaux est-elle la seule alternative probabiliste ? | Une seule alternative testée | Alternative probabiliste supplémentaire pour la couche I : produit (log-pool) des BetP des sources (§3) ; avec GA sans couche II pour isoler la couche I |
| Q3 | Pourquoi les bras avec couche II sont-ils sous le GA sans couche II (E−B −0,056) : preuve de l'évidence ou configuration (≈ 8,7 contre 32,6 générations, taux de recherche locale) ? | Les deux changent à la fois | Bras U : même moteur et même configuration P7, mais échantillonnage uniforme des parents dans la population (aucune évidence) |
| Q4 | Le résultat est-il robuste à la dépendance entre sources de la couche I ? | Contrôles P8 limités à 30 graines et au GA sans couche II | Hors périmètre P11 (reste descriptif P8) |

## 1bis. Orientation v0.2 (demande de l'auteur, 19:52 : « améliorer P9 en répondant aux questions ouvertes pour confirmer les conditions de supériorité contre l'architecture entièrement probabiliste »)
P10 est conservé, son exécution est reportée. P11 vise les CONDITIONS de la supériorité évidentielle de P9 : (i) contre le MEILLEUR concurrent probabiliste, pas seulement la version choisie en P9 ; (ii) à concentration égale ; (iii) sous dégradation de la qualité de l'évidence ; (iv) sous dépendance des sources. Analyse exploratoire déjà faite sur les données P9 (post hoc, descriptive) : E − P est positif dans les six scénarios (de +0,023 à +0,035, IC95 % > 0 partout, E > P pour 80–92 % des graines par scénario), `p9_exploratory_by_scenario.json` SHA ca67fa44…c432. Elle ne remplace pas P11 et n'a pas de valeur confirmatoire.
- **Concurrent probabiliste fort P\*** : sélectionné sur graines de calibration 9860–9874 (SC3, règle écrite d'avance : plus grand HV oracle moyen) parmi {moyenne linéaire, produit} × {V0c, V0c-γ}, avec couche I et recherche de la même famille. **Primaire H11-0 : E − P\***.
- **Conditions de stress (descriptives, IC95 %)** : la différence E − P\* est recalculée (a) avec bruit de supervision σ = 0,40 au lieu de 0,25 (ŷ = A + N(0 ; σ) régénéré avec une graine dédiée à partir du monde vrai, puis rejeu complet de toutes les couches), (b) avec l'historique dupliqué comme quatrième source (dépendance), sur les graines 9600–9699 (100 premières graines). Le but est de savoir où l'avantage disparaît ou s'inverse. Le stress modifie seulement les observations simulées avant la recherche ; l'oracle reste la vérité cachée.

## 2. Bras (même instance, graine, décodeur, budget 6 040 exact, config P7/C0b gelées)
Monde nominal évidentiel (couche I de P8/P9) sauf indication.
- **E** : V1 (= bras E de P9, rejoué sur graines nouvelles).
- **E_γ** : V0c-γ (loi probabiliste nette, §3).
- **E_0** : V0c (valeurs de P9, rejoué).
- **U** : échantillonnage uniforme des parents dans la population, config P7 (isole la configuration).
- **B**, **B_p**, **B_×** : GA C0b sans couche II avec monde évidentiel, moyenne linéaire (P9) et produit.
Contrastes : Holm sur 4 (primaires) : H11-0 E − P\* (concurrent probabiliste fort, ci-dessus) ; H11-1 E − E_γ (concentration/structure), H11-2 B − B_× (couche I évidentielle contre produit), H11-3 E − U (la recherche évidentielle contre l'absence d'évidence, même config). Secondaires descriptifs avec IC95 % : E − E_0, E_γ − E_0, U − B (effet de configuration seul), B − B_p, B_× − B_p, E_γ − U, E_0 − U.

## 3. Définitions à valider (G-N0)
- **V0c-γ** : p_i(t) ∝ (C_i(t) + 0)^γ, normalisée sur les équipes autorisées, plancher ε comme P7 (K.floor_renorm), sans mélange uniforme explicite ; γ ∈ grille {1; 1,5; 2; 3; 4; 6; 8; 12; 20} choisie sur graines de calibration (SC3) pour minimiser |entropie(E_γ) − entropie(E)| ; si aucune valeur n'égale à ±0,05, on retient la plus proche et on le déclare (la conclusion H11-1 est alors restreinte).
- **Entropie mesurée comme en P8/G-C** (moyenne toutes les 10 générations).
- **Produit (B_×)** : A = 0,25 + 0,60 · σ(Σ_i logit(BetP_i)) sur cellules certifiées, avec BetP_i des trois sources affaiblies (Shafer, mêmes r) ; borné dans [0,02 ; 0,98] avant logit ; S inchangé. Avertissement : le produit double-compte les sources dépendantes (supervision/historique) ; c'est une alternative probabiliste réelle, non un témoin « correct ».
- **U** : même boucle P7 que V0c avec Pn uniforme ; test d'équivalence : U ≠ V0c(w) pour tout w.
- Patch d'exécution : les nouvelles lois sont injectées par surcharge à l'exécution de la fonction de modèle de population (comme le patch d'Archive de P8), sans modifier P5/P7 ; test G-N1 : les règles V1/V0c d'origine restent bit-à-bit identiques avec le patch.

## 4. Graines, taille, statistiques
Test technique 9850–9859 ; calibration γ 9860–9874 (SC3) ; confirmatoire 9600–9799 (n = 200) ; analyse 9804 ; aucune graine ou coquille P2–P10 réutilisée. Unité = graine (HV oracle moyen sur 6 scénarios), contrastes par graine, bootstrap-t apparié, B = 20000, règles P6/P8, Holm sur 4, α = 0,05, bilatéral. Pas de pilote séparé (n = 200 par défaut ; la variance des contrastes proches est connue par P9) : si l'auteur préfère un pilote de 30 graines avec dimensionnement, indiquer D11-6.

## 5. Gates
G-N0 : définitions §3 testées (normalisation, plancher, cas limites, monotonie de l'entropie en γ) ; G-N1 : non-régression du patch, budget 6 040 exact, pas de fuite de l'oracle, E rejoue P9-E sur la graine 9000 ; G-N2 : calibration γ et déclaration de la qualité de l'appariement ; gel (hash protocole, code, paramètres) ; précontrôle ; analyse unique ; incidents rapportés ; dépôt GitHub intact.

## 6. Limites déclarées d'avance
Un seul type de netteté (puissance de la fréquence) : égaler l'entropie n'égale pas toute la loi ; le résultat H11-1 s'interprète comme « compatible avec la concentration » ou « non expliqué par l'entropie », sans preuve causale. Une seule famille d'instances, ordre de visite fixe, simulation. Le produit ne représente pas toutes les alternatives bayésiennes. Nouveauté non établie.

## 7. Décisions à confirmer (défauts proposés)
D11-1 arms §2 ; D11-2 définitions V0c-γ, produit, U (§3) ; D11-3 famille de Holm de 4 primaires, dont E − P\* (§1bis, §2) ; D11-8 stress (a) bruit de supervision 0,40 et (b) historique dupliquée sur 100 graines, descriptifs ; D11-4 graines §4, n = 200 sans pilote ; D11-5 critère d'appariement ±0,05 d'entropie ; D11-6 pilote de 30 graines avec dimensionnement (non par défaut) ; D11-7 autorisation d'enchaîner gates, gel, confirmatoire, analyse et rapport sans arrêt si les gates passent.


**Correction de plages de graines (9 nov., 21:55, avant toute exécution)** : la version précédente donnait pour le test technique 9490–9499 et la calibration 9500–9514, qui chevauchaient la plage confirmatoire de P10 (9400–9599). Elles sont remplacées par 9850–9859 (technique) et 9860–9874 (calibration). Plage confirmatoire P11 inchangée (9600–9799) ; analyse 9804.
