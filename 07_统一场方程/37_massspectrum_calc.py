# -*- coding: utf-8 -*-
"""openuft/07_统一场方程 · 编号 37 = 系列 39 · 粒子质量谱全序卷锚点
250-digit recomputation of full mass-spectrum ratios (log10), PDG central values:
  leptons (pole): m_e=0.51099895 MeV, m_mu=105.6583755 MeV, m_tau=1776.86 MeV
  quarks: m_u=2.16 MeV, m_d=4.67 MeV, m_s=93.4 MeV (MSbar 2 GeV);
          m_c=1.27 GeV, m_b=4.18 GeV (MSbar); m_t=172.69 GeV (pole)
  bosons (pole): M_W=80.369 GeV, M_Z=91.188 GeV, m_H=125.10 GeV
Writes 37_massspectrum_calc_results.json
"""
import json
import mpmath as mp

mp.mp.dps = 250
res = {}

me = mp.mpf("0.51099895")     # MeV
mmu = mp.mpf("105.6583755")   # MeV
mtau = mp.mpf("1776.86")      # MeV
mu = mp.mpf("2.16")           # MeV
md = mp.mpf("4.67")           # MeV
ms = mp.mpf("93.4")           # MeV
mc = mp.mpf("1270.0")         # MeV
mb = mp.mpf("4180.0")         # MeV
mt = mp.mpf("172690.0")       # MeV (172.69 GeV)
MW = mp.mpf("80.369")         # GeV
MZ = mp.mpf("91.188")         # GeV
mH = mp.mpf("125.10")         # GeV

def ratio_log(a, b, name, note=""):
    r = a / b
    res[name] = {
        "ratio": mp.nstr(r, 250),
        "log10": mp.nstr(mp.log10(r), 250),
        "note": note,
    }

res["leptons"] = {}
ratio_log(mtau, me, "leptons.tau/electron", "m_tau/m_e；三代轻子跨度 3.54 量级")
ratio_log(mmu, me, "leptons.mu/electron", "m_mu/m_e")
ratio_log(mtau, mmu, "leptons.tau/mu", "m_tau/m_mu")

res["quarks_up"] = {}
ratio_log(mt, mc, "quarks_up.t/c", "m_t/m_c（pole/MSbar 混合，标注能标；量级稳健）")
ratio_log(mc, mu, "quarks_up.c/u", "m_c/m_u（MSbar 2 GeV）")
ratio_log(mt, mu, "quarks_up.t/u", "m_t/m_u")

res["quarks_down"] = {}
ratio_log(mb, ms, "quarks_down.b/s", "m_b/m_s（MSbar）")
ratio_log(ms, md, "quarks_down.s/d", "m_s/m_d（MSbar 2 GeV）")
ratio_log(mb, md, "quarks_down.b/d", "m_b/m_d")

res["bosons"] = {}
ratio_log(MZ, MW, "bosons.Z/W", "M_Z/M_W；17 卷 sin^2 theta_W on-shell=0.22305189 相关")
ratio_log(mH, MW, "bosons.H/W", "m_H/M_W")
ratio_log(MW, me * mp.mpf("1e-3"), "bosons.W/electron", "M_W/m_e（GeV/MeV 统一）")

res["notes"] = {
  "energy_scales": "轻子/玻色子=Pole 质量；夸克=MSbar（u/d/s 在 2 GeV，c/b 在各自标度，t 为 Pole 172.69 GeV）——比值量级不依赖能标细节",
  "pdg": "PDG 中心值（文献）",
  "verdict": "质量谱=SM 输入（19 独立常数之一），无生成原理（34 U5 深化）；TUFT 无质量谱预言（23 G1–G5）",
}

print(json.dumps(res, ensure_ascii=False, indent=2))
with open(r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\37_massspectrum_calc_results.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("\nOK -> 37_massspectrum_calc_results.json")
