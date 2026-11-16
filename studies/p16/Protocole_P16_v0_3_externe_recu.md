# Protocole P16 v0.3 — Régulation adaptative de DEC et évolution de l'ignorance

**Statut :** brouillon méthodologique — conception et révision uniquement.  
**Date :** 11 novembre 2026.  
**Version précédente :** P16 v0.2-F (fusion).  
**Autorisation actuelle :** rédaction et révision du protocole uniquement. Aucun code, calcul, test, calibration, pilote, gel ou expérimentation n'est autorisé.

---

## 0. Objet et principes méthodologiques

P16 étudie si une régulation adaptative de l'intensité de DEC peut modifier l'ignorance de la fonction de croyance DA et si cette évolution est associée aux propriétés de la population de recherche.

Le protocole distingue trois notions :

1. **Ignorance de l'évidence :** masse \(m(\Theta)\).
2. **Dépendance génotypique de la population :** indicateur `Dep`, défini par `dep_stats` dans P11.
3. **Dépendance entre sources d'information :** dépendance liée à la provenance, aux données communes et aux erreurs partagées entre sources documentaires, historiques ou supervisées.

Ces notions ne sont pas interchangeables. En particulier, `Dep` ne mesure pas directement la dépendance statistique entre sources d'information.

DEC intervient sur le processus de recherche et de réparation des affectations. Une modification de `Dep` ou de \(m(\Theta)\) après son intervention ne démontre donc pas, à elle seule, un mécanisme causal reliant dépendance et ignorance.

Les résultats seront interprétés en premier lieu comme des effets observés de DEC sur les indicateurs mesurés. Toute interprétation mécanistique devra être justifiée séparément.

### Principes de comparaison

- Les comparaisons entre bras doivent être appariées par graine et scénario.
- Les mêmes données et propositions doivent être utilisées pour les calculs DA et E lorsqu'ils servent à construire \(\Delta m\).
- Les indicateurs de population et les indicateurs d'évidence doivent être rapportés séparément.
- Les intensités nominales de DEC ne seront pas assimilées automatiquement à des intensités effectives.
- Aucune conclusion sur la HV ne sera tirée de la phase D, qui reste aveugle à cette mesure.

---

## 1. Questions de recherche

### Q-D — Diagnostic de l'effet de DEC

Une intensité DEC forte modifie-t-elle, par rapport à DA sans DEC :

- l'ignorance moyenne \(\bar m(\Theta)\) ;
- la dépendance génotypique `Dep` ;
- la diversité effective \(N_{\mathrm{eff}}\) ;
- la concentration de la cible d'échantillonnage ;
- le conflit conjonctif entre propositions ?

Deux directions sont possibles :

- diminution de l'ignorance, éventuellement associée à une diminution de `Dep` ;
- augmentation ou absence de diminution de l'ignorance, notamment lorsque les réparations modifient les propositions ou leur concordance.

Le signe de l'effet est empirique. Il n'est pas présupposé.

### Q-R — Régulation adaptative

Une régulation de DEC fondée sur :

- l'ignorance moyenne de DA (R1) ;
- la différence d'ignorance entre DA et le calcul Dempster de référence (R2) ;

modifie-t-elle les trajectoires d'ignorance, les indicateurs de population, le conflit et la qualité finale des affectations, par rapport aux intensités fixes et à un calendrier non adaptatif ?

La valeur ajoutée de l'adaptation devra être distinguée de l'effet du niveau d'intensité et de l'effet du moment auquel DEC intervient.

### Q-S — Dépendance entre sources

Cette question est retirée des questions expérimentales de P16.

Le moteur considéré ne dispose pas, dans le cadre décrit ici, d'une provenance suffisamment documentée ni d'une mesure directe des données communes et des erreurs partagées entre sources. Les masses de croyance seules ne permettent pas d'identifier un coefficient universel de dépendance entre sources.

Une étude de la dépendance documentaire et statistique entre sources nécessiterait un protocole distinct.

---

## 2. Grandeurs mesurées et définitions

Les diagnostics sont enregistrés par génération.

### 2.1. Ignorance DA

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

Le calcul E utilise les mêmes sources et les mêmes données d'entrée que DA, sans correction DEC.

Pour toute comparaison utilisée dans R2, les deux calculs doivent porter sur les mêmes propositions, pour les mêmes patients et à la même génération. Une comparaison entre deux populations de candidats différentes ne constitue pas une différence d'ignorance appariée au sens de cette définition.

### 2.3. Différence d'ignorance DA–E

\[
\Delta m
=\bar m_{DA}(\Theta)-\bar m_E(\Theta)
\]

Cette variable est appelée **différence d'ignorance DA–E**. Elle n'est pas appelée « ignorance attribuable à la dépendance ».

La version fusionnée rapporte la propriété suivante :

> Lorsque les calculs DA et E utilisent les mêmes sources, les poids corrigés de DA sont inférieurs ou égaux aux poids de E, avec \(1\leq\tilde n_t\leq n_t\). Il en résulterait \(m_{DA,i}(\Theta)\geq m_{E,i}(\Theta)\) et donc \(\Delta m\geq0\), au bruit numérique près.

Cette propriété est rapportée comme une propriété annoncée de l'implémentation, et non comme une démonstration générale indépendante du code.

Le test unitaire mentionné dans la fusion aurait porté sur 60 jeux de sources dans P15. Il n'est pas considéré comme réexécuté ou vérifié dans le cadre de cette révision.

Conséquences opérationnelles proposées :

- \(\Delta m>0\) : DA conserve davantage d'ignorance que E ;
- \(\Delta m=0\) : les deux calculs présentent la même ignorance moyenne ;
- \(\Delta m<0\) : résultat incompatible avec la propriété annoncée, à examiner comme incident.

Aucune troncature ni valeur absolue ne sera appliquée à \(\Delta m\). Un résultat négatif ne sera pas corrigé silencieusement.

### 2.4. Dépendance et diversité de la population

Les diagnostics comprennent :

- `Dep`, défini par `dep_stats` dans P11 ;
- \(N_{\mathrm{eff}}\) ;
- `frac_dup` ;
- `q_max` ;
- `q_ent` ;
- similarité moyenne ;
- taille du premier front ;
- \(N_{\mathrm{eff}}\) des sources du premier front.

Ces variables décrivent la dynamique de recherche. Elles ne constituent pas, isolément, des mesures de dépendance statistique entre sources d'information.

### 2.5. Conflit

Le conflit doit être distingué de l'ignorance.

La fusion précise que le champ `m_empty` utilisé dans P7/P15 correspond au conflit conjonctif non normalisé :

\[
K=1-e^{-W}
\left(1+\sum_s(e^{W_s}-1)\right)
\]

Il sera donc désigné par \(K\), et non par une masse finale sur l'ensemble vide.

Pour la règle de Dempster normalisée, lorsque la normalisation est définie, la masse finale sur l'ensemble vide est nulle. Il ne faut donc pas assimiler automatiquement cette masse finale au conflit \(K\).

Les valeurs antérieurement rapportées sous le nom `m_empty` devront être interprétées comme des valeurs de \(K\), sous réserve de confirmation de la correspondance exacte avec l'implémentation.

### 2.6. Diagnostics DEC

Enregistrer :

- intensité nominale choisie ;
- `n_max` ;
- paramètre correspondant à la fraction maximale de patients modifiés ;
- nombre de réparations ;
- mutations ;
- violations ;
- candidats réparés ;
- régénérations ;
- recherches locales ignorées ;
- évaluations consommées.

Le nom conceptuel \(\rho_{\max}\) doit être distingué du nom exact de l'attribut utilisé dans l'API. Cette correspondance reste à vérifier avant toute implémentation.

Les résultats devront distinguer :

- **intensité nominale** : niveau S ou L demandé au contrôleur ;
- **intervention effective** : réparations et modifications effectivement réalisées ;
- **échecs ou violations** : situations où les contraintes de DEC ne sont pas satisfaites.

La HV finale peut être enregistrée dans les données, mais elle demeure inaccessible au script d'analyse de la phase D.

---

## 3. Intensités de DEC

Le paramètre \(\sigma=0,7\) est maintenu, ainsi que \(r_{\max}=3\), conformément à la proposition v0.1.

Deux intensités sont proposées :

| Niveau | \(n_{\max}\) | \(\rho_{\max}\) | Interprétation nominale |
|---|---:|---:|---|
| S — petit pas | 5 | 0,2 | Intervention plus limitée |
| L — grand pas | 2 | 0,4 | Intervention plus forte |

Référence fixe P11 :

| Niveau | \(n_{\max}\) | \(\rho_{\max}\) |
|---|---:|---:|
| Fixe-P11 | 2 | 0,2 |

La proposition considère qu'un plafond de voisins plus faible correspond à une intervention plus forte. Cette interprétation est nominale : elle ne garantit pas que le nombre de réparations effectivement réalisées sera supérieur.

La fusion signale notamment que le passage à \(n_{\max}=2\) dans une population déjà regroupée peut conduire à des échecs de réparation et à des violations. Ce risque doit être conservé dans l'interprétation des résultats.

Le contrôleur ne modifie que les paramètres DEC entre deux générations. La valeur calculée à la génération \(t\) s'applique aux candidats de la génération \(t+1\).

### 3.1. Initialisation

La v0.2-F propose un niveau S au démarrage des bras adaptatifs et du calendrier. Elle indique également que la population initiale est nettoyée par DEC avant la première mesure.

Cette formulation doit être précisée pour éviter une contamination de la comparaison :

- les bras avec DEC peuvent appliquer leur procédure initiale de nettoyage, selon une règle commune explicitement définie ;
- le bras DA sans DEC ne doit pas subir implicitement une réparation DEC ;
- les mesures de génération 1 doivent être prises après une initialisation identique dans tous les bras, sauf pour l'intervention expérimentale explicitement étudiée.

**Proposition à confirmer :** niveau S pour l'initialisation des bras DEC, et aucune intervention DEC pour DA. La définition exacte de la population mesurée en génération 1 reste une décision ouverte.

Aucune modification de la classe DEC n'est prévue dans le protocole.

---

## 4. Règles de régulation

### 4.1. R1 — Régulation selon l'ignorance

\[
R1(t)=
\begin{cases}
L & \text{si }\bar m_{DA,t}(\Theta)\geq\tau\\
S & \text{sinon}
\end{cases}
\]

Lorsque l'ignorance moyenne est au moins égale au seuil, le contrôleur choisit L. Dans le cas contraire, il choisit S.

Cette règle traduit l'hypothèse de l'auteur selon laquelle une ignorance élevée appelle une intervention DEC plus forte.

Avec un seuil unique, la règle distingue deux régimes, et non trois niveaux indépendants.

### 4.2. R2 — Régulation selon la différence d'ignorance DA–E

\[
R2(t)=
\begin{cases}
L & \text{si }\Delta m_t\geq\tau_\Delta\\
S & \text{sinon}
\end{cases}
\]

R2 utilise la différence d'ignorance entre DA et E calculée sur les mêmes propositions.

R2 ne mesure pas directement la dépendance entre sources.

**Précaution importante :** lorsque \(\bar m_E(\Theta)\) est faible, \(\Delta m\) peut être très proche de \(\bar m_{DA}(\Theta)\). R2 peut alors se comporter de façon proche de R1. La comparaison entre les deux règles devra donc rapporter :

- la corrélation entre les signaux R1 et R2 ;
- la proportion de générations où les règles choisissent des niveaux différents ;
- le nombre de transitions S/L ;
- les trajectoires d'ignorance produites.

Si les décisions de R1 et R2 sont presque toujours identiques, il ne sera pas possible de revendiquer une valeur ajoutée substantielle de R2 sur la seule base de résultats finaux similaires.

### 4.3. R1-inv — Contrôle négatif

\[
R1_{\mathrm{inv}}(t)=
\begin{cases}
S & \text{si }\bar m_{DA,t}(\Theta)\geq\tau\\
L & \text{sinon}
\end{cases}
\]

Cette règle permet d'examiner si le sens de la régulation influence les résultats.

Elle constitue un contrôle exploratoire, et non une stratégie dont la supériorité ou l'infériorité est présupposée.

### 4.4. Détermination des seuils

Les seuils sont déterminés avant la phase D et avant toute lecture de HV.

Calibration proposée :

- bras DA sans DEC ;
- scénario SC3 ;
- graines techniques 11100–11114 ;
- générations 1 à 150 ;
- aucune HV calculée ou consultée.

Le calcul se déroule en deux étapes :

1. calcul de la médiane des générations 1 à 150 pour chaque run ;
2. calcul de la médiane des médianes entre les runs de calibration.

Le même principe est appliqué séparément à \(\bar m_{DA}(\Theta)\) et à \(\Delta m\).

Cette procédure produit un seuil unique pour R1 et un seuil unique pour R2.

**Limite de généralisation :** les seuils sont calibrés sur SC3, alors que la phase D porte sur SC6. Leur stabilité entre scénarios n'est donc pas garantie. Les résultats devront signaler explicitement cette différence de domaine. Aucune recalibration sur les résultats de la phase D ne sera autorisée dans le cadre de ce protocole.

La calibration requiert une autorisation écrite distincte.

---

## 5. Bras expérimentaux

Les bras proposés sont :

| Bras | Configuration | Rôle |
|---|---|---|
| E | Dempster | Référence de combinaison |
| DA | DA sans DEC | Référence principale |
| DA+S | DEC fixe, petit pas | Contrôle d'intensité faible |
| DA+L | DEC fixe, grand pas | Contrôle d'intensité forte |
| DA+Fixe-P11 | DEC fixe P11 | Référence antérieure |
| DA+R1 | DEC adaptatif selon ignorance | Règle de l'auteur |
| DA+R2 | DEC adaptatif selon différence DA–E | Règle alternative |
| DA+R1-inv | Règle inversée | Contrôle négatif |
| DA+Calendrier | Alternance S/L non adaptative | Contrôle temporel |

### 5.1. Contrôle de calendrier

DA+Calendrier utilise les mêmes niveaux S et L que les règles adaptatives, mais leur ordre ne dépend pas de l'ignorance.

La fusion propose L de la génération 1 à 50, puis S. Cette proposition doit être harmonisée avec la proposition d'initialisation commune en S.

**Proposition à confirmer :** appliquer le même traitement initial que les autres bras DEC, puis commencer le calendrier non adaptatif à la première génération de décision du contrôleur. La séquence exacte devra être inscrite dans le protocole de la phase P et gelée avant toute exécution.

Une comparaison complémentaire à exposition égale pourra être construite à partir du nombre d'applications S/L effectivement observé. Elle sera qualifiée de contrôle descriptif d'exposition : construite à partir des expositions réalisées, elle ne constitue pas un contrôle expérimental indépendant.

Elle ne remplacera pas la comparaison principale avec DA+Calendrier.

---

## 6. Phase D — Diagnostic sans HV

### 6.1. Objectif

Vérifier si DEC fixe modifie les indicateurs d'ignorance et de population avant d'introduire les règles adaptatives.

### 6.2. Bras

- DA ;
- DA+S ;
- DA+L ;
- DA+Fixe-P11.

### 6.3. Plan proposé

- SC6 ;
- 30 graines : 11000–11029 ;
- budget : 6 040 évaluations par run ;
- comparaison appariée par graine et scénario.

### 6.4. Mesures

Aux générations 1, 25, 50, 100 et 150 :

- \(\bar m_{DA}(\Theta)\) ;
- \(\bar m_E(\Theta)\) ;
- \(\Delta m\) ;
- conflit \(K\) ;
- `Dep` ;
- \(N_{\mathrm{eff}}\) ;
- `frac_dup` ;
- `q_max` ;
- `q_ent` ;
- compteurs DEC.

Les trajectoires complètes seront conservées.

Les compteurs DEC seront analysés par niveau nominal, afin de vérifier si S et L produisent effectivement des interventions distinctes.

### 6.5. Analyse

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
- distribution des différences par scénario ;
- trajectoires par génération ;
- compteurs d'intervention effective.

L'unité de rééchantillonnage est la graine, en conservant ensemble les six scénarios d'une même graine. Les scénarios ne seront pas traités comme des réplications indépendantes.

La phase D reste descriptive. Aucune p-valeur confirmatoire ne sera rapportée.

Le script d'analyse ne lit aucun champ HV.

### 6.6. Règle de décision proposée

La prémisse opérationnelle « DEC fort réduit l'ignorance moyenne de DA » sera considérée comme étayée dans ce montage si, aux trois points de contrôle 50, 100 et 150, les trois conditions suivantes sont simultanément satisfaites :

- la borne supérieure de l'IC95 % du contraste \(\bar m(\Theta)[DA+L]-\bar m(\Theta)[DA]\) est inférieure à zéro à la génération 50 ;
- la même condition est satisfaite à la génération 100 ;
- la même condition est satisfaite à la génération 150.

Cette règle est une condition conjointe : il faut satisfaire les trois critères, et non sélectionner a posteriori le point de contrôle le plus favorable.

Si l'une des conditions échoue, la prémisse sera considérée comme non étayée selon le critère préétabli.

Les indicateurs `Dep` et \(N_{\mathrm{eff}}\) seront examinés séparément. Ils ne remplacent pas le critère d'ignorance.

Même si l'ignorance diminue, cela ne démontrera pas que la dépendance entre sources a diminué.

Si le critère n'est pas satisfait, la phase P ne sera pas automatiquement lancée. Une nouvelle proposition méthodologique et une autorisation écrite seront nécessaires.

---

## 7. Phase P — Pilote de régulation adaptative

Cette phase est distincte de la phase D et exige une autorisation écrite séparée.

### 7.1. Bras proposés

- DA ;
- DA+S ;
- DA+L ;
- DA+Fixe-P11 ;
- DA+R1 ;
- DA+R2 ;
- DA+R1-inv ;
- DA+Calendrier ;
- E.

### 7.2. Objectif

Étudier les trajectoires produites par les règles adaptatives et les comparer aux intensités fixes et au calendrier non adaptatif.

### 7.3. Mesures

Enregistrer les mêmes indicateurs que dans la phase D, ainsi que :

- proportion de générations passées en régime L ;
- nombre de transitions S vers L et L vers S ;
- durée moyenne de chaque régime ;
- évaluations consommées dans chaque régime ;
- nombre de réparations et de violations par régime ;
- HV finale oracle.

Les résultats HV ne seront lus qu'après gel des données, du code et du script d'analyse de cette phase.

### 7.4. Interprétation

Une amélioration de HV ne sera pas automatiquement attribuée à une réduction de l'ignorance.

L'interprétation examinera conjointement :

- les changements d'ignorance ;
- les changements de `Dep` et \(N_{\mathrm{eff}}\) ;
- la concentration ;
- le conflit ;
- le nombre de réparations et de violations ;
- l'exposition aux niveaux S et L ;
- les différences entre R1, R2 et le contrôle de calendrier.

Le pilote restera descriptif et ne constituera pas une confirmation statistique.

---

## 8. Hypothèses descriptives

**HD1 :** DA+L présente une ignorance moyenne inférieure à DA.

**HD2 :** DA+L présente une dépendance génotypique `Dep` inférieure à DA et/ou un \(N_{\mathrm{eff}}\) supérieur.

**HD3 :** DEC modifie le conflit et la concentration de la cible d'échantillonnage ; aucun signe n'est présupposé.

**HP1 :** R1 produit une trajectoire d'ignorance différente de DA+S et DA+L.

**HP2 :** R2 produit une trajectoire d'ignorance différente de DA+S et DA+L.

**HP3 :** une différence entre les règles adaptatives et le contrôle de calendrier indique que le moment de l'intervention peut avoir une importance au-delà du seul nombre d'applications de L.

Aucune hypothèse ne prédit une amélioration de HV.

Une amélioration, une absence d'effet ou une dégradation sont des résultats recevables.

---

## 9. Implémentation prévue

Après autorisation seulement :

- module séparé `p16.py` ;
- import de P10/P11/P15 sans modification ;
- contrôleur appelé entre deux générations.

### Tests techniques prévus

1. Contrôleur inactif = P15 DA bit à bit.
2. Niveau fixe via contrôleur = DEC fixe correspondant.
3. Budget d'évaluations inférieur ou égal à 6 040.
4. Modification des paramètres uniquement entre générations.
5. R1, R2 et R1-inv sélectionnent le niveau prévu sur des valeurs synthétiques.
6. R2 utilise les valeurs appariées DA/E de la même génération et des mêmes propositions.
7. Aucune fuite de HV dans la phase D.
8. Calendrier non adaptatif reproductible.
9. Traçabilité des paramètres DEC appliqués à chaque génération.
10. \(\Delta m\geq0\) sur sources identiques, sous réserve de la propriété annoncée ; un échec est déclaré comme incident.
11. Taux de violations et de régénérations par régime S/L, rapportés séparément.
12. Initialisation conforme à la définition approuvée, sans intervention DEC implicite dans le bras DA.

Les tests et le gel du code nécessitent une autorisation explicite. Aucun résultat de test n'est présumé.

---

## 10. Limites et précautions d'interprétation

1. DEC est aussi un opérateur de diversité et de réparation. Son effet sur HV ne peut pas être attribué à la seule dépendance.
2. `Dep` est une dépendance génotypique de population, pas une mesure directe de dépendance entre sources.
3. \(\Delta m\) est une différence entre deux traitements de l'évidence, pas une mesure causale de redondance.
4. Une diminution de \(m(\Theta)\) n'est pas nécessairement un gain d'optimisation.
5. Une augmentation de l'ignorance n'est pas nécessairement négative si elle évite une confiance injustifiée.
6. Concentration, conflit et ignorance doivent être analysés séparément.
7. Une règle adaptative peut imiter un calendrier fixe.
8. Le paramètre \(w=0,3\) hérité de P10 a été choisi sur HV ; cette origine doit rester déclarée.
9. Une seule famille d'instances ne permet pas une généralisation à tous les problèmes d'affectation HHC.
10. Toute revendication de nouveauté attend la recherche bibliographique RS1 de l'auteur.
11. Le passage à L sur une population déjà regroupée peut entraîner des échecs de réparation et des violations. L'intensité effective peut donc différer de l'intensité nominale.
12. Le sens « moins de dépendance génotypique, moins d'ignorance » demeure une hypothèse, pas un résultat.
13. La calibration des seuils sur SC3 et leur application sur SC6 limitent la portée de leur généralisation.
14. Si R1 et R2 produisent presque toujours les mêmes décisions, la comparaison ne permettra pas d'établir une supériorité spécifique de l'un des signaux.
15. Le contrôle d'exposition construit à partir des décisions effectivement observées est descriptif et ne remplace pas un contrôle indépendant préétabli.
16. La comparaison DA/E utilisée par R2 doit être calculée sur des propositions identiques ; sinon, le signal mélange différence de traitement et différence de composition de population.

---

## 11. Décisions à trancher

**D16-1 :** confirmer les niveaux S, L et Fixe-P11.

**D16-2 :** confirmer le seuil unique ou demander une règle à trois régimes.

**D16-3 :** conserver R2 fondée sur \(\Delta m\), en reconnaissant qu'elle ne mesure pas directement la dépendance entre sources et qu'elle peut être proche de R1.

**D16-4 :** autoriser ou non la calibration HV-aveugle des seuils (SC3, graines 11100–11114).

**D16-5 :** autoriser ou non la phase D (SC6, graines 11000–11029).

**D16-6 :** confirmer la liste des bras, notamment le contrôle DA+Calendrier.

**D16-7 :** confirmer la définition opérationnelle et le nom exact des attributs DEC dans l'API.

**D16-8 :** confirmer que la phase P fera l'objet d'une autorisation écrite distincte, après lecture de la phase D.

**D16-9 :** confirmer le niveau initial de DEC à la génération 1 et sa justification, en distinguant l'initialisation des bras DEC du bras DA sans DEC.

**D16-10 :** confirmer le retrait de Q-S des questions expérimentales de P16.

**D16-11 :** confirmer la définition opérationnelle de la comparaison DA/E utilisée pour R2 : mêmes propositions, mêmes patients et même génération.

**D16-12 :** confirmer le calendrier initial de DA+Calendrier et son articulation avec l'initialisation commune des bras DEC.

---

## 12. Règles permanentes

- Dépôts GitHub et codes gelés P3–P5, P7, P10, P11, P14 et P15 inchangés.
- Aucun rerun pour améliorer un résultat.
- Aucune hypothèse, aucun seuil et aucune règle modifiés après lecture des résultats.
- Chemins absolus pour les sorties.
- Incidents consignés.
- Les propositions d'autres assistants sont des entrées méthodologiques ; seules les déclarations explicites de l'auteur autorisent une action.
- Aucun calcul, calibration, test, pilote, gel ou expérimentation n'est autorisé par le présent brouillon.

**Statut final de P16 v0.3 : proposition révisée, non approuvée et non exécutée.**