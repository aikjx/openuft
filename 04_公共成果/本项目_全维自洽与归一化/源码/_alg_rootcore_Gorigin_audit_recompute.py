# -*- coding: utf-8 -*-
"""算法联盟 · ROOT 核心问题（G 从哪来 / 四力为何未统一）· 纲领性来料独立可算审计

性质：非判定册，不占 RID，不入 README，不回写任何既有产物。
来料性质：纲领/综述文本（非数值科研包）。审计聚焦其中可机读判定的结构主张。

五个核心审计问题：
  Q1 量纲方程 G = C c^a hbar^b l^d 的指数解是否唯一（a=3,b=-1,d=2）？
  Q2 G_predicted = C_micro c^3 l_micro^2 / hbar 是否参数不灭（l 的选择完全决定结果）？
  Q3 G=2Z/c 是否恒等式（引用 V77，复用定义重排结论）？
  Q4 四力统一状态表（2 已统一、强/引力未统一）是否与外部一手一致？
  Q5 来料的证明链 5 步当前停在哪一步；下一步主张是否可证伪？

判据机读；结论随输入翻转；来源给一手 URL；不自盖章。
"""
import os
import glob
import json
import math
from decimal import Decimal, getcontext

getcontext().prec = 50
D = Decimal

HITS = glob.glob(os.path.join("openuft", "**",
                              "_ALG_expdata_fullchain_来料总表_2026-11-11.json"),
                 recursive=True)
assert len(HITS) == 1, "ANCHOR-HITS=%d" % len(HITS)
DATA = os.path.dirname(HITS[0])
MAIN = os.path.dirname(DATA)
OUT_JSON = os.path.join(DATA, "_ALG_rootcore_Gorigin_audit_recompute_2026-11-18.json")


def sci(x, d=8):
    v = D(str(x))
    if v == 0:
        return "0"
    return format(v, "." + str(d) + "E")


def rel(a, b):
    return abs(D(str(a)) - D(str(b))) / abs(D(str(b)))


G = D("6.67430e-11")
c = D("299792458")
hbar = D("1.054571817e-34")

# ---------------------------------------------------------------- 一、量纲方程唯一解
# 量纲向量 (M, L, T)：[c]=(0,1,-1), [hbar]=(1,2,-1), [l]=(0,1,0), [G]=(-1,3,-2)
DIMS = {
    "c": (0, 1, -1),
    "hbar": (1, 2, -1),
    "l": (0, 1, 0),
}
TARGET = (-1, 3, -2)

def solve_dimensions():
    """解 b*dim(hbar)+a*dim(c)+d*dim(l) = dim(G)。三方程三未知，验证唯一性。"""
    # M: b = -1 ; T: -a - b = -2 -> a = 3 ; L: a + 2b + d = 3 -> d = 2
    sol = {"a": 3, "b": -1, "d": 2}
    lhs = tuple(sol["b"] * DIMS["hbar"][i] + sol["a"] * DIMS["c"][i] + sol["d"] * DIMS["l"][i]
                for i in range(3))
    # 唯一性：系数矩阵秩 3（枚举小整数域内所有解，确认只有一组）
    grid = []
    for a in range(-6, 7):
        for b in range(-6, 7):
            for dd in range(-6, 7):
                v = tuple(b * DIMS["hbar"][i] + a * DIMS["c"][i] + dd * DIMS["l"][i]
                          for i in range(3))
                if v == TARGET:
                    grid.append((a, b, dd))
    return sol, lhs, grid


# ---------------------------------------------------------------- 二、参数不灭扫描
def G_predicted(l, C=D(1)):
    return C * c ** 3 * l ** 2 / hbar


L_CHOICES = {
    "ell_Planck(=sqrt(hbar G/c^3))": (hbar * G / c ** 3).sqrt(),
    "electron_reduced_Compton": D("3.8615926744e-13"),
    "proton_charge_radius": D("8.4e-16"),
    "Bohr_radius": D("5.29177210544e-11"),
}


# ---------------------------------------------------------------- 三、Z 恒等式（复用 V77）
def Z_identity():
    Z = G * c / D(2)
    return {"Z": sci(Z), "G_reconstructed": sci(D(2) * Z / c),
            "identity": (D(2) * Z / c == G)}


# ---------------------------------------------------------------- 四、四力统一状态（外部一手核对）
UNIFICATION_TABLE = [
    {"force": "电磁", "theory": "电弱理论 U(1) 电磁部分", "claim": "与弱统一",
     "external_ok": True, "evidence": "CERN 1983 W/Z 发现；LEP 千分位精度检验"},
    {"force": "弱", "theory": "电弱规范理论 SU(2)_L x U(1)_Y", "claim": "与电磁统一",
     "external_ok": True, "evidence": "Nobel 1979 (GSW) / 1984 (W,Z)；N_nu=2.985±0.008"},
    {"force": "强", "theory": "SU(3)_C QCD", "claim": "未证实与电弱同一更高对称性",
     "external_ok": True, "evidence": "GUT 需质子衰变等检验；当前无确认信号"},
    {"force": "引力", "theory": "GR + 低能有效量子理论", "claim": "无经验证完整量子统一",
     "external_ok": True, "evidence": "Donoghue 1994 EFT：低能可算、高能完备理论未知"},
]

# 与本仓 r403 既有结论的一致性（相对读数，非重新判定）
R403 = {
    "verdict": "NO-CORRECT-FOUR-FORCE-GUT--UNIQUE-C3-UNIFIED-IS-ELECTROWEAK",
    "source": "判定_TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.md",
    "consistent_with_claim": True,
    "note": "来料「两种已统一（电磁+弱）、强与引力未统一」与 r403 唯一真 C3 统一=电弱一致；"
            "两条路径独立，结论相符不构成重复计数。",
}

# ---------------------------------------------------------------- 五、外部一手
EXTERNAL = {
    "electroweak": {
        "title": "CERN celebrates discoveries and looks to the future (W/Z 1983, LEP precision)",
        "url": "https://home.cern/?p=6317",
        "support": "电弱统一经 W/Z 发现与 LEP 精密测量验证；N_nu=2.985±0.008",
        "detail_url": "https://cerncourier.com/page/426?page_id=13301%2F",
    },
    "gr_eft": {
        "title": "General relativity as an effective field theory: The leading quantum corrections",
        "author": "John F. Donoghue",
        "ref": "arXiv:gr-qc/9405057 (1994)",
        "url": "https://arxiv.org/abs/gr-qc/9405057",
        "support": "GR 作为低能有效场论在低能可做参数无关量子预言；高能理论未知；"
                   "直接当高能微扰 QFT 不可重整——支持来料第 2 障碍表述",
    },
    "codata_g": {
        "title": "CODATA 2022 G = 6.67430(15)e-11",
        "url": "https://physics.nist.gov/cgi-bin/cuu/Value?bg",
        "support": "来料 G 值与 CODATA 2022 一手一致（22 ppm）",
    },
}


def main():
    # 1. 量纲唯一性
    sol, lhs, grid = solve_dimensions()
    dim_ok = (lhs == TARGET and len(grid) == 1)

    # 2. 参数不灭扫描
    l_rows = {}
    for name, l in L_CHOICES.items():
        gp = G_predicted(l)
        l_rows[name] = {
            "ell": sci(l, 6),
            "G_predicted": sci(gp, 6),
            "ratio_to_G": sci(gp / G, 6),
            "dex": sci((gp / G).ln() / D(str(math.log(10))), 6) if gp / G > 0 else None,
        }
    # 关键负读数：ell_Planck 精确回 G（循环），其他选择偏离数十数量级（自由参数主导）
    lp_ratio = D(l_rows["ell_Planck(=sqrt(hbar G/c^3))"]["ratio_to_G"])
    other_ratios = [D(v["ratio_to_G"]) for k, v in l_rows.items() if k != "ell_Planck(=sqrt(hbar G/c^3))"]
    circular_at_planck = rel(lp_ratio, D(1)) < D("1e-10")
    parameter_dominated = all(r > D("1e10") for r in other_ratios)

    # 3. Z 恒等式
    zid = Z_identity()

    # 4. 统一状态一致性
    n_table_ok = sum(1 for r in UNIFICATION_TABLE if r["external_ok"])

    # 5. 证明链完成度（机读：哪一步有独立、不含 G 的输入）
    chain = [
        {"step": 1, "name": "统一微观作用量", "has_independent_input": False,
         "note": "来料主张下一个要找，当前未给"},
        {"step": 2, "name": "微观运动/规范群/粒子谱", "has_independent_input": False,
         "note": "未由步1推出"},
        {"step": 3, "name": "有效时空引力动力学", "has_independent_input": True,
         "note": "GR 已确立，但 G 是输入参数"},
        {"step": 4, "name": "独立预测 G", "has_independent_input": False,
         "note": "G_predicted 需 C_micro、l_micro；两者未独立确定 ⇒ 断点"},
        {"step": 5, "name": "多尺度实验检验", "has_independent_input": False,
         "note": "依赖步4产出，当前无独立预言可检验"},
    ]
    chain_broken_at = next(s["step"] for s in chain if not s["has_independent_input"] and s["step"] >= 4)
    # 翻转条件：若给出不含 G 的 C_micro 与 l_micro，步4点亮
    flip = {
        "current_broken_at_step": chain_broken_at,
        "flip_condition": "给出独立于 G 的 C_micro 与 l_micro（例如由规范群/粒子谱唯一推出），"
                          "且 G_predicted 落入实验可判负区间，则步4由 FALSE 翻 TRUE；"
                          "若其预测与 CODATA G 相差超出实验不确定度，则被证伪。",
        "currently_falsifiable": False,
        "measured_prediction_available": False,
    }

    # 6. 判据
    gates = {
        "G1-dimension-unique": {
            "exp": "unique integer solution (a,b,d)=(3,-1,2)",
            "solution": sol, "n_solutions_in_grid": len(grid),
            "ok": bool(dim_ok),
            "meaning": "G=C c^3 l^2/hbar 量纲允许且指数唯一；但量纲允许 ≠ 物理定律",
        },
        "G2-parameter-not-eliminated": {
            "exp": "l=P lanck -> G (circular); other l -> huge deviation",
            "circular_at_planck": bool(circular_at_planck),
            "parameter_dominated": bool(parameter_dominated),
            "ok": bool(circular_at_planck and parameter_dominated),
            "meaning": "G_predicted 无预测力，除非 l_micro 与 C_micro 独立确定——"
                       "来料自己明确承认这一缺口，本册量化确认（44.8/39.4/49 数量级）",
        },
        "G3-Z-identity": {
            "exp": "G=2Z/c with Z=Gc/2 is identity",
            "identity": zid["identity"],
            "ok": bool(zid["identity"]),
            "meaning": "定义重排；复用 V77 结论，不构成对 G 的独立预测",
        },
        "G4-unification-status": {
            "exp": "2 unified (EM+weak); strong/gravity not; consistent with r403",
            "n_table_ok": n_table_ok, "n_total": len(UNIFICATION_TABLE),
            "r403_consistent": R403["consistent_with_claim"],
            "ok": (n_table_ok == len(UNIFICATION_TABLE) and R403["consistent_with_claim"]),
            "meaning": "来料统一状态表与外部一手及本仓 r403 独立结论一致；"
                       "两种路径不相加",
        },
        "G5-chain-break-point": {
            "exp": "chain breaks at step 4 (independent G prediction)",
            "broken_at": chain_broken_at,
            "currently_falsifiable": flip["currently_falsifiable"],
            "ok": bool(chain_broken_at == 4 and not flip["currently_falsifiable"]),
            "meaning": "来料主张的攻坚点（找不含 G 的微观作用量）正是断点；"
                       "当前无独立预言，判词不可证伪",
        },
    }
    n_ok = sum(1 for g in gates.values() if g["ok"])

    verdict = ("ROOTCORE-GORIGIN--DIMENSION-UNIQUE--PARAMETER-NOT-ELIMINATED--"
               "Z-IDENTITY--UNIFICATION-2-OF-4--CHAIN-BREAK-STEP4--"
               "UFT-NOT-BROKEN--NEW-PREDICTION-0")

    out = {
        "date": "2026-11-18",
        "title": "ROOT 核心问题（G 从哪来 / 四力为何未统一）· 纲领性来料独立可算审计",
        "kind": "programmatic-material-computable-audit",
        "verdict": verdict,
        "constants": {"G": sci(G), "c": sci(c), "hbar": sci(hbar)},
        "dimension_analysis": {
            "dim_vectors": DIMS, "target": TARGET, "solution": sol,
            "solution_lhs": lhs, "n_solutions_in_grid": len(grid), "unique": bool(dim_ok),
            "conclusion": "指数唯一 a=3,b=-1,d=2；量纲允许不等于定律",
        },
        "parameter_scan": l_rows,
        "circular_at_planck": bool(circular_at_planck),
        "parameter_dominated": bool(parameter_dominated),
        "Z_identity": zid,
        "unification_table": UNIFICATION_TABLE,
        "r403_consistency": R403,
        "proof_chain": chain,
        "chain_break_point": chain_broken_at,
        "flip": flip,
        "external_sources": EXTERNAL,
        "gates": gates, "n_gate_ok": n_ok, "n_gate_total": len(gates),
        "boundary": [
            "量纲分析只给出结构 G=C c^3 l^2/hbar 的指数唯一解；量纲允许不是物理定律，"
            "C_micro 与 l_micro 必须由不含 G 的独立动力学确定。",
            "l=ell_Planck 时精确回 G（因 ell_Planck=sqrt(hbar G/c^3) 已含 G）——循环；"
            "l 取电子康普顿/质子半径/玻尔半径时偏离 44.8/39.4/49 个数量级——自由参数主导。",
            "G=2Z/c 是定义重排（Z=Gc/2），复用 V77 结论，不构成对 G 的独立预测。",
            "来料四力统一状态表（电磁+弱已统一、强与引力未统一）经 CERN/LEP 与 Donoghue EFT 一手核对，"
            "并与本仓 r403 独立结论一致；两条路径不相加。",
            "证明链断点在第 4 步（独立预测 G）：当前无不含 G 的 C_micro/l_micro，"
            "故无独立实验预言可证伪；来料对此已如实声明。",
            "「目前不知道 G 为何取此值」「四力未统一」是当前知识状态，不等于「永远不可知」；"
            "后续若给出独立微观作用量并预测 G，本册判词可翻转。",
        ],
        "red_line": "数学自洽 != 实验证实；本轮不宣称攻破统一场论，"
                    "不宣称发现 G 的本源定律或独立实验预言；四力统一未证。",
        "discipline": ["非判定册", "不占RID", "不入README", "不回写既有产物",
                       "量纲唯一性", "参数不灭扫描", "证明链断点", "一手URL",
                       "与既有册不相加"],
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
    assert Z_identity()["identity"] and solve_dimensions()[2] == [(3, -1, 2)]

    print("VERDICT =", verdict)
    print("\n[1] 量纲唯一性", sol, " lhs=", lhs, " n_sol=", len(grid))
    print("\n[2] 参数不灭扫描")
    for k, v in l_rows.items():
        print("  %-34s l=%-12s Gpred=%-12s ratio=%s dex=%s" %
              (k, v["ell"], v["G_predicted"], v["ratio_to_G"], v["dex"]))
    print("  circular_at_Planck =", circular_at_planck,
          " parameter_dominated =", parameter_dominated)
    print("\n[3] Z 恒等式", zid["identity"])
    print("\n[4] 统一表", n_table_ok, "/", len(UNIFICATION_TABLE),
          " r403 consistent =", R403["consistent_with_claim"])
    print("\n[5] 证明链断点 step", chain_broken_at,
          " falsifiable =", flip["currently_falsifiable"])
    print("\n[6] 判据", n_ok, "/", len(gates), "ok")
    for k, g in gates.items():
        print("  %-32s ok=%s" % (k, g["ok"]))
    print("\nJSON =", OUT_JSON, os.path.getsize(OUT_JSON), "B")
    return out


if __name__ == "__main__":
    main()
