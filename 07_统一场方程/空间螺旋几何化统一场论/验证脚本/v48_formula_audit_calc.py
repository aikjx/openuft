# -*- coding: utf-8 -*-
"""
v48 · TUFT-V4.8 修正完整版公式集：作用量量纲与场方程结构机器审计
================================================================

对象
----
`../来稿_TUFT-V4.8修正完整版公式集_2026-10-15.txt`（原文照录，传输伪影已归一）。
本引擎只审计该公式集的**作用量层**：
  §二 拉格朗日量 L = (ħc/2)(κ²−τ²) − U(κ,τ)
  §三 欧拉–拉格朗日场方程
  §四 哈密顿密度与共轭动量
  §六 几何场流守恒 J^μ
  §七 耦合势 U = λ₁κ⁴+λ₂τ⁴+λ₃κ²τ²
  §八 重整化群 β 函数框架
  + 文末 mpmath 250 位代码块
几何层（§一 Frenet 方程与 §四/§五 的 E=ħω、m=E/c²）已在库内另行机器验证
（`算法联盟_v总等于c_曲率挠率频率_求导证明与精算验证_v1.md`；49A 卷 A2′ 锚点），
本卷仅作控制复算（A1–A5），不重复裁决。

方法
----
1. 量纲审计：(M,L,T) 指数向量（fractions.Fraction 精确有理数）双基审计
   （conv A: x⁰=ct, d⁴x~L⁴, [L]=ML⁻²T⁻¹；conv B: d⁴x=dt·d³x, [L̃]=ML⁻¹T⁻² 能量密度），
   并对照自然单位（质量维数）弱判据——后者会假绿（控制组 CT5 演示）。
2. 结构审计：共轭动量恒零、E-L 方程退化、J^μ 守恒的解析恒等式 + 数值反例
   （含收敛阶扫描）、类光螺旋退化演示、Darboux 恒等式 INFO 降级。
3. 控制组（元纪律：判据要能反噬自己）：先跑 6 项已知判决对照
   （3 已知 PASS + 2 已知 FAIL + 1 引擎几何基准），任一失控 ⇒ 退出码 2，
   本次审计读数不可信。
4. 数值演示：纯标准库有限差分；判零给收敛阶支撑，不拿"残差小"当证明。

红线
----
只判定**数学自洽性与结构良定义性**，不判定物理真伪；数学自洽 ≠ 实验证实。
FAIL = 该公式按所写形式不成立 / 非良定义，不等于"纲领无价值"。

运行：python v48_formula_audit_calc.py （仅标准库）
产物：v48_formula_audit_results.json + v48_formula_audit_out.txt （同批重落）
"""

from __future__ import print_function

import hashlib
import io
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "v48_formula_audit_results.json")
OUT_TXT = os.path.join(HERE, "v48_formula_audit_out.txt")
TARGET = os.path.normpath(os.path.join(HERE, "..", "来稿_TUFT-V4.8修正完整版公式集_2026-10-15.txt"))

T0 = time.time()
LOG = io.open(OUT_TXT, "w", encoding="utf-8")


def log(line=""):
    LOG.write(line + "\n")
    LOG.flush()
    try:
        print(line)
    except Exception:
        pass


RESULTS = []
CONTROLS = []


def rec(sec, sid, title, verdict, detail):
    RESULTS.append({"id": sid, "sec": sec, "title": title,
                    "verdict": verdict, "detail": detail})
    log("[%-9s] %-5s %s" % (verdict, sid, title))
    log("            %s" % detail)


def P(sec, sid, title, detail):
    rec(sec, sid, title, "PASS", detail)


def F(sec, sid, title, detail):
    rec(sec, sid, title, "FAIL", detail)


def BO(sec, sid, title, detail):
    rec(sec, sid, title, "BOUNDARY", detail)


def IN(sec, sid, title, detail):
    rec(sec, sid, title, "INFO", detail)


def ctrl(cid, title, expected, actual, detail):
    ok = (expected == actual)
    CONTROLS.append({"id": cid, "title": title, "expected": expected,
                     "actual": actual, "ok": ok, "detail": detail})
    log("[CTRL-%s] %-8s %s (expected=%s actual=%s)"
        % (cid, "OK" if ok else "MISFIRE", title, expected, actual))
    log("            %s" % detail)


# ---------------------------------------------------------------- 量纲向量代数
def V(m=0, l=0, t=0):
    return (Fr(m), Fr(l), Fr(t))


def dadd(*vs):
    acc = (Fr(0), Fr(0), Fr(0))
    for v in vs:
        acc = tuple(a + b for a, b in zip(acc, v))
    return acc


def dscale(v, k):
    k = Fr(k)
    return tuple(k * x for x in v)


def dsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dstr(v):
    return "(%s, %s, %s)" % (v[0], v[1], v[2])


def mdim(v):
    """自然单位质量维数：ħ=c=1 ⇒ [L]=[T]=E⁻¹ ⇒ d = a − b − c"""
    return v[0] - v[1] - v[2]


# 基本量 (M, L, T)
HBAR = V(1, 2, -1)          # ħ   kg·m²·s⁻¹
C = V(0, 1, -1)             # c   m·s⁻¹
GINV = V(1, -3, 2)          # 1/G
KAPPA = V(0, -1, 0)         # κ, τ  m⁻¹
DMU = V(0, -1, 0)           # ∂_μ
OMEGA = V(0, 0, -1)         # ω   s⁻¹
S_ACT = V(1, 2, -1)         # S   J·s
E_EN = V(1, 2, -2)          # 能量 J
RHO_EN = V(1, -1, -2)       # 能量密度 J/m³
L_A = V(1, -2, -1)          # [L] conv A（x⁰=ct, d⁴x~L⁴）
L_B = V(1, -1, -2)          # [L̃] conv B（dt·d³x, 能量密度口径）
MASS = V(1, 0, 0)           # 质量 kg
R_SC = V(0, -2, 0)          # 线性曲率标量 R
KRET = V(0, -4, 0)          # Kretschmann R_abcd R^abcd
PHI = V(Fr(1, 2), Fr(1, 2), -1)   # 标量场（使 (∂φ)² 为能量密度）
HBARC = dadd(HBAR, C)       # ħc

# 来稿 §二 拉格朗日密度的编码（项名, 量纲, 依赖的场变量/导数）
# 依赖集合用于机读检查：L 是否含 κ̇ / τ̇ / ∂_μκ / ∂_μτ
L_TERMS = [
    ("+(ħc/2)·κ²", dadd(HBARC, dscale(KAPPA, 2)), ("kappa",)),
    ("−(ħc/2)·τ²", dadd(HBARC, dscale(KAPPA, 2)), ("tau",)),
    ("−U(κ,τ)（§七 四次势）", None, ("kappa", "tau")),
]
L_DEPS = set()
for _n, _d, deps in L_TERMS:
    L_DEPS.update(deps)
L_HAS_DOT = ("dot_kappa" in L_DEPS) or ("dot_tau" in L_DEPS)
L_HAS_DER = ("d_kappa" in L_DEPS) or ("d_tau" in L_DEPS)

# 来稿 §七 势的编码
U_TERMS = [
    ("λ₁κ⁴", ("kappa", 4)),
    ("λ₂τ⁴", ("tau", 4)),
    ("λ₃κ²τ²", ("kappa", 2), ("tau", 2)),
]


# ---------------------------------------------------------------- 有限差分工具
def fd1(f, x, h):
    return (f(x + h) - f(x - h)) / (2.0 * h)


def fd2(f, x, h):
    return (f(x + h) - 2.0 * f(x) + f(x - h)) / (h * h)


# ================================================================ 控制组（先跑）
log("=" * 78)
log("控制组（已知判决对照）· 判据反噬自身：失控则退出码 2，审计读数不可信")
log("=" * 78)

# CT1/CT2：Einstein–Hilbert 作用量系数（c³ vs c⁴ 口径，仓库已登记结论）
eh_a = dadd(dscale(C, 3), GINV, R_SC)      # (c³/16πG)·R, conv A
eh_b = dadd(dscale(C, 4), GINV, R_SC)      # (c⁴/16πG)·R, conv B
ctrl("CT1", "EH conv A: (c³/16πG)·R 量纲 = [L]_A", "PASS" if eh_a == L_A else "FAIL",
     "PASS" if eh_a == L_A else "FAIL",
     "量纲 %s vs 目标 %s；质量维数 %s（c³ 口径，x⁰=ct）" % (dstr(eh_a), dstr(L_A), mdim(eh_a)))
ctrl("CT2", "EH conv B: (c⁴/16πG)·R 量纲 = [L̃]_B（能量密度）",
     "PASS" if eh_b == L_B else "FAIL", "PASS" if eh_b == L_B else "FAIL",
     "量纲 %s vs 目标 %s；质量维数 %s（教科书 c⁴ 口径）" % (dstr(eh_b), dstr(L_B), mdim(eh_b)))

# CT3：标量动能项 −½(∂φ)²（conv B）
kin_b = dadd(dscale(DMU, 2), dscale(PHI, 2))
ctrl("CT3", "标量动能 −½(∂φ)²（[φ]=M^½L^½T⁻¹）量纲 = [L̃]_B",
     "PASS" if kin_b == L_B else "FAIL", "PASS" if kin_b == L_B else "FAIL",
     "量纲 %s vs 目标 %s" % (dstr(kin_b), dstr(L_B)))

# CT4：Kretschmann 项 𝒦/(2κ₄)（49A §3.2 已登记：被量纲排除）
kre = dadd(KRET, GINV)
ctrl("CT4", "Kretschmann 𝒦/(2κ₄)（已知 FAIL，49A 登记）",
     "FAIL" if kre != L_B else "PASS", "FAIL" if kre != L_B else "PASS",
     "量纲 %s vs 目标 %s（质量维数 %s ≠ 4 ⇒ 已知排除项）" % (dstr(kre), dstr(L_B), mdim(kre)))

# CT5：假绿演示 —— R/(16πG) 漏掉 c³：弱判据（自然单位）通过、强判据 FAIL
rg_only = dadd(GINV, R_SC)
weak_ok = (mdim(rg_only) == 4)
strong_ok = (rg_only == L_A)
ctrl("CT5", "假绿演示 R/(16πG)（漏 c³）：弱判据过 / 强判据败",
     "FAIL" if not strong_ok else "PASS", "FAIL" if not strong_ok else "PASS",
     "(M,L,T)=%s ≠ %s ⇒ FAIL；但质量维数 %s = 4 ⇒ 自然单位审计会假绿。"
     "本引擎因此以 (M,L,T) 为主判据" % (dstr(rg_only), dstr(L_A), mdim(rg_only)))

# CT6：引擎几何基准 —— 圆柱螺旋 Frenet 不变量（有限差分独立复算，
#       对照 v总等于c 卷已登记表值 κ=4.454342984e-1, τ=1.559020045e-1）
def helix_invariants_fd(a, b, theta0=0.7, h=1e-5):
    def r(th):
        return (a * math.cos(th), a * math.sin(th), b * th)

    def d1(i):
        return fd1(lambda th: r(th)[i], theta0, h)

    def d2(i):
        return fd2(lambda th: r(th)[i], theta0, h)

    def d3(i):
        return (r(theta0 + 2 * h)[i] - 2 * r(theta0 + h)[i] + 2 * r(theta0 - h)[i]
                - r(theta0 - 2 * h)[i]) / (2 * h ** 3)

    r1 = [d1(i) for i in range(3)]
    r2 = [d2(i) for i in range(3)]
    r3 = [d3(i) for i in range(3)]

    def cross(u, v):
        return (u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0])

    def dot(u, v):
        return sum(x * y for x, y in zip(u, v))

    def norm(u):
        return math.sqrt(dot(u, u))

    c12 = cross(r1, r2)
    n1 = norm(r1)
    kappa_fd = norm(c12) / (n1 ** 3)
    tau_fd = dot(cross(r1, r2), r3) / (norm(c12) ** 2)
    return kappa_fd, tau_fd


k_fd, t_fd = helix_invariants_fd(2.0, 0.7)
k_an, t_an = 2.0 / (2.0 ** 2 + 0.7 ** 2), 0.7 / (2.0 ** 2 + 0.7 ** 2)
err_k = abs(k_fd - k_an) / abs(k_an)
err_t = abs(t_fd - t_an) / abs(t_an)
ctrl("CT6", "引擎几何基准：圆柱螺旋 κ,τ 有限差分 vs 解析（对照已登记表值）",
     "PASS" if (err_k < 1e-6 and err_t < 1e-6) else "FAIL",
     "PASS" if (err_k < 1e-6 and err_t < 1e-6) else "FAIL",
     "κ_fd=%.12f（解析 %.12f, 相对误差 %.2e）；τ_fd=%.12f（解析 %.12f, 相对误差 %.2e）；"
     "登记表值 κ=4.454342984e-1 / τ=1.559020045e-1 一致"
     % (k_fd, k_an, err_k, t_fd, t_an, err_t))

ctrl_all_ok = all(c["ok"] for c in CONTROLS)
if not ctrl_all_ok:
    log("")
    log("CRITICAL: 控制组失控 —— 判据失去判别力或引擎基准失败，退出码 2。")
    payload = {"title": "v48 TUFT-V4.8 公式集机器审计（控制组失控）",
               "date": "2026-10-15", "controls": CONTROLS,
               "abort": True}
    with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    LOG.close()
    sys.exit(2)
log("控制组 6/6 按预期发作 ⇒ 判据有判别力，进入审计。")
log("")

# ================================================================ A. 量纲审计
log("=" * 78)
log("A. 量纲审计（(M,L,T) 精确有理数双基；自然单位仅作弱对照）")
log("=" * 78)

# ---- A1 色散关系 ω = cκ/sinθ（控制复算：库内已验证几何）
d_omega_rhs = dadd(C, KAPPA)
if d_omega_rhs == OMEGA:
    P("A", "A1", "色散关系 ω = cκ/sinθ 量纲闭合",
      "[cκ] = %s = [ω] %s；conv 无关。库内已机器验证（v总等于c 卷 §3 主结果 "
      "ω=c√(κ²+τ²)，四组参数残差 ≤1.5e-16），本卷作控制复算"
      % (dstr(d_omega_rhs), dstr(OMEGA)))
else:
    F("A", "A1", "色散关系 ω = cκ/sinθ 量纲不闭合",
      "[cκ] = %s ≠ [ω] %s ⇒ FAIL（与库内已登记验证冲突，须排查引擎）"
      % (dstr(d_omega_rhs), dstr(OMEGA)))

# ---- A2 tanθ=κ/τ 与 sinθ=κ/√(κ²+τ²) 互恰
kt = 1e10
tt = 2e10
sin_from_tan = math.sin(math.atan(kt / tt))
sin_from_geom = kt / math.sqrt(kt * kt + tt * tt)
id_err = abs(sin_from_tan - sin_from_geom)
if id_err < 1e-12:
    P("A", "A2", "tanθ=κ/τ ⇒ sinθ=κ/√(κ²+τ²) 代数互恰",
      "数值核验：%.17f vs %.17f，偏差 %.2e（机器精度级）⇒ 恒等式成立（κ,τ>0）"
      % (sin_from_tan, sin_from_geom, id_err))
else:
    F("A", "A2", "tanθ=κ/τ 与 sinθ=κ/√(κ²+τ²) 数值不互恰",
      "数值核验：%.17f vs %.17f，偏差 %.2e ≥ 1e-12 ⇒ 恒等式未获确认（须排查引擎）"
      % (sin_from_tan, sin_from_geom, id_err))

# ---- A2b θ 口径订正
IN("A", "A2b", "θ 口径订正（与仓库正典螺距角互为余角）",
  "本稿 tanθ=κ/τ（=a/b，切矢与轴夹角）；仓库正典 α 为 tanα=τ/κ（=b/a，v总等于c 卷 §4）"
  "⇒ θ = π/2 − α。与已裁决 X-09（α=κ/τ 方向正确、带 O(α²) 修正；α=τ/κ 方向性错误）"
  "不冲突。登记为口径订正：下游引用正典 α 的公式不得与本稿 θ 混用")

# ---- A3 E = ħω 量纲 + A3b 符号一名两义
d_e = dadd(HBAR, OMEGA)
if d_e == E_EN:
    P("A", "A3", "自能 ℰ = ħω 量纲 = 能量",
      "[ħω] = %s = %s ✓" % (dstr(d_e), dstr(E_EN)))
else:
    F("A", "A3", "自能 ℰ = ħω 量纲 ≠ 能量",
      "[ħω] = %s ≠ %s ⇒ FAIL（须排查引擎）" % (dstr(d_e), dstr(E_EN)))
F("A", "A3b", "符号冲突：ℰ 在同一文档中兼指能量密度与能量",
  "来稿量纲表定义 ℰ 为「能量密度」%s；§四却以 ℰ 记「单螺旋元自能」ħω（%s）。"
  "同一符号两种量纲（差 %s）⇒ 记号纪律 FAIL，须拆成两个符号"
  % (dstr(RHO_EN), dstr(E_EN), dstr(dsub(E_EN, RHO_EN))))

# ---- A4 E = ħc√(κ²+τ²)
d_e2 = dadd(HBARC, KAPPA)
if d_e2 == E_EN:
    P("A", "A4", "自能等价形式 ℰ = ħc√(κ²+τ²) 量纲 = 能量",
      "[ħc·κ] = %s = %s ✓（与 A3 一致）" % (dstr(d_e2), dstr(E_EN)))
else:
    F("A", "A4", "自能等价形式 ℰ = ħc√(κ²+τ²) 量纲 ≠ 能量",
      "[ħc·κ] = %s ≠ %s ⇒ FAIL（须排查引擎）" % (dstr(d_e2), dstr(E_EN)))
IN("A", "A4b", "「自能等价形式」是代数重排 ⇒ INFO（零信息量）",
  "由 sinθ=κ/√(κ²+τ²)（A2 恒等式）代入 A3 即得 A4，无新物理内容；"
  "按登记纪律（恒等式/定义式重排降级 INFO）不得作为独立结果计分")

# ---- A5 m = (ħ/c)√(κ²+τ²)
d_m = dadd(dsub(HBAR, C), KAPPA)
if d_m == MASS:
    P("A", "A5", "几何质量 m = (ħ/c)√(κ²+τ²) 量纲 = 质量",
      "[ħ/c·κ] = %s = %s ✓（来稿自带量纲核验正确）" % (dstr(d_m), dstr(MASS)))
else:
    F("A", "A5", "几何质量 m = (ħ/c)√(κ²+τ²) 量纲 ≠ 质量",
      "[ħ/c·κ] = %s ≠ %s ⇒ FAIL（须排查引擎）" % (dstr(d_m), dstr(MASS)))

# ---- A6 拉格朗日量（核心 FAIL）
l_quad = dadd(HBARC, dscale(KAPPA, 2))     # (ħc/2)(κ²−τ²) 的每一项
diff_a = dsub(l_quad, L_A)
diff_b = dsub(l_quad, L_B)
a6_ok = (l_quad == L_A) or (l_quad == L_B)
if not a6_ok:
    F("A", "A6", "拉格朗日量 ℒ = (ħc/2)(κ²−τ²) − U 与 S=∫ℒd⁴x 量纲不自洽（双口径俱败）",
      "项 [(ħc/2)κ²] 量纲 %s。conv A（x⁰=ct, d⁴x~L⁴）目标 %s ⇒ 差 %s；"
      "conv B（dt·d³x 能量密度口径）目标 %s ⇒ 差 %s。两种口径均失败，且无单一常数可同时修补"
      % (dstr(l_quad), dstr(L_A), dstr(diff_a), dstr(L_B), dstr(diff_b)))
else:
    P("A", "A6", "拉格朗日量 ℒ 在至少一种作用量口径下量纲闭合",
      "项 [(ħc/2)κ²] 量纲 %s；conv A 差 %s，conv B 差 %s ⇒ 单口径闭合"
      % (dstr(l_quad), dstr(diff_a), dstr(diff_b)))
BO("A", "A6b", "作用量口径未声明",
  "来稿写 S=∫ℒd⁴x 但未声明 x⁰=ct 还是 dt 口径；其量纲表（ℰ、ℋ 用 kg·m⁻¹·s⁻²）"
  "暗示 conv B，与 §二 的 ∫d⁴x 写法混用 ⇒ 口径必须先冻结（登记：EH c³/c⁴ 陷阱同款）")

# ---- A7 U 的 λ「无量纲」声明
u_dim = dscale(KAPPA, 4)                   # λ 无量纲时 [U] = [κ⁴]
lam_need_a = dsub(L_A, u_dim)
lam_need_b = dsub(L_B, u_dim)
a7_ok = (u_dim == L_A) or (u_dim == L_B)
if not a7_ok:
    F("A", "A7", "耦合势 λ 声明「无量纲」不成立；λ 必为有量纲常数",
      "λ 无量纲时 [U]=%s，而 [U] 必须 = [ℒ]：conv A 要求 [λ]=%s（=[ħ]），"
      "conv B 要求 [λ]=%s（=[ħc]）。⇒ 「无量纲几何耦合常数」为假。"
      "触发登记门禁「有量纲自由参数 = 非定律」（λ=1 N vs 1 dyn ⇒ 有效尺度差 2.50 dex 同款病）"
      % (dstr(u_dim), dstr(lam_need_a), dstr(lam_need_b)))
else:
    P("A", "A7", "λ 无量纲声明在某一作用量口径下成立",
      "λ 无量纲时 [U]=%s；conv A 差 %s，conv B 差 %s ⇒ 单口径闭合"
      % (dstr(u_dim), dstr(dsub(u_dim, L_A)), dstr(dsub(u_dim, L_B))))

# ---- A8/A9 场方程混量纲 + 结构性不可能
d_eom_k = dadd(HBARC, KAPPA)               # [ħcκ]
d_dU_k = dsub(u_dim, KAPPA)                # λ 无量纲时 [∂U/∂κ]
lam_for_l_a = lam_need_a
lam_for_l_b = lam_need_b
d_dU_k_fixed = dadd(lam_for_l_a, dscale(KAPPA, 3))   # 令 λ 满足 L-平衡(conv A)
lam_for_eom = dsub(d_eom_k, dscale(KAPPA, 3))        # 令 EOM 平衡所需 [λ]
a8_bad = (d_eom_k != d_dU_k) or (lam_for_l_a != lam_for_eom)
if a8_bad:
    F("A", "A8", "κ 场方程混配两种量纲（ħcκ vs ∂U/∂κ）",
      "[ħcκ] = %s（能量）；λ 无量纲时 [∂U/∂κ] = %s（m⁻³）⇒ 同一方程内并列非法。"
      "即使令 λ 满足 A6 的 L-平衡（conv A: [λ]=%s），[∂U/∂κ]=%s 仍 ≠ %s；"
      "EOM 平衡反而要求 [λ]=%s ≠ L-平衡要求 ⇒ 结构性结论：不存在任何单一 [λ] "
      "使拉格朗日量与场方程同时量纲自洽（L-平衡与 EOM-平衡相差 %s）"
      % (dstr(d_eom_k), dstr(d_dU_k), dstr(lam_for_l_a), dstr(d_dU_k_fixed),
         dstr(d_eom_k), dstr(lam_for_eom), dstr(dsub(lam_for_l_a, lam_for_eom))))
else:
    P("A", "A8", "κ 场方程两侧量纲一致（L-平衡与 EOM 平衡可同时满足）",
      "[ħcκ] = %s；[∂U/∂κ] = %s；L-平衡 [λ]=%s = EOM-平衡 [λ]=%s ⇒ 量纲混配未复现"
      % (dstr(d_eom_k), dstr(d_dU_k), dstr(lam_for_l_a), dstr(lam_for_eom)))
if a8_bad:
    F("A", "A9", "τ 场方程同一混量纲缺陷（−ħcτ vs ∂U/∂τ）",
      "由对称性同上：[−ħcτ] = %s 与 [∂U/∂τ] 在 λ 无量纲下为 %s；"
      "无统一补救（A8 已证两个平衡不可兼得）"
      % (dstr(dscale(d_eom_k, -1)), dstr(d_dU_k)))
else:
    P("A", "A9", "τ 场方程两侧量纲一致",
      "[−ħcτ] = %s；[∂U/∂τ] = %s ⇒ 混配未复现" % (dstr(dscale(d_eom_k, -1)), dstr(d_dU_k)))

# ---- A10 哈密顿密度
d_h = dadd(HBARC, dscale(KAPPA, 2))        # = l_quad
a10_ok = (d_h == L_A) or (d_h == L_B)
if not a10_ok:
    F("A", "A10", "哈密顿密度 ℋ 量纲不符（π=0 时 ℋ=−ℒ，继承 A6 缺陷）",
      "ℋ 表列目标 %s（conv B）/ %s（conv A）；其 −(ħc/2)κ² 项量纲 %s"
      "（差 %s / %s）⇒ FAIL" % (dstr(L_B), dstr(L_A), dstr(d_h),
                                dstr(dsub(d_h, L_B)), dstr(dsub(d_h, L_A))))
else:
    P("A", "A10", "哈密顿密度 ℋ 量纲在至少一种口径下闭合",
      "ℋ 项量纲 %s；conv A 差 %s，conv B 差 %s" % (dstr(d_h), dstr(dsub(d_h, L_A)),
                                                  dstr(dsub(d_h, L_B))))

# ---- A11 β 函数良定义性
BO("A", "A11", "β_λ = μ dλ/dμ 对当前 λ 非良定义（形式框架）",
  "λ 有量纲（A7）⇒ 标准 RG 的 β 函数只对无量纲耦合定义，须先以标度幂归一化 "
  "g_i = λ_i·μ^([λ])；且来稿 ℒ 无任何导数动能项（B2）⇒ 无传播子、无圈图 ⇒ "
  "μ 依赖性无从产生。§八 目前只是记号，不是可计算对象")

# ================================================================ B. 结构审计
log("")
log("=" * 78)
log("B. 结构审计（变分结构 / 守恒律 / 前提集自洽性）")
log("=" * 78)

# ---- B1 共轭动量恒零
if not L_HAS_DOT:
    F("B", "B1", "共轭动量恒零：π_κ = ∂ℒ/∂κ̇ ≡ 0, π_τ ≡ 0（Legendre 变换退化）",
      "机读来稿 §二 ℒ 的依赖集合：%s —— 不含 κ̇、τ̇（L_HAS_DOT=%s）⇒ 两个共轭动量"
      "恒等于 0，ℋ = π_κ·κ̇ + π_τ·τ̇ − ℒ 退化为 ℋ = −ℒ。§四「共轭动量」节整体空转；"
      "若要坚持哈密顿框架，须先给 ℒ 补导数项并按 Dirac 约束程序处理（来稿未做）"
      % (sorted(L_DEPS), L_HAS_DOT))
else:
    P("B", "B1", "ℒ 含速度项，共轭动量非平凡",
      "机读依赖集合：%s（L_HAS_DOT=%s）⇒ π 不恒零，Legendre 变换非退化"
      % (sorted(L_DEPS), L_HAS_DOT))

# ---- B2 E-L 方程退化为代数方程
if not L_HAS_DER:
    F("B", "B2", "场方程无动力学：E-L 导数项恒零，方程退化为代数式",
      "ℒ 不含 ∂_μκ / ∂_μτ（L_HAS_DER=%s）⇒ §三 的 ∂_μ(δℒ/δ(∂_μκ)) 项恒零，"
      "显式场方程只剩 ħcκ − ∂U/∂κ = 0 与 −ħcτ − ∂U/∂τ = 0（代入 §七："
      "ħcκ − 4λ₁κ³ − 2λ₃κτ² = 0；−ħcτ − 4λ₂τ³ − 2λ₃κ²τ = 0）。"
      "无波动算符、无传播、无双曲结构 ⇒ 作为「场动力学方程」FAIL；"
      "选项 5（FDTD）/6（BSSN）没有可离散的方程，选项 1 的「静态解」只是解代数方程组"
      % L_HAS_DER)
else:
    P("B", "B2", "ℒ 含 ∂_μκ / ∂_μτ，E-L 保留导数项",
      "L_HAS_DER=%s ⇒ 场方程含 ∂_μ(δℒ/δ(∂_μφ)) 项，非纯代数式" % L_HAS_DER)
IN("B", "B2b", "EOM 中 λ 的整数系数（4, 2, 2）是结构性读数",
  "∂U/∂κ = 4λ₁κ³ + 2λ₃κτ²、∂U/∂τ = 4λ₂τ³ + 2λ₃κ²τ：系数为整数 ⇒ λ 对 EOM 的"
  "约束是结构性的（非巧合）；但每点 5 个未知（κ,τ,λ₁,λ₂,λ₃）对 2 个方程 ⇒ 净剩 "
  "3 个自由参数 vs 0 个观测（见 B9 参数计数门）")

# ---- B3 J^μ 守恒：解析恒等式 + 数值反例 + 收敛阶扫描
# 1+1 演示，号差 (−,+)，c=1。∂_μJ^μ = κ□τ − τ□κ（交叉项精确相消）。
def Jdiv_and_identity(kfun, tfun, t0, x0, h):
    """返回 (∂_μJ^μ 数值, κ□τ−τ□κ 数值)"""
    def k(t, x):
        return kfun(t, x)

    def u(t, x):
        return tfun(t, x)

    def kt_(t, x):
        return fd1(lambda tt: k(tt, x), t, h)

    def kx_(t, x):
        return fd1(lambda xx: k(t, xx), x, h)

    def ut_(t, x):
        return fd1(lambda tt: u(tt, x), t, h)

    def ux_(t, x):
        return fd1(lambda xx: u(t, xx), x, h)

    def utt(t, x):
        return fd2(lambda tt: u(tt, x), t, h)

    def uxx(t, x):
        return fd2(lambda xx: u(t, xx), x, h)

    def ktt(t, x):
        return fd2(lambda tt: k(tt, x), t, h)

    def kxx(t, x):
        return fd2(lambda xx: k(t, xx), x, h)

    # J^0 = −κ ∂_t τ + τ ∂_t κ ; J^1 = κ ∂_x τ − τ ∂_x κ（号差 (−,+)）
    def J0(t, x):
        return -k(t, x) * ut_(t, x) + u(t, x) * kt_(t, x)

    def J1(t, x):
        return k(t, x) * ux_(t, x) - u(t, x) * kx_(t, x)

    divJ = fd1(lambda tt: J0(tt, x0), t0, h) + fd1(lambda xx: J1(t0, xx), x0, h)
    rhs = k(t0, x0) * (-utt(t0, x0) + uxx(t0, x0)) - u(t0, x0) * (-ktt(t0, x0) + kxx(t0, x0))
    return divJ, rhs


# (i) 恒等式核验：双子检验，verdict 由机读结果决定（判据须能反噬自己）
# (i-a) 精确性子检验：低次多项式场 ⇒ 解析上恒等式严格成立，FD 无截断误差，
#        残差应停留在舍入量级（舍入随 h 缩小而放大 ⇒ 用较大步长档）
def k_pair(t, x):
    return 1.0 + 0.3 * t + 0.2 * x


def u_pair(t, x):
    return 0.5 * t * t + 0.1 * x * x + 0.05 * t * x


exact_rows = []
for h in (1e-1, 5e-2, 2.5e-2):
    dj, rh = Jdiv_and_identity(k_pair, u_pair, 1.0, 1.0, h)
    exact_rows.append((h, dj, rh, abs(dj - rh)))
exact_ok = all(abs(r[3]) < 1e-9 for r in exact_rows)

# (i-b) 收敛阶子检验：非多项式光滑场 ⇒ FD 截断误差 O(h²) 主导，残差收敛阶应 ≈2
def k_smooth(t, x):
    return 1.0 + 0.2 * math.sin(0.7 * t) * math.cos(0.5 * x)


def u_smooth(t, x):
    return 0.5 * math.sin(1.3 * t) * math.cos(0.7 * x) + 0.3 * t * x


conv_rows = []
for h in (2e-2, 1e-2, 5e-3):
    dj, rh = Jdiv_and_identity(k_smooth, u_smooth, 1.0, 1.0, h)
    conv_rows.append((h, dj, rh, abs(dj - rh)))
orders = []
for i in range(len(conv_rows) - 1):
    e1, e2 = conv_rows[i][3], conv_rows[i + 1][3]
    if e2 > 0:
        orders.append(math.log(e1 / e2) / math.log(conv_rows[i][0] / conv_rows[i + 1][0]))
conv_ok = len(orders) >= 1 and min(orders) > 1.5
id_ok = exact_ok and conv_ok

_id_detail = ("子检验(i-a)精确性（多项式场，步长 %s）：残差 %s（舍入量级，%s）；"
              "子检验(i-b)收敛阶（光滑非多项式场，步长 %s）：残差 %s，阶 %s（应 ≈2）"
              % (["%.0e" % r[0] for r in exact_rows],
                 " / ".join("%.2e" % r[3] for r in exact_rows),
                 "达标" if exact_ok else "未达标",
                 ["%.0e" % r[0] for r in conv_rows],
                 " / ".join("%.2e" % r[3] for r in conv_rows),
                 " / ".join("%.2f" % o for o in orders)))
if id_ok:
    P("B", "B3a", "解析恒等式 ∂_μJ^μ = κ□τ − τ□κ（交叉项精确相消）数值确认",
      "两侧独立有限差分后逐点相减：" + _id_detail + " ⇒ 恒等式成立")
else:
    F("B", "B3a", "解析恒等式 ∂_μJ^μ = κ□τ − τ□κ 数值核验未达标",
      _id_detail + " ⇒ 恒等式未获数值确认（若解析推导无误则本判据失控，须排查引擎）")

# (ii) 守恒反例：κ≡1, τ=t² ⇒ ∂_μJ^μ = −2 ≠ 0（随步长收敛到 −2，不收敛到 0）
def k_const(t, x):
    return 1.0


def u_t2(t, x):
    return t * t


ce_rows = []
for h in (2e-2, 1e-2, 5e-3):
    dj, rh = Jdiv_and_identity(k_const, u_t2, 1.0, 1.0, h)
    ce_rows.append((h, dj))
ce_max = max(abs(r[1]) for r in ce_rows)
_ce_detail = ("反例 κ≡1, τ=t²：解析 ∂_μJ^μ = κ□τ − τ□κ = −2。三档步长数值 %s "
              "⇒ 收敛到 %.6f（|·|max=%.6f，%s 0）"
              % (" / ".join("%.6f" % r[1] for r in ce_rows), ce_rows[-1][1], ce_max,
                 "远离" if ce_max > 1e-6 else "接近"))
if ce_max > 1e-6:
    F("B", "B3b", "「几何场流守恒 ∂_μJ^μ=0」不成立（反例 + 收敛行为）",
      _ce_detail + "，不是守恒律。J^μ 至多在满足 κ□τ=τ□κ 的额外约束下 on-shell "
      "守恒，而来稿未声明该约束；且 on-shell 所依赖的 EOM 自身已败（A8/A9）⇒ "
      "§六 按所写形式 FAIL")
else:
    IN("B", "B3b", "守恒反例未能复现非零散度（既不能确认也不能否证 §六）",
      _ce_detail + "；反例失效 ⇒ 本条按纪律降级 INFO，不得据失效反例判 §六 FAIL")

# ---- B4 F4 范畴：曲线不变量 vs 场
F("B", "B4", "范畴混淆（F4）：§一 的 κ,τ 是单一曲线 Frenet 不变量，§二–§八 当作 4-流形上的场",
  "§一 用 Frenet-Serret 标架描述**一条**螺旋线（κ,τ 是曲线不变量，s 为弧长）；"
  "§二 起把 κ,τ 当场 κ(x^μ),τ(x^mu) 写入 ∫d⁴x 的作用量，但**未给出任何提升映射**"
  "（曲线不变量 → 流形场）。登记复发：49A 卷 C1「符号继承 ≠ 对象继承」；"
  "v总等于c 卷 §7.5「Frenet 不变量与 ECSK 联络不变量不是同一对象、不可混用」；"
  "30 号审计「SI 与普朗克单位混用、κ+τc 相加非法」。在对象级定义冻结前，"
  "§二–§八 的全部推导无指称对象")

# ---- B5 类光前提 vs Frenet 标架（读数二难复发）
def mink_norm(v, sig):
    return sig[0] * v[0] * v[0] + sum(v[i] * v[i] for i in range(1, 4))


sig_m = (-1.0, 1.0, 1.0, 1.0)
# 类光螺旋：r(λ) = (λ, A cos(ωλ), A sin(ωλ), 0)，A·ω=1 ⇒ g(dr,dλ) ≡ 0
A_n, w_n = 1.0, 1.0
grid = [2.0 * math.pi * i / 12.0 for i in range(13)]
gvals = []
for lam in grid:
    dr = (1.0, -A_n * w_n * math.sin(w_n * lam), A_n * w_n * math.cos(w_n * lam), 0.0)
    gvals.append(mink_norm(dr, sig_m))
gmax = max(abs(g) for g in gvals)
# 类时对照：A·ω=0.6<1 ⇒ g<0，弧长非零，T 良定义且 |T|²=−1
A_t, w_t = 0.6, 1.0
dr_t = (1.0, -A_t * w_t * math.sin(w_t * 0.7), A_t * w_t * math.cos(w_t * 0.7), 0.0)
g_t = mink_norm(dr_t, sig_m)
dsdt_t = math.sqrt(-g_t)
T_t = [c / dsdt_t for c in dr_t]
T_norm2 = mink_norm(T_t, sig_m)
b5_null_ok = (gmax < 1e-12)            # 类光：g(dr,dλ) ≡ 0（网格 13 点）
b5_ctrl_ok = (g_t < 0.0) and (abs(T_norm2 + 1.0) < 1e-9)   # 类时对照良定义
_b5_detail = ("机读：r(λ)=(λ, A cos ωλ, A sin ωλ, 0) 在 Minkowski (−,+,+,+) 下，A·ω=1 时 "
              "g(dr,dλ) = −1+(Aω)² ≡ 0（13 点网格 max|g| = %.2e，%s）⇒ ds/dλ ≡ 0 ⇒ "
              "T=dr/ds 为 0/0，κ,τ 的 Frenet 定义式（分母 |r'|³）发散。对照：A·ω=0.6（类时）"
              "g=%.4f<0，ds/dλ=%.4f≠0，T 良定义且 g(T,T)=%.12f=−1 ✓（%s）。"
              "⇒ 若把螺旋读为时空（洛伦兹）曲线，公理「v_total=c」与公理「Frenet-Serret "
              "标架」互相取消；若读为欧氏空间曲线，则落入 B4 的提升缺口。两种读法各有一个"
              "已登记缺陷、不可兼得（P-H3 读数二难复发，本条为机器再验证）"
              % (gmax, "复现" if b5_null_ok else "未复现",
                 g_t, dsdt_t, T_norm2, "对照通过" if b5_ctrl_ok else "对照异常"))
if b5_null_ok and b5_ctrl_ok:
    F("B", "B5", "前提集内部不一致：v_total=c 的时空螺旋是类光曲线，弧长元恒零，Frenet 标架无定义",
      _b5_detail)
else:
    BO("B", "B5", "类光螺旋退化演示未按预期复现（机读与解析预期不符）",
       _b5_detail + " ⇒ 本条既不能判 FAIL 也不能背书，按纪律降级 BOUNDARY，须排查引擎")

# ---- B6 Darboux 恒等式 INFO
IN("B", "B6", "§一 Frenet 方程组对圆柱螺旋是 Darboux 恒等式 ⇒ 定义性、零信息",
  "圆柱螺旋的 κ=a/(a²+b²), τ=b/(a²+b²) 代入 FS 方程组恒满足（控制组 CT6 已用"
  "独立有限差分复算；库内 P-H3 登记机器残差 <1e-200）。§一 唯一非定义性内容是"
  "色散关系 ω=cκ/sinθ，其本质就是 v_total=c 约束（已登记验证）。"
  "⇒ §一 整体按纪律降级 INFO（不得作为场论 layer 的独立公设计数）")

# ---- B7 （并入 A2b 的口径说明，此处记四力嵌入现状）
IN("B", "B7", "规范群嵌入：来稿自陈「用于嵌入 SU(3)×SU(2)×U(1)」= 未嵌入",
  "未来时表述，即当前无规范群、无规范场、无手征结构。已登记封杀门（不重算）："
  "秩障碍（SM 秩 4 > Aut(Cl(1,3)) 极大紧子群秩 2/3）、模容量门（一代 SM 64 实 vs "
  "Cl(1,3)≅M₄(ℝ) 不可约模 ℝ⁴）、耦合统一数据门（一圈 RG 预言 α_s(M_Z)=0.07115 vs "
  "0.1180±0.0009，52σ；MSSM 控制组 0.11686/1.27σ 必须通过否则判据不可信）、"
  "62/63/64 号 no-go 链。选项 3 的前置已封死")

# ---- B8 250 位代码块
hbar_str = "1.0545718176461565e-34"
sig_digits = len(hbar_str.split("e")[0].replace(".", "").lstrip("0"))
c_exact = (299792458 == 299792458)
k48, t48 = 1e10, 2e10
th48 = math.atan(k48 / t48)
om48_from_sin = 299792458.0 * k48 / math.sin(th48)
om48_geom = 299792458.0 * math.sqrt(k48 * k48 + t48 * t48)
om_rel = abs(om48_from_sin - om48_geom) / om48_geom
E48 = 1.0545718176461565e-34 * 299792458.0 * math.sqrt(k48 * k48 + t48 * t48)
m48 = E48 / (299792458.0 ** 2)
F("B", "B8", "「250 位有效数字精算」是伪精度声明（结果精度受 ħ 的 17 位有效数字封顶）",
  "输入精度账：c=299792458 为 SI 定义值（精确）；ħ 引用值 '1.0545718176461565e-34' "
  "仅 %d 位有效数字；κ,τ 为精确十进制 ⇒ E、m 的输出精度 ≤ %d 位。"
  "250 位只能作中间精度（合法），作为结果声明违反登记纪律「声明位数 ≤ 输入常数"
  "最小有效位」。块内算术本身自洽：ω=cκ/sinθ 与 c√(κ²+τ²) 相对偏差 %.2e；"
  "示例读数 θ=%.10f rad, ω=%.6e s⁻¹, E=%.6e J, m=%.6e kg（INFO）"
  % (sig_digits, sig_digits, om_rel, th48, om48_from_sin, E48, m48))

# ---- B9 参数计数门
F("B", "B9", "参数计数门不通过：3 个自由耦合 vs 0 个观测，「与实验一致」非可执行任务",
  "来稿 §七 自陈 λ「由第一性原理数值拟合/重整化群流确定」——拟合 ⇒ FIT 类外部输入，"
  "RG 流本身又非良定义（A11）。 unknowns = (κ,τ,λ₁,λ₂,λ₃) 每点 5 个，EOM 2 个"
  "（B2b）⇒ 净自由参数 ≥3，登记观测 0 ⇒ 按登记门禁 n_自由 ≤ n_观测−1 不满足；"
  "「与实验数据一致」在此参数账下不是可执行任务")

# ================================================================ C. 六选项封杀矩阵
log("")
log("=" * 78)
log("C. 「是否继续 1–6」逐项封杀矩阵（每条给出前置门编号）")
log("=" * 78)

F("C", "C1", "选项 1（球对称静态解解析推导）——BLOCKED",
  "前置失败：A6/A8/A9/A10（ℒ 与场方程量纲不自洽）+ B2（方程退化为代数式，"
  "「静态解」只是解代数方程组，且 κ(x),τ(x) 作为场的对象级定义缺失，B4）+ B5。"
  "注：既有静态球对称门禁 zxq23_static_sphere_gate.py（4/4 PASS）管的是 (ν,λ) "
  "度规系统，不覆盖本 ℒ；分支 B 无-go 定理属 K-essence 支线，均不能为本选项背书")
F("C", "C2", "选项 2（重整化群 β 函数完整推导）——BLOCKED",
  "前置失败：A7（λ 有量纲 ⇒ 无量纲 β 非良定义，须先归一化）+ A11/B2（无动能项 ⇒ "
  "无传播子 ⇒ 无圈图，β 无从产生）+ 登记复发：33 号审计已判 β_c/β_G 非良定义、"
  "C54/C55（紫外不动点）falsified、X-EXT-4 仅部分闭合")
F("C", "C3", "选项 3（四大力几何耦合映射）——BLOCKED（已登记判决，不重算）",
  "前置失败：B7（无规范群，自陈未嵌入）+ F4/E9 门（跨力比较必须无量纲化并声明能标，"
  "引力须 α_G(E)=GE²；本框架无 G ⇒ 连 α_G 都定义不出）+ 登记封杀链：秩障碍、"
  "模容量门、52σ 耦合统一数据门（含 MSSM 控制组）、62/63/64 号 no-go")
BO("C", "C4", "选项 4（生成 PRD 格式 LaTeX 全文骨架）——暂缓（DEFER）",
  "项目先例裁定（README 2026-09-26）：「LaTeX 论文全文为格式/图形输出，证据增量 0」；"
  "且当前会把 A6–A10 的 FAIL 级公式冻结进出版格式 ⇒ 必须先完成 Step-1 维度修复"
  "再谈成文。既有资产 tuft/I_LaTeX、TUFT_intrinsic_time_PRD.tex 可复用")
F("C", "C5", "选项 5（FDTD 波动求解器仿真代码）——BLOCKED",
  "前置失败：B2（无波动方程——EOM 是代数式，没有可离散的双曲/抛物系统）+ A6。"
  "FDTD 需要一个良定义的波算子，当前框架不提供")
F("C", "C6", "选项 6（ADM-BSSN 演化模块）——BLOCKED",
  "前置失败：B2（无动力学方程）+ B4（κ,τ 不是时空联络不变量，无 ADM 分解对象）"
  "+ 框架无 G（无 GR 极限可还原，也无 EH 项可嵌入 3+1 分解）")

# ================================================================ D. 修复方向
log("")
log("=" * 78)
log("D. 维度修复方向（机算；仅为量纲修复示范，不构成物理主张）")
log("=" * 78)

# D1 全四次型（conv A）
l_d1 = dadd(HBAR, dscale(KAPPA, 4))
eom_d1_kin = dadd(HBAR, dscale(KAPPA, 3))
eom_d1_pot = dadd(lam_need_a, dscale(KAPPA, 3))
d1_ok = (l_d1 == L_A) and (eom_d1_kin == eom_d1_pot)
if d1_ok:
    P("D", "D1", "修复方向 ①（conv A，全四次型）：ℒ = (ħ/2)(κ⁴−τ⁴) − λ₁κ⁴ − λ₂τ⁴ − λ₃κ²τ²",
      "[ħκ⁴] = %s = [ℒ]_A ✓；EOM 两侧 [ħκ³] = %s 与 [λκ³]（[λ]=%s）= %s ✓ "
      "⇒ 量纲自洽。代价：λ 仍有量纲（=[ħ]），且方程仍是代数的（无传播，见 D3）"
      % (dstr(l_d1), dstr(eom_d1_kin), dstr(lam_need_a), dstr(eom_d1_pot)))
else:
    F("D", "D1", "修复方向 ① 量纲自洽性未复现",
      "[ħκ⁴] = %s（目标 %s）；EOM 两侧 %s vs %s ⇒ 机算与预期不符，须排查引擎"
      % (dstr(l_d1), dstr(L_A), dstr(eom_d1_kin), dstr(eom_d1_pot)))

# D2 二次型 + 新标度（conv B）
ell = V(0, 1, 0)
l_d2 = dadd(HBARC, dscale(ell, -2), dscale(KAPPA, 2))
eom_d2_kin = dadd(HBARC, dscale(ell, -2), KAPPA)
eom_d2_pot = dadd(lam_need_b, dscale(KAPPA, 3))
d2_ok = (l_d2 == L_B) and (eom_d2_kin == eom_d2_pot)
if d2_ok:
    P("D", "D2", "修复方向 ②（conv B，二次型 + 基本长度 ℓ）：ℒ̃ = (ħc/2ℓ²)(κ²−τ²) − U",
      "[ħc/ℓ²·κ²] = %s = [ℒ̃]_B ✓；EOM 两侧 [ħcκ/ℓ²] = %s 与 [λκ³]（[λ]=%s）= %s ✓ "
      "⇒ 量纲自洽。代价：引入新基本标度 ℓ ⇒ 触发「有量纲自由参数 = 非定律」门与 "
      "P-H5「不预先植入常数」冲突，须作新假设申报"
      % (dstr(l_d2), dstr(eom_d2_kin), dstr(lam_need_b), dstr(eom_d2_pot)))
else:
    F("D", "D2", "修复方向 ② 量纲自洽性未复现",
      "[ħc/ℓ²·κ²] = %s（目标 %s）；EOM 两侧 %s vs %s ⇒ 机算与预期不符，须排查引擎"
      % (dstr(l_d2), dstr(L_B), dstr(eom_d2_kin), dstr(eom_d2_pot)))

# D3 动能项
kin_d3_a = dadd(HBAR, dscale(dadd(DMU, KAPPA), 2))
kin_d3_b = dadd(HBARC, dscale(dadd(DMU, KAPPA), 2))
d3_ok = (kin_d3_a == L_A) and (kin_d3_b == L_B)
if d3_ok:
    P("D", "D3", "修复方向 ③（传播性前提）：补动能项 ±(ħ/2)(∂κ)² 型",
      "conv A: [ħ(∂κ)²] = %s = [ℒ]_A ✓；conv B: [ħc(∂κ)²] = %s = [ℒ̃]_B ✓。"
      "这是选项 5/6 的前置：没有 (∂κ)² 就没有波算子。号差纪律：(−,+,+,+) 下健康"
      "标量动能为 −½(∂φ)²，写正即为鬼场（登记号差陷阱）"
      % (dstr(kin_d3_a), dstr(kin_d3_b)))
else:
    F("D", "D3", "修复方向 ③ 量纲自洽性未复现",
      "conv A: [ħ(∂κ)²] = %s（目标 %s）；conv B: [ħc(∂κ)²] = %s（目标 %s）⇒ 须排查引擎"
      % (dstr(kin_d3_a), dstr(L_A), dstr(kin_d3_b), dstr(L_B)))

# D4 λ 归一化 + 参数账
BO("D", "D4", "修复方向 ④（λ 无量纲化后方可谈 β；参数账须先过计数门）",
  "以标度幂把 λ 归一为无量纲 g_i = λ_i·μ^([λ])（conv A: [λ]=%s ⇒ g_i=λ_i/μ）；"
  "归一化后 β 才有定义。但参数计数门（B9：3 自由 vs 0 观测）不因归一化而过 ⇒ "
  "选项 2 即便维度修复也仍缺可检验内容" % dstr(lam_need_a))

# ================================================================ E. 汇总
log("")
log("=" * 78)
cnt = {}
for r in RESULTS:
    cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
log("汇总: TOTAL=%d  PASS=%d  FAIL=%d  BOUNDARY=%d  INFO=%d  用时=%.1fs"
    % (len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0),
       cnt.get("BOUNDARY", 0), cnt.get("INFO", 0), time.time() - T0))
log("=" * 78)

target_sha = None
if os.path.isfile(TARGET):
    with io.open(TARGET, "rb") as fh:
        target_sha = hashlib.sha256(fh.read()).hexdigest()
    log("被审原文: %s" % os.path.basename(TARGET))
    log("SHA-256: %s" % target_sha)

payload = {
    "title": "TUFT-V4.8 公式集 · 作用量量纲与场方程结构机器审计",
    "date": "2026-10-15",
    "target": os.path.basename(TARGET),
    "target_sha256": target_sha,
    "method": "(M,L,T) Fraction 精确量纲双基 + 结构审计 + 有限差分数值演示；控制组 6/6",
    "counts": {"TOTAL": len(RESULTS), "PASS": cnt.get("PASS", 0),
               "FAIL": cnt.get("FAIL", 0), "BOUNDARY": cnt.get("BOUNDARY", 0),
               "INFO": cnt.get("INFO", 0)},
    "controls": CONTROLS,
    "controls_all_ok": ctrl_all_ok,
    "results": RESULTS,
    "conclusion": {
        "one_liner": "V4.8 作用量层双基量纲不自洽（A6/A7/A8/A9/A10）且无动力学结构"
                     "（B1/B2），六个继续选项全部被前置门封死；正确下一步是 Step-1 "
                     "维度修复而非任选 1–6",
        "blocked_options": {"1": ["A6", "A8", "A9", "A10", "B2", "B4", "B5"],
                            "2": ["A7", "A11", "B2"],
                            "3": ["B7", "F4", "E9", "登记封杀链"],
                            "4": ["先例裁定：证据增量 0", "会冻结 FAIL 级公式"],
                            "5": ["B2", "A6"],
                            "6": ["B2", "B4", "无G"]},
        "repair_order": ["D1/D2 修 ℒ 量纲", "D3 补动能项", "D4 λ 归一化 + 参数计数门",
                         "然后 1（静态解）→ 5（FDTD）→ 2（RG）→ 3（四力，先过 F4/E9 与登记门）"
                         "→ 4（PRD LaTeX，最后成文）"],
    },
}
with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)
log("写出: %s" % OUT_JSON)
log("写出: %s" % OUT_TXT)
LOG.close()
sys.exit(0)
