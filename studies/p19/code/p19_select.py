"""P19 gamma_m selection from the stored HV-blind calibration table (amended rule, fixed BEFORE the table was read). Run once."""
import json, os
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p19"; OUT = B + "/p19_gamma.json"; assert not os.path.exists(OUT)
c = json.load(open(B + "/p19_calib.json")); tab = c["table"]; HD, QD = c["Dg_target"]["entropy"], c["Dg_target"]["qmax"]
import math; assert all(math.isfinite(v[k]) for v in tab.values() for k in ("entropy", "qmax")) and math.isfinite(HD) and math.isfinite(QD), "non-finite calibration value: stop"
J = {g: ((v["entropy"] - HD) / HD) ** 2 + ((v["qmax"] - QD) / 0.05) ** 2 for g, v in tab.items()}; gate = [g for g, v in tab.items() if v["gate"]]; pool = gate if gate else list(tab)
gm = min(pool, key=lambda g: (round(J[g], 12), float(g))); json.dump(dict(gamma_m=float(gm), J=J, gate_passing=gate, gate_satisfied=bool(gate), rule="J(g)=((H-Hcible)/Hcible)^2+((qmax-qmax_cible)/0.05)^2 ; argmin J among gate-passing grid values, else over the whole grid; ties -> smaller gamma; table from p19_calib.json (HV not read)", note="the field gamma_m of p19_calib.json (relative-entropy-only rule) is superseded by this amendment"), open(OUT, "w"), indent=1); print(open(OUT).read())
