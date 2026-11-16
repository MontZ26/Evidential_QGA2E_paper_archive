"""P19 runner. python p19_run.py OUTDIR FREEZE : arms DAg6 (gamma 6) and DAgm (gamma_m from the HV-blind calibration), SC6 x seeds 11200-11259. HV stored, never read here."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p19
PRM = json.load(open(p19.BASE + "/p15/p15_params.json"))["chosen"]; GM = json.load(open(p19.BASE + "/p19/p19_gamma.json"))["gamma_m"]; ARMS = {"DAg6": 6.0, "DAgm": GM}; CFG = {}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{CFG['out']}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p19.task19(sc, seed, ARMS, PRM); r["wall_s"] = time.time() - t0; r["gamma_m"] = GM; save(r, path); return path
def init(c): CFG.update(c)
if __name__ == "__main__":
    outdir, freeze = sys.argv[1:3]; assert os.path.isabs(outdir) and os.path.isabs(freeze) and p19.R.verify_freeze(freeze), "freeze verification failed"; os.makedirs(outdir, exist_ok=True)
    jobs = [(sc, s) for s in range(11200, 11260) for sc in p19.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs, gamma_m", GM, flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(dict(out=outdir),)) as pool:
        for i in range(0, len(jobs), 12): pool.map(job, jobs[i:i + 12], chunksize=1); print(f"{min(i + 12, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
