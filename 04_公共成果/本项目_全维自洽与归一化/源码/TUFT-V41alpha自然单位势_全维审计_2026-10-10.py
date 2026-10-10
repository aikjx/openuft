# -*- coding: utf-8 -*-
"""
TUFT V4.1「a-势自然单位版」· 全维审计（r34）

撞号处置：r33 已被并发会话的《V41 全域力统一方程》册占用（A01–H04，审的是**同一份来料**）。
按「后到者改号不覆盖他人」本册取空号 r34，并在 X27 里把那册的自报分布读盘并列，不做条目号映射。

来料（正本已落盘，本册所有文本层计数从该文件现读，不靠转写）：
  数据/TUFT-V41alpha自然单位势_来料全文_2026-10-10.md（7 节 + 前置总声明）
    1  U(r) = a*(kappa^2 - tau^2)，[a] = L，[U] = L^-1
    2  F_uni = -a*grad(kappa^2 - tau^2)；球对称 F = -a*d/dr(kappa^2-tau^2) rhat
    3  四力剖面 kappa ~ M/r（引）/ tau ~ q/r（电）/ tau ~ q*exp(-mu r)/r（弱）/
       tau ~ sigma*r*exp(-r/r0)（强）
    4  声称：删多余 r 因子、量纲绝对闭环、四力全部第一性原理自然导出、无人为拟合

本册的核心追问（不是「量纲齐不齐」——齐；而是「四力还原层是否成立」）：
  Q1 由它自己的剖面实算出的力的幂次，等于它声称的观测幂次吗？
  Q2 只有一个全局符号 a 的势能，能否同时容纳「引力吸引」与「电磁两号」？
  Q3 [a] = L ⇒ a 必须等于多少米？四力给出同一个数吗？该数随 r 变吗？
  Q4 相对同日已审的 V4.1（mc^2 版，r32）「删掉 m」换来了什么、又丢掉了什么？

关键读数（数值一律由面印出，本 docstring 只点名形状、不钉数）：
  X05b 引力与电磁两支：由自家剖面 d/dr(A^2 r^-2) 得 F ~ r^-3，文中却写 r^-2
  X07  符号分支全枚举（a 的符号是唯一全局自由度）⇒ 自然世界的三条符号要求无法同时满足
  X08  平方势对手性符号不可见：tau -> -tau、kappa -> -kappa 逐位同力（正对照另配）
  X09  U 的符号集无试探体 ⇒ F 与受力体无关 ⇒ a = F/m 破等效原理（相对 r32 是退步）
  X11  a 的数值账单：引力支 a = (m/M)*r/2、电磁支 a = r/(8*pi)，两支都随 r 线性
  X16  力在 r = r0 处恰为零 ⇒ 它举作证据的那一点正是它翻号的那一点
  X17  挠率 24 分量在局域 Lorentz 下不可约分解 4+4+16 ⇒ 1/3/8 维生成元全无载体

纯标准库；Python 3.8.8 实测可跑。
"""
from __future__ import division
import io
import os
import re
import sys
import json
import math
import difflib
import hashlib
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DATA_DIR = os.path.join(ROOT, "数据")
SRC_DIR = os.path.join(ROOT, "源码")
TAG = "TUFT-V41alpha自然单位势_全维审计_2026-10-10"
ROUND = "r34"
CORPUS = os.path.join(DATA_DIR, "TUFT-V41alpha自然单位势_来料全文_2026-10-10.md")
R32_SCRIPT = os.path.join(SRC_DIR, "TUFT-V41几何势修复版_全维审计_2026-10-10.py")
R33_SAME_SRC_FACE = os.path.join(DATA_DIR, "TUFT-r33_V41全域力统一方程_全维审计_2026-10-10.md")

ITEMS = []
GUARDS = []
KEY = {}


def add(iid, verdict, title, detail):
    ITEMS.append({"id": iid, "verdict": verdict, "title": title, "detail": detail})


def g(name, ok, msg):
    GUARDS.append({"name": name, "ok": bool(ok), "msg": msg})


def f6(x):
    return "%.6g" % x


# ---------------------------------------------------------------------
# 常数（CODATA 2018 / PDG 2022 / IAU 2015；两路可交叉者在后文交叉）
# ---------------------------------------------------------------------
HBAR = 1.054571817e-34          # J s
C = 299792458.0                 # m/s
HBAR_C = HBAR * C               # J m
GEV_J = 1.602176634e-10         # J
HBAR_C_GEVM = HBAR_C / GEV_J    # GeV m
G_SI = 6.67430e-11              # m^3 kg^-1 s^-2
GM_SUN = 1.32712440018e20       # m^3 s^-2（IAU 2015 名义太阳质量参数）
M_SUN = GM_SUN / G_SI           # kg
M_EARTH = 5.9722e24             # kg
AU_M = 1.495978707e11           # m
E_CHG = 1.602176634e-19         # C
K_E = 8.9875517923e9            # N m^2 C^-2
ALPHA_EM = 7.2973525693e-3      # 精细结构常数
Q2_ELECTRON = 4.0 * math.pi * ALPHA_EM  # Heaviside-Lorentz 自然单位下 e^2
M_W_GEVM = 80.377               # GeV
G_F_GEVM2 = 1.1663787e-5        # GeV^-2
G_PL_GEVM2 = 6.708e-39          # GeV^-2
L_PLANCK = 1.616255e-35         # m


def kg_to_inv_m(m_kg):
    """自然单位：质量 -> L^-1（约化康普顿波数）"""
    return m_kg * C / HBAR


def newton_to_inv_m2(force_n):
    """自然单位：力 -> L^-2（F_SI = hbar*c * F_nat）"""
    return force_n / HBAR_C


G_NAT_M2 = G_SI * HBAR / C ** 3                 # 路 A：G -> L^2
G_NAT_M2_ALT = G_PL_GEVM2 * HBAR_C_GEVM ** 2    # 路 B：经 GeV^-2
MU_W_INV_M = M_W_GEVM / HBAR_C_GEVM             # m_W -> L^-1

# ---------------------------------------------------------------------
# 量纲引擎（自然单位 ħ=c=1：每个量 = L 的幂；分数精确）
# ---------------------------------------------------------------------
NAT = {
    "kappa": Fraction(-1), "tau": Fraction(-1), "nabla": Fraction(-1),
    "r": Fraction(1), "E": Fraction(-1), "U": Fraction(-1),
    "m": Fraction(-1), "M": Fraction(-1), "F": Fraction(-2),
    "G": Fraction(2), "alpha": Fraction(1), "q": Fraction(0),
    "sigma": Fraction(-2), "mu": Fraction(-1),
}


def nd(sym):
    return NAT[sym]


# ---------------------------------------------------------------------
# 0. 来料正本读取（文本层计数的唯一载体）
# ---------------------------------------------------------------------
CORPUS_OK = os.path.isfile(CORPUS)
BODY = u""
CORPUS_BYTES = 0
CR_N = LF_N = CRLF_N = 0
if CORPUS_OK:
    with io.open(CORPUS, "rb") as fh:
        _raw = fh.read()
    CORPUS_BYTES = len(_raw)
    CR_N = _raw.count(b"\r")
    LF_N = _raw.count(b"\n")
    CRLF_N = _raw.count(b"\r\n")
    _txt = _raw.decode("utf-8", "replace")
    _i = _txt.find(u"TUFT V4.1 修正版")
    BODY = _txt[_i:] if _i >= 0 else _txt
    MD5_CORPUS = hashlib.md5(_raw).hexdigest()
else:
    MD5_CORPUS = "NO FILE"

N_SECT = len(re.findall(r"^[\u4e00-\u9fff]\u3001", BODY, re.M))
N_EQLINE = len(re.findall(r"\$\$", BODY))
N_EQBLK = N_EQLINE // 2
N_OKGLYPH = BODY.count(u"\u2705")          # ✅
N_ABS = sum(BODY.count(t) for t in
            [u"无BUG", u"彻底", u"完全", u"绝对", u"唯一", u"终极", u"致命", u"严格"])
N_HEDGE = sum(BODY.count(t) for t in [u"假说", u"需后续", u"需验证", u"不推翻", u"不宣称", u"不做绝对"])


def def_hits(sym):
    """符号 sym 在来料里是否有定义式（等号）或比例式（\\propto）"""
    eq = len(re.findall(re.escape(sym) + r"\s*=", BODY))
    pr = len(re.findall(re.escape(sym) + r"\s*(?:\\;)?\s*\\propto", BODY))
    return eq, pr, BODY.count(sym)


EXT = [u"\\alpha", u"k", u"g_w", u"g_s", u"\\mu", u"\\sigma", u"r_0", u"\\kappa", u"\\tau"]
EXT_LEDGER = [(s,) + def_hits(s) for s in EXT]
N_EXT_UNDEF = sum(1 for s, eq, pr, tot in EXT_LEDGER if eq == 0 and pr == 0)

add("X01", "INFO", u"来料清点：节数／可代入方程块数／判定符数／正本形状（全部从盘现读）",
    u"正本 = %s（%s B，CR %d／LF %d／CRLF %d，md5 %s）。节标题命中 %d 节（另含 1 段前置总声明），"
    u"$$ 块 %d 处（$$ 记号共 %d 个），✅ 判定符 %d 个。文本层全部计数由本册现读，不转抄上一轮。"
    % (os.path.relpath(CORPUS, ROOT).replace("\\", "/"), CORPUS_BYTES, CR_N, LF_N, CRLF_N,
       MD5_CORPUS[:10], N_SECT, N_EQBLK, N_EQLINE, N_OKGLYPH))

# ---------------------------------------------------------------------
# X02 势能闭合的自洽性：反解 [alpha]
# ---------------------------------------------------------------------
ALPHA_FROM_U = nd("U") - 2 * nd("kappa")           # [a] = [U] - [k^2]
ALPHA_FROM_F = nd("F") - nd("nabla") - 2 * nd("kappa")
add("X02", "PASS", u"§二／§五 的量纲核验自身成立：反解 [alpha] = L^+1，两条独立路径同值",
    u"由 [U]=L^-1 与 [kappa^2]=L^-2 反解 => [alpha] = L^%s；由 [F]=L^-2 与 [grad]=L^-1 反解 => "
    u"[alpha] = L^%s。两路同值且与来料所写 [alpha]=L 一致 => 势能量纲闭环这一条来料没写错。"
    % (ALPHA_FROM_U, ALPHA_FROM_F))

# ---------------------------------------------------------------------
# X03 量纲表内部：R 与 kappa 同行同维，但正统 Ricci 标量是 L^-2
# ---------------------------------------------------------------------
DIM_KRETSCH = 2 * nd("G") + 2 * nd("M") - 6 * nd("r")   # [48 G^2 M^2 / r^6]
DIM_SQRT_K = DIM_KRETSCH / 2
DIM_U_IF_R_IS_STD = nd("alpha") + 2 * DIM_SQRT_K
add("X03", "FAIL", u"§一.1 把 R 与 kappa 同行同维（L^-1）：与来料自己的「施瓦西几何」不符（差整一维 L）",
    u"来料唯一具体的曲率出处是 §四.1 的施瓦西天体。机器用施瓦西 Kretschmann 标量 K = 48 G^2 M^2/r^6 "
    u"实算：[K] = L^%s => 曲率幅度的自然量纲 = sqrt 后 L^%s（即 L^-2，与正统 Ricci 标量一致）。"
    u"而来料 §一.1 把 R 列为 L^-1。若读者取正统 R 代进 §二 势能，[U] = L^%s ≠ L^-1（能量），"
    u"闭环破在 L^-2 上 => 闭合只在「kappa := sqrt(曲率标量)」这个非标准记号下成立，而来料用同一行把 R "
    u"并列进来，使口径不可分辨。" % (DIM_KRETSCH, DIM_SQRT_K, DIM_U_IF_R_IS_STD))

# ---------------------------------------------------------------------
# X04 引力剖面 kappa ~ M/r 与自家 [kappa] = L^-1 冲突；需 sqrt(G) 才齐
# ---------------------------------------------------------------------
DIM_M_OVER_R = nd("M") - nd("r")
DIM_SQRTG = nd("G") / 2
DIM_PROFILE_FIX = DIM_SQRTG + nd("M") - nd("r")
add("X04", "FAIL", u"§四.1 剖面 kappa ~ M/r 违反来料自己的量纲表（差 L^-1）；补齐须把 G 放进剖面",
    u"[M/r] = L^%s 而 §一.1 声明 [kappa] = L^-1 => 差 L^-1，不可由改记号吸收。"
    u"唯一零维补齐是取 kappa = sqrt(G)*M/r（[sqrt G] = L^%s，[该剖面] = L^%s ✓）。"
    u"但那样引力耦合 G 住在剖面层，不在 alpha 层 => 与 §二 末句「alpha 统一包含 G」直接互斥（见 X06）。"
    % (DIM_M_OVER_R, DIM_SQRTG, DIM_PROFILE_FIX))

# ---------------------------------------------------------------------
# X05a/X05b 幂次：求导代数对，落成的幂次不对
# ---------------------------------------------------------------------
def force_exp(p):
    """kappa = A r^-p 时 |F| 的 r 幂次（F = -alpha d/dr kappa^2）"""
    return -(2 * p + 1)


EXP_GRAV_WRITTEN = force_exp(1)                  # 剖面 p=1 -> r^-3
EXP_CLAIMED = -2
NEED_P = Fraction((0 - Fraction(-2)) - 1, 2)      # 2p+1=2 => p=1/2


def central_diff(func, x, h):
    return (func(x + h) - func(x - h)) / (2.0 * h)


A_TEST = 1.0
_K2 = lambda r: A_TEST ** 2 * r ** -2
_dK2_an = lambda r: -2.0 * A_TEST ** 2 * r ** -3
_h1, _h2 = 1e-4, 5e-5
_err1 = abs(central_diff(_K2, 1.0, _h1) - _dK2_an(1.0))
_err2 = abs(central_diff(_K2, 1.0, _h2) - _dK2_an(1.0))
_CONV_EXPECT = (_h1 / _h2) ** 2          # 期望由步长比现推（中心差分二阶精度），不硬编 4
_ratio_conv = _err1 / _err2

add("X05a", "PASS", u"§四.1/§四.2 的求导代数本身正确：d/dr(A^2 r^-2) = -2A^2 r^-3（差分对拍）",
    u"解析 -2A^2/r^3 与中心差分在 r=1、A=1 处的绝对残差 = %s（h=1e-4）与 %s（h=1e-5），"
    u"步长减半因子 %s（应 ~4 = O(h^2) 收敛）=> 来料这一步没有算错；错在下一步的等号。"
    % (f6(_err1), f6(_err2), f6(_ratio_conv)))

add("X05b", "FAIL", u"核心缺陷：由自家剖面实算 F ~ r^%s，文中却写 r^%s（引力与电磁两支同一处跳步）"
    % (EXP_GRAV_WRITTEN, EXP_CLAIMED),
    u"主方程 F_r = -alpha*d/dr(kappa^2 - tau^2)。取 kappa = A r^-p => |F_r| = 2*alpha*A^2*p*r^( -(2p+1) )。"
    u"来料 §四.1 写 kappa ~ M/r（p=%s）、§四.2 写 tau ~ q/r（p=%s）=> 必然给 r^%s；"
    u"但两支的结论行都写 r^%s（牛顿／库仑的观测律），幂次差 = %s。"
    u"要得到观测的 r^-2 需要 p = %s（即 kappa ~ r^-1/2），而来料的剖面是 p=1 => 「1/r^2 规律来自曲率梯度衰减」"
    u"（§四.1 修正说明句）在其自身公式内不成立。此即 r32 Z04 的同一幂次诊断在 V4.1(a 版) 的复现。"
    % (1, 1, EXP_GRAV_WRITTEN, EXP_CLAIMED, abs(EXP_GRAV_WRITTEN - EXP_CLAIMED), NEED_P))

# ---------------------------------------------------------------------
# X06 [alpha] = L 与「alpha 包含 G、k、g_w、g_s」的维度冲突（4/4 不匹配）
# ---------------------------------------------------------------------
DIM_DIFF = {
    u"G": nd("G") - nd("alpha"),
    u"k": Fraction(0) - nd("alpha"),
    u"g_w": Fraction(0) - nd("alpha"),
    u"g_s": Fraction(0) - nd("alpha"),
}
add("X06", "FAIL", u"§二 末句「alpha 统一包含 G、k/g_w/g_s」在量纲层不成立：四个目标 4/4 与 [alpha] 不合",
    u"自然单位下 [G] = L^+2（G = M_Pl^-2）、规范耦合无量纲（[k]=[g_w]=[g_s]=L^0），而 §二 反解得 "
    u"[alpha] = L^+1。逐只差量：G 差 L^%s，k／g_w／g_s 各差 L^%s => 「包含」在此不是比喻而是维度命题，"
    u"机器判 0/4 匹配。后果：四力强度差只能由剖面系数（M、q、sigma、mu）携带，即由外部输入携带，"
    u"alpha 只是同一个数（见 X11 的数值账单）。" % (DIM_DIFF[u"G"], DIM_DIFF[u"k"]))

# ---------------------------------------------------------------------
# X07 符号结构：全局自由度只有 sign(alpha) 一维 => 枚举 2 支
# ---------------------------------------------------------------------
REQ = [u"引力吸引(F_r<0)", u"电磁同号排斥(F_r>0)", u"电磁异号吸引(F_r<0)"]


def sign_branch(u_sign):
    """u_sign = +1 对应 U = +alpha(k^2-t^2),alpha>0；返回三条符号要求的满足情况"""
    f_grav = u_sign * 1.0        # F_r(引力支) = +2*alpha*A^2/r^3 的符号（alpha>0 时向外=排斥）
    f_em_like = u_sign * -1.0    # F_r(电磁支) = -2*alpha*B^2/r^3 的符号（alpha>0 时向内=吸引）
    f_em_unlike = u_sign * -1.0  # tau^2 ~ q^2 恒正 => 异号与同号给同一个力（见 X08）
    return [f_grav < 0, f_em_like > 0, f_em_unlike < 0]


BRANCHES = [(u"alpha>0", sign_branch(1.0)), (u"alpha<0", sign_branch(-1.0))]
HITS = [(nm, sum(1 for b in bs if b), len(bs)) for nm, bs in BRANCHES]
MAXHIT = max(h for _, h, _ in HITS)
add("X07", "FAIL", u"符号全枚举：势能对 kappa、tau 只取平方 => 全局符号自由度仅 1 维，2 支皆不满足自然世界",
    u"机器枚举两支：%s。引力支 F_r 符号 = sign(alpha)，电磁支 F_r 符号 = -sign(alpha)（同一 r^-3 幅度），"
    u"所以「引力与电磁同号相反」是被公式定死的：alpha>0 => 引力排斥＋电磁对同号异号一律吸引；"
    u"alpha<0 => 引力吸引＋电磁一律排斥。自然界要求 %s 三条同时成立，两支的最好成绩 = %s/%s => 判 FAIL。"
    u"（注：这是结构判定，与 X05b 的幂次缺陷相互独立：即使幂次修好，符号层仍然 0 命中。）"
    % (u"；".join(u"%s => 命中 %d/%d" % (nm, h, t) for nm, h, t in HITS),
       u"／".join(REQ), MAXHIT, len(REQ)))

# ---------------------------------------------------------------------
# X08 手性宣称被平方抹掉（含正对照：奇次势下符号差必须非零）
# ---------------------------------------------------------------------
GRID = [0.37, 1.0, 2.718, 5.0, 13.0]
_q = 1.0


def f_tau_branch(tau_val, r, odd=False):
    """odd=False：来料的平方势；odd=True：正对照（把手性符号接回来的奇次势）"""
    if odd:
        t2 = (tau_val ** 2) * (1.0 if tau_val > 0 else -1.0)   # tau^2 * sign(tau)
    else:
        t2 = tau_val ** 2
    return 2.0 * t2 * (-1.0) * r ** -3 * -1.0   # F_r = alpha * d/dr(tau^2) 形状，符号由 t2 承载


_maxdiff_even = max(abs(f_tau_branch(_q, r) - f_tau_branch(-_q, r)) for r in GRID)
_maxdiff_odd = max(abs(f_tau_branch(_q, r, True) - f_tau_branch(-_q, r, True)) for r in GRID)
_maxdiff_kappa = max(abs(((_q ** 2) - ((-_q) ** 2))) for _ in [1])
add("X08", "FAIL", u"§四.2「吸引/排斥由挠率拓扑手性符号区分」在 U = alpha(kappa^2 - tau^2) 内无载体",
    u"势能只含 tau^2 => tau -> -tau 是严格对称。机器在 r 的 5 点网格上比对：|F(tau) - F(-tau)| 最大值 = %s"
    u"（κ 同理 = %s）=> 手性在可观察量里被平方完全消掉。正对照（把势改成 tau^2*sign(tau) 这一类手性感光写法）"
    u"同一网格上给出 %s 的非零差 => 零读数来自对象而非针坏。因此「电荷由环绕数定义」「宇称破缺由手征挠率携带」"
    u"两句在此势能下没有任何力学后果：模型对手征与荷的符号是不可分辨的。"
    % (f6(_maxdiff_even), f6(_maxdiff_kappa), f6(_maxdiff_odd)))

# ---------------------------------------------------------------------
# X09 无试探体 => 等效原理破（与 r32 的 mc^2 版并列定价）
# ---------------------------------------------------------------------
A_EFF = 0.5 * (M_EARTH / M_SUN) * AU_M          # 使地球轨道力复现牛顿值的 alpha（见 X11）
_M_sun_nat = kg_to_inv_m(M_SUN)
_G_for_probe = None


def model_force_N(m_probe_kg):
    """模型力（与试探体无关）：F = 2*alpha*G*M^2/r^3，用 alpha 定标到太阳-地球 @1AU"""
    r = AU_M
    a_src = 2.0 * A_EFF * G_NAT_M2 * _M_sun_nat ** 2 / r ** 3   # L^-2
    return a_src * HBAR_C                                        # -> N


PROBE_MASSES = [1e-3, 1.0, 1e3, 1e6]
_ACC = [model_force_N(m) / m for m in PROBE_MASSES]
_SPREAD_THIS = _ACC[0] / _ACC[-1]
_F_N = model_force_N(1.0)
add("X09", "FAIL", u"§二 势能不含受力体属性 => F 与受力体无关 => a = F/m 破弱等效原理（相对 r32 是退步）",
    u"U 的符号集只有 {alpha, kappa, tau}，源量（M、q）住在剖面里，受力体的 m 与 q 无处出现。"
    u"机器把 alpha 定标到「太阳源 + 1AU 处复现牛顿力」（F = %s N），再换四档受力体质量 %s kg： "
    u"加速度 = %s m/s^2，极差 = %s 倍；等效原理要求该极差 = 1。"
    u"跨册并列：同日 r32 审的 V4.1(mc^2 版) 含因子 m，其 a = F/m 与 m 无关（r32 Z10 判 PASS）；"
    u"本变体把 m 删去换来了 [alpha]=L 的自然单位闭环，代价是把 r32 已挣到的等效原理自动成立退回破坏 => "
    u"两版 V4.1 在「删 m / 留 m」上是相反取舍，本册不代选，只登记：留 m 版保等效原理但需外部标度 L0（r32 Z06），"
    u"删 m 版保量纲表但破等效原理（本条）。"
    % (f6(_F_N), u"／".join(f6(m) for m in PROBE_MASSES),
       u"／".join(f6(x) for x in _ACC), f6(_SPREAD_THIS)))

# ---------------------------------------------------------------------
# X10 电荷维：q^2 是单电荷自受力，两体式需要的第二个荷无载体
# ---------------------------------------------------------------------
_Q_IN_MASTER = BODY.count(u"\\kappa^2") + BODY.count(u"\\tau^2")
_M_IN_MASTER = 0
_CONC_GMm = BODY.count(u"GMm")
_CONC_Q1Q2 = BODY.count(u"q_1 q_2")
_add_probe = []
for _s in [u"\\alpha \\,\\nabla", u"\\alpha \\cdot \\partial_r", u"\\alpha \\cdot \\left("]:
    _add_probe.append((_s, BODY.count(_s)))
add("X10", "FAIL", u"§四.2 结论行的 q_1 q_2（与 §四.1 的 GMm）在推导链里没有第二个荷的来源",
    u"剖面 tau ~ q/r 只含 1 个荷 => tau^2 ~ q^2 是同一电荷的自受力；观测库仑力需要 q_1 q_2（两个独立荷）。"
    u"来料正本现读：结论行里「GMm」命中 %d 次、「q_1 q_2」命中 %d 次，而 §三 主方程书写形态 %s => "
    u"两体荷／质信息只出现在结论，不出现在方程 => 那个 ∝ 步骤是替换而非推导（与 X05b 同一处、X09 同根）。"
    % (_CONC_GMm, _CONC_Q1Q2, u"；".join(u"「%s」%d 次" % (s, n) for s, n in _add_probe)))

# ---------------------------------------------------------------------
# X11 alpha 的数值账单（两路交叉 + 随 r 线性）
# ---------------------------------------------------------------------


def alpha_grav_closed(m_test_kg, M_src_kg, r_m):
    """F_model = 2*a*G*M^2/r^3 = G*M*m/r^2 => a = (m/M)*r/2"""
    return (m_test_kg / M_src_kg) * r_m / 2.0


def alpha_grav_brute(m_test_kg, M_src_kg, r_m):
    f_nat = newton_to_inv_m2(G_SI * M_src_kg * m_test_kg / r_m ** 2)
    return f_nat * r_m ** 3 / (2.0 * G_NAT_M2 * kg_to_inv_m(M_src_kg) ** 2)


_AG_CL = alpha_grav_closed(M_EARTH, M_SUN, AU_M)
_AG_BR = alpha_grav_brute(M_EARTH, M_SUN, AU_M)
_AG_DEV = abs(_AG_CL - _AG_BR) / _AG_CL


def alpha_em_closed(r_m):
    """F_model = 2*a*e^2/r^3 = e^2/(4*pi*r^2) => a = r/(8*pi)（q^2 相消）"""
    return r_m / (8.0 * math.pi)


def alpha_em_brute(r_m):
    f_nat = newton_to_inv_m2(K_E * E_CHG ** 2 / r_m ** 2)
    return f_nat * r_m ** 3 / (2.0 * Q2_ELECTRON)


_AE_CL = alpha_em_closed(1.0)
_AE_BR = alpha_em_brute(1.0)
_AE_DEV = abs(_AE_CL - _AE_BR) / _AE_CL
_R_LADDER = [1.0, 1e3, 1e7, AU_M]
_AG_LADDER = [alpha_grav_closed(M_EARTH, M_SUN, r) for r in _R_LADDER]
_AG_SCALE = _AG_LADDER[-1] / _AG_LADDER[0]
_AG_OVER_LP = _AG_CL / L_PLANCK
_RATIO_EM_G_AT_1M = alpha_em_closed(1.0) / alpha_grav_closed(M_EARTH, M_SUN, 1.0)
KEY.update({
    "alpha_grav_1AU_m": f6(_AG_CL), "alpha_grav_route_dev": "%.3e" % _AG_DEV,
    "alpha_em_1m_m": f6(_AE_CL), "alpha_em_route_dev": "%.3e" % _AE_DEV,
    "alpha_over_planck": f6(_AG_OVER_LP), "alpha_r_spread": f6(_AG_SCALE),
    "ratio_em_to_grav_at_1m": f6(_RATIO_EM_G_AT_1M),
})
add("X11", "FAIL", u"§六.3「alpha 分化为四力各自耦合系数，解决强度差异」机器不可满足：alpha 是随 r 线性的长度",
    u"引力支（太阳源、地球受力体）逐位反解：alpha = (m/M)*r/2 = %s m（闭式）vs %s m（按 F*r^3/(2GM^2) 硬乘），"
    u"两路相对偏差 %s。电磁支（两电子 @1 m）：alpha = r/(8*pi) = %s m vs 硬乘 %s m（偏差 %s；注意 q^2 相消 "
    u"=> 该值与电荷无关，只与 r 有关）。三笔账：(a) 同一支要求 alpha 随 r 线性变化——r 从 1 m 到 1 AU 时 "
    u"alpha = %s => 跨 %s 倍，故「常数 alpha」与「1/r^2 律」互斥（根因即 X05b 的 r^-3）；"
    u"(b) 同一 r（1 m）下两支所需 alpha 之比 = %s，且该比值 = (1/4pi)*(M_源/m_试探)，即四力强度差被推回"
    u"给「受力体是谁」而不是耦合常数；(c) 引力支在 1 AU 的 alpha = %s m = 普朗克长的 %s 倍，"
    u"不是 l_P、不是任何康普顿波长、也不是来料 §一.1 里任何几何量 => 「时空几何耦合常数」无几何出处。"
    % (f6(_AG_CL), f6(_AG_BR), "%.3e" % _AG_DEV, f6(_AE_CL), f6(_AE_BR), "%.3e" % _AE_DEV,
       u"／".join(f6(x) for x in _AG_LADDER), f6(_AG_SCALE), f6(_RATIO_EM_G_AT_1M),
       f6(_AG_CL), f6(_AG_OVER_LP)))

# ---------------------------------------------------------------------
# X12/X13 弱力支：求导对，识别错（力程差 2 倍 + 势是汤川的平方）
# ---------------------------------------------------------------------
_tauw = lambda r: math.exp(-MU_W_INV_M * r) / r
_dw_explicit = lambda r: -2.0 * math.exp(-2.0 * MU_W_INV_M * r) * (1.0 + MU_W_INV_M * r) / r ** 3
_h = 1e-6 / MU_W_INV_M
_w_resid = abs(central_diff(lambda x: _tauw(x) ** 2, 1.0 / MU_W_INV_M, _h)
               - _dw_explicit(1.0 / MU_W_INV_M)) / abs(_dw_explicit(1.0 / MU_W_INV_M))
_RANGE_STD = 1.0 / MU_W_INV_M
_RANGE_MODEL = 1.0 / (2.0 * MU_W_INV_M)
_KEY_EXP_RATIO = _RANGE_STD / _RANGE_MODEL
KEY.update({"weak_range_std_m": f6(_RANGE_STD), "weak_range_model_m": f6(_RANGE_MODEL),
            "weak_diff_relative_resid": "%.3e" % _w_resid})
add("X12", "PASS", u"§四.3 弱力剖面的求导代数正确（解析 vs 中心差分，相对残差 %s）" % ("%.3e" % _w_resid),
    u"tau = q e^(-mu r)/r => d/dr tau^2 = -2 q^2 e^(-2 mu r)(1+mu r)/r^3，与来料所写逐位一致；"
    u"机器在 r = 1/mu 处（mu = m_W = %s GeV => %s m^-1）用中心差分对拍，相对残差 %s。"
    % (f6(M_W_GEVM), f6(MU_W_INV_M), "%.3e" % _w_resid))

add("X13", "FAIL", u"但 §四.3「还原弱力／对标电弱」不成立：模型势是汤川势的平方，力程差 %s 倍" % f6(_KEY_EXP_RATIO),
    u"标准弱力来自 U_Y ~ e^(-mu r)/r => F_Y ~ e^(-mu r)(mu/r + 1/r^2)，力程 = 1/mu = %s m。"
    u"来料的 U ~ tau^2 ~ e^(-2 mu r)/r^2 => 力程 = 1/(2 mu) = %s m（指数里多一个 2 是平方势的必然后果，"
    u"不是拟合选择），且前因子是 (1+mu r)/r^3 而非 (mu/r+1/r^2)。两条都不等于它对标的那个律；"
    u"同时 §一.2.3 的「弱＝挠率分量激发模态」要载体，见 X14（EC 挠率的强度差 %s 个数量级）。"
    % (f6(_RANGE_STD), f6(_RANGE_MODEL), "%.3e" % abs(math.log10(G_F_GEVM2 / G_PL_GEVM2))))

# ---------------------------------------------------------------------
# X14 EC 挠率做弱力：强度账
# ---------------------------------------------------------------------
_RATIO_EC_GF = G_PL_GEVM2 / G_F_GEVM2
KEY.update({"ec_over_G_F": f6(_RATIO_EC_GF)})
add("X14", "FAIL", u"§六.2「EC 理论挠率原生关联自旋，V4.1 严格沿用正统关联」⇒ 正统关联给的强度远不够弱力",
    u"最小 Einstein-Cartan 里挠率无传播子（代数方程），其物理后果是四费米子接触作用，强度由牛顿常数承担："
    u"G(普朗克) = %s GeV^-2，实测费米常数 G_F = %s GeV^-2 => 比值 = %s（即差 %.3g 个数量级）。"
    u"所以「沿用正统 EC 关联」与「承载弱相互作用」不能同时成立；本条与 X13 独立（一个是力程／幂次，一个是强度）。"
    % (f6(G_PL_GEVM2), f6(G_F_GEVM2), f6(_RATIO_EC_GF), abs(math.log10(_RATIO_EC_GF))))

# ---------------------------------------------------------------------
# X15/X16 强力支：求导对，两个结论都被自家公式否证
# ---------------------------------------------------------------------
_tau_str = lambda x: x * math.exp(-x)          # x = r/r0，sigma=1
_d_str_an = lambda x: 2.0 * x * math.exp(-2.0 * x) * (1.0 - x)
_x0 = 0.7
_hx = 1e-5
_s_resid = abs(central_diff(lambda t: _tau_str(t) ** 2, _x0, _hx) - _d_str_an(_x0)) / abs(_d_str_an(_x0))
add("X15", "PASS", u"§四.4 强力剖面的求导代数正确（相对残差 %s）" % ("%.3e" % _s_resid),
    u"tau = sigma*r*e^(-r/r0) => d/dr tau^2 = 2 sigma^2 r e^(-2r/r0)(1-r/r0)，与来料一致。"
    u"机器在 r/r0 = %s 处以 r0=1、sigma=1 无量纲对拍，相对残差 %s。（形状比对取无量纲单位，"
    u"不引入未定价的 sigma/r0 数值，避免伪造精度。）" % (f6(_x0), "%.3e" % _s_resid))

_XGRID = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
_FMOD = [2.0 * x * math.exp(-2.0 * x) * (1.0 - x) for x in _XGRID]     # d/dr tau^2 的 x 形状
_Frad = [-v for v in _FMOD]                                            # F_s = -alpha * d/dr tau^2
_F_AT_R0 = abs(_Frad[_XGRID.index(1.0)])
# |F|(x) = 2x(1-x)e^(-2x) 的峰值：解析解 2x^2-4x+1=0 => x* = 1 - 1/sqrt(2)，另以细扫复核
_X_PEAK_ANA = 1.0 - 1.0 / math.sqrt(2.0)
_fine = [(i / 20000.0) for i in range(1, 20000)]
_Fmag = lambda x: 2.0 * x * (1.0 - x) * math.exp(-2.0 * x)
_X_PEAK_SCAN = max(_fine, key=_Fmag)
_FMAX_ABS = _Fmag(_X_PEAK_SCAN)
_PEAK_DEV = abs(_X_PEAK_SCAN - _X_PEAK_ANA)
_FAR_TAIL = abs(_Frad[-1]) / _FMAX_ABS
_U_MODEL = [x * x * math.exp(-2.0 * x) for x in _XGRID]


def _cornell(x):
    return -1.0 / x + x          # 形状比对，a = b = 1（无量纲，只判极限）


KEY.update({"strong_F_at_r0": "%.1f" % _F_AT_R0, "strong_tail_over_peak": f6(_FAR_TAIL),
            "strong_peak_x": f6(_X_PEAK_ANA)})
add("X16", "FAIL", u"§四.4 两个 ✅ 被自家公式否证：r = r0 处力恰为 0，且 r->inf 力归于 0（无禁闭）",
    u"取 alpha*sigma^2/r0 为单位，径向力 F_s(x) = -2x e^(-2x)(1-x)，x = r/r0。机器网格 x = %s："
    u"F_s = %s；|F_s| 峰值 %s 出现在 x = %s（解析根：d|F|/dx = 0 => 2x^2-4x+1 = 0 => x* = 1-1/sqrt(2) = %s，"
    u"步长 5e-5 细扫复核 %s，两路差 %s）=> 峰值点在 r0 的 0.29 处，不在 r0。三笔：(a) 来料写"
    u"「中距离 r ~ r0：力线性增强，还原夸克禁闭」，而 x=1 处 F_s = %s（该点正是符号翻转点，力为零而非最强）；"
    u"(b) x>1 之后 F_s 变正 = 向外 = 排斥，即模型把禁闭区间之外做成「把夸克推开」；(c) x = 10 处 "
    u"|F_s|/峰值 = %s，长程归于 0，而禁闭要求力不衰减（Cornell 的 sigma*r 项给常力，见 r32 Z18 更正）。"
    u"小 r 侧同样不是渐近自由：模型 U ~ x^2 e^(-2x)（谐振子型，U(0)=%s）在 r->0 无 -a/r 库仑项，"
    u"同网格上 U_Cornell（取 a=b=1 无量纲，只判极限形状）= %s（x=0.1 处为 %s，发散到 -inf）。"
    u"「渐近自由」的标准含义是高能标耦合趋零（对数），不是「零距离时力为零」——后者是任何有限势的平凡性质。"
    % (u"／".join(f6(x) for x in _XGRID), u"／".join("%.4f" % v for v in _Frad),
       f6(_FMAX_ABS), f6(_X_PEAK_SCAN), f6(_X_PEAK_ANA), f6(_X_PEAK_SCAN), f6(_PEAK_DEV),
       "%.1f" % _F_AT_R0, f6(_FAR_TAIL), f6(_U_MODEL[0]),
       u"／".join(f6(v) for v in [_cornell(x) for x in _XGRID]), f6(_cornell(0.1))))

# ---------------------------------------------------------------------
# X17 挠率的表示论账：24 -> 4+4+16，无 1/3/8 维载体
# ---------------------------------------------------------------------
D = 4
TORS_COMP = D * (D * (D - 1) // 2)
ANTISYM3 = math.comb(D, 3)
IRREPS = [D, D, TORS_COMP - 2 * D]
SM_GEN = [1, 3, 8]
SM_TOTAL = sum(SM_GEN)
MISSING = [n for n in SM_GEN if n not in IRREPS]
add("X17", "FAIL", u"§四.4「三重全反对称色挠率」与 §一.2.3「规范群＝挠率分量」在 4 维流形上无载体",
    u"T^lam_{mu nu} 关于下反对称 => 分量数 = 4*C(4,2) = %d；全反对称部分维数 = C(4,3) = %d（对偶赝矢量，"
    u"既不是 3 也不是 8）；局域 Lorentz 不可约分解 = 迹矢量 %d + 轴迹 %d + 纯张量 %d（和 = %d ✓）。"
    u"标准模型需要 U(1)/SU(2)/SU(3) 的生成元数 %s（合计 %d），而挠率的可约分块维数集合 = %s => 缺 %s。"
    u"结论：在「唯一基础场 = 4 维挠率流形」这一公理下，色 SU(3) 的 8 维伴随表示没有载体，"
    u"「三重全反对称色挠率」的计数本身就是错（全反对称给 4，不给 3）。"
    u"注：这与 r30 Y21、r32 Z22 同族，但本条由本册独立复算（不引用他册读数）。"
    % (TORS_COMP, ANTISYM3, D, D, TORS_COMP - 2 * D, sum(IRREPS),
       u"／".join(str(n) for n in SM_GEN), SM_TOTAL, u"／".join(str(n) for n in IRREPS),
       u"／".join(str(n) for n in MISSING)))

# ---------------------------------------------------------------------
# X18 删多余 r 因子：与库内已登记的 V4.0 原式逐字比对（读盘，不靠记忆）
# ---------------------------------------------------------------------
R32_LAI = {}
R32_READ = u"未读到"
if os.path.isfile(R32_SCRIPT):
    with io.open(R32_SCRIPT, "r", encoding="utf-8") as fh:
        _t32 = fh.read()
    for _mm in re.finditer(r'"(v40_[a-zA-Z0-9_]+|v41_[a-zA-Z0-9_]+|newton_cond|coulomb|yukawa|cornell)"\s*:\s*"([^"]*)"', _t32):
        R32_LAI[_mm.group(1)] = _mm.group(2)
    R32_READ = u"读到 %d 条转写" % len(R32_LAI)
_V40_FORCE = R32_LAI.get("v40_force", u"")
_R_FACTOR_IN_V40 = u") . r" in _V40_FORCE
_R_FACTOR_IN_V41 = BODY.count(u"\\cdot r ") + BODY.count(u") \\cdot r")
add("X18", "PASS", u"§三.3「彻底删除 V4.0 人为非法添加的 r 因子」属实（跨册逐字核对）",
    u"对照载体 = %s（%s）。其登记的 V4.0 主方程转写为「%s」，含尾部因子「) . r」= %s；"
    u"本册来料主方程书写形态里 r 作为整体乘子的命中 = %d => 该项指控的修复在文本层可核对，成立。"
    % (os.path.basename(R32_SCRIPT), R32_READ, _V40_FORCE if _V40_FORCE else u"（无）",
       u"是" if _R_FACTOR_IN_V40 else u"否（读不到，此句不得引用）", _R_FACTOR_IN_V41))

# ---------------------------------------------------------------------
# X19 自然单位表与 SI 还原
# ---------------------------------------------------------------------
_SI_F = {"hbar": (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)),
         "c": (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)),
         "F_nat": (Fraction(0), Fraction(-2), Fraction(0), Fraction(0))}
_SI_PROD = tuple(_SI_F["hbar"][i] + _SI_F["c"][i] + _SI_F["F_nat"][i] for i in range(4))
_SI_FORCE = (Fraction(1), Fraction(1), Fraction(-2), Fraction(0))
add("X19", "PASS", u"§一.1 表的能量／力／梯度三行正确；§五 末句的 SI 还原在量纲层成立（但欠一个定价）",
    u"自然单位（hbar=c=1）下 [E] = L^-1、[F] = [dE/dr] = L^-2、[grad] = L^-1 三机器判定全过；"
    u"SI 还原：F_SI = hbar*c*F_nat 的量纲乘积 = (M,L,T,Q) = %s，与 [力] = %s 相同 => 「可通过常数换算还原 "
    u"MLT^-2」这句成立。但换算只提供一个普适因子（hbar*c = %s J m），而 §六.3 要四力各自的强度差 => "
    u"普适因子不产生差异，差异仍须另加（见 X11 的比值 %s）。"
    % (u"(%s,%s,%s,%s)" % tuple(str(x) for x in _SI_PROD),
       u"(%s,%s,%s,%s)" % tuple(str(x) for x in _SI_FORCE), f6(HBAR_C), f6(_RATIO_EM_G_AT_1M)))

# ---------------------------------------------------------------------
# X20 语域内部冲突：绝对化词 vs 自限词
# ---------------------------------------------------------------------
add("X20", "MISMATCH", u"标题／§七 的绝对化措辞与 §六.1 的自限定调在同一份文内并存",
    u"来料正本现读：绝对化词族（无BUG／彻底／完全／绝对／唯一／终极／致命／严格）命中 %d 次，"
    u"自限词族（假说／需后续／需验证／不推翻／不宣称／不做绝对）命中 %d 次。"
    u"§六.1 明写「不做绝对终结性断言…需后续数值实验验证」，而标题写「无BUG」、§七 写「无谬误、可精算的正经理论框架」"
    u"且六条成果全用「彻底／完全」。判定：这不是修辞问题而是引用风险——本册 X05b/X07/X09/X11 的读数说明"
    u"「无BUG」不成立，故凡引此文者须按 §六.1 口径而非标题口径引（登记为 MISMATCH，不改写他人正文）。"
    % (N_ABS, N_HEDGE))

# ---------------------------------------------------------------------
# X21 外部输入账：未定义式符号计数（正本现读）
# ---------------------------------------------------------------------
_ledger_lines = []
for s, eq, pr, tot in EXT_LEDGER:
    _ledger_lines.append(u"%s：等号定义 %d 次／比例式 %d 次／提及 %d 次" % (s, eq, pr, tot))
add("X21", "FAIL", u"§「核心修正原则：纯第一性原理推导」与 §七.3「四力规律全部为第一性原理梯度推导」被符号账否证",
    u"来料正本对每个关键量的定义式命中数现读 = %s => 等号与比例式都为 0 的符号 %d 个。"
    u"四个剖面（kappa ~ M/r、tau ~ q/r、tau ~ q e^(-mu r)/r、tau ~ sigma r e^(-r/r0)）在数学上就是把目标势"
    u"取平方根后写入：汤川剖面即汤川势、q/r 剖面即库仑势、M/r 剖面是牛顿律所要求的形状（且要求错了，见 X05b）"
    u"——所以「无拟合」不成立，成立的是「拟合从结论层前移到了前提层」。"
    u"与 r32 Z11（零判别力）、Z19（外部输入账）同族：本册独立复算而不引用他册数值。"
    % (u"；".join(_ledger_lines), N_EXT_UNDEF))

# ---------------------------------------------------------------------
# X22 kappa/tau 分担未定：lambda 族逐位同力（与 r32 Z12 同族，本册复算）
# ---------------------------------------------------------------------
_A_LAM = 1.0
_LAMS = [0.0, 0.25, 0.5, 1.0, 3.0]
_F_LAM = []
for lam in _LAMS:
    k2 = (1.0 + lam) * _A_LAM
    t2 = lam * _A_LAM
    _F_LAM.append(-(-(2.0) * (k2 - t2) * 1.0 * 1.0 ** -3))   # F_r 形状，alpha=1,r=1
_F_SPREAD = max(_F_LAM) - min(_F_LAM)
add("X22", "FAIL", u"§一.2.5「四力差异化来源＝曲率／挠率的对称模态」：分担完全不可观测（lambda 族逐位同力）",
    u"主方程只依赖差 kappa^2 - tau^2。机器取 kappa^2 = (1+lam)*A、tau^2 = lam*A（差恒为 A，两者恒非负、"
    u"物理合法），lam = %s 五点上 r=1 处的力 = %s，散布 = %s => 力对「曲率出多少、挠率出多少」严格不可分辨。"
    u"因此以模态区分四力的说法在力学层零判别力；lam 自身还是未声明外部输入（撞 X21 的账）。"
    % (u"／".join(f6(x) for x in _LAMS), u"／".join("%.6f" % v for v in _F_LAM), f6(_F_SPREAD)))

# ---------------------------------------------------------------------
# X23 §一.2.5 三条差异化通道逐条判决（通道可用性，不重推物理）
# ---------------------------------------------------------------------
_CH = [(u"对称模态", u"X17：挠率不可约分块维数 %s，不含 %s => 无载体" % (u"／".join(str(n) for n in IRREPS), u"／".join(str(n) for n in SM_GEN))),
       (u"能标截断", u"本册复算：若 beta(g)=mu dg/dmu 由同一个几何量驱动，则两耦合之差守恒（见下）=> 不能收敛也不能分化"),
       (u"衰减梯度", u"X05b/X21：剖面即目标势的平方根重写，且幂次与观测不合")]
_b = 1.0
_g0 = {"em": 1.0 / 137.035999084, "w": 1.0 / 29.584, "s": 1.0 / 8.482}
_mu_ratio = 1e18
_diff_at = {}
for _k, _v in _g0.items():
    _diff_at[_k] = _v + _b * math.log(_mu_ratio)
_pairs = [("em-w", _diff_at["em"] - _diff_at["w"], _g0["em"] - _g0["w"]),
          ("em-s", _diff_at["em"] - _diff_at["s"], _g0["em"] - _g0["s"]),
          ("w-s", _diff_at["w"] - _diff_at["s"], _g0["w"] - _g0["s"])]
_MAXDRIFT = max(abs(d1 - d0) for _, d1, d0 in _pairs)
add("X23", "BOUNDARY", u"§一.2.5 三条「四力差异化来源」通道：0/3 可用（逐条判，不代来料补形式）",
    u"%s。第二通道本册独立复算（来料未写 beta 函数，故按其 §一.2.5 的最弱读法检验：设 beta 由同一个几何量"
    u"给出、取常数 b = %s 积分跨 18 个数量级能标）=> 任意两耦合之差在两点间的漂移最大 = %s（机器零）"
    u"=> 若几何对三个耦合是同一个函数，差值守恒，既不能解释差异也不能统一；要它工作就必须给每个耦合不同的"
    u"几何出处，即撞回第一通道（X17 无载体）。第三通道见 X05b。判定 BOUNDARY 而非 FAIL：来料只点名通道、"
    u"未给方程，本册不代其构造。"
    % (u"；".join(u"(%s) %s" % (nm, txt) for nm, txt in _CH), f6(_b), f6(_MAXDRIFT)))

# ---------------------------------------------------------------------
# X24 MHD／Grad 关联：0 条导出链
# ---------------------------------------------------------------------
_N_MHD = BODY.count(u"MHD")
_N_GRAD = BODY.count(u"Grad")
_EQ_WITH_MHD = sum(1 for blk in re.findall(r"\$\$(.+?)\$\$", BODY, re.S) if (u"MHD" in blk or u"Grad" in blk or u"nabla\\times" in blk))
add("X24", "BOUNDARY", u"§六.2「MHD 磁平衡、Grad 猜想体系为宏观挠率统计平均近似」：文中 0 条导出式",
    u"来料正本现读：MHD 命中 %d 次、Grad 命中 %d 次，出现在任何 $$ 方程块内的次数 = %d。"
    u"即该关联只以名词出现，无近似定义、无平均算符、无误差量级；本册按库内既有纪律登记为「无载体的关联句」，"
    u"不判其物理真假（判它需要来料先给出式子）。同族先例：r30 Y33/Y34/Y35（MHD 三式零信息量 + Beltrami 反例）。"
    % (_N_MHD, _N_GRAD, _EQ_WITH_MHD))

# ---------------------------------------------------------------------
# X25 稳定性／鬼：导数阶记账 + 来料未处理
# ---------------------------------------------------------------------
_ORDER_R = 2
_ORDER_R2 = 4
_TOKENS_STAB = [u"鬼", u"稳定", u"幺正", u"Ostrogradsky", u"ghost", u"病态"]
_N_STAB = sum(BODY.count(t) for t in _TOKENS_STAB)
add("X25", "BOUNDARY", u"势能对曲率／挠率取二次型 => 场方程阶数升一截，而来料 0 次触及稳定性判据",
    u"导数阶记账（机器只算阶数，不判稳定性本身）：R 型量含度规的 %d 阶导数，R^2／kappa^2 型量含 %d 阶 => "
    u"由 U ~ alpha*(kappa^2 - tau^2) 出发的度规方程一般到四阶，即 Ostrogradsky 型额外自由度的出现条件；"
    u"来料正本对 %s 六个判据词命中 = %d => 该风险未被登记、未被处理。"
    u"注：本册不给结论（四阶不等于必病态，需来料先写清 kappa 的定义式才能判），只登记缺口。"
    % (_ORDER_R, _ORDER_R2, u"／".join(_TOKENS_STAB), _N_STAB))

# ---------------------------------------------------------------------
# X26 跨册定位：同日 V4.1 第 3 变体（逐字相似度现算）
# ---------------------------------------------------------------------
_MY_EQS = {
    "v41a_U": u"U(r) = alpha ( kappa^2(r) - tau^2(r) )",
    "v41a_F": u"F_uni = -alpha nabla( kappa^2 - tau^2 )",
    "v41a_Fsph": u"F_uni = -alpha d/dr( kappa^2 - tau^2 ) rhat",
}
_SIM_ROWS = []
_sim_vals = []
for _mk, _mv in _MY_EQS.items():
    _best = (u"(无对照)", 0.0)
    for _rk, _rv in R32_LAI.items():
        _s = difflib.SequenceMatcher(None, _mv, _rv).ratio()
        if _s > _best[1]:
            _best = (_rk, _s)
    _SIM_ROWS.append(u"%s -> r32:%s = %.6f" % (_mk, _best[0], _best[1]))
    _sim_vals.append(_best[1])
_MEAN_SIM = sum(_sim_vals) / len(_sim_vals) if _sim_vals else -1.0
KEY.update({"mean_similarity_r32": "%.6f" % _MEAN_SIM})
add("X26", "INFO", u"跨册定位：本册是同日第 3 份 V4.1 变体；与 r32 的 mc^2 版逐字相似度均值 %s" % ("%.6f" % _MEAN_SIM),
    u"同日已存：r32《V4.1 几何势修复版》（K、T 无量纲 + m*c^2 因子）与《V4.1 全维统一场论候选》（作用量式）。"
    u"本册（V4.1 alpha-势自然单位版）的净差三处：删 m（等效原理由成立转破坏，X09）、"
    u"以 [alpha]=L 替换 L0 标度问题（X11：alpha 数值随 r 线性、无几何出处）、"
    u"把「四力还原」写成正文推导而非唯象拟合（X05b：还原层当场不成立）。"
    u"逐字最近邻 = %s（对照源 = r32 脚本 LAI 现读；若读不到本条不得引用）。"
    % (u"；".join(_SIM_ROWS)))

# ---------------------------------------------------------------------
# X27 同源复现核对：并发 r33 册审的是同一份来料（读盘并列，不做号映射）
# ---------------------------------------------------------------------
VERDICT_WORDS = (u"PASS", u"FAIL", u"MISMATCH", u"BOUNDARY", u"INFO")


def parse_face_counts(text):
    u"""从一份审计面的「条目统计」区抽判决分布。

    只认这一族形状：行首 '- '，其后以 ' / ' 分隔的 K=N 对，K 必须整词命中 VERDICT_WORDS。
    抽不到返回 None——不返回空字典，因为「没读到」与「读到 0 条」在引用侧是两件事。
    """
    for _ln in text.split(u"\n"):
        _s = _ln.strip()
        if not _s.startswith(u"- "):
            continue
        _parts = [p.strip() for p in _s[2:].split(u"/")]
        if len(_parts) < 2:
            continue
        _got = {}
        for _p in _parts:
            _mm = re.match(u"^(" + u"|".join(VERDICT_WORDS) + u")=(\\d+)$", _p)
            if not _mm:
                _got = {}
                break
            _got[_mm.group(1)] = int(_mm.group(2))
        if _got:
            return _got
    return None


def face_self_account(text):
    u"""现算一份面的自账：分布之和、guard 总数、行首 `**ID**` 枚数，以及闭合判据。

    闭合 = 行首 ID 枚数 == 分布之和 + guard 总数（本库体例里 guard 行也用 `**G01** [PASS]` 形状，
    所以 ID 计数天然含 guard；不闭合说明「自报的条数」与「明细区真有的行」不是一回事）。
    抽不到任何一项时返回 closed=False，不返回「没问题」。
    """
    cnt = parse_face_counts(text)
    s = sum(cnt.values()) if cnt else -1
    gm = re.search(u"^- 自检 guard: (\\d+) / (\\d+) 通过", text, re.M)
    gt = int(gm.group(2)) if gm else -1
    n = len(re.findall(u"^- \\*\\*([A-Z][0-9]+[a-z]?)\\*\\*", text, re.M))
    return {"dist": cnt, "sum": s, "guard_total": gt, "guard_pair": gm, "id_lines": n,
            "closed": (n == s + gt) and s > 0 and gt > 0}


_SIB_TEXT = u""
_SIB_BYTES = 0
_SIB_MD5 = u""
if os.path.isfile(R33_SAME_SRC_FACE):
    with io.open(R33_SAME_SRC_FACE, "rb") as fh:
        _SIB_RAW = fh.read()
    _SIB_BYTES = len(_SIB_RAW)
    _SIB_MD5 = hashlib.md5(_SIB_RAW).hexdigest()
    _SIB_TEXT = _SIB_RAW.decode("utf-8", "replace")
_SIB_ACCT = face_self_account(_SIB_TEXT)
_SIB_CNT = _SIB_ACCT["dist"]
_SIB_ITEMS = _SIB_ACCT["id_lines"]
_SIB_GUARD = _SIB_ACCT["guard_pair"]
_SIB_HAS_CORPUS = u"来料正本" in _SIB_TEXT
_SIB_SUM = _SIB_ACCT["sum"]
_SIB_GTOT = _SIB_ACCT["guard_total"]
_SIB_CLOSE = _SIB_ACCT["closed"]
_SIB_CORPUS_SENT = (
    u"该册正文中出现「来料正本」字样 => 库内另有正本，本册那句「唯一逐字载体」作废，须并读两份。"
    if _SIB_HAS_CORPUS else
    u"该册正文未出现「来料正本」字样 => 本册的 数据/TUFT-V41alpha自然单位势_来料全文_2026-10-10.md "
    u"是这份 V4.1 α 版来料在库内当前唯一的逐字载体（现读于本册运行时刻，非永久事实）。")
add("X27", "INFO", u"同源复现核对：并发 r33 册审的是同一份来料；两册独立、其面的自账现算闭合",
    u"对照载体 = %s（现读 %d B，md5 %s）。"
    u"该册自报分布 = %s，分布之和 = %d；该册自报 guard = %s；该册行首 `**ID**` 命中 = %d 枚。"
    u"自账闭合判据（本册现算，不引他册散文）：行首 ID 枚数 == 分布之和 + guard 总数 => %s"
    u"（该册把 guard 与条目同印在明细区，故 ID 计数含 guard 行，本条不把它们记作条目）。"
    u"号空间：该册为 A–H 系列，与本册 X 系列不同源，本册不做逐条映射，也不为他的判决背书；"
    u"两册若需并引，引用者须同时点名两份面。"
    u"%s"
    u"若该文件被改号或移走，本条读数作废、须重跑本册重读，不许沿用此处数字。"
    % (os.path.basename(R33_SAME_SRC_FACE), _SIB_BYTES, _SIB_MD5[:12] if _SIB_MD5 else u"（无）",
       (u"／".join(u"%s=%d" % (k, _SIB_CNT[k]) for k in VERDICT_WORDS if k in _SIB_CNT)
        if _SIB_CNT else u"**没抽到**（本条不得引用）"),
       _SIB_SUM,
       (u"%s/%s" % (_SIB_GUARD.group(1), _SIB_GUARD.group(2))) if _SIB_GUARD else u"（没抽到）",
       _SIB_ITEMS,
       u"成立" if _SIB_CLOSE else u"不成立（须人工并读该册）",
       _SIB_CORPUS_SENT))

# ---------------------------------------------------------------------
# X28 总结条目
# ---------------------------------------------------------------------
add("X28", "INFO", u"总裁定：来料对自身 V4.0 的三处指控修复属实（数学层真实进步），四力还原层 4/4 不成立",
    u"修复属实处：删多余 r（X18）、矢量合规（主方程 F = -alpha grad(...) 为矢量等式）、势能量纲闭环（X02）、"
    u"自然单位表三行（X19）、弱与强两支的求导代数（X12/X15）。不成立处：引力（X04/X05b/X07/X09/X10/X11）、"
    u"电磁（X05b/X08/X10/X11）、弱（X13/X14）、强（X16/X17）=> 四力 4/4 的「还原」不成立，"
    u"而 §一.2.5 的三条差异化通道 0/3 可用（X23）。净结论与 r32 一致且本册独立复算："
    u"这是一个把任意有心势写成同一形式的记号层重写，其自洽性与解释力可以同时分别成立；"
    u"本册不否定「几何统一」纲领本身，只否定「V4.1 已无 BUG、四力已自然导出」这一具体主张。")

# =====================================================================
# 自检 GUARDS（含 4 枚变异体：证明数字守卫真能咬）
# ======================================================================
_cnt0 = {}
for _it in ITEMS:
    _cnt0[_it["verdict"]] = _cnt0.get(_it["verdict"], 0) + 1

g("G01 量纲两路反解 alpha 同值", ALPHA_FROM_U == ALPHA_FROM_F == Fraction(1),
  u"两路 = %s／%s，期望 1" % (ALPHA_FROM_U, ALPHA_FROM_F))
g("G02 中心差分正对照（d/dr r^-2 -> -2r^-3，收敛因子 == 步长比的平方）",
  abs(_ratio_conv - _CONV_EXPECT) / _CONV_EXPECT < 0.02,
  u"实测因子 = %s，期望 = %s（由 h=%s/h=%s 现推，非硬编）" % (f6(_ratio_conv), f6(_CONV_EXPECT), f6(_h1), f6(_h2)))
g("G03 引力 alpha 闭式 vs 硬乘 相对偏差 < 1e-12", _AG_DEV < 1e-12,
  u"偏差 = %.3e" % _AG_DEV)
g("G04 电磁 alpha 两路（HL 闭式 1/(8pi) vs SI 硬乘）相对偏差 < 1e-8",
  _AE_DEV < 1e-8,
  u"偏差 = %.3e（该残差的量级 = 所打字面常数 k_e 与 alpha_EM 各自的舍入，非单位口径冲突；"
  u"若口径错则残差会是 O(1) 或 4pi 量级）" % _AE_DEV)
g("G05 G 的两路自然单位化（hbar/c^3 vs G_Pl*(hbar c)^2）相对偏差 < 1e-3",
  abs(G_NAT_M2 - G_NAT_M2_ALT) / G_NAT_M2 < 1e-3,
  u"%s vs %s，偏差 %.3e" % (f6(G_NAT_M2), f6(G_NAT_M2_ALT), abs(G_NAT_M2 - G_NAT_M2_ALT) / G_NAT_M2))
g("G06 手性正对照：奇次势下符号差必须非零（否则 X08 的零是针坏）",
  _maxdiff_even == 0.0 and _maxdiff_odd > 0.0,
  u"平方势差 = %s（期望 0），正对照差 = %s（期望 >0）" % (f6(_maxdiff_even), f6(_maxdiff_odd)))
g("G07 符号分支枚举完备：两支命中数必须不同（否则表没跑）",
  len(BRANCHES) == 2 and HITS[0][1] != HITS[1][1],
  u"命中 = %s" % u"／".join(u"%s:%d" % (nm, h) for nm, h, _t in HITS))
g("G08 强力零点解析：x=1 处 F = 0（|.| < 1e-15）", abs(_F_AT_R0) < 1e-15,
  u"F(x=1) = %s" % ("%.1f" % _F_AT_R0))
g("G08b 强力峰值点两路复核：解析根 vs 细扫（差 < 2 倍扫描步长）",
  _PEAK_DEV < 2 * (1.0 / 20000.0),
  u"解析 %s vs 细扫 %s，差 %s（步长 %s）" % (f6(_X_PEAK_ANA), f6(_X_PEAK_SCAN), f6(_PEAK_DEV), f6(1.0 / 20000.0)))
g("G09 弱力力程比解析恒等：1/mu / (1/(2mu)) == 2",
  abs(_RANGE_STD / _RANGE_MODEL - 2.0) < 1e-12,
  u"比值 = %s" % f6(_RANGE_STD / _RANGE_MODEL))
g("G10 挠率计数恒等：24 == 4+4+16 且 C(4,3) == 4",
  TORS_COMP == 24 and sum(IRREPS) == TORS_COMP and ANTISYM3 == 4,
  u"分量 = %d，分块 = %s，全反对称 = %d" % (TORS_COMP, u"／".join(str(n) for n in IRREPS), ANTISYM3))
_NUMS = sorted(set(int(re.sub(r"[A-Za-z]+$", "", it["id"][1:])) for it in ITEMS))
g("G11 条目 id 唯一且号段 X01..Xnn 连续（子号 a/b 并归主号）",
  len(set(it["id"] for it in ITEMS)) == len(ITEMS) and _NUMS == list(range(1, len(_NUMS) + 1)),
  u"条目 %d 个，主号 %d 枚，号 = %s" % (len(ITEMS), len(_NUMS), u",".join(it["id"] for it in ITEMS)))
g("G12 判决分布之和 == 条目数", sum(_cnt0.values()) == len(ITEMS),
  u"分布之和 = %d，条目数 = %d" % (sum(_cnt0.values()), len(ITEMS)))
g("G12b 来料 $$ 记号成对（方程块计数可辨）", N_EQLINE % 2 == 0 and N_EQLINE > 0,
  u"$$ 记号 = %d（期望偶数且 > 0）" % N_EQLINE)
g("G13 变异体 p=1 -> 1/2：幂次差必须从 1 变 0",
  abs(force_exp(Fraction(1, 2)) - (-2)) == 0 and abs(EXP_GRAV_WRITTEN - EXP_CLAIMED) == 1,
  u"p=1/2 给 r^%s（观测 -2 => 差 0），p=1 给 r^%s（差 %s）" % (force_exp(Fraction(1, 2)), EXP_GRAV_WRITTEN, abs(EXP_GRAV_WRITTEN - EXP_CLAIMED)))
g("G14 变异体 U 整体改号：符号表两支必须给出不同判决（否则 X07 读的是散文不是势）",
  sign_branch(1.0) != sign_branch(-1.0),
  u"alpha>0 => %s；alpha<0 => %s" % (u"／".join(str(b) for b in sign_branch(1.0)),
                                    u"／".join(str(b) for b in sign_branch(-1.0))))
g("G15 来料正本可读（读不到则本册文本层计数无载体）", CORPUS_OK and CORPUS_BYTES > 0,
  u"正本字节 = %d，md5 = %s" % (CORPUS_BYTES, MD5_CORPUS[:12]))
g("G16 跨册对照可读（读不到则 X18/X26 不得被引用）",
  len(R32_LAI) >= 5 and _R_FACTOR_IN_V40,
  u"%s，v40_force 含尾部 r 因子 = %s" % (R32_READ, u"是" if _R_FACTOR_IN_V40 else u"否"))
_SYN_OK = u"# t\n\n- PASS=5 / FAIL=9 / BOUNDARY=3 / INFO=4\n"
_SYN_SHAPE_BAD = u"- PASS=大约 5 条 / FAIL=9 条\n"
_SYN_ONLY_TOTAL = u"- 条目统计\n"
_SYN_FACE = (u"# 数据: SYN\n\n## 条目统计\n\n" + _SYN_OK[5:].strip() + u"\n- 自检 guard: 10 / 10 通过\n\n"
             u"## 条目明细\n\n"
             + u"".join(u"- **A%02d** [PASS] t\n" % i for i in range(1, 22))
             + u"".join(u"- **G%02d** [PASS] t\n" % i for i in range(1, 11)))
_SYN_ACCT = face_self_account(_SYN_FACE)
_SYN_MUTANT = _SYN_FACE.replace(u"- **A21** [PASS] t\n", u"", 1)
_SYN_ACCT_MUT = face_self_account(_SYN_MUTANT)
g("G17 面分布解析器两侧夹具：合法行须抽全 4 桶；形似行与只有标题的行须抽不到（None，不是 0）",
  parse_face_counts(_SYN_OK) == {u"PASS": 5, u"FAIL": 9, u"BOUNDARY": 3, u"INFO": 4}
  and parse_face_counts(_SYN_SHAPE_BAD) is None
  and parse_face_counts(_SYN_ONLY_TOTAL) is None,
  u"正对照 = %s，形似反对照 = %s，无分布反对照 = %s" % (
      parse_face_counts(_SYN_OK), parse_face_counts(_SYN_SHAPE_BAD), parse_face_counts(_SYN_ONLY_TOTAL)))
g("G18 自账闭合判据双侧：整面夹具须判闭合（21+10=31），删一枚明细行须判不闭合（30 vs 31）",
  _SYN_ACCT["closed"] and _SYN_ACCT["sum"] == 21 and _SYN_ACCT["guard_total"] == 10
  and _SYN_ACCT["id_lines"] == 31 and not _SYN_ACCT_MUT["closed"]
  and _SYN_ACCT_MUT["id_lines"] == 30,
  u"夹具 = %s（和 %d／guard %d／ID %d），变异体 = %s（ID %d，分布行未变 => 期望不闭合）" % (
      _SYN_ACCT["closed"], _SYN_ACCT["sum"], _SYN_ACCT["guard_total"], _SYN_ACCT["id_lines"],
      _SYN_ACCT_MUT["closed"], _SYN_ACCT_MUT["id_lines"]))


def tally():
    cnt = {}
    for it in ITEMS:
        cnt[it["verdict"]] = cnt.get(it["verdict"], 0) + 1
    return cnt


def _jsonable(x):
    if isinstance(x, dict):
        return dict((k, _jsonable(v)) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, Fraction):
        return str(x)
    return x


def write_outputs(cnt, guard_pass, n_guard):
    payload = {"tag": TAG, "round": ROUND, "corpus": {
        "path": CORPUS.replace("\\", "/"), "bytes": CORPUS_BYTES,
        "CR": CR_N, "LF": LF_N, "CRLF": CRLF_N, "md5": MD5_CORPUS},
        "verdict_counts": cnt, "guards_passed": guard_pass, "guards_total": n_guard,
        "key_numbers": KEY, "items": ITEMS,
        "constants": {"hbar": HBAR, "c": C, "hbar_c_Jm": HBAR_C, "G_SI": G_SI,
                      "G_nat_m2": G_NAT_M2, "M_sun_kg": M_SUN, "M_earth_kg": M_EARTH,
                      "AU_m": AU_M, "alpha_EM": ALPHA_EM, "m_W_GeV": M_W_GEVM,
                      "G_F_GeV2": G_F_GEVM2, "G_Pl_GeV2": G_PL_GEVM2, "l_P_m": L_PLANCK}}
    jp = os.path.join(DATA_DIR, TAG + ".json")
    with io.open(jp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(_jsonable(payload), ensure_ascii=False, indent=2))

    order = ["PASS", "FAIL", "MISMATCH", "BOUNDARY", "INFO"]
    lines = [u"# 数据: " + TAG, u"", u"## 条目统计", u""]
    lines.append(u"- 条目 %d：" % len(ITEMS) + u" / ".join(k + u"=" + unicode_or_str(cnt.get(k, 0)) for k in order))
    lines.append(u"- 自检 guard: %d / %d 通过" % (guard_pass, n_guard))
    lines.append(u"- 来料正本: %s B（CR %d／LF %d），md5 %s" % (CORPUS_BYTES, CR_N, LF_N, MD5_CORPUS))
    lines.append(u"- 关键读数（本面是判定册唯一可引数值载体）: " +
                 u"；".join(u"%s=%s" % (k, v) for k, v in sorted(KEY.items())))
    lines.append(u"")
    lines.append(u"## 条目明细")
    lines.append(u"")
    for it in ITEMS:
        lines.append(u"- **" + it["id"] + u"** [" + it["verdict"] + u"] " + it["title"])
        lines.append(u"")
        lines.append(u"  " + it["detail"].replace(u"\n", u"\n  "))
        lines.append(u"")
    mp = os.path.join(DATA_DIR, TAG + ".md")
    with io.open(mp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(u"\n".join(lines))

    rep = [u"=" * 68, u"TUFT V4.1 alpha-势自然单位版 · 全维审计 (" + ROUND + u")", u"=" * 68,
           u"counts: " + u" / ".join(k + u"=" + unicode_or_str(cnt.get(k, 0)) for k in order),
           u"guards: %d/%d" % (guard_pass, n_guard), u""]
    for it in ITEMS:
        rep.append(u"[" + it["verdict"] + u"] " + it["id"] + u" " + it["title"])
        rep.append(u"    " + it["detail"])
        rep.append(u"")
    rp = os.path.join(DATA_DIR, TAG + "_report.txt")
    with io.open(rp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(u"\n".join(rep))

    # G15-family：写后回读，尺寸由盘上那张图给（不是字符串长度）
    sizes = []
    for p in (jp, mp, rp):
        with io.open(p, "rb") as fh:
            _b = fh.read()
        sizes.append((os.path.basename(p), len(_b), hashlib.md5(_b).hexdigest()))
    return jp, mp, rp, sizes


def unicode_or_str(x):
    return str(x)


def main():
    cnt = tally()
    guard_pass = sum(1 for gg in GUARDS if gg["ok"])
    paths = write_outputs(cnt, guard_pass, len(GUARDS))
    jp, mp, rp, sizes = paths
    print(u"=" * 68)
    print(u"TUFT V4.1 alpha-势自然单位版 · 全维审计 (%s)" % ROUND)
    print(u"=" * 68)
    order = ["PASS", "FAIL", "MISMATCH", "BOUNDARY", "INFO"]
    print(u"条目 %d：" % len(ITEMS) + u" / ".join(u"%s=%d" % (k, cnt.get(k, 0)) for k in order))
    print(u"自检 %d/%d" % (guard_pass, len(GUARDS)))
    print(u"")
    print(u"关键读数（判定册只许引这些串，且须点名 数据/%s.md）：" % TAG)
    for k in sorted(KEY):
        print(u"  %s = %s" % (k, KEY[k]))
    print(u"")
    print(u"写后回读（尺寸由盘给）：")
    for nm, n, h in sizes:
        print(u"  %s  %d B  md5 %s" % (nm, n, h))
    print(u"")
    print(u"判定明细（前 3 行硬摘要）：")
    for it in ITEMS[:3]:
        print(u"  [%s] %s %s" % (it["verdict"], it["id"], it["title"]))
    if guard_pass != len(GUARDS):
        for gg in GUARDS:
            if not gg["ok"]:
                print(u"GUARD FAIL: " + gg["name"] + u" -- " + gg["msg"])
        sys.exit(1)
    print(u"OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
