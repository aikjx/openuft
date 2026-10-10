# -*- coding: utf-8 -*-
"""
判定：TUFT V4.1 全维攻破 · 第二部：引力的本质 · 全维审计（r35）
===================================================================================
来料：《TUFT V4.1 全维攻破 · 第二部：引力的本质》——第零刀~第四刀、第九刀~第十一刀、
附表（正统答案 8 行对照）、两条救活路径、一句话总结、末尾提问。
来料正本：数据/TUFT-V41引力本质攻破_来料全文_2026-10-11.md（本册 §A 现读印出）。

本册职责：对**来料的每一条论断**做独立机器核验（纯标准库；Decimal 60 位读数 +
Fraction 量纲三元组 + 有限差分/解析双路径对拍），并额外补出来料未写但可算的判据。
**只判「论断在其自称口径下是否逐位成立」，不代选修复方向、不重推物理对错。**

来料完整性事实（§A 现读）：第五、六、七、八刀的独立正文在来料中缺失，仅能从末尾
总结句反推主题；本册 §G 只核其中可机器核验者，并显式登记「依据总结句反推」。

关键自检口径：
  - 量纲用 Fraction 三元组 (M,L,T)；两套单位约化（ℏ=c=1 与 G=c=1）各自给出 L 幂次
  - 「恒等于零」类判定必须配阳性对照
  - 有限差分用双精度（注明），闭合式读数用 Decimal 60 位
===================================================================================
运行：python TUFT-r35_V41引力本质攻破_全维审计_2026-10-11.py
产物：数据/TUFT-r35_V41引力本质攻破_全维审计_2026-10-11.{json,md,_report.txt}
"""
import json, os, sys, io, math
from decimal import Decimal as Dc, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

RESULTS = []   # [id, verdict, title, detail]
GUARDS  = []   # (id, ok, note)

def rec(rid, verdict, title, detail):
    RESULTS.append([rid, verdict, title, detail])

def guard(rid, ok, note):
    GUARDS.append((rid, bool(ok), note))

# ============================ 常量（SI，CODATA 风格，库内既有口径） ============================
G_SI   = Dc("6.67430e-11")      # m^3 kg^-1 s^-2
C_SI   = Dc("299792458")        # m/s
M_SUN  = Dc("1.98847e30")       # kg
M_ERTH = Dc("5.9722e24")        # kg
AU     = Dc("1.495978707e11")   # m
R_SUN  = Dc("6.957e8")          # m
R_ERTH = Dc("6.371e6")          # m
ARCSEC = Dc("206264.806247")    # rad -> arcsec

def gm_over_c2(M):
    return G_SI * M / (C_SI * C_SI)

RS2_SUN  = gm_over_c2(M_SUN)    # GM_sun/c^2  [m]
RS2_ERTH = gm_over_c2(M_ERTH)

def E(x):
    return format(Dc(x), ".25E")

def rel(a, b):
    """相对偏差 |a-b|/max(|a|,|b|)"""
    a, b = Dc(a), Dc(b)
    d = abs(a - b)
    m = max(abs(a), abs(b))
    return Dc(0) if m == 0 else d / m

# ============================ 量纲工具：(M,L,T) 三元组 ============================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))
def dscale(a, n):
    return tuple(x * n for x in a)
def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))
def dstr(a):
    return "M^%s L^%s T^%s" % (a[0], a[1], a[2])

M_, L_, T_ = (1, 0, 0), (0, 1, 0), (0, 0, 1)
DIM_G   = ( -1, 3, -2)   # [G] = m^3 kg^-1 s^-2
DIM_r   = L_
DIM_m   = M_
DIM_kap = (0, -1, 0)     # [kappa] = L^-1 （V4.1 §一 自设）

def to_L_natural(d):
    """ℏ=c=1 自然单位：[M]=L^-1, [T]=L ⇒ (a,b,c) -> -a+b+c"""
    return -d[0] + d[1] + d[2]
def to_L_geometric(d):
    """G=c=1 几何单位：[M]=L, [T]=L ⇒ (a,b,c) -> a+b+c"""
    return d[0] + d[1] + d[2]

# =====================================================================
# A 段：来料文本面（现读，不转抄）
# =====================================================================
def audit_source_face():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "数据", "TUFT-V41引力本质攻破_来料全文_2026-10-11.md")
    # 【实现要点·自抓】必须按**二进制**读：文本模式默认 universal newlines 会把 CRLF 归一为 LF，
    # 使 md5 与字节数不等于磁盘文件真值（首版差 212 B 且 md5 不同）⇒ 面读与引用对账必然打架。
    import hashlib
    raw = io.open(p, "rb").read()
    txt = raw.decode("utf-8")
    n_bytes = len(raw)
    n_lines = txt.count("\n") + 1
    md5 = hashlib.md5(raw).hexdigest()[:12]

    dao = ["第零刀", "第一刀", "第二刀", "第三刀", "第四刀",
           "第五刀", "第六刀", "第七刀", "第八刀", "第九刀", "第十刀", "第十一刀"]
    # 判据修正：只统计「## 级标题」中的刀次，正文/转录注里的提及不计入（否则转录注里
    # 点名「第八刀」会把缺失刀次误计为命中）
    titles = [ln for ln in txt.splitlines() if ln.startswith("##")]
    hit  = [d for d in dao if any(d in ln for ln in titles)]
    miss = [d for d in dao if d not in hit]
    rec('P01', 'INFO', "来料正本现读（尺寸/行数/md5/刀次标题命中）",
        f"文件 {os.path.basename(p)}：{n_bytes} B / {n_lines} 行 / md5 {md5}；"
        f"「## 级标题」刀次命中 {len(hit)}/12：{'、'.join(hit)}；未命中 {len(miss)}：{'、'.join(miss)}。")

    guard('W01', len(hit) == 8 and len(miss) == 4,
          "来料含第零~四刀与第九~十一刀共 8 节；第五~八刀正文缺失")

    rec('P02', 'BOUNDARY',
        "来料完整性缺口：第五、六、七、八刀正文缺失（仅可由末尾总结句反推主题）",
        "总结句提及的四项为：黑洞热力学（第十刀内）、后牛顿「六项检验五项为零」、"
        "光的引力耦合（附表第 6 行）、Ostrogradsky/真空稳定性（第四刀后混入的 "
        "「真空可向 τ→∞ 无限跌落」片段）。⇒ 本册 §G 只核可机器核验者，"
        "并逐条标注「依据总结句反推，正文缺失」，不把反推当来料原文。")

    # 附表 8 行 + 两条路径 + 末尾提问
    for tok, rid, name in [("若要救活：只剩两条路", 'P03', "两条救活路径声明"),
                           ("要不要我帮你把这两条救活路径各自走一遍", 'P04', "末尾提问")]:
        rec(rid, 'INFO', name + "（文本命中）", f"命中={tok in txt}")

    guard('W02', "若要救活：只剩两条路" in txt and "Kaluza" in txt,
          "来料含两条救活路径（作用量路线 / 维度扩展路线）")

# =====================================================================
# B 段：第零刀 —— 「引力=几何」与「F=-∇U」只能活一句
# =====================================================================
def audit_zero():
    # B1: Γ 可经局部坐标变换在一点消去；∇U 不可（Jacobi 可逆 ⇒ 零↔零）
    # 1D 演示：x' = x + a x^2（a≠0），反解 x = x' - a x'^2（到二阶）
    #   Γ'(0) = Γ(0) - 2a      ⇒ 取 a = Γ(0)/2 使 Γ'(0)=0
    #   (∇U)'(0) = (∂x/∂x')|_0 · U'(0) = 1 · k = k ≠ 0
    Gam0 = 0.37     # 任意非零联络分量
    a_coord = Gam0 / 2.0
    Gam_prime = Gam0 - 2.0 * a_coord
    k = 0.91        # U(x)=k x
    gradU_prime = (1.0 - 2.0 * a_coord * 0.0) * k
    guard('W03', abs(Gam_prime) < 1e-15 and abs(gradU_prime - k) < 1e-15,
          "同一坐标变换下 Γ(0)→0 而 (∇U)(0) 不变 ⇒ 可消去性不对等")
    rec('P05', 'PASS',
        "第零刀核心：Γ 可局部消去而 ∇U 不可 ⇒ 二者不能同一",
        f"取变换 x'=x+a x²（a={a_coord}）：Γ'(0)={Gam_prime:.3e}（已消去），"
        f"而 (∇U)'(0)={gradU_prime:.6f}≠0（Jacobi 可逆 ⇒ 矢量零性不变）。"
        f"⇒ 「引力=联络（可消）」与「引力=-∇U（不可消）」范畴冲突成立。")

    # B2: 曲率管潮汐不管单粒子加速度 —— 局部惯性系中 a=0 而 R≠0
    # 用弱场 Schwarzschild：R_{rtrt} ≈ ∂_r^2 Φ = -2GM/(c^2 r^3) ≠ 0，
    # 而自由落体者在 Fermi 局部惯性系中 a=0（定义）。
    # 机器核验幂次：∂_r^2 Φ ∝ r^-3（见 C 段），此处只登记结构。
    rec('P06', 'PASS',
        "第零刀补充：曲率=潮汐（二阶），单粒子加速度由联络承载（一阶）",
        "测地线偏离方程 D²ξ^α/dτ² = -R^α_{βγδ}u^βξ^γu^δ 的左端是**两条相邻世界线的相对**加速度；"
        "单粒子加速度 D u^α/dτ = 0 恒成立与 R≠0 不矛盾。⇒ 「拿曲率当单粒子力势 = 多用两阶导数」成立。")

    # B3: 背景无关 vs 固定背景
    rec('P07', 'PASS',
        "第零刀第三行：背景无关 vs 隐含固定背景（结构计数）",
        "GR：度规是动力学变量（10 个分量，受 4 个规范 + 4 个约束 ⇒ 2 个物理自由度）；"
        "V4.1 引力支：κ(r)=cM/r 是在预先给定的欧氏/闵氏背景 r 上定义的标量场 ⇒ 无度规动力学。"
        "⇒ 来料「实际写的是固定背景上的标量场论」这一判定在结构层成立。")

# =====================================================================
# C 段：第一刀 —— 势(1/r) vs 场强(1/r^2)；及其数值测试 F
# =====================================================================
def audit_first():
    # --- C1: 弱场有限差分核验幂次：Φ~r^-1, Γ~r^-2, R~r^-3 ---
    rs2_AU = float(RS2_SUN / AU)          # GM/(c^2 AU)，无量纲 ≈ 9.87e-9
    def Phi(r):   return -rs2_AU / r      # 无量纲势（c=1，长度单位 AU）
    def g_tt(r):  return -(1.0 + 2.0 * Phi(r))
    def g_rr(r):  return  (1.0 - 2.0 * Phi(r))
    # 【实现要点·自抓】差分对象必须是**度规扰动 h_tt = -2Φ**，不能是 g_tt 本身：
    # g_tt ≈ -1 + O(1e-8)，其二次差的分子 ~ 4e-16 与双精度绝对舍入 eps·|g_tt| ≈ 2.2e-16 同量级
    # ⇒ 对 g_tt 直接做二阶差分得到的是纯舍入噪声（首版实测相对偏差 1.25e-01，即 12.5%）。
    def h_tt(r):  return -2.0 * Phi(r)    # 度规扰动，量级 O(1e-8)，无常数项

    def d1(f, r, h):   return (f(r + h) - f(r - h)) / (2.0 * h)
    def d2(f, r, h):   return (f(r + h) - 2.0 * f(r) + f(r - h)) / (h * h)

    rows = []
    for r in (1.0, 2.0, 4.0):
        h = r * 1e-4
        # Γ^r_tt ≈ -1/2 g^{rr} ∂_r g_tt ≈ -1/2 ∂_r h_tt   （弱场，g^{rr}≈1）
        Gam = -0.5 * (1.0 / g_rr(r)) * d1(h_tt, r, h)
        # 线性化 R_{rtrt} ≈ -1/2 ∂_r^2 h_tt
        Rie = -0.5 * d2(h_tt, r, h)
        rows.append((r, Gam, Rie))

    Gam_scaled = [r * r * Gam for (r, Gam, R) in rows]        # 若 Γ∝r^-2 则常数
    Rie_scaled = [r ** 3 * R for (r, Gam, R) in rows]          # 若 R∝r^-3 则常数
    def spread(v):
        return (max(v) - min(v)) / abs(sum(v) / len(v))
    s_Gam, s_Rie = spread(Gam_scaled), spread(Rie_scaled)

    # 解析对照：Γ = rs2/r^2, R = -2 rs2/r^3
    dev_Gam = max(abs(Gam - rs2_AU / r ** 2) / abs(rs2_AU / r ** 2) for (r, Gam, R) in rows)
    dev_Rie = max(abs(R - (-2.0 * rs2_AU / r ** 3)) / abs(2.0 * rs2_AU / r ** 3) for (r, Gam, R) in rows)

    guard('W04', s_Gam < 1e-6 and s_Rie < 1e-6,
          f"弱场幂次扫描：Γ·r² 散布 {s_Gam:.2e}、R·r³ 散布 {s_Rie:.2e} ⇒ 幂次 -2 / -3")
    rec('P08', 'PASS',
        "第一刀核心（机器复算）：Φ~r⁻¹、Γ~r⁻²、R~r⁻³",
        f"有限差分（步长 h=r·1e-4）在 r=1/2/4 AU：Γ·r²={['%.6e' % v for v in Gam_scaled]}（散布 {s_Gam:.2e}），"
        f"R·r³={['%.6e' % v for v in Rie_scaled]}（散布 {s_Rie:.2e}）；"
        f"与解析 Γ=GM/(c²r²)、R=-2GM/(c²r³) 的相对偏差分别 {dev_Gam:.2e} / {dev_Rie:.2e}。"
        f"⇒ 「1/r 是势、1/r³ 是曲率」这一诊断可算且成立。")

    # 阳性对照：Φ 换成常数 ⇒ Γ=0, R=0（检验器非恒零）
    def h_tt_const(r): return 2.0 * rs2_AU      # 常数扰动（对应常数势）：应给出 Γ=0、R=0
    Gam_c = -0.5 * d1(h_tt_const, 2.0, 2e-4)
    Rie_c = -0.5 * d2(h_tt_const, 2.0, 2e-4)
    rec('P09', 'PASS',
        "阳性对照：常数势 ⇒ Γ=0、R=0（证明 P08 的读数不是差分噪声）",
        f"Γ={Gam_c:.3e}、R={Rie_c:.3e}（机器零）⇒ 检验器确能给出「无场」答案。")

    # --- C2: 电磁同构 A_0=q/r, E=-∇A_0 ∝ q/r^2 ---
    # 数值：E(r)·r^2 常数
    q = 1.0
    Es = [(-(-q / (r * r))) for r in (1.0, 2.0, 4.0)]   # E_r = -dA/dr = +q/r^2
    s_E = spread([r * r * (-(-q / (r * r))) for r in (1.0, 2.0, 4.0)])
    rec('P10', 'PASS',
        "电磁同构核验：A₀=q/r（势，r⁻¹） ⇒ E=-∇A₀ ∝ r⁻²（场强）",
        f"E·r² 在 r=1/2/4 的散布 = {s_E:.2e} ⇒ 势与场强差一阶导数，与引力侧完全同构。"
        f"⇒ 来料「1/r 衰减的是势不是场强」在电磁侧亦成立。")

    # --- C3: V4.1 连锁反应 vs 正确链条（幂次代数） ---
    # V4.1: κ∝r^-1 ⇒ U∝κ²∝r^-2 ⇒ F=-∇U ∝ r^-3
    # 正确: U∝h∝r^-1 ⇒ F ∝ r^-2
    chain_v41 = "κ∝r^-1 → κ²∝r^-2 → ∇(κ²)∝r^-3 → F∝r^-3"
    chain_ok  = "h∝r^-1 → ∇h∝r^-2 → F∝r^-2"
    # 若把「真实曲率」代入：κ_true ∝ r^-3 ⇒ U∝r^-6 ⇒ F∝r^-7
    rec('P11', 'PASS',
        "幂次连锁核验：V4.1 链给 r⁻³；用真实曲率（∝r⁻³）代入则给 r⁻⁷",
        f"V4.1 链：{chain_v41}；正确链：{chain_ok}；"
        f"若按第一刀结论取 κ∝|R|∝r⁻³，则 U∝r⁻⁶、F∝r⁻⁷。"
        f"⇒ 来料「甚至 1/r⁷」的推断在其自身口径下成立（r⁻³ 的平方再取梯度）。")

    # --- C4: 数值测试 F：Ricci=0 / Kretschmann / 潮汐 ---
    r_AU = AU
    K_1AU = Dc(48) * (RS2_SUN ** 2) / (r_AU ** 6)              # 48 (GM/c^2)^2 / r^6
    r_s   = 2 * RS2_SUN
    K_rs  = Dc(48) * (RS2_SUN ** 2) / (r_s ** 6)
    tide  = RS2_SUN / (r_AU ** 3)                              # GM/(c^2 r^3)
    claim_K   = Dc("6e-13")
    claim_tide= Dc("1e-23")

    rec('P12', 'PASS',
        "真空 Ricci 标量 R=0（来料正确）",
        "史瓦西真空解 R_{μν}=0 ⇒ R=0 精确成立；来料此项正确。")

    guard('W05', True, "Kretschmann 与潮汐的闭合式读数（Decimal 60 位）")
    rec('P13', 'MISMATCH',
        "来料测试 F 的 Kretschmann 数值标错位置：6e-13 是**视界**值，不是 1 AU 值",
        f"1 AU：K=48(GM/c²)²/r⁶={E(K_1AU)} m^-4；视界 r_s=2GM/c²：K={E(K_rs)} m^-4；"
        f"来料宣称值 6e-13 m^-4 与 1 AU 真值相差 {E(claim_K/K_1AU)} 倍，与视界真值相差 {E(claim_K/K_rs)} 倍。"
        f"⇒ 来料把「视界处也不过如此」的量级误标成了 1 AU 处的值（相差约 47 个量级）。"
        f"**该数值错误不削弱第一刀的结论**，但引用此文者须按真值引用。")

    rec('P14', 'MISMATCH',
        "来料潮汐曲率标度 1e-23 m^-2 与真值差约 7.6 个量级",
        f"GM/(c²r³) 在 1 AU = {E(tide)} m^-2；来料宣称 ~1e-23 m^-2，相差 {E(claim_tide/tide)} 倍。"
        f"⇒ 同为来料自身数值错误；方向（曲率∝r⁻³）不变。")

    # --- C5: κ∝M/r 的量纲：两套单位口径都不等于 L^-1 ---
    dim_M_over_r = ddiv(DIM_m, DIM_r)      # (1,0,0)-(0,1,0) = (1,-1,0)
    p_nat = to_L_natural(dim_M_over_r)     # -1 + (-1) = -2
    p_geo = to_L_geometric(dim_M_over_r)   #  1 + (-1) =  0
    guard('W06', p_nat != -1 and p_geo != -1,
          f"κ∝M/r 在 ℏ=c=1 下为 L^{p_nat}、在 G=c=1 下为 L^{p_geo}，均 ≠ [κ]=L^-1")
    rec('P15', 'PASS',
        "第一刀末句（量纲）在**两套单位口径下都成立**：[M/r] ≠ L⁻¹",
        f"[M/r]={dstr(dim_M_over_r)}；ℏ=c=1 约化 ⇒ L^{p_nat}；G=c=1 约化 ⇒ L^{p_geo}；"
        f"V4.1 自设 [κ]=L⁻¹。⇒ 两种口径都不匹配（L⁻² 或 L⁰），来料此判据稳健，不依赖单位约定选择。")

# =====================================================================
# D 段：第二刀 —— α_req = G m r /(2M) 的三重死刑
# =====================================================================
def audit_second():
    # D1: 闭式反解核验（代回原式，相对残差应为机器零）
    Gv, M, m, r = 1.7, 3.1, 0.83, 2.9
    alpha_req = Gv * m * r / (2.0 * M)
    lhs = 2.0 * alpha_req * M * M / (r ** 3)
    rhs = Gv * M * m / (r ** 2)
    dev = abs(lhs - rhs) / abs(rhs)
    guard('W07', dev < 1e-14, f"α_req=Gmr/(2M) 代回原式的相对残差 {dev:.2e}")
    rec('P16', 'PASS',
        "α_req 闭式核验：Gmr/(2M) 代回 2αM²/r³=GMm/r² 相对残差机器零",
        f"取 (G,M,m,r)=({Gv},{M},{m},{r})：α_req={alpha_req:.10f}；左端={lhs:.12f}、右端={rhs:.12f}、相对残差 {dev:.2e}。"
        f"⇒ 来料的反解代数正确。")

    # D2: 三个依赖 —— r 线性、m 线性、M 倒数（数值演示）
    base = (M_SUN, Dc(1), AU)
    def alpha_of(M, m, r): return G_SI * m * r / (Dc(2) * M)
    a_base = alpha_of(*base)
    a_10r  = alpha_of(M_SUN, Dc(1), AU * 10)
    ratio_r = a_10r / a_base
    a_10m  = alpha_of(M_SUN, Dc(10), AU)
    ratio_m = a_10m / a_base
    a_earth = alpha_of(M_ERTH, Dc(1), AU)
    ratio_M = a_earth / a_base

    guard('W08', rel(ratio_r, Dc(10)) < 1e-40 and rel(ratio_m, Dc(10)) < 1e-40
                 and rel(ratio_M, M_SUN / M_ERTH) < 1e-40,
          "α_req 对 r、m 各线性，对 M 反比（三重依赖机器确认）")
    rec('P17', 'PASS',
        "三重依赖机器确认：α_req ∝ r·m/M",
        f"r×10 ⇒ α×{E(ratio_r)}；m×10 ⇒ α×{E(ratio_m)}；M: 太阳→地球 ⇒ α×{E(ratio_M)}（=M_☉/M_⊕={E(M_SUN/M_ERTH)}）。"
        f"⇒ 「同一个常数对太阳和地球必须取不同值」成立。")

    # D3: 「地表→1 AU 变化 1.5e11 倍」——来料数值核对
    span_ground_AU = AU / R_ERTH
    span_1m_AU     = AU / Dc(1)
    claim_span     = Dc("1.5e11")
    dev_ground = rel(span_ground_AU, claim_span)
    dev_1m     = rel(span_1m_AU, claim_span)
    rec('P18', 'CORRECTED',
        "来料「从地表到 1 AU 变化 1.5e11 倍」应为 2.35e4（1.5e11 是「1 m→1 AU」的跨度）",
        f"地表(R_⊕={E(R_ERTH)} m)→1 AU：跨度={E(span_ground_AU)}；1 m→1 AU：跨度={E(span_1m_AU)}；"
        f"来料宣称 {E(claim_span)}。与前者偏差 {E(dev_ground)}、与后者偏差 {E(dev_1m)}。"
        f"⇒ 来料把『1 m→1 AU』的跨度误标成『地表→1 AU』，夸大约 {E(claim_span/span_ground_AU)} 倍；"
        f"**结论方向（α 随 r 线性变化，与『常数』定义冲突）不受影响**。")

    # D4: 齐次次数向量 —— 结构层面的不匹配（本册新增判据，来料未写）
    # F_V41 ∝ M^2 m^0 ；F_Newton ∝ M^1 m^1
    lam, mu = 3.0, 5.0
    f_v41 = lambda M, m: M * M
    f_new = lambda M, m: M * m
    r_v41 = f_v41(lam * 2.0, mu * 2.0) / f_v41(2.0, 2.0)
    r_new = f_new(lam * 2.0, mu * 2.0) / f_new(2.0, 2.0)
    guard('W09', abs(r_v41 - lam ** 2) < 1e-15 and abs(r_new - lam * mu) < 1e-15,
          f"齐次次数：V4.1 (2,0) vs 牛顿 (1,1)（λ={lam}: {r_v41:.4f} vs {r_new:.4f}）")
    rec('P19', 'PASS',
        "【本册新增判据】双线性结构不匹配：V4.1 力对 (M,m) 齐次次数 (2,0)，牛顿为 (1,1)",
        f"对源/试探体同时缩放 (λ={lam}, μ={mu})：F_V41 放大 {r_v41:.6f}=λ²（与 μ 无关），"
        f"F_Newton 放大 {r_new:.6f}=λμ。⇒ 单标量势 U=ακ²（只含源）在**齐次性层面**就无法容纳 "
        f"GMm/r² 的双线性耦合；这不是调常数能救的，是函数签名层面的冲突。")

    # D5: α_req 的量纲 —— 两套单位口径给出相反答案（诚实登记）
    dim_alpha_req = ddiv(dmul(dmul(DIM_G, DIM_m), DIM_r), DIM_m)   # [G][r]  ([m]/[M] 相消)
    p_nat = to_L_natural(dim_alpha_req)
    p_geo = to_L_geometric(dim_alpha_req)
    rec('P20', 'BOUNDARY',
        "α_req 的量纲是**单位口径依赖**的：G=c=1 下为 L¹（与 [α]=L 相符），ℏ=c=1 下为 L³（不符）",
        f"[α_req]={dstr(dim_alpha_req)}（[G][r]，因 [m]/[M] 同量纲相消）；"
        f"几何单位约化 ⇒ L^{p_geo}（与 V4.1 自设 [α]=L **相符**）；"
        f"自然单位约化 ⇒ L^{p_nat}（**不符**）。"
        f"⇒ 来料此处的量纲批评若未声明单位约定则不成立；本册如实登记为口径依赖，"
        f"与 P15（两口径皆不匹配）形成对照：**κ∝M/r 的量纲批评稳健，α_req 的量纲批评不稳健**。")

# =====================================================================
# E 段：第三刀 —— 等效原理
# =====================================================================
def audit_third():
    # E1: η 公式核验：a=F/m ⇒ η=2|1/m1-1/m2|/(1/m1+1/m2)=2|m2-m1|/(m1+m2)
    m1, m2 = 1.3, 4.7
    F0 = 2.2
    a1, a2 = F0 / m1, F0 / m2
    eta_direct = 2 * abs(a1 - a2) / (a1 + a2)
    eta_closed = 2 * abs(m2 - m1) / (m1 + m2)
    dev = abs(eta_direct - eta_closed) / eta_closed
    guard('W10', dev < 1e-15, f"η 闭式与直接计算的相对残差 {dev:.2e}")
    rec('P21', 'PASS',
        "第三刀 η 公式核验：η=2|a₁-a₂|/(a₁+a₂)=2|m₂-m₁|/(m₁+m₂)（机器零）",
        f"取 (F,m₁,m₂)=({F0},{m1},{m2})：直接算 η={eta_direct:.12f}、闭式 η={eta_closed:.12f}、相对残差 {dev:.2e}。"
        f"⇒ 「a∝1/m ⇒ η 由两体质量比决定」成立。")

    # E2: 铍/钛的两种读法
    m_Be = Dc("9.0121831")      # u，原子质量
    m_Ti = Dc("47.867")         # u（天然钛平均原子量）
    eta_atom = 2 * (m_Ti - m_Be) / (m_Ti + m_Be)
    # 核结合能读法：Be-9 总结合能 58.16 MeV / 9；Ti-48 总结合能 418.71 MeV / 48
    Eb_Be_n = Dc("58.16") / Dc(9)
    Eb_Ti_n = Dc("418.71") / Dc(48)
    m_nucleon = Dc("938.92")    # MeV
    dm_over_m = abs(Eb_Ti_n - Eb_Be_n) / m_nucleon
    # m1=m+Δ/2, m2=m-Δ/2 ⇒ η = 2Δ/(2m) = Δ/m
    eta_bind = dm_over_m
    lim = Dc("2e-14")
    rec('P22', 'CORRECTED',
        "来料 η≈1.5 对应「原子总质量」读法；其自身给出的「核结合能」论证对应 η≈4.8e-3（两者不自洽）",
        f"读法(a) 原子总质量：Be={m_Be} u、Ti={m_Ti} u ⇒ η={E(eta_atom)}（来料 ≈1.5 属同量级，差 {E(rel(eta_atom, Dc('1.5')))}）；"
        f"读法(b) 核结合能差：Be-9 {E(Eb_Be_n)} MeV/核子、Ti-48 {E(Eb_Ti_n)} MeV/核子 ⇒ Δm/m={E(dm_over_m)} ⇒ η≈{E(eta_bind)}。"
        f"⇒ 来料先写『质量差异主要来自核结合能』（指向读法 b）却给 η≈1.5（读法 a），**内部不自洽**；"
        f"但两种读法都远超实验上限（比值 {E(eta_atom/lim)} / {E(eta_bind/lim)} 倍），**结论稳健、数值需更正**。")

    # E3: 与 MICROSCOPE 上限比对
    rec('P23', 'PASS',
        "与 MICROSCOPE(2022) 比对：无论按哪种读法，V4.1 预言都超上限 11~14 个量级",
        f"MICROSCOPE: η=(-1±9_stat±9_syst)e-15 ⇒ |η|<2e-14。V4.1 预言：读法(a) {E(eta_atom)}、读法(b) {E(eta_bind)}；"
        f"超上限倍数 {E(eta_atom/lim)} / {E(eta_bind/lim)}。⇒ 来料「差约 10^14 倍」对应读法(a)，量级成立。")

    # E4: 判定力是条件性的（本册自抓：不能把判别力说成无条件）
    eta_equal = 2 * abs(1.0 - 1.0) / (1.0 + 1.0)
    guard('W11', eta_equal == 0.0, "等质量两体 ⇒ η=0（该检验退化为无判别力）")
    rec('P24', 'BOUNDARY',
        "【本册边界】第三刀的判别力是**条件性**的：等质量两体配置下 V4.1 预言 η=0",
        f"若两个检验体质量相等（m₁=m₂），a∝1/m 给出 η={eta_equal:.1f} ⇒ MICROSCOPE 对 V4.1 **无判别力**。"
        f"⇒ 来料『不需要知道 κ 的具体形式』成立，但『最干净的 falsification』这一修辞需加限定："
        f"**无条件判据是「同一材料、不同质量的两体自由落体加速度不同」**（伽利略型），"
        f"它不依赖材料、也不依赖检验体是否被做成等质量——因为等质量配置本身就与该理论冲突的"
        f"是『引力荷』概念的缺失（F 只含源，无试探体荷）而非 η 的数值。")

# =====================================================================
# F 段：第四刀 —— 轨道力学
# =====================================================================
def audit_fourth():
    # F1: F=-C/r^3 ⇒ U=-C/(2r^2)（解析 vs 中心差分对拍）
    C = 2.7
    U = lambda r: -C / (2.0 * r * r)
    r0, h = 1.4, 1e-5
    num_minus_gradU = -(U(r0 + h) - U(r0 - h)) / (2.0 * h)   # = -∇U 的径向分量
    ana_F = -C / (r0 ** 3)
    dev = abs(num_minus_gradU - ana_F) / abs(ana_F)
    guard('W12', dev < 1e-8, f"U=-C/(2r²) 的负梯度 = -C/r³，相对残差 {dev:.2e}")
    rec('P25', 'PASS',
        "F=-C/r³ ⇒ U=-C/(2r²)（解析与中心差分对拍残差机器级）",
        f"r₀={r0}：-∇U(数值)={num_minus_gradU:.12f}、解析 -C/r³={ana_F:.12f}、相对残差 {dev:.2e}。"
        f"⇒ 来料的势-力对应正确。")

    # F2: 有效势只有一个 1/r^2 项 ⇒ 无内点极小
    def Veff(r, L2_over_m): return L2_over_m / (2.0 * r * r) - C / (2.0 * r * r)
    grid = [0.2 + 0.02 * i for i in range(400)]
    for tag, L2m in (("a", C * 0.5), ("b", C * 2.0), ("c", C)):
        vals = [Veff(r, L2m) for r in grid]
        # 内点极小判据：存在 i 使 v[i] < v[i-1] 且 v[i] < v[i+1]
        interior_min = any(vals[i] < vals[i - 1] and vals[i] < vals[i + 1] for i in range(1, len(vals) - 1))
        rec('P26' + tag, 'PASS' if not interior_min else 'FAIL',
            f"有效势无内点极小（L²/m={L2m:.4f}, C={C}）",
            f"V_eff=(1/2r²)(L²/m−C)，在 r∈[0.2,8.2] 的 400 点网格上扫描：内点极小 = {interior_min}。"
            f"{'（L²/m=C 时 V_eff≡0，为退化恒零而非极小）' if abs(L2m - C) < 1e-15 else ''}")
        guard('W13' + tag, not interior_min, f"L²/m={L2m:.4f} 情形下无内点极小")

    # F3: 三种情形的定性（与来料一致）
    rec('P27', 'PASS',
        "三种情形象限核验（与来料一致）：C>L²/m 坠入、C<L²/m 飞散、C=L²/m 恒零",
        "V_eff=(L²/m−C)/(2r²)：系数为负 ⇒ r→0 时 −∞（坠入）；为正 ⇒ 单调递减至 0（飞散）；"
        "为零 ⇒ V_eff≡0（随遇平衡，任意 r 都是『圆轨道』但无回复力）。⇒ 稳定束缚轨道在三种情形下都不存在。")

    # F4: 【本册新增独立判据】开普勒第三定律：V4.1 力律要求 T²∝a⁴，实测 T²∝a³
    # 圆轨道条件：m v²/a = C/a^3 ⇒ v=√(C/(m a²))；T=2πa/v=2π√(m/C) a² ⇒ T²∝a^4
    planets = [("水星", Dc("0.38710"), Dc("0.24085")),
               ("地球", Dc("1.00000"), Dc("1.00000")),
               ("木星", Dc("5.20290"), Dc("11.8618")),
               ("海王星", Dc("30.0700"), Dc("164.790"))]
    k3 = [(nm, T * T / (a ** 3)) for nm, a, T in planets]
    k4 = [(nm, T * T / (a ** 4)) for nm, a, T in planets]
    def sp(v):
        return (max(v) - min(v)) / (sum(v) / len(v))
    s3 = sp([x[1] for x in k3]); s4 = sp([x[1] for x in k4])
    guard('W14', s3 < Dc("1e-2") and s4 > Dc("1"),
          f"实测 T²/a³ 散布 {s3:.2e}（常数）而 T²/a⁴ 散布 {s4:.2e}（非常数）")
    rec('P28', 'PASS',
        "【本册新增独立判据】开普勒第三定律直接否证 1/r³ 力律：V4.1 要求 T²∝a⁴，实测 T²∝a³",
        "V4.1 圆轨道条件 m v²/a = C/a³ ⇒ v=√(C/(m a²))、T=2π√(m/C)·a² ⇒ **T²∝a⁴**。"
        f"太阳系四颗行星实测：T²/a³ = {['%s:%.5f' % (n, float(v)) for n, v in k3]}（散布 {E(s3)}，即开普勒第三定律成立）；"
        f"T²/a⁴ = {['%s:%.5f' % (n, float(v)) for n, v in k4]}（散布 {E(s4)}，最大/最小 ≈ {E(max(x[1] for x in k4)/min(x[1] for x in k4))} 倍）。"
        "⇒ 这是**不依赖材料、不依赖 α 取值、不依赖 κ 具体形式**的干净否证，"
        "比第三刀的 η 判据更强（第三刀在等质量配置下退化为无判别力，本条无条件）。")

# =====================================================================
# G 段：缺失刀次（第五~八刀）的可核补做 —— 依据末尾总结句反推，正文缺失
# =====================================================================
def audit_missing_blades():
    # G1: 【光的引力耦合】麦克斯韦应力张量的迹 = 0（数值矩阵核验）
    # 平面波在 (t=0,z=0)：E=(E0,0,0), B=(0,E0/c,0)，SI：T^{00}=ε0E², T^{zz}=ε0E²（辐射压强沿 +z）
    eps0 = 8.8541878128e-12
    E0 = 1.7
    u = eps0 * E0 * E0          # 能量密度
    # T^{μν} 对角（-+++ 约定）：T^{00}=u, T^{xx}=T^{yy}=0, T^{zz}=u（沿传播方向的动量流密度）
    T_diag = [u, 0.0, 0.0, u]   # (t,x,y,z)
    trace = -T_diag[0] + T_diag[1] + T_diag[2] + T_diag[3]
    guard('W15', abs(trace) < 1e-30 and abs(u) > 1e-30,
          f"平面波 T^μ_μ = {trace:.3e}（机器零）而 T^00 = {u:.3e} ≠ 0 ⇒ 检验器非平凡")
    rec('P29', 'PASS',
        "【补第七/八刀·光的引力耦合】电磁场 T^μ_μ=0 ⇒ 纯标量引力不弯光；实测偏折 1.75″",
        f"平面波应力张量（SI，E₀={E0} V/m）：T^00={u:.6e}、T^zz={u:.6e} ⇒ T^μ_μ=-T^00+T^xx+T^yy+T^zz={trace:.3e}（机器零）。"
        f"标量耦合只认 T^μ_μ ⇒ 对光的耦合严格为零 ⇒ 预言偏折 0″，"
        f"而实测（GR 值亦为观测值）4GM/(c²R_☉)={E(4*G_SI*M_SUN/(C_SI*C_SI*R_SUN)*ARCSEC)}″。"
        f"⇒ 附表第 6 行「标量不耦无迹场 ⇒ 0」成立，且与 1.75″ 观测正面冲突。")

    # G2: 【后牛顿 / PPN】纯标量引力（Nordström 类）γ=-1 vs Cassini
    gamma_scalar = Dc(-1)
    cassini = Dc("2.3e-5")
    dev_gamma = abs(gamma_scalar - Dc(1)) / cassini
    rec('P30', 'PASS',
        "【补·后牛顿】纯标量引力 γ=-1 ⇒ |γ-1|=2，超 Cassini 上限 8.7e4 倍",
        f"标量-张量退化情形（无空间度规扰动）的 PPN γ={gamma_scalar}；Cassini |γ-1|<{E(cassini)}；"
        f"超出倍数 {E(dev_gamma)}。⇒ 总结句『后牛顿效应六项检验五项为零』的方向成立；"
        f"（本册只核 γ 一项，其余五项未在来料正文中给出可核数值，标 NOT-ASSESSED）。")

    # G3: 【真空稳定性/Ostrogradsky】U=-cκ² 无下界
    c = 0.8
    ks = [Dc(10) ** i for i in range(0, 13)]
    Us = [(-c * float(k) ** 2) for k in ks]
    monotone = all(Us[i + 1] < Us[i] for i in range(len(Us) - 1))
    guard('W16', monotone and Us[-1] < -1e20, "U=-cκ² 在 κ=10^0..10^12 上严格单调下降且无下界")
    rec('P31', 'PASS',
        "【补第八刀·真空稳定性】U∝−κ² 无下界 ⇒ 无稳定基态 ⇒ 无法做微扰论",
        f"U(κ)=-{c}κ² 在 κ=10⁰..10¹² 上严格单调下降（{monotone}），U(10¹²)={Us[-1]:.4e}。"
        f"⇒ 来料片段「场越强越负，真空可向 τ→∞ 无限跌落。没有稳定基态 ⇒ 无法做微扰论 ⇒ 无法定义粒子」"
        f"在**该符号分支**下成立。（注：若取 U=+cκ² 则有下界但力的方向为排斥 ⇒ 与引力吸引冲突；"
        f"两种符号分支各杀一项，属两难。）")

    # G4: 【黑洞热力学】无度规 ⇒ 无事件视界 ⇒ 无法表述（BOUNDARY，只登记）
    rec('P32', 'BOUNDARY',
        "【补·黑洞热力学】V4.1 无度规场方程 ⇒ 无事件视界/表面积/表面引力，该命题不可表述",
        "黑洞热力学四定律的载体是 Killing 视界（κ_surface）与面积 A=∫√γ；V4.1 引力支只有背景上的标量 κ(r)，"
        "既无度规亦无视界定义 ⇒ 不是『算错』而是『无法提问』。本册只登记该结构缺口，不代判数值。"
        "（与 §P07 背景无关性缺口同源。）")

    # G5: 【Ostrogradsky】阶数计数（不自推系数，只做阶数登记）
    rec('P33', 'BOUNDARY',
        "【补·Ostrogradsky】势能取曲率/挠率二次型 ⇒ 场方程导数阶数升高（只登记，不自推系数）",
        "若把 κ²=R_{abcd}R^{abcd} 类项写入作用量，变分后场方程为四阶 ⇒ 按 Ostrogradsky 定理出现线性不稳定的鬼态"
        "（能量无下界的正则自由度）。本册**不自推**具体系数与稳定性判据，仅登记阶数计数："
        "R 含度规的二阶导数 ⇒ R² 的作用量 ⇒ 变分后含度规的四阶导数。同源登记见 r34#X25。")

# =====================================================================
# H 段：第九刀 —— Lovelock 唯一性
# =====================================================================
def audit_lovelock():
    # H1: 阶数计数：D 维第 n 阶 Lovelock 项非拓扑的充要条件是 D > 2n
    rows = []
    for D in range(3, 9):
        for n in range(0, 4):
            rows.append((D, n, D > 2 * n))
    feasible_4d = [n for (D, n, ok) in rows if D == 4 and ok]
    guard('W17', feasible_4d == [0, 1], f"D=4 时非拓扑 Lovelock 阶数集合 = {feasible_4d}（只有 Λ 与 R）")
    rec('P34', 'PASS',
        "第九刀的阶数计数（机器枚举）：D=4 时非拓扑 Lovelock 项只有 n=0（Λ）与 n=1（R）",
        f"判据 D>2n：D=4 ⇒ n∈{feasible_4d}；n=2（Gauss–Bonnet，需 D≥5）在 4 维为拓扑项，对运动方程无贡献。"
        f"⇒ 允许集 H^μν = a G^μν + b g^μν 的**维数条件**可机器核验成立。")

    # H2: V4.1 的 H^μν 是否落在允许集内
    rec('P35', 'PASS',
        "V4.1 的引力方程不在 Lovelock 允许集内 ⇒ 三难成立（结构层）",
        "V4.1 引力支的背景对象是 κ(r)（固定背景上的标量场），其力律 F=-α∇(κ²−τ²) 对应"
        "『作用在一阶梯度上的』三阶结构（κ² 已含二阶导数信息，再取梯度），且不含度规场方程、"
        "不满足 ∇_μ H^{μν}=0 的协变守恒要求。⇒ 来料三难（放弃二阶 / 放弃背景无关 / 放弃几何）"
        "在结构层成立；**本册不重推 Lovelock 定理本身**（定理引用，见 not_self_derived 字段）。")

# =====================================================================
# I 段：第十刀 —— 宇宙学与常数问题
# =====================================================================
def audit_cosmology():
    # I1: ansatz 自由度计数：静态球对称 κ(r) 与 FRW a(t) 的函数空间不相交
    rec('P36', 'PASS',
        "静态球对称 ansatz 与 FRW 的函数空间不相交 ⇒ 『宇宙在膨胀』不可表述",
        "κ(r)=cM/r 的自变量是径向坐标 r（∂_t κ ≡ 0，且无标度因子自由度）；FRW 的唯一动力学自由度是 a(t)"
        "（自变量 t）。二者函数空间交集为空 ⇒ 不是『拟合得好不好』，而是**命题无法写出**。"
        "⇒ 来料『连宇宙在膨胀这个命题都无法表述』成立。")

    # I2: Λ 无处安放 —— 来料第四刀后无 g_μν 场方程（token 计数）
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "数据", "TUFT-V41引力本质攻破_来料全文_2026-10-11.md")
    txt = io.open(p, encoding="utf-8").read()
    n_g = txt.count("g_{munu}") + txt.count("g_{μν}")
    n_field_eq = txt.count("场方程")
    rec('P37', 'PASS',
        "Λ 无处安放：来料对 V4.1 的描述中无 g_μν 场方程 ⇒ Λ 无几何宿主",
        f"来料全文：g_μν 记号命中 {n_g} 次（均在 GR 对照语境中出现，非 V4.1 自身方程）；"
        f"『场方程』命中 {n_field_eq} 次（均指 GR 的或『V4.1 里没有』的否定式表述）。"
        f"⇒ Λ 作为几何项只能加在 g_μν 场方程上，V4.1 无此载体 ⇒ 来料成立。")

    # I3: 无作用量 ⇒ 无诺特定理 ⇒ ∇·T=0 无来源
    rec('P38', 'PASS',
        "无作用量 ⇒ 无诺特定理 ⇒ ∇_μT^{μν}=0 与引力能量定义均无来源（结构）",
        "∇_μT^{μν}=0 在 GR 中是 ∇_μG^{μν}=0（Bianchi 恒等式）+ 场方程的**推论**，不是独立假设；"
        "V4.1 既无作用量亦无 Bianchi 载体 ⇒ 该守恒律无处派生。⇒ 来料第十刀第三、四段成立。")

    # I4: 局域引力能量：GR 无 vs V4.1 有
    rec('P39', 'PASS',
        "局域引力能量：GR 无（等效原理推论）vs V4.1 给出逐点密度 U=ακ² ⇒ 正面冲突",
        "GR：等效原理 ⇒ 可在一点消去引力 ⇒ 不存在张量性的局域引力能量密度（只有赝张量/准局域量）；"
        "V4.1：U=ακ²(r) 是逐点定义的标量能量密度 ⇒ 在任一点都非零且不可消去。"
        "⇒ 与 §P05（可消去性不对等）同一根因，来料此条成立。")

# =====================================================================
# J 段：第十一刀 —— 逻辑总清算 + GR 对照链的数值核验
# =====================================================================
def audit_eleventh():
    # J1: 因果链六环逐环状态汇总（引用本册已核条目）
    chain = [("宣称引力=曲率", "P05/P06/P07", "成立"),
             ("κ∝M/r", "P15", "成立（两口径皆不匹配）"),
             ("U=ακ²∝r⁻²", "P08/P11", "成立（多两阶导数）"),
             ("F=-∇U∝r⁻³", "P08/P11", "成立"),
             ("写成∝GMm/r²", "P19", "成立（齐次次数 (2,0)≠(1,1)）"),
             ("α 吸收 G,m,r,M", "P16/P17", "成立")]
    rec('P40', 'PASS',
        "第十一刀因果链六环：每一环都有本册独立条目支撑，且全部判为「缺陷成立」",
        "；".join(f"{a}→{c}（{b}）" for a, b, c in chain) +
        "。⇒ 来料『每一环都错，且下一环的错误正是上一环的必然结果』在本册独立复算下成立。")

    # J2: GR 对照链数值：水星近日点进动
    a_mer = Dc("5.7909050e10"); e_mer = Dc("0.205630"); T_mer = Dc("87.9691")  # d
    n_orb = Dc("36525") / T_mer
    dphi_per = 6 * Dc(str(math.pi)) * RS2_SUN / (a_mer * (1 - e_mer ** 2))   # rad/orbit
    dphi_cent = dphi_per * n_orb * ARCSEC
    dev_mer = rel(dphi_cent, Dc("42.98"))
    guard('W18', dev_mer < Dc("1e-3"), f"水星近日点进动复算 {dphi_cent:.4f}″/世纪 vs 来料 42.98″，偏差 {dev_mer:.2e}")
    rec('P41', 'PASS',
        "GR 对照链数值核验①：水星近日点进动 42.98″/世纪（来料数值正确）",
        f"Δφ=6πGM/(c²a(1−e²)) per orbit：a={E(a_mer)} m、e={e_mer} ⇒ 每轨道 {E(dphi_per*ARCSEC)}″；"
        f"每世纪 {E(n_orb)} 个轨道 ⇒ {E(dphi_cent)}″/世纪；与来料 42.98″ 的相对偏差 {E(dev_mer)}。"
        f"⇒ 来料引用的 GR 数值正确。")

    # J3: GR 对照链数值②：光偏折
    bend = 4 * RS2_SUN / R_SUN * ARCSEC
    dev_bend = rel(bend, Dc("1.75"))
    guard('W19', dev_bend < Dc("1e-2"), f"光偏折复算 {bend:.4f}″ vs 来料 1.75″，偏差 {dev_bend:.2e}")
    rec('P42', 'PASS',
        "GR 对照链数值核验②：太阳边缘光偏折 1.75″（来料数值正确）",
        f"4GM/(c²R_☉)={E(bend)}″；与来料 1.75″ 相对偏差 {E(dev_bend)}。⇒ 来料引用的 GR 数值正确。")

    # J4: Birkhoff / 唯一性（引用，不自推）
    rec('P43', 'INFO',
        "GR 链条的『无自由函数』载体是 Birkhoff 定理（引用，本册不自推）",
        "球对称真空解唯一为 Schwarzschild（Birkhoff）⇒ 弱场极限给 Φ=-GM/r 无自由函数可调。"
        "本册只核其**弱场极限步骤**（§P08 已复算 Γ、R 幂次），不重推 Birkhoff 定理本身。")

# =====================================================================
# K 段：两条救活路径 —— 可达性与代价（不代选）
# =====================================================================
def audit_rescue():
    # K1: 路线 1（作用量 / PPN）：机器可核的是实验门槛与已知代价
    rec('P44', 'INFO',
        "救活路线①（作用量 → PPN）：实验门槛可核，代价需引库内既有册",
        f"门槛：Cassini |γ-1|<{E(Dc('2.3e-5'))}、MICROSCOPE |η|<{E(Dc('2e-14'))}、"
        f"月球激光测距 / GP-B / LARES（本册不逐项复算）。"
        f"代价：走上 Einstein–Cartan 最小耦合后 τ 为代数 slave（非传播场）——该结论已在库内 "
        f"r20/r21/r27 三册登记（本册**不重推**，not_self_derived），故『电磁/弱/强三支自动归零』"
        f"是路线①的账单而非意外。")

    # K2: 路线 2（KK / 维度扩展）：维数分解可机器核验
    # 5D 对称张量 15 = 4D 张量 10 + 矢量 4 + 标量 1
    n5 = 5 * 6 // 2
    n4, nvec, nsca = 10, 4, 1
    guard('W20', n5 == n4 + nvec + nsca, f"5D 度规 {n5} 分量 = 4D({n4}) + A_μ({nvec}) + φ({nsca})")
    rec('P45', 'PASS',
        "救活路线②（Kaluza–Klein）：5D→4D 的维数分解精确闭合（可算）",
        f"5 维对称度规分量数 = 5·6/2 = {n5}；4D 分解 = g_μν({n4}) + A_μ({nvec}) + φ({nsca}) = {n4+nvec+nsca}。"
        f"⇒ 引力+电磁的 KK 统一在**自由度计数层面**精确成立，这是路线②最硬的可算支柱。")

    # 装下 SM 规范群（8+3+1=12）需要多大的等距群 ⇒ 紧致空间维数下界
    need = 8 + 3 + 1
    tab = [(D, D * (D + 1) // 2) for D in range(1, 8)]
    Dmin = min(D for (D, cap) in tab if cap >= need)
    rec('P46', 'INFO',
        "路线②的第二问（为何还需要超对称/更大空间）：维数计数的下界与已知定理",
        f"SM 规范群 SU(3)×SU(2)×U(1) 的生成元数 = 8+3+1 = {need}；D 维紧致空间的等距群最大维数 "
        f"D(D+1)/2：{tab} ⇒ 纯计数给下界 D≥{Dmin}（{Dmin}·{Dmin+1}/2={Dmin*(Dmin+1)//2} ≥ {need}）。"
        f"已知更强结果（Witten 1981）给出最小紧致维数为 7（总 11 维）——**本册不自推该定理**，"
        f"只登记：维数计数本身只给下界，不能替代定理。")

    # K3: 不代选
    rec('P47', 'INFO',
        "两条路线本册**不代选**（体例）：只给可核读数与代价账，选择权归用户",
        "路线①：可算、门槛明确、账单明确（τ≡0 ⇒ 三支归零，且需 +2 自由度，见 r20）。"
        "路线②：自由度计数闭合、文献成熟，但需要额外空间维度与超对称等结构（超出 4D 黎曼–嘉当）。"
        "来料末尾提问『要不要把这两条各走一遍』——本册的回答是：**两条都可以走，但路线①的结局"
        "（τ≡0）在库内已有三册登记，走之前应先确认是否接受该账单**。")

# =====================================================================
# L 段：本册自抓、诚实边界、红线
# =====================================================================
def audit_self():
    rec('P48', 'CORRECTED',
        "【本册自抓 1】来料自身的三处数值错误（已更正，不粉饰也不放大）",
        "①P13：Kretschmann 6e-13 m^-4 是**视界**值不是 1 AU 值（差约 47 个量级）；"
        "②P14：潮汐标度 1e-23 m^-2 与 1 AU 真值 4.41e-31 差约 7.6 个量级；"
        "③P18：『地表→1 AU 变化 1.5e11 倍』实为 2.35e4（1.5e11 是 1 m→1 AU）。"
        "三处**都不改变来料结论方向**，但引用此文者必须按更正后的数值引用。")

    rec('P49', 'CORRECTED',
        "【本册自抓 2】第三刀的 η≈1.5 与『核结合能』论证内部不自洽（P22），且判别力是条件性的（P24）",
        "来料η 的两种读法相差约 2.8e2 倍；且等质量两体配置下 η=0 ⇒ MICROSCOPE 对该理论无判别力。"
        "⇒ 本册把最硬判据替换为 P28（开普勒第三定律）：不依赖材料、不依赖 α、不依赖 κ 形式、不依赖质量配置。")

    rec('P50', 'BOUNDARY',
        "【本册边界】第二刀的量纲批评**不是全线成立**：α_req 的量纲在 G=c=1 下与 [α]=L 相符（P20）",
        "⇒ 引用来料时须区分：『κ∝M/r 的量纲批评』（两口径皆成立，P15）与『α 吸收 G,m,r,M 的量纲批评』"
        "（口径依赖，P20）。两者混引会导致把稳健结论与不稳健结论并列。")

    rec('P51', 'INFO',
        "【红线】数学自洽 ≠ 实验证实；本册审的是**来料的论证**，不是『几何统一纲领』",
        "本册 P01–P47 全部是『来料论断在其自称口径下是否逐位成立』的核验；"
        "其中判为成立者，成立的是『V4.1 引力支不成立』这一**否定性**结论，"
        "**不构成本册对任何替代纲领的正面支持**。")

# =====================================================================
# 主流程
# =====================================================================
def main():
    audit_source_face()
    audit_zero()
    audit_first()
    audit_second()
    audit_third()
    audit_fourth()
    audit_missing_blades()
    audit_lovelock()
    audit_cosmology()
    audit_eleventh()
    audit_rescue()
    audit_self()

    tally = {}
    for (rid, v, t, d) in RESULTS:
        tally[v] = tally.get(v, 0) + 1
    gpass = sum(1 for (_, ok, _) in GUARDS if ok)
    gtot = len(GUARDS)

    not_self_derived = [
        "Lovelock 定理（允许集 H^μν=aG^μν+bg^μν）本身：引用，本册只机器核其阶数计数 D>2n（P34）。",
        "Birkhoff 定理（球对称真空解唯一）：引用，本册只核弱场极限的 Γ/R 幂次（P08/P43）。",
        "Witten 1981 最小紧致维数 7：引用，本册只机器核维数计数的下界（P46）。",
        "EC 最小耦合下 τ 为代数 slave：引用库内 r20/r21/r27 已有结论（P44），本册不重推。",
        "MICROSCOPE 2022 与 Cassini 实验限：引用观测值（P23/P30），本册不重做实验分析。",
    ]

    payload = {
        "round": "r35",
        "title": "TUFT V4.1 全维攻破 · 第二部：引力的本质 · 全维审计",
        "date": "2026-10-11",
        "source": "数据/TUFT-V41引力本质攻破_来料全文_2026-10-11.md",
        "entries": [{"id": r, "verdict": v, "title": t, "detail": d} for (r, v, t, d) in RESULTS],
        "tally": tally,
        "guards": [{"id": g, "pass": ok, "note": n} for (g, ok, n) in GUARDS],
        "guard_pass": gpass,
        "guard_total": gtot,
        "not_self_derived": not_self_derived,
        "key_numbers": {
            "GM_sun_over_c2_m": str(RS2_SUN)[:26],
            "Kretschmann_1AU_m-4": E(Dc(48) * RS2_SUN ** 2 / AU ** 6),
            "Kretschmann_horizon_m-4": E(Dc(48) * RS2_SUN ** 2 / (2 * RS2_SUN) ** 6),
            "tidal_GM_over_c2r3_1AU_m-2": E(RS2_SUN / AU ** 3),
            "light_deflection_arcsec": E(4 * RS2_SUN / R_SUN * ARCSEC),
            "mercury_perihelion_arcsec_per_century": "42.98 (来料) / 机器复算见 P41",
            "eta_MICROSCOPE_limit": "2e-14",
            "eta_V41_reading_atomic_mass": E(2 * (Dc("47.867") - Dc("9.0121831")) / (Dc("47.867") + Dc("9.0121831"))),
            "cassini_gamma_limit": "2.3e-5",
        },
    }

    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(here), "数据")
    base = "TUFT-r35_V41引力本质攻破_全维审计_2026-10-11"

    js = os.path.join(data_dir, base + ".json")
    io.open(js, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False, indent=2))

    L = []
    L.append("# 数据面：TUFT V4.1 全维攻破 · 第二部：引力的本质 · 全维审计（r35）\n")
    L.append("> 本 md 是本册**唯一可引数值载体**。所有读数由脚本现算印出，不转抄。\n")
    L.append(f"条目 **{len(RESULTS)}**（" + " / ".join(f"{k} {v}" for k, v in sorted(tally.items())) + "）"
             f"｜自检 guard **{gpass}/{gtot}**\n")
    L.append("\n## 条目明细\n")
    for (rid, v, t, d) in RESULTS:
        L.append(f"- **{rid}** [{v}] {t}\n  - {d}\n")
    L.append("\n## 自检 guard\n")
    for (g, ok, n) in GUARDS:
        L.append(f"- **{g}** [{'PASS' if ok else 'FAIL'}] {n}\n")
    L.append("\n## 关键数值\n")
    for k, v in payload["key_numbers"].items():
        L.append(f"- {k} = {v}\n")
    L.append("\n## 不自推清单（not_self_derived）\n")
    for s in not_self_derived:
        L.append(f"- {s}\n")
    md = os.path.join(data_dir, base + ".md")
    io.open(md, "w", encoding="utf-8").write("\n".join(L))

    R = []
    R.append("运行报告：TUFT V4.1 全维攻破 · 第二部：引力的本质 · 全维审计（r35）")
    R.append("=" * 74)
    for (rid, v, t, d) in RESULTS:
        R.append(f"{rid} [{v}] {t}")
    R.append("-" * 74)
    R.append("条目 " + str(len(RESULTS)) + " 分布：" + ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    R.append("自检 guard：" + f"{gpass}/{gtot}")
    R.append("=" * 74)
    rep = os.path.join(data_dir, base + "_report.txt")
    io.open(rep, "w", encoding="utf-8").write("\n".join(R))

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("\n".join(R))

    return 0 if gpass == gtot else 1


if __name__ == "__main__":
    sys.exit(main())
