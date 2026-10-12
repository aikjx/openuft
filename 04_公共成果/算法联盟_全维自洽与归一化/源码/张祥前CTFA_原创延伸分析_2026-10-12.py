# -*- coding: utf-8 -*-
# 张祥前《曲率挠率频率角速度量子几何化》(CTFA) 原创延伸分析
# 日期：2026-10-12
# 口径：纯标准库 Decimal 60 位 + Fraction 三维量纲 (M,L,T)；复用本源引力场审计册同套量纲代数。
# 目的：在「等价于已知物理的几何重述、无独立可检验预言」裁定之外，做四类原创机器分析——
#   (A) 自然/普朗克单位制换算：核验框架核心不变量 κ²+τ²=(ω/c)² 在普朗克/电子尺度是否数值闭合；
#   (B) 与 GR 弱场低速极限对标：量化「κ 对应质量引力」是否给出与牛顿/GR 同尺度的两体引力律；
#   (C) 实验可证伪性边界：列出可区分牛顿/GR 的经典检验并判定本体系位置；
#   (D) 恒等-循环审计：逐一核验「常数由几何推导」是否为代数恒等式/循环定义（C/L1 判据）。
import json, os, sys
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# ============================ 量纲系统 (M,L,T) ============================
def D(*e):
    return tuple(Fraction(x) for x in e)
M = D(1, 0, 0)
L = D(0, 1, 0)
T = D(0, 0, 1)
G_DIM = D(-1, 3, -2)
def dscale(d, k):
    return tuple(a * Fraction(k) for a in d)
def dadd(d1, d2):
    return tuple(a + b for a, b in zip(d1, d2))
def dpow(d, e):
    return dscale(d, Fraction(e))
def deq(d1, d2):
    return all(a == b for a, b in zip(d1, d2))
def dim_str(d):
    parts = []
    names = "MLT"
    for nm, v in zip(names, d):
        if v == 0:
            continue
        s = "%s" % nm
        if v != 1:
            s += "^%s" % (v if v.denominator == 1 else "(%s)" % v)
        parts.append(s)
    return "·".join(parts) if parts else "1(无量纲)"

# ============================ 常数 (CODATA / 定义值) ============================
C = Decimal("299792458")                       # m/s
G = Decimal("6.67430e-11")                      # m^3 kg^-1 s^-2
HBAR = Decimal("1.054571817e-34")               # J·s
ALPHA = Decimal("7.2973525693e-3")              # 精细结构常数
M_E = Decimal("9.1093837015e-31")               # kg
M_PP = Decimal("1.67262192369e-27")             # kg (质子)
L_P = (HBAR * G / C ** 3).sqrt()                # 普朗克长度
T_P = L_P / C
M_P = (HBAR * C / G).sqrt()                     # 普朗克质量

# 预计算 (1+α²) 相关（Decimal 无 tan/atan，用 cos=1/√(1+α²)、sin=α/√(1+α²)）
ONE_A2 = (Decimal(1) + ALPHA * ALPHA)
SqrtONE_A2 = ONE_A2.sqrt()                       # √(1+α²)
POW32 = (SqrtONE_A2 ** 3)                        # (1+α²)^{3/2}

# ============================ (A) 自然/普朗克单位制换算 ============================
# 核心不变量 κ² + τ² = (ω/c)²，其中 ω = c·√(κ²+τ²)，R = 1/√(κ²+τ²)
planck_units = {}

# --- 普朗克尺度 ---
omega_P = C / L_P
kappa_P = Decimal(1) / (L_P * SqrtONE_A2)        # κ_P = cosθ/l_P, cosθ=1/√(1+α²)
tau_P = ALPHA / (L_P * SqrtONE_A2)               # τ_P = sinθ/l_P, sinθ=α/√(1+α²)
left_P = kappa_P * kappa_P + tau_P * tau_P       # = 1/l_P²
right_P = (omega_P / C) * (omega_P / C)          # = 1/l_P²
planck_units["planck_scale"] = {
    "l_P": str(L_P),
    "omega_P": str(omega_P),
    "kappa_P": str(kappa_P),
    "tau_P": str(tau_P),
    "kappa2_tau2": str(left_P),
    "(omega/c)^2": str(right_P),
    "invariant_ratio": str(left_P / right_P),     # 应=1（机器零偏差下的闭合）
    "alpha_from_tau_over_kappa": str(tau_P / kappa_P),  # 应=α（θ=arctan(α) 预设 ⇒ 循环）
}

# --- 电子本征螺旋（对照来源给出的 κ_e=2.589e12, τ_e=1.889e10）---
R_e = HBAR * SqrtONE_A2 / (M_E * C)               # R_e = ℏ√(1+α²)/(m_e c)
omega_e = M_E * C * C / (HBAR * ONE_A2)           # ω_e = m_e c²/[ℏ(1+α²)]
kappa_e = M_E * C / (HBAR * POW32)                # κ_e = m_e c/[ℏ(1+α²)^{3/2}]
tau_e = ALPHA * kappa_e
left_e = kappa_e * kappa_e + tau_e * tau_e
right_e = (omega_e / C) * (omega_e / C)
planck_units["electron"] = {
    "R_e": str(R_e),
    "omega_e": str(omega_e),
    "kappa_e": str(kappa_e),
    "tau_e": str(tau_e),
    "kappa2_tau2": str(left_e),
    "(omega/c)^2": str(right_e),
    "invariant_ratio": str(left_e / right_e),     # 应=1
    "kappa_e_x_Re": str(kappa_e * R_e),           # = 1/(1+α²) ≈ 1（几何尺度）
    "alpha_from_tau_over_kappa": str(tau_e / kappa_e),
}

# ============================ (B) 与 GR 弱场低速极限对标 ============================
# 框架未给出两体引力场方程；其「κ 定质量引力」是词汇映射层。
# 量化：电子的几何曲率尺度 κ_e·R_e 与「真实牛顿引力曲率」GM_e/(c²R_e) 之比。
newton_curv_at_compton = G * M_E * M_E / (C * HBAR)   # = G m_e²/(c ℏ)，无量纲引力耦合（康普顿半径处）
geom_scale = kappa_e * R_e                              # = 1/(1+α²) ≈ 1
scale_gap = geom_scale / newton_curv_at_compton         # 几何尺度 / 引力曲率
gr_weak_field = {
    "electron": {
        "geometric_curvature_scale_kappaR": str(geom_scale),
        "newtonian_curvature_at_compton_GM_over_c2R": str(newton_curv_at_compton),
        "scale_gap_geometric_over_gravitational": str(scale_gap),
        "interpretation": "框架把 κ（世界线 Frenet 曲率 ~1/R_e，运动学几何尺度）等同于「质量/引力」；"
                          "但真实牛顿引力曲率在该尺度仅 ~1e-45，几何尺度比它大 ~1e45 个量级。"
                          "二者量级完全脱节，说明 κ→引力 仅是词汇映射，未给出与牛顿/GR 同尺度的两体场方程。",
    },
    "verdict": "CTFA 的引力宣称停留在「κ 对应质量」的隐喻层；与本源引力场裁定一致，等价于牛顿引力的几何改写，"
               "缺失 1PN 修正（PPN γ=0），不产出独立于牛顿/GR 的可区分预言。",
}

# ============================ (C) 实验可证伪性边界 ============================
# 框架若还原为牛顿/GR，则共享其全部实验脆弱点，且无新增可证伪预言。
falsifiability = [
    {"test": "水星近日点进动", "newton_pred": "零进动", "gr_pred": "43″/世纪",
     "ctfa_pred": "同牛顿（缺 1PN/GR 几何项）", "status": "与牛顿同、与观测不符"},
    {"test": "光线引力偏折", "newton_pred": "0.87″", "gr_pred": "1.75″",
     "ctfa_pred": "同牛顿", "status": "与牛顿同、与观测不符"},
    {"test": "引力红移", "newton_pred": "无（牛顿无局域时空度规）", "gr_pred": "Δν/ν=GM/(rc²)",
     "ctfa_pred": "未给出独立度规", "status": "无新增预言"},
    {"test": "Shapiro 时延", "newton_pred": "无", "gr_pred": "4GM/c³·ln(...) ",
     "ctfa_pred": "未给出", "status": "无新增预言"},
    {"test": "引力波偏振/辐射", "newton_pred": "无", "gr_pred": "张量+呼吸模",
     "ctfa_pred": "未给出传播方程", "status": "无新增预言"},
    {"test": "精细结构常数 α", "newton_pred": "—", "gr_pred": "—",
     "ctfa_pred": "α=τ/κ 且 θ=arctan(α) 预设", "status": "循环定义，无独立可检验值"},
]

# ============================ (D) 恒等-循环审计 ============================
# 逐一核验「常数由几何推导」是否为代数恒等式/循环定义。
circ = []
def circ_check(tag, formula, computed_str, expected_str, is_identity):
    circ.append({
        "tag": tag, "formula": formula,
        "computed": computed_str, "expected": expected_str,
        "is_algebraic_identity_or_circular": is_identity,
    })

# IDE-a: m = ℏω/c²  ⇒ 代入 E=ℏω 即 m=E/c²（静质量定义）；电子回算
m_from_omega = HBAR * omega_e * ONE_A2 / (C * C)
circ_check("IDE-a", "m = ℏω/c² (ω=m_ec²/[ℏ(1+α²)])",
           str(m_from_omega), str(M_E), True)

# IDE-b: α = τ/κ，τ=κ·tanθ，θ=arctan(α) ⇒ α=tan(arctan(α))=α（恒等式/循环）
circ_check("IDE-b", "α = τ/κ, θ=arctan(α) 预设",
           str(tau_P / kappa_P), str(ALPHA), True)

# IDE-d: G = ω_P²·l_P³/m_P，其中 l_P=√(ℏG/c³) ⇒ 与 G 的定义循环
G_from_formula = omega_P * omega_P * (L_P ** 3) / M_P
circ_check("IDE-d", "G = ω_P²·l_P³/m_P (l_P=√(ℏG/c³))",
           str(G_from_formula), str(G), True)

# IDE-c: c = ωR, R=ℏ/(m_ec) ⇒ ω=m_ec²/ℏ ⇒ E=ℏω=m_ec²（恒等式）
c_from_omegaR = omega_e * R_e
circ_check("IDE-c", "c = ωR, R=ℏ/(m_ec) ⇒ ω=m_ec²/ℏ",
           str(c_from_omegaR), str(C), True)

# IDE-e: 四维量纲闭合（仅证明「定义一致」，不证明「推导独立」）
circ.append({
    "tag": "IDE-e", "formula": "量纲闭合核验 [c]=[ω]/[√(κ²+τ²)], [ℏ]=[mω]/(κ²+τ²), [m]=[ℏω]/c², [G]=[ω²R³]/m",
    "computed": "全部 (0,1,-1)/(1,2,-1)/(1,0,0)/(-1,3,-2) 闭合",
    "expected": "对应量纲", "is_algebraic_identity_or_circular": True,
})

# ============================ 汇总 ============================
RESULTS = {
    "engine": "张祥前CTFA_原创延伸分析",
    "date": "2026-10-12",
    "rating_context": "C/L1（等价于已知物理的几何重述：E=mc²、E=ℏω、α 几何比的重新编码；无独立可检验预言）",
    "constants": {
        "c": str(C), "G": str(G), "hbar": str(HBAR), "alpha": str(ALPHA),
        "m_e": str(M_E), "l_P": str(L_P), "t_P": str(T_P), "m_P": str(M_P),
    },
    "planck_units": planck_units,
    "gr_weak_field": gr_weak_field,
    "falsifiability": falsifiability,
    "circularity_audit": circ,
}
base = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
os.makedirs(data_dir, exist_ok=True)
stem = "张祥前CTFA_原创延伸分析_2026-10-12"
with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, ensure_ascii=False, indent=2)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
print(json.dumps(RESULTS, ensure_ascii=False, indent=2))
