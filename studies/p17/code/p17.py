"""P17 engine: marginal-evidence selection (SEL4 / SELW / SELR) on top of the P15 targets. Frozen modules UNMODIFIED; runtime patch of X.select_next inside try/finally.
Reference set S = first front (3 real objectives) of the parent population at the start of the generation (same sources as the target); leave-one-out gain G(x) = u(S_-x) - u(S_-x U {x}); selection objective U = -G (minimised)."""
import sys, math, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p15/code")
import numpy as np, p15, p14, p10, p9, p8, p7
from scipy.stats import rankdata
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds17:
    def __contains__(self, s): return (11200 <= s <= 11299 or 11500 <= s <= 11514 or 10400 <= s <= 10401 or s in (9290, 7000, 5200))
P.ALLOWED_SEEDS = _Seeds17()
ARMS17 = ["E", "DA", "Dp", "Dg", "DA+SEL4", "DA+SELW", "DA+SELR", "Dp+SEL4"]
BASEARM = {"E": "E", "DA": "DA", "Dp": "Dp", "Dg": "Dg", "DA+SEL4": "DA", "DA+SELW": "DA", "DA+SELR": "DA", "Dp+SEL4": "Dp"}
SELMODE = {"DA+SEL4": "SEL4E", "DA+SELW": "SELW", "DA+SELR": "SELR", "Dp+SEL4": "SEL4P"}
LAMW = 0.5
# ------------------------------------------------------------------ evidential marginal gain (exact, vectorised)
def base_E(src, M, w, sigma, lam):
    nt, nM = p15.eff_counts(src, M, sigma, lam); alpha = 1.0 / (1.0 + lam * (nM - 1)); om = -math.log(1 - w)
    D = 1.0 + (np.exp(om * nt) - 1).sum(1); return nt, nM, alpha, om, D
def gain_E(src, M, w, sigma, lam, cand, member_pos):
    """G(x) for every candidate row of cand; member_pos[c] = row of src that IS candidate c (leave-one-out) or -1"""
    nt, nM, alpha, om, D = base_E(src, M, w, sigma, lam); N, n_p = src.shape; C = len(cand); mut = M.sum(1) >= 2; mp = np.asarray(member_pos)
    agree = (cand[:, None, :] == src[None, :, :]); sim = agree.mean(2) >= sigma
    for c in range(C):
        if mp[c] >= 0: sim[c, mp[c]] = False
    nb = agree & sim[:, :, None]; ntx = nt[np.arange(n_p)[None, :], cand]                       # [C,n_p]
    nbc = nb.sum(1)
    a_add = 1.0 / (1.0 + lam * nbc); t_add = np.where(nb, 1.0 / (1.0 + lam * nM[None]) - alpha[None], 0.0).sum(1)
    d_add = a_add + t_add
    t_rem = np.where(nb, 1.0 / (1.0 + lam * (np.maximum(nM, 2)[None] - 2)) - alpha[None], 0.0).sum(1)
    ak = np.zeros((C, n_p)); isM = mp >= 0
    if isM.any(): ak[isM] = alpha[mp[isM]]
    d_rem = -ak + t_rem; d = np.where(isM[:, None], d_rem, d_add)
    Dn = D[None, :] + np.exp(om * ntx) * (np.exp(om * d) - 1.0)
    mnew = (1.0 / Dn)[:, mut].mean(1); mS = float((1.0 / D)[mut].mean())
    return np.where(isM, mnew - mS, mS - mnew)
def ref_gain_E(src, M, w, sigma, lam, cand, member_pos):
    """brute force through p15.da_model (test reference)"""
    mS = p15.da_model(src, M, w, sigma, lam)[1]["m_theta"]; G = np.empty(len(cand))
    for c in range(len(cand)):
        if member_pos[c] >= 0:
            rest = np.delete(src, member_pos[c], 0); mrest = 1.0 if len(rest) == 0 else p15.da_model(rest, M, w, sigma, lam)[1]["m_theta"]; G[c] = mrest - mS
        else: G[c] = mS - p15.da_model(np.vstack([src, cand[c][None]]), M, w, sigma, lam)[1]["m_theta"]
    return G
# ------------------------------------------------------------------ probabilistic marginal gain (entropy of the V0c target)
def _counts(src, n_p, n_t):
    cnt = np.zeros((n_p, n_t))
    for r in src: np.add.at(cnt, (np.arange(n_p), r), 1.0)
    return cnt
def _H(cnt, n, M, w, mut):
    U = M / M.sum(1, keepdims=True); q = (w * cnt / n + (1 - w) * U) if n > 0 else U
    qq = np.where(q > 0, q, 1.0); return float((-(q * np.log(qq)).sum(1))[mut].mean())
def gain_P(src, M, w, cand, member_pos):
    N, n_p = src.shape; n_t = M.shape[1]; mut = M.sum(1) >= 2; cnt = _counts(src, n_p, n_t); H0 = _H(cnt, N, M, w, mut); G = np.empty(len(cand)); ar = np.arange(n_p)
    for c in range(len(cand)):
        x = cand[c]; c1 = cnt.copy()
        if member_pos[c] >= 0: c1[ar, x] -= 1.0; G[c] = _H(c1, N - 1, M, w, mut) - H0
        else: c1[ar, x] += 1.0; G[c] = H0 - _H(c1, N + 1, M, w, mut)
    return G
def ref_gain_P(src, M, w, cand, member_pos):
    mut = M.sum(1) >= 2
    def Hs(s):
        if len(s) == 0: U = M / M.sum(1, keepdims=True); q = U
        else: q = p7.population_model(s, M, w, "V0c")[0]
        qq = np.where(q > 0, q, 1.0); return float((-(q * np.log(qq)).sum(1))[mut].mean())
    H0 = Hs(src); G = np.empty(len(cand))
    for c in range(len(cand)):
        if member_pos[c] >= 0: G[c] = Hs(np.delete(src, member_pos[c], 0)) - H0
        else: G[c] = H0 - Hs(np.vstack([src, cand[c][None]]))
    return G
# ------------------------------------------------------------------ selection
def sources_index(fits_parents):
    fr = X.nds(fits_parents); return list(fr[0]) if fr[0] else [0]
def selw_select(pop_fits3, U, size, lam=LAMW):
    n = len(U); fronts = X.nds(pop_fits3); rF = np.zeros(n); cd = np.zeros(n)
    for k, f in enumerate(fronts):
        d = X.G["crowding_dist"](pop_fits3, f)
        for i in f: rF[i] = k + 1; cd[i] = d[i]
    rU = rankdata(U, method="average")
    def nrm(r): return (r - 1) / (r.max() - 1) if r.max() > 1 else np.zeros_like(r)
    score = (1 - lam) * nrm(rF) + lam * nrm(rU); order = np.lexsort((np.arange(n), -cd, score)); return list(order[:size])
def make_select17(I, prm, mode, orig, log, rs):
    M = I["M"]; w = prm["w"]
    def sel(pop, fits, size):
        if len(pop) == size: return orig(pop, fits, size)                       # initial selection (POP -> POP): untouched
        POP = size; S_idx = sources_index(fits[:POP]); src = pop[S_idx]; mp = -np.ones(len(pop), int)
        for k, i in enumerate(S_idx): mp[i] = k
        if mode == "SEL4E": G = gain_E(src, M, w, prm["sigma"], prm["lam"], pop, mp); Uo = -G
        elif mode == "SEL4P": G = gain_P(src, M, w, pop, mp); Uo = -G
        elif mode == "SELW": G = gain_E(src, M, w, prm["sigma"], prm["lam"], pop, mp); Uo = -G
        elif mode == "SELR": G = np.zeros(len(pop)); Uo = rs.rand(len(pop))
        else: raise ValueError(mode)
        if mode == "SELW": s = selw_select(fits, Uo, size)
        else: s = orig(pop, np.column_stack([fits, Uo]), size)
        s3 = orig(pop, fits, size); f4 = X.nds(np.column_stack([fits, Uo]))
        log.append(dict(S_size=len(S_idx), front4_share=len(f4[0]) / len(pop), divergence=1.0 - len(set(s) & set(s3)) / size, G_sel=float(np.mean(G[list(s)])), G_all=float(np.mean(G)), finite=bool(np.isfinite(Uo).all())))
        return s
    return sel
def run_arm17(I, arm, prm, wd=None):
    W = p9.worlds9(I) if wd is None else wd; base = BASEARM[arm]; mode = SELMODE.get(arm)
    if mode is None: r = p15.run_arm15(I, base, prm, W); r["sel_log"] = []; return r
    log = []; rs = P.rs(I["sc"], I["seed"], "p17_selr"); orig = X.select_next; X.select_next = make_select17(I, prm, mode, orig, log, rs)
    try: r = p15.run_arm15(I, base, prm, W)
    finally: X.select_next = orig
    r["sel_log"] = log; return r
def task17(sc, seed, arms, prm):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm17(I, a, prm, W) for a in arms}; return out
