"""P8 analysis. Usage:
  python p8_an.py pilot PILOT_DIR OUT_DIR           sizing for the three Holm contrasts (alpha 0.05, m=1), writes p8_n.json decision
  python p8_an.py precheck CONF_DIR FREEZE
  python p8_an.py final CONF_DIR OUT.json FREEZE    (RUN ONCE)"""
import sys, os, json, math, glob
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6/code")
import numpy as np
import p6_stats as S
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"); import run_p1m as R
B8 = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p8"
MAIN = ["A", "B", "C", "D", "Cp", "Dp", "Dt", "DV2"]; SC = S.SC
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")):
        r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def usable(res):
    seeds = sorted({r["seed"] for r in res.values()}); keep = []; excl = {}
    for s in seeds:
        why = []
        for sc in SC:
            r = res.get(f"{sc}|{s}")
            if r is None: why.append(f"{sc}: missing"); continue
            if not r.get("feasible", False): why.append(f"{sc}: infeasible"); continue
            miss = [a for a in MAIN if a not in r.get("conds", {})]
            if miss: why.append(f"{sc}: missing {miss}")
        if why: excl[s] = why
        else: keep.append(s)
    return keep, excl
def hv_matrix(res, keep): return {a: np.array([np.mean([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for sc in SC]) for s in keep]) for a in MAIN}
def contrasts(H):
    return {"I_V1": H["D"] - H["B"] - H["C"] + H["A"], "I_V0c": H["Dp"] - H["B"] - H["Cp"] + H["A"], "G_tau": H["D"] - H["Dt"]}
def secondary(H):
    return {"D-B": H["D"] - H["B"], "D-C": H["D"] - H["C"], "B-A": H["B"] - H["A"], "C-A": H["C"] - H["A"], "D-Dp(V1-V0c|nominal)": H["D"] - H["Dp"], "Dp-Dt(V0c-V0ctau)": H["Dp"] - H["Dt"], "DV2-Dp": H["DV2"] - H["Dp"], "C-Cp": H["C"] - H["Cp"]}
def cell(a):
    name, ser, g, outdir = a; path = f"{outdir}/cell_{name}_{g}.json"
    if os.path.exists(path): return path
    d = np.asarray(ser, float); base = d - d.mean(); n_p = len(d); pw = {}
    for sh, nm in ((+S.DELTA, "plus"), (-S.DELTA, "minus")):
        rng = S.sub_rng(f"p8power|{name}|{g}|{nm}", 9801); rej = 0
        for _ in range(S.NSIM):
            smp = base[rng.randint(0, n_p, g)] + sh; p, _ = S.boot_t(smp, rng, S.B_DEF); rej += int(p < 0.05)
        pw[nm] = rej / S.NSIM
    save(dict(name=name, g=g, power_plus=pw["plus"], power_minus=pw["minus"]), path); return path
def pilot(pdir, outdir):
    from scipy.stats import chi2
    os.makedirs(outdir, exist_ok=True); res = load_dir(pdir); keep, excl = usable(res); H = hv_matrix(res, keep); C = contrasts(H); n_p = len(keep)
    jobs = [(nm, C[nm].tolist(), g, outdir) for nm in C for g in S.GRID]
    with Pool(2) as pool: list(pool.imap_unordered(cell, jobs))
    rep = dict(n_pilot=n_p, excluded=excl, hv_means={a: float(H[a].mean()) for a in MAIN}, by_contrast={})
    for nm, d in C.items():
        s = float(d.std(ddof=1)); up = s * math.sqrt((n_p - 1) / chi2.ppf(0.2, n_p - 1)); n_f = math.ceil(((1.960 + S.Z80) * up / S.DELTA) ** 2); pw = {}
        for g in S.GRID:
            c = json.load(open(f"{outdir}/cell_{nm}_{g}.json")); pm = min(c["power_plus"], c["power_minus"]); pw[g] = dict(power_min=pm, power_plus=c["power_plus"], power_minus=c["power_minus"])
        ok = [g for g in S.GRID if pw[g]["power_min"] >= 0.8]; ns = ok[0] if ok else None; cand = [g for g in S.GRID if ns is not None and g >= max(n_f, ns)]; nc = cand[0] if cand else None
        rep["by_contrast"][nm] = dict(mean=float(d.mean()), sd=s, sd_haut=up, n_f=n_f, n_s=(ns if ns else ">300"), n_contraste=(nc if nc else ">300"), power=pw)
    prim = rep["by_contrast"]["I_V1"]["n_contraste"]; ns_ = [v["n_contraste"] for v in rep["by_contrast"].values()]
    rep["primary_infeasible"] = (prim == ">300"); rep["n_requis"] = ">300" if any(x == ">300" for x in ns_) else max(ns_)
    rep["n_retenu"] = None if prim == ">300" else (300 if rep["n_requis"] == ">300" else rep["n_requis"]); rep["underpowered_secondary"] = [k for k, v in rep["by_contrast"].items() if v["n_contraste"] == ">300"] if prim != ">300" else []
    save(rep, outdir + "/p8_pilot_report.json"); print(json.dumps({k: rep[k] for k in ("n_pilot", "n_requis", "n_retenu", "primary_infeasible", "underpowered_secondary")}))
    if rep["n_retenu"]: save(dict(n=rep["n_retenu"], source="sizing rule P8 amendment item 1-2"), B8 + "/p8_n.json")
def precheck(d, freeze):
    bad = []
    if not R.verify_freeze(freeze): bad.append("freeze verification failed")
    n = json.load(open(B8 + "/p8_n.json"))["n"]; res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(8200, 8200 + n)): bad.append(f"seed set: {len(seeds)} seeds")
    if len(res) != 6 * n: bad.append(f"{len(res)} shards, expected {6 * n}")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append(f"infeasible {k}"); continue
        for a in MAIN:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a} budget/missing")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def final(d, out, freeze):
    assert not os.path.exists(out), "final analysis already exists: RUN ONCE"
    assert precheck(d, freeze); res = load_dir(d); keep, excl = usable(res); H = hv_matrix(res, keep); C = contrasts(H); n = len(keep)
    rng = S.sub_rng("p8final", 9801); idx = rng.randint(0, n, size=(S.B_DEF, n)).astype(np.int32); fam = {}
    for nm, dd in C.items():
        p, inf = S.boot_t(dd, rng, S.B_DEF, idx); fam[nm] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), p_raw=p, info=inf, share_pos=float((dd > 0).mean()))
        bm = dd[idx].mean(1); fam[nm]["ci95_pct_boot"] = [float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))]
    hp = S.holm([fam[k]["p_raw"] for k in C]); 
    for k, p in zip(C, hp): fam[k]["p_holm"] = float(p); fam[k]["reject_0.05"] = bool(p < 0.05)
    sec = {}
    for nm, dd in secondary(H).items():
        p, inf = S.boot_t(dd, rng, S.B_DEF, idx); bm = dd[idx].mean(1); sec[nm] = dict(mean=float(dd.mean()), p_raw_descriptive=p, ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))], share_pos=float((dd > 0).mean()))
    diag = {}
    for a in MAIN:
        sd = [np.mean(res[f"{sc}|{s}"]["conds"][a].get("sd_f", [np.nan] * 3)[1:]) for s in keep for sc in SC if "sd_f" in res[f"{sc}|{s}"]["conds"][a]]
        diag[a] = dict(sd_f23_search_archive=float(np.nanmean(sd)) if sd else None, ents=float(np.mean([e for s in keep if s % 10 == 0 for sc in SC for _, e in (res[f"{sc}|{s}"]["conds"][a].get("ent") or [])])) if any(res[f"{sc}|{s}"]["conds"][a].get("ent") for s in keep for sc in SC) else None)
    rep = dict(n=n, excluded=excl, hv_oracle_means={a: float(H[a].mean()) for a in MAIN}, family_holm=fam, secondary_descriptive=sec, diagnostics=diag, seeds_range=[keep[0], keep[-1]])
    save(rep, out); print(json.dumps({"hv": rep["hv_oracle_means"], "family": {k: (v["mean"], v["p_raw"], v["p_holm"]) for k, v in fam.items()}}, indent=1))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "pilot": pilot(sys.argv[2], sys.argv[3])
    elif m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
