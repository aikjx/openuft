# -*- coding: utf-8 -*-
"""
ASCII 路径 runner：驱动含中文路径的攻破⑰引擎。
中文路径以 UTF-8 写在本源码内，不经 bash/PowerShell argv（避免 GBK 误码）。
stdout 落报告文件，边跑边 flush（块缓冲在 SIGTERM 时会整段丢失）。
"""
import os
import sys
import subprocess

PY = r"C:/Users/mo/.workbuddy/binaries/python/versions/3.13.12/python.exe"

TARGET = (
    r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
    r"\剩余5体系公设层深攻_S05S06S11S04S01_2026-10-10.py"
)

REPORT = (
    r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
    r"\_攻破17_运行报告.txt"
)


def main():
    print("TARGET exists:", os.path.exists(TARGET), flush=True)
    if not os.path.exists(TARGET):
        print("!! target not found", flush=True)
        return 2

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    proc = subprocess.run(
        [PY, TARGET],
        capture_output=True,
        env=env,
        cwd=os.path.dirname(TARGET),
    )
    out = proc.stdout.decode("utf-8", errors="replace")
    err = proc.stderr.decode("utf-8", errors="replace")

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("EXIT CODE = %d\n\n" % proc.returncode)
        f.write("---- STDOUT ----\n")
        f.write(out)
        f.write("\n---- STDERR ----\n")
        f.write(err)

    print("EXIT CODE =", proc.returncode, flush=True)
    print(out, flush=True)
    if err.strip():
        print("---- STDERR ----", flush=True)
        print(err, flush=True)
    print("REPORT ->", REPORT, flush=True)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
