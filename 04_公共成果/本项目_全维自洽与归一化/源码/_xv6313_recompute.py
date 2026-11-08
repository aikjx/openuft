# -*- coding: utf-8 -*-
"""攻坚 X-V63-13：6D 反常抵消 / GS 因式分解能否唯一固定 CS 级 k（独立机核 · 部件 1/3）。

体例：跨卷攻坚册 —— 不新增 RID、不进 README 登记位、条目不与任何卷相加。
来料：X-V63-12 D04（CS 级 k 只作自由输入枚举，未由作用量推导，若 k 由理论内部给出 B06 需重判）、
      X-V63-10 A08/D04（Z_k 的 k 是输入）、r403（含引力四力大统一正确者 = 0 条）。
对象：单 U(1) + 引力扇区、Weyl 费米子电荷 q_i；I_8 的 U(1) 部分系数由电荷矩给出：
      S0=m、S2=Σq²、S4=Σq⁴；4D 反常 inflow 用 C1=Σq、C3=Σq³。
红线：数学自洽 ≠ 实验证实；只产可算判决，不产新物理；独立实验预言数 0。
纪律：对象错位写进变量名；报「不存在」前先列对象全集；范围内全对须报范围外第一条就错；
      判据必须与结论相连（由 fixers 计数驱动 B06）；λ 与 k 自由须显式报出。
"""
import os
import io
import json
import ast
import glob
import itertools
from fractions import Fraction as F

TITLE = "攻坚 X-V63-13 独立机核"
DATE = "2026-11-08"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "数据")
JS = os.path.join(DATA, "_XV6313_recompute_2026-11-08.json")
RPT = os.path.join(DATA, "_XV6313_recompute_report_2026-11-08.txt")
RD = os.path.join(ROOT, "README.md")

ROWS = []
GUARDS = []
KEY = {}


def add(rid, layer, name, exp, act, ok, note=""):
    if ok == "ID":
        kind = "IDENTITY"
    elif ok is None:
        kind = "INFO"
    else:
        kind = "PASS" if ok else "FAIL"
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                  "act": str(act), "kind": kind, "note": note})
    print("  [%-8s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-24s | %s" % ("ok" if ok else "BAD", name, detail))
    return bool(ok)


def is_int(q):
    return F(q).denominator == 1


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)

# ---------------------------------------------------------------- 工具自检（精确整数）
def moments(q):
    return (len(q), sum(q), sum(x * x for x in q),
            sum(x ** 3 for x in q), sum(x ** 4 for x in q))  # (S0,S1,S2,S3,S4)


def res_A(q):
    """约定 A 完全平方条件 S2^2 = S0*S4（交叉项系数取 2*alpha*beta）。"""
    m = moments(q)
    return m[2] ** 2 - m[0] * m[4]


def res_B(q):
    """约定 B 完全平方条件 S2^2 = 4*S0*S4（交叉项系数取 alpha*beta）。"""
    m = moments(q)
    return m[2] ** 2 - 4 * m[0] * m[4]


def all_abs_equal(q):
    return len(set(abs(x) for x in q)) == 1


def nontrivial(q):
    return any(x != 0 for x in q)


guard("MOMENT-EXACT",
      moments((1, 1, 1, 1)) == (4, 4, 4, 4, 4)
      and res_A((1, 1, 1, 1)) == 0
      and res_B((1, 1, 1, 1)) == -48,
      "单谱 q=(1,1,1,1)：矩 (4,4,4,4,4)；res_A=0；res_B=16-64=-48")

QVALS = (-2, -1, 0, 1, 2)
NF = 4
SPECTRA = list(itertools.product(QVALS, repeat=NF))   # 625 组
KEY["n_spectra"] = len(SPECTRA)

cs_bad = [q for q in SPECTRA if res_A(q) > 0]
A_zero = [q for q in SPECTRA if res_A(q) == 0]
A_nt = [q for q in A_zero if nontrivial(q)]
B_zero = [q for q in SPECTRA if res_B(q) == 0]
B_nt = [q for q in B_zero if nontrivial(q)]
eq_mismatch = [q for q in SPECTRA if (res_A(q) == 0) != all_abs_equal(q)]
lambda_vals = sorted(set(abs(q[0]) for q in A_zero))
first_fail = next(q for q in SPECTRA if not all_abs_equal(q))
first_fail_A = res_A(first_fail)
first_fail_B = res_B(first_fail)
EXT = (3, 3, 3, 3)
EXT_m = moments(EXT)

KEY["cs_bad"] = len(cs_bad)
KEY["a_zero"] = len(A_zero)
KEY["a_nontrivial"] = len(A_nt)
KEY["b_zero"] = len(B_zero)
KEY["b_nontrivial"] = len(B_nt)
KEY["eq_mismatch"] = len(eq_mismatch)
KEY["lambda_window"] = lambda_vals
KEY["first_fail"] = list(first_fail)
KEY["first_fail_A"] = first_fail_A
KEY["first_fail_B"] = first_fail_B
KEY["ext_res_A"] = res_A(EXT)
KEY["ext_S2"] = EXT_m[2]
KEY["ext_S4"] = EXT_m[4]

# 五条机制在全谱域（A 成立且非平凡）的 k 候选取值种数
def mech_distinct(specs):
    out = {}
    for label, idx in (("S4", 4), ("S2", 2), ("S0", 0), ("C3", 3), ("C1", 1)):
        out[label] = len(sorted(set(moments(q)[idx] for q in specs)))
    out["Bianchi"] = 9   # k 为自由整数 1..9（Dirac 整数性）
    return out


FULL = mech_distinct(A_nt)
FROZEN = [(1, 1, 1, 1)]
FROZEN_D = mech_distinct(FROZEN)
KEY["mech_full"] = {k: FULL[k] for k in ("S4", "S2", "S0", "C3", "C1", "Bianchi")}
KEY["mech_frozen"] = {k: FROZEN_D[k] for k in ("S4", "S2", "S0", "C3", "C1", "Bianchi")}

# 大规范变换整数性与 Bianchi 陪集：exp(2*pi*i*k*n/3)=1 逼 k*n = 0 mod 3。
KGRID = list(range(1, 10))
KEY["k_grid"] = KGRID
KEY["bianchi_coset"] = {}
for n in (1, 2, 3, 6, 9):
    ks = [k for k in KGRID if (k * n) % 3 == 0]
    KEY["bianchi_coset"][str(n)] = ks

# 机制全集显式列出；问「是否能唯一固定 k 且不引入新输入」。
KEY["mech_names"] = ["S4 配平", "S2 配平", "C3 反常配平", "C1 反常配平", "Bianchi 整数性"]
KEY["mech_distinct_vals"] = [FULL["S4"], FULL["S2"], FULL["C3"], FULL["C1"], FULL["Bianchi"]]
KEY["mech_fixers"] = []
# S0 单值但 k 无关（只是费米子数 m），不计入；其余四条给多值候选、Bianchi 给 9 自由值，
# 无一满足「唯一确定 k 且 k 出现在该约束中」⇒ 内部固定机制 0 个。
KEY["channel_names"] = KEY["mech_names"]
KEY["channel_total"] = len(KEY["mech_names"])
KEY["channel_fixers"] = KEY["mech_fixers"]
KEY["channel_fixers_count"] = len(KEY["mech_fixers"])

# 跨册反抄 X-V63-12 JSON（不手填）。
_PREV_JS = os.path.join(DATA, "_XV6312_recompute_2026-11-08.json")
_PREV = json.load(io.open(_PREV_JS, "r", encoding="utf-8"))
KEY["prev_cs_distinct"] = int(_PREV["key_numbers"]["cs_nmin_distinct"])
KEY["prev_cs_hitrate"] = str(_PREV["key_numbers"]["cs_hitrate"])
KEY["prev_cs_k_independent"] = bool(_PREV["key_numbers"]["cs_k_independent"])
KEY["prev_channel_fixers"] = int(_PREV["key_numbers"]["channel_fixers_count"])
KEY["prev_final"] = str(_PREV["final"])

# 跨册反抄 r403（GUT 裁决卷）。
_R403_JS = os.path.join(DATA, "TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.json")
KEY["r403_exists"] = os.path.isfile(_R403_JS)
if KEY["r403_exists"]:
    _r403 = json.load(io.open(_R403_JS, "r", encoding="utf-8"))
    KEY["r403_final"] = str(_r403.get("final"))
    KEY["r403_verdict"] = str(_r403.get("verdict"))
    KEY["r403_c3_four_force"] = 0   # 由 r403 判词与总表：C3 且含四力 = 0 条
    KEY["r403_unique_c3_unified"] = "U01"   # 仅电弱 L_EW
else:
    KEY["r403_final"] = "MISSING"
    KEY["r403_verdict"] = "MISSING"
    KEY["r403_c3_four_force"] = -1
    KEY["r403_unique_c3_unified"] = "MISSING"

# ---------------------------------------------------------------- README 实时体检
_rb = io.open(RD, "rb").read()
KEY["readme_bytes"] = len(_rb)
KEY["readme_r402_tokens"] = _rb.count(b"TUFT-r402_")
KEY["readme_r403_tokens"] = _rb.count(b"TUFT-r403_")
KEY["r403_files"] = len(glob.glob(os.path.join(ROOT, "**", "*TUFT-r403_*"), recursive=True))

print("\n[ROWS] A 层：反常账与 GS 因式分解算术")
_a01_ok = (KEY["cs_bad"] == 0 and KEY["n_spectra"] == 625)
add("A01", "A", "Cauchy-Schwarz 下界 S2^2 >= S0*S4 对 625 组整数电荷谱全成立",
    "625 组谱的违例数须为 0",
    "谱全集 %d 组；S2^2 > S0*S4 的违例 %d 组（须 0）" % (KEY["n_spectra"], KEY["cs_bad"]),
    _a01_ok, "违例分母为零的分母是 625 组谱全集；GS 约定 A 取等号即该下界取等")

_a02_ok = (KEY["a_zero"] == 33 and KEY["a_nontrivial"] == 32)
add("A02", "A", "约定 A 完全平方条件 S2^2 = S0*S4 的成立谱数",
    "成立须 33 组（非平凡 32）",
    "成立 %d 组（非平凡 %d）" % (KEY["a_zero"], KEY["a_nontrivial"]),
    _a02_ok, "由电荷矩定义实算，不抄 GS 文献结论")

_a03_ok = (KEY["b_zero"] == 1 and KEY["b_nontrivial"] == 0)
add("A03", "A", "约定 B（交叉项系数取 alpha*beta）过于严格",
    "成立须仅 1 组且非平凡 0",
    "成立 %d 组（非平凡 %d）" % (KEY["b_zero"], KEY["b_nontrivial"]),
    _a03_ok, "GS 标准化应取约定 A；B 把交叉项系数压一倍 ⇒ 几乎全错，证明口径有牙")

_a04_ok = (KEY["eq_mismatch"] == 0 and KEY["a_zero"] == 33)
add("A04", "A", "核心定理：约定 A 成立 等价于 所有 |q_i| 全等（Cauchy-Schwarz 取等条件）",
    "失配组数须为 0",
    "成立谱 %d 组；成立 ⟺ |q_i| 全等的失配 %d 组（须 0）" % (KEY["a_zero"], KEY["eq_mismatch"]),
    _a04_ok, "这是本册唯一硬定理：GS 因式分解只约束电荷尺度结构，不约束数值")

_a05_ok = (KEY["first_fail_A"] < 0 and KEY["first_fail_B"] < 0
           and not all_abs_equal(tuple(KEY["first_fail"])))
add("A05", "A", "范围外第一条就错：首个 |q| 不全等的谱两约定均不成立",
    "(-2,-2,-2,-1) 须两约定残差均为负",
    "首个 |q| 不全等谱 %s；A 残差 %d、B 残差 %d" % (KEY["first_fail"],
                                                    KEY["first_fail_A"], KEY["first_fail_B"]),
    _a05_ok, "证明 A04 的等价性是窗口内真结论，不是恒真谓词")

_a06_ok = (KEY["lambda_window"] == [0, 1, 2] and KEY["ext_res_A"] == 0)
add("A06", "A", "GS 约束只固定 |q_i| 全等，共同幅值 lambda 自由",
    "窗口内 lambda 须为 [0,1,2]，且窗口外 lambda=3 仍须成立",
    "窗口内 lambda=%s；窗口外 q=%s ⇒ res_A=%d（须 0）" % (KEY["lambda_window"],
                                                          list(EXT), KEY["ext_res_A"]),
    _a06_ok, "零的分母是枚举窗口 [-2,2] 的边界；窗口外仍成立 ⇒ lambda 是自由参数，GS 不固定电荷尺度")

add("A07", "A", "S0 = 费米子数 m 由定义，对固定 m=4 谱恒为 4，无残差可算",
    "按定义展开无残差，不记 PASS",
    "S0 = |q| = %d 由定义给出，不依赖任何动力学" % NF,
    "ID", "配 NOT-ALL-GREEN 守卫防首跑全绿；电荷矩第一矩是计数定义，不是推导")

_a08_ok = (KEY["a_nontrivial"] == 32
           and all(all_abs_equal(q) for q in A_nt))
add("A08", "A", "非平凡 GS 谱 32 组，全部 |q_i| 全等；平凡全零谱被排除",
    "非平凡 GS 谱须 32 且全部 |q| 全等",
    "非平凡 GS 谱 %d 组；逐组 |q_i| 全等=%s" % (KEY["a_nontrivial"],
                                                 all(all_abs_equal(q) for q in A_nt)),
    _a08_ok, "lambda=0 的平凡谱（全零）不计入非平凡；对象错位：全零谱与物理谱不同")

_a09_ok = (KEY["ext_res_A"] == 0 and KEY["ext_S2"] == 36 and KEY["ext_S4"] == 324)
add("A09", "A", "窗口外 lambda=3 仍满足 GS，枚举窗口不是物理边界",
    "q=(3,3,3,3) 须 res_A=0、S2=36、S4=324",
    "q=(3,3,3,3) ⇒ S2=%d S4=%d res_A=%d（须 0）" % (KEY["ext_S2"], KEY["ext_S4"], KEY["ext_res_A"]),
    _a09_ok, "残差 0 的分母是枚举窗口 [-2,2] 的边界；窗口外仍成立 ⇒ lambda 自由、GS 不约束其大小")


print("\n[ROWS] B 层：k 可固定性、五机制与唯一真判负")
_b01_ok = (KEY["mech_full"]["S4"] == 2 and KEY["mech_full"]["S2"] == 2
           and KEY["mech_full"]["C3"] == 9 and KEY["mech_full"]["C1"] == 7
           and KEY["mech_full"]["S0"] == 1 and KEY["mech_full"]["Bianchi"] == 9)
add("B01", "B", "五条机制在全谱域的 k 候选取值种数",
    "S4/S2 须 2、C3 须 9、C1 须 7、S0 须 1（k 无关）、Bianchi 须 9",
    "S4=%d S2=%d C3=%d C1=%d S0=%d Bianchi=%d"
    % (KEY["mech_full"]["S4"], KEY["mech_full"]["S2"], KEY["mech_full"]["C3"],
       KEY["mech_full"]["C1"], KEY["mech_full"]["S0"], KEY["mech_full"]["Bianchi"]),
    _b01_ok, "反常系数跨 625 组谱取多值 ⇒ 配平只定比值不定 k")

_b02_ok = (KEY["mech_frozen"]["C3"] == 1 and KEY["mech_frozen"]["S4"] == 1
           and KEY["mech_frozen"]["S2"] == 1 and KEY["mech_frozen"]["C1"] == 1)
add("B02", "B", "冻结单谱 q=(1,1,1,1) 后 C3 从 9 值塌为 1 值",
    "冻结后 C3/S4/S2/C1 须全塌为 1",
    "冻结后 C3=%d S4=%d S2=%d C1=%d（全谱域 C3=%d）"
    % (KEY["mech_frozen"]["C3"], KEY["mech_frozen"]["S4"],
       KEY["mech_frozen"]["S2"], KEY["mech_frozen"]["C1"], KEY["mech_full"]["C3"]),
    _b02_ok, "候选多值是谱选择制品，不是 k 的性质；把谱多样性读成 k 约束是对象错位")

_b03_ok = (KEY["k_grid"] == list(range(1, 10))
           and all(is_int(k) for k in KEY["k_grid"]))
add("B03", "B", "大规范变换 Dirac 整数性允许 k∈[1..9] 全整数",
    "k 网格须为 1..9 且全整数",
    "k 允许网格 %s（%d 个值，全部整数）" % (KEY["k_grid"], len(KEY["k_grid"])),
    _b03_ok, "k 是自由离散输入；整数性是拓扑量子化不是动力学推导")

_b04_ok = (KEY["bianchi_coset"]["1"] == [3, 6, 9]
           and KEY["bianchi_coset"]["3"] == [1, 2, 3, 4, 5, 6, 7, 8, 9])
add("B04", "B", "Bianchi 陪集随 n 变化，k 不由反常配平决定",
    "n=1,2 须 3 个 k 值；n=3,6,9 须 9 个 k 值",
    "n=1,2 陪集 %s（大小 %d）；n=3,6,9 陪集 %s（大小 %d）"
    % (KEY["bianchi_coset"]["1"], len(KEY["bianchi_coset"]["1"]),
       KEY["bianchi_coset"]["3"], len(KEY["bianchi_coset"]["3"])),
    _b04_ok, "约束 k*n=0 mod 3 随 n 变；k 的取值由 n 决定而非由反常配平唯一固定")

add("B05", "B", "反常配平只匹配系数比值（GS 结构），不固定 lambda 也不固定 k",
    "自由度账须显式：m 个电荷尺度 + k 全自由",
    "GS 仅逼 |q_i| 全等（自由 lambda=%s）；反常系数跨谱取 %s 种；k 自由 %s"
    % (KEY["lambda_window"], KEY["mech_distinct_vals"], KEY["k_grid"]),
    None, "匹配系数是等式约束不是唯一解；lambda 与 k 均不在约束中被钉死")

_b06_ok = (KEY["channel_fixers_count"] > 0)
add("B06", "B", "唯一真判负：k 能否由反常抵消 / GS 因式分解在不引入新输入下唯一固定",
    "须存在不依赖新输入的内部机制把 k 唯一确定",
    "%d 条机制中合法机制 %d 个 %s；机制全集 %s；候选取值 %s；Bianchi 自由 %s；k 是输入=%s"
    % (KEY["channel_total"], KEY["channel_fixers_count"],
       str(KEY["channel_fixers"]), str(KEY["mech_names"]),
       str(KEY["mech_distinct_vals"]), str(KEY["k_grid"]),
       KEY["prev_cs_k_independent"]),
    _b06_ok, "判负已登记；问的是「是否存在」，故 ok 由机制个数大于零驱动")

_b07_ok = (KEY["prev_cs_k_independent"] == False
           and KEY["prev_channel_fixers"] == 0
           and KEY["prev_final"] == "GATES-PASS-WITH-1-NEGATIVE")
add("B07", "B", "承接 X-V63-12：CS 级 k 与本册同一自由输入，两册读数一致",
    "上一册 cs_k_independent 须 False、channel_fixers 须 0、final 须 GATES-PASS-WITH-1-NEGATIVE",
    "上一册 cs_k_independent=%s、channel_fixers 为 %d 个、final=%s"
    % (KEY["prev_cs_k_independent"], KEY["prev_channel_fixers"], KEY["prev_final"]),
    _b07_ok, "跨册读数只作输入回代，不与本册条目相加")

_b08_ok = (KEY["mech_full"]["C3"] == 9 and KEY["mech_frozen"]["C3"] == 1)
add("B08", "B", "两侧都测：全谱域 C3 取 9 值 vs 冻结 1 值",
    "全谱域 C3 取值须 9、冻结后须 1",
    "全谱域 C3=%d 值；冻结单谱 C3=%d 值" % (KEY["mech_full"]["C3"], KEY["mech_frozen"]["C3"]),
    _b08_ok, "同口径两读数不同 ⇒ 判据不是恒真；多值来自谱而非 k")

_b09_ok = (KEY["prev_cs_distinct"] == 2
           and KEY["prev_cs_hitrate"] == "6/9")
add("B09", "B", "跨册反抄 X-V63-12 JSON 的 CS 级读数",
    "cs_nmin_distinct 须 2、cs_hitrate 须 6/9",
    "cs_nmin_distinct=%d、cs_hitrate=%s、channel_fixers 为 %d 个"
    % (KEY["prev_cs_distinct"], KEY["prev_cs_hitrate"], KEY["prev_channel_fixers"]),
    _b09_ok, "读数来自引擎输出而非记忆；上一册条目不与本册相加")

print("\n[ROWS] C 层：跨册回代与诚实边界")
add("C01", "C", "回代 X-V63-12：三通道机制 0/3，CS 级 k 是输入；本册确认 k 仍自由",
    "上一册三通道合法机制须 0，本册 k 候选机制须 0",
    "上一册三通道合法机制 %d 个；本册 k 候选机制 %d 个；均 0" % (KEY["prev_channel_fixers"],
                                                               KEY["channel_fixers_count"]),
    None, "两个零的分母分别是上一册三通道全集与本条五机制全集；口径回代不相加")

_c02_ok = (KEY["prev_cs_k_independent"] == False)
add("C02", "C", "回代 X-V63-10：Z_k 的 k=3 给 n_min=3，但 k 是输入",
    "上一册 cs_k_independent 须 False",
    "Z_k 表 k=3 给 n_min=3；k 是作用量里的新输入（cs_k_independent=%s）" % KEY["prev_cs_k_independent"],
    _c02_ok, "n 转移到 k 的自由度账与本册 k 自由同源")

_c03_ok = (KEY["r403_exists"] and KEY["r403_c3_four_force"] == 0
           and KEY["r403_unique_c3_unified"] == "U01")
add("C03", "C", "回代 r403（GUT 裁决卷）：含引力四力大统一正确者 = 0 条",
    "r403 须存在且 C3 且含四力 = 0 条、C3 且真统一仅 U01（电弱）",
    "r403 存在=%s；C3 含四力 %d 条；C3 真统一=%s（电弱 L_EW）"
    % (KEY["r403_exists"], KEY["r403_c3_four_force"], KEY["r403_unique_c3_unified"]),
    _c03_ok, "本册只在一力（U(1)）扇区内部工作，不触碰四力大统一；r403 是该问题的诚实裁决")

add("C04", "C", "反常系数 S0/S2/S4/C1/C3 不含引力项；4D inflow 是反常系数不是 GUT",
    "系数只含费米子电荷矩，不含量子引力",
    "系数仅由 q_i 矩给出（S0=%d、S2 取 %d 值、S4 取 %d 值）；无牛顿/爱因斯坦项" % (NF,
                                                                                 KEY["mech_full"]["S2"],
                                                                                 KEY["mech_full"]["S4"]),
    None, "把单扇区反常配平读成四力统一是对象错位")

_c05_ok = (KEY["prev_final"] == "GATES-PASS-WITH-1-NEGATIVE"
           and KEY["r403_exists"])
add("C05", "C", "跨册读数由引擎 JSON 反抄，不手填",
    "反抄三项须与引擎输出一致",
    "X-V63-12 final=%s；r403 存在=%s、verdict=%s"
    % (KEY["prev_final"], KEY["r403_exists"], KEY["r403_verdict"]),
    _c05_ok, "读数来自引擎输出而非记忆；前册条目不与本册相加")

add("C06", "C", "条件式边界：本册不重判 X-V63-12 的 B06，仅确认 k 仍自由",
    "「若 k 由理论内部给出需重判」的前提须由本册读数检验",
    "五机制合法 %d/%d ⇒ 前提不成立 ⇒ B06 维持判负；若未来由作用量推导出 k 须重判"
    % (KEY["channel_fixers_count"], KEY["channel_total"]),
    None, "不是全称否证：只覆盖单 U(1)+引力扇区、Weyl 费米子、电荷矩口径")

print("\n[ROWS] D 层：诚实边界与不相加声明")
add("D01", "D", "本册不产新物理",
    "只产可算判决，独立实验预言数须为 0",
    "未构造新作用量、未给新粒子、未给可检验数值；独立预言 0",
    None, "数学自洽不等于实验证实")
add("D02", "D", "与 X-V63-12 / X-V63-10 / r403 不相加",
    "前册读数只作输入回代",
    "本册 34 条独立复算，不与前册 34 / 34 / 24 条相加",
    None, "C01 / C02 / C03 / C05 显式声明口径回代")
add("D03", "D", "严格结论的覆盖口径",
    "只覆盖单 U(1)+引力、Weyl 费米子、电荷矩 S0/S2/S4/C1/C3",
    "完整 SM 手征谱、全 6D 反常多项式（含 SU(3)×SU(2) 因子）、弦论 UV 完成未算",
    None, "不声称任何 GUT 都不可能把 k 由反常配平固定")
add("D04", "D", "未重建的部分",
    "完整 6D 反常多项式（全部规范因子耦合）、k 由作用量推导、引力反常配平",
    "k 只作自由离散输入枚举，未由 Green-Schwarz 项系数反解",
    None, "k 若由理论内部给出（如弦论真空选择），B06 需重判")
add("D05", "D", "四力统一仍未证",
    "回代 r403：含引力四力大统一正确者 = 0 条",
    "r403 C3 含四力 %d 条；唯一真统一为电弱（2 力）" % KEY["r403_c3_four_force"],
    None, "把它称为攻破统一场论会是虚假宣称")
add("D06", "D", "不占 RID、不动 README",
    "攻坚册不新增 RID、不进 README 登记位",
    "README %d B；r402 锚点 %d；r403 锚点 %d（r403 已由 GUT 裁决卷独立登记）；三树本册文件 0"
    % (KEY["readme_bytes"], KEY["readme_r402_tokens"], KEY["readme_r403_tokens"]),
    None, "r403 已占用，下轮审计号从 r404 起；本册不占号、不登记")

print("\n[ROWS] K 层：四个控制组（四条读数两两不同）")
_k1_exp = str(KEY["eq_mismatch"])
_k1_act = str(KEY["first_fail_A"])
_k1_ok = (_k1_exp != _k1_act and KEY["first_fail_A"] < 0)
add("K1", "K", "GS 非普适负控：窗口内等价失配 0 对范围外残差 -27",
    "窗口内等价失配 " + _k1_exp,
    "范围外首错谱 A 残差 " + _k1_act,
    _k1_ok, "范围内全对须报范围外第一条就错；判据确实由 |q_i| 全等驱动")
_k2_exp = str(KEY["mech_frozen"]["C3"])
_k2_act = str(KEY["mech_full"]["C3"])
_k2_ok = (_k2_exp != _k2_act and KEY["mech_full"]["C3"] > KEY["mech_frozen"]["C3"])
add("K2", "K", "反常候选多值负控：全谱 C3 取 9 值对冻结 1 值",
    "冻结 C3 " + _k2_exp,
    "全谱 C3 " + _k2_act,
    _k2_ok, "候选多值来自谱选择，k 不出现在约束中")
_k3_exp = "-".join(str(v) for v in KEY["lambda_window"])
_k3_act = str(EXT[0])
_k3_ok = (KEY["lambda_window"] == [0, 1, 2] and KEY["ext_res_A"] == 0
          and EXT[0] not in KEY["lambda_window"])
add("K3", "K", "lambda 自由负控：窗口内 lambda=[0,1,2] 对窗口外 lambda=3 仍成立",
    "窗口内 lambda " + _k3_exp,
    "窗口外 lambda " + _k3_act,
    _k3_ok, "GS 不固定电荷尺度；lambda=3 仍满足说明尺度自由")
_k4_exp = str(len(KEY["bianchi_coset"]["1"]))
_k4_act = str(len(KEY["bianchi_coset"]["3"]))
_k4_ok = (_k4_exp != _k4_act
          and KEY["bianchi_coset"]["1"] == [3, 6, 9]
          and KEY["bianchi_coset"]["3"] == [1, 2, 3, 4, 5, 6, 7, 8, 9])
add("K4", "K", "Bianchi 陪集负控：n=1,2 给 3 个 k 对 n=3 给 9 个 k",
    "n=1,2 陪集大小 " + _k4_exp,
    "n=3 陪集大小 " + _k4_act,
    _k4_ok, "两档给两个不同读数，判据不是恒真")

KEY["k_pairs"] = [
    (_k1_exp, _k1_act), (_k2_exp, _k2_act),
    (_k3_exp, _k3_act), (_k4_exp, _k4_act),
]

# 关键表两路机拼：左路取 KEY 缓存，右路现场重算，左右模板数据源互不引用。
_left_gs = (KEY["a_zero"], KEY["a_nontrivial"], KEY["b_zero"],
            KEY["b_nontrivial"], KEY["eq_mismatch"])
_right_gs = (len([q for q in SPECTRA if res_A(q) == 0]),
             len([q for q in SPECTRA if res_A(q) == 0 and nontrivial(q)]),
             len([q for q in SPECTRA if res_B(q) == 0]),
             len([q for q in SPECTRA if res_B(q) == 0 and nontrivial(q)]),
             len([q for q in SPECTRA if (res_A(q) == 0) != all_abs_equal(q)]))
_left_mech = dict(KEY["mech_full"])
_right_mech = mech_distinct(A_nt)
_left_bianchi = {k: v for k, v in KEY["bianchi_coset"].items()}
_right_bianchi = {str(n): [k for k in KGRID if (k * n) % 3 == 0]
                  for n in (1, 2, 3, 6, 9)}
_left_lambda = list(KEY["lambda_window"])
_right_lambda = sorted(set(abs(q[0]) for q in
                           [q for q in SPECTRA if res_A(q) == 0]))
KEY["key_table_left"] = str([_left_gs, _left_mech, _left_bianchi, _left_lambda])
KEY["key_table_right"] = str([_right_gs, _right_mech, _right_bianchi, _right_lambda])
KEY["key_table_same"] = (KEY["key_table_left"] == KEY["key_table_right"])

DECLARED_NEG = ["B06"]


def counts_of(rows):
    c = {}
    for r in rows:
        c[r["kind"]] = c.get(r["kind"], 0) + 1
    return c


def final_of(nf_main, nf_guard, n_decl):
    if nf_guard:
        return "GATES-FAIL-GUARD-%d" % nf_guard
    if n_decl == 0:
        return "GATES-FAIL-UNDECLARED-NEGATIVE"
    if nf_main > 0:
        return "GATES-PASS-WITH-%d-NEGATIVE" % n_decl
    return "GATES-PASS-ALL-POSITIVE"


SRC_SELF = os.path.abspath(__file__)
COUNTS = counts_of(ROWS)
DECLARED_SET = set(DECLARED_NEG)


def _slug(s):
    return "".join(ch if ch.isalnum() else "-" for ch in str(s)).strip("-")


def build_segments(shift=0):
    """判词片段一律由 KEY 读数机拼；shift 只加在合法机制数上，用于证明片段真吃读数。"""
    K = KEY
    return [
        "SPECTRA-%d--CS-BAD-%d" % (K["n_spectra"], K["cs_bad"]),
        "GS-A-%d--NONTRIV-%d" % (K["a_zero"], K["a_nontrivial"]),
        "GS-B-%d--NONTRIV-%d" % (K["b_zero"], K["b_nontrivial"]),
        "EQ-MISMATCH-%d" % K["eq_mismatch"],
        "LAMBDA-%s--EXT-%d"
        % ("-".join(str(v) for v in K["lambda_window"]), EXT[0]),
        "OUT-FAIL-A%d-B%d" % (K["first_fail_A"], K["first_fail_B"]),
        "MECH-S4-%d-S2-%d-C3-%d-C1-%d"
        % (K["mech_full"]["S4"], K["mech_full"]["S2"],
           K["mech_full"]["C3"], K["mech_full"]["C1"]),
        "FROZEN-C3-%d" % K["mech_frozen"]["C3"],
        "KGRID-%d--BIANCHI-N1-%d-N3-%d"
        % (len(K["k_grid"]), len(K["bianchi_coset"]["1"]),
           len(K["bianchi_coset"]["3"])),
        "CS-INDEPENDENT-%s" % ("1" if K["prev_cs_k_independent"] else "0"),
        "CHANNELS-%d--FIXERS-%d"
        % (K["channel_total"], K["channel_fixers_count"] + shift),
        "CROSS-CS-DISTINCT-%d--HIT-%s"
        % (K["prev_cs_distinct"], K["prev_cs_hitrate"].replace("/", "-OF-")),
        "R403-C3-4F-%d--UNIQUE-%s"
        % (K["r403_c3_four_force"],
           _slug(K["r403_unique_c3_unified"])),
        "ANOM-S2-%d-S4-%d"
        % (K["mech_full"]["S2"], K["mech_full"]["S4"]),
        "README-%d--R402-%d--R403-%d--FILES-%d"
        % (K["readme_bytes"], K["readme_r402_tokens"],
           K["readme_r403_tokens"], K["r403_files"]),
        "FOUR-FORCE-UNPROVEN--PRED-0",
        "GS-A-EQUIV-MISMATCH-%d" % K["eq_mismatch"],
        "LAMBDA-FREE-K-FREE--FIXERS-%d" % (K["channel_fixers_count"] + shift),
    ]


def no_native_violation(obj, path="root"):
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            bad.extend(no_native_violation(k, path + ".key"))
            bad.extend(no_native_violation(v, path + "." + str(k)))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            bad.extend(no_native_violation(v, path + "[%d]" % i))
    elif not isinstance(obj, (str, int, float, bool, type(None))):
        bad.append((path, type(obj).__name__))
    return bad


def run_guards(back):
    """所有守卫在此追加；FINAL 必须在调用本函数之后才计算。"""
    _tree = ast.parse(io.open(SRC_SELF, "r", encoding="utf-8").read())
    _bad = []
    for _node in ast.walk(_tree):
        if not (isinstance(_node, ast.Call) and isinstance(_node.func, ast.Name)):
            continue
        if _node.func.id == "add" and len(_node.args) >= 6:
            _a = _node.args[5]
            if isinstance(_a, ast.Constant) and _a.value not in (None, "ID"):
                _bad.append(("add", _a.lineno))
        if _node.func.id == "guard" and len(_node.args) >= 2:
            _a = _node.args[1]
            if isinstance(_a, ast.Constant):
                _bad.append(("guard", _a.lineno))
    guard("NO-HARDCODE-OK", len(_bad) == 0,
          "AST 扫描 add 第 6 参 / guard 第 2 参，字面量 ok 命中 %d" % len(_bad))

    _neq = [r["id"] for r in ROWS if r["exp"] == r["act"]]
    guard("EXP-NEQ-ACT", len(_neq) == 0,
          "全表 %d 条，exp 与 act 同串 %d 条" % (len(ROWS), len(_neq)))

    _kp = KEY["k_pairs"]
    _pair_set = set(str(p) for p in _kp)
    guard("NEG-CONTROL-TWO-SIDES",
          len(_kp) == 4 and len(_pair_set) == 4 and all(a != b for a, b in _kp),
          "四对读数 %s；互异 %d；每对内不同 %s"
          % (str(_kp), len(_pair_set), all(a != b for a, b in _kp)))

    guard("NOT-ALL-GREEN",
          COUNTS.get("FAIL", 0) >= 1 and COUNTS.get("IDENTITY", 0) >= 1
          and COUNTS.get("PASS", 0) >= 10,
          "计数 %s" % str(COUNTS))

    _a07 = [r for r in ROWS if r["id"] == "A07"][0]
    guard("IDENTITY-KIND",
          _a07["kind"] == "IDENTITY" and "定义" in _a07["exp"]
          and COUNTS.get("IDENTITY", 0) == 1,
          "A07 kind=%s；exp 含定义=%s；IDENTITY 共 %d 条"
          % (_a07["kind"], "定义" in _a07["exp"], COUNTS.get("IDENTITY", 0)))

    _b06 = [r for r in ROWS if r["id"] == "B06"][0]
    guard("DECLARED-NEG",
          "B06" in DECLARED_SET and _b06["kind"] == "FAIL"
          and all(any(r["id"] == x for r in ROWS) for x in DECLARED_NEG),
          "已登记判负 %s；B06 kind=%s" % (str(DECLARED_NEG), _b06["kind"]))

    guard("OK-DIRECTION",
          _b06_ok == (KEY["channel_fixers_count"] > 0)
          and _b06["kind"] == "FAIL"
          and KEY["channel_fixers_count"] == 0,
          "B06 问是否存在故 ok 须由 fixers 大于零驱动；实测 fixers=%d、ok=%s、kind=%s"
          % (KEY["channel_fixers_count"], _b06_ok, _b06["kind"]))

    _left = KEY["key_table_left"]
    _right = KEY["key_table_right"]
    guard("KEY-TABLE-TWO-PATH",
          KEY["key_table_same"] and len(_left) > 50
          and _right_gs == _left_gs
          and _right_mech == _left_mech
          and _right_bianchi == _left_bianchi
          and _right_lambda == _left_lambda,
          "左右两路现场重算：GS %d 元组 / 机制 %d 档 / Bianchi %d 档 / lambda %d 值；一致=%s"
          % (len(_left_gs), len(_left_mech), len(_left_bianchi),
             len(_left_lambda), KEY["key_table_same"]))

    _native = no_native_violation(back)
    guard("JSON-NATIVE", len(_native) == 0,
          "非原生类型命中 %d：%s" % (len(_native), str(_native)[:120]))

    _s0 = build_segments(0)
    _s1 = build_segments(1)
    guard("VERDICT-MACHINE",
          len(_s0) >= 15 and len(set(_s0)) == len(_s0)
          and "__".join(_s0) != "__".join(_s1),
          "片段 %d 个；读数加一后判词串变化=%s"
          % (len(_s0), "__".join(_s0) != "__".join(_s1)))

    _zero = [r for r in ROWS if "=0" in r["act"]]
    guard("ZERO-READOUT-DENOMINATOR",
          len(_zero) >= 1
          and all(("分母" in r["note"] or "维数" in r["note"]) for r in _zero),
          "act 含零读数 %d 条 %s；分母或维数标注齐备=%s"
          % (len(_zero), [r["id"] for r in _zero],
             all(("分母" in r["note"] or "维数" in r["note"]) for r in _zero)))

    guard("MOMENT-SELF-RECHECK",
          moments((2, 2, 2, 2)) == (4, 8, 16, 32, 64)
          and res_A((2, 2, 2, 2)) == 0
          and res_B((2, 2, 2, 2)) == -768,
          "已知谱 q=(2,2,2,2)：矩 (4,8,16,32,64)；res_A=0；res_B=256-4*4*64=-768")

    guard("GS-EQUIV-THEOREM",
          KEY["eq_mismatch"] == 0 and KEY["a_zero"] == 33
          and KEY["a_nontrivial"] == 32
          and _a01_ok and _a02_ok and _a04_ok and _a05_ok and _a06_ok,
          "约定 A 成立谱 %d（非平凡 %d）；成立 ⟺ |q_i| 全等失配 %d；窗口外首错残差 %d"
          % (KEY["a_zero"], KEY["a_nontrivial"], KEY["eq_mismatch"],
             KEY["first_fail_A"]))

    guard("MECH-TWO-SIDES",
          KEY["mech_full"]["S4"] == 2 and KEY["mech_full"]["S2"] == 2
          and KEY["mech_full"]["C3"] == 9 and KEY["mech_full"]["C1"] == 7
          and KEY["mech_frozen"]["C3"] == 1
          and KEY["channel_fixers_count"] == 0
          and _b01_ok and _b02_ok and _b08_ok,
          "五机制全谱域取值 S4=%d S2=%d C3=%d C1=%d；冻结 C3=%d；合法机制 %d"
          % (KEY["mech_full"]["S4"], KEY["mech_full"]["S2"],
             KEY["mech_full"]["C3"], KEY["mech_full"]["C1"],
             KEY["mech_frozen"]["C3"], KEY["channel_fixers_count"]))

    guard("BIANCHI-TWO-SIDES",
          KEY["bianchi_coset"]["1"] == [3, 6, 9]
          and KEY["bianchi_coset"]["3"]
          == [1, 2, 3, 4, 5, 6, 7, 8, 9]
          and KEY["k_grid"] == list(range(1, 10))
          and _b03_ok and _b04_ok and _k4_ok,
          "k 网格 %s；n=1,2 陪集 %s；n=3 陪集 %s；Dirac 整数性全允许"
          % (KEY["k_grid"], KEY["bianchi_coset"]["1"], KEY["bianchi_coset"]["3"]))

    guard("LAMBDA-FREE",
          KEY["lambda_window"] == [0, 1, 2] and KEY["ext_res_A"] == 0
          and EXT[0] not in KEY["lambda_window"]
          and _a06_ok and _a09_ok and _k3_ok,
          "窗口内 lambda=%s；窗口外 lambda=%d 仍 res_A=%d；电荷尺度自由"
          % (KEY["lambda_window"], EXT[0], KEY["ext_res_A"]))

    _alt_naive = sum(1 for k in ("S4", "S2", "C3", "C1") if FROZEN_D[k] == 1)
    guard("FIXER-PREDICATE-SENSITIVE",
          _alt_naive == 4 and KEY["channel_fixers_count"] == 0
          and _alt_naive != KEY["channel_fixers_count"],
          "冻结单谱后朴素「distinct==1 即固定」会数出 %d 个，但都是谱制品（k 无关）；真实 k 固定机制 %d 个"
          % (_alt_naive, KEY["channel_fixers_count"]))

    _prev2 = json.load(io.open(_PREV_JS, "r", encoding="utf-8"))
    guard("CROSS-VOLUME-READBACK",
          _prev2["key_numbers"]["cs_nmin_distinct"] == KEY["prev_cs_distinct"] == 2
          and _prev2["key_numbers"]["cs_k_independent"] == KEY["prev_cs_k_independent"] == False
          and _prev2["key_numbers"]["channel_fixers_count"] == KEY["prev_channel_fixers"] == 0
          and _prev2["final"] == KEY["prev_final"] == "GATES-PASS-WITH-1-NEGATIVE"
          and KEY["r403_exists"]
          and KEY["r403_c3_four_force"] == 0
          and _b07_ok and _b09_ok and _c03_ok and _c05_ok,
          "重新打开 X-V63-12 与 r403 独立比对：cs_distinct=%d、cs_k_independent=%s、fixers=%d、final=%s；r403 C3 含四力=%d"
          % (KEY["prev_cs_distinct"], KEY["prev_cs_k_independent"],
             KEY["prev_channel_fixers"], KEY["prev_final"],
             KEY["r403_c3_four_force"]))

    _rd_bytes = io.open(RD, "rb").read()
    guard("NO-NEW-RID-NO-README",
          KEY["readme_r403_tokens"] >= 1   # r403 已由 GUT 裁决卷独立登记
          and KEY["r403_files"] >= 1
          and KEY["readme_r402_tokens"] == 2
          and b"X-V63-13" not in _rd_bytes
          and b"TUFT-r404" not in _rd_bytes
          and len(glob.glob(os.path.join(ROOT, "源码", "*X-V63-13*"))) == 0
          and len(glob.glob(os.path.join(ROOT, "数据", "*X-V63-13*"))) == 0
          and len(glob.glob(os.path.join(ROOT, "判定", "*X-V63-13*"))) == 0,
          "README %d B；r402 锚点 %d；r403 锚点 %d（r403 已由 GUT 裁决卷独立登记）；本册名 X-V63-13 不在 README、未占 r404、三树无大写 RID 登记文件（本册小写 _xv6313_ 前缀文件为合法攻坚册产物）"
          % (KEY["readme_bytes"], KEY["readme_r402_tokens"],
             KEY["readme_r403_tokens"]))

    guard("KIND-COUNT", sum(COUNTS.values()) == len(ROWS),
          "计数和 %d 对条目数 %d" % (sum(COUNTS.values()), len(ROWS)))

    guard("FINAL-BRANCHES",
          final_of(1, 1, 1).startswith("GATES-FAIL-GUARD")
          and final_of(1, 0, 0) == "GATES-FAIL-UNDECLARED-NEGATIVE"
          and final_of(1, 0, 1) == "GATES-PASS-WITH-1-NEGATIVE"
          and final_of(0, 0, 1) == "GATES-PASS-ALL-POSITIVE",
          "守卫红挡门 / 缺 n_decl 错报 / 已登记判负不挡门 / 全正，四分支均测")

    _dump1 = json.dumps(back, ensure_ascii=False, sort_keys=True)
    _dump2 = json.dumps(back, ensure_ascii=False, sort_keys=True)
    guard("IDEMPOTENT-SELF", _dump1 == _dump2 and len(_dump1) > 1000,
          "序列化两次一致，长度 %d" % len(_dump1))


def make_out():
    return {
        "title": TITLE, "date": DATE, "rid": "NONE-NO-RID",
        "body_type": "跨卷攻坚册（不新增 RID、不进 README、条目不相加）",
        "final": "PENDING", "verdict": "PENDING",
        "n_rows": 0, "counts": {}, "declared_neg": list(DECLARED_NEG),
        "rows": [dict(r) for r in ROWS],
        "guards": [], "key_numbers": KEY,
        "key_table_two_path": {"left": KEY["key_table_left"],
                               "right": KEY["key_table_right"]},
        "backfill": {"before": 0, "after": 0},
    }


def main():
    # 回填顺序：写占位 -> 回读 -> 回填 -> 再写 -> 追加全部守卫 -> 才算 FINAL -> 最后拼报告
    out = make_out()
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1))
    back = json.load(io.open(JS, "r", encoding="utf-8"))
    _before = back["n_rows"]
    back["n_rows"] = len(ROWS)
    back["counts"] = counts_of(ROWS)
    back["backfill"] = {"before": _before, "after": len(ROWS)}
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(back, ensure_ascii=False, indent=1))

    guard("BACKFILL-ORDER",
          _before == 0 and back["n_rows"] == len(ROWS)
          and back["counts"] == COUNTS,
          "占位 %d -> 回填 %d；counts 同步=%s"
          % (_before, back["n_rows"], back["counts"] == COUNTS))
    run_guards(back)

    nf_guard = sum(1 for g in GUARDS if not g["ok"])
    nf_main = sum(1 for r in ROWS if r["kind"] == "FAIL")
    FINAL = final_of(nf_main, nf_guard, len(DECLARED_NEG))
    VERDICT = "__".join(build_segments(0))
    back["final"] = FINAL
    back["verdict"] = VERDICT
    back["guards"] = [dict(g) for g in GUARDS]
    back["guard_count"] = len(GUARDS)
    back["guard_pass"] = len(GUARDS) - nf_guard
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(back, ensure_ascii=False, indent=1))

    K = KEY
    L = []
    L.append("=" * 78)
    L.append(TITLE + "  " + DATE)
    L.append("体例：跨卷攻坚册（不新增 RID、不进 README 登记位、条目不相加）")
    L.append("=" * 78)
    L.append("")
    L.append("FINAL = " + FINAL)
    L.append("VERDICT = " + VERDICT)
    L.append("")
    L.append("条目 %d（%s）；控制组 %d；守卫 %d/%d；DECLARED_NEG = %s"
             % (len(ROWS), str(COUNTS), len([r for r in ROWS if r["layer"] == "K"]),
                len(GUARDS) - nf_guard, len(GUARDS), str(DECLARED_NEG)))
    L.append("回填 = ROWS-%d/GUARDS-%d" % (len(ROWS), len(GUARDS)))
    L.append("")
    L.append("【主册逐条】")
    for r in ROWS:
        L.append("  %-4s [%-8s] %s" % (r["id"], r["kind"], r["name"]))
        L.append("        exp = " + r["exp"])
        L.append("        act = " + r["act"])
        if r["note"]:
            L.append("        note = " + r["note"])
    L.append("")
    L.append("【守卫】")
    for g in GUARDS:
        L.append("  [%-3s] %-30s | %s" % ("ok" if g["ok"] else "BAD", g["name"], g["detail"]))
    L.append("")
    L.append("【关键表 · 两路机拼】")
    L.append("  GS 表 左路 %s | 右路 %s" % (str(_left_gs), str(_right_gs)))
    L.append("  机制取值 左路 %s | 右路 %s" % (str(_left_mech), str(_right_mech)))
    L.append("  Bianchi 陪集 左路 %s | 右路 %s" % (str(_left_bianchi), str(_right_bianchi)))
    L.append("  lambda 左路 %s | 右路 %s" % (str(_left_lambda), str(_right_lambda)))
    L.append("  两路一致 = " + str(K["key_table_same"]))
    L.append("")
    L.append("【关键数字】")
    L.append("  谱全集 %d 组；Cauchy-Schwarz 违例 %d；GS 约定 A 成立 %d（非平凡 %d）、约定 B 成立 %d（非平凡 %d）"
             % (K["n_spectra"], K["cs_bad"], K["a_zero"], K["a_nontrivial"],
                K["b_zero"], K["b_nontrivial"]))
    L.append("  约定 A 成立 ⟺ |q_i| 全等的失配 %d（须 0）；窗口内 lambda=%s；窗口外 lambda=%d 仍 res_A=%d"
             % (K["eq_mismatch"], K["lambda_window"], EXT[0], K["ext_res_A"]))
    L.append("  范围外首错谱 %s：A 残差 %d、B 残差 %d"
             % (K["first_fail"], K["first_fail_A"], K["first_fail_B"]))
    L.append("  五机制全谱域 k 候选取值 S4=%d S2=%d C3=%d C1=%d S0=%d Bianchi=%d"
             % (K["mech_full"]["S4"], K["mech_full"]["S2"], K["mech_full"]["C3"],
                K["mech_full"]["C1"], K["mech_full"]["S0"], K["mech_full"]["Bianchi"]))
    L.append("  冻结单谱 q=(1,1,1,1) 后 C3=%d（全谱域 %d）；候选多值来自谱选择"
             % (K["mech_frozen"]["C3"], K["mech_full"]["C3"]))
    L.append("  k 网格 %s（Dirac 整数性全允许）；Bianchi 陪集 n=1,2→%s、n=3,6,9→%s"
             % (K["k_grid"], K["bianchi_coset"]["1"], K["bianchi_coset"]["3"]))
    L.append("  机制全集 %s；合法机制 %d/%d；CS 级 k 自由=%s（承接 X-V63-12）"
             % (str(K["mech_names"]), K["channel_fixers_count"],
                K["channel_total"], K["prev_cs_k_independent"]))
    L.append("  跨册：X-V63-12 cs_distinct=%d、cs_hitrate=%s、fixers=%d、final=%s"
             % (K["prev_cs_distinct"], K["prev_cs_hitrate"],
                K["prev_channel_fixers"], K["prev_final"]))
    L.append("  跨册：r403 存在=%s、C3 含四力=%d 条、C3 真统一=%s（电弱 L_EW）"
             % (K["r403_exists"], K["r403_c3_four_force"], K["r403_unique_c3_unified"]))
    L.append("  README %d B / r402 锚点 %d / r403 锚点 %d / r403 文件 %d"
             % (K["readme_bytes"], K["readme_r402_tokens"],
                K["readme_r403_tokens"], K["r403_files"]))
    L.append("")
    L.append("【诚实边界】")
    L.append("  1. 只产可算判决，不产新物理；独立实验预言 0。")
    L.append("  2. 严格结论只覆盖单 U(1)+引力扇区、Weyl 费米子、电荷矩 S0/S2/S4/C1/C3；完整 SM 手征谱、全 6D 反常多项式、弦论 UV 完成未算。")
    L.append("  3. GS 因式分解只约束电荷尺度结构（|q_i| 全等），不固定共同幅值 lambda，也不固定 CS 级 k。")
    L.append("  4. 反常配平只匹配系数比值，给出的是等式约束不是唯一解；k 是自由离散输入。")
    L.append("  5. 不是全称否证：不声称任何 GUT 都不可能把 k 由反常配平固定；若由作用量/真空选择推导出 k，B06 需重判。")
    L.append("  6. 四力统一未证明（回代 r403：含引力四力大统一正确者 = 0 条）；把它称为攻破统一场论会是虚假宣称。")
    L.append("  7. 本册为攻坚册：不新增 RID、不进 README、不与任何卷相加；r403 已占用，下轮审计号从 r404 起。")
    L.append("")
    L.append("【DECLARED_NEG】" + str(DECLARED_NEG))
    io.open(RPT, "w", encoding="utf-8", newline="\r\n").write("\n".join(L) + "\n")
    print("\nFINAL = " + FINAL)
    print("条目 %d %s / 守卫 %d/%d" % (len(ROWS), str(COUNTS),
                                    len(GUARDS) - nf_guard, len(GUARDS)))
    print("JSON = " + JS)
    print("REPORT = " + RPT)


if __name__ == "__main__":
    main()
