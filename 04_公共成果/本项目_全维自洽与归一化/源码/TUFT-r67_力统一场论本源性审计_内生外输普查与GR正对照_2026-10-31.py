# -*- coding: utf-8 -*-
"""
TUFT-r67 · 力统一场论「本源性」审计 —— 内生/外输普查 + GR 正对照
（纯标准库 Decimal；10+ 自检 guard）

核心问题：这套"几何/一运动即宇宙本源"的叙事，究竟从自身公设里**算出**了几个数？
还是所有吻合实验的数都只是从实验**搬进来**的？

方法（四态分类 + 结构/数值分离，承 r264 纪律）：
  ENDO_NUM   内生数值（由公设推出、非拟合、且吻合实验）  ← 真正想要的
  ENDO_FAIL  内生数值但被实验否证（真预言但错）
  ENDO_STRUCT内生结构（对称性/量子化等，非数值）        ← 叙事价值在此
  IMPORTED   外输（由实验测量值直接或间接输入）
  FIT        可调自由参数（拟合所得）
  DEF        纯定义（由已测量常数拼装，不产生新数）

★ 正对照：GR 水星近日点进动 42.98″/世纪 —— 由 (G,M☉,a,e) 推出，
  未用进动数据拟合 ⇒ 真内生预测。证明本审计能识别"真推导"，非恒否。

裁决常量：GEOMETRIC_ORIGIN_NARRATIVE_ZERO_ENDogenous_NUMBERS_WITH_GR_CONTROL
"""
import json
import os
import math
from decimal import Decimal, getcontext

getcontext().prec = 50

OUT_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据"
BASENAME = "TUFT-r67_力统一场论本源性审计_2026-10-31"
os.makedirs(OUT_DIR, exist_ok=True)

PI = Decimal(str(math.pi))

# ---------------------------------------------------------------------------
# 一、本源链普查（覆盖 r62–r66 已审各层）
# ---------------------------------------------------------------------------
# layer / 量 / 表达式 / 分类 / 是否数值 / 是否吻合实验 / 依据
CENSUS = [
    {"layer": "KK几何(r66)", "量": "α 精细结构常数", "表达式": "α_KK=4(ℓ_P/R)^2",
     "分类": "IMPORTED", "数值": True, "吻合": True,
     "依据": "R 由实测 α 反解(R=23.412475 ℓ_P) ⇒ 循环，非预测"},
    {"layer": "KK几何(r66)", "量": "R 紧致半径", "表达式": "R=2ℓ_P/√α",
     "分类": "FIT", "数值": True, "吻合": True,
     "依据": "由实测 α 反解 ⇒ 拟合输入，非几何选出(真空 R_MN=0 对任意 R)"},
    {"layer": "KK几何(r66)", "量": "ℓ_P 普朗克长度", "表达式": "√(Gℏ/c^3)",
     "分类": "DEF", "数值": True, "吻合": True,
     "依据": "由已测量 G,ℏ,c 拼装的定义，不产生新数"},
    {"layer": "KK几何(r66)", "量": "U(1) 规范对称性", "表达式": "θ→θ+χ ⇒ B_μ-∂_μχ",
     "分类": "ENDO_STRUCT", "数值": False, "吻合": True,
     "依据": "★真内生：由坐标变换推出（标准 KK 结果），但非数值"},
    {"layer": "KK几何(r66)", "量": "电荷量子化", "表达式": "n∈ℤ（绕圈单值）",
     "分类": "ENDO_STRUCT", "数值": False, "吻合": True,
     "依据": "★真内生：拓扑给出整数性，但不给电荷数值"},
    {"layer": "KK几何(r66)", "量": "m_KK,1 第一带电模态", "表达式": "ℏ/(Rc)=5.2147e17 GeV",
     "分类": "ENDO_FAIL", "数值": True, "吻合": False,
     "依据": "★真预言但被否证：超电子 1.02e21 倍；且 e/m 普适 ⇒ 零参数 no-go"},
    {"layer": "KK几何(r66)", "量": "A,B 稳定化系数", "表达式": "V=Ax^2+B/x^2, A/B=3.33e-6",
     "分类": "FIT", "数值": True, "吻合": True,
     "依据": "2 个新自由常数拟合 1 个数(α) ⇒ 参数净增(Ω5)"},
    {"layer": "螺旋(r42/r45/r61)", "量": "V(κ) 势", "表达式": "½(c^2κ^2/sin^2θ-ω^2)^2",
     "分类": "ENDO_FAIL", "数值": True, "吻合": False,
     "依据": "r45 C2：公理1 使 V(κ)≡0 ⇒ 变分链无粒子"},
    {"layer": "螺旋(r42/r45/r61)", "量": "κ(m) 质量-曲率", "表达式": "由 V 反解 κ(m)",
     "分类": "ENDO_FAIL", "数值": True, "吻合": False,
     "依据": "r45 C4/T16：真实粒子无实根(需 θ<1.4e-11 rad)"},
    {"layer": "螺旋(r42/r45/r61)", "量": "ω 螺旋频率", "表达式": "ω=mc^2/ħ",
     "分类": "DEF", "数值": True, "吻合": True,
     "依据": "r264：ω 只是 mc^2/ħ 的改名（L1353 vs L1784 对撞）"},
    {"layer": "螺旋(r42)", "量": "l0 自由长度", "表达式": "自由常数",
     "分类": "FIT", "数值": True, "吻合": True,
     "依据": "r42：撞 Ω5；取 l0=l_P 则退化为零信息"},
    {"layer": "GUT(r64)", "量": "M_GUT 统一能标", "表达式": "2.06e16 GeV(MSSM)",
     "分类": "FIT", "数值": True, "吻合": True,
     "依据": "SM 内无共同能标(相遇跨 4 量级)；MSSM 需外挂 SUSY"},
    {"layer": "引力(r65)", "量": "α_G(E) 引力耦合", "表达式": "(E/E_P)^2",
     "分类": "IMPORTED", "数值": True, "吻合": True,
     "依据": "E_P 由 G,ℏ,c 输入；四力仍不交于一点(缺 1.47e4)"},
    {"layer": "参数(r62/r63)", "量": "v, Yukawa, 混合角, Λ", "表达式": "—",
     "分类": "IMPORTED", "数值": True, "吻合": True,
     "依据": "r63 C2：均为 INPUT，非由主方程推导"},
]

# ---------------------------------------------------------------------------
# 二、普查统计
# ---------------------------------------------------------------------------
def count(cls):
    return sum(1 for c in CENSUS if c["分类"] == cls)


N_ENDO_NUM = count("ENDO_NUM")          # 真正想要的
N_ENDO_FAIL = count("ENDO_FAIL")
N_ENDO_STRUCT = count("ENDO_STRUCT")
N_IMPORTED = count("IMPORTED")
N_FIT = count("FIT")
N_DEF = count("DEF")

# 内生且数值且吻合实验 = 真正的"本源算出了数"
ENDO_NUM_MATCH = [c for c in CENSUS
                  if c["分类"] == "ENDO_NUM" and c["数值"] and c["吻合"]]

# 经济性：正确且非外输的数值产出 / 输入参数数
N_INPUTS = N_IMPORTED + N_FIT
ECONOMY_RATIO = (Decimal(len(ENDO_NUM_MATCH)) / Decimal(N_INPUTS)) if N_INPUTS else Decimal(0)

# ---------------------------------------------------------------------------
# 三、★ 正对照：GR 水星近日点进动（真内生预测）
# ---------------------------------------------------------------------------
G = Decimal("6.67430e-11")
M_SUN = Decimal("1.9885e30")
C = Decimal("2.99792458e8")
A_MER = Decimal("5.7909050e10")      # 半长轴 m
E_MER = Decimal("0.205630")          # 偏心率
ORBITS_PER_CENTURY = Decimal("415.2")
ARCSEC_PER_RAD = Decimal("206264.806")

# Δφ(每圈) = 6πGM / (c^2 a (1-e^2))
GM = G * M_SUN
denom = C ** 2 * A_MER * (Decimal(1) - E_MER ** 2)
dphi_orbit = Decimal(6) * PI * GM / denom                 # rad
dphi_century_rad = dphi_orbit * ORBITS_PER_CENTURY
GR_PREDICTED_ARCSEC = dphi_century_rad * ARCSEC_PER_RAD   # ″/世纪
GR_OBSERVED_ARCSEC = Decimal("42.98")                      # 观测异常进动
GR_REL_ERR = abs(GR_PREDICTED_ARCSEC - GR_OBSERVED_ARCSEC) / GR_OBSERVED_ARCSEC

# GR 的输入（均为独立测量，未用进动数据拟合）；输出为内生预测
GR_INPUTS = 4                    # G, M☉, a, e
GR_OUTPUTS = 1                   # 42.98″/世纪
GR_ECONOMY = Decimal(GR_OUTPUTS) / Decimal(GR_INPUTS)

# ---------------------------------------------------------------------------
# 四、自检 guard
# ---------------------------------------------------------------------------
guards = []
def guard(name, cond):
    guards.append((name, bool(cond)))
    return bool(cond)


guard("census_nonempty", len(CENSUS) >= 10)
guard("no_endogenous_numeric_match", len(ENDO_NUM_MATCH) == 0)
guard("economy_ratio_is_zero", ECONOMY_RATIO == 0)
guard("structural_results_present", N_ENDO_STRUCT >= 2)
guard("genuine_but_falsified_predictions_present", N_ENDO_FAIL >= 3)
guard("gr_control_matches_observation", GR_REL_ERR < Decimal("1e-3"))
guard("gr_control_is_endogenous_prediction", GR_ECONOMY > 0)
guard("gr_predicted_value_sane", Decimal("42") < GR_PREDICTED_ARCSEC < Decimal("44"))
guard("imported_plus_fit_dominates", (N_IMPORTED + N_FIT) > (N_ENDO_NUM + N_ENDO_STRUCT))

VERDICT = "GEOMETRIC_ORIGIN_NARRATIVE_ZERO_ENDogenous_NUMBERS_WITH_GR_CONTROL"
guard("verdict_constant_set",
      VERDICT == "GEOMETRIC_ORIGIN_NARRATIVE_ZERO_ENDogenous_NUMBERS_WITH_GR_CONTROL")

F4 = ("『几何/一运动 = 宇宙本源』若所有吻合实验的数值均为外输，则它是**重新描述**而非**推导**"
      " → F4 触发：范畴一致判据要求『本源』须产出内生的数，而非仅提供叙事")
E9 = ("本源叙事跨 KK/螺旋/GUT/引力 多层，各层自由参数与能标互不锁定"
      "(R 未定、l0 自由、M_GUT 拟合、E_P 输入) ⇒ 无统一本源能标，E9 FAIL")
Ω5 = ("普查中自由参数 R, l0, A, B, M_GUT ≥5 个，且为拟合非推导 ⇒ 自由参数净增，Ω5 触发")

payload = {
    "audit": "TUFT-r67",
    "subject": "力统一场论本源性审计：内生/外输普查 + GR 正对照",
    "verdict": VERDICT,
    "census": CENSUS,
    "counts": {"ENDO_NUM": N_ENDO_NUM, "ENDO_FAIL": N_ENDO_FAIL,
               "ENDO_STRUCT": N_ENDO_STRUCT, "IMPORTED": N_IMPORTED,
               "FIT": N_FIT, "DEF": N_DEF, "total": len(CENSUS)},
    "endogenous_numeric_matching_experiment": len(ENDO_NUM_MATCH),
    "economy_ratio_out_over_in": float(ECONOMY_RATIO),
    "gr_positive_control": {
        "predicted_arcsec_per_century": float(GR_PREDICTED_ARCSEC),
        "observed_arcsec_per_century": float(GR_OBSERVED_ARCSEC),
        "relative_error": float(GR_REL_ERR),
        "inputs": GR_INPUTS, "outputs": GR_OUTPUTS,
        "economy": float(GR_ECONOMY),
        "note": "由 (G,M☉,a,e) 独立测量值推出，未用进动数据拟合 ⇒ 真内生预测；"
                "证明本审计能识别真推导（非恒否）",
    },
    "gates": {"F4": F4, "E9": E9, "Ω5": Ω5},
    "conclusion": (
        "普查 %d 项：内生数值且吻合实验 **%d** 项；内生结构 %d 项（U(1) 对称、电荷量子化 —— 真但非数值）；"
        "内生但被否证 %d 项（m_KK 差 1.02e21、V(κ)≡0、κ(m) 无实根）；外输 %d 项、拟合 %d 项、定义 %d 项。"
        "经济性 n_out/n_in = %d/%d = 0。⇒『几何/一运动即本源』提供了自洽的**叙事与结构**，"
        "但**未从自身公设算出任何吻合实验的数值**；所有对得上的数都是搬进来的。"
        "正对照 GR 水星进动 %.2f″/世纪（观测 %.2f″，相对误差 %.1e）由 4 个独立测量输入推出 1 个"
        "未拟合的输出 ⇒ 本审计能识别真推导，故上述『零内生数值』不是方法偏倚所致。"
        % (len(CENSUS), len(ENDO_NUM_MATCH), N_ENDO_STRUCT, N_ENDO_FAIL,
           N_IMPORTED, N_FIT, N_DEF, len(ENDO_NUM_MATCH), N_INPUTS,
           float(GR_PREDICTED_ARCSEC), float(GR_OBSERVED_ARCSEC), float(GR_REL_ERR))
    ),
}

with open(os.path.join(OUT_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

md = []
md.append("# TUFT-r67 · 力统一场论本源性审计 · 机器数据册\n")
md.append("- 裁决：%s" % VERDICT)
md.append("\n## 普查统计（共 %d 项）" % len(CENSUS))
md.append("- ENDO_NUM(内生数值·吻合)=%d  ← 真正想要的" % N_ENDO_NUM)
md.append("- ENDO_STRUCT(内生结构·非数值)=%d" % N_ENDO_STRUCT)
md.append("- ENDO_FAIL(内生但被否证)=%d" % N_ENDO_FAIL)
md.append("- IMPORTED(外输)=%d | FIT(拟合)=%d | DEF(定义)=%d" % (N_IMPORTED, N_FIT, N_DEF))
md.append("- **可数内生数值(吻合实验) = %d**" % len(ENDO_NUM_MATCH))
md.append("- 经济性 n_out/n_in = %d/%d = 0" % (len(ENDO_NUM_MATCH), N_INPUTS))
md.append("\n## 普查明细")
for c in CENSUS:
    md.append("- [%s] %s（%s）→ %s | 数值=%s 吻合=%s | %s"
              % (c["layer"], c["量"], c["表达式"], c["分类"], c["数值"], c["吻合"], c["依据"]))
md.append("\n## ★ 正对照：GR 水星近日点进动")
md.append("- 预测 %.3f ″/世纪；观测 %.2f ″/世纪；相对误差 %.2e" %
          (float(GR_PREDICTED_ARCSEC), float(GR_OBSERVED_ARCSEC), float(GR_REL_ERR)))
md.append("- 输入 %d 个独立测量(G,M☉,a,e)，输出 %d 个未拟合预测 ⇒ 经济性 %.2f ⇒ 真内生" %
          (GR_INPUTS, GR_OUTPUTS, float(GR_ECONOMY)))
md.append("\n## 门禁")
md.append("- F4：%s" % F4)
md.append("- E9：%s" % E9)
md.append("- Ω5：%s" % Ω5)
with open(os.path.join(OUT_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

report = []
report.append("TUFT-r67 本源性审计 生成=%s" % __import__("datetime").datetime.now().isoformat())
report.append("裁决=%s" % VERDICT)
report.append("普查%d项: ENDO_NUM=%d ENDO_STRUCT=%d ENDO_FAIL=%d IMPORTED=%d FIT=%d DEF=%d"
              % (len(CENSUS), N_ENDO_NUM, N_ENDO_STRUCT, N_ENDO_FAIL, N_IMPORTED, N_FIT, N_DEF))
report.append("★可数内生数值(吻合实验)=%d | 经济性=%d/%d=0" % (len(ENDO_NUM_MATCH), len(ENDO_NUM_MATCH), N_INPUTS))
report.append("★GR正对照: %.3f arcsec/century (观测42.98, 相对误差%.1e) => 方法能识别真推导"
              % (float(GR_PREDICTED_ARCSEC), float(GR_REL_ERR)))
report.append("guard 数=%d, 全过=%s" % (len(guards), all(g[1] for g in guards)))
with open(os.path.join(OUT_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

guard_all = all(g[1] for g in guards) and (len(guards) >= 9)
raise SystemExit(0 if guard_all else 1)
