# -*- coding: utf-8 -*-
"""
67号 · 全标度对数轴几何律检验 · 随机对照证伪测试
=================================================================================
66 号发现 μ_Landau 在 [M_Z, m_P] 对数轴的分数位置≈0.398≈2/5 (候选结构)。
本号做**科学的可证伪检验**: 把框架所有独立质量/能量标度纳入, 检验是否存在
统一的层级几何律 (多个标度落在简单分数位), 并做随机对照统计以区分:
  真实几何结构  vs  过拟合巧合 (简单分数很多, 任何随机点都可能在某个分数附近)。

方法:
  [A] 收集框架所有独立标度 (粒子谱 e/μ/τ/π/p/t + 电弱 + 暗物质 + Landau + GUT + Planck)
  [B] 固定轴定义, 计算每个标度的分数位置 frac_pos=(logμ-logμ_lo)/(logμ_hi-logμ_lo)
  [C] 对每个标度找最近简单分数(分母≤10), 报告偏差
  [D] **随机对照**: 生成 N 组随机标度(同轴内均匀对数分布), 统计'命中简单分数位'比例,
      与真实数据命中率对比 => 若真实命中率显著高于随机 => 支持几何律; 否则证伪
  [E] **轴鲁棒性**: 换轴定义([m_e,m_P] 等)看 Landau 的 2/5 位置是否稳定
      若换轴即变 => 2/5 是轴依赖伪结构; 若稳定 => 更可信

诚实边界: 本号目的=证伪/确证 66 候选; 结论只报告统计事实, 不预设框架成立。
"""
import sys, io, os, random
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from fractions import Fraction
from mpmath import mp, mpf, pi, log, nstr, log10, exp
mp.dps = 40

MZ  = mpf('91.1876')
MP  = mpf('1.2209e19')
MEV = mpf('1e-3')   # GeV

def ok(b): return "[OK] PASS" if b else "[X] FAIL"
L = []
def sec(t): L.append("\n" + "=" * 74); L.append("  " + t); L.append("=" * 74)
def put(s=""): L.append(s)

# ---------- 框架所有独立标度 (GeV) ----------
# (名称, 质量/能量 GeV, 来源)
SCALES = [
    ("电子 e⁻",      mpf('0.51099895000')*MEV, "PDG"),
    ("μ子 μ⁻",       mpf('105.6583755')*MEV,   "PDG"),
    ("τ子 τ⁻",       mpf('1776.86')*MEV,       "PDG"),
    ("π± 介子",      mpf('139.57039')*MEV,     "PDG"),
    ("质子 p",       mpf('938.27208816')*MEV,  "PDG"),
    ("W± 玻色子",    mpf('80369.2')*MEV,        "PDG"),
    ("Z⁰ 玻色子",    mpf('91187.6')*MEV,        "PDG"),
    ("顶夸克 t",     mpf('173.0'),             "PDG"),
    ("暗物质 m_DM",  mpf('1.678'),             "34/37预言"),
    ("Landau极点",   mpf('6.0626e8'),          "65b"),
    ("GUT M_GUT",    mpf('2e16'),              "SM假设"),
    ("Planck m_P",   mpf('1.2209e19'),         "定义"),
]
# 所有简单分数 分母<=10
def simple_fractions(maxden=10):
    fs = []
    for d in range(2, maxden+1):
        for n in range(1, d):
            fs.append((n, d, mpf(n)/mpf(d)))
    return fs
SIMPLE = simple_fractions(10)

# ---------- A/B/C: 主检验轴 [M_Z, m_P] ----------
sec("A/B/C · 主检验轴 [M_Z, m_P] 全标度分数位置")
lo, hi = MZ, MP
span = log10(hi)-log10(lo)
def frac_pos(mu): return (log10(mu)-log10(lo))/span
def nearest_simple(fp):
    best = None; bd = mpf('9')
    for n,d,v in SIMPLE:
        d0 = abs(fp-v)
        if d0 < bd: bd = d0; best = (f"{n}/{d}", v, bd)
    return best
put(f"  轴: [log10 M_Z={nstr(log10(lo),4)}, log10 m_P={nstr(log10(hi),4)}], 跨度={nstr(span,4)}")
put(f"  {'标度':<12}{'μ(GeV)':<13}{'log10':<9}{'frac_pos':<10}{'最近简单分数':<14}{'偏差':<10}")
axis_inside = []
for nm, mu, src in SCALES:
    fp = frac_pos(mu)
    ns, nsv, nd = nearest_simple(fp)
    # 仅报告轴内 (fp in [0,1]) 或最接近
    inside = mpf(0) <= fp <= mpf(1)
    if inside: axis_inside.append((nm, mu, fp, ns, nd))
    put(f"  {nm:<12}{nstr(mu,6):<13}{nstr(log10(mu),7):<9}{nstr(fp,8):<10}{ns+('' if inside else '(轴外)'):<14}{nstr(nd,6):<10}")

# ---------- D: 随机对照 ----------
sec("D · 随机对照: 真实命中率 vs 随机命中率")
# 定义'命中': 最近简单分数偏差 < 阈值 (如 0.02)
th = mpf('0.02')
def hit_rate(samples_fp):
    h = 0
    for fp in samples_fp:
        if mpf(0)<=fp<=mpf(1):
            ns,nsv,nd = nearest_simple(fp)
            if nd < th: h += 1
    return h
real_fps = [frac_pos(mu) for nm,mu,src in SCALES]
real_hits = hit_rate(real_fps)
put(f"  命中阈值: 最近简单分数偏差<{nstr(th,3)}")
put(f"  真实数据: 轴内标度命中率 = {real_hits}/{len(SCALES)} = {nstr(real_hits*mpf(100)/len(SCALES),2)}%")
# 随机对照: 生成 10000 组随机标度, 每组同样数量, 统计平均命中率
random.seed(42)
Ntrials = 2000
rand_hit_sum = 0; rand_hit_axis = 0
for _ in range(Ntrials):
    # 随机生成 len(SCALES) 个对数均匀标度, 覆盖 log10(lo)-log10(hi) 全跨度
    fps = []
    for i in range(len(SCALES)):
        r = random.random()
        fps.append(r)   # 均匀 [0,1] 相当于对数均匀在轴上
    rand_hit_sum += hit_rate(fps)
    rand_hit_axis += 1
rand_avg = rand_hit_sum/Ntrials
put(f"  随机对照: {Ntrials} 组, 平均命中数 = {nstr(rand_avg,4)} (命中率 {nstr(rand_avg*mpf(100)/len(SCALES),2)}%)")
put(f"  [统计判定] 真实轴内命中 {real_hits} vs 随机平均 {nstr(rand_avg,3)}:")
if real_hits > rand_avg + 2:
    put(f"    => 真实命中显著高于随机 (+{nstr(real_hits-rand_avg,2)}), 支持几何律信号 (需更多标度复核)")
elif real_hits > rand_avg:
    put(f"    => 真实命中略高于随机 (+{nstr(real_hits-rand_avg,2)}), 弱信号, 不足以断言")
else:
    put(f"    => 真实命中率不高于随机, 66 候选**不具统计显著性**, 诚实证伪")

# ---------- E: 轴鲁棒性 ----------
sec("E · 轴鲁棒性: Landau 的 2/5 位置是否随轴定义变化?")
# 用不同轴下界检验 Landau 位置
for nm_lo, v_lo in [("M_Z=91.19", MZ), ("m_t=173", mpf('173')), ("m_e=0.511MeV", mpf('0.511')*MEV), ("暗物质=1.68", mpf('1.678'))]:
    lo2, hi2 = v_lo, MP
    span2 = log10(hi2)-log10(lo2)
    fpL = (log10(mpf('6.0626e8'))-log10(lo2))/span2
    fpG = (log10(mpf('2e16'))-log10(lo2))/span2
    put(f"  轴 [log10{nm_lo}, m_P]: Landau frac={nstr(fpL,5)} (偏差0.4={nstr(abs(fpL-mpf('0.4')),5)}), GUT frac={nstr(fpG,5)}")
put(f"  [诚实] 若 Landau 的 2/5 位置对轴下界敏感 => 轴依赖伪结构;")
put(f"  仅当在多轴下都稳定接近同一简单分数 => 才可能是真几何律。")

# ---------- F: 判定 ----------
sec("F · 67 号判定 (证伪/确证 66 候选)")
put(f"  66 号候选 'μ_Landau≈2/5' 的证伪检验:")
put(f"    D 随机对照: 真实命中率 vs 随机命中率 (见上)")
put(f"    E 轴鲁棒性: 2/5 是否对轴定义稳定 (见上)")
put(f"  结论按统计事实诚实判定, 不预设框架成立; 若证伪则撤回候选, 若弱信号则降级'待更多标度'。")

report = "\n".join(L)
print(report)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "67_全标度对数轴几何律检验_随机对照证伪测试报告.md")
with io.open(out, "w", encoding="utf-8") as fh:
    fh.write("# 67号 · 全标度对数轴几何律检验 · 随机对照证伪测试\n\n> 算法联盟 ROOT 最高权限 · 可证伪检验 · 2026-08-19\n\n```\n" + report + "\n```\n")
print("\n[报告已写入] " + out)
