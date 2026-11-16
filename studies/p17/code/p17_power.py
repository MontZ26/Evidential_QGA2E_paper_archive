"""P17 power simulation (before freeze): seed-level paired contrast, sd from P14, n = 100, percentile bootstrap at the Bonferroni level 99% (5 primaries). No P17 data."""
import numpy as np, json
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p17"
rng = np.random.RandomState(17001); n = 100; nrep = 400; nb = 1000; delta = 0.005; out = {}
for sd in (0.0109, 0.0154):
    for eff in (0.0, 0.002, 0.005, 0.01):
        sup = eq = inf = 0
        for _ in range(nrep):
            d = rng.normal(eff, sd, n); idx = rng.randint(0, n, (nb, n)); bm = d[idx].mean(1); lo, hi = np.percentile(bm, [0.5, 99.5])
            sup += lo > 0; inf += hi < 0; eq += (lo > -delta) and (hi < delta)
        out[f"sd={sd},effect={eff}"] = dict(P_superiority=sup / nrep, P_inferiority=inf / nrep, P_equivalence=eq / nrep)
json.dump(dict(n=n, level="99%", margin=delta, reps=nrep, boot=nb, results=out), open(B + "/p17_power.json", "w"), indent=1); print(json.dumps(out, indent=1))
