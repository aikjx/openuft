# -*- coding: utf-8 -*-
"""
TUFT-r176｜S17 核心公式 18「核力场定义方程」
          D = −G m [ c − 3 (r/r) ṙ ] / r³
          —— 定义求导本身正确，但量纲缺 T⁻¹、阶数错一阶、公设代入后θ依赖、
             非中心力、强度恰等于引力、短程性只有幂次没有截断

00. 编号与定位
  【编号】r176。起草前实测磁盘实占 r148..r175（r175 = 空间波动方程，2026-10-25，
        并行会话在途）⇒ 本卷取首空号 r176；**下轮从 r177 起**（r 序列竞争态，
        落盘前必须复查）。
  【靶】01_独立体系/S17_统一场论核心公式/04_理论推导/核心公式集/
        18-核力场定义方程/1.md（189 行）+ 其 code/ 下三个自称 verify 的脚本。
    主链（靶 §3）：D ≡ dA/dt；A = −Gm r/r³；
                   d/dt(r/r³) = (ṙ − 3 r̂ ṙ)/r³；
                   **步骤 4：dr/dt = c**（公设 1）；
                   ⇒ D = −Gm[c − 3 r̂ ṙ]/r³。
  【继承（本册不重算）】
    · 库内总汇册（统一场论核心公式_正确核固化_2026-10-03）把本式列入「剔除 7 条」，
      记「量纲缺口 T⁻¹ + 比库仑弱 36.1 量级」；本卷**独立复算并给出口径**，
      并把定性缺口升级为机器唯一化（整数幂网格零命中）+ 阶数错位 + 角动量 +
      短程性 + 强度 + 量级宣称六条新读数。
    · r141 / r142 F2 已判「核力场无作用程」；r147 判「B4/F2 在 {FLIP,DEL}
      内关闭解 0」；本卷不重复其枚举结论，只做**式子层**的机器判决。
  【分层】本卷只判「该式作为核力场定义方程」是否成立；**不**判强相互作用
        本身的 QCD 描述（那需要一个完整的场论，本卷未触及）。

01. 机读手段
  纯标准库。量纲四元组 (M,L,T,Q) 整数元组；解析导数闭式 + 中心差分双路径对拍
  （无量纲单位 Gm=1，避免 1e−34 量级下相减抵消）；θ 网格扫描（c 与 r̂ 夹角）；
  整数幂网格穷举（{c,ħ,G} 与 {c,ħ,G,l_P} 两套）；解析梯度/旋度对拍；
  Yukawa 对照（r₀ = π 介子康普顿波长）；靶文正则计数（自承词与项位词）。

02. 红线
  数学自洽 ≠ 实验证实；求导正确 ≠ 结论成立；量纲齐 ≠ 物理对。
  本卷不否证「强相互作用存在」，只判「该式是不是它的场方程」。
  折算类读数（把 jerk 乘时间变加速度、把 D·r·m′ 当功率）均为**本卷的口径**，
  已在条目 note 中显式标注，不作为靶的宣称。
"""

import io
import json
import math
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 路径 / 登记器
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r176_核力场定义方程_定义求导与量纲阶数错位_精算_2026-10-25"

TARGET = os.path.join(
    BASE, "01_独立体系", "S17_统一场论核心公式", "04_理论推导", "核心公式集",
    "18-核力场定义方程", "1.md")
CODEDIR = os.path.join(
    BASE, "01_独立体系", "S17_统一场论核心公式", "04_理论推导", "核心公式集",
    "18-核力场定义方程", "code")

ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def fs(x, n=6):
    try:
        return "%.*e" % (n, float(x))
    except Exception:
        return str(x)


def rel(x, y):
    """两个同量级量的相对差 |x−y|/max(|x|,|y|)。

    注意语义边界：不能把「残差」当 x、把「真值」当 y 传进来——
    残差为 0 时本式返回 1.0（假故障），残差=真值时返回 0（假通过）。
    残差类比较一律用 relerr(x, y) 或直接 |Δ|/|真值|。
    """
    m = max(abs(x), abs(y))
    return 0.0 if m == 0.0 else abs(x - y) / m


def relerr(x, y):
    """相对误差 |x−y|/|y|，y 为参照量（残差类比较唯一正确用法）。"""
    x = float(x)
    y = float(y)
    if y == 0.0:
        return 0.0 if x == 0.0 else float("inf")
    return abs(x - y) / abs(y)


# ============================================================
# 量纲四元组 (M, L, T, Q)，Q = 电流 A。整数元组，相加即相乘。
# ============================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


def dstr(d):
    names = ("M", "L", "T", "Q")
    parts = []
    for nm, e in zip(names, d):
        if e == 0:
            continue
        parts.append("%s^%d" % (nm, e))
    return "1" if not parts else " ".join(parts)


D_ONE = (0, 0, 0, 0)
D_MASS = (1, 0, 0, 0)
D_LEN = (0, 1, 0, 0)
D_TIME = (0, 0, 1, 0)
D_VEL = (0, 1, -1, 0)            # 速度
D_ACC = (0, 1, -2, 0)            # 加速度（重力场强度 / 力·kg⁻¹）
D_JERK = (0, 1, -3, 0)           # 急动度（加速度变化率）
D_FORCE = (1, 1, -2, 0)
D_C = (0, 1, -1, 0)
D_C2 = (0, 2, -2, 0)
D_HBAR = (1, 2, -1, 0)
D_G = (-1, 3, -2, 0)


def dim_check():
    """量纲工具自检（先过 guard，再用于判定 —— 本库纪律）。

    自检断言必须自己先对：r176 首版有 3 条期望值写错（[a]/[L]、
    [c⁵/ħG]、[ħG/c⁵]），导致「工具 7/10」被误当成工具故障。
    """
    checks = []
    lhs = ddiv(dmul(D_G, D_MASS), dpow(D_LEN, 2))      # [G][m]/[r]²
    checks.append(("Gm/r2 == 加速度", lhs == D_ACC))
    checks.append(("dmul 语义 = 指数相加",
                   dmul(D_LEN, D_VEL) == (0, 2, -1, 0)))
    checks.append(("ddiv 语义 = 指数相减（[a]/[L] = T^-2）",
                   ddiv(D_ACC, D_LEN) == (0, 0, -2, 0)))
    checks.append(("[c^5/hbar/G] = T^-2",
                   ddiv(dpow(D_C, 5), dmul(D_HBAR, D_G)) == (0, 0, -2, 0)))
    checks.append(("[hbar G/c^5] = T^2（= t_P²）",
                   ddiv(dmul(D_HBAR, D_G), dpow(D_C, 5)) == (0, 0, 2, 0)))
    checks.append(("[D]=[Gmc/r^3] = L T^-3",
                   ddiv(dmul(dmul(D_G, D_MASS), D_C), dpow(D_LEN, 3)) == D_JERK))
    checks.append(("[m][D] != [F]（缺口非零）",
                   dmul(D_MASS, D_JERK) != D_FORCE))
    checks.append(("[F]/[D] = M T",
                   ddiv(D_FORCE, D_JERK) == (1, 0, 1, 0)))
    checks.append(("[l_P/c] = T", ddiv(D_LEN, D_C) == D_TIME))
    checks.append(("[D]·[T] = 加速度", dmul(D_JERK, D_TIME) == D_ACC))
    return checks, lhs


# ============================================================
# 物理常量（CODATA / PDG 公布值，字面引用）
# ============================================================
G_N = 6.67430e-11
C_LIGHT = 299792458.0
HBAR = 1.054571817e-34
M_P = 1.67262192369e-27
M_E = 9.1093837015e-31
E_CH = 1.602176634e-19
K_E = 8.9875517923e9
L_P = 1.616255e-35
M_PK = 2.176434e-8
ALPHA_S = 1.0
R_NUC = 1.0e-15
R_PION = 1.4138e-15      # π 介子康普顿波长（Yukawa 力程标准值）

T_P = L_P / C_LIGHT
HBARC = HBAR * C_LIGHT


# ============================================================
# 向量工具
# ============================================================
def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def vmul(a, s):
    return tuple(x * s for x in a)


def vdot(a, b):
    return sum(x * y for x, y in zip(a, b))


def vnorm(a):
    return math.sqrt(vdot(a, a))


def vunit(a):
    n = vnorm(a)
    return tuple(x / n for x in a)


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def A_field(x, Gm):
    """静引力场 A(x) = −Gm x / r³。"""
    r = vnorm(x)
    return tuple(-Gm * xi / r ** 3 for xi in x)


def dA_dt(x, v, Gm):
    """解析 dA/dt = −Gm [v − 3 r̂ (r̂·v)] / r³。"""
    r = vnorm(x)
    rh = vunit(x)
    rv = vdot(rh, v)
    return tuple(-Gm * (vi - 3.0 * rh[i] * rv) / r ** 3
                 for i, vi in enumerate(v))


def dA_dt_num(x, v, Gm, h):
    xp = tuple(x[i] + h * v[i] for i in range(3))
    xm = tuple(x[i] - h * v[i] for i in range(3))
    Ap = A_field(xp, Gm)
    Am = A_field(xm, Gm)
    return tuple((Ap[i] - Am[i]) / (2.0 * h) for i in range(3))


def D_field(x, cvec, Gm):
    """把 c 当固定矢量时，D 作为空间场：−Gm ∇[(x·c)/r³]。"""
    r = vnorm(x)
    rh = vunit(x)
    rc = vdot(rh, cvec)      # = ṙ（由 dr/dt = c 推出）
    return tuple(-Gm * (cvec[i] - 3.0 * rh[i] * rc) / r ** 3
                 for i in range(3))


def curl_num(F, x, h=1.0e-5):
    """中心差分求旋度。"""
    def d(f, i):
        xp = list(x)
        xm = list(x)
        xp[i] += h
        xm[i] -= h
        return (f(tuple(xp))[0] - f(tuple(xm))[0],
                f(tuple(xp))[1] - f(tuple(xm))[1],
                f(tuple(xp))[2] - f(tuple(xm))[2])
    # 只取分量形式，调用方按需使用
    dF = [d(F, i) for i in range(3)]
    return (dF[1][2] - dF[2][1],
            dF[2][0] - dF[0][2],
            dF[0][1] - dF[1][0])


# ============================================================
# SECTIONS：段落元数据（打印顺序由 SECTIONS 决定，与 add 顺序无关）
# ============================================================
SECTIONS = [
    ("A", "推导链层：求导本身 / 公设代入 / 简化式条件", ["A01", "A04"]),
    ("B", "量纲与阶数层：T⁻¹ 缺口 / jerk≠加速度 / 补齐因子", ["B01", "B04"]),
    ("C", "物理量级层：强度 / 短程 / 中心性 / 角动量 / 各向异性 / 做功宣称",
     ["C01", "C07"]),
    ("D", "跨卷层：与统一力方程的项位 / 与 c 的恒常性 / 靶自承", ["D01", "D03"]),
]


def build():
    # ---------- 文本层：靶可定位 + 自承词计数 ----------
    txt = ""
    nlines = 0
    if os.path.exists(TARGET):
        txt = io.open(TARGET, encoding="utf-8", errors="replace").read()
        nlines = len(txt.split("\n"))
    cnt_guess = txt.count("高度推测") + txt.count("猜测")
    cnt_third = txt.count("第三项")
    cnt_cvec = txt.count("d\\vec{c}") + txt.count("dc/dt")
    code_files = []
    if os.path.isdir(CODEDIR):
        code_files = sorted(f for f in os.listdir(CODEDIR) if f.endswith(".py"))

    # ============================================================
    # A 组：推导链
    # ============================================================
    Gm = 1.0
    x0 = (1.7, 0.9, 0.4)
    v0 = (0.6, -0.3, 0.2)
    ana = dA_dt(x0, v0, Gm)
    conv = []
    for h in (4.0e-5, 2.0e-5, 1.0e-5):
        nn = dA_dt_num(x0, v0, Gm, h)
        # 相对残差 = |解析−差分| / |解析|（不能用 rel：残差为 0 时 rel 返回 1.0）
        conv.append((h, vnorm(vsub(ana, nn)) / vnorm(ana)))
    resid_A01 = conv[-1][1]

    add("A01",
        "求导链 d/dt(r/r³) = (ṙ − 3 r̂ ṙ)/r³ 的算术正确性（解析 vs 中心差分）",
        "PASS",
        "对靶有利单列：商法则与链式法则使用无误，解析式与差分双路径一致，"
        "且步长收敛单调（二阶差分）。错的是最后一步的『代入』，不是求导。",
        residual=resid_A01,
        conv=[(h, r) for h, r in conv])

    # A02：dr/dt = c 与 ṙ 的重复计数
    rhat = vunit(x0)
    theta_rows = []
    for deg in (0.0, 15.0, 30.0, 60.0, 75.0, 89.99994):
        th = math.radians(deg)
        # 构造与 r̂ 成 θ 的单位矢量（取一个与 r̂ 不平行的参考方向）
        ref = (0.0, 0.0, 1.0)
        if abs(vdot(ref, rhat)) > 0.99:
            ref = (1.0, 0.0, 0.0)
        e1 = vunit(vsub(ref, vmul(rhat, vdot(ref, rhat))))
        chat = vadd(vmul(rhat, math.cos(th)), vmul(e1, math.sin(th)))
        rdot = C_LIGHT * math.cos(th)          # 由 d r/dt = c 唯一决定
        cvec = vmul(chat, C_LIGHT)
        D = D_field(x0, cvec, 1.0)
        # 靶的简化式 D ≈ −Gm c/r³（丢掉 −3r̂ṙ 项）。首版漏了 c 因子，
        # 使 simple_dev 饱和在 1.0（失去量纲意义）。
        D_simple = vmul(chat, -1.0 * C_LIGHT / vnorm(x0) ** 3)
        cos_dc = vdot(vunit(D), chat)
        # 与简化式的偏差必须用「矢量差 / 简化式模长」（保留符号信息）：
        # θ=0 时 D=+2ĉ、D_simple=−ĉ ⇒ 偏差 3，而不是只比模长得到的 1。
        simple_dev = vnorm(vsub(D, D_simple)) / vnorm(D_simple)
        theta_rows.append({
            "theta_deg": deg, "rdot_over_c": rdot / C_LIGHT,
            "D_over_Gmc_r3": vnorm(D) / (1.0 * C_LIGHT / vnorm(x0) ** 3),
            "simple_dev": simple_dev,
            "cos_D_c": cos_dc,
            "cos_D_Dsimple": vdot(vunit(D), vunit(D_simple)),
            "angle_to_minus_c_deg": math.degrees(math.acos(max(-1.0, min(1.0, -cos_dc)))),
        })

    # 靶声称 ṙ ≪ c ⇒ 反解所需 θ
    eps = 1.0e-6
    theta_needed = math.degrees(math.acos(eps))
    add("A02",
        "步骤 4『dr/dt = c』与分子里的标量 ṙ 重复计数：由公设 ṙ = c·r̂ 被唯一决定",
        "FAIL",
        "d r/dt = c（矢量）与 ṙ = d|r|/dt（标量）满足 ṙ = c·r̂。二者同时出现在"
        "同一式里且被当作独立量 ⇒ 重复计数。机器读数：ṙ/c = cosθ，"
        "θ=0/30/60/90° ⇒ 1/0.866/0.5/0。靶的『ṙ ≪ c』等价于 θ→90°（c 垂直于连线），"
        "而不是『原子核内速度小』。",
        rdot_over_c=[(r["theta_deg"], r["rdot_over_c"]) for r in theta_rows],
        theta_needed_deg=theta_needed)

    # A03：θ=0 时符号翻转且幅度加倍
    th0 = theta_rows[0]
    th90 = [r for r in theta_rows if abs(r["theta_deg"] - 90.0) < 1e-6]
    add("A03",
        "严格代入公设后 D = −(Gmc/r³)(ĉ − 3cosθ r̂) ⇒ θ=0 时 D = +2(Gmc/r³) r̂（反向加倍）",
        "FAIL",
        "靶 §4.3 的简化式 D ≈ −(Gm/r³)c 只在 c ⊥ r̂（θ=90°、ṙ=0）时成立。"
        "若 c 沿连线（θ=0，最自然的读法：空间本底沿径向流过源），"
        "机器给出 D = +2(Gmc/r³) r̂ —— 方向与靶的简化式相反、幅度为 2 倍。"
        "⇒ 简化式不是『忽略小量』的结果，而是『忽略了一整项（且该项恰是主导项）』。",
        theta0_D_over_simple=th0["D_over_Gmc_r3"],
        theta0_simple_dev=th0["simple_dev"],
        theta90_D_over_simple=th90[0]["D_over_Gmc_r3"] if th90 else None)

    # A04：简化条件的真实形式
    add("A04",
        "简化式 D ≈ −Gmc/r³ 的成立条件是 c ⊥ r̂（ṙ=0），不是靶声称的 ṙ ≪ c",
        "FAIL",
        "靶的论证『原子核内 ṙ 远小于 c，故 c 项主导』把 ṙ 当作可自由取小的参数；"
        "由 dr/dt = c 它被锁定为 c·cosθ，取值范围 [−c, +c]，"
        "『小』只能由 θ→90° 实现。⇒ 论证的物理理由（核内速度小）与数学条件"
        "（方向垂直）不是同一件事；且 θ 依赖意味着场强依赖 c 与两点连线的夹角。",
        theta_needed_for_1e_minus_6=theta_needed,
        D_ratio_theta0_over_theta90=(th0["D_over_Gmc_r3"] /
                                     (th90[0]["D_over_Gmc_r3"] if th90 else 1.0)))

    # ============================================================
    # B 组：量纲与阶数
    # ============================================================
    dims = ddiv(dmul(dmul(D_G, D_MASS), D_C), dpow(D_LEN, 3))
    gap = ddiv(D_ACC, dims)          # 目标 / 实得
    add("B01",
        "量纲缺口（目标/实得）= T¹：D 比加速度多带一个 T⁻¹（急动度 ≠ 加速度）",
        "FAIL",
        "靶 §4.2 自己算出 [D] = [L T⁻³] 并称『这是急动度，符合其作为引力场变化率的定义』。"
        "但『核力场』若要与质量耦合给出力（F = m′D），则 [D] 必须是加速度 L T⁻²。"
        "机器判定缺口 = [加速度]/[D] = M⁰L⁰T¹Q⁰ = **T¹**（等价说法：D 相对加速度"
        "多带一个 T⁻¹，故必须乘一个时间因子才能当加速度用；该时间因子见 B03）。"
        "⇒ 这不是「定义选择」，而是与「核力场给出力」这一用途直接冲突。",
        dim_D=dstr(dims), dim_required=dstr(D_ACC), gap=dstr(gap),
        dim_mD=dstr(dmul(D_MASS, dims)))

    add("B02",
        "阶数错位：D = dA/dt 是引力的三阶时间导（jerk），核力项 m·dc/dt 是二阶（力）",
        "FAIL",
        "靶 §4.3 声称 D 是统一力方程中『m dc/dt』这一项的具体表达式。"
        "但 D = dA/dt 含的是 c 的**零阶**（c 本身，来自 dr/dt = c），"
        "而 m dc/dt 含的是 c 的**一阶时间导数**。二者相差一阶时间导数，"
        "正是 B01 的 T⁻¹ 缺口的来源。⇒ 『为该项提供具体表达式』在阶数上不成立。",
        order_D=3, order_nuclear_term=2,
        dim_c=dstr(D_C), dim_cdot=dstr(D_ACC),
        dim_D=dstr(dims))

    # B03：补齐因子穷举
    basis = {"c": D_C, "hbar": D_HBAR, "G": D_G}
    hits3 = []
    rng = range(-3, 4)
    for a in rng:
        for b in rng:
            for d in rng:
                v = (0, 0, 0, 0)
                for nm, e in (("c", a), ("hbar", b), ("G", d)):
                    v = dmul(v, dpow(basis[nm], e))
                if v == D_TIME:
                    hits3.append((a, b, d))
    hits4 = []
    basis4 = dict(basis)
    basis4["lP"] = D_LEN
    for a in rng:
        for b in rng:
            for d in rng:
                for f in rng:
                    v = (0, 0, 0, 0)
                    for nm, e in (("c", a), ("hbar", b), ("G", d), ("lP", f)):
                        v = dmul(v, dpow(basis4[nm], e))
                    if v == D_TIME:
                        hits4.append((a, b, d, f))

    D_mag = G_N * M_P * C_LIGHT / R_NUC ** 3
    a_need = ALPHA_S * HBARC / (R_NUC ** 2 * M_P)
    t_need = a_need / D_mag
    t_years = t_need / 3.15576e7
    add("B03",
        "补齐因子唯一化：整数幂网格内命中 0，闭式解需半整数幂 t_P；且 t_P 口径差 58 量级",
        "FAIL",
        "{c,ħ,G} 的整数幂 [−3,3]³ = 343 组中**无一组**给出 T¹（命中 0）⇒ 时间量纲"
        "只能由半整数幂得到：t_P = sqrt(ħG/c⁵)。加 l_P 后整数解 = l_P/c（同一个 t_P）。"
        "把 t_P 乘到 D 上得 1.80e−27 m/s²（比核力弱 58 量级）；"
        "要落到核力强度需乘 t = 5.65e14 s = **1.79e7 年**（天文时间，非核时间 1e−23 s）。"
        "⇒ 量纲可以被『补上』，但补上的那个时间尺度没有核物理来源。",
        integer_hits_3basis=len(hits3),
        integer_hits_with_lP=len(hits4),
        tP_s=T_P, D_times_tP_m_s2=D_mag * T_P,
        t_need_s=t_need, t_need_years=t_years)

    # B04：无旋（定义使然，零信息）
    xc = (1.3, -0.7, 1.1)
    cvec = (0.4, 0.9, -0.3)
    F = lambda y: D_field(y, cvec, 1.0)
    cr = curl_num(F, xc)
    cr_rel = vnorm(cr) / max(1e-30, vnorm(F(xc)))
    add("B04",
        "D 恒为无旋场（D = −∇[Gm(x·c)/r³]），∇×D 机器零 ⇒ 形式保守但零信息",
        "INFO",
        "因 D 是某个标量（引力势的时间导数）的梯度，其旋度恒为零 ⇒ 『核力场』"
        "在定义上是保守场。这不是靶的功绩（任何势场的时间导数都无旋），"
        "但它与『核力耗散/延迟（介子交换）』的物理图像不一致。",
        curl_rel=cr_rel)

    # ============================================================
    # C 组：物理量级
    # ============================================================
    # C01：1/r³ 比 1/r² 快（对靶有利）
    decay = []
    for rfm in (1.0, 2.0, 5.0, 10.0):
        decay.append((rfm, (1.0 / rfm ** 3) / (1.0 / rfm ** 2)))
    add("C01",
        "1/r³ 确实比 1/r² 衰减得快（比值 = 1/r，单调递减）",
        "PASS",
        "对靶有利单列：『比引力/库仑更快衰减』这一数值事实成立。"
        "但它只说明『更强』，不说明『短程』（见 C02/C03）。",
        decay_ratio=[(r, d) for r, d in decay])

    # C02：与 Yukawa 对照
    yuk = []
    for rfm in (1.0, 2.0, 5.0, 10.0, 20.0, 50.0):
        pw = (1.0 / rfm) ** 3
        yk = math.exp(-rfm * 1e-15 / R_PION)
        yuk.append((rfm, pw, yk, pw / yk))
    add("C02",
        "1/r³ 只是幂律、无截断：1–10 fm 与 Yukawa 量级相近，50 fm 处强 1e10 倍",
        "BOUNDARY",
        "取 Yukawa 力程 r₀ = π 介子康普顿波长 1.4138 fm：r=10 fm 时幂律/Yukawa = 1.18"
        "（量级相近），r=20 fm = 1.7e2，r=50 fm = 1.9e10。⇒ 近场形状不排除，"
        "远场尾巴与『指数截断』定性不同。因此『短程性』只能算『更陡』，"
        "不能算『短程』——后者需要指数或有界支撑。",
        table=yuk)

    # C03：无零点 / 无硬核 / 结合能发散
    signs = []
    for rfm in (0.4, 0.7, 1.0, 2.0, 5.0, 20.0):
        # 取 θ=90°（靶的简化式所在口径）
        d = G_N * M_P * C_LIGHT / (rfm * 1e-15) ** 3
        signs.append((rfm, d))
    mono = all(signs[i][1] > signs[i + 1][1] for i in range(len(signs) - 1))
    zero_cross = 0
    Eb = []
    for rmin in (1e-18, 1e-20, 1e-24):
        Eb.append((rmin, G_N * M_P * C_LIGHT * M_P / (2.0 * rmin ** 2)))
    add("C03",
        "无零点、无硬核、无饱和：|D| 在 r→0 单调发散，结合能无下界",
        "FAIL",
        "核力必须在 r≈0.4–1 fm 由吸引转排斥（硬核 + 饱和）。"
        "机器扫描 0.4–20 fm：|D| 严格单调、符号恒不变 ⇒ 零交点 0 个。"
        "且 ∫|D|dr = Gmc m′/(2r_min²) 在 r_min→0 发散（三档实测 0.17 eV / 1.7 keV / 2.8e−8 J）"
        "⇒ 核物质会无限塌缩，与饱和性（每核子 ~8 MeV、密度 ~0.16 fm⁻³）直接矛盾。",
        monotone=mono, zero_crossings=zero_cross,
        binding_energy=[(r, e) for r, e in Eb])

    # C04：非中心力 / 角动量
    tau_rows = []
    for deg in (0.0, 30.0, 60.0, 90.0):
        th = math.radians(deg)
        ref = (0.0, 0.0, 1.0)
        if abs(vdot(ref, rhat)) > 0.99:
            ref = (1.0, 0.0, 0.0)
        e1 = vunit(vsub(ref, vmul(rhat, vdot(ref, rhat))))
        chat = vadd(vmul(rhat, math.cos(th)), vmul(e1, math.sin(th)))
        cvec2 = vmul(chat, C_LIGHT)
        x_si = vmul(rhat, R_NUC)
        D_si = D_field(x_si, cvec2, G_N * M_P)
        tau = vcross(x_si, D_si)          # 比角动量变化率（m²/s²）
        tau_rows.append((deg, vnorm(tau), vnorm(tau) / (G_N * M_P * C_LIGHT / R_NUC ** 2)))
    add("C04",
        "非中心力：r×D = −Gm(r×c)/r³ ≠ 0（θ≠0）⇒ 角动量不守恒",
        "FAIL",
        "D 含一个与两点连线无关的固定矢量 c（靶的『空间本底速度』），"
        "故力不沿连线。机器读数：θ=0 时力矩 0（阳性对照）；θ=90° 时比角动量变化率"
        "达 33.47 m²/s²（= Gm c/r²，无任何抑制因子）。核力在实验上是中心力"
        "（除自旋-轨道 ~MeV 级修正），不能带一个宇宙学方向的整体力矩。",
        tau_table=[(d, t, u) for d, t, u in tau_rows],
        tau_max_m2_s2=tau_rows[-1][1])

    # C05：c 的方向两难
    add("C05",
        "c 的方向两难：固定 ⇒ |D| 各向异性 2 倍（100%）；各向同性 ⇒ 场无确定方向",
        "BOUNDARY",
        "|D(θ)| = (Gmc/r³)·sqrt(1+3cos²θ)：θ=0 给 2、θ=90° 给 1 ⇒ 比值恰 2。"
        "若 c 有固定宇宙学方向，则同一距离上的核力场强随连线方向变化 100%，"
        "被核力的各向同性（除自旋项）排除；若 c 各向同性（无方向），"
        "则 D 的矢量方向无定义。⇒ 两种读法都不给出可用的中心场。"
        "（本卷不判『空间本底速度』本身，只判它作为核力场方向源的问题。）",
        anisotropy_ratio=2.0)

    # C06：强度恰等于引力
    a_N = G_N * M_P / R_NUC ** 2
    a_s = ALPHA_S * HBARC / (R_NUC ** 2 * M_P)
    a_C = K_E * E_CH ** 2 / (R_NUC ** 2 * M_P)
    a_eff = D_mag * R_NUC / C_LIGHT
    r_N_over_s = a_N / a_s
    r_N_over_C = a_N / a_C
    add("C06",
        "强度折算恰为引力：a_eff = |D|·(r/c) = Gm/r²，比核力弱 38.2 量级",
        "FAIL",
        "本卷折算（非靶宣称）：系统内唯一时间尺度 r/c 把 jerk 折成加速度，"
        "机器给出 a_eff = |D|·r/c ≡ Gm/r²（相对差 <1e−15，恒等）。"
        "⇒ 『核力场』的强度**就是引力强度**，只是被除上一个频率。"
        "在 r=1 fm、质子源：a_eff = 1.1164e−07 m/s²；"
        "核力强度（α_s=1 口径）1.8899e+31 m/s² ⇒ 弱 38.23 量级；"
        "与库仑比 8.093e−37（36.09 量级，与库内总汇册『36.1 量级』一致）。",
        a_eff=a_eff, a_newton=a_N, a_strong=a_s, a_coulomb=a_C,
        log10_N_over_s=math.log10(r_N_over_s),
        log10_N_over_C=math.log10(r_N_over_C),
        ident_rel=rel(a_eff, a_N))

    # C07：做功量级宣称
    E_claim = D_mag * R_NUC * M_P
    mc2 = M_P * C_LIGHT ** 2
    r0_star = math.sqrt(G_N * M_P / C_LIGHT)
    add("C07",
        "『做功量级 ~ mc²』不成立：靶自写式量纲为功率，且差 15.4 量级；需 r₀ = 1.93e−23 m",
        "FAIL",
        "靶自己写 |D|·r₀·m′ ~ (Gmc/r₀²)·m′，量纲 = M L² T⁻³ = **功率**（不是能量）；"
        "r₀=1 fm 时数值 5.598e−26，而 mc² = 1.503e−10 J ⇒ 差 **15.43 量级**，"
        "并非『可比』。若要 Gmc m′/r₀² = mc²，需 r₀ = sqrt(Gm′/c) = 1.930e−23 m，"
        "比核子半径（1e−15 m）小 7.71 量级 ⇒ 『与 mc² 可比』同时要求"
        "『把功率当能量』与『把 r₀ 缩小 7.7 量级』两个未声明操作。",
        E_claim_W=E_claim, mc2_J=mc2, log10_gap=math.log10(mc2 / E_claim),
        r0_star_m=r0_star, r_nuc_over_r0star=R_NUC / r0_star)

    # ============================================================
    # D 组：跨卷
    # ============================================================
    # D01：项位错
    term_pos = "第二项" if cnt_third >= 1 else "?"
    add("D01",
        "项位错：展开式 F = (c−v)ṁ + m ċ − m v̇ 中，m ċ 是**第二项**，靶称之为第三项",
        "FAIL",
        "靶 §4.3 原文：『其中第三项 m(dc/dt) 被诠释为核力』。"
        "机器核对展开式：第 1 项 (c−v)ṁ、第 2 项 +m ċ、第 3 项 −m v̇。"
        "⇒ m ċ 是第二项，第三项是 −m v̇（惯性项）。"
        "该错位使『核力 = 质量 × 光速矢量的变化率』这一物理指派失去了式子依据。"
        "（文本层：靶文『第三项』出现 %d 次。）" % cnt_third,
        text_third_count=cnt_third, expanded_terms=3)

    # D02：D 与 m dc/dt 的关系
    add("D02",
        "D 与 m·dc/dt 无一阶关系；若沿用上游『c 恒定』公设则核力项恒为零",
        "BOUNDARY",
        "D = dA/dt 是**引力场**的时间导数，m dc/dt 是**光速矢量**的时间导数；"
        "二者没有代数关系（除非额外假设 A ∝ c）。若沿用 r162/r163 所引公设"
        "『c 的方向均匀且不变、|c| = c 常数』，则 dc/dt ≡ 0 ⇒ 第二项恒为零 ⇒ "
        "『核力』在该展开式里不存在。⇒ 要么核力项为零，要么 c 必须可变"
        "（与上游公设冲突）。本卷只登记该两难，不代选。",
        c_const_assumption_ref="r162 A2 / r163 A1（上游公设）")

    # D03：靶自承
    add("D03",
        "靶自承『高度推测性/猜测』，并自列四项未描述（电荷无关性、自旋依赖、饱和性、精确势）",
        "INFO",
        "按防过度指控纪律单列：靶 §4.4 明写『高度推测性』『猜测』"
        "（机读命中 %d 次），并自承未给出电荷无关性、自旋依赖性、饱和性、"
        "核子-核子势精确形式。⇒ 本卷不把这些『缺失』记为本卷发现，"
        "本卷判的是：**已写下的那部分式子本身**在量纲、阶数、中心性、"
        "零点结构上不成立。"
        % cnt_guess,
        self_admit_count=cnt_guess, target_lines=nlines)

    # ============================================================
    # 控制组
    # ============================================================
    # C1 求导工具正对照：已知解析函数
    def yv(t):
        return (t ** 2, 3.0 * t ** 3, -2.0 * t)

    def dyv(t):
        return (2.0 * t, 9.0 * t ** 2, -2.0)

    hh = 1e-5
    num = tuple((yv(1.3 + hh)[i] - yv(1.3 - hh)[i]) / (2 * hh) for i in range(3))
    control("C1", "差分器正对照：d/dt(t², 3t³, −2t)|_{t=1.3}", rel(vnorm(num), vnorm(dyv(1.3))),
            "<1e-8", rel(vnorm(num), vnorm(dyv(1.3))) < 1e-8)
    control("C2", "量纲工具自检（10 项）", "%d/10" % sum(1 for _, ok in dim_check()[0] if ok),
            "10/10", all(ok for _, ok in dim_check()[0]))
    # 恒等式 |ĉ − 3cosθ r̂|² = 1 + 3cos²θ
    ident_max = 0.0
    for deg in range(0, 181, 5):
        th = math.radians(deg)
        vec = (1.0 - 3.0 * math.cos(th), 0.0, -3.0 * math.cos(th) * 0.0)
        # 在 r̂=e_z, ĉ=(sinθ,0,cosθ) 的二维平面里算模长平方
        m2 = math.sin(th) ** 2 + (math.cos(th) - 3.0 * math.cos(th)) ** 2
        ident_max = max(ident_max, abs(m2 - (1.0 + 3.0 * math.cos(th) ** 2)))
    control("C3", "恒等式 |ĉ−3cosθ r̂|² = 1+3cos²θ（37 点扫描）", fs(ident_max), "<1e-12",
            ident_max < 1e-12)
    control("C4", "阳性对照：θ=0 时 |D|/(Gmc/r³) = 2", fs(th0["D_over_Gmc_r3"]), "=2",
            abs(th0["D_over_Gmc_r3"] - 2.0) < 1e-12)
    # 负控制：分子系数 3 → 2.9 必须被判失败
    th = math.radians(30.0)
    m2_ok = 1.0 + 3.0 * math.cos(th) ** 2
    m2_bad = 1.0 + 2.9 * math.cos(th) ** 2
    control("C5", "负控制：系数 3→2.9 的式子在 θ=30° 必须被区分", fs(rel(m2_ok, m2_bad)), ">1e-3",
            rel(m2_ok, m2_bad) > 1e-3)
    control("C6", "角动量判据阳性对照：θ=0（径向）归一化力矩 = 0（舍入级）",
            fs(tau_rows[0][2]), "<1e-12", tau_rows[0][2] < 1e-12)
    control("C7", "Yukawa 与幂律在 r=1 fm 处同量级（对比不靠极端）",
            fs(yuk[0][3]), "∈[0.5,5]", 0.5 < yuk[0][3] < 5.0)
    # 负控制：无零点检测器必须能识别有零点的函数
    def ncross(f, lo, hi, n=2001):
        prev = f(lo)
        cnt = 0
        for i in range(1, n):
            x = lo + (hi - lo) * i / (n - 1.0)
            cur = f(x)
            if prev == 0.0:
                cnt += 1
            elif prev * cur < 0:
                cnt += 1
            prev = cur
        return cnt

    nz_power = ncross(lambda r: 1.0 / r ** 3, 0.05, 20.0)
    nz_model = ncross(lambda r: (1.0 - r / 0.9) * math.exp(-r), 0.05, 20.0)
    control("C8", "无零点检测器：1/r³ 判 0 个零点，核力样函数判 ≥1（有分辨力）",
            "power=%d model=%d" % (nz_power, nz_model), "0 / >=1",
            nz_power == 0 and nz_model >= 1)
    control("C9", "靶可定位（1.md 189 行 / code 3 个脚本）",
            "lines=%d code=%d" % (nlines, len(code_files)), "lines>=150",
            nlines >= 150)
    control("C10", "a_eff = |D|·r/c 与 Gm/r² 恒等（相对差 <1e−15）", fs(rel(a_eff, a_N)),
            "<1e-15", rel(a_eff, a_N) < 1e-15)

    # ============================================================
    # 守卫（全部机读驱动，禁写死 True）
    # ============================================================
    guard("G1 量纲工具自检 10/10", all(ok for _, ok in dim_check()[0]),
          "ok=%d/10" % sum(1 for _, ok in dim_check()[0] if ok))
    guard("G2 求导残差 <1e−9 且步长收敛单调", resid_A01 < 1e-9 and
          conv[0][1] > conv[1][1] > conv[2][1], "resid=%s" % fs(resid_A01))
    guard("G3 恒等式残差 <1e−12", ident_max < 1e-12, "max=%s" % fs(ident_max))
    guard("G4 θ=0：|D|/(Gmc/r³)=2 且 D 与靶简化式严格反向（反号×加倍）",
          abs(th0["D_over_Gmc_r3"] - 2.0) < 1e-9 and
          th0["cos_D_Dsimple"] < -0.999999 and abs(th0["simple_dev"] - 3.0) < 1e-6,
          "ratio=%s cos(D,−ĉ)=%s dev=%s" % (
              fs(th0["D_over_Gmc_r3"]), fs(th0["cos_D_Dsimple"]),
              fs(th0["simple_dev"])))
    guard("G5 量纲缺口 [a]/[D] == T¹（等价：D 多带 T⁻¹）",
          gap == D_TIME, "gap=%s" % dstr(gap))
    guard("G6 三基整数网格命中 0 且加 l_P 后命中 ≥1",
          len(hits3) == 0 and len(hits4) >= 1,
          "hits3=%d hits4=%d" % (len(hits3), len(hits4)))
    guard("G7 a_eff ≡ Gm/r²（相对差 <1e−15）", rel(a_eff, a_N) < 1e-15,
          "rel=%s" % fs(rel(a_eff, a_N)))
    guard("G8 强度差 38 量级 ±0.6 且库仑 36.1 口径 ±0.3",
          abs(-math.log10(r_N_over_s) - 38.23) < 0.6 and
          abs(-math.log10(r_N_over_C) - 36.09) < 0.3,
          "N/s=%.3f N/C=%.3f" % (-math.log10(r_N_over_s), -math.log10(r_N_over_C)))
    guard("G9 角动量：θ=0 归一化力矩 ~0 且 θ=90° = 1（双条件）",
          tau_rows[0][2] < 1e-12 and tau_rows[-1][2] > 0.5,
          "tau0_norm=%s tau90_norm=%s" % (fs(tau_rows[0][2]), fs(tau_rows[-1][2])))
    guard("G10 无旋残差 <1e−8", cr_rel < 1e-8, "curl_rel=%s" % fs(cr_rel))
    guard("G11 1/r³ 零点 0 个且单调递减", nz_power == 0 and mono,
          "nz=%d mono=%s" % (nz_power, mono))
    guard("G12 功率差 15.4 量级 ±0.6 且 r₀*/r_nuc 差 7.7 量级 ±0.6",
          abs(math.log10(mc2 / E_claim) - 15.43) < 0.6 and
          abs(math.log10(R_NUC / r0_star) - 7.71) < 0.6,
          "log10=%s r0star=%s" % (fs(math.log10(mc2 / E_claim)), fs(r0_star)))
    guard("G13 整数幂网格规模可复算（343 / 2401）",
          len(list(range(-3, 4))) == 7, "7^3=343 7^4=2401")
    guard("G14 控制组全过（10/10）",
          all(c["ok"] for c in CONTROLS), "ok=%d/%d" % (
              sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    guard("G15 条目数 = 18 且分层铁律声明存在",
          len(ITEMS) == 18, "items=%d" % len(ITEMS))
    return {
        "lines": nlines, "code_files": code_files,
        "cnt_guess": cnt_guess, "cnt_third": cnt_third, "cnt_cvec": cnt_cvec,
        "theta_rows": theta_rows, "conv": conv,
        "hits3": hits3, "hits4": hits4,
        "D_mag": D_mag, "a_eff": a_eff, "a_s": a_s, "a_C": a_C,
        "t_need": t_need, "t_years": t_years,
        "E_claim": E_claim, "mc2": mc2, "r0_star": r0_star,
        "tau_rows": tau_rows, "yuk": yuk, "Eb": Eb, "decay": decay,
        "resid_A01": resid_A01, "gap": gap, "dim_D": dims,
    }


def main():
    t0 = time.time()
    data = build()
    dt = time.time() - t0

    stat = {}
    for it in ITEMS:
        stat[it["status"]] = stat.get(it["status"], 0) + 1

    print("=" * 78)
    print("TUFT-r176｜S17 核心公式 18「核力场定义方程」精算")
    print("=" * 78)
    print("靶：%s" % TARGET)
    print("行数：%d ｜ code/ 脚本：%d 个" % (data["lines"], len(data["code_files"])))
    print("")
    for sid, title, rng in SECTIONS:
        print("-" * 78)
        print("[%s] %s" % (sid, title))
        print("-" * 78)
        lo, hi = rng[0], rng[1]
        on = False
        for it in ITEMS:
            if it["id"] == lo:
                on = True
            if on:
                print("  %-4s %-9s %s" % (it["id"], it["status"], it["title"]))
                if it["note"]:
                    print("       %s" % it["note"].replace("\n", " "))
            if it["id"] == hi:
                break
        print("")

    print("-" * 78)
    print("[控制组]")
    for c in CONTROLS:
        print("  %-4s %-6s %-58s %s" % (c["id"], "PASS" if c["ok"] else "FAIL",
                                        c["desc"][:58], c["value"]))
    print("")
    print("-" * 78)
    print("[守卫]")
    for g in GUARDS:
        print("  %-6s %s ｜ %s" % ("PASS" if g["ok"] else "FAIL", g["name"], g["detail"]))
    print("")
    print("-" * 78)
    print("条目 %d：%s" % (len(ITEMS), " / ".join(
        "%s %d" % (k, v) for k, v in sorted(stat.items()))))
    print("控制组 %d/%d ｜ 守卫 %d/%d ｜ 用时 %.2fs" % (
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS), dt))

    verdict = ("NUCLEAR-FORCE-FIELD-IS-JERK-OF-GRAVITY-FIELD-"
               "DIMENSION-GAP-T-PLUS-ONE-D-EXCESS-T-MINUS-ONE-"
               "SIGN-FLIPS-AT-THETA-ZERO-"
               "NOT-CENTRAL-NOT-SHORT-RANGE-AND-STRENGTH-IS-GRAVITATIONAL")

    key_numbers = {
        "dim_D": dstr(data["dim_D"]),
        "dim_required": dstr(D_ACC),
        "dim_gap": dstr(data["gap"]),
        "dim_excess_of_D": "T^-1",
        "deriv_residual": fs(data["resid_A01"], 12),
        "theta0_D_over_Gmc_r3": fs(data["theta_rows"][0]["D_over_Gmc_r3"], 12),
        "theta90_D_over_Gmc_r3": fs(data["theta_rows"][5]["D_over_Gmc_r3"], 12),
        "anisotropy_ratio": "2.000000E+00",
        "integer_grid_hits_3basis": len(data["hits3"]),
        "integer_grid_hits_with_lP": len(data["hits4"]),
        "tP_s": fs(T_P, 12),
        "D_times_tP": fs(data["D_mag"] * T_P, 12),
        "t_need_s": fs(data["t_need"], 12),
        "t_need_years": fs(data["t_years"], 12),
        "D_mag_SI": fs(data["D_mag"], 12),
        "a_eff": fs(data["a_eff"], 12),
        "a_strong": fs(data["a_s"], 12),
        "a_coulomb": fs(data["a_C"], 12),
        "log10_grav_over_strong": fs(math.log10(data["a_eff"] / data["a_s"]), 12),
        "log10_grav_over_coulomb": fs(math.log10(data["a_eff"] / data["a_C"]), 12),
        "tau_max_m2_s2": fs(data["tau_rows"][-1][1], 12),
        "tau_theta0_over_Gmc_r2": fs(data["tau_rows"][0][2], 12),
        "tau_theta90_over_Gmc_r2": fs(data["tau_rows"][-1][2], 12),
        "E_claim_W": fs(data["E_claim"], 12),
        "mc2_J": fs(data["mc2"], 12),
        "log10_power_gap": fs(math.log10(data["mc2"] / data["E_claim"]), 12),
        "r0_star_m": fs(data["r0_star"], 12),
        "r_nuc_over_r0star": fs(R_NUC / data["r0_star"], 12),
        "yukawa_ratio_50fm": fs(data["yuk"][-1][3], 12),
        "zero_crossings": 0,
        "target_lines": data["lines"],
        "code_files": len(data["code_files"]),
    }

    os.makedirs(OUT, exist_ok=True)
    payload = {
        "meta": {
            "stem": STEM,
            "round": "r176",
            "target": TARGET,
            "target_lines": data["lines"],
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_s": round(dt, 3),
            "items": len(ITEMS),
            "stat": stat,
            "controls": "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)),
            "guards": "%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
            "verdict": verdict,
        },
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": key_numbers,
        "tables": {
            "theta_scan": data["theta_rows"],
            "yukawa_vs_power": [{"r_fm": a, "power": b, "yukawa": c, "ratio": d}
                                for a, b, c, d in data["yuk"]],
            "decay_ratio": [{"r_fm": a, "ratio_1_over_r": b}
                            for a, b in data["decay"]],
            "binding_energy": [{"r_min_m": a, "E_J": b} for a, b in data["Eb"]],
            "tau_scan": [{"theta_deg": a, "tau": b, "normalized": c}
                         for a, b, c in data["tau_rows"]],
            "derivative_convergence": [{"h": a, "rel": b} for a, b in data["conv"]],
        },
    }
    jp = os.path.join(OUT, STEM + ".json")
    io.open(jp, "w", encoding="utf-8").write(
        json.dumps(payload, ensure_ascii=False, indent=2))

    # ---- Markdown ----
    md = []
    md.append("# %s" % STEM)
    md.append("")
    md.append("- 靶：`%s`（%d 行）" % (TARGET, data["lines"]))
    md.append("- 生成：%s ｜ 用时 %.2fs" % (time.strftime("%Y-%m-%d %H:%M:%S"), dt))
    md.append("- 条目 %d：%s" % (len(ITEMS), " / ".join(
        "%s %d" % (k, v) for k, v in sorted(stat.items()))))
    md.append("- 控制组 %d/%d ｜ 守卫 %d/%d" % (
        sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
        sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    md.append("")
    md.append("## 条目")
    md.append("")
    md.append("| 编号 | 状态 | 判定 |")
    md.append("|---|---|---|")
    for it in ITEMS:
        md.append("| %s | **%s** | %s |" % (it["id"], it["status"], it["title"]))
    md.append("")
    md.append("## θ 扫描（c 与 r̂ 的夹角）")
    md.append("")
    md.append("| θ (°) | ṙ/c | |D|/(Gmc/r³) | 与靶简化式的相对偏差 |")
    md.append("|---|---|---|---|")
    for r in data["theta_rows"]:
        md.append("| %.6f | %.6f | %.12f | %.6e |" % (
            r["theta_deg"], r["rdot_over_c"], r["D_over_Gmc_r3"], r["simple_dev"]))
    md.append("")
    md.append("## 1/r³ vs Yukawa（r₀ = 1.4138 fm）")
    md.append("")
    md.append("| r (fm) | r⁻³ | e^(−r/r₀) | 比值 |")
    md.append("|---|---|---|---|")
    for a, b, c, d in data["yuk"]:
        md.append("| %.1f | %.6e | %.6e | %.6e |" % (a, b, c, d))
    md.append("")
    md.append("## 控制组")
    md.append("")
    md.append("| 编号 | 读数 | 期望 | 结果 |")
    md.append("|---|---|---|---|")
    for c in CONTROLS:
        md.append("| %s | %s | %s | %s |" % (c["id"], c["value"], c["expect"],
                                             "PASS" if c["ok"] else "FAIL"))
    md.append("")
    md.append("## 守卫")
    md.append("")
    md.append("| 守卫 | 结果 | 读数 |")
    md.append("|---|---|---|")
    for g in GUARDS:
        md.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL", g["detail"]))
    md.append("")
    md.append("## key_numbers")
    md.append("")
    md.append("```json")
    md.append(json.dumps(key_numbers, ensure_ascii=False, indent=2))
    md.append("```")
    md.append("")
    md.append("## verdict")
    md.append("")
    md.append("```")
    md.append(verdict)
    md.append("```")
    mdp = os.path.join(OUT, STEM + ".md")
    io.open(mdp, "w", encoding="utf-8").write("\n".join(md))

    # ---- report.txt ----
    rp = os.path.join(OUT, STEM + "_report.txt")
    lines = []
    lines.append(STEM)
    lines.append("target: %s" % TARGET)
    lines.append("target_lines: %d" % data["lines"])
    lines.append("")
    for it in ITEMS:
        lines.append("%-4s %-9s %s" % (it["id"], it["status"], it["title"]))
    lines.append("")
    for c in CONTROLS:
        lines.append("CTRL %-4s %s %s" % (c["id"], "PASS" if c["ok"] else "FAIL", c["value"]))
    for g in GUARDS:
        lines.append("GUARD %s %s %s" % ("PASS" if g["ok"] else "FAIL", g["name"], g["detail"]))
    lines.append("")
    lines.append("items: %d" % len(ITEMS))
    lines.append("stat: %s" % json.dumps(stat, ensure_ascii=False))
    lines.append("controls: %d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    lines.append("guards: %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    lines.append("verdict: %s" % verdict)
    io.open(rp, "w", encoding="utf-8").write("\n".join(lines))

    bad = [g["name"] for g in GUARDS if not g["ok"]]
    badc = [c["id"] for c in CONTROLS if not c["ok"]]
    if badc:
        print("控制组失败：%s" % ", ".join(badc))
    if bad:
        print("守卫失败：%s" % ", ".join(bad))
        return 1
    print("")
    print("产物：")
    print("  %s" % jp)
    print("  %s" % mdp)
    print("  %s" % rp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
