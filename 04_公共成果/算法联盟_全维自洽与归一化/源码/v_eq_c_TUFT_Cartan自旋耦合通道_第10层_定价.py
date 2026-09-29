# -*- coding: utf-8 -*-
"""
v = c 求导验证链 · 第 ⑩ 层：Cartan 通道定价 —— 挠率的正确耦合对象能否喂进 g-2 / EDM
============================================================================

位置：承接第 ⑨ 层 `v_eq_c_TUFT_V2prime_修复分支_求导证明与全维度总结.py`。
第 ⑨ 层在 S-03 行留下一句它自己没有算的东西（原文，行号由本册 A-01 现读）：
  「挠率的正确耦合对象：EC 标准结论中挠率代数联系到自旋密度……
    修复方向：宿主应为旋量的自旋/轴向流双线性量……（属下一轮独立攻关项）」
本层就是那一轮：把这个「正确宿主」的重量算出来，并判它能否闭合 g-2 / EDM。

不做的事
--------
不提出新方程（与 ⑨ 层不同，本层零新假设）；不宣称统一场论被推进；
不写 S14 claims.csv、不写算法联盟 README.md（并发写者持有）⇒ 登记是欠账。

本层三件事
----------
[C 结构层] 用 sympy 4x4 Dirac 矩阵把双线性量的 P 宇称**算**出来（不引教科书口径，
          只把教科书表当复现锚）；再把「挠率是否有传播子」做成代数可判的二分：
          辅助场配平方 ⇒ ξ=0 给接触项（不含 q²、无力程），ξ≠0 给极点。
[G 数量级层] 两条**不共享中间量**的路各自算出 EC 自旋接触道在电子尺度的无量纲强度：
          路 A 走自然单位（archive 载 G[GeV^-2]，且先由 SI 三常数复现它）；
          路 B 走 SI，并且「需要哪一幂的 c」由 sympy **解出**（不手数指数）。
          两路必须落在同一年内代才印数。
[B 接口层] 把最小耦合 EC 的代数场方程接到卷十四 §B 的 T_B 扫描：外区 S=0 ⇒ T=0。

诚实红线
--------
本层结论是**否证性的**：正确宿主（自旋/轴向流）在电子尺度的强度由 §G 两条独立路现算并互校，
且 EDM 的偶极算符在该通道下 P-odd 而接触项 P-even ⇒ 树级禁闭。
「方向正确」不等于「能闭合」。这是第 ⑨ 层 T-01（每闭合一条硬伤至少付一个自由度）
在本档案的第二次实测：本层付的是「选对宿主 ⇒ 得到普朗克级压制（十年数由 §G 现读现印，本串不写数）」。
"""
from __future__ import print_function

import os
import re
import sys
import json
import time
import ast

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp
import mpmath as mp

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                       # 04_公共成果/算法联盟_全维自洽与归一化
ROOT = os.path.dirname(os.path.dirname(BASE))      # openuft/
OUT_DIR = os.path.join(BASE, "数据")
SCRIPT_NAME = "v_eq_c_TUFT_Cartan自旋耦合通道_第10层_定价.py"
STEM = "v_eq_c_TUFT_Cartan自旋耦合通道_第10层_定价"

mp.mp.dps = 50

WANT = ["hbar", "c", "e", "G", "Ggev", "alpha", "m_e", "m_e_gev", "GF", "GEV_J"]
CONST_FILE = os.path.join(ROOT, "02_共享基础", "公共计算", "dimensional_transmutation_open7.py")
NINE_MD = os.path.join(BASE, "整理_TUFT_V2修复分支_求导证明与全维度总结_2026-09-30.md")
NINE_JSON = os.path.join(OUT_DIR, "v_eq_c_TUFT_V2prime_修复分支_全维度总结.json")
EC = os.path.join(ROOT, "03_跨体系研究", "tuft_复能动张量协变守恒_EC含挠率.py")
V14 = os.path.join(ROOT, "01_独立体系", "S14_挠率统一场论TUFT", "00_研究立项",
                   "卷十四_CMB与黑洞QNM联合约束_研究计划.md")
AE_FILE = os.path.join(ROOT, "02_共享基础", "公共计算", "源码", "alpha_spiral_semantics.py")
A_E_E = "0.00115965218059"
G2_AUDIT = os.path.join(HERE, "v_eq_c_TUFT_V2_双分量螺旋驻波孤子_可证伪性审计.py")
LEDGER = os.path.join(ROOT, "01_独立体系", "S16_TUFT归一化主册", "13_论文与成果", "台账",
                      "TUFT_归一化台账_v1.0.json")

RESULTS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[" + verdict + "] " + cid.ljust(6) + " | " + item.ljust(26) + " | " + detail)


def ns(x, n=8):
    return mp.nstr(mp.mpf(x), n)


def read_constants(path, names):
    """从载体文件的 AST 现读数值的字面量与其行号（数字不从我记忆里来）。"""
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    got = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id in names and tgt.id not in got:
                    try:
                        val = ast.literal_eval(node.value)
                    except Exception:
                        continue
                    if isinstance(val, (int, float)):
                        got[tgt.id] = (val, node.lineno)
    return got


def anchor(path, needle):
    """在载体文件里按内容找锚点，返回现读行号列表（行号是运行时刻的账，不是抄来的）。"""
    if not os.path.exists(path):
        return []
    hits = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if needle in line:
                hits.append(i)
    return hits


CONST = read_constants(CONST_FILE, WANT)
MISSING = [k for k in WANT if k not in CONST]

NEEDLES = {
    "9层S-03宿主": (NINE_MD, "宿主应为旋量的自旋/轴向流双线性量"),
    "ECω_I=cT_B": (EC, "ω_I = c·T_B"),
    "EC𝓡量纲FAIL": (EC, "𝓡 ≡ g^{μν}𝓡_{μν} = κ + iτ"),
    "卷十四T_B=0基准": (V14, "当 $T_B=0$，模型输出必须复现标准"),
    "卷十四T_B扫描": (V14, "$T_B \\in [0,\\ 10^{-4}]$"),
    "卷十四T_B释义": (V14, "$T_B$ 是黑洞时空背景挠率"),
    "a_e实验值": (AE_FILE, A_E_E),
    "台账|T_B|²": (LEDGER, '"|T_B|^2": 0.220661304516'),
}


# =========================================================================
# 结构层机器：Dirac 矩阵与 P 宇称（变异体走同一条代码路，不许另行断言）
# =========================================================================
I2 = sp.eye(2)
Z2 = sp.zeros(2, 2)
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
METRIC = [1, -1, -1, -1]


def bm(a, b, c, d):
    return sp.BlockMatrix([[a, b], [c, d]]).as_explicit()


G0 = bm(I2, Z2, Z2, -I2)
GM = [G0] + [bm(Z2, s, -s, Z2) for s in (sx, sy, sz)]


def parity_image(Mmat, mut=None):
    """ψ̄ M ψ 在 P: ψ -> γ0 ψ 下的矩阵像。mut='P_DROP_RIGHT_GAMMA' 是变异臂。"""
    if mut == "P_DROP_RIGHT_GAMMA":
        return sp.simplify(Mmat * G0 * G0)          # 故意漏掉右侧的 γ0
    return sp.simplify(G0 * Mmat * G0)


def par_sign(Mmat, mut=None):
    out = parity_image(Mmat, mut)
    for s in (1, -1):
        if sp.simplify(out - s * Mmat) == sp.zeros(4, 4):
            return s
    return None


G5 = sp.simplify(sp.I * G0 * GM[1] * GM[2] * GM[3])
SIG = {}
for mu in range(4):
    for nu in range(4):
        SIG[(mu, nu)] = sp.simplify(sp.I / 2 * (GM[mu] * GM[nu] - GM[nu] * GM[mu]))

BILINEARS = [("S", sp.eye(4)), ("P", G5)]
for mu in range(4):
    BILINEARS.append(("V^%d" % mu, GM[mu]))
for mu in range(4):
    BILINEARS.append(("A^%d" % mu, sp.simplify(GM[mu] * G5)))
for mu in range(4):
    for nu in range(mu + 1, 4):
        BILINEARS.append(("T^{%d%d}" % (mu, nu), SIG[(mu, nu)]))
for nu in range(1, 4):
    BILINEARS.append(("T5^{0%d}" % nu, sp.simplify(SIG[(0, nu)] * G5)))
for mu in range(1, 4):
    for nu in range(mu + 1, 4):
        BILINEARS.append(("T5^{%d%d}" % (mu, nu), sp.simplify(SIG[(mu, nu)] * G5)))

# 复现锚：教科书宇称表（S 偶、P 奇、V 的 0/ i 反号、A 反之于 V、T 与 *T 各自成套）
EXPECT = {"S": 1, "P": -1, "V^0": 1, "V^1": -1, "V^2": -1, "V^3": -1,
          "A^0": -1, "A^1": 1, "A^2": 1, "A^3": 1,
          "T^{01}": -1, "T^{02}": -1, "T^{03}": -1, "T^{12}": 1, "T^{13}": 1, "T^{23}": 1,
          "T5^{01}": 1, "T5^{02}": 1, "T5^{03}": 1, "T5^{12}": -1, "T5^{13}": -1, "T5^{23}": -1}


def cliff_ok():
    for a in range(4):
        for b in range(4):
            rhs = 2 * METRIC[a] * sp.eye(4) if a == b else sp.zeros(4, 4)
            if sp.simplify(GM[a] * GM[b] + GM[b] * GM[a] - rhs) != sp.zeros(4, 4):
                return False
    return True


def g5_ok():
    return (sp.simplify(G5 * G5 - sp.eye(4)) == sp.zeros(4, 4)
            and all(sp.simplify(G5 * GM[a] + GM[a] * G5) == sp.zeros(4, 4) for a in range(4)))


def sign_table(mut=None):
    tab = {}
    unreadable = []
    for nm, Mmat in BILINEARS:
        sg = par_sign(Mmat, mut)
        if sg is None:
            unreadable.append(nm)
        else:
            tab[nm] = sg
    return tab, unreadable


def pred_C01(mut=None):
    tab, unreadable = sign_table(mut)
    if not (cliff_ok() and g5_ok()) or unreadable:
        return False, None, None
    mismatch = sorted([nm for nm in EXPECT if tab.get(nm) != EXPECT[nm]])
    return (not mismatch), tab, mismatch


POLAR_E = -1        # 极矢量 E_i 在 P 下反号：定义，非本轮证明（版面已点名）
POLAR_B = 1         # 轴矢量 B_i 在 P 下同号（用于 C-04 的对比，不作判据）


def pred_C03(mut=None, polar_e=POLAR_E):
    ok, tab, _ = pred_C01(mut)
    if not ok:
        return False, tab
    host_even = (tab["A^0"] ** 2 == 1 and tab["A^1"] ** 2 == 1)
    bil = tab.get("T5^{01}")
    return bool(host_even and bil is not None and bil * polar_e == -1), tab


# =========================================================================
# 量纲解：SI 里需要哪一幂的 c / ℏ，由 sympy 解，不手数
# =========================================================================
def solve_pow(base, target, cands):
    """求整数/实指数 p_i 使 base + Σ p_i·v_i = target（(M,L,T) 指数向量）。"""
    ps = sp.symbols(" ".join("p%d" % i for i in range(len(cands))), real=True)
    if not isinstance(ps, tuple):                   # 单候选时 sympy 返回裸 Symbol
        ps = (ps,)
    eqs = []
    for k in range(3):
        eqs.append(sp.Eq(base[k] + sum(ps[i] * cands[i][k] for i in range(len(cands))), target[k]))
    sol = sp.solve(eqs, ps, dict=True)
    if not sol:
        return None
    return [sol[0][p] for p in ps]


D = {"G": (-1, 3, -2), "hbar": (1, 2, -1), "c": (0, 1, -1), "n": (0, -3, 0),
     "S": (1, -1, -1), "u": (1, -1, -2), "torsion": (0, -1, 0), "energy": (1, 2, -2)}

# ① Cartan 方程：G·S·c^p·ℏ^q 须是挠率 [L^-1]
SOL_T = solve_pow(tuple(x + y for x, y in zip(D["G"], D["S"])), D["torsion"], [D["c"], D["hbar"]])
# ② 接触项系数：G·c^p 须满足 系数·S² = 能量密度 ⇒ 系数维 = u − 2S
COEF_TGT = tuple(D["u"][k] - 2 * D["S"][k] for k in range(3))
SOL_C = solve_pow(D["G"], COEF_TGT, [D["c"]])


# =========================================================================
# §A 载体闸
# =========================================================================
print("=" * 96)
print("第 ⑩ 层：Cartan 通道定价（挠率↔自旋）｜常数与散文锚点全部现读载体")
print("=" * 96)

if MISSING:
    add("A-00", "A 载体层", "常数载体", "载体文件须含本层全部所需常数", "FAIL",
        "缺 " + ",".join(MISSING) + " ⇒ 本层不得印任何数量级")
    print("[自检失败] 载体缺常数，拒绝继续（不许用记忆值补）")
    sys.exit(1)
add("A-00", "A 载体层", "常数载体", "载体文件须含本层全部所需常数", "PASS",
    "现读 " + str(len(CONST)) + " 枚于 " + os.path.relpath(CONST_FILE, ROOT) + "：" +
    "；".join(k + "@" + str(CONST[k][1]) for k in WANT))

ANCH = {}
for k, (path, needle) in NEEDLES.items():
    ANCH[k] = anchor(path, needle)
anch_mut = {}
for k, (path, needle) in NEEDLES.items():                      # 变异臂：把锚点改一个错字
    anch_mut[k] = anchor(path, needle[:-3] + "zz!" if len(needle) > 4 else needle + "zz!")


def pred_A01(mut=None):
    src = anch_mut if mut == "NEEDLE_TYPO" else ANCH
    dead = [k for k, v in src.items() if not v]
    return (not dead), dead


ok_A01, dead_A01 = pred_A01()
add("A-01", "A 载体层", "散文锚点存在性", "本层所判的每处主张必须在盘上被逐字找到",
    "PASS" if ok_A01 else "FAIL",
    "现读行号：" + "；".join(k + "@" + ",".join(str(x) for x in v) for k, v in sorted(ANCH.items()))
    + ("" if ok_A01 else " ｜未命中 " + ",".join(dead_A01) + " ⇒ 该主张不许被判"))

nine_counts = None
if os.path.exists(NINE_JSON):
    try:
        nine_counts = json.load(open(NINE_JSON, encoding="utf-8"))["meta"]["counts"]
    except Exception:
        nine_counts = None
add("A-02", "A 载体层", "⑨ 层产物可读", "第 ⑨ 层 JSON 在盘且含判定分布（本层不引其结论数值）",
    "PASS" if nine_counts else "BOUNDARY",
    "⑨层判定分布：" + (json.dumps(nine_counts, ensure_ascii=False)
                        if nine_counts else "未找到或不可读 ⇒ 本层不引其计数"))

hbar = mp.mpf(repr(CONST["hbar"][0]))
cl = mp.mpf(repr(CONST["c"][0]))
Gsi = mp.mpf(repr(CONST["G"][0]))
Ggev = mp.mpf(repr(CONST["Ggev"][0]))
m_e = mp.mpf(repr(CONST["m_e"][0]))
m_e_gev = mp.mpf(repr(CONST["m_e_gev"][0]))
GF = mp.mpf(repr(CONST["GF"][0]))
GEV_J = mp.mpf(repr(CONST["GEV_J"][0]))
a_e = mp.mpf(A_E_E)


# =========================================================================
# §C 结构层
# =========================================================================
print("\n=== §C 结构层：Cartan 耦合的宿主是谁，它的对称性是什么 ===")

ok_C01, tab, mismatch = pred_C01()
add("C-01", "C 结构层", "γ 代数与 P 宇称表（复现闸）",
    "先复现已证对象：{γμ,γν}=2gμν、(γ5)²=1、{γ5,γμ}=0 与 " + str(len(BILINEARS)) +
    " 个双线性量的 P 号",
    "PASS" if ok_C01 else "FAIL",
    "Clifford 16 项恒等=%s；γ5²=1 与 {γ5,γμ}=0=%s；P 号表 %d 条对教科书锚点分歧 %d 处%s"
    % (cliff_ok(), g5_ok(), len(tab), len(mismatch or []),
       "" if ok_C01 else "；分歧明细 " + json.dumps(mismatch, ensure_ascii=False)))

sgn_A0 = tab.get("A^0") if tab else None
sgn_A1 = tab.get("A^1") if tab else None
ok_C02 = bool(sgn_A0 is not None and sgn_A1 is not None and sgn_A0 == -sgn_A1)
add("C-02", "C 结构层", "轴矢量的 0/空间分量在 P 下反号",
    "挠率的正确宿主 (ψ̄γ^μγ5ψ)： contraction 偶，但时间分量本身奇 ⇒ 「把 A^0 当标量密度」不合法",
    "PASS" if ok_C02 else "FAIL",
    "机器现读 A^0 号=%s、A^1 号=%s ⇒ 二者反号（contraction 由平方结构自动 P-even，"
    "而单个 A^0 分量 P-odd）；故任何把轴向**密度**直接当背景标量用的写法，在 P 下不闭合"
    % (sgn_A0, sgn_A1))

ok_C03, _t3 = pred_C03()
sgn_T5 = _t3.get("T5^{01}") if _t3 else None
host_sgn = ("A^0=%s/A^1=%s 平方皆 +1" % (_t3.get("A^0"), _t3.get("A^1"))) if _t3 else "表未出"
add("C-03", "C 结构层", "EDM 通道的对称性禁闭",
    "若约化理论保持 P（宿主 A_μA^μ 为 P 偶），偶极算符 ψ̄σ^{0i}γ5 ψ E_i 不可由该接触项产生",
    "PASS" if ok_C03 else "FAIL",
    ("机器现读双线性 T5^{01}=ψ̄σ^{01}γ5ψ 的 P 号=%s，宿主自收缩 %s ⇒ P 偶；"
     "前提「E_i 为极矢量、P 下反号」（定义，"
     "不是本轮证明，已点名）⇒ 算符整体 P-odd，接触项 P-even ⇒ 该通道任意阶插入都生不出偶极。"
     "**EDM 由对称性给 0，不需要任何屏蔽因子，也不依赖螺旋窗口**（比 ⑨ 层 S-01 的窗口论证硬）")
    % (sgn_T5, host_sgn))

tab_T01 = tab.get("T^{01}") if tab else None
tab_T12 = tab.get("T^{12}") if tab else None
add("C-04", "C 结构层", "g-2 通道不被对称性禁闭",
    "同一 σ^{μν} 张量对 E（P-odd）与 B（P-even）分别给出禁止/允许的通道",
    "INFO",
    "机器现读 T^{0i} 号=%s、T^{ij} 号=%s：磁矩型 ψ̄σ^{μν}ψ B_{μν} 为 P 偶（POLAR_B=%s）⇒ 放行，"
    "欠的只是数量级；电偶极型为 P 奇 ⇒ 禁闭（C-03）。故 g-2 的账只能由 §G 判"
    % (tab_T01, tab_T12, POLAR_B))

K, Jc, xi, q2, Aec = sp.symbols('K J xi q2 A', real=True)
Lalg = -sp.Rational(1, 2) * Aec * K ** 2 + Jc * K
L_eff_alg = sp.simplify(Lalg.subs(K, sp.solve(sp.diff(Lalg, K), K)[0]))
contact_coef = sp.simplify(sp.diff(L_eff_alg, Jc, 2) / 2)
Lkin = sp.Rational(1, 2) * K * (xi * q2 - Aec) * K + Jc * K
L_eff_kin = sp.simplify(Lkin.subs(K, sp.solve(sp.diff(Lkin, K), K)[0]))
den_kin = sp.denom(sp.together(L_eff_kin))


def pred_C05(as_if_kinetic_is_contact=False):
    """ξ=0 时接触系数必须不含 q²；ξ≠0 时分母必须含 q²。"""
    a = sp.simplify(contact_coef - sp.Rational(1, 2) / Aec) == 0
    c = "q2" in str(den_kin)
    if as_if_kinetic_is_contact:      # 变异臂：拿动能版的分母去声明「与 q² 无关」
        b = ("q2" not in str(den_kin))
    else:
        b = ("q2" not in str(contact_coef))
    return bool(a and b and c)


ok_C05 = pred_C05()
add("C-05", "C 结构层", "挠率的代数性 ⇒ 必为接触项",
    "最小耦合 EC（无挠率动能项）积分掉挠率：所得四项相互作用无极点、不含量度尺度",
    "PASS" if ok_C05 else "FAIL",
    "配平方残差 L_eff−J²/(2A)=%s（机器零）；有效系数 ∂²L_eff/∂J²/2=%s 不含 q² ⇒ 无传播子、无力程；"
    "动能版（ξ≠0）分母=%s ⇒ 一旦加动能项就是极点（长程或有质量媒介）"
    % (sp.simplify(L_eff_alg - Jc ** 2 / (2 * Aec)), contact_coef, den_kin))

add("C-06", "C 结构层", "受检主张「卷十四 §B 的外区背景挠率可非零」判 FAIL",
    "C-05 的代数方程直接推：自旋源为零的时空区，挠率不是「小」而是恒等于零",
    "FAIL",
    "代数解 K=J/A 无齐次自由度（J=0 ⇒ K=0，机器解）⇒ 真空/外区挠率恒零。对卷十四的后果："
    "§B 把 T_B 当**外区背景挠率**扫 [0,1e-4]（锚点 卷十四T_B=0基准@" +
    ",".join(str(x) for x in ANCH["卷十四T_B=0基准"]) + "、卷十四T_B扫描@" +
    ",".join(str(x) for x in ANCH["卷十四T_B扫描"]) + "），但最小耦合 EC 在外区给 T=0 ⇒ "
    "该扫描没有经典源。要让它非零只有两条：(i) 加动能项（C-05 已证 ⇒ 长程力，落第五力实验区）"
    "或 (ii) 声明 T_B 为不受场方程约束的外冻结背景（＝特设输入，与被否证的 0.00404 同族）。")

# =========================================================================
# §G 数量级层
# =========================================================================
print("\n=== §G 数量级层：EC 自旋接触道的无量纲强度（双路互校）===")

kappa_nat = 8 * mp.mpf(mp.pi) * Ggev
C0 = {"3/16": mp.mpf(3) / 16, "3/8": mp.mpf(3) / 8, "3/4": mp.mpf(3) / 4, "3/2": mp.mpf(3) / 2}


def eta_A(scale_geV, mut=None):
    kap = Ggev if mut == "DROP_8PI" else kappa_nat
    return {k: v * kap * scale_geV ** 2 for k, v in C0.items()}


def eta_B(mut=None):
    """路 B：SI，系数幂用 G-02 解出的 p；mut=NAIVE_CP4 退回手写的 8πG/c⁴。"""
    n = (m_e * cl / hbar) ** 3
    S = (hbar / 2) * n
    p = int(SOL_C[0]) if (SOL_C is not None and mut != "NAIVE_CP4") else -4
    coeff = 8 * mp.pi * Gsi * cl ** p           # p=-2 ⇒ 系数 = 8πG/c²，由 G-02 解出而非手数
    u_contact = coeff * S ** 2
    u_rest = m_e * cl ** 2 * n
    return u_contact / u_rest


def eta_B_closed_form():
    """路 B 的闭式：η_B = 2πG m_e²/(ℏc)（把上面四行代死）。用它判「实现==推导」。"""
    return 2 * mp.pi * Gsi * m_e ** 2 / (hbar * cl)


M_pl = mp.sqrt(hbar * cl / Gsi)
E_pl_J = M_pl * cl ** 2
E_pl_GeV = E_pl_J / GEV_J
Ggev_derived = 1 / E_pl_GeV ** 2
rel_A = abs(Ggev_derived - Ggev) / Ggev

add("G-01", "G 数量级层", "复现闸：由 SI 三常数导 G[GeV^-2]",
    "先回到档案已载的 Ggev，才有资格给新对象定价",
    "PASS" if rel_A < mp.mpf("1e-4") else "FAIL",
    "M_Pl=sqrt(ℏc/G)=%s kg；E_Pl=%s GeV；1/E_Pl²=%s GeV^-2 对 archive 载 %s ⇒ 相对差 %s"
    % (ns(M_pl, 10), ns(E_pl_GeV, 10), ns(Ggev_derived, 12), ns(Ggev, 12), ns(rel_A, 3)))

def pow_txt(p):
    """把解出的 c 幂写成不会读反的形式：-3 ⇒ 1/c^3（版面里 c^{负幂} 会被读成 c 的正幂）。"""
    p = int(p)
    return "c^" + str(p) if p >= 0 else "1/c^" + str(-p)


add("G-02", "G 数量级层", "量纲所需的 c / ℏ 幂由 sympy 解出",
    "Cartan 方程与接触系数各需要哪一幂的 c（不手数），两个解是否差一整幂",
    "INFO",
    ("①Cartan：[G·S]=%s 须成挠率 [L^-1] ⇒ 解 (p_c,p_hbar)=%s ⇒ T=8πG·(%s)·S，"
     "而把 κ 记作 8πG/c⁴ 再去乘自旋密度就差一整幂的 c（档案 03_跨体系研究 报告 §5 用自建维度向量"
     "抓到同族缺陷，锚点 EC𝓡量纲FAIL@%s）；"
     "②接触：[系数]=u−2S=%s ⇒ p_c=%s ⇒ 系数=8πG·(%s)。①②相差一整幂 c，源于 x⁰=ct 与 x⁰=t 两种约定，"
     "**本层不裁这个约定**，故只把「十年不变性」当判据（G-04），不把系数当判据")
    % (str(tuple(x + y for x, y in zip(D["G"], D["S"]))), str(SOL_T),
       pow_txt(SOL_T[0]) if SOL_T else "无解",
       ",".join(str(x) for x in ANCH["EC𝓡量纲FAIL"]),
       str(COEF_TGT), str(SOL_C[0]) if SOL_C else "无解",
       pow_txt(SOL_C[0]) if SOL_C else "无解"))

add("G-03", "G 数量级层", "路 A：自然单位 η = c₀·κ·E²",
    "以电子质量为尺度，EC 自旋接触道的无量纲强度",
    "INFO",
    "κ=8πG=%s GeV^-2；m_e=%s GeV ⇒ η(c₀∈{3/16,3/8,3/4,3/2}) = %s ~ %s；"
    "约定臂内跨 %s 个十年 ⇒ 数量级对 c₀ 不变"
    % (ns(kappa_nat, 6), ns(m_e_gev, 8), ns(min(eta_A(m_e_gev).values()), 4),
       ns(max(eta_A(m_e_gev).values()), 4),
       ns(mp.log10(max(eta_A(m_e_gev).values()) / min(eta_A(m_e_gev).values())), 4)))

eb = eta_B()
eA_ref = eta_A(m_e_gev)["3/4"]


def eta_B_spin1(mut=None):
    """变异臂用：把自旋取成 ℏ 而非 ℏ/2（其余不动）。 decade 仍可能同一年内代，但闭合身份必崩。"""
    n = (m_e * cl / hbar) ** 3
    S = hbar * n
    return (8 * mp.pi * Gsi * cl ** (int(SOL_C[0]) if SOL_C else -2)) * S ** 2 / (m_e * cl ** 2 * n)


def g04_identity(v_b, v_a):
    """两路之比必须恰好等于自旋因子的倒数（c₀=3/4 ⇒ 1/(4c₀)=1/3）——自我闭合，不是巧合。"""
    exp_ratio = 1 / (4 * C0["3/4"])
    got_ratio = v_b / v_a
    return abs(got_ratio - exp_ratio) / exp_ratio, got_ratio, exp_ratio


def pred_G04(mut=None):
    v_b = eta_B_spin1() if mut == "SPIN_ONE_UNIT" else eta_B(mut)
    v_a = eta_A(m_e_gev, mut)["3/4"]          # eta_A 只对 DROP_8PI 敏感
    resid, _g, _e = g04_identity(v_b, v_a)
    decade_ok = abs(mp.log10(v_b) - mp.log10(v_a)) < 1
    return (decade_ok and resid < mp.mpf("1e-6")), v_b, v_a, resid, decade_ok


ok_G04, eb2, ea2, resid_G04, dec_G04 = pred_G04()
_rid_b = g04_identity(eta_B_spin1(), ea2)[0]
_rid_naive = g04_identity(eta_B("NAIVE_CP4"), ea2)[0]
add("G-04", "G 数量级层", "双路互校（不共享中间量）＋比值身份闭合",
    "路 A（自然单位）与路 B（SI＋G-02 的解）不仅要落在同一年内代，其比值还必须**等于**自旋因子的倒数",
    ("PASS" if ok_G04 else ("BOUNDARY" if dec_G04 else "FAIL")),
    "η_A=%s 对 η_B=%s ⇒ log10 差 %s < 1。更强的那条：两路之比实测 %s 对 1/(4c₀)=%s（c₀=3/4），"
    "相对残差 %s ⇒ 差的**正是** S=(ℏ/2)n 里那个自旋 ½ 的平方（4 倍），不是路径错误也不是巧合。"
    "两枚变异臂各打这一格的一支：NAIVE_CP4（手写 8πG/c⁴）十年差 %s、身份残差 %s ⇒ 十年臂红；"
    "SPIN_ONE_UNIT（自旋取 ℏ 而非 ℏ/2）十年仍一致而身份残差 %s ⇒ 身份臂红 ⇒ 本行判 PASS 需两支同时成立"
    % (ns(ea2, 6), ns(eb2, 6), ns(abs(mp.log10(eb2) - mp.log10(ea2)), 4),
       ns(g04_identity(eb2, ea2)[1], 8), ns(g04_identity(eb2, ea2)[2], 8), ns(resid_G04, 3),
       ns(abs(mp.log10(eta_B('NAIVE_CP4')) - mp.log10(ea2)), 4), ns(_rid_naive, 4), ns(_rid_b, 4)))

add("G-05", "G 数量级层", "与弱作用的比价 G_T/G_F",
    "把 EC 接触道写成费米型耦合，它比 μ 衰变定的 G_F 弱多少",
    "PASS" if 0 < kappa_nat / GF < 1 else "FAIL",
    "G_T=κ=%s GeV^-2；G_F=%s GeV^-2（载体 %s:%d）⇒ G_T/G_F=%s ~ %s（跨约定），"
    "判据取「严格小于 1 且大于 0」，即 EC 接触道比弱作用更弱"
    % (ns(kappa_nat, 6), ns(GF, 8), os.path.relpath(CONST_FILE, ROOT), CONST["GF"][1],
       ns(min(C0.values()) * kappa_nat / GF, 4), ns(max(C0.values()) * kappa_nat / GF, 4)))

gt_gf = {k: v * kappa_nat / GF for k, v in C0.items()}


def deficit(scale_geV, mut=None):
    ea = eta_A(scale_geV, mut)
    return {k: mp.log10(a_e / v) for k, v in ea.items()}


def_low = min(deficit(m_e_gev).values())
def_high = max(deficit(m_e_gev).values())
DEF_BAR = mp.mpf(10)          # 门槛：≥10 个十年才判「喂不进」，比「能动 a_e 任一位」强 7 个十年
ok_G06 = def_low >= DEF_BAR
add("G-06", "G 数量级层", "受检主张「Cartan 道能解释 a_e」判 FAIL（电子尺度）",
    "该通道能否解释 a_e（引 archive 载实验值），并明确结论是下界",
    "FAIL" if ok_G06 else "PASS",
    "a_e=%s（载体 %s:%d 现读）；η=%s ~ %s ⇒ 欠 %s ~ %s 个十年（门槛=%s 个十年，由本轮显式声明而非手感；"
    "实测距门槛 %s 个十年）。另：接触项不含光子，要移出一个 a_e 至少还得挂电磁耦合（本轮**未算圈图**），"
    "故写成下界。对照尺度：同一式在 E=E_Pl 处 η=%s（欠账=%s，已非欠账）⇒ 通道只在普朗克尺度成立，"
    "而 TUFT 要解释的是电子的磁矩"
    % (a_e, os.path.relpath(AE_FILE, ROOT), (ANCH["a_e实验值"] or [0])[0],
       ns(min(eta_A(m_e_gev).values()), 4), ns(max(eta_A(m_e_gev).values()), 4),
       ns(def_low, 4), ns(def_high, 4), ns(DEF_BAR, 2), ns(def_low - DEF_BAR, 4),
       ns(max(eta_A(E_pl_GeV).values()), 6), ns(min(deficit(E_pl_GeV).values()), 4)))

G2_LABEL = "74.2"
lab_hits = anchor(G2_AUDIT, G2_LABEL)
alpha = mp.mpf(repr(CONST["alpha"][0]))
g2_tuft = mp.mpf("0.00404")
cands = {
    "100*(1-a_e/g2)": (1 - a_e / g2_tuft) * 100,
    "100*(g2/a_e-1)": (g2_tuft / a_e - 1) * 100,
    "100*(1-g2/(2α))": (1 - g2_tuft / (2 * alpha)) * 100,
    "100*(2α/g2-1)": (2 * alpha / g2_tuft - 1) * 100,
    "200*|g2-a_e|/(g2+a_e)": abs(g2_tuft - a_e) / (a_e + g2_tuft) * 200,
}
closest = sorted(cands.items(), key=lambda kv: abs(kv[1] - mp.mpf("74.2")))[0]
add("G-07", "G 数量级层", "引 74.2% 前先复现它的分母",
    "档案给 g-2_TUFT=0.00404 打了「偏 74.2%」的标签；本层只问：哪一对数除得出 74.2",
    "BOUNDARY" if abs(closest[1] - mp.mpf("74.2")) > mp.mpf("0.05") else "PASS",
    "候选（全部由本文件所读常数现算）：" +
    "；".join(k + "=" + ns(v, 5) for k, v in sorted(cands.items())) +
    " ⇒ 最近者 %s=%s（距 74.2 差 %s）；标签载体 %s:%s。本轮不据此判档案错，"
    "只登记「该百分数的分母在档案里没有点名」"
    % (closest[0], ns(closest[1], 5), ns(abs(closest[1] - mp.mpf("74.2")), 3),
       os.path.basename(G2_AUDIT), ",".join(str(x) for x in lab_hits)))

# =========================================================================
# §B 接口层
# =========================================================================
print("\n=== §B 接口层：同名 T_B 的三处载体与本轮判掉的选项 ===")

add("B-01", "B 接口层", "同名 T_B 的三枚载体互斥",
    "ω_I=c·T_B（EC 报告 §5）／|T_B|²（S16 台账）／卷十四的外区背景挠率 [0,1e-4]",
    "FAIL",
    "现读：EC「ω_I = c·T_B（T_B 为挠率量 [L^-1]）」@" +
    ",".join(str(x) for x in ANCH["ECω_I=cT_B"]) + " ⇒ 那里 T_B 是挠率，故 T_B=0 ⇒ ω_I=0，"
    "阻尼全由挠率提供；卷十四要求 T_B=0 时复现 ω_I=-0.08896≠0 @" +
    ",".join(str(x) for x in ANCH["卷十四T_B=0基准"]) + "，并把 T_B 当**无量纲**微扰扫 @" +
    ",".join(str(x) for x in ANCH["卷十四T_B扫描"]) + " 与线性式 ω_I=ω_I⁽⁰⁾+k_I·T_B ⇒ "
    "两载体对同一关系式给出**相反的阻尼归属**，不可同时成立；第三枚 |T_B|²=0.220661304516 @" +
    ",".join(str(x) for x in ANCH["台账|T_B|²"]) + " 是势垒双程透射率，与挠率无关 ⇒ "
    "任何自动引用会把 0.2207 读成挠率幅度")

add("B-02", "B 接口层", "卷十四 §B 的 T_B 在最小 EC 下无源",
    "C-06 的代数结论直接作用到 §B 的参数扫描上",
    "FAIL",
    "外区 S=0 ⇒ T=0（C-05/C-06 机器解）⇒ §B 的 T_B 扫描要么改理论（加动能项 ⇒ 长程力，"
    "见 B-03 的未取数），要么改性质（外冻结背景 ⇒ 特设，与 0.00404 同族）。"
    "两个选项都要付自由度，没有第三条免费的路")

add("B-03", "B 接口层", "传播挠率的实验账未取数",
    "若 ξ≠0，接触变极点、力有量程 λ=1/m_T；第五力/自旋-自旋实验给上限",
    "BOUNDARY",
    "本层未在 archive 内找到可用的第五力或自旋-自旋上限读数（不引外部数），故只登记欠账："
    "C-05 已给出「ξ≠0 ⇒ 极点」的代数事实，实验比价未做")

add("B-04", "B 接口层", "对第 ⑨ 层 S-03 的答复",
    "S-03 说宿主应为自旋/轴向流双线性量，本层算了这个宿主之后是什么",
    "INFO",
    "宿主选对了（C-01~C-03：A_μA^μ 为 P 偶、积分掉挠率所得接触项无极点、EDM 被 P 禁闭），"
    "但代价是 G-06 的 " + ns(def_low, 4) + " 个十年（本层现读下界）⇒ "
    "**S-03 的修复方向判为「方向正确、闭合无效」**："
    "它把 EDM 灾难解释干净（对称性给 0，且不依赖 ⑨ 层 S-01 的窗口选取），"
    "却把 g-2 推得更远。锚点 9层S-03宿主@" + ",".join(str(x) for x in ANCH["9层S-03宿主"]))

# =========================================================================
# §T 自由度账（承接 ⑨ 层 T-01）
# =========================================================================
add("T-01", "T 自由度层", "交换定理在本档案的第二次实测",
    "⑨ 层原则：每闭合一条硬伤至少支付一个自由度",
    "FAIL",
    "本层闭合的是「宿主是谁」（S-03），支付的是「该通道的效力」：选自旋为源 ⇒ 耦合被钉在 G"
    "（κ=8πG=%s GeV^-2），没有可调旋钮；不想要这个压制就再买一个自由度（动能项或外加背景），"
    "分别落入 B-03 的未取数实验区与 B-02 的特设桶 ⇒ 与 ⑨ 层 T-01 同形，是同一定理的两次实例"
    % (ns(kappa_nat, 6),))

add("T-02", "T 自由度层", "本轮未推进清单（不得记为已解决）",
    "哪些东西在本轮之后仍然开放",
    "FAIL",
    "①TUFT 的 g-2 映射仍未导出（本轮只**判死一条候选路**）；②绝对标度/质量层级/β 缺口/δ_TUFT "
    "一字未动；③ξ≠0 的实验比价未做（B-03）；④非 minimal 耦合 EC 未扫，本层只判最小耦合；"
    "⑤圈图系数未算，故 G-06 写成下界而非精确排除；⑥未提出新方程，⑨ 层 V2′ 状态矩阵不改写；"
    "⑦S14 claims.csv 与算法联盟 README.md 本轮未写（登记债）")

# =========================================================================
# 汇总 + 不可回退自检
# =========================================================================
print("\n" + "=" * 96)
counts = {}
for rr in RESULTS:
    counts[rr["verdict"]] = counts.get(rr["verdict"], 0) + 1
print("汇总：总数 %d | %s" % (len(RESULTS), " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
print("总耗时 %.1fs" % (time.time() - T_START))
print("=" * 96)

GUARD = {"A-00": "PASS", "A-01": "PASS", "A-02": "PASS", "C-01": "PASS", "C-02": "PASS",
         "C-03": "PASS", "C-05": "PASS", "C-06": "FAIL", "G-01": "PASS", "G-04": "PASS",
         "G-05": "PASS", "G-06": "FAIL", "G-07": "BOUNDARY", "B-01": "FAIL", "B-02": "FAIL",
         "B-03": "BOUNDARY", "T-01": "FAIL", "T-02": "FAIL"}


def verdict_of(rid):
    for q in RESULTS:
        if q["id"] == rid:
            return q["verdict"]
    return None


bad = [(k, v, verdict_of(k)) for k, v in sorted(GUARD.items()) if verdict_of(k) != v]
if bad:
    print("[自检失败] 与基线不符（禁止静默改判）：" + json.dumps(bad, ensure_ascii=False))
    sys.exit(1)
print("[自检] " + str(len(GUARD)) + " 条不可回退基线全部在位")

# =========================================================================
# 牙齿：变异体走**同一条判定函数**，只改被点名的那一步
# =========================================================================
MUT = {
    "P_DROP_RIGHT_GAMMA": (["C-01", "C-02", "C-03"], [],
                           "P 变换的矩阵像漏掉右侧 γ0（γ0 M → M γ0 γ0）"),
    "POLAR_E_AS_AXIAL": (["C-03"], [], "把 E_i 当轴矢量（P 偶）来判 EDM 算符"),
    "PROP_AS_CONTACT": (["C-05"], [], "拿动能版分母去声明「与 q² 无关」（接触/极点之辨的桩）"),
    "NAIVE_CP4": (["G-04"], [], "路 B 无视 G-02 的解，退回手写 8πG/c⁴"),
    "SPIN_ONE_UNIT": (["G-04"], [], "路 B 的自旋取 ℏ 而非 ℏ/2：十年仍一致，但比值身份必崩"
                                    "⇒ 证明 G-04 的 PASS 确实要两支同时成立"),
    "DROP_8PI": (["G-04"], ["G-06"],
                  "把 κ=8πG 改成 G（丢 8π）⇒ 只能打红 G-04；G-06 在同一个臂内被现量证明**不红**"
                  "（十年不变性吸收 8π），故该臂的「未打红名单」是判据的一部分而非遗漏"),
    "RATIO_INVERT": (["G-05"], [], "把 G_T/G_F 写成 G_F/G_T"),
    "SCALE_AT_PLANK": (["G-06"], [], "把尺度由 m_e 换成 E_Pl：证明 G-06 不是恒 FAIL 的桩，判决随尺度移动"),
    "NEEDLE_TYPO": (["A-01"], [], "把每个锚点串改一个错字（证明 A-01 不是无条件 PASS）"),
}


def run_mutant(name):
    """返回该变异臂下**受影响行**的判定；判据与基线用同一批函数。"""
    out = {}
    if name == "P_DROP_RIGHT_GAMMA":
        ok1, tab1, _m = pred_C01(name)
        out["C-01"] = "PASS" if ok1 else "FAIL"
        a0 = tab1.get("A^0") if tab1 else None
        a1 = tab1.get("A^1") if tab1 else None
        out["C-02"] = "PASS" if (a0 is not None and a1 is not None and a0 == -a1) else "FAIL"
        ok3, _t = pred_C03(name)
        out["C-03"] = "PASS" if ok3 else "FAIL"
    elif name == "POLAR_E_AS_AXIAL":
        ok3, _t = pred_C03(None, polar_e=POLAR_B)
        out["C-03"] = "PASS" if ok3 else "FAIL"
    elif name == "PROP_AS_CONTACT":
        out["C-05"] = "PASS" if pred_C05(True) else "FAIL"
    elif name == "NAIVE_CP4":
        ok, _b, _a, _r, _d = pred_G04(name)
        out["G-04"] = "PASS" if ok else ("BOUNDARY" if _d else "FAIL")
    elif name == "SPIN_ONE_UNIT":
        ok, _b, _a, _r, dk = pred_G04(name)
        out["G-04"] = "PASS" if ok else ("BOUNDARY" if dk else "FAIL")
    elif name == "DROP_8PI":
        ok, _b, _a, _r, _d = pred_G04(name)
        out["G-04"] = "PASS" if ok else ("BOUNDARY" if _d else "FAIL")
        d = deficit(m_e_gev, name)
        out["G-06"] = "FAIL" if min(d.values()) >= DEF_BAR else "PASS"
    elif name == "SCALE_AT_PLANK":
        d = deficit(E_pl_GeV)
        out["G-06"] = "FAIL" if min(d.values()) >= DEF_BAR else "PASS"
    elif name == "RATIO_INVERT":
        r = GF / kappa_nat
        out["G-05"] = "PASS" if (0 < r < 1) else "FAIL"
    elif name == "NEEDLE_TYPO":
        ok, _d = pred_A01("NEEDLE_TYPO")
        out["A-01"] = "PASS" if ok else "FAIL"
    else:
        raise KeyError(name)
    return out


print("\n=== 牙齿（变异体）：每枚必须只打红它点名的格 ===")
mut_report = []
mut_fail = []
for name in sorted(MUT):
    expect_ids, expect_same_ids, why = MUT[name]
    got = run_mutant(name)
    reddened = sorted(k for k, v in got.items() if v != verdict_of(k))
    stayed = sorted(k for k in got if k not in reddened)
    clean = (set(reddened) == set(expect_ids)) and (set(stayed) == set(expect_same_ids))
    mut_report.append({"mutant": name, "why": why, "must_redden": sorted(expect_ids),
                       "must_stay": sorted(expect_same_ids),
                       "reddened": reddened, "not_reddened_by_this_mutant": stayed,
                       "clean": clean})
    print("[牙] " + name.ljust(20) + " 期望点名 " + (",".join(sorted(expect_ids)) or "<无>").ljust(18) +
          " 实打红 " + (",".join(reddened) if reddened else "<无>").ljust(18) +
          ("OK" if clean else "BAD") + " ｜刻意探针须不红:" +
          (",".join(expect_same_ids) if expect_same_ids else "<无>") +
          " ｜实际未红:" + (",".join(stayed) if stayed else "<无>") + " ｜" + why)
    if not clean:
        mut_fail.append(name)

armed = sorted({r for v in MUT.values() for r in v[0]})
all_row_ids = [q["id"] for q in RESULTS]
unarmed = sorted(set(all_row_ids) - set(armed))
print("[牙账] " + str(len(MUT)) + " 枚变异体覆盖 " + str(len(armed)) + " / " +
      str(len(all_row_ids)) + " 行：" + ",".join(armed))
print("[牙账] 无变异臂的行（不得当作已被见证）共 " + str(len(unarmed)) + " 行：" + ",".join(unarmed))

if "--selftest" in sys.argv:
    if mut_fail:
        print("[牙齿失败] 未按要求打红：" + ",".join(mut_fail))
        sys.exit(2)
    print("[牙齿] " + str(len(MUT)) + " 枚变异体全部只在其点名格上打红")
    sys.exit(0)
if mut_fail:
    print("[警告] 变异体未全红 ⇒ 本轮不写产物，先修牙：" + ",".join(mut_fail))
    sys.exit(2)

os.makedirs(OUT_DIR, exist_ok=True)
payload = {
    "meta": {
        "script": SCRIPT_NAME, "layer": "第 ⑩ 层（v=c 求导验证链）",
        "elapsed_sec": round(time.time() - T_START, 2), "counts": counts,
        "guard_baseline": GUARD,
        "carriers": {
            "constants": {"file": os.path.relpath(CONST_FILE, ROOT),
                          "values": {k: {"value": CONST[k][0], "line": CONST[k][1]} for k in WANT}},
            "prose_anchor_lines": ANCH,
            "anchor_files": {k: os.path.relpath(v[0], ROOT) for k, v in NEEDLES.items()},
            "a_e_source": {"file": os.path.relpath(AE_FILE, ROOT),
                           "line": (ANCH["a_e实验值"] or [None])[0], "value": A_E_E},
            "g2_label_source": {"file": os.path.relpath(G2_AUDIT, ROOT), "lines": lab_hits,
                                "label": "74.2%", "candidate_denominators":
                                    {k: mp.nstr(v, 8) for k, v in cands.items()},
                                "closest": [closest[0], mp.nstr(closest[1], 8)]},
            "barrier_T_B2_source": {"file": os.path.relpath(LEDGER, ROOT),
                                    "lines": ANCH["台账|T_B|²"], "value": 0.220661304516}
        },
        "key_numbers": {
            "kappa_8piG_GeV2": mp.nstr(kappa_nat, 12),
            "Ggev_from_SI": mp.nstr(Ggev_derived, 12), "E_Pl_GeV": mp.nstr(E_pl_GeV, 12),
            "M_Pl_kg": mp.nstr(M_pl, 12), "rel_diff_vs_archive_Ggev": mp.nstr(rel_A, 4),
            "dimension_solve_cartan": str(SOL_T), "dimension_solve_coeff": str(SOL_C),
            "eta_routeA_by_convention": {k: mp.nstr(v, 8) for k, v in eta_A(m_e_gev).items()},
            "eta_routeB_SI": mp.nstr(eta_B(), 8),
            "routeAB_log10_gap": mp.nstr(abs(mp.log10(eta_B()) - mp.log10(eA_ref)), 6),
            "routeAB_ratio": mp.nstr(g04_identity(eta_B(), eA_ref)[1], 10),
            "routeAB_ratio_expected_1_over_4c0": mp.nstr(g04_identity(eta_B(), eA_ref)[2], 10),
            "routeAB_identity_rel_residual": mp.nstr(g04_identity(eta_B(), eA_ref)[0], 4),
            "deficit_gate_decades": mp.nstr(DEF_BAR, 4),
            "deficit_decades_by_convention": {k: mp.nstr(v, 6) for k, v in deficit(m_e_gev).items()},
            "deficit_at_E_Pl": {k: mp.nstr(v, 6) for k, v in deficit(E_pl_GeV).items()},
            "G_T_over_G_F": {k: mp.nstr(v, 6) for k, v in gt_gf.items()},
            "parity_table_machine": tab
        },
        "mutant_report": mut_report,
        "teeth_coverage": {"n_mutants": len(MUT), "n_rows": len(all_row_ids),
                           "armed_rows": armed, "unarmed_rows": unarmed},
        "teeth_coverage": {"armed_rows": armed, "unarmed_rows": unarmed,
                           "rows_total": len(all_row_ids),
                           "note": "无臂行不得当作已被见证"},
        "registration_debt": "本轮未写 S14 claims.csv、未写算法联盟 README.md（并发写者持有）；"
                             "登记由下一轮现读文件尾接续",
        "red_line": "数学自洽 != 物理成立；本层是**否证**（判死一条候选通道），不是新公式，"
                    "不宣称推进统一场论"
    },
    "results": RESULTS
}
JSON_PATH = os.path.join(OUT_DIR, STEM + ".json")
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = []
lines.append("# v = c 求导验证链 第 ⑩ 层：Cartan 通道定价（挠率↔自旋）")
lines.append("")
lines.append("> 脚本：`04_公共成果/算法联盟_全维自洽与归一化/源码/" + SCRIPT_NAME + "`  ")
lines.append("> 上游：`数据/v_eq_c_TUFT_V2prime_修复分支_全维度总结.md`（第 ⑨ 层，"
             "其 S-03 留下一句未算的宿主）→ `判定_TUFT_V2_双分量螺旋驻波孤子_可证伪性审计_2026-09-30.md`"
             "（第 ⑧ 层）  ")
lines.append("> 精度：sympy 4×4 矩阵恒等 + 辅助场配平方 + 量纲指数线性解；mpmath 50 位；常数全部现读载体  ")
lines.append("> 总计 %d 项：%s" % (len(RESULTS), " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
lines.append("")
lines.append("**一句话结论**：挠率的正确耦合对象**是**自旋/轴向流（第 ⑨ 层 S-03 的方向判断对），"
             "但把这个宿主算出来之后，EDM 由 P 宇称禁闭、g-2 欠 " + ns(def_low, 4) + " ~ " +
             ns(def_high, 4) + " 个十年 ⇒ **选对宿主的代价是通道失效**。"
             "本层未提出新方程，也不宣称推进统一场论。")
lines.append("")
lines.append("**判定极性约定**：每行的「判定」判的是**被审主张**（通常属 TUFT/卷十四）成不成立，"
             "不是本脚本措辞的对错 ⇒ `FAIL` 读作「该主张在本层被否证」，"
             "`PASS` 读作「该主张（或本层的复现闸）通过」。`INFO` 只报读数不作判决，"
             "`BOUNDARY` 表示判据本身还没资格下判决。")
lines.append("")
lines.append("## 判决表")
lines.append("")
def md_cell(s):
    """表格单元：换行压平，竖线**转义**成 \\|。

    绝不用 replace('|','/')：那会把 `台账|T_B|²` 之类的标识符悄悄改名（数字对、名字坏），
    而改名后的串在源文件里根本找不到 ⇒ 引用不可回溯。
    """
    return s.replace("\n", " ").replace("|", "\\|")


# 该改名缺陷的夹具：含竖线的单元必须产出转义形，且不得出现斜杠替身
_fx = md_cell("台账|T_B|²")
if _fx != "台账\\|T_B\\|²" or "/" in _fx:
    print("[版面缺陷] 表格单元把竖线改名成了斜杠：" + repr(_fx))
    sys.exit(3)

lines.append("| 编号 | 分支 | 项 | 判定 | 细节 |")
lines.append("|---|---|---|---|---|")
for rr in RESULTS:
    lines.append("| " + rr["id"] + " | " + rr["section"] + " | " + md_cell(rr["item"]) +
                 " | " + rr["verdict"] + " | " + md_cell(rr["detail"]) + " |")
lines.append("")
lines.append("## 关键数（只活在印它的本面里）")
lines.append("")
lines.append("| 量 | 值 | 来源/载体 |")
lines.append("|---|---|---|")
lines.append("| κ = 8πG | " + mp.nstr(kappa_nat, 12) + " GeV^-2 | " +
             os.path.relpath(CONST_FILE, ROOT) + ":" + str(CONST["Ggev"][1]) + " |")
lines.append("| G 由 SI 导出 | " + mp.nstr(Ggev_derived, 12) + " GeV^-2（相对差 " + ns(rel_A, 3) +
             "） | M_Pl=sqrt(ℏc/G)=" + mp.nstr(M_pl, 8) + " kg，E_Pl=" + mp.nstr(E_pl_GeV, 8) + " GeV |")
lines.append("| 路 A η（跨约定） | " + " ~ ".join(mp.nstr(eta_A(m_e_gev)[k], 4) for k in sorted(C0)) +
             " | c₀∈{" + ",".join(sorted(C0)) + "} |")
lines.append("| 路 B η（SI） | " + mp.nstr(eta_B(), 6) + " | 系数幂由 sympy 解 p=" + str(SOL_C) + " |")
lines.append("| 双路 log10 差 | " + mp.nstr(abs(mp.log10(eta_B()) - mp.log10(eA_ref)), 6) +
             " | 十年门 <1 |")
lines.append("| 双路之比（身份） | " + mp.nstr(g04_identity(eta_B(), eA_ref)[1], 8) +
             " 对 1/(4c₀)=" + mp.nstr(g04_identity(eta_B(), eA_ref)[2], 8) +
             " | 相对残差 " + mp.nstr(g04_identity(eta_B(), eA_ref)[0], 3) +
             "（= G-01 的 Ggev 载入相对差，非新误差） |")
lines.append("| 欠账门槛 | " + mp.nstr(DEF_BAR, 2) + " 个十年 | 本轮显式声明；实测下界 " +
             mp.nstr(def_low, 4) + " ⇒ 距门槛 " + mp.nstr(def_low - DEF_BAR, 4) + " |")
lines.append("| G_T/G_F | " + " ~ ".join(mp.nstr(gt_gf[k], 4) for k in sorted(C0)) +
             " | G_F 载 @" + str(CONST["GF"][1]) + " |")
lines.append("| a_e 实验 | " + A_E_E + " | " + os.path.relpath(AE_FILE, ROOT) + ":" +
             str((ANCH["a_e实验值"] or [0])[0]) + " |")
lines.append("| 欠账（十年） | " + " ~ ".join(mp.nstr(deficit(m_e_gev)[k], 4) for k in sorted(C0)) +
             " | log10(a_e)−log10(η) @m_e |")
lines.append("| 同一式在 E_Pl | 欠 " + mp.nstr(min(deficit(E_pl_GeV).values()), 4) + " ~ " +
             mp.nstr(max(deficit(E_pl_GeV).values()), 4) + " 十年 ⇒ 变号 | η=c₀κE_Pl²≈c₀ |")
lines.append("")
lines.append("## 对称性表（机器现算的 P 号，非引用）")
lines.append("")
lines.append("| 双线性量 | P 号 | 锚点期望 |")
lines.append("|---|---|---|")
for nm in sorted(tab):
    lines.append("| " + nm + " | " + str(tab[nm]) + " | " + str(EXPECT.get(nm, "—")) + " |")
lines.append("")
lines.append("## 牙齿")
lines.append("")
lines.append("| 变异体 | 应打红 | 应不红（刻意探针） | 实打红 | 同臂未打红 | 结果 |")
lines.append("|---|---|---|---|---|---|")
for mr in mut_report:
    lines.append("| " + mr["mutant"] + " | " + (",".join(mr["must_redden"]) or "<无>") + " | " +
                 (",".join(mr["must_stay"]) or "<无>") + " | " +
                 (",".join(mr["reddened"]) if mr["reddened"] else "<无>") + " | " +
                 (",".join(mr["not_reddened_by_this_mutant"]) or "<无>") + " | " +
                 ("OK" if mr["clean"] else "BAD") + " |")
lines.append("")
lines.append("变异臂覆盖 " + str(len(armed)) + " / " + str(len(all_row_ids)) + " 行（" +
             ",".join(armed) + "）；**无臂行 " + str(len(unarmed)) + " 行不得当作已被见证**：" +
             ",".join(unarmed) + "。")
lines.append("")
lines.append("## 诚实边界与红线")
lines.append("")
lines.append("- 本层**没有提出新方程**（与 ⑨ 层不同），只判死一条候选通道；哥德巴赫与本册无关。")
lines.append("- 只判**最小耦合** EC；非 minimal 耦合未扫，ξ≠0 的第五力比价未取数（B-03、T-02 ③④）。")
lines.append("- G-06 的欠账门槛在本层显式声明为 " + ns(DEF_BAR, 2) + " 个十年（实测下界 " +
             ns(def_low, 4) + "，距门槛 " + ns(def_low - DEF_BAR, 4) + "），且写成**下界**：接触项移出"
             " a_e 至少还需电磁耦合，本轮未算圈图，故不写「已排除到 10^-45」这种把下界当精确值的措辞。")
lines.append("- C-03 只用 P 宇称；T（时间反演，反幺正）未做机器验证 ⇒ 结论不依赖 T。")
lines.append("- G-02 的两个量纲解差一整幂 c，源于 x⁰=ct 与 x⁰=t 的约定差：**本层不裁约定**，"
             "判据只取十年不变性（G-04）。")
lines.append("- B-01 顺带抓到一处既有档案互斥（EC 报告 §5 与卷十四 §B 对 ω_I(T_B) 给出相反的阻尼归属），"
             "属 S14 §14.8「与 No-Go III/VI 的自洽性核验」（标注「规划（未展开）」）该拦的事。")
lines.append("- 本轮未写 S14 `claims.csv`、未写算法联盟 `README.md`（并发写者持有）⇒ 登记是欠账。")
lines.append("")
lines.append("**红线**：数学自洽 != 物理成立；判死一条路 != 否证 TUFT 本体；"
             "本层的价值是把 ⑨ 层的 S-03 从「方向」变成「带价格的判决」。")
lines.append("")
MD_PATH = os.path.join(OUT_DIR, STEM + ".md")
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("已写出：数据/" + STEM + ".md + .json")

# --- 写后版面闸：未代入的占位符必须由这台尺子能读出来（先自证有牙）---
PH_PAT = "%" + "(?:[sdifr]|[0-9]*\\.[0-9]+[efd])"
PH_RE = re.compile(PH_PAT)


def placeholder_hits(txt):
    return [m.group(0) for m in PH_RE.finditer(txt)]


PCT = chr(37)      # 本文件自建夹具时要造占位符，但源码里不许出现字面 %s（静态尺子会认它）
planted = placeholder_hits("示例：a_e=" + PCT + "s 欠 " + PCT + "d 个十年")
if len(planted) != 2:
    print("[闸失效] 占位符尺子在植入样例上读到 " + str(planted) + "（期望 2 枚）⇒ 它对版面是盲的")
    sys.exit(3)
leaks = placeholder_hits("\n".join(lines))
if leaks:
    print("[版面缺陷] 写出后仍有未代入占位符：" + json.dumps(leaks, ensure_ascii=False))
    sys.exit(3)
print("[版面闸] 占位符 0 处（该尺子在植入样例上现读到 2 枚 ⇒ 有牙）")

# --- 写后版面闸之二：锚点键名不许被表格处理改名（数字对、名字坏＝不可回溯）---
face = open(MD_PATH, encoding="utf-8").read()
renamed = [k for k in NEEDLES if (k not in face) and (md_cell(k) not in face)]
if renamed:
    print("[版面缺陷] 以下锚点键名在版面上找不到原形或转义形（疑似被改名）：" +
          json.dumps(renamed, ensure_ascii=False))
    sys.exit(3)
print("[版面闸] " + str(len(NEEDLES)) + " 个锚点键名在原面上一一可见（原形或转义形）")

print("登记债：本轮未写 S14 claims.csv 与算法联盟 README.md；两者由下一轮现读文件尾接续")
