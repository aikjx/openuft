# -*- coding: utf-8 -*-
"""
attack_C0140_耦合常数攻破_2026-10-20.py
独立复算：P13「耦合常数绝对值」· 布局 Phase 1 第一项

定位：布局册（C0135）Phase 1 第一项（阻塞力 3）。仓内此前对耦合常数的处理散落在
TUFT R11/R12（1-loop RGE 缺口）与开放项 O-COUPLING 中；本册把「耦合常数能不能被
第一性导出」这个问题压缩成三条可复核读数 + 一张输入账单：

  E1 三个规范耦合在 M_Z 的绝对值与跨度（外部值只引用不复算）。
  E2 **SM 单圈跑动不汇聚**（本册核心）：由三个耦合反解两两交点 ln-比，
     ΔL = 9.17 e-折 ⇒ 交点能标差 ~9.6e3 倍 ⇒ SM 内无统一点。
  E3 MSSM 对照：加一个超对称阈值 M_SUSY 后 ΔL < 1 ⇒ 汇聚，
     但代价 = 1 个新标度 + 整族超伴子（撞 C1/C2），且 M_GUT/α_GUT 仍无来源。
  E4 几何供给 0：量纲矩阵满秩 ⇒ (ℏ,G,c) 不能生成任何无量纲数；
     补一个质量只给 1 个无量纲组合 Gm²/(ℏc) ⇒ 耦合常数的**数值**仍需外部输入。
  E5 裁定：P13 结构性负面（对 TUFT/几何框架）。

纯标准库（Decimal 48 位 + Fraction 精确线性代数），零外部依赖，退出码 0。

诚实边界：本册不宣称已解释耦合常数；α_s / α_em / sin²θ_W / b 系数 / M_SUSY
均为外部引用或建模约定；质子衰变用唯象标度律（标 [C]）。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 外部输入（只引用不复算） ----------
M_Z = Decimal("91.1876")          # GeV
ALPHA_S_MZ = Decimal("0.1180")    # α_s(M_Z)
ALPHA_EM_INV_MZ = Decimal("127.95")   # α_em^{-1}(M_Z)（MS-bar）
SIN2W_MZ = Decimal("0.23121")     # sin²θ_W(M_Z)
M_SUSY = Decimal("1000")          # GeV（MSSM 阈值，建模约定）

# 单圈 β 系数（SM 与 MSSM，约定：dα_i^{-1}/d ln μ = -b_i/(2π)）
B_SM = (Fraction(41, 10), Fraction(-19, 6), Fraction(-7))
B_MSSM = (Fraction(33, 5), Fraction(1), Fraction(-3))

TWO_PI = Decimal("6.283185307179586476925286766559005768394")


def _ln(x):
    return Decimal(x).ln()


def _exp(x):
    return Decimal(x).exp()


def e1_couplings():
    """三个规范耦合在 M_Z 的绝对值（α_1 用 SU(5) 归一 5/3）。"""
    a_em = Decimal(1) / ALPHA_EM_INV_MZ
    a_y = a_em / (Decimal(1) - SIN2W_MZ)          # α_Y
    a1 = Decimal(5) / Decimal(3) * a_y            # GUT 归一
    a2 = a_em / SIN2W_MZ
    a3 = ALPHA_S_MZ
    vals = [a1, a2, a3]
    invs = [Decimal(1) / v for v in vals]
    spread = max(vals) / min(vals)
    return {"alpha_1": a1, "alpha_2": a2, "alpha_3": a3,
            "alpha_em": a_em, "alpha_Y": a_y,
            "inv": invs, "spread_max_over_min": spread,
            "sin2w": SIN2W_MZ, "m_z": M_Z}


def _dec(x):
    """Fraction / Decimal / int 统一转 Decimal。"""
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)


def _intersections(inv, b):
    """两两交点 ln-比 L_ij = 2π(α_i^{-1}-α_j^{-1})/(b_i-b_j)，及 ΔL。"""
    out = {}
    for (i, j, key) in ((0, 1, "L_12"), (1, 2, "L_23"), (0, 2, "L_13")):
        num = _dec(inv[i]) - _dec(inv[j])
        den = _dec(b[i]) - _dec(b[j])
        out[key] = TWO_PI * num / den
    ls = [out["L_12"], out["L_23"], out["L_13"]]
    out["L_max"] = max(ls)
    out["L_min"] = min(ls)
    out["delta_L"] = max(ls) - min(ls)
    out["L_bar"] = sum(ls) / Decimal(3)
    out["scale_ratio"] = _exp(out["delta_L"])
    return out


def e2_sm_running(g1):
    """SM 单圈：三交点是否汇聚。"""
    inv = g1["inv"]
    r = _intersections(inv, B_SM)
    return r


def e3_mssm_running(g1):
    """MSSM 对照：M_Z→M_SUSY 用 SM b，之上用 MSSM b。"""
    inv_susy = []
    lstep = _ln(M_SUSY / M_Z)
    for inv, b in zip(g1["inv"], B_SM):
        inv_susy.append(_dec(inv) - _dec(b) / TWO_PI * lstep)
    r = _intersections(inv_susy, B_MSSM)
    r["inv_at_msusy"] = inv_susy
    r["m_susy"] = M_SUSY
    # 统一点与统一耦合（用三交点均值 L_bar 处评估三个 α^{-1}）
    lbar = r["L_bar"]
    r["m_gut_GeV"] = M_SUSY * _exp(lbar)
    inv_gut = []
    for inv, b in zip(inv_susy, B_MSSM):
        inv_gut.append(_dec(inv) - _dec(b) / TWO_PI * lbar)
    r["inv_gut"] = inv_gut
    r["alpha_gut_inv_spread"] = max(inv_gut) - min(inv_gut)
    r["alpha_gut_inv"] = sum(inv_gut) / Decimal(3)
    # 质子衰变唯象标度律（[C]：τ_p ≈ (M_GUT/2e16)^4 × 1e35 yr）
    r["tau_p_yr"] = (r["m_gut_GeV"] / Decimal("2e16")) ** 4 * Decimal("1e35")
    r["tau_p_sk_limit_yr"] = Decimal("2.4e34")
    return r


def _rank(rows):
    """Fraction 高斯消元求秩（rows: list of list[Fraction]）。"""
    m = [row[:] for row in rows]
    ncol = len(m[0])
    rank = 0
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        rank += 1
        if r == len(m):
            break
    return rank


def e4_geometry_supply():
    """量纲线性代数：(ℏ,G,c) 能否生成无量纲数？补一个质量后呢？"""
    # 列顺序：[ℏ, G, c, m]，行顺序：[M, L, T]
    # ℏ=(1,2,-1)  G=(-1,3,-2)  c=(0,1,-1)  m=(1,0,0)
    cols3 = [[Fraction(1), Fraction(-1), Fraction(0)],
             [Fraction(2), Fraction(3), Fraction(1)],
             [Fraction(-1), Fraction(-2), Fraction(-1)]]
    rows3 = [[cols3[r][c] for c in range(3)] for r in range(3)]
    det3 = (rows3[0][0] * (rows3[1][1] * rows3[2][2] - rows3[1][2] * rows3[2][1])
            - rows3[0][1] * (rows3[1][0] * rows3[2][2] - rows3[1][2] * rows3[2][0])
            + rows3[0][2] * (rows3[1][0] * rows3[2][1] - rows3[1][1] * rows3[2][0]))
    rank3 = _rank(rows3)
    cols4 = [[Fraction(1), Fraction(-1), Fraction(0), Fraction(1)],
             [Fraction(2), Fraction(3), Fraction(1), Fraction(0)],
             [Fraction(-1), Fraction(-2), Fraction(-1), Fraction(0)]]
    rows4 = [cols4[r] for r in range(3)]
    rank4 = _rank(rows4)
    return {"det_3const": det3, "rank_3const": rank3,
            "nullity_3const": 3 - rank3, "rank_4const": rank4,
            "nullity_4const": 4 - rank4}


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    def fv(x, n="6e"):
        return format(Decimal(x), "." + n)

    w("=" * 74)
    w("attack_C0140 · 耦合常数绝对值（P13）攻破")
    w("=" * 74)

    entries = []

    # ---- E1 ----
    g1 = e1_couplings()
    w("\n[E1] 三个规范耦合在 M_Z（外部值只引用不复算；α_1 用 SU(5) 归一 5/3）")
    w("  α_em^{-1}(M_Z) = %s ⇒ α_em = %s；sin²θ_W = %s"
      % (ALPHA_EM_INV_MZ, fv(g1["alpha_em"]), g1["sin2w"]))
    w("  α_1 = %s（α_1^{-1} = %s）" % (fv(g1["alpha_1"]), fv(g1["inv"][0])))
    w("  α_2 = %s（α_2^{-1} = %s）" % (fv(g1["alpha_2"]), fv(g1["inv"][1])))
    w("  α_3 = %s（α_3^{-1} = %s）" % (fv(g1["alpha_3"]), fv(g1["inv"][2])))
    w("  跨度 max/min = %s（同一能标上三个耦合相差约 %s 倍）"
      % (fv(g1["spread_max_over_min"], "6f"), fv(g1["spread_max_over_min"], "2f")))
    entries.append(("E1", "三个耦合在 M_Z：α = %s / %s / %s，跨度 %s"
                    % (fv(g1["alpha_1"]), fv(g1["alpha_2"]), fv(g1["alpha_3"]),
                       fv(g1["spread_max_over_min"], "2f")), "PASS",
                    "外部值只引用；本册只做归一换算"))

    # ---- E2 ----
    g2 = e2_sm_running(g1)
    w("\n[E2] SM 单圈跑动（本册核心）：dα_i^{-1}/d lnμ = -b_i/(2π)，b=%s"
      % str(tuple(str(b) for b in B_SM)))
    w("  两两交点 ln-比：L_12 = %s；L_23 = %s；L_13 = %s"
      % (fv(g2["L_12"], "6f"), fv(g2["L_23"], "6f"), fv(g2["L_13"], "6f")))
    w("  ΔL = %s e-折 ⇒ 交点能标相差 %s 倍"
      % (fv(g2["delta_L"], "6f"), fv(g2["scale_ratio"])))
    w("  => SM 单圈**不汇聚**：不存在同时满足三个耦合相交的统一能标。")
    entries.append(("E2", "SM 单圈不汇聚：ΔL = %s e-折 ⇒ 交点能标差 %s 倍"
                    % (fv(g2["delta_L"], "4f"), fv(g2["scale_ratio"])), "PASS",
                    "b_SM=(41/10,-19/6,-7)；三交点 ln-比机器反解"))

    # ---- E3 ----
    g3 = e3_mssm_running(g1)
    w("\n[E3] MSSM 对照（M_SUSY = %s GeV，建模约定）" % g3["m_susy"])
    w("  M_Z→M_SUSY 用 SM b，之上用 MSSM b = %s"
      % str(tuple(str(b) for b in B_MSSM)))
    w("  L_12 = %s；L_23 = %s；L_13 = %s ⇒ ΔL = %s"
      % (fv(g3["L_12"], "6f"), fv(g3["L_23"], "6f"), fv(g3["L_13"], "6f"),
         fv(g3["delta_L"], "6f")))
    w("  M_GUT ≈ %s GeV；α_GUT^{-1} ≈ %s（三分量散布 %s）"
      % (fv(g3["m_gut_GeV"]), fv(g3["alpha_gut_inv"], "6f"),
         fv(g3["alpha_gut_inv_spread"])))
    w("  质子衰变唯象标度律（[C]）：τ_p ≈ %s yr vs Super-K 下限 %s yr"
      % (fv(g3["tau_p_yr"]), fv(g3["tau_p_sk_limit_yr"])))
    w("  => 汇聚了，但代价清单：①新标度 M_SUSY（撞 C2）②整族超伴子谱（撞 C1）")
    w("     ③α_GUT ≈ 1/%s 与 M_GUT 本身**仍无第一性来源**（撞 C2/C3）。"
      % fv(g3["alpha_gut_inv"], "4f"))
    entries.append(("E3", "MSSM 汇聚（ΔL = %s）但代价 = 1 新标度 + 整族超伴子；"
                    "α_GUT^{-1} ≈ %s 仍无来源"
                    % (fv(g3["delta_L"], "4f"), fv(g3["alpha_gut_inv"], "2f")), "PASS",
                    "M_SUSY=1 TeV 建模约定；τ_p 标度律标 [C]"))

    # ---- E4 ----
    g4 = e4_geometry_supply()
    w("\n[E4] 几何供给：量纲线性代数")
    w("  (ℏ,G,c) 三常数量纲矩阵 det = %s ⇒ rank = %d ⇒ nullity = %d"
      % (g4["det_3const"], g4["rank_3const"], g4["nullity_3const"]))
    w("  ⇒ 三个常数**不能**生成任何无量纲组合 ⇒ 耦合常数（纯数）无从得到。")
    w("  补一个质量后：rank = %d，nullity = %d ⇒ 唯一无量纲组合是 Gm²/(ℏc) = (m/m_P)²"
      % (g4["rank_4const"], g4["nullity_4const"]))
    w("  ⇒ 即便如此，仍需**外部质量标度**；耦合常数的**数值**仍由该标度决定（撞 C2/C3）。")
    entries.append(("E4", "几何供给 0：(ℏ,G,c) nullity = 0（det=%s）；"
                    "补质量后 nullity = 1 但仍需外部标度"
                    % g4["det_3const"], "PASS", "Fraction 精确高斯消元，承接 C0134"))

    # ---- E5 ----
    w("\n[E5] 裁定")
    w("  耦合常数问题被精确翻译成两件事：(a) 三个**纯数**从哪来；(b) 它们是否汇聚。")
    w("  (a) 量纲代数已证：(ℏ,G,c) 满秩 ⇒ 纯数不可由几何常数生成 ⇒ 撞 C2/C3；")
    w("  (b) SM 单圈不汇聚（E2）；唯一已知汇聚方案（MSSM）需 ≥1 个新标度 + 整族新粒子（E3）。")
    w("  => **P13 结构性负面（对 TUFT/几何框架）**。")
    entries.append(("E5", "P13 结构性负面：耦合常数的数值与汇聚均需外部输入，几何供给 0",
                    "PASS", "撞 C1（粒子内容）/C2（绝对标度）/C3（零自由参数）"))

    # ---- 守卫 ----
    guards = [
        ("G1", "SM 单圈 ΔL > 1（不汇聚）", g2["delta_L"] > Decimal("1")),
        ("G2", "MSSM ΔL < 1（汇聚，代价另计）", g3["delta_L"] < Decimal("1")),
        ("G3", "(ℏ,G,c) 量纲矩阵满秩（nullity = 0）", g4["nullity_3const"] == 0),
        ("G4", "补一个质量后 nullity 恰为 1", g4["nullity_4const"] == 1),
        ("G5", "M_GUT 落在 1e15–1e17 GeV（与已知 MSSM 量级一致）",
         Decimal("1e15") < g3["m_gut_GeV"] < Decimal("1e17")),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0140 guard failed"

    w("\n[诚实边界]")
    w("  本册不宣称已解释耦合常数：α_s/α_em/sin²θ_W 与 b 系数只引用，M_SUSY 为建模约定，")
    w("  τ_p 用唯象标度律（[C]）。裁的是「几何/TUFT 框架能否导出耦合常数」。")

    w("\n条目 %d（PASS %d）；守卫 %d/%d；退出码 0。"
      % (len(entries), len(entries), sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    report_path = os.path.join(BASE, "attack_C0140_耦合常数攻破_2026-10-20_report.txt")
    json_path = os.path.join(BASE, "attack_C0140_耦合常数攻破_2026-10-20.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": "C0140_coupling_constants",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]}
                        for e in entries],
            "E1_couplings": {k: (str(v) if isinstance(v, Decimal) else
                                 [str(x) for x in v])
                             for k, v in g1.items()},
            "E2_sm_running": {k: str(v) for k, v in g2.items()},
            "E3_mssm_running": {k: (str(v) if not isinstance(v, list) else [str(x) for x in v])
                                for k, v in g3.items()},
            "E4_geometry_supply": {k: (str(v) if not isinstance(v, Fraction) else str(v))
                                   for k, v in g4.items()},
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0140 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
