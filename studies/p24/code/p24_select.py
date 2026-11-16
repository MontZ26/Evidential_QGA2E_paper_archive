"""P24 selection of gamma per (w) and per (sigma at w=0.3) from the stored HV-blind calibration table. Rule identical to P23 (fixed before reading): conforming = rel. entropy gap <= 0.10 and |qmax gap| <= 0.05 (reference DA(1;w,sigma)); among conforming: smallest rel. entropy gap, then smallest |qmax gap|; if none: argmin J = gap^2 + (qgap/0.05)^2 over the grid (best attempt, declared). Edge-of-grid selections are flagged. Builds arm list. Run once."""
import json, os, math, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p24
B = p24.BASE; OUT = B + "/p24/p24_params.json"; assert not os.path.exists(OUT)
c = json.load(open(B + "/p24/p24_calib.json")); H, Q = c["entropy"], c["qmax"]; assert all(math.isfinite(v) for v in list(H.values()) + list(Q.values())), "non-finite calibration value: stop"
def pick(ref, w):
    tab = {}; cands = [p24.aid("Dg", w, gamma=g) for g in p24.GAMMA_GRID]
    for k in cands:
        gap = abs(H[k] - H[ref]) / H[ref]; qg = abs(Q[k] - Q[ref]); tab[k] = dict(entropy=H[k], qmax=Q[k], rel_entropy_gap=gap, abs_qmax_gap=qg, gate=bool(gap <= 0.10 and qg <= 0.05), J=gap ** 2 + (qg / 0.05) ** 2)
    ok = [k for k in cands if tab[k]["gate"]]
    best = min(ok, key=lambda k: (round(tab[k]["rel_entropy_gap"], 12), round(tab[k]["abs_qmax_gap"], 12))) if ok else min(cands, key=lambda k: round(tab[k]["J"], 12))
    g = p24.spec(best)[3]; return g, bool(ok), dict(ref=ref, ref_entropy=H[ref], ref_qmax=Q[ref], table=tab, edge=bool(g in (p24.GAMMA_GRID[0], p24.GAMMA_GRID[-1])))
gam_w = {}; gam_s = {}; gate = {}; det = {}
for w in p24.W_LIST:
    g, ok, d = pick(p24.aid("DA", w, 0.7), w); gam_w[w] = g; gate["w%g" % w] = ok; det["w%g" % w] = d
for s in p24.SIGMAS:
    g, ok, d = pick(p24.aid("DA", 0.3, s), 0.3); gam_s[s] = g; gate["s%g" % s] = ok; det["s%g" % s] = d
gcal = gam_w[0.3]
# arm list (unique ids). Roles map contrasts to ids.
arms = []
def add(a):
    if a not in arms: arms.append(a)
    return a
roles = {}
for w in (0.15, 0.5, 0.7):
    roles["E_w%g" % w] = add(p24.aid("E", w)); roles["Dp_w%g" % w] = add(p24.aid("Dp", w)); roles["DA_w%g" % w] = add(p24.aid("DA", w, 0.7)); roles["Dg_w%g" % w] = add(p24.aid("Dg", w, gamma=gam_w[w]))
roles["Dp_w0.3"] = add(p24.aid("Dp", 0.3)); roles["DA_w0.3"] = add(p24.aid("DA", 0.3, 0.7)); roles["Dg6_w0.3"] = add(p24.aid("Dg", 0.3, gamma=6.0))
roles["Dg8"] = add(p24.aid("Dg", 0.3, gamma=8.0)); roles["Dg12"] = add(p24.aid("Dg", 0.3, gamma=12.0)); roles["Dgcal"] = add(p24.aid("Dg", 0.3, gamma=gcal))
for s in p24.SIGMAS: roles["DA_s%g" % s] = add(p24.aid("DA", 0.3, s)); roles["Dg_s%g" % s] = add(p24.aid("Dg", 0.3, gamma=gam_s[s]))
prm = dict(gamma_w={str(k): v for k, v in gam_w.items()}, gamma_sigma={str(k): v for k, v in gam_s.items()}, gamma_cal_baseline=gcal, gate_satisfied=gate, roles=roles, arms=arms, n_families=len(arms), detail=det, rule="see docstring; table from p24_calib.json; HV not read")
assert len(arms) <= 22, len(arms)
json.dump(prm, open(OUT, "w"), indent=1); print(json.dumps(dict(gamma_w=gam_w, gamma_s=gam_s, gate=gate, n_arms=len(arms), arms=arms, edge={k: v["edge"] for k, v in det.items()}), indent=1))
