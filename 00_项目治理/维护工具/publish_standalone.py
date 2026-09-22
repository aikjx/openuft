# -*- coding: utf-8 -*-
"""把本目录镜像为独立发布仓库的根，先校验再推送。仅用标准库。

为什么需要这个脚本（背景，务必先读）
------------------------------------
本项目的 git 根目录是 **上层工作区**（my_lib），`openuft/` 只是它下面的一个子目录。
但 GitHub 上的独立仓库 github.com/aikjx/openuft.git 需要让 `openuft/` 的**内容**
位于仓库**根**（这样 `README.md`、`verify.py` 就是仓库首页与首页命令）。

于是存在两套布局：

- **主仓库布局**：<工作区根>/openuft/00_项目治理/...
- **发布仓库布局**：<仓库根>/00_项目治理/...（openuft 这层被去掉）

本脚本负责在两者之间做"子树去前缀镜像"，并要求**在干净副本内**跑 verify.py。

为什么必须在干净副本内校验
--------------------------
主工作区里可能有：未提交的新文件、被 `.gitignore` 排除的文件、以及本地残留的空目录。
这些东西在主工作区**存在**，在 `git clone` 出来的仓库里**不存在**。
历史上本项目就因此出过两次"克隆后 verify.py 直接崩/FAIL"的问题：
被 `*.zip` 规则误排除的迁移快照、以及 git 无法表达的空目录。
所以：只信干净副本的结果。

设计取舍
--------
- 用 `git worktree` + `git read-tree`，**不改动主工作区**，也**不重写任何历史**；
  正常情况推送是 fast-forward，不会丢失远端任何提交。
- 发布分支名为 `openuft-standalone`，内容是"仓库根即 openuft"；
  推送到远端时映射为 `main`（可用 --remote-branch 改）。
- 不使用 force push。若预演显示非 fast-forward，脚本会停下并要求人工确认。

用法
----
    # 1) 只做镜像 + 干净副本校验（安全，不动远端）
    python -B 00_项目治理/维护工具/publish_standalone.py

    # 2) 校验通过后再推送
    python -B 00_项目治理/维护工具/publish_standalone.py --push

    # 3) 从发布仓库（已克隆的 GitHub 版）里运行：只校验，不做镜像
    python -B 00_项目治理/维护工具/publish_standalone.py --verify-only
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# [UTF8-GUARD v1]
import sys as _sys_utf8
try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve()
LAYER = HERE.parents[2]                 # 本目录（00_项目治理 的上一级）
DEFAULT_BRANCH = 'openuft-standalone'
DEFAULT_REMOTE = 'openuft'
DEFAULT_REMOTE_BRANCH = 'main'

# 凭据：显式绕过helper-selector，只读 ~/.git-credentials（store）
#
# 本机 PortableGit 的系统 gitconfig 把 credential.helper 设成 WorkBuddy 自带的
# helper-selector，而 ~/.gitconfig 只给 codeup.aliyun.com / gitee.com / gitcode.com
# 配了 provider，**github.com 没配**。命中未配置的 host 时该选择器会尝试交互式取凭据，
# 在无终端环境下表现为永久阻塞：`git push` 卡 20+ 分钟无输出，最终 401；手工执行
# `git credential fill` 同样挂住不返回。
#
# `-c credential.helper=` 先清空 helper 列表，再用第二个 -c 只装上 store，
# 等价于命令行版 `git -c credential.helper= -c credential.helper=store push ...`。
# 同一内容用 store 直推实测 6 秒完成（be529536..b4f062ad）。
#
# 若你的凭据不放在 ~/.git-credentials、而依赖 manager/交互式助手，
# 设 OPENUFT_GIT_CRED=default 可关闭本覆盖。
CRED_ARGS: list[str] = [] if os.environ.get('OPENUFT_GIT_CRED') == 'default' else [
    '-c', 'credential.helper=', '-c', 'credential.helper=store',
    '-c', 'http.postBuffer=524288000',
]


def git(*args: str, cwd: Path, check: bool = True, merge: bool = False) -> str:
    """运行 git 并返回输出。

    merge=True 时把 stderr 也并入返回值：**`git push` 的状态行（含 fast-forward
    箭头与 rejected 提示）是写到 stderr 的**，只取 stdout 会把"需要推送"
    误判成"远端已是最新"。凡解析 push 结果必须用 merge=True。
    """
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    proc = subprocess.run(['git', *CRED_ARGS, *args], cwd=str(cwd), env=env,
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and proc.returncode != 0:
        raise SystemExit('git {} 失败：\n{}'.format(' '.join(args), (proc.stderr or '').strip()))
    out = proc.stdout or ''
    if merge:
        out += proc.stderr or ''
    return out.strip()


def run_python(script: Path, cwd: Path) -> tuple[int, str]:
    proc = subprocess.run([sys.executable, '-B', str(script)], cwd=str(cwd),
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    return proc.returncode, ((proc.stdout or '') + (proc.stderr or '')).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description='镜像 openuft 为独立发布仓库的根，校验后推送')
    parser.add_argument('--push', action='store_true', help='校验通过后执行推送')
    parser.add_argument('--verify-only', action='store_true', help='只校验当前目录，不做镜像')
    parser.add_argument('--branch', default=DEFAULT_BRANCH, help='发布分支名')
    parser.add_argument('--remote', default=DEFAULT_REMOTE, help='远端名')
    parser.add_argument('--remote-branch', default=DEFAULT_REMOTE_BRANCH, help='远端目标分支')
    parser.add_argument('--worktree', default=None, help='干净副本路径（默认：工作区同级的 _openuft_publish，会复用）')
    args = parser.parse_args()

    verify = LAYER / 'verify.py'
    if not verify.exists():
        raise SystemExit('未找到 {}：请在 openuft 目录内运行本脚本'.format(verify))

    if args.verify_only:
        code, out = run_python(verify, LAYER)
        print(out)
        print('\n[verify-only] 结果：{}'.format('PASS' if code == 0 else 'FAIL'))
        return code

    # ---- 判断当前布局 ----
    try:
        toplevel = Path(git('rev-parse', '--show-toplevel', cwd=LAYER))
    except SystemExit:
        raise SystemExit('当前目录不在 git 仓库中')

    if toplevel == LAYER:
        print('检测到**发布仓库布局**（仓库根即 openuft）。\n'
              '此布局下没有可镜像的子树；请在主工作区运行本脚本，或改用 --verify-only 校验。')
        code, out = run_python(verify, LAYER)
        print(out)
        return code

    prefix = LAYER.relative_to(toplevel).as_posix()
    print('主仓库布局：git 根 = {}，子树前缀 = {}/'.format(toplevel, prefix))

    # ---- 主工作区状态提示（不阻断，但要说清） ----
    dirty = git('status', '--porcelain', cwd=toplevel)
    if dirty:
        n = len([l for l in dirty.splitlines() if l.strip()])
        print('提醒：主工作区有 {} 处未提交改动。本脚本只镜像**已提交**内容，'
              '未提交内容不会进入发布仓库。'.format(n))

    tree = git('rev-parse', 'HEAD:{}'.format(prefix), cwd=toplevel)
    print('子树的 tree 对象 = {}'.format(tree[:12]))

    worktree = Path(args.worktree) if args.worktree else (toplevel.parent / '_openuft_publish')

    # ---- 准备 worktree ----
    existing = git('worktree', 'list', '--porcelain', cwd=toplevel).splitlines()
    has_branch = bool(git('branch', '--list', args.branch, cwd=toplevel))

    if worktree.exists() and any(l.startswith('worktree ' + worktree.as_posix()) for l in existing):
        print('复用已存在的干净副本：{}'.format(worktree))
    else:
        if worktree.exists():
            print('清理残留目录：{}'.format(worktree))
            shutil.rmtree(worktree, ignore_errors=True)
        if has_branch:
            out = git('worktree', 'add', str(worktree), args.branch, cwd=toplevel)
        else:
            out = git('worktree', 'add', '--orphan', '-b', args.branch, str(worktree), cwd=toplevel)
        print('已创建干净副本：{}'.format(worktree))

    # ---- 镜像：把子树内容放到副本根 ----
    git('read-tree', '--reset', '-u', tree, cwd=worktree)
    changed = [l for l in git('status', '--short', cwd=worktree).splitlines() if l.strip()]
    print('镜像后变更条目：{}'.format(len(changed)))

    # ---- 在干净副本内校验（关键一步） ----
    code, out = run_python(worktree / 'verify.py', worktree)
    print('\n---- 干净副本 verify.py ----')
    print(out)
    if code != 0:
        print('\n校验未通过，**已中止**，远端未被改动。请修复导致失败的内容后重跑。')
        return code

    if not changed:
        print('\n镜像内容与发布分支一致，无需新提交。')

    # ---- 提交 ----
    if changed:
        git('add', '-A', cwd=worktree)
        subj = 'release: 同步 {} 至仓库根（发布快照）'.format(prefix)
        git('commit', '-q', '-m', subj, cwd=worktree)
        print('已提交：{}'.format(git('log', '-1', '--format=%h %s', cwd=worktree)))

    # ---- 推送预演 / 推送 ----
    refspec = '{}:{}'.format(args.branch, args.remote_branch)
    dry = git('push', '--dry-run', args.remote, refspec, cwd=toplevel, merge=True)
    print('\n---- 推送预演 ----\n{}'.format(dry or '（空：远端已是最新）'))

    if not dry.strip():
        print('\n远端已是最新，无需推送。')
        return 0

    low = dry.lower()
    if 'everything up-to-date' in low:
        print('\n远端已是最新，无需推送。')
        return 0

    ff = ('..' in dry) and ('+' not in dry) and ('rejected' not in low) and ('non-fast-forward' not in low)

    if not args.push:
        print('\n预演结束（未推送）。确认无误后加 --push 执行。')
        return 0

    if not ff:
        print('\n**预演显示不是 fast-forward**（可能需要处理无关历史或强推）。'
              '本脚本拒绝自动强推，请人工判断后再操作。')
        return 2

    print('\n---- 实际推送 ----')
    print(git('push', args.remote, refspec, cwd=toplevel, merge=True))
    print('已完成。远端 {} refs/heads/{} 应为：{}'.format(
        args.remote, args.remote_branch, git('rev-parse', 'HEAD', cwd=worktree)[:12]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
