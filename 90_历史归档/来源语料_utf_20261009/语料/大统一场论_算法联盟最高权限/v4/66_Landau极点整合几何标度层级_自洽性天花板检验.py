# -*- coding: utf-8 -*-
"""
⚠️ 66号 · 【已作废, 勿重跑】 · 原"Landau 极点整合进几何标度层级"检验
=================================================================================
[作废声明] 本号已被 67 号(统计证伪) + 68 号(β符号bug证实65b错误) 双重撤回 (见 69 号总审计 [X] 条):
  1) 67 号随机对照证伪: 本号 C/C2 段"μ_Landau≈2/5 中位 0.4 候选结构"是选择轴+事后挑简单分数的人为产物,
     单点拟合 + 对 μ_Landau 系数归一化高度敏感(±2x 即消失), 统计不成立。
  2) 68 号证实 65b 的"Landau 极点 μ_Landau≈6e8 GeV"本身是 β 符号 bug 伪结论 (QCD 无 Landau 极点),
     本号 A/B 段依赖的错误 μ_Landau 一并作废。
  [处置] 本号彻底作废; 结论以 69 号审计为准。保留作为"自我证伪/撤回"范式样本。

原 docstring (历史, 仅存档):
接 65b: 非 SUSY SM 2-loop 强耦合有真实 Landau 极点... (详见 65b 作废声明)
"""
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from fractions import Fraction
from mpmath import mp, mpf, pi, log, nstr, sqrt, exp, log10, mpf as m
mp.dps = 50

SIN2   = mpf('0.23129')
ALS_MZ = mpf('0.1179')
AINV_MZ = mpf('127.95')
MZ = mpf('91.1876')
MT = mpf('173.0')
M_GUT = mpf('2e16')
MP = mpf('1.2209e19')   # Planck 质量 GeV

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

# ---- 实验锚 at M_Z, 1-loop 跑到 m_t ----
aEM = 1/AINV_MZ
a1z = (mpf(5)/mpf(3))*aEM/(4*pi)
a2z = aEM/SIN2/(4*pi)
a3z = ALS_MZ/(4*pi)
a1mt = a1z/(1 - f(B1)*a1z*log(MT/MZ))
a2mt = a2z/(1 - f(B2)*a2z*log(MT/MZ))
a3mt = a3z/(1 - f(B3)*a3z*log(MT/MZ))

# ---------- A: 精确定标 μ_Landau ----------
sec("A · 高精度精确定标 μ_Landau (完整 2-loop 三耦合, a3→∞)")

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

# 精细推进, 记录 a3 达到很大值(如 50)时对应的 μ; a3=50 已接近极点(极点处 a3→∞)
# 用极小 dl 从 m_t 推到 a3 突破 50
dl = mpf('0.0005')
a1,a2,a3 = a1mt,a2mt,a3mt
mu = MT
THRESH = mpf('50')
while a3 < THRESH and mu < mpf('1e30'):
    a1,a2,a3 = rk4(a1,a2,a3,dl)
    mu = mu*exp(dl)
muL_full = mu
put(f"  (完整 2-loop 三耦合, 自适应 dl=0.0005, a3 突破 {nstr(THRESH,2)} 时)")
put(f"  μ(a3→{nstr(THRESH,2)}) = {nstr(muL_full,6)} GeV, log10={nstr(log10(muL_full),7)}")
# 解析: 仅 a3 主导 (忽略交叉), 高精度定位极点
abs_b3 = abs(f(B3)); abs_b32 = abs(f(B32))
def integrand(a): return 1.0/(abs_b3*a*a + abs_b32*a*a*a)
tL = mp.quad(lambda a: integrand(mpf(a)), [a3mt, mpf('1e10')])
muL_ana = MT*exp(tL)
put(f"  解析(仅 a3 主导) μ_Landau = {nstr(muL_ana,6)} GeV, log10={nstr(log10(muL_ana),7)}")
put(f"  完整数值 vs 解析: {nstr(muL_full/muL_ana,4)} (交叉项 a1,a2 贡献 ~{nstr(abs(1-muL_full/muL_ana)*100,2)}%)")
put(f"  => μ_Landau 精确值 ~ 10^{nstr(log10(muL_ana),4)} GeV, 量级区间 [10^8.7, 10^8.8]")

# ---------- B: 框架质量标度层级盘点 ----------
sec("B · 几何框架质量标度层级 (对数轴结构检验)")
# 关键质量标度 (GeV): 电弱, top, Landau, GUT, Planck
scales = [
    ("电弱(M_Z)",   MZ),
    ("顶夸克(m_t)", MT),
    ("Landau极点",  muL_ana),
    ("GUT(M_GUT)",  M_GUT),
    ("Planck(m_P)", MP),
]
logsc = [(nm, log10(mu0)) for nm, mu0 in scales]
put(f"  {'标度':<12}{'μ(GeV)':<14}{'log10':<10}")
for nm, lg in logsc:
    put(f"  {nm:<12}{nstr(scales[[x[0] for x in scales].index(nm)][1],6):<14}{nstr(lg,6):<10}")
# 相邻层级对数间隔
put(f"\n  相邻层级对数间隔 Δlog10 (是否呈现几何/整数关系?):")
deltas = [(logsc[i+1][0], logsc[i+1][1]-logsc[i][1]) for i in range(len(logsc)-1)]
for nm, d in deltas:
    put(f"    {nm:<14} Δ={nstr(d,5)}  (比={nstr(d/mpf('3'),4)}×3, {nstr(d/mpf('4'),4)}×4)")
# 全跨度对数比: Landau 在整个质量谱的"位置参数"
Lw = log10(MZ); LL = log10(muL_ana); LG = log10(M_GUT); LP = log10(MP)
put(f"\n  几何位置参数 (Landau 在质量谱对数轴的位置):")
put(f"    log10(μ_Landau/M_Z) = {nstr(LL-Lw,5)}   (电弱→Landau)")
put(f"    log10(M_GUT/μ_Landau) = {nstr(LG-LL,5)} (Landau→GUT)")
put(f"    log10(m_P/M_GUT) = {nstr(LP-LG,5)}      (GUT→Planck)")
put(f"    log10(m_P/M_Z) = {nstr(LP-Lw,5)}        (全跨度电弱→Planck)")
# 检验几何关系: 是否 log10(m_P/M_Z) ≈ 17 (已知 Planck/电弱≈10^17), Landau 是否恰在中位?
mid_electroweak_planck = (Lw+LP)/2
put(f"\n  [几何检验] Landau 是否位于电弱-Planck 中位附近?")
put(f"    中位 log10 = (log10M_Z+log10m_P)/2 = {nstr(mid_electroweak_planck,5)}")
put(f"    Landau log10 = {nstr(LL,5)}; 偏差 = {nstr(LL-mid_electroweak_planck,4)}")
put(f"    (若≈0 => Landau 恰在中位, 高度非平凡几何结构; 否则只是测量锚)")

# ---------- C: 诚实判定 ----------
sec("C · 判定: μ_Landau 是框架预言还是测量锚?")
# 计算 Landau 相对电弱-Planck 中位的分数位置
frac_pos = (LL-Lw)/(LP-Lw)
put(f"  Landau 在电弱→Planck 对数轴的**分数位置** = {nstr(frac_pos,5)}")
put(f"    0=电弱, 1=Planck; 若≈1/2(中位)或≈其它简单有理数 => 几何结构;")
put(f"    若无简单有理 => 测量锚(如 m_e, 同属 NG-X)。")
# 检查是否接近常见简单分数
for num in [mpf('1')/mpf('2'), mpf('1')/mpf('3'), mpf('2')/mpf('5'), mpf('1')/mpf('4')]:
    put(f"    对 {nstr(num,3)}: 偏差 {nstr(abs(frac_pos-num),4)}")
# 决定
nearest = None; best = mpf('9')
for num in [mpf('1')/mpf('2'), mpf('1')/mpf('3'), mpf('2')/mpf('5'), mpf('1')/mpf('4')]:
    d0 = abs(frac_pos-num)
    if d0 < best: best = d0; nearest = num
put(f"\n  最接近简单分数: {nstr(nearest,3)} (偏差 {nstr(best,4)})")

# ---------- C2: 鲁棒性检验 (0.4 结构是否对 μ_Landau 系数依赖敏感?) ----------
sec("C2 · 鲁棒性检验: 0.4 候选结构是否对 μ_Landau 不确定区间稳定?")
Lw = log10(MZ); LP = log10(MP); span = LP-Lw
put(f"  电弱 log10={nstr(Lw,4)}, Planck log10={nstr(LP,4)}, 全跨度={nstr(span,4)}")
put(f"  若 0.4 结构成立, 要求 frac_pos≈0.4 → log10(μ_Landau)=Lw+0.4·span={nstr(Lw+mpf('0.4')*span,5)}")
put(f"  实际 log10(μ_Landau)={nstr(LL,5)} → 对 0.4 偏差={nstr(abs(frac_pos-mpf('0.4')),5)}")
# 扫描 μ_Landau 在合理区间 [3e8, 5e9] (log10 8.48~9.70) 的 frac_pos 变化
put(f"  扫描 μ_Landau 在物理合理区间 (系数归一化±量级) 对 0.4 位置的敏感度:")
samples = [mpf('3e8'), mpf('6e8'), mpf('1e9'), mpf('2e9'), mpf('5e9'), mpf('1e10')]
for s in samples:
    fp = (log10(s)-Lw)/span
    mark = " ★0.4" if abs(fp-mpf('0.4'))<mpf('0.02') else ""
    put(f"    μ_Landau={nstr(s,3)} GeV (log10={nstr(log10(s),5)}): frac_pos={nstr(fp,5)} (偏差0.4={nstr(abs(fp-mpf('0.4')),5)}){mark}")
put(f"  [诚实] 仅 μ_Landau≈(5-7)e8 GeV 时 0.4 成立; μ_Landau 系数归一化若偏移>2x,")
put(f"    0.4 结构即消失。单数据点+高敏感度 => **过拟合风险高**, 不能据此断言层级几何律。")

# 最终判定
put(f"\n  [最终判定] Landau 分数位置≈0.398 (最接近 2/5=0.4, 偏差 0.16%):")
put(f"    - 是**值得记录的候选结构**: 若框架存在质量层级几何律, Landau 应落简单分数位")
put(f"    - 但**不构成证明**: 单点拟合, 且对 μ_Landau 系数归一化高度敏感(见 C2)")
put(f"    - 诚实定级: **候选整合点 (待严格 2-loop+阈值定标与多标度验证)**, 非几何派生")
put(f"  [诚实边界] μ_Landau 精确值依赖 2-loop 系数归一化(±量级内), 此处为 MV GUT 归一化估值;")
put(f"    框架未从第一性原理推出 μ_Landau; 本号只做**事后整合检验**, 不伪称派生。")

report = "\n".join(L)
print(report)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "66_Landau极点整合几何标度层级_自洽性天花板检验报告.md")
RETRACT = ("# ⚠️ 66号 【已作废】 Landau 极点整合进几何标度层级\n\n"
           "> **作废声明 (2026-08-19, 由 67 号证伪 + 68 号证实, 69 号审计确认)**:\n"
           "> - 本号 C/C2 段'μ_Landau≈2/5 中位 0.4 候选结构'被 67 号随机对照证伪 (选择轴+事后挑分数, 过拟合);\n"
           "> - 本号 A/B 段依赖的'Landau 极点 μ_Landau≈6e8 GeV'被 68 号证实是 65b 的 β 符号 bug 伪结论 "
           "(QCD 任意圈阶都渐近自由, 无 Landau 极点), 一并作废。\n"
           "> **本号彻底作废**, 结论以 69 号总审计 [X] 条为准。\n"
           "> (以下为原脚本历史输出存档, 仅供反例研究, 不作为有效结论)\n\n---\n\n")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write(RETRACT + "# 66号 · 历史输出存档 (已作废)\n\n> 算法联盟 ROOT 最高权限 · 整合检验(已撤) · 2026-08-19\n\n```\n" + report + "\n```\n")
print("\n[报告已写入(含作废横幅)] " + out)
