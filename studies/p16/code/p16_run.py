"""P16 runner. python p16_run.py calib OUTDIR | phaseD OUTDIR FREEZE THRESHOLDS.json"""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p16
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p16"; PRM = json.load(open(B + "/../p15/p15_params.json"))["chosen"]; CFG = {}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{CFG['out']}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p16.task16(sc, seed, CFG["arms"], PRM, CFG["th"]); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(c): CFG.update(c)
if __name__ == "__main__":
    mode, outdir = sys.argv[1], sys.argv[2]; assert os.path.isabs(outdir); os.makedirs(outdir, exist_ok=True)
    if mode == "calib": arms, scs, seeds, th = ["DA"], p16.p8.SC3, range(11100, 11115), None
    else:
        assert os.path.isabs(sys.argv[3]) and p16.R.verify_freeze(sys.argv[3]), "freeze verification failed"; th = json.load(open(sys.argv[4])); arms, scs, seeds = ["DA", "DA+S", "DA+L", "DA+P11"], p16.p8.SC6, range(11000, 11030)
    jobs = [(sc, s) for s in seeds for sc in scs if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(dict(out=outdir, arms=arms, th=th),)) as pool:
        for i in range(0, len(jobs), 12): pool.map(job, jobs[i:i + 12], chunksize=1); print(f"{min(i + 12, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
