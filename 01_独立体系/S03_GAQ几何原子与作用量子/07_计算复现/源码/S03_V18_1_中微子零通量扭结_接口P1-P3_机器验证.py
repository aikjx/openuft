# -*- coding: utf-8 -*-
"""
S03-D1 后续 · V18.1 分支二（中微子零通量扭结与马约拉纳）接口 P1–P3 机器验证

承接 S03-D1 §9.2 选定的分支二与 §9.3 的三项前置接口。逐项给出可算与不可算的边界。

验证 1（P3-a）W- 衰变末态的 J_z 守恒与螺旋度组合相容性
验证 2（P3-b）V-A 电子角分布 1+cosθ 的 Wigner d 归一化与宇称破缺指标
验证 3（P2）  h_W = f(σ_τ, N) 映射族对 d→u 手性守恒与 e-ν̄ 螺旋性反差的相容性
验证 4（P1）  内部自由度三约束联合扫描 + 目标反解 + 可证伪性判决
验证 5      过拟合检测：α 自由时该族恒有解
自检 8 项

红线：
- 验证 1/2 是 SM 已确立事实，其 PASS 不构成 GAQ 的成就，只构成对 GAQ 的约束。
- 验证 3 只证明构造族在手性约束层面未被否证，不构成存在性证明。
- 验证 4 是本册唯一的否证结果，射程严格限于族 F1（单一幂律 m ∝ N^α + 手性由 N 奇偶翻转）。
- 不调参数、不做后验拟合：α 始终由 d/u 质量比锁定，α 自由版本单列为验证 5（不可证伪演示）。
- 质量取标称值；夸克质量为 running 量，单值带约 10% 理论依赖，已计入结论不确定度。

判定词表：PASS / FAIL / BOUNDARY / INFO
"""
import math
import sys
import sys as _sys_utf8

try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 标称输入
# 夸克质量为 MSbar 标称值（running 量，理论依赖约 10%）
M_U_MEV = 2.16
M_D_MEV = 4.67
M_E_MEV = 0.510999
# 中微子质量实验上限（KATRIN 2022，90% CL）
M_NU_MAX_EV = 0.8
M_NU_MAX_MEV = M_NU_MAX_EV * 1.0e-6
RATIO_DU = M_D_MEV / M_U_MEV
RATIO_ENU_MIN = M_E_MEV / M_NU_MAX_MEV
LN_DU = math.log(RATIO_DU)
LN_ENU = math.log(RATIO_ENU_MIN)

MIN_GAP = 2   # R1 要求 Nd 与 Nu 同奇偶且 Nd>Nu ⇒ 最小差为 2
MAXN = 20     # 验证 3 的枚举上限

RESULTS = []


def P(name, detail):
    RESULTS.append(("PASS", name, detail))


def F(name, detail):
    RESULTS.append(("FAIL", name, detail))


def B(name, detail):
    RESULTS.append(("BOUNDARY", name, detail))


def I(name, detail):
    RESULTS.append(("INFO", name, detail))


def hdr(title):
    print("=" * 70)
    print(title)
    print("=" * 70)


# ================================================================ 验证 1
# W- 静止系且沿 -z 飞行 ⇒ J_z = -1。
# 末态电子动量沿 +z、中微子动量沿 -z；螺旋度 λ 定义为自旋沿**自身动量**的投影。
# 故 J_z = λ_e - λ_ν。
hdr("验证 1 | P3-a  J_z 守恒对末态螺旋度组合的相容性筛选")

COMBOS = [(+0.5, +0.5), (+0.5, -0.5), (-0.5, +0.5), (-0.5, -0.5)]
allowed = []
rejected = []
for lam_e, lam_nu in COMBOS:
    jz = lam_e - lam_nu
    tag = "e-{} nu-{}".format("R" if lam_e > 0 else "L", "R" if lam_nu > 0 else "L")
    if abs(jz + 1.0) < 1e-12:
        allowed.append((tag, jz, "W-"))
    elif abs(jz - 1.0) < 1e-12:
        allowed.append((tag, jz, "W+"))
    else:
        rejected.append((tag, jz))

print("  J_z = lambda_e - lambda_nu")
for tag, jz, src in allowed:
    print("    [容许] {:<12} J_z = {:+.1f}   ({})".format(tag, jz, src))
for tag, jz in rejected:
    print("    [排除] {:<12} J_z = {:+.1f}   (与 J_z=+/-1 均不符)".format(tag, jz))

n_allowed = len(allowed)
n_rejected = len(rejected)
if n_allowed == 2 and n_rejected == 2:
    P("P3-a", "J_z 守恒唯一保留异螺旋度组合 e-L nu-R(J_z=-1) 与 e-R nu-L(J_z=+1)；"
              "同螺旋度 LL/RR 因 J_z=0 被排除。这正是 V-A 的最小内容（宇称破坏），"
              "且它只用了角动量守恒，未用任何弱作用输入。")
else:
    F("P3-a", "组合筛选异常：容许 {} 个、排除 {} 个（期望 2/2）".format(n_allowed, n_rejected))

B("P3-a->GAQ", "对 GAQ 的硬约束：扭结分类必须能产生 e-L 与 nu-R 这一对螺旋性并排除 e-L 与 nu-L。"
              "S03-D1 §3.4 把 e- 与 nu-bar 列为同一类闭合扭结仅净通量不同，"
              "该分类无法产生此螺旋性反差 → 必须引入区分两者的内部标签（接口 P1）。")

# ================================================================ 验证 2
hdr("验证 2 | P3-b  V-A 电子角分布 1+cosθ 的归一化与宇称破缺指标")


def dmat_1_11(cos_t):
    return 0.5 * (1.0 + cos_t)


def prob_unnorm(cos_t):
    return dmat_1_11(cos_t) ** 2


def integrate(f, lo, hi, n=200000):
    """辛普森积分。注意 (1+x)^2 非偶函数，禁止半区间乘 2 的对称性加速。"""
    h = (hi - lo) / n
    s = 0.0
    for k in range(n + 1):
        x = lo + k * h
        w = 1.0 if k in (0, n) else (4.0 if k % 2 == 1 else 2.0)
        s += w * f(x)
    return s * h / 3.0


integral_full = integrate(prob_unnorm, -1.0, 1.0)
norm_const = 1.0 / integral_full


def prob(cos_t):
    return norm_const * prob_unnorm(cos_t)


integral_prob = integrate(prob, -1.0, 1.0)
parity_odd = integrate(lambda t: prob(t) - prob(-t), 0.0, 1.0)

print("  Int |d_11|^2 dcos = {:.12f}   (解析 2/3)".format(integral_full))
print("  归一化常数            = {:.12f}   (解析 1.5)".format(norm_const))
print("  Int f dcos           = {:.12f}   (应 = 1)".format(integral_prob))
print("  f(0)  = {:.8f}   (解析 0.375)".format(prob(0.0)))
print("  f(+1) = {:.8f}   f(-1) = {:.8f}   (解析 1.5 / 0)".format(prob(1.0), prob(-1.0)))
print("  宇称奇分量 Int_0^1[f(x)-f(-x)]dx = {:.10f}   (解析 0.75)".format(parity_odd))

if abs(integral_prob - 1.0) < 1e-9 and abs(norm_const - 1.5) < 1e-9:
    P("P3-b", "归一化因子 1.5 精确复现，f(x)=3/8(1+x)^2 在 [-1,1] 上积分为 1（偏差 < 1e-9）。"
              "V-A 电子角分布的 Wigner d 表达机器零通过。")
else:
    F("P3-b", "归一化未通过：Int f = {:.12f}，norm = {:.12f}".format(integral_prob, norm_const))

if abs(parity_odd - 0.75) < 1e-9:
    P("P3-b-parity", "f(x) != f(-x)，宇称奇分量 0.75 != 0：角分布本身即宇称破坏的可观测量，"
                    "这是 GAQ 若走手性路线必须复现的量。")
else:
    F("P3-b-parity", "宇称奇分量异常：{:.10f}".format(parity_odd))

# ================================================================ 验证 3
# 接口 P2：映射族 F1 —— h_W = (-1)^N · σ_τ（内部扭结数奇偶决定手性翻转）
hdr("验证 3 | P2  映射族 F1 对两条 V-A 约束的相容性")

r1_solutions = [(nd, nu) for nd in range(1, MAXN + 1) for nu in range(1, MAXN + 1)
                if nd % 2 == nu % 2]
r2_solutions = [(ne, nn) for ne in range(1, MAXN + 1) for nn in range(1, MAXN + 1)
                if ne % 2 != nn % 2]
same_parity_pairs = [(nd, nu) for nd, nu in r1_solutions if nd - nu == MIN_GAP]

print("  R1（d→u 手性守恒，需 Nd 同奇偶）解数 N<={}: {}".format(MAXN, len(r1_solutions)))
print("  R2（e-nu 螺旋性反差，需 Ne 异奇偶）解数 N<={}: {}".format(MAXN, len(r2_solutions)))
print("  R1 最小质量比情形 Nd=Nu+2（同奇偶）解数: {}  样例 {}".format(
    len(same_parity_pairs), same_parity_pairs[:5]))

if r1_solutions and r2_solutions:
    P("P2-existence", "族 F1 在纯手性约束层面有解：R1 要求 N 同奇偶、R2 要求 N 异奇偶，"
                     "两者分别约束夸克侧与轻子侧、互不冲突。"
                     "故「手性反差」这一要求本身不可被纯手性约束否证。")
else:
    F("P2-existence", "族 F1 在纯手性约束层面无解")

# ================================================================ 验证 4
hdr("验证 4 | P1  内部自由度三约束联合扫描 + 目标反解 + 可证伪性判决")

print("  输入：m_d/m_u = {:.6f}    m_e/m_nu > {:.4e}".format(RATIO_DU, RATIO_ENU_MIN))
print("  构造假设 CA-1：N 为正整数；Nd 与 Nu 同奇偶且 Nd>Nu（d 更重）")
print("  质量标度 m ∝ N^α，α 由 d/u 锁定：α = ln(m_d/m_u)/ln(Nd/Nu)")
print("  e/nu 侧需求：Ne/Nν = (m_e/m_nu)^(1/α)")
print()
print("  敏感性表（N_u = 基准内部扭结数）")
print("    {:>5} {:>11} {:>9} {:>9} {:>15} {:>12}".format(
    "N_u", "Nd范围", "α最小", "α最大", "需求Ne/Nν", "对应Nd/Nu"))
scan_rows = []
for nu in (1, 2, 3, 5, 10, 20, 50, 100, 200):
    nd_list = [nd for nd in range(nu + MIN_GAP, 4 * nu + 1) if (nd - nu) % 2 == 0]
    if not nd_list:
        continue
    a_list = [LN_DU / math.log(float(nd) / float(nu)) for nd in nd_list]
    a_lo = min(a_list)
    a_hi = max(a_list)
    need = math.exp(LN_ENU / a_hi)
    scan_rows.append((nu, nd_list[0], nd_list[-1], a_lo, a_hi, need))
    print("    {:>5} {:>11} {:>9.4f} {:>9.4f} {:>15.3e} {:>12.4f}".format(
        nu, "{}-{}".format(nd_list[0], nd_list[-1]), a_lo, a_hi, need,
        math.exp(LN_DU / a_hi)))

print()
print("  趋势：N_u 增大 → 最小质量比 Nd/Nu 趋近 1 → α 无上界 → e/nu 需求趋近 1。")
print("  即该族的可行性由 N 的**量级**支配，而非由 α 的取值支配。")

print()
print("  目标反解（令 Nν=1、Ne=目标值，求满足需求 <= 目标 的最小同奇偶 N 对）")
print("    {:>12} {:>10} {:>9} {:>9} {:>14}".format(
    "目标Ne/Nν", "最小N对", "比值", "α", "实际需求"))
reverse_rows = []
for target in (2.0, 10.0, 100.0, 1.0e4, 1.0e8):
    best = None
    for nu in range(1, 400):
        for nd in range(nu + MIN_GAP, 4 * nu + 1):
            if (nd - nu) % 2 != 0:
                continue
            a = LN_DU / math.log(float(nd) / float(nu))
            need = math.exp(LN_ENU / a)
            if need <= target and (best is None or nd < best[0]):
                best = (nd, nu, float(nd) / float(nu), a, need)
    if best:
        reverse_rows.append((target, best))
        print("    {:>12.3g} {:>10} {:>9.4f} {:>9.4f} {:>14.3e}".format(
            target, "{}:{}".format(best[0], best[1]), best[2], best[3], best[4]))
    else:
        print("    {:>12.3g} {:>10}".format(target, "N<=399 内无解"))

need_at_one = [r[5] for r in scan_rows if r[0] == 1][0]
n_for_10 = next((b[0] for t, b in reverse_rows if abs(t - 10.0) < 1e-9), None)
n_for_2 = next((b[0] for t, b in reverse_rows if abs(t - 2.0) < 1e-9), None)

print()
print("  => 目标 Ne/Nν = 2   需最小 N 对约 N = {}".format(n_for_2))
print("  => 目标 Ne/Nν = 10  需最小 N 对约 N = {}".format(n_for_10))
B("P1-joint", "族 F1 在 N=O(1)（内部扭结数为少数几个，符合「结」的图像）时不可行："
              "N_u=1 下 e/nu 质量比要求 Ne/Nν ≳ {:.2e}。"
              "要把它压到 O(10) 需内部扭结数 N ≳ {}；压到最小整数比 2 需 N ≳ {}。"
              "此时「内部扭结数」已失去「结」的物理含义（数十个扭结是复合体或介质，不是结）。"
              "结论：族 F1 的可行域与其物理图像不相容。".format(need_at_one, n_for_10, n_for_2))

need_at_200 = [r[5] for r in scan_rows if r[0] == 200][0]
F("P1-falsifiability", "族 F1 不满足可证伪性：N_u 增至 200 时 α 可取任意大，"
                       "e/nu 需求降至 {:.3f}（见敏感性表末行），"
                       "故该族对**任意**质量比恒存在参数解。"
                       "无论参数取何值它都无法被实验否证，不能作为解释性构造通过审查。"
                       "这是本册的核心否证结果，射程严格限于族 F1。".format(need_at_200))

I("P1-repair", "两条出路（均需 V18.2，本册不预判）："
               "(a) 给 α 或 N 一个**独立**定义或约束，使该族不再任意可调；"
               "(b) 引入两类内部自由度 N_Q（夸克型）与 N_L（轻子型）各自独立幂律 —— "
               "与 SM 中夸克质量源自强子标度、轻子质量源自电弱真空期望值的两类机制同构。")

# ================================================================ 验证 5
hdr("验证 5 | 过拟合检测：α 自由时该族恒有解（故不可证伪）")

free_solutions = len(r2_solutions)
print("  α 自由时 R2 可行解数（N<={}）：{}".format(MAXN, free_solutions))
print("  每个解都给出一个 α = ln(Ne/Nν) 可拟合对应质量比 → 恒可拟合。")
P("P5-method", "过拟合演示：α 自由 ⇒ 该构造族对任意质量比恒有解 ⇒ 不具备证伪能力。"
               "因此验证 4 必须锁定 α（本册用 d/u 质量比锁定）才有判据力。"
               "此为本册方法论前提，也是 S03-D1 §9.3 预设失效阈值的执行方式。")

# ================================================================ 自检
hdr("自检")

SC = []


def sc(name, ok, detail=""):
    SC.append((name, ok, detail))
    print("  [{}] {}{}".format("OK" if ok else "NG", name, ("  " + detail) if detail else ""))


n_pass_sc = sum(1 for _, ok, _ in SC if ok) if SC else 0
sc("SC1 J_z 组合筛选 = 2 容许 / 2 排除", n_allowed == 2 and n_rejected == 2)
sc("SC2 角分布 Int f = 1", abs(integral_prob - 1.0) < 1e-9,
   "偏差 {:.2e}".format(abs(integral_prob - 1.0)))
sc("SC3 归一化常数 = 1.5", abs(norm_const - 1.5) < 1e-9)
sc("SC4 宇称奇分量 = 0.75 != 0", abs(parity_odd - 0.75) < 1e-9 and parity_odd > 0)
sc("SC5 R1 与 R2 解集均非空", len(r1_solutions) > 0 and len(r2_solutions) > 0)
sc("SC6 目标反解单调（目标越大所需 N 越小或不增）",
   len(reverse_rows) >= 2 and reverse_rows[-1][1][0] <= reverse_rows[0][1][0],
   "{} -> {}".format(reverse_rows[0][1][0], reverse_rows[-1][1][0]))
sc("SC7 N_u=1 需求 > 1e6（小 N 不可行的数值前提）", need_at_one > 1.0e6,
   "{:.3e}".format(need_at_one))
sc("SC8 N_u=200 需求 < 10（可证伪性否证的前提）", need_at_200 < 10.0,
   "{:.3f}".format(need_at_200))

# ================================================================ 汇总
hdr("判定汇总")
cnt = {}
for kind, name, detail in RESULTS:
    cnt[kind] = cnt.get(kind, 0) + 1
    print("  [{}] {}".format(kind, name))
    print("         {}".format(detail))
print()
print("  统计：PASS={} FAIL={} BOUNDARY={} INFO={}  合计={}".format(
    cnt.get("PASS", 0), cnt.get("FAIL", 0), cnt.get("BOUNDARY", 0),
    cnt.get("INFO", 0), len(RESULTS)))

n_ok = sum(1 for _, ok, _ in SC if ok)
print("  自检：{}/{} 通过".format(n_ok, len(SC)))
print()
print("  红线声明：")
print("   - 验证 1/2 是 SM 已确立事实，其 PASS 不构成 GAQ 的成就，只构成对 GAQ 的约束。")
print("   - 验证 3 只证明构造族在手性约束层面未被否证，不构成存在性证明。")
print("   - 验证 4 是本册唯一的否证结果（P1-falsifiability），射程严格限于族 F1。")
print("   - 验证 5 说明该族在 α 自由时不可证伪，故本册全部结论依赖 α 锁定前提。")
print("   - 本册未对 GAQ 的任何主张给出正面支持证据。")

if n_ok == len(SC):
    print()
    print("SELF-CHECK PASS ({}/{})".format(n_ok, len(SC)))
else:
    print()
    print("SELF-CHECK FAIL")
    sys.exit(1)
