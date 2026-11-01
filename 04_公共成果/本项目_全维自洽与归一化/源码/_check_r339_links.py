# -*- coding: utf-8 -*-
"""r339 链接体检：解析 数据说明件 + 判定册 + README 中 r339 相关行 的本地相对链接，逐条 stat。

纪律（承 r309/r319/r325/r327/r331/r335 教训）：
  ① 必须报**分母**；分母 0 判 FAIL（「断链 0」在 0 条链接时毫无意义）
  ② 三条负控 + 一条正控，且负控方向不能写反（负控「通过」的语义是**必须报断**）
  ③ 负控①的副本必须放回**原目录**（放 scratch/ 会改相对基准，一次断多条 ⇒ 负控自己先坏）
  ④ 本卷新增：**围栏代码块内的 `[...](...)` 不是链接**（渲染器不链接化）
     ——首跑时 `d·[h^n]( e^{kh} td(T_X) )` 被当成 1 条断链，是**校验器的错**不是文件的错。
     处置：校验器按渲染语义跳过 ``` 围栏；同时把该数学式改写为 ⟨h^n, …⟩ 消歧（双保险，且后者
     让源码级 grep 也不会误判）。
  ⑤ README 只检 **含 r339 的行**（本卷登记的 8 条），不检历史他卷链接（不代修他人缺口）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(ROOT, "scratch")

STEM = ("TUFT-r339_秩一超曲面上整性从不排除整数通量_Newton系数全整定理与Z加半整数是坐标假象_"
        "精算与可视化_2026-11-01")
TARGETS = [
    os.path.join(ROOT, "数据", STEM + ".md"),
    os.path.join(ROOT, "判定", "判定_" + STEM + ".md"),
]
README = os.path.join(ROOT, "README.md")

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def _strip_fences(text):
    """把围栏代码块内容抹成空行（保留行号），返回行列表。"""
    out, inside = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return out


def _strip_inline(line):
    """抹掉行内代码 span（`...`），换成等长空格（保持列不影响，只需行号）。
    渲染器同样不把行内代码当链接；本卷补钉为说明负控写了 `[...](...)` 字面量，
    不剥离就会自伤成 2 条断链（这是校验器的第二处自伤，已登记为纪律④的补充）。"""
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)


def collect(path, only=None):
    """返回 [(行号, 原始目标, 规范化目标)]；只取本地链接。only=过滤器(行文本)。"""
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
            if raw.startswith("http://") or raw.startswith("https://") or raw.startswith("mailto:"):
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


# ================================================================ 正式体检
print("=== 正式 ①：数据说明件 + 判定册 ===")
t1, b1, ok1 = run(TARGETS)
show("MAIN", t1, b1, ok1)

print("=== 正式 ②：README 中 r339 相关行 ===")
t2, b2, ok2 = run([README], only=lambda s: "r339" in s)
show("README-r339", t2, b2, ok2)

TOT = t1 + t2
BRK = b1 + b2
if TOT == 0:
    print("LINK-FAIL：分母为 0（本卷没有任何本地链接可检 ⇒ 体检形同空转）")
    sys.exit(2)
if BRK:
    print("LINK-FAIL：存在断链 %d 条" % len(BRK))
    sys.exit(1)

# ================================================================ 控制组
if not os.path.exists(SCRATCH):
    os.makedirs(SCRATCH, exist_ok=True)

CTL = []

# 负控 ①：把一个真目标改成不存在的名字 ⇒ 必须精确报 1 条断链（副本放回 判定/ 原目录）
neg1 = os.path.join(ROOT, "判定", "_neg_r339_links_1.md")
src1 = TARGETS[1]
s = io.open(src1, encoding="utf-8").read()
FAKE_OLD = "../四力统一方程_秩一超曲面整性_r339可视化_2026-11-01.html"
FAKE_NEW = "../四力统一方程_不存在的卷_neg_r339.html"
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
neg2 = os.path.join(SCRATCH, "_neg_r339_links_2.md")
io.open(neg2, "w", encoding="utf-8", newline="\n").write(
    "[外部](https://example.com/a) 与 [外部2](https://example.com/b)\n")
n2_tot, n2_brk, n2_ok = run([neg2])
ctl2_ok = (n2_tot == 0) and (n2_ok is False)
CTL.append(("负控② 全外链 ⇒ 分母 0 ⇒ 必须判 FAIL（不能空转报绿）", ctl2_ok,
            "链接 %d 条 / 断 %d 条 / run_ok=%s" % (n2_tot, len(n2_brk), n2_ok)))
show("NEG2", n2_tot, n2_brk, n2_ok)

# 负控 ③：目标文件缺失 ⇒ 必须报「文件缺失」而不是静默跳过
n3_tot, n3_brk, n3_ok = run([os.path.join(SCRATCH, "不存在的说明件.md")])
ctl3_ok = (len(n3_brk) == 1) and (n3_brk[0][1] == "文件缺失")
CTL.append(("负控③ 目标文件缺失 ⇒ 必须报「文件缺失」而不是静默跳过", ctl3_ok,
            "断 %d 条：%s" % (len(n3_brk), n3_brk[:1])))
show("NEG3", n3_tot, n3_brk, n3_ok)

# 负控 ④（本卷新增）：围栏代码块里的 `[...](...)` 必须**不**被当链接
neg4 = os.path.join(SCRATCH, "_neg_r339_links_4.md")
io.open(neg4, "w", encoding="utf-8", newline="\n").write(
    "```\nχ = d · [h^n]( e^{kh} td(T_X) )\n```\n"
    "[真](https://example.com/x)\n")
n4_tot, n4_brk, _ = run([neg4])
ctl4_ok = (n4_tot == 0)  # 围栏内 0 条 + 外链 0 条 ⇒ 分母 0（被跳过，不误报断链）
CTL.append(("负控④ 围栏代码块内 `[...](...)` 必须不算链接（分母 0）", ctl4_ok,
            "链接 %d 条 / 断 %d 条" % (n4_tot, len(n4_brk))))
show("NEG4", n4_tot, n4_brk, n4_tot > 0)

# 负控 ④b：同一段文字**移出**围栏后必须变回 1 条（否则负控④ 可能只是正则失效）
neg4b = os.path.join(SCRATCH, "_neg_r339_links_4b.md")
io.open(neg4b, "w", encoding="utf-8", newline="\n").write(
    "χ = d · [h^n]( e^{kh} td(T_X) )\n")
n4b_tot, _, _ = run([neg4b])
ctl4b_ok = (n4b_tot == 1)
CTL.append(("负控④b 同一段移出围栏 ⇒ 必须变回 1 条（证明④ 不是正则失效）", ctl4b_ok,
            "链接 %d 条" % n4b_tot))

# 负控 ⑤：行内代码 span 里的 `[...](...)` 不算链接（补钉自伤处）
neg5 = os.path.join(SCRATCH, "_neg_r339_links_5.md")
io.open(neg5, "w", encoding="utf-8", newline="\n").write(
    "说明：负控④/④b 用 `[...](...)` 举例，另见 [真外链](https://example.com/x)\n")
n5_tot, n5_brk, _ = run([neg5])
ctl5_ok = (n5_tot == 0)
CTL.append(("负控⑤ 行内代码内 `[...](...)` 不算链接（分母 0）", ctl5_ok,
            "链接 %d 条 / 断 %d 条" % (n5_tot, len(n5_brk))))

# 负控 ⑤b：同一字面量移出行内代码 ⇒ 必须变回 1 条
neg5b = os.path.join(SCRATCH, "_neg_r339_links_5b.md")
io.open(neg5b, "w", encoding="utf-8", newline="\n").write(
    "说明：负控用 [文字](目标.md) 举例\n")
n5b_tot, _, _ = run([neg5b])
ctl5b_ok = (n5b_tot == 1)
CTL.append(("负控⑤b 同一字面量移出行内代码 ⇒ 必须变回 1 条", ctl5b_ok,
            "链接 %d 条" % n5b_tot))

# 正控：外链 + 一条真本地链接 ⇒ 分母 1、断 0、必须判 PASS
pos = os.path.join(SCRATCH, "_pos_r339_links.md")
rel = os.path.relpath(os.path.join(ROOT, "判定", "判定_" + STEM + ".md"), SCRATCH).replace("\\", "/")
io.open(pos, "w", encoding="utf-8", newline="\n").write(
    "[外部](https://example.com/x)\n[本地](%s)\n" % rel)
p_tot, p_brk, p_ok = run([pos])
ctrl5_ok = (p_tot == 1) and (len(p_brk) == 0) and p_ok
CTL.append(("正控 外链 + 1 条真本地链接 ⇒ 分母 1 / 断 0 / 判 PASS", ctrl5_ok,
            "链接 %d 条 / 断 %d 条" % (p_tot, len(p_brk))))
show("POS", p_tot, p_brk, p_ok)

# ================================================================ 清理临时副本
for tmp in (neg1, neg2, neg4, neg4b, neg5, neg5b, pos):
    if os.path.exists(tmp):
        os.remove(tmp)
        print("cleanup %s" % os.path.basename(tmp))

# ================================================================ 汇总
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
