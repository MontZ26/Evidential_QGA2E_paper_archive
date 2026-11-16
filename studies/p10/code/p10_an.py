"""P10 analysis. python p11_an.py pilot PILOT_DIR OUT_DIR | precheck CONFDIR FREEZE | final CONFDIR OUT.json FREEZE (RUN ONCE). Co-primaries: D1 = E1-P1 ; D2 = (E1-E0)-(P1-P0); Holm on 2, bilateral alpha 0.05, bootstrap-t over seeds (P6 rules), seed tag 9803."""
import sys, os, json, math, glob
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R
B11 = B + "/p10"; ARMS = ["E", "P", "X", "Dp", "A", "B", "Bp", "E_DEC", "P_DEC", "C0"]; SC = S.SC
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
def prim(H): return {"G10_E-P": H["E"] - H["P"], "E-Dp": H["E"] - H["Dp"], "E-X": H["E"] - H["X"]}   # sizing contrasts (P10 section 5); only G10 is confirmatory
def sec(H): return {"E-X": H["E"] - H["X"], "Dp-P": H["Dp"] - H["P"], "E-Dp": H["E"] - H["Dp"], "X-P": H["X"] - H["P"], "interaction E-Dp-X+P": H["E"] - H["Dp"] - H["X"] + H["P"], "E-B": H["E"] - H["B"], "P-Bp": H["P"] - H["Bp"], "B-Bp": H["B"] - H["Bp"], "B-A": H["B"] - H["A"], "E-C0": H["E"] - H["C0"], "B-C0": H["B"] - H["C0"],
  "DEC: E_DEC-E": H["E_DEC"] - H["E"], "DEC: P_DEC-P": H["P_DEC"] - H["P"], "DEC: E_DEC-P_DEC": H["E_DEC"] - H["P_DEC"], "DEC: Delta_DEC=[E_DEC-E]-[P_DEC-P]": (H["E_DEC"] - H["E"]) - (H["P_DEC"] - H["P"])}
def cell(a):
    name, ser, g, outdir = a; path = f"{outdir}/cell_{name}_{g}.json"
    if os.path.exists(path): return path
    d = np.asarray(ser, float); base = d - d.mean(); n_p = len(d); pw = {}
    for sh, nm in ((+S.DELTA, "plus"), (-S.DELTA, "minus")):
        rng = S.sub_rng(f"p10power|{name}|{g}|{nm}", 9803); rej = 0
        for _ in range(S.NSIM): smp = base[rng.randint(0, n_p, g)] + sh; p, _ = S.boot_t(smp, rng, S.B_DEF); rej += int(p < 0.05)
        pw[nm] = rej / S.NSIM
    save(dict(name=name, g=g, power_plus=pw["plus"], power_minus=pw["minus"]), path); return path
def pilot(pdir, outdir):
    from scipy.stats import chi2
    os.makedirs(outdir, exist_ok=True); res = load_dir(pdir); keep, excl = usable(res); H = hv(res, keep); C = prim(H); n_p = len(keep)
    with Pool(2) as pool: list(pool.imap_unordered(cell, [(nm, C[nm].tolist(), g, outdir) for nm in C for g in S.GRID]))
    rep = dict(n_pilot=n_p, excluded=excl, hv_means={a: float(H[a].mean()) for a in ARMS}, by_contrast={})
    for nm, d in C.items():
        s = float(d.std(ddof=1)); up = s * math.sqrt((n_p - 1) / chi2.ppf(0.2, n_p - 1)); n_f = math.ceil(((1.960 + S.Z80) * up / S.DELTA) ** 2); pw = {}
        for g in S.GRID:
            c = json.load(open(f"{outdir}/cell_{nm}_{g}.json")); pw[g] = dict(power_min=min(c["power_plus"], c["power_minus"]))
        ok = [g for g in S.GRID if pw[g]["power_min"] >= 0.8]; ns = ok[0] if ok else None; cand = [g for g in S.GRID if ns is not None and g >= max(n_f, ns)]; nc = cand[0] if cand else None
        rep["by_contrast"][nm] = dict(mean=float(d.mean()), sd=s, sd_haut=up, n_f=n_f, n_s=(ns if ns else ">300"), n_contraste=(nc if nc else ">300"), power=pw)
    ns_ = [v["n_contraste"] for v in rep["by_contrast"].values()]; rep["any_infeasible_at_300"] = any(x == ">300" for x in ns_)
    rep["n_requis"] = ">300" if rep["any_infeasible_at_300"] else max(ns_); rep["n_retenu"] = None if rep["any_infeasible_at_300"] else rep["n_requis"]
    save(rep, outdir + "/p10_pilot_report.json"); print(json.dumps({k: rep[k] for k in ("n_pilot", "n_requis", "n_retenu", "any_infeasible_at_300")}), {k: (v["n_contraste"], round(v["mean"], 4), round(v["sd"], 4)) for k, v in rep["by_contrast"].items()})
    if rep["n_retenu"]: save(dict(n=rep["n_retenu"], source="sizing rule P10 (pilot 9350-9379); n=200 convention (author)"), B11 + "/p10_n.json")
def precheck(d, freeze):
    bad = []
    if not R.verify_freeze(freeze): bad.append("freeze verification failed")
    n = json.load(open(B11 + "/p10_n.json"))["n"]; res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(9400, 9400 + n)): bad.append(f"seed set {len(seeds)}")
    if len(res) != 6 * n: bad.append(f"{len(res)} shards expected {6 * n}")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append(f"infeasible {k}"); continue
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def final(d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); keep, _ = usable(res); H = hv(res, keep); n = len(keep); C = prim(H)
    rng = S.sub_rng("p10final", 9803); idx = rng.randint(0, n, size=(S.B_DEF, n)).astype(np.int32); rep = dict(n=n, hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, primary={}, secondary_descriptive={})
    dd = C["G10_E-P"]; p, inf = S.boot_t(dd, rng, S.B_DEF, idx); bm = dd[idx].mean(1)
    rep["primary"]["G10_E-P"] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), p_raw=p, info=inf, ci95_boot=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))], share_pos=float((dd > 0).mean()), reject_0_05=bool(p < 0.05), note="single primary, no Holm; unadjusted percentile CI; bootstrap p floor 1/(B+1)")
    for k, dd in sec(H).items():
        pp, _ = S.boot_t(dd, rng, S.B_DEF, idx); b = dd[idx].mean(1); rep["secondary_descriptive"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], p_raw_descriptive=pp, share_pos=float((dd > 0).mean()))
    # diagnostics (descriptive): final-population dependence and DEC counters by arm
    dg = {}
    for a in ARMS:
        rows = [res[f"{sc}|{s}"]["conds"][a] for sc in SC for s in keep]
        if a == "C0": dg[a] = dict(note="classical GA reference, no QGA diagnostics"); continue
        dg[a] = dict(dep_last=float(np.mean([r["dyn"][-1]["dep"] for r in rows])), neff_last=float(np.mean([r["dyn"][-1]["neff"] for r in rows])), marg_ent_last=float(np.mean([r["dyn"][-1]["marg_ent"] for r in rows])))
        if a != "C0" and "src_dep" in rows[0]["dyn"][-1]: dg[a].update(src_dep_last=float(np.mean([r["dyn"][-1].get("src_dep", np.nan) for r in rows])), src_neff_last=float(np.nanmean([r["dyn"][-1].get("src_neff", np.nan) for r in rows])), q_ent_last=float(np.nanmean([r["dyn"][-1].get("q_ent", np.nan) for r in rows])), q_max_last=float(np.nanmean([r["dyn"][-1].get("q_max", np.nan) for r in rows])))
        dd_ = [r["dec"] for r in rows if r.get("dec")]
        if dd_: dg[a].update(violation_rate=float(np.sum([x["violations"] for x in dd_]) / max(1, np.sum([x["cands"] for x in dd_]))), mutations_per_run=float(np.mean([x["mutations"] for x in dd_])), regen_per_cand=float(np.sum([x["regen"] for x in dd_]) / max(1, np.sum([x["cands"] for x in dd_]))), ls_skipped_per_run=float(np.mean([x["ls_skipped"] for x in dd_])))
    rep["diagnostics_descriptive"] = dg; save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "pilot": pilot(sys.argv[2], sys.argv[3])
    elif m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
