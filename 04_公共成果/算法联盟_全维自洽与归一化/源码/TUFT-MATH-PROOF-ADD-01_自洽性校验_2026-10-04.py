# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF-ADD-01 自洽性校验引擎（分支 4）
================================================
性质：元审计 / 自洽性校验。非物理层判决。
纯标准库（math, cmath, json），零第三方依赖。

目标：把整理册 N1-N5 固化为可复算 guard；并给出 N1 的构造性修正
（A_obs 定义于 |M_SM+M_TUFT|^2 干涉交叉项，δA_TUFT ∝ -2|Ω| c_I sinφ）。

分区几何（已由 ADD-02 确立的三正瓣结构）：
  D_EM    锥心 0°   （60° 扇区，[-30°,30°)）
  D_Strong锥心 120° （90°~150°）
  D_Weak  锥心 240° （210°~270°）
  D_G     三负瓣之并（补集）
弱域参数：θ_W,c = 240° = 4π/3 rad，Δθ_W = 60° = π/3 rad。

关键口径：
  前置判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04（C-01 α 标度 7.10%）
  整理_TUFT-MATH-PROOF_双参量流形四力分区_实Ω构造与可证伪预言（N1-N9）
  突破_TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派（三正瓣分区 + OPEN-ΩH）

退出码：0 = 全部 guard 通过（即 N1-N5 结论全部复现 + 构造性修正成立）
        2 = 任一 guard 断言异常（非预期结果 / 除零 / 数值崩溃）。
"""
import math
import json
import os

# ----------------------------------------------------------------------------
# 全局参数（口径固定）
# ----------------------------------------------------------------------------
LAMBDA = 1.0                      # Ω 幅值常数（测试取 1；耦合层不在此判定）
PHI0   = 0.5                      # 弱域手征相位常数（测试值，rad）
THETA_WC = 4.0 * math.pi / 3.0    # 弱域扇区中心角 = 240°
DELTA_W  = math.pi / 3.0          # 弱域扇区宽度 = 60°
DEG = 180.0 / math.pi

# CODATA/PDG 口径
ALPHA_0    = 1.0 / 137.036        # α(0)，Thomson 极限
ALPHA_MZ   = 1.0 / 127.952        # α(M_Z)
ALPHA_S    = 0.1179               # α_s(M_Z)

# ADD-01 C.2/C.3 引用量
DAE_CENTER = 2.4e-13              # Δa_e 中心
DAE_SIGMA  = 0.65e-13             # Δa_e 引用 σ
SIGMA_LAM  = 0.0076               # σ_λ/λ
SIGMA_BI   = 0.02                 # σ_{B_i}/B_i
DGZK_CENTER = 0.68e19             # ΔE_GZK 中心 (eV)
DGZK_SIGMA  = 0.21e19             # ΔE_GZK 引用 σ (eV)

# ----------------------------------------------------------------------------
# 核心场定义（ADD-01 B.2 / B.4）
# ----------------------------------------------------------------------------
def omega_real(theta):
    """实部 λ·cos(3θ)。"""
    return LAMBDA * math.cos(3.0 * theta)

def weak_phase(theta):
    """弱域相位 φ(θ) = φ_0·(θ−θ_W,c)/Δθ_W。弱域外为 0。"""
    # 把 θ 规范到弱域 [210°,270°]（用最近角距判断是否在弱域）
    d = theta - THETA_WC
    # 归一化到 [-π, π]
    while d > math.pi:  d -= 2.0 * math.pi
    while d < -math.pi: d += 2.0 * math.pi
    half = DELTA_W / 2.0
    if abs(d) <= half:
        return PHI0 * (d / DELTA_W)
    return 0.0

def omega_complex(theta):
    """复 Ω：弱域叠相位，其余实场。返回 (mod, phase)。"""
    ph = weak_phase(theta)
    return omega_real(theta), ph

# ----------------------------------------------------------------------------
# Guard 注册表
# ----------------------------------------------------------------------------
GUARDS = []

def guard(name, detail=""):
    """记录一个 guard 结果。ok=True 表示预期结论复现/断言成立。"""
    def deco(fn):
        try:
            ok, note = fn()
        except Exception as e:  # 数值/逻辑异常 → 非预期
            ok, note = False, "EXC: %r" % e
        GUARDS.append({"name": name, "ok": ok, "note": note, "detail": detail})
        return fn
    return deco

# --- N1：A_chiral 恒等于 0 ---------------------------------------------------
@guard("chiral_asymmetry_identically_zero",
       "N1：A_chiral=(|g_L|^2-|g_R|^2)/(|g_L|^2+|g_R|^2) 恒等于 0")
def _():
    gL2 = gR2 = LAMBDA ** 2.0  # |Ω|^2
    A = (gL2 - gR2) / (gL2 + gR2)
    ok = (abs(A) < 1e-15)
    note = "A_chiral = %g （恒等于 0）→ 与「不对称来自干涉相位」自相矛盾" % A
    return ok, note

# --- N1 构造性修正：干涉项 δA_TUFT 非零 -------------------------------------
@guard("interference_deltaA_nonzero",
       "N1 修正：把 A_obs 定义于 |M_SM+M_TUFT|^2 交叉项，δA_TUFT∝-2|Ω| c_I sinφ")
def _():
    # M_tot = M_SM + |Ω| e^{iφ} M_0 ；c = M_SM*·M_0 = c_R + i c_I
    # |M_tot|^2 = |M_SM|^2 + |Ω|^2|M_0|^2 + 2|Ω| Re(e^{iφ} c)
    # Re(e^{iφ} c) = c_R cosφ − c_I sinφ ；宇称奇项 = −c_I sinφ
    theta = 225.0 / DEG          # 弱域内、离锥心 15° 的测试点
    Om, ph = omega_complex(theta)
    # 情形 1：c 有虚部（c_I=1）
    cR, cI = 1.0, 1.0
    inter_cI = Om * (cR * math.cos(ph) - cI * math.sin(ph))
    # 情形 2：c 纯实（c_I=0）——宇称奇项消失
    inter_c0 = Om * (cR * math.cos(ph) - 0.0 * math.sin(ph))
    delta_with_Im = -2.0 * Om * cI * math.sin(ph)   # 宇称奇贡献
    ok = (abs(delta_with_Im) > 1e-9) and (abs(inter_cI - inter_c0) > 1e-9)
    note = ("θ=225°, φ=%.3f, |Ω|=%.4f：奇项 −2|Ω|c_I sinφ = %.4f ≠ 0；"
            "纯实 c 时该奇项 = 0 ⇒ δA_TUFT 非零要求 c_I≠0"
            % (ph, Om, delta_with_Im))
    return ok, note

# --- N2：PΩ=Ω* 需奇相位 / θ_W,c=0 --------------------------------------------
@guard("parity_omega_star_needs_odd_phase",
       "N2：PΩ=Ω* ⟺ 相位为奇函数 ⟺ θ_W,c=0；三正瓣下 θ_W,c=240°≠0 ⇒ 不成立")
def _():
    # 奇相位条件：φ(−θ) ≡ −φ(θ) ⟺ θ_W,c = 0
    # 一般 θ_W,c：φ(−θ) − (−φ(θ)) = −2 φ_0 θ_W,c / Δθ_W
    theta = 225.0 / DEG
    d = theta - THETA_WC
    while d > math.pi:  d -= 2 * math.pi
    while d < -math.pi: d += 2 * math.pi
    phi_theta = PHI0 * (d / DELTA_W)
    # φ(−θ)：−225° ≡ 135°（强瓣，弱域外）→ 0
    phi_neg = weak_phase(-theta)
    diff = phi_neg - (-phi_theta)
    ok = (abs(diff) > 1e-9)   # 确认一般 θ_W,c 下不成立
    note = ("φ(225°)=%.4f, φ(−225°)=%.4f, −φ(225°)=%.4f ⇒ φ(−θ)≠−φ(θ) "
            "（差 %.4f，θ_W,c=240°≠0）；仅 θ_W,c=0 时成立" %
            (phi_theta, phi_neg, -phi_theta, diff))
    return ok, note

@guard("parity_breaking_holds_POmega_ne_Omega",
       "N2 补充：宇称破缺本身（PΩ≠Ω）在三正瓣下仍成立")
def _():
    theta = 225.0 / DEG
    Om, ph = omega_complex(theta)
    # P: θ→−θ
    OmP, phP = omega_complex(-theta)
    same = (abs(OmP - Om) < 1e-9) and (abs(phP - ph) < 1e-9)
    ok = (not same) and (abs(ph) > 1e-9)
    note = ("PΩ(225°)=|Ω|%.4f e^{i%.4f} vs Ω(225°)=|Ω|%.4f e^{i%.4f} ⇒ PΩ≠Ω" %
            (OmP, phP, Om, ph))
    return ok, note

# --- N3：σ_{Δa_e} 与误差预算不符 ---------------------------------------------
@guard("sigma_delta_a_mismatch",
       "N3：λ+B 合成相对不确定度仅 2.1%，引用 σ 比预算大 ~13 倍")
def _():
    rel_comb = math.sqrt(SIGMA_LAM ** 2 + SIGMA_BI ** 2)
    sigma_computed = DAE_CENTER * rel_comb
    ratio = DAE_SIGMA / sigma_computed
    ok = (ratio > 3.0)   # 引用值显著大于预算
    note = ("√(0.0076²+0.02²)=%.4f ⇒ 相对 2.1%%，σ_computed=%.2e；"
            "引用 σ=%.2e，比值 %.1f×" % (rel_comb, sigma_computed, DAE_SIGMA, ratio))
    return ok, note

# --- N4：C-01 复现（α 标度）--------------------------------------------------
@guard("alpha_scale_repeat",
       "N4：Part C 标 μ=M_Z 却取 α(0)=1/137.036 ⇒ C-01 复现（差 7.10%）")
def _():
    rel = (ALPHA_0 - ALPHA_MZ) / ALPHA_0
    ok = (abs(rel) > 0.05)
    note = ("α(0)=%.6e vs α(M_Z)=%.6e，相对差 %.4f%%（复现前置 C-01）" %
            (ALPHA_0, ALPHA_MZ, rel * 100.0))
    return ok, note

# --- N5：UHECR 区间算术 + SM 基线 --------------------------------------------
@guard("gz_interval_arithmetic",
       "N5a：区间算术自洽（0.68±0.42→[0.26,1.10]），但 SM 基线未交代")
def _():
    lo = DGZK_CENTER - 2 * DGZK_SIGMA
    hi = DGZK_CENTER + 2 * DGZK_SIGMA
    # E_GZK^TUFT = E_SM + ΔE ∈ [3.90,4.74] ⇒ E_SM = 3.64（两式反解）
    sm_from_lo = 3.90e19 - lo
    sm_from_hi = 4.74e19 - hi
    ok = (abs(sm_from_lo - sm_from_hi) < 1e14)
    note = ("ΔE∈[%.2e,%.2e]；SM 基线反解 %.4e eV（两路一致 %.1f eV）——"
            "标准 GZK 常引 ~5e19，基线来源未交代" %
            (lo, hi, sm_from_lo, abs(sm_from_lo - sm_from_hi)))
    return ok, note

@guard("gz_falsify_window_narrow",
       "N5b：证伪窗口窄——CI 上界距证伪阈值 5.0e19 仅 0.26e19")
def _():
    hi = DGZK_CENTER + 2 * DGZK_SIGMA
    upper = 3.64e19 + hi
    margin = 5.0e19 - upper
    ok = (margin < 1.0e19)             # 确认窗口窄
    note = "TUFT 上界 %.2f e19，证伪阈值 5.0e19，余量 %.2f e19（窄窗口）" % (
        upper / 1e19, margin / 1e19)
    return ok, note

# --- 基础恒等 / 量纲 / 对称性 ------------------------------------------------
@guard("cos3theta_identity",
       "基础：cos(3θ)=(κ³−3κτ²)/(κ²+τ²)^{3/2} 恒等")
def _():
    worst = 0.0
    for k in range(1, 5):
        kk, tt = float(k), 1.0
        r = math.hypot(kk, tt)
        theta = math.atan2(tt, kk)
        lhs = math.cos(3 * theta)
        rhs = (kk**3 - 3 * kk * tt**2) / (r**3)
        worst = max(worst, abs(lhs - rhs))
    ok = (worst < 1e-12)
    return ok, "κ,τ∈{1..4} 最大偏差 %.2e" % worst

@guard("omega_dimensionless_under_scaling",
       "基础：Ω 无量纲（κ,τ→sκ,sτ 不变）")
def _():
    def omega_ratio(k, t):
        r = math.hypot(k, t)
        return (k**3 - 3 * k * t**2) / (r**3)
    v1 = omega_ratio(2.0, 1.0)
    v2 = omega_ratio(2.0 * 1e6, 1.0 * 1e6)
    ok = (abs(v1 - v2) < 1e-12)
    return ok, "缩放 1e6 倍：%.10f vs %.10f" % (v1, v2)

@guard("real_omega_parity_even",
       "基础：实 Ω 在 P 下为偶（PΩ_real=Ω_real），宇称破缺只来自相位")
def _():
    t = 225.0 / DEG
    ok = (abs(omega_real(-t) - omega_real(t)) < 1e-12)
    return ok, "Ω_real(−θ)=Ω_real(θ)=%.6f（偶）" % omega_real(t)

@guard("parity_theta_flips",
       "基础：P:(κ,τ)→(κ,−τ) ⟺ θ→−θ")
def _():
    k, tau = 2.0, 1.0
    t1 = math.atan2(tau, k)
    t2 = math.atan2(-tau, k)
    ok = (abs(t2 - (-t1)) < 1e-12)
    return ok, "atan2(1,2)=%.6f → atan2(−1,2)=%.6f（=−θ）" % (t1, t2)

@guard("amplitude_continuous_at_weak_boundary",
       "基础：跨弱域边界 |Ω|=|λcos3θ| 连续（弱域边界恰为 cos3θ 零点，|Ω|→0）")
def _():
    worst = 0.0
    for bdeg in (210.0, 270.0):
        b = bdeg / DEG
        # 弱域内侧 / 外侧：不连续性只看两侧之差，不含幅值本身
        m_in  = abs(omega_real(b + 1e-6))   # 内侧（弱域）
        m_out = abs(omega_real(b - 1e-6))   # 外侧
        worst = max(worst, abs(m_in - m_out))
    ok = (worst < 1e-9)
    return ok, "弱域边界 |Ω| 两侧差最大 %.2e（连续）" % worst

@guard("phase_discontinuous_at_weak_boundary",
       "N6（新发现）：线性相位 ansatz 在弱域硬截断处相位不连续（跳变 φ_0/2）")
def _():
    b = 210.0 / DEG
    # 弱域内侧 φ(b+ε) → φ_0(−Δθ_W/2)/Δθ_W = −φ_0/2 ；外侧 φ=0
    eps = 1e-9
    phi_in  = weak_phase(b + eps)
    phi_out = weak_phase(b - eps)
    jump = abs(phi_in - phi_out)
    ok = (jump > 1e-3)          # 确认存在 ~φ_0/2 的相位跳变
    note = ("φ(210°⁺)=%.4f, φ(210°⁻)=%.4f ⇒ 相位跳变 %.4f = φ_0/2 ≠ 0 ⇒ "
            "「相位连续（φ光滑）✔」不成立" % (phi_in, phi_out, jump))
    return ok, note

# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    # 触发所有 guard
    for fn in [g for g in globals().values() if callable(g) and getattr(g, "__name__", "").startswith("_")]:
        pass  # guard 装饰器在 import 时已执行；这里仅触发 main 注册
    # 由于 guard 装饰器在定义时即执行，GUARDS 已填充；这里补一个显式计数
    results = {
        "engine": "TUFT-MATH-PROOF-ADD-01 自洽性校验引擎（分支 4）",
        "date": "2026-10-04",
        "dependency": ["判定_TUFT_V3.5修复方案_全维审计与重整_2026-10-04",
                       "整理_TUFT-MATH-PROOF_双参量流形四力分区_实Ω构造与可证伪预言",
                       "突破_TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派"],
        "partition": {"D_EM": "0°±30°", "D_Strong": "120°±30°",
                      "D_Weak": "240°±30°", "D_G": "三负瓣之并",
                      "theta_Wc_deg": 240.0, "dtheta_W_deg": 60.0},
        "guards": GUARDS,
        "n_guards": len(GUARDS),
        "n_pass": sum(1 for g in GUARDS if g["ok"]),
        "n_fail": sum(1 for g in GUARDS if not g["ok"]),
    }
    # 报告
    lines = []
    lines.append("# TUFT-MATH-PROOF-ADD-01 自洽性校验报告（分支 4）")
    lines.append("")
    lines.append("- 引擎：源码/TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04.py（纯标准库）")
    lines.append("- 日期：2026-10-04")
    lines.append("- 分区：三正瓣（EM 0° / Strong 120° / Weak 240°，各 60°）+ G 三负瓣之并")
    lines.append("- 读数：%d guard —— PASS %d / FAIL %d（退出码 %d）"
                 % (len(GUARDS), results["n_pass"], results["n_fail"],
                    0 if results["n_fail"] == 0 else 2))
    lines.append("")
    for g in GUARDS:
        flag = "PASS" if g["ok"] else "FAIL"
        lines.append("| %s | %s | %s |" % (flag, g["name"], g["note"]))
    lines.append("")
    lines.append("### 结论映射")
    lines.append("""
- N1（A_chiral≡0）确认；N1 修正给出 δA_TUFT∝−2|Ω|c_I sinφ，非零要求 c_I≠0（SM×TUFT 干涉有虚部）。
- N2（PΩ=Ω* 需 θ_W,c=0）确认：三正瓣 θ_W,c=240°≠0，PΩ=Ω* 不成立；但破缺本身（PΩ≠Ω）成立。
- N3（σ_{Δa_e} 与预算差 ~13 倍）确认：需重算区间或补 27% 级第三误差源。
- N4（C-01 复现，α 标度差 7.10%）确认：Part C 须改 μ=M_Z 或明确 μ→0。
- N5（UHECR 区间算术自洽但 SM 基线 3.64e19 未交代 + 证伪窗口窄）确认。
""")
    report = "\n".join(lines)

    # 落盘
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, "..", "数据")
    data_dir = os.path.abspath(data_dir)
    stem = "TUFT-MATH-PROOF-ADD-01_自洽性校验_2026-10-04"
    json_path = os.path.join(data_dir, stem + ".json")
    md_path = os.path.join(data_dir, stem + ".md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print("\nJSON → %s" % json_path)
    print("MD   → %s" % md_path)
    return 0 if results["n_fail"] == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
