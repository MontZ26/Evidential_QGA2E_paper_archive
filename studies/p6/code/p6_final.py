"""P6 single confirmatory analysis (protocol v2.6 sections 6-7). Usage: python p6_final.py CONF_DIR OUT.json FREEZE.txt. RUN ONCE, after p6_precheck.py PASS."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p6_stats as S, p6_load as L
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"); import run_p1m as R
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6"
NAMES = ["H6.1", "H6.2", "H6.3", "H6.4", "H6.5", "H6.6"]
DESC = {"H6.1": "interaction model x LS budget policy (primary, alpha 0.05)", "H6.2": "main effect of parental selection (T-R)", "H6.3": "selection x model", "H6.4": "selection x LS", "H6.5": "three-factor interaction", "H6.6": "C2-T-on minus C0b-T"}
def summ(x, nm):
    x = np.asarray(x, float); return dict(mean=float(x.mean()), median=float(np.median(x)), sd=float(x.std(ddof=1)), ci95_boot=S.boot_ci(x, S.sub_rng("ci|" + nm)), share_positive=float((x > 0).mean()))
def main(d, out, freeze):
    assert R.verify_freeze(freeze), "freeze verification failed"
    res = L.load_dir(d); keep, excl = L.usable(res, S.ARMS); H = L.hv_matrix(res, keep); n = len(keep); se = S.series(H); rep = dict(n_seeds=n, seeds=[keep[0], keep[-1]], excluded=excl)
    ps = {}; tests = {}
    for nm in NAMES:
        p, info = S.boot_t(se[nm], S.sub_rng("test|" + nm)); ps[nm] = p
        tests[nm] = dict(desc=DESC[nm], p_raw=p, boot_info=info, **summ(se[nm], nm), p_wilcoxon_sensitivity=S.wilc_p(se[nm]), p_signflip_sensitivity=S.signflip_p(se[nm], S.sub_rng("sf|" + nm)))
    sec = ["H6.2", "H6.3", "H6.4", "H6.5", "H6.6"]; adj = S.holm([ps[k] for k in sec])
    for k, a in zip(sec, adj): tests[k]["p_holm"] = a; tests[k]["reject_holm_0.05"] = bool(a < 0.05)
    tests["H6.1"]["reject_0.05"] = bool(ps["H6.1"] < 0.05); rep["tests"] = tests
    hist, edges = np.histogram(se["H6.1"], bins=20); rep["H6.1_histogram"] = dict(counts=hist.tolist(), edges=edges.tolist())
    # descriptive
    desc = {}
    desc["hv_mean_by_arm"] = {a: dict(mean=float(H[a].mean()), sd=float(H[a].std(ddof=1))) for a in S.ARMS}
    Dm = lambda m, l: H[f"{m}-T-{l}"] - H[f"{m}-R-{l}"]
    desc["D_cells"] = {f"{m}-{l}": summ(Dm(m, l), f"D{m}{l}") for m in ("C2", "C3") for l in ("on", "off")}
    simple = {}
    for l in ("on", "off"):
        for s in ("T", "R"): simple[f"C2-C3|{s}|{l}"] = summ(H[f"C2-{s}-{l}"] - H[f"C3-{s}-{l}"], f"simple{s}{l}")
    desc["model_simple_effects_C2minusC3"] = simple
    desc["M_on"] = summ(0.5 * (H["C2-T-on"] + H["C2-R-on"]) - 0.5 * (H["C3-T-on"] + H["C3-R-on"]), "Mon"); desc["M_off"] = summ(0.5 * (H["C2-T-off"] + H["C2-R-off"]) - 0.5 * (H["C3-T-off"] + H["C3-R-off"]), "Moff")
    desc["LS_gain_on_minus_off"] = {f"{m}-{s}": summ(H[f"{m}-{s}-on"] - H[f"{m}-{s}-off"], f"gain{m}{s}") for m in ("C2", "C3") for s in ("T", "R")}
    desc["C0bT_off_minus_C0bT"] = summ(H["C0b-T-off"] - H["C0b-T"], "c0boff"); desc["C0bT_minus_C2Ton"] = summ(H["C0b-T"] - H["C2-T-on"], "c0bvsc2"); desc["C2Ton_minus_C3Ton"] = summ(H["C2-T-on"] - H["C3-T-on"], "c2c3on")
    desc["equivalence_zone_[-0.01,0.01]_ci_inside"] = {k: bool(tests[k]["ci95_boot"][0] >= -0.01 and tests[k]["ci95_boot"][1] <= 0.01) for k in NAMES}
    agg = {a: dict(n_M=0, n_G=0, ins_M=0, ins_G=0, ls_eval=0, ins_L=0, shards=0, t=0.0, gens=0, ent=[], div=[]) for a in S.ARMS}; ks = set(keep)
    for k, r in res.items():
        if not r.get("feasible") or r["seed"] not in ks: continue
        for a in S.ARMS:
            c = r["conds"][a]; g = agg[a]; cn = c["cnt"]; g["shards"] += 1; g["t"] += c["search_time_s"]; g["gens"] += c["gens"]; g["ls_eval"] += cn.get("ls_eval", 0)
            g["n_M"] += cn.get("n_M", 0); g["n_G"] += cn.get("n_G", 0); g["ins_M"] += cn.get("ins_M", 0); g["ins_G"] += cn.get("ins_G", 0); g["ins_L"] += cn.get("ins_L", 0)
            if c.get("ent"): g["ent"].append(c["ent"][-1][1])
            if c.get("div") and "6000" in c["div"]: g["div"].append(c["div"]["6000"])
    rates = {}
    for a, g in agg.items():
        tot = g["n_M"] + g["n_G"]
        rates[a] = dict(shards=g["shards"], mean_time_s=g["t"] / g["shards"], mean_generations=g["gens"] / g["shards"], realised_prop_M=(g["n_M"] / tot if tot else None), n_M=g["n_M"], n_G=g["n_G"],
                        ins_rate_M=(g["ins_M"] / g["n_M"] if g["n_M"] else None), ins_rate_G=(g["ins_G"] / g["n_G"] if g["n_G"] else None), ls_neighbours_evaluated=g["ls_eval"], ins_rate_LS_neighbours=(g["ins_L"] / g["ls_eval"] if g["ls_eval"] else None),
                        mean_final_entropy=(float(np.mean(g["ent"])) if g["ent"] else None), mean_diversity_at_6000=(float(np.mean(g["div"])) if g["div"] else None))
    desc["rates_and_diagnostics"] = rates; tuned = json.load(open(BASE + "/p6_tuned.json")); desc["retained_configs"] = tuned; rep["descriptive"] = desc
    L.save(rep, out)
    print("n seeds", n, "excluded", len(excl))
    for nm in NAMES: t = tests[nm]; print(nm, f"mean {t['mean']:+.5f}  CI {t['ci95_boot'][0]:+.5f},{t['ci95_boot'][1]:+.5f}  p_raw {t['p_raw']:.5f}", f"p_holm {t.get('p_holm', float('nan')):.5f}" if "p_holm" in t else "")
if __name__ == "__main__": main(sys.argv[1], sys.argv[2], sys.argv[3])
