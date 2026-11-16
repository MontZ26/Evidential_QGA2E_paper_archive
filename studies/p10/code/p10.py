"""P10 engine (Protocol P10 v0.2 + Amendement 10 nov. 01:40): QGA2-E (P3 elitist, 40 + 150x40 = 6040 evaluations) with a multi-source rotation target.
Frozen P3/P5/P7/P8/P9/P11 modules are used UNMODIFIED; qga_pareto(elitist=True, archive=True) is re-implemented here as a copy with hooks that are inert when rule=None and dec=None (G-Q1 checks bit-for-bit equality).
Layer II target (sources = individuals of the first non-dominated front of the current population):
  q = floor_renorm(population_model(sources, M, w, rule), M, eps)  with rule 'V0c' (probabilistic: w*freq + (1-w)*uniform) or 'V1' (Dempster of P7);
  rotation of individual i: theta_i <- clip(theta_i + delta*(q - onehot(x_i)), 0, pi/2) * M. With ONE source and q = one-hot (w -> 1, eps = 0) this is exactly the QGA2-E rotation delta*(onehot(best) - onehot(x_i)) (G-Q0/G-Q1).
DEC (optional, parameters of P11 unchanged): cap on population U already-repaired children, repair of the unevaluated collapsed child only, redraw (r_max) of the collapse draws if the repair fails."""
import sys, math, random, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p12/code")
import numpy as np, p11, p9, p8, p7
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds10:
    def __contains__(self, s): return (9290 <= s <= 9299 or 9300 <= s <= 9314 or 9350 <= s <= 9379 or 9400 <= s <= 9599 or s == 9803 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds10()
POP, GEN = P.POP, P.GEN
ARMS10 = {"E": ("nom", "V1", False), "P": ("pavg", "V0c", False), "X": ("pavg", "V1", False), "Dp": ("nom", "V0c", False), "A": ("non", None, False), "B": ("nom", None, False), "Bp": ("pavg", None, False),
          "E_DEC": ("nom", "V1", True), "P_DEC": ("pavg", "V0c", True)}
def make_dec10(I, dp): return p11.Dec(dp["sigma"], dp["n_max"], dp["rho_max"], dp["r_max"], P.rs(I["sc"], I["seed"], "p10_dec"))
def target(src, M, w, rule, eps):
    Pn, md = p7.population_model(src, M, w, rule); return K.floor_renorm(Pn, M, eps), md
def run_q(I, rule=None, w=0.5, eps=0.02, dec=None, diag=False, single=False):
    n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed); ev = X.Cnt(I); delta = P.DELTA; mutable = M.sum(1) >= 2
    th, decs, dr, rng = X.init_qga(I)
    if dec is not None: decs = p11._init_clean(decs, dec, M, mutable, I)
    fits = np.array([ev(decs[i]) for i in range(POP)]); arch = X.Arch(); arch.add(decs, fits); dyn = []
    def rec(g, src=None, q=None):
        d = p11.dep_stats(decs, 0.7, n_t); d["gen"] = g
        if src is not None and len(src) > 1: ds = p11.dep_stats(src, 0.7, n_t); d["src_n"] = int(len(src)); d["src_dep"] = ds["dep"]; d["src_neff"] = ds["neff"]; d["src_nmax"] = ds["n_max_obs"]
        elif src is not None: d["src_n"] = 1
        if q is not None:
            mut = M.sum(1) >= 2; qq = np.where(q > 0, q, 1.0); d["q_ent"] = float(np.mean(-(q * np.log(qq)).sum(1)[mut])); d["q_max"] = float(np.mean(q.max(1)[mut]))
        dyn.append(d)
    if diag: rec(0)
    for g in range(GEN):
        if g == 0: sel = X.select_next(decs, fits, POP); th, decs, fits = th[sel], decs[sel], fits[sel]
        fr = X.nds(fits); q = None; src = None
        if rule is None: best = decs[fr[0][0] if fr[0] else 0].copy()
        else:
            src = decs[fr[0]] if fr[0] else decs[:1]
            if single: src = src[:1]
            q, md = target(src, M, w, rule, eps)
        nth = np.empty_like(th); new = np.empty_like(decs)
        for i in range(POP):
            if rule is None: nth[i] = X._rot(th[i], decs[i], best, n_t, M, delta)
            else: nth[i] = np.clip(th[i] + delta * (q - np.eye(n_t)[decs[i]]), 0.0, P.HALF) * M
            ux = rng.rand(n_p, n_t); ur = rng.rand(n_p); new[i] = P.collapse_r(nth[i], M, ux, ur)
            if dec is not None:
                base = np.vstack([decs, new[:i]]) if i else decs; tries = 0; cand, ok_, _ = dec.repair(base, new[i], M, mutable)
                while not ok_ and tries < dec.r_max:
                    tries += 1; dec.c["regen"] += 1; ux = rng.rand(n_p, n_t); ur = rng.rand(n_p); new[i] = P.collapse_r(nth[i], M, ux, ur); cand, ok_, _ = dec.repair(base, new[i], M, mutable)
                if not ok_: dec.c["violations"] += 1
                new[i] = cand
        nf = np.array([ev(new[i]) for i in range(POP)]); arch.add(new, nf)
        ath = np.concatenate([th, nth]); ad = np.vstack([decs, new]); af = np.vstack([fits, nf]); sel = X.select_next(ad, af, POP); th, decs, fits = ath[sel], ad[sel], af[sel]
        if diag: rec(g + 1, src, q)
    return dict(F=arch.F, D=arch.D, n_eval=ev.n, dyn=dyn, dec=(dec.c if dec else None), final_pop=decs)
def run_one10(I, arm, prm, wd=None):
    world, rule, on = ARMS10[arm]; W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W[world]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    dec = make_dec10(I, prm["dec"]) if on else None; r = run_q(Is, rule, prm["w"], prm["eps"], dec, diag=True)
    Ao, So = I["A_true"], I["S_true"]; Fo = np.array([P.evaluate(d, I, Ao, So) for d in r["D"]]) if len(r["D"]) else np.empty((0, 3))
    return dict(n_eval=r["n_eval"], hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(r["F"])), F_search=r["F"].tolist(), F_oracle=Fo.tolist(), D=r["D"].tolist(), dyn=r["dyn"], dec=r["dec"])
def task10(sc, seed, arms, prm, with_c0=True):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_one10(I, a, prm, W) for a in arms}
    if with_c0: out["conds"]["C0"] = p9.p8.run_one(I, "nom", None, None, None, W) | {}
    for c in out["conds"].values(): c.pop("snap", None)
    return out
