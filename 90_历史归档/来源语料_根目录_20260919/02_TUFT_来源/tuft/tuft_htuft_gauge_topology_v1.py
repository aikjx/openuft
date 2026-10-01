# -*- coding: utf-8 -*-
"""
tuft_htuft_gauge_topology_v1.py
================================

H-TUFT 规范结构的拓扑起源 —— **脚手架 + 划界工具（非预言）**

用途：补齐补充卷H 的 `script_ref`。本卷问题：能否从螺旋挠率丛的「局部缠绕」
**自然导出** SM 规范结构 `SU(3)×SU(2)×U(1)`？

本文件的立场（承定理 B 的两侧）：
  - 【允许侧】拓扑/整数**可以**编码**离散**可观测量：
      * 电荷量子化（缠绕数为整数 ⇒ 电荷取离散值）；
      * 手征零模数（Atiyah-Singer 指数定理 ⇒ 拓扑指数给出手征零模的净个数）。
    这些是拓扑的**真实成功**，本文件如实记录（不抹功）。
  - 【禁止侧】拓扑**不能**编码**连续/选择**：
      * **群的选择**：缺陷同伦签名**不唯一**选出 SM（§3 演示：≥3 个不同群共享同一签名）；
      * **耦合常数的值/比值** `α_s:α_2:α_1`（§6：无拓扑不变量 ⇒ 撞定理 C/D）；
      * **具体手征表示与超荷赋值**（§4/§5：需外生赋值；反常相消是**约束**而非导出）。

结论（§0 与本文件实跑）：**强宣称「自然导出 SU(3)×SU(2)×U(1)」结构性失败**——
同伦数据不区分候选群。CUR-20 定级：❌ 核心宣称失败（结构性），同时**明确承认离散侧的成功**。

依赖 numpy + fractions；不引入新假设。
"""

import hashlib
import os
import sys
from fractions import Fraction

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ----------------------------------------------------------------------
# §5 一代 SM 费米子（**全左手 Weyl 约定**；反常计算须用此约定）
#    (名称, SU(3) 重数, SU(2) 重数, 超荷 Y)   —— Q = T_3 + Y/2
# ----------------------------------------------------------------------
SM_LEFT_HANDED = (
    ("Q_L   (u_L,d_L)", 3, 2, Fraction(1, 6)),
    ("u_R^c (u 右手共轭)", 3, 1, Fraction(-2, 3)),
    ("d_R^c (d 右手共轭)", 3, 1, Fraction(1, 3)),
    ("L_L   (nu_L,e_L)", 1, 2, Fraction(-1, 2)),
    ("e_R^c (e 右手共轭)", 1, 1, Fraction(1, 1)),
)

# §6 三个规范耦合（M_Z 标度，GUT 归一化）——无任何拓扑不变量给出此比值
ALPHA_S_MZ = 0.1179
ALPHA_2_MZ = 0.0338
ALPHA_1_MZ = 0.0102

# ----------------------------------------------------------------------
# §3 缺陷分类签名 (pi_0, pi_1, pi_2, pi_3)  ——「拓扑能给什么」
#    Z = 整数；Z2 = 二阶；0 = 平凡
# ----------------------------------------------------------------------
HOMOTOPY_SIGNATURE = {
    "SU(2)":                 (0, 0, 0, "Z"),
    "SU(3)":                 (0, 0, 0, "Z"),
    "SU(5)":                 (0, 0, 0, "Z"),
    "E6":                    (0, 0, 0, "Z"),
    "SU(3)xSU(2)xU(1) [SM]": (0, "Z", 0, "Z"),
    "U(1)xSU(3)":            (0, "Z", 0, "Z"),
    "U(1)xSU(5)":            (0, "Z", 0, "Z"),
    "U(1)":                  (0, "Z", 0, 0),
    "SO(10)":                (0, "Z2", 0, "Z"),
}


def anomaly_checks():
    """§5 SM 反常相消检验（一代，4 个条件；须**精确**为零）。

    条件：
      grav-U(1)  : Σ n3·n2·Y          = 0
      SU(2)^2 U(1): Σ_{SU(2) doublet} n3·Y = 0
      SU(3)^2 U(1): Σ_{SU(3) triplet} n2·Y = 0
      U(1)^3     : Σ n3·n2·Y^3        = 0
    """
    grav = Fraction(0)
    su2 = Fraction(0)
    su3 = Fraction(0)
    u1c = Fraction(0)
    for name, n3, n2, Y in SM_LEFT_HANDED:
        grav += n3 * n2 * Y
        u1c += n3 * n2 * Y ** 3
        if n2 == 2:
            su2 += n3 * Y
        if n3 == 3:
            su3 += n2 * Y
    return {"grav-U(1)": grav, "[SU(2)]^2 U(1)": su2,
            "[SU(3)]^2 U(1)": su3, "[U(1)]^3": u1c}


def hypercharge_lattice():
    """§5 超荷晶格：把 Y 用 1/6 为单位写出 ⇒ 观测到的『整数模式』。"""
    unit = Fraction(1, 6)
    rows = []
    for name, n3, n2, Y in SM_LEFT_HANDED:
        rows.append((name, n3, n2, Y, Y / unit))
    return rows


def signature_groups():
    """§3 【核心】按同伦签名分组：证明拓扑**不唯一**选出 SM。"""
    groups = {}
    for grp, sig in HOMOTOPY_SIGNATURE.items():
        groups.setdefault(sig, []).append(grp)
    return groups


def coupling_ratios():
    """§6 三耦合比值（归一化到 alpha_1）。"""
    a1 = ALPHA_1_MZ
    return {"alpha_s/alpha_1": ALPHA_S_MZ / a1,
            "alpha_2/alpha_1": ALPHA_2_MZ / a1,
            "alpha_1/alpha_1": 1.0}


def winding_charge(n):
    """§2 电荷量子化演示：场 e^{i n phi} 的缠绕数 n ∈ Z ⇒ 电荷离散。

    注意（诚实）：观测到的电荷量子是 **e/3**（夸克 ±1/3、±2/3），
    单纯 U(1) 缠绕给的是**整数** e ⇒ 仍需**超荷归一化**（大统一 / 磁单极）
    才能把 e/3 解释为量子。这一环与原稿所声称的『缠绕直接给出电荷』**不同**。
    """
    if int(n) != n:
        raise ValueError("缠绕数必须为整数")
    return int(n), int(n)  # (缠绕数, 电荷量子数/e)


def _demo():
    print("=" * 72)
    print("补充卷H：规范结构的拓扑起源 —— 划界实跑")
    print("=" * 72)

    print("\n[允许侧 A] 电荷量子化（§2）")
    for n in (-2, -1, 0, 1, 2):
        w, q = winding_charge(n)
        print("  缠绕数 n=%-3d -> 电荷 = %+d e" % (w, q))
    print("  ⇒ 拓扑**可以**解释『电荷为何量子化』（离散），此点成立。")
    print("  ⚠ 但观测量子是 e/3（夸克），整数缠绕给 e ⇒ 仍需外生超荷归一化。")

    print("\n[允许侧 B] 手征零模（§4，Atiyah-Singer）")
    print("  拓扑指数 ind(D) = n_L - n_R ≠ 0 ⇒ **可以**产生手征零模（离散净个数）。")
    print("  ⇒ 『拓扑不能给手征』是**错误**的过强表述；拓扑给的是**净手征数**，不是表示内容。")

    print("\n" + "=" * 72)
    print("[禁止侧 1] 【核心】同伦签名**不唯一**选出 SM（§3）")
    print("=" * 72)
    groups = signature_groups()
    for sig, members in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print("  pi=(%s)  ->  %d 个候选群: %s" % (
            ",".join(str(s) for s in sig), len(members), ", ".join(members)))
    multi = {s: m for s, m in groups.items() if len(m) >= 2}
    print("\n  ⇒ 签名 (0,0,0,Z) 被 %d 个**完全不同**的群共享（秩 1..6）；" % len(groups[(0, 0, 0, "Z")]))
    print("     签名 (0,Z,0,Z) 被 %d 个群共享（含 SM）。" % len(groups[(0, "Z", 0, "Z")]))
    print("  ⇒ 缺陷分类数据**不足以**选出 SU(3)xSU(2)xU(1)：『自然导出』(唯一性) **失败**。")

    print("\n" + "=" * 72)
    print("[禁止侧 2] 耦合常数的值/比值无拓扑来源（§6，撞定理 C/D）")
    print("=" * 72)
    for k, v in coupling_ratios().items():
        print("  %-16s = %.4f" % (k, v))
    print("  ⇒ alpha_s : alpha_2 : alpha_1(M_Z) = %.4f : %.4f : 1.0000" % (
        ALPHA_S_MZ / ALPHA_1_MZ, ALPHA_2_MZ / ALPHA_1_MZ))
    print("     无任何拓扑不变量给出该比值；且三者**跑动**(beta != 0) ⇒ 撞定理 C（无跑动）。")

    print("\n" + "=" * 72)
    print("[约束侧] 反常相消：是**约束**，不是导出（§5）")
    print("=" * 72)
    print("  一代 SM（全左手 Weyl 约定）超荷：")
    for name, n3, n2, Y, lat in hypercharge_lattice():
        print("    %-20s n3=%d n2=%d  Y=%-6s (=%d/6)" % (name, n3, n2, str(Y), lat))
    print("  四个反常条件（须**精确**为 0）：")
    ok = True
    for k, v in anomaly_checks().items():
        flag = "OK" if v == 0 else "**非零**"
        if v != 0:
            ok = False
        print("    %-16s = %-6s  [%s]" % (k, str(v), flag))
    print("  ⇒ 全部为 0（%s）== SM 超荷赋值被反常相消**精确约束**。" % ("成立" if ok else "不成立"))
    print("     任何『从拓扑导出超荷』的构造**必须复现**这 4 个条件；本卷未给出该推导。")
    print("     超荷晶格 = {1,4,2,3,6}/6 ⇒ 非单一缠绕模式（需外生的分数量子化）。")

    print("\n" + "=" * 72)
    print("结论")
    print("=" * 72)
    print("  允许侧（成立）：电荷量子化 ✅、手征零模净数 ✅（离散量由拓扑编码）")
    print("  禁止侧（失败）：群的选择 ❌（同伦签名非唯一）、耦合比值 ❌（无来源）、")
    print("                  具体表示/超荷赋值 ❌（外生；反相消为约束而非导出）")
    print("  ⇒ 强宣称『从丛缠绕自然导出 SU(3)xSU(2)xU(1)』= **结构性失败**；")
    print("     拓扑给『离散外壳』，不给『群的选择与连续参数』（定理 B 两侧的分界）。")


def _selfhash():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 72)
    print("本文件 SHA256 =", _selfhash())
    print("定位：脚手架 + 划界工具（非预言）。数学自洽 != 实验证实。")
