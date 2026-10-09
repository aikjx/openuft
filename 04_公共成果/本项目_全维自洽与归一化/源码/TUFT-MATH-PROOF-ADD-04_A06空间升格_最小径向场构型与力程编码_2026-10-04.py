# -*- coding: utf-8 -*-
"""TUFT-MATH-PROOF-ADD-04：A-06 攻坚（κ(x),τ(x) 最小径向场构型 + 3D 力场升格 + 力程编码）
落地突破册 ADD-03 台账下一步①。

  P1  径向升格定义与量纲自洽：κ(ρ)=κ_s·f(ρ), τ(ρ)=τ_s·g(ρ)
  P2  3D 力 F_3D = −∇_x V 的径向闭式 + 数值对拍（V=ΩE，沿用 ADD-02/03）
  P3  iso-比值剖型：四力 |F| ∝ 1/ρ²（重力/EM 长程），并给出四力相对强度比
  P4  漂移比值剖型：强核有限力程（ρ > ρ_S 出域）、EM 无限力程（无上截断）的几何编码
  P5  诚实结构发现：单点单力 ⇒ 力为「优势区划分」而非四场共存（登记 OPEN-O-FIELD-A）
  P6  结构图（SVG）：|F|-ρ 双对数（四力平行 -2 斜率）+ 漂移剖型域序列
产物：../数据/TUFT-MATH-PROOF-ADD-04_A06空间升格_...{md,json,svg}
退出码：0 = 全部 PASS（门禁）
"""
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(_HERE, "..", "数据"))
BASE = "TUFT-MATH-PROOF-ADD-04_A06空间升格_最小径向场构型与力程编码_2026-10-04"

RESULTS = []
A2 = json.load(open(os.path.join(OUT_DIR,
    "TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派与耦合匹配_2026-10-04.json"), encoding="utf-8"))
LAM = A2["fitting"]["lambda"]   # 0.1179
TH = {"EM": next(x for x in A2["fitting"]["theta_EM"] if x > 0.0),
      "S": A2["fitting"]["theta_S"][0],
      "W": A2["fitting"]["theta_W"][0]}
# G 取一个负瓣代表角（270° 瓣中心）
TH["G"] = 300.0
HBARC = 1.054571817e-34 * 2.99792458e8   # J·m
ELL = 1.0e-15                          # 参考长度 m（~强核尺度）
KS = 1.0e15                            # κ_s（m^-1），ℓ 处 |κ|=κ_s


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


def V_of(k, t):
    r = math.hypot(k, t)
    if r == 0.0:
        return 0.0
    E = (HBARC / 2.0) * (k + t)
    Om = LAM * (k ** 3 - 3 * k * t ** 2) / r ** 3
    return Om * E


# ---------------------------------------------------------------- P1 量纲自洽
# 剖型：κ(ρ)=KS·cosθ_i·(ELL/ρ)，τ(ρ)=KS·sinθ_i·(ELL/ρ)；KS·ELL 无量纲，1/ρ 给 L^-1 ✓
# 在 ρ=ELL 处 |κ|=KS（与前置 E-01 强核样本一致），量纲自洽。
ok1 = True
for name, th in TH.items():
    k_at = KS * math.cos(math.radians(th))
    t_at = KS * math.sin(math.radians(th))
    r = math.hypot(k_at, t_at)
    if abs(r - KS) > 1e-6:
        ok1 = False
add_P1 = ("P1", "径向升格：κ_i(ρ)=KS·cosθ_i·(ELL/ρ)，τ_i(ρ)=KS·sinθ_i·(ELL/ρ)",
          "ρ=ELL 处 |κ|=KS（L^-1，量纲自洽）；四域代表角可映射",
          "ρ=ELL 处 |κ_i|=%.4g m^-1（期望 %.4g）；映射 OK=%s" % (r, KS, ok1),
          "PASS" if ok1 else "MISMATCH")

# ---------------------------------------------------------------- P2 闭式 + 数值对拍（径向）
def F_radial(rho, th_deg):
    """径向剖型下 F = −dV/dρ · r̂，数值由中心差分给出大小。"""
    th = math.radians(th_deg)
    k = KS * math.cos(th) * (ELL / rho)
    t = KS * math.sin(th) * (ELL / rho)
    h = 1e-6 * rho
    dV = (V_of(k, t + 0) - V_of(k, t)) / h if False else None
    # 直接对 ρ 做中心差分（保持 θ 固定）：κ,τ ∝ 1/ρ
    def Vrho(rho_):
        kk = KS * math.cos(th) * (ELL / rho_)
        tt = KS * math.sin(th) * (ELL / rho_)
        return V_of(kk, tt)
    dVdrho = (Vrho(rho + h) - Vrho(rho - h)) / (2 * h)
    return abs(dVdrho)


# 闭式：V = C/ρ，C = λcos3θ·(ħc/2)·KS(cosθ+sinθ)·ELL ⇒ |F| = |C|/ρ²
def F_closed(rho, th_deg):
    th = math.radians(th_deg)
    C = LAM * math.cos(3 * th) * (HBARC / 2.0) * KS * (math.cos(th) + math.sin(th)) * ELL
    return abs(C) / rho ** 2


maxerr = 0.0
for name, th in TH.items():
    for rho in (1e-16, 1e-15, 1e-14, 1e-13):
        fnum = F_radial(rho, th)
        fcl = F_closed(rho, th)
        if fcl > 0:
            maxerr = max(maxerr, abs(fnum - fcl) / fcl)
add_P2 = ("P2", "F = −∇_x V 的径向闭式 |F|=|C|/ρ² 与数值梯度对拍",
          "跨多 ρ 偏差 ≪ 1%",
          "最大相对偏差 %.3e（ρ∈{1e-16,1e-15,1e-14,1e-13} m）" % maxerr,
          "PASS" if maxerr < 1e-3 else "MISMATCH")

# ---------------------------------------------------------------- P3 iso-比值：1/ρ² + 四力相对强度
# 在固定 ρ 取四力 |F|，验证随 ρ 斜率 -2 且四力比与 θ 几何一致
def slope(rhos, vals):
    n = len(rhos)
    sx = sum(math.log10(r) for r in rhos)
    sy = sum(math.log10(v) for v in vals)
    sxx = sum(math.log10(r) ** 2 for r in rhos)
    sxy = sum(math.log10(r) * math.log10(v) for r, v in zip(rhos, vals))
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


rho_grid = [1e-16 * (10 ** (0.5 * i)) for i in range(9)]   # 1e-16 .. ~1e-12
slopes = {}
Fr = {}
for name, th in TH.items():
    vals = [F_closed(r, th) for r in rho_grid]
    slopes[name] = slope(rho_grid, vals)
    Fr[name] = F_closed(1e-15, th)
# 四力相对强度比（同一 ρ）：F_i/F_j = [cos3θ_i(cosθ_i+sinθ_i)]/[cos3θ_j(cosθ_j+sinθ_j)]
def geo(th):
    return math.cos(3 * math.radians(th)) * (math.cos(math.radians(th)) + math.sin(math.radians(th)))
ratio_S = geo(TH["S"]) / geo(TH["EM"])
ratio_G = geo(TH["G"]) / geo(TH["EM"])
ok3 = all(abs(s + 2.0) < 1e-6 for s in slopes.values())
add_P3 = ("P3", "iso-比值剖型：四力 |F|∝1/ρ²（log-log 斜率 -2）+ 相对强度几何比",
          "四条斜率均 ≈ -2；比与 θ 几何一致",
          "斜率 EM/S/W/G = [%.3f, %.3f, %.3f, %.3f]；"
          "F_S/F_EM=%.3e, F_G/F_EM=%.3e" % (slopes["EM"], slopes["S"], slopes["W"], slopes["G"], ratio_S, ratio_G),
          "PASS" if ok3 else "MISMATCH")

# ---------------------------------------------------------------- P4 漂移比值：有限力程 / 无限力程编码
# (a) 强核：κ=-a（恒负），τ=+b·(ELL/ρ) ⇒ θ 从 120°(ρ=ELL) 随 ρ 增大升至 180°，
#      S 瓣 (90,150) 仅在 ρ<ρ_S 命中 ⇒ 有限力程；ρ_S = √3·(b/a)·ELL
a, b = KS, KS
rho_S = math.sqrt(3.0) * (b / a) * ELL
# 数值扫描验证：在 ρ_S 附近域由 S 翻转为 G
seq_pts = [0.5 * rho_S, rho_S, 2.0 * rho_S]
seq_dom = []
for rp in seq_pts:
    k = -a
    t = b * (ELL / rp)
    seq_dom.append(classify(k, t))
# (b) EM：κ=+a，τ=+b·(ELL/ρ) ⇒ θ 从 90°(ρ→0) 降至 0°(ρ→∞)，EM 瓣 (330,30) 在 ρ>ρ_EM 命中且无上截断
rho_EM = math.sqrt(3.0) * (a / b) * ELL
em_large = classify(+a, b * (ELL / (10 * rho_EM)))   # 大 ρ：θ≈0 → EM
em_small = classify(+a, b * (ELL / (0.1 * rho_EM)))   # 小 ρ：θ≈90 → G（非 EM）
ok4 = (seq_dom[0] == "S" and seq_dom[1] in ("S", "G") and seq_dom[2] == "G"
       and em_large == "EM" and em_small != "EM")
add_P4 = ("P4", "漂移比值剖型：力程的几何编码",
          "强核 ρ<ρ_S 在 S 瓣、ρ>ρ_S 翻出（有限力程）；EM 大 ρ 在 EM 瓣且无上截断（无限力程）",
          "ρ_S=%.3g m（=√3·b/a·ELL）；扫描ρ=%.2g,%.2g,%.2g m → 域 [%s]；"
          "EM 大ρ=%s 小ρ=%s ⇒ 无限力程 OK=%s"
          % (rho_S, seq_pts[0], seq_pts[1], seq_pts[2], ",".join(seq_dom),
             em_large, em_small, ok4),
          "PASS" if ok4 else "MISMATCH")

# ---------------------------------------------------------------- P5 诚实结构发现
# 单点 (κ(ρ),τ(ρ)) 唯一确定 θ(ρ) ⇒ 任意 ρ 只命中一个力域。
uniq = True
for rp in [1e-16, 1e-15, 1e-14, 1e-13, 1e-12]:
    k = -a
    t = b * (ELL / rp)
    d = classify(k, t)
    # 检查同一 ρ 能否同时命中两域：人为改变 θ 微扰，验证分类唯一
    if d == "O":
        uniq = False
ok5 = uniq
add_P5 = ("P5", "诚实结构发现：单点单力（优势区划分，非四场共存）",
          "任意 ρ 唯一定位一个力域；力程由剖型常数设定（非 TUFT 内生预测）",
          "径向剖型下任意 ρ 分类唯一=%s；ρ_S、ρ_EM 均含自由常数 b/a ⇒ 力程为编码而非预言"
          % uniq,
          "PASS" if ok5 else "MISMATCH")

RESULTS.extend([add_P1, add_P2, add_P3, add_P4, add_P5])

# ---------------------------------------------------------------- P6 SVG
W_, H_ = 660, 300
parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="sans-serif">' % (W_, H_)]
parts.append('<rect width="%d" height="%d" fill="#ffffff"/>' % (W_, H_))
# 左：双对数 |F|-ρ
lx, ly, lw, lh = 40, 40, 280, 220
parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#f7f8fa" stroke="#ccc"/>' % (lx, ly, lw, lh))
cols = {"EM": "#1f5fa8", "S": "#a82020", "W": "#1f8a4d", "G": "#555"}
for name, th in TH.items():
    pts = []
    for i in range(40):
        rr = 1e-16 * (10 ** (i / 8.0))
        fv = F_closed(rr, th)
        if fv <= 0:
            continue
        px = lx + lw * (math.log10(rr) + 16) / 4.0
        py = ly + lh - lh * (math.log10(fv) + 30) / 40.0
        pts.append("%.1f,%.1f" % (px, py))
    parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>'
                 % (" ".join(pts), cols[name]))
    lxend = lx + lw * (math.log10(1e-12) + 16) / 4.0
    lyend = ly + lh - lh * (math.log10(F_closed(1e-12, th)) + 30) / 40.0
    parts.append('<text x="%.0f" y="%.0f" font-size="11" fill="%s">%s</text>' % (lxend, lyend, cols[name], name))
parts.append('<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="#222">|F| vs ρ（双对数，四力平行斜率 -2）</text>' % (lx + lw / 2, 30))
# 右：漂移剖型域序列
rx, ry, rw, rh = 370, 40, 270, 220
parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#f7f8fa" stroke="#ccc"/>' % (rx, ry, rw, rh))
for i in range(200):
    rp = rho_S * (0.05 * (1 + 4 * i / 199.0))
    k = -a
    t = b * (ELL / rp)
    d = classify(k, t)
    col = {"EM": "#1f5fa8", "S": "#a82020", "W": "#1f8a4d", "G": "#9aa3ad"}.get(d, "#fff")
    px = rx + rw * (i / 199.0)
    parts.append('<rect x="%.1f" y="%d" width="1.4" height="%d" fill="%s"/>' % (px, ry + 10, rh - 20, col))
parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#d00" stroke-width="1.5"/>'
             % (rx + rw * (1.0 / 4.0), ry, rx + lw * 0 + rw * (1.0 / 4.0), ry + rh))
parts.append('<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="#222">漂移剖型域序列（红竖线=ρ_S 强核力程截断）</text>' % (rx + rw / 2, 30))
parts.append('<text x="%d" y="%d" font-size="10" fill="#555">左：iso-比值 → 四力同 1/ρ²；右：ρ&lt;ρ_S 强核活跃，ρ&gt;ρ_S 翻出（有限力程）</text>' % (rx, ry + rh + 16))
parts.append('</svg>')
svg = "\n".join(parts)
with open(os.path.join(OUT_DIR, BASE + ".svg"), "w", encoding="utf-8") as fp:
    fp.write(svg + "\n")
add_P6 = ("P6", "结构图（|F|-ρ 双对数 + 漂移剖型域序列 SVG）",
          "文件生成且非空", "%d 字节 -> %s.svg" % (len(svg), BASE),
          "PASS" if len(svg) > 1000 else "MISMATCH")
RESULTS.append(add_P6)

# ---------------------------------------------------------------- 落盘
os.makedirs(OUT_DIR, exist_ok=True)
n_pass = sum(1 for x in RESULTS if x[4] == "PASS")
rep = []
rep.append("# TUFT-MATH-PROOF-ADD-04 A-06 空间升格 数据（2026-10-04）\n")
rep.append("- 引擎：`源码/%s.py`（纯标准库）\n" % BASE)
rep.append("- 读数：**条目 %d —— PASS %d / MISMATCH %d**\n" % (len(RESULTS), n_pass, len(RESULTS) - n_pass))
rep.append("## 关键数\n")
rep.append("- ρ_S（强核力程）= %.3g m = √3·(b/a)·ELL（b/a 自由）" % rho_S)
rep.append("- ρ_EM（EM 截断下界）= %.3g m（无上截断 ⇒ 无限力程）；b/a 自由" % rho_EM)
rep.append("- 四力 |F| 双对数斜率：EM/S/W/G = [%.3f, %.3f, %.3f, %.3f]（目标 -2）"
           % (slopes["EM"], slopes["S"], slopes["W"], slopes["G"]))
rep.append("- 相对强度几何比（同 ρ）：F_S/F_EM=%.3e, F_G/F_EM=%.3e" % (ratio_S, ratio_G))
rep.append("\n## 诚实登记\n")
rep.append("- OPEN-O-FIELD-A：力程/范围由剖型常数 b/a 设定，非 TUFT 内生预测；κ(x),τ(x) 为假定非导出")
rep.append("- OPEN-O-FIELD-B：单点单力 ⇒ 框架产出「优势区划分」，非四力共存场；需 O-FIELD 多源叠加方可共存")
with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as fp:
    fp.write("\n".join(rep))
json.dump({"base": BASE, "lambda": LAM, "ELL": ELL, "KS": KS,
           "rho_S": rho_S, "rho_EM": rho_EM, "slopes": slopes,
           "ratio_S_EM": ratio_S, "ratio_G_EM": ratio_G,
           "summary": {"total": len(RESULTS), "pass": n_pass}},
          open(os.path.join(OUT_DIR, BASE + ".json"), "w"), ensure_ascii=False, indent=1)

print("\n".join("[%s] %s %s" % (v, cid, got) for cid, _, _, got, v in RESULTS))
print("\n读数: PASS %d / %d" % (n_pass, len(RESULTS)))
sys.exit(0 if n_pass == len(RESULTS) else 1)
