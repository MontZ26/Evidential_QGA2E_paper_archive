"""P8 descriptive controls (amendment item 6): dependence/ablation/cautious/duplicate/B-cal variants of layer I, arms B-type (GA) and D-type (V1), seeds 8200-8229, SC6.
Descriptive/exploratory only; does not alter confirmatory results. Usage: python p8_ctrl.py OUTDIR"""
import sys, os, json, glob
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, p8
sys.path.insert(0, p8.BASE + "/p7/code"); import p7_g0 as G0
P = p8.P; B8 = p8.BASE + "/p8"; A_, N_, T_ = 1, 2, 3
def weak(m, r): return {x: (r * v if x != T_ else 1 - r * (1 - v)) for x, v in m.items()}
def srcs(I, t, k, hx, hn):
    ev = I["ev"]; cov = bool(ev["doc_cov"][t, k]) and (not I["unv"][t, k]) and I["CT"][t, k] == 1
    doc = {A_: 0.5, T_: 0.5} if cov else {T_: 1.0}; y = float(ev["yhat"][t, k]); s = abs(2 * y - 1)
    sup = {A_: s, T_: 1 - s} if y >= 0.5 else {N_: s, T_: 1 - s}; his = {A_: hx / (hn + 2.0), N_: (hn - hx) / (hn + 2.0), T_: 2.0 / (hn + 2.0)}
    return dict(doc=weak(doc, P.R_DOC), sup=weak(sup, P.R_SUP), his=weak(his, P.R_HIS))
def combine(lst, rule):
    m = lst[0]
    for x in lst[1:]: m = G0.conj(m, x) if rule == "conj" else G0.cautious(m, x, 2)
    return m
def world_variant(I, var):
    ev = I["ev"]; n_t = I["n_t"]; A = np.zeros((n_t, P.NK)); Ks = []; wd = []; cert = I["CT"] == 1
    for t in range(n_t):
        for k in range(P.NK):
            if not cert[t, k]: continue
            s = srcs(I, t, k, ev["h_x"][t, k], ev["h_n"][t, k])
            lst, rule = {"nosup": ([s["doc"], s["his"]], "conj"), "nohist": ([s["doc"], s["sup"]], "conj"), "cautious": ([s["doc"], s["sup"], s["his"]], "cautious"), "dup": ([s["doc"], s["sup"], s["his"], s["his"]], "conj")}[var]
            m = combine(lst, rule); Kc = m.get(0, 0.0); mA = m.get(A_, 0.0); mT = m.get(T_, 0.0) + Kc
            A[t, k] = 0.25 + 0.60 * (mA + mT / 2); Ks.append(Kc); wd.append(mT)
    return A, dict(mean_K=float(np.mean(Ks)), mean_width=float(np.mean(wd)))
def job(a):
    sc, seed = a; path = f"{OUT}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if I["feasible"]:
        W = p8.worlds_for(I); nomS = W["nom"][1]; tau = json.load(open(B8 + "/p8_tau.json")); bc = tau["bcal"]; res = {}
        for var in ("nosup", "nohist", "cautious", "dup", "bcal"):
            if var == "bcal": A = np.where(I["CT"] == 1, np.clip(bc["slope"] * W["nom"][0] + bc["intercept"], 0.0, 1.0), 0.0); dg = {}
            else: A, dg = world_variant(I, var)
            w = (A, nomS); res[var] = dict(diag=dg, Bv=p8.run_one(I, w, None, wd=W)["hv_oracle"], Dv=p8.run_one(I, w, "V1", wd=W)["hv_oracle"])
        out["variants"] = res
    json.dump(out, open(path, "w")); return path
OUT = None
if __name__ == "__main__":
    OUT = sys.argv[1]; assert os.path.isabs(OUT); os.makedirs(OUT, exist_ok=True)
    jobs = [(sc, s) for s in range(8200, 8230) for sc in p8.SC6]
    with Pool(2, initializer=lambda o: globals().__setitem__("OUT", o), initargs=(OUT,)) as pool: pool.map(job, jobs, chunksize=1)
    # summary vs reference B, D from confirmatory shards (same seeds)
    ref = {}
    for f in glob.glob(B8 + "/runs/conf/*__82[0-2]?.json"):
        r = json.load(open(f)); ref[(r["sc"], r["seed"])] = r
    rows = {}
    for f in glob.glob(OUT + "/*__*.json"):
        r = json.load(open(f))
        if r.get("feasible"): rows[(r["sc"], r["seed"])] = r
    seeds = sorted({s for _, s in rows}); summ = {}
    for var in ("nosup", "nohist", "cautious", "dup", "bcal"):
        for arm, key, refarm in (("B", "Bv", "B"), ("D", "Dv", "D")):
            d = np.array([np.mean([rows[(sc, s)]["variants"][var][key] - ref[(sc, s)]["conds"][refarm]["hv_oracle"] for sc in p8.SC6]) for s in seeds]); rng = np.random.RandomState(9801); bm = d[rng.randint(0, len(d), (5000, len(d)))].mean(1)
            summ[f"{arm}:{var}-ref"] = dict(mean=float(d.mean()), ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))], share_pos=float((d > 0).mean()))
        summ[f"diag:{var}"] = {k: float(np.mean([rows[(sc, s)]["variants"][var]["diag"].get(k, np.nan) for sc in p8.SC6 for s in seeds])) for k in ("mean_K", "mean_width")}
    json.dump(dict(n_seeds=len(seeds), note="descriptive/exploratory, 30 seeds, not confirmatory", summary=summ), open(B8 + "/p8_controls_summary.json", "w"), indent=1); print(json.dumps(summ, indent=1))
