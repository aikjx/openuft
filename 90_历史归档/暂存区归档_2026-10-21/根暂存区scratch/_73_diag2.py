# -*- coding: utf-8 -*-
"""73 卷补充诊断（三项）：
D1: Case A/B 轨迹形状与单调性违背位置（λ 过零后是否真回升）
D2: 回升特征的步长收敛（dt=0.002 vs 0.01）
D3: Case B 口径 α₃ 敏感度（G5/B2 修复用）
"""
import runpy
from mpmath import mp, mpf, log, exp, sqrt

SRC = r"D:\a10\aikjx\code\my_lib\openuft\07_统一场方程\73_higgs_stability_calc.py"
mod = runpy.run_path(SRC)

M_H = mod["M_H"]; M_T = mod["M_T"]
BM_M_H = mod["BM_M_H"]; BM_M_T = mod["BM_M_T"]
BM_LAM = mod["BM_LAM_NNLO"]; BM_YT = mod["BM_YT_NNLO"]
D_A3 = mod["D_A3"]
DT = mpf("0.01")

print("=== D1: 轨迹形状（Case A LO @物理点 / Case B NNLO @基准点）===")


def traj_of(m_h, m_t, lm, ym, dt):
    out = mod["assemble"](m_h, m_t, lm, ym, 2, dt, use_cache=False)
    return out


outA = traj_of(M_H, M_T, None, None, DT)
lam0B = BM_LAM * (BM_M_H / BM_M_H) ** 2
y0B = BM_YT * (BM_M_T / BM_M_T)
outB = traj_of(BM_M_H, BM_M_T, BM_LAM, BM_YT, DT)

for tag, out in [("A(LO)", outA), ("B(NNLO)", outB)]:
    ts, sts = out["traj"]
    lam = [s[0] for s in sts]
    # 单调性违背位置
    bad = [(i, mp.nstr(ts[i], 6), mp.nstr(lam[i], 8), mp.nstr(lam[i + 1], 8))
           for i in range(len(lam) - 1) if not (lam[i + 1] < lam[i])]
    print(f"[{tag}] n={len(lam)} 违背数={len(bad)}")
    for b in bad[:8]:
        print("   i=%s t=%s λ_i=%s λ_i+1=%s" % b)
    # 选点打印
    marks = [mpf("5.15"), mpf("10"), mpf("13.3"), mpf("16"), mpf("20"), mpf("25"),
             mpf("30"), mpf("35"), mpf("40"), mpf("44.4")]
    row = []
    for tm in marks:
        best = min(range(len(ts)), key=lambda i: abs(ts[i] - tm))
        row.append("t=%s:λ=%s" % (mp.nstr(ts[best], 4), mp.nstr(lam[best], 6)))
    print("   ", " | ".join(row))
    print("    λ(M_Pl)=", mp.nstr(lam[-1], 8), " t_cross0=",
          mp.nstr(out["t_cross0"], 6) if out["t_cross0"] is not None else None)

print()
print("=== D2: 回升特征步长收敛（Case A, dt=0.002 vs 0.01）===")
outA2 = traj_of(M_H, M_T, None, None, mpf("0.002"))
ts2, sts2 = outA2["traj"]
lam2 = [s[0] for s in sts2]
bad2 = sum(1 for i in range(len(lam2) - 1) if not (lam2[i + 1] < lam2[i]))
print("dt=0.002: n=%d 违背数=%d λ(M_Pl)=%s" % (len(lam2), bad2, mp.nstr(lam2[-1], 8)))
print("dt=0.010: λ(M_Pl)=%s" % mp.nstr([s[0] for s in outA['traj'][1]][-1], 8))
# 最小值位置
i_min = min(range(len(lam2)), key=lambda i: lam2[i])
print("dt=0.002 最小值: t=%s λ=%s" % (mp.nstr(ts2[i_min], 6), mp.nstr(lam2[i_min], 8)))
i_min1 = min(range(len(outA["traj"][1])), key=lambda i: outA["traj"][1][i][0])
print("dt=0.010 最小值: t=%s λ=%s" % (mp.nstr(outA["traj"][0][i_min1], 6),
                                    mp.nstr(outA["traj"][1][i_min1][0], 8)))

print()
print("=== D3: Case B 口径 α₃ 敏感度（G5/B2 修复用）===")


def log_scan_bm(a3=None):
    if a3 is not None:
        mod["A3_MZ"] = a3
    s = mod["instability_scale"](BM_M_H, BM_M_T, BM_LAM, BM_YT, 2, DT)
    return None if s is None else log(s) / log(10)


l0 = log_scan_bm()
lp = log_scan_bm(mod["A3_MZ"] + D_A3)
lm = log_scan_bm(mod["A3_MZ"] - D_A3)
print("log10 Λ(中心)=%s  +σ=%s  -σ=%s" % (mp.nstr(l0, 8), mp.nstr(lp, 8), mp.nstr(lm, 8)))
print("dlog10Λ/dα₃(中心差/2σ) =", mp.nstr((lp - lm) / (2 * D_A3), 6),
      " per unit α₃ ⇒ 每 σ: ", mp.nstr(abs(lp - lm) / 2, 6), "dex")
print()
print("DIAG DONE")
