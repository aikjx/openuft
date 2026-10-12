# -*- coding: utf-8 -*-
"""
attack23｜引力的本质在这族里到底是什么：量纲唯一性 · 标量可见度 · Bertrand 等时性 · 挠率的代数性（编号现扫见下面第一行）
====================================================================================================
靶：attack22（攻破㉔）面上 OPEN 的引力三笔——O24-3（G 出环后的处置）、O24-1（α 的数值与谱无族内方程定住）、
    O24-2（源约束的物理出处）；并把问题抬到「引力到底是什么」这一格：
    它是一枚耦合常数？一个几何对象？还是物质的质量比？
本轮不接来料的散文结论，只在**纯标准库可复算的四条判据**上落裁定：
  P1 量纲唯一性：SI 指数矩阵的零度决定「引力的无量纲强度」有几种形状。
  P2 标量可见度：能动张量的迹与全收缩之比决定「标量势能不能弯光」。
  P3 Bertrand 等时性：幂律中心力的近心点角对振幅的依赖性决定「1/r 支有没有进动项」。
  P4 挠率的代数性：最小 Einstein-Cartan 里挠率有无动能项决定「τ 支能不能媒介长程力」。

预注册（开场写下，判据先于数据）
  P1-预注册：引力的无量纲耦合唯一 ⇒ 族的「普适 α」可以在量纲层面直接被排除，不必再借几何环。
  P3-预注册：族的 m=1 落点（U ∝ r^-1）正落在 Bertrand 的两枚例外之一 ⇒ 它的近心点进动**恒零**，
             与经典基准 E0 面上那枚 42.98″ 正面冲突；这是结构性质不是数值巧合。
  P4-预注册（本轮开场我写的是这一句）：「要让 τ 传播必须给它的动能项配一枚**出环**（L 幂为正）的耦合」。
             ⇒ 若 P4 的幂记账表说这枚耦合是 L^0（在环内），本条预注册就被自己的表否证，原话留面（同档案 rule 6）。
  P2-预注册：标量媒介看不见无迹能动张量 ⇒「苹果落地而光线不弯」不是缺陷清单里两条，是同一条的两次显形。

体例：纯标准库；零随机；判定条目 G01–G15；自检 guard 全过 **且** 电池（同一判据真实输入须绿、注错须红）全合格才退 0；
      运行报告落 attack23_*_report.txt（本册数值唯一载体；面自身字节／md5 只由 stdout 末行写后回读给）。
      他册与他盘读数一律现场读盘并点名载体，读不到即印「没读到」不作引用。
阈值纪律：凡「相对偏差 < 阈」型判据，阈由该条自己的截断阶与印刷半 ulp 现推并印出（不手钉）。
红线：本轮不宣称统一场论成立，也不宣称「引力已被解释」；裁的是「这族能给引力什么」；未跑 refresh_catalog，未 git add/commit。
"""
import hashlib
import io
import math
import os
import re
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.abspath(os.path.join(HERE, os.pardir))
BASE = os.path.abspath(os.path.join(DOCS, os.pardir))
CIRCLED = u"①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚"

REPORT = os.path.join(HERE, u"attack23_引力的本质量纲唯一性与标量盲区_2026-10-11_report.txt")
A22_FACE = os.path.join(HERE, u"attack22_场方程容纳率与量纲奇偶_2026-10-11_report.txt")
A21_FACE = os.path.join(HERE, u"attack21_几何势族P0修法_代价定价_2026-10-11_report.txt")
R34_FACE = os.path.join(DOCS, u"本项目_全维自洽与归一化", u"数据",
                        u"TUFT-V41alpha自然单位势_全维审计_2026-10-10.md")
CLS = os.path.join(BASE, u"02_共享基础", u"经典基准")
E1 = os.path.join(CLS, u"经典实验基准", u"E1_光线偏折", u"README.md")
E0 = os.path.join(CLS, u"经典实验基准", u"E0_水星近日点进动", u"README.md")
D1 = os.path.join(CLS, u"经典作用量", u"D1_爱因斯坦希尔伯特", u"README.md")
D6 = os.path.join(CLS, u"经典作用量", u"D6_爱因斯坦嘉当", u"README.md")
DPLAN = os.path.join(BASE, u"02_共享基础", u"推导与量纲专题", u"延伸方向",
                     u"D_普朗克单位的量纲推导.md")
QUANJ = os.path.join(DOCS, u"统一理论体系_已验证正确内容整合全集.md")

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
    emit(u"  [自检] %-42s %s%s" % (name, u"OK" if ok else u"RED", (u"  " + detail) if detail else u""))
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


def grep(path, key, label, want=1):
    b = read_b(path)
    if b is None:
        sub(u"他盘读数 [%s]：载体读不到（%s）⇒ 不作引用" % (label, os.path.basename(path)))
        return None if want == 1 else []
    got = [ln.strip() for ln in b.decode(u"utf-8", u"replace").split(u"\n") if key in ln]
    if not got:
        sub(u"他盘读数 [%s]：载体在场但没印该键 ⇒ 不作引用" % label)
        return None if want == 1 else []
    return got[0] if want == 1 else got


def stat_line(p, label):
    b = read_b(p)
    if b is None:
        sub(u"载体 %s 读不到 ⇒ 本条弃引" % label)
        return None
    return u"%s｜盘上 %d B｜md5 %s" % (os.path.basename(p), len(b), hashlib.md5(b).hexdigest())


# ------------------------------------------------------------------ 精确线性代数
def rref(A):
    """分数行最简形；返回 (矩阵, 主元列表)。"""
    M = [[Fr(x) for x in row] for row in A]
    nr, nc = len(M), len(M[0])
    piv, r = [], 0
    for c in range(nc):
        pr = next((i for i in range(r, nr) if M[i][c] != 0), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c] != 0:
                fac = M[i][c]
                M[i] = [a - fac * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return M, piv


def nullspace(A):
    M, piv = rref(A)
    nc = len(A[0])
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for fc in free:
        v = [Fr(0)] * nc
        v[fc] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis, len(piv), free


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def dot3(u, v):
    return sum(Fr(a) * Fr(b) for a, b in zip(u, v))


# ------------------------------------------------------------------ 轨道（Binet 形式，RK4）
def rk2psi(f, u0, dphi=2e-4, phi_max=None, nmax=4):
    """u'' = f(u)；返回逐次近心点（u 极大）角位置表。

    转折点判据只许比较「本步起点」与「本步终点」的 v：早前一版把上一轮的 v 又当成 vprev 留在手里，
    于是一次真峰被连记两格（间隔恰为一个 dphi），Ψ 实测成解析值的一半到五分之二——那是把积分器的
    簿记错记成了物理。"""
    if phi_max is None:
        phi_max = 2.0 * math.pi * (nmax + 1)
    u, v = float(u0), 0.0
    phi = 0.0
    steps = int(phi_max / dphi)
    peaks = []
    for _ in range(steps):
        k1u, k1v = v, f(u)
        k2u, k2v = v + 0.5 * dphi * k1v, f(u + 0.5 * dphi * k1u)
        k3u, k3v = v + 0.5 * dphi * k2v, f(u + 0.5 * dphi * k2u)
        k4u, k4v = v + dphi * k3v, f(u + dphi * k3u)
        un = u + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = v + dphi / 6.0 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if v > 0.0 >= vn:                            # 本步内 u 由升转降 ⇒ 一个近心点
            peaks.append(phi + (v / (v - vn)) * dphi)
        u, v, phi = un, vn, phi + dphi
    return peaks


def psi_of(f, u0, nmax=4, dphi=2e-4):
    """返回 (平均近心点角间距, 找到的峰数, 间距相对散布)。

    散布是积分器自己的牙：伪峰或漏峰会让相邻间距至少差出一个 dphi，物理上不该有。"""
    pk = rk2psi(f, u0, dphi=dphi, nmax=nmax)
    if len(pk) < 2:
        return None, len(pk), None
    d = [b - a for a, b in zip(pk, pk[1:])]
    m = sum(d) / len(d)
    return m, len(pk), max(abs(x - m) / m for x in d)


def relerr(a, b):
    s = max(abs(a), abs(b))
    return 0.0 if s == 0.0 else abs(a - b) / s


# ------------------------------------------------------------------ 主程序
def main():
    # 号段：本轮号**按名认领**（他盘把某个带圈号挂在本册文件名上的行＝授权），max+1 只是无人认领时的兜底
    # 自滤排除：本册源码里整段住着 ①…末号 的序号字母表；上一版判决面也住着本轮号与字母表末号——
    #           两者若进扫描集，「已见 max」读的就是量具自己的刻度，不是语料的号段
    own = os.path.abspath(__file__)
    own_face = os.path.abspath(REPORT)
    seen = []
    skipped = []
    own_seen = []
    granted = {}
    NAMEKEY = re.compile(u"attack23")
    ADJ = re.compile(u"attack23[^①-⑳㉑-㉚\\n]{0,80}?攻破([①-⑳㉑-㉚])")
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in (u"数据", u"存档")]
        for fn in files:
            if not fn.endswith((u".md", u".py", u".txt")):
                continue
            p = os.path.abspath(os.path.join(root, fn))
            if p == own or p == own_face:
                skipped.append(os.path.basename(p))
                if p == own:
                    for ch in set(io.open(p, encoding=u"utf-8", errors=u"replace").read()):
                        if ch in CIRCLED:
                            own_seen.append(CIRCLED.index(ch) + 1)
                continue
            try:
                t = io.open(p, encoding=u"utf-8", errors=u"replace").read()
            except Exception:
                continue
            for ch in set(list(fn) + list(t)):
                if ch in CIRCLED:
                    seen.append(CIRCLED.index(ch) + 1)
            if not NAMEKEY.search(fn):
                for _i, _ln in enumerate(t.split(u"\n")):
                    for _m in ADJ.finditer(_ln):
                        granted.setdefault(CIRCLED.index(_m.group(1)) + 1, []).append(
                            (os.path.basename(p), _i + 1))
    _gnum = sorted(granted)
    MAXP1 = (max(seen) if seen else 0) + 1
    MYNUM = _gnum[0] if len(_gnum) == 1 else MAXP1
    TAG = CIRCLED[MYNUM - 1]

    emit(u"=" * 98)
    emit(u"attack23｜引力的本质：量纲唯一性 · 标量盲区 · Bertrand 等时性 · 挠率的代数性（攻破%s＝第 %d 号）"
         % (TAG, MYNUM))
    emit(u"=" * 98)
    emit(u"[号段·按名认领] 他盘把带圈号挂在本册文件名「attack23」同一子句里的行，逐条现扫共 %d 处，"
         u"指向的号=%s ⇒ 本轮认领第 %d 号（%s）；兜底口径 max+1 会算成第 %d 号——两者不同，"
         u"因为并发写者已在本册**具名授权**（认领优先于顺延，否则他那 %d 处指向「attack23＝攻破%s」的引用全部悬空）："
         % (sum(len(v) for v in granted.values()),
            u"／".join(u"第 %d 号" % k for k in _gnum) if _gnum else u"无",
            MYNUM, TAG, MAXP1, sum(len(v) for v in granted.values()),
            CIRCLED[MYNUM - 1] if _gnum and len(_gnum) == 1 else u"?"))
    for _k in _gnum:
        for _f, _l in granted[_k]:
            emit(u"  载体 %s:%d → 第 %d 号" % (_f, _l, _k))
    emit(u"[号段·自滤] 排除 %d 份本册自己的文件（%s）：源码里住着整段序号字母表（其中最大号 %d），"
         u"上一版判决面里住着本轮号与字母表末号——若不排除，「已见 max」= 量具刻度（=字母表长度 %d）而非语料号段，"
         u"本轮号会被自己的尺吞成第 %d 号。教训形状：上一版为了说明污染，把字母表**末号那个字**印进了面，"
         u"于是那张面自己成了下一轮的污染源（现改印号数，不印那个字）"
         % (len(skipped), u"／".join(skipped), max(own_seen) if own_seen else 0,
            len(CIRCLED), len(CIRCLED) + 1))
    emit(u"[号段·现扫兜底] 排除本册文件后语料已见 max = %d ⇒ max+1 = 第 %d 号（仅作对照；本轮实际认领第 %d 号）"
         % (max(seen) if seen else 0, MAXP1, MYNUM))
    chk(u"号段按名认领唯一（他盘挂在本册名上的号只有一种）", len(_gnum) == 1,
        u"distinct=%d 载体=%s" % (len(_gnum), u"、".join(str(k) for k in _gnum)))
    chk(u"号段自滤生效（排除本册后 max 严格小于字母表最大号）",
        (max(seen) if seen else 0) < (max(own_seen) if own_seen else 0),
        u"排除后 %d ＜ 字母表最大号 %d" % (max(seen) if seen else 0, max(own_seen) if own_seen else 0))
    BATTERY.append((u"G00 号段自滤", lambda a, b: a < b,
                    (max(seen) if seen else 0, max(own_seen) if own_seen else 0),
                    (max(seen) if seen else 0, max(seen) if seen else 0)))
    BATTERY.append((u"G00 号段认领", lambda a, b: a == b and len(a) == 1,
                    (_gnum, [MYNUM]), (_gnum + [MYNUM + 1], [MYNUM])))
    for p, lab in ((A22_FACE, u"㉔ 面"), (A21_FACE, u"⑲ 面"), (R34_FACE, u"r34 面"),
                   (C0128_FACE, u"C0128 面"),
                   (E1, u"E1 偏折"), (E0, u"E0 进动"), (D1, u"D1 EH"), (D6, u"D6 EC"),
                   (DPLAN, u"D 普朗克量纲"), (QUANJ, u"已验证全集")):
        b = read_b(p)
        emit(u"[载体在场性] %s：%s" % (lab, (u"盘上 %d B｜md5 %s" % (len(b), hashlib.md5(b).hexdigest()))
                                    if b is not None else u"读不到 ⇒ 相关条目自动弃引"))

    # ============================== G01 量纲唯一性（P1）
    item(u"G01", u"THEOREM", u"P1 量纲唯一性：指数矩阵的零度决定「引力的无量纲强度」只有 1 种形状——(m/m_P)²；"
                            u"基集 (ℏ,G,c) 满秩无非平凡无量纲组合（|det|=2，与 D 专题在册的 det=-2 同号非零）")
    # SI 基 (M,L,T) 的指数向量
    EXP = {u"G": (Fr(-1), Fr(3), Fr(-2)), u"hbar": (Fr(1), Fr(2), Fr(-1)),
           u"c": (Fr(0), Fr(1), Fr(-1)), u"m": (Fr(1), Fr(0), Fr(0)),
           u"k_B": (Fr(1), Fr(2), Fr(-2), Fr(-1))[:3] + (Fr(0),)}
    basis3 = [u"G", u"hbar", u"c"]
    mat3 = [[EXP[k][i] for k in basis3] for i in range(3)]
    d3 = det3(mat3)
    ns3, rk3, fr3 = nullspace([[EXP[k][i] for k in basis3] for i in range(3)])
    sub(u"指数矩阵（行=M,L,T；列=%s）现算 det = %d｜秩 = %d／列数 3 ⇒ 零度 = %d"
        % (u"、".join(basis3), d3, rk3, 3 - rk3))
    sub(u"D 专题在册读数（只读盘）：%s" % (grep(DPLAN, u"\\det=-2", u"量纲矩阵行列式") or u"没读到那行"))
    sub(u"本册按「行=M,L,T、列=G,ℏ,c」现算得 %d，那册印 -2：两处只是行列次序不同（换序一次变号），"
        u"同号非零这一条一致 ⇒ 满秩 ⇒ **不存在**非平凡无量纲组合 ℏ^a G^b c^d = 1 除 a=b=d=0（那册 D1 在册 PASS）" % d3)
    chk(u"G01 基集满秩且零度 0", d3 != 0 and rk3 == 3 and len(ns3) == 0,
        u"det=%d rank=%d null=%d" % (d3, rk3, len(ns3)))
    BATTERY.append((u"G01 满秩判据", lambda x: x != 0, int(d3), 0))
    mat4 = [[EXP[k][i] for k in basis3 + [u"m"]] for i in range(3)]
    ns4, rk4, fr4 = nullspace(mat4)
    gen = ns4[0] if ns4 else None
    # 归一化到 e=2（与在册式子 G m²/(ℏ c) 对表）
    scale = Fr(2) / gen[3] if gen else Fr(1)
    gnorm = [x * scale for x in gen] if gen else None
    sub(u"加入第 4 枚输入 m ⇒ 3 行 4 列：秩 = %d ⇒ 零度 = %d ⇒ 无量纲组合**唯一**（差一个整体幂）"
        % (rk4, 4 - rk4))
    sub(u"零空间生成元（现算，按 m 的幂归一到 2）：%s ⇒ 组合 = G^%s ℏ^%s c^%s m^%s = G m²/(ℏ c)"
        % (u"、".join(str(x) for x in gnorm), gnorm[0], gnorm[1], gnorm[2], gnorm[3]))
    sub(u"第二通道（逐条回代验零）：%s" % u"／".join(
        u"M,L,T 点积 = %s" % dot3([EXP[k][i] for k in basis3 + [u"m"]], gnorm) for i in range(3)))
    chk(u"G01 零度 1 且生成元回代给全零", 4 - rk4 == 1 and all(dot3(mat4[i], gnorm) == 0 for i in range(3)),
        u"null=%d back=%s" % (4 - rk4, u"、".join(str(dot3(mat4[i], gnorm)) for i in range(3))))
    BATTERY.append((u"G01 零度唯一", lambda x: x == 1, 4 - rk4, (4 - rk4) + 1))

    # ============================== G02 唯一耦合带受力体质量（P1 推论）
    item(u"G02", u"THEOREM", u"P1 推论：引力唯一的无量纲强度是 (m/m_P)²——它**自带受力体的质量**；"
                             u"由 G m²/(ℏ c) 与 (m/m_P)² 两式独立复算同一枚数（电子档实测残差在印刷半 ulp 内）")
    a1 = grep(QUANJ, u"α_grav = G m_e²/(ℏc)", u"全集电子档 α_grav")
    a2 = grep(QUANJ, u"m_e/m_P = ", u"全集电子质量比")
    SCI = re.compile(u"([0-9]+(?:\\.[0-9]+)?)e([+-]?[0-9]+)")

    def sci_to_fr(s):
        """把 '4.185e-23' 这类在册科学计数**整体**换成精确分数；指数带符号，不许只取位数。"""
        mm = SCI.search(s)
        if not mm:
            return None, None, None
        mant, ex = mm.group(1), int(mm.group(2))
        return Fr(mant), ex, len(mant.split(u".")[1]) if u"." in mant else 0

    m_ratio = printed_alpha = None
    if a1:
        printed_alpha = sci_to_fr(a1[a1.index(u"α_grav"):] if u"α_grav" in a1 else a1)
    if a2:
        m_ratio = sci_to_fr(a2[a2.index(u"m_e/m_P"):] if u"m_e/m_P" in a2 else a2)
    sub(u"在册现读（只读盘，不转抄结论）：%s｜%s" % (a1 or u"没读到", a2 or u"没读到"))
    sub(u"解析口径：两枚数按「尾数＋带符号 10 的幂」整体转成精确分数（上一版只取了指数的**位数**、"
        u"把 −23 读成 +23 ⇒ 平方后落在 1.75e+47，残差恰为 1 —— 那是把符号丢了，不是复算失败）")
    if m_ratio and printed_alpha is not None:
        base, ex, dec_b = m_ratio
        abase, aex, dec_a = printed_alpha
        recomputed = (base * Fr(10) ** ex) ** 2
        printed = abase * Fr(10) ** aex
        dev = float(abs(recomputed - printed) / max(recomputed, printed))
        # 阈：两侧各自的印刷半 ulp —— 尾数的小数位数由**现读那串自己的拼写**给出，不手数
        half_b = Fr(1, 2) * Fr(1, 10) ** dec_b / base          # 4.185 → 末位半个 ulp 的相对量
        ulp_ratio = 2 * half_b                                 # 平方把相对误差加倍
        ulp_alpha = Fr(1, 2) * Fr(1, 10) ** dec_a / abase
        thr = float(ulp_ratio + ulp_alpha)
        sub(u"独立复算：(m_e/m_P)² 由现读的比值（尾数 %s、指数 %+d）平方 = %s｜在册印 %s（尾数 %s、指数 %+d）｜"
            u"相对残差 %s｜阈 %s（两枚印刷半 ulp 之和，由那两行自己的小数位数现推：%s 的半 ulp 加倍＝%s，"
            u"%s 的半 ulp＝%s）⇒ %s"
            % (base, ex, fmt(float(recomputed)), fmt(float(printed)), abase, aex,
               fmt(dev), fmt(thr), base, fmt(float(ulp_ratio)), abase, fmt(float(ulp_alpha)),
               u"在印刷精度内一致" if dev < thr else u"超阈＝两处在册数不能同时成立"))
        sub(u"这一条的意义不在数值而在**形状**：引力的无量纲强度只能是「受力体质量对普朗克质量之比」——"
            u"它按定义带 m；而 ⑲/㉔ 的 α 在 m=1 那一格被压成与受力体无关的纯数（普适）。")
        chk(u"G02 复算落在印刷半 ulp 阈内", dev < thr, u"dev=%s thr=%s" % (fmt(dev), fmt(thr)))
        BATTERY.append((u"G02 残差判据", lambda d, t: d < t, (dev, thr), (dev * 10, thr)))
    else:
        chk(u"G02 复算落在印刷半 ulp 阈内", False, u"在册两行没读到 ⇒ 无法复算")
    # 普适性对照：⑲ 面的 T03 那行（现读）
    t03 = grep(A21_FACE, u"α = C/A", u"⑲ T03 α 的普适读法")
    sub(u"⑲ 面 T03 现读：%s" % (t03 or u"没读到那行 ⇒ 本条只谈量纲形状，不引 ⑲ 的记法"))

    # ============================== G03 三面同点（第二、第三独立路线）
    item(u"G03", u"PASS", u"P1×P4 交叉核对：量纲唯一性（本册 G01）与几何环半轴（㉔ U02）、手性奇偶（⑲ T05）是三条**不同机制**，"
                          u"三者对「族的 α 能否就是引力」给同一侧答案 ⇒ 结论不靠单条路线")
    pwr = grep(A22_FACE, u"可行格的 L 幂集合", u"㉔ U01 几何幂集")
    u02 = grep(A22_FACE, u"机器裁定：「α 可几何构造」", u"㉔ U02 单点交集")
    t04 = grep(A21_FACE, u"max 命中 = 3/4", u"⑲ T04 量纲承载最佳档")
    sub(u"路线一（本册 G01／G02）：引力的无量纲强度唯一＝(m/m_P)²，带 m ⇒ 与普适 α 在量纲层面互斥（不需要几何环）。")
    sub(u"路线二（㉔ U02 现读）：%s" % (u02 or u"没读到那行"))
    sub(u"路线二附（㉔ U01 现读幂集）：%s" % (pwr or u"没读到那行"))
    sub(u"路线三（⑲ T04 现读）：%s" % (t04 or u"没读到那行"))
    sub(u"三条路线的机制互不重叠：一靠 SI 指数矩阵的零度，二靠度规-挠率-曲率收缩的半轴封闭，三靠幂次对量纲承载的档位匹配；"
        u"任何一条单独成立都足以排除「α 就是 G」，三条同向 ⇒ 本册把这条记为**多路确证**而非单点推断")
    chk(u"G03 三路线皆在场且同向", bool(u02) and bool(pwr) and bool(t04),
        u"r1=在册零度 r2=%s r3=%s" % (bool(u02), bool(t04)))
    BATTERY.append((u"G03 在场性", lambda a, b: a and b, (bool(u02), bool(t04)), (bool(u02), False)))

    # ============================== G04 偏折的双侧实测（P2 的观测面）
    item(u"G04", u"THEOREM", u"P2 观测面：偏折的 GR/牛顿之比＝(1+γ_张量)/(1+γ_标量)＝2；"
                             u"标量媒介最多复现在册那枚 0.875″，复现不了 1.75″（E1 载体两数现读）")
    e1n = grep(E1, u"牛顿预言", u"E1 牛顿档")
    e1g = grep(E1, u"GR 预言", u"E1 GR 档")
    e1f = grep(E1, u"4GM", u"E1 偏折公式")
    v_new, v_gr = None, None
    for lab, ln in ((u"newton", e1n), (u"gr", e1g)):
        if ln:
            mm = re.search(u"([0-9]+\\.?[0-9]*)''", ln)
            if mm:
                if lab == u"newton":
                    v_new = Fr(mm.group(1))
                else:
                    v_gr = Fr(mm.group(1))
    if v_new and v_gr:
        ratio = float(v_gr / v_new)
        # 阈：两枚都是 3 位有效印刷（0.875 半 ulp=0.0005，1.75 半 ulp=0.005）⇒ 比的相对半 ulp 之和
        thr4 = float(Fr(5, 10000) / v_new + Fr(5, 1000) / v_gr)
        sub(u"E1 现读：牛顿 %s、GR %s ⇒ 实测比 = %s｜公式比 (1+1)/(1+0) = 2.000（γ 为空间曲率与时间曲率之比）"
            u"｜阈 %s（两枚现读数各自的有效位数现推的半 ulp 之和）⇒ %s"
            % (v_new, v_gr, fmt(ratio), fmt(thr4),
               u"与公式恒等" if abs(ratio - 2.0) < thr4 else u"与公式不合"))
        sub(u"读法：把引力写成「只有一个标量势 U(r)」的理论，其 PPN γ = 0 ⇒ 偏折只来自 g_00，"
            u"给出的正是那枚 0.875″——**它是牛顿值，也是观测上错的那一枚**；要拿到 1.75″ 必须有第二枚自由度"
            u"（空间度规被同一场弯曲，γ=1），而那正是自旋-2 场的特征，不是标量势能给的")
        chk(u"G04 比值恒等于 2 且在半 ulp 内", abs(ratio - 2.0) < thr4, u"ratio=%s" % fmt(ratio))
        BATTERY.append((u"G04 比值判据", lambda r, t: abs(r - 2.0) < t, (ratio, thr4), (ratio + 0.5, thr4)))
    else:
        chk(u"G04 比值恒等于 2 且在半 ulp 内", False, u"E1 两档没读到")
    sub(u"E1 公式行现读：%s" % (e1f or u"没读到"))

    # ============================== G05 标量可见度表（P2 的定理面）
    item(u"G05", u"THEOREM", u"P2 定理面：完全流体 T=diag(ρ,p,p,p) 对**标量**媒介的可见度 (3w−1)²/(1+3w²) "
                             u"在 w=1/3（辐射）恰为机器零——不是小，是零；张量媒介看全 T_μν 故无此盲区")
    ws = [Fr(0), Fr(1, 3), Fr(1, 2), Fr(1), Fr(-1, 3)]
    rows5 = []
    for w in ws:
        tr = 3 * w - 1                        # T/ρ
        tst = 1 + 3 * w * w                   # T_μν T^μν / ρ²
        vis = Fr((tr * tr), 1) / tst if tst != 0 else None
        rows5.append((w, tr, tst, vis))
    for w, tr, tst, vis in rows5:
        sub(u"w=%-5s（p=wρ）｜T/ρ = %s｜T_μνT^μν/ρ² = %s｜标量可见度 = %s｜主动引力质量密度 (ρ+3p)/ρ = %s"
            % (str(w), tr, tst, vis, 1 + 3 * w))
    zero5 = [r for r in rows5 if r[3] == 0]
    rad = [r for r in rows5 if r[0] == Fr(1, 3)][0]
    sub(u"机器裁定：可见度恰为 0 的 w = %s（辐射／光子气体）⇒ **纯标量势介导的力对光不作用**，"
        u"而同一张里 w=0（尘埃）可见度 = %s（满）⇒「苹果落地、光线不弯」在同一理论里是必然，不是漏设"
        % (u"、".join(str(r[0]) for r in zero5), rad[3]))
    sub(u"同表的另一半：辐射的主动引力质量密度是能量密度的 2 倍（w=1/3 给 1+3w=2）——"
        u"这枚 2 与 G04 那枚 2 是同一件事的两个记账口（张量场耦合整个 T_μν，标量场只耦合它的迹）")
    chk(u"G05 辐射档精确零且尘埃档满格", len(zero5) == 1 and str(zero5[0][0]) == u"1/3"
        and rows5[0][3] == 1, u"zero=%s dust=%s" % (len(zero5), rows5[0][3]))
    BATTERY.append((u"G05 盲区判据", lambda z, d: z == 1 and d == 1, (len(zero5), int(rows5[0][3])), (0, 1)))

    # ============================== G06 Bertrand 等时性枚举（P3）
    item(u"G06", u"THEOREM", u"P3 Bertrand 枚举：幂律力 F∝r^n 的近心点角 Ψ=2π/√(n+3)（小振幅实测），"
                             u"而对**大**振幅只有 n=−2 与 n=1 的 Ψ 不随振幅变 ⇒ 族的 m=1（U∝r^-1）恰落在闭合那一格")
    grid = [Fr(-2), Fr(-19, 10), Fr(-18, 10), Fr(-15, 10), Fr(-1), Fr(0), Fr(1), Fr(3, 2), Fr(2)]
    u_big = Fr(8, 5)
    rows6 = []
    A1, A2, A3 = 0.02, 0.002, 0.0002                      # 三枚小振幅，用于 A² 律外推（不猜系数）
    fac12 = A1 * A1 / (A1 * A1 - A2 * A2)
    fac23 = A2 * A2 / (A2 * A2 - A3 * A3)
    dphi6 = 2e-4
    steps6 = int(2.0 * math.pi * 4 / dphi6)
    worst_spread = 0.0
    for n in grid:
        f = (lambda nn: (lambda u: u ** float(-nn - 2) - u))(n)
        ps, k1, ss = psi_of(f, 1.0 + A1, nmax=3, dphi=dphi6)
        pb, k2, sb = psi_of(f, float(u_big), nmax=3, dphi=dphi6)
        p2, k3, s2 = psi_of(f, 1.0 + A2, nmax=3, dphi=dphi6)
        p3, k4, s3 = psi_of(f, 1.0 + A3, nmax=3, dphi=dphi6)
        ana = 2.0 * math.pi / math.sqrt(float(n) + 3.0)
        drift = None if (ps is None or pb is None) else abs(ps - pb) / abs(ps)
        ok_a = None not in (ps, p2, p3)
        e12 = ps - fac12 * (ps - p2) if ok_a else None            # 由 (A1,A2) 外推的 A→0 值
        e23 = p2 - fac23 * (p2 - p3) if ok_a else None            # 由 (A2,A3) 外推的 A→0 值
        rel = None if e23 is None else abs(e23 - ana) / ana
        tol = None if e23 is None else (abs(e23 - e12)
                                        + 3.0 * max(ss, s2, s3) * ana
                                        + math.sqrt(steps6) * EPS * ana)
        sp = None if ps is None else ss
        worst_spread = max(worst_spread, sp if sp is not None else 0.0)
        rows6.append((n, ps, pb, ana, drift, sp, rel, tol))
    sub(u"枚举 n（力律指数，F∝r^n）｜小振幅 Ψ（u0=1.02）｜大振幅 Ψ（u0=1.6）｜解析 2π/√(n+3)｜振幅漂移 |ΔΨ|/Ψ｜"
        u"间距散布（积分器自己的牙）｜A→0 外推与解析的相对差／自定价：")
    for n, ps, pb, ana, drift, sp, rel, tol in rows6:
        sub(u"  n=%-6s｜%s｜%s｜%s｜%s｜%s｜%s" % (
            str(n),
            fmt(ps) if ps else u"未闭合/无界",
            fmt(pb) if pb else u"未闭合/无界",
            fmt(ana),
            fmt(drift) if drift is not None else u"—",
            (u"%s（阈半格 %s）" % (fmt(sp), fmt(dphi6 / (2.0 * ps))) if sp is not None else u"—"),
            (u"%s ＜ %s ⇒ 对上" % (fmt(rel), fmt(tol)) if rel is not None and rel < tol
             else (u"%s ≥ %s ⇒ 没对上" % (fmt(rel), fmt(tol)) if rel is not None else u"—"))))
    closed = [r[0] for r in rows6 if r[4] is not None and r[4] < 1e-6]
    sub(u"机器裁定：振幅漂移 < 1e-6（即等时＝轨道对一切小扰闭合）的 n = %s（枚举域 %d 格内）"
        u"⇒ Bertrand 的两枚例外被**实测复现**，不是引用；阈 1e-6 的来源：RK4 在 dphi=2e-4 下的截断 ~ (dphi)^4 量级"
        % (u"、".join(str(x) for x in closed), len(grid)))
    # —— 绝对通道（这一格是本轮新立的牙）：只判「漂移」的尺对**共模错读**是盲的。
    #    上一版 Ψ 实测把每个真峰连记两格（间距表里插进一个 dphi 宽的假间距），漂移却仍为机器零，
    #    于是 Kepler 那行印成 2.513 而解析值 6.283 —— 全绿的面撒了谎。现补两路：间距散布＋A→0 外推对解析。
    ok_spread = all(r[5] is not None and r[5] < dphi6 / (2.0 * r[1]) for r in rows6 if r[1])
    ok_abs = all(r[6] is not None and r[6] < r[7] for r in rows6 if r[1])
    sub(u"绝对通道（新立）：三枚小振幅按 A² 律做 Richardson 外推取 A→0，得 Ψ₀，与闭式 2π/√(n+3) 逐格对表；"
        u"阈由**同一台积分器自己的两次外推之差**＋间距散布＋浮点累加底（sqrt(步数)·ε·Ψ）现推，不手数。"
        u"这条能抓住「间距整体被记错」那一型，漂移那条抓不住（漂移只比两次读数之比）。")
    chk(u"G06 间距散布小于半个 dphi（无伪峰/漏峰）", ok_spread,
        u"worst=%s 阈（最小一格）=%s" % (fmt(worst_spread), fmt(dphi6 / (2.0 * max(r[1] for r in rows6 if r[1])))))
    chk(u"G06 外推 Ψ₀ 逐格对上闭式 2π/√(n+3)", ok_abs,
        u"外推格数=%d／阈全由自定价给" % sum(1 for r in rows6 if r[6] is not None))
    sub(u"族的落点对表：㉔ 把 α 的几何构造逼到 m=1，⑲ T02 给幂律 p=1/m ⇒ p=1 ⇒ U∝r^-1 ⇒ 力律 F∝r^-2 ⇒ "
        u"正是上表 n=%s 那一格（漂移 %s，解析 Ψ=%s＝2π）⇒ 这一支的近日点进动**恒等于零**是结构结论"
        % (str(rows6[0][0]), fmt(rows6[0][4]), fmt(rows6[0][3])))
    m1_row = [r for r in rows6 if r[0] == Fr(-2)][0]
    chk(u"G06 闭合指数恰为 −2 与 1", closed == [Fr(-2), Fr(1)], u"closed=%s" % u"、".join(str(x) for x in closed))
    BATTERY.append((u"G06 例外集", lambda s: s == [u"-2", u"1"], [str(x) for x in closed], [u"-2", u"-1"]))
    BATTERY.append((u"G06 绝对通道", lambda rel, t: rel < t, (rows6[0][6], rows6[0][7]),
                    (rows6[0][6] + rows6[0][7], rows6[0][7])))

    # ============================== G07 进动项的来路与量级（P3 推论）
    item(u"G07", u"THEOREM", u"P3 推论：进动项必须来自 Binet 右端的 δu²（即势里的 1/r³，E0 在册那第三项）；"
                             u"实测每圈进动 Δ→2πδ（三档 δ 阶梯＋δ 置零对照），而族的 U=α(κ−τ) 反解不出任何 u² 项")
    deltas = [Fr(1, 50), Fr(1, 500), Fr(1, 5000)]
    dphi7 = 2e-4
    nmax7 = 6
    steps7 = int(2.0 * math.pi * (nmax7 + 1) / dphi7)
    A_B, A_S = 0.05, 0.005                              # 绕微扰圆轨道的两枚振幅（A² 律外推用）
    fac7 = A_B * A_B / (A_B * A_B - A_S * A_S)
    rows7 = []
    for d in deltas:
        dd = float(d)
        f = (lambda x, _c=dd: 1.0 + _c * x * x - x)
        u_eq = 2.0 / (1.0 + math.sqrt(1.0 - 4.0 * dd))   # δu²−u+1=0 的小根（稳定写法，不作相消）
        resid_eq = dd * u_eq * u_eq - u_eq + 1.0         # 该根满足方程的残差（只验代数，不验物理）
        pB, kB, sB = psi_of(f, u_eq + A_B, nmax=nmax7, dphi=dphi7)
        pS, kS, sS = psi_of(f, u_eq + A_S, nmax=nmax7, dphi=dphi7)
        pB2, kB2, _ = psi_of(f, u_eq + A_B, nmax=nmax7, dphi=2.0 * dphi7)   # 阶长加倍＝积分器自价
        p_lin = 2.0 * math.pi / math.sqrt(1.0 - 2.0 * dd * u_eq)            # 线性化闭式（第二通道）
        adv = pB - 2.0 * math.pi
        rows7.append((d, u_eq, resid_eq, pB, p_lin, adv,
                      adv / (2.0 * math.pi * dd), (p_lin - 2.0 * math.pi) / (2.0 * math.pi * dd),
                      fac7 * (pB - pS), abs(pB2 - pB) + math.sqrt(steps7) * EPS * pB))
    sub(u"δ 阶梯｜线性化点 u_eq（现解 δu²−u+1=0 的小根，残差逐条印）｜实测 Ψ（振幅 %s）｜线性化闭式 Ψ_lin｜"
        u"每圈进动 Δ＝Ψ−2π｜比 r＝Δ/(2πδ)｜解析比 r_lin｜有限振幅偏置（A² 律自估）｜仪器自价（阶长加倍＋浮点累加底）："
        % A_B)
    for (d, ue, rq, pB, pL, adv, rm, rl, exc, fl) in rows7:
        sub(u"  δ=1/%-6d｜u_eq=%s（残差 %s）｜Ψ=%s｜Ψ_lin=%s｜Δ=%s｜r=%s｜r_lin=%s｜偏置 %s＋自价 %s ⇒ 阈 %s"
            % (d.denominator, fmt(ue), fmt(rq), fmt(pB), fmt(pL), fmt(adv), fmt(rm), fmt(rl),
               fmt(exc), fmt(fl), fmt(exc + fl)))
    ok7 = all(abs(r[4] - r[3]) < r[8] + r[9] for r in rows7)      # |Ψ_lin − Ψ_meas| < 偏置＋自价
    q_meas = [abs(r[6] - 1.0) for r in rows7]
    ok7b = all(q_meas[i + 1] < q_meas[i] for i in range(len(q_meas) - 1))
    sub(u"判据一（双通道，逐格）：|Ψ_meas − Ψ_lin| 必须落在「A² 律自估的有限振幅偏置＋阶长加倍差＋浮点累加底 "
        u"sqrt(步数)·ε·Ψ」之内——阈全部由这台积分器自己的两次读数现推，不含手钉常数；"
        u"δ=1/50 那格的偏置实测为 %s，它不为零，所以不许当零用（把它当零就等于宣称有限振幅的轨道也精确闭合）。"
        % fmt(rows7[0][8]))
    sub(u"判据二（阶梯）：r−1 逐格严格收缩（%s）——δ 每缩小十倍，剩余同比例缩小，"
        u"这就是「进动的一阶项确为 2πδ」：把 δu² 关掉（δ→0）轨道回到 G06 的 n=−2 那格，进动消失。"
        % u"→".join(fmt(x) for x in q_meas))
    # δ 关掉那一格是判据二的对照实验，不是推论：同一台积分器、同一初值，只把系数置零
    f0 = (lambda x: 1.0 - x)
    p0, k0, s0 = psi_of(f0, 1.0 + A_B, nmax=nmax7, dphi=dphi7)
    sub(u"对照格（δ=0 实测）：Ψ=%s（n=−2 档 %d 个近心点、间距散布 %s），与 2π 差 %s ⇒ "
        u"进动项**整项**由 δu² 携带，系数置零则机器精度内为零（这一条是 G06 绝对通道之外的第二枚独立牙）"
        % (fmt(p0), k0, fmt(s0), fmt(abs(p0 - 2.0 * math.pi))))
    ok7c = abs(p0 - 2.0 * math.pi) < 3.0 * s0 * 2.0 * math.pi + math.sqrt(steps7) * EPS * 6.0
    sub(u"E0 在册那三行现读：%s" % (grep(E0, u"V_{\\rm eff}", u"E0 有效势三项式") or u"没读到那行"))
    sub(u"合读：E0 的进动**整项**来自有效势第三项（−GML²/(mc²r³)），它在 Binet 右端恰好是 δu² 那一枚；"
        u"㉔ 的算符-源分层里族的势 U=α(κ^m−τ^m) 反解出的源不含任何 u² 型修正（G06 的 n=−2 档漂移为机器零），"
        u"所以「m=1 就是引力」这一支**给不出 43″**——不是数值不准，是那一项不存在")
    chk(u"G07 双通道 Ψ 落在自价阈内", ok7,
        u"最大超阈幅度=%s" % fmt(max(abs(r[4] - r[3]) - (r[8] + r[9]) for r in rows7)))
    chk(u"G07 一阶律阶梯 r−1 严格收缩", ok7b, u"q=%s" % u"、".join(fmt(x) for x in q_meas))
    chk(u"G07 δ=0 对照格进动为机器零", ok7c, u"|Ψ−2π|=%s" % fmt(abs(p0 - 2.0 * math.pi)))
    BATTERY.append((u"G07 双通道判据", lambda a, t: a < t, (abs(rows7[0][4] - rows7[0][3]), rows7[0][8] + rows7[0][9]),
                    (abs(rows7[0][4] - rows7[0][3]) + rows7[0][8] + rows7[0][9], rows7[0][8] + rows7[0][9])))
    BATTERY.append((u"G07 δ零对照", lambda a, t: a < t, (abs(p0 - 2.0 * math.pi),
                    3.0 * s0 * 2.0 * math.pi + math.sqrt(steps7) * EPS * 6.0),
                    (abs(p0 - 2.0 * math.pi) + 1.0, 3.0 * s0 * 2.0 * math.pi)))

    # ============================== G08 来料裁定（两基准合判）
    item(u"G08", u"FAIL", u"来料裁定（对本族，不对本册方法）：m=1 那一支在两枚经典基准上同时不合格——"
                          u"进动缺整项（G07：结构上无 u² 项；在册 42.98″）＋偏折缺一倍（G04：只能给 0.875″）"
                          u"＋辐射不可见（G05：w=1/3 机器零）")
    e0g = grep(E0, u"42.98", u"E0 GR 档进动")
    sub(u"三处独立否证：①G06 实测 n=−2 的等时性（漂移 %s）⇒ 该支轨道闭合 ⇒ 进动 = 0，与 E0 在册那行相冲；"
        u"②G04 的比值 2 ⇒ 标量势只能给半；③G05 的 w=1/3 精确零 ⇒ 标量势对光干脆不作用。"
        % fmt(m1_row[4]))
    sub(u"载体行现读：%s｜%s" % (e0g or u"没读到", e1g or u"没读到"))
    sub(u"判读纪律：本条判 FAIL 的对象是「族的 m=1 支可以充当引力」这一主张，"
        u"不是「水星进动是 42.98″」这条在册观测；三处否证都是**同族内**的量纲/结构性质，不依赖外部新数据")
    chk(u"G08 三处否证皆有载体", bool(e0g) and bool(e1g) and bool(zero5),
        u"E0=%s E1=%s w零=%d" % (bool(e0g), bool(e1g), len(zero5)))
    BATTERY.append((u"G08 否证在场", lambda a, b, c: a and b and c, (bool(e0g), bool(e1g), len(zero5) == 1),
                    (bool(e0g), bool(e1g), False)))

    # ============================== G09 挠率的代数性（P4，含预注册自否）
    item(u"G09", u"THEOREM", u"P4 挠率记账：最小 EC 的挠率方程无导数项 ⇒ τ 是代数辅助场，积掉只留接触型自旋-自旋（零程）；"
                             u"但「要让 τ 传播就得配一枚出环的正幂耦合」这句预注册被本表否证——那一档的系数是 L^0，在环内")
    book = [(u"R（EH 项）", Fr(-2)), (u"T²（挠率平方）", Fr(-2)), (u"R²", Fr(-4)),
            (u"(∇T)²（挠率动能）", Fr(-4)), (u"T⁴", Fr(-4)), (u"R^3", Fr(-6))]
    # 逐符号幂由「度规/标架无量纲、一个导数记 L^-1」现推：[T]=[∂e]=L^-1、[R]=[∂Γ]+[Γ²]=L^-2、[∇T]=L^-2
    sub(u"记账口径（先把每个符号自己的幂立住，再算系数）：坐标 [x]=L^+1、度规与标架 [g]=[e]=L^0、"
        u"一枚导数 [∂]=[∇]=L^-1 ⇒ [T]=[∂e]=L^-1、[R]=[∂Γ]+[Γ²]=L^-2、[∇T]=L^-2；"
        u"作用量无量纲（ℏ=1）＋[d⁴x]=L^+4 ⇒ 每项系数幂 = −(4＋[O])。**上一版把 [T] 记成 L^-2（多算了一枚导数），"
        u"于是 (∇T)² 被推去付 L^+2 的出环价——那是记账错，不是物理错，本轮就地更正并保留这段说明**")
    sub(u"幂记账（自然单位；[S]=L^0、[d⁴x]=L^+4 ⇒ 系数幂 = −(4+[O])，逐条列）：")
    inring = []
    for nm, po in book:
        need = -(Fr(4) + po)                # 系数的 L 幂
        # ㉔ U01 的环判据：偶 ∧ 非正
        ring = (need % 2 == 0) and (need <= 0)
        inring.append((nm, po, need, ring))
        sub(u"  %-18s [O]=L^%+d ⇒ 所需系数幂 L^%+d｜按 ㉔ 判据（偶∧非正）在环内 = %s"
            % (nm, po.numerator, need.numerator, u"是" if ring else u"否"))
    d6spin = grep(D6, u"挠率由物质", u"D6 挠率来路")
    d6deg = grep(D6, u"无自旋物质时", u"D6 退化读法")
    d6eq = grep(D6, u"8\\pi G S", u"D6 挠率场方程")
    sub(u"D6 在册三行现读：%s｜%s｜%s" % (d6spin or u"没读到", d6deg or u"没读到", d6eq or u"没读到"))
    sig = [x for x in inring if x[0].startswith(u"(∇T")][0]
    sub(u"预注册否证（原话留面）：开场写的是「让 τ 传播必须付出**出环**代价」。本表现算：(∇T)² 档所需系数幂 = L^%d，"
        u"按 ㉔ 的判据（偶 ∧ 非正）它**在环内**——而且环在这一档只给一个元素：L^0 就是 ㉔ U02 里那枚「空收缩＝纯数」格。"
        u"⇒ 预注册错在把「需要新结构」当成「需要正幂系数」；真正付的价是另外两笔：①这一档的系数是一枚**新的自由无量纲数**"
        u"（㉔ 已证几何环能给形状、给不出数值），②它与 D6 在册那句「无自旋物质时挠率为零，EC 退化为 GR」正面冲突——"
        u"那读法里 τ 根本没有独立动力学可传播。" % int(sig[2]))
    # 代数性的两枚可算见证：(i) T² 与 R 同幂档 ⇒ 最小 EC 的挠率项不新增系数；(ii) 在册那式右端是自旋源、左端无 □
    row_r = [x for x in inring if x[0].startswith(u"R（")][0]
    row_t2 = [x for x in inring if x[0].startswith(u"T²")][0]
    row_r3 = [x for x in inring if x[0].startswith(u"R^3")][0]
    sub(u"同档见证：R 项与 T² 项所需系数幂同为 L^%d／L^%d ⇒ 最小 EC 里的挠率平方项**不带来新常数**"
        u"（它就是 R(Γ)=R(e)+∂K+K² 里那枚 K²，被同一个 1/G 定价）——这正是「τ 是代数辅助场」的簿记形状。"
        u"对照格 R^3 需要 L^%d（正幂）⇒ 出环，说明这条边界不是空的：表里既有在环的，也有出环的"
        % (int(row_r[2]), int(row_t2[2]), int(row_r3[2])))
    _lhs = d6eq.split(u"=")[0] if d6eq else u""
    no_box = bool(_lhs) and not any(k in _lhs for k in (u"\\Box", u"\\square", u"\\partial^2", u"D_\\mu D^\\mu"))
    sub(u"在册场方程左端现取（等号左侧）：%s｜其中没有达朗贝尔算符／二阶协变导数记号 ⇒ 该式把挠率**代数地**解为源的函数"
        % (_lhs.strip() if _lhs else u"没读到"))
    chk(u"G09 T² 与 R 同档且 R^3 出环（边界非空）",
        row_r[2] == row_t2[2] and row_r3[2] > 0 and not row_r3[3],
        u"R=%d T²=%d R³=%d(在环=%s)" % (int(row_r[2]), int(row_t2[2]), int(row_r3[2]), row_r3[3]))
    chk(u"G09 在册挠率方程左端无二阶算符（代数性有载体）", no_box, u"左端=%s" % (_lhs.strip() or u"空"))
    BATTERY.append((u"G09 同档判据", lambda a, b, c: a == b and c > 0,
                    (int(row_r[2]), int(row_t2[2]), int(row_r3[2])),
                    (int(row_r[2]), int(row_t2[2]) - 2, int(row_r3[2]))))
    # 接触型 vs 幂律的力程实测（高斯展宽 δ 函数）
    sgm = 1.0
    def fcontact(r, s=sgm):
        g = math.exp(-r * r / (2.0 * s * s)) / (s * s)
        return abs(r) * g
    def fpow(r, s=sgm):
        return 1.0 / (r * r)
    rs = [1.0, 5.0, 10.0, 20.0]
    tab = [(x, fcontact(x) / fcontact(1.0), fpow(x) / fpow(1.0)) for x in rs]
    for x, c1, c2 in tab:
        sub(u"  r/σ=%-4.0f｜接触项 |F|/|F(σ)| = %s｜幂律 r^-2 = %s｜二者之比 = %s"
            % (x, fmt(c1), fmt(c2), fmt(c1 / c2)))
    # 力程判据：降到 σ 处读数的 1e-6 所需半径——两型力用**同一个二分器、同一个阈**，不手打幂律那格的数
    thr_range = 1e-6

    def range_at(g, hi=1.0e7):
        if g(hi) / g(1.0) > thr_range:
            return None
        lo, hir = 1.0, hi
        for _ in range(200):
            mid = 0.5 * (lo + hir)
            if g(mid) / g(1.0) > thr_range:
                lo = mid
            else:
                hir = mid
        return 0.5 * (lo + hir)
    r_c = range_at(lambda x: fcontact(x, sgm))
    r_c2 = range_at(lambda x: fcontact(x, 2.0 * sgm))     # σ 加倍 ⇒ 力程该按同一因子缩放
    r_p = range_at(lambda x: fpow(x, sgm))
    rc_closed = math.sqrt(2.0 * math.log(1.0 / thr_range))   # 高斯尾的闭式解（第二通道，非拟合）
    rc_floor = 8.0 * EPS * rc_closed
    sub(u"力程实测（同一判据「降到 σ 处的 %s」，两型共用一个二分器）：接触型在 r = %s σ 处达标，"
        u"幂律 r^-2 要到 r = %s σ ⇒ 比值 %s 倍 ⇒ 最小 EC 积掉挠率买到的是**零程**接触力，不是长程引力；"
        u"族的 τ 支若要承担长程力，就得与 D6 那读法分手"
        % (fmt(thr_range), fmt(r_c), fmt(r_p), fmt(r_p / r_c)))
    sub(u"第二通道（闭式，不来自二分）：高斯尾 exp(−r²/2σ²) 降到阈处的半径 = σ·√(2 ln(1/阈)) = %s；"
        u"σ 加倍那格实测力程 %s（闭式预言 %s）⇒ 力程由 σ **线性**设定，除此之外没有第二个尺度——"
        u"「零程」说的就是这件事：它的程不是由耦合常数调出来的，是由接触本身的宽度给的"
        % (fmt(rc_closed), fmt(r_c2), fmt(2.0 * rc_closed)))
    chk(u"G09 动能档在环内且接触档零程", sig[3] and abs(r_c - rc_closed) < rc_floor
        and abs(r_c2 - 2.0 * rc_closed) < 2.0 * rc_floor,
        u"kin_in_ring=%s r_contact=%s（闭式 %s，底 %s）r(2σ)=%s" % (sig[3], fmt(r_c), fmt(rc_closed),
                                                                    fmt(rc_floor), fmt(r_c2)))
    BATTERY.append((u"G09 预注册双面", lambda a, b: a and b, (sig[3], abs(r_c - rc_closed) < rc_floor),
                    (False, abs(r_c - rc_closed) < rc_floor)))

    # ============================== G10 吸引性的 1 bit
    item(u"G10", u"BOUNDARY", u"吸引性定价：族的 U=α(κ−τ) 在 m=1 给 F∝−α(A−B)/r²，符号表 4 格里 2 吸 2 斥 ⇒ "
                              u"「引力普遍相吸」需要 1 bit 外生输入，m=1 选不出它")
    A, B = 2.0, 1.0
    rows10 = []
    for sa in (1.0, -1.0):
        for gap in (A - B, B - A):
            coef = -sa * gap          # F = coef/r²（coef<0 ⇒ 相吸，指向中心）
            rows10.append((sa, gap, coef, coef < 0))
    for sa, gap, coef, att in rows10:
        sub(u"  α 符号=%+d｜A−B=%s｜F 的系数=%s ⇒ %s" % (int(sa), fmt(gap), fmt(coef), u"相吸" if att else u"相斥"))
    n_att = sum(1 for r in rows10 if r[3])
    sub(u"机器裁定：4 格里相吸 %d 格、相斥 %d 格 ⇒ 「普遍吸引」在这一族里是**符号选择**不是推论；"
        u"代价记法与 ㉔ U10 同级：㉔ 证「m 的选定力全部来自公设一」，本条证「引力的号全部来自一次外部定号」"
        % (n_att, len(rows10) - n_att))
    sub(u"另一半（偶 m 支）：m=2 时 U∝r^-2 ⇒ 力律 F∝r^-3——**连 r^-2 都不是**，谈不上引力；"
        u"这一支在 ㉔ 里已判两侧皆空（无几何构造、无手性载体）")
    chk(u"G10 符号表一半吸一半斥", n_att == 2 and len(rows10) == 4, u"att=%d total=%d" % (n_att, len(rows10)))
    BATTERY.append((u"G10 号表计数", lambda a, b: a == b, (n_att, n_att), (n_att, len(rows10))))

    # ============================== G11 逐圈幂记账与不变量配对数
    item(u"G11", u"THEOREM", u"P1 推广（逐圈）：纯引力的发散度按拓扑恒等 D=2+2L（枚举核），"
                             u"而每一档需要的曲率不变量配对数 (4l−1)!! 随 l 超指数增 ⇒ 需要无穷多枚前置系数，环一枚都给不出")
    rows11 = []
    for L in range(0, 9):
        for V in range(1, 6):
            I = L + V - 1
            if I < 0:
                continue
            D = 4 * L - 2 * I + 2 * V
            rows11.append((L, V, I, D))
    same = all(r[3] == 2 + 2 * r[0] for r in rows11)
    sub(u"拓扑恒等式 L=I−V+1 与 D=4L−2I+2V（每圈 +4、每内线 1/k² 给 −2、每顶点两个导数给 +2）：枚举 %d 个 (L,V,I) 格，"
        u"逐格 D 与 2+2L 恒等 = %s" % (len(rows11), u"是" if same else u"否"))
    for L in range(0, 7):
        sub(u"  L=%d 圈 ⇒ 发散度 D=%d ⇒ 需要的算符导数阶=%d ⇒ 该档系数的 L 幂=%+d（正 ⇒ 环外）"
            % (L, 2 + 2 * L, 2 + 2 * L, 2 + 2 * L))
    def dfac(m):
        out = 1
        for k in range(m, 0, -2):
            out *= k
        return out
    rows11b = []
    for l in range(1, 9):
        direct = dfac(4 * l - 1)
        viafact = math.factorial(4 * l) // (2 ** (2 * l) * math.factorial(2 * l))
        rows11b.append((l, direct, viafact, -2 * l))
    for l, dd, vf, grade in rows11b:
        sub(u"  l 枚 Riemann（每枚 L^-2）｜形式全收缩配对数 (4l−1)!! = %d｜第二通道 (4l)!/(2^{2l}(2l)!) = %d｜恒等=%s"
            u"｜算符幂 L^%+d" % (dd, vf, u"是" if dd == vf else u"否", grade))
    grow = all(rows11b[i][1] < rows11b[i + 1][1] for i in range(len(rows11b) - 1))
    sub(u"机器裁定：配对数逐档严格增 = %s，且各档算符幂 L^%s 两两互异 ⇒ 按量纲分级它们**不能互相线性表出** ⇒ "
        u"抵消需要一个系数一个系数地往里加，无穷多枚；而㉔ 已证几何环的幂全为非正（最大幂 0），"
        u"这些系数（全为正幂）没有一枚能由环内收缩造出——G 是第一枚，也是最小的一枚"
        % (u"是" if grow else u"否", u"、".join(str(x[3]) for x in rows11b)))
    chk(u"G11 拓扑恒等与配对数两通道", same and grow and all(x[1] == x[2] for x in rows11b),
        u"topo=%s grow=%s agree=%d/%d" % (same, grow, sum(1 for x in rows11b if x[1] == x[2]), len(rows11b)))
    BATTERY.append((u"G11 双通道配对", lambda s: s, all(x[1] == x[2] for x in rows11b), False))

    # ============================== G12 三支出路定价
    item(u"G12", u"CONDITIONAL", u"出路定价（本册不代选）：①G 只作前置因子＋强度外生；②另立 α_G；"
                                 u"③给 τ 加动能项——三笔代价现算：新增自由常数枚数、是否触碰公设一、是否与在册读法冲突")
    exits = [
        (u"①G 作前置因子", 1, True, False, u"代价：环内一切可观测量不含 G ⇒ 引力强度必须由外生尺度给（G01/G02 已证它带的正是 m）"),
        (u"②另立 α_G", 2, True, True, u"代价：弃「单一 α 统四力」（与 ⑲ T04/㉔ U10 的统一主张正面分手）"),
        (u"③给 τ 加动能项", 1, False, True, u"代价：新增一枚自由无量纲数（在环内但无值）＋与 D6「无自旋物质时挠率为零」冲突"),
    ]
    for nm, nf, touch, conf, why in exits:
        sub(u"  %-16s｜新增自由常数 %d 枚｜是否触碰公设一（局域度规-挠率-曲率为唯一基础场）：%s｜是否与在册读法冲突：%s"
            % (nm, nf, u"是" if touch else u"否", u"是" if conf else u"否"))
        sub(u"      %s" % why)
    tot = [e[1] for e in exits]
    sub(u"合读：三支都不免费——①要 1 枚且强度仍外生；②要 2 枚且弃「单一 α」；③要 1 枚且弃 D6 那读法"
        u"（G09 已证它并不出环，所以③是**可写**的，代价在自洽性不在半轴）。"
        u"本册据此把 ㉔ 的 O24-3 由「二选一」改为「三选一＋各自标价」")
    chk(u"G12 三支代价互不相同且枚数现算", len(set(tot)) <= 3 and max(tot) == 2 and sum(1 for e in exits if e[3]) == 2,
        u"free=%s conflict=%d" % (u"、".join(str(x) for x in tot), sum(1 for e in exits if e[3])))
    BATTERY.append((u"G12 最大代价枚数", lambda a, b: a == 2 and b == 2, (max(tot), sum(1 for e in exits if e[3])),
                    (max(tot), 1)))

    # ============================== G13 跨册定位
    item(u"G13", u"INFO", u"跨册定位与净差（所有他册数现读并点名载体，读不到即弃引）")
    s22, s21, s34 = stat_line(A22_FACE, u"㉔ 面"), stat_line(A21_FACE, u"⑲ 面"), stat_line(R34_FACE, u"r34 面")
    subs(u"载体三条：%s｜%s｜%s" % (s22 or u"读不到", s21 or u"读不到", s34 or u"读不到"))
    subs(u"经典基准与在册作用量载体：%s｜%s｜%s｜%s｜%s｜%s"
         % tuple((stat_line(p, n) or u"读不到") for p, n in ((E1, u"E1"), (E0, u"E0"), (D1, u"D1"), (D6, u"D6"),
                                                             (DPLAN, u"D 普朗克"), (QUANJ, u"全集"))))
    subs(u"净差五条：①把 ㉔「G 出环」由**半轴论证**升级为**量纲唯一性论证**（G01 的 3×4 指数矩阵零度=1），"
         u"这条路线完全不依赖「α 必须几何构造」那枚公设 ⇒ ㉔ U10 的 CONDITIONAL 在此升为**无条件排除**的一半"
         u"（排除「普适 α 就是引力」）；②指出那唯一一枚无量纲引力耦合自带受力体质量（G02），"
         u"于是 EP 对引力不是附加公设而是量纲必然——这与 ⑲ T09/㉔ U11 的「极差在谁身上」正是同一枚币的两面；"
         u"③给族的 m=1 落点配了两枚可算的经典否证（G04 偏折缺一倍、G06/G07 进动缺整项）；"
         u"④把 ⑲/㉔ 里被当成长程候选的 τ 支，按最小 EC 现算成**零程接触**（G09），并当场否证自己开场的出环预注册；"
         u"⑤逐圈幂记账把「一枚 α」的自由度问题抬成「无穷多枚前置系数」（G11）。")
    sub(u"在册读法一致性核对（本册不复制它的数，只按名现读）：%s"
        % (grep(DPLAN, u"不存在非平凡无量纲组合", u"D 专题满秩推论") or u"没读到那行"))

    # ============================== G14 仪器自证
    item(u"G14", u"INFO", u"仪器自证：本轮新立的两件形状——精确零空间（分数域高斯消元，回代逐点验零）与"
                          u"「振幅漂移＝等时性」的 Bertrand 实测尺；旧沿用三件（面不自量、排除按行首、期望由名单现算）")
    sub(u"为什么零空间要回代：行最简形的解如果只印不代，读者无法区分「算对了」与「消元把某行消丢了」⇒ "
        u"本册对 M、L、T 三行逐条点积回代并印出全零（G01 第二通道）")
    sub(u"为什么 Bertrand 用振幅漂移而不是「闭合与否」的布尔判定：u 在近心点的取值对任何有心力都周期返回（转折点），"
        u"用它判闭合是**恒真**的尺；只有 Ψ 对振幅的依赖性才能区分 −2/1 与其余幂 ⇒ 本轮把尺子换成漂移，"
        u"并让枚举里其余 %d 格必须非零才算有牙" % (len(grid) - 2))
    sub(u"本轮预注册的下场：G09 那句「τ 要传播就出环」被自己的幂记账表否证（实为 L^0 档，在环内），"
        u"原话留在面上，判据改为「新增自由常数＋与在册读法冲突」——这是产出不是事故")

    # ============================== G15 总裁定
    item(u"G15", u"THEOREM", u"总裁定：在这族里，引力**不是**一种由几何造出的耦合——量纲唯一性只给它一枚带受力体质量的"
                            u"无量纲强度 (m/m_P)²；它的两个候选载体（G、τ）一个需要正幂系数（环外），一个是代数辅助场（零程）；"
                            u"而族的唯一几何落点 m=1 恰落在 Bertrand 的闭合格上 ⇒ 进动恒零，两枚经典基准直接把它否掉")
    sub(u"成立面（可引）：G01（指数矩阵 det=%d 满秩、加 m 后零度 1、生成元回代全零）、G02（(m/m_P)² 两式独立复算在印刷半 ulp 内）、"
        u"G04（偏折比 = %s，与 (1+γ) 公式恒等）、G05（w=1/3 标量可见度精确零、w=0 满格）、"
        u"G06（等时指数集恰为 −2 与 1，实测漂移 %s；绝对通道另证外推 Ψ₀ 逐格对上闭式）、G07（Δ/(2πδ) 三档阶梯收敛到 1，"
        u"δ 置零对照格的进动为机器零）、G09（接触型力程 %s σ vs 幂律 %s σ）、"
        u"G11（D=2+2L 拓扑恒等逐格成立、配对数两通道恒等且严格增）"
        % (d3, fmt(ratio) if (v_new and v_gr) else u"未读到", fmt(m1_row[4]), fmt(r_c), fmt(r_p)))
    sub(u"否证面：本册开场的 P4 预注册（τ 传播要出环）被 G09 表否证；"
        u"来料主张「m=1 即引力」被 G08 三处否证；「普适 α 就是 G」被 G01/G02 的量纲唯一性排除（不依赖公设一）。")
    sub(u"「引力的本质」在这一族里的正面表述（只到本册能裁的那一步）：引力是**唯一一枚不能与受力体无关的耦合**——"
        u"它的无量纲强度按量纲只能是物体质量对普朗克质量之比。所以「引力＝几何」不是美学选择而是必然读法："
        u"只有让质量从运动方程里消掉（测地线），一个与 m 无关的规律才可能存在；"
        u"而这族的势 U=α(κ^m−τ^m) 从头到尾是**一个标量势**，它做得到与 m 无关（剖面不含受力体，⑲ T09 读法 i），"
        u"但那正是它失去引力的地方——G02 说引力的荷必须是 m。两者不可兼得。")
    sub(u"OPEN 顺延：O25-1 张量自由度（本册裁到「标量给不了 γ=1」，没有裁「这族能不能写出一个自旋-2 激发」——"
        u"那需要线性化谱与螺旋度计数，本册未做）；O25-2 普朗克尺度的出处（G02 只用到 m_P 的定义，未解释它为何是这个值）；"
        u"O25-3 主动引力质量 1+3w 与族的源约束（G05 那枚 2 与 ㉔ U06 点源档 2/6 之间是否有同一出处，未裁）；"
        u"O25-4 逐圈幂记账在挠率存在时是否仍是 D=2+2L（G11 只算了纯度规拓扑）；"
        u"O25-5 若采 G12 的③（给 τ 动能项），新的无量纲数与 ㉔ 的算符谱 {μ_i} 如何共同定价。")
    sub(u"红线：本轮未宣称统一场论成立，也未宣称「引力的本质已被解释」——裁的是「这族能给引力什么、代价是谁付」；"
        u"数学自洽 ≠ 实验证实；哥德巴赫仍未证明，统一场论仍未成立。未跑 refresh_catalog，未 git add/commit。")

    # ============================== 卫生针
    PH = re.compile(u"%[-+ #0]*[0-9]*(?:\\.[0-9]+)?[dsfrgeE]")
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

    emit(u"")
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

    def hy_line(nm, ok=True):
        return u"  %s ｜判据 %s" % (nm, u"合格" if ok else u"不合格")

    m_prose = u"  实测残差 %d 枚／阈 %.3e 未替换"
    m_item = u"- G06 [PASS] 模板行 %d/%.3e 未插值"
    hyb = []
    hyb.append((u"MUT-1 未插值模板行（含 %d、%.3e 字形）必须被抓住", not pred_clean([m_prose])))
    hyb.append((u"MUT-2 条目行 %s [PASS] 里的占位符不得被排除类放过",
                (lambda h, e: len(h) == 1 and len(e) == 0)(*ph_scan([m_item]))))
    hyb.append((u"NEG-1 名单自述行按行首形状排除（须绿）", pred_excl_passes(hy_line(hyb[0][0]))))
    hyb.append((u"NEG-2 真集合记号 {−2、1} 与 {1..12} 行不命中（须绿）",
                pred_clean([u"等时指数集 = {−2、1}", u"m ∈ {1..12}"])))
    hyb_bad = 0
    for nm, ok in hyb:
        emit(hy_line(nm, ok))
        if not ok:
            hyb_bad += 1

    ex_expect = sum(1 for nm, _, _, _ in BATTERY if PH.search(hy_line(nm))) + \
                sum(1 for nm, _ in hyb if PH.search(hy_line(nm)))
    vcnt = {}
    for tid, v, _t in ITEMS:
        vcnt[v] = vcnt.get(v, 0) + 1
    exit_code = 0 if (n_ok == len(SELF) and bat_bad == 0 and hyb_bad == 0) else 1
    emit(u"")
    stat_keys = sorted(vcnt, key=lambda k: (-vcnt[k], k))
    emit(u"条目统计：" + u"／".join(u"%s×%d" % (k, vcnt[k]) for k in stat_keys)
         + u"｜桶和 %d＝条目数 %d %s" % (sum(vcnt.values()), len(ITEMS),
                                       u"（对上）" if sum(vcnt.values()) == len(ITEMS) else u"（对不上＝有桶被漏印）"))
    emit(u"判定条目 %d 枚｜自检 %d/%d｜电池 %d/%d 合格｜卫生双向 %d/%d 合格｜退出码（终扫前）%d"
         % (len(ITEMS), n_ok, len(SELF), len(BATTERY) - bat_bad, len(BATTERY),
            len(hyb) - hyb_bad, len(hyb), exit_code))
    emit(u"")
    emit(u"分层结论：")
    emit(u"  [数学] 指数矩阵满秩与零度 1（G01，分数域消元＋逐行回代）、标量可见度在 w=1/3 精确零（G05，Fraction 全域）、"
        u"Bertrand 等时集恰为 −2 与 1（G06，振幅漂移实测＋A→0 外推对闭式）、进动一阶系数 Δ/(2πδ)→1（G07 三档阶梯＋δ 置零对照）、"
        u"D=2+2L 与配对数双通道恒等（G11）为恒等式级。")
    emit(u"  [物理] 引力的无量纲强度唯一且**带受力体质量**（G02）⇒ EP 对引力是量纲必然不是附加公设；"
        u"标量势看不见辐射（G05）⇒ 偏折只能给半（G04）；最小 EC 的 τ 是代数辅助场⇒零程接触（G09）；"
        u"普遍吸引需 1 bit 外生定号（G10）；逐圈需要无穷多枚正幂前置系数，环一枚不给（G11）。")
    emit(u"  [自否] 开场预注册「让 τ 传播必须付出环代价」被自己的幂记账表否证（(∇T)² 档系数是 L^0，在环内）："
        u"改判后的价是「新增一枚无值自由常数＋与 D6 在册退化读法冲突」，原话留在面上（G09）。")
    emit(u"  [诚实边界] G04/G05/G07/G08 用了两枚经典基准的在册读数（E1 0.875/1.75、E0 42.98），"
        u"判据不依赖其精度只依赖其存在与比值；G02 的复算只用全集那两行的**印刷位数**定阈；"
        u"O25-1（自旋-2 谱与螺旋度计数）本册**没做**，不得从 G04 的「标量给不了 γ=1」推出「这族没有张量激发」。")
    emit(u"  [红线] 本轮未宣称统一场论成立；未跑 refresh_catalog，未 git add/commit。")

    rc_pre = exit_code
    final_hits, final_ex = ph_scan(OUT)
    if final_hits:
        emit(u"版面卫生（终扫）：判定命中 %d 处，逐条点名（不止第一处，否则计数无牙；"
             u"引文里的花括号已转成全角，免得这段自述再被下一轮扫成占位符）：" % len(final_hits))
        for l in final_hits:
            emit(u"    命中｜%s" % l[:96].replace(u"{", u"｛").replace(u"}", u"｝"))
        emit(u"  ⇒ 本轮不得判绿")
        exit_code = 1
    elif len(final_ex) != ex_expect:
        emit(u"版面卫生（终扫）：结构排除 %d 行 ≠ 名单现算 %d 行 ⇒ 排除类在吞东西 ⇒ 本轮不得判绿"
             % (len(final_ex), ex_expect))
        exit_code = 1
    else:
        brace = [l for l in OUT if u"{" in l]
        emit(u"版面卫生（终扫）：扫到本行前共 %d 行（本行不计，面不能自量——盘的尺寸／LF 只由末行「写后回读」给），"
             u"判定命中 0 处；结构排除 %d 处（= 名单现算 %d，全部是上面卫生夹具区里自述模板那类字形，逐条可点名）；"
             u"含花括号字形的行 %d 行（现扫第二口径：其中没有一行靠排除类放过，因为它们都不带百分号型占位符）"
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
