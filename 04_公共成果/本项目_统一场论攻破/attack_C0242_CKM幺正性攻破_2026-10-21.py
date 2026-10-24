# -*- coding: utf-8 -*-
"""
attack_C0242_CKM幺正性攻破_2026-10-21.py
独立复算：母册 T288「CKM 第一行幺正性 V_ud²+V_us²+V_ub² 偏差 | 树级核矩阵元 | C5,C6」
（L 线域 H 批 · 平方和偏差核算，母册登记撞 C5/C6）

定位：母册 T288（CKM 第一行幺正性检验）。本册**不采信任何自报**，用任务指定 PDG
世界平均值（V_ud=0.97435(16)、V_us=0.22500(67)、V_ub=0.00369(11)）独立精算：
第一行平方和 Σ₁=V_ud²+V_us²+V_ub²、偏差 Δ₁=1−Σ₁、不确定度平方和传播 σ(Δ₁)，
并对比第二行（V_cd²+V_cs²+V_cb²）、Cabibbo 角 θ_C=arctan(V_us/V_ud) 与行正交性，
最后对 TUFT/几何框架判定"是否供给 CKM 混合/幺正结构"。

把"CKM 第一行幺正性检验"压缩成五条可复核读数：

  E1 输入事实（PDG 只引用不复算）：第一行 |V_ud|,|V_us|,|V_ub| 及其误差；
     第二行 |V_cd|,|V_cs|,|V_cb| 及其误差。
  E2 **第一行幺正性核算（本册核心）**：Σ₁、Δ₁=1−Σ₁、误差带 σ(Δ₁)（不确定度平方
     和传播 σ(Δ)=sqrt((2V_udσ_ud)²+(2V_usσ_us)²+(2V_ubσ_ub)²)）、显著性 Δ₁/σ(Δ₁)。
  E3 对比核算：第二行 Σ₂=V_cd²+V_cs²+V_cb²、Δ₂=1−Σ₂、σ(Δ₂)，第一行 vs 第二行。
  E4 Cabibbo 角 θ_C=arctan(V_us/V_ud) 精算（Taylor 级数，Decimal）与 CKM 行
     正交性核算（行1·行2 ≈ V_udV_cd−V_usV_cs+V_ubV_cb·相 残差）。
  E5 裁定：TUFT 无 CKM 混合/无无味结构供给（承接 C0142 E4、C0234 E5）→ 结构性
     负面，按母册 T288 登记撞 C5/C6。

纯标准库（Decimal 48 位 + Fraction 精确交叉核对），零外部依赖、零网络、零随机，
退出码 0。arctan 用 Taylor 级数在 Decimal 域精算（x≈0.23，收敛比 x²≈0.053）；
π 取 50 位硬编码数学常数（非 PDG 输入）。

诚实边界：本册不宣称已解释 CKM 幺正性或味混合；PDG 值只引用不复算；所有数值均为
标准弱作用算术复核，**严禁写成 TUFT 预测/修正**；TUFT 已注销（C0133）。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（PDG 世界平均值，只引用不复算） ----------
# 第一行（任务指定值）
V_UD = Decimal("0.97435")   # |V_ud|  PDG 世界平均
S_UD = Decimal("0.00016")   # σ(|V_ud|)
V_US = Decimal("0.22500")   # |V_us|
S_US = Decimal("0.00067")   # σ(|V_us|)
V_UB = Decimal("0.00369")   # |V_ub|
S_UB = Decimal("0.00011")   # σ(|V_ub|)
# 第二行（PDG，只引用）
V_CD = Decimal("0.221")     # |V_cd|
S_CD = Decimal("0.004")      # σ(|V_cd|)
V_CS = Decimal("0.975")      # |V_cs|
S_CS = Decimal("0.006")     # σ(|V_cs|)
V_CB = Decimal("0.04085")   # |V_cb|
S_CB = Decimal("0.0014")     # σ(|V_cb|)

# 数学常数（非实验输入）：π 50 位
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
RAD2DEG = Decimal("180") / PI


def e1_inputs():
    """E1：PDG 输入事实（只引用）。"""
    return {
        "row1": {"V_ud": V_UD, "s_ud": S_UD, "V_us": V_US, "s_us": S_US,
                 "V_ub": V_UB, "s_ub": S_UB},
        "row2": {"V_cd": V_CD, "s_cd": S_CD, "V_cs": V_CS, "s_cs": S_CS,
                 "V_cb": V_CB, "s_cb": S_CB},
    }


def _row_sum(v1, v2, v3):
    """一行平方和 Σ 与偏差 Δ=1−Σ。"""
    s = v1 * v1 + v2 * v2 + v3 * v3
    return s, Decimal(1) - s


def _row_sigma(v1, s1, v2, s2, v3, s3):
    """误差传播：σ(Δ)=sqrt((2V_1σ_1)²+(2V_2σ_2)²+(2V_3σ_3)²)（Σ 对各 V 偏导=2V）。"""
    a = (Decimal(2) * v1 * s1) ** 2
    b = (Decimal(2) * v2 * s2) ** 2
    c = (Decimal(2) * v3 * s3) ** 2
    return (a + b + c).sqrt(), a, b, c


def e2_row1():
    """E2：第一行幺正性核算（本册核心）。"""
    s1, d1 = _row_sum(V_UD, V_US, V_UB)
    sig1, a_ud, a_us, a_ub = _row_sigma(V_UD, S_UD, V_US, S_US, V_UB, S_UB)
    # Fraction 精确交叉核对 Σ₁
    fr = (Fraction(str(V_UD)) ** 2 + Fraction(str(V_US)) ** 2
          + Fraction(str(V_UB)) ** 2)
    s1_frac = Decimal(fr.numerator) / Decimal(fr.denominator)
    sig1_div = d1 / sig1  # 显著性（应 ≈0）
    return {
        "V_ud2": V_UD * V_UD, "V_us2": V_US * V_US, "V_ub2": V_UB * V_UB,
        "sum1": s1, "delta1": d1,
        "sig1": sig1, "a_ud": a_ud, "a_us": a_us, "a_ub": a_ub,
        "sum1_frac": s1_frac, "frac_check_diff": abs(s1 - s1_frac),
        "significance_delta_over_sig": sig1_div,
    }


def e3_row2():
    """E3：第二行对比核算。"""
    s2, d2 = _row_sum(V_CD, V_CS, V_CB)
    sig2, a_cd, a_cs, a_cb = _row_sigma(V_CD, S_CD, V_CS, S_CS, V_CB, S_CB)
    return {
        "V_cd2": V_CD * V_CD, "V_cs2": V_CS * V_CS, "V_cb2": V_CB * V_CB,
        "sum2": s2, "delta2": d2, "sig2": sig2,
        "a_cd": a_cd, "a_cs": a_cs, "a_cb": a_cb,
        "significance_delta2_over_sig2": d2 / sig2,
    }


def _arctan_decimal(x):
    """Decimal 域 arctan：Taylor 级数 arctan(x)=Σ(−1)^k x^(2k+1)/(2k+1)。"""
    assert Decimal("0") < x < Decimal("1"), x
    total = Decimal(0)
    term = x  # k=0: x
    k = 0
    x2 = x * x
    while abs(term) > Decimal(10) ** (-getcontext().prec - 2):
        if k % 2 == 0:
            total += term
        else:
            total -= term
        term *= x2 * Decimal(2 * k + 1) / Decimal(2 * k + 3)
        k += 1
    return total


def e4_cabibbo_orthogonality():
    """E4：Cabibbo 角 + 行正交性。"""
    tan_c = V_US / V_UD
    theta_rad = _arctan_decimal(tan_c)
    theta_deg = theta_rad * RAD2DEG
    # 行1·行2 正交性残差（实部，相位未知取主项）：
    #   V_ud V_cd − V_us V_cs + V_ub V_cb·(相) ≈ 0（Wolfenstein 下 −λ·1 + 1·λ = 0）
    ortho = V_UD * V_CD - V_US * V_CS + V_UB * V_CB
    return {
        "tan_c": tan_c, "theta_rad": theta_rad, "theta_deg": theta_deg,
        "row_orthogonality_residual": ortho,
    }


def e5_verdict():
    """E5：TUFT 供给判定。"""
    return {
        "tuft_ckm_supply": 0,          # TUFT 无 CKM 混合矩阵（承接 C0142 E4）
        "tuft_flavor_mixing_supply": 0,  # 无三代味结构（承接 C0221 味耦合线）
        "tuft_unitarity_supply": 0,     # 无幺正性约束/弱作用对称性供给
        "needs": "CKM 3×3 幺正矩阵结构（标准弱作用，3 角 + 1 CP 相）+ PDG 矩阵元实测",
        "verdict": "结构性负面（对 TUFT/几何框架）",
        "hits": "C5（可检验）+ C6（误差带）",
    }


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0242 · CKM 第一行幺正性 V_ud²+V_us²+V_ub² 偏差（母册 T288 · L 线域 H 批）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_inputs()
    w("\n[E1] PDG 输入事实（只引用不复算）")
    w("  第一行：|V_ud|=%s(%s)；|V_us|=%s(%s)；|V_ub|=%s(%s)"
      % (V_UD, S_UD, V_US, S_US, V_UB, S_UB))
    w("  第二行：|V_cd|=%s(%s)；|V_cs|=%s(%s)；|V_cb|=%s(%s)"
      % (V_CD, S_CD, V_CS, S_CS, V_CB, S_CB))
    w("  => 全部为 PDG 世界平均外部输入（第一行按任务指定值）；本册只做平方和/误差传播/角度算术。")
    entries.append(("E1", "PDG 第一行/第二行矩阵元及误差只引用；本册做平方和与误差传播算术",
                    "PASS", "外部输入显式计数"))

    # ---- E2 ----
    g2 = e2_row1()
    w("\n[E2] 第一行幺正性核算（本册核心）：Σ₁=V_ud²+V_us²+V_ub²")
    w("  V_ud² = %s；V_us² = %s；V_ub² = %s"
      % (fv(g2["V_ud2"], "10f"), fv(g2["V_us2"], "10f"), fv(g2["V_ub2"], "12e")))
    w("  Σ₁ = %s" % fv(g2["sum1"], "12f"))
    w("  Δ₁ = 1 − Σ₁ = %s（Fraction 精确交叉核对差 %s）"
      % (fv(g2["delta1"], "12e"), fv(g2["frac_check_diff"], "2e")))
    w("  误差传播：(2V_udσ_ud)²=%s；(2V_usσ_us)²=%s；(2V_ubσ_ub)²=%s"
      % (fv(g2["a_ud"], "4e"), fv(g2["a_us"], "4e"), fv(g2["a_ub"], "2e")))
    w("  σ(Δ₁) = sqrt(和) = %s" % fv(g2["sig1"], "6e"))
    w("  显著性 Δ₁/σ(Δ₁) = %s（应 ≈ 0：与幺正性一致）"
      % fv(g2["significance_delta_over_sig"], "6f"))
    w("  => 第一行平方和与 1 的偏差 ~1e-6 量级，远在误差带 ~4e-4 之内，")
    w("     第一行幺正性闭合（数值复核，非新物理）。")
    entries.append(("E2", "Σ₁=%s；Δ₁=%s；σ(Δ₁)=%s；Δ₁/σ=%s（与幺正性一致）"
                    % (fv(g2["sum1"], "8f"), fv(g2["delta1"], "4e"),
                       fv(g2["sig1"], "4e"), fv(g2["significance_delta_over_sig"], "3f")),
                    "PASS", "平方和 + 不确定度平方和传播，Decimal 48 位 + Fraction 核对"))

    # ---- E3 ----
    g3 = e3_row2()
    w("\n[E3] 对比核算：第二行 Σ₂=V_cd²+V_cs²+V_cb²")
    w("  V_cd² = %s；V_cs² = %s；V_cb² = %s"
      % (fv(g3["V_cd2"], "10f"), fv(g3["V_cs2"], "10f"), fv(g3["V_cb2"], "10f")))
    w("  Σ₂ = %s；Δ₂ = 1 − Σ₂ = %s" % (fv(g3["sum2"], "10f"), fv(g3["delta2"], "6e")))
    w("  σ(Δ₂) = %s；Δ₂/σ(Δ₂) = %s（误差带 ~1e-2，远粗于第一行）"
      % (fv(g3["sig2"], "6e"), fv(g3["significance_delta2_over_sig2"], "3f")))
    w("  => 第二行偏差 ~1e-3、误差带 ~1e-2，同样与幺正性一致但精度低一个量级")
    w("     （V_cs 大误差主导）；第一行精度显著优于第二行。")
    entries.append(("E3", "Σ₂=%s；Δ₂=%s；σ(Δ₂)=%s；Δ₂/σ=%s（一致性差但误差带更宽）"
                    % (fv(g3["sum2"], "6f"), fv(g3["delta2"], "3e"),
                       fv(g3["sig2"], "3e"), fv(g3["significance_delta2_over_sig2"], "2f")),
                    "PASS", "第一行 vs 第二行精度对比"))

    # ---- E4 ----
    g4 = e4_cabibbo_orthogonality()
    w("\n[E4] Cabibbo 角 θ_C 与 CKM 行正交性核算")
    w("  tan θ_C = V_us/V_ud = %s" % fv(g4["tan_c"], "10f"))
    w("  θ_C = arctan = %s rad = %s°" % (fv(g4["theta_rad"], "10f"), fv(g4["theta_deg"], "8f")))
    w("  行1·行2 正交残差 = V_udV_cd−V_usV_cs+V_ubV_cb = %s（≈0 即正交成立）"
      % fv(g4["row_orthogonality_residual"], "6f"))
    w("  => θ_C ≈ 13° 量级（与 C0142 E1 引用的 13.04° 一致）；行正交残差 ~1e-3，")
    w("     在误差带内（Wolfenstein −λ+λ=0 主相消）。")
    entries.append(("E4", "θ_C=%s°；行正交残差=%s（≈0，误差带内）"
                    % (fv(g4["theta_deg"], "4f"), fv(g4["row_orthogonality_residual"], "4f")),
                    "PASS", "Taylor arctan（Decimal）+ 行点积主相消核算"))

    # ---- E5 ----
    g5 = e5_verdict()
    w("\n[E5] 裁定：TUFT 供给检查")
    w("  TUFT CKM 矩阵供给 = %d；味混合/三代结构供给 = %d；幺正性/弱对称供给 = %d"
      % (g5["tuft_ckm_supply"], g5["tuft_flavor_mixing_supply"], g5["tuft_unitarity_supply"]))
    w("  CKM 幺正性依赖：%s" % g5["needs"])
    w("  => TUFT 已注销（C0133）；无 CKM 混合、无味结构、无幺正性约束供给，")
    w("     所有读数均为标准弱作用算术复核，**严禁写成 TUFT 预测/修正**。")
    w("  => **结构性负面（对 TUFT/几何框架）**；按母册 T288 登记撞 C5（可检验）/C6（误差带）。")
    entries.append(("E5", "TUFT 无 CKM 混合/无味结构/无幺正性供给 ⇒ 结构性负面；撞 C5/C6",
                    "PASS", "标准弱作用算术，非 TUFT 预测"))

    # ---- 守卫 ----
    guards = [
        ("G1", "第一行 Σ₁ 在 0.999–1.001（幺正性带）",
         Decimal("0.999") < g2["sum1"] < Decimal("1.001")),
        ("G2", "第一行中心偏差 |Δ₁| < 1e-3",
         abs(g2["delta1"]) < Decimal("1e-3")),
        ("G3", "σ(Δ₁) 在 3e-4–6e-4（误差带量级）",
         Decimal("3e-4") < g2["sig1"] < Decimal("6e-4")),
        ("G4", "|Δ₁|/σ(Δ₁) < 0.1（与幺正性一致）",
         abs(g2["significance_delta_over_sig"]) < Decimal("0.1")),
        ("G5", "θ_C 在 12.5°–13.5°（Cabibbo 角量级）",
         Decimal("12.5") < g4["theta_deg"] < Decimal("13.5")),
        ("G6", "第二行 Σ₂ 在 0.99–1.01",
         Decimal("0.99") < g3["sum2"] < Decimal("1.01")),
        ("G7", "行正交残差 |resid| < 0.05",
         abs(g4["row_orthogonality_residual"]) < Decimal("0.05")),
        ("G8", "Fraction 交叉核对 Σ₁ 差 ≈ 0",
         g2["frac_check_diff"] < Decimal("1e-30")),
        ("G9", "TUFT CKM 供给 = 0",
         g5["tuft_ckm_supply"] == 0),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0242 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释 CKM 幺正性或味混合；PDG 值只引用不复算；")
    w("  所有数值为标准弱作用算术复核，非 TUFT 预测；TUFT 已注销（C0133）。")
    w("  红线：不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("       有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0242_CKM幺正性攻破_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0242_CKM幺正性攻破_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0242_CKM_row1_unitarity",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_inputs": {k: str(v) for k, v in g1["row1"].items()}
            | {("row2_" + k): str(v) for k, v in g1["row2"].items()},
            "E2_row1": {k: str(v) for k, v in g2.items()},
            "E3_row2": {k: str(v) for k, v in g3.items()},
            "E4_cabibbo_orthogonality": {k: str(v) for k, v in g4.items()},
            "E5_verdict": {k: str(v) for k, v in g5.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0242 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
