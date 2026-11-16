# Protocole P18 v0.1 — Phase P de P16 (régulation DEC) et Tier 2 de P17 (mécanisme du 4ᵉ objectif), préenregistré

Dr M. Zaghdoud · rédigé 2026-11-11 · à geler avant toute exécution (gel : `p18_freeze1.txt`).

## A. Autorisation et périmètre
Message de l'auteur, 12:36 : « J'autorise Tier 2, phase P, addendum P16, erratum P15, RS1 ». **Lecture :** (i) l'erratum P15 et l'addendum P16 (exploratoire, sans HV) sont exécutés (fait avant ce protocole, fichiers `p15/Rapport_pilote_P15.md`, `p16/p16_addendum.json`) ; (ii) RS1 : recherche web préliminaire seulement, sans valeur de preuve de nouveauté ; l'export Scopus/WoS/IEEE reste à faire par l'auteur ; (iii) phase P de P16 (partie A) et Tier 2 de P17 (partie B) sont exécutés en continu selon le présent protocole, avec **toutes les décisions ci-dessous prises par Claude, déclarées ici avant résultat**, puis analyse unique par partie et rapport. L'auteur n'a pas validé le détail de ces décisions ; il peut interrompre. **Non autorisé :** tout ajout d'arme, de graine, de marge, de λ, de seuil après résultat ; GitHub ; code gelé P3–P5, P7, P10, P11, P14–P17 inchangé.

## B. Partie A — phase P (régulation adaptative de DEC)
Question Q-R : la régulation de l'intensité DEC par l'ignorance (R1) fait-elle mieux, en HV oracle, que les intensités fixes ou le calendrier ?
Bras (8) : E ; DA ; DA+S ; DA+L ; DA+P11 (niveau Fixe-P11) ; DA+R1 (L si m̄_DA(Θ) ≥ τ sinon S) ; DA+R1inv (inverse) ; DA+SCH (L générations 1–50 puis S). Niveaux S=(5 ; 0,2), L=(2 ; 0,4), P11=(2 ; 0,2). Seuil τ = 0,03414872690282237 (calibration HV-aveugle P16, fichier `p16_thresholds.json`, non modifié). R2 n'est pas un bras (corrélation de rang 0,996–0,999 avec R1). Initialisation, nettoyage initial niveau S pour les bras DEC, chronologie : comme P16 v0.4 §F.
Données : SC6 × graines 11400–11459 (n = 60), budget 6040. Graines jamais utilisées.
Contrastes primaires (HV oracle moyen sur SC6 par graine ; bootstrap percentile B = 20000, unité = graine ; IC 99 % (5 primaires, Bonferroni) ; marge δ = 0,005) :
A1 R1 − S ; A2 R1 − L ; A3 R1 − R1inv ; A4 SCH − S ; A5 S − DA (effet du DEC de base).
Décisions : supériorité (borne inf > 0), infériorité (borne sup < 0), équivalence (IC dans ±δ), sinon non concluant.
Secondaires (IC 95 %, descriptifs) : L−S, P11−S, L−DA, R1−DA, S−E, DA−E ; par scénario ; diagnostics m̄(Θ), K, Dep, N_eff, q_max, q_ent aux générations 1/25/50/100/150 ; part de générations en L pour R1/R1inv ; compteurs DEC (réparés, violations).

## C. Partie B — Tier 2 (mécanisme du gain du 4ᵉ objectif)
Constat Tier 1 : un 4ᵉ objectif aléatoire (SELR) fait mieux que l'ignorance (SEL4). Hypothèse de mécanisme à tester : le gain vient de la diversité génotypique introduite par un 4ᵉ objectif dans le tri non dominé.
Nouveaux bras : DA+DIV (4ᵉ objectif = similarité génotypique moyenne du candidat aux autres candidats de la population de sélection, définie par la fraction de patients à équipe identique ; minimisée) ; DA+SELL (U de l'ignorance utilisé seulement pour départager des candidats de même front et de crowding égal à 1e-12 près) ; Dp+SELW (U entropique, λ = 0,5) ; Dg de γ = 2, 4, 8, 12 (courbe). Bras de référence repris des fichiers Tier 1 (mêmes graines et instances, déterministes, vérifiés bit à bit par test) : E, DA, Dp, Dg(6), DA+SEL4, DA+SELR, DA+SELW, Dp+SEL4.
Données : SC6 × graines 11200–11259 (n = 60, sous-ensemble des 100 du Tier 1 ; la HV de ces graines a déjà été vue en Tier 1 pour les bras de référence ; déclaré).
Contrastes primaires (IC 99 %, δ = 0,005) : B1 DA+DIV − DA ; B2 DA+DIV − DA+SELR ; B3 DA+DIV − DA+SEL4 ; B4 DA+SELL − DA ; B5 Dp+SELW − Dp.
Secondaires (IC 95 %) : courbe Dg(γ) − E et − Dg(6), Dg(γ) − Dp ; DA+DIV − E ; diagnostics de sélection (front à 4 objectifs, divergence).
Lecture préenregistrée : si B2 = équivalence ou DIV ≥ SELR et B1 > 0, le gain est compatible avec une explication par la diversité ; si DIV ≈ DA, la diversité n'explique pas le gain. Aucune causalité n'est affirmée à partir d'un seul montage.

## D. Règles communes
Un seul passage d'analyse par partie, HV lue uniquement à ce moment. Pas de relance pour améliorer. Les incidents sont déclarés. Les résultats restent « préenregistrés, un montage » ; pas de revendication de nouveauté (RS1 non faite). Le test de non-régression bit à bit (P16 stocké, P17 stocké) précède le gel.

## E. Décisions D18 (prises par Claude, déclarées)
D18-1 R2 exclue ; D18-2 n = 60 par partie (calcul limité à 2 cœurs, effet détectable ≈ 0,004 pour σ ≈ 0,011) ; D18-3 5 primaires par famille (A et B séparées), IC 99 % ; D18-4 τ de P16 inchangé ; D18-5 DIV défini ci-dessus (aucune information d'évidence) ; D18-6 baselines B repris de Tier 1 ; D18-7 pas de NSGA-II/MOEA/D rejoués (références P14 non appariées) ; D18-8 diagnostic « propositions communes » non exécuté (hors périmètre de la lecture).

## F. Incident avant gel (déclaré)
Premier passage des tests : l'échec du contrôle 3a (SELL à U constant ≠ sélection d'origine) révélait que SELL départageait les égalités par indice de patient alors que la sélection d'origine le fait par position dans le front. Corrigé dans `p18.sell_select` (défaut de code, pas de test), vérifié sur 200 tirages (200/200 identiques), suite relancée : 19 contrôles PASS. Sortie du premier passage conservée : `p18_tests_stdout_run1_FAIL3a.txt`. Aucune HV P18 lue. Le contrôle 3a a aussi été resserré (grille dyadique pour que les égalités soient exactes). Remarque : `p17.selw_select` (déjà gelé, utilisé par Dp+SELW) départage les égalités exactes par indice ; effet limité aux égalités exactes, déclaré.
