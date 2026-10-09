# -*- coding: utf-8 -*-
"""
claims 登记列语义修复（UFT-3）——把误填进数值列的文字无损迁回 prediction 列
==============================================================================

背景（它修什么）
----------------
写入侧门禁（`源码/靶场登记列校验_写入侧门禁.py`）首跑读出 9 条违规：

  ERROR 1 条  S15-C0020  `prediction_value = 「第四代粒子存在」`、`prediction_urel = 1.0`
  WARN  8 条  P03-C0001..0009  `prediction_value` 是「15 / 0 / 0」「MSSM M_GUT=2.0e16 GeV; …」
              等**文字/多值摘要**，`prediction_urel` 全空

根因是**字段语义误用**：`claims_schema_升级.py` 给两列的定义是
「无量纲靶的**预测值 + 相对不确定度**」（UFT-3 登记必填，都必须是数）；
对预测的**文字描述**应放在 `prediction` 列。本工具做**无损迁移**：

    prediction_value / prediction_urel 里的非数值内容  →  追加进 prediction 列
    两列清空（回到合法的 `empty` = 未登记状态）

不做的事（红线）
----------------
1. **不做任何猜测性换算**：不把「1e29–1e31 yr」「15 / 0 / 0」猜成一个 (数值, 不确定度) 对——
   那是编造登记。要登记为真靶，须由所属体系给出**无量纲数值 + 相对不确定度**。
2. **数值但非法的内容不迁移**：如 `urel = -0.1`（负数）是数值错误，迁成文字会掩盖问题；
   只报告，交人工处理。
3. **逐字段不变量校验**：迁移后重读全文件，断言除 `prediction` / `prediction_value` /
   `prediction_urel` 三列外，**其余所有列的值逐一不变**、行数与表头不变。
4. 迁移前落 **`.bak` 备份**；产物写**迁移日志**（逐行 before/after），保证可溯源、可回放。

幂等
----
迁移后两列为空 ⇒ 再跑 `--apply` 不再改动（合法行与已迁移行都会被跳过）。

语义真源
--------
数值解析**不在此实现**：导入写入侧门禁的 `parse_number`（mpf + 有理数 a/b），
与门禁、统计层共用同一把尺子。

用法：
    python claims_登记列语义修复.py --check    # 列出将迁移的行（默认）
    python claims_登记列语义修复.py --apply    # 执行迁移（先备份，后校验）
"""

import os
import sys
import csv
import io
import json
import time
import importlib.util

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SYS_DIR = os.path.join(ROOT, "01_独立体系")
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
LOG_PATH = os.path.join(OUT_DIR, "claims_登记列语义修复_迁移日志.json")
GATE = os.path.join(HERE, "靶场登记列校验_写入侧门禁.py")


def load_gate():
    spec = importlib.util.spec_from_file_location("tau_registry_checker", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel_path(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def read_table(path):
    """读取并**校验列宽**：任何行字段数 ≠ 表头宽度 ⇒ 抛 ValueError（带行号与 claim_id）。

    这是被现场教训换来的硬规则：S15 的 claims.csv 存在 16 列行（表头 14 列），
    DictReader 会把多余字段塞进 restkey=None；若不先拒绝，写回时会中途抛错——
    而此时目标文件已被 `open(..., 'w')` 截断，等于把别人的台账写坏（实测发生）。
    口径与 `claims_列对齐修复.py` / `claims_schema_升级.py` 一致：**错位文件先修对齐，
    拒绝盲目自动补列**。"""
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        raw = list(csv.reader(fh))
    if not raw:
        raise ValueError("空文件：" + path)
    header = raw[0]
    for i, r in enumerate(raw[1:], start=2):
        if len(r) != len(header):
            cid = r[0] if r else "（空行）"
            raise ValueError("字段错位：%s 第 %d 行宽 %d ≠ 表头 %d（claim_id=%s）"
                             % (os.path.basename(path), i, len(r), len(header), cid))
    rows = [dict(zip(header, r)) for r in raw[1:]]
    return header, rows


def needs_migration(row, parse_number):
    """返回 (该行是否需迁移, 原因)。数值但非法（负 urel）不迁移，只报告。"""
    pv = (row.get("prediction_value") or "").strip()
    pu = (row.get("prediction_urel") or "").strip()
    if not pv and not pu:
        return False, "empty"
    v = parse_number(pv) if pv else True
    u = parse_number(pu) if pu else True
    if pv and v is None:
        return True, "prediction_value 非数值"
    if pu and u is None:
        return True, "prediction_urel 非数值"
    if pv and pu and v is not None and u is not None and u < 0:
        return False, "数值但非法（urel 为负）⇒ 不迁移，交人工"
    if pv and pu and v is not None and u is not None:
        return False, "ok（合法登记）"
    if pu and v is not None and u is not None and u == 0 and v != int(v):
        return False, "ok（整数靶 urel=0 合法）"
    return False, "ok"


def plan(rows, parse_number):
    out = []
    for i, r in enumerate(rows):
        need, why = needs_migration(r, parse_number)
        out.append({"i": i, "claim_id": (r.get("claim_id") or "").strip(),
                    "need": need, "why": why})
    return out


def migrate_rows(path, header, rows, parse_number):
    """就地迁移 rows（内存中），返回日志条目列表。"""
    entries = []
    for r in rows:
        need, why = needs_migration(r, parse_number)
        if not need:
            continue
        pv = (r.get("prediction_value") or "").strip()
        pu = (r.get("prediction_urel") or "").strip()
        pieces = []
        if pv:
            pieces.append(pv)
        if pu and parse_number(pu) is None:
            pieces.append("urel=" + pu)          # 文字型 urel 一并迁走
        old_pred = (r.get("prediction") or "").strip()
        new_pred = old_pred + ("；" if old_pred and pieces else "") + "；".join(pieces)
        entries.append({
            "file": rel_path(path),
            "claim_id": (r.get("claim_id") or "").strip(),
            "before": {"prediction": old_pred, "prediction_value": pv,
                       "prediction_urel": pu},
            "after": {"prediction": new_pred, "prediction_value": "",
                      "prediction_urel": ""},
            "why": why,
        })
        r["prediction"] = new_pred
        r["prediction_value"] = ""
        r["prediction_urel"] = ""
    return entries


def write_table(path, header, rows):
    """写盘前的最后防线：**先在内存里把全部行序列化**，任何一行都不得产生
    `fields not in fieldnames`（restkey）——通过后才 `open('w')` 截断文件。
    否则就会出现「写一半炸掉、别人台账只剩表头」的事故。"""
    w = csv.DictWriter(io.StringIO(), fieldnames=header, lineterminator="\r\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(w.getvalue())


def verify_invariants(path, before_header, before_rows, before_map):
    """逐字段不变量：表头/行数不变；除三列外所有列的值逐一不变；
    三列只发生在计划内的行上，且与计划一致。"""
    header, rows = read_table(path)
    problems = []
    if header != before_header:
        problems.append("表头变化")
    if len(rows) != len(before_rows):
        problems.append("行数变化 %d → %d" % (len(before_rows), len(rows)))
    watched = {"prediction", "prediction_value", "prediction_urel"}
    for i, (b, a) in enumerate(zip(before_rows, rows)):
        cid = (a.get("claim_id") or "").strip()
        for col in header:
            if col in watched:
                continue
            bv, av = (b.get(col) or ""), (a.get(col) or "")
            if bv != av:
                problems.append("第 %d 行（%s）列 %s 被意外改动：%r → %r"
                                % (i + 1, cid, col, bv[:40], av[:40]))
        rec = before_map.get(cid)
        if rec is None:
            if (a.get("prediction_value") or "") != (b.get("prediction_value") or "") \
               or (a.get("prediction_urel") or "") != (b.get("prediction_urel") or "") \
               or (a.get("prediction") or "") != (b.get("prediction") or ""):
                problems.append("第 %d 行（%s）不在计划内却被改动" % (i + 1, cid))
            continue
        if (a.get("prediction") or "") != rec["after"]["prediction"]:
            problems.append("第 %d 行（%s）prediction 与计划不符" % (i + 1, cid))
        if (a.get("prediction_value") or "") or (a.get("prediction_urel") or ""):
            problems.append("第 %d 行（%s）数值列未清空" % (i + 1, cid))
    return problems


def check_text_preserved(path, before_map):
    """迁移出的每段文字都必须完整出现在该行 prediction 列里。"""
    header, rows = read_table(path)
    problems = []
    by_id = {(r.get("claim_id") or "").strip(): r for r in rows}
    for cid, rec in before_map.items():
        row = by_id.get(cid)
        if row is None:
            problems.append("%s 行消失" % cid)
            continue
        pred = row.get("prediction") or ""
        for piece in (rec["before"]["prediction_value"],
                      rec["before"]["prediction_urel"]):
            if piece and piece not in pred:
                problems.append("%s 的文字未完整保留：「%s」" % (cid, piece[:40]))
    return problems


def rebuild_log():
    """从 `*.bak_语义修复_*` 备份**只读重建**迁移日志。

    为什么需要：首跑 --apply 在错位文件上崩溃（见判定册 §9.3），P03 的迁移实际已完成，
    但日志写在流程末尾 ⇒ 丢失。溯源不能靠「记得」，必须能从备份重放。
    本模式不写任何台账、不迁移任何行，只重建日志。
    """
    import glob
    pairs = {}
    for bak in sorted(glob.glob(os.path.join(SYS_DIR, "*", "claims.csv.bak_语义修复_*"))):
        orig = bak.split(".bak_")[0]
        pairs[orig] = bak
    gate = load_gate()
    parse_number = gate.parse_number
    entries, skipped = [], []
    for orig, bak in sorted(pairs.items()):
        try:
            header, rows = read_table(bak)
        except ValueError as exc:
            skipped.append({"file": rel_path(orig), "reason": str(exc)})
            continue
        if not all(c in header for c in ("prediction", "prediction_value", "prediction_urel")):
            continue
        for r in rows:
            need, why = needs_migration(r, parse_number)
            if not need:
                continue
            pv = (r.get("prediction_value") or "").strip()
            pu = (r.get("prediction_urel") or "").strip()
            pieces = [x for x in (pv, "urel=" + pu if (pu and parse_number(pu) is None) else "") if x]
            old_pred = (r.get("prediction") or "").strip()
            new_pred = old_pred + ("；" if old_pred and pieces else "") + "；".join(pieces)
            entries.append({
                "file": rel_path(orig),
                "claim_id": (r.get("claim_id") or "").strip(),
                "before": {"prediction": old_pred, "prediction_value": pv,
                           "prediction_urel": pu},
                "after": {"prediction": new_pred, "prediction_value": "",
                          "prediction_urel": ""},
                "why": why, "reconstructed": True,
            })
    os.makedirs(OUT_DIR, exist_ok=True)
    log = {"updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "mode": "reconstructed-from-backup（只读重建，未写任何台账）",
           "skipped": skipped, "entries": entries}
    with open(LOG_PATH, "w", encoding="utf-8") as fh:
        json.dump(log, fh, ensure_ascii=False, indent=2)
    print("重建迁移日志：%d 条（跳过错位文件 %d 个）→ 数据/claims_登记列语义修复_迁移日志.json"
          % (len(entries), len(skipped)))
    for e in entries:
        print("  %-12s value=「%s」⇒ prediction=「%s」"
              % (e["claim_id"], e["before"]["prediction_value"][:32],
                 e["after"]["prediction"][:48]))
    for s in skipped:
        print("  [跳过] %s：%s" % (s["file"], s["reason"]))
    return 0


def main():
    if "--rebuild-log" in sys.argv:
        return rebuild_log()
    apply_mode = "--apply" in sys.argv
    gate = load_gate()
    parse_number = gate.parse_number

    targets = []
    if os.path.isdir(SYS_DIR):
        for name in sorted(os.listdir(SYS_DIR)):
            p = os.path.join(SYS_DIR, name, "claims.csv")
            if os.path.isfile(p):
                targets.append(p)

    print("=" * 78)
    print("claims 登记列语义修复（UFT-3）· %s" % ("APPLY" if apply_mode else "CHECK"))
    print("=" * 78)

    # ---- 计划阶段：只读，逐文件列出将迁移的行 ----
    plans = []                     # (path, entries, before_rows)
    total = 0
    for path in targets:
        try:
            header, rows = read_table(path)
        except ValueError as exc:
            # 字段错位 ⇒ 拒迁（先修对齐，见 read_table 文档头）；不中断其它文件
            print("\n[拒迁] %s\n    %s" % (rel_path(path), exc))
            continue
        if not all(c in header for c in ("prediction", "prediction_value", "prediction_urel")):
            continue
        pl = plan(rows, parse_number)
        n_need = sum(1 for x in pl if x["need"])
        if not n_need:
            continue
        print("\n%s（%d 行待迁移）" % (rel_path(path), n_need))
        for x in pl:
            if x["need"]:
                r = rows[x["i"]]
                print("  [迁] %-12s value=「%s」urel=「%s」"
                      % (x["claim_id"],
                         (r.get("prediction_value") or "")[:36],
                         (r.get("prediction_urel") or "")[:16]))
        plans.append((path, header, rows))
        total += n_need

    if not total:
        print("\n无需迁移（登记列已全部合规）。")
        return 0
    if not apply_mode:
        print("\n共 %d 行待迁移。以上为计划；执行请加 --apply。" % total)
        return 0

    # ---- APPLY：备份 → 迁移 → 写回 → 逐字段校验 → 日志 ----
    stamp = time.strftime("%Y%m%d_%H%M%S")
    ok = True
    all_entries = []
    backups = {}
    for path, header, rows in plans:
        bak = path + ".bak_语义修复_" + stamp
        with open(path, "rb") as fi, open(bak, "wb") as fo:
            fo.write(fi.read())
        backups[path] = bak

    for path, header, rows in plans:
        entries = migrate_rows(path, header, rows, parse_number)
        all_entries.extend(entries)
        write_table(path, header, rows)

    for path, header, rows in plans:
        b_header, b_rows = read_table(backups[path])
        before_map = {e["claim_id"]: e for e in all_entries if e["file"] == rel_path(path)}
        problems = verify_invariants(path, b_header, b_rows, before_map)
        problems += check_text_preserved(path, before_map)
        if problems:
            ok = False
            print("\n[FAIL] %s" % rel_path(path))
            for p in problems:
                print("    " + p)
        else:
            print("\n[OK] %s（%d 行迁移；逐字段不变量与文字保全校验通过）"
                  % (rel_path(path), len(before_map)))

    os.makedirs(OUT_DIR, exist_ok=True)
    log = {"updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "backups": {rel_path(k): rel_path(v) for k, v in backups.items()},
           "entries": all_entries}
    with open(LOG_PATH, "w", encoding="utf-8") as fh:
        json.dump(log, fh, ensure_ascii=False, indent=2)

    print("-" * 78)
    print("迁移日志：数据/claims_登记列语义修复_迁移日志.json（%d 条）" % len(all_entries))
    print("备份：*.bak_语义修复_%s" % stamp)
    if not ok:
        print("结论：校验未通过 —— 请用备份回退后人工核查。")
        return 1
    print("结论：迁移完成，逐字段不变量与文字保全校验全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
