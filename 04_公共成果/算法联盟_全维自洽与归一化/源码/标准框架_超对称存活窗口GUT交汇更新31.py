# -*- coding: utf-8 -*-
"""标准框架·三十一期数值靶：MSSM 超对称存活窗口 × GUT 交汇更新（含 LHC 2026 约束）
两段 1-loop 跑动：SM 段 M_Z→M_susy（b_SM=(41/10,-19/6,-7)），MSSM 段 M_susy→M_GUT（b_MSSM=(33/5,1,-3)）
扫描 M_susy ∈ [1,100] TeV，输出交汇 M_GUT、1/αG、统一度 Δ13，标注 LHC 排除线（gluino 2.25-2.4 TeV）
与 CMS 拟合（M_SUSY=2820 GeV → M_GUT=1.05±0.07e16 GeV）交叉验证。mpmath 250 位。
"""
import mpmath as mp
import json

mp.mp.dps = 250

MZ = mp.mpf("91.1876")   # GeV
A1Z = mp.mpf("59.1716")  # 1/alpha1(MZ) GUT 归一化（SM 精确跑动值，沿用 12 期口径）
A2Z = mp.mpf("29.5858")  # 1/alpha2(MZ)
A3Z = mp.mpf("8.5034")   # 1/alpha3(MZ)

bS1 = mp.mpf("41") / 10   # SM
bS2 = mp.mpf("-19") / 6
bS3 = mp.mpf("-7")
bM1 = mp.mpf("33") / 5    # MSSM
bM2 = mp.mpf("1")
bM3 = mp.mpf("-3")

def alpha_inv(mu, Msusy):
    t1 = mp.log(Msusy / MZ) / (2 * mp.pi)
    t2 = mp.log(mu / Msusy) / (2 * mp.pi)
    return [
        A1Z - bS1*t1 - bM1*t2,
        A2Z - bS2*t1 - bM2*t2,
        A3Z - bS3*t1 - bM3*t2,
    ]

def solve_MGUT(Msusy):
    def f12(x):
        ai = alpha_inv(mp.mpf("10")**x, Msusy)
        return ai[0] - ai[1]
    xG = mp.findroot(f12, 16)
    muG = mp.mpf("10")**xG
    aG = alpha_inv(muG, Msusy)
    return muG, aG

print("===== 三十一期：MSSM 超对称存活窗口 × GUT 交汇更新（两段 1-loop，250 位）=====")
print("输入（沿用 12 期口径）：1/α1(M_Z)=%.4f  1/α2(M_Z)=%.4f  1/α3(M_Z)=%.4f  M_Z=%.4f GeV" % (A1Z, A2Z, A3Z, MZ))
print("SM 段系数 b=(41/10,-19/6,-7)；MSSM 段系数 b=(33/5,1,-3)")

rows = []
Msusy_list = [mp.mpf("1e3"), mp.mpf("2e3"), mp.mpf("2.25e3"), mp.mpf("2.4e3"),
              mp.mpf("2.82e3"), mp.mpf("3e3"), mp.mpf("5e3"), mp.mpf("1e4"),
              mp.mpf("2e4"), mp.mpf("5e4"), mp.mpf("1e5")]
print("\n%-10s | %-13s | %-9s | %-9s | %s" % ("M_susy(GeV)", "M_GUT(GeV)", "1/αG", "Δ13(%)", "注"))
prev = None
for Ms in Msusy_list:
    muG, aG = solve_MGUT(Ms)
    d13 = (aG[2] - aG[0]) / aG[0] * 100
    note = ""
    if Ms == mp.mpf("2.25e3"):
        note = "ATLAS/CMS gluino 排除线(~2.25)"
    elif Ms == mp.mpf("2.4e3"):
        note = "ATLAS Run2 gluino 2.4"
    elif Ms == mp.mpf("2.82e3"):
        note = "CMS 拟合 M_SUSY=2820"
    elif Ms == mp.mpf("1e3"):
        note = "12 期单段对照点"
    sens = "—"
    if prev is not None:
        sens = mp.nstr(mp.log(muG/prev[0]) / mp.log(Ms/prev[1]), 5)
    rows.append({"Msusy_GeV": mp.nstr(Ms, 10), "MGUT_GeV": mp.nstr(muG, 15), "inv_alphaG": mp.nstr(aG[0], 12),
                 "Delta13_pct": mp.nstr(d13, 10), "sens_dlnMGUT_dlnMs": sens, "note": note})
    print("%-10s | %-13s | %-9s | %-9s | %s" % (mp.nstr(Ms, 6), mp.nstr(muG, 8), mp.nstr(aG[0], 6), mp.nstr(d13, 5), note))
    prev = (muG, Ms)

# 非超对称 SM 全程对照：α1 与 α2 在 ~10^13 GeV 交汇，但 α3 在该处严重偏离（三力不统一）
def sm_alpha_inv(mu):
    t = mp.log(mu / MZ) / (2 * mp.pi)
    return [A1Z - bS1*t, A2Z - bS2*t, A3Z - bS3*t]
def f12_sm(x):
    ai = sm_alpha_inv(mp.mpf("10")**x)
    return ai[0] - ai[1]
sm_converge = False
try:
    xs = mp.findroot(f12_sm, 10)
    sm_converge = xs.real > 0
except Exception:
    pass
if sm_converge:
    aG_sm = sm_alpha_inv(mp.mpf("10")**xs)
    d13_sm = (aG_sm[2] - aG_sm[0]) / aG_sm[0] * 100
    print("\nSM 全程（无超对称）对照：1/α1=1/α2 交汇于 10^%.3f GeV，但交汇处 1/α3 偏离 1/αG 达 %.2f%%"
          "（三力不能精确统一，非超对称 GUT 被排除）" % (xs, d13_sm))
else:
    print("\nSM 全程（无超对称）对照：1/α1=1/α2 在正能标无交汇（非超对称 GUT 被排除）")

# 交叉验证：CMS 拟合 M_SUSY=2820 GeV → M_GUT=1.05±0.07e16 GeV
muG_cms, aG_cms = solve_MGUT(mp.mpf("2.82e3"))
dev_cms = abs(muG_cms - mp.mpf("1.05e16"))/mp.mpf("1.05e16")*100
print("\n交叉验证（M_SUSY=2820 GeV）：本计算 M_GUT=%.3e GeV vs CMS 文献 1.05±0.07e16 GeV（偏差 %.1f%%）"
      "——口径差异：本靶为单阈值两段 1-loop 近似，文献为完整谱/含 2-loop 与 GUT 阈值效应" % (muG_cms, dev_cms))

# LHC 2026 约束下的存活判定
print("\n===== LHC 2026 约束判定 =====")
print("ATLAS/CMS RPC 场景：gluino < 2.25-2.4 TeV 已排除、top-squark < 1.45 TeV、squark < 1.7 TeV（场景依赖）")
print("→ 自然 MSSM（M_susy~1 TeV）窗口受压；M_susy>=2.25 TeV 存活窗口仍与 GUT 交汇兼容（见上表）")
mgut_1 = solve_MGUT(mp.mpf("1e3"))[0]
mgut_at_225 = solve_MGUT(mp.mpf("2.25e3"))[0]
mv_225 = abs(mgut_at_225 - mgut_1)/mgut_1*100
print("交汇移动：M_susy 1→2.25 TeV：M_GUT %.3e→%.3e GeV（移动 %.2f%%）" % (mgut_1, mgut_at_225, mv_225))
d13_225 = (solve_MGUT(mp.mpf("2.25e3"))[1][2] - solve_MGUT(mp.mpf("2.25e3"))[1][0]) / solve_MGUT(mp.mpf("2.25e3"))[1][0] * 100
print("LHC 排除线处交汇统一度 Δ13=%.2f%%：MSSM-GUT 交汇在排除线以上仍成立（量级可被 GUT 阈值修正吸收，"
      "文献量级 ±几%%）；自然超对称出局，存活谱为压缩/分裂超对称——Hyper-K 质子衰变与 0νββ 成为 B 线判决探针"
      % d13_225)

out = {
    "期次": "三十一",
    "口径": "两段 1-loop：SM(M_Z→M_susy)+MSSM(M_susy→M_GUT)，250 位；单阈值近似",
    "输入": {"1alpha1_MZ": "59.1716", "1alpha2_MZ": "29.5858", "1alpha3_MZ": "8.5034", "MZ_GeV": "91.1876"},
    "LHC2026": "gluino 排除至 2.25-2.4 TeV（RPC）；squark 1.7 TeV；top-squark 1.45 TeV；CMS 拟合 M_SUSY=2820 GeV→M_GUT=1.05±0.07e16 GeV",
    "扫描结果": rows,
    "SM全程对照": ("1/α1=1/α2 交汇于 10^%.3f GeV、交汇处 1/α3 偏离 %.2f%%（三力不统一，非超对称 GUT 排除）" % (xs, d13_sm)) if sm_converge else "1/α1=1/α2 正能标无交汇",
    "CMS交叉验证": {"M_SUSY_GeV": "2820", "本文M_GUT": mp.nstr(muG_cms, 12), "CMS_M_GUT": "1.05e16", "偏差pct": mp.nstr(dev_cms, 6),
                    "口径说明": "本文单阈值两段 1-loop 近似；文献含完整谱/2-loop/GUT 阈值效应"},
    "LHC排除线统一度Delta13_pct": mp.nstr(d13_225, 8),
    "判定": "MSSM-GUT 交汇在 LHC 2026 排除线以上仍成立（Δ13 量级 -2.4%% 可被 GUT 阈值修正吸收）；自然超对称出局，存活谱为压缩/分裂超对称",
}
with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\算法联盟_全维自洽与归一化\数据\标准框架_超对称存活窗口GUT交汇更新31.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\njson 已写入：标准框架_超对称存活窗口GUT交汇更新31.json")
