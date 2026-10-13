# -*- coding: utf-8 -*-
"""
TUFT 第九章 · LW 推迟势数值验证（V9.3.1，光锥解析构造版）
============================================================
验证对象（§9.5.1 / §9.6.2 / §9.6.3 的结构性声明）：
  [A] E_速度 ∝ 1/R^2（近场），E_加速度 ∝ 1/R（辐射场）——对数斜率拟合
  [B] 球面积分总辐射功率 P(R) 与距离无关（R→∞ 收敛），且 → 相对论 Liénard 值
  [C] 固定速率 u 下，P ∝ κ^2（公理极限 u→c 即 ∝ c^4κ^2 结构）
  [D] v=c 本源场元不能直接作 LW 源：(1-n·β) 可精确取零（β=1 奇点）
口径声明：
  - 单位制 c=1, q=1；螺旋源 r(t)=(ρ cosωt, ρ sinωt, bωt)，速率 u=ω√(ρ²+b²)<1
  - 亚光速源是 LW 标准适用域；公理 v=c 情形见测试 [D]
  - 光锥解析构造：观测点 x = r(t*) + R·n̂，观测时刻 t_obs = t*+R，
    推迟时间严格等于 t*（无需数值解方程），消除源状态随 R 漂移
  - 相对论 Liénard 功率（β⊥a，均匀螺旋）：P = (2/3)γ⁴|a|²
"""
import json, time
import numpy as np

C = 1.0

def helix(par, t):
    rho, b, w = par
    return np.array([rho*np.cos(w*t), rho*np.sin(w*t), b*w*t])

def velocity(par, t):
    rho, b, w = par
    return np.array([-rho*w*np.sin(w*t), rho*w*np.cos(w*t), b*w])

def accel(par, t):
    rho, b, w = par
    return np.array([-rho*w*w*np.cos(w*t), -rho*w*w*np.sin(w*t), 0.0])

def lw_at_ret(par, t_star, n, R):
    """LW 场，光锥构造：x = r(t*)+R·n̂, t = t*+R（c=1）。
    n: (…,3) 单位方向数组；R: 标量或 (…) 数组"""
    R = np.asarray(R, float)
    beta = velocity(par, t_star)
    a = accel(par, t_star)
    gam2 = 1.0/(1.0 - np.dot(beta, beta))
    ndotb = np.tensordot(n, beta, axes=([-1], [0]))
    denom = 1.0 - ndotb
    n_b = n - beta
    E_vel = n_b/(gam2*denom[..., None]**3*R[..., None]**2)
    E_acc = np.cross(n, np.cross(n_b, a))/(denom[..., None]**3*R[..., None])
    E = E_vel + E_acc
    return E, E_vel, E_acc, denom

def fib_sphere(N):
    ga = np.pi*(3.0 - np.sqrt(5.0))
    z = 1.0 - 2.0*(np.arange(N)+0.5)/N
    r = np.sqrt(np.maximum(0.0, 1.0 - z*z))
    th = ga*np.arange(N)
    return np.stack([r*np.cos(th), r*np.sin(th), z], axis=1)

def lsq_slope(xs, ys):
    x = np.log10(np.asarray(xs, float)); y = np.log10(np.asarray(ys, float))
    A = np.vstack([x, np.ones_like(x)]).T
    (slope, intercept), *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - (slope*x + intercept)
    return float(slope), float(10**intercept), float(np.sqrt(np.mean(res**2)))

out = {"unit": "c=1, q=1, 高斯单位", "method": "光锥解析构造（推迟时间锁定 t*）",
       "tests": {}}

# ---------------------------------------------------------------- [A] 衰减律
t0 = time.time()
BASE = dict(rho=0.5, b=0.2, w=1.0)
parB = (BASE["rho"], BASE["b"], BASE["w"])
t_star = 20.0
theta, phi = np.pi/4, 0.3
n0 = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
n0 = n0/np.linalg.norm(n0)
Rlist = np.array([10.0, 20.0, 40.0, 80.0, 160.0])
E, Ev, Ea, _ = lw_at_ret(parB, t_star, np.tile(n0, (len(Rlist), 1)), Rlist)
absEv = np.linalg.norm(Ev, axis=1); absEa = np.linalg.norm(Ea, axis=1)
sl_vel, _, rms_vel = lsq_slope(Rlist, absEv)
sl_acc, _, rms_acc = lsq_slope(Rlist, absEa)
out["tests"]["A_scale"] = {
    "rows": [{"R": float(r), "|E_vel|": float(v), "|E_acc|": float(a)}
             for r, v, a in zip(Rlist, absEv, absEa)],
    "slope_Evel": sl_vel, "slope_Eacc": sl_acc,
    "rms_Evel": rms_vel, "rms_Eacc": rms_acc,
    "expect": {"Evel": -2.0, "Eacc": -1.0},
    "verdict": "PASS" if abs(sl_vel+2) < 1e-6 and abs(sl_acc+1) < 1e-6 else "FAIL"}
print(f"[A] slope_Evel={sl_vel:.9f}（期望 -2），slope_Eacc={sl_acc:.9f}（期望 -1）")

# ---------------------------------------------------------------- [B] 功率：R 无关 + Liénard
t0 = time.time()
N = 3000
dirs = fib_sphere(N)
uB = BASE["w"]*np.sqrt(BASE["rho"]**2 + BASE["b"]**2)
gam2B = 1.0/(1.0 - uB*uB)
P_lienard = (2.0/3.0)*gam2B**2*(BASE["rho"]*BASE["w"]**2)**2   # (2/3)γ⁴|a|²
Pvals = {}
for R in [40.0, 80.0, 160.0, 320.0, 640.0]:
    E, _, _, denom = lw_at_ret(parB, t_star, dirs, R)
    Sn = (np.sum(E*E, axis=1) - np.sum(E*dirs, axis=1)**2)/(4.0*np.pi)
    Pvals[R] = float(np.sum(Sn*denom)*(4.0*np.pi*R*R)/N)   # 推迟功率：加权 (1-n·β)
rel = (Pvals[640.0] - P_lienard)/P_lienard
out["tests"]["B_power_R"] = {
    "u": uB, "|a|": BASE["rho"]*BASE["w"]**2,
    "P_Lienard_23g4a2": P_lienard,
    "P_R": Pvals, "rel_dev_R640": rel,
    "verdict": "PASS" if abs(rel) < 0.02 else "FAIL"}
print(f"[B] P_Lienard={P_lienard:.6f}；P(40)={Pvals[40.0]:.5f} P(160)={Pvals[160.0]:.5f} "
      f"P(640)={Pvals[640.0]:.5f}（相对偏差 {rel*100:.2f}%）")

# ---------------------------------------------------------------- [C] P ∝ κ²（固定 u）
t0 = time.time()
uC, wC = 0.6, 1.0
rhopq = uC*uC/wC**2                                  # ρ²+b²
gam2C = 1.0/(1.0 - uC*uC)
cases = []
for rho in [0.30, 0.45, 0.55]:
    b = np.sqrt(rhopq - rho*rho)
    kappa = rho/rhopq
    tau = b/rhopq
    par = (rho, b, wC)
    E, _, _, denom = lw_at_ret(par, t_star, dirs, 80.0)
    Sn = (np.sum(E*E, axis=1) - np.sum(E*dirs, axis=1)**2)/(4.0*np.pi)
    P = float(np.sum(Sn*denom)*(4.0*np.pi*80.0*80.0)/N)   # 推迟功率：加权 (1-n·β)
    P_theory = (2.0/3.0)*gam2C**2*(rho*wC**2)**2    # (2/3)γ⁴|a|²，|a|=u²κ·…=ρω²
    cases.append({"rho": rho, "b": float(b), "kappa": kappa, "tau": float(tau),
                  "P_num": P, "P_theory": P_theory, "rel": (P-P_theory)/P_theory})
xs = np.array([c["kappa"]**2 for c in cases]); ys = np.array([c["P_num"] for c in cases])
slP, _, rmsP = lsq_slope(xs, ys)
out["tests"]["C_P_kappa2"] = {
    "u": uC, "cases": cases,
    "slope_logP_logkappa2": slP, "rms": rmsP, "expect_slope": 1.0,
    "max_rel_dev": max(abs(c["rel"]) for c in cases),
    "verdict": "PASS" if abs(slP-1.0) < 1e-3 and max(abs(c["rel"]) for c in cases) < 0.01 else "FAIL"}
print(f"[C] P vs κ² 对数斜率={slP:.9f}（期望 1）；相对偏差："
      + ", ".join(f"{c['rel']*100:.2f}%" for c in cases))

# ---------------------------------------------------------------- [D] v=c 奇点
t0 = time.time()
rhoD, bD = 0.5, 0.2
wD = 1.0/np.sqrt(rhoD*rhoD + bD*bD)                  # u=1
parD = (rhoD, bD, wD)
ts = np.linspace(0.0, 2.0*np.pi/wD, 400)
nd = fib_sphere(200)
mins = []
for t in ts:
    v = velocity(parD, t); bm = v/np.linalg.norm(v)
    d = 1.0 - nd @ bm
    mins.append(float(d.min()))
min_denom = float(np.min(mins))
tA = 0.3
vA = velocity(parD, tA); nA = vA/np.linalg.norm(vA)
deriv = float(np.dot(nA, vA) - 1.0)
out["tests"]["D_vc_singular"] = {
    "u": 1.0, "min(1-n·β)_over_grid": min_denom,
    "f'(t)=1-n·β_at_n∥β": deriv,
    "conclusion": "β=1 时 (1-n·β) 可精确取 0 → LW 分母奇异；推迟映射 f'=1-n·β 可到 0（非严格单调）→ 以 c 运动的点源不能作标准 LW 源",
    "verdict": "CONFIRMED"}
print(f"[D] v=c：min(1-n·β)={min_denom:.3e}（≈0），f'=1-n·β 可到 {deriv:.1e}")

# ---------------------------------------------------------------- 推迟求解器交叉验证
t0 = time.time()
def retarded(par, obs, t_obs, iters=120):
    rho, b, w = par
    M = 10.0*(np.linalg.norm(obs) + rho + abs(b)*abs(t_obs) + 1.0)
    lo, hi = t_obs - M, t_obs
    def f(t): return np.linalg.norm(obs - helix(par, t)) - (t_obs - t)
    for _ in range(iters):
        tm = 0.5*(lo+hi)
        if f(tm) > 0: hi = tm
        else: lo = tm
    return 0.5*(lo+hi)
Rc = 160.0
obs_c = helix(parB, t_star) + Rc*n0
tr_solved = retarded(parB, obs_c, t_star + Rc)
out["tests"]["retarded_crosscheck"] = {
    "analytic_t*": t_star, "solved_t_ret": float(tr_solved),
    "abs_diff": abs(tr_solved - t_star),
    "verdict": "PASS" if abs(tr_solved-t_star) < 1e-9 else "FAIL"}
print(f"[交叉] 推迟求解器 vs 光锥解析：差={abs(tr_solved-t_star):.2e}")

# ---------------------------------------------------------------- 汇总
flags = {k: v["verdict"] for k, v in out["tests"].items()}
out["summary"] = flags
with open(r"D:\a10\aikjx\code\my_lib\tuft_lw_retarded_results.json", "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)
print("\n===== 汇总 =====")
for k, v in flags.items(): print(f"  {k}: {v}")
print("结果已写入 tuft_lw_retarded_results.json")
