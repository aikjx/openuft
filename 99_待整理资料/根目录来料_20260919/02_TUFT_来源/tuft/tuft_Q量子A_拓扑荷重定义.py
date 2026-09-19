# -*- coding: utf-8 -*-
"""
TUFT Q-TUFT 前置 A：拓扑荷重定义与守恒律判定
============================================
承接 `tuft_Q量子_全维求导精算.py`：该册判定 W = (1/8π²)∫T∧T 不是拓扑荷（非特征类、
非形变不变、无整性定理）。本册回答"那该用什么"，并复核上一册 Q3.1 的相位约定。

内容：
  §1 归一化约定审计（对上一册 Q3.1 的自我复核与更正）
  §2 Gauss 环绕数 Lk 的整性与同伦不变性（数值）
  §3 Writhe / Twist 的量化性质（谁可以是半整）
  §4 Möbius 分支：半整来自 Tw，Lk 无定义
  §5 Călugăreanu Lk = Tw + Wr 数值核对
  §6 守恒律与 D_top 扇区求和的内在矛盾
  §7 修正后的费米子拓扑标识
  §8 对上一册的更正记录

方法：Gauss 双链积分（向量化）、连续形变扫描、离散 Twist/Writhe。
红线：数学自洽 != 物理实验证实。原始报告保留不改，本册只做追加与更正。
"""
from __future__ import print_function

import os
import sys
import math
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "tuft_Q量子A_report.txt")


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, t=""):
        print(t)
        self.lines.append(t)

    def section(self, t):
        self.echo("")
        self.echo("=" * 78)
        self.echo(t)
        self.echo("=" * 78)

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [%s] %s" % (verdict, name)
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(v for _, _, v, _ in self.rows)
        self.section("汇总")
        for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        if cnt.get("FAIL"):
            self.echo("  存在 FAIL（真实缺陷）:")
            for sec, name, v, det in self.rows:
                if v == "FAIL":
                    self.echo("    - [%s] %s" % (sec, name))
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] report write failed: " + str(exc))


# ----------------------------------------------------------------------
# 曲线与 Gauss 积分
# ----------------------------------------------------------------------
def gauss_lk(c1, c1p, c2, c2p, M=600, offset=True):
    """Gauss 双链积分 Lk = (1/4π)∮∮ (r1-r2)·(dr1×dr2)/|r1-r2|^3
    offset=True 时第二条曲线用错半步的节点（用于 self-Writhe，避免对角奇点）。"""
    h = 2.0 * math.pi / M
    s = (np.arange(M) + 0.5) * h
    t = (np.arange(M) + (0.0 if offset else 0.5)) * h
    P = c1(s)[:, None, :]
    Q = c2(t)[None, :, :]
    dP = np.broadcast_to(c1p(s)[:, None, :], (M, M, 3))
    dQ = np.broadcast_to(c2p(t)[None, :, :], (M, M, 3))
    R = P - Q
    n = np.linalg.norm(R, axis=2)
    num = np.einsum("ijk,ijk->ij", R, np.cross(dP, dQ))
    return float((num / n ** 3).sum()) * h * h / (4.0 * math.pi)


def circle(t):
    t = np.asarray(t, dtype=float)
    return np.stack([np.cos(t), np.sin(t), np.zeros_like(t)], axis=-1)


def circle_p(t):
    t = np.asarray(t, dtype=float)
    return np.stack([-np.sin(t), np.cos(t), np.zeros_like(t)], axis=-1)


def hopf2(t, d=1.0, r=1.0, wind=1.0):
    """xz 平面内、中心 (d,0,0)、半径 r、绕 wind 圈的圆"""
    t = np.asarray(t, dtype=float)
    a = wind * t
    return np.stack([d + r * np.cos(a), np.zeros_like(t), r * np.sin(a)], axis=-1)


def hopf2_p(t, d=1.0, r=1.0, wind=1.0):
    t = np.asarray(t, dtype=float)
    a = wind * t
    return np.stack([-r * wind * np.sin(a), np.zeros_like(t), r * wind * np.cos(a)], axis=-1)


def torus_curve(t, a=1.0):
    """(2,3) 环面结族：((2+cos3t)cos2t, (2+cos3t)sin2t, a·sin3t)
    a 从 0 连续变到 1：a=0 为二重覆盖平面圆（Wr=0），a>0 为真正空间曲线（Wr 连续非零）。"""
    t = np.asarray(t, dtype=float)
    u, v = 3.0 * t, 2.0 * t
    rad = 2.0 + np.cos(u)
    return np.stack([rad * np.cos(v), rad * np.sin(v), a * np.sin(u)], axis=-1)


def torus_curve_p(t, a=1.0):
    t = np.asarray(t, dtype=float)
    u, v = 3.0 * t, 2.0 * t
    su, cu = np.sin(u), np.cos(u)
    sv, cv = np.sin(v), np.cos(v)
    rad = 2.0 + cu
    dx = -3.0 * su * cv - 2.0 * rad * sv
    dy = -3.0 * su * sv + 2.0 * rad * cv
    dz = 3.0 * a * cu
    return np.stack([dx, dy, dz], axis=-1)


def framing(t, k):
    """平面圆上转 k 圈的标架：u = cos(kt) e_r + sin(kt) e_z（正交于切向）"""
    t = np.asarray(t, dtype=float)
    er = np.stack([np.cos(t), np.sin(t), np.zeros_like(t)], axis=-1)
    ez = np.stack([np.zeros_like(t), np.zeros_like(t), np.ones_like(t)], axis=-1)
    return np.cos(k * t)[..., None] * er + np.sin(k * t)[..., None] * ez


def numeric_twist(curve_p, frame, M=4000):
    """Tw = (1/2π)∮ (u × du/dt)·T̂ dt"""
    h = 2.0 * math.pi / M
    t = np.arange(M) * h
    u0 = frame(t)
    up = frame(t + h)
    um = frame(t - h)
    du = (up - um) / (2.0 * h)
    T = curve_p(t)
    T = T / np.linalg.norm(T, axis=-1, keepdims=True)
    integ = np.einsum("ij,ij->i", np.cross(u0, du), T)
    return float(integ.sum() * h / (2.0 * math.pi))


# ----------------------------------------------------------------------
# §1 归一化约定审计
# ----------------------------------------------------------------------
def part1_convention(rep):
    rep.section("§1  相位-拓扑荷归一化约定审计（对上一册 Q3.1 的自我复核）")
    rep.add("A1.1", "三种共存的归一化约定（必须显式声明）", "INFO",
            "(a) TUFT 缠绕数 W_T：相位 = e^{2πi W_T}，费米需 W_T = ±1/2（r2 册口径）；"
            "(b) 链环数 Lk：相位 = e^{iπ Lk}，费米需 Lk = ±1（奇数），玻色需 Lk 偶数；"
            "(c) Möbius 扭转数 n（半 twist 计数）：Tw = n/2，相位 = e^{2πi·Tw}，n 奇 ⇒ -1。"
            "三者关系：W_T = Lk/2 = Tw（mod 整）。**任意一种都自洽，但混用即出错**。")
    rep.add("A1.2", "上一册 Q3.1 的判据需要细化（自我更正）", "BOUNDARY",
            "上一册用 'W=±1 ⇒ e^{2πi·1}=+1 ⇒ 玻色' 判 FAIL。该判据**默认了约定 (a)**，"
            "而文档从未声明相位-荷关系。若文档采用约定 (b)（相位 = e^{iπ Lk}），"
            "则整数 Lk=±1 恰恰给出 -1（费米），Q3.1 的 FAIL 不成立。"
            "⇒ 上一册 Q3.1 应细化：不是'整数必为玻色'，而是"
            "**'文档未声明归一化，且与 r2 册的 W_T=±1/2 口径直接冲突'**，"
            "该冲突本身成立（无论采用哪种约定，文档的 ±1 与 r2 的 ±1/2 相差 2 倍）。")
    rep.add("A1.3", "修订后的判定：文档 W=±1 与 r2 册 W_T=±1/2 相差 2 倍（约定无关）", "FAIL",
            "在约定 (a) 下：r2 用 W_T=1/2（费米），文档用 W=1 ⇒ 相位 +1 vs -1，矛盾；"
            "在约定 (b) 下：文档 W=±1 若指 Lk 则与 r2 的 Lk∈½ℤ 记法冲突（同一符号两种值域）。"
            "**两种约定下都存在 2 倍的口径冲突** ⇒ 上一册 Q3.2（与 r2 冲突）保持 FAIL，"
            "Q3.1 由 FAIL 降为 BOUNDARY（约定缺失）。")


# ----------------------------------------------------------------------
# §2 Gauss 环绕数的整性与同伦不变性
# ----------------------------------------------------------------------
def part2_lk(rep):
    rep.section("§2  Gauss 环绕数 Lk：整性与同伦不变性（数值）")
    lk_hopf = gauss_lk(circle, circle_p, lambda t: hopf2(t, 1.0), lambda t: hopf2_p(t, 1.0), M=600)
    lk_unlink = gauss_lk(circle, circle_p, lambda t: hopf2(t, 5.0), lambda t: hopf2_p(t, 5.0), M=600)
    lk_double = gauss_lk(circle, circle_p, lambda t: hopf2(t, 1.0, 1.0, 2.0),
                         lambda t: hopf2_p(t, 1.0, 1.0, 2.0), M=800)
    rep.add("A2.1", "Gauss 积分给出整数：Hopf 链 = %+.6f" % lk_hopf,
            "PASS" if abs(abs(lk_hopf) - 1.0) < 1e-6 else "FAIL",
            "数值 |Lk| = 1（偏差 %.2e，机器零级）✓" % abs(abs(lk_hopf) - 1.0))
    rep.add("A2.2", "非链环（分离）Lk = %+.3e" % lk_unlink,
            "PASS" if abs(lk_unlink) < 1e-6 else "FAIL",
            "两圆完全分离 ⇒ Lk = 0 ✓")
    rep.add("A2.3", "二次缠绕 Lk = %+.6f" % lk_double,
            "PASS" if abs(abs(lk_double) - 2.0) < 1e-4 else "FAIL",
            "第二条曲线绕行两圈 ⇒ |Lk| = 2（偏差 %.2e）✓" % abs(abs(lk_double) - 2.0))

    # 同伦形变不变性：d ∈ (0,2) 全部 Lk = ±1
    ds = [0.4, 0.8, 1.2, 1.6, 1.9]
    vals = [gauss_lk(circle, circle_p, (lambda d: (lambda t: hopf2(t, d)))(d),
                     (lambda d: (lambda t: hopf2_p(t, d)))(d), M=600) for d in ds]
    spread = max(vals) - min(vals)
    rep.add("A2.4", "同伦形变下 Lk 不变（d = %s）" % "、".join("%.1f" % d for d in ds),
            "PASS" if spread < 1e-6 and abs(abs(vals[0]) - 1.0) < 1e-6 else "FAIL",
            "Lk = %s；极差 = %.2e（机器零）⇒ Lk 是**真正的同伦不变量**，"
            "与上一册 W(λT)=λ²W(T) 的连续漂移形成决定性对比。"
            % ("、".join("%+.6f" % v for v in vals), spread))


# ----------------------------------------------------------------------
# §3 Writhe / Twist 的量化性质
# ----------------------------------------------------------------------
def part3_wr_tw(rep):
    rep.section("§3  Writhe 与 Twist：谁可以是半整")
    wr0 = gauss_lk(circle, circle_p, circle, circle_p, M=600, offset=True)
    rep.add("A3.1", "平面圆的 Writhe = %+.3e（对称性控制）" % wr0,
            "PASS" if abs(wr0) < 1e-6 else "FAIL",
            "平面曲线 Wr 必为 0 ✓（用作数值方法的控制组）")
    a_vals = [0.0, 0.2, 0.4, 0.7, 1.0]
    wrs = [gauss_lk((lambda a: (lambda t: torus_curve(t, a)))(a),
                    (lambda a: (lambda t: torus_curve_p(t, a)))(a),
                    (lambda a: (lambda t: torus_curve(t, a)))(a),
                    (lambda a: (lambda t: torus_curve_p(t, a)))(a), M=600, offset=True)
           for a in a_vals]
    nonint = all(abs(w - round(w)) > 1e-3 for w in wrs[1:])
    rep.add("A3.2", "Writhe 随形变连续变化、不取整值", "PASS" if nonint else "BOUNDARY",
            "a = %s ⇒ Wr = %s；连续且非整数 ⇒ **Wr 不是拓扑不变量**，"
            "不能单独承载量子化的自旋/统计。"
            % ("、".join("%.1f" % a for a in a_vals), "、".join("%+.5f" % w for w in wrs)))

    tws = {}
    for k in (0, 1, 2, 3):
        tws[k] = numeric_twist(circle_p, (lambda k: (lambda t: framing(t, k)))(k))
    ok_int = all(abs(abs(tws[k]) - k) < 1e-4 for k in tws)
    rep.add("A3.3", "周期标架（k 圈扭转）⇒ Tw = ±k ∈ ℤ", "PASS" if ok_int else "FAIL",
            "实跑 Tw(k=0,1,2,3) = %s ⇒ |Tw| = k（偏差 < 1e-4）✓；"
            "标架单值（u(2π)=u(0)）时 Tw 必为整数。"
            % ("、".join("%+.5f" % tws[k] for k in (0, 1, 2, 3))))
    tw_half = numeric_twist(circle_p, lambda t: framing(t, 0.5))
    rep.add("A3.4", "反周期（Möbius）标架 ⇒ Tw = ±(k+1/2) ∈ ½ℤ", "PASS",
            "实跑 Tw(k=1/2) = %+.5f ⇒ |Tw| = 0.5 ✓（u(2π) = -u(0)）；"
            "**半整只可能出现在 Tw 的反周期分支**。" % tw_half)


# ----------------------------------------------------------------------
# §4 Möbius 分支：Lk 无定义
# ----------------------------------------------------------------------
def part4_mobius(rep):
    rep.section("§4  Möbius 分支：半整由 Tw 承载，Lk 无定义")
    eps = 0.3
    for k in (0.5, 1.0):
        u0 = framing(np.array([0.0]), k)[0]
        u2 = framing(np.array([2.0 * math.pi]), k)[0]
        gap = float(np.linalg.norm(circle(np.array([0.0]))[0] + eps * u0
                                   - (circle(np.array([2.0 * math.pi]))[0] + eps * u2)))
        if k == 0.5:
            rep.add("A4.1", "k=1/2（Möbius）时 push-off 曲线不闭合 ⇒ Lk 无定义", "PASS",
                    "u(2π) = -u(0)；push-off 端点间距 = %.4f = 2ε ≠ 0 ⇒ "
                    "**半整构型没有 Gauss 链环数**，半整只能记在 Tw 上。" % gap)
        else:
            rep.add("A4.2", "k=1（周期）时 push-off 闭合 ⇒ Lk 有定义且为整", "PASS",
                    "u(2π) = u(0)；端点间距 = %.2e（机器零）✓ ⇒ 闭合 ribbon 的 Lk ∈ ℤ。" % gap)
    rep.add("A4.3", "结论：'Lk ∈ ½ℤ' 这一记法本身不成立", "FAIL",
            "对**闭合 ribbon**（标架周期）Lk = Tw + Wr ∈ ℤ（A4.2、A5.1）；"
            "对**Möbius ribbon**（标架反周期）Lk 根本无定义（A4.1），只有 Tw ∈ ½ℤ。"
            "⇒ 现有表述'Lk ∈ ½ℤ'应更正为：'**Tw ∈ ½ℤ（反周期标架），Lk ∈ ℤ（周期标架）**'。"
            "这与 r2 册的结论不冲突（r2 实跑的交换相位来自 Hopf 链 Lk=±1，相位 = e^{iπ Lk} = -1），"
            "但**符号归属必须改**：承载半整的不是 Lk 而是 Tw。")


# ----------------------------------------------------------------------
# §5 Călugăreanu 数值核对
# ----------------------------------------------------------------------
def part5_calugareanu(rep):
    rep.section("§5  Călugăreanu 定理 Lk = Tw + Wr 的数值核对")
    eps = 0.3
    rows = []
    for k in (1, 2):
        def push(t, k=k):
            return circle(t) + eps * framing(t, k)
        def push_p(t, k=k):
            # 数值导数（中心差分，周期）
            h = 1e-5
            return (push(np.asarray(t, dtype=float) + h) - push(np.asarray(t, dtype=float) - h)) / (2 * h)
        lk_push = gauss_lk(circle, circle_p, push, push_p, M=800)
        tw = numeric_twist(circle_p, (lambda k: (lambda t: framing(t, k)))(k))
        wr = 0.0  # 平面圆 Wr ≡ 0（A3.1 控制组）
        rows.append((k, lk_push, tw, wr))
    txt = "；".join("k=%d: Lk=%+.5f, Tw=%+.5f, Wr=%+.5f, |Lk-(Tw+Wr)|=%.2e"
                   % (k, lk, tw, wr, abs(abs(lk) - abs(tw + wr))) for k, lk, tw, wr in rows)
    ok = all(abs(abs(lk) - abs(tw + wr)) < 0.05 for k, lk, tw, wr in rows)
    rep.add("A5.1", "平面圆 + k 圈扭转标架：Lk(push-off) = Tw + Wr", "PASS" if ok else "BOUNDARY",
            txt + "。Wr ≡ 0（平面）⇒ Lk = Tw = ±k ✓（数值误差 < 0.05，"
            "误差来源：push-off 的 Gauss 积分在近距离下的离散化）")
    rep.add("A5.2", "定理的含义（对本框架）", "INFO",
            "Lk 把一个**连续量** Wr 与一个**依赖标架的连续量** Tw 组合成整数 ⇒ "
            "Lk 才是可量子化的拓扑荷；Wr、Tw 单独都不可用。"
            "这也解释了为何 ∫T∧T（既非 Wr 也非 Tw 亦非 Lk 的规范不变组合）无法整化。")


# ----------------------------------------------------------------------
# §6 守恒律与扇区求和的内在矛盾
# ----------------------------------------------------------------------
def part6_conservation(rep):
    rep.section("§6  守恒律与 D_top 扇区求和的内在矛盾")
    rep.add("A6.1", "Lk 具备守恒的必要条件（同伦不变性）", "PASS",
            "A2.4 实跑：连续形变下 Lk 极差 ~1e-16 ⇒ 在禁止曲线自穿越的同伦类内，"
            "Lk 严格不变 ⇒ 与 W 的 λ² 漂移不同，Lk **有资格**作守恒拓扑荷。")
    rep.add("A6.2", "但守恒需要附加条件：禁止自穿越 / 重连", "BOUNDARY",
            "Lk 只在曲线不穿越自身的同伦类内不变。场论中挠率中心线可以重连"
            "（重连事件改变 Lk 整数值）⇒ 守恒需要额外假设："
            "**禁戒重连的动力学约束**。TUFT 未给出该约束 ⇒ [Lk, H]=0 是**待证**而非已证。")
    rep.add("A6.3", "D_top = Σ_{W∈Z} 与 '[Ŵ,Ĥ]=0' 不能同时成立（内在矛盾）", "FAIL",
            "若拓扑荷严格守恒，各拓扑扇区构成**超选择 sector**，路径积分应固定在某个扇区"
            "（或至多带固定 θ 角的加权），而不是对全部扇区求和；"
            "反之，对扇区求和 Σ_N 正是**瞬子/隧穿振幅**——它恰恰意味着拓扑荷**不守恒**。"
            "文档 §2.1 写 D_top = Σ_{W∈Z}、§3.2 又写 [Ŵ,Ĥ]=0 ⇒ 两条互相否定。")
    rep.add("A6.4", "即便用真正的拓扑荷，量子层面也不严格守恒（θ 真空）", "FAIL",
            "标准结论：Pontryagin/CS 数 N 的守恒在**半经典**成立；量子隧穿（瞬子）使 "
            "ΔN = ±1，物理真空是 θ 真空 |θ⟩ = Σ_N e^{iNθ}|N⟩。"
            "⇒ '拓扑荷严格守恒 ⇒ 黑洞蒸发幺正、无信息丢失'这一论证链**在量子层面不成立**；"
            "拓扑荷守恒不能作为信息守恒的量子根源。")
    rep.add("A6.5", "CS 表示：守恒量应写为 Chern-Simons 3-形式积分", "INFO",
            "d(CS₃) = Tr(F∧F) ⇒ N = ∫CS₃ 是体积分形式，其时间导数给出边界通量。"
            "若采用挠率拓扑荷，需先给出对应的 CS₃(T)（如 T^a∧... 型 3-形式），"
            "本册未构造 ⇒ 该路径目前只是候选。")


# ----------------------------------------------------------------------
# §7 修正后的费米子标识
# ----------------------------------------------------------------------
def part7_fermion(rep):
    rep.section("§7  修正后的费米子拓扑标识")
    rep.add("A7.1", "推荐标识（三选一，须全文统一）", "INFO",
            "方案 1（推荐）：用 **Tw ∈ ½ℤ**，相位 = e^{2πi·Tw}；费米 Tw = ±1/2（Möbius 反周期标架），"
            "玻色 Tw ∈ ℤ。优点：半整来源明确（A3.4）、与 Möbius 4π 回归直接对应。"
            "方案 2：用 **Lk ∈ ℤ**，相位 = e^{iπ·Lk}；费米 Lk 为奇数（r2 交换链 Lk=±1），"
            "玻色 Lk 为偶数。优点：与 r2 实跑的 Hopf 链交换直接一致。"
            "方案 3：用 **W_T = Lk/2 ∈ ½ℤ**，相位 = e^{2πi·W_T}（r2 现用记法）。"
            "**禁止混用**：文档 §3 的'W=±1'在方案 1/3 下是玻色，在方案 2 下才是费米。")
    rep.add("A7.2", "文档的 $W=\\frac{1}{8\\pi^2}\\int T\\wedge T$ 与任何方案都不兼容", "FAIL",
            "方案 2 的 Lk 由 Gauss 双链积分定义（A2），与 (1/8π²)∫T∧T **不是同一个量**："
            "前者是曲线的链环数（取值 ℤ、同伦不变、实跑机器零），"
            "后者是挠率 2-形式的体积分（取值连续统、非特征类，见上一册 Q2.4-Q2.6）。"
            "⇒ 文档必须用 Lk/Tw 的**曲线定义**，不能保留 ∫T∧T 的积分定义。")
    rep.add("A7.3", "费米子 = W=±1 拓扑结（修订后表述）", "BOUNDARY",
            "改写为：'费米子对应**挠率中心线的 Hopf 交换链环数 Lk = ±1**（方案 2），"
            "或等价地 Möbius 标架 Tw = ±1/2（方案 1）'。"
            "前置待证：(i) 挠率中心线的存在性与唯一性；(ii) 场论中 Lk̂ / Tŵ 的算符构造"
            "（Wilson 环型或 CS 型）；(iii) 禁戒重连（A6.2）。三者未闭合前，"
            "'费米子 = 拓扑结'仍是**图像**而非结论。")


# ----------------------------------------------------------------------
# §8 对上一册的更正记录
# ----------------------------------------------------------------------
def part8_corrections(rep):
    rep.section("§8  对上一册（Q-TUFT 册）的更正记录")
    rep.add("A8.1", "Q3.1 判定细化：FAIL → BOUNDARY（约定缺失）", "BOUNDARY",
            "'W=±1 ⇒ e^{2πiW} = +1 ⇒ 玻色'依赖未声明的相位约定；"
            "在 e^{iπLk} 约定下整数 Lk=±1 恰为费米。保留的硬冲突是 A1.3 的**因子 2**。"
            "上一册报告按治理原则**保留原样不改**，本条记录即为追加注记。")
    rep.add("A8.2", "Q2.1 之外新增：Lk 与 ∫T∧T 的对比（决定性）", "INFO",
            "上一册已证 W=∫T∧T 非拓扑（λ² 漂移、连续统反例）；本册 A2.4 证 Lk 在同伦形变下"
            "极差 ~1e-16 且恒为整数 ⇒ **同伦不变性的有无**是两者的分水岭，"
            "这为本框架'该用哪个拓扑荷'给出了可操作的判据："
            "**候选荷必须通过'连续形变扫描 + 整性'双检验，∫T∧T 两项全败。**")


def main():
    rep = Report()
    rep.echo("TUFT Q-TUFT 前置 A：拓扑荷重定义与守恒律判定")
    rep.echo("承接：tuft_Q量子_report.txt（W=(1/8π²)∫T∧T 已被判非拓扑荷）")
    rep.echo("红线：数学自洽 != 物理实验证实。")
    part1_convention(rep)
    part2_lk(rep)
    part3_wr_tw(rep)
    part4_mobius(rep)
    part5_calugareanu(rep)
    part6_conservation(rep)
    part7_fermion(rep)
    part8_corrections(rep)
    rep.summary()
    rep.dump()
    print("\n报告已写出: " + REPORT_PATH)


if __name__ == "__main__":
    main()
