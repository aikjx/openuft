# -*- coding: utf-8 -*-
"""
GAQ-UFT P0 攻坚：螺旋系综引力涌现模型
====================================
目标：为候选公式  G = Γ · n_w · R^2 · c^2 · tanθ
      中缺失的 [L^2 M^-1] 几何因子 Γ 提供一个来自"系综统计涌现"的建模，
      并诚实检验维度闭合与数值是否真正闭合（还是套代）。

关键认识论边界（反复强调）：
  - 这是"建模/ansatz"，不是第一性原理已证推导；
  - 若用 Planck 单位构造 Γ，会因 l_P、m_P 内含 G 而变成恒等式（套代），
    数值上无法独立预测 G，只能验证维度自洽；
  - 真正的闭合要求 n_w、L_0、R 由**非 G 输入**（如 α、真空零点能密度）
    独立确定 —— 这是剩余 OPEN 项。
"""
import mpmath as mp
import json

mp.mp.dps = 80

RESULTS = {"tests": [], "bugs": [], "open_notes": []}


def record(name, status, detail, data=None):
    RESULTS["tests"].append({"name": name, "status": status, "detail": detail})
    tag = {"PASS": "PASS", "OPEN": "OPEN", "BUG": "BUG", "INFO": "INFO"}.get(status, status)
    print(f"[{tag}] {name}: {detail}")


# ---- 物理常数 (CODATA-2022 近似值) ----
G_COD = mp.mpf("6.67430e-11")      # m^3 kg^-1 s^-2
c = mp.mpf("299792458")            # m/s
hbar = mp.mpf("1.054571817e-34")   # J*s
alpha = mp.mpf("7.2973525693e-3")  # 精细结构常数
epsilon0 = mp.mpf("8.8541878128e-12")


def planck_units():
    """Planck 长度、质量、时间（内含 G，用于检验套代）。"""
    l_P = mp.sqrt(hbar * G_COD / (c ** 3))
    m_P = mp.sqrt(hbar * c / G_COD)
    t_P = mp.sqrt(hbar * G_COD / (c ** 5))
    return l_P, m_P, t_P


# ---------------------------------------------------------------------------
# 模型 1：几何因子 Γ = β · L0^2 / M0  （系综相关长度^2 / 特征质量）
# 维度：[L0^2/M0] = [L^2 M^-1]  ✓ 正是缺失的维度
# ---------------------------------------------------------------------------
def model_geometric_factor(L0, M0, beta=mp.mpf("1")):
    return beta * (L0 ** 2) / M0


# ---------------------------------------------------------------------------
# 模型 2：完整候选公式 + 系综密度假设
#   n_w ~ 1 / L0^3   （每 Planck 关联胞一个螺旋链）
#   R   ~ L0         （真空曲率尺度取关联长度）
# ---------------------------------------------------------------------------
def G_from_ensemble(L0, M0, beta, theta=mp.atan(alpha)):
    """theta 是螺旋升角；框架定义 tan(theta)=alpha，故 theta=atan(alpha)。
    注意：不要直接传 theta=alpha 再取 tan —— 那会得到 tan(alpha)≠alpha（差 ~alpha^3/3）。"""
    Gamma = model_geometric_factor(L0, M0, beta)
    n_w = mp.mpf("1") / (L0 ** 3)
    R = L0
    return Gamma * n_w * (R ** 2) * (c ** 2) * mp.tan(theta)


def main():
    l_P, m_P, t_P = planck_units()
    record("Planck 单位基准",
           "INFO",
           f"l_P={float(l_P):.4e} m, m_P={float(m_P):.4e} kg, t_P={float(t_P):.4e} s")

    # --- T-E1: Γ 维度核验（解析）---
    # [L0^2/M0] = [L^2 M^-1]，与所需一致 → 维度闭合
    record("T-E1 Γ=L0^2/M0 维度闭合",
           "PASS",
           "Γ 维度 = [L^2 M^-1]，与候选公式缺失维度完全一致 → 维度层面已闭合")

    # --- T-E2: 取 L0=l_P, M0=m_P, β=1 → 自洽检验 ---
    # G = (l_P^2/m_P) * (1/l_P^3) * l_P^2 * c^2 * tanθ
    #   = tanθ * c^2 * (l_P^2 * l_P^2)/(m_P * l_P^3)
    #   = tanθ * c^2 * l_P / m_P
    # 而 l_P/m_P = G_COD/c^2  （由 Planck 定义直接可得）→ G = tanθ * G_COD
    # ⇒ 要求 β = 1/tanθ ≈ 1/α 才能使 G==G_COD
    theta = mp.atan(alpha)  # 框架定义 tanθ=α ⇒ θ=atan α（不要直接传 alpha！）
    G_model = G_from_ensemble(l_P, m_P, mp.mpf("1"), theta)
    ratio_self = G_model / G_COD
    # 理论预期：G_model/G_COD = tanθ ≡ α  （当 β=1 时）
    record("T-E2 套代自洽 (L0=l_P,M0=m_P,β=1)",
           "PASS" if abs(ratio_self - alpha) < mp.mpf("1e-30") else "BUG",
           f"G_model/G_COD = {float(ratio_self):.6e}, 理论预期=α={float(alpha):.6e} "
           f"→ 数值上 G_model = α·G_COD（套代，未独立预测）")

    # --- T-E3: 求 β 使 G==G_COD（构造性标定，非预测）---
    beta_needed = alpha ** (-1)   # 因为 G_model ∝ β·α·G_COD
    G_cal = G_from_ensemble(l_P, m_P, beta_needed, theta)
    dev = abs(G_cal - G_COD) / G_COD
    record("T-E3 β=1/α 标定闭合",
           "OPEN",
           f"需 β={float(beta_needed):.4f}=1/α 才使 G=G_COD；回代偏差={float(dev):.2e}"
           f" —— 这是构造标定，因 l_P,m_P 已含 G（套代），不构成独立预测")

    # --- T-E4: 套代暴露测试（用不含 G 的 L0,M0 假设能否独立定 G）---
    # 若改用纯几何/量子假设 L0 = hbar/(m_e c) (Compton), M0 = m_e，
    # 看 G_model 是否还在 CODATA 量级 —— 这是真正"独立输入"的检验。
    m_e = mp.mpf("9.1093837015e-31")
    L0_compton = hbar / (m_e * c)
    M0_e = m_e
    beta_try = alpha ** (-1)
    G_indep = G_from_ensemble(L0_compton, M0_e, beta_try, theta)
    dev_indep = abs(G_indep - G_COD) / G_COD
    record("T-E4 独立输入 (Compton 尺度的 L0,M0) 预测 G",
           "OPEN",
           f"L0=λ_C={float(L0_compton):.3e} m, M0=m_e → G_indep={float(G_indep):.3e}, "
           f"偏离 CODATA {float(dev_indep):.1e} 倍 → 纯几何输入不能复现 G，"
           f"说明 n_w,R 的真实绑定机制仍未找到（核心 OPEN）")

    # --- T-E5: 维度链完整自洽（汇总）---
    # Γ[L^2M^-1] · n_w[L^-3] · R^2[L^2] · c^2[L^2T^-2] · tanθ[1]
    # = [L^2 M^-1 · L^-3 · L^2 · L^2 T^-2] = [L^3 M^-1 T^-2] = [G]  ✓
    record("T-E5 候选公式维度链全闭合",
           "PASS",
           "[Γ][n_w][R^2][c^2][tanθ] = [L^3 M^-1 T^-2] = [G]，维度层面完全自洽")

    # --- 结论性 OPEN 登记 ---
    RESULTS["open_notes"].append(
        "引力 G 的维度已通过 Γ=L0^2/M0 闭合，但数值仍 OPEN："
        "用 Planck 单位构造是套代（l_P,m_P 内含 G）；"
        "用纯几何/Compton 独立输入则远离 CODATA。"
        "真正闭合需由框架独立确定 n_w 与真空曲率尺度 R —— 依赖尚未建立的"
        "系综统计力学/路径积分涌现机制（P0-a）。"
    )
    RESULTS["open_notes"].append(
        "β=1/α 的自洽关系提示：若框架能独立证明 n_w·R^2·c^2·Γ = G/α，"
        "则 α 作为几何种子与 G 的耦合结构成立；但 'G/α' 仍含 G。"
    )

    with open("ensemble_gravity_results.json", "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2, default=str)


if __name__ == "__main__":
    main()
    print("\n=== 摘要 ===")
    n_pass = sum(1 for t in RESULTS["tests"] if t["status"] == "PASS")
    n_open = sum(1 for t in RESULTS["tests"] if t["status"] == "OPEN")
    n_bug = sum(1 for t in RESULTS["tests"] if t["status"] == "BUG")
    print(f"PASS={n_pass}  OPEN={n_open}  BUG={n_bug}")
    if n_bug == 0:
        print("结论：未发现新 bug；引力维度已闭合，数值仍 OPEN（套代/独立输入均不充分）。")
