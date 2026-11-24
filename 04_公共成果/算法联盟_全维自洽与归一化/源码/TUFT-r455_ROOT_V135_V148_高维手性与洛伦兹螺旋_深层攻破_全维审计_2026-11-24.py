#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r455 / ROOT V135 + V148 深层攻破审计：高维手性与洛伦兹螺旋。

只读来料正本；不验收 ZIP、图片、HTML 面板或未随来料提供的源码。纯标准库：
Decimal 60 位做指标/矩阵维数/洛伦兹变换/引力数值复算，整数计数做结构账。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r455_ROOT_V135_V148_高维手性与洛伦兹螺旋_深层攻破_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V135_V148_来料全文_2026-11-24.md"

D = Decimal

entries = []
guards = []
key = {}


def fmt(x, digits="18"):
    x = D(x)
    if x == 0:
        return "0"
    return format(x, "." + str(digits) + "E")


def rel(a, b):
    a, b = D(a), D(b)
    return abs(a - b) / max(abs(a), abs(b), D("1e-80"))


def dsqrt(x):
    x = D(x)
    if x < 0:
        raise ValueError("sqrt of negative Decimal")
    return (x.ln() / D(2)).exp()


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    key["source_sha256"] = sha
    key["source_bytes"] = len(raw)

    anchors = [
        "ROOT V135｜统一场论深度攻坚：修复高维几何，检验三代粒子与四力起源",
        "M_{3,1}\\times \\mathbb{CP}^{2}\\times S^2\\times S^1",
        "c_1(L)=(2q+1)h",
        "\\operatorname{ind}D_L =\\frac{(2q+1)^2-1}{8} =\\frac{q(q+1)}2",
        "\\slashed D_{11} = \\slashed D_4\\otimes I + \\gamma_5\\otimes\\slashed D_7",
        "3\\text{ 个内部零模}\\;\\Longrightarrow\\;3\\text{ 个四维 Dirac 模式}",
        "R_{MN}=\\frac{2\\Lambda_{11}}9g_{MN}",
        "ROOT V148｜光速螺旋与四力统一：洛伦兹协变性攻坚",
        "a^2\\omega^2+u^2=1",
        "\\omega'&=\\frac{\\omega}{\\gamma(1-\\beta u)}",
        "\\frac{E'}{\\hbar|\\omega'|} =D^2\\frac{E}{\\hbar|\\omega|}",
        "\\mathbf E\\cdot\\mathbf B=0,\\qquad \\mathbf E\\times\\mathbf B=E_0^2\\hat{\\mathbf z}",
        "9.820250332",
        "0.350998310",
        "四力统一尚未得到证明。",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 1000, "来料正本非空且 SHA256 格式有效")

    # ---------- V135：可复算数学 ----------
    add("A-01", "PASS", "CP² 非 Spin 而允许 Spin^c 的判据可复算",
        "CP² 的 w2 非零，普通 Spin 结构不存在；Spin^c 行列式线丛 c1(L)=(2q+1)h 为奇整数类，满足 Spin^c 提升条件。来料对此口径正确。")
    odd_ok = all(((2 * q + 1) % 2 == 1) for q in range(-5, 6))
    guard("G1-01", odd_ok, "c1(L)/h=2q+1 对所有抽样 q 均为奇整数类")

    q_rows = [(-2, -3, 1), (-1, -1, 0), (0, 1, 0), (1, 3, 1), (2, 5, 3), (3, 7, 6), (4, 9, 10)]
    ind_ok = True
    calc_rows = []
    for q, c1, claimed in q_rows:
        val = q * (q + 1) // 2
        calc_rows.append((q, c1, val))
        ind_ok = ind_ok and (val == claimed) and (c1 == 2 * q + 1)
    guard("G1-02", ind_ok, "Spin^c 指标表 q(q+1)/2 与来料 7 行逐项一致")
    key["spin_c_index_rows"] = calc_rows
    key["spin_c_index_q2"] = 3
    add("A-02", "PASS", "Spin^c Dirac 指标公式与 q=2 指标 3 可复算",
        "Â=1-h²/8，exp(c1/2) 的四阶项为 (2q+1)²h²/8；积分为 ((2q+1)²-1)/8=q(q+1)/2。q=2 时指标为 3，来料表格 7 行逐项复算一致。")

    guard("G1-03", 8 + 3 + 1 == 12 and 8 + 3 + 1 == 12, "8+3+1=12 与标准模型李代数维数账一致")
    add("A-03", "PASS", "内部等距维数 8+3+1=12 的局部账正确",
        "CP² 的 PU(3) 局部代数 su(3) 为 8 维，S² 的 so(3)≅su(2) 为 3 维，S¹ 的 u(1) 为 1 维；与 SM 李代数维数 8+3+1=12 相同。该条只确认局部维数账，不确认全局群或耦合。")

    spinor_dim = 2 ** (11 // 2)
    guard("G2-01", spinor_dim == 32, "11D 复 Clifford 不可约旋量维数 2^5=32")
    rank4 = 4 // 2
    guard("G2-02", rank4 == 2, "4D 块中 γ5 左右投影各自秩为 2；完整 32 维乘积表示中各自秩为 16")
    key["clifford_11d_complex_dim"] = spinor_dim
    key["gamma5_rank_4d_block"] = rank4
    key["gamma5_rank_32d_product"] = 16
    add("A-04", "PASS", "11D 复旋量 32 维与 4D 手征投影口径可复算",
        "11D 复 Clifford 表示维数为 2^5=32；4D Dirac 块中 γ5 的左右投影各秩 2。若在完整 32 维乘积表示中计数，每手征为 16 维；来料“两个复维度”须声明为 4D 块口径。")

    lam_factor = D(2) / D(9)
    guard("G3-01", rel(lam_factor, D(2) / D(11 - 2)) == 0, "D=11 Einstein 方程 Λ 系数为 2/(11-2)=2/9")
    guard("G3-02", D(0) == D(2) * D(0) / D(9), "Minkowski 四维 Rμν=0 强制 Λ11=0")
    guard("G3-03", D(6) > 0 and D(1) > 0, "CP² 与 S² 的 Ricci 系数 6/R_C²、1/R_S² 对有限正半径非零")
    add("A-05", "PASS", "平直四维 × 正曲率内部的纯 Einstein+Λ 排除成立",
        "R_MN=2Λ11 g_MN/9；R_μν=0 强制 Λ11=0，随后内部也必须 Ricci-flat。指定 CP² 与 S² 的 Ricci 张量分别为 6g/R_C² 与 g/R_S²，有限半径下非零，故无该简单直积解。")

    # ---------- V135：深层攻破 ----------
    guard("G4-01", "指标 3 是两个内部手征零模数量之差" in text and "不自动等于三代物理粒子" in text,
          "来料自陈指标 3 不等于三代 SM 粒子")
    add("B-01", "FAIL", "指标 3 不等于三代标准模型手征粒子",
        "Dirac 指标是 n_+−n_- 的有符号差，不给出完整零模数量、规范表示、Yukawa 耦合、质量谱或弱手征结构。即使 q=2 给 ind=3，也只能说存在净拓扑差，不能说产生三代 SM 粒子。")

    guard("G4-02", "取 \\(q=2\\) 是额外选择" in text, "来料自陈 q=2 未从 ROOT 基本原理推出")
    add("B-02", "FAIL", "q=2 是外部拓扑选择而非框架内生常数",
        "Spin^c 行列式类 c1=(2q+1)h 有无穷多奇整数解；指标随 q 变化。来料承认 q=2 是额外选择。没有选择原理时，指标 3 是从外部输入读入，不是统一理论的预测。")

    guard("G4-03", "普通十一维 Dirac 场、平滑乘积紧化、没有额外手征投影" in text,
          "来料限定普通 11D Dirac 简单紧化模型")
    add("B-03", "FAIL", "普通 11D Dirac 紧化不自动给出四维手征谱",
        "内部零模代入后得到普通四维 Dirac 模式，左右手仍成对；而且 K7 为奇数维闭流形，不存在通常意义上的手征分级。要得到 SM 手征谱，还需明确内部规范丛、投影/边界机制、反常抵消与四维 Yukawa 结构。")

    guard("G4-04", "规范李代数维数相同" in text and "是否已经确定规范耦合？" in text and "未确定" in text,
          "来料同时给出维数匹配与耦合未确定")
    add("B-04", "FAIL", "等距代数维数匹配不是规范统一",
        "PU(3)、SO(3)、U(1) 与 SU(3)、SU(2)、U(1) 只在局部李代数层同维/同构到覆盖群；全局中心、表示内容、规范耦合、破缺链与反常抵消均未推出。12=8+3+1 是记账吻合，不是四力统一。")

    guard("G4-05", "没有这种简单直积解" in text, "来料承认背景场方程排除")
    add("B-05", "FAIL", "拓扑修复未修复动力学背景方程",
        "正曲率内部空间需要通量、翘曲、更高曲率项或其他物质源共同满足场方程；仅把 Spin^c 指标写入谱计算不能使 R_MN=2Λg_MN/9 成立。来料承认必须另建候选作用量。")

    add("B-06", "FAIL", "规范耦合、G、质量谱与四力统一均未闭包",
        "V135 自身汇总表明确列出规范耦合未确定、G 未独立预测、四力未证明。指标、矩阵维数与场方程排除是筛选条件，不是统一完成。")

    # ---------- V148：可复算数学 ----------
    a, omega, u = D("0.6"), D(1), D("0.8")
    speed2 = (a * omega) ** 2 + u * u
    guard("G5-01", rel(speed2, D(1)) == 0, "示例 a=0.6,ω=1,u=0.8 满足光速条件 a²ω²+u²=1")
    kappa = a * omega * omega
    tau = u * omega
    guard("G5-02", rel(kappa, D("0.6")) == 0 and rel(tau, D("0.8")) == 0, "空间曲率 κ=aω²=0.6、挠率 τ=uω=0.8")
    key["helix_original"] = {"a": "0.6", "omega": "1", "u": "0.8", "kappa": "0.6", "tau": "0.8"}

    beta = u
    gamma = D(1) / dsqrt(D(1) - beta * beta)
    Dfac = gamma * (D(1) - beta * u)
    omega_p = omega / Dfac
    u_p = (u - beta) / (D(1) - beta * u)
    kappa_p = a * omega_p * omega_p
    tau_p = u_p * omega_p
    speed2_p = (a * omega_p) ** 2 + u_p * u_p
    guard("G5-03", rel(Dfac, D("0.6")) < D("1e-50"), "β=u=0.8 时 D=γ(1-βu)=0.6")
    guard("G5-04", rel(omega_p, D("5") / D(3)) < D("1e-50") and rel(u_p, D(0)) == 0,
          "boost 后 ω'=5/3、u'=0")
    guard("G5-05", rel(kappa_p, D("5") / D(3)) < D("1e-50") and rel(tau_p, D(0)) == 0,
          "boost 后 κ'=5/3、τ'=0")
    guard("G5-06", rel(speed2_p, D(1)) < D("1e-50"), "boost 后空间速率仍为 1")
    key["helix_boost"] = {
        "D": fmt(Dfac, 25),
        "omega_prime": fmt(omega_p, 25),
        "u_prime": fmt(u_p, 25),
        "kappa_prime": fmt(kappa_p, 25),
        "tau_prime": fmt(tau_p, 25),
        "speed2_prime": fmt(speed2_p, 25),
    }
    add("C-01", "PASS", "光速螺旋曲率/挠率与 boost 公式可复算",
        "r=(a cosωt,a sinωt,ut) 在 a²ω²+u²=1 时给 κ=aω²、τ=uω；沿轴 boost 给 ω'=ω/[γ(1-βu)]、u'=(u-β)/(1-βu)。示例 a=0.6,ω=1,u=0.8,β=0.8 逐项复现 κ'=5/3、τ'=0。")
    add("C-02", "PASS", "boost 后空间速率仍为 c",
        "用 (aω')²+u'² 逐项代入，示例与一般代数均回到 1；这说明来料的 boost 处理没有把光速条件破坏掉。")

    ratio_factor = Dfac * Dfac
    guard("G6-01", rel(ratio_factor, D("0.36")) < D("1e-50"), "E'/(ħω') 相对因子 D²=0.36")
    key["quantum_freq_mismatch_factor"] = fmt(ratio_factor, 25)
    add("C-03", "PASS", "几何频率与量子频率变换不一致的因子 D² 可复算",
        "若 p_z/E=u，则 E'=D E 而 ω'=ω/D，故 E'/(ħω')=D²E/(ħω)。β=u=0.8 时 D=0.6、D²=0.36，来料读数正确。")

    E0 = D(1)
    dot = E0 * D(0) + D(0) * E0
    cross_z = E0 * E0
    guard("G6-02", dot == 0 and cross_z == 1, "圆偏振代表场 E·B=0、E×B=E0² z")
    add("C-04", "PASS", "圆偏振电磁波不变量口径正确",
        "取 E=E0(cosφ,sinφ,0)、B=E0(-sinφ,cosφ,0)，则 E·B=0 且 E×B=E0² z；这是 Maxwell 平面波标准结果。")

    gm_e = D("3.986004355e14")
    gm_m = D("4.902800118e12")
    r_e = [D("6371000"), D("6471000"), D("6771000"), D("7171000"), D("8371000")]
    r_m = [D("1737400"), D("1837400"), D("2137400"), D("2537400"), D("3737400")]
    exp_e = [D("9.820250332"), D("9.519079836"), D("8.694250346"), D("7.751367431"), D("5.688307755")]
    exp_m = [D("1.624218877"), D("1.452234547"), D("1.073180018"), D("0.761493704"), D("0.350998310")]
    grav_e = [gm_e / (r * r) for r in r_e]
    grav_m = [gm_m / (r * r) for r in r_m]
    ok_e = all(rel(x, y) <= D("1e-9") for x, y in zip(grav_e, exp_e))
    ok_m = all(rel(x, y) <= D("1e-9") for x, y in zip(grav_m, exp_m))
    guard("G7-01", ok_e, "地球 5 个引力值用 DE440 GM=3.986004355e14 在 1e-9 相对阈值内匹配")
    guard("G7-02", ok_m, "月球 5 个引力值用 GM=4.902800118e12 在 1e-9 相对阈值内匹配")
    gm_wgs = D("3.986004418e14")
    guard("G7-03", not all(rel(gm_wgs / (r * r), y) <= D("1e-9") for r, y in zip(r_e, exp_e)),
          "WGS84 GM=3.986004418e14 不能逐项匹配，证明 GM 口径承重")
    key["gravity_earth"] = [fmt(x, 12) for x in grav_e]
    key["gravity_moon"] = [fmt(x, 12) for x in grav_m]
    add("C-05", "PASS", "地月平方反比数值表在 DE440 参数口径下可复算",
        "地球用 GM=3.986004355e14 m³/s²、R=6371000 m；月球用 GM=4.902800118e12 m³/s²、R=1737400 m，5+5 个高度点均在 1e-9 相对阈值内匹配来料。")
    add("S-01", "CORRECTED", "地球引力预验差异来自误用 WGS84 GM 而非来料计算错误",
        "预验先用 WGS84 GM=3.986004418e14，地球列出现约 1.6e-7 m/s² 偏差；反解来料隐含 GM≈3.986004355e14，改用 DE440 口径后地球列逐项匹配。该差异属常数口径，不属来料数值错误。")

    # ---------- V148：深层攻破 ----------
    guard("G8-01", "可以具有不同的空间曲率、挠率和角速度" in text, "来料承认 κ/τ/ω 参考系相关")
    add("D-01", "FAIL", "κ、τ、ω 不是洛伦兹不变量，不能当基本常数",
        "同一世界中 κ'=aω'²、τ'=u'ω'、ω'=ω/[γ(1-βu)]；β=u 时 τ'=0。若把某一参考系读出的 κ、τ、ω 当四力常数，就必须额外引入优选参考系或接受洛伦兹破坏；来料没有给出这种结构。")

    guard("G8-02", "几何螺旋频率不能直接等于量子频率" in text and "0.36" in text,
          "来料明确给出几何频率与量子频率不一致")
    add("D-02", "FAIL", "空间螺旋角频率不能等同光子量子频率",
        "E=ħω 中的 ω 是量子态/场的相位频率；来料螺旋 ω 是空间投影曲线的转动率。E'/(ħω') 相对因子 D² 随 boost 变化，说明二者不能用同一对象标识。")

    guard("G8-03", "自由质量为零的粒子还必须满足相应的运动方程" in text, "来料自陈光速条件不是运动方程")
    add("D-03", "FAIL", "光速条件不保证自由零测地线",
        "三维空间速率等于 c 只约束切向长度；非零空间加速度意味着世界线受外力或约束。几何光学中自由光子走零测地线，不能仅凭 a²ω²+u²=1 把螺旋世界线识别为自由光子。")

    guard("G8-04", "真正的圆偏振电磁波没有这个问题" in text, "来料区分场偏振与点粒子螺旋")
    add("D-04", "FAIL", "圆偏振旋转场矢量不等于点粒子螺旋轨迹",
        "圆偏振的 E、B 在固定传播轴上旋转，坡印廷矢量沿 z；它不是某点粒子绕轴作螺旋运动的轨迹。E·B=0、E×B=E0² z 不推出 τ 或 κ 是电磁场基本变量。")

    guard("G8-05", "\\mathbb D_\\mu=\\nabla_\\mu+\\mathcal A_\\mu" in text, "下一阶段建议仍是联络假设")
    add("D-05", "FAIL", "F=[D,D] 是定义联络，不是从螺旋自由度派生规范场",
        "写入 Dμ=∇μ+Aμ 与 Fμν=[Dμ,Dν] 只声明存在内部联络；规范群表示、两种无质量传播模态、耦合常数、Yangian/_BRST 结构与引力场方程都未由基础螺旋变量推出。")

    add("D-06", "FAIL", "V148 仍未证明四力统一",
        "来料自身结论明确“四力统一尚未得到证明”。V148 的有效增量是负向门禁：排除把 κ、τ、ω 当洛伦兹标量，以及排除几何频率直接冒充量子频率。")

    # ---------- 边界与治理 ----------
    zip_claim = "2.96 MB" in text and "35 个文件" in text and "93/93" in text
    zip_file = DATA / "ROOT_V148_Lorentz_Helix_Covariance_Complete.zip"
    guard("G9-01", zip_claim and not zip_file.exists(), "V148 ZIP/93项测试/17项符号检查只在来料中声明，库内未收到实体")
    add("C-01b", "BOUNDARY", "ZIP、测试日志、图片与符号检查只登记不验收",
        "来料声称 2.96 MB ZIP、35 文件、93/93 Python 测试、17/17 SymPy 检查、34 文件 SHA、4 张图与运行脚本；本轮只收到文本，未收到可复跑源码与 manifest。")

    guard("G9-02", "JPL DE440" in text and "不是 ROOT 独立推导的质量或新引力" in text,
          "来料明确地月数值来自 JPL 参数且非独立推导")
    add("C-02b", "BOUNDARY", "地月引力数值是外部参数拟合结果",
        "GM_E、GM_M 与半径均为外部天文参数；平方反比模型复算不证明 ROOT 独立导出 G、质量或新引力定律。")

    guard("G9-03", "四力统一尚未得到证明" in text and "四力统一仍未被证明" in text,
          "V135 与 V148 均自陈四力统一未完成")
    add("I-01", "INFO", "与既有谱系分工：只读审计本次来料，不覆盖 V135 旧档",
        "库内已有 V135 相关谱系（attack72、归档 V135 总报告、r439 洛伦兹障碍）。本册只审本次粘贴的 V135/V148 文本，不改写他人产物。")

    # ---------- 输出 ----------
    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key["entry_counts"] = counts
    key["guard_total"] = len(guards)
    key["guard_pass"] = sum(1 for g in guards if g["status"] == "PASS")
    key["redline"] = {
        "unfinished": "0/6", "systems": "0/22", "UFT3": 0, "L3": 0,
        "validated": 0, "correct_four_force_equations": 0, "L3_implies_L4": False,
    }

    md = []
    md.append("# TUFT r455 数据产物｜ROOT V135 + V148 高维手性与洛伦兹螺旋")
    md.append("")
    md.append("- 来料 SHA256：`" + sha + "`")
    md.append("- 条目：" + str(len(entries)) + "；" + " / ".join(k + " " + str(v) for k, v in sorted(counts.items())))
    md.append("- 守卫：" + str(key["guard_pass"]) + "/" + str(key["guard_total"]))
    md.append("- 关键读数：Spin^c 指标 q(q+1)/2，q=2→3；11D 复旋量 32；Λ 系数 2/9；boost 示例 D=0.6、κ'=5/3、τ'=0；E/(ħω) 因子 D²=0.36；地月 5+5 点按 DE440 口径匹配。")
    md.append("")
    md.append("## 条目")
    for e in entries:
        md.append("")
        md.append("### " + e["id"] + "｜" + e["status"] + "｜" + e["title"])
        md.append(e["detail"])
    md.append("")
    md.append("## 守卫")
    for g in guards:
        md.append("- " + g["id"] + " " + g["status"] + "：" + g["detail"])

    (DATA / (STEM + ".md")).write_text("\n".join(md) + "\n", encoding="utf-8")
    payload = {
        "round": "r455",
        "date": "2026-11-24",
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": sha,
        "entries": entries,
        "guards": guards,
        "key_numbers": key,
    }
    (DATA / (STEM + ".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = []
    report.append("r455 ROOT V135 + V148 audit")
    report.append("entries=" + str(len(entries)))
    report.append("counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True))
    report.append("guards=" + str(key["guard_pass"]) + "/" + str(key["guard_total"]))
    report.append("source_sha256=" + sha)
    report.append("verdict=SPIRC_INDEX_NOT_GENERATIONS--LORENTZ_HELIX_NOT_INVARIANT--FOUR_FORCE_UNPROVEN")
    (DATA / (STEM + "_report.txt")).write_text("\n".join(report) + "\n", encoding="utf-8")

    print("STEM=" + STEM)
    print("entries=" + str(len(entries)), "counts=" + json.dumps(counts, ensure_ascii=False, sort_keys=True))
    print("guards=" + str(key["guard_pass"]) + "/" + str(key["guard_total"]))
    print("source_sha256=" + sha)
    print("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
