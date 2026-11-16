"""M2 technical tests: engine combination vs G0 general implementations; budget; vacuous populations. Output p7_tests_m2.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p7, p7m2, p7_g0 as G
OUT = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7/p7_tests_m2.json"; res = {}; ok_all = True
def rec(n, ok, **kw):
    global ok_all; ok_all &= bool(ok); res[n] = dict(ok=bool(ok), **kw); print(n, "OK" if ok else "FAIL", kw, flush=True)
I = p7.P.build("S4-RC101", 7900); M = I["M"]; n_p, n_t = I["n_p"], I["n_t"]; rng = np.random.RandomState(11); mx = 0.0
for rule in ("V1", "V2", "V0c"):
    for t in range(5):
        N = int(rng.randint(4, 12)); decs = np.zeros((N, n_p), int); Lm = np.zeros((N, n_p), np.int64)
        for p in range(n_p):
            al = np.flatnonzero(M[p]); decs[:, p] = rng.choice(al, N)
            for j in range(N):
                for a in al:
                    if a != decs[j, p] and rng.rand() < 0.25: Lm[j, p] |= 1 << int(a)
        has = rng.rand(N) < 0.7; w = float(rng.uniform(0.1, 0.9)); Pn, _ = p7m2.model_m2(decs, Lm, has, M, w, rule)
        for p in range(0, n_p, 7):
            al = list(np.flatnonzero(M[p])); Kp = len(al); idx = {a: i for i, a in enumerate(al)}; conv = lambda mask: sum(1 << idx[a] for a in al if (mask >> int(a)) & 1)
            srcs = []; qs = []
            for j in range(N):
                if has[j]:
                    A = conv((1 << int(decs[j, p])) | int(Lm[j, p])); srcs.append(G.simple(A, w, Kp))
                    msk = np.array([(A >> i) & 1 for i in range(Kp)], float); qs.append(w * msk / msk.sum() + (1 - w) / Kp)
                else: srcs.append({G.full(Kp): 1.0}); qs.append(np.ones(Kp) / Kp)
            if rule == "V0c": pg = G.V0c(qs, Kp)
            elif rule == "V1": pg, _ = G.V1(srcs, Kp)
            else:
                distinct = []; seen = set()
                for s in srcs:
                    key = tuple(sorted(s.items()))
                    if key not in seen and list(s.keys()) != [G.full(Kp)]: seen.add(key); distinct.append(s)
                pg, _ = G.V2(distinct or [{G.full(Kp): 1.0}], Kp)
            mx = max(mx, float(np.max(np.abs(Pn[p, al] - pg))))
rec("T1_M2_matches_G0_general", mx < 1e-8, max_dev=mx)
base = dict(N=20, pc=0.8, eta_k=2.0, w=0.5, eps=0.005, p_LS=0.25, k_LS=50, rule="pondere"); bad = []
for N in (20, 100):
    for rule in p7.RULES:
        r = p7m2.run7m2(I, rule, dict(base, N=N))
        if r["n_eval"] != 6040: bad.append((N, rule, r["n_eval"]))
rec("T2_M2_budget_exact", not bad, bad=bad)
r = p7m2.run7m2(I, "V2", dict(base, p_LS=0.0)); r2 = p7.run7(I, "V2", dict(base, p_LS=0.0)); rec("T3_no_LS_M2_vacuous_is_uniform_sampling_nonerror", r["n_eval"] == 6040)
res["all_ok"] = ok_all; json.dump(res, open(OUT, "w"), indent=1, default=str); print("ALL_OK", ok_all)
