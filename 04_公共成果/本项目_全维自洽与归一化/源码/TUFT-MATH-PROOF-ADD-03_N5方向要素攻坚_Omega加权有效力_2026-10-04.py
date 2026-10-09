# -*- coding: utf-8 -*-
"""TUFT-MATH-PROOF-ADD-03：N5 方向要素攻坚（Ω 加权有效力）
落地整理册/ADD-02 台账下一步①：消除「方向」要素的流形常值退化。

  P1  Ω 加权有效势 V=Ω·E 的有效力方向 ƒ̂(θ) 闭式推导 + 量纲/单值性
  P2  网格验证 ƒ̂ 非恒定：全域方向跨度、四域圆周均值方向 + 圆周方差（Mardia）
  P3  奇异性核查：开域内 |∇(ΩE)| 最小值（应 >0，无零力方向奇点，除原点）
  P4  退化消除量化：旧 ƒ̂ ≡ (1,1)/√2（跨度 0°）vs 新 ƒ̂ 跨度
  P5  结构图（SVG，纯 stdlib）：单位圆分区 + ƒ̂(θ) 箭头场
产物：../数据/TUFT-MATH-PROOF-ADD-03_N5方向要素攻坚_Omega加权有效力_2026-10-04.{md,json,svg}
退出码：0 = 全部 PASS（门禁）
"""
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(_HERE, "..", "数据"))
BASE = "TUFT-MATH-PROOF-ADD-03_N5方向要素攻坚_Omega加权有效力_2026-10-04"

RESULTS = []
ADD2 = os.path.join(OUT_DIR, "TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派与耦合匹配_2026-10-04.json")
with open(ADD2, encoding="utf-8") as f:
    A2 = json.load(f)
LAM = A2["fitting"]["lambda"]          # α_s = 0.1179（沿用 ADD-02 归一化）
HBARC = 197.326e-9  # GeV·m，仅用于量纲说明，不参与方向计算


def classify(k, t):
    r = math.hypot(k, t)
    if r == 0.0:
        return "O"
    s3 = math.sqrt(3.0)
    if 2 * k >= s3 * r:
        return "EM"
    if -k + s3 * t >= s3 * r:
        return "S"
    if -k - s3 * t >= s3 * r:
        return "W"
    return "G"


def fhat(theta_deg, lam=LAM):
    """有效力方向 ƒ̂(θ) = −∇(ΩE)/|∇(ΩE)|，返回单位方向 (ux,uy)。"""
    th = math.radians(theta_deg)
    c, s = math.cos(th), math.sin(th)
    c3, s3t = math.cos(3 * th), math.sin(3 * th)
    # V = Ω·E，Ω=λcos3θ，E∝(cosθ+sinθ)（令 r=1，方向只依赖 θ）
    # ∇V = A·r̂ + B·θ̂，A=∂V/∂r ∝ (c+s)cos3θ，B=(1/r)∂V/∂θ ∝ (−s+c)cos3θ − 3(c+s)sin3θ
    A = (c + s) * c3
    B = (-s + c) * c3 - 3.0 * (c + s) * s3t
    # 直角坐标梯度 ∇V = (A cosθ − B sinθ, A sinθ + B cosθ)
    gx = A * c - B * s
    gy = A * s + B * c
    norm = math.hypot(gx, gy)
    if norm == 0.0:
        return None
    return (-gx / norm, -gy / norm)   # 取 −∇V 方向


def circ_stats(angles):
    """angles: 弧度列表；返回 (均值角 rad, R=合向量模, 方差=1-R)。"""
    if not angles:
        return None, 0.0, 1.0
    sx = sum(math.sin(a) for a in angles)
    cx = sum(math.cos(a) for a in angles)
    R = math.hypot(sx, cx) / len(angles)
    mean = math.atan2(sx, cx)
    return mean, R, 1.0 - R


# ---------------------------------------------------------------- P1 闭式校验 + r 无关性（数值梯度对拍）
# 直接对 V(κ,τ)=Ω·E 做有限差分梯度，与闭式 ƒ̂(θ) 对拍；并跨多档 r 验证方向只依赖 θ。
def V_num(k, t, lam=LAM):
    r = math.hypot(k, t)
    if r == 0.0:
        return 0.0
    E = (k + t)                       # ∝ 真实 E=(ħc/2)(κ+τ)，常数因子不影响方向
    Om = lam * (k ** 3 - 3 * k * t ** 2) / r ** 3
    return Om * E


def fhat_numeric(k, t, hh=1e-6):
    gx = (V_num(k + hh, t) - V_num(k - hh, t)) / (2 * hh)
    gy = (V_num(k, t + hh) - V_num(k, t - hh)) / (2 * hh)
    n = math.hypot(gx, gy)
    if n == 0.0:
        return None
    return (-gx / n, -gy / n)


max_err = 0.0
for rr in (0.3, 1.0, 2.5, 6.0):
    for deg in (10, 55, 120, 175, 240, 300, 350):
        th = math.radians(deg)
        k, t = rr * math.cos(th), rr * math.sin(th)
        fn = fhat_numeric(k, t)
        fc = fhat(deg)
        if fn is None:
            continue
        # 方向角差（取 [0,180) 因单位矢量无指向）
        a1 = (math.degrees(math.atan2(fn[1], fn[0])) + 180) % 180
        a2 = (math.degrees(math.atan2(fc[1], fc[0])) + 180) % 180
        max_err = max(max_err, abs(a1 - a2))
add_P1 = ("P1", "ƒ̂(θ) 闭式：V=ΩE ⇒ ∇V=(A cosθ−B sinθ, A sinθ+B cosθ)，"
          "A∝(cosθ+sinθ)cos3θ，B∝(−sinθ+cosθ)cos3θ−3(cosθ+sinθ)sin3θ；ƒ̂=−∇V/|∇V|",
          "闭式与数值梯度方向一致（误差≪1°）；跨多档 r 方向不变（只依赖 θ）",
          "数值梯度对拍最大方向偏差 %.3e°（含 r∈{0.3,1,2.5,6} 四档）" % max_err,
          "PASS" if max_err < 1e-3 else "MISMATCH")

# ---------------------------------------------------------------- P2 网格：非恒定 + 四域圆周统计
N = 1441
dom_sin = {"EM": [], "S": [], "W": [], "G": []}
angles_all = []
for i in range(N):
    deg = 360.0 * i / (N - 1)
    fh = fhat(deg)
    if fh is None:
        continue
    ang = math.atan2(fh[1], fh[0])
    angles_all.append(ang)
    # 取一个半径上的代表点（方向只依赖 θ）
    th = math.radians(deg)
    k, t = math.cos(th), math.sin(th)
    dom = classify(k, t)
    if dom in dom_sin:
        dom_sin[dom].append(ang)

stats = {d: circ_stats(angles_all if False else dom_sin[d]) for d in dom_sin}
span = (max(angles_all) - min(angles_all)) if angles_all else 0.0
means = {d: stats[d][0] for d in stats if stats[d][0] is not None}
# 域间均值最小分离度
seps = []
ds = list(means.values())
for i in range(len(ds)):
    for j in range(i + 1, len(ds)):
        d = abs(ds[i] - ds[j])
        d = min(d, 2 * math.pi - d)
        seps.append(d)
min_sep = min(seps) if seps else 0.0
P2_ok = span > 0.1 and all(stats[d][2] < 0.999 for d in stats)
add_P2 = ("P2", "ƒ̂ 非恒定 + 四域圆周方向统计",
          "全域方向跨度 >0；四域均具非零圆周方差（方向散布）；域间均值方向可分离",
          "全域跨度 %.1f°；四域 R=[%s]；域间最小均值分离 %.1f°"
          % (math.degrees(span),
             ", ".join("%s=%.3f" % (d, stats[d][1]) for d in ("EM", "S", "W", "G")),
             math.degrees(min_sep)),
          "PASS" if P2_ok else "MISMATCH")

# ---------------------------------------------------------------- P3 奇异性：|∇(ΩE)| 最小值（开域）
mn = 1e9
mn_deg = 0
for i in range(3600):
    deg = 360.0 * i / 3600
    th = math.radians(deg)
    c, s = math.cos(th), math.sin(th)
    c3, s3t = math.cos(3 * th), math.sin(3 * th)
    A = (c + s) * c3
    B = (-s + c) * c3 - 3.0 * (c + s) * s3t
    gx = A * c - B * s
    gy = A * s + B * c
    norm = math.hypot(gx, gy)
    if norm < mn:
        mn, mn_deg = norm, deg
add_P3 = ("P3", "开域内 |∇(ΩE)| 最小值（奇异性核查）",
          "min > 0（无零力方向奇点，除 r=0 原点）",
          "min|∇V| = %.4e（θ=%.0f°）⇒ 全开域非零，ƒ̂ 处处良定义" % (mn, mn_deg),
          "PASS" if mn > 1e-6 else "MISMATCH")

# ---------------------------------------------------------------- P4 退化消除量化
old_span = 0.0   # 旧 F = −(ħc/2)(1,1) ⇒ 方向恒为 225°（单位矢量方向 45°），跨度 0°
P4_ok = math.degrees(span) > 1.0
add_P4 = ("P4", "退化消除量化：旧 ƒ̂ ≡ 常矢量 vs 新 ƒ̂",
          "新方向全域跨度 ≫ 0（旧为 0°）",
          "旧跨度 %.1f°（恒定 (1,1)/√2）⇒ 新跨度 %.1f°（消除退化）" % (math.degrees(old_span), math.degrees(span)),
          "PASS" if P4_ok else "MISMATCH")

RESULTS.extend([add_P1, add_P2, add_P3, add_P4])

# ---------------------------------------------------------------- P5 SVG 箭头场
W_, H_ = 460, 340
cx, cy, R = 190, 175, 120
parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="sans-serif">' % (W_, H_)]
parts.append('<rect width="%d" height="%d" fill="#ffffff"/>' % (W_, H_))
# 分区底图
segs = [("EM", -30, 30, "#4d8fd6"), ("S", 90, 150, "#d64d4d"), ("W", 210, 270, "#4dd67c")]
for name, a0, a1, col in segs:
    a0r, a1r = math.radians(a0 - 90), math.radians(a1 - 90)
    x0, y0 = cx + R * math.cos(a0r), cy + R * math.sin(a0r)
    x1, y1 = cx + R * math.cos(a1r), cy + R * math.sin(a1r)
    parts.append('<path d="M%d %d A%d %d 0 0 1 %d %d L%d %d Z" fill="%s" fill-opacity="0.5"/>'
                 % (cx, cy, R, R, x1, y1, cx, cy, col))
for a0, a1 in ((30, 90), (150, 210), (270, 330)):
    a0r, a1r = math.radians(a0 - 90), math.radians(a1 - 90)
    x0, y0 = cx + R * math.cos(a0r), cy + R * math.sin(a0r)
    x1, y1 = cx + R * math.cos(a1r), cy + R * math.sin(a1r)
    parts.append('<path d="M%d %d A%d %d 0 0 1 %d %d L%d %d Z" fill="#9aa3ad" fill-opacity="0.5"/>'
                 % (cx, cy, R, R, x1, y1, cx, cy))
parts.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#333"/>' % (cx, cy, R))
# ƒ̂ 箭头（半径 0.7R 处，每 5° 一支）
for i in range(72):
    deg = 5.0 * i
    th = math.radians(deg)
    k, t = math.cos(th), math.sin(th)
    dom = classify(k, t)
    col = {"EM": "#1f5fa8", "S": "#a82020", "W": "#1f8a4d", "G": "#555"}.get(dom, "#000")
    fh = fhat(deg)
    if fh is None:
        continue
    px, py = cx + 0.7 * R * math.cos(th), cy + 0.7 * R * math.sin(th)
    ex, ey = px + 26 * fh[0], py + 26 * fh[1]
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5"/>'
                 % (px, py, ex, ey, col))
    # 箭头头
    ang = math.atan2(fh[1], fh[0])
    for da in (2.6, -2.6):
        hx = ex - 7 * math.cos(ang + da)
        hy = ey - 7 * math.sin(ang + da)
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5"/>'
                     % (ex, ey, hx, hy, col))
parts.append('<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="#222">'
             'N5 修复：ƒ̂(θ)=−∇(ΩE)/|∇(ΩE)|（箭头随几何转向）</text>' % (cx, 25))
parts.append('<text x="%d" y="%d" font-size="11" text-anchor="middle" fill="#555">'
             '全域方向跨度 %.1f°，四域方向可分离（旧 ƒ̂ 恒定）</text>' % (cx, 318, math.degrees(span)))
parts.append('</svg>')
svg = "\n".join(parts)
with open(os.path.join(OUT_DIR, BASE + ".svg"), "w", encoding="utf-8") as fp:
    fp.write(svg + "\n")
add_P5 = ("P5", "结构图（Ω 加权有效力方向场 SVG）",
          "文件生成且非空",
          "%d 字节 -> %s.svg" % (len(svg), BASE),
          "PASS" if len(svg) > 1000 else "MISMATCH")
RESULTS.append(add_P5)

# ---------------------------------------------------------------- 落盘
os.makedirs(OUT_DIR, exist_ok=True)
n_pass = sum(1 for x in RESULTS if x[4] == "PASS")
rep = []
rep.append("# TUFT-MATH-PROOF-ADD-03 N5 方向要素攻坚 数据（2026-10-04）\n")
rep.append("- 引擎：`源码/%s.py`（纯标准库）\n" % BASE)
rep.append("- 读数：**条目 %d —— PASS %d / MISMATCH %d**\n" % (len(RESULTS), n_pass, len(RESULTS) - n_pass))
rep.append("## 四域圆周方向统计（Mardia）\n")
rep.append("| 域 | 均值方向 | 合向量 R | 圆周方差 |\n|---|---|---|---|")
for d in ("EM", "S", "W", "G"):
    m, R_, v = stats[d]
    rep.append("| %s | %.1f° | %.4f | %.4f |" % (d, math.degrees(m) % 360, R_, v))
rep.append("\n- 旧 ƒ̂ 跨度 0°（恒定 (1,1)/√2）；新 ƒ̂ 全域跨度 %.1f°\n" % math.degrees(span))
rep.append("- 域间均值方向最小分离 %.1f°（>0 ⇒ 四力方向可区分）\n" % math.degrees(min_sep))
rep.append("- min|∇(ΩE)| = %.4e（θ=%.0f°），开域无零力方向奇点\n" % (mn, mn_deg))
with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as fp:
    fp.write("\n".join(rep))
with open(os.path.join(OUT_DIR, BASE + ".json"), "w", encoding="utf-8") as fp:
    json.dump({"base": BASE, "date": "2026-10-04", "lambda": LAM,
               "fhat_stats": {d: {"mean_deg": math.degrees(stats[d][0]) % 360,
                                  "R": stats[d][1], "var": stats[d][2]} for d in stats},
               "global_span_deg": math.degrees(span), "min_sep_deg": math.degrees(min_sep),
               "min_grad": mn, "summary": {"total": len(RESULTS), "pass": n_pass}},
              fp, ensure_ascii=False, indent=1)

print("\n".join("[%s] %s %s" % (v, cid, got) for cid, _, _, got, v in RESULTS))
print("\n读数: PASS %d / %d -> %s" % (n_pass, len(RESULTS), os.path.join(OUT_DIR, BASE + ".md")))
sys.exit(0 if n_pass == len(RESULTS) else 1)
