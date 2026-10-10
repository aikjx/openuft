# -*- coding: utf-8 -*-
"""
TUFT 垂直原理螺旋统一场论 ·「统一势结构完整性」攻破（r25）

来料：同 r22/r23/r24 的《四力大统一：垂直原理螺旋统一场论》（V9.0 全书 + V9.1 续篇）
分工（三册已覆盖，本册不重算）：
  - r22（48 条）：L0 公设 / L1 恒等式 / L2 场论 / L3 经典极限 / L5 参数边界
  - r23（33 条）：续篇第八~十章 + 附录 D
  - r24（30 条）：全书第一~七章 + 附录 A/B/C 的增量与复发（电子半径定量否证 W06、
        标量 Proca 自旋 0 与 GR 冲突 W10、两条禁闭修复方案可行性 W14/W16、垂直原理
        推理链 W18、路线图裁定 W26）
  - **本册只攻一个问题**：来料的核心声称是「四力可以写入同一个统一势函数
    U = s·ℏc·q₁q₂·e^{−r/λ}/r」。本册逐项清点该势的**构成要件是否齐备**，
    并给出「这个统一到底统一了什么」的机器裁定。

五个清点维度：
  A 荷 q 的定义完整性（4 力中定义了几个？）
  B 场 κ 与势 U 之间的映射（有方程吗？）
  C 动力学完整性（有时间和 τ 的方程吗？）
  D 量纲/数值闭合与「预言力」（λ=∞ 的退化分支能否被检验？）
  E 归一裁定与最小修补清单

引擎：纯标准库（Decimal 60 位 + Fraction 量纲层）
评级：O / L2
"""

from decimal import Decimal, getcontext
from fractions import Fraction
import json
import os
import sys

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "数据")
os.makedirs(DATA_DIR, exist_ok=True)

BASENAME = "TUFT-垂直原理统一势结构完整性攻破_2026-10-10"

# ---------------------------------------------------------------- 常数
C_LIGHT = Decimal("299792458")
HBAR = Decimal("1.054571817e-34")
G_N = Decimal("6.67430e-11")
Q_E = Decimal("1.602176634e-19")
EPS0 = Decimal("8.8541878128e-12")
ALPHA = Decimal("7.2973525693e-3")
M_E = Decimal("9.1093837015e-31")
M_PROTON = Decimal("1.67262192369e-27")
M_W_GEV = Decimal("80.377")
M_PI0_MEV = Decimal("134.9768")

M_PLANCK = (HBAR * C_LIGHT / G_N).sqrt()
L_PLANCK = (HBAR * G_N / C_LIGHT ** 3).sqrt()
HBAR_C = HBAR * C_LIGHT                       # J·m

# 弱力（自然单位，GeV）
G_F = Decimal("1.1663787e-5")                 # GeV^-2
M_W_NAT = M_W_GEV                             # GeV
ALPHA_EM_MZ = Decimal("1") / Decimal("127.955")
SIN2_THETA = Decimal("0.23121")

# 外部实验上限（[C] 人工锚）
M_PHOTON_LIMIT_EV = Decimal("1e-18")          # PDG 光子质量上限量级
M_GRAVITON_LIMIT_EV = Decimal("1.27e-22")     # LIGO/Virgo 引力子质量上限


def ev_to_kg(mev):
    return mev * Decimal("1e6") * Q_E / (C_LIGHT ** 2)


M_W = ev_to_kg(M_W_GEV * Decimal("1000"))
M_PI0 = ev_to_kg(M_PI0_MEV)
LAMBDA_W = HBAR / (M_W * C_LIGHT)
LAMBDA_PI = HBAR / (M_PI0 * C_LIGHT)

# ---------------------------------------------------------------- 工具
def fmt(x, n=25):
    if isinstance(x, Decimal):
        return format(x, "." + str(n) + "E")
    return format(Decimal(str(x)), "." + str(n) + "E")


def rel(a, b):
    a = Decimal(a)
    b = Decimal(b)
    if b == 0:
        return Decimal("Infinity") if a != 0 else Decimal(0)
    return abs(a - b) / abs(b)


DIM = {
    "c": (Fraction(1), Fraction(0), Fraction(-1)),
    "hbar": (Fraction(2), Fraction(1), Fraction(-1)),
    "r": (Fraction(1), Fraction(0), Fraction(0)),
    "E": (Fraction(2), Fraction(1), Fraction(-2)),
    "kappa": (Fraction(-1), Fraction(0), Fraction(0)),
    "one": (Fraction(0), Fraction(0), Fraction(0)),
}


def dim_mul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dim_pow(a, k):
    k = Fraction(k)
    return (a[0] * k, a[1] * k, a[2] * k)


ITEMS = []
GUARDS = []


def add_item(cid, verdict, title, detail, numbers=None, ref=""):
    ITEMS.append({"id": cid, "verdict": verdict, "title": title,
                  "detail": detail, "numbers": numbers or {}, "ref": ref})


def vpass(cid, t, d, n=None, ref=""):
    add_item(cid, "PASS", t, d, n, ref)


def vfail(cid, t, d, n=None, ref=""):
    add_item(cid, "FAIL", t, d, n, ref)


def vbound(cid, t, d, n=None, ref=""):
    add_item(cid, "BOUNDARY", t, d, n, ref)


def vmis(cid, t, d, n=None, ref=""):
    add_item(cid, "MISMATCH", t, d, n, ref)


def vinfo(cid, t, d, n=None, ref=""):
    add_item(cid, "INFO", t, d, n, ref)


def vcorr(cid, t, d, n=None, ref=""):
    add_item(cid, "CORRECTED", t, d, n, ref)


def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)


# 全书显式方程清单（同 r24 W12 口径，本册沿用并扩充）
INVENTORY = [
    ("§2.1", "κ = ρ/(ρ²+b²)"),
    ("§2.1", "τ = b/(ρ²+b²)"),
    ("§2.2", "α = τ/κ = b/ρ"),
    ("§2.3", "κ²+τ² = 1/(ρ²+b²)"),
    ("§2.4", "κ²+τ² = (ω/c)²"),
    ("§2.6", "(ρ,b) = (κ,τ)/(κ²+τ²)"),
    ("§2.7", "m = ℏω/c²"),
    ("§2.7", "ρ = ℏ/(mc√(1+α²))"),
    ("§3.1", "(∇²−μ²)κ = 0"),
    ("§3.1", "κ(r) = q·e^{−μr}/r"),
    ("§3.2", "lim_{μ→0} q e^{−μr}/r = q/r"),
    ("§3.3", "U = s·ℏc·q₁q₂·e^{−r/λ}/r"),
    ("§3.3", "q_G = m/m_P"),
    ("§3.3", "q_EM = √α·Z"),
    ("§3.3", "λ = ℏ/(mc)"),
    ("§3.4", "∇κ·∇τ = 0"),
    ("§4.1", "G = ℏc/m_P²"),
    ("§4.2", "ℏcα = e²/(4πε₀)"),
    ("§4.6", "F_E/F_G = α(m_P/m_p)²"),
    ("§4.7", "(∇²−μ²)(σr) = σ(2/r−μ²r)"),
    ("§4.7", "∇²κ − μ²κ + λκ³ = 0"),
]


# ================================================================ A 段：荷 q 的定义完整性
def section_A():
    # ---- Y01 四个力中定义了几个荷
    q_defs = [(_s, e) for (_s, e) in INVENTORY if e.strip().startswith("q_")]
    forces = ["引力", "电磁", "弱核力", "剩余强核力"]
    defined = {"引力": "q_G = m/m_P", "电磁": "q_EM = √α·Z", "弱核力": None, "剩余强核力": None}
    n_def = sum(1 for v in defined.values() if v)
    guard("Y01_charge_def_count", n_def == 2 and len(q_defs) == 2,
          "显式 q 定义 %d 条，已定义力 %d/%d" % (len(q_defs), n_def, len(forces)))
    vfail("Y01", "【头条】统一势的四个力中**只有 2 个定义了荷** ⇒ 「四力统一」实际只完成 2/4",
          "全书 §3.3 只给出 q_G=m/m_P（引力）与 q_EM=√α·Z（电磁）两条荷的定义；"
          "§4.3 弱核力与 §4.4 剩余强核力**只给了力程 λ_W、λ_π，从未给出 q_W 与 q_S**。"
          "⇒ 统一势 U=s·ℏc·q₁q₂·e^{−r/λ}/r 中，2/4 的力缺少使公式可算的那一半（荷）。"
          "这不是笔误而是**结构性缺口**：没有 q_W/q_S，这两个力的势无法被算出，"
          "§4.3/§4.4 的「力程匹配 PDG」实际上是**只核对了 λ、没核对 U** 的半程验证。",
          {"forces": forces, "defined_count": n_def, "total": len(forces),
           "missing": ["弱核力", "剩余强核力"]})

    # ---- Y02 若补齐 q_W：两条独立来源给同一个 α_W，但都是实验输入
    a_w_gf = (Decimal(2).sqrt() * G_F * M_W_NAT ** 2) / Decimal(str(3.14159265358979323846))
    a_w_theta = ALPHA_EM_MZ / SIN2_THETA
    d_aw = rel(a_w_gf, a_w_theta)
    guard("Y02_alpha_W_two_routes_agree", d_aw < Decimal("1e-2"),
          "α_W(G_F,M_W)=%s vs α_W(α_em,sin²θ)=%s，相对差 %s" % (fmt(a_w_gf, 12), fmt(a_w_theta, 12), fmt(d_aw, 6)))
    vinfo("Y02", "补齐 q_W=√α_W 后两条独立来源数值一致，但两者都是实验输入 ⇒ 零信息量",
          "按标准关系 g²/(8M_W²)=G_F/√2 反解 α_W=g²/(4π)=√2·G_F·M_W²/π = %s；"
          "另一路由 α_em(M_Z)/sin²θ_W = %s/%s = %s。两条独立路径相对差 %.2E ⇒ 数值自洽。"
          "但注意：G_F、M_W、α_em、sin²θ_W **全是实验测量值**，螺旋几何对 α_W 没有任何贡献"
          "（同 r24 W03 的换源不变性）⇒ 该一致性是标准模型内部的一致性，不是本理论的预言。"
          "⇒ 记 INFO：补齐 q_W 在技术上是可行的，代价是再加一个外部常数。"
          % (fmt(a_w_gf, 12), fmt(ALPHA_EM_MZ, 10), fmt(SIN2_THETA, 8), fmt(a_w_theta, 12), d_aw),
          {"alpha_W_from_GF": fmt(a_w_gf, 12), "alpha_W_from_theta": fmt(a_w_theta, 12),
           "rel_diff": fmt(d_aw, 6)})

    # ---- Y03 强力荷 q_S：低能非微扰 + 强跑动
    a_s_mz = Decimal("0.1179")
    a_s_low = Decimal("1")  # 低能非微扰量级示意
    spread = a_s_low / a_s_mz
    vbound("Y03", "强力荷 q_S 无定义，若取 √α_s 则该常数**不是常数**（低能非微扰 + 强跑动）",
           "强力在 M_Z 处 α_s=%s（微扰可用），在 1 fm/低能区进入非微扰（量级 O(1)）⇒ 跨 %.3E 倍。"
           "统一势要求 q_S 是**一个**无量纲数，而 α_s 是随能标强跑动的量；"
           "且低能 QCD 的束缚/禁闭不是单玻色子交换势（这正是来料 §4.7 自陈的 FAIL）。"
           "⇒ 即便补齐 q_S，也只能在「介子交换的有效力」层面用（与 r23 P01「三力 + 一个有效力」同构）。"
           % (fmt(a_s_mz, 6), spread),
           {"alpha_s_MZ": float(a_s_mz), "spread_low_over_MZ": float(spread)},
           ref="同 r23 P01")

    # ---- Y04 符号机制不一致：引力靠 s 手工指定，电磁靠 Z 自动
    q_g_pos = M_PROTON / M_PLANCK
    vfail("Y04", "引力荷恒正 ⇒ 引力「只吸引」靠符号因子 s 手工指定；与电磁的符号机制不同源",
          "q_G=m/m_P > 0 恒成立（质子 %s、电子 %s 皆正），因此 q₁q₂ 无法给出排斥；"
          "引力只能是吸引这件事完全由 §3.3 的符号因子 s 手工指定。"
          "而电磁 q_EM=√α·Z 的 Z 可正可负 ⇒ 同号相斥、异号相吸是**荷的代数自动给出的**。"
          "⇒ 两种力的符号来自两套完全不同的机制：一个是外加的手工符号，一个是荷自身的代数。"
          "「垂直原理」若真要统一四力，至少应给出「为什么引力的荷恒正」的来源；全书没有。"
          "⇒ 这构成第 5 条未登记的外部输入（与 §5.3 自陈的「耦合常数外部输入」不同族，需单列）。"
          % (fmt(q_g_pos, 12), fmt(M_E / M_PLANCK, 12)),
          {"q_G_proton": fmt(q_g_pos, 12), "q_G_electron": fmt(M_E / M_PLANCK, 12)})


# ================================================================ B 段：场 κ 与势 U 的映射
def section_B():
    # ---- Y05 是否存在 U = f(κ) 的方程
    hits = [(s, e) for (s, e) in INVENTORY if "U" in e and ("κ" in e or "τ" in e)]
    guard("Y05_scan_zero_hits", len(hits) == 0, "含 U 且含 κ/τ 的方程数 = %d" % len(hits))
    vfail("Y05", "【本册核心】全书**没有** U=f(κ) 的方程 ⇒ §3.1 的场与 §3.3 的势之间无推导关系",
          "对全书 %d 条显式方程扫描「同时出现 U 与 κ（或 τ）」⇒ 命中 **%d** 条。"
          "§3.1 给出场 κ(r)=q·e^{−μr}/r（Proca 解），§3.3 给出势 U=s·ℏc·q₁q₂·e^{−r/λ}/r，"
          "两者形式相似但**没有任何方程把 U 与 κ 连起来**：κ 是曲率场（量纲 L⁻¹），U 是势能（量纲能量），"
          "全书既没写 U∝κ，也没写 U∝κ² 或 U=ℏc·κ 之类。⇒ 第三章的两节是**并列罗列**而非推导链；"
          "「四力统一」实际是「把四个已知势抄成同一个函数形式」，场论部分（Proca）与势部分（统一势）"
          "各说各话。可复算判据：若真有映射，方程清单中至少有一条同时含 U 与 κ；实际为 0。"
          % (len(INVENTORY), len(hits)),
          {"inventory_size": len(INVENTORY), "hits": len(hits)})

    # ---- Y06 §3.1 与 §4.7 代入的是不同量纲的对象（范畴混装）
    dim_kappa = DIM["kappa"]                                   # L^-1
    dim_sigma_r = DIM["E"]                                     # 弦张力 σ = 能量/长度 ⇒ σr = 能量
    dim_mismatch = (dim_kappa != dim_sigma_r)
    guard("Y06_dims_differ", dim_mismatch, "[κ]=%s vs [σr]=%s" % (str(dim_kappa), str(dim_sigma_r)))
    vfail("Y06", "§3.1 与 §4.7 代入同一 Proca 算子的对象**量纲不同** ⇒ 范畴混装",
          "§3.1 的 (∇²−μ²)κ=0 中 κ 是曲率场，量纲 [κ]=%s（L⁻¹）；"
          "§4.7 检验「(∇²−μ²)(σr)」时，σr 是**势**（弦张力 σ = 能量/长度 ⇒ [σr]=%s）。"
          "同一个算子在这两节里作用在两个不同量纲、不同物理范畴的对象上 ⇒ "
          "「齐次 Proca 无法容纳禁闭势」这个结论，严格说是**把势塞进场的方程**后得到的，"
          "其有效性依赖「κ 就是势」这一未在书中写明、且与 §2.1 的 κ=ρ/(ρ²+b²) 量纲冲突的额外假设。"
          "⇒ 与 r24 W17 登记的 O-CONF-V9 同源，但本册指出它在**全书层面**就已存在（不只是孤子处）。"
          % (str(dim_kappa), str(dim_sigma_r)),
          {"dim_kappa": str(dim_kappa), "dim_sigma_r": str(dim_sigma_r)},
          ref="升级 r24 W17 / O-CONF-V9")

    # ---- Y07 μ 与 λ 的一致性（唯一闭合项）
    mu_from_lambda_w = Decimal(1) / LAMBDA_W
    mu_direct = M_W * C_LIGHT / HBAR
    d_mu = rel(mu_from_lambda_w, mu_direct)
    m_back = mu_from_lambda_w * HBAR / C_LIGHT
    d_m = rel(m_back, M_W)
    guard("Y07_mu_lambda_consistent", d_mu < Decimal("1e-45") and d_m < Decimal("1e-45"),
          "μ 两路相对差 %s，反解 M_W 相对差 %s" % (fmt(d_mu, 6), fmt(d_m, 6)))
    vpass("Y07", "μ 与 λ 的成对定义自洽：μ=1/λ=mc/ħ（全书唯一严格闭合的场-势联系）",
          "由 λ_W=%s m 反解 μ=%s m⁻¹，与直接计算 M_Wc/ħ=%s m⁻¹ 相对差 %s；"
          "反解质量 M_W=%s kg 与输入相对差 %s ⇒ 机器零。"
          "⇒ 这是全书**唯一**一处「力程参数 ↔ 场方程参数」的严格闭合（μ↔λ），值得记为 PASS；"
          "但它只是同一个定义 mc/ħ 的两种写法，属定义一致而非物理推导。"
          % (fmt(LAMBDA_W, 12), fmt(mu_from_lambda_w, 12), fmt(mu_direct, 12), fmt(d_mu, 6),
             fmt(m_back, 12), fmt(d_m, 6)),
          {"lambda_W": fmt(LAMBDA_W, 12), "mu_from_lambda": fmt(mu_from_lambda_w, 12),
           "mu_direct": fmt(mu_direct, 12), "rel_diff": fmt(d_mu, 6)})


# ================================================================ C 段：动力学完整性
def section_C():
    # ---- Y08 全书无时间导数
    time_keys = ["∂/∂t", "∂_t", "□", "∂²/∂t²", "d/dt", "∂t"]
    t_hits = [(s, e) for (s, e) in INVENTORY for k in time_keys if k in e]
    guard("Y08_no_time_derivative", len(t_hits) == 0, "含时间导数的方程数 = %d" % len(t_hits))
    vfail("Y08", "全书方程**全部静态**（无 ∂/∂t、无 □）⇒ 不能描述波、辐射与光的传播",
          "对 %d 条显式方程扫描时间导数判据 %s ⇒ 命中 **%d** 条。"
          "§3.1 用的是静态 Helmholtz 型 (∇²−μ²)κ=0，而非完整的 Proca 方程 (□+μ²)A^μ=0。"
          "后果是决定性的：静态方程只有束缚/静势解，**没有行波解** ⇒ "
          "该理论在其现有形式下无法描述电磁波（光）、引力波，也无法给出传播速度 c 的场论来源"
          "——而 c 恰恰是全书第一公设的核心。⇒ 与 r24 W10（自旋 0）互补且独立："
          "W10 说的是「场的自旋错了」，本条说的是「连时间都没有」。"
          % (len(INVENTORY), "、".join(time_keys), len(t_hits)),
          {"time_hits": len(t_hits), "keys": time_keys})

    # ---- Y09 τ 场无动力学方程
    tau_dyn = [(s, e) for (s, e) in INVENTORY if "τ" in e and ("∇²" in e or "□" in e)]
    tau_any = [(s, e) for (s, e) in INVENTORY if "τ" in e]
    guard("Y09_tau_has_no_evolution_eq", len(tau_dyn) == 0,
          "含 τ 的动力学方程 %d 条（含 τ 的方程共 %d 条，均为定义式/约束）" % (len(tau_dyn), len(tau_any)))
    vfail("Y09", "τ 场**没有场方程** ⇒ 垂直原理在 L2 层只实现了一半（只有 κ 有动力学）",
          "含 τ 的方程共 %d 条：§2.1 的定义式、§2.2 的 α=τ/κ、§2.3/§2.4 的平方和、§2.6 的反演、"
          "§3.4 的约束 ∇κ·∇τ=0 —— **没有一条是 τ 的演化/场方程**（含 ∇² 或 □ 且以 τ 为解的为 %d 条）。"
          "⇒ 来料 §1.3 声称「弯曲动力学（κ）与扭转动力学（τ）天然解耦，构成四力分维承载」，"
          "但 L2 层只给了 κ 的方程 ⇒ τ 侧没有动力学可言，「分维承载四力」缺一半。"
          "这正是 r24 W03（场论层零几何残留）的机制性解释：**连 τ 的方程都没有，何来几何耦合**。"
          % (len(tau_any), len(tau_dyn)),
          {"tau_equations": len(tau_any), "tau_dynamical": len(tau_dyn),
           "tau_sections": [s for s, _ in tau_any]})

    # ---- Y10 若补 τ 方程的后果（引用 r22 C10，不重算）
    vbound("Y10", "若补齐 τ 的同类 Proca 方程，会直接撞上 r22 C10 的径向不相容定理",
           "r22 C10 已证：在来料自设的**径向汤川解**结构内，Proca + ∇κ·∇τ=0 + 两场皆有质量"
           "三者不可同时成立（κ′≠0 ⇒ 强制 τ′≡0 ⇒ 挠率场退化为空间常数）。"
           "⇒ 本册 Y09 指出的「缺 τ 方程」不能靠「照抄 κ 的方程」来补：一补就与 §3.4 的"
           "场梯度正交约束冲突。本册不重算 r22 C10，只登记这条**修补路径已被预先封死**。",
           ref="同 r22 C10")

    # ---- Y11 静态 Helmholtz ↔ Yukawa 解一致（数值验证）
    mu_v = 1.0
    r_v = 2.0
    h = 1e-5
    import math as _m

    def u_f(r):
        return _m.exp(-mu_v * r) / r

    def lap(r):
        # ∇²u = (1/r²) d/dr (r² u'(r))
        def g(rr):
            return rr * rr * (u_f(rr + h) - u_f(rr - h)) / (2 * h)
        return (g(r + h) - g(r - h)) / (2 * h) / (r * r)

    lap_v = lap(r_v)
    rhs_v = mu_v ** 2 * u_f(r_v)
    d_lap = abs(lap_v - rhs_v) / abs(rhs_v)
    guard("Y11_yukawa_solves_helmholtz", d_lap < 1e-6,
          "∇²u=%.12e vs μ²u=%.12e，相对差 %.3e" % (lap_v, rhs_v, d_lap))
    vpass("Y11", "Yukawa 势确为静态 Helmholtz 方程的解（数值残差在差分截断量级）⇒ §3.1 自洽",
          "取 μ=1、r=2，数值 ∇²(e^{−μr}/r) = %.12E，μ²u = %.12E，相对差 %.2E（差分截断量级）"
          "⇒ §3.1 的「场方程 ↔ 汤川解」这一步严格成立。注意作用域：仅 r>0（r=0 处有 δ 奇性，"
          "正是点源所在的点，全书未讨论源项）⇒ 与 Y05/Y08 的缺口无关，本条独立判 PASS。"
          % (lap_v, rhs_v, d_lap),
          {"laplacian_numeric": lap_v, "mu2_u": rhs_v, "rel_diff": d_lap})


# ================================================================ D 段：量纲闭合与「预言力」
def section_D():
    # ---- Y12 统一势量纲
    dim_u = dim_mul(DIM["hbar"], DIM["c"])
    dim_u = dim_mul(dim_u, dim_pow(DIM["r"], -1))
    guard("Y12_potential_dim_is_energy", dim_u == DIM["E"], "[ℏc/r]=%s" % str(dim_u))
    vpass("Y12", "统一势量纲闭合：[ℏc·q₁q₂/r] = 能量（Fraction 精确）",
          "[ℏc]=%s，除以 [r]=%s 得 %s，与能量 %s 严格相等（q 无量纲）⇒ §3.3 的量纲设计无误。"
          "这是全书最扎实的一条：势的**函数形式**确实能承载能量量纲（与 r24 W24 符号表一致）。"
          % (str(dim_mul(DIM["hbar"], DIM["c"])), str(DIM["r"]), str(dim_u), str(DIM["E"])),
          {"dim_hbar_c": str(dim_mul(DIM["hbar"], DIM["c"])), "dim_U": str(dim_u)})

    # ---- Y13 同一函数形式下的数值跨度
    r0 = Decimal("1e-15")
    j_to_mev = Decimal("1e-6") / Q_E          # J → MeV
    u_em = HBAR_C * ALPHA / r0
    alpha_g = G_N * M_PROTON ** 2 / HBAR_C
    u_g = HBAR_C * alpha_g / r0
    a_w = (Decimal(2).sqrt() * G_F * M_W_NAT ** 2) / Decimal(str(3.14159265358979323846))
    u_s = HBAR_C * Decimal("1") * (-r0 / LAMBDA_PI).exp() / r0
    u_w = HBAR_C * a_w * (-r0 / LAMBDA_W).exp() / r0
    span_sg = u_s / u_g
    span_eg = u_em / u_g
    guard("Y13_coulomb_cross_check", rel(u_em * j_to_mev, Decimal("1.43996")) < Decimal("1e-4"),
          "U_EM(1 fm)=%s MeV vs e²/(4πε₀r)=1.43996 MeV" % fmt(u_em * j_to_mev, 8))
    vinfo("Y13", "同一函数形式，四力系数跨近 40 个量级（电磁侧与库仑势逐位交叉印证）",
          "取 r=1 fm、统一势 U=ℏc·q₁q₂·e^{−r/λ}/r："
          "电磁 q₁q₂=α ⇒ U_EM=%s MeV（与教科书 e²/(4πε₀·1fm)=1.43996 MeV **逐位一致**，"
          "独立交叉印证统一势的电磁分支没错）；引力 q₁q₂=(m_p/m_P)²=%s ⇒ U_G=%s MeV；"
          "强力取 α_s=1（示意）⇒ U_S≈%s MeV（核力量级合理）；"
          "弱力 α_W=%s 但 e^{−r/λ_W}=e^{−%s} ⇒ U_W=%s MeV（**实际为零**）。"
          "⇒ 比值 U_S/U_G=%.3E、U_EM/U_G=%.3E —— 函数形式只有一个，系数却跨近 40 个量级。"
          "这就是「形式统一」的精确含义：统一的是**符号排版**，不是数值来源。"
          % (fmt(u_em * j_to_mev, 8), fmt(alpha_g, 10), fmt(u_g * j_to_mev, 8),
             fmt(u_s * j_to_mev, 8), fmt(a_w, 8), fmt(r0 / LAMBDA_W, 6), fmt(u_w * j_to_mev, 8),
             span_sg, span_eg),
          {"U_EM_MeV": fmt(u_em * j_to_mev, 8), "U_G_MeV": fmt(u_g * j_to_mev, 8),
           "U_S_MeV": fmt(u_s * j_to_mev, 8), "U_W_MeV": fmt(u_w * j_to_mev, 8),
           "alpha_G_proton": fmt(alpha_g, 10), "span_S_over_G": fmt(span_sg, 8),
           "span_EM_over_G": fmt(span_eg, 8)})

    # ---- Y14 λ=∞ 是退化分支
    vbound("Y14", "引力与电磁的 λ=∞ 是 μ→0 的**退化分支**，不是「力程由康普顿波长决定」的正常情形",
           "统一势的力程机制是 λ=ħ/(mc)；引力子与光子 m=0 ⇒ λ=∞ ⇒ 这两个力处在参数空间的**边界**上，"
           "e^{−r/λ}≡1，力程机制对它们不起作用。⇒ 四力中 2/4 由「有限力程机制」描述、2/4 由「退化」描述，"
           "统一势并未给这 4 个力一个统一的机制（同 r23 P02，本册确认并补上荷维度的对应缺口 Y01）。",
           ref="同 r23 P02")

    # ---- Y15 λ=∞ 与实验下限不可区分 ⇒ 零预言力
    hbarc_evm = HBAR_C / Q_E                       # J·m → eV·m
    lam_gamma = hbarc_evm / M_PHOTON_LIMIT_EV
    lam_grav = hbarc_evm / M_GRAVITON_LIMIT_EV
    guard("Y15_limits_are_finite", lam_gamma > 0 and lam_grav > 0,
          "λ_γ>%s m，λ_g>%s m" % (fmt(lam_gamma, 8), fmt(lam_grav, 8)))
    vinfo("Y15", "λ=∞ 与实验下限不可区分 ⇒ 统一势在长程力上**零预言力**（[C]）",
          "实验上限 [C]：光子质量 m_γ<%s eV ⇒ λ_γ>ħc/(m_γc²)=%s m；"
          "引力子质量 m_g<%s eV（LIGO/Virgo 量级）⇒ λ_g>%s m。"
          "理论取 λ=∞，实验只能约束 λ 大于 ~1e11~1e15 m ⇒ **任何足够大的 λ 都与实验一致**，"
          "理论值 ∞ 不落在可区分区间 ⇒ 该统一势对引力、电磁**不产生任何可检验的新预言**。"
          "⇒ 这条与 Y13 合起来给出「形式统一」的精确边界：短程力（弱/强）的 λ 可测，"
          "但那里荷未定义（Y01）；长程力的荷有定义，但那里 λ 不可测（本条）。"
          "**可算的部分与可测的部分恰好不重合** —— 这是本册对「统一」一词最锐利的机器裁定。"
          % (fmt(M_PHOTON_LIMIT_EV, 4), fmt(lam_gamma, 8), fmt(M_GRAVITON_LIMIT_EV, 4), fmt(lam_grav, 8)),
          {"lambda_gamma_lower_bound_m": fmt(lam_gamma, 8),
           "lambda_graviton_lower_bound_m": fmt(lam_grav, 8),
           "note": "[C] 外部实验上限，本册只做换算与归口"})


# ================================================================ E 段：归一裁定与最小修补
def section_E():
    vinfo("Y16", "四册归一：条目不可相加，本册是第 4 本（r22 48 / r23 33 / r24 30 / 本册 19）",
          "四册口径各不相同，不可相加。本册与前三册的关系：r22 攻**场论与参数边界**；"
          "r23 攻**续篇的仿真/对标/预言**；r24 攻**全书的定量否证与推理链**；"
          "**本册攻「统一」这个声称本身的结构完整性**。四册结论互相独立、方向一致，"
          "无一条相互矛盾。")

    vcorr("Y17", "r24 W17 登记的开放项 O-CONF-V9 应**升格**为全书级缺陷，而非孤子处的问题",
          "r24 W17 把「场-势映射缺失」登记为孤子修复方案处的开放项。本册 Y05 表明："
          "缺失的不是一个局部映射，而是**全书根本没有 U=f(κ) 的方程**；"
          "Y06 进一步表明 §3.1 与 §4.7 代入同一算子的对象量纲都不同。"
          "⇒ O-CONF-V9 应从「孤子路线缺一步」升格为「L2 层结构性缺口」，"
          "并作为 Y05/Y06 的上位条目。")

    vfail("Y18", "一句话裁定：该「统一」统一的是**函数形式与符号排版**，四个力中可算与可测恰好不重合",
          "把本册五条清点合起来："
          "① 荷：4 个力只定义 2 个（Y01），引力符号还是手工外加（Y04）；"
          "② 映射：场与势之间没有方程（Y05），且两处代入对象量纲不同（Y06）；"
          "③ 动力学：无时间（Y08）、τ 无方程（Y09）；"
          "④ 唯一闭合的是 μ↔λ 的定义一致（Y07）与势的量纲（Y12）；"
          "⑤ 可算的（弱/强，λ 可测）荷未定义，可测的（引力/电磁，荷有定义）λ 在退化分支且不可区分（Y14/Y15）。"
          "⇒ **没有哪一个力同时满足「荷已定义」且「λ 可检验」** ⇒ 统一势在现有形式下"
          "对任何一个力都没有产生超出已知物理的可检验推论。")

    vbound("Y19", "最小修补清单（按依赖序，本册不代选）",
           "若要在保留「垂直原理」的前提下让统一势成为可算理论，依赖序不可换："
           "**P0** 给出 U=f(κ) 的映射并统一量纲（修 Y05/Y06）——否则后面全部无从谈起；"
           "**P1** 把静态 Helmholtz 升级为含时间的方程（修 Y08）——否则没有波与光；"
           "**P2** 补 q_W、q_S 的定义并说明引力荷为何恒正（修 Y01/Y04）；"
           "**P3** 给 τ 的场方程（修 Y09），但须先解决与 §3.4 正交约束的冲突（r22 C10，Y10）；"
           "**P4** 才谈实验检验——且须先确认所选的力同时满足「荷已定义 + λ 可测」（Y15 的陷阱）。"
           "注意：P0–P3 每一步都引入新的自由度或新假设 ⇒ 与 openuft r14/r15 的「Ω5 自由常数 ≤1」"
           "约束直接冲突 ⇒ **修补本身就是公设集层面的决策，不是技术修补**。")


# ================================================================ 自检
def selfcheck():
    a_w_gf = (Decimal(2).sqrt() * G_F * M_W_NAT ** 2) / Decimal(str(3.14159265358979323846))
    a_w_theta = ALPHA_EM_MZ / SIN2_THETA
    guard("S1_alpha_W_routes", rel(a_w_gf, a_w_theta) < Decimal("1e-2"),
          "α_W 两路相对差 %s" % fmt(rel(a_w_gf, a_w_theta), 6))
    u_em = HBAR_C * ALPHA / Decimal("1e-15") * (Decimal("1e-6") / Q_E)
    guard("S2_coulomb_1fm", rel(u_em, Decimal("1.43996")) < Decimal("1e-4"),
          "U_EM(1fm)=%s MeV vs 1.43996" % fmt(u_em, 8))
    d_u = dim_mul(dim_mul(DIM["hbar"], DIM["c"]), dim_pow(DIM["r"], -1))
    guard("S3_dim_U", d_u == DIM["E"], "[ℏc/r]=%s" % str(d_u))
    guard("S4_mu_lambda", rel(Decimal(1) / LAMBDA_W, M_W * C_LIGHT / HBAR) < Decimal("1e-45"),
          "μ 相对差 %s" % fmt(rel(Decimal(1) / LAMBDA_W, M_W * C_LIGHT / HBAR), 6))
    guard("S5_charge_count", sum(1 for _s, e in INVENTORY if e.strip().startswith("q_")) == 2,
          "q_ 定义数 2")
    guard("S6_no_U_kappa_link", len([1 for _s, e in INVENTORY if "U" in e and ("κ" in e or "τ" in e)]) == 0,
          "U∧κ 命中 0")
    guard("S7_no_time", len([1 for _s, e in INVENTORY for k in ["∂/∂t", "∂_t", "□", "∂t"] if k in e]) == 0,
          "时间导数命中 0")
    guard("S8_tau_no_dynamics",
          len([1 for _s, e in INVENTORY if "τ" in e and ("∇²" in e or "□" in e)]) == 0,
          "τ 动力学方程 0")
    legal = {"PASS", "FAIL", "BOUNDARY", "MISMATCH", "INFO", "CORRECTED"}
    guard("S9_verdicts_legal", all(i["verdict"] in legal for i in ITEMS), "条目 %d" % len(ITEMS))
    ids = [i["id"] for i in ITEMS]
    guard("S10_ids_unique", len(ids) == len(set(ids)), "id %d/去重 %d" % (len(ids), len(set(ids))))
    guard("S11_dir_writable", os.path.isdir(DATA_DIR), DATA_DIR)
    guard("S12_numbers_dict", all(isinstance(i["numbers"], dict) for i in ITEMS), "numbers 全 dict")
    return {
        "alpha_W_from_GF": fmt(a_w_gf, 12),
        "alpha_W_from_theta": fmt(a_w_theta, 12),
        "U_EM_1fm_MeV": fmt(u_em, 10),
        "lambda_W_m": fmt(LAMBDA_W, 12),
        "lambda_pi0_m": fmt(LAMBDA_PI, 12),
        "alpha_G_proton": fmt(G_N * M_PROTON ** 2 / HBAR_C, 12),
    }


def main():
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    extra = selfcheck()

    dist = {}
    for it in ITEMS:
        dist[it["verdict"]] = dist.get(it["verdict"], 0) + 1
    g_ok = sum(1 for g in GUARDS if g["ok"])
    summary = {
        "title": "TUFT 垂直原理 · 统一势结构完整性攻破（r25）",
        "date": "2026-10-10",
        "items": len(ITEMS),
        "verdict_dist": dist,
        "guards_total": len(GUARDS),
        "guards_pass": g_ok,
        "key_numbers": extra,
        "rating": "O / L2",
    }
    payload = {"summary": summary, "items": ITEMS, "guards": GUARDS}
    with open(os.path.join(DATA_DIR, BASENAME + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = ["# TUFT 垂直原理 · 统一势结构完整性攻破 · 数据产物（r25）", "",
             "- 日期：2026-10-10",
             "- 条目：%d（%s）" % (len(ITEMS), " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))),
             "- 自检：%d/%d" % (g_ok, len(GUARDS)), "- 评级：O / L2", "",
             "## 关键读数"]
    for k, v in extra.items():
        lines.append("- %s = %s" % (k, v))
    lines.append("")
    lines.append("## 条目")
    for it in ITEMS:
        lines.append("### %s [%s] %s" % (it["id"], it["verdict"], it["title"]))
        lines.append("")
        lines.append(it["detail"])
        if it["ref"]:
            lines.append("")
            lines.append("> 关联：%s" % it["ref"])
        lines.append("")
    with open(os.path.join(DATA_DIR, BASENAME + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    rep = []
    for k in ["PASS", "FAIL", "BOUNDARY", "MISMATCH", "INFO", "CORRECTED"]:
        rep.append("%s: %d" % (k, dist.get(k, 0)))
    rep.append("GUARD: %d/%d" % (g_ok, len(GUARDS)))
    with open(os.path.join(DATA_DIR, BASENAME + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("TUFT 垂直原理统一势结构完整性攻破 r25\n" + "\n".join(rep) + "\n")

    print("=" * 70)
    print("TUFT 垂直原理统一势结构完整性攻破（r25）")
    print("=" * 70)
    print("条目 %d：" % len(ITEMS), " ".join("%s=%d" % (k, v) for k, v in sorted(dist.items())))
    print("自检 %d/%d" % (g_ok, len(GUARDS)))
    for g in GUARDS:
        if not g["ok"]:
            print("  [GUARD MISS] %s :: %s" % (g["name"], g["note"]))
    print("-" * 70)
    for it in ITEMS:
        print("[%s] %s %s" % (it["verdict"], it["id"], it["title"]))
    print("-" * 70)
    print("退出码 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
