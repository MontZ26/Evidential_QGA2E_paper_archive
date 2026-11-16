"""P8 runner (absolute paths, resumable). Modes:
  gc   OUTDIR            G-C: tau for V0c-tau (entropy matching) + B-cal affine fit, seeds 8100-8114, SC3 (no freeze needed; written to p8_tau.json before freeze)
  pilot OUTDIR FREEZE    seeds 8150-8179, main arms, SC6
  conf  OUTDIR FREEZE    seeds 8200..8200+n-1 (n from p8_n.json), main arms + DV2, SC6"""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, p8
K, P = p8.K, p8.P; B8 = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p8"
GRID_W = [round(0.10 + 0.05 * i, 2) for i in range(18)] + [0.99, 0.999]
MAIN = ["A", "B", "C", "D", "Cp", "Dp", "Dt", "DV2"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w")); os.replace(tmp, p)
def gc_job(a):
    sc, seed, w = a; I = P.build(sc, seed)
    if not I["feasible"]: return (a, None)
    W = p8.worlds_for(I); diag = dict(ent=True)
    if w == "V1": o = p8.run_one(I, "nom", "V1", diag=diag, wd=W)
    else: o = p8.run_one(I, "nom", "V0c-tau", tau=w, diag=diag, wd=W)
    ent = float(np.mean([e for _, e in o["ent"]])) if o["ent"] else float("nan")
    me = float(np.mean([m["m_empty"] for _, m in o["mdiag"]])) if o["mdiag"] else float("nan")
    mx = float(np.mean([m.get("betp_vs_freq_L1", 0.0) for _, m in o["mdiag"]])) if o["mdiag"] else float("nan")
    return (a, dict(ent=ent, m_empty=me, hv_oracle=o["hv_oracle"], n_eval=o["n_eval"]))
def bcal_job(a):
    sc, seed = a; I = P.build(sc, seed)
    if not I["feasible"]: return None
    nom = p8.worlds_for(I)["nom"][0]; c = I["CT"] == 1; return (nom[c].tolist(), I["A_true"][c].tolist())
def gc(outdir):
    os.makedirs(outdir, exist_ok=True); seeds = range(8100, 8115); jobs = [(sc, s, w) for sc in p8.SC3 for s in seeds for w in ["V1"] + GRID_W]
    with Pool(2) as pool: out = pool.map(gc_job, jobs, chunksize=4)
    by = {}
    for a, r in out:
        if r is not None: by.setdefault(str(a[2]), []).append(r)
    summ = {w: dict(n=len(v), ent=float(np.mean([x["ent"] for x in v])), m_empty=float(np.mean([x["m_empty"] for x in v])), hv=float(np.mean([x["hv_oracle"] for x in v])), budgets_ok=all(x["n_eval"] == 6040 for x in v)) for w, v in by.items()}
    e1 = summ["V1"]["ent"]; cand = [(abs(summ[str(w)]["ent"] - e1), w) for w in GRID_W]; best = min(cand)[1]
    with Pool(2) as pool: bc = [x for x in pool.map(bcal_job, [(sc, s) for sc in p8.SC3 for s in seeds]) if x]
    x = np.concatenate([np.array(a) for a, _ in bc]); y = np.concatenate([np.array(b) for _, b in bc]); slope, icpt = np.polyfit(x, y, 1)
    res = dict(tau=best, V1_entropy=e1, tau_entropy=summ[str(best)]["ent"], matched_within=abs(summ[str(best)]["ent"] - e1), summary=summ, bcal=dict(slope=float(slope), intercept=float(icpt), n_cells=int(len(x)), corr=float(np.corrcoef(x, y)[0, 1])),
               note="tau chosen on calibration seeds 8100-8114 only; if matched_within is large the grid could not match V1 concentration")
    save(res, outdir + "/gc_results.json"); save(dict(tau=best, bcal=res["bcal"]), B8 + "/p8_tau.json"); print(json.dumps({k: res[k] for k in ("tau", "V1_entropy", "tau_entropy", "matched_within", "bcal")}))
def full_job(a):
    phase, sc, seed, outdir = a; path = f"{outdir}/{sc}__{seed}.json"
    if os.path.exists(path): return path
    t0 = time.time(); tau = json.load(open(B8 + "/p8_tau.json"))["tau"]; diag = dict(ent=True) if seed % 10 == 0 else None
    r = p8.task8(sc, seed, MAIN, tau=tau, diag=diag); r["wall_s"] = time.time() - t0; save(r, path); return path
def full_phase(phase, seeds, outdir, maxsec, nproc=2):
    os.makedirs(outdir, exist_ok=True); jobs = [(phase, sc, s, outdir) for s in seeds for sc in p8.SC6 if not os.path.exists(f"{outdir}/{sc}__{s}.json")]
    print(phase, len(jobs), "jobs", flush=True); t0 = time.time(); i = 0
    with Pool(nproc) as pool:
        while i < len(jobs) and time.time() - t0 < maxsec:
            b = jobs[i:i + 12]; i += len(b); pool.map(full_job, b, chunksize=1); print(f"{i}/{len(jobs)} {time.time() - t0:.0f}s", flush=True)
    print("ALL DONE" if i >= len(jobs) else "PARTIAL", flush=True)
if __name__ == "__main__":
    mode, outdir = sys.argv[1], sys.argv[2]; maxsec = float(os.environ.get("P8_MAXSEC", "3000")); assert os.path.isabs(outdir)
    if mode == "gc": gc(outdir)
    else:
        assert K.R.verify_freeze(sys.argv[3]), "P8 freeze verification failed: refusing to run"
        if mode == "pilot": full_phase("pilot", range(8150, 8180), outdir, maxsec)
        elif mode == "conf": n = json.load(open(B8 + "/p8_n.json"))["n"]; full_phase("conf", range(8200, 8200 + n), outdir, maxsec)
