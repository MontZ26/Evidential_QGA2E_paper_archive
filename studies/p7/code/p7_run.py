"""P7 runner (Amendement v0.3). Modes (absolute paths, resumable, atomic; each launch verifies the freeze file):
  calib OUTDIR FREEZE   shared configuration for V0c,V1,V2: 50 cfg x seeds 7100-7104, top 5 x seeds 7105-7114, scenarios S4-*; score = mean HV over the three arms
  pilot OUTDIR FREEZE   seeds 7150-7179, arms V0,V0c,V1,V2, six scenarios
  conf  OUTDIR FREEZE   seeds 7200..7200+n-1 (n from p7_n.json)"""
import sys, os, json, math, time, zlib
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, p7
K, P = p7.K, p7.P
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7"
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def sample_one(r):
    d = dict(N=int(2 * r.randint(10, 51)), pc=float(r.uniform(0.5, 1.0)), eta_k=float(r.uniform(1.0, 5.0)), w=float(r.uniform(0.10, 0.95)), eps=float([0.001, 0.005, 0.01, 0.02][r.randint(0, 4)]))
    d["p_LS"] = float(r.uniform(0.05, 0.25)); d["k_LS"] = int(r.randint(5, 51)); d["rule"] = ["dominance", "pondere"][r.randint(0, 2)]; return d
def sample_configs(n=50):
    r = np.random.RandomState(zlib.crc32(b"p7calib|shared") % (2 ** 31)); out = []; seen = set()
    while len(out) < n:
        d = sample_one(r); key = tuple((k, round(v, 5) if isinstance(v, float) else v) for k, v in sorted(d.items()))
        if key not in seen: seen.add(key); out.append(d)
    return out
def cal_job(a):
    cid, prm, seed = a; out = {}
    for sc in p7.SC3:
        I = P.build(sc, seed)
        if not I["feasible"]: continue
        o = {}
        for rule in p7.RULES:
            r = p7.run7(I, rule, prm); o[rule] = dict(hv=float(K.R.hv(r["front"])), n_eval=r["n_eval"], t=r["search_time_s"])
        out[sc] = o
    return (f"{cid}|{seed}", out)
def run_pool(fn, jobs, res, path, maxsec, nproc=2, batch=8):
    t0 = time.time(); i = 0
    with Pool(nproc) as pool:
        while i < len(jobs) and time.time() - t0 < maxsec:
            b = jobs[i:i + batch]; i += len(b)
            for k, v in pool.map(fn, b, chunksize=1): res[k] = v
            save(res, path)
    return i >= len(jobs)
def mean_hv(res, cids, seeds):
    out = {}
    for c in cids:
        v = [np.mean([x[s_]["hv"] for x in res[f"{c}|{s}"].values() for s_ in p7.RULES]) for s in seeds if f"{c}|{s}" in res and res[f"{c}|{s}"]]; out[c] = float(np.mean(v)) if v else float("nan")
    return out
def calib(outdir, maxsec):
    os.makedirs(outdir, exist_ok=True); cfgs = sample_configs(50); p1, p2 = f"{outdir}/calib1.json", f"{outdir}/calib2.json"
    r1 = json.load(open(p1)) if os.path.exists(p1) else {}
    jobs = [(c, cfgs[c], s) for c in range(50) for s in range(7100, 7105) if f"{c}|{s}" not in r1]; print("stage1 jobs", len(jobs), flush=True)
    if jobs and not run_pool(cal_job, jobs, r1, p1, maxsec): print("PARTIAL", flush=True); return
    m1 = mean_hv(r1, range(50), range(7100, 7105)); top = sorted(range(50), key=lambda c: (-m1[c], c))[:5]
    r2 = json.load(open(p2)) if os.path.exists(p2) else {}
    jobs = [(c, cfgs[c], s) for c in top for s in range(7105, 7115) if f"{c}|{s}" not in r2]; print("top5", top, "stage2 jobs", len(jobs), flush=True)
    if jobs and not run_pool(cal_job, jobs, r2, p2, maxsec): print("PARTIAL", flush=True); return
    m2 = mean_hv(r2, top, range(7105, 7115)); best = sorted(top, key=lambda c: (-m2[c], c))[0]
    save(dict(chosen_cfg_id=best, chosen=cfgs[best], stage1_top5=top, stage1_mean_hv={str(c): m1[c] for c in range(50)}, stage2_mean_hv={str(c): m2[c] for c in top}), f"{outdir}/calib_selected.json")
    save(dict(cfg_id=best, prm=cfgs[best]), BASE + "/p7_tuned.json"); print("SELECTED", best, cfgs[best], flush=True)
def phase_cfgs():
    t = json.load(open(BASE + "/p7_tuned.json"))["prm"]; c2 = json.load(open(K.HERE + "/p5_tuned.json"))["C2c"]["prm"]
    out = {"V0": dict(kind="rot", strat="c", prm=c2)}
    for r in p7.RULES: out[r] = dict(kind="p7", rule=r, prm=t)
    if os.path.exists(BASE + "/p7_m2_enabled.json"):
        for r in p7.RULES: out[r + "-M2"] = dict(kind="p7", rule=r, prm=t, m2=True)
    return out
def full_job(a):
    phase, sc, seed, outdir = a; path = f"{outdir}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); diag = dict(conv=(phase == "conf" and seed < 7220), ent=(phase == "conf" and seed < 7220), div=True)
    r = p7.task7(sc, seed, phase_cfgs(), diag); r["wall_s"] = time.time() - t0; save(r, path); return path
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
    if mode == "calib": calib(outdir, maxsec)
    elif mode == "pilot": full_phase("pilot", range(7150, 7180), outdir, maxsec)
    elif mode == "conf": n = json.load(open(BASE + "/p7_n.json"))["n"]; full_phase("conf", range(7200, 7200 + n), outdir, maxsec)
