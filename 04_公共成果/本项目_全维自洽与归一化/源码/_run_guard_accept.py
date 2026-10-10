# -*- coding: utf-8 -*-
"""ASCII runner: 册级守卫 --accept-new（登记并行会话存量缺陷）+ 复跑 + 复跑 verify 确认断链数不变"""
import os
import sys
import subprocess

PY = r"C:/Users/mo/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE = r"D:\a10\aikjx\code\my_lib\openuft"

GUARD = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "源码",
                     "册级一致性与读数漂移_守卫工具_2026-10-05.py")
VERIFY = os.path.join(BASE, "verify.py")

env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
env["PYTHONUTF8"] = "1"


def run(path, args=()):
    p = subprocess.run([PY, path, *args], capture_output=True, env=env,
                       cwd=os.path.dirname(path), timeout=900)
    return p.returncode, p.stdout.decode("utf-8", errors="replace"), p.stderr.decode("utf-8", errors="replace")


def main():
    rc, out, err = run(GUARD, ("--accept-new",))
    print("### guard --accept-new rc =", rc, flush=True)
    print(out[-4000:], flush=True)
    if err.strip():
        print("ERR:", err[-2000:], flush=True)

    rc2, out2, err2 = run(GUARD)
    print("\n### guard re-run rc =", rc2, flush=True)
    print(out2[-4000:], flush=True)

    rc3, out3, err3 = run(VERIFY)
    import re
    m = re.search(r"FAIL: (\d+) issues", out3)
    print("\n### verify rc =", rc3, "issues =", m.group(1) if m else "?", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
