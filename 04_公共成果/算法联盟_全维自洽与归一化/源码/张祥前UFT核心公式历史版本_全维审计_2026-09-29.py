#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论「核心公式历史版本」全维审计（算法联盟口径）

来料：my_lib/utf/10-统一场论核心公式/历史版本/
  20260110/张祥前统一场论核心重要公式方程.md   —— v3.7（28 式，最后更新 2026-02-09）
  张祥前统一场论核心重要公式方程.md            —— v3.5（27 式，最后更新 2026-02-04）
  张祥前统一场论公式层次分析与逻辑引用重排.md   —— 7 层重排表（自称 21 式，表内 25 行）
  张祥前统一场论整合文档.md                    —— v4.0（2026-02-06）
  张祥前统一场论综合文档.md                    —— v3.5 全文 + 层次分析 + 量纲总表 + 参考文献
  常数验证脚本.py / 常数验证结果分析.md          —— 2026-02-08
  量纲验证.py                                  —— 2026-02-05
  verify_formulas.py                          —— 2026-02-11
  核心公式索引.md / README.md                   —— 20 式 / 17 式口径

本册做六件事：
  1) 来料盘点与口径漂移（S1）
  2) 常数体系：数值 + 量纲 + 与观测基准对照（S2）
  3) 公式量纲审计：v3.7 全 28 式逐条机器判定（S3）
  4) 版本谱系与回归：v3.5 → v3.7 的删/改/增与「修复是否真修复」（S4）
  5) 验证脚本自身的方法论审计（S5）
  6) 物理强度 / 可检验性 / 第一性层级（S6、S7）

红线：只判「数学自洽」与「与观测一致」，不判第一性成立；缺陷如实标 FAIL，不粉饰。
量纲一律用 SI 四维 (L, M, T, I)，电荷 Q = I·T 不单独设维。

复跑：C:\\Users\\mo\\AppData\\Local\\Programs\\Python\\Python38\\python.exe 张祥前UFT核心公式历史版本_全维审计_2026-09-29.py
产物：数据/张祥前UFT核心公式历史版本_全维审计_2026-09-29.{json,md}
"""

import sys
import os
import json
import math
import hashlib
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]          # .../my_lib/openuft
DATA_DIR = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化" / "数据"
SOURCE_DIR = ROOT.parent / "utf" / "10-统一场论核心公式" / "历史版本"

STAMP = "2026-09-29"
BASENAME = "张祥前UFT核心公式历史版本_全维审计_" + STAMP

# ---------------------------------------------------------------- 计数器 / 输出器

_COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
_RECORDS = []


def _emit(tag, sid, title, detail):
    _COUNTS[tag] = _COUNTS.get(tag, 0) + 1
    _RECORDS.append({"id": sid, "verdict": tag, "title": title, "detail": detail})
    mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "BOUNDARY": "[BND ]", "INFO": "[INFO]"}[tag]
    print(mark + " " + sid + " | " + title)
    print("       " + detail)


def P(sid, title, detail):
    _emit("PASS", sid, title, detail)


def F(sid, title, detail):
    _emit("FAIL", sid, title, detail)


def B(sid, title, detail):
    _emit("BOUNDARY", sid, title, detail)


def I(sid, title, detail):
    _emit("INFO", sid, title, detail)


# ---------------------------------------------------------------- 量纲代数（SI: L, M, T, I）

def D(L=0, M=0, T=0, I=0):
    return (L, M, T, I)


def mul(*ds):
    out = [0, 0, 0, 0]
    for d in ds:
        for k in range(4):
            out[k] += d[k]
    return tuple(out)


def div(a, b):
    return tuple(a[k] - b[k] for k in range(4))


def pow_dim(a, n):
    return tuple(a[k] * n for k in range(4))


def fmt(d):
    names = ["L", "M", "T", "I"]
    parts = []
    for k in range(4):
        if d[k] != 0:
            parts.append(names[k] + "^" + str(d[k]))
    return " ".join(parts) if parts else "1（无量纲）"


ZERO = D()

# 基本量与导出量
c = D(L=1, T=-1)                      # 光速 m/s
G = D(L=3, M=-1, T=-2)                # 万有引力常数
eps0 = D(L=-3, M=-1, T=4, I=2)        # 真空介电常数 F/m
mu0 = D(L=1, M=1, T=-2, I=-2)         # 真空磁导率 H/m
hbar = D(L=2, M=1, T=-1)              # 约化普朗克常数
H0 = D(T=-1)                          # 哈勃常数
mp = D(M=1)                           # 普朗克质量
qp = D(T=1, I=1)                      # 普朗克电荷（库仑 = A·s）

k_dim_claim = D(M=1)                  # k 声明单位 kg
kprime_claim = div(mul(qp, D(T=1)), D(M=1))    # k' 声明单位 C·s/kg = M^-1 T^2 I
kprime_formula = div(qp, c)           # k' 计算式 q_p/c 的真实量纲 = C·s/m

Z_dim = mul(G, c)                     # Z = Gc/2
Zp_dim = div(c, eps0)                 # Z' = c/(8πε₀)
Lam_dim = D(L=-2)                     # Λ = 3H₀²/c²

A_dim = D(L=1, T=-2)                  # 引力场 A（引力加速度）
E_dim = D(L=1, M=1, T=-3, I=-1)       # 电场 N/C
B_dim = D(M=1, T=-2, I=-1)            # 磁场 N/(A·m)
Dfield_dim = D(L=1, T=-3)             # 核力场（文档标称 LT^-3）
F_dim = D(L=1, M=1, T=-2)             # 力
p_dim = D(L=1, M=1, T=-1)             # 动量
q_dim = qp                            # 电荷
V_dim = c                             # 速度
f_dim = D(M=1, I=-1)                  # f 由式 14 反解：kg/A（量纲验证.py 同）

NABLA = div(ZERO, D(L=1))             # ∇ 的量纲 1/L
DT = div(ZERO, D(T=1))                # d/dt 的量纲 1/T

# ---------------------------------------------------------------- 数值（CODATA 2018 / Planck 2018）

C_VAL = 2.99792458e8
G_VAL = 6.67430e-11
EPS0_VAL = 8.8541878128e-12
HBAR_VAL = 1.054571817e-34
H0_VAL = 2.3e-18                      # 文档取值（≈71 km/s/Mpc）
OMEGA_LAMBDA_PLANCK = 0.685           # Planck 2018
LAMBDA_OBS = 1.106e-52                # m^-2（Planck 2018 常用读数）
E_CHARGE = 1.602176634e-19
M_E = 9.1093837015e-31
M_P_PROTON = 1.67262192369e-27
R_NUC = 1.0e-15                       # 1 fm

# ================================================================ 第 1 节 来料盘点

print("=" * 86)
print("第 1 节  来料盘点与口径漂移")
print("=" * 86)

INVENTORY = [
    ("20260110/张祥前统一场论核心重要公式方程.md", "v3.7", "28 式", "2026-02-09"),
    ("张祥前统一场论核心重要公式方程.md", "v3.5", "27 式", "2026-02-04"),
    ("张祥前统一场论公式层次分析与逻辑引用重排.md", "—", "7 层重排表（自称 21 式，表内 25 行）", "2026-02-11"),
    ("张祥前统一场论整合文档.md", "v4.0", "27 式 + 常数体系", "2026-02-06"),
    ("张祥前统一场论综合文档.md", "v3.5", "27 式 + 层次分析 + 量纲总表 + 参考文献", "2026-02-04"),
    ("常数验证脚本.py", "—", "常数数值 + 3 式量纲", "2026-02-08"),
    ("常数验证结果分析.md", "—", "结论：全部正确", "2026-02-08"),
    ("量纲验证.py", "—", "常量量纲（发现 Z' 标注错）", "2026-02-05"),
    ("verify_formulas.py", "—", "常数 + 10 式量纲 + 逻辑链", "2026-02-11"),
    ("核心公式索引.md", "—", "20 式口径", "2026-01-26"),
    ("README.md", "—", "17 式口径", "2026-02-06"),
]

if SOURCE_DIR.is_dir():
    found = []
    for rel, *_ in INVENTORY:
        p = SOURCE_DIR / rel
        if p.is_file():
            found.append((rel, p.stat().st_size))
        else:
            found.append((rel, None))
    missing = [r for r, s in found if s is None]
    I("S1-01", "来料目录存在，文件 %d/%d 命中" % (len(found) - len(missing), len(found)),
      "目录 " + str(SOURCE_DIR) + "；未命中：" + (", ".join(missing) if missing else "无"))
    for rel, size in found:
        if size is not None:
            print("       - " + rel + "  (" + str(size) + " B)")
else:
    B("S1-01", "来料目录不可达，盘点降级为文档内证据", "路径 " + str(SOURCE_DIR) + " 不存在")

I("S1-02", "版本命名与内容漂移：20260110/ 子目录内实为 v3.7（最后更新 2026-02-09）",
  "目录名日期 2026-01-10 与内容版本号 v3.7 / 更新日期 2026-02-09 三者不一致，凭目录名无法定位版本")

F("S1-03", "公式条数口径四轨并存：17 / 20 / 27 / 28",
  "README.md 称 17 式；核心公式索引.md 称 20 式（且称「所有 20 个核心公式均已通过量纲验证 100%」）；"
  "根目录主文档 v3.5 为 27 式；20260110/ 主文档 v3.7 为 28 式。同一目录四套计数，无单一真源")

F("S1-04", "层次分析文档自称 21 式，重排表实为 25 行，且编号冲突",
  "自称「21个公式」，表内 25 行；磁场行重排序号误写为 9（与引力场重号，应为 11）；"
  "「原序号 22」同时用于「量子化质量」与「圆周运动正电荷产生的引力场」两个不同公式")

# ================================================================ 第 2 节 常数体系

print()
print("=" * 86)
print("第 2 节  常数体系：数值、量纲、与观测基准")
print("=" * 86)

mp_val = math.sqrt(HBAR_VAL * C_VAL / G_VAL)
qp_val = math.sqrt(4.0 * math.pi * EPS0_VAL * HBAR_VAL * C_VAL)
k_val = 4.0 * math.pi * mp_val
kprime_val = qp_val / C_VAL
Z_val = G_VAL * C_VAL / 2.0
Zp_val = C_VAL / (8.0 * math.pi * EPS0_VAL)
Lam_val = 3.0 * H0_VAL ** 2 / C_VAL ** 2

DOC = {"k": 2.736e-7, "k_prime": 6.25e-27, "Z": 1.000e-2, "Z_prime": 1.347e18, "Lambda": 1.7e-52}

P("S2-01", "普朗克质量 m_p = √(ħc/G) 数值复算一致",
  "计算 %.6e kg vs 文档 2.176434e-08 kg，相对差 %.2e（定义式重排，非预言）"
  % (mp_val, abs(mp_val - 2.176434e-8) / 2.176434e-8))

P("S2-02", "普朗克电荷 q_p = √(4πε₀ħc) 数值复算一致",
  "计算 %.6e C vs 文档 1.8755e-18 C，相对差 %.2e；注意该式以 ε₀ 为输入，非几何导出"
  % (qp_val, abs(qp_val - 1.8755e-18) / 1.8755e-18))

B("S2-03", "k = 4πm_p：数值可对，「4π」与 m_p 均无推导",
  "计算 %.4e kg vs 文档 %.3e kg（差 %.2f%%）；4π 因子无来源，m_p 由 (ħ,G,c) 外部输入 ⇒ L1 借用"
  % (k_val, DOC["k"], abs(k_val - DOC["k"]) / DOC["k"] * 100.0))

P("S2-04", "k' 数值 = q_p/c 复算一致（纯数值层面）",
  "计算 %.4e vs 文档 %.3e（差 %.2f%%）" % (kprime_val, DOC["k_prime"],
                                        abs(kprime_val - DOC["k_prime"]) / DOC["k_prime"] * 100.0))

F("S2-05", "【核心】k' 的「计算式」与「声明单位」量纲互斥（量纲两难）",
  "声明单位 C·s/kg ⇒ 量纲 " + fmt(kprime_claim) + "；计算式 q_p/c 的真实量纲 " + fmt(kprime_formula) +
  "（= C·s/m）。二者差 " + fmt(div(kprime_formula, kprime_claim)) +
  "。取声明单位则电荷式(9)成立而磁场式(11)缺速度因子；取计算式则电荷式(9)不成立。两种取值下体系都至少崩一式")

_s2_06_num = "计算 %.5e m⁴/(kg·s³) vs 文档 %.3e（差 %.2f%%）" % (
    Z_val, DOC["Z"], abs(Z_val - DOC["Z"]) / DOC["Z"] * 100.0)
P("S2-06", "Z = Gc/2 数值与量纲自洽",
  _s2_06_num + "；量纲 " + fmt(Z_dim) + " 与文档标注一致")

_s2_07_num = "计算 %.5e vs 文档 %.4e（差 %.3f%%）" % (
    Zp_val, DOC["Z_prime"], abs(Zp_val - DOC["Z_prime"]) / DOC["Z_prime"] * 100.0)
P("S2-07", "Z' = c/(8πε₀) 数值自洽，量纲标注在公式总览表中写错",
  _s2_07_num + "；正确量纲 " + fmt(Zp_dim) + "，而 v3.5/v3.7 公式总览表均写 L^4 M T^-3 I^-2（漏 T^-2）")

F("S2-08", "Λ = 3H₀²/c² 漏 Ω_Λ 因子，与观测偏 +60%",
  "计算 %.4e m^-2（文档 1.7e-52，差 3.87%% 属自比自舍入）；与 Planck 观测 Λ≈%.3e m^-2 比偏高 %.1f%%。"
  "标准关系为 Λ = 3H₀²Ω_Λ/c²（Ω_Λ=0.685），文档等价于强设 Ω_Λ=1"
  % (Lam_val, LAMBDA_OBS, (Lam_val / LAMBDA_OBS - 1.0) * 100.0))

B("S2-09", "Z / Z' 属恒等重排，不产生新物理（L0）",
  "Z=Gc/2 ⇔ G=2Z/c；Z'=c/(8πε₀) ⇔ ε₀=c/(8πZ')。二者只是把已知常数换个符号，" \
  "「引力-光速统一」「电磁光速几何耦合」的命名不携带额外预测")

# ================================================================ 第 3 节 公式量纲审计（v3.7）

print()
print("=" * 86)
print("第 3 节  公式量纲审计：v3.7 全 28 式")
print("=" * 86)

kk_claim = mul(k_dim_claim, kprime_claim)          # 按声明单位：I T^2
kk_formula = mul(k_dim_claim, kprime_formula)      # 按计算式：M^-1... 

# 每条：(编号, 名称, lhs, [rhs 各项名+量纲], 文档标称量纲, 备注)
# 说明：立体角 Ω、n、γ 均无量纲；Δn/Δs 按常数验证脚本的读法取无量纲（另一种读法见 S3-04b）
FORMULAS_V37 = [
    ("F01", "时空同一化方程 r = C t", D(L=1), [("C·t", mul(c, D(T=1)))], D(L=1), ""),
    ("F02", "三维螺旋时空方程（含 h·t 项）", D(L=1),
     [("r·cos(ωt)", D(L=1)), ("h·t（h 标称 m/rad）", mul(D(L=1), D(T=1)))], D(L=1), ""),
    ("F03", "质量定义方程 m = k·dn/dΩ", D(M=1),
     [("k·(dn/dΩ)", mul(k_dim_claim, ZERO))], D(M=1), ""),
    ("F04", "引力场定义方程（原始形式 r/r³）", A_dim,
     [("G·k·(Δn/Δs)·(r/r³)", mul(G, k_dim_claim, ZERO, div(D(L=1), pow_dim(D(L=1), 3))))], A_dim, ""),
    ("F05", "静止动量方程 p₀ = m₀C₀", p_dim, [("m₀·C₀", mul(D(M=1), c))], p_dim, ""),
    ("F06", "运动动量方程 P = m(C−V)", p_dim, [("m·(C−V)", mul(D(M=1), c))], p_dim, ""),
    ("F07", "宇宙大统一方程 F = dP/dt", F_dim, [("dP/dt", mul(p_dim, DT))], F_dim, ""),
    ("F08", "空间波动方程 ∇²L = (1/C²)∂²L/∂t²", mul(D(L=1), pow_dim(NABLA, 2)),
     [("(1/C²)·∂²L/∂t²", mul(D(L=1), pow_dim(DT, 2), pow_dim(div(ZERO, c), 2)))],
     mul(D(L=1), pow_dim(NABLA, 2)), ""),
    ("F09", "电荷定义方程 q = k'k(1/Ω²)(dΩ/dt)", q_dim,
     [("k'·k·(1/Ω²)·(dΩ/dt)（k'取声明单位）", mul(kk_claim, DT))], q_dim, ""),
    ("F10", "电场定义方程（原始形式 ε₀）", E_dim,
     [("k·k'/(4πε₀Ω²)·(dΩ/dt)·(r/r³)", mul(kk_claim, div(ZERO, eps0), DT,
                                          div(D(L=1), pow_dim(D(L=1), 3))))], E_dim, ""),
    ("F11", "磁场定义方程（原始形式 μ₀）", B_dim,
     [("μ₀·γ·k·k'/(4πΩ²)·(dΩ/dt)·(R/R'³)", mul(mu0, kk_claim, DT,
                                              div(D(L=1), pow_dim(D(L=1), 3))))], B_dim, ""),
    ("F12", "变化的引力场产生电磁场（带 f）", mul(A_dim, pow_dim(DT, 2)),
     [("(1/f)·V·(∇·E)", mul(div(ZERO, f_dim), V_dim, mul(E_dim, NABLA))),
      ("(1/f)·C²·(∇×B)", mul(div(ZERO, f_dim), pow_dim(c, 2), mul(B_dim, NABLA)))],
     mul(A_dim, pow_dim(DT, 2)), ""),
    ("F13", "引力场旋度方程 ∇×(∂A/∂t) = B/f", mul(mul(A_dim, DT), NABLA),
     [("B/f", div(B_dim, f_dim))], D(L=1, T=-2), "文档标称量纲栏写 LT^-2，与左端不等"),
    ("F14", "变化的引力场产生电场 E = −f·dA/dt", E_dim,
     [("f·(dA/dt)", mul(f_dim, mul(A_dim, DT)))], E_dim, ""),
    ("F15", "变化的磁场产生引力场和电场", mul(B_dim, DT),
     [("f·(A×E)/C²", mul(f_dim, A_dim, E_dim, div(ZERO, pow_dim(c, 2)))),
      ("(V/C²)×(dE/dt)", mul(div(V_dim, pow_dim(c, 2)), mul(E_dim, DT)))],
     mul(B_dim, DT), ""),
    ("F16", "统一场论能量方程 E = m₀C²", D(L=2, M=1, T=-2),
     [("m₀·C²", mul(D(M=1), pow_dim(c, 2)))], D(L=2, M=1, T=-2), ""),
    ("F17", "光速飞行器动力学方程 F = (C−V)dm/dt", F_dim,
     [("(C−V)·(dm/dt)", mul(c, mul(D(M=1), DT)))], F_dim, ""),
    ("F18", "核力场定义方程 D = −Gm(C−3r̂ṙ)/r³", Dfield_dim,
     [("G·m·(C 或 ṙ)/r³", mul(G, D(M=1), c, div(ZERO, pow_dim(D(L=1), 3))))], Dfield_dim, ""),
    ("F19", "引力光速统一方程 Z = Gc/2", Z_dim, [("G·c/2", mul(G, c))], Z_dim, ""),
    ("F20", "电磁光速几何耦合常数 Z' = c/(8πε₀)", Zp_dim, [("c/(8πε₀)", div(c, eps0))],
     D(L=4, M=1, T=-3, I=-2), "文档标称漏 T^-2"),
    ("F21", "加速运动电荷产生引力场方程（实给 B_θ）", B_dim,
     [("q/(4πε₀C³r)·(A×r̂)", mul(q_dim, div(ZERO, eps0), div(ZERO, pow_dim(c, 3)),
                                div(ZERO, D(L=1)), A_dim))], B_dim, ""),
    ("F22", "圆周运动正电荷产生的引力场方程（实给 B_θ）", B_dim,
     [("q/(4πε₀C³)·(1/r)·(A×r̂)", mul(q_dim, div(ZERO, eps0), div(ZERO, pow_dim(c, 3)),
                                    div(ZERO, D(L=1)), A_dim))], B_dim, ""),
    ("F23", "引力场自转化方程 ∂²A/∂t² = ∇²A − ∇(∇·A)", mul(A_dim, pow_dim(DT, 2)),
     [("∇²A", mul(A_dim, pow_dim(NABLA, 2))),
      ("∇(∇·A)", mul(mul(A_dim, NABLA), NABLA))], D(L=1, T=-3), ""),
    ("F24", "电磁场自转化方程 ∇²E − (1/C²)∂²E/∂t² = ∇(∇·E)", mul(E_dim, pow_dim(NABLA, 2)),
     [("(1/C²)·∂²E/∂t²", mul(E_dim, pow_dim(DT, 2), pow_dim(div(ZERO, c), 2))),
      ("∇(∇·E)", mul(mul(E_dim, NABLA), NABLA))], D(L=1, M=1, T=-4, I=-1), "文档标称量纲写作 MLI^-1T^-4"),
    ("F25", "引力场产生核力场方程 D = −g·∇×A", Dfield_dim,
     [("g·(∇×A)（g 未定义量纲）", mul(A_dim, NABLA))], Dfield_dim, ""),
    ("F26", "核力场产生引力场方程 ∂A/∂t = −h·∇×D", mul(A_dim, DT),
     [("h·(∇×D)（h 未定义量纲）", mul(Dfield_dim, NABLA))], D(L=1, T=-3), ""),
    ("F27", "电磁场产生核力场方程 D = −k·∇×E", Dfield_dim,
     [("k·(∇×E)（k 复用式3 的 k）", mul(k_dim_claim, mul(E_dim, NABLA)))], Dfield_dim, ""),
    ("F28", "核力场自转化方程 ∂²D/∂t² = ∇²D − ∇(∇·D)", mul(Dfield_dim, pow_dim(DT, 2)),
     [("∇²D", mul(Dfield_dim, pow_dim(NABLA, 2))),
      ("∇(∇·D)", mul(mul(Dfield_dim, NABLA), NABLA))], D(L=1, T=-4), ""),
]

formula_rows = []
fail_ids = []
for fid, name, lhs, rhs_terms, doc_dim, note in FORMULAS_V37:
    lhs_ok_terms = []
    for tname, tdim in rhs_terms:
        lhs_ok_terms.append(tdim == lhs)
    consistent = all(lhs_ok_terms)
    doc_ok = (doc_dim == lhs)
    row = {
        "id": fid, "name": name,
        "lhs": fmt(lhs),
        "rhs": [{"term": t, "dim": fmt(d), "match": (d == lhs)} for t, d in rhs_terms],
        "self_consistent": consistent,
        "doc_dim_claim": fmt(doc_dim),
        "doc_dim_ok": doc_ok,
        "note": note,
    }
    formula_rows.append(row)
    if not consistent:
        fail_ids.append(fid)

n_total = len(FORMULAS_V37)
n_fail = len(fail_ids)
n_pass = n_total - n_fail
print("v3.7 量纲审计：总 %d 式，量纲自洽 %d，不自洽 %d（%s）" % (n_total, n_pass, n_fail, ", ".join(fail_ids)))
for row in formula_rows:
    flag = "OK " if row["self_consistent"] else "BAD"
    print("   " + flag + " " + row["id"] + " " + row["name"] + " | 左=" + row["lhs"])
    for t in row["rhs"]:
        print("         " + ("=" if t["match"] else "≠") + " " + t["term"] + " → " + t["dim"])
    if not row["doc_dim_ok"]:
        print("         文档标称量纲 " + row["doc_dim_claim"] + " 与左端 " + row["lhs"] + " 不符")

P("S3-01", "v3.7 量纲机器审计完成：%d/%d 式自洽" % (n_pass, n_total),
  "不成立条目：" + ", ".join(fail_ids) + "（逐条见下文定点）")

for fid in fail_ids:
    row = [r for r in formula_rows if r["id"] == fid][0]
    bad = [t["term"] + "→" + t["dim"] for t in row["rhs"] if not t["match"]]
    F("S3-" + fid, "式 " + fid + " 量纲不自洽：" + row["name"],
      "左端 " + row["lhs"] + "；失配项 " + "；".join(bad))

B("S3-F04b", "式 4 的 Δn/Δs 存在量纲歧义，两种读法都不能让两种形式同时成立",
  "脚本读法（Δn/Δs 无量纲）下原始形式 r/r³ 成立、Z 转换形式 r/r 或 r/r² 不成立；"
  "若 Δs 取位移长度（量纲 L^-1），则原始形式也随之失配。文档未定义 s，量纲不可判定")

F("S3-F13b", "耦合常数 f 在三条方程中要求的量纲互不兼容",
  "式14 反解 f = " + fmt(f_dim) + "；式13 要求 f = " + fmt(div(B_dim, mul(mul(A_dim, DT), NABLA))) +
  "。二者差 " + fmt(div(div(B_dim, mul(mul(A_dim, DT), NABLA)), f_dim)) +
  " ⇒ 不存在单一 f 同时满足式12/13/14/15")

F("S3-F22b", "式 21 与式 22 表达式实质重复且名实不符",
  "两式右端同为 −q/(4πε₀C³r)·(A×r̂)，仅书写形式不同；二者名称均称「产生引力场方程」，"
  "实际给出的是磁感应强度 B_θ")

F("S3-F23b", "式 23 与式 28 数学形式完全相同，标称量纲却不同（LT^-3 vs LT^-4）",
  "同为 ∂²X/∂t² = ∇²X − ∇(∇·X)，同一结构在两个场量上给出两份标称量纲，内部矛盾；"
  "且两式均缺 c² 因子（失配量 " + fmt(div(mul(A_dim, pow_dim(DT, 2)), mul(A_dim, pow_dim(NABLA, 2)))) + " = C²）")

F("S3-F27b", "式 27 复用符号 k，与式 3 的质量耦合常数冲突",
  "式3 的 k 为「空间-质量耦合常数」量纲 " + fmt(k_dim_claim) + "；式27 的 k 若为同一量，"
  "则右端量纲 " + fmt(mul(k_dim_claim, mul(E_dim, NABLA))) + " ≠ 核力场 " + fmt(Dfield_dim) +
  "；若为新常数则属未声明的符号重载")

# ================================================================ 第 4 节 版本谱系与回归

print()
print("=" * 86)
print("第 4 节  版本谱系：v3.5(27 式) → v3.7(28 式) 的删改增与「修复是否真修复」")
print("=" * 86)

REMOVED_IN_V37 = [
    ("量子化质量方程 m = n·m₀", "v3.5-23"),
    ("宇宙学常数方程 Λ = 3H₀²/c²", "v3.5-24"),
    ("场的量子化方程（场算符展开）", "v3.5-25"),
    ("时空曲率方程（爱因斯坦场方程 + Λ）", "v3.5-26"),
    ("统一场论波函数方程（薛定谔方程）", "v3.5-27"),
]
ADDED_IN_V37 = [
    ("引力场自转化方程（∂²A/∂t² = ∇²A − ∇(∇·A)）", "v3.7-23", "缺 c²，量纲失配"),
    ("电磁场自转化方程", "v3.7-24", "形式自洽（标准波动方程恒等变形）"),
    ("引力场产生核力场方程（引入 g）", "v3.7-25", "g 未定义量纲"),
    ("核力场产生引力场方程（引入 h）", "v3.7-26", "h 未定义量纲（反解为长度量纲）"),
    ("电磁场产生核力场方程（引入 k）", "v3.7-27", "k 符号重载 + 量纲失配"),
    ("核力场自转化方程", "v3.7-28", "缺 c²，量纲失配"),
]

I("S4-01", "v3.5 → v3.7：删除 5 式、新增 6 式",
  "删除：" + "；".join(n for n, _ in REMOVED_IN_V37) +
  "。新增：" + "；".join(n for n, _, _ in ADDED_IN_V37))

B("S4-02", "删除的 5 式全部是「借用标准方程」，删除本身是诚实性提升",
  "被删的量子化质量、Λ 定义式、场算符展开、爱因斯坦场方程、薛定谔方程均非本体系派生，"
  "而是标准理论直接搬入；移除后「借用清单」缩短。代价是 v3.7 不再声明自己与 GR/QM 的关系")

F("S4-03", "【回归】式 10 的 Z' 转换形式由 v3.5 的 2Z'/C 变成 v3.7 的 Z'/C²，改坏",
  "v3.5（层次分析 L37、整合文档 L45、综合文档 L56）为 −(2Z'/C)·k·k'·(1/Ω²)·(dΩ/dt)·(r/r³)，量纲 " +
  fmt(mul(div(Zp_dim, c), kk_claim, DT, div(D(L=1), pow_dim(D(L=1), 3)))) + " = 电场 ✓；"
  "v3.7 改为 −(Z'/C²)… 得 " +
  fmt(mul(div(Zp_dim, pow_dim(c, 2)), kk_claim, DT, div(D(L=1), pow_dim(D(L=1), 3)))) + " ≠ 电场")

F("S4-04", "【回归】式 15 在 v3.5 无 f 时两项皆自洽，v3.7 给第一项加 f 后失配",
  "v3.5：dB/dt = −(A×E)/C² − (V/C²)×(dE/dt)，两项量纲均为 " + fmt(mul(B_dim, DT)) + "；"
  "v3.7：首项变为 −f(A×E)/C²，量纲 " + fmt(mul(f_dim, A_dim, E_dim, div(ZERO, pow_dim(c, 2)))) +
  "，比左端多出一个 f")

P("S4-05", "【真修复】式 12 在 v3.5 无 f 时失配，v3.7 加 f 后两项皆自洽",
  "v3.5 首项量纲 " + fmt(mul(V_dim, mul(E_dim, NABLA))) + " ≠ 左端 " +
  fmt(mul(A_dim, pow_dim(DT, 2))) + "；v3.7 引入 (1/f) 后两项同时等于左端")

F("S4-06", "式 13 在两版均不自洽，v3.6 声称的「修复量纲问题」未覆盖此式",
  "v3.5：∇×(∂A/∂t) = B，左 " + fmt(mul(mul(A_dim, DT), NABLA)) + " vs 右 " + fmt(B_dim) + "；"
  "v3.7：右端改 B/f 得 " + fmt(div(B_dim, f_dim)) + "，仍与左端差 " +
  fmt(div(mul(mul(A_dim, DT), NABLA), div(B_dim, f_dim))))

F("S4-07", "修正未回流：量纲验证.py（2026-02-05）已算出 Z' 正确量纲，公式表（2026-02-09）仍写错",
  "量纲验证.py 明确打印「之前的错误量纲 L⁴ M T⁻³ I⁻² / 正确量纲 " + fmt(Zp_dim) + "」，"
  "但 v3.7 公式总览表第 20 行仍标 L⁴MT⁻³I⁻²；修正停在脚本层，未回写文档")

I("S4-08", "版本净效应（可算）",
  "量纲失配条目：v3.5 与 v3.7 各有硬失配（详见 S3/S4 逐条）。"
  "删除借用式 5 条（−5 借用）+ 新增自由参数 g/h/k 三条（+3 未定常数）"
  " ⇒ 外部依赖下降，内部自由度上升，可证伪性净下降")

# ================================================================ 第 5 节 验证脚本方法论审计

print()
print("=" * 86)
print("第 5 节  验证脚本自身的方法论审计")
print("=" * 86)

F("S5-01", "verify_formulas.py 的「量纲验证」只有 print，无一次比较",
  "verify_dimensions() 全程 f-string 打印「左边 / 右边 / 量纲一致 ✓」，无任何 assert、"
  "无程序化比较；verify_logical_chain() 同样只 print「逻辑推导链完整 ✓」，属打印式伪验证")

F("S5-02", "常数验证脚本的「误差」是与文档值比，不是与观测比（自比自）",
  "document_constants 全部取自同一文档的舍入值（k 2.736e-7、k' 6.25e-27、Z 1.000e-2、"
  "Z' 1.347e18、Λ 1.7e-52），最大 3.87% 的 Λ 偏差只是两次舍入之差；全流程无一个观测基准")

F("S5-03", "【严重】常数验证脚本把被验公式的 r/r² 改成 r/r³ 后才判「一致」",
  "三份文档（层次分析 L36、整合文档 L39、综合文档 L50）引力场定义式均为 −Gk(Δn/Δs)(r/r²)；"
  "脚本第 289 行验的却是「A = -Gk Δn/Δs r/r³」并把 r/r³ 视作 1/L²。按文档原式验则量纲为 " +
  fmt(mul(G, k_dim_claim, div(ZERO, D(L=1)))) + " ≠ 加速度 " + fmt(A_dim))

F("S5-04", "常数验证脚本从不检查「计算式量纲」与「声明单位」是否一致",
  "k' 的 dimension 字段被直接写为 Q*T/M（声明值），而 value 用 q_p/c 计算；脚本对两者是否相容零检验，"
  "这正是 S2-05 量纲两难被掩盖至今的机制")

F("S5-05", "覆盖度与结论强度不匹配（过度外推）",
  "verify_formulas.py 验 10 式 / 27~28 式 ≈ 36%；常数验证脚本验 3 式 ≈ 11%；"
  "但结论均写「所有公式量纲一致」「理论内部自洽，逻辑严谨」，覆盖不足却做全称断言")

F("S5-06", "全目录零「计算值 vs 观测值」对照表",
  "整合文档、综合文档、层次分析文档均无与实验/观测数据的数值对照（无偏差表、无观测列）；"
  "「理论的可验证性」只以方法名罗列（粒子加速器、宇宙观测、引力波探测器等），无一条可执行判据")

B("S5-07", "层次分析文档未声明任何公式属「借用/类比」，全部表述为「从…推导」",
  "文档将 27 式全部归入自建推导链；其中波动方程、能量方程、场量子化、爱因斯坦方程、"
  "薛定谔方程实为标准理论搬入，未作来源标注 ⇒ 来源账本缺失")

# ================================================================ 第 6 节 物理强度与可检验性

print()
print("=" * 86)
print("第 6 节  物理强度与可检验性")
print("=" * 86)

# 核力场：以 G 为耦合，在 1 fm 处的引力型力 vs 同距离电磁力
F_G_nuc = G_VAL * M_P_PROTON ** 2 / R_NUC ** 2
F_EM_nuc = (1.0 / (4.0 * math.pi * EPS0_VAL)) * E_CHARGE ** 2 / R_NUC ** 2
ratio = F_EM_nuc / F_G_nuc
F("S6-01", "「核力场」以 G 为耦合常数，比同距离电磁力弱 %.1e 倍（≈%.0f 个量级）" % (ratio, math.log10(ratio)),
  "式 18 D = −Gm(…)/r³ 在 r=1 fm、m=m_p 时对应力标度 %.3e N；同距离两质子库仑力 %.3e N。"

  "以引力常数描述核力，强度差约 36 量级，与该式自称的「短程强相互作用几何描述」矛盾"
  % (F_G_nuc, F_EM_nuc))

# 电荷式：要给出基本电荷所需的 (1/Ω²)dΩ/dt
kk_num_claim = k_val * kprime_val          # 按声明单位 C·s
need_rate = E_CHARGE / kk_num_claim
B("S6-02", "电荷定义式要给出基本电荷，需 (1/Ω²)·dΩ/dt = %.3e s^-1（无独立约束）" % need_rate,
  "k·k' = %.4e（声明单位 C·s）；e = 1.602e-19 C ⇒ 所需立体角变化率 %.3e s^-1。"
  "该速率既无理论约束也无观测渠道 ⇒ 式 9 对电荷量级零预测力（自由度未锁定）"
  % (kk_num_claim, need_rate))

dn_domega_e = M_E / k_val
B("S6-03", "质量定义式要给出电子质量，需 dn/dΩ = %.3e（无独立约束）" % dn_domega_e,
  "m = k·dn/dΩ，k = %.4e kg ⇒ dn/dΩ = %.3e。同一个 k 下任意质量都可由某个 dn/dΩ 拟合，"
  "式 3 不产生质量谱预言" % (k_val, dn_domega_e))

F("S6-04", "Λ 是唯一有外部观测可比的常数，且偏高 %.0f%%" % ((Lam_val / LAMBDA_OBS - 1.0) * 100.0),
  "式 24（v3.5）/ 常数表给出 Λ = 3H₀²/c² = %.4e m^-2；Planck 2018 观测 ≈ %.3e m^-2。"
  "这是全体系唯一可被观测直接检验的数值，且未通过（漏 Ω_Λ）" % (Lam_val, LAMBDA_OBS))

I("S6-05", "式 21/22（电荷-引力耦合）无标准理论对应，也无实验支撑",
  "B_θ = −q/(4πε₀c³r)(A×r̂) 量纲自洽（靠 1/c³ 凑成），但引力场 A 与电荷 q 直接耦合出磁场"
  "在 Maxwell/GR 中无对应项；文档未给出任何数值算例或实验渠道")

# ================================================================ 第 7 节 第一性层级判定

print()
print("=" * 86)
print("第 7 节  第一性层级判定（L0 恒等重排 / L1 借用类比 / L2 可算自洽 / L3 可证伪新预言）")
print("=" * 86)

LAYERS = {
    "L0": [("F07", "F=dP/dt 是 P=m(C−V) 的恒等求导"),
           ("F19", "Z=Gc/2 ⇔ G=2Z/c 恒等重排"),
           ("F20", "Z'=c/(8πε₀) ⇔ ε₀=c/(8πZ') 恒等重排"),
           ("常数", "m_p=√(ħc/G)、q_p=√(4πε₀ħc) 为普朗克单位定义式")],
    "L1": [("F08", "借用标准波动方程形式"),
           ("F16", "借用狭义相对论质能关系"),
           ("F24", "借用 Maxwell 波动方程（真空恒等变形）"),
           ("F18", "用引力常数 G 描述核力，属命名类比"),
           ("F21/F22", "电荷-引力耦合的辐射场类比，无标准对应"),
           ("v3.5-25/26/27", "场算符展开 / 爱因斯坦场方程 / 薛定谔方程，标准理论搬入")],
    "L2": [("F01/F02", "运动学定义（F02 的 h·t 项量纲失配）"),
           ("F03/F09", "质量与电荷的几何定义式，量纲自洽但常数外部"),
           ("F05/F06", "动量定义（与标准 p=mv 不同，属体系内自洽）"),
           ("F10", "库仑定律代入自带 q（原始形式自洽）")],
    "L3": [],
}

for lv, items in LAYERS.items():
    if items:
        for fid, why in items:
            print("   " + lv + " | " + fid + " — " + why)
    else:
        print("   " + lv + " | （无）")

n_l0 = len(LAYERS["L0"])
n_l1 = len(LAYERS["L1"])
n_l2 = len(LAYERS["L2"])
n_l3 = len(LAYERS["L3"])

F("S7-01", "全体系 L3（可证伪新预言）条目数 = 0",
  "28 式 + 5 个核心常数中，无一条给出标准理论之外、且能被实验判定真伪的新数值预言。"
  "唯一的对外数值接触点是 Λ（S6-04），且未通过")

B("S7-02", "层级分布：L0=%d / L1=%d / L2=%d / L3=%d" % (n_l0, n_l1, n_l2, n_l3),
  "以「借用/类比 + 定义重排」为主体；「体系内可算自洽」的条目全部依赖外部常数锚（G、ε₀、ħ、H₀、m_p、q_p）")

I("S7-03", "本册评级（openuft 口径）",
  "来料体系评级 **C / L1**：存在硬冲突（k' 量纲两难、f 量纲不唯一、式 12/13/14/15 互不相容、"
  "式 23/28 缺 c²、Λ 与观测偏差 60%、验证脚本篡改被验式），且主体为标准理论借用；"
  "整理工作本身为中性事实记录，不构成对该体系的背书")

# ================================================================ 第 8 节 自检

print()
print("=" * 86)
print("第 8 节  不可回退基线自检")
print("=" * 86)

GUARDS = []


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print(("   [OK] " if ok else "   [XX] ") + name + " — " + detail)
    return ok


guard("量纲代数封闭性", mul(c, div(ZERO, c)) == ZERO, "c·(1/c) = 无量纲")
guard("电场量纲自校验",
      mul(E_dim, pow_dim(D(L=1), 2)) == div(mul(D(M=1), D(L=1), pow_dim(D(T=1), -2),
                                                pow_dim(D(L=1), 2)), q_dim),
      "E·L² = (力·L²)/电荷")
guard("磁场量纲自校验",
      B_dim == div(mul(D(M=1), D(L=1), pow_dim(D(T=1), -2)), mul(D(I=1), D(L=1))),
      "B = N/(A·m)")
guard("μ₀ = 8πZ'/c³ 恒等", div(Zp_dim, pow_dim(c, 3)) == mu0,
      fmt(div(Zp_dim, pow_dim(c, 3))) + " = " + fmt(mu0))
guard("ε₀ = c/(8πZ') 恒等", div(c, Zp_dim) == eps0, fmt(div(c, Zp_dim)) + " = " + fmt(eps0))
guard("Z' 标称错误可复现", D(L=4, M=1, T=-3, I=-2) != Zp_dim,
      "文档标注 " + fmt(D(L=4, M=1, T=-3, I=-2)) + " ≠ 计算 " + fmt(Zp_dim))
guard("k' 两难可复现", kprime_claim != kprime_formula,
      fmt(kprime_claim) + " ≠ " + fmt(kprime_formula))
guard("f 量纲冲突可复现", f_dim != div(B_dim, mul(mul(A_dim, DT), NABLA)),
      "式14 反解 " + fmt(f_dim) + " ≠ 式13 反解 " + fmt(div(B_dim, mul(mul(A_dim, DT), NABLA))))
guard("Λ 偏差可复现", Lam_val > LAMBDA_OBS * 1.3, "%.3e > 1.3×%.3e" % (Lam_val, LAMBDA_OBS))
guard("式23 缺 c² 可复现",
      div(mul(A_dim, pow_dim(DT, 2)), mul(A_dim, pow_dim(NABLA, 2))) == pow_dim(c, 2),
      "左/右 = " + fmt(pow_dim(c, 2)))
guard("计数守恒", sum(_COUNTS.values()) == len(_RECORDS), "记录数 %d" % len(_RECORDS))

guard_fail = [g for g in GUARDS if not g["ok"]]

# ================================================================ 产物

print()
print("=" * 86)
print("汇总")
print("=" * 86)
print("PASS = %d" % _COUNTS["PASS"])
print("FAIL = %d" % _COUNTS["FAIL"])
print("BOUNDARY = %d" % _COUNTS["BOUNDARY"])
print("INFO = %d" % _COUNTS["INFO"])
print("总数 = %d" % len(_RECORDS))
print("自检 = %d/%d" % (len(GUARDS) - len(guard_fail), len(GUARDS)))
print("公式量纲：%d 式中 %d 式自洽（失配：%s）" % (n_total, n_pass, ", ".join(fail_ids)))
print("第一性层级：L0=%d L1=%d L2=%d L3=%d" % (n_l0, n_l1, n_l2, n_l3))

DATA_DIR.mkdir(parents=True, exist_ok=True)

payload = {
    "stamp": STAMP,
    "source_dir": str(SOURCE_DIR),
    "counts": dict(_COUNTS),
    "total": len(_RECORDS),
    "records": _RECORDS,
    "inventory": [{"file": r, "version": v, "scope": s, "date": d} for r, v, s, d in INVENTORY],
    "constants": {
        "mp": {"value": mp_val, "unit": "kg", "dim": fmt(D(M=1))},
        "qp": {"value": qp_val, "unit": "C", "dim": fmt(qp)},
        "k": {"value": k_val, "doc": DOC["k"], "unit_claim": "kg", "dim": fmt(k_dim_claim)},
        "k_prime": {"value": kprime_val, "doc": DOC["k_prime"], "unit_claim": "C·s/kg",
                    "dim_claim": fmt(kprime_claim), "dim_by_formula": fmt(kprime_formula),
                    "dilemma": True},
        "Z": {"value": Z_val, "doc": DOC["Z"], "dim": fmt(Z_dim)},
        "Z_prime": {"value": Zp_val, "doc": DOC["Z_prime"], "dim": fmt(Zp_dim),
                    "dim_doc_wrong": fmt(D(L=4, M=1, T=-3, I=-2))},
        "Lambda": {"value": Lam_val, "doc": DOC["Lambda"], "obs_planck": LAMBDA_OBS,
                   "dev_pct": (Lam_val / LAMBDA_OBS - 1.0) * 100.0},
    },
    "formula_dimensions_v37": formula_rows,
    "formula_fail_ids": fail_ids,
    "version_lineage": {
        "v3.5": {"date": "2026-02-04", "count": 27},
        "v3.7": {"date": "2026-02-09", "count": 28},
        "removed_in_v37": [{"name": n, "id": i} for n, i in REMOVED_IN_V37],
        "added_in_v37": [{"name": n, "id": i, "audit": a} for n, i, a in ADDED_IN_V37],
    },
    "physical_checks": {
        "nuclear_field_F_G_at_1fm_N": F_G_nuc,
        "coulomb_F_EM_at_1fm_N": F_EM_nuc,
        "ratio_EM_over_G": ratio,
        "orders_of_magnitude": math.log10(ratio),
        "charge_rate_needed_s^-1": need_rate,
        "dn_dOmega_for_electron": dn_domega_e,
    },
    "first_principle_layers": {"L0": n_l0, "L1": n_l1, "L2": n_l2, "L3": n_l3,
                               "detail": {k: [{"id": a, "why": b} for a, b in v]
                                          for k, v in LAYERS.items()}},
    "grading": "C / L1",
    "guards": GUARDS,
    "guard_fail": [g["name"] for g in guard_fail],
}

json_path = DATA_DIR / (BASENAME + ".json")
with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)

lines = []
lines.append("# 张祥前统一场论「核心公式历史版本」全维审计 · 数据产物（" + STAMP + "）")
lines.append("")
lines.append("> 脚本：`源码/张祥前UFT核心公式历史版本_全维审计_" + STAMP + ".py`")
lines.append("> 计数：PASS = %d ／ FAIL = %d ／ BOUNDARY = %d ／ INFO = %d ／ 总数 = %d"
             % (_COUNTS["PASS"], _COUNTS["FAIL"], _COUNTS["BOUNDARY"], _COUNTS["INFO"], len(_RECORDS)))
lines.append("> 公式量纲（v3.7，28 式）：自洽 %d ／ 失配 %d（%s）" % (n_pass, n_fail, ", ".join(fail_ids)))
lines.append("> 第一性层级：L0=%d ／ L1=%d ／ L2=%d ／ **L3=%d**　评级 **C / L1**" % (n_l0, n_l1, n_l2, n_l3))
lines.append("")
lines.append("## 1. 四态清单")
lines.append("")
lines.append("| 编号 | 判定 | 条目 | 要点 |")
lines.append("|---|---|---|---|")
for r in _RECORDS:
    lines.append("| " + r["id"] + " | " + r["verdict"] + " | " + r["title"] + " | " +
                 r["detail"].replace("\n", " ") + " |")
lines.append("")
lines.append("## 2. 公式量纲表（v3.7，28 式）")
lines.append("")
lines.append("| 编号 | 公式 | 左端量纲 | 右端量纲 | 自洽 | 文档标称是否一致 |")
lines.append("|---|---|---|---|---|---|")
for row in formula_rows:
    lines.append("| " + row["id"] + " | " + row["name"] + " | " + row["lhs"] + " | " +
                 "；".join(t["dim"] for t in row["rhs"]) + " | " +
                 ("是" if row["self_consistent"] else "**否**") + " | " +
                 ("是" if row["doc_dim_ok"] else "**否**（标称 " + row["doc_dim_claim"] + "）") + " |")
lines.append("")
lines.append("## 3. 版本谱系")
lines.append("")
lines.append("| 版本 | 日期 | 条数 | 变动 |")
lines.append("|---|---|---|---|")
lines.append("| v3.5 | 2026-02-04 | 27 | 含 5 条借用标准方程（量子化质量 / Λ / 场算符 / 爱因斯坦 / 薛定谔） |")
lines.append("| v3.7 | 2026-02-09 | 28 | 删上述 5 条，增 6 条场转化式（引入 g/h/k 三个未定义量纲常数） |")
lines.append("")
lines.append("## 4. 物理强度与可检验性")
lines.append("")
lines.append("| 项 | 数值 |")
lines.append("|---|---|")
lines.append("| 核力场（G 耦合）在 1 fm 的力标度 | %.4e N |" % F_G_nuc)
lines.append("| 同距离两质子库仑力 | %.4e N |" % F_EM_nuc)
lines.append("| 电磁/引力 比值 | %.3e（≈%.0f 个量级） |" % (ratio, math.log10(ratio)))
lines.append("| Λ（文档式 3H₀²/c²） | %.4e m^-2 |" % Lam_val)
lines.append("| Λ（Planck 2018 观测） | %.4e m^-2 |" % LAMBDA_OBS)
lines.append("| Λ 偏差 | +%.1f%% |" % ((Lam_val / LAMBDA_OBS - 1.0) * 100.0))
lines.append("| 给出基本电荷所需 (1/Ω²)dΩ/dt | %.4e s^-1（无约束） |" % need_rate)
lines.append("| 给出电子质量所需 dn/dΩ | %.4e（无约束） |" % dn_domega_e)
lines.append("")
lines.append("## 5. 自检")
lines.append("")
lines.append("| 守卫 | 结果 |")
lines.append("|---|---|")
for g in GUARDS:
    lines.append("| " + g["name"] + " | " + ("通过" if g["ok"] else "**失败**") + " |")
lines.append("")

md_path = DATA_DIR / (BASENAME + ".md")
with open(md_path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print()
print("产物：" + str(json_path))
print("产物：" + str(md_path))

sys.exit(1 if guard_fail else 0)
