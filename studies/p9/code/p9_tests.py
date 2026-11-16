"""G-I / G-P tests for P9. Usage: python p9_tests.py OUT.json (absolute)"""
import sys, json, glob
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p9/code")
import numpy as np, p9, p8
P = p9.P; res = {}; r = lambda w, a: w
def indep_A(I):
    ev = I["ev"]; Rd, Rs, Rh = P.R_DOC, P.R_SUP, P.R_HIS; cov = ev["doc_cov"].astype(bool) & (~I["unv"].astype(bool)) & (I["CT"] == 1)
    bd = np.where(cov, 0.5 + 0.25 * Rd, 0.5); y = ev["yhat"].astype(float); s = np.abs(2 * y - 1); bs = 0.5 + 0.5 * Rs * s * np.where(y >= 0.5, 1.0, -1.0)
    bh = (ev["h_x"] + 1.0) / (ev["h_n"] + 2.0) if Rh == 1.0 else None
    return np.where(I["CT"] == 1, 0.25 + 0.60 * (bd + bs + bh) / 3.0, 0.0)
dev = 0.0; budgets = True; leak = True; ranges = True; n = 0
for sc in ["S4-RC101", "S5-C101"]:
    for seed in [8900, 8901]:
        I = P.build(sc, seed)
        if not I["feasible"]: continue
        W = p9.worlds9(I); d = np.max(np.abs(W["pavg"][0] - indep_A(I))); dev = max(dev, float(d)); n += 1
        ranges &= bool(np.all((W["pavg"][0] >= 0) & (W["pavg"][0] <= 0.85 + 1e-12))) and np.array_equal(W["pavg"][1], W["nom"][1])
        for a, (w, w2) in p9.ARMS.items():
            o = p8.run_one(I, w, w2, wd=W); budgets &= o["n_eval"] == 6040
        I2 = dict(I); I2["A_true"] = I["A_true"] * 0.5 + 0.1; I2["S_true"] = np.clip(I["S_true"][::-1].copy(), 0, 1)
        for a in ("E", "P", "X", "B"):
            w, w2 = p9.ARMS[a]; o1 = p8.run_one(I, w, w2, wd=W); o2 = p8.run_one(I2, w, w2, wd=W); leak &= o1["F_search"] == o2["F_search"] and o1["D"] == o2["D"]
# reproducibility of arm E against P8 arm D on a P8 confirmatory seed
sc, seed = "S4-RC101", 8200; I = P.build(sc, seed); eo = p8.run_one(I, "nom", "V1"); ref = json.load(open(f"{p9.BASE}/p8/runs/conf/{sc}__{seed}.json"))["conds"]["D"]
res.update(G_P_pavg_matches_independent_max_dev=dev, G_P_ok=bool(dev < 1e-12 and ranges), G_I_budget_6040_all_arms=bool(budgets), G_I_no_oracle_leak=bool(leak), G_I_E_reproduces_P8_D=bool(eo["F_search"] == ref["F_search"] and eo["hv_oracle"] == ref["hv_oracle"]), n_instances=n)
res["all_ok"] = bool(res["G_P_ok"] and res["G_I_budget_6040_all_arms"] and res["G_I_no_oracle_leak"] and res["G_I_E_reproduces_P8_D"]); json.dump(res, open(sys.argv[1], "w"), indent=1, default=bool); print(json.dumps(res, default=bool))
