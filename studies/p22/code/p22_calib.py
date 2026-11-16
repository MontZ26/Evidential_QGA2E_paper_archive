"""P22 calibration (HV-BLIND): gamma_m for the evidential mutation target so that mean entropy and q_max match GDg6. SC3 x seeds 11700-11714. No HV is read. Run once."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p22; from p22 import P
from multiprocessing import Pool
B = p22.BASE; GG = [1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0]; OUT = B + "/p22/p22_calib.json"
def ser(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"]]
def job(a):
    sc, seed = a; I = P.build(sc, seed); W = p22.p9.worlds9(I); o = dict(GDg6=ser(p22.run_arm22(I, "GDg6", p22.PRM, W)))
    for g in GG: o[str(g)] = ser(p22.run_arm22(I, "GEgm", p22.PRM, W, g))
    return o
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(11700, 11715) for sc in p22.p8.SC3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    Hm = lambda k: float(np.mean([np.mean([x[0] for x in r[k]]) for r in res])); Qm = lambda k: float(np.mean([np.mean([x[1] for x in r[k]]) for r in res]))
    HD, QD = Hm("GDg6"), Qm("GDg6"); tab = {}
    for g in GG: k = str(g); tab[k] = dict(entropy=Hm(k), qmax=Qm(k), rel_entropy_gap=abs(Hm(k) - HD) / HD, abs_qmax_gap=abs(Qm(k) - QD), gate=bool(abs(Hm(k) - HD) / HD <= 0.10 and abs(Qm(k) - QD) <= 0.05))
    json.dump(dict(GDg6_target=dict(entropy=HD, qmax=QD), table=tab, n_tasks=len(res), note="HV-blind: means of mutation-target entropy and q_max over generations then over 45 runs (SC3 x 11700-11714); no HV used"), open(OUT, "w"), indent=1); print(json.dumps(tab, indent=1), "CALIB DONE")
