# -*- coding: utf-8 -*-
"""r327 链接体检：解析 数据说明件 + 判定册 里的本地相对链接，逐条 stat。
纪律（承 r309/r319/r325 教训）：
  ① 必须报**分母**；分母 0 判 FAIL（「断链 0」在 0 条链接时毫无意义）
  ② 必须有三条负控 + 一条正控，且负控方向不能写反（负控「通过」的语义是**必须报断**）
  ③ 控制组不读 run() 的返回值来做负控判断，直接判 (total > 0 and len(broken) == 1)
"""
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(ROOT, "scratch")

STEM = ("TUFT-r327_指标映射的二项式闭式与跳过3定理_"
        "为什么只有n等于1和2能给出三代_精算与可视化_2026-11-01")
TARGETS = [
    os.path.join(ROOT, "数据", STEM + ".md"),
    os.path.join(ROOT, "判定", "判定_" + STEM + ".md"),
]

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def collect(path):
    """返回 [(行号, 原始目标, 规范化目标)]；只取本地链接。"""
    if not os.path.exists(path):
        return None
    base = os.path.dirname(path)
    out = []
    for ln, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        for m in LINK.finditer(line):
            raw = m.group(1).strip()
            if raw.startswith("http://") or raw.startswith("https://") or raw.startswith("mailto:"):
                continue
            if raw.startswith("#"):
                continue
            tgt = raw.split("#")[0]
            if not tgt:
                continue
            out.append((ln, raw, os.path.normpath(os.path.join(base, tgt))))
    return out


def run(paths):
    total, broken = 0, []
    for p in paths:
        items = collect(p)
        if items is None:
            broken.append((p, "文件缺失", "(self)"))
            continue
        for ln, raw, tgt in items:
            total += 1
            if not os.path.exists(tgt):
                broken.append((os.path.basename(p), ln, raw))
    ok = (total > 0) and (len(broken) == 0)
    return total, broken, ok


def show(tag, total, broken, ok):
    print("[%s] 链接 %d 条 / 断 %d 条 / %s" % (tag, total, len(broken), "OK" if ok else "FAIL"))
    for b in broken[:10]:
        print("     ! %s" % (b,))


# ---------------------------------------------------------------- 正式体检
print("=== 正式：数据说明件 + 判定册 ===")
t0, b0, ok0 = run(TARGETS)
show("MAIN", t0, b0, ok0)
if t0 == 0:
    print("LINK-FAIL：分母为 0（本卷没有任何本地链接可检 ⇒ 体检形同空转）")
    sys.exit(2)
if b0:
    print("LINK-FAIL：存在断链")
    sys.exit(1)

# ---------------------------------------------------------------- 控制组
if not os.path.exists(SCRATCH):
    os.makedirs(SCRATCH, exist_ok=True)

CTL = []

# 负控 ①：把一个真目标改成一个不存在的名字 ⇒ 必须精确报 1 条断链
# ★副本必须放回**原目录**：放到 scratch/ 会改变相对链接的基准目录，于是全部链接连带断掉，
#   那条「断 1 条」的断言就变成「断 4 条」—— 负控自己先坏了（本脚本首跑即踩中）。
neg1 = os.path.join(ROOT, "数据", "_neg_r327_links_1.md")
s = io.open(TARGETS[0], encoding="utf-8").read()
bad = s.replace("TUFT-r325_通量量子数与稳定性的联立", "TUFT-r325_不存在的卷名", 1)
assert bad != s
io.open(neg1, "w", encoding="utf-8", newline="\n").write(bad)
n1_tot, n1_brk, _ = run([neg1])
n1_ok = (n1_tot > 0) and (len(n1_brk) == 1)
CTL.append(("负控① 注入 1 个假目标 ⇒ 必须报断 1 条", n1_ok,
            "链接 %d 条 / 断 %d 条" % (n1_tot, len(n1_brk))))
show("NEG1", n1_tot, n1_brk, n1_ok)

# 负控 ②：全部换成外链 ⇒ 本地链接 0 条 ⇒ 必须触发「分母 0 即 FAIL」
neg2 = os.path.join(SCRATCH, "_neg_r327_links_2.md")
only_ext = "[外部](https://example.com/a) 与 [外部2](https://example.com/b)\n"
io.open(neg2, "w", encoding="utf-8", newline="\n").write(only_ext)
n2_tot, n2_brk, n2_ok = run([neg2])
ctl2_ok = (n2_tot == 0) and (n2_ok is False)
CTL.append(("负控② 全外链 ⇒ 分母 0 ⇒ 必须判 FAIL（不能空转报绿）", ctl2_ok,
            "链接 %d 条 / 断 %d 条 / run_ok=%s" % (n2_tot, len(n2_brk), n2_ok)))
show("NEG2", n2_tot, n2_brk, n2_ok)

# 负控 ③：删掉一个目标文件（数据说明件本身）⇒ 必须报「文件缺失」
tmp3 = os.path.join(SCRATCH, "_neg_r327_links_3.md")
io.open(tmp3, "w", encoding="utf-8", newline="\n").write("占位\n")
n3_tot, n3_brk, n3_ok = run([os.path.join(SCRATCH, "不存在的说明件.md")])
ctl3_ok = (len(n3_brk) == 1) and (n3_brk[0][1] == "文件缺失")
CTL.append(("负控③ 目标文件缺失 ⇒ 必须报「文件缺失」而不是静默跳过", ctl3_ok,
            "断 %d 条：%s" % (len(n3_brk), n3_brk[:1])))

# 正控：外链 + 一条真本地链接 ⇒ 分母 1、断 0、必须判 PASS
pos = os.path.join(SCRATCH, "_pos_r327_links.md")
rel = os.path.relpath(os.path.join(ROOT, "数据", STEM + ".md"), SCRATCH).replace("\\", "/")
io.open(pos, "w", encoding="utf-8", newline="\n").write(
    "[外部](https://example.com/x)\n[本地](%s)\n" % rel)
p_tot, p_brk, p_ok = run([pos])
ctl4_ok = (p_tot == 1) and (len(p_brk) == 0) and p_ok
CTL.append(("正控 外链 + 1 条真本地链接 ⇒ 分母 1 / 断 0 / 判 PASS", ctl4_ok,
            "链接 %d 条 / 断 %d 条" % (p_tot, len(p_brk))))

# ---------------------------------------------------------------- 汇总
print("\n=== 控制组 ===")
npass = 0
for desc, ok, det in CTL:
    print("  %s  %s  ; %s" % ("PASS" if ok else "FAIL", desc, det))
    npass += 1 if ok else 0
print("controls = %d/%d" % (npass, len(CTL)))

if npass != len(CTL):
    print("\nLINK-CTL-FAIL")
    sys.exit(3)

print("\nLINK-OK  links=%d  broken=0  controls=%d/%d  rc=0" % (t0, npass, len(CTL)))
