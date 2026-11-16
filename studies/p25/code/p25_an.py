"""P25 pre-registered analysis. python p25_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE (RUN ONCE)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
SC6 = ["V6-U", "V7-U", "V6-K", "V7-K", "V6-M", "V7-M"]; DELTA = 0.005
PRM = json.load(open(B + "/p25/p25_params.json")); ARMS = PRM["arms"]; ROLES = PRM["roles"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d): return {f"{r['sc']}|{r['seed']}": r for r in (json.load(open(f)) for f in sorted(glob.glob(d + "/*__*.json")))}
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != list(range(14000, 14060)) or len(res) != 360: bad.append(f"shape {len(res)}")
    for k, r in res.items():
        if not r.get("feasible"): bad.append(f"{k} infeasible"); continue
        if not os.path.exists(d + "/" + k.replace("|", "__") + ".npz"): bad.append(f"{k} npz")
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def cls(lo, hi):
    if lo > 0: return "superiority"
    if hi < 0: return "inferiority"
    if lo > -DELTA and hi < DELTA: return "equivalence"
    return "inconclusive"
def final(d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
    R = ROLES; src = {a: {sc: np.array([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for sc in SC6} for a in ARMS}
    H = {a: np.mean([src[a][sc] for sc in SC6], axis=0) for a in ARMS}
    idx = S.sub_rng("p25_final", 14993).randint(0, n, size=(20000, n)).astype(np.int32)
    def ci(dd, a2): bm = dd[idx].mean(1); return float(np.percentile(bm, a2 / 2)), float(np.percentile(bm, 100 - a2 / 2))
    p24r = json.load(open(B + "/p24/p24_final_analysis.json"))["contrasts"]; p23r = json.load(open(B + "/p23/p23_final_analysis.json"))["primary"]
    REF = {"K1 DA-E w=0.3": p23r["C4 DA100-E"], "K2 DA-Dg_cal w=0.3": None, "K1 DA-E w=0.7": p24r["DA-E w=0.7"], "K2 DA-Dg_cal w=0.7": p24r["DA-Dg w=0.7"]}
    C = []
    for w in (0.3, 0.7):
        C += [("K1 DA-E w=%g" % w, R["DA_w%g" % w], R["E_w%g" % w]), ("K2 DA-Dg_cal w=%g" % w, R["DA_w%g" % w], R["Dg_w%g" % w]), ("K3 Dg_cal-E w=%g" % w, R["Dg_w%g" % w], R["E_w%g" % w]), ("K4 DA-Dp w=%g" % w, R["DA_w%g" % w], R["Dp_w%g" % w])]
    C.append(("K5 DA-Dg6 w=0.3", R["DA_w0.3"], R["Dg6_w0.3"]))
    rep = dict(status="PRE-REGISTERED P25 v0.1 (9 contrasts, 99% marginal CI, margin 0.005)", n_seeds=n, gamma_cal=PRM["gamma_cal"], gate=PRM["gate_satisfied"], hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, hv_oracle_sd={a: float(H[a].std(ddof=1)) for a in ARMS}, contrasts={}, secondary={})
    for nm, a, b in C:
        dd = H[a] - H[b]; lo, hi = ci(dd, 1.0); blo, bhi = ci(dd, 1.0 / 4)
        r = dict(a=a, b=b, mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), ci_bonferroni=[blo, bhi], decision_bonferroni=cls(blo, bhi), share_pos=float((dd > 0).mean()))
        ref = REF.get(nm)
        if ref: r["ref_earlier"] = dict(mean=ref["mean"], ci99=ref["ci99"], decision=ref["decision"]); r["same_direction"] = bool(np.sign(r["mean"]) == np.sign(ref["mean"])); r["same_class"] = bool(r["decision"] == ref["decision"])
        rep["contrasts"][nm] = r
        rep["secondary"][nm] = dict(per_scenario={sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC6}, by_geometry={g: float(np.mean([(src[a][sc] - src[b][sc]) for sc in SC6 if sc.endswith("-" + g)])) for g in "UKM"}, by_size={v: float(np.mean([(src[a][sc] - src[b][sc]) for sc in SC6 if sc.startswith(v)])) for v in ("V6", "V7")})
    def mser(a, key): return float(np.mean([x[key] for r in res.values() for x in r["conds"][a]["dyn"] if "q_ent" in x]))
    mt = {}
    for w in (0.3, 0.7):
        for lab, b in (("Dg_cal", R["Dg_w%g" % w]),) + ((("Dg6", R["Dg6_w0.3"]),) if w == 0.3 else ()):
            a = R["DA_w%g" % w]; Hr, Ho, Qr, Qo = mser(a, "q_ent"), mser(b, "q_ent"), mser(a, "q_max"), mser(b, "q_max"); gap = abs(Ho - Hr) / Hr; qg = abs(Qo - Qr)
            mt["w=%g %s" % (w, lab)] = dict(rel_entropy_gap=gap, abs_qmax_gap=qg, conform=bool(gap <= 0.10 and qg <= 0.05), entropy_ref=Hr, entropy_other=Ho, qmax_ref=Qr, qmax_other=Qo)
    rep["matching_SC6P25"] = mt
    save(rep, out); print(json.dumps(dict(contrasts=rep["contrasts"], matching=mt), indent=1, default=str)[:9000])
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
