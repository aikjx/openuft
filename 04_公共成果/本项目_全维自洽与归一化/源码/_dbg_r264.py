# -*- coding: utf-8 -*-
import io, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
NAME = ("TUFT-r264_自由参数总账层_ω赋值与单位依赖及四态分类与八粒子字典表自洽崩坏"
        "_精算与可视化_2026-10-31")
m = importlib.import_module(NAME)
book = m.BOOK_TEXT
print("book lines:", len(book.splitlines()))
print("%-6s %-6s %-6s %-6s %-6s %-6s %s" %
      ("sym", "state", "value", "numAs", "symAs", "fitLn", "sample"))
for sym, mac, desc in m.CORE_SYMBOLS:
    c = m.classify_symbol(sym, mac, book)
    s = (c["fit_samples"][0] if c["fit_samples"] else "")
    print("%-6s %-6s %-6s %-6d %-6d %-6d %s" %
          (sym, c["state"], c["has_value"], c["num_assign"],
           c["sym_assign"], c["fit_lines"], s[:60]))
print()
print("states:", sorted({m.classify_symbol(s, mm, book)["state"]
                         for s, mm, _ in m.CORE_SYMBOLS}))
