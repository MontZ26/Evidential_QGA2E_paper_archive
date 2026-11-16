"""P9 confirmatory runner. Usage: python p9_run.py OUTDIR FREEZE (absolute paths); seeds 9000-9199, 6 scenarios, 6 arms; resumable."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p9, p8
OUT = None
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{OUT}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p9.task9(sc, seed); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(o): globals()["OUT"] = o
if __name__ == "__main__":
    outdir, freeze = sys.argv[1], sys.argv[2]; assert os.path.isabs(outdir) and os.path.isabs(freeze); assert p8.K.R.verify_freeze(freeze), "freeze verification failed"
    os.makedirs(outdir, exist_ok=True); jobs = [(sc, s) for s in range(9000, 9200) for sc in p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(outdir,)) as pool:
        for i in range(0, len(jobs), 24): pool.map(job, jobs[i:i + 24], chunksize=1); print(f"{min(i + 24, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
