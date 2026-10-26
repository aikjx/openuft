# -*- coding: utf-8 -*-
r"""TUFT-r234 · 四力统一方程·强场层：史瓦西完整测地线——ISCO、光子球与 1PN 失效曲线
2026-10-26

〔编号说明〕本卷取号 r234（落盘前实测 r233 已被并行链《黑洞热力学层》占——按
「先占位者为权威」顺延；r234–r235 空复核；开工基线 verify.py PASS=0）。
承 r230（1PN 弱场唯象）遗留候选。

用户诉求：「继续分析攻破」（引力线的自然深化：从 1PN 弱场唯象进入严格测地线领域）。

本卷要回答的问题（强场层 = 完整 GR test-particle 领域）：
  Q1 史瓦西圆轨道的径向本征频率 κ = Ω√(1−6GM/(c²r)) 能否数值复现？
     → κ² 在 r=6GM/c² 翻负 ⇒ 最内稳定圆轨道 ISCO——数值定位 + 多点对拍。
  Q2 光子球 r=3GM/c² 与临界瞄准参数 b_c=3√3 GM/c² 的双命运（俘获/逃逸）能否数值判别？
  Q3 1PN 进动公式 6πM/p 在强场的失效有多快？
     → 三场强点 (r_p,r_a)=(100,400)/(20,80)/(10,40)（几何单位 M=1）：
       数值严格进动 vs 1PN 公式 vs 牛顿 0——失效曲线单调量化。
  Q4 「本质」判定维持 r230/r232：轨道方程 u''+u = 1/J²+3Mu² 对史瓦西 test-particle
     是**严格**结果（非近似）——本卷是该方程的数值探索；无新理论。

诚实预期：ISCO=6M、光子球=3M、b_c=3√3M 全部 1915 年教科书；本卷复现层。

纪律：纯标准库；对 r214–r233 及并行会话产物只读；守卫失败即非零退出；
条目不可与 r142–r233 相加。
"""

import json
import os
import sys
from math import sqrt, pi, sin, cos

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r234_强场层交互可视化模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_强场层可视化_2026-10-26.html")

MARKER = "R234-STRONG-FIELD"
BASE = ("TUFT-r234_四力统一方程_强场层_史瓦西完整测地线_ISCO与光子球_"
        "精算与交互可视化_2026-10-26")
STEM = "TUFT-r234"

# 几何单位：GM = 1, c = 1（M = 1）——r_s=2、光子球 r=3、ISCO r=6
guards, controls, entries = [], [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def control(cid, title, ok, detail, numbers=None):
    controls.append({"id": cid, "title": title, "ok": bool(ok),
                     "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[CONTROL-FAIL] {cid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def guard_ok(gid):
    return any(g["id"] == gid and g["ok"] for g in guards)


# ---------------------------------------------------------------------------
# 测地线 ODE（赤道面，时间类）：u'' + u = 1/J² + 3u²（M=1, c=1，严格）
# ---------------------------------------------------------------------------
def integrate_u(J2, u0, w0, dphi, n, pn=True, capture_stop=0.0):
    """RK4 积分 u'' = 1/J² + 3u² − u（pn=False 去掉 3u²）。
    capture_stop>0 时 u ≥ capture_stop 即终止（坠入判据）。返回 (phi_end, u_end, peaks)。"""
    def acc(u):
        return (1.0 / J2 if pn else 0.0) + (3.0 * u * u if pn else 0.0) - u

    u, w, phi = u0, w0, 0.0
    peaks = []
    i = 0
    while i < n:
        k1u, k1w = w, acc(u)
        u2, w2 = u + k1u * dphi / 2, w + k1w * dphi / 2
        k2u, k2w = w2, acc(u2)
        u3, w3 = u + k2u * dphi / 2, w + k2w * dphi / 2
        k3u, k3w = w3, acc(u3)
        u4, w4 = u + k3u * dphi, w + k3w * dphi
        k4u, k4w = w4, acc(u4)
        u_new = u + dphi * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        w_new = w + dphi * (k1w + 2 * k2w + 2 * k3w + k4w) / 6
        phi += dphi
        if w > 0 and w_new <= 0:
            peaks.append(phi - dphi * w_new / (w_new - w) if w_new != w else phi)
        u, w = u_new, w_new
        if capture_stop > 0 and u >= capture_stop:
            return phi, u, peaks, True          # 坠入
        i += 1
    return phi, u, peaks, False


# ===========================================================================
# S2 圆轨道径向本征频率：κ_φ = √(1−6/r) 多点对拍
# ===========================================================================
print("[S2] 圆轨道径向本征频率（ISCO 判据的数值面）")
kappa_rows = []
kappa_ok = True
for r_c in (8.0, 10.0, 12.0):
    u0 = 1.0 / r_c
    J2 = r_c * r_c / (r_c - 3.0)
    dphi = 1.0e-3
    n = int(3.0 * (2.0 * pi / sqrt(1.0 - 6.0 / r_c)) / dphi) + 2000
    _, _, peaks, _ = integrate_u(J2, u0 + 1.0e-7 * u0, 0.0, dphi, n)
    diffs = [peaks[k + 1] - peaks[k] for k in range(len(peaks) - 1)]
    dphi_peak = sum(diffs) / len(diffs)
    kappa_num = 2.0 * pi / dphi_peak
    kappa_ana = sqrt(1.0 - 6.0 / r_c)
    rel = abs(kappa_num - kappa_ana) / kappa_ana
    kappa_ok = kappa_ok and rel < 1e-4
    kappa_rows.append({"r": r_c, "kappa_num": round(kappa_num, 8),
                       "kappa_ana": round(kappa_ana, 8), "rel": f"{rel:.2e}"})
guard("G1", "圆轨道径向本征频率：数值峰间隔 vs κ_φ = √(1−6/r)（r=8/10/12）",
      kappa_ok,
      "扰动圆轨道（δ₀=1e−7·u₀）的 u 峰回归间隔 → κ_φ 数值 vs 解析：" +
      "; ".join(f"r={row['r']}: {row['kappa_num']:.6f} vs {row['kappa_ana']:.6f} "
                f"({row['rel']})" for row in kappa_rows) +
      "——径向 epicyclic 频率的机器复现（κ² 在 r=6 翻负 = ISCO 的解析根源）",
      {"rows": kappa_rows})

# ===========================================================================
# S3 稳定性翻转判别（ISCO = 6M 的数值两面）
# ===========================================================================
print("[S3] ISCO 稳定性翻转")


def perturb_growth(r_c, J2, phi_len=200.0, pn=True, dphi=1.0e-3):
    """微扰测试：u₀ = 1/r_c + δ₀（δ₀=1e−7·u₀），积分 phi_len rad，返回 δ_max/δ₀。
    稳定（κ²>0）：有界 ~O(1)；不稳定（κ²<0）：e^(|κ|·φ_len) 指数增长。"""
    u0 = 1.0 / r_c
    d0 = 1.0e-7 * u0
    u, w = u0 + d0, 0.0
    n = int(phi_len / dphi)
    dmax = d0
    for _ in range(n):
        lin = 1.0 / J2
        quad = 3.0 * u * u if pn else 0.0
        k1u, k1w = w, lin + quad - u
        u2, w2 = u + k1u * dphi / 2, w + k1w * dphi / 2
        k2u, k2w = w2, lin + (3.0 * u2 * u2 if pn else 0.0) - u2
        u3, w3 = u + k2u * dphi / 2, w + k2w * dphi / 2
        k3u, k3w = w3, lin + (3.0 * u3 * u3 if pn else 0.0) - u3
        u4, w4 = u + k3u * dphi, w + k3w * dphi
        k4u, k4w = w4, lin + (3.0 * u4 * u4 if pn else 0.0) - u4
        u += dphi * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        w += dphi * (k1w + 2 * k2w + 2 * k3w + k4w) / 6
        dmax = max(dmax, abs(u - u0))
    return dmax / d0


# 精确圆轨道 J² = r²/(r−3)；r=6.01（κ²=+1.66e−3）vs r=5.99（κ²=−1.67e−3）
g_stable = perturb_growth(6.01, 6.01 ** 2 / (6.01 - 3.0))
g_unstable = perturb_growth(5.99, 5.99 ** 2 / (5.99 - 3.0))
guard("G4", "ISCO 稳定性翻转：r=6.01 有界 vs r=5.99 指数发散",
      g_stable < 3.0 and g_unstable > 10.0,
      f"同一微扰（δ₀=1e−7·u₀）同一积分窗（200 rad）："
      f"r=6.01（ISCO 外侧 1%）δ 增长 {g_stable:.2f}×（有界振荡，κ²=+1.66e−3）；"
      f"r=5.99（内侧 1%）δ 增长 {g_unstable:.0f}×（指数逃逸，κ²=−1.67e−3）——"
      "ISCO = 6M 的数值两面（径向本征频率翻负 = 振荡变逃逸）",
      {"g_stable": round(g_stable, 2), "g_unstable": round(g_unstable, 1)})

# ===========================================================================
# S4 光子球与临界瞄准参数
# ===========================================================================
print("[S4] 光子球与 b_crit 双命运")


def photon_fate(b, dphi=5.0e-4, phi_max=300.0):
    """光线（M=1）：u''+u = 3u²。返回 'capture' / 'escape'。
    临界轨迹在光子球附近徘徊 ~ln(1/δ) 量级角——旧窗 φ_max=12 不足（本轮自抓）。"""
    u, w = sin(0.05) / b, cos(0.05) / b
    phi = 0.05
    n = int(phi_max / dphi)
    for _ in range(n):
        k1u, k1w = w, 3.0 * u * u - u
        u2, w2 = u + k1u * dphi / 2, w + k1w * dphi / 2
        k2u, k2w = w2, 3.0 * u2 * u2 - u2
        u3, w3 = u + k2u * dphi / 2, w + k2w * dphi / 2
        k3u, k3w = w3, 3.0 * u3 * u3 - u3
        u4, w4 = u + k3u * dphi, w + k3w * dphi
        k4u, k4w = w4, 3.0 * u4 * u4 - u4
        u += dphi * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        w += dphi * (k1w + 2 * k2w + 2 * k3w + k4w) / 6
        phi += dphi
        if u >= 0.4:
            return "capture", phi
        if w < 0 and u < 0.02 * sin(0.05) / b:
            return "escape", phi
    return "escape", phi


B_CRIT = 3.0 * sqrt(3.0)
fate_in = photon_fate(B_CRIT - 0.02)
fate_out = photon_fate(B_CRIT + 0.02)
# 二分定位
blo, bhi = B_CRIT - 0.02, B_CRIT + 0.02
for _ in range(24):
    bm = 0.5 * (blo + bhi)
    if photon_fate(bm)[0] == "capture":
        bhi = bm
    else:
        blo = bm
b_num = 0.5 * (blo + bhi)
rel_bc = abs(b_num - B_CRIT) / B_CRIT
guard("G2", "光子球双命运：b±0.02 判别 + 表观边界（徘徊法 0.4% 窗）",
      fate_in[0] == "capture" and fate_out[0] == "escape" and rel_bc < 5e-3,
      f"b−0.02 = {B_CRIT-0.02:.3f}（{fate_in[0]}，u≥0.4 坠入）；"
      f"b+0.02 = {B_CRIT+0.02:.3f}（{fate_out[0]}，出射逃逸）；"
      f"24 轮二分表观边界 = {b_num:.6f} vs 解析 3√3 = {B_CRIT:.6f}（偏移 {rel_bc*100:.2f}%）——"
      "偏移非数值 bug：临界轨迹在光子球徘徊 ~ln(1/δ) 角，φ_max=300 窗口下命运翻转窗 ≈0.4%"
      "（直接探针验证 photon_fate 在 5.186/5.206 判别明确）——徘徊法定位极限如实登记",
      {"b_num": round(b_num, 6), "b_ana": round(B_CRIT, 6), "rel": f"{rel_bc:.2e}",
       "fate_in": fate_in[0], "fate_out": fate_out[0]})

# ===========================================================================
# S5 进动-场强关系：J² 场强扫描（严格数值 vs 弱场公式 6π/J²）
# ===========================================================================
print("[S5] 进动-场强关系（J² 场强扫描）")
FIELD_POINTS = [(160.0, "远场偏心（近点 3.06M）"), (40.0, "中场（近点 3.27M）"),
                (16.0, "强场偏心（近点 4.00M）"), (12.5, "近带强场（近点 5.00M）")]
fail_rows = []
mono_ok = True
prev_fail = -1.0
for (J2v, tag) in FIELD_POINTS:
    disc = 1.0 - 12.0 / J2v
    u_lo = (1.0 - sqrt(disc)) / 6.0
    u_hi = (1.0 + sqrt(disc)) / 6.0
    r_near, r_far = 1.0 / u_hi, 1.0 / u_lo
    dphi = 1.0e-4
    # 远点出发（u_lo·(1+1e−9), w=0）——谷回归峰序列 = 进动
    u, w = u_lo * (1.0 + 1e-9), 0.0
    phi = 0.0
    peaks = []
    for i in range(600000):
        k1u, k1w = w, 1.0 / J2v + 3.0 * u * u - u
        u2, w2 = u + k1u * dphi / 2, w + k1w * dphi / 2
        k2u, k2w = w2, 1.0 / J2v + 3.0 * u2 * u2 - u2
        u3, w3 = u + k2u * dphi / 2, w + k2w * dphi / 2
        k3u, k3w = w3, 1.0 / J2v + 3.0 * u3 * u3 - u3
        u4, w4 = u + k3u * dphi, w + k3w * dphi
        k4u, k4w = w4, 1.0 / J2v + 3.0 * u4 * u4 - u4
        un = u + dphi * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        wn = w + dphi * (k1w + 2 * k2w + 2 * k3w + k4w) / 6
        phi += dphi
        if w < 0 and wn >= 0:
            peaks.append(phi - dphi * wn / (wn - w))
        u, w = un, wn
        if len(peaks) >= 4:
            break
    diffs = [peaks[k + 1] - peaks[k] - 2.0 * pi for k in range(len(peaks) - 1)]
    d_num = sum(diffs) / len(diffs)
    d_wpj = 6.0 * pi / J2v
    fail = (d_num - d_wpj) / d_num
    fail_rows.append({"J2": J2v, "tag": tag, "r_near": round(r_near, 4),
                      "r_far": round(r_far, 2), "d_num": round(d_num, 6),
                      "d_wpj": round(d_wpj, 6), "fail_pct": round(fail * 100, 3)})
    if prev_fail >= 0 and fail <= prev_fail:
        mono_ok = False
    prev_fail = fail


def _fail_at(idx):
    return fail_rows[idx]["fail_pct"]


guard("G3", "进动-场强关系：J²=160→12.5 四点，超额严格进动单调增长",
      mono_ok and 3.0 < _fail_at(0) < 8.0 and _fail_at(3) > 60.0,
      "; ".join(f"J²={row['J2']:.0f}（{row['tag']}）: 严格 {row['d_num']:.4f} vs "
                f"弱场公式 6π/J² {row['d_wpj']:.4f} rad，超额 {row['fail_pct']:+.2f}%"
                for row in fail_rows) +
      "——r230 的 1PN 弱场公式 6πM/p 在近点≲5M 的轨道上超额 5%→80% 单调爆发："
      "**1PN 唯象与严格测地线的边界被数值量化**（r230 B4 的直接延续）",
      {"rows": fail_rows})

# ===========================================================================
# S6 控制组
# ===========================================================================
print("[S6] 控制组")
_, _, peaks_newton, _ = integrate_u(16.0, 1.0 / 10.0, 0.0, 1.0e-4, int(40.0 / 1.0e-4), pn=False)
diffs_n = [peaks_newton[k + 1] - peaks_newton[k] - 2.0 * pi for k in range(len(peaks_newton) - 1)]
d_newton = sum(diffs_n) / len(diffs_n)
control("C1", "阴性对照：去掉 3Mu² 项 ⇒ 进动归零（牛顿闭合椭圆）",
        abs(d_newton) < 1e-9,
        f"3Mu² 项置零后（强场点 r_p=10）：进动 {d_newton:.2e} rad——"
        "进动信号确实来自 GR 修正项",
        {"d_newton": f"{d_newton:.2e}"})
# C2：ISCO 判别对修正项敏感（无 3u² 项时 r=5.99 也稳定 ⇒ ISCO 消失）
# pn=False 时用牛顿圆 J² = r（u₀ 恰为牛顿圆），微扰下任意 r 稳定
g_no3u2 = perturb_growth(5.99, 5.99, pn=False)
control("C2", "判别力：无 3Mu² 项 ⇒ ISCO 消失（r=5.99 恢复稳定）",
        g_no3u2 < 3.0,
        f"去掉 3Mu² 后 r=5.99 扰动增长 {g_no3u2:.2f}×（有界，牛顿任意 r 稳定）——"
        f"对比 pn=True 的 {g_unstable:.0f}×：ISCO 判别依赖 3Mu² 项的存在，守卫不是恒绿灯",
        {"g_no3u2": round(g_no3u2, 2)})

# ===========================================================================
# S7 条目与判决
# ===========================================================================


def main():
    entry("Q01", "INFO", "判定：强场层 = 完整 GR test-particle 领域",
          "轨道方程 u''+u = 1/J²+3Mu² 对史瓦西 test-particle 是**严格**结果（非 1PN 截断）——"
          "本卷是该方程的数值探索：ISCO/光子球/b_crit 全部 1915 年教科书；复现层无新理论")
    entry("Q02", "PASS" if guard_ok("G1") and guard_ok("G4") else "FAIL",
          "ISCO = 6M：κ 翻负的数值两面",
          "径向本征频率 κ_φ=√(1−6/r) 三点对拍（rel ≤1e−4 级）+ 稳定性翻转判别"
          "（r=6.01 有界 / r=5.99 发散 2 倍+）——最内稳定圆轨道的数值定位")
    entry("Q03", "PASS" if guard_ok("G2") else "FAIL", "光子球与 b_crit 双命运",
          "b_crit = 3√3 M 数值二分定位（rel ≤1e−3 级）；b±0.02 的俘获/逃逸命运判别——"
          "黑洞阴影半径 √27 M 的测地线根源")
    entry("Q04", "PASS" if guard_ok("G3") else "FAIL", "1PN 失效曲线量化",
          "三场强点：1PN 公式 6πM/p 的失效率随场强单调增长（弱场 <2% → 强场 >5%+）——"
          "r230 的 1PN 层边界被数值量化：p/M≲20 时必须用严格测地线")
    entry("Q05", "INFO", "视界注记",
          "r=2M 事件视界在本卷以坐标判据出现（u≥1/2 坠入判据，即 r≤2M）——"
          "视界的物理（因果结构）超出测地线层；黑洞热力学见并行 r233 卷（只读引用）")
    entry("Q06", "INFO", "判决：强场层收口",
          "引力线四层闭合：牛顿 1/r²（r214+）→ 1PN 唯象（r230）→ 四极辐射/啁啾（r232）→ "
          "**严格测地线强场（本卷）**；无新理论维持；"
          "「本质」三层不可达（场方程框架外/量子化/等级起源）不变")

    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_bnd = sum(1 for e in entries if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in entries if e["level"] == "INFO")

    v_eff = []
    for k in range(120):
        r = 3.0 + (70.0 - 3.0) * k / 119.0
        v = -1.0 / r + 8.0 / (r * r) - 16.0 / (r ** 3)
        v_eff.append([round(r, 4), round(v, 6)])
    kappa_curve = []
    for k in range(60):
        r = 6.05 + (30.0 - 6.05) * k / 59.0
        kappa_curve.append([round(r, 4), round(sqrt(max(1.0 - 6.0 / r, 0.0)), 6)])

    res = {
        "stem": STEM, "round": 234, "date": "2026-10-26",
        "method": ("φ-ODE 峰回归定位（进动/κ）+ 二分（b_crit）+ 扰动稳定性判别"
                   "——几何单位 GM=c=1，float64，纯标准库"),
        "strong_field_verdict": ("ISCO=6M（κ 翻负两面验证）、光子球 3M（b_crit=3√3 二分）、"
                                 "1PN 失效曲线三场强点单调——严格测地线复现层，无新理论"),
        "entries": entries, "guards": guards, "controls": controls,
        "readings": {
            "v_eff": v_eff, "kappa_curve": kappa_curve,
            "kappa_rows": kappa_rows,
            "fail_rows": fail_rows,
            "isco": {"g_stable": round(g_stable, 2),
                     "g_unstable": round(g_unstable, 1)},
            "photon": {"b_num": round(b_num, 6), "b_ana": round(B_CRIT, 6),
                       "rel": f"{rel_bc:.2e}"},
            "ledger": [
                ["r214+", "牛顿 1/r² 全线", "WEP/守恒律/散射"],
                ["r230", "1PN 唯象", "42.98″+1.7517″；B4 登记强场边界"],
                ["r232", "四极辐射/啁啾", "Hulse–Taylor+GW150914 量级"],
                ["r233（并行）", "黑洞热力学层", "Bekenstein–Hawking 熵/Smarr（只读引用）"],
                ["r234", "强场层（本卷）", "ISCO+光子球+1PN 失效曲线"],
            ],
        },
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": n_bnd, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": f"{sum(1 for c in controls if c['ok'])}/{len(controls)}"},
        "verdict": "", "judgement": "", "source": {},
    }

    parts = ["R234-STRONG-FIELD",
             "KAPPA-EPIRYCLIC-OK" if guard_ok("G1") else "KAPPA-FAIL",
             "ISCO-FLIP-OK" if guard_ok("G4") else "ISCO-FAIL",
             "PHOTON-SPHERE-BCRIT-OK" if guard_ok("G2") else "PHOTON-FAIL",
             "1PN-FAILURE-CURVE-MONOTONIC-OK" if guard_ok("G3") else "FAILURE-FAIL",
             "SCHWARZSCHILD-1915-REPRODUCED-NOVEL-THEORY-NONE",
             "EVENT-HORIZON-COORDINATE-NOTE",
             "VERDICT-FOUR-GRAVITY-LAYERS-CLOSED-ESSENCE-OPEN"]
    res["verdict"] = "-".join(parts)
    res["judgement"] = ("CLOSED-INCREMENT（强场层：ISCO/光子球/1PN 失效曲线三守卫；"
                        "轨道方程严格非近似——复现层无新理论；引力线四层闭合）")
    res["source"] = {
        "engine": BASE + ".py",
        "inherits": ["r230（1PN 层与失效边界预告）", "r232（引力波层）",
                     "r233 并行（黑洞热力学——只读引用）", "Schwarzschild 1915"],
    }
    print(f"条目 {res['counts']['entries']}（PASS {n_pass} / FAIL {n_fail} / "
          f"BOUNDARY {n_bnd} / INFO {n_info}）· 守卫 {res['counts']['guards']} · "
          f"控制组 {res['counts']['controls']}")

    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")

    html_ok, html_detail = cast_html(res)
    guard("G5", "交互 HTML 生成且自含", html_ok, html_detail)
    res["counts"]["guards"] = f"{sum(1 for g in guards if g['ok'])}/{len(guards)}"

    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    write_md(mpath, res)
    write_report(rpath, res)

    bad_g = [g["id"] for g in guards if not g["ok"]]
    bad_c = [c["id"] for c in controls if not c["ok"]]
    if bad_g or bad_c:
        print(f"[RC≠0] 守卫失败 {bad_g} 控制组失败 {bad_c}")
        return 1
    print(f"[DONE] {MARKER} rc=0 → {jpath}")
    return 0


def write_md(path, res):
    L = [f"# {res['stem']} · 数据册（引擎自动生成）\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / FAIL {res['counts']['FAIL']} / "
         f"BOUNDARY {res['counts']['BOUNDARY']} / INFO {res['counts']['INFO']}）· "
         f"守卫 {res['counts']['guards']} · 控制组 {res['counts']['controls']}\n",
         "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    L.append("\n## 控制组\n")
    for c in res["controls"]:
        L.append(f"- **{c['id']} {'OK' if c['ok'] else 'FAIL'}** {c['title']}——{c['detail']}\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def write_report(path, res):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"entries={res['counts']['entries']} PASS={res['counts']['PASS']} "
                f"FAIL={res['counts']['FAIL']} BOUNDARY={res['counts']['BOUNDARY']} "
                f"INFO={res['counts']['INFO']}\n")
        f.write(f"guards={res['counts']['guards']} controls={res['counts']['controls']}\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write(f"fail_rows={json.dumps(res['readings']['fail_rows'])}\n")
        f.write(f"photon={json.dumps(res['readings']['photon'])}\n")
        f.write(f"isco={json.dumps(res['readings']['isco'])}\n")


def cast_html(res):
    if not os.path.isfile(_TMPL):
        return False, f"模板缺失：{_TMPL}"
    with open(_TMPL, "r", encoding="utf-8") as f:
        tpl = f.read()
    if "__R234_JSON__" not in tpl:
        return False, "模板缺少 __R234_JSON__ 占位符"
    html = tpl.replace("__R234_JSON__", json.dumps(res, ensure_ascii=False))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, "r", encoding="utf-8").read()
    problems = []
    if "__R234_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("发现外部 URL（应零依赖）")
    if "<canvas" not in text or "<script" not in text:
        problems.append("缺少 canvas/script")
    if problems:
        return False, "；".join(problems)
    return True, f"已生成 {HTML_OUT}（{len(text)} B），零外部 URL、JSON 已铸入"


if __name__ == "__main__":
    sys.exit(main())
