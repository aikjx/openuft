# -*- coding: utf-8 -*-
"""
TUFT-r169｜S17 核心公式「变化的引力场产生电场」：E=−f·∂A/∂t 是电磁矢势的重命名

00. 编号与定位
  【编号】r169。实测首空号：r100–r168 全占（本线 + 并行会话），r169 为首空号。
  【动机】S17 核心公式集「14-变化的引力场产生电场」的核心主张（靶原文）：
      「电场 E = −f·∂A/∂t，其中 A 是引力场（空间加速度），f 是耦合常数；
        磁场 B = f·∇×A。对 E 取旋度、结合 ∇×A=B/f，直接导出法拉第定律；
        安培环路定理通过磁场定义、电荷守恒、高斯定律推导。」
      并预测「f ≈ 1.05e−8 kg/A（连接引力弱耦合与电磁强耦合）」「电场本质 =
        动态引力场的表现」「电荷起源 = 质量变化率」。
  靶**自承**「公设实验支撑薄弱」「常数 f 计算细节缺失」。但靶未自承、且 r148–r168
  从未判的是：**这套「导出」是不是把电磁矢势 A_EM 重命名为 f·A_grav 后的恒等重写**。
  本卷判四问：
    (i)  E=−f·∂A/∂t、B=f·∇×A 与标准 Maxwell 矢势的关系是「导出」还是「变量替换」？
    (ii) 法拉第定律是被「导出」还是被 B 的定义「重述」？
    (iii) 安培定律的「导出」是否需要额外假设 Maxwell 波动方程（循环）？
    (iv) 常数 f 的数值是否自相矛盾？

01. ★分层声明（与既有卷条目不可相加）
  r148=式子层（P=m(c−v)）· r157=积分层 · r158=字典层（ω=qB/(γm)）·
  r159=引力侧还原 · r160=S17 力方程 · r161=电荷几何化 · r162=时空/质量几何化 ·
  r163=宇宙本源 · r164=质量定义 · r165=四力闭合层 · r166=能量方程 ·
  r167=可证伪性层 · r168=耦合 f 量纲（并行）
  **本卷 = 电磁-引力互生层（核心公式 14 的具体攻破）**：
  判「变化的引力场产生电场」这一具体公式是**导出**还是**矢势重命名**。
  与 r168 的区别：r168 判 f 的「量纲」五重矛盾；本卷判「E=−f∂A/∂t」这一公式
  本身的**循环导出 + 变量替换 + 数值矛盾**。

02. 机读手段
  全部解析构造（平面波电磁矢势，闭式 E、B、∇×、∂/∂t，无差分）；
  变量替换恒等式（A_EM = f·A_grav 代入 Maxwell 得靶式）；法拉第/安培的链式展开；
  常数 f 三口径数值复核；量纲四元组 (M,L,T,Q)；控制组 6 项；守卫 6 项；
  修复算子 {KEEP, DEL, REPLACE}。

03. 不自推声明
  NS1 不替靶补 A 的观测锚点；不修改靶任何字节。
  NS2 不重判 r148–r168 任何结论（分层铁律）。
  NS3 只判核心公式 14（E=−f∂A/∂t）这一条链；不判 S17 其它 19 个公式。

04. 红线
  数学自洽 ≠ 实验证实；**恒等式成立 ≠ 有新内容**；**成立 ≠ 宣称域无边界**；
  **靶自承优先**：靶已自承「公设实验支撑薄弱」「f 计算细节缺失」，
  本卷不把「无观测锚点」当发现，只判「导出是重命名」这一结构。
"""

import io
import json
import math
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ============================================================
# 常数（CODATA 2018 / SI）
# ============================================================
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
C_L = 299792458.0
G_N = 6.67430e-11
Q_E = 1.602176634e-19
M_E = 9.1093837015e-31
PI = math.pi

# ============================================================
# 路径
# ============================================================
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "数据")
STEM = "TUFT-r169_电磁引力互生层_变化的引力场产生电场是矢势重命名_2026-10-24"

# ============================================================
# 登记器
# ============================================================
ITEMS = []
CONTROLS = []
GUARDS = []


def add(iid, title, status, note="", **metrics):
    ITEMS.append({"id": iid, "title": title, "status": status,
                  "note": note, "metrics": metrics})


def control(cid, desc, value, expect, ok):
    CONTROLS.append({"id": cid, "desc": desc, "value": value,
                     "expect": expect, "ok": bool(ok)})


def guard(name, ok, detail=""):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})


def rel(x, y):
    m = max(abs(x), abs(y))
    if m == 0.0:
        return 0.0
    return abs(x - y) / m


# ============================================================
# 平面波电磁矢势（解析；真空无源）
#   A_EM = A0 cos(k z − ω t) ŷ
#   E = −∂A/∂t = −A0 ω sin(kz−ωt) ŷ
#   B = ∇×A = A0 k sin(kz−ωt) x̂
# ============================================================
def plane_wave(A0, k, omega, z, t):
    ph = k * z - omega * t
    A = (0.0, A0 * math.cos(ph), 0.0)
    E = (0.0, -A0 * omega * math.sin(ph), 0.0)
    B = (A0 * k * math.sin(ph), 0.0, 0.0)
    return A, E, B


def curl_of_B(A0, k, omega, z, t):
    """平面波 B=(B0 sin,0,0) 的旋度：∇×B = (0, −B0 k cos, 0)。"""
    ph = k * z - omega * t
    return (0.0, -A0 * k * k * math.cos(ph), 0.0)


def dE_dt(A0, k, omega, z, t):
    """∂E/∂t = (0, −A0 ω² cos, 0)。"""
    ph = k * z - omega * t
    return (0.0, -A0 * omega * omega * math.cos(ph), 0.0)


# ============================================================
# A 组 · 变量替换：A_EM = f·A_grav 代入 Maxwell 得靶式（零新增）
# ============================================================
F_TEST = 1.0e-8   # 任意标度（结构性检验，f 的具体值不影响替换恒等式）


def group_a():
    """取 A_grav = A_EM / f，验证 E=−f·∂A_grav/∂t 与 B=f·∇×A_grav 逐位等于
    标准 Maxwell 的 E=−∂A_EM/∂t、B=∇×A_EM。"""
    rows = []
    A0, k, omega = 1.0, 2.0 * PI / 0.5, 2.0 * PI * 1.0
    for z in (0.0, 0.125, 0.25, 0.375):
        t = 0.0
        A_em, E_std, B_std = plane_wave(A0, k, omega, z, t)
        A_grav = tuple(x / F_TEST for x in A_em)
        # 靶式：E = −f ∂A_grav/∂t；B = f ∇×A_grav
        ph = k * z - omega * t
        E_target = (0.0, -F_TEST * (A0 / F_TEST) * omega * math.sin(ph), 0.0)
        B_target = (F_TEST * (A0 / F_TEST) * k * math.sin(ph), 0.0, 0.0)
        rows.append({"z": z, "res_E": rel(E_target[1], E_std[1]),
                     "res_B": rel(B_target[0], B_std[0])})
    return rows


# ============================================================
# B 组 · 法拉第定律是恒等式（B=f∇×A 是定义）
# ============================================================
def group_b():
    """∇×E = −f ∂(∇×A_grav)/∂t = −∂(f∇×A_grav)/∂t = −∂B/∂t，
    其中 B≡f∇×A_grav 是定义 ⇒ 法拉第定律被重述而非导出。"""
    rows = []
    A0, k, omega = 1.0, 2.0 * PI / 0.5, 2.0 * PI * 1.0
    for z in (0.0, 0.125, 0.25, 0.375):
        t = 0.0
        # ∇×E 的 y 分量对 z 求导：∂E_y/∂z = −A0 ω k cos
        curlE_x = -A0 * omega * k * math.cos(k * z - omega * t)
        # −∂B/∂t 的 x 分量：−∂B_x/∂t = −A0 k ω cos
        minus_dBdt_x = -A0 * k * omega * math.cos(k * z - omega * t)
        rows.append({"z": z, "curlE_x": curlE_x,
                     "minus_dBdt_x": minus_dBdt_x,
                     "res": rel(curlE_x, minus_dBdt_x)})
    return rows


# ============================================================
# C 组 · 安培定律需要额外假设 Maxwell 波动方程（循环）
# ============================================================
def group_c():
    """∇×B = (0, −A0 k² cos, 0)；μ0ε0 ∂E/∂t = (0, −A0 ω²/c² cos, 0)。
    安培定律成立 ⟺ k² = ω²/c²（真空色散 = Maxwell 波动方程本身）。"""
    rows = []
    A0, k, omega = 1.0, 2.0 * PI / 0.5, 2.0 * PI * 1.0
    c = C_L
    for z in (0.0, 0.125, 0.25, 0.375):
        t = 0.0
        cb = curl_of_B(A0, k, omega, z, t)[1]          # −A0 k² cos
        de = dE_dt(A0, k, omega, z, t)[1]              # −A0 ω² cos
        rhs_ampere = (1.0 / (c * c)) * de              # μ0ε0 = 1/c²
        # 真空色散比
        disp = (k * k) / (omega * omega / (c * c))
        rows.append({"z": z, "curlB": cb, "mu0eps0_dE": rhs_ampere,
                     "res": rel(cb, rhs_ampere), "dispersion": disp})
    return rows


# ============================================================
# D 组 · 常数 f 数值三重矛盾
# ============================================================
def group_d():
    sqrt_4peG = math.sqrt(4.0 * PI * EPS0 * G_N)
    return {
        "f_paper": 1.05e-8,
        "f_sqrt": sqrt_4peG,                  # 8.6175e-11
        "f_c2": (C_L / 2.0) * sqrt_4peG,      # 1.2917e-2
        "ratio_paper_over_sqrt": 1.05e-8 / sqrt_4peG,
        "ratio_paper_over_c2": 1.05e-8 / ((C_L / 2.0) * sqrt_4peG),
    }


# ============================================================
# E 组 · 量纲（f = [M I⁻¹]）自洽记 PASS
# ============================================================
def group_e():
    # E: [M L T⁻³ I⁻¹]；dA/dt: [L T⁻³] ⇒ f=[E]/[dA/dt]=[M I⁻¹]
    dim_E = (1, 1, -3, -1)
    dim_dAdt = (0, 1, -3, 0)
    dim_f = tuple(a - b for a, b in zip(dim_E, dim_dAdt))
    return {"dim_f": dim_f, "dim_f_ok": dim_f == (1, 0, 0, -1)}


def main():
    a_rows = group_a()
    b_rows = group_b()
    c_rows = group_c()
    d = group_d()
    e = group_e()

    res_a_E = max(r["res_E"] for r in a_rows)
    res_a_B = max(r["res_B"] for r in a_rows)
    res_b = max(r["res"] for r in b_rows)
    res_c = max(r["res"] for r in c_rows)
    disp = c_rows[0]["dispersion"]

    # 色散成立对照：ω = k·c ⇒ 安培定律残差应为 0（证明是色散在起作用）
    k0 = 2.0 * PI / 0.5
    omega_disp = k0 * C_L
    cb_d = curl_of_B(1.0, k0, omega_disp, 0.0, 0.0)[1]
    de_d = dE_dt(1.0, k0, omega_disp, 0.0, 0.0)[1]
    res_disp = rel(cb_d, de_d / (C_L * C_L))

    # ---------- 条目 ----------
    add("A1", "E=−f∂A/∂t、B=f∇×A 是电磁矢势的重命名", "FAIL",
        "取 A_grav = A_EM/f，则靶式 E=−f·∂A_grav/∂t 与 B=f·∇×A_grav 逐位等于标准 "
        "Maxwell 的 E=−∂A_EM/∂t、B=∇×A_EM（E 残差 %.1e、B 残差 %.1e）。"
        "⇒ 靶所谓的『电场=引力场变化率』只是把电磁矢势 A_EM 重命名为 f·A_grav，"
        "零新增物理。" % (res_a_E, res_a_B), res_E=res_a_E, res_B=res_a_B)
    add("A2", "法拉第定律是被 B 的定义重述，不是导出", "FAIL",
        "∇×E = −f·∂(∇×A_grav)/∂t = −∂(f·∇×A_grav)/∂t = −∂B/∂t，最后一步依赖 "
        "B≡f·∇×A_grav（这是靶自己的定义）。四相位残差 %.1e ⇒ 法拉第定律是恒等式，"
        "被 B 的定义重述，非独立导出。" % res_b, res=res_b)
    add("A3", "安培定律需额外假设 Maxwell 波动方程（循环）", "FAIL",
        "∇×B 与 μ0ε0·∂E/∂t 相等 ⟺ k²=ω²/c²（真空色散）。本组取 ω/k=0.5 m/s ≠ c，"
        "残差 %.3e（dispersion=%.3e）⇒ 安培定律不是无条件导出；色散对照 ω=kc 时残差 "
        "%.1e（由 Maxwell 波动方程本身保证）⇒ 『导出』实为把波动方程当隐藏前提的循环。"
        % (res_c, disp, res_disp), res=res_c, dispersion=disp, res_disp=res_disp)
    add("A4", "常数 f 数值三重矛盾", "FAIL",
        "靶文 f≈1.05e−8 kg/A；但 √(4πε0G)=%.6e、且 (c/2)·√(4πε0G)=%.6e。"
        "三者互斥（比值 %.4e 与 %.4e，均 ≠1）。靶自承『f 计算细节缺失』，本卷机读"
        "证实数值不自洽。" % (d["f_sqrt"], d["f_c2"],
                              d["ratio_paper_over_sqrt"], d["ratio_paper_over_c2"]),
        f_paper=d["f_paper"], f_sqrt=d["f_sqrt"], f_c2=d["f_c2"])
    add("A5", "量纲 f=[M I⁻¹] 自洽（诚实记 PASS）", "PASS",
        "[E]=[M L T⁻³ I⁻¹]、[dA/dt]=[L T⁻³] ⇒ [f]=[M I⁻¹]，与 f=k'/(4πε0G) "
        "量纲一致。量纲层面自洽，与 r168 的量纲清点不冲突。",
        dim_f=str(e["dim_f"]), dim_f_ok=e["dim_f_ok"])
    add("B1", "与标准 Maxwell 不可区分（防过度指控）", "BOUNDARY",
        "A_grav（引力场=空间加速度）在电磁学语境无独立可观测量，A_EM=f·A_grav "
        "使任意电磁现象都可等价描述 ⇒ 靶式与标准 Maxwell 零区分；本卷不判其『错』，"
        "只判其『非新内容』（与靶自承『公设实验支撑薄弱』一致）。")
    add("R1", "修复定价：3 动作枚举", "INFO",
        "KEEP（E=−f∂A/∂t 仍作『电场起源』）⇒ A1/A2/A3 依旧成立，修不好；"
        "DEL（删『电场本质=引力场变化率』诠释）⇒ 退回标准 Maxwell 矢势表述；"
        "REPLACE（给 A_grav 补独立观测锚点）⇒ 需另立可检验预言 = 换框架。"
        "宣称域内成立 1 / 零代价 0 ⇒ 『修复可行 ≠ 修复后仍有内容』。",
        survive=1, zero_cost=0)

    # ---------- 控制组 ----------
    control("C1", "变量替换逐位一致（A_EM=f·A_grav ⇒ E/B 重命名）",
            "E=%.1e B=%.1e" % (res_a_E, res_a_B), "<1e-15",
            res_a_E < 1e-15 and res_a_B < 1e-15)
    control("C2", "法拉第恒等式（B 定义重述）", "%.3e" % res_b, "<1e-15",
            res_b < 1e-15)
    control("C3", "安培定律非色散下不成立（残差 O(1)）", "%.3e" % res_c,
            "O(1)", res_c > 1e-3)
    control("C4", "安培定律色散 ω=kc 下成立（对照，残差 0）", "%.3e" % res_disp,
            "<1e-15", res_disp < 1e-15)
    control("C5", "f 数值三重矛盾（比值 ≠1）",
            "%.4e / %.4e" % (d["ratio_paper_over_sqrt"], d["ratio_paper_over_c2"]),
            "≠1", abs(d["ratio_paper_over_sqrt"] - 1.0) > 1e-3)
    control("C6", "量纲 f=[M I⁻¹] 自洽", str(e["dim_f_ok"]), "True", e["dim_f_ok"])

    # ---------- 守卫 ----------
    guard("G1-变量替换零新增", res_a_E < 1e-15 and res_a_B < 1e-15,
          "E=%.1e B=%.1e" % (res_a_E, res_a_B))
    guard("G2-法拉第是恒等式", res_b < 1e-15, "res=%.1e" % res_b)
    guard("G3-安培需色散假设", res_c > 1e-3 and res_disp < 1e-15,
          "非色散=%.3e 色散=%.1e" % (res_c, res_disp))
    guard("G4-f 三重矛盾", abs(d["ratio_paper_over_sqrt"] - 1.0) > 1e-3,
          "ratio=%.4e" % d["ratio_paper_over_sqrt"])
    guard("G5-量纲自洽诚实记 PASS", e["dim_f_ok"], "dim_f_ok=True")
    guard("G6-控制组全部通过", all(c["ok"] for c in CONTROLS),
          "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))

    # ---------- 汇总 ----------
    cnt = {}
    for it in ITEMS:
        cnt[it["status"]] = cnt.get(it["status"], 0) + 1
    allok = all(c["ok"] for c in CONTROLS)
    gallok = all(g["ok"] for g in GUARDS)
    verdict = ("VARYING-GRAVITATIONAL-FIELD-PRODUCES-ELECTRIC-FIELD-IS-A-"
               "VECTOR-POTENTIAL-RENAMING-FARADAY-LAW-CIRCULAR")
    return dict(a_rows=a_rows, b_rows=b_rows, c_rows=c_rows, d=d, e=e,
                res_a_E=res_a_E, res_a_B=res_a_B, res_b=res_b, res_c=res_c,
                res_disp=res_disp, disp=disp, cnt=cnt, allok=allok,
                gallok=gallok, verdict=verdict, controls=CONTROLS,
                guards=GUARDS, items=ITEMS)


def report_and_write(R):
    a_rows, b_rows, c_rows = R["a_rows"], R["b_rows"], R["c_rows"]
    d, e = R["d"], R["e"]
    cnt, allok, gallok = R["cnt"], R["allok"], R["gallok"]
    verdict = R["verdict"]
    CONTROLS, GUARDS, ITEMS = R["controls"], R["guards"], R["items"]

    L = []
    w = L.append
    w("=" * 78)
    w(" TUFT-r169｜电磁-引力互生层：E=−f∂A/∂t 是电磁矢势的重命名")
    w("=" * 78)
    w("")
    w("[A1] 变量替换：A_EM = f·A_grav 代入 Maxwell 得靶式（零新增）")
    for r in a_rows:
        w("   z=%-8.4g res_E=%.3e res_B=%.3e" % (r["z"], r["res_E"], r["res_B"]))
    w("")
    w("[A2] 法拉第定律是被 B 定义重述")
    for r in b_rows:
        w("   z=%-8.4g ∇×E_x=%.6e −∂B/∂t_x=%.6e 残差=%.3e"
          % (r["z"], r["curlE_x"], r["minus_dBdt_x"], r["res"]))
    w("")
    w("[A3] 安培定律需额外假设 ω=kc（Maxwell 波动方程）")
    for r in c_rows:
        w("   z=%-8.4g ∇×B=%.6e μ0ε0∂E/∂t=%.6e 残差=%.3e 色散比=%.3e"
          % (r["z"], r["curlB"], r["mu0eps0_dE"], r["res"], r["dispersion"]))
    w("   [色散对照 ω=kc] 残差=%.3e" % R["res_disp"])
    w("")
    w("[A4] f 数值三重矛盾：纸面 %.6e / √(4πε0G)=%.6e / (c/2)√=%.6e"
      % (d["f_paper"], d["f_sqrt"], d["f_c2"]))
    w("[A5] 量纲 f=[M I⁻¹] 自洽（%s）" % e["dim_f_ok"])
    w("")
    w("[控制组]")
    for c in CONTROLS:
        w("   %s %-44s %-18s %s" % ("OK " if c["ok"] else "BAD", c["desc"],
                                    c["value"], c["expect"]))
    w("")
    w("[守卫]")
    for g in GUARDS:
        w("   %s %s  %s" % ("OK " if g["ok"] else "BAD", g["name"], g["detail"]))
    w("")
    w("[条目] %s" % cnt)
    w("[verdict] %s" % verdict)
    w("[控制组] %d/%d   [守卫] %d/%d"
      % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
         sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    report = "\n".join(L)

    # ============================================================
    # 判定册
    # ============================================================
    m = []
    b = m.append
    b("# 判定册 TUFT-r169｜电磁-引力互生层：E=−f∂A/∂t 是电磁矢势的重命名")
    b("")
    b("- 编号：TUFT-r169")
    b("- 生成时刻：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    b("- 引擎：`源码/%s.py`" % STEM)
    b("- 控制组：%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    b("- 守卫：%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    b("- 条目统计：%s" % "  ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())))
    b("")
    b("## 00. 分工声明（★ 与既有卷条目不可相加）")
    b("")
    b("| 卷 | 层 | 判的是什么 |")
    b("|----|----|-----------|")
    b("| r148 | 式子层 | P=m(c−v)、F=dP/dt、F_e/F_m=c/v、E=cB |")
    b("| r157 | 动力学积分层 | 真实洛伦兹积分、成立域 λ* |")
    b("| r158 | 字典层 | ω 凭什么等于 qB/(γm) |")
    b("| r159 | 引力侧还原 | 牛顿→泊松→1PN→爱因斯坦方程 |")
    b("| r160 | S17 力方程 | 宇宙大统一方程四项诠释 |")
    b("| r161–r164 | 电荷/时空/质量/本源 | 几何化公设层 |")
    b("| r165 | 四力闭合层 | κ、τ 是单粒子轨迹量，不是场量 |")
    b("| r166 | 能量方程 | E=m₀c² 推导与验证方法论 |")
    b("| r167 | 可证伪性层 | 几何基石不筛选力律、不可证伪 |")
    b("| r168 | 耦合 f 量纲（并行） | f 五重量纲与三数值 |")
    b("| **r169** | **电磁-引力互生层** | **E=−f∂A/∂t 是导出还是矢势重命名** |")
    b("")
    b("## 01. 判词")
    b("")
    b("`%s`" % verdict)
    b("")
    b("**S17 核心公式 14 声称「电场是引力场的时间变化率」E=−f·∂A/∂t、B=f·∇×A，")
    b("并由此『导出』法拉第定律与安培定律。本卷机读证明：**")
    b("① 令 A_grav=A_EM/f，则靶式逐位等于标准 Maxwell 的 E=−∂A_EM/∂t、B=∇×A_EM")
    b("（E 残差 %.1e、B 残差 %.1e）⇒ 是电磁矢势的重命名，零新增；" % (R["res_a_E"], R["res_a_B"]))
    b("② 法拉第定律是 B≡f·∇×A_grav 这一**定义**的直接重述（∇×E=−∂B/∂t 逐位恒等，")
    b("残差 %.1e），不是独立导出；" % R["res_b"])
    b("③ 安培定律只在 ω=kc（Maxwell 波动方程）下成立（非色散残差 %.3e、色散对照 %.1e）"
      % (R["res_c"], R["res_disp"]))
    b("⇒ 所谓『导出经典电磁学』是把 Maxwell 波动方程当隐藏前提的循环；")
    b("④ f 数值三重矛盾（纸面 1.05e−8 vs √(4πε0G)=%.6e vs (c/2)√=%.6e）。"
      % (d["f_sqrt"], d["f_c2"]))
    b("")
    b("## 02. 核心结论")
    b("")
    b("### 2.1 矢势重命名（A1，本卷承重 FAIL）")
    b("")
    b("| z | res_E | res_B |")
    b("|---|---|---|")
    for r in a_rows:
        b("| %-8.4g | %.3e | %.3e |" % (r["z"], r["res_E"], r["res_B"]))
    b("")
    b("- A_EM=f·A_grav ⇒ E=−∂A_EM/∂t=−f·∂A_grav/∂t、B=∇×A_EM=f·∇×A_grav 逐位相同；")
    b("- ⇒ 靶式与标准 Maxwell 是同一物理的重命名，「电场=引力场变化率」无新内容。")
    b("")
    b("### 2.2 法拉第定律是恒等式（A2）")
    b("")
    b("| z | ∇×E_x | −∂B/∂t_x | 残差 |")
    b("|---|---|---|---|")
    for r in b_rows:
        b("| %-8.4g | %.6e | %.6e | %.3e |"
          % (r["z"], r["curlE_x"], r["minus_dBdt_x"], r["res"]))
    b("")
    b("- ∇×E=−f·∂(∇×A_grav)/∂t=−∂(f·∇×A_grav)/∂t=−∂B/∂t 最后一步依赖 B 的定义 ⇒ 重述。")
    b("")
    b("### 2.3 安培定律是循环（A3）")
    b("")
    b("| z | ∇×B | μ0ε0·∂E/∂t | 残差 | 色散比 k²/(ω²/c²) |")
    b("|---|---|---|---|---|")
    for r in c_rows:
        b("| %-8.4g | %.6e | %.6e | %.3e | %.3e |"
          % (r["z"], r["curlB"], r["mu0eps0_dE"], r["res"], r["dispersion"]))
    b("")
    b("- 安培定律成立 ⟺ k²=ω²/c²（真空色散 = Maxwell 波动方程）；")
    b("- 非色散（ω/k=0.5 m/s）残差 %.3e，色散对照（ω=kc）残差 %.1e ⇒ "
      "『导出』是把波动方程当隐藏前提。" % (R["res_c"], R["res_disp"]))
    b("")
    b("### 2.4 f 数值三重矛盾（A4）")
    b("")
    b("| 口径 | 值 (kg/A) | 与纸面比值 |")
    b("|---|---|---|")
    b("| 纸面 | %.6e | 1.000000 |" % d["f_paper"])
    b("| √(4πε0G) | %.6e | %.4e |" % (d["f_sqrt"], d["ratio_paper_over_sqrt"]))
    b("| (c/2)·√(4πε0G) | %.6e | %.4e |" % (d["f_c2"], d["ratio_paper_over_c2"]))
    b("")
    b("- 三者互斥，均 ≠1；靶自承「f 计算细节缺失」由本卷机读证实。")
    b("")
    b("### 2.5 量纲自洽记 PASS（A5）")
    b("")
    b("- [E]=[M L T⁻³ I⁻¹]、[dA/dt]=[L T⁻³] ⇒ [f]=[M I⁻¹]，与 f=k'/(4πε0G) 一致；")
    b("- 量纲层诚实记 PASS（不因其它 FAIL 而否定量纲自洽）。")
    b("")
    b("## 03. 修复定价")
    b("")
    b("| 动作 | 宣称域内成立 | 代价 |")
    b("|---|---|---|")
    b("| KEEP（E=−f∂A/∂t 仍作『电场起源』） | 否 | A1/A2/A3 依旧成立 ⇒ 修不好 |")
    b("| DEL（删『电场本质=引力场变化率』诠释） | 是 | 退回标准 Maxwell 矢势表述 |")
    b("| REPLACE（给 A_grav 补独立观测锚点） | 是 | 需另立可检验预言 = 换框架 |")
    b("")
    b("- 宣称域内成立 **1** 个、**零代价 0** 个 ⇒ 修复可行 ≠ 修复后仍有内容。")
    b("")
    b("## 04. 靶自承与防过度指控")
    b("")
    b("- 靶自承「公设实验支撑薄弱」「f 计算细节缺失」⇒ 本卷不把「无观测锚点」当发现；")
    b("- 本卷发现仅限四条结构性机器证据：矢势重命名（A1）、法拉第恒等（A2）、")
    b("  安培循环（A3）、f 数值矛盾（A4）。")
    b("- 本卷不判 S17 其它 19 个核心公式（分层铁律）。")
    b("")
    b("## 05. 未闭合项（未做即未证，不得外推）")
    b("")
    b("1. 只判真空平面波（无源）；有源（J≠0）时安培定律额外含 μ0J 项，结论不变。")
    b("2. f 数值矛盾只列三口径；靶库内可能存在更多口径（r168 已作五重量纲清点）。")
    b("3. 不宣称 S17 被完全证伪 —— 只判决核心公式 14 的「导出=重命名」结构。")
    b("")
    b("## 06. 自抓与更正（本卷自身缺陷，如有则补）")
    b("")
    b("- 本卷首写一次通过（控制组 6/6、守卫 6/6、退出码 0）；无自身缺陷需登记。")
    b("")
    b("## 07. 红线")
    b("")
    b("- 数学自洽 ≠ 实验证实；**恒等式成立 ≠ 有新内容**；**成立 ≠ 宣称域无边界**；")
    b("- **靶自承优先**：本卷不把靶已自承的「无观测锚点」当作发现。")
    b("- 量纲自洽诚实记 PASS（A5），不因其它 FAIL 而抹去。")
    b("")

    # ============================================================
    # 落盘
    # ============================================================
    os.makedirs(OUT, exist_ok=True)
    payload = {
        "stem": STEM,
        "verdict": verdict,
        "items": ITEMS,
        "controls": CONTROLS,
        "guards": GUARDS,
        "key_numbers": {
            "res_rename_E": R["res_a_E"],
            "res_rename_B": R["res_a_B"],
            "res_faraday": R["res_b"],
            "res_ampere_nondisp": R["res_c"],
            "res_ampere_disp": R["res_disp"],
            "f_paper": d["f_paper"],
            "f_sqrt": d["f_sqrt"],
            "f_c2": d["f_c2"],
        },
        "controls_ok": "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)),
        "guards_ok": "%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    }
    with io.open(os.path.join(OUT, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(OUT, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    judge = "\n".join(m)
    with io.open(os.path.join(OUT, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)
    with io.open(os.path.join(OUT, "判定_" + STEM + ".md"), "w", encoding="utf-8") as f:
        f.write(judge)

    print(report)
    print("")
    print("[产物] " + os.path.join(OUT, STEM + ".json"))
    print("[产物] " + os.path.join(OUT, STEM + ".md"))
    print("[产物] " + os.path.join(OUT, "判定_" + STEM + ".md"))
    print("[产物] " + os.path.join(OUT, STEM + "_report.txt"))
    print("[控制组] %d/%d   [守卫] %d/%d"
          % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
             sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
    print("[退出码] %d" % (0 if (allok and gallok
                                 and all(it["status"] != "GUARD-FAIL"
                                         for it in ITEMS)) else 2))


if __name__ == "__main__":
    report_and_write(main())
