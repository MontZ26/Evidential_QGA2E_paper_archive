"""P15 pilot analysis (descriptive). python p15_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE (RUN ONCE)."""
import sys, os, json, glob, math
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R
from scipy.stats import spearmanr
ARMS = ["E", "Dp", "Dg", "DA", "PDA", "V2"]; SC = S.SC; GENS = [1, 25, 50, 100, 150]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")): r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def precheck(d, freeze):
    bad = []
    if not R.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(10900, 10930)): bad.append(f"seeds {len(seeds)}")
    if len(res) != 180: bad.append(f"{len(res)} shards")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append(f"infeasible {k}"); continue
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def final(d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
    H = {a: np.array([np.mean([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for sc in SC]) for s in seeds]) for a in ARMS}
    rng = S.sub_rng("p15pilot", 10990); idx = rng.randint(0, n, size=(20000, n)).astype(np.int32)
    pairs = [("DA", "E"), ("DA", "PDA"), ("DA", "V2"), ("DA", "Dg"), ("DA", "Dp"), ("E", "Dp"), ("E", "V2"), ("E", "Dg"), ("PDA", "Dp"), ("V2", "Dp")]
    rep = dict(status="PILOT, DESCRIPTIVE ONLY", n_seeds=n, hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, contrasts={}, sizing_indicative={})
    for a, b in pairs:
        dd = H[a] - H[b]; bm = dd[idx].mean(1); sd = float(dd.std(ddof=1)); rep["contrasts"][f"{a}-{b}"] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))], sd=sd, share_pos=float((dd > 0).mean()))
        rep["sizing_indicative"][f"{a}-{b}"] = int(math.ceil(((1.96 + 0.8416) * sd / 0.01) ** 2))
    keys = ("m_theta", "m_empty", "q_ent", "q_max", "neff_ratio", "alpha_mean", "dep", "neff", "marg_ent"); diag = {}
    for a in ARMS:
        rows = [res[f"{sc}|{s}"]["conds"][a]["dyn"] for sc in SC for s in seeds]; diag[a] = {}
        for k in keys:
            diag[a][k] = {str(g): (float(np.mean([r[g][k] for r in rows if k in r[g]])) if any(k in r[g] for r in rows) else None) for g in GENS}
    rep["diagnostics_by_generation"] = diag
    gen_ok = [float(np.mean([res[f"{sc}|{s}"]["conds"]["DA"]["dyn"][g]["m_theta"] for sc in SC for s in seeds]) >= np.mean([res[f"{sc}|{s}"]["conds"]["E"]["dyn"][g]["m_theta"] for sc in SC for s in seeds]) - 1e-12) for g in range(1, 151)]
    rep["H1_share_of_generations_mean_mTheta_DA_ge_E"] = float(np.mean(gen_ok))
    qm = {a: float(np.mean([np.mean([x["q_max"] for x in res[f"{sc}|{s}"]["conds"][a]["dyn"] if "q_max" in x]) for sc in SC for s in seeds])) for a in ARMS}; rep["H2_mean_q_max_over_generations"] = qm
    cor = {}
    for a in ARMS:
        rs = []
        for sc in SC:
            hh = [res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]; mm = [np.mean([x["m_theta"] for x in res[f"{sc}|{s}"]["conds"][a]["dyn"] if "m_theta" in x]) for s in seeds]
            if np.std(mm) > 0 and np.std(hh) > 0: rs.append(float(spearmanr(mm, hh)[0]))
        cor[a] = dict(per_scenario=rs, mean=float(np.mean(rs)) if rs else None)
    rep["H4_within_scenario_spearman_mTheta_vs_HV"] = cor; save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
