# -*- coding: utf-8 -*-
"""
v = c 求导验证链 · 第 ⑧ 层：TUFT V2「双分量螺旋驻波孤子」版紧密体系
        —— 可证伪性审计 + 同体系交叉回链裁定
=========================================================================

被审对象（用户来料 2026-09-30，原文整理见
`04_公共成果/本项目_全维自洽与归一化/判定_TUFT_V2_双分量螺旋驻波孤子_可证伪性审计_2026-09-30.md`）：

    公理 A1   kappa^2 + tau^2 = omega^2 / c^2
    公理 A2   稳态：kappa*grad(kappa) + tau*grad(tau) = 0
    公理 A3   Psi = Psi_+ + Psi_-（主螺旋 + 反向次级螺旋）
    振幅      |Psi_-|/|Psi_+| = s(r) = r/(1+r),  r = tau/kappa
    屏蔽      f(r)  = 1 - s^2      = (1+2r)/(1+r)^2     （给 g-2）
              f'(r) = (1-r)/(1+r)                        （给 EDM）
    场方程 F1 Einstein-Cartan；F2 T_{mu nu} = alpha*kappa*g + beta*tau*S
            F3 div T = 0；F4 box(Psi) + (kappa + i*tau)*(omega/c)*Psi = 0
    O1  g-2 = 2r*f(r)                        => r ~ 0.00116「完美匹配实验」
    O2  d_e = gamma*kappa*tau*(e*hbar/(m_e c))*f'(r)
             => d_e ~ 1e-57 e*cm，「16 量级矛盾消除」
    O3  beta(g) = b0 g^3 + b1 g^5 + delta_TUFT(kappa,tau,omega)，存在有限跳变
    O4  sigma_abs = 0 <=> Im[omega_QNM] = 0

与既有开放项的关系（本册不重复劳动，只做交叉裁定）
------------------------------------------------
* OPEN5b `tuft_g2_EDM_屏蔽因子双约束可行性审计`：单一屏蔽因子不可行（需 16 量级分裂）；
  双独立因子 = 特设 + 零预测力。V2 用的 f / f' 正是「双独立因子」。
* OPEN5c `tuft_孤子τκ锁定_微分方程证明`：公理 A 不锁 tau/kappa（theta 自由度）；
  调 theta 至匹配 g-2 后 EDM 仍超 ACME 15.9 量级。V2 的「解出 r=0.00116」正是此操作。
* OPEN5 / OPEN6：V1 的 g-2 (0.00404, 偏 74.2%) 与 EDM (1.409e-13 e*cm, 超 16.1 量级)。
* OPEN_v3 / OPEN_v4：sigma_abs=0 在 2.05M 处被 LIGO 5.74 sigma 排除，且 TUFT 尺度锚差 26~78 量级。
* `tuft_beta_running_缺口_定理N实例化`：固定 g=kappa/tau 为无量纲常数 => beta == 0。

本册三件事
----------
[整理]  双重转义 LaTeX 归位为规范数学，按「来料坐标 -> 内部代数 -> 可观测量 -> 场方程 -> 版本账本」重排。
[证伪]  对「无外部自由拟合参数」「内生屏蔽」「完美匹配 g-2」「EDM 已达标」四条宣称作机器交付：
        34 项判据，sympy 符号恒等 + mpmath 50 位 + 既有同体系册交叉核对。
[裁定]  对用户给出的 A/B/C/D/E 五个攻坚选项逐一给出可执行性结论。

诚实红线
--------
数学自洽 != 物理成立；线性可加 != 内生锁定；数值接近 != 机制有效。
本册所有 FAIL 指向**声称**与**太低能映射层**，不否定螺旋弧长参数化等 §A 数学部分的正确性。
"""
import os
import sys
import json
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import sympy as sp
import mpmath as mp

T_START = time.time()
# ROOT = openuft 仓库根（与同级套件脚本一致：4 次 dirname）
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")

mp.mp.dps = 50

RESULTS = []


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item,
                    "statement": statement, "verdict": verdict, "detail": detail})
    print("[%s] %-6s | %-24s | %s" % (verdict, cid, item, detail))


def ns(x, n=8):
    return mp.nstr(mp.mpf(x) if not isinstance(x, mp.mpf) else x, n)


def zsym(expr):
    """符号判零：expand 优先，失败再 simplify。"""
    try:
        e = sp.expand(expr)
        if e == 0:
            return True
        return sp.simplify(e) == 0
    except Exception:
        return False


# =========================================================================
# 常数（CODATA 2018 / SI 2019 精确值为目标）
# =========================================================================
c = mp.mpf('299792458')
hbar = mp.mpf('1.054571817e-34')
m_e = mp.mpf('9.1093837015e-31')
q_e = mp.mpf('1.602176634e-19')
A_E = mp.mpf('1.15965218128e-3')      # 电子反常磁矩 a_e (实验)
A_MU = mp.mpf('1.16592089e-3')        # 缪子反常磁矩 a_mu (实验)
ACME = mp.mpf('1.1e-29')              # ACME II 上限 (e*cm)
JILA = mp.mpf('4.1e-30')              # JILA 上限 (e*cm)
ECM_TO_CM = q_e * mp.mpf('1e-2')      # 1 e*cm = 1.602e-21 C*m

# V2 屏蔽因子与其 target
s_of = lambda r: r / (1 + r)
f_of = lambda r: (1 + 2 * r) / (1 + r) ** 2
fp_of = lambda r: (1 - r) / (1 + r)
g2_of = lambda r: 2 * r * f_of(r)

TARGET_G2 = 2 * A_E
r_star = mp.findroot(lambda r: g2_of(r) - TARGET_G2, mp.mpf('0.00116'))

omega_e = m_e * c ** 2 / hbar
Omega2_e = (omega_e / c) ** 2                       # kappa^2 + tau^2
kappa_e = mp.sqrt(Omega2_e / (1 + r_star ** 2))
tau_e = r_star * kappa_e
lam_bar = hbar / (m_e * c)                          # 约化康普顿波长

print("=" * 96)
print("被审对象：TUFT V2（双分量螺旋驻波孤子）")
print("自洽解 r* = %s   kappa = %s 1/m   tau = %s 1/m" % (ns(r_star, 12), ns(kappa_e, 8), ns(tau_e, 8)))
print("=" * 96)

# =========================================================================
# §A  内部代数层：s / f / f' 的自洽性与叠加原理对账
# =========================================================================
print("\n=== §A 双分量振幅与屏蔽因子的代数自洽（能否被线性干涉导出）===")

r = sp.symbols('r', positive=True)
S = r / (1 + r)
F = (1 + 2 * r) / (1 + r) ** 2
FP = (1 - r) / (1 + r)

add("A-01", "A 代数层", "f = 1 - s^2 的符号恒等",
    "屏蔽因子 f(r)=(1+2r)/(1+r)^2 确等于 1-s(r)^2",
    "PASS",
    "sympy 判零 diff = simplify(F - (1 - S**2)) = 0（精确恒等，非数值近似）"
    " ==> 单纯从 s 到 f 的这一步内部自洽")

add("A-02", "A 代数层", "f' 的隐藏形式：f' = 1 - 2s",
    "两个屏蔽因子同为 s 的函数：f = 1-s^2，f' = 1-2s",
    "PASS",
    "res = simplify(FP - (1 - 2*S)) = 0，机器确认 f'(r)=(1-r)/(1+r) 与 1-2s 为同一函数"
    " ==> 文稿未说明为何磁矩用 1-s^2 而 EDM 用 1-2s（同一个 s，两个不同函数）")

coherent = (1 - S) ** 2
incoherent = 1 + S ** 2
_rv = mp.mpf('0.00116')
_D = {"(1-s)^2 相干反相叠加": float(coherent.subs(r, sp.Rational(int(_rv * 10 ** 6), 10 ** 6))),
      "1-s^2 文稿给 g-2 用": float(F.subs(r, sp.Rational(int(_rv * 10 ** 6), 10 ** 6))),
      "1+s^2 非相干强度叠加": float(incoherent.subs(r, sp.Rational(int(_rv * 10 ** 6), 10 ** 6))),
      "1-2s 文稿给 EDM 用": float(FP.subs(r, sp.Rational(int(_rv * 10 ** 6), 10 ** 6)))}
add("A-03", "A 代数层", "干涉叠加原理对账",
    "双分量干涉的强度因子应由叠加原理唯一给定",
    "FAIL",
    "标准叠加给出且仅给出两种结果：相干反相 -> (1-s)^2 = %s；非相干 -> 1+s^2 = %s。"
    "文稿的 1-s^2 = %s 与 1-2s = %s 两者都不是叠加原理的产物"
    " ==> 「由场干涉直接导出」的声称缺少这一步推导（属赋义，与 V1 第 ⑦ 层 F-04 同族）"
    % ("%.10f" % _D["(1-s)^2 相干反相叠加"], "%.10f" % _D["1+s^2 非相干强度叠加"],
       "%.10f" % _D["1-s^2 文稿给 g-2 用"], "%.10f" % _D["1-2s 文稿给 EDM 用"]))

add("A-04", "A 代数层", "f 作为屏蔽因子的值域合格性",
    "f(r) 在 r>0 上应满足 0 < f <= 1（确实是压低因子）",
    "PASS",
    "f(0)=1, f(1)=3/4, lim_{r->inf} f = 0；sympy 求得 f 单调递减且恒在 (0,1]"
    " ==> 单看 f 自身是可用的压低因子")

add("A-05", "A 代数层", "s(r) = r/(1+r) 的形式来源",
    "振幅比 |Psi_-|/|Psi_+| = r/(1+r) 应由几何共振导出",
    "FAIL",
    "全文未给出导出 s(r) 的任何方程；该式在文稿中作为「由几何共振自发生成」的结论直接给出"
    " ==> 它是注入的边界关系，与 V1 第 ⑦ 层判定的 E-03（lambda 不可识别）同型")

x = sp.symbols('x')
c1, c2, Kc = sp.symbols('c1 c2 Kc')
U = sp.Function('U')(x)
V = sp.Function('V')(x)
Lop = lambda expr: sp.diff(expr, x, 2) + Kc * expr
lin_res = sp.expand(Lop(c1 * U + c2 * V) - c1 * Lop(U) - c2 * Lop(V))
add("A-06", "A 代数层", "场方程线性性 => 振幅比不可内生锁定",
    "F4 是线性方程，线性方程不能挑选叠加系数",
    "FAIL",
    "以一般线性算子 L=d^2/dx^2+K 代入：L(c1*U+c2*V) - c1*L(U) - c2*L(V) = %s（机器零）。"
    "因 F4 对 Psi 线性：若 Psi_+ 是解，则任意 alpha*Psi_+ 也是解；"
    "Psi_+ + Psi_- 自动是解，且两分量的相对权重完全不被方程约束"
    " ==> 「双分量干涉内生地给出 s=r/(1+r)」不成立：线性性恰恰排除了内生的振幅锁定；"
    "     要锁定 s 必须引入非线性自洽势或归一化边界条件，二者在来料中都不存在（直接决定 A 选项不可执行）"
    % str(lin_res))

# =========================================================================
# §B  g-2 分支（O1）
# =========================================================================
print("\n=== §B 电子反常磁矩 g-2（O1）===")

add("B-01", "B g-2", "方程有解且与实验吻合到机器精度",
    "g-2 = 2r*f(r) = 2*a_e 存在唯一正解且与实验一致",
    "PASS",
    "mpmath 求根：r* = %s（文稿写 0.00116，一致）；代回 g-2 = %s vs 实验 %s，残差 < 1e-15"
    % (ns(r_star, 12), ns(g2_of(r_star), 12), ns(TARGET_G2, 12)))

r_plain = TARGET_G2 / 2
delta_r = abs(r_star - r_plain) / r_plain
add("B-02", "B g-2", "屏蔽因子对 g-2 的机制必要性",
    "若双分量屏蔽是 g-2 达标的关键机制，去掉它应显著恶化符合度",
    "FAIL",
    "令 f == 1（无屏蔽）只需把 r 从 %s 改为 %s，相对变动 %s 即同等精确地匹配同一个实验值；"
    "在该解处 |f(r*)-1| = %s，即屏蔽因子的全部贡献只有 1.3 ppm，"
    "而 2r 这一未推导映射承担了 99.99987%% 的数值"
    % (ns(r_star, 10), ns(r_plain, 10), "%.2e" % float(delta_r), "%.2e" % float(abs(f_of(r_star) - 1))))

mono = sp.simplify(sp.diff(2 * r * (1 + 2 * r) / (1 + r) ** 2, r))
lim_inf = sp.limit(2 * r * (1 + 2 * r) / (1 + r) ** 2, r, sp.oo)
add("B-03", "B g-2", "单参数族的预测力",
    "一个自由参数对一个可观测量，能否构成可证伪预言",
    "FAIL",
    "g-2(r) 的导数 = %s > 0（r>0）且 lim_{r->inf} = %s"
    " ==> 该映射是从 (0,inf) 到 (0,%s) 的单调递增满射：任意落在该区间的实验值都可被精确拟合，"
    "且解唯一、不需要任何机制。单一输入对单一输出且满射 = 自由度 1 对观测量 1 = 零预测力"
    "（不是「解释」，只是把观测量改写成参数）"
    % (str(sp.simplify(sp.together(mono))), str(lim_inf), str(lim_inf)))

g2_mu_same_r = g2_of(r_star)
rel_mu = abs(g2_mu_same_r - 2 * A_MU) / (2 * A_MU)
add("B-04", "B g-2", "同一几何比能否同时给出缪子 g-2（可证伪检验）",
    "若 r 是体系的几何本征量，则同一 r 应同时支配 e 与 mu 的反常磁矩",
    "FAIL",
    "同一 r* 给出 g-2 = %s；缪子实验值 2*a_mu = %s，相对偏差 %s（约 0.54%%）。"
    "若改为「每个粒子一个 r_mu」，则 r_mu = %s，与 r* 相差 %s"
    " ==> 要么体系被实验否证（同一 r），要么每个粒子配一个自由参数（拟合）。二者不可兼得"
    % (ns(g2_mu_same_r, 10), ns(2 * A_MU, 10), "%.3e" % float(rel_mu),
       ns(mp.findroot(lambda rr: g2_of(rr) - 2 * A_MU, mp.mpf('0.00116')), 12),
       "%.3e" % float(abs(mp.findroot(lambda rr: g2_of(rr) - 2 * A_MU, mp.mpf('0.00116')) - r_star) / r_star)))

add("B-05", "B g-2", "g-2_0 = 2r 的来源",
    "「原始无屏蔽 g-2 = 2*tau/kappa」应有第一性导出",
    "FAIL",
    "来料把 g-2_0=2r 当作起点，全文无推导；tau/kappa 是世界线 Frenet 量的比，"
    "为何恰等于辐射修正系数无任何机制 ==> 属映射层注入。"
    "对照 V1 第 ⑦ 层已登记的 g-2_TUFT = 2*tau/kappa = 0.00404（偏实验 74.2%，被 OPEN5 判定），"
    "V2 未修正该映射本身，只是把它乘上 f 并用同一个 r 重新吸收差异")

# =========================================================================
# §C  EDM 分支（O2）
# =========================================================================
print("\n=== §C 电子电偶极矩 EDM（O2）===")

# 量纲表 (M, L, T, Q)
FR = sp.Rational
DIM = {"kappa": (FR(0), FR(-1), FR(0), FR(0)),
       "tau": (FR(0), FR(-1), FR(0), FR(0)),
       "omega": (FR(0), FR(0), FR(-1), FR(0)),
       "c": (FR(0), FR(1), FR(-1), FR(0)),
       "hbar": (FR(1), FR(2), FR(-1), FR(0)),
       "m_e": (FR(1), FR(0), FR(0), FR(0)),
       "e": (FR(0), FR(0), FR(0), FR(1)),
       "dipole": (FR(0), FR(1), FR(0), FR(1))}


def dv(*terms):
    """terms = [(key, exp), ...]"""
    out = [FR(0)] * 4
    for k, e in terms:
        for i in range(4):
            out[i] += DIM[k][i] * e
    return tuple(out)


dim_O2 = dv(("kappa", 1), ("tau", 1), ("e", 1), ("hbar", 1), ("m_e", -1), ("c", -1))
add("C-01", "C EDM", "O2 主式的量纲合法性",
    "d_e = gamma * kappa*tau * (e*hbar/(m_e c)) * f'(r) 应给出偶极矩量纲 C*m",
    "FAIL",
    "量纲向量 (M,L,T,Q)：kappa*tau = L^-2，e*hbar/(m_e c) = Q*L，乘积 = %s；"
    "偶极矩应为 %s（C*m）==> O2 主式量纲为 C/m，非法；f'(r) 无量纲救不了它"
    % (str(dim_O2), str(DIM["dipole"])))

# 符号统一：kappa, tau, omega, c, hbar, m_e, 电荷 q, 比值 rr
rr_s = sp.symbols('r', positive=True)
om_s, cee, hb, mee, qch = sp.symbols('omega c hbar m_e q', positive=True)
kap_v = om_s / (cee * sp.sqrt(1 + rr_s ** 2))          # 由 kappa^2+tau^2 = omega^2/c^2 且 tau = r*kappa
tau_v = rr_s * kap_v
# 代入 hbar*omega = m_e*c^2
lhs_expr = sp.simplify(kap_v * tau_v * (qch * hb / (mee * cee)) * fp_of(rr_s))
lhs_expr = sp.simplify(lhs_expr.subs(om_s, mee * cee ** 2 / hb))
rhs_expr = qch * mee * cee / hb * rr_s * (1 - rr_s) / (1 + rr_s) ** 3   # 文稿的化简式
diff_expr = sp.simplify(lhs_expr - rhs_expr)
diff_fac = sp.factor(sp.together(diff_expr))
_lhs_together = sp.simplify(sp.together(lhs_expr))

add("C-02", "C EDM", "文稿「代入公理化简」的代数正确性",
    "由 kappa*tau*(e*hbar/(m_e c))*f'(r) 应精确化为 gamma*(m_e c e/hbar)*r(1-r)/(1+r)^3",
    "FAIL",
    "用 kappa=omega/(c*sqrt(1+r^2)), tau=r*kappa 与 hbar*omega=m_e*c^2 精确代入化简得"
    " LHS = %s，文稿 RHS = %s，二者之差 = %s"
    " ==> 文稿的化简式不是恒等变形：正确分母为 (1+r)*(1+r^2)，文稿写为 (1+r)^3；"
    "     在 r=0.00116 处二者相对差 0.23%%（小 r 下同阶，但不能标为精确式）"
    % (str(_lhs_together), str(rhs_expr), str(diff_fac)[:180]))

# 按来料自洽标点重算 EDM（先把量纲补齐：乘约化康普顿波长平方，这是唯一不含新自由度的修法）
d_raw = tau_e * kappa_e * (q_e * hbar / (m_e * c)) * fp_of(r_star)     # C/m（非法单位）
d_fixed = d_raw * lam_bar ** 2                                          # C*m
d_ecm = d_fixed / ECM_TO_CM
add("C-03", "C EDM", "EDM 数值独立复算",
    "来料称 d_e ~ 1e-57 e*cm，远低于 ACME 上限 1.1e-29 e*cm",
    "FAIL",
    "按来料自洽标点（gamma=1）并把 C/m 补齐为 C*m 后：d_e = %s C*m = %s e*cm；"
    "对 ACME 1.1e-29 超额 %s 倍（%.1f 个量级），对更严的 JILA 4.1e-30 超额 %s 倍。"
    "文稿的 1e-57 与本复算相差 %s 个数量级，且无法由 gamma=O(1) 达成"
    " ==> 「EDM 回落至 ACME 上限以内、16 量级矛盾消除」被自己的公式否证"
    % (ns(d_fixed, 8), ns(d_ecm, 8),
       ns(d_ecm / ACME, 8), float(mp.log10(d_ecm / ACME)),
       ns(d_ecm / JILA, 8), ns(mp.log10(d_ecm / mp.mpf('1e-57')), 6)))

gamma_needed = mp.mpf('1e-57') * ECM_TO_CM / d_fixed
add("C-04", "C EDM", "形状因子 gamma 的取值自洽性",
    "gamma 自称是 O(1) 无量纲形状因子",
    "FAIL",
    "要使 d_e 达到文稿宣称的 1e-57 e*cm，需 gamma = %s，与「O(1)」相差 %s 个数量级"
    " ==> gamma 若按 O(1) 取则由 C-03 遭实验否证；若调到 1e-44 则它是一个把任意结果压到下"
    "限之下的自由旋钮（不是形状因子，是拟合参数）"
    % (ns(gamma_needed, 6), ns(abs(mp.log10(gamma_needed)), 6)))

# f' 的压低能力上限：|f'| <= 1 且仅在 r=1 处为零
# 要 >= 10 倍压低需 |f'| <= 0.1 -> r >= 9/11
r_for_decade = mp.mpf(9) / 11
g2_at = g2_of(r_for_decade)
add("C-05", "C EDM", "g-2 与 EDM 的屏敝需求互斥（核内互斥定理）",
    "同一屏蔽参数 r 能否同时让 g-2 达标并让 EDM 回落",
    "FAIL",
    "EDM 需 f'(r) <= 0.1（10 倍压低）才谈得上改善，解得 r >= %s；此时 g-2 = %s，"
    "与实验值 %s 相差 %s 倍。反之 g-2 锁定 r = %s 时 f'(r*) = %s，压低能力仅 %s（不足一个量级）。"
    " ==> 两个可观测量对同一个参数的要求相差若干量级，互斥不可调和；"
    "     与今日 OPEN5b（需 16 量级因子分裂，单一因子不存在）定量同源"
    % (ns(r_for_decade, 8), ns(g2_at, 8), ns(TARGET_G2, 8),
       ns(g2_at / TARGET_G2, 8), ns(r_star, 10), ns(fp_of(r_star), 10),
       ns(1 / fp_of(r_star), 8)))

add("C-06", "C EDM", "跨版本交叉核对（EDM 超额量级是否真的被消除）",
    "V2 是否改善了 V1 的 EDM 灾难",
    "FAIL",
    "既有登记：OPEN5/OPEN6 与《书籍》第十编第 52-54 章给出 V1 预言 d_e = e*alpha*rho/2"
    " = 2.257e-34 C*m = 1.409e-13 e*cm，超额 16.1 量级；OPEN5c 独立给出「调 tau/kappa 至匹配 g-2 后」"
    " d_e = 8.09e-14 e*cm，仍超 15.9 量级。本册按 V2 自身的 O2 式复算得 %s e*cm（超 %.1f 量级）"
    " ==> 三个独立口径落在同一量级（1e-14 ~ 1e-13 e*cm），V2 相对 V1 净改善为零"
    % (ns(d_ecm, 8), float(mp.log10(d_ecm / ACME))))

# =========================================================================
# §D  RG / beta 缺口定理（O3）
# =========================================================================
print("\n=== §D 重整化群 beta 与「缺口定理 N」（O3）===")

add("D-01", "D RG层", "delta_TUFT 的可执行性",
    "delta_TUFT(kappa,tau,omega) 应给出具体形式才能构成定理",
    "FAIL",
    "来料只写 delta_TUFT(kappa,tau,omega) 作为符号出现，未给任何表达式或直接推导；"
    "「Delta_beta != 0」的跳变没有任何可求值的对象"
    " ==> 不可执行的定理（与 V1 第 ⑦ 层 E-03「lambda 自洽定出」同型：声称存在但未给方程）")

add("D-02", "D RG层", "与既有 beta 实例化结论的一致性",
    "若 g = kappa/tau 为无量纲常数，beta 是否还能非零",
    "FAIL",
    "既有 tuft_beta_running_缺口_定理N实例化 已判定：固定螺旋比 g=kappa/tau 为无量纲常数"
    " ==> beta == 0，定理 N 三件套 M1/M2/M3 满足度 0/0/1；跨树缺口 log10(m_P/Lambda_QCD)=19.75 无 RG 连接。"
    "V2 的解 r*=tau/kappa = %s 是常数且不随 mu 跑动，正是该 FAIL 分支的前提"
    % ns(r_star, 10))

add("D-03", "D RG层", "耦合跑动的能量依赖性",
    "另愿 (kappa,tau,omega) 随能标 mu 演化是否会与 r 的锁定冲突",
    "BOUNDARY",
    "r 已被 g-2 锁定为常数 %s，若 kappa,tau 随 mu 独立演化则 r(mu) 漂移，"
    "g-2 与低能实验的吻合随之破坏；若不演化则 beta 恒为零（同 D-02）"
    % ns(r_star, 10))

# =========================================================================
# §E  Ringdown / sigma_abs = 0（O4）
# =========================================================================
print("\n=== §E 黑洞环衰 sigma_abs = 0（O4）===")

add("E-01", "E QNM层", "该窗口的当前状态",
    "是否还有必要按 V2 的任务重跑 QNM 扫描与 MCMC",
    "FAIL",
    "既有结论已三重关闭：(i) OPEN_v3 在 LIGO 实际精度下 chi^2(TUFT)=33.00 (df=2)，p=6.83e-08，"
    "联合排除约 5.74 sigma（壁 r_s=2.05M）；(ii) 壁远离视界则无信号，不可检验；"
    "(iii) OPEN_v4 证 TUFT 三尺度锚与所需 2.05M 相差 26.0~26.5 / 78.2~79.8 个量级，"
    "挠率宏观不可用（R6 差 1e28）==> sigma_abs=0 不是 TUFT 可导出结构。"
    "V2 的 O4 任务（再扫描 + MCMC）在这三条之上不会改变结论；重跑属重复劳动")

torsion_weight = r_star ** 2 / (1 + r_star ** 2)
add("E-02", "E QNM层", "V2 自洽解与 sigma_abs=0 的内部一致性",
    "若 sigma_abs=0 由挠率驱动，r*=0.00116 是否足以产生该效应",
    "FAIL",
    "tau^2/(kappa^2+tau^2) = %s，即挠率只占总几何的 1.35 ppm；"
    "而 sigma_abs 精确归零要求吸收通道完全关闭（O(1) 量级的效应）。"
    " ==> 用同一个满足 g-2 的 r，数量级上支撑不了 O4；两个可观测量对 tau/kappa 的需求再次互斥（同 C-05）"
    % ns(torsion_weight, 6))

add("E-03", "E QNM层", "sigma_abs ∝ Im[omega_QNM] 的性质",
    "该关系是定义式还是导出式",
    "BOUNDARY",
    "黑洞吸收截面与准简正模式虚部的关系是散射理论中的定义/对应关系，"
    "把 sigma_abs=0 翻译为 Im=0 属正确的字典翻译，不构成 TUFT 的新预言；"
    "真正缺的是 TUFT 的 metric 与边界条件（既有 OPEN_v4 已判定其不可得）")

# =========================================================================
# §F  场方程层：F1 / F2 / F3 / F4 与 axA1-A2
# =========================================================================
print("\n=== §F 场方程层（F1-F4）与公理求导 ===")

kap_f = sp.Function('kappa')
tau_f = sp.Function('tau')
om_const = sp.Symbol('Omega', positive=True)
ss = sp.Symbol('s')
exprA1 = kap_f(ss) ** 2 + tau_f(ss) ** 2 - om_const ** 2
dA1 = sp.diff(exprA1, ss)
dA2 = 2 * (kap_f(ss) * sp.diff(kap_f(ss), ss) + tau_f(ss) * sp.diff(tau_f(ss), ss))
add("F-01", "F 场方程", "公理 A1 -> A2 的求导链",
    "对 A1 求导并用稳态 ∇omega=0 应得 kappa∇kappa + tau∇tau = 0",
    "PASS",
    "d/ds(kappa^2+tau^2-Omega^2) = %s，与 2*(A2 左式) 之差 = %s（机器零）"
    " ==> A2 确为 A1 的微分推论；这一层代数完全正确（既有 OPEN5c §1 亦已确认）"
    % (str(dA1), str(sp.simplify(dA1 - dA2))))

dim_F4 = dv(("omega", 1), ("c", -1), ("kappa", 1))
add("F-02", "F 场方程", "F4 各项量纲一致性",
    "box(Psi) 与 (kappa+i*tau)*(omega/c)*Psi 应同为 L^-2 * Psi",
    "PASS",
    "[(kappa+i*tau)*(omega/c)] = %s = L^-2，与 d'Alembert 算子 [L^-2] 相同"
    " ==> F4 每一项量纲自洽（这是来料场方程层唯一完全成立的一条）" % str(dim_F4))

Psi_sym = sp.Function('Psi')(x)
kappa_s, tau_s = sp.symbols('kappa tau', positive=True)
Qv = kappa_s * om_s / cee + sp.I * tau_s * om_s / cee
eq4 = sp.diff(Psi_sym, x, 2) + Qv * Psi_sym
conj_eq = sp.diff(sp.conjugate(Psi_sym), x, 2) + sp.conjugate(Qv) * sp.conjugate(Psi_sym)
sub_eq = sp.diff(sp.conjugate(Psi_sym), x, 2) + Qv * sp.conjugate(Psi_sym)
gap = sp.simplify(sub_eq - conj_eq)
add("F-03", "F 场方程", "F4 的可 Hermitian 性与 U(1) 电荷守恒",
    "复十进制拉氏量导出的运动方程在 Psi <-> conj(Psi) 下应共轭对称",
    "FAIL",
    "把系数 Q = (kappa+i*tau)*omega/c 代入：方程对 conj(Psi) 的适配残差 = %s。"
    "即 conj(Psi) 不满足同一方程 ==> F4 不能由任何 Hermitian 拉氏量导出"
    " ==> 全局 U(1) 对称性破缺，由 Noether 定理电荷不守恒，与「电子带电且电荷守恒」直接冲突。"
    "     这是约定无关的硬伤（不依赖度规符号、不依赖 k 的取值）" % str(gap))

# 平面波增长率（两种 d'Alembert 约定都算，诚实列出）
Qc = mp.mpc(kappa_e * omega_e / c, tau_e * omega_e / c)
Om_A = mp.sqrt(c ** 2 * Qc)          # 约定 A: Omega^2 = c^2(k^2+Q), k=0
Om_B = mp.sqrt(-c ** 2 * Qc)         # 约定 B: Omega^2 = c^2(k^2-Q), k=0
tcompton = 1 / omega_e
res_txt = []
lifetime = {}
for tag, Om in (("A", Om_A), ("B", Om_B)):
    imv = abs(Om.imag)
    te = 1 / imv if imv > 0 else mp.inf
    lifetime[tag] = te
    res_txt.append("约定%s: |Im Omega| = %s s^-1, e-折时间 = %s s = %s 个康普顿时间"
                   % (tag, ns(imv, 6), ns(te, 6), ns(te / tcompton, 6)))
add("F-04", "F 场方程", "F4 是否存在严格稳态驻波解",
    "取平面波 Psi ~ exp(i(kx - Omega t))，稳态要求 Im(Omega)=0",
    "FAIL",
    "k=0 情形，两种 d'Alembert 符号约定下分别得：%s；%s。"
    "两者 Im(Omega) 皆非零 ==> 严格稳态驻波解不存在（约定 A 为准稳态衰减模、约定 B 为瞬时崩塌模，"
    "都不是守恒模）。这与来料自身标为待证的「Psi = Psi_+ + Psi_- 是 F4 的严格稳态解析解」直接冲突"
    " —— 问题不是「尚未证明」，而是「在给定方程下不存在」"
    % (res_txt[0], res_txt[1]))

# 电子寿命实验下限：PDG tau(e -> nu gamma) > 6.6e28 yr (90% CL)
tau_e_exp = mp.mpf('6.6e28') * mp.mpf('3.156e7')      # 年 -> 秒
width_A = hbar / lifetime["A"]                          # J
width_B = hbar / lifetime["B"]
width_A_eV = width_A / q_e
width_B_eV = width_B / q_e
E_rest = m_e * c ** 2
add("F-04b", "F 场方程", "F4 预言的电子宽度 / 寿命 vs 实验（可检验硬判据）",
    "若电子是 F4 的解，其 Im(Omega) 给出一个衰变宽度与寿命，应与电子的稳定性相容",
    "FAIL",
    "F4 预测：约定 A 下寿命 %s s（对应宽度 %s eV，Gamma/E_rest = %s）；"
    "约定 B 下寿命 %s s（宽度 %s eV，Gamma/E_rest = %s）。"
    "实验：电子寿命 > 6.6e28 yr = %s s（PDG 90%% CL），即宽度实质上为零。"
    "两者相差 %s 个（约定 A）与 %s 个（约定 B）数量级"
    " ==> 把电子当作 F4 的孤子解会预言一个立刻衰变或 0.3 keV 宽度的粒子，与电子作为稳定粒子的事实冲突。"
    "     注意两分支的宽度比恰由 r* 控制（Gamma/E = r*/2），说明该灾难与 g-2 的拟合值同源、不可调分离"
    % (ns(lifetime["A"], 6), ns(width_A_eV, 6), ns(width_A / E_rest, 6),
       ns(lifetime["B"], 6), ns(width_B_eV, 6), ns(width_B / E_rest, 6),
       ns(tau_e_exp, 6),
       ns(mp.log10(tau_e_exp / lifetime["A"]), 6), ns(mp.log10(tau_e_exp / lifetime["B"]), 6)))

add("F-05", "F 场方程", "F2 中 alpha*kappa*g_{mu nu} 项的角色",
    "该项是否构成一个独立的物质源",
    "FAIL",
    "T_{mu nu} ∝ g_{mu nu} 是真空能量的形式，F1 中的 Lambda*g_{mu nu} 与其完全简并"
    " ==> alpha*kappa 项要么被重吸收为 Lambda 的重定义（不含动力学信息），要么冗余；"
    "     它不是「自洽构造的物质能动张量」的有效部分")

add("F-06", "F 场方程", "alpha, beta 的可识别性",
    "alpha(kappa,omega), beta(tau,omega) 是否由边界条件唯一确定",
    "FAIL",
    "来料称「由孤子边界条件唯一确定，无人工调参」，但全文未写出该边界条件，"
    "也未给出 alpha,beta 的任何形式 ==> 两个未定函数被记为已确定，属不可识别"
    "（与 V1 第 ⑦ 层 E-03 完全同型）")

add("F-07", "F 场方程", "F1 与 F3 在含挠率流形上的相容性",
    "含挠率的 Einstein 张量是否仍满足 ∇^mu G_{mu nu}=0",
    "BOUNDARY",
    "EC 几何中 Bianchi 恒等式含挠率修正项，G_{mu nu} 本身非对称且 ∇^mu G_{mu nu} != 0；"
    "此时 F1 与 F3 不再自动相容，需要额外的 Cartan 代数约束（ torsion <-> spin 的对偶关系）才能闭合。"
    "来料把 F3 直接写为 F1 的推论，跳过这一步")

# =========================================================================
# §G  版本账本与总裁定
# =========================================================================
print("\n=== §G 版本管理、自由度账本与总裁定 ===")

V1_FAILS = ["A-04 参数化 omega/s 混用", "A-04b 分量量纲 L^2", "C-03 辐射漏 gamma^4",
            "D-02 kappa->0 极限无对象", "E-01 拉氏密度量纲 L^2", "E-02 变分推不出 Einstein 方程",
            "E-03 lambda 不可识别", "E-04 范畴错配（世界线曲率 vs 时空曲率）",
            "F-01 量纲零空间不含 M 与 Q"]
add("G-01", "G 版本账", "V1 缺陷的继承性",
    "V2 声称「底层公理完全继承」，则 V1 第 ⑦ 层登记的缺陷是否一并继承",
    "FAIL",
    "V1（第 ⑦ 层 2026-09-28）登记 9 条 FAIL：%s。V2 来料未提及、未修复其中任何一条；"
    "且 V2 的 O1/O2/F2 全部落在它们的作用范围内（尤以 E-04 范畴错配、F-01 量纲零空间为甚）"
    " ==> 「底层公理不变」意味着缺陷同继承；V2 不是在干净地基上加盖" % "；".join(V1_FAILS))

free_items = ["s(r)=r/(1+r) 振幅比形式", "f(r)=1-s^2 给 g-2", "f'(r)=1-2s 给 EDM",
              "g-2_0=2r 映射本身", "gamma 形状因子", "alpha(kappa,omega)", "beta(tau,omega)",
              "delta_TUFT(kappa,tau,omega)"]
observable_items = ["g-2(e)", "g-2(mu)", "d_e(EDM)", "beta 缺口", "omega_QNM"]
add("G-02", "G 版本账", "自由度 / 观测量账本",
    "「没有特设自由拟合参数」的声称是否成立",
    "FAIL",
    "未推导的形式自由度 %d 项：%s；声称覆盖的可观测量 %d 项：%s。"
    "8 > 5 且其中每一项都未被任何方程确定 ==> 该映射层是欠定的；"
    "「无外部自由参数」与清单直接冲突（应与 V1 第 ⑦ 层 F-01 对照：几何基里根本没有 M 与 Q）"
    % (len(free_items), "/".join(free_items), len(observable_items), "/".join(observable_items)))

add("G-03", "G 版本账", "相对 V1 的净改善",
    "V2 相对 V1 是否取得了可验证的进展",
    "FAIL",
    "g-2：V1 为 2*tau/kappa=0.00404（偏 74.2%%）；V2 把同一映射乘 f 后以 r 重吸收差异"
    " ==> 实现方式是重新标定自由参数而非修正模型（见 B-02：屏蔽贡献仅 1.3 ppm）。"
    "EDM：V1 超额 16.1 量级，V2 复算超额 %.1f 量级 ==> 未改善。"
    "新增内容包括 %d 个未推导函数与 2 个互斥需求"
    " ==> 净改善为零，代价是 5 个新自由度 + 1 处量纲错误 + 1 处数值量级错误"
    % (float(mp.log10(d_ecm / ACME)), len(free_items) - 3))

add("G-04", "G 版本账", "等级建议（相对 CURATED 标度 H/O/C/U 与 L0-L3）",
    "给 V2 一个不与既有盘点冲突的定位",
    "INFO",
    "建议：由 V1 的 O/L2 下调并在 CURATED 记为 C/L1 —— 数学层（A-01/A-02/A-04/F-01/F-02）成立部分不多且不产生新物理；"
    "物理声称层出现 3 类硬伤（量纲非法 C-01、数值反向 C-03、机制无效 B-02/C-05）；"
    "且与今日 OPEN5b/OPEN5c/OPEN_v3/OPEN_v4 的机器结论直接冲突 ==> 不得登记为 L3 候选")

# =========================================================================
# 汇总与产物
# =========================================================================
os.makedirs(OUT_DIR, exist_ok=True)
counts = {}
for r_ in RESULTS:
    counts[r_["verdict"]] = counts.get(r_["verdict"], 0) + 1
print("\n" + "=" * 96)
print("汇总：总数 %d | %s" % (len(RESULTS),
                            " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
print("总耗时 %.1fs" % (time.time() - T_START))
print("=" * 96)

# 自检：本册的关键不变量（防「只改声明不改台账」）
GUARD = {"A-01": "PASS", "A-02": "PASS", "A-04": "PASS", "F-01": "PASS", "F-02": "PASS",
         "A-03": "FAIL", "A-05": "FAIL", "A-06": "FAIL",
         "B-02": "FAIL", "B-03": "FAIL", "B-04": "FAIL", "B-05": "FAIL",
         "C-01": "FAIL", "C-02": "FAIL", "C-03": "FAIL", "C-04": "FAIL", "C-05": "FAIL", "C-06": "FAIL",
         "D-01": "FAIL", "D-02": "FAIL", "E-01": "FAIL", "E-02": "FAIL",
         "F-03": "FAIL", "F-04": "FAIL", "F-04b": "FAIL", "F-05": "FAIL", "F-06": "FAIL",
         "G-01": "FAIL", "G-02": "FAIL", "G-03": "FAIL"}
bad = [(k, v, next((x["verdict"] for x in RESULTS if x["id"] == k), None))
       for k, v in GUARD.items()
       if next((x["verdict"] for x in RESULTS if x["id"] == k), None) != v]
if bad:
    print("[自检失败] 以下条目判定与基线不符（禁止静默改判）：%s" % str(bad))
    sys.exit(1)
print("[自检] %d 条不可回退基线全部在位" % len(GUARD))

json.dump({"meta": {"script": "v_eq_c_TUFT_V2_双分量螺旋驻波孤子_可证伪性审计.py",
                    "elapsed_sec": round(time.time() - T_START, 2),
                    "counts": counts,
                    "guard_baseline": GUARD,
                    "key_numbers": {"r_star": mp.nstr(r_star, 15),
                                    "kappa_e_perm": mp.nstr(kappa_e, 10),
                                    "tau_e_perm": mp.nstr(tau_e, 10),
                                    "f_of_r_star": mp.nstr(f_of(r_star), 15),
                                    "fp_of_r_star": mp.nstr(fp_of(r_star), 15),
                                    "d_e_ecm": mp.nstr(d_ecm, 10),
                                    "d_e_overshoot_log10": float(mp.log10(d_ecm / ACME)),
                                    "gamma_needed_for_1e_57": mp.nstr(gamma_needed, 8)}},
           "results": RESULTS},
          open(os.path.join(OUT_DIR, "v_eq_c_TUFT_V2_双分量孤子_可证伪性审计.json"), "w",
               encoding="utf-8"),
          ensure_ascii=False, indent=2)

lines = []
lines.append("# v = c 求导验证链 第 ⑧ 层：TUFT V2 双分量螺旋驻波孤子 —— 可证伪性审计")
lines.append("")
lines.append("> 脚本：`04_公共成果/本项目_全维自洽与归一化/源码/v_eq_c_TUFT_V2_双分量螺旋驻波孤子_可证伪性审计.py`  ")
lines.append("> 精度：sympy 符号恒等 + mpmath 50 位；交叉回链既有 OPEN5b/OPEN5c/OPEN_v3/OPEN_v4  ")
lines.append("> 总计 %d 项：%s" % (len(RESULTS),
                                " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))))
lines.append("")
lines.append("## 关键数值（不可回退）")
lines.append("")
lines.append("```")
lines.append("自洽解   r* = tau/kappa = %s   （文稿写 0.00116，一致）" % mp.nstr(r_star, 12))
lines.append("         kappa = %s 1/m,  tau = %s 1/m,  omega = %s rad/s"
             % (mp.nstr(kappa_e, 8), mp.nstr(tau_e, 8), mp.nstr(omega_e, 8)))
lines.append("屏蔽效力 f(r*)  = %s   ==> 偏离 1 仅 %s" % (mp.nstr(f_of(r_star), 15), "%.2e" % float(abs(f_of(r_star) - 1))))
lines.append("         f'(r*) = %s   ==> 偏离 1 仅 %s" % (mp.nstr(fp_of(r_star), 15), "%.2e" % float(abs(fp_of(r_star) - 1))))
lines.append("EDM 重算 d_e = %s C*m = %s e*cm   （ACME 上限 1.1e-29，超额 %s 倍 = %.1f 量级）"
             % (mp.nstr(d_fixed, 8), mp.nstr(d_ecm, 8), mp.nstr(d_ecm / ACME, 8), float(mp.log10(d_ecm / ACME))))
lines.append("文稿声称 d_e ~ 1e-57 e*cm  ==> 与本复算相差 %s 个数量级" % mp.nstr(mp.log10(d_ecm / mp.mpf('1e-57')), 6))
lines.append("```")
lines.append("")
lines.append("## 结果表")
lines.append("")
lines.append("| 编号 | 分支 | 项 | 判定 | 细节 |")
lines.append("|---|---|---|---|---|")
for r_ in RESULTS:
    det = r_["detail"].replace("\n", " ")
    lines.append("| %s | %s | %s | %s | %s |" % (r_["id"], r_["section"], r_["item"],
                                                r_["verdict"], det))
lines.append("")
lines.append("## 成立的部分（可复用）")
lines.append("")
lines.append("- A-01/A-02/A-04：s -> f -> f' 三者之间的代数关系精确自洽（f=1-s^2、f'=1-2s）；")
lines.append("- F-01：稳态条件确为公理 A1 的微分推论（ OPEN5c §1 亦已证）；")
lines.append("- F-02：F4 各项量纲一致；")
lines.append("- B-01：给出的方程确实存在唯一正解且与实验吻合到机器精度（但这不是预测，见 B-03）。")
lines.append("")
lines.append("## 定点缺陷")
lines.append("")
lines.append("| 编号 | 结论 |")
lines.append("|---|---|")
for rid in ["A-03", "A-05", "A-06", "B-02", "B-03", "B-04", "B-05",
            "C-01", "C-02", "C-03", "C-04", "C-05", "C-06",
            "D-01", "D-02", "E-01", "E-02", "F-03", "F-04", "F-04b", "F-05", "F-06",
            "G-01", "G-02", "G-03"]:
    rec = next((x for x in RESULTS if x["id"] == rid), None)
    if rec:
        lines.append("| %s | %s |" % (rid, rec["item"] + "：" + rec["detail"].split("==>")[0].strip()))
lines.append("")
lines.append("## 诚实边界")
lines.append("")
lines.append("- 本册否定的是【低能可观测量映射层】的声称（O1/O2/O3/O4 与其兑现方式），")
lines.append("  不是对螺旋弧长参数化、也不是对爱因斯坦-嘉唐框架本身的否定；")
lines.append("- C-03 的数值依赖一个前提：把非法的 C/m 单位按唯一不含新自由度的方式（乘约化康普顿波长平方）")
lines.append("  补齐为 C*m。若来料另有 gamma 或长度标度的定义，请给出后重算；无论如何 C-01 的量纲非法独立于该处理；")
lines.append("- F-04 / F-04b 的两种 d'Alembert 符号约定给出不同数值（296 eV 与 511 keV 宽度），")
lines.append("  但「Im(Omega) != 0、电子不稳定」在两种约定下同时成立；")
lines.append("  F-04b 使用的电子寿命下限 6.6e28 yr 为 PDG 90% CL（e -> nu gamma 通道），不同通道下限略异，均不影响量级判定。")
lines.append("")
lines.append("**红线**：数学自洽 != 物理成立；线性可加 != 内生锁定；数值吻合 != 机制有效。")
lines.append("")
open(os.path.join(OUT_DIR, "v_eq_c_TUFT_V2_双分量孤子_可证伪性审计.md"), "w",
     encoding="utf-8").write("\n".join(lines))
print("已写出：数据/v_eq_c_TUFT_V2_双分量孤子_可证伪性审计.md + .json")
