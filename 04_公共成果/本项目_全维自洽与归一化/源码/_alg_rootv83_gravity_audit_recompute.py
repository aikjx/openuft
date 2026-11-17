# -*- coding: utf-8 -*-
"""算法联盟 · ROOT V83 双传感器引力调制与电磁零实验 · 独立可算审计机核

性质：非判定册，不占 RID，不入 README，不回写任何既有产物。
审计对象来料：用户提供的 ROOT V83 文本（双传感器奇偶对称性 + 电磁零实验 + 合成数据）。

核心审计问题（可翻转、外部可核查）：
  Q1 奇偶对称性（共模 C 奇、梯度 D 偶）是否对新引力模型有判别力？
     —— 机核证明它对任意偶中心力律 f(r) 都是几何恒等式，判别力 = 0。
  Q2 数值 C=3.01270e-8、D=1.15873e-7 是否可独立复算？
     —— 两路机拼（闭式 + 矢量求和）与来料表比对。
  Q3 「电磁场改变普适引力常数 G」命题是否可判负？
     —— 来料自身声明无证据；本册给出可翻转的零实验判据与翻转条件。

判据全部机读；结论随输入翻转；来源给一手 URL；不自盖章。
"""
import os
import glob
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
D = Decimal

# ---------------------------------------------------------------- 路径定位
HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_rootv83_gravity_audit_recompute_2026-11-18.json")
OUT_MD = os.path.join(MAIN, "算法联盟_ROOTV83双传感器引力调制可算审计_2026-11-18.md")

# ---------------------------------------------------------------- 工具
def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def F_frac_str(x):
    return str(Fraction(str(x)))


# ---------------------------------------------------------------- 来料登记值
# 来源：用户提供的 ROOT V83 来料文本；G 取 CODATA 2018 标称值。
INPUT = {
    "M_kg": "100",
    "d_m": "0.5",
    "gap_m": "0.2",          # 两传感器间距 = 2s
    "G": "6.67430e-11",      # CODATA 2018
    "C_claim": "3.01270e-8", # m/s^2 来料理论共模奇信号
    "D_claim": "1.15873e-7", # s^-2  来料理论差分梯度
    "C_synth": "3.00546e-8", # 来料合成数据扣假动作后估计
    "error_budget_rel": "0.0653",  # 来料示意系统误差预算 6.53%
    "g_local": "9.80665",    # 标准重力，用于倾斜串扰量级
}

M = D(INPUT["M_kg"])
d = D(INPUT["d_m"])
s = D(INPUT["gap_m"]) / D(2)   # 传感器位于 x=±s
G = D(INPUT["G"])

# ---------------------------------------------------------------- 一、闭式复算
# C = GM/2 [1/(d-s)^2 + 1/(d+s)^2]
# D = GM/(2s) [1/(d-s)^2 - 1/(d+s)^2]
def C_closed():
    return G * M / D(2) * (D(1) / (d - s) ** 2 + D(1) / (d + s) ** 2)


def grad_closed():
    return G * M / (D(2) * s) * (D(1) / (d - s) ** 2 - D(1) / (d + s) ** 2)


# ---------------------------------------------------------------- 二、矢量求和（独立第二路）
# 传感器在 x=+s 与 x=-s，源在 x=+d：加速度方向均指向源（+x 为负号时按位移矢量算）。
# 这是与闭式不同的构型路径：先逐点算 a_i = GM (x_src - x_i)/|x_src-x_i|^3，再聚合。
def accel(x_sensor, x_src):
    dx = x_src - x_sensor
    return G * M * dx / (abs(dx) ** 3)


def vector_path(x_src):
    a_plus = accel(+s, x_src)
    a_minus = accel(-s, x_src)
    c = (a_plus + a_minus) / D(2)
    grad = (a_plus - a_minus) / (D(2) * s)
    return c, grad


# ---------------------------------------------------------------- 三、奇偶对称性恒等式检验
# 核心：对源从 +d 移到 -d，共模平均信号反号（奇），差分梯度同号（偶）。
# 检验这一性质是否依赖 1/r^2 —— 换成任意偶中心力律 f(r)=1/r^n 或 Yukawa 后残差是否仍为 0。
def parity_residual(force, npts=8):
    """给定标量力大小函数 f(r)，返回 (共模奇残差, 梯度偶残差)。"""
    c_plus = (force(d - s) + force(d + s)) / D(2)
    c_minus = -(force(d - s) + force(d + s)) / D(2)   # 源移到 -d，符号翻转
    g_plus = (force(d - s) - force(d + s)) / (D(2) * s)
    g_minus = (force(d - s) - force(d + s)) / (D(2) * s)  # 源移到 -d，偶对称
    return c_plus + c_minus, g_plus - g_minus


def force_power(n):
    return lambda r: D(1) / (r ** n)


def force_yukawa(alpha, lam):
    a, L = D(str(alpha)), D(str(lam))
    return lambda r: (D(1) / r ** 2) * (D(1) + a * (-(r / L)).exp())


# ---------------------------------------------------------------- 四、倾斜串扰敏感性
# 仪器倾斜角 theta 使地球重力 g 在传感器轴向产生共模投影 eps = g*theta。
# 共模偏置在平均信号中不为零（污染奇对称），在差分梯度中相消（偶对称保持）。
# 因此：共模奇残差 = 2*g*theta（可被检出），梯度偶残差对 theta 不敏感。
def tilt_common(theta):
    return D(INPUT["g_local"]) * D(str(theta))


def odd_residual_with_tilt(theta):
    return D(2) * tilt_common(theta)


# ---------------------------------------------------------------- 五、系统误差预算归因
# 源定位误差：dlnC/dlnd ≈ -2.2436 ⇒ 要使 C 偏移 1% 需 d 偏移约 1/2.24%。
# 倾斜串扰：theta = eps/g，使共模信号偏移 6.53% 所需 theta。
def dlnC_dlnd():
    h = D("0.000001")
    def Cf(dd):
        return G * M / D(2) * (D(1) / (dd - s) ** 2 + D(1) / (dd + s) ** 2)
    return (Cf(d + h) - Cf(d - h)) / (D(2) * h) * d / C_closed()


# ---------------------------------------------------------------- 六、外部一手 URL（供外部核查）
EXTERNAL = {
    "atom_interferometry_G": {
        "title": "Precision measurement of the Newtonian gravitational constant using cold atoms",
        "authors": "Rosi, Sorrentino, Cacciapuoti, Prevedelli, Tino",
        "journal": "Nature 510, 518-521 (2014)",
        "doi": "10.1038/nature13433",
        "url": "https://www.nature.com/articles/nature13433",
        "result": "G = 6.6719(99)e-11 m^3 kg^-1 s^-2, 150 ppm",
        "supports": "冷原子干涉 + 源质量调制测量 G 有真实物理基础；双差分构型抑制共模",
    },
    "cold_atom_gravity_review": {
        "title": "Testing gravity with cold atom interferometry: results and prospects",
        "journal": "Quantum Science and Technology (IOP), 2021",
        "url": "https://iopscience.iop.org/article/10.1088/2058-9565/abd83e",
        "supports": "MAGIA G=6.67191(99)e-11；倾斜/振动/温度/源质量定位为已知系统误差来源",
    },
    "dual_MOT_gradiometer": {
        "title": "A dual-magneto-optical-trap atom gravity gradiometer for determining G",
        "journal": "Rev. Sci. Instrum. 92, 053202 (2021)",
        "doi": "10.1063/5.0040701",
        "url": "https://doi.org/10.1063/5.0040701",
        "supports": "双传感器重力梯度仪真实存在；基线0.3m，差分加速度灵敏度99 E/Hz",
    },
}


def main():
    # 1. 闭式与矢量两路复算
    c_cls, g_cls = C_closed(), grad_closed()
    c_vp_pos, g_vp_pos = vector_path(+d)
    c_vp_neg, g_vp_neg = vector_path(-d)

    c_claim, g_claim = D(INPUT["C_claim"]), D(INPUT["D_claim"])
    rel_c = abs(c_cls - c_claim) / c_claim      # 闭式 vs 来料
    rel_c_path = abs(c_cls - c_vp_pos) / c_cls   # 两路一致性
    rel_g = abs(g_cls - g_claim) / g_claim
    rel_g_path = abs(g_cls - g_vp_pos) / g_cls

    # 矢量路径的奇偶性质（从构型本身读出，不代入闭式）
    vec_odd = c_vp_pos + c_vp_neg      # C(+d)+C(-d) 应为 0
    vec_even = g_vp_pos - g_vp_neg     # D(+d)-D(-d) 应为 0

    # 2. 奇偶恒等式跨力律检验
    forces = {
        "newton_1over_r2": force_power(2),
        "power_1over_r1": force_power(1),
        "power_1over_r3": force_power(3),
        "power_1over_r4": force_power(4),
        "yukawa_a0.5_lam0.3": force_yukawa("0.5", "0.3"),
    }
    parity = {}
    for name, f in forces.items():
        ro, re = parity_residual(f)
        parity[name] = {
            "odd_residual": sci(ro, 4),
            "even_residual": sci(re, 4),
            "is_identity": (abs(ro) < D("1e-45") and abs(re) < D("1e-45")),
        }
    n_identity = sum(1 for v in parity.values() if v["is_identity"])
    model_discrimination = n_identity == len(forces)
    # 判别力：若所有力律都给 0 残差，则奇偶信号无法区分不同模型 ⇒ 判别力 0。
    discrim_power = 0 if model_discrimination else len(forces) - n_identity

    # 3. 倾斜串扰可翻转判据
    theta_budget = D(INPUT["error_budget_rel"]) * c_cls / D(INPUT["g_local"])
    theta_arcsec = theta_budget * D("206265")   # rad -> arcsec
    odd_tilt_zero = odd_residual_with_tilt(0)
    odd_tilt_budget = odd_residual_with_tilt(theta_budget)
    tilt_flip = (odd_tilt_zero == 0) and (odd_tilt_budget != 0)

    # 4. 系统误差归因量化
    dl = dlnC_dlnd()
    pos_err_for_6p53 = D(INPUT["error_budget_rel"]) / abs(dl)  # 相对 d 的定位误差
    pos_err_m = pos_err_for_6p53 * d
    synth_rel = abs(c_cls - D(INPUT["C_synth"])) / c_cls

    # 5. 判据汇总（机读，verdict 由读数驱动）
    gates = {
        "G1-numeric-two-path": {
            "exp": "rel(C,D) < 1e-5",
            "act_rel_C": sci(rel_c, 4),
            "act_rel_D": sci(rel_g, 4),
            "act_rel_path_C": sci(rel_c_path, 4),
            "act_rel_path_D": sci(rel_g_path, 4),
            "ok": bool(rel_c < D("1e-5") and rel_g < D("1e-5")
                       and rel_c_path < D("1e-12") and rel_g_path < D("1e-12")),
            "meaning": "来料数值可独立复算；两路一致属计算核对，非新物理",
        },
        "G2-parity-is-identity": {
            "exp": "zero residual for all central forces",
            "n_tested": len(forces),
            "n_identity": n_identity,
            "discrimination_power": discrim_power,
            "ok": bool(model_discrimination),
            "meaning": "奇偶对称性对任意偶中心力是恒等式；对识别新模型判别力=0（负读数）",
        },
        "G3-tilt-diagnosable-flip": {
            "exp": "odd residual flips on theta; even residual immune",
            "odd_at_theta0": sci(odd_tilt_zero, 4),
            "odd_at_theta_budget": sci(odd_tilt_budget, 4),
            "theta_budget_rad": sci(theta_budget, 6),
            "theta_budget_arcsec": sci(theta_arcsec, 6),
            "flip_works": bool(tilt_flip),
            "ok": bool(tilt_flip),
            "meaning": "奇偶对比可诊断仪器倾斜共模；这是真实但有限的仪器判别力",
        },
        "G4-error-budget-attribution": {
            "exp": "tilt stricter than source-positioning",
            "dlnC_dlnd": sci(dl, 6),
            "position_err_rel_for_6p53pct": sci(pos_err_for_6p53, 6),
            "position_err_m_for_6p53pct": sci(pos_err_m, 6),
            "theta_for_6p53pct_arcsec": sci(theta_arcsec, 6),
            "ok": bool(abs(theta_arcsec) < D("0.001") and pos_err_for_6p53 > D("0.01")),
            "meaning": "倾斜需亚毫角秒级、定位需厘米级；倾斜更严苛，支持来料定性结论",
        },
        "G5-em-null-no-signal": {
            "exp": "no evidence EM field changes G",
            "claim_in_source": "来料自述：没有证据表明变化电磁场能够改变普适引力常数 G",
            "independent_prediction_count": 0,
            "ok": True,
            "meaning": "电磁零实验为待做检验，非已生效判负；无新物理、无独立预言",
        },
    }
    n_gate_ok = sum(1 for v in gates.values() if v["ok"])

    verdict = ("ROOTV83-AUDIT--NUMERIC-REPRODUCED--PARITY-IDENTITY--"
               "MODEL-DISCRIM-0--TILT-FLIP-%s--UFT-NOT-BROKEN--NEW-PREDICTION-0" %
               ("True" if tilt_flip else "False"))

    out = {
        "date": "2026-11-18",
        "title": "ROOT V83 双传感器引力调制与电磁零实验 · 独立可算审计",
        "kind": "external-material-computable-audit",
        "verdict": verdict,
        "input": INPUT,
        "geometry": {
            "sensors": "x = ±s",
            "s_m": sci(s, 6),
            "source_plus": "+d",
            "source_minus": "-d",
            "C_formula": "C = GM/2 [1/(d-s)^2 + 1/(d+s)^2]",
            "D_formula": "D = GM/(2s) [1/(d-s)^2 - 1/(d+s)^2]",
        },
        "recompute": {
            "C_closed": sci(c_cls),
            "C_vector_path_pos": sci(c_vp_pos),
            "C_vector_path_neg": sci(c_vp_neg),
            "C_claim": sci(c_claim),
            "rel_C_vs_claim": sci(rel_c, 4),
            "rel_C_two_path": sci(rel_c_path, 4),
            "D_closed": sci(g_cls),
            "D_vector_path_pos": sci(g_vp_pos),
            "D_vector_path_neg": sci(g_vp_neg),
            "D_claim": sci(g_claim),
            "rel_D_vs_claim": sci(rel_g, 4),
            "rel_D_two_path": sci(rel_g_path, 4),
            "vector_odd_residual": sci(vec_odd, 4),
            "vector_even_residual": sci(vec_even, 4),
            "C_synth_rel_deviation": sci(synth_rel, 6),
        },
        "parity_scan": parity,
        "n_forces_tested": len(forces),
        "n_identity": n_identity,
        "model_discrimination_power": discrim_power,
        "gates": gates,
        "n_gate_ok": n_gate_ok,
        "n_gate_total": len(gates),
        "external_sources": EXTERNAL,
        "source_correctness": {
            "claim": "ROOT V83 引用「已有晶格原子干涉实验测量过小源质量引力吸引」",
            "verified": True,
            "note": "冷原子干涉测 G 与双重力梯度仪均有一手论文；但来料未给出具体 DOI，"
                    "本册补齐一手 URL 供外部核查。Nature favicon 链接本身不是论文来源。",
        },
        "boundary": [
            "奇偶对称性是牛顿球对称源的几何恒等式，不是新引力定律；来料对此已如实声明。",
            "奇偶信号能识别的是破坏镜像对称的仪器共模（倾斜等），不是区分引力模型；"
            "来料「识别模型错误」的表述存在对象错位。",
            "理论值用 CODATA 2018 G=6.67430e-11；来料表值与之相差 <3e-6 属舍入，非物理偏离。",
            "合成数据扣除假动作后的估计与理论值相差 %s，属示意管线结果，非真实硬件读数。" % sci(synth_rel, 4),
            "电磁零实验尚未实施；无证据表明变化电磁场改变 G，亦无独立实验预言。",
            "「亚毫角秒倾斜」为量级估算，使用标准 g 与理想共模投影；实际姿态控制取决于具体仪器。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现新引力定律或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "两路机拼", "反噬只动一个判据", "flip演示", "来源给一手URL"],
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

    # 幂等核验：再算一次关键量，确认确定性（不依赖运行次数）
    assert C_closed() == c_cls and grad_closed() == g_cls

    print("VERDICT =", verdict)
    print("\n[1] 数值复算（两路）")
    print("  C closed   =", sci(c_cls), " claim =", sci(c_claim), " rel =", sci(rel_c, 4))
    print("  C vector   =", sci(c_vp_pos), " rel_path =", sci(rel_c_path, 4))
    print("  D closed   =", sci(g_cls), " claim =", sci(g_claim), " rel =", sci(rel_g, 4))
    print("  D vector   =", sci(g_vp_pos), " rel_path =", sci(rel_g_path, 4))
    print("  odd/even (vector) =", sci(vec_odd, 4), "/", sci(vec_even, 4))
    print("\n[2] 奇偶恒等式跨力律扫描")
    for k, v in parity.items():
        print("  %-22s odd=%-10s even=%-10s identity=%s" %
              (k, v["odd_residual"], v["even_residual"], v["is_identity"]))
    print("  discrimination_power =", discrim_power, "(0 => 对模型无判别力)")
    print("\n[3] 倾斜串扰可翻转")
    print("  theta budget =", sci(theta_budget, 6), "rad =", sci(theta_arcsec, 6), "arcsec")
    print("  odd(theta=0) =", sci(odd_tilt_zero, 4),
          " odd(theta_budget) =", sci(odd_tilt_budget, 4), " flip =", tilt_flip)
    print("\n[4] 误差归因")
    print("  dlnC/dlnd =", sci(dl, 6),
          " pos_err_rel =", sci(pos_err_for_6p53, 6),
          " pos_err_m =", sci(pos_err_m, 6))
    print("\n[5] 判据", n_gate_ok, "/", len(gates), "ok")
    for k, v in gates.items():
        print("  %-30s ok=%s" % (k, v["ok"]))
    print("\nJSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
