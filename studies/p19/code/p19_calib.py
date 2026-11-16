"""P19 calibration (HV-BLIND): gamma_m for DA-hardened so that target entropy and q_max match Dg(gamma=6). SC3 x seeds 11700-11714. No HV is used. Run once."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p19; from p19 import p15, P
from multiprocessing import Pool
B = p19.BASE; PRM = json.load(open(B + "/p15/p15_params.json"))["chosen"]; GG = [1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0]; OUT = B + "/p19/p19_calib.json"
def ser(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"] if "q_ent" in d]
def job(a):
    sc, seed = a; I = P.build(sc, seed); W = p19.p9.worlds9(I); o = dict(Dg=ser(p19.run_arm19(I, "Dg", PRM, W)))
    for g in GG: o[g] = ser(p19.run_arm19(I, "DAg", dict(PRM, gamma_da=g), W))
    return o
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(11700, 11715) for sc in p19.p8.SC3]
    with Pool(1) as p: res = p.map(job, jobs, chunksize=1)
    Hm = lambda k: float(np.mean([np.mean([x[0] for x in r[k]]) for r in res])); Qm = lambda k: float(np.mean([np.mean([x[1] for x in r[k]]) for r in res]))
    HD, QD = Hm("Dg"), Qm("Dg"); tab = {}
    for g in GG: tab[str(g)] = dict(entropy=Hm(g), qmax=Qm(g), rel_entropy_gap=abs(Hm(g) - HD) / HD, abs_qmax_gap=abs(Qm(g) - QD), gate=bool(abs(Hm(g) - HD) / HD <= 0.10 and abs(Qm(g) - QD) <= 0.05))
    ok = [g for g in GG if tab[str(g)]["gate"]]; pool = ok if ok else GG; gm = min(pool, key=lambda g: tab[str(g)]["rel_entropy_gap"])
    json.dump(dict(Dg_target=dict(entropy=HD, qmax=QD), table=tab, gamma_m=gm, gate_satisfied=bool(ok), rule="gamma_m = argmin relative entropy gap to Dg(6) among grid values passing the gate (rel entropy gap <= 0.10 and |qmax gap| <= 0.05); if none passes, argmin over the whole grid (declared best attempt). Means over generations with diagnostics, runs SC3 x 11700-11714. HV not read."), open(OUT, "w"), indent=1); print(json.dumps(tab, indent=1), "gamma_m", gm, "gate", bool(ok))
