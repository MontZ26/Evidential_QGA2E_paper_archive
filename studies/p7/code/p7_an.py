"""P7 analysis helpers + pilot sizing (H7.1) + single final analysis. Usage:
  python p7_an.py pilot PILOT_DIR OUT_DIR           (sizing for H7.1 = V2 - V0c, alpha 0.05, m = 1, 1.25, 1.5; method of P6 v2.6 section 8)
  python p7_an.py precheck CONF_DIR FREEZE
  python p7_an.py final CONF_DIR OUT.json FREEZE    (RUN ONCE)"""
import sys, os, json, math, glob
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6/code")
import numpy as np
from scipy.stats import chi2
import p6_stats as S
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"); import run_p1m as R
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7"
ARMS = ["V0", "V0c", "V1", "V2", "V0c-M2", "V1-M2", "V2-M2"]; SC = S.SC
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")):
        r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def hvl(f): return float(R.hv(np.asarray(f, float).reshape(-1, 3))) if f is not None and len(f) else 0.0
def usable(res):
    seeds = sorted({r["seed"] for r in res.values()}); keep = []; excl = {}
    for s in seeds:
        why = []
        for sc in SC:
            r = res.get(f"{sc}|{s}")
            if r is None: why.append(f"{sc}: missing"); continue
            if not r.get("feasible", False): why.append(f"{sc}: infeasible"); continue
            miss = [a for a in ARMS if a not in r.get("conds", {})]
            if miss: why.append(f"{sc}: missing {miss}")
        if why: excl[s] = why
        else: keep.append(s)
    return keep, excl
def hv_matrix(res, keep): return {a: np.array([np.mean([hvl(res[f"{sc}|{s}"]["conds"][a]["front"]) for sc in SC]) for s in keep]) for a in ARMS}
# ---------------------------------------------------------------- pilot sizing
def cell(a):
    ser, m, g, outdir = a; path = f"{outdir}/cell_{m}_{g}.json"
    if os.path.exists(path): return path
    d = np.asarray(ser, float); base = (d - d.mean()) * m; n_p = len(d); pw = {}; nc = {}
    for sh, nm in ((+S.DELTA, "plus"), (-S.DELTA, "minus")):
        rng = S.sub_rng(f"p7power|H7.1|{m}|{g}|{nm}", 9701); rej = 0; k = 0
        for _ in range(S.NSIM):
            smp = base[rng.randint(0, n_p, g)] + sh; p, inf = S.boot_t(smp, rng, S.B_DEF); rej += int(p < 0.05); k += int(inf["status"] == "not_computable")
        pw[nm] = rej / S.NSIM; nc[nm] = k
    save(dict(m=m, g=g, power_plus=pw["plus"], power_minus=pw["minus"], not_computable=nc), path); return path
def pilot(pdir, outdir):
    os.makedirs(outdir, exist_ok=True); res = load_dir(pdir); keep, excl = usable(res); H = hv_matrix(res, keep); d = H["V2"] - H["V0c"]; n_p = len(keep)
    jobs = [(d.tolist(), m, g, outdir) for m in (1.0, 1.25, 1.5) for g in S.GRID]
    with Pool(2) as pool: list(pool.imap_unordered(cell, jobs))
    s = float(d.std(ddof=1)); up = s * math.sqrt((n_p - 1) / chi2.ppf(0.2, n_p - 1)); rep = dict(n_pilot=n_p, excluded=excl, mean=float(d.mean()), sd=s, sd_haut=up, by_m={})
    for m in (1.0, 1.25, 1.5):
        n_f = math.ceil(((1.960 + S.Z80) * up * m / S.DELTA) ** 2); pw = {}
        for g in S.GRID:
            c = json.load(open(f"{outdir}/cell_{m}_{g}.json")); pm = min(c["power_plus"], c["power_minus"]); se = math.sqrt(max(pm * (1 - pm), 1e-12) / S.NSIM); pw[g] = dict(power_min=pm, power_plus=c["power_plus"], power_minus=c["power_minus"], mc_se=se, mc_ci95=[pm - 1.96 * se, pm + 1.96 * se])
        ok = [g for g in S.GRID if pw[g]["power_min"] >= 0.8]; ns = ok[0] if ok else None; cand = [g for g in S.GRID if ns is not None and g >= max(n_f, ns)]; nc = cand[0] if cand else None
        rep["by_m"][str(m)] = dict(n_f=n_f, n_s=(ns if ns else ">300"), n_contraste=(nc if nc else ">300"), power=pw)
    mr = rep["by_m"]["1.0"]["n_contraste"]; rep["n_requis"] = mr; rep["n_retenu"] = 300 if mr == ">300" else mr; rep["under_powered"] = (mr == ">300")
    save(rep, outdir + "/p7_pilot_report.json"); print(json.dumps({k: rep[k] for k in ("n_pilot", "mean", "sd", "n_requis", "n_retenu", "under_powered")}))
# ---------------------------------------------------------------- precheck
def precheck(d, freeze):
    bad = []
    if not R.verify_freeze(freeze): bad.append("freeze verification failed")
    n = json.load(open(BASE + "/p7_n.json"))["n"]; res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(7200, 7200 + n)): bad.append(f"seed set: {len(seeds)} seeds")
    if len(res) != 6 * n: bad.append(f"{len(res)} shards, expected {6 * n}")
    inf = []
    for k, r in res.items():
        if not r.get("feasible", False): inf.append(k); continue
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None: bad.append(f"{k}: missing {a}"); continue
            F = np.asarray(c["front"], float)
            if F.ndim != 2 or F.shape[1] != 3 or F.size == 0 or not np.isfinite(F).all() or F.min() < 0 or F.max() > 1 + 1e-9: bad.append(f"{k}|{a}: front invalid")
            if c["n_eval"] != 6040: bad.append(f"{k}|{a}: n_eval {c['n_eval']}")
    print("infeasible tasks:", inf); print("PRECHECK", "PASS" if not bad else "FAIL"); [print(" -", b) for b in bad[:30]]; return 0 if not bad else 1
# ---------------------------------------------------------------- final
def summ(x, nm):
    x = np.asarray(x, float); return dict(mean=float(x.mean()), median=float(np.median(x)), sd=float(x.std(ddof=1)), ci95_boot=S.boot_ci(x, S.sub_rng("ci|" + nm, 9701)), share_positive=float((x > 0).mean()))
def final(d, out, freeze):
    assert R.verify_freeze(freeze), "freeze verification failed"
    res = load_dir(d); keep, excl = usable(res); H = hv_matrix(res, keep); n = len(keep); rep = dict(n_seeds=n, seeds=[keep[0], keep[-1]], excluded=excl)
    ser = {"H7.1": H["V2"] - H["V0c"], "H7.2": H["V2"] - H["V1"], "H7.3": H["V1"] - H["V0c"], "H7.4": H["V2"] - H["V0"]}; desc_ = {"H7.1": "V2 - V0c (primary, alpha 0.05)", "H7.2": "V2 - V1", "H7.3": "V1 - V0c", "H7.4": "V2 - V0 (P5 C2c)"}
    ps = {}; tests = {}
    for nm, x in ser.items():
        p, info = S.boot_t(x, S.sub_rng("test|" + nm, 9701)); ps[nm] = p
        tests[nm] = dict(desc=desc_[nm], p_raw=p, boot_info=info, **summ(x, nm), p_wilcoxon_sensitivity=S.wilc_p(x), p_signflip_sensitivity=S.signflip_p(x, S.sub_rng("sf|" + nm, 9701)))
    sec = ["H7.2", "H7.3", "H7.4"]; adj = S.holm([ps[k] for k in sec])
    for k, a in zip(sec, adj): tests[k]["p_holm"] = a; tests[k]["reject_holm_0.05"] = bool(a < 0.05)
    tests["H7.1"]["reject_0.05"] = bool(ps["H7.1"] < 0.05); rep["tests"] = tests
    desc = {"hv_mean_by_arm": {a: dict(mean=float(H[a].mean()), sd=float(H[a].std(ddof=1))) for a in ARMS}}
    desc["M2_minus_M1_by_rule_descriptive_only"] = {r: summ(H[r + "-M2"] - H[r], "m2" + r) for r in ("V0c", "V1", "V2")}
    desc["M2_V2_minus_V0c_descriptive_only"] = summ(H["V2-M2"] - H["V0c-M2"], "m2v2v0c"); desc["M2_V1_minus_V0c_descriptive_only"] = summ(H["V1-M2"] - H["V0c-M2"], "m2v1v0c")
    desc["V0c_minus_V0"] = summ(H["V0c"] - H["V0"], "v0cv0"); desc["equivalence_zone_ci_inside"] = {k: bool(tests[k]["ci95_boot"][0] >= -0.01 and tests[k]["ci95_boot"][1] <= 0.01) for k in tests}
    ks = set(keep); agg = {a: dict(sh=0, t=0.0, gens=0, mE=[], mT=[], fb=[], L1=[], ent=[], div=[], ev=[]) for a in ARMS}
    for k, r in res.items():
        if not r.get("feasible") or r["seed"] not in ks: continue
        for a in ARMS:
            c = r["conds"][a]; g = agg[a]; g["sh"] += 1; g["t"] += c["search_time_s"]; g["gens"] += c["gens"]
            if c.get("ent"): g["ent"].append(c["ent"][-1][1])
            if c.get("div") and "6000" in c["div"]: g["div"].append(c["div"]["6000"]["dh"])
            for gen, md in c.get("mdiag", []) or []:
                for key, lst in (("m_empty", "mE"), ("m_theta", "mT"), ("fallback", "fb"), ("betp_vs_freq_L1", "L1"), ("evidence_share", "ev")):
                    if key in md: g[lst].append(md[key])
    desc["diagnostics"] = {a: dict(shards=g["sh"], mean_time_s=g["t"] / max(g["sh"], 1), mean_generations=g["gens"] / max(g["sh"], 1), mean_m_empty=(float(np.mean(g["mE"])) if g["mE"] else None), mean_m_theta=(float(np.mean(g["mT"])) if g["mT"] else None),
                          mean_fallback_share=(float(np.mean(g["fb"])) if g["fb"] else None), mean_betp_freq_L1=(float(np.mean(g["L1"])) if g["L1"] else None), mean_evidence_share_M2=(float(np.mean(g["ev"])) if g["ev"] else None),
                          mean_final_entropy=(float(np.mean(g["ent"])) if g["ent"] else None), mean_diversity_at_6000=(float(np.mean(g["div"])) if g["div"] else None)) for a, g in agg.items()}
    desc["retained_config"] = json.load(open(BASE + "/p7_tuned.json")); rep["descriptive"] = desc; save(rep, out)
    print("n seeds", n)
    for nm in tests: t = tests[nm]; print(nm, f"mean {t['mean']:+.5f} CI {t['ci95_boot'][0]:+.5f},{t['ci95_boot'][1]:+.5f} p_raw {t['p_raw']:.5f}", (f"p_holm {t['p_holm']:.5f}" if "p_holm" in t else ""))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "pilot": pilot(sys.argv[2], sys.argv[3])
    elif m == "precheck": sys.exit(precheck(sys.argv[2], sys.argv[3]))
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
