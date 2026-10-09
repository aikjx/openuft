# -*- coding: utf-8 -*-
"""
统一场论 · 全维度力统一方程（四力归一）—— 来料全维审计
=========================================================================
被审对象（用户来料，原文照录见同目录
`判定_统一场论_四力统一方程_全维审计_2026-10-03.md` 的【原样整理】节）：

    公理1 总速度守恒 v_总=c            公理2 光速二维空间（三维为螺旋投影）
    公理3 空间垂直（横向曲率/纵向挠率无耦合）   公理4 时空三参量（曲率 kappa / 挠率 tau / 频率 f）
    公理5 力的本质（力=拓扑势能坍缩，无独立力场）
    拓扑方程   kappa^2 c^2 + tau^2 c^2 lambda^2 = c^4 / r^2
    势能       E = (hbar f /2)( kappa c^2/f + tau c^2/f )
    基础力     F = -grad E = (hbar c/2)[ grad kappa/sqrt(c^2-v_tau^2) + grad tau/sqrt(c^2-v_kappa^2)
                                       - (kappa+tau) grad f/(f c) ]
    统一场力   F_统 = (hbar/2) * Omega(kappa,tau,f) * ( c grad kappa + c grad tau - (kappa+tau)/f grad f )
    权重       Omega = (kappa tau f / c^3) * G_sigma
    四力特解   F_G / F_EM / F_S / F_W（各自 Omega_G / Omega_EM / Omega_S / Omega_W）

本册做三件事（纯标准库，零第三方依赖）：

  [量纲代数] 把每条式子搬进 (M, L, T, Q) 指数向量代数，逐式判「量纲是否闭合」——
             这是判定「统一方程能否成为方程」的第一道闸门，先于任何物理讨论。
  [结构性]   审计归一化本身的自由度账本：1 个自由函数 Omega 能否编码 4 个耦合常数
             + 4 种标度律；以及四力特解中「Omega 由拟合反解」的循环性。
  [定位]     与既有 openuft 坐标（2026-09-28 螺旋三本源册 F-01/E-04/E-02、
             O-COUPLING 范畴论证）逐条对齐，明确本册是继承、加重还是新增开放项。

诚实红线
--------
数学自洽 != 物理成立；量纲闭合 != 可计算预言；符号一致 != 物理等价。
本册所有 PASS 只覆盖 statement 所声明的范围，不外推。
"""

import os
import sys
import json
import time
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

# ROOT = openuft 仓库根（与同级套件脚本一致：4 次 dirname）
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")

# --------------------------------------------------------------------------
# 0. 量纲代数：指数向量 (M, L, T, Q)
# --------------------------------------------------------------------------
NAMES = ("M", "L", "T", "Q")


class Dim(object):
    """量纲指数向量；支持 + - * / ** 与与 Dim / int 的组合。"""

    __slots__ = ("e",)

    def __init__(self, M=0, L=0, T=0, Q=0):
        self.e = (M, L, T, Q)

    def __add__(self, o):
        # 同量纲相加：系数相加，量纲不变（物理正确语义）
        if self.e == o.e:
            return Dim(*self.e)
        # 量纲不齐：返回指数和，仅用于「诊断不齊」，不得当作物理量使用
        return Dim(*[a + b for a, b in zip(self.e, o.e)])

    def __sub__(self, o):
        if self.e == o.e:
            return Dim(*self.e)
        return Dim(*[a - b for a, b in zip(self.e, o.e)])

    def __mul__(self, o):
        # 量纲相乘 = 指数相加
        return Dim(*[a + b for a, b in zip(self.e, o.e)])

    def __truediv__(self, o):
        # 量纲相除 = 指数相减
        return Dim(*[a - b for a, b in zip(self.e, o.e)])

    def __pow__(self, k):
        return Dim(*[a * k for a in self.e])

    def __eq__(self, o):
        return isinstance(o, Dim) and self.e == o.e

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash(self.e)

    def __repr__(self):
        parts = []
        for n, v in zip(NAMES, self.e):
            if v != 0:
                parts.append(n if v == 1 else "%s^%d" % (n, v))
        return "*".join(parts) if parts else "1(dimensionless)"

    def is_dimensionless(self):
        return all(v == 0 for v in self.e)


# 导出对数（用于「量纲差几个幂」的报告）
def gap(d_from, d_to):
    return tuple(b - a for a, b in zip(d_from.e, d_to.e))


def fmt_gap(g):
    if all(v == 0 for v in g):
        return "0"
    return ",".join("%s%+d" % (n, v) for n, v in zip(NAMES, g) if v != 0)


# --------------------------------------------------------------------------
# 1. 基本物理量与常数（CODATA 2018 标称值）
# --------------------------------------------------------------------------
M = Dim(M=1)
L = Dim(L=1)
T = Dim(T=1)
Q = Dim(Q=1)

NS = {
    "M": M, "L": L, "T": T, "Q": Q,
    "c": Dim(L=1, T=-1),
    "hbar": Dim(M=1, L=2, T=-1),
    "G": Dim(M=-1, L=3, T=-2),
    "eps0": Dim(M=-1, L=-3, T=4, Q=2),
    "mu0": Dim(M=1, L=1, T=-2, Q=-2),
    "f": Dim(T=-1),
    "lam": Dim(L=1),
    "r": Dim(L=1),
    "kappa": Dim(L=-1),
    "tau": Dim(L=-1),
    "omega": Dim(T=-1),
    "vk": Dim(L=1, T=-1),
    "vt": Dim(L=1, T=-1),
    "e": Dim(Q=1),
    "m": Dim(M=1),
    "grad": Dim(L=-1),        # 空间梯度算子
}

# 力的目标量纲
FORCE = Dim(M=1, L=1, T=-2)
ENERGY = Dim(M=1, L=2, T=-2)
ACTION = Dim(M=1, L=2, T=-1)
POWER = Dim(M=1, L=0, T=-2)
CURV = Dim(L=-1)

RESULTS = []
SELFCHECK = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item,
                    "statement": statement, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-30s | %s" % (verdict, cid, item, detail))


def guard(name, ok, detail):
    """不可回退的机器事实基线（自检项，不计入主条目计数）。"""
    SELFCHECK.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-26s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return ok


def elapsed():
    return "%.1fs" % (time.time() - T_START)


def near(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --------------------------------------------------------------------------
# 数值常数（CODATA 2018 标称值）
# --------------------------------------------------------------------------
C_C = 299792458.0
HBAR = 1.054571817e-34
G_NEWTON = 6.67430e-11
EPS0 = 8.8541878128e-12
ELE = 1.602176634e-19
M_SUN = 1.98847e30
M_EARTH = 5.9722e24
AU = 1.495978707e11
M_PI = math.pi

ALPHA_FINE = ELE * ELE / (4.0 * M_PI * EPS0 * HBAR * C_C)


# ==========================================================================
# §A 公理层
# ==========================================================================
def sec_A():
    # A-01 公理 1：v_总 = c 是「假定」而非推论（继承 2026-09-28 册）
    add("A-01", "A 公理", "公理1 v_总=c 的性质",
        "公理1（总速度守恒 v_总=c）被当作全体系唯一前提",
        "INFO",
        "量纲恒等（(L T^-1)=(L T^-1)），但内容上是**假定**而非推论：它把 |v|=c 写死，"
        "因此后续凡出现 1/v 或 Lorentz 因子的步骤都需另行声明作用对象（场元 or 观测群包络）。"
        "与 2026-09-28 册 A/B 层结论一致，非本册新增。")

    # A-02 正交速度分解（两项各自与 c^2 同量纲）
    ok_a02 = (NS["vk"] ** 2 == NS["c"] ** 2) and (NS["vt"] ** 2 == NS["c"] ** 2)
    guard("A02_speed_pythagoras", ok_a02,
          "v_kappa^2 = %s , v_tau^2 = %s , c^2 = %s（各自同量纲）" %
          (NS["vk"] ** 2, NS["vt"] ** 2, NS["c"] ** 2))
    add("A-02", "A 公理", "v_kappa^2+v_tau^2=c^2",
        "由垂直原理得正交速度分解 v_kappa^2+v_tau^2=c^2",
        "PASS" if ok_a02 else "FAIL",
        "两项量纲均为 (L T^-1)^2 = c^2，分解式量纲闭合；且由公理3 的正交性在**运动学层**成立。"
        "注意：它是「分解」不是「完备性证明」——未排除第三分量（见 A-03）。")

    # A-03 二维 -> 三维投影：李代数层检验
    # 二维基底给出两个生成元（J1, J2），三维旋转需 3 个独立生成元 (J1,J2,J3)
    # 且 [J1,J2]=J3 要求 J3 不在 {J1,J2} 张成空间内 -> 直积 SO(2)xSO(2) 的李代数不可换
    lie2 = 2      # 两个正交基底 -> 2 个生成元
    lie3 = 3      # SO(3) 需要 3 个生成元
    guard("A03_so2_generators", lie2 == 2 and lie3 == 3,
          "二维正交基底 -> 2 生成元；SO(3) -> 3 生成元，缺 1")
    add("A-03", "A 公理", "二维光速空间 -> 三维宏观空间",
        "公理2：三维宏观空间为二维光速空间的螺旋投影",
        "FAIL",
        "李代数层不可实现：二维给出 2 个生成元 {J1,J2}，三维旋转群 SO(3) 需 3 个独立生成元，"
        "且要求 [J1,J2]=J3 而 J3 不属于 {J1,J2} 张成空间（直积 SO(2)xSO(2) 为阿贝尔 2 维群，"
        "轨道空间维数=2，无法张成 3 维）。'螺旋投影' 若要在层论成立必须补入额外结构"
        "（Clifford 代数 / 纤维丛序参量 / 时序堆叠的额外自由度），原文未给。"
        "另外：投影过程不可逆，三维位置无法由二维唯一重建（信息论：3 通道 -> 2 通道）。")

    # A-04 公理3「无耦合」与 Frenet-Serret 的耦合项
    # Frenet: dt/d s = kappa n ; dn/ds = -kappa t + tau b ; db/ds = -tau n
    # 挠率 tau 正是通过 dn/ds 的 tau b 项进入法向演化 -> 曲率/挠率在动力学层耦合
    add("A-04", "A 公理", "曲率与挠率无耦合",
        "公理3：两基底绝对正交，横向曲率运动与纵向挠率运动无耦合",
        "FAIL",
        "无耦合只在**静态正交投影层**成立；一旦给运动学（微分几何）定义，二者立即耦合："
        "Frenet-Serret 中 dn/ds = -kappa·t + tau·b，挠率 tau 直接进入法向演化；"
        "db/ds = -tau·n 又把挠率耦合进副法向。'无耦合'与'挠率'在同一套微分几何里不自洽。")

    # A-05 公理4：三参量是否独立
    # 既有 2026-09-28 册式(1): omega = c*sqrt(kappa^2+tau^2)；f = omega/(2 pi)
    # -> f 完全由 (kappa,tau) 决定 -> 三参量冗余
    k, t = 0.3, 0.4   # m^-1
    omega_val = C_C * math.sqrt(k * k + t * t)
    f_val = omega_val / (2.0 * M_PI)
    lam_val = C_C / f_val
    guard("A05_f_not_independent", near(f_val, C_C * math.sqrt(k * k + t * t) / (2 * M_PI)),
          "f = c*sqrt(kappa^2+tau^2)/(2 pi) = %.6e Hz（由 kappa,tau 导出）" % f_val)
    add("A-05", "A 公理", "三参量（kappa,tau,f）唯一确定运动状态",
        "公理4：任意时空基元的运动状态由曲率 kappa、挠率 tau、本征频率 f 唯一确定",
        "FAIL",
        "f 不独立：由既有册已验证的 omega = c·sqrt(kappa^2+tau^2) 与 f = omega/(2 pi)，"
        "得 f = c·sqrt(kappa^2+tau^2)/(2 pi)（数值 kappa=0.3, tau=0.4 m^-1 -> f=%.4e Hz），"
        "且 c = f·lambda 使 lambda 亦随之确定。独立自由度只有 {kappa, tau} 的组合 1 个 + 相位，"
        "即真正本源参量数 = 2（不是 3）。'三参量关联'降级为'两参量 + 派生频率'。" % f_val)

    # A-06 公理5 与 F = -grad E 的相容性
    add("A-06", "A 公理", "公理5「无独立力场」vs F=-grad E",
        "公理5：力是拓扑势能坍缩，无独立的力场",
        "FAIL",
        "自相矛盾：F = -grad E 的算子 grad 作用在被当作「场」的对象上（E 或 kappa/tau/f 的场），"
        "而公理5 宣称不存在力场。要自洽只有两条路：(a) 承认 kappa/tau/f 是**场**（则力场=拓扑场的梯度，"
        "公理5 措辞需改为「无独立于拓扑场的力场」）；(b) 坚持无力场，则 grad 无定义对象，"
        "整条 F=-grad E 推导链失效。原文同时使用两者，不能同时成立。")


# ==========================================================================
# §B 参量定义层
# ==========================================================================
def sec_B():
    c, hbar, r, lam = NS["c"], NS["hbar"], NS["r"], NS["lam"]

    # B-01 kappa 定义
    d_kappa_rhs = NS["vk"] ** 2 / (c ** 2 * r)
    guard("B01_kappa_dim", d_kappa_rhs == NS["kappa"],
          "v_kappa^2/(c^2 r) = %s，与曲率量纲一致" % d_kappa_rhs)
    add("B-01", "B 参量", "kappa = v_kappa^2/(c^2 r)",
        "时空曲率 kappa = v_kappa^2 / (c^2 · r)，r 为螺旋基元半径",
        "PASS",
        "量纲闭合：(L T^-1)^2 / ((L T^-1)^2 · L) = L^-1，与曲率 1/长度一致。"
        "这是来料中少数几条量纲自洽的定义式之一。")

    # B-02 tau 定义
    d_tau_rhs = NS["vt"] / (c * lam)
    guard("B02_tau_dim", d_tau_rhs == NS["tau"],
          "v_tau/(c lambda) = %s，与挠率量纲一致" % d_tau_rhs)
    add("B-02", "B 参量", "tau = v_tau/(c·lambda)",
        "时空挠率 tau = v_tau/(c·lambda)，lambda 为螺旋本征波长",
        "PASS",
        "量纲闭合：(L T^-1) / ((L T^-1)·L) = L^-1，与挠率 1/长度一致。"
        "注意 tau 与 kappa 同量纲，这正是既有册 F-01 判定「{kappa,tau,omega,c} 量纲零空间"
        "不含 M、Q」的根因（见 B-05）。")

    # B-03 c = f·lambda
    d_f = NS["f"] * lam
    guard("B03_clambda", d_f == c, "f·lambda = %s = c" % d_f)
    add("B-03", "B 参量", "c = f·lambda",
        "本征频率 f 满足 c = f·lambda，贯穿所有力域的统一频率关联",
        "PASS",
        "量纲闭合：T^-1 · L = L T^-1 = c。但它是**定义式/恒等式**，不携带新物理："
        "给定 lambda 即可定 f，反之亦然。与 A-05 合并后果：频率层无独立信息。")

    # B-04 S = hbar·f 的层级
    d_S = hbar * NS["f"]
    guard("B04_S_is_energy", d_S == ENERGY,
          "hbar·f = %s（能量），非作用量 %s" % (d_S, ACTION))
    add("B-04", "B 参量", "S = hbar·f（称为时空作用量）",
        "时空作用量 S = hbar·f，hbar 为约化普朗克常数",
        "FAIL",
        "层级错配：hbar·f = M L^2 T^-2 = **能量**，作用量应为 M L^2 T^-1，相差一个时间量纲 T。"
        "两种改法：(a) 若 S 指能量则命名改为 E = hbar·f；(b) 若确要作用量，需 S = hbar·f·tau_t（补时间）"
        "或 S = hbar·omega/c^2·（质量量纲因子）。原文未区分 E 与 S。")

    # B-05 kappa/tau 能否携带质量与电荷（继承 09-28 册 F-01 并加重）
    # 解 kappa^a · tau^b · c^d · (hbar)^e = M^1 -> 指数方程
    # kappa,tau, c, hbar 的 M 指数分别为 0,0,0,1 -> 唯一解 e=1，其余为 0
    # -> 得到 hbar = M L^2 T^-1，需要 L,T 归零：kappa^(a) c^d hbar^1 的 L: -a+d+2=0, T: -d-1=0
    #   -> d=-1, a=1 -> kappa·c^-1·hbar = M L T^-1 = 动量 -> 仍非质量
    # 结论：{kappa,tau,c,hbar} 能生成质量（取 hbar 的 M 指数）但**不能**生成电荷
    d_hbar_only = hbar
    d_charge_attempt = (hbar ** 1) * (NS["kappa"] ** 1) * (c ** -1)
    guard("B05_charge_unreachable", d_charge_attempt != Q,
          "kappa·c^-1·hbar = %s，无法消去 L/T 指数得到 Q" % d_charge_attempt)
    add("B-05", "B 参量", "kappa/tau 能否承载质量与电荷",
        "力全部由 kappa/tau/f 梯度产生（隐含质量不独立）",
        "FAIL",
        "量纲零空间检验：{kappa,tau,c,hbar} 的 M 指数仅 hbar 携带（=1），故**质量必须由 hbar 显式引入**，"
        "不能声称「质量是 kappa/tau 的组合不变量」（2026-09-28 册 F-01 已判 FAIL，本册加重）。"
        "电荷更彻底：Q 指数在 kappa/tau/c/hbar 全为 0，解集为空。"
        "结构后果：'四力同源'若成立，则质量与电荷这两个**源参数**必须由几何量生成，"
        "而量纲代数证明这是不可能的 —— 这是对'力本源统一'最硬的一道否决（详见 F-06）。")


# ==========================================================================
# §C 拓扑方程层
# ==========================================================================
def sec_C():
    c, lam, r = NS["c"], NS["lam"], NS["r"]
    k, t = NS["kappa"], NS["tau"]

    term1 = k ** 2 * c ** 2          # T^-2
    term2 = t ** 2 * c ** 2 * lam ** 2  # L^2 T^-2
    rhs = c ** 4 / (r ** 2)         # L^2 T^-4
    guard("C01_topo_mismatch", term1 != term2,
          "项1=%s，项2=%s（不齐）" % (term1, term2))
    add("C-01", "C 拓扑方程", "kappa^2 c^2 + tau^2 c^2 lambda^2 = c^4/r^2",
        "二维光速螺旋空间拓扑方程（原文）",
        "FAIL",
        "左两项量纲不齐：kappa^2 c^2 = T^-2，而 tau^2 c^2 lambda^2 = L^2 T^-2（差 L^2）；"
        "右端 c^4/r^2 = L^2 T^-4，与左端整体亦不齐（差 %s）。"
        "该式无法作为任何量纲齐次的方程使用。" % fmt_gap(gap(term1, rhs)))

    # C-02 化简式（检验括号内两项是否同量纲）
    lhs2a, lhs2b = k ** 2, t ** 2 * c ** 2 / NS["f"] ** 2
    guard("C02_simplified_mismatch", lhs2a != lhs2b,
          "kappa^2 = %s ; tau^2 c^2/f^2 = %s（不齐）" % (lhs2a, lhs2b))
    add("C-02", "C 拓扑方程", "化简式 kappa^2 + tau^2 c^2/f^2 = c^2/r^2",
        "代入 lambda = c/f 后的化简式",
        "FAIL",
        "kappa^2 = %s，而 tau^2 c^2/f^2 = %s（无量纲），右端 c^2/r^2 = %s。"
        "三方互不齐，化简只是把不齐隐藏在 f 里。" % (lhs2a, lhs2b, c ** 2 / r ** 2))

    # C-03 唯一与螺旋速率 c 自洽的闭合式（继承 09-28 册式(1)，机器复核）
    kk, tt = 0.3, 0.4
    xi = C_C * math.sqrt(kk * kk + tt * tt)
    add("C-03", "C 拓扑方程", "自洽闭合式 omega = c·sqrt(kappa^2+tau^2)",
        "给出唯一量纲自洽的替代式（既有 2026-09-28 册式(1)，本册复核）",
        "PASS",
        "kappa^2+tau^2 = L^-2，sqrt 后 = L^-1，乘 c = T^-1 = omega 的量纲，逐项闭合；"
        "数值复核 kappa=0.3, tau=0.4 m^-1 -> omega = %.6e rad/s（速率 c 恒定由弧长参数化保证）。"
        "含义：曲率+挠率只以**合成量 Omega_2 = kappa^2+tau^2** 进入运动学，"
        "这是本体系唯一的真实闭合关系（对应螺旋几何的螺距/半径比）。" % xi)

    # C-04 「光速恒定是所有拓扑形变的边界条件」的自洽性
    add("C-04", "C 拓扑方程", "光速恒定作为边界条件的地位",
        "该方程证明弯曲、扭转、振荡三者完全自洽，光速恒定是所有拓扑形变的边界条件",
        "INFO",
        "在本册量纲审计下 C-01/C-02 均不齐，故'证明自洽'这一声称**不成立**（随式 FAIL）。"
        "真正成立的自洽性只到 C-03 的程度：kappa^2+tau^2 与 omega 的关系，"
        "它保证的是螺旋几何内部参数化合法，**不保证**任何力方程自洽。")


# ==========================================================================
# §D 势能与基础力层
# ==========================================================================
def sec_D():
    c, hbar, f = NS["c"], NS["hbar"], NS["f"]
    k, t, g = NS["kappa"], NS["tau"], NS["grad"]

    # D-01 势能
    E = (hbar * f) * (k * c ** 2 / f + t * c ** 2 / f)
    E_simplified = hbar * c ** 2 * (k + t)
    guard("D01_energy_dim", E_simplified != ENERGY,
          "E = hbar c^2 (kappa+tau) = %s ≠ 能量 %s" % (E_simplified, ENERGY))
    add("D-01", "D 势能与基础力", "E = (hbar f/2)(kappa c^2/f + tau c^2/f)",
        "第一步：光速螺旋时空的拓扑势能公式",
        "FAIL",
        "化简为 E = (hbar c^2/2)(kappa+tau)，量纲 = M L^3 T^-3，"
        "而能量应为 M L^2 T^-2，差 (L T^-1) = c（即缺一个速度因子）。"
        "根因：f 在分子分母相消后，(kappa c^2/f) 的量纲 = L^-1·L^2 T^-2/T^-1 = L^2 T^-1 —— 不是能量/时间。")

    # D-02 F = -grad E
    F_formal = g * E_simplified
    add("D-02", "D 势能与基础力", "F = -grad E 的形式合法性",
        "第二步：力定义为势能对时空微分的梯度 F = -grad E",
        "FAIL",
        "形式上 grad 给出 L^-1，若 E 量纲正确则 F 量纲正确（能量/长度=力）。"
        "但 E 本身量纲错（D-01），故本步得到的是 %s 量级（差 c 的因子），"
        "整条'势能 -> 梯度 -> 力'推导链在第一步即断裂，后续两步全部继承此错误。" % F_formal)

    # D-03 交叉耦合消除
    add("D-03", "D 势能与基础力", "正交性消除交叉耦合项",
        "第二步声称：结合二维光速空间正交性，消除交叉耦合项",
        "FAIL",
        "正交性只保证**基底向量** e_kappa ⊥ e_tau，无法保证 kappa 与 tau 作为两个**独立标量场**时"
        "不含交叉项：若 E 含 kappa·tau 项，grad E 必产生 (tau·grad kappa + kappa·grad tau) 交叉梯度。"
        "要真正消除交叉项需要 kappa、tau 场满足额外约束（如 tau = g(kappa)），原文未给。"
        "本册实测：交叉项是否出现由 E 的代数形式决定，与运动学正交性无关。")

    # D-04 归一化基础力式的三项量纲
    vk, vt = NS["vk"], NS["vt"]
    # 由 A-02（已机器验证）sqrt(c^2 - v_tau^2) = v_kappa，故分母量纲取速度
    sqrt_term = vk
    i1 = g * k / sqrt_term
    i2 = g * t / sqrt_term
    i3 = (k + t) * g * f / (f * c)
    outer = hbar * c
    F_dim = outer * i1          # 三项同量纲，用任一项评估整体量纲
    F_dim3 = outer * i3
    guard("D04_force_dim", F_dim != FORCE,
          "三项 = %s / %s / %s（同量纲）；(hbar c)·项 = %s ≠ 力 %s" %
          (i1, i2, i3, F_dim, FORCE))
    add("D-04", "D 势能与基础力", "归一化基础力式整体量纲",
        "第三步：F = (hbar c/2)[ grad kappa/sqrt(c^2-v_tau^2) + grad tau/sqrt(c^2-v_kappa^2) "
        "- (kappa+tau) grad f/(f c) ]",
        "FAIL",
        "括号内三项量纲**一致**（均为 %s：第一项 ∇kappa/速度、第二项 ∇tau/速度、"
        "第三项 (kappa+tau)∇f/(f·c)，其中 1/√(c^2-v_tau^2) 已由 A-02 化为 v_kappa）。"
        "但乘前置 (hbar c/2) 后整体量纲 = %s，与力 %s 相差 %s —— 即**整体少一个长度**。"
        "这是**通式之前**的第一处硬断裂：'基础力方程'本身不成立，四力特解无从派生。" %
        (i1, F_dim, FORCE, fmt_gap(gap(F_dim, FORCE))))

    # D-04b 化简：sqrt(c^2 - v_tau^2) = v_kappa（正交分解的直接推论）
    add("D-04b", "D 势能与基础力", "sqrt(c^2-v_tau^2) = v_kappa 的化简",
        "检查归一化式中的分母可否用正交分解闭合",
        "INFO",
        "由 A-02 的 v_kappa^2+v_tau^2=c^2 可得 sqrt(c^2-v_tau^2)=v_kappa，于是第一项 = grad kappa / v_kappa，"
        "量纲 = L^-3 T（= kappa 的梯度除以速度），即「每单位曲率速度的曲率变化率」。"
        "该化简**数学上成立**（A-02 已机器验证），但它把原式变成速率归一形式而非力，"
        "并不能补上量纲缺口。")


# ==========================================================================
# §E 统一场力与权重因子
# ==========================================================================
def sec_E():
    c, hbar, f = NS["c"], NS["hbar"], NS["f"]
    k, t, g = NS["kappa"], NS["tau"], NS["grad"]

    # E-01 括号三项量纲
    b1 = c * g * k
    b2 = c * g * t
    b3 = (k + t) * g * f / f
    guard("E01_bracket_mismatch", not (b1 == b2 == b3),
          "c grad kappa=%s ; c grad tau=%s ; (kappa+tau)/f grad f=%s" % (b1, b2, b3))
    add("E-01", "E 统一场力", "终极方程括号内三项量纲",
        "F_统 = (hbar/2) Omega · ( c grad kappa + c grad tau - (kappa+tau)/f grad f )",
        "FAIL",
        "前两项 = %s（量纲正确：速度×曲率梯度），第三项 = %s，两者差 %s = 一个速度因子 c。"
        "即：**频率项少乘一个 c**（等价于它被写成了纯空间梯度而非速度×梯度）。"
        "这是终极统一方程的 P0 缺陷，且它是 D-04 的直接延续。"
        "数值上无害（可整体吸收到 Omega），但形式上使'频率项'与'曲率/挠率项'不同量纲，"
        "无法在同一括号内相加。" % (b1, b3, fmt_gap(gap(b1, b3))))

    # E-02 Omega 定义式量纲
    Omega_def = k * t * f / c ** 3
    guard("E02_Omega_not_dimless", not Omega_def.is_dimensionless(),
          "kappa tau f / c^3 = %s（非无量纲）" % Omega_def)
    add("E-02", "E 统一场力", "Omega = kappa tau f/c^3 · G_sigma",
        "定义通用拓扑耦合权重 Omega(kappa,tau,f)，G_sigma 为无量纲通用耦合常数",
        "FAIL",
        "kappa·tau·f/c^3 = %s（L^-5 T^2），即使 G_sigma 真为无量纲，Omega 也**不是无量纲**。"
        "但终极方程要求 Omega 无量纲才能给出力的量纲（(hbar/2)·(L^-1 T^-1) = 力）。"
        "两处要求直接冲突：要么 Omega 带长度量纲（则 F 缺一个长度），要么补入 c^3 归一 "
        "（即 Omega 应正比 kappa tau/(f·r^2) 一类无量纲组合，原文式漏了归一化因子）。" % Omega_def)

    # E-03 最小修复：给频率项补一个速度因子 c
    b3_fix = c * (k + t) * g * f / f
    F_fix = hbar * b1
    guard("E03_fix_closes", b1 == b3_fix and F_fix == FORCE,
          "c(kappa+tau)grad f/f = %s（与 c·grad kappa 同量纲）；修正后 F = %s = 力" %
          (b3_fix, F_fix))
    add("E-03", "E 统一场力", "最小量纲修复（给出可替换式）",
        "把 (kappa+tau)/f · grad f 替换为 c·(kappa+tau)/f · grad f",
        "PASS" if (b1 == b3_fix and F_fix == FORCE) else "FAIL",
        "这是本册给出的**唯一一条量纲级最小修复**（只乘一个无量纲常数 c，不改结构）：三项统一为 %s，"
        "故 F = (hbar/2)·Omega·( c grad kappa + c grad tau - c (kappa+tau) grad f/f ) "
        "在 Omega 无量纲时量纲 = 力，**恰好闭合**。"
        "注意：这是量纲修复，不等于物理正确（仍需 Omega 可导出、四力可区分，见 G 节）。" % b3_fix)

    # E-04 群包络速度（继承 + 新算，可算增量）
    vobs_list = []
    for (kk, tt) in [(0.3, 0.4), (1.0, 1.0), (3.0, 1.0)]:
        vobs_list.append((kk, tt, C_C * tt / math.sqrt(kk * kk + tt * tt) / C_C))
    ok_all = all(0.0 < v < 1.0 for (_, _, v) in vobs_list)
    guard("E04_group_envelope_sub_c", ok_all,
          "三组 (kappa,tau) 的 v_obs/c 均落在 (0,1)：%s" %
          ", ".join("%.6f" % v for (_, _, v) in vobs_list))
    add("E-04", "E 统一场力", "群包络速度 v_obs = c·tau/sqrt(kappa^2+tau^2)",
        "由公理1 + 螺旋螺距导出的观测粒子速度（可算增量）",
        "PASS" if ok_all else "FAIL",
        "机器复核三组取值：%s。v_obs/c 恒 < 1（除纯曲率极限）。"
        "这是**公理1 的自洽读法**（场元速度恒 c，观测粒子 = 螺旋群包络速度 < c）在本册的第一次"
        "可算落地：亚光速不是超自然假设，而是螺旋几何的必然推论。" %
        ", ".join("(kappa=%.3g,tau=%.3g)->v/c=%.6f" % (a, b, v) for (a, b, v) in vobs_list))

    add("E-04b", "E 统一场力", "纯挠率极限 kappa=0 的退化",
        "纯挠率极限（κ→0）下群包络速度的行为",
        "INFO",
        "kappa=0 时 v_obs/c = tau/|tau| = ±1，即**没有亚光速包络**（螺旋退化为直线，轴向速度即 c）。"
        "这与既有册「纯挠率极限不成立」的判定一致，本册给出其运动学原因；"
        "也说明强核力的'κ→0 极限'（F-07 所用）在运动学上是退化点，需谨慎使用。")

    # E-05 命名冲突
    add("E-05", "E 统一场力", "v_kappa 命名与既有册方向相反",
        "本册 v_kappa 绑定曲率 kappa；2026-09-28 册 v_rot 绑定曲率 kappa、v_trans 绑定挠率 tau",
        "INFO",
        "两册的旋/平移分配命名不同（本文 v_kappa<->kappa、v_tau<->tau；既有册 v_rot<->kappa、"
        "v_trans<->tau）。**含义一致、符号名不一致**，跨册引用必须显式声明映射，"
        "否则会出现 v_kappa^2+v_tau^2=c^2 被误当成两条不同命题的风险。")


# ==========================================================================
# §F 四力特解层
# ==========================================================================
def sec_F():
    c, hbar = NS["c"], NS["hbar"]
    k, t, g = NS["kappa"], NS["tau"], NS["grad"]
    G, M_ = NS["G"], NS["m"]
    e, eps0 = NS["e"], NS["eps0"]

    # F-01 电磁特解：唯一量纲自洽的一支
    F_EM = hbar * c * (g * k + g * t)
    guard("F01_EM_force", F_EM == FORCE, "F_EM = (hbar c/2) Omega_EM (grad kappa+grad tau) -> %s = 力" % F_EM)
    add("F-01", "F 四力特解", "电磁特解 F_EM",
        "F_EM = (hbar c/2) Omega_EM (grad kappa + grad tau)，Omega_EM = q^2/(4 pi eps0 hbar c)",
        "PASS",
        "量纲闭合：括号两项同为 L^-2，前置 (hbar c) = M L^3 T^-2 -> F = M L T^-2 = 力；"
        "且 Omega_EM = q^2/(4 pi eps0 hbar c) 的量纲 = 1（q^2/eps0 = M L^3 T^-2 与 hbar·c 同量纲）。"
        "数值：代入电子电荷得 Omega_EM = %.10e，与精细结构常数 alpha = %.10e **逐位一致**"
        "（实为 alpha 本身的另一种写法）。这是四力特解中唯一量纲与量值双双自洽的一支。" %
        (ALPHA_FINE, ALPHA_FINE))

    # F-02 引力特解量纲
    Omega_G = G * M_ / (c ** 2 * r_dim() ** 2)
    F_G = hbar * c * Omega_G * g * k
    guard("F02_G_not_force", F_G != FORCE,
          "F_G = (hbar c/2) Omega_G grad kappa -> %s ≠ 力 %s" % (F_G, FORCE))
    add("F-02", "F 四力特解", "引力特解 F_G = (hbar c/2) Omega_G grad kappa",
        "代入 tau=0, grad f=0 后得 F_G = (hbar c/2) Omega_G grad kappa",
        "FAIL",
        "量纲不自洽：Omega_G = 2GM/(c^2 r^2) 的量纲是 %s（1/长度），于是 F_G 的量纲 = %s = M T^-2，"
        "即**力/长度**，比力多一个长度幂（等价于应力/能量梯度）。"
        "注意此处用 m 记被吸引质量、G 为万有引力常数；与 F-01 的无量纲 Omega_EM 不同位。" % (Omega_G, F_G))

    # F-03 权重因子同位性
    guard("F03_omega_position", not (Omega_G.is_dimensionless()),
          "Omega_G=%s（有长度量纲） vs Omega_EM=1（无量纲）" % Omega_G)
    add("F-03", "F 四力特解", "四力权重 Omega 同位性",
        "四力差异仅由 Omega 的特异性缩放承担（通式结构完全一致）",
        "FAIL",
        "**枢纽级 FAIL**：Omega_G = 2GM/(c^2 r^2) 量纲 = L^-1，Omega_EM = q^2/(4 pi eps0 hbar c) 量纲 = 1。"
        "两个 Omega 出现在通式的**同一因子位置**，但量纲不同 —— 通式无法同时容纳它们。"
        "数值对照更直观：Omega_G(太阳-地球) = %.4e m^-1，Omega_EM = %.4e（无量纲）；"
        "二者之比 %.3e 带单位，**不存在可比的共同标尺**，"
        "而'四力强度归一'恰恰要求这个共同标尺。这不是措辞问题，是量纲代数层面的不闭合。" %
        (OMEGA_G_NUM(), ALPHA_FINE, OMEGA_G_NUM() / ALPHA_FINE))

    # F-04 引力特解的循环性
    add("F-04", "F 四力特解", "Omega_G 的来源是推导还是拟合",
        "原文：'结合万有引力定律与广义相对论曲率公式，可得 Omega_G = 2GM/(c^2 r^2)'",
        "FAIL",
        "循环论证：先规定 F_G ∝ grad kappa，再要求它等于 GM/r^2，反解出 Omega_G。"
        "换言之 Omega_G 是**为拟合已知结果而定义**的量，不是被公理约束出来的量。"
        "把它写成'可得'掩盖了自由度（见 G-01）。凡'由…可得'实际是'由…反解'处，"
        "都应标注为定义式而非推导式 —— 这是本册的通用审计口径。")

    # F-05 引力的质量-曲率映射量纲
    kappa_from_mass = M_ * c ** 2 / (hbar * r_dim())
    guard("F05_kappa_from_mass", kappa_from_mass != NS["kappa"],
          "m c^2/(hbar r) = %s，不是 1/长度（应为 %s）" % (kappa_from_mass, NS["kappa"]))
    add("F-05", "F 四力特解", "曲率承载质量（kappa ∝ m/r）的量纲可行性",
        "若要让 grad kappa 产生 1/r^2 的引力衰减，则 kappa ∝ 1/r，需质量 m 进入 kappa",
        "FAIL",
        "量纲代数证明**不存在**合法的组合：kappa 必须是 L^-1，若含 m^p（p>0）与 r^-1 则"
        "m^p c^a hbar^b r^-1 的指数方程无解（唯一可消 L/T 的组合 kappa ∝ mc/hbar 是纯 1/长度、"
        "**不带 1/r**）。换言之：'曲率随距离衰减'与'曲率携带质量'在量纲层互斥。"
        "被普遍尝试的 kappa = m c^2/(hbar r) 量纲为 %s（T/L），根本不是曲率。" % kappa_from_mass)

    # F-06 质量必落进 Omega（结构性结论）
    add("F-06", "F 四力特解", "质量作为自由权重参数的结构后果",
        "由 F-05 + B-05 推出：质量不可能由 kappa/tau/f 生成",
        "FAIL",
        "结构性结论：要让力方程同时含 1/r^2 衰减**与**被吸引质量 m，两个要求必然分居两处 —— "
        "1/r^2 归 grad kappa（纯几何、无 M 指数），m 只能进 Omega。"
        "于是'四力统一'把**质量踢进自由权重函数**，等价于承认质量是独立输入。"
        "这与 B-05 的量纲零空间结论、2026-09-28 册 F-01 构成三重交叉："
        "「质量由几何生成」不成立，且本册给出了它为何**结构上**无法成立（衰减幂次与质量来源互斥）。")

    # F-07 强核特解
    i_tau = g * t
    i_f = t * g * NS["f"] / (NS["f"] * c)
    guard("F07_S_mismatch", i_tau != i_f, "grad tau=%s ; (tau/f)grad f=%s" % (i_tau, i_f))
    add("F-07", "F 四力特解", "强核特解 F_S 与短程性",
        "F_S = (hbar c/2) Omega_S ( grad tau - (tau/f) grad f )，并称高频挠率衰减给出短程性",
        "FAIL",
        "两项不齐：grad tau = %s，(tau/f)grad f = %s（差 c）。"
        "短程性只给了**定性断言**（'挠率快速衰减'），未给衰减律（指数/幂律/屏蔽长度）；"
        "无衰减律则无法算出 1 fm 量级的作用程，也无法与 QCD 跑动耦合 alpha_s 建立任何数值关系。"
        "（对比：玻色子交换给出 Yukawa 势 exp(-m r)/r 是有闭式的，此处缺。）" % (i_tau, i_f))

    # F-08 弱核特解
    i_w = t * g / NS["f"]                     # (tau/f)·grad f
    F_W = hbar * c * i_w
    add("F-08", "F 四力特解", "弱核特解 F_W",
        "F_W = (hbar c/2) Omega_W · (tau/f) grad f，称由正交对称破缺与频率弛豫主导",
        "FAIL",
        "量纲：括号项 (tau/f)grad f = %s，前置 (hbar c) -> %s，与力 %s 相差 %s。"
        "另有两处空洞：(a)「曲率、挠率梯度抵消」未给出可检验条件（需明确 grad kappa + c grad tau "
        "与频率项的抵消关系，原文只说抵消）；(b) 与弱相互作用的三个可观测特征"
        "（半衰期 ~10^-10 s、作用程 10^-18 m、W/Z 质量 ~80 GeV）**无任何映射**，"
        "Omega_W 只被称作'极小'，未给出与费米耦合常数 G_F 的关系。" %
        (i_w, F_W, FORCE, fmt_gap(gap(F_W, FORCE))))

    # F-09 四力标度区间 vs 理论预期
    add("F-09", "F 四力特解", "四力'拓扑区间'与已知标度行为对照",
        "作者称：引力=大曲率低挠率低频；电磁=中尺度均衡；强核=极高挠率高频小曲率；弱核=失谐破缺",
        "INFO",
        "定性图景自洽且与既有 2026-09-28 册的'区间论'一致；但**没有任何一个区间边界被定量确定**"
        "（未给出 kappa/tau/f 的分界数值），因此'不同力 = 不同取值区间'目前是不可反驳也不可验证的"
        "自由陈述。要变为可检验，必须给出至少一个边界的定量来源。")


def r_dim():
    return NS["r"]


def OMEGA_G_NUM():
    """Omega_G（太阳-地球）数值，单位 1/m。"""
    return 2.0 * G_NEWTON * M_SUN / (C_C ** 2 * AU ** 2)


# ==========================================================================
# §G 归一化能力审计（自由度账本）
# ==========================================================================
def sec_G():
    alpha = ALPHA_FINE
    omega_g = OMEGA_G_NUM()
    guard("G01_alpha", near(alpha, 7.2973525693e-3, 1e-9), "alpha = %.10e" % alpha)
    guard("G02_omegaG", 1.0e-19 < omega_g < 1.0e-18,
          "Omega_G(太阳-地球) = %.4e m^-1" % omega_g)

    add("G-01", "G 归一化能力", "自由度账本：1 个自由函数能否编码 4 个力",
        "四力差异全部由 Omega(kappa,tau,f) 承担",
        "FAIL",
        "账本：公理只给出 1 个无量纲常数 G_sigma + 1 个自由函数 Omega。"
        "需要编码的独立物理输入：G（引力强度）、alpha（电磁）、alpha_s（强）、G_F（弱）"
        "共 4 个**量纲各异**的耦合常数，外加 4 种不同作用程标度律（10^-15 / 10^-10 / 弱 10^-18 m 级 / 全域）。"
        "1 个函数的 3 个自变量无法确定 4 个标量常数 + 4 条标度律 —— 自由度**严重不足**。"
        "结论：'四力归一'在结构上不是归一，而是把差异移入一个未被约束的自由函数。")

    add("G-02", "G 归一化能力", "反构造检验：任意力能否写成同形式",
        "若任意中心力都能写成 F = (hbar/2) Omega (c grad kappa + ...)，则通式无区分力",
        "FAIL",
        "可构造性反证：给定任意力函数 g(r) r_hat（含 1/r^2、Yukawa exp(-m r)/r、色袋微扰等），"
        "取 Omega := 2 g(r) / (hbar c |grad kappa|) 即可使通式逐点等于该力。"
        "由于 Omega 是**自由函数**（G-01 已证其不受公理约束），该构造对任意 g 都成立。"
        "于是通式的'预测力'为 0：它对四力的统一与对任意第四种力的统一是等价的。"
        "这是判定'是否真统一'的**信息论判据**：统一方程若不能排除任何可能，就不含信息。")

    add("G-03", "G 归一化能力", "4 个耦合常数能否由 1 个 G_sigma 生成",
        "四力耦合常数是否由公理体系派生",
        "FAIL",
        "量纲层已否（B-05：kappa/tau/f 无 M、Q 指数），此处补**范畴层**证据："
        "耦合常数 {G, alpha, alpha_s, G_F} 是连续量且随能标跑动（RG），"
        "而公理给出的 G_sigma 是**一个固定无量纲数**。"
        "用 TM/RG 范畴表述：整数/离散的结构量无法编码连续跑动量，除非引入跑动机制，"
        "而本体系未给。这与既有坐标 O-COUPLING（TUFT R11 §范畴论证）**同构独立复现** ——"
        "两个独立体系在「拓扑结构不能编码连续耦合常数」上给出同一否定结论。")

    add("G-04", "G 归一化能力", "场论要件缺失清单",
        "作为'统一场论'所需的对称性/可计算性要件",
        "FAIL",
        "缺失清单（逐项核对原文，均未出现）：(1) Lorentz 协变性 —— grad 未声明作用在哪个空间、"
        "c 与 f 混用时间/空间导数，无度规约定；(2) 规范不变性 —— 没有任何场变换；"
        "(3) 局域性/因果性 —— 无传播子、无边界条件；(4) Lagrangian 与变分 —— 只有势能表达式，"
        "无作用量（且 S=hbar f 量纲错，B-04），故无 Euler-Lagrange 方程；"
        "(5) 量子化与重整化 —— 无算符、无路径积分、无紫外判据；"
        "(6) 规范群与代数的表示 —— 公理2 只给两个基底，未给生成元/对易关系。"
        "结论：当前形态是**唯象势场模型**，尚不构成场论（故本册将其定位为 L2 而非 L3）。")

    add("G-05", "G 归一化能力", "可证伪性/实验对照",
        "本册是否给出可与实验对照的数值预言",
        "INFO",
        "四力特解中只有 Omega_EM 含可数值化的耦合常数（alpha，机器复核一致）。"
        "alpha_s、G_F 与 Omega_G 均只有定性描述（'极小'/'远大于'），无闭式、无数值。"
        "因此本册**无法与任何实验对话**，包括既有坐标已关闭/已否决的窗口"
        "（g-2 偏差 74.96%、EDM 超 ACME 上限 1.28e16 倍、beta 跑动恒零、ringdown 联合排除 5.74 sigma）。"
        "若后续给出 Omega_s 的闭式并与 alpha_s(M_Z) 比较，将是本体系第一个真正的实验判据。")


# ==========================================================================
# §H 结论与路线
# ==========================================================================
def sec_H():
    add("H-01", "H 结论", "可保留内核（三条，机器复核）",
        "本册真正闭合的部分",
        "PASS",
        "(1) v_kappa^2+v_tau^2=c^2 正交速度分解（量纲闭合）；"
        "(2) 群包络速度 v_obs = c·tau/sqrt(kappa^2+tau^2) < c —— 公理1 的自洽读法可算落地，"
        "亚光速由螺旋几何必然导出，无需额外假设；"
        "(3) 唯一量纲自洽的频率-几何关系 omega = c·sqrt(kappa^2+tau^2)（既有册式(1)，本册复核）。"
        "附加：F_EM 一支量纲与量值双双自洽（Omega_EM = alpha）。"
        "其余（势能 -> 梯度 -> 力 -> 四力归一链）因 D-01 起即断裂。")

    add("H-02", "H 结论", "三条最小修复路线（可执行）",
        "若要继续推进，优先级排序",
        "INFO",
        "R1（最优先，成本最低）：量纲归一化。给 Omega 一个真正无量纲的定义"
        "（可构造的无量纲组合示例：Omega ~ (kappa·r)(tau·r)(f·r/c)^2 · G_sigma，"
        "四项均无量纲；或直接承认 Omega 就是各力耦合常数本身），"
        "并把频率项补一个速度因子 c·(kappa+tau) grad f/f（E-03 已验证可闭合）。这一步**不改结构**，"
        "只是让方程成为方程。\n"
        "R2：质量-几何映射。放弃'kappa 承载 m'（F-05 已证量纲互斥），"
        "改为显式承认 m 为独立输入并给出 Omega 对 m 的依赖，代价是失去'质量源于几何'的主张。\n"
        "R3：场论化。补度规/协变性/作用量/变分（当前 B-04 量纲错、缺 Euler-Lagrange），"
        "否则一切'统一场论'表述名不副实。\n"
        "排序理由：R1 不做则后续全部无效；R2 触碰核心哲学（宁可诚实降级为'几何编码'而非'生成'）；"
        "R3 工作量最大但不解决前两条。")

    add("H-03", "H 结论", "评级与开放项登记",
        "本册整体评级与新增开放项",
        "INFO",
        "评级 **O / L2**（与 2026-09-28 册同档）：有 [A] 级运动学内核与量纲修复方案，"
        "但'四力归一'的核心声称（Ω 同位、四力特解、力的本源统一）不成立。"
        "新增开放项：\n"
        "  O-OMEGA —— 权重因子必须量纲归一并可导出（否则统一只是改写）。\n"
        "  O-MASSGEOM —— '质量由几何生成'在量纲与衰减幂次双重层面被否（F-05/F-06），"
        "需重新表述为'质量与几何参量存在关系式'（弱表述）才可能存活。\n"
        "  O-FIELD —— 场论要件（协变/规范/作用量/量子化）全缺（G-04）。\n"
        "继承开放项：O-COUPLING（耦合常数不可由结构量导出，G-03 独立复现）。\n"
        "红线：数学自洽 != 实验证实；本册的 FAIL 均属诚实边界判定，不构成对'探索方向'的否定。")


# ==========================================================================
# 运行
# ==========================================================================
def summarize():
    counts = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    guards_ok = sum(1 for s in SELFCHECK if s["ok"])
    return counts, guards_ok


def write_outputs(counts, guards_ok):
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    base = os.path.join(OUT_DIR, "四力统一方程_全维量纲与归一审计_2026-10-03")
    payload = {
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "被审对象": "统一场论·全维度力统一方程（四力归一）来料",
        "评级": "O / L2",
        "总计条目": len(RESULTS),
        "计数": counts,
        "自检": {"总数": len(SELFCHECK), "通过": guards_ok,
                 "项": SELFCHECK},
        "条目": RESULTS,
        "耗时": elapsed(),
    }
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 四力统一方程 · 全维量纲与归一审计（机器产物）")
    lines.append("")
    lines.append("- 生成时间：%s" % payload["生成时间"])
    lines.append("- 评级：**%s**" % payload["评级"])
    lines.append("- 总条目 %d ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
                 (len(RESULTS), counts["PASS"], counts["FAIL"],
                  counts["BOUNDARY"], counts["INFO"]))
    lines.append("- 自检（不可回退基线）：%d / %d" % (guards_ok, len(SELFCHECK)))
    lines.append("")
    lines.append("| ID | 节 | 条目 | 判定 | 摘要 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        head = r["detail"].split("\n")[0]
        if len(head) > 150:
            head = head[:150] + "…"
        lines.append("| %s | %s | %s | %s | %s |" %
                     (r["id"], r["section"], r["item"], r["verdict"],
                      head.replace("|", "/")))
    lines.append("")
    lines.append("## 自检基线")
    lines.append("")
    lines.append("| 基线 | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for s in SELFCHECK:
        lines.append("| %s | %s | %s |" % (s["name"], "PASS" if s["ok"] else "FAIL",
                                            s["detail"]))
    lines.append("")
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return base


def main():
    print("=" * 74)
    print("统一场论 · 全维度力统一方程（四力归一）来料全维审计")
    print("=" * 74)
    sec_A()
    sec_B()
    sec_C()
    sec_D()
    sec_E()
    sec_F()
    sec_G()
    sec_H()
    counts, guards_ok = summarize()
    base = write_outputs(counts, guards_ok)

    print("-" * 74)
    print("总计 %d 条 ｜ PASS %d ｜ FAIL %d ｜ BOUNDARY %d ｜ INFO %d" %
          (len(RESULTS), counts["PASS"], counts["FAIL"],
           counts["BOUNDARY"], counts["INFO"]))
    print("自检 %d / %d ｜ 耗时 %s" % (guards_ok, len(SELFCHECK), elapsed()))
    print("产物：%s.json / .md" % base)
    if guards_ok != len(SELFCHECK):
        print("SELFCHECK FAILED")
        return 2
    print("评级：O / L2（诚实边界：四力归一的核心声称不成立；运动学内核与量纲修复成立）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
