# -*- coding: utf-8 -*-
"""73 卷补丁冒烟：①上穿探测器行为 ②H5 扫描预览 ③G5 双操作点 σ 预览。"""
import runpy

SRC = "D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/73_higgs_stability_calc.py"
mod = runpy.run_path(SRC)
mpf = mod["mpf"]
assemble = mod["assemble"]
BM_M_H, BM_M_T = mod["BM_M_H"], mod["BM_M_T"]
BM_LAM_NNLO, BM_YT_NNLO = mod["BM_LAM_NNLO"], mod["BM_YT_NNLO"]
M_H, M_T = mod["M_H"], mod["M_T"]

print("== ① 上穿探测器（t_cross_np）行为 ==")
for mh in ["125.25", "150", "160", "165", "170", "175", "180"]:
    out = assemble(mpf(mh), M_T, None, None, 2, mpf("0.01"))
    t_np = out["t_cross_np"]
    lam_end = out["lam_Mpl"]
    print("  m_h=%7s  t_cross_np=%s  λ(M_Pl)=%s" % (
        mh, ("None" if t_np is None else "%.6f" % float(t_np)),
        "%.6f" % float(lam_end)))

print("== ② Case B σ 预览（中心差，±1 GeV）==")


def scan_b(mh, mt):
    lam0 = BM_LAM_NNLO * (mpf(mh) / BM_M_H) ** 2
    y0 = BM_YT_NNLO * (mpf(mt) / BM_M_T)
    from mpmath import log as _log
    s = mod["instability_scale"](mpf(mh), mpf(mt), lam0, y0, 2, mpf("0.01"))
    return None if s is None else _log(s) / _log(10)


l0 = scan_b("125.25", "172.57")
lh = scan_b("126.25", "172.57")
ll = scan_b("124.25", "172.57")
lt = scan_b("125.25", "173.57")
ltm = scan_b("125.25", "171.57")
D_M_H, D_M_T = mod["D_M_H"], mod["D_M_T"]
s_mh = abs((lh - ll) / 2) * D_M_H
s_mt = abs((lt - ltm) / 2) * D_M_T
print("  l0=%.5f  sens_mh=%.4f/GeV  sens_mt=%.4f/GeV" % (l0, (lh - ll) / 2, (lt - ltm) / 2))
print("  σ_mh=%.4f  σ_mt=%.4f  ⇒ σ_tot(不含a3)≈%.4f dex" % (s_mh, s_mt, (s_mh**2 + s_mt**2) ** 0.5))
print("  B2 阈值 0.2 ⇒ 预估 verdict:", "FAIL" if (s_mh**2 + s_mt**2) ** 0.5 > 0.2 else "PASS")
