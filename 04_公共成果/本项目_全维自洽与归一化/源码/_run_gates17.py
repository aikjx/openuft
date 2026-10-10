# -*- coding: utf-8 -*-
"""
ASCII 路径 runner：依次跑 refresh_catalog.py / verify.py / 册级一致性守卫。
中文路径以 UTF-8 写在本源码内，不经 bash argv。
"""
import os
import sys
import subprocess

PY = r"C:/Users/mo/.workbuddy/binaries/python/versions/3.13.12/python.exe"

BASE = r"D:\a10\aikjx\code\my_lib\openuft"

TARGETS = [
    ("refresh_catalog", os.path.join(BASE, "00_项目治理", "维护工具", "refresh_catalog.py")),
    ("verify", os.path.join(BASE, "verify.py")),
    ("guard", os.path.join(
        BASE, "04_公共成果", "本项目_全维自洽与归一化", "源码",
        "册级一致性与读数漂移_守卫工具_2026-10-05.py")),
]

REPORT = os.path.join(
    r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码",
    "_攻破17_门禁报告.txt")


def run(name, path):
    if not os.path.exists(path):
        return name, None, "NOT FOUND", ""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    p = subprocess.run([PY, path], capture_output=True, env=env,
                       cwd=os.path.dirname(path), timeout=600)
    return (name, p.returncode,
            p.stdout.decode("utf-8", errors="replace"),
            p.stderr.decode("utf-8", errors="replace"))


def main():
    chunks = []
    allok = True
    for name, path in TARGETS:
        n, rc, out, err = run(name, path)
        print("=" * 70, flush=True)
        print(f"[{n}] rc={rc}", flush=True)
        print(out[-6000:], flush=True)
        if err.strip():
            print("---- STDERR ----", flush=True)
            print(err[-3000:], flush=True)
        chunks.append(f"===== {n} ===== rc={rc}\n{out}\n---- stderr ----\n{err}\n")
        if rc != 0:
            allok = False

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(chunks))
    print("REPORT ->", REPORT, flush=True)
    print("ALL RC==0:", allok, flush=True)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
