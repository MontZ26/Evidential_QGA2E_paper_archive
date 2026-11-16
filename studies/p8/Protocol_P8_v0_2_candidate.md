# P8 v0.2 — Intégration de l'évidence externe (couche I) et de l'évidence de recherche (couche II) — CANDIDAT

**Statut :** candidat, NON gelé, NON autorisé. Date : 9 novembre 2026. Aucune expérience P8 (pilote, calibration, confirmatoire) ne peut démarrer avant confirmation écrite de l'auteur des décisions D8-1 à D8-10 (§11).
**Bases :** P7 v0.3 + D7-1..D7-8 + rapport final P7 ; G-D P8 (`/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p8/p8_gd_results.json`, SHA cd04d195…a256f) ; texte v0.2 fourni par l'auteur (tronqué au §8, traité comme entrée) ; recommandations D1–D5 de l'auteur. Moteur et code P4/P5/P7 gelés, inchangés.

## 1. Question
L'intégration de la couche I (données externes) et de la couche II (évidence de la population de recherche) améliore-t-elle le HV oracle au-delà des effets séparés, dépendances contrôlées ? Un résultat nul ou négatif est un résultat valide.

## 2. Motivation et limites (rapportées sans embellissement)
P7 : V1−V0c = +0,0250 (conflit moyen m(∅)=0,98, concentration extrême) ; V2−V0c = −0,0092 ; M2 descriptif. G-D partie V : réimplémentation conforme (4 320 cellules, écart 2,5e-16). G-D partie E (60 instances, GA classique, oracle HV) : vrai 0,674 ; nominal 0,648 ; moyenne probabiliste 0,627 ; historique seul 0,633 (descriptif). Calibration : A vrai dans [low,high] dans 20,2 % des cellules certifiées (sous 52,9 %, au-dessus 26,9 %) ; 9,3 % des cellules certifiées échouent dans la vérité cachée → les intervalles ne sont PAS des bornes de couverture et ne seront jamais présentés ainsi.

## 3. Architecture
**Couche I** (monde d'évaluation vu par l'optimiseur) : masses de p1m (doc/supervision/historique, affaiblissement de Shafer, conjonctive, Yager), monde nominal A=0,25+0,60·BetP, S=BetP. Inchangée (code P5 gelé). Registre de provenance (§6).
**Couche II** : modèle de population de P7 (M1) : V1 (Dempster) principal ; V0c contrôle probabiliste apparié ; V2 sensibilité secondaire.
**Interface :** (i) la couche I ne change QUE le monde d'évaluation (A_hat,S_hat) utilisé pour calculer les objectifs pendant la recherche ; (ii) la couche II ne change QUE la loi d'échantillonnage des parents/mutation à partir des individus évalués ; aucune règle de combinaison entre couches ; (iii) la couche II ne lit que des individus et leurs objectifs sous le monde de la couche I (jamais l'oracle) ; (iv) pas de rétroaction : la couche I est fixée avant la recherche et ne dépend pas de la population.

## 4. Plan 2×2 (définitions opérationnelles — D8-1)
Même instance, graine, décodeur, budget 6040 évaluations exactes, mêmes paramètres GA (C0b gelé, P7 pour la couche II).
- Couche I désactivée = monde non informatif : A_hat = 0,55 constante sur cellules certifiées (0,25+0,60·0,5), S_hat = 0,5 ; I activée = monde nominal.
- Couche II désactivée = GA classique C0b (pas de modèle) ; activée = P7 avec règle V1.
- A : off/off ; B : nominal/off ; C : non informatif/V1 ; D : nominal/V1.
- Famille appariée V0c : C', D' (mêmes que C, D avec V0c). Contrôle de concentration V0c-τ (D8-2, §5).
- Archives : vecteurs d'affectation ET objectifs conservés ; réévaluation post hoc sous l'oracle pour tous les bras.
Note : sous couche I désactivée, le front de recherche est quasi sans signal de compétence ; l'interaction est donc surtout un test de complémentarité, à interpréter avec cette réserve.

## 5. Conflit et concentration de V1 (D8-2)
Diagnostics enregistrés à chaque génération : m(∅) moyen, entropie de Pn, taille effective de support, part de masse du maximum. Contrôle apparié V0c-τ : V0c dont le paramètre w est choisi sur les graines de calibration pour égaler l'entropie moyenne de Pn de V1 (jamais sur les graines de test). Règle préenregistrée : si le gain V1−V0c disparaît face à V0c-τ, la conclusion est « gain attribuable à la concentration, non à la structure évidentielle » (descriptif). V2 : analyse de sensibilité uniquement.

## 6. Dépendance et double comptabilisation (D8-3)
Registre : source → origine (document, supervision ŷ=A+bruit, historique Beta, votes S) → lien avec la vérité cachée. Constat : supervision et historique dérivent partiellement de la même vérité. Contrôles (descriptifs, rapportés quel que soit le résultat) : (a) ablation de source (I sans supervision ; I sans historique) ; (b) combinaison prudente de Denœux de la couche I à la place de la conjonctive ; (c) comparaison K et largeur Pl−Bel avant/après ; (d) scénario redondant (historique dupliquée comme source supplémentaire) pour mesurer la sur-concentration. Aucune indépendance supposée sur la base des noms/formats.

## 7. Calibration de la couche I (D8-4)
Primaire : monde nominal non recalibré (cohérent avec G-D). Sensibilité B-cal : correction monotone affine du monde nominal ajustée sur graines de calibration (usage de la vérité dans la CALIBRATION seulement, simulation, explicitement hors-optimiseur de test) ; jamais présentée comme calibration réelle. Les intervalles low/high ne sont pas utilisés comme couverture.

## 8. Hypothèses et statistiques (D8-5, D8-6)
Unité : instance×graine (scénarios P5 × graines), 1 HV oracle par bras. Estimand primaire I_V1 = Y_D − Y_B − Y_C + Y_A (moyenne appariée). H0 : I_V1 = 0, bilatéral (direction non préenregistrée comme attendue). α = 0,05. Test : bootstrap-t apparié (B=20000, règles Bv/B<0,99 → p=1 et sd nul comme P6). Famille de Holm (3) : I_V1 ; I_V0c ; D−V0c-τ pair (D vs D' avec τ) — secondaires hors famille : D−B, D−C, B−A, C−A, V2, ablations, B-cal. Dimensionnement : n ∈ {100,150,200,300}, ±0,01 sur I, puissance 80 %, 1500 simulations sur variances du pilote, plafond 300 ; si non atteignable à 300 → arrêt, rapport descriptif.

## 9. Graines et séparation des données (D8-7)
Technique/G-D 8000–8009 (utilisé) ; calibration 8100–8114 ; pilote 8150–8179 ; confirmatoire 8200–8399 ; analyse bootstrap 9801. Aucune graine/shard P5/P6/P7 réutilisée. Paramètres de la couche II : P7 gelé ; réglage éventuel uniquement sur 8100–8114, config partagée entre bras.

## 10. Gates avant exécution
- **G-P7** : fait (note de décision : V1 candidat, V0c contrôle, V2 sensibilité).
- **G-D** : fait (V valide ; E descriptif ; calibration défaillante déclarée).
- **G-I** (à faire) : tests d'interface : bras A reproduit bit à bit le GA C0b classique ; aucun accès à l'oracle dans l'optimisation (instrumentation) ; budget exact 6040 pour 4+2+1 bras ; archives complètes ; couche I fixée avant recherche.
- **G-C** (à faire) : diagnostics de concentration V1 et construction de V0c-τ sur 8100–8114 ; règle de l'§5 figée.
- **G-Y** (à faire) : pilote 30 graines (8150–8179) pour variances → dimensionnement ; critères d'arrêt (§8).
- **Gel** : hash du protocole + code + paramètres avant toute lecture confirmatoire. Un amendement doit être écrit avant tout résultat confirmatoire lu.

## 11. Décisions à confirmer par écrit (avec valeur par défaut proposée)
D8-1 définition des bras (§4) ; D8-2 contrôle V0c-τ et règle de concentration (§5) ; D8-3 contrôles de dépendance (§6) ; D8-4 couche I primaire non recalibrée + B-cal en sensibilité (§7) ; D8-5 test bilatéral, α 0,05, famille de Holm de 3 (§8) ; D8-6 sizing ±0,01, 80 %, cap 300 (arrêt si impossible) ; D8-7 graines (§9) ; D8-8 V2 en sensibilité seulement ; D8-9 n final par défaut = n requis arrondi à la grille (ou 200 comme P6/P7 sur votre ordre) ; D8-10 autorisation d'enchaîner G-I, G-C, G-Y, gel et confirmatoire sans arrêt si les gates passent (sinon arrêt et rapport).

## 12. Engagements
Pas de ré-exécution pour améliorer les résultats ; pas de changement d'hypothèse/seuil après résultats ; incidents rapportés ; dépôt GitHub intact ; code P4/P5/P7 inchangé ; arrêt acceptable.
