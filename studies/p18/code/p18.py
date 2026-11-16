"""P18 engine: Part A (P16 regulated DEC arms, via p16.run_arm16) and Part B (new selection arms DIV / SELL / Dp+SELW and Dg(gamma) curve). Frozen modules UNMODIFIED."""
import sys, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p15/code"); sys.path.insert(0, BASE + "/p16/code"); sys.path.insert(0, BASE + "/p17/code")
import numpy as np, p15, p16, p17
P, X = p17.P, p17.X
class _Seeds18:
    def __contains__(self, s): return (11400 <= s <= 11459 or 11200 <= s <= 11259 or 11000 <= s <= 11029 or 11600 <= s <= 11609 or s in (10400, 10401, 9290, 7000, 5200))
P.ALLOWED_SEEDS = _Seeds18()
TAU = json.load(open(BASE + "/p16/p16_thresholds.json"))
ARMS_A = ["E", "DA", "DA+S", "DA+L", "DA+P11", "DA+R1", "DA+R1inv", "DA+SCH"]
ARMS_B = ["DA+DIV", "DA+SELL", "Dp+SELW", "Dg2", "Dg4", "Dg8", "Dg12"]
GAMMA = {"Dg2": 2.0, "Dg4": 4.0, "Dg8": 8.0, "Dg12": 12.0}
BASE_B = {"DA+DIV": "DA", "DA+SELL": "DA", "Dp+SELW": "Dp"}; SELMODE18 = {"DA+DIV": "DIV", "DA+SELL": "SELL", "Dp+SELW": "SELWP"}
def div_U(pop):
    a = (pop[:, None, :] == pop[None, :, :]).mean(2); n = len(pop); return (a.sum(1) - 1.0) / max(n - 1, 1)
def sell_select(fits3, U, size):
    n = len(U); fronts = X.nds(fits3); rF = np.zeros(n); cd = np.zeros(n); pos = np.zeros(n)
    for k, f in enumerate(fronts):
        d = X.G["crowding_dist"](fits3, f)
        for j, i in enumerate(f): rF[i] = k + 1; cd[i] = d[i]; pos[i] = j
    order = np.lexsort((pos, U, -np.round(cd, 12), rF)); return list(order[:size])      # residual ties: position in the front list, as in the original selection
def make_select18(I, prm, mode, orig, log):
    M = I["M"]; w = prm["w"]
    def sel(pop, fits, size):
        if len(pop) == size: return orig(pop, fits, size)
        POP = size; S_idx = p17.sources_index(fits[:POP]); src = pop[S_idx]; mp = -np.ones(len(pop), int)
        for k, i in enumerate(S_idx): mp[i] = k
        if mode == "DIV": Uo = div_U(pop); s = orig(pop, np.column_stack([fits, Uo]), size)
        elif mode == "SELL": Uo = -p17.gain_E(src, M, w, prm["sigma"], prm["lam"], pop, mp); s = sell_select(fits, Uo, size)
        elif mode == "SELWP": Uo = -p17.gain_P(src, M, w, pop, mp); s = p17.selw_select(fits, Uo, size)
        else: raise ValueError(mode)
        s3 = orig(pop, fits, size); f4 = X.nds(np.column_stack([fits, Uo]))
        log.append(dict(front4_share=len(f4[0]) / len(pop), divergence=1.0 - len(set(s) & set(s3)) / size, finite=bool(np.isfinite(Uo).all()), U_mean_sel=float(np.mean(Uo[list(s)])), U_mean_all=float(np.mean(Uo))))
        return s
    return sel
def run_arm18(I, arm, prm, wd=None):
    W = p17.p9.worlds9(I) if wd is None else wd
    if arm in ARMS_A:
        if arm == "E": r = p15.run_arm15(I, "E", prm, W)
        else: r = p16.run_arm16(I, arm, prm, TAU, W)
        r["sel_log"] = []; return r
    if arm in GAMMA: r = p15.run_arm15(I, "Dg", dict(prm, gamma=GAMMA[arm]), W); r["sel_log"] = []; return r
    log = []; orig = X.select_next; X.select_next = make_select18(I, prm, SELMODE18[arm], orig, log)
    try: r = p15.run_arm15(I, BASE_B[arm], prm, W)
    finally: X.select_next = orig
    r["sel_log"] = log; return r
def task18(sc, seed, arms, prm):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p17.p9.worlds9(I); out["conds"] = {a: run_arm18(I, a, prm, W) for a in arms}; return out
