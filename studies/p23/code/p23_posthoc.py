"""P23 post hoc DESCRIPTIVE annex (not pre-registered, not part of the freeze). Reads stored runs only. No confirmatory claims."""
import sys, os, json, glob
import warnings; warnings.filterwarnings("ignore"); import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.stats import spearmanr
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p23"; OUT = B + "/posthoc"; os.makedirs(OUT, exist_ok=True)
R = {}
for f in sorted(glob.glob(B + "/runs/main/*.json")): o = json.load(open(f)); R[(o["sc"], o["seed"])] = o
SC = ["S4-RC101", "S4-R101", "S4-C101", "S5-RC101", "S5-R101", "S5-C101"]; seeds = sorted({k[1] for k in R}); n = len(seeds)
H = lambda a, sc: np.array([R[(sc, s)]["conds"][a]["hv_oracle"] for s in seeds])
rng = np.random.RandomState(20261114); idx = rng.randint(0, n, size=(5000, n))
def ci(d): bm = d[idx].mean(1); return float(d.mean()), float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))
res = {"per_scenario_contrast": {}, "by_type": {}, "diversity": {}, "div_vs_hv": {}, "decoding_by_type": {}}
pairs = {"DA25-Dg": ("DA25", "Dg100"), "DA50-Dg": ("DA50", "Dg100"), "DA100-Dg": ("DA100", "Dg100"), "DA100-E": ("DA100", "E")}
for k, (a, b) in pairs.items(): res["per_scenario_contrast"][k] = {sc: ci(H(a, sc) - H(b, sc)) for sc in SC}
TY = {"R": ["S4-R101", "S5-R101"], "RC": ["S4-RC101", "S5-RC101"], "C": ["S4-C101", "S5-C101"]}
for k, (a, b) in pairs.items(): res["by_type"][k] = {t: ci(np.mean([H(a, sc) - H(b, sc) for sc in v], 0)) for t, v in TY.items()}
GEN = (1, 25, 50, 100, 150); ARMS = ["E", "DA25", "DA50", "DA100", "Dg100", "RHO", "MIX"]
for a in ARMS: res["diversity"][a] = {k: {str(g): float(np.mean([r["conds"][a]["dyn"][g][k] for r in R.values()])) for g in GEN} for k in ("dep", "neff", "frac_dup", "q_max")}
for a in ARMS:
    cors = []
    for sc in SC:
        x = np.array([R[(sc, s)]["conds"][a]["dyn"][150]["neff"] for s in seeds]); y = H(a, sc); cors.append(float(spearmanr(x, y)[0]))
    res["div_vs_hv"][a] = dict(per_scenario=dict(zip(SC, cors)), mean=float(np.nanmean(cors)))
for a in ("E", "DA100", "Dg100", "RHO"):
    res["decoding_by_type"][a] = {t: {k: float(np.mean([x[k] for sc in v for s in seeds for x in R[(sc, s)]["conds"][a]["log"] if x["gen"] == 150])) for k in ("dec_max", "dec_ent", "L1_dec_target")} for t, v in TY.items()}
json.dump(res, open(OUT + "/p23_posthoc.json", "w"), indent=1)
C = {"DA25-Dg": "#c0504d", "DA50-Dg": "#e08a3c", "DA100-Dg": "#7a4fa0", "DA100-E": "#3d7ea6"}
fig, ax = plt.subplots(1, 1, figsize=(9, 4.6)); w = 0.2
for i, (k, col) in enumerate(C.items()):
    m = [res["per_scenario_contrast"][k][sc][0] for sc in SC]; lo = [res["per_scenario_contrast"][k][sc][1] for sc in SC]; hi = [res["per_scenario_contrast"][k][sc][2] for sc in SC]
    x = np.arange(6) + (i - 1.5) * w; ax.errorbar(x, m, yerr=[np.array(m) - np.array(lo), np.array(hi) - np.array(m)], fmt="o", color=col, capsize=3, label=k)
ax.axhline(0, color="k", lw=.8); ax.axhline(.005, color="gray", ls=":", lw=.8); ax.axhline(-.005, color="gray", ls=":", lw=.8)
ax.set_xticks(range(6)); ax.set_xticklabels(SC, fontsize=8); ax.set_ylabel("Δ HV oracle (moyenne, IC 95 % descriptif)"); ax.set_title("P23 post hoc : contrastes par scénario (pointillés = ±0,005)"); ax.legend(fontsize=8, ncol=4); fig.tight_layout(); fig.savefig(OUT + "/fig_contrastes_par_scenario.png", dpi=150); plt.close(fig)
fig, axs = plt.subplots(1, 3, figsize=(12, 3.8)); col = {"E": "#3d7ea6", "DA100": "#7a4fa0", "Dg100": "#c0504d", "RHO": "#2e9e6b"}
for ax, k, tt in zip(axs, ("q_max", "dep", "neff"), ("q_max de la cible", "dépendance génotypique (Dep)", "N_eff")):
    for a in col: ax.plot(range(1, 151), np.mean([[d[k] for d in r["conds"][a]["dyn"][1:]] for r in R.values()], 0), color=col[a], label=a)
    ax.set_title(tt, fontsize=10); ax.set_xlabel("génération")
axs[0].legend(fontsize=8); fig.suptitle("P23 post hoc : trajectoires (moyenne sur 600 runs)", fontsize=10); fig.tight_layout(); fig.savefig(OUT + "/fig_trajectoires.png", dpi=150); plt.close(fig)
lam = [0, .25, .5, 1]; hv = [H(a, sc).mean() for a in ("E", "DA25", "DA50", "DA100") for sc in [SC[0]]]
fig, ax = plt.subplots(figsize=(6, 3.8))
for sc in SC: ax.plot(lam, [H(a, sc).mean() - H("E", sc).mean() for a in ("E", "DA25", "DA50", "DA100")], marker="o", label=sc)
ax.axhline(0, color="k", lw=.8); ax.set_xlabel("λ"); ax.set_ylabel("HV(DA(λ)) − HV(E)"); ax.set_title("P23 post hoc : HV selon λ, par scénario", fontsize=10); ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(OUT + "/fig_hv_lambda.png", dpi=150); plt.close(fig)
print(json.dumps({k: res[k] for k in ("by_type", "div_vs_hv")}, indent=0)[:2500])
