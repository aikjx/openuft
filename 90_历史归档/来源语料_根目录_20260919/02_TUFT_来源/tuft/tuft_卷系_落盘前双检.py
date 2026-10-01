# -*- coding: utf-8 -*-
"""
tuft_卷系_落盘前双检.py
=======================
把「落盘前双检」固化为**一条命令**（可挂到提交钩子 / 批次流程）：

  ① **结构完整性**（`tuft_卷系_归一化总览.py`）：CURATED 索引 / 缺号 / 重号 / 哈希漂移 / 脚本落盘 / 反回退守卫
  ② **构造可行性**（`tuft_卷系_构造可行性门禁.py`）：定理 A~I 覆盖完整性 + 扇区重复登记 + 新提案自查表

任一不通过 ⇒ **非零退出**，并输出差异摘要。

用法：
    python tuft_卷系_落盘前双检.py                     # 双检（推荐）
    python tuft_卷系_落盘前双检.py --quick             # 只跑结构完整性
    python tuft_卷系_落盘前双检.py --check <提案>.json  # 双检 + 追加校验新提案自查表

红线：本册只做**门禁编排**，不新增物理主张、不改动任何 CURATED 真源状态。
"""

from __future__ import print_function

import hashlib
import os
import re
import subprocess
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
STRUCT = os.path.join(HERE, "tuft_卷系_归一化总览.py")
GATE = os.path.join(HERE, "tuft_卷系_构造可行性门禁.py")
OUT = os.path.join(HERE, "tuft_卷系_落盘前双检_report.txt")


def _run(script, extra=()):
    cmd = [sys.executable, script] + list(extra)
    try:
        proc = subprocess.run(cmd, cwd=HERE, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=1800)
        out = proc.stdout.decode("utf-8", "replace")
        return proc.returncode, out
    except Exception as exc:                                     # noqa: BLE001
        return 1, "运行失败：%s" % exc


def check_structure(quick=False):
    rc, out = _run(STRUCT)
    m = re.search(r"条目 (\d+)；缺号 (\S+?)。?；问题 (\d+)", out) or \
        re.search(r"条目 (\d+)；缺号 (\S+)；问题 (\d+)", out)
    info = {"rc": rc, "raw": out}
    if m:
        info["n_entries"] = int(m.group(1))
        info["gaps"] = m.group(2)
        info["problems"] = int(m.group(3))
    else:
        info["n_entries"] = info["gaps"] = info["problems"] = None
    info["ok"] = (rc == 0 and info["problems"] == 0 and info["gaps"] == "无")
    return info


def check_gate(check_file=None):
    extra = ["--check", check_file] if check_file else []
    rc, out = _run(GATE, extra)
    info = {"rc": rc, "raw": out}
    m = re.search(r"PASS = (\d+) / FAIL = (\d+) / BOUNDARY = (\d+) / INFO = (\d+)", out)
    info["pass"] = int(m.group(1)) if m else None
    info["fail"] = int(m.group(2)) if m else None
    v3 = dict((k, ("[PASS] V3%s" % k) in out) for k in "abc")
    info["v3"] = v3
    info["v5"] = "[PASS] V5" in out
    info["v5_fail"] = "[FAIL] V5" in out
    info["ok"] = (rc == 0 and info["fail"] == 0 and all(v3.values()) and info["v5"])
    return info


def main():
    args = sys.argv[1:]
    quick = "--quick" in args
    check_file = None
    if "--check" in args:
        i = args.index("--check")
        check_file = args[i + 1] if len(args) > i + 1 else None

    t0 = time.time()
    L = []
    L.append("=" * 76)
    L.append("TUFT / H-TUFT 卷系·落盘前双检（结构完整性 + 构造可行性）")
    L.append("=" * 76)

    st = check_structure(quick)
    L.append("[双检① 结构完整性] %s" % ("✅ 通过" if st["ok"] else "❌ 不通过"))
    L.append("   条目 = %s ；缺号 = %s ；问题 = %s" % (st["n_entries"], st["gaps"], st["problems"]))
    for line in st["raw"].splitlines():
        if line.strip().startswith(("[重号]", "[反回退违规]", "[缺号]", "[哈希漂移]", "[未落盘]")):
            L.append("   ⚠ %s" % line.strip())

    gt = None
    if not quick:
        gt = check_gate(check_file)
        L.append("[双检② 构造可行性] %s" % ("✅ 通过" if gt["ok"] else "❌ 不通过"))
        L.append("   PASS = %s ；FAIL = %s" % (gt["pass"], gt["fail"]))
        L.append("   覆盖完整性 V3a/V3b/V3c = %s/%s/%s ；扇区去重 V5 = %s"
                 % (gt["v3"]["a"], gt["v3"]["b"], gt["v3"]["c"], gt["v5"]))
        for line in gt["raw"].splitlines():
            if line.startswith(("[FAIL]", "[BOUNDARY] V5")):
                L.append("   ⚠ %s" % line.strip())

    ok = st["ok"] and (gt is None or gt["ok"])
    L.append("-" * 76)
    L.append("双检结论：%s（耗时 %.1fs）" % ("✅ 允许落盘" if ok else "❌ 禁止落盘", time.time() - t0))
    if not ok:
        L.append("  处置：①结构问题 ⇒ 修 CURATED/hash/编号；②覆盖问题 ⇒ 补定理登记或显式豁免；"
                 "③扇区问题 ⇒ 在 tuft_卷系_扇区真源登记.md 指定规范真源")
    L.append("红线：本册只做门禁编排，不新增物理主张、不改动真源。")

    text = "\n".join(L) + "\n"
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(os.path.abspath(__file__), "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    text2 = text + "自哈希(SHA256) = %s\n" % sha
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text2)
    print(text2)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
