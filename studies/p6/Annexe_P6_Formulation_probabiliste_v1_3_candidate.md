# Annexe explicative — Formulation probabiliste de P6 (CANDIDATE, non gelée, non approuvée)

Statut : texte explicatif, rattaché au protocole P6 v1.3 (SHA-256 251b2e44…2f92a39). Il ne modifie
ni les bras, ni les hypothèses, ni les règles statistiques. Aucun code, aucune exécution P6.
Les formules génériques ci-dessous (taille de tournoi t, critère de rang) sont des notations ;
les valeurs et critères réels sont ceux du protocole.

## A. Définition d'un QIGA probabiliste (au sens de P5/P6)
Algorithme génétique « inspiré quantique » dont la composante quantique est un modèle de probabilités
explicite, échantillonné pour générer des solutions et mis à jour à partir des élites.
Ce n'est ni un algorithme quantique ni une simulation d'états quantiques.
Modèle factorisé par patient : P_ik = α_ik², Σ_k P_ik = 1, P_ik ≥ ε après plancher.
Mises à jour comparées : rotation d'amplitudes (C2) et PBIL p ← (1−λ)p + λq (C3), même plancher ε.

## B. Génération hybride
Route M avec probabilité ρ (échantillonnage du modèle), route G avec probabilité 1−ρ (deux parents + croisement).
Pr(x) = ρ · Π_i P_{i,x_i} + (1−ρ) · Σ_{a,b} π(a) π(b) · Pr_cross(x | a,b)   (puis mutation).
π = distribution de sélection parentale : le facteur manipulé par P6.

## C. Sélection parentale
Population de taille N classée du rang 1 (meilleur) à N.
Aléatoire (R) : π_R(r) = 1/N.
Tournoi (T), taille t, tirage avec remise, vainqueur = meilleur tiré :
π_T(r) = [(N−r+1)^t − (N−r)^t] / N^t.
Meilleur : 1 − ((N−1)/N)^t ≈ t/N ; pire : 1/N^t.

## D. Risque de concentration
Entropie du modèle : H(P) = −(1/n) Σ_i Σ_k P_ik log P_ik. Elle décroît au fil des mises à jour ;
la route M reproduit alors des quasi-copies des élites. La route G porte la diversité résiduelle :
T accroît la pression de sélection sur G, R la maintient exploratoire.
Question de P6 : cette pression supplémentaire aide-t-elle ou nuit-elle quand M se concentre déjà,
et dépend-elle de la règle de mise à jour ?

## E. Lien avec les hypothèses
D2 = HV(C2-T) − HV(C2-R) ; D3 = HV(C3-T) − HV(C3-R) ;
S = (D2+D3)/2 (H6.1) ; I = D2 − D3 (H6.2).
Une H6.2 significative indique seulement que l'effet du tournoi diffère entre les deux règles ; elle ne prouve
pas que la rotation est globalement meilleure que PBIL.

## F. Portée
Conclusions limitées à cette architecture : modèle factorisé, hybride M/G avec ρ calibré, stratégie d'élites c.
H(P) pourra être rapportée à titre descriptif (diagnostic de concentration), sans test confirmatoire.
