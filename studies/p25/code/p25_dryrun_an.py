"""Dry run of p25_an.final on synthetic data (random HV, fake dyn); verifies the pipeline end-to-end. No real HV."""
import sys, os, json, numpy as np, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p25_an as A
B = A.B; D = B + "/p25/dry_synth"; shutil.rmtree(D, ignore_errors=True); os.makedirs(D); rng = np.random.RandomState(1)
for s in range(14000, 14060):
    for sc in A.SC6:
        conds = {a: dict(n_eval=6040, hv_oracle=float(0.5 + 0.02 * rng.randn()), dyn=[dict(q_ent=1.0 + rng.rand() * .1, q_max=0.4 + rng.rand() * .1) for _ in range(151)]) for a in A.ARMS}
        json.dump(dict(sc=sc, seed=s, feasible=True, conds=conds), open(f"{D}/{sc}__{s}.json", "w")); np.savez(f"{D}/{sc}__{s}.npz", M=np.ones((3, 3)))
A.R0.verify_freeze = lambda f: True
out = D + "/dry_out.json"; A.final(D, out, "x"); print("DRY OK", os.path.exists(out))
