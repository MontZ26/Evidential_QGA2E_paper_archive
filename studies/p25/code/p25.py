"""P25 engine (new file; frozen P3..P24 code used UNMODIFIED). Independent instance family: NEW synthetic Solomon-like geographies (uniform U, clustered K, mixed M; generated per seed) and NEW sizes (V6: 40 patients / 9 teams; V7: 70 / 12).
The scenarios are registered in the in-memory dictionaries of the shared generator library (no file is modified); instance data other than the geography come from the unchanged generator. Search engine and arms = P24 (p24.run_arm24)."""
import sys, os, json, zlib
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p24/code")
import numpy as np, p24
from p24 import P, p23
G = P.G
class _Seeds25:
    def __contains__(self, s): return (14000 <= s <= 14099 or 14700 <= s <= 14714 or 14900 <= s <= 14909 or s in p24._Seeds24())
P.ALLOWED_SEEDS = _Seeds25()
SC_V6 = ["V6-U", "V7-U", "V6-K", "V7-K", "V6-M", "V7-M"]; SC_V3 = ["V6-U", "V6-K", "V6-M"]
NEW_SC = {"V6-U": ("V6-U", "UNI", 40, 9, 20), "V7-U": ("V7-U", "UNI", 70, 12, 20), "V6-K": ("V6-K", "CLU", 40, 9, 20), "V7-K": ("V7-K", "CLU", 70, 12, 20), "V6-M": ("V6-M", "MIX", 40, 9, 20), "V7-M": ("V7-M", "MIX", 70, 12, 20)}
DAY = {"UNI": dict(day_end=230, visit=10), "CLU": dict(day_end=1236, visit=90), "MIX": dict(day_end=240, visit=10)}
DEPOT = {"UNI": (35, 35), "CLU": (40, 50), "MIX": (40, 50)}
NPTS = 101
def _rs(*a): return np.random.RandomState(zlib.crc32("|".join(map(str, a)).encode()) % (2 ** 31))
def gen_points(topo, seed):
    """Solomon-like integer coordinates in [0,100]^2; depot first. UNI: uniform. CLU: 8 Gaussian clusters (sd 5). MIX: half clustered, half uniform, shuffled."""
    r = _rs("p25geo", topo, seed); dep = DEPOT[topo]
    def uni(n): return r.randint(0, 101, size=(n, 2))
    def clu(n):
        c = r.randint(10, 91, size=(8, 2)); a = r.randint(0, 8, size=n); return np.clip(np.rint(c[a] + r.normal(0, 5, size=(n, 2))), 0, 100).astype(int)
    if topo == "UNI": pts = uni(NPTS - 1)
    elif topo == "CLU": pts = clu(NPTS - 1)
    else:
        pts = np.vstack([clu((NPTS - 1) // 2), uni(NPTS - 1 - (NPTS - 1) // 2)]); pts = pts[r.permutation(len(pts))]
    return [(float(dep[0]), float(dep[1]))] + [(float(x), float(y)) for x, y in pts]
def register():
    for k, v in NEW_SC.items(): p24.P.SC[k] = v
    for t, d in DAY.items(): G["DAY_PARAMS"][t] = dict(d)
register()
def build25(sc, seed):
    topo = NEW_SC[sc][1]; G["PTS_MAP"][topo] = gen_points(topo, seed); return P.build(sc, seed)
def task25(sc, seed, arms, oracle=True, logging=True):
    I = build25(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"]); npz = {}
    if not I["feasible"]: return out, npz
    W = p24.p9.worlds9(I); out["conds"] = {}
    for a in arms:
        o, fql = p24.run_arm24(I, a, W, oracle, logging); out["conds"][a] = o
        if logging:
            for g, c in fql.items(): npz["%s|%d" % (a, g)] = c
    if logging: npz["M"] = np.asarray(I["M"]).astype(np.uint8)
    return out, npz
