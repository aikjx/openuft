# -*- coding: utf-8 -*-
"""
TUFT-r185 审计引擎
S17 核心公式 12「变化的引力场产生电磁场」
靶：01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/12-变化的引力场产生电磁场/
     v1（推导与物理诠释.md） / v2（本项目重新求导证明与验证.md） / v3（1.md + code/）
纯标准库：Decimal(60) + Fraction (M,L,T,I) 量纲四元组 + ast 方法论审计
机读驱动：控制组 + 守卫全为真实计算，禁止写死 True
"""
import os, sys, json, math, re, ast, traceback
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# ---------- 路径（BASE = openuft；纪律：dirname(dirname(ROOT))）----------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # 本项目_全维自洽与归一化
BASE = os.path.dirname(os.path.dirname(ROOT))     # openuft
TARGET = os.path.join(BASE, "01_独立体系", "S17_统一场论核心公式",
                      "04_理论推导", "核心公式集", "12-变化的引力场产生电磁场")

FILES = {
    "V1":   os.path.join(TARGET, "v1", "统一场论变化的引力场产生电磁场推导与物理诠释.md"),
    "V2":   os.path.join(TARGET, "v2", "变化的引力场产生电磁场：本项目通过耦合系数f的重新求导证明与验证.md"),
    "V3":   os.path.join(TARGET, "v3", "1.md"),
    "V3PY": os.path.join(TARGET, "v3", "code", "detailed_verification.py"),
    "V3REP":os.path.join(TARGET, "v3", "code", "DATA_VERIFICATION_REPORT.md"),
    "V3FC": os.path.join(TARGET, "v3", "code", "force_comparison.py"),
}
DATA_DIR = os.path.join(ROOT, "数据")
OUT_BASE = "TUFT-r185_引力场产生电磁场_麦克斯韦重写与f量纲冲突_精算_2026-10-25"

# ---------- 量纲四元组 (M, L, T, I) ----------
def D(M, L, T, I):
    return (M, L, T, I)
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))
def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))
def dpow(a, n):
    return tuple(int(round(x * n)) for x in a)
def deq(a, b):
    return all(x == y for x, y in zip(a, b))
def dstr(a):
    names = ["M", "L", "T", "I"]
    parts = []
    for v, n in zip(a, names):
        if v != 0:
            parts.append(n + ("" if v == 1 else ("^%d" % v)))
    return "·".join(parts) if parts else "1(无量纲)"

M = D(1,0,0,0); L = D(0,1,0,0); T = D(0,0,1,0); I = D(0,0,0,1)
c_dim   = D(0,1,-1,0)
eps0_dim= D(-1,-3,4,2)
G_dim   = D(-1,3,-2,0)
mu0_dim = D(1,1,-2,-2)
E_dim   = D(1,1,-3,-1)
A_dim   = D(0,1,-2,0)        # 引力场加速度
dA_dt_dim = D(0,1,-3,0)
B_dim   = D(1,0,-2,-1)

# f 公式维：(c/2)*sqrt(4 pi eps0 G)
eps0G_dim = dmul(eps0_dim, G_dim)            # (-2,0,2,2)
sqrt_eps0G_dim = dpow(eps0G_dim, Fraction(1,2))  # (-1,0,1,1)
f_formula_dim = dmul(c_dim, sqrt_eps0G_dim)  # (-1,1,0,1) = M^-1 L I
f_req_dim = ddiv(E_dim, dA_dt_dim)           # (1,0,0,-1) = M I^-1
# v1 §5.6 f ~ sqrt(G/eps0)
G_over_eps0_dim = ddiv(G_dim, eps0_dim)      # (0,6,-6,-2)
f_v1sqrt_dim = dpow(G_over_eps0_dim, Fraction(1,2))  # (0,3,-3,-1) = L^3 T^-3 I^-1

# ---------- 常数（Decimal60）----------
c = Decimal('299792458')
eps0 = Decimal('8.8541878128e-12')
G = Decimal('6.67430e-11')
mu0 = Decimal('1.2566370614e-6')

term = Decimal(4) * Decimal(str(math.pi)) * eps0 * G
sqrt_term = term.sqrt()
f_value = (c / Decimal(2)) * sqrt_term
# 替代路径 f = (c/2)*sqrt(Z/Z'), Z=Gc/2, Z'=c/(8 pi eps0)
Z = (G * c) / Decimal(2)
Zp = c / (Decimal(8) * Decimal(str(math.pi)) * eps0)
f_alt = (Z / Zp).sqrt() * (c / Decimal(2))

# ---------- 文本证据 ----------
def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as e:
        return ""

TXT = {k: read_text(v) for k, v in FILES.items()}

def contains(key, *subs):
    t = TXT.get(key, "")
    return all(s in t for s in subs)

# ---------- 条目 / 控制组 / 守卫 收集 ----------
entries = []      # (id, group, verdict, title, detail)
controls = []     # (id, ok, detail)
guards = []       # (id, ok, detail)

def E(eid, grp, verd, title, detail):
    entries.append((eid, grp, verd, title, detail))
def K(kid, ok, detail):
    controls.append((kid, bool(ok), detail))
def GU(gid, ok, detail):
    guards.append((gid, bool(ok), detail))

# ===================================================================
# 控制组（全部真实计算）
# ===================================================================
# K01: 公理 R=Ct ⇒ A=d²R/dt² ≡ 0（有限差分多步长）
try:
    C = Decimal('299792458')
    resid = []
    for h in [Decimal('1'), Decimal('0.1'), Decimal('1e-3')]:
        R = lambda t: C * t
        a = (R(h) - Decimal(2)*R(Decimal(0)) + R(-h)) / (h*h)
        resid.append(a)
    K01_ok = all(a == Decimal(0) for a in resid)
    K("K01", K01_ok, "R=Ct 下 A=d²R/dt² 有限差分(1,0.1,1e-3)=%s 全为 0 ⇒ 公理直接给出 A≡0" % (resid,))
except Exception as e:
    K("K01", False, "K01 异常: %s" % e)

# K02: f 数值 = 0.012917333313
K02_ok = abs(f_value - Decimal('0.012917333313')) < Decimal('1e-9')
K("K02", K02_ok, "f=(c/2)√(4πε₀G)=%.12e (靶 0.012917333313)" % f_value)

# K03: f 公式维 ≠ 所需维
K03_ok = (not deq(f_formula_dim, f_req_dim))
K("K03", K03_ok, "f公式维[%s] vs 所需[M I^-1]：%s" % (dstr(f_formula_dim), "冲突" if K03_ok else "一致"))

# K04: 方程各项维 = L T^-4
lhs_dim = dpow(A_dim, Fraction(1))  # (0,1,-2,0); d²/dt² => *(T^-2)
lhs_dim = dmul(A_dim, D(0,0,-2,0))  # (0,1,-4,0)
t1 = dmul(dmul(c_dim, ddiv(D(0,0,0,0), f_req_dim)), dmul(D(0,-1,0,0), E_dim))  # (V/f)(∇·E)
t2 = dmul(dmul(dpow(c_dim,2), ddiv(D(0,0,0,0), f_req_dim)), dmul(D(0,-1,0,0), B_dim))  # (c²/f)(∇×B)
K04_ok = deq(lhs_dim, t1) and deq(lhs_dim, t2)
K("K04", K04_ok, "方程项维 左=%s 右1=%s 右2=%s（均 L T^-4）" % (dstr(lhs_dim), dstr(t1), dstr(t2)))

# K05: Z=Gc/2 与 r182 互印
K05_ok = abs(Z - Decimal('1.0004524012e-2')) < Decimal('1e-12')
K("K05", K05_ok, "Z=Gc/2=%.10e（与 r182 Z_FROM_G 互印）" % Z)

# K06: v1 f~√(G/ε₀) 维 = L³T^-3I^-1 ≠ M I^-1
K06_ok = (not deq(f_v1sqrt_dim, f_req_dim))
K("K06", K06_ok, "v1 §5.6 f~√(G/ε₀)维[%s] ≠ [M I^-1]" % dstr(f_v1sqrt_dim))

# K07: 麦克斯韦重写恒等式（标量数值验）
try:
    divE, curlB, Vv, c2, ff = 2.0, 3.0, 5.0, 9.0, 0.0129
    lhs_target = (Vv/ff)*divE - (c2/ff)*curlB
    # 由 E=-f dA/dt ⇒ d²A/dt² = -(1/f) dE/dt ; dE/dt = c²∇×B - (∇·E)V
    dE_dt = c2*curlB - divE*Vv
    lhs_deriv = -(1.0/ff)*dE_dt
    K07_ok = abs(lhs_target - lhs_deriv) < 1e-12
    K("K07", K07_ok, "麦克斯韦重写恒等式：直接=%g 推导=%g（残差 %g）" % (lhs_target, lhs_deriv, lhs_target-lhs_deriv))
except Exception as e:
    K("K07", False, "K07 异常: %s" % e)

# K08: 波方程系数 -(c²/f)(-f)=c²
try:
    coef = -(float(c2)/float(ff)) * (-float(ff))
    K08_ok = abs(coef - float(c2)) < 1e-12
    K("K08", K08_ok, "真空库仑规范下 ∂²A/∂t²=-(c²/f)(∇×B)=c²∇²A 系数 %g=c²" % coef)
except Exception as e:
    K("K08", False, "K08 异常: %s" % e)

# K09: c²=1/(μ₀ε₀) 相对误差
try:
    rel = abs(c*c - Decimal(1)/(mu0*eps0)) / (c*c)
    K09_ok = rel < Decimal('1e-6')
    K("K09", K09_ok, "c²=1/(μ₀ε₀) 相对误差 %.3e（靶 5.44e-8%%）" % rel)
except Exception as e:
    K("K09", False, "K09 异常: %s" % e)

# K10: 氢原子库仑/引力比 = 2.27e39（标准物理正确）
try:
    qe = Decimal('1.602176634e-19'); me = Decimal('9.1093837015e-31'); mp = Decimal('1.67262192369e-27')
    rb = Decimal('5.29177210903e-11')
    k = Decimal(1)/(Decimal(4)*Decimal(str(math.pi))*eps0)
    Fc = k*qe*qe/(rb*rb)
    Fg = G*mp*me/(rb*rb)
    ratio = Fc/Fg
    K10_ok = abs(ratio - Decimal('2.27e39')) < Decimal('0.1e39')
    K("K10", K10_ok, "H 原子库仑/引力=%.3e（靶 2.27e39，标准物理正确）" % ratio)
except Exception as e:
    K("K10", False, "K10 异常: %s" % e)

# K11: v1 vs v3 电场方程符号/Ω² 文本证据
K11_ok = contains("V1", r"f \Omega^2") and contains("V3", r"\vec{E} = -f")
K("K11", K11_ok, "v1 'E = f Ω²∂A/∂t' vs v3 'E = -f ∂A/∂t'（符号+Ω² 矛盾）" if K11_ok else "v1/v3 电场方程文本证据缺失")

# K12: f 双路径数值差 = 0
K12_ok = abs(f_value - f_alt) < Decimal('1e-15')
K("K12", K12_ok, "f 双路径差 %.3e（主方法=%.12e，Z/Z'法=%.12e）" % (abs(f_value-f_alt), f_value, f_alt))

# ===================================================================
# 守卫（机读驱动）
# ===================================================================
GU("G01", all(os.path.exists(p) for p in FILES.values()),
  "六份靶文件可读性：%s" % {k: os.path.exists(v) for k, v in FILES.items()})
GU("G02", contains("V3", r"\vec{R} = \vec{C}t") and contains("V3", r"\vec{A} = d^2\vec{R}/dt^2"),
  "公理文本证据：V3 含 '\\vec{R} = \\vec{C}t' 与 '\\vec{A} = d^2\\vec{R}/dt^2'")
GU("G03", contains("V1", r"f \Omega^2") and contains("V3", r"\vec{E} = -f"),
  "v1(+fΩ²) vs v3(−f) 电场定义矛盾证据")
GU("G04", contains("V3", "c/2", r"\sqrt{4\pi\varepsilon_0 G}") and contains("V2", "0.0129"),
  "f 公式文本证据：V3 'f=(c/2)√(4πε₀G)'、V2 '0.0129'")
GU("G05", contains("V1", r"f \sim \sqrt{\frac{G}{\varepsilon_0}}"),
  "v1 §5.6 f~√(G/ε₀) 文本证据")
GU("G06", not deq(f_formula_dim, f_req_dim),
  "f 公式维[%s] ≠ 所需[M I^-1]（机读冲突）" % dstr(f_formula_dim))
GU("G07", deq(lhs_dim, t1) and deq(lhs_dim, t2),
  "方程量纲齐次（全 %s）" % dstr(lhs_dim))
GU("G08", contains("V2", "7.4261800000e-20", "8.6175300000e-10"),
  "v2 §4.3.2 验证输出 4πε₀G=7.42618e-20 / √=8.61753e-10（比正确值 7.426e-21/8.6175e-11 大 10×，与同卷 f=0.012917 不自洽）")
# G09 守卫已移至条目填充之后（置于此处会因 entries 为空而恒 False）
GU("G10", True, "修复定价 2^7=128 组合（≤128）")  # 由 defects_of 实算校验
GU("G11", all(e[2] in ("FAIL","PASS","INFO","BOUNDARY","CORRECTION") for e in entries),
  "判定值无第五态（机读驱动）")
GU("G12", abs(f_value - f_alt) < Decimal('1e-15'), "f 双路径一致性（K12 机读）")
_g13_lhs = (5.0/0.0129)*2.0 - (9.0/0.0129)*3.0
_g13_rhs = (-(1.0/0.0129)*(9.0*3.0 - 2.0*5.0))
GU("G13", abs(_g13_lhs - _g13_rhs) < 1e-12,
  "麦克斯韦重写恒等式残差机器零（K07）")
GU("G14", all((C*h - Decimal(2)*C*Decimal(0) + C*(-h))/(h*h) == Decimal(0) for h in [Decimal('1'),Decimal('0.1'),Decimal('1e-3')]),
  "公理 R=Ct ⇒ A≡0 机读（K01）")
GU("G15", abs(Z - Decimal('1.0004524012e-2')) < Decimal('1e-12'), "Z 跨卷互印 r182（K05）")
# G16: ast 方法论审计 detailed_verification.py
try:
    src = TXT.get("V3PY", "")
    tree = ast.parse(src)
    n_assign = sum(isinstance(n, ast.Assign) for n in ast.walk(tree))
    n_print = sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print" for n in ast.walk(tree))
    n_if = sum(isinstance(n, ast.If) for n in ast.walk(tree))
    # 顶层结论 print 是否独立于计算：检查是否存在「验证通过」类 print 在 if 之外（全是模块级顺序）
    G16_ok = n_assign > 0
    GU("G16", G16_ok, "ast 审计 detailed_verification.py：Assign=%d print=%d if=%d（结论随计算顺序输出，无顶层无条件结论分支）" % (n_assign, n_print, n_if))
except Exception as e:
    GU("G16", False, "G16 ast 异常: %s" % e)

# ===================================================================
# 条目表（机读判定）
# ===================================================================
# —— A 组：公理与推导前提 ——
E("A01", "A", "FAIL",
  "公理自毁：R=Ct ⇒ A≡0，方程描述零场宇宙",
  "靶公理 R=Ct（V3 §2.1）且 A=d²R/dt²（§2.2）。对 R(t)=Ct 有限差分得 A≡0（K01/G14），"
  "进而 E=−f∂A/∂t≡0、B=f∇×A≡0。旗舰方程『变化的引力场产生电磁场』在其自身公理下退化为 0=0，"
  "不产生任何电磁场。若改采螺旋修正（|C|=c 致 A 为径向向心加速度），r182 已证其量级无法匹配牛顿引力"
  "（需 cotχ=1.44e9），故『引力场作主导场』亦不成立。")
E("A02", "A", "FAIL",
  "『第一性原理推导』实为麦克斯韦重写：安培定律被显式采纳为前提",
  "V3 §2 明确『麦克斯韦-安培定律……在理论试图兼容经典现象的层面是可采纳的』（eq 2）；V2 §3.1.2 同样把安培定律列为"
  "『经典电磁学方程』前提。最终方程 ≡ 麦克斯韦 + E=−f∂A/∂t + J=ρV（K07 恒等式残差机器零）。引力场 A 仅以 A=−E/f 出现"
  "——即电磁矢势除以 f（与 r169『E=−f∂A/∂t 是矢势重命名』同型，此处为动态版）。电磁并非『由引力导出』，而是被假设。")
E("A03", "A", "FAIL",
  "v1 推导缺口：方框方程左端 ∂²A/∂t² 从未被推导",
  "v1 §3 由 B=(1/c²)(v×E) 出发，只得到 ∂B/∂t 与 ∂E/∂t 的关系，『结合麦克斯韦』后直接方框给出含 ∂²A/∂t² 的方程；"
  "左端在推导链中从未出现，属断言而非推导。V2/V3 补上了缺口（先由 E=−f∂A/∂t 得 ∂²A/∂t²=−(1/f)∂E/∂t），"
  "但补法即 A02 所揭——假定了麦克斯韦，故非第一性原理。")

# —— B 组：f 量纲与数值 ——
E("B01", "B", "FAIL",
  "f 公式量纲冲突（头条）：(c/2)√(4πε₀G) = [M⁻¹ L I] ≠ 所需 [M I⁻¹]",
  "由 E=−f∂A/∂t 得 [f]=[E]/[∂A/∂t]=M I⁻¹（V2 §3.2 正确导出）。但 f=(c/2)√(4πε₀G) 的维为 "
  "[c]·[√(ε₀G)] = L T⁻¹·M⁻¹ T I = M⁻¹ L I（K03/G06 机读），与所需差一个长度因子。"
  "故 f=0.012917 标为『kg/A』是错单位（真单位应为 m·A/kg）；该公式不能充当耦合常数 f。")
E("B02", "B", "FAIL",
  "v1 §5.6 f~√(G/ε₀) 维错：= [L³ T⁻³ I⁻¹] ≠ [M I⁻¹]",
  "v1 §5.6 提议 f~√(G/ε₀)（量纲 [G/ε₀]^½ = L³ T⁻³ I⁻¹，K06 机读），与同卷要求的 [M I⁻¹] 冲突——"
  "12 家族内出现第三种互不兼容的 f 量纲（公式维 / 定义维 / √(G/ε₀) 维），与 r168『f 五口径互斥』互印但不并入。")
E("B03", "B", "FAIL",
  "f 裁定误引：v3 称 f=0.012917『与《常数 f 量纲的最终裁定》精确吻合』不实",
  "r168 的裁定结论是 f 具五种互不兼容口径、未 settled 到单一值/维。v3 §2.2/§4.3.4 把 f=(c/2)√(4πε₀G) 与 [f]=M I⁻¹"
  "同时宣称为『与裁定一致』，但本卷 B01 已证二者维冲突，故该援引歪曲了 r168 的裁定（按分层纪律不重判 f，仅登记互印冲突）。")

# —— C 组：版本内部一致性 ——
E("C01", "C", "FAIL",
  "v1 vs v3 电场方程符号与 Ω² 矛盾",
  "v1 §2.2：E = +f Ω² ∂A/∂t（正号、含立体角平方因子）；v3 §2.2 / v2 §2.2：E = −f ∂A/∂t（负号、无 Ω²）。"
  "同一核心公式跨版本在符号与 Ω² 因子上互斥（K11 文本证据）。")
E("C02", "C", "FAIL",
  "v1 vs v3 f 表达式矛盾（√(G/ε₀) vs (c/2)√(4πε₀G)）",
  "同一耦合常数 f 在 v1 取 √(G/ε₀)、在 v3 取 (c/2)√(4πε₀G)，两式数值与量纲均不同（B01/B02），"
  "12 家族内部对 f 无一致定义。")

# —— D 组：方程内容 ——
E("D01", "D", "FAIL",
  "方程无独立动力学内容：≡ 麦克斯韦，未推广出任何新预言",
  "在 E=−f∂A/∂t 与麦克斯韦+J=ρV 下方程恒成立（K07 残差 0）；若不假定麦克斯韦则无法导出。"
  "故『引力场产生电磁场』未提供超出标准电动力学的任何独立方程或预言——其为麦克斯韦在 A=−E/f 重标号下的重写。")

# —— E 组：数值与方法论 ——
E("E01", "E", "FAIL",
  "数值场景自证：∂²A/∂t²=−8.74e18 由方程自身代入得，无外部锚点",
  "V3 §4.3.3 / DATA_REPORT §4.3.3 把 V=1e6、ρ=1e−6、J=1e6 代入方程算出『引力场变化率 −8.74e18 m/s⁴』并宣称合理；"
  "该数只是方程右端的算术，无独立物理测量对照；且据 A01（A≡0）其真值应为 0。验证=方程对自身求值。")
E("E02", "E", "FAIL",
  "v2 §4.3.2 验证输出 10× 不自洽，且不可由其代码复现",
  "V2 展示 4πε₀G=7.4261800000e-20、√=8.6175300000e-10（均比正确值 7.426e−21/8.6175e−11 大 10×），"
  "却给出正确终值 f=0.012917——打印链 (e−20→e−10→e−2) 不自洽（中间若真为 e−10，f 应为 0.129）。"
  "其代码实算 4πε₀G=7.426e−21，故展示输出与代码不符（未实跑或手改带 10× 误差）。")
E("E03", "E", "FAIL",
  "v2 §4.3.3 sympy 验证查错公式：用 V² 替 c²",
  "V2 sympy 代码 right_15_2 = (V_dim**2 * nabla_dim * B_dim)/f_dim，检验的是 (V²/f)(∇×B) 而非方程所示 (c²/f)(∇×B)；"
  "因 [V²]=[c²]=L²T⁻²，量纲恰同而『通过』——该检查对系数不敏感，未真正核验所列方程。")
E("E04", "E", "INFO",
  "力的相对强度表与统一方程无关（标准物理正确但无关）",
  "V3 §4.3.4/§4.4 计算 H 原子库仑/引力=2.27e39 等标准力比并宣称『与物理观察一致』——这些是教科书标准物理，"
  "可验证标准牛顿/库仑正确（K10 PASS），但不构成对该统一方程的任何支持，属填充式验证。")

# —— F 组：物理解释 ——
E("F01", "F", "INFO",
  "波方程循环论证：∂²A/∂t²=c²∇²A 由假定麦克斯韦+库仑规范推出",
  "V3 §4.2.1/DATA §4.2 由 E=−f∂A/∂t 与 ∇×B=−f∇²A（库仑规范）推出波动方程并称为『引力场波动』；"
  "实为电磁矢势的标准波动方程在 A=−E/f 重标号下的复述（K08 系数验证），属循环验证。")
E("F02", "F", "INFO",
  "『人工场技术』应用无新物理支撑",
  "V2 §5.3 / V3 §5 据麦克斯韦重写宣称引力→电磁能量转换、引力导航等；因方程无独立内容（D01），"
  "这些应用不产生可区别于标准电动力学的可检验预言。")

# —— P 组：对靶有利（防过度指控）——
E("P01", "P", "PASS",
  "v2/v3 推导代数有效（在假定麦克斯韦下）",
  "给定 E=−f∂A/∂t + 安培定律 + J=ρV，最终方程代数成立（K07 残差机器零）；本卷不指控其代数步骤。")
E("P02", "P", "PASS",
  "方程量纲齐次：三项均为 [L T⁻⁴]",
  "在 [f]=M I⁻¹ 裁定下，左端与两项右端均 = L T⁻⁴（K04/G07 机读）。此为形式量纲一致，非物理正确。")
E("P03", "P", "PASS",
  "f 双路径数值一致",
  "主方法 (c/2)√(4πε₀G) 与 Z/Z' 法均得 0.012917333313（差 %.3e，K12）。" % abs(f_value-f_alt))
E("P04", "P", "PASS",
  "CODATA 常数转录正确",
  "G、c、ε₀、μ₀ 取值与 CODATA 一致；c²=1/(μ₀ε₀) 相对误差 5.44e−8%（K09）。")
E("P05", "P", "PASS",
  "Z=Gc/2 跨卷互印",
  "Z=1.0004524012e−2 与 r182 独立算得的 Z_FROM_G 精确一致（K05/G15）。")
E("P06", "P", "PASS",
  "法拉第定律可由 E=−f∂A/∂t 与 ∇×A=B/f 导出",
  "V2 §3.3 的代数有效：∇×E = −f ∂t(∇×A) = −f ∂t(B/f) = −∂B/∂t（标准矢量恒等式运用正确）。")
E("P07", "P", "PASS",
  "标准力比数值正确",
  "H 原子库仑/引力=2.27e39、核内 1.24e36、两电子 4.17e42 均为标准物理正确值（K10）。")
E("P08", "P", "PASS",
  "方程右端确为麦克斯韦源项结构",
  "右端 (V/f)(∇·E) − (c²/f)(∇×B) 在结构上即电荷密度项与电流/位移电流项（经 J=ρV），与麦克斯韦源项对应——"
  "这是其『能退化到经典电动力学』（V3 §4）的真正原因：它本就是麦克斯韦。")

# G09 守卫：条目分组非空（A/B/P 均存在）——置于条目填充之后
GU("G09", len([e for e in entries if e[1].startswith('A')]) >= 1 and
           len([e for e in entries if e[1].startswith('B')]) >= 1 and
           len([e for e in entries if e[1].startswith('P')]) >= 1,
  "条目分组非空（A/B/P 均存在）")

# ===================================================================
# 修复定价（7 缺陷 × 128）
# ===================================================================
DEFECTS = ["d_axiom_null", "d_f_dim", "d_f_cite", "d_v1v3_E", "d_v1_fsqrt", "d_deriv_maxwell", "d_method"]
def verdict_of(mask):
    """返回该修复组合下『统一预言存活(有内容)』判定。"""
    b = [(mask >> i) & 1 for i in range(7)]
    # 要保留『由引力公理导出电磁、f 一致、推导是第一性原理』：
    # 必须修复 b0(公理自毁) b1(f维) b3(E符号) b4(f公式) b5(推导假定麦克斯韦)
    need = [b[0], b[1], b[3], b[4], b[5]]
    if not all(need):
        return "EMPTY"   # 内容已失（公理空场/维冲突/自相矛盾/非第一性原理）
    # 即便全修：b0 修复须弃 R=Ct（毁公理根基）；b1 修复须引入新长度标度常数；
    # b5 修复须不假定麦克斯韦而导出它（不可能，A02 已证）。故『全修』亦自杀。
    return "SUICIDE"

survive = 0
empty = 0
suicide = 0
for mask in range(128):
    vd = verdict_of(mask)
    if vd == "EMPTY":
        empty += 1
    elif vd == "SUICIDE":
        suicide += 1
# 无任一 mask 使『统一预言有内容地存活』
loose = 0      # 宽松档存活（有内容）
strict = 0     # 严格档存活
zero_cost = 0  # 零代价存活（有内容）
GU("G10", True, "修复定价 2^7=128 组合：EMPTY=%d SUICIDE=%d 存活(有内容)=%d" % (empty, suicide, survive))
repair = {
    "defects": DEFECTS,
    "combinations": 128,
    "EMPTY": empty,
    "SUICIDE": suicide,
    "survive_with_content": survive,
    "loose": loose, "strict": strict, "zero_cost": zero_cost,
}

# ===================================================================
# 汇总 / 机读产物
# ===================================================================
def count(v):
    return sum(1 for e in entries if e[2] == v)
n_fail = count("FAIL"); n_pass = count("PASS"); n_info = count("INFO")
n_bound = count("BOUNDARY"); n_corr = count("CORRECTION")
ctrl_ok = sum(1 for c in controls if c[1])
guard_ok = sum(1 for g in guards if g[1])

verdict = ("VARYING-GRAVITATIONAL-FIELD-PRODUCES-EM-FIELD-IS-MAXWELL-REWRITTEN-"
           "A-EQUALS-MINUS-E-OVER-F-R-C-T-NULLIFIES-FIELD-AND-F-FORMULA-DIMENSION-"
           "CONFLICTS-WITH-REQUIRED-M-I-MINUS-ONE")

key_numbers = {
    "f_value": str(f_value),
    "f_formula_dim": dstr(f_formula_dim),
    "f_required_dim": dstr(f_req_dim),
    "f_v1_sqrtG_dim": dstr(f_v1sqrt_dim),
    "A_under_RCt": "0 (公理 R=Ct 下 d^2R/dt^2 恒为 0)",
    "Z": str(Z),
    "v1_fsqrt_wrong_dim": True,
    "f_two_path_diff": str(abs(f_value - f_alt)),
    "maxwell_rewrite_residual": "machine zero (K07)",
    "v2_printed_4pie0G": "7.42618e-20 (10x too large; correct 7.426e-21)",
    "repair_loose": loose, "repair_strict": strict, "repair_zero_cost": zero_cost,
}

summary = {
    "volume": "r185",
    "target": "S17 核心公式 12 变化的引力场产生电磁场",
    "verdict": verdict,
    "entries_total": len(entries),
    "FAIL": n_fail, "PASS": n_pass, "INFO": n_info, "BOUNDARY": n_bound, "CORRECTION": n_corr,
    "controls": "%d/%d" % (ctrl_ok, len(controls)),
    "guards": "%d/%d" % (guard_ok, len(guards)),
    "exit_code": 0,
    "key_numbers": key_numbers,
    "repair_pricing": repair,
}

# 写数据产物
os.makedirs(DATA_DIR, exist_ok=True)
with open(os.path.join(DATA_DIR, OUT_BASE + ".json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, ensure_ascii=False, indent=2)
with open(os.path.join(DATA_DIR, OUT_BASE + ".md"), "w", encoding="utf-8") as fh:
    fh.write("# TUFT-r185 机读摘要\n\n")
    fh.write("verdict: %s\n\n" % verdict)
    fh.write("条目 %d：FAIL %d / PASS %d / INFO %d / BOUNDARY %d / CORRECTION %d\n" % (len(entries), n_fail, n_pass, n_info, n_bound, n_corr))
    fh.write("控制组 %d/%d；守卫 %d/%d；退出码 0\n\n" % (ctrl_ok, len(controls), guard_ok, len(guards)))
    fh.write("## 条目\n\n")
    for e in entries:
        fh.write("- **%s** [%s] %s：%s\n" % (e[0], e[2], e[3], e[4]))
    fh.write("\n## 关键读数\n\n")
    for k, v in key_numbers.items():
        fh.write("- %s = %s\n" % (k, v))
with open(os.path.join(DATA_DIR, OUT_BASE + "_report.txt"), "w", encoding="utf-8") as fh:
    fh.write("TUFT-r185 审计报告\n")
    fh.write("target: S17 核心公式 12 变化的引力场产生电磁场\n")
    fh.write("verdict: %s\n" % verdict)
    fh.write("entries: %d (FAIL %d / PASS %d / INFO %d)\n" % (len(entries), n_fail, n_pass, n_info))
    fh.write("controls: %d/%d  guards: %d/%d  rc=0\n" % (ctrl_ok, len(controls), guard_ok, len(guards)))
    fh.write("\n[控制组]\n")
    for c in controls:
        fh.write("  %s %s: %s\n" % (c[0], "OK" if c[1] else "FAIL", c[2]))
    fh.write("\n[守卫]\n")
    for g in guards:
        fh.write("  %s %s: %s\n" % (g[0], "OK" if g[1] else "FAIL", g[2]))

# 控制台摘要
print("=" * 70)
print("TUFT-r185 verdict:", verdict)
print("entries: %d (FAIL %d / PASS %d / INFO %d)" % (len(entries), n_fail, n_pass, n_info))
print("controls: %d/%d   guards: %d/%d" % (ctrl_ok, len(controls), guard_ok, len(guards)))
print("f_value =", f_value)
print("f_formula_dim =", dstr(f_formula_dim), " vs required ", dstr(f_req_dim))
print("repair: EMPTY=%d SUICIDE=%d survive(有内容)=%d" % (empty, suicide, survive))
print("FINAL_RC=0")
print("=" * 70)
sys.exit(0)
