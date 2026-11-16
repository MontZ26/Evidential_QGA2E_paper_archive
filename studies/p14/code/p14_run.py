"""P14 runner. python p14_run.py OUTDIR SEED_LO SEED_HI FREEZE (descriptive, no pilot). 6 scenarios x 9 arms."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p14
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p14"; PRM = json.load(open(B + "/p14_params.json"))["chosen"]; ARMS = list(p14.ARMS14); OUT = None
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{OUT}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p14.task14(sc, seed, ARMS, PRM); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(o): globals()["OUT"] = o
if __name__ == "__main__":
    outdir, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); assert os.path.isabs(outdir)
    assert os.path.isabs(sys.argv[4]) and p14.R.verify_freeze(sys.argv[4]), "freeze verification failed"
    os.makedirs(outdir, exist_ok=True); jobs = [(sc, s) for s in range(lo, hi + 1) for sc in p14.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(outdir,)) as pool:
        for i in range(0, len(jobs), 24): pool.map(job, jobs[i:i + 24], chunksize=1); print(f"{min(i + 24, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
