# Protocole P16 (v0.1, CONCEPTION SEULE, NON EXÉCUTÉ) — Régulation de l'ignorance par DEC adaptatif liée à la dépendance
Date : 11 novembre 2026. Statut : **brouillon à valider par le Dr Montassar Zaghdoud. Aucun code, aucun calcul, aucune exécution n'est autorisé par ce document.** Le « Oui » de 04:30 autorise l'écriture de ce protocole uniquement.

## 0. Origine et idée de l'auteur
Message de 04:25 : l'objectif n'est pas d'augmenter l'ignorance mais de la réduire. Règles proposées : « si ignorance élevée ou moyenne, la réduire en utilisant DEC à grand pas ; si ignorance faible, DEC à petit pas ; chercher une règle en liaison avec la réduction de la dépendance (on suppose que réduire la dépendance permet de réduire l'ignorance) ». Cohérent avec le sens A (« plus de dépendance, plus d'ignorance ») confirmé à 23:58.

## 1. Questions de recherche
- **Q-D (diagnostic) :** à propositions de sources non fixées, DEC fort réduit-il l'ignorance m(Θ) de DA (réduction de dépendance → réduction d'ignorance) ? Deux effets s'opposent : (a) moins de redondance, donc moins de pénalité α et ñ plus grand, donc m(Θ) plus petit ; (b) moins d'accord entre sources sur un patient, donc moins de soutien cumulé et m(Θ) plus grand (cf. V2, m(Θ) ≈ 0,23 avec des sources diverses). Le signe net est **empirique** ; les deux signes sont informatifs.
- **Q-R (régulation) :** une règle qui fait varier l'intensité de DEC selon l'ignorance (R1) ou selon l'ignorance attribuable à la dépendance (R2) modifie-t-elle la trajectoire de m(Θ), de la dépendance, du conflit, de la concentration et de la HV, par rapport à DEC fixe ?

## 2. Grandeurs mesurées (par génération, déjà disponibles dans DIAG de P15 sauf mention)
m̄(Θ) = moyenne sur les patients de m(Θ) de la cible DA ; m̄_E(Θ) = valeur Dempster non corrigée sur les mêmes sources ; Δm = m̄_DA(Θ) − m̄_E(Θ) (**ignorance attribuable à la dépendance**) ; conflit m(∅) ; dép (Dep), N_eff, frac_dup ; q_max, q_ent ; intensité de DEC choisie ; compteurs DEC (repairs, mutations, violations, cands_repaired, regen, ls_skipped) ; évaluations consommées. La HV finale est enregistrée mais **non lue** en phase D.

## 3. Intensités de DEC (le « pas »)
DEC (p11.Dec) n'a pas de pas continu ; son intensité dépend de n_max (plafond de voisins, plus petit = plus fort) et ρ_max (fraction maximale de patients modifiés par réparation). σ = 0,7 fixé (identique à DA), r_max = 3.
- **Petit pas S :** n_max = 5, ρ_max = 0,2.
- **Grand pas L :** n_max = 2, ρ_max = 0,4.
- Référence P11 déjà calibrée (HV-aveugle) : (n_max = 2, ρ_max = 0,2), bras « Fixe-P11 ».
Le contrôleur ne change que les attributs n_max et m_max_frac de l'objet Dec entre deux générations ; la classe Dec n'est pas modifiée. Le changement s'applique aux candidats de la génération suivante (règle causale, valeur de la génération précédente).

## 4. Règles de régulation
- **R1 (règle de l'auteur) :** si m̄(Θ) ≥ τ (ignorance moyenne ou élevée) alors L, sinon S.
- **R2 (liée à la dépendance, proposition de Claude) :** si Δm ≥ τ_Δ alors L, sinon S. DEC n'agit alors que sur l'ignorance réductible par diminution de la redondance, pas sur l'ignorance de fond.
- **R1-inv (contrôle négatif) :** affectation inversée de R1 (S si m̄(Θ) ≥ τ, L sinon), pour tester si le sens de la règle compte.
- Seuils τ, τ_Δ : fixés **avant toute exécution du pilote de régulation, sans HV**, par une règle écrite : médiane (sur générations et runs) de m̄(Θ), respectivement de Δm, observée pour DA sans DEC sur une calibration SC3 × graines techniques 11100–11114 (HV non calculée ni lue). Cette calibration exige une **autorisation écrite séparée**. Le seuil unique résume vos trois niveaux (élevé/moyen → grand pas, faible → petit pas) ; un seuil à deux niveaux est possible sur demande.
- Pas d'hystérésis ; aucun lissage ; évaluation à chaque génération (déclaré).
- Nota : pour E, m(Θ) ≈ 0,002 ; R1 sans correction de dépendance serait presque toujours en régime « faible ». R1 et R2 sont donc définies sur le bras DA.

## 5. Bras
E (Dempster, référence P10/P14/P15) ; DA (sans DEC, = P15) ; DA+S fixe ; DA+L fixe ; DA+Fixe-P11 ; DA+R1 ; DA+R2 ; DA+R1-inv. Contrôle de calendrier (L puis S selon la proportion d'usage de L par R1/R2) : à définir en phase P avec les proportions observées, sans lecture de la HV.

## 6. Phases
- **Phase D (diagnostic HV-aveugle, descriptif) :** bras DA, DA+S, DA+L, DA+Fixe-P11 ; SC6 × 30 graines (11000–11029) ; budget 6 040. Lecture : m̄(Θ) aux générations 1/25/50/100/150, Δm, conflit, Dep, N_eff, q_max ; contrastes DA+L − DA et DA+S − DA, moyenne [IC95 % bootstrap, B = 20 000], sans p-valeur. Le script d'analyse ne lit aucun champ HV.
- **Règle de décision écrite avant la phase D :** si, à partir de la génération 50, la borne supérieure de l'IC95 % du contraste m̄(Θ)[DA+L] − m̄(Θ)[DA] est < 0, la prémisse « réduire la dépendance par DEC réduit l'ignorance » est étayée et la phase P peut être proposée ; si l'IC contient 0 ou est > 0, la prémisse n'est pas étayée dans ce montage, R1 et R2 sont déclarées non pertinentes en l'état et la phase P n'est pas proposée sans redéfinition.
- **Phase P (pilote de régulation, descriptif) :** bras du §5 ; seuils §4 ; graines à fixer ; HV lue seulement à ce stade ; **séparée, avec autorisation écrite, règle de calibration des seuils et gel avant exécution.**
- **Phase confirmatoire :** hors périmètre ; exige une marge d'équivalence et un dimensionnement fixés avant tout calcul, un nouveau protocole et une autorisation écrite.

## 7. Hypothèses (descriptives)
HD1 : DA+L a un m̄(Θ) inférieur à DA (sens A). HD2 : DA+L a Dep plus bas et N_eff plus haut que DA. HD3 : effet sur conflit et q_max, sans signe prédit. HP1 (phase P) : R1 et R2 donnent un m̄(Θ) plus bas que DA+S et plus haut que DA+L, par construction ; l'effet sur la HV n'est pas prédit.

## 8. Implémentation prévue (après autorisation, non faite)
Module p16.py importe p10/p11/p15 sans les modifier ; contrôleur appelé à chaque génération. Tests prévus : (i) contrôleur inactif = P15 DA bit à bit ; (ii) niveau fixe via contrôleur = DEC fixe de p11 ; (iii) évaluations ≤ 6 040 ; (iv) les attributs ne changent qu'entre générations ; (v) R1 et R2 sélectionnent le niveau attendu sur des valeurs synthétiques ; (vi) le script d'analyse de la phase D ne lit pas la HV. Gel du code et analyse unique avant toute lecture de résultats.

## 9. Limites déclarées
DEC est aussi un opérateur de diversité (P11 : C1 − C0 = −0,0378 ; Δ_DEC = −0,0048 en P10, Δ2 = −0,0040 en P11) : un effet sur la HV ne s'attribuerait pas à la seule dépendance. Réduire m(Θ) n'est pas en soi un gain d'optimisation ; la concentration (q_max 0,86 pour E) et le conflit (0,8 à 0,9) restent les phénomènes dominants. Une règle adaptative peut imiter un simple calendrier. w = 0,3 est hérité de P10 (choisi sur HV, déclaré). Une famille d'instances. Toute revendication de nouveauté attend RS1 (recherche Scopus/WoS/IEEE de l'auteur).

## 10. Décisions à trancher par l'auteur
D16-1 : définition des deux pas (S = (5 ; 0,2), L = (2 ; 0,4)) ou autre grille. D16-2 : seuil unique ou deux seuils. D16-3 : R2 retenue ou non. D16-4 : autorisation de la calibration des seuils (SC3, 11100–11114, sans HV). D16-5 : autorisation de la phase D (SC6 × 30 graines 11000–11029). D16-6 : liste des bras.

## 11. Règles permanentes appliquées
Dépôt GitHub et code gelé (P3–P5, P7, P10, P11, P14, P15) inchangés ; aucun rerun pour améliorer un résultat ; aucune hypothèse ni aucun seuil modifié après lecture des résultats ; chemins absolus ; incidents déclarés ; les textes d'autres assistants sont des entrées, seules vos déclarations autorisent.
