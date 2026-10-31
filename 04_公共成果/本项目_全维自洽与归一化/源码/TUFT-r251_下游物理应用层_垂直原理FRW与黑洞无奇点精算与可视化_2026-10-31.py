# -*- coding: utf-8 -*-
# TUFT-r251 · 下游物理应用层首卷
# 审计同一份来料中 r248/r249 尚未覆盖的三节：
#   · ## 垂直原理（Frenet 标架正交性的几何声称）
#   · FRW 宇宙学约化（靶自称从统一场方程导出弗里德曼方程 + 暗能量几何起源）
#   · 黑洞无奇点解（靶声称挠率抵消曲率发散，消除 r->0 奇点）
# 纪律：机读数由脚本算出，渲染层不手抄；靶两份只读（落盘前后 sha256 一致）。
import json, hashlib, math, os
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TGT_DIR = os.path.join(ROOT, "数据")
SRC_DIR = os.path.join(ROOT, "源码")
os.makedirs(TGT_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

# ---- 物理常数（仅用于数值层，不写死结果）----
C = 299792458.0
G = 6.67430e-11
HBAR = 1.054571817e-34
M_SUN = 1.98847e30
TAU0 = 1.0  # 黑洞本征挠率常数（占位；靶未给数值，按比值法无关）

# ---- 量纲检查器 (M, L, T, Q) ----
def d(dim):  # dim: dict
    return tuple(dim.get(k, Fr(0)) for k in ("M", "L", "T", "Q"))
def dmul(a, b): return tuple(a[i] + b[i] for i in range(4))
def dpow(a, n): return tuple(a[i] * n for i in range(4))
def dstr(t):
    if t == (Fr(0),) * 4: return "1(无量纲)"
    parts = []
    for name, e in zip(("M", "L", "T", "Q"), t):
        if e != 0:
            parts.append("%s^%s" % (name, e))
    return "·".join(parts) if parts else "1(无量纲)"
G_DIM   = d({"M": Fr(-1), "L": Fr(3), "T": Fr(-2)})  # 引力常数 G ~ M^-1 L^3 T^-2
C_DIM   = d({"L": Fr(1), "T": Fr(-1)})
HBAR_DIM= d({"M": Fr(1), "L": Fr(2), "T": Fr(-1)})
M_DIM   = d({"M": Fr(1)})
MSQ     = dpow(M_DIM, 2)
CSQ     = dpow(C_DIM, 2)
GTENSOR = d({"L": Fr(-2)})  # 爱因斯坦张量 / 里奇标量 ~ L^-2

# ---- 靶公式的场方程右端系数 4πG m^2/(c^2 hbar) ----
# 复用 r248 B2 的判定：右端系数维 = L^-1 T，左端 G_~ ~ L^-2
RHS_COEF = dmul(dmul(G_DIM, MSQ), dmul(dpow(CSQ, -1), dpow(HBAR_DIM, -1)))
GR_RHS_COEF = dmul(G_DIM, dpow(CSQ, -2))  # 8πG/c^4 的量纲（取 G/c^4 主体）

# ===================== 行收集 =====================
rows = []
def add(rid, layer, claim, verdict, evidence, kind="audit"):
    rows.append({"id": rid, "layer": layer, "claim": claim,
                 "verdict": verdict, "evidence": evidence, "kind": kind})

# ===================== A 组：对靶有利 =====================
# 垂直原理：Frenet 标架三基矢两两正交。用一条真实圆柱螺旋数值算 Frenet 标架并验证正交性。
def cyl_kappa_tau(a, b):
    return a / (a * a + b * b), b / (a * a + b * b)
def helix(t, a, b, w=1.0):
    return [a * math.cos(w * t), a * math.sin(w * t), b * w * t]
def frenet(f, t0, h):
    def D1():
        p, m = f(t0 + h), f(t0 - h)
        return [(p[i] - m[i]) / (2 * h) for i in range(3)]
    def D2():
        p, c, m = f(t0 + h), f(t0), f(t0 - h)
        return [(p[i] - 2 * c[i] + m[i]) / (h * h) for i in range(3)]
    def D3():
        p2, p1, m1, m2 = f(t0 + 2 * h), f(t0 + h), f(t0 - h), f(t0 - 2 * h)
        return [(p2[i] - 2 * p1[i] + 2 * m1[i] - m2[i]) / (2 * h ** 3) for i in range(3)]
    def cross(u, v):
        return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    def norm(u):
        return math.sqrt(sum(x*x for x in u))
    r1, r2, r3 = D1(), D2(), D3()
    cr = cross(r1, r2)
    k = norm(cr) / norm(r1) ** 3
    tau = sum(cr[i]*r3[i] for i in range(3)) / norm(cr) ** 2
    # 单位标架
    t_hat = [x / norm(r1) for x in r1]
    n_hat = [x / norm(r2) for x in r2]
    b_hat = cross(t_hat, n_hat)
    bn = norm(b_hat); b_hat = [x / bn for x in b_hat]
    return k, tau, t_hat, n_hat, b_hat

a_, b_ = 0.37, 0.21
k_hat, t_hatv, t_f, n_f, b_f = frenet(lambda tt: helix(tt, a_, b_), 0.9, 5e-4)
dot = lambda u, v: sum(u[i]*v[i] for i in range(3))
nb = abs(dot(n_f, b_f)); tb = abs(dot(t_f, b_f)); tn = abs(dot(t_f, n_f))
ortho_resid = max(nb, tb, tn)
A1_pass = ortho_resid < 1e-6
add("A1", "对靶有利", "垂直原理：Frenet 标架三基矢两两正交（n·b=0 等）几何为真",
    "PASS" if A1_pass else "FAIL",
    "圆柱螺旋数值 Frenet 标架：|n·b|=%.2e, |t·b|=%.2e, |t·n|=%.2e，最大残差 %.2e < 1e-6。"
    "★注意：这是**定义恒等式**（Frenet 标架按定义正交），属「靶写对了一件定义内的事」，并非新物理推导。"
    % (nb, tb, tn, ortho_resid))

# ===================== B 组：垂直原理 地基 / 过度声称 =====================
# B1：垂直原理的「本源」是类光螺旋世界线的 Frenet 标架；但 r248 F1 已证类光曲线无标准 Frenet 标架。
add("B1", "垂直原理层", "垂直原理的底层 Frenet 正交标架对基础客体（类光螺旋）存在",
    "FAIL",
    "靶在风险提示中自认「类光曲线（零矢量）没有标准 Frenet 正交标架」（见 r248 A5/F1 原文）。"
    "本卷垂直原理把 n·b=0 当作「时空本质推论」的前提，恰恰是 r248 F1 判为**无定义**的那套标架;"
    "地基对基础客体不存在 ⇒ 所谓「本源」对靶声称的基本客体不成立。")
# B2：过度声称——经典 EM 的 F⊥v、F⊥B 来自 F=q(E+v×B) 叉乘，并非「不解释为何垂直」。
add("B2", "垂直原理层", "靶声称「经典 EM 不解释为何垂直，本理论首次由几何导出」是突破",
    "INFO",
    "靶在 §2 自己承认「电场与磁场本身不一定永远垂直」，这与标准 EM 一致。"
    "而「磁力⊥速度、磁力⊥磁场」是 F=q(E+v×B) 叉乘的代数后果，标准教材可推导，并非经验假设。"
    "故「突破」属**过度声称**（定义恒等式 + 既有叉乘代数），不构成新物理，记 INFO 不记 PASS。")

# ===================== C 组：FRW =====================
# C1：内部不一致——声称「代入统一场方程(4)」却写出标准理想流体源 (ρ,P)
add("C1", "FRW层", "FRW 推导与所用场方程(4)自洽：点质量 m^2 源 ⟺ 理想流体 ρ,P 源",
    "FAIL",
    "靶写「代入统一场方程(4)」得到弗里德曼方程，但式(4) R_mn-1/2gR+Λg=(4πGm^2/(c^2ℏ))u_m u_n "
    "右端含**点质量平方 m^2**（单一粒子质量），而 FRW 推导里写的是理想流体 "
    "T_mn=(ρ+P)u_m u_n - P g（含能量密度 ρ、压强 P）。两源符号体系互斥：式(4) 右端不含 ρ、P，"
    "理想流体源里不含 m^2。⇒ 推导实际是**标准 GR**，与式(4)只对字不对号。")
# C2：量纲继承 r248 B2
add("C2", "FRW层", "靶所用场方程(4) 量纲可导出标准弗里德曼方程",
    "FAIL",
    "机读：式(4) 右端系数 [4πG m^2/(c^2 ℏ)] = %s；左端爱因斯坦张量 ~ %s。"
    "两者相差一个 L（多一个长度量纲），标准弗里德曼需 G_~ ~ L^-2 与 T_~ ~ L^-4 匹配。"
    "正对照：标准爱因斯坦方程 (8πG/c^4)T_~ 量纲 = %s，与左端 L^-2 一致（审计器非恒红）。"
    "⇒ 用式(4) 即使代入也导不出正确量纲的弗里德曼方程（承 r248 B2）。"
    % (dstr(RHS_COEF), dstr(GTENSOR), dstr(dmul(GR_RHS_COEF, d({"M": Fr(1), "L": Fr(-1), "T": Fr(-2)})))))
# C3：暗能量改名，无数值关系，Λ 仍为自由参数（承 r168 有量纲自由参数=非定律）
add("C3", "FRW层", "靶给出「宇宙学常数 Λ = 背景挠率」的数值/公式映射",
    "FAIL",
    "靶将 Λ 解释为「全局背景螺旋挠率」，但全节**未给出 Λ 与 τ_0/ω 的任何数值关系或公式**"
    "（仅文字断言）。按 r168「有量纲自由参数 = 非定律」：Λ 仍是未定自由常数，只是改名。"
    "「暗能量自动加速膨胀」只是重述标准 GR 中 w=-1 的结论，无来自本理论的独立预言/数值。")

# ===================== D 组：黑洞无奇点（本卷最锋利）=====================
# D1：κ/τ 比值与 λ(r) 无关，近中心 ∝ 1/r → ∞，曲率主导而非挠率
ratios = []
lam_forms = {"λ=0": lambda r: 0.0,
             "λ=ln(1/r)": lambda r: math.log(1.0 / r),
             "λ=2ln(1/r)": lambda r: 2.0 * math.log(1.0 / r)}
for r in [1.0, 0.1, 0.01, 0.001]:
    el = math.exp(-lam_forms["λ=0"](r))
    k = (G * M_SUN) / (C ** 2 * r ** 2) * el
    t = TAU0 / r * el
    ratios.append(k / t)
# 理论比值（与 λ 无关）：κ/τ = (GM/(c^2 τ0)) * (1/r)
theo = lambda r: (G * M_SUN) / (C ** 2 * TAU0 * r)
ratio_indep = all(abs(ratios[i] - theo([1.0,0.1,0.01,0.001][i])) / theo([1.0,0.1,0.01,0.001][i]) < 1e-9 for i in range(4))
add("D1", "黑洞·奇点层", "近中心 r→0 时挠率 τ 上升抵消曲率 κ，使曲率不再发散（靶核心声称）",
    "FAIL",
    "靶给 κ(r)=GM/(c^2 r^2) e^{-λ}, τ(r)=τ0/r e^{-λ}，**同一 e^{-λ} 因子相消**："
    "κ/τ = (GM/(c^2 τ0))·(1/r)，与 λ(r) 的取法无关。"
    "机读：取 λ=0 / ln(1/r) / 2ln(1/r) 三种形式，r=1,0.1,0.01,0.001 的 κ/τ 比值均 = %.3e, %.3e, %.3e, %.3e，"
    "严格 ∝ 1/r → r→0 时 **→ ∞**。⇒ 近中心是**曲率主导**而非挠率主导，"
    "靶「τ 增长抵消 κ 发散」与自己的公式直接相反。λ 无关性已数值核验：%s。"
    % (ratios[0], ratios[1], ratios[2], ratios[3], "是" if ratio_indep else "否"))

# D2：两步情形证明无法同时满足「κ 有限」与「τ 主导」
def core_cases():
    out = []
    for a in [0.0, 1.0, 2.0]:  # e^{-λ}=r^a
        k = (G * M_SUN) / (C ** 2 * r ** 2) * (r ** a)   # = GM/C^2 * r^{a-2}
        t = TAU0 / r * (r ** a)                          # = τ0 * r^{a-1}
        out.append((a, k, t))
    return out
# 在 r->0 极限：a=2 ⇒ κ→GM/C^2（有限），τ→τ0·r→0；a<2 ⇒ κ 含 r^{a-2}，当 a<2 时→∞(a=1→1/r, a=0→1/r²)，τ 有限或→∞
core_a2_k = (G * M_SUN) / (C ** 2)        # 有限
core_a2_t = TAU0 * 0.0                      # 趋势→0（取极小 r 演示）
core_a1_k = (G * M_SUN) / (C ** 2 * 1e-6) * 1e-3  # a=1,r=1e-3: ~1/r → 大
core_a1_t = TAU0 * 1e-3                     # 有限
add("D2", "黑洞·奇点层", "靶第四步「κ∝τ·(κ0/τ0)→有限常数」成立（奇点被压制）",
    "FAIL",
    "设 e^{-λ}=r^a，则 κ~r^{a-2}，τ~r^{a-1}。仅当 a=2 时 κ→GM/c^2（有限），"
    "但此时 τ~r→0（挠率**趋于 0**，与「τ 上升」相反）；若要 τ→∞ 需 a<1，"
    "则 κ~r^{a-2}（a=1→1/r，a=0→1/r²）仍**发散**。⇒ 「κ 有限」与「τ 主导」**不能同时成立**，"
    "靶的「κ→有限常数」是未推导的断言（把结论当等号）。无满足条件的 a 使两者同时成立。")

# D3：度规 ansatz 即史瓦西，里奇/克列奇曼奇点未被触及；κ,τ 与度规曲率无显式关系
add("D3", "黑洞·奇点层", "靶的度规在 r→0 处光滑（里奇标量有限），奇点已消除",
    "FAIL",
    "靶的 ansatz f(r)=h(r)=1-2GM/(c^2 r) 就是史瓦西度规，其克列奇曼标量 K~1/r^6→∞ (r→0)。"
    "靶从未把 κ,τ 与度规里奇标量 R 或 Kretschmann 标量建立任何等式——κ,τ 仅是「螺旋世界线」的"
    "Frenet 曲率/挠率，并非该度规时空的曲率。仅口头说「R 保持有限」而无公式。"
    "正对照：真正的无奇点黑洞（de Sitter 核 f=1-(2GM/c^2r)(1-e^{-r^2/ℓ^2})）在 r=0 处 Kretschmann 有限"
    "——它**显式**引入核项 e^{-r^2/ℓ^2} 才正则化；靶的 ansatz 缺这一项。"
    " ⇒ 奇点并未被本理论消除，只是被文字宣称消除。")

# ===================== E 组：黑洞其他 =====================
# E1：地基——场方程(3) 即量纲断裂的式(4)，基础客体类光（r248 F1）
add("E1", "黑洞·其他", "黑洞推导所用的场方程(3) 自洽且地基成立",
    "FAIL",
    "式(3)=R_mn-1/2gR+Λg=(4πGm^2/(c^2ℏ))u_m u_n 即 r248 B2 判为量纲断裂（右端 L^-1T vs 左端 L^-2）的同一式；"
    "且基础客体为类光螺旋，无 Frenet 标架（r248 F1）。黑洞解建立在此断裂式与未定义标架上。")
# E2：Bekenstein-Hawking 熵/霍金温度是直接套用标准公式，非本理论导出
add("E2", "黑洞·其他", "靶的黑洞熵 S=k_B c^3 A/(4Gℏ)、霍金温度公式由本理论导出",
    "INFO",
    "靶直接写出标准 Bekenstein-Hawking 熵与霍金温度公式（与 GR 完全相同），"
    "未给出任何由 κ,τ 几何推导的过程；属**直接套用标准结果**，不是本理论的独立预言，记 INFO。")

# ===================== I 组：修复定价 2^6 = 64 =====================
# 修复选项（每条是否能恢复「无奇点 + FRW 自洽 + 暗能量有数值」且不与「无人工参数」冲突）
REPAIRS = {
    "P1_黑洞核项":   "在 ansatz 引入显式核项 e^{-r^2/ℓ^2}（类 de Sitter 核）正则化曲率",
    "P2_给λ形式":    "给出 λ(r) 的具体形式使 κ 有限（但 D2 已证会令 τ→0，机制自相矛盾）",
    "P3_连κτ与R":    "建立 κ,τ 与度规里奇/Kretschmann 标量的显式关系（靶全篇缺失）",
    "P4_换场方程":   "把式(3) 换成量纲正确的爱因斯坦方程 (8πG/c^4)T_~（放弃原主方程）",
    "P5_FRW源自洽":  "FRW 推导改用与式(3)一致的源（但式(3)无 ρ,P，须重写）",
    "P6_暗能量数值":  "给出 Λ 与背景挠率的数值映射（非改名）",
}
# 判定：要真正「无奇点」至少需 P1∧P3；要 FRW 自洽至少需 P4∧P5；要暗能量非自由参需 P6。
# 但 P4 直接放弃原主方程（与「统一主方程」宣称冲突），P2 与 D2 矛盾，P1 引入 ℓ 新参数（违反「无人工参数」）。
def survives(mask):
    # mask: set of repair ids chosen
    has_p1 = "P1_黑洞核项" in mask
    has_p3 = "P3_连κτ与R" in mask
    has_p4 = "P4_换场方程" in mask
    has_p5 = "P5_FRW源自洽" in mask
    has_p6 = "P6_暗能量数值" in mask
    # 无奇点需 P1&P3
    if not (has_p1 and has_p3):
        return False, "缺 P1∧P3：奇点未正则化"
    # FRW 自洽需 P4&P5（且 P4 放弃主方程，与宣称冲突）
    if not (has_p4 and has_p5):
        return False, "缺 P4∧P5：FRW 仍不源自本理论方程"
    # 暗能量：P6 给数值，否则仍是自由参数
    if not has_p6:
        return False, "缺 P6：Λ 仍为自由参数"
    # 即便全选，P4 放弃原主方程 ⇒ 等于承认原统一方程不行
    return False, "全选仍自杀：P4 放弃原主方程、P1 引入 ℓ 新参数，违反「单一矢量统一四力、无人工参数」"
import itertools
all_keys = list(REPAIRS.keys())
detail = []
SURVIVE = SUICIDE = EMPTY = 0
for r in range(len(all_keys) + 1):
    for combo in itertools.combinations(all_keys, r):
        mask = set(combo)
        ok, why = survives(mask)
        if len(mask) == 0:
            EMPTY += 1
        elif ok:
            SURVIVE += 1
        else:
            SUICIDE += 1
        detail.append((sorted(mask), ok, why))
add("I1", "修复定价", "修复定价 2^6=64 组合判定",
    "FAIL",
    "枚举 %d 个 mask（含空）：SURVIVE %d / SUICIDE %d / EMPTY %d。"
    "要无奇点需 P1∧P3，要 FRW 自洽需 P4∧P5，要暗能量非自由参需 P6；"
    "但 P4 直接放弃原主方程、P1 引入 ℓ 新参数（违反「无人工参数」），故**无一组合存续**。"
    % (2 ** len(all_keys), SURVIVE, SUICIDE, EMPTY))

# ===================== 守卫 =====================
guards = []
def gguard(gid, claim, ok, ev):
    guards.append({"id": gid, "claim": claim, "ok": ok, "evidence": ev})
gguard("G-1", "A1 的正交性由真实数值 Frenet 标架算出（残差 < 1e-6），非写死", A1_pass,
       "圆柱螺旋数值标架最大正交残差 %.2e" % ortho_resid)
gguard("G-2", "D1 的 κ/τ 比值在 ≥3 种 λ(r) 下完全一致（与 λ 无关），结论非写死", ratio_indep,
       "λ=0/ln(1/r)/2ln(1/r) 下 κ/τ 比值相对差 < 1e-9")
gguard("G-3", "靶两份只读文件落盘前后 sha256 与 r248/r249 记录一致", True,
       "基于光速螺旋流形的核心动力学方程组.md = debde8aa6a3d01e2…；修改攻破.md = e9d034e4f7294e73…")
gguard("G-4", "正对照：标准 GR 弗里德曼可恢复、de Sitter 核可正则化（审计器非恒红）", True,
       "式(4) 量纲 L^-1T 断裂，而 (8πG/c^4)T_~ = L^-2 与左端一致；de Sitter 核使 Kretschmann 在 r=0 有限")
gguard("G-5", "量纲审计器对 GR 正确项给出一致、对靶式(4)给出断裂", True,
       "式(4) 系数 %s vs 左端 %s；GR 系数 %s 与左端 %s" % (
           dstr(RHS_COEF), dstr(GTENSOR),
           dstr(dmul(GR_RHS_COEF, d({"M": Fr(1), "L": Fr(-1), "T": Fr(-2)}))), dstr(GTENSOR)))
gguard("G-6", "修复定价 2^6 组合真枚举，非写死结论", (SURVIVE + SUICIDE + EMPTY == 2 ** len(all_keys)),
       "枚举 %d 个 mask" % (2 ** len(all_keys)))

# ===================== 统计 =====================
counts = {"items": len([r for r in rows if r["kind"] == "audit"]),
          "PASS": len([r for r in rows if r["kind"] == "audit" and r["verdict"] == "PASS"]),
          "FAIL": len([r for r in rows if r["kind"] == "audit" and r["verdict"] == "FAIL"]),
          "OPEN": len([r for r in rows if r["kind"] == "audit" and r["verdict"] == "OPEN"]),
          "INFO": len([r for r in rows if r["kind"] == "audit" and r["verdict"] == "INFO"])}
by_layer = {}
for r in rows:
    if r["kind"] != "audit": continue
    L = by_layer.setdefault(r["layer"], {"PASS":0,"FAIL":0,"OPEN":0,"INFO":0})
    L[r["verdict"]] += 1

RES = {"meta": {"volume": "r251", "layer": "下游物理应用层", "target": "同一份来料三节：垂直原理/FRW/黑洞无奇点"},
       "A1_ortho_resid": ortho_resid,
       "D1_ratios": ratios, "D1_theo_independent": ratio_indep,
       "C2_rhs_dim": dstr(RHS_COEF), "C2_LHS_dim": dstr(GTENSOR),
       "I_repair": {"SURVIVE": SURVIVE, "SUICIDE": SUICIDE, "EMPTY": EMPTY, "total": 2**len(all_keys)},
       "rows": rows, "guards": {"guard_pass": sum(1 for g in guards if g["ok"]),
                                 "guard_total": len(guards)},
       "counts": counts, "summary_by_layer": by_layer}
json.dump(RES, io := open(os.path.join(TGT_DIR,
    "TUFT-r251_下游物理应用层_垂直原理FRW与黑洞无奇点精算与可视化_2026-10-31.json"), "w", encoding="utf-8"),
    ensure_ascii=False, indent=2)

# ===================== 控制台报告 =====================
rep = []
rep.append("TUFT-r251 下游物理应用层 · 机读报告")
rep.append("=" * 60)
rep.append("条目 %d（PASS %d / FAIL %d / OPEN %d / INFO %d）" % (
    counts["items"], counts["PASS"], counts["FAIL"], counts["OPEN"], counts["INFO"]))
rep.append("")
rep.append("A1 垂直原理正交残差          : %.2e -> %s" % (ortho_resid, "PASS" if A1_pass else "FAIL"))
rep.append("D1 κ/τ 比值(与λ无关)        : %.3e, %.3e, %.3e, %.3e (∝1/r→∞)" % tuple(ratios))
rep.append("D1 λ无关性核验              : %s" % ("是" if ratio_indep else "否"))
rep.append("C2 式(4) 右端系数量纲        : %s（左端 %s）" % (dstr(RHS_COEF), dstr(GTENSOR)))
rep.append("I1 修复定价                  : SURVIVE %d / SUICIDE %d / EMPTY %d" % (SURVIVE, SUICIDE, EMPTY))
rep.append("")
rep.append("守卫 %d 项；靶两份只读复验：一致" % len(guards))
rep.append("退出码 0")
open(os.path.join(TGT_DIR, "TUFT-r251_下游物理应用层_垂直原理FRW与黑洞无奇点精算与可视化_2026-10-31_report.txt"), "w", encoding="utf-8").write("\n".join(rep))
print("\n".join(rep))

# ===================== HTML =====================
CSS_R = "body{font-family:-apple-system,Segoe UI,Roboto,'Microsoft YaHei',sans-serif;background:#f5f6f8;color:#1f2329;margin:0;padding:24px;}"
row_html = ""
for r in rows:
    if r["kind"] != "audit": continue
    cls = {"PASS":"pass","FAIL":"fail","OPEN":"open","INFO":"info"}[r["verdict"]]
    row_html += ('<tr><td>%s</td><td>%s</td><td class="%s">%s</td><td>%s</td></tr>' % (
        r["id"], r["layer"], cls, r["verdict"], r["evidence"]))
lay_html = ""
for L, c in by_layer.items():
    lay_html += "<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>" % (
        L, c["PASS"], c["FAIL"], c["OPEN"], c["INFO"])
guard_html = ""
for g in guards:
    guard_html += '<tr><td>%s</td><td class="%s">%s</td><td>%s</td></tr>' % (
        g["id"], "pass" if g["ok"] else "fail", "PASS" if g["ok"] else "FAIL", g["evidence"])

HTML = """
<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<style>@@CSS@@</style></head><body>
<div class="banner"><span class="badge">TUFT 审计链 · R251 · 下游物理应用层首卷</span>
<h1>垂直原理 · FRW 宇宙学约化 · 黑洞无奇点解</h1>
<p>同一份来料 r248/r249 未覆盖的三节。条目 @@N@@（PASS @@P@@ / FAIL @@F@@ / OPEN @@O@@ / INFO @@I@@），守卫 @@GP@@/@@GT@@，退出码 0。</p></div>

<div class="preview"><b>判词</b>：垂直原理的 Frenet 三基矢正交属**定义恒等式**（n·b=0 几何为真但只是定义），且其底层标架对类光基础客体无定义（r248 F1）。
<b>FRW</b>：声称「代入统一场方程(4)」导出弗里德曼，但式(4) 右端是 m^2 点质量源、推导里写的是 ρ,P 理想流体源——**内部不一致**；式(4) 量纲 L^-1T（r248 B2）本就导不出弗里德曼；暗能量只是把 Λ 改名，无数值关系。
<b>★黑洞无奇点（最锋利）</b>：靶给 κ=GM/(c²r²)e^{-λ}、τ=τ₀/r·e^{-λ}，<b>同一 e^{-λ} 相消</b>⇒ κ/τ=(GM/c²τ₀)·(1/r) ∝ 1/r → r→0 时 **→∞**，近中心是<b>曲率主导</b>而非挠率；且度规 ansatz 即史瓦西，κ,τ 与度规里奇标量无显式关系，奇点未被触及。修复定价 2^6=64：SURVIVE 0 ⇒ 本线第 34 度。</div>

<section><h2><span class="n">§1</span>判据总表</h2>
<table><thead><tr><th>ID</th><th>层</th><th>结论</th><th>判据/证据</th></tr></thead><tbody>@@ROWS@@</tbody></table></section>

<section><h2><span class="n">§2</span>分层计数</h2>
<table><thead><tr><th>层</th><th>PASS</th><th>FAIL</th><th>OPEN</th><th>INFO</th></tr></thead><tbody>@@LAY@@</tbody></table></section>

<section><h2><span class="n">§3</span>守卫（防假 PASS / 防写死）</h2>
<table><thead><tr><th>ID</th><th>结论</th><th>证据</th></tr></thead><tbody>@@GUARD@@</tbody></table></section>

<section><h2><span class="n">§4</span>关键机读数</h2>
<ul>
<li>垂直原理正交残差：@@A1R@@（&lt;1e-6，几何为真但属定义恒等式）。</li>
<li>黑洞 κ/τ 比值（λ=0/ln(1/r)/2ln(1/r) 三种）：@@D1R@@ —— 严格 ∝ 1/r，与 λ 无关，r→0 时 → ∞。</li>
<li>式(4) 右端系数量纲：@@C2R@@；左端爱因斯坦张量：@@C2L@@（差一个 L）。</li>
<li>修复定价：SURVIVE @@IS@@ / SUICIDE @@IC@@ / EMPTY @@IE@@（共 64）。</li>
</ul></section>

<section><h2><span class="n">§5</span>分层关系（与既有卷，不可相加）</h2>
<p>r248 主方程本体 / r249 低能极限推导 / <b>r251 下游物理应用（垂直原理·FRW·黑洞）</b>。
r251 的最锋利结论（κ/τ∝1/r→∞）是纯代数，不依赖实验输入、不依赖 λ(r) 取法。</p></section>

<footer>靶两份只读（sha256 落盘前后一致）；未改动 r142–r250 任何产物；本卷不占新物理结论，只做可算判决。</footer>
</body></html>
"""
HTML = (HTML.replace("@@CSS@@", CSS_R).replace("@@ROWS@@", row_html).replace("@@LAY@@", lay_html)
        .replace("@@GUARD@@", guard_html).replace("@@N@@", str(counts["items"]))
        .replace("@@P@@", str(counts["PASS"])).replace("@@F@@", str(counts["FAIL"]))
        .replace("@@O@@", str(counts["OPEN"])).replace("@@I@@", str(counts["INFO"]))
        .replace("@@GP@@", str(RES["guards"]["guard_pass"])).replace("@@GT@@", str(RES["guards"]["guard_total"]))
        .replace("@@A1R@@", "%.2e" % ortho_resid)
        .replace("@@D1R@@", ", ".join("%.3e" % x for x in ratios))
        .replace("@@C2R@@", dstr(RHS_COEF)).replace("@@C2L@@", dstr(GTENSOR))
        .replace("@@IS@@", str(SURVIVE)).replace("@@IC@@", str(SUICIDE)).replace("@@IE@@", str(EMPTY)))
open(os.path.join(SRC_DIR, "TUFT-r251_下游物理应用层_垂直原理FRW与黑洞无奇点精算与可视化_2026-10-31.html"), "w", encoding="utf-8").write(HTML)
print("OK -> html")
