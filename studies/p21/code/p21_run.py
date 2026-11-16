"""P21 runner. python p21_run.py PART(A|B) OUTDIR FREEZE. A: NSGA2,MOEAD x SC6 x 11200-11299. B: Eg1.1,Eg1.25,Eg0.9,Eg0.8 x SC6 x 10400-10499. HV stored, never read."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p21
CFG = {}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{CFG['out']}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p21.task21(sc, seed, CFG["arms"]); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(c): CFG.update(c)
if __name__ == "__main__":
    part, outdir, freeze = sys.argv[1:4]; assert part in "AB" and os.path.isabs(outdir) and os.path.isabs(freeze)
    sys.path.insert(0, p21.BASE + "/p5"); import run_p1m as R0; assert R0.verify_freeze(freeze), "freeze verification failed"; os.makedirs(outdir, exist_ok=True)
    arms = p21.ARMS_A if part == "A" else p21.ARMS_B; seeds = range(11200, 11300) if part == "A" else range(10400, 10500)
    jobs = [(sc, s) for s in seeds for sc in p21.p14.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(part, len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(dict(out=outdir, arms=arms),)) as pool:
        for i in range(0, len(jobs), 12): pool.map(job, jobs[i:i + 12], chunksize=1); print(f"{part} {min(i + 12, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print(f"PART {part} DONE", flush=True)
