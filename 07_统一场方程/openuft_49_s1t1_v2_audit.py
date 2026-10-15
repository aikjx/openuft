# -*- coding: utf-8 -*-
"""
openuft#49 阶段1·任务1  v2 二次审计引擎
  A. 量纲审计：(M,L,T) 精确幂向量（Fraction），不用自然单位（自然单位会抹掉 c / hbar 的位置）
  B. 250 位 mpmath 锚点：普朗克频率 vs 宇宙学频率，量级缺口与敏感度
  C. Frenet-Darboux 恒等式机器验证 + 类光曲线退化检验
  D. Clifford 规范群嵌入不可行判定（秩论证 + 表示分解穷举）
输出：JSON / TXT 报告，并把自身归档到目标目录。
"""
import os, json, shutil, sys
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt, log10

mp.dps = 260

ROOT = "D:/a10/aikjx/code/my_lib"
OUTDIR = ROOT + "/openuft/07_" + "\u7edf\u4e00\u573a\u65b9\u7a0b"          # 07_统一场方程
OJSON = OUTDIR + "/openuft_49_s1t1_v2_audit.json"
OTXT = OUTDIR + "/openuft_49_s1t1_v2_report.txt"
OPY = OUTDIR + "/openuft_49_s1t1_v2_audit.py"

RES = {}

def dv(m, l, t):
    return (F(m), F(l), F(t))

def dadd(*vs):
    return tuple(sum(x) for x in zip(*vs))

def dmul(v, n):
    return tuple(x * F(n) for x in v)

HBAR = dv(1, 2, -1)      # M L^2 T^-1
C = dv(0, 1, -1)         # L T^-1
G = dv(-1, 3, -2)        # M^-1 L^3 T^-2
L0 = dv(0, 1, 0)         # 参考长度 l0
OM0 = dv(0, 0, -1)       # 参考角频率 Omega0
MASS = dv(1, 0, 0)
LAM = dv(0, -2, 0)       # 宇宙学常数 / 曲率标量 R
RSC = dv(0, -2, 0)
TOR = dv(0, -1, 0)       # 挠率张量
OMG = dv(0, 0, -1)       # 标量 omega
KAP = dv(0, -1, 0)       # kappa
PSI = dv(0, F(-3, 2), 0) # 旋量场 (L^-3/2)
DX4 = dv(0, 4, 0)        # d^4x  (x^mu 全部取长度量纲)
FF = dv(0, -2, 0)        # 规范场强
TARGET = dv(1, -2, -1)   # [L] : S = int L d^4x , [S] = [hbar]

# ---------------------------------------------------------------- A 量纲审计
def term(name, coeffs, fields, note):
    """coeffs/fields: [(dimvec, power), ...]"""
    tot = dv(0, 0, 0)
    for v, p in coeffs:
        tot = dadd(tot, dmul(v, p))
    for v, p in fields:
        tot = dadd(tot, dmul(v, p))
    ok = (tot == TARGET)
    return dict(项=name, 系数说明=note, 幂向量M_L_T=[str(x) for x in tot],
                目标=[str(x) for x in TARGET], 判定=("PASS" if ok else "FAIL"))

A = []
# --- v2 修正版（SI 完备，c/hbar 显式）---
A.append(term("L1 EC曲率项", [(G, -1), (C, 3)], [(RSC, 1)], "c^3/(16piG) * e * R(Gamma)"))
A.append(term("L2 宇宙学项", [(G, -1), (C, 3)], [(LAM, 1)], "-(c^3/(16piG)) * e * 2Lambda"))
A.append(term("L3 挠率二次型", [(G, -1), (C, 3)], [(TOR, 2)], "(c^3/(16piG)) * e * (a1 T^2 + a2 T'T' + a3 T_a T^a)"))
A.append(term("L4 Holst项", [(G, -1), (C, 3)], [(RSC, 1)], "(c^3/(16piG)) * (1/gamma) * e * eps R"))
A.append(term("L5 Nieh-Yan项", [(HBAR, 1), (L0, -2)], [(TOR, 2)], "(hbar/l0^2) * theta * e * (T^T - R^e^e)"))
A.append(term("L6 omega动能", [(HBAR, 1), (C, -2)], [(OMG, 2), (dv(0, -1, 0), 2)], "-(1/2) Z (hbar/c^2) e (grad omega)^2"))
A.append(term("L7 omega势能", [(HBAR, 1), (C, -2), (L0, -2), (OM0, 2)], [], "(hbar Omega0^2/(c^2 l0^2)) * U(omega/Omega0)"))
A.append(term("L8a 约束项 kappa^2 分支", [(HBAR, 1), (L0, -2)], [(KAP, 2)], "- e * lambda * kappa^2 ,  lambda=(hbar/l0^2) * lambdahat"))
A.append(term("L8b 约束项 tau^2 分支", [(HBAR, 1), (L0, -2)], [(TOR, 2)], "- e * lambda * tau^2"))
A.append(term("L8c 约束项 omega^2/c^2 分支", [(HBAR, 1), (L0, -2), (OMG, 2), (C, -2)], [], "+ e * lambda * omega^2/c^2"))
A.append(term("L9 Dirac动能", [(HBAR, 1)], [(PSI, 2), (dv(0, -1, 0), 1)], "(i hbar/2)[psibar gamma^a D_a psi - h.c.]"))
A.append(term("L10 Dirac质量", [(MASS, 1), (C, 1)], [(PSI, 2)], "- m c psibar psi"))
A.append(term("L11 规范场强项", [(HBAR, 1)], [(FF, 2)], "-(hbar/4) F^a_mn F^a^mn"))
# --- v1 原稿（自然单位写法）在 (M,L,T) 下的复核 ---
A.append(term("[v1] EC曲率项 (1/16piG)R", [(G, -1)], [(RSC, 1)], "v1 原稿：缺 c^3"))
A.append(term("[v1] 乘子项 (lambdatilde/16piG)(kappa^2+...)", [(G, -1)], [(KAP, 2)], "v1 原稿：乘子系数沿用 1/G"))
RES["A_量纲审计"] = A

# P-H3 双侧
lhs = dadd(dmul(KAP, 2))
rhs = dadd(dmul(OMG, 2), dmul(C, -2))
RES["A_PH3双侧"] = dict(
    左侧_kappa2_tau2=[str(x) for x in lhs],
    右侧_omega2_over_c2=[str(x) for x in rhs],
    判定=("PASS" if lhs == rhs else "FAIL"))

# ---------------------------------------------------------------- B 250位锚点
hbar = mpf("1.054571817e-34")
GG = mpf("6.67430e-11")
cc = mpf("299792458")
MPC = mpf("3.0856775814913673e22")

lP = sqrt(hbar * GG / cc ** 3)
tP = sqrt(hbar * GG / cc ** 5)
wP = 1 / tP

H0 = mpf("67.4") * 1000 / MPC
OL = mpf("0.685")
Lam = 3 * H0 ** 2 * OL / cc ** 2
Rvac = 4 * Lam
wLam = cc * sqrt(Rvac)          # kappa^2 = |R| = 4Lambda  ->  omega = c*sqrt(R)

ratio = wP / wLam
dex = log10(ratio)
kapP2 = 1 / lP ** 2             # (omega_P/c)^2
dex_curv = log10(kapP2 / Rvac)  # 若 omega=omega_P 则真空曲率 vs 4Lambda 的缺口

# 敏感度扫描（H0 +-0.5, Omega_L +-0.007, G 相对不确定度 2.2e-5）
sc = []
for dh in (mpf("-0.5"), mpf("0"), mpf("0.5")):
    for do in (mpf("-0.007"), mpf("0"), mpf("0.007")):
        for dg in (mpf("1") - mpf("2.2e-5"), mpf("1"), mpf("1") + mpf("2.2e-5")):
            h = (mpf("67.4") + dh) * 1000 / MPC
            o = OL + do
            g = GG * dg
            lam = 3 * h ** 2 * o / cc ** 2
            wp = 1 / sqrt(hbar * g / cc ** 5)
            sc.append(log10(wp / (cc * sqrt(4 * lam))))
dmin, dmax = min(sc), max(sc)

RES["B_250位锚点"] = dict(
    ell_P_m=mp.nstr(lP, 8), t_P_s=mp.nstr(tP, 8),
    **{"omega_P_[s^-1]": mp.nstr(wP, 8)},
    **{"H0_[s^-1]": mp.nstr(H0, 8)}, **{"Lambda_[m^-2]": mp.nstr(Lam, 8)},
    **{"R_vac_4Lambda_[m^-2]": mp.nstr(Rvac, 8)},
    **{"omega_Lambda_[s^-1]": mp.nstr(wLam, 8)},
    omega_Lambda_over_H0=mp.nstr(wLam / H0, 12),
    代数自检_2sqrt3OmegaL=mp.nstr(2 * sqrt(3 * OL), 12),
    dex_gap_omegaP_over_omegaLambda=mp.nstr(dex, 12),
    dex_gap_灵敏度区间=[mp.nstr(dmin, 10), mp.nstr(dmax, 10)],
    dex_gap_若取omegaP则真空曲率对4Lambda=mp.nstr(dex_curv, 12),
    伪精度警告="G 相对不确定度 2.2e-5（约 5 位有效数字）；250 位仅为中间精度，对外声明不得超过 6 位")

# ---------------------------------------------------------------- C Frenet-Darboux
def darboux(a, b, t):
    a = mpf(a); b = mpf(b); t = mpf(t)
    w = sqrt(a * a + b * b)
    T = [(-a * mp.sin(t)) / w, (a * mp.cos(t)) / w, b / w]
    N = [-mp.cos(t), -mp.sin(t), mpf(0)]
    B = [(b * mp.sin(t)) / w, (-b * mp.cos(t)) / w, a / w]
    kap = a / (a * a + b * b)
    tau = b / (a * a + b * b)
    Om = [tau * T[i] + kap * B[i] for i in range(3)]
    def cross(u, v):
        return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    dT = [(-a * mp.cos(t)) / (w * w), (-a * mp.sin(t)) / (w * w), mpf(0)]
    dN = [mp.sin(t) / w, -mp.cos(t) / w, mpf(0)]
    dB = [(b * mp.cos(t)) / (w * w), (b * mp.sin(t)) / (w * w), mpf(0)]
    r1 = max(abs(cross(Om, T)[i] - dT[i]) for i in range(3))
    r2 = max(abs(cross(Om, N)[i] - dN[i]) for i in range(3))
    r3 = max(abs(cross(Om, B)[i] - dB[i]) for i in range(3))
    mag = sqrt(sum(x * x for x in Om))
    clos = abs(mag - sqrt(kap * kap + tau * tau))
    return dict(残差_dT=mp.nstr(r1, 5), 残差_dN=mp.nstr(r2, 5), 残差_dB=mp.nstr(r3, 5),
                **{"|Omega|": mp.nstr(mag, 25), "sqrt(kappa^2+tau^2)": mp.nstr(sqrt(kap * kap + tau * tau), 25)},
                恒等式残差=mp.nstr(clos, 5),
                判定=("PASS" if (r1 < mpf("1e-200") and r2 < mpf("1e-200")
                                and r3 < mpf("1e-200") and clos < mpf("1e-200")) else "FAIL"))

C1 = [darboux(3, 4, "0.7"), darboux(mpf("1.23456789"), mpf("0.98765432"), "2.3")]
# 类光曲线退化：r(l) = (l, sin l, 1-cos l, 0)，Minkowski (-,+,+,+)
nl = []
for lam in ("0.3", "1.1", "2.7"):
    l = mpf(lam)
    v = [mpf(1), mp.cos(l), mp.sin(l), mpf(0)]
    norm2 = -v[0] ** 2 + v[1] ** 2 + v[2] ** 2 + v[3] ** 2
    nl.append(dict(lambda_=lam, eta_vdotv=mp.nstr(norm2, 20),
                   弧长元=mp.nstr(sqrt(abs(norm2)), 20)))
RES["C_FrenetDarboux"] = dict(
    螺旋线验证=C1,
    类光曲线退化=nl,
    结论=("Darboux 恒等式 |Omega|^2=kappa^2+tau^2 对非类光曲线严格成立（机器残差 < 1e-200）；"
          "类光曲线弧长元恒为 0，Frenet 标架（单位切矢 + 弧长导数）不存在，恒等式推导前提失效"))

# ---------------------------------------------------------------- D Clifford 嵌入
def a2_dims(bound):
    out = set()
    for p in range(0, 12):
        for q in range(0, 12):
            d = (p + 1) * (q + 1) * (p + q + 2) // 2
            if d <= bound:
                out.add(d)
    return sorted(out)

def embed_possible(N):
    d3 = a2_dims(N)
    d2 = [d for d in range(1, N + 1)]
    sols = []
    def rec(rem, chosen):
        if rem == 0:
            has3 = any(x[0] > 1 for x in chosen)
            has2 = any(x[1] > 1 for x in chosen)
            if has3 and has2:
                sols.append(list(chosen))
            return
        for a in d3:
            for b in d2:
                if a * b <= rem and (not chosen or (a, b) >= chosen[-1]):
                    rec(rem - a * b, chosen + [(a, b)])
    rec(N, [])
    return sols

n1 = embed_possible(4)
n2 = embed_possible(8)
RES["D_Clifford嵌入"] = dict(
    环境代数="Cl(1,3)_C ~ Mat(4,C)；Aut(Cl(1,3)) 的李代数 = su*(4)（sl(4,C) 的实形式）",
    rank_sl4C=3, rank_su3_su2_u1=4,
    秩判定=("FAIL：秩 4 > 秩 3，紧子代数无法嵌入（Cartan 子代数维数上界论证）"),
    dim_sl4C=15, dim_sm_algebra=12,
    表示分解_单代4维解个数=len(n1), 单代解=n1,
    表示分解_双份8维解个数=len(n2), 双份解样例=(n2[:3] if n2 else []),
    结论=("单代 Dirac（C^4）口径下 su(3)+su(2)+u(1) 无嵌入：秩论证与表示穷举双重否决；"
          "允许 >=2 份副本（C^4 (x) C^n, n>=2）时表示论上不再被否决，但所得是横向/代空间对称性，"
          "不等于定域规范对称，需作为 P-H4-prime 重新提交"))

# ---------------------------------------------------------------- 汇总
nA = len(A); nApass = sum(1 for x in A if x["判定"] == "PASS")
RES["汇总"] = dict(
    量纲审计项数=nA, 量纲PASS=nApass,
    v1原稿两项在MLT下=[x["判定"] for x in A if x["项"].startswith("[v1]")],
    总判定="阶段1-任务1 交付 v2：量纲关在 (M,L,T) 精确口径下通过；P-H3 数值锚点关 FAIL；P-H4 代数关 FAIL；M5 旋量门槛自身错误")

os.makedirs(OUTDIR, exist_ok=True)
with open(OJSON, "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1)

lines = []
lines.append("openuft#49 阶段1任务1 v2 审计报告")
lines.append("=" * 60)
for k, v in RES.items():
    lines.append("")
    lines.append("### " + k)
    lines.append(json.dumps(v, ensure_ascii=False, indent=1))
with open(OTXT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

try:
    shutil.copy(__file__, OPY)
except Exception as e:
    print("copy fail", e)

print("WROTE:", OJSON)
print("WROTE:", OTXT)
print("dex_gap =", mp.nstr(dex, 10), " range", mp.nstr(dmin, 8), mp.nstr(dmax, 8))
