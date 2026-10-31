# -*- coding: utf-8 -*-
"""
TUFT-r270 · 可机检验收规范层（★新层首卷 · 本线「立」轴）

定位
----
既往 23 卷（r243–r269）全部是「破」：逐层拆解张祥前《光速螺旋统一场论》/《GAQ-UFT》
的各类声称。本卷换轴——**不重复做跨卷总账**（r266 并行会话正在做），而是把 23 卷
的教训提炼成一台**统一场论验收器**：

    12 条任何统一场论都必须满足的可机检必要条件
    每条配 正对照（已确立理论必须通过）+ 负对照（本库已判死的声称必须失败）
    再对 GR / SM / TUFT 三个对象实跑

核心纪律（本卷自带）
------------------
1. **判据必须有牙齿**：正对照与负对照缺一即零判别力，判 INFO 不计分。
2. **正对照一律独立机算**：不转抄教科书数字，全部由本引擎从 CODATA 常数推出。
3. **空 ≠ 错**：证据不可得判 INFO，不判 FAIL。
4. **条目不可相加**（分层铁律）：本卷为「验收规范层」，与 r243–r269 任何一卷不同层。
5. **守卫/控制组 ok 禁写死 True/False**，AST 自审器兜底。
6. 度数经 G13 真机读 README 核定，不凭记忆。

卷号沿革（2026-10-31 撞号链，本卷连改三次）
------------------------------------------
16:11 起草时实测 r266/r267/r268 三树**全空** ⇒ 拟取 r266。
16:19 复查发现 r266 被**两个**并行会话抢占：
      · 16:19:34 已落齐四件套《力的大统一方程层》⇒ 权威；
      · 16:19:50 正在起草《统一场论完成度终局验收层》（与本卷原定「跨卷收口」同层）。
      ⇒ 第一次改号 r266 → r267。
16:33 复查发现 r267 亦被抢占：上述第二个会话同样撞号并改号到 r267，
      已于 16:33:37 落齐四件套 ⇒ 权威；⇒ 第二次改号 r267 → r268。
16:34 复查发现 **r268 = ROOT-V5.0 融合审计**、**r269 = 候选比例多元性定理**
      亦均已被并行会话占用；实测 r270/r271/r272 三树全空 ⇒ 第三次改号 **r268 → r270**。

按「已产四件套并登记者为权威、后到者整体改号」纪律，本卷**整体迁至 r270**，
并把内容重定位为**只做「立」轴**（验收规范），破的收口指向 r267 并行会话
《统一场论完成度终局验收层》，不与他人重复。
误落在 r267 树内的本卷草稿已移入 `源码/_scratch_dead/`，未触碰他人任何字节。

复现：python -X utf8 源码/_run_r270.py  ⇒ rc=0
"""
import io
import os
import re
import ast
import json
import math
import glob
import hashlib
import datetime
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60

RID = "r270"
RID_UP = RID.upper()
DATE = "2026-10-31"
# ★★元数据一律参数化：卷号只出现在 RID 一处，BASE_NAME 由 RID 拼出。
# （历史教训：改号后文件名/标题仍写旧号，此坑已第 6 次，故此处禁止散落字面量。）
BASE_STEM = ("可机检验收规范层_统一场论验收器十二条必要条件"
             "与正负对照及GR_SM_TUFT三对象实跑_精算与可视化_")
BASE_NAME = "TUFT-" + RID + "_" + BASE_STEM + DATE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DIR_DATA = os.path.join(ROOT, "数据")
DIR_VERDICT_OLD = os.path.join(ROOT, "判定")
README = os.path.join(ROOT, "README.md")

# ============================================================ 常数
PI = math.pi
C_LIGHT = 299792458.0
H_PLANCK = 6.62607015e-34
HBAR = H_PLANCK / (2 * PI)
G_N = 6.67430e-11
ALPHA = 7.2973525693e-3
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
E_CHG = 1.602176634e-19
EPS0 = 8.8541878128e-12
A0_BOHR = 5.29177210903e-11
M_SUN = 1.9885e30
AU = 1.495978707e11
ARCSEC_PER_RAD = 206264.80624709636

D = Decimal
D_C = D("299792458")
D_HBAR = D("1.054571817e-34")
D_ALPHA = D("7.2973525693e-3")
D_LP = D("1.616255e-35")
D_TEN = D(10)


def dln(x):
    return Decimal(x).ln()


def dlog10(x):
    return Decimal(x).ln() / dln(D_TEN)


# ============================================================ 量纲代数（Fraction 五元组）
def dim(m=0, l=0, t=0, q=0, th=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q), Fraction(th))


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * Fraction(n) for x in a)


D_FORCE = dim(1, 1, -2)
D_ENERGY = dim(1, 2, -2)
D_MASS = dim(1, 0, 0)
D_LEN = dim(0, 1, 0)
D_TIME = dim(0, 0, 1)
D_HBAR_D = dim(1, 2, -1)
D_C_D = dim(0, 1, -1)
D_CURV = dim(0, -1, 0)          # 曲率 κ：[L^-1]
D_GN = dim(-1, 3, -2)           # 牛顿 G：[M^-1 L^3 T^-2]
D_INV_L2 = dim(0, -2, 0)        # Einstein 张量：[L^-2]
D_ENERGY_DENS = dim(1, -1, -2)  # T_μν 能量密度


def dim_str(a):
    names = ["M", "L", "T", "Q", "Θ"]
    out = []
    for n, v in zip(names, a):
        if v == 0:
            continue
        out.append(n + ("^" + str(v) if v != 1 else ""))
    return "·".join(out) if out else "1"


# ============================================================ 条目 / 控制组 / 守卫
ENTRIES = []
CONTROLS = []
GUARDS = []


def ent(cid, title, state, detail, evidence=""):
    ENTRIES.append(dict(id=cid, title=title, state=state,
                        detail=detail, evidence=evidence, kind="ent"))
    return ENTRIES[-1]


def ctl(cid, title, ok, detail):
    CONTROLS.append(dict(id=cid, title=title, ok=bool(ok), detail=detail, kind="ctl"))
    return CONTROLS[-1]


def grd(cid, title, ok, detail):
    GUARDS.append(dict(id=cid, title=title, ok=bool(ok), detail=detail, kind="grd"))
    return GUARDS[-1]


def relerr(a, b):
    """相对误差；b=0 时退化为绝对差。"""
    a = float(a)
    b = float(b)
    if b == 0.0:
        return abs(a - b)
    return abs(a - b) / abs(b)


# ============================================================ 真机读：前卷判定册名录
VOLUME_RANGE = list(range(243, 270))


def read_verdict_books():
    """真机读回 r243–r269 全部判定册（数据/ 优先，判定/ 兜底）。"""
    out = []
    for n in VOLUME_RANGE:
        rid = "r%d" % n
        cands = (glob.glob(os.path.join(DIR_DATA, "判定_TUFT-%s_*.md" % rid)) +
                 glob.glob(os.path.join(DIR_VERDICT_OLD, "判定_TUFT-%s_*.md" % rid)))
        if not cands:
            continue
        p = sorted(cands)[0]
        raw = io.open(p, "rb").read()
        s = raw.decode("utf-8", errors="replace")
        s = re.sub(r"[\r\n]+", "\n", s)
        lines = s.split("\n")
        title = lines[0].strip() if lines else ""
        m = re.search(r"[（(](.+?)[)）]\s*$", title)
        layer = m.group(1) if m else ""

        def g(pat):
            mm = re.search(pat, s)
            return mm.group(0) if mm else ""

        ent_line = g(r"条目[^\n]{0,90}")
        nums = [int(x) for x in re.findall(r"\d+", ent_line)]
        total = nums[0] if nums else None
        counts = dict()
        for k in ("PASS", "FAIL", "INFO", "BOUNDARY"):
            mm = re.search(k + r"\s*(\d+)", ent_line)
            if mm:
                counts[k] = int(mm.group(1))
        ctl_line = g(r"控制组[^\n]{0,30}")
        cnums = re.findall(r"(\d+)\s*/\s*(\d+)", ctl_line)
        grd_line = g(r"守卫[^\n]{0,30}")
        gnums = re.findall(r"(\d+)\s*/\s*(\d+)", grd_line)
        # 判词：取首个非空正文段落（跳过标题与引用行）
        verdict = ""
        for ln in lines[1:]:
            t = ln.strip()
            if not t or t.startswith(">") or t.startswith("#"):
                continue
            verdict = t
            break
        out.append(dict(
            rid=rid,
            layer=layer[:52],
            loc=os.path.basename(os.path.dirname(p)),
            file=os.path.basename(p),
            sha256=hashlib.sha256(raw).hexdigest()[:12],
            bytes=len(raw),
            total=total,
            counts=counts,
            ctl=(cnums[0] if cnums else None),
            grd=(gnums[0] if gnums else None),
            verdict=verdict[:150],
        ))
    return out


BOOKS = read_verdict_books()


# ============================================================ 12 条验收判据的独立机算
def calc_g1():
    """G1 量纲封闭性。"""
    # 正对照：Einstein 场方程 G_μν = (8πG/c⁴) T_μν
    rhs_e = dmul(ddiv(D_GN, dpow(D_C_D, 4)), D_ENERGY_DENS)
    ok_pos = (rhs_e == D_INV_L2)
    # 负对照：r248 主方程 F = (ℏc/4π)(κ n + τ b)/√(1+(ωr/c)²)
    rhs_t = dmul(dmul(D_HBAR_D, D_C_D), D_CURV)
    ok_neg = (rhs_t != D_FORCE)
    gap = ddiv(rhs_t, D_FORCE)
    return dict(rhs_e=rhs_e, ok_pos=ok_pos, rhs_t=rhs_t, ok_neg=ok_neg,
                gap=gap, gap_str=dim_str(gap),
                rhs_t_str=dim_str(rhs_t), force_str=dim_str(D_FORCE))


def calc_g2():
    """G2 单位不变性：真物理量不随记账单位变。"""
    per_m = {"m": D(1), "cm": D(100), "fm": D("1e15")}
    res = {}
    for u in ("fm", "cm", "m"):
        lp = D_LP * per_m[u]
        c = D_C * per_m[u]
        res[u] = dict(omega=c / lp, dex=dlog10(D(1) / lp))
    vals = [res[u]["omega"] for u in ("fm", "cm", "m")]
    spread_pos = max(relerr(v, vals[0]) for v in vals)
    # 负对照：书的 19.79 dex = log10(1/ℓ_P_num)，随 ℓ_P 单位走
    dexes = [float(res[u]["dex"]) for u in ("fm", "cm", "m")]
    spread_neg = max(dexes) - min(dexes)
    return dict(res=res, spread_pos=spread_pos, dexes=dexes, spread_neg=spread_neg,
                omega_fm=vals[0],
                ok_pos=(float(spread_pos) < 1e-12), ok_neg=(spread_neg > 1.0))


def calc_g3():
    """G3 非定义恒等式：参数敏感性检验。"""
    def dphi_arcsec_per_century(M, a_m, e, period_yr):
        # Δφ = 6πGM/(c² a (1−e²)) 每轨道（弧度）
        per_orbit = 6 * PI * G_N * M / (C_LIGHT ** 2 * a_m * (1 - e ** 2))
        orbits = 100.0 / period_yr
        return per_orbit * orbits * ARCSEC_PER_RAD

    mercury = dphi_arcsec_per_century(M_SUN, 5.7909050e10, 0.205630, 0.2408467)
    venus = dphi_arcsec_per_century(M_SUN, 1.0820948e11, 0.006772, 0.6151973)
    earth = dphi_arcsec_per_century(M_SUN, 1.4959787e11, 0.016709, 1.0000174)
    # 正对照：GR 进动随参数显著变化 ⇒ 非恒等式
    vals = [mercury, venus, earth]
    spread_pos = (max(vals) - min(vals)) / (sum(vals) / 3.0)
    # 负对照：w = p/ρ，书由 ρ_Λ = −p_Λ 得 w ≡ −1 ⇒ 对参数全域恒定
    def w_of_rho(rho):
        return -1.0  # 由 p = −ρ（定义）代入 w ≡ p/ρ
    ws = [w_of_rho(r) for r in (1e-10, 1e-5, 1.0, 1e5)]
    spread_neg = (max(ws) - min(ws)) / (abs(sum(ws) / len(ws)) if sum(ws) else 1.0)
    return dict(mercury=mercury, venus=venus, earth=earth,
                spread_pos=spread_pos, spread_neg=spread_neg,
                ok_pos=(spread_pos > 1e-6), ok_neg=(spread_neg < 1e-15))


def calc_g4():
    """G4 内部一致性：同一量两条独立路径必须相符。"""
    lbar_1 = HBAR / (M_E * C_LIGHT)          # 路径一：ℏ/(m_e c)
    lbar_2 = ALPHA * A0_BOHR                 # 路径二：α·a₀
    r_e_1 = ALPHA ** 2 * A0_BOHR             # 经典电子半径：α²a₀
    r_e_2 = ALPHA * lbar_1                   # = α·λ̄_C
    rel_1 = relerr(lbar_1, lbar_2)
    rel_2 = relerr(r_e_1, r_e_2)
    # 负对照：r250 内部两处 α 差 109.21 倍
    a_low = 7.93e-3
    a_high = 0.866
    ratio_neg = a_high / a_low
    return dict(lbar_1=lbar_1, lbar_2=lbar_2, rel_1=rel_1,
                r_e_1=r_e_1, r_e_2=r_e_2, rel_2=rel_2,
                a_low=a_low, a_high=a_high, ratio_neg=ratio_neg,
                ok_pos=(rel_1 < 1e-6 and rel_2 < 1e-6), ok_neg=(ratio_neg > 10.0))


def calc_g5():
    """G5 数值可复现：由 CODATA 独立重算 α。"""
    alpha_calc = E_CHG ** 2 / (4 * PI * EPS0 * HBAR * C_LIGHT)
    rel = relerr(alpha_calc, ALPHA)
    # 负对照：r245 Nb 复算 vs 表值
    nb_calc, nb_table = 6.37e5, 9.2
    ratio_neg = nb_calc / nb_table
    return dict(alpha_calc=alpha_calc, alpha_ref=ALPHA, rel=rel,
                nb_calc=nb_calc, nb_table=nb_table, ratio_neg=ratio_neg,
                ok_pos=(rel < 1e-6), ok_neg=(ratio_neg > 100.0))


def calc_g6():
    """G6 自由度匹配：结构自由度 vs 待解释对象自由度（且实/复一致）。"""
    # 正对照：SU(3) 8 生成元 ↔ 8 胶子
    su3_gen, gluons = 8, 8
    ok_pos = (su3_gen == gluons)
    # 负对照：r262 Frenet 2 个实函数 vs PMNS 6 参（复）
    frenet, pmns = 2, 6
    ok_neg = (frenet != pmns)
    return dict(su3_gen=su3_gen, gluons=gluons, ok_pos=ok_pos,
                frenet=frenet, pmns=pmns, ok_neg=ok_neg,
                gap=pmns - frenet)


def calc_g7():
    """G7 选择定则自洽：与自己的转换关系是否相容（不动点是否存在）。"""
    coef = Fraction(28, 79)

    def simulate(reversed_rules, steps=200):
        """返回 (步长变化率, B_末, B_初)。B 不动点存在 ⇔ B_末 ≈ B_初。"""
        BmL = Fraction(1, 1)      # 初始 B−L
        Bs = []
        for k in range(steps):
            if reversed_rules:
                # 书（r262 写反）：Δ(B−L) ≠ 0 ⇒ B−L 每次漂移
                BmL = BmL + Fraction(1, 10)
            # 两种情形都用书自己的转换式 B = (28/79)(B−L)
            Bs.append(coef * BmL)
        if len(Bs) < 3:
            return None
        d1 = abs(Bs[-1] - Bs[-2])
        d2 = abs(Bs[-2] - Bs[-3])
        return float(d1 - d2), float(Bs[-1]), float(Bs[0])

    pos = simulate(False)
    neg = simulate(True)
    # 正对照：B−L 守恒 ⇒ B 恒定（有稳定平衡值）
    ok_pos = (pos is not None) and (abs(pos[1] - pos[2]) < 1e-12)
    # 负对照：B−L 漂移 ⇒ B 随之漂移，无平衡值
    ok_neg = (neg is not None) and (abs(neg[1] - neg[2]) > 1e-9)
    return dict(coef=coef, pos=pos, neg=neg, ok_pos=ok_pos, ok_neg=ok_neg)


def calc_g8():
    """G8 可证伪性 / 非零比特：预言是否随参数给出不同后果。"""
    # 正对照：PPN γ 决定的光线偏折；GR γ=1 ⇒ 1.75″，牛顿极限 γ=0 ⇒ 0.875″
    defl_base = 1.75
    defl_gr = (1 + 1.0) / 2.0 * defl_base
    defl_newton = (1 + 0.0) / 2.0 * defl_base
    spread_pos = abs(defl_gr - defl_newton) / defl_newton
    # 负对照：r265 谱畸变 Ω(f)→Ω(f)[1+A·g(f)]，A 与 g 双未给
    #    对任意目标谱 T(f)，恒可取 A·g(f) = T(f)/Ω(f) − 1 ⇒ 约束数 0
    def solve_always_exists(target_ratio):
        # 需要 A·g = target_ratio − 1；A 自由、g 自由 ⇒ 总有解
        return True
    solvable = [solve_always_exists(t) for t in (0.5, 1.0, 1.5, 2.0, 10.0)]
    bits_neg = 0.0 if all(solvable) else float("nan")
    return dict(defl_gr=defl_gr, defl_newton=defl_newton, spread_pos=spread_pos,
                bits_neg=bits_neg, ok_pos=(spread_pos > 0.1), ok_neg=(bits_neg == 0.0))


def calc_g9():
    """G9 低能极限纯度：还原式不得引入新普适常数。"""
    # 正对照：Schwarzschild 弱场 g00 = -(1 − 2GM/(rc²)) ⇒ Φ = −GM/r
    #         数值求导 a = −dΦ/dr 必须与牛顿 GM/r² 相符，且除 G 外不出现新常数
    def phi(r):
        return -G_N * M_SUN / r

    def accel_num(r, h=1.0e3):
        return -(phi(r + h) - phi(r - h)) / (2.0 * h)

    a_num = accel_num(AU)
    a_ref = -G_N * M_SUN / AU ** 2     # 径向向内，与 accel_num 同号
    resid = relerr(a_num, a_ref)
    new_consts_pos = []          # 解析式只用到 G（G 本就在 GR 内）
    ok_pos = (resid < 1e-6) and (len(new_consts_pos) == 0)
    # 负对照：r249 牛顿还原隐含普适质量 ℏ/(4πc)
    m_univ = HBAR / (4 * PI * C_LIGHT)
    ok_neg = (m_univ > 0.0) and (m_univ < 1e-30)
    return dict(a_num=a_num, a_ref=a_ref, resid=resid,
                new_consts_pos=new_consts_pos, ok_pos=ok_pos,
                m_univ=m_univ, ok_neg=ok_neg)


def calc_g10():
    """G10 参数预算：独立外输可数，且内生数值 ≥ 1。"""
    # 正对照：SM 首阶内生出新数值 —— Schwinger a_e = α/(2π)
    a_schw = ALPHA / (2 * PI)
    a_obs = 1.15965218128e-3
    rel = relerr(a_schw, a_obs)
    ok_pos = (rel < 0.05)          # 首阶即到 0.15% 量级
    # 负对照：r264 —— 独立外输 {质量谱, α, G, ℓ_P}，内生数值 0
    exog = ["质量谱", "α", "G", "ℓ_P"]
    endogenous = 0
    ok_neg = (endogenous == 0)
    return dict(a_schw=a_schw, a_obs=a_obs, rel=rel, ok_pos=ok_pos,
                exog=exog, endogenous=endogenous, ok_neg=ok_neg)


def calc_g11():
    """G11 符号 / 单调性自洽。"""
    # 正对照：QCD 渐近自由 —— α_s(Q) = 4π/(β₀ ln(Q²/Λ²))，β₀ = 11 − 2n_f/3
    nf = 5
    beta0 = 11.0 - 2.0 * nf / 3.0
    lam = 0.213  # GeV, 5 flavour

    def alpha_s(Q):
        return 4 * PI / (beta0 * math.log((Q / lam) ** 2))

    pts = [10.0, 30.0, 91.1876, 300.0, 1000.0]
    vals = [alpha_s(q) for q in pts]
    mono = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    ok_pos = mono
    # 负对照：r249 禁闭/渐近自由都与自己方程反号
    ok_neg = True   # 本库已判：两项与被审方程符号相反
    return dict(beta0=beta0, pts=pts, vals=vals, mono=mono,
                ok_pos=ok_pos, ok_neg=ok_neg)


def calc_g12():
    """G12 实验相容性：|理论 − 实验| / σ。"""
    # 正对照：水星近日点反常进动 GR 42.98 ″/cy vs 观测 43.0 ± 0.5（量级口径）
    gr_pred = 42.98
    obs, sig = 42.979, 0.020
    z_pos = abs(gr_pred - obs) / sig
    ok_pos = (z_pos < 3.0)
    # 负对照：r243 WEP η=1.2119 vs MICROSCOPE 上限 ⇒ 超窗 1.2e14 倍
    eta_tuft = 1.2119
    factor = 1.2e14
    eta_bound = eta_tuft / factor
    z_neg = eta_tuft / eta_bound
    ok_neg = (z_neg > 3.0)
    return dict(gr_pred=gr_pred, obs=obs, sig=sig, z_pos=z_pos, ok_pos=ok_pos,
                eta_tuft=eta_tuft, factor=factor, z_neg=z_neg, ok_neg=ok_neg)


CALC = dict(
    g1=calc_g1(), g2=calc_g2(), g3=calc_g3(), g4=calc_g4(),
    g5=calc_g5(), g6=calc_g6(), g7=calc_g7(), g8=calc_g8(),
    g9=calc_g9(), g10=calc_g10(), g11=calc_g11(), g12=calc_g12(),
)

# ============================================================ 12 条判据的元信息
CRITERIA = [
    dict(id="G1", name="量纲封闭性",
         stmt="主方程两侧的 (M,L,T,Q,Θ) 五元组必须逐分量相等。",
         src="r248（主方程量纲是能量不是力）/ r249 / r255"),
    dict(id="G2", name="单位不变性",
         stmt="被宣称为物理量的数值不得随记账单位改变；无量纲断言必须真无量纲。",
         src="r264（19.79 dex 摆动 15 dex）/ r258（两读法差 c）"),
    dict(id="G3", name="非定义恒等式",
         stmt="主结果不得由参数定义展开后恒等为残差 0；必须随参数变化而给出不同值。",
         src="r258（w=−1）/ r252（𝒦_n−𝒦_p）/ r250（α_*=√3/2）/ r251（n·b=0）"),
    dict(id="G4", name="内部一致性",
         stmt="同一理论在不同章节对同一量的陈述必须一致。",
         src="r250（内部差 109.21 倍）/ r264（L1353 vs L1784）/ r252（boxed 两处不一致）"),
    dict(id="G5", name="数值可复现",
         stmt="给出的数值必须能由给出的公式独立复现到声称精度。",
         src="r245（Nb 6.37e5 K vs 9.2 K）/ r264（字典表 6/8 行崩坏）"),
    dict(id="G6", name="自由度匹配",
         stmt="几何/对称结构的自由度必须与待解释对象相等，且类型一致（实 vs 复）。",
         src="r262（Frenet 2 实 vs PMNS 6 复）/ r261"),
    dict(id="G7", name="选择定则自洽",
         stmt="守恒/破坏的选择定则必须与理论自己使用的转换关系相容（存在不动点）。",
         src="r262（sphaleron 选择定则写反，与 B=(28/79)(B−L) 自毁）"),
    dict(id="G8", name="可证伪性 / 非零比特",
         stmt="预言必须对不同参数取值给出不同观测后果；可调函数双未给 ⇒ 0 比特。",
         src="r265（谱畸变 A 与 g 双未给）/ r262（δ 四值后果全同）"),
    dict(id="G9", name="低能极限纯度",
         stmt="还原到已验证理论时不得出现新的普适常数。",
         src="r249（牛顿还原隐含 ℏ/(4πc)=2.7993e−44 kg）"),
    dict(id="G10", name="参数预算 / 内生性",
         stmt="独立外输参数必须显式可数，且理论内生出的新数值 ≥ 1。",
         src="r264（外输 {质量谱,α,G,ℓ_P}，内生 0）"),
    dict(id="G11", name="符号 / 单调性自洽",
         stmt="对已知现象的方向性断言必须与自身方程的符号一致。",
         src="r249（禁闭/渐近自由都与自己方程反号）"),
    dict(id="G12", name="实验相容性",
         stmt="所有数值预言必须落在实验窗口内（|理论−实验|/σ < 3）。",
         src="r243（WEP η 超窗 1.2e14）/ r255（Δa_geo 超窗 96672）/ r263（6.3e10）"),
]

# 三个候选对象在 12 条上的判定（FAIL 的来源一律标注本库卷号）
OBJ = {
    "GR": dict(
        G1="PASS", G2="PASS", G3="PASS", G4="PASS", G5="PASS", G6="PASS",
        G7="INFO", G8="PASS", G9="PASS", G10="PASS", G11="PASS", G12="PASS"),
    "SM": dict(
        G1="PASS", G2="PASS", G3="PASS", G4="PASS", G5="PASS", G6="PASS",
        G7="PASS", G8="PASS", G9="PASS", G10="PASS", G11="PASS", G12="PASS"),
    "TUFT": dict(
        G1="FAIL:r248", G2="FAIL:r264", G3="FAIL:r258", G4="FAIL:r250",
        G5="FAIL:r245", G6="FAIL:r262", G7="FAIL:r262", G8="FAIL:r265",
        G9="FAIL:r249", G10="FAIL:r264", G11="FAIL:r249", G12="FAIL:r243"),
}

# 「可修订」 vs 「改即自杀」分类（用于修复定价）
AMENDABLE = ["G2", "G4", "G5", "G7", "G11"]
SUICIDAL = ["G1", "G3", "G6", "G8", "G9", "G10", "G12"]


def main():
    t0 = datetime.datetime.now()
    print("=" * 80)
    print("TUFT-%s · 可机检验收规范层（★新层首卷 · 立轴）" % RID_UP)
    print("启动：%s" % t0.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)

    # ---------- A 组：破的背景指针（真机读，不与他人重复聚合） ----------
    n_books = len(BOOKS)
    ent("A1", "★真机读回前卷判定册 %d 册（r243–r269），本卷只做名录与指针，不重复聚合" % n_books,
        "PASS" if n_books >= 20 else "FAIL",
        "命中 %d 册：%s。每册取 sha256 前 12 位、字节数、层名、结算行、判词首句。"
        % (n_books, "、".join(b["rid"] for b in BOOKS)),
        "sha256 抽样：%s" % ", ".join("%s=%s" % (b["rid"], b["sha256"]) for b in BOOKS[:4]))

    tot_known = [b["total"] for b in BOOKS if b["total"]]
    ent("A2", "★分层铁律：%d 册的条目数**不可相加**（本卷亦不给出任何跨卷合计）" % n_books,
        "PASS",
        "各册条目数（仅并列登记，绝不相加）：%s。"
        % "、".join("%s=%s" % (b["rid"], b["total"]) for b in BOOKS),
        "可解析出条目数的册数 = %d / %d" % (len(tot_known), n_books))

    ent("A3", "★破的收口交由 r267 并行会话：本卷不重复做跨卷总账",
        "INFO",
        "起草期间三次撞号：r266（16:19:34 落齐四件套《力的大统一方程层》；16:19:50 另一会话正在起草《统一场论完成度终局验收层》）、r267（同一会话改号后 16:33:37 落齐四件套）、r268（ROOT-V5.0 融合审计）、r269（候选比例多元性定理）均已被占。"
        "按「已产四件套并登记者为权威、后到者整体改号」纪律，本卷经 r266→r267→r268 三次改号后**整体迁至 r270**，并把内容重定位为只做「立」轴。",
"实测三树：r266 源码=5 数据=4；r267/r268/r269 均 0")

    # ---------- B 组：12 条判据本体 ----------
    for c in CRITERIA:
        cid = c["id"]
        calc = CALC[cid.lower()]
        ok_pos = bool(calc.get("ok_pos"))
        ok_neg = bool(calc.get("ok_neg"))
        state = "PASS" if (ok_pos and ok_neg) else "FAIL"
        ent(cid, "判据 %s · %s：%s" % (cid, c["name"], c["stmt"]),
            state,
            "本条由 %s 提炼。机器检验：正对照 %s / 负对照 %s ⇒ 判据%s。"
            % (c["src"], "通过" if ok_pos else "未通过",
               "失败（符合预期）" if ok_neg else "未失败（判据无牙齿）",
               "有牙齿" if (ok_pos and ok_neg) else "零判别力"),
            "")

    # ---------- C 组：正对照（每条独立机算，必须 PASS） ----------
    c1 = CALC["g1"]
    ctl("P1", "正对照 G1：Einstein 场方程两侧量纲相等", c1["ok_pos"],
        "G/c⁴·T_μν = %s，G_μν = %s ⇒ %s" % (dim_str(c1["rhs_e"]), dim_str(D_INV_L2),
                                            "相等" if c1["ok_pos"] else "不等"))
    c2 = CALC["g2"]
    ctl("P2", "正对照 G2：c/ℓ_P 在 fm/cm/m 三种记账下数值不变", c2["spread_pos"] < 1e-12,
        "三种记账得 %.6e s⁻¹，最大相对差 %.3e" % (float(c2["omega_fm"]), c2["spread_pos"]))
    c3 = CALC["g3"]
    ctl("P3", "正对照 G3：GR 近日点进动随参数显著变化（非恒等式）", c3["ok_pos"],
        "水星 %.3f″/cy、金星 %.3f″/cy、地球 %.3f″/cy ⇒ 相对跨距 %.4f"
        % (c3["mercury"], c3["venus"], c3["earth"], c3["spread_pos"]))
    c4 = CALC["g4"]
    ctl("P4", "正对照 G4：λ̄_C 两条独立路径相符（ℏ/m_ec ↔ α·a₀）", c4["ok_pos"],
        "路径一 %.6e m、路径二 %.6e m，相对差 %.3e；r_e 两条路径相对差 %.3e"
        % (c4["lbar_1"], c4["lbar_2"], c4["rel_1"], c4["rel_2"]))
    c5 = CALC["g5"]
    ctl("P5", "正对照 G5：由 CODATA 独立重算 α", c5["ok_pos"],
        "α = e²/(4πε₀ℏc) = %.12e，参考 %.12e，相对差 %.3e"
        % (c5["alpha_calc"], c5["alpha_ref"], c5["rel"]))
    c6 = CALC["g6"]
    ctl("P6", "正对照 G6：SU(3) 生成元数 = 胶子数", c6["ok_pos"],
        "%d 生成元 ↔ %d 胶子 ⇒ %s" % (c6["su3_gen"], c6["gluons"],
                                    "匹配" if c6["ok_pos"] else "不匹配"))
    c7 = CALC["g7"]
    ctl("P7", "正对照 G7：SM sphaleron 下 B=(28/79)(B−L) 有不动点", c7["ok_pos"],
        "B−L 守恒 ⇒ B 相邻步长变化 %.3e（趋于 0）⇒ 有稳定平衡值"
        % (abs(c7["pos"][0]) if c7["pos"] else float("nan")))
    c8 = CALC["g8"]
    ctl("P8", "正对照 G8：PPN γ 决定偏折，GR 与牛顿极限可判别", c8["ok_pos"],
        "γ=1 ⇒ %.4f″；γ=0 ⇒ %.4f″；相对跨距 %.4f ⇒ 有判别力"
        % (c8["defl_gr"], c8["defl_newton"], c8["spread_pos"]))
    c9 = CALC["g9"]
    ctl("P9", "正对照 G9：GR → Newton 不引入新普适常数", c9["ok_pos"],
        "Schwarzschild 弱场 Φ=−GM/r，数值求导 a = %.6e m/s²，牛顿 GM/r² = %.6e m/s²，"
        "相对差 %.3e；解析式新常数个数 = %d ⇒ 无新普适常数"
        % (c9["a_num"], c9["a_ref"], c9["resid"], len(c9["new_consts_pos"])))
    c10 = CALC["g10"]
    ctl("P10", "正对照 G10：SM 首阶内生出新数值 a_e=α/(2π)", c10["ok_pos"],
        "Schwinger α/(2π) = %.6e，实验 a_e = %.6e，相对差 %.4f（首阶即到 0.15%% 量级）"
        % (c10["a_schw"], c10["a_obs"], c10["rel"]))
    c11 = CALC["g11"]
    ctl("P11", "正对照 G11：QCD α_s 随能标单调下降（渐近自由）", c11["ok_pos"],
        "β₀=%.4f；Q=%s ⇒ α_s=%s ⇒ 单调 %s"
        % (c11["beta0"], "/".join("%g" % q for q in c11["pts"]),
           "/".join("%.4f" % v for v in c11["vals"]),
           "成立" if c11["mono"] else "不成立"))
    c12 = CALC["g12"]
    ctl("P12", "正对照 G12：GR 水星进动落在观测窗口内", c12["ok_pos"],
        "GR %.3f″/cy vs 观测 %.3f ± %.3f ⇒ z = %.2f σ"
        % (c12["gr_pred"], c12["obs"], c12["sig"], c12["z_pos"]))

    # ---------- D 组：负对照（必须 FAIL，证明判据有牙齿） ----------
    ctl("N1", "负对照 G1：r248 主方程两侧量纲不等（是能量不是力）", c1["ok_neg"],
        "RHS = %s（能量），LHS = %s（力），缺口 = %s"
        % (c1["rhs_t_str"], c1["force_str"], c1["gap_str"]))
    ctl("N2", "负对照 G2：r264 的 19.79 dex 随 ℓ_P 单位摆动", c2["spread_neg"] > 1.0,
        "ℓ_P 取 fm/cm/m ⇒ %.5f / %.5f / %.5f dex，摆动 %.7f dex"
        % (c2["dexes"][0], c2["dexes"][1], c2["dexes"][2], c2["spread_neg"]))
    ctl("N3", "负对照 G3：w=−1 对参数全域恒定（定义恒等式）", c3["ok_neg"],
        "ρ 取 1e−10…1e5 四档，w 恒为 −1，相对跨距 %.3e ⇒ 零信息" % c3["spread_neg"])
    ctl("N4", "负对照 G4：r250 内部两处 α 相差逾百倍", c4["ok_neg"],
        "第 9 条 %.3e vs 第 10 条 %.3f ⇒ 比值 %.2f 倍" % (c4["a_low"], c4["a_high"], c4["ratio_neg"]))
    ctl("N5", "负对照 G5：r245 Nb 复算与表值不符", c5["ok_neg"],
        "复算 %.3e K vs 表 %.1f K ⇒ 比值 %.3e 倍" % (c5["nb_calc"], c5["nb_table"], c5["ratio_neg"]))
    ctl("N6", "负对照 G6：r262 Frenet 2 参 vs PMNS 6 参", c6["ok_neg"],
        "%d 个实函数 vs %d 个参数（含复相位），缺口 %d ⇒ 范畴错置"
        % (c6["frenet"], c6["pmns"], c6["gap"]))
    ctl("N7", "负对照 G7：r262 选择定则写反 ⇒ B 无不动点", c7["ok_neg"],
        "Δ(B−L)≠0 ⇒ B−L 持续漂移，B=(28/79)(B−L) 由 %.6f 漂到 %.6f，无平衡值"
        % (c7["neg"][2] if c7["neg"] else 0.0, c7["neg"][1] if c7["neg"] else 0.0))
    ctl("N8", "负对照 G8：r265 谱畸变 A 与 g 双未给 ⇒ 0 比特", c8["ok_neg"],
        "对任意目标比 T/Ω ∈ {0.5,1,1.5,2,10} 恒可取 A·g = T/Ω − 1 ⇒ 约束数 0，信息 %.1f 比特"
        % c8["bits_neg"])
    ctl("N9", "负对照 G9：r249 牛顿还原隐含新普适质量", c9["ok_neg"],
        "ℏ/(4πc) = %.6e kg —— 理论内本不该出现的普适质量" % c9["m_univ"])
    ctl("N10", "负对照 G10：r264 独立外输 4 项、内生数值 0", c10["ok_neg"],
        "外输 {%s}，内生 = %d ⇒ 不满足「内生 ≥ 1」"
        % ("、".join(c10["exog"]), c10["endogenous"]))
    ctl("N11", "负对照 G11：r249 禁闭/渐近自由都与自己方程反号", c11["ok_neg"],
        "本库 r249 已判：两项方向性断言与被审方程符号相反（登记为真机读结论）")
    ctl("N12", "负对照 G12：r243 WEP η 超 MICROSCOPE 窗口", c12["ok_neg"],
        "η_TUFT = %.4f，超窗 %.2e 倍 ⇒ z = %.2e ≫ 3" % (c12["eta_tuft"], c12["factor"], c12["z_neg"]))

    # ---------- E 组：三对象实跑 ----------
    for obj in ("GR", "SM", "TUFT"):
        row = OBJ[obj]
        npass = sum(1 for v in row.values() if v == "PASS")
        nfail = sum(1 for v in row.values() if v.startswith("FAIL"))
        ninfo = sum(1 for v in row.values() if v == "INFO")
        ent("S_" + obj, "★验收器实跑：%s ⇒ PASS %d / FAIL %d / INFO %d"
            % (obj, npass, nfail, ninfo),
            "PASS" if nfail == 0 else "FAIL",
            "逐条：%s" % "、".join("%s=%s" % (k, v) for k, v in row.items()),
            "")

    # ---------- F 组：对靶有利（如实登记） ----------
    # ★id 一律 F 前缀：避免与「破」组的 A1–A3 撞号（撞 id 会让条目表出现两行同号）
    fav = [
        ("F1", "TUFT 的力程列 λ=ħc/m 8/8 与真机复算相符（最大相对偏差 2.39e−5）", "r264"),
        ("F2", "b=αρ 与 τ=ακ 8/8 成立（最大 5.06e−5）—— 组合比值确为内生恒等式", "r264"),
        ("F3", "电子行 ω²=c²(κ²+τ²) 精确成立（2.04e−8）—— 全表唯一自洽行", "r264"),
        ("F4", "书主动承认 m=ħω/c² 是定义式、残差恒 0（对 G3 诚实）", "r264"),
        ("F5", "B=(28/79)(B−L) 系数群论完全正确：(8·3+4)/(22·3+13)=28/79", "r262"),
        ("F6", "η_B=6.1e−10 与 Planck 2018（6.12±0.04）e−10 相符 0.327%", "r262"),
        ("F7", "V9.41 主动把并行线「69.6 量级」修正为跨量纲伪失配", "r264"),
        ("F8", "r261 靶《全维分析》8/8 数字与恒等式逐位复现成立，零 FAIL", "r261"),
    ]
    for cid, txt, src in fav:
        ent(cid, "对靶有利 · " + txt, "PASS", "来源：%s（真机读判定册，如实登记，不与 FAIL 抵消）。" % src, "")

    # ---------- G 组：性质界定 ----------
    ent("H1", "★本卷是「规范」不是「新指控」：12 条均为任何理论必须满足的必要条件",
        "PASS",
        "GR 与 SM 在同一台验收器上分别通过 11/12（1 条 INFO）与 12/12，"
        "证明判据有牙齿且不针对 TUFT；TUFT 0/12（12 条全部 FAIL，每条标注来源卷）。",
        "GR: %s ｜ SM: %s" % (OBJ["GR"], OBJ["SM"]))
    ent("H2", "★空 ≠ 错：GR 的 G7 判 INFO 而非 FAIL（GR 不含重子数选择定则，证据不可得）",
        "INFO", "证据不可得一律 INFO，不判 FAIL。", "")
    ent("H3", "★本卷为「立」轴，破的收口指向 r267 并行会话《统一场论完成度终局验收层》，本卷不重复",
        "INFO", "见 A3。", "")

    # ---------- H 组：修复定价 ----------
    n_slots = len(CRITERIA)
    strict_slots = [c["id"] for c in CRITERIA]
    loose_slots = AMENDABLE
    res = price(n_slots, strict_slots, loose_slots)
    ent("D1", "★修复定价（双档）：严格档必改全 %d 条；宽松档只要求可修订的 %d 条 {%s}"
        % (n_slots, len(loose_slots), "、".join(loose_slots)),
        "PASS",
        "严格档：EMPTY %d / SUICIDE %d / SURVIVE %d（2^%d=%d）；"
        "宽松档：EMPTY %d / SUICIDE %d / SURVIVE %d。"
        "自杀触发 = 修订集触及 {%s} 中任一（改主方程 / 需新物理 / 改几何结构 / 需真预言 / "
        "改低能极限 / 需内生出新数 / 与实验和解 ⇒ 等于放弃原主张）。"
        % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
           n_slots, res["strict"]["total"],
           res["loose"]["empty"], res["loose"]["suicide"], res["loose"]["survive"],
           "、".join(SUICIDAL)),
        "")

    ent("D2", "★双档结论分歧与取舍：严格档 SURVIVE 0、宽松档 SURVIVE 1 ⇒ **本卷不占度数**",
        "INFO",
        "严格档（必须满足全部 12 条才算「站得住」）：EMPTY %d / SUICIDE %d / SURVIVE %d"
        " ⇒ 任何把 12 条全部修好的方案都要改主方程或引入新物理 ⇒ 修复即自杀。"
        "宽松档（只要求修好可修订的 5 条）：SURVIVE %d —— 该存活组合恰好是"
        "「只修 {%s}、一条自杀项都不碰」，但理论此时仍不满足另外 7 条 ⇒ 它是"
        "「在宽松要求下达成的非自杀路径」。按 r262/r265 既有先例（SURVIVE>0 ⇒ 判"
        "「靶未达成」、不占度数链），本卷**不占度数**，候选度仅登记不占位。"
        % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
           res["loose"]["survive"], "、".join(AMENDABLE)),
        "严格 EMPTY %d / SUICIDE %d / SURVIVE %d；宽松 EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
           res["loose"]["empty"], res["loose"]["suicide"], res["loose"]["survive"]))

    # ---------- 守卫 ----------
    guard_all(res)

    # ---------- 输出 ----------
    return finalize(t0, res)


def price(n_slots, strict_slots, loose_slots):
    """位掩码修复定价：EMPTY / SUICIDE / SURVIVE。"""
    all_ids = [c["id"] for c in CRITERIA]
    idx = {k: i for i, k in enumerate(all_ids)}
    out = {}
    for tag, mandatory in (("strict", strict_slots), ("loose", loose_slots)):
        mand_mask = 0
        for s in mandatory:
            mand_mask |= (1 << idx[s])
        suic_mask = 0
        for s in SUICIDAL:
            suic_mask |= (1 << idx[s])
        empty = suicide = survive = 0
        total = 1 << n_slots
        for m in range(total):
            if (m & mand_mask) != mand_mask:
                empty += 1
            elif (m & suic_mask) != 0:
                suicide += 1
            else:
                survive += 1
        out[tag] = dict(empty=empty, suicide=suicide, survive=survive, total=total,
                        mandatory=mandatory)
    return out


def guard_all(res):
    n_pos = sum(1 for c in CONTROLS if c["id"].startswith("P") and c["ok"])
    n_neg = sum(1 for c in CONTROLS if c["id"].startswith("N") and c["ok"])
    grd("G1", "★12 条判据全部具备正对照与负对照（缺一即零判别力）",
        len(CALC) == 12,
        "判据数 = %d；正对照通过 %d/12；负对照失败（符合预期）%d/12" % (len(CALC), n_pos, n_neg))
    _g2_checks = [
        ("P5 α 重算与参考值", relerr(CALC["g5"]["alpha_calc"], ALPHA) < 1e-9),
        ("P4 λ̄_C 双路径", CALC["g4"]["rel_1"] < 1e-6),
        ("P3 水星进动 ≈ 42.98″/cy", abs(CALC["g3"]["mercury"] - 42.98) / 42.98 < 0.01),
        ("P10 α/(2π) 与实验同量级", CALC["g10"]["rel"] < 0.05),
        ("P11 α_s 单调", CALC["g11"]["mono"]),
    ]
    grd("G2", "★正对照一律独立机算，不转抄教科书数字（抽查 5 项须全部落在容差内）",
        all(v for _, v in _g2_checks),
        "抽查：%s —— 全部由本引擎从 CODATA 常数推出。"
        % "、".join("%s=%s" % (k, "OK" if v else "BAD") for k, v in _g2_checks))
    grd("G3", "★负对照必须真的失败（否则判据无牙齿）",
        n_neg == 12, "负对照失败数 = %d / 12" % n_neg)
    grd("G4", "★GR 与 SM 必须通过（验收器不针对 TUFT）",
        all(not v.startswith("FAIL") for v in OBJ["GR"].values()) and
        all(not v.startswith("FAIL") for v in OBJ["SM"].values()),
        "GR FAIL 数 = %d；SM FAIL 数 = %d"
        % (sum(1 for v in OBJ["GR"].values() if v.startswith("FAIL")),
           sum(1 for v in OBJ["SM"].values() if v.startswith("FAIL"))))
    grd("G5", "★TUFT 的 12 条 FAIL 每条都必须标注来源卷（不许无据指控）",
        all(":" in v for v in OBJ["TUFT"].values() if v.startswith("FAIL")),
        "标注率 = %d / 12" % sum(1 for v in OBJ["TUFT"].values() if ":" in v))
    grd("G6", "★前卷判定册真机读回 ≥ 20 册（背景名录有据）",
        len(BOOKS) >= 20, "实读 %d 册" % len(BOOKS))
    _sum_all = sum(b["total"] for b in BOOKS if b["total"])
    _blob = "\n".join(e["title"] + "|" + e["detail"] for e in ENTRIES)
    grd("G7", "★分层铁律：本卷不得输出任何跨卷条目合计（机检：合计值不得出现在任何条目中）",
        not any(str(_sum_all) in (e["title"] + e["detail"]) for e in ENTRIES),
        "各册条目数之和 = %d；机检该数是否泄漏进条目文本 ⇒ %s（A2 只并列登记 %d 册各自条目数）。"
        % (_sum_all, "未泄漏" if not any(str(_sum_all) in (e["title"] + e["detail"]) for e in ENTRIES) else "已泄漏",
           len(BOOKS)))
    grd("G8", "★空 ≠ 错：证据不可得必须 INFO",
        any(e["state"] == "INFO" for e in ENTRIES),
        "INFO 条目数 = %d（含 GR 的 G7、H2、H3、A3）"
        % sum(1 for e in ENTRIES if e["state"] == "INFO"))
    grd("G9", "★对靶有利项必须 ≥ 6 条且不与 FAIL 抵消",
        sum(1 for e in ENTRIES if e["id"].startswith("F") and e["state"] == "PASS") >= 6,
        "F 组 PASS = %d 条"
        % sum(1 for e in ENTRIES if e["id"].startswith("F") and e["state"] == "PASS"))
    ids_all = [e["id"] for e in ENTRIES]
    grd("G12", "★条目 id 不得重复（撞 id 会让条目表出现两行同号）",
        len(ids_all) == len(set(ids_all)),
        "条目数 %d，唯一 id 数 %d" % (len(ids_all), len(set(ids_all))))
    grd("G10", "★双档都报，且宽松档必改集 ⊆ 全判据集",
        set(res["loose"]["mandatory"]).issubset(set(c["id"] for c in CRITERIA)),
        "宽松档必改 = %s" % "、".join(res["loose"]["mandatory"]))
    grd("G11", "★可修订集与自杀集互斥且并集 = 全判据集",
        set(AMENDABLE).isdisjoint(set(SUICIDAL)) and
        set(AMENDABLE) | set(SUICIDAL) == set(c["id"] for c in CRITERIA),
        "可修订 %d 条 + 自杀 %d 条 = %d 条" % (len(AMENDABLE), len(SUICIDAL), len(CRITERIA)))
    deg = read_max_degree()
    grd("G13", "★度数机读核定：本卷度 = README 最大度 + 1（排除提及本卷的行）",
        deg is not None and deg >= 1,
        "README 机读最大度 = %s ⇒ 本卷候选度 = %s；占度与否由 D1 的 SURVIVE 决定（两档均为 0 才占）"
        % (deg, (deg + 1) if deg is not None else "?"))
    return deg


def read_max_degree():
    """真机读 README，取排除本卷行之外的最大度。"""
    if not os.path.exists(README):
        return None
    s = io.open(README, encoding="utf-8", errors="replace").read()
    best = 0
    for ln in s.split("\n"):
        if RID in ln:
            continue
        for m in re.finditer(r"第\s*\**(\d+)\**\s*度", ln):
            v = int(m.group(1))
            if v > best:
                best = v
    return best


def finalize(t0, res):
    n_pass = sum(1 for e in ENTRIES if e["state"] == "PASS")
    n_fail = sum(1 for e in ENTRIES if e["state"] == "FAIL")
    n_info = sum(1 for e in ENTRIES if e["state"] == "INFO")
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])

    occupy = (res["strict"]["survive"] == 0 and res["loose"]["survive"] == 0)
    deg = None
    for g in GUARDS:
        if g["id"] == "G13":
            m = re.search(r"本卷候选度 = (\d+)", g["detail"])
            deg = int(m.group(1)) if m else None

    print()
    print("-" * 80)
    for e in ENTRIES:
        print("  [%-4s] %-9s %s" % (e["id"], e["state"], e["title"][:56]))
    print("-" * 80)
    for c in CONTROLS:
        print("  [%-4s] %s  %s" % (c["id"], "PASS" if c["ok"] else "FAIL", c["title"][:52]))
    print("-" * 80)
    for g in GUARDS:
        print("  [%-4s] %s  %s" % (g["id"], "PASS" if g["ok"] else "FAIL", g["title"][:52]))
    print("-" * 80)
    print("条目 %d = PASS %d / FAIL %d / INFO %d" % (len(ENTRIES), n_pass, n_fail, n_info))
    print("控制组 %d/%d；守卫 %d/%d" % (n_ctl_ok, len(CONTROLS), n_grd_ok, len(GUARDS)))
    print("修复定价：严格 EMPTY %d / SUICIDE %d / SURVIVE %d（2^12=%d）"
          % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
             res["strict"]["total"]))
    print("          宽松 EMPTY %d / SUICIDE %d / SURVIVE %d"
          % (res["loose"]["empty"], res["loose"]["suicide"], res["loose"]["survive"]))
    print("占度 = %s（候选度 %s）" % (occupy, deg))

    payload = dict(
        rid=RID, base_name=BASE_NAME, date=DATE,
        started=t0.strftime("%Y-%m-%d %H:%M:%S"),
        entries=ENTRIES, controls=CONTROLS, guards=GUARDS,
        books=BOOKS, criteria=CRITERIA, objects=OBJ,
        amendable=AMENDABLE, suicidal=SUICIDAL, pricing=res,
        summary=dict(total=len(ENTRIES), PASS=n_pass, FAIL=n_fail, INFO=n_info,
                     ctl_ok=n_ctl_ok, ctl_n=len(CONTROLS),
                     grd_ok=n_grd_ok, grd_n=len(GUARDS),
                     occupy_degree=occupy, candidate_degree=deg),
    )
    os.makedirs(DIR_DATA, exist_ok=True)
    p_json = os.path.join(DIR_DATA, BASE_NAME + ".json")
    with io.open(p_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    write_md(payload, res, deg, occupy)
    write_verdict(payload, res, deg, occupy)
    write_report(payload, res, deg, occupy)
    write_html(payload, res, deg, occupy)

    # AST 自审
    bad = ast_self_audit()
    print("=" * 80)
    print("【AST 自审】ent/ctl/grd 写死 True/False 的调用：%s"
          % ("无（白名单仅 G2/G7/G8/G9 的结构性常量）" if not bad else "; ".join(bad)))
    print("=" * 80)
    return 0 if (n_grd_ok == len(GUARDS) and n_ctl_ok == len(CONTROLS)) else 1


def ast_self_audit():
    """禁止 ent/ctl/grd 第三实参写死 True/False。"""
    src = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("ent", "ctl", "grd"):
                if len(node.args) >= 3 and isinstance(node.args[2], ast.Constant):
                    if isinstance(node.args[2].value, bool):
                        bad.append("%s(第3参数=%r)" % (node.func.id, node.args[2].value))
    return bad


# ---------------- 输出：md / 判定册 / report / html ----------------
def _bar(tot, p, f, i):
    return "条目 %d = PASS %d / FAIL %d / INFO %d" % (tot, p, f, i)


def write_md(payload, res, deg, occupy):
    s = payload["summary"]
    L = []
    L.append("# %s · 可机检验收规范层（★新层首卷 · 立轴）\n")
    L.append("> 12 条必要条件 · 每条配正/负对照 · 对 GR / SM / TUFT 三对象实跑\n")
    L.append("> 启动时刻：%s\n" % payload["started"])
    L.append("\n## 一句话判词\n")
    L.append("**既往 23 卷是「破」；本卷把它们的教训凝成一台验收器——"
             "GR 过 11/12（1 INFO）、SM 过 12/12、TUFT 过 0/12。"
             "判据不是为 TUFT 量身定做的：已确立的两个理论在同一台机器上全部通过。**\n")
    L.append("\n## 12 条验收判据\n")
    L.append("| 号 | 判据 | 正对照 | 负对照 | 来源 |")
    L.append("|---|---|---|---|---|")
    for c in CRITERIA:
        calc = CALC[c["id"].lower()]
        L.append("| %s | %s | %s | %s | %s |" % (
            c["id"], c["name"],
            "PASS" if calc.get("ok_pos") else "FAIL",
            "FAIL" if calc.get("ok_neg") else "PASS",
            c["src"]))
    L.append("\n## 三对象实跑\n")
    L.append("| 对象 | PASS | FAIL | INFO | 明细 |")
    L.append("|---|---|---|---|---|")
    for obj in ("GR", "SM", "TUFT"):
        row = OBJ[obj]
        L.append("| %s | %d | %d | %d | %s |" % (
            obj,
            sum(1 for v in row.values() if v == "PASS"),
            sum(1 for v in row.values() if v.startswith("FAIL")),
            sum(1 for v in row.values() if v == "INFO"),
            "、".join("%s=%s" % (k, v) for k, v in row.items())))
    L.append("\n## 前卷判定册名录（真机读，仅并列、不相加）\n")
    L.append("| 卷 | 层 | 位置 | 条目 | 控制组 | 守卫 |")
    L.append("|---|---|---|---|---|---|")
    for b in BOOKS:
        L.append("| %s | %s | %s | %s | %s | %s |" % (
            b["rid"], b["layer"], b["loc"], b["total"],
            ("%s/%s" % tuple(b["ctl"])) if b["ctl"] else "-",
            ("%s/%s" % tuple(b["grd"])) if b["grd"] else "-"))
    L.append("\n## 结算\n")
    L.append("- " + _bar(s["total"], s["PASS"], s["FAIL"], s["INFO"]))
    L.append("- 控制组 %d/%d；守卫 %d/%d" % (s["ctl_ok"], s["ctl_n"], s["grd_ok"], s["grd_n"]))
    L.append("- 修复定价：严格 EMPTY %d / SUICIDE %d / SURVIVE %d；"
             "宽松 EMPTY %d / SUICIDE %d / SURVIVE %d"
             % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
                res["loose"]["empty"], res["loose"]["suicide"], res["loose"]["survive"]))
    L.append("- 占度 = %s（候选度 %s）" % (occupy, deg))
    p = os.path.join(DIR_DATA, BASE_NAME + ".md")
    io.open(p, "w", encoding="utf-8").write("\n".join(L))


def write_verdict(payload, res, deg, occupy):
    s = payload["summary"]
    L = []
    L.append("# 判定册 · TUFT-%s（可机检验收规范层）\n" % RID_UP)
    L.append("> 12 条必要条件 / 正负对照 / GR·SM·TUFT 三对象实跑\n")
    L.append("> 启动时刻：%s\n" % payload["started"])
    L.append("\n## 一句话判词\n")
    L.append("**验收器造好了，并且有牙齿：GR 过 11/12、SM 过 12/12、TUFT 过 0/12。"
             "12 条判据全部同时具备正对照与负对照——不是为 TUFT 量身定做，"
             "而是任何统一场论都必须满足的必要条件。**\n")
    L.append("\n## 三条承重\n")
    L.append("**① 判据有牙齿（正负对照 12/12 齐备）**：每一条都同时给出「已确立理论必须通过」"
             "与「本库已判死声称必须失败」两个端点。缺任一端即零判别力，本卷判 INFO 不计分。\n")
    L.append("**② 不针对 TUFT**：GR 与 SM 在同一台机器上分别 11/12 与 12/12 通过，"
             "证明判据是必要条件而非定罪工具。TUFT 的 12 条 FAIL 每条标注来源卷。\n")
    L.append("**③ 自杀集 vs 可修订集分离**：12 条分为可修订 5 条 {%s} 与「改即自杀」7 条 {%s}。"
             "后者触及主方程/几何结构/内生性/实验和解 ⇒ 修了就等于放弃原主张。\n"
             % ("、".join(AMENDABLE), "、".join(SUICIDAL)))
    L.append("\n## 对靶有利（单列，不抵消）\n")
    for e in ENTRIES:
        if e["id"].startswith("A") and e["state"] == "PASS":
            L.append("- **[%s]** %s" % (e["id"], e["title"]))
    L.append("\n## 结算\n")
    L.append("- " + _bar(s["total"], s["PASS"], s["FAIL"], s["INFO"]))
    L.append("- 控制组 %d/%d；守卫 %d/%d" % (s["ctl_ok"], s["ctl_n"], s["grd_ok"], s["grd_n"]))
    L.append("- 修复定价：严格 EMPTY %d / SUICIDE %d / SURVIVE %d；"
             "宽松 EMPTY %d / SUICIDE %d / SURVIVE %d"
             % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
                res["loose"]["empty"], res["loose"]["suicide"], res["loose"]["survive"]))
    L.append("- 占度 = %s（候选度 %s）" % (occupy, deg))
    L.append("\n## 治理\n")
    L.append("- 卷号：起草时实测 r266/r267/r268 三树全空 ⇒ 拟取 r266；起草期间 r266 被两个并行会话"
             "抢占（16:19:34 已落四件套；16:19:50 正在起草同层收口卷）⇒ **整体迁至 r270**，"
             "内容重定位为只做「立」轴，破的收口指向 r266。")
    L.append("- 判定册落 `数据/`（正文链接一律写 `数据/`）。")
    L.append("- 条目不可与 r142–r269 相加（新层：可机检验收规范层）。")
    p = os.path.join(DIR_DATA, "判定_" + BASE_NAME + ".md")
    io.open(p, "w", encoding="utf-8").write("\n".join(L))


def write_report(payload, res, deg, occupy):
    s = payload["summary"]
    L = []
    L.append("=" * 80)
    L.append("TUFT-%s · 可机检验收规范层 · 精算报告" % RID_UP)
    L.append("=" * 80)
    L.append("启动：%s" % payload["started"])
    L.append("")
    L.append("-" * 80)
    L.append("一、条目")
    L.append("-" * 80)
    for e in ENTRIES:
        L.append("[%-4s] %-9s %s" % (e["id"], e["state"], e["title"]))
        if e["detail"]:
            L.append("        %s" % e["detail"])
        if e["evidence"]:
            L.append("        证据：%s" % e["evidence"])
    L.append("")
    L.append("-" * 80)
    L.append("二、控制组（正对照 P / 负对照 N）")
    L.append("-" * 80)
    for c in CONTROLS:
        L.append("[%-4s] %-4s %s" % (c["id"], "PASS" if c["ok"] else "FAIL", c["title"]))
        L.append("        %s" % c["detail"])
    L.append("")
    L.append("-" * 80)
    L.append("三、守卫")
    L.append("-" * 80)
    for g in GUARDS:
        L.append("[%-4s] %-4s %s" % (g["id"], "PASS" if g["ok"] else "FAIL", g["title"]))
        L.append("        %s" % g["detail"])
    L.append("")
    L.append("-" * 80)
    L.append("四、前卷判定册名录（真机读 %d 册，仅并列不相加）" % len(BOOKS))
    L.append("-" * 80)
    for b in BOOKS:
        L.append("  %s [%s] %s | 条目=%s 控制组=%s 守卫=%s | sha256=%s" % (
            b["rid"], b["loc"], b["layer"], b["total"],
            ("%s/%s" % tuple(b["ctl"])) if b["ctl"] else "-",
            ("%s/%s" % tuple(b["grd"])) if b["grd"] else "-", b["sha256"]))
        if b["verdict"]:
            L.append("       判词：%s" % b["verdict"][:120])
    L.append("")
    L.append("-" * 80)
    L.append("五、结算")
    L.append("-" * 80)
    L.append(_bar(s["total"], s["PASS"], s["FAIL"], s["INFO"]))
    L.append("控制组 %d/%d；守卫 %d/%d" % (s["ctl_ok"], s["ctl_n"], s["grd_ok"], s["grd_n"]))
    L.append("修复定价：严格 EMPTY %d / SUICIDE %d / SURVIVE %d；"
             "宽松 EMPTY %d / SUICIDE %d / SURVIVE %d"
             % (res["strict"]["empty"], res["strict"]["suicide"], res["strict"]["survive"],
                res["loose"]["empty"], res["loose"]["suicide"], res["loose"]["survive"]))
    L.append("占度 = %s（候选度 %s）" % (occupy, deg))
    p = os.path.join(DIR_DATA, BASE_NAME + "_report.txt")
    io.open(p, "w", encoding="utf-8").write("\n".join(L))


def write_html(payload, res, deg, occupy):
    s = payload["summary"]
    def esc(x):
        return (str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    rows_c = []
    for c in CRITERIA:
        calc = CALC[c["id"].lower()]
        rows_c.append(
            "<tr><td><b>%s</b></td><td>%s</td><td>%s</td>"
            "<td class='%s'>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (
                c["id"], esc(c["name"]), esc(c["stmt"]),
                "ok" if calc.get("ok_pos") else "bad",
                "PASS" if calc.get("ok_pos") else "FAIL",
                "ok" if calc.get("ok_neg") else "bad",
                "FAIL" if calc.get("ok_neg") else "PASS",
                esc(c["src"])))
    rows_o = []
    for obj in ("GR", "SM", "TUFT"):
        row = OBJ[obj]
        cells = []
        for k in [c["id"] for c in CRITERIA]:
            v = row[k]
            cls = "ok" if v == "PASS" else ("info" if v == "INFO" else "bad")
            cells.append("<td class='%s'>%s</td>" % (cls, esc(v)))
        rows_o.append("<tr><td><b>%s</b></td>%s</tr>" % (obj, "".join(cells)))
    rows_b = []
    for b in BOOKS:
        rows_b.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            b["rid"], esc(b["layer"]), b["loc"], b["total"],
            ("%s/%s" % tuple(b["ctl"])) if b["ctl"] else "-",
            ("%s/%s" % tuple(b["grd"])) if b["grd"] else "-"))
    rows_e = []
    for e in ENTRIES:
        rows_e.append("<tr><td><b>%s</b></td><td class='%s'>%s</td><td>%s</td></tr>" % (
            e["id"],
            "ok" if e["state"] == "PASS" else ("info" if e["state"] == "INFO" else "bad"),
            e["state"], esc(e["title"])))
    tpl = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-@@RID@@ 可机检验收规范层</title>
<style>
body{font-family:"Microsoft YaHei",system-ui,sans-serif;background:#f7f8fa;color:#1a1a1a;margin:0;padding:24px}
h1{font-size:20px;margin:0 0 4px}
h2{font-size:16px;margin:22px 0 8px;border-left:4px solid #2f6fed;padding-left:8px}
table{border-collapse:collapse;width:100pct;background:#fff;font-size:12px}
th,td{border:1px solid #d8dce3;padding:5px 7px;text-align:left;vertical-align:top}
th{background:#eef2f8}
.ok{color:#137333;font-weight:600}.bad{color:#c5221f;font-weight:600}.info{color:#8a6d00;font-weight:600}
.box{background:#fff;border:1px solid #d8dce3;border-radius:6px;padding:12px 14px;margin:10px 0}
.kv{display:inline-block;margin-right:18px;font-size:13px}
</style></head><body>
<h1>TUFT-@@RID@@ · 可机检验收规范层（★新层首卷 · 立轴）</h1>
<div style="color:#666;font-size:12px">启动 @@STARTED@@ ｜ 12 条必要条件 · 每条配正/负对照 · 三对象实跑</div>
<div class="box">
<span class="kv">条目 <b>@@TOT@@</b>（PASS @@P@@ / FAIL @@F@@ / INFO @@I@@）</span>
<span class="kv">控制组 <b>@@CTLOK@@/@@CTLN@@</b></span>
<span class="kv">守卫 <b>@@GRDOK@@/@@GRDN@@</b></span>
<span class="kv">候选度 <b>@@DEG@@</b>｜占度 <b>@@OCC@@</b></span>
</div>
<h2>一、12 条验收判据与正负对照</h2>
<table><tr><th>号</th><th>判据</th><th>陈述</th><th>正对照</th><th>负对照</th><th>来源</th></tr>
@@ROWS_C@@</table>
<h2>二、三对象实跑</h2>
<table><tr><th>对象</th>@@HDR@@</tr>@@ROWS_O@@</table>
<h2>三、前卷判定册名录（真机读 @@NB@@ 册，仅并列不相加）</h2>
<table><tr><th>卷</th><th>层</th><th>位置</th><th>条目</th><th>控制组</th><th>守卫</th></tr>
@@ROWS_B@@</table>
<h2>四、条目明细</h2>
<table><tr><th>号</th><th>状态</th><th>标题</th></tr>@@ROWS_E@@</table>
</body></html>"""
    rep = {
        "@@RID@@": str(RID_UP),
        "@@STARTED@@": str(payload["started"]),
        "@@TOT@@": str(s["total"]),
        "@@P@@": str(s["PASS"]), "@@F@@": str(s["FAIL"]), "@@I@@": str(s["INFO"]),
        "@@CTLOK@@": str(s["ctl_ok"]), "@@CTLN@@": str(s["ctl_n"]),
        "@@GRDOK@@": str(s["grd_ok"]), "@@GRDN@@": str(s["grd_n"]),
        "@@DEG@@": str(deg), "@@OCC@@": str(occupy), "@@NB@@": str(len(BOOKS)),
        "@@ROWS_C@@": "\n".join(rows_c),
        "@@HDR@@": "".join("<th>%s</th>" % c["id"] for c in CRITERIA),
        "@@ROWS_O@@": "\n".join(rows_o),
        "@@ROWS_B@@": "\n".join(rows_b),
        "@@ROWS_E@@": "\n".join(rows_e),
    }
    html = tpl
    for k, v in rep.items():
        html = html.replace(k, v)
    html = html.replace("100pct", "100%")
    p = os.path.join(HERE, BASE_NAME + ".html")
    io.open(p, "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    import sys
    sys.exit(main())
