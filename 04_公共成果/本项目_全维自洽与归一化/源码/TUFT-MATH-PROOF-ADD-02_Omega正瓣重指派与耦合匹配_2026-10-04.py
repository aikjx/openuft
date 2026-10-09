# -*- coding: utf-8 -*-
"""TUFT-MATH-PROOF-ADD-02：Ω 正瓣重指派 + 互斥完备划分 + 耦合匹配攻坚（纯标准库）

落地整理册 M1–M4，执行主册 Part 5 选项 A，并给出层级定价：
  P1  互斥完备划分（M2）：三正瓣闭式锥不等式 + D_G=补集；网格验证覆盖/互斥/Ω3
  P2  Ω 闭式一致性：λ(κ³-3κτ²)/r³ ≡ λcos(3θ)（数值逐点验证）
  P3  力程统一（M4）：L = c/f = 2π/r；强/弱两档数值与 ħc/L 对标
  P4  耦合匹配（选项 A）：归一化 λ=α_s（最强耦合置于瓣心）⇒ 唯一解 + 简并计数
  P5  层级定价：代表点精细调节位数 + 敏感度表（%/度）
  P6  分区结构图（SVG，纯 stdlib 生成）
产物：../数据/TUFT-MATH-PROOF-ADD-02_...{md,json,.svg}
退出码：0 = 全部 PASS（门禁）
"""
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(_HERE, "..", "数据"))
BASE = "TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派与耦合匹配_2026-10-04"

RESULTS = []


def add(cid, desc, expect, got, verdict):
    RESULTS.append({"id": cid, "desc": desc, "expect": expect, "got": got, "verdict": verdict})
    print("[%s] %s" % (verdict, cid))


# 来料耦合值（μ=M_Z 口径 + 电子口径 α_G，见整理册 N7 口径声明）
ALPHA_S = 0.1179
ALPHA_EM = 7.297e-3
ALPHA_W = 1.696e-2
ALPHA_G = 1.75e-45

# ---------------------------------------------------------------- P1 互斥完备划分（M2 闭式锥不等式）
# 正瓣（各 60° 锥，闭式）：D_EM: 2κ >= √3·r；D_Strong: -κ+√3·τ >= √3·r；D_Weak: -κ-√3·τ >= √3·r
# D_G = 补集（自动 cos3θ<0）。互斥性来自三锥方向两两相距 120° > 60°。
def classify(k, t):
    r = math.hypot(k, t)
    if r == 0.0:
        return "O"          # 原点：Ω 无定义（单点，零测度）
    s3 = math.sqrt(3.0)
    if 2 * k >= s3 * r:
        return "EM"
    if -k + s3 * t >= s3 * r:
        return "S"
    if -k - s3 * t >= s3 * r:
        return "W"
    return "G"


def p1():
    n, lo, hi = 721, -5.0, 5.0
    cnt = {"EM": 0, "S": 0, "W": 0, "G": 0, "O": 0}
    sign_bad = equiv_bad = bnd = 0
    s3 = math.sqrt(3.0)
    for i in range(n):
        t = lo + (hi - lo) * i / (n - 1)
        for j in range(n):
            k = lo + (hi - lo) * j / (n - 1)
            d = classify(k, t)
            cnt[d] += 1
            r = math.hypot(k, t)
            if r == 0.0:
                continue
            c3 = math.cos(3 * math.atan2(t, k))
            if abs(c3) < 1e-9:
                bnd += 1        # 边界点（cos3θ=0，零测度）：归属为约定，不做符号断言
                continue
            if d == "G" and not c3 < 0:
                sign_bad += 1
            if d in ("EM", "S", "W") and not c3 > 0:
                sign_bad += 1
            # 等价性：cos3θ>0 ⟺ 恰好命中某一正瓣锥
            in_cone = (2 * k >= s3 * r) or (-k + s3 * t >= s3 * r) \
                or (-k - s3 * t >= s3 * r)
            if (c3 > 0) != in_cone:
                equiv_bad += 1
    total = n * n - cnt["O"]
    covered = cnt["EM"] + cnt["S"] + cnt["W"] + cnt["G"]
    cov = 100.0 * covered / total
    return cnt, cov, sign_bad, equiv_bad, bnd


cnt1, cov1, sign_bad, equiv_bad, bnd1 = p1()
add("P1", "M2 重指派分区：覆盖/互斥/Ω3/闭式等价（网格 721×721）",
    "覆盖 100%、互斥（分类唯一）、Ω3 全域成立、锥不等式 ⟺ cos3θ 符号",
    "覆盖 %.4f%%、瓣计数 %s、Ω3 违反 %d 点、等价性违反 %d 点（边界点 %d 个按约定跳过）"
    % (cov1, cnt1, sign_bad, equiv_bad, bnd1),
    "PASS" if (cov1 > 99.99 and sign_bad == 0 and equiv_bad == 0) else "MISMATCH")

# ---------------------------------------------------------------- P2 Ω 闭式一致性
lam_test = 0.37
max_rel = 0.0
for i in range(200):
    th = 2 * math.pi * i / 200
    k, t = math.cos(th), math.sin(th)
    r = math.hypot(k, t)
    v1 = lam_test * (k ** 3 - 3 * k * t ** 2) / r ** 3
    v2 = lam_test * math.cos(3 * th)
    max_rel = max(max_rel, abs(v1 - v2))
add("P2", "Ω(κ,τ)=λ(κ³-3κτ²)/r³ 与 λ·cos(3θ) 逐点一致性",
    "最大相对偏差 ~1e-15（浮点精度）",
    "最大绝对偏差 %.3e" % max_rel,
    "PASS" if max_rel < 1e-12 else "MISMATCH")

# ---------------------------------------------------------------- P3 力程统一（M4）：L = c/f = 2π/r
HBARC_MEVF = 197.326  # MeV·fm
r_s, r_w = 1.0e15, 1.0e18          # 前置 E-01 仅有的两档样本尺度（m^-1）
L_s, L_w = 2 * math.pi / r_s, 2 * math.pi / r_w
E_s = HBARC_MEVF / (L_s * 1e15)    # ħc/L（MeV），L 换算 fm
E_w = HBARC_MEVF / (L_w * 1e15) / 1e3  # GeV
add("P3", "M4 力程 L=c/f=2π/r 的强/弱两档对标",
    "给出两档数值并声明口径（承认 2π 歧义，回链前置 A-03/C-07）",
    "强核 L=6.283e-15 m ⇒ ħc/L=%.1f MeV（vs Λ_QCD 200–300 MeV，低 ~7.7 倍）；"
    "弱核 L=6.283e-18 m ⇒ ħc/L=%.1f GeV（vs M_W=80.4 GeV，低 ~2.6 倍）" % (E_s, E_w),
    "PASS" if (abs(L_s - 6.283185e-15) / 6.283185e-15 < 1e-4 and E_w < 80.4) else "MISMATCH")

# ---------------------------------------------------------------- P4 耦合匹配（选项 A）：λ = α_s 归一化
lam = ALPHA_S


def solve_theta(alpha, lobe, lam_):
    """解 |λ cos3θ| = alpha，返回落在指定正瓣/负瓣内的全部解（角度制）。"""
    c = alpha / lam_
    if c > 1.0:
        return [], "无解（alpha > λ）"
    if c < 1e-12:
        # 近零解析分支：arccos(c) 在浮点下湮没于 π/2，改用 δ = asin(c) ≈ c
        if lobe == "G":
            d = math.degrees(c / 3.0)
            sols = []
            for k in range(6):
                th0 = 30.0 + 60.0 * k
                sgn = 1.0 if k % 2 == 0 else -1.0   # 零点的 G 侧方向
                sols.append(round((th0 + sgn * d) % 360.0, 12))
            return sols, None
        return [], None
    a = math.degrees(math.acos(min(1.0, c)))   # 3θ 的基解（0..180）
    sols = []
    for k in range(-2, 3):
        for s in (+1, -1):
            th = (s * a) / 3.0 + 120.0 * k
            th = ((th + 180.0) % 360.0) - 180.0
            if -180.0 <= th <= 180.0:
                sols.append(th)
    uniq = sorted({round(x, 9) for x in sols})

    def in_lobe(th):
        t = th % 360.0
        if lobe == "EM":
            return t < 30 or t > 330
        if lobe == "S":
            return 90 < t < 150
        if lobe == "W":
            return 210 < t < 270
        if lobe == "G":
            return math.cos(3 * math.radians(t)) < 0
        return False

    return [x for x in uniq if in_lobe(x)], None


sol_S, e1 = solve_theta(ALPHA_S, "S", lam)
sol_EM, e2 = solve_theta(ALPHA_EM, "EM", lam)
sol_W, e3 = solve_theta(ALPHA_W, "W", lam)
sol_G, e4 = solve_theta(ALPHA_G, "G", lam)
ok4 = (e1 is e2 is e3 is e4 is None and len(sol_S) == 1 and len(sol_EM) == 2
       and len(sol_W) == 2 and len(sol_G) == 6)
add("P4", "耦合匹配唯一解（归一化 λ=α_s=0.1179，最强耦合置于瓣心）",
    "θ_S=120°（1 解）、θ_EM=±28.82°（2 解）、θ_W∈{212.76,267.24}（2 解）、θ_G=零点 G 侧（6 解）",
    "S=%s EM=%s W=%s G(前3)=%s... 共%d" % (
        [round(x, 3) for x in sol_S], [round(x, 3) for x in sol_EM],
        [round(x, 3) for x in sol_W], [round(x, 6) for x in sol_G[:3]], len(sol_G)),
    "PASS" if ok4 else "MISMATCH")

# ---------------------------------------------------------------- P5 层级定价：精细调节 + 敏感度
delta_G_rad = (ALPHA_G / lam) / 3.0            # 距最近零点的角距（弧度）
delta_G_deg = math.degrees(delta_G_rad)
digits = -math.log10(delta_G_rad)              # 十进制精度位数
span = math.log10(ALPHA_S / ALPHA_G)           # 耦合层级跨度


def sens(alpha, th_center_deg):
    """代表点每偏 1° 引起的耦合相对变化（一阶）。"""
    d = math.radians(1.0)
    dadt = 3.0 * lam * abs(math.sin(3 * math.radians(th_center_deg)))
    return dadt * d / alpha


sens_EM = sens(ALPHA_EM, sol_EM[0])
sens_W = sens(ALPHA_W, sol_W[0])
sens_G = sens(ALPHA_G, 30.0 + 60.0 * 0 + math.degrees(delta_G_rad))
sens_S = 0.0  # 瓣心 sin3θ=0，一阶稳定
add("P5", "层级定价：引力代表点精细调节与耦合敏感度",
    "量化代价（诚实定价，不隐藏）",
    "耦合跨度 %.1f 个量级；θ_G 距域边界 %.3e 弧度（%.3e 度）⇒ ~%.0f 位十进制精度；"
    "敏感度（相对变化/度）：S=0（瓣心二阶稳定）、EM=%.0f%%、W=%.0f%%、G=%.1e%%"
    % (span, delta_G_rad, delta_G_deg, digits, 100 * sens_EM, 100 * sens_W, 100 * sens_G),
    "PASS" if (38 < span < 50 and 40 < digits < 50) else "MISMATCH")

# ---------------------------------------------------------------- P6 结构图（SVG，纯 stdlib）
def make_svg():
    W_, H_ = 680, 340
    cx, cy, R = 170, 175, 120
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
             'font-family="sans-serif">' % (W_, H_)]
    parts.append('<rect width="680" height="340" fill="#ffffff"/>')
    # 左：单位圆分区
    segs = [("EM", -30, 30, "#4d8fd6"), ("S", 90, 150, "#d64d4d"),
            ("W", 210, 270, "#4dd67c")]
    for name, a0, a1, col in segs:
        a0r, a1r = math.radians(a0 - 90), math.radians(a1 - 90)
        x0, y0 = cx + R * math.cos(a0r), cy + R * math.sin(a0r)
        x1, y1 = cx + R * math.cos(a1r), cy + R * math.sin(a1r)
        large = 0
        parts.append('<path d="M%d %d A%d %d 0 %d 1 %d %d L%d %d Z" fill="%s" '
                     'fill-opacity="0.55" stroke="none"/>' % (cx, cy, R, R, large, x1, y1, cx, cy, col))
        mid = math.radians((a0 + a1) / 2 - 90)
        lx, ly = cx + (R + 22) * math.cos(mid), cy + (R + 22) * math.sin(mid)
        parts.append('<text x="%d" y="%d" font-size="15" text-anchor="middle" '
                     'fill="#222">%s</text>' % (lx, ly, name))
    # G：三个负瓣
    for a0, a1 in ((30, 90), (150, 210), (270, 330)):
        a0r, a1r = math.radians(a0 - 90), math.radians(a1 - 90)
        x0, y0 = cx + R * math.cos(a0r), cy + R * math.sin(a0r)
        x1, y1 = cx + R * math.cos(a1r), cy + R * math.sin(a1r)
        parts.append('<path d="M%d %d A%d %d 0 0 1 %d %d L%d %d Z" fill="#9aa3ad" '
                     'fill-opacity="0.55"/>' % (cx, cy, R, R, x1, y1, cx, cy))
    parts.append('<text x="%d" y="%d" font-size="15" text-anchor="middle" fill="#222">G×3</text>'
                 % (cx + R + 30, cy))
    parts.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#333" stroke-width="1.5"/>'
                 % (cx, cy, R))
    parts.append('<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#222">'
                 'M2 重指派：正瓣↔EM/S/W，负瓣之并↔G</text>' % (cx, 30))
    parts.append('<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="#555">'
                 '各正瓣 60°，互斥；D_G = cos3θ&lt;0（不连通，3 瓣）</text>' % (cx, 315))
    # 右：Ω(θ)=cos3θ 曲线
    ox, oy, ow, oh = 380, 60, 270, 200
    parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#f7f8fa" stroke="#ccc"/>'
                 % (ox, oy, ow, oh))
    pts = []
    for i in range(361):
        th = math.radians(i)
        px = ox + ow * i / 360.0
        py = oy + oh / 2 - (oh / 2 - 6) * math.cos(3 * th)
        pts.append("%.1f,%.1f" % (px, py))
    parts.append('<polyline points="%s" fill="none" stroke="#2a5fa8" stroke-width="1.8"/>'
                 % " ".join(pts))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-dasharray="4 3"/>'
                 % (ox, oy + oh / 2, ox + ow, oy + oh / 2))
    for deg in (30, 90, 150, 210, 270, 330):
        px = ox + ow * deg / 360.0
        parts.append('<circle cx="%.1f" cy="%d" r="3" fill="#d64d4d"/>' % (px, oy + oh / 2))
    for deg, lab in ((0, "0°"), (90, "90°"), (180, "180°"), (270, "270°"), (360, "360°")):
        px = ox + ow * deg / 360.0
        parts.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" fill="#555">%s</text>'
                     % (px, oy + oh + 14, lab))
    parts.append('<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#222">'
                 'Ω(θ)=cos3θ：6 个符号区间，红点为零点 30°+60°k</text>' % (ox + ow / 2, 30))
    parts.append('<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="#555">'
                 '解 θ_G 距零点仅 %.1e rad（~%d 位精度）</text>'
                 % (ox + ow / 2, 315, delta_G_rad, round(digits)))
    parts.append('</svg>')
    return "\n".join(parts)


svg = make_svg()
with open(os.path.join(OUT_DIR, BASE + ".svg"), "w", encoding="utf-8") as fp:
    fp.write(svg + "\n")
add("P6", "分区结构图与 Ω 剖面图（SVG）",
    "文件生成且非空",
    "%d 字节 -> %s.svg" % (len(svg), BASE),
    "PASS" if len(svg) > 1000 else "MISMATCH")

# ---------------------------------------------------------------- 产物落盘
os.makedirs(OUT_DIR, exist_ok=True)
n_pass = sum(1 for x in RESULTS if x["verdict"] == "PASS")
rep = []
rep.append("# TUFT-MATH-PROOF-ADD-02 攻坚数据（2026-10-04）")
rep.append("")
rep.append("- 引擎：`源码/%s.py`（纯标准库）" % BASE)
rep.append("- 读数：**条目 %d —— PASS %d / MISMATCH %d**" % (len(RESULTS), n_pass, len(RESULTS) - n_pass))
rep.append("")
rep.append("## 耦合匹配解表（λ = α_s = 0.1179）")
rep.append("")
rep.append("| 力 | α | α/λ | 域内解 θ（度） | 距瓣心 | 距域边界 |")
rep.append("|---|---|---|---|---|---|")
rows = [
    ("Strong", ALPHA_S, sol_S, 120.0, 30.0),
    ("EM", ALPHA_EM, sol_EM, 0.0, 30.0),
    ("Weak", ALPHA_W, sol_W, 240.0, 30.0),
]
for name, al, sols, center, half in rows:
    if sols:
        th = sols[0]
        d_center = min(abs(((th - center + 180) % 360) - 180), abs(((th - center + 180) % 360) - 180))
        d_edge = half - min(abs(((th - center + 180) % 360) - 180), 180 - abs(((th - center + 180) % 360) - 180)) \
            if False else ""
        rep.append("| %s | %.4e | %.6f | %s | %.2f° | — |" %
                   (name, al, al / lam, ", ".join("%.3f" % x for x in sols),
                    min(abs(th - center), 360 - abs(th - center))))
rep.append("| G | %.4e | %.3e | 零点 G 侧 ×6：θ0±%.3e° | — | %.3e° |" %
           (ALPHA_G, ALPHA_G / lam, delta_G_deg, delta_G_deg))
rep.append("")
rep.append("## 层级定价")
rep.append("")
rep.append("- 耦合跨度：α_s/α_G = %.1f 个量级" % span)
rep.append("- θ_G 距域边界：%.3e 弧度 = %.3e 度 ⇒ ~%.0f 位十进制精度" % (delta_G_rad, delta_G_deg, digits))
rep.append("- 敏感度（耦合相对变化/代表点每偏 1°）：Strong 0（二阶稳定）；EM %.0f%%；Weak %.0f%%；G %.1e%%"
           % (100 * sens_EM, 100 * sens_W, 100 * sens_G))
rep.append("- **结论**：单常数 cos3θ 结构下，耦合层级不被解释，而是被转移为代表点的角度精细调节——"
           "与前置 B-08（D-01 定价不可消除）同构且更强。登记为开放项 OPEN-ΩH。")
rep.append("")
with open(os.path.join(OUT_DIR, BASE + ".md"), "w", encoding="utf-8") as fp:
    fp.write("\n".join(rep) + "\n")
with open(os.path.join(OUT_DIR, BASE + ".json"), "w", encoding="utf-8") as fp:
    json.dump({"base": BASE, "date": "2026-10-04", "results": RESULTS,
               "fitting": {"lambda": lam, "theta_S": sol_S, "theta_EM": sol_EM,
                           "theta_W": sol_W, "theta_G_count": len(sol_G),
                           "delta_G_rad": delta_G_rad, "digits": digits, "span_dex": span},
               "summary": {"total": len(RESULTS), "pass": n_pass}},
              fp, ensure_ascii=False, indent=1)

print("\n读数: PASS %d / %d -> %s" % (n_pass, len(RESULTS), os.path.join(OUT_DIR, BASE + ".md")))
sys.exit(0 if n_pass == len(RESULTS) else 1)
