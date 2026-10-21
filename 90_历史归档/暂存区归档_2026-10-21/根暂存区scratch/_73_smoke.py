# -*- coding: utf-8 -*-
"""73 卷冒烟诊断：修复后三项机读验证（不产出交付物）。
1) CT7 核心：rk4_run 落点修复后 mpmath vs float64 的 Λ_I 一致度
2) CT5 探针：Case B 口径 dlog10Λ/dm_h、dlog10Λ/dm_t 真实量级
3) β 两套实现逐点一致（beta_all vs 内联 f64 bb）
"""
import runpy
import math
from mpmath import mp, mpf, log, exp, sqrt

SRC = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\73_higgs_stability_calc.py"
mod = runpy.run_path(SRC)

M_H = mod["M_H"]; M_T = mod["M_T"]; DT = mpf("0.01")

print("=== [1] CT7 核心：mpmath vs float64 Λ_I（Case A, LO 匹配）===")
lam_mp = mod["instability_scale"](M_H, M_T, None, None, 2, DT)
lam_f = mod["instability_scale_f64"](M_H, M_T, 2, 0.01)
print("mpmath Λ_I =", mp.nstr(lam_mp, 12) if lam_mp is not None else None)
print("f64    Λ_I =", lam_f)
if lam_mp is not None and lam_f is not None:
    rel = abs(lam_mp - mpf(str(lam_f))) / lam_mp
    print("相对差 =", mp.nstr(rel, 8), " 阈 1e-6")

print()
print("=== [2] CT5 探针：Case B 敏感度（带匹配标度扫描，±0.5 GeV 中心差）===")
BM_M_H = mod["BM_M_H"]; BM_M_T = mod["BM_M_T"]
BM_LAM = mod["BM_LAM_NNLO"]; BM_YT = mod["BM_YT_NNLO"]


def log_scan(m_h, m_t):
    lam0 = BM_LAM * (m_h / BM_M_H) ** 2
    y0 = BM_YT * (m_t / BM_M_T)
    s = mod["instability_scale"](m_h, m_t, lam0, y0, 2, DT)
    return None if s is None else log(s) / log(10)


l0 = log_scan(BM_M_H, BM_M_T)
lh = log_scan(BM_M_H + mpf("0.5"), BM_M_T)
ll = log_scan(BM_M_H - mpf("0.5"), BM_M_T)
ltp = log_scan(BM_M_H, BM_M_T + mpf("0.5"))
ltm = log_scan(BM_M_H, BM_M_T - mpf("0.5"))
print("log10 Λ(中心) =", mp.nstr(l0, 8) if l0 is not None else None)
smh = (lh - ll) if (lh is not None and ll is not None) else None
smt = (ltp - ltm) if (ltp is not None and ltm is not None) else None
print("sens_mh =", mp.nstr(smh, 6) if smh is not None else None,
      "（文献 Eq.67: +0.7）")
print("sens_mt =", mp.nstr(smt, 6) if smt is not None else None,
      "（文献 Eq.67: -1.0）")

print()
print("=== [3] β 两套实现逐点一致（beta_all vs 内联 f64 bb）===")


def bb_f64(lam, y, g2, gp, g3, loop=2):
    P = 16 * math.pi ** 2
    y2, y4, y6 = y * y, y ** 4, y ** 6
    g22, g24, g26 = g2 * g2, g2 ** 4, g2 ** 6
    gp2, gp4, gp6 = gp * gp, gp ** 4, gp ** 6
    g32, g34 = g3 * g3, g3 ** 4
    lam2 = lam * lam
    b1 = (24 * lam2 - 6 * y4 + 0.375 * (2 * g24 + (g22 + gp2) ** 2)
          + (-9 * g22 - 3 * gp2 + 12 * y2) * lam)
    if loop == 1:
        return [b1 / P, None, None, None, None]
    b2 = ((1 / 48) * (915 * g26 - 289 * g24 * gp2 - 559 * g22 * gp4 - 379 * gp6)
          + 30 * y6 - y4 * (8 / 3 * gp2 + 32 * g32 + 3 * lam)
          + lam * (-73 / 8 * g24 + 39 / 4 * g22 * gp2 + 629 / 24 * gp4
                   + 108 * g22 * lam + 36 * gp2 * lam - 312 * lam2)
          + y2 * (-9 / 4 * g24 + 21 / 2 * g22 * gp2 - 19 / 4 * gp4
                  + lam * (45 / 2 * g22 + 85 / 6 * gp2 + 80 * g32 - 144 * lam)))
    return [b1 / P + b2 / P ** 2, None, None, None, None]


maxrel = mpf("0")
for lam, y, g2, gp, g3 in [(0.129, 0.94, 0.648, 0.358, 1.167),
                           (0.05, 0.5, 0.55, 0.40, 1.05),
                           (0.30, 0.80, 0.60, 0.36, 1.10),
                           (0.001, 0.40, 0.70, 0.50, 0.60)]:
    for loop in (1, 2):
        b_mp = mod["beta_all"](mpf(lam), mpf(y), mpf(g2), mpf(gp), mpf(g3), loop=loop)[0]
        b_f = bb_f64(lam, y, g2, gp, g3, loop)[0]
        d = abs(b_mp - mpf(str(b_f)))
        r = d / max(abs(b_mp), mpf("1e-300"))
        maxrel = max(maxrel, r)
        print(f"  lam={lam} loop={loop}: mp={mp.nstr(b_mp, 10)} f64={b_f:.12e} rel={mp.nstr(r, 3)}")
print("max rel =", mp.nstr(maxrel, 6))
print()
print("SMOKE DONE")
