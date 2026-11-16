"""P6 statistics library (protocol v2.6 sections 6-8): paired bootstrap-t on the mean, Holm, sizing/power simulation, factorial series. Absolute paths only."""
import os, sys, json, math, zlib, glob
import numpy as np
from scipy.stats import chi2, wilcoxon
SC = ["S4-RC101", "S5-RC101", "S4-R101", "S5-R101", "S4-C101", "S5-C101"]
ARMS8 = [f"{m}-{s}-{l}" for m in ("C2", "C3") for l in ("on", "off") for s in ("T", "R")]
ARMS = ARMS8 + ["C0b-T", "C0b-T-off"]
B_DEF = 20000; GRID = [100, 150, 200, 300]; Z80 = 0.842; DELTA = 0.01; NSIM = 1500

def sub_rng(name, base=9101): return np.random.RandomState(zlib.crc32(f"{base}|{name}".encode()) % (2 ** 31))

def boot_t(d, rng, B=B_DEF, idx=None):
    """Paired bootstrap-t on the mean, section 7. Returns (p, info). d: per-seed series. Centre, resample n with replacement, t* = mean*/(sd*/sqrt n);
    replications with sd*=0 excluded (Bv valid); Bv/B<0.99 -> not computable, p=1; else p=(1+#{|t*|>=|t_obs|})/(1+Bv). sd(d)=0: p=1 if mean=0 else 1/(1+B)."""
    d = np.asarray(d, float); n = len(d); m = float(d.mean()); s = float(d.std(ddof=1))
    if d.max() == d.min(): return (1.0 if m == 0.0 else 1.0 / (1 + B)), dict(status="sd_zero", Bv=0)
    t_obs = m / (s / math.sqrt(n)); x = d - m
    if idx is None: idx = rng.randint(0, n, size=(B, n)).astype(np.int32)
    y = x[idx]; mb = y.mean(1); sb = y.std(1, ddof=1); valid = y.max(1) > y.min(1); Bv = int(valid.sum())
    if Bv / B < 0.99: return 1.0, dict(status="not_computable", Bv=Bv, t_obs=t_obs)
    ts = mb[valid] / (sb[valid] / math.sqrt(n)); k = int((np.abs(ts) >= abs(t_obs)).sum())
    return (1 + k) / (1 + Bv), dict(status="ok", Bv=Bv, t_obs=t_obs, k=k)

def boot_t_reference(d, idx, B=B_DEF):
    """Independent slow implementation (pure Python loops, statistics.stdev) from the SAME index matrix; used only to cross-check boot_t."""
    import statistics
    n = len(d); m = sum(d) / n; s = statistics.stdev(d); t_obs = m / (s / math.sqrt(n)); x = [v - m for v in d]; ts = []; Bv = 0
    for row in idx:
        ys = [x[j] for j in row]
        if max(ys) == min(ys): continue
        Bv += 1; ts.append((sum(ys) / n) / (statistics.stdev(ys) / math.sqrt(n)))
    if Bv / B < 0.99: return 1.0
    return (1 + sum(1 for t in ts if abs(t) >= abs(t_obs))) / (1 + Bv)

def holm(ps):
    m = len(ps); order = np.argsort(ps, kind="stable"); adj = np.zeros(m); run = 0.0
    for i, j in enumerate(order): run = max(run, (m - i) * ps[j]); adj[j] = min(1.0, run)
    return adj.tolist()

def boot_ci(x, rng, B=10000):
    x = np.asarray(x, float); n = len(x); mm = x[rng.randint(0, n, (B, n))].mean(1); return [float(np.percentile(mm, 2.5)), float(np.percentile(mm, 97.5))]

def wilc_p(d):
    d = np.asarray(d, float)
    if np.all(d == 0): return 1.0
    if int((d != 0).sum()) < 6: return 1.0
    return float(wilcoxon(d, zero_method="wilcox", alternative="two-sided").pvalue)

def signflip_p(d, rng, B=20000):
    d = np.asarray(d, float); n = len(d); obs = abs(d.mean()); sg = rng.choice([-1.0, 1.0], size=(B, n)); k = int((np.abs((sg * d).mean(1)) >= obs - 1e-15).sum()); return (1 + k) / (1 + B)

# ---------------------------------------------------------------- factorial series from a per-seed arm matrix H[arm] (arrays over seeds)
def series(H):
    Dm = lambda m, l: H[f"{m}-T-{l}"] - H[f"{m}-R-{l}"]; HVm = lambda m, l: 0.5 * (H[f"{m}-T-{l}"] + H[f"{m}-R-{l}"])
    out = {}
    out["H6.1"] = (HVm("C2", "on") - HVm("C3", "on")) - (HVm("C2", "off") - HVm("C3", "off"))
    out["H6.2"] = 0.25 * (Dm("C2", "on") + Dm("C2", "off") + Dm("C3", "on") + Dm("C3", "off"))
    out["H6.3"] = 0.5 * sum(Dm("C2", l) - Dm("C3", l) for l in ("on", "off"))
    out["H6.4"] = 0.5 * sum(Dm(m, "on") - Dm(m, "off") for m in ("C2", "C3"))
    out["H6.5"] = (Dm("C2", "on") - Dm("C3", "on")) - (Dm("C2", "off") - Dm("C3", "off"))
    if "C0b-T" in H: out["H6.6"] = H["C2-T-on"] - H["C0b-T"]
    return out

# ---------------------------------------------------------------- sizing (section 8)
def sizing_task(args):
    """args: (name, series list, alpha, m, seed_tag). Full grid, both directions. Returns a JSON-able dict; deterministic (own sub-stream per (name, m, n, direction))."""
    name, ser, alpha, m, nsim, B = args; d = np.asarray(ser, float); n_p = len(d); s = float(d.std(ddof=1)); sd_haut = s * math.sqrt((n_p - 1) / chi2.ppf(0.2, n_p - 1)) * m
    zq = {0.05: 1.960, 0.01: 2.576}[alpha]; n_f = math.ceil(((zq + Z80) * sd_haut / DELTA) ** 2); base = (d - d.mean()) * m; res = {}
    for g in GRID:
        pw = {}
        for sh, nm in ((+DELTA, "plus"), (-DELTA, "minus")):
            rng = sub_rng(f"power|{name}|{m}|{g}|{nm}"); rej = 0
            for _ in range(nsim):
                smp = base[rng.randint(0, n_p, g)] + sh; p, _ = boot_t(smp, rng, B); rej += int(p < alpha)
            pw[nm] = rej / nsim
        pmin = min(pw.values()); res[g] = dict(power_plus=pw["plus"], power_minus=pw["minus"], power_min=pmin, mc_se=math.sqrt(max(pmin * (1 - pmin), 1e-12) / nsim),
                                                  mc_ci95=[pmin - 1.96 * math.sqrt(pmin * (1 - pmin) / nsim), pmin + 1.96 * math.sqrt(pmin * (1 - pmin) / nsim)])
    ok = [g for g in GRID if res[g]["power_min"] >= 0.8]; n_s = ok[0] if ok else None
    cand = [g for g in GRID if g >= max(n_f, n_s if n_s is not None else 10 ** 9)]; n_c = cand[0] if cand else None
    return dict(name=name, m=m, alpha=alpha, n_pilot=n_p, mean=float(d.mean()), sd=s, sd_haut_times_m=sd_haut, n_f=n_f, power=res, n_s=n_s, n_contraste=n_c, n_contraste_report=(n_c if n_c else ">300"), n_s_report=(n_s if n_s else ">300"))
