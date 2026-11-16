"""P9 engine: reuses frozen P5/P7 and the P8 engine (unmodified). Arms: E (evidential data + V1), P (probabilistic-average data + V0c), X (prob data + V1), Dp (evidential data + V0c), B (evidential data, classical GA), Bp (prob data, classical GA)."""
import sys, os
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p8/code")
import numpy as np, p8, p8_ctrl as C
P = p8.P; A_, T_ = 1, 3
class _Seeds9:
    def __contains__(self, s): return (8000 <= s <= 8399 or 8900 <= s <= 8909 or 9000 <= s <= 9199 or s == 9802)
P.ALLOWED_SEEDS = _Seeds9()
ARMS = {"E": ("nom", "V1"), "P": ("pavg", "V0c"), "X": ("pavg", "V1"), "Dp": ("nom", "V0c"), "B": ("nom", None), "Bp": ("pavg", None)}
def pavg_A(I):
    ev = I["ev"]; A = np.zeros((I["n_t"], P.NK))
    for t in range(I["n_t"]):
        for k in range(P.NK):
            if I["CT"][t, k] != 1: continue
            s = C.srcs(I, t, k, ev["h_x"][t, k], ev["h_n"][t, k]); b = [m.get(A_, 0.0) + m.get(T_, 0.0) / 2 for m in (s["doc"], s["sup"], s["his"])]; A[t, k] = 0.25 + 0.60 * float(np.mean(b))
    return A
def worlds9(I):
    W = p8.worlds_for(I); W["pavg"] = (pavg_A(I), W["nom"][1]); return W
def task9(sc, seed, arms=tuple(ARMS)):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = worlds9(I); out["conds"] = {a: p8.run_one(I, ARMS[a][0], ARMS[a][1], None, None, W) for a in arms}; return out
