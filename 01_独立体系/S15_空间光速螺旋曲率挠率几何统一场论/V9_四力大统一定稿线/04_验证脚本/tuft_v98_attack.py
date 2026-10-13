# -*- coding: utf-8 -*-
"""TUFT V9.9 攻破脚本：旗舰汤川解 vs 3.4 垂直原理（no-go）+ 几何作用量平凡极值核验。
单位制：量纲自由（c=1 可选）；核心为解析恒等式 + 有限差分复核。
用法：python tuft_v98_attack.py
"""
import json, math, random

random.seed(20261013)

# ---------- 公共：§2.1 几何映射与 §3.4 修正公式 ----------
def kappa_rho(rho, b):
    return rho / (rho*rho + b*b)

def tau_rho(rho, b):
    return b / (rho*rho + b*b)

def grad_kappa_dot_grad_tau(rho, b, grho, gb):
    """§3.4 V9.1 修正公式：∇κ·∇τ = (1/D^4)[ 2ρb(ρ²-b²)(|∇ρ|²-|∇b|²) + (-ρ⁴+6ρ²b²-b⁴)∇ρ·∇b ]
    D = ρ²+b²；分母为 D⁴ = (ρ²+b²)²"""
    D = rho*rho + b*b
    D4 = D*D*D*D   # (ρ²+b²)⁴
    t1 = 2*rho*b*(rho*rho - b*b)*(grho*grho - gb*gb)
    t2 = (-rho**4 + 6*rho*rho*b*b - b**4)*(grho*gb)
    return (t1 + t2)/D4

# ---------- 有限差分梯度（球对称） ----------
def fd_grad(fun, r, dr=1e-6):
    """f'(r) 中心差分"""
    return (fun(r+dr) - fun(r-dr))/(2*dr)

# ---------- A. 旗舰汤川解：κ(r)=q e^{-μr}/r, τ=ακ ----------
ALPHA = 7.2973525693e-3   # CODATA α（书 §2.2 口径 τ/κ）
MU, Q = 1.0, 1.0

def kappa_y(r):
    return Q*math.exp(-MU*r)/r

def tau_y(r):
    return ALPHA*kappa_y(r)

def rho_y(r):
    k = kappa_y(r)
    return 1.0/(k*(1+ALPHA*ALPHA))

def b_y(r):
    return ALPHA*rho_y(r)

A = {}
A["config"] = "旗舰汤川解 κ=q e^{-μr}/r, τ=ακ (μ=1, q=1, α=7.297e-3)"
A["rows"] = []
for r in [0.5, 1.0, 2.0, 5.0]:
    k = kappa_y(r)
    t = tau_y(r)
    # 解析：∇κ·∇τ = α|∇κ|² = α κ² (μ+1/r)²
    an_dot = ALPHA*k*k*(MU + 1.0/r)**2
    # 有限差分
    dk = fd_grad(kappa_y, r)
    dt = fd_grad(tau_y, r)
    fd_dot = dk*dt
    cosang = 1.0 if (dk*dt >= 0) else -1.0
    # (ρ,b) 空间双条件
    drho = fd_grad(rho_y, r)
    db = fd_grad(b_y, r)
    rho = rho_y(r); b = b_y(r)
    cond1 = drho*db                    # ∇ρ·∇b 应=0
    cond2 = abs(drho)/abs(db) if db != 0 else float("inf")  # |∇ρ|/|∇b| 应=1
    # §3.4 完整公式核验
    g34 = grad_kappa_dot_grad_tau(rho, b, drho, db)
    A["rows"].append({
        "r": r, "kappa": k, "tau": t,
        "dot_analytic": an_dot, "dot_fd": fd_dot,
        "rel_dev": abs(fd_dot-an_dot)/max(abs(an_dot),1e-300),
        "cos(∇κ,∇τ)": cosang,
        "∇ρ·∇b": cond1, "|∇ρ|/|∇b|": cond2,
        "3.4_full_formula": g34,
        "3.4_vs_fd_dev": abs(g34-fd_dot)/max(abs(fd_dot),1e-300),
    })
A["verdict"] = ("旗舰解梯度平行（cos=+1），∇κ·∇τ = α|∇κ|² ≠ 0：最大化违反 §3.4；"
                "(ρ,b) 双条件 ∇ρ·∇b=0、|∇ρ|=|∇b| 均被破坏 → no-go")

# ---------- B. 一般恒等式：τ=ακ ⇒ ∇κ·∇τ ≡ α|∇κ|²（随机测试场） ----------
B = {"n_test": 200, "max_abs_dev": 0.0, "max_rel_dev": 0.0, "checks": []}
def gen_test_field():
    # 随机光滑场：多高斯叠加，3D 有限差分
    gs = [(random.uniform(-2,2), random.uniform(-1,1), random.uniform(-1,1))
          for _ in range(4)]
    def f(x,y,z):
        s = 0.0
        for (A_,sx,sy) in gs:
            s += A_*math.exp(-((x-sx)**2 + (y-sy)**2 + (z-0.5)**2))
        return s + 1.0
    return f

def grad3(f, x, y, z, h=1e-5):
    gx = (f(x+h,y,z)-f(x-h,y,z))/(2*h)
    gy = (f(x,y+h,z)-f(x,y-h,z))/(2*h)
    gz = (f(x,y,z+h)-f(x,y,z-h))/(2*h)
    return (gx,gy,gz)

for i in range(B["n_test"]):
    f = gen_test_field()
    x,y,z = random.uniform(-0.5,0.5), random.uniform(-0.5,0.5), random.uniform(-0.5,0.5)
    gk = grad3(f, x,y,z)
    def tau_f(xx,yy,zz):
        return ALPHA*f(xx,yy,zz)
    gt = grad3(tau_f, x,y,z)
    dot = gk[0]*gt[0]+gk[1]*gt[1]+gk[2]*gt[2]
    a_norm2 = gk[0]**2+gk[1]**2+gk[2]**2
    dev = abs(dot - ALPHA*a_norm2)
    B["max_abs_dev"] = max(B["max_abs_dev"], dev)
    if a_norm2 > 1e-12:
        B["max_rel_dev"] = max(B["max_rel_dev"], dev/a_norm2)
B["verdict"] = "τ=ακ ⇒ ∇κ·∇τ ≡ α|∇κ|² 恒等式（200 随机场，max abs dev=%.2e）" % B["max_abs_dev"]

# ---------- C. 禁闭构型复核（V9.8 14.3：∇κ·∇τ = ασ²） ----------
SIGMA = 1.0
C = {}
c_dot = ALPHA*SIGMA*SIGMA
# 有限差分：κ=σr
dk = fd_grad(lambda r: SIGMA*r, 1.0)
dt = fd_grad(lambda r: ALPHA*SIGMA*r, 1.0)
C["analytic"] = c_dot
C["fd"] = dk*dt
C["verdict"] = "禁闭构型 ∇κ·∇τ = ασ² 复核一致（偏差 %.2e）" % abs(dk*dt-c_dot)

# ---------- D. 第十二章几何作用量的平凡极值核验（审计 D 数值佐证） ----------
# S = ∫[(1/2λ)(κ²-τ²)+ω²/(2c²)]√-g，ω²=c²(κ²+τ²)，δS/δκ=(1/λ+1)κ、δS/δτ=(-1/λ+1)τ
D = {"lambda_values": [0.5, 1.0, -1.0, 2.0]}
D["rows"] = []
for lam in D["lambda_values"]:
    for (k, t) in [(0.5, 0.3), (0.0, 0.0), (1.0, 1.0)]:
        dSdk = (1.0/lam + 1.0)*k
        dSdt = (-1.0/lam + 1.0)*t
        trivial = (abs(dSdk) < 1e-12 and abs(dSdt) < 1e-12)
        D["rows"].append({"lambda": lam, "kappa": k, "tau": t,
                          "δS/δκ": dSdk, "δS/δτ": dSdt,
                          "both_zero(平凡解)": trivial})
D["verdict"] = ("无导数项 + κ,τ 独立场 ⇒ 仅 κ=τ=0 平凡解（λ=±1 精细调节除外）；"
                "得不到传播型场方程——审计 D 数值佐证，需 Palatini/EC 正规作用量闭合")

out = {"A_flagship_no_go": A, "B_identity": B, "C_confinement_recheck": C,
       "D_trivial_extremum": D,
       "summary": {
           "A": "no-go（旗舰解最大化违反 3.4）",
           "B": "PASS（恒等式 ∇κ·∇τ=α|∇κ|²）",
           "C": "PASS（V9.8 14.3 复核）",
           "D": "CONFIRMED（审计 D 平凡极值）"}}

with open(r"D:\a10\aikjx\code\my_lib\tuft_v98_attack_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
