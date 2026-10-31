# -*- coding: utf-8 -*-
import io, os, re, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
NAME = ("TUFT-r264_自由参数总账层_ω赋值与单位依赖及四态分类与八粒子字典表自洽崩坏"
        "_精算与可视化_2026-10-31")
m = importlib.import_module(NAME)
book = m.BOOK_TEXT

EXTRA = [("G", "G", "牛顿引力常数"), ("α_s", "alpha_s", "强耦合常数"),
         ("g_W", "g_W", "弱耦合常数"), ("σ", "sigma", "禁闭弦张力"),
         ("θ_W", "theta_W", "温伯格角"), ("N_p", "N_p", "自由参数计数"),
         ("κ_q", "kappa_q", "电荷曲率（书称补充公设）")]

print("%-6s %-6s %-6s %-6s %s" % ("sym", "state", "value", "symAs", "sample"))
for sym, mac, desc in EXTRA:
    c = m.classify_symbol(sym, mac, book)
    print("%-6s %-6s %-6s %-6d %s" % (sym, c["state"], c["has_value"],
                                      c["sym_assign"],
                                      (c["samples"][0] if c["samples"] else "")[:40]))

print()
print("=== 外输清单机读 ===")
for mt in re.finditer(r"外输清单[^）)]{0,200}", book):
    print(" *", mt.group(0)[:180])
    print()
