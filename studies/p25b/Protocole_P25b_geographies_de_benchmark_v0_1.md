# Protocole P25b v0.1 — Évaluation indépendante sur des géographies de fichiers de benchmark publics
Statut : rédigé AVANT calibration et exécution. Autorisation de l'auteur : message du 15 nov. 09:21 (« continuer sans arrêt jusqu'à produire la nouvelle version du papier »). Fichiers nouveaux ; code gelé P3–P25 inchangé ; dépôt GitHub non touché. Aucune revendication de nouveauté.

## 1. Pourquoi
La validation P25 utilisait des géographies synthétiques. Pour répondre à une critique prévisible sur les données, P25b utilise des **coordonnées de fichiers de benchmark publics jamais utilisés** (les autres instances Solomon R1xx/R2xx, C1xx/C2xx, RC1xx/RC2xx partagent les coordonnées de R101, C101, RC101 : écartées).

## 2. Géographies (fichiers, hachages dans files_sha256.txt ; copie issue de github.com/PyVRP/VRPLIB, commit 309f1890, données de test)
B-X : Uchoa et al. X-n101-k25 ; B-M : Christofides et al. M-n101-k10 ; B-G : Golden_1 (240 clients) ; B-L : Li_21 (560 clients) ; B-O : ORTEC-n242-k12 (décrit comme dérivé d'un service réel de livraison) ; B-H : Homberger C1_2_1 (200 clients). Pour chaque graine, 100 clients tirés sans remise (graine) dans le fichier, coordonnées remises à l'échelle uniforme (boîte max 100), dépôt = dépôt du fichier ; les 50 premiers tirés sont les patients (n_p = 50, N_T = 10, fin de journée 240, visite 10 ; paramètres fixés avant tout résultat sur critère de faisabilité : 10/10 faisables par scénario). Compétences, équipes, fenêtres, vérité cachée, sources d'évidence : générateur inchangé (simulés).
## 3. Graines
Calibration 15700–15714 (B-X, B-G, B-O) ; pilote 15900–15909 ; principal 15000–15059 (60 × 6 = 360 tâches).
## 4. Bras, contrastes, règles
Identiques à P25 (bras E, Dp, DA(1; σ=0,7), Dg(γ_cal) à w ∈ {0,3 ; 0,7}, Dg(6) à w=0,3 ; contrastes K1–K5 ; IC 99 % marginal, bootstrap B=20000 apparié, δ=0,005 ; ordre de décision ; Bonferroni en sensibilité ; vérification d'appariement sans recalibration ; référence : contrastes P25, cohérence descriptive de direction et de classe). γ_cal choisi sans HV par la règle P24 ; si la porte n'est pas satisfaite : meilleur essai, déclaré.
## 5. Procédure
Tests → calibration HV-aveugle → sélection → pilote → essai à sec → gel → exécution reprenable → précontrôle → une analyse → rapport. Pas de rerun ; pas de changement après résultats ; incidents déclarés.
