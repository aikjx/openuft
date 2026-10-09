# -*- coding: utf-8 -*-
"""
68号 · 2-loop β 符号错误修正 · Landau 极点真伪判定 (重大)
=================================================================================
审计 65b/66 发现: 65b 的 beta2 写成了 `da = -(b a² + b_ij a²a_j + b_ii a³)`,
即**多套了一个外层负号**。标准 SM 约定 (a_i=α_i/(4π), t=lnμ) 是:
    da_i/dt = b_i a_i² + b_ii a_i³ + Σ_j b_ij a_i² a_j   (系数自带符号, 无外层负号)
因此正确形式应为:
    da3/dt = B3 a3² + B32 a3³ + B3_1 a3² a1 + B3_2 a3² a2
           = -7 a3² - (26/3) a3³ + (11/2) a3² a1 + 9 a3² a2   (<0 主导 => 渐近自由)
而 65b 写的是:
    da3 = 7 a3² + (26/3) a3³ - (11/2) a3² a1 - 9 a3² a2        (符号全反!)

符号写反 ⇒ 把渐近自由写成增长 ⇒ **人为制造了不存在的 Landau 极点**。
本号用**正确符号**重跑 2-loop 全耦合, 判定:
  [A] 1-loop 对照 (应渐近自由, a3 随能减)
  [B] 2-loop 正确符号: a3 是否仍渐近自由? 若 b32=-26/3<0 使 2-loop 仍渐近自由,
      则 a3 不会出现 Landau 极点 (65b 的极点=符号 bug 伪结论)
  [C] 2-loop 错误符号 (65b 原式): 复现其 Landau 极点, 对比
  [D] 诚实判定: 若正确符号下无极点 => 撤回 65b 的 "Landau 极点" 结论 (重大修正)
      同时影响 61/64/65/65b/66 所有 2-loop RK 数值 (需逐号复核)
"""
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from fractions import Fraction
from mpmath import mp, mpf, pi, log, nstr, exp, log10
mp.dps = 40

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

aEM = 1/AINV_MZ
a1z = (mpf(5)/mpf(3))*aEM/(4*pi)
a2z = aEM/SIN2/(4*pi)
a3z = ALS_MZ/(4*pi)
a1mt = a1z/(1 - f(B1)*a1z*log(MT/MZ))
a2mt = a2z/(1 - f(B2)*a2z*log(MT/MZ))
a3mt = a3z/(1 - f(B3)*a3z*log(MT/MZ))

# ---------- 正确与错误的 beta ----------
def beta2_correct(a1,a2,a3):
    """标准 SM 2-loop: da/dt = b a² + b_ii a³ + Σ b_ij a² a_j (系数自带符号, 无外层负号)."""
    da1 =  f(B1)*a1**2 + f(B12)*a1**3 + f(B1_2)*a1**2*a2 + f(B1_3)*a1**2*a3
    da2 =  f(B2)*a2**2 + f(B22)*a2**3 + f(B2_1)*a2**2*a1 + f(B2_3)*a2**2*a3
    da3 =  f(B3)*a3**2 + f(B32)*a3**3 + f(B3_1)*a3**2*a1 + f(B3_2)*a3**2*a2
    return da1,da2,da3
def beta2_wrong(a1,a2,a3):
    """65b/66 原式 (多套外层负号, 符号全反)."""
    da1 = -( f(B1)*a1**2 + f(B12)*a1**3 + f(B1_2)*a1**2*a2 + f(B1_3)*a1**2*a3 )
    da2 = -( f(B2)*a2**2 + f(B22)*a2**3 + f(B2_1)*a2**2*a1 + f(B2_3)*a2**2*a3 )
    da3 = -( f(B3)*a3**2 + f(B32)*a3**3 + f(B3_1)*a3**2*a1 + f(B3_2)*a3**2*a2 )
    return da1,da2,da3
def rk4(beta,a1,a2,a3,dl):
    k1=beta(a1,a2,a3); k2=beta(a1+k1[0]*dl/2,a2+k1[1]*dl/2,a3+k1[2]*dl/2)
    k3=beta(a1+k2[0]*dl/2,a2+k2[1]*dl/2,a3+k2[2]*dl/2); k4=beta(a1+k3[0]*dl,a2+k3[1]*dl,a3+k3[2]*dl)
    return (a1+(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6*dl,
            a2+(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6*dl,
            a3+(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6*dl)
def run(beta, a1,a2,a3, mu0, mu1, N):
    dl = log(mu1/mu0)/N
    for _ in range(N):
        a1,a2,a3 = rk4(beta,a1,a2,a3,dl)
    return a1,a2,a3

sec("A · 起点与 1-loop 对照")
put(f"  a1(m_t)={nstr(a1mt,6)}, a2(m_t)={nstr(a2mt,6)}, a3(m_t)={nstr(a3mt,6)}")
put(f"  1-loop a3(GUT)={nstr(a3mt/(1-f(B3)*a3mt*log(M_GUT/MT)),6)} (渐近自由, 随能减, <a3mt)")

sec("B · 2-loop 正确符号 (标准 SM): a3 是否渐近自由?")
N = 4000
a1c,a2c,a3c = run(beta2_correct, a1mt,a2mt,a3mt, MT, M_GUT, N)
put(f"  [正确符号] 跑到 M_GUT: a1={nstr(a1c,6)}, a2={nstr(a2c,6)}, a3={nstr(a3c,6)}")
put(f"  a3: {nstr(a3mt,6)} -> {nstr(a3c,6)}  ({'减小/渐近自由' if a3c<a3mt else '增大/非渐近自由'})")
# 扫描看是否有极点: 跑到极高能看 a3 是否发散
a1h,a2h,a3h = run(beta2_correct, a1mt,a2mt,a3mt, MT, mpf('1e30'), N)
put(f"  正确符号跑到 1e30 GeV: a3={nstr(a3h,6)} ({'渐近自由无极点' if a3h<a3c else '发散?'})")

sec("C · 2-loop 错误符号 (65b/66 原式): 复现其 Landau 极点")
a1w,a2w,a3w = run(beta2_wrong, a1mt,a2mt,a3mt, MT, M_GUT, N)
put(f"  [错误符号] 跑到 M_GUT: a1={nstr(a1w,6)}, a2={nstr(a2w,6)}, a3={nstr(a3w,6)}")
put(f"  a3: {nstr(a3mt,6)} -> {nstr(a3w,6)}  ({'增大' if a3w>a3mt else '减小'})")
put(f"  错误符号在 GUT 附近 a3≈{nstr(a3w,3)} 已非微扰 => 这是 65b 报告的 'Landau 极点' 来源")

sec("D · 判定: 65b 的 Landau 极点是真物理还是符号 bug 伪结论?")
pole_correct = (a3h > mpf('1'))   # 正确符号下 a3 是否越过非微扰 1
put(f"  正确符号下 a3(1e30 GeV)={nstr(a3h,6)}, 是否越过 1 (Landau 极点)?: {ok(not pole_correct)}")
if not pole_correct:
    put(f"  => **65b 的 'SM 2-loop 强耦合 Landau 极点' 是 β 符号 bug 造成的伪结论**")
    put(f"  正确标准 SM 2-loop (b32=-26/3<0) 保持渐近自由, a3 随能减, 无 Landau 极点")
    put(f"  65b 用错误外层负号把渐近自由写成增长, 人为制造了不存在的极点")
    put(f"  影响范围: 61/64/65/65b/66 所有 2-loop RK 数值的符号均需复核(可能同为伪)")
    put(f"  保留有效的: 1-loop (59/63/65) 因 inv1 公式正确, 结论不受影响")
else:
    put(f"  => 正确符号下仍有极点, 65b 结论方向正确(需复核精确值)")
put(f"  [后续] 用正确符号重跑 65 的同阶往返机器零检验, 确认 2-loop 段是否仍自洽。")

report = "\n".join(L)
print(report)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "68_2loopβ符号错误修正_Landau极点真伪判定报告.md")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write("# 68号 · 2-loop β 符号错误修正 · Landau 极点真伪判定\n\n> 算法联盟 ROOT 最高权限 · 重大审计 · 2026-08-19\n\n```\n" + report + "\n```\n")
print("\n[报告已写入] " + out)
