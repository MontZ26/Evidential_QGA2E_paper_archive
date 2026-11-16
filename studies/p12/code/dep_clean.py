"""Dependency measure + cleaner (prototype, synthetic tests only; not wired into any engine).
Population X: (N, n_p) int team per patient; M: (n_p, n_t) 0/1 allowed teams; movable: bool mask (N,) individuals the cleaner may mutate (offspring only).
Similarity s_ij = share of patients with the same team. K_ij = 1[s_ij >= sigma] (self included), n_i = sum_j K_ij.
Individual-level entropy H_ind = ln N - mean_i ln n_i  (= Shannon entropy of cluster proportions when clusters are cliques); Dep = 1 - H_ind/ln N = mean_i ln n_i / ln N in [0,1]
(0: all individuals distinct at radius sigma; 1: all in one cluster). N_eff = sum_i 1/n_i."""
import numpy as np
def sim(X): return (X[:, None, :] == X[None, :, :]).mean(2)
def dep(X, sigma):
    N = len(X)
    if N < 2: return 0.0, float(N), np.ones(N)
    n_i = (sim(X) >= sigma).sum(1).astype(float); return float(np.log(n_i).mean() / np.log(N)), float((1.0 / n_i).sum()), n_i
def marg_entropy(X, n_t):
    return float(np.mean([-(q[q > 0] * np.log(q[q > 0])).sum() for q in (np.bincount(X[:, p], minlength=n_t) / len(X) for p in range(X.shape[1]))]))
def clean(X, M, movable, sigma, tau, rho, rng, t_max=500):
    """Greedy anti-consensus mutation of movable individuals until Dep <= tau or t_max steps. Returns (X', log)."""
    X = X.copy(); n_p, n_t = M.shape; log = []
    for it in range(t_max):
        d, neff, n_i = dep(X, sigma); log.append(d)
        if d <= tau: break
        cand = np.flatnonzero(movable & (n_i > 1))
        if len(cand) == 0: break
        S = sim(X); i = cand[np.lexsort((cand, -np.array([(S[c] >= sigma).sum() for c in cand]) ))][0]   # largest n_i, ties by index
        S[i, i] = -1; j = int(np.argmax(S[i])); agree = np.flatnonzero(X[i] == X[j]); k = max(1, int(np.ceil(rho * len(agree))))
        pick = rng.choice(agree, size=min(k, len(agree)), replace=False); cnt = np.stack([np.bincount(X[:, p], minlength=n_t) for p in range(n_p)])
        for p in pick:
            allowed = np.flatnonzero(M[p] == 1); allowed = allowed[allowed != X[i, p]]
            if len(allowed) == 0: continue
            c = cnt[p][allowed]; X[i, p] = allowed[np.flatnonzero(c == c.min())[rng.randint(0, int((c == c.min()).sum()))]]   # least frequent allowed team
    else: log.append(dep(X, sigma)[0])
    return X, log
