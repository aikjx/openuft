# -*- coding: utf-8 -*-
"""空间光速螺旋曲率挠率几何统一场论的核心公式复算（诚实版）。

本脚本仅复算来源语料的「核心几何恒等式」与「常数几何重参数化」，
并显式标注哪些是代数恒等式、哪些是用 CODATA 反算自身的循环自证。

不声称任何物理证明；输出用作 openuft 治理登记的证据记录。
"""
import math
import os

CODATA = {
    "m_e": 9.1093837015e-31,
    "hbar": 1.054571817e-34,
    "c": 299792458.0,
    "e": 1.602176634e-19,
    "epsilon0": 8.8541878128e-12,
    "alpha": 7.2973525693e-3,
}

OUT_LINES = []


def log(line):
    OUT_LINES.append(line)
    print(line)


def res(name, ok, detail, kind):
    tag = "PASS" if ok else "FAIL"
    log("{0:<28} {1}  [{2}]  {3}".format(name, tag, kind, detail))
    return ok


def main():
    m_e = CODATA["m_e"]
    hbar = CODATA["hbar"]
    c = CODATA["c"]
    e = CODATA["e"]
    eps0 = CODATA["epsilon0"]
    alpha = CODATA["alpha"]

    log("=" * 78)
    log("空间光速螺旋曲率挠率几何统一场论 核心公式复算（诚实版）")
    log("输入锚：CODATA 2018 推荐值（m_e, hbar, c, e, eps0, alpha）")
    log("=" * 78)

    # 电子层螺旋半径
    rho_e = hbar / (m_e * c)
    # 来源定义 alpha = rho / b  =>  b = rho / alpha
    b_e = rho_e / alpha

    # 曲率 / 挠率
    denom = rho_e * rho_e + b_e * b_e
    kappa_e = rho_e / denom
    tau_e = b_e / denom

    # 代数恒等式
    lhs = kappa_e * kappa_e + tau_e * tau_e
    rhs = 1.0 / denom
    ok_id = abs(lhs - rhs) / max(abs(rhs), 1e-300) < 1e-15
    res("C0003.kappa2+tau2", ok_id,
        "lhs={0:.6e} rhs={1:.6e} 残差={2:.2e}".format(lhs, rhs, abs(lhs - rhs)),
        "代数恒等式")

    # alpha = kappa / tau
    alpha_calc = kappa_e / tau_e
    ok_a = abs(alpha_calc - alpha) / alpha < 1e-15
    res("C0004.alpha=kappa/tau", ok_a,
        "alpha_calc={0:.6e} alpha={1:.6e}".format(alpha_calc, alpha),
        "定义性（非独立导出）")

    # 类光约束 omega*rho = c
    omega = c / rho_e
    ok_w = abs(omega * rho_e - c) < 1e-6
    res("C0001.omega*rho=c", ok_w,
        "omega*rho={0:.6e} c={1:.6e}".format(omega * rho_e, c),
        "代数恒等式")

    # 尺度变换不变性 alpha 不变
    k_scale = 1e6
    kappa_s = kappa_e / k_scale
    tau_s = tau_e / k_scale
    ok_scale = abs(kappa_s / tau_s - alpha) / alpha < 1e-15
    res("C0005.scale_invariance", ok_scale, "alpha 在尺度缩放下保持不变", "代数结果")

    # 质量几何化派生式（循环自证）
    m_recovered = hbar * tau_e * (alpha * alpha + 1.0) / (alpha * c)
    rel = abs(m_recovered - m_e) / m_e
    ok_m = rel < 1e-12
    res("C0006.m=hbar*tau*(a2+1)/(a c)", ok_m,
        "m_rec={0:.6e} m_e={1:.6e} 相对误差={2:.2e}".format(m_recovered, m_e, rel),
        "循环自证（输入即输出）")

    # 普朗克常数几何化 hbar = m c rho（循环）
    hbar_rec = m_e * c * rho_e
    rel_h = abs(hbar_rec - hbar) / hbar
    res("C0008.hbar=m*c*rho", abs(hbar_rec - hbar) / hbar < 1e-12,
        "hbar_rec={0:.6e} 相对误差={1:.2e}".format(hbar_rec, rel_h),
        "循环自证")

    # 元电荷 e = sqrt(4 pi eps0 hbar c kappa/tau)
    # 若几何 alpha=kappa/tau 等同精细结构常数，则 e=sqrt(4pi eps0 hbar c alpha) 为精确恒等式。
    # 实测相对误差 ~3e-10 来自 CODATA 各「精确值」取整不一致（alpha 由 e,h,c,eps0 派生，
    # 与表列 alpha 在 1e-10 量级不闭合），并非真机器零。来源宣称 <1e-14% 夸大。
    e_rec = math.sqrt(4.0 * math.pi * eps0 * hbar * c * (kappa_e / tau_e))
    rel_e = abs(e_rec - e) / e
    res("C0009.e=sqrt(4pi eps0 hbar c kappa/tau)", rel_e < 1e-9,
        "e_rec={0:.6e} 相对误差={1:.2e}（受 CODATA 取整限制，非机器零）".format(e_rec, rel_e),
        "循环自证")

    # 真空介电常数 eps0 = tau/(4 pi c^2 kappa) = 1/(4pi c^2 alpha)
    # 物理正确式应为 eps0 = e^2/(4pi hbar c alpha)，来源式缺 hbar、e^2 因子，不自洽。
    eps0_rec = tau_e / (4.0 * math.pi * c * c * kappa_e)
    rel_eps = abs(eps0_rec - eps0) / eps0
    res("C0010.eps0=tau/(4pi c^2 kappa)", rel_eps < 1e-6,
        "eps0_rec={0:.6e} 真值={1:.6e} 偏差={2:.2e}（公式缺 hbar、e^2 因子，不自洽）".format(eps0_rec, eps0, rel_eps),
        "公式不自洽")

    log("-" * 78)
    log("诚实结论：以上 C0006/C0008/C0009/C0010 的『零误差』来自以")
    log("CODATA 常数为输入反算同一常数，属重参数化而非独立预言。")
    log("C0003/C0001/C0005 为螺旋几何代数恒等式，自洽但不产出新物理。")
    log("=" * 78)

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "..", "..", "09_验证结果", "原始运行记录")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "verify_ct_uft_report.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(OUT_LINES) + "\n")
    log("报告已写入：" + out_path)


if __name__ == "__main__":
    main()
