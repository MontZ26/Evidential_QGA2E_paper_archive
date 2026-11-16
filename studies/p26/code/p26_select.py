"""P26 selection of schedules per (w, ref in {E, DA}); trajectory gate; builds arm list. Run once."""
import sys, os, json, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p26, p24
B = p26.BASE; OUT = B + "/p26/p26_params.json"; assert not os.path.exists(OUT)
c = json.load(open(B + "/p26/p26_calib.json")); H, Q, CAND = c["entropy_traj"], c["qmax_traj"], c["cand"]
assert all(np.all(np.isfinite(v)) for v in list(H.values()) + list(Q.values()))
sel = {}; gate = {}; detail = {}
for w in (0.3, 0.7):
    for ref in ("E", "DA"):
        ra = p24.aid("E", w) if ref == "E" else p24.aid("DA", w, 0.7); Hr, Qr = np.array(H[ra]), np.array(Q[ra]); tab = {}
        for (g0, g1, Gs) in CAND:
            k = p26.gid(w, "X", g0, g1, Gs); h, q = np.array(H[k]), np.array(Q[k])
            eg = np.abs(h - Hr) / Hr; qg = np.abs(q - Qr); ebar, qbar = float(eg.mean()), float(qg.mean())
            tab[k] = dict(g0=g0, g1=g1, Gs=Gs, rel_entropy_gap_mean=ebar, abs_qmax_gap_mean=qbar, gate=bool(ebar <= 0.10 and qbar <= 0.05), J=float(np.mean(eg ** 2) + np.mean((qg / 0.05) ** 2)))
        ok = [k for k in tab if tab[k]["gate"]]; best = min(ok if ok else tab, key=lambda k: round(tab[k]["J"], 12))
        t = tab[best]; sel["w%g_%s" % (w, ref)] = p26.gid(w, ref, t["g0"], t["g1"], t["Gs"]); gate["w%g_%s" % (w, ref)] = bool(ok); detail["w%g_%s" % (w, ref)] = dict(chosen=best, table=tab)
arms = []; roles = {}
def add(a):
    if a not in arms: arms.append(a)
    return a
for w in (0.3, 0.7):
    roles["E_w%g" % w] = add(p24.aid("E", w)); roles["DA_w%g" % w] = add(p24.aid("DA", w, 0.7)); roles["Dp_w%g" % w] = add(p24.aid("Dp", w))
    roles["Dgt_E_w%g" % w] = add(sel["w%g_E" % w]); roles["Dgt_DA_w%g" % w] = add(sel["w%g_DA" % w]); roles["Dg6_w%g" % w] = add(p24.aid("Dg", w, gamma=6.0))
prm = dict(schedules=sel, gate_satisfied=gate, roles=roles, arms=arms, detail=detail)
json.dump(prm, open(OUT, "w"), indent=1); print(json.dumps(dict(schedules=sel, gate=gate, arms=arms, n_arms=len(arms)), indent=1))
