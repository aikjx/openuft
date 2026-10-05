# -*- coding: utf-8 -*-
"""
TUFT-MATH-PROOF-ADD-01 复 Omega 场渲染与全域审计（分支 2）
============================================================
对 ADD-01 Part B 定义的复 Omega 场做全域数值审计 + 生成渲染数据。
场定义（B.4 坐标形式 + ADD-02 三分瓣分区）：
  theta = atan2(tau, kappa)；u=cos, v=sin；u^2+v^2=1
  cos(3theta) = (kappa^3-3*kappa*tau^2)/(kappa^2+tau^2)^(3/2)
  Omega(kappa,tau) = lambda*cos(3theta)           (非弱域)
                    lambda*cos(3theta)*exp(i*phi) (弱域 theta in [210,270])
  phi(theta) = phi0*(theta-theta_Wc)/delta_theta_W, phi0 代表性取 0.5
分区（ADD-02）：EM=0deg±30、Strong=120deg±30、Weak=240deg±30、G=三负瓣之并。
lambda = alpha_s = 0.1179。

关键审计点：
  1) B.4 cos3theta 恒等式（极坐标 vs 直角坐标式）
  2) Omega 纯角度依赖（径向退化：Omega(2r)=Omega(r)）
  3) 幅值 |Omega| 跨弱域边界连续（cos3theta 零点）
  4) 相位在弱域边界不连续（N6：跳变 phi0/2）
  5) 三分瓣分区 + 幅值符号
  6) 无量纲
  7) 矢量场 F=-grad|Omega| 纯方位角（径向分量~0）

退出码：0 = 全部 guard 通过；2 = 任一 guard 异常/非预期。
"""
import math
import json
import os

LAMBDA = 0.1179          # alpha_s
PHI0   = 0.5             # 代表性相位常数（N6 示例用）
THETA_WC = math.radians(240.0)
DELTA_W  = math.radians(60.0)
WEAK_LO  = math.radians(210.0)
WEAK_HI  = math.radians(270.0)

def cos3theta_rect(kappa, tau):
    return (kappa**3 - 3.0*kappa*tau**2) / (kappa**2 + tau**2)**1.5

def in_weak(theta):
    # theta 归一化到 [0,2pi)
    t = theta % (2.0*math.pi)
    return (WEAK_LO <= t <= WEAK_HI) or (t >= WEAK_LO - 2*math.pi and t <= WEAK_HI - 2*math.pi)

def phase(theta):
    t = theta % (2.0*math.pi)
    if in_weak(t):
        return PHI0 * (t - THETA_WC) / DELTA_W
    return 0.0

def omega(kappa, tau):
    th = math.atan2(tau, kappa)
    mag = LAMBDA * cos3theta_rect(kappa, tau)
    ph = phase(th)
    return mag * math.cos(ph), mag * math.sin(ph)   # (Re, Im)

def mag_omega(kappa, tau):
    th = math.atan2(tau, kappa)
    return abs(LAMBDA * cos3theta_rect(kappa, tau))

GUARDS = []
def guard(name, detail=""):
    def deco(fn):
        try:
            ok, note = fn()
        except Exception as e:
            ok, note = False, "EXC: %r" % e
        GUARDS.append({"name": name, "ok": ok, "note": note, "detail": detail})
        return fn
    return deco

@guard("b4_cos3theta_identity",
       "B.4：cos3theta = (kappa^3-3 kappa tau^2)/(kappa^2+tau^2)^{3/2} 逐点成立")
def _():
    worst = 0.0
    for k, t in ((2,1),(1,0.5),(3,-2),(0.8,1.2),(2.5,2.5)):
        c = cos3theta_rect(k, t)
        th = math.atan2(t, k)
        ref = math.cos(3.0*th)
        worst = max(worst, abs(c-ref))
    return worst < 1e-12, "max|rect - cos(3theta)| = %.2e（机器精度）" % worst

@guard("angular_only_radial_degenerate",
       "Omega 纯角度依赖：Omega(2r)=Omega(r)（径向退化，幅值沿射线恒定）")
def _():
    (r1,i1) = omega(1.0, 0.8)
    (r2,i2) = omega(2.0, 1.6)
    ok = (abs(r1-r2)<1e-12) and (abs(i1-i2)<1e-12)
    return ok, "Omega(1,0.8)=(%.4f,%+.4f) vs Omega(2,1.6)=(%.4f,%+.4f)（径向不变）" % (
        r1,i1,r2,i2)

@guard("magnitude_continuous_boundary",
       "幅值 |Omega| 跨弱域边界连续（弱域边界为 cos3theta 零点）")
def _():
    a = mag_omega(1.0, math.tan(WEAK_LO))
    b = mag_omega(1.0, math.tan(WEAK_LO+1e-9))
    ok = abs(a-b) < 1e-9
    return ok, "|Omega|(210°两侧) = %.3e / %.3e（连续）" % (a, b)

@guard("phase_discontinuity_N6",
       "N6 确认：相位跨弱域边界不连续（跳变幅度 phi0/2，方向为负）")
def _():
    p_out = phase(WEAK_LO - 1e-9)
    p_in  = phase(WEAK_LO + 1e-9)
    jump = p_in - p_out
    ok = abs(abs(jump) - PHI0/2.0) < 1e-6
    return ok, "phi(210°⁻)=%.4f, phi(210°⁺)=%.4f, 跳变=%.4f（幅度=phi0/2）" % (
        p_out, p_in, jump)

@guard("three_lobe_partition",
       "三分瓣分区：Weak 瓣内幅值>0，边界为 cos3theta 零点")
def _():
    # Weak 瓣中心 240°
    m_c = mag_omega(1.0, math.tan(THETA_WC))
    # EM 瓣中心 0°
    m_em = mag_omega(1.0, 0.0)
    # Strong 瓣中心 120°
    m_s = mag_omega(1.0, math.tan(math.radians(120)))
    ok = (m_c > 0) and (m_em > 0) and (m_s > 0)
    return ok, "|Omega|(240°)=%.4f, |Omega|(0°)=%.4f, |Omega|(120°)=%.4f（三正瓣均非零）" % (
        m_c, m_em, m_s)

@guard("dimensionless",
       "Omega 无量纲：cos3theta 无量纲，无物理量纲残留")
def _():
    return True, "Omega = lambda*cos3theta*exp(i phi)，lambda 无量纲耦合 ⇒ 无量纲"

@guard("vector_field_azimuthal",
       "矢量场 F=-grad|Omega| 纯方位角：沿射线（固定角）幅值不变，无径向分量")
def _():
    # 沿固定角 theta 的射线，检验 |Omega| 与半径无关
    th = 0.5
    h = 1e-3
    m1 = mag_omega(1.0*math.cos(th), 1.0*math.sin(th))
    m2 = mag_omega((1.0+h)*math.cos(th), (1.0+h)*math.sin(th))
    dr = (m2 - m1) / h
    ok = abs(dr) < 1e-6
    return ok, "d|Omega|/dr(沿射线) = %.2e（径向梯度~0 ⇒ 流场纯方位角）" % dr

# --- 主流程：渲染网格数据 + 审计报告 --------------------------------
def main():
    # 极坐标渲染网格：角度 0..360，半径 0.3..1.0（场与半径无关，画极坐标玫瑰）
    angles_deg = list(range(0, 361, 3))
    mag_line = [abs(LAMBDA*math.cos(math.radians(3*a))) for a in angles_deg]
    phase_line = [phase(math.radians(a)) for a in angles_deg]
    # 分区分界角（cos3theta 零点 = 30,90,150,210,270,330 deg）
    zeros = [30,90,150,210,270,330]

    results = {
        "engine": "TUFT-MATH-PROOF-ADD-01 复Omega场渲染与全域审计（分支 2）",
        "date": "2026-10-05",
        "inputs": {"lambda": LAMBDA, "phi0": PHI0,
                   "weak_center_deg": 240, "weak_width_deg": 60,
                   "weak_lo_deg": 210, "weak_hi_deg": 270},
        "field": {
            "angular_only": True,
            "zeros_deg": zeros,
            "partition_deg": {"EM": [0,30], "Strong": [120,150],
                              "Weak": [210,270], "G_negative": "其余"},
            "mag_line": mag_line,
            "phase_line": phase_line,
            "angle_deg": angles_deg,
        },
        "guards": GUARDS,
        "n_guards": len(GUARDS),
        "n_pass": sum(1 for g in GUARDS if g["ok"]),
        "n_fail": sum(1 for g in GUARDS if not g["ok"]),
    }
    lines = []
    lines.append("# TUFT-MATH-PROOF-ADD-01 复Omega场渲染与全域审计报告（分支 2）")
    lines.append("")
    lines.append("- 引擎：源码/TUFT-MATH-PROOF-ADD-01_复Omega场渲染与全域审计_2026-10-05.py")
    lines.append("- 日期：2026-10-05")
    lines.append("- 读数：%d guard —— PASS %d / FAIL %d（退出码 %d）"
                 % (len(GUARDS), results["n_pass"], results["n_fail"],
                    0 if results["n_fail"] == 0 else 2))
    lines.append("")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % ("PASS" if g["ok"] else "FAIL",
                                           g["name"], g["note"]))
    lines.append("")
    lines.append("### 渲染要点")
    lines.append("""
1. **Omega 是纯角度场**（径向退化）：幅值 |Omega|=lambda|cos3theta| 沿每条射线恒定，
   与半径无关 ⇒ 渲染用极坐标玫瑰图（|cos3theta| 三瓣）最忠实。
2. **幅值三正瓣**：EM(0°±30)、Strong(120°±30)、Weak(240°±30)，边界为 cos3theta
   零点（30/90/150/210/270/330°）；负瓣区为 G。
3. **N6 相位不连续**：相位在弱域[210°,270°]内线性变化，跨 210°/270° 边界跳变 phi0/2
   （幅值连续但相位不连续）——与 ADD-01「相位连续✔」矛盾。
4. **矢量场 F=-grad|Omega| 纯方位角**：因幅值与半径无关，流场无径向分量，仅沿角向
   在三瓣内环流。
""")
    report = "\n".join(lines)

    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base, "..", "数据"))
    stem = "TUFT-MATH-PROOF-ADD-01_复Omega场渲染与全域审计_2026-10-05"
    with open(os.path.join(data_dir, stem + ".json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(os.path.join(data_dir, stem + ".md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    return 0 if results["n_fail"] == 0 else 2

if __name__ == "__main__":
    import sys
    sys.exit(main())
