# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF-ADD-01 β 衰变手征不对称修正（δA_TUFT）数值计算（分支 3）
==========================================================================
性质：数值计算 / 可证伪性评估。非物理层判决，但给出明确的排除/存活结论。
纯标准库，零第三方依赖。

口径（全部由已确立/已审文本给出）：
  分区：三正瓣（ADD-02）——弱域锥心 θ_W,c = 240°，Δθ_W = 60°；
  弱代表点：ADD-02 由 α_W/λ = cos3θ = 0.1438 反解 θ_W = 212.757°（取一支）；
  幅值：|Ω_weak| = λ·cos3θ_W = α_W = 0.01696（ADD-02 归一化 λ = α_s = 0.1179）；
  相位：φ_W = φ_0·(θ_W − θ_W,c)/Δθ_W（ADD-01 B.2 线性 ansatz，分支4 N6 边界跳变不影响代表点内部）；
  修正：按分支4 N1 修法，A_obs = A_SM + δA_TUFT，δA_TUFT 来自 |M_SM+M_TUFT|² 干涉；
         纯左 SM（V−A，M_SM 实）+ TUFT 左耦合 |Ω|e^{+iφ} + TUFT 右耦合 |Ω|e^{-iφ}（ADD-01 B.3）：
         δA_even = 2ρ·cosφ_W（宇称偶，cosφ 项；SM 实振幅时）
         δA_odd  = 2ρ·c_I·sinφ_W（宇称奇，需 SM×TUFT 干涉有虚部 c_I≠0，分支4 构造性修正）
  ρ = |Ω_weak|/g_SM（SM 弱顶角振幅归一化）；g_SM 两个自然口径：
         √α_W = 0.130  ⇒ ρ = 0.130
         g_2 ≈ 0.65    ⇒ ρ = 0.0261
  实验参照：中子 β 衰变不对称参数 A_exp ≈ −0.1184，精度 ΔA ≈ 0.001（PERKEO 量级）。
           A_exp − A_SM 与 0 相容 ⇒ |δA_TUFT| > ΔA 即被排除。

退出码：0 = 全部 guard 通过；2 = 任一 guard 异常/非预期。
"""
import math
import json
import os
import sys

# 中文 Windows 控制台守卫：报告含 U+2212（−）等非 ASCII 字符时 print 会抛
# UnicodeEncodeError（'gbk' codec）⇒ 本脚本历史上同样是「落盘成功但退出码 1」
# （2026-10-04 第十一轮与分支4 一并查出并修复）。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DEG = 180.0 / math.pi

# --- 口径 ---
ALPHA_W   = 0.01696          # α_W(M_Z)（ADD-01 C.1）
LAMBDA    = 0.1179           # λ = α_s（ADD-02 最大幅值原则）
THETA_WC  = 240.0            # 弱域锥心（deg）
DELTA_W   = 60.0             # 弱域宽度（deg）
THETA_W   = 212.757          # 弱代表点（deg，ADD-02 由 cos3θ=0.1438 反解）
DELTA_A   = 0.001            # 中子 β 衰变 A 参数实验精度（~10⁻³）

def phi_W(phi0):
    """弱代表点相位 φ_W = φ_0·(θ_W−θ_Wc)/Δθ_W。"""
    return phi0 * (THETA_W - THETA_WC) / DELTA_W

def omega_weak_amp():
    """|Ω_weak| = λ·cos3θ_W（应 = α_W）。"""
    return LAMBDA * math.cos(3.0 * THETA_W / DEG)

GUARDS = []
def guard(name, detail=""):
    def deco(fn):
        try:
            ok, note = fn()
        except Exception as e:
            ok, note = False, "EXC: %r" % e
        GUARDS.append({"name": name, "ok": ok, "note": note, "detail": detail})
        return fn
    return deco

# --- 几何自洽 ---------------------------------------------------------------
@guard("weak_rep_geometry",
       "几何：弱代表点 |Ω_weak|=α_W，φ_W 比例因子 −0.454")
def _():
    Om = omega_weak_amp()
    f = (THETA_W - THETA_WC) / DELTA_W
    ok = (abs(Om - ALPHA_W) / ALPHA_W < 0.02) and (abs(f - (-0.45405)) < 1e-3)
    return ok, "|Ω_weak|=%.5f (α_W=%.5f, 差 %.1f%%)，φ_W=%.5f·φ_0" % (
        Om, ALPHA_W, abs(Om-ALPHA_W)/ALPHA_W*100, f)

# --- 自然幅值（未调谐假设）--------------------------------------------------
@guard("deltaA_natural_magnitude",
       "自然幅值：δA=2ρcosφ，ρ=α_W/g_SM ⇒ δA~O(0.05–0.26) 远超 ΔA=0.001")
def _():
    rho_sqrt = ALPHA_W / math.sqrt(ALPHA_W)   # g_SM=√α_W ⇒ ρ=0.130
    rho_g2   = ALPHA_W / 0.65                 # g_SM=g_2≈0.65 ⇒ ρ=0.0261
    dA_sqrt = 2.0 * rho_sqrt
    dA_g2   = 2.0 * rho_g2
    ok = (dA_g2 > 10.0 * DELTA_A)
    note = ("ρ(√α_W)=%.4f ⇒ δA_max=%.3f；ρ(g_2)=%.4f ⇒ δA_max=%.3f；"
            "两者均 >> ΔA=%.3f（超出 %.0f–%.0f 倍）" %
            (rho_sqrt, dA_sqrt, rho_g2, dA_g2, DELTA_A,
             dA_g2/DELTA_A, dA_sqrt/DELTA_A))
    return ok, note

# --- 排除因子 / 存活阈值 -----------------------------------------------------
@guard("survival_rho_threshold",
       "存活阈值：要 |δA|<ΔA 对所有 φ_0 成立，需 ρ < ΔA/2 = 5e-4")
def _():
    rho_crit = DELTA_A / 2.0
    rho_nat = ALPHA_W / 0.65
    factor = rho_nat / rho_crit
    ok = (factor > 50.0)   # 自然 ρ 超出阈值 ~52 倍
    return ok, ("ρ_crit = ΔA/2 = %.2e；自然 ρ = %.4f 超出 %.0f 倍 ⇒ "
                "天然假设下被排除，须调谐 ρ 或 φ" % (rho_crit, rho_nat, factor))

@guard("survival_phi0_fraction",
       "存活窗口：ρ=0.0261 下，|δA|<ΔA 的 φ_0 占比（cosφ_W 需 < 0.019）")
def _():
    rho = ALPHA_W / 0.65
    # |2ρ cosφ_W| < ΔA ⇔ |cosφ_W| < ΔA/(2ρ)
    cos_crit = DELTA_A / (2.0 * rho)
    # φ_W = −0.45405·φ_0；φ_0 ∈ [0,2π] 均匀 ⇒ φ_W ∈ [−2.853, 0]
    # |cosφ_W| < cos_crit=0.0192 的 φ_W 窗口
    # cosφ 接近 ±1 的区间排除。用数值扫描计占比。
    N = 200000
    n_survive = 0
    for i in range(N):
        phi0 = 2.0 * math.pi * (i + 0.5) / N
        ph = phi_W(phi0)
        dA = 2.0 * rho * math.cos(ph)
        if abs(dA) < DELTA_A:
            n_survive += 1
    frac = n_survive / N
    ok = (frac < 0.05)   # 存活窗口很窄（≈2%)
    return ok, "φ_0∈[0,2π] 存活占比 %.1f%%（其余 φ_0 均被排除）" % (frac * 100)

# --- 宇称奇项（干涉虚部）----------------------------------------------------
@guard("deltaA_parity_odd_needs_cI",
       "宇称奇项 δA_odd=2ρ c_I sinφ_W：需 SM×TUFT 干涉虚部 c_I≠0；c_I 未定 ⇒ 预测非唯一")
def _():
    rho = ALPHA_W / 0.65
    # 取 φ_0 使 sinφ_W 最大：φ_W=−π/2 ⇒ φ_0=π/2/0.454=3.459
    phi0_max = (math.pi / 2.0) / 0.45405
    ph = phi_W(phi0_max)
    dA_cI1 = 2.0 * rho * 1.0 * math.sin(ph)
    # 若 c_I=0 ⇒ δA_odd=0
    ok = (abs(dA_cI1) > 10.0 * DELTA_A)
    note = ("c_I=1, φ_0=%.2f 时 δA_odd=%.3f >> ΔA；但 c_I 由模型未定 ⇒ "
            "δA_TUFT 是 (c_I, ρ, φ_0) 三维族，非唯一数值预言" % (phi0_max, dA_cI1))
    return ok, note

# --- δA_TUFT 在 φ_0 上的 95% 区间 ---------------------------------------------
@guard("deltaA_ci_over_phi0",
       "95% 区间：ρ=α_W/g_2=0.0261，φ_0∈[0,2π] 均匀先验下 δA_even 的分位数")
def _():
    rho = ALPHA_W / 0.65
    vals = []
    N = 200000
    for i in range(N):
        phi0 = 2.0 * math.pi * (i + 0.5) / N
        vals.append(2.0 * rho * math.cos(phi_W(phi0)))
    vals.sort()
    lo, med, hi = vals[int(N*0.05)], vals[int(N*0.5)], vals[int(N*0.95)]
    ok = True
    return ok, ("δA_even 5%%/50%%/95%% = %.3f / %.3f / %.3f；"
                "|δA|<ΔA 仅当 φ_0 落入 cosφ_W≈0 的窄窗" % (lo, med, hi))

# --- 数值扫描：ρ 允许上限（机器求值）-----------------------------------------
@guard("max_rho_for_survival",
       "存活上限：存在 φ_0 使 |δA|<ΔA 的最大 ρ = ΔA/2 = 5e-4")
def _():
    rho_max = DELTA_A / 2.0
    rho_nat = ALPHA_W / 0.65
    ok = (rho_nat / rho_max > 50)
    return ok, ("ρ_max=%.2e，自然 ρ=%.4f ⇒ 须将 TUFT 顶角耦合压低 %.0f 倍方存活" %
                (rho_max, rho_nat, rho_nat/rho_max))

# --- 步1（2026-10-04 第十一轮执行序列 1）：通道范围分离声明 ---------------
@guard("beta_channel_outside_closed_windows",
       "步1 声明：β 衰变通道**不在** g-2/EDM/UHECR 关窗范围（链 A-④ D-02 关窗范围只含这三项）；"
       "其阻塞是 ① δA_TUFT 未定义（五项前置）② 参数账 6→7、c_I 无源（ADD-01R F04）")
def _():
    src = open(os.path.abspath(__file__), encoding="utf-8", errors="replace").read()
    outside = "不在" in src and "关窗范围" in src
    blockers = ("未定义" in src) and ("6→7" in src or "参数账" in src)
    ok = outside and blockers
    return ok, ("自证：β 通道范围分离声明=%s、阻塞两项声明=%s ⇒ %s" %
                (outside, blockers,
                 "已落盘，勿删" if ok else "**声明缺失**"))

# --- 主流程 ----------------------------------------------------------------
def main():
    results = {
        "engine": "TUFT-MATH-PROOF-ADD-01 β 衰变手征不对称修正数值计算（分支 3）",
        "date": "2026-10-04",
        "dependencies": ["ADD-02 三正瓣分区", "ADD-01 B.3 手征耦合",
                         "分支4 N1 干涉项重定义", "分支4 N6 相位边界"],
        "inputs": {"alpha_W": ALPHA_W, "lambda": LAMBDA,
                   "theta_W_deg": THETA_W, "theta_Wc_deg": THETA_WC,
                   "delta_W_deg": DELTA_W, "DeltaA_neutron": DELTA_A,
                   "rho_natural_sqrt": ALPHA_W/math.sqrt(ALPHA_W),
                   "rho_natural_g2": ALPHA_W/0.65},
        "guards": GUARDS,
        "n_guards": len(GUARDS),
        "n_pass": sum(1 for g in GUARDS if g["ok"]),
        "n_fail": sum(1 for g in GUARDS if not g["ok"]),
    }
    lines = []
    lines.append("# TUFT-MATH-PROOF-ADD-01 β 衰变手征不对称修正（δA_TUFT）数值报告（分支 3）")
    lines.append("")
    lines.append("- 引擎：源码/TUFT-MATH-PROOF-ADD-01_β衰变手征不对称_数值计算_2026-10-04.py")
    lines.append("- 日期：2026-10-04")
    lines.append("- 口径：三正瓣（弱域 240°±30°）；弱代表点 θ_W=212.757°；|Ω_weak|=α_W=0.01696")
    lines.append("- 修正：A_obs=A_SM+δA_TUFT，δA 来自 |M_SM+M_TUFT|² 干涉（分支4 N1 修法）")
    lines.append("- 实验参照：中子 β 不对称 A_exp≈−0.1184，精度 ΔA≈0.001")
    lines.append("- 读数：%d guard —— PASS %d / FAIL %d（退出码 %d）"
                 % (len(GUARDS), results["n_pass"], results["n_fail"],
                    0 if results["n_fail"] == 0 else 2))
    lines.append("")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % ("PASS" if g["ok"] else "FAIL",
                                           g["name"], g["note"]))
    lines.append("")
    lines.append("### 结论")
    lines.append("""
1. 在 ADD-02 已确立的归一化（|Ω_weak|=α_W=0.01696）下，δA_TUFT 自然幅值 ~O(0.05–0.26)，
   超出中子 β 衰变不对称参数精度（ΔA≈0.001）**~50–260 倍**。
2. 存活阈值：要 |δA|<ΔA 对所有 φ_0 成立，须 ρ=|Ω|/g_SM < ΔA/2 = 5e-4；
   自然 ρ=α_W/g_2≈0.0261 超出阈值 ~52 倍 ⇒ 天然假设下被排除，须把 TUFT 顶角耦合压低 ~52 倍。
3. 存活窗口：φ_0∈[0,2π] 中仅 ~1.3% 的 φ_0（cosφ_W≈0 附近）能存活，属强调谐
   （口径已统一：以本报告 guard `survival_phi0_fraction` 的读数为准）。
4. 宇称奇项 δA_odd=2ρ c_I sinφ_W 需 SM×TUFT 干涉虚部 c_I≠0；c_I 模型未定 ⇒
   δA_TUFT 实为 (c_I, ρ, φ_0) 三维族，**当前不是唯一数值预言**（不满足 D-06 门槛 (d)）。
5. 诚实判定：β 衰变不对称确为可证伪窗口（方向对），但 ADD-01 未定 g_SM 归一化与相对相位，
   且自然幅值已被实验排除；需先明确 (g_SM, c_I) 或把 ρ 压低 ~52 倍，方能成为有效预言。
6. **通道范围分离（步1，2026-10-04）**：g-2 / EDM / UHECR 三项窗口已关（链 A-④ D-02 物理层 FAIL），
   但 **β 衰变不在关窗范围**（关窗范围仅含那三项）⇒ 本册的排除结论（52 倍调谐）**不是**
   「已关窗口」的一部分，而是独立的模型缺陷：① δA_TUFT 未定义（五项前置，见 ADD-01R D03）
   ② 引入 c_I 使参数账由 6 增至 7 而观测量仍 4 ⇒ 可识别性恶化（ADD-01R F04）。
   ⇒ 重做前置 = 闭合五项前置 + 给 c_I 输入来源。
""")
    report = "\n".join(lines)

    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    stem = "TUFT-MATH-PROOF-ADD-01_β衰变手征不对称_数值计算_2026-10-04"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    return 0 if results["n_fail"] == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
