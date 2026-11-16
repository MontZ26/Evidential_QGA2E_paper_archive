"""P9 analysis. python p9_an.py precheck CONFDIR FREEZE | final CONFDIR OUT.json FREEZE (RUN ONCE)"""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R
ARMS = ["E", "P", "X", "Dp", "B", "Bp"]; SC = S.SC
def load(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")): r = json.load(open(f)); out[(r["sc"], r["seed"])] = r
    return out
def precheck(d, fr):
    bad = []
    if not R.verify_freeze(fr): bad.append("freeze")
    res = load(d); seeds = sorted({s for _, s in res})
    if seeds != list(range(9000, 9200)): bad.append(f"seeds {len(seeds)}")
    if len(res) != 1200: bad.append(f"shards {len(res)}")
    for k, r in res.items():
        if not r.get("feasible"): bad.append(f"infeasible {k}"); continue
        for a in ARMS:
            c = r["conds"].get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def final(d, out, fr):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, fr); res = load(d); seeds = sorted({s for _, s in res})
    H = {a: np.array([np.mean([res[(sc, s)]["conds"][a]["hv_oracle"] for sc in SC]) for s in seeds]) for a in ARMS}
    prim = H["E"] - H["P"]; sec = {"E-X": H["E"] - H["X"], "Dp-P": H["Dp"] - H["P"], "E-Dp": H["E"] - H["Dp"], "X-P": H["X"] - H["P"], "interaction E-Dp-X+P": H["E"] - H["Dp"] - H["X"] + H["P"], "B-Bp": H["B"] - H["Bp"], "E-B": H["E"] - H["B"], "P-Bp": H["P"] - H["Bp"]}
    n = len(seeds); rng = S.sub_rng("p9final", 9802); idx = rng.randint(0, n, size=(S.B_DEF, n)).astype(np.int32); p, inf = S.boot_t(prim, rng, S.B_DEF, idx); bm = prim[idx].mean(1)
    rep = dict(n=n, hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, primary_E_minus_P=dict(mean=float(prim.mean()), sd=float(prim.std(ddof=1)), p_raw=p, info=inf, ci95_boot=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))], share_pos=float((prim > 0).mean()), reject_0_05=bool(p < 0.05)), secondary_descriptive={})
    for k, dd in sec.items():
        pp, _ = S.boot_t(dd, rng, S.B_DEF, idx); b = dd[idx].mean(1); rep["secondary_descriptive"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], p_raw_descriptive=pp, share_pos=float((dd > 0).mean()))
    json.dump(rep, open(out, "w"), indent=1, default=str); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
