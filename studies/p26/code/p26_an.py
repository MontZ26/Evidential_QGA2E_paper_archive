"""P26 pre-registered analysis. python p25_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE (RUN ONCE)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
SC6 = ["B-X", "B-M", "B-G", "B-L", "B-O", "B-H"]; DELTA = 0.005
PRM = json.load(open(B + "/p26/p26_params.json")); ARMS = PRM["arms"]; ROLES = PRM["roles"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d): return {f"{r['sc']}|{r['seed']}": r for r in (json.load(open(f)) for f in sorted(glob.glob(d + "/*__*.json")))}
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != list(range(16000, 16060)) or len(res) != 360: bad.append(f"shape {len(res)}")
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
    idx = S.sub_rng("p26_final", 16993).randint(0, n, size=(20000, n)).astype(np.int32)
    def ci(dd, a2): bm = dd[idx].mean(1); return float(np.percentile(bm, a2 / 2)), float(np.percentile(bm, 100 - a2 / 2))
    p24r = json.load(open(B + "/p24/p24_final_analysis.json"))["contrasts"]; p23r = json.load(open(B + "/p23/p23_final_analysis.json"))["primary"]
    p25r = json.load(open(B + "/p25b/p25b_final_analysis.json"))["contrasts"]
    REF = {"L3 DA-E w=0.3": p25r["K1 DA-E w=0.3"], "L3 DA-E w=0.7": p25r["K1 DA-E w=0.7"], "L4 DA-Dp w=0.3": p25r["K4 DA-Dp w=0.3"], "L4 DA-Dp w=0.7": p25r["K4 DA-Dp w=0.7"]}
    C = []
    for w in (0.3, 0.7):
        C += [("L1 E-Dgt_E w=%g" % w, R["E_w%g" % w], R["Dgt_E_w%g" % w]), ("L2 DA-Dgt_DA w=%g" % w, R["DA_w%g" % w], R["Dgt_DA_w%g" % w]), ("L3 DA-E w=%g" % w, R["DA_w%g" % w], R["E_w%g" % w]), ("L4 DA-Dp w=%g" % w, R["DA_w%g" % w], R["Dp_w%g" % w]), ("L5 DA-Dg6 w=%g" % w, R["DA_w%g" % w], R["Dg6_w%g" % w])]
    rep = dict(status="PRE-REGISTERED P26 v0.1 (10 contrasts, 99% marginal CI, margin 0.005)", n_seeds=n, schedules=PRM["schedules"], gate=PRM["gate_satisfied"], hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, hv_oracle_sd={a: float(H[a].std(ddof=1)) for a in ARMS}, contrasts={}, secondary={})
    for nm, a, b in C:
        dd = H[a] - H[b]; lo, hi = ci(dd, 1.0); blo, bhi = ci(dd, 1.0 / 5)
        r = dict(a=a, b=b, mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), ci_bonferroni=[blo, bhi], decision_bonferroni=cls(blo, bhi), share_pos=float((dd > 0).mean()))
        ref = REF.get(nm)
        if ref: r["ref_earlier"] = dict(mean=ref["mean"], ci99=ref["ci99"], decision=ref["decision"]); r["same_direction"] = bool(np.sign(r["mean"]) == np.sign(ref["mean"])); r["same_class"] = bool(r["decision"] == ref["decision"])
        rep["contrasts"][nm] = r
        rep["secondary"][nm] = dict(per_scenario={sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC6})
    def traj(a, key): return np.mean([[x[key] for x in r["conds"][a]["dyn"] if "q_ent" in x] for r in res.values()], axis=0)
    mt = {}
    for w in (0.3, 0.7):
        for lab, ra, b in (("E", R["E_w%g" % w], R["Dgt_E_w%g" % w]), ("DA", R["DA_w%g" % w], R["Dgt_DA_w%g" % w])):
            Hr, Ho, Qr, Qo = traj(ra, "q_ent"), traj(b, "q_ent"), traj(ra, "q_max"), traj(b, "q_max"); ebar = float(np.mean(np.abs(Ho - Hr) / Hr)); qbar = float(np.mean(np.abs(Qo - Qr)))
            gi = [0, 24, 49, 99, 149]; prof = dict(gens=[g + 1 for g in gi], rel_entropy_gap=[float(abs(Ho[g] - Hr[g]) / Hr[g]) for g in gi], qmax_gap=[float(abs(Qo[g] - Qr[g])) for g in gi])
            def effd(ra_, b_, gen):
                js, l1, n = 0.0, 0.0, 0
                for k_ in res:
                    fn = d + "/" + k_.replace("|", "__") + ".npz"
                    try: z = np.load(fn); a1 = z["%s|%d" % (ra_, gen)].astype(float) / 40.0; b1 = z["%s|%d" % (b_, gen)].astype(float) / 40.0; mod = z["M"].sum(1) >= 2
                    except Exception: continue
                    m1 = 0.5 * (a1 + b1)
                    def kl(p, q): return np.where(p > 0, p * np.log2(np.where(p > 0, p, 1.0) / np.where(q > 0, q, 1.0)), 0.0).sum(1)
                    js += float((0.5 * kl(a1, m1) + 0.5 * kl(b1, m1))[mod].mean()); l1 += float(np.abs(a1 - b1).sum(1)[mod].mean()); n += 1
                return dict(js=js / n, l1=l1 / n, n_tasks=n) if n else None
            prof["effective_distribution_gen50"] = effd(ra, b, 50); prof["effective_distribution_gen150"] = effd(ra, b, 150)
            mt["w=%g ref %s" % (w, lab)] = dict(profile=prof, rel_entropy_gap_mean_over_gens=ebar, abs_qmax_gap_mean_over_gens=qbar, max_rel_entropy_gap=float(np.max(np.abs(Ho - Hr) / Hr)), conform=bool(ebar <= 0.10 and qbar <= 0.05), schedule=b)
    rep["matching_trajectory_SC6P26"] = mt
    save(rep, out); print(json.dumps(dict(contrasts=rep["contrasts"], matching=mt), indent=1, default=str)[:9000])
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
