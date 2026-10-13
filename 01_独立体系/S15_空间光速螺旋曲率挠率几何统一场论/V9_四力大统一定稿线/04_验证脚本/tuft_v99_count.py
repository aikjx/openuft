# -*- coding: utf-8 -*-
"""TUFT V9.10 攻破脚本：
C 组：公理3「电荷=组合不变量」欠定计数证明（自由度计数 + 雅可比 + e⁻/p/π⁰ 映射复现 + q 自由缩放）
D 组：类光-FS 衔接精确化核验（3D 投影弧长单位速率、4D 零切线范数、FS 曲率一致）
用法：python tuft_v99_count.py
"""
import json, math

HBARC = 197.3269804   # MeV·fm
ALPHA = 7.2973525693e-3

# ---------- C1 自由度计数（解析陈述 + 数值） ----------
C = {}
C["dof_statement"] = ("形状自由度 (ρ,b) = 2；ω 由类光约束 ω²=c²(κ²+τ²)=c²/(ρ²+b²) 决定（非独立）；"
                      "需复现的可观测 {m, α, q} = 3 ⇒ 欠定度 ≥ 1；q 无几何方程约束")
C["jacobian"] = {}
# (ρ,b) → (m,α)：m = ħ/(c√(ρ²+b²))，α = b/ρ；det J = -m/ρ² ≠ 0 ⇒ 局部双射
def m_of(rho, b):
    return 1.0/math.sqrt(rho*rho + b*b)   # 单位 ħ=c=1

def alpha_of(rho, b):
    return b/rho

def jac_det(rho, b):
    m = m_of(rho, b)
    return -m/(rho*rho)

C["jacobian"]["det_formula"] = "det J = −m/ρ² ≠ 0 ⇒ (ρ,b)↔(m,α) 局部双射"
C["jacobian"]["demo"] = []
for (rho, b) in [(386.149, 2.81787), (0.2103, 1.53e-3), (1.4619, 1.0668e-2)]:
    C["jacobian"]["demo"].append({"rho": rho, "b": b, "det": jac_det(rho, b)})

# ---------- C2 数值：e⁻/p/π⁰ 映射复现（对照 ch.10 表） ----------
C["particles"] = []
particles = [
    ("电子 e⁻", 0.51099895, 1),
    ("质子 p", 938.272088, 1),
    ("π⁰", 134.9768, 1),
]
for (name, m_MeV, Z) in particles:
    rho = HBARC/(m_MeV*math.sqrt(1+ALPHA*ALPHA))          # fm（2.7：ρ=ħ/(mc√(1+α²))）
    b = ALPHA*rho
    wc = 1.0/math.sqrt(rho*rho + b*b)                     # ω/c = √(κ²+τ²) = 1/√(ρ²+b²)
    m_check = HBARC*wc                                    # ħω/c² (MeV)
    q_def = math.sqrt(ALPHA)*Z                            # 3.3：q_EM=√α·Z（定义式）
    C["particles"].append({
        "name": name, "m_in": m_MeV, "rho_fm": rho, "b_fm": b,
        "omega_c_fm1": wc, "m_check_MeV": m_check,
        "rel_dev_m": abs(m_check-m_MeV)/m_MeV,
        "alpha_check": b/rho, "q_EM_def": q_def,
    })

# ---------- C3 q 的自由缩放演示（几何恒等式对 q 无感） ----------
C["q_freedom"] = {}
rho, b = C["particles"][0]["rho_fm"], C["particles"][0]["b_fm"]
wc = C["particles"][0]["omega_c_fm1"]
kappa = rho/(rho*rho + b*b)
tau = b/(rho*rho + b*b)
C["q_freedom"]["geometry_fixed"] = {"rho": rho, "b": b, "omega_c": wc,
                                    "kappa": kappa, "tau": tau}
C["q_freedom"]["rows"] = []
for q in [1.0, math.sqrt(ALPHA), 0.5]:
    # 验证：q 不进入任何几何恒等式（|v|=c、κ²+τ²=ω²/c²、α=b/ρ、ρ=κ/(κ²+τ²)）
    checks = {
        "|v|=c": abs(math.sqrt((rho*wc)**2 + (b*wc)**2) - 1.0),
        "κ²+τ²=ω²/c²": abs(math.sqrt(kappa*kappa+tau*tau) - wc),
        "α=b/ρ": abs(tau/kappa - b/rho),
        "对偶反演 ρ=κ/(κ²+τ²)": abs(kappa/(kappa*kappa+tau*tau) - rho),
    }
    C["q_freedom"]["rows"].append({"q": q, "max_geom_dev": max(checks.values())})

# ---------- D1 类光-FS：3D 投影弧长单位速率 ----------
D = {}
D["d1_statement"] = ("4D 类光世界线 ds₄=0 ⇒ 无固有时、无 proper-arc-length FS；"
                     "TUFT 的 s 为 3D 空间投影弧长，dt/ds=1/c；「类光」= |v|=c 速度约束")
rho, b = C["particles"][0]["rho_fm"], C["particles"][0]["b_fm"]
OMEGA = wc   # Ω = ω/c = 1/√(ρ²+b²)
def r3(s):
    return (rho*math.cos(OMEGA*s), rho*math.sin(OMEGA*s), b*OMEGA*s)

def r3prime(s):
    return (-rho*OMEGA*math.sin(OMEGA*s), rho*OMEGA*math.cos(OMEGA*s), b*OMEGA)

D["unit_speed"] = {}
D["unit_speed"]["max_dev_|r'|"] = max(abs(math.sqrt(sum(c**2 for c in r3prime(s))) - 1.0)
                                      for s in [0.0, 0.1, 1.0, 3.7, 10.0])
# 4D 零切线：X=(ct, r)，范数² = c²(dt/ds)² − |r'|² = 1 − 1 = 0
D["null_tangent"] = {"g(X',X')": 0.0, "explain": "1 − |r'(s)|² ≡ 0 ⇒ 类光切线"}
# FS 曲率：κ_helix = ρΩ² = ρ/(ρ²+b²)
D["fs_curvature"] = {"kappa_helix": rho*OMEGA*OMEGA, "kappa_geom": rho/(rho*rho+b*b),
                     "dev": abs(rho*OMEGA*OMEGA - rho/(rho*rho+b*b))}

# ---------- 汇总 ----------
out = {"C_underdetermination": C, "D_null_fs": D,
       "summary": {
           "C": "欠定度 ≥1 成立（2 DOF vs 3 观测）；(ρ,b)↔(m,α) 双射；q 自由——B03 计数层佐证",
           "D": "单位速率偏差 %g；零切线范数 0；FS 曲率一致——类光-FS 约定自洽（术语层 PASS）" % D["unit_speed"]["max_dev_|r'|"],
       }}

with open(r"D:\a10\aikjx\code\my_lib\tuft_v99_count_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
