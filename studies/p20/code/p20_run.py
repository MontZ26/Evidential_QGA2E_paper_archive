"""P10 v3 runner. python p20_run.py OUTDIR FREEZE : arms Eg1.5, Eg2, Eg4, Eg6 ; SC6 x seeds 10400-10499 ; HV stored, never read here."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p20
ARMS = ["Eg1.5", "Eg2", "Eg4", "Eg6"]; CFG = {}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{CFG['out']}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p20.task20(sc, seed, ARMS); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(c): CFG.update(c)
if __name__ == "__main__":
    outdir, freeze = sys.argv[1:3]; assert os.path.isabs(outdir) and os.path.isabs(freeze)
    sys.path.insert(0, p20.BASE + "/p5"); import run_p1m as R0; assert R0.verify_freeze(freeze), "freeze verification failed"; os.makedirs(outdir, exist_ok=True)
    jobs = [(sc, s) for s in range(10400, 10500) for sc in p20.p14.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(dict(out=outdir),)) as pool:
        for i in range(0, len(jobs), 12): pool.map(job, jobs[i:i + 12], chunksize=1); print(f"{min(i + 12, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
