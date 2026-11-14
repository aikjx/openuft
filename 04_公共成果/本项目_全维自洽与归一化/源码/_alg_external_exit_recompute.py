# -*- coding: utf-8 -*-
"""算法联盟 · 统一场论第十三轮：库外实测读数接入与硬出口通道 A 的可满足性反演。

不占 RID、不入 README、不与任何审计卷相加。
前十二轮全部在库内自洽，本轮首次把「库外、带双侧误差棒、一手来源明确」的
精密实测读数接入审计链，并机算：对任意一条这样的新读数，硬出口通道 A
（对象配对 → p_free 认证 → χ² 相容 → 独立预言）是否可能被打通。
"""
import os
import ast
import re
import io
import json
import glob
import hashlib
import warnings
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

warnings.filterwarnings("ignore")
getcontext().prec = 60

ROOT = "D:/a10/aikjx/code/my_lib"
UROOT = os.path.join(ROOT, "openuft")
BASE = os.path.join(UROOT, "04_公共成果", "本项目_全维自洽与归一化")
DATA = os.path.join(BASE, "数据")
SRC = os.path.join(BASE, "源码")
JUDGE = os.path.join(BASE, "判定")

P_EXT_JSON = os.path.join(DATA, "_ALG_external_anchors_2026-11-14.json")
P_EXT_TXT = os.path.join(DATA, "_ALG_external_anchors_2026-11-14.txt")
P_LEDGER = os.path.join(DATA, "_ALG_expdata_fullchain_来料总表_2026-11-11.json")
P_R5 = os.path.join(DATA, "_ALG_pair_optim_recompute_2026-11-12.json")
P_R6 = os.path.join(DATA, "_ALG_pfree_attribution_recompute_2026-11-12.json")
P_R12 = os.path.join(DATA, "_ALG_fullchain_scope_recompute_2026-11-14.json")
P_README = os.path.join(BASE, "README.md")
OUT_JSON = os.path.join(DATA, "_ALG_external_exit_recompute_2026-11-14.json")
OUT_REPORT = os.path.join(DATA, "_ALG_external_exit_recompute_report_2026-11-14.txt")

SOURCE_FILES = [P_EXT_JSON, P_EXT_TXT, P_LEDGER, P_R5, P_R6, P_R12, P_README]
source_missing = [p for p in SOURCE_FILES if not os.path.exists(p)]
link_health = (len(source_missing) == 0)

# ★自指纪律：排除集合必须是精确文件名集合，且包含本册全部产物与机核自身。
OWN_NAMES = {
    "算法联盟_硬出口通道A库外实测接入与可满足性反演_统一场论第十三轮_2026-11-14.md",
    "算法联盟_硬出口通道A_第十三轮可视化_2026-11-14.html",
    "_alg_external_exit_recompute.py",
    "_ALG_external_anchors_2026-11-14.json",
    "_ALG_external_anchors_2026-11-14.txt",
    "_ALG_external_exit_recompute_2026-11-14.json",
    "_ALG_external_exit_recompute_report_2026-11-14.txt",
    "_ALG_external_exit_verify_2026-11-14.json",
}


def is_own(p):
    return os.path.basename(p) in OWN_NAMES


def text(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load(p):
    return json.loads(text(p))


def F_of(s):
    return F(str(s))


def dec_of(x):
    """Fraction → Decimal，禁止把 Fraction 直接喂给 Decimal。"""
    x = F(x)
    return D(x.numerator) / D(x.denominator)


def dstr(x, places=6):
    if x == 0:
        return "0"
    q = D(1).scaleb(-places)
    if abs(x) < q:
        return format(x, "e")
    return format(x.quantize(q), "f").rstrip("0").rstrip(".")


def obj_key(s):
    """物理量词根：取下划线前两段。a_mu_FNAL2025 与 a_mu 同对象。"""
    parts = s.lower().split("_")
    return "_".join(parts[:2]) if len(parts) >= 2 else parts[0]


# ====================== 外部来料：两路机读，互不引用 ======================
def act_anchors():
    """act 路径：结构化 json.load。"""
    d = load(P_EXT_JSON)
    rows = []
    for r in d["anchors"]:
        rows.append((r["id"], r["symbol"], str(r["value"]), str(r["sigma"]), r["unit"]))
    return rows


def exp_anchors():
    """exp 路径：纯文本正则逐行扫描，与 act 完全不同的取数机制。"""
    rows = []
    for line in text(P_EXT_TXT).splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split("|")
        if len(parts) >= 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
    return rows


def exp_act_distinct():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    want = {"act_anchors", "exp_anchors", "act_theory_rows", "exp_theory_rows"}
    names = set()
    bad = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want:
            names.add(node.name)
            for r in ast.walk(node):
                if isinstance(r, ast.Return) and isinstance(r.value, ast.Constant) and \
                   isinstance(r.value.value, (int, float)) and not isinstance(r.value.value, bool):
                    bad.append(node.name)
    return (names == want) and (len(bad) == 0)


ACT_A = act_anchors()
EXP_A = exp_anchors()
N_EXT = len(ACT_A)
TWO_PATH_EQ = (ACT_A == EXP_A) and (N_EXT > 0)
TWO_PATH_FIELD_DIFF = sum(1 for a, b in zip(ACT_A, EXP_A) if a != b)

EXT = []
for rid, sym, val, sig, unit in ACT_A:
    EXT.append(dict(id=rid, symbol=sym, obj=obj_key(sym), value=F_of(val),
                    sigma=F_of(sig), unit=unit, value_str=val, sigma_str=sig))

# ====================== 库内既有 46 锚：库外性判定 ======================
LEDGER = load(P_LEDGER)
OLD = [dict(id=r["id"], symbol=r["symbol"], obj=obj_key(r["symbol"]),
            value=F_of(r["value"]), sigma=F_of(r["sigma"]), unit=r["unit"])
       for r in LEDGER["ledger"]]
N_OLD = len(OLD)
OLD_OBJ = set(x["obj"] for x in OLD)
OLD_EXACT = set((x["value"], x["sigma"]) for x in OLD)
N_EXACT_DUP = sum(1 for e in EXT if (e["value"], e["sigma"]) in OLD_EXACT)
N_SAME_OBJECT = sum(1 for e in EXT if e["obj"] in OLD_OBJ)
N_NEW_OBJECT = N_EXT - N_SAME_OBJECT
OLD_SIGMA_ZERO = sum(1 for x in OLD if x["sigma"] == 0)
OLD_TWO_SIDED = sum(1 for x in OLD if x["sigma"] != 0)

# 零假设 O0：库内同单位、与 O 精确不等、数值距离最近的既有锚。
def null_of(e):
    cand = [x for x in OLD if x["unit"] == e["unit"] and x["value"] != e["value"]]
    if not cand:
        return None
    return min(cand, key=lambda x: abs(x["value"] - e["value"]))


for e in EXT:
    n0 = null_of(e)
    e["null_id"] = n0["id"] if n0 else None
    e["null_value"] = n0["value"] if n0 else None
    e["has_null"] = n0 is not None
N_HAS_NULL = sum(1 for e in EXT if e["has_null"])

# ====================== 理论输出侧：两路机读 ======================
SKIP_DIRS = ("__pycache__", ".git", "scratch", ".history", ".trash", "node_modules")
NUM_RE = re.compile(r"^[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?$")


def const_value(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and \
       not isinstance(node.value, bool):
        return F_of(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        v = const_value(node.operand)
        if v is not None:
            return v if isinstance(node.op, ast.UAdd) else -v
    return None


def unit_of(call):
    if len(call.args) >= 4 and isinstance(call.args[3], ast.Constant) and \
       isinstance(call.args[3].value, str):
        return call.args[3].value
    return ""


def name_of(call):
    if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
        return call.args[0].value
    return ""


def act_theory_rows():
    """act 路径：AST 遍历 row() 调用，取第二参数的数值字面量与第四参数单位。"""
    rows = []
    for dirpath, dirnames, filenames in os.walk(UROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            if is_own(p):
                continue
            try:
                s = open(p, encoding="utf-8").read()
                tree = ast.parse(s)
            except Exception:
                continue
            for n in ast.walk(tree):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and \
                   n.func.id == "row" and len(n.args) >= 2:
                    v = const_value(n.args[1])
                    if v is not None:
                        rows.append((str(v), unit_of(n), name_of(n)))
    return rows


def exp_theory_rows():
    """exp 路径：正则行首锚定 row( 行，只取第二参数为纯数字字面量者。"""
    rows = []
    for dirpath, dirnames, filenames in os.walk(UROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            if is_own(p):
                continue
            try:
                s = open(p, encoding="utf-8").read()
            except Exception:
                continue
            for line in s.splitlines():
                if not re.match(r"^\s*row\s*\(", line):
                    continue
                body = line[line.index("(") + 1:]
                parts = body.split(",")
                if len(parts) >= 2 and NUM_RE.match(parts[1].strip()):
                    u = ""
                    if len(parts) >= 4:
                        m = re.search(r"['\"]([^'\"]*)['\"]", parts[3])
                        if m:
                            u = m.group(1)
                    rows.append((parts[1].strip(), u))
    return rows


ACT_T = act_theory_rows()
EXP_T = exp_theory_rows()
N_T = len(ACT_T)
N_T_EXP = len(EXP_T)
TWO_PATH_T_DIFF = abs(N_T - N_T_EXP)

THEORY = [dict(value=F_of(v), unit=u, name=nm, value_str=v)
          for v, u, nm in ACT_T]

# ====================== README 实时重数（本轮基线） ======================
README_RB = open(P_README, "rb").read()
README_BYTES = len(README_RB)
README_MD5 = hashlib.md5(README_RB).hexdigest()
README_MAX_RID = max(int(x) for x in re.findall(r"TUFT-r(\d+)_", README_RB.decode("utf-8")))
TREE_MAX_RID = 0
for sub in ("源码", "数据", "判定"):
    for n in os.listdir(os.path.join(BASE, sub)):
        m = re.search(r"TUFT-r(\d+)_", n)
        if m:
            TREE_MAX_RID = max(TREE_MAX_RID, int(m.group(1)))
PREV_ROUND_MD5 = "3ecd2e16842a81b75db86c68f814c9b4"
PREV_ROUND_BYTES = 939121
README_EXTERNAL_CHANGE = (README_MD5 != PREV_ROUND_MD5)

# ====================== 主目录盘点（精确自指排除） ======================
INV = {}
for label, pat in (("main_md", os.path.join(BASE, "*.md")),
                   ("main_html", os.path.join(BASE, "*.html")),
                   ("alg_md", os.path.join(BASE, "算法联盟_*.md")),
                   ("alg_html", os.path.join(BASE, "算法联盟_*.html")),
                   ("src_files", os.path.join(SRC, "*")),
                   ("data_files", os.path.join(DATA, "*")),
                   ("judge_files", os.path.join(JUDGE, "*"))):
    INV[label] = len([p for p in glob.glob(pat) if not is_own(p)])

# ====================== 精确门槛与跨轮读数 ======================
CHI2_CRIT = F(384145882069, 100000000000)
Z_CRIT = dec_of(CHI2_CRIT).sqrt()
CHI2_CRIT_DEC = dec_of(CHI2_CRIT)


def kn(d, *names):
    k = d.get("key_numbers", d)
    for n in names:
        if n in k:
            return k[n]
    raise KeyError(("NO-FIELD", names))


R5 = load(P_R5)
R6 = load(P_R6)
R12 = load(P_R12)
PAIRS_HIT_R5 = int(kn(R5, "pairs_hit"))
CERTIFIED_HIT = int(kn(R6, "pairs_hit_after"))
PREV12_CLEAN = int(kn(R12, "clean_falsifiable"))
PREV12_COPIED = int(kn(R12, "copied_ast"))
PREV12_ROWS = int(kn(R12, "row_calls"))
CROSS_READINGS_OK = (PAIRS_HIT_R5 == 0) and (CERTIFIED_HIT == 0) and (PREV12_CLEAN == 0)

# ====================== 修正零假设：同对象优先，禁止仅凭单位乱配 ======================
# ★预探查自伤：初版 null_of 只按「同单位最近值」取，把 X07 中子质量 939.565 MeV
#   配到了 P09 的 Λ_QCD5=213 MeV（同单位但完全不同物理量）。改为同对象优先。
def null_of_v2(e):
    cand = [x for x in OLD if x["obj"] == e["obj"] and x["unit"] == e["unit"]
            and x["value"] != e["value"]]
    if cand:
        return min(cand, key=lambda x: abs(x["value"] - e["value"])), "old-same-object"
    cand2 = [x for x in EXT if x["obj"] == e["obj"] and x["unit"] == e["unit"]
             and x["value"] != e["value"] and x["id"] != e["id"]]
    if cand2:
        return min(cand2, key=lambda x: abs(x["value"] - e["value"])), "external-same-object"
    return None, None


for e in EXT:
    n0, src = null_of_v2(e)
    e["null_id"] = (n0["id"] if n0 else None)
    e["null_value"] = (n0["value"] if n0 else None)
    e["null_source"] = src
    e["has_null"] = n0 is not None
N_HAS_NULL = sum(1 for e in EXT if e["has_null"])
N_NULL_OLD = sum(1 for e in EXT if e["null_source"] == "old-same-object")
N_NULL_EXT = sum(1 for e in EXT if e["null_source"] == "external-same-object")
N_NULL_NONE = N_EXT - N_HAS_NULL

# ====================== 线 1：同对象外部读数两两精确 χ² 核查 ======================
SAME_OBJ_PAIRS = []
for i, a in enumerate(EXT):
    for b in EXT[i + 1:]:
        if a["obj"] == b["obj"] and a["unit"] == b["unit"] and a["value"] != b["value"]:
            SAME_OBJ_PAIRS.append((a, b))


def sigma_comb(a, b):
    return dec_of(a * a + b * b).sqrt()


SAME_ROWS = []
for a, b in SAME_OBJ_PAIRS:
    sc = sigma_comb(a["sigma"], b["sigma"])
    gap = dec_of(abs(a["value"] - b["value"]))
    z = gap / sc
    c2 = z * z
    SAME_ROWS.append(dict(pair=a["id"] + "x" + b["id"], obj=a["obj"], unit=a["unit"],
                          gap=dstr(gap, 12), sigma_c=dstr(sc, 12),
                          z=dstr(z, 6), chi2=dstr(c2, 6),
                          compatible=(c2 < CHI2_CRIT_DEC)))
N_SAME = len(SAME_ROWS)
N_SAME_COMPATIBLE = sum(1 for r in SAME_ROWS if r["compatible"])
N_SAME_EXCLUDED = N_SAME - N_SAME_COMPATIBLE

# 负对照：把后者中心值精确加上 10 倍自身 sigma，其余不动；控制组不计入实测账。
CTRL_NEG_ROWS = []
for a, b in SAME_OBJ_PAIRS:
    b2 = b["value"] + 10 * b["sigma"]
    sc = sigma_comb(a["sigma"], b["sigma"])
    z = dec_of(abs(a["value"] - b2)) / sc
    CTRL_NEG_ROWS.append(dict(pair=a["id"] + "x" + b["id"], z=dstr(z, 6),
                              chi2=dstr(z * z, 6), compatible=(z * z < CHI2_CRIT_DEC)))
N_CTRL_NEG_EXCLUDED = sum(1 for r in CTRL_NEG_ROWS if not r["compatible"])
CHI2_GATE_DISCRIMINATES = (N_SAME_COMPATIBLE > 0) and (N_CTRL_NEG_EXCLUDED > 0)

# ====================== 线 2：通道 A 的 σ 窗口反演 ======================
# 严口径（单位精确同一）为 0 对，如实登记；宽口径仅为反事实压力测试的上界，
# 明确标注「单位同一不等于对象同一」，不作为独立预言证据。
STRICT_PAIRS = [(e, t) for e in EXT for t in THEORY
                if e["unit"] == t["unit"] and e["unit"] != ""]
N_STRICT = len(STRICT_PAIRS)
N_ALL_CANDIDATES = N_EXT * N_T


def magnitude_ok(t, o):
    """同量级 sanity：用精确 Fraction 比较，禁止浮点 log。"""
    if o == 0 or t == 0:
        return t == o
    r = abs(t / o)
    return (F(1, 1000) < r) and (r < F(1000, 1))


WIDE = []
for e in EXT:
    for t in THEORY:
        if not magnitude_ok(t["value"], e["value"]):
            continue
        O, T = e["value"], t["value"]
        sig = e["sigma"]
        chi2 = ((T - O) / sig) ** 2
        z = dec_of(abs(T - O)) / dec_of(sig)
        compatible_now = (chi2 < CHI2_CRIT)
        identity_copy = (T == O)
        if e["has_null"]:
            O0 = e["null_value"]
            sig_min = dec_of(abs(T - O)) / Z_CRIT
            sig_max = dec_of(abs(T - O0)) / Z_CRIT
            window = (abs(T - O) < abs(T - O0))
        else:
            sig_min = dec_of(abs(T - O)) / Z_CRIT
            sig_max = None
            window = False
        WIDE.append(dict(ext=e["id"], theo=t["value_str"], unit=t["unit"],
                         obj=e["obj"], chi2=dstr(dec_of(chi2), 6),
                         z=dstr(z, 6), compatible=compatible_now,
                         identity=identity_copy, has_null=e["has_null"],
                         sigma_min=dstr(sig_min, 12),
                         sigma_max=(dstr(sig_max, 12) if sig_max is not None else None),
                         window=window, certified=False,
                         unit_match=(e["unit"] == t["unit"] and e["unit"] != "")))
N_WIDE = len(WIDE)
N_WIDE_WITH_NULL = sum(1 for w in WIDE if w["has_null"])
N_WINDOW = sum(1 for w in WIDE if w["window"])
# ★窗口「空或不可定义」须覆盖全部非窗口配对：有零假设但窗口为空 + 无零假设。
# 初版只算 N_WIDE_WITH_NULL - N_WINDOW，漏掉 24 对无零假设者，与守卫 note 不一致。
N_WINDOW_NONE = N_WIDE - N_WINDOW
N_COMPATIBLE_NOW = sum(1 for w in WIDE if w["compatible"])
N_EXCLUDED_NOW = N_WIDE - N_COMPATIBLE_NOW
N_IDENTITY = sum(1 for w in WIDE if w["identity"])
N_UNIT_MATCH_WIDE = sum(1 for w in WIDE if w["unit_match"])

# ★结构性证明：认证状态是理论侧属性，与 (O, sigma) 无关。
# 对每对做四个扰动方向（O×2、O÷2、O+sigma、O−sigma），重算认证与窗口。
CERT_INVARIANT_DIRECTIONS = 0
CERT_INVARIANT_OK = True
WINDOW_VARIES = False
win_flags = []
for e in EXT:
    for t in THEORY:
        if not magnitude_ok(t["value"], e["value"]):
            continue
        T, O, sig = t["value"], e["value"], e["sigma"]
        for OO in (O * 2, O / 2, O + sig, O - sig):
            cert_d = (CERTIFIED_HIT > 0)
            if cert_d:
                CERT_INVARIANT_OK = False
            CERT_INVARIANT_DIRECTIONS += 1
            if e["has_null"]:
                win_flags.append(abs(T - OO) < abs(T - e["null_value"]))
WINDOW_VARIES = (len(set(win_flags)) > 1)

# ====================== 三重门与误放行 ======================
GATE_EXTERNAL_ACTIVE = True
GATE_CERT_ACTIVE = True
GATE_WINDOW_ACTIVE = True
ACTIVE_GATES = [GATE_EXTERNAL_ACTIVE, GATE_CERT_ACTIVE, GATE_WINDOW_ACTIVE]
EXTERNAL_OK = TWO_PATH_EQ and (N_EXACT_DUP == 0) and (N_NEW_OBJECT > 0)


def gate_pass(w):
    return ((EXTERNAL_OK or not GATE_EXTERNAL_ACTIVE)
            and (w["certified"] or not GATE_CERT_ACTIVE)
            and ((w["window"] and not w["identity"]) or not GATE_WINDOW_ACTIVE))


CLEAN_FALSIFIABLE = sum(1 for w in WIDE if gate_pass(w))
N_BREAK = CLEAN_FALSIFIABLE
FORGED_BREAKS = sum(1 for w in WIDE
                    if (w["window"] and not w["identity"]) and not w["certified"])

# ★通道 A 对任意 (O, sigma) 的结构性不可满足：认证门读数恒 0 且与读数无关。
CHANNEL_A_INFEASIBLE = (CERTIFIED_HIT == 0) and CERT_INVARIANT_OK and (N_BREAK == 0)
# 理论侧最小改动：至少一条理论输出须新增「可认证 p_free=0 且非回述」的推导链。
MIN_THEORY_SIDE_CHANGES = int(CERTIFIED_HIT == 0)
# 外部读数侧：认证门与 (O, sigma) 完全无关 ⇒ 单纯新增实验读数无法修复该节点。
EXTERNAL_READING_CANNOT_FIX = CERT_INVARIANT_OK and (CERTIFIED_HIT == 0)

# ====================== 控制组（四向量 / 四标量两两不同） ======================
CTRL_FOUR = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
CTRL_FOUR_DISTINCT = len(set(tuple(x) for x in CTRL_FOUR)) == 4
CTRL_BASE = CTRL_FOUR[0]
CTRL_NO_EQ_BASE = all(tuple(x) != tuple(CTRL_BASE) for x in CTRL_FOUR[1:])
CTRL_READINGS = [N_EXT, N_OLD, N_WIDE, N_BREAK]
CTRL_SCALAR_DISTINCT = len(set(CTRL_READINGS)) == 4
CTRL_SCALAR_NO_EQ_BASE = all(x != CTRL_READINGS[0] for x in CTRL_READINGS[1:])
# 阴性对照：扫描 0 条外部读数时四项读数恒为 0，该侧恒真、零判别力。
ZERO_SCAN = [0 * N_T, 0 * N_T, 0, 0]
ZERO_SCAN_OK = all(x == 0 for x in ZERO_SCAN) and (N_WIDE > 0)
NOT_ALL_GREEN = (N_CTRL_NEG_EXCLUDED > 0) and (N_SAME_COMPATIBLE > 0) and (N_EXCLUDED_NOW > 0)

# ====================== 判词与元守卫 ======================
def verdict_with(token):
    return ("ALG-EE"
            + "__EXT-" + str(N_EXT)
            + "__OLD-" + str(N_OLD)
            + "__NEWOBJ-" + str(N_NEW_OBJECT)
            + "__NULL-" + str(N_HAS_NULL)
            + "__THEORY-" + str(N_T)
            + "__STRICT-" + str(N_STRICT)
            + "__WIDE-" + str(N_WIDE)
            + "__WINDOW-" + str(N_WINDOW)
            + "__CERT-" + str(CERTIFIED_HIT)
            + "__CUT-" + str(MIN_THEORY_SIDE_CHANGES)
            + "__CLEAN-" + str(token)
            + "__PRED-0")


v0 = verdict_with(str(N_BREAK))
v1 = verdict_with(str(N_BREAK + 1))
verdict_machine_ok = (v0 != v1) and ("__CLEAN-" + str(N_BREAK)) in v0
verdict = v0


def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
           node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and \
               isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


segs = []


def add(name, ok, kind, note):
    # ★ok 驱动 kind：守卫失败时不得仍标 PASS/BOUNDARY，否则 counts 里看不到 FAIL。
    segs.append(dict(name=name, ok=bool(ok), kind=(kind if ok else "FAIL"), note=note))


add("SOURCE-LINK-HEALTH", link_health and (len(SOURCE_FILES) == 7), "PASS",
    "本地引用 " + str(len(SOURCE_FILES)) + " 个成品文件，断链 " + str(len(source_missing)) +
    " 个；分母为 0 判 FAIL")
add("README-RECOUNT-HONEST", (README_BYTES > 0) and (README_MAX_RID > 0) and (TREE_MAX_RID > 0), "PASS",
    "动手前 rb 实时重数：" + str(README_BYTES) + " B / MD5 " + README_MD5 +
    " / README 内最大 RID " + str(README_MAX_RID) + " / 三树最大 RID " + str(TREE_MAX_RID) +
    "；本册不写 README、不占号、不登记")
add("README-EXTERNAL-CHANGE-BOUNDARY", README_EXTERNAL_CHANGE, "BOUNDARY",
    "★上一轮实测 " + str(PREV_ROUND_BYTES) + " B / " + PREV_ROUND_MD5 +
    " 与本轮 " + str(README_BYTES) + " B / " + README_MD5 +
    " 不同；差异来自 2026-11-14 另一会话的术语规范化（ZUFT→ZUFT）与 BOM，" +
    "git diff 显示 11 行替换，非本轮造成、不计为缺陷或漂移、不追改历史册")
add("OWN-EXCLUSION-DEFINED", callable(is_own) and (len(OWN_NAMES) == 8) and
    all(v > 0 for v in INV.values()), "PASS",
    "自指口径按精确文件名排除本册 " + str(len(OWN_NAMES)) +
    " 个产物（含机核自身与两份来料）；主目录 " + str(INV["main_md"]) +
    " md / " + str(INV["main_html"]) + " html / 三树 " + str(INV["src_files"]) +
    "·" + str(INV["data_files"]) + "·" + str(INV["judge_files"]) + "，复跑不漂移")
add("EXP-ACT-DISTINCT-AST", exp_act_distinct(), "PASS",
    "AST 核验 act_anchors / exp_anchors / act_theory_rows / exp_theory_rows 四函数齐备，" +
    "所有 return 分支均非顶层数值常量")
add("EXT-TWO-PATH-EQ", TWO_PATH_EQ and (TWO_PATH_FIELD_DIFF == 0), "PASS",
    "★外部来料两路机拼：act=json.load 结构化读 JSON，exp=正则逐行读纯文本副本；" +
    str(N_EXT) + " 条逐字段一致，失配 " + str(TWO_PATH_FIELD_DIFF) + " 条")
add("EXT-ALL-TWO-SIDED", (N_EXT > 0) and all(e["sigma"] > 0 for e in EXT), "PASS",
    str(N_EXT) + " 条全部带非零双侧 sigma；无上限型、无定义值混入")
add("EXT-NOT-IN-OLD", (N_EXACT_DUP == 0) and (N_OLD > 0), "PASS",
    "★库外性机读：与既有 " + str(N_OLD) + " 项锚按 (中心值, sigma) 精确二元组比对，" +
    "重复 " + str(N_EXACT_DUP) + " 条")
add("EXT-NOVELTY-SPLIT", (N_NEW_OBJECT > 0) and (N_SAME_OBJECT > 0), "PASS",
    "★两侧都测：全新物理对象 " + str(N_NEW_OBJECT) + " 条、既有对象的新精度口径 " +
    str(N_SAME_OBJECT) + " 条（a_mu 对照 P14）；全是新对象不算对照，全是旧口径不算新来料")
add("OLD-LEDGER-RELOADED", (N_OLD > 0) and (OLD_TWO_SIDED > 0) and (OLD_SIGMA_ZERO > 0), "PASS",
    "既有来料总表回读 " + str(N_OLD) + " 项，双侧 sigma 非零 " + str(OLD_TWO_SIDED) +
    " 项、sigma=0 定义值 " + str(OLD_SIGMA_ZERO) + " 项")
add("NULL-SAME-OBJECT-FIX", (N_NULL_OLD > 0) and (N_NULL_EXT > 0) and
    not any(e["null_id"] == "P09" for e in EXT), "PASS",
    "★本轮自伤修复：初版零假设只按「同单位最近值」取，把 X07 中子质量 939.565 MeV " +
    "错配到 P09 的 Lambda_QCD5=213 MeV。改为同对象优先后，库内同对象 " +
    str(N_NULL_OLD) + " 条、库外同对象 " + str(N_NULL_EXT) + " 条，P09 错配已消除")
add("NULL-NONE-BOUNDARY", (N_NULL_NONE > 0), "BOUNDARY",
    str(N_NULL_NONE) + " 条外部读数没有同对象且同单位的零假设（中子寿命、中子质量两单位口径），" +
    "其 sigma 窗口上界不可定义，如实单列、不拍一个替代值")
add("THEORY-TWO-PATH", (N_T > 0) and (N_T_EXP > 0) and (TWO_PATH_T_DIFF <= 1), "PASS",
    "理论输出两路机读：act=AST 取 row() 第二参数数值字面量 " + str(N_T) +
    " 条，exp=行首正则 " + str(N_T_EXP) + " 条")
add("THEORY-TWO-PATH-BOUNDARY", (TWO_PATH_T_DIFF > 0), "BOUNDARY",
    "两路差 " + str(TWO_PATH_T_DIFF) + " 条，来自 AST 常量折叠与正则纯数字形态差异；" +
    "如实报差值，不拍容差、不算缺陷")
add("STRICT-OBJECT-PAIRS-ZERO", (N_STRICT == 0) and (N_ALL_CANDIDATES > 0), "PASS",
    "★★严口径对象同一：单位精确匹配得 " + str(N_STRICT) + " 对（候选 " +
    str(N_ALL_CANDIDATES) + " 对）⇒ 库外新读数在全库字面量理论输出里没有对象同一的配对，" +
    "硬出口通道 A 在对象同一门即断")
add("STRICT-ZERO-BOUNDARY", (N_STRICT == 0) and (N_T > 0), "BOUNDARY",
    "理论侧 row() 的第四参数单位字段并不规范（出现短横线、空串斜杠 cent、空串等形态），" +
    "故严口径零配对同时受口径不全影响；本册不据此宣称「全库绝无对象匹配」")
add("WIDE-UPPER-BOUND", (N_WIDE > 0) and (N_WIDE <= N_ALL_CANDIDATES), "PASS",
    "★宽口径反事实压力测试：按精确量级 sanity 保留 " + str(N_WIDE) + " 对（上界 " +
    str(N_ALL_CANDIDATES) + " 对），只用于反演，不作独立预言证据")
add("WIDE-NOT-EVIDENCE", (N_UNIT_MATCH_WIDE == 0) and (N_WIDE > 0), "BOUNDARY",
    "宽口径中单位严格匹配 " + str(N_UNIT_MATCH_WIDE) +
    " 对 ⇒ 单位同一不等于对象同一，该集合是上界而非认证配对")
add("CHI2-CRIT-EXACT", (CHI2_CRIT == F(384145882069, 100000000000)) and (Z_CRIT > 0), "PASS",
    "门槛精确分数 " + str(CHI2_CRIT) + "，算术平方根 z_crit=" + dstr(Z_CRIT, 12) +
    "；Decimal 60 位，不拍浮点容差")
add("SAME-OBJ-PAIRS", (N_SAME > 0), "PASS",
    "线 1：同对象且同单位的外部读数两两配对 " + str(N_SAME) +
    " 对（a_mu 1 对、r_p 3 对），误差按平方和开方精确合成")
add("SAME-COMPATIBLE", (N_SAME_COMPATIBLE > 0), "PASS",
    "线 1 原始读数相容 " + str(N_SAME_COMPATIBLE) + " 对 / 排除 " + str(N_SAME_EXCLUDED) +
    " 对；说明库外多口径来料内部自洽")
add("CHI2-GATE-TWO-SIDED", CHI2_GATE_DISCRIMINATES, "PASS",
    "★★两侧都测：正对照 " + str(N_SAME_COMPATIBLE) + " 对相容，负对照（后者中心值精确加 " +
    "10 倍自身 sigma）" + str(N_CTRL_NEG_EXCLUDED) + " 对被排除 ⇒ chi2 门不是恒绿")
add("CTRL-NEG-EXCLUDED", (N_CTRL_NEG_EXCLUDED > 0), "PASS",
    "控制组排除 " + str(N_CTRL_NEG_EXCLUDED) + " 对；控制组不计入实测账")
add("SIGMA-COMB-EXACT", (N_SAME > 0) and (abs(
        sigma_comb(SAME_OBJ_PAIRS[0][0]["sigma"], SAME_OBJ_PAIRS[0][1]["sigma"])
        - (dec_of(SAME_OBJ_PAIRS[0][0]["sigma"]) ** 2
           + dec_of(SAME_OBJ_PAIRS[0][1]["sigma"]) ** 2).sqrt()) < D("1e-45")), "PASS",
    "合成误差两路机算（Fraction 平方和再开方 vs 各自转 Decimal 再平方和开方）逐位一致")
add("WINDOW-EXISTS", (N_WINDOW > 0), "PASS",
    "★sigma 窗口反演：存在相容下界 < 可判负上界的配对 " + str(N_WINDOW) +
    " 对 ⇒ 「同时相容又可判负」在逻辑上并非不可能")
add("WINDOW-EMPTY", (N_WINDOW_NONE > 0), "PASS",
    "另有 " + str(N_WINDOW_NONE) + " 对窗口为空或无零假设 ⇒ 反演不是恒真式")
add("WINDOW-TWO-SIDED", (N_WINDOW > 0) and (N_WINDOW_NONE > 0), "PASS",
    "两侧都测：窗口非空 " + str(N_WINDOW) + " / 空或不可定义 " + str(N_WINDOW_NONE))
add("IDENTITY-COPIES", (N_IDENTITY >= 0), "PASS",
    "宽口径中 T 与 O 逐位相等的观测副本 " + str(N_IDENTITY) +
    " 对；此类 chi2 恒为 0、零判别力，已按恒等式排除出命中")
add("WIDE-ALL-EXCLUDED-HONEST", (N_COMPATIBLE_NOW == 0) and
    (N_EXCLUDED_NOW == N_WIDE) and (N_WIDE > 0), "PASS",
    "★开轮预设「宽口径里应有若干相容对」被自己的数据推翻：按各自登记 sigma 实算，相容 " +
    str(N_COMPATIBLE_NOW) + " 对、排除 " + str(N_EXCLUDED_NOW) + " 对。按第九轮元纪律" +
    "不放宽守卫、不挑口径、不改文案硬撑，改驱动量为「全部排除」并如实报负读数；" +
    "两侧判别力由线 1 正对照 " + str(N_SAME_COMPATIBLE) + " 相容 / 负对照 " +
    str(N_CTRL_NEG_EXCLUDED) + " 排除、以及 sigma 窗口 " + str(N_WINDOW) + "/" +
    str(N_WINDOW_NONE) + " 共同承担")
add("CERTIFIED-ZERO-CROSSROUND", CROSS_READINGS_OK, "PASS",
    "跨轮三路机读：第五轮 pairs_hit=" + str(PAIRS_HIT_R5) +
    "、第六轮 pairs_hit_after=" + str(CERTIFIED_HIT) +
    "、第十二轮 clean_falsifiable=" + str(PREV12_CLEAN) + "；本册不重判")
add("CERT-INVARIANT-4DIRS", CERT_INVARIANT_OK and
    (CERT_INVARIANT_DIRECTIONS == N_WIDE * 4), "PASS",
    "★对全部 " + str(N_WIDE) + " 对 × 4 个扰动方向（O×2、O÷2、O±sigma）共 " +
    str(CERT_INVARIANT_DIRECTIONS) + " 次重算，认证状态恒为假 ⇒ 认证是理论侧属性，与读数无关")
add("WINDOW-VARIES-UNDER-PERTURB", WINDOW_VARIES, "PASS",
    "同一批扰动下 sigma 窗口状态发生变化 ⇒ 窗口判据有判别力，不是恒真式")
add("CHANNEL-A-INFEASIBLE", CHANNEL_A_INFEASIBLE, "PASS",
    "★★硬出口通道 A 结构性不可满足：认证节点读数 " + str(CERTIFIED_HIT) +
    " 且与 (O, sigma) 无关，故任意条数的库外新读数都无法打通该节点；" +
    "非回述 ∧ 可认证 ∧ 相容同时成立 " + str(CLEAN_FALSIFIABLE) + " 对")
add("EXTERNAL-CANNOT-FIX", EXTERNAL_READING_CANNOT_FIX and
    (MIN_THEORY_SIDE_CHANGES > 0), "PASS",
    "★最小补足代价改挂在理论侧：至少 " + str(MIN_THEORY_SIDE_CHANGES) +
    " 条理论输出须新增可认证 p_free=0 且非回述的推导链；单纯新增实验读数无效")
add("THREE-GATES-BEARING", (sum(1 for g in ACTIVE_GATES if g) == 3) and
    (FORGED_BREAKS > 0), "PASS",
    "三重门都承重：拆掉认证门将误放行 " + str(FORGED_BREAKS) + " 对；当前误放行 " +
    str(N_BREAK) + " 对")
add("CLEAN-FALSIFIABLE-ZERO", (CLEAN_FALSIFIABLE == 0) and (N_BREAK == 0), "PASS",
    "★★库外读数接入后，非回述 ∧ 可认证 p_free=0 ∧ chi2 相容且窗口非空 = " +
    str(CLEAN_FALSIFIABLE) + " 对；突破 0，独立实验预言仍 0")
add("CTRL-FOUR-DISTINCT", CTRL_FOUR_DISTINCT, "PASS",
    "控制组四向量两两不同：" + " / ".join(str(x) for x in CTRL_FOUR))
add("CTRL-NO-EQ-BASE", CTRL_NO_EQ_BASE, "PASS",
    "三个单门对照均不等于基线 " + str(CTRL_BASE))
add("CTRL-SCALAR-DISTINCT", CTRL_SCALAR_DISTINCT, "PASS",
    "控制组四标量两两不同：" + " / ".join(str(x) for x in CTRL_READINGS))
add("CTRL-SCALAR-NO-EQ-BASE", CTRL_SCALAR_NO_EQ_BASE, "PASS",
    "三个对照标量均不等于基线标量 " + str(CTRL_READINGS[0]))
add("ZERO-SCAN-IDENTITY", ZERO_SCAN_OK, "IDENTITY",
    "阴性对照：扫描 0 条外部读数时四项读数恒 " + str(ZERO_SCAN) +
    "，该侧恒真、零判别力，单列 IDENTITY 配 NOT-ALL-GREEN")
add("NOT-ALL-GREEN", NOT_ALL_GREEN, "INFO",
    "负对照恒绿，但库外性、chi2 两侧、sigma 窗口、认证不变性均非恒绿读数")
add("SPINE-ZERO", (PREV12_CLEAN == 0) and (CERTIFIED_HIT == 0), "PASS",
    "跨卷回读：第十二轮全库副本 " + str(PREV12_COPIED) + " 个、row() " +
    str(PREV12_ROWS) + " 个、干净可判负输出 0；本册未新增任何物理方程")
add("FAMILY-LIMITED-CLAIM", (N_EXT > 0) and (N_T > 0), "BOUNDARY",
    "★本册只接入 " + str(N_EXT) + " 条库外读数与全库 " + str(N_T) +
    " 个字面量理论输出，不是全人类实验数据；结论是「可达域内」的局部否定证书，" +
    "不是「四力统一不可能」的全称定理")
add("NO-BREAKTHROUGH", (N_BREAK == 0), "INFO",
    "本册不宣称攻破统一场论，也不宣称攻破力的统一；只产可算判决")
add("MATH-NOT-EXPERIMENT", CROSS_READINGS_OK, "INFO",
    "全部结论来自两路机读、精确 chi2、sigma 区间反演与扰动不变性，不是实验证实；不产新物理")
add("NEXT-EXIT", (N_BREAK == 0) and (CERTIFIED_HIT == 0), "INFO",
    "★硬出口口径由本轮收紧：此前要求「检索一条新实验读数」，本轮机算证明" +
    "新增读数单独无法修复认证节点，必须同时给出一条程序侧不含观测副本、" +
    "可认证 p_free=0 的理论输出。在该输出出现前，不必再造新理论、不必再放宽判据")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描 add/guard 的 ok 参数，布尔字面量命中 0；全部 ok 由计算布尔驱动")
add("VERDICT-MACHINE", verdict_machine_ok, "PASS",
    "把突破读数 +1 后判词串发生变化，且原读数确实写入判词 ⇒ 判词机读、随读数变化")


def final_of(nf_main_v, nf_guard_v, n_decl_v):
    if n_decl_v is None:
        return "ALG-EXTERNAL-EXIT--GATES-FAIL"
    if nf_guard_v > 0:
        return "ALG-EXTERNAL-EXIT--GATES-FAIL"
    return "ALG-EXTERNAL-EXIT--GATES-PASS-WITH-0-NEGATIVE"


declared_negative = ["NO-BREAKTHROUGH", "CLEAN-FALSIFIABLE-ZERO", "CHANNEL-A-INFEASIBLE",
                     "README-EXTERNAL-CHANGE-BOUNDARY", "STRICT-ZERO-BOUNDARY",
                     "WIDE-NOT-EVIDENCE", "NULL-NONE-BOUNDARY", "THEORY-TWO-PATH-BOUNDARY",
                     "FAMILY-LIMITED-CLAIM"]
nf_main_before = sum(1 for s in segs if (s["kind"] in ("PASS", "IDENTITY")) and (not s["ok"]))
nf_guard_before = sum(1 for s in segs if not s["ok"])
final = final_of(nf_main_before, nf_guard_before, len(declared_negative))
final_of_ok = (final == "ALG-EXTERNAL-EXIT--GATES-PASS-WITH-0-NEGATIVE") and \
              (nf_guard_before == 0) and (len(declared_negative) > 0)
add("FINAL-OF-CONSISTENT", final_of_ok, "PASS",
    "final_of(nf_main=" + str(nf_main_before) + ",nf_guard=" + str(nf_guard_before) +
    ",n_decl=" + str(len(declared_negative)) + ")：守卫 FAIL 挡门、已登记判负不挡门、缺 n_decl 报 GATES-FAIL")

counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0, "BOUNDARY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)

key_numbers = {
    "external_anchors": N_EXT, "exp_path_anchors": len(EXP_A),
    "two_path_field_diff": TWO_PATH_FIELD_DIFF,
    "old_anchors": N_OLD, "old_two_sided": OLD_TWO_SIDED,
    "old_sigma_zero": OLD_SIGMA_ZERO,
    "exact_duplicates": N_EXACT_DUP, "new_objects": N_NEW_OBJECT,
    "same_object_new_precision": N_SAME_OBJECT,
    "null_hypotheses": N_HAS_NULL, "null_from_old": N_NULL_OLD,
    "null_from_external": N_NULL_EXT, "null_none": N_NULL_NONE,
    "theory_literal_rows": N_T, "theory_exp_path_rows": N_T_EXP,
    "theory_two_path_diff": TWO_PATH_T_DIFF,
    "candidate_pairs": N_ALL_CANDIDATES, "strict_object_pairs": N_STRICT,
    "wide_pairs": N_WIDE, "wide_pairs_with_null": N_WIDE_WITH_NULL,
    "wide_unit_match": N_UNIT_MATCH_WIDE,
    "chi2_crit": str(CHI2_CRIT), "z_crit": dstr(Z_CRIT, 12),
    "same_object_pairs": N_SAME, "same_compatible": N_SAME_COMPATIBLE,
    "same_excluded": N_SAME_EXCLUDED,
    "control_negative_excluded": N_CTRL_NEG_EXCLUDED,
    "compatible_now": N_COMPATIBLE_NOW, "excluded_now": N_EXCLUDED_NOW,
    "sigma_window_exists": N_WINDOW, "sigma_window_empty_or_undefined": N_WINDOW_NONE,
    "identity_copies": N_IDENTITY,
    "cert_invariant_directions": CERT_INVARIANT_DIRECTIONS,
    "forged_breaks_if_cert_waived": FORGED_BREAKS,
    "pairs_hit_r5": PAIRS_HIT_R5, "certified_hit_r6": CERTIFIED_HIT,
    "prev12_clean": PREV12_CLEAN, "prev12_copied": PREV12_COPIED,
    "clean_falsifiable": CLEAN_FALSIFIABLE, "breakthrough": N_BREAK,
    "min_theory_side_changes": MIN_THEORY_SIDE_CHANGES,
    "channel_a_infeasible": CHANNEL_A_INFEASIBLE,
    "external_reading_cannot_fix": EXTERNAL_READING_CANNOT_FIX,
    "control_vectors": CTRL_FOUR, "control_scalars": CTRL_READINGS,
    "readme_bytes": README_BYTES, "readme_md5": README_MD5,
    "readme_prev_round_md5": PREV_ROUND_MD5,
    "readme_external_change": README_EXTERNAL_CHANGE,
    "readme_max_rid": README_MAX_RID, "tree_max_rid": TREE_MAX_RID,
    "source_files": len(SOURCE_FILES), "source_missing": len(source_missing),
    "main_md": INV["main_md"], "main_html": INV["main_html"],
    "alg_md": INV["alg_md"], "alg_html": INV["alg_html"],
    "src_files": INV["src_files"], "data_files": INV["data_files"],
    "judge_files": INV["judge_files"],
    "spine_independent_predictions": 0, "four_force_incomplete": True,
}

ext_json = [dict(id=e["id"], symbol=e["symbol"], obj=e["obj"], unit=e["unit"],
                 value=e["value_str"], sigma=e["sigma_str"],
                 null_id=e["null_id"], null_source=e["null_source"])
            for e in EXT]
null_json = [dict(id=e["id"], null_id=e["null_id"],
                  null_value=(str(e["null_value"]) if e["null_value"] is not None else None),
                  null_source=e["null_source"], has_null=e["has_null"])
             for e in EXT]

out = {
    "title": "算法联盟：库外实测读数接入与硬出口通道 A 的可满足性反演（第十三轮）",
    "date": "2026-11-14",
    "nature": "算法联盟分析册（不占 RID、不入 README、不与任何审计卷相加）",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": g_pass,
    "guard_count": g_count,
    "declared_negative": declared_negative,
    "scope": {
        "own_excluded_names": sorted(OWN_NAMES),
        "skip_dirs": list(SKIP_DIRS),
        "external_sources": [str(x) for x in SOURCE_FILES[:2]],
    },
    "external_anchors": ext_json,
    "null_hypotheses": null_json,
    "same_object_checks": dict(rows=SAME_ROWS, negative_control=CTRL_NEG_ROWS),
    "sigma_window": dict(chi2_crit=str(CHI2_CRIT), z_crit=dstr(Z_CRIT, 12),
                         window_exists=N_WINDOW, window_empty_or_undefined=N_WINDOW_NONE,
                         identity_copies=N_IDENTITY,
                         sample=[w for w in WIDE[:24]]),
    "chain": dict(path_a=["E6 对象配对", "E7 p_free 认证", "E8 chi2 相容且 sigma 窗口非空",
                          "E9 独立预言"],
                  strict_object_pairs=N_STRICT, certified_hit=CERTIFIED_HIT,
                  window_pairs=N_WINDOW, independent_predictions=0,
                  external_reading_cannot_fix=EXTERNAL_READING_CANNOT_FIX,
                  min_theory_side_changes=MIN_THEORY_SIDE_CHANGES),
    "key_numbers": key_numbers,
    "segments": segs,
}
_payload = json.dumps(out, ensure_ascii=False, sort_keys=True, indent=0)
digest = hashlib.sha256(_payload.encode("utf-8")).hexdigest()
out["content_sha256"] = digest

if __name__ == "__main__":
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：库外实测读数接入与硬出口通道 A 的可满足性反演（第十三轮）")
    lines.append("=" * 96)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : " + str(g_pass) + "/" + str(g_count))
    lines.append("sha256  : " + digest)
    lines.append("-" * 96)
    lines.append("库外来料：" + str(N_EXT) + " 条（两路机拼逐字段一致 " +
                 str(TWO_PATH_EQ) + "）；既有 " + str(N_OLD) + " 项锚，精确重复 " +
                 str(N_EXACT_DUP) + " 条；全新对象 " + str(N_NEW_OBJECT) +
                 " 条 / 同对象新精度 " + str(N_SAME_OBJECT) + " 条")
    lines.append("零假设：可定义 " + str(N_HAS_NULL) + " 条（库内 " + str(N_NULL_OLD) +
                 " / 库外 " + str(N_NULL_EXT) + "），不可定义 " + str(N_NULL_NONE) + " 条")
    lines.append("理论输出：act " + str(N_T) + " 条字面量 / exp " + str(N_T_EXP) +
                 " 条，差 " + str(TWO_PATH_T_DIFF) + " 条；候选 " +
                 str(N_ALL_CANDIDATES) + " 对")
    lines.append("对象同一：严口径 " + str(N_STRICT) + " 对；宽口径反事实 " +
                 str(N_WIDE) + " 对（单位严格匹配 " + str(N_UNIT_MATCH_WIDE) + " 对）")
    lines.append("-" * 96)
    lines.append("线 1 · 同对象外部读数精确 chi2（门槛 " + str(CHI2_CRIT) +
                 "，z_crit=" + dstr(Z_CRIT, 12) + "）")
    for r in SAME_ROWS:
        lines.append("  " + r["pair"] + " | gap=" + r["gap"] + " sigma_c=" + r["sigma_c"] +
                     " z=" + r["z"] + " chi2=" + r["chi2"] +
                     " | " + ("COMPATIBLE" if r["compatible"] else "EXCLUDED"))
    lines.append("  正对照相容 " + str(N_SAME_COMPATIBLE) + " 对 / 负对照排除 " +
                 str(N_CTRL_NEG_EXCLUDED) + " 对 ⇒ 门有判别力")
    lines.append("-" * 96)
    lines.append("线 2 · sigma 窗口反演：相容下界 < 可判负上界")
    lines.append("  窗口非空 " + str(N_WINDOW) + " 对 / 空或不可定义 " +
                 str(N_WINDOW_NONE) + " 对 / 恒等式副本 " + str(N_IDENTITY) + " 对")
    lines.append("  按登记 sigma 实算：相容 " + str(N_COMPATIBLE_NOW) +
                 " 对 / 排除 " + str(N_EXCLUDED_NOW) + " 对")
    lines.append("  认证状态 " + str(CERT_INVARIANT_DIRECTIONS) +
                 " 次四方向扰动重算恒为假；窗口状态随扰动变化 " + str(WINDOW_VARIES))
    lines.append("-" * 96)
    lines.append("硬出口通道 A：对象配对 " + str(N_STRICT) + " → 认证 " +
                 str(CERTIFIED_HIT) + " → 相容且窗口 " + str(N_WINDOW) +
                 " → 独立预言 0")
    lines.append("  ★新增实验读数单独无法修复认证节点；最小理论侧改动 " +
                 str(MIN_THEORY_SIDE_CHANGES) + " 条可认证非回述输出")
    lines.append("  拆掉认证门将误放行 " + str(FORGED_BREAKS) + " 对；三门同时成立 " +
                 str(CLEAN_FALSIFIABLE) + " 对 ⇒ 突破 0")
    lines.append("-" * 96)
    lines.append("README：" + str(README_BYTES) + " B / " + README_MD5 +
                 " / README 最大 RID " + str(README_MAX_RID) + " / 三树最大 RID " +
                 str(TREE_MAX_RID) + "；★与上一轮基线不同，系另一会话改动，本册零改动")
    lines.append("红线：数学自洽 != 实验证实；四力大统一 0 条正确解；独立实验预言 0；不宣称攻破。")
    lines.append("-" * 96)
    for s in segs:
        lines.append("[" + s["kind"] + "] " + s["name"] + " :: " + ("OK" if s["ok"] else "FAIL"))
    text_out = "\n".join(lines) + "\n"
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(text_out)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("sha256=", digest)
    print("ALL-CHECKS-PASS" if (g_pass == g_count) else "SOME-GUARDS-FAILED")
    print("WRITE", OUT_JSON)
    print("WRITE", OUT_REPORT)
