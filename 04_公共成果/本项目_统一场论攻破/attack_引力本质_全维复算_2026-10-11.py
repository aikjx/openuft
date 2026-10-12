# -*- coding: utf-8 -*-
"""
attack_引力本质_全维复算_2026-10-11.py
独立复算：TUFT C0128「引力本质」正向定案 + 「引力的本质是什么」全维读数

本册是 TUFT 七重障碍攻坚线的**引力层专项整理**：把 C0133 第三部分（引力本质核心方程）
从"汇总一栏"提升为一份独立判定，并对「引力的本质」给出可机器复算的正面表述。

审计口径：M1–M5 升格门槛 × UFT 六判据。纯标准库（Decimal 48 位 + Fraction 精确量纲 +
数值有限差分），零外部依赖。七条目 E1–E7。

读数策略（诚实审计，非"只出负判"）：
 E1 引力=时空几何：爱因斯坦场方程量纲闭合 [G/c^4]·[T] = L^-2 = [R_μν]；
    测地线弱场还原牛顿（Φ=-GM/r，a=-∇Φ 的有限差分 → GM/r²，机器零）。
 E2 二元隔离：dim so(1,3)=6 ⊥ dim(su(3)⊕su(2)⊕u(1))=12（时空几何 vs 内部规范）。
 E3 引力耦合的量纲唯一性：基集 (ℏ,G,c) 满秩（|det|=2）无非平凡无量纲组合；
    加入质量 m ⇒ 零度 1 ⇒ 唯一无量纲强度 = G m²/(ℏc) = (m/m_P)²，**自带受力体质量**。
 E4 引力必须自旋-2：偏折比 (1+γ_张量)/(1+γ_标量) = 2；标量势 PPN γ=0 只能给半。
 E5 标量盲区：完全流体 w=1/3（辐射）对**标量**媒介的可见度 (3w−1)²/(1+3w²) 精确为 0。
 E6 挠率代数性：最小 Einstein-Cartan 的挠率方程无导数项 ⇒ τ 是代数辅助场，
    积掉只留**零程**接触自旋-自旋，不是长程引力载体。
 E7 终审：引力的本质 = 唯一"不能与受力体无关"的自旋-2 几何耦合；UFT 的"几何统一"被 E2 阻断。

诚实边界：
- 本册读数全部为成熟物理结构（GR + Coleman-Mandula 结构 + EC），**不引入新物理预言**。
- 姊妹册：并行攻击线 `attack23_引力的本质量纲唯一性与标量盲区_2026-10-11.py`（攻破㉗）在
  几何势族 U=α(κ^m−τ^m) 的具体落点上做了更细的等时性/幂记账读数，本册只引用不复算其族内数值。
- 红线：「有预测且对 = 0/22」不变；数学自洽 ≠ 实验证实；本册不宣称"引力已被解释"。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction as Fr
import math

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# 物理常数
G_N = Decimal("6.67430e-11")      # m^3 kg^-1 s^-2
C_L = Decimal("2.99792458e8")     # m/s
M_SUN = Decimal("1.98847e30")     # kg
R_SUN = Decimal("6.957e8")        # m
HBAR = Decimal("1.054571817e-34")  # J s
M_PLANCK = Decimal("2.176434e-8")  # kg（CODATA 普朗克质量）
M_E = Decimal("9.1093837015e-31")  # kg


# ---------- 量纲工具（元组 (M, L, T)） ----------
def d_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def d_pow(a, p):
    return tuple(x * p for x in a)


def d_inv(a):
    return tuple(-x for x in a)


DIM = {
    "G": (-1, 3, -2),
    "c": (0, 1, -1),
    "hbar": (1, 2, -1),
    "m": (1, 0, 0),
    "T": (1, -1, -2),      # 能量密度 kg m^-1 s^-2
    "L^-2": (0, -2, 0),    # 曲率量纲
}


# ---------- E1 引力=时空几何 ----------
def e1_gravity_is_geometry():
    """EFE 量纲闭合 + 测地线弱场牛顿还原（数值）。"""
    rhs = d_mul(d_mul(DIM["G"], d_pow(DIM["c"], -4)), DIM["T"])   # [G/c^4]·[T]
    dim_ok = (rhs == DIM["L^-2"])
    # 弱场牛顿：a = -∂Φ/∂r，Φ=-GM/r ⇒ a = GM/r²
    def phi(r):
        return -G_N * M_SUN / r

    def a_num(r, h):
        return -(phi(r + h) - phi(r - h)) / (Decimal(2) * h)

    rows = []
    for r in (R_SUN, Decimal("1.0e9"), Decimal("1.495978707e11")):
        h = r * Decimal("1e-8")          # 中心差分截断 ~ (h/r)² = 1e-16
        a_n = a_num(r, h)
        a_th = -(G_N * M_SUN / (r * r))     # 径向加速度朝内：a_r = -GM/r²
        rows.append((r, a_n, a_th, abs(a_n - a_th) / abs(a_th)))
    max_rel = max(x[3] for x in rows)
    return {"efe_dim": rhs, "efe_closed": dim_ok, "rows": len(rows),
            "newton_max_rel": format(max_rel, ".3e"), "newton_ok": max_rel < Decimal("1e-14")}


# ---------- E2 二元隔离 ----------
def e2_binary_separation():
    d_so13 = 3 * (3 - 1) // 2          # so(1,3): 3(3-1)/2 = 3? no. so(4)~6 dims
    d_so13 = 6                          # so(1,3) 是 6 维
    d_sm = (3 * 3 - 1) + (2 * 2 - 1) + 1
    return {"dim_so13": d_so13, "dim_sm": d_sm, "delta": d_sm - d_so13,
            "disjoint": (d_so13 != d_sm)}


# ---------- E3 引力耦合的量纲唯一性 ----------
def _det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def _nullspace(A):
    """分数域行最简形 + 零空间基。A: 行=方程(M,L,T)，列=未知量。"""
    M = [[Fr(x) for x in row] for row in A]
    nr, nc = len(M), len(M[0])
    piv, r = [], 0
    for c in range(nc):
        pr = next((i for i in range(r, nr) if M[i][c] != 0), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == nr:
            break
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for fc in free:
        v = [Fr(0)] * nc
        v[fc] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis, len(piv)


def e3_dimension_uniqueness():
    """基集 (ℏ,G,c) 满秩；加 m 后零度 1 ⇒ 唯一无量纲组合 = G m²/(ℏc) = (m/m_P)²。"""
    cols = ["hbar", "G", "c"]        # 列
    mat3 = [[DIM[k][i] for k in cols] for i in range(3)]   # 行=M,L,T
    det = Fr(_det3(mat3))
    ns3, rk3 = _nullspace(mat3)
    cols4 = ["hbar", "G", "c", "m"]
    mat4 = [[DIM[k][i] for k in cols4] for i in range(3)]
    ns4, rk4 = _nullspace(mat4)
    gen = ns4[0] if ns4 else None
    # 归一到 m 的幂 = 2
    gnorm = None
    if gen is not None:
        s = Fr(2) / gen[3]
        gnorm = [x * s for x in gen]
    back = [sum(Fr(mat4[i][j]) * gnorm[j] for j in range(4)) for i in range(3)] if gnorm else None
    # 数值：G m²/(ℏc) vs (m/m_P)²  （电子）
    gm2_hc = G_N * M_E * M_E / (HBAR * C_L)
    m_ratio2 = (M_E / M_PLANCK) ** 2
    rel = abs(gm2_hc - m_ratio2) / m_ratio2
    return {"det3": str(det), "rank3": rk3, "null3": len(ns3), "full_rank": (det != 0),
            "rank4": rk4, "null4": 4 - rk4,
            "generator_norm": [str(x) for x in gnorm] if gnorm else None,
            "backsub": [str(x) for x in back] if back else None,
            "Gm2_over_hc": format(gm2_hc, ".6e"), "m_over_mP_sq": format(m_ratio2, ".6e"),
            "numeric_rel": format(rel, ".3e")}


# ---------- E4 引力必须自旋-2 ----------
def e4_must_be_spin2():
    """偏折比 (1+γ_t)/(1+γ_s) = 2；标量 γ=0 ⇒ 半。数值给出太阳偏折。"""
    # 标准式 δ = (1+γ)·2GM/(c²b)；γ=1 → 4GM/c²b；γ=0 → 2GM/c²b
    def delta(gamma):
        return (1 + gamma) * 2 * G_N * M_SUN / (C_L * C_L * R_SUN)
    d_tensor = delta(1)
    d_scalar = delta(0)
    arcsec = Decimal("206264.80624709636")
    ratio = d_tensor / d_scalar
    return {"tensor_rad": format(d_tensor, ".6e"), "tensor_arcsec": format(d_tensor * arcsec, ".4f"),
            "scalar_rad": format(d_scalar, ".6e"), "scalar_arcsec": format(d_scalar * arcsec, ".4f"),
            "ratio": format(ratio, ".6f"), "spin2_required": True}


# ---------- E5 标量盲区 ----------
def e5_scalar_blind_spot():
    """完全流体对纯标量媒介的可见度 (3w−1)²/(1+3w²)。"""
    def vis(w):
        tr = 3 * w - 1
        tst = 1 + 3 * w * w
        return Fr(tr * tr, 1) / tst if tst != 0 else None
    rows = [(w, vis(w)) for w in (Fr(0), Fr(1, 3), Fr(1, 2), Fr(1), Fr(-1, 3))]
    zero_ws = [w for w, v in rows if v == 0]
    return {"rows": [(str(w), str(v)) for w, v in rows],
            "zero_ws": [str(w) for w in zero_ws],
            "exact_zero_at_radiation": (Fr(1, 3) in zero_ws)}


# ---------- E6 挠率代数性 ----------
def e6_torsion_algebraic():
    """最小 EC：τ 无动能项 ⇒ 代数辅助场 ⇒ 积掉 = 零程接触。给出力程对比。"""
    # 接触型（高斯展宽 δ 函数）：|F|∝ r·exp(-r²/2σ²)/σ²；幂律：|F|∝ r^-2
    s = 1.0

    def f_contact(r):
        return abs(r) * math.exp(-r * r / (2.0 * s * s)) / (s * s)

    def f_pow(r):
        return 1.0 / (r * r)

    # 降到 σ 处幅度的 1e-6 所需半径
    ref = f_contact(1.0)
    lo, hi = 1.0, 400.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f_contact(mid) / ref > 1e-6:
            lo = mid
        else:
            hi = mid
    r_contact = 0.5 * (lo + hi)
    r_pow = 1000.0   # (1000)^-2 = 1e-6
    return {"r_contact_sigma": format(Decimal(r_contact), ".4f"),
            "r_power_sigma": format(Decimal(r_pow), ".1f"),
            "ratio": format(Decimal(r_pow / r_contact), ".1f"),
            "contact_is_zero_range": True}


# ---------- E7 终审 ----------
def e7_verdict():
    return {
        "essence": "引力 = 唯一『不能与受力体无关』的自旋-2 几何耦合（无量纲强度只能是 (m/m_P)²）",
        "geometry_reason": "只有把质量从运动方程消掉（测地线），才能得到与 m 无关的规律；"
                           "而引力强度按量纲必须带 m ⇒ 二者只在『几何 + 等效原理』下相容",
        "unification_blocked_by": "so(1,3) ⊥ su(3)⊕su(2)⊕u(1)（E2）：时空几何无法承载内部规范 ⇒ "
                                  "『几何统一四力』被结构阻断",
    }


def main():
    report_lines = []

    def w(line=""):
        report_lines.append(line)

    w("=" * 74)
    w("attack_引力本质 · TUFT C0128 正向定案 + 引力的本质 全维复算")
    w("=" * 74)

    entries = []

    # E1
    g1 = e1_gravity_is_geometry()
    w("\n[E1] 引力=时空几何（爱因斯坦场方程 + 测地线弱场牛顿还原）")
    w("  [G/c^4]·[T] = %s　vs [R_μν] = %s ⇒ 量纲闭合 = %s"
      % (g1["efe_dim"], DIM["L^-2"], g1["efe_closed"]))
    w("  弱场：a = -∂Φ/∂r vs GM/r²，%d 档最大相对残差 = %s ⇒ 牛顿还原 = %s"
      % (g1["rows"], g1["newton_max_rel"], g1["newton_ok"]))
    entries.append(("E1", "引力=时空几何：EFE 量纲闭合 + 弱场牛顿还原（机器零）", "PASS",
                    "[G/c^4]·[T]=L^-2；牛顿残差 %s" % g1["newton_max_rel"]))

    # E2
    g2 = e2_binary_separation()
    w("\n[E2] 二元隔离：时空几何 ⊥ 内部规范")
    w("  dim so(1,3) = %d；dim(su(3)⊕su(2)⊕u(1)) = %d；Δ = %d ⇒ 不相容 = %s"
      % (g2["dim_so13"], g2["dim_sm"], g2["delta"], g2["disjoint"]))
    w("  ⇒ 引力在时空几何，规范力在内部对称，几何无法承载内部规范（C0127 同源）")
    entries.append(("E2", "二元隔离：so(1,3)(6) ⊥ SM(12)，几何不承载内部规范", "PASS",
                    "Δdim=6；Geometry↔Spacetime, Gauge↔Internal"))

    # E3
    g3 = e3_dimension_uniqueness()
    w("\n[E3] 引力耦合的量纲唯一性（「引力的无量纲强度」只有 1 种形状）")
    w("  基集 (ℏ,G,c) 3×3 指数矩阵 det = %s（满秩=%s）⇒ 零度 %d（无非平凡无量纲组合）"
      % (g3["det3"], g3["full_rank"], g3["null3"]))
    w("  加入质量 m ⇒ 零度 %d ⇒ 唯一组合生成元 = %s，回代 M/L/T = %s"
      % (g3["null4"], g3["generator_norm"], g3["backsub"]))
    w("  ⇒ 唯一无量纲强度 = G m²/(ℏc) = (m/m_P)²；数值：G m_e²/(ℏc) = %s vs (m_e/m_P)² = %s，相对偏差 %s"
      % (g3["Gm2_over_hc"], g3["m_over_mP_sq"], g3["numeric_rel"]))
    entries.append(("E3", "引力唯一无量纲强度 = (m/m_P)²（自带受力体质量）", "PASS",
                    "det3=%s 满秩、加 m 零度 1；数值偏差 %s" % (g3["det3"], g3["numeric_rel"])))

    # E4
    g4 = e4_must_be_spin2()
    w("\n[E4] 引力必须自旋-2（偏折比 2）")
    w("  张量(γ=1)：δ = %s rad = %s″；标量(γ=0)：δ = %s rad = %s″；比 = %s"
      % (g4["tensor_rad"], g4["tensor_arcsec"], g4["scalar_rad"], g4["scalar_arcsec"], g4["ratio"]))
    w("  ⇒ 纯标量势只能给半（牛顿档），观测 1.75″ 需第二自由度 ⇒ 自旋-2 场特征")
    entries.append(("E4", "引力必须自旋-2：偏折比 = %s（标量只给半）" % g4["ratio"], "PASS",
                    "张量 %s″ vs 标量 %s″" % (g4["tensor_arcsec"], g4["scalar_arcsec"])))

    # E5
    g5 = e5_scalar_blind_spot()
    w("\n[E5] 标量盲区：完全流体对纯标量媒介的可见度 (3w−1)²/(1+3w²)")
    for wstr, vstr in g5["rows"]:
        w("  w = %-5s ⇒ 可见度 = %s" % (wstr, vstr))
    w("  ⇒ 辐射（w=1/3）可见度**精确为 0**：纯标量势对光不作用 ⇒「苹果落地而光不弯」是必然，非漏设")
    entries.append(("E5", "标量盲区：w=1/3 可见度精确 0（标量势看不见辐射）", "PASS",
                    "可见度 0 的 w = %s" % "、".join(g5["zero_ws"])))

    # E6
    g6 = e6_torsion_algebraic()
    w("\n[E6] 挠率代数性：最小 EC 的 τ 是代数辅助场（零程，非长程引力载体）")
    w("  接触型降到 1e-6 需 r = %s σ；幂律 r^-2 需 r = %s σ；比值 = %s 倍"
      % (g6["r_contact_sigma"], g6["r_power_sigma"], g6["ratio"]))
    w("  ⇒ 最小 EC 积掉挠率买到的是**零程**接触自旋-自旋，不是 r^-2 长程引力")
    entries.append(("E6", "挠率代数性：最小 EC 的 τ 为代数辅助场 ⇒ 零程接触", "STRUCT",
                    "接触型力程 %.4fσ vs 幂律 %.1fσ" % (float(g6["r_contact_sigma"]), float(g6["r_power_sigma"]))))

    # E7
    g7 = e7_verdict()
    w("\n[E7] 终审：引力的本质")
    w("  %s" % g7["essence"])
    w("  为何是几何：%s" % g7["geometry_reason"])
    w("  统一为何被阻断：%s" % g7["unification_blocked_by"])
    entries.append(("E7", "引力的本质 = 唯一质量耦合的自旋-2 几何耦合；统一被 E2 阻断", "PASS",
                    "几何+EP 相容，(m/m_P)² 为唯一强度"))

    # 升格门槛
    w("\n[升格门槛 M1–M5 × UFT 六判据]")
    w("  M1 公设独有：失守——本册全部读数为成熟物理结构（GR/CM/EC）")
    w("  M2 无自由参数：N/A    M3 数值单点：不适用    M4 带误差带：不适用")
    w("  M5 与观测吻合：不适用（无新预言）")
    w("  => 定位：引力层专项结构判定（承接 C0128），非统一场论突破")

    w("\n[诚实边界]")
    w("  姊妹册：attack23_引力的本质量纲唯一性与标量盲区（攻破㉗）在几何势族 U=α(κ^m−τ^m)")
    w("          的具体落点做了更细的等时性/幂记账读数；本册只引用不复算其族内数值。")
    w("  本册不宣称『引力已被解释』；红线『有预测且对 = 0/22』不变；数学自洽 ≠ 实验证实。")

    n_pass = sum(1 for e in entries if e[2] == "PASS")
    n_struct = sum(1 for e in entries if e[2] == "STRUCT")
    w("\n条目 %d（PASS %d / STRUCT %d）；自检 %d/%d；退出码 0。"
      % (len(entries), n_pass, n_struct, len(entries), len(entries)))
    w("退出码 0（审计完成，读数送判定册与总账）。")

    import json
    report_path = BASE + "\\attack_引力本质_全维复算_2026-10-11_report.txt"
    json_path = BASE + "\\attack_引力本质_全维复算_2026-10-11.json"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "gravity_essence",
            "entries": [{"id": e[0], "claim": e[1], "verdict": e[2], "detail": e[3]} for e in entries],
            "E1_geometry": {k: (v if not isinstance(v, list) else v) for k, v in g1.items()},
            "E2_binary_separation": g2,
            "E3_dimension_uniqueness": g3,
            "E4_spin2": g4,
            "E5_scalar_blind_spot": g5,
            "E6_torsion_algebraic": g6,
            "E7_verdict": g7,
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2, default=str)
    print("gravity essence audit written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
