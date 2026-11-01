# -*- coding: utf-8 -*-
"""
企业级验收总入口 **单命令**（CI 友好）—— `_run_audit_all.py`

编排三层验证，任一环节失败 ⇒ 总退出码非 0：
  ① **源级可复现**：复跑本次迁移到权威门禁的卷（r334 / r340），证明「源可重算」而非仅产物完好；
     （r340 用区别化 runner `_run_r340_alpha.py`，规避与并行册共用 `_run_r340.py` 被覆盖）
  ② **统一验收门禁卷 r345**：327 份 r-json 语料的两级回归（Tier-1 严格 / Tier-2 可读性）
     + 8 例门禁电池覆盖 5 分支 + 撞号防御 + manifest 一致性；
  ③ 汇总退出码。

纪律：
  - 中文路径不进 argv ⇒ 一律 `cwd=<源码目录>` 后传**相对**脚本名（复刻本库 ASCII runner 惯例）。
  - 本脚本只做编排，不改写任何卷的字节；不回填 README / 09，不 git。
"""
import os
import subprocess
import sys

BASE = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"

# ① 源级复跑目标（本次迁移到权威门禁的卷；相对名，避免中文进 argv）
SOURCE_RERUN = ["_run_r334.py", "_run_r340_alpha.py"]
# ② 验收门禁卷
ACCEPTANCE = ["_run_r345.py"]


def run_one(script):
    """在 BASE 下以相对名执行单个 runner，返回 (ok, 摘要尾部 2 行)。"""
    try:
        p = subprocess.run([sys.executable, script], cwd=BASE,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
    except Exception as exc:                                   # 执行器本身异常
        return False, "EXC: %s" % type(exc).__name__
    out = (p.stdout or "") + (p.stderr or "")
    tail = [ln for ln in out.strip().splitlines() if ln.strip()][-2:] or ["(无输出)"]
    return (p.returncode == 0), " | ".join(tail)


def main():
    print("=" * 72)
    print("TUFT 企业级验收总入口（三层）")
    print("=" * 72)
    failures = []

    print("\n[① 源级可复现] 复跑迁移到权威门禁的卷")
    for s in SOURCE_RERUN:
        ok, tail = run_one(s)
        print("  [%s] %-24s %s" % ("OK" if ok else "FAIL", s, tail))
        if not ok:
            failures.append(s)

    print("\n[② 统一验收门禁卷] 全语料两级回归 + 门禁电池 + 撞号防御")
    for s in ACCEPTANCE:
        ok, tail = run_one(s)
        print("  [%s] %-24s %s" % ("OK" if ok else "FAIL", s, tail))
        if not ok:
            failures.append(s)

    print("\n" + "=" * 72)
    if failures:
        print("总判：**FAILED** —— 失败环节: %s" % ", ".join(failures))
        return 1
    print("总判：**ALL PASSED** —— 源级可复现 + 全语料回归 + 门禁电池 三层全绿")
    return 0


if __name__ == "__main__":
    sys.exit(main())
