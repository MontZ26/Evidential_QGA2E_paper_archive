# Protocole P25 v0.1 — Évaluation indépendante (nouvelle famille d'instances)
Statut : candidat, rédigé AVANT toute calibration/exécution ; autorisation de lancer : message de l'auteur du 15 nov. 06:56 (« préparer un protocole et le lancer sans arrêt »). Fichiers nouveaux uniquement ; code gelé P3–P24 inchangé ; dépôt GitHub non touché.

## 1. Question
Les conclusions de P23/P24 (E, Dp, DA, Dg ; effet de concentration, degré de dépendance w) tiennent-elles sur une famille d'instances **non utilisée** pour les décisions ? Ce n'est pas une réplication sur mêmes graines ; aucune revendication de nouveauté.

## 2. Famille d'instances (fixée avant calcul)
- Géographies synthétiques de type Solomon, générées par graine (p25.gen_points) : U (uniforme), K (8 grappes, σ=5), M (mixte). Dépôt fixe. Fenêtres/durées : paramètres des familles R101 (U), C101 (K), RC101 (M).
- Tailles : V6 = 40 patients/9 équipes ; V7 = 70/12 (P24 : 40–70 patients selon scénarios, mais autres géographies).
- Scénarios : V6-U, V7-U, V6-K, V7-K, V6-M, V7-M (« SC6-P25 »). Reste du générateur (vérité cachée, sources d'évidence, fiabilités 0,95/0,80/1,0, S_true) inchangé.
- Graines : calibration 14700–14714 (SC3 = V6-U, V6-K, V6-M) ; pilote 14900–14909 ; principal 14000–14059 (60 graines × 6 scénarios = 360 tâches). Allowlist étendue (nouveaux blocs ; anciens inclus) ; aucune graine ne chevauche les registres antérieurs.
- Budget 40+150×40 = 6040 évaluations ; HV oracle, réf. 1,2 ; moteur = P24 (run_arm24), non modifié.

## 3. Bras
Pour w ∈ {0,3 ; 0,7} : E, Dp, DA(λ=1,σ=0,7), Dg(γ_cal(w)) ; plus Dg(6) à w=0,3. Soit 9 bras uniques. γ_cal(w) choisi **sans HV** sur calibration par la règle P24 (grille γ ∈ {1 ; 1,5 ; 2 ; 3 ; 4 ; 6 ; 8 ; 10 ; 12 ; 16} (virgule = décimale) ; porte : écart relatif d'entropie ≤10 % et |Δq_max| ≤0,05 sur moyennes générations 1–150 ; sélection : écart d'entropie min puis |Δq| ; sinon J min, déclaré). Vérification d'appariement sur les six scénarios principaux sans recalibration ; non conformes signalés.

## 4. Contrastes préenregistrés (par graine : moyenne sur 6 scénarios ; différence de HV)
Pour chaque w : K1 DA−E ; K2 DA−Dg_cal ; K3 Dg_cal−E ; K4 DA−Dp. Plus K5 DA−Dg(6) à w=0,3. Bootstrap percentile apparié B=20000 sur graines, IC marginal 99 %, δ=0,005 ; ordre de décision : supériorité (IC>0 et… borne basse > 0), infériorité, équivalence (IC ⊂ [−δ,δ]), sinon non concluant. Sensibilité : Bonferroni par sous-famille. Secondaire : par scénario, par taille, par géographie ; JS/L1 des distributions effectives (npz). Lecture seule des contrastes non appariés : non interprétables.
Critère de cohérence avec P24 (descriptif, pas de test supplémentaire) : même direction et même classe pratique que le contraste P24 correspondant.

## 5. Procédure
Tests unitaires → calibration (HV-aveugle, une fois) → sélection (une fois) → pilote (temps) → essai à sec de l'analyse sur données synthétiques → gel (hash) → exécution reprenable sous surveillance active → précontrôle d'intégrité → **une** analyse → rapport. Aucun rerun pour améliorer ; aucun changement d'hypothèse/marge/règle après résultats ; incidents déclarés. Les étapes aveugles ne lisent pas le HV.
