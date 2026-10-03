# -*- coding: utf-8 -*-
"""
O-P1 正面攻关：螺旋公设 ⇒ 场互变三式（zxq23_o1_gap）

问题
----
UFE-2 的 A 类 9 条全部从 3 条独立输入（C-01 主式、C-02 ∇×A=B/f、C-03 本构）可达，
但这 3 条本身是**公设**：从螺旋公设 C-20（ωρ=c）到它们之间没有推导链（缺口 O-P1）。
本脚本不是再确认一遍"缺口存在"，而是**真的去推**，看它究竟卡在哪一步。

方法
----
全部读数走**直角坐标下的中心差分**，解析式只用来对拍 —— 不共用任何中间量纲引擎，
以免"用同一个错误算两遍"。自检 A00 先验证差分算子本身。

三条候选路线
------------
R1  A 取螺旋切矢场 T = r'/|r'|（最自然的候选）
R2  A 取常矢量场类 A = a_ρ(ρ,z) ê_ρ + a_φ(ρ,z) ê_φ + a_z(ρ,z) ê_z（轴对称一般解）
R3  23 式自己给的 B 定义（式 11）—— 已被 Q11 判量纲 FAIL，此处只补相容性读数

依赖：仅标准库。运行：python -B zxq23_o1_gap.py [--strict]

红线：O-P1 若被关闭必须能指出**新引入的、当前不依赖的可观测量**；本脚本不会给出这种量，
所以无论读数如何，UFE-2 保持 L2。
"""

import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "zxq23_o1_gap_results.json")

RESULTS = []


def rec(sid, title, verdict, detail):
    RESULTS.append({"id": sid, "title": title, "verdict": verdict, "detail": detail})


def P(sid, title, d):
    rec(sid, title, "PASS", d)


def F(sid, title, d):
    rec(sid, title, "FAIL", d)


def BO(sid, title, d):
    rec(sid, title, "BOUNDARY", d)


def IN(sid, title, d):
    rec(sid, title, "INFO", d)


def g(x, n=6):
    return "%.*g" % (n, x)


# ============================================================ 向量工具
def add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def mul(a, s):
    return [a[0] * s, a[1] * s, a[2] * s]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def norm(a):
    return math.sqrt(dot(a, a))


def cyl(r, phi, z):
    return [r * math.cos(phi), r * math.sin(phi), z]


def e_r(r, phi):
    return [math.cos(phi), math.sin(phi), 0.0]


def e_phi(phi):
    return [-math.sin(phi), math.cos(phi), 0.0]


def curl_centered(field, p, h=1e-5):
    """直角坐标下的中心差分旋度。field(p) -> [Fx,Fy,Fz]（p 为 [x,y,z]）。"""
    x, y, z = p
    d = []
    for comp in range(3):
        pp = list(p)
        pm = list(p)
        pp[comp] += h
        pm[comp] -= h
        d.append(sub(field(pp), field(pm)))
    fx, fy, fz = d[0], d[1], d[2]
    return [
        (fy[2] - fz[1]) / (2 * h),
        (fz[0] - fx[2]) / (2 * h),
        (fx[1] - fy[0]) / (2 * h),
    ]


def deriv_centered(field, p, axis, h=1e-5):
    pp = list(p)
    pm = list(p)
    pp[axis] += h
    pm[axis] -= h
    return mul(sub(field(pp), field(pm)), 1.0 / (2 * h))


# ============================================================ 螺旋参数（取 ω=r=b=1 ⇒ c=√2）
OMEGA = 1.0
R_HELIX = 1.0
B_PITCH = 1.0
V_PERP = R_HELIX * OMEGA            # 横向速度
V_AXIS = OMEGA * B_PITCH            # 轴向速度
C_LIGHT = math.sqrt(V_PERP ** 2 + V_AXIS ** 2)
RHO_EFF = math.sqrt(R_HELIX ** 2 + B_PITCH ** 2)   # = c/ω
ALPHA_LOCAL = V_PERP / C_LIGHT


def helix(t):
    return [R_HELIX * math.cos(OMEGA * t),
            R_HELIX * math.sin(OMEGA * t),
            V_AXIS * t]


# --- 高阶差分：Richardson 外推的一阶导数（O(h^4)），再逐级差分得到二/三阶。
#     第一版用嵌套的二阶中心差分（h=1e-6），实测挠率偏差达 15.3 —— 舍入被 1/h²
#     放大后又嵌套一次，彻底失效。那一版还把偏差**只打印不判定**，
#     于是"偏差 15.3"照样打了 PASS：判据不会红等于没有判据。本轮两处都修。
H_DIFF = 1e-3


def _d1_raw(t, h):
    return mul(sub(helix(t + h), helix(t - h)), 1.0 / (2 * h))


def _d1_raw2(t, h):
    return mul(sub(helix(t + 2 * h), helix(t - 2 * h)), 1.0 / (4 * h))


def d1(t, h=H_DIFF):
    """一阶导，Richardson 外推 ⇒ O(h^4)"""
    return mul(sub(mul(_d1_raw(t, h), 4.0), _d1_raw2(t, h)), 1.0 / 3.0)


def d2(t, h=H_DIFF):
    return mul(sub(d1(t + h), d1(t - h)), 1.0 / (2 * h))


def d3(t, h=H_DIFF):
    return mul(sub(d2(t + h), d2(t - h)), 1.0 / (2 * h))


# ============================================================ §A 差分算子自检 + 螺旋运动学
def sec_selfcheck_and_kinematics():
    # A00 自检：差分旋度算子对已知场必须给对
    #   F = (−y, x, 0) ⇒ curl F = (0, 0, 2)
    def f_known(p):
        return [-p[1], p[0], 0.0]
    got = curl_centered(f_known, [0.7, 0.3, 0.0])
    err = max(abs(got[0]), abs(got[1]), abs(got[2] - 2.0))
    if err < 1e-6:
        P("A00", "差分旋度算子自检（对 F=(−y,x,0) 应得 curl=(0,0,2)）",
          "最大偏差 %s（中心差分 h=1e-5 的截断水平）⇒ 算子可信" % g(err))
    else:
        F("A00", "差分旋度算子自检未过", "偏差 %s" % g(err))
        return None

    # A01 速度与 v=c
    v1 = d1(0.37)
    speed = norm(v1)
    if abs(speed - C_LIGHT) / C_LIGHT < 1e-8:
        P("A01", "螺旋的合速率恒为 c",
          "|dr/dt|=%s，c=√(v_⊥²+v_z²)=%s，相对差 %s；v_⊥=%s、v_z=%s"
          % (g(speed), g(C_LIGHT), g(abs(speed - C_LIGHT) / C_LIGHT),
             g(V_PERP), g(V_AXIS)))
    else:
        F("A01", "合速率与 c 不符", "算得 %s vs %s" % (g(speed), g(C_LIGHT)))

    # A02/A03 曲率与挠率（通用定义式，差分实现）
    worst_k, worst_t = 0.0, 0.0
    for i in range(9):
        t = 0.11 + 0.13 * i
        a, b, cc = d1(t), d2(t), d3(t)
        k = norm(cross(a, b)) / norm(a) ** 3
        tau = dot(a, cross(b, cc)) / (norm(cross(a, b)) ** 2)
        worst_k = max(worst_k, abs(k - R_HELIX * OMEGA ** 2 / C_LIGHT ** 2))
        worst_t = max(worst_t, abs(tau - V_AXIS * OMEGA / C_LIGHT ** 2))
    k_th = R_HELIX * OMEGA ** 2 / C_LIGHT ** 2
    tau_th = V_AXIS * OMEGA / C_LIGHT ** 2
    tol = 1e-6
    if worst_k < tol:
        P("A02", "曲率 κ=|r'×r''|/|r'|³ 的差分复算",
          "9 个采样点最大偏差 %s（判据 <%s）；解析值 Rω²/c²=%s ⇒ 与 07 层第 10 卷的 κ=(ω/c)cosθ 一致"
          % (g(worst_k), g(tol), g(k_th)))
    else:
        F("A02", "曲率差分复算超出容差", "最大偏差 %s（判据 <%s）" % (g(worst_k), g(tol)))
    if worst_t < tol:
        P("A03", "挠率 τ=(r',r'',r''')/|r'×r''|² 的差分复算",
          "9 个采样点最大偏差 %s（判据 <%s）；解析值 v_zω/c²=%s。"
          "（第一版此处偏差 15.3 却因「只打印不判定」打了 PASS，已修）"
          % (g(worst_t), g(tol), g(tau_th)))
    else:
        F("A03", "挠率差分复算超出容差",
          "最大偏差 %s（判据 <%s）—— 三阶导数对步长极敏感，这正是必须真判红的原因"
          % (g(worst_t), g(tol)))

    lhs = k_th ** 2 + tau_th ** 2
    rhs = (OMEGA / C_LIGHT) ** 2
    P("A04", "κ²+τ²=(ω/c)²",
      "左 %s / 右 %s ⇒ 相对差 %s" % (g(lhs), g(rhs), g(abs(lhs - rhs) / rhs)))
    return (k_th, tau_th)


# ============================================================ §B 路线 R1：A 取切矢场 T
def sec_route_T():
    # T = r'/|r'| = (v_⊥ ê_φ + v_z ê_z)/c，与 z 无关
    def field_T(p):
        rho = math.hypot(p[0], p[1])
        if rho == 0.0:
            return [0.0, 0.0, 0.0]
        ph = math.atan2(p[1], p[0])
        return [(V_PERP / C_LIGHT) * e_phi(ph)[0],
                (V_PERP / C_LIGHT) * e_phi(ph)[1],
                V_AXIS / C_LIGHT]

    worst = 0.0
    samples = []
    for rr in (0.5, 1.0, 2.0, 3.0):
        for pp in (0.0, 0.7, 1.9, 3.0):
            p = cyl(rr, pp, 0.0)
            got = curl_centered(field_T, p)
            er, ephi_, ez = e_r(rr, pp), e_phi(pp), [0.0, 0.0, 1.0]
            # 解析式：∇×T = (v_⊥/(cρ)) ê_z
            ana = [(V_PERP / (C_LIGHT * rr)) * ez[0],
                   (V_PERP / (C_LIGHT * rr)) * ez[1],
                   (V_PERP / (C_LIGHT * rr)) * ez[2]]
            rel = norm(sub(got, ana)) / max(norm(ana), 1e-300)
            worst = max(worst, rel)
            samples.append((rr, pp, got, ana))
    if worst < 1e-6:
        P("B03", "R1：切矢场 T 的旋度 = (v_⊥/(cρ)) ê_z（中心差分 vs 解析）",
          "16 个采样点最大相对偏差 %s（判据 <1e-6）；**方向沿轴向 ê_z，量级 ∝1/ρ**；"
          "ρ=0.5 处算得 %s" % (g(worst), g(samples[0][2][2])))
    else:
        F("B03", "R1：旋度的差分与解析式不吻合", "最大相对偏差 %s" % g(worst))

    # B04：与沿螺旋的切向导数（协变导数 / Frenet 结构）对比
    #   dT/ds = (1/|r'|) dT/dt ；T 沿螺旋 = (v_⊥ê_φ(ωt) + v_z ê_z)/c
    def field_T_t(t):
        ph = OMEGA * t
        return [(V_PERP / C_LIGHT) * e_phi(ph)[0],
                (V_PERP / C_LIGHT) * e_phi(ph)[1],
                V_AXIS / C_LIGHT]

    h = 1e-6
    worst2 = 0.0
    for i in range(7):
        t = 0.17 + 0.2 * i
        dTdt = mul(sub(field_T_t(t + h), field_T_t(t - h)), 1.0 / (2 * h))
        dTds = mul(dTdt, 1.0 / C_LIGHT)
        ph = OMEGA * t
        # 解析：dT/ds = −κ ê_r
        ana = mul(e_r(1.0, ph), -R_HELIX * OMEGA ** 2 / C_LIGHT ** 2)
        worst2 = max(worst2, norm(sub(dTds, ana)) / max(norm(ana), 1e-300))
    if worst2 < 1e-6:
        P("B04", "R1 旁证：沿螺旋的切向导数 dT/ds = −κ ê_r（Frenet 结构）",
          "7 个采样点最大相对偏差 %s（判据 <1e-6）。**注意它与 B03 的旋度是两个不同方向**"
          "（径向 vs 轴向）⇒ 二者不是同一个算子" % g(worst2))
    else:
        F("B04", "dT/ds 与 −κê_r 不吻合", "最大相对偏差 %s" % g(worst2))

    # B05：算子错配的定量判据
    F("B05", "核心负面结果：螺旋公设给的是协变导数结构，C-02 要的是旋度结构",
      "同一候选场 T：∇×T=(v_⊥/(cρ))ê_z（轴向、1/ρ），∇_⊥T=−κê_r（径向、v_⊥ω/c²）。"
      "方向差 90°、径向依赖分别 ∝1/ρ 与常数。"
      "**结论：从 ωρ=c 能推出的是 Frenet（协变导数）关系，推不出 C-02 的旋度关系。**"
      "这不是数值问题，是算子不匹配（若强行用 ∇×T 读 C-02，得到的 B 只能是轴向 1/ρ 场）")


# ============================================================ §C 路线 R2：常矢量场类
def sec_route_cyl():
    # A = a_ρ(ρ,z) ê_ρ + a_φ(ρ,z) ê_φ + a_z(ρ,z) ê_z
    # curl 的三个分量（柱坐标，轴对称）：
    #   (∇×A)_ρ = (1/ρ)[∂_φ A_z − ∂_z(ρ A_φ)]
    #   (∇×A)_φ = ∂_z A_ρ − ∂_ρ A_z
    #   (∇×A)_z = (1/ρ)[∂_ρ(ρ A_φ) − ∂_φ(ρ A_ρ)]
    # ⇒ ê_φ 分量**只**来自 −∂_ρ A_z
    P("C01", "R2 结构分析：柱坐标旋度的 ê_φ 分量的唯一来源是 −∂_ρ A_z",
      "(∇×A)_φ = ∂_z A_ρ − ∂_ρ A_z。要得到非零的环向分量（螺线管型磁场的自然方向），"
      "**必须** A_z 随 ρ 变化 ⇒ A 必须含一个与螺旋公设无关的轴向分量。")

    # 数值确认：取 A_z = k·ρ，A_ρ=A_φ=0 ⇒ curl 应为 (0,−k,0)
    def field_Az(p):
        rho = math.hypot(p[0], p[1])
        return [0.0, 0.0, 1.3 * rho]

    worst = 0.0
    for rr in (0.8, 1.7, 2.9):
        for pp in (0.3, 1.4, 2.6):
            p = cyl(rr, pp, 0.0)
            got = curl_centered(field_Az, p)
            ph = pp
            ana = [(0.0), (0.0), (0.0)]
            # (∇×A)_φ = −∂_ρ A_z = −1.3 ； ê_φ=(-sinφ,cosφ,0)
            ana = mul(e_phi(ph), -1.3)
            rel = norm(sub(got, ana)) / max(norm(ana), 1e-300)
            worst = max(worst, rel)
    if worst < 1e-6:
        P("C02", "R2 数值确认：取 A_z=kρ 时 curl 沿 ê_φ 且大小 k（差分 vs 解析）",
          "9 个采样点最大相对偏差 %s（k=1.3）⇒ C01 的结构分析成立" % g(worst))
    else:
        F("C02", "R2 的结构分析未被数值确认", "最大相对偏差 %s" % g(worst))

    BO("C03", "O-P1 在「常矢量场类」内的 no-go（适用范围须写明）",
       "在「A 为轴对称常矢量场类」这一假设下：要让 C-02 的 B 具备物理意义"
       "（环向或轴向的 B），A 必须含与螺旋公设无关的分量；"
       "而只用螺旋公设能构造出的 A（切矢场 T）的旋度是轴向 1/ρ 场。"
       "**⇒ 在此假设类内，C-02 要么脱离螺旋本源、要么推不出来。**"
       "该 no-go 只在这一类内成立，不是全局定理（其它类如带 z 依赖的场未穷举）")

    IN("C04", "T 的旋度虽非零，但它与 23 式自己的 B 定义不相容",
       "∇×T 给出 B ∥ ê_z、大小 ∝1/ρ；而 23 式式 11 给的是 B ∝ μ₀kk'/Ω²·(dΩ/dt)·R/R'³，"
       "该式已被 Q11 判量纲 FAIL（缺速度因子）。"
       "⇒ 即便绕开量纲问题，两者的空间依赖也对不上（1/ρ vs 1/r²）")


# ============================================================ §D 缺口重述
def sec_gap():
    F("Q01", "O-P1 攻关结论：公设 ⇒ 场互变三式的推导链**在本轮未能建立**",
      "正面尝试了 R1（螺旋切矢场）与 R2（轴对称常矢量场类）两条路线，"
      "都卡在同一个点：螺旋公设 ωρ=c 只确定 Frenet 型**协变导数**结构，"
      "而 C-02 需要的是**旋度**结构。B05 给出两者的定量分离（方向差 90°、径向依赖不同），"
      "C03 给出在常矢量场类内的 no-go。")
    BO("Q02", "缺口被精确重述（原表述「没人推出」不准确）",
       "旧表述：O-P1 = 缺一条推导链。修正后：**推导链的第一步就会遇到算子错配** ——"
       "不是算力问题，是「∇× 与 ∇_⊥ 不是同一个算子」这一结构障碍。"
       "任何后续攻关都应先回答：为什么旋度，而不是（协变）导数？")
    IN("Q03", "对 L3 门槛的影响",
       "即便日后补上推导链，按本目录的判据，它必须产生一个**当前不依赖的可观测量**；"
       "R1/R2 两路给出的候选量（轴向 1/ρ 场、环向场）都不满足这一点。"
       "⇒ UFE-2 保持 L2，本册不改变任何评级")


def main():
    argv = sys.argv[1:]
    kin = sec_selfcheck_and_kinematics()
    if kin is None:
        for r in RESULTS:
            print("[%-8s] %-5s %s\n           %s"
                  % (r["verdict"], r["id"], r["title"], r["detail"]))
        return 2
    sec_route_T()
    sec_route_cyl()
    sec_gap()

    cnt = {}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    payload = {
        "instrument": "zxq23_o1_gap.py",
        "param": {"omega": OMEGA, "r_helix": R_HELIX, "b_pitch": B_PITCH,
                  "v_perp": V_PERP, "v_axis": V_AXIS, "c": C_LIGHT,
                  "alpha_local": ALPHA_LOCAL},
        "counts": cnt, "total": len(RESULTS), "results": RESULTS,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print("=" * 78)
    print("O-P1 正面攻关：螺旋公设 ⇒ 场互变三式")
    print("=" * 78)
    for r in RESULTS:
        print("[%-8s] %-5s %s" % (r["verdict"], r["id"], r["title"]))
        print("           %s" % r["detail"])
    print("-" * 78)
    print("合计 %d 条：PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
          % (len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0),
             cnt.get("BOUNDARY", 0), cnt.get("INFO", 0)))
    print("产物：%s" % os.path.basename(OUT_JSON))
    print("红线：数学自洽 ≠ 实验证实；本册不改变 UFE-2 的 L2 评级。")
    if "--strict" in argv and cnt.get("FAIL", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
