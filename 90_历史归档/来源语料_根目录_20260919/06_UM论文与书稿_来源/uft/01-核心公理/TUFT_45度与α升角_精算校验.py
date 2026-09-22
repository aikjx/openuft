# -*- coding: utf-8 -*-
"""
TUFT「费米子 45 度」与「精细结构常数升角」精算校验（H13-H17）

校验对象：
  (1) s + Lk^2 = 1，s = sin^2(eta)，Lk = cos(eta)  =>  费米子 s=1/2  =>  eta = 45 度
  (2) 玻色子 s=1 => Lk=0 => eta=90 度
  (3) 路线 A：tan(alpha_eta) = alpha            => alpha_eta  = 0.4181 度
  (4) 路线 B：tan(eta_eff)   = 1/alpha          => eta_eff    = 89.5819 度

红线（ROOT）：
  1. 只原样记录实跑所得判定，不篡改、不粉饰；
  2. 数学自洽 != 物理实证；恒等式重述不得记为"推导"；
  3. 两难（dilemma）若两支都不成立，判 FAIL 并显式写明两支，不得只挑一支反驳。

运行：
  python uft/01-核心公理/TUFT_45度与α升角_精算校验.py
产物：
  uft/01-核心公理/TUFT_45度与α升角_校验结果.json
"""

import sys
import json
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mpmath as mp
import sympy as sp

mp.mp.dps = 50

# ---------------------------------------------------------------- 常数
c = mp.mpf("299792458")
hbar = mp.mpf("1.054571817e-34")
G = mp.mpf("6.67430e-11")
m_e = mp.mpf("9.1093837015e-31")
m_p = mp.mpf("1.67262192369e-27")
e_charge = mp.mpf("1.602176634e-19")
eps0 = mp.mpf("8.8541878128e-12")
k_coulomb = 1 / (4 * mp.pi * eps0)
alpha = mp.mpf("7.2973525693e-3")          # 1/137.035999085
DEG = mp.pi / 180

RESULTS = []


def record(rid, title, verdict, severity, claim, numbers, note):
    RESULTS.append({
        "id": rid, "title": title, "verdict": verdict, "severity": severity,
        "claim": claim, "numbers": numbers, "note": note,
    })
    print("[" + verdict + "] " + rid + " " + title)
    for kk in numbers:
        print("        " + str(kk) + " = " + str(numbers[kk]))
    print("        note: " + note)
    print("")


# ================================================================= H13
def h13_identity_is_tautology():
    eta = sp.symbols("eta", real=True)
    s = sp.sin(eta) ** 2
    Lk = sp.cos(eta)
    resid = sp.simplify(s + Lk ** 2 - 1)

    # 若换一种同样"自然"的 s-eta 映射，s=1/2 解出的角度完全不同
    half = sp.Rational(1, 2)
    candidates = {
        "s = sin^2(eta)   （原稿）": float(sp.deg(sp.asin(sp.sqrt(half)))),
        "s = sin(eta)": float(sp.deg(sp.asin(half))),
        "s = sin^4(eta)": float(sp.deg(sp.asin(half ** sp.Rational(1, 4)))),
        "s = (1 + cos(eta))/2": float(sp.deg(sp.acos(2 * half - 1))),
        "s = sin^2(2 eta)": float(sp.deg(sp.asin(sp.sqrt(half)) / 2)),
        "s = eta / 90deg （线性）": 45.0,
    }

    record(
        "H13",
        "s + Lk^2 = 1 在 s=sin^2(eta), Lk=cos(eta) 下退化为三角恒等式",
        "FAIL",
        "P0",
        "把 s 定义为 sin^2(eta)、Lk 定义为 cos(eta) 后，s+Lk^2=1 即 sin^2+cos^2=1，"
        "是恒等式而非物理约束；'由 s=1/2 解出 eta=45 度'属于同义反复",
        {
            "符号残差 sin^2+cos^2-1": str(resid),
            "换映射后 s=1/2 解出的角度（度）": str({k: round(v, 4) for k, v in candidates.items()}),
            "解出的角度种数": str(len(set(round(v, 4) for v in candidates.values()))),
        },
        "关键：s=1/2 与 eta=45 度 在 s:=sin^2(eta) 的定义下【完全等价】，"
        "不存在任何'推导'。真正需要回答而未被回答的问题是："
        "为什么量子自旋 1/2 应当等于横向拓扑权重 sin^2(eta)？"
        "实跑表明换成 sin(eta)、sin^4(eta)、(1+cos)/2、sin^2(2eta) 等同样自然的映射，"
        "分别得到 30 / 57.2349 / 90 / 22.5 度（共 5 个不同值）——该映射是纯任意的，"
        "因此 45 度不是结论而是选择。",
    )


# ================================================================= H14
def h14_zero_writhe_dilemma():
    # 支一：Wr = 0 => Lk = Tw，而 Călugăreanu–White 要求 Lk ∈ Z
    allowed = []
    for deg in [0, 30, 45, 60, 90, 120, 180]:
        val = mp.cos(mp.mpf(deg) * DEG)
        allowed.append((deg, mp.nstr(val, 8), abs(val - mp.mpf(round(float(val)))) < mp.mpf("1e-30")))
    ok_angles = [a[0] for a in allowed if a[2]]

    # 45 度检验
    cos45 = mp.cos(45 * DEG)
    tw_45 = cos45
    is_int_45 = abs(tw_45 - round(float(tw_45))) < mp.mpf("1e-30")

    # 支二：若 Wr != 0，则 Lk = Tw + Wr 使 Lk 与 eta 脱钩
    # 取任意 Wr 使 Lk 为整数，此时 eta 完全自由
    wr_samples = {}
    for deg in [15, 30, 45, 60, 75]:
        tw = mp.cos(mp.mpf(deg) * DEG)
        wr_needed = 1 - tw          # 令 Lk = Tw + Wr = 1
        wr_samples[str(deg) + " 度"] = {
            "Tw": mp.nstr(tw, 6),
            "为使 Lk=1 所需 Wr": mp.nstr(wr_needed, 6),
            "Lk": "1（此时 s+Lk^2=1 要求 s=0，与 s=1/2 冲突）",
        }

    record(
        "H14",
        "Wr=0 与 45 度的二难：两支都不成立",
        "FAIL",
        "P0",
        "二难支一：Wr=0 => Lk=Tw，而 Călugăreanu–White 要求 Lk ∈ Z，"
        "故 cos(eta) ∈ Z => eta ∈ {0, 90, 180} 度，45 度被排除；"
        "二难支二：若允许 Wr≠0，则 Lk=Tw+Wr 由 Wr 承担整数性，"
        "s+Lk^2=1 与 eta 脱钩，45 度不再被任何东西约束",
        {
            "cos(45 度)": mp.nstr(cos45, 10),
            "Tw=cos(45 度) 是否为整数": str(is_int_45),
            "满足 cos(eta) ∈ Z 的角度（度）": str(ok_angles),
            "支二：任取 eta 均可由 Wr 补足整数 Lk": str(wr_samples),
        },
        "这是本次最硬的结论：'为了简化而假设 Wr=0'这一步恰恰把 45 度排除了。"
        "支一中允许的只有 0/90/180 度（90 度即玻色子，0 与 180 度为直线/反平行，"
        "kappa=0 不闭合）；支二中 eta 完全自由、45 度失去约束来源。"
        "两难无第三支：不能既用 Wr=0 锁住 Lk=Tw，又要求 Tw 取非整数值。",
    )


# ================================================================= H15
def h15_helix_not_closed():
    # 圆柱螺旋 r(u) = (R cos u, R sin u, b u)：闭合要求 b = 0（或周期后回到原点，仅 b=0）
    R, b, u, N = sp.symbols("R b u N", positive=True)
    # 一圈后位置差
    dz = sp.simplify(b * (u + 2 * sp.pi * N) - b * u)
    # 45 度时 b/R = cot(45) = 1
    b_over_R_45 = sp.simplify(sp.cot(sp.pi / 4))
    # 若要闭合必须 b=0 => eta = 90 度 => tau = 0（玻色子分支）
    eta_boson = 90

    # 若强行闭合（弯成环面纽结 T(p,q)），则 kappa, tau 非常数，定理1 稳态解失效；
    # 且 (p,q) 环面纽结的 Wr 一般非零
    torus_examples = {
        "T(2,3) 三叶结": "Wr ≠ 0（非零拧数），kappa/tau 非常数",
        "T(2,5)": "Wr ≠ 0",
        "T(3,4)": "Wr ≠ 0",
    }

    record(
        "H15",
        "圆柱螺旋（b≠0）不是闭合曲线，Călugăreanu–White 前提不成立",
        "FAIL",
        "P0",
        "Călugăreanu–White 定理适用于闭合带（或端点固定的带）；"
        "稳态圆柱螺旋 r(u)=(R cos u, R sin u, b u) 在 b≠0 时沿轴无限延伸，永不闭合",
        {
            "一圈后轴向位移 dz": str(dz) + " （b≠0 且 N≥1 时非零）",
            "45 度时 b/R = cot(45 度)": str(b_over_R_45),
            "闭合所需条件": "b = 0  ⇒  eta = 90 度  ⇒  tau = 0（落在玻色子分支）",
            "强行闭合的代价（环面纽结）": str(torus_examples),
        },
        "二难的第二层：要么保持'稳态圆柱螺旋'（kappa,tau 常数，定理1 适用）则不闭合、"
        "Călugăreanu–White 不适用；要么强行闭合（弯成环面纽结）则 kappa,tau 不再是常数、"
        "定理1 的稳态解失效，且环面纽结的 Wr≠0，又违反 H14 支一的 Wr=0 前提。"
        "因此'闭合 + 稳态圆柱螺旋 + Wr=0'三者不可兼得，而 45 度论证同时用到了这三条。",
    )


# ================================================================= H16
def h16_alpha_two_routes_conflict():
    a_route = mp.atan(alpha) / DEG              # 路线 A
    b_route = mp.atan(1 / alpha) / DEG          # 路线 B
    total = a_route + b_route

    # 两条路线对 tau/kappa 的赋值（统一按 tan(eta) = kappa/tau 的体系定义）
    # 路线 A: tan(alpha_eta) = alpha = kappa/tau  =>  tau/kappa = 1/alpha
    tau_over_kappa_A = 1 / alpha
    # 路线 B: tau_eff/kappa_eff = alpha          =>  tau/kappa = alpha
    tau_over_kappa_B = alpha
    conflict = tau_over_kappa_A / tau_over_kappa_B

    # 范畴检验：真实的引力/电磁强度比（质子-电子）
    ratio_GE = G * m_p * m_e / (k_coulomb * e_charge ** 2)
    gap_orders = mp.log10(alpha / ratio_GE)

    record(
        "H16",
        "alpha 两条路线互斥：不是两条路径，而是同一等式的互余写法 + 赋值相差 1.88e4 倍",
        "FAIL",
        "P0",
        "路线 A 的 arctan(alpha) 与路线 B 的 arctan(1/alpha) 互为余角，和为 90 度，"
        "属同一等式的两种写法，却被赋予'单孤子内部'与'双孤子复合'两种不同物理；"
        "且两者对 tau/kappa 的赋值相差 alpha^-2",
        {
            "路线 A：arctan(alpha)（度）": mp.nstr(a_route, 8),
            "路线 B：arctan(1/alpha)（度）": mp.nstr(b_route, 8),
            "两者之和（度）": mp.nstr(total, 10),
            "路线 A 隐含 tau/kappa = 1/alpha": mp.nstr(tau_over_kappa_A, 8),
            "路线 B 隐含 tau/kappa = alpha": mp.nstr(tau_over_kappa_B, 8),
            "两路线互斥倍数 alpha^-2": mp.nstr(conflict, 6),
            "真实引力/电磁强度比（质子-电子）": mp.nstr(ratio_GE, 6),
            "alpha 与该比值相差（数量级）": mp.nstr(gap_orders, 4),
        },
        "三层问题：(a) 两路线是互余角而非独立路径，重复计数；"
        "(b) 二者对 tau/kappa 的赋值相差 1.88e4 倍，不能都自洽；"
        "(c) 把 alpha 解释为'挠率(电磁)/曲率(引力)耦合比'是范畴错误——"
        "alpha 是电磁耦合自身的无量纲强度（在低能标下约 1/137），"
        "而真实的引力/电磁强度比为 4.41e-40，与 1/137 相差 37.2 个数量级。"
        "因此'alpha = tau_eff/kappa_eff'是重新贴标签，不是推导，也不构成任何可检验联系。",
    )


# ================================================================= H17
def h17_soliton_size_at_claimed_angles():
    K = m_e * c / hbar                 # sqrt(kappa^2+tau^2) = m c / hbar
    invK = 1 / K
    rows = {}
    for name, deg in [("费米 45 度", 45),
                      ("路线 B 89.5819 度", mp.atan(1 / alpha) / DEG),
                      ("路线 A 0.4181 度", mp.atan(alpha) / DEG),
                      ("玻色 90 度", 90)]:
        e = mp.mpf(deg) * DEG
        Rr = mp.sin(e) / K
        bb = mp.cos(e) / K
        rows[name] = {
            "螺旋半径 R = sin(eta)/K (m)": mp.nstr(Rr, 5),
            "螺距参数 b = cos(eta)/K (m)": mp.nstr(bb, 5),
            "sqrt(R^2+b^2) (m)": mp.nstr(mp.sqrt(Rr ** 2 + bb ** 2), 5),
            "超出点状性 1e-19 m 倍数（取 max(R,b)）": mp.nstr(max(Rr, bb) / mp.mpf("1e-19"), 4),
        }

    record(
        "H17",
        "按 45 度 / 89.58 度 / 0.42 度 取电子孤子几何，尺度均被点状性实验排除",
        "FAIL",
        "P1",
        "由定理1+定理3 得 sqrt(R^2+b^2) = hbar/(m_e c) = 3.86e-13 m（角度无关）；"
        "逐个角度实算 R 与 b，取较大者作为几何延展尺度",
        {
            "1/K = hbar/(m_e c) (m)": mp.nstr(invK, 6),
            "逐角度几何": str(rows),
            "实验点状性上限 (m)": "1e-19",
        },
        "无论把电子孤子的升角取 45 度、89.58 度还是 0.42 度，"
        "其几何延展尺度都落在 1e-13 m 量级，比点状性上限大 6 个数量级以上。"
        "这与 H11 一致：尺度由质量锁死，调角度只能改变形状分配、不能改变总尺度。",
    )


# ================================================================= 方案门禁
def gate_for_scheme_1():
    # 方案 1（把 alpha 嵌入 PDE 推氢原子精细结构）的外部硬门槛（CODATA / 实验值，非推导）
    Rydberg_eV = mp.mpf("13.605693122994")
    lamb_shift_MHz = mp.mpf("1057.844")      # 2S1/2 - 2P1/2
    fs_2P_MHz = mp.mpf("10969.13")           # 2P3/2 - 2P1/2 精细结构分裂
    g_minus_2 = mp.mpf("1.15965218073e-3")   # (g-2)/2 电子
    record(
        "GATE",
        "方案 1（嵌入 PDE 推玻尔能级 / 氢原子精细结构）的可判定门槛",
        "INFO",
        "—",
        "方案 1 有外部硬检验值；这些是需要被复现的目标量，不是本脚本推导出的结果",
        {
            "里德伯能量 E_1 (eV)": mp.nstr(Rydberg_eV, 12),
            "精细结构分裂 2P3/2-2P1/2 (MHz)": str(fs_2P_MHz),
            "Lamb 位移 2S1/2-2P1/2 (MHz)": str(lamb_shift_MHz),
            "电子反常磁矩 (g-2)/2": str(g_minus_2),
        },
        "方案 1 的前置门禁（任一不过则 PDE 无意义）："
        "(1) 必须区分 kappa_soliton / kappa_field（H12）；"
        "(2) 必须定义曲线量到场量的提升映射（H5）；"
        "(3) 必须说明电子孤子为何在 1e-19 m 下仍点状（H11/H17）。"
        "方案 2（第一性推 alpha=1/137）在本框架内只能把 alpha 定义为某个比值再'解出'，"
        "属 H13 同型循环，且无可判定终点（推不出永远是'未完成'），建议不立项。",
    )


def main():
    print("=" * 78)
    print("TUFT 45 度 / 精细结构常数升角 精算校验（H13-H17 + 方案门禁）")
    print("红线：只记录实跑结果，两难若两支皆不成立则判 FAIL 并写明两支")
    print("=" * 78)
    print("")

    h13_identity_is_tautology()
    h14_zero_writhe_dilemma()
    h15_helix_not_closed()
    h16_alpha_two_routes_conflict()
    h17_soliton_size_at_claimed_angles()
    gate_for_scheme_1()

    n = {}
    for r in RESULTS:
        n[r["verdict"]] = n.get(r["verdict"], 0) + 1
    print("=" * 78)
    print("汇总: " + str(n))
    print("=" * 78)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "TUFT_45度与α升角_校验结果.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"summary": n, "results": RESULTS}, f, ensure_ascii=False, indent=2)
    print("写出: " + out)


if __name__ == "__main__":
    main()
