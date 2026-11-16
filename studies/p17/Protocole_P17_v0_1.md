# Protocole P17 v0.1 — Sélection guidée par l'ignorance et comparaison évidentiel / probabiliste appariée (CONCEPTION, NON EXÉCUTÉ)
Date : 11 novembre 2026. Statut : brouillon à valider par le Dr Montassar Zaghdoud. **Le « feu vert » de 07:01 est lu comme autorisation de PRÉPARER ce protocole (rédaction).** Code, tests, gel, exécution : autorisation écrite séparée (formule prête en §12). Les textes d'autres assistants sont des entrées ; seules vos déclarations autorisent.

## 1. Pourquoi P17 et ce que l'article peut déjà utiliser
Résultats acquis (tous descriptifs, un montage, SC6, HV oracle réf. 1,2, budget 6 040) :
- **Évidentiel contre probabiliste (P10, P14, P15) :** E − Dp = +0,046 / +0,041 [+0,040 ; +0,043] (n = 200) / +0,043 ; mais le probabiliste durci Dg (γ = 6, non conforme à G-N) égale ou dépasse E (E − Dg = −0,004 [−0,0055 ; −0,0025] en P14 ; −0,005 en P15). Aucun vainqueur net ; l'avantage de E est compatible avec un effet de concentration de la cible.
- **Références :** NSGA-II et MOEA/D dépassent tous les bras QGA2-E de 0,12 à 0,13 (P14).
- **Dépendance et ignorance (P15, pilote n = 30) :** la correction de dépendance DA multiplie l'ignorance par environ dix sans effet détectable sur la HV (DA − E = −0,0003 [−0,0024 ; +0,0018]) ; le probabiliste à effectifs corrigés ne gagne rien sur Dp.
- **DEC (P16, phase D, sans HV) :** DEC réduit m̄(Θ) de DA (−0,032 à la génération 150, six scénarios), réduit Dep (0,27 à 0,03) et augmente N_eff, mais augmente aussi la concentration de la cible et le conflit K ; S produit déjà −0,030 ; R2 quasi redondante avec R1 ; HV non lue.
**P17 vise à produire, pour l'article, une comparaison confirmatoire préenregistrée** (hypothèses, marge et effectif fixés avant le calcul) de l'ignorance comme critère de sélection, appariée à son équivalent probabiliste. Les phases P10–P16 sont citées comme travaux préliminaires descriptifs. Aucune revendication de nouveauté avant la recherche RS1 (auteur) ; Salama & Uhde non cités.

## 2. Questions de recherche
- **Q1 (comparaison appariée évidentiel / probabiliste).** À mécanisme de sélection identique, l'évidentiel (DA) fait-il mieux que le probabiliste, y compris contre le probabiliste durci qui reproduit sa concentration ?
- **Q2 (ignorance dans la sélection).** Utiliser l'ignorance comme critère de sélection (4e objectif, pondération, ordre lexicographique) améliore-t-il la HV du problème à 3 objectifs ?
- **Q3 (attribution).** Un éventuel gain vient-il de l'ignorance, ou d'un effet générique (pénalisant quelconque, diversité) ?

## 3. Point de conception central : l'ignorance d'un individu
**Fait établi (preuve à vérifier par test) :** pour une combinaison de Dempster normalisée de supports simples sur des singletons et Θ, Bel({t}) = m({t}) et Pl({t}) = m({t}) + m(Θ) ; l'intervalle [Bel, Pl] d'un singleton a donc la même largeur m_p(Θ) pour toutes les équipes d'un patient. L'ignorance « d'un individu » définie par la largeur d'intervalle de ses choix est donc **la même pour tous les individus** d'une génération (Σ_p m_p(Θ)) : elle ne peut pas discriminer.
**Définition retenue : ignorance marginale d'un individu x** — ignorance moyenne de l'ensemble de sources si x en faisait partie : U_E(x) = (1/n_p) Σ_p m_p^{S∪{x}}(Θ). Forme fermée de premier ordre : m_p^{new} = 1 / (D_p + e^{W_{p,x_p}} (e^{ω α_x(p)} − 1)), avec D_p = 1 + Σ_s (e^{W_s} − 1), W = ω ñ, α_x(p) = 1 / (1 + λ · nb de voisins de x à σ = 0,7 au patient p). Approximation déclarée : l'effet de x sur le rabais α de ses voisins est ignoré ; l'erreur est mesurée contre le calcul exact (test). Coût O(POP × n_p) par génération.
**Équivalent probabiliste :** U_P(x) = entropie moyenne de la cible q^{S∪{x}} (forme linéaire w n_t/N + (1 − w)/K recalculée avec x), pour que le bras probabiliste ait son incertitude naturelle.
**Propriété à documenter :** sous DA, un quasi-doublon ajoute peu d'évidence (α petit) ; U_E favorise donc les individus qui s'accordent avec le consensus tout en étant génotypiquement distincts. Risque : conformisme (copier le consensus minimise U_E) ; contrôlé par §6.

## 4. Mécanismes de sélection (appliqués à la sélection environnementale seulement)
- **SEL4 :** U comme 4e objectif dans le tri non dominé, **sources issues du front sur les 3 objectifs réels** (évite la boucle sources ↔ front). Archive et HV restent sur les 3 objectifs.
- **SELW :** score pondéré sur rangs normalisés dans la population : (1 − λ) rang(fitness agrégée Pareto) + λ rang(U), λ = 0,5 **fixé a priori, non réglé** ; λ ∈ {0,25 ; 0,75} en sensibilité descriptive.
- **SELL :** ordre lexicographique (rang Pareto d'abord, U pour départager à rang et crowding égaux).
- **Variante au niveau de l'ensemble** (sélectionner le sous-ensemble de 40 qui maximise HV − λ·ignorance de l'ensemble, style SMS-EMOA) : écartée en v0.1 pour son coût (environ 10^5 appels HV par run) ; à examiner si SEL4 est concluant.
Implémentation prévue : patch d'exécution de `X.select_next` dans un try/finally (même méthode que `p10.target`), modules gelés non modifiés ; vérification préalable que le tri non dominé et le crowding de `X.nds` / `X.select_next` acceptent un 4e objectif (à lire dans le code, non vérifié ici).

## 5. Bras
**Tier 1 (noyau, répond à Q1–Q3) :** (1) E ; (2) DA ; (3) Dp ; (4) Dg γ = 6 ; (5) DA+SEL4 ; (6) DA+SELW ; (7) Dp+SEL4 (U_P) ; (8) DA+SELR (contrôle : même mécanisme que SEL4 avec un score aléatoire de même loi).
**Tier 2 (si autorisé) :** courbe probabiliste Dg avec γ ∈ {2 ; 4 ; 8 ; 12} (courbe HV contre q_max pour juger E sur son niveau de concentration, sans porte G-N) ; DA+SELL ; Dp+SELW ; DA+S (DEC fixe, contrôle de diversité, issu de P16) ; références NSGA-II, MOEA/D, C0 (P14 gelé) ; DEC adaptatif R1 (phase P de P16, autorisation distincte).
Sans DEC dans Tier 1 pour éviter de confondre ignorance et diversité ; DA+S fournit ce contrôle en Tier 2.

## 6. Contrôles d'attribution (Q3)
SELR (pénalisant aléatoire), DA fitness seule, DA+S (diversité), et le pendant probabiliste. Sont rapportés conjointement : HV, m̄(Θ), K, Dep, N_eff, q_max, q_ent, part de la population dans le premier front à 4 objectifs, taux de remplacement des sources. Alerte conformisme : si le premier front à 4 objectifs dépasse 60 % de la population, la pression de sélection est jugée diluée et le fait est rapporté.

## 7. Hypothèses préenregistrées (propositions à valider, D17-3 et D17-4)
Contrastes primaires, appariés par graine (moyenne des 6 scénarios par graine) :
- **P1 :** DA+SEL4 − DA (HV oracle).
- **P2 :** DA+SEL4 − DA+SELR (attribution à l'ignorance).
- **P3 :** (DA+SEL4 − DA) − (Dp+SEL4 − Dp) (l'ignorance aide-t-elle l'évidentiel plus que l'entropie le probabiliste ?).
Règle : IC95 % percentile corrigé de Bonferroni (trois primaires, niveau 98,33 %), B = 20 000, rééchantillonnage par graine. « Supériorité » si la borne inférieure > 0 ; « équivalence » si l'IC est entièrement dans ±δ (δ = 0,005 proposé, soit environ 1 % de la HV moyenne) ; sinon « non concluant ». Secondaires, descriptifs : SELW, Dg, DA − Dp, E − Dg, trajectoires d'ignorance.
Aucune hypothèse ne prédit un signe sur la HV : une baisse, une absence d'effet et un gain sont des résultats recevables.

## 8. Plan et effectif
SC6 (6 scénarios) × **100 graines (11200–11299)**, budget 6 040 évaluations par run, graines techniques de test 11500–11514. Effectif indicatif : l'écart-type observé des contrastes de HV par graine est d'environ 0,01 (P14) ; pour δ = 0,005 à puissance 80 %, n ≈ 31 ; n = 100 donne de la marge pour trois primaires corrigées. Durée indicative Tier 1 : 8 bras × 600 runs ≈ 4 800 runs ; à 3 à 4 s par run sur 2 cœurs, environ 2,5 à 4 h, surcoût de sélection non mesuré. Les chiffres sont indicatifs, la mesure vient des tests.

## 9. Calibration
Aucun paramètre réglé sur la HV : w = 0,3 hérité de P10 (HV-informé, déclaré), σ = 0,7, λ_dépendance = 1 (axiome P15), λ_sélection = 0,5 (fixé). Pas de calibration préalable, donc aucun risque d'ordre « calibration avant règle ».

## 10. Tests techniques (avant gel, à écrire)
(1) bras sans sélection modifiée = P15 DA / P14 Dp / Dg / E bit à bit ; (2) U_E sous forme fermée = recalcul exact (erreur mesurée et plafonnée) ; (3) constance de la largeur d'intervalle (fait §3) ; (4) sources issues du front à 3 objectifs ; (5) archive et HV sur les 3 objectifs seulement ; (6) budget exact 6 040 ; (7) SELR : score indépendant des génotypes ; (8) aucune fuite du monde oracle dans la recherche ; (9) l'analyse du Tier 1 ne lit la HV qu'après gel et dans un script gelé ; (10) 4e objectif sans NaN ni ex æquo non gérés.

## 11. Interprétation et risques
Un gain de HV ne serait pas attribué à l'ignorance sans passer P2 et le contrôle de diversité. L'ignorance basse signifie un consensus, pas une bonne solution (P16 : l'ignorance baisse quand concentration et conflit montent). Une famille d'instances ; HV oracle contre monde de recherche ; seul le probabiliste a besoin d'un pendant (entropie). La comparaison à NSGA-II et MOEA/D est une référence de contexte, non un test. Nouveauté : attend RS1.

## 12. Autorisation d'exécution (formule prête, pour que le papier avance vite)
Pour lancer en continu Tier 1 (code, tests, gel, exécution, analyse unique, rapport), vous pouvez écrire : « Autorise P17 Tier 1 avec les décisions D17 recommandées, exécution sans arrêt, analyse unique. » Tier 2, DEC adaptatif et toute modification de marge, d'effectif ou de λ nécessitent un message distinct. Rien n'est exécuté avant ce message.

## 13. Décisions D17 (recommandations de Claude)
D17-1 définition de l'ignorance individuelle : ignorance marginale U (§3). D17-2 mécanismes : SEL4 prioritaire, SELW λ = 0,5, SELL en Tier 2. D17-3 contrastes primaires P1–P3. D17-4 marge δ = 0,005 ; niveau 98,33 % ; n = 100. D17-5 Tier 1 comme §5. D17-6 sans DEC en Tier 1. D17-7 courbe Dg en Tier 2 plutôt que porte G-N. D17-8 références NSGA-II/MOEA/D reprises de P14 (non appariées, déclarées) ou rejouées en Tier 2. D17-9 addendum P16 (contraste direct DA+L − DA+S avec IC) : à décider séparément. D17-10 utilisation dans l'article : P10–P16 en « résultats préliminaires descriptifs », P17 en « étude préenregistrée ».

## 14. Règles permanentes
Dépôt GitHub et codes gelés (P3–P5, P7, P10, P11, P14, P15, P16) inchangés ; aucun rerun pour améliorer un résultat ; hypothèses, marges et règles non modifiées après lecture ; chemins absolus ; incidents déclarés ; propositions externes = entrées.
