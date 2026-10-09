# -*- coding: utf-8 -*-
"""
靶场登记列（UFT-3）· 写入侧校验与防回潮门禁
============================================

背景（为什么需要它）
--------------------
`源码/claims_schema_升级.py` 给 19 个独立体系的 claims.csv 加了 UFT-3 登记两列
`prediction_value` / `prediction_urel`（**无量纲靶的预测值 + 相对不确定度**，UFT-3 登记的必填项），
但**加列不等于会用**。统计层（`源码/靶场卡方联合拟合_统计层与判决力读数.py`）首次消费这两列时
当场读出两类真实缺陷：

  ① **高危**：`S15-C0020` 的 `prediction_value = 「第四代粒子存在」`、`prediction_urel = 1.0`
     —— 两列齐备、内容却是文字描述。**只看「非空」的判定会把它算成一条已登记靶**
     （统计层首版就踩了这个坑）。
  ② `P03-C0001..0004` 的 `prediction_value` 是「15 / 0 / 0」「几何输入 0/5」等文字、
     `prediction_urel` **全空** —— 登记不完整，无法参与 χ²。

本册把「读取侧兜底」升级为「**写入侧门禁**」，并把登记列语义做成**单一真源**：
统计层不再自己解析这两列，而是导入本模块（避免同一条规则两处实现而口径漂移）。

单一真源（供统计层导入）
------------------------
  `parse_number(txt)`   数值解析：先 `mpf`，再退到有理数 `a/b`（如 `3/8`）
  `classify(pv, pu)`    逐行判定，返回 (flag, severity, reason)
  `scan_registry()`     扫描 20 个体系 claims.csv，返回 (rows, paths)

判定分级
--------
| flag | 含义 | 级别 |
|---|---|---|
| `ok` | 两列齐备且均为数值（urel ≥ 0） | — |
| `empty` | 两列皆空（未登记，合法） | — |
| `non_numeric` | 两列齐备但至少一列不可解析为数值 | **ERROR** |
| `negative_urel` | `prediction_urel` 为负 | **ERROR** |
| `partial` | **只填一列** ⇒ 登记不完整 | **WARN** |
| `urel_zero_noninteger` | `urel = 0` 但值不是整数/精确有理数（精确性声明存疑） | **WARN** |

适用范围（诚实边界）
--------------------
只校验 `01_独立体系/*/claims.csv`（14 列 schema）。`07_统一场方程/…/claims.csv` 是**另一种口径**
的台账（5 列，由守卫 G1 管），**不在适用范围内**，本册只作 INFO 记录，不判违规。

防回潮（基线语义，与守卫 G5 同款且修正其教训）
----------------------------------------------
  `--update-baseline`  把**当前**违规集合登记为基线（历史遗留），**只有显式调用才写**
  `--check`（默认）    与基线比对：**新增 ⇒ 退出码 1**；缩水 ⇒ 报告改进但**不自动改写基线**
  ⚠ 守卫 G5 曾踩过的坑：报篡改时仍把篡改后的内容写回基线 ⇒ 下次自动变 PASS。
    本册因此规定：**`--check` 绝不写任何文件**（产物报告除外），基线只能由显式开关更新。

红线
----
1. **不自动改写任何体系的 claims.csv**：只报告 + 给「建议去向」（文字描述属于 `prediction` 列）。
   数据改正必须由所属体系自行完成——这是本仓库「不替他人改台账」的一贯口径。
2. 本册不新增 claim、不改任何状态、不做物理判定；它是**元数据门禁**。

产出：数据/靶场登记列校验.json + 数据/靶场登记列校验.md + 数据/靶场登记列_违规基线.json

用法：
    python 靶场登记列校验_写入侧门禁.py                      # = --check
    python 靶场登记列校验_写入侧门禁.py --update-baseline
    python 靶场登记列校验_写入侧门禁.py --quiet
    python 靶场登记列校验_写入侧门禁.py --selftest           # 自证：8 分类变异体 + 1 端到端
    python 靶场登记列校验_写入侧门禁.py --sys-dir <副本目录>  # 负向测试模式（不比对基线、不写文件）
"""

import os
import sys
import csv
import json
import time
import shutil
import tempfile
from fractions import Fraction

from mpmath import mpf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SYS_DIR = os.path.join(ROOT, "01_独立体系")
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
BASELINE = os.path.join(OUT_DIR, "靶场登记列_违规基线.json")

UFT3_COLS = ("prediction_value", "prediction_urel")
SEVERITY = {
    "ok": None, "empty": None,
    "non_numeric": "ERROR", "negative_urel": "ERROR",
    "partial": "WARN", "urel_zero_noninteger": "WARN",
}
SUGGESTION = {
    "non_numeric": "两列须为数值；若该内容是对预测的**文字描述**，应放在 `prediction` 列，"
                   "`prediction_value`/`prediction_urel` 留空或填数值",
    "negative_urel": "相对不确定度不得为负；整数靶可填 0，其余填正数",
    "partial": "只填了一列：请补 `prediction_urel`（相对不确定度；整数靶填 0）或一并清空两列",
    "urel_zero_noninteger": "`prediction_urel = 0` 是「精确预言」声明，只对整数/精确有理数合理；"
                            "一般靶请给出真实相对不确定度",
}


# ---------------------------------------------------------------------------
# 一、单一真源：数值解析与逐行判定
# ---------------------------------------------------------------------------

def parse_number(txt):
    """登记列的数值解析（单一真源）。先试 mpf（含 1e-3 这类科学计数），
    再退到有理数（'3/8'）。不可解析返回 None。"""
    if txt is None:
        return None
    s = str(txt).strip()
    if not s:
        return None
    try:
        return mpf(s)
    except Exception:
        pass
    try:
        frac = Fraction(s)
    except Exception:
        return None
    return mpf(frac.numerator) / mpf(frac.denominator)


def classify(pv, pu):
    """逐行判定，返回 (flag, severity, reason)。pv/pu 为已 strip 的字符串。"""
    pv = (pv or "").strip()
    pu = (pu or "").strip()
    both = bool(pv and pu)
    if not pv and not pu:
        return "empty", None, "两列皆空（未登记，合法）"
    if not both:
        return "partial", "WARN", "只填一列（%s）⇒ 登记不完整" % ("prediction_value" if pv else "prediction_urel")
    v, u = parse_number(pv), parse_number(pu)
    if v is None:
        return "non_numeric", "ERROR", "prediction_value 不可解析为数值：「%s」" % pv
    if u is None:
        return "non_numeric", "ERROR", "prediction_urel 不可解析为数值：「%s」" % pu
    if u < 0:
        return "negative_urel", "ERROR", "prediction_urel 为负：%s" % pu
    if u == 0 and v != int(v):
        return "urel_zero_noninteger", "WARN", "urel = 0（精确声明）但值非整数：%s" % pv
    return "ok", None, "两列齐备且均为数值"


# ---------------------------------------------------------------------------
# 二、扫描（供统计层导入使用）
# ---------------------------------------------------------------------------

def scan_registry(sys_dir=None):
    """扫描 01_独立体系/*/claims.csv，返回 (rows, paths)。

    返回行字段：file/owner/schema/claim_id/prediction_value/prediction_urel/
                flag/severity/reason/nonempty/numeric_ok/registered
    其中 `registered` 恒等于 `flag == "ok"`（即「可参与 χ²」的口径）。
    """
    base = sys_dir or SYS_DIR
    rows, paths = [], []
    if not os.path.isdir(base):
        return rows, paths
    for name in sorted(os.listdir(base)):
        path = os.path.join(base, name, "claims.csv")
        if os.path.isfile(path):
            paths.append(path)
            rows.extend(scan_one(path, name))
    return rows, paths


def scan_one(path, owner):
    out = []
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        header = rd.fieldnames or []
        if not all(c in header for c in UFT3_COLS):
            return out
        schema = "UFT-3(14列)"
        for r in rd:
            pv = (r.get("prediction_value") or "").strip()
            pu = (r.get("prediction_urel") or "").strip()
            flag, sev, reason = classify(pv, pu)
            out.append({
                "file": path, "owner": owner, "schema": schema,
                "claim_id": (r.get("claim_id") or "").strip(),
                "prediction_value": pv, "prediction_urel": pu,
                "flag": flag, "severity": sev, "reason": reason,
                "nonempty": flag in ("ok", "non_numeric", "negative_urel",
                                     "partial", "urel_zero_noninteger"),
                "numeric_ok": flag == "ok",
                "registered": flag == "ok",
            })
    return out


def scan_out_of_scope():
    """适用范围外的台账（不同口径），只作 INFO 记录。"""
    other = os.path.join(ROOT, "07_统一场方程", "空间螺旋几何化统一场论", "claims.csv")
    if not os.path.isfile(other):
        return []
    with open(other, "r", encoding="utf-8-sig", newline="") as fh:
        header = csv.DictReader(fh).fieldnames or []
    missing = [c for c in UFT3_COLS if c not in header]
    return [{"file": other, "columns": len(header),
             "missing": missing,
             "note": "该台账为另一种口径（由空间螺旋守卫 G1 管），不在 UFT-3 校验适用范围内"}]


# ---------------------------------------------------------------------------
# 三、基线比对（新增即报警；缩水只报告不自动改写）
# ---------------------------------------------------------------------------

def key_of(row):
    return "%s|%s|%s" % (os.path.relpath(row["file"], ROOT).replace("\\", "/"),
                         row["claim_id"], row["flag"])


def load_baseline():
    if not os.path.isfile(BASELINE):
        return None
    with open(BASELINE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def violations(rows):
    return [r for r in rows if r["severity"] in ("ERROR", "WARN")]


def diff(vio, base):
    """返回 (added, removed)。base=None 表示无基线（全部视为待登记）。"""
    cur = {key_of(r): r for r in vio}
    if base is None:
        return sorted(cur.keys()), []
    old = set(base.get("violations", {}).keys())
    return sorted(set(cur) - old), sorted(old - set(cur))


# ---------------------------------------------------------------------------
# 四、渲染与主流程
# ---------------------------------------------------------------------------

def render_md(P):
    A = []
    a = A.append
    a("# 靶场登记列（UFT-3）校验（可复跑产物）\n")
    a("> 本文件由 `源码/靶场登记列校验_写入侧门禁.py` 生成，**请勿手工编辑**。\n")
    a("> Python %s · 生成于 %s\n" % (P["python"], P["generated_utc"]))
    a("\n## 一、适用范围内统计\n")
    a("| 文件 | 归属 | 行数 | 数值合法 | 未登记 | ERROR | WARN |")
    a("| --- | --- | --- | --- | --- | --- | --- |")
    for d in P["by_file"]:
        a("| `%s` | %s | %d | **%d** | %d | %d | %d |"
          % (d["rel"], d["owner"], d["rows"], d["ok"], d["empty"], d["error"], d["warn"]))
    a("\n> 合计：扫描 **%d** 个 claims.csv；数值合法登记 **%d** 条；"
      "ERROR **%d** 条；WARN **%d** 条。\n"
      % (P["file_count"], P["ok_count"], P["error_count"], P["warn_count"]))
    if P["violations"]:
        a("\n## 二、违规明细\n")
        a("| 体系 / 层 | 主张 | prediction_value | prediction_urel | 级别 | 判定 | 建议 |")
        a("| --- | --- | --- | --- | --- | --- | --- |")
        for r in P["violations"]:
            a("| %s | `%s` | `%s` | `%s` | **%s** | %s | %s |"
              % (r["owner"], r["claim_id"], r["prediction_value"],
                 r["prediction_urel"] or "（空）", r["severity"], r["reason"],
                 SUGGESTION.get(r["flag"], "—")))
    else:
        a("\n## 二、违规明细\n\n（无）\n")
    a("\n## 三、基线与防回潮\n")
    a("| 项 | 值 |")
    a("| --- | --- |")
    a("| 基线文件 | `%s` |" % (P["baseline_rel"] or "（尚无基线）"))
    a("| 基线登记违规数 | %s |" % (P["baseline_count"] if P["baseline_count"] is not None else "—"))
    a("| 相对基线**新增** | **%d** |" % len(P["added"]))
    a("| 相对基线**已消除** | %d |" % len(P["removed"]))
    if P["added"]:
        a("\n**新增违规（门禁报警，退出码 1）**：\n")
        for k in P["added"]:
            a("- `%s`" % k)
    if P["removed"]:
        a("\n**已消除（改进；基线不自动改写，需显式 `--update-baseline`）**：\n")
        for k in P["removed"]:
            a("- `%s`" % k)
    a("\n## 四、适用范围外（INFO）\n")
    if P["out_of_scope"]:
        for o in P["out_of_scope"]:
            a("- `%s`：%d 列，缺 %s —— %s"
              % (os.path.relpath(o["file"], ROOT).replace("\\", "/"),
                 o["columns"], "、".join(o["missing"]), o["note"]))
    else:
        a("- （无）")
    a("\n## 五、口径与红线\n")
    for line in P["notes"]:
        a("- " + line)
    a("\n```powershell")
    a("cd openuft/04_公共成果/本项目_全维自洽与归一化/源码")
    a("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B 靶场登记列校验_写入侧门禁.py --check")
    a("& C:/Users/mo/AppData/Local/Programs/Python/Python38/python.exe -B 靶场登记列校验_写入侧门禁.py --update-baseline")
    a("```\n")
    return "\n".join(A) + "\n"


# ---------------------------------------------------------------------------
# 五、自证（牙齿：分类变异体 + 端到端临时台账）
# ---------------------------------------------------------------------------
# (名称, prediction_value, prediction_urel, 期望 flag)
SELFTEST_ROWS = [
    ("ok-numeric",            "1.5",              "0.1",    "ok"),
    ("ok-fraction",           "3/8",              "0.05",   "ok"),
    ("ok-integer-urel0",      "3",                "0",      "ok"),
    ("err-value-text",        "第四代粒子存在",     "1.0",    "non_numeric"),
    ("err-urel-text",         "1.5",              "约一成",  "non_numeric"),
    ("err-urel-negative",     "1.5",              "-0.1",   "negative_urel"),
    ("warn-partial",          "15 / 0 / 0",       "",       "partial"),
    ("warn-urel0-noninteger", "1.5",              "0",      "urel_zero_noninteger"),
]


def run_selftest():
    """返回逐项结果。分类变异体证明判定正确；端到端证明扫描链路正确。"""
    T = []
    for name, pv, pu, want in SELFTEST_ROWS:
        got, sev, why = classify(pv, pu)
        T.append({"name": name, "ok": got == want,
                  "detail": "value=「%s」urel=「%s」⇒ %s（期望 %s）｜%s"
                            % (pv, pu, got, want, why)})
    # 端到端：临时台账（**不碰仓库真实数据**）2 行 ⇒ 必须 1 ok + 1 ERROR
    tmp = tempfile.mkdtemp(prefix="uft3_selftest_")
    try:
        d = os.path.join(tmp, "X_自检体系")
        os.makedirs(d)
        with open(os.path.join(d, "claims.csv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["claim_id", "prediction_value", "prediction_urel"])
            w.writerow(["X-C0001", "1.5", "0.1"])
            w.writerow(["X-C0002", "文字预测", "0.1"])
        rows, _ = scan_registry(tmp)
        n_err = sum(1 for r in rows if r["severity"] == "ERROR")
        n_ok = sum(1 for r in rows if r["flag"] == "ok")
        T.append({"name": "端到端：临时台账 2 行",
                  "ok": (len(rows) == 2 and n_ok == 1 and n_err == 1),
                  "detail": "扫到 %d 行；ok=%d、ERROR=%d（期望 2 / 1 / 1）"
                            % (len(rows), n_ok, n_err)})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return T


def main():
    t0 = time.time()
    update = "--update-baseline" in sys.argv
    quiet = "--quiet" in sys.argv
    selftest = "--selftest" in sys.argv
    sys_dir = SYS_DIR
    test_mode = False
    if "--sys-dir" in sys.argv:
        try:
            sys_dir = os.path.abspath(sys.argv[sys.argv.index("--sys-dir") + 1])
            test_mode = True
        except IndexError:
            print("--sys-dir 需要路径参数")
            return 2

    if selftest:
        T = run_selftest()
        print("=" * 78)
        print("靶场登记列校验 · 自检（%d 项）" % len(T))
        print("=" * 78)
        for t in T:
            print("  %-9s %-26s %s" % ("CAUGHT/CLEAN" if t["ok"] else "MISSED",
                                       t["name"], t["detail"]))
        bad = [t for t in T if not t["ok"]]
        print("-" * 78)
        print("  自检 %d/%d %s" % (len(T) - len(bad), len(T),
                                   "全部通过" if not bad else "存在 MISSED"))
        return 0 if not bad else 1

    rows, paths = scan_registry(sys_dir)
    vio = violations(rows)

    by_file = []
    for path in paths:
        fr = [r for r in rows if r["file"] == path]
        by_file.append({
            "rel": os.path.relpath(path, ROOT).replace("\\", "/"),
            "owner": (fr[0]["owner"] if fr else "—"),
            "rows": len(fr),
            "ok": sum(1 for r in fr if r["flag"] == "ok"),
            "empty": sum(1 for r in fr if r["flag"] == "empty"),
            "error": sum(1 for r in fr if r["severity"] == "ERROR"),
            "warn": sum(1 for r in fr if r["severity"] == "WARN"),
        })

    base = load_baseline()
    added, removed = diff(vio, base)

    if test_mode:
        # 负向测试模式（--sys-dir）：在**副本目录**上跑，不做基线比对、不写基线、
        # **不覆写真实产物**。退出码语义：存在 ERROR ⇒ 1（证明门禁会咬），否则 0。
        errs = [r for r in vio if r["severity"] == "ERROR"]
        if not quiet:
            print("=" * 78)
            print("靶场登记列校验 · 测试模式（--sys-dir；不做基线比对、不写任何文件）")
            print("=" * 78)
            print("  扫描 %d 个 claims.csv / %d 行；ERROR %d 条；WARN %d 条"
                  % (len(paths), len(rows), len(errs),
                     sum(1 for r in vio if r["severity"] == "WARN")))
            for r in vio:
                print("    [%-5s] %-24s %-10s value=「%s」urel=「%s」"
                      % (r["severity"], r["owner"], r["claim_id"],
                         r["prediction_value"][:24], r["prediction_urel"][:12]))
            print("  结论：%s" % ("存在 ERROR ⇒ 门禁会咬（期望行为）" if errs else "无 ERROR"))
        return 1 if errs else 0

    if update:
        os.makedirs(OUT_DIR, exist_ok=True)
        payload = {
            "updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "note": "历史遗留违规基线：只许不增。由 --update-baseline 显式登记；"
                    "--check 绝不改写本文件。",
            "violations": {key_of(r): {"owner": r["owner"], "claim_id": r["claim_id"],
                                       "flag": r["flag"], "severity": r["severity"]}
                           for r in vio},
        }
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        base = payload
        added, removed = diff(vio, base)

    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "file_count": len(paths),
        "row_count": len(rows),
        "ok_count": sum(1 for r in rows if r["flag"] == "ok"),
        "error_count": sum(1 for r in vio if r["severity"] == "ERROR"),
        "warn_count": sum(1 for r in vio if r["severity"] == "WARN"),
        "empty_count": sum(1 for r in rows if r["flag"] == "empty"),
        "by_file": by_file,
        "violations": vio,
        "out_of_scope": scan_out_of_scope(),
        "baseline_rel": ("04_公共成果/本项目_全维自洽与归一化/数据/靶场登记列_违规基线.json"
                         if os.path.isfile(BASELINE) else None),
        "baseline_count": (len(base.get("violations", {})) if base else None),
        "added": added, "removed": removed,
        "notes": [
            "本册是**元数据门禁**：不新增 claim、不改任何状态、不做物理判定。",
            "**不自动改写任何体系的 claims.csv**：只报告 + 给建议去向"
            "（文字描述属于 `prediction` 列）。改正须由所属体系自行完成。",
            "`registered` 恒等于 `flag == ok`（可参与 χ² 的口径）；统计层直接导入本模块，"
            "登记列语义**单一真源**。",
            "`--check` 绝不写任何文件（产物报告除外）；基线只能由 `--update-baseline` 显式更新"
            "（守卫 G5 曾因自动写回基线而把篡改『自愈』）。",
            "适用范围只含 `01_独立体系/*/claims.csv`（14 列 UFT-3 schema）；"
            "`07_统一场方程` 的 5 列台账是另一种口径，不在范围内。",
            "数值解析先试 `mpf`（含科学计数），再退有理数 `a/b`（如 `3/8`）。",
        ],
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "靶场登记列校验.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "靶场登记列校验.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(payload))

    if not quiet:
        print("=" * 78)
        print("靶场登记列（UFT-3）写入侧校验（Python %s）" % sys.version.split()[0])
        print("=" * 78)
        print("  扫描 %d 个 claims.csv / %d 行；数值合法登记 %d 条；ERROR %d 条；WARN %d 条"
              % (len(paths), len(rows), payload["ok_count"],
                 payload["error_count"], payload["warn_count"]))
        for r in vio:
            print("    [%-5s] %-34s %-10s value=「%s」urel=「%s」"
                  % (r["severity"], r["owner"], r["claim_id"],
                     r["prediction_value"][:24], r["prediction_urel"][:12]))
        print("-" * 78)
        print("  基线：%s" % (payload["baseline_rel"] or "（尚无基线，先跑 --update-baseline）"))
        print("  相对基线：新增 %d 条；已消除 %d 条" % (len(added), len(removed)))
        for k in added:
            print("    [新增·报警] " + k)
        for k in removed:
            print("    [已消除]   " + k)
        print("  产出：数据/靶场登记列校验.{json,md}  用时 %.2fs" % (time.time() - t0))

    if update:
        return 0
    if base is None:
        if not quiet:
            print("  结论：无基线可比 ⇒ 请先显式登记基线（--update-baseline）")
        return 1
    if added:
        if not quiet:
            print("  结论：存在**新增**违规 %d 条 ⇒ 门禁报警" % len(added))
        return 1
    if not quiet:
        print("  结论：无新增违规（历史遗留 %d 条在基线内）" % len(base.get("violations", {})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
