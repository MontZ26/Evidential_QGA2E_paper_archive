"""P7 pilot/confirmation runner including the descriptive M2 arms (V0c-M2, V1-M2, V2-M2). Usage: p7_run2.py pilot|conf OUTDIR FREEZE. Resumable; verifies the freeze at each launch."""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p7, p7m2
K = p7.K; BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7"
ARMS = ["V0", "V0c", "V1", "V2", "V0c-M2", "V1-M2", "V2-M2"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def phase_cfgs():
    t = json.load(open(BASE + "/p7_tuned.json"))["prm"]; c2 = json.load(open(K.HERE + "/p5_tuned.json"))["C2c"]["prm"]; out = {"V0": dict(kind="rot", strat="c", prm=c2)}
    for r in p7.RULES: out[r] = dict(kind="p7", rule=r, prm=t)
    for r in p7.RULES: out[r + "-M2"] = dict(kind="p7", rule=r, prm=t, m2=True)
    return out
def full_job(a):
    phase, sc, seed, outdir = a; path = f"{outdir}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); diag = dict(conv=(phase == "conf" and seed < 7220), ent=(phase == "conf" and seed < 7220), div=True)
    r = p7m2.task7m2(sc, seed, phase_cfgs(), diag); r["wall_s"] = time.time() - t0; save(r, path); return path
def full_phase(phase, seeds, outdir, maxsec, nproc=2):
    os.makedirs(outdir, exist_ok=True); jobs = [(phase, sc, s, outdir) for s in seeds for sc in p7.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]
    print(phase, len(jobs), "jobs to run", flush=True); t0 = time.time()
    if not jobs: print("ALL DONE", flush=True); return
    with Pool(nproc) as pool:
        i = 0
        while i < len(jobs) and time.time() - t0 < maxsec:
            b = jobs[i:i + 12]; i += len(b); pool.map(full_job, b, chunksize=1); print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    if i >= len(jobs): print("ALL DONE", flush=True)
if __name__ == "__main__":
    mode, outdir, freeze = sys.argv[1], sys.argv[2], sys.argv[3]; maxsec = float(os.environ.get("P7_MAXSEC", "3000"))
    assert os.path.isabs(outdir) and K.R.verify_freeze(freeze), "P7 freeze verification failed: refusing to run"
    if mode == "pilot": full_phase("pilot", range(7150, 7180), outdir, maxsec)
    elif mode == "conf": n = json.load(open(BASE + "/p7_n.json"))["n"]; full_phase("conf", range(7200, 7200 + n), outdir, maxsec)
