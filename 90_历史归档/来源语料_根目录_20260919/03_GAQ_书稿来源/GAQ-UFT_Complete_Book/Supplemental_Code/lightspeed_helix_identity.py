"""
GAQ-UFT 审计延伸：光速螺旋本源假说 (v_total = c) 的独立验证
假设："空间是匀速 c 前进的圆柱螺旋真空；曲率κ、挠率τ与频率ω由 κ²+τ²=(ω/c)² 锁定"
本脚本独立复算该恒等式，并检验它能否真正闭合 α 与 G（还是只是把尺度问题换个包装）。
"""
import mpmath as mp

mp.mp.dps = 80

REC = []


def record(tag, verdict, detail):
    REC.append({"tag": tag, "verdict": verdict, "detail": detail})
    print(f"[{verdict}] {tag}\n      {detail}\n")


# 常量
c = mp.mpf("299792458")
alpha = mp.mpf("1") / mp.mpf("137.035999084")
G_COD = mp.mpf("6.67430e-11")
m_e = mp.mpf("9.1093837015e-31")
hb = mp.mpf("1.054571817e-34")
l_P = mp.sqrt(hb * G_COD / c ** 3)
m_P = mp.sqrt(hb * c / G_COD)


def helix_geom(R, b):
    """螺旋 r(t)=(R cos ωt, R sin ωt, b·ω t)，返回 κ,τ,以及满足 |dr/dt|=c 的 ω"""
    denom = R ** 2 + b ** 2
    kappa = R / denom
    tau = b / denom
    # |dr/dt| = ω·sqrt(R²+b²) = c  ⇒  ω = c/sqrt(R²+b²)
    omega = c / mp.sqrt(denom)
    return kappa, tau, omega


def test_identity():
    """检验 κ²+τ² = ω²/c² 对所有 (R,b) 是否成立"""
    ok_all = True
    worst = mp.mpf("0")
    for (R, b) in [(mp.mpf("1"), mp.mpf("0.5")),
                   (mp.mpf("2"), mp.mpf("3")),
                   (mp.mpf("0.3"), mp.mpf("10")),
                   (mp.mpf("1.0e-35"), mp.mpf("1.0e-35"))]:
        kappa, tau, omega = helix_geom(R, b)
        lhs = kappa ** 2 + tau ** 2
        rhs = (omega ** 2) / (c ** 2)
        rel = abs(lhs - rhs) / rhs
        worst = max(worst, rel)
        if rel > mp.mpf("1e-60"):
            ok_all = False
    record("I-1 光速螺旋恒等式 κ²+τ²=(ω/c)²",
           "PASS" if ok_all else "FAIL",
           f"对任意 (R,b) 恒等成立，最大相对偏差 = {float(worst):.2e}（纯几何结论，合法）")


def test_pitch_and_alpha():
    """固定 tanθ=τ/κ=α，检验尺度自由度 b 是否能被确定"""
    theta = mp.atan(alpha)          # θ = atan α （框架定义）
    # tanθ = b/R = α  ⇒ R = b/α
    R = mp.mpf("1") / alpha          # 取 b=1 单位
    b = mp.mpf("1")
    kappa, tau, omega = helix_geom(R, b)
    # 频率
    f_hz = omega / (2 * mp.pi)
    record("I-2 螺距角 → α",
           "PASS",
           f"tanθ=b/R={float(tau/kappa):.6e}  vs α={float(alpha):.6e}（一致，已知结果）")
    record("I-3 曲率/挠率的绝对尺度由 b 决定",
           "OPEN",
           f"b=1(单位) ⇒ κ={float(kappa):.4e}, τ={float(tau):.4e}, f={float(f_hz):.4e} Hz；"
           f"b 本身是自由参数，几何无法独立确定其量纲尺度")


def test_scale_contradiction():
    """致命点：同一 κ 要同时满足 ℏ=mc/κ(电子尺度) 与 G=c³/(ℏ(κ²+τ²))(普朗克尺度)？
    在 v=c 约束下 κ²+τ²=ω²/c²，把 ω 反解代入看两处 κ 是否相容"""
    # 方案A：从电子康普顿 ℏ = m_e c / κ  ⇒ κ_A = m_e c / ℏ
    kappa_A = m_e * c / hb
    # 方案B：从 G = c³/(ℏ(κ²+τ²)) 且 κ²+τ²=ω²/c²；若 ω 来自某 b，则 κ_B 需 ≈ 1/l_P 量级
    kappa_B = mp.mpf("1") / l_P
    ratio = kappa_B / kappa_A
    record("I-4 κ 尺度矛盾（v=c 下仍存在）",
           "BUG" if ratio > mp.mpf("1e10") else "OK",
           f"电子尺度 κ_A={float(kappa_A):.3e} m⁻¹ vs 普朗克尺度 κ_B={float(kappa_B):.3e} m⁻¹ "
           f"⇒ 相差 {float(ratio):.2e} 倍；v=c 恒等式不消除该矛盾（b 仍需两选一）")


def test_g_prediction():
    """若强行令 κ=κ_B(普朗克) 并取框架 G=c³/(ℏ(κ²+τ²))，是否=CODATA？"""
    # 取 b 使 κ=κ_B：由 κ=R/(R²+b²), b/R=α ⇒ 解出 b ≈ α/κ_B ... 直接验证 G 公式
    R = mp.mpf("1") / alpha
    b = mp.mpf("1")
    kappa, tau, omega = helix_geom(R, b)
    G_cand = c ** 3 / (hb * (kappa ** 2 + tau ** 2))
    # 注意：此 G_cand 用 b=1(单位) 的 κ，必然是乱的；正确套代须 b=l_P 量级
    record("I-5 G 候选公式需 b=普朗克尺度才≈CODATA",
           "OPEN",
           f"b=1 ⇒ G_cand={float(G_cand):.3e}（离谱）；"
           f"只有当 b≈l_P 时 κ²+τ²≈1/l_P² ⇒ G_cand→G_COD（构造套代，非独立预测）")


if __name__ == "__main__":
    test_identity()
    test_pitch_and_alpha()
    test_scale_contradiction()
    test_g_prediction()
    import json
    with open("lightspeed_helix_results.json", "w", encoding="utf-8") as f:
        json.dump(REC, f, ensure_ascii=False, indent=2, default=lambda o: float(o) if isinstance(o, mp.mpf) else str(o))
    n_pass = sum(1 for r in REC if r["verdict"] == "PASS")
    n_open = sum(1 for r in REC if r["verdict"] == "OPEN")
    n_bug = sum(1 for r in REC if r["verdict"] == "BUG")
    print(f"\n=== 汇总：PASS={n_pass} OPEN={n_open} BUG={n_bug} ===")
