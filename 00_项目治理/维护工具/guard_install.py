#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
guard_install.py —— 把「openuft 全维守卫 guard_all.py」固化为 git pre-commit 门禁
=============================================================================
全维分形知识自动演化引擎的「写入即拦」闭环：任何涉及核心治理资产的提交，
在写入前自动运行 guard_all.py（复用已全绿的 verify.py），未通过即阻断提交。

设计要点（沿用 openuft 门禁红线，与 TUFT 卷系门禁同一套纪律）：
  · **不改 git config**（不设 core.hooksPath），只追加写入标准 `.git/hooks/pre-commit`；
  · **不覆盖已有门禁**：TUFT 卷系双检段（若已安装）保留在前，本段追加在后；
  · 已有 pre-commit 会被**备份**为 `pre-commit.bak.<时间戳>`，可 `--uninstall` 还原；
  · **只触发核心治理资产**：仅当本次提交涉及 claims.csv / system.json / layout /
    system_registry / chapter_provenance / verify.py / 维护工具 / 迁移记录 / 审计记录
    时运行守卫，避免阻断无关提交；
  · 逃生门：`git commit --no-verify`（git 原生，不可被本工具关闭）；
    `OPENUFT_GUARD_SKIP=1`（guard_all.py 自身支持，供 CI/演练）。
  · 幂等：已含本段则跳过，不重复追加。

红线：本工具只做门禁编排，不改动任何 CURATED 真源、不新增物理主张、不复制校验逻辑
      （校验单一真源 = verify.py，经 guard_all.py 调用）。

用法：
  python 00_项目治理/维护工具/guard_install.py             # 安装（幂等）
  python 00_项目治理/维护工具/guard_install.py --status    # 查看当前 pre-commit 结构
  python 00_项目治理/维护工具/guard_install.py --uninstall # 卸载（还原最近备份）
  python 00_项目治理/维护工具/guard_install.py --test      # 演练：制造假提交 → 期望触发守卫
"""
from __future__ import print_function

import os
import subprocess
import sys
import time
from pathlib import Path

MARK = "# === openuft 全维守卫（guard_all.py，由 guard_install.py 追加；--uninstall 还原备份）==="

GUARD_SEGMENT = (
    "\n"
    "# === openuft 全维守卫（guard_all.py，由 guard_install.py 追加；--uninstall 还原备份）===\n"
    "# 触发范围：本次提交涉及核心治理资产时，运行全维守卫；未通过即阻断提交。\n"
    "# 逃生门：git commit --no-verify ；OPENUFT_GUARD_SKIP=1（guard_all.py 内部支持）\n"
    "TOP2=$(git rev-parse --show-toplevel 2>/dev/null)\n"
    "if [ -n \"$TOP2\" ] && [ \"${TUFT_HOOK_FORCE:-0}\" != \"1\" ]; then\n"
    "  if git diff --cached --name-only | grep -Eq \"(claims\\\\.csv|system\\\\.json|layout\\\\.json|"
    "system_registry\\\\.json|module_types\\\\.json|chapter_provenance\\\\.json|^verify\\\\.py|"
    "00_项目治理/维护工具/|00_项目治理/审计记录/|90_历史归档/迁移记录/)\"; then\n"
    "    echo \"[openuft 全维守卫] 本次提交涉及治理资产 => 运行全维校验...\" >&2\n"
    "    PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null)\n"
    "    if [ -n \"$PY\" ]; then\n"
    "      \"$PY\" -B \"$TOP2/00_项目治理/维护工具/guard_all.py\"\n"
    "      if [ $? -ne 0 ]; then\n"
    "        echo \"\" >&2\n"
    "        echo \"❌ openuft 全维守卫未通过 => 提交已阻断（逃生：git commit --no-verify）\" >&2\n"
    "        exit 1\n"
    "      fi\n"
    "      echo \"✅ openuft 全维守卫通过\" >&2\n"
    "    fi\n"
    "  fi\n"
    "fi\n"
    "# === openuft 全维守卫结束 ===\n"
)


def hooks_dir(root):
    return root / ".git" / "hooks"


def precommit_path(root):
    return hooks_dir(root) / "pre-commit"


def read_precommit(root):
    p = precommit_path(root)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    here = Path(__file__).resolve().parent
    root = here.parent.parent
    pc = precommit_path(root)
    cur = read_precommit(root)

    arg = sys.argv[1] if len(sys.argv) > 1 else "install"

    if arg == "--status":
        print("pre-commit 存在:", pc.exists())
        print("已含 openuft 全维守卫段:", MARK in cur)
        print("已含 TUFT 卷系门禁段:", "TUFT" in cur)
        print("--- 当前 pre-commit 行数:", cur.count("\n") + (1 if cur else 0))
        return 0

    if arg == "--uninstall":
        if not pc.exists():
            print("无 pre-commit，无需卸载")
            return 0
        # 还原最近备份
        baks = sorted(hooks_dir(root).glob("pre-commit.bak.*"))
        if not baks:
            print("未找到备份 pre-commit.bak.*，跳过还原")
            return 0
        src = baks[-1]
        pc.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print("已从 %s 还原 pre-commit" % src.name)
        return 0

    if arg == "--test":
        # 只读演练：确认触发正则能在「核心资产」上命中
        import re
        pat = r"(claims\.csv|system\.json|layout\.json|system_registry\.json|module_types\.json|chapter_provenance\.json|^verify\.py|00_项目治理/维护工具/|00_项目治理/审计记录/|90_历史归档/迁移记录/)"
        probes = ["00_项目治理/维护工具/guard_all.py", "01_独立体系/S05_HDU高维紧致化统一/claims.csv",
                  "00_项目治理/审计记录/DIRECTORY_AUDIT.md", "90_历史归档/迁移记录/20261003_毕业迁移与改名/毕业迁移清单.json",
                  "verify.py", "01_独立体系/S02_空间光速螺旋统一力/02_基础公设/source_chapter.md",
                  "README.md", "03_跨体系研究/物理领域/大统一/README.md"]
        for probe in probes:
            hit = bool(re.search(pat, probe))
            print(("HIT  " if hit else "pass ") + probe)
        # 正例应命中，反例（纯 README/体系内容）不应命中
        return 0

    # install（幂等）
    if MARK in cur:
        print("已安装 openuft 全维守卫段，幂等跳过（--uninstall 可卸载）")
        return 0

    hooks_dir(root).mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    if pc.exists():
        bak = hooks_dir(root) / ("pre-commit.bak." + ts)
        bak.write_text(cur, encoding="utf-8")
        print("已备份原 pre-commit => %s" % bak.name)
    new = cur.rstrip() + "\n" + GUARD_SEGMENT
    pc.write_text(new, encoding="utf-8")
    print("openuft 全维守卫段已追加到 pre-commit（幂等可重复；--uninstall 还原备份）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
