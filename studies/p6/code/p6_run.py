"""P6 runner (protocol v2.6). Modes (absolute paths, resumable, atomic; every launch verifies the freeze file):
  calib PAIR OUTDIR FREEZE   PAIR in {C2|on, C2|off, C3|on, C3|off}: 50 cfg x seeds 6000-6004, top 5 x seeds 6005-6014, scenarios S4-*; each candidate run in BOTH arms (T, R); score = mean HV over both arms
  pilot OUTDIR FREEZE        seeds 6050-6079, 10 arms, six scenarios
  conf OUTDIR FREEZE         seeds 6200..6200+n-1 (n from p6_n.json)"""
import sys, os, json, math, time, zlib
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, p6
K, P = p6.K, p6.P
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6"
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
MK = {"C2": "rot", "C3": "pbil"}

def sample_one(pair, r):
    m, l = pair.split("|"); d = {}
    d["N"] = int(2 * r.randint(10, 51)); d["pc"] = float(r.uniform(0.5, 1.0)); d["eta_k"] = float(r.uniform(1.0, 5.0)); d["rho"] = float(r.uniform(0.2, 0.8))
    if m == "C2": d["delta"] = float(math.exp(r.uniform(math.log(0.005 * math.pi), math.log(0.15 * math.pi))))
    else: d["lam"] = float(math.exp(r.uniform(math.log(0.01), math.log(0.30))))
    d["eps"] = float([0.001, 0.005, 0.01, 0.02][r.randint(0, 4)]); d["k_e"] = int(r.randint(1, 11))
    if l == "on": d["p_LS"] = float(r.uniform(0.05, 0.25)); d["k_LS"] = int(r.randint(5, 51)); d["rule"] = ["dominance", "pondere"][r.randint(0, 2)]
    return d

def sample_configs(pair, n=50):
    r = np.random.RandomState(zlib.crc32(("p6calib|" + pair).encode()) % (2 ** 31)); out = []; seen = set()
    while len(out) < n:
        d = sample_one(pair, r); key = tuple((k, round(v, 5) if isinstance(v, float) else v) for k, v in sorted(d.items()))
        if key not in seen: seen.add(key); out.append(d)
    return out

def cal_job(a):
    pair, cid, prm, seed = a; m, l = pair.split("|"); out = {}
    for sc in p6.SC3:
        I = P.build(sc, seed)
        if not I["feasible"]: continue
        o = {}
        for sel in ("T", "R"):
            r = p6.run6(I, MK[m], prm, l == "on", sel); o[sel] = dict(hv=float(K.R.hv(r["front"])), n_eval=r["n_eval"], t=r["search_time_s"])
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
        v = [np.mean([x[s_]["hv"] for x in res[f"{c}|{s}"].values() for s_ in ("T", "R")]) for s in seeds if f"{c}|{s}" in res and res[f"{c}|{s}"]]; out[c] = float(np.mean(v)) if v else float("nan")
    return out

def calib(pair, outdir, maxsec):
    os.makedirs(outdir, exist_ok=True); tag = pair.replace("|", "_"); cfgs = sample_configs(pair, 50); p1, p2 = f"{outdir}/calib1_{tag}.json", f"{outdir}/calib2_{tag}.json"
    r1 = json.load(open(p1)) if os.path.exists(p1) else {}
    jobs = [(pair, c, cfgs[c], s) for c in range(50) for s in range(6000, 6005) if f"{c}|{s}" not in r1]; print(pair, "stage1 jobs", len(jobs), flush=True)
    if jobs and not run_pool(cal_job, jobs, r1, p1, maxsec): print("PARTIAL", flush=True); return
    m1 = mean_hv(r1, range(50), range(6000, 6005)); top = sorted(range(50), key=lambda c: (-m1[c], c))[:5]
    r2 = json.load(open(p2)) if os.path.exists(p2) else {}
    jobs = [(pair, c, cfgs[c], s) for c in top for s in range(6005, 6015) if f"{c}|{s}" not in r2]; print(pair, "top5", top, "stage2 jobs", len(jobs), flush=True)
    if jobs and not run_pool(cal_job, jobs, r2, p2, maxsec): print("PARTIAL", flush=True); return
    m2 = mean_hv(r2, top, range(6005, 6015)); best = sorted(top, key=lambda c: (-m2[c], c))[0]
    sel = dict(pair=pair, chosen_cfg_id=best, chosen=cfgs[best], stage1_top5=top, stage1_mean_hv={str(c): m1[c] for c in range(50)}, stage2_mean_hv={str(c): m2[c] for c in top},
               n_eval_values=sorted({s_["n_eval"] for r in (r1, r2) for v in r.values() for x in v.values() for s_ in x.values()}),
               search_time_total_s=float(sum(s_["t"] for r in (r1, r2) for v in r.values() for x in v.values() for s_ in x.values())))
    save(sel, f"{outdir}/calib_selected_{tag}.json"); print("SELECTED", pair, best, cfgs[best], flush=True)
    tp = BASE + "/p6_tuned.json"; tuned = json.load(open(tp)) if os.path.exists(tp) else {}; tuned[pair] = dict(cfg_id=best, prm=cfgs[best]); save(tuned, tp)

def phase_cfgs():
    t = json.load(open(BASE + "/p6_tuned.json")); out = {}
    for m in ("C2", "C3"):
        for l in ("on", "off"):
            for s in ("T", "R"): out[f"{m}-{s}-{l}"] = dict(kind="p6", mkind=MK[m], prm=t[f"{m}|{l}"]["prm"], ls_on=(l == "on"), sel=s)
    c0 = json.load(open(K.HERE + "/p5_tuned.json"))["C0b"]["prm"]; out["C0b-T"] = dict(kind="ga", strat="a", prm=c0)
    c0o = dict(c0); c0o["p_LS"] = 0.0; out["C0b-T-off"] = dict(kind="ga", strat="a", prm=c0o); return out

def full_job(a):
    phase, sc, seed, outdir = a; path = f"{outdir}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); diag = dict(conv=(phase == "conf" and seed < 6220), ent=(phase == "conf" and seed < 6220), div=True)
    r = p6.task6(sc, seed, phase_cfgs(), diag); r["wall_s"] = time.time() - t0; save(r, path); return path

def full_phase(phase, seeds, outdir, maxsec, nproc=2):
    os.makedirs(outdir, exist_ok=True); jobs = [(phase, sc, s, outdir) for s in seeds for sc in p6.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]
    print(phase, len(jobs), "jobs to run", flush=True); t0 = time.time()
    if not jobs: print("ALL DONE", flush=True); return
    with Pool(nproc) as pool:
        i = 0
        while i < len(jobs) and time.time() - t0 < maxsec:
            b = jobs[i:i + 12]; i += len(b); pool.map(full_job, b, chunksize=1); print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    if i >= len(jobs): print("ALL DONE", flush=True)

if __name__ == "__main__":
    mode = sys.argv[1]; maxsec = float(os.environ.get("P6_MAXSEC", "6000"))
    if mode == "calib": pair, outdir, freeze = sys.argv[2], sys.argv[3], sys.argv[4]
    else: outdir, freeze = sys.argv[2], sys.argv[3]
    assert os.path.isabs(outdir) and K.R.verify_freeze(freeze), "P6 freeze verification failed: refusing to run"
    if mode == "calib": calib(pair, outdir, maxsec)
    elif mode == "pilot": full_phase("pilot", range(6050, 6080), outdir, maxsec)
    elif mode == "conf":
        n = json.load(open(BASE + "/p6_n.json"))["n"]; full_phase("conf", range(6200, 6200 + n), outdir, maxsec)
