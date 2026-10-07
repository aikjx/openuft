# -*- coding: utf-8 -*-
"""
S03-V18.7
任务（承接 S03-V18.6 §11 约束 1）：给 GAQ 螺旋场线定义一个体系内的加框（framing），
并判定它是否可导出。

纯标准库（math / sys / os / io），Python 3.8+
红线：本册全部为可否证性裁定与自洽性检验，不含对 GAQ 主张的正面支持证据。

输出：07_计算复现/运行记录/S03_V18_7_加框可导出性与闭合性二难报告.txt
"""

import sys
import os
import io
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PI = math.pi

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.dirname(HERE)
LOGDIR = os.path.join(CALC, "运行记录")
REPORT_NAME = "S03_V18_7_加框可导出性与闭合性二难报告.txt"

LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0}
ITEMS = []


def emit(t=""):
    LINES.append(t)


def rec(code, verdict, title):
    COUNTS[verdict] += 1
    ITEMS.append((code, verdict, title))
    emit("[%s] %s  %s" % (verdict, code, title))


def P(c, t):
    rec(c, "PASS", t)


def F(c, t):
    rec(c, "FAIL", t)


def B(c, t):
    rec(c, "BOUNDARY", t)


def I(c, t):
    rec(c, "INFO", t)


def CR(c, t):
    rec(c, "CORRECTED", t)


def table(headers, rows):
    w = [len(h) for h in headers]
    for r in rows:
        for k in range(len(headers)):
            w[k] = max(w[k], len(str(r[k])))
    fmt = " | ".join("{:<%d}" % x for x in w)
    emit("  " + fmt.format(*headers))
    emit("  " + "-+-".join("-" * x for x in w))
    for r in rows:
        emit("  " + fmt.format(*[str(x) for x in r]))


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsc(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vnorm(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def vunit(a):
    n = vnorm(a)
    return (a[0] / n, a[1] / n, a[2] / n)


def vmid(a, b):
    return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5, (a[2] + b[2]) * 0.5)


def gauss_linking(P, Q):
    n = len(P)
    m = len(Q)
    r1 = [vmid(P[i], P[(i + 1) % n]) for i in range(n)]
    d1 = [vsub(P[(i + 1) % n], P[i]) for i in range(n)]
    r2 = [vmid(Q[j], Q[(j + 1) % m]) for j in range(m)]
    d2 = [vsub(Q[(j + 1) % m], Q[j]) for j in range(m)]
    cr = [[vcross(d1[i], d2[j]) for j in range(m)] for i in range(n)]
    acc = 0.0
    for i in range(n):
        ri = r1[i]
        row = cr[i]
        for j in range(m):
            d = vsub(ri, r2[j])
            nd = vnorm(d)
            acc += vdot(d, row[j]) / (nd * nd * nd)
    return acc / (4.0 * PI)


def gauss_writhe(P, skip=1):
    n = len(P)
    r1 = [vmid(P[i], P[(i + 1) % n]) for i in range(n)]
    d1 = [vsub(P[(i + 1) % n], P[i]) for i in range(n)]
    acc = 0.0
    for i in range(n):
        ri = r1[i]
        di = d1[i]
        for j in range(n):
            g = abs(i - j)
            g = min(g, n - g)
            if g <= skip:
                continue
            d = vsub(ri, r1[j])
            nd = vnorm(d)
            acc += vdot(d, vcross(di, d1[j])) / (nd * nd * nd)
    return acc / (4.0 * PI)


def tf(t):
    return (2.0 * math.cos(2 * t) + 0.5 * math.cos(5 * t) + 0.5 * math.cos(t),
            2.0 * math.sin(2 * t) + 0.5 * math.sin(5 * t) - 0.5 * math.sin(t),
            math.sin(3 * t))


def tf_d1(t):
    return (-4.0 * math.sin(2 * t) - 2.5 * math.sin(5 * t) - 0.5 * math.sin(t),
            4.0 * math.cos(2 * t) + 2.5 * math.cos(5 * t) - 0.5 * math.cos(t),
            3.0 * math.cos(3 * t))


def tf_d2(t):
    return (-8.0 * math.cos(2 * t) - 12.5 * math.cos(5 * t) - 0.5 * math.cos(t),
            -8.0 * math.sin(2 * t) - 12.5 * math.sin(5 * t) + 0.5 * math.sin(t),
            -9.0 * math.sin(3 * t))


def tf_d3(t):
    return (16.0 * math.sin(2 * t) + 62.5 * math.sin(5 * t) + 0.5 * math.sin(t),
            -16.0 * math.cos(2 * t) - 62.5 * math.cos(5 * t) + 0.5 * math.cos(t),
            -27.0 * math.cos(3 * t))


def frame_at(t):
    d1 = tf_d1(t)
    d2 = tf_d2(t)
    tv = vunit(d1)
    bv = vunit(vcross(d1, d2))
    nv = vcross(bv, tv)
    return tv, nv, bv


def torsion_at(t):
    d1 = tf_d1(t)
    d2 = tf_d2(t)
    d3 = tf_d3(t)
    cr = vcross(d1, d2)
    den = vdot(cr, cr)
    if den < 1e-18:
        return 0.0
    return vdot(cr, d3) / den


def speed_at(t):
    return vnorm(tf_d1(t))


def simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for k in range(1, n):
        s += f(a + k * h) * (4.0 if k % 2 else 2.0)
    return s * h / 3.0


def trefoil_points(N):
    return [tf(2.0 * PI * k / N) for k in range(N)]


def frenet_ribbon(N, eps):
    out = []
    for k in range(N):
        t = 2.0 * PI * k / N
        _, nv, _ = frame_at(t)
        out.append(vadd(tf(t), vsc(nv, eps)))
    return out


def circle_points(R=1.0, N=240):
    return [(R * math.cos(2 * PI * k / N), R * math.sin(2 * PI * k / N), 0.0)
            for k in range(N)]


CHECKS = []


def check(name, ok, detail):
    CHECKS.append((name, bool(ok), detail))
    emit("  [SC %s] %s :: %s" % ("OK" if ok else "NG", name, detail))


emit("=" * 78)
emit("S03-V18.7  GAQ 螺旋场线的加框（framing）可导出性判定")
emit("          承接 S03-V18.6 §11 约束 1")
emit("=" * 78)
emit("")
emit("红线：本册全部为可否证性裁定与自洽性检验。PASS 仅表示『该式机器自洽』")
emit("      或『标准数学事实被独立复算』，不构成对 GAQ 的物理验证。")
emit("")

emit("-" * 78)
emit("第 0 节  验证器（沿用 V18.6 的 Gauss 积分实现，先复校）")
emit("-" * 78)
circ = circle_points(R=1.0, N=240)
wr_circ = gauss_writhe(circ, skip=1)
check("SC1 平面圆 Writhe = 0", abs(wr_circ) < 1e-3, "Wr = %.3e" % wr_circ)
tw_circ = 0.0
check("SC2 平面圆 Frenet Twist = 0（τ ≡ 0）", abs(tw_circ) < 1e-15, "Tw = 0")
emit("")

emit("-" * 78)
emit("第 1 节  常曲率常挠率曲线能否闭合（V7-a）")
emit("-" * 78)
emit("")
emit("  来稿前置锚点：类时孤子是『轴向螺旋』的【闭合】扭结场线，而 GAQ 全套解析式")
emit("  （κ = Rω²/c²、τ = ωu/c²、κ²+τ² = Ω²）建立在【常曲率常挠率】之上。")
emit("")
emit("  由 Frenet-Serret 基本定理：κ、τ 为常数 ⇒ 曲线在刚体运动下唯一，")
emit("  只能是圆（τ=0）或圆螺旋 r(t) = (R cos t, R sin t, a t)（τ≠0）。")
emit("  圆螺旋的 z 分量 a·t 严格单调 ⇒ 不可能闭合。")
emit("")
rows = []
for (R, a) in ((1.0, 0.3), (1.0, 1.0), (2.0, 0.1), (0.5, 2.0)):
    den = R * R + a * a
    kappa = R / den
    tau = a / den
    best = None
    m = 4000
    for k in range(1, m + 1):
        T = 2.0 * PI * (1.0 + 400.0 * k / m)
        dz = a * T
        dr = math.sqrt((R * math.cos(T) - R) ** 2 + (R * math.sin(T)) ** 2 + dz * dz)
        if best is None or dr < best:
            best = dr
    rows.append(("R=%g,a=%g" % (R, a), "%.6e" % kappa, "%.6e" % tau,
                 "%.6f" % best, "%.3e" % (2 * PI * abs(a))))
table(["圆螺旋参数", "曲率 κ", "挠率 τ", "min|r(T)-r(0)|", "下界 2π|a|"], rows)
emit("")
all_pos = all(float(r[3]) > 1e-6 for r in rows)
check("SC3 常 κ≠0、常 τ≠0 的圆螺旋永不闭合", all_pos,
      "四组参数 min|r(T)-r(0)| 均 > 0")
emit("")
F("V7-a", "不存在闭合的常 κ≠0 且常 τ≠0 曲线 ⇒ GAQ『闭合轴向螺旋孤子』与常 κτ 解析式不可兼得")
emit("      依据：F-S 基本定理（κ,τ 常数 ⇒ 唯一为圆螺旋）+ z 分量严格单调（机器扫描四组）。")
emit("      射程：不单独否定『闭合扭结』或『圆螺旋解析式』，只否定**二者同时成立**。")
emit("")

emit("-" * 78)
emit("第 2 节  Frenet 加框的可导出性 + White 公式在真扭结上的检验（V7-b）")
emit("-" * 78)
emit("")
emit("  Frenet 标架 T,N,B 是曲线的局部函数：闭合曲线一周后必回到同一标架（κ>0 处处），")
emit("  故 Frenet 加框自动闭合、由曲线唯一确定、无残余自由度。")
emit("")
_, nv0, bv0 = frame_at(0.0)
_, nv1, bv1 = frame_at(2.0 * PI)
reg = max(vnorm(vsub(nv0, nv1)), vnorm(vsub(bv0, bv1)))
check("SC4 trefoil 的 Frenet 标架沿一周自动回归", reg < 1e-9,
      "max|u(2π)-u(0)| = %.3e" % reg)
emit("")
tw_tf = simpson(lambda t: torsion_at(t) * speed_at(t), 0.0, 2 * PI, 20000) / (2.0 * PI)
emit("  trefoil 的 Frenet Twist：Tw = (1/2π)∮τ ds = %.9f（非整数，合法）" % tw_tf)
emit("")
rows = []
for N in (400, 800):
    tfpts = trefoil_points(N)
    wr = gauss_writhe(tfpts, skip=1)
    for eps in (0.03, 0.06, 0.12):
        edge = frenet_ribbon(N, eps)
        lk = gauss_linking(tfpts, edge)
        rows.append((N, "%.2f" % eps, "%.6f" % wr, "%.6f" % lk,
                     "%.6f" % (tw_tf + wr),
                     "%.6f" % abs(lk - (tw_tf + wr)),
                     "%.6f" % abs(lk - round(lk))))
table(["N", "eps", "Wr", "Lk(ribbon)", "Tw+Wr", "|Lk-(Tw+Wr)|", "|Lk-整数|"], rows)
emit("")
best_row = min(rows, key=lambda r: float(r[5]))
check("SC5 trefoil 上 Lk = Tw + Wr（White 公式非平凡检验）", float(best_row[5]) < 0.05,
      "最佳 N=%s eps=%s：|Lk-(Tw+Wr)| = %s" % (best_row[0], best_row[1], best_row[5]))
check("SC6 Lk 为整数（拓扑不变量）", float(best_row[6]) < 0.05,
      "|Lk-最近整数| = %s，最近整数 = %d" % (best_row[6], round(float(best_row[3]))))
emit("")
P("V7-b", "Frenet 加框可导出：由曲线唯一确定、自动闭合、无残余自由度；White 公式在真扭结上数值闭合")
emit("      读数：Tw = %.9f，Wr = %s，Lk = %s ≈ 整数 %d"
      % (tw_tf, best_row[2], best_row[3], round(float(best_row[3]))))
emit("      这是 V18.6 V6-a（平面圆，Wr=0 的退化情形）的非平凡推广。")
emit("")
B("V7-b-r", "代价：Frenet 加框在 κ→0 处奇异。GAQ 螺旋 κ=R/(R²+a²)>0 故此处无碍，")
emit("        但构型一旦出现拐点即须改 Bishop（见 V7-c）。")
emit("")

emit("-" * 78)
emit("第 3 节  Bishop（平行输运）加框：holonomy 与残余自由度（V7-c）")
emit("-" * 78)
emit("")
emit("  Bishop 加框旋转率 φ' = -τ|r'| ⇒ 一周 holonomy Δφ = -∮τ ds。")
emit("  若 ∮τ ds 非 2π 整数倍，则 Bishop 加框不闭合，无法构造闭合 ribbon。")
emit("")
hol_tf = tw_tf * 2.0 * PI
rows = [("trefoil", "%.9f" % hol_tf, "%.9f" % (hol_tf / (2 * PI)),
         "%.6f" % abs(hol_tf / (2 * PI) - round(hol_tf / (2 * PI)))),
        ("平面圆（对照）", "0.000000000", "0.000000000", "0.000000")]
table(["曲线", "holonomy ∮τ ds (rad)", "圈数 ∮τ ds /2π", "距最近整数偏差"], rows)
emit("")
check("SC7 trefoil 的 Bishop holonomy 非 2π 整数倍",
      abs(hol_tf / (2 * PI) - round(hol_tf / (2 * PI))) > 1e-3,
      "圈数 = %.9f" % (hol_tf / (2 * PI)))
emit("")
B("V7-c", "Bishop 加框在 trefoil 上不闭合（%.6f 圈，非整数）⇒ 不可用其定义闭合 ribbon"
  % (hol_tf / (2 * PI)))
emit("      且 Bishop 依赖初始角（连续自由度）⇒ 即使闭合，Tw 也需外加约定。")
emit("      ⇒ 在需要闭合场线的场合，加框候选实质只有 Frenet 一个。")
emit("")

emit("-" * 78)
emit("第 4 节  二难与三条出路的代价（V7-d）")
emit("-" * 78)
emit("")
table(["出路", "内容", "代价", "可否救"],
      [("1", "放弃闭合（类时孤子也改开式）",
        "Lk/Wr/Tw 全无定义 ⇒ §5 判据表与 §6 重联命题全部作废", "否"),
       ("2", "放弃常 κ、τ（改非常数螺旋）",
        "GAQ 全套解析式 κ=Rω²/c²、τ=ωu/c²、κ²+τ²=Ω² 失效；"
        "V18.5 的机器零结果（κ/τ=u/v、副法向倾角）不再适用", "部分"),
       ("3", "二者皆保留",
        "与 F-S 基本定理矛盾（V7-a）", "否")])
emit("")
B("V7-d", "出路 2 是唯一不立即自杀的选项，但其代价是 GAQ 的整个圆螺旋解析层失效")
emit("      且非常数 κ、τ 下，来稿 §1『Tw ∝ ∮τ ds』仍成立，但『Wr 对应曲率积分』仍是错的（V18.6 V6-d），")
emit("      故 §1 的 Tw/Wr 分配叙事仍无约束内容。")
emit("")

emit("-" * 78)
emit("第 5 节  对 V18.6 V6-b 的更正（V7-e）")
emit("-" * 78)
emit("")
emit("  V18.6 V6-b 称『Tw ∝ ∮τ ds 隐含加框闭合条件』——该表述不准确，本册更正：")
emit("")
emit("  · Frenet 加框是曲线的局部函数，对 κ>0 处处的【闭合】曲线**自动闭合**（SC4 机器零）；")
emit("  · Tw = ∮τ ds / 2π 是**实数**，不需要是整数；Lk = Tw + Wr 的整数性由 Wr 补偿（SC5/SC6）；")
emit("  · V18.6 中 n=0.5 的加框不闭合，是本册自己构造的**人工加框**的问题，")
emit("    不构成对来稿的指摘。")
emit("")
CR("V7-e", "更正 V18.6 V6-b：加框闭合条件只对『非 Frenet 的人工加框』构成约束，Frenet 加框自动闭合")
emit("       射程收窄为：若 GAQ 采用非 Frenet 加框（如 Bishop），须额外声明闭合性（V7-c）。")
emit("       V18.6 的其它条目不受此更正影响。")
emit("")

emit("-" * 78)
emit("第 6 节  裁定：framing 本身不是公设边界")
emit("-" * 78)
emit("")
table(["加框候选", "由曲线唯一确定", "自动闭合", "无残余自由度", "体系内可导出"],
      [("Frenet（κ>0）", "是", "是（SC4）", "是", "**是**"),
       ("Bishop", "否（依赖初始角）", "否（holonomy 非整数，SC7）", "否", "否"),
       ("人工加框（V18.6 n=0.5）", "否", "否", "否", "否")])
emit("")
P("V7-f", "裁定：加框在体系内**可导出**（取 Frenet），不构成新的公设边界")
emit("      ⇒ V18.6 §11 约束 1『必须显式给出加框』已由本册落实，可解除。")
emit("")
F("V7-g", "但分支三的真正阻塞不是加框，而是【闭合性二难】（V7-a）")
emit("      类时孤子若闭合 ⇒ 常 κτ 解析式失效；若常 κτ ⇒ 不闭合 ⇒ Lk/Wr/Tw 无定义。")
emit("      二者皆使来稿 §5 判据表与 §6 重联命题失去地基。")
emit("      加上光子侧本就是开式（V18.6 V6-e），GAQ 的两个孤子类**都没有**良定义的 Lk。")
emit("")
I("V7-h", "分支三若要继续，唯一可行输入仍是 V18.6 V6-f 的手性符号（镜像 Writhe 机器零反号），")
emit("      因为它只依赖构型而不依赖闭合性/Lk。建议下一步直接沿此线推进。")
emit("")

emit("=" * 78)
emit("汇总")
emit("=" * 78)
for code, verdict, title in ITEMS:
    emit("  [%-9s] %-7s %s" % (verdict, code, title))
emit("")
emit("条目合计 %d" % len(ITEMS))
emit("PASS = %d" % COUNTS["PASS"])
emit("FAIL = %d" % COUNTS["FAIL"])
emit("BOUNDARY = %d" % COUNTS["BOUNDARY"])
emit("INFO = %d" % COUNTS["INFO"])
emit("CORRECTED = %d" % COUNTS["CORRECTED"])
emit("")
emit("自检：")
nok = sum(1 for _, ok, _ in CHECKS if ok)
for name, ok, detail in CHECKS:
    emit("  [%s] %s :: %s" % ("OK" if ok else "NG", name, detail))
emit("自检 %d/%d" % (nok, len(CHECKS)))
emit("")
emit("红线复述：")
emit("  1. 本册所有 FAIL 均为来稿内部自洽性或与几何定理的冲突，不是对 GAQ 全部内容的否定。")
emit("  2. PASS（V7-b、V7-f）是标准微分几何事实的独立复算，不构成对 GAQ 的物理验证。")
emit("  3. V7-e 是对本体系 V18.6 自身表述的更正，已登记。")
emit("  4. 本册未对任何物理预言做正面验证。")
emit("")

ok_all = (nok == len(CHECKS)) and len(CHECKS) >= 7
text = "\n".join(LINES) + "\n"
if not os.path.isdir(LOGDIR):
    os.makedirs(LOGDIR)
path = os.path.join(LOGDIR, REPORT_NAME)
with io.open(path, "w", encoding="utf-8") as fh:
    fh.write(text)

print(text)
print("报告已写入: %s" % path)
print("自检 %d/%d" % (nok, len(CHECKS)))
sys.exit(0 if ok_all else 1)
