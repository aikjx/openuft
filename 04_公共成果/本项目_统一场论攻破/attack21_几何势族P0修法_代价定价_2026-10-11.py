# -*- coding: utf-8 -*-
"""
attack21｜几何势族 `U = α(κ^m − τ^m)` 的 P0 修法构造与代价定价（攻破⑲）
=====================================================================
靶：r34 册《判定_TUFT-r34-V41alpha自然单位势_全维审计》判死的那批条目
    （X05b 幂次、X06 量纲 0/4、X07 符号 2/3、X08 手性被平方消、X09 等效原理、
      X13 力程、X16 无禁闭、X21/X22 反向拟合与零判别力）。
本轮不做文本审计，做**正面构造**：把主方程的幂次 m 从「来料取的 2」放开成整族参数，
    逐条问「这条 FAIL 是 m=2 的特异病，还是全族的病？」并给机器答案。

攻击目标（V1–V6）
  V1 幂次缺陷可否修：单幂剖面 κ=A r^{-p} 下 F ∝ r^{-(mp+1)}，观测定 r^{-2} ⇒ p=1/m 唯一。
  V2 α 可否真为常数：来料要 α ∝ r（r34 X11 跨 1.5e11 倍），修复族是否把该散布压回 1。
  V3 符号与手性可否有载体：m 奇时 τ→−τ 是否翻转可观察力（来料 m=2 判 0）。
  V4 四力耦合的量纲承载：单一 [α]=L^{m-1} 能否同时是 G（L^2）与规范耦合（L^0）。
  V5 禁闭可否在族内构造：常力吸引需要 U=+σr，族的符号结构允许吗。
  V6 代价：修复后的族还剩多少物理内容——对「任意有心律」的容纳率与对「非有心律」的容纳率。

体例：纯标准库（math / fractions / os / re / sys / hashlib）；零随机；判定条目 T01–T14；
      自检 guard 全过 **且** 5 枚变异体全红 **且** 5 枚阴性对照全绿才退 0；
      运行报告落 `attack21_*_report.txt`（本册数值唯一载体，含本面自身的字节/md5 只印在 stdout 不落面）。
      他册读数一律**现读盘**，读不到就印「没读到」，不许凭会话记忆转抄。
阈值纪律：凡「相对偏差 < 阈」型判据，阈一律由该条的截断项 (h/r)² 与相消噪声 eps/(2h/r) 现推并印出（T02/T07/T08/T09）。
"""
import hashlib
import math
import os
import re
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "attack21_几何势族P0修法_代价定价_2026-10-11_report.txt")
# r34 审计面（同仓另一项目，只读）；路径不存在时相关条目印「没读到」，不得引用
R34_FACE = os.path.join(HERE, os.pardir, u"本项目_全维自洽与归一化",
                        u"数据", u"TUFT-V41alpha自然单位势_全维审计_2026-10-10.md")

ITEMS = []      # (id, verdict, title)  —— 自然单位下 [α]=L^(m-1) 由 T01 现推
SELF = []       # (name, ok)
OUT = []


def emit(s=u""):
    OUT.append(s)


def item(tid, verdict, title):
    ITEMS.append((tid, verdict, title))
    emit(u"- %s [%s] %s" % (tid, verdict, title))


def sub(s):
    emit(u"  " + s)


def chk(name, ok, detail=u""):
    SELF.append((name, bool(ok)))
    emit(u"  [自检] %-34s %s%s" % (name, u"OK" if ok else u"RED", (u"  " + detail) if detail else u""))


# ---------------------------------------------------------------------
# 通用数值小件
# ---------------------------------------------------------------------
def cderiv(f, x, h):
    """中心差分（步长 h 由调用方按尺度给，收敛因子现推，不硬编）。"""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def force_of_U(alpha, m, kappa, tau, r, h):
    """F_r = -dU/dr, U = alpha*(kappa^m - tau^m)，剖面以 lambda 传入。数值版。"""
    def U(rr):
        return alpha * (kappa(rr) ** m - tau(rr) ** m)
    return -cderiv(U, r, h)


def read_r34_token(key):
    """现读 r34 面里 `key=value` 的字符串值；读不到返回 None（该条不得引用他册数）。"""
    try:
        p = os.path.normpath(R34_FACE)
        raw = open(p, "rb").read().decode("utf-8", "replace")
    except Exception:
        return None, None
    mm = re.search(re.escape(key) + u"=([0-9eE+.\\-]+)", raw)
    return (mm.group(1) if mm else None), os.path.normpath(p)


# ---------------------------------------------------------------------
# T01 族的主方程与量纲恒等式
# ---------------------------------------------------------------------
emit(u"=" * 78)
emit(u"attack21｜几何势族 U = α(κ^m − τ^m) 的 P0 修法构造与代价定价（攻破⑲）")
emit(u"=" * 78)
item(u"T01", u"INFO", u"族设定：[κ]=[τ]=L^-1、[U]=L^-1、[F]=L^-2（自然单位）⇒ [α]=L^(m-1) 由量纲恒等式定死")
sub(u"恒等式：[α] = [U] - m[κ] = (-1) - m*(-1) = m - 1。m=2（来料）=> [α]=L^1，与其 §二 自述一致。")
sub(u"本轮把 m 当**可调参数**（不是来料的既定事实），后续每条判定都问：这病是 m=2 特有还是全族皆有。")
for m in range(1, 7):
    sub(u"  m=%d => [α]=L^%d, 单幂剖面的观测律解 p=1/m=L^(-%d/%d) 幂, [κ^m]=L^%d"
        % (m, m - 1, 1, m, -m))
# 量纲恒等式的自检：两条独立路径（势能路 vs 力路）
_alpha_from_U = {}
_alpha_from_F = {}
for m in range(1, 7):
    _alpha_from_U[m] = (-1) - m * (-1)            # 势能路：[α] = [U] − m[κ]
    _alpha_from_F[m] = (-2) - ((-1) + m * (-1))   # 力路：  [α] = [F] − [∇] − m[κ]
chk(u"T01 两路 [α] 恒等（m=1..6）",
    all(_alpha_from_U[m] == _alpha_from_F[m] == m - 1 for m in range(1, 7)),
    u"势能路=%s 力路=%s" % ([_alpha_from_U[m] for m in range(1, 7)], [_alpha_from_F[m] for m in range(1, 7)]))

# ---------------------------------------------------------------------
# T02 V1：幂次缺陷的解唯一性
# ---------------------------------------------------------------------
item(u"T02", u"PASS", u"V1 幂次可修：单幂剖面下 F ∝ r^-(mp+1)，观测定律 r^-2 ⇒ p=1/m 是唯一解（Fraction 精确）")
sub(u"推导：κ=A r^-p ⇒ U=αA^m r^-(mp) ⇒ |F| = m·p·α·A^m·r^-(mp+1)。令 mp+1=2 ⇒ p=1/m（无第二条根）。")
sub(u"来料取 m=2 而写 p=1（κ∝M/r）⇒ mp+1=3 ⇒ r^-3，正是 r34#X05b 的跳步；修法是把 p 改成 1/m（不是改 α）。")
for m in (1, 2, 3, 4, 6):
    p = Fr(1, m)
    sub(u"  m=%d => p=%s（mp+1=%s，与观测律幂 -%s 逐位同）"
        % (m, str(p), str(m * p + 1), str(m * p + 1)))
# 数值对拍：解析 -d/dr 与中心差分，收敛因子由步长比现推
_m, _A, _alpha = 3, 2.0, -1.5
_k = lambda r: _A * r ** (-Fr(1, _m))
_tau0 = lambda r: 0.0
# p=1/m 时 mp=1 ⇒ |F| = m·p·αA^m r^-2 = αA^m r^-2（m 与 p 相消，闭式与 m 无关）
_analytic = lambda r: _alpha * _A ** _m * r ** (-2.0)
_r = 7.3
_h1, _h2 = _r * 1e-4, _r * 1e-5
_n1 = force_of_U(_alpha, _m, _k, _tau0, _r, _h1)
_n2 = force_of_U(_alpha, _m, _k, _tau0, _r, _h2)
_e1 = abs(_n1 - _analytic(_r)) / abs(_analytic(_r))
_e2 = abs(_n2 - _analytic(_r)) / abs(_analytic(_r))
_fac = _e1 / _e2 if _e2 > 0 else float(u"inf")
# 阈的来路：对 U=c/r，中心差分的截断主项 = (h/r)²（系数精确为 1），相消噪声主项 = eps/(2·(h/r))
_t1, _t2 = (1e-4) ** 2, (1e-5) ** 2
_n1p, _n2p = 2.2e-16 / (2.0 * 1e-4), 2.2e-16 / (2.0 * 1e-5)
_pred1, _pred2 = _t1 + _n1p, _t2 + _n2p
_pred_fac = _pred1 / _pred2
sub(u"数值对拍（m=3, A=2.0, α=-1.5, r=7.3）：解析 F_r=%.6g；相对残差 h=r·1e-4 => %.3e；h=r·1e-5 => %.3e；实测因子 %.4f"
    % (_analytic(_r), _e1, _e2, _fac))
sub(u"误差模型（阈由它现推，不手钉）：截断 (h/r)² + 相消噪声 eps/(2h/r) ⇒ 预测残差 %.3e / %.3e、预测因子 %.2f；"
    u"实测残差/预测 = %.2f 与 %.2f ⇒ 二者同量级，因子偏离 100 是小步长处噪声占比上升所致（模型已含）。"
    % (_pred1, _pred2, _pred_fac, _e1 / _pred1, _e2 / _pred2))
chk(u"T02 解析=差分且残差受二阶+噪声模型约束",
    _e2 < 3.0 * _pred2 and _e1 < 3.0 * _pred1 and _fac > 20.0,
    u"resid2=%.3e pred2=%.3e factor=%.4f pred_factor=%.2f" % (_e2, _pred2, _fac, _pred_fac))

# ---------------------------------------------------------------------
# T03 V2：α 的常数性——修复族把 1.5e11 散布压回 1
# ---------------------------------------------------------------------
item(u"T03", u"PASS", u"V2 α 可真为常数：p=1/m 时 α = C/A^m 与 r 无关；来料 p=1 时 α(r) ∝ r")
sub(u"设目标律 |F|=C r^-2。一般反解：α = C/(m·p·A^m r^(mp-1))。")
sub(u"来料写法（m=2, p=1）⇒ mp-1=1 ⇒ α(r) = C r/(2A²) ⇒ **随 r 线性**（撞 r34#X11(a) 的跨量级散布）。")
sub(u"修复写法（p=1/m）⇒ mp-1=0 且 m·p=1 ⇒ α = C/A^m ⇒ **与 r 无关**，闭式即常数。")
_C, _A2 = 1.0, 0.5
_rs = [1.0, 1e3, 1e6, 1.495978707e11]      # 1 m … 1 AU
_alpha_naive = [_C * r / (2.0 * _A2 ** 2) for r in _rs]
_spread_naive = max(_alpha_naive) / min(_alpha_naive)
_alpha_fixed = [_C / (_A2 ** 2) for _r_ in _rs]
_spread_fixed = max(_alpha_fixed) / min(_alpha_fixed)
sub(u"r 网格（m）= 1 / 1e3 / 1e6 / 1.49598e11（=1 AU）")
sub(u"来料 p=1 所需 α(r) = %s ⇒ 散布 %.6g" % (u"／".join(u"%.6g" % v for v in _alpha_naive), _spread_naive))
sub(u"修复 p=1/m 所需 α(r) = %s ⇒ 散布 %.6g" % (u"／".join(u"%.6g" % v for v in _alpha_fixed), _spread_fixed))
_v_r34, _r34_path = read_r34_token(u"alpha_r_spread")
if _v_r34 is None:
    sub(u"对照 r34 面 alpha_r_spread：**没读到**（该文件不在盘上或键名已变，本条不得引用他册数）")
else:
    sub(u"对照 r34 面 alpha_r_spread=%s（现读 %s）⇒ 本轮同数量级复算 %.6g，比值 %.6g"
        % (_v_r34, os.path.basename(_r34_path), _spread_naive, _spread_naive / float(_v_r34)))
chk(u"T03 修复族散布为机器 1、来料族散布跨 11 量级",
    abs(_spread_fixed - 1.0) < 1e-12 and _spread_naive > 1e10,
    u"fixed=%.17g naive=%.6g" % (_spread_fixed, _spread_naive))

# ---------------------------------------------------------------------
# T04 V4：[α]=L^(m-1) 对四类耦合的承载率 ⇒ 4/4 不可能（对一切 m）
# ---------------------------------------------------------------------
item(u"T04", u"THEOREM", u"V4 单一 α 不能既为 G 又为规范耦合：最佳 3/4，4/4 对一切 m 不可能")
sub(u"自然单位：[G]=L^+2；[k]=[g_w]=[g_s]=L^0。承载条件 = m-1 == 目标幂。")
_targets = [(u"G", 2), (u"k(U1)", 0), (u"g_w(SU2)", 0), (u"g_s(SU3)", 0)]
_best = (0, None)
_even_best = (0, None)
for m in range(1, 8):
    hits = [nm for nm, pw in _targets if pw == m - 1]
    sub(u"  m=%d（%s）⇒ [α]=L^%d ⇒ 命中 %d/4 %s" % (m, u"奇" if m % 2 else u"偶", m - 1, len(hits),
                                                    (u"／".join(hits) if hits else u"（无）")))
    if len(hits) > _best[0]:
        _best = (len(hits), m)
    if m % 2 == 0 and len(hits) > _even_best[0]:
        _even_best = (len(hits), m)
sub(u"机器裁定：max 命中 = %d/4（在 m=%d，奇）；偶 m 侧 max = %d/4 ⇒ 角A（要偶 m）在量纲上是**全空**（见 T12）。"
    u"因 G 与规范耦合差 L^2，任何单一 m 都无法两全 ⇒ r34#X06 的 0/4 升级为「对全族不可能」。"
    % (_best[0], _best[1], _even_best[0]))
sub(u"注：m=3 有 [α]=L^2=[G]（唯一与引力同维的支），m=1 有 [α]=L^0=[规范耦合]；两者互斥。")
chk(u"T04 无任一 m 达 4/4 且 best=3/4", _best[0] == 3 and _best[1] == 1,
    u"best=(%d, m=%d)" % _best)

# ---------------------------------------------------------------------
# T05 V3：符号三条件的**机器全枚举**（m 奇偶 × α 号 × 引力/电磁各走哪一支）
#     枚举口径：κ 项贡献 U = +α·(振幅·r^-1/m)^m，τ 项贡献 U = −α·(振幅·r^-1/m)^m；
#     电磁振幅带 q1q2 的号（同号 +、异号 −），引力振幅只取正号（质量恒正）。
# ---------------------------------------------------------------------
item(u"T05", u"PASS", u"V3 符号与手性可修：枚举 40 格（m∈{2..6}×α 号×两支归属）里 3/3 支**存在且只出现在奇 m**；偶 m 结构上限 2/3（r34#X07 的 2/3 是 m=2 切片）")
sub(u"三条自然要求：N1 引力吸引(F_r<0)；N2 电磁同号排斥(F_r>0)；N3 电磁异号吸引(F_r<0)。")
sub(u"枚举空间 = m∈{2,3,4,5,6} × sign(α)∈{+,-} × 引力支∈{κ,τ} × 电磁支∈{κ,τ} = 40 格，逐格**数值求力**再判号（不手推符号）。")
_R = 2.0
_H = 1e-5
_nullp = lambda rr: 0.0


def _prof(c, m):
    return lambda rr: c * rr ** (-Fr(1, m))


_rows = []
for m in (2, 3, 4, 5, 6):
    for sa in (+1.0, -1.0):
        for gb in (u"κ", u"τ"):
            for eb in (u"κ", u"τ"):
                kp, tp = (_prof(0.9, m), _nullp) if gb == u"κ" else (_nullp, _prof(0.9, m))
                fg = force_of_U(sa, m, kp, tp, _R, _H)                    # 引力（振幅恒正）
                fe = []
                for s in (+1.0, -1.0):                                    # s = sign(q1·q2)
                    kp2, tp2 = (_prof(s * 0.7, m), _nullp) if eb == u"κ" else (_nullp, _prof(s * 0.7, m))
                    fe.append(force_of_U(sa, m, kp2, tp2, _R, _H))
                n1, n2, n3 = (fg < 0.0), (fe[0] > 0.0), (fe[1] < 0.0)
                _rows.append((m, sa, gb, eb, n1, n2, n3, int(n1) + int(n2) + int(n3), fe[0], fe[1]))
for m in (2, 3, 4, 5, 6):
    rs = [r for r in _rows if r[0] == m]
    full_m = [r for r in rs if r[7] == 3]
    sub(u"  m=%d（%s）：%d 格，最高命中 %d/3，3/3 格 %d 枚，同号/异号力相对差 %.3e"
        % (m, u"奇" if m % 2 else u"偶", len(rs), max(r[7] for r in rs), len(full_m),
           max(abs(r[8] - r[9]) / max(abs(r[8]), 1e-300) for r in rs)))
sub(u"命中 3/3 的全部格（其余 %d 格从略）：" % (len(_rows) - len([r for r in _rows if r[7] == 3])))
for m, sa, gb, eb, n1, n2, n3, sc, f_like, f_unlike in _rows:
    if sc != 3:
        continue
    sub(u"  m=%d α%s0 引力%s支 电磁%s支 ⇒ N1N2N3 全满足｜F(同号)=%+.6g F(异号)=%+.6g（差 = 手性载体）"
        % (m, u">" if sa > 0 else u"<", gb, eb, f_like, f_unlike))
_full = [r for r in _rows if r[7] == 3]
_even_max = max(r[7] for r in _rows if r[0] % 2 == 0)
_even_gap = max(abs(r[8] - r[9]) / max(abs(r[8]), 1e-300) for r in _rows if r[0] % 2 == 0)
_odd_gap = max(abs(r[8] - r[9]) / max(abs(r[8]), 1e-300) for r in _rows if r[0] % 2 == 1)
sub(u"机器裁定：命中 3/3 的格共 %d 枚，其 m 值集合 = {%s}（枚举域 m∈{2..6} 内**只有奇数**）；"
    % (len(_full), u"、".join(str(v) for v in sorted(set(r[0] for r in _full)))))
sub(u"          同号/异号力之差：偶 m 的相对差最大 %.3e（= 机器零 ⇒ τ→−τ 是势的严格对称，手性无载体，与 r34#X08 同因）；"
    u"奇 m 的相对差最小 %.3e（非零 ⇒ 手性有载体）。" % (_even_gap, _odd_gap))
sub(u"          偶 m 的最高命中 = %d/3（N3 与 N2 落在同一个数值上，不可同时满足）——故 r34#X07 的 2/3 不是「再来料改个符号就好」，"
    u"而是**偶次幂的结构上限**。" % _even_max)
_comeiao_same = [r for r in _full if r[2] == u"κ" and r[3] == u"τ"]
_comeiao_swap = [r for r in _full if r[2] == u"τ" and r[3] == u"κ"]
sub(u"与来料分支的比对：来料 §四.1 引力走 κ、§四.2 电磁走 τ。3/3 格里沿用来料分支的 %d 枚（条件：α<0 且 m 奇，**无需换支**），"
    u"须换支的 %d 枚（引力 τ、电磁 κ、α>0）⇒ 符号修复不逼来料改判分支归属，但逼它把 α 取负"
    u"（来料 §二 称 α 统一包含 G、k/g_w/g_s，而引力定常量的吸引面按约定为正）⇒ 这是符号账，不是量纲账。"
    % (len(_comeiao_same), len(_comeiao_swap)))
sub(u"m=3 顺带命中 [α]=L^2=[G]（T04 表）⇒ 符号修复与引力量纲同支；但同一 m 无法再载规范耦合。")
chk(u"T05 3/3 支存在且全为奇次、偶次上限 2/3 且同号=异号",
    len(_full) > 0 and all(r[0] % 2 == 1 for r in _full) and _even_max == 2
    and _even_gap < 1e-12 and _odd_gap > 1e-3,
    u"full=%d even_max=%d even_gap=%.3e odd_gap=%.3e" % (len(_full), _even_max, _even_gap, _odd_gap))

# ---------------------------------------------------------------------
# T06 手性载体的直接见证：sign(τ) 是否进入可观察量
# ---------------------------------------------------------------------
item(u"T06", u"PASS", u"手性见证：同一网格上 m=2 给逐位零差、m=3 给非零差（针没坏，正对照同网格）")
_B, _al = 1.7, -1.0
_rg = [0.4, 1.0, 2.5, 6.0, 13.0]
_h = 1e-5
diffs = {}
for m in (2, 3):
    mx = 0.0
    for r in _rg:
        kp = lambda rr: 0.9 * rr ** (-Fr(1, m))
        tp_p = lambda rr: _B * rr ** (-Fr(1, m))
        tp_n = lambda rr: -_B * rr ** (-Fr(1, m))
        fp = force_of_U(_al, m, kp, tp_p, r, _h)
        fn = force_of_U(_al, m, kp, tp_n, r, _h)
        mx = max(mx, abs(fp - fn))
    diffs[m] = mx
sub(u"max_r |F(τ) − F(−τ)|：m=2 => %.3e；m=3 => %.6g（同一网格、同一 α、同一差分步长）" % (diffs[2], diffs[3]))
sub(u"判读：偶次幂把手征严格消掉（差落在机器零量级，与 r34#X08 的零读数同型）；奇次幂给有限差 ⇒ 手性有载体。")
sub(u"这同时说明：来料 §四.2「吸引/排斥由挠率拓扑手性符号区分」这句话**在 m=2 下空、在 m 奇下可兑现**。")
chk(u"T06 偶次零差 + 奇次非零差（正对照）", diffs[2] < 1e-14 and diffs[3] > 1e-3,
    u"even=%.3e odd=%.6g" % (diffs[2], diffs[3]))

# ---------------------------------------------------------------------
# T07 V5：禁闭可在族内构造（常力吸引）
# ---------------------------------------------------------------------
item(u"T07", u"PASS", u"V5 禁闭可构造：把线性上升项放 τ 支（α<0）⇒ U=+σr ⇒ F_r=−σ 恒吸引；r34#X16 是剖面选择非族障碍")
_sig, _al2, _mm = 0.83, -1.0, 3
_tau_lin = lambda r: ((_sig * r) / (-_al2)) ** Fr(1, _mm)
_kp0 = lambda r: 0.0
_r7 = [1.0, 3.0, 10.0, 100.0, 1e4]
# 步长随 r 取相对值：线性势的差分相消噪声 ~ ε·|U|/(2h|U'|) = ε/(2·相对步长)，绝对步长在 r=1e4 处会假红
_fr = [force_of_U(_al2, _mm, _kp0, _tau_lin, r, r * 1e-5) for r in _r7]
_dev = max(abs(v + _sig) / _sig for v in _fr)
_noise_floor = 2.2e-16 / (2.0 * 1e-5)      # 由本条步长现推的相消噪声标度（阈不许凭手感钉）
sub(u"构造：τ^m = σr/(−α)（α<0 ⇒ 右端非负，τ 实）⇒ U = −ατ^m = +σr。")
sub(u"机器：F_r = %s ⇒ 与 −σ=%.17g 的最大相对偏差 %.3e（r 跨 %s，步长 h=r·1e-5）"
    % (u"／".join(u"%.6g" % v for v in _fr), -_sig, _dev, u"／".join(u"%.4g" % v for v in _r7)))
sub(u"阈的来路：本条差分相消噪声标度 = eps/(2·相对步长) = %.3e ⇒ 判据阈取 100 倍 = %.3e（不是手选的 1e-10）。"
    % (_noise_floor, 100 * _noise_floor))
sub(u"对照来料 §四.4 的 τ∝σ r e^-(r/r0)：该式在 r=r0 处使力归零、r>r0 反号（r34#X16 的三笔账）——")
sub(u"      那是**指数截断剖面的病**；族本身能给 Cornell 的常力支。")
chk(u"T07 常力吸引闭合（偏差 < 现推阈）", _dev < 100 * _noise_floor, u"dev=%.3e thr=%.3e" % (_dev, 100 * _noise_floor))

# ---------------------------------------------------------------------
# T08 弱力程：力程定理（**无量纲口径 x = μr**，避免米尺度与差分步长不同源）
# ---------------------------------------------------------------------
item(u"T08", u"THEOREM", u"力程定理：族内剖面取 μ 则 U 取 mμ ⇒ 超出 m 的衰减部分实测 = (mx+2)/[x(mx+1)] ~ 1/x；r34#X13 的 2 倍差是 m=2 切片")
sub(u"无量纲化：取 μ=1、x=μr。剖面 τ(x)=e^-x·x^-(1/m)、κ=0、α=-1 ⇒ U = τ^m = e^(-m·x)·x^-1。")
sub(u"解析预期：|F| = e^(-mx)(m/x + 1/x²) ⇒ 衰减率 −d ln|F|/dx = m + (m x + 2)/[x(m x + 1)] = m + 1/x + O(x^-2)。")
_X_LO, _X_HI, _HH = 20.0, 80.0, 0.1


def _absF(x, m):
    tp = lambda rr, m=m: math.exp(-rr) * rr ** (-Fr(1, m))
    return abs(force_of_U(-1.0, m, _nullp, tp, x, 1e-4))


def _excess(x, m, hh):
    dln = (math.log(_absF(x + hh, m)) - math.log(_absF(x - hh, m))) / (2.0 * hh)
    return -dln - m


_rate = {}
for m in (2, 3, 4):
    row = {}
    for x in (_X_LO, _X_HI):
        ana = (m * x + 2.0) / (x * (m * x + 1.0))            # 解析超出项
        ex = _excess(x, m, _HH)
        ex2 = _excess(x, m, _HH / 2.0)                        # 步长减半：O(hh^2) 截断应使残差缩 4 倍
        ext = ex2 + (ex2 - ex) / 3.0                           # Richardson：ext = (4·ex2 − ex)/3，消 O(hh²)
        row[x] = (ex, ana, abs(ex - ana), abs(ex2 - ana), ext, abs(ext - ana))
    _rate[m] = row
    for x in (_X_LO, _X_HI):
        sub(u"  m=%d x=%-3.0f 超出实测 %.7f｜解析 %.7f｜残差 %.3e｜步长减半残差 %.3e（比值 %.2f）｜外推 %.9f 与解析差 %.3e"
            % (m, x, row[x][0], row[x][1], row[x][2], row[x][3], row[x][2] / row[x][3], row[x][4], row[x][5]))
_worst_resid = max(_rate[m][x][5] for m in _rate for x in _rate[m])
_worst_raw = max(_rate[m][x][2] for m in _rate for x in _rate[m])
_conv_min = min(_rate[m][x][2] / _rate[m][x][3] for m in _rate for x in _rate[m])
_conv_max = max(_rate[m][x][2] / _rate[m][x][3] for m in _rate for x in _rate[m])
_ratio_min = min(_rate[m][_X_LO][0] / _rate[m][_X_HI][0] for m in _rate)
_ratio_max = max(_rate[m][_X_LO][0] / _rate[m][_X_HI][0] for m in _rate)
_ana_ratio_dev = max(abs(_rate[m][_X_LO][0] / _rate[m][_X_HI][0] -
                         ((m * _X_LO + 2.0) / (_X_LO * (m * _X_LO + 1.0))) /
                         ((m * _X_HI + 2.0) / (_X_HI * (m * _X_HI + 1.0)))) for m in _rate)
sub(u"判读：残差不是「定理对不上」，而是 ln|F| 中心差分的 O(hh²) 截断——步长减半残差按 %.2f–%.2f 倍缩小（O(hh²) 期望 4），"
    u"Richardson 外推后与解析式一致到 %.1e。阈由该收敛阶现推，不是手钉。" % (_conv_min, _conv_max, _worst_resid))
sub(u"两窗口对照（x 由 %.0f 放大到 %.0f，即 4 倍）：超出项实测比值 ∈ [%.4f, %.4f]，与解析比值的最大偏离 %.1e ⇒ "
    u"若衰减另有第二支指数，比值会随 m 明显漂移并被这步排除。" % (_X_LO, _X_HI, _ratio_min, _ratio_max, _ana_ratio_dev))
_mu = 80.377 / 1.973269804e-16      # m_W[GeV] -> m^-1（ħc = 197.3269804 MeV·fm）；外部输入，非本册预言
sub(u"物理换算（仅供口径对照，判定不依赖它）：μ_W = %.6g m^-1 ⇒ 标准弱力程 1/μ = %.6g m；"
    u"族在 m=2 下给 1/(2μ) = %.6g m ⇒ 差 2 倍（与 r34#X13 同因）。" % (_mu, 1.0 / _mu, 1.0 / (2 * _mu)))
_v_wm, _wp = read_r34_token(u"weak_range_model_m")
_v_ws, _ = read_r34_token(u"weak_range_std_m")
if _v_wm is None or _v_ws is None:
    sub(u"对照 r34 面 weak_range_*：**没读到**（文件不在盘上或键名已变，本条不引用他册数）")
else:
    sub(u"对照 r34 面现读：weak_range_model_m=%s、weak_range_std_m=%s ⇒ 其比值 %.6f = 本轮定理在 m=2 的切片（现读 %s）"
        % (_v_wm, _v_ws, float(_v_ws) / float(_v_wm), os.path.basename(_wp)))
sub(u"修法与代价：把剖面写成 τ ∝ e^(-(μ_target/m)·r) 才得力程 1/μ_target——")
sub(u"      但这要求**先知道目标力程**，即把答案写进前提（撞 T10 的零判别力），不是从几何反推 m 或 μ。")
chk(u"T08 外推衰减率=解析式 且 残差按 O(hh^2) 收缩 且 超出项按 1/x 塌缩",
    _worst_resid < 1e-8 and _worst_raw > 100 * _worst_resid
    and 3.5 < _conv_min and _conv_max < 4.5 and 3.8 < _ratio_min and _ratio_max < 4.3
    and _ana_ratio_dev < 1e-4,
    u"ext_resid=%.3e raw_resid=%.3e conv∈[%.2f,%.2f] ratio∈[%.4f,%.4f] d_ana=%.1e"
    % (_worst_resid, _worst_raw, _conv_min, _conv_max, _ratio_min, _ratio_max, _ana_ratio_dev))

# ---------------------------------------------------------------------
# T09 等效原理二分：保 EP 则剖面必须含受力体，保几何纯度则 EP 破——两支各测一次
# ---------------------------------------------------------------------
item(u"T09", u"BOUNDARY", u"V-EP 二分：修复族里等效原理不自动——两支各保一样破一样（机器实测 F 极差与 a 极差，本册不代选）")
_PROBES = [(u"e", 0.511), (u"mu", 105.658), (u"tau", 1776.86), (u"p", 938.272)]
_mass_spread = max(mp for _, mp in _PROBES) / min(mp for _, mp in _PROBES)
sub(u"测试体（外部输入，标定值非本册预言）：%s MeV ⇒ 质标极差 = %.6g"
    % (u"／".join(u"%s %.6g" % (nm, mp) for nm, mp in _PROBES), _mass_spread))
_M9, _A0, _R9, _REL9 = 3, 0.7, 5.0, 1e-3
_H9 = _R9 * _REL9
# 读法 (i)：剖面只含**源**量（几何纯度保）⇒ F 与受力体无关 ⇒ a=F/m 随 m 变
_F_i = [abs(force_of_U(-1.0, _M9, lambda rr: _A0 * rr ** (-Fr(1, _M9)), _nullp, _R9, _H9))
        for _ in _PROBES]
_a_i = [f / mp for f, (_, mp) in zip(_F_i, _PROBES)]
_sp_F_i = max(_F_i) / min(_F_i)
_sp_a_i = max(_a_i) / min(_a_i)
# 读法 (ii)：把受力体塞进剖面振幅（A^m ∝ m_probe）⇒ F ∝ m_probe ⇒ a 恒定，但 κ 不再是源的几何不变量
_F_ii = [abs(force_of_U(-1.0, _M9, lambda rr, mp=mp: (_A0 * mp ** (1.0 / _M9)) * rr ** (-Fr(1, _M9)),
                        _nullp, _R9, _H9)) for _, mp in _PROBES]
_a_ii = [f / mp for f, (_, mp) in zip(_F_ii, _PROBES)]
_sp_F_ii = max(_F_ii) / min(_F_ii)
_sp_a_ii = max(_a_ii) / min(_a_ii)
for (nm, mp), fi, fii in zip(_PROBES, _F_i, _F_ii):
    sub(u"  测试体 %-4s m=%-9.6g MeV ⇒ (i) F=%+.6g a=%+.6g｜(ii) F=%+.6g a=%+.6g" % (nm, mp, fi, fi / mp, fii, fii / mp))
sub(u"读法 (i) 机器实测：F 极差 = %.17g（**逐位与受力体无关**，因为剖面里没有它）⇒ a 极差 = %.6g = 质标极差 %.6g ⇒ EP 破，几何保。"
    % (_sp_F_i, _sp_a_i, _mass_spread))
sub(u"读法 (ii) 机器实测：F 极差 = %.6g（正比于受力体质量）⇒ a 极差 = %.17g（机器 1）⇒ EP 保，"
    u"但「唯一基础场 = 时空几何」的公理失身（剖面成了 per-body 记账）。" % (_sp_F_ii, _sp_a_ii))
_v_au, _vp = read_r34_token(u"alpha_grav_1AU_m")
if _v_au is None:
    sub(u"对照 r34 面 alpha_grav_1AU_m：**没读到** ⇒ 本条不引他册数（上面两个极差皆本轮自算）")
else:
    sub(u"旁注：r34 面现读 alpha_grav_1AU_m=%s（%s）——那是 α 的定标问题，与本条的 EP 二分**不同源**，故不作阈值用。"
        % (_v_au, os.path.basename(_vp)))
sub(u"⇒ 关键更正：EP 的破坏不是「来料删了受力体 m」的偶然笔误，而是「剖面要不要含受力体」的**必选**（两支各测得一次）。")
sub(u"步长的价（阈的来路）：h=%.1e（=r·%.0e）。差分截断项 ~%.1e 对四个测试体**严格共模**"
    u"（U 对振幅线性 ⇒ F_num = 振幅^m × 同一形状函数，比值里被约掉），相消噪声 ~%.1e ⇒ 极差判据阈取 1e-12/1e-9。"
    % (_H9, _REL9, (_H9 / _R9) ** 2 / 6.0, 2.2e-16 * _R9 / (2.0 * _H9)))
chk(u"T09 (i) F 极差=机器1 而 a 极差=质标极差；(ii) 反之",
    abs(_sp_F_i - 1.0) < 1e-12 and abs(_sp_a_i / _mass_spread - 1.0) < 1e-9
    and abs(_sp_a_ii - 1.0) < 1e-12 and abs(_sp_F_ii / _mass_spread - 1.0) < 1e-9
    and _sp_a_i > 1e3,
    u"F_i=%.17g a_i=%.6g F_ii=%.6g a_ii=%.17g mass=%.6g"
    % (_sp_F_i, _sp_a_i, _sp_F_ii, _sp_a_ii, _mass_spread))

# ---------------------------------------------------------------------
# T10 V6 核心：零判别力的构造性证明（任意有心律都可写入族）
# ---------------------------------------------------------------------
item(u"T10", u"FAIL", u"V6 代价：对「有心律」的容纳率 6/6（含一枚已知错误律）⇒ 修复族对 r 依赖零判别力")
sub(u"定理（构造性）：任给有心势 U_t(r)，取 κ^m = max(U_t/α, 0)、τ^m = max(−U_t/α, 0) ⇒ U = α(κ^m−τ^m) ≡ U_t。")
sub(u"⇒ 族的表达能力 = 全体有心力。它**不排除任何** r 依赖，包括错的。")
_targets6 = [
    (u"牛顿 r^-2", lambda r: -1.0 / r),
    (u"库仑 r^-2", lambda r: 0.7 / r),
    (u"错误律 r^-5", lambda r: -1.0 / r ** 4),
    (u"汤川 e^-r/λ", lambda r: -math.exp(-r / 3.0) / r),
    (u"Cornell", lambda r: -1.0 / r + 0.4 * r),
    (u"谐振子 +kr", lambda r: 0.5 * r ** 2),
]
_C6 = 2.0
_grid10 = (0.5, 1.0, 3.0, 11.0, 40.0)
_T10_THR = 1e-6
_rows10 = []
for nm, U in _targets6:
    kp = lambda r, U=U: (max(U(r) / _C6, 0.0)) ** Fr(1, 2)
    tp = lambda r, U=U: (max(-U(r) / _C6, 0.0)) ** Fr(1, 2)
    worst = 0.0
    for r in _grid10:
        h = r * 1e-6
        num = force_of_U(_C6, 2, kp, tp, r, h)
        ana = -cderiv(U, r, h)
        worst = max(worst, abs(num - ana) / max(abs(ana), 1e-30))
    _rows10.append((nm, worst))
    sub(u"  %-14s 族内构造后 F 与目标律的最大相对残差 = %.3e ⇒ 容纳" % (nm, worst))
_sub = sum(1 for _, w in _rows10 if w < _T10_THR)
sub(u"机器裁定：容纳 %d/6（阈 %.0e；六枚实测残差皆 ≤ %.3e，即阈比实测宽 4 个量级以上——本条只主张『容纳』，不主张精度）；"
    u"其中第 3 行 r^-5 是**观测上错的律**也被逐位容纳 ⇒ 判别力 = 0（不是小，是零）。"
    % (_sub, _T10_THR, max(w for _, w in _rows10)))
_kinks = [(nm, [r for r in _grid10 if abs(U(r)) < 1e-9]) for nm, U in _targets6]
sub(u"构造的已知棱角（如实登记）：max() 拆分在 U_t=0 处给 κ 或 τ 一个零点，κ^m 的导数在那里可能不连续；"
    u"本轮网格（%s）上落进零点的目标 = %s ⇒ 残差读数未受该棱角污染，**跨零点拼接**不在本条见证范围内。"
    % (u"／".join(u"%.4g" % v for v in _grid10),
       u"／".join(u"%s%s" % (nm, (u"含零点" if k else u"无")) for nm, k in _kinks)))
sub(u"这条把 r34#X21/X22（「拟合前移到前提层」「λ 族逐位同力」）从**断言**升为**构造性证明**：修复不增信息，只换记号。")
chk(u"T10 六目标全容纳且含错误律",
    _sub == len(_rows10) and any(nm.startswith(u"错误律") and w < _T10_THR for nm, w in _rows10)
    and max(w for _, w in _rows10) < 1e-8,
    u"%d/%d 容纳，worst=%.3e" % (_sub, len(_rows10), max(w for _, w in _rows10)))

# ---------------------------------------------------------------------
# T11 针有牙：族的管辖边界 = 有心力类（非有心律不容纳）
# ---------------------------------------------------------------------
item(u"T11", u"PASS", u"边界见证：目标为纯切向力（F ⟂ r̂）时族在任何剖面上残差 = 满幅值 ⇒ 判别力只有 1 bit")
# 族给 F 必沿 r̂（U 只依赖 r）；目标取旋转场 F_t = (-y, x)/r²，在单位圆上 F_t ⟂ r̂ 处处成立。
worst_cos = 0.0
for i in range(12):
    th = 2.0 * math.pi * i / 12.0
    x, y = math.cos(th), math.sin(th)
    r2 = x * x + y * y
    tx, ty = -y / r2, x / r2                 # 目标力方向（切向）
    rx, ry = x / math.sqrt(r2), y / math.sqrt(r2)
    cosang = (tx * rx + ty * ry) / math.sqrt(tx * tx + ty * ty)
    worst_cos = max(worst_cos, abs(cosang))
sub(u"12 点均匀方位上 max|cos(F_族方向, F_目标方向)| = %.17g ⇒ 族只能给径向力，切向目标逐点正交（cos=0）。" % worst_cos)
# 反向见证：任何有心律的 cos 应为 ±1（同一条尺子在可容纳目标上必须绿）
kappa_c = lambda r: r ** (-0.5)
tau_c = lambda r: 0.0
ok_radial = True
_fr11 = []
for r in (0.7, 2.0, 9.0):
    fr = force_of_U(1.0, 2, kappa_c, tau_c, r, 1e-6)
    _fr11.append(fr)
    ok_radial = ok_radial and (abs(fr) > 0.0)
sub(u"正对照（同一把尺打在有心目标 κ=r^-1/2 上）：径向分量非零且沿 r̂ = %s ⇒ 针没坏，红在对象不在尺。"
    % (u"成立" if ok_radial else u"不成立"))
sub(u"满幅残差：切向目标在 r̂ 上的投影恒为 0，而族的任何非退化剖面只给径向力（本轮标定 F_r = %s）"
    u"⇒ 族能达到的最小残差 = 目标自身的满幅值（残差/目标幅值 = 1，与剖面怎么选、α 怎么定**无关**）。"
    % u"／".join(u"%.4g" % v for v in _fr11))
sub(u"⇒ 修复族的**全部**判别力 = 「是不是有心力」这 1 bit；四力的 r 依赖、力程、强度差一概不判。")
chk(u"T11 切向目标全正交 + 有心对照非零", worst_cos < 1e-15 and ok_radial and all(abs(v) > 0 for v in _fr11),
    u"maxcos=%.3g F_r=%s" % (worst_cos, u"／".join(u"%.4g" % v for v in _fr11)))

# ---------------------------------------------------------------------
# T12 三难定价表：α 普适 / 等效原理 / 符号手性 三者的取舍
# ---------------------------------------------------------------------
item(u"T12", u"BOUNDARY", u"三难定价：保任两条须弃第三条；机器给出三个角落各自的价")
_rows12 = [
    (u"角A 保 α 普适＋EP", u"弃符号/手性",
     u"须 m 偶 ⇒ N3 无载体（T05 枚举偶 m 上限 %d/3、T06 机器零），且 [α]=L^(m-1) 在偶 m 侧对四类耦合命中 %d/4（T04：全空）"
     % (_even_max, _even_best[0])),
    (u"角B 保 α 普适＋符号手性", u"弃 EP",
     u"m 奇且 κ,τ 只含源量 ⇒ 加速度极差 = %.6g（T09(i) 实测，恰等于测试体质标极差），而力极差 = %.17g" % (_sp_a_i, _sp_F_i)),
    (u"角C 保 EP＋符号手性", u"弃 α 普适（=弃「统一」二字）",
     u"剖面须含受力体 m、q ⇒ 力极差 = %.6g（正比于质量）、α 退化为 per-body 记账，四力不再有共同耦合（T09(ii)）" % _sp_F_ii),
]
for nm, give, price in _rows12:
    sub(u"%s ⇒ 弃：%s；价：%s" % (nm, give, price))
sub(u"机器裁定：三行皆无「零代价」角 ⇒ 来料 §六.3「α 分化为四力各自耦合系数」不是第三条出路而是**选了角C**，")
sub(u"      而角C 与 §一「唯一基础场」的公理正面冲突（本册不代选，只登记价格）。")
chk(u"T12 三角落皆标注了弃项与价（无零价角）", all(give and price for _, give, price in _rows12), u"3 行")

# ---------------------------------------------------------------------
# T13 他册读数现读（不复述；读不到不得引）
# ---------------------------------------------------------------------
item(u"T13", u"INFO", u"跨册定位：本轮相对 r34 的净差（他册数全部现读盘，读不到即弃引）")
try:
    p = os.path.normpath(R34_FACE)
    raw = open(p, "rb").read()
    sub(u"r34 面（只读）= %s：%d B，md5 %s" % (os.path.basename(p), len(raw), hashlib.md5(raw).hexdigest()))
    _hdr = raw.decode("utf-8", "replace").split(u"\n")[:8]
    _dist = [l.strip() for l in _hdr if u"条目" in l and u"PASS=" in l]
    sub(u"其面头部条目行现读 = %s" % (_dist[0] if _dist else u"**没读到**（本条不得引用）"))
except Exception as e:
    sub(u"r34 面读取异常：%r ⇒ 本轮所有跨册对照作废，不得引用" % (e,))
sub(u"净差五条（本轮印数不转抄）：①V1/V2 幂次与 α 常数**给出构造**（r34 只判死不给修）；")
sub(u"      ②V3/V5 符号·手性·禁闭改判为「m=2 特异病，m 奇/τ 支可修」；③V4 量纲承载从 0/4 升为「对一切 m 不可能 4/4」；")
sub(u"      ④力程从「差 2 倍」升为「力程定理：差 m 倍」；⑤零判别力从断言升为构造性定理（T10），并给边界 1 bit（T11）。")

# ---------------------------------------------------------------------
# T14 总裁定
# ---------------------------------------------------------------------
item(u"T14", u"INFO", u"总裁定：P0 修法**存在且本轮已交付构造**，但修复的认知内容为零；纲领唯一活口仍是场方程")
sub(u"成立面：幂次（T02）、α 常数（T03）、符号与手性（T05/T06，取 m 奇且 α<0）、禁闭常力（T07）、力程（T08 给形式解）——")
sub(u"        ⇒ r34 判死的四力还原（引力/电磁/强/弱）在**放开 m** 之后确有 4/4 可在族内写出"
    u"（弱力那一支只到「形式解」：力程要靠把目标 μ 写进剖面前提，见 T08 修法与代价），"
    u"故「V4.1 不可修」这个比 r34 更强的主张被本轮否证。")
sub(u"否证面：正因任一族都能写（T10），「可写」不承载任何约束；族的判别力 = 1 bit（T11），")
sub(u"        且 [α] 的承载 4/4 不可能（T04）、EP 与 α 普适与符号三角必弃一（T12）。")
sub(u"⇒ 结论：**这是一族恒等式改写，不是理论**。要成为理论必须回答「m 取几、κ/τ 的场方程是什么、剖面衰减从何而来」；")
sub(u"        4 维挠率的局域代数自由度（24=4⊕4⊕16，无 1/3/8 载体）已由 r34#X17 与本轮 T04 两侧夹住，仍是 OPEN。")
sub(u"OPEN 登记：O19-1 m 的选定原理（无）；O19-2 κ/τ 场方程（无）；O19-3 α 普适 vs EP 的取舍（未裁）；O19-4 力程修法与零判别力的分离（未做）。")

# ---------------------------------------------------------------------
# 自检收口 + 变异体（每条判据都喂一枚「已知错误的读数」，必须被打破才算数）
# ---------------------------------------------------------------------
# 版面卫生针：未替换的占位符（`%d`/`%.3e`/`{}`/`{nm}`）能穿过**所有**数值判据把模板印进面，
# 单列一条只扫字形的针；判集不许为空，故同时断言扫描行数。
# 花括号两支只认「空/纯数字/标识符」三种形，真集合记号 {2..6}、{κ,τ}、{3、5} 天生不命中（NEG-8 见证）。
PH = re.compile(u"%[-+ #0]*[0-9]*(?:\\.[0-9]+)?[dsfrgeE]|\\{\\d*\\}|\\{[A-Za-z_][A-Za-z0-9_]*\\}")


def pred_placeholder_clean(lines):
    return not any(PH.search(l) for l in lines)


# 排除类只按**行首形状**认（变异体描述行天生要引用模板字形），不按内容认；
# 内容式排除会把真缺陷行放过去——MUT-7 就是打这一点的。
MUTLINE = re.compile(u"^  (?:MUT|NEG)-\\d")


def ph_scan(lines):
    """返回 (判定命中, 结构排除)。两者都要印出来：排除数不印 = 门柱挪了没人知道。"""
    hits, excl = [], []
    for l in lines:
        if not PH.search(l):
            continue
        (excl if MUTLINE.match(l) else hits).append(l)
    return hits, excl


def pred_excl_passes(line):
    """问的是「卫生判据把这行**放过了**吗」：
       若排除类按内容认（坏写法），伪装行会被放过 ⇒ 返回真 ⇒ MUT 绿 = 无牙；
       按行首形状认（本轮写法）⇒ 伪装行落进命中、不许放过 ⇒ 返回假 = 红（合格）。"""
    hits, excl = ph_scan([line])
    return len(hits) == 0 and len(excl) == 1


_ph_hits, _ph_ex = ph_scan(OUT)
emit(u"版面卫生扫描：")
for l in _ph_hits[:10]:
    emit(u"  残留占位符 <<< %s" % l.strip()[:90])
chk(u"版面卫生 无未替换占位符", len(_ph_hits) == 0 and len(_ph_ex) == 0 and len(OUT) > 100,
    u"扫描 %d 行，命中 %d 处，结构排除 %d 处" % (len(OUT), len(_ph_hits), len(_ph_ex)))

emit(u"")
emit(u"自检 guard：")
_n_ok = sum(1 for _, ok in SELF if ok)
for nm, ok in SELF:
    if not ok:
        emit(u"  [自检] %-34s RED  <<< 本册不得引用" % nm)
emit(u"  合计 %d / %d 通过（逐条 OK/RED 已在各条目内印出）" % (_n_ok, len(SELF)))


# ---- 判据本体（与上面各条 chk 同一表达式，变异体只改**输入**不改判据）----
def pred_spread_one(vals, tol=1e-12):
    return abs(max(vals) / min(vals) - 1.0) < tol


def pred_const_force(vals, target, tol):
    return max(abs(v - target) / abs(target) for v in vals) < tol


def pred_power_closed(m, p):
    return Fr(m) * p + 1 == Fr(2)


def pred_rate(excess, analytic, tol):
    return abs(excess - analytic) < tol


def pred_chirality_zero(gap, tol=1e-12):
    return gap < tol


def pred_chirality_odd(gap, tol=1e-3):
    return gap > tol


_mut = []
# MUT-1：往「修复族 α 常数」里注入 1e-6 的 r 线性漂移 ⇒ T03 判据必须红
_m1_vals = [v * (1.0 + 1e-6 * i) for i, v in enumerate(_alpha_fixed)]
_mut.append((u"MUT-1 α 注入 1e-6 漂移 vs T03", pred_spread_one(_m1_vals), u"T03"))
# MUT-2：给常力读数加 1e-5·σ ⇒ T07 判据必须红（用 T07 自己的现推阈）
_m2_vals = list(_fr)
_m2_vals[2] += 1e-5 * _sig
_mut.append((u"MUT-2 常力加 1e-5·σ vs T07", pred_const_force(_m2_vals, -_sig, 100 * _noise_floor), u"T07"))
# MUT-3：把来料自己的 (m=2, p=1) 喂给 T02 的幂次判据 ⇒ 必须红（否则本尺量不出来料的病）
_mut.append((u"MUT-3 来料 (m=2,p=1) vs T02", pred_power_closed(2, Fr(1)), u"T02"))
# MUT-4：把力程超出项的解析式换成 1/x² ⇒ T08 判据必须红
_m4_ana = 1.0 / (_X_HI ** 2)
_mut.append((u"MUT-4 解析式换成 1/x^2 vs T08",
             pred_rate(_rate[2][_X_HI][4], _m4_ana, 1e-8), u"T08"))
# MUT-5：宣称「偶次幂也有手性载体」⇒ T05/T06 两条判据必须同时红
_mut.append((u"MUT-5 偶次称有手性 vs T05/T06",
             pred_chirality_odd(_even_gap) or not pred_chirality_zero(_even_gap), u"T05/T06"))
# MUT-6：往版面里放一行**没做完插值**的模板 ⇒ 卫生针必须抓到
_mut.append((u"MUT-6 模板行 %d/%.3e 未插值 vs 卫生针",
             pred_placeholder_clean([u"读数 %d 枚与 %.3e 阈", u"正常行 0.123"]), u"版面卫生"))
# MUT-7：MUT-6 那行自己就带占位符字形，它靠「行首是 MUT-」进了排除类。
# 把同一串占位符的行首伪装成条目行 ⇒ 排除类不得放过（证明排除按形状而非按内容，也没吞真缺陷）。
_m7_line = u"- T10 [FAIL] " + _mut[5][0][6:]
_mut.append((u"MUT-7 占位符行伪装成条目行 vs 排除类（须仍抓）",
             pred_excl_passes(_m7_line), u"版面卫生"))
# MUT-8：把尺加宽到 str.format 型 `{名字}` ⇒ 必须抓到（否则加宽只是装饰）
_mut.append((u"MUT-8 花括号 {nm} 未插值 vs 加宽后的卫生针",
             pred_placeholder_clean([u"读数 {nm} 枚", u"集合 m∈{2..6} 不是占位符"]), u"版面卫生"))
# 阴性对照：同一批判据喂**本轮真实读数**，必须全绿（否则红是尺坏不是针有牙）
_T7_THR = 100 * _noise_floor
_brace_lines = [l for l in OUT if u"{" in l]
_neg = [(u"NEG-1 真实 α 常数读数", pred_spread_one(_alpha_fixed)),
        (u"NEG-2 真实常力读数", pred_const_force(_fr, -_sig, _T7_THR)),
        (u"NEG-3 真实幂次 (m=3,p=1/3)", pred_power_closed(3, Fr(1, 3))),
        (u"NEG-4 真实衰减率(外推) vs 解析",
         all(pred_rate(_rate[m][x][4], _rate[m][x][1], 1e-8) for m in _rate for x in _rate[m])),
        (u"NEG-5 真实奇次手性差", pred_chirality_odd(_odd_gap)),
        (u"NEG-6 条目区真实版面（%d 行，不含变异体区；全面由终扫覆盖）" % len(OUT),
         pred_placeholder_clean(OUT)),
        # NEG-7：排除类的另一半见证——同一串占位符**带 MUT- 行首**时确实进得了排除类
        #（否则排除类可以是空类，MUT-7 的「红」就什么也没证明）
        (u"NEG-7 真自述模板行（MUT-6 原形）应被排除", pred_excl_passes(u"  " + _mut[5][0])),
        # NEG-8：加宽后的尺打在**真集合记号**上（m∈{2..6}、{κ,τ}、{3、5}）必须全不命中，
        # 否则加宽就是把门柱挪到能过关（判集由版面现读，不凭手感）
        (u"NEG-8 真集合记号行 vs 加宽后的卫生针",
         all(pred_placeholder_clean([l]) for l in _brace_lines) and len(_brace_lines) > 0)]

emit(u"变异体（期望：%d 枚全红 = 判据有牙；%d 枚阴性对照全绿 = 尺没坏；枚数由名单现算，不是手钉）：" % (len(_mut), len(_neg)))
for nm, ok, tgt in _mut:
    emit(u"  %-34s（打向 %s）%s" % (nm, tgt, u"红（合格）" if not ok else u"绿（无牙，本册不得引用）"))
_n_neg = sum(1 for _, ok in _neg if ok)
for nm, ok in _neg:
    emit(u"  %-34s%s" % (nm, u"绿（合格）" if ok else u"红（尺坏，本册不得引用）"))
_teeth = all(not ok for _, ok, _ in _mut) and _n_neg == len(_neg)
exit_code = 0 if (_n_ok == len(SELF)) and _teeth else 1

emit(u"")
emit(u"条目统计：%s" % u" ／ ".join(u"%s×%d" % (v, sum(1 for _, x, _ in ITEMS if x == v))
                                    for v in (u"PASS", u"FAIL", u"THEOREM", u"BOUNDARY", u"INFO")))
emit(u"判定条目 %d 枚｜自检 %d/%d｜变异体 %d/%d 红｜阴性对照 %d/%d 绿｜退出码 %d"
     % (len(ITEMS), _n_ok, len(SELF), sum(1 for _, o, _ in _mut if not o), len(_mut),
        _n_neg, len(_neg), exit_code))
emit(u"")
emit(u"分层结论：")
emit(u"  [数学] 幂次 p=1/m、[α]=L^(m-1)、力程 剖面 μ⇒U mμ、常力支 τ^m=σr/(−α) 四条为恒等式级，机器残差见 T02/T07/T08。")
emit(u"  [物理] 放开 m 后四力皆可写入族（T02/T03/T05/T07/T08）⇒ r34「四力还原不可修」的**强**主张不成立；"
     u"但族对有心律容纳 6/6 含一枚错律（T10）⇒ 可写不承载约束。")
emit(u"  [诚实边界] EP/α普适/符号 三角无零代价角（T12）；4/4 量纲承载对一切 m 不可能（T04）；判别力仅 1 bit（T11）；场方程仍 OPEN（T14）。")
emit(u"  [红线] 本轮未宣称统一场论成立，只裁「哪些缺陷可修、修要付什么」；数学自洽 ≠ 实验证实；")
emit(u"         哥德巴赫仍未证明，统一场论仍未成立。未跑 refresh_catalog，未 git add/commit。")

# 终扫：占位符针要覆盖**含收口尾部**的整张面（中途那次只扫到条目区）
_final_hits, _final_ex = ph_scan(OUT)
# 排除数不许凭手感钉：由变异体名单里**自带占位符字形的行**现算，两路须恒等
_ex_expect = sum(1 for nm, _, _ in _mut if PH.search(u"  " + nm)) + \
             sum(1 for nm, _ in _neg if PH.search(u"  " + nm))
if _final_hits:
    emit(u"版面卫生（终扫）：判定命中 %d 行 ⇒ 本册不得引用，退出码强置 1" % len(_final_hits))
    for l in _final_hits[:10]:
        emit(u"  <<< %s" % l.strip()[:90])
    exit_code = 1
elif len(_final_ex) != _ex_expect:
    emit(u"版面卫生（终扫）：结构排除 %d 行 ≠ 名单现算 %d 行 ⇒ 排除类在吞东西，退出码强置 1"
         % (len(_final_ex), _ex_expect))
    exit_code = 1
else:
    _bl = [l for l in OUT if u"{" in l]
    emit(u"版面卫生（终扫）：扫到本行前共 %d 行（本行不计，面不能自量——盘的尺寸／LF 只由末行「写后回读」给），"
         u"判定命中 0 处；结构排除 %d 处（= 名单现算 %d，"
         u"全部是 MUT-6 那类自述模板的字形，逐条列在变异体区）；"
         u"含真集合记号 {…} 的行 %d 行（现扫，加宽尺对其不命中——第二口径复核，不是靠排除类放过）"
         % (len(OUT), len(_final_ex), _ex_expect, len(_bl)))

_txt = u"\n".join(OUT) + u"\n"
data = _txt.encode("utf-8")
open(REPORT, "wb").write(data)
back = open(REPORT, "rb").read()
_tail = (u"写后回读：%s｜盘上 %d B｜md5 %s｜CR %d／LF %d｜判定条目 %d 枚｜自检 %d/%d｜退出码 %d\n"
         % (os.path.basename(REPORT), len(back), hashlib.md5(back).hexdigest(),
            back.count(b"\r"), back.count(b"\n"), len(ITEMS), _n_ok, len(SELF), exit_code)).encode("utf-8")
# 控制台可能是 GBK：整段走 buffer，绝不让 print() 去猜编码
sys.stdout.buffer.write(data)
sys.stdout.buffer.write(_tail)
sys.stdout.flush()
sys.exit(exit_code)
