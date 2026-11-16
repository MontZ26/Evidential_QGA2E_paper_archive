# P23 v0.1 — Règle graduelle R_ρ contre durcissement probabiliste à concentration appariée (QGA2-E) — CANDIDAT

**Statut : brouillon du 14 novembre 2026, NON lancé.** Aucune exécution, aucune lecture de hypervolume, aucun fichier de code ou de résultats existant modifié. Les décisions D23-1 à D23-8 (§8) attendent la confirmation écrite de l'auteur. Aucune revendication de nouveauté (RS1 non terminée). Théorie : *Ebauche_regle_graduelle_dependance_v0_1.md*.

## 1. Question
Une cible évidentielle dont la concentration est réglée par un degré de dépendance entre sources (R_ρ) fait-elle mieux, aussi bien ou moins bien qu'une cible probabiliste durcie (Dg) quand les deux ont la même concentration ? C'est le contraste central laissé non concluant en P19 (DAgm − Dg = −0,0025, IC 99 % [−0,0057 ; +0,0009]).

## 2. Bras (5, dans QGA2-E, instances SC6)
- **E** : Dempster, ρ = 0 (référence recalculée sur les nouvelles graines).
- **DA** : actualisation par similarité tout ou rien (λ = 1, σ = 0,7), code inchangé.
- **Dg** : cible probabiliste durcie, γ = 6, code inchangé.
- **Rρ** : R_ρ continue, ρ_ij = ρ₀·s_ij pour les paires désignant la même équipe, formule de l'ébauche (§2) ; ρ₀ choisi par la porte de concentration (§5), sans lire d'hypervolume.
- **Rpru** : cas extrême ρ = 1 par équipe (équivalent prudent), contrôle haut de dépendance.
Option (D23-3) : **Rmix**, règle mixte γ·conj + (1 − γ)·prudente, réimplémentation *simplifiée* (γ apparié en concentration, pas l'estimation par regroupement d'origine), à déclarer comme non fidèle.

## 3. Contrastes primaires (famille de 4, IC à 99 %, marge δ = 0,005)
C1 Rρ − Dg ; C2 Rρ − DA ; C3 Rρ − E ; C4 Rpru − E.
Décision (règle de P22) : supériorité si borne inf > 0 ; infériorité si borne sup < 0 ; équivalence si l'IC est dans ±0,005 ; sinon non concluant. HV oracle moyen sur SC6 par graine, bootstrap percentile B = 20 000 avec rééchantillonnage conjoint des graines.
Secondaires (IC 95 %) : Rρ − Rpru, DA − Dg (réplication), par scénario ; diagnostics de concentration (q_max, entropie) par génération ; si D23-3 : Rmix − Dg, Rmix − Rρ.

## 4. Données et graines
SC6 × graines **12000–12099** (n = 100), plage non utilisée dans les études précédentes (à vérifier par un contrôle automatique contre le registre des graines avant le gel). Calibration : SC3 × graines 12700–12714. Tests techniques : 12900–12909. Les références E, DA, Dg ne sont **pas** réutilisées des anciennes plages : tous les bras sont exécutés sur les nouvelles graines.

## 5. Porte de concentration (avant gel, sans lire de HV)
Grille ρ₀ ∈ {0,02 ; 0,05 ; 0,1 ; 0,2}. Un ρ₀ est conforme si, à la génération 150 sur la calibration, l'écart relatif d'entropie moyenne avec Dg est ≤ 10 % et |Δq_max| ≤ 0,05. Parmi les conformes, la règle de sélection de P19 (J(γ)) est appliquée à ρ₀. Si aucun n'est conforme, Rρ est déclarée non conforme : C1 à C3 sont rapportés comme descriptifs, sans décision.

## 6. Portes de tests (avant gel)
T1 ρ = 0 reproduit E à 1e-15 ; T2 DA reproduit par ρ_ij = 1[s_ij ≥ σ] (identité à 1e-15) ; T3 somme des q = 1, valeurs finies ; T4 masse d'ignorance m(Θ) non décroissante en ρ (test sur comptages aléatoires) ; T5 unanimité : q = 1 − (1 − 1/K)(1 − w)^ñ avec ñ = N/(1 + (N − 1)ρ) ; T6 cas limites N = 0, K = 1 ; T7 budget 6 040 exact et archive complète ; T8 non-fuite de l'oracle ; T9 reproductibilité (même graine, même résultat) ; T10 le code existant (P3–P22) est inchangé (hachages).

## 7. Diagnostics de distribution effective (réponse à la revue du 14 nov.)
En plus de la cible q, enregistrer sans effet sur la recherche : fréquences de décodage empiriques par patient (à G = 1, 25, 50, 100, 150), concentration des angles (sin²θ moyen maximum), diversité de la population. Test d'innocuité : mêmes graines, HV identique à 1e-15 avec et sans journalisation. Analyse descriptive : la concentration de la cible est-elle comparable à celle de la distribution effectivement induite, pour Rρ et pour Dg ?

## 8. Décisions à confirmer
D23-1 question et bras ; D23-2 forme continue de ρ_ij (ρ₀·s_ij) ; D23-3 bras Rmix simplifié oui/non ; D23-4 diagnostics de distribution effective (§7) oui/non ; D23-5 NSGA-II guidé en secondaire descriptif (n = 100, mêmes graines) oui/non ; D23-6 graines et familles de contrastes (§3 et §4) ; D23-7 variante de générateur à sources de données corrélées : hors P23, à traiter dans un protocole séparé ; D23-8 ordre : lancer avant ou après RS1 (RS1 ne bloque pas le calcul, mais aucune revendication de nouveauté sans elle).

## 9. Règles constantes
Protocole, code, tests, gel avec hachages avant toute exécution ; analyse unique ; pas de relance pour améliorer ; hypothèses, marges et règles non modifiées après lecture des résultats ; incidents déclarés ; suivi actif pendant le calcul ; dépôt GitHub intact ; code gelé inchangé (nouveaux fichiers uniquement). Durée estimée : environ 5 bras × 600 tâches, environ 2 à 3 h sur 2 cœurs (à mesurer au pilote technique), plus calibration, analyse et rapport.

## 10. Résultats possibles
Si Rρ ≈ Dg (équivalence), un résultat négatif de plus, mais qui répond à l'objection que « la représentation » n'a pas été isolée à concentration égale. Si Rρ > Dg, premier avantage mesuré d'une règle dépendante de la dépendance à concentration égale. Si Rρ < Dg, la règle graduelle n'apporte rien au-delà d'une cible probabiliste durcie. Dans tous les cas, aucune conclusion hors des configurations testées.
