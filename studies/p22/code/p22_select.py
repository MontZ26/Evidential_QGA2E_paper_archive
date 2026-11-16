"""P22 gamma_m selection from the stored HV-blind calibration table (rule J as in P19, fixed in the protocol before the table was read). Run once."""
import json, os, math
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p22"; OUT = B + "/p22_gamma.json"; assert not os.path.exists(OUT)
c = json.load(open(B + "/p22_calib.json")); tab = c["table"]; HD, QD = c["GDg6_target"]["entropy"], c["GDg6_target"]["qmax"]
assert all(math.isfinite(v[k]) for v in tab.values() for k in ("entropy", "qmax")) and math.isfinite(HD) and math.isfinite(QD), "non-finite calibration value: stop"
J = {g: ((v["entropy"] - HD) / HD) ** 2 + ((v["qmax"] - QD) / 0.05) ** 2 for g, v in tab.items()}; gate = [g for g, v in tab.items() if v["gate"]]; pool = gate if gate else list(tab)
gm = min(pool, key=lambda g: (round(J[g], 12), float(g))); json.dump(dict(gamma_m=float(gm), J=J, gate_passing=gate, gate_satisfied=bool(gate), rule="J(g)=((H-Hcible)/Hcible)^2+((qmax-qmax_cible)/0.05)^2 ; argmin J among gate-passing grid values, else whole grid; ties -> smaller gamma; HV not used"), open(OUT, "w"), indent=1); print("gamma_m", gm, "gate", bool(gate))
