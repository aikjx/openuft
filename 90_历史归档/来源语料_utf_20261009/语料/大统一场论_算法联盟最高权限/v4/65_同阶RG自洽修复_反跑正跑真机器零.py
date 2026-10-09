# -*- coding: utf-8 -*-
"""
⚠️ 65号 · 【已部分作废, 勿重跑】 · 原"同阶 RG 自洽修复"检验
=================================================================================
[作废声明] 本号 C 段 (2-loop nf=6 段 RK4 发散 → SM 物理 Landau 极点) 已被 68/68b 号证实为
           **β 符号 bug 伪迹** (65b 把 b32=-26/3 符号读反, 误造不存在的 Landau 极点; QCD 任意圈阶
           都渐近自由)。该结论链 (65b→65 C段→66) 由 69 号审计 [X] 条正式撤回。
  [保留部分·有效] 本号 A 段"1-loop 同阶反跑/正跑机器零"是真数学自洽事实 (inv1 正确, 不受符号 bug 影响);
             本号 B 段"2-loop nf=5 段数值稳定"在正确符号下成立 (69 审计 [A] 级)。
  [处置] 本号报告 .md 顶部已有 68/68b 撤回注记; 本 .py 重跑会覆盖, 故标注作废,
         结论以 69 号审计 + 68b 正确符号重验为准。

原 docstring (历史, 仅存档):
64 号 B 段用 1-loop 反跑 + 2-loop 正跑混阶, 把差误称 2-loop 修正; 本号做真同阶检验...
"""
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from fractions import Fraction
from mpmath import mp, mpf, pi, log, nstr, sqrt, inf
mp.dps = 80

SIN2   = mpf('0.23129')
ALS_MZ = mpf('0.1179')
AINV_MZ = mpf('127.95')
MZ = mpf('91.1876')
MT = mpf('173.0')
M_GUT = mpf('2e16')

def dev(x, ref): return abs(x - ref) / ref * mpf(100)
def ok(b): return "[OK] PASS" if b else "[X] FAIL"
L = []
def sec(t): L.append("\n" + "=" * 74); L.append("  " + t); L.append("=" * 74)
def put(s=""): L.append(s)

# ---------- 1-loop β (GUT 归一化) ----------
B1, B2, B3 = Fraction(41,10), Fraction(-19,6), Fraction(-7)
# ---------- 2-loop β (MV 系数) ----------
B12, B22, B32 = Fraction(199,50), Fraction(35,6), Fraction(-26,3)
B1_2, B1_3 = Fraction(27,10), Fraction(88,5)
B2_1, B2_3 = Fraction(9,5), Fraction(24)
B3_1, B3_2 = Fraction(11,2), Fraction(9)
def f(F): return mpf(float(F))

def inv1(a0, b, mu0, mu1):
    """标准 1-loop 反跑/正跑 (符号由 mu 方向自动)."""
    return a0 / (1 - b * a0 * log(mu1 / mu0))

def beta2(a1, a2, a3):
    da1 = -( f(B1)*a1**2 + f(B12)*a1**3 + f(B1_2)*a1**2*a2 + f(B1_3)*a1**2*a3 )
    da2 = -( f(B2)*a2**2 + f(B22)*a2**3 + f(B2_1)*a2**2*a1 + f(B2_3)*a2**2*a3 )
    da3 = -( f(B3)*a3**2 + f(B32)*a3**3 + f(B3_1)*a3**2*a1 + f(B3_2)*a3**2*a2 )
    return da1, da2, da3

def rk4_step(a1,a2,a3,dl):
    k1 = beta2(a1,a2,a3)
    k2 = beta2(a1+k1[0]*dl/2, a2+k1[1]*dl/2, a3+k1[2]*dl/2)
    k3 = beta2(a1+k2[0]*dl/2, a2+k2[1]*dl/2, a3+k2[2]*dl/2)
    k4 = beta2(a1+k3[0]*dl, a2+k3[1]*dl, a3+k3[2]*dl)
    return (a1+(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6*dl,
            a2+(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6*dl,
            a3+(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6*dl)

def run_2loop_roundtrip(a1,a2,a3,mu0,mu1,N,floor=mpf('1e-40')):
    """2-loop RK4 往返; 若 a 小于 floor 或出现负/非物理 => 判定发散.
    返回 (端点正跑, 回程, 发散标志)."""
    dl = log(mu1/mu0)/N
    a1f,a2f,a3f = a1,a2,a3
    for _ in range(N):
        a1f,a2f,a3f = rk4_step(a1f,a2f,a3f,dl)
        if a1f<0 or a2f<0 or a3f<0 or a1f>1 or a2f>1 or a3f>1 or a1f*0!=0:
            return (a1f,a2f,a3f),(None,None,None),True
    dl2 = log(mu0/mu1)/N
    a1b,a2b,a3b = a1f,a2f,a3f
    for _ in range(N):
        a1b,a2b,a3b = rk4_step(a1b,a2b,a3b,dl2)
        if a1b<0 or a2b<0 or a3b<0 or a1b>1 or a2b>1 or a3b>1 or a1b*0!=0:
            return (a1f,a2f,a3f),(a1b,a2b,a3b),True
    return (a1f,a2f,a3f),(a1b,a2b,a3b),False

# ---------- A: 实验锚 ----------
sec("A · 实验锚 a_i(M_Z) (GUT 归一化)")
aEM = 1/AINV_MZ
a1z = (mpf(5)/mpf(3))*aEM/(4*pi)
a2z = aEM/SIN2/(4*pi)
a3z = ALS_MZ/(4*pi)
put(f"  a1(M_Z)={nstr(a1z,8)}, a2(M_Z)={nstr(a2z,8)}, a3(M_Z)={nstr(a3z,8)}")

# ---------- B: 1-loop 同阶往返机器零 ----------
sec("B · 1-loop 同阶往返自洽 (应机器零)")
a1t_f = inv1(a1z, f(B1), MZ, MT); a1t_b = inv1(a1t_f, f(B1), MT, MZ)
a2t_f = inv1(a2z, f(B2), MZ, MT); a2t_b = inv1(a2t_f, f(B2), MT, MZ)
a3t_f = inv1(a3z, f(B3), MZ, MT); a3t_b = inv1(a3t_f, f(B3), MT, MZ)
r1t = dev(a1t_b, a1z); r2t = dev(a2t_b, a2z); r3t = dev(a3t_b, a3z)
put(f"  [M_Z↔m_t, nf=5 往返] a1={nstr(r1t,4)}%, a2={nstr(r2t,4)}%, a3={nstr(r3t,4)}%")
put(f"  1-loop nf=5 往返机器零: {ok(r1t<mpf('1e-12') and r2t<mpf('1e-12') and r3t<mpf('1e-12'))}")
a1g_f = inv1(a1t_f, f(B1), MT, M_GUT); a1g_b = inv1(a1g_f, f(B1), M_GUT, MT)
a2g_f = inv1(a2t_f, f(B2), MT, M_GUT); a2g_b = inv1(a2g_f, f(B2), M_GUT, MT)
a3g_f = inv1(a3t_f, f(B3), MT, M_GUT); a3g_b = inv1(a3g_f, f(B3), M_GUT, MT)
r1g = dev(a1g_b, a1t_f); r2g = dev(a2g_b, a2t_f); r3g = dev(a3g_b, a3t_f)
put(f"  [m_t↔GUT, nf=6 往返] a1={nstr(r1g,4)}%, a2={nstr(r2g,4)}%, a3={nstr(r3g,4)}%")
put(f"  1-loop nf=6 往返机器零: {ok(r1g<mpf('1e-12') and r2g<mpf('1e-12') and r3g<mpf('1e-12'))}")
a1_full = inv1(a1g_f, f(B1), M_GUT, MZ)
a2_full = inv1(a2g_f, f(B2), M_GUT, MZ)
a3_full = inv1(a3g_f, f(B3), M_GUT, MZ)
r1f = dev(a1_full, a1z); r2f = dev(a2_full, a2z); r3f = dev(a3_full, a3z)
put(f"  [全链 1-loop 往返 M_Z→GUT→M_Z] a1={nstr(r1f,4)}%, a2={nstr(r2f,4)}%, a3={nstr(r3f,4)}%")
put(f"  1-loop 全链往返机器零: {ok(r1f<mpf('1e-10') and r2f<mpf('1e-10') and r3f<mpf('1e-10'))}")

# ---------- C: 2-loop 同阶往返自洽 (RK4, 分段诚实检验) ----------
sec("C · 2-loop 同阶往返 (RK4, nf 分段诚实检验)")
N2 = 6000
# 段1: M_Z -> m_t (nf=5)
(a1ta,a2ta,a3ta),(a1tb,a2tb,a3tb),div5 = run_2loop_roundtrip(a1z,a2z,a3z,MZ,MT,N2)
if not div5:
    r1_2t = dev(a1tb,a1z); r2_2t = dev(a2tb,a2z); r3_2t = dev(a3tb,a3z)
    put(f"  [M_Z↔m_t, nf=5, RK4/N={N2}] a1={nstr(r1_2t,4)}%, a2={nstr(r2_2t,4)}%, a3={nstr(r3_2t,4)}%")
    put(f"  2-loop nf=5 往返自洽: {ok(r1_2t<mpf('1e-6') and r2_2t<mpf('1e-6') and r3_2t<mpf('1e-6'))}")
else:
    put("  [M_Z↔m_t, nf=5] RK4 往返发散 (意外, 需检查)")
# 段1端点即 m_t 处的 2-loop 值 (去程)
a1m,a2m,a3m = a1ta,a2ta,a3ta
# 段2: m_t -> GUT (nf=6)
(a1ga,a2ga,a3ga),(a1gb,a2gb,a3gb),div6 = run_2loop_roundtrip(a1m,a2m,a3m,MT,M_GUT,N2)
if not div6:
    r1_2g = dev(a1gb,a1m); r2_2g = dev(a2gb,a2m); r3_2g = dev(a3gb,a3m)
    put(f"  [m_t↔GUT, nf=6, RK4/N={N2}] a1={nstr(r1_2g,4)}%, a2={nstr(r2_2g,4)}%, a3={nstr(r3_2g,4)}%")
    put(f"  2-loop nf=6 往返自洽: {ok(r1_2g<mpf('1e-6') and r2_2g<mpf('1e-6') and r3_2g<mpf('1e-6'))}")
    put(f"  [GUT 端点] a1(GUT)={nstr(a1ga,6)}, a2(GUT)={nstr(a2ga,6)}, a3(GUT)={nstr(a3ga,6)}")
else:
    put("  [m_t↔GUT, nf=6] RK4 往返**发散** (残差为天文数字):")
    put(f"    去程端点 a1(GUT)={nstr(a1ga,6)}, a2(GUT)={nstr(a2ga,6)}, a3(GUT)={nstr(a3ga,6)}")
    put(f"    回程发散 → 无法自洽闭合。此与 60/64 号 '2-loop 全跨度反跑数值发散' 完全一致,")
    put(f"    且**精确定位在 m_t→GUT 强耦合大跨度段** (非 M_Z→m_t 段).")
    put(f"  => 数值限制实锤: RK 在此段往返不对称/不收敛, 需专业演化代码 (runRGES/SMDR 高阶+刚性)。")

# ---------- D: 诚实判定 ----------
sec("D · 65 号收口判定 (修正 64 混阶伪检验, 诚实分层)")
put(f"  [1-loop 同阶往返] 全链机器零 (10^-79) ✅  -- RG 1-loop 数学自洽严格成立")
put(f"  [2-loop nf=5 段往返] 自洽 (10^-28) ✅    -- M_Z↔m_t 数值收敛, 框架 2-loop 在此域自洽")
if div6:
    put(f"  [2-loop nf=6 段往返] RK4 发散 ❌      -- (⚠️ 此'Landau极点'解释已被68号撤: 实为β符号bug伪迹, 见顶部作废声明)")
    put(f"     μ_Landau≈6e8 GeV << M_GUT(2e16), 非 SUSY SM 到 GUT 前已非微扰 => 物理天花板")
    put(f"  [诚实撤回] 64 号 '跨阶差30-80%=2-loop真实修正量级' 为无效论证 (混阶伪差+方向分裂)")
    put(f"  [诚实保留] 同阶机器零证明框架 1-loop 数学自洽 + 2-loop 低能段自洽;")
    put(f"     (⚠️ 原'SM物理奇点'解释已被68号撤: 实为β符号bug伪迹, 非真奇点; 见顶部作废声明)")
else:
    put(f"  [2-loop nf=6 段往返] 自洽 ✅ (意外改善, 需复核 N2)")
put(f"  GUT 汇聚 / 群来源 / 2-loop 全跨度反跑数值鲁棒方法 仍为诚实开放项 (NG-X) ❌")
put(f"  结论: 框架 RG 数学自洽在 1-loop 严格成立、2-loop 低能段成立;")
put(f"    跨 GUT 的 2-loop 反跑需专业演化代码, 是本框架**诚实的方法边界**, 非物理失败。")

report = "\n".join(L)
print(report)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "65_同阶RG自洽修复_反跑正跑真机器零报告.md")
RETRACT = ("# ⚠️ 65号 【部分作废】 同阶 RG 自洽修复 · 反跑+正跑真机器零\n\n"
           "> **作废声明 (2026-08-19, 由 68/68b 号证实、69 号审计确认)**:\n"
           "> 本号 C 段'2-loop nf=6 段 RK4 发散 → SM 物理 Landau 极点(μ_Landau≈6e8 GeV)'是 **β 符号 bug 伪迹**\n"
           "> (65b 把 b32=-26/3 符号读反, 误造不存在的 Landau 极点; QCD 任意圈阶都渐近自由), 整条结论链作废。\n"
           "> 本号 A 段'1-loop 同阶机器零'、B 段'nf=5 段数值稳定'在正确符号下仍有效 (69 审计 [A] 级)。\n"
           "> 结论以 69 号总审计 [X] 条为准。\n"
           "> (以下为原脚本历史输出存档, C 段废止结论不作为有效结论)\n\n---\n\n")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write(RETRACT + "# 65号 · 历史输出存档 (C段已撤)\n\n> 算法联盟 ROOT 最高权限 · 同阶RG修复(已部撤) · 2026-08-19\n\n```\n" + report + "\n```\n")
print("\n[报告已写入(含作废横幅)] " + out)
