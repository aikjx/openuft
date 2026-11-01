# -*- coding: utf-8 -*-
"""r325 链接体检。
纪律（r309/r319 教训）：
  - 必须报**分母**；分母为 0 直接判 FAIL（「断链 0」在分母 0 时毫无意义）
  - 三负控：①注入假目标须报断 ②仅真目标须 0 断 ③空目标集须触发「0 条即 FAIL」分支
  - 一正控：只放外链（本地 0 条）同样须触发该分支
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = ("TUFT-r325_通量量子数与稳定性的联立_"
        "Q是否为自由参数与三代选定的第一原理审计_精算与可视化_2026-11-01")

TARGETS = [
    os.path.join(ROOT, "数据", STEM + ".md"),
    os.path.join(ROOT, "判定", "判定_" + STEM + ".md"),
]

LINK_PAT = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def local_links(text):
    out = []
    for m in LINK_PAT.finditer(text):
        t = m.group(1).strip()
        if t.startswith("#") or t.startswith("http://") or t.startswith("https://") or t.startswith("mailto:"):
            continue
        out.append(t.split("#")[0])
    return out


def audit(pairs):
    """pairs = [(base_dir, rel_target)] -> (total, broken, detail)"""
    total, broken, detail = 0, [], []
    for base, rel in pairs:
        total += 1
        full = os.path.normpath(os.path.join(base, rel))
        if not os.path.exists(full):
            broken.append(rel)
            detail.append(("BROKEN", rel))
        else:
            detail.append(("OK", rel))
    return total, broken, detail


def run(name, pairs, expect_total_zero_fail=True):
    total, broken, detail = audit(pairs)
    if total == 0 and expect_total_zero_fail:
        print("  %-14s total=0  ⇒ FAIL（分母为 0，断链 0 无意义）" % name)
        return False
    ok = (len(broken) == 0)
    print("  %-14s total=%-3d broken=%-2d %s" % (name, total, len(broken), "OK" if ok else "FAIL"))
    for st, rel in detail:
        if st == "BROKEN":
            print("       ! %s" % rel)
    return ok


print("=" * 72)
print("TUFT-r325 链接体检")
print("=" * 72)

# ---------------- 正式体检
pairs = []
for p in TARGETS:
    if not os.path.exists(p):
        print("MISSING TARGET FILE: %s" % os.path.basename(p))
        sys.exit(2)
    txt = io.open(p, encoding="utf-8").read()
    base = os.path.dirname(p)
    got = local_links(txt)
    print("  %-42s 本地链接 %d 条" % (os.path.basename(p)[:42], len(got)))
    for rel in got:
        pairs.append((base, rel))

print("")
print("[正式体检]")
ok_main = run("r325 产物链接", pairs)

# ---------------- 负控 ①：注入假目标
# 注意方向：负控「通过」= **必须报断**，所以不能用 run() 的返回值（run 只在 0 断时 True）
print("")
print("[负控 ①：注入一个假目标 —— 必须报断]")
fake = pairs + [(ROOT, "__definitely_missing_r325_target__.md")]
n1_total, n1_broken, _ = audit(fake)
run("注入假目标", fake)          # 打印用，故意返回 False
ok_n1 = (n1_total > 0 and len(n1_broken) == 1)

# ---------------- 负控 ②：仅真目标 —— 必须 0 断
print("")
print("[负控 ②：只给真目标 —— 必须 0 断]")
real = [(ROOT, "数据/" + STEM + ".md"), (ROOT, "判定/判定_" + STEM + ".md")]
ok_n2 = run("仅真目标", real)

# ---------------- 负控 ③：空目标集 —— 必须触发「0 条即 FAIL」
print("")
print("[负控 ③：空目标集 —— 必须触发 0 条即 FAIL 分支]")
ok_n3 = (run("空目标集", []) is False)

# ---------------- 正控：只放外链 ⇒ 本地 0 条 —— 同样必须触发
print("")
print("[正控：只放外链 —— 本地 0 条，仍须触发同一分支]")
ext_text = "[a](https://example.com/x) [b](http://example.org/y) [c](mailto:x@y.z)"
n_ext = len(local_links(ext_text))
ok_p1 = (n_ext == 0) and (run("只放外链", []) is False)
print("       外链样本解析出本地链接 = %d（应为 0）" % n_ext)

print("")
print("[控制组] ①注入假目标报断=%s ②仅真目0断=%s ③空集FAIL=%s 正控外链=%s"
      % (ok_n1, ok_n2, ok_n3, ok_p1))
ctls = [ok_n1, ok_n2, ok_n3, ok_p1]
print("[控制组] %d/4" % sum(1 for c in ctls if c))

# 负控①必须真的报出断链，否则是恒绿
hard_n1 = ok_n1
print("[硬判] 负控① 分母>0 且恰报 1 条断链 = %s（total=%d broken=%d）"
      % (hard_n1, n1_total, len(n1_broken)))

ok_all = ok_main and all(ctls) and hard_n1 and (n1_total == len(pairs) + 1)
print("")
if ok_all:
    print("LINK-OK  rc=0   （本地链接 %d 条，断链 0，分母非零）" % len(pairs))
    sys.exit(0)
print("LINK-FAIL")
sys.exit(1)
