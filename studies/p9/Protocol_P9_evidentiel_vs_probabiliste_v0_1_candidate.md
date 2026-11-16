# P9 v0.1 — Évidentiel (données + recherche) contre probabiliste (données + recherche) — CANDIDAT, non gelé, non autorisé
Date : 9 novembre 2026. Demande de l'auteur (17:59) : comparer « couche de données évidentielle + couche de recherche évidentielle » à « couche de données probabiliste + couche de recherche probabiliste ». Les paramètres ci-dessous sont des valeurs par défaut proposées ; aucune exécution avant confirmation écrite de l'auteur. Code P4/P5/P7/P8 gelé, inchangé ; dépôt GitHub intact.

## 1. Question et estimand primaire
L'intégration évidentielle (couche I évidentielle + V1) est-elle meilleure que l'intégration probabiliste (couche I moyenne probabiliste + V0c) en HV oracle ?
Primaire : G = Y_E − Y_P (moyenne par graine sur 6 scénarios), H0 : G = 0, bilatéral, α = 0,05, bootstrap-t apparié sur graines (B = 20000, règles P6/P8). Résultat négatif ou nul = résultat valide.

## 2. Bras (même instance, graine, décodeur, budget 6 040 exact, mêmes paramètres GA C0b et P7 gelés)
- **E** : monde nominal évidentiel (p1m, Dempster/Yager) + modèle de recherche V1 (= bras D de P8).
- **P** : monde probabiliste (chaque source de A — document, supervision, historique — affaiblie par Shafer puis transformée en BetP, moyenne à poids égaux, A = 0,25 + 0,60·moyenne sur cellules certifiées ; S = BetP des votes, comme G-D) + modèle V0c.
- **X** (croisé) : monde probabiliste + V1. **D′** (croisé) : monde évidentiel + V0c.
- Références classiques (sans couche II) : **B** (évidentiel) et **B_p** (probabiliste), GA C0b.
Pour décomposer : effet de la représentation des données = E − X et D′ − P ; effet de la représentation de la recherche = E − D′ et X − P ; interaction de représentation = E − D′ − X + P (descriptifs avec IC95 %).

## 3. Graines, taille, séparation
Graines confirmatoires 9000–9199 (n = 200, nouvelles : aucune graine P5–P8 réutilisée, les coquilles P8 ne servent pas de données) ; test technique 8900–8909 (G-I : budgets exacts, pas de fuite de l'oracle, A=…). Graine d'analyse 9802. n = 200 par défaut (variance du contraste D−D′ de P8 : voir rapport P8 ; puissance à vérifier avant lancement sur les données P8 sans les relire pour de nouveaux résultats).

## 4. Gates
G-I (tests d'interface comme P8) ; G-P : le monde probabiliste est vérifié contre une réimplémentation indépendante (valeurs BetP et moyenne) avant tout run ; gel (hash protocole + code + paramètres) avant la première coquille confirmatoire ; précontrôle avant analyse ; analyse exécutée une seule fois.

## 5. Limites déclarées d'avance
Une seule famille d'instances (dérivée de Solomon), ordre de visite fixe ; la comparaison porte sur ces deux implémentations (la moyenne probabiliste des sources n'est pas la seule alternative probabiliste, par exemple un produit bayésien) ; V0c n'est pas apparié en concentration à V1 (P8/G-C) : une différence E − P ne distinguera pas structure évidentielle et concentration. Le contraste mesure la performance en simulation (vérité cachée) ; novelty non établie.

## 6. Décisions à confirmer (défauts proposés)
D9-1 bras E/P/X/D′/B/B_p (§2) ; D9-2 primaire E − P bilatéral α = 0,05, sans famille Holm, secondaires descriptifs ; D9-3 moyenne probabiliste à poids égaux comme version probabiliste de la couche I ; D9-4 graines 9000–9199, n = 200 ; D9-5 autorisation d'enchaîner G-I, G-P, gel, confirmatoire, analyse et rapport sans arrêt si les gates passent.
