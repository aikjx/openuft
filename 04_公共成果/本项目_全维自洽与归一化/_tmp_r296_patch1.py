# -*- coding: utf-8 -*-
"""把 r296 里 _ricci_with_coef / _gamma_fd 改成系数一致的干净实现。"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "源码",
    "TUFT-r296_KK电磁耦合链求导证明验证精算_"
    "符号多项式Christoffel与非平坦背景曲率分解_"
    "EL变分导出Maxwell与光子质量零定理_正负对照_2026-11-01.py",
)

NEW = '''def _dg_fd(gpoly, x, h):
    """中心差分一阶导表（独立实现，不复用 pdiff）。"""
    n = len(gpoly)
    dg = [[[0.0] * n for _ in range(n)] for _ in range(n)]
    for k in range(n):
        xp = list(x)
        xm = list(x)
        xp[k] += h
        xm[k] -= h
        gp = eval_metric(gpoly, xp)
        gm = eval_metric(gpoly, xm)
        for b in range(n):
            for c in range(n):
                dg[k][b][c] = (gp[b][c] - gm[b][c]) / (2.0 * h)
    return dg


def _gamma_fd(gpoly, x, h, coef=0.5):
    """在偏移点重算 Γ（中心差分求导 + 可选系数改写，仅供负对照）。"""
    n = len(gpoly)
    g = eval_metric(gpoly, list(x))
    gi = mat_inv(g)
    dg = _dg_fd(gpoly, x, h)
    G = [[[0.0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0.0
                for d in range(n):
                    s += gi[a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                G[a][b][c] = coef * s
    return G


def _ricci_with_coef(gpoly, x, coef, h=1.0e-4):
    """Christoffel 系数被人为改错的版本（仅供负对照使用，物理上非法）。"""
    n = len(gpoly)
    g = eval_metric(gpoly, list(x))
    gi = mat_inv(g)
    dg = _dg_fd(gpoly, x, h)
    G = [[[0.0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0.0
                for d in range(n):
                    s += gi[a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                G[a][b][c] = coef * s
    dG = [[[[0.0] * n for _ in range(n)] for _ in range(n)]
           for _ in range(n)] for _ in range(n)]
    for e in range(n):
        xp = list(x)
        xm = list(x)
        xp[e] += h
        xm[e] -= h
        gp = _gamma_fd(gpoly, xp, h, coef)
        gm = _gamma_fd(gpoly, xm, h, coef)
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    dG[e][a][b][c] = (gp[a][b][c] - gm[a][b][c]) / (2.0 * h)
    return ricci_from(G, dG, n)
'''

src = io.open(P, encoding="utf-8").read()
lines = src.splitlines(True)
# 定位待替换区间（1-indexed 573..610）
start = None
end = None
for i, l in enumerate(lines):
    if l.startswith("def _ricci_with_coef"):
        start = i
    if l.startswith("def _gamma_fd"):
        end = i
# _ricci_with_coef 结束于 _gamma_fd 之前；_gamma_fd 结束于 'def q4_negative_controls' 之前
q4 = None
for i, l in enumerate(lines):
    if l.startswith("def q4_negative_controls"):
        q4 = i
        break
assert start is not None and end is not None and q4 is not None, (start, end, q4)
out = lines[:start] + [NEW + "\n\n"] + lines[q4:]
io.open(P, "w", encoding="utf-8", newline="").write("".join(out))
print("patched, lines:", len(out))
