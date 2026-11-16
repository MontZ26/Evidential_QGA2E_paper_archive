# Amendement P8 v0.2.1 — décisions confirmées et autorisation d'exécution

Auteur : Dr Montassar Zaghdoud. Enregistré par l'assistant le 2026-11-09 (Africa/Lagos). Protocole : `/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p8/Protocol_P8_v0_2_1_candidate.md` (SHA-256 28c94157de7e17f28a74f3d38614c27c098dfb25acecf97440fe3efc1892066e).

## 1. Autorisation écrite de l'auteur (citations)
- 06:51 : « Ok launch new P8 version with my confirmation for all decisions! » → D8-1 à D8-10 confirmées avec les valeurs par défaut du protocole.
- 06:51 : « without stop, I am going to teach, I will be out of door for many hours. » → D8-10 : enchaînement G-I, G-C, G-Y, gel, confirmatoire, analyse et rapport sans arrêt tant que les gates passent.

## 2. Précisions opérationnelles écrites AVANT tout résultat P8 de calibration, pilote ou confirmatoire
1. D8-9 : l'auteur n'a pas fixé n. Règle littérale du protocole : n = n requis (grille {100,150,200,300}) issu du dimensionnement ; pas de n=200 par défaut. Le dimensionnement porte sur les trois contrastes de la famille de Holm, α=0,05 par contraste, m=1 ; n_requis = max des trois, plafonné à 300.
2. Arrêt G-Y : si le n requis pour le contraste PRIMAIRE I_V1 dépasse 300 (grille), arrêt avec rapport descriptif du pilote ; si seul un contraste secondaire de la famille dépasse 300, exécution à n=300 avec mention « sous-dimensionné » pour ce contraste.
3. Monde non informatif (couche I off) : A_hat = 0,55 sur cellules certifiées (CT==1), 0 sur les autres (comme le monde nominal) ; S_hat = 0,5 partout.
4. V0c-τ : grille w ∈ {0,10;0,15;…;0,95;0,99;0,999} ; choix du w dont l'entropie moyenne du modèle (mesurée toutes les 10 générations, bras D' nominal, graines de calibration 8100–8114, scénarios SC3) est la plus proche de celle de V1 (bras D, mêmes graines, config P7 gelée partagée). Si aucun w de la grille n'égale V1, on prend le plus proche et on le déclare.
5. Bras V2 de sensibilité : D_V2 (nominal + V2) exécuté ; D_V2 − D' rapporté, descriptif.
6. Contrôles de dépendance (§6 du protocole) et B-cal : exécutés sur le bras B (GA classique + monde modifié) et le bras D, descriptifs, sur les 30 premières graines confirmatoires 8200–8229 seulement. Définitions : sans supervision (source retirée de la conjonctive), sans historique, combinaison de la couche I par règle prudente de Denœux (poids canonique de chaque source), historique dupliquée (source redondante). B-cal : régression affine A_vrai ~ A_nom sur les cellules certifiées des graines de calibration 8100–8114, appliquée au monde nominal.
7. Paramètres : GA classique = C0b de p5_tuned.json ; couche II = p7_tuned.json (partagé V1/V0c/V2). Aucun nouveau réglage hors τ.
8. Agrégation par graine : moyenne des HV oracle sur les 6 scénarios SC6 ; graines confirmatoires 8200…8200+n−1 ; bootstrap-t apparié sur les graines, B=20000, graine d'analyse 9801 ; Holm sur (I_V1, I_V0c, G_τ) ; exclusion d'une graine seulement si un scénario est infaisable ou manquant (pour tous les bras, déclarée).
9. Réévaluation oracle : tous les vecteurs d'affectation de l'archive finale de chaque bras sont réévalués sous l'oracle ; HV de référence (1.2, 1.2, 1.2) ; les archives (affectations + objectifs recherche et oracle) sont sauvegardées.
10. Capture des affectations : sous-classe d'Archive enregistrant l'instance créée (comportement identique, vérifié par G-I) ; aucun fichier P4/P5/P7 modifié.
