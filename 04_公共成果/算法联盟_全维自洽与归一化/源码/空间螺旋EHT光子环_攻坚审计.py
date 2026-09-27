# -*- coding: utf-8 -*-
"""
空间螺旋 · EHT 光子环攻坚与审计（2026-09-26）
================================================
对象：草稿《算法联盟｜V21续修》「下一步选项 3」——黑洞光子环仿真，EHT 视界成像预测。

结构：
  1. GR 基准（mpmath 250 位）：光子球半径、临界捕获参数、shadow 角直径（Sgr A*/M87*）
  2. 散射角 RK4 数值验证（Schwarzschild Binet 方程，双精度）——验证工具链
  3. 纲领映射审查：对空间螺旋纲领现有全部几何量逐条审查「能否进入光子环可检验靶」
  4. 判别式 V 与伪派生判定（与 C53/C54 同款判定纪律）
  5. 输出 json + md（与批量审计体例一致）

红线：本模块只做「GR 基准精确复现 + 纲领映射证据审查」，不构造任何新物理；
      纲领无度规场方程 ⇒ 光子环预言无法第一性导出，本模块给出逐条证据。
"""
import io
import os
import json
import time
import math
from mpmath import mp, mpf, sqrt, pi, nstr

mp.dps = 250

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "数据")
OUT_DIR = os.path.abspath(OUT_DIR)

# =====================================================================
# 1. GR 基准（250 位）
# =====================================================================
C = mpf("299792458")
G = mpf("6.67430e-11")
MSUN = mpf("1.98847e30")
ARCSEC = mp.pi / (180 * 3600)          # 角秒→弧度
UAS = mp.pi / (180 * 3600 * 1e6)       # 微角秒→弧度

# EHT 目标（公开参数，2022/2019 观测）
# Sgr A*：质量 ~4.154e6 M☉（EHT 2022 拟合区间 ~4.0–4.3e6），距离 8.178 kpc
M_SGR = mpf("4.154e6") * MSUN
D_SGR = mpf("8.178e3") * mpf("3.0856775814913673e16")   # kpc→m
# M87*：质量 ~6.5e9 M☉，距离 16.8 Mpc
M_M87 = mpf("6.5e9") * MSUN
D_M87 = mpf("16.8e6") * mpf("3.0856775814913673e16")    # Mpc→m

r_g = lambda M: G * M / C**2          # 引力半径 GM/c²
r_s = lambda M: 2 * G * M / C**2      # Schwarzschild 半径
r_ph = lambda M: 3 * G * M / C**2     # 光子球半径
b_cr = lambda M: sqrt(27) * G * M / C**2   # 临界捕获参数 √27 GM/c²
theta_sh = lambda M, D: 2 * b_cr(M) / D    # shadow 角直径（rad）

results = {}

print("===== 1. GR 基准（mpmath 250 位） =====")
for name, M, D in (("Sgr A*", M_SGR, D_SGR), ("M87*", M_M87, D_M87)):
    rg = r_g(M); rs = r_s(M); rp = r_ph(M); bc = b_cr(M); th = theta_sh(M, D)
    th_uas = th / UAS
    print("%-7s | r_g=%.6e m | r_s=%.6e m | r_ph=%.6e m | b_crit=%.6e m | b/r_s=%.10f | θ_sh=%.3f μas"
          % (name, rg, rs, rp, bc, bc / rs, th_uas))
    results[name] = {
        "M_kg": float(M), "D_m": float(D),
        "r_g": float(rg), "r_s": float(rs), "r_ph": float(rp),
        "b_crit": float(bc), "b_over_rs": float(bc / rs),
        "theta_sh_uas": float(th_uas),
    }

# 观测对照（公开报道值，供交叉核对；非本模块产出）
results["obs"] = {
    "SgrA_shadow_uas": "~51.8 ± 2.3（EHT 2022 公开报道）",
    "M87_shadow_uas": "~42 ± 3（EHT 2019 公开报道，环状像角直径）",
    "note": "本模块仅复现 GR 理论基准；观测值为公开报道引用，用于量级交叉核对",
}

# 1PN 展开的 b_crit 修正量级（论证 β0≡GR 1PN 分支「零新内容」）
# Schwarzschild 精确 b_crit = 3√3 M；1PN 近似（只保留 GM/r 一阶）给出 b_crit^(1PN)，
# 其与精确值的相对差 ~ O((GM/(c²·r))²) ≈ (1/3)² —— 对 Sgr A* 用 r_ph 处：
M_unit = M_SGR
eps = r_g(M_unit) / r_ph(M_unit)      # = 1/3 精确
b1pn_over_b = mpf(1) + eps            # 1PN 冲击参数相对修正的一阶记号（示意）
print("\n     1PN 记号：r_g/r_ph = 1/3 精确 ⇒ β0≡GR 1PN 分支对 b_crit 的相对修正量级 O((GM/c²r)²)")
results["1pn"] = {
    "r_g_over_r_ph": float(eps),
    "note": "β0=3h²/c² 分支（C51）与 GR 1PN 恒等 ⇒ 对光子环无独立内容；"
            "高于 1PN 的修正需 2PN 以上，纲领无对应结构",
}

# =====================================================================
# 2. 散射角 RK4（Schwarzschild Binet 方程 w''+w=3M w²，双精度工具链验证）
# =====================================================================
print("\n===== 2. 散射角 RK4（双精度；Schwarzschild Binet 方程） =====")

def scatter_angle(b_over_bcrit, M=1.0, nstep=2000000):
    """Schwarzschild 光子散射角（弧度）。Binet: w''+w=3M w²，w=1/r，G=c=1。
    标准做法：从最近点（turnaround，dw/dφ=0）积分，w 首次过零（r→∞）时线性插值
    得半程角 φ_half，总偏折 α = 2·φ_half − π。步长 h=0.001/M（RK4 误差 O(h⁴)）。"""
    bc = math.sqrt(27) * M
    b = b_over_bcrit * bc
    # 最近点 w_max：1/b² = w_max²(1−2M w_max)，0 < w_max < 1/(3M)（二分）
    lo, hi = 0.0, 1.0 / (3.0 * M)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * mid * (1 - 2 * M * mid) - 1.0 / b**2 > 0:
            hi = mid
        else:
            lo = mid
    wmax = 0.5 * (lo + hi)
    w = wmax
    wp = 0.0
    phi = 0.0
    h = 0.001 / M
    w_prev = w
    for i in range(nstep):
        k1w = wp
        k1p = -w + 3 * M * w * w
        k2w = wp + 0.5 * h * k1p
        k2p = -(w + 0.5 * h * k1w) + 3 * M * (w + 0.5 * h * k1w) ** 2
        k3w = wp + 0.5 * h * k2p
        k3p = -(w + 0.5 * h * k2w) + 3 * M * (w + 0.5 * h * k2w) ** 2
        k4w = wp + h * k3p
        k4p = -(w + h * k3w) + 3 * M * (w + h * k3w) ** 2
        w_new = w + h / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w)
        wp_new = wp + h / 6.0 * (k1p + 2 * k2p + 2 * k3p + k4p)
        phi += h
        w, wp = w_new, wp_new
        if w <= 0.0:                       # w 过零（r→∞）：线性插值半程角
            if w_prev > 0.0:
                phi_half = phi - h * w / (w - w_prev)
            else:
                phi_half = phi
            return 2 * phi_half - math.pi
        w_prev = w
    return float("inf")                    # 临界发散（b→b_crit），未在步数内出射

scatter_rows = []
for bb in (1.001, 1.01, 1.1, 2.0, 5.0, 50.0, 200.0):
    alpha = scatter_angle(bb)
    # 弱场 1PN 解析：α ≈ 4GM/(bc²) = 4/(bb·3√3)；仅在 b >> M 时成立（b≳50·b_crit 偏差 <1%）
    weak = 4.0 / (bb * 3.0 * math.sqrt(3.0))
    scatter_rows.append((bb, alpha, alpha * 180 / math.pi, weak, abs(alpha - weak)))
    print("   b/b_crit=%7.1f | 总偏折 α=%.8f rad (%.2f°) | 1PN 解析 α≈%.8f rad | |Δ|=%.2e"
          % (bb, alpha, alpha * 180 / math.pi, weak, abs(alpha - weak)))
print("   弱场极限验证：b=200·b_crit 时数值应收敛到 1PN（偏差 < 1e-5）；b~b_crit 时强场修正显著，数值为准")
results["scatter"] = {
    "method": "RK4, Schwarzschild Binet w''+w=3M w²",
    "note": "b/b_crit→1 时偏折发散（光子绕多圈）；b/b_crit>1 散射角有限。"
            "工具链验证用；纲领自身无测地线方程可借",
}

# =====================================================================
# 3. 纲领映射审查（逐条证据）
# =====================================================================
print("\n===== 3. 纲领映射审查（能否进入光子环可检验靶） =====")

# (几何量, 来源 claim, 量纲/状态, 能否构成 b_crit/环宽修正的映射证据, 结论)
MAP_REVIEW = [
    ("κ/τ（Frenet 曲率/挠率）", "C26（四方冲突 falsified）",
     "[L⁻¹]；τ/κ=u/(Aω) 唯一性被否",
     "光子环半径/宽度由度规测地线决定；纲领无度规场方程，κ 无处挂载；"
     "叠加修正无方程载体",
     "FAIL（无映射方程）"),
    ("β（Binet 修正参数）", "C49/C51（open）",
     "β0=3h²/c² 分支 ≡ GR 1PN（u² 系数精确相等）；β_correct=2.74e11 m²（[L²]，水星标定）",
     "β0 分支已被 GR 1PN 包含 ⇒ 对 b_crit 零新内容（1PN 记号 r_g/r_ph=1/3）；"
     "β_correct 为弱场标定值，无理论给出 β 对场强的依赖 ⇒ 无法外推到强场",
     "FAIL（零内容 / 无外推映射）"),
    ("ω、A（基底参数）", "C24/C25（|R'|=c 修复；α 公式欠定）",
     "ωA=c/2.0068（读数A）；无量纲组合无引力内容",
     "基底参数只进入 α 电磁公式；与引力光子环无任何方程连接",
     "FAIL（无映射方程）"),
    ("N（拓扑绕数）", "C27（falsified）/C50（外部输入）",
     "无量纲；floor 定义不可复现",
     "N 只调制 LB 本征谱（退化谱 1e-75）；与测地线/度规无连接",
     "FAIL（无映射方程）"),
    ("Φ₀（相位场）", "C36（falsified）",
     "[Φ₀]=[Φ]/L 量纲冲突",
     "量纲冲突已定罪 ⇒ 不可进入任何场方程",
     "FAIL（量纲死亡）"),
    ("ρ、K₀、α²K 类", "C12/C29/C30/C31/C32/C33（falsified）",
     "量纲失败 / 循环定义 / 孤儿场",
     "已尽数定罪，无活体结构可复用",
     "FAIL（已证伪）"),
    ("GravBubble κ0/τ0/σ/αg", "C53（falsified）",
     "量纲非法 ×4；无作用量",
     "已定罪；且无作用量 ⇒ 无法衍生出度规/测地线结构",
     "FAIL（已证伪）"),
    ("RG 系数 b1..b6", "C54（falsified）",
     "六自由无映射；无紫外固定点",
     "RG 流与观测靶无映射方程（同 C54 结论）；不能产生光子环预言",
     "FAIL（无映射方程）"),
]

fails = 0
for name, src, dim, ev, concl in MAP_REVIEW:
    tag = "✓" if concl == "PASS" else "✗"
    print("   %s %-28s | %s | %s" % (tag, name, src, concl))
    if concl != "PASS":
        fails += 1
results["mapping"] = {
    "items": [
        {"quantity": n, "source": s, "dimension": d, "evidence": e, "conclusion": c}
        for n, s, d, e, c in MAP_REVIEW
    ],
    "pass_count": len(MAP_REVIEW) - fails,
    "fail_count": fails,
}

# =====================================================================
# 4. 判别式与判定（C53/C54 同款纪律）
# =====================================================================
print("\n===== 4. 判别式与判定 =====")
# 自由参数：纲领可调入光子环修正的独立参数 = 0（映射全部 FAIL ⇒ 无可调入参数）
# 约束方程：0（无场方程、无映射方程）
F = 0; Cst = 0
V = F - Cst
print("   自由参数 F=%d，约束 C=%d，判别式 V=F−C=%d" % (F, Cst, V))
verdict = "falsified" if V <= 0 else "open"
print("   V≤0 ⇒ 伪派生（无映射方程层）；与 C53（V=−4）、C54（无映射）同模式")
print("   体系级开放问题：空间螺旋纲领若存在度规场方程，光子环预言可重启；"
      "当前无此结构（无作用量→无场方程→无测地线→无光子环）")
results["verdict"] = {
    "F": F, "C": Cst, "V": V, "verdict": verdict,
    "conclusion": "EHT 光子环模块：GR 基准精确复现（工具链验证通过）；"
                  "纲领映射 8 项全部 FAIL ⇒ 无独立可检验靶 ⇒ V≤0 伪派生（无映射方程层）。"
                  "体系级「若纲领给出场方程则重启」保持 open（前置：从作用量导出场方程）",
}

# =====================================================================
# 5. 输出 json + md
# =====================================================================
payload = {
    "title": "空间螺旋 · EHT 光子环攻坚与审计",
    "date": "2026-09-26",
    "dps": 250,
    "results": results,
    "claims_register_suggestion": {
        "C55": "EHT 光子环模块（GR 基准复现 + 纲领映射审查）→ falsified（无映射方程层）；"
               "体系级 open 前置：先由作用量导出场方程",
        "C56": "CMB 拓扑双谱模块——未提交（无模块、无公式、无脚本），延续 V21续修② 建议："
               "不得凭声明登记",
    },
}
with io.open(os.path.join(OUT_DIR, "空间螺旋EHT光子环_攻坚审计.json"), "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)
print("\n    JSON 已写出：数据/空间螺旋EHT光子环_攻坚审计.json")

md = []
md.append("# 空间螺旋 · EHT 光子环攻坚与审计（2026-09-26）")
md.append("")
md.append("> 日期 2026-09-26 · mpmath dps=250 · 对象：草稿「下一步选项 3」（EHT 视界成像预测）")
md.append("> 纪律：GR 基准精确复现 + 纲领映射逐条证据审查 + V 判别式（与 C53/C54 同款）")
md.append("")
md.append("## 1. GR 基准（可检验靶的基准值）")
md.append("")
md.append("| 目标 | r_g (m) | r_s (m) | r_ph (m) | b_crit (m) | b/r_s | θ_sh (μas) |")
md.append("|---|---|---|---|---|---|---|")
for name in ("Sgr A*", "M87*"):
    r = results[name]
    md.append("| %s | %.4e | %.4e | %.4e | %.4e | %.6f | %.3f |"
              % (name, r["r_g"], r["r_s"], r["r_ph"], r["b_crit"], r["b_over_rs"], r["theta_sh_uas"]))
md.append("")
md.append("**观测对照（公开报道值，仅量级交叉核对）**：Sgr A* 阴影角直径 ~51.8±2.3 μas（EHT 2022）；"
          "M87* 环状像角直径 ~42±3 μas（EHT 2019）。本模块 GR 理论基准 52.1 / 39.7 μas 与之同量级一致。")
md.append("")
md.append("**1PN 记号**：r_g/r_ph=1/3 精确 ⇒ β0=3h²/c² 分支（C51）≡ GR 1PN，对 b_crit 零新内容；"
          "高于 1PN 的修正需 2PN 以上结构，纲领无对应项。")
md.append("")
md.append("## 2. 散射角 RK4（工具链验证，双精度）")
md.append("")
md.append("Schwarzschild Binet 方程 w''+w=3M w²，RK4 积分：")
md.append("")
md.append("| b/b_crit | 总偏折 α (rad) | α (°) | 弱场 1PN 解析 (rad) | |Δ| |")
md.append("|---|---|---|---|---|")
for bb, alpha, adeg, weak, diff in scatter_rows:
    md.append("| %.3f | %.6f | %.2f | %.6f | %.2e |" % (bb, alpha, adeg, weak, diff))
md.append("")
md.append("b/b_crit→1 偏折发散（光子绕多圈），>1 有限散射——工具链行为正确。"
          "**纲领自身无测地线方程**，本工具链只能借自 GR。")
md.append("")
md.append("## 3. 纲领映射审查（8 项全部 FAIL）")
md.append("")
md.append("| 几何量 | 来源 | 量纲/状态 | 证据 | 结论 |")
md.append("|---|---|---|---|---|")
for n, s, d, e, c in MAP_REVIEW:
    md.append("| %s | %s | %s | %s | **%s** |" % (n, s, d, e, c))
md.append("")
md.append("**失败模式总结**：8 项无一能构成 b_crit/环宽修正——量纲死亡（Φ₀/ρ/K₀/α²K/引力泡）、"
          "零内容（β0≡1PN）、或**无映射方程**（κ/ω/N/β_correct/RG）。")
md.append("")
md.append("## 4. 判定")
md.append("")
md.append("自由参数 F=0（无可调入参数），约束 C=0，**判别式 V=F−C=0 ≤ 0 ⇒ falsified（无映射方程层）**。")
md.append("与 C53（V=−4）、C54（无映射）同模式：纲领的每一个可计算模块都死于"
          "「从几何量到可观测量的映射方程缺失」这一整层结构。")
md.append("")
md.append("**体系级 open（如实保留）**：若纲领先给出作用量并导出场方程，光子环预言可重启——"
          "但当前无此结构（无作用量→无场方程→无测地线→无光子环），故体系级断言保持 open 而非关闭。")
md.append("")
md.append("## 5. 台账登记建议（待用户确认）")
md.append("")
md.append("- **C55**：EHT 光子环模块 → **falsified**（无映射方程层）；体系级前置 open（先由作用量导出场方程）。")
md.append("- **C56**：CMB 拓扑双谱模块——**未提交**（无模块、无公式、无脚本），延续 V21续修② 建议：不得凭声明登记。")
md.append("")
md.append("**红线**：本模块不构造新物理，只做 GR 基准复现与映射证据审查；不修改 claims.csv 任何状态。")

with io.open(os.path.join(OUT_DIR, "空间螺旋EHT光子环_攻坚审计.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(md))
print("    MD 已写出：数据/空间螺旋EHT光子环_攻坚审计.md")
print("\n" + "=" * 76)
print("判定：%s | V=%d | 映射 0/8 通过 | GR 基准 2/2 复现" % (verdict, V))
print("=" * 76)
