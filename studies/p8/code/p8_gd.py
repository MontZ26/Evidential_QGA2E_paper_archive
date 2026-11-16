"""P8 gate G-D — reconstruction and verification of the data-evidence layer (layer I) of the original P1-M implementation (p1m.py, frozen/unchanged). Technical seeds 8000-8009 (descriptive; no hypothesis test).
Part V: independent re-implementation (general mass functions on the frame {A, notA}: Shafer discounting, unnormalised conjunctive combination, conflict K recorded, Yager transfer to Theta, Bel/Pl/BetP) compared cell by cell with p1m.a_masses / s_masses;
        invariants; nominal/low/high world ordering; objective monotonicity; calibration of the evidence intervals against the hidden truth (descriptive).
Part E: engine comparator: the SAME classical GA (frozen P5 C0b = NSGA-II + auxiliary operators, no quantum operator) optimises in the oracle world (upper bound), the nominal evidential world, a probabilistic-average comparator
        (each source -> BetP, then averaged) and a history-only world; every archive is re-evaluated in the oracle world (HV, ref point 1.2). Isolates the contribution of the data layer from the old quantum operators.
Usage: python p8_gd.py OUT.json LOG.txt"""
import sys, os, json, math, time
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7/code")
import p7_g0 as G0
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5")
import p5 as K
P, R, X = K.P, K.R, K.X
class _S8:
    def __contains__(self, s): return 8000 <= s <= 8009
P.ALLOWED_SEEDS = _S8()
A_, N_, T_ = 1, 2, 3
def weak(m, r): return {x: (r * v if x != T_ else 1 - r * (1 - v)) for x, v in m.items()} if True else m
def clean(m): return {k: v for k, v in m.items() if v != 0 or k == T_}
def cell_A(I, t, k, hx, hn):
    ev = I["ev"]; cov = bool(ev["doc_cov"][t, k]) and (not I["unv"][t, k]) and I["CT"][t, k] == 1
    doc = {A_: 0.5, T_: 0.5} if cov else {T_: 1.0}
    y = float(ev["yhat"][t, k]); s = abs(2 * y - 1); sup = {A_: s, T_: 1 - s} if y >= 0.5 else {N_: s, T_: 1 - s}
    his = {A_: hx / (hn + 2.0), N_: (hn - hx) / (hn + 2.0), T_: 2.0 / (hn + 2.0)}
    d, s_, h = weak(doc, P.R_DOC), weak(sup, P.R_SUP), weak(his, P.R_HIS)
    m = G0.conj(G0.conj(d, s_), h); Kc = m.get(0, 0.0); mA, mN, mT = m.get(A_, 0.0), m.get(N_, 0.0), m.get(T_, 0.0) + Kc          # Yager: conflict -> Theta
    return dict(mA=mA, mN=mN, mT=mT, K=Kc, Bel=mA, Pl=mA + mT, betp=mA + mT / 2, srcs=(d, s_, h))
def run_V(log):
    res = dict(n_cells=0, max_dev=0.0, bad=[]); inv = dict(sum_bad=0, order_bad=0, K_bad=0, world_order_bad=0); st = dict(K=[], width=[], hidden_fail_cells=0, cov_A_nom=0, cov_A_n=0, below=0, above=0, cov_S=0, cov_S_n=0)
    mono_bad = 0; mono_n = 0; rng = np.random.RandomState(5)
    for sc in P.SC:
        for seed in range(8000, 8010):
            I = P.build(sc, seed)
            if not I["feasible"]: continue
            ev = I["ev"]; am = P.a_masses(I, ev["h_x"], ev["h_n"]); sm = P.s_masses(ev["v_x"], ev["v_n"]); n_t = I["n_t"]
            for t in range(n_t):
                for k in range(P.NK):
                    c = cell_A(I, t, k, ev["h_x"][t, k], ev["h_n"][t, k]); res["n_cells"] += 1
                    d = max(abs(c["mA"] - am["mA"][t, k]), abs(c["mN"] - am["mN"][t, k]), abs(c["mT"] - am["mT"][t, k]), abs(c["K"] - am["K"][t, k]), abs(c["Bel"] - am["Bel"][t, k]), abs(c["Pl"] - am["Pl"][t, k]))
                    res["max_dev"] = max(res["max_dev"], d)
                    if d > 1e-10: res["bad"].append((sc, seed, t, k, d))
                    inv["sum_bad"] += abs(c["mA"] + c["mN"] + c["mT"] - 1) > 1e-10; inv["order_bad"] += not (c["Bel"] <= c["betp"] + 1e-12 <= c["Pl"] + 2e-12); inv["K_bad"] += not (-1e-12 <= c["K"] <= 1 + 1e-12)
                    st["K"].append(c["K"]); st["width"].append(c["Pl"] - c["Bel"])
            for g in range(P.NG):                                     # S layer
                for t in range(n_t):
                    x, n = ev["v_x"][t, g], ev["v_n"][t, g]; mS, mN, mT = x / (n + 2.0), (n - x) / (n + 2.0), 2.0 / (n + 2.0)
                    d = max(abs(mS - sm["Bel"][t, g]), abs(mS + mT - sm["Pl"][t, g]), abs(mS + mT / 2 - sm["betp"][t, g]), abs(mT - sm["width"][t, g])); res["max_dev"] = max(res["max_dev"], d); res["n_cells"] += 1
                    if d > 1e-10: res["bad"].append((sc, seed, "S", t, g, d))
            stt = P.make_state(I); W = P.worlds(I, stt)
            for nm_ in ("nom", "low", "high"): pass
            inv["world_order_bad"] += int(np.any(W["low"][0] > W["nom"][0] + 1e-12) or np.any(W["nom"][0] > W["high"][0] + 1e-12) or np.any(W["low"][1] > W["nom"][1] + 1e-12) or np.any(W["nom"][1] > W["high"][1] + 1e-12))
            cert = I["CT"] == 1; At = I["A_true"]; lo, hi = W["low"][0], W["high"][0]; ins = cert & (At >= lo - 1e-12) & (At <= hi + 1e-12)
            st["cov_A_nom"] += int(ins.sum()); st["cov_A_n"] += int(cert.sum()); st["below"] += int((cert & (At < lo - 1e-12)).sum()); st["above"] += int((cert & (At > hi + 1e-12)).sum()); st["hidden_fail_cells"] += int((cert & (I["CT_true"] == 0)).sum())
            St = I["S_true"]; slo, shi = W["low"][1], W["high"][1]; st["cov_S"] += int(((St >= slo - 1e-12) & (St <= shi + 1e-12)).sum()); st["cov_S_n"] += St.size
            M = I["M"]
            for _ in range(5):                                          # objective monotonicity: better A,S => not worse objectives
                dec = np.array([rng.choice(np.flatnonzero(M[p])) for p in range(I["n_p"])]); fl, fn, fh = (P.evaluate(dec, I, *W[w_]) for w_ in ("low", "nom", "high")); mono_n += 1
                if not (fl[1] >= fn[1] - 1e-12 >= fh[1] - 2e-12 and fl[2] >= fn[2] - 1e-12 >= fh[2] - 2e-12 and abs(fl[0] - fh[0]) < 1e-12): mono_bad += 1
    # Shafer discounting extremes and conflict behaviour (general implementation)
    ext = {}
    m = {A_: 0.7, N_: 0.2, T_: 0.1}; ext["r1_identity"] = all(abs(weak(m, 1.0)[x] - m[x]) < 1e-12 for x in m); ext["r0_vacuous"] = abs(weak(m, 0.0)[T_] - 1.0) < 1e-12 and weak(m, 0.0)[A_] == 0.0
    c = G0.conj({A_: 0.6, T_: 0.4}, {N_: 0.6, T_: 0.4}); ext["conflict_K_0.36"] = abs(c[0] - 0.36) < 1e-12
    c = G0.conj({A_: 0.6, T_: 0.4}, {T_: 1.0}); ext["vacuous_neutral"] = abs(c[A_] - 0.6) < 1e-12 and c.get(0, 0) == 0
    res.update(invariants=inv, extremes=ext, monotonicity=dict(n=mono_n, bad=mono_bad), mean_K=float(np.mean(st["K"])), mean_width_A=float(np.mean(st["width"])), share_K_gt_0=float(np.mean(np.array(st["K"]) > 1e-12)),
               calib=dict(A_true_inside_low_high=st["cov_A_nom"] / max(st["cov_A_n"], 1), A_true_below_low=st["below"] / max(st["cov_A_n"], 1), A_true_above_high=st["above"] / max(st["cov_A_n"], 1),
                                                                    hidden_failed_certified_cells=st["hidden_fail_cells"] / max(st["cov_A_n"], 1), S_true_inside_low_high=st["cov_S"] / max(st["cov_S_n"], 1)))
    res["ok"] = bool(not res["bad"] and res["max_dev"] < 1e-10 and all(inv[k] == 0 for k in inv) and all(ext.values()) and mono_bad == 0); log.write(f"V: {json.dumps({k: v for k, v in res.items() if k != 'bad'}, default=str)}\n"); log.flush(); return res
def pavg_world(I):
    """probabilistic-average comparator: each of the three A sources -> BetP (A) after the same Shafer weakening, then equal-weight average; S as in the evidential world (single source: BetP)."""
    ev = I["ev"]; n_t = I["n_t"]; A = np.zeros((n_t, P.NK)); sm = P.s_masses(ev["v_x"], ev["v_n"])
    for t in range(n_t):
        for k in range(P.NK):
            if I["CT"][t, k] != 1: continue
            c = cell_A(I, t, k, ev["h_x"][t, k], ev["h_n"][t, k]); bs = [m.get(A_, 0.0) + m.get(T_, 0.0) / 2 for m in c["srcs"]]; A[t, k] = 0.25 + 0.60 * float(np.mean(bs))
    return A, sm["betp"]
def hist_world(I):
    ev = I["ev"]; xh = ev["h_x"] / (ev["h_n"] + 2.0) + 1.0 / (ev["h_n"] + 2.0); cert = I["CT"] == 1; return np.where(cert, 0.25 + 0.60 * xh, 0.0), P.s_masses(ev["v_x"], ev["v_n"])["betp"]
def run_E(log):
    prm = json.load(open(K.HERE + "/p5_tuned.json"))["C0b"]["prm"]; rows = []
    for sc in P.SC:
        for seed in range(8000, 8010):
            I = P.build(sc, seed)
            if not I["feasible"]: continue
            stt = P.make_state(I); worlds = {"T": (I["A_true"], I["S_true"]), "N": P.worlds(I, stt)["nom"], "Pavg": pavg_world(I), "Hist": hist_world(I)}; row = dict(sc=sc, seed=seed)
            for nm, w in worlds.items():
                Is = dict(I); Is["A_true"], Is["S_true"] = w; r = K.run(Is, "ga", "a", prm)
                D = r["D"]; real = np.array([P.evaluate(d, I, I["A_true"], I["S_true"]) for d in D]); row[nm] = dict(hv_oracle=float(R.hv(real)), hv_search=float(R.hv(np.asarray(r["front"]))), n_eval=r["n_eval"])
            rows.append(row); log.write(f"E {sc} {seed} " + " ".join(f"{k}={row[k]['hv_oracle']:.4f}" for k in worlds) + "\n"); log.flush()
    out = dict(n_instances=len(rows), hv_oracle_mean={a: float(np.mean([r[a]["hv_oracle"] for r in rows])) for a in ("T", "N", "Pavg", "Hist")}); diff = {}
    for a, b in (("N", "T"), ("Pavg", "T"), ("Hist", "T"), ("N", "Pavg"), ("N", "Hist"), ("Pavg", "Hist")):
        d = np.array([r[a]["hv_oracle"] - r[b]["hv_oracle"] for r in rows]); diff[f"{a}-{b}"] = dict(mean=float(d.mean()), se=float(d.std(ddof=1) / math.sqrt(len(d))), share_positive=float((d > 0).mean()))
    out["paired_differences_oracle_HV_descriptive"] = diff; out["all_budgets_exact"] = all(r[a]["n_eval"] == 6040 for r in rows for a in ("T", "N", "Pavg", "Hist")); out["rows"] = rows; return out
def main(out, logp):
    log = open(logp, "w"); V = run_V(log); E = run_E(log); res = dict(V=V, E=E, all_ok=bool(V["ok"] and E["all_budgets_exact"]))
    json.dump(res, open(out, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)); log.close(); print("V ok", V["ok"], "max_dev", V["max_dev"], "n_cells", V["n_cells"]); print(json.dumps({k: E[k] for k in ("n_instances", "hv_oracle_mean", "paired_differences_oracle_HV_descriptive", "all_budgets_exact")}, indent=1))
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
