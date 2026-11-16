# Rapport final — P2 étape 2 : QGA à deux amplitudes (QGA2) contre NSGA-II
Protocole : v1.5-candidat gelé le 5 nov. 2026 (empreintes SHA-256 dans `p2s2_freeze.txt`). Graines confirmatoires 3820-3919 (n = 100), 6 scénarios, 600 jobs, aucun infaisable, aucune graine exclue, aucun enregistrement descriptif manquant. Analyse exécutée une seule fois (`an_p2s2_final.py`). Dépôt GitHub non touché.

## 1. Résultat confirmatoire (famille de 3 tests Wilcoxon bilatéraux, Holm)
Contraste = HV_T(QGA2) − HV_T(NSGA-II standard), agrégat par graine sur les 6 scénarios.
| Hypothèse | Monde | Moyenne | IC bootstrap 95 % | Graines négatives | p Holm |
|---|---|---|---|---|---|
| H-S2.1 | T (vérité) | −0,1321 | [−0,1353 ; −0,1290] | 100/100 | 1,2e-17 |
| H-S2.2 | F0\|N | −0,1206 | [−0,1242 ; −0,1170] | 100/100 | 1,2e-17 |
| H-S2.3 | F0\|DRI_exp | −0,1220 | [−0,1251 ; −0,1189] | 100/100 | 1,2e-17 |
Les trois hypothèses sont confirmées **en faveur du NSGA-II standard** : à budget d'évaluations identique (6 040), son hypervolume est supérieur dans les 100 graines et les 3 mondes. Le QGA2 n'est pas supérieur. HV moyens (vrai monde) : QGA2 0,540 / 0,526 / 0,527 ; NSGA-II 0,672 / 0,647 / 0,649 (T / F0|N / F0|DRI_exp). Cela correspond au sens observé au pilote.

## 2. Descriptif (aucune p-valeur lue comme confirmation)
- **Élitisme (variante appariée NSGA-II sans fusion parents-descendants)** : NSGA-II apparié − NSGA-II standard = −0,166 (T), −0,155 (F0|N), −0,155 (F0|DRI_exp), ICs étroits. QGA2 − NSGA-II apparié = +0,033 (T), +0,035 (F0|N), +0,033 (F0|DRI_exp), ICs excluant 0. Lecture prudente : dans cette implémentation, la grande majorité de l'écart au NSGA-II standard est associée au remplacement élitiste ; face à un NSGA-II non élitiste, le QGA2 obtient un hypervolume supérieur. Ce n'est pas l'effet isolé de l'opérateur de variation : ce sont deux mécanismes d'évolution différents (les paramètres de variation ont été réglés sur la version élitiste).
- **Perte due à l'incertitude** L = HV(T) − HV(F0|N) : QGA2 0,0141 [0,0106 ; 0,0176] ; NSGA-II 0,0256 [0,0233 ; 0,0279] ; apparié 0,0151 [0,0130 ; 0,0174]. Différence de robustesse QGA2 − NSGA-II = −0,0115 [−0,0158 ; −0,0072] : en valeur absolue le QGA2 perd moins, mais à partir d'un niveau d'hypervolume nettement plus bas (perte relative d'environ 2,6 % contre 3,8 %). Contre l'apparié : −0,0011 [−0,0052 ; +0,0030], indistinguable de 0.
- **Part récupérée par l'acquisition R_o** : QGA2 0,07 [−0,22 ; 0,29] (non interprétable) ; NSGA-II 0,094 [0,009 ; 0,171] ; apparié 0,164 [0,021 ; 0,295]. L'acquisition DRI_exp récupère au plus une faible part de la perte, quel que soit l'optimiseur.
- **Sensibilité population entière** : écarts QGA2 − NSGA-II −0,132 / −0,120 / −0,122, quasi identiques à l'analyse principale.
- **ΓHV (écart front optimiste/pessimiste)** : plus faible sous l'état DRI_exp que N pour les trois optimiseurs (QGA2 0,203→0,165 ; NSGA-II 0,229→0,187).
- **HV dans le monde bas** : NSGA-II 0,569 (F0|N) et 0,590 (DRI_exp) ; QGA2 0,462 et 0,481 ; apparié 0,431 et 0,449.
- **Temps moyen par recherche** : QGA2 ≈ 3,7 s ; NSGA-II standard ≈ 5,4 s ; apparié ≈ 3,3 s.
- Analyse B (HV dans le monde de recherche) et convergence : produites dans `p2s2_final_analysis.json` (non commentées ici).

## 3. Limites déclarées
κ = 0 ; NSGA-II réglé sur 3 jeux (J2 retenu), QGA2 non réglé ; QGA2 non élitiste par construction héritée de P1-M ; instances synthétiques ; Ā non calibrée ; budget égal d'évaluations ne signifie pas coût égal ; comparaison limitée aux configurations étudiées.

## 4. Déviations et incidents (aucun n'a modifié une hypothèse, un paramètre ou une règle d'analyse)
1. Le job a été étendu avant le gel (enregistrements descriptifs : monde de recherche, monde bas, ΓHV, convergence) ; les fronts confirmatoires sont identiques à ceux du pilote (vérifié, `p2s2_verify_ext.json`).
2. Les tests S1-S10 ont été relancés sur le code final avec les paramètres a priori J1 par défaut des tests (le run utilise J2) ; S1, S8, etc. ne dépendent pas de ces paramètres. Le test d'origine `p2s2_tests.py` échoue désormais sur son assertion de plage de graines (3800-3809 seulement) car le code autorise aussi 3810-3819 : la copie `p2s2_tests_finalcode.py` a été utilisée.
3. Le run a été interrompu plusieurs fois (redémarrage du conteneur, arrêt des processus d'arrière-plan). Deux arrêts de tranche sont tombés pendant l'écriture non atomique du fichier de résultats, détruisant environ 80 jobs terminés ; les jobs complets ont été récupérés avec `salvage_conf.py` et les jobs manquants recalculés (jobs déterministes ; 48 jobs communs aux deux sources étaient identiques). Le runner gelé n'a pas été modifié. Détails dans `p2s2_run_notes.txt`.
4. Un premier fichier de réglage avait été écrit par erreur dans le dossier de données du dépôt (chemin relatif) ; il a été déplacé, le dépôt est resté propre et rien n'a été commis.

## 5. Conclusion honnête
Résultat négatif confirmé pour la supériorité du QGA2 face à un NSGA-II élitiste standard. Le résultat descriptif le plus informatif est que cet écart est surtout associé à l'élitisme : le QGA2 non élitiste dépasse un NSGA-II non élitiste. Aucune promesse de publication.
