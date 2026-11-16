"""P21 pre-registered analyses. python p21_an.py precheck A|B DIR FREEZE | final A|B DIR OUT.json FREEZE (RUN ONCE per part; HV read only here)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
SC = S.SC; DELTA = 0.005; GENS = [1, 25, 50, 100, 150]
CFGP = {"A": dict(new=["NSGA2", "MOEAD"], seeds=list(range(11200, 11300)), nb=6040), "B": dict(new=["Eg1.1", "Eg1.25", "Eg0.9", "Eg0.8"], seeds=list(range(10400, 10500)), nb=6040)}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d): return {f"{r['sc']}|{r['seed']}": r for r in (json.load(open(f)) for f in sorted(glob.glob(d + "/*__*.json")))}
def precheck(part, d, freeze):
    c = CFGP[part]; bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != c["seeds"] or len(res) != 600: bad.append(f"shape {len(res)}")
    for k, r in res.items():
        for a in c["new"]:
            x = r.get("conds", {}).get(a)
            if x is None or x["n_eval"] != (6030 if a == "MOEAD" else 6040): bad.append(f"{k} {a}")
    print("PRECHECK", part, "OK" if not bad else bad[:10]); return not bad
def cls(lo, hi):
    if lo > 0: return "superiority"
    if hi < 0: return "inferiority"
    if lo > -DELTA and hi < DELTA: return "equivalence"
    return "inconclusive"
def refs(part, seeds):
    if part == "A":
        names = ["E", "DA", "Dp", "Dg", "DA+SEL4", "DA+SELR"]; return names, {f"{sc}|{s}": json.load(open(f"{B}/p17/runs/tier1/{sc}__{s}.json")) for sc in SC for s in seeds}
    names = ["E", "Dp", "Dg"]; r14 = {f"{sc}|{s}": json.load(open(f"{B}/p14/runs/conf/{sc}__{s}.json")) for sc in SC for s in seeds}
    r20 = {f"{sc}|{s}": json.load(open(f"{B}/p20/runs/main/{sc}__{s}.json")) for sc in SC for s in seeds}; return names, (r14, r20)
def final(part, d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(part, d, freeze); c = CFGP[part]; new = c["new"]; res = load_dir(d); seeds = c["seeds"]; n = len(seeds)
    names, rf = refs(part, seeds); src = {}; cond = {}
    for a in new: cond[a] = lambda sc, s, a=a: res[f"{sc}|{s}"]["conds"][a]
    if part == "A":
        for a in names: cond[a] = lambda sc, s, a=a: rf[f"{sc}|{s}"]["conds"][a]
    else:
        r14, r20 = rf
        for a in ["E", "Dp", "Dg"]: cond[a] = lambda sc, s, a=a: r14[f"{sc}|{s}"]["conds"][a]
        for a in ["Eg1.5", "Eg2", "Eg4", "Eg6"]: cond[a] = lambda sc, s, a=a: r20[f"{sc}|{s}"]["conds"][a]
    for a in cond: src[a] = {sc: np.array([cond[a](sc, s)["hv_oracle"] for s in seeds]) for sc in SC}
    H = {a: np.mean([src[a][sc] for sc in SC], axis=0) for a in src}
    idx = S.sub_rng("p21_final_" + part, 11995 if part == "A" else 11996).randint(0, n, size=(20000, n)).astype(np.int32)
    if part == "A": prim = {"A1 NSGA2-MOEAD": H["NSGA2"] - H["MOEAD"], "A2 NSGA2-E": H["NSGA2"] - H["E"], "A3 NSGA2-Dg": H["NSGA2"] - H["Dg"], "A4 MOEAD-Dg": H["MOEAD"] - H["Dg"], "A5 NSGA2-DA+SELR": H["NSGA2"] - H["DA+SELR"]}
    else: prim = {"B1 Eg1.1-E": H["Eg1.1"] - H["E"], "B2 Eg1.25-E": H["Eg1.25"] - H["E"], "B3 Eg0.9-E": H["Eg0.9"] - H["E"], "B4 Eg0.8-E": H["Eg0.8"] - H["E"]}
    rep = dict(status=f"PRE-REGISTERED P21 part {part} (primaries, 99% CI, margin 0.005)", n_seeds=n, hv_oracle_means={a: float(H[a].mean()) for a in H}, hv_oracle_sd={a: float(H[a].std(ddof=1)) for a in H}, primary={}, secondary={}, per_scenario={})
    for k, dd in prim.items():
        bm = dd[idx].mean(1); lo, hi = float(np.percentile(bm, 0.5)), float(np.percentile(bm, 99.5)); rep["primary"][k] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), share_pos=float((dd > 0).mean()))
    sec = {}
    if part == "A":
        for x in ("NSGA2", "MOEAD"):
            for b in ("E", "DA", "Dp", "Dg", "DA+SEL4", "DA+SELR"): sec[f"{x}-{b}"] = H[x] - H[b]
    else:
        sec["Eg1.25-Eg1.5"] = H["Eg1.25"] - H["Eg1.5"]; sec["Eg1.1-Eg1.5"] = H["Eg1.1"] - H["Eg1.5"]
        for g in ("Eg1.1", "Eg1.25", "Eg0.9", "Eg0.8"): sec[f"{g}-Dg"] = H[g] - H["Dg"]; sec[f"{g}-Dp"] = H[g] - H["Dp"]
        for g in ("Eg1.5", "Eg2", "Eg4", "Eg6"): sec[f"{g}-E"] = H[g] - H["E"]
    for k, dd in sec.items(): bm = dd[idx].mean(1); rep["secondary"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))])
    pairs = {"A": {"A1": ("NSGA2", "MOEAD"), "A2": ("NSGA2", "E"), "A3": ("NSGA2", "Dg"), "A4": ("MOEAD", "Dg"), "A5": ("NSGA2", "DA+SELR")}, "B": {"B1": ("Eg1.1", "E"), "B2": ("Eg1.25", "E"), "B3": ("Eg0.9", "E"), "B4": ("Eg0.8", "E")}}[part]
    for k, (a, b) in pairs.items(): rep["per_scenario"][k] = {sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC}
    if part == "A": rep["wall_s_mean_per_task"] = float(np.mean([r["wall_s"] for r in res.values()]))
    else:
        dg = {}
        for a in ["E", "Dp", "Dg", "Eg1.5", "Eg2", "Eg4", "Eg6"] + new:
            if a in res[f"{SC[0]}|{seeds[0]}"]["conds"] or True:
                try: dg[a] = {k: {str(g): float(np.mean([cond[a](sc, s)["dyn"][g][k] for sc in SC for s in seeds])) for g in GENS} for k in ("q_max", "q_ent")}
                except Exception as e: dg[a] = f"unavailable: {e}"
        rep["diagnostics"] = dg
    save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3], sys.argv[4]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
