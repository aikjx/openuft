# -*- coding: utf-8 -*-
"""
tuft_安装提交钩子.py
====================
把「**落盘前双检**」固化为 **git 提交钩子（pre-commit）**——直接封堵一个**已复现两次**的流程缺口：

    新条目落盘（CUR-22 / CUR-24）但**未登记覆盖矩阵** ⇒ 门禁首跑即 FAIL。

三次拦截中有两次同因 ⇒ 说明这不是偶发，而是**流程缺口**：靠事后人工补登不可靠。
本安装器把「新条目落盘」与「覆盖矩阵登记」**原子化**：只要本次提交涉及卷系目录，
就会强制运行 `tuft_卷系_落盘前双检.py`（结构完整性 ⊕ 构造可行性），**未通过即阻断提交**。

设计要点（诚实）：
  · **不改动 git config**（不设 `core.hooksPath`）——只写入仓库标准的 `.git/hooks/pre-commit`；
  · 已有 pre-commit 会被**备份**为 `pre-commit.bak.<时间戳>`，可 `--uninstall` 还原；
  · 钩子只在本提交**涉及卷系目录**时触发（避免阻断无关提交）；
  · 可用 `git commit --no-verify` 临时绕过（git 原生逃生门，**不可**被本工具关闭）；
  · 测试用逃生门：环境变量 `TUFT_HOOK_FORCE=1` 可强制执行（用于自检/演练）。

用法：
    python tuft_安装提交钩子.py              # 安装（幂等）
    python tuft_安装提交钩子.py --status     # 查看状态
    python tuft_安装提交钩子.py --uninstall  # 卸载（还原备份）
    python tuft_安装提交钩子.py --test       # 端到端演练（临时制造违规 ⇒ 期望被阻断 ⇒ 自动清理）

红线：本工具只做**门禁编排**，不新增物理主张、不改动任何 CURATED 真源状态。
"""

from __future__ import print_function

import hashlib
import os
import shutil
import subprocess
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK_NAME = "pre-commit"
MARKER = "# TUFT 卷系门禁钩子 v1（由 tuft_安装提交钩子.py 写入）"

# 钩子本体（POSIX sh；git for Windows 自带 sh）。
# `__CORPUS__` 由安装器替换为卷系目录相对仓库根的路径。
HOOK_TEMPLATE = """#!/bin/sh
__MARKER__
# 作用：当本次提交涉及卷系目录时，强制运行「落盘前双检」（结构完整性 ⊕ 构造可行性）。
#       未通过即**阻断提交** —— 封堵「新条目落盘但未登记覆盖矩阵」这一流程缺口。
# 安装/卸载：python tuft_安装提交钩子.py  /  ... --uninstall
# 临时绕过：git commit --no-verify     强制执行（测试）：TUFT_HOOK_FORCE=1
CORPUS_REL="__CORPUS__"
TOP=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOP" ]; then
  exit 0
fi
if [ "${TUFT_HOOK_FORCE:-0}" != "1" ]; then
  # 用纯 ASCII 片段匹配，避免 core.quotepath 把中文路径转义成八进制而漏判
  if ! git diff --cached --name-only | grep -q "02_TUFT_"; then
    exit 0
  fi
fi
PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null)
if [ -z "$PY" ]; then
  echo "[TUFT 双检] 跳过：未找到 python 解释器（钩子不阻断）" >&2
  exit 0
fi
if ! cd "$TOP/$CORPUS_REL" 2>/dev/null; then
  echo "[TUFT 双检] 失败：未找到卷系目录 $CORPUS_REL" >&2
  exit 1
fi
echo "[TUFT 双检] 本次提交涉及卷系 ⇒ 运行 结构完整性 + 构造可行性 ..."
"$PY" tuft_卷系_落盘前双检.py
if [ $? -ne 0 ]; then
  echo "" >&2
  echo "❌ TUFT 卷系落盘前双检未通过 ⇒ 提交已阻断（临时绕过：git commit --no-verify）" >&2
  echo "   处置：见 tuft_卷系_落盘前双检_report.txt 的『双检结论』；" >&2
  echo "         未登记覆盖 ⇒ 在 tuft_卷系_结构障碍定理族.md §6 覆盖矩阵补登定理命中" >&2
  exit 1
fi
echo "✅ TUFT 双检通过"
exit 0
"""


def git(*args):
    proc = subprocess.run(["git"] + list(args), cwd=HERE, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip()


def repo_root():
    rc, out = git("rev-parse", "--show-toplevel")
    if rc != 0 or not out:
        return None
    return out.replace("/", os.sep)


def corpus_rel(top):
    """卷系目录相对仓库根的路径（POSIX 风格，供钩子内 cd 使用）。"""
    rel = os.path.relpath(HERE, top).replace(os.sep, "/")
    return rel


def hook_path(top):
    return os.path.join(top, ".git", "hooks", HOOK_NAME)


def build_hook(top):
    body = HOOK_TEMPLATE.replace("__MARKER__", MARKER).replace("__CORPUS__", corpus_rel(top))
    return body


def do_status(top):
    hp = hook_path(top)
    print("仓库根   ：%s" % top)
    print("卷系目录 ：%s" % corpus_rel(top))
    print("钩子路径 ：%s" % hp)
    if not os.path.exists(hp):
        print("状态     ：❌ 未安装")
        return 1
    with open(hp, "r", encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    if MARKER in txt:
        print("状态     ：✅ 已安装（本工具写入，v1）")
        return 0
    print("状态     ：⚠ 存在钩子但**不是本工具写入**（安装时会自动备份，不覆盖丢失）")
    return 2


def do_uninstall(top):
    hp = hook_path(top)
    if not os.path.exists(hp):
        print("卸载：无钩子，无需处理")
        return 0
    with open(hp, "r", encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    if MARKER not in txt:
        print("卸载：拒绝删除**非本工具写入**的钩子（请手工处理）：%s" % hp)
        return 1
    os.remove(hp)
    print("卸载：已删除 %s" % hp)
    baks = sorted(f for f in os.listdir(os.path.dirname(hp)) if f.startswith(HOOK_NAME + ".bak."))
    if baks:
        src = os.path.join(os.path.dirname(hp), baks[-1])
        shutil.copy2(src, hp)
        os.chmod(hp, 0o755)
        print("卸载：已还原备份 %s ⇒ %s" % (baks[-1], HOOK_NAME))
    else:
        print("卸载：无备份可还原（此前无既有钩子）")
    return 0


def do_install(top):
    hp = hook_path(top)
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    if os.path.exists(hp):
        with open(hp, "r", encoding="utf-8", errors="replace") as fh:
            old = fh.read()
        if MARKER in old:
            print("安装：已存在本工具钩子 ⇒ 覆盖更新（幂等）")
        else:
            bak = hp + ".bak." + time.strftime("%Y%m%d_%H%M%S")
            shutil.copy2(hp, bak)
            print("安装：既有钩子已备份 ⇒ %s" % os.path.basename(bak))
    body = build_hook(top)
    with open(hp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    try:
        os.chmod(hp, 0o755)
    except Exception:                                            # noqa: BLE001
        pass
    print("安装：已写入 %s（%d 字节）" % (hp, len(body.encode("utf-8"))))
    print("行为：本次提交涉及 `02_TUFT_` 路径 ⇒ 强制运行落盘前双检；未通过即阻断提交")
    print("逃生门：`git commit --no-verify`（git 原生）｜演练：`TUFT_HOOK_FORCE=1`")
    return 0


def find_shell():
    """返回可执行钩子的命令前缀（不含钩子路径）。

    优先 `git hook run pre-commit`（Git ≥2.36；由 **git 自带的 shell** 执行 =
    与真实提交时**完全同一条路径**，最可信）；否则回退到 `sh` / git 自带 `sh.exe`。
    """
    rc, _ = git("hook", "run", "--help")
    if rc == 0:
        return ["git", "hook", "run", "pre-commit"]
    for cand in ("sh", "bash",
                 r"C:\Program Files\Git\usr\bin\sh.exe",
                 r"C:\Program Files (x86)\Git\usr\bin\sh.exe"):
        try:
            p = subprocess.run([cand, "-c", "exit 0"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            if p.returncode == 0:
                return [cand]
        except Exception:                                        # noqa: BLE001
            continue
    return None


def do_test(top):
    """端到端演练：临时制造一个**违规**（重号条目）⇒ 期望双检 FAIL ⇒ 钩子阻断 ⇒ 自动清理。"""
    import json
    print("=" * 70)
    print("端到端演练：制造违规 ⇒ 期望「双检 FAIL ⇒ 钩子返回非零（阻断提交）」")
    print("=" * 70)
    hp = hook_path(top)
    if not os.path.exists(hp):
        print("❌ 演练中止：钩子未安装（先运行 python tuft_安装提交钩子.py）")
        return 1
    shell = find_shell()
    if not shell:
        print("❌ 演练中止：未找到可用于执行钩子的 shell（git hook run / sh 均不可用）")
        print("   注：这只影响**本演练**；真实提交时由 git 自带 shell 执行钩子，不受影响。")
        return 1
    print("执行方式：%s%s" % (" ".join(shell), "" if len(shell) > 1 else " " + hp))
    bad = os.path.join(HERE, "_hooktest_CURATED.json")
    docs = {"volume": "钩子演练（临时文件，演练后即删）", "entries": [
        {"entry_id": "CUR-01", "name": "临时重号条目（演练用）", "script_ref": "_hooktest_CURATED.json",
         "script_sha256": "0" * 64, "category": "演练", "status": "❌ 演练用",
         "core_prediction": "-", "observational_bound": "-", "falsification_criterion": "-",
         "cross_ref_volume": "-", "uncertainty": "-"}]}
    rc0 = 0
    try:
        with open(bad, "w", encoding="utf-8") as fh:
            json.dump(docs, fh, ensure_ascii=False, indent=2)
        cmd = shell + ([] if len(shell) > 1 else [hp])
        env = dict(os.environ, TUFT_HOOK_FORCE="1")
        proc = subprocess.run(cmd, cwd=top, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        out = proc.stdout.decode("utf-8", "replace")
        rc0 = proc.returncode
        for l in [x for x in out.splitlines() if x.strip()][-7:]:
            print("   %s" % l)
        print("钩子退出码 = %d" % rc0)
        if rc0 != 0:
            print("✅ 演练通过：违规被**成功阻断**（正是封堵「未登记覆盖/重号」所需的机制）")
        else:
            print("❌ 演练未通过：违规**未被阻断**（钩子未生效，须复核）")
    finally:
        if os.path.exists(bad):
            os.remove(bad)
            print("清理：已删除临时演练文件 `_hooktest_CURATED.json`")
    return 0 if rc0 != 0 else 1


def main():
    args = sys.argv[1:]
    top = repo_root()
    if not top:
        print("❌ 未找到 git 仓库根（须在仓库内运行）")
        return 1
    if "--status" in args:
        return do_status(top)
    if "--uninstall" in args:
        return do_uninstall(top)
    if "--test" in args:
        return do_test(top)
    rc = do_install(top)
    with open(os.path.abspath(__file__), "rb") as fh:
        print("自哈希(SHA256) = %s" % hashlib.sha256(fh.read()).hexdigest())
    print("红线：本工具只做门禁编排，不新增物理主张、不改动 CURATED 真源。")
    return rc


if __name__ == "__main__":
    sys.exit(main())
