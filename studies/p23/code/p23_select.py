"""P23 selection of gamma (per lambda), rho0, gmix from the stored HV-blind calibration table. Rule fixed in the protocol (section 5) BEFORE the table was read: conforming = rel. entropy gap <= 0.10 and |qmax gap| <= 0.05 (reference: DA(lambda) for Dg; DA(1) for R_rho and R_mix); among conforming: smallest rel. entropy gap, then smallest |qmax gap|; if none conforms: argmin J = gap^2 + (qgap/0.05)^2 over the whole grid (best attempt, declared). Run once."""
import json, os, math
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; OUT = B + "/p23/p23_params.json"; assert not os.path.exists(OUT)
c = json.load(open(B + "/p23/p23_calib.json")); H, Q = c["entropy"], c["qmax"]; assert all(math.isfinite(v) for v in list(H.values()) + list(Q.values())), "non-finite calibration value: stop"
def pick(ref, cands):
    tab = {}
    for k in cands:
        gap = abs(H[k] - H[ref]) / H[ref]; qg = abs(Q[k] - Q[ref]); tab[k] = dict(entropy=H[k], qmax=Q[k], rel_entropy_gap=gap, abs_qmax_gap=qg, gate=bool(gap <= 0.10 and qg <= 0.05), J=gap ** 2 + (qg / 0.05) ** 2)
    ok = [k for k in cands if tab[k]["gate"]]
    best = min(ok, key=lambda k: (round(tab[k]["rel_entropy_gap"], 12), round(tab[k]["abs_qmax_gap"], 12))) if ok else min(cands, key=lambda k: (round(tab[k]["J"], 12)))
    return best, bool(ok), dict(ref=ref, table=tab, ref_entropy=H[ref], ref_qmax=Q[ref])
GG = [1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0]; sel = {"gamma": {}}; detail = {}; gate = {}
for lam in ("DA25", "DA50", "DA100"):
    b, ok, d = pick(lam, ["Dg_%s" % g for g in GG]); sel["gamma"][lam] = float(b.split("_")[1]); gate["Dg_" + lam] = ok; detail["Dg_" + lam] = d
b, ok, d = pick("DA100", ["RHO_%s" % r for r in (0.02, 0.05, 0.1, 0.2)]); sel["rho0"] = float(b.split("_")[1]); gate["RHO"] = ok; detail["RHO"] = d
b, ok, d = pick("DA100", ["MIX_%s" % m for m in (0.25, 0.5, 0.75)]); sel["gmix"] = float(b.split("_")[1]); gate["MIX"] = ok; detail["MIX"] = d
base = json.load(open(B + "/p15/p15_params.json"))["chosen"]; prm = dict(w=base["w"], eps=base["eps"], sigma=base["sigma"], gamma=sel["gamma"], rho0=sel["rho0"], gmix=sel["gmix"], gate_satisfied=gate, detail=detail, rule="see docstring of p23_select.py; table from p23_calib.json; HV not read")
json.dump(prm, open(OUT, "w"), indent=1); print(json.dumps(dict(gamma=sel["gamma"], rho0=sel["rho0"], gmix=sel["gmix"], gate=gate), indent=1))
