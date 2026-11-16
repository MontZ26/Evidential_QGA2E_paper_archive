"""Dry run of the analysis code on SYNTHETIC data built from the technical pilot files (HV perturbed with random noise; not real results). Bypasses the freeze check only. Output to a temp path, never to the real analysis file."""
import sys, os, json, glob, random, shutil; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p23_an as A
B = A.B; src = sorted(glob.glob(B + "/p23/pilot_runs/*.json")); d = B + "/p23/dry_synth"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d); rng = random.Random(1); ref = {}
for f in src: o = json.load(open(f)); ref.setdefault(o["sc"], o)
for sc in A.SC:
    base = ref.get(sc) or next(iter(ref.values()))
    for s in range(12000, 12100):
        o = json.loads(json.dumps(base)); o["sc"] = sc; o["seed"] = s
        for c in o["conds"].values(): c["hv_oracle"] = c["hv_oracle"] + rng.gauss(0, 0.01)
        json.dump(o, open(f"{d}/{sc}__{s}.json", "w"))
A.R0.verify_freeze = lambda p: True; out = B + "/p23/dry_synth_analysis.json"
if os.path.exists(out): os.remove(out)
A.final(d, out, "x"); print("DRY RUN OK")
