"""P25b engine (new file). Geographies from PUBLIC BENCHMARK FILES never used before (distributed copy: github.com/PyVRP/VRPLIB tests/data, commit 309f1890; instances: Uchoa X-n101-k25, Christofides M-n101-k10, Golden_1, Li_21, ORTEC-n242-k12 (described as derived from a real grocery delivery service), Homberger C1_2_1). Per seed: customers drawn WITHOUT replacement from the file (seeded); coordinates rescaled uniformly so that the bounding box max side = 100 (depot = file depot). All other generator parts (hidden truth, evidence sources) unchanged. Engine/arms = P24."""
import sys, os, json, zlib, re
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p24/code")
import numpy as np, p24
from p24 import P
G = P.G; FD = BASE + "/p25b/files/"
class _Seeds25b:
    def __contains__(self, s): return (15000 <= s <= 15099 or 15700 <= s <= 15714 or 15900 <= s <= 15909 or s in p24._Seeds24())
P.ALLOWED_SEEDS = _Seeds25b()
FILES = {"B-X": "X-n101-k25.vrp", "B-M": "M-n101-k10.vrp", "B-G": "Golden_1.vrp", "B-L": "Li_21.vrp", "B-O": "ORTEC-n242-k12.vrp", "B-H": "C1_2_1.txt"}
SC_B6 = list(FILES); SC_B3 = ["B-X", "B-G", "B-O"]
NP, NT, DAY_END, VISIT = 50, 10, 240, 10
def read_coords(fn):
    L = open(FD + fn).read().split("\n"); out = []
    if fn.endswith(".txt"):
        i = next(k for k, l in enumerate(L) if l.strip().startswith("CUST NO"))
        for l in L[i + 1:]:
            t = l.split()
            if len(t) >= 7: out.append((float(t[1]), float(t[2])))
        return out
    i = next(k for k, l in enumerate(L) if "NODE_COORD_SECTION" in l)
    for l in L[i + 1:]:
        t = l.split()
        if len(t) < 3 or not t[0].lstrip("-").isdigit(): break
        out.append((float(t[1]), float(t[2])))
    return out
_CACHE = {}
def coords(sc):
    if sc not in _CACHE: _CACHE[sc] = read_coords(FILES[sc])
    return _CACHE[sc]
def _rs(*a): return np.random.RandomState(zlib.crc32("|".join(map(str, a)).encode()) % (2 ** 31))
def gen_points(sc, seed):
    c = np.array(coords(sc), float); dep = c[0]; cust = c[1:]
    mn = c.min(0); span = max((c.max(0) - mn).max(), 1e-9); f = 100.0 / span
    r = _rs("p25bgeo", sc, seed); idx = r.choice(len(cust), size=100, replace=len(cust) < 100)
    pts = [tuple(((dep - mn) * f).round(3))] + [tuple(((cust[i] - mn) * f).round(3)) for i in idx]
    return [(float(x), float(y)) for x, y in pts]
def register():
    for k in SC_B6:
        P.SC[k] = (k, "T" + k, NP, NT, 20); G["DAY_PARAMS"]["T" + k] = dict(day_end=DAY_END, visit=VISIT)
register()
def build25b(sc, seed):
    G["PTS_MAP"]["T" + sc] = gen_points(sc, seed); return P.build(sc, seed)
def task25b(sc, seed, arms, oracle=True, logging=True):
    I = build25b(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"]); npz = {}
    if not I["feasible"]: return out, npz
    W = p24.p9.worlds9(I); out["conds"] = {}
    for a in arms:
        o, fql = p24.run_arm24(I, a, W, oracle, logging); out["conds"][a] = o
        if logging:
            for g, c in fql.items(): npz["%s|%d" % (a, g)] = c
    if logging: npz["M"] = np.asarray(I["M"]).astype(np.uint8)
    return out, npz
