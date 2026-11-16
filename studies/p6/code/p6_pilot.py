"""P6 pilot -> sizing (protocol v2.6 section 8). Usage: python p6_pilot.py PILOT_DIR OUT_DIR. Resumable (one JSON per (contrast, m, grid value)). Writes p6_pilot_report.json. Does NOT write p6_n.json (decision step is separate)."""
import sys, os, json, math, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import chi2
import p6_stats as S, p6_load as L
MULT = (1.0, 1.25, 1.5); ALPHA = {"H6.1": 0.05, "H6.5": 0.01}

def cell(a):
    name, ser, alpha, m, g, outdir = a; path = f"{outdir}/cell_{name}_{m}_{g}.json"
    if os.path.exists(path): return path
    d = np.asarray(ser, float); base = (d - d.mean()) * m; n_p = len(d); pw = {}; info = {}
    for sh, nm in ((+S.DELTA, "plus"), (-S.DELTA, "minus")):
        rng = S.sub_rng(f"power|{name}|{m}|{g}|{nm}"); rej = 0; nc = 0
        for _ in range(S.NSIM):
            smp = base[rng.randint(0, n_p, g)] + sh; p, inf = S.boot_t(smp, rng, S.B_DEF); rej += int(p < alpha); nc += int(inf["status"] == "not_computable")
        pw[nm] = rej / S.NSIM; info[nm + "_not_computable"] = nc
    L.save(dict(name=name, m=m, g=g, alpha=alpha, power_plus=pw["plus"], power_minus=pw["minus"], **info), path); return path

def main(pdir, outdir):
    os.makedirs(outdir, exist_ok=True); res = L.load_dir(pdir); keep, excl = L.usable(res, S.ARMS); H = L.hv_matrix(res, keep); se = S.series(H)
    ser = {k: se[k].tolist() for k in ("H6.1", "H6.5")}; n_p = len(keep)
    jobs = [(nm, ser[nm], ALPHA[nm], m, g, outdir) for nm in ser for m in MULT for g in S.GRID]; t0 = time.time()
    with Pool(2) as pool:
        for i, _ in enumerate(pool.imap_unordered(cell, jobs)): print(i + 1, len(jobs), f"{time.time() - t0:.0f}s", flush=True)
    rep = dict(n_pilot=n_p, seeds=[keep[0], keep[-1]], excluded=excl, contrasts={})
    for nm in ser:
        d = np.asarray(ser[nm]); s = float(d.std(ddof=1)); sd_up = s * math.sqrt((n_p - 1) / chi2.ppf(0.2, n_p - 1)); zq = 1.960 if ALPHA[nm] == 0.05 else 2.576; rep["contrasts"][nm] = dict(mean=float(d.mean()), sd=s, sd_haut=sd_up, alpha=ALPHA[nm], by_m={})
        for m in MULT:
            n_f = math.ceil(((zq + S.Z80) * sd_up * m / S.DELTA) ** 2); pw = {}
            for g in S.GRID:
                c = json.load(open(f"{outdir}/cell_{nm}_{m}_{g}.json")); pmin = min(c["power_plus"], c["power_minus"]); se_ = math.sqrt(max(pmin * (1 - pmin), 1e-12) / S.NSIM)
                pw[g] = dict(power_plus=c["power_plus"], power_minus=c["power_minus"], power_min=pmin, mc_se=se_, mc_ci95=[pmin - 1.96 * se_, pmin + 1.96 * se_], not_computable=(c["plus_not_computable"], c["minus_not_computable"]))
            ok = [g for g in S.GRID if pw[g]["power_min"] >= 0.8]; n_s = ok[0] if ok else None; cand = [g for g in S.GRID if n_s is not None and g >= max(n_f, n_s)]; n_c = cand[0] if cand else None
            rep["contrasts"][nm]["by_m"][str(m)] = dict(n_f=n_f, n_s=(n_s if n_s else ">300"), n_contraste=(n_c if n_c else ">300"), power=pw)
    for m in MULT:
        v = [rep["contrasts"][nm]["by_m"][str(m)]["n_contraste"] for nm in ser]; rep.setdefault("n_requis", {})[str(m)] = (">300" if any(x == ">300" for x in v) else max(v))
    mainreq = rep["n_requis"]["1.0"]; rep["n_retenu"] = 300 if mainreq == ">300" else mainreq; rep["under_powered_declared"] = [nm for nm in ser if rep["contrasts"][nm]["by_m"]["1.0"]["n_contraste"] == ">300"]
    rep["rule_note"] = "n from the main simulation (m=1.0); grid {100,150,200,300}; cap 300; sensitivity (m=1.25,1.5) informs but never changes n; no automatic pilot extension (D-21)."
    L.save(rep, outdir + "/p6_pilot_report.json"); print(json.dumps({k: rep[k] for k in ("n_pilot", "n_requis", "n_retenu", "under_powered_declared")}, indent=1))
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
