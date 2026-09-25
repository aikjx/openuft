# -*- coding: utf-8 -*-
"""
空间螺旋几何化统一场论 · CSV 元数据卫生校验（openuft 诚实审计口径）

校验对象
--------
- `claims.csv`           主张登记表
- `现象覆盖矩阵.csv`      现象 → 主控子系统 → 证据状态

校验项
------
1. 编码 / 必需列 / 行数
2. claim_id 唯一性与编号格式
3. **单元格禁英文逗号与双引号**（openuft 已知坑：CSV 字段混用英文逗号会静默错位）
4. status / 判定 / 证据状态 值域
5. 现象主键唯一性
6. claims.csv ↔ 现象覆盖矩阵.csv ↔ 01 评级文档 的交叉引用覆盖
7. status 分布统计（供「理论横向对比矩阵」计数使用）

红线：只报告，**不自动改写**任何 CSV。
"""

import csv
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CLAIMS = os.path.join(ROOT, "claims.csv")
MATRIX = os.path.join(ROOT, "现象覆盖矩阵.csv")
DOC_AUDIT = os.path.join(ROOT, "01_全维评级与诚实边界.md")
DOC_MAIN = os.path.join(ROOT, "00_核心理论体系总纲.md")

RESULTS = []


def rec(cid, title, verdict, detail):
    RESULTS.append({"id": cid, "title": title, "verdict": verdict, "detail": detail})


def P(cid, t, d):
    rec(cid, t, "PASS", d)


def F(cid, t, d):
    rec(cid, t, "FAIL", d)


def BO(cid, t, d):
    rec(cid, t, "BOUNDARY", d)


def IN(cid, t, d):
    rec(cid, t, "INFO", d)


def read_csv(path):
    """返回 (header, dict_rows, raw_rows)。

    raw_rows 是 csv.reader 的原生二维表，用于**逐行列数校验**——
    这是唯一能抓出「字段内未转义英文逗号导致整行错位」的手段
    （DictReader 会把多余字段塞进 None 键而静默掩盖该问题）。
    """
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        raw = [row for row in csv.reader(f) if row]
    if not raw:
        return [], [], []
    header = raw[0]
    data = raw[1:]
    rows = []
    for r in data:
        if len(r) == len(header):
            rows.append(dict(zip(header, r)))
        else:
            # 错位行：按位置截断/补齐，保证后续值域检查不会 KeyError
            padded = (r + [""] * len(header))[:len(header)]
            rows.append(dict(zip(header, padded)))
    return header, rows, data


def scan_bad_cells(rows, header):
    bad = []
    for i, row in enumerate(rows, start=2):
        for k in header:
            v = row.get(k) or ""
            if "," in v:
                bad.append((i, k, "英文逗号", v))
            if '"' in v:
                bad.append((i, k, "双引号", v))
    return bad


def scan_row_width(header, data, name):
    """逐行列数校验：返回错位行清单。"""
    bad = []
    for i, r in enumerate(data, start=2):
        if len(r) != len(header):
            bad.append((i, len(r), " | ".join(r)))
    return bad


def run():
    RESULTS[:] = []

    # ---------------- C1 文件可读性
    for path, name in ((CLAIMS, "claims.csv"), (MATRIX, "现象覆盖矩阵.csv")):
        if not os.path.exists(path):
            F("V1-" + name, "文件存在性", "缺失：" + path)
            return RESULTS
    P("V1-01", "两份 CSV 均存在且 UTF-8 可解码",
      "claims.csv / 现象覆盖矩阵.csv 均以 utf-8-sig 成功解析（自动剥离 BOM）")

    h_claims, rows_claims, raw_claims = read_csv(CLAIMS)
    h_matrix, rows_matrix, raw_matrix = read_csv(MATRIX)

    # ---------------- C0 列数错位（最高优先级：错位会让后续所有值域检查失真）
    w1 = scan_row_width(h_claims, raw_claims, "claims.csv")
    w2 = scan_row_width(h_matrix, raw_matrix, "现象覆盖矩阵.csv")
    if w1 or w2:
        det = []
        for i, n, txt in w1:
            det.append("claims.csv 行" + str(i) + " 实际 " + str(n) + " 列（应为 " +
                       str(len(h_claims)) + "）：" + txt[:70])
        for i, n, txt in w2:
            det.append("矩阵 行" + str(i) + " 实际 " + str(n) + " 列（应为 " +
                       str(len(h_matrix)) + "）：" + txt[:70])
        F("V0-01", "行字段数一致性（防英文逗号错位）",
          "命中 " + str(len(w1) + len(w2)) + " 行；" + "；".join(det[:6]) +
          "。根因：字段内未转义的**英文逗号**被当作分隔符（openuft CSV 卫生禁令）。")
    else:
        P("V0-01", "行字段数一致性（防英文逗号错位）",
          "claims.csv " + str(len(raw_claims)) + " 行、矩阵 " + str(len(raw_matrix)) +
          " 行，每行字段数均等于表头列数（" + str(len(h_claims)) + " / " +
          str(len(h_matrix)) + "），无错位")

    # ---------------- C2 表头
    need_claims = ["claim_id", "statement", "category", "status", "reviewer"]
    miss = [c for c in need_claims if c not in h_claims]
    if miss:
        F("V2-01", "claims.csv 表头契约", "缺失列：" + ", ".join(miss))
    else:
        P("V2-01", "claims.csv 表头契约",
          "列=" + " | ".join(h_claims) + "（必需列齐全）")

    need_matrix = ["现象", "主控子系统", "证据状态", "判定", "备注"]
    miss2 = [c for c in need_matrix if c not in h_matrix]
    if miss2:
        F("V2-02", "现象覆盖矩阵.csv 表头契约", "缺失列：" + ", ".join(miss2))
    else:
        P("V2-02", "现象覆盖矩阵.csv 表头契约",
          "列=" + " | ".join(h_matrix) + "（必需列齐全）")

    # ---------------- C3 claim_id 唯一性与格式
    ids = [r.get("claim_id", "").strip() for r in rows_claims]
    dup = [x for x in set(ids) if ids.count(x) > 1]
    if dup:
        F("V3-01", "claim_id 唯一性", "重复 id：" + ", ".join(sorted(dup)))
    else:
        P("V3-01", "claim_id 唯一性", str(len(ids)) + " 条主张，id 无重复")

    badfmt = [x for x in ids if not re.match(r"^C\d{2,}$", x)]
    if badfmt:
        BO("V3-02", "claim_id 编号格式", "不符合 C## 约定：" + ", ".join(badfmt))
    else:
        P("V3-02", "claim_id 编号格式", "全部匹配 ^C\\d{2,}$")

    nums = sorted(int(x[1:]) for x in ids if re.match(r"^C\d{2,}$", x))
    gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums] if nums else []
    if gaps:
        BO("V3-03", "claim_id 连续性", "缺号 C" + ", C".join(str(x).zfill(2) for x in gaps))
    else:
        P("V3-03", "claim_id 连续性", "C01–C" + str(nums[-1]).zfill(2) + " 连续无缺号")

    # ---------------- C4 单元格卫生（openuft 已知坑）
    bad1 = scan_bad_cells(rows_claims, h_claims)
    bad2 = scan_bad_cells(rows_matrix, h_matrix)
    if bad1 or bad2:
        det = []
        for i, k, kind, v in (bad1 + bad2)[:12]:
            det.append("行" + str(i) + " 列「" + k + "」含" + kind + "：" + v[:60])
        F("V4-01", "单元格禁英文逗号/双引号",
          "命中 " + str(len(bad1) + len(bad2)) + " 处；示例：" + "；".join(det))
    else:
        P("V4-01", "单元格禁英文逗号/双引号",
          "两份 CSV 全部单元格无英文逗号、无双引号（openuft CSV 卫生要求达标）")

    # ---------------- C5 status 值域
    allow_status = {"pass", "open", "boundary", "falsified"}
    got = {}
    for r in rows_claims:
        s = (r.get("status") or "").strip().lower()
        got[s] = got.get(s, 0) + 1
    unknown = [k for k in got if k not in allow_status]
    if unknown:
        F("V5-01", "claims.csv status 值域", "未登记状态值：" + ", ".join(unknown))
    else:
        P("V5-01", "claims.csv status 值域",
          "全部落在 {pass,open,boundary,falsified}；分布：" +
          "，".join(k + "=" + str(v) for k, v in sorted(got.items())))

    IN("V5-02", "claims.csv status 分布统计（供横向对比矩阵计数）",
       "pass=" + str(got.get("pass", 0)) + " / open=" + str(got.get("open", 0)) +
       " / boundary=" + str(got.get("boundary", 0)) +
       " / falsified=" + str(got.get("falsified", 0)) +
       "；合计 " + str(len(rows_claims)) + " 条。" +
       "其中 falsified 为体系**自承**的内部矛盾条目。")

    # ---------------- C6 现象主键唯一
    pk = [(r.get("现象") or "").strip() for r in rows_matrix]
    dupk = [x for x in set(pk) if pk.count(x) > 1]
    if dupk:
        F("V6-01", "现象主键唯一性", "重复现象：" + ", ".join(dupk))
    else:
        P("V6-01", "现象主键唯一性", str(len(pk)) + " 条现象记录，主键无重复")

    # ---------------- C7 判定列值域
    allow_verdict = {"PASS", "FAIL", "BOUNDARY", "INFO"}
    vgot = {}
    for r in rows_matrix:
        s = (r.get("判定") or "").strip().upper()
        vgot[s] = vgot.get(s, 0) + 1
    unk2 = [k for k in vgot if k not in allow_verdict]
    if unk2:
        F("V7-01", "现象覆盖矩阵 判定列值域", "未登记判定值：" + ", ".join(unk2))
    else:
        P("V7-01", "现象覆盖矩阵 判定列值域",
          "落在 {PASS,FAIL,BOUNDARY,INFO}；分布：" +
          "，".join(k + "=" + str(v) for k, v in sorted(vgot.items())))

    # ---------------- C8 证据状态列语义漂移
    egot = {}
    for r in rows_matrix:
        s = (r.get("证据状态") or "").strip().upper()
        egot[s] = egot.get(s, 0) + 1
    mixed = [k for k in egot if k in allow_verdict]
    if mixed:
        BO("V8-01", "『证据状态』列混入了判定值",
           "证据状态列取值：" + "，".join(k + "=" + str(v) for k, v in sorted(egot.items())) +
           "；其中 " + ", ".join(mixed) + " 实为**判定四态**而非证据状态，" +
           "与判定列语义重叠 ⇒ 建议把该列值域收敛为 {OPEN, PASS, BOUNDARY, CONFLICT} 并重命名。")
    else:
        P("V8-01", "『证据状态』列语义",
          "取值：" + "，".join(k + "=" + str(v) for k, v in sorted(egot.items())))

    # ---------------- C9 交叉引用覆盖
    doc_text = ""
    for p in (DOC_AUDIT, DOC_MAIN):
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                doc_text += f.read()
    cited = [x for x in ids if x and x in doc_text]
    uncited = [x for x in ids if x and x not in doc_text]
    if uncited:
        BO("V9-01", "claim_id 在评级文档中的引用覆盖",
           str(len(cited)) + "/" + str(len(ids)) + " 被 00/01 文档显式引用；" +
           "未引用：" + ", ".join(uncited) +
           "（不影响 CSV 合法性，但主张与评级条目的可追溯性有缺口）")
    else:
        P("V9-01", "claim_id 在评级文档中的引用覆盖",
          "全部 " + str(len(ids)) + " 条均在 00/01 文档中被显式引用")

    doc_ids = set(re.findall(r"\bC\d{2,}\b", doc_text))
    orphan = sorted(x for x in doc_ids if x not in ids)
    if orphan:
        BO("V9-02", "文档中出现的 C## 是否都已登记",
           "文档引用但未在 claims.csv 登记：" + ", ".join(orphan))
    else:
        P("V9-02", "文档中出现的 C## 是否都已登记", "无孤儿引用")

    # ---------------- C10 现象 ↔ 子系统 覆盖
    subs = {}
    for r in rows_matrix:
        k = (r.get("主控子系统") or "").strip()
        subs[k] = subs.get(k, 0) + 1
    IN("V10-01", "现象 → 主控子系统 分布",
       "；".join((k if k else "(空)") + "×" + str(v) for k, v in
                sorted(subs.items(), key=lambda kv: -kv[1])))

    return RESULTS


def counts():
    c = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    return c


def render():
    lines = []
    lines.append("# 空间螺旋几何化统一场论 · CSV 元数据校验报告")
    lines.append("")
    lines.append("> 生成脚本：`csv_validate.py`。只报告，不改写原始数据。")
    lines.append("")
    c = counts()
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 判定 | 计数 |")
    lines.append("|------|------|")
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        lines.append("| " + k + " | " + str(c.get(k, 0)) + " |")
    lines.append("")
    lines.append("| 条目 | 判定 | 结论 |")
    lines.append("|------|------|------|")
    for r in RESULTS:
        lines.append("| " + r["id"] + " | " + r["verdict"] + " | " +
                     r["title"].replace("|", "/") + " |")
    lines.append("")
    lines.append("## 逐条明细")
    lines.append("")
    for r in RESULTS:
        lines.append("**" + r["id"] + " · [" + r["verdict"] + "] " + r["title"] + "**")
        lines.append("")
        lines.append(r["detail"])
        lines.append("")
    return "\n".join(lines)


def main():
    run()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
