"""P24 dry run of the analysis on SYNTHETIC data (random HV; rerun arms copied from stored P23 so the precheck equality passes). Never touches real P24 results. Run before freeze."""
import sys, os, json, numpy as np, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import p24, p24_an as A
B = p24.BASE; D = B + "/p24/dry_synth"; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
tpl_j = json.load(open(B + "/p24/pilot_runs/S4-C101__13900.json")); tpl_z = dict(np.load(B + "/p24/pilot_runs/S4-C101__13900.npz")); old = A.p23_runs(); rng = np.random.RandomState(5); R = A.ROLES
for s in range(12000, 12100):
    for sc in A.SC:
        r = json.loads(json.dumps(tpl_j)); r["sc"], r["seed"] = sc, s
        for a, c in r["conds"].items(): c["hv_oracle"] = float(0.5 + 0.03 * rng.randn())
        o = old[f"{sc}|{s}"]["conds"]; r["conds"][R["DA_w0.3"]]["hv_oracle"] = o["DA100"]["hv_oracle"]; r["conds"][R["Dg6_w0.3"]]["hv_oracle"] = o["Dg100"]["hv_oracle"]
        json.dump(r, open(f"{D}/{sc}__{s}.json", "w")); np.savez_compressed(f"{D}/{sc}__{s}.npz", **tpl_z)
A.R0.verify_freeze = lambda p: True
out = B + "/p24/dry_synth_analysis.json"
if os.path.exists(out): os.remove(out)
A.final(D, out, "unused"); print("DRYRUN OK", os.path.getsize(out))
