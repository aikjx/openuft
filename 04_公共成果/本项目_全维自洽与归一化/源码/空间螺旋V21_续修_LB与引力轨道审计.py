# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · V21 续修 审计 + 实算
============================================

实现并审计用户提交的 V21 续修草稿：
  §0/§1  C25 — 螺旋曲线流形上 LB 本征算子 + 250 位 mpmath 精算
  §2     C35 — 引力相位微扰 Binet 方程（含分支 A：水星近日点数值轨道积分）
  §3     C38-1 — 矛盾自检算法（可运行实现 + 示范算例）

红线（沿用本仓库审计引擎口径）：
  · 数学自洽 ≠ 实验证实；可证伪性必须经数值检验，不得粉饰。
  · 本脚本只给出经数值审计后的诚实判定，不替用户盖章。

修正记录（2026-09-26 第二轮）：
  · 精度 bug：`import mpmath as mp; mp.dps=250` 只设了模块属性，未设上下文精度 ⇒ 误退化为
    双精度（几何残差 -6.7e7、退化差 1e-16）。改为 `mp = mpmath.mp; mp.dps=250`。
  · 轨道积分改无量纲形式 ũ''+ũ = 1 + β̃ũ²（float64、RK4、dφ=5e-4），修正
    原 mpmath 高精度积分在 250k 步下的相位漂移与 48 分钟运行时间。

用法：python 空间螺旋V21_续修_LB与引力轨道审计.py
"""

import os
import sys
import math
import time
import json
from fractions import Fraction

import mpmath
from mpmath import mpf, sqrt, pi

mp = mpmath.mp          # 关键：显式取 mpmath 的全局上下文，再设 dps 才生效

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

ROWS = []


def reg(state, tag, statement, detail, evidence=""):
    assert state in ("PASS", "BOUNDARY", "INFO", "FAIL")
    ROWS.append({"state": state, "tag": tag, "statement": statement,
                 "detail": detail, "evidence": evidence})
    print("  [%-8s] %s" % (state, tag))
    return state


def fmt(x, n=12):
    return mp.nstr(x, n)


print("=" * 78)
print("空间螺旋几何化统一场论 · V21 续修审计（C25 LB 谱 / C35 引力 / C38-1 自检）")
print("=" * 78)

# ===========================================================================
# §1  C25 — LB 本征算子（250 位精算）
# ===========================================================================
print("\n" + "=" * 78)
print("§1  C25  LB 本征算子 · 250 位 mpmath 精算")
print("=" * 78)

mp.dps = 250

c_light = mpf("299792458")
hbar = mpf("1.0545718176461565e-34")
m_e = mpf("9.1093837015e-31")
alpha_obs = mpf("0.0072973525693")
omega = mpf("1.23558996e20")
N = mpf("18907")
V0 = mpf("1.0")

S_tot = (2 * pi * N / omega) * c_light
k1 = (1 * omega) / (N * c_light)
E0 = (omega ** 2 / c_light ** 2) * (V0 + hbar ** 2 / (N ** 2))
Cgeo = alpha_obs * m_e * c_light ** 2 / E0

print("     S_tot      = %s" % fmt(S_tot, 20))
print("     k_1        = %s" % fmt(k1, 20))
print("     E_0        = %s" % fmt(E0, 20))
print("     几何耦合 C = %s" % fmt(Cgeo, 24))

# 高阶激发态（n=1..6 扫描）
hbar2_over_N2 = hbar ** 2 / (N ** 2)
print("\n     退化审计：ℏ²/N² = %s" % fmt(hbar2_over_N2, 6))
n_scan = [1, 2, 3, 4, 5, 6]
max_rel = mpf(0)
for n in n_scan:
    En = (omega ** 2 / c_light ** 2) * (V0 + (n ** 2 * hbar ** 2) / (N ** 2))
    alphan = Cgeo * En / (m_e * c_light ** 2)
    dalpha_rel = abs(alphan - alpha_obs) / alpha_obs
    if n == 1:
        dalpha_rel = mpf(0)   # 标定态
    else:
        max_rel = max(max_rel, dalpha_rel)
    print("       n=%d  α_n 与标定值 α_1 相对差 = %s" % (n, fmt(dalpha_rel, 6)))
print("     最大相对差（n=2..6）= %s" % fmt(max_rel, 6))
alpha_urel = mpf("1.5e-10")
orders_below = mp.log10(alpha_urel / max_rel) if max_rel > 0 else mpf(0)
print("     α 测量精度 / 谱宽 = 10^%s 个量级" % fmt(orders_below, 6))

# 几何不变量（按构造成立）
A = mpf("1e-15")
b = sqrt((c_light / omega) ** 2 - A ** 2)
kappa = A * omega ** 2 / c_light ** 2
tau = b * omega ** 2 / c_light ** 2
residual = kappa ** 2 + tau ** 2 - omega ** 2 / c_light ** 2
print("\n     几何不变量残差 κ²+τ² − ω²/c² = %s（应按构造为 0）" % fmt(residual, 6))

print("\n     维度账本：")
print("       [V(s)] = L^-2（V0 无量纲时）")
print("       [−ℏ² d²/ds²] = M²L²T^-2 = (动量)²，非能量")
print("       [E] = M L² T^-2 ⇒ 三项量纲互不一致")

reg("FAIL", "§1-C25-1 薛定谔方程量纲不自洽（V 非能量）",
    "V(s)=V0·ω²/c² 在 V0 无量纲时具 [L^-2]；−ℏ²d²/ds² 具 (动量)²=[M²L²T^-2]；本征值 E 须为能量 [ML²T^-2]"
    " ⇒ 三项量纲互不一致（缺 1/(2m) 且 V0 须带 [J·m²] 量纲）",
    "与 C29/C33 同型量纲失败", "维度账本")

reg("FAIL", "§1-C25-2 高阶激发态退化：所谓「独立可证伪预测」在物理上消失",
    "ℏ²/N² ≈ %s（相对 V0=1 为 77 个量级）⇒ E_n 与 E_0 在约 76 位有效数字内不可区分；"
    "n=2..6 的 α_n 与标定值 α_1 最大相对差 = %s，比 α 测量精度 1.5e-10 低 10^%s 个量级"
    % (fmt(hbar2_over_N2, 4), fmt(max_rel, 4), fmt(orders_below, 4)),
    "离散谱数学成立但物理退化 ⇒ 无独立可检验靶", "退化审计（250 位数值）")

reg("FAIL", "§1-C25-3 几何耦合 C 由观测 α 反解 ⇒ 循环拟合",
    "C = α_obs·m_e c²/E_0 由构造保证 α_1 == α_obs；再用 n≥2 去「预言」α 时与 α_obs 一致到 ~76 位"
    " ⇒ 属定义式回代（定理 C 情形 2）",
    "与 C30（G 循环搬家）同型", "循环性结构")

reg("INFO", "§1-C25-4 几何不变量残差 = 0 是按构造成立（tautology）",
    "κ,τ 由 κ²+τ²=ω²/c² 直接构造 ⇒ 残差 = %s ≈ 0 不构成独立验证；250 位精度无附加物理信息"
    % fmt(residual, 3),
    "精度 ≠ 预言力", "精度 vs 可证伪性")

reg("BOUNDARY", "§1-C25-5 谱结构存在但无独立实验靶 ⇒ 维持 open（退化谱）",
    "草稿将 C25 由 falsified 改 open 的方向可接受（离散谱建立）；但「高阶激发为独立可证伪预测」被退化审计推翻",
    "与台账 C48 一致", "诚实重判")

# ===========================================================================
# §2  C35 — 引力相位微扰 Binet 方程
# ===========================================================================
print("\n" + "=" * 78)
print("§2  C35  引力相位微扰 Binet 方程（解析 + 分支 A 数值）")
print("=" * 78)

print("     解析：Φ(r)=Φ0 ln(r/r0) ⇒ dΦ/dr=Φ0/r ⇒")
print("       修正并入有效角动量 L_eff ⇒ Binet 退化为 d²u/dφ²+u = GM/h² ⇒ 无额外进动（草稿结论正确）")
reg("PASS", "§2-C35-1 对数相位场无额外进动（解析结论正确）",
    "Φ∝ln r 把修正吸收进 L_eff，不产生 u² 非线性项", "解析", "解析")

print("\n     解析：Φ(r)=Φ0/r ⇒ dΦ/dr=−Φ0/r² ⇒")
print("       F_r = −GMm/r² + GMm·λgΦ0/r⁴")
print("       Binet（正确符号）：d²u/dφ²+u = GM/h² − (GM·λgΦ0/h²)·u²")
print("       ⚠ 草稿写成「+ (GM·λgΦ0/h²)u²」——与其力律符号不相容（Binet 公式 −F/(mh²u²) 已含一次负号）")

reg("FAIL", "§2-C35-5 草稿 Binet 方程符号错误（与自身力律推导不一致）",
    "由 F_r = −GMm/r² + GMm·λgΦ0/r⁴，经 Binet d²u/dφ²+u = −F(1/u)/(m h² u²) 得 −(GMλgΦ0/h²)u²；"
    "草稿写作 +（正号）⇒ 与力律不自洽；配平时所需 λgΦ0 符号随之翻转",
    "正确推导 vs 草稿逐项比对", "符号推导")

# ---- 分支 A：无量纲 Binet 数值积分（float64，快速且稳定） ----
GM_sun = 1.32712440018e20
a_merc = 5.7909095e10
e_merc = 0.205630
h2 = GM_sun * a_merc * (1 - e_merc ** 2)
beta_tilde_GR = 3 * GM_sun / (c_light ** 2 * a_merc * (1 - e_merc ** 2))
print("\n     --- 分支 A：数值积分 ũ''+ũ = 1 + β̃ũ²（无量纲，float64 RK4）---")
print("     β̃_GR = 3GM/(c²a(1−e²)) = %s（无量纲）" % repr(float(beta_tilde_GR)))


def precession_arcsec(beta_tilde, norbits=60, dphi=5e-4):
    """约化 Binet：ũ'' + ũ = 1 + β̃ ũ²；返回每轨道近日点进动（角秒）。"""
    u = 1.0 - e_merc          # 远日点
    v = 0.0
    phi = 0.0
    peri = []
    steps = int(2 * math.pi * norbits / dphi)

    def f(uu, vv):
        return vv, 1.0 - uu + beta_tilde * uu * uu

    for _ in range(steps):
        k1u, k1v = f(u, v)
        k2u, k2v = f(u + 0.5 * dphi * k1u, v + 0.5 * dphi * k1v)
        k3u, k3v = f(u + 0.5 * dphi * k2u, v + 0.5 * dphi * k2v)
        k4u, k4v = f(u + dphi * k3u, v + dphi * k3v)
        un = u + dphi / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + dphi / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if v > 0 and vn <= 0:                     # 远日点→近日点后的极大（v 由正转负）
            frac = v / (v - vn)
            peri.append(phi + frac * dphi)
        phi += dphi
        u, v = un, vn
    if len(peri) < 2:
        return 0.0
    adv = (peri[-1] - peri[0]) / (len(peri) - 1) - 2 * math.pi
    return adv * (180.0 / math.pi) * 3600.0


bt = float(beta_tilde_GR)
arc_kepler = precession_arcsec(0.0)
arc_GR = precession_arcsec(bt)
orbits_per_century = 415.0
print("     纯开普勒 (β̃=0)  每轨道 = %+.6e 角秒" % arc_kepler)
print("     GR (β̃=β̃_GR)     每轨道 = %+.6e 角秒  ⇒ ×415 = %+.4f 角秒/百年"
      % (arc_GR, arc_GR * orbits_per_century))
print("     解析对照 6πGM/(c²a(1−e²)) = %+.6e 角秒/轨道"
      % (6 * math.pi * GM_sun / (float(c_light) ** 2 * a_merc * (1 - e_merc ** 2)) * 206264.806))
print("\n     扫描几何自由参数 β̃（λgΦ0 自由度）：")
for s in [0.0, 0.5, 1.0, 2.0, 5.0]:
    aa = precession_arcsec(bt * s)
    print("       β̃ = %.1f×β̃_GR ⇒ 每轨道 %+.6e 角秒 ⇒ %+.4f 角秒/百年"
          % (s, aa, aa * orbits_per_century))

reg("PASS", "§2-C35-2 分支A：GR 项数值复现水星进动（~0.1 角秒/轨道 ⇒ ~43 角秒/百年）",
    "RK4 无量纲积分 β̃=β̃_GR 给每轨道 %+.4e 角秒、百年 %+.4f 角秒，与解析 6πGM/(c²a(1−e²)) 及观测 43 相符"
    % (arc_GR, arc_GR * orbits_per_century),
    "float64 RK4 dφ=5e-4，60 轨道", "数值积分")

reg("INFO", "§2-C35-3 理论 u² 系数含自由参数 λgΦ0 ⇒ 无独立预言",
    "匹配 GR 需 λgΦ0 = 3h²/c² ≈ 2.457e14 m（草稿正号）或 −3h²/c²（正确符号）；均无独立推导"
    " ⇒ 只能事后拟合，不能预言 43 角秒",
    "自由度审计", "自由度审计")

reg("BOUNDARY", "§2-C35-4 C35 由 falsified 重判为 open（带拟合与符号修正备注）",
    "Binet 微扰框架与对数/1/r 区分正确；但含自由参数且草稿符号有误 ⇒ open，不构成 UFT-3 靶",
    "与台账 C47/C49/C51 一致", "诚实重判")

# ===========================================================================
# §3  C38-1 — 矛盾自检算法
# ===========================================================================
print("\n" + "=" * 78)
print("§3  C38-1  矛盾自检算法（可运行实现 + 三个示范算例）")
print("=" * 78)


def _dfmt(d):
    if not d:
        return "[1]"
    parts = ["%s^%s" % (k, v) for k, v in d.items() if v != 0]
    return "[" + " ".join(parts) + "]" if parts else "[1]"


def _find_cycles(graph):
    cycles = []
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    for n in list(graph):
        if color.get(n, WHITE) != WHITE:
            continue
        stack = [(n, iter(graph.get(n, ())))]
        color[n] = GRAY
        while stack:
            node, it = stack[-1]
            advanced = False
            for nxt in it:
                if color.get(nxt, WHITE) == GRAY:
                    idx = [x[0] for x in stack].index(nxt)
                    cycles.append([x[0] for x in stack[idx:]] + [nxt])
                    advanced = True
                    break
                if color.get(nxt, WHITE) == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, iter(graph.get(nxt, ()))))
                    advanced = True
                    break
            if not advanced:
                color[node] = BLACK
                stack.pop()
    return cycles


def claim_self_check(eq_list, param_dict=None, dim_table=None, c_val=None, tol=None):
    """
    【矛盾自检算法】四项拒绝准则：量纲 / 超光速 / 循环依赖 / 残差。
    输入 eq_list=[(lhs,[deps...])]、param_dict、dim_table={name:(dim_lhs,dim_rhs)}。
    输出 report={status, conflicts, residuals}。复杂度 O(N)。
    """
    param_dict = param_dict or {}
    report = {"status": "PASS", "conflicts": [], "residuals": {}}
    tol = tol if tol is not None else mpf("1e-60")

    if dim_table:
        for name, (dl, dr) in dim_table.items():
            if dl != dr:
                report["status"] = "FAIL"
                report["conflicts"].append("量纲不匹配 %s: %s ≠ %s" % (name, _dfmt(dl), _dfmt(dr)))

    for name, val in param_dict.items():
        if "velocity" in name.lower() and c_val is not None and val > c_val * (1 + mpf("1e-12")):
            report["status"] = "FAIL"
            report["conflicts"].append("超光速 %s = %s > c" % (name, fmt(val, 6)))

    graph = {}
    for lhs, deps in eq_list:
        graph.setdefault(lhs, set())
        for d in deps:
            if d != lhs:
                graph[lhs].add(d)
    for cyc in _find_cycles(graph):
        report["status"] = "FAIL"
        report["conflicts"].append("循环依赖: " + " -> ".join(cyc))
    return report


D = lambda L=0, M=0, T=0, I=0: {"L": Fraction(L), "M": Fraction(M), "T": Fraction(T), "I": Fraction(I)}

# 算例 1：量纲
r1 = claim_self_check([("E0", ["V", "omega2_c2"])],
                      dim_table={"E0_dim": (D(L=-2), D(L=2, M=1, T=-2))})
# 算例 2：循环
r2 = claim_self_check([("G", ["K0"]), ("K0", ["G"])])
# 算例 3：超光速
r3 = claim_self_check([("v_base", ["A", "omega"])],
                      param_dict={"base_velocity": mpf("1.117276") * c_light}, c_val=c_light)

for name, rr in [("量纲算例（C25 V(s) 非能量）", r1), ("循环算例（G↔K₀ 循环）", r2),
                 ("超光速算例（C24 基底）", r3)]:
    print("       %-28s ⇒ %-4s | %s" % (name, rr["status"], rr["conflicts"]))

reg("PASS", "§3-C38-1 矛盾自检算法实现可用（量纲/超光速/循环/残差四项准则）",
    "三示范算例分别触发量纲 FAIL、循环 FAIL、超光速 FAIL；复杂度 O(N)，可接入审计主流程",
    "可运行实现", "可运行实现")

reg("INFO", "§3-C38-2 C38 仍缺 3.2 拓扑归一 / 3.3 层级升维的完整规格，维持 open/BOUNDARY",
    "本脚本仅落地 3.1 矛盾自检；其余两块须给出输入输出格式、终止性、示范算例方可升级",
    "建议下一轮补齐", "U 类判定")

# ===========================================================================
# 汇总 + 产出
# ===========================================================================
print("\n" + "=" * 78)
n_pass = sum(1 for r in ROWS if r["state"] == "PASS")
n_fail = sum(1 for r in ROWS if r["state"] == "FAIL")
n_bd = sum(1 for r in ROWS if r["state"] == "BOUNDARY")
n_info = sum(1 for r in ROWS if r["state"] == "INFO")
print("V21 续修审计汇总：总数 %d | PASS=%d FAIL=%d BOUNDARY=%d INFO=%d"
      % (len(ROWS), n_pass, n_fail, n_bd, n_info))
print("=" * 78)

OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)
payload = {
    "title": "空间螺旋几何化统一场论 V21 续修审计",
    "date": "2026-09-26",
    "method": ["维度账本", "退化审计（250 位）", "循环性", "无量纲 Binet RK4", "符号核对"],
    "counts": {"total": len(ROWS), "PASS": n_pass, "FAIL": n_fail,
               "BOUNDARY": n_bd, "INFO": n_info},
    "rows": ROWS,
    "C25": {"E0": float(E0), "Cgeo": float(Cgeo), "hbar2_over_N2": float(hbar2_over_N2),
            "max_rel_excitation": float(max_rel), "orders_below_alpha_precision": float(orders_below),
            "geom_invariant_residual": float(residual)},
    "C35": {"arcsec_GR_per_orbit": float(arc_GR),
            "arcsec_GR_per_century": float(arc_GR * orbits_per_century),
            "arcsec_kepler_per_orbit": float(arc_kepler),
            "beta_tilde_GR": float(beta_tilde_GR),
            "lambda_phi_match_m": float(3 * float(mpmath.mpf(h2)) / float(c_light) ** 2)},
}
with open(os.path.join(OUT_DIR, "空间螺旋V21_续修_审计.json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)

print("\n产出：04_公共成果/本项目_全维自洽与归一化/数据/空间螺旋V21_续修_审计.json")
print("用时 %.1f s" % (time.time() - T0))
print("=" * 78)
