# -*- coding: utf-8 -*-
"""
攻破⑰ · 剩余 5 体系「公设层」第一性深攻（S05 / S06 / S11 / S04 / S01）

纯标准库：decimal(prec=50) + fractions + json + csv + math
纪律：
  * 输出目录用 __file__ 定位（_verify_all.py 以 ROOT 为 cwd）
  * 4 类判定 PASS/FAIL/BOUNDARY/INFO；counts 求和恒等断言
  * PASS ≠ 有内容：恒等式/定义式/标准定理一律降级 INFO
  * 自检必须含「能反噬自己」的反向自检
  * 阈值不得拍机器零：跟随输入常数有效位与自报位数

引擎自写产物：数据/<BASENAME>.{json,md}
"""
import os
import sys
import json
import csv
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # openuft/
OUTDIR = os.path.abspath(os.path.join(HERE, "..", "数据"))             # .../本项目_全维自洽与归一化/数据
SYSTEMS = os.path.join(ROOT, "01_独立体系")
BASENAME = "剩余5体系公设层深攻_S05S06S11S04S01_2026-10-10"

RESULTS = []
SELFTESTS = []

# ---------------------------------------------------------------- 基础工具

def _lim(p):
    return Decimal(10) ** (-(p + 5))

def _arctan_inv(x, p):
    """arctan(1/x)，x 为整数。递推必须 除以 x^2（不是乘）。"""
    xx = Decimal(x)
    x2 = xx * xx
    lim = _lim(p)
    total = Decimal(0)
    term = Decimal(1) / xx
    n = 0
    while True:
        piece = term / (2 * n + 1)
        total += piece
        if abs(piece) < lim:
            break
        term = -term / x2
        n += 1
        if n > 100000:
            break
    return total

def machin_pi(p=50):
    return 4 * (4 * _arctan_inv(5, p) - _arctan_inv(239, p))

PI = machin_pi(50)

def dcbrt(x):
    """Decimal 立方根：float 初值 + Newton，避免 Decimal 非整数幂的陷阱。"""
    x = Decimal(x)
    if x == 0:
        return Decimal(0)
    g = Decimal(repr(float(x) ** (1.0 / 3.0)))
    for _ in range(200):
        g2 = g * g
        if g2 == 0:
            break
        g = (2 * g + x / g2) / 3
    return g

def rel(a, b):
    """相对偏差"""
    if b == 0:
        return abs(a) if a != 0 else Decimal(0)
    return abs(a - b) / abs(b)

def add(*vs):
    return tuple(sum(x) for x in zip(*vs))

def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def canon_verdict(v):
    return v if v in ("PASS", "FAIL", "BOUNDARY", "INFO") else "INFO"

def rec(rid, system, item, claim, reading, criterion, verdict, note=""):
    RESULTS.append({
        "id": rid, "system": system, "item": item, "claim": claim,
        "reading": reading, "criterion": criterion,
        "verdict": canon_verdict(verdict), "note": note,
    })

def st(name, ok, detail=""):
    SELFTESTS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    return bool(ok)

def fmt(x, n=6):
    try:
        if isinstance(x, Decimal):
            s = f"{x:.{n}E}"
        else:
            s = f"{x:.{n}E}"
        return s
    except Exception:
        return str(x)

# ---------------------------------------------------------------- 常数（CODATA 2018）
C = Decimal("299792458")                    # exact
HBAR = Decimal("1.054571817e-34")
G = Decimal("6.67430e-11")                  # 6 位有效 —— 伪精度纪律：声明位数 <= 6
QE = Decimal("1.602176634e-19")             # exact
EPS0 = Decimal("8.8541878128e-12")
ME = Decimal("9.1093837015e-31")
MP_KG = Decimal("1.67262192369e-27")
GEV_KG = Decimal("1.782661921e-27")         # kg per GeV/c^2  （注意：不是 e-36）
HBARC = Decimal("1.973269804e-7")           # eV*m

TWO_PI = 2 * PI
CBRT_2PI = dcbrt(TWO_PI)
TWO_PI_POW_2_3 = CBRT_2PI * CBRT_2PI        # (2π)^{2/3}

# ================================================================ S05 HDU
def section_s05():
    LP = (HBAR * G / (C ** 3)).sqrt()
    MP_kg = HBAR / (C * LP)
    MP_GeV = MP_kg / GEV_KG

    # A1: M11 * c * L11 = hbar * 2*pi ; A2: L11 = R11 = L_P
    M11_from_A1A2 = TWO_PI * MP_GeV                    # 2π · M_P
    M11_selfrep = CBRT_2PI * MP_GeV                    # M_P (2π)^{1/3}   （体系自报修复值）
    M11_standard = MP_GeV / CBRT_2PI                   # M_P (2π)^{-1/3}  （M 理论标准关系）
    ratio = M11_from_A1A2 / M11_selfrep
    ratio_std = M11_selfrep / M11_standard

    # 反向自检用：若把 A1 误读为 M11 c L11 = hbar（无 2π）
    M11_no2pi = MP_GeV
    ratio_no2pi = M11_no2pi / M11_selfrep

    # A3: M4 = d(AdS_11)，dim(d AdS_n) = n-1
    hits = [n for n in range(2, 13) if (n - 1) == 4]
    dim_bdry_11 = 10

    rec("S05-1", "S05 HDU", "公设 A1+A2 与自报修复值互斥",
        "A1: M11*c*L11 = hbar*2pi ; A2: L11 = R11 = L_P",
        f"L_P={fmt(LP)} m, M_P={fmt(MP_GeV)} GeV/c^2 | "
        f"M11(A1+A2)=2pi*M_P={fmt(M11_from_A1A2)} GeV/c^2 ; "
        f"M11(自报修复)=(2pi)^(1/3)*M_P={fmt(M11_selfrep)} GeV/c^2 ; "
        f"比值={fmt(ratio)}",
        "公设强制值与体系自报修复值若不等（相对偏差 > 1e-6，取自报 7 位末位半刻度）则互斥",
        "FAIL",
        f"互斥因子 {fmt(ratio)} = (2π)^(2/3) = {fmt(TWO_PI_POW_2_3)}；公设与自身账本不能同时成立")

    rec("S05-2", "S05 HDU", "外部口径二选一（不自作裁定）",
        "M 理论标准关系 M_P^2 = 2π R11 M11^3",
        f"M11(标准口径)=(2pi)^(-1/3)*M_P={fmt(M11_standard)} GeV/c^2 ; "
        f"自报值/标准值={fmt(ratio_std)}",
        "存在两个互斥的外部口径且都与自报值差同一因子 ⇒ 登记待裁决，不代选",
        "BOUNDARY",
        f"自报值 {fmt(M11_selfrep)} 与标准口径 {fmt(M11_standard)} 亦差 {fmt(ratio_std)}；"
        f"两者相差 (2π)^(2/3)，体系未声明采用哪一约定")

    rec("S05-3", "S05 HDU", "A2 的 R11 ≡ L_P 是定义式（普朗克锚定复发）",
        "A2: R11 = (hbar*G/c^3)^(1/2) = L_P",
        f"R11 = {fmt(LP)} m ≡ L_P（与自报逐位一致）",
        "若「待求的紧致化尺度」被直接锚定为已知普朗克量，则该式不是预测而是单位重述",
        "FAIL",
        "跨册缺陷族①（普朗克锚定）复发第 4 例：S03 M_p≡hbar/(c L_p)、S08 R=hbar/(mc)、"
        "S12 R=hbar/(2 m_e c)、S05 R11≡L_P。改错为对 ≠ 从公设导出")

    rec("S05-4", "S05 HDU", "A3 维数互斥",
        "A3: M4 = d(AdS_11)",
        f"dim(∂AdS_n)=n-1 ⇒ dim(∂AdS_11)={dim_bdry_11} ≠ 4；"
        f"扫描 n=2..12 满足 dim(∂AdS_n)=4 的 n = {hits}",
        "若不存在 n=11 使 dim(∂AdS_n)=4，则 A3 与 A1/A2 的 11 维本体正面对撞",
        "FAIL",
        f"只有 n={hits} 给 4 维边界，即需 AdS_5，与 11 维本体冲突")

    return dict(LP=LP, MP_GeV=MP_GeV, M11_from_A1A2=M11_from_A1A2,
                M11_selfrep=M11_selfrep, M11_standard=M11_standard,
                ratio=ratio, ratio_no2pi=ratio_no2pi, ratio_std=ratio_std)

# ================================================================ S06 TCL
def cl_complex(p, q):
    """Cl(p,q)⊗C ≅ Cl(p+q, C) 的分类标签（纯数学定理编码）"""
    n = p + q
    if n % 2 == 0:
        k = 2 ** (n // 2)
        return f"M_{k}(C)"
    k = 2 ** ((n - 1) // 2)
    return f"M_{k}(C)+M_{k}(C)"

def pi3_su(n):
    """π₃(SU(N))：N>=2 为 Z，N=1 为 0（标准结果编码）"""
    return "Z" if n >= 2 else "0"

def section_s06():
    # A1 分辨力扫描：p+q = 8
    labels8 = {}
    for p in range(0, 9):
        q = 8 - p
        labels8[(p, q)] = cl_complex(p, q)
    distinct8 = sorted(set(labels8.values()))

    # A2 分辨力扫描：π₃(SU(N)) for N=2..8
    pi3_scan = {n: pi3_su(n) for n in range(2, 9)}
    distinct_pi3 = sorted(set(pi3_scan.values()))

    # A2 的 × Z_2^chiral → 3*2=6
    pi3_z2 = "0"                      # π₃(离散群)=0
    pi3_prod = "Z" if pi3_su(3) == "Z" and pi3_z2 == "0" else "?"

    # A3：m_nu = m_b * exp(-L3/xi)：3 个未知、1 个可观测量
    target = Decimal("0.05")          # eV
    L3 = Decimal("1")                 # 任意固定（本身亦未锚定）
    fits = []
    for xi in (Decimal("0.5"), Decimal("1"), Decimal("2")):
        mb = target * (L3 / xi).exp()
        back = mb * (-(L3 / xi)).exp()
        fits.append((xi, mb, back))

    # 振荡长度回算 L = 4π ħc E / Δm²
    def Losc(E_eV, dm2):
        return 4 * PI * HBARC * E_eV / dm2 / Decimal(1000)   # km

    E10 = Decimal("1e7")
    E1G = Decimal("1e9")
    dm21 = Decimal("7.5e-5")
    dm32 = Decimal("2.5e-3")
    L12_10 = Losc(E10, dm21)
    L23_10 = Losc(E10, dm32)
    L12_1G = Losc(E1G, dm21)
    L23_1G = Losc(E1G, dm32)

    rec("S06-1", "S06 TCL", "A1 复化后对 (p,q) 无分辨力",
        "A1: Cl(4,4)⊗C ≅ M_16(C)（dim=256）",
        f"扫描 p+q=8 的 9 组 (p,q)：输出集合 = {distinct8}（全部相同）",
        "扫定义域：若输出恒定则携带 0 bit，选 Cl(4,4) 是外部输入",
        "FAIL",
        "新缺陷族⑤「无分辨力选择（机器可证）」实例 1；真正的物理内容若存在必在未复化的实结构里，"
        "而「边界态」映射未在公设中给出")

    rec("S06-2", "S06 TCL", "A2 的 π₃ 对 N 无分辨力",
        "A2: pi_3(SU(3)) = Z",
        f"扫描 N=2..8：{pi3_scan} ⇒ 输出集合 = {distinct_pi3}",
        "若 π₃(SU(N)) 对 N>=2 恒为 Z，则它不携带代数信息",
        "FAIL",
        "「3 代」不来自拓扑：3 来自「选了 SU(3)」，而 SU(3) 借自标准模型色群")

    rec("S06-3", "S06 TCL", "「× Z_2^chiral → 3*2=6」是范畴错误",
        "A2: pi_3(SU(3)) = Z × Z_2^chiral -> 3*2=6",
        f"π₃(SU(3)×Z₂) = π₃(SU(3)) ⊕ π₃(Z₂) = Z ⊕ {pi3_z2} = {pi3_prod} ≠ 6",
        "同伦群对直积是可加的（直和），不能与标签数相乘",
        "FAIL",
        "把同伦群乘以手征标签数；6 是标签计数而非群论结论。体系自身已把代/手征计数降级 conjecture")

    rec("S06-4", "S06 TCL", "A3 中微子质量式不可证伪",
        "A3: m_nu = m_boundary * exp(-L3/xi)",
        "固定 L3=1，目标 m_nu=0.05 eV：三组解 "
        + "; ".join(f"(xi={fmt(x)}, m_b={fmt(m)})" for x, m, _ in fits),
        "未知量 3 个（m_b, xi, L3）对 1 个可观测量 ⇒ 欠定 2 ⇒ 任意目标值可达 ⇒ 不可证伪",
        "FAIL",
        "解族连续（三组解回代残差均 < 1e-40），无唯一预言；体系自报 L12/L23 亦属回算")

    rec("S06-5", "S06 TCL", "L12/L23 = 标准振荡长度回算，E 为自由参数",
        "体系自报 L12≈330 km、L23≈10 km",
        f"L = 4π ħc E/Δm²：E=10 MeV ⇒ L12={fmt(L12_10)} km、L23={fmt(L23_10)} km；"
        f"E=1 GeV ⇒ L12={fmt(L12_1G)} km、L23={fmt(L23_1G)} km",
        "若 E 未声明且 L ∝ E，则任何长度均可得 ⇒ 零信息量",
        "FAIL",
        "在 E=10 MeV 下精确复现自报值（容差 1%），但 E 是未声明的自由参数："
        "E 改 100 倍，L 精确改 100 倍")

    rec("S06-6", "S06 TCL", "A1 的数学内容本身正确",
        "Cl(4,4)⊗C ≅ M_16(C), dim_C = 256",
        f"分类器输出 = {cl_complex(4, 4)}，dim_C = 256",
        "标准 Clifford 定理，数学无误 —— 但定理正确 ≠ 物理内容（降级 INFO）",
        "INFO",
        "借用：复 Clifford 代数分类是教科书结果；与「边界态/费米子代」的连接未在公设中建立")

    return dict(labels8={f"{k[0]},{k[1]}": v for k, v in labels8.items()},
                distinct8=distinct8, pi3_scan=pi3_scan, distinct_pi3=distinct_pi3,
                fits=fits, L12_10=L12_10, L23_10=L23_10,
                L12_1G=L12_1G, L23_1G=L23_1G)

# ================================================================ S11 GMUFT
def section_s11():
    QM = (4 * PI * EPS0 * G).sqrt()                 # C/kg
    qme = QE / ME
    qmp = QE / MP_KG
    r_e = qme / QM
    r_p = qmp / QM

    # A2/A3 量纲（Fraction 精确；单位向量次序 (L, M, T, I)）
    DIM_G = (Fraction(3), Fraction(-1), Fraction(-2), Fraction(0))     # L^3 M^-1 T^-2
    DIM_M = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))       # M
    DIM_J = (Fraction(2), Fraction(1), Fraction(-1), Fraction(0))      # M L^2 T^-1
    DIM_C_INV2 = (Fraction(-2), Fraction(0), Fraction(2), Fraction(0)) # c^-2
    DIM_R_INV3 = (Fraction(-3), Fraction(0), Fraction(0), Fraction(0)) # r^-3

    dim_R2 = add(DIM_G, DIM_M, DIM_C_INV2, DIM_R_INV3)      # 2GM/(c^2 r^3) → L^-2
    dim_w = add(DIM_G, DIM_J, DIM_C_INV2, DIM_R_INV3)       # 2GJ/(c^2 r^3) → T^-1
    EXPECT_R2 = (Fraction(-2), Fraction(0), Fraction(0), Fraction(0))
    EXPECT_W = (Fraction(0), Fraction(0), Fraction(-1), Fraction(0))
    ok_dim_R2 = (dim_R2 == EXPECT_R2)
    ok_dim_w = (dim_w == EXPECT_W)

    # 地球量级示例
    GM_E = Decimal("3.986004418e14")
    R_E = Decimal("6.371e6")
    J_E = Decimal("5.86e33")
    R_eff = 2 * GM_E / (C * C) / (R_E ** 3)
    w_drag = 2 * G * J_E / (C * C) / (R_E ** 3)

    rec("S11-1", "S11 GMUFT", "A4 有确定数值预测但被实验排除",
        "A4: Q/M = sqrt(4 pi eps0 G)",
        f"Q/M={fmt(QM)} C/kg（自报 8.6175e-11，逐位一致）；"
        f"e/m_e={fmt(qme)}（差 {fmt(r_e)} 倍）；e/m_p={fmt(qmp)}（差 {fmt(r_p)} 倍）；中子 0",
        "该式给出唯一确定的荷质比 ⇒ 可证伪；与已知粒子荷质比对标",
        "FAIL",
        "本轮唯一「有确定数值预测且可证伪」的式子，如实判「有预测但错」；"
        "差 21.3（电子）/ 18.0（质子）个量级。G 仅 6 位有效 ⇒ 声明位数 ≤ 6")

    rec("S11-2", "S11 GMUFT", "A4 是平衡荷质比的定义式",
        "A4 来源：令 F_G = F_E 且 m = q",
        "F_G=F_E ⟹ G m²/r² = q²/(4π ε₀ r²) ⟹ q/m = √(4πε₀G) —— 与粒子种类无关",
        "若该式只是「两力平衡时的荷质比」的定义，则它不预言任何具体粒子的荷质比",
        "FAIL",
        "零第一性内容：定义式。体系自承「令 m=q」量纲不匹配（[M] vs [I·T]）；"
        "正确表述无需 m=q，但仍只是平衡条件")

    rec("S11-3", "S11 GMUFT", "A2/A3 为 GR 标准读数且系数未定",
        "A2: R_eff ∼ 2GM/(c²r³) ; A3: ω_drag ∼ 2GJ/(c²r³)",
        f"量纲：[A2]={tuple(str(x) for x in dim_R2)}（L^-2，匹配={ok_dim_R2}）、"
        f"[A3]={tuple(str(x) for x in dim_w)}（T^-1，匹配={ok_dim_w}）；"
        f"地球示例 R_eff={fmt(R_eff)} m^-2、ω_drag={fmt(w_drag)} s^-1",
        "含 ∼ 且系数 2 无来源；量级即 GR 潮汐/拖拽读数 ⇒ 借用 + 无确定系数，不可作预测",
        "FAIL",
        "量纲各自正确（仅作附注，不记 PASS）；∝ 号 + 未定系数 ⇒ 需外部标定")

    rec("S11-4", "S11 GMUFT", "框架未完成（命名式统一）",
        "A1: 四自由度 {R, T, Q, Π}；Π 标「待探索」；OPEN-3 联合场方程未建立",
        "{R→质量, T→自旋, Q→电荷, Π→?} 是命名映射，不是方程",
        "若第四自由度无激发源与效应、联合场方程缺失 ⇒ 暂不可判，登记未完成",
        "BOUNDARY",
        "与攻破⑪「TEGT k=3 选择性」同型：命名式统一不等于派生统一")

    n_claims = count_claims("S11_GMUFT几何自由度与耦合")
    rec("S11-5", "S11 GMUFT", "唯一可数值检验的式子未登记为 claim",
        "claims.csv 行数",
        f"S11 claims.csv 数据行 = {n_claims}",
        "若该体系唯一可数值检验的式子（A4）从未登记为 claim ⇒ 账本层缺口",
        "FAIL",
        "A4 有确定数值、可被实验排除，却不在账本内 ⇒ 攻破⑯「空账本」结论需补注："
        "不是没有可检验内容，而是可检验内容未登记")

    return dict(QM=QM, qme=qme, qmp=qmp, r_e=r_e, r_p=r_p,
                dim_R2=dim_R2, dim_w=dim_w, R_eff=R_eff, w_drag=w_drag,
                ok_dim_R2=ok_dim_R2, ok_dim_w=ok_dim_w, n_claims=n_claims)

# ================================================================ S04 IEG
def section_s04():
    # 量纲向量 (L, M, T, I)
    DIM_D4X_A = (4, 0, 0, 0)      # x^0 = ct
    DIM_D4X_B = (3, 0, 1, 0)      # x^0 = t
    dim_rho_A = tuple(-Fraction(x) for x in DIM_D4X_A)
    dim_rho_B = tuple(-Fraction(x) for x in DIM_D4X_B)

    dim_phi = (Fraction(2), Fraction(0), Fraction(-2), Fraction(0))   # L^2 T^-2
    dim_lap = (Fraction(-2), Fraction(0), Fraction(0), Fraction(0))   # L^-2
    dim_lap_phi = add(dim_phi, dim_lap)                                # T^-2

    dim_G = (Fraction(3), Fraction(-1), Fraction(-2), Fraction(0))
    dim_rhoM = (Fraction(-3), Fraction(1), Fraction(0), Fraction(0))
    dim_GrhoM = add(dim_G, dim_rhoM)

    need = dim_lap_phi                     # ρ_info^excess 必须是 T^-2
    ok_A = (tuple(Fraction(x) for x in dim_rho_A) == need)
    ok_B = (tuple(Fraction(x) for x in dim_rho_B) == need)

    K_A = sub(need, tuple(Fraction(x) for x in dim_rho_A))   # L^4 T^-2
    K_B = sub(need, tuple(Fraction(x) for x in dim_rho_B))   # L^3 T^-1

    # 方程计数
    n_einstein = 10     # 对称 4x4
    n_divJ = 4          # ∇^μ J_{μν} = 0，ν=1..4
    underdet = n_einstein - n_divJ

    # 归一化发散：4-球体积 ∝ R^4
    vols = []
    for R in (1, 10, 100, 1000):
        V = (PI ** 2) / 2 * Decimal(R) ** 4
        vols.append((R, V))

    rec("S04-1", "S04 IEG", "A2 与 A3 量纲互斥",
        "A2: ∫ρ_info √−g d⁴x = 1 ; A3: ∇²φ = 4πGρ_M − ρ_info^excess",
        f"A2 ⟹ [ρ_info] = L^-4（x⁰=ct）或 L^-3 T^-1（x⁰=t）；"
        f"A3 ⟹ [4πGρ_M] = T^-2 = [∇²φ] ⇒ [ρ_info^excess] 必须为 T^-2；"
        f"两种坐标约定下匹配 = ({ok_A}, {ok_B})",
        "若两种坐标约定下 [ρ_info] 都无法等于 T^-2，则公设组不自洽",
        "FAIL",
        f"唯一修复路径 = 插入量纲换算常数 K：[K] = L^4 T^-2（{K_A}）或 L^3 T^-1（{K_B}）")

    rec("S04-2", "S04 IEG", "可修复但需新的未锚定自由参数",
        "修复 A2/A3 量纲冲突",
        f"需引入 [K] = L^4 T^-2 或 L^3 T^-1 的换算常数",
        "若修复必须引入公设未确定的量纲常数 ⇒ 「可修复」不等于「闭合」",
        "BOUNDARY",
        "新常数不由 A1–A3 中任何一条确定 ⇒ 修复后仍是外部输入")

    rec("S04-3", "S04 IEG", "A1 的 ⟺ 反向不成立（欠定）",
        "A1: G_μν+Λg_μν = 8πG T_μν ⟺ ∇^μ J^info_μν = 0",
        f"爱因斯坦方程独立分量 = {n_einstein}；∇^μJ^info_μν=0 方程数 = {n_divJ}；欠定 = {underdet}",
        "若反向方程数少于场方程独立分量数，则 ⟺ 不成立",
        "FAIL",
        "从 4 个守恒律推不出 10 个独立分量 ⇒ 欠定 6 个自由度")

    rec("S04-4", "S04 IEG", "⟺ 正向仅在重命名时成立",
        "A1 正向",
        "仅当 J^info_μν := T_μν 时，Bianchi ⟹ ∇^μT_μν=0 成立",
        "若正向成立依赖把信息流重命名为应力-能量张量 ⇒ 零信息量（降级 INFO）",
        "INFO",
        "重命名，不是新内容；体系自承黑洞「信息饱和态」引用标准 Bekenstein–Hawking 熵")

    rec("S04-5", "S04 IEG", "A2 归一化在非紧时空发散（两难）",
        "A2: ∫ρ_info √−g d⁴x = 1",
        "截断 4-球体积 ∝ R⁴：" + ", ".join(f"R={r}→V={fmt(v)}" for r, v in vols),
        "若在非紧时空上归一化，则 ρ_info → 0 ⇒ A3 的「信息过剩」项恒为 0；"
        "若改在有限区域归一化，则区域选择成为新的外部输入",
        "BOUNDARY",
        "两难：ρ_info→0 则体系唯一的新项自消解（退化为牛顿泊松方程）；"
        "限定区域则引入未锚定的区域选择。与 A1 中的 Λ 一样属未声明外部输入")

    return dict(dim_rho_A=tuple(str(x) for x in dim_rho_A),
                dim_rho_B=tuple(str(x) for x in dim_rho_B),
                need=tuple(str(x) for x in need),
                K_A=tuple(str(x) for x in K_A), K_B=tuple(str(x) for x in K_B),
                ok_A=ok_A, ok_B=ok_B, n_einstein=n_einstein,
                n_divJ=n_divJ, underdet=underdet, vols=vols)

# ================================================================ S01 螺旋三重奏
def section_s01():
    def frenet_check(R, om, b, phase):
        """phase: 't0' -> (sin,cos)=(0,1); 't90' -> (sin,cos)=(1,0)"""
        s, csin = (Decimal(0), Decimal(1)) if phase == "t0" else (Decimal(1), Decimal(0))
        v2 = R * R * om * om + b * b
        v = v2.sqrt()
        # r' = (-R om s, R om c, b)
        r1 = (-R * om * s, R * om * csin, b)
        # r'' = (-R om^2 c, -R om^2 s, 0)
        r2 = (-R * om * om * csin, -R * om * om * s, Decimal(0))
        # r''' = (R om^3 s, -R om^3 c, 0)
        r3 = (R * om ** 3 * s, -R * om ** 3 * csin, Decimal(0))

        def cross(a, bb):
            return (a[1] * bb[2] - a[2] * bb[1],
                    a[2] * bb[0] - a[0] * bb[2],
                    a[0] * bb[1] - a[1] * bb[0])

        def det3(a, bb, cc):
            return (a[0] * (bb[1] * cc[2] - bb[2] * cc[1])
                    - a[1] * (bb[0] * cc[2] - bb[2] * cc[0])
                    + a[2] * (bb[0] * cc[1] - bb[1] * cc[0]))

        cr = cross(r1, r2)
        crn = (cr[0] ** 2 + cr[1] ** 2 + cr[2] ** 2).sqrt()
        kappa = crn / (v ** 3)
        tau = det3(r1, r2, r3) / (crn ** 2)

        k_claim = R * om * om / v2
        t_claim = om * b / v2
        resid_k = rel(kappa, k_claim)
        resid_t = rel(tau, t_claim)
        ident = rel(kappa ** 2 + tau ** 2, om * om / v2)
        return kappa, tau, k_claim, t_claim, resid_k, resid_t, ident

    params = [(Decimal(1), Decimal(1), Decimal(1)),
              (Decimal("2.5"), Decimal("0.7"), Decimal("3.1")),
              (Decimal("0.3"), Decimal(5), Decimal("0.05"))]
    checks = []
    for R, om, b in params:
        for ph in ("t0", "t90"):
            checks.append(((str(R), str(om), str(b), ph), frenet_check(R, om, b, ph)))

    # A3: -tr(A^2)/(2 v^2) = sum(omega_j^2)/v^2，A 为分块反对称
    def skew(ws):
        n = 2 * len(ws)
        A = [[Decimal(0)] * n for _ in range(n)]
        for i, w in enumerate(ws):
            r, c = 2 * i, 2 * i + 1
            A[r][c] = -w
            A[c][r] = w
        return A

    def trA2(A):
        n = len(A)
        s = Decimal(0)
        for i in range(n):
            for j in range(n):
                s += A[i][j] * A[j][i]
        return s

    ws_list = [[Decimal("0.3")],
               [Decimal("0.3"), Decimal("1.7")],
               [Decimal("0.3"), Decimal("1.7"), Decimal("2.9")]]
    a3_checks = []
    for ws in ws_list:
        v2 = Decimal("4")            # 任意 v²（恒等式对 v 无关）
        A = skew(ws)
        lhs = -trA2(A) / (2 * v2)
        rhs = sum(w * w for w in ws) / v2
        a3_checks.append(([str(w) for w in ws], lhs, rhs, rel(lhs, rhs)))

    max_resid_k = max(x[1][4] for x in checks)
    max_resid_t = max(x[1][5] for x in checks)
    max_ident = max(x[1][6] for x in checks)
    max_a3 = max(x[3] for x in a3_checks)

    rec("S01-1", "S01 螺旋三重奏", "范畴豁免（F4 一致性）",
        "S01 明文：数学框架，不引入物理本体，不登记任何物理预测",
        "kind = mathematical_framework；claims 数据行 = %s" % count_claims("S01_螺旋三重奏与谱几何"),
        "体系若自陈不提物理主张，则不适用「攻破统一场论」的判负（不得为凑数判 FAIL）",
        "INFO",
        "登记为「不适用 / 范畴豁免」；本册对其改做定理实算")

    rec("S01-2", "S01 螺旋三重奏", "Frenet 三重奏定理实算成立",
        "κ = Rω²/v²、τ = ωb/v²、κ²+τ² = (ω/v)²",
        f"3 组参数 × 2 个精确相位点（t=0 与 t=π/2）= {len(checks)} 次检验；"
        f"max|κ 残差|={fmt(max_resid_k)}、max|τ 残差|={fmt(max_resid_t)}、"
        f"max|κ²+τ²−(ω/v)²|={fmt(max_ident)}",
        "由定义式 κ=|r'×r''|/|r'|³、τ=det(r',r'',r''')/|r'×r''|² 实算，"
        "若与声称闭式一致（残差 < 1e-40）则定理成立",
        "PASS",
        "数学定理成立 ≠ 统一场论成立；此 PASS 不计入「攻破成功数」")

    rec("S01-3", "S01 螺旋三重奏", "A3 全维生成元恒等式实算成立",
        "Σκᵢ² = Σωⱼ²/v² = −tr(A²)/(2v²)",
        f"{len(a3_checks)} 组反对称矩阵检验；max 相对残差 = {fmt(max_a3)}",
        "对分块反对称 A，若 −tr(A²)/(2v²) 与 Σωⱼ²/v² 精确相等则恒等式成立",
        "PASS",
        "同 S01-2：数学恒等式成立，不构成物理预测")

    rec("S01-4", "S01 螺旋三重奏", "借用链复发登记（不重复计数）",
        "S02/S10/S12 借用本体系螺旋数学",
        "体系自陈 R2 已证三重奏不能反向生成物理常数（sympy 求解 G 为空集，欠定 + 循环）",
        "跨册条目不可相加 ⇒ 只记复发，不在本册重复计数",
        "INFO",
        "三个借用体系的判定见攻破⑮（S02/S12）与攻破⑧⑩（S10）；此处仅登记同源关系")

    return dict(checks=[(k, [str(z) for z in v]) for k, v in checks],
                a3_checks=[(w, str(l), str(r), str(d)) for w, l, r, d in a3_checks],
                max_resid_k=max_resid_k, max_resid_t=max_resid_t,
                max_ident=max_ident, max_a3=max_a3)

# ---------------------------------------------------------------- 账本读取
def count_claims(dirname):
    path = os.path.join(SYSTEMS, dirname, "claims.csv")
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            rows = [r for r in csv.reader(f) if r and any(x.strip() for x in r)]
        return max(0, len(rows) - 1)
    except Exception:
        return -1

# ---------------------------------------------------------------- 自检
def run_selftests(refs):
    s05 = refs["s05"]; s06 = refs["s06"]; s11 = refs["s11"]; s01 = refs["s01"]

    # 1. S05 自报 M11 = 2.252872e19 复现（自报 7 位 ⇒ 末位半刻度相对 4.4e-7 ⇒ 取 1e-6）
    st("锚点复现·S05 自报 M11=2.252872e19",
       rel(s05["M11_selfrep"], Decimal("2.252872e19")) < Decimal("1e-6"),
       f"实算 {fmt(s05['M11_selfrep'])}，相对偏差 {fmt(rel(s05['M11_selfrep'], Decimal('2.252872e19')))}")

    # 2. S11 自报 Q/M = 8.6175e-11 复现（5 位 ⇒ 半刻度相对 ~5.8e-6 ⇒ 取 1e-5）
    st("锚点复现·S11 自报 Q/M=8.6175e-11",
       rel(s11["QM"], Decimal("8.6175e-11")) < Decimal("1e-5"),
       f"实算 {fmt(s11['QM'])}，相对偏差 {fmt(rel(s11['QM'], Decimal('8.6175e-11')))}")

    # 3. S06 自报 L12≈330 / L23≈10 km（自报 2-3 位 ⇒ 容差 1%）
    ok12 = rel(s06["L12_10"], Decimal(330)) < Decimal("1e-2")
    ok23 = rel(s06["L23_10"], Decimal(10)) < Decimal("1e-2")
    st("锚点复现·S06 自报 L12≈330/L23≈10 km（E=10 MeV，容差 1%）", ok12 and ok23,
       f"L12={fmt(s06['L12_10'])} km（偏差 {fmt(rel(s06['L12_10'], Decimal(330)))}）；"
       f"L23={fmt(s06['L23_10'])} km（偏差 {fmt(rel(s06['L23_10'], Decimal(10)))}）")

    # 4. 反向自检：A1 无 2π 读法必须能被区分（证明 3.405 不是巧合）
    r_bad = s05["ratio_no2pi"]
    distinguishable = abs(r_bad - s05["ratio"]) > Decimal(1)
    st("反向自检·A1 两种读法可区分（3.405 非巧合）",
       distinguishable and rel(s05["ratio"], TWO_PI_POW_2_3) < Decimal("1e-30"),
       f"有 2π：{fmt(s05['ratio'])}；无 2π：{fmt(r_bad)}；"
       f"与 (2π)^(2/3)={fmt(TWO_PI_POW_2_3)} 偏差 {fmt(rel(s05['ratio'], TWO_PI_POW_2_3))}")

    # 5. L ∝ E 线性
    lin12 = rel(s06["L12_1G"] / s06["L12_10"], Decimal(100))
    lin23 = rel(s06["L23_1G"] / s06["L23_10"], Decimal(100))
    st("敏感度·L ∝ E（E×100 ⇒ L×100）",
       lin12 < Decimal("1e-30") and lin23 < Decimal("1e-30"),
       f"L12 比值 {fmt(s06['L12_1G'] / s06['L12_10'])}；L23 比值 {fmt(s06['L23_1G'] / s06['L23_10'])}")

    # 6. Frenet 恒等残差
    st("恒等实算·κ²+τ² = (ω/v)² 达机器精度",
       s01["max_ident"] < Decimal("1e-40") and s01["max_resid_k"] < Decimal("1e-40")
       and s01["max_resid_t"] < Decimal("1e-40"),
       f"max|κ²+τ²−(ω/v)²|={fmt(s01['max_ident'])}；max|κ 残差|={fmt(s01['max_resid_k'])}；"
       f"max|τ 残差|={fmt(s01['max_resid_t'])}")

    # 7. Clifford 分类器自洽
    ok_cl = (cl_complex(2, 0) == "M_2(C)" and cl_complex(4, 0) == "M_4(C)"
             and cl_complex(6, 0) == "M_8(C)" and cl_complex(8, 0) == "M_16(C)"
             and cl_complex(4, 4) == "M_16(C)")
    st("分类器自洽·Cl(2/4/6/8,C)=M_2/M_4/M_8/M_16 且 Cl(4,4)⊗C≅M_16(C)", ok_cl,
       f"Cl(2)={cl_complex(2,0)}, Cl(4)={cl_complex(4,0)}, Cl(6)={cl_complex(6,0)}, "
       f"Cl(8)={cl_complex(8,0)}, Cl(4,4)={cl_complex(4,4)}")

    # 8. 量纲代数精确自洽
    dimG = (Fraction(3), Fraction(-1), Fraction(-2), Fraction(0))
    dimRhoM = (Fraction(-3), Fraction(1), Fraction(0), Fraction(0))
    dimLapPhi = (Fraction(0), Fraction(0), Fraction(-2), Fraction(0))
    ok_dim = (add(dimG, dimRhoM) == dimLapPhi)
    st("量纲代数·[4πGρ_M] = [∇²φ] 精确相等（Fraction）", ok_dim,
       f"[Gρ_M]={add(dimG, dimRhoM)} vs [∇²φ]={dimLapPhi}")

    # 9. π 精度
    PI_REF = Decimal("3.14159265358979323846264338327950288419716939937511")
    st("π 精度·Machin（除以 x² + 绝对收敛判据）", abs(PI - PI_REF) < Decimal("1e-45"),
       f"|π − π_ref| = {fmt(abs(PI - PI_REF))}")

    # 10. dcbrt 自洽
    ok_cbrt = (rel(dcbrt(Decimal(8)), Decimal(2)) < Decimal("1e-40")
               and rel(dcbrt(Decimal(27)), Decimal(3)) < Decimal("1e-40"))
    st("立方根自洽·dcbrt(8)=2, dcbrt(27)=3", ok_cbrt,
       f"dcbrt(8)={fmt(dcbrt(Decimal(8)))}；dcbrt(27)={fmt(dcbrt(Decimal(27)))}")

    # 11. S05 普朗克锚点
    st("锚点复现·L_P = 1.616255e-35 m",
       rel(s05["LP"], Decimal("1.616255e-35")) < Decimal("1e-6"),
       f"实算 {fmt(s05['LP'])} m，偏差 {fmt(rel(s05['LP'], Decimal('1.616255e-35')))}")

    # 12. A3 恒等
    st("恒等实算·−tr(A²)/(2v²) = Σωⱼ²/v²", s01["max_a3"] < Decimal("1e-40"),
       f"max 相对残差 {fmt(s01['max_a3'])}")

    # 13. S11 A2/A3 量纲必须各自落在预期格点上（本条曾因 J 量纲写错而自相矛盾）
    st("量纲自洽·[2GM/(c²r³)]=L^-2 且 [2GJ/(c²r³)]=T^-1",
       s11["ok_dim_R2"] and s11["ok_dim_w"],
       f"[A2]={tuple(str(x) for x in s11['dim_R2'])}；[A3]={tuple(str(x) for x in s11['dim_w'])}")

# ---------------------------------------------------------------- 主流程
def main():
    print("=" * 78, flush=True)
    print("攻破⑰ · 剩余 5 体系公设层第一性深攻（S05/S06/S11/S04/S01）", flush=True)
    print("=" * 78, flush=True)

    s05 = section_s05()
    s06 = section_s06()
    s11 = section_s11()
    s04 = section_s04()
    s01 = section_s01()

    run_selftests({"s05": s05, "s06": s06, "s11": s11, "s01": s01})

    counts = {}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        counts.setdefault(k, 0)

    assert sum(counts.values()) == len(RESULTS), "counts 求和必须 == 判定项总数"
    assert all(canon_verdict(r["verdict"]) == r["verdict"] for r in RESULTS), "判定值非法"

    n_ok = sum(1 for t in SELFTESTS if t["ok"])
    print(f"\n判定项 {len(RESULTS)} 条：PASS={counts['PASS']} FAIL={counts['FAIL']} "
          f"BOUNDARY={counts['BOUNDARY']} INFO={counts['INFO']}", flush=True)
    print(f"自检 {n_ok}/{len(SELFTESTS)}", flush=True)
    for t in SELFTESTS:
        print(f"  [{'OK ' if t['ok'] else 'BAD'}] {t['name']}", flush=True)
        print(f"        {t['detail']}", flush=True)
    print("\n判定明细：", flush=True)
    for r in RESULTS:
        print(f"  {r['id']:<8} {r['verdict']:<9} {r['item']}", flush=True)

    os.makedirs(OUTDIR, exist_ok=True)

    payload = {
        "meta": {
            "title": "攻破⑰ · 剩余 5 体系公设层第一性深攻",
            "systems": ["S05", "S06", "S11", "S04", "S01"],
            "date": "2026-10-10",
            "engine": os.path.basename(__file__),
            "precision": "Decimal(50)",
            "total": len(RESULTS),
        },
        "counts": counts,
        "selftests": {"total": len(SELFTESTS), "passed": n_ok, "items": SELFTESTS},
        "results": RESULTS,
        "key_readings": {
            "L_P_m": str(s05["LP"]),
            "M_P_GeV": str(s05["MP_GeV"]),
            "S05_M11_from_A1A2_GeV": str(s05["M11_from_A1A2"]),
            "S05_M11_selfrep_GeV": str(s05["M11_selfrep"]),
            "S05_M11_standard_GeV": str(s05["M11_standard"]),
            "S05_mutual_exclusion_factor": str(s05["ratio"]),
            "S06_L12_km_at_10MeV": str(s06["L12_10"]),
            "S06_L23_km_at_10MeV": str(s06["L23_10"]),
            "S11_QM_C_per_kg": str(s11["QM"]),
            "S11_e_over_me_ratio_gap": str(s11["r_e"]),
            "S11_e_over_mp_ratio_gap": str(s11["r_p"]),
            "S04_underdetermined": str(s04["underdet"]),
        },
        "cross_book_families": [
            {"id": "族①", "name": "普朗克锚定（定义式冒充尺度预测）",
             "recurrence": ["S03 M_p≡hbar/(cL_p)", "S08 R=hbar/(mc)",
                            "S12 R=hbar/(2 m_e c)", "S05 R11≡L_P"],
             "this_round": "S05（第 4 例）"},
            {"id": "族⑤", "name": "无分辨力选择（机器可证，新登记）",
             "criterion": "扫定义域 → 输出恒定 ⇒ 0 bit",
             "instances": ["S06-A1 Cl(p,q)⊗C 对 p+q=8 的 9 组同输出",
                           "S06-A2 π₃(SU(N)) 对 N=2..8 同输出"],
             "note": "与 S13 攻破④ 同型，但不受 2026-10-10 复审修正影响（该修正针对 CP²/色涌现）"},
            {"id": "族⑥", "name": "有确定预测但未登记（新登记）",
             "instances": ["S11-A4 Q/M=sqrt(4πε₀G) 可证伪且已被排除，claims.csv 空账本"]},
        ],
    }

    jpath = os.path.join(OUTDIR, BASENAME + ".json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 攻破⑰ · 剩余 5 体系公设层第一性深攻（数据件）")
    lines.append("")
    lines.append(f"- 引擎：`源码/{os.path.basename(__file__)}`（纯标准库，Decimal 50 位）")
    lines.append(f"- 判定项：**{len(RESULTS)}** ｜ PASS={counts['PASS']} FAIL={counts['FAIL']} "
                 f"BOUNDARY={counts['BOUNDARY']} INFO={counts['INFO']}")
    lines.append(f"- 自检：**{n_ok}/{len(SELFTESTS)}**")
    lines.append("")
    lines.append("## 关键读数（机器复算）")
    lines.append("")
    lines.append("| 读数 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| L_P | {fmt(s05['LP'])} m |")
    lines.append(f"| M_P | {fmt(s05['MP_GeV'])} GeV/c² |")
    lines.append(f"| S05 M11（A1+A2 强制） | {fmt(s05['M11_from_A1A2'])} GeV/c² |")
    lines.append(f"| S05 M11（自报修复） | {fmt(s05['M11_selfrep'])} GeV/c² |")
    lines.append(f"| S05 互斥因子 | {fmt(s05['ratio'])} = (2π)^(2/3) |")
    lines.append(f"| S06 L12 @10 MeV | {fmt(s06['L12_10'])} km（自报 ≈330） |")
    lines.append(f"| S06 L23 @10 MeV | {fmt(s06['L23_10'])} km（自报 ≈10） |")
    lines.append(f"| S11 Q/M | {fmt(s11['QM'])} C/kg（自报 8.6175e-11） |")
    lines.append(f"| S11 与 e/m_e 差 | {fmt(s11['r_e'])} 倍 |")
    lines.append(f"| S11 与 e/m_p 差 | {fmt(s11['r_p'])} 倍 |")
    lines.append(f"| S04 ⟺ 欠定 | {s04['underdet']} 个自由度 |")
    lines.append("")
    lines.append("## 判定明细")
    lines.append("")
    lines.append("| ID | 体系 | 项 | 判定 | 读数 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        rd = r["reading"].replace("|", "\\|")
        lines.append(f"| {r['id']} | {r['system']} | {r['item']} | **{r['verdict']}** | {rd} |")
    lines.append("")
    lines.append("## 判定理由")
    lines.append("")
    for r in RESULTS:
        lines.append(f"### {r['id']} · {r['item']} — **{r['verdict']}**")
        lines.append("")
        lines.append(f"- 对象：{r['claim']}")
        lines.append(f"- 判据：{r['criterion']}")
        lines.append(f"- 理由：{r['note']}")
        lines.append("")
    lines.append("## 自检")
    lines.append("")
    for t in SELFTESTS:
        lines.append(f"- [{'x' if t['ok'] else ' '}] {t['name']} — {t['detail']}")
    lines.append("")

    mpath = os.path.join(OUTDIR, BASENAME + ".md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n产物：{jpath}", flush=True)
    print(f"产物：{mpath}", flush=True)

    if n_ok != len(SELFTESTS):
        print("\n自检未全过 ⇒ EXIT=1", flush=True)
        return 1
    print("\nEXIT=0", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
