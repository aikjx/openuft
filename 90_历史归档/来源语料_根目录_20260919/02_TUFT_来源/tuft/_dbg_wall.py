import sys, numpy as np
HERE = r"d:/a10/aikjx/code/my_lib/openuft/90_历史归档/来源语料_根目录_20260919/02_TUFT_来源/tuft"
sys.path.insert(0, HERE)
import tuft_r26_leaver_wall_qnm as m
ga, gb, gc, td = m.make_solver(2)
print("td=%.3f" % td)
w = 0.41 - 0.03j
for n in range(4):
    print("n=%d  af=%r  bf=%r  gf=%r" % (n, ga(n, w), gb(n, w), gc(n, w)))
print("wall_series N=50 :", m.wall_series(w, 0.02439, 50, ga, gb, gc))
print("wall_series N=3000:", m.wall_series(w, 0.02439, 3000, ga, gb, gc))
# 逐步看 a_cur 演化
a_prev = 0.0 + 0j; a_cur = 1.0 + 0j; xp = 0.02439; S = a_cur + 0j
for n in range(20):
    an = complex(ga(n, w)); bn = complex(gb(n, w)); gn = complex(gc(n, w))
    if n == 0:
        a_next = -bn * a_cur / an
    else:
        a_next = -(bn * a_cur + gn * a_prev) / an
    a_prev = a_cur; a_cur = a_next; xp = xp * 0.02439; S = S + a_cur * xp
    print("  n=%2d an=%12.4e a_cur=%12.4e S=%12.4e" % (n, an, a_cur, S))
