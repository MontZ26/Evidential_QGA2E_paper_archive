# P23 v0.2 — Paramètre de degré de dépendance λ dans la règle de Dempster (DA) : balayage et comparaison à concentration appariée — CANDIDAT

**Statut : brouillon du 14 novembre 2026, NON lancé.** Remplace v0.1 (conservée). Aucune exécution, aucune lecture de HV, aucun fichier existant modifié. Décisions D23-1 à D23-9 (§9) à confirmer par écrit. Aucune revendication de nouveauté (RS1 non terminée).

## 0. Origine et lecture retenue (à corriger si erronée)
Suggestion de l'auteur (rappelée le 14 nov., 18:33) : introduire dans la règle de Dempster un paramètre facteur de degré de dépendance. Il existe déjà : λ dans DA (P15 ; α_i = 1/(1+λ(g_i−1)) ; λ = 0 redonne Dempster bit à bit, test unitaire P15), mais λ n'a jamais été varié (fixé à 1 par axiome d'invariance par duplication). P23 étudie donc λ comme paramètre graduel. Accord de l'auteur sur ce recadrage : message du 14 nov., 18:35 (« Ok je suis d'accord, je vous attends »), qui autorise la rédaction de cette v0.2 seulement, pas l'exécution.

## 1. Questions
Q1 (dose-réponse) : comment la HV oracle et la concentration de la cible évoluent-elles quand λ passe de 0 (E) à 1 (DA) ?
Q2 (représentation à concentration égale) : pour chaque λ, DA(λ) fait-il mieux, aussi bien ou moins bien qu'une cible probabiliste durcie Dg dont γ est calibré (sans HV) pour apparier sa concentration ? (Contraste laissé non concluant en P19 : DAgm − Dg = −0,0025 [−0,0057 ; +0,0009].)

## 2. Bras (QGA2-E inchangé ; seule la cible change ; SC6 = S4/S5 × RC101/R101/C101)
- E = DA(λ=0). Référence recalculée sur les nouvelles graines.
- DA(0,25), DA(0,5), DA(1) : σ = 0,7, w = 0,3, ε = 0,02 inchangés.
- Dg(γ₀,₂₅), Dg(γ₀,₅), Dg(γ₁) : cible probabiliste durcie, un γ par λ choisi à la calibration (§5).
- Secondaires (descriptifs, D23-3) : Rρ (forme continue ρ_ij = ρ₀·s_ij, ρ₀ choisi par la porte §5) et Rmix (règle mixte de Chebbah et al., réimplémentation **simplifiée** : γ_mix apparié en concentration, sans leur estimation par groupement ; déclarée non fidèle). Référence : Chebbah, Martin, Ben Yaghlane, Decision Support Systems, 2015, pp. 37–46, DOI 10.1016/j.dss.2015.02.017.

## 3. Contrastes primaires (famille de 4, IC 99 %, marge δ = 0,005)
C1 DA(0,25) − Dg(γ₀,₂₅) ; C2 DA(0,5) − Dg(γ₀,₅) ; C3 DA(1) − Dg(γ₁) ; C4 DA(1) − E (réplication).
Décision : supériorité si borne inf > 0 ; infériorité si borne sup < 0 ; équivalence si l'IC ⊂ [−0,005 ; +0,005] ; sinon non concluant (supériorité et infériorité testées d'abord). Unité : graine (moyenne sur les six scénarios), bootstrap percentile B = 20 000.
Secondaires (IC 95 %) : DA(λ) − E pour chaque λ (courbe dose-réponse, descriptive) ; DA(λ) − Dg(6) ; par scénario ; Rρ et Rmix − Dg apparié, − E ; diagnostics q_max, entropie, m̄(Θ), Dep, N_eff par génération.

## 4. Données
SC6 × graines 12000–12099 (n = 100) ; calibration SC3 × 12700–12714 ; tests techniques 12900–12909. Plages 12xxx à vérifier automatiquement contre le registre des graines avant gel (vérifiées seulement dans les fichiers de protocole à ce jour). Tous les bras sont exécutés sur les nouvelles graines (aucune réutilisation de HV passées). Budget 6 040 évaluations par run. Environ 8 bras × 600 tâches ; durée à mesurer au pilote technique.

## 5. Porte de concentration (HV-aveugle, avant gel)
Pour chaque λ ∈ {0,25 ; 0,5 ; 1}, sur la calibration SC3 × 12700–12714, au sens de P19 : grille γ ∈ {1 ; 1,25 ; 1,5 ; 2 ; 3 ; 4 ; 6} ; γ_λ conforme si l'écart relatif d'entropie moyenne avec DA(λ) est ≤ 10 % et |Δq_max| ≤ 0,05 ; sinon meilleur essai, déclaré. Même procédure pour ρ₀ ∈ {0,02 ; 0,05 ; 0,1 ; 0,2} (Rρ). Un contraste dont l'appariement n'est pas conforme sur SC6 (vérification descriptive) reste valide mais n'isole pas l'effet de représentation. Aucun γ ni ρ₀ ajusté après lecture de la HV.

## 6. Portes de tests (avant gel)
T1 λ = 0 reproduit E (égalité bit à bit) ; T2 λ = 1 reproduit DA de P15/P17 ; T3 somme des q = 1, valeurs finies ; T4 m(Θ) non décroissant en λ (comptages aléatoires) ; T5 invariance par permutation et par duplication exacte à λ = 1 ; T6 cas limites N = 0, K = 1 ; T7 budget exact, archive complète ; T8 non-fuite de l'oracle ; T9 reproductibilité ; T10 code gelé (P3–P22) inchangé (hachages) ; T11 Rρ : ρ₀ = 0 reproduit E, ρ_ij binaire reproduit DA.

## 7. Diagnostics de distribution effective (D23-5)
Journalisation sans effet sur la recherche : fréquences de décodage empiriques par patient (G = 1, 25, 50, 100, 150), concentration des angles, diversité. Test d'innocuité : HV identique avec et sans journalisation. Objectif : comparer la concentration de la cible à celle de la distribution effectivement induite (objection de la revue externe).

## 8. Règles constantes
Protocole, code, tests, gel avec hachages avant exécution ; analyse unique ; pas de relance pour améliorer ; hypothèses, marges, règles non modifiées après lecture des résultats ; incidents déclarés ; suivi actif pendant le calcul ; dépôt GitHub intact ; nouveaux fichiers seulement.

## 9. Décisions à confirmer
D23-1 questions Q1 et Q2 ; D23-2 grille λ ∈ {0 ; 0,25 ; 0,5 ; 1} ; D23-3 bras secondaires Rρ et Rmix oui/non ; D23-4 famille C1–C4 ; D23-5 diagnostics de distribution effective ; D23-6 graines (§4) ; D23-7 NSGA-II guidé en secondaire descriptif oui/non ; D23-8 générateur à sources corrélées : protocole séparé ; D23-9 ordre par rapport à RS1.

## 10. Lecture des issues
DA(λ) ≈ Dg apparié : pas d'avantage de représentation démontré dans ces configurations. DA(λ) > Dg apparié : premier avantage mesuré à concentration égale. DA(λ) < Dg apparié : la correction de dépendance n'apporte rien au-delà d'une cible probabiliste durcie. Dans tous les cas, aucune conclusion hors des configurations testées.
