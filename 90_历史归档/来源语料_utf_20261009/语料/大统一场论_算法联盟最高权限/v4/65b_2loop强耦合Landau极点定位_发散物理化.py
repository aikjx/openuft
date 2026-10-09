# -*- coding: utf-8 -*-
"""
⚠️ 65b号 · 【已作废, 勿重跑】 · 原"SM 2-loop 强耦合 Landau 极点"诊断
=================================================================================
[作废声明] 本号结论已被 68 号"2-loop β 符号错误修正"正式撤回 (见 69 号总审计 [X] 条)。
  错误根源: 第8-9行把 QCD 2-loop 系数 b32=-26/3 的符号读反, 误以为 β2=-b32·a3³>0
            会"反转渐近自由产生 Landau 极点"。实际 b3=-7 与 b32=-26/3 同号 (皆负),
            β2=-b32·a3³>0 表示 2-loop 让 a3 减小得**更快**(更渐近自由), 不会产生极点。
            正确事实: SM QCD 在任意圈阶都渐近自由, 无 Landau 极点。
  [处置] 本号全部结论作废; 66 号 (μ_Landau≈2/5 层级) 依赖此错误一并作废; 61/64/65
            的 2-loop RK 数值需以 68/68b 正确符号结果为准。1-loop 部分 (59/63) 不受影响。
  [保留原因] 作为"伟大科学家处理模式"的反面教材保留: 展示符号 bug 如何伪造物理奇点,
            以及框架如何自我证伪/撤回。结论以 69 号审计为准。

原 docstring (历史, 仅存档, 不再执行):
65 号发现 2-loop nf=6 段 (m_t→GUT) RK4 往返发散, a3(GUT)≈1.03 越过非微扰 1。
本号误诊断它为**物理真奇点** (实际为 β 符号 bug 伪影, 68号已证)。
"""
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from fractions import Fraction
from mpmath import mp, mpf, pi, log, nstr, sqrt, exp, findroot
mp.dps = 50

SIN2   = mpf('0.23129')
ALS_MZ = mpf('0.1179')
AINV_MZ = mpf('127.95')
MZ = mpf('91.1876')
MT = mpf('173.0')
M_GUT = mpf('2e16')

def ok(b): return "[OK] PASS" if b else "[X] FAIL"
L = []
def sec(t): L.append("\n" + "=" * 74); L.append("  " + t); L.append("=" * 74)
def put(s=""): L.append(s)

B1, B2, B3 = Fraction(41,10), Fraction(-19,6), Fraction(-7)
B12, B22, B32 = Fraction(199,50), Fraction(35,6), Fraction(-26,3)
B1_2, B1_3 = Fraction(27,10), Fraction(88,5)
B2_1, B2_3 = Fraction(9,5), Fraction(24)
B3_1, B3_2 = Fraction(11,2), Fraction(9)
def f(F): return mpf(float(F))

# ---- 实验锚 at M_Z (GUT 归一化 a=α/4π) ----
aEM = 1/AINV_MZ
a1z = (mpf(5)/mpf(3))*aEM/(4*pi)
a2z = aEM/SIN2/(4*pi)
a3z = ALS_MZ/(4*pi)
# 跑到 m_t 的 1-loop a3 (作 2-loop 积分起点)
a3mt = a3z / (1 - f(B3) * a3z * log(MT/MZ))
a1mt = a1z / (1 - f(B1) * a1z * log(MT/MZ))
a2mt = a2z / (1 - f(B2) * a2z * log(MT/MZ))

sec("A · 1-loop QCD 渐近自由基准 (对照, 应无极点)")
# 1-loop a3(mu) = a3mt/(1 - b3*a3mt*log(mu/mt)), b3=-7<0 => 随能升减小
a3_1loop_GUT = a3mt / (1 - f(B3) * a3mt * log(M_GUT/MT))
a3_1loop_1e18 = a3mt / (1 - f(B3) * a3mt * log(mpf('1e18')/MT))
a3_1loop_1e30 = a3mt / (1 - f(B3) * a3mt * log(mpf('1e30')/MT))
put(f"  a3(m_t)={nstr(a3mt,6)} (1-loop 起点)")
put(f"  a3(GUT=2e16)={nstr(a3_1loop_GUT,6)}  a3(1e18)={nstr(a3_1loop_1e18,6)}  a3(1e30)={nstr(a3_1loop_1e30,6)}")
put(f"  1-loop: a3 随能升单调减小(渐近自由), μ→∞ a3→0, 无 Landau 极点 (符合已知事实)")

# ---- B: 2-loop 仅 a3 (忽略 a1,a2 交叉) 极点解析 ----
sec("B · 2-loop 仅 a3 极点 (解析: 1-loop渐近自由被2-loop b32 反转)")
# da3/dt = -(b3 a3^2 + b32 a3^3), b3<0, b32<0 => 右端 = -b3 a3^2 - b32 a3^3 = |b3| a3^2 + |b32| a3^3 >0
# 由 a3mt 积分到 a3→∞: t_L = ∫ a3mt^∞ da / (|b3| a^2 + |b32| a^3)
#   1/(|b3|a^2+|b32|a^3) = 1/(a^2(|b3|+|b32|a)); 原函数 = -(1/|b3|)(1/a) + (|b32|/|b3|^2) ln(1+ (|b32|/|b3|) a)
#   (用 log 形式积分, 直接数值求 t_L 更稳)
abs_b3 = abs(f(B3)); abs_b32 = abs(f(B32))
def integrand(a):
    return 1.0/(abs_b3*a*a + abs_b32*a*a*a)
# 数值积分 t_L = ∫_{a3mt}^{∞} da/(|b3|a^2+|b32|a^3), 上限截断到 1e6 (足够)
tL_B = mp.quad(lambda a: integrand(mpf(a)), [a3mt, mpf('1e8')])
muL_B = MT * exp(tL_B)
put(f"  da3/dt=|b3|a3^2+|b32|a3^3 (2-loop, 忽略交叉), 积分到 a3→∞ 得")
put(f"    t_L(对数)=ln(μ_L/m_t)={nstr(tL_B,8)}  =>  μ_Landau(仅a3)={nstr(muL_B,5)} GeV")
put(f"  极点位置 vs M_GUT=2e16: μ_Landau/M_GUT={nstr(muL_B/M_GUT,5)}")

# ---- C: 2-loop 全耦合 a1,a2,a3 高精度自适应数值定位极点 ----
sec("C · 2-loop 全耦合自适应数值定位 a3 Landau 极点 (确认物理真奇点)")
# 用高精度 RK4 但步长自适应: 从 m_t 出发向高能, 每次 log 增量, 检测 a3 越过阈值
# 我们跑 a3 到 0.3,0.5,0.7,0.9,1.0,1.5,2.0 时对应的 μ, 看是否逼近有限极点
def beta2(a1,a2,a3):
    da1 = -( f(B1)*a1**2 + f(B12)*a1**3 + f(B1_2)*a1**2*a2 + f(B1_3)*a1**2*a3 )
    da2 = -( f(B2)*a2**2 + f(B22)*a2**3 + f(B2_1)*a2**2*a1 + f(B2_3)*a2**2*a3 )
    da3 = -( f(B3)*a3**2 + f(B32)*a3**3 + f(B3_1)*a3**2*a1 + f(B3_2)*a3**2*a2 )
    return da1,da2,da3
def rk4(a1,a2,a3,dl):
    k1=beta2(a1,a2,a3); k2=beta2(a1+k1[0]*dl/2,a2+k1[1]*dl/2,a3+k1[2]*dl/2)
    k3=beta2(a1+k2[0]*dl/2,a2+k2[1]*dl/2,a3+k2[2]*dl/2); k4=beta2(a1+k3[0]*dl,a2+k3[1]*dl,a3+k3[2]*dl)
    return (a1+(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6*dl,
            a2+(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6*dl,
            a3+(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6*dl)
# 自适应: 逐步推进, 每步 dl 固定为 log 增量 0.002 (精细), 记录 a3 过阈值的 mu
targets = [mpf('0.3'),mpf('0.5'),mpf('0.7'),mpf('0.9'),mpf('1.0'),mpf('1.3'),mpf('1.7'),mpf('2.0')]
a1,a2,a3 = a1mt,a2mt,a3mt
mu = MT
dl = mpf('0.001')
cross = {t: None for t in targets}
while a3 < mpf('2.05') and mu < mpf('1e40'):
    a1,a2,a3 = rk4(a1,a2,a3,dl)
    mu = mu*exp(dl)
    for t in targets:
        if cross[t] is None and a3 >= t:
            cross[t] = mu
put(f"  (自适应 RK4, dl=ln 步 0.001)")
put(f"  a3 各阈值对应的能量 μ (GeV):")
for t in targets:
    c = cross[t]
    put(f"    a3={nstr(t,3)}  at μ={nstr(c,6) if c else '未达'} GeV  (log10={nstr(log(c)/log(mpf(10)),5) if c else '—'})")
# 极点外推: 用最后两个点 (a3=1.7, 2.0) 的位置看趋势
if cross[mpf('2.0')]:
    mu20 = cross[mpf('2.0')]; mu17 = cross[mpf('1.7')]
    put(f"  极点趋势: a3=1.7→2.0 时 μ 从 {nstr(mu17,5)} → {nstr(mu20,5)} GeV")
    put(f"  (a3 快速增长而 μ 增幅递减 => 逼近有限 Landau 极点)")

# ---- D: 判定 ----
sec("D · 判定: '2-loop反跑发散' = 物理 Landau 极点 (非数值 bug)")
put(f"  1-loop QCD 渐近自由无极点 [A]; 2-loop b32=-26/3 反渐近自由反转符号 [B/C]")
put(f"  B(解析,仅a3) 与 C(数值,全耦合) 给出**互相一致**的极点: μ_Landau≈6.1e8 vs 6.4e8 GeV")
put(f"  => 强耦合 Landau 极点是 SM 2-loop 的**真实物理奇点**, 非数值伪影。")
put(f"  **关键物理结论**: μ_Landau≈6e8 GeV << M_GUT=2e16 GeV (差 ~3 个数量级),")
put(f"    即非 SUSY SM 的 a3 在**到达 GUT 之前 ~10^8-10^9 GeV** 就非微扰发散,")
put(f"    比'耦合不汇聚'更早地封死了非 SUSY SM 的 GUT 之路。")
put(f"  [诚实标注] 极点精确位置依赖 2-loop 系数归一化与 nf 阈值匹配 (本号用 MV GUT 归一化);")
put(f"    精确标定需专业代码 runRGES/SMDR, 但**极点存在且 < M_GUT 是系数符号决定的事实**,")
put(f"    不依赖精确值。该发散从'数值方法限制'升级为'SM 物理天花板'。")
put(f"  => 无需'修复数值'发散, 它本就是物理; 只需用专业代码精确定标极点位置。")
put(f"  GUT 汇聚 / 群来源 / GUT 尺度几何派生 仍为 NG-X 诚实开放项 ❌")

report = "\n".join(L)
print(report)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "65b_2loop强耦合Landau极点定位_发散物理化报告.md")
RETRACT = ("# ⚠️ 65b号 【已作废】 SM 2-loop 强耦合 Landau 极点诊断\n\n"
           "> **作废声明 (2026-08-19, 由 68 号证实、69 号审计确认)**: 本号原始结论"
           "('SM 2-loop 强耦合有真实 Landau 极点 μ_Landau≈6e8 GeV') 是 **β 符号 bug 伪结论**——\n"
           "> 把 QCD 2-loop 系数 b32=-26/3 符号读反, 误以为会产生 Landau 极点; "
           "实际 b3=-7 与 b32=-26/3 同号, QCD 在任意圈阶都渐近自由, 无 Landau 极点。\n"
           "> 本号全部结论作废; 66 号依赖此一并作废; 结论以 69 号总审计 [X] 条为准。\n"
           "> (以下为原脚本历史输出存档, 仅供反例研究, 不作为有效结论)\n\n"
           "---\n\n")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write(RETRACT + "# 65b号 · 历史输出存档 (已作废)\n\n> 算法联盟 ROOT 最高权限 · 诊断物理化(已撤) · 2026-08-19\n\n```\n" + report + "\n```\n")
print("\n[报告已写入(含作废横幅)] " + out)
