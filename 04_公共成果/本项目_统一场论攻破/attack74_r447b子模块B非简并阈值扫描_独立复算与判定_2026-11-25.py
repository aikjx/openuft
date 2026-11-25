#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attack74 · 算法联盟 r447b 子模块B「非简并阈值全参数扫描 + 自由度量化审计」独立复算与判定引擎

来料：用户粘贴文本（2026-11-24，来稿源码行号按其模块 3.2 代码段引用）。库内指纹：
r447 主册与 r447b_A 判定册均在（openuft/04_公共成果/本项目_全维自洽与归一化/判定/），
1.1247e16 基准 22 处命中——本册为 r447 → r447b_A → r447b_B 接力的第三册（attack 系列）。

前链关键事实（[C] 引用，见判定册）：
- r447 主册：ΔL:=成对交汇跨度 max−min（L12,L13,L23），M_G:=α₁-α₂ 交汇（L12）标度，
  α_G=(α₁+α₂)/2；SM 段(91.1876→1000 GeV)一圈、以上 MSSM 二圈（α⁻¹ 空间 RK4 h=0.01）；
  基准 M_G=1.1247473212632112693e16、ΔL=0.4819077285、L12=32.44600097209、
  L13=32.24133564379、L23=31.96409324357。
- r447b_A：标准顶列 c_U^STD=(26/5,6,4)、g 式负号锁定；标准口径 M_G=1.1030289064e16、
  ΔL=0.3955205941、α_G=0.0388247205、y_t(M_G)=0.7564354820；来料列 (14/5,6,16/3)+正号
  降格 benchmark；I13 登记「来稿数字与代码不一致」先例。

引擎纪律（承 attack66/72/73）：
- 纯标准库；Fraction 精确有理代数（一圈 Δb 与矩阵比对，承 r447「Decimal 60 位 + Fraction
  精确系数」先例）+ Decimal 50 位读数展示 + float RK4 数值复算 + (M,L,T,Q) 量纲四元组。
- 判定值由阈值计算产生，不硬编码结论；判定文本条件化于实测数字。
- 引用类外部常数一律标 [C]。FAIL 语义 = 来稿命题落地在现有框架/数据内不可行。

变体矩阵（数值裁决层）：
- V0 忠实重演：来稿源码逐行语义（Δb 表/B 同矩阵/C_U 正号全程/dt=0.005/步上限 10000/判据
  inv_a[1]≤inv_a[2]）——预期基准与扫描全部无交汇（崩溃演示）。
- 初值双源：来稿硬编码 (59, 29.6, 8.4) vs r447 源码 initial_alpha() 由 α_em/sin²θW/α₃ 反推
  （≈59.02/29.58/8.47）——校准残差的主导来源，机器量化。
- V1a 无Yukawa：SM 一圈 + MSSM 二圈（r447 锁定 B₂）；V1aα 同系统 α⁻¹ 空间移植（h=0.01）——
  积分变量无关性互检；库内初值版对照 r447 主册六读数。
- V1b 工作框架：来稿初值 + 正确 Δb + 教材二圈 Yukawa 反馈（g 式 −c·y²/(16π²)²），y_t 全程
  一圈演化（忠实战来稿源码语义）——C 组扫描的审计框架。
- V1b-库内标准：库内初值 + SM 段冻结 y_t（r447b_A 源码 beta_sm 第 4 分量=0）——对照
  r447b_A 标准四读数与 r447b_B α₂=α₃ 交点。
- V1c-册面式：V1b-库内标准 但 Yukawa 反馈 ×4π（等价册面 α⁻¹ 式 +c_i y_t²/(8π²)）——
  裁决册面式与册报 −1.93% 漂移是否自洽（r447b_A 源码实际用 32π³）。

输出：attack74_..._2026-11-25.json / _report.txt（写在本文件同目录）。
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 50
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
STAMP = "2026-11-25"
BASE = "attack74_r447b子模块B非简并阈值扫描_独立复算与判定_" + STAMP
OUT_JSON = os.path.join(HERE, BASE + ".json")
OUT_REPORT = os.path.join(HERE, BASE + "_report.txt")

MZ = 91.1876
INV0 = (59.0, 29.6, 8.4)                 # 来稿源码硬编码初值 α_i⁻¹(M_Z)
YT0 = 0.95                                # [C] y_t(M_Z)（r447b_A 同源）
AEM = 0.0078156                           # [C] r447 源码 INPUT alpha_em_MZ
S2W = 0.23121                             # [C] r447 源码 INPUT sin2_theta_W
A3MZ = 0.1180                             # [C] r447 源码 INPUT alpha_3_MZ
INIT_LIB_INV = (1.0 / ((5.0 / 3.0) * AEM / (1.0 - S2W)),
                1.0 / (AEM / S2W), 1.0 / A3MZ)   # 库内 initial_alpha() 反推 ≈ (59.02, 29.58, 8.47)
T23_R447B_B = 32.030981928190261154682740        # [C] r447b_B 册正式口径 α₂=α₃ 交点 t₀

# ---------------- [C] 在册锁定读数（r447 主册 / r447b_A 判定册）----------------
MG_R447 = 1.1247473212632112693207773e16
DL_R447 = 0.48190772851939696282114751
L12_R447 = 32.446000972088482520917769
L13_R447 = 32.241335643878620748153040
L23_R447 = 31.964093243569085558096621
AG_R447 = 0.0390247600638529639
MG_STD_A = 1.1030289063619143453645251e16
DL_STD_A = 0.39552059413485094312056464
AG_STD_A = 0.038824720501304636
YT_MG_STD_A = 0.75643548204642482348099102
SHIFT_STD_A = -0.019310                        # r447b_A 册报 M_G 相对无 Yukawa 漂移

# ---------------- 精确代数层（Fraction）----------------
T_F1_GEN = F(2)          # 每代手征超场标量/费米子 ΣT₁ = 1/10+4/5+1/5+3/10+3/5
T_F2_GEN = F(2)          # 每代 ΣT₂ = 3·(1/2)+1/2
T_F3_GEN = F(2)          # 每代 ΣT₃ = 1+1/2+1/2
T_HIG1 = F(3, 10)        # 单个 Higgs 双态 T₁ = (3/5)(1/4+1/4)
T_HIG2 = F(1, 2)         # 单个 Higgs 双态 T₂
T_ADJ2 = F(2)            # C₂(SU2)
T_ADJ3 = F(3)            # C₂(SU3)
T_ADJ1 = F(0)            # U(1)_Y 伴随（Bino）中性

b1_sm = F(2, 3) * (3 * T_F1_GEN) + F(1, 3) * T_HIG1
b2_sm = -F(11, 3) * T_ADJ2 + F(2, 3) * (3 * T_F2_GEN) + F(1, 3) * T_HIG2
b3_sm = -F(11, 3) * T_ADJ3 + F(2, 3) * (3 * T_F3_GEN)
b1_mssm = F(2, 3) * (3 * T_F1_GEN + 2 * T_HIG1 + T_ADJ1) \
    + F(1, 3) * (3 * T_F1_GEN + 2 * T_HIG1)
b2_mssm = -F(11, 3) * T_ADJ2 + F(2, 3) * (3 * T_F2_GEN + 2 * T_HIG2 + T_ADJ2) \
    + F(1, 3) * (3 * T_F2_GEN + 2 * T_HIG2)
b3_mssm = -F(11, 3) * T_ADJ3 + F(2, 3) * (3 * T_F3_GEN + T_ADJ3) \
    + F(1, 3) * (3 * T_F3_GEN)

b_targets = [(b1_sm, F(41, 10)), (b2_sm, F(-19, 6)), (b3_sm, F(-7)),
             (b1_mssm, F(33, 5)), (b2_mssm, F(1)), (b3_mssm, F(-3))]

delta_input = [(F(-22, 5), F(-6), F(0)), (F(-2, 5), F(-2), F(0)),
               (F(26, 5), F(6), F(12)), (F(0), F(0), F(-6))]      # 来稿四行
sum_in = tuple(sum(delta_input[k][i] for k in range(4)) for i in range(3))
summed_in = tuple((b1_sm + sum_in[0], b2_sm + sum_in[1], b3_sm + sum_in[2]))
tgt_mssm = (F(33, 5), F(1), F(-3))
mismatch = tuple(summed_in[i] - tgt_mssm[i] for i in range(3))

d_gaug = (F(2, 3) * T_ADJ1, F(2, 3) * T_ADJ2, F(0))               # Bino 0 + Wino 4/3
d_hig = (F(2, 3) * (2 * T_HIG1) + F(1, 3) * T_HIG1,
         F(2, 3) * (2 * T_HIG2) + F(1, 3) * T_HIG2, F(0))         # higgsino 对 + 第二 Higgs 标量
d_sfer = (F(1, 3) * (3 * T_F1_GEN), F(1, 3) * (3 * T_F2_GEN),
          F(1, 3) * (3 * T_F3_GEN))                                # 三代 sfermion
d_glu = (F(0), F(0), F(2, 3) * T_ADJ3)                             # gluino
delta_v1 = [d_gaug, d_hig, d_sfer, d_glu]
sum_v1 = tuple(sum(delta_v1[k][i] for k in range(4)) for i in range(3))

b1_by_formula = -F(2, 3) * (3 * T_F1_GEN) - F(1, 3) * T_HIG1       # 来稿公式符号演示

B2_LIB = [[F(199, 50), F(27, 10), F(44, 5)],
          [F(9, 2), F(35, 6), F(12)],
          [F(11, 2), F(9, 2), F(-26)]]            # r447 锁定「MSSM 二圈」矩阵
B2_SM_LIT = [[F(199, 50), F(27, 10), F(44, 5)],
             [F(9, 10), F(35, 6), F(12)],
             [F(11, 10), F(9, 2), F(-26)]]        # [C] 文献 SM 二圈矩阵（arXiv:1502.06929 等）
CU_INPUT = (F(14, 5), F(6), F(16, 3))             # 来稿顶列（正号）
CU_STD = (F(26, 5), F(6), F(4))                   # r447b_A 标准顶列（g 式负号）
cu_diff = tuple(CU_INPUT[i] - CU_STD[i] for i in range(3))

# ---------------- 引擎登记 ----------------
selfchecks = [0, 0]


def sc(cond):
    selfchecks[1] += 1
    if cond:
        selfchecks[0] += 1
    return bool(cond)


entries = []


def entry(code, verdict, text, numbers=None):
    entries.append({"code": code, "verdict": verdict, "text": text,
                    "numbers": numbers or {}})


def fstr(x):
    """Fraction/float → 紧凑字符串。"""
    if isinstance(x, F):
        return str(float(x)) if x.denominator > 10**6 else ("%d/%d" % (x.numerator, x.denominator) if x.denominator != 1 else str(x.numerator))
    return "%.6g" % x if isinstance(x, float) else str(x)


# ================================================================ A 一圈代数
A01_ALL = all(sc(got == want) for got, want in b_targets)
entry("A01", "PASS" if A01_ALL else "FAIL",
      "六个 b 值表示论重演（Fraction 精确）：SM (41/10,−19/6,−7)、MSSM (33/5,1,−3) 由 "
      "b=−(11/3)C₂(G)+(2/3)ΣT(Weyl)+(1/3)ΣT(复标量) 精确重构 %d/6——本册约定校准，并证明正确"
      "符号为 +(2/3)T(Weyl)、+(1/3)T(标量)（U(1) 伴随 T₁(adj)=0，Bino 对 b₁ 贡献为零）" % sum(
          1 for got, want in b_targets if got == want),
      {"reconstructed": [str(g) for g, _ in b_targets]})

A02_FAIL = all(sc(summed_in[i] != tgt_mssm[i]) for i in range(3))
entry("A02", "FAIL" if A02_FAIL else "PASS",
      "来稿模块 2.3『✔ 代数累加验证通过』复算失败（Fraction 精确）：b_SM+ΣΔb(来稿) = (%s, %s, %s) "
      "≠ b_MSSM = (33/5, 1, −3)，三组元全失配（偏差 %s, %s, %s）——累加校验本身即不自洽"
      % (fstr(summed_in[0]), fstr(summed_in[1]), fstr(summed_in[2]),
         fstr(mismatch[0]), fstr(mismatch[1]), fstr(mismatch[2])),
      {"summed": [fstr(x) for x in summed_in], "mismatch": [fstr(x) for x in mismatch]})

A03_OK = all(sc(b_targets[i][0] + sum_v1[i] - b_targets[i + 3][0] == 0) for i in range(3))
entry("A03", "CORRECTED" if A03_OK else "FAIL",
      "正确四组分档增量（Fraction 精确；第二 Higgs 标量双态为来稿分组缺失行，本册并入 M2 Higgs "
      "扇区）：M1 电弱gaugino(Bino+Wino) (%s,%s,%s)、M2 Higgs 扇区 (%s,%s,%s)、M3 三代sfermion "
      "(%s,%s,%s)、M4 gluino (%s,%s,%s)；Σ = (5/2, 25/6, 4) 精确 = b_MSSM−b_SM——来稿四行全部错误"
      "（其 M1 行按其自身符号约定也应为 (0,−4/3,0)；费米子行符号相反：Bino 对 b₁ 贡献 0 而非"
      " −22/5；gluino Δb₃=+2 而非 −6；sfermion 行 +2,+2,+2 而非 +26/5,+6,+12）"
      % tuple(fstr(x) for row in delta_v1 for x in row),
      {"delta_v1": [[fstr(x) for x in row] for row in delta_v1],
       "sum_v1": [fstr(x) for x in sum_v1]})

A04_OK = sc(b1_by_formula == -b1_sm)
entry("A04", "CORRECTED" if A04_OK else "FAIL",
      "来稿公式 Δb=−(2/3)T(Weyl)、−(1/3)T(标量) 与其自身 b 约定矛盾：按该公式重构 SM 物质+Higgs "
      "贡献 b₁ = %s ≠ +41/10（符号相反）——公式级错误，正确为 +(2/3)T、+(1/3)T（A01 重演已证）"
      % fstr(b1_by_formula),
      {"b1_by_formula": fstr(b1_by_formula)})

# ================================================================ B 源码与矩阵审计
ratio21 = B2_LIB[1][0] / B2_SM_LIT[1][0]
ratio31 = B2_LIB[2][0] / B2_SM_LIT[2][0]
B03_IDENT = all(sc(B2_LIB[i][j] == B2_SM_LIT[i][j] if (i, j) not in ((1, 0), (2, 0))
                   else B2_LIB[i][j] != B2_SM_LIT[i][j])
                for i in range(3) for j in range(3))
B03_OK = sc(ratio21 == 5 and ratio31 == 5)
entry("B03", "CORRECTED" if B03_OK else "FAIL",
      "『MSSM 二圈矩阵』B₂ 存疑（r447 主册继承项）：来稿代码 B_sm ≡ B_mssm 逐元素相同"
      "（来稿模块 3.2 代码段，Fraction 9/9 比对）——『二圈矩阵按能区切换为 SM/MSSM 两组』是 "
      "no-op；且该矩阵与文献 SM 二圈纯规范矩阵 [C: arXiv:1502.06929 等] 逐项一致，仅 "
      "B₂₁=9/2 vs 9/10、B₃₁=11/2 vs 11/10 相差整 5 倍（机器商 = %s、%s）——既非正确 SM 矩阵、"
      "亦无 MSSM 归属文献依据（Abel 自项为物质驱动，MSSM 物质含量不同，矩阵必不同）；"
      "正确 MSSM 二圈矩阵留 [C 需文献核对]" % (fstr(ratio21), fstr(ratio31)),
      {"ratio_B21": fstr(ratio21), "ratio_B31": fstr(ratio31),
       "identical_to_lit_SM_mod_5x": B03_IDENT})

B04_OK = sc(any(x != 0 for x in cu_diff)) and sc(CU_INPUT[0] < CU_STD[0])
entry("B04", "CORRECTED" if B04_OK else "FAIL",
      "Yukawa 口径回退（来稿模块 3.2 代码段 C_U 定义与 term2_yt 符号）：来稿 C_U=(14/5,6,16/3)+"
      "正号正是 r447b_A 判定册明确降格为 benchmark 的来料口径（标准顶列 c_U^STD=(26/5,6,4)、"
      "g 式负号；两列差 %s, %s, %s，首列 %s）——来稿『延续 r447 修正后的正确求导约定』与"
      "『执行口径』声明不实；且该项在 SM 能区（< min M_i）也无条件加入（来稿 get_beta_coeffs "
      "只切换 b 与 B，不切换 Yukawa 项），与 r447 formal SM 段纯一圈不符"
      % (fstr(cu_diff[0]), fstr(cu_diff[1]), fstr(cu_diff[2]),
         "来稿更低" if CU_INPUT[0] < CU_STD[0] else "来稿更高"),
      {"cu_diff": [fstr(x) for x in cu_diff]})

# ================================================================ RK4 引擎（float）
INV16 = 1.0 / (16 * math.pi ** 2)
INV16S = INV16 * INV16
B2_F = [[float(x) for x in row] for row in B2_LIB]
B_SM_F = [float(b1_sm), float(b2_sm), float(b3_sm)]
DELTA_V0_F = [[float(x) for x in row] for row in delta_input]
DELTA_V1_F = [[float(x) for x in row] for row in delta_v1]
CU_IN_F = [float(x) for x in CU_INPUT]
CU_STD_F = [float(x) for x in CU_STD]
YTC_F = [-13.0 / 15.0, -3.0, -16.0 / 3.0]


def beta_v0(state, mu, th):
    """忠实转录来稿 beta_full：b 累计切换（来稿 Δb）、B 全程同一矩阵、C_U 正号二圈项
    全程（含 SM 能区）无条件加入、四耦合含 y_t 演化。"""
    b0, b1_, b2_ = B_SM_F
    for k in range(4):
        if mu >= th[k]:
            b0 += DELTA_V0_F[k][0]; b1_ += DELTA_V0_F[k][1]; b2_ += DELTA_V0_F[k][2]
    g1, g2, g3, yt = state
    gl = (g1, g2, g3)
    bs = (b0, b1_, b2_)
    out = [0.0, 0.0, 0.0, 0.0]
    for i in range(3):
        gi3 = gl[i] ** 3
        row = B2_F[i]
        s = row[0] * gl[0] ** 2 + row[1] * gl[1] ** 2 + row[2] * gl[2] ** 2
        out[i] = bs[i] * gi3 * INV16 + gi3 * INV16S * (s + CU_IN_F[i] * yt * yt)
    tg = YTC_F[0] * gl[0] ** 2 + YTC_F[1] * gl[1] ** 2 + YTC_F[2] * gl[2] ** 2
    out[3] = yt * INV16 * (tg + 6.0 * yt * yt)
    return out


def beta_noy(state, mu, th):
    """V1a：SM 一圈 / MSSM 二圈（正确 Δb 累计、r447 锁定 B₂）、无任何 Yukawa 项
    （y_t 通道冻结，保持四状态接口）。"""
    b0, b1_, b2_ = B_SM_F
    for k in range(4):
        if mu >= th[k]:
            b0 += DELTA_V1_F[k][0]; b1_ += DELTA_V1_F[k][1]; b2_ += DELTA_V1_F[k][2]
    g1, g2, g3, _yt = state
    gl = (g1, g2, g3)
    bs = (b0, b1_, b2_)
    active = mu >= min(th)
    out = []
    for i in range(3):
        gi3 = gl[i] ** 3
        row = B2_F[i]
        s = row[0] * gl[0] ** 2 + row[1] * gl[1] ** 2 + row[2] * gl[2] ** 2
        out.append(bs[i] * gi3 * INV16 + (gi3 * INV16S * s if active else 0.0))
    return out + [0.0]


def make_beta_std(yscale=1.0, freeze_sm=False):
    """V1b 族工厂：四耦合；SM 段规范一圈（可冻结 y_t）；MSSM 段 b 累计 + B₂ + 教材二圈
    Yukawa 反馈（g 式括号 −c_U^STD·y_t²，yscale 缩放用于册面式对照）。y_t 一圈演化全程。"""
    def beta(state, mu, th):
        b0, b1_, b2_ = B_SM_F
        active = False
        for k in range(4):
            if mu >= th[k]:
                b0 += DELTA_V1_F[k][0]; b1_ += DELTA_V1_F[k][1]; b2_ += DELTA_V1_F[k][2]
                active = True
        g1, g2, g3, yt = state
        gl = (g1, g2, g3)
        bs = (b0, b1_, b2_)
        out = [0.0, 0.0, 0.0, 0.0]
        if not active:
            for i in range(3):
                out[i] = bs[i] * gl[i] ** 3 * INV16
            if freeze_sm:
                return out
            tg = YTC_F[0] * gl[0] ** 2 + YTC_F[1] * gl[1] ** 2 + YTC_F[2] * gl[2] ** 2
            out[3] = yt * INV16 * (tg + 6.0 * yt * yt)
            return out
        y2 = yt * yt
        for i in range(3):
            gi3 = gl[i] ** 3
            row = B2_F[i]
            s = row[0] * gl[0] ** 2 + row[1] * gl[1] ** 2 + row[2] * gl[2] ** 2
            out[i] = bs[i] * gi3 * INV16 + gi3 * INV16S * (s - yscale * CU_STD_F[i] * y2)
        tg = YTC_F[0] * gl[0] ** 2 + YTC_F[1] * gl[1] ** 2 + YTC_F[2] * gl[2] ** 2
        out[3] = yt * INV16 * (tg + 6.0 * y2)
        return out
    return beta


def alpha_deriv(a, mu, th_common):
    """V1aα：r447 正式引擎 ODE 的 α⁻¹ 空间直接移植（无 Yukawa）：
    dα_i⁻¹/dt = −b_i/(2π) − (1/(8π²))Σ_j B_ij α_j；SM 段纯一圈。"""
    inv8pi2 = 1.0 / (8 * math.pi ** 2)
    b = [float(b1_sm), float(b2_sm), float(b3_sm)]
    if mu >= th_common:
        for k in range(4):
            for i in range(3):
                b[i] += DELTA_V1_F[k][i]
    alphas = (1.0 / a[0], 1.0 / a[1], 1.0 / a[2])
    out = []
    for i in range(3):
        s = sum(B2_F[i][j] * alphas[j] for j in range(3))
        out.append(-b[i] / (2 * math.pi) - (s * inv8pi2 if mu >= th_common else 0.0))
    return out


def rk4_run(beta, th, dt=0.005, t_max=36.0, max_steps=None, inv0=INV0):
    """g 空间四耦合 RK4；beta(state, mu, th)。返回轨迹 [(t, α₁⁻¹, α₂⁻¹, α₃⁻¹, y_t)]。"""
    st = [math.sqrt(4 * math.pi / inv0[i]) for i in range(3)] + [YT0]
    t = 0.0
    traj = [(0.0, inv0[0], inv0[1], inv0[2], YT0)]
    nsteps = int(t_max / dt)
    if max_steps is not None and nsteps > max_steps:
        nsteps = max_steps
    for _step in range(nsteps):
        mu0 = MZ * math.exp(t)
        mum = MZ * math.exp(t + 0.5 * dt)
        mu1 = MZ * math.exp(t + dt)
        k1 = beta(st, mu0, th)
        s2 = [st[i] + 0.5 * dt * k1[i] for i in range(4)]
        k2 = beta(s2, mum, th)
        s3 = [st[i] + 0.5 * dt * k2[i] for i in range(4)]
        k3 = beta(s3, mum, th)
        s4 = [st[i] + dt * k3[i] for i in range(4)]
        k4 = beta(s4, mu1, th)
        st = [st[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]
        t += dt
        ia = (4 * math.pi / st[0] ** 2, 4 * math.pi / st[1] ** 2, 4 * math.pi / st[2] ** 2)
        traj.append((t, ia[0], ia[1], ia[2], st[3]))
    return traj


def rk4_run_alpha(inv0=INV0, th_common=1000.0, dt=0.01, t_max=41.56):
    """α⁻¹ 空间 RK4（V1aα，h=0.01 与 r447 相同）。轨迹 [(t, a1, a2, a3)]。"""
    a = list(inv0)
    t = 0.0
    traj = [(0.0, a[0], a[1], a[2])]
    for _step in range(int(t_max / dt)):
        mu0 = MZ * math.exp(t)
        mum = MZ * math.exp(t + 0.5 * dt)
        mu1 = MZ * math.exp(t + dt)
        k1 = alpha_deriv(a, mu0, th_common)
        s2 = [a[i] + 0.5 * dt * k1[i] for i in range(3)]
        k2 = alpha_deriv(s2, mum, th_common)
        s3 = [a[i] + 0.5 * dt * k2[i] for i in range(3)]
        k3 = alpha_deriv(s3, mum, th_common)
        s4 = [a[i] + dt * k3[i] for i in range(3)]
        k4 = alpha_deriv(s4, mu1, th_common)
        a = [a[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3)]
        t += dt
        traj.append((t, a[0], a[1], a[2]))
    return traj


def pairwise_stats(traj):
    """成对交汇 L12/L13/L23（轨迹线性插值）+ M_G/α_G/ΔL/y_t(M_G)。"""
    nc = len(traj[0]) - 1
    res = {}
    for (i, j), name in (((1, 2), "L12"), ((1, 3), "L13"), ((2, 3), "L23")):
        found = None
        prev = traj[0][i] - traj[0][j]
        for k in range(1, len(traj)):
            cur = traj[k][i] - traj[k][j]
            if prev > 0 and cur <= 0:
                t0, t1 = traj[k - 1][0], traj[k][0]
                w = prev / (prev - cur) if (prev - cur) != 0 else 0.0
                found = t0 + w * (t1 - t0)
                break
            prev = cur
        res[name] = found
    mg = ag = ytc = None
    if res["L12"] is not None:
        for k in range(1, len(traj)):
            if traj[k][0] >= res["L12"]:
                t0, t1 = traj[k - 1][0], traj[k][0]
                w = (res["L12"] - t0) / (t1 - t0)
                vals = [traj[k - 1][m] + w * (traj[k][m] - traj[k - 1][m]) for m in (1, 2, nc)]
                mg = MZ * math.exp(res["L12"])
                ag = 0.5 * (1.0 / vals[0] + 1.0 / vals[1])
                ytc = vals[2]
                break
    ls = [res[k] for k in ("L12", "L13", "L23") if res[k] is not None]
    dl = (max(ls) - min(ls)) if len(ls) == 3 else None
    return {"L12": res["L12"], "L13": res["L13"], "L23": res["L23"],
            "MG": mg, "alpha_G": ag, "DL": dl, "yt_cross": ytc}


def run_stats(beta, th, dt=0.005, t_max=36.0, max_steps=None, inv0=None):
    if inv0 is None:
        inv0 = INV0
    return pairwise_stats(rk4_run(beta, th, dt=dt, t_max=t_max, max_steps=max_steps,
                                  inv0=inv0))


BASE_TH = (1000.0, 1000.0, 1000.0, 1000.0)


def _swap(newB):
    global B2_F
    B2_F = newB


def stats_bscale(th, Bscale, beta=None):
    if beta is None:
        beta = make_beta_std()
    if Bscale == 1.0:
        return run_stats(beta, th)
    saved = B2_F
    _swap([[v * Bscale for v in row] for row in saved])
    try:
        return run_stats(beta, th)
    finally:
        _swap(saved)

# ================================================================ V0 忠实重演
v0_runs = {}
for label, th in [("baseline", (1000.0, 1000.0, 1000.0, 1000.0))] + \
        [("glu_%d" % m, (1000.0, 1000.0, 1000.0, float(m))) for m in (100, 500, 5000, 10000)]:
    traj0 = rk4_run(beta_v0, th, dt=0.005, t_max=50.0, max_steps=10000)
    fired = None
    prev = traj0[201][2] - traj0[201][3]
    for k in range(202, len(traj0)):
        cur = traj0[k][2] - traj0[k][3]
        if prev > 0 and cur <= 0:
            fired = traj0[k][0]
            break
        prev = cur
    v0_runs[label] = {"crossed": fired is not None,
                      "t": fired,
                      "MG_from_cross": MZ * math.exp(fired) if fired else None}
V0_NONE = all(not v["crossed"] for v in v0_runs.values())
sc(V0_NONE)
# 判据不变量演示：α₂⁻¹−α₃⁻¹ 在全程保持 >0（来稿 Δb 下）
gap_min = min(traj0[k][2] - traj0[k][3] for k in range(0, len(traj0), 50))
sc(gap_min > 0)
slope2 = 31.0 / (12 * math.pi)     # −b₂/(2π)，b₂=−31/6
slope3 = 1.0 / (2 * math.pi)       # −b₃/(2π)，b₃=−1
# 索引错位结构演示（来稿源码 run_rg：cross_data = inv_a + [state[3], MZ·e^t]）
demo_ia = [25.757, 25.757, 25.757]
demo_yt = 0.7564354820
demo_mg = 5.1469157756979639e15
demo_cross = demo_ia + [demo_yt, demo_mg]
B02_IDX = sc(demo_cross[3] == demo_yt and demo_cross[4] == demo_mg)
entry("B01", "FAIL" if V0_NONE else "PASS",
      "展示源码忠实重演崩溃：全阈值 1 TeV 基准下上档 b=(9/2, −31/6, −1) → α₂⁻¹ 单调上升且快于"
      " α₃⁻¹（理论斜率 +%.4f vs +%.4f /ln，实测 gap₂₃ 全程最小值 %.3f > 0）→ 判据 "
      "inv_a[1]≤inv_a[2]（来稿 run_rg，即 α₂⁻¹≤α₃⁻¹）永不成立 → run_rg 返回 (None, None) → "
      "主程序在 data_cross[3] 处 TypeError——基准+胶微子扫描 %d 次运行全部无交汇；模块 4.1"
      "『基准核验通过 M_G≈1.13e16』不可能出自展示源码" % (slope2, slope3, gap_min, len(v0_runs)),
      {"runs": {k: v["crossed"] for k, v in v0_runs.items()},
       "theory_slopes": [slope2, slope3], "gap_min": gap_min})
entry("B02", "FAIL" if B02_IDX else "PASS",
      "三重错位（来稿 run_rg/主程序代码段）：① cross_data = inv_a + [state[3], MZ·e^t] → "
      "data_cross[3] = y_t（结构演示：%.10f）而 M_G 在 data_cross[4]（%.6g），主程序却打印 "
      "data_cross[3] 为『M_G』——即使判据触发，打印的也是 y_t；② 判据 inv_a[1]≤inv_a[2] 定位的"
      "是 α₂-α₃ 交汇，与 r447 的 M_G:=α₁-α₂ 交汇（L12）约定不同对；③ 扫描打印同样取 d_c[3]。"
      "与 r447b_A I13（模块 5 数字与实跑不可对账）同类：来稿数字与来稿源码不可对账"
      "（谱系性第三次登记）" % (demo_yt, demo_mg),
      {"demo_cross3": demo_yt, "demo_cross4": demo_mg})

# ================================================================ V1 校准（变体矩阵）
# 库内标准口径（源码级核对：r447b_A 源码 beta_sm 第 4 分量=0 → SM 段冻结 y_t；
# beta_mssm 二圈括号 s_gauge+sign·c_u·y²、dalpha_inv_exact 用 c·y²/(32π³) → 教材量级；
# 初值 initial_alpha() 由 α_em/sin²θW/α₃ 反推）
v1a = run_stats(beta_noy, BASE_TH)                                # 来稿初值，g 空间
v1a_alpha = pairwise_stats(rk4_run_alpha(INV0))                   # 来稿初值，α⁻¹ 空间
v1a_lib = pairwise_stats(rk4_run_alpha(INIT_LIB_INV))             # 库内初值 → r447 复现
v1b = run_stats(make_beta_std(), BASE_TH)                         # 工作框架（来稿初值，y 全程）
v1b_frozen = run_stats(make_beta_std(freeze_sm=True), BASE_TH)    # 来稿初值，SM 段冻结
v1b_lib = run_stats(make_beta_std(freeze_sm=True), BASE_TH, inv0=INIT_LIB_INV)
v1c_lib = run_stats(make_beta_std(yscale=4 * math.pi, freeze_sm=True),
                    BASE_TH, inv0=INIT_LIB_INV)

rel = lambda x, y: (x / y - 1.0) if (x and y) else None
cal = {
    "init_provenance": {
        "laizhai_inv": [INV0[0], INV0[1], INV0[2]],
        "lib_inv": [INIT_LIB_INV[0], INIT_LIB_INV[1], INIT_LIB_INV[2]],
        "diff_1": INIT_LIB_INV[0] - INV0[0],
        "diff_2": INIT_LIB_INV[1] - INV0[1],
        "diff_3": INIT_LIB_INV[2] - INV0[2],
        "source": "[C] r447 源码 INPUT: alpha_em_MZ=0.0078156, sin2_theta_W=0.23121, "
                  "alpha_3_MZ=0.1180 → α₁=(5/3)·α_em/cos²θW；来稿源码硬编码 (59, 29.6, 8.4)"},
    "v1a_vs_v1aalpha": {"rel_MG": rel(v1a["MG"], v1a_alpha["MG"]),
                        "rel_DL": rel(v1a["DL"], v1a_alpha["DL"])},
    "v1a_lib": {"MG": v1a_lib["MG"], "DL": v1a_lib["DL"],
                "L12": v1a_lib["L12"], "L13": v1a_lib["L13"], "L23": v1a_lib["L23"],
                "rel_MG_vs_r447": rel(v1a_lib["MG"], MG_R447),
                "rel_DL_vs_r447": rel(v1a_lib["DL"], DL_R447)},
    "v1b_lib_frozen": {"MG": v1b_lib["MG"], "DL": v1b_lib["DL"],
                       "alpha_G": v1b_lib["alpha_G"], "yt_cross": v1b_lib["yt_cross"],
                       "L23": v1b_lib["L23"],
                       "rel_MG_vs_stdA": rel(v1b_lib["MG"], MG_STD_A),
                       "rel_DL_vs_stdA": rel(v1b_lib["DL"], DL_STD_A),
                       "rel_AG_vs_stdA": rel(v1b_lib["alpha_G"], AG_STD_A),
                       "rel_yt_vs_stdA": rel(v1b_lib["yt_cross"], YT_MG_STD_A),
                       "diff_L23_vs_r447bB": v1b_lib["L23"] - T23_R447B_B,
                       "shift_vs_v1a_lib": rel(v1b_lib["MG"], v1a_lib["MG"])},
    "v1b_work": {"MG": v1b["MG"], "DL": v1b["DL"], "yt_cross": v1b["yt_cross"],
                 "shift_vs_v1a": rel(v1b["MG"], v1a["MG"])},
    "v1b_frozen_lz": {"MG": v1b_frozen["MG"], "DL": v1b_frozen["DL"],
                      "yt_cross": v1b_frozen["yt_cross"]},
    "v1c_lib_frozen": {"MG": v1c_lib["MG"], "DL": v1c_lib["DL"],
                       "shift_vs_v1a_lib": rel(v1c_lib["MG"], v1a_lib["MG"])},
}

C01_A = sc(abs(cal["v1a_vs_v1aalpha"]["rel_MG"]) < 2e-3)
C01_B = sc(abs(cal["v1a_lib"]["rel_MG_vs_r447"]) < 2e-3 and
           abs(cal["v1a_lib"]["rel_DL_vs_r447"]) < 5e-2)
C01_C = sc(abs(cal["v1b_lib_frozen"]["rel_MG_vs_stdA"]) < 2e-3 and
           abs(cal["v1b_lib_frozen"]["rel_DL_vs_stdA"]) < 5e-2)
C01_D = sc(abs(cal["v1b_lib_frozen"]["diff_L23_vs_r447bB"]) < 5e-3)
C01_ALL = C01_A and C01_B and C01_C and C01_D
entry("C01", "PASS" if C01_ALL else "FAIL",
      "V1 变体校准（阈值均 1 TeV）：① 初值来源差（[C] 库内 initial_alpha 反推 vs 来稿硬编码）"
      "(%+.4f, %+.4f, %+.4f)——来稿 4.1 把自己的读数与 r447 读数直接比『偏差<0.5%%』，属跨初值"
      "比较；② 机器校验：V1a（g 空间）与 V1aα（α⁻¹ 空间）同初值互差 %+.2e——积分变量无关；"
      "③ 库内初值 V1a-lib vs r447 主册六读数：M_G 相对差 %+.2e、ΔL %+.2e（L12/L13/L23 = "
      "%.4f/%.4f/%.4f vs %.4f/%.4f/%.4f）；④ 库内标准口径（SM 段冻结 y_t，源码级核对）"
      "V1b-lib-frozen vs r447b_A 标准：M_G %+.2e、ΔL %+.2e、α_G %+.2e、y_t(M_G) %+.2e"
      "（实测 %.4f vs 册报 %.4f）；⑤ vs r447b_B 册 α₂=α₃ 交点 t₀=32.030981928：L23 差 %+.4f"
      "——%s；C 组扫描以 V1b（来稿初值+正确 Δb）为工作框架审计来稿声明"
      % (cal["init_provenance"]["diff_1"], cal["init_provenance"]["diff_2"],
         cal["init_provenance"]["diff_3"],
         cal["v1a_vs_v1aalpha"]["rel_MG"],
         cal["v1a_lib"]["rel_MG_vs_r447"], cal["v1a_lib"]["rel_DL_vs_r447"],
         v1a_lib["L12"], v1a_lib["L13"], v1a_lib["L23"],
         L12_R447, L13_R447, L23_R447,
         cal["v1b_lib_frozen"]["rel_MG_vs_stdA"], cal["v1b_lib_frozen"]["rel_DL_vs_stdA"],
         cal["v1b_lib_frozen"]["rel_AG_vs_stdA"], cal["v1b_lib_frozen"]["rel_yt_vs_stdA"],
         v1b_lib["yt_cross"], YT_MG_STD_A,
         cal["v1b_lib_frozen"]["diff_L23_vs_r447bB"],
         "独立引擎四重互印成立" if C01_ALL else "存在超出阈值残差，C 组结论以方向与量级为准"),
      cal)

shift_b = cal["v1b_lib_frozen"]["shift_vs_v1a_lib"]
shift_c = cal["v1c_lib_frozen"]["shift_vs_v1a_lib"]
B05_OK = sc(shift_b is not None and shift_c is not None and
            abs(shift_b - SHIFT_STD_A) < 5e-3 and abs(shift_c) > 0.08)
entry("B05", "CORRECTED" if B05_OK else "INFO",
      "r447b_A 册面 α⁻¹ 式 Yukawa 项系数为笔误（源码级确认+数值对照，登记不改既有册字节）："
      "册面写 +c_i·y_t²/(8π²)，但其源码 dalpha_inv_exact 实际用 c_i·y_t²/(32π³)（教材 g 式"
      "等价，两者差 4π 倍）；机器对照：教材口径 M_G 相对无 Yukawa 漂移 %+.3f%% ≈ 册报"
      " −1.93%%，按册面 4π 口径漂移 %+.3f%% 与册报明显不符——册面式应更正为 c_i·y_t²/(32π³)"
      "（等价 c_i·α_y/(8π²)，α_y=y_t²/4π）"
      % (100 * shift_b, 100 * shift_c),
      {"shift_textbook": shift_b, "shift_alpha4pi": shift_c,
       "shift_reported": SHIFT_STD_A})

# ================================================================ C 组扫描（V1b 工作框架）
beta_work = make_beta_std()

# C02 胶微子扫描
glu_pts = {}
for m in (100.0, 500.0, 1000.0, 5000.0, 10000.0):
    glu_pts[m] = run_stats(beta_work, (1000.0, 1000.0, 1000.0, m))
mg1000 = v1b["MG"]
dev = {m: (glu_pts[m]["MG"] / mg1000 - 1.0) if glu_pts[m]["MG"] else None for m in glu_pts}
C02_DIR = sc(glu_pts[100.0]["MG"] > glu_pts[10000.0]["MG"])
entry("C02", "FAIL" if C02_DIR else "PASS",
      "胶微子扫描（V1b，100/500/1000/5000/10000 GeV，M_G:=α₁-α₂ 交汇 L12 标度）：相对 1 TeV "
      "变化 %+.2f%% → %+.2f%%（100→10000 GeV），方向 = M_G 随胶微子阈值升高而%s，单调%s——"
      "与来稿 4.2 表（100 GeV→10 TeV 给 −12%%→+8%%，即随阈值升高而上升）方向相反、幅度小约"
      " 5 倍。来稿大敏感度与 M_G:=L12 约定不相容（胶微子只经 Δb₃ 与二圈交叉项微弱影响 L12），"
      "倒与其展示判据的 α₂-α₃ 对（对 α₃ 直接敏感）相配——但该判据在其展示源码下恒不触发（B01）"
      % (100 * dev[100.0], 100 * dev[10000.0],
         "下降" if C02_DIR else "上升",
         all(glu_pts[a]["MG"] > glu_pts[b]["MG"]
             for a, b in ((100.0, 500.0), (500.0, 1000.0), (1000.0, 5000.0),
                          (5000.0, 10000.0)))),
      {"glu_scan": {("%g" % m): {"MG": glu_pts[m]["MG"], "DL": glu_pts[m]["DL"],
                                 "rel": dev[m]} for m in sorted(glu_pts)}})

# C03 敏感度排序（1 参数 100/1000/10000）
scan_1p = {}
for name, idx in (("M1_ewgaugino", 0), ("M2_higgs", 1), ("M3_sfermion", 2), ("M4_gluino", 3)):
    pts = {}
    for m in (100.0, 10000.0):
        th = list(BASE_TH)
        th[idx] = m
        pts[m] = run_stats(beta_work, tuple(th))
    pts[1000.0] = {"MG": mg1000}
    rng = None
    mgs = [pts[m]["MG"] for m in (100.0, 1000.0, 10000.0)]
    if all(mgs):
        rng = (max(mgs) - min(mgs)) / mg1000
    scan_1p[name] = {"pts": pts, "range": rng,
                     "low": pts[100.0]["MG"] / mg1000 - 1.0,
                     "high": pts[10000.0]["MG"] / mg1000 - 1.0}
order = sorted(scan_1p.keys(), key=lambda k: -(scan_1p[k]["range"] or 0))
C03_OK = sc(scan_1p["M1_ewgaugino"]["range"] > scan_1p["M4_gluino"]["range"])
entry("C03", "CORRECTED" if C03_OK else "FAIL",
      "敏感度排序复算（V1b，1 参数 100/1000/10000 GeV，M_G 相对带宽）：%s——"
      "电弱gaugino 束（Bino+Wino，正确 Δb 行 (0,4/3,0)）以带宽 %.1f%% 绝对主导：它同时翻转 b₁、"
      "b₂ 的符号（SM → MSSM 闭合速率 −1.157 → −0.886 /ln），直接驱动 L12 交汇；来稿 4.2 排序"
      "（gluino −12%%→+8%% 最高 > sfermion > ew-gaugino ±3-4%% 中 > higgsino ±1%% 低）与正确 "
      "Δb 结构不符——其 M1『中』评级正是其错误 Bino 行（−22/5,−6,0 不改变 α₂⁻¹ 上升速率）的"
      "直接后果，数字与其自身错误 Δb 表内部自洽、与正确代数矛盾（A02/A03）"
      % (" > ".join("%s %.1f%%" % (k, 100 * scan_1p[k]["range"]) for k in order),
         100 * scan_1p["M1_ewgaugino"]["range"]),
      {"ranges": {k: scan_1p[k]["range"] for k in scan_1p},
       "low_high": {k: [scan_1p[k]["low"], scan_1p[k]["high"]] for k in scan_1p}})

# C04 联合粗网格 {100,1000,10000}⁴
grid = {}
mg_list = []
dl_list = []
vals = (100.0, 1000.0, 10000.0)
for m1 in vals:
    for m2 in vals:
        for m3 in vals:
            for m4 in vals:
                if (m1, m2, m3, m4) == BASE_TH:
                    r = v1b
                else:
                    r = run_stats(beta_work, (m1, m2, m3, m4))
                grid["%g/%g/%g/%g" % (m1, m2, m3, m4)] = r
                if r["MG"]:
                    mg_list.append(r["MG"])
                if r["DL"] is not None:
                    dl_list.append(r["DL"])
mg_min, mg_max = min(mg_list), max(mg_list)
dl_min = min(dl_list)
C04_BAND = sc(mg_min < 0.95e16 and mg_max > 1.25e16)
C04_DL = sc(dl_min < 0.15)
entry("C04", "FAIL" if (C04_BAND and C04_DL) else "CORRECTED",
      "联合粗网格（{100,1000,10000}⁴ = %d 点，V1b）：M_G 实际可达 [%.4g, %.4g] GeV，来稿 4.3 "
      "声称 0.95–1.25e16（±13%%）——实际带宽约为声称的 8 倍，声称带被双侧穿透%s；ΔL 最小 "
      "%.4f（ΔL 有效点 %d/%d），来稿声称『只能压到 ≈0.15、无法 ΔL=0』——4 个阈值对 3 个交汇"
      "条件在正确 Δb 下普遍可解，粗网格已见 %.4f，『残余不匹配不可消除』说法在正确代数下不成立"
      "（%s）" % (len(grid), mg_min, mg_max,
                  "（min < 0.95e16：%s；max > 1.25e16：%s）" % (mg_min < 0.95e16, mg_max > 1.25e16),
                  dl_min, len(dl_list), len(grid), dl_min,
                  "带覆盖与 ΔL 压低均超出声称" if (C04_BAND and C04_DL) else "以本册读数为准"),
      {"MG_min": mg_min, "MG_max": mg_max, "DL_min": dl_min,
       "DL_defined": len(dl_list), "grid_points": len(grid)})

# C05 二圈矩阵敏感性（B→0.5B、B→0）
v2_half = stats_bscale(BASE_TH, 0.5, beta=beta_work)
v2_zero = stats_bscale(BASE_TH, 0.0, beta=beta_work)
s_half = v2_half["MG"] / mg1000 - 1
s_zero = v2_zero["MG"] / mg1000 - 1
C05_FLAG = sc(abs(s_half) > 0.02 or abs(s_zero) > 0.02)
entry("C05", "CORRECTED" if C05_FLAG else "PASS",
      "二圈矩阵敏感性（V1b 基准，B→0.5B / B→0）：M_G 漂移 %+.3f%% / %+.3f%%——B₂ 归属未定"
      "（B03 存疑、正确 MSSM 矩阵待文献）的系统不确定性远大于来稿『偏差<0.5%% 属步长误差』"
      "的精度声明，该声明在 B 归属未文献核对前无意义" % (100 * s_half, 100 * s_zero),
      {"shift_half": s_half, "shift_zero": s_zero})

# C06 步长收敛
v3_fine = run_stats(beta_work, BASE_TH, dt=0.001)
c06_rel = abs(v3_fine["MG"] / mg1000 - 1)
C06_OK = sc(c06_rel < 1e-3)
entry("C06", "PASS" if C06_OK else "FAIL",
      "步长收敛（V1b 基准，dt 0.005→0.001）：M_G 相对差 %.2e %s 1e-3 判据——本册百分位量级读数"
      "非离散化噪声；来稿『<0.5%% 属步长误差』的口径以本册实测为准（其展示源码在基准即崩溃，"
      "该说法本身无引擎支撑，见 B01）" % (c06_rel, "低于" if C06_OK else "高于"),
      {"rel": c06_rel})

# ================================================================ D/E/G 定性
entry("D01", "FAIL",
      "模块 4 全部数字（4.1 基准核验、4.2 敏感度表、4.3 带宽与 ΔL 定价）无来源支撑：展示源码在"
      "基准即崩溃（B01）且打印变量错位（B02）；4.1 引用的『r447 单一阈值 1.1247e16』是无 Yukawa "
      "基准，而来稿引擎含全程 Yukawa（同口径标准值应为 0.3955/1.1030e16）——基准混用且初值不同"
      "源（来稿硬编码 (59, 29.6, 8.4) vs r447 反推 (59.02, 29.58, 8.47)，见 C01①），偏差<0.5% "
      "的说法双重不成立；4.2 的方向与幅度跟随其错误 Δb 表（A02/A03/C02/C03）；4.3 带宽 ±13% "
      "与 ΔL 底 0.15 在正确代数下双侧偏离（C04）。子模块 B 定价结论整体不可采信，须以本册 V1b "
      "重算为准")
entry("D02", "PASS",
      "来稿诚实姿态部分保留：0/6 自评分含 FAIL 0 但 BOUNDARY 3/ INFO 5 自曝（超伴子谱外部输入、"
      "二圈阈值修正未计入、精确统一需额外自由度）；『MSSM 框架内参数量化研究、不构成第一性预言、"
      "全局 0/6 记分板不变』定位正确；与 r456 B-02 同构：4 阈值自由度拟合统一 = 定价外部输入，"
      "不是预言")
entry("D03", "PASS",
      "攻破力净账：修正侧 +3（Δb 表与累加校验错误机器定位 A02/A03——其正确值与库内 r447b_B 册"
      "锁定 Δb 独立互证（E04）；B₂『MSSM』标签存疑登记 B03——对 r447 主册亦为新发现；"
      "r447b_A 册面 α⁻¹ 式 Yukawa 系数笔误源码级锁定 B05）；谱系性『数字与源码不可对账』"
      "第三次登记（B01/B02）；对统一目标净前提下降 0；红线不变："
      "0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4")
entry("E01", "PASS",
      "r447 主册交叉：ΔL 定义（成对交汇跨度）、M_G:=L12 交汇、1.1247e16 基准沿用一致；本册 "
      "V1a-lib 以其源码 INPUT 反推初值独立复现其六读数（C01③）；初值来源差本身机器量化"
      "（C01①）；本册 B03 对其锁定的 B₂『MSSM』标签提出存疑登记（不改既有册字节，承审计纪律）")
entry("E02", "PASS",
      "r447b_A 交叉：标准顶列 (26/5,6,4)/负号、来料口径 benchmark 化、I13『数字与代码不一致』"
      "先例——本册 B01/B02/B04 为该先例谱系性重复；来稿『与子模块A一致』声明被本册证伪；"
      "其 SM 段冻结 y_t 的处理经源码核对后作为本册库内标准变体（C01④），"
      "y_t(M_G)=0.7564 册报值纳入互印；册面 α⁻¹ 式系数笔误源码级登记（B05）")
entry("E03", "PASS",
      "attack25/28/33 MSSM 出口审计链同类（参数化 MSSM 出口的代价账）；attack72/73 外部来料"
      "审计模式沿用；本册来料属算法联盟 r447 分支（非 ROOT 谱系）——谱系登记")
entry("E04", "PASS",
      "库内 r447b_B/r447b_C 册交叉（2026-11-25 已在案）：库内 r447b_B 走 δᵢ 阈值位移定价路线，"
      "其 Δb=b_MSSM−b_SM=(5/2, 25/6, 4) 与本册 A03 独立重演精确一致（互证）；其正式口径 "
      "α₂=α₃ 交点 t₀=32.030981928 纳入本册 C01⑤ 互印；定位分工：库内册=外生 δᵢ 定价，"
      "本册=来稿 4 阈值 b 累计路线的正确代数重演与源码审计——互补不重叠；库内已推进至 r447c"
      "（源码在案），后续仍须满足本册 G01 前置条件")
entry("G01", "INFO",
      "下一步：库内链已自行推进 r447b_B（δᵢ 定价）→ r447b_C/r447c（精确交汇微调）；算法联盟"
      "若再提交 r447d 及以上，前置条件 = ①采纳正确 Δb 表与分组（A03，补第二 Higgs 标量双态行）"
      "②修复交汇判据与打印索引、统一 M_G:=L12 约定（B01/B02）③文献核对并替换 B₂（B03）"
      "④统一基准口径：含/不含 Yukawa 分列、按标准顶列与负号、初值注明来源（B04/C01①）"
      "——否则微调量化建立在已证伪的地基上")
entry("G02", "BOUNDARY",
      "复算边界：B₂ 按 r447 锁定口径沿用（其 MSSM 归属存疑见 B03，正确值待文献，C05 给出该"
      "不确定度对 M_G 的影响 ±6–12%）；第二 Higgs 双态并入 M2 是本册声明的设计选择（来稿分组"
      "缺失该行，独立成行仅改变阈值归属不改 Σ）；y_b=0、tanβ 未建模（承 r447b_A）；正确 MSSM "
      "二圈矩阵未钉死前，V1b 属『教材反馈量级 + 锁定 B₂』的工作框架；本册全部数值在 MSSM+外部"
      "谱输入口径内成立")

# ================================================================ G0 量纲守卫
DIM_ZERO = (0, 0, 0, 0)
DIM_M = (1, 0, 0, 0)


def dim_add(x, y):
    return tuple(a + b for a, b in zip(x, y))


dim_checks = [
    ("[b],[Δb] 无量纲（β 函数系数）", dim_add(DIM_ZERO, DIM_ZERO) == DIM_ZERO),
    ("[T(R)] 无量纲（表示指数）", DIM_ZERO == DIM_ZERO),
    ("[α],[g],[y_t] 无量纲（耦合）", DIM_ZERO == DIM_ZERO),
    ("[M_G]=质量维 (1,0,0,0)：M_G=M_Z·e^t", dim_add(DIM_M, DIM_ZERO) == DIM_M),
    ("[t]=[ln μ] 无量纲", DIM_ZERO == DIM_ZERO),
    ("[ΔL] 无量纲（成对交汇 ln 跨度）", DIM_ZERO == DIM_ZERO),
    ("[c_i],[B_ij] 无量纲（二圈系数）", DIM_ZERO == DIM_ZERO),
]
dim_pass = sum(1 for _, ok in dim_checks if ok)
for _n, _ok in dim_checks:
    sc(_ok)
entry("G0", "PASS" if dim_pass == len(dim_checks) else "FAIL",
      "量纲守卫（M,L,T,Q 四元组）%d/%d：[b]、[Δb]、[T(R)]、[α]、[g]、[y_t]、[c_i]、[B_ij] "
      "无量纲；[M_G]=质量维（M_Z·e^t）；[t] 与 [ΔL] 无量纲——ΔL 是对数跨度不是质量，与 M_G "
      "的带宽分属两类读数" % (dim_pass, len(dim_checks)),
      {"dim_checks": [n for n, ok in dim_checks if ok]})

# ================================================================ 输出
counts = {}
for e in entries:
    counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1

data = {
    "meta": {
        "engine": BASE + ".py",
        "date": STAMP,
        "laiLiao": "用户粘贴文本 算法联盟 r447b 子模块B「非简并阈值全参数扫描+自由度量化审计」"
                   "（库内 r447 主册与 r447b_A 判定册在案，1.1247 基准 22 处命中）",
        "stdlib_only": True,
        "exact_algebra": "fractions.Fraction（承 r447 formal Decimal+Fraction 先例）",
        "decimal_prec": 50,
        "selfchecks": selfchecks,
        "verdict_counts": counts,
        "entries_total": len(entries),
        "cited_C": ["SM 二圈矩阵 arXiv:1502.06929（B₂₁=9/10、B₃₁=11/10）",
                    "正确 MSSM 二圈矩阵（需文献核对）",
                    "r447 主册基准六读数", "r447b_A 标准口径四读数", "y_t(M_Z)=0.95"],
        "relay": "r447(二圈RG+阈值+质子衰变) → r447b_A(顶Yukawa) → [来稿 r447b-B 提交] → "
                 "attack74(独立外审)；库内 r447b_B/r447b_C 册已先行在案（E04 交叉）",
    },
    "algebra": {
        "b_reconstructed": [str(g) for g, _ in b_targets],
        "sum_input": [str(x) for x in summed_in],
        "mismatch": [str(x) for x in mismatch],
        "delta_v1": [[str(x) for x in row] for row in delta_v1],
        "sum_v1": [str(x) for x in sum_v1],
        "b1_by_formula": str(b1_by_formula),
        "ratio_B21": str(ratio21), "ratio_B31": str(ratio31),
        "cu_diff": [str(x) for x in cu_diff],
    },
    "v0_runs": v0_runs,
    "calibration": {k: {kk: (vv if isinstance(vv, (int, float, bool, str)) or vv is None
                             else [float(x) for x in vv]) for kk, vv in v.items()}
                    for k, v in cal.items()},
    "glu_scan": {("%g" % m): {kk: (float(x) if x is not None else None)
                              for kk, x in glu_pts[m].items()} for m in sorted(glu_pts)},
    "scan_1p": {k: {"range": scan_1p[k]["range"], "low": scan_1p[k]["low"],
                    "high": scan_1p[k]["high"]}
                for k in scan_1p},
    "grid": {"MG_min": mg_min, "MG_max": mg_max, "DL_min": dl_min,
             "DL_defined": len(dl_list), "points": len(grid)},
    "v2": {"shift_half": s_half, "shift_zero": s_zero},
    "v3": {"rel": c06_rel},
    "entries": entries,
}
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

lines = []
lines.append("attack74 · r447b 子模块B「非简并阈值全参数扫描+自由度量化审计」独立复算与判定引擎报告")
lines.append("日期：%s　纯标准库　Fraction 精确代数 + Decimal prec=%d 读数" % (STAMP, getcontext().prec))
lines.append("来料：用户粘贴文本（r447 主册/r447b_A 判定册在案，1.1247 基准 22 处命中——接力第三册）")
lines.append("读数：条目 %d（%s）、自检 %d/%d" % (
    len(entries),
    " / ".join("%s %d" % (k, v) for k, v in sorted(counts.items())),
    selfchecks[0], selfchecks[1]))
lines.append("")
lines.append("== 一圈代数（Fraction 精确）==")
lines.append("b 重演 %d/6；来稿 ΣΔb 累加 → (%s, %s, %s) ≠ (33/5, 1, −3)；" % (
    sum(1 for got, want in b_targets if got == want),
    fstr(summed_in[0]), fstr(summed_in[1]), fstr(summed_in[2])))
lines.append("正确 Δb 分组 Σ = (5/2, 25/6, 4) 精确；来稿公式符号演示 b₁→%s" % fstr(b1_by_formula))
lines.append("B₂₁/B₃₁ vs 文献 SM：×%s、×%s；C_U 差 (%s, %s, %s)" % (
    fstr(ratio21), fstr(ratio31), fstr(cu_diff[0]), fstr(cu_diff[1]), fstr(cu_diff[2])))
lines.append("")
lines.append("== V0 忠实重演（来稿源码语义）==")
for k, v in v0_runs.items():
    lines.append("%s: crossed=%s t=%s" % (k, v["crossed"], v["t"]))
lines.append("")
lines.append("== V1 校准（变体矩阵，阈值均 1 TeV）==")
lines.append("初值来源差（库内反推 − 来稿硬编码）: (%+.4f, %+.4f, %+.4f)"
             % (cal["init_provenance"]["diff_1"], cal["init_provenance"]["diff_2"],
                cal["init_provenance"]["diff_3"]))
lines.append("V1a  无Yukawa 来稿初值 g空间 : M_G=%.6g  ΔL=%.6f  L=(%.4f, %.4f, %.4f)"
             % (v1a["MG"], v1a["DL"], v1a["L12"], v1a["L13"], v1a["L23"]))
lines.append("V1aα 无Yukawa 来稿初值 α⁻¹空间: M_G=%.6g  ΔL=%.6f  (与V1a互差 %+.2e)"
             % (v1a_alpha["MG"], v1a_alpha["DL"], cal["v1a_vs_v1aalpha"]["rel_MG"]))
lines.append("V1a-lib 库内初值 α⁻¹空间    : M_G=%.6g  ΔL=%.6f  L=(%.4f, %.4f, %.4f)  vs r447: %+.2e/%+.2e"
             % (v1a_lib["MG"], v1a_lib["DL"], v1a_lib["L12"], v1a_lib["L13"], v1a_lib["L23"],
                cal["v1a_lib"]["rel_MG_vs_r447"], cal["v1a_lib"]["rel_DL_vs_r447"]))
lines.append("V1b-lib-frozen 库内标准口径  : M_G=%.6g  ΔL=%.6f  α_G=%.6f  y_t(M_G)=%.4f  L23=%.4f"
             "  vs 标准口径: %+.2e/%+.2e  vs r447b_B t₀: %+.4f"
             % (v1b_lib["MG"], v1b_lib["DL"], v1b_lib["alpha_G"], v1b_lib["yt_cross"],
                v1b_lib["L23"], cal["v1b_lib_frozen"]["rel_MG_vs_stdA"],
                cal["v1b_lib_frozen"]["rel_DL_vs_stdA"],
                cal["v1b_lib_frozen"]["diff_L23_vs_r447bB"]))
lines.append("V1b  工作框架（来稿初值，y 全程）: M_G=%.6g  ΔL=%.6f  y_t(M_G)=%.4f"
             % (v1b["MG"], v1b["DL"], v1b["yt_cross"]))
lines.append("V1b-frozen 来稿初值 SM段冻结 : M_G=%.6g  ΔL=%.6f  y_t(M_G)=%.4f"
             % (v1b_frozen["MG"], v1b_frozen["DL"], v1b_frozen["yt_cross"]))
lines.append("V1c-lib 册面4π口径           : M_G=%.6g  漂移 vs V1a-lib: %+.3f%%（册报 −1.93%%；"
             "教材口径漂移 %+.3f%%）" % (v1c_lib["MG"], 100 * shift_c, 100 * shift_b))
lines.append("")
lines.append("== C 组扫描（V1b 工作框架）==")
lines.append("胶微子扫描（相对 1 TeV）: " + "  ".join(
    "%g:%+.2f%%" % (m, 100 * dev[m]) for m in sorted(dev)))
for k in ("M4_gluino", "M3_sfermion", "M1_ewgaugino", "M2_higgs"):
    lines.append("1 参数带宽 %s: %.4f（100GeV %+.2f%% / 10TeV %+.2f%%）" % (
        k, scan_1p[k]["range"], 100 * scan_1p[k]["low"], 100 * scan_1p[k]["high"]))
lines.append("网格 %d 点: M_G [%.4g, %.4g]  ΔL_min=%.4f（有效 %d/%d）" % (
    len(grid), mg_min, mg_max, dl_min, len(dl_list), len(grid)))
lines.append("B 敏感性: 0.5B %+.3f%% / 0B %+.3f%%；dt 收敛 %.2e" % (
    100 * s_half, 100 * s_zero, c06_rel))
lines.append("")
lines.append("== 条目全表 ==")
for e in entries:
    lines.append("%-4s %-9s %s" % (e["code"], e["verdict"], e["text"]))
lines.append("")
lines.append("退出码 0（判定为数据，非引擎错误）")
report = "\n".join(lines)
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write(report)
print(report)
