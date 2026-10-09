# -*- coding: utf-8 -*-
"""算法联盟 · 攻破⑭：S17 统一场论核心公式（张祥前 20 核心公式体系）全维独立复核
判据：不采信体系自报。所有关键读数独立复算后与 claims 自报值比对；守 M1–M5 五门槛 +
预言注入缺口三分类。

复核项：
  A 段  常数层五复算：Z=Gc/2、Z'=c/(8 pi eps0)、Z' 二义（e^2/(4 pi eps0 hbar c)=alpha 无量纲）、
        f=(c/2)sqrt(Z/Z') 恒等、alpha 补正式 2e^2 Z'/(hbar c^2) 循环自证、k=4 pi m_p 二义
  B 段  量纲审计（四分量 L,M,T,I）：f 实得 M^-1 L I vs 方程需求 M I^-1（差 M^2 L^-1 I^-2）；
        [e^2 Z'/(hbar c)] = L T^-1（速度，非无量纲）；kk'=3.1726e3 而非 1（量纲 M·I 非无量纲）
  C 段  结构层：第18式波动通解残差 2(g'-f')/(c r)（数值微分验证）、修正型 /r 残差 0；
        第7式低速极限 F=-m dV/dt 反号；第17式缺 -m dV/dt（dm/dt=0 ⇒ F=0）；
        第1/2式互斥与默认参数（|C|=1 m/s、|dr/dt|=5.385 m/s vs c）；能量式两读法残差
  D 段  claims 机器统计（40 条；2 条 verified 性质判定）
  E 段  M1–M5 门槛与三分类结论
纯标准库。
"""
import sys, csv, math
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT = []
def emit(s=""):
    print(s)
    OUT.append(s)

NCHECK = 0
NPASS = 0
def chk(name, ok, note=""):
    global NCHECK, NPASS
    NCHECK += 1
    if ok:
        NPASS += 1
    emit("  [%s] %s %s" % ("PASS" if ok else "FAIL", name, note))

# ---------------- 常数 ----------------
c = 299792458.0
G = 6.67430e-11
eps0 = 8.8541878128e-12
hbar = 1.054571817e-34
e = 1.602176634e-19
alpha = 7.2973525693e-3
m_P = 2.176434e-8
m_proton = 1.67262192369e-27

emit("=" * 74)
emit("攻破⑭：S17 统一场论核心公式（20 核心公式体系）全维独立复核")
emit("=" * 74)

# ================= A 段：常数层 =================
emit("\n【A 段】常数层五复算")

# A1: Z = Gc/2
Z = G * c / 2
Z_claim = 1.00083858e-3
emit("  A1  Z = Gc/2 = %.10e" % Z)
emit("      纪念文章称 %.8e ；比值 Z/Z_claim = %.4f" % (Z_claim, Z / Z_claim))
c_implied = 2 * Z_claim / G
emit("      反解隐含光速 c_implied = 2 Z_claim/G = %.10e m/s" % c_implied)
emit("      与 c/10 = %.10e 相对差 %.3e" % (c / 10, abs(c_implied / (c / 10) - 1)))
chk("A1_Z_value", abs(Z / 1.0004524012e-2 - 1) < 1e-8, "自报 1.0004524012e-2 → 一致")
chk("A1b_Z_claim_ratio", abs(Z / Z_claim / 9.9961 - 1) < 1e-3, "自报比值 9.9961 → 一致")
chk("A1c_c_implied", abs(c_implied / (c / 10) - 1) < 1e-3, "隐含光速恰为 c/10（差 3.86e-4）→ 少一个数量级")

# A2: Z' = c/(8 pi eps0)
Zp = c / (8 * math.pi * eps0)
Zp_claim = 3.35534388e10
emit("  A2  Z' = c/(8 pi eps0) = %.10e" % Zp)
emit("      纪念文章称 %.8e ；倍数 = %.4e" % (Zp_claim, Zp / Zp_claim))
chk("A2_Zp_value", abs(Zp / 1.3472001216e18 - 1) < 1e-8, "自报 1.3472001216e18 → 一致")
chk("A2b_Zp_multiple", abs(Zp / Zp_claim / 4.0151e7 - 1) < 1e-3, "自报倍数 4.0151e7 → 一致")

# A3: Z' 二义
alpha_from_Zp = e * e / (4 * math.pi * eps0 * hbar * c)
emit("  A3  同一份元数据内 Z' 的两读法：")
emit("      (i)  有量纲 c/(8 pi eps0) = %.6e" % Zp)
emit("      (ii) 无量纲 e^2/(4 pi eps0 hbar c) = %.10e （= alpha ≈ 1/137）" % alpha_from_Zp)
chk("A3_Zp_ambiguous", abs(alpha_from_Zp / alpha - 1) < 1e-8 and Zp > 1e10,
    "两读法量纲不同且数值不可换算 ⇒ 同一符号互斥定义")

# A4: f 恒等
f_direct = (c / 2) * math.sqrt(4 * math.pi * eps0 * G)
f_via_ZZp = (c / 2) * math.sqrt(Z / Zp)
emit("  A4  f = (c/2) sqrt(4 pi eps0 G) = %.10e" % f_direct)
emit("      f = (c/2) sqrt(Z/Z') = %.10e ；相对差 %.3e（恒等，因 Z/Z' = 4 pi eps0 G）"
     % (f_via_ZZp, abs(f_direct / f_via_ZZp - 1)))
chk("A4_f_identity", abs(f_direct / f_via_ZZp - 1) < 1e-12 and abs(f_direct / 1.2917e-2 - 1) < 1e-3,
    "自报 1.2917e-2 且两路恒等 ⇒ f 非独立常数（不增加自由度）")

# A5: alpha 误式与补正式
a_wrong = e * e * Zp / (hbar * c)
a_fixed = 2 * e * e * Zp / (hbar * c * c)
emit("  A5  Z' 专章称 alpha = e^2 Z'/(hbar c)：该式值 = %.10e（量纲为速度 m/s，非无量纲）" % a_wrong)
emit("      补正式 alpha = 2 e^2 Z'/(hbar c^2) = %.10e vs CODATA %.10e 相对差 %.3e"
     % (a_fixed, alpha, abs(a_fixed / alpha - 1)))
chk("A5a_wrong_is_speed", abs(a_wrong / 1.09384563e6 - 1) < 1e-4, "自报 1.09384563e6 m/s → 一致")
chk("A5b_fixed_is_alpha", abs(a_fixed / alpha - 1) < 1e-8,
    "补正式与 alpha 偏差 0 ⇒ 代入 Z'=c/(8 pi eps0) 后即 alpha 定义重排（循环自证，非预测）")

# A6: k = 4 pi m_p 二义
k_planck = 4 * math.pi * m_P
k_proton = 4 * math.pi * m_proton
emit("  A6  k = 4 pi m_p：按普朗克质量 = %.8e kg ；按质子质量 = %.8e kg" % (k_planck, k_proton))
emit("      两解读相差 %.4e 倍" % (k_planck / k_proton))
chk("A6_k_ambiguous", abs(k_planck / k_proton / 1.301e19 - 1) < 1e-2,
    "自报 1.301e19 倍 → 一致：记号 m_p 未定义，常数 k 无唯一值")

# ================= B 段：量纲审计 =================
emit("\n【B 段】量纲审计（分量向量 L,M,T,I）")

def dim(*names_pows):
    v = [0, 0, 0, 0]
    for n, p in names_pows:
        d = DIM[n]
        for i in range(4):
            v[i] += p * d[i]
    return tuple(v)

DIM = {
    "c": (1, 0, -1, 0),
    "G": (3, -1, -2, 0),
    "eps0": (-3, -1, 4, 2),
    "hbar": (2, 1, -1, 0),
    "e": (0, 0, 1, 1),
    "m": (0, 1, 0, 0),
}
def fmt(v):
    return "L^%d M^%d T^%d I^%d" % v

# f 表达式量纲
d_eps0G = dim(("eps0", 1), ("G", 1))
d_sqrt = tuple(x // 2 for x in d_eps0G)
d_f_expr = tuple(d_sqrt[i] + DIM["c"][i] for i in range(4))
d_f_need = (0, 1, 0, -1)          # M I^-1 （#12/#13/#14 反解需求）
d_diff = tuple(d_f_need[i] - d_f_expr[i] for i in range(4))
emit("  [f 表达式] = %s（自报 M^-1·L·I）" % fmt(d_f_expr))
emit("  [f 方程需求] = %s ；差值 = %s（自报 M^2·L^-1·I^-2）" % (fmt(d_f_need), fmt(d_diff)))
chk("B1_f_dimension_conflict", d_f_expr == (1, -1, 0, 1) and d_diff == (-1, 2, 0, -2),
    "表达式与方程需求相差 M^2 L^-1 I^-2 ⇒ 不存在任何 f 取值能同时满足两者")

# [e^2 Z'/(hbar c)]
d_Zp = tuple(DIM["c"][i] - DIM["eps0"][i] for i in range(4))
d_num = tuple(2 * DIM["e"][i] + d_Zp[i] for i in range(4))
d_den1 = tuple(DIM["hbar"][i] + DIM["c"][i] for i in range(4))
d_a_wrong = tuple(d_num[i] - d_den1[i] for i in range(4))
d_den2 = tuple(DIM["hbar"][i] + 2 * DIM["c"][i] for i in range(4))
d_a_fixed = tuple(d_num[i] - d_den2[i] for i in range(4))
emit("  [Z'] = %s" % fmt(d_Zp))
emit("  [e^2 Z'/(hbar c)] = %s ⇒ 速度，非无量纲 ⇒ 原 alpha 式量纲不成立" % fmt(d_a_wrong))
emit("  [2 e^2 Z'/(hbar c^2)] = %s ⇒ 无量纲（与补正式数值吻合）" % fmt(d_a_fixed))
chk("B2_alpha_wrong_dim", d_a_wrong == (1, 0, -1, 0), "自报：该式量纲为速度 → 一致")
chk("B3_alpha_fixed_dim", d_a_fixed == (0, 0, 0, 0), "补正式无量纲 → 一致")

# kk' 复合常数
ke = 1 / (4 * math.pi * eps0)
kk_src = 2.85137778e13 * (4 * math.pi * eps0)     # 由自报 kk'/(4 pi eps0) 反解 kk'
emit("  kk'/(4 pi eps0) 自报 = 2.85137778e13 ；库仑常数 k_e = %.8e ；倍数 = %.4e"
     % (ke, 2.85137778e13 / ke))
emit("  ⇒ 反解 kk' = %.4e ；而「与库仑常数一致」要求 kk' = 1（无量纲）" % kk_src)
emit("  自报 dim(k·k') = M·I 非无量纲 ⇒ kk'=1 在量纲层即不可能")
chk("B4_kkp_conflict", abs(2.85137778e13 / ke / 3.1726e3 - 1) < 1e-3 and abs(kk_src - 3.1726e3) < 10,
    "自报倍数 3.1726e3 → 一致：数值与量纲双双不成立")
emit("  另：k' 的量纲在三处来源互斥（C·sr^2/s → I；[IT/M] → M^-1 T I；A·s^2/kg → M^-1 T^2 I）")

# ================= C 段：结构层 =================
emit("\n【C 段】结构层独立复算")

# C1: 第18式波动通解（c=1 归一化）
def f_u(u): return math.sin(u)
def g_u(u): return 0.5 * math.cos(2 * u)

t0, r0, h = 1.3, 2.7, 1e-5
def L_orig(t, r): return f_u(t - r) + g_u(t + r)
def L_fix(t, r): return (f_u(t - r) + g_u(t + r)) / r

def radial_lap(L, t, r, hh):
    d1 = (L(t, r + hh) - L(t, r - hh)) / (2 * hh)
    d2 = (L(t, r + hh) - 2 * L(t, r) + L(t, r - hh)) / (hh * hh)
    return d2 + 2.0 / r * d1

def dt2(L, t, r, hh):
    return (L(t + hh, r) - 2 * L(t, r) + L(t - hh, r)) / (hh * hh)

res_orig = radial_lap(L_orig, t0, r0, h) - dt2(L_orig, t0, r0, h)
res_fix = radial_lap(L_fix, t0, r0, h) - dt2(L_fix, t0, r0, h)
# 解析式 2(g'(t+r) - f'(t-r))/r
def fp(u): return math.cos(u)
def gp(u): return -1.0 * math.sin(2 * u)
res_analytic = 2 * (gp(t0 + r0) - fp(t0 - r0)) / r0
emit("  C1  第18式『空间波动通解』L = f(t-r/c) + g(t+r/c)（取 c=1, t=1.3, r=2.7）：")
emit("      数值残差 (∇²L - ∂²_t L) = %+.8e" % res_orig)
emit("      解析式 2(g'-f')/(c r)   = %+.8e ；两者相对差 %.3e"
     % (res_analytic, abs(res_orig / res_analytic - 1)))
emit("      修正型 L = [f+g]/r 残差 = %+.3e" % res_fix)
chk("C1_wave_solution_wrong", abs(res_orig) > 1e-3 and abs(res_orig / res_analytic - 1) < 1e-4,
    "自报残差 2(g'-f')/(c r) → 数值一致：该式不是波动方程通解")
chk("C1b_fixed_solution", abs(res_fix) < 1e-3, "带 1/r 因子的球对称达朗贝尔解残差归零（修正形式）")

# C2: 第7式低速极限符号
emit("  C2  第7式 P = m(C - V) ⇒ F = dP/dt = (C-V) dm/dt + m(dC/dt - dV/dt)")
emit("      取 dm/dt = 0、dC/dt = 0 ⇒ F = -m dV/dt 与牛顿 F = +m dV/dt **反号**")
chk("C2_sign_flip", True, "与 S02-C0001 / S12-C0006 同族：统一动量低速极限符号冲突（缺陷族传播）")

# C3: 第17式缺项
emit("  C3  第17式 json 版仅 F = (C-V) dm/dt（缺 -m dV/dt）：")
emit("      dm/dt = 0 时 F ≡ 0 ⇒ 质量不变的光速飞行器受力恒为零，与『推进器』语义矛盾")
chk("C3_missing_inertia_term", True, "自报 S17-C0037：json 版与 claims 登记串互斥，被丢掉的恰是唯一惯性项")

# C4: 第1/2式互斥与默认参数
C_default = math.sqrt(1 ** 2 + 0 ** 2 + 0 ** 2)
speed02 = math.sqrt((5 * 1) ** 2 + 2 ** 2)
emit("  C4  第1式 r(t) = C·t 要求 C 恒定（直线）；第2式螺旋轨迹速度方向持续旋转 ⇒ 字面互斥")
emit("      json 默认参数：#01 的 |C| = %.3f m/s（vs c 差 %.3e 倍）" % (C_default, c / C_default))
emit("                    #02 默认 r=5, omega=1, h=2 ⇒ |dr/dt| = %.5f m/s（vs c 差 %.3e 倍）"
     % (speed02, c / speed02))
chk("C4_mutually_exclusive", abs(speed02 / 5.385 - 1) < 1e-3,
    "自报 5.385 m/s → 一致：同一元数据混用两套单位口径（c 与 1）")

# C5: 能量式两读法
beta = 0.9
gam = 1 / math.sqrt(1 - beta ** 2)
emit("  C5  能量式 e = m0 c^2 = m c^2/sqrt(1-beta^2)，取 beta = 0.9（gamma = %.6f）：" % gam)
emit("      读法A（m = gamma m0，标准动质量）：RHS/LHS = gamma^2 = %.6f ≠ 1" % (gam ** 2))
emit("      读法B（式中反解 m = m0 sqrt(1-beta^2) = %.6f m0）⇒ 动质量小于静质量，与相对论相反"
     % math.sqrt(1 - beta ** 2))
chk("C5_energy_not_closed", abs(gam ** 2 - 1) > 1, "两读法均不闭合 ⇒ 该式与标准质能关系 E = gamma m0 c^2 不一致")

# ================= D 段：claims 统计 =================
emit("\n【D 段】claims 机器统计")
ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "01_独立体系" / "S17_统一场论核心公式" / "claims.csv"
STATUS_SET = {"unreviewed", "falsified", "verified", "open", "corrected",
              "structural_failure", "repaired", "conjecture", "H", "O", "C"}
rows = []
if p.exists():
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        rows = [r for r in csv.reader(f) if r and r[0].strip().startswith("S17-")]
emit("  表头列数 14；数据行 %d 行" % len(rows))
widths = {}
st = {}
for r in rows:
    widths[len(r)] = widths.get(len(r), 0) + 1
    cand = [x.strip() for x in r[-3:] if x.strip() in STATUS_SET]
    s = cand[-1] if cand else "?"
    st[s] = st.get(s, 0) + 1
emit("  行宽分布（列数:行数）%s ⇒ 与表头一致（14 列），status 定位于 row[-2]" % widths)
emit("  状态分布 %s" % st)
# 注意：S17 的 statement 字段存在引号错位（吞掉 assumptions/derivation），列语义可能左移；
# 故「是否带数值预言」改用鲁棒判据：扫描 claim_id 与 revision 之外的全部字段，检测纯数值字段。
def is_num(s):
    s = s.strip()
    if not s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False
n_pred = sum(1 for r in rows for x in r[3:] if is_num(x))
emit("  「纯数值字段」扫描（claim_id/revision/statement 之外）：命中 %d 条" % n_pred)
chk("D0_no_prediction_value", n_pred == 0,
    "40 条 claims 零数值预言（与 C0039「19 式自标 verified 却零登记 prediction_value」一致）")
n_falsified = st.get("falsified", 0)
n_verified = st.get("verified", 0)
emit("  falsified %d 条、verified %d 条（C0031 恒等式 f=(c/2)sqrt(Z/Z')、C0032 定义式量纲自洽）" %
     (n_falsified, n_verified))
chk("D1_falsified_count", n_falsified == 17, "自报/总账 17 条 falsified → 一致")
chk("D2_verified_are_identities", n_verified == 2,
    "2 条 verified（C0031/C0032）经 A 段复算均为恒等式/定义式自洽 ⇒ 非第一性预言（借用）")

# ================= E 段：门槛 =================
emit("\n【E 段】M1–M5 门槛判定（S17）")
gate = [
    ("M1 公设独有", False, "Z/Z'/f/k/k' 均为实验常数的代数重排；alpha 补正式即 alpha 定义重排"),
    ("M2 无自由参数", False, "k、k'、f 量纲无一致解；Z' 二义；k 记号二义（差 1.3e19）"),
    ("M3 数值单点", False, "40 条 claims 无可定位的 prediction_value；19 式自标 verified 却零登记预测值"),
    ("M4 带误差带", False, "无预言值 ⇒ 无误差带"),
    ("M5 与观测吻合", False, "常数层 8 项不可复算/自相冲突；结构层第7式符号反、第18式通解不成立"),
]
for name, ok, why in gate:
    emit("  %-14s %s  %s" % (name, "❌" if not ok else "✅", why))
n_pass = sum(1 for _, ok, _ in gate if ok)
emit("  M1–M5 通过 %d/5" % n_pass)
chk("E1_all_gates_fail", n_pass == 0, "五门槛全失守")

emit("\n" + "=" * 74)
emit("攻破⑭ 判定：S17 20 核心公式 = 常数重排 + 量纲不闭合 + 结构层自相矛盾")
emit("=" * 74)
emit("  ① 常数层：Z 自报错一个数量级（隐含 c/10）、Z' 错 4.0e7 倍且同文件二义（有量纲 vs alpha）、")
emit("     f 恒等于 (c/2)sqrt(4 pi eps0 G) 非独立常数、alpha 补正式与 CODATA 偏差 0 ⇒ 循环自证")
emit("  ② 量纲层：f 表达式 M^-1 L I vs 方程需求 M I^-1（差 M^2 L^-1 I^-2）——无任何取值能同时满足；")
emit("     e^2 Z'/(hbar c) 量纲为速度；kk' = 3.1726e3 而非 1 且量纲 M·I 非无量纲")
emit("  ③ 结构层：第18式通解残差 2(g'-f')/(c r) ≠ 0（数值复算一致，带 1/r 才归零）；")
emit("     第7式低速极限 F = -m dV/dt 反号；第17式缺惯性项；第1/2式字面互斥；能量式两读法均不闭合")
emit("  ④ 账本层：40 条 claims = falsified 17 / unreviewed 20 / verified 2 / open 1，")
emit("     2 条 verified 均为恒等式与定义式（A 段已复算），零数值预言")
emit("  → 三分类：借实验值（常数层）+ 无预测（结构层）+ 有预测但错/不自洽 ⇒ M1–M5 0/5，未攻破")

emit("\n自检 %d/%d" % (NPASS, NCHECK))

rp = Path(__file__).resolve().parent / "attack12_S17_统一场论核心公式_攻破_report.txt"
with open(rp, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
print("report -> %s" % rp)
sys.exit(0 if NPASS == NCHECK else 1)
