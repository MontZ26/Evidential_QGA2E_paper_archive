"""P18 runner. python p18_run.py A|B OUTDIR FREEZE  (A: seeds 11400-11459, arms ARMS_A ; B: seeds 11200-11259, arms ARMS_B). HV stored, never read here."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p18
PRM = json.load(open(p18.BASE + "/p15/p15_params.json"))["chosen"]; CFG = {}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{CFG['out']}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p18.task18(sc, seed, CFG["arms"], PRM); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(c): CFG.update(c)
if __name__ == "__main__":
    part, outdir, freeze = sys.argv[1:4]; assert os.path.isabs(outdir) and os.path.isabs(freeze) and p18.p17.R.verify_freeze(freeze), "freeze verification failed"; os.makedirs(outdir, exist_ok=True)
    seeds = range(11400, 11460) if part == "A" else range(11200, 11260); arms = p18.ARMS_A if part == "A" else p18.ARMS_B
    jobs = [(sc, s) for s in seeds for sc in p18.p17.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(part, len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(dict(out=outdir, arms=arms),)) as pool:
        for i in range(0, len(jobs), 12): pool.map(job, jobs[i:i + 12], chunksize=1); print(f"{min(i + 12, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", part, flush=True)
