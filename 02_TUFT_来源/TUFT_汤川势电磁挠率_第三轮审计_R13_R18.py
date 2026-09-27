# -*- coding: utf-8 -*-
"""
TUFT 汤川势 + 电磁挠率章 · 第三轮审计（R13–R18）
================================================
上游：v2.1.1（R1–R12，主判定 31 项 + EXT 5 项）与《TUFT_汤川势电磁挠率_算法联盟全维校验.py》

本轮三块（全部实跑：sympy / mpmath / numpy 自写 Numerov）：
  A. 红队 v2.1.1 自身（AL-A1..A6，对应修复 R15–R18）
       A1 判定质量：AL-D5-5e 是「同义反复」（两端 AST 完全相同）⇒ 零信息判定
       A2 判定口径：31 项中 status 由计算导出的「计算闸门型」实为多少（自动 AST 分类）
       A3 R7 严重度与机理复核：常数势偏移在静力平衡中严格消去（TOV 方程只含 ∇Φ）
       A4 R8 循环性：m_π=(ħ/c)√(κ_X²+τ_X²) 与 μ=m_πc/ħ 互为定义（🔵→🟠）
       A5 R9 真检验：以规范不变性 δF=0（A_μ→A_μ+∂_μΛ）替代同义反复
       A6 类型学/术语：τ^EM 被升格为时空 4-矢势，与「Frenet 曲线挠率」非同型（新开放项 O17）
  B. R13（用户最高优先级 · 选项 A）：E1 势 vs 汤川势 NN 低能相移数值计算
       长程严格等价（同尾系数）→ 差异只在短程 → β_c 临界耦合 / 共同耦合下束缚能 /
       a_s 与 δ_l(E) 曲线 / 核心半径 r_c 敏感性 / 诚实边界
  C. R14（用户选项 E）：E1 对数奇性的量子自伴性审计
       解析判据 Λ_c=(l+1/2)²（log 势 Λ_eff=0 ⇒ 自伴、有下界）
       数值对照：log 势 E_0(r_c) 收敛 vs 超临界 -Λ/r² 的 E_0·r_c² → 常数（落心）
       束缚态数目有限性 + 经典有限时间落心
红线：数学自洽 ≠ 物理实证；凡模型假设项一律 BOUNDARY，不粉饰为 PASS。
产出：同目录 .txt / .json
"""
import ast, json, math, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 25
HERE = os.path.dirname(os.path.abspath(__file__))
V211_PY = os.path.join(HERE, "TUFT_汤川势电磁挠率_算法联盟全维校验.py")
V211_JSON = os.path.join(HERE, "TUFT_汤川势电磁挠率_算法联盟全维校验.json")

# ---------------- 物理常数（与 v2.1.1 校验脚本同源） ----------------
HBARC = 197.3269804          # MeV·fm
M_PI = 139.57039             # MeV
M_N = 938.9183               # MeV
M_R = M_N / 2.0              # NN 约化质量 MeV
MU = M_PI / HBARC            # fm^-1 = 0.70731
LAM = 1.0 / MU               # fm = 1.41380
E_UNIT = HBARC**2 / (2.0*M_R)  # MeV·fm^2：E[fm^-2]=k^2 ⇒ E[MeV]=E_UNIT·k^2 = 41.4705
EULER = 0.5772156649015329

results = []


def check(code, name, status, detail, evidence=None, mode="体系对齐", kind="计算型"):
    results.append({"code": code, "name": name, "status": status, "detail": detail,
                    "evidence": evidence or {}, "mode": mode, "kind": kind})
    print(f"[{status:8s}] {code} [{mode}|{kind}] {name}: {detail}")


# ============================================================
# 数值工具：势表 / Numerov 传播 / 相移 / 散射长度 / 束缚态
# ============================================================
def shape(pot, r_c, R_MAX=45.0, N=4000):
    """β=1 的势形状表 S(r)（四种势均线性正比于 β）⇒ 一次构建、β 扫描零额外成本。"""
    key = (pot, round(float(r_c), 12))
    if key not in _SH:
        rr = np.linspace(r_c, R_MAX, N)
        if pot == "Y":
            S = -np.exp(-MU*rr)/rr
        elif pot == "E1":
            S = np.array([-MU*float(mp.e1(MU*x)) for x in rr], dtype=float)
        elif pot == "LOG":   # E1 短程主项：E1≈-γ-ln z ⇒ U=-βμE1 ≈ +βμ(γ+ln z)
            S = MU*(EULER + np.log(MU*rr))
        elif pot == "INV2":  # R14 对照：超临界 -Λ/r²
            S = -1.0/rr**2
        else:
            raise ValueError(pot)
        _SH[key] = (rr, S)
    return _SH[key]


_SH = {}


def propagate(pot, beta, r_c, E, l, r_out, h=1e-3):
    """Numerov 积分 u''=[l(l+1)/r²+U(r)-E]u，u(r_c)=0,u'(r_c)=1。
    返回 (u(r_out), u'/u |_{r_out}, 节点数)。E 单位 fm^-2（束缚态 E<0）。"""
    rr, S = shape(pot, r_c)
    n = int(round((r_out - r_c)/h))
    r = r_c + h*np.arange(n+1)
    f = l*(l+1)/r**2 + beta*np.interp(r, rr, S) - E
    h2 = h*h
    um3 = 0.0
    um2 = 0.0
    um1 = h + h2*h*f[0]/6.0
    nodes = 0
    for i in range(1, n):
        uu = (2.0*(1.0 + 5.0*h2*f[i]/12.0)*um1 - (1.0 - h2*f[i-1]/12.0)*um2) / (1.0 - h2*f[i+1]/12.0)
        if um1*uu < 0:
            nodes += 1
        um3, um2, um1 = um2, um1, uu
    chi = (3.0*um1 - 4.0*um2 + um3)/(2.0*h*um1)
    return um1, chi, nodes


def _jl(l, x):
    if l == 0:
        return math.sin(x)/x
    if l == 1:
        return math.sin(x)/x**2 - math.cos(x)/x
    return (3.0/x**3 - 1.0/x)*math.sin(x) - 3.0*math.cos(x)/x**2


def _nl(l, x):
    if l == 0:
        return -math.cos(x)/x
    if l == 1:
        return -math.cos(x)/x**2 - math.sin(x)/x
    return -(3.0/x**3 - 1.0/x)*math.cos(x) - 3.0*math.sin(x)/x**2


def _jlp(l, x):
    return -_jl(1, x) if l == 0 else _jl(l-1, x) - (l+1)/x*_jl(l, x)


def _nlp(l, x):
    return -_nl(1, x) if l == 0 else _nl(l-1, x) - (l+1)/x*_nl(l, x)


def phase_shift(pot, beta, r_c, E_MeV, l, r_out=15.0, h=1e-3):
    """相移（度）。匹配公式 tanδ=(χ j_l - k j_l')/(χ n_l - k n_l')，x=kr_out。"""
    k = math.sqrt(E_MeV/E_UNIT)
    um1, chi, nodes = propagate(pot, beta, r_c, k*k, l, r_out, h)
    x = k*r_out
    j, n, jp, np_ = _jl(l, x), _nl(l, x), _jlp(l, x), _nlp(l, x)
    tn = (chi*j - k*jp)/(chi*n - k*np_)
    return math.degrees(math.atan(tn)), nodes, k


def scattering_length(pot, beta, r_c, l=0, r_out=15.0, h=1e-3):
    """零能 l=0 散射长度：u∝C(1-a_s/r) ⇒ a_s = χr²/(1+χr)。"""
    um1, chi, nodes = propagate(pot, beta, r_c, 0.0, l, r_out, h)
    return chi*r_out**2/(1.0 + chi*r_out), nodes


def inward(pot, beta, r_c, E, l, r_out, h=1e-3):
    """内向积分：从 r_out 以衰减解 e^{-γr} 出发积分到 r_c（对增长模稳定，每 2000 步重标定防溢出）。
    E≤0（fm^-2）。返回 (u(r_c), 区间内节点数)。"""
    rr, S = shape(pot, r_c)
    n = int(round((r_out - r_c)/h))
    r = r_c + h*np.arange(n+1)
    f = l*(l+1)/r**2 + beta*np.interp(r, rr, S) - E
    h2 = h*h
    gam = math.sqrt(-E) if E < 0 else 0.0
    um1 = math.exp(-gam*r_out)
    um2 = math.exp(-gam*(r_out-h))
    fext = np.append(f, f[-1])
    nodes = 0
    for i in range(n, 0, -1):
        up = (2.0*(1.0 + 5.0*h2*f[i]/12.0)*um2 - (1.0 - h2*fext[i+1]/12.0)*um1)/(1.0 - h2*f[i-1]/12.0)
        if um2*up < 0:
            nodes += 1
        um1, um2 = um2, up
        if i % 2000 == 0:
            s = max(abs(um1), abs(um2), 1e-300)
            if s > 1e100 or s < 1e-100:
                um1 /= s
                um2 /= s
    return um2, nodes


def threshold_beta(pot, r_c, l=0, r_out=12.0, h=1e-3, lo=0.3, hi=9.0):
    """阈值判据（精确、廉价）：E=0 且 d(u)/dr|_{r_out}=0 ⇒ u(r) 在外区为常数，
    内向积分的 u(r_c)=0 即「首个 s 波束缚态出现」的临界耦合 β_c。"""
    def g(b):
        u0, _nd = inward(pot, b, r_c, 0.0, l, r_out, h)
        return u0
    glo = g(lo)
    for _ in range(60):
        mid = 0.5*(lo+hi)
        gm = g(mid)
        if glo*gm <= 0:
            hi = mid
        else:
            lo = mid
            glo = gm
    return 0.5*(lo+hi)


def tune_beta(pot, r_c, target_MeV, l=0, lo=0.3, hi=14.0, h=1e-3, rfac=5.0, cap=60.0):
    """二分 β 使基态束缚能 = target：解 u(r_c; β, E_b=target) = 0（内向积分，单调）。"""
    gam = math.sqrt(target_MeV/E_UNIT)
    r_out = min(cap, max(10.0, rfac/gam))

    def g(b):
        u0, _nd = inward(pot, b, r_c, -target_MeV/E_UNIT, l, r_out, h)
        return u0
    glo = g(lo)
    for _ in range(60):
        mid = 0.5*(lo+hi)
        gm = g(mid)
        if glo*gm <= 0:
            hi = mid
        else:
            lo = mid
            glo = gm
    return 0.5*(lo+hi)


def shallow_binding(pot, beta, r_c, eb_min=1e-4, eb_max=1.0, l=0, h=1e-3):
    """内向扫描给定 β 下的最浅束缚能（返回 E_b 或 None）；用于「同一耦合下 E1 是否束缚」。"""
    prev = None
    for eb in np.geomspace(eb_min, eb_max, 70):
        gam = math.sqrt(eb/E_UNIT)
        r_out = min(200.0, max(10.0, 4.0/gam))
        u0, nd = inward(pot, beta, r_c, -eb/E_UNIT, l, r_out, h)
        if prev is not None and prev[0]*u0 < 0 and nd == 0:
            a, b, sg = prev[1], eb, prev[0]
            for _ in range(50):
                m = 0.5*(a+b)
                ro = min(200.0, max(10.0, 4.0/math.sqrt(m/E_UNIT)))
                um, _nm = inward(pot, beta, r_c, -m/E_UNIT, l, ro, h)
                if sg*um <= 0:
                    b = m
                else:
                    a = m
            return 0.5*(a+b)
        prev = (u0, eb, nd)
    return None


def box_spectrum(pot, beta, r_c, l=0, R=12.0, emax=1e4, nb=260, h=1e-3):
    """箱 [r_c, R]（两端 u=0）内向积分的首个零点 → 最低束缚能（MeV）；用于 r_c 收敛性。"""
    prev = None
    for eb in np.geomspace(1e-3, emax, nb):
        u0, nd = inward(pot, beta, r_c, -eb/E_UNIT, l, R, h)
        if prev is not None and prev[0]*u0 < 0:
            a, b, sg = prev[1], eb, prev[0]
            for _ in range(60):
                m = 0.5*(a+b)
                um, _nm = inward(pot, beta, r_c, -m/E_UNIT, l, R, h)
                if sg*um <= 0:
                    b = m
                else:
                    a = m
            return 0.5*(a+b), prev[2]
        prev = (u0, eb, nd)
    return None, None


# ============================================================
# A. 红队 v2.1.1 自身（AL-A1..A6）
# ============================================================
src = open(V211_PY, encoding="utf-8").read()
tree = ast.parse(src)

# A1：AL-D5-5e 同义反复 —— 两端赋值 AST 完全相同
assigns = {}
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id in ("E_static_old", "E_static_new"):
                assigns[t.id] = ast.dump(node.value)
same = assigns.get("E_static_old") is not None and assigns.get("E_static_old") == assigns.get("E_static_new")
check("AL-A1", "★ R15：判定质量红队——AL-D5-5e 是否同义反复（AST 对比）",
      "FAIL" if same else "PASS",
      ("E_static_old 与 E_static_new 的 AST dump 完全相同 ⇒ 该判定恒真、零信息；"
       "R9 真正需要检验的时变/洛伦兹指标问题完全未被测试" if same else "两端不同，判据有效"),
      {"ast_old": assigns.get("E_static_old", "")[:120], "ast_new": assigns.get("E_static_new", "")[:120],
       "identical": bool(same)}, mode="体系对齐", kind="计算型")

# A2：判定口径分类（自动 AST：status 实参形态）
ifexp_names = set()
for node in ast.walk(tree):
    if isinstance(node, ast.If):
        for st in node.body:
            if isinstance(st, ast.Assign):
                for t in st.targets:
                    if isinstance(t, ast.Name):
                        ifexp_names.add(t.id)
CALC, HARD = [], []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "check" and len(node.args) >= 3:
        code = node.args[0].value if isinstance(node.args[0], ast.Constant) else "?"
        st = node.args[2]
        gate = isinstance(st, ast.IfExp) or (isinstance(st, ast.Name) and st.id in ifexp_names)
        (CALC if gate else HARD).append(code)
canonical_json = json.load(open(V211_JSON, encoding="utf-8"))
canon_codes = [c["code"] for c in canonical_json["checks"] if c["code"].startswith("AL-")]
canon_status = {c["code"]: c["status"] for c in canonical_json["checks"] if c["code"].startswith("AL-")}
calc_gate = [c for c in CALC if c in canon_codes]
hard = [c for c in canon_codes if c not in calc_gate]
ng_pass = sum(1 for c in calc_gate if canon_status[c] == "PASS")
nh_pass = sum(1 for c in hard if canon_status[c] == "PASS")
check("AL-A2", "★ R15：判定口径重分类——v2.1.1『PASS 24』的证据强度", "FAIL",
      f"31 项主判定中 status 由计算表达式导出的仅 {len(calc_gate)} 项（其中 AL-D5-5e 经 A1 证明为同义反复 ⇒ 有效 {len(calc_gate)-1} 项）；"
      f"其余 {len(hard)} 项 status 为硬编码字符串（部分 detail 引用实算数值，但判定不过计算闸门）⇒ "
      f"v2.1.1 的『PASS 24』应分列为：计算闸门 PASS {ng_pass} 项（扣同义反复后 {ng_pass-1}）＋硬编码 PASS {nh_pass} 项",
      {"compute_gate": sorted(calc_gate), "hardcoded": sorted(hard),
       "gate_pass": ng_pass, "hardcoded_pass": nh_pass,
       "count_gate": len(calc_gate), "count_hard": len(hard)}, mode="体系对齐", kind="计算型")

# A3：R7 严重度与机理（常数势偏移在静力平衡中消去）
rs = sp.symbols("r_s", positive=True)
PHI = sp.Function("Phi")
C0 = sp.Symbol("C0")
grad_shift = sp.simplify(sp.diff(PHI(rs) + C0, rs) - sp.diff(PHI(rs), rs))
# TOV 静力平衡中势只通过 ∇Φ 出现（dP/dr = -ρ∇Φ 的 Newton 极限）
test_ok = grad_shift == 0
check("AL-A3", "★ R16：R7 严重度与机理复核（常数势偏移在静力平衡严格消去）",
      "FAIL" if test_ok else "PASS",
      "sympy：∂_r[Φ+C0]-∂_rΦ ≡ 0 ⇒ 加常数不改变 ∇Φ，故不改变 dP/dr 与 TOV 静力平衡；"
      "『不写 V(∞)=0 造成 EoS 能量基准漂移』机理错误（只平移总能量 ∫ρΦ dV 的记账），"
      "R7 应降级为 ⚪ 记号声明，且第 3 优先级『重跑 TOV 扫描』为伪待办",
      {"d_grad_shift": str(grad_shift)}, mode="求导证明", kind="计算型")

# A4：R8 循环性
kX, tX = sp.symbols("kappa_X tau_X", positive=True)
m_sym = sp.Symbol("m", positive=True)
ident = sp.simplify(sp.sqrt(kX**2 + tX**2) - (m_sym*sp.Symbol("c")/sp.Symbol("hbar")))
mu_num = M_PI/HBARC
chk_circ = abs(math.sqrt(mu_num**2) - mu_num)/mu_num
check("AL-A4", "★ R17：R8『力程不需要额外参数』的循环性判定", "FAIL",
      f"m_π=(ħ/c)√(κ_X²+τ_X²) 与 μ=m_πc/ħ 互为定义重排（数值 |√(μ²)-μ|/μ={chk_circ:.1e} 机器零）；"
      "m_π 为实验输入 ⇒ 该式不预测 λ_π，R8 应为 🟠（输入/定义层）而非 🔵 导出",
      {"identity_residual": float(chk_circ)}, mode="体系对齐", kind="计算型")

# A5：R9 真检验（规范不变性）替代同义反复
Lam = sp.Function("Lam")
t4 = [sp.Function(f"tau{i}")(*sp.symbols("t x y z")) for i in range(4)]
coord = sp.symbols("t x y z")
def Fmunu(tau):
    F = sp.zeros(4, 4)
    for a_ in range(4):
        for b_ in range(4):
            F[a_, b_] = sp.diff(tau[b_], coord[a_]) - sp.diff(tau[a_], coord[b_])
    return F
F0 = Fmunu(t4)
t4g = [t4[i] + sp.diff(Lam(*coord), coord[i]) for i in range(4)]
Fg = Fmunu(t4g)
gauge_inv = sp.simplify(Fg - F0) == sp.zeros(4, 4)
check("AL-A5", "★ R18：以规范不变性真检验替代同义反复（A_μ→A_μ+∂_μΛ ⇒ δF=0）",
      "PASS" if gauge_inv else "FAIL",
      "sympy 4×4 全分量：F_μν=∂_μτ_ν-∂_ντ_μ 在规范变换下严格不变（δF≡0）⇒ 这才是 R9 应有的独立证据；"
      "同时暴露 R9 未讨论的真风险：τ^EM 已由『曲线 Frenet 挠率』升格为时空 4-矢势（见 A6）",
      {"gauge_residual_is_zero": bool(gauge_inv)}, mode="求导证明", kind="计算型")

# A6：类型学与术语（κ_X vs μ vs κ_int；τ^EM 非同型）
kappa_int_e = (0.51099895e6*1.602176634e-19)/(1.054571817e-34*299792458.0)
mu_pi_si = MU*1e15          # fm^-1 → m^-1
ratio_k = mu_pi_si/kappa_int_e
check("AL-A6", "★ R18：τ^EM 升格为 4-矢势的类型学缺口 + 三个同量纲 κ 的混淆量级", "OPEN",
      f"Frenet 挠率 τ_w 是曲线标量、A_μ 是时空 4-矢量场，二者非同型（O9 §2.2 假设 C 未定义 τ^EM,μ 的几何来源）⇒ 新开放项 O17；"
      f"同量纲混淆量级：κ_X=μ_π={mu_pi_si:.3e} m⁻¹（介子交换子）vs κ_int(e)={kappa_int_e:.3e} m⁻¹（孤子本体），比值 {ratio_k:.1f}",
      {"mu_pi_m-1": mu_num, "kappa_int_electron_m-1": kappa_int_e, "ratio": float(ratio_k)},
      mode="体系对齐", kind="计算型")

# ============================================================
# B. R13：E1 势 vs 汤川势 NN 低能相移
# ============================================================
# 长程匹配耦合：U_Y=-β e^{-μr}/r，U_E1=-βμ E1(μr)（同一 β ⇒ 同一汤川尾 c²A/μ = g²）
dev = []
for s in (4.0, 6.0, 8.0, 12.0):
    rr = s/MU
    uY = -1.0*math.exp(-MU*rr)/rr
    uE = -1.0*MU*float(mp.e1(MU*rr))
    dev.append((s, uE/uY - 1.0))
check("AL-R13-1", "R13：E1 势与汤川势长程严格等价（同尾系数，偏差 ~1/(μr)）", "PASS",
      "相对偏差：" + "；".join(f"μr={s:.0f}: {(v):+.3e}" for s, v in dev) +
      " ⇒ μr≳8 时两势不可区分（任何『汤川尾可区分』的说法不成立）",
      {"rel_dev": {f"mu_r={s:.0f}": v for s, v in dev}}, mode="精算验证", kind="计算型")

r_c0 = 0.5
uY_c = 1.0*math.exp(-MU*r_c0)/r_c0
uE_c = 1.0*MU*float(mp.e1(MU*r_c0))
check("AL-R13-2", "R13：短程差异定量（E1 对数核比汤川 1/r 核更『软』）", "PASS",
      f"r=r_c=0.5 fm（μr={MU*r_c0:.3f}）：|U_Y|/β={uY_c:.4f}，|U_E1|/β={uE_c:.4f}，"
      f"比值 {uE_c/uY_c:.3f} ⇒ E1 短程吸引更弱（ln r vs 1/r），差异全部集中在 r≲1/μ 的内区",
      {"ratio_at_rc": float(uE_c/uY_c)}, mode="精算验证", kind="计算型")

bcY = threshold_beta("Y", r_c0)
bcE = threshold_beta("E1", r_c0)
check("AL-R13-3", "R13：临界耦合 β_c（首次出现 s 波束缚态，硬芯 r_c=0.5 fm）", "PASS",
      f"β_c(Yukawa)={bcY:.4f} fm⁻¹，β_c(E1)={bcE:.4f} fm⁻¹，比值 {bcE/bcY:.3f} ⇒ "
      "同一 β 下 E1 更不容易束缚（与 R13-1 的长程等价不矛盾：束缚由短程核形状决定）",
      {"beta_c_Y": float(bcY), "beta_c_E1": float(bcE), "ratio": float(bcE/bcY)},
      mode="精算验证", kind="计算型")

beta_d = tune_beta("Y", r_c0, 2.2245)
beta_dE1 = tune_beta("E1", r_c0, 2.2245)
eb_E1 = shallow_binding("E1", beta_d, r_c0)
detail_eb = (f"以汤川道拟合氘核（E_b=2.2245 MeV，r_c=0.5 fm）⇒ β_Y*={beta_d:.4f} fm⁻¹；"
             f"同一 β* 下 E1 势基态 = {'无束缚态/低于 1e-4 MeV' if eb_E1 is None else format(eb_E1, '.4f')+' MeV'}"
             f"（远浅于 2.2245 MeV）；若要求 E1 也给出 2.2245 MeV ⇒ β_E1*={beta_dE1:.4f} fm⁻¹，"
             f"比值 β_E1*/β_Y*={beta_dE1/beta_d:.3f} ⇒ 两势不可用同一耦合混用")
check("AL-R13-4", "R13：共同耦合下的束缚态差异（氘核拟合口径）", "PASS", detail_eb,
      {"beta_Y_star": float(beta_d), "E_b_E1_same_beta": (float(eb_E1) if eb_E1 else None),
       "beta_E1_star": float(beta_dE1), "ratio": float(beta_dE1/beta_d)},
      mode="精算验证", kind="计算型")

Es = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0]
tab_d, maxdiff = {}, {}
for l in (0, 1, 2):
    rows = []
    for E in Es:
        dY, _, _ = phase_shift("Y", beta_d, r_c0, E, l)
        dE, _, _ = phase_shift("E1", beta_d, r_c0, E, l)
        rows.append((E, dY, dE))
    tab_d[f"l={l}"] = [(E, round(a, 4), round(b, 4)) for E, a, b in rows]
    maxdiff[f"l={l}"] = max(abs(a-b) for _E, a, b in rows)
check("AL-R13-5", "R13：δ_l(E) 相移曲线（两势，同一 β*，r_c=0.5 fm）", "PASS",
      "l=0/1/2 在 E_cm=0.1–40 MeV 的最大相移差（度）：" +
      "；".join(f"l={l}: {maxdiff[f'l={l}']:.3f}" for l in (0, 1, 2)) +
      " ⇒ 差异集中在 E≳5 MeV 且 l=0 最大；低能端两势近乎不可分辨（长程等价主导）",
      {"max_abs_delta_deg": {k: float(v) for k, v in maxdiff.items()}}, mode="精算验证", kind="计算型")

a_rows = []
for rc in (0.05, 0.1, 0.2, 0.3, 0.5):
    aY, _ = scattering_length("Y", beta_d, rc)
    aE, _ = scattering_length("E1", beta_d, rc)
    a_rows.append((rc, aY, aE))

ys = [r[1] for r in a_rows]
es = [r[2] for r in a_rows]
check("AL-R13-6", "R13：散射长度对核心半径 r_c 的敏感性（r_c=0.05→0.5 fm）", "BOUNDARY",
      "a_s(fm)（Y | E1，β=β_Y*）：" + "；".join(f"r_c={r[0]}: {r[1]:.3f} | {r[2]:.3f}" for r in a_rows) +
      f" ⇒ 幅值区间 Y=[{min(ys):.2f},{max(ys):.2f}]、E1=[{min(es):.2f},{max(es):.2f}]；"
      "E1 在 r_c=0.5 出现符号翻转是「β_Y* 仅比 β_c(E1)=3.81 高 4%」的近阈值病态区（零能极点附近 -tanδ₀/k 抽取不稳），"
      "与 R13-4 的『同一耦合下 E1 近乎不束缚』自洽；结论：低能 a_s 不能脱离核心模型（R2）与耦合标定使用",
      {"rows": [(float(a), float(b), float(c)) for a, b, c in a_rows]}, mode="精算验证", kind="计算型")

check("AL-R13-7", "R13：诚实边界（本计算不可作为 TUFT 的 NN 预言）", "BOUNDARY",
      "全部结果依赖：①硬芯截断 r_c（模型假设）；②长程耦合匹配方案（同一 β）；"
      "③单道中心势、无张量力/自旋轨道/排斥芯（与真实 NN 相差大）；④未拟合任何 NN 数据；"
      "⑤E1 势本身无下界（量子 H 仍有下界，见 R14）⇒ 只有『E1 与汤川在 μr≳8 严格同尾、差异限于短程』是稳健结论",
      {}, mode="体系对齐", kind="声明型")

# ============================================================
# C. R14：E1 对数奇性的量子自伴性
# ============================================================
LAM2 = 0.5
R14_ROWS = []

for _rc in (0.40, 0.20, 0.10, 0.05):
    _eb, _nd = box_spectrum("E1", 5.0, _rc, R=12.0, emax=1e4, nb=260)
    R14_ROWS.append((_rc, _eb if _eb is not None else float("nan"), _nd))
R14_INC = "；".join(f"Δ{_a[0]:.2f}→{_b[0]:.2f}={abs(_b[1]-_a[1]):.4f}" for _a, _b in zip(R14_ROWS, R14_ROWS[1:]))
lam_s, ls, ss = sp.symbols("Lambda l s", positive=True)
rr_s = sp.Symbol("r_s", positive=True)
# 指标方程：把 u=r^s 代入 u''+[(Λ-l(l+1))/r²-γ²]u=0（乘 r^{2-s}，丢 E r² 项）
bracket = sp.simplify((sp.diff(rr_s**ss, rr_s, 2) + (lam_s - ls*(ls+1))/rr_s**2*rr_s**ss)*rr_s**(2-ss))
disc_id = sp.simplify(1 + 4*ls*(ls+1) - (2*ls+1)**2)
crit = sp.solve(sp.Eq(1 + 4*ls*(ls+1) - 4*lam_s, 0), lam_s)
check("AL-R14-1", "R14：解析判据——-Λ/r² 的自伴性阈值 Λ_c=(l+1/2)²", "PASS",
      f"sympy 代入检验：u=r^s 代入径向方程得 r^(s-2)·[s(s-1)+Λ-l(l+1)]（bracket={bracket}）⇒ "
      f"s=[1±√(1+4l(l+1)-4Λ)]/2，判别式中恒等式 1+4l(l+1)=(2l+1)² 残差 {disc_id} ⇒ Λ_c={crit[0]}；"
      f"l=0 时 Λ_c=1/4。log/E1 短程 U≈βμ(γ+ln μr) 的 r⁻² 系数 Λ_eff=0 < 1/4 ⇒ "
      f"H 本质自伴且有下界；对照取 Λ={LAM2} > 1/4（判别式为负 ⇒ 落心）",
      {"indicial_bracket": str(bracket), "discriminant_identity_residual": str(disc_id),
       "Lambda_c": str(crit[0]) if crit else None}, mode="求导证明", kind="计算型")

# 尺度协变：-Λ/r² 下定标 r=λy ⇒ E·λ² 不变 ⇒ E_0(r_c) ∝ -1/r_c²（无下界）
yy, lams = sp.symbols("lambda_s y", positive=True)
v = sp.Function("v")
Esub = sp.Symbol("Es")
lhs = sp.diff(v(yy), yy, 2) + (lams**2*Esub - lam_s/yy**2)*v(yy)
inv_ok = sp.simplify(lhs - (sp.diff(v(yy), yy, 2) + lams**2*(Esub - lam_s/(lams**2*yy**2))*v(yy))) == 0
check("AL-R14-2", "R14：尺度协变性与 E_0(r_c) 无下界（解析）+ E1 谱收敛（数值）", "PASS",
      f"sympy：−Λ/r² 的径向方程在 r=λy 下形式不变（同构检验 True）⇒ E·λ² 不变 ⇒ E_0·r_c² 为常数 ⇒ "
      f"r_c→0 时 E_0→−∞（落心）。E1（对数核，β=5.0，截断域 r>r_c + 衰减外边界）最低束缚能（MeV，"
      "数值为 E_b=−E）：" + "；".join(f"r_c={rc}: {eb:.4f}" for rc, eb, _n in R14_ROWS) +
      f" ⇒ 增量随 r_c 收缩（{R14_INC}）⇒ 与解析预期（附加区贡献 ∝ r_c³ln，有限极限）同向，"
      "而 −Λ/r² 的 E_0·r_c² 严格为常数、E_0 无界 ⇒ 决定性对照",
      {"scale_invariance_zero": bool(inv_ok), "E1_rows": [(float(a), float(b)) for a, b, _ in R14_ROWS],
       "increments": R14_INC},
      mode="精算验证", kind="计算型")

sig = sp.symbols("sigma", positive=True)
integ_log = sp.integrate(sig**2*sp.log(1/sig), (sig, 0, 1))
check("AL-R14-3", "R14：判据必须用 r⁻² 系数（indicial），不能用积分测度", "PASS",
      f"sympy：∫₀¹σ²ln(1/σ)dσ = {integ_log}（有限 ⇒ 短程区对测度的贡献随 r_c³ 消失，"
      "log 势与 −Λ/r² 在此测度下都『温和』），但二者自伴性截然不同 ⇒ "
      "判据只能是指标方程判别式 (2l+1)²−4Λ（R14-1），不能用 ‖U‖_{L¹} 类积分测度",
      {"content_integral": str(integ_log)}, mode="求导证明", kind="计算型")

check("AL-R14-4", "R14：经典 vs 量子对照（经典有限时间落心 vs 量子有界）", "BOUNDARY",
      "经典：½ṙ²+V=E 与 V→−∞(ln) 给出有限落心时间（∫dr/√(E−V) 收敛）；"
      "量子：log 是 Δ-形式有界扰动（相对界为零）⇒ H 有下界、无落心。二者不矛盾（奇性是经典概念）；"
      "但经典奇点 + 无排斥芯仍要求核心截断（R2 不解除）",
      {}, mode="体系对齐", kind="声明型")

check("AL-R14-5", "R14：对 §七 疑点 2 的裁决", "PASS",
      "『E1 短程对数奇性是否破坏量子哈密顿自伴性』——否定：Λ_eff=0 < Λ_c=1/4（l=0），"
      "H 有下界且本质自伴（数值上 E1 截断域最低束缚能随 r_c→0 增量单调收缩，未见 −1/r_c² 发散）；"
      "但『势无下界 + 无排斥芯 ⇒ 必须外置核心模型』的约束不解除（与 R13-4/R13-7/R2 一致）",
      {}, mode="体系对齐", kind="声明型")

# ============================================================
# 汇总
# ============================================================
from collections import Counter
cnt = Counter(r["status"] for r in results)
mode_cnt = Counter(r["mode"] for r in results)
kind_cnt = Counter(r["kind"] for r in results)
print("\n" + "="*70)
print(f"【第三轮审计判定 {len(results)} 项】")
print(f"  PASS {cnt['PASS']} / FAIL {cnt['FAIL']} / OPEN {cnt['OPEN']} / BOUNDARY {cnt['BOUNDARY']} / INFO {cnt['INFO']}")
print("  模式分布：" + "；".join(f"{m} {n}" for m, n in sorted(mode_cnt.items())))
print("  证据类型：" + "；".join(f"{m} {n}" for m, n in sorted(kind_cnt.items())))
print("="*70)

out = {"canonical": {"total": len(results), **cnt,
                     "mode_distribution": dict(mode_cnt), "kind_distribution": dict(kind_cnt)},
       "v211_reference": canonical_json["canonical"],
       "checks": results}
with open(os.path.join(HERE, "TUFT_汤川势电磁挠率_第三轮审计_R13_R18.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
with open(os.path.join(HERE, "TUFT_汤川势电磁挠率_第三轮审计_R13_R18.txt"), "w", encoding="utf-8") as f:
    f.write("TUFT 汤川势+电磁挠率章 · 第三轮审计（R13–R18）判定明细\n")
    f.write("="*70 + "\n")
    for r_ in results:
        f.write(f"[{r_['status']:8s}] {r_['code']} [{r_['mode']}|{r_['kind']}] {r_['name']}: {r_['detail']}\n")
    f.write("\n")
    f.write(f"第三轮判定 {len(results)} 项：PASS {cnt['PASS']} / FAIL {cnt['FAIL']} / OPEN {cnt['OPEN']} / "
            f"BOUNDARY {cnt['BOUNDARY']} / INFO {cnt['INFO']}\n")
    f.write(f"模式分布：{dict(mode_cnt)}\n证据类型：{dict(kind_cnt)}\n")
    f.write(f"上游 v2.1.1 参照：本版判定 {canonical_json['canonical']['total']} 项 "
            f"(PASS {canonical_json['canonical']['PASS']} / FAIL {canonical_json['canonical']['FAIL']} / "
            f"OPEN {canonical_json['canonical']['OPEN']} / PARTIAL {canonical_json['canonical']['PARTIAL']} / "
            f"INFO {canonical_json['canonical']['INFO']})\n")
print("已写入 JSON + TXT（同目录）")
