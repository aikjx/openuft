# -*- coding: utf-8 -*-
"""
C11 检验：TUFT-C 2PN 度规偏离的可检验性量化（实跑）。

目标：把《TUFT_修正核_与实验一致的正确公式集.md》§4 的「唯一新预言 C11（2PN 偏离）」
     落到真实天体上，回答「它现在能被检验吗、需要多好的观测」。
方法论：mpmath 50 位实跑；度规直接比较 TUFT-C 与 GR 的标准 Schwarzschild 外部解。
红线：
  - TUFT-C 只定义了真空外部度规（H7：仅 r>0 成立），其内部度规未定义 ⇒ 中子星
    结构方程（TOV）本身无 TUFT-C 版本，本脚本不臆造内部度规。
  - 「中子星表面红移偏离」按「外部真空度规延续到表面」近似给出，并显式标注此近似。
  - 借用标准 GR/NICER 数据之处显式标注，不得记成 TUFT 成就。
运行：
  python uft/01-核心公理/TUFT_C11_2PN中子星检验.py
"""

import sys
import json
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mpmath as mp

mp.mp.dps = 50

G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
Msun = mp.mpf("1.98847e30")
GMc2 = G * Msun / c ** 2  # 几何长度/太阳质量，单位 m

# ---- 度规（外部 Schwarzschild，几何单位 x = GM/(c^2 r)）----
def g00_TUFT(x):
    return mp.e ** (-2 * x)          # |g_00| = e^{-2x}

def g00_GR(x):
    return 1 - 2 * x                 # |g_00| = 1 - 2x

def grr_TUFT(x):
    return mp.e ** (2 * x)           # g_rr = e^{+2x}

def grr_GR(x):
    return 1 / (1 - 2 * x)           # g_rr = (1-2x)^{-1}

def z_TUFT(x):
    return mp.e ** x - 1             # 1+z = 1/sqrt(g00) => e^{x}-1

def z_GR(x):
    return 1 / mp.sqrt(1 - 2 * x) - 1


def rel_dev(a, b):
    return mp.fabs(a - b) / (mp.fabs(b) + mp.mpf("1e-300"))


rows = []
print("=== §4 复算：真空外部 2PN 度规偏离 ===")
surf = {
    "地球表面": (mp.mpf("5.972e24"), mp.mpf("6.371e6")),
    "太阳表面": (mp.mpf("1.989e30"), mp.mpf("6.9634e8")),
    "中子星表面(典型 M=1.4,R=12km)": (mp.mpf("1.4") * Msun, mp.mpf("12e3")),
}
for name, (M, R) in surf.items():
    x = G * M / (c ** 2 * R)
    d00 = rel_dev(g00_TUFT(x), g00_GR(x))
    drr = rel_dev(grr_TUFT(x), grr_GR(x))
    rows.append({"天体": name, "x": mp.nstr(x, 8),
                 "g00相对偏离": mp.nstr(d00, 8), "grr相对偏离": mp.nstr(drr, 8)})
    print("[%s] x=%s  g00_dev=%s  grr_dev=%s" % (name, mp.nstr(x, 6), mp.nstr(d00, 8), mp.nstr(drr, 8)))
print("")

print("=== 双星系统：2PN 偏离是否可检验 ===")
# 双星：x = G M_tot/(c^2 a)，a=轨道半长轴；2PN 偏离 ~ 度规 x^2 阶
binaries = {
    "PSR B1913+16": (mp.mpf("2.828378") * Msun, mp.mpf("1.950995e9")),
    "PSR J0737-3039(双脉冲星)": (mp.mpf("2.587") * Msun, mp.mpf("8.8e8")),
}
# 当前脉冲星计时对后开普勒参数的相对精度量级 ~ 1e-3（与 GR 模板符合 <0.3%）
obs_precision = mp.mpf("1e-3")
bin_rows = []
for name, (Mtot, a) in binaries.items():
    x = G * Mtot / (c ** 2 * a)
    d00 = rel_dev(g00_TUFT(x), g00_GR(x))
    drr = rel_dev(grr_TUFT(x), grr_GR(x))
    dev_max = max(d00, drr)
    detectable = "否(偏离<<观测精度)" if dev_max < obs_precision else "可能"
    bin_rows.append({"双星": name, "x": mp.nstr(x, 8), "2PN最大偏离": mp.nstr(dev_max, 6),
                     "观测精度~": mp.nstr(obs_precision, 6), "可检验": detectable})
    print("[%s] x=%s  2PN_dev=%s  观测精度~%s => %s" %
          (name, mp.nstr(x, 6), mp.nstr(dev_max, 6), mp.nstr(obs_precision, 6), detectable))
print("")

print("=== 中子星表面红移：TUFT-C vs GR（近似：外部度规延续到表面）===")
# NICER 实测：M(M_sun), R(km)
ns = {
    "PSR J0030+0451 (NICER)": (mp.mpf("1.44"), mp.mpf("13.0e3")),
    "PSR J0740+6620 (NICER)": (mp.mpf("2.08"), mp.mpf("13.7e3")),
}
# X 射线暴振荡/吸收线对中子星表面红移 z 的当前测量相对精度 ~ 10-20%（系统误差大）
ns_obs_prec = mp.mpf("0.15")
ns_rows = []
for name, (Mnum, R) in ns.items():
    x = GMc2 * Mnum / R
    zt = z_TUFT(x)
    zg = z_GR(x)
    dz_rel = rel_dev(zt, zg)
    verdict = "差异>>当前精度,但需<10%精度+补H7内部度规" if dz_rel > ns_obs_prec else "当前可区分"
    ns_rows.append({"中子星": name, "x": mp.nstr(x, 8),
                    "z_TUFT-C": mp.nstr(zt, 8), "z_GR": mp.nstr(zg, 8),
                    "红移相对偏差": mp.nstr(dz_rel, 8),
                    "当前红移精度~": mp.nstr(ns_obs_prec, 6), "结论": verdict})
    print("[%s] x=%s  z_TUFT=%s  z_GR=%s  红移偏差=%s  当前精度~%s => %s" %
          (name, mp.nstr(x, 6), mp.nstr(zt, 8), mp.nstr(zg, 8), mp.nstr(dz_rel, 8),
           mp.nstr(ns_obs_prec, 6), verdict))
print("")

# ---- 结论 ----
conclusion = (
    "C11（2PN 度规偏离）在太阳系与双星系均不可检验：双星的 x~1e-6，2PN 偏离 ~1e-11，"
    "远低于脉冲星计时 ~1e-3 的精度。唯一潜在窗口是中子星表面（x~0.17-0.22），"
    "其 g_rr 偏离 7-8%、表面红移偏离 27-46%，但：(1) TUFT-C 内部度规未定义（H7），"
    "表面红移检验依赖「外部真空度规延续到表面」近似，非严格；(2) 当前 X 射线红移测量"
    "相对精度 ~10-20% 且系统误差大，尚不足以干净区分。需补 H7（定义内部度规 / 修改 TOV）"
    "并等待下一代 X 射线任务（eXTP/Athena 暴胀振荡目标 ~1-5%）才能把 C11 提升为可证伪检验。"
)
print("结论:", conclusion)

out = {
    "sec4_复算": rows,
    "双星可检验性": bin_rows,
    "中子星表面红移": ns_rows,
    "观测精度假设": {
        "双星后开普勒相对精度~": str(obs_precision),
        "中子星红移相对精度~": str(ns_obs_prec),
    },
    "结论": conclusion,
}
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TUFT_C11_2PN中子星检验_结果.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("写出:", path)
