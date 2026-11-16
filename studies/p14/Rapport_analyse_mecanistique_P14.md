# Analyse mécanistique exploratoire de E, Dg et Dp (traces P14 déjà stockées)
Date : 10 novembre 2026. Autorisation : décision écrite du Dr Montassar Zaghdoud, 17:18, option (b). **Exploratoire, post hoc (après lecture du rapport P14), descriptive : aucun test, aucune p-valeur, aucun rerun, aucune reconstruction.** Données : p14/runs/conf (1 200 fichiers = 200 graines × 6 scénarios ; traces par génération, générations 0–150). Scripts de lecture seule (non du moteur) : p14/mech/mech_read.py, mech_read2.py ; sorties : mech_read_out.json, mech_read2_out.json.

## 0. Ce qui est disponible et ce qui ne l'est pas
Disponible par génération : q_ent, q_max (cible d'échantillonnage ; E, Dp, Dg seulement), entropie marginale de la population, Dep, N_eff, fraction de doublons, taille et N_eff du premier front (sources de QGA2-E). **Non disponible : la HV par génération** (seules la HV et le front finaux sont stockés), donc ni « évolution de la HV » ni vitesse de convergence en HV ; et aucune trace permettant de juger de la capacité à éviter les minima locaux. Aucune valeur n'est reconstruite. Pour B et Bt, la cible q n'existe pas (pas de modèle).

## 1. Dynamique de la cible (moyennes sur 200 graines × 6 scénarios)
| Génération | 1 | 25 | 50 | 100 | 150 |
|---|---|---|---|---|---|
| q_max E | 0,449 | 0,669 | 0,747 | 0,818 | 0,851 |
| q_max Dg | 0,536 | 0,615 | 0,682 | 0,761 | 0,802 |
| q_max Dp | 0,298 | 0,281 | 0,280 | 0,280 | 0,279 |
| q_ent E | 1,276 | 0,906 | 0,748 | 0,598 | 0,527 |
| q_ent Dg | 1,120 | 1,021 | 0,899 | 0,741 | 0,654 |
| q_ent Dp | 1,449 | 1,458 | 1,459 | 1,459 | 1,459 |
**Lecture.** Dg part plus concentré que E (q_max 0,54 contre 0,45 à la génération 1), puis E le rattrape et le dépasse à partir d'environ la génération 25 : la concentration de E est **adaptative** (elle croît avec la convergence de la population), celle de Dg est fixée en grande partie par la transformation puissance. Dp reste plat. Cela est cohérent avec l'échec de G-N sur les moyennes, et avec la forme exponentielle de Dempster contre la loi de puissance de Dg (document de formalisation, section 1).

## 2. Diversité et redondance (population de 40)
| Génération | 25 | 50 | 100 | 150 |
|---|---|---|---|---|
| Dep E / Dg / Dp | 0,030 / 0,015 / 0,002 | 0,139 / 0,056 / 0,002 | 0,328 / 0,192 / 0,002 | 0,448 / 0,335 / 0,002 |
| N_eff E / Dg / Dp | 37,7 / 38,8 / 39,8 | 31,7 / 36,0 / 39,8 | 23,0 / 28,5 / 39,8 | 17,8 / 21,6 / 39,8 |
| Entropie marginale E / Dg / Dp | 1,231 / 1,242 / 1,373 | 1,089 / 1,138 / 1,369 | 0,913 / 0,968 / 1,365 | 0,812 / 0,852 / 1,362 |
B : Dep 0,228 et N_eff 25,9 à la génération 150 ; Bt : 0,494 et 13,2. **Dp ne converge pratiquement pas** (entropie 1,38 vers 1,36) : sa « vitesse de convergence » n'est pas définie de façon utile (le déclin total est de 0,02). Sur les moitiés de déclin de l'entropie marginale : E 53 générations, Dg 56, B 22, Bt 16 (Dp non interprétable). E converge un peu plus vite et plus loin que Dg ; Bt converge le plus vite.

## 3. Les sources de QGA2-E (premier front)
Taille moyenne du front et N_eff de ses sources à la génération 150 : E 30,5 / 11,7 (rapport 0,46) ; Dg 30,0 / 16,3 (0,56) ; Dp 31,5 / 31,3 (1,00). Aux générations 10 et 25, le rapport est ≈ 0,95–1,0 pour tous. **La redondance des sources n'apparaît qu'après la génération 50** (E : 0,80 ; 0,58 à 100). Conséquence pour DA-DST : un affaiblissement par la dépendance agirait peu en début de run et fortement en fin de run, c'est-à-dire pendant la phase où E est le plus concentré.

## 4. Lien concentration–qualité : un piège à éviter
Corrélation de Spearman brute entre q_max moyen par run et HV, sur 1 200 runs de E : **0,75**. Ce chiffre est essentiellement un artefact de scénario (les scénarios C101, faciles, ont à la fois une HV plus haute et un q_max plus haut). **Dans chaque scénario**, la corrélation sur les graines est faible : E de −0,05 à +0,37 (moyenne 0,09) ; Dg de −0,02 à +0,41 (moyenne 0,20) ; Dp ≈ 0. Au niveau des graines (moyenne sur SC6) : ≈ 0 pour E et Dg. **Conclusion descriptive : la concentration varie beaucoup entre bras (Dp 0,28 contre E et Dg 0,70–0,80, avec HV 0,48 contre 0,52–0,53), mais elle n'explique presque pas la variation de HV entre graines à l'intérieur d'un bras.** Avec trois bras seulement, l'association entre bras n'est qu'un constat, pas une preuve de causalité.

## 5. E contre Dg par scénario (différence de HV moyenne)
E − Dg : S4-C101 −0,0068 ; S4-R101 −0,0006 ; S4-RC101 −0,0021 ; S5-C101 +0,0003 ; S5-R101 −0,0069 ; S5-RC101 −0,0079. Dg ≥ E dans 5 scénarios sur 6, avec un écart très faible (≤ 0,008) ; Dg − Dp entre +0,035 et +0,054 dans tous.

## 6. Ce que l'analyse permet de dire et de ne pas dire
Permis (descriptif) : (i) Dg et E atteignent des niveaux de concentration comparables en fin de run mais par des trajectoires différentes ; (ii) E concentre davantage et converge un peu plus que Dg ; (iii) la redondance des sources croît tard ; (iv) la corrélation brute concentration–HV est un artefact de scénario ; (v) la HV par génération n'est pas stockée.
Non permis : dire que la concentration « explique » l'avantage évidentiel ; dire que E et Dg sont mécaniquement équivalents ; en déduire un effet causal. Toute hypothèse issue de cette lecture (par exemple « un seuil de concentration au-delà duquel plus de concentration n'aide pas ») doit être préenregistrée dans un protocole avant d'être testée.
