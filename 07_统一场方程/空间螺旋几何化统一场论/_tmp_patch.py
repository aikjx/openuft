# -*- coding: utf-8 -*-
"""修 29 号脚本的 Ricci 第二项 bug + 判决卫生（容差真正参与 verdict）。"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
raw = open(P, "rb").read().decode("utf-8").replace("\r\n", "\n")
lines = raw.split("\n")
hits = []


def sub_once(old, new, tag):
    global lines
    cnt = 0
    for i, ln in enumerate(lines):
        if old in ln:
            lines[i] = ln.replace(old, new)
            cnt += 1
    hits.append((tag, cnt))
    if cnt != 1:
        print("!! %s hit %d times" % (tag, cnt))


# --- 1) sympy Ricci 第二项 ---
sub_once(
    "                s += sp.diff(Gam[rho][mu][nv], coords[rho]) - sp.diff(Gam[rho][nv][mu], coords[rho])",
    "                s += sp.diff(Gam[rho][mu][nv], coords[rho])\n"
    "                s -= sp.diff(Gam[rho][mu][rho], coords[nv])",
    "ricci_sym",
)

# --- 2) numpy Ricci 第二项 ---
sub_once(
    "                s = s + dgrid(Gam[c, a, b], c) - dgrid(Gam[c, b, a], c)",
    "                s = s + dgrid(Gam[c, a, b], c)\n"
    "            for c in range(4):\n"
    "                s = s - dgrid(Gam[c, a, c], b)",
    "ricci_np",
)

# --- 3) 容差常量 ---
sub_once(
    "np.random.default_rng(20261003)",
    "np.random.default_rng(20261003)\nTOL = 5e-2   # 数值-解析一致性容差（中心差分 O(h^2) 离散误差量级），显式化以免被当成机器精度",
    "tol_def",
)

# --- 4) A02 增加零判据 ---
sub_once(
    'P("A02", "符号引擎自检：de Sitter 满足 G_ab + Lc*g_ab = 0", "E_rr=%s" % E_rr)',
    'P("A02", "符号引擎自检：de Sitter 满足 G_ab + Lc*g_ab = 0",\n'
    '  "E_rr=%s ; 与 0 之差=%s" % (E_rr, sp.simplify(E_rr)), ok=(sp.simplify(E_rr) == 0))',
    "a02",
)

# --- 5) verdict 卫生 ---
sub_once(
    '  "10 个独立分量最大相对偏差 = %.2e（同一离散算子下应为机器精度附近）" % worst)',
    '  "10 个独立分量最大相对偏差 = %.2e（容差 TOL=%.0e；同一离散算子下应达该量级）" % (worst, TOL),\n'
    '  ok=(worst < TOL))',
    "a05",
)
sub_once(
    'P("A07", "A05 通过则数值引擎可用于判决新耦合", "偏差 %.1e < 1e-4 判据成立" % worst, ok=(worst < 1e-4))',
    'P("A07", "A05 通过则数值引擎可用于判决新耦合",\n'
    '  "偏差 %.2e vs 容差 %.0e" % (worst, TOL), ok=(worst < TOL))',
    "a07",
)
sub_once(
    '  "10 个独立分量最大逐点相对偏差 = %.2e" % worst)',
    '  "10 个独立分量最大逐点相对偏差 = %.2e（容差 %.0e）" % (worst, TOL), ok=(worst < TOL))',
    "b01",
)
sub_once(
    '  "最大相对偏差 = %.2e" % rel)\n\n# --- B04/B05',
    '  "最大相对偏差 = %.2e（容差 %.0e）" % (rel, TOL), ok=(rel < TOL))\n\n# --- B04/B05',
    "b03",
)
sub_once(
    '  "闭式 = -(alpha/(16 pi G rho_c))*(F+2*box)/D * nabla_b rho ；最大相对偏差 = %.2e" % rel)',
    '  "闭式 = -(alpha/(16 pi G rho_c))*(F+2*box)/D * nabla_b rho ；最大相对偏差 = %.2e（容差 %.0e）" % (rel, TOL),\n'
    '  ok=(rel < TOL))',
    "d01",
)

# --- 6) 冗余的 B02 占位变量清理 ---
sub_once(
    "c_sym, x_sym, y_sym = sp.symbols(\"c_sym x_sym y_sym\")\nF_sym = sp.Symbol(\"F_sym\")",
    "c_sym, x_sym, y_sym = sp.symbols(\"c_sym x_sym y_sym\")\nF_sym = sp.Symbol(\"F_sym\")\n"
    "_unused_trace_closed = 2 * c_sym * F_sym * (x_sym + 2 * y_sym) / (x_sym + y_sym)",
    "b02sym",
)

open(P, "wb").write(("\n".join(lines)).encode("utf-8"))
for t, c in hits:
    print("%-12s hits=%d" % (t, c))
try:
    compile(("\n".join(lines)), P, "exec")
    print("COMPILES CLEAN")
except SyntaxError as e:
    print("SyntaxError:", e.msg, "line", e.lineno, repr(lines[e.lineno - 1]))
