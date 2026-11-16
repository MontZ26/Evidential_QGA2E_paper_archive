"""P14 descriptive analysis. python p14_an.py precheck CONFDIR FREEZE | final CONFDIR OUT.json FREEZE (RUN ONCE). No primary, no p-values: percentile bootstrap CI95 over seeds (B=20000, tag 10803)."""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R
B14 = B + "/p14"; ARMS = ["E", "Dp", "Dg", "Es", "B", "Bt", "NSGA2", "MOEAD", "C0"]; SC = S.SC; NEV = {a: 6040 for a in ARMS}; NEV["MOEAD"] = 6030
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")): r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def usable(res):
    keep = []; excl = {}
    for s in sorted({r["seed"] for r in res.values()}):
        why = []
        for sc in SC:
            r = res.get(f"{sc}|{s}")
            if r is None: why.append(f"{sc}: missing"); continue
            if not r.get("feasible", False): why.append(f"{sc}: infeasible"); continue
            miss = [a for a in ARMS if a not in r.get("conds", {})]
            if miss: why.append(f"{sc}: missing {miss}")
        (excl.__setitem__(s, why) if why else keep.append(s))
    return keep, excl
def hv(res, keep): return {a: np.array([np.mean([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for sc in SC]) for s in keep]) for a in ARMS}
def contrasts(H):
    c = {"E-Dp": H["E"] - H["Dp"], "E-Dg(gamma=6, non-conforming)": H["E"] - H["Dg"], "Dg-Dp": H["Dg"] - H["Dp"], "E-Es": H["E"] - H["Es"], "Es-Dg": H["Es"] - H["Dg"], "Bt-B": H["Bt"] - H["B"], "E-B": H["E"] - H["B"], "Dg-B": H["Dg"] - H["B"]}
    for a in ("NSGA2", "MOEAD"): c[f"{a}-C0"] = H[a] - H["C0"]; c[f"{a}-B"] = H[a] - H["B"]; c[f"E-{a}"] = H["E"] - H[a]
    c["E-C0"] = H["E"] - H["C0"]; c["B-C0"] = H["B"] - H["C0"]; c["NSGA2-MOEAD"] = H["NSGA2"] - H["MOEAD"]; return c
def precheck(d, freeze):
    bad = []
    if not R.verify_freeze(freeze): bad.append("freeze verification failed")
    n = json.load(open(B14 + "/p14_n.json"))["n"]; res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(10400, 10400 + n)): bad.append(f"seed set {len(seeds)}")
    if len(res) != 6 * n: bad.append(f"{len(res)} shards expected {6 * n}")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append(f"infeasible {k}"); continue
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != NEV[a]: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def final(d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); keep, _ = usable(res); H = hv(res, keep); n = len(keep)
    rng = S.sub_rng("p14final", 10803); idx = rng.randint(0, n, size=(20000, n)).astype(np.int32)
    rep = dict(status="DESCRIPTIVE ONLY (D14-9): G-N failed, no primary, no test", n=n, hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, hv_oracle_sd={a: float(H[a].std(ddof=1)) for a in ARMS}, contrasts_descriptive={})
    for k, dd in contrasts(H).items():
        b = dd[idx].mean(1); rep["contrasts_descriptive"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], share_pos=float((dd > 0).mean()))
    dg = {}
    for a in ("E", "Dp", "Dg", "Es", "B", "Bt"):
        rows = [res[f"{sc}|{s}"]["conds"][a] for sc in SC for s in keep]; ser = lambda key: [np.mean([x[key] for x in r["dyn"] if key in x]) for r in rows]
        dg[a] = {k: float(np.nanmean(ser(k))) for k in ("q_ent", "q_max", "marg_ent", "dep", "neff") if rows[0]["dyn"] and any(k in x for x in rows[0]["dyn"])}
    rep["gn_diagnostics_descriptive"] = dg; save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
