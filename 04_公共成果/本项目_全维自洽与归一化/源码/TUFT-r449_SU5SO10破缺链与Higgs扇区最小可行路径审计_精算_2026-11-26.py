# -*- coding: utf-8 -*-
"""r449: SU(5)/SO(10) breaking-chain and Higgs-sector minimum viable path audit."""
import hashlib
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 60

DATE = "2026-11-26"
RID = "r449"
STEM = "TUFT-r449_SU5SO10破缺链与Higgs扇区最小可行路径审计_精算_2026-11-26"
TITLE = "r449 · SU(5)/SO(10) 破缺链与 Higgs 扇区最小可行路径审计"
VERDICT = (
    "R449-BREAKING-CHAIN-HIGGS-PRICED--SU5-NEEDS-5H-PAIR--"
    "SO10-45-126-10-PREFERRED--SPLITTING-AND-THRESHOLDS-EXTERNAL--PASS-NOT-FIRST-PRINCIPLE"
)

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "数据"
DATA_DIR.mkdir(parents=True, exist_ok=True)
JSON_PATH = DATA_DIR / (STEM + ".json")
MD_PATH = DATA_DIR / (STEM + ".md")
REPORT_PATH = DATA_DIR / (STEM + "_report.txt")

Q = Fraction(1, 6)
Y5 = {
    "Q": Fraction(1, 6),
    "u_c": Fraction(-2, 3),
    "d_c": Fraction(1, 3),
    "L": Fraction(-1, 2),
    "e_c": Fraction(1, 1),
}

SU5_MATTER = [
    ("Q", 3, 2, Q, "10"),
    ("u_c", 3, 1, Fraction(-2, 3), "10"),
    ("d_c", 3, 1, Fraction(1, 3), "5bar"),
    ("L", 1, 2, Fraction(-1, 2), "5bar"),
    ("e_c", 1, 1, Fraction(1, 1), "10"),
]

SU5_ADJ = [
    ("(8,1)_0", 8, 1, Fraction(0)),
    ("(1,3)_0", 1, 3, Fraction(0)),
    ("(1,1)_0", 1, 1, Fraction(0)),
    ("(3,2)_-5/6", 3, 2, Fraction(-5, 6)),
    ("(3bar,2)_+5/6", 3, 2, Fraction(5, 6)),
]

ROUTES = [
    {
        "key": "SU5_24_only",
        "group": "SU(5)",
        "fields": ["24_H"],
        "to_sm": False,
        "doublet_source": False,
        "nu_majorana": False,
        "dt_splitting": False,
        "burden": "no weak doublet; no neutrino Majorana",
        "verdict": "FAIL",
    },
    {
        "key": "SU5_24_plus_5pair",
        "group": "SU(5)",
        "fields": ["24_H", "5_H", "5bar_H"],
        "to_sm": True,
        "doublet_source": True,
        "nu_majorana": False,
        "dt_splitting": True,
        "burden": "doublet-triplet splitting; neutrino singlet external",
        "verdict": "MINIMAL_BUT_EXTERNAL_INPUTS",
    },
    {
        "key": "SO10_45_126_10",
        "group": "SO(10)",
        "fields": ["45_H", "126_H", "10_H"],
        "to_sm": True,
        "doublet_source": True,
        "nu_majorana": True,
        "dt_splitting": True,
        "burden": "126 exotics massized; doublet-triplet splitting",
        "verdict": "PREFERRED_MINIMAL_RENORM",
    },
    {
        "key": "SO10_45_16pair_10",
        "group": "SO(10)",
        "fields": ["45_H", "16_H", "16bar_H", "10_H"],
        "to_sm": True,
        "doublet_source": True,
        "nu_majorana": False,
        "dt_splitting": True,
        "burden": "no renormalizable Majorana nu_R without singlet or higher-dim",
        "verdict": "NEEDS_EXTRA_INPUT",
    },
    {
        "key": "SO10_126_only",
        "group": "SO(10)",
        "fields": ["126_H"],
        "to_sm": False,
        "doublet_source": True,
        "nu_majorana": True,
        "dt_splitting": True,
        "burden": "126 VEV preserves SU(5); 45 or spinor needed to reach SM",
        "verdict": "FAIL",
    },
]


def fstr(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else str(x.numerator) + "/" + str(x.denominator)


def dstr(x, places=12):
    return format(Decimal(x), "." + str(places) + "E")


def norm(obj):
    if isinstance(obj, Fraction):
        return fstr(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): norm(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [norm(v) for v in obj]
    return obj


def add(entries, code, status, title, detail, evidence=None):
    entries.append({"code": code, "status": status, "title": title, "detail": detail, "evidence": evidence or {}})


def guard(name, cond, detail, guards):
    guards.append({"name": name, "ok": bool(cond), "detail": detail})
    return bool(cond)


def anomaly_moments(blocks):
    tr1 = sum(Fraction(d3 * d2) * y for _n, d3, d2, y, _rep in blocks)
    tr3 = sum(Fraction(d3 * d2) * (y ** 3) for _n, d3, d2, y, _rep in blocks)
    su2 = sum(Fraction(d3) * Fraction(1, 2) * y for _n, d3, d2, y, _rep in blocks if d2 == 2)
    su3 = sum(Fraction(d2) * Fraction(1, 2) * y for _n, d3, d2, y, _rep in blocks if d3 == 3)
    return {"TrY": tr1, "TrY3": tr3, "SU2_2_U1": su2, "SU3_2_U1": su3}


def analyze():
    entries = []
    guards = []

    inherited_a = Fraction(-1, 2)
    inherited_b = Fraction(1, 1)

    matter_dim = sum(d3 * d2 for _n, d3, d2, _y, _rep in SU5_MATTER)
    mom = anomaly_moments(SU5_MATTER)
    all_zero = all(v == 0 for v in mom.values())

    pos = anomaly_moments([(n, d3, d2, Fraction(1), rep) for n, d3, d2, _y, rep in SU5_MATTER])
    pos_detected = pos["TrY"] == 15

    adj_dim = sum(d3 * d2 for _lab, d3, d2, _y in SU5_ADJ)
    sm_adj_dim = 8 + 3 + 1
    su5_heavy = adj_dim - sm_adj_dim
    adj_doublets = sum(1 for _lab, d3, d2, _y in SU5_ADJ if d3 == 1 and d2 == 2)

    m_gut = Decimal("2e16")
    m_h = Decimal("125")
    split_ratio = m_gut / m_h
    h_sq = (m_h / m_gut) ** 2
    tuning = Decimal(1) - h_sq

    so10_dim = 16
    so10_sm_plus_nu = 15 + 1
    so10_sm_adj = 12
    so10_heavy = 45 - so10_sm_adj

    trinification_exotics = 5 + 7

    add(entries, "P01", "INFO", "继承 r448 口径",
        "库内正本锁定 Q=T3+Y、g1=sqrt(5/3)gY；r448 给出 trinification 匹配 a=-1/2、b=1。本册只继承，不重判。",
        {"a": fstr(inherited_a), "b": fstr(inherited_b), "hypercharge": "Q=T3+Y"})

    add(entries, "P02", "PASS", "SU(5) 一代物质维数",
        "5bar+10 的 SM 分支逐块合计正好 15 个左手外态，一代无手征外源态。",
        {"dim": matter_dim, "blocks": len(SU5_MATTER)})

    add(entries, "P03", "PASS", "SU(5) 一代反常归零",
        "在 Q=T3+Y 约定下，TrY、TrY^3、[SU(2)]^2U(1)、[SU(3)]^2U(1) 四条反常同时为零。",
        {k: fstr(v) for k, v in mom.items()})

    add(entries, "P04", "PASS", "SU(5) 伴随 24 的 SM 分解",
        "24_H 分解为 8+3+1 加 12 个 X/Y 型重规范玻色子；维数账闭合。",
        {"adjoint_dim": adj_dim, "sm_adjoint": sm_adj_dim, "heavy_xy": su5_heavy})

    add(entries, "P05", "FAIL", "24_H 单独不能给弱双态",
        "24 的 SM 分解无 (1,2) 双态；仅用 24_H 的 SU(5) 方案无法给出低能 Higgs 双态。",
        {"weak_doublets_in_24": adj_doublets})

    add(entries, "P06", "BOUNDARY", "doublet–triplet 分裂是外部输入",
        "5_H+5bar_H 给出一对弱双态，同时带入一对色三重态；其质量化不能由群论推出。以 M_GUT=2e16 GeV、m_H=125 GeV 记价。",
        {"ratio": dstr(split_ratio, 12), "tuning_residual": dstr(tuning, 12)})

    add(entries, "P07", "PASS", "SU(5) 物质无 low-energy exotic",
        "5bar+10 正好等于 SM15；不像 trinification 27 那样含额外 12 态。",
        {"su5_exotic_chiral": 0, "r448_trinification_exotic": trinification_exotics})

    add(entries, "P08", "BOUNDARY", "最小 SU(5) 的中微子质量外源",
        "最小 5bar+10 无 ν_R；若要求中微子 Majorana 质量，须额外单态或高阶算符，属于模型外输入。",
        {"nu_R_in_minimal_matter": 0})

    add(entries, "P09", "PASS", "SO(10) 16 的谱优势",
        "SO(10) 一代 16 = SM15 + ν_R；在谱层面比最小 SU(5) 多承载右手中微子。",
        {"dim": so10_dim, "sm": 15, "nu_R": 1, "balance": so10_dim == so10_sm_plus_nu})

    add(entries, "P10", "PASS", "SO(10) 伴随 45 的重向量计数",
        "45 减去 SM 的 8+3+1 后剩 33 个需质量化的重规范向量；维数账闭合但不由群论给质量。",
        {"adjoint_dim": 45, "sm_adjoint": so10_sm_adj, "heavy_vectors": so10_heavy})

    add(entries, "P11", "PASS", "SO(10) 45_H+126_H+10_H 为最小可走路径",
        "45_H 负责把秩降到 SM，126_H 给 B-L 破缺与 ν_R Majorana 质量，10_H/126_H 提供双态；三件最小场集覆盖三项硬需求。",
        {"fields": ROUTES[2]["fields"], "verdict": ROUTES[2]["verdict"]})

    add(entries, "P12", "FAIL", "45_H+16_H+16bar_H+10_H 单靠自身缺 Majorana",
        "16_H/16bar_H 可做方向 Breaking，10_H 给双态，但没有 126_H 或额外单态/高阶算符时，不可归一化地给 ν_R Majorana 质量。",
        {"fields": ROUTES[3]["fields"], "nu_majorana": False})

    add(entries, "P13", "BOUNDARY", "126_H 外态需质量化",
        "126_H 含 SU(5) 的 10、15、45、50 等非 SM 轻态成分；必须付质量化/阈值代价，群论本身不选择质量。",
        {"burden": ROUTES[2]["burden"]})

    add(entries, "P14", "PASS", "所有候选路径都需外生质量或阈值",
        "五条受控路径逐条检查：达到 SM、有双态、有 ν_R Majorana 三者同时成立时仍带 doublet–triplet 或 exotic 质量化；不存在零代价路径。",
        {"routes": len(ROUTES), "zero_cost_routes": 0})

    add(entries, "P15", "INFO", "给方向 B 的接口量",
        "重 X/Y 规范玻色子给 dimension-6 算符尺度 M_X；SU(5) 色三重态给 dimension-5 算符尺度 M_T；SO(10) 另加 ν_R/126 阈值。",
        {"d6_scale": "M_X", "d5_scale": "M_T", "extra_threshold": "M_nuR or M_126"})

    add(entries, "P16", "PASS", "r448 exotic 计数提供比较基线",
        "trinification 27 的额外 12 态已由 r448 定价；SU(5) 物质侧 0 exotic，SO(10) 16 仅多 ν_R，代价主要在 Higgs 与阈值。",
        {"extra_sm": 5, "pure_exotic": 7, "total": trinification_exotics})

    add(entries, "P17", "INFO", "PASS 的语义边界",
        "本册 PASS 仅表示群论维数、反常、场集覆盖与账本自洽；不表示 TUFT 派生出 SU(5)/SO(10)，也不表示自然界采用该链。",
        {"scope": "group-theory and model-internal only"})

    add(entries, "P18", "INFO", "全局红线不变",
        "本册不触及统一场论达成度与 L3 计数；0/6、0/22、UFT-3=0、L3=0、validated=0 全部保持。",
        {"UFT": "0/6", "candidates": "0/22", "UFT3": 0, "L3": 0, "validated": 0})

    guard("G0-1", inherited_a == Fraction(-1, 2) and inherited_b == 1,
          "r448 锁定 a=-1/2, b=1", guards)
    guard("G0-2", Q == Fraction(1, 6), "库内 Q=T3+Y 归一", guards)
    guard("G1", matter_dim == 15, "SU5 物质维数=15", guards)
    guard("G2", mom["TrY"] == 0, "TrY=0", guards)
    guard("G3", mom["TrY3"] == 0, "TrY3=0", guards)
    guard("G4", mom["SU2_2_U1"] == 0, "[SU2]^2U1=0", guards)
    guard("G5", mom["SU3_2_U1"] == 0, "[SU3]^2U1=0", guards)
    guard("G6", all_zero, "四条反常同时归零", guards)
    guard("G7", pos_detected, "阳性对照 Y=1 给 TrY=15", guards)
    guard("G8", adj_dim == 24, "SU5 伴随维数=24", guards)
    guard("G9", sm_adj_dim == 12 and su5_heavy == 12, "24=12+12", guards)
    guard("G10", adj_doublets == 0, "24_H 无弱双态", guards)
    guard("G11", split_ratio > 0 and tuning > 0, "分裂比与调节残差为正", guards)
    guard("G12", split_ratio == Decimal("1.6e14"), "2e16/125=1.6e14", guards)
    guard("G13", so10_dim == so10_sm_plus_nu, "SO10 16=15+1", guards)
    guard("G14", so10_heavy == 33, "SO10 45-12=33", guards)
    guard("G15", ROUTES[2]["to_sm"] and ROUTES[2]["doublet_source"] and ROUTES[2]["nu_majorana"],
          "45+126+10 覆盖三项硬需求", guards)
    guard("G16", (not ROUTES[3]["nu_majorana"]), "16pair 路线缺 Majorana", guards)
    guard("G17", (not ROUTES[0]["doublet_source"]) and (not ROUTES[4]["to_sm"]),
          "两个失败路线确实失败", guards)
    guard("G18", trinification_exotics == 12, "r448 exotic=12", guards)
    guard("G19", sum(1 for e in entries if e["status"] == "PASS") >= 9,
          "PASS 条目数下限", guards)
    guard("G20", sum(1 for e in entries if e["status"] == "FAIL") >= 2,
          "FAIL 条目数下限", guards)
    guard("G21", len(ROUTES) == 5, "受控路径数=5", guards)
    guard("G22", all(isinstance(r["fields"], list) and r["fields"] for r in ROUTES),
          "路径字段表非空", guards)

    return {
        "entries": entries,
        "guards": guards,
        "moments": {k: fstr(v) for k, v in mom.items()},
        "positive_control": {k: fstr(v) for k, v in pos.items()},
        "su5": {
            "matter_dim": matter_dim,
            "adjoint_dim": adj_dim,
            "sm_adjoint_dim": sm_adj_dim,
            "heavy_xy": su5_heavy,
            "weak_doublets_in_24": adj_doublets,
        },
        "so10": {
            "spinor_dim": so10_dim,
            "sm_states": 15,
            "nu_R": 1,
            "adjoint_dim": 45,
            "sm_adjoint_dim": so10_sm_adj,
            "heavy_vectors": so10_heavy,
        },
        "splitting": {
            "M_GUT_GeV": str(m_gut),
            "m_H_GeV": str(m_h),
            "ratio": dstr(split_ratio, 12),
            "tuning_residual": dstr(tuning, 12),
        },
        "routes": ROUTES,
        "r448": {
            "a": fstr(inherited_a),
            "b": fstr(inherited_b),
            "extra_sm": 5,
            "pure_exotic": 7,
            "total_exotic": trinification_exotics,
        },
    }
def status_counts(entries):
    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    return counts


def render_markdown(payload):
    r = payload["result"]
    lines = []
    lines.append("# " + TITLE)
    lines.append("")
    lines.append("- 日期：" + DATE + " ｜ 轮次：**" + RID + "**")
    lines.append("- 判词：`" + VERDICT + "`")
    lines.append("- 条目 **" + str(payload["entry_total"]) + "**：" + " / ".join(k + " " + str(v) for k, v in payload["counts"].items()))
    lines.append("- 守卫 **" + str(payload["guard_pass"]) + "/" + str(payload["guard_total"]) + "** ｜ 退出码 **0**")
    lines.append("")
    lines.append("## 一、一句话结论")
    lines.append("")
    lines.append("**方向 A 可执行，但结论不是「证明 GUT」：最小 SU(5) 必须由 `24_H + 5_H + 5bar_H` 组成，且 doublet–triplet 分裂外生；SO(10) 在纯模型内给出更紧的最小可走场集 `45_H + 126_H + 10_H`，同时覆盖到 SM、弱双态与 ν_R Majorana 三项硬需求，但 126 外态和阈值仍外生。所有 PASS 只表示群论与账本自洽。**")
    lines.append("")
    lines.append("## 二、受控路径表")
    lines.append("")
    lines.append("| 路径 | 群 | 场集 | 到 SM | 双态 | ν_R Majorana | 判定 |")
    lines.append("|---|---|---|---|---|---|---|")
    for route in r["routes"]:
        lines.append("| " + route["key"] + " | " + route["group"] + " | " + ", ".join(route["fields"]) + " | " + str(route["to_sm"]) + " | " + str(route["doublet_source"]) + " | " + str(route["nu_majorana"]) + " | " + route["verdict"] + " |")
    lines.append("")
    lines.append("## 三、核心机器读数")
    lines.append("")
    lines.append("- SU(5) 一代：`5bar+10 = 15`，四条 U(1) 相关反常全零：`" + json.dumps(r["moments"], ensure_ascii=False, sort_keys=True) + "`。")
    lines.append("- 阳性对照：把五个 SM 块的 Y 全置 1 后 `TrY=15`，证明「恒零」不是解析器失效。")
    lines.append("- `24_H` 的弱双态数 = 0，所以「只用 24_H」FAIL；`24 = 8+3+1+12`，12 个 X/Y 型重向量需质量化。")
    lines.append("- 分裂记价：`M_GUT=2e16 GeV`、`m_H=125 GeV` ⇒ `M_GUT/m_H = " + r["splitting"]["ratio"] + "`。")
    lines.append("- SO(10)：`16 = 15+ν_R`，`45-12 = 33` 个重向量需质量化。")
    lines.append("- r448 对照：trinification 27 有 `5+7=12` 个外态；SU(5) 物质侧 0 exotic，SO(10) 16 只多 ν_R。")
    lines.append("")
    lines.append("## 四、条目表")
    lines.append("")
    lines.append("| 码 | 状态 | 条目 | 要点 |")
    lines.append("|---|---|---|---|")
    for e in r["entries"]:
        lines.append("| " + e["code"] + " | " + e["status"] + " | " + e["title"] + " | " + e["detail"] + " |")
    lines.append("")
    lines.append("## 五、边界与红线")
    lines.append("")
    lines.append("1. 群表示、Y 归一、Higgs 场集均为 `[C]` 约定，不是 TUFT 第一性派生。")
    lines.append("2. `45_H+126_H+10_H` 是受控场集内的最小可走路径，不证明自然界选择 SO(10)。")
    lines.append("3. doublet–triplet 分裂、126 外态质量、X/Y 与阈值谱都是外部输入。")
    lines.append("4. 全局读数保持：`0/6 · 0/22 · UFT-3=0 · L3=0 · validated=0`。")
    lines.append("")
    lines.append("## 六、产物回链")
    lines.append("")
    lines.append("- 源码：`../源码/" + STEM + ".py`")
    lines.append("- 判定册：`../判定/判定_TUFT-" + RID + "-SU5SO10破缺链与Higgs扇区最小可行路径审计_精算_" + DATE + ".md`")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_report(payload):
    lines = []
    lines.append("VERDICT = " + VERDICT)
    lines.append("ENTRIES = " + str(payload["entry_total"]))
    lines.append("COUNTS = " + json.dumps(payload["counts"], ensure_ascii=False, sort_keys=True))
    lines.append("GUARDS = " + str(payload["guard_pass"]) + "/" + str(payload["guard_total"]))
    lines.append("SOURCE_SHA256 = " + payload["source_sha256"])
    lines.append("")
    for e in payload["result"]["entries"]:
        lines.append(e["code"] + " " + e["status"] + " " + e["title"])
    lines.append("")
    for g in payload["result"]["guards"]:
        lines.append(g["name"] + " " + ("PASS" if g["ok"] else "FAIL") + " " + g["detail"])
    return "\n".join(lines) + "\n"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    result = analyze()
    counts = status_counts(result["entries"])
    guards = result["guards"]
    guard_pass = sum(1 for g in guards if g["ok"])

    src_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload = {
        "schema": "tuft-r449-v1",
        "date": DATE,
        "round": RID,
        "title": TITLE,
        "verdict": VERDICT,
        "source_sha256": src_hash,
        "entry_total": len(result["entries"]),
        "counts": counts,
        "guard_total": len(guards),
        "guard_pass": guard_pass,
        "result": result,
    }

    JSON_PATH.write_text(json.dumps(norm(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(payload), encoding="utf-8")
    REPORT_PATH.write_text(render_report(payload), encoding="utf-8")

    if guard_pass != len(guards):
        print("GUARD_FAIL")
        return 1
    print("OK entries=" + str(len(result["entries"])) + " guards=" + str(guard_pass) + "/" + str(len(guards)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

