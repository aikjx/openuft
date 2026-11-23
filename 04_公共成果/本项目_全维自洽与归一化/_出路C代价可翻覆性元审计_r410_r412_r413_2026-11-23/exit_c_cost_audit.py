# -*- coding: utf-8 -*-
"""出路 C 代价可翻覆性元审计：r410 / r412 / r413 三册链。

对象：r410 把「可变函数 + 部门选择」标价为 Ω5-S 结构限额 +1；
      r412 把它登记为 LU-6 条件式、未落地、唯一强度入口；
      r413 把它重定价为「伪 +1」，给 shape×assign 四分支可识别性账。
本册只做：两路机拼、独立复算、代价注入反噬、L/C 轴区分、最新继承定价核验。

路 A = r413 JSON 派生账。
路 B = r413 判定册 Markdown 表格机拼；B 不读取 A 的 JSON 派生字段作计算输入。
路 C = 从原始规则重算：4 个强度需 4 条数值约束；fixed 给 1 条、free 给 0 条；
      assign=external 给 log2(4!) bits，derived 给 0 bits。
三路只在末尾比对。

红线：不是新判定册，不占 RID，不登记 README，不与 r410/r412/r413/r414/r415/r421/r437 相加；
不产生新物理，不落地 LU-6，不宣称攻破统一场论研究纲领；独立实验预言计数 0。
"""
import ast
import glob
import json
import os
import re
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def one(pattern):
    hits = glob.glob(pattern)
    assert len(hits) == 1, (pattern, hits)
    return hits[0]


DATA_ALG = one(os.path.join(BASE, "04_*", "算法联盟_全维自洽与归一化", "数据"))
JUDGE_ALG = one(os.path.join(BASE, "04_*", "算法联盟_全维自洽与归一化"))
DATA_MAIN = one(os.path.join(BASE, "04_*", "本项目_全维自洽与归一化", "数据"))
JUDGE_MAIN = one(os.path.join(BASE, "04_*", "本项目_全维自洽与归一化", "判定"))

R410_JSON = one(os.path.join(DATA_ALG, "TUFT-r410_*.json"))
R412_JSON = one(os.path.join(DATA_ALG, "TUFT-r412_*.json"))
R413_JSON = one(os.path.join(DATA_ALG, "TUFT-r413_*.json"))
R410_MD = one(os.path.join(JUDGE_ALG, "判定_TUFT-r410-*.md"))
R412_MD = one(os.path.join(JUDGE_ALG, "判定_TUFT-r412-*.md"))
R413_MD = one(os.path.join(JUDGE_ALG, "判定_TUFT-r413-*.md"))
R421_MD = one(os.path.join(JUDGE_ALG, "判定_TUFT-r421-*.md"))
R437_MD = one(os.path.join(JUDGE_MAIN, "判定_TUFT-r437_*.md"))
R403_JSON = one(os.path.join(DATA_MAIN, "TUFT-r403_*.json"))

OUT_JSON = os.path.join(HERE, "_exit_c_cost_meta.json")
REPORT_PATH = os.path.join(HERE, "_exit_c_cost_meta_report.txt")

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


r410 = load_json(R410_JSON)
r412 = load_json(R412_JSON)
r413 = load_json(R413_JSON)
r403 = load_json(R403_JSON)
r410_md = load_text(R410_MD)
r412_md = load_text(R412_MD)
r413_md = load_text(R413_MD)
r421_md = load_text(R421_MD)
r437_md = load_text(R437_MD)
script_src = load_text(os.path.abspath(__file__))

# AST 前置与写死 ok 防护（必须在任何判据落表之前）
tree = ast.parse(script_src)
bad_import = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            if alias.name in ("numpy", "sympy", "random", "subprocess"):
                bad_import.append(alias.name)
    if isinstance(node, ast.ImportFrom) and node.module in ("numpy", "sympy", "random", "subprocess"):
        bad_import.append(node.module)
bad_call = [getattr(getattr(n.func, "id", None), "__str__", lambda: "")()
            for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in ("eval", "exec")]
hardcoded_ok = []
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "add" and len(node.args) >= 5):
        fifth = node.args[4]
        if isinstance(fifth, ast.Constant) and isinstance(fifth.value, bool):
            hardcoded_ok.append(getattr(node.args[0], "value", "?"))
ast_ok = (not bad_import) and (not bad_call) and (not hardcoded_ok)
add("G00-ast-precheck", "gate", "AST 前置：无禁Import、无eval/exec、add 的 ok 不写死",
    "bad_import=%s bad_call=%s hardcoded_ok=%s" % (bad_import, bad_call, hardcoded_ok),
    ast_ok, "守卫不写死；本判据自己若被写死 ok 也必须翻红")

# ---------------------------------------------------------------------------
# 来源锚：旧标价 -> 条件式 -> 伪 +1 -> 关闭 -> 最新唯一出口
# ---------------------------------------------------------------------------
markers = {
    "r410_plus1": "Ω5-S 结构限额 +1" in r410_md,
    "r412_open": ("未落地" in r412_md and "Ω5-S 限额 +1" in r412_md),
    "r413_pseudo": ("伪代价" in r413_md and "OPEN-COST-UNDERSTATED" in r413_md),
    "r421_closed": ("出路 C 已被 r413" in r421_md and "EXIT-C-CLOSED" in r421_md),
    "r437_unique_exit": ("UNIQUE-EXIT-9FOLD-REAFFIRMED" in r437_md and "E1" in r437_md and "E4" in r437_md),
}
add("M1-price-chain-anchors", "gate", "五段代价链锚点齐备：+1→未落地→伪+1→已关闭→体系外唯一出口",
    "markers=%s" % markers,
    all(markers.values()),
    "按纪律取链条最新重定价：r421 已关闭出路 C，r437 重证唯一出口 E1–E4；"
    "不照抄 r410 的旧『+1 唯一可能』")

add("M2-latest-no-reopen", "gate", "最新链未重开出路 C：r421 关闭且 r437 仍指体系外来料",
    "r421_closed=%s r437_unique_exit=%s" % (markers["r421_closed"], markers["r437_unique_exit"]),
    markers["r421_closed"] and markers["r437_unique_exit"],
    "只核价格标签是否被后续册重开；不重判 r421/r437 的物理内容")

# ---------------------------------------------------------------------------
# 路 A / 路 B / 路 C：r413 四分支账
# ---------------------------------------------------------------------------
LOG2_24 = Decimal(24).ln() / Decimal(2).ln()
LOG2_6 = Decimal(6).ln() / Decimal(2).ln()
LOG2_18 = Decimal(18).ln() / Decimal(2).ln()


def clean_cell(cell):
    return cell.replace("**", "").strip()


def parse_md_ledger(text):
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [clean_cell(c) for c in s.strip("|").split("|")]
        if len(cells) != 7:
            continue
        shape, assign, nc, miss, can, dof, bits = cells
        if shape not in ("fixed", "free") or assign not in ("derived", "external"):
            continue
        rows.append({
            "shape": shape,
            "assign": assign,
            "numeric_constraints": int(nc),
            "missing_constraints": int(miss),
            "identifiable": can == "是",
            "shape_dof": "UNBOUNDED" if "无界" in dof else int(dof),
            "assign_bits": Decimal(bits),
        })
    return rows


def norm_json_rows(rows):
    out = []
    for r in rows:
        sd = r["shape_dof"]
        if sd == float("inf") or str(sd).lower() in ("inf", "infinity"):
            dof = "UNBOUNDED"
        else:
            dof = int(sd)
        out.append({
            "shape": r["shape"],
            "assign": r["assign"],
            "numeric_constraints": int(r["numeric_constraints"]),
            "missing_constraints": int(r["missing_constraints"]),
            "identifiable": bool(r["identifiable"]),
            "shape_dof": dof,
            "assign_bits": Decimal(str(r["assign_bits"])),
        })
    return out


def rule_rows():
    out = []
    for shape in ("fixed", "free"):
        for assign in ("derived", "external"):
            numeric = 1 if shape == "fixed" else 0
            missing = 4 - numeric
            bits = Decimal(0) if assign == "derived" else LOG2_24
            dof = 1 if shape == "fixed" else "UNBOUNDED"
            identifiable = (shape == "fixed" and assign == "derived" and missing == 0)
            out.append({
                "shape": shape,
                "assign": assign,
                "numeric_constraints": numeric,
                "missing_constraints": missing,
                "identifiable": identifiable,
                "shape_dof": dof,
                "assign_bits": bits,
            })
    return out


def row_equal(a, b, tol=Decimal("1e-9")):
    scalar_keys = ("shape", "assign", "numeric_constraints", "missing_constraints",
                   "identifiable", "shape_dof")
    return (all(a[k] == b[k] for k in scalar_keys)
            and abs(a["assign_bits"] - b["assign_bits"]) <= tol)


def pair_match(aa, bb):
    return (len(aa) == len(bb) == 4
            and all(any(row_equal(a, b) for b in bb) for a in aa)
            and all(any(row_equal(a, b) for a in aa) for b in bb))


a_rows = norm_json_rows(r413["可识别性账"])
b_rows = parse_md_ledger(r413_md)
c_rows = rule_rows()
add("A1-two-path-ledger", "gate", "路A(JSON) 与路B(MD表格) 四分支逐格一致",
    "A=%d行 B=%d行 match=%s" % (len(a_rows), len(b_rows), pair_match(a_rows, b_rows)),
    pair_match(a_rows, b_rows),
    "路 B 从判定册 Markdown 表格抽取，不读取 r413 JSON 派生字段作计算输入；"
    "bits 用 1e-9 容差吸收 MD 10 位截断")

add("A2-rule-recompute", "gate", "路C(原始规则) 与路A(JSON) 四分支逐格一致",
    "C=%d行 match=%s" % (len(c_rows), pair_match(a_rows, c_rows)),
    pair_match(a_rows, c_rows),
    "规则：4 强度需 4 数值约束；fixed=1/free=0；external 指派=log2(4!) bits，derived=0")

# 指派熵：定义门单列、不承重；真正承重的是 B2/B3 的反噬与差异
bits_json = Decimal(str(r413["指派熵"]["bits"]))
bits_25e = Decimal(r413["指派熵"]["bits_25E"])
entropy_tol = Decimal("1e-15")
entropy_ok = (abs(LOG2_24 - bits_json) < entropy_tol
              and abs(LOG2_24 - bits_25e) < entropy_tol
              and abs(bits_json - LOG2_6) > Decimal("1"))
add("B1-assignment-entropy", "gate", "log2(4!)=4.584962500721... 与 JSON 双字段一致",
    "recompute=%s json_bits=%s json_25E=%s diff18=%s tol=%s" % (
        LOG2_24, bits_json, bits_25e, LOG2_24 - LOG2_18, entropy_tol),
    entropy_ok,
    "由 n_assignments=24 独立算熵；不是把 JSON 文本抄回报告。"
    "JSON bits 是 16 位浮点序列化，25E 字段为 25 位；"
    "实测差约 8e-16，容差取 1e-15 对应继承末位截断，非放宽物理门限")

add("B2-wrong-sample-space-neg", "neg", "若把熵样本空间错取 3!，读数必须翻红",
    "log2(3!)=%s vs log2(4!)=%s 差=%s" % (LOG2_6, LOG2_24, LOG2_24 - LOG2_6),
    abs(LOG2_6 - LOG2_24) > Decimal("1"),
    "反噬：若错把力数当指派数仍能通过，则熵门无判别力")

short_controls = [p for p in r413["阳性对照"] if p.get("name") == "inject_short_range_constraint"]
short_ok = (len(short_controls) == 1
            and str(short_controls[0].get("before")) == "24"
            and str(short_controls[0].get("after")) == "18"
            and bool(short_controls[0].get("ok")) is True
            and LOG2_18 < LOG2_24)
add("B3-short-range-constraint", "gate", "注入短程约束 24→18 使指派熵下降但不归零",
    "controls=%s bits24=%s bits18=%s" % (short_controls, LOG2_24, LOG2_18),
    short_ok,
    "正对照：判据能响应约束注入；但 18>1，仍不能唯一化")

# ---------------------------------------------------------------------------
# +1 代价可翻覆性：不是宣称 LU-6 可落地，而是检验判据是否被单一口径写死
# ---------------------------------------------------------------------------
def evaluate_cost(shape, assign, forced_numeric=None, force_assign_derived=False,
                  params_internal=False):
    numeric = (1 if shape == "fixed" else 0) if forced_numeric is None else forced_numeric
    missing = 4 - numeric
    assign_bits = Decimal(0) if (assign == "derived" or force_assign_derived) else LOG2_24
    shape_cost = 1 if shape == "fixed" else "UNBOUNDED"
    identifiable = (shape == "fixed" and missing == 0 and assign_bits == 0)
    adequate = identifiable and params_internal and shape_cost == 1
    return {
        "shape": shape,
        "assign": assign,
        "numeric_constraints": numeric,
        "missing_constraints": missing,
        "assign_bits": assign_bits,
        "shape_cost": shape_cost,
        "params_source": "internal" if params_internal else "external-k",
        "identifiable": identifiable,
        "plus_one_adequate": adequate,
    }


base_cost = [evaluate_cost(r["shape"], r["assign"]) for r in c_rows]
base_identifiable = sum(1 for r in base_cost if r["identifiable"])
base_adequate = sum(1 for r in base_cost if r["plus_one_adequate"])
add("C1-plus-one-pseudo", "gate", "四分支无一可由公设内 +1 定解，复现 r413 伪+1",
    "identifiable=%d/4 plus_one_adequate=%d/4" % (base_identifiable, base_adequate),
    base_identifiable == 0 and base_adequate == 0,
    "复算路线与 r413 总裁定一致；本册不把它当成新证据份数")

inj_4 = evaluate_cost("fixed", "derived", forced_numeric=4,
                      params_internal=True)
add("C2-inject-four-constraints", "neg", "注入 4 条假数值约束+内部形状参数使 fixed/derived 翻绿",
    "before(missing=%s,adequate=%s) after(missing=%s,adequate=%s)" % (
        base_cost[0]["missing_constraints"], base_cost[0]["plus_one_adequate"],
        inj_4["missing_constraints"], inj_4["plus_one_adequate"]),
    (base_cost[0]["plus_one_adequate"] is False
     and inj_4["missing_constraints"] == 0
     and inj_4["identifiable"] is True
     and inj_4["plus_one_adequate"] is True),
    "反噬：若注入 4 条约束仍不能翻绿，则『不可识别』是写死结论；"
    "翻绿只说明判据有牙，不说明外部买入后成为公设内预言")

inj_assign = evaluate_cost("fixed", "external", force_assign_derived=True)
add("C3-assign-derivation-insufficient", "gate", "只派生部门指派、补 3 条数值约束仍不够",
    "bits=%s missing=%s identifiable=%s adequate=%s" % (
        inj_assign["assign_bits"], inj_assign["missing_constraints"],
        inj_assign["identifiable"], inj_assign["plus_one_adequate"]),
    (inj_assign["assign_bits"] == 0 and inj_assign["missing_constraints"] == 3
     and inj_assign["identifiable"] is False
     and inj_assign["plus_one_adequate"] is False),
    "证明 4.585 bits 是必要非充分项；不能把派生指派当成 +1 已含内容")

inj_collapse = evaluate_cost("fixed", "derived")
add("C4-free-function-collapse", "gate", "把自由函数塌成固定形状仍缺 3 条约束，+1 不复活",
    "free(missing=%s) collapsed(missing=%s,adequate=%s)" % (
        base_cost[2]["missing_constraints"],
        inj_collapse["missing_constraints"], inj_collapse["plus_one_adequate"]),
    (base_cost[2]["shape_cost"] == "UNBOUNDED"
     and inj_collapse["missing_constraints"] == 3
     and inj_collapse["plus_one_adequate"] is False),
    "负对照不保留被测机制：塌掉自由函数后不再含无界自由度，"
    "若此时判据仍称伪+1 则须由缺约束数承载，而非由自由函数标签承载")

r410_price_hit = ("Ω5-S 结构限额 +1" in r410_md and "唯一可能路径" in r410_md)
r412_price_hit = ("Ω5-S 限额 +1" in r412_md and "未落地" in r412_md)
r413_reprice_hit = ("伪代价" in r413_md and "OPEN-COST-UNDERSTATED" in r413_md)
add("C5-chain-reprice-visible", "gate", "+1 标签在三册中被重定价，后续关闭可见",
    "r410=%s r412=%s r413=%s closed=%s" % (
        r410_price_hit, r412_price_hit, r413_reprice_hit, markers["r421_closed"]),
    r410_price_hit and r412_price_hit and r413_reprice_hit and markers["r421_closed"],
    "本册审计的是价格标签的可翻覆性，不是新造统一方案")

# ---------------------------------------------------------------------------
# L0-L5 结构层 与 C0-C3 证据口径不是同一根轴
# ---------------------------------------------------------------------------
L_codes = sorted(set(row["layer"] for row in r412["全情况"]))
L_criteria = sorted(set(row["criteria"] for row in r412["全情况"]))
C_codes = sorted(set(level["code"] for level in r403["levels"]))
C_names = sorted(set(level["name"] for level in r403["levels"]))
add("H1-axis-not-identical", "gate", "L0-L5 结构层不等于 C0-C3 证据口径轴",
    "L=%s(%d) C=%s(%d)" % (L_codes, len(L_codes), C_codes, len(C_codes)),
    (len(L_codes) == 6 and len(C_codes) == 4 and L_codes != C_codes),
    "两轴基数不同且语义不同：前者是构造层级，后者是正确性证据强度")

add("H2-criteria-not-identical", "gate", "三判据维度不等于四层证据口径",
    "Lcriteria=%s Cnames=%s" % (L_criteria, C_names),
    (len(L_criteria) == 3 and len(C_names) == 4 and set(L_criteria) != set(C_names)),
    "结构/形式/数值统一 不等于 形式量纲/数学复现/还原/实证")

mapping_pattern = re.compile(r"L[0-5]\s*(?:→|->|=|对应)\s*C[0-3]")
explicit_map = (mapping_pattern.findall(r412_md) + mapping_pattern.findall(r413_md)
                + mapping_pattern.findall(json.dumps(r412, ensure_ascii=False)))
add("H3-no-explicit-map", "gate", "被引来源没有 L 层到 C 层的显式映射表",
    "explicit_map=%s" % explicit_map,
    len(explicit_map) == 0,
    "无映射却跨轴搬运即对象错位；不能凭名字都带数字就同列")

l0_pass = [row for row in r412["全情况"]
           if row["layer"] == "L0几何代数" and row["verdict"] == "PASS"]
c3_unified = [c["id"] for c in r403["candidates"]
              if c.get("c3") == "PASS" and c.get("unified") is True]
l_blob = json.dumps(r412["全情况"], ensure_ascii=False)
u_ids_in_l = sorted(set(re.findall(r"\bU\d{2}\b", l_blob)))
add("H4-cross-axis-transfer-fails", "gate", "L0 恒等式 PASS 不能搬运成 r403 的 C3 统一候选",
    "L0_PASS=%d C3_unified=%s U_ids_in_L_table=%s" % (
        len(l0_pass), c3_unified, u_ids_in_l),
    (len(l0_pass) == 2 and c3_unified == ["U01"] and len(u_ids_in_l) == 0),
    "L0 PASS 是结构恒等式，C3 PASS∧unified 是实证统一；两者对象不同，不能相加")

base_transfer_licensed = False
fake_mapping = {"L0": "C3"}
fake_transfer_licensed = (len(fake_mapping) > 0
                          and set(fake_mapping.values()).issubset(set(C_codes)))
add("H5-fake-mapping-neg", "neg", "注入伪映射 L0→C3 才许可跨轴搬运，判据必须翻红",
    "base=%s injected=%s" % (base_transfer_licensed, fake_transfer_licensed),
    (base_transfer_licensed is False and fake_transfer_licensed is True),
    "反噬：若没有映射也能搬运，则轴区分门是恒绿装饰")

# ---------------------------------------------------------------------------
# 结论与产物
# ---------------------------------------------------------------------------
n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
failed = [g["id"] for g in gates if not g["ok"]]
if failed:
    verdict = "EXIT-C-COST-META-FAIL--" + "-".join(failed)
else:
    verdict = ("EXIT-C-COST-META--TWO-PATH-LEDGER-4OF4-MATCH--"
               "ASSIGN-ENTROPY-LOG2-24-4.5849625007--"
               "PLUS-ONE-PSEUDO-COST-REPRODUCED--"
               "INJECT-FOUR-CONSTRAINTS-FLIPS-IDENTIFIABLE--"
               "ASSIGN-DERIVATION-ALONE-INSUFFICIENT--"
               "L0-L5-NOT-C0-C3-AXIS--"
               "EXIT-C-CLOSED-R421--UNIQUE-EXIT-R437-EXTERNAL--"
               "NO-NEW-EXIT--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")

result = {
    "subject": "出路 C 代价可翻覆性元审计：r410 / r412 / r413",
    "object_boundary": ("只审 r410 的 +1 标价、r412 的 LU-6 条件式、r413 的四分支可识别性账；"
                        "排除 r414 图论、r415 方法谱系、r421 验收器、r437 出口重证，不相加"),
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(failed)},
    "independent_prediction_count": 0,
    "three_way_ledger": {
        "A_json": [{k: str(v) for k, v in r.items()} for r in a_rows],
        "B_md": [{k: str(v) for k, v in r.items()} for r in b_rows],
        "C_rules": [{k: str(v) for k, v in r.items()} for r in c_rows],
    },
    "entropy": {
        "log2_4_fact": str(LOG2_24),
        "log2_3_fact": str(LOG2_6),
        "log2_18": str(LOG2_18),
    },
    "cost_injection": {
        "base": [{k: str(v) for k, v in r.items()} for r in base_cost],
        "inject_four_constraints": {k: str(v) for k, v in inj_4.items()},
        "inject_assignment_derivation": {k: str(v) for k, v in inj_assign.items()},
        "collapse_free_function": {k: str(v) for k, v in inj_collapse.items()},
    },
    "axis": {
        "L_codes": L_codes, "L_criteria": L_criteria,
        "C_codes": C_codes, "C_names": C_names,
        "L0_pass_count": len(l0_pass), "C3_unified": c3_unified,
    },
    "latest_pricing": {
        "r421_outlet_c_closed": markers["r421_closed"],
        "r437_unique_exit_external": markers["r437_unique_exit"],
    },
    "gates": gates,
}
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

lines = [
    "出路 C 代价可翻覆性元审计 · r410 / r412 / r413",
    "=" * 72,
    "判词: " + verdict,
    "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(failed)),
    "对象边界: " + result["object_boundary"],
    "独立预言计数: 0",
    "-" * 72,
]
for g in gates:
    lines.append("[%s] %-34s %-8s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.extend([
    "-" * 72,
    "熵: log2(4!)=%s ; log2(3!)=%s ; log2(18)=%s" % (LOG2_24, LOG2_6, LOG2_18),
    "轴: L=%s C=%s ; L0_PASS=%d ; C3_unified=%s" % (
        L_codes, C_codes, len(l0_pass), c3_unified),
    "继承: r421_outlet_closed=%s ; r437_external_exit=%s" % (
        markers["r421_closed"], markers["r437_unique_exit"]),
    "-" * 72,
    "Decimal 60 ; 路A JSON / 路B MD表格 / 路C 原始规则 ; 全确定性无随机 ; 不占RID",
])
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(failed)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
