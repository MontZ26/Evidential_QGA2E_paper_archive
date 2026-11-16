# Protocole P26 v0.1 — Cible probabiliste à exposant variable dans le temps (séparer représentation et calendrier)
Statut : rédigé AVANT toute calibration ou exécution. Autorisation : message de l'auteur du 15 nov. 13:04 (« traiter les dans l'ordre », après l'évaluation externe collée, point D). Fichiers nouveaux ; code gelé P3–P25b inchangé ; dépôt GitHub non touché ; aucune revendication de nouveauté.

## 1. Question
Dans les études précédentes, la cible évidentielle (règle de Dempster) augmente sa concentration au fil des générations selon un calendrier propre, tandis que la cible probabiliste affûtée Dg utilise un exposant constant. La comparaison confond donc la représentation et le calendrier de concentration. P26 compare la cible évidentielle à une cible probabiliste dont l'exposant γ_t varie dans le temps de façon à reproduire la **trajectoire** d'entropie et de q_max de la cible évidentielle (calibration sans HV).

## 2. Cible Dgt
Dp (V0c) élevée à la puissance γ_t, renormalisée, plancher 0,02 ; γ_t = g0 + (g1−g0)·min(1,(g−1)/(Gs−1)) à la génération g. Une rampe constante (g0=g1) coïncide avec Dg (testé au bit près).

## 3. Instances et graines
Famille de P25b (géographies B-X, B-M, B-G, B-L, B-O, B-H ; 50 patients, 10 équipes ; générateur inchangé). Nouvelles graines : calibration 16700–16714 (B-X, B-G, B-O) ; pilote 16900–16909 ; principal 16000–16059 (60 × 6 = 360 tâches). Mêmes fichiers de géographie que P25b mais graines et échantillons de patients nouveaux (non indépendant en géographie de P25b : déclaré).

## 4. Calibration sans HV (une fois)
Forces de source w ∈ {0,3 ; 0,7}. Références : E_w et DA_w (λ=1, σ=0,7). Candidats : g0 ∈ {1 ; 3}, g1 ∈ {6 ; 10 ; 16}, Gs ∈ {30 ; 90} (12 par w). Pour chaque (w, référence) : trajectoires moyennes par génération (g = 1..150) de l'entropie relative et de q_max ; écart d'entropie relatif moyen sur les générations ē, écart moyen |Δq_max| q̄ ; porte : ē ≤ 10 % et q̄ ≤ 0,05 ; sélection : min J = mean_g[(écart relatif d'entropie)²] + mean_g[(Δq_max/0,05)²] parmi les candidats qui passent la porte ; sinon min J (meilleur essai, déclaré). 4 arbres Dgt retenus (w × référence). La vérification sur l'évaluation se fait sans recalibration.

## 5. Bras (12) et contrastes préenregistrés
Bras : E, DA, Dp, Dgt_E, Dgt_DA à w=0,3 et 0,7 ; plus Dg(6) statique à chaque w. Contrastes par w (par graine : moyenne sur 6 géographies de la différence de HV oracle) : L1 E − Dgt_E ; L2 DA − Dgt_DA ; L3 DA − E ; L4 DA − Dp ; L5 DA − Dg(6). IC 99 % marginal, bootstrap B=20000, δ=0,005, ordre de décision usuel ; Bonferroni (m=5 par w) en sensibilité.
## 6. Lecture préenregistrée (conditionnelle à la conformité de trajectoire)
Si la trajectoire de Dgt est conforme (porte vérifiée sur l'évaluation) et que L1 (ou L2) est une équivalence : aucun avantage de la représentation évidentielle au-delà du calendrier de concentration dans ce montage. Si E (ou DA) est supérieur : un avantage de la représentation ou de la dynamique n'est pas expliqué par le calendrier seul. Si Dgt supérieur : un calendrier de concentration probabiliste fait mieux que la règle de Dempster. Non conforme : non interprétable comme séparation ; contrastes rapportés à titre descriptif. Résultats inconclusifs rapportés tels quels.
## 7. Procédure
Tests (passés) → calibration → sélection → pilote → essai à sec → gel → exécution reprenable → précontrôle → une analyse → rapport. Pas de rerun ; pas de changement après résultats ; incidents déclarés.
