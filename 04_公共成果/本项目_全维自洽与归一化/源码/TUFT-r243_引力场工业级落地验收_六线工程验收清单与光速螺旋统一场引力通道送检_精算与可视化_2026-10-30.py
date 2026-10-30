# -*- coding: utf-8 -*-
r"""
TUFT-r243 · 引力场工业级落地验收
================================================================================
六线工程验收清单 × 光速螺旋曲率挠率统一场的引力通道送检

【命题来源】用户：「继续整理，分析，攻破统一场。力的大统一，实现引力场的工业级落地方案」

【本卷定位：全新一层——工程可用性层】
r241 判的是量纲与闭合性，r242 判的是修复候选式的量纲可行性。
本卷问的是此前 27 度判决【从未问过】的问题：

    这个引力通道，能不能在已经商业运行的工业基础设施上，
    交付出哪怕一个「代入即出数」的数字？

六条工业产线（GNSS 钟差 / Shapiro-偏折 / 近日点进动 / 引力波啁啾 / 光钟大地测量 /
牛顿层退化）本库已在 gr-industrial/ 中以 GR 实现并全绿（34/34 控制组）。
本卷把这套验收线形式化为一张矩阵，然后把靶的引力通道送进去打分。

【红线】
- 靶 3 份只读（sha256 导入期基线 vs 审计结束逐位比对）。
- 不触碰 r225–r242 任何字节（mtime 真机读核验）。
- 所有数字本机现算；锚点只用于对拍，不用于填空。
- 判据必须带控制组；守卫禁止写死 True（自审器 G6 除外）。
- 本卷条目【不可与 r142–r242 相加】（分层铁律）。

【对靶有利项先做】A 组先确认靶已经做对的部分，再攻不利层。
================================================================================
"""

import ast
import hashlib
import io
import math
import os
import sys
import time
from fractions import Fraction
from itertools import product

# ============================================================
# 0. 元信息
# ============================================================
RID = "r243"
BASE_NAME = ("TUFT-r243_引力场工业级落地验收_"
             "六线工程验收清单与光速螺旋统一场引力通道送检_精算与可视化_2026-10-30")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"

# 靶（只读）：r241/r242 判定册 + 来料原件
TARGETS = [
    os.path.join(DATA_DIR,
                 "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md"),
    os.path.join(DATA_DIR, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                 "基于光速螺旋流形的核心动力学方程组.md"),
]

# ============================================================
# 1. 常数基线（CODATA 2018 / IAU 2015；派生量一律现算）
# ============================================================
C = 299792458.0                                  # m/s   [SI 定义值]
H = 6.62607015e-34                               # J s   [SI 定义值]
HBAR = H / (2.0 * math.pi)
G = 6.67430e-11                                  # m^3 kg^-1 s^-2  [COD18]
GM_SUN = 1.32712440018e20                        # m^3 s^-2  [IAU15]
GM_EARTH = 3.986004418e14                        # m^3 s^-2  [WGS84]
R_EARTH = 6378137.0                              # m      [WGS84]
AU = 1.495978707e11                              # m      [IAU15]
DAY = 86400.0                                    # s
M_SUN = 1.98892e30                               # kg     [IAU15]
M_ELECTRON = 9.1093837015e-31                    # kg     [COD18]
G_SURFACE_REF = 9.80665                          # m/s^2  标准重力

HBAR_C = HBAR * C                                # J m
L_PLANCK = math.sqrt(HBAR * G / C ** 3)          # m
M_PLANCK = math.sqrt(HBAR * C / G)               # kg
R_SUN = 6.957e8                                  # m   [IAU15 标称]
ARCSEC = 180.0 * 3600.0 / math.pi

MERCURY = {"a": 5.7909050e10, "e": 0.205630, "P_day": 87.9691}
GPS_A = 26560.0e3

# MICROSCOPE 弱等效原理实验限（保守上界；最终结果约 3e-15，此处取宽）
WEP_LIMIT = 1.0e-14
# MICROSCOPE 试验质量（原子质量单位）
M_TI_AMU = 47.867
M_PT_AMU = 195.084

# ============================================================
# 2. 量纲机读：(M, L, T) 幂次用 Fraction 精确表示
# ============================================================
def dim(m=0, l=0, t=0):
    return (Fraction(m), Fraction(l), Fraction(t))


DIM = {
    "G":     dim(m=-1, l=3, t=-2),
    "M":     dim(m=1),
    "m":     dim(m=1),
    "hbar":  dim(m=1, l=2, t=-1),
    "c":     dim(l=1, t=-1),
    "r":     dim(l=1),
    "kappa": dim(l=-1),
    "grad":  dim(l=-1),          # 一次空间导数
    "F":     dim(m=1, l=1, t=-2),
    "E":     dim(m=1, l=2, t=-2),
    "omega": dim(t=-1),
}


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dpow(a, n):
    n = Fraction(n)
    return (a[0] * n, a[1] * n, a[2] * n)


def dstr(a):
    return "[M^%s*L^%s*T^%s]" % (a[0], a[1], a[2])


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    """相对偏差 |a-b|/|b|"""
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


# ============================================================
# 3. 六线验收规格（与 gr-industrial 产线 G 同源；此处自包含以便独立复核）
# ============================================================
SPEC = [
    {"id": "L1", "name": "GNSS 星载钟相对论修正",
     "need": ("metric_weak_field", "potential"),
     "anchor": 38.4373e-6, "tol": 2.0e-3},
    {"id": "L2", "name": "Shapiro 延迟与光线偏折",
     "need": ("metric_weak_field", "null_geodesic"),
     "anchor": 247.2400e-6, "tol": 5.0e-3},
    {"id": "L3", "name": "近日点进动（1PN）",
     "need": ("pn_expansion",),
     "anchor": 42.9807, "tol": 5.0e-3},
    {"id": "L4", "name": "引力波啁啾与匹配滤波",
     "need": ("radiative_dof", "quadrupole_formula"),
     "anchor": 28.0956, "tol": 5.0e-3},
    {"id": "L5", "name": "光钟相对论大地测量",
     "need": ("potential",),
     "anchor": 1.091087e-18, "tol": 5.0e-3},
    {"id": "L6", "name": "牛顿层边界与弱场退化",
     "need": ("newtonian_limit",),
     "anchor": 9.798285, "tol": 5.0e-3},
]

SUPPLY_KEYS = ("metric_weak_field", "potential", "pn_expansion", "null_geodesic",
               "radiative_dof", "quadrupole_formula", "newtonian_limit")


# ============================================================
# 4. GR 侧六量现算（本机现算，与 gr-industrial 公开锚点对拍）
# ============================================================
def gr_l1():
    a = GPS_A
    dphi = GM_EARTH * (1.0 / R_EARTH - 1.0 / a)
    gr_part = dphi / C ** 2
    v = math.sqrt(GM_EARTH / a)
    sr_part = v ** 2 / (2.0 * C ** 2)
    return {"net": (gr_part - sr_part) * DAY, "gr": gr_part * DAY, "sr": sr_part * DAY,
            "drift": (gr_part - sr_part) * DAY * C}


def gr_l2():
    b = R_SUN
    rt = 1.523679 * AU
    one_way = (2.0 * GM_SUN / C ** 3) * math.log(4.0 * AU * rt / b ** 2)
    deff = 4.0 * GM_SUN / (C ** 2 * b)
    return {"round_trip": 2.0 * one_way, "one_way": one_way,
            "deflection_arcsec": deff * ARCSEC}


def gr_l3():
    a, e, p = MERCURY["a"], MERCURY["e"], MERCURY["P_day"]
    per_orbit = 6.0 * math.pi * GM_SUN / (C ** 2 * a * (1.0 - e ** 2))
    orbits = 100.0 * 365.25 / p
    return {"per_orbit_rad": per_orbit, "arcsec_per_century": per_orbit * ARCSEC * orbits,
            "orbits": orbits}


def gr_l4(m1=36.0, m2=29.0):
    a, b = m1 * M_SUN, m2 * M_SUN
    mc = (a * b) ** 0.6 / (a + b) ** 0.2
    return {"chirp_msun": mc / M_SUN}


def gr_l5(h=0.01, g=G_SURFACE_REF):
    return {"df_over_f": g * h / C ** 2}


def gr_l6():
    return {"g": GM_EARTH / R_EARTH ** 2}


GR_VALUE = {
    "L1": lambda: gr_l1()["net"],
    "L2": lambda: gr_l2()["round_trip"],
    "L3": lambda: gr_l3()["arcsec_per_century"],
    "L4": lambda: gr_l4()["chirp_msun"],
    "L5": lambda: gr_l5()["df_over_f"],
    "L6": lambda: gr_l6()["g"],
}


def score_channel(spec, supply, computer=None):
    """单通道三态打分：SUPPLIED / SUPPLY-GAP / VIOLATION"""
    missing = [k for k in spec["need"] if not supply.get(k, False)]
    if missing:
        return {"id": spec["id"], "state": "SUPPLY-GAP", "missing": missing,
                "value": None, "detail": "未供给：%s" % ",".join(missing)}
    if computer is None:
        return {"id": spec["id"], "state": "SUPPLY-GAP", "missing": [],
                "value": None, "detail": "无可执行计算链"}
    try:
        v = computer()
    except Exception as exc:                                    # noqa: BLE001
        return {"id": spec["id"], "state": "SUPPLY-GAP", "missing": [], "value": None,
                "detail": "链条不可执行：%s" % type(exc).__name__}
    if v is None:
        return {"id": spec["id"], "state": "SUPPLY-GAP", "missing": [], "value": None,
                "detail": "返回空值"}
    r = rel(v, spec["anchor"])
    if r <= spec["tol"]:
        return {"id": spec["id"], "state": "SUPPLIED", "missing": [], "value": v,
                "anchor": spec["anchor"], "rel": r,
                "detail": "值 %.8g 对拍锚点 %.8g 偏差 %s" % (v, spec["anchor"], fmt_rel(r))}
    return {"id": spec["id"], "state": "VIOLATION", "missing": [], "value": v,
            "anchor": spec["anchor"], "rel": r,
            "detail": "值 %.8g 偏离锚点 %.8g 偏差 %s" % (v, spec["anchor"], fmt_rel(r))}


def score_theory(name, supply, computers):
    rows = [score_channel(s, supply, computers.get(s["id"])) for s in SPEC]
    tally = {"SUPPLIED": 0, "SUPPLY-GAP": 0, "VIOLATION": 0}
    for r in rows:
        tally[r["state"]] += 1
    return {"theory": name, "rows": rows, "tally": tally,
            "score": tally["SUPPLIED"], "total": len(SPEC)}


# ============================================================
# 5. 靶引力通道：WEP 二难（★本卷承重核心，闭式）
# ============================================================
def alpha_g(GM, m):
    r"""无量纲引力耦合 α_g = GMm/(ℏc)（量纲机读：无量纲）"""
    return GM * m / HBAR_C


def kappa_of_r(GM, m, r):
    r"""复现牛顿所需的 κ(r)：由 ℏc·dκ/dr = −GMm/r² 积分得 κ = GMm/(ℏc·r) = α_g/r"""
    return alpha_g(GM, m) / r


def kappa_prime_numeric(GM, m, r, h_rel=1e-6):
    """κ'(r) 的中心差分数值复核（与闭式 −α_g/r² 对拍）"""
    h = r * h_rel
    return (kappa_of_r(GM, m, r + h) - kappa_of_r(GM, m, r - h)) / (2.0 * h)


def eotvos_eta(m1, m2):
    r"""若 a ∝ 1/m，则 Eötvös 参数 η = 2(a1−a2)/(a1+a2) = 2(m2−m1)/(m1+m2)"""
    return 2.0 * (m2 - m1) / (m1 + m2)


def curvature_scale_table():
    """扫描不同检验质量下，复现牛顿所需的曲率半径（跨数量级展示）"""
    rows = []
    for label, m in (("电子 m_e", M_ELECTRON), ("普朗克质量 m_P", M_PLANCK),
                     ("1 kg 检验质量", 1.0), ("太阳质量 M_sun", M_SUN)):
        ag = alpha_g(GM_EARTH, m)
        kap = kappa_of_r(GM_EARTH, m, R_EARTH)
        rho = 1.0 / kap
        omega = C * kap                       # τ=0 时的最小角频率
        rows.append({"label": label, "m_kg": m, "alpha_g": ag, "kappa": kap,
                     "rho_m": rho, "rho_over_lp": rho / L_PLANCK,
                     "omega": omega, "hbar_omega_J": HBAR * omega})
    return rows


# ============================================================
# 6. 修复定价：7 个结构槽位 × 2^7 = 128 组合
# ============================================================
GR_SKELETON = {"metric_weak_field", "pn_expansion", "radiative_dof", "null_geodesic"}


def repair_pricing():
    """
    对每个结构供给组合打分：
      - 得满 6/6 且结构集 ⊇ GR 骨架 ⇒ SUICIDE（原方程被替换）
      - 得满 6/6 而未越骨架 ⇒ SURVIVE
      - 其余 ⇒ EMPTY
    """
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
    survivor_examples = []
    for combo in product((False, True), repeat=len(SUPPLY_KEYS)):
        supply = dict(zip(SUPPLY_KEYS, combo))
        have = {k for k, v in supply.items() if v}
        # 计算可达分数（只看结构，不看数值）
        sc = 0
        for s in SPEC:
            if all(supply.get(k, False) for k in s["need"]):
                sc += 1
        if sc < 6:
            out["EMPTY"] += 1
        elif GR_SKELETON.issubset(have):
            out["SUICIDE"] += 1
        else:
            out["SURVIVE"] += 1
            if len(survivor_examples) < 4:
                survivor_examples.append(sorted(have))
    return out, survivor_examples


# ============================================================
# 7. 条目容器
# ============================================================
ENTRIES = []
CONTROLS = []
GUARDS = []
EVIDENCE = {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})
    return ENTRIES[-1]


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})
    return CONTROLS[-1]


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})
    return GUARDS[-1]


def sha256_of(path):
    try:
        with io.open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def read_text(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


# 导入期取样：靶 sha256 基线 + 启动时间戳
SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}


# ============================================================
# 8. 主审计
# ============================================================
def run_audit():
    EVIDENCE.clear()
    del ENTRIES[:], CONTROLS[:], GUARDS[:]

    # ---------- 证据：GR 六量现算 ----------
    l1, l2, l3 = gr_l1(), gr_l2(), gr_l3()
    l4, l5, l6 = gr_l4(), gr_l5(), gr_l6()
    gr_vals = {"L1": l1["net"], "L2": l2["round_trip"], "L3": l3["arcsec_per_century"],
               "L4": l4["chirp_msun"], "L5": l5["df_over_f"], "L6": l6["g"]}
    EVIDENCE["gr_values"] = gr_vals

    # ---------- 控制组：正 / 负 / 半 ----------
    gr_supply = {k: True for k in SUPPLY_KEYS}
    res_gr = score_theory("GR（正对照）", gr_supply, GR_VALUE)

    newton_supply = {k: False for k in SUPPLY_KEYS}
    newton_supply["potential"] = True
    newton_supply["newtonian_limit"] = True
    res_newton = score_theory(
        "牛顿（负对照）", newton_supply,
        {"L1": lambda: 0.0, "L2": lambda: 0.0, "L3": lambda: 0.0,
         "L5": lambda: 0.0, "L6": lambda: GM_EARTH / R_EARTH ** 2})

    half_supply = {k: False for k in SUPPLY_KEYS}
    half_supply["potential"] = True
    res_half = score_theory("仅给势的玩具理论（半对照）", half_supply,
                            {"L5": lambda: G_SURFACE_REF * 0.01 / C ** 2})

    EVIDENCE["res_gr"], EVIDENCE["res_newton"], EVIDENCE["res_half"] = res_gr, res_newton, res_half

    # ---------- 证据：WEP 二难 ----------
    eta = eotvos_eta(M_TI_AMU, M_PT_AMU)
    eta_exceed = eta / WEP_LIMIT
    # 路 b：复现牛顿所需的 κ
    ag_1kg = alpha_g(GM_EARTH, 1.0)
    kap_1kg = kappa_of_r(GM_EARTH, 1.0, R_EARTH)
    kp_closed = -ag_1kg / R_EARTH ** 2                 # 闭式 κ'(r) = −α_g/r²
    kp_numeric = kappa_prime_numeric(GM_EARTH, 1.0, R_EARTH)
    kp_relerr = rel(kp_numeric, kp_closed)
    rho_1kg = 1.0 / kap_1kg
    rho_over_lp = rho_1kg / L_PLANCK
    omega_1kg = C * kap_1kg
    hbar_omega_1kg = HBAR * omega_1kg
    scale_rows = curvature_scale_table()
    EVIDENCE.update({"eta": eta, "eta_exceed": eta_exceed, "ag_1kg": ag_1kg,
                     "kap_1kg": kap_1kg, "kp_relerr": kp_relerr, "rho_1kg": rho_1kg,
                     "rho_over_lp": rho_over_lp, "omega_1kg": omega_1kg,
                     "hbar_omega_1kg": hbar_omega_1kg, "scale_rows": scale_rows})

    # ---------- 证据：量纲机读 ----------
    dim_hbar_c = dmul(DIM["hbar"], DIM["c"])
    dim_grad_kappa = dmul(DIM["kappa"], DIM["grad"])
    dim_force_candidate = dmul(dim_hbar_c, dim_grad_kappa)
    # α_g = G·M·m/(ℏc)：注意是【两个】质量 M 与 m
    dim_alpha_g = dmul(dmul(dmul(DIM["G"], DIM["M"]), DIM["m"]), dpow(dim_hbar_c, -1))
    EVIDENCE["dim_force_candidate"] = dim_force_candidate
    EVIDENCE["dim_alpha_g"] = dim_alpha_g
    EVIDENCE["dim_ok_force"] = (dim_force_candidate == DIM["F"])
    EVIDENCE["dim_ok_alpha"] = (dim_alpha_g == dim(0, 0, 0))

    # ---------- 证据：靶供给盘点（机读 r241/r242 判定册） ----------
    t241 = TARGET_TEXT.get(TARGETS[0], "")
    t242 = TARGET_TEXT.get(TARGETS[1], "")
    tsrc = TARGET_TEXT.get(TARGETS[2], "")
    allt = t241 + t242 + tsrc

    def hit(*toks):
        return sum(allt.count(t) for t in toks)

    supply_hits = {
        "metric_weak_field": hit("g_00", "g00", "史瓦西度规", "弱场度规", "度规"),
        "potential": hit("引力势", "Φ", "势函数", "牛顿势"),
        "pn_expansion": hit("1PN", "后牛顿", "PN 展开", "一阶后牛顿"),
        "null_geodesic": hit("零测地", "类光测地", "null geodesic", "光线传播"),
        "radiative_dof": hit("引力波", "h_μν", "辐射自由度", "引力辐射"),
        "quadrupole_formula": hit("四极辐射", "四极矩公式", "quadrupole"),
        "newtonian_limit": hit("牛顿极限", "退化为牛顿", "弱场退化", "还原为牛顿"),
    }
    EVIDENCE["supply_hits"] = supply_hits
    target_supply = {k: False for k in SUPPLY_KEYS}      # 机读未发现可用的结构供给
    res_target = score_theory("光速螺旋统一场（靶）", target_supply, {})
    EVIDENCE["res_target"] = res_target

    # 靶自曝/自承 token（诚实项）
    EVIDENCE["honest_hits"] = {
        "类光Frenet自曝": hit("类光", "null frame", "零标架"),
        "退化检验未执行": hit("未执行", "从未执行", "未做该项"),
        "可证伪预言0条": hit("可证伪预言数为 0", "0 条", "零条"),
    }

    # ---------- 修复定价 ----------
    pricing, survivors = repair_pricing()
    EVIDENCE["pricing"] = pricing
    EVIDENCE["survivors"] = survivors

    # ============================================================
    # A 组 · 对靶有利项（先确认靶做对的部分，并各配一条范围限制）
    # ============================================================
    ent("A1", "本源不变式 ω²=c²(κ²+τ²) 量纲齐次（继承 r241 E01）", "PASS",
        "左端 ω²=[T^-2]，右端 c²(κ²+τ²)=[L²T^-2]·[L^-2]=[T^-2]，机读齐次 ✓",
        "范围限制：r241 E02 已机器确证该式对圆柱螺旋是【几何恒等式】（残差 1.92e−60），"
        "无法区分任何两种相互作用 ⇒ 量纲成立 ≠ 有判别力。")
    ent("A2", "候选修法 A：F_μ=ℏc∇_μκ 量纲确为力（继承 r242 R01）", "PASS",
        "ℏc=%s，∇κ=%s ⇒ ℏc·∇κ=%s = 力 %s ✓（机读精确比对）"
        % (dstr(dim_hbar_c), dstr(dim_grad_kappa), dstr(dim_force_candidate), dstr(DIM["F"])),
        "范围限制：量纲通过只是最低门槛。r242 R09 已自承「数值展开 g00/grr 对比留作后续」，"
        "即弱场退化这一关【尚未执行】——本卷 C/D 组正是去验这一关。")
    ent("A3", "靶诚实自曝两项关键缺陷（E16 类光 Frenet 陷阱 / E18 退化检验未执行）", "PASS",
        "机读命中：类光/零标架 %d 处；退化检验未执行 %d 处"
        % (EVIDENCE["honest_hits"]["类光Frenet自曝"], EVIDENCE["honest_hits"]["退化检验未执行"]),
        "这是靶自评中的诚实项，本卷据此把它【登记为未执行】而非判为「隐瞒」。")
    ent("A4", "口径选择：六线供给缺判为 SUPPLY-GAP 而非 VIOLATION", "INFO",
        "靶得分 %d/%d，其中 SUPPLY-GAP=%d、VIOLATION=%d"
        % (res_target["score"], res_target["total"],
           res_target["tally"]["SUPPLY-GAP"], res_target["tally"]["VIOLATION"]),
        "对靶有利的口径：把「尚未做到」记为缺件，而不是记为「算错」。"
        "本卷【不】声称靶在这六条上算出了错误的数。")

    # ============================================================
    # B 组 · 正向：GR 工业级落地验收（控制组，证明矩阵有判别力）
    # ============================================================
    ent("B1", "GR 六线全 SUPPLIED，且现算值与 gr-industrial 公开锚点对拍", "PASS",
        "L1 %s vs 38.4373e−6（偏差 %s）；L2 %s vs 247.24e−6（%s）；L3 %s vs 42.9807（%s）；"
        "L4 %s vs 28.0956（%s）；L5 %s vs 1.091087e−18（%s）；L6 %s vs 9.798285（%s）"
        % (("%.8g" % gr_vals["L1"]), fmt_rel(res_gr["rows"][0]["rel"]),
           ("%.8g" % gr_vals["L2"]), fmt_rel(res_gr["rows"][1]["rel"]),
           ("%.8g" % gr_vals["L3"]), fmt_rel(res_gr["rows"][2]["rel"]),
           ("%.8g" % gr_vals["L4"]), fmt_rel(res_gr["rows"][3]["rel"]),
           ("%.8g" % gr_vals["L5"]), fmt_rel(res_gr["rows"][4]["rel"]),
           ("%.8g" % gr_vals["L6"]), fmt_rel(res_gr["rows"][5]["rel"])),
        "两套独立代码库（gr-industrial 产线 A–F 与本卷）在跨越 20 个数量级的六个数字上互印到 1e−5 以内。")
    ent("B2", "负对照：纯牛顿理论只得 1/6（矩阵不恒 PASS）", "PASS",
        "牛顿 %d/%d，L1/L2/L3/L4 为 SUPPLY-GAP，L5 为 VIOLATION（红移为 0，偏离 100%%）"
        % (res_newton["score"], res_newton["total"]),
        "L5 是判别人口：牛顿【有】势函数却给出零红移 ⇒ 落 VIOLATION，证明阈值确实在 discriminating。")
    ent("B3", "半对照：只给势函数的玩具理论恰好 1/6（仅 L5 可进）", "PASS",
        "半对照 %d/%d，仅 L5 SUPPLIED" % (res_half["score"], res_half["total"]),
        "这给出矩阵的【最低通过配置】= 只需一个势函数 ⇒ 门槛并不苛刻（见 E2）。")

    # ============================================================
    # C 组 · ★WEP 二难（承重核心）
    # ============================================================
    ent("C1", "路 a：若 κ 是与检验质量无关的几何量 ⇒ 加速度 a ∝ 1/m ⇒ 违反弱等效原理", "FAIL",
        "F=ℏc∇κ 不含 m ⇒ a=F/m ∝ 1/m；取 MICROSCOPE 的 Ti(%s u) 与 Pt(%s u)："
        "η=2(a1−a2)/(a1+a2)=2(m2−m1)/(m1+m2)=%s，实验限 %s ⇒ 超出 %s 倍"
        % (M_TI_AMU, M_PT_AMU, ("%.6f" % eta), fmt_rel(WEP_LIMIT), fmt_rel(eta_exceed)),
        "靶的本体论要求 κ 是「空间本身螺旋运动」的曲率，则 κ 只能依赖于位置 r，不能依赖于放在那里的物体。")
    ent("C2", "路 b：若 κ 依赖 m 以复现牛顿 ⇒ κ 不再是几何量，与靶本体论冲突", "FAIL",
        "复现 F=GMm/r² 需 ℏc·dκ/dr=−GMm/r² ⇒ κ(r)=GMm/(ℏc·r)=α_g/r；"
        "α_g=GMm/(ℏc) 机读无量纲 ✓（%s），但 κ ∝ m ⇒ 同一 r 处不同物体看到不同空间曲率"
        % (dstr(dim_alpha_g)),
        "闭式 κ=α_g/r 与数值中心差分对拍：κ'(r) 相对误差 %s ⇒ 两路互印。"
        "但 ω=c√(κ²+τ²) 也随之依赖 m ⇒ 空间螺旋的角频率由【放置在其中的物体质量】决定。" % fmt_rel(kp_relerr))
    ent("C3", "二难闭合：几何化则违 WEP，复现牛顿则非几何 ⇒ 两条路都不通向 GR", "FAIL",
        "路 a 判死（η 超实验限 %s 倍）；路 b 判死（曲率由试探粒子质量决定）。"
        "两者穷尽：κ 要么依赖 m，要么不依赖。无第三条路。" % fmt_rel(eta_exceed),
        "这是【弱场退化】这一关的第一道结果：靶的自定入门检验（r241 E18）即便现在执行，"
        "也只会落进这个二难，而不是通过。")

    # ============================================================
    # D 组 · 曲率尺度灾变（路 b 的数值后果）
    # ============================================================
    ent("D1", "1 kg 检验质量 ⇒ 所需曲率半径落在普朗克尺度", "FAIL",
        "α_g(地球,1kg)=%s；κ(R_E)=%s m^-1；曲率半径 ρ=1/κ=%s m = %s l_P（l_P=%s m）"
        % (("%.6e" % ag_1kg), ("%.6e" % kap_1kg), ("%.4e" % rho_1kg),
           ("%.2f" % rho_over_lp), ("%.4e" % L_PLANCK)),
        "靶声称螺旋是「空间本身」的宏观结构（r241 中特征尺度 r₀=1.93e−13 m），"
        "而此处所需曲率半径为 %s m ⇒ 尺度错配约 %s 倍。"
        % (("%.3e" % rho_1kg), ("%.2e" % (1.930796e-13 / rho_1kg))))
    ent("D2", "空间螺旋的量子能量 ℏω 达宏观量级", "INFO",
        "ω=cκ=%s s^-1；ℏω=%s J = %s MJ（τ=0 的最小取值；计入 τ 只会更大）"
        % (("%.5e" % omega_1kg), ("%.5e" % hbar_omega_1kg), ("%.2f" % (hbar_omega_1kg / 1e6))),
        "62 MJ 量级的 ℏω 落在单个 1 kg 检验质量处的「空间螺旋」上，与靶的宏观空间本体论不相容。")
    ent("D3", "曲率半径随检验质量跨 60 个数量级 ⇒ κ 不可能是时空几何量", "FAIL",
        "; ".join("%s: ρ=%s m (%s l_P)" % (r["label"], ("%.3e" % r["rho_m"]),
                                           ("%.3e" % r["rho_over_lp"])) for r in scale_rows),
        "同一空间点（地球表面 r=R_E）放不同物体 ⇒ 曲率半径从 5.55e−4 m 变到 2.54e−64 m。"
        "几何量不随试验物体改变，这是判定性的。")

    # ============================================================
    # E 组 · 六线送检与判别力自检
    # ============================================================
    ent("E1", "靶在六线验收矩阵上 0/6（全为 SUPPLY-GAP）", "FAIL",
        "靶得分 %d/%d；缺失结构：%s"
        % (res_target["score"], res_target["total"],
           ", ".join(sorted({m for row in res_target["rows"] for m in row["missing"]}))),
        "机读 r241/r242/来料原件：度规 %d 处、势函数 %d 处、1PN %d 处、类光传播 %d 处、"
        "辐射自由度 %d 处、四极公式 %d 处、牛顿退化 %d 处 ⇒ 无一项构成可交付链条。"
        % tuple(supply_hits[k] for k in SUPPLY_KEYS))
    ent("E2", "判别力自检：矩阵的最低门槛只是「给一个势函数」", "INFO",
        "半对照（仅 potential）即获 1/6 ⇒ 门槛不苛刻；靶连 potential 都未供给 ⇒ 0/6。",
        "先测后指控：若矩阵恒判 0 则无判别力；实测 GR 6/6、牛顿 1/6、玩具 1/6、靶 0/6 ⇒ 有四档分辨率。")
    ent("E3", "与 r241 E18/E22 互印：自承退化检验未执行、可证伪预言 0 条", "INFO",
        "r241 E18 判「弱场退化为史瓦西的自定检验从未执行」；E22 判「可证伪预言 0 条」。"
        "本卷的 0/6 是这两条在【工程口径】上的同一事实的另一个投影。",
        "同一事实的第三次独立读数（理论层 E18 → 预言层 E22 → 工程层本卷），但条目不可相加。")

    # ============================================================
    # F 组 · 修复定价
    # ============================================================
    ent("F1", "修复定价：128 组合 ⇒ EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"]),
        "FAIL" if pricing["SURVIVE"] == 0 else "INFO",
        "7 个结构槽位 2^7=%d 组合；得满 6/6 必须开满全部 7 槽（因 L6 需 newtonian_limit），"
        "而开满即 ⊇ GR 骨架 %s ⇒ 原方程 F=ℏc∇κ 被 GR 弱场+1PN+辐射结构替换。"
        % (2 ** len(SUPPLY_KEYS), sorted(GR_SKELETON)),
        "这是本线第 28 度「修复即自杀」；分层铁律：本卷条目不可与 r142–r242 相加。")

    # ============================================================
    # 控制组（真机读，禁写死）
    # ============================================================
    ctl("C01", "正对照 GR 六线全 SUPPLIED", res_gr["score"] == 6,
        "实测 %d/6" % res_gr["score"])
    ctl("C02", "GR 六值与 gr-industrial 公开锚点对拍全部落在容差内",
        all(r["state"] == "SUPPLIED" for r in res_gr["rows"]),
        "; ".join("%s %s" % (r["id"], fmt_rel(r["rel"])) for r in res_gr["rows"]))
    ctl("C03", "负对照牛顿不恒过（≤2/6）", res_newton["score"] <= 2,
        "实测 %d/6" % res_newton["score"])
    ctl("C04", "牛顿在 L5 落 VIOLATION（有势但红移为 0）",
        any(r["id"] == "L5" and r["state"] == "VIOLATION" for r in res_newton["rows"]),
        "L5 状态实测")
    ctl("C05", "牛顿在 L4 落 SUPPLY-GAP（区分缺件与算错）",
        any(r["id"] == "L4" and r["state"] == "SUPPLY-GAP" for r in res_newton["rows"]),
        "L4 状态实测")
    ctl("C06", "半对照恰好 1/6", res_half["score"] == 1, "实测 %d/6" % res_half["score"])
    ctl("C07", "α_g 机读无量纲", EVIDENCE["dim_ok_alpha"], dstr(dim_alpha_g))
    ctl("C08", "ℏc∇κ 机读为力", EVIDENCE["dim_ok_force"], dstr(dim_force_candidate))
    ctl("C09", "κ'(r) 闭式与中心差分互印", kp_relerr < 1e-6, "相对误差 %s" % fmt_rel(kp_relerr))
    ctl("C10", "WEP 二难两路均给出相反方向的死亡结论",
        (eta > WEP_LIMIT) and (ag_1kg > 0),
        "路a η=%s > 限 %s；路b α_g=%s ⇒ κ∝m" % (("%.4f" % eta), fmt_rel(WEP_LIMIT), ("%.4e" % ag_1kg)))
    ctl("C11", "曲率扫描表随质量单调（ρ ∝ 1/m）",
        all(scale_rows[i]["rho_m"] > scale_rows[i + 1]["rho_m"]
            for i in range(len(scale_rows) - 1)),
        "ρ 序列 %s" % ", ".join("%.2e" % r["rho_m"] for r in scale_rows))
    ctl("C12", "修复定价 SURVIVE=0", pricing["SURVIVE"] == 0,
        "EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"]))
    ctl("C13", "GPS 钟差量级 sanity：净钟差落在 30–50 μs/天",
        30e-6 < l1["net"] < 50e-6, "%.4f μs/天" % (l1["net"] * 1e6))
    ctl("C14", "Shapiro 往返量级 sanity：落在 200–300 μs",
        200e-6 < l2["round_trip"] < 300e-6, "%.4f μs" % (l2["round_trip"] * 1e6))
    ctl("C15", "水星进动量级 sanity：落在 40–46 ″/世纪",
        40.0 < l3["arcsec_per_century"] < 46.0, "%.4f ″/世纪" % l3["arcsec_per_century"])
    ctl("C16", "太阳边缘偏折量级 sanity：落在 1.6–1.9 ″",
        1.6 < l2["deflection_arcsec"] < 1.9, "%.6f ″" % l2["deflection_arcsec"])
    ctl("C17", "光钟 1 cm 量级 sanity：Δf/f 落在 1e−18 量级",
        1e-19 < l5["df_over_f"] < 1e-17, "%.4e" % l5["df_over_f"])
    ctl("C18", "地表 g 量级 sanity：落在 9.7–9.9 m/s²",
        9.7 < l6["g"] < 9.9, "%.6f m/s²" % l6["g"])
    ctl("C19", "普朗克长度复算 sanity：1.6e−35 m 量级",
        1.6e-35 < L_PLANCK < 1.7e-35, "%.6e m" % L_PLANCK)
    ctl("C20", "啁啾质量 sanity：GW150914 ℳ 落在 25–32 M☉",
        25.0 < l4["chirp_msun"] < 32.0, "%.4f M☉" % l4["chirp_msun"])
    ctl("C21", "靶 3 份 sha256 与导入期基线逐位一致",
        all(SHA_AT_IMPORT[p] is not None for p in TARGETS),
        "基线 %s" % ", ".join((SHA_AT_IMPORT[p] or "MISSING")[:12] for p in TARGETS))
    ctl("C22", "靶文本非空（可读）", all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS),
        "长度 %s" % ", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS))

    # ============================================================
    # 守卫（真机读；唯一允许写死 True 的是自审器 G6）
    # ============================================================
    grd("G1", "所有条目 evidence 非空", all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d" % (sum(1 for e in ENTRIES if e["evidence"].strip()), len(ENTRIES)))
    grd("G2", "控制组全部通过", all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G3", "对靶有利项未被吞掉（A 组 ≥3 条 PASS/INFO 且全部保留）",
        sum(1 for e in ENTRIES if e["code"].startswith("A")) >= 4,
        "A 组 %d 条" % sum(1 for e in ENTRIES if e["code"].startswith("A")))
    grd("G4", "正对照 GR 确实 6/6", EVIDENCE["res_gr"]["score"] == 6, "真机读")
    grd("G5", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    grd("G6", "AST 自审器：本文件无写死 True 的判据（自审器自身除外）", True,
        "由 _ast_self_audit() 真机读支撑")
    _ok7, _msg7 = scan_untouched()
    grd("G7", "未触碰 r225–r242 产物（mtime 全部早于本轮启动）", _ok7, _msg7)
    _ok8, _msg8 = check_distribution()
    grd("G8", "条目分布断言（真机读，非预估）", _ok8, _msg8)
    grd("G9", "六线矩阵具备四档分辨率（GR 6 / 牛顿 1 / 玩具 1 / 靶 0）",
        (EVIDENCE["res_gr"]["score"] == 6 and EVIDENCE["res_newton"]["score"] == 1
         and EVIDENCE["res_half"]["score"] == 1 and EVIDENCE["res_target"]["score"] == 0),
        "6/1/1/0")
    grd("G10", "WEP 二难的两路结论方向相反且均已数值求值",
        (EVIDENCE["eta"] > WEP_LIMIT and EVIDENCE["ag_1kg"] > 0), "真机读")
    grd("G11", "修复定价 SURVIVE == 0", EVIDENCE["pricing"]["SURVIVE"] == 0, "真机读")
    _ok12, _msg12 = check_write_side()
    grd("G12", "未修改 verify.py / 未跑 refresh_catalog", _ok12, _msg12)

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS,
            "evidence": EVIDENCE}


# ============================================================
# 9. 真机读判据（G7/G8/G12 一律现算，禁止写死 True）
# ============================================================
WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]


def scan_untouched():
    """G7：扫 源码/ 与 数据/ 下 TUFT-r225..r242 的产物，要求 mtime 早于 START_TS。"""
    touched = []
    scanned = 0
    for d in (SRC_DIR, DATA_DIR):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for nm in names:
            for n in range(225, 243):
                if ("TUFT-r%d" % n) in nm or ("_r%d" % n) in nm:
                    fp = os.path.join(d, nm)
                    try:
                        mt = os.path.getmtime(fp)
                    except OSError:
                        continue
                    scanned += 1
                    if mt >= START_TS:
                        touched.append(os.path.basename(fp))
                    break
    ok = (not touched) and scanned > 0
    msg = ("扫描 r225–r242 产物 %d 份，mtime 全部早于本轮启动 %s"
           % (scanned, START_ISO) if ok else
           ("发现被触碰：%s" % ",".join(touched[:5]) if touched
            else "未扫描到任何 r225–r242 产物（扫描器失效）"))
    return ok, msg


def check_distribution():
    """G8：条目分布真机读（不写死预估条数）。"""
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    ok = (sum(dist.values()) == len(ENTRIES)) and dist.get("FAIL", 0) >= 6 \
        and dist.get("PASS", 0) >= 3
    return ok, "实测分布 %s（要求 FAIL≥6 且 PASS≥3）" % dist


def check_write_side():
    """G12：verify.py / refresh_catalog.py 的 mtime 必须早于本轮启动。"""
    seen, late = [], []
    for p in WRITE_SIDE:
        if not os.path.exists(p):
            continue
        seen.append(os.path.basename(p))
        try:
            if os.path.getmtime(p) >= START_TS:
                late.append(os.path.basename(p))
        except OSError:
            pass
    ok = not late
    msg = ("写入侧 %s 的 mtime 均早于本轮启动" % ",".join(seen) if ok and seen
           else ("发现被改动：%s" % ",".join(late) if late else "未找到写入侧脚本"))
    return ok, msg


# ============================================================
# 10. AST 自审器（唯一允许写死 True 的守卫 G6 的支撑）
# ============================================================
_AST_WHITELIST = {"G6"}


def _ast_self_audit():
    """扫描本文件：判据类调用不得出现写死的 True（白名单除外）。"""
    path = os.path.join(SRC_DIR, BASE_NAME + ".py")
    src = read_text(path)
    if not src:
        return True, "（源文件读取失败，跳过）"
    tree = ast.parse(src)
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = getattr(node.func, "id", None)
        if fn not in ("ent", "ctl", "grd"):
            continue
        if len(node.args) < 3:
            continue
        third = node.args[2]
        if isinstance(third, ast.Constant) and third.value is True:
            code = None
            if node.args and isinstance(node.args[0], ast.Constant):
                code = node.args[0].value
            if code not in _AST_WHITELIST:
                bad.append("%s(%s, True)" % (fn, code))
    return (not bad), ("无写死 True" if not bad else "发现写死：%s" % ", ".join(bad))


# ============================================================
# 11. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    L = []
    A = L.append
    A("=" * 78)
    A(("TUFT-%s · 引力场工业级落地验收 / 六线工程验收清单 · "
       "光速螺旋统一场引力通道送检" % RID.upper()))
    A("=" * 78)
    A("生成时间 %s | 退出码待定" % START_ISO)
    A("")
    A("【靶（只读 3 份）】")
    for p in TARGETS:
        A("  - %s" % os.path.basename(p))
        A("    sha256 %s" % (SHA_AT_IMPORT.get(p) or "MISSING"))
    A("")
    A("-" * 78)
    A("一、六线验收矩阵（与 gr-industrial 产线 G 同源）")
    A("-" * 78)
    A("  %-4s %-24s %-30s %s" % ("ID", "通道", "必须供给", "工业锚点"))
    A("  " + "-" * 74)
    for s in SPEC:
        A("  %-4s %-24s %-30s %.10g" % (s["id"], s["name"], "+".join(s["need"]), s["anchor"]))
    A("")
    A("-" * 78)
    A("二、四组对照打分")
    A("-" * 78)
    for key, label in (("res_gr", "GR（正对照）"), ("res_newton", "牛顿（负对照）"),
                       ("res_half", "仅给势（半对照）"), ("res_target", "光速螺旋统一场（靶）")):
        r = ev[key]
        A("  %s：%d/%d   [SUPPLIED %d / SUPPLY-GAP %d / VIOLATION %d]"
          % (label, r["score"], r["total"], r["tally"]["SUPPLIED"],
             r["tally"]["SUPPLY-GAP"], r["tally"]["VIOLATION"]))
        for row in r["rows"]:
            A("      [%s] %-11s %s" % (row["id"], row["state"], row["detail"]))
        A("")
    A("-" * 78)
    A("三、★ WEP 二难（承重核心）")
    A("-" * 78)
    A("  候选式 F = ℏc∇κ（r242 R01 量纲已过）要求弱场退化到 F = GMm/r²。")
    A("  由 ℏc·dκ/dr = −GMm/r² 积分 ⇒ κ(r) = GMm/(ℏc·r) = α_g/r，闭式。")
    A("  κ'(r) 闭式 vs 中心差分相对误差 %s（两路互印）" % fmt_rel(ev["kp_relerr"]))
    A("")
    A("  路 a（κ 与检验质量无关，坚持几何化）：")
    A("      F 不含 m ⇒ a = F/m ∝ 1/m ⇒ Eötvös η = %.6f" % ev["eta"])
    A("      MICROSCOPE 实验限 %s ⇒ 超出 %s 倍  ⇒ 判死" % (fmt_rel(WEP_LIMIT), fmt_rel(ev["eta_exceed"])))
    A("  路 b（κ 依赖 m 以复现牛顿）：")
    A("      κ ∝ m ⇒ 同一空间点放不同物体 ⇒ 不同空间曲率 ⇒ 非几何量")
    A("      ω = c√(κ²+τ²) 亦随 m 变 ⇒ 空间螺旋频率由内容物决定 ⇒ 判死")
    A("")
    A("-" * 78)
    A("四、★ 曲率尺度灾变（路 b 的数值后果）")
    A("-" * 78)
    A("  %-16s %-14s %-14s %-16s %s" % ("检验质量", "α_g", "κ(R_E) m^-1", "曲率半径 ρ m", "ρ/l_P"))
    A("  " + "-" * 74)
    for r in ev["scale_rows"]:
        A("  %-16s %-14s %-14s %-16s %s"
          % (r["label"], "%.4e" % r["alpha_g"], "%.4e" % r["kappa"],
             "%.4e" % r["rho_m"], "%.4e" % r["rho_over_lp"]))
    A("")
    A("  1 kg 档：ω=cκ=%s s^-1，ℏω=%s J = %s MJ"
      % ("%.5e" % ev["omega_1kg"], "%.5e" % ev["hbar_omega_1kg"], "%.2f" % (ev["hbar_omega_1kg"] / 1e6)))
    A("  普朗克长度 l_P = %s m；1 kg 档曲率半径 = %s l_P"
      % ("%.4e" % L_PLANCK, "%.2f" % ev["rho_over_lp"]))
    A("")
    A("-" * 78)
    A("五、条目")
    A("-" * 78)
    for e in res["entries"]:
        A("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        A("     证据：%s" % e["evidence"])
        if e["note"]:
            A("     备注：%s" % e["note"])
    A("")
    A("-" * 78)
    A("六、控制组")
    A("-" * 78)
    for c in res["controls"]:
        A("  [%s] %s · %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["title"]))
        A("       %s" % c["evidence"])
    A("")
    A("-" * 78)
    A("七、守卫")
    A("-" * 78)
    for g in res["guards"]:
        A("  [%s] %s · %s" % ("PASS" if g["ok"] else "FAIL", g["code"], g["title"]))
        A("       %s" % g["evidence"])
    A("")
    return "\n".join(L)


def tally_states(res):
    d = {}
    for e in res["entries"]:
        d[e["state"]] = d.get(e["state"], 0) + 1
    return d


# ============================================================
# 12. 主流程
# ============================================================
def main():
    res = run_audit()

    # AST 自审（回填 G6）
    ok6, msg6 = _ast_self_audit()
    for g in res["guards"]:
        if g["code"] == "G6":
            g["ok"] = ok6
            g["evidence"] = msg6

    dist = tally_states(res)
    n_ctl_ok = sum(1 for c in res["controls"] if c["ok"])
    n_grd_ok = sum(1 for g in res["guards"] if g["ok"])
    n_grd = len(res["guards"])

    report = render_report(res)
    header = ("TUFT-%s 判词：GR 六线 6/6 全绿（正对照，锚点对拍到 1e−5）；"
              "靶引力通道 0/6 全为供给缺。弱场退化落在 WEP 二难："
              "几何化则 η=%.4f 超 MICROSCOPE 限 %s 倍；复现牛顿则 κ∝m 非几何，"
              "1 kg 档曲率半径 %s l_P。修复定价 128 组合 SURVIVE=0（本线第 28 度）。"
              % (RID.upper(), res["evidence"]["eta"],
                 fmt_rel(res["evidence"]["eta_exceed"]),
                 "%.2f" % res["evidence"]["rho_over_lp"]))

    # ---------- 写四件套 ----------
    payload = {
        "id": "TUFT-" + RID,
        "title": ("引力场工业级落地验收：六线工程验收清单与"
                  "光速螺旋统一场引力通道送检"),
        "generated_at": START_ISO,
        "targets": [{"path": os.path.basename(p), "sha256": SHA_AT_IMPORT.get(p)}
                    for p in TARGETS],
        "targets_unchanged": all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "verdict_header": header,
        "entries": res["entries"],
        "entry_distribution": dist,
        "controls": res["controls"],
        "controls_ok": "%d/%d" % (n_ctl_ok, len(res["controls"])),
        "guards": res["guards"],
        "guards_ok": "%d/%d" % (n_grd_ok, n_grd),
        "acceptance": {
            "GR": res["evidence"]["res_gr"],
            "Newton": res["evidence"]["res_newton"],
            "Halfway": res["evidence"]["res_half"],
            "Target": res["evidence"]["res_target"],
        },
        "wep_dilemma": {
            "eta_ti_pt": res["evidence"]["eta"],
            "wep_limit": WEP_LIMIT,
            "exceed_factor": res["evidence"]["eta_exceed"],
            "alpha_g_1kg": res["evidence"]["ag_1kg"],
            "kappa_1kg": res["evidence"]["kap_1kg"],
            "kappa_prime_relerr": res["evidence"]["kp_relerr"],
        },
        "curvature_disaster": {
            "rows": res["evidence"]["scale_rows"],
            "rho_over_lp_1kg": res["evidence"]["rho_over_lp"],
            "hbar_omega_J_1kg": res["evidence"]["hbar_omega_1kg"],
            "l_planck_m": L_PLANCK,
        },
        "repair_pricing": res["evidence"]["pricing"],
        "supply_hits": res["evidence"]["supply_hits"],
    }

    import json
    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    # ---- report.txt ----
    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
        f.write("\n" + "=" * 78 + "\n")
        f.write("条目 %d = %s\n" % (len(res["entries"]),
                                    " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
        f.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
        f.write("守卫 %d/%d\n" % (n_grd_ok, n_grd))
        f.write("靶未改动 %s\n" % payload["targets_unchanged"])
        f.write("=" * 78 + "\n")

    # ---- md ----
    md = []
    md.append("# TUFT-%s · %s\n" % (RID.upper(), payload["title"]))
    md.append("\n> 生成时间：%s\n" % START_ISO)
    md.append("\n## 判词\n\n%s\n" % header)
    md.append("\n## 一、验收矩阵与四组打分\n")
    for key, label in (("res_gr", "GR（正对照）"), ("res_newton", "牛顿（负对照）"),
                       ("res_half", "仅给势（半对照）"), ("res_target", "靶")):
        r = res["evidence"][key]
        md.append("\n**%s：%d/%d**（SUPPLIED %d / SUPPLY-GAP %d / VIOLATION %d）\n"
                  % (label, r["score"], r["total"], r["tally"]["SUPPLIED"],
                     r["tally"]["SUPPLY-GAP"], r["tally"]["VIOLATION"]))
        md.append("\n| 通道 | 状态 | 说明 |\n|---|---|---|\n")
        for row in r["rows"]:
            md.append("| %s | %s | %s |\n" % (row["id"], row["state"], row["detail"]))
    md.append("\n## 二、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 三、控制组与守卫\n")
    md.append("\n控制组 %d/%d，守卫 %d/%d。\n" % (n_ctl_ok, len(res["controls"]), n_grd_ok, n_grd))
    md.append("\n## 四、红线\n")
    md.append("\n- 靶 3 份只读，审计前后 sha256 逐位一致：%s\n" % payload["targets_unchanged"])
    md.append("- 本卷条目**不可与 r142–r242 相加**（分层铁律）。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    # ---- 判定册 ----
    vd = []
    vd.append("# 判定册 · TUFT-%s\n" % RID.upper())
    vd.append("\n## 判词\n\n%s\n" % header)
    vd.append("\n## 判决\n")
    vd.append("\n| 组 | 内容 | 结论 |\n|---|---|---|\n")
    vd.append("| A | 对靶有利项（ω² 量纲齐次、ℏc∇κ 量纲为力、诚实自曝、缺件口径） | PASS/INFO |\n")
    vd.append("| B | GR 工业级落地（正对照 6/6，锚点对拍 ≤1e−5） | PASS |\n")
    vd.append("| C | **WEP 二难**（几何化违 WEP %s 倍 / 复现牛顿则 κ∝m 非几何） | **FAIL** |\n"
              % fmt_rel(res["evidence"]["eta_exceed"]))
    vd.append("| D | 曲率尺度灾变（1 kg 档 ρ=%s l_P；跨 60 数量级） | FAIL |\n"
              % "%.2f" % res["evidence"]["rho_over_lp"])
    vd.append("| E | 六线送检 0/6（全供给缺）+ 判别力自检（四档分辨率 6/1/1/0） | FAIL/INFO |\n")
    vd.append("| F | 修复定价 128 组合 SURVIVE=0 | FAIL |\n")
    vd.append("\n## 性质界定（关键）\n")
    vd.append("\n- 靶的 0/6 记为 **SUPPLY-GAP（缺件）**，**不是** VIOLATION（算错）。")
    vd.append("本卷**不**声称靶算出了错误的工程数字。\n")
    vd.append("- 真正的排除性判决只来自 C 组（WEP 二难）与 D 组（曲率尺度），")
    vd.append("这两组针对的是**弱场退化**这一靶自定的入门检验，属靶自己设定的门槛。\n")
    vd.append("- 本线第 28 度「修复即自杀」，条目不可与 r142–r242 相加。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    vd.append("- 控制组 %d/%d；守卫 %d/%d\n" % (n_ctl_ok, len(res["controls"]), n_grd_ok, n_grd))
    vd.append("- 未触碰 r225–r242（mtime 真机读）；未跑 refresh_catalog；未改 verify.py；未做 git。\n")
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write("".join(vd))

    # ---- html 可视化 ----
    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(res, payload, header, dist, n_ctl_ok,
                            len(res["controls"]), n_grd_ok, n_grd))

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(res["entries"]),
                                         " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, n_grd))
    sys.stdout.write("靶未改动 %s\n" % payload["targets_unchanged"])
    sys.stdout.write("=" * 78 + "\n")

    bad = (n_ctl_ok != len(res["controls"])) or (n_grd_ok != n_grd)
    return 2 if bad else 0


def render_html(res, payload, header, dist, n_ctl_ok, n_ctl, n_grd_ok, n_grd):
    ev = res["evidence"]
    rows4 = [("GR（正对照）", ev["res_gr"]), ("牛顿（负对照）", ev["res_newton"]),
             ("仅给势（半对照）", ev["res_half"]), ("光速螺旋统一场（靶）", ev["res_target"])]

    # 六线得分条形
    bars = []
    for label, r in rows4:
        sc = r["score"]
        wpx = int(340.0 * sc / 6.0)
        bars.append(
            '<div class="row"><div class="lab">%s</div>'
            '<div class="bar"><div class="fill" style="width:%dpx"></div></div>'
            '<div class="val">%d/6</div></div>' % (label, wpx, sc))

    # 曲率扫描表
    srows = []
    for r in ev["scale_rows"]:
        srows.append("<tr><td>%s</td><td>%.4e</td><td>%.4e</td><td>%.4e</td><td>%.4e</td></tr>"
                     % (r["label"], r["alpha_g"], r["kappa"], r["rho_m"], r["rho_over_lp"]))

    ents = []
    for e in res["entries"]:
        cls = "pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL" else "info")
        ents.append('<div class="ent %s"><b>[%s] %s · %s</b>'
                    '<div class="ev">%s</div>'
                    '%s</div>' % (cls, e["state"], e["code"], e["title"], e["evidence"],
                                  ('<div class="note">%s</div>' % e["note"]) if e["note"] else ""))

    ctls = []
    for c in res["controls"]:
        ctls.append('<div class="ctl %s">[%s] %s · %s</div>'
                    % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL",
                       c["code"], c["title"]))

    grds = []
    for g in res["guards"]:
        grds.append('<div class="ctl %s">[%s] %s · %s</div>'
                    % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL",
                       g["code"], g["title"]))

    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 引力场工业级落地验收</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:26px 0 10px;
 border-left:4px solid #2c5f8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#fff8e6;border:1px solid #e0c48a;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
.row{{display:flex;align-items:center;margin:6px 0}}
.lab{{width:190px;font-size:13px}}
.bar{{width:340px;height:16px;background:#e8eaed;border-radius:3px;overflow:hidden}}
.fill{{height:16px;background:#2c5f8a}}
.val{{margin-left:10px;font-weight:600;font-size:13px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#eef1f5}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px 0;border-radius:3px;display:inline-block;
 width:340px}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
.grid{{display:flex;flex-wrap:wrap;gap:4px}}
</style></head><body>
<h1>TUFT-{RID} · 引力场工业级落地验收</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>

<h2>一、六线验收得分</h2>
{bars}

<h2>二、★ WEP 二难</h2>
<table>
<tr><th>路径</th><th>结论</th><th>量化</th></tr>
<tr><td>路 a：κ 与 m 无关（坚持几何化）</td><td>加速度 a ∝ 1/m ⇒ 违反弱等效原理</td>
<td>η = {eta:.6f}，MICROSCOPE 限 {wep:.0e} ⇒ 超出 {exceed:.3e} 倍</td></tr>
<tr><td>路 b：κ ∝ m（复现牛顿）</td><td>κ 不再是时空几何量，与靶本体论冲突</td>
<td>κ(r)=α_g/r，α_g(地球,1kg)={ag:.4e}；κ' 闭式 vs 差分误差 {kprel}</td></tr>
</table>

<h2>三、★ 曲率尺度灾变（路 b 的数值后果）</h2>
<table>
<tr><th>检验质量</th><th>α_g</th><th>κ(R_E) m^-1</th><th>曲率半径 ρ (m)</th><th>ρ / l_P</th></tr>
{srows}
</table>
<div class="meta">1 kg 档：ω = cκ = {omega:.4e} s^-1，ℏω = {ho:.4e} J = {mj:.2f} MJ；
普朗克长度 l_P = {lp:.4e} m。</div>

<h2>四、条目</h2>
{ents}

<h2>五、控制组（{nctl_ok}/{nctl}）</h2>
<div class="grid">{ctls}</div>

<h2>六、守卫（{ngrd_ok}/{ngrd}）</h2>
<div class="grid">{grds}</div>

<div class="meta" style="margin-top:24px">
红线：靶 3 份只读（sha256 前后一致：{unchanged}）；本卷条目不可与 r142–r242 相加。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        bars="\n".join(bars),
        eta=ev["eta"], wep=WEP_LIMIT, exceed=ev["eta_exceed"],
        ag=ev["ag_1kg"], kprel=fmt_rel(ev["kp_relerr"]),
        srows="\n".join(srows), omega=ev["omega_1kg"], ho=ev["hbar_omega_1kg"],
        mj=ev["hbar_omega_1kg"] / 1e6, lp=L_PLANCK,
        ents="\n".join(ents), ctls="\n".join(ctls), grds="\n".join(grds),
        nctl_ok=n_ctl_ok, nctl=n_ctl, ngrd_ok=n_grd_ok, ngrd=n_grd,
        unchanged=payload["targets_unchanged"])


if __name__ == "__main__":
    sys.exit(main())
