# Protocole P16 v0.2-F (fusion) — Régulation adaptative de DEC et évolution de l'ignorance
*Texte de la v0.2 proposée par un assistant externe, révisé par Claude (v0.1 de Claude intégrée). Entrée méthodologique : seules les déclarations du Dr Montassar Zaghdoud autorisent une action.*

**Date :** 11 novembre 2026  
**Statut :** brouillon méthodologique — conception seulement, non gelé, non exécuté.  
**Autorisation actuelle :** rédaction et révision du protocole uniquement. Aucun code, calcul, calibration, pilote ou expérimentation n'est autorisé.

## Journal des modifications de la fusion (v0.2-F)
Repris de la v0.2 externe : trois notions de dépendance distinctes ; Δm renommé « différence d'ignorance DA–E » ; seuils en deux étapes (médiane par run puis entre runs) ; contrôle DA+Calendrier ; rééchantillonnage par graine ; conclusions limitées aux effets mesurés.
Ajouté ou corrigé par Claude : (1) Δm ≥ 0 par construction sur des sources identiques (le texte externe le disait signé) ; (2) la quantité enregistrée « conflit m(∅) » est le conflit conjonctif non normalisé K, nommé ainsi désormais ; (3) niveau initial de DEC à la génération 1 non défini dans la v0.2, ajouté ; (4) Q-S retirée des questions expérimentales (aucune provenance dans le moteur) ; (5) règle de décision de la phase D précisée aux points de contrôle 50, 100, 150 ; (6) risque de violations massives lors d'un passage à L sur une population déjà regroupée ; (7) Dep est défini par `dep_stats` de P11 (non par P15) ; (8) tests et décisions D16-9 et D16-10 ajoutés.

## 0. Objet et modifications par rapport à v0.1

L'objectif est d'étudier si une régulation adaptative de l'intensité de DEC peut modifier l'ignorance de la fonction de croyance DA, et si cette évolution est associée aux propriétés de la population de recherche.

Le protocole distingue désormais explicitement trois notions :

1. **Ignorance de l'évidence :** masse \(m(\Theta)\).
2. **Dépendance génotypique de la population :** indicateur `Dep` défini par `dep_stats` (module P11) et enregistré dans les traces P14.
3. **Dépendance entre sources d'information :** dépendance liée à la provenance et aux données communes des sources documentaires, historiques et supervisées.

Ces notions ne sont pas interchangeables. En particulier, `Dep` ne constitue pas une mesure directe de la dépendance entre sources d'information.

DEC agit sur le processus de recherche et de réparation des affectations. Une modification de `Dep` ou de \(m(\Theta)\) après son intervention ne suffira pas, à elle seule, à démontrer un mécanisme causal entre dépendance et ignorance.

Les résultats seront interprétés comme des effets de DEC sur les indicateurs observés, sauf démonstration supplémentaire du mécanisme.

## 1. Questions de recherche

### Q-D — Diagnostic

Une intensité DEC forte modifie-t-elle, par rapport à DA sans DEC :

- l'ignorance moyenne \(\bar m(\Theta)\) ;
- la dépendance génotypique `Dep` ;
- la diversité effective \(N_{\mathrm{eff}}\) ;
- la concentration de la cible d'échantillonnage ;
- le conflit entre les propositions des sources ?

Deux résultats sont possibles :

- une diminution de l'ignorance, éventuellement associée à une diminution de `Dep` ;
- une augmentation ou une absence de diminution de l'ignorance, notamment si les réparations modifient les propositions ou leur concordance.

Le signe de l'effet est empirique et n'est pas présupposé.

### Q-R — Régulation adaptative

Une régulation de DEC fondée sur :

- l'ignorance moyenne de DA (R1) ;
- la différence d'ignorance entre DA et le calcul Dempster de référence (R2) ;

modifie-t-elle les trajectoires de l'ignorance, des indicateurs de population, du conflit et de la qualité finale des affectations, par rapport à DEC fixe et à un calendrier non adaptatif d'intensité comparable ?

### Q-S — retirée des questions expérimentales (Claude)
La cohérence avec la provenance et les redondances documentaires ne peut pas être testée dans ce moteur : les « sources » y sont des individus du premier front, sans provenance ni données communes. Les masses de croyance seules n'identifient pas un coefficient universel de dépendance entre sources. Un indicateur fondé sur la provenance et les erreurs communes serait une question de recherche distincte (cadre P8 externe).

## 2. Grandeurs mesurées et définitions

Les diagnostics sont enregistrés par génération.

### 2.1. Ignorance

\[
\bar m_{DA}(\Theta)
=\frac{1}{N_p}\sum_i m_{DA,i}(\Theta)
\]

où \(N_p\) est le nombre de patients considérés.

### 2.2. Référence Dempster

\[
\bar m_E(\Theta)
=\frac{1}{N_p}\sum_i m_{E,i}(\Theta)
\]

Le calcul E utilise les mêmes sources et les mêmes données d'entrée que DA, sans correction DEC, afin de permettre une comparaison appariée.

### 2.3. Différence d'ignorance

\[
\Delta m
=\bar m_{DA}(\Theta)-\bar m_E(\Theta)
\]

Cette variable est nommée **différence d'ignorance DA–E**.

Elle ne sera plus appelée directement « ignorance attribuable à la dépendance », car cette attribution causale n'est pas établie par la différence de deux masses.

- \(\Delta m>0\) : DA conserve davantage d'ignorance que E.
- \(\Delta m=0\) : les deux traitements ont la même ignorance moyenne.
- \(\Delta m<0\) : DA conserve moins d'ignorance que E.

**Propriété (Claude).** Calculés sur les mêmes sources, les poids corrigés de DA sont inférieurs ou égaux à ceux de E (1 ≤ ñ_t ≤ n_t), donc m_DA(Θ) ≥ m_E(Θ) patient par patient et Δm ≥ 0 (au bruit numérique près ; vérifié par test unitaire en P15, 60 jeux de sources). Les lignes « Δm = 0 » et « Δm < 0 » ci-dessus décrivent donc des cas qui ne devraient pas se produire ; un Δm < 0 observé signalerait une erreur de calcul ou des sources non identiques, et serait rapporté comme incident. Δm n'est ni tronqué ni transformé en valeur absolue.

### 2.4. Dépendance et diversité de la population

Les diagnostics comprennent :

- `Dep` : dépendance génotypique de la population ;
- \(N_{\mathrm{eff}}\) ;
- `frac_dup` ;
- `q_max` ;
- `q_ent` ;
- similarité moyenne ;
- taille du premier front et \(N_{\mathrm{eff}}\) de ses sources.

Ces variables décrivent la dynamique de recherche. Elles ne constituent pas, isolément, des mesures de dépendance statistique entre les sources d'information.

### 2.5. Conflit

Le conflit doit être distingué de l'ignorance.

Le rapport précisera si le champ enregistré correspond :

- au conflit conjonctif non normalisé \(K\) avant normalisation ;
- à une masse résiduelle sur l'ensemble vide ;
- ou à une autre quantité issue de l'implémentation.

Pour la règle de Dempster normalisée, lorsque la normalisation est définie, la masse finale sur l'ensemble vide est nulle. Le protocole ne doit donc pas assimiler automatiquement \(m(\varnothing)\) final et conflit \(K\).

**Précision (Claude) :** le champ enregistré par P7/P15 sous le nom `m_empty` est le conflit conjonctif non normalisé K = 1 − e^{−W}(1 + Σ_s (e^{W_s} − 1)) (forme fermée avant normalisation). Il sera désormais noté K. Les valeurs « conflit m(∅) » du rapport P15 (E 0,79–0,90 ; DA 0,79–0,90 ; V2 0,32–0,41) sont des valeurs de K ; erratum de dénomination à ajouter au rapport sans changer les chiffres.

### 2.6. Diagnostics DEC

Enregistrer :

- intensité choisie ;
- `n_max` ;
- paramètre de fraction maximale de patients modifiés ;
- réparations ;
- mutations ;
- violations ;
- candidats réparés ;
- régénérations ;
- recherches locales ignorées ;
- évaluations consommées.

Les noms exacts des attributs de l'API DEC devront être vérifiés avant toute implémentation. Le protocole distingue le nom conceptuel \(\rho_{\max}\) du nom d'attribut effectivement utilisé dans le code.

La HV finale est enregistrée, mais reste inaccessible à l'analyse de la phase D.

## 3. Intensités de DEC

Le paramètre \(\sigma=0,7\) est maintenu, ainsi que \(r_{\max}=3\), conformément à v0.1.

Deux intensités sont proposées :

| Niveau | \(n_{\max}\) | \(\rho_{\max}\) | Interprétation |
|---|---:|---:|---|
| S — petit pas | 5 | 0,2 | Intervention plus limitée |
| L — grand pas | 2 | 0,4 | Intervention plus forte |

Référence fixe P11 :

| Niveau | \(n_{\max}\) | \(\rho_{\max}\) |
|---|---:|---:|
| Fixe-P11 | 2 | 0,2 |

La relation entre \(n_{\max}\) et l'intensité est celle déclarée dans le protocole P16 : un plafond de voisins plus faible correspond à une intervention plus forte.

Le contrôleur ne modifie que les paramètres DEC entre deux générations. La valeur calculée à la génération \(t\) s'applique aux candidats de la génération \(t+1\).

**Niveau initial (Claude) :** la population initiale est nettoyée par DEC avant toute mesure de m(Θ) ; le niveau à la génération 1 doit donc être fixé à l'avance. Proposition : niveau S pour tous les bras adaptatifs et pour le calendrier, afin que le démarrage soit identique (à confirmer, D16-9).

Aucune modification de la classe DEC n'est prévue.

## 4. Règles de régulation

### R1 — Régulation selon l'ignorance

\[
R1(t)=
\begin{cases}
L & \text{si }\bar m_{DA,t}(\Theta)\geq\tau\\
S & \text{sinon}
\end{cases}
\]

Cette règle traduit l'hypothèse de l'auteur : lorsque l'ignorance est moyenne ou élevée, DEC applique un grand pas ; lorsque l'ignorance est faible, il applique un petit pas.

Avec un seuil unique, la règle distingue deux régimes, et non trois niveaux indépendants.

### R2 — Régulation selon la différence d'ignorance DA–E

\[
R2(t)=
\begin{cases}
L & \text{si }\Delta m_t\geq\tau_\Delta\\
S & \text{sinon}
\end{cases}
\]

R2 régule DEC selon l'écart d'ignorance observé entre DA et E. Comme Δm ≥ 0, le seuil τ_Δ porte sur une grandeur positive ; R2 se rapproche de R1 quand m_E(Θ) ≈ 0 (cas de E en fin de run, 0,002).

**R2 ne sera pas présentée comme une mesure directe de la dépendance entre sources.** Elle teste si une différence d'ignorance entre les deux traitements constitue un signal utile pour adapter DEC.

### R1-inv — Contrôle négatif

\[
R1_{\mathrm{inv}}(t)=
\begin{cases}
S & \text{si }\bar m_{DA,t}(\Theta)\geq\tau\\
L & \text{sinon}
\end{cases}
\]

Cette règle permet d'examiner si le sens de la régulation influence les résultats.

### Détermination des seuils

Les seuils sont déterminés avant la phase D et avant toute lecture de HV.

Calibration proposée :

- bras DA sans DEC ;
- scénario SC3 ;
- graines techniques 11100–11114 ;
- générations 1 à 150 ;
- aucune HV calculée ou consultée.

Pour éviter de traiter les générations d'un même run comme des observations indépendantes, le calcul sera effectué en deux étapes :

1. médiane des générations 1 à 150 pour chaque run ;
2. médiane des médianes obtenues sur les runs de calibration.

Le même principe est appliqué séparément à \(\bar m_{DA}(\Theta)\) et \(\Delta m\).

Cette procédure produit un seuil unique pour R1 et un seuil unique pour R2.

Aucune valeur de seuil ne sera ajustée après lecture des résultats.

La calibration requiert une autorisation écrite distincte.

## 5. Bras expérimentaux

Les bras proposés sont :

| Bras | Configuration | Rôle |
|---|---|---|
| E | Dempster | Référence de combinaison |
| DA | DA sans DEC | Référence principale |
| DA+S | DEC fixe, petit pas | Contrôle intensité faible |
| DA+L | DEC fixe, grand pas | Contrôle intensité forte |
| DA+Fixe-P11 | DEC fixe P11 | Référence calibrée antérieure |
| DA+R1 | DEC adaptatif selon ignorance | Règle de l'auteur |
| DA+R2 | DEC adaptatif selon différence DA–E | Règle alternative |
| DA+R1-inv | Règle inversée | Contrôle négatif |
| DA+Calendrier | Alternance S/L non adaptative | Contrôle de calendrier |

### Contrôle de calendrier

DA+Calendrier utilise les mêmes intensités S et L que la règle adaptative de référence, mais leur ordre ne dépend pas de l'ignorance.

Le calendrier devra être défini dans le protocole de la phase P et gelé avant toute exécution de cette phase (non après lecture de résultats). Calendrier proposé : L de la génération 1 à 50, puis S, indépendant de l'ignorance ; une variante à exposition égale décrite ci-dessous reste descriptive.

Pour contrôler le nombre d'applications de L, une comparaison complémentaire à exposition égale pourra être construite à partir du nombre d'applications S/L effectivement observé, sans utiliser la HV.

Cette comparaison sera explicitement qualifiée de contrôle descriptif d'exposition. Elle ne remplacera pas la comparaison principale avec DA+Calendrier.

## 6. Phase D — Diagnostic sans HV

### Objectif

Vérifier si DEC fixe modifie les indicateurs d'ignorance et de population avant d'introduire les règles adaptatives.

### Bras

- DA ;
- DA+S ;
- DA+L ;
- DA+Fixe-P11.

### Plan

- SC6 ;
- 30 graines : 11000–11029 ;
- budget : 6 040 évaluations par run ;
- comparaison appariée par graine et scénario.

### Mesures

Aux générations 1, 25, 50, 100 et 150 :

- \(\bar m_{DA}(\Theta)\) ;
- \(\bar m_E(\Theta)\) ;
- \(\Delta m\) ;
- conflit ;
- `Dep` ;
- \(N_{\mathrm{eff}}\) ;
- `frac_dup` ;
- `q_max` ;
- `q_ent` ;
- compteurs DEC.

Les trajectoires complètes seront également conservées.

### Analyse

Les contrastes principaux sont :

\[
DA+L-DA
\]

et

\[
DA+S-DA.
\]

Pour chaque contraste, rapporter :

- moyenne des différences appariées ;
- intervalle bootstrap à 95 % ;
- distribution par scénario ;
- trajectoires par génération.

L'unité de rééchantillonnage est la graine, en conservant ensemble les six scénarios d'une même graine. Les scénarios ne seront pas traités comme des réplications indépendantes.

La phase D reste descriptive. Aucune p-valeur confirmatoire ne sera rapportée.

Le script d'analyse ne lit aucun champ HV.

### Règle de décision avant la phase D

La prémisse opérationnelle « DEC fort réduit l'ignorance moyenne de DA » sera considérée comme étayée dans ce montage si, aux trois points de contrôle 50, 100 et 150 (les trois conditions simultanément, sans ajustement de multiplicité, phase descriptive) :

- la borne supérieure de l'IC95 % du contraste \(\bar m(\Theta)[DA+L]-\bar m(\Theta)[DA]\) est inférieure à zéro.

La prémisse sera considérée comme non étayée si l'intervalle contient zéro ou si le contraste est positif.

Les indicateurs `Dep` et \(N_{\mathrm{eff}}\) seront examinés séparément.

Même si l'ignorance diminue, cela ne démontrera pas que la dépendance entre sources a diminué. La conclusion sera limitée à l'effet observé de DEC sur l'ignorance et les diagnostics de population.

Si le critère n'est pas satisfait, la phase P ne sera pas automatiquement lancée. Une nouvelle proposition méthodologique et une autorisation seront nécessaires.

## 7. Phase P — Pilote de régulation adaptative

Cette phase est distincte de la phase D et exige une autorisation écrite séparée.

### Bras

- DA ;
- DA+S ;
- DA+L ;
- DA+Fixe-P11 ;
- DA+R1 ;
- DA+R2 ;
- DA+R1-inv ;
- DA+Calendrier ;
- E.

### Objectif

Étudier les trajectoires produites par les règles adaptatives et les comparer aux intensités fixes et au calendrier non adaptatif.

### Mesures

Enregistrer les mêmes indicateurs que dans la phase D, ainsi que :

- proportion de générations passées en régime L ;
- nombre de transitions S vers L et L vers S ;
- durée moyenne de chaque régime ;
- évaluations consommées dans chaque régime ;
- HV finale oracle.

Les résultats HV ne seront lus qu'après le gel des données, du code et du script d'analyse de cette phase.

### Interprétation

Une amélioration de HV ne sera pas automatiquement attribuée à une réduction de l'ignorance.

L'interprétation devra examiner conjointement :

- les changements d'ignorance ;
- les changements de `Dep` et \(N_{\mathrm{eff}}\) ;
- la concentration ;
- le nombre de réparations ;
- l'exposition aux niveaux S et L ;
- le contrôle de calendrier.

Le pilote restera descriptif et ne constituera pas une confirmation statistique.

## 8. Hypothèses descriptives

**HD1 :** DA+L présente une ignorance moyenne inférieure à DA.

**HD2 :** DA+L présente une dépendance génotypique `Dep` inférieure à DA et/ou un \(N_{\mathrm{eff}}\) supérieur.

**HD3 :** DEC modifie le conflit et la concentration de la cible d'échantillonnage ; aucun signe n'est présupposé.

**HP1 :** R1 produit une trajectoire d'ignorance différente de DA+S et DA+L.

**HP2 :** R2 produit une trajectoire d'ignorance différente de DA+S et DA+L.

**HP3 :** une différence entre les règles adaptatives et le contrôle de calendrier indique que le moment de l'intervention peut avoir une importance au-delà du seul nombre d'applications de L.

Aucune hypothèse ne prédit une amélioration de HV. Une amélioration, une absence d'effet ou une dégradation sont des résultats recevables.

## 9. Implémentation prévue

Après autorisation seulement :

- module séparé `p16.py` ;
- import de P10/P11/P15 sans modification ;
- contrôleur appelé entre deux générations.

Tests techniques prévus :

1. contrôleur inactif = P15 DA bit à bit ;
2. niveau fixe via contrôleur = DEC fixe correspondant ;
3. budget d'évaluations inférieur ou égal à 6 040 ;
4. modification des paramètres uniquement entre générations ;
5. R1, R2 et R1-inv sélectionnent le niveau prévu sur des valeurs synthétiques ;
6. R2 utilise les valeurs appariées DA/E de la même génération ;
7. aucune fuite de HV dans la phase D ;
8. calendrier non adaptatif reproductible ;
9. traçabilité des paramètres DEC appliqués à chaque génération ;
10. Δm ≥ 0 sur sources identiques (échec = incident, non corrigé en silence) ;
11. taux de violations et de régénérations par régime S/L, rapportés séparément.

Les tests et le gel du code nécessitent une autorisation explicite. Aucun résultat de test n'est présumé.

## 10. Limites et précautions d'interprétation

1. DEC est aussi un opérateur de diversité et de réparation. Son effet sur HV ne peut être attribué à la seule dépendance.
2. `Dep` est une dépendance génotypique de population, pas une mesure directe de dépendance entre sources.
3. \(\Delta m\) est une différence entre deux traitements de l'évidence, pas une mesure causale de redondance.
4. Une diminution de \(m(\Theta)\) n'est pas nécessairement un gain d'optimisation.
5. Une augmentation de l'ignorance n'est pas nécessairement négative si elle évite une confiance injustifiée.
6. La concentration, le conflit et l'ignorance doivent être analysés séparément.
7. Une règle adaptative peut imiter un calendrier fixe.
8. Le paramètre \(w=0,3\) hérité de P10 a été choisi sur HV et cette origine doit rester déclarée.
9. Une seule famille d'instances ne permet pas une généralisation à tous les problèmes d'affectation HHC.
10. Toute revendication de nouveauté attend la recherche bibliographique RS1 de l'auteur.
11. Passage à L sur une population déjà regroupée (Claude) : le test `ok` de DEC vérifie aussi que chaque voisin du candidat respecte le plafond ; si la population dépasse déjà n_max = 2, la plupart des candidats voisins échouent à la réparation, sont gardés et comptés comme violations. L'intensité effective de L peut donc différer de l'intensité nominale ; les violations sont rapportées par régime et l'interprétation en tient compte.
12. Dans les arbres de décision D16, le sens « moins de dépendance, moins d'ignorance » est une hypothèse (HD1), pas un résultat.

## 11. Décisions à trancher

**D16-1 :** confirmer les niveaux S, L et Fixe-P11.

**D16-2 :** confirmer le seuil unique ou demander une règle à trois régimes.

**D16-3 :** conserver R2 fondée sur \(\Delta m\), en reconnaissant qu'elle ne mesure pas directement la dépendance entre sources.

**D16-4 :** autoriser ou non la calibration HV-aveugle des seuils (SC3, graines 11100–11114).

**D16-5 :** autoriser ou non la phase D (SC6, graines 11000–11029).

**D16-6 :** confirmer la liste des bras, notamment le contrôle DA+Calendrier.

**D16-7 :** confirmer la définition opérationnelle et le nom exact des attributs DEC dans l'API.

**D16-8 :** confirmer que la phase P fera l'objet d'une autorisation écrite distincte, après lecture de la phase D.

**D16-9 (Claude) :** niveau initial de DEC à la génération 1 (S proposé) et sa justification.

**D16-10 (Claude) :** confirmer le retrait de Q-S des questions expérimentales.

## 12. Règles permanentes

- Dépôt GitHub et codes gelés P3–P5, P7, P10, P11, P14 et P15 inchangés.
- Aucun rerun pour améliorer un résultat.
- Aucune hypothèse, aucun seuil et aucune règle modifiés après lecture des résultats.
- Chemins absolus pour les sorties.
- Incidents consignés.
- Les propositions d'autres assistants sont des entrées méthodologiques ; seules les déclarations explicites de l'auteur autorisent une action.
- Aucun calcul, calibration, pilote, gel ou expérimentation n'est autorisé par le présent brouillon.