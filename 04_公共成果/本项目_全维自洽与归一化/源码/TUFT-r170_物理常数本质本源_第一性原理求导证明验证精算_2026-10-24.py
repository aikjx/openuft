# -*- coding: utf-8 -*-
"""
TUFT-r170｜所有物理常数的本质本源 —— 第一性原理求导证明验证精算

00. 编号与定位
  【编号】r170。编号冲突：r169 已由并行会话占用（电磁引力互生层，README 已登记）⇒ 按后到者整体改号改用 r170。实测首空号：全仓已占 r148..r169（r166=S17能量方程、r167/r168
         属并行线），r170 为首空号。
  【靶】三份文档：
    (1) S17/04_理论推导/核心公式集/24-时空与物理常数归一化方程/v1/
        物理理论公式归一化：从微观到宇观的全尺度统一（严谨修订版）.md（662 行）
    (2) 同目录/G和ε0的关系/G和ε0最底层关系的全维求导证明验证.md（138 行）
    (3) S15/04_理论推导/常数几何化与统一母方程.md（127 行，本身含诚实评级）
  【问题】用户问「总结分析所有物理常数（c,G,ħ,e,ε₀,μ₀,k_B,Λ,H₀,α,m_e）的
    本质本源？第一性原理求导证明验证精算出来」。本卷判：
    (i)   这些常数的「导出」是独立预言，还是用 CODATA 代入后反推（循环）？
    (ii)  同一常数的多版本公式是否互斥？
    (iii) 量纲是否合法？数值断言是否成立？
    (iv)  统一母方程的系数方向是否自洽？

01. 机读手段
  纯标准库；量纲五元组 (M,L,T,Q,Θ)（含温度量纲，因靶把 k_B 标错）；
  循环检测（输入=输出残差机器零 + 真正独立关系负对照）；
  多版本互斥（同一 G 五个公式数值对拍）；数值断言复核；母方程系数双向量纲检查。

02. 红线
  数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；靶自承优先（不把「没做」当发现）。
"""

import io
import json
import math
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# CODATA 2018 / SI
# ============================================================
C = 2.99792458e8
G_N = 6.67430e-11
H_P = 6.62607015e-34
HBAR = 1.054571817e-34
E_CHG = 1.602176634e-19
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
K_B = 1.380649e-23
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
ALPHA = 7.2973525693e-3
LAMBDA_E = H_P / (M_E * C)
R_E = LAMBDA_E / (2.0 * math.pi)
L_P = math.sqrt(HBAR * G_N / C ** 3)

# ============================================================
# 路径
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r170_物理常数本质本源_第一性原理求导证明验证精算_2026-10-24"

# ============================================================
# 登记器
# ============================================================
ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


def rel(x, y):
    m = max(abs(x), abs(y))
    if m == 0.0:
        return 0.0
    return abs(x - y) / m


# ============================================================
# 量纲五元组 (M,L,T,Q,Θ)
# ============================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


D_M = (1, 0, 0, 0, 0)
D_L = (0, 1, 0, 0, 0)
D_T = (0, 0, 1, 0, 0)
D_Q = (0, 0, 0, 1, 0)
D_TH = (0, 0, 0, 0, 1)
D_V = ddiv(D_L, D_T)
D_E = (1, 2, -2, 0, 0)
D_F = (1, 1, -2, 0, 0)
D_EDENS = (1, -1, -2, 0, 0)
D_KB = (1, 2, -2, 0, -1)
D_DENS = (1, -3, 0, 0, 0)
D_PRESS = (1, -1, -2, 0, 0)
D_G = (-1, 3, -2, 0, 0)
D_E2 = (1, 3, -2, 0, 0)
D_OMEGA = (0, 0, -1, 0, 0)
D_INV_L = (0, -1, 0, 0, 0)


def dim_check():
    return (dmul(D_M, (0, 1, -2, 0, 0)) == D_F
            and dmul(D_M, dpow(D_V, 2)) == D_E
            and ddiv(D_E, D_EDENS) == (0, 3, 0, 0, 0)
            and dpow(D_L, -1) == (0, -1, 0, 0, 0))


D_HBAR = (1, 2, -1, 0, 0)


# ============================================================
# A 组 · 循环性检测：输入即输出
#   靶：ρ = ħ/(mc)（螺旋参数定义），再用 m = ħ/(ρc)「导出」m。
#   代入即恒等 ⇒ 残差机器零；且 {ρ=ħ/(mc), ħ=mcρ} 是同一式 ⇒ 秩 1。
# ============================================================
def group_a():
    rho = HBAR / (M_E * C)          # ρ 由 CODATA 的 m_e、ħ、c 定出
    m_back = HBAR / (rho * C)       # m = ħ/(ρc) 反解
    res_m = rel(m_back, M_E)
    hbar_back = M_E * C * rho       # ħ = mcρ 反解
    res_h = rel(hbar_back, HBAR)
    # 秩：ρ=ħ/(mc) 与 ħ=mcρ 在对数空间是同一线性方程 ⇒ 秩 1，3 量中 2 自由
    return {"rho": rho, "m_back": m_back, "res_m": res_m,
            "hbar_back": hbar_back, "res_h": res_h,
            "rank": 1, "free": 2}


# ============================================================
# B 组 · 同一 G 的五版本公式（S15 §5 a–e）互斥
#   κ_P = τ_P = 1/l_P（标准读法：κ,τ 为 m⁻¹）
#   量纲回归：(M,L,T,Q,Θ)，G 应为 (-1,3,-2,0,0)
# ============================================================
def group_b():
    kp = 1.0 / L_P
    tp = 1.0 / L_P
    ga = C ** 3 / (2.0 * HBAR * (kp ** 2 + tp ** 2))
    gb = 2.0 * C ** 3 * tp / kp ** 2
    gc = C ** 3 * tp ** 2 / (2.0 * HBAR * kp ** 2)
    gd = 8.0 * math.pi * C ** 3 * tp / (3.0 * kp ** 2)
    ge = ALPHA ** 2 * MU0
    rows = [
        ("a", "c^3/(2h(κP²+τP²))", ga,
         ddiv(dpow(D_V, 3), dmul(D_HBAR, dpow(D_INV_L, 2)))),
        ("b", "2c^3τP/κP²", gb,
         ddiv(dmul(dpow(D_V, 3), D_INV_L), dpow(D_INV_L, 2))),
        ("c", "c^3τP²/(2hκP²)", gc,
         ddiv(dmul(dpow(D_V, 3), dpow(D_INV_L, 2)),
              dmul(D_HBAR, dpow(D_INV_L, 2)))),
        ("d", "8πc^3τP/(3κP²)", gd,
         ddiv(dmul(dpow(D_V, 3), D_INV_L), dpow(D_INV_L, 2))),
        ("e", "α²μ0", ge, (1, 1, 0, -2, 0)),
    ]
    out = []
    for iid, f, val, dim in rows:
        out.append({"id": iid, "formula": f, "G": val,
                    "ratio": val / G_N, "dim": dim, "dim_ok": (dim == D_G)})
    spread = max(r["G"] for r in out) / min(r["G"] for r in out)
    closest = min(out, key=lambda r: abs(math.log(abs(r["ratio"]))))
    return {"rows": out, "spread": spread,
            "n_dim_ok": sum(1 for r in out if r["dim_ok"]),
            "closest": closest}


# ============================================================
# C 组 · 数值断言复核（文件 1 §8）
#   m_e = c²r_e/G（r_e=λ_e/2π）声称 ≈9.112e-31（0.03%）
#   e = √(4πε₀Gm²) 声称 ≈1.601e-19 C（0.06%）
# ============================================================
def group_c():
    m_claim = C ** 2 * R_E / G_N
    m_doc = 9.112e-31
    e_claim = math.sqrt(4.0 * math.pi * EPS0 * G_N * M_E ** 2)
    e_doc = 1.601e-19
    r_s = 2.0 * G_N * M_E / C ** 2          # 史瓦西半径
    m_circ = C ** 2 * (r_s / 2.0) / G_N     # 若 r=Rs/2 ⇒ 回到 m（循环）
    return {"m_claim": m_claim, "m_doc": m_doc, "m_ratio": m_claim / m_doc,
            "e_claim": e_claim, "e_doc": e_doc, "e_ratio": e_claim / e_doc,
            "m_circ": m_circ, "m_circ_res": rel(m_circ, M_E)}


# ============================================================
# D 组 · 量纲审计（6 项，逐项给出实测维与应为维）
# ============================================================
def group_d():
    rows = [
        ("k_B = hν/T（T 取周期/时间）",
         ddiv(dmul(D_HBAR, D_OMEGA), D_T), D_KB),
        ("ρ_vac = c⁷/(4πG²h)",
         ddiv(dpow(D_V, 7), dmul(dpow(D_G, 2), D_HBAR)), D_DENS),
        ("双隐量 mω²rc²/(Ghν)",
         ddiv(dmul(dmul(dmul(D_M, dpow(D_OMEGA, 2)), D_L), dpow(D_V, 2)),
              dmul(dmul(D_G, D_HBAR), D_OMEGA)), (0, 0, 0, 0, 0)),
        ("母方程系数 c⁴/8πG × 力密度",
         dmul(ddiv(dpow(D_V, 4), D_G), D_EDENS), (0, -2, 0, 0, 0)),
        ("母方程系数 8πG/c⁴ × 力密度",
         dmul(ddiv(D_G, dpow(D_V, 4)), D_EDENS), (0, -2, 0, 0, 0)),
        ("文件2 G = e²/(4πε₀ω³r⁵c)",
         ddiv(D_E2, dmul(dmul(dpow(D_OMEGA, 3), dpow(D_L, 5)), D_V)), D_G),
    ]
    return [{"name": n, "dim": d, "expect": x, "ok": (d == x)}
            for n, d, x in rows]


# ============================================================
# E 组 · 归一化关联式 4π²r³c²/(GT²hν)=1 是同义反复
#   代 r=Gm/c²、T=2πr/c、hν=mc² ⇒ 对任意 m 恒为 1
# ============================================================
def group_e():
    out = []
    for m in (1.0, 1.0e-3, 1.0e3):
        r = G_N * m / C ** 2
        T = 2.0 * math.pi * r / C
        nu = m * C ** 2 / H_P          # 由 hν = mc²（文件1 式5）
        val = 4.0 * math.pi ** 2 * r ** 3 * C ** 2 / (G_N * T ** 2 * H_P * nu)
        out.append({"m": m, "val": val, "res": rel(val, 1.0)})
    return out


# ============================================================
# F 组 · 跨文件矛盾：F_e/F_g
#   文件1 §6.6 称 =1；文件2 L54 称 ≈4.17e42
# ============================================================
def group_f():
    fem = E_CHG ** 2 / (4.0 * math.pi * EPS0 * G_N * M_E ** 2)
    return {"fem": fem, "doc1": 1.0, "doc2": 4.17e42,
            "ratio_to_one": fem / 1.0, "ratio_doc2": rel(fem, 4.17e42)}


# ============================================================
# 控制组（6 项）
# ============================================================
def run_controls(a, b, c, d, e, f):
    control("C1", "量纲工具自检（ma=F / m v²=2E / E/能量密度=L³ / 1/L=L⁻¹）",
            "dim_check", "True", dim_check())

    a_e = 1.495978707e11
    m_s = 1.98847e30
    t_e = 3.15581450e7
    res_kep = rel(t_e ** 2, 4.0 * math.pi ** 2 * a_e ** 3 / (G_N * m_s))
    control("C2", "循环检测：正(ρ=ħ/mc ⇒ m 反解残差 0) 负(开普勒地球残差非零)",
            "%.2e / %.2e" % (a["res_m"], res_kep), "0 / >0",
            a["res_m"] < 1e-15 and res_kep > 0.0)

    control("C3", "多版本检测：五版本 spread>1e60 且 a 版=G/4",
            "spread=%.2e a/G=%.4f" % (b["spread"], b["rows"][0]["ratio"]),
            ">1e60 / 0.25",
            b["spread"] > 1e60 and abs(b["rows"][0]["ratio"] - 0.25) < 0.01)

    control("C4", "量纲检测：G 维合法 与 α²μ₀ 维非法同时成立",
            "G=%s e=%s" % (D_G, b["rows"][4]["dim"]), "(-1,3,-2,0,0) / ≠",
            D_G == (-1, 3, -2, 0, 0) and b["rows"][4]["dim"] != D_G)

    ratio_pm = M_P / M_E
    control("C5", "数值复核：m_p/m_e=1836.15 且 文件1 的 m 偏离>1e40",
            "%.3f / %.1e" % (ratio_pm, c["m_ratio"]), "1836.15 / >1e40",
            abs(ratio_pm - 1836.152673) < 0.01 and c["m_ratio"] > 1e40)

    control("C6", "归一化同义反复：任意 m 关联式恒=1",
            " / ".join("%.1e" % x["res"] for x in e), "全 0",
            all(x["res"] < 1e-12 for x in e))


# ============================================================
# 守卫（8 项；任一失控 ⇒ 退出码 2）
# ============================================================
def run_guards(a, b, c, d, e, f):
    guard("G1-量纲工具自检", dim_check(), "dim_check()")

    g2 = (a["res_m"] < 1e-15 and a["res_h"] < 1e-15 and a["rank"] == 1)
    guard("G2-循环：m/ħ 反解残差机器零、秩1", g2,
          "res_m=%.1e res_h=%.1e rank=%d" % (a["res_m"], a["res_h"], a["rank"]))

    g3 = (b["spread"] > 1e60 and b["n_dim_ok"] == 1 and not b["closest"]["dim_ok"])
    guard("G3-G 五版本：spread>1e60、仅1个维合法、最近者维非法", g3,
          "spread=%.1e n_dim_ok=%d closest=%s(dim_ok=%s)"
          % (b["spread"], b["n_dim_ok"], b["closest"]["id"], b["closest"]["dim_ok"]))

    g4 = (c["m_ratio"] > 1e40 and abs(math.log10(c["e_ratio"])) > 20)
    guard("G4-文件1数值断言错误：m 偏离>1e40、e 偏离>1e20", g4,
          "m_ratio=%.1e e_ratio=%.1e" % (c["m_ratio"], c["e_ratio"]))

    n_illegal = sum(1 for r in d if not r["ok"])
    master_ok = (d[3]["ok"] is False and d[4]["ok"] is True)
    guard("G5-量纲审计：≥4/6 项非法，母方程 c⁴/8πG 非法而 8πG/c⁴ 合法",
          n_illegal >= 4 and master_ok, "illegal=%d/6" % n_illegal)

    guard("G6-F_e/F_g 跨文件矛盾：真值 4.17e42 ≠ 文件1 的 1",
          f["ratio_to_one"] > 1e40, "value=%.1e" % f["fem"])

    guard("G7-归一化关联式：3 个不同 m 全部恒=1（同义反复）",
          all(x["res"] < 1e-12 for x in e), "res_max=%.1e" % max(x["res"] for x in e))

    guard("G8-控制组全部通过", all(x["ok"] for x in CONTROLS),
          "%d/%d" % (sum(1 for x in CONTROLS if x["ok"]), len(CONTROLS)))


# ============================================================
# 条目登记
# ============================================================
def register_items(a, b, c, d, e, f):
    add("A1", "质量与 ħ 的「导出」是循环（输入即输出）", "INFO",
        "ρ=ħ/(mc) 由 CODATA 定出后，m=ħ/(ρc) 反解残差 %.1e（机器零）、ħ=mcρ 残差 %.1e；"
        "两式在对数空间是同一方程（秩 1）⇒ 3 个量中 2 自由 ⇒ 不能预言任一新常数。"
        "按本线纪律：代数恒等变换记 INFO，不记 PASS（PASS ≠ 有内容）。"
        % (a["res_m"], a["res_h"]),
        res_m=a["res_m"], res_h=a["res_h"])

    add("A2", "「溯源归一化关联式」是同义反复", "FAIL",
        "4π²r³c²/(GT²hν)=1 经 r=Gm/c²、T=2πr/c、hν=mc² 代换后，对任意 m（测试 1、1e-3、1e3 kg）"
        "均恒为 1（残差 %.1e）⇒ 只是把史瓦西半径与 hν=mc² 重排，零预言内容。"
        % max(x["res"] for x in e),
        res_max=max(x["res"] for x in e))

    add("B1", "同一 G 的五个公式互斥（S15 §5 a–e）", "FAIL",
        "五版本比值（相对 CODATA G）: a=%.4f, b=%.3e, c=%.2e, d=%.2e, e=%.4f；"
        "max/min=%.2e ⇒ 同一物理量五个互不等价的「第一性」公式。"
        % (b["rows"][0]["ratio"], b["rows"][1]["ratio"], b["rows"][2]["ratio"],
           b["rows"][3]["ratio"], b["rows"][4]["ratio"], b["spread"]),
        spread=b["spread"])

    add("B2", "G 的两难：唯一数值接近的版本量纲非法", "FAIL",
        "五版本中仅 a 维合法（给出 G/4，差 4 倍）；b/c/d 维非法；e（α²μ₀）数值=%.4f×G（0.27%%）"
        "但维=%s ≠ G ⇒ 「最像的」恰是被来源自承量纲非法的那条。"
        % (b["rows"][4]["ratio"], b["rows"][4]["dim"]),
        closest=b["closest"]["id"])

    add("C1", "文件1 §8 质量数值断言错误（约 44 个量级）", "FAIL",
        "m=c²r_e/G（r_e=λ_e/2π=%s）实算 %.2e kg，文档写 9.112e-31 kg，比值 %.1e；"
        "「0.03%% 误差」不成立；若改 r=Rs/2 则回到 m（残差 %.1e）= 循环。"
        % (fs(R_E), c["m_claim"], c["m_ratio"], c["m_circ_res"]),
        m_ratio=c["m_ratio"])

    add("C2", "文件1 §8 电荷数值断言错误（约 21 个量级）", "FAIL",
        "e=√(4πε₀Gm²) 实算 %.2e C，文档写 1.601e-19 C，比值 %.1e ⇒「0.06%% 误差」不成立。"
        % (c["e_claim"], c["e_ratio"]),
        e_ratio=c["e_ratio"])

    add("D1", "k_B = hν/T 量纲非法（T 兼作周期与温度）", "FAIL",
        "实测维 %s，应为 %s ⇒ hν 是能量、除以周期(时间)得功率量纲，非 k_B；"
        "文档同一符号 T 既作周期又作温度。" % (d[0]["dim"], d[0]["expect"]))

    add("D2", "ρ_vac = c⁷/(4πG²h) 量纲非法且数值差 138 量级", "FAIL",
        "实测维 %s（压强），应为 %s（密度）；数值 ≈%.1e，与 3H²c²/(8πG)~1e-26 相差 ~138 量级。"
        % (d[1]["dim"], d[1]["expect"], C ** 7 / (4 * math.pi * G_N ** 2 * H_P)))

    add("D3", "统一母方程系数方向倒置（c⁴/8πG 应为 8πG/c⁴）", "FAIL",
        "c⁴/8πG×力密度 实测维 %s ≠ L⁻²；8πG/c⁴×力密度 = %s ✓ ⇒ 左端曲率、右端须 [L⁻²]。"
        % (d[3]["dim"], d[4]["dim"]))

    add("D4", "双隐量恒等式 mω²rc²/(Ghν) 量纲非法", "FAIL",
        "实测维 %s ≠ 无量纲 ⇒ 文中标注「量纲:1，闭合」不成立。" % (d[2]["dim"],))

    add("E1", "F_e/F_g 跨文件矛盾（=1 vs 4.17e42）", "FAIL",
        "e²/(4πε₀Gm²) 实算 %.4e；文件1 称 =1、文件2 称 ≈4.17e42 ⇒ 同一理论内互相否证；"
        "且该比值随粒子质量变，非普适常数。" % f["fem"],
        fem=f["fem"])

    add("F1", "质量式作为「代数恒等变换」本身自洽", "PASS",
        "m=ħ/(ρc) 在 ρ=ħ/(mc) 下逐位复原 m（残差 %.1e）⇒ 作为代数重排正确；"
        "问题不在算术，在把重排当作「第一性导出」。" % a["res_m"])

    add("F2", "靶自承核对", "INFO",
        "S15 文档自承「用 CODATA 代入螺旋参数后反推同一常数，零误差是重参数化而非独立预言」；"
        "本卷不得把「循环」记为本卷新发现，只判其结构性后果。")

    add("G1", "本卷判域边界", "BOUNDARY",
        "只判三份文档明确给出的常数式（c,G,ħ,e,ε₀,μ₀,k_B,Λ,H₀,α,m_e）；"
        "S17 其余 22 式与其他卷的常数声明未纳入。")


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 78)
    print(" TUFT-r170｜所有物理常数的本质本源 —— 第一性原理求导证明验证精算")
    print(" 2026-10-24 ｜ 纯标准库 ｜ 量纲五元组 (M,L,T,Q,Θ)")
    print("=" * 78)
    a = group_a()
    b = group_b()
    c = group_c()
    d = group_d()
    e = group_e()
    f = group_f()

    print("\n[A] 循环性：ρ=%.6e；m 反解残差=%.2e；ħ 反解残差=%.2e；秩=%d"
          % (a["rho"], a["res_m"], a["res_h"], a["rank"]))
    print("[B] G 五版本（比值 vs CODATA）:")
    for r in b["rows"]:
        print("    %s %-24s G=%.6e  G/G_N=%.4e  dim_ok=%s"
              % (r["id"], r["formula"], r["G"], r["ratio"], r["dim_ok"]))
    print("    spread=%.2e  n_dim_ok=%d  最近者=%s(dim_ok=%s)"
          % (b["spread"], b["n_dim_ok"], b["closest"]["id"], b["closest"]["dim_ok"]))
    print("[C] 数值断言：m实算=%.2e(文档9.112e-31, 比%.1e)；e实算=%.2e(文档1.601e-19, 比%.1e)"
          % (c["m_claim"], c["m_ratio"], c["e_claim"], c["e_ratio"]))
    print("[D] 量纲审计：")
    for r in d:
        print("    %-28s 实测%s 应为%s  %s"
              % (r["name"], r["dim"], r["expect"], "OK" if r["ok"] else "BAD"))
    print("[E] 归一化关联式：m=1/1e-3/1e3 残差=%s"
          % " / ".join("%.1e" % x["res"] for x in e))
    print("[F] F_e/F_g 实算=%.4e（文件1称1，文件2称4.17e42）" % f["fem"])

    register_items(a, b, c, d, e, f)
    run_controls(a, b, c, d, e, f)
    run_guards(a, b, c, d, e, f)

    return {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f}


# ============================================================
# 产物：console / 判定册 md / 数据 md / json / report txt
# ============================================================
def report_and_write(R):
    a, b, c, d, e, f = R["a"], R["b"], R["c"], R["d"], R["e"], R["f"]
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    verdict = ("CONSTANT-ORIGIN-IS-REPARAMETERIZATION-G-MULTI-VERSION-"
               "AND-DIMENSION-INVALID")
    allok = all(x["ok"] for x in CONTROLS)
    gallok = all(x["ok"] for x in GUARDS)

    L = []
    w = L.append
    w("=" * 78)
    w(" TUFT-r170｜所有物理常数的本质本源 —— 第一性原理求导证明验证精算")
    w("=" * 78)
    w("")
    w("[A] 循环性：ρ=%.6e  m 反解残差=%.2e  ħ 反解残差=%.2e  秩=%d"
      % (a["rho"], a["res_m"], a["res_h"], a["rank"]))
    w("")
    w("[B] G 五版本（比值 vs CODATA G）:")
    for r in b["rows"]:
        w("   %s %-22s G=%.6e  G/G_N=%.4e  dim=%s %s"
          % (r["id"], r["formula"], r["G"], r["ratio"], r["dim"],
             "OK" if r["dim_ok"] else "BAD"))
    w("   spread=%.2e  n_dim_ok=%d  最近者=%s(dim_ok=%s)"
      % (b["spread"], b["n_dim_ok"], b["closest"]["id"], b["closest"]["dim_ok"]))
    w("")
    w("[C] 数值断言：m实算=%.2e（文档9.112e-31，比%.1e）"
      % (c["m_claim"], c["m_ratio"]))
    w("               e实算=%.2e（文档1.601e-19，比%.1e）"
      % (c["e_claim"], c["e_ratio"]))
    w("")
    w("[D] 量纲审计：")
    for r in d:
        w("   %-30s 实测%s 应为%s %s"
          % (r["name"], r["dim"], r["expect"], "OK" if r["ok"] else "BAD"))
    w("")
    w("[E] 归一化关联式：m=1/1e-3/1e3 残差=%s"
      % " / ".join("%.1e" % x["res"] for x in e))
    w("[F] F_e/F_g=%.4e（文件1称1，文件2称4.17e42）" % f["fem"])
    w("")
    w("[控制组]")
    for x in CONTROLS:
        w("   %s %-52s %-26s %s"
          % ("OK " if x["ok"] else "BAD", x["desc"], x["value"], x["expect"]))
    w("")
    w("[守卫]")
    for x in GUARDS:
        w("   %s %s  %s" % ("OK " if x["ok"] else "BAD", x["name"], x["detail"]))
    w("")
    w("[条目] %s" % cnt)
    w("[verdict] %s" % verdict)
    w("[控制组] %d/%d   [守卫] %d/%d"
      % (sum(1 for x in CONTROLS if x["ok"]), len(CONTROLS),
         sum(1 for x in GUARDS if x["ok"]), len(GUARDS)))
    report = "\n".join(L)

    # ---------- 判定册 ----------
    m = []
    bb = m.append
    bb("# 判定册 TUFT-r170｜所有物理常数的本质本源 —— 第一性原理求导证明验证精算")
    bb("")
    bb("- 编号：TUFT-r170")
    bb("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    bb("- 引擎：`源码/%s.py`" % STEM)
    bb("- 控制组：%d/%d ｜ 守卫：%d/%d"
       % (sum(1 for x in CONTROLS if x["ok"]), len(CONTROLS),
          sum(1 for x in GUARDS if x["ok"]), len(GUARDS)))
    bb("- 条目统计：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())))
    bb("")
    bb("## 00. 分工声明")
    bb("")
    bb("| 卷 | 层 | 判的是什么 |")
    bb("|----|----|-----------|")
    bb("| r160–r164 | 公设层（S17 四项诠释 / 电荷 / 时空 / 质量 / 本源） | 逐条公设的求导与验证 |")
    bb("| r166 | 能量方程求导层 | E=mc²√(1−β²) 的推导与验证脚本 |")
    bb("| **r169** | **常数本源层** | **所有物理常数的「第一性原理导出」是否成立** |")
    bb("")
    bb("## 01. 判词")
    bb("")
    bb("`%s`" % verdict)
    bb("")
    bb("## 02. 核心结论")
    bb("")
    bb("### 2.1 循环性（A1/A2）")
    bb("")
    bb("- `ρ=ħ/(mc)` 在代数上把 m、ħ、c 三者绑死；用 `m=ħ/(ρc)` 反解残差 **%.1e**"
       "（机器零），`ħ=mcρ` 残差 **%.1e** ⇒ 两式秩 1，3 量中 2 自由；"
       % (a["res_m"], a["res_h"]))
    bb("- 「溯源归一化关联式」`4π²r³c²/(GT²hν)=1` 对任意 m（1、1e-3、1e3 kg）**恒为 1**"
       "（残差 %.1e）⇒ 只是史瓦西半径与 `hν=mc²` 的重排，零预言内容。" % max(x["res"] for x in e))
    bb("")
    bb("### 2.2 同一 G 的五版本互斥（B1/B2）")
    bb("")
    bb("| 版本 | 公式 | G/G_N | 维合法 |")
    bb("|---|---|---|---|")
    for r in b["rows"]:
        bb("| %s | `%s` | %.4e | %s |" % (r["id"], r["formula"], r["ratio"],
                                          "✓" if r["dim_ok"] else "✗"))
    bb("")
    bb("- 五版本 max/min = **%.2e**；仅 **a** 维合法且给出 **G/4**（差 4 倍）；" % b["spread"])
    bb("- **e（α²μ₀）数值 = %.4f×G（0.27%%）但量纲非法** ⇒ 「最像的」恰是来源自承"
       "量纲非法（废弃）的那条 ⇒ 两难：维合法则数值错，数值对则维非法。" % b["rows"][4]["ratio"])
    bb("")
    bb("### 2.3 数值断言复核（C1/C2）")
    bb("")
    bb("- `m=c²r_e/G`（r_e=λ_e/2π=%.3e m）实算 **%.2e kg**，文档写 9.112e-31 kg"
       "（比 **%.1e**，约 44 量级）；若改 r=Rs/2 则回到 m（残差 %.1e）= 循环；"
       % (R_E, c["m_claim"], c["m_ratio"], c["m_circ_res"]))
    bb("- `e=√(4πε₀Gm²)` 实算 **%.2e C**，文档写 1.601e-19 C（比 **%.1e**，约 21 量级）"
       % (c["e_claim"], c["e_ratio"]))
    bb("")
    bb("### 2.4 量纲审计（D1–D4）")
    bb("")
    bb("| 项 | 实测维 | 应为维 | 判定 |")
    bb("|---|---|---|---|")
    for r in d:
        bb("| %s | %s | %s | %s |" % (r["name"], r["dim"], r["expect"],
                                      "OK" if r["ok"] else "非法"))
    bb("")
    bb("### 2.5 跨文件矛盾（E1）")
    bb("")
    bb("- `F_e/F_g = e²/(4πε₀Gm²)` 实算 **%.4e**；文件1 称 `=1`、文件2 称 `≈4.17e42`"
       " ⇒ 同一理论内互相否证；且该比值随粒子质量变，非普适常数。" % f["fem"])
    bb("")
    bb("### 2.6 诚实 PASS（F1）")
    bb("")
    bb("- 质量式 `m=ħ/(ρc)` 在 `ρ=ħ/(mc)` 下逐位复原 m（残差 %.1e）⇒ 作为**代数重排**正确；"
       "问题不在算术，在把重排当作「第一性导出」。" % a["res_m"])
    bb("")
    bb("## 03. 修复定价")
    bb("")
    bb("| 动作 | 宣称域内成立 | 代价 |")
    bb("|---|---|---|")
    bb("| 保留「唯一独立常数为 c」的几何重排 | 否 | 全部常数式循环 ⇒ 零预言 |")
    bb("| 补齐 G 的独立导出 | 否 | 五版本互斥，无版本维合法且数值对 |")
    bb("| 修量纲并改母方程系数为 8πG/c⁴ | 是 | 仍只是 GR 重写，无新预言 |")
    bb("")
    bb("- 宣称域内成立 **1** 个、**零代价 0** 个 ⇒ 修复可行 ≠ 修复后仍有内容。")
    bb("")
    bb("## 04. 靶自承与防过度指控")
    bb("")
    bb("- S15 文档自承「用 CODATA 代入螺旋参数后反推，零误差是重参数化而非独立预言」⇒"
       "「循环」不是本卷新发现，本卷只判其结构性后果（零预言、多版本互斥、量纲非法）。")
    bb("- 文件1 自称「所有公式误差<1%%」与 §8 实算不符（差 44/22 量级），此为本卷机器发现。")
    bb("")
    bb("## 05. 未闭合项与红线")
    bb("")
    bb("- 未闭合：① 只判三份文档明确给出的常数式；② κ、τ 的数值来源（螺旋参数）未独立审计；"
       "③ Λ/H₀ 的观测闭合（C0012/C0013）未单独精算；④ 修复空间只枚举 3 个动作。")
    bb("- 红线：数学自洽 ≠ 实验证实；恒等式成立 ≠ 有新内容；靶自承优先；"
       "降级一条旧结论 ≠ 该方向被否证。")
    bb("")

    # ---------- 落盘 ----------
    os.makedirs(OUT, exist_ok=True)
    jp = os.path.join(OUT, STEM + ".json")
    dp = os.path.join(OUT, STEM + ".md")
    vp = os.path.join(OUT, "判定_" + STEM + ".md")
    rp = os.path.join(OUT, STEM + "_report.txt")

    key_numbers = {
        "rho_e": a["rho"], "m_back_res": a["res_m"], "hbar_back_res": a["res_h"],
        "G_a_ratio": b["rows"][0]["ratio"], "G_b_ratio": b["rows"][1]["ratio"],
        "G_c_ratio": b["rows"][2]["ratio"], "G_d_ratio": b["rows"][3]["ratio"],
        "G_e_ratio": b["rows"][4]["ratio"], "G_spread": b["spread"],
        "n_dim_ok_G": b["n_dim_ok"], "closest_G": b["closest"]["id"],
        "m_claim": c["m_claim"], "m_ratio": c["m_ratio"],
        "e_claim": c["e_claim"], "e_ratio": c["e_ratio"],
        "m_circ_res": c["m_circ_res"],
        "dim_illegal_count": sum(1 for r in d if not r["ok"]),
        "normalization_res_max": max(x["res"] for x in e),
        "fem": f["fem"],
    }
    payload = {
        "volume": "TUFT-r170",
        "title": "所有物理常数的本质本源 —— 第一性原理求导证明验证精算",
        "date": "2026-10-24",
        "engine": "源码/" + STEM + ".py",
        "stats": cnt,
        "verdict": verdict,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "not_closed": [
            "只判三份文档明确给出的常数式（c,G,ħ,e,ε₀,μ₀,k_B,Λ,H₀,α,m_e）。",
            "κ、τ 的数值来源（螺旋参数）未独立审计。",
            "Λ/H₀ 的观测闭合（C0012/C0013）未单独精算。",
            "修复空间只枚举 3 个低阶动作。",
        ],
        "redline": [
            "数学自洽 ≠ 实验证实。",
            "恒等式成立 ≠ 有新内容。",
            "靶自承优先：不把『没做』当发现。",
            "降级一条旧结论 ≠ 该方向被否证。",
        ],
    }
    with io.open(jp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)
    with io.open(vp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(m))
    with io.open(rp, "w", encoding="utf-8") as fh:
        fh.write(report)

    dm = ["# 数据 TUFT-r170｜物理常数本质本源关键读数", "",
          "- 判词：`%s`" % verdict,
          "- 条目：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())),
          "- 控制组 %d/%d ｜ 守卫 %d/%d"
          % (sum(1 for x in CONTROLS if x["ok"]), len(CONTROLS),
             sum(1 for x in GUARDS if x["ok"]), len(GUARDS)), "",
          "| 读数 | 值 |", "|---|---|"]
    for kk, vv in key_numbers.items():
        dm.append("| %s | %s |" % (kk, vv))
    with io.open(dp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(dm))

    print(report)
    print("")
    for p in (jp, dp, vp, rp):
        print("[产物] " + os.path.basename(p))
    print("[控制组] %d/%d  [守卫] %d/%d"
          % (sum(1 for x in CONTROLS if x["ok"]), len(CONTROLS),
             sum(1 for x in GUARDS if x["ok"]), len(GUARDS)))
    print("[退出码] %d" % (0 if (allok and gallok) else 2))
    return 0 if (allok and gallok) else 2


if __name__ == "__main__":
    sys.exit(report_and_write(main()))
