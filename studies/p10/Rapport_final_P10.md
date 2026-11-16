# Rapport final P10 — évidentiel contre probabiliste dans QGA2-E (avec volet DEC descriptif)
Date : 10 novembre 2026. Autorisation : Dr Montassar Zaghdoud (« I confirm all decisions », 01:40 ; D10-6 = non, D10-9 = descriptif, D10-8 = oui). Protocole P10 v0.2 (SHA 965cbbdc…233a), gel p10_freeze1.txt. n = 200 graines (9400–9599) × 6 scénarios, budget 6 040, HV oracle moyen sur SC6 par graine, analyse unique (graine 9803), bootstrap-t apparié B = 20 000. Paramètres : w = 0,3 (bord de grille), ε = 0,02, δ = 0,05π ; DEC = paramètres P11.
Fichiers : p10_final_analysis.json (SHA 77c27d73121b3fae099f54b9733e7f15e6ed73747fecf8a5677447e54875bbc1), p10_final_stdout.txt (02e6e65b…a31ba399).

## Résultat primaire (unique, sans DEC, sans Holm)
G10 = HV(E) − HV(P) = **+0,0459**, IC95 % [+0,0444 ; +0,0473], p brut au plancher du bootstrap (5e-5), 100 % des graines positives → rejet de H0. L'intégration évidentielle (couche I nominale + cible de rotation de Dempster V1-Q) dépasse l'équivalent probabiliste (couche I moyenne des BetP + V0c-Q) dans QGA2-E. L'ampleur est plus grande qu'en P9/P11 (+0,019 à +0,028).

## HV moyens
E 0,5299 ; P 0,4840 ; X 0,5205 ; D′ 0,4861 ; A 0,4903 ; B 0,5046 ; B_p 0,5016 ; E_DEC 0,5251 ; P_DEC 0,4840 ; C0b (GA classique) 0,6362.

## Décomposition descriptive (IC95 %)
E−D′ (V1-Q contre V0c-Q, monde nominal) +0,0437 [0,0423 ; 0,0452] ; X−P (idem, monde probabiliste) +0,0365 ; E−X (couche I évidentielle sous V1-Q) +0,0093 ; D′−P (couche I sous V0c-Q) +0,0021 ; interaction E−D′−X+P +0,0072. La plus grande part de G10 vient de la règle de couche II (V1-Q contre V0c-Q), non de la couche de données.
Contre les références QGA2-E : E−B +0,0253 (la cible évidentielle améliore la rotation vers le meilleur) ; P−B_p −0,0176 (la cible probabiliste la dégrade) ; B−B_p +0,0030 ; B−A +0,0143. Contre le GA classique : E−C0b −0,1064 ; B−C0b −0,1316 (écart connu de QGA2-E).

## Diagnostics de dépendance (descriptifs, fin de run, σ = 0,7)
Sources de la cible (premier front) : E Dep 0,456, N_eff ≈ 11,6 ; P Dep 0,002, N_eff ≈ 31 ; entropie de la cible q : E 0,53 (q_max 0,85) ; P 1,46 (q_max 0,28). Les sources de V1-Q sont donc très redondantes et la cible évidentielle très concentrée ; la cible probabiliste à w = 0,3 est presque diffuse.

## Volet DEC (descriptif, hors G10 et hors Holm)
E_DEC−E −0,0048 [−0,0056 ; −0,0040] ; P_DEC−P −0,0000 [−0,0002 ; +0,0002] ; E_DEC−P_DEC +0,0411 [0,0396 ; 0,0425] (≈ 90 % de G10) ; Δ_DEC −0,0048. DEC ramène Dep de 0,456 à 0,028 (E) avec ~3 640 mutations par run, taux de violation 0,1 %, perte d'HV faible. Lecture conjointe prédéfinie : issue (i) — l'avantage évidentiel sans DEC et avec DEC existe dans les deux architectures (P5/P7 en P11 ; QGA2-E ici), et DEC pénalise légèrement plus l'évidentiel (P11 : Δ2 −0,0040 ; ici −0,0048).

## Limites déclarées
- **Concentration non appariée (D10-6 = non)** : la cible V1-Q est très concentrée (q_max 0,85) et la cible V0c-Q presque diffuse (0,28) ; l'écart de G10 est donc en partie un écart de netteté de cible, non nécessairement d'« évidence » (confusion déjà vue en P8). w = 0,3 a été choisi sur le bord de la grille par la règle neutre ; un w plus élevé pourrait rapprocher les deux cibles. Aucun ré-ajustement après résultats.
- La cible multi-sources est un composant NOUVEAU (s = q − onehot, pas δ) ; la réduction exacte à QGA2-E n'est vérifiée que dans la limite w = 1, ε = 0.
- E > B (+0,0253) : ici la couche II évidentielle améliore l'optimiseur QGA2-E de référence, contrairement à P8/P9 où elle restait sous le GA classique ; mais aucun bras QGA2-E n'approche le GA classique (−0,106), donc aucune compétitivité n'est établie.
- Dépendance génotypique (proxy), pas d'indépendance statistique démontrée ; DEC ne permet pas d'isoler un effet causal de la dépendance.
- n = 200 appliqué selon le protocole ; le dimensionnement du pilote donnait 100. p au plancher : on lit taille d'effet et IC95 % (non ajustés, percentile).
- Une seule famille d'instances, simulation à vérité cachée ; nouveauté non établie (recherche bibliographique de l'auteur). Dépôt GitHub intact ; code gelé P3/P4/P5/P7 inchangé.
