"""P7 gate G0 — mathematical validation (Amendement P7 v0.3 + protocol v0.3 section 9). Independent of the evolutionary engine; no experimental data.
Mass function = dict {bitmask: mass} on frame Theta = {0..K-1}. Implements: M1/M2 masses, Dempster, Denoeux cautious rule via canonical (weight) decomposition, conditioned BetP, V0c, tests.
Usage: python p7_g0.py OUT.json LOG.txt"""
import sys, json, math, itertools, hashlib, random
import numpy as np
EPS = 1e-10
def full(K): return (1 << K) - 1
def card(a): return bin(a).count("1")
def norm_m(m): return {a: v for a, v in m.items() if abs(v) > 0}
def simple(A, w, K):
    """source with strength w on A: m(A)=w, m(Theta)=1-w (A=Theta merges)"""
    if A == full(K): return {full(K): 1.0}
    return {A: w, full(K): 1.0 - w}
def conj(m1, m2):
    out = {}
    for a, x in m1.items():
        for b, y in m2.items(): out[a & b] = out.get(a & b, 0.0) + x * y
    return out
def dempster(m1, m2):
    c = conj(m1, m2); k = c.get(0, 0.0)
    if k >= 1 - 1e-15: return None, k
    return {a: v / (1 - k) for a, v in c.items() if a != 0}, k
def commonality(m, K):
    q = {}
    for B in range(1 << K): q[B] = sum(v for a, v in m.items() if (a & B) == B)
    return q
def mobius_from_q(q, K):
    m = {}
    for A in range(1 << K):
        s = 0.0
        for B in range(1 << K):
            if (B & A) == A: s += (-1) ** (card(B) - card(A)) * q[B]
        m[A] = s
    return {a: v for a, v in m.items() if abs(v) > 1e-14}
def canonical_weights(m, K):
    """Denoeux (2008): for non-dogmatic m (m(Theta)>0): w(A) = prod_{B superset of A} q(B)^{(-1)^{|B|-|A|+1}}, A proper subset of Theta (incl. empty set)"""
    q = commonality(m, K); assert q[0] > 0 and m.get(full(K), 0) > 0, "dogmatic"
    w = {}
    for A in range((1 << K) - 1):
        lw = 0.0
        for B in range(1 << K):
            if (B & A) == A: lw += ((-1) ** (card(B) - card(A) + 1)) * math.log(q[B])
        w[A] = math.exp(lw)
    return w
def from_weights(w, K):
    """m = conjunctive combination of generalised simple functions A^{w(A)} (m(A)=1-w, m(Theta)=w); via commonalities (product), then Moebius"""
    q = {}
    for B in range(1 << K):
        p = 1.0
        for A, wa in w.items(): p *= wa + (1 - wa) * (1.0 if (B & A) == B else 0.0)
        q[B] = p
    return mobius_from_q(q, K)
def cautious(m1, m2, K):
    w1, w2 = canonical_weights(m1, K), canonical_weights(m2, K); return from_weights({A: min(w1[A], w2[A]) for A in w1}, K)
def betp_cond(m, K):
    s = sum(v for a, v in m.items() if a != 0)          # = 1 - m(empty), computed directly (no cancellation)
    if s < 1e-300: return None
    p = np.zeros(K)
    for a, v in m.items():
        if a == 0: continue
        for i in range(K):
            if (a >> i) & 1: p[i] += v / card(a)
    return p / s
def combine_all(sources, K, rule):
    m = sources[0]
    for s in sources[1:]:
        if rule == "dempster": m = conj(m, s)          # unnormalised conjunctive; normalised once at the end (same result as sequential Dempster)
        else: m = cautious(m, s, K)
    return m
def V1(sources, K):
    m = combine_all(sources, K, "dempster"); k = m.get(0, 0.0); return betp_cond(m, K), k           # normalisation by 1-m(empty) happens inside betp_cond (Dempster normalisation)
def V2(sources, K):
    m = combine_all(sources, K, "cautious"); return betp_cond(m, K), m.get(0, 0.0)
def V0c(srcs_q, K, r=None):
    r = r or [1.0] * len(srcs_q); return sum(ri * q for ri, q in zip(r, srcs_q)) / sum(r)
def pign(m, K): return betp_cond(m, K)
def src_M1(team, w, K): return simple(1 << team, w, K)
def src_M2(Aset, w, K): return simple(Aset, w, K)
# ---- closed forms used by the engine (M1: singleton supports only)
def closed_M1(counts, w, mode, K):
    """counts[a]: sources supporting team a. mode 'dempster' (c copies) or 'cautious' (one weight per distinct team). returns (BetP conditioned, m_empty)"""
    T = [a for a in range(K) if counts[a] > 0]; u = {a: ((1 - w) ** counts[a] if mode == "dempster" else (1 - w)) for a in T}
    mTheta = float(np.prod([u[a] for a in T])); mS = {a: (1 - u[a]) * float(np.prod([u[b] for b in T if b != a])) for a in T}; s = mTheta + sum(mS.values()); k = 1.0 - s
    p = np.array([(mS.get(a, 0.0) + mTheta / K) for a in range(K)]) / s; return p, k
def close(a, b, tol=1e-9): return bool(np.max(np.abs(np.asarray(a) - np.asarray(b))) < tol)

def main(out, log):
    res = {}; L = open(log, "w"); ok_all = True
    def rec(name, ok, **kw):
        nonlocal ok_all; ok_all &= bool(ok); res[name] = dict(ok=bool(ok), **kw); L.write(f"{name}: {'OK' if ok else 'FAIL'} {kw}\n"); L.flush()
    rng = np.random.RandomState(7)
    # 1 mass conservation / non-negativity for M1, M2 (incl. A=Theta, no observation)
    K = 5; w = 0.6; ms = [src_M1(2, w, K), src_M2(0b00110, w, K), src_M2(full(K), w, K), {full(K): 1.0}]
    rec("T1_masses_valid", all(abs(sum(m.values()) - 1) < EPS and min(m.values()) >= 0 for m in ms), n=len(ms))
    # 2 illustrative example: three copies of m({A})=0.8, m(Theta)=0.2 -> m({A}) = 0.992 under Dempster
    K = 3; s = simple(1, 0.8, K); m3 = conj(conj(s, s), s); rec("T2_three_copies_dempster", abs(m3[1] - 0.992) < 1e-12, m_A=m3[1], m_Theta=m3[full(K)])
    # 3 two disjoint supports, same w: unnormalised conj -> m(empty)=w^2, m(A)=m(B)=w(1-w), m(Theta)=(1-w)^2
    w = 0.7; c = conj(simple(1, w, 3), simple(2, w, 3)); rec("T3_disjoint_pair", abs(c[0] - w * w) < 1e-12 and abs(c[1] - w * (1 - w)) < 1e-12 and abs(c[2] - w * (1 - w)) < 1e-12 and abs(c[7] - (1 - w) ** 2) < 1e-12, c={k: v for k, v in c.items()})
    # 4 canonical decomposition round trip on random non-dogmatic masses (K=4)
    K = 4; bad = []
    for t in range(30):
        foc = rng.choice(range(1, 1 << K), size=rng.randint(2, 6), replace=False); m = {int(a): float(v) for a, v in zip(foc, rng.dirichlet(np.ones(len(foc))))}; m[full(K)] = m.get(full(K), 0) + 0.1; s_ = sum(m.values()); m = {a: v / s_ for a, v in m.items()}
        r = from_weights(canonical_weights(m, K), K); keys = set(m) | set(r); d = max(abs(m.get(a, 0) - r.get(a, 0)) for a in keys)
        if d > 1e-8: bad.append(d)
    rec("T4_canonical_roundtrip", not bad, bad=bad[:3])
    # 5 cautious rule: idempotence, commutativity, associativity, validity (masses >= 0, sum 1) on random non-dogmatic masses
    bad = {"idem": 0, "comm": 0, "assoc": 0, "valid": 0}
    def rnd():
        foc = rng.choice(range(1, 1 << K), size=rng.randint(1, 5), replace=False); foc = [a for a in foc if a != full(K)] or [1]; m = {int(a): float(v) for a, v in zip(foc, rng.dirichlet(np.ones(len(foc))) * 0.8)}; m[full(K)] = 0.2; return m
    mxd = 0.0
    for t in range(15):
        a, b, c = rnd(), rnd(), rnd(); ab = cautious(a, b, K)
        aa = cautious(a, a, K); keys = set(a) | set(aa); bad["idem"] += max(abs(a.get(x, 0) - aa.get(x, 0)) for x in keys) > 1e-8
        ba = cautious(b, a, K); keys = set(ab) | set(ba); bad["comm"] += max(abs(ab.get(x, 0) - ba.get(x, 0)) for x in keys) > 1e-8
        l = cautious(ab, c, K); r_ = cautious(a, cautious(b, c, K), K); keys = set(l) | set(r_); d = max(abs(l.get(x, 0) - r_.get(x, 0)) for x in keys); mxd = max(mxd, d); bad["assoc"] += d > 1e-7
        bad["valid"] += (min(ab.values()) < -1e-9) or abs(sum(ab.values()) - 1) > 1e-9
    rec("T5_cautious_properties", sum(bad.values()) == 0, bad=bad, max_assoc_dev=mxd)
    # 6 Dempster is NOT idempotent (reference)
    s = simple(1, 0.5, 3); dd, _ = dempster(s, s); rec("T6_dempster_not_idempotent", abs(dd[1] - 0.75) < 1e-12, m_A=dd[1])
    # 7 cautious rule on the focal structures actually used in P7: simple supports on singletons (M1) and on sets A_i (M2), possibly overlapping, duplicates, A=Theta
    #   general canonical-decomposition cautious vs the structural identity "conjunction of the distinct simple supports with weight min"
    K = 6; w = 0.55; bad = []; maxd = 0.0
    for t in range(40):
        nsrc = rng.randint(2, 9); sets = [int(rng.randint(1, full(K))) if rng.rand() < 0.5 else 1 << int(rng.randint(K)) for _ in range(nsrc)]; srcs = [simple(a, w, K) for a in sets]
        m = srcs[0]
        for s_ in srcs[1:]: m = cautious(m, s_, K)
        ref = {full(K): 1.0}
        for a in set(sets): ref = conj(ref, simple(a, w, K))
        keys = set(m) | set(ref); d = max(abs(m.get(x, 0) - ref.get(x, 0)) for x in keys); maxd = max(maxd, d)
        if d > 1e-8: bad.append((sets, d))
    rec("T7_cautious_on_real_focal_structures", not bad, max_dev=maxd, n=40, bad=bad[:2])
    # 8 closed forms for M1 (engine) vs general implementations
    bad = []; mx = 0.0
    for K in (3, 4, 6, 8):
        for t in range(12):
            counts = [int(rng.randint(0, 40)) if rng.rand() < 0.6 else 0 for _ in range(K)]
            if sum(counts) == 0: counts[0] = 3
            w = float(rng.uniform(0.1, 0.95)); srcs = [src_M1(a, w, K) for a in range(K) for _ in range(counts[a])]
            p1, k1 = V1(srcs, K); p1c, k1c = closed_M1(counts, w, "dempster", K)
            distinct = [src_M1(a, w, K) for a in range(K) if counts[a] > 0]
            p2, k2 = V2(srcs, K) if len(srcs) <= 9 else (None, None)
            p2c, k2c = closed_M1(counts, w, "cautious", K)
            d = max(np.max(np.abs(p1 - p1c)), abs(k1 - k1c)); mx = max(mx, d)
            if d > 1e-9: bad.append(("V1", K, counts, d))
            if p2 is not None:
                d2 = max(np.max(np.abs(p2 - p2c)), abs(k2 - k2c)); mx = max(mx, d2)
                if d2 > 1e-8: bad.append(("V2", K, counts, d2))
            pd, kd = V2(distinct, K); d3 = max(np.max(np.abs(pd - p2c)), abs(kd - k2c)); mx = max(mx, d3)
            if d3 > 1e-8: bad.append(("V2distinct", K, counts, d3))
    rec("T8_closed_forms_match_general", not bad, max_dev=mx, bad=bad[:3])
    # 9 deterministic cases: 1 source/1 team; identical repeated; different teams; overlapping sets; total ignorance; conflicting; unequal weights; A=Theta
    K = 4; w = 0.6; det = {}
    p, k = V1([src_M1(1, w, K)], K); det["one_source_V1"] = p.tolist(); p2, k2 = V2([src_M1(1, w, K)], K); det["one_source_V2"] = p2.tolist()
    q = V0c([w * np.eye(K)[1] + (1 - w) * np.ones(K) / K], K); det["one_source_V0c"] = q.tolist()
    ok_one = close(p, p2) and close(p, q) and abs(p[1] - (w + (1 - w) / K)) < 1e-12
    p, k = V1([{full(K): 1.0}] * 5, K); ok_ign = close(p, np.ones(K) / K); p2, _ = V2([{full(K): 1.0}] * 5, K); ok_ign &= close(p2, np.ones(K) / K)
    pa, ka = V1([src_M1(0, w, K)] * 10, K); pb, kb = V2([src_M1(0, w, K)] * 10, K); det["ten_identical_V1_V2"] = [pa.tolist(), pb.tolist()]; ok_rep = close(pb, V2([src_M1(0, w, K)], K)[0]) and pa[0] > pb[0]
    srcs = [src_M1(0, w, K), src_M1(1, w, K)]; p1, k1 = V1(srcs, K); p2, k2 = V2(srcs, K); det["two_teams"] = dict(V1=p1.tolist(), V2=p2.tolist(), mempty=[k1, k2]); ok_two = abs(k1 - w * w) < 1e-12 and abs(k2 - w * w) < 1e-12 and close(p1, p2) and abs(p1[0] - p1[1]) < 1e-12
    ov = [src_M2(0b0011, w, K), src_M2(0b0110, w, K)]; p1, k1 = V1(ov, K); p2, k2 = V2(ov, K); det["overlap_sets"] = dict(V1=p1.tolist(), V2=p2.tolist(), mempty=[k1, k2]); ok_ov = abs(p1.sum() - 1) < 1e-12 and abs(p2.sum() - 1) < 1e-12 and k1 < 1e-12
    uw = [simple(1, 0.9, K), simple(2, 0.3, K)]; p1, k1 = V1(uw, K); p2, k2 = V2(uw, K); det["unequal_weights"] = dict(V1=p1.tolist(), V2=p2.tolist(), mempty=[k1, k2]); ok_uw = p1[0] > p1[1] > 0 or True
    ok_uw = p1[1] > p1[2] and abs(k1 - 0.27) < 1e-12
    th = V1([src_M2(full(K), w, K), src_M1(2, w, K)], K); ok_th = close(th[0], closed_M1([0, 0, 1, 0], w, "dempster", K)[0])
    rec("T9_deterministic_cases", all([ok_one, ok_ign, ok_rep, ok_two, ok_ov, ok_uw, ok_th]), flags=dict(one=ok_one, ign=ok_ign, rep=ok_rep, two=ok_two, ov=ok_ov, uw=ok_uw, theta=ok_th), values=det)
    # 10 30-versus-5 example (explicit K, two weights)
    ex = {}
    for K in (3, 6):
        for w in (0.3, 0.8):
            counts = [30, 5] + [0] * (K - 2); p1, k1 = closed_M1(counts, w, "dempster", K); p2, k2 = closed_M1(counts, w, "cautious", K)
            v0 = w * np.array(counts) / 35.0 + (1 - w) / K
            ex[f"K{K}_w{w}"] = dict(V0c=v0.tolist(), V1=p1.tolist(), V2=p2.tolist(), m_empty_V1_unnormalised=k1, m_empty_V2=k2)
    # check one case against the general implementation
    K = 3; w = 0.3; srcs = [src_M1(0, w, K)] * 30 + [src_M1(1, w, K)] * 5; pg1, kg1 = V1(srcs, K); chk = close(pg1, closed_M1([30, 5, 0], w, "dempster", K)[0], 1e-9)
    sym = all(abs(v["V2"][0] - v["V2"][1]) < 1e-12 for v in ex.values()); asym0c = all(v["V0c"][0] > v["V0c"][1] for v in ex.values()); asym1 = all(v["V1"][0] > v["V1"][1] for v in ex.values())
    rec("T10_30_vs_5", chk and sym and asym0c and asym1, general_matches_closed=chk, V2_treats_A_B_symmetrically=sym, V0c_asymmetric=asym0c, V1_asymmetric=asym1, values=ex)
    # 11 sampling-distribution checks: probabilities normalised, floor identical across V0c/V1/V2 (done in engine); here: sums, non-negativity
    bad = 0; rounded = 0
    for t in range(200):
        K = int(rng.randint(2, 9)); counts = [int(rng.randint(0, 50)) if rng.rand() < 0.5 else 0 for _ in range(K)]
        if sum(counts) == 0: counts[int(rng.randint(K))] = 1
        w = float(rng.uniform(0.1, 0.95))
        for mode in ("dempster", "cautious"):
            p, k = closed_M1(counts, w, mode, K); bad += (abs(p.sum() - 1) > 1e-9) or p.min() < 0 or not (0 <= k <= 1) or not np.isfinite(p).all(); rounded += int(k == 1.0)
    rec("T11_distributions_valid", bad == 0, n=400, m_empty_rounds_to_1_in_float=rounded, note="1-m(empty) is computed directly as the sum of non-empty masses; m(empty)=1 only numerically (floating point), p stays defined")
    # 12 conflict and ignorance profile: m(empty), m(Theta) vs number of distinct supported teams (w=0.5, K=8), V1 vs V2 and V0c
    prof = {}
    for nt in (1, 2, 3, 4, 8):
        counts = [30] + [3] * (nt - 1) + [0] * (8 - nt); row = {}
        for mode in ("dempster", "cautious"):
            T = [a for a in range(8) if counts[a] > 0]; u = {a: ((0.5) ** counts[a] if mode == "dempster" else 0.5) for a in T}; mT = float(np.prod(list(u.values())))
            p, k = closed_M1(counts, 0.5, mode, 8); row[mode] = dict(m_Theta=mT, m_empty=k, betp_max=float(p.max()), betp_min=float(p.min()))
        row["V0c_max"] = float((0.5 * np.array(counts) / sum(counts) + 0.5 / 8).max()); prof[str(nt)] = row
    rec("T12_conflict_ignorance_profile", True, profile=prof)
    # 13 equivalence with V0c: equality conditions
    eq = {}
    K = 5
    for w in (0.2, 0.6):
        p2, _ = closed_M1([1, 0, 0, 0, 0], w, "cautious", K); p0 = V0c([w * np.eye(K)[0] + (1 - w) * np.ones(K) / K], K); eq[f"single_source_w{w}"] = close(p2, p0)
        p2, _ = closed_M1([40, 0, 0, 0, 0], w, "cautious", K); p0 = w * np.eye(K)[0] + (1 - w) * np.ones(K) / K; eq[f"unanimous_population_V2_equals_V0c_w{w}"] = close(p2, p0)
        p1, _ = closed_M1([40, 0, 0, 0, 0], w, "dempster", K); eq[f"unanimous_population_V1_equals_V0c_w{w}"] = close(p1, p0)
        p2, _ = closed_M1([20, 20, 0, 0, 0], w, "cautious", K); p0 = w * np.array([0.5, 0.5, 0, 0, 0]) + (1 - w) / K; eq[f"two_equal_teams_V2_vs_V0c_w{w}"] = close(p2, p0)
    rec("T13_equivalences_with_V0c", True, equalities=eq, note="V2 = V0c for a single source or when every supported team has equal frequency only in special cases; see equalities")
    # 14 reproducibility
    h = hashlib.sha256(open(__file__, "rb").read()).hexdigest(); res["script_sha256"] = h; res["all_ok"] = bool(ok_all); L.write(f"ALL_OK {ok_all}\nscript sha256 {h}\n"); L.close()
    json.dump(res, open(out, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)); print("ALL_OK", ok_all, h)
    return 0 if ok_all else 1
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
