"""P14 calibration (HV-blind): gamma for D'_gamma (match E target entropy and q_max), gamma_e for E_soft (descriptive). SC3 x seeds 10300-10314. No HV is used."""
import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p14/code")
import p14
from multiprocessing import Pool
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p14"
BASEPRM = dict(json.load(open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10/p10_calib.json"))["chosen"])
GG = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0]; GE = [1.0, 0.75, 0.5, 0.35, 0.25, 0.15]
def series(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"] if "q_ent" in d]
def job(a):
    sc, seed = a; I = p14.P.build(sc, seed); W = p14.p9.worlds9(I); out = dict(sc=sc, seed=seed)
    out["E"] = series(p14.run_arm14(I, "E", dict(BASEPRM, gamma=1.0, gamma_e=1.0), W))
    out["Dg"] = {g: series(p14.run_arm14(I, "Dg", dict(BASEPRM, gamma=g, gamma_e=1.0), W)) for g in GG}
    out["Es"] = {g: series(p14.run_arm14(I, "Es", dict(BASEPRM, gamma=1.0, gamma_e=g), W)) for g in GE}
    return out
if __name__ == "__main__":
    jobs = [(sc, s) for s in range(10300, 10315) for sc in p14.p8.SC3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    def stats(key, grid, ref_key, ref):
        out = {}
        for g in grid:
            he = [np.mean([x[0] for x in r[ref_key]]) for r in res] if ref is None else None
        return out
    S = {}
    Hm = lambda ser: float(np.mean([x[0] for x in ser])); Qm = lambda ser: float(np.mean([x[1] for x in ser]))
    HE = float(np.mean([Hm(r["E"]) for r in res])); QE = float(np.mean([Qm(r["E"]) for r in res])); HD = float(np.mean([Hm(r["Dg"][1.0]) for r in res])); QD = float(np.mean([Qm(r["Dg"][1.0]) for r in res]))
    S["E_target"] = dict(entropy=HE, qmax=QE); S["Dprime_target"] = dict(entropy=HD, qmax=QD); S["Dg"] = {}; S["Es"] = {}
    for g in GG:
        H = float(np.mean([Hm(r["Dg"][g]) for r in res])); Q = float(np.mean([Qm(r["Dg"][g]) for r in res]))
        within = [abs(a[0] - b[0]) / b[0] <= 0.10 and abs(a[1] - b[1]) <= 0.05 for r in res for a, b in zip(r["Dg"][g], r["E"])]
        dH = [a[0] - b[0] for r in res for a, b in zip(r["Dg"][g], r["E"])]; dQ = [a[1] - b[1] for r in res for a, b in zip(r["Dg"][g], r["E"])]
        S["Dg"][str(g)] = dict(entropy=H, qmax=Q, rel_entropy_gap=abs(H - HE) / HE, abs_qmax_gap=abs(Q - QE), pass_gate=bool(abs(H - HE) / HE <= 0.10 and abs(Q - QE) <= 0.05), prop_obs_within=float(np.mean(within)), dH_q=[float(np.quantile(dH, q)) for q in (.1, .5, .9)], dQ_q=[float(np.quantile(dQ, q)) for q in (.1, .5, .9)])
    for g in GE:
        H = float(np.mean([Hm(r["Es"][g]) for r in res])); Q = float(np.mean([Qm(r["Es"][g]) for r in res])); S["Es"][str(g)] = dict(entropy=H, qmax=Q, rel_entropy_gap_to_Dprime=abs(H - HD) / HD, abs_qmax_gap=abs(Q - QD))
    ok = [g for g in GG if S["Dg"][str(g)]["pass_gate"]]; gamma = min(ok, key=lambda g: S["Dg"][str(g)]["rel_entropy_gap"]) if ok else None
    ge = min(GE, key=lambda g: S["Es"][str(g)]["rel_entropy_gap_to_Dprime"]); chosen = dict(BASEPRM, gamma=gamma, gamma_e=ge)
    out = dict(summary=S, G_N_pass=gamma is not None, chosen=chosen, best_attempt_gamma=min(GG, key=lambda g: S["Dg"][str(g)]["rel_entropy_gap"]))
    json.dump(out, open(B + "/p14_calib.json", "w"), indent=1); print(json.dumps(out, indent=1))
