# -*- coding: utf-8 -*-
"""r252 补探：mu_e / Lambda_QCD / f 的形式 / 三重涡旋 / 权重候选"""
import re, os, io

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(BASE, "数据", "TUFT-r241_光速螺旋_来料原件_2026-10-30")
F1 = os.path.join(SRC, "基于光速螺旋流形的核心动力学方程组.md")

_ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def depollute(s):
    for ch in _ALPHA:
        s = s.replace("\\(\\boldsymbol{" + ch + "}\\)", ch)
    return re.sub(r"[\r\n]+", "\n", s)

T = depollute(io.open(F1, "r", encoding="utf-8", errors="replace").read())
L = T.split("\n")
print("lines =", len(L))

def show(title, pat, limit=10, win=2):
    hits = [i + 1 for i, s in enumerate(L) if re.search(pat, s)]
    print("\n" + "=" * 78)
    print("## %s  regex=%s  hits=%d  lines=%s" % (title, pat, len(hits), hits[:20]))
    for ln in hits[:limit]:
        print("---- line %d ----" % ln)
        for k in range(max(0, ln - 1 - win), min(len(L), ln + win)):
            print("%s %5d| %s" % (">>" if k == ln - 1 else "  ", k + 1, L[k][:280]))

show("mu_e 定义", r"\\mu_e|\\mu_\{e\}|电子标度|电子质量标度", limit=8)
show("Lambda_QCD（宽）", r"Lambda_\{\\?t?e?x?t?\}?\{?QCD|Lambda_\{?QCD|QCD\}\}?|QCD", limit=6)
show("200 MeV", r"200\s*\\,?\\text\{?M|200\\,|200\s*MeV", limit=8)
show("被积函数 f 的形式", r"f\\\(|f\\left|权重函数|交叉耦合", limit=8)
show("三重 / 缠绕", r"三重|缠绕数|拓扑缠绕|三价|三个夸克|三夸克", limit=8)
show("几何权重候选", r"权重候选|候选", limit=8)
show("误差审计 / 诚实", r"误差审计|诚实|不是.{0,12}第一性|模型构造", limit=10)
show("alpha_s", r"\\alpha_s", limit=6)

# 检查 boxed 主结果那一段的完整上下文
print("\n" + "=" * 78)
print("## boxed 主结果完整段 (line 4226 附近 ±25)")
for k in range(4200, 4250):
    print("%5d| %s" % (k + 1, L[k][:250]))

print("\n" + "=" * 78)
print("## 第三步完整段 (line 4145-4200)")
for k in range(4144, 4200):
    print("%5d| %s" % (k + 1, L[k][:250]))
