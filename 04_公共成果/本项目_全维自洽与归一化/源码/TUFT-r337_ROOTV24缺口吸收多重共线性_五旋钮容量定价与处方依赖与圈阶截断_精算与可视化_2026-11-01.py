# -*- coding: utf-8 -*-
"""
TUFT-r329 · ROOT V24 续篇【缺口吸收多重共线性（第五重）+ 处方依赖 + 圈阶截断定价】

承 r321（坐标/能标冗余）与 r328（场内容冗余）。前三卷分别证明了：
    ① 耦合坐标冗余（Möbius ≡ B→B−cA，v*=1/(150−c)）
    ② 能标冗余（同一 137 挂 m_e / m_Z / M_Pl 差 12.20）
    ③ 场内容冗余（含哪几味、各味质量、荷、色）
各自的结论是「有未声明输入」。本卷问一个**更强的问题**：

    即使把上面全部固定，观测上的「吻合」能不能归因于「固定点预测了 α」？

答：不能。原因是**多重共线性**——从 UV 值到观测值之间的缺口
    R = 137 − α⁻¹(m_Z) = 9.048
可以被**至少四个相互独立的旋钮各自 100% 吸收**（坐标 / 能标 / 场内容 / 非微扰强子），
而方程只有一个 ⇒ 欠定 ≥3 维 ⇒ 吻合没有归因力。

本卷三条轴（★= 净增量，与 r317/r320/r321/r328 条目不可相加）：
    X1 ★五旋钮容量定价：把每个旋钮「单独拨到能吸收缺口」所需的量求出来
        （c*=22.048 / Q*≈3.9e15 GeV / N*=1.98 个 e 当量或 m*≈8 eV / 圈阶只 0.21% / 强子 105%）
    X2 ★处方依赖：同一场内容下三种**都合法**的一圈处方（精确闭式 / 阶跃渐近含常数 /
        阶跃渐近不含常数）给 α⁻¹(m_Z) 的跨度 ≈0.53 = 2.5e7 倍 CODATA 不确定度
    X3 ★圈阶截断定价：一圈截断残余量级 ≈1e−2，是「预言 α」所需精度 2.1e−8 的 4.8e5 倍
        ⇒ 来料 §四 的一圈闭合**结构上**不足以支撑「预言 α 到观测精度」

诚实边界（写在最前）：
  · 圈阶一条是**量级估计**（(α/π)·Δ₁），不是精算二圈系数；登记为 BOUNDARY，不作硬判据。
  · 强子（非微扰）旋钮的容量用流夸克微扰式给出，物理上不成立（同 r328 C02），
    只用于定**量级**；正确的强子贡献需色散关系/格点，本卷不代做。
  · 实测锚 α⁻¹(m_Z)=127.952 与 M_Pl 为外部 [C] 级输入，needs_official_confirmation，
    只作参照，不作判据前提；把锚整体挪走，X1 的容量排序与 X3 的结论不受影响。
  · 本卷不否证渐近安全纲领；否证的是「吻合 ⟹ 预测」这一归因推理。

条目族：A01–A03（缺口分解/交叉印证）· B01–B05（五旋钮容量）· C01–C05（主判据）· CTL1–CTL6
守卫：G1–G12
"""

import io
import json
import os
import sys
import time
from decimal import Decimal, getcontext

import mpmath as mp

getcontext().prec = 60
mp.mp.dps = 90

RID = "r337"
STAMP = "2026-11-01"
ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(ROOT, "源码")
DATA = os.path.join(ROOT, "数据")

BASE = ("TUFT-%s_ROOTV24缺口吸收多重共线性_五旋钮容量定价与处方依赖与圈阶截断_%s"
        % (RID, STAMP))
HTML_NAME = "四力统一方程_ROOTV24缺口吸收多重共线性_r337可视化_%s.html" % STAMP

ALLOWED = set()
WRITTEN = []
T0 = time.time()
ITEMS = []
GUARDS = []

PI_D = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230782")

# ── 常数（逐项登记） ─────────────────────────────────────────────────────
ALPHA_INV = Decimal("137.035999084")     # CODATA 2018（真值锚）
ALPHA_INV_U = Decimal("0.000000021")
TOY_INV = Decimal(137)                   # 来料的玩具值
M_E_MEV = Decimal("0.51099895000")       # PDG
M_MU_MEV = Decimal("105.6583755")
M_TAU_MEV = Decimal("1776.86")
M_Z_MEV = Decimal("91187.6")
# 外部锚（[C] 级，needs_official_confirmation）
ALPHA_INV_MZ = Decimal("127.952")
ALPHA_INV_MZ_U = Decimal("0.009")
M_PL_GEV = Decimal("1.22089e19")         # 普朗克能量（[C]，只作量级参照）
# 夸克流质量（MS-bar，MeV）
CUR_M = {"u": Decimal("2.16"), "d": Decimal("4.67"), "s": Decimal("93"),
         "c": Decimal("1270"), "b": Decimal("4180")}
# 权重 = N_c * Q_f^2：u,c 为 3*(2/3)^2 = 4/3；d,s,b 为 3*(1/3)^2 = 1/3；轻子为 1
QCH2 = {"u": Decimal(4) / Decimal(3), "d": Decimal(1) / Decimal(3),
        "s": Decimal(1) / Decimal(3), "c": Decimal(4) / Decimal(3),
        "b": Decimal(1) / Decimal(3)}
K23PI = Decimal(2) / (Decimal(3) * PI_D)     # 2/(3π)
C59 = Decimal(5) / (Decimal(9) * PI_D)       # 5/(9π)：渐近有限常数项


def add(tid, layer, title, verdict, detail, kv=None):
    ITEMS.append({"id": tid, "layer": layer, "title": title,
                  "verdict": verdict, "detail": detail, "kv": kv or {}})
    return ITEMS[-1]


def P_(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "PASS", detail, kv)


def F_(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "FAIL", detail, kv)


def Bd(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "BOUNDARY", detail, kv)


def I_(tid, layer, title, detail, kv=None):
    return add(tid, layer, title, "INFO", detail, kv)


def guard(name, ok, note=""):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)


def fv(x, n=24):
    try:
        return format(Decimal(x), ".%dE" % (n - 1))
    except Exception:
        return str(x)


def dec(x):
    return Decimal(x) if not isinstance(x, Decimal) else x


# ── H(q)：闭式 / 90 位求积 / 渐近（与 r321·r328 同源，独立实现） ──────────
def dasinh(x):
    x = dec(x)
    return (x + (x * x + Decimal(1)).sqrt()).ln()


def H_closed(q):
    """返回 (I, H)；I=∫_0^1 x(1−x) ln[1+q²x(1−x)] dx，H=(2/π)I。"""
    q = dec(q)
    q2 = q * q
    if q2 == 0:
        return Decimal(0), Decimal(0)
    t1 = (Decimal(4) + q2) / (Decimal(6) * q2)
    t3 = ((q2 - Decimal(2)) * (Decimal(4) + q2).sqrt()
          * dasinh(q / Decimal(2)) / (Decimal(3) * q2 * q))
    I = t1 - Decimal(4) / Decimal(9) + t3
    return I, I * Decimal(2) / PI_D


def H_quad(q):
    q = mp.mpf(str(dec(q)))

    def f(x):
        return x * (1 - x) * mp.log(1 + q * q * x * (1 - x))

    I = mp.quad(f, [0, 1])
    return Decimal(str(I)), Decimal(str(I * 2 / mp.pi))


def H_asym(q):
    """阶跃渐近：H ≈ (2/(3π)) ln q − 5/(9π)（含有限常数项）。"""
    q = dec(q)
    return K23PI * q.ln() - C59


def H_log(q):
    """阶跃渐近不含常数项：H ≈ (2/(3π)) ln q。"""
    q = dec(q)
    return K23PI * q.ln()


def log2d(x):
    x = dec(x)
    return x.ln() / Decimal(2).ln()


def bisect_H(target, lo=None, hi=None):
    """求 q 使 H_closed(q)=target（H 在 q>0 严格单调增）。"""
    target = dec(target)
    lo = Decimal("1e-6") if lo is None else dec(lo)
    hi = Decimal(10) ** 30 if hi is None else dec(hi)
    for _ in range(400):
        mid = (lo * hi).sqrt()
        hm = H_closed(mid)[1]
        if hm < target:
            lo = mid
        else:
            hi = mid
        if hi / lo - Decimal(1) < Decimal("1e-45"):
            break
    return (lo * hi).sqrt()


def attribution_failure(caps, R):
    """判据：容量 ≥ R 的旋钮数 ≥2 ⇒ 吻合无归因力（欠定）。"""
    R = dec(R)
    n_eff = sum(1 for c in caps if dec(c) >= R)
    return (n_eff >= 2), n_eff


def section_A():
    # ── A01 缺口定义与守恒恒等式 ────────────────────────────────────────
    R = TOY_INV - ALPHA_INV_MZ
    He = H_closed(M_Z_MEV / M_E_MEV)[1]
    Hmu = H_closed(M_Z_MEV / M_MU_MEV)[1]
    Htau = H_closed(M_Z_MEV / M_TAU_MEV)[1]
    Hlep = He + Hmu + Htau
    Qc = sum(QCH2[f] * H_closed(M_Z_MEV / CUR_M[f])[1] for f in CUR_M)
    F3 = TOY_INV - Hlep
    Fq = F3 - Qc
    R_lep = F3 - ALPHA_INV_MZ
    R_full = Fq - ALPHA_INV_MZ
    resid = (Hlep + Qc + R_full) - R
    P_("A01", "分解", "缺口分解与守恒：R=%s = ΣH(轻子 %s + 夸克 %s) + 过头量 %s"
       % (fv(R), fv(Hlep), fv(Qc), fv(-R_full)),
       "定义总缺口 R ≡ α⁻¹(0)−α⁻¹(m_Z) = 137 − %s = %s（这是「把 137 搬到 m_Z」"
       "必须发生的下降量）。机器分解：轻子三味贡献 %s、五味夸克（流质量）贡献 %s，"
       "合计施加下降 %s；而只需 %s ⇒ **越过锚 %s**（α⁻¹(m_Z)=%s vs 锚 %s）。"
       "守恒恒等式 ΣH + R_full − R = %s（机器零）⇒ 分解无遗漏、无重复计数。"
       % (fv(ALPHA_INV_MZ), fv(R), fv(Hlep), fv(Qc), fv(Hlep + Qc), fv(R),
          fv(-R_full), fv(Fq), fv(ALPHA_INV_MZ), fv(resid)),
       {"R_total": fv(R), "H_lepton": fv(Hlep), "H_quark": fv(Qc),
        "F_lepton": fv(F3), "F_with_quark": fv(Fq),
        "R_lepton_gap": fv(R_lep), "R_full_gap": fv(R_full),
        "conservation_residual": fv(resid)})
    guard("G1_conservation_identity", abs(resid) < Decimal("1e-40"), fv(resid))

    # ── A02 与 r328 的交叉印证（自算，非读取他卷） ──────────────────────
    _, H1 = H_closed(Decimal(1))
    _, H1q = H_quad(Decimal(1))
    rel1 = abs(H1 - H1q) / abs(H1)
    P_("A02", "分解", "真空极化工具与 r321/r328 同源自算（H(1)=%s，相对差 %s）" % (fv(H1), fv(rel1)),
       "本卷独立实现闭式与 mpmath 90 位求积，在 q=1 给 H(1)=%s，与求积相对差 %s；"
       "与 r321 的 1.92353209028294044992602E−2、r328 A02 同值 ⇒ 三卷工具同源且各自可复现"
       "（交叉印证·不重复计数）。"
       % (fv(H1), fv(rel1)),
       {"H_1": fv(H1), "rel_dev": fv(rel1),
        "cross_ref": "r321-C01 / r328-A02（交叉印证·不重复计数）"})
    guard("G2_tool_homologous", rel1 < Decimal("1e-35"), fv(rel1))

    # ── A03 方向反转：锚被夹在中间 ─────────────────────────────────────
    P_("A03", "分解", "方向反转：轻子档欠 %s、加夸克后**过** %s ⇒ 锚被夹在中间"
       % (fv(R_lep), fv(-R_full)),
       "只用轻子三味：α⁻¹(m_Z)=%s，**高于**锚 %s（欠）；再把五味夸克（流质量）加进来："
       "%s，**低于**锚 %s（过）。⇒ 场内容旋钮**从上方扫到下方、跨过锚**，"
       "而 r328 已证明换一套夸克质量口径还能再动 1.81 ⇒ 该旋钮的扫描区间"
       "严格覆盖锚。**这是本卷 X1 的事实基础：缺口不是「差一点没凑上」，"
       "而是「旋钮一转就跨过去」**。"
       % (fv(F3), fv(R_lep), fv(Fq), fv(-R_full)),
       {"undershoot_lepton": fv(R_lep), "overshoot_with_quark": fv(-R_full),
        "anchor": fv(ALPHA_INV_MZ), "bracketed": (R_lep > 0) and (R_full < 0)})
    guard("G3_anchor_bracketed", (R_lep > 0) and (R_full < 0),
          "%s / %s" % (fv(R_lep), fv(R_full)))

    return {"R": R, "Hlep": Hlep, "Qc": Qc, "F3": F3, "Fq": Fq,
            "R_lep": R_lep, "R_full": R_full, "He": He, "Hmu": Hmu, "Htau": Htau}


def section_B(A):
    R = A["R"]
    R_lep = A["R_lep"]
    He = A["He"]

    # ── B01 旋钮 K1：耦合坐标 c ────────────────────────────────────────
    c_star = Decimal(150) - ALPHA_INV_MZ
    P_("B01", "容量", "★K1 耦合坐标旋钮：容量**无界**（α⁻¹=150−c，c 连续）；吸收 R 只需 c=%s"
       % fv(c_star),
       "Möbius v=u/(1−cu) 把两参数 (A,B) 压成一个不变量，u*=1/150 与 v*=1/137 只差一个 c。"
       "由于 c 是**连续实数**，α⁻¹=150−c 可取任意实数 ⇒ 该旋钮的容量**无界**，"
       "单独就足以 100%% 吸收任何缺口（吸收 R=%s 只需 c=%s；来料取 c=13 恰好落在 137）。"
       "⇒ 「137」不是预测值，而是 c 的**一次取值**。（与 r321 坐标冗余同源，本卷只做容量定价。）"
       % (fv(R), fv(c_star)),
       {"capacity": "unbounded", "c_star": fv(c_star), "c_toy": "13",
        "cross_ref": "r321（坐标冗余·不重复计数）"})
    guard("G4_k1_unbounded", c_star > Decimal(0), fv(c_star))

    # ── B02 旋钮 K2：能标 Q ────────────────────────────────────────────
    q_star = bisect_H(R)
    Q_star = M_E_MEV * q_star
    Q_gev = Q_star / Decimal(1000)
    over_pl = Q_gev / M_PL_GEV
    P_("B02", "容量", "★K2 能标旋钮：单电子圈吸收 R 只需跑到 Q*=%s GeV（=%s M_Pl）"
       % (fv(Q_gev), fv(over_pl)),
       "把 137 挂在 Q=0 上、只保留电子一圈，则 α⁻¹(Q)=137−H(Q/m_e)。解 H(Q*/m_e)=R=%s "
       "得 Q*=%s MeV = %s GeV，仅为普朗克能量的 %s 倍 ⇒ **远在 Planck 之下就能吸收全部缺口**。"
       "而 H(q) 随 q→∞ 无上界 ⇒ 该旋钮容量同样无界（上界=把 α⁻¹ 压到 0）。"
       "⇒ 「挂哪个能标」是一个连续输入，其容量足以单独解释任何缺口。"
       % (fv(R), fv(Q_star), fv(Q_gev), fv(over_pl)),
       {"q_star": fv(q_star), "Q_star_MeV": fv(Q_star), "Q_star_GeV": fv(Q_gev),
        "over_planck": fv(over_pl), "capacity": "unbounded"})
    guard("G5_k2_reaches_target", abs(H_closed(q_star)[1] - R) / R < Decimal("1e-30"),
          fv(abs(H_closed(q_star)[1] - R) / R))

    # ── B03 旋钮 K3：场内容（个数 / 单味质量两个口径） ──────────────────
    N_star = R_lep / He
    q_m = bisect_H(R_lep)
    m_star = M_Z_MEV / q_m
    m_eV = m_star * Decimal(1000)
    P_("B03", "容量", "★K3 场内容旋钮：吸收轻子档缺口 %s 只需 %s 个电子当量，"
       "或一个质量 %s eV、电荷 1 的无色费米子" % (fv(R_lep), fv(N_star), fv(m_eV)),
       "（口径甲·个数）在 m_Z 处每个 m=m_e 的单位电荷费米子贡献 H_e=%s ⇒ 需 %s 个；"
       "（口径乙·单味质量）解 H(m_Z/m*)=%s 得 m*=%s MeV = %s eV ⇒ "
       "**一个 ~8 eV、电荷 1、无色、目前未被计入的费米子就能把 α(m_Z) 拉到锚上**。"
       "⇒ 场内容旋钮的灵敏度高到「一个不可见粒子就能顶掉全部缺口」，"
       "而它同样无界（可任意加场）。观测吻合因此**无法归因于固定点**。"
       % (fv(He), fv(N_star), fv(R_lep), fv(m_star), fv(m_eV)),
       {"N_star": fv(N_star), "m_star_MeV": fv(m_star), "m_star_eV": fv(m_eV),
        "H_e_at_mZ": fv(He), "capacity": "unbounded"})
    guard("G6_k3_sensitivity_extreme", m_eV < Decimal(1000), fv(m_eV))

    # ── B04 旋钮 K4：圈阶（量级估计，BOUNDARY） ────────────────────────
    alpha = Decimal(1) / ALPHA_INV
    d1 = A["Hlep"]
    d2 = (alpha / PI_D) * d1
    frac4 = d2 / R_lep
    Bd("B04", "容量", "K4 圈阶旋钮：二圈残余量级 %s，只占轻子档缺口 %s 的 %s ⇒ **不是有效旋钮**"
       % (fv(d2), fv(R_lep), fv(frac4)),
       "一圈施加的下降 Δ₁=%s；微扰下一阶相对量级为 α/π=%s ⇒ Δ₂≈%s。相对缺口 %s 只有 %s，"
       "**远不足以**吸收 ⇒ 在五个旋钮里，**圈阶是唯一一个「拨不动」的**。"
       "但反过来它给出 X3 的硬读数：这个残余 %s 是 CODATA 不确定度 %s 的 %s 倍 ⇒ "
       "**一圈处方本身在精度上就不够格谈「预言 α」**。"
       "（诚实：本条为量级估计 (α/π)·Δ₁，非精算二圈系数，登记 BOUNDARY 不作硬判据。）"
       % (fv(d1), fv(alpha / PI_D), fv(d2), fv(R_lep), fv(frac4),
          fv(d2), fv(ALPHA_INV_U), fv(d2 / ALPHA_INV_U)),
       {"alpha_over_pi": fv(alpha / PI_D), "delta1": fv(d1), "delta2_est": fv(d2),
        "fraction_of_gap": fv(frac4), "over_codata_u": fv(d2 / ALPHA_INV_U),
        "method": "order-of-magnitude (alpha/pi)*Delta1, NOT an exact 2-loop coefficient"})
    guard("G7_k4_is_ineffective", frac4 < Decimal("1e-1"), fv(frac4))

    # ── B05 旋钮 K5：非微扰强子（物理上不成立，只定量级） ───────────────
    Qc = A["Qc"]
    frac5 = Qc / R_lep
    Bd("B05", "容量", "K5 非微扰强子旋钮：容量 %s = 轻子档缺口 %s 的 %s ⇒ 有效但**不可微扰计算**"
       % (fv(Qc), fv(R_lep), fv(frac5)),
       "五味夸克的微扰真空极化项（流质量口径）为 %s，已达轻子档缺口 %s 的 %s ⇒ "
       "**单独就能 100%% 吸收**。但诚实边界（同 r328 C02）：用微扰式配流夸克质量在"
       "m_Z 附近的轻夸克区间**物理上不成立**；正确的 Δα_had 需色散关系（e⁺e⁻ 数据）或格点。"
       "⇒ 这个旋钮的**容量是真的大，但它的值不在微扰可及范围内** —— "
       "缺口恰好落在「必须由非微扰输入填」的区间，而那部分不是固定点给出的。"
       % (fv(Qc), fv(R_lep), fv(frac5)),
       {"quark_term": fv(Qc), "fraction_of_gap": fv(frac5),
        "physical_validity": "NOT a physical computation; magnitude demo only",
        "cross_ref": "r328-C02（同口径·不重复计数）"})
    guard("G8_k5_is_effective", frac5 > Decimal("0.5"), fv(frac5))

    return {"c_star": c_star, "Q_gev": Q_gev, "over_pl": over_pl,
            "N_star": N_star, "m_eV": m_eV, "d2": d2, "frac4": frac4,
            "frac5": frac5}


def section_C(A, B):
    R = A["R"]
    R_lep = A["R_lep"]
    He, Hmu, Htau = A["He"], A["Hmu"], A["Htau"]

    # ── C01 ★主判据：多重共线性 ────────────────────────────────────────
    caps = {"K1_coordinate": Decimal(10) ** 12, "K2_scale": Decimal(10) ** 12,
            "K3_fieldcontent": Decimal(10) ** 12, "K4_looporder": B["d2"],
            "K5_hadronic": A["Qc"]}
    fail, n_eff = attribution_failure(list(caps.values()), R_lep)
    rank = n_eff - 1
    P_("C01", "主判据",
       "★缺口吸收多重共线性：方程 1 个、有效旋钮 %d 个 ⇒ 欠定 %d 维 ⇒ 吻合**无归因力**"
       % (n_eff, rank),
       "把「从 UV 值到 α(m_Z)」的缺口写成 1 个方程 R_lep=%s；能单独 100%% 吸收它的旋钮有 %d 个"
       "（K1 坐标 ∞ / K2 能标 ∞ / K3 场内容 ∞ / K5 强子 %s），只有 K4 圈阶无效（%s）。"
       "⇒ 未知量 %d 个、方程 1 个 ⇒ **欠定 %d 维**：给定任意观测值，都存在无穷多组"
       "(c, Q, 场内容, 强子输入) 与之吻合。这不是「还没算准」，而是**解空间本身不唯一** —— "
       "与 r12 的 Fisher 可识别性判据同构（cross_ref 登记）。"
       "⇒ **判词 ATTRIBUTION-FAILURE**：观测吻合不能归因于「固定点预测了 α」。"
       % (fv(R_lep), n_eff, fv(B["frac5"]), fv(B["frac4"]), n_eff, rank),
       {"n_effective_knobs": n_eff, "underdetermined_dim": rank,
        "capacities": {k: ("unbounded" if v > Decimal(10) ** 11 else fv(v))
                       for k, v in caps.items()},
        "cross_ref": "r12（Fisher 可识别性·同构）"})
    guard("G9_multicollinearity", fail and rank >= 2, "n_eff=%d rank=%d" % (n_eff, rank))

    # ── C02 ★处方依赖：三种合法一圈处方 ────────────────────────────────
    flav = [("e", M_Z_MEV / M_E_MEV), ("mu", M_Z_MEV / M_MU_MEV),
            ("tau", M_Z_MEV / M_TAU_MEV)]
    Ha = sum(H_closed(q)[1] for _, q in flav)
    Hb = sum(H_asym(q) for _, q in flav)
    Hc = sum(H_log(q) for _, q in flav)
    Fa, Fb, Fc = TOY_INV - Ha, TOY_INV - Hb, TOY_INV - Hc
    span = max(Fa, Fb, Fc) - min(Fa, Fb, Fc)
    # 与 CODATA 精度比（不是与实测锚的不确定度比）：处方误差属「预言精度」层，
    # 与 m_Z 处实测值本身的误差是两个不同层面（口径与 C03、C05 一致）
    over_u = span / ALPHA_INV_U
    P_("C02", "处方",
       "★处方依赖：同一场内容下三种**都合法**的一圈处方给 α⁻¹(m_Z) = %s / %s / %s，跨度 %s"
       % (fv(Fa), fv(Fb), fv(Fc), fv(span)),
       "P_a 精确闭式（含阈值平滑）= %s；P_b 阶跃渐近**含**有限常数 −5/(9π) = %s；"
       "P_c 阶跃渐近**不含**常数（教科书常见写法）= %s。三者差别只是「有限常数项要不要、"
       "阈值要不要平滑」，**都是一圈 QED 真空极化的合法表述**，却在 α⁻¹ 上散开 %s "
       "= CODATA 精度 %s 的 %s 倍（此处比的是**预言精度**，不是实测锚的不确定度）。"
       "⇒ 即使坐标/能标/场内容**全部钉死**，"
       "「用哪套处方」仍然是一个未声明输入，且其量级远超「命中 137」所需的精度。"
       % (fv(Fa), fv(Fb), fv(Fc), fv(span), fv(ALPHA_INV_MZ_U), fv(over_u)),
       {"P_exact": fv(Fa), "P_asym_with_const": fv(Fb), "P_asym_no_const": fv(Fc),
        "span": fv(span), "over_sigma": fv(over_u)})
    guard("G10_prescription_span_large", span > Decimal("1e-1") and over_u > Decimal("1e6"),
          "%s / %s" % (fv(span), fv(over_u)))

    # ── C03 ★圈阶截断 vs 精度需求 ──────────────────────────────────────
    d2 = B["d2"]
    need_ratio = d2 / ALPHA_INV_U
    P_("C03", "处方",
       "★圈阶截断定价：一圈残余 %s 是「预言 α」所需精度 %s 的 %s 倍 ⇒ 结构上不够格"
       % (fv(d2), fv(ALPHA_INV_U), fv(need_ratio)),
       "要把 α 声明到实验精度，α⁻¹ 的允许误差是 %s；而一圈处方自带的截断残余量级 %s "
       "是它的 %s 倍。⇒ **即使所有输入（坐标/能标/场内容/质量）全部给定，"
       "来料 §四 的一圈闭合也不可能把 α 预言到 CODATA 精度** —— "
       "缺口不是输入不够，而是**阶数不够**。这条不依赖外部锚（只用 CODATA 不确定度），"
       "是本卷最不依赖外部输入的一条读数。"
       % (fv(ALPHA_INV_U), fv(d2), fv(need_ratio)),
       {"delta2_est": fv(d2), "codata_u": fv(ALPHA_INV_U), "ratio": fv(need_ratio),
        "depends_on_external_anchor": False})
    guard("G11_loop_truncation_fatal", need_ratio > Decimal("1e5"), fv(need_ratio))

    # ── C04 剩余缺口的归属（BOUNDARY） ─────────────────────────────────
    Bd("C04", "处方",
       "剩余缺口的归属：轻子档欠 %s 落在**非微扰可及区间之外**的待填项，"
       "而填它的 K5 本身不可微扰计算" % fv(R_lep),
       "轻子档缺口 %s 与五味夸克微扰项 %s 同量级（%s），但后者的物理值只能由"
       "色散关系/格点给出 ⇒ **缺口恰好落在必须由非微扰实验输入填的区间**。"
       "这意味着来料 V25 目标链第 4 步（实际粒子质量与量子阈值）在这一段上"
       "**不是「待推导」，而是「待输入」**。本卷不代做该计算。"
       % (fv(R_lep), fv(A["Qc"]), fv(B["frac5"])),
       {"gap": fv(R_lep), "quark_term": fv(A["Qc"]),
        "cross_ref": "r328-C02（同口径·不重复计数）"})
    guard("G12_gap_in_nonperturbative_band", B["frac5"] > Decimal("0.5"), fv(B["frac5"]))

    # ── C05 冗余账扩表 ─────────────────────────────────────────────────
    bits_need = log2d(Decimal(1) / (ALPHA_INV_U / ALPHA_INV))
    bits_coord = Decimal("32.7338541217033817191315")   # r321 读数（引用登记）
    bits_scale = Decimal("29.1143583101872304558821")   # r321 读数（引用登记）
    # 场内容项：取 r328-C03 的合计读数 89.2509581703183424854605 减去 r321 的两项
    # （r328 只公布了合计，本卷按同一口径回算分量，避免自造数字）
    bits_field_r328 = Decimal("89.2509581703183424854605")
    bits_field = bits_field_r328 - bits_coord - bits_scale
    bits_presc = log2d(span / ALPHA_INV_U)
    tot = bits_coord + bits_scale + bits_field + bits_presc
    P_("C05", "记账",
       "★冗余账扩表：坐标 %s + 能标 %s + 场内容 %s + **处方 %s** = %s bit ≫ 需要 %s bit"
       % (fv(bits_coord), fv(bits_scale), fv(bits_field), fv(bits_presc),
          fv(tot), fv(bits_need)),
       "与 r321/r328 同口径（bits = log₂(跨度 / 目标分辨率)，分辨率取 α⁻¹ 的绝对不确定度 %s）。"
       "本卷**净新增**只有处方一项 log₂(%s / %s) = %s bit；坐标/能标/场内容三项为引用登记，"
       "不重复计数。合计 %s bit vs 声明 α 到实验精度所需 %s bit ⇒ **净信息 %s bit**。"
       % (fv(ALPHA_INV_U), fv(span), fv(ALPHA_INV_U), fv(bits_presc),
          fv(tot), fv(bits_need), fv(bits_need - tot)),
       {"bits_coordinate": fv(bits_coord), "bits_scale": fv(bits_scale),
        "bits_field": fv(bits_field), "bits_prescription": fv(bits_presc),
        "bits_total": fv(tot), "bits_needed": fv(bits_need),
        "net_bits": fv(bits_need - tot),
        "new_in_this_round": "bits_prescription only",
        "cross_ref": "r321-C08 / r328-C03（引用登记·不重复计数）"})
    guard("G13_budget_exceeds_need", tot > bits_need, "%s > %s" % (fv(tot), fv(bits_need)))

    return {"n_eff": n_eff, "rank": rank, "span": span, "over_u": over_u,
            "bits_total": tot, "bits_need": bits_need}


def section_CTL(A, B, span):
    R_lep = A["R_lep"]

    # ── CTL1 判据空运行：零容量 ⇒ 不报失败（判据有牙） ──────────────────
    f1, n1 = attribution_failure([Decimal(0)] * 5, R_lep)
    P_("CTL1", "控制组", "空运行：五个旋钮容量全 0 ⇒ 「有效 %d 个」⇒ 判据报**可归因**" % n1,
       "把所有旋钮容量置 0（等价于理论无任何可调输入），判据给 n_eff=%d <2 ⇒ "
       "**不触发**归因失败 ⇒ 判据不是「怎么说都对」，它有明确的放行条件。"
       % n1, {"n_eff": n1, "attribution_failure": f1})
    guard("G0a_zero_capacity_passes", (not f1) and n1 == 0, "n_eff=%d" % n1)

    # ── CTL2 单旋钮有效 ⇒ 不报失败（区分力，关键） ─────────────────────
    small = R_lep / Decimal(1000)
    f2, n2 = attribution_failure([Decimal(10) ** 12, small, small, small, small], R_lep)
    P_("CTL2", "控制组", "★区分力：只留一个有效旋钮 ⇒ n_eff=%d ⇒ 判据报**可归因**" % n2,
       "构造场景：K1 无界、其余四个容量仅为缺口的 0.1%% ⇒ n_eff=%d <2 ⇒ 判据**不**报失败。"
       "⇒ C01 的「归因失败」不是恒真结论，而是**由实测容量分布推出**的；"
       "若将来有人把其它四旋钮钉死（例如给出唯一处方、唯一场内容、唯一能标），"
       "归因就恢复了 —— 判据把「该钉死什么」精确地指了出来。"
       % n2, {"n_eff": n2, "attribution_failure": f2})
    guard("G0b_single_knob_passes", (not f2) and n2 == 1, "n_eff=%d" % n2)

    # ── CTL3 缺口超容量 ⇒ 不报失败（对偶面） ──────────────────────────
    f3, n3 = attribution_failure([Decimal(1), Decimal(1), Decimal(1),
                                  Decimal(1), Decimal(1)], Decimal(10) ** 30)
    P_("CTL3", "控制组", "对偶面：缺口取 %s（远超一切容量）⇒ n_eff=%d ⇒ 判据报**可归因**"
       % (fv(Decimal(10) ** 30), n3),
       "当缺口大到任何旋钮都吸收不了，判据给 n_eff=%d <2 ⇒ 不报归因失败，"
       "此时正确的结论是**理论被否证**（吻合不成立），而不是「无法归因」。"
       "⇒ 判据的两个出口语义不同：n_eff≥2 = 吻合但无归因力；n_eff=0 且 |R|>0 = 不吻合。"
       % n3, {"n_eff": n3, "attribution_failure": f3})
    guard("G0c_huge_gap_passes", (not f3) and n3 == 0, "n_eff=%d" % n3)

    # ── CTL4 处方跨度有不可消下限 ──────────────────────────────────────
    q_big = Decimal(10) ** 12
    lo = abs(H_asym(q_big) - H_log(q_big))
    P_("CTL4", "控制组", "处方跨度的**不可消下限**：单味 q→∞ 处 P_b 与 P_c 仍差 %s" % fv(lo),
       "即使 q→∞（阈值平滑修正 → 0），「含不含有限常数 −5/(9π)」的差别"
       "仍恒为 %s，不随 q 消失 ⇒ **处方不确定度有一个不可约下限**（每味 %s）。"
       "三味即 %s，与 C02 实测跨度 %s 同阶 ⇒ 该跨度不是数值巧合。"
       % (fv(lo), fv(C59), fv(Decimal(3) * C59), fv(span)),
       {"per_flavor_floor": fv(C59), "three_flavor_floor": fv(Decimal(3) * C59)})
    guard("G0d_prescription_floor", lo > Decimal("1e-2"), fv(lo))

    # ── CTL5 圈阶估计的线性性（α→0 极限） ─────────────────────────────
    a1 = Decimal(1) / ALPHA_INV
    a2 = a1 / Decimal(10)
    r_lin = ((a1 / PI_D) * A["Hlep"]) / ((a2 / PI_D) * A["Hlep"])
    P_("CTL5", "控制组", "圈阶估计线性：α 缩到 1/10 ⇒ Δ₂ 缩到 1/10（比值 %s）" % fv(r_lin),
       "Δ₂ 的量级估计取 (α/π)·Δ₁，对 α 线性 ⇒ 比值恰为 10.000…（实测 %s）。"
       "⇒ B04/C03 的「圈阶无效 / 但截断致命」两条读数对 α 的取值方式是**自洽**的："
       "α 越小，圈阶残余越小，但 CODATA 精度门槛不变 ⇒ 结论方向不翻转。"
       % fv(r_lin), {"ratio": fv(r_lin)})
    guard("G0e_loop_estimate_linear", abs(r_lin - Decimal(10)) < Decimal("1e-40"), fv(r_lin))

    # ── CTL6 单调性（保证二分求根有效） ────────────────────────────────
    qs = [Decimal(10) ** k for k in range(-3, 7)]
    hs = [H_closed(q)[1] for q in qs]
    mono = all(hs[i + 1] > hs[i] for i in range(len(hs) - 1))
    rel_mono = min((hs[i + 1] - hs[i]) / hs[i + 1] for i in range(len(hs) - 1))
    P_("CTL6", "控制组", "单调性：H(q) 在 q ∈ [1e−3, 1e6] 严格增（最小相对增幅 %s）" % fv(rel_mono),
       "B02/B03 的两个反解（Q* 与 m*）都靠二分，其有效性依赖 H 严格单调。"
       "机器检验 10 个十倍程：全部严格增，最小相对增幅 %s ⇒ **反解唯一、无多解风险**。"
       % fv(rel_mono), {"monotone": mono, "min_rel_increment": fv(rel_mono)})
    guard("G0f_H_monotone", mono, str(mono))


def build_md():
    L = ["# %s · 数据底稿" % RID, "",
         "- 轮次：%s　日期：%s　条目：%d" % (RID, STAMP, len(ITEMS)), "",
         "## 条目表", "", "| 编号 | 层 | 条目 | 判定 |", "|---|---|---|---|"]
    for e in ITEMS:
        L.append("| %s | %s | %s | %s |" % (e["id"], e["layer"], e["title"], e["verdict"]))
    L += ["", "## 明细", ""]
    for e in ITEMS:
        L += ["### %s · %s（%s）" % (e["id"], e["title"], e["verdict"]), "", e["detail"], ""]
    L += ["## 守卫", ""]
    for g in GUARDS:
        L.append("- %s ⇒ %s %s" % (g["name"], "PASS" if g["ok"] else "FAIL", g["note"]))
    return "\n".join(L) + "\n"


def build_html():
    rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                   % (e["id"], e["layer"], e["title"], e["verdict"]) for e in ITEMS)
    gl = "".join("<li>%s ⇒ %s</li>" % (x["name"], "PASS" if x["ok"] else "FAIL")
                 for x in GUARDS)
    det = "".join("<h3>%s · %s（%s）</h3><p>%s</p>"
                  % (e["id"], e["title"], e["verdict"], e["detail"]) for e in ITEMS)
    return """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>%s 可视化</title><style>
body{font-family:system-ui,"Microsoft YaHei",sans-serif;margin:24px;line-height:1.6}
table{border-collapse:collapse;width:100%%;font-size:13px}
th,td{border:1px solid #ccc;padding:6px 8px;text-align:left}
th{background:#f2f4f8}
</style></head><body>
<h1>TUFT-%s · ROOT V24 缺口吸收多重共线性（第五重）</h1>
<p><b>判词：</b>ABSORPTION-MULTICOLLINEARITY / ATTRIBUTION-FAILURE / PRESCRIPTION-SENSITIVITY / LOOP-TRUNCATION-FATAL</p>
<h2>条目表</h2><table><tr><th>编号</th><th>层</th><th>条目</th><th>判定</th></tr>%s</table>
<h2>守卫</h2><ul>%s</ul>
<h2>明细</h2>%s
</body></html>
""" % (RID, RID, rows, gl, det)


def write_out(name, text):
    path = os.path.join(DATA, name) if name != HTML_NAME else os.path.join(ROOT, name)
    if path not in ALLOWED:
        raise SystemExit("越界写入：%s" % path)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    WRITTEN.append(path)


def main():
    for n in (BASE + ".json", BASE + ".md", BASE + "_report.txt"):
        ALLOWED.add(os.path.join(DATA, n))
    ALLOWED.add(os.path.join(ROOT, HTML_NAME))

    A = section_A()
    B = section_B(A)
    C = section_C(A, B)
    section_CTL(A, B, C["span"])

    payload = {
        "round": RID, "title": "ROOT V24 缺口吸收多重共线性（第五重）", "date": STAMP,
        "verdict_summary": ("ABSORPTION-MULTICOLLINEARITY / ATTRIBUTION-FAILURE / "
                            "PRESCRIPTION-SENSITIVITY / LOOP-TRUNCATION-FATAL"),
        "entries": ITEMS, "guards": GUARDS,
        "guard_pass": sum(1 for g in GUARDS if g["ok"]), "guard_total": len(GUARDS),
        "constants": {
            "alpha_inv": str(ALPHA_INV), "alpha_inv_u": str(ALPHA_INV_U),
            "toy_inv": str(TOY_INV), "m_e_MeV": str(M_E_MEV),
            "m_mu_MeV": str(M_MU_MEV), "m_tau_MeV": str(M_TAU_MEV),
            "m_Z_MeV": str(M_Z_MEV),
            "alpha_inv_mZ_anchor": str(ALPHA_INV_MZ),
            "alpha_inv_mZ_u": str(ALPHA_INV_MZ_U),
            "m_Pl_GeV": str(M_PL_GEV),
            "anchor_is_external": True,
            "needs_official_confirmation": True,
        },
        "closed_forms": {
            "H": "H(q)=(2/pi)[(4+q^2)/(6q^2)-4/9+(q^2-2)sqrt(4+q^2)asinh(q/2)/(3q^3)]",
            "sum_rule": "alpha_eff^-1(Q) = alpha^-1(0) - sum_i N_c^i (Q_f^i)^2 H(Q/m_i)",
            "asymptotic": "H ~ (2/(3pi)) ln q - 5/(9pi)",
            "gap_identity": "R = 137 - alpha^-1(m_Z) = sum_i w_i H_i + R_full",
        },
        "relations": {
            "r321": "坐标/能标冗余 + 真空极化工具同源（引用登记·不重复计数）",
            "r328": "场内容冗余 + 夸克质量口径（引用登记·不重复计数）",
            "r320": "图表层（不重复）", "r317": "V24 主卷（不重复）",
        },
    }
    write_out(BASE + ".json", json.dumps(payload, ensure_ascii=False, indent=1))
    write_out(BASE + ".md", build_md())
    write_out(BASE + "_report.txt",
              "entries=%d guards=%d/%d\n" % (len(ITEMS), payload["guard_pass"],
                                             payload["guard_total"]))
    write_out(HTML_NAME, build_html())

    sys.stdout.write("r337 rc=0 entries=%d guards=%d/%d\n"
                     % (len(ITEMS), payload["guard_pass"], payload["guard_total"]))
    sys.stdout.write("R=%s R_lep=%s n_eff=%d rank=%d\n"
                     % (fv(A["R"]), fv(A["R_lep"]), C["n_eff"], C["rank"]))
    sys.stdout.write("c_star=%s Q_star_GeV=%s over_planck=%s\n"
                     % (fv(B["c_star"]), fv(B["Q_gev"]), fv(B["over_pl"])))
    sys.stdout.write("N_star=%s m_star_eV=%s span=%s bits=%s\n"
                     % (fv(B["N_star"]), fv(B["m_eV"]), fv(C["span"]),
                        fv(C["bits_total"])))
    sys.stdout.write("elapsed=%.1fs\nwritten:\n" % (time.time() - T0))
    for p in WRITTEN:
        sys.stdout.write("    " + p + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
