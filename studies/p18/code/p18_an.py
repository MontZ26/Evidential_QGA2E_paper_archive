"""P18 pre-registered analysis. python p18_an.py precheckA|precheckB DIR FREEZE | finalA|finalB DIR OUT.json FREEZE (RUN ONCE per part; HV read only here)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
ARMS_A = ["E", "DA", "DA+S", "DA+L", "DA+P11", "DA+R1", "DA+R1inv", "DA+SCH"]; ARMS_B = ["DA+DIV", "DA+SELL", "Dp+SELW", "Dg2", "Dg4", "Dg8", "Dg12"]; REF_B = ["E", "DA", "Dp", "Dg", "DA+SEL4", "DA+SELR", "DA+SELW", "Dp+SEL4"]
SC = S.SC; GENS = [1, 25, 50, 100, 150]; DELTA = 0.005; T1 = B + "/p17/runs/tier1"
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")): r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def precheck(part, d, freeze):
    bad = []; arms = ARMS_A if part == "A" else ARMS_B; rs = range(11400, 11460) if part == "A" else range(11200, 11260)
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != list(rs): bad.append("seeds")
    if len(res) != 360: bad.append(f"{len(res)} shards")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append("infeasible " + k); continue
        for a in arms:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", part, "OK" if not bad else bad[:10]); return not bad
def cls(lo, hi):
    if lo > 0: return "superiority"
    if hi < 0: return "inferiority"
    if lo > -DELTA and hi < DELTA: return "equivalence"
    return "inconclusive"
def final(part, d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(part, d, freeze); res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
    if part == "A": arms = ARMS_A; src = {a: {sc: np.array([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for sc in SC} for a in arms}
    else:
        t1 = {f"{sc}|{s}": json.load(open(f"{T1}/{sc}__{s}.json")) for sc in SC for s in seeds}; arms = ARMS_B + REF_B
        src = {a: {sc: np.array([(res if a in ARMS_B else t1)[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for sc in SC} for a in arms}
    H = {a: np.mean([src[a][sc] for sc in SC], axis=0) for a in arms}
    idx = S.sub_rng("p18_final_" + part, 11992).randint(0, n, size=(20000, n)).astype(np.int32)
    if part == "A": prim = {"A1 R1-S": H["DA+R1"] - H["DA+S"], "A2 R1-L": H["DA+R1"] - H["DA+L"], "A3 R1-R1inv": H["DA+R1"] - H["DA+R1inv"], "A4 SCH-S": H["DA+SCH"] - H["DA+S"], "A5 S-DA": H["DA+S"] - H["DA"]}
    else: prim = {"B1 DIV-DA": H["DA+DIV"] - H["DA"], "B2 DIV-SELR": H["DA+DIV"] - H["DA+SELR"], "B3 DIV-SEL4": H["DA+DIV"] - H["DA+SEL4"], "B4 SELL-DA": H["DA+SELL"] - H["DA"], "B5 Dp+SELW-Dp": H["Dp+SELW"] - H["Dp"]}
    rep = dict(status=f"PRE-REGISTERED P18 PART {part} (5 primaries, 99% CI, margin 0.005)", n_seeds=n, hv_oracle_means={a: float(H[a].mean()) for a in arms}, primary={}, secondary={}, per_scenario={})
    for k, dd in prim.items():
        bm = dd[idx].mean(1); lo, hi = float(np.percentile(bm, 0.5)), float(np.percentile(bm, 99.5)); rep["primary"][k] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), share_pos=float((dd > 0).mean()))
        rep["per_scenario"][k] = {sc: None for sc in SC}
    if part == "A":
        sec = {"L-S": ("DA+L", "DA+S"), "P11-S": ("DA+P11", "DA+S"), "L-DA": ("DA+L", "DA"), "R1-DA": ("DA+R1", "DA"), "S-E": ("DA+S", "E"), "DA-E": ("DA", "E"), "R1-P11": ("DA+R1", "DA+P11")}
        pairs = {"A1 R1-S": ("DA+R1", "DA+S"), "A2 R1-L": ("DA+R1", "DA+L"), "A3 R1-R1inv": ("DA+R1", "DA+R1inv"), "A4 SCH-S": ("DA+SCH", "DA+S"), "A5 S-DA": ("DA+S", "DA")}
        keys = ("m_theta", "m_empty", "dep", "neff", "q_max", "q_ent")
        rep["diagnostics"] = {a: {k: {str(g): float(np.mean([res[f"{sc}|{s}"]["conds"][a]["dyn"][g][k] for sc in SC for s in seeds])) for g in GENS if all(k in res[f"{sc}|{s}"]["conds"][a]["dyn"][g] for sc in SC for s in seeds)} for k in keys} for a in ARMS_A if a != "E"}
        rep["share_L"] = {a: float(np.mean([np.mean([x == "L" for x in res[f"{sc}|{s}"]["conds"][a]["levels"]]) for sc in SC for s in seeds])) for a in ("DA+R1", "DA+R1inv", "DA+SCH", "DA+L")}
    else:
        sec = {"DIV-E": ("DA+DIV", "E"), "SELR-DA": ("DA+SELR", "DA"), "SEL4-DA": ("DA+SEL4", "DA")}
        for g in ("Dg2", "Dg4", "Dg8", "Dg12"): sec[f"{g}-E"] = (g, "E"); sec[f"{g}-Dg6"] = (g, "Dg"); sec[f"{g}-Dp"] = (g, "Dp")
        pairs = {"B1 DIV-DA": ("DA+DIV", "DA"), "B2 DIV-SELR": ("DA+DIV", "DA+SELR"), "B3 DIV-SEL4": ("DA+DIV", "DA+SEL4"), "B4 SELL-DA": ("DA+SELL", "DA"), "B5 Dp+SELW-Dp": ("Dp+SELW", "Dp")}
        sl = {}
        for a in ("DA+DIV", "DA+SELL", "Dp+SELW"):
            L = [res[f"{sc}|{s}"]["conds"][a]["sel_log"] for sc in SC for s in seeds]; sl[a] = {k: float(np.mean([np.mean([x[k] for x in l]) for l in L])) for k in ("front4_share", "divergence", "U_mean_sel", "U_mean_all")}
        rep["selection_diagnostics"] = sl
    for k, (a, b) in sec.items():
        dd = H[a] - H[b]; bm = dd[idx].mean(1); rep["secondary"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))])
    for k, (a, b) in pairs.items(): rep["per_scenario"][k] = {sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC}
    save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m.startswith("precheck"): sys.exit(0 if precheck(m[-1], sys.argv[2], sys.argv[3]) else 1)
    elif m.startswith("final"): final(m[-1], sys.argv[2], sys.argv[3], sys.argv[4])
