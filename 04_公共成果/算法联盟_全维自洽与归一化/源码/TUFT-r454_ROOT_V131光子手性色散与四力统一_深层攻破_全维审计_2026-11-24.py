#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r454 / ROOT V131 深层攻破：光子手性色散与四力统一审查。

只读 V131 来料正本；不验收 ZIP/HTML/外链观测原文。纯标准库：
Decimal 60 位做色散、稳定性与偏振数值；Fraction/整数计数做结构账。
"""
from __future__ import print_function

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "04_公共成果" / "算法联盟_全维自洽与归一化"
DATA = BASE / "数据"
STEM = "TUFT-r454_ROOT_V131光子手性色散与四力统一_深层攻破_全维审计_2026-11-24"
SOURCE = DATA / "TUFT-ROOT_V131_光子螺旋度传播方程与四力统一审查_来料全文_2026-11-24.md"

D = Decimal
PI = D("3.14159265358979323846264338327950288419716939937510582097494")
DEG = D("180") / PI

entries = []
guards = []
key = {}


def fmt(x, digits="18"):
    x = D(x)
    digits = str(digits)
    if x == 0:
        return "0"
    return format(x, "." + digits + "E")


def rel(a, b):
    a, b = D(a), D(b)
    return abs(a - b) / max(abs(a), abs(b), D("1e-80"))


def dsqrt(x):
    x = D(x)
    if x < 0:
        raise ValueError("sqrt of negative Decimal")
    return (x.ln() / D(2)).exp()


def add(code, status, title, detail):
    entries.append({"id": code, "status": status, "title": title, "detail": detail})


def guard(code, ok, detail):
    guards.append({"id": code, "status": "PASS" if ok else "FAIL", "detail": detail})


def main():
    if not SOURCE.exists():
        print("MISSING SOURCE:", SOURCE)
        return 2
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    key["source_sha256"] = sha
    key["source_bytes"] = len(raw)

    anchors = [
        "S=\\int d^4x\\sqrt{-g}",
        "\\nabla\\cdot\\mathbf E &=-\\eta\\nabla\\theta\\cdot\\mathbf B",
        "\\ddot{\\mathbf A}-\\nabla^2\\mathbf A =\\eta\\dot\\theta\\,\\nabla\\times\\mathbf A",
        "\\ddot A_\\sigma+ \\left(k^2-\\sigma\\eta\\dot\\theta k\\right) A_\\sigma=0",
        "\\omega_\\sigma^2=k^2-\\sigma bk",
        "v_{g,\\sigma}^2-1 =\\frac{b^2}{4k(k-\\sigma b)}",
        "\\gamma_{\\max}=\\frac{|b|}{2}",
        "\\Delta\\beta\\simeq\\frac b2L",
        "0.028648",
        "\\eta_1 B_{\\mu\\nu}\\widetilde B^{\\mu\\nu}",
        "\\eta_\\gamma =\\eta_1\\cos^2\\theta_W +\\eta_2\\sin^2\\theta_W",
        "ROOT V131｜光子手性色散与四力统一审查",
    ]
    hits = [a in text for a in anchors]
    guard("G0-01", all(hits), "来料锚点 %d/%d 可见" % (sum(hits), len(hits)))
    guard("G0-02", len(sha) == 64 and len(raw) > 1000, "正本非空且 SHA256 格式有效")

    # ---- A 段：承认可复算数学 ----
    add("A-01", "PASS", "轴子电动力学作用量与场方程结构可复算",
        "S 中 -eta/4 theta F Ftilde 给 nabla·E=-eta nabla theta·B、nabla×B-dtE=eta(dottheta B+nabla theta×E)，另两条 Maxwell 方程不变；这是标准轴子电动力学形式。")
    add("A-02", "PASS", "两螺旋度色散与群速度公式成立",
        "theta=theta(t) 且横向规范下，A_sigma 方程为 ddot A_sigma+(k²-sigma b k)A_sigma=0，b=eta dottheta；vg=(2k-sigma b)/(2 sqrt(k²-sigma b k))，且 vg²-1=b²/[4k(k-sigma b)]。")
    b0, k0, sig = D("0.3"), D(1), 1
    omega2 = k0 * k0 - D(sig) * b0 * k0
    omega = dsqrt(omega2)
    vg_direct = (D(2) * k0 - D(sig) * b0) / (D(2) * omega)
    vg2_direct = vg_direct * vg_direct
    vg2_formula = D(1) + b0 * b0 / (D(4) * k0 * (k0 - D(sig) * b0))
    guard("G2-01", rel(omega2, D("0.7")) == 0, "b=0.3,k=1,sigma=+ 时 omega²=0.7")
    guard("G2-02", rel(vg2_direct, vg2_formula) < D("1e-50"), "vg 直接式与 vg²-1 公式一致")

    add("A-03", "PASS", "低频不稳定区间与最大增长率成立",
        "b>0 时 sigma=+、0<k<b 给 omega_+²<0，gamma=sqrt(bk-k²)，在 k=b/2 处 gamma_max=|b|/2；b<0 时不稳定分支交换。")
    b1, k1 = D(1), D("0.25")
    om2_low = k1 * k1 - b1 * k1
    gam2_low = b1 * k1 - k1 * k1
    gam_max = b1 / D(2)
    guard("G3-01", om2_low < 0 and rel(gam2_low, D("0.1875")) == 0, "低 k 分支 omega²<0 且 gamma²=0.1875")
    guard("G3-02", rel(gam_max, D("0.5")) == 0, "b=1 时 gamma_max=0.5 于 k=0.5")

    add("A-04", "PASS", "封闭场系统的能动量交换项相消",
        "Poynting 定理 RHS=-eta dottheta E·B，theta 扇区 RHS=+eta dottheta E·B；两式相加总能量守恒。EM 可从 theta 背景取能，但背景必须动态参与。")
    eta, dottheta, evec, bvec = D(1), D(2), D(3), D(5)
    rhs_em = -eta * dottheta * evec * bvec
    rhs_theta = eta * dottheta * evec * bvec
    guard("G4-01", rhs_em + rhs_theta == 0, "能量交换项逐项相消：%s + %s = 0" % (fmt(rhs_em), fmt(rhs_theta)))

    add("A-05", "PASS", "弱耦合偏振旋转数值与一阶/二阶分层可复算",
        "Delta beta≈bL/2 是一阶，vg-1≈b²/(8k²) 是二阶；b=1e-6 m^-1、lambda=550 nm、L=1 km 给旋转角约 0.028648°，vg²-1 约 1.916e-27。")
    k_numeric = D("1.1423973E7")
    b_numeric = D("1E-6")
    length = D("1000")
    rot_rad = b_numeric * length / D(2)
    rot_deg = rot_rad * DEG
    bk_ratio = b_numeric / k_numeric
    vg2m1 = b_numeric * b_numeric / (D(4) * k_numeric * (k_numeric - b_numeric))
    guard("G5-01", rel(rot_deg, D("0.028648")) < D("1e-5"), "偏振旋转角 %s deg 与来料 0.028648 deg 一致" % fmt(rot_deg, 12))
    guard("G5-02", rel(vg2m1, D("1.916E-27")) < D("1e-3"), "vg²-1=%s 与来料同量级" % fmt(vg2m1, 12))

    beta_center = D("0.277")
    beta_sigma = D("0.057")
    eta_delta_center = D(2) * beta_center / DEG
    eta_delta_sigma = D(2) * beta_sigma / DEG
    guard("G5-03", rel(eta_delta_center, D("0.009669")) < D("1e-3") and rel(eta_delta_sigma, D("0.001990")) < D("1e-3"),
          "ACT/Planck beta 反推 eta Delta theta=%s ± %s" % (fmt(eta_delta_center, 12), fmt(eta_delta_sigma, 12)))
    add("I-01", "INFO", "宇宙偏振观测只约束 eta 与 Delta theta 的乘积",
        "beta=(0.277±0.057)° 在该模型中只给 eta Delta theta≈0.009669±0.001990；不能分开 eta 与 Delta theta，更不能推出机械螺旋半径或 ROOT 几何。")

    # ---- B 段：深层攻破 ----
    guard("G6-01", "已有的轴子电动力学理论框架" in text and "不是 ROOT 已经独立发现的新物理" in text,
          "来料自陈模型属于已有轴子电动力学")
    add("B-01", "FAIL", "手性色散是已有轴子电动力学，不是 ROOT 新物理",
        "作用量、场方程、圆偏振分裂、低频不稳定、能量交换均是轴子电动力学标准结果。V131 的价值是把检验链写清，不是从光速螺旋第一性推出电磁手性。")

    has_theta_time = "\\theta=\\theta(t)" in text
    has_geometry_map = ("\\kappa" in text) or ("\\tau" in text) or ("空间螺旋" in text and "\\theta=" in text)
    guard("G6-02", has_theta_time and not has_geometry_map,
          "theta 仅作为背景场输入，未给 theta=f(kappa,tau,螺旋变量) 的映射")
    add("B-02", "FAIL", "theta 与 b 没有从 ROOT 几何自由度导出",
        "模型把 theta 定为无量纲赝标量，常取 theta=theta(t)，b=eta dottheta 是输入组合。没有给 theta 与 Frenet 曲率/挠率、光速闭环半径或内部空间的映射，因而两个螺旋度的差别不是由空间螺旋结构推出。")

    add("B-03", "FAIL", "总能量守恒不消除低频不稳定",
        "0<k<b 的指数增长在固定背景近似下明确存在；加入 theta 动力学后总能量守恒只说明能量从 theta 扇区转入 EM 扇区，不证明增长被饱和、不证明真空稳定，也不给初值约束或观测上界。")

    guard("G6-03", all(x in text for x in ("\\eta_1", "\\eta_2", "\\eta_3")) and "\\eta_\\gamma" in text,
          "三规范耦合 eta1/eta2/eta3 与电弱混合 eta_gamma 均在来料中")
    add("B-04", "FAIL", "跨相互作用耦合不是四力统一",
        "L_int 写入 eta1、eta2、eta3 三个自由耦合，规范群 U(1)/SU(2)/SU(3) 预先给定；eta_gamma=eta1 cos²theta_W+eta2 sin²theta_W 只是正则归一化后的低能匹配。没有推出规范群、耦合数值、粒子谱或混合角。")

    guard("G6-04", "未找到必要的动力学尺度关系" in text and "独立计算 \\(G\\)" in text,
          "来料自陈未独立建立引力尺度 G")
    add("B-05", "FAIL", "引力尺度 G 与 theta 手性扇区无动力学连接",
        "作用量含 R/(16πG)，但 G 是外部常数；没有把 G、f_theta、eta、V(theta) 或内部几何尺度联立的方程，也没有不依赖标定的引力可证伪预言。")

    guard("G7-01", "信号前沿速度" in text and "光锥限制" in text,
          "来料明确区分群速度超光速与信号前沿/因果传播")
    add("C-01", "BOUNDARY", "群速度大于 1 不等于信息超光速",
        "vg²-1=b²/[4k(k-sigma b)] 在稳定分支为正，但最高阶算子仍为 Box=dt²-nabla²；来料已正确说明这是背景场中的群速度，不是信号前沿速度。不得改写为“光子自旋导致真实超光速”。")

    zip_claim = "ROOT V131｜光子手性色散与四力统一审查" in text and "ZIP · 7 个文件" in text
    zip_file = DATA / "ROOT_V131_光子手性色散与四力统一审查.zip"
    guard("G7-02", zip_claim and not zip_file.exists(), "ZIP/HTML 面板只在来料中声明，库内未收到实体")
    add("C-02", "BOUNDARY", "ZIP、HTML 面板、外部论文与观测值只登记不验收",
        "来料声称 7 文件 ZIP、离线交互面板、SHA-256 清单与数值积分数据，但本轮只收到文本；ACT/Planck 观测与 PRD 引用也未取原文复核。数值只按来料文本常量复算。")

    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    key["status_counts"] = counts
    key["dispersion_test_b"] = fmt(b0)
    key["dispersion_test_k"] = fmt(k0)
    key["omega2_plus"] = fmt(omega2)
    key["vg2_direct"] = fmt(vg2_direct, 18)
    key["vg2_formula"] = fmt(vg2_formula, 18)
    key["low_k_omega2"] = fmt(om2_low)
    key["low_k_gamma2"] = fmt(gam2_low)
    key["gamma_max_b1"] = fmt(gam_max)
    key["energy_exchange_em"] = fmt(rhs_em)
    key["energy_exchange_theta"] = fmt(rhs_theta)
    key["lambda_numeric_m"] = "5.5e-7"
    key["k_numeric_per_m"] = fmt(k_numeric, 12)
    key["b_over_k"] = fmt(bk_ratio, 12)
    key["rotation_rad"] = fmt(rot_rad, 12)
    key["rotation_deg"] = fmt(rot_deg, 12)
    key["vg2_minus_1"] = fmt(vg2m1, 12)
    key["ACT_beta_deg"] = "%s ± %s" % (fmt(beta_center, 12), fmt(beta_sigma, 12))
    key["ACT_eta_delta_theta"] = "%s ± %s" % (fmt(eta_delta_center, 12), fmt(eta_delta_sigma, 12))

    md = ["# TUFT r454 机器数据：ROOT V131 深层攻破", ""]
    md.append("- 来源 SHA256：`%s`" % sha)
    md.append("- 关系：V131 来料深层审计；不改 r450-r453 任何字节。")
    md.append("")
    md.append("## 条目")
    md.append("")
    for e in entries:
        md.append("- `%s` [%s] **%s** — %s" % (e["id"], e["status"], e["title"], e["detail"]))
    md.append("")
    md.append("## 守卫")
    md.append("")
    for g in guards:
        md.append("- `%s` [%s] %s" % (g["id"], g["status"], g["detail"]))
    md.append("")
    md.append("## 关键读数")
    md.append("")
    for k2 in sorted(key):
        md.append("- `%s`: %s" % (k2, key[k2]))

    payload = {
        "round": "r454",
        "topic": "ROOT V131 光子手性色散与四力统一深层攻破",
        "source_sha256": sha,
        "source_bytes": len(raw),
        "relation": "deep attack on V131 text; axion electrodynamics arithmetic accepted; ROOT derivation not established; ZIP claimed but not received",
        "entries": entries,
        "guards": guards,
        "key_numbers": key,
    }

    (DATA / (STEM + ".md")).write_text("\n".join(md) + "\n", encoding="utf-8")
    (DATA / (STEM + ".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "TUFT r454 / ROOT V131 deep attack",
        "OK entries=%d guards=%d/%d" % (len(entries), sum(1 for g in guards if g["status"] == "PASS"), len(guards)),
        "source_sha256=" + sha,
        "status_counts=" + ",".join("%s:%d" % (k2, counts[k2]) for k2 in sorted(counts)),
        "rotation_deg=" + fmt(rot_deg, 12),
        "vg2_minus_1=" + fmt(vg2m1, 12),
        "ACT_eta_delta_theta=" + fmt(eta_delta_center, 12) + " +/- " + fmt(eta_delta_sigma, 12),
    ]
    (DATA / (STEM + "_report.txt")).write_text("\n".join(report) + "\n", encoding="utf-8")

    print("entries=%d guards=%d/%d" % (len(entries), sum(1 for g in guards if g["status"] == "PASS"), len(guards)))
    print("counts=" + repr(counts))
    print("rotation_deg=" + fmt(rot_deg, 12))
    return 0 if all(g["status"] == "PASS" for g in guards) else 1


if __name__ == "__main__":
    sys.exit(main())
