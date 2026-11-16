"""P24 main runner. python p24_run.py OUTDIR FREEZE : all arms of p24_params.json x SC6 x seeds 12000-12099 (600 tasks). HV stored in json, per-patient decoded counts in npz; never read here."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, p24
sys.path.insert(0, p24.BASE + "/p5"); import run_p1m as RP
PRM = json.load(open(p24.BASE + "/p24/p24_params.json")); ARMS = PRM["arms"]; CFG = {}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{CFG['out']}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r, npz = p24.task24(sc, seed, ARMS); r["wall_s"] = time.time() - t0
    if npz: np.savez_compressed(f"{CFG['out']}/{sc}__{seed}.npz.tmp.npz", **npz); os.replace(f"{CFG['out']}/{sc}__{seed}.npz.tmp.npz", f"{CFG['out']}/{sc}__{seed}.npz")
    save(r, path); return path
def init(c): CFG.update(c)
if __name__ == "__main__":
    from multiprocessing import Pool
    outdir, freeze = sys.argv[1:3]; assert os.path.isabs(outdir) and os.path.isabs(freeze) and RP.verify_freeze(freeze), "freeze verification failed"; os.makedirs(outdir, exist_ok=True)
    jobs = [(sc, s) for s in range(12000, 12100) for sc in p24.p23.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(dict(out=outdir),)) as pool:
        for i in range(0, len(jobs), 12): pool.map(job, jobs[i:i + 12], chunksize=1); print(f"{min(i + 12, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
