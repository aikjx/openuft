# -*- coding: utf-8 -*-
"""
TUFT 全维统一场论（K, T, f 三元体系）全维校验
============================================
对象：《TUFT全维统一场论 — 核心公式、计算、分析与数值验证》+《终极全域场论著作》大纲
姊妹文档：TUFT全维统一场论_全维审计与重构建议_v3.md（同目录）
上游：TUFT_核心公式总集与全维审计_v2.md（kappa/tau 体系，61 项已归档）

判定口径：
  PASS = 声称成立且符号/数值/量纲残差为 0
  FAIL = 残差非零 / 内部矛盾 / 指标或量纲非法 / 声称越权（真缺陷）
  OPEN = 需要外部物理输入或尚未给出推导（诚实边界，不是 bug）
  WARN = 编辑/符号层缺陷

依赖：Python 3 + sympy
"""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp

RESULTS = []


def record(cid, title, verdict, detail=""):
    if not isinstance(verdict, str):
        verdict = "PASS" if bool(verdict) else "FAIL"
    RESULTS.append((cid, title, verdict, detail))
    line = "[" + verdict + "] " + cid + " " + title
    if detail:
        line = line + "  |  " + str(detail)
    print(line)


def section(name):
    print("")
    print("=== " + name + " ===")


class Dim(object):
    """四维量纲 (M, L, T, I)"""

    def __init__(self, M=0, L=0, T=0, I=0):
        self.v = (M, L, T, I)

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __rtruediv__(self, o):
        if isinstance(o, (int, float)):
            return Dim(*[-a for a in self.v])
        return NotImplemented

    def __rmul__(self, o):
        return self.__mul__(o)

    def __pow__(self, n):
        return Dim(*[a * n for a in self.v])

    def __eq__(self, o):
        return tuple(self.v) == tuple(o.v)

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return "Dim(M=" + str(self.v[0]) + ",L=" + str(self.v[1]) + \
               ",T=" + str(self.v[2]) + ",I=" + str(self.v[3]) + ")"


MAS = Dim(M=1)
LEN = Dim(L=1)
TIM = Dim(T=1)
DIMLESS = Dim()
VEL = LEN / TIM
ACC = LEN / TIM ** 2
ENE = MAS * LEN ** 2 / TIM ** 2
MOM = MAS * VEL
ACT = ENE * TIM          # 作用量 [hbar]
FRQ = 1 / TIM

C = sp.Float("299792458")
HBAR = sp.Float("1.054571817e-34")
HH = 2 * sp.pi * HBAR          # h
GG = sp.Float("6.67430e-11")
M_E = sp.Float("9.1093837015e-31")
ALPHA = 1 / sp.Float("137.035999084")
E_E = M_E * C ** 2

# Planck 2018 (TT,TE,EE+lowE+lensing) 参考值
OM_B = sp.Float("0.0486")
OM_B_SIG = sp.Float("0.0010")
OM_C = sp.Float("0.2589")
OM_C_SIG = sp.Float("0.0050")
OM_L = sp.Float("0.6911")
OM_L_SIG = sp.Float("0.0060")


def fnum(x, n=6):
    return sp.N(x, n)


# ============================================================
# A. 光速螺旋本征恒等式 c = lambda * f
# ============================================================
def sec_A():
    section("A. c = lambda * f")

    lam = sp.Float("5e-7")
    f_ph = C / lam
    record("A1", "光子 lambda=500nm -> f=c/lambda", True,
           "f=" + str(fnum(f_ph)) + " Hz，落在可见光区间，OK")

    # 推广到物质波：与德布罗意关系联立
    v = sp.Float("1e6")
    lam_dB = HH / (M_E * v)
    f_tuft = C / lam_dB
    f_qm = E_E / HH
    ratio = sp.N(f_tuft / f_qm, 8)
    vc = sp.N(v / C, 8)
    record("A2", "c=lambda*f 推广到物质波（lambda=h/p）", "FAIL",
           "f_TUFT/f_QM = " + str(ratio) + " = v/c = " + str(vc)
           + "；物质波相速度为 c^2/v != c，故 c=lambda*f 仅对无质量粒子成立")

    record("A3", "德布罗意关系是否由 c=lambda*f 导出", "FAIL",
           "c=lambda*f 与 lambda=h/p 联立给 f=cp/h，而量子力学要求 f=E/h；"
           "两者相差因子 v/c，非导出关系，方向相反（是德布罗意+普朗克推出相速度）")


# ============================================================
# B. 几何-能量等价恒等式 E = hbar f = alpha K T Omega
# ============================================================
def sec_B():
    section("B. E = hbar f = alpha*K*T*Omega（量纲 + 数值）")

    # 约定一：K,T 有量纲（文档正文 [K]=m^-2, [T]=m^-1）
    d1 = (1 / LEN ** 2) * (1 / LEN)
    record("B1a", "约定一 K=m^-2, T=m^-1 时 [alpha*K*T*Omega]", d1 == ENE,
           "得 " + str(d1) + "，要求能量 " + str(ENE) + " -> 不成立")
    # 约定二：K,T 无量纲（文档脚注）
    d2 = DIMLESS
    record("B1b", "约定二 K,T 无量纲时 [alpha*K*T*Omega]", d2 == ENE,
           "得无量纲，无法等于能量 -> 不成立")
    record("B1", "E=alpha*K*T*Omega 的量纲闭合性", "FAIL",
           "两种归一化约定都不闭合：有量纲给 m^-3，无量纲给 1，均非能量。"
           "缺少一个带量纲的尺度因子（死结，非措辞可补救）")

    # 数值：文档给出的 KT
    kt_doc = sp.Float("1.797e-11")
    kt_true = E_E / (ALPHA * sp.Float("0.0625"))
    rel = sp.N(abs(kt_doc - kt_true) / kt_true, 8)
    record("B2", "电子 KT = E/(alpha*Omega_matter) 的数值", "FAIL",
           "正确值 " + str(fnum(kt_true)) + "，文档写 " + str(kt_doc)
           + "，相对偏差 " + str(rel) + "（约 10 倍算术错误）")

    f_e = E_E / HBAR
    record("B3", "电子本征频率 f_e = E_e/hbar", True,
           "f_e=" + str(fnum(f_e)) + " Hz（文档数值 OK）")

    # 修复候选：与已归档的 kappa/tau 母式对齐
    kt_tot = E_E / (HBAR * C)
    kap_tot = M_E * C / HBAR
    record("B4", "修复候选 E = hbar*c*sqrt(K^2+T^2)（与 v2 母式同构）",
           sp.N(abs(kt_tot - kap_tot) / kap_tot, 12) < sp.Float("1e-12"),
           "sqrt(K^2+T^2) = E/(hbar c) = " + str(fnum(kt_tot))
           + " m^-1，与 v2 的 m=(hbar/c)sqrt(kappa^2+tau^2) 完全一致（相对残差 0）")
    record("B5", "修复候选的量纲", (ACT * VEL * (1 / LEN)) == ENE,
           "[hbar*c*sqrt(K^2+T^2)] = (J*s)(m/s)(1/m) = J  OK")


# ============================================================
# C. E=alpha*K*T*Omega 与四力分化表的内部冲突
# ============================================================
def sec_C():
    section("C. E=alpha*K*T*Omega 与四力分化/光子定义的一致性")

    record("C1", "光子：K=0（纯挠率）时 E=alpha*K*T*Omega", "FAIL",
           "K=0 -> E=0，但 hbar*f = " + str(fnum(E_E)) + " J != 0；"
           "E=hbar f 与 E=alpha K T Omega 在 K=0 时直接矛盾")
    record("C2", "引力：T->0 极限", "FAIL",
           "T->0 -> E->0；纯引力系统的能量趋于零，与 E=hbar f 冲突")
    record("C3", "弱力：K<<T（K->0）极限", "FAIL",
           "K->0 -> E->0；弱相互作用通道能量消失")
    record("C4", "四力分化表与能量母式的兼容", "FAIL",
           "E=alpha*K*T*Omega 要求 K,T 同时非零；"
           "而分化表以 K>>T / K<<T / K->0 为特征，与母式不兼容（结构性冲突）")


# ============================================================
# D. 时空场通用演化主方程
# ============================================================
def sec_D():
    section("D. 主方程 d_mu Gamma^lambda_{mu nu} = c grad(KT) - (Omega/c^2) J_nu")

    record("D1", "爱因斯坦求和约定：指标 mu 的合法性", "FAIL",
           "mu 在 d_mu 与 Gamma^lambda_{mu nu} 中两次均为下标，无上标配对 -> 非法；"
           "自由指标 lambda(上)、nu(下) 使左边为 (1,1) 型张量")
    record("D2", "张量阶数匹配：左 (1,1) vs 右 grad(KT) 与 J_nu 均为 (0,1)", "FAIL",
           "左边 (1,1) 型，右边两项都是 (0,1) 型矢量，缺少上标 lambda，阶数不匹配")
    d_lhs = (1 / LEN) * (1 / LEN)
    d_rhs = VEL * ((1 / LEN ** 2) * (1 / LEN)) / LEN
    record("D3", "量纲：[d Gamma] vs [c grad(KT)]", d_lhs == d_rhs,
           "左 " + str(d_lhs) + " vs 右 " + str(d_rhs) + "（[K]=m^-2,[T]=m^-1）")
    record("D4", "量纲：[(Omega/c^2) J_nu] 是否可与之相加", "OPEN",
           "J_nu 量纲未定义（能量流？电荷流？自旋流？）；"
           "文档自述『已内置 1/c 尺度因子』但未给出形式，不可核验")
    record("D5", "极限检验2：T->0 退化为 GR 联络演化", "FAIL",
           "T->0 使 KT->0，右边第一项消失，方程退化为 "
           "d_mu Gamma = -(Omega/c^2) J_nu，不是 Einstein 方程，也非 GR 联络演化；"
           "GR 的联络由度规相容+无挠给出，与本式无对应关系")
    record("D6", "GR 是否包含在本方程内", "OPEN",
           "未给出任何从该式推出 Einstein 张量方程的步骤；声称『还原 GR』未兑现")


# ============================================================
# E. 统一哈密顿与对易子
# ============================================================
def sec_E():
    section("E. H = c*K_hat + (hbar/2)*T_hat*f_hat 与 [K,T] = i (Omega/c) hbar")

    # 第一项 c*K
    a1 = VEL * (1 / LEN)          # K 为曲率 m^-1
    a1b = VEL * (1 / LEN ** 2)    # K 为 m^-2
    record("E1", "第一项 [c*K] 是否为能量", "FAIL",
           "K=m^-1 -> " + str(a1) + "；K=m^-2 -> " + str(a1b)
           + "；均非 " + str(ENE) + "。要成为能量需 [K]=动量 " + str(MOM) + "，与曲率矛盾")
    b1 = ACT * DIMLESS * FRQ
    record("E2", "第二项 [(hbar/2)*T*f] 是否为能量", b1 == ENE,
           "仅当 T 无量纲时成立 -> " + str(b1))
    record("E3", "哈密顿两项量纲能否同时为能量", "FAIL",
           "第一项要求 K 为动量量纲，第二项要求 T 无量纲；"
           "二者不可能同时满足（曲率/挠率语义下无解）")

    # 对易子
    c1 = (1 / LEN) * (1 / LEN)                # [K][T] 均为 m^-1
    c2 = ACT / VEL                            # (Omega/c)*hbar
    record("E4", "对易子 [K,T] = i(Omega/c)hbar 的量纲", c1 == c2,
           "左 " + str(c1) + " vs 右 " + str(c2) + "（kg*m）")
    record("E5", "曲率与挠率能否构成正则共轭对", "FAIL",
           "[K][T] 必须等于 [hbar] = " + str(ACT) + "；"
           "若 T 为挠率 m^-1，则 K 须为 " + str(ACT / (1 / LEN)) + "，不是曲率。"
           "故 (曲率, 挠率) 数学上不可能满足 [K,T]=i*hbar")
    record("E6", "期望值分解 <T*f> = <T><f>", "FAIL",
           "算符乘积的期望值分解为期望值之积需要不关联假设；"
           "[K,T]!=0 且 f 与 T 经 E=hbar f 绑定，分解无依据")
    record("E7", "『不存在紫外发散』的证明", "OPEN",
           "几何量算符化本身不消除发散（需显式给出传播子截断）；"
           "普朗克尺度『自然截断』未给出机制，属未证实宣称")


# ============================================================
# F. 引力场方程与 FLRW
# ============================================================
def sec_F():
    section("F. G_mn = (8 pi G/c^4) T_mn + Omega_Lambda g_mn 与 FLRW")

    record("F1", "方程移项后的等效宇宙学常数符号", "FAIL",
           "标准式 G_mn + Lambda g_mn = (8 pi G/c^4) T_mn；"
           "本文档把 +Omega_Lambda g_mn 写在右边，等价于 Lambda_eff = -Omega_Lambda < 0，"
           "给出减速而非加速膨胀")
    record("F2", "与本文自己的 FLRW 式 H^2 = (8 pi G/3)rho + (Omega_Lambda/3)c^2 是否一致",
           "FAIL", "FLRW 式取 Lambda_eff = +Omega_Lambda > 0；"
           "与 F1 推出的符号相反 —— 同一文档内部自相矛盾")
    record("F3", "修正写法 G_mn + Omega_Lambda g_mn = (8 pi G/c^4) T_mn", "PASS",
           "与标准 ΛCDM 一致，且量纲 [G_mn]=m^-2，[Λ g_mn]=m^-2 匹配")
    record("F4", "水星近日点 43''/世纪", "OPEN",
           "未从本文档方程推出 Schwarzschild 解或给出进动积分；"
           "『完全复现』为未兑现声称（GR 值本身为 42.98''/世纪）")


# ============================================================
# G. 宇宙组分配比 1:4:11
# ============================================================
def sec_G():
    section("G. Omega 配比 1:4:11 = 6.25% : 25% : 68.75%")

    om_m = sp.Float(1) / 16
    om_dm = sp.Float(4) / 16
    om_de = sp.Float(11) / 16
    record("G1", "算术归一 1/16+4/16+11/16=1",
           abs(float(om_m + om_dm + om_de) - 1.0) < 1e-12,
           "6.25% + 25% + 68.75% = 100%（算术正确）")

    sb = sp.N(abs(om_m - OM_B) / OM_B_SIG, 6)
    sc = sp.N(abs(om_dm - OM_C) / OM_C_SIG, 6)
    sl = sp.N(abs(om_de - OM_L) / OM_L_SIG, 6)
    record("G2", "Omega_matter 6.25% vs Planck Omega_b 4.86%", "FAIL",
           "绝对偏差 " + str(sp.N(abs(om_m - OM_B) * 100, 6))
           + " 个百分点，相对偏差 " + str(sp.N(abs(om_m - OM_B) / OM_B * 100, 6))
           + "%，约 " + str(sb) + " sigma —— 远超观测误差，『定义差异』不足以解释")
    record("G3", "Omega_DM 25% vs Planck Omega_c 25.89%", "PASS",
           "偏差 " + str(sc) + " sigma（在 ~2 sigma 内）")
    record("G4", "Omega_DE 68.75% vs Planck Omega_L 69.11%", "PASS",
           "偏差 " + str(sl) + " sigma（在 1 sigma 内）")

    # Clifford 分级候选构造
    grades = [1, 4, 6, 4, 1]
    tot = sum(grades)
    merged = 6 + 4 + 1
    record("G5", "Cl(1,3) 分级 1:4:6:4:1 与 1:4:11 的可嵌入性",
           tot == 16 and merged == 11,
           "1+4+6+4+1=16；合并后三项 6+4+1=11 -> 恰得 1:4:11。"
           "这是目前唯一能自圆其说的候选拓扑来源（文档未给出）")
    record("G6", "1:4:11 是否已被『严格代数证明』", "FAIL",
           "文档只给赋值与比喻（1份闭环结/4份弥散/11份基底拉伸），"
           "零推导步骤；即使采用 G5 的 Clifford 构造，"
           "仍缺『为何代数值对应宇宙组分』的物理机制 -> 降级为候选假设")


# ============================================================
# H. 可证伪预言
# ============================================================
def sec_H():
    section("H. 四条预言公式（量纲 + 可证伪性）")

    # 预言1: delta T ~ sqrt(E_CM)/(c^2 hbar)
    d1 = ENE ** 0.5 / (VEL ** 2 * ACT)
    record("H1", "预言1 delta T ~ sqrt(E)/(c^2 hbar) 的量纲", d1 == (1 / LEN),
           "得 " + str(d1) + "（非半整数次量纲，不可能等于挠率 m^-1）；"
           "且无系数 -> 不可证伪")

    # 预言3: delta h ~ (hbar/c^3) <K>
    d3 = ACT / VEL ** 3 * (1 / LEN)
    record("H2", "预言3 delta h ~ (hbar/c^3)<K> 的量纲", d3 == DIMLESS,
           "得 " + str(d3) + "，应变应无量纲；"
           "（标准普朗克型组合是 hbar*G/c^3，本式缺 G）-> 不可证伪")

    # 预言4: Delta g ~ alpha * Delta(KT)
    d4 = (1 / LEN ** 2) * (1 / LEN)
    record("H3", "预言4 Delta g ~ alpha*Delta(KT) 的量纲", d4 == DIMLESS,
           "得 " + str(d4) + "，度规扰动应无量纲 -> 不可证伪")

    record("H4", "预言2 d(alpha)/dt ~ dOmega_DE/dt 的量纲", "PASS",
           "两侧同为 s^-1，量纲匹配；但无系数、无机制 -> 形式上不可证伪")
    record("H5", "四条预言的可证伪性总体评价", "FAIL",
           "全部为比例式，无数量级系数、无测量阈值、无背景噪声估计；"
           "严格说目前不构成可证伪预言")


# ============================================================
# I. 麦克斯韦几何映射
# ============================================================
def sec_I():
    section("I. 电磁映射 E~grad T, B~curl T")

    record("I1", "B ~ curl(T) 在 T 为标量时的合法性", "FAIL",
           "旋度只对矢量场定义；若 T 是标量则 curl(T) 无定义；"
           "若 T 是矢量场则 E~grad_r T 的『径向梯度』含义不清（符号重载）")
    record("I2", "E ~ grad T 能否还原麦克斯韦", "FAIL",
           "标准 E = -grad(phi) - dA/dt，本式缺矢势时间导数项；"
           "对比 v2 已通过校验的形式 E = -k(c grad tau_t + d tau/dt)（含两项）")
    record("I3", "波动方程无源项", "OPEN",
           "Box T = 0 只是自由波；无电荷/电流源 -> 非齐次麦克斯韦未导出（O15 同源）")
    record("I4", "q ~ sgn(T)（电荷=挠率手性符号）", "OPEN",
           "符号只能给出正负，给不出电荷量子化与 e 的数值（O5）")


# ============================================================
# J. 文稿结构与声称
# ============================================================
def sec_J():
    section("J. 文稿结构与声称审核")

    record("J1", "尺度归一恒等式 lim(K,T,f)=定值", "FAIL",
           "『取极限后为定值』与同段『场方程形式不变，只是参数取值随尺度改变』直接冲突；"
           "极限无定义（无度量、无拓扑），不可验证")
    record("J2", "第六章声称 7 个常数全部第一性导出", "FAIL",
           "c, hbar, alpha, G, k_B, m_e, e：全文 0 条推导步骤；"
           "『与 CODATA 精准吻合』为未兑现声称")
    record("J3", "第九章『现有实验观测 100% 拟合验证』", "FAIL",
           "6 项验证中 0 项给出计算过程；G2 已证 Omega_b 项不符（>13 sigma）")
    record("J4", "强力饱和条件 dK/dr|_{r0}=0 作为渐近自由", "OPEN",
           "渐近自由要求 r->0 时耦合->0，本式给出 K->K_sat != 0（饱和而非消失）；"
           "定性图像可类比，定量含义与 QCD 相反")
    record("J5", "Omega 符号重载（组分权重/局域耦合/场方程系数/对易子系数）", "WARN",
           "同一符号在 4 处含义不同，必须分记 Omega_comp / Omega_loc / k_J / k_com")
    record("J6", "排版污染：H_hat 公式被当作『场论』占位符插入正文", "WARN",
           "如『四大力 <H公式> 场论』『(K,T,f)_{<H公式>} = 定值』；"
           "系字符串替换错误，需全部替换为『TUFT』或『统一场』")
    record("J7", "『本理论为宇宙底层终极真理/最终完备形态』等表述", "WARN",
           "与『可证伪、可实测』的科学标准冲突；建议改为可检验性声明")


# ============================================================
def summary():
    print("")
    print("=" * 64)
    cnt = {}
    for item in RESULTS:
        cnt[item[2]] = cnt.get(item[2], 0) + 1
    parts = []
    for k in ["PASS", "FAIL", "OPEN", "WARN"]:
        if k in cnt:
            parts.append(k + " " + str(cnt[k]))
    print("总计 " + str(len(RESULTS)) + " 项：" + "  ".join(parts))
    print("=" * 64)
    for tag in ["FAIL", "OPEN", "WARN"]:
        print("")
        print("--- " + tag + " 清单 ---")
        for cid, title, v, detail in RESULTS:
            if v == tag:
                print("  " + cid + "  " + title)


def main():
    print("TUFT 全维统一场论（K,T,f 体系）全维校验")
    print("=" * 64)
    sec_A()
    sec_B()
    sec_C()
    sec_D()
    sec_E()
    sec_F()
    sec_G()
    sec_H()
    sec_I()
    sec_J()
    summary()


if __name__ == "__main__":
    main()
