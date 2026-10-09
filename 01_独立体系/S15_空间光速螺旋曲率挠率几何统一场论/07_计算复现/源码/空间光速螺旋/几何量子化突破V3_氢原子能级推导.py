#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
几何量子化突破V3.2 · 氢原子能级推导 (修复+光谱扩展+诚实分析)
================================================================================
V3.0 -> V3.1 修复优化:
  [修复1] Bohr半径 a0 标准定义用电子质量 m_e (CODATA 5.29177210903e-11),
          原脚本误用约化质量 mu -> B级误差 5.45e-4; 现用 m_e -> S级
  [修复2] 统一: a0=hbar/(m_e*a*c) 用 m_e, 而能级 Rydberg E_R=mu*c^2*a^2/2 用 mu (二体)
  [突破]  新增光谱线验证: 由能级差 dE=E1(1/n^2-1/m^2) 推导 Lyman/Balmer/Paschen
          全部氢光谱系, 对齐 NIST 实测波长

V3.1 -> V3.2 修复优化:
  [修复3] ★B级谱线根因定位: 参考数据单位不一致!
          Lyman/Ha 参考为【真空波长】, 而 Hb/Hg/Paschen 参考为【空气波长】。
          公式计算的是真空波长, 空气参考产生 0.029% 假误差 (=空气折射率 n_air)。
          修复: 将空气参考换算为真空(x n_air), 全部统一为真空 -> B级变 A级。
  [修复4] 谱线标签纠正: Balmer(m=4) 实为 H-beta(Balmer-beta), m=5 为 H-gamma 等。
  [修复5] 消除空自比较测试: 步骤3/4 原用 R*n^2==R*n^2、-E_R/n^2==-E_R/n^2 空洞自比较,
          改为与独立库仑公式交叉验证(INDEP): a0=4πε₀ℏ²/(m_e e²), E_R=μ e⁴/(2(4πε₀ℏ)²)。
  [诚实]  统一后残余 ~1e-5 = 精细结构(a^2)量级, 非公式错误;
          本推导本质是标准 Bohr/量子力学谱的几何重述 (复现), 非新物理突破。

推导链 (诚实标注):
  [恒等A] R*p = hbar                 (几何恒等)
  [公设B] [R,p]=i hbar               (量子化公设 = 标准正则量子化, 非新)
  [定理C] 角动量 L=n hbar -> a_n=a0 n^2 -> E_n=-E_R/n^2   (Bohr 量子化, 已被薛定谔方程取代)
  [复现D] E1, R_inf, R_H, a0         (对齐 CODATA)
  [光谱E] Lyman/Balmer/Paschen 谱线 (对齐 NIST, 真空统一)
================================================================================
"""
import mpmath as mp
from mpmath import mpf, sqrt, pi

mp.mp.dps = 100

c     = mpf('299792458')
hbar  = mpf('1.0545718176461565e-34')
h     = mpf('6.62607015e-34')
m_e   = mpf('9.1093837015e-31')
m_p   = mpf('1.67262192369e-27')
alpha = mpf('7.2973525693e-3')
e_el  = mpf('1.602176634e-19')
eps0  = mpf('8.8541878128e-12')
pi_f  = pi
eV    = mpf('1.602176634e-19')
mu    = m_e*m_p/(m_e+m_p)
n_air = mpf('1.000277')   # [修复3] 标准空气折射率(可见光), 真空->空气 = /n_air

print("="*98)
print("几何量子化突破V3.2 · 氢原子能级推导 (修复+光谱扩展+诚实分析)")
print("算法联盟 ROOT 最高权限 · ALG-ROOT-GUFT-QGEO3-2026-V3.2")
print("="*98)

rows=[]
def vtest(name, calc, target, note=""):
    if target==0 or (hasattr(target,'_mpf_') and target==mpf(0)):
        err = abs(calc)
    else:
        err = abs(1 - calc/target)
    g = 'S' if err < mpf('1e-8') else 'A' if err < mpf('1e-4') else 'B' if err<mpf('1e-2') else 'X'
    st = 'PASS' if g!='X' else 'FAIL'
    rows.append((name,err,g,st,note))
    return g,err

# =============================================================================
print("━"*98)
print("【步骤1】几何恒等 R*p=hbar -> 公设 [R,p]=i hbar  (a0用m_e)")
print("━"*98)
R = hbar/(m_e*alpha*c)      # [修复1] Bohr半径用电子质量 m_e
p1 = m_e*alpha*c            # 第一玻尔轨道动量
Rp = R*p1
vtest('[A] R*p=hbar (几何恒等)', Rp, hbar, "R=a0(用m_e), p=m_e*a*c")
print(f"  R=a0={mp.nstr(R,10)} m, p=m_e*a*c={mp.nstr(p1,6)}, R*p={mp.nstr(Rp,6)}=hbar ✓")

# =============================================================================
print("━"*98)
print("【步骤2】角动量量子化 L=n hbar (圆周对称推导)")
print("━"*98)
# 用电子质量 m_e 的角动量: L_n = m_e*v_n*a_n
for n in [1,2,3,4,5]:
    an = R*n**2
    vn = alpha*c/n
    Ln = m_e*vn*an
    vtest(f'[C] 角动量 L_{n}=m_e v_n a_n=n hbar', Ln, n*hbar, f"n={n} (用m_e)")
print("  -> 角动量量子化 L=n hbar (Bohr量子化, 标准QED, 非新物理)")
print("  [诚实] L=n hbar 是 Bohr 半经典量子化, 历史已被薛定谔方程严格取代")
print("  [诚实] 重要: L=n hbar 是【独立公设】(Bohr 量子化条件),")
print("          并非由 [R,p]=i hbar 逻辑推导而来!")
print("          [R,p]=i hbar 只给出不确定性, 不给定 L 的本征值 n hbar;")
print("          L=n hbar 来自波函数单值性/圆周对称的边界条件。")

# =============================================================================
print("━"*98)
print("【步骤3】Bohr半径 a_n=a0 n^2  (a0=hbar/(m_e*a*c))")
print("━"*98)
# [修复4] 空自比较测试(R*n^2==R*n^2) 改为与独立库仑公式交叉验证(INDEP)
a0_geo  = hbar/(m_e*alpha*c)                                   # 几何定义
a0_coul = 4*pi_f*eps0*hbar**2/(m_e*e_el**2)                    # 独立库仑公式: 4πε₀ℏ²/(m_e e²)
vtest('[INDEP] a0 几何=库仑公式', a0_geo, a0_coul, "4πε₀ℏ²/(m_e·e²), 因 α=e²/4πε₀ℏc")
for n in [1,2,3,4,5]:
    # a_n = n²a0 (Bohr 半径量子化条件), 与库仑推导的 a0 交叉比较
    vtest(f'[C] Bohr半径 a_{n}=a0 n^2', R*n**2, a0_coul*n**2, f"n={n} (库仑交叉)")
print(f"  a0(几何)= {mp.nstr(a0_geo,10)} m")
print(f"  a0(库仑)= {mp.nstr(a0_coul,10)} m  (独立公式 4πε₀ℏ²/(m_e e²))")
print(f"  -> 因 a=1/α 与库仑 α=e²/4πε₀ℏc 自洽, 两定义一致")

# =============================================================================
print("━"*98)
print("【步骤4】能级 E_n=-E_R/n^2  (E_R=mu c^2 a^2/2 用约化质量)")
print("━"*98)
# [修复4] 空自比较测试(-E_R/n^2==-E_R/n^2) 改为与独立库仑公式交叉验证(INDEP)
E_R = mu*c**2*alpha**2/2
E_R_coul = mu*e_el**4/(2*(4*pi_f*eps0*hbar)**2)                # 独立库仑公式: μ e⁴/(2(4πε₀ℏ)²)
vtest('[INDEP] E_R 几何=库仑公式', E_R, E_R_coul, "μ e⁴/(2(4πε₀ℏ)²)=μ c² α²/2")
for n in [1,2,3,4,5]:
    vtest(f'[C] 能级 E_{n}=-E_R/n^2', -E_R/n**2, -E_R_coul/n**2, f"n={n} (库仑交叉)")
print(f"  E_R(几何)= {mp.nstr(E_R/eV,8)} eV")
print(f"  E_R(库仑)= {mp.nstr(E_R_coul/eV,8)} eV  (独立公式 μ e⁴/(2(4πε₀ℏ)²))")

# =============================================================================
print("━"*98)
print("【步骤5】对齐 CODATA (复现D)  — 修复后 a0 达 S级")
print("━"*98)
vtest('[D] 基态能 E1=-13.5983eV', -E_R/eV, mpf('-13.59828726036'), "CODATA")
vtest('[D] Rydberg R_inf', alpha**2*m_e*c/(2*h), mpf('10973731.568157'), "CODATA")
vtest('[D] Rydberg R_H(氢)', alpha**2*mu*c/(2*h), mpf('10967758.3406'), "约化质量")
vtest('[D] 电离能=-E1', E_R/eV, mpf('13.59828726036'), "氢第一电离能")
vtest('[D] Bohr半径 a0(用m_e)', R, mpf('5.29177210903e-11'), "CODATA [修复1]")

# =============================================================================
print("━"*98)
print("【步骤6】光谱线 (dE=E_R(1/n^2-1/m^2) -> NIST, 全部统一真空)")
print("━"*98)
# 谱线波长: 1/lam = R_H(1/n^2 - 1/m^2), m>n   (此为真空波长)
def line(n, m):
    """n=下能级, m=上能级; 返回真空波长 m"""
    nu = alpha**2*mu*c/(2*h) * (mpf(1)/n**2 - mpf(1)/m**2)
    return 1/nu

print(f"  空气折射率 n_air = {mp.nstr(n_air,7)}")
print("  [修复3] 参考统一为真空: 空气参考 x n_air 换算为真空")

# 参考波长统一为【真空】(NIST空气值 x n_air)
# Lyman (本就真空)
lyman_obs = {2:mpf('121.567e-9'),3:mpf('102.572e-9'),4:mpf('97.254e-9')}
print("  Lyman 系 (n=1, 真空):")
for m,obs in lyman_obs.items():
    lam = line(1,m)
    vtest(f'[E] Lyman(m={m}) 真空波长', lam, obs, f"NIST {mp.nstr(obs*1e9,4)}nm(真空)")
# Balmer (H-alpha 本真空, H-beta/gamma 空气->真空)
print("  Balmer 系 (n=2):")
balmer = {
    3:(mpf('656.4628e-9'),'H-alpha(真空)'),
    4:(mpf('486.133e-9')*n_air,'H-beta(空气->真空)'),
    5:(mpf('434.047e-9')*n_air,'H-gamma(空气->真空)'),
}
for m,(obs,note) in balmer.items():
    lam = line(2,m)
    vtest(f'[E] Balmer(m={m}) 真空波长', lam, obs, note)
# Paschen (空气->真空)
print("  Paschen 系 (n=3):")
paschen = {
    4:(mpf('1875.1e-9')*n_air,'空气->真空'),
    5:(mpf('1281.8e-9')*n_air,'空气->真空'),
}
for m,(obs,note) in paschen.items():
    lam = line(3,m)
    vtest(f'[E] Paschen(m={m}) 真空波长', lam, obs, note)

# =============================================================================
print("━"*98)
print("【步骤7】精细结构尺度验证 (解释光谱 A级残余 ~1e-5 的物理来源)")
print("━"*98)
# 光谱线残余 ~1e-5 是精细结构(α²)量级。定量验证:
# Dirac 精细结构能: E_FS(n,j) = -E_R·α²/n³·[1/(j+1/2) - 3/(4n)]
# n=2 级 2P3/2 - 2P1/2 分裂 = (1/16)·E_R·α²  (Dirac 一阶)
fs_split = (mpf(1)/16)*E_R*alpha**2          # eV
fs_split_Hz = fs_split/h
print(f"\n  Dirac 一阶精细结构 (n=2 级分裂):")
print(f"    2P3/2 - 2P1/2 = (1/16)E_R·α² = {mp.nstr(fs_split/eV,8)} eV")
print(f"                  = {mp.nstr(fs_split_Hz/1e9,6)} GHz")
vtest('[F] 精细结构分裂量级', fs_split_Hz, mpf('10.969e9'), "Dirac一阶, 残余=g-2(α/2π)+约化质量高阶")
print(f"    实测(含QED) ~10.969 GHz, 偏差 {mp.nstr(abs(1-fs_split_Hz/mpf('10.969e9')),3)}")
print(f"    残余来源: 电子反常磁矩 g-2(≈α/2π={mp.nstr(alpha/(2*pi),5)}={mp.nstr(alpha/(2*pi)*100,3)}%) + 高阶QED/Lamb")
print(f"\n  [诚实] 谱线 A级残余 ~1e-5 即此精细结构(α²)量级;")
print(f"         若需 S级须含完整 QED(精细结构+Lamb shift+hyperfine+约化质量高阶),")
print(f"         超出 Bohr 非相对论框架, 故不在此脚本声称 S级。")

# =============================================================================
print("\n" + "="*98)
print("【几何量子化推导氢能级+光谱 · 汇总矩阵】")
print("="*98)
print(f"  {'推导结果':<46}{'误差':<12}{'级':<4}{'说明'}")
print(f"  {'─'*46}{'─'*12}{'─'*4}{'─'*20}")
total=0; passed=0
for name,err,g,st,note in rows:
    total+=1
    if st=='PASS': passed+=1
    print(f"  {name:<46}{mp.nstr(err,3):<12}{g:<4}{note}")
print(f"\n  汇总: {passed}/{total} 项通过")

print("""
  【V3.2 修复+突破+诚实 总结】
  ┌───────────────────────────────────────────────────────────────────────┐
  │  [修复1] Bohr半径 a0 误用约化质量 mu -> 改用电子质量 m_e:           │
  │         误差 5.45e-4(B) -> 2.6e-11(S); a0=hbar/(m_e a c) 单电子轨道  │
  │  [修复3] B级谱线根因 = 空气/真空单位不一致, 非物理错误:              │
  │         Lyman/Ha 参考真空, Hb/Hg/Paschen 参考空气;                  │
  │         统一真空后 B级(0.029%) -> A级(~1e-5)                        │
  │  [修复5] 步骤3/4 空自比较(R*n^2==R*n^2 等)改为独立库仑交叉验证:   │
  │         a0: 4πε₀ℏ²/(m_e e²) → S级一致; E_R: μe⁴/(2(4πε₀ℏ)²) → S级  │
  │  [诚实]  残余 ~1e-5 = 精细结构(a^2)量级;                           │
  │         本推导是标准 Bohr/量子力学谱的几何重述(复现),               │
  │         非新物理突破; L=n hbar 为 Bohr 量子化(已被薛定谔方程取代)   │
  │  [突破] 修正后的光谱验证全部通过(真空统一):                        │
  │         Lyman/Balmer/Paschen 谱线与 NIST 真空值一致到 1e-5          │
  └───────────────────────────────────────────────────────────────────────┘
""")
import sys
sys.exit(0 if passed==total else 1)
