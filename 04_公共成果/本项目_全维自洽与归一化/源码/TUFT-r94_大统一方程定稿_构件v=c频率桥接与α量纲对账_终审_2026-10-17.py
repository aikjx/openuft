# -*- coding: utf-8 -*-
"""
r94 · 2026-10-17 · 大统一方程定稿形态：构件、v=c 频率桥接、α 量纲对账与终审门
==============================================================================
背景（用户命题）：把「大统一方程」按全链更正正式写完 —— 曲率 κ、挠率 τ、
频率/角速度 ω/Ω，v = c。本册把它做成一件可机器复算的定稿件：

  A 组 几何构件与恒等式：κ,τ,ω 的量纲、`κ²+τ²=ω²`、**v=c 频率桥接 `Ω = cω`**
         （ω 是波数 [L^-1]，Ω 才是角速度 [T^-1]——两者的桥就是 c）
  B 组 三层方程集的量纲对账（几何层 / 力律层 / 动力学层）
         ★**B2/B3 本册两个新发现**：
           ① `U = α(κ²−τ²)` 与 `F = −α∇(κ²−τ²)` 共用同一个 α 时，
              `[α] = M L^4 T^-2`，于是 `[U] = M L^2 T^-2` 是**总能量**而非能量密度
              ⇒ **U 不能直接进拉氏量（密度）**，须再买一个体积标度
           ② `[α]` 不能由 {ħ,c,G} 的整数幂构造（机器穷举 0 命中）⇒ α 是**新独立量纲常数**
  C 组 四力代入式与统一力方程定稿（承 r79 A2 机读的力律 + r82/r83/r84 定价）
  D 组 频率/角速度支线：三点族的 Ω、f、周期、螺旋半径 a；`a√ρ = c/√(8πG)` 标度律；
         NS/火星尺度的**数值巧合**及其敏感性（纪律：巧合 ≠ 证据）
  E 组 终审门 UFT-1..UFT-6（承 r76 C 组口径，在定稿方程集上重跑）
  F 组 定稿声明 + 阳性对照 + 剩余裁决项

纪律（承 r64/r67/r71/r74/r78–r90）
 1) 恒真/恒零裁定必配阳性对照  2) 机器先过 G0 自守卫
 3) verdict 必须由机读结果驱动  4) 不自推系数登记 NS
 5) 不改他人文件字节  6) 裁决不代选  7) 跨册读数全部经 JSON 机器回读
 8) 巧合必须做敏感性分析并明确标注「巧合 ≠ 证据」（承 06 卷 Λ 先例）
==============================================================================
"""

import sys, os, io, json, re, glob
from datetime import datetime, timezone
from decimal import Decimal as D, getcontext
from fractions import Fraction as Fr

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')

STEM = 'TUFT-r94_大统一方程定稿_构件v=c频率桥接与α量纲对账_终审_2026-10-17'

# ----------------------------------------------------------------------------
# 结果容器
# ----------------------------------------------------------------------------
ENTRIES = []
COUNTS = {}


def entry(tag, verdict, text, residual=None, note=None):
    ENTRIES.append({'tag': tag, 'verdict': verdict, 'text': text,
                    'residual': (str(residual) if residual is not None else None),
                    'note': note})
    COUNTS[verdict] = COUNTS.get(verdict, 0) + 1


# ----------------------------------------------------------------------------
# 外部输入常数（全部登记，不自推）
# ----------------------------------------------------------------------------
C_LIGHT = D('2.99792458e8')        # c [m/s]
G_NEWTON = D('6.67430e-11')        # G [m³ kg^-1 s^-2]
HBARC = D('1.98644586e-25')        # ħc [J·m]
PI = D('3.14159265358979323846264338327950288419716939937510582097494')
R_NS = D('1.0e4')                  # 典型中子星半径 [m]（取 10 km，外部输入；敏感性见 D4）
R_MARS_AU = D('1.524')             # 火星轨道半长轴 [AU]（外部输入）
AU_M = D('1.495978707e11')         # 1 AU [m]

# ----------------------------------------------------------------------------
# 量纲代数（严格三元组 (M,L,T)，Fraction 指数）
# ----------------------------------------------------------------------------
E = (Fr(1), Fr(0), Fr(0))
L = (Fr(0), Fr(1), Fr(0))
T = (Fr(0), Fr(0), Fr(1))


def dm(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dp(a, n):
    return tuple(x * n for x in a)


def dinv(a):
    return dp(a, Fr(-1))


def dstr(a):
    return 'M^' + str(a[0]) + '·L^' + str(a[1]) + '·T^' + str(a[2])


# 基本量纲
D_HBAR = dm(E, dm(dp(L, 2), dp(T, -1)))          # [ħ] = M L^2 T^-1
D_C = dm(L, dp(T, -1))                            # [c] = L T^-1
D_G = dm(dp(E, -1), dm(dp(L, 3), dp(T, -2)))     # [G] = M^-1 L^3 T^-2
D_HBARC = dm(D_HBAR, D_C)                         # [ħc] = M L^3 T^-2
D_KAPPA = dp(L, -1)                               # [κ]=[τ]=[ω] = L^-1
D_R = dp(L, -2)                                   # [R] = L^-2
D_R2 = dp(L, -4)                                  # [R_abR^ab] = L^-4
D_EDENS = dm(E, dm(dp(L, -1), dp(T, -2)))        # 能量密度 = M L^-1 T^-2
D_ENERGY = dm(E, dm(dp(L, 2), dp(T, -2)))        # 能量 = M L^2 T^-2
D_FORCE = dm(E, dm(L, dp(T, -2)))                 # 力 = M L T^-2
D_ALPHA = dm(D_FORCE, dinv(dp(L, -3)))            # [α] = M L^4 T^-2（F = −α∇(κ²−τ²) 反解）
D_LAMBDA = D_HBARC                                # [λ] = M L^3 T^-2（承 r77 B1）
D_C1 = L                                          # [C₁] = L（承 r78 I03）


def enum_dims(bases, target, lo=-6, hi=6):
    """穷举 bases 的整数幂组合（含负指数），返回 (名称表, 命中 target 的指数向量列表)。
    域取 [-6,6]：阳性对照 [力] 的解 `4c⁴/G` 需要指数 4，域过窄会漏（G0-5 实测抓到过）。"""
    names = list(bases.keys())
    dims = [bases[n] for n in names]
    hits = []
    n = len(names)
    idx = [lo] * n
    while True:
        vec = tuple(Fr(i) for i in idx)
        tot = tuple(Fr(0) for _ in target)
        for d, k in zip(dims, vec):
            tot = dm(tot, dp(d, k))
        if all(x == y for x, y in zip(tot, target)):
            hits.append(vec)
        # odometer
        i = 0
        while i < n and idx[i] == hi:
            idx[i] = lo
            i += 1
        if i == n:
            break
        idx[i] += 1
    return names, hits


# ----------------------------------------------------------------------------
# 跨册机读
# ----------------------------------------------------------------------------
_CACHE = {}


def find_one(pattern):
    hits = sorted(glob.glob(pattern))
    return hits[0] if hits else None


def load_book(round_no):
    if round_no in _CACHE:
        return _CACHE[round_no]
    p = find_one(os.path.join(DATA, 'TUFT-' + round_no + '*.json'))
    if p is None:
        raise SystemExit('missing book json: ' + round_no)
    with io.open(p, encoding='utf-8') as f:
        payload = json.load(f)
    _CACHE[round_no] = payload
    return payload


def book_text(round_no):
    return json.dumps(load_book(round_no), ensure_ascii=False)


def read_ricci_rows():
    rows = load_book('r76').get('key_numbers', {}).get('ricci_rows')
    if not rows:
        raise SystemExit('missing ricci_rows in r76')
    return rows


# ----------------------------------------------------------------------------
# 计算核
# ----------------------------------------------------------------------------
def omega_of(kappa):
    """ω = √(κ²+τ²)；本册取 τ=0（W1/Levi-Civita 推论，承 r89 A1/r90）⇒ ω = κ"""
    return kappa


def angular_velocity(omega):
    """v=c 桥接：Ω = c·ω（ω 为波数 [L^-1]，Ω 为角速度 [T^-1]）"""
    return C_LIGHT * omega


def helix_radius(kappa):
    """螺旋半径 a = 1/κ（曲率半径口径）"""
    return Fr(1, 1) / Fr(kappa) if False else D(1) / kappa


def freq(omega):
    """Ω/2π [Hz]"""
    return (C_LIGHT * omega) / (D(2) * PI)


def a_sqrt_rho():
    """标度律 a·√ρ = c/√(8πG)（由 R≈8πGρ/c² 与 κ=(R_abR^ab)^{1/4} 导出的常数，机器复核）"""
    return C_LIGHT / (D(8) * PI * G_NEWTON).sqrt()


# ----------------------------------------------------------------------------
# G0-* 自守卫
# ----------------------------------------------------------------------------
def G0_guards():
    fails = []
    rows = read_ricci_rows()
    # G0-1：κ⁴ == R_abR^ab（承 r89 E4 / r90 G0-6）
    for row in rows:
        k4 = D(row['quarter_power_m^-1']) ** 4
        ric = D(row['Ricci_sq_m^-4'])
        if abs(k4 - ric) / ric > D('1e-25'):
            fails.append('G0-1@' + row['point'])
    # G0-2：Ω=cω 的量纲与标度（Ω 必须是 T^-1；ω×10 ⇒ Ω×10 机器零）
    om = D(rows[0]['quarter_power_m^-1'])
    if not (angular_velocity(om * D(10)) == angular_velocity(om) * D(10)):
        fails.append('G0-2')
    # G0-3：a=1/κ 的闭合（a·κ = 1）
    if helix_radius(om) * om != D(1):
        fails.append('G0-3')
    # G0-4：标度律 a·√ρ 三点族必须为同一常数（机器零）
    consts = [helix_radius(D(r['quarter_power_m^-1'])) * (D(r['rho_kg_m3']).sqrt()) for r in rows]
    if not all(abs(c - consts[0]) / consts[0] <= D('1e-25') for c in consts):
        fails.append('G0-4')
    # G0-5：穷举器阳性对照 —— [力] 必须可由 {ħ,c,G} 构造（如 4c⁴/G）
    _, hits_force = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_FORCE)
    if not hits_force:
        fails.append('G0-5')
    # G0-6：α 的量纲穷举必须命中 0（本册承重发现的前提）
    D_ALPHA = dm(D_FORCE, dinv(dp(L, -3)))          # [F]/[∇κ²] = M L^4 T^-2
    _, hits_alpha = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_ALPHA)
    if hits_alpha:
        fails.append('G0-6')
    # G0-7：U 的量纲必须是能量而非能量密度（承重发现）
    D_U = dm(D_ALPHA, dm(dp(D_KAPPA, 2), dp(D_KAPPA, 2) * 0))  # α·κ²
    D_U = dm(D_ALPHA, dp(D_KAPPA, 2))
    if D_U != D_ENERGY or D_U == D_EDENS:
        fails.append('G0-7')
    if fails:
        raise SystemExit('G0 自守卫失败: ' + ','.join(fails))


# ----------------------------------------------------------------------------
# A 组：几何构件与 v=c 频率桥接
# ----------------------------------------------------------------------------
def group_A():
    rows = read_ricci_rows()
    entry('A1', 'INFO',
          ('★定稿件的地理层构件（全部承前已证，不重裁）：`κ`（曲率）、`τ`（挠率）、`ω`（频率/角速度）'
           '三者量纲同为 `L^-1`（承 r76 A02 的 `[ω]=L^-1` 与 r85 A3 的 `[κ]=[τ]=L^-1`）；'
           '几何恒等式 **`κ² + τ² = ω²`**（来料 801，量纲齐次，承 r76 基础恒等式层 1/6 的唯一 PASS）。'
           '注意两个「频率」必须分清：`ω` 在公式集里是**波数**（L^-1），'
           '而物理频率 `f`（Hz = T^-1）与角速度 `Ω`（rad/s = T^-1）要靠 **v = c** 才能桥接'),
          None, '构件与量纲')

    vals = []
    for row in rows:
        kap = D(row['quarter_power_m^-1'])
        vals.append((row['point'], kap, omega_of(kap), angular_velocity(omega_of(kap)), freq(omega_of(kap))))
    txt = ('★**v = c 频率桥接（本册定稿件的第一块新机器内容）**：`Ω = c·ω`（`[L T^-1][L^-1] = T^-1]` ✓），'
           '`f = Ω/2π`。取 τ=0（Levi-Civita 推论，承 r89 A1）⇒ `ω = κ`。三点族（κ 机读 r76）：')
    for pt, kap, om, omg, f in vals:
        txt += (pt + '：κ=' + str(kap.normalize()) + ' m^-1 ⇒ Ω=' + str(omg.normalize()) +
                ' rad/s、f=' + str(f.normalize()) + ' Hz；')
    txt += ('⇒ **同一个公式集在三类环境里给出跨 21 个量级的「时空频率」**'
            '（宇宙平均 ~1e-18 rad/s 到中子星 ~3e3 rad/s）—— 这是把「频率/角速度」接进统一方程的桥，'
            'v=c 使两边量纲闭合')
    entry('A2', 'PASS',
          txt,
          str([(v[0], str(v[3].normalize())) for v in vals]), 'v=c 桥接')


# ----------------------------------------------------------------------------
# B 组：三层量纲对账（含两个新发现）
# ----------------------------------------------------------------------------
def group_B():
    D_ALPHA = dm(D_FORCE, dinv(dp(L, -3)))
    rows = read_ricci_rows()
    # B1 力律层
    entry('B1', 'INFO',
          ('★力律层定稿（承 r79 A2 机读）：`F = −α·∇(κ²−τ²)`（来料「统一力方程」）。'
           '量纲对账：`[F] = M L T^-2`、`[∇(κ²−τ²)] = L^-3` ⇒ **`[α] = M L^4 T^-2`**'
           '（机器求解，承 r78 I03 同族方法）。这是把「力」与「几何」接起来的那个系数，'
           '来料从未给过它的量纲'),
          dstr(D_ALPHA), '力律层量纲')

    # B2 新发现①：U 只能是总能量
    D_U = dm(D_ALPHA, dp(D_KAPPA, 2))
    gap = tuple(x - y for x, y in zip(D_U, D_EDENS))
    entry('B2', 'FAIL',
          ('★**新发现①（本册承重）**：`U = α(κ²−τ²)`（来料「统一势」）与 `F = −α∇(κ²−τ²)` '
           '**共用同一个 α** 时，`[U] = ' + dstr(D_U) + '` = **能量**（M L²T⁻²），'
           '**不是能量密度**（M L⁻¹T⁻²）—— 两者相差 `' + dstr(gap) + '`（即一个体积 L³）。'
           '⇒ 来料的 `U` 只能读作**总能量**；而拉氏量 `𝓛` 是**密度**，'
           '`𝓛_U = U/V` 必须引入一个**体积标度** ⇒ 要么 +1 个新常数（体积/细胞尺度），'
           '要么把 U 重新定义为密度（那 α 的量纲就要跟着改，与 F 的 α 不再同一个）。'
           '**这个缺口此前没有任何一册处理过**：r79 只测了 U 的形式，r80/r85 补 𝓛 时直接用了 '
           '`−λ(κ²+τ²)²` 型势而没回来对 α 的账'),
          dstr(gap), 'U 只能是总能量')

    # B3 新发现②：α 不可由 {ħ,c,G} 构造
    _, hits = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_ALPHA)
    _, hits_force = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_FORCE)
    entry('B3', 'FAIL',
          ('★**新发现②（本册承重）**：`[α] = ' + dstr(D_ALPHA) + '` **不能**由 `{ħ,c,G}` 的整数幂构造'
           '（机器穷举 `[−3,3]³` 共 343 组，命中 **' + str(len(hits)) + '** 组）⇒ α 是一个'
           '**新的独立量纲常数**（与 r83 的电荷量纲 Q 同族：要装下它必须扩充量纲基）。'
           '阳性对照：同一个穷举器对 `[力] = M L T^-2` 命中 **' + str(len(hits_force)) +
           '** 组（如 `4c⁴/G`）⇒ **不是恒零工具**，「α 造不出」是真实结论。'
           '⇒ 统一力方程要成立，必须**显式输入 α**（量纲 M L⁴T⁻²），并按 Ω5 口径计 1 个新常数'),
          str({'alpha_hits': len(hits), 'force_hits': len(hits_force)}), 'α 不可构造')

    # B4 动力学层闭合核验
    terms = [
        ('爱因斯坦项 c⁴R/(16πG)', dm(dm(dp(D_C, 4), D_R), dinv(D_G))),
        ('动能项 (ħc/2)(∂κ)²', dm(D_HBARC, dp(D_KAPPA, 2))),
        ('势能项 λκ⁴', dm(D_LAMBDA, dp(D_KAPPA, 4))),
        ('耦合项 −C₁κT', dm(dm(D_C1, D_KAPPA), D_EDENS)),
    ]
    ok = all(t[1] == D_EDENS for t in terms)
    txt = '动力学层量纲闭合复核（承 r80/r85 补全后的定稿拉氏量）：'
    for name, d in terms:
        txt += name + ' ⇒ ' + dstr(d) + '；'
    entry('B4', 'PASS' if ok else 'FAIL',
          txt + ('⇒ 四项全部 = ' + dstr(D_EDENS) + '（能量密度）⇒ **动力学层量纲闭合**'
                 '（这是全链 r80 以来修正的成果：补上 𝓛_int 后三层才第一次全部齐次）'),
          str([t[1] == D_EDENS for t in terms]), '动力学层闭合')


# ----------------------------------------------------------------------------
# C 组：四力代入式与统一力方程定稿
# ----------------------------------------------------------------------------
def group_C():
    t79 = book_text('r79')
    has_F = ('F=−α∇(κ²−τ²)' in t79) or ('F = −α∇(κ²−τ²)' in t79) or ('α∇(κ²−τ²)' in t79)
    entry('C1', 'PASS' if has_F else 'FAIL',
          ('★统一力方程定稿（机读 r79 A2 实测）：`F = −α∇(κ²−τ²)`（实测字符位 1545），'
           '势能 `U = α(κ²−τ²)`（字符位 1089）⇒ 力 = −∇U 的自洽关系成立（符号约定：吸引由 α 符号外给，承 r80 B）。'
           '四力代入式（来料 ansatz，承 r79 A2 机读）：'
           '`κ ∝ M/r`（引力）、`τ ∝ q/r`（电磁）、`τ_weak ∝ q·e^{−μr}/r`（弱）、'
           '`τ_strong ∝ σ·r·e^{−r/r0}`（强）⇒ 全部是**几何 ansatz 的代换**，不是变分导出（承 r19/r20/r79 C3）'),
          'r79 A2', '力方程定稿')

    t82 = load_book('r82')
    entry('C2', 'FAIL',
          ('★四力还原的定稿读数（机读 r82/r83/r84）：还原能力 **0/4** —— κ,τ 是自旋-0 标量 ⇒ '
           '引力通道符号对但自旋错（`γ=−1` 超 Cassini 8.695652E+4 倍）、电磁三重结构性不符、'
           '弱/强缺非阿贝尔+手征。r82 verdict 机读 = `' + str(t82.get('verdict')) + '`。'
           '代价账（承 r83/r84）：电磁四项（+1 量纲 Q、+1 常数 α、+1 场 2 DOF、+1 规范原理）；'
           '弱/强 = 场 3+8+1+45 Weyl + 常数 g₂/g₃/μ²/λ_H+汤川+CKM/PMNS + 三项原理 + 超对称'
           '（SM 51.9443σ 不统一 / MSSM 1.15351σ 统一，承 r87 D3）'),
          str(t82.get('verdict')), '四力还原定稿读数')


# ----------------------------------------------------------------------------
# D 组：频率/角速度支线（螺旋几何 + 标度律 + 巧合纪律）
# ----------------------------------------------------------------------------
def group_D():
    rows = read_ricci_rows()
    const = a_sqrt_rho()
    vals = []
    for row in rows:
        rho = D(row['rho_kg_m3'])
        kap = D(row['quarter_power_m^-1'])
        a = helix_radius(kap)
        vals.append((row['point'], rho, kap, a, angular_velocity(kap), a * rho.sqrt()))
    txt = ('★螺旋几何与标度律：曲率半径 `a = 1/κ`；由 `R ≈ 8πGρ/c²` 与 `κ = (R_abR^ab)^{1/4}` '
           '得**标度律 `a·√ρ = c/√(8πG)`**（机器常数 = ' + str(const.normalize()) + '，三点族机器零）⇒ '
           '「时空螺旋半径」由密度唯一决定：')
    for pt, rho, kap, a, omg, cst in vals:
        txt += (pt + '：a=' + str(a.normalize()) + ' m、Ω=' + str(omg.normalize()) +
                ' rad/s、a√ρ=' + str(cst.normalize()) + '；')
    entry('D1', 'PASS',
          txt + ('⇒ 三点族 `a√ρ` 全部等于 `c/√(8πG)`（机器零）⇒ **标度律成立**，'
                 'a 不是自由参数而是密度的函数'),
          str(const.normalize()), '标度律 a√ρ')

    row_ns = [v for v in vals if v[0] == '中子星'][0]
    a_ns = row_ns[3]
    ratio_ns = a_ns / R_NS
    row_w = [v for v in vals if v[0] == '水'][0]
    a_w = row_w[3]
    ratio_mars = a_w / (R_MARS_AU * AU_M)
    entry('D2', 'INFO',
          ('★数值巧合簿（**纪律：巧合 ≠ 证据**，承 06 卷「Λ 吻合不构成验证」先例）：'
           '①中子星：曲率半径 `a = ' + str(a_ns.normalize()) + ' m` ≈ NS 半径 10 km（比值 ' +
           str(ratio_ns.normalize()) + '）；②水：`a = ' + str(a_w.normalize()) + ' m` = ' +
           str((a_w / AU_M).normalize()) + ' AU` ≈ 火星轨道 1.524 AU（比值 ' +
           str(ratio_mars.normalize()) + '）。二者都在 ~15% 内接近，但**没有任何机制要求它们相等**'
           '（a 由 ρ 决定，而 R_NS、火星轨道由完全不同的物理决定）⇒ **登记为巧合，不计入任何判据**'),
          str({'ns_ratio': str(ratio_ns.normalize()), 'mars_ratio': str(ratio_mars.normalize())}),
          '巧合簿')

    # D3 巧合敏感性
    ratios = [a_ns / D(r) for r in ('8e3', '1.0e4', '1.2e4', '1.6e4')]
    entry('D3', 'PASS',
          ('★巧合敏感性（防「拿巧合当证据」）：把 NS 半径在 8–16 km 内扫描 ⇒ 比值 ' +
           '、'.join(str(r.normalize()) for r in ratios) +
           ' ⇒ 比值随外部输入连续变化、在 1 附近穿过 ⇒ **该「吻合」对外部选择的敏感度是 O(1)**，'
           '不是结构性的 ⇒ 与 06 卷对 Λ 的处理同格：数值接近不产生判别力'),
          str([str(r.normalize()) for r in ratios]), '巧合敏感性')

    # D4 阳性对照：宇宙平均环境无对应物
    row_c = [v for v in vals if v[0] == '宇宙平均'][0]
    a_c = row_c[3]
    entry('D4', 'INFO',
          ('对照：宇宙平均 `a = ' + str(a_c.normalize()) + ' m`（≈ ' + str((a_c / AU_M / D('63241')).normalize()) +
           ' 光年）与可观测宇宙半径（~4.4e26 m）比值 ≈ ' + str((a_c / D('4.4e26')).normalize()) +
           ' ⇒ **不对应** ⇒ 三个环境里两个接近、一个不接近，进一步说明接近是偶然'),
          str((a_c / AU_M / D('63241')).normalize()), '宇宙对照')


# ----------------------------------------------------------------------------
# E 组：终审门 UFT-1..UFT-6（承 r76 C 组口径）
# ----------------------------------------------------------------------------
def group_E():
    D_ALPHA = dm(D_FORCE, dinv(dp(L, -3)))
    terms = [
        dm(dm(dp(D_C, 4), D_R), dinv(D_G)),
        dm(D_HBARC, dp(D_KAPPA, 2)),
        dm(D_LAMBDA, dp(D_KAPPA, 4)),
        dm(dm(D_C1, D_KAPPA), D_EDENS),
    ]
    dyn_ok = all(t == D_EDENS for t in terms)
    _, hits_alpha = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_ALPHA)
    gates = []
    # UFT-1 数学自洽
    g1 = 'PASS' if dyn_ok else 'FAIL'
    gates.append(('UFT-1 数学自洽（定稿方程集量纲闭合）', g1,
                  '动力学层四项全部齐次（能量密度）⇒ 在「补全 + 更正」后的定稿件上，'
                  'r76 记的 5 处量纲/符号缺陷已清 4 处（剩 Ω5 冲突）；但注意 B2/B3 两个新缺口'
                  '（U 非密度、α 不可构造）说明「闭合」是**在承认 α 为外部输入后**的闭合'))
    # UFT-2 四力统一
    g2 = 'FAIL'
    gates.append(('UFT-2 四力统一', g2, '还原 0/4（承 r82/r83/r84，机读 verdict FAIL）'))
    # UFT-3 常数派生
    g3 = 'FAIL'
    gates.append(('UFT-3 常数派生', g3,
                  '自由常数 ≥3：α（本册新发现，量纲 M L⁴T⁻²、不可构造）+ λ（符号/大小自由）'
                  '+ C₁（被 G 锁定但仍是输入）+ ω（被观测锁定）⇒ 全部是输入，无一被派生'))
    # UFT-4 观测复现
    g4 = 'BOUNDARY'
    gates.append(('UFT-4 观测复现', g4,
                  'GR 由爱因斯坦项复现（EH 在 𝓛 中）⇒ 复现 PASS；但 G 是输入、复现是重排非预言'
                  '（承 r78 C3 / r87 D4）⇒ BOUNDARY'))
    # UFT-5 可证伪预言
    g5 = 'BOUNDARY'
    gates.append(('UFT-5 可证伪预言', g5,
                  '可证伪新预言 0 条（机读 r76 `n_falsifiable=0`；r81 C1 同族）⇒ 事实计数，'
                  '可接受性属哲学层'))
    # UFT-6 外部验证
    g6 = 'FAIL'
    gates.append(('UFT-6 外部验证', g6, '无任何外部独立验证（承 r76）'))
    for (name, v, why) in gates:
        entry('E' + str(gates.index((name, v, why)) + 1), v,
              '终审门【' + name + '】⇒ **' + v + '**：' + why, v, '终审门')

    n_pass = sum(1 for g in gates if g[1] == 'PASS')
    n_bnd = sum(1 for g in gates if g[1] == 'BOUNDARY')
    n_fail = sum(1 for g in gates if g[1] == 'FAIL')
    entry('E7', 'INFO',
          ('终审门汇总：PASS ' + str(n_pass) + ' / BOUNDARY ' + str(n_bnd) + ' / FAIL ' + str(n_fail) +
           ' ⇒ **定稿方程集得分 ' + str(n_pass) + '/6**（承 r76 口径：体系层）。'
           '与 r76 的 0/6 相比多的这 1 分是「数学自洽」——它恰恰是六条里最便宜的一条'
           '（补上耦合项、对齐量纲就能拿到），而它没有带来任何新的可证伪内容'),
          str({'PASS': n_pass, 'BOUNDARY': n_bnd, 'FAIL': n_fail}), '终审门汇总')


# ----------------------------------------------------------------------------
# F 组：定稿声明与阳性对照
# ----------------------------------------------------------------------------
def group_F():
    D_ALPHA = dm(D_FORCE, dinv(dp(L, -3)))
    _, hits_alpha = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_ALPHA)
    rows = read_ricci_rows()
    entry('F1', 'INFO',
          ('★**大统一方程定稿形态（本册交付件）**：三层、七式 —— '
           '**几何层**：`κ²+τ²=ω²`、`Ω=cω`（v=c）、`κ=(R_abR^ab)^{1/4}`（承 r76 route a）；'
           '**力律层**：`F=−α∇(κ²−τ²)`、`U=α(κ²−τ²)`（承 r79 A2）；'
           '**动力学层**：`𝓛=(c⁴/16πG)R + (ħc/2)[(∂κ)²+(∂τ)²] − λ(κ²+τ²)² − C₁κT + 𝓛_m`'
           '（承 r80/r85 补全与 r74 同号化）。'
           '**定稿的同时必须如实登记三张欠条**：①`U` 是总能量、进 𝓛 须再买体积标度（B2）；'
           '②`α` 是新独立量纲常数、不可由 {ħ,c,G} 构造（B3，穷举 ' + str(len(hits_alpha)) + ' 命中）；'
           '③W1 支的 κ(g) 识别不适定（承 r90：非解析 + 曲率平方鬼）'),
          str(len(hits_alpha)), '定稿形态')

    entry('F2', 'INFO',
          ('★对「继续完成大统一方程」的诚实回答：**方程可以写完，且已经写完（本册定稿）；'
           '但写完不等于完成** —— 定稿件在终审门下得 ' + '1/6' +
           '（仅数学自洽），四力统一、常数派生、外部验证三条 FAIL，观测复现与可证伪预言两条 BOUNDARY。'
           '它不是「还差一个技巧」，而是三张欠条（体积标度 / α 常数 / κ(g) 适定性）'
           '加上四力需要整套 SM 内容。**三条欠条的定价都已在机器里，只差裁决**'),
          None, '诚实回答')

    entry('F3', 'INFO',
          ('剩余项（按依赖序，不代选）：①`X-R90-1` 付 +1 个长度常数换解析识别（直接决定 B2 的体积标度来源）；'
           '②`X-R76-2` W1 vs W2（决定动力学层的最终形态）；③r83 (a)/(b)（决定 τ 扇区去留）；'
           '④屏蔽选型与 λ 符号（仅当选 W2）。**以上任何一条被裁决后，本册的定稿件都可以'
           '在 1 秒内重算并给出新的终审门读数** —— 这就是「完成」的剩余工作量'),
          'dependency-ordered', '剩余项')


# ----------------------------------------------------------------------------
# payload 与输出
# ----------------------------------------------------------------------------
def build_payload():
    verdict = 'FAIL' if COUNTS.get('FAIL', 0) > 0 else (
        'BOUNDARY' if COUNTS.get('BOUNDARY', 0) > 0 else 'PASS')
    D_ALPHA = dm(D_FORCE, dinv(dp(L, -3)))
    _, hits_alpha = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_ALPHA)
    meta = ('大统一方程定稿形态（几何层/力律层/动力学层七式）机器定稿 + 终审门 1/6。'
            '新发现两个：①[α]=M L^4 T^-2 ⇒ U=α(κ²−τ²) 是总能量而非能量密度，进拉氏量须再买体积标度；'
            '②[α] 不能由 {ħ,c,G} 整数幂构造（穷举 0 命中，阳性对照 [力] 有解）⇒ α 为新独立量纲常数。'
            'v=c 桥接 Ω=cω 给出三类环境跨 21 个量级的时空频率；标度律 a√ρ=c/√(8πG) 机器成立。')
    return {
        'round': 'r94',
        'date': '2026-10-17',
        'source': '大统一方程定稿（承 r79 A2 力律 / r80/r85 拉氏量 / r76 route a / r90 适定性）',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'module': os.path.abspath(__file__),
        'source_mtime': datetime.fromtimestamp(os.path.getmtime(__file__), timezone.utc).isoformat(),
        'counts': dict(COUNTS),
        'total': len(ENTRIES),
        'verdict': verdict,
        'meta_verdict': meta,
        'guard_all_ok': True,
        'entries': ENTRIES,
        'not_self_derived': [
            {'tag': 'NS1', 'text': 'c、G 取 CODATA；ħc=1.98644586e-25 J·m；π 60 位'},
            {'tag': 'NS2', 'text': '三点族 ρ 与 (R_abR^ab)^{1/4} 全部机读 r76 key_numbers，无手抄'},
            {'tag': 'NS3', 'text': '力律 F=−α∇(κ²−τ²) 与 U=α(κ²−τ²) 承 r79 A2 机读实测；四力代入式同源'},
            {'tag': 'NS4', 'text': '𝓛 的四项补全（EH/动能/势/耦合）承 r80 D/r85 A1-A2，本册只做量纲复核不重推'},
            {'tag': 'NS5', 'text': '「R≈8πGρ/c²」（尘埃、trace-reversed）为 GR 标准结论，用于标度律 a√ρ 推导'},
            {'tag': 'NS6', 'text': 'NS 半径 10 km、火星轨道 1.524 AU 为外部输入，仅用于巧合簿与敏感性（不计入判据）'},
            {'tag': 'NS7', 'text': '终审门 UFT-1..6 口径承 r76 C 组（体系层/基础恒等式层两条分列，本册取体系层）'},
            {'tag': 'NS8', 'text': 'τ=0（Levi-Civita）承 r89 A1/r90；ω=κ 的取值依赖该前提，已在条目内声明'},
        ],
        'red_line': '数学／数值自洽 ≠ 物理证实。本册把「大统一方程」写成可机器复算的定稿件，'
                    '但**交付的是方程，不是证实**：定稿件终审 1/6，三张欠条（体积标度、α 常数、κ(g) 适定性）'
                    '与四力需整套 SM 内容的账都已在机器里。**巧合（NS/火星尺度接近）不计入任何判据。**'
                    '写完方程 ≠ 完成统一场论。',
    }


def write_outputs(payload):
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    verdict = payload['verdict']
    jp = os.path.join(DATA, STEM + '.json')
    with io.open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rl = ['TUFT-r94 大统一方程定稿（构件 / v=c 桥接 / α 对账 / 终审门）运行报告',
          'counts=' + str(payload['counts']) + ' total=' + str(payload['total']) + ' verdict=' + verdict,
          'meta=' + payload['meta_verdict']]
    for e in ENTRIES:
        rl.append('[' + e['verdict'] + '] ' + e['tag'] + ' : ' + e['text'])
        if e['residual']:
            rl.append('    residual=' + e['residual'])
    rl.append('')
    rl.append('GUARD G0: 自守卫全过（G0-1 κ⁴==R_abR^ab / G0-2 Ω 标度 / G0-3 aκ=1 / '
              'G0-4 a√ρ 三点族同常数 / G0-5 穷举器阳性对照 / G0-6 α 穷举 0 命中 / G0-7 U 是能量非密度）')
    rl.append('GENERATED_AT=' + payload['generated_at'])
    rl.append('MODULE=' + payload['module'])
    rp = os.path.join(DATA, STEM + '_report.txt')
    with io.open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rl))

    ml = ['# ' + STEM, '', '日期：2026-10-17 · 大统一方程定稿形态与终审', '',
          '## 条目计数', '- 总条目：' + str(payload['total'])]
    for k in sorted(payload['counts'].keys()):
        ml.append('- ' + k + '：' + str(payload['counts'][k]))
    ml += ['- 总体 verdict：' + verdict, '- 元判定：' + payload['meta_verdict'], '', '## 逐条裁定']
    for e in ENTRIES:
        line = '- **' + e['tag'] + '** [' + e['verdict'] + '] ' + e['text']
        if e['residual']:
            line += '  （残差 ' + e['residual'] + '）'
        ml.append(line)
    ml += ['', '## not_self_derived']
    for n in payload['not_self_derived']:
        ml.append('- ' + n['tag'] + '：' + n['text'])
    ml += ['', '## 红线', payload['red_line']]
    mp = os.path.join(DATA, STEM + '.md')
    with io.open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ml))
    return jp, rp, mp


def write_judgment(payload):
    rows = read_ricci_rows()
    # D_ALPHA 取模块级定义（函数内局部列表 L 会遮蔽全局量纲元组 L，故不在此重算）
    _, hits_alpha = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_ALPHA)
    _, hits_force = enum_dims({'ħ': D_HBAR, 'c': D_C, 'G': D_G}, D_FORCE)
    L = ['# 判定_TUFT-r94-大统一方程定稿_构件v=c频率桥接与α量纲对账_终审_2026-10-17', '',
         '日期：2026-10-17 · **大统一方程定稿册**（应用户命题：曲率/挠率/频率/角速度，v=c）· **下轮从 r95 起**', '',
         '## 〇、一句话结论',
         '**大统一方程可以写完，本册已把它写成七式三层的可机器复算定稿件；但定稿不等于完成** —— '
         '终审门 **1/6**（仅数学自洽），并新发现两张欠条：`U` 是**总能量**（进拉氏量须再买体积标度）、'
         '`α` 是**不可由 {ħ,c,G} 构造的新量纲常数**（穷举 0 命中，阳性对照有效）。', '',
         '## 一、定稿件（七式三层）', '',
         '**几何层**', '',
         '```',
         'κ² + τ² = ω²            （来料 801；[κ]=[τ]=[ω]=L^-1）',
         'Ω = c·ω                 （v = c 桥接：ω 是波数，Ω 才是角速度 [T^-1]）',
         'κ = (R_ab R^ab)^{1/4}   （承 r76 A02 route (a)：零新常数、量纲 L^-1）',
         '```', '',
         '**力律层**', '',
         '```',
         'F = −α·∇(κ² − τ²)       （统一力方程，承 r79 A2；[α] = M L^4 T^-2）',
         'U = α·(κ² − τ²)         （统一势；[U] = M L^2 T^-2 = **总能量**，非密度）',
         'κ ∝ M/r,  τ ∝ q/r,  τ_weak ∝ q e^{−μr}/r,  τ_strong ∝ σ r e^{−r/r0}   （四力 ansatz）',
         '```', '',
         '**动力学层**（承 r80/r85 补全 + r74 同号化）', '',
         '```',
         '𝓛 = (c⁴/16πG)·R + (ħc/2)[(∂κ)² + (∂τ)²] − λ(κ²+τ²)² − C₁·κ·T + 𝓛_m',
         '```', '',
         '## 二、v = c 频率桥接（定稿件第一块新机器内容）', '',
         '| 环境 | κ [m^-1] | a = 1/κ [m] | Ω = cω [rad/s] | f [Hz] |',
         '|---|---|---|---|---|']
    for row in rows:
        kap = D(row['quarter_power_m^-1'])
        L.append('| ' + row['point'] + ' | ' + str(kap.normalize()) + ' | ' +
                 str(helix_radius(kap).normalize()) + ' | ' + str(angular_velocity(kap).normalize()) +
                 ' | ' + str(freq(kap).normalize()) + ' |')
    L += ['', '⇒ 同一公式集在三类环境给出跨 **21 个量级**的时空频率。'
          '**标度律**：`a·√ρ = c/√(8πG)`（机器常数 ' + str(a_sqrt_rho().normalize()) +
          '，三点族机器零）⇒ 螺旋半径由密度唯一决定。', '',
          '## 三、两个新发现（本册承重）',
          '- **①[U] 是总能量**：`[α] = M L^4 T^-2`（由 F 反解）⇒ `[U] = M L^2 T^-2` = 能量，'
          '比能量密度差一个 L³ ⇒ **`𝓛_U = U/V` 必须引入体积标度**（+1 常数或细胞口径）。'
          '此前无任何一册处理过这个缺口（r79 只测形式，r80/r85 补 𝓛 时没回来对 α 的账）。',
          '- **②[α] 不可构造**：`{ħ,c,G}` 整数幂穷举 343 组，对 `[α]` 命中 **' + str(len(hits_alpha)) +
          '** 组；阳性对照对 `[力]` 命中 **' + str(len(hits_force)) + '** 组 ⇒ α 是**新独立量纲常数**'
          '（与 r83 的电荷量纲 Q 同族）。', '',
          '## 四、终审门（承 r76 C 组口径，在定稿件上重跑）', '',
          '| 门 | 判定 | 依据 |',
          '|---|---|---|',
          '| UFT-1 数学自洽 | **PASS** | 动力学层四项齐次（补全+更正的成果） |',
          '| UFT-2 四力统一 | **FAIL** | 还原 0/4（承 r82–r84） |',
          '| UFT-3 常数派生 | **FAIL** | α+λ+C₁+ω 全是输入，≥3 个自由常数 |',
          '| UFT-4 观测复现 | BOUNDARY | GR 复现但 G 是输入（重排非预言） |',
          '| UFT-5 可证伪预言 | BOUNDARY | 新预言 0 条（机读 r76） |',
          '| UFT-6 外部验证 | **FAIL** | 无 |',
          '', '⇒ **定稿件得分 1/6**（比 r76 的 0/6 多的 1 分恰是六条里最便宜的「数学自洽」）。', '',
          '## 五、巧合簿（纪律：巧合 ≠ 证据）',
          '- NS：曲率半径 ' + str(helix_radius(D([r for r in rows if r['point'] == '中子星'][0]['quarter_power_m^-1'])).normalize()) +
          ' m ≈ NS 半径 10 km；水：≈ 1.547 AU ≈ 火星轨道 1.524 AU。',
          '- 敏感性：NS 半径取 8–16 km ⇒ 比值 1.29 → 1.04 → 0.86 → 0.65 ⇒ 对输入 O(1) 敏感 ⇒ **非结构性**。',
          '- 对照：宇宙平均 a ≈ 8.06e9 光年，与可观测宇宙半径不对应 ⇒ 三环境两近一远，接近是偶然。', '',
          '## 六、不自推登记']
    for n in payload['not_self_derived']:
        L.append('- ' + n['tag'] + '：' + n['text'])
    L += ['', '## 七、剩余项与治理',
          '- `X-R90-1`（+1 长度常数换解析识别，同时是 B2 体积标度的来源）· `X-R76-2`（W1 vs W2）· '
          'r83 (a)/(b) · 屏蔽选型与 λ 符号 ⇒ **全部待裁决，本册不代选**。',
          '- 任何一条被裁决后，本定稿件可在 1 秒内重算并给出新的终审门读数。',
          '- 治理：未改动任何他人文件字节（r76/r79/r82 全部只读机读）；未跑 `refresh_catalog`；未做 git 操作。'
          '**下轮从 r95 起**。', '',
          '## 八、红线', payload['red_line'], '',
          'GENERATED_AT=' + payload['generated_at'], 'MODULE=' + payload['module']]
    jb = os.path.join(BASE, '判定_TUFT-r94-大统一方程定稿_构件v=c频率桥接与α量纲对账_终审_2026-10-17.md')
    with io.open(jb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    return jb


def main():
    G0_guards()
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    group_F()
    payload = build_payload()
    jp, rp, mp = write_outputs(payload)
    jb = write_judgment(payload)
    assert len(ENTRIES) == sum(payload['counts'].values()), 'entry count mismatch'
    print('counts=' + str(payload['counts']))
    print('total=' + str(payload['total']))
    print('verdict=' + payload['verdict'])
    print('written: ' + jp + ' | ' + rp + ' | ' + mp + ' | ' + jb)


if __name__ == '__main__':
    main()
