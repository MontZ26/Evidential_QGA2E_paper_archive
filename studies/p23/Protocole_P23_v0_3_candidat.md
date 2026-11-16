# P23 v0.3 — Degré de dépendance λ dans la règle de Dempster (DA) : comparaison à des cibles probabilistes appariées en concentration dans QGA2-E — CANDIDAT

**Statut : PROTOCOLE CANDIDAT, NON LANCÉ.** Date : 14 novembre 2026. Remplace v0.2 (conservée). Périmètre : QGA2-E, SC6 (S4/S5 × RC101/R101/C101), budget de 6 040 évaluations par run, HV oracle (référence 1,2). Aucune exécution, aucune lecture de HV, aucun fichier existant modifié.
**Autorisation.** Message du Dr Montassar Zaghdoud, 14 nov. 2026, 18:54 : confirmation de la rédaction de v0.3 avec trois choix (dose-réponse descriptive ; Rρ et Rmix exploratoires ; NSGA-II guidé hors de P23) et de corrections rédactionnelles. **Non autorisés :** implémentation, tests, gel, exécution, lecture de HV, modification du dépôt GitHub ou des codes gelés. Les propositions d'autres assistants sont des entrées ; seules les déclarations de l'auteur autorisent une action.
**Aucune revendication de nouveauté** tant que RS1 n'est pas achevée (recherche à exécuter par l'auteur dans Scopus, Web of Science, IEEE Xplore).

## 1. Objectif et questions
P23 vise à déterminer si le paramètre λ de degré de dépendance dans la règle de Dempster de DA (introduit en P15, toujours fixé à 1 jusqu'ici) apporte un avantage de HV, et si cet avantage persiste face à une cible probabiliste durcie dont la concentration est appariée selon des critères préétablis.
- **Q1 (descriptive).** Décrire l'évolution de la HV, de l'entropie et de q_max de la cible, de m̄(Θ) et des diagnostics de distribution effective lorsque λ ∈ {0 ; 0,25 ; 0,5 ; 1}. λ = 0 est Dempster sans correction (E) ; λ = 1 est DA complet. Aucune hypothèse de linéarité ou de monotonie ; aucun test de tendance.
- **Q2 (confirmatoire).** Pour λ ∈ {0,25 ; 0,5 ; 1}, DA(λ) fait-il mieux, aussi bien ou moins bien qu'une cible Dg dont γ est calibré sans HV pour apparier la concentration ? Contraste laissé non concluant en P19 : DAgm − Dg = −0,0025, IC 99 % [−0,0057 ; +0,0009] (non concluant, pas une équivalence).
- **Réplication (distincte de Q2).** C4 : DA(1) − E, effet de la correction de dépendance complète.
**Formulation d'interprétation.** Une différence de HV à concentration appariée serait un indice d'un effet propre à la représentation ; elle ne démontrerait pas que la représentation est l'unique mécanisme. L'appariement porte sur l'entropie et q_max de la cible, pas sur la distribution effective induite par QGA2-E (angles, masques, mesure) : voir §8.

## 2. Bras (9)
| Bras | Description | Statut |
|---|---|---|
| E | Dempster pur, λ = 0 | Référence |
| DA(0,25), DA(0,5), DA(1) | DA, σ = 0,7, w = 0,3, ε = 0,02 | Principaux |
| Dg(γ₀,₂₅), Dg(γ₀,₅), Dg(γ₁) | Dp durci, γ choisi à la calibration pour apparier DA(λ) | Principaux |
| Rρ | Dépendance continue par paire (§2.1) | Exploratoire |
| Rmix | Règle mixte simplifiée (§2.2) | Exploratoire |
Moteur QGA2-E inchangé ; seule la fonction de cible diffère (copie, patch à l'exécution, fichiers gelés intacts). Sources : premier front non dominé, comme en P15. Rρ et Rmix ne contribuent à aucun contraste confirmatoire.

### 2.1 Définition de Rρ (à implémenter ; **aucune spécification gelée n'existe**)
Pour le patient p et la source i (individu du premier front) désignant l'équipe t : α_i(p) = 1/(1 + Σ_{j≠i, x_j(p)=t} ρ_ij), avec ρ_ij = ρ₀·s_ij, s_ij ∈ [0,1] la similarité entre individus définie en P11/P15 (inchangée), **sans seuil σ**. Le comptage effectif ñ_{t,p} = Σ_{i:x_i(p)=t} α_i(p), puis la suite de P15 (poids W = ω·ñ, Dempster sur supports simples, BetP) est inchangée. DA(λ) est le cas ρ_ij = λ·1[s_ij ≥ σ]. ρ₀ ∈ {0,02 ; 0,05 ; 0,1 ; 0,2} est choisi par la porte de §5 (un seul ρ₀, apparié à DA(1)). Limites : ρ_ij continu n'a pas d'axiome d'invariance par duplication à ρ₀ < 1 ; la forme n'est justifiée par aucune référence à ce jour.

### 2.2 Définition de Rmix (**version simplifiée, non fidèle** à Chebbah, Martin, Ben Yaghlane, *Decision Support Systems*, 2015, pp. 37–46, DOI 10.1016/j.dss.2015.02.017)
Cible q_mix = γ_mix·q_E + (1 − γ_mix)·q_caut, où q_E est la cible de E (Dempster) et q_caut la BetP de la combinaison prudente des supports simples : poids W_t = ω·1[c_t ≥ 1] pour toute équipe supportée (poids égaux, minimum des poids de la décomposition canonique), puis Dempster sur ces supports. BetP étant linéaire, le mélange de masses équivaut au mélange des BetP.
Écarts déclarés avec la règle publiée : (i) la partie conjonctive est Dempster normalisée, non la conjonctive non normalisée ; (ii) γ_mix est un scalaire constant choisi dans {0,25 ; 0,5 ; 0,75} par la porte de §5, **non appris** par groupement évidentiel et appariement de groupes ; (iii) la dépendance est fixée, pas mesurée. Rmix n'est donc pas une réplication de leur méthode.

## 3. Contrastes
**Famille confirmatoire (4), IC à 99 %, sans correction supplémentaire, δ = 0,005.**
- C1 DA(0,25) − Dg(γ₀,₂₅) ; C2 DA(0,5) − Dg(γ₀,₅) ; C3 DA(1) − Dg(γ₁) (Q2).
- C4 DA(1) − E (réplication).
Décision : supériorité si borne inf > 0 ; infériorité si borne sup < 0 ; équivalence si l'IC ⊂ [−0,005 ; +0,005] ; sinon non concluant (supériorité et infériorité testées d'abord). Une absence de différence détectée n'est pas une équivalence.
**Exploratoires (IC 95 %, aucune décision) :** DA(0,25) − E, DA(0,5) − E ; DA(λ) − Dg(6) ; Rρ − E, Rρ − DA(1), Rρ − Dg(γ₁) ; Rmix − E, Rmix − Dg(γ₁) ; par scénario ; courbes HV, entropie, q_max, m̄(Θ) en fonction de λ.
**Statistique.** Unité : graine (moyenne sur les six scénarios) ; bootstrap percentile B = 20 000, rééchantillonnage conjoint des graines ; seed du bootstrap fixée. Un seul script d'analyse, une seule exécution.

## 4. Données
SC6 × graines **12000–12099** (n = 100, 600 runs par bras, **5 400 runs**), mêmes graines et instances pour tous les bras, même budget de 6 040 évaluations. Calibration (HV non lue) : SC3 × 12700–12714. Tests techniques : 12900–12909. Contrôle de graines fait à ce jour sur les fichiers de la session (protocoles, scripts, JSON, runs) : aucune graine 12xxx utilisée ; **contrôle automatique contre le registre complet à refaire avant gel**. Aucune HV passée n'est réutilisée. Durée non extrapolée : mesurée au pilote technique.

## 5. Porte de concentration (HV-aveugle, avant gel)
Calibration sur SC3 × 12700–12714, générations 1–150, bras DA(λ), Dg(γ), Rρ(ρ₀), Rmix(γ_mix), sans lecture de HV (le script de calibration ne contient aucun champ HV ; test dédié).
- Dg(γ_λ) : γ ∈ {1 ; 1,25 ; 1,5 ; 2 ; 3 ; 4 ; 6} ; conforme si écart relatif d'entropie moyenne avec DA(λ) ≤ 10 % et |Δq_max| ≤ 0,05 ; sinon meilleur essai, déclaré.
- Rρ : ρ₀ ∈ {0,02 ; 0,05 ; 0,1 ; 0,2}, mêmes critères contre DA(1). Rmix : γ_mix ∈ {0,25 ; 0,5 ; 0,75}, mêmes critères contre DA(1).
Parmi les conformes : plus petit écart d'entropie, puis plus petit |Δq_max|. Aucun γ, ρ₀ ni γ_mix ajusté après lecture de la HV.
**Rapport de conformité sur SC6 (obligatoire pour C1, C2, C3 ; recommandé pour les bras exploratoires) :** entropie moyenne de chaque cible, écart relatif, q_max moyen de chaque cible, écart absolu, statut de conformité aux deux seuils. Si non conforme sur SC6, le contraste reste une comparaison valide entre deux bras mais n'est pas présenté comme un test isolant la représentation à concentration comparable. Aucun réajustement à partir des HV de SC6.

## 6. Portes de tests (avant gel ; tout échec bloque)
T1 λ = 0 reproduit E (égalité bit à bit). T2 λ = 1 reproduit DA de P15/P17. T3 somme des q = 1, valeurs finies et positives. T4 m(Θ) non décroissant en λ (comptages aléatoires). T5 invariance par permutation des sources ; invariance par duplication exacte à λ = 1. T6 cas limites : N = 0, K = 1, une seule équipe supportée. T7 budget exact de 6 040 évaluations, archive complète. T8 non-fuite de l'oracle (l'oracle n'est pas lu par la recherche). T9 reproductibilité (même graine, même résultat). T10 code gelé P3–P22 inchangé (hachages). T11 Rρ : ρ₀ = 0 reproduit E ; ρ_ij = λ·1[s_ij ≥ σ] reproduit DA(λ) ; Rmix : γ_mix = 1 reproduit E, γ_mix = 0 reproduit la cible prudente de forme fermée. T12 le script de calibration ne lit aucun champ HV. T13 la journalisation des diagnostics (§8) ne modifie pas la HV (identique bit à bit avec et sans).

## 7. Gel, exécution et incidents
Ordre : protocole confirmé par l'auteur → code et tests → pilote technique (12900–12909) → calibration → gel avec hachages (protocole, code, paramètres, γ, ρ₀, γ_mix, graines) → exécution des 5 400 runs → précontrôle → analyse unique. Pas de relance pour améliorer un résultat. Hypothèses, marges, règles non modifiées après lecture. Incident = tout écart au protocole, déclaré dans le rapport avec sa cause ; un run échoué technique est relancé à l'identique, pas pour un autre motif. Suivi actif de l'exécution (surveillant en arrière-plan). Dépôt GitHub intact ; nouveaux fichiers seulement.

## 8. Diagnostics de distribution effective (composante centrale de l'analyse)
Journalisés sans effet sur la recherche (T13) : fréquences de décodage empiriques par patient (G = 1, 25, 50, 100, 150), concentration des angles (sin²θ maximum moyen), diversité de la population, Dep, N_eff, frac_dup, m̄(Θ), conflit. Analyse descriptive : la concentration de la cible est-elle comparable à celle de la distribution effectivement induite, pour DA(λ) et pour Dg apparié ? Les résultats de HV sont lus conjointement à ces diagnostics.

## 9. Décisions
Confirmées par l'auteur (18:54) : D23-1 Q1 descriptive, Q2 confirmatoire ; D23-3 Rρ et Rmix exploratoires, définitions à spécifier avant gel (§2.1, §2.2, à confirmer) ; D23-4 famille C1–C4 ; D23-5 diagnostics centraux ; D23-7 NSGA-II guidé hors de P23 ; D23-8 générateur à sources corrélées : protocole séparé.
**Restent à confirmer :** D23-2 grille λ ∈ {0 ; 0,25 ; 0,5 ; 1} (confirmée dans la ligne de décisions, à ratifier ici) ; D23-6 graines (§4) sous réserve du contrôle de registre ; D23-9 ne pas attendre RS1 pour exécuter P23 (aucune revendication de nouveauté avant RS1) ; D23-10 définitions de Rρ (§2.1) et de Rmix (§2.2), grilles de ρ₀ et γ_mix ; D23-11 structure de l'ordre d'exécution (§7).

## 10. Lecture des issues
DA(λ) ≈ Dg apparié : pas d'avantage de représentation démontré dans ces configurations. DA(λ) > Dg apparié : indice d'un effet propre à la représentation à concentration comparable, sous réserve de conformité SC6 et de diagnostics §8. DA(λ) < Dg apparié : la correction de dépendance n'apporte rien au-delà d'une cible probabiliste durcie. Aucune conclusion hors de QGA2-E, des six scénarios SC6 et du budget de 6 040 évaluations.
