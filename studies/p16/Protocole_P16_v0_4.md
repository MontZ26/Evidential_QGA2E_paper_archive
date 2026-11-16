# Protocole P16 v0.4 — Régulation adaptative de DEC et évolution de l'ignorance
Date : 11 novembre 2026. Base : v0.3 (assistant externe, texte reçu à 04:44) + v0.2-F + cinq remarques de Claude. Les propositions d'autres assistants sont des entrées ; seules les déclarations du Dr Montassar Zaghdoud autorisent une action.

## A. Autorisation et lecture retenue (à corriger si erronée)
Message de l'auteur, 04:46 : « ok pour nouvelle version de P16 avec confirmation des décisions et exécution sans arrêt ». **Lecture retenue :** (i) rédaction de cette v0.4 ; (ii) les décisions D16 sont confirmées telles que recommandées par Claude à 04:44/04:46 (liste en §K) ; (iii) exécution continue, sans arrêt intermédiaire, de **la calibration HV-aveugle des seuils (SC3, graines 11100–11114) puis de la phase D (SC6, graines 11000–11029)**, avec code, tests et gel préalables. **Non autorisés :** phase P, toute lecture de HV, tout confirmatoire, toute modification du dépôt GitHub ou des codes gelés P3–P5, P7, P10, P11, P14, P15. Les D16-4 et D16-5 sont réputées accordées par ce message ; si l'auteur n'avait pas cette intention, il le dit et l'exécution s'arrête.

## B. Principes (de v0.3)
Trois notions distinctes : ignorance m(Θ) ; dépendance génotypique Dep (`dep_stats`, P11) ; dépendance entre sources d'information (hors périmètre, Q-S retirée). DEC modifie aussi la diversité et les réparations : aucune conclusion causale. Comparaisons appariées par graine et scénario ; DA et E calculés sur les mêmes propositions (même premier front, même génération) pour Δm ; intensité nominale ≠ intensité effective ; aucune conclusion sur la HV en phase D.

## C. Questions
Q-D : à intensité DEC fixe forte (L), l'ignorance moyenne m̄(Θ) de DA, Dep, N_eff, concentration (q_max, q_ent) et conflit K changent-ils par rapport à DA sans DEC ? Signe non présupposé. Q-R (phase P, non autorisée) : régulation adaptative R1 vs intensités fixes et calendrier.

## D. Grandeurs (par génération 1–150, moyennes sur les patients modifiables)
m̄_DA(Θ) ; m̄_E(Θ) (Dempster non corrigé sur les mêmes sources) ; Δm = m̄_DA − m̄_E (≥ 0 sur sources identiques : α ≤ 1 ⇒ ñ_t ≤ n_t ⇒ W corrigés ≤ W ⇒ m(Θ)=1/(1+Σ(e^{W_s}−1)) plus grand ; un Δm < 0 serait un incident) ; K = conflit conjonctif non normalisé (champ `m_empty`), pour DA et pour E ; Dep, N_eff, frac_dup, q_max, q_ent ; niveau DEC appliqué, n_max, ρ_max ; compteurs DEC cumulés (cands, cands_repaired, repairs, mutations, violations, regen). Le calendrier de mesure d'un niveau : la valeur de m̄ calculée sur les sources au début de la génération g détermine le niveau appliqué aux enfants de la génération g (équivalent à « valeur de t appliquée à t+1 » pour l'état de fin de génération).

## E. Niveaux DEC (D16-1, D16-7)
σ = 0,7 (identique à DA), r_max = 3. Attributs de la classe `p11.Dec` : `n_max` et `m_max_frac` (nom conceptuel ρ_max). S = (n_max 5 ; ρ_max 0,2) ; L = (2 ; 0,4) ; Fixe-P11 = (2 ; 0,2). Classe Dec non modifiée.

## F. Initialisation (D16-9, D16-12)
Population initiale brute identique pour une graine donnée dans tous les bras. DA sans DEC : aucune réparation. Bras avec DEC : nettoyage initial de `p11._init_clean` au **niveau S** pour tous (fixes comme adaptatifs), puis le niveau du bras s'applique à partir de la génération 1 (premier appel de la cible). L'écart entre bras DEC et DA à la génération 1 est donc l'effet du nettoyage initial et est rapporté comme tel. Calendrier (phase P, non exécuté) : L de la génération 1 à 50, puis S.

## G. Règles de régulation (implémentées et testées, non exécutées)
R1 : L si m̄_DA(Θ) ≥ τ sinon S. R2 : L si Δm ≥ τ_Δ sinon S. R1-inv : inverse de R1. **R2 est évaluée passivement en phase D** (signal calculé sans agir) ; elle n'est un bras de la phase P que si l'accord R1/R2 est faible (D16-3). Seuil unique pour chaque règle (D16-2). Limite : si DEC fort augmente m(Θ), R1 forme une boucle à rétroaction positive.

## H. Règle de calibration des seuils (écrite avant toute exécution, HV-aveugle)
Bras DA sans DEC ; SC3 = {S4-RC101, S4-R101, S4-C101} × graines techniques 11100–11114 (45 runs) ; générations 1 à 150 ; HV non lue. Pour chaque run : médiane sur les générations 1–150 de m̄_DA(Θ) et de Δm ; τ et τ_Δ = médiane de ces 45 médianes. Aucun seuil ajusté après lecture des résultats de la phase D. Limite : seuils calibrés sur SC3, appliqués à SC6 (D16-13 : calibration SC6 non retenue, coût plus élevé ; limite déclarée).

## I. Phase D (autorisée)
Bras : DA, DA+S, DA+L, DA+Fixe-P11. SC6 = 6 scénarios × 30 graines 11000–11029, budget 6 040 évaluations par run, appariement graine×scénario. Mesures aux générations 1, 25, 50, 100, 150 + trajectoires complètes. Contrastes : DA+L − DA, DA+S − DA (et, descriptif, DA+Fixe-P11 − DA) ; unité de rééchantillonnage = graine (moyenne des 6 scénarios par graine, les six restent ensemble) ; moyenne des différences appariées, IC95 % percentile (B = 20 000), distribution par scénario ; compteurs DEC par niveau (intervention effective, violations). Descriptif, aucune p-valeur. Analyse unique, précontrôle, gel vérifié. Le script d'analyse ne lit aucun champ HV ; les HV sont enregistrées dans les fichiers mais **non lues**.
Passif R1/R2 : sur chaque trajectoire, décisions R1 (m̄_DA ≥ τ) et R2 (Δm ≥ τ_Δ) aux générations 1–150 ; part de générations où elles diffèrent ; corrélation de rang des deux signaux ; par bras.
**Règle de décision (avant l'exécution) :** la prémisse « DEC fort réduit l'ignorance moyenne de DA » est étayée si et seulement si, aux générations 50, 100 et 150 simultanément, la borne supérieure de l'IC95 % de m̄(Θ)[DA+L] − m̄(Θ)[DA] est < 0. Sinon elle est non étayée ; la phase P n'est alors pas proposée sans redéfinition. Même si elle est étayée, aucune conclusion sur la dépendance entre sources.

## J. Phase P et confirmatoire : non autorisés ; autorisation écrite distincte, protocole et gel séparés.

## K. Décisions D16 retenues (recommandations de Claude)
D16-1 niveaux S, L, Fixe-P11 comme §E. D16-2 seuil unique. D16-3 R2 passive en phase D. D16-4 calibration autorisée (réputée accordée, §A). D16-5 phase D autorisée (idem). D16-6 bras de la phase P après phase D : DA, DA+S, DA+L, Fixe-P11, R1, R1-inv, Calendrier, E. D16-7 attributs `n_max`, `m_max_frac` vérifiés dans `p11.py`. D16-8 phase P : autorisation séparée. D16-9, D16-12 §F. D16-10 Q-S retirée. D16-11 comparaison DA/E sur mêmes propositions, patients, génération. D16-13 calibration SC3, limite déclarée.

## L. Limites
DEC est un opérateur de diversité (P11 : C1 − C0 = −0,0378 ; Δ_DEC = −0,0048 en P10 ; Δ2 = −0,0040 en P11) ; Dep est génotypique ; Δm n'est pas une mesure causale de redondance ; baisser m(Θ) n'est pas un gain d'optimisation ; l'intensité effective peut différer de la nominale (violations lors d'un passage à n_max = 2 sur une population déjà regroupée) ; calendrier et règle adaptative confondables ; w = 0,3 hérité de P10 (HV-informé, déclaré) ; une famille d'instances ; seuils SC3→SC6 ; nouveauté attend RS1 (auteur).

## M. Règles permanentes
Dépôt GitHub et code gelé inchangés ; aucun rerun pour améliorer un résultat ; aucune hypothèse, règle ou seuil modifié après lecture ; chemins absolus ; incidents consignés ; propositions externes = entrées.
