# -*- coding: utf-8 -*-
"""r346 链接体检：解析 数据说明件 + 判定册 + README 中 r346 相关行 的本地相对链接，逐条 stat。

纪律（承 r309/r319/r325/r327/r331/r335/r339 教训）：
  ① 必须报**分母**；分母 0 判 FAIL（「断链 0」在 0 条链接时毫无意义）
  ② 三条负控 + 一条正控，且负控方向不能写反（负控「通过」的语义是**必须报断**）
  ③ 负控①的副本必须放回**原目录**（放 scratch/ 会改相对基准，一次断多条 ⇒ 负控自己先坏）
  ④ 围栏代码块内的 `[...](...)` 不是链接（渲染器不链接化）——r339 首跑自伤两次
  ⑤ 行内代码 span 内的 `[...](...)` 也不是链接——r339 补钉时第二次自伤
  ⑥ README 只检 **含 r346 的行**（不代修他人缺口）
  ⑦ 本卷新情况：README 现行两棵树位于**未闭合**的 ```text 围栏内（并行会话 23:14:59 重写所致），
     树行为纯文本不含链接 ⇒ README 分母如实报 **0**。为免该项变成「静默空转」，
     加一条 **正控「README 行」**证明过滤器有效（同一行带上真链接 ⇒ 必须检出 1 条、断 0）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(ROOT, "scratch")

STEM = ("TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
        "分母整除首项定理与判词下调_精算与可视化_2026-11-01")
HTML = "四力统一方程_整数Newton系数_r346可视化_2026-11-01.html"
TARGETS = [
    os.path.join(ROOT, "数据", STEM + ".md"),
    os.path.join(ROOT, "判定", "判定_" + STEM + ".md"),
]
README = os.path.join(ROOT, "README.md")

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def _strip_fences(text):
    out, inside = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return out


def _strip_inline(line):
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)


def collect(path, only=None):
    if not os.path.exists(path):
        return None
    base = os.path.dirname(path)
    lines = _strip_fences(io.open(path, encoding="utf-8").read())
    out = []
    for ln, line in enumerate(lines, 1):
        if only is not None and not only(line):
            continue
        for m in LINK.finditer(_strip_inline(line)):
            raw = m.group(1).strip()
            if raw.startswith(("http://", "https://", "mailto:")):
                continue
            if raw.startswith("#"):
                continue
            tgt = raw.split("#")[0]
            if not tgt:
                continue
            out.append((ln, raw, os.path.normpath(os.path.join(base, tgt))))
    return out


def run(paths, only=None):
    total, broken = 0, []
    for p in paths:
        items = collect(p, only)
        if items is None:
            broken.append((os.path.basename(p), "文件缺失", "(self)"))
            continue
        for ln, raw, tgt in items:
            total += 1
            if not os.path.exists(tgt):
                broken.append((os.path.basename(p)[:42], ln, raw))
    ok = (total > 0) and (len(broken) == 0)
    return total, broken, ok


def show(tag, total, broken, ok):
    print("[%s] 链接 %d 条 / 断 %d 条 / %s" % (tag, total, len(broken), "OK" if ok else "FAIL"))
    for b in broken[:10]:
        print("     ! %s" % (b,))


print("=== 正式 ①：数据说明件 + 判定册 ===")
t1, b1, ok1 = run(TARGETS)
show("MAIN", t1, b1, ok1)

print("=== 正式 ②：README 中 r346 相关行 ===")
t2, b2, ok2 = run([README], only=lambda s: "r346" in s)
show("README-r346", t2, b2, ok2)
print("    （注：README 现行两树在未闭合 ``` 围栏内、树行为纯文本 ⇒ 本项分母如实为 0；"
      "由下方正控「README 行」证明过滤器未失效）")

TOT, BRK = t1 + t2, b1 + b2
if TOT == 0:
    print("LINK-FAIL：分母为 0（本卷没有任何本地链接可检 ⇒ 体检形同空转）")
    sys.exit(2)
if BRK:
    print("LINK-FAIL：存在断链 %d 条" % len(BRK))
    sys.exit(1)

# ================================================================ 控制组
os.makedirs(SCRATCH, exist_ok=True)
CTL = []

# 负控 ①：把一个真目标改成不存在的名字 ⇒ 必须精确报 1 条断链（副本放回 判定/ 原目录）
neg1 = os.path.join(ROOT, "判定", "_neg_r346_links_1.md")
s = io.open(TARGETS[1], encoding="utf-8").read()
FAKE_OLD = "../" + HTML
FAKE_NEW = "../四力统一方程_不存在的卷_neg_r346.html"
assert FAKE_OLD in s, "负控① 的替换锚点没命中"
bad = s.replace(FAKE_OLD, FAKE_NEW, 1)
assert bad != s
io.open(neg1, "w", encoding="utf-8", newline="\n").write(bad)
n1_tot, n1_brk, _ = run([neg1])
n1_ok = (n1_tot > 0) and (len(n1_brk) == 1)
CTL.append(("负控① 注入 1 个假目标 ⇒ 必须报断 1 条（副本在原目录）", n1_ok,
            "链接 %d 条 / 断 %d 条" % (n1_tot, len(n1_brk))))
show("NEG1", n1_tot, n1_brk, n1_ok)

# 负控 ②：全部换成外链 ⇒ 本地链接 0 条 ⇒ 必须触发「分母 0 即 FAIL」
neg2 = os.path.join(SCRATCH, "_neg_r346_links_2.md")
io.open(neg2, "w", encoding="utf-8", newline="\n").write(
    "[外部](https://example.com/a) 与 [外部2](https://example.com/b)\n")
n2_tot, n2_brk, n2_ok = run([neg2])
ctl2_ok = (n2_tot == 0) and (n2_ok is False)
CTL.append(("负控② 全外链 ⇒ 分母 0 ⇒ 必须判 FAIL（不能空转报绿）", ctl2_ok,
            "链接 %d 条 / 断 %d 条 / run_ok=%s" % (n2_tot, len(n2_brk), n2_ok)))
show("NEG2", n2_tot, n2_brk, n2_ok)

# 负控 ③：目标文件缺失 ⇒ 必须报「文件缺失」而不是静默跳过
n3_tot, n3_brk, _ = run([os.path.join(SCRATCH, "不存在的说明件.md")])
ctl3_ok = (len(n3_brk) == 1) and (n3_brk[0][1] == "文件缺失")
CTL.append(("负控③ 目标文件缺失 ⇒ 必须报「文件缺失」而不是静默跳过", ctl3_ok,
            "断 %d 条：%s" % (len(n3_brk), n3_brk[:1])))
show("NEG3", n3_tot, n3_brk, False)

# 负控 ④：围栏代码块里的 `[...](...)` 必须**不**被当链接
neg4 = os.path.join(SCRATCH, "_neg_r346_links_4.md")
io.open(neg4, "w", encoding="utf-8", newline="\n").write(
    "```\nχ = d · [h^n]( e^{kh} td(T_X) )\n```\n[真](https://example.com/x)\n")
n4_tot, n4_brk, _ = run([neg4])
CTL.append(("负控④ 围栏代码块内 `[...](...)` 必须不算链接（分母 0）", n4_tot == 0,
            "链接 %d 条 / 断 %d 条" % (n4_tot, len(n4_brk))))

# 负控 ④b：同一段文字**移出**围栏后必须变回 1 条
neg4b = os.path.join(SCRATCH, "_neg_r346_links_4b.md")
io.open(neg4b, "w", encoding="utf-8", newline="\n").write("χ = d · [h^n]( e^{kh} td(T_X) )\n")
n4b_tot, _, _ = run([neg4b])
CTL.append(("负控④b 同一段移出围栏 ⇒ 必须变回 1 条（证明④ 不是正则失效）", n4b_tot == 1,
            "链接 %d 条" % n4b_tot))

# 负控 ⑤：行内代码 span 里的 `[...](...)` 不算链接
neg5 = os.path.join(SCRATCH, "_neg_r346_links_5.md")
io.open(neg5, "w", encoding="utf-8", newline="\n").write(
    "说明：负控④/④b 用 `[...](...)` 举例，另见 [真外链](https://example.com/x)\n")
n5_tot, n5_brk, _ = run([neg5])
CTL.append(("负控⑤ 行内代码内 `[...](...)` 不算链接（分母 0）", n5_tot == 0,
            "链接 %d 条 / 断 %d 条" % (n5_tot, len(n5_brk))))

# 负控 ⑤b：同一字面量移出行内代码 ⇒ 必须变回 1 条
neg5b = os.path.join(SCRATCH, "_neg_r346_links_5b.md")
io.open(neg5b, "w", encoding="utf-8", newline="\n").write("说明：负控用 [文字](目标.md) 举例\n")
n5b_tot, _, _ = run([neg5b])
CTL.append(("负控⑤b 同一字面量移出行内代码 ⇒ 必须变回 1 条", n5b_tot == 1,
            "链接 %d 条" % n5b_tot))

# 正控 ①：外链 + 一条真本地链接 ⇒ 分母 1、断 0、判 PASS
pos = os.path.join(SCRATCH, "_pos_r346_links.md")
rel = os.path.relpath(TARGETS[1], SCRATCH).replace("\\", "/")
io.open(pos, "w", encoding="utf-8", newline="\n").write(
    "[外部](https://example.com/x)\n[本地](%s)\n" % rel)
p_tot, p_brk, p_ok = run([pos])
CTL.append(("正控① 外链 + 1 条真本地链接 ⇒ 分母 1 / 断 0 / 判 PASS",
            (p_tot == 1) and (len(p_brk) == 0) and p_ok,
            "链接 %d 条 / 断 %d 条" % (p_tot, len(p_brk))))
show("POS1", p_tot, p_brk, p_ok)

# 正控 ②（本卷新增）：README 过滤器有效性 —— 同一行带真链接 ⇒ 必须检出 1 条、断 0
pos2 = os.path.join(SCRATCH, "_pos_r346_links_readme.md")
# 目标刻意取 README.md（不含 r346），否则链接目标本身就会被过滤器命中 ⇒ ②b 失去对照意义
io.open(pos2, "w", encoding="utf-8", newline="\n").write(
    "│   ├── TUFT-r346_某某.py  # 新增（**r346 · 2026-11-01**）：[README](../README.md)\n")
q_tot, q_brk, q_ok = run([pos2], only=lambda s: "r346" in s)
CTL.append(("正控② README 过滤器有效性：含 r346 的行带真链接 ⇒ 检出 1 条 / 断 0",
            (q_tot == 1) and (len(q_brk) == 0) and q_ok,
            "链接 %d 条 / 断 %d 条" % (q_tot, len(q_brk))))
show("POS2", q_tot, q_brk, q_ok)

# 正控 ②b：同一行去掉 r346 ⇒ 必须变回 0 条（证明过滤器不是「全部放行」）
pos2b = os.path.join(SCRATCH, "_pos_r346_links_readme_b.md")
io.open(pos2b, "w", encoding="utf-8", newline="\n").write(
    "│   ├── TUFT-r999_某某.py  # 新增（**r999**）：[README](../README.md)\n")
r_tot, _, _ = run([pos2b], only=lambda s: "r346" in s)
CTL.append(("正控②b 同一行去掉 r346 ⇒ 变回 0 条（证明过滤器不是全放行）", r_tot == 0,
            "链接 %d 条" % r_tot))

# ================================================================ 清理临时副本
for tmp in (neg1, neg2, neg4, neg4b, neg5, neg5b, pos, pos2, pos2b):
    if os.path.exists(tmp):
        os.remove(tmp)
        print("cleanup %s" % os.path.basename(tmp))

print("")
print("=== 控制组 ===")
npass = 0
for desc, ok, det in CTL:
    print("  %s  %s  ; %s" % ("PASS" if ok else "FAIL", desc, det))
    npass += 1 if ok else 0
print("controls = %d/%d" % (npass, len(CTL)))

if npass != len(CTL):
    print("")
    print("LINK-CTL-FAIL")
    sys.exit(3)

print("")
print("LINK-OK  links=%d (md=%d + readme=%d)  broken=0  controls=%d/%d  rc=0"
      % (TOT, t1, t2, npass, len(CTL)))
