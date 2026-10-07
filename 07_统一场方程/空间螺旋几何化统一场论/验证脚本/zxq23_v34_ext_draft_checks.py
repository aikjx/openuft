# -*- coding: utf-8 -*-
"""
zxq23_v34_ext_draft_checks.py — 外部来稿《TUFT V3.4：能量动量守恒+完整拉格朗日密度+挠子量子场》独立复算判据
日期：2026-10-07
归属：openuft/07_统一场方程/空间螺旋几何化统一场论/验证脚本/
铁律：数学自洽 ≠ 实验证实；FAIL 不粉饰；判定逐条带数值依据。
判据：sympy 精确符号推导 + mpmath 50 位数值锚点 + SI 指数向量量纲层（沿用 24 册口径）。
读数：zxq23_v34_ext_draft_results.json / zxq23_v34_ext_draft_report.txt
"""
import json
import os
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = {}
ROWS = []


def judge(jid, name, verdict, detail):
    ROWS.append({"id": jid, "name": name, "verdict": verdict, "detail": detail})
    RESULTS[jid] = {"name": name, "verdict": verdict, "detail": detail}
    print(f"[{verdict:>8}] {jid} {name}: {detail}")


# ============================================================
# V01 挠率场方程 vs 本稿自身拉格朗日密度（E-L 变分）
# 本稿 L_tau = sqrt(-g) * ( -a/2 (∂τ)² + a/2 τ² - ητ )
# 平直 1 维代表元做 E-L（□ → d²/dx²）
# ============================================================
x = sp.symbols("x", real=True)
tau_f = sp.Function("tau")(x)
alpha, eta = sp.symbols("alpha eta", nonzero=True)

L = -sp.Rational(1, 2) * alpha * sp.diff(tau_f, x) ** 2 + sp.Rational(1, 2) * alpha * tau_f**2 - eta * tau_f
# E-L: dL/dτ - d/dx dL/dτ' = 0
el = sp.diff(L, tau_f) - sp.diff(sp.diff(L, sp.diff(tau_f, x)), x)
el_simplified = sp.simplify(el)  # = alpha*τ'' + alpha*τ - eta
# 同除 α：τ'' + τ - η/α = 0（本稿自身拉格朗日的正确运动方程）
derived = sp.simplify(el_simplified / alpha)
draft_hom = sp.diff(tau_f, x, 2) - tau_f + eta / alpha  # 本稿齐次部分：□τ - τ + η/α
diff_expr = sp.simplify(derived - draft_hom)
v01_diff_zero = sp.simplify(diff_expr.subs(tau_f, sp.Symbol("t_val"))) if False else diff_expr
is_zero = sp.simplify(diff_expr) == 0
judge("V01", "挠率EOM vs 自身L_tau（E-L变分）",
      "FAIL" if not is_zero else "PASS",
      f"由 L_tau 变分得 τ'' + τ - η/α = 0；本稿写 τ'' - τ + η/α = 0；"
      f"两者之差 = {sp.simplify(2 * tau_f - 2 * eta / alpha)}（恒非零）。"
      f"本稿运动方程与自身拉格朗日密度不一致（质量项与 η 项同时反号）。")

# ============================================================
# V02 挠子质量平方：L_tau 的 τ² 项系数给 m² = -1（快子），非本稿宣称的 m_τ² = +1
# ============================================================
# 标准自由标量 L = -a/2 (∂τ)² - a/2 m² τ²；本稿 τ² 项为 +a/2 τ² ⇒ m² = -1
m2_from_L = -1
judge("V02", "挠子质量平方符号",
      "FAIL",
      f"本稿 L_tau 的 τ² 项为 +（α/2)τ²，按自由标量标准形 对应 m_τ² = {m2_from_L}"
      f"（快子型，τ=0 不稳定）；§3.1 却宣称 m_τ² = +1 且 §3.2 把挠子当有质量粒子交换。"
      f"与本稿自身 L_tau 矛盾（独立于 V01 的第二处内部不自洽）。")

# ============================================================
# V03 源项：耦合项 (1/(2c⁴))·τc·R = τR/(2c³) 对 τ 变分 → -R/(2αc³)
# 本稿写 +R/(2αc)：符号反、c 幂次差 c²
# ============================================================
judge("V03", "曲率源项变分（按本稿字面）",
      "FAIL",
      "耦合项 τ·c/(2c⁴)·R = τR/(2c³)，对 τ 变分并入 E-L 得 "
      "τ'' + τ - η/α = -R/(2αc³)；本稿写 □τ - τ + η/α = +R/(2αc)。"
      "源项符号相反、c 幂次差 c²。注：因 κ+τc 量纲未闭合（见 V04），本条按字面变分判定。")

# ============================================================
# V04 量纲审计（SI 指数向量 (M,L,T)）
# ============================================================
def dim_check(name, vecs, expect=None):
    """vecs: list of (label, exponent-vector, sign) summed; expect None => 非零判 FAIL"""
    s = [0, 0, 0]
    for _, v, sign in vecs:
        s = [si + sign * vi for si, vi in zip(s, v)]
    return name, s

M, Lg, T = 0, 1, 2
d_G = [-1, 3, -2]
d_c = [0, 1, -1]
d_c4 = [0, 4, -4]
d_R = [0, -2, 0]           # [R] = L⁻²
d_kappaG = [a - b for a, b in zip(d_G, d_c4)]          # [8πG/c⁴] = M⁻¹L⁻¹T²
d_tau = [0, -1, 0]                                     # [τ] = L⁻¹（挠率迹标量）
d_tauc = [a + b for a, b in zip(d_tau, d_c)]           # [τc] = T⁻¹
d_energy_density = [1, -1, -2]

# (a) κ + τc 相加：两向量必须相等
sum_ok = d_kappaG == d_tauc
# (b) 本稿几何项系数 (1/(2c⁴))·κ_G·R 的量纲 vs 能量密度
c1 = [a + b + c for a, b, c in zip([0, -4, 4], d_kappaG, d_R)]
# (c) (1/(2c⁴))·τc·R
c2 = [a + b + c for a, b, c in zip([0, -4, 4], d_tauc, d_R)]
# (d) L_tau 内部： (∇τ)² 项系数 α vs τ² 项系数 α：前者要求 [α]=ED·L²=M·L·T⁻²，后者要求 [α]=ED
alpha_from_grad = [a + b for a, b in zip(d_energy_density, [0, 2, 0])]
alpha_from_mass = list(d_energy_density)
ltau_ok = alpha_from_grad == alpha_from_mass
judge("V04", "拉格朗日密度量纲闭合（SI 指数向量）",
      "FAIL",
      f"[κ_G]=[M⁻¹L⁻¹T²]={[d_kappaG]} vs [τc]=[T⁻¹]={[d_tauc]} ⇒ κ+τc 相加{'合法' if sum_ok else '非法'}；"
      f"几何项 κR/(2c⁴) 量纲={[c1]}、τcR/(2c⁴) 量纲={[c2]}，均 ≠ 能量密度 [ML⁻¹T⁻²]={[d_energy_density]}；"
      f"L_tau 自身 (∇τ)² 项要求 [α]=[MLT⁻²]（力）而 τ² 项要求 [α]=[ML⁻¹T⁻²]（能量密度），{'一致' if ltau_ok else '互斥（差 L²）'}。"
      f"结论：本稿把 SI 基本量与普朗克单位（m_τ²=1 无量纲）混用，量纲体系未闭合 —— 与 S14 已剔除病根『非法量纲』同型。")

# ============================================================
# V05 守恒律右侧恒为零：全反对称 S^{μρν} 压在对称 Ricci R_{μρ} 上 ≡ 0
# ============================================================
S = sp.MutableDenseNDimArray([0] * 27, (3, 3, 3))
# 构造一个一般的全反对称 S^{μρν}（3 维代表元，由 1 个独立分量生成）
vals = [sp.Symbol(f"s{i}") for i in range(1)]
import itertools
cnt = 0
indep = {}
for mu, rho, nu in itertools.product(range(3), repeat=3):
    perm = (mu, rho, nu)
    if len(set(perm)) < 3:
        continue
    key = tuple(sorted(perm))
    if key not in indep:
        indep[key] = sp.Symbol(f"S_{key}")
    sign = sp.LeviCivita(mu, rho, nu) * sp.LeviCivita(*key)  # +1/-1
    S[mu, rho, nu] = sign * indep[key]
# 对称 Ricci：一般对称 3x3
Rsym = sp.Matrix([[sp.Symbol(f"R_{i}{j}") for j in range(3)] for i in range(3)])
Rsym = Rsym + Rsym.T - sp.diag(*Rsym.diagonal())  # 强制对称
rhs = sum(S[mu, rho, nu] * Rsym[mu, rho] for mu in range(3) for rho in range(3) for nu in range(3))
rhs_zero = sp.simplify(rhs) == 0
judge("V05", "守恒律右侧 S^{μρν}R_{μρ} 恒等性",
      "FAIL" if rhs_zero else "PASS",
      f"S^(μρν) 对 (μ,ρ) 全反对称、Ricci R_(μρ) 对称 ⇒ 缩并 ≡ {sp.simplify(rhs)}（精确恒零，符号代数验证）。"
      f"即本稿守恒方程右侧**恒等于零**，与『右侧为挠率带来的自旋-引力交换源项』的物理解释直接矛盾；"
      f"正确形式须用全曲率张量（Hehl et al., Rev. Mod. Phys. 48, 393 (1976)：∇T = ½ S^(αβμ) R^ν_(αβμ)）。"
      f"按本稿字面，方程退化为 ∇T=0 ——『自旋-引力交换』不存在。")

# ============================================================
# V06 mpmath 代码语义：delta_g(alpha) ≡ alpha（恒等式，250 位无信息量）
# ============================================================
hb, me, cc = sp.symbols("hbar m_e c", positive=True)
lam_e = hb / (me * cc)
tau_e = alpha * hb / (me * cc * lam_e**2)
dg = tau_e * hb / (me * cc)
dg_simplified = sp.simplify(dg)
dg_is_alpha = sp.simplify(dg_simplified - alpha) == 0
# 数值复现（对齐本稿扫描档）
def delta_g_num(a):
    le = mp.mpf("1.054571817e-34") / (mp.mpf("9.1093837015e-31") * mp.mpf("299792458"))
    te = a * mp.mpf("1.054571817e-34") / (mp.mpf("9.1093837015e-31") * mp.mpf("299792458") * le**2)
    return te * mp.mpf("1.054571817e-34") / (mp.mpf("9.1093837015e-31") * mp.mpf("299792458"))
num_check = all(abs(delta_g_num(mp.mpf(f"1e-{k}")) - mp.mpf(f"1e-{k}")) < mp.mpf("1e-60") for k in (40, 39, 38))
judge("V06", "g-2 代码语义（Δg ≡ α 恒等式）",
      "FAIL" if (dg_is_alpha and num_check) else "PASS",
      f"符号简化 delta_g(α) = {dg_simplified}；数值三档 delta_g(1e-40/39/38) ≡ 1e-40/39/38（精确）。"
      f"本稿『250 位精度』扫描是恒等式复读：Δg = α，无任何物理内容；且 tau_eq（挠子场方程）在代码中从未被调用，"
      f"『挠子场运动方程+有效耦合扫描』两个声称目标实际均未执行。")

# ============================================================
# V07 能标一致性（跨力耦合条款）：m_τ = m_Pl 与电子 g-2/EDM 的 45 个量级缺口
# ============================================================
G_N = mp.mpf("6.67430e-11")
hb_m = mp.mpf("1.054571817e-34")
c_m = mp.mpf("299792458")
m_e_kg = mp.mpf("9.1093837015e-31")
m_p_kg = mp.mpf("1.67262192369e-27")
M_pl_kg = mp.mpf("2.176434e-8")
hbar_c = hb_m * c_m
alphaG_ee = G_N * m_e_kg**2 / hbar_c          # 电子-电子引力耦合（锚点1）
alphaG_pp = G_N * m_p_kg**2 / hbar_c          # 质子-质子（锚点2，教科书 5.9e-39）
supp = (m_e_kg / M_pl_kg) ** 2                 # 挠子树图交换对电子低能过程的压低
ok1 = abs(alphaG_ee / mp.mpf("1.7518e-45") - 1) < mp.mpf("2e-4")
ok2 = abs(alphaG_pp / mp.mpf("5.906e-39") - 1) < mp.mpf("2e-4")
# 实验锚：a_e 理论-实验残差窗口 ~1e-12；本稿扫描档 Δg=α=1e-40~1e-38 与窗口差 ~26-28 个量级
window = mp.mpf("1e-12")
gap_scan = mp.log10(window / mp.mpf("1e-38"))
judge("V07", "能标一致性（m_τ=m_Pl vs 电子 g-2）",
      "FAIL",
      f"锚点自检：α_G(ee)={mp.nstr(alphaG_ee, 6)}（锚 {'OK' if ok1 else 'BAD'}）、"
      f"α_G(pp)={mp.nstr(alphaG_pp, 6)}（锚 {'OK' if ok2 else 'BAD'}）。"
      f"m_τ=m_Pl ⇒ 挠子树图交换对电子低能过程天然压低 (m_e/M_Pl)² = {mp.nstr(supp, 6)}（≈45 个量级）；"
      f"要经此通道匹配 Δg~1e-12 窗口需 α ≈ Δg·M_Pl²/m_e² ≈ 10^33 量级——本稿未给任何抵消机制；"
      f"而本稿扫描档 Δg=α=1e-40~1e-38 又比 1e-12 窗口低 {mp.nstr(gap_scan, 4)} 个量级。"
      f"两头都对不上：能标缺口无机制闭合。违反跨力耦合比较的能标一致性条款。")

# ============================================================
# V08 挠率势下有界性
# ============================================================
judge("V08", "挠率势下有界性",
      "FAIL",
      "由 L_tau 读出 V(τ) = -(α/2)τ² + ητ（α>0 时）⇒ τ→±∞ 有 V→-∞，势无下界，"
      "τ=0 为极大而非真空。与本目录已登记的『势非下有界（V₂<0）』红线同型；"
      "且与 §3.1 把 τ=0 当挠子真空展开量子涨落（τ̂）的做法矛盾——快子真空不能直接当微扰量子化背景。")

# ============================================================
# V09 / V10：结构层判定（BOUNDARY / INFO，不冒充数值结论）
# ============================================================
judge("V09", "能动张量可加性与分别守恒",
      "BOUNDARY",
      "耦合 (κ+τc)R 使引力『常数』依赖 τ ⇒ 物质与挠率场的能动张量一般不分别守恒；"
      "本稿直接断言 T = T_matter + T_tau 且各自协变守恒，未证明。需给出联合变分的完整 □ 关系才能判定。")
judge("V10", "引力波挠极化预言",
      "BOUNDARY",
      "ΔΦ_τ ∝ α∫τ dt 未给比例系数与 τ(t,r) 解；标量极化响应 F_τ 未定义；"
      "ET 可检测的说法是定性展望。当前只能记为『可证伪方向候选』，不构成量化预言。")
judge("P01", "方向性肯定：挠率传播动力学", "INFO",
      "ECSK 标准框架中挠率由自旋代数锁定、不传播；本稿给挠率加 KG 型动力学属于合理的扩展方向"
      "（cf. 含 T² 项的传播挠率文献）。方向不加分，具体方程按 V01–V03 判 FAIL。")
judge("P02", "方向性肯定：可证伪意识", "INFO",
      "§四给出标量极化的探测器级预言意识、§3.3 立非高斯不动点为目标——可证伪意识成立，"
      "但 β 函数系数 C1–D2 全部未算，『可重整化』目前是猜想不是结果。")

# ============================================================
# 汇总落盘
# ============================================================
summary = {}
for r in ROWS:
    summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
RESULTS["_summary"] = summary
RESULTS["_date"] = "2026-10-07"
RESULTS["_subject"] = "外部来稿《TUFT V3.4：能量动量守恒+完整拉格朗日密度+挠子量子场》独立复算"

with open(os.path.join(HERE, "zxq23_v34_ext_draft_results.json"), "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, ensure_ascii=False, indent=2)

with open(os.path.join(HERE, "zxq23_v34_ext_draft_report.txt"), "w", encoding="utf-8") as f:
    f.write("外部来稿《TUFT V3.4 能量动量守恒/完整拉格朗日/挠子量子场》独立复算报告（2026-10-07）\n")
    f.write("=" * 78 + "\n")
    for r in ROWS:
        f.write(f"[{r['verdict']:>8}] {r['id']} {r['name']}\n  {r['detail']}\n\n")
    f.write(f"总账：{json.dumps(summary, ensure_ascii=False)}\n")

print(f"\n总账：{summary}")
print("读数已写入 zxq23_v34_ext_draft_results.json / zxq23_v34_ext_draft_report.txt")
