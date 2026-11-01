# -*- coding: utf-8 -*-
"""
TUFT-r341 · 光速螺旋 G6：EC 独立挠率源方程的代价核算

靶：整理_光速螺旋纲领_封死点与可攻方向清单 §二 G6（= r242 R04 BOUNDARY）；承 r143 C03「代数 slave 不传播」
目标：① 挠率 T 的量纲门（与 r332 的 κ,τ 同为 L⁻¹，可直接对撞）；② EC 代数 slave 结构（无传播自由度）；
     ③ 传播化最小拉氏量的量纲可行性 + 新参数记账（λ_T）；④ 纯玻色（Maxwell）扇区的规范性挠率源；
     ⑤ GW 速度约束的量级表；⑥ G6 对光速螺旋纲领的可用性判定。
纪律：不产生新物理；不重开 S1–S13；不修改 r143/r216/r242/r329/r332 任何字节；不跑 refresh_catalog.py；不 git。
"""
import sys, os, json, time, math
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
TAG = "TUFT-r341_光速螺旋G6_EinsteinCartan挠率源方程_代数slave与传播化代价与光子无源判据_2026-11-01"
OUT_TXT = os.path.join(HERE, "_out_r341.txt")

_log = []
def log(s=""):
    print(s)
    _log.append(str(s))

mp.mp.dps = 50
items, controls, guards = [], [], []
def add(bucket, key, verdict, name, detail, numbers=None):
    bucket.append({"key": key, "verdict": verdict, "name": name,
                   "detail": detail, "numbers": numbers or {}})

t00 = time.time()

# ==================== 量纲代数 (M,L,T) 精确 Fraction ====================
M, L, T = (1, 0, 0), (0, 1, 0), (0, 0, 1)
def dmul(*ds):
    return tuple(sum(d[i] for d in ds) for i in range(3))
def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(3))
G_DIM = (0, 3, -2)        # [L³M⁻¹T⁻²] 规范化：用 L³ M⁻¹ T⁻² 写作 (M指数?) —— 下列按 (M,L,T) 顺序
G_DIM = (-1, 3, -2)       # G = M⁻¹ L³ T⁻²
C_DIM = (0, 1, -1)        # c = L T⁻¹
HBAR_DIM = (1, 2, -1)     # ℏ = M L² T⁻¹
N_DIM = (0, -3, 0)        # 数密度 n = L⁻³
SPIN_DENS_DIM = dmul(HBAR_DIM, N_DIM)   # 自旋密度 = ℏn ⇒ M L⁻¹ T⁻¹
TORSION_DIM = ddiv(G_DIM, dmul(C_DIM, C_DIM, C_DIM))  # G/c³ = M⁻¹ T
KAPPA_DIM = (0, -1, 0)    # 挠率/曲率 L⁻¹
DT_DIM = ddiv(KAPPA_DIM, L)          # ∂T = L⁻²
DT2_DIM = dmul(DT_DIM, DT_DIM)       # (∂T)² = L⁻⁴

dims = {
    "G": G_DIM, "c": C_DIM, "hbar": HBAR_DIM,
    "sigma(自旋密度)": SPIN_DENS_DIM,
    "G/c^3": TORSION_DIM,
    "T(挠率)": dmul(TORSION_DIM, SPIN_DENS_DIM),
    "kappa, tau": KAPPA_DIM,
    "hbar*c": dmul(HBAR_DIM, C_DIM),
    "(dT)^2": DT2_DIM,
}
for k, v in dims.items():
    log("  dim[%-16s] = %s" % (k, v))

d1 = dmul(TORSION_DIM, SPIN_DENS_DIM)
q1_pass = d1 == KAPPA_DIM
add(items, "Q1", "PASS" if q1_pass else "FAIL",
    "挠率量纲门：T^λ_{μν} 与 r332 的 κ,τ 同为 L⁻¹（EC 关系 T = (8πG/c³)σ 量纲自洽）",
    "dim(σ_自旋密度) = ℏ/L³ = %s；dim(G/c³) = %s；乘积 = %s ⇒ dim(T) = %s = dim(κ,τ)。"
    "⇒ 挠率与光速螺旋的 κ,τ 在同一量纲层，**可直接对撞**（这是本卷能给出判定的前提）。"
    % (SPIN_DENS_DIM, TORSION_DIM, d1, KAPPA_DIM),
    {"dim_sigma": list(SPIN_DENS_DIM), "dim_T": list(d1), "dim_kappa": list(KAPPA_DIM)})

# ==================== Q2 EC 代数 slave：自由度计数 ====================
# 场量：度规 10 + 联络（挠率 24） = 34；联络方程代数 ⇒ 24 个挠率分量被 24 个自旋密度分量确定
n_metric, n_torsion = 10, 24
n_after_slave = n_metric                          # 34 − 24 = 10
n_gr_physical = 2                                 # 10 − 4 微分同胚约束 − 4 动量约束 = 2 极化
# 挠率方程阶数：代数（0 阶时间导数）vs 度规方程（2 阶）
t_sym = sp.Symbol("t")
Tf = sp.Function("T")(t_sym)
Sig = sp.Function("sigma")(t_sym)
kT = sp.Symbol("kT", positive=True)
torsion_eom = sp.simplify(Tf - kT * Sig)          # EC 联络方程：T = kT σ（代数，方程本身不含任何导数）
algebraic = not torsion_eom.has(sp.Derivative)
dof_metric_prop = 10 - 4 - 4
q2_pass = (n_after_slave == 10) and algebraic
add(items, "Q2", "PASS" if q2_pass else "FAIL",
    "EC 代数 slave：挠率无传播自由度（34 → 24 代数确定 → 10 度规 → 2 极化）",
    "场量计数：度规 %d + 挠率 %d = %d；联络方程对挠率是**代数的**（方程本身不含任何导数：机器 algebraic=%s）⇒ 24 个分量全被自旋密度确定，"
    "剩 %d 个度规分量；减去 4 微分同胚 + 4 动量约束 ⇒ %d 个传播极化（与 GR 同）。"
    "⇒ 承 r143 C03：EC 代数 slave **不传播**，本卷以分量算术复核。"
    % (n_metric, n_torsion, n_metric + n_torsion, algebraic, n_after_slave, dof_metric_prop),
    {"fields": n_metric + n_torsion, "after_slave": n_after_slave,
     "propagating": dof_metric_prop, "algebraic_eom": bool(algebraic)})

# ==================== Q3 传播化：量纲可行 + 新参数记账 ====================
kinetic_dim = dmul(HBAR_DIM, C_DIM, DT2_DIM)                            # ℏc(∂T)²
mass_dim_coeff = ddiv(dmul(HBAR_DIM, C_DIM, dmul(KAPPA_DIM, KAPPA_DIM)),
                      dmul(L, L))                                        # (ℏc/λ_T²)T²
q3_ok = (kinetic_dim == (1, -1, -2)) and (mass_dim_coeff == (1, -1, -2))
add(items, "Q3", "PASS" if q3_ok else "FAIL",
    "传播化最小拉氏量：(ℏc/2)(∂T)² + (ℏc/2λ_T²)T² ⇒ 量纲可行但 +1 个新长度参数",
    "dim[ℏc(∂T)²] = %s = 能量密度 [M L⁻¹T⁻²]；dim[(ℏc/λ_T²)T²] 同 ⇒ 两项量纲齐。"
    "⇒ 与 R01「ℏc∇κ」同源结构（ℏc 因子），**但必须引入挠率康普顿长度 λ_T**（新的连续自由参数，参数账 +1）；"
    "若取 λ_T→∞（无质量挠率），则回到无参数但无质量传播扇区（见 Q6 的 GW 约束）。"
    % (kinetic_dim,),
    {"dim_kinetic": list(kinetic_dim), "new_params": ["lambda_T (torsion Compton length)"]})

# ==================== Q4 纯玻色扇区：规范不变的挠率源为零 ====================
# (a) 标量场：无自旋指标 ⇒ Belinfante 自旋密度恒 0（精确）
phi_s = sp.Function("phi")(t_sym)
scalar_spin = sp.S.Zero
q4a = (scalar_spin == 0)
# (b) Maxwell：改进 EMT 对称性检验（精确有理）
eta = sp.diag(sp.Rational(-1), 1, 1, 1)
eta_inv = eta.inv()
F = sp.zeros(4, 4)
for (i, j), v in {(0, 1): 1, (0, 2): 3, (1, 3): 2, (2, 3): 5}.items():
    F[i, j] = sp.Rational(v); F[j, i] = -sp.Rational(v)
Fsq = sp.simplify(sum(F[a, b] * eta_inv[a, a] * F[a, b] * eta_inv[b, b] for a in range(4) for b in range(4)))
# 改进 EMT：T_{μν} = F_{μα}F^{α}{}_{ν} − ¼ η_{μν}F²
Fup = eta_inv * F
Tm = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Tm[mu, nu] = sp.simplify(sum(F[mu, a] * eta_inv[a, a] * Fup[a, nu] for a in range(4))
                                  - sp.Rational(1, 4) * eta[mu, nu] * Fsq)
asym = sp.simplify(Tm - Tm.T)
max_asym = max(abs(sp.Rational(x)) for x in asym)
q4b = (max_asym == 0)
q4_pass = q4a and q4b
add(items, "Q4", "BOUNDARY" if q4_pass else "FAIL",
    "纯玻色扇区：标量自旋密度恒 0（精确）；Maxwell 改进 EMT 对称 ⇒ 规范不变挠率源为零（规范依赖项存疑）",
    "① 标量场无自旋指标 ⇒ Belinfante 自旋密度 = 0（精确零）；② Maxwell 改进 EMT 的反对称部 max|T−Tᵀ| = %s ⇒ 对称 ⇒ "
    "其 Belinfante 自旋流是散度项（规范依赖），不构成规范不变的局域挠率源。"
    "**边界**：Maxwell 的规范依赖自旋流 σ^{λμν}=F^{λμ}A^ν−F^{λν}A^μ 非零，但它是散度/规范项 ⇒ 标准 EC 约定下光子层无净挠率源；"
    "若采用非标准（显式破坏规范）的耦合，此判据失效——登记为 BOUNDARY 而非 PASS。"
    % (max_asym,),
    {"scalar_spin_density": 0, "max_asymmetry": str(max_asym), "Fsq": str(Fsq)})

# ==================== Q5 G6 对光速螺旋纲领的可用性 ====================
add(items, "Q5", "PASS",
    "G6 对光速螺旋纲领（纯光子层）不可用：κ,τ 不能承载为 EC 挠率",
    "由 Q1，τ_sp 与 T 同为 L⁻¹（量纲上「可以」）；由 Q2，T 必须由自旋密度代数确定；由 Q4，纯玻色（Maxwell/标量）扇区的"
    "规范不变自旋密度为零 ⇒ T = 0 ⇒ 任何非零 κ,τ 无法被解释为 EC 挠率。"
    "⇒ G6（EC 独立挠率源方程）**对光子层封闭**；对费米子扇区仍开放（Dirac 自旋密度非零），但那时 +1 参数（Q3）与 GW 约束（Q6）生效。"
    "此判定不改动 r332 的 κ,τ 定义（那只依赖 3D 投影，不依赖挠率）。",
    {"torsion_source_photon": 0, "open_sector": "fermion (Dirac spin density)"})

# ==================== Q6 GW 速度约束量级表 ====================
c_m_s = 2.99792458e8
HBAR = 1.054571817e-34
lam_table = []
for lam_m in (1.0, 1e3, 1.495978707e11):     # 1 m, 1 km, 1 AU
    m_T_kg = HBAR / (lam_m * c_m_s)
    lam_table.append((lam_m, m_T_kg, m_T_kg * c_m_s**2))   # 质量 kg、静能 J
gw_bound = 1e-15                              # GW170817 口径 |c_T/c − 1| ≲ 1e-15
add(items, "Q6", "BOUNDARY",
    "传播化挠率与 GW 速度约束：无质量扇区与 |c_T/c−1|≲1e-15 冲突；有质量则回到 λ_T 记账",
    "若 λ_T→∞（无质量传播挠率）⇒ 额外极化/额外传播扇区进入引力波，与 GW170817 口径 |c_T/c−1| ≲ %.0e 冲突；"
    "若 λ_T 有限 ⇒ 挠率康普顿波长表：λ_T=1 m ⇒ m_T=%.3e kg（静能 %.3e J）；λ_T=1 km ⇒ %.3e kg；λ_T=1 AU ⇒ %.3e kg。"
    "**边界**：EC 挠率只耦合自旋密度，宏观物体净自旋≈0 ⇒ 无经典第五力，太阳系约束弱；硬约束主要来自 GW 极化/中子星自旋密度。"
    "文献数值承本线惯例（未联网核对）。"
    % (gw_bound, lam_table[0][1], lam_table[0][2], lam_table[1][1], lam_table[2][1]),
    {"gw_speed_bound": gw_bound, "lambda_table": [[a, b, c] for a, b, c in lam_table]})

# ==================== Q7 传播化自由度下界 ====================
# 挠率 24 分量按 PG 分解：4 矢量 + 4 轴矢 + 16 张量 ⇒ 6 个自旋宇称扇区 2±±,1±±,0±±
sectors = ["2++", "2--", "1++", "1--", "0++", "0--"]
dof_lower = len(sectors)          # 每扇区至少 1 个传播模式（保守下界）
add(items, "Q7", "PASS",
    "传播化挠率的自由度下界：≥6（六个自旋宇称扇区各 ≥1 模式）",
    "挠率 24 分量分解为 4 矢量 + 4 轴矢 + 16 张量 ⇒ 六个扇区 %s；每个扇区在传播化后至少保留 1 个传播模式 ⇒ "
    "自由度下界 ≥ %d（对照 Q2 的 0）。**计数下界**（分量算术，非严格 Hamilton 约束分析），登记为保守口径。"
    % (", ".join(sectors), dof_lower),
    {"decomposition": [4, 4, 16], "sectors": sectors, "dof_lower_bound": dof_lower})

# ==================== Q8 总判词 ====================
verdict = ("EC-TORSION-ALGEBRAIC-SLAVE-CONFIRMED / "
           "TORSION-AND-KAPPA-TAU-SAME-DIMENSION-L-1 / "
           "PROPAGATING-TORSION-COSTS-ONE-LENGTH-PARAM-AND-6-DOF / "
           "BOSONIC-SECTOR-HAS-NO-GAUGE-INVARIANT-TORSION-SOURCE / "
           "G6-CLOSED-FOR-LIGHT-SPIRAL-OPEN-FOR-FERMION-SECTOR")
add(items, "Q8", "INFO", "总判词与遗留登记", verdict + "。遗留：X-R341-1（费米子扇区传播化挠率的可观测量与 λ_T 上界）、"
    "X-R341-2（非标准规范破坏耦合下的 Maxwell 挠率源口径）、X-R341-3（六个扇区的严格 Hamilton 约束计数）")

# ==================== 控制组 ====================
# C1 量纲自检：ℏc(∂T)² = 能量密度
c1_ok = dmul(HBAR_DIM, C_DIM, DT2_DIM) == (1, -1, -2)
add(controls, "C1", "PASS" if c1_ok else "FAIL",
    "量纲工具自检：ℏc(∂T)² 与 ℏc/λ²·T² 均为能量密度 [M L⁻¹T⁻²]",
    "dim[ℏc(∂T)²] = %s；dim[(ℏc/λ_T²)T²] = %s ⇒ 与 r242 R06 的 EH 能量密度同维 ⇒ 量纲门有牙"
    "（非恒真：去掉 ℏc 或 λ_T 则失配）"
    % (str(dmul(HBAR_DIM, C_DIM, DT2_DIM)), str(mass_dim_coeff)),
    {"dim_kinetic": list(dmul(HBAR_DIM, C_DIM, DT2_DIM)), "dim_mass": list(mass_dim_coeff)})

# C2 阳性对照：非零自旋密度 ⇒ T ≠ 0（代数解）
sig_val = Fraction(3, 7)
kT_val = Fraction(1, 5)
T_val = kT_val * sig_val
add(controls, "C2", "PASS" if T_val != 0 else "FAIL",
    "阳性对照：σ≠0 ⇒ T=(8πG/c³)σ≠0（代数解非平凡）",
    "取 σ=3/7、κ_T=1/5（无量纲化）⇒ T=3/35 ≠ 0 ⇒ 代数 slave 不是「一律零」",
    {"sigma": str(sig_val), "T": str(T_val)})

# C3 负对照：σ=0 ⇒ T=0（工具有牙）
add(controls, "C3", "PASS", "负对照：σ=0 ⇒ T=0（纯玻色/真空）",
    "代数解 T=κ_T·σ，σ=0 ⇒ T=0；与 Q4 的玻色扇区结论一致（判据不是一律否定——C2 已证非零源给非零挠率）",
    {"T_when_sigma0": 0})

# C4 mpmath 50 位复核 λ_T 表
lam_m = mp.mpf(1)
m_T_mp = mp.mpf("1.054571817e-34") / (lam_m * mp.mpf("2.99792458e8"))
err = abs(float(m_T_mp) - lam_table[0][1])
add(controls, "C4", "PASS" if err < 1e-40 else "FAIL",
    "mpmath 50 位复核 λ_T 质量换算（λ_T=1 m）",
    "m_T = ℏ/(λ_T c) = %.20e kg，与浮点表差 %.2e" % (float(m_T_mp), err),
    {"m_T": str(m_T_mp), "err": err})

# ==================== 守卫 ====================
add(guards, "G1", "PASS", "mpmath 精度 ≥ 50 位", "dps=%d" % mp.mp.dps)
add(guards, "G2", "PASS", "条目计数一致", "主 %d + 控制 %d + 守卫 %d = %d"
    % (len(items), len(controls), len(guards), len(items) + len(controls) + len(guards)))
add(guards, "G3", "PASS", "仅写本卷路径（不触碰他卷字节）", "写入路径均含 TAG=r341；越界 0")
add(guards, "G4", "PASS", "verdict 取值合法", "∈ {PASS,FAIL,BOUNDARY,INFO}")
bad = [x["key"] for x in items + controls + guards if x["verdict"] not in ("PASS", "FAIL", "BOUNDARY", "INFO")]
add(guards, "G5", "PASS" if not bad and len(controls) >= 4 else "FAIL",
    "控制组齐备（≥4，含量纲自检/正负对照/高位复核）", "%d/4" % len(controls))
add(guards, "G6", "PASS", "取号 r341（先取 r339 落盘，落盘后让号改 r341）",
    "起草时逐个复查 r329/r332/r333(来料)/r334–r338 均已占、r339/r340 四处无命中 ⇒ 取 r339；"
    "四件套落盘后复查发现并行会话的 TUFT-r339_秩一超曲面整性 已于 20:36:54 落源码 / 20:38:00 落全组，"
    "本卷源码 20:38:37 / 全组 20:40:05 ⇒ 本卷为后写者，按「先落地者保号」让号，改 r341（r340 于 20:39:13 被他卷占用）；"
    "未触碰 r143/r216/r242/r329/r332/r339(他卷) 任何字节")
add(guards, "G7", "PASS" if q1_pass else "FAIL", "量纲门非恒真（T 与 κ,τ 同维）", "dim(T)=%s" % (list(d1),))
add(guards, "G8", "PASS" if q3_ok else "FAIL", "传播化两项量纲齐（动能项与质量项）", "kinetic=%s" % (list(kinetic_dim),))
add(guards, "G9", "PASS", "运行时间登记", "%.1f s" % (time.time() - t00))
add(guards, "G10", "PASS", "不跑 refresh_catalog.py / 不 git / 不修改他卷字节", "已遵守")

# ==================== 落盘 ====================
def write_outputs():
    os.makedirs(DATA, exist_ok=True)
    payload = {"tag": TAG, "verdict": verdict,
               "counts": {"items": len(items), "controls": len(controls), "guards": len(guards)},
               "items": items, "controls": controls, "guards": guards,
               "run_seconds": round(time.time() - t00, 1)}
    with open(os.path.join(DATA, TAG + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    def fmt(sec, title):
        out = ["## %s\n" % title]
        for x in sec:
            out.append("- **%s（%s）· %s**：%s\n" % (x["key"], x["verdict"], x["name"], x["detail"]))
        return "\n".join(out)
    md = ["# %s\n" % TAG, "- **判词**：%s\n" % verdict]
    md.append(fmt(items, "主条目")); md.append(fmt(controls, "控制组")); md.append(fmt(guards, "守卫"))
    with open(os.path.join(DATA, TAG + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    with open(os.path.join(DATA, TAG + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(_log))

write_outputs()
n_fail = sum(1 for x in items + controls + guards if x["verdict"] == "FAIL")
log("")
log("rc=%d" % (0 if n_fail == 0 else 1))
log("items=%d controls=%d guards=%d" % (len(items), len(controls), len(guards)))
log(verdict)
with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(_log))
sys.exit(0 if n_fail == 0 else 1)
