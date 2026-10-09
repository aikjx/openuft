# -*- coding: utf-8 -*-
"""
统一场论达成度总账 · 全体系×全维度×全链路×全力 · 机器核验脚本（2026-10-09）

目的
----
把"继续完成物理全体系全维度全链路全力的统一场论"在本项目语境下**可机器判定的部分**
收敛为一组合 invariants，并断言它们全部成立。本脚本**不**证明任何统一场论已成立；
它只核验"诚实边界总账"所依赖的跨文档不变量是否仍然自洽。

核验的不变量
------------
1. system_registry.json：体系数 == 22，且 validated 状态数 == 0（红线）。
2. 状态看板 状态看板.md：含"零个 进入 validated"红线声明。
3. F4/E9 跨册门禁（常态化合冒）：自验 4/4、双锚点 ok、总判定 ✓ 通过。
4. 四力本源审计判定册：含关键结论串（"「四」不是本源数字" / 两个元开放问题未回答）。
5. claims.csv：全仓 falsified 登记总数 > 0（证明"冲突必须显式登记"纪律在执行）。

出口
----
输出 JSON 账本到同目录 `统一场论达成度总账_核验_out_2026-10-09.json`；
全部断言通过则 sys.exit(0)，否则 sys.exit(1)。
"""

import os
import re
import sys
import json
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
# ROOT = <repo>/my_lib  （本脚本在 openuft/04_公共成果/本项目_全维自洽与归一化/源码）
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 4)))

REGISTRY = os.path.join(ROOT, "openuft", "00_项目治理", "system_registry.json")
BOARD = os.path.join(ROOT, "openuft", "04_公共成果", "状态看板.md")
GATE_OUT = os.path.join(ROOT, "scratch", "_f4e9_gate_out.txt")
FOUR_FORCE = os.path.join(
    ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化",
    "判定_四力本源_层级与可统一性的机器审计_2026-10-07.md",
)
OPEN_DIR = os.path.join(ROOT, "openuft")


def section(title):
    print("=" * 70)
    print(title)
    print("=" * 70)


def find_systems(data):
    if isinstance(data, dict) and isinstance(data.get("systems"), list):
        return data["systems"]
    return None


def check_registry(ledger):
    section("[1] system_registry.json 体系计数与红线")
    with open(REGISTRY, encoding="utf-8") as f:
        data = json.load(f)
    systems = find_systems(data)
    assert systems is not None, "system_registry.json 缺少 systems 列表"
    n = len(systems)
    cnt = collections.Counter()
    for s in systems:
        cnt[str(s.get("status", "?")).lower()] += 1
    validated = [s.get("id") for s in systems if str(s.get("status", "")).lower() == "validated"]
    print(f"  体系总数 = {n}")
    print(f"  状态计数 = {dict(cnt)}")
    print(f"  validated 数 = {len(validated)} -> {validated}")
    # 不变量断言
    assert n == 22, f"体系总数应为 22，实为 {n}"
    assert len(validated) == 0, f"存在 validated 体系：{validated} —— 违反红线"
    ledger["registry"] = {"n_systems": n, "status_counts": dict(cnt), "n_validated": 0}
    print("  [OK] 22 体系 / 0 validated（红线满足）")
    return True


def check_board(ledger):
    section("[2] 状态看板.md 红线声明")
    txt = open(BOARD, encoding="utf-8", errors="ignore").read()
    has_redline = ("零个" in txt and "validated" in txt) or ("零个 进入" in txt)
    print(f"  含 '零个 ... validated' 红线声明：{has_redline}")
    assert has_redline, "状态看板缺少 '零个 进入 validated' 红线声明"
    # 提取健康度分布（看板叙述 "C 6 · O 10 · H 2 · U 4"）
    m = re.search(r"C\s*(\d+)\s*·\s*O\s*(\d+)\s*·\s*H\s*(\d+)\s*·\s*U\s*(\d+)", txt)
    if m:
        cohu = {"C": int(m.group(1)), "O": int(m.group(2)),
                "H": int(m.group(3)), "U": int(m.group(4))}
        print(f"  看板健康度分布 = {cohu}（合计 {sum(cohu.values())}）")
        ledger["board_health"] = cohu
    ledger["board_redline"] = True
    print("  [OK] 红线声明存在")
    return True


def check_gate(ledger):
    section("[3] F4/E9 跨册门禁（常态化）")
    assert os.path.exists(GATE_OUT), f"缺失 gate 输出 {GATE_OUT}"
    txt = open(GATE_OUT, encoding="utf-8", errors="ignore").read()
    c1 = bool(re.search(r"自验案例\s*4\s*/\s*通过\s*4", txt))
    c2 = "双锚点 ok = True" in txt
    c3 = "总判定" in txt and "✓ 通过" in txt
    print(f"  自验 4/4：{c1}；双锚点 ok：{c2}；总判定通过：{c3}")
    assert c1 and c2 and c3, "F4/E9 门禁未全通过"
    ledger["f4e9_gate"] = {"self_test_4of4": c1, "dual_anchor_ok": c2, "overall_pass": c3}
    print("  [OK] F4/E9 门禁 PASS（常态化运行）")
    return True


def check_four_force(ledger):
    section("[4] 四力本源审计 · 关键结论已登记")
    assert os.path.exists(FOUR_FORCE), f"缺失四力判定册 {FOUR_FORCE}"
    txt = open(FOUR_FORCE, encoding="utf-8", errors="ignore").read()
    needles = [
        "「四」不是本源数字",
        "为何是这个规范群",
        "量子引力",
    ]
    hits = {n: (n in txt) for n in needles}
    print("  关键结论串命中：")
    for k, v in hits.items():
        print(f"    - {k!r}: {v}")
    assert all(hits.values()), f"四力册缺失关键结论：{[k for k,v in hits.items() if not v]}"
    # 提取裁定计数
    m = re.search(r"PASS\s*(\d+)\s*/\s*FAIL\s*(\d+)\s*/\s*BOUNDARY\s*(\d+)", txt)
    if m:
        ledger["four_force_verdict"] = {
            "PASS": int(m.group(1)), "FAIL": int(m.group(2)), "BOUNDARY": int(m.group(3))
        }
        print(f"  裁定计数 = {ledger['four_force_verdict']}")
    ledger["four_force_conclusion_registered"] = True
    print("  [OK] 四力本源审计结论已登记（力非本源 / 开放=规范群选择+量子引力）")
    return True


def check_claims(ledger):
    section("[5] claims.csv · falsified 登记纪律在执行")
    total = 0
    per_system = collections.Counter()
    for dp, _, fns in os.walk(OPEN_DIR):
        if ".git" in dp.split(os.sep):
            continue
        for fn in fns:
            if fn.lower() == "claims.csv":
                p = os.path.join(dp, fn)
                try:
                    with open(p, encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            # 宽松匹配：status 列含 falsified
                            if re.search(r"\bfalsified\b", line, re.I):
                                total += 1
                                # 体系标识：取距 openuft 的路径第二段（体系目录）
                                rel = os.path.relpath(p, OPEN_DIR)
                                parts = rel.split(os.sep)
                                sysid = parts[1] if len(parts) > 1 else parts[0]
                                per_system[sysid] += 1
                except Exception as e:
                    print(f"  [warn] 读取 {p} 失败：{e}")
    print(f"  全仓 falsified claim 登记总数 = {total}")
    print(f"  涉及体系数 = {len(per_system)}")
    assert total > 0, "claims.csv 中无任何 falsified 登记 —— 与审计结论矛盾"
    ledger["claims_falsified"] = {"total": total, "n_systems": len(per_system)}
    print("  [OK] 冲突显式登记纪律在执行（falsified 总数 > 0）")
    return True


def run_all():
    """执行全部不变量核验，返回 (ledger, ok)。不调用 sys.exit，便于被 wrapper 导入。"""
    ledger = {
        "doc": "统一场论达成度总账_全体系全维度全链路全力_核验",
        "date": "2026-10-09",
        "root": ROOT,
        "assertions": [],
    }
    try:
        check_registry(ledger)
        check_board(ledger)
        check_gate(ledger)
        check_four_force(ledger)
        check_claims(ledger)
    except AssertionError as e:
        print("\n[FAIL] 断言失败：", e)
        ledger["overall"] = "FAIL"
        ledger["error"] = str(e)
        out = os.path.join(HERE, "统一场论达成度总账_核验_out_2026-10-09.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)
        print(f"[out] 账本已写 {out}")
        return ledger, False

    ledger["overall"] = "PASS"
    out = os.path.join(HERE, "统一场论达成度总账_核验_out_2026-10-09.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
    print("\n" + "=" * 70)
    print("总判定: ✓ 通过 —— 达成度总账的全部跨文档不变量自洽")
    print(f"[out] 账本已写 {out}")
    return ledger, True


def main():
    _, ok = run_all()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
