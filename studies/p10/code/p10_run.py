"""P10 runner. python p10_run.py OUTDIR SEED_LO SEED_HI [FREEZE]. 6 scenarios x 10 arms (E,P,X,Dp,A,B,Bp,E_DEC,P_DEC + C0 classical GA reference); params from p10_calib.json (chosen)."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p10
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10"; PRM = json.load(open(B + "/p10_calib.json"))["chosen"]; ARMS = list(p10.ARMS10); OUT = None
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def job(a):
    sc, seed = a; path = f"{OUT}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); r = p10.task10(sc, seed, ARMS, PRM); r["wall_s"] = time.time() - t0; save(r, path); return path
def init(o): globals()["OUT"] = o
if __name__ == "__main__":
    outdir, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); assert os.path.isabs(outdir)
    if len(sys.argv) > 4: assert os.path.isabs(sys.argv[4]) and p10.R.verify_freeze(sys.argv[4]), "freeze verification failed"
    os.makedirs(outdir, exist_ok=True); jobs = [(sc, s) for s in range(lo, hi + 1) for sc in p10.p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]; print(len(jobs), "jobs", flush=True); t0 = time.time()
    with Pool(2, initializer=init, initargs=(outdir,)) as pool:
        for i in range(0, len(jobs), 24): pool.map(job, jobs[i:i + 24], chunksize=1); print(f"{min(i + 24, len(jobs))}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)
