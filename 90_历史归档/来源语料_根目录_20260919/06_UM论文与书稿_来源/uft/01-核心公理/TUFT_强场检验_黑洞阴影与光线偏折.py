# -*- coding: utf-8 -*-
"""
TUFT-C 强场检验：黑洞阴影 / 光子球 / 光线偏折（实跑）。

为什么做这个（比 C11 更硬）：
  TUFT-C 外部度规 g_rr=e^{2M/r}, -g_00=e^{-2M/r} 在**所有 r>0 都有限非零** ⇒
  它**没有有限半径事件视界**（GR 的 1-2M/r 在 r=2M 归零）。视界/光子球的位置与大小
  直接决定黑洞阴影的临界冲击参数 b_c，而 EHT 已实测 M87* / Sgr A* 阴影角直径。
  这是纯外部真空计算（不涉及 H7 内部度规），因此是 TUFT-C 绕不开的检验场。

方法论：mpmath 40 位；光子轨道 (du/dφ)^2 = 1/b^2 - f(u)，u=1/r，
        f(u) = u^2 / B(u)（A·B=1 两类度规都成立：GR A=1-2Mu,B=(1-2Mu)^{-1}；
        TUFT-C A=e^{-2Mu},B=e^{2Mu}）；光子球 f'(u)=0；b_c=1/sqrt(f(u_c))。
        偏折角 = 2∫_0^{u_c} du/sqrt(1/b^2-f(u)) - π；表面弯曲角 = ∫_0^{1/R} du/sqrt(1/b^2-f(u))。
红线：数值只原样记录；"与 EHT 冲突"是 TUFT-C 外部解的直接推论，不是外部数据问题。
运行：python uft/01-核心公理/TUFT_强场检验_黑洞阴影与光线偏折.py
"""

import sys
import json
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mpmath as mp

mp.mp.dps = 40

M = mp.mpf(1)  # 几何单位 G=c=1，质量单位 M

# ---- 度规函数 f(u)=u^2/B(u)（A·B=1）----
def f_GR(u):
    return u ** 2 * (1 - 2 * M * u)

def f_TUFT(u):
    return u ** 2 * mp.e ** (-2 * M * u)

# ---- 光子球：f'(u)=0 ----
u_phot_GR_analytic = 1 / (3 * M)
u_phot_T_analytic = 1 / M  # 解析（f'=2u e^{-2Mu}(1-Mu)=0）
u_phot_GR = mp.findroot(lambda u: mp.diff(f_GR, u), mp.mpf("0.3") / M)
u_phot_T = mp.findroot(lambda u: mp.diff(f_TUFT, u), mp.mpf("0.9") / M)

b_c_GR = 1 / mp.sqrt(f_GR(u_phot_GR))     # 应 = 3*sqrt(3) M
b_c_T = 1 / mp.sqrt(f_TUFT(u_phot_T))     # 预期 = M*e

print("=== A. 光子球与临界冲击参数 b_c ===")
print("GR      : u_c=%s (r_c=%s M)   b_c=%s  (解析 3*sqrt3=%s)" %
      (mp.nstr(u_phot_GR, 8), mp.nstr(1 / u_phot_GR, 8), mp.nstr(b_c_GR, 10),
       mp.nstr(3 * mp.sqrt(3), 10)))
print("TUFT-C  : u_c=%s (r_c=%s M)   b_c=%s  (解析 e=%s)" %
      (mp.nstr(u_phot_T, 8), mp.nstr(1 / u_phot_T, 8), mp.nstr(b_c_T, 10), mp.nstr(mp.e, 10)))
ratio_bc = b_c_GR / b_c_T
print("b_c 比值 GR/TUFT-C = %s  （阴影线性尺度差 ~%s 倍）" %
      (mp.nstr(ratio_bc, 8), mp.nstr(ratio_bc, 6)))
print("")

# ---- EHT 观测对比 ----
G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
Msun = mp.mpf("1.98847e30")
rad2uas = mp.mpf(180) / mp.pi * 3600 * 1e6  # rad -> micro-arcsec

def shadow_diameter_uas(M_msun, D_m, bc_over_M):
    # 阴影角直径 = 2 * b_c / D = 2 * (bc/M) * G*M/c^2 / D
    return 2 * bc_over_M * G * M_msun * Msun / c ** 2 / D_m * rad2uas

targets = {
    "M87*": (mp.mpf("6.5e9"), mp.mpf("16.8") * mp.mpf("3.0856775814913673e22"), mp.mpf("42"), mp.mpf("3")),
    "Sgr A*": (mp.mpf("4.297e6"), mp.mpf("8.15") * mp.mpf("3.0856775814913673e19"), mp.mpf("51.8"), mp.mpf("2.3")),
}
print("=== B. EHT 阴影角直径：GR vs TUFT-C vs 观测 ===")
eht_rows = []
for name, (Mm, Dm, obs, obs_err) in targets.items():
    d_GR = shadow_diameter_uas(Mm, Dm, 3 * mp.sqrt(3))
    d_T = shadow_diameter_uas(Mm, Dm, mp.e)
    sig_GR = mp.fabs(d_GR - obs) / obs_err
    sig_T = mp.fabs(d_T - obs) / obs_err
    eht_rows.append({
        "目标": name, "观测阴影角直径(μas)": mp.nstr(obs, 5), "观测误差(μas)": mp.nstr(obs_err, 4),
        "GR预报(μas)": mp.nstr(d_GR, 8), "TUFT-C预报(μas)": mp.nstr(d_T, 8),
        "GR偏差(σ)": mp.nstr(sig_GR, 6), "TUFT-C偏差(σ)": mp.nstr(sig_T, 6),
    })
    print("[%s] 观测=%s±%s μas  | GR=%s (%sσ)  TUFT-C=%s (%sσ)" %
          (name, mp.nstr(obs, 5), mp.nstr(obs_err, 4), mp.nstr(d_GR, 6), mp.nstr(sig_GR, 5),
           mp.nstr(d_T, 6), mp.nstr(sig_T, 5)))
print("")

# ---- C. 强场光线偏折 / 中子星表面弯曲角 ----
print("=== C. 强场光线弯曲角（中子星表面掠射 -> 无穷远）===")

def bend_surface(f, x):
    # M=1, R=1/x, u0=x；掠射：b 使 u0 为最接近点
    u0 = x
    binv2 = f(u0)
    return mp.re(mp.quad(lambda u: 1 / mp.sqrt(binv2 - f(u)), [0, u0]))

ns_rows = []
for x in [mp.mpf("0.10"), mp.mpf("0.17"), mp.mpf("0.22"), mp.mpf("0.30")]:
    psi_GR = bend_surface(f_GR, x)
    psi_T = bend_surface(f_TUFT, x)
    dev = mp.fabs(psi_T - psi_GR) / psi_GR
    ns_rows.append({"x=GM/c^2R": mp.nstr(x, 4),
                    "弯曲角_GR(rad)": mp.nstr(psi_GR, 8),
                    "弯曲角_TUFT-C(rad)": mp.nstr(psi_T, 8),
                    "相对偏差": mp.nstr(dev, 6)})
    print("[x=%s] ψ_GR=%s rad  ψ_TUFT=%s rad  偏差=%s" %
          (mp.nstr(x, 4), mp.nstr(psi_GR, 8), mp.nstr(psi_T, 8), mp.nstr(dev, 6)))
print("")

conclusion = (
    "TUFT-C 外部指数度规无有限半径事件视界（g_00=e^{-2M/r} 全空间非零），其光子球在 r=M、"
    "临界冲击参数 b_c=M*e≈2.718M；而 GR 为 r=3M、b_c=3√3 M≈5.196M，两者差 1.912 倍。"
    "代入 EHT 实测 M87*/Sgr A* 的阴影角直径（GR 预报与观测在 1-2σ 内），TUFT-C 预报的阴影"
    "只有观测的一半左右 ⇒ 与 EHT 强烈冲突。这是 TUFT-C 外部解的直接、绕不开的强场证伪点，"
    "且不依赖 H7 内部度规。结论：TUFT-C 若声称描述强场引力/黑洞，已被 EHT 否证；"
    "若声明只适用弱场，则必须显式写下强场失效边界（r 下限），并放弃一切黑洞相关推论。"
)
print("结论:", conclusion)

out = {
    "A_光子球": {
        "GR": {"r_c/M": mp.nstr(1 / u_phot_GR, 8), "b_c/M": mp.nstr(b_c_GR, 10)},
        "TUFT-C": {"r_c/M": mp.nstr(1 / u_phot_T, 8), "b_c/M": mp.nstr(b_c_T, 10)},
        "b_c比值_GR/TUFT": mp.nstr(ratio_bc, 8),
    },
    "B_EHT阴影": eht_rows,
    "C_表面弯曲角": ns_rows,
    "结论": conclusion,
}
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TUFT_强场检验_黑洞阴影与光线偏折_结果.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("写出:", path)
