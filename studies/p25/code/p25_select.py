"""P25 selection of gamma_cal(w), w in {0.3,0.7}, from HV-blind calibration. Rule = P24. Builds arm list. Run once."""
import json, os, math, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p25, p24
B = p24.BASE; OUT = B + "/p25/p25_params.json"; assert not os.path.exists(OUT)
c = json.load(open(B + "/p25/p25_calib.json")); H, Q = c["entropy"], c["qmax"]; assert all(math.isfinite(v) for v in list(H.values()) + list(Q.values()))
def pick(ref, w):
    tab = {}; cands = [p24.aid("Dg", w, gamma=g) for g in p24.GAMMA_GRID]
    for k in cands:
        gap = abs(H[k] - H[ref]) / H[ref]; qg = abs(Q[k] - Q[ref]); tab[k] = dict(entropy=H[k], qmax=Q[k], rel_entropy_gap=gap, abs_qmax_gap=qg, gate=bool(gap <= 0.10 and qg <= 0.05), J=gap ** 2 + (qg / 0.05) ** 2)
    ok = [k for k in cands if tab[k]["gate"]]
    best = min(ok, key=lambda k: (round(tab[k]["rel_entropy_gap"], 12), round(tab[k]["abs_qmax_gap"], 12))) if ok else min(cands, key=lambda k: round(tab[k]["J"], 12))
    g = p24.spec(best)[3]; return g, bool(ok), dict(ref=ref, ref_entropy=H[ref], ref_qmax=Q[ref], table=tab, edge=bool(g in (p24.GAMMA_GRID[0], p24.GAMMA_GRID[-1])))
gam = {}; gate = {}; det = {}
for w in (0.3, 0.7): g, ok, d = pick(p24.aid("DA", w, 0.7), w); gam[w] = g; gate["w%g" % w] = ok; det["w%g" % w] = d
arms = []; roles = {}
def add(a):
    if a not in arms: arms.append(a)
    return a
for w in (0.3, 0.7): roles["E_w%g" % w] = add(p24.aid("E", w)); roles["Dp_w%g" % w] = add(p24.aid("Dp", w)); roles["DA_w%g" % w] = add(p24.aid("DA", w, 0.7)); roles["Dg_w%g" % w] = add(p24.aid("Dg", w, gamma=gam[w]))
roles["Dg6_w0.3"] = add(p24.aid("Dg", 0.3, gamma=6.0))
prm = dict(gamma_cal={str(k): v for k, v in gam.items()}, gate_satisfied=gate, roles=roles, arms=arms, detail=det)
json.dump(prm, open(OUT, "w"), indent=1); print(json.dumps(dict(gamma=gam, gate=gate, arms=arms, edge={k: v["edge"] for k, v in det.items()}), indent=1))
