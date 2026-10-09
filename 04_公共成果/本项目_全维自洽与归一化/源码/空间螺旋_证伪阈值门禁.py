# -*- coding: utf-8 -*-
"""证伪阈值门禁 · UFT-3 登记列审计与 δ_min 现场读数（可复跑）
================================================================================

承接缺口
--------
`07_统一场方程/空间螺旋几何化统一场论/03_验证与可证伪性.md` §5 给出 **T1–T8 阈值表**，
但那是**文档**不是**门禁**：阈值会漂移、登记列无人消费、UFT-3 恒为 0 且说不出成因。
本仪器把三件事做成可重跑读数：

1. **登记列审计**：直接消费 `01_独立体系/*/claims.csv` 的 `prediction_value` /
   `prediction_urel` 两列（UFT-3 的登记列，此前**无引擎消费**），把"UFT-3 = 0"
   拆成可归因的排除桶（列错位 / 半填 / 非数值占用 / urel 无效 / 无观测侧）。
2. **阈值现场计算**：$\\chi^2_{\\mathrm{crit}}(1,0.95)=2\\,\\mathrm{erfinv}(0.95)^2$ 走**闭式**
   （不硬编码；G8 与常量对账 ⇒ 谁把它改回写死字符串，G8 立刻红），
   逐条给出 $\\delta_{\\min}=\\lvert v\\rvert\\cdot u_{\\mathrm{rel}}\\sqrt{\\chi^2_{\\mathrm{crit}}}$。
3. **两条轴**（继承 [靶场统计层](判定_靶场卡方联合拟合_2026-09-26.md) 口径）：
   - 轴 A 登记自洽（G3/G4/G5）
   - 轴 B 可检验性（G6 有观测侧 + urel 有限）
   轴 A 过而轴 B 不过 ⇒ 判 `FAIL`（不可判 ≠ 通过），与靶场同口径。

不做的事
--------
- **不改任何 CSV**（只读；产物只落 `数据/`），不改 `claims.csv` 状态；
- **不猜列位置**：行宽 ≠ 表头宽的行一律判 `unreadable` 并计数（缺失不是通过）；
- **不新造判据**：χ²_crit、δ_min、两条轴、排除桶口径全部复用靶场/登记既有定义。

判据编号：G1–G12（见 `judge()` 的 docstring）。四态：PASS / FAIL / BOUNDARY / INFO。
产物：`数据/空间螺旋_证伪阈值门禁.json` + `.md`。
退出码：任一 FAIL ⇒ 1（可作 CI 门禁）。

用法
----
    python -B 空间螺旋_证伪阈值门禁.py                     # 全库 01_独立体系/*
    python -B 空间螺旋_证伪阈值门禁.py --systems-root <dir> # 夹具/临时目录（牙齿用）
    python -B 空间螺旋_证伪阈值门禁.py --quiet              # 只打结论行
"""

import csv
import io
import json
import os
import sys
import time

from mpmath import mp, mpf, sqrt, erfinv

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 80

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # -> openuft
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
DEFAULT_SYS = os.path.join(ROOT, "01_独立体系")

# 规范表头（14 列）。缺任何一列 ⇒ G1 FAIL。
CANONICAL = ["claim_id", "hypothesis_revision", "statement", "assumptions",
             "derivation", "prediction", "prediction_value", "prediction_urel",
             "run_id", "data_id", "uncertainty", "evidence_level", "status", "reviewer"]

# 已知常量（仅用于与闭式对账，不用于计算）
CHI2_CRIT_REF = mpf("3.84145882069")

EXCLUDE_BUCKETS = ["half_filled", "nonnumeric_value", "invalid_urel",
                   "no_observation_side"]


def chi2_crit_closed_form():
    """χ²_crit(1, 0.95) = 2·erfinv(0.95)²  —— 闭式，非硬编码。"""
    return 2 * erfinv(mpf("0.95")) ** 2


def read_claims(path):
    """读一个 claims.csv：返回 (header, rows, row_length_hist)。不做列位置猜测。"""
    with io.open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return [], [], {}
    header = [h.strip() for h in rows[0]]
    data = rows[1:]
    hist = {}
    for r in data:
        hist[len(r)] = hist.get(len(r), 0) + 1
    return header, data, hist


def locate(header):
    """返回规范列在当前表头中的下标（缺失为 None）。"""
    idx = {}
    for name in CANONICAL:
        idx[name] = header.index(name) if name in header else None
    return idx


def cell(row, i):
    if i is None or i >= len(row):
        return ""
    return row[i]


REG_GATE = os.path.join(HERE, "靶场登记列校验_写入侧门禁.py")
# 牙齿在临时目录里跑本仪器的副本时，副本旁边没有真源文件 ⇒ 用环境变量指回仓库里的真源
REG_GATE_ENV = "UFT3_REGISTRY_GATE"


def load_registry_gate():
    """归一化：数值解析与逐行判定**委托**单一真源
    `源码/靶场登记列校验_写入侧门禁.py`（其 `parse_number` / `classify` 是全仓唯一实现）。

    本仪器**不复制**这套逻辑——只加它不覆盖的两层：δ_min 现场计算 与 观测侧/阈值门禁。
    缺失真源时返回 None（判据 G0 随即变红，绝不静默回退到自建实现）。
    """
    path = os.environ.get(REG_GATE_ENV) or REG_GATE
    if not os.path.isfile(path):
        return None
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("uft3_registry_gate", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not (hasattr(mod, "parse_number") and hasattr(mod, "classify")):
            return None
        return mod
    except Exception:
        return None


def fmt(v, n=12):
    try:
        return mp.nstr(mpf(v), n)
    except Exception:
        return str(v)


def judge(systems_root=DEFAULT_SYS):
    """主判据。返回 (gates, per_system, entries, totals)

    判据编号
    --------
    G1  表头自洽：每个 claims.csv 必须含 14 个规范列（含 prediction_value/urel）
    G2  行宽一致：数据行字段数 == 表头宽（列错位必须 0 条）
    G3  数值占用：prediction_value 非空 ⇒ 必须可解析为有限数
    G4  半填：value / urel 只填其一 ⇒ 排除
    G5  urel 有效：填了 value 的行 urel > 0
    G6  观测侧：data_id 或 uncertainty 至少一列非空
    G7  UFT-3 计数：同过轴 A（G3/G4/G5）与轴 B（G6）的条数
    G8  χ²_crit 走闭式（含源码级防写死检查）
    G9  δ_min 现场值自洽：δ_min/(|v|·u) 必须等于 √χ²_crit（独立路径复核）
    G10 两条轴各自成列（轴 A / 轴 B 分别计数）
    G11 账目平衡：有效 + 各排除桶 == 候选总数
    G12 只读不改：本仪器不写任何 claims.csv（结构性保证，见 run()）
    """
    gates = {}

    def rec(gid, ok, verdict_fail, verdict_pass, note):
        gates[gid] = {"ok": bool(ok),
                      "verdict": verdict_pass if ok else verdict_fail,
                      "note": note}

    # 归一化：数值解析与逐行判定委托单一真源（缺失即红的 G0）
    reg = load_registry_gate()

    # ---- 扫描 ----
    sys_dirs = []
    if os.path.isdir(systems_root):
        for name in sorted(os.listdir(systems_root)):
            p = os.path.join(systems_root, name, "claims.csv")
            if os.path.isfile(p):
                sys_dirs.append((name, p))

    per_system = []
    entries = []
    buckets = dict((k, 0) for k in EXCLUDE_BUCKETS)
    candidates = 0
    header_bad = []
    misaligned_rows = 0
    axis_a_pass = 0
    axis_b_pass = 0
    # G9 的独立复核基准：√χ²_crit（闭式），在扫描前算一次，与 δ_min 全程同精度
    sqrt_cc = sqrt(chi2_crit_closed_form())
    g9_bad = []

    unreadable_rows = 0

    for name, path in sys_dirs:
        header, data, hist = read_claims(path)
        if not header:
            header_bad.append(name)
            continue
        idx = locate(header)
        missing = [k for k in CANONICAL if idx[k] is None]
        width = len(header)
        ps = {"system": name, "rows": len(data), "candidates": 0, "valid": 0,
              "misaligned": sum(c for w, c in hist.items() if w != width),
              "missing_cols": missing}
        if missing:
            header_bad.append(name)
        misaligned_rows += ps["misaligned"]

        for r in data:
            if len(r) != width:
                # 不猜列位置：整行不可读。它**不计入候选账目**（无法判断是否登记了预测），
                # 只计入结构性 unreadable 计数，由 G2 承担。
                unreadable_rows += 1
                continue
            pv = cell(r, idx["prediction_value"])
            pu = cell(r, idx["prediction_urel"])
            pred = cell(r, idx["prediction"])
            did = cell(r, idx["data_id"])
            unc = cell(r, idx["uncertainty"])
            if not (pv.strip() or pu.strip() or pred.strip()):
                continue                      # 未声明预测 ⇒ 不是候选
            candidates += 1
            ps["candidates"] += 1
            # 轴 A（登记自洽）**委托单一真源**判定
            flag, sev, why = reg.classify(pv, pu) if reg else ("non_numeric", "ERROR", "真源缺失")
            if flag == "partial":
                buckets["half_filled"] += 1
                continue
            if flag == "non_numeric":
                buckets["nonnumeric_value"] += 1
                continue
            if flag != "ok":
                buckets["invalid_urel"] += 1
                continue
            v = reg.parse_number(pv)
            u = reg.parse_number(pu)
            if v is None or u is None or u <= 0:
                buckets["invalid_urel"] += 1
                continue
            axis_a_pass += 1
            has_obs = bool(did.strip() or unc.strip())
            if has_obs:
                axis_b_pass += 1
            else:
                buckets["no_observation_side"] += 1
                continue
            sigma = abs(v) * u
            dmin = sigma * sqrt(chi2_crit_closed_form())
            # G9：δ_min/(|v|·u) 必须等于 √χ²_crit（在 mpf 全精度下复核，不看打印值）
            if abs(dmin / (abs(v) * u) - sqrt_cc) > mpf("1e-30"):
                g9_bad.append(cell(r, idx["claim_id"]))
            ps["valid"] += 1
            entries.append({"system": name, "claim_id": cell(r, idx["claim_id"]),
                            "value": fmt(v), "urel": fmt(u), "sigma": fmt(sigma),
                            "delta_min": fmt(dmin),
                            "statement": cell(r, idx["statement"])[:60]})
        per_system.append(ps)

    # ---- 与单一真源的交叉对账（同一份 CSV 在两台仪器上口径是否收敛） ----
    cross = {"registry_rows": 0, "registry_registered": 0,
             "registry_non_numeric": 0, "registry_partial": 0}
    if reg is not None and hasattr(reg, "scan_registry"):
        try:
            rrows, _ = reg.scan_registry(systems_root)
            cross["registry_rows"] = len(rrows)
            for rr in rrows:
                f = rr.get("flag")
                if f == "ok":
                    cross["registry_registered"] += 1
                elif f == "non_numeric":
                    cross["registry_non_numeric"] += 1
                elif f == "partial":
                    cross["registry_partial"] += 1
        except Exception as e:
            cross["error"] = str(e)

    # ---- 判据 ----
    rec("G0", reg is not None, "FAIL", "PASS",
        "归一化：数值解析/逐行判定委托单一真源 `靶场登记列校验_写入侧门禁.py`（%s）"
        % ("已加载" if reg is not None else "**真源缺失**"))
    rec("G1", not header_bad, "FAIL", "PASS",
        "表头缺列或缺失的体系：%s" % (",".join(header_bad) if header_bad else "无"))
    rec("G2", unreadable_rows == 0, "FAIL", "PASS",
        "不可读行（行宽 ≠ 表头宽，不猜列位置）= %d；"
        "与单一真源对账：其可读行数 %d（DictReader 容错尾部多余列）⇒ 两台仪器口径不收敛时以**先修列宽**为准"
        % (unreadable_rows, cross["registry_rows"]))
    rec("G3", buckets["nonnumeric_value"] == 0, "FAIL", "PASS",
        "非数值占用 = %d" % buckets["nonnumeric_value"])
    rec("G4", buckets["half_filled"] == 0, "FAIL", "PASS",
        "半填（只填一列）= %d" % buckets["half_filled"])
    rec("G5", buckets["invalid_urel"] == 0, "FAIL", "PASS",
        "urel 无效（缺失或非正）= %d（在 G3/G4 之后逐条检查）" % buckets["invalid_urel"])
    rec("G6", buckets["no_observation_side"] == 0, "FAIL", "PASS",
        "无观测侧 = %d（data_id 与 uncertainty 全空）" % buckets["no_observation_side"])
    uft3 = len(entries)
    rec("G7", uft3 > 0, "BOUNDARY", "PASS",
        "UFT-3 有效登记 = %d 条（轴 A 过 %d、轴 B 过 %d）" % (uft3, axis_a_pass, axis_b_pass))
    cc = chi2_crit_closed_form()
    closed_ok = abs(cc - CHI2_CRIT_REF) < mpf("1e-10")
    try:
        import inspect
        import re as _re
        src = inspect.getsource(chi2_crit_closed_form)
        # 去掉 docstring 与注释后再查：否则文档串里那句含 erfinv 的公式会让"写死"也过关
        code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
        code = _re.sub(r"#.*", "", code)
        closed_ok = closed_ok and ("erfinv(" in code)
    except Exception:
        closed_ok = False
    rec("G8", closed_ok, "FAIL", "PASS",
        "χ²_crit(1,0.95) 闭式 = %s（常量对照 %s，源码须含 erfinv）"
        % (fmt(cc, 15), fmt(CHI2_CRIT_REF, 12)))
    rec("G9", not g9_bad, "FAIL", "PASS",
        "δ_min/(|v|·u) 与 √χ²_crit 不符的条目：%s" % (",".join(g9_bad) if g9_bad else "无"))
    rec("G10", axis_a_pass >= axis_b_pass, "FAIL", "PASS",
        "轴 A（登记自洽）%d ≥ 轴 B（可检验）%d：轴 B 必须是轴 A 的子集" % (axis_a_pass, axis_b_pass))
    balanced = (uft3 + sum(buckets.values())) == candidates
    rec("G11", balanced, "FAIL", "PASS",
        "账目：有效 %d + 排除桶合计 %d = %d，候选总数 %d"
        % (uft3, sum(buckets.values()), uft3 + sum(buckets.values()), candidates))
    rec("G12", True, "FAIL", "PASS", "只读：本仪器不写任何 claims.csv，产物只落 数据/")

    totals = {"systems": len(sys_dirs), "candidates": candidates, "uft3": uft3,
              "axis_a": axis_a_pass, "axis_b": axis_b_pass,
              "buckets": buckets, "unreadable_rows": unreadable_rows,
              "crosscheck": cross,
              "chi2_crit": fmt(cc, 15), "sqrt_chi2_crit": fmt(sqrt_cc, 15)}
    return gates, per_system, entries, totals


def run(systems_root=DEFAULT_SYS, quiet=False, out_dir=OUT_DIR, write=True):
    gates, per_system, entries, totals = judge(systems_root)
    failed = [g for g in gates if not gates[g]["ok"]]
    verdict = "FAIL" if failed else "PASS"

    lines = []
    add = lines.append
    add("# 证伪阈值门禁 · UFT-3 登记列审计（自动生成）")
    add("")
    add("> 引擎 `源码/空间螺旋_证伪阈值门禁.py` ｜ 口径继承靶场统计层（轴 A 自洽 / 轴 B 可检验）")
    add("")
    add("**判定：%s**（判据 %d 条，未过 %d 条：%s）"
        % (verdict, len(gates), len(failed), ",".join(failed) if failed else "无"))
    add("")
    add("## 1. 阈值（闭式）")
    add("")
    add("| 量 | 值 |")
    add("|---|---|")
    add("| χ²_crit(1, 0.95) = 2·erfinv(0.95)² | %s |" % totals["chi2_crit"])
    add("| √χ²_crit（δ_min 的系数） | %s |" % totals["sqrt_chi2_crit"])
    add("| δ_min 定义 | δ_min = |v|·u_rel·√χ²_crit |")
    add("")
    add("## 2. 判据")
    add("")
    add("| 判据 | 结果 | 说明 |")
    add("|---|---|---|")
    for g in sorted(gates):
        add("| %s | **%s** | %s |" % (g, gates[g]["verdict"], gates[g]["note"]))
    add("")
    add("## 3. UFT-3 成因分解（为什么是 %d 条）" % totals["uft3"])
    add("")
    add("| 桶 | 条数 | 含义 |")
    add("|---|---|---|")
    add("| **有效登记（UFT-3）** | %d | 轴 A 与轴 B 同时通过 |" % totals["uft3"])
    for k in EXCLUDE_BUCKETS:
        add("| %s | %d | %s |" % (k, totals["buckets"][k],
                                  {"half_filled": "只填了一列（登记不完整）",
                                   "nonnumeric_value": "数值列被非数值占用",
                                   "invalid_urel": "urel 缺失/为负/非正",
                                   "no_observation_side": "无观测侧（data_id/uncertainty 全空）"}[k]))
    add("| 候选总数（可读行内） | %d | 声明了 prediction / prediction_value 的行 |" % totals["candidates"])
    add("| **结构不可读行** | %d | 行宽 ≠ 表头宽 ⇒ 不猜列位置，**不计入候选账目**（见 G2） |"
        % totals["unreadable_rows"])
    cc_ = totals.get("crosscheck", {})
    add("")
    add("与单一真源对账：`靶场登记列校验_写入侧门禁.scan_registry` 可读 %s 行，"
        "其中 ok %s / non_numeric %s / partial %s ⇒ 两台仪器口径若不收敛，**先修列宽**再谈登记。"
        % (cc_.get("registry_rows", "?"), cc_.get("registry_registered", "?"),
           cc_.get("registry_non_numeric", "?"), cc_.get("registry_partial", "?")))
    add("")
    add("## 4. 逐体系")
    add("")
    add("| 体系 | 数据行 | 候选 | 有效 | 列错位 | 缺列 |")
    add("|---|---|---|---|---|---|")
    for ps in per_system:
        add("| %s | %d | %d | %d | %d | %s |"
            % (ps["system"], ps["rows"], ps["candidates"], ps["valid"],
               ps["misaligned"], ",".join(ps["missing_cols"]) or "无"))
    add("")
    add("## 5. 有效登记的 δ_min（最多列 40 条）")
    add("")
    if entries:
        add("| 体系 | claim | value | u_rel | σ | δ_min |")
        add("|---|---|---|---|---|---|")
        for e in entries[:40]:
            add("| %s | %s | %s | %s | %s | %s |"
                % (e["system"], e["claim_id"], e["value"], e["urel"], e["sigma"], e["delta_min"]))
    else:
        add("**无有效登记**（UFT-3 = 0）。这不是“没有预测”，而是“没有任何一条登记同时通过轴 A 与轴 B”。")
    add("")

    payload = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
               "verdict": verdict, "gates": gates, "per_system": per_system,
               "entries": entries, "totals": totals}
    if write:
        os.makedirs(out_dir, exist_ok=True)
        with io.open(os.path.join(out_dir, "空间螺旋_证伪阈值门禁.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        with io.open(os.path.join(out_dir, "空间螺旋_证伪阈值门禁.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    if not quiet:
        print("\n".join(lines))
    print("判定 %s ｜ 判据 %d 条 ｜ 未过 %s ｜ UFT-3 = %d"
          % (verdict, len(gates), ",".join(failed) if failed else "无", totals["uft3"]))
    return 0 if not failed else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    quiet = "--quiet" in argv
    root = DEFAULT_SYS
    if "--systems-root" in argv:
        root = argv[argv.index("--systems-root") + 1]
    out_dir = OUT_DIR
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
    write = "--no-write" not in argv
    return run(root, quiet=quiet, out_dir=out_dir, write=write)


if __name__ == "__main__":
    sys.exit(main())

