"""G-D0: DEC off is bit-for-bit identical to P9/E, P9/Dp (=D'), P9/B (=C0b) fronts, decisions, oracle objective vectors, HV."""
import sys, json, hashlib; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/code")
import p11, p9
MAP = {"E0": "E", "P0": "Dp", "C0": "B"}; res = []; ok = True
for sc in p11.p8.SC6:
    for seed in (9910, 9911, 9912):
        a = p11.task11(sc, seed, list(MAP)); b = p9.task9(sc, seed, arms=tuple(MAP.values()))
        for k, v in MAP.items():
            x, y = a["conds"][k], b["conds"][v]
            same = all(x[f] == y[f] for f in ("D", "F_search", "F_oracle", "hv_oracle", "hv_search", "n_eval", "gens"))
            res.append(dict(sc=sc, seed=seed, arm=k, ref=v, identical=bool(same), hv=x["hv_oracle"])); ok &= bool(same)
print("G-D0", "PASS" if ok else "FAIL", len(res), "comparisons"); json.dump(dict(pass_=ok, n=len(res), details=res), open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/p11_gd0_results.json", "w"), indent=1)
