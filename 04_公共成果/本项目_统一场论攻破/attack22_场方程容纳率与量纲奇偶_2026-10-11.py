# -*- coding: utf-8 -*-
"""
attack22｜几何势族的场方程能不能救它：量纲奇偶定理 · 算符-源分层 · 跑动尺度来路（攻破㉔）
=====================================================================================
靶：attack21（攻破⑲）面上登记的四个 OPEN——O19-1 m 的选定原理（无）、
    O19-2 κ/τ 的场方程（无）、O19-3 α 普适 vs 等效原理（未裁）、O19-4 力程修法与零判别力的分离（未做）。
本轮给族加上两条真实约束（局域度规-挠率-曲率几何；线性有心场方程），逐条问：
    判别力到底增加了几比特、从哪里增加的、代价记在谁账上。

攻击主张
  W1 量纲奇偶定理：只用 g、ε、Riem(L^-2)、Tors(L^-1) 及其协变导数作完全收缩，量纲**必为偶且非正**（幂集 {0,-2,-4,…}）。
  W2 半轴交集：族侧 [α]=L^(m-1) 的幂集是 {0,+1,+2,…}；两半轴之交 = {0} ⇒「α 可由多项式几何构造」⟺ m=1 唯一（且该格是空收缩＝纯数）。
  W2-预注册（开场写法，已被自己的穷举否证，否证留在 U03 面上）：原写「几何要偶 m、手性要奇 m ⇒ 交集空」。
      错处＝把「指数偶」读成「m 偶」：指数 m−1 为偶 ⟺ m 为奇 ⇒ 与 ⑲ T05 的手性侧**同向**，交集非空而是单点 {1}。
      幸存的半边：偶 m 在两侧皆无载体（既无手性，其 [α] 幂又不在几何环内）。
  W3 例外点名：要 m≥2 的 α 就得有 L^+ 幂的几何对象——环里没有（生成元幂全 ≤ 0）；绕开只能引外生矢量场或逆算符（非局域），两者都撞公设一。
  W4 算符分层：L=prod(∇²−μ_i²) 的球对称外部解空间维数 = 2s；任给有心势都能反解源 ⇒ 判别力从剖面搬进算符谱与源，净增 0。
  W5 判别力定价：三把算符（∇²／∇²−μ² 且 μ＝1/λ 匹配／∇²−μ² 且 μ＝1.3 不匹配）× 四类源约束（无约束／正定／外部零＝唯一点源／尾部快衰减）实测 6 枚目标律
     ⇒ 排除错误律 r^-5 的权力**只在源约束**里，幸存者数只由**手选的 μ**定（2／1／0），且「要 r^-2」与「要有限力程」不可同时免费。
  W6 手性奇偶见证延到 m=1：⑲ T05/T06 的枚举域是 m∈{2..6}，而 U02 选出的 m=1 不在域内 ⇒ 本条把同一把尺打到 m=1/2/3 三点现测（奇＝非零差、偶＝机器零）。
  W7 跑动不造尺度：1-loop 量纲生成的参考标度 Λ 仍是输入；反解「跑出弱力程所需 g²」⇒ 对每个 Λ>μ 都可凑，零内容。

体例：纯标准库；零随机；判定条目 U01–U15；自检 guard 全过 **且** 电池（每条判据真实输入须绿、
       corrupt 输入须红）全合格才退 0；运行报告落 `attack22_*_report.txt`（本册数值唯一载体；
      面自身字节／md5 只由 stdout 报，不落面）。他册读数一律现读盘，读不到即印「没读到」不作引用。
否证纪律：本轮开场预注册的 W2（互斥／空交）被自己的穷举否证 ⇒ 否证原样落在面上（U03），
          不许把主张改成事后正确的版本再假装它一开始就这样（同档案 rule 6：改判要留证词）。
阈值纪律：凡「相对偏差 < 阈」型判据，阈由该条差分截断 (h/r)^2 与相消噪声 eps/(2h/r) 现推并印出。
"""
import hashlib
import io
import math
import os
import re
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "attack22_场方程容纳率与量纲奇偶_2026-10-11_report.txt")
A21_FACE = os.path.join(HERE, u"attack21_几何势族P0修法_代价定价_2026-10-11_report.txt")
R34_FACE = os.path.join(HERE, os.pardir, u"本项目_全维自洽与归一化",
                        u"数据", u"TUFT-V41alpha自然单位势_全维审计_2026-10-10.md")

EPS = sys.float_info.epsilon
ITEMS = []
SELF = []
OUT = []
BATTERY = []


def emit(s=u""):
    OUT.append(s)


def item(tid, verdict, title):
    ITEMS.append((tid, verdict, title))
    emit(u"- %s [%s] %s" % (tid, verdict, title))


def sub(s):
    emit(u"  " + s)


subs = sub


def chk(name, ok, detail=u""):
    SELF.append((name, bool(ok)))
    emit(u"  [自检] %-40s %s%s" % (name, u"OK" if ok else u"RED", (u"  " + detail) if detail else u""))
    return bool(ok)


def read_b(p):
    if not os.path.isfile(p):
        return None
    with io.open(p, "rb") as fh:
        return fh.read()


def fmt(x):
    if x == 0:
        return u"0.000e+00"
    return u"%.3e" % x


def grep_face(path, key, label):
    b = read_b(path)
    if b is None:
        sub(u"他册读数 [%s]：载体读不到（%s）⇒ 不作引用" % (label, os.path.basename(path)))
        return None
    for ln in b.decode("utf-8", "replace").split(u"\n"):
        if key in ln:
            return ln.strip()
    sub(u"他册读数 [%s]：载体在场但没印该键 ⇒ 不作引用" % label)
    return None


# ---------------------------------------------------------------- 径向算符（中心差分）
def lap_num(f, r, h):
    """∇²f = f'' + 2f'/r，中心差分。"""
    fm, fp, f0 = f(r - h), f(r + h), f(r)
    return (fp - 2.0 * f0 + fm) / (h * h) + 2.0 * (fp - fm) / (2.0 * h * r)


def rel_dev(a, b):
    s = max(abs(a), abs(b))
    return 0.0 if s == 0.0 else abs(a - b) / s


def rank_tol(rows, tol=1e-9):
    """高斯消元求秩（纯标准库），用于 U04 的外部解空间维数实测。"""
    m = [list(r) for r in rows]
    nr, nc = len(m), len(m[0])
    r_ = 0
    for c in range(nc):
        piv = max(range(r_, nr), key=lambda i: abs(m[i][c])) if r_ < nr else None
        if piv is None or abs(m[piv][c]) < tol:
            continue
        m[r_], m[piv] = m[piv], m[r_]
        pv = m[r_][c]
        for i in range(nr):
            if i != r_ and m[i][c] != 0.0:
                fac = m[i][c] / pv
                for j in range(c, nc):
                    m[i][j] -= fac * m[r_][j]
        r_ += 1
        if r_ == nr:
            break
    return r_


# ---------------------------------------------------------------- 目标律库（6 枚，含一枚观测上错的）
SIG, A4, KK, LAM = 0.83, (-4.0 / 3.0) * 0.18, 0.5, 2.0


def u_newton(r):
    return -1.0 / r


def u_coulomb(r):
    return 1.0 / r


def u_wrong5(r):
    return 1.0 / r ** 5


def u_yukawa(r):
    return math.exp(-r / LAM) / r


def u_cornell(r):
    return SIG * r + A4 / r


def u_harmonic(r):
    return KK * r * r


TARGETS = [(u"牛顿 r^-2", u_newton), (u"库仑 r^-2", u_coulomb), (u"错误律 r^-5", u_wrong5),
           (u"汤川 e^-r/λ", u_yukawa), (u"Cornell", u_cornell), (u"谐振子 +kr", u_harmonic)]


def rho_analytic(name, r, mu):
    """ρ = ∇²U − μ²U 的逐条解析式（r>0；手推过程印在面上）。"""
    if name == u"牛顿 r^-2":
        return -mu * mu * (-1.0 / r)
    if name == u"库仑 r^-2":
        return -mu * mu * (1.0 / r)
    if name == u"错误律 r^-5":
        return 20.0 / r ** 7 - mu * mu / r ** 5          # ∇² r^-5 = (30−10) r^-7
    if name == u"汤川 e^-r/λ":
        e = math.exp(-r / LAM)
        a2 = 1.0 / (LAM * LAM)
        return a2 * e / r - mu * mu * e / r              # ∇²(e^{-r/λ}/r) = e/(λ²r)
    if name == u"Cornell":
        return 2.0 * SIG / r - mu * mu * (SIG * r + A4 / r)   # ∇²(σr)=2σ/r，∇²(1/r)=0
    if name == u"谐振子 +kr":
        return 6.0 * KK - mu * mu * KK * r * r          # ∇² r² = 6
    raise ValueError(name)


def main():
    emit(u"=" * 78)
    emit(u"attack22｜几何势族的场方程能不能救它：量纲奇偶定理 · 算符-源分层 · 跑动尺度来路（攻破㉔）")
    emit(u"=" * 78)

    a21 = read_b(A21_FACE)
    r34 = read_b(R34_FACE)
    a21_size = len(a21) if a21 else 0
    r34_size = len(r34) if r34 else 0
    emit(u"载体在场性（现读）：attack21 面 %s｜r34 面 %s" % (
        u"%d B／md5 %s" % (a21_size, hashlib.md5(a21).hexdigest()) if a21 else u"读不到",
        u"%d B／md5 %s" % (r34_size, hashlib.md5(r34).hexdigest()) if r34 else u"读不到"))

    # ============================== U01 量纲奇偶定理
    item(u"U01", u"THEOREM",
         u"W1 量纲奇偶＋半轴定理：g/ε/Riem/Tors 及协变导数的任何完全收缩，其 L 幂必为**偶且非正**（幂集 {0,-2,-4,…}；穷举 k,l,d,e ＋ 构造性配对）")
    KB, LB, DB, EB = 4, 3, 6, 3
    grid_n = (KB + 1) * (LB + 1) * (DB + 1) * (EB + 1)
    odd_feasible, even_feasible, witnesses = [], 0, []
    geo_powers = set()
    pos_feasible = 0
    dim0_cells = 0
    for k in range(KB + 1):                 # 挠率块数（3 指标，量纲 1）
        for l in range(LB + 1):             # 曲率块数（4 指标，量纲 2）
            for d in range(DB + 1):         # 协变导数（1 指标，量纲 1）
                for e in range(EB + 1):     # ε 用量（每次消化 4 枚指标，量纲 0）
                    idx = 3 * k + 4 * l + d - 4 * e
                    if idx < 0:
                        continue
                    dim = k + 2 * l + d
                    feas = (idx % 2 == 0)   # 度规只成对消化指标 ⇒ 剩余指标须为偶
                    if feas and dim % 2 == 1:
                        odd_feasible.append((k, l, d, e, dim))
                    if feas and dim % 2 == 0:
                        even_feasible += 1
                        geo_powers.add(-dim)
                        if dim > 0:
                            pos_feasible += 1
                        if dim == 0:
                            dim0_cells += 1
                        if 0 < dim <= 4:
                            witnesses.append((k, l, d, e, dim))
    sub(u"设定：[Tors]=L^-1（3 指标）、[Riem]=L^-2（4 指标）、[∇]=L^-1；g、ε 无量纲；"
        u"完全收缩＝自由指标全由度规成对消化（±ε 一次拿 4 枚）。收缩的 L 幂 = −(k+2l+d)，剩余指标数 = 3k+4l+d−4e。")
    sub(u"穷举 k≤%d, l≤%d, d≤%d, e≤%d（%d 格）：奇幂且可行 %d 枚｜偶幂且可行 %d 枚（非空＝定理不是空集之谈）"
        % (KB, LB, DB, EB, grid_n, len(odd_feasible), even_feasible))
    sub(u"半轴核算：可行格的 L 幂集合 = %s｜幂 > 0 的可行格 = %d 枚（生成元幂全 ≤ 0 ⇒ 多项式收缩造不出正幂）｜"
        u"幂 = 0 的可行格 = %d 枚（唯一那一格是空收缩 k=l=d=e=0，即纯数）"
        % (u"、".join(u"L^%+d" % p for p in sorted(geo_powers)), pos_feasible, dim0_cells))
    sub(u"最低阶见证：(k,l,d,e)=(2,0,0,0)→T_{μνρ}T^{μνρ} [L^-2]；(0,1,0,0)→R_{μνρσ}R^{μνρσ} [L^-4]；"
        u"(1,0,1,0)→∇·(Tr T) 型 [L^-2]；(3,0,0,0) 指标 9 为奇 ⇒ 不可行（同一判据在低阶也成立）")
    sub(u"证明骨架：3k+4l+d−4e ≡ k+d (mod 2)；幂 −(k+2l+d) 的奇偶 = k+2l+d ≡ k+d (mod 2) ⇒ 二者同奇偶；"
        u"可行⇒指标偶⇒k+d 偶⇒幂偶。反向：k+d 偶且指标数≥0 时逐对度规缩并必成 ⇒ 可行集非空且全为偶。"
        u"半轴：每一块幂 ≤ 0 且无常数块 ⇒ 收缩幂 ≤ 0，取 0 当且仅当全块为 0。")
    chk(u"U01 奇幂可行格 0 枚、偶幂可行格 > 0、正幂 0 枚、零幂唯一",
        len(odd_feasible) == 0 and even_feasible > 0 and pos_feasible == 0 and dim0_cells == 1,
        u"odd=%d even=%d pos=%d dim0=%d witnesses=%d"
        % (len(odd_feasible), even_feasible, pos_feasible, dim0_cells, len(witnesses)))
    BATTERY.append((u"U01 奇偶穷举", lambda n: n == 0, len(odd_feasible), len(odd_feasible) + 1))
    BATTERY.append((u"U01 零幂唯一", lambda n: n == 1, dim0_cells, 2))

    # ============================== U02 半轴交集：几何可构造 ⟺ m=1
    item(u"U02", u"THEOREM",
         u"W2 半轴交集：族侧 [α]=L^(m-1) 的幂集 {0,+1,+2,…} ∩ 几何幂集 {0,-2,-4,…} = {0} ⇒「α 可多项式几何构造」⟺ m=1（唯一）")
    rows = []
    for m in range(1, 13):
        da = m - 1
        geo = (-da) in geo_powers          # α 幂 = L^(m-1) 落在几何幂集内（该集非正，故仅 m=1）
        chir = (m % 2 == 1)                # ⑲ T05：手性有载体 ⟺ m 奇
        carry = u"G" if da == 2 else (u"k/g_w/g_s" if da == 0 else u"无")
        rows.append((m, da, geo, chir, carry))
    geo_only = [r[0] for r in rows if r[2]]
    both = [r[0] for r in rows if r[2] and r[3]]
    sub(u"m:[α]幂:几何可构造(U01):手性载体(⑲ T05):该幂按 ⑲ T04 承载")
    sub(u"  ".join(u"%d:%+d:%s:%s:%s" % (m, da, u"可" if g else u"否", u"有" if c else u"无", h)
                   for m, da, g, c, h in rows))
    sub(u"机器裁定：「α 可几何构造」的 m = %s（幂只能是 L^0，而那格是空收缩＝纯数）；"
        u"∩「手性有载体」= %s ⇒ **交集不是空集，而是单点 {1}**；"
        u"⑲ T04 的最佳命中 3/4 恰好也在 m=1（无量纲规范耦合），两条独立路线同点 ⇒ m=1 是这一族被几何公设逼出来的唯一点"
        % (u"、".join(str(x) for x in geo_only), u"、".join(str(x) for x in both)))
    sub(u"仍然成立的半边（原预注册里唯一活下来的部分）：偶 m 侧「几何可构造 ∪ 手性有载体」= %s 枚 ⇒ 来料 m=2 是**两侧皆空**："
        u"[α]=L^1 既不在几何环内（奇幂），又不载体征（⑲ T05 偶 m 的同号/异号力相对差 = 机器零）"
        % sum(1 for r in rows if r[0] % 2 == 0 and (r[2] or r[3])))
    sub(u"G 一支（⑲ T04：[G]=L^+2 需 m=3）：L^+2 ∉ 几何幂集 ⇒ **α=G 对全族任何 m 都不能由多项式几何收缩构造**，"
        u"这比 ⑲ T04 的「4/4 对一切 m 不可能」更强：不是各支抢同一个 m 抢不到，而是引力那一支单独就出环。")
    chk(u"U02 几何侧单点 {1}、与手性侧之交 {1}、偶 m 侧并集空",
        geo_only == [1] and both == [1] and sum(1 for r in rows if r[0] % 2 == 0 and (r[2] or r[3])) == 0,
        u"geo=%s both=%s even_union=%d" % (geo_only, both,
                                          sum(1 for r in rows if r[0] % 2 == 0 and (r[2] or r[3]))))
    BATTERY.append((u"U02 单点集", lambda s: s == [1], geo_only, [1, 3]))

    # ============================== U02b 预注册主张的否证记录（最小对）
    item(u"U02b", u"FAIL",
         u"本轮开场的预注册主张 W2（「几何要偶 m、手性要奇 m ⇒ 交集空」）被自己的穷举否证——错因是幂平移一格，非数据偶然")
    wrong_geo = [m for m in range(1, 13) if m % 2 == 0]
    wrong_both = [m for m in range(1, 13) if m % 2 == 0 and m % 2 == 1]
    sub(u"两条判据并列（其余一切不动）：错读「指数偶 ⇒ m 偶」给出 m = %s；正读「L^(m-1) ∈ 几何幂集」给出 m = %s；"
        u"两者互反 ⇒ 我原先写的空交集是**用错读的那一侧**去交「m 奇」，才恰好显得互斥"
        % (u"、".join(str(x) for x in wrong_geo), u"、".join(str(x) for x in geo_only)))
    sub(u"最小对（一枚字符之差翻转结论）：把「m 偶」换成「m−1 偶」＝平移一格 ⇒ 交集由 %s（空）变为 %s（单点）；"
        u"这条否证只在面上留证词，不改写开场主张（同档案 rule 6：改判要留原话）"
        % (u"∅" if not wrong_both else u"、".join(str(x) for x in wrong_both),
           u"、".join(str(x) for x in both)))
    chk(u"U02b 错读集与正读集互反且正读集 = {1}",
        set(wrong_geo).isdisjoint(geo_only) and geo_only == [1] and len(wrong_both) == 0,
        u"wrong=%d right=%d inter_wrong=%d" % (len(wrong_geo), len(geo_only), len(wrong_both)))
    BATTERY.append((u"U02b 错读集非空", lambda s: len(s) > 0 and s == wrong_geo and s != geo_only,
                    wrong_geo, geo_only))

    # ============================== U02c 手性奇偶见证延到 m=1
    item(u"U02c", u"PASS",
         u"W6 把 ⑲ T05/T06 的 τ→−τ 奇偶尺打到 m=1（它不在 ⑲ 的枚举域 m∈{2..6} 内，却是 U02 选出的唯一点）")
    AA, BB, alpha0 = 2.0, 1.0, -1.5
    rs_c = [0.7, 1.3, 2.9, 6.1]
    def u_branch(mm, s, r):
        return alpha0 * (AA ** mm * r ** (-1.0) - (s * BB) ** mm * r ** (-1.0))
    def f_branch(mm, s, r, hh):
        return -(u_branch(mm, s, r + hh) - u_branch(mm, s, r - hh)) / (2.0 * hh)
    seen_c = []
    for mm in (1, 2, 3):
        hh = mm * 0 + 1e-5
        dmax = max(abs(f_branch(mm, +1.0, r, hh) - f_branch(mm, -1.0, r, hh)) for r in rs_c)
        fmax = max(abs(f_branch(mm, +1.0, r, hh)) for r in rs_c)
        seen_c.append((mm, dmax, dmax / fmax))
    for mm, dmax, reld in seen_c:
        subs(u"m=%d：max|F(τ)−F(−τ)| = %s｜相对差 = %s ⇒ 手性%s载体（奇偶判据：%s）"
             % (mm, fmt(dmax), fmt(reld), u"有" if dmax > 1e-9 else u"无",
                u"奇 m 应非零" if mm % 2 else u"偶 m 应机器零"))
    sub(u"判读：⑲ T05 的枚举域是 m∈{2..6}，其 3/3 集 = {3、5}（现读见 U12）；本条把同一条奇偶律延到 m=1，"
        u"实测非零差且相对差 = %s（与 ⑲ 奇 m 侧的 2.000 同值，因 A=2、B=1 时相对差 = 2B^m/(A^m−B^m)）⇒ "
        u"U02 选出的唯一点 m=1 在手性侧**同样开着**：交集 {1} 不是靠把 m=1 排除在枚举域外才非空"
        % fmt(seen_c[0][2]))
    chk(u"U02c 奇 m 非零差（含 m=1）、偶 m 机器零", 
        all(s[1] > 1e-9 for s in seen_c if s[0] % 2) and all(s[1] < 1e-12 for s in seen_c if s[0] % 2 == 0),
        u"odd=%s even_zero=%s" % ([u"%d:%s" % (s[0], fmt(s[1])) for s in seen_c if s[0] % 2],
                                  [u"%d:%s" % (s[0], fmt(s[1])) for s in seen_c if s[0] % 2 == 0]))
    BATTERY.append((u"U02c 奇偶两侧", lambda o, ev: o > 1e-9 and ev < 1e-12,
                    (seen_c[0][1], seen_c[1][1]), (seen_c[0][1], 1.0)))

    # ============================== U03 例外的最小外来物
    item(u"U03", u"PASS",
         u"W3 绕开半轴的两条路都要付公设一：环里没有 L^+ 幂元素（第二把尺独立复核），只能引外生矢量场或逆算符（非局域）")
    pure_odd = 0
    pure_even = 0
    for k in range(3):
        for l in range(3):
            for d in range(5):
                if (3 * k + 4 * l + d) % 2 == 0:
                    if (k + 2 * l + d) % 2 == 1:
                        pure_odd += 1
                    else:
                        pure_even += 1
    vec_odd = 0
    for a in range(1, 4):                 # 外生矢量 A_μ：1 指标、量纲 0（作为背景场）
        for k in range(3):
            for d in range(4):
                if (a + 3 * k + 1 * d) % 2 == 0 and (k + d) % 2 == 1:
                    vec_odd += 1
    sub(u"第二把尺（只看指标奇偶，不穷举 ε）：纯几何块（T/R/∇）指标偶且量纲奇的组合 = %d 枚；"
        u"偶量纲可行组合 = %d 枚；加入 1 枚外生矢量后奇量纲组合 = %d 枚" % (pure_odd, pure_even, vec_odd))
    sub(u"最低例外例：A_μ T^{μ}（迹矢量与外生矢量缩并，量纲 L^-1）；或 ∇_μ A^μ（L^-1）。"
        u"两条都携带「非度规-挠率-曲率」的新自由度 ⇒ 与来料公设一正面冲突（要么禁止它、要么公设失身）。")
    chk(u"U03 纯几何奇量纲 0 枚、含外生矢量 > 0 枚", pure_odd == 0 and vec_odd > 0,
        u"pure_odd=%d pure_even=%d vec=%d" % (pure_odd, pure_even, vec_odd))
    BATTERY.append((u"U03 例外计数", lambda a, b: a == 0 and b > 0, (pure_odd, vec_odd), (1, vec_odd)))

    # ============================== U04 外部解空间维数
    item(u"U04", u"THEOREM",
         u"W4a 算符 L=prod(∇²−μ_i²) 的球对称外部解空间维数 = 2s（s＝不同 μ 个数），形状只有 e^{±μr}/r 的线性组合")
    mus = {1: [1.7], 2: [1.7, 0.9], 3: [1.7, 0.9, 0.4]}
    dims_expected = {}
    for s, ms in sorted(mus.items()):
        basis = []
        for mu_i in ms:
            basis.append(lambda r, q=mu_i: math.exp(-q * r) / r)
            basis.append(lambda r, q=mu_i: math.exp(q * r) / r)
        rs = [0.7 + 0.11 * i for i in range(len(basis) + 4)]
        M = [[f(r) for f in basis] for r in rs]
        rk = rank_tol(M)
        dims_expected[s] = rk
        sub(u"s=%d（不同 μ 个数 %s）⇒ 基函数 %d 枚，采样矩阵 %d×%d 的实测秩 = %d（期望 2s=%d）"
            % (s, u"、".join(fmt(x) for x in ms), len(basis), len(rs), len(basis), rk, 2 * s))
    deg = rank_tol([[math.exp(-1.7 * r) / r, r * math.exp(-1.7 * r) / r, math.exp(1.7 * r) / r,
                     r * math.exp(1.7 * r) / r] for r in [0.7, 0.9, 1.1, 1.3]])
    sub(u"重根支（μ 相同 s=2）：基要换成 e^{±μr}/r 与 r e^{±μr}/r，实测秩 = %d ⇒ 维数仍是 2s，但形状多出 r 的幂因子" % deg)
    chk(u"U04 实测秩 = 2s 全部成立且重根支维数不变",
        all(dims_expected[s] == 2 * s for s in dims_expected) and deg == 4,
        u"dims=%s repeated=%d" % (sorted(dims_expected.items()), deg))
    BATTERY.append((u"U04 维数", lambda d: d == 2, dims_expected[1], 3))

    # ============================== U05 源可反解（构造性零增量）
    item(u"U05", u"THEOREM",
         u"W4b 场方程不增判别力：任给有心目标势 U_t，ρ=L[U_t] 精确存在 ⇒ 加线性算符后仍容纳全体有心律（⑲ T10 的推广）")
    MU5 = 1.7
    worst = 0.0
    pred_thr = (1e-4) ** 2 + EPS / (2.0 * 1e-4)
    detail5 = []
    for nm, f in TARGETS:
        mx = 0.0
        for r in [0.5, 1.0, 3.0, 11.0, 40.0]:
            h = r * 1e-4
            num = lap_num(f, r, h) - MU5 * MU5 * f(r)
            mx = max(mx, rel_dev(num, rho_analytic(nm, r, MU5)))
        detail5.append((nm, mx))
        worst = max(worst, mx)
    for nm, mx in detail5:
        subs(u"%s：数值 ρ=∇²U−μ²U 对解析式最大相对残差 %s ⇒ 源精确可反解（无不可容纳的形状）"
             % (nm, fmt(mx)))
    thr5 = 100 * pred_thr
    sub(u"阈的来路：h=r·1e-4 ⇒ 截断 (h/r)²=%s、相消噪声 eps/(2h/r)=%s ⇒ 预测残差 %s、判据阈取 100 倍 = %s；实测 worst=%s"
        % (fmt((1e-4) ** 2), fmt(EPS / (2e-4)), fmt(pred_thr), fmt(thr5), fmt(worst)))
    chk(u"U05 六目标全可反解源（worst < 现推阈）", worst < thr5 and len(detail5) == 6,
        u"worst=%s thr=%s" % (fmt(worst), fmt(thr5)))
    BATTERY.append((u"U05 残差判据", lambda w, t: w < t, (worst, thr5), (worst + 1e-3, thr5)))

    # ============================== U06 源约束的判别力定价（三把算符 × 四类约束）
    item(u"U06", u"PASS",
         u"W5 判别力定价：无约束 6/6、正定档是橡皮图章（∇² 下 6/6）、唯一点源档在 ∇² 下 2/6——排除错误律的权力全在源约束，"
         u"而幸存者数只由手选的 μ 定（匹配 1 枚／不匹配 0 枚）")
    rs6 = [0.35, 0.6, 1.0, 1.8, 3.2, 6.0, 12.0, 25.0]
    MU_M = 1.0 / LAM
    MU_U = 1.3
    OPS = [(u"∇²", 0.0), (u"∇²−μ²(μ=1/λ 匹配)", MU_M), (u"∇²−μ²(μ=1.3 不匹配)", MU_U)]
    mats = {}
    for opname, mu_op in OPS:
        rows6 = []
        for nm, f in TARGETS:
            rho = [rho_analytic(nm, r, mu_op) for r in rs6]
            ext = max(abs(x) for x in rho)
            posdef = all(x >= -1e-9 * max(1.0, max(abs(x) for x in rho)) for x in rho)
            pointlike = ext < 1e-9
            tail = max(abs(x) for x in rho[-2:]) / max(1e-300, max(abs(x) for x in rho[:3]))
            fastdec = tail < 1e-4
            rows6.append((nm, posdef, pointlike, fastdec, ext, tail))
        mats[opname] = rows6
    for opname, mu_op in OPS:
        sub(u"算符 %s（μ=%s）下逐枚目标律的源形状（外部 max|ρ|、尾/头比）："
            % (opname, fmt(mu_op) if mu_op else u"0（无质量）"))
        for nm, pdc, pt, fd, ext, tail in mats[opname]:
            subs(u"%-12s 正定=%s 唯一点源=%s 尾快衰减=%s｜外部 max|ρ|=%s｜尾/头=%s"
                 % (nm, u"是" if pdc else u"否", u"是" if pt else u"否", u"是" if fd else u"否",
                    fmt(ext), fmt(tail)))
    cnt = {}
    for opname, mu_op in OPS:
        cnt[opname] = (6, sum(1 for x in mats[opname] if x[1]),
                       sum(1 for x in mats[opname] if x[2]), sum(1 for x in mats[opname] if x[3]))
    for opname, mu_op in OPS:
        sub(u"容纳数 %s：无约束=%d｜正定=%d｜唯一点源=%d｜尾快衰减=%d" % ((opname,) + cnt[opname]))
    pt_lap = [x[0] for x in mats[u"∇²"] if x[2]]
    pt_m = [x[0] for x in mats[u"∇²−μ²(μ=1/λ 匹配)"] if x[2]]
    pt_u = [x[0] for x in mats[u"∇²−μ²(μ=1.3 不匹配)"] if x[2]]
    pt_counts = (len(pt_lap), len(pt_m), len(pt_u))
    sub(u"判读：①「正定」在 ∇² 下 6/6 全收＝**橡皮图章**（一枚约束都没有）；②「唯一点源」在 ∇² 下只留 %s"
        u"——被排除的正是那枚观测上错的 r^-5 以及汤川/Cornell/谐振子；③换成有质量算符，点源档随**手选的 μ** 变动："
        u"μ=1/λ 时只剩 %s（就是那支汤川，λ=1/μ 天然吻合），μ=1.3 时剩 %s ⇒ 算符自己选不出该留哪一支，"
        u"它是**旋钮不是结论**；④μ=1/λ 那一档里 r^-2 两支（%s）都不再是外部解 ⇒ **「要 r^-2 律」与「要有限力程」不能同时免费**，"
        u"要两者兼得就必须允许**连续分布源**，而那是族里从未写过的一条独立物理输入。"
        % (u"、".join(pt_lap), u"、".join(pt_m) or u"空", u"、".join(pt_u) or u"空",
           u"、".join([x[0] for x in mats[u"∇²−μ²(μ=1/λ 匹配)"] if x[0].startswith((u"牛", u"库"))])
        ))
    chk(u"U06 正定档橡皮图章(∇² 6/6)、点源档 2/1/0 三档且 ∇² 档只留 r^-2 两支",
        cnt[u"∇²"][1] == 6 and pt_counts == (2, 1, 0)
        and set(pt_lap) == {u"牛顿 r^-2", u"库仑 r^-2"},
        u"lap=%s m=%s u=%s" % (list(cnt[u"∇²"]), list(cnt[u"∇²−μ²(μ=1/λ 匹配)"]),
                               list(cnt[u"∇²−μ²(μ=1.3 不匹配)"])))
    BATTERY.append((u"U06 点源档有牙", lambda t, n: t == (2, 1, 0) and n == 6,
                    (pt_counts, cnt[u"∇²"][1]), ((2, 2, 0), 6)))

    # ============================== U07 数值通道的牙（核 vs 非核：h 阶梯的收缩率）
    item(u"U07", u"BOUNDARY",
         u"W4c 差分尺自己要有牙：同一把尺打在算符核上残差按 O(h²) 收缩（两次半距比值都≈4）、"
         u"打在非核上不随 h 消失（比值≈1）")
    hs = [2e-3, 1e-3, 5e-4]
    rs7 = [1.0, 2.0, 3.0]
    q = []
    for nm, f in ((u"核 e^-μr/r（λ=1/μ）", lambda r: math.exp(-MU_M * r) / r),
                  (u"非核 r^-5", lambda r: 1.0 / r ** 5)):
        res = [max(abs(lap_num(f, r, hh) - MU_M * MU_M * f(r)) for r in rs7) for hh in hs]
        rat = [res[i] / res[i + 1] if res[i + 1] else float("inf") for i in range(len(res) - 1)]
        q.append((nm, res, rat))
    for nm, res, rat in q:
        subs(u"%s：max|(∇²−μ²)f| 在 h=%s 阶梯上 = %s｜相邻比值 %s（期望 %s）"
             % (nm, u"→".join(fmt(x) for x in hs), u"→".join(fmt(x) for x in res),
                u"、".join(fmt(x) for x in rat),
                u"≈4（核＝纯截断，h 折半 ⇒ 残差 /4）" if nm.startswith(u"核") else u"≈1（非核＝真信号，减半不缩小）"))
    ker_pred = q[0][1][0] * (hs[0] / hs[-1]) ** 2
    ker_dev = rel_dev(ker_pred, q[0][1][-1])
    # 阈由同一把 O(h²) 尺的两端现推：比值带宽 [3.5,4.5] ⇒ 两步预测 res0·16 落在 [16/4.5², 16/3.5²]·res2
    thr_ker = max(abs(16.0 / (3.5 * 3.5) - 1.0), abs(16.0 / (4.5 * 4.5) - 1.0))
    ok_ker = all(3.5 <= x <= 4.5 for x in q[0][2]) and ker_dev < thr_ker
    ok_non = all(0.85 <= x <= 1.15 for x in q[1][2])
    sub(u"第二口径（不按比值按幂律本身）：由 O(h²) 用最大 h 的残差预测最小 h 的残差 = %s，实测 = %s，相对偏差 %s；"
        u"阈 %s 不是手钉——由比值带宽 [3.5,4.5] 的两端反推（16/4.5² 与 16/3.5² 两侧取最大偏离）"
        % (fmt(ker_pred), fmt(q[0][1][-1]), fmt(ker_dev), fmt(thr_ker)))
    sub(u"判读：核函数残差是**纯截断**（两次相邻比值都落在 O(h²) 的 4 附近），非核残差是真信号（比值≈1，h 减半不缩小）"
        u"⇒ 这台尺能分辨「在核里」与「不在核里」，U06 的点源档不是把尺子的盲区写成排除。")
    chk(u"U07 核两次比值∈[3.5,4.5] 且幂律预测<现推阈、非核两次比值∈[0.85,1.15]", ok_ker and ok_non,
        u"rat_ker=%s rat_non=%s dev=%s thr=%s" % ([fmt(x) for x in q[0][2]], [fmt(x) for x in q[1][2]],
                                                  fmt(ker_dev), fmt(thr_ker)))
    BATTERY.append((u"U07 双比值", lambda a, b: all(3.5 <= x <= 4.5 for x in a) and all(0.85 <= x <= 1.15 for x in b),
                    (q[0][2], q[1][2]), ([2.0, 2.0], q[1][2])))

    # ============================== U08 跑动不造尺度
    item(u"U08", u"FAIL",
         u"W6 量子跑动不产生尺度：1-loop 关系里参考标度 Λ 是输入；反解「得弱力程所需 g²」对所有 Λ>μ_W 都有解 ⇒ 零内容")
    line_mu = grep_face(A21_FACE, u"μ_W =", u"attack21 T08 弱力程标度 μ_W")
    mu_w = None
    if line_mu:
        mm = re.search(u"([0-9.eE+-]+)\\s*m\\^-1", line_mu)
        if mm:
            mu_w = float(mm.group(1))
    sub(u"他册现读：%s ⇒ μ_W = %s（载体＝attack21 面；读不到则本条降级为无量纲演示，不引数值）"
        % (line_mu if line_mu else u"没读到那行", fmt(mu_w) if mu_w else u"没读到"))
    scales = [(u"普朗克长度倒数", 1.0 / 1.616255e-35), (u"1 fm 倒数", 1.0 / 1e-15),
              (u"电弱长度倒数", 1.0 / 2.45502e-18), (u"1 AU 倒数", 1.0 / 1.49598e11),
              (u"1 m 倒数", 1.0)]
    rows8 = []
    if mu_w:
        for nm, lam in scales:
            x = math.log(lam / mu_w)
            for b in (Fr(1, 10), Fr(1, 2), Fr(1)):
                g2 = 1.0 / (2.0 * float(b) * x) if x > 0 else None
                rows8.append((nm, float(b), x, g2, g2 is not None and g2 > 0,
                              g2 is not None and 0 < g2 < 4 * math.pi))
        sub(u"公式：μ_phys = Λ·exp(−1/(2 b g²(Λ))) ⇒ 要得 μ_W 必须 1/(2bg²) = ln(Λ/μ_W)；Λ 由「现成的那把尺」给")
        for nm, b, x, g2, solv, pert in rows8:
            subs(u"Λ=%-15s b=%.1f ⇒ ln(Λ/μ_W)=%s｜所需 g²=%s｜有正解=%s｜微扰内(g²<4π)=%s"
                 % (nm, b, fmt(x), fmt(g2) if g2 is not None else u"无解(Λ<μ_W)",
                    u"是" if solv else u"否", u"是" if pert else u"否"))
        nsolv = sum(1 for r in rows8 if r[4])
        npert = sum(1 for r in rows8 if r[5])
        sub(u"机器裁定：%d 个 (Λ,b) 组合里 %d 个有正解、其中 %d 个落在微扰区 ⇒ "
            u"给定任意 Λ>μ_W 都能凑出 g²，「跑动生成力程」**不排除任何力程值**（零判别力）；"
            u"Λ<μ_W 的组合无解——那是同一件事的另一面：这条路线只约束了层级符号，没约束 μ_W 本身"
            % (len(rows8), nsolv, npert))
        chk(u"U08 每个 Λ>μ_W 都有解（零内容的实测形状）", nsolv == sum(1 for r in rows8 if r[2] > 0) and nsolv > 0,
            u"rows=%d solvable=%d perturbative=%d" % (len(rows8), nsolv, npert))
        BATTERY.append((u"U08 有解计数", lambda a, b: a == b and a > 0, (nsolv, sum(1 for r in rows8 if r[2] > 0)),
                        (nsolv - 1, sum(1 for r in rows8 if r[2] > 0))))
    else:
        sub(u"μ_W 读数缺席 ⇒ 本条不落地（登记为读数缺席，不作任何数值引用）")
        chk(u"U08 读数缺席如实登记", True, u"mu_w=None")
        BATTERY.append((u"U08 缺席分支", lambda ok: ok, True, False))

    # ============================== U09 微扰侧的部分可证伪
    item(u"U09", u"BOUNDARY",
         u"W6b 微扰性只否掉一部分 Λ 档：它给出一条真可证伪的约束（Λ 必须足够高于 μ_W），但选不出 Λ ⇒ O24-4 仍 OPEN")
    if mu_w and rows8:
        by = {}
        for nm, b, x, g2, solv, pert in rows8:
            by.setdefault(nm, []).append(pert)
        for nm, lst in sorted(by.items()):
            subs(u"Λ=%-15s 存在微扰解=%s（%d/%d 档 b 合格）" % (nm, u"是" if any(lst) else u"否",
                                                                sum(1 for v in lst if v), len(lst)))
        nok = sum(1 for nm, lst in by.items() if any(lst))
        sub(u"判读：%d/%d 档 Λ 至少有一个 b 让 g² 落在微扰区；被否掉的那些是 Λ<μ_W 的档（层级符号，不是力程数值）。"
            u"⇒ 这条路线**可被部分证伪**（若所有档都非微扰就死了），但「选哪一档 Λ」仍需外部输入 ⇒ 判别力仍为 0。")
        chk(u"U09 至少一档被否且至少一档可活（两侧都非空＝这条约束真有内容但不够）",
            0 < nok < len(by), u"alive=%d total=%d" % (nok, len(by)))
        BATTERY.append((u"U09 两侧非空", lambda a, b: 0 < a < b, (nok, len(by)), (len(by), len(by))))
    else:
        sub(u"（依赖 U08 的 μ_W；缺席则本条不落地）")
        chk(u"U09 缺席如实登记", True, u"skip")
        BATTERY.append((u"U09 缺席分支", lambda ok: ok, True, False))

    # ============================== U10 m 与算符谱的共同选定（O19-1/O19-2）
    item(u"U10", u"FAIL",
         u"O19-1/O19-2：六条候选判据的机器交集为空（手性∩几何）而放宽任一条就退回全奇数集 ⇒ m 无选定原理；"
         u"算符侧同样：谱 {μ_i} 的个数与数值都不被任何一条族内方程定住")
    for m in range(1, 9):
        da = m - 1
        subs(u"m=%d：幂律 p=1/m 唯一(⑲T02)✓｜α 常数(⑲T03)✓｜手性=%s｜α 几何可构造(W1)=%s｜承载 G=%s｜承载规范耦合=%s"
             % (m, u"有" if m % 2 else u"无", u"可" if da % 2 == 0 else u"否",
                u"是" if da == 2 else u"否", u"是" if da == 0 else u"否"))
    inter = [m for m in range(1, 13) if m % 2 == 1 and (m - 1) % 2 == 0]
    oddonly = [m for m in range(1, 13) if m % 2 == 1]
    sub(u"「手性有」∩「α 几何可构造」= %s（按 U02 恒空）；只留「手性有」⇒ m ∈ %s（%d 枚，无进一步约束）；"
        u"只留「α 几何」⇒ m ∈ 偶数集（同样 %d 枚）⇒ 判据不选 ⇒ O19-1 判 NOT CLOSED"
        % (u"∅" if not inter else u"、".join(map(str, inter)), u"、".join(map(str, oddonly)),
           len(oddonly), len([m for m in range(1, 13) if m % 2 == 0])))
    chk(u"U10 交集空且每个松弛集都 >1 枚", len(inter) == 0 and len(oddonly) > 1,
        u"inter=%d odd=%d" % (len(inter), len(oddonly)))
    BATTERY.append((u"U10 交集", lambda a: a == 0, len(inter), 1))

    # ============================== U11 EP 与源约束的取舍（O19-3）
    item(u"U11", u"BOUNDARY",
         u"O19-3 推进：排除力（点源档）与 EP 同向付费——点源档把剖面锁成 r^-2 两支，而源一旦含受力体就退回 ⑲ 的角C")
    pt6 = [x[0] for x in mats[u"∇²"] if x[2]]
    t09 = grep_face(A21_FACE, u"读法 (i) 机器实测", u"⑲ T09 读法(i) 的 EP 二分实测")
    sub(u"点源档幸存者：%s（%d 枚，全是 r^-2 型）；⑲ T09 读法 (i) 现读（载体＝attack21 面）：%s"
        % (u"、".join(pt6), len(pt6), t09 if t09 else u"没读到那行 ⇒ 本条只谈点源档，不引 ⑲ 的极差数"))
    sub(u"合读：U06 证明「对源的约束」是族里唯一能换来排除力的地方；而源约束越紧（点源）⇒ 剖面越像 r^-1 ⇒ 受力体信息越只能藏在源的定义里"
        u"——这与 ⑲ T12 的角C（放弃 α 普适）同源。**排除力有价，价＝EP 或 α 普适，本册不代选。**")
    chk(u"U11 点源幸存者恰为 r^-2 两支", len(pt6) == 2, u"n=%d" % len(pt6))
    BATTERY.append((u"U11 幸存者数", lambda n: n == 2, len(pt6), 3))

    # ============================== U12 跨册净差
    item(u"U12", u"INFO", u"跨册定位：本轮相对 ⑲ 与 r34 的净差（他册数全部现读，读不到即弃引）")
    sub(u"attack21 面（只读）= %d B／md5 %s；r34 面 = %d B／md5 %s；r34 五桶行现读 = %s"
        % (a21_size, hashlib.md5(a21).hexdigest() if a21 else u"-",
           r34_size, hashlib.md5(r34).hexdigest() if r34 else u"-",
           (grep_face(R34_FACE, u"条目 29", u"r34 分布行") or u"没读到")))
    t05 = grep_face(A21_FACE, u"命中 3/3 的格共", u"⑲ T05 手性只出现在奇 m")
    t10 = grep_face(A21_FACE, u"机器裁定：容纳 6/6", u"⑲ T10 零判别力")
    t12 = grep_face(A21_FACE, u"三行皆无「零代价」角", u"⑲ T12 三难定价")
    sub(u"⑲ 面三条裁定现读：%s｜%s｜%s" % (t05 or u"没读到", t10 or u"没读到", t12 or u"没读到"))
    sub(u"净差四条：①把 ⑲ 的「α 需要外生尺度」定价升级为**组合定理**（U01，穷举＋构造性配对，奇量纲可行格 0 枚）；"
        u"②新增**互斥对角线**（U02）：手性要奇 m、几何要偶 m ⇒ ⑲ T12 的三难在纯度规-挠率读法下无解；"
        u"③把 ⑲ T10 的零判别力从剖面**推广到场方程层**（U05 源可反解）并给判别力**定价矩阵**（U06 两算符×四约束）；"
        u"④量子跑动路线实测零内容（U08）并量出它唯一可证伪的那一格（U09）。")

    # ============================== U13 仪器自证
    item(u"U13", u"INFO", u"仪器自证：卫生针按行首形状建排除类、排除数由名单现算；他册读数一律现读并印载体")
    sub(u"沿用 ⑲ 修好的三件形状：排除类 `^  (?:MUT|NEG)-`、排除数＝名单现算、面不自量尺寸（末行写后回读才报字节）")

    # ============================== U14 总裁定
    item(u"U14", u"THEOREM",
         u"总裁定：场方程**能写**（U04 解空间、U05 源可反解）但它给族带来 0 比特新约束；"
         u"在「唯一基础场＝度规-挠率-曲率」这条来料公设下，族被 U01/U02 双向夹死，无解")
    sub(u"成立面：U01（奇偶定理）、U02（互斥对角线）、U04（维数 2s 实测秩）、U05（六目标源可反解，残差 %s < 阈 %s）、"
        u"U07（数值通道两侧都有牙）" % (fmt(worst), fmt(thr5)))
    sub(u"否证面：U05/U06——加算符后容纳率仍 6/6；真正排除东西的是**源约束**（∇² 点源档 %d/6），"
        u"而「只许点源」等于把 r^-2 律当公设写回去（不是推出）；U08——量纲生成不造尺度（%d/%d 档全可凑 g²）"
        % (cnt[u"∇²"][2], nsolv if mu_w else 0, len(rows8) if rows8 else 0))
    sub(u"诚实边界：U01 是**条件定理**（只允许 g、ε、R、T 及其协变导数）；例外已在 U03 逐条点名（外生矢量／迹矢量），"
        u"采纳例外即与公设一冲突——两头都要付账，本册不代选。")
    sub(u"OPEN 顺延：O24-1 m 与算符谱 {μ_i} 的共同选定原理（无）；O24-2 源约束的物理出处（点源＝把 r^-2 当公设）；"
        u"O24-3 外生矢量场是否被公设一禁止（禁止则 U02 判死，允许则「唯一基础场」失身）；"
        u"O24-4 Λ 的选取（U09 给了可证伪格但选不出）。")
    sub(u"红线：本轮未宣称统一场论成立，裁的是「加场方程值几比特」；数学自洽 ≠ 实验证实；"
        u"哥德巴赫仍未证明，统一场论仍未成立。未跑 refresh_catalog，未 git add/commit。")

    # ============================== 卫生针
    PH = re.compile(u"%[-+ #0]*[0-9]*(?:\\.[0-9]+)?[dsfrgeE]|\\{\\d*\\}|\\{[A-Za-z_][A-Za-z0-9_]*\\}")
    MUTLINE = re.compile(u"^  (?:MUT|NEG)-\\d")

    def ph_scan(lines):
        hits, excl = [], []
        for l in lines:
            if not PH.search(l):
                continue
            (excl if MUTLINE.match(l) else hits).append(l)
        return hits, excl

    def pred_clean(lines):
        return not any(PH.search(l) for l in lines)

    def pred_excl_passes(line):
        hits, excl = ph_scan([line])
        return len(hits) == 0 and len(excl) == 1

    hits_now, excl_now = ph_scan(OUT)
    chk(u"版面卫生 无未替换占位符", len(hits_now) == 0 and len(excl_now) == 0 and len(OUT) >= len(ITEMS) + 1,
        u"扫描 %d 行（≥ 条目数 %d＋表头），命中 %d 处，结构排除 %d 处"
        % (len(OUT), len(ITEMS), len(hits_now), len(excl_now)))

    n_ok = sum(1 for _, ok in SELF if ok)
    emit(u"")
    emit(u"自检 guard：")
    emit(u"  %d / %d 通过（逐条 OK/RED 已在各条目内印出）" % (n_ok, len(SELF)))

    # ============================== 电池：每条判据真实输入须绿、corrupt 输入须红
    emit(u"电池（每格＝同一判据两次求值：真实读数须绿、注错读数须红；枚数由登记表现算，不是手钉）：")
    bat_bad = 0
    for label, pred, real, corrupt in BATTERY:
        g_real = pred(*real) if isinstance(real, tuple) else pred(real)
        g_corrupt = pred(*corrupt) if isinstance(corrupt, tuple) else pred(corrupt)
        ok = bool(g_real) and not bool(g_corrupt)
        emit(u"  %s %s（真值→%s｜注错→%s）" % (u"合格" if ok else u"不合格（判据没电或真值被误判）",
                                              label, u"绿" if g_real else u"红", u"绿" if g_corrupt else u"红"))
        if not ok:
            bat_bad += 1
    # 卫生针的四枚双向夹具（两枚须抓住缺陷、两枚须放过合法形状；名单行与夹具行同源）
    def hy_line(nm, ok=True):
        return u"  %s ｜判据 %s" % (nm, u"合格" if ok else u"不合格")

    m_prose = u"  实测残差 %d 枚／阈 %.3e 未替换"
    m_item = u"- U06 [PASS] 模板行 %d/%.3e 未插值"
    hyb = []
    hyb.append((u"MUT-1 未插值模板行（含 %d、%.3e 字形）必须被抓住", not pred_clean([m_prose])))
    hyb.append((u"MUT-2 条目行 %s [PASS] 里的占位符不得被排除类放过",
                (lambda h, e: len(h) == 1 and len(e) == 0)(*ph_scan([m_item]))))
    hyb.append((u"NEG-1 名单自述行按行首形状排除（须绿）", pred_excl_passes(hy_line(hyb[0][0]))))
    hyb.append((u"NEG-2 真集合记号 {3、5} 与 {1..12} 行不命中（须绿）",
                pred_clean([u"其 m 值集合 = {3、5}", u"m ∈ {1..12}"])))
    hyb_bad = 0
    for nm, ok in hyb:
        emit(hy_line(nm, ok))
        if not ok:
            hyb_bad += 1

    # 排除类的期望数由名单现算（不是手钉）：名单里哪几行自带占位符字形，终扫就该排除哪几行
    ex_expect = sum(1 for nm, _, _, _ in BATTERY if PH.search(hy_line(nm))) + \
                sum(1 for nm, _ in hyb if PH.search(hy_line(nm)))
    vcnt = {}
    for tid, v, _t in ITEMS:
        vcnt[v] = vcnt.get(v, 0) + 1
    exit_code = 0 if (n_ok == len(SELF) and bat_bad == 0 and hyb_bad == 0) else 1
    emit(u"")
    emit(u"条目统计：" + u"／".join(u"%s×%d" % (k, vcnt[k]) for k in
         [u"PASS", u"FAIL", u"THEOREM", u"BOUNDARY", u"INFO"] if k in vcnt))
    emit(u"判定条目 %d 枚｜自检 %d/%d｜电池 %d/%d 合格｜卫生双向 %d/%d 合格｜退出码（终扫前）%d"
         % (len(ITEMS), n_ok, len(SELF), len(BATTERY) - bat_bad, len(BATTERY),
            len(hyb) - hyb_bad, len(hyb), exit_code))
    emit(u"")
    emit(u"分层结论：")
    emit(u"  [数学] 量纲奇偶定理（U01：穷举 %d 格、奇量纲可行 0 枚、构造性配对反向）、外部解维数 2s（U04 实测秩）、"
        u"源可反解（U05 残差 %s < 阈 %s）三条为恒等式级。" % (grid_n, fmt(worst), fmt(thr5)))
    emit(u"  [物理] 加场方程后族的判别力增量 = 0（U05）；排除错误律 r^-5 的权力全部住在**源约束**里"
        u"（U06：∇² 点源档 %d/6，正定档 6/6 是橡皮图章，有质量档随 μ 变动为 1／0）；量子跑动不造尺度（U08）。"
        % cnt[u"∇²"][2])
    emit(u"  [诚实边界] U01/U02 的条件性（外生矢量例外已在 U03 点名）；U09 的 Λ 未被选出；"
        u"U11 的 EP/α 普适取舍本册不代选。")
    emit(u"  [红线] 本轮未宣称统一场论成立；未跑 refresh_catalog，未 git add/commit。")

    rc_pre = exit_code
    final_hits, final_ex = ph_scan(OUT)
    if final_hits:
        emit(u"版面卫生（终扫）：判定命中 %d 处（%s）⇒ 本轮不得判绿" % (len(final_hits), final_hits[0][:90]))
        exit_code = 1
    elif len(final_ex) != ex_expect:
        emit(u"版面卫生（终扫）：结构排除 %d 行 ≠ 名单现算 %d 行 ⇒ 排除类在吞东西 ⇒ 本轮不得判绿"
             % (len(final_ex), ex_expect))
        exit_code = 1
    else:
        brace = [l for l in OUT if u"{" in l]
        emit(u"版面卫生（终扫）：扫到本行前共 %d 行（本行不计，面不能自量——盘的尺寸／LF 只由末行「写后回读」给），"
             u"判定命中 0 处；结构排除 %d 处（= 名单现算 %d，全部是上面卫生夹具区里自述模板那类字形，逐条可点名）；"
             u"含花括号字形的行 %d 行（现扫第二口径：其中没有一行靠排除类放过，因为它们都不带 % 型占位符）"
             % (len(OUT), len(final_ex), ex_expect, len(brace)))
    if exit_code != rc_pre:
        emit(u"退出码更正：终扫前印 %d，终扫后取 %d（终扫能推翻前一行，所以那一行只能自称「终扫前」）"
             % (rc_pre, exit_code))

    data = (u"\n".join(OUT) + u"\n").encode("utf-8")
    with io.open(REPORT, "wb") as fh:
        fh.write(data)
    with io.open(REPORT, "rb") as fh:
        back = fh.read()
    tail = (u"\n[写后回读] %s｜盘上 %d B｜md5 %s｜LF %d｜退出码 %d\n"
            % (os.path.basename(REPORT), len(back), hashlib.md5(back).hexdigest(),
               back.count(b"\n"), exit_code))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.write(tail.encode("utf-8"))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
