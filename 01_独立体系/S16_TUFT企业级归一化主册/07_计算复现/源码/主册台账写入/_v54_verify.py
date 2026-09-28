# -*- coding: utf-8 -*-
import io, json, os
base = r"D:\a10\aikjx\code\my_lib"
chdir = os.path.join(base, "openuft", "书籍", "v1_正文", "第十二编_动力学本征值路线_解锁UFT-3的真实尝试")

print("=== 1) ledger JSON reload ===")
d = json.load(io.open(os.path.join(base,"TUFT_归一化台账_v1.0.json"), encoding="utf-8"))
print("version=", d["version"], "| latest_round=", d["latest_round"], "| equation_range=", d["equation_range"])
print("date=", d["date"], "| last_updated=", d.get("last_updated"), "| latest_erratum=", d["latest_erratum"])
print("v54 key_results present:", "v54_rotating_msplit_key_results" in d)
print("open_backlog[0] head:", d["open_backlog"][0][:50])
fsc = d["four_state_counts_approx"]; print("four_state:", fsc["strict"], fsc["conditional"], fsc["definition"], fsc["open"])

print("\n=== 2) master register version/E504 ===")
m = io.open(os.path.join(base,"TUFT_企业级归一化主册_v1.0.md"), encoding="utf-8").read()
print("title v6.6:", m.startswith("# TUFT 企业级归一化主册 v6.6"))
print("E504 count:", m.count("E504"), "| v6.6 block:", m.count("v6.6（v54"))
print("6.44× present:", "6.44" in m, "| erratum #42 held:", "#42 held" in m)

print("\n=== 3) ch66 + chapter ledger len() ===")
files = [
 ("62","第62章_动力学本征值路线_可行性判据与首次真实尝试.md"),
 ("63","第63章_旋钮零空间定理_动力学可行性判据的形式化.md"),
 ("64","第64章_定理D作用S13_标度不变性壁垒.md"),
 ("65","第65章_TUFT理论几何与反射律.md"),
 ("66","第66章_复谱GradeA_TUFT基频极点与两路互证.md"),
 ("67","第67章_物理阻尼独立通道与否定定理全录.md"),
 ("68","第68章_砖一构造尝试与输入壁垒.md"),
 ("69","第69章_砖一_CW环绕数整数性变分硬约束.md"),
 ("70","第70章_砖三_动力学零核与参数空间零核OPEN.md"),
]
tot=0
for k,v in files:
    n=len(io.open(os.path.join(chdir,v),encoding="utf-8").read()); tot+=n; print(f"  ch{k}={n}")
print("  TOTAL =", tot)
led = io.open(os.path.join(chdir,"_章节账本.md"),encoding="utf-8").read()
print("  ledger md len:", len(led), "| 122749 in ledger:", "122749" in led, "| 39492 in ledger:", "39492" in led)
print("  66.17 in ch66:", "66.17" in io.open(os.path.join(chdir,files[4][1]),encoding="utf-8").read())

print("\n=== 4) flowchart HTML ===")
h = io.open(os.path.join(base,"TUFT_全物理现象关系流程图.html"),encoding="utf-8").read()
print("  SSOT v6.6:", "SSOT v6.6" in h, "| E1–E504:", "E1–E504" in h)
print("  v54 box:", "v54 旋转 m 频裂观测量" in h, "| 6.44× in box:", "6.44×" in h)
print("  div open/close:", h.count("<div"), h.count("</div>"))

print("\n=== 5) merge report ===")
r = io.open(os.path.join(base,"TUFT_v54_旋转m频裂合并报告.md"),encoding="utf-8").read()
print("  report len:", len(r), "| has 求导链/判别量/勘误/文件清单:", all(x in r for x in ["求导链","判别量","勘误","文件清单","外推","可探测"]))
print("\nALL CHECKS DONE")
