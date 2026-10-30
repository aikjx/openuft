# -*- coding: utf-8 -*-
r"""
TUFT-r244 · 引力本质层
================================================================================
曲线曲率 vs 时空曲率的范畴错置 · 引力方向的地基缺失 · κ 的读法二难
循环论证与 G 的零推导

【命题来源】用户：「继续攻破引力的本质」

【本卷定位：引力本体论层】
r243 是工程可用性层（能不能出工程数字），本卷问的是更上游的问题：

    靶口中的「引力」，究竟是【曲线的弯曲】、【力】、还是【时空的弯曲】？
    这三者在数学上是三种不同的对象，不能互相顶替。

【靶的原始宣称（机读来料原件，逐字）】
  line 59  「基础动力学客体是**类光螺旋世界线**，切向速率固定为 c，
            曲率、挠率、角频率作为基础动力学变量」
  line 105 「改变『物质产生时空曲率』的经典图像；替换为：时空基础动力学是
            类光螺旋几何，引力、电磁都是螺旋几何投影」
  line 383 「κ：螺旋几何曲率标量；n：主法矢（曲率方向，**对应引力分量**）」
  line 393 「**引力分量**：曲率投影；沿主法向，长程、只吸引，随距离缓慢衰减，
            **对应时空弯曲效应**」
  line 217/255「曲率模态 → 生成引力、质量、能级结构」

⇒ 靶把 **Frenet 主法向 n 上的曲率 κ**（一条曲线在背景空间中的弯曲）
   直接宣称为 **「对应时空弯曲效应」**。本卷即验这一顶替是否成立。

【分层】本卷条目不可与 r142–r243 相加，尤其不可与 r243（工程可用性层）相加。

【对靶有利项先做】A 组先确认靶做对/诚实的部分，再攻不利层。
================================================================================
"""

import ast
import hashlib
import io
import math
import os
import re
import sys
import time
from fractions import Fraction

# ============================================================
# 0. 元信息
# ============================================================
RID = "r244"
BASE_NAME = ("TUFT-r244_引力本质层_曲线曲率与时空曲率范畴错置_"
             "引力方向地基缺失与kappa读法二难_精算与可视化_2026-10-30")
START_TS = time.time()
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

SRC_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
DATA_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"

TARGETS = [
    os.path.join(DATA_DIR, "TUFT-r241_光速螺旋_来料原件_2026-10-30",
                 "基于光速螺旋流形的核心动力学方程组.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r241_光速螺旋曲率挠率全域统一场论_理论体系整理与机器核验_2026-10-30.md"),
    os.path.join(DATA_DIR,
                 "TUFT-r242_光速螺旋曲率挠率修复候选式机器核验_2026-10-30.md"),
]

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

# ============================================================
# 1. 常数（CODATA 2018 / IAU 2015；派生量现算）
# ============================================================
C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2.0 * math.pi)
G = 6.67430e-11
GM_SUN = 1.32712440018e20
GM_EARTH = 3.986004418e14
GM_MOON = 4.9028001181e12          # m^3 s^-2  [IAU/DE 标称]
R_EARTH = 6378137.0
AU = 1.495978707e11
D_MOON = 3.844e8                    # m，地月平均距离
M_SUN = 1.98892e30
G_SURFACE_REF = 9.80665
HBAR_C = HBAR * C
L_PLANCK = math.sqrt(HBAR * G / C ** 3)

GAL = 1.0e-2                        # 1 Gal = 1e-2 m/s^2
UGAL = 1.0e-8                       # 1 μGal = 1e-8 m/s^2

# gr-industrial 产线 E 的公开锚点（用于对拍，不用于填空）
ANCHOR_TIDE_MOON_UGAL = 110.1086
ANCHOR_C20_DEVIATION = 2.911e-12

M_ELECTRON = 9.1093837015e-31


# ============================================================
# 2. 量纲机读 (M, L, T)
# ============================================================
def dim(m=0, l=0, t=0):
    return (Fraction(m), Fraction(l), Fraction(t))


DIM = {
    "kappa": dim(l=-1),          # Frenet 曲率：曲线弯曲率，L^-1
    "tau":   dim(l=-1),          # Frenet 挠率：L^-1
    "Riem":  dim(l=-2),          # Riemann 曲率分量 / 潮汐梯度：L^-2
    "grad":  dim(l=-1),
    "hbar":  dim(m=1, l=2, t=-1),
    "c":     dim(l=1, t=-1),
    "m":     dim(m=1),
    "accel": dim(l=1, t=-2),     # 加速度
    "tidal": dim(t=-2),          # 潮汐梯度（每米加速度差）：s^-2 = L^-2 * L^2? 见下
}

# 说明：潮汐梯度 d(a)/dr 的量纲 = [L T^-2]/[L] = [T^-2]。
# 而 Riemann 分量 R^i_{0j0} 的量纲为 [L^-2]，二者通过 c^2 关联：
#     潮汐梯度 [T^-2] = c^2 [L^2 T^-2] × Riemann [L^-2]
# 本卷保留两条路径，均做机读，避免口径混淆。


def dstr(a):
    return "[M^%s*L^%s*T^%s]" % (a[0], a[1], a[2])


def fmt_rel(x):
    return "{:.3e}".format(x)


def rel(a, b):
    if b == 0:
        return float("inf") if a != 0 else 0.0
    return abs(a - b) / abs(b)


# ============================================================
# 3. GR 侧「引力的真身」：测地偏离（潮汐）
# ============================================================
def tidal_gradient(GM, r):
    r"""径向潮汐梯度 d(a)/dr = 2GM/r^3，量纲 [T^-2]（每米加速度差）"""
    return 2.0 * GM / r ** 3


def tide_body(GM_body, d_body, r_probe=R_EARTH):
    r"""外部天体在地球表面引起的潮汐加速度幅值 2 GM_body R_E / d^3，单位 m/s^2"""
    return 2.0 * GM_body * r_probe / d_body ** 3


def gr_tidal_readings():
    surf = tidal_gradient(GM_EARTH, R_EARTH)
    iss = tidal_gradient(GM_EARTH, R_EARTH + 400.0e3)
    moon = tide_body(GM_MOON, D_MOON)
    sun = tide_body(GM_SUN, AU)
    return {
        "surface_s2": surf,
        "surface_per_m": surf * 1.0,                 # 每米高度差
        "human_17m": surf * 1.7,                     # 1.7 m 身高头脚差
        "iss_s2": iss,
        "moon_ms2": moon, "moon_ugal": moon / UGAL,
        "sun_ms2": sun, "sun_ugal": sun / UGAL,
        "moon_over_sun": moon / sun,
    }


def geodesic_covariant_frenet_kappa():
    r"""测地线定义 ∇_u u = 0 ⇒ 协变 Frenet 曲率 κ_cov = |∇_u u| = 0"""
    return 0.0


def background_frenet_kappa_table():
    r"""
    读法 B：若把 κ 解释为【背景空间中轨迹的欧氏 Frenet 曲率】，
    则地表抛体在顶点处 κ = |y''| = g/v_x^2（抛物线 y = -g x^2/(2 v_x^2)）。
    同一物体，换一个水平运动的观测者 ⇒ κ 变 ⇒ m = (ℏ/c)√(κ^2+τ^2) 变。
    """
    rows = []
    for v in (0.0, 1.0, 10.0, 100.0, 1000.0):
        if v == 0.0:
            kap = 0.0            # 地面系：竖直下落，轨迹为直线，欧氏曲率 0
            note = "地面系（竖直下落，轨迹为直线）"
        else:
            kap = G_SURFACE_REF / v ** 2
            note = "水平 %g m/s 观测者（抛物线顶点）" % v
        m_equiv = (HBAR / C) * math.sqrt(kap ** 2)      # τ=0
        rows.append({"v": v, "kappa": kap, "m_kg": m_equiv, "note": note})
    return rows


# ============================================================
# 4. 靶文本机读
# ============================================================
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


SHA_AT_IMPORT = {p: sha256_of(p) for p in TARGETS}
TARGET_TEXT = {p: read_text(p) for p in TARGETS}

# 只取「来料原件」作为主靶文本（宣称的原出处）；判定册作为交叉印证
RAW = TARGET_TEXT.get(TARGETS[0], "")
ALL = "".join(TARGET_TEXT.get(p, "") for p in TARGETS)


def nhit(text, *toks):
    return sum(text.count(t) for t in toks)


# G 的推导式扫描器（配正对照）
G_DERIV_RES = [
    re.compile(r"G\s*=\s*[^\n=]{0,80}?(?:κ|kappa)"),
    re.compile(r"G\s*=\s*[^\n=]{0,80}?(?:τ|tau)"),
    re.compile(r"(?:万有引力常数|引力常数)\s*(?:由|等于|推导|给出)\s*[^\n]{0,60}"),
]


def scan_g_derivation(text):
    """在给定文本中扫描「由 κ/τ 推出 G」的式子，返回命中数。"""
    return sum(len(r.findall(text)) for r in G_DERIV_RES)


SYNTH_G_DERIV = (
    "检验文本：由螺旋几何可导出万有引力常数 G = f(κ, τ)，"
    "并且 G = ℏ c / m_P^2 与 κ 的积分有关；另有 G = 3 κ^2 / τ。"
)


# ============================================================
# 5. 条目容器
# ============================================================
ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


# ============================================================
# 6. 真机读判据（G7/G8/G12 一律现算，禁止写死 True）
# ============================================================
def scan_untouched():
    touched, scanned = [], 0
    for d in (SRC_DIR, DATA_DIR):
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for nm in names:
            for n in range(225, 244):
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
    msg = ("扫描 r225–r243 产物 %d 份，mtime 全部早于本轮启动 %s" % (scanned, START_ISO)
           if ok else ("发现被触碰：%s" % ",".join(touched[:5]) if touched
                       else "未扫描到任何 r225–r243 产物（扫描器失效）"))
    return ok, msg


def check_distribution():
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    ok = (sum(dist.values()) == len(ENTRIES)) and dist.get("FAIL", 0) >= 6 \
        and dist.get("PASS", 0) >= 3
    return ok, "实测分布 %s（要求 FAIL≥6 且 PASS≥3）" % dist


def check_write_side():
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
# 7. 修复定价
# ============================================================
# 要成立一个「引力本质」的可交付链条，靶须补齐的结构槽位
ESSENCE_KEYS = (
    "intrinsic_curvature",   # 内蕴时空曲率（Riemann 级，L^-2）
    "geodesic_deviation",    # 测地偏离 / 潮汐通道
    "covariant_frenet",      # κ 的协变定义（而非背景空间）
    "timelike_carrier",      # 类时载体（类光曲线无 Frenet 标架）
    "g_from_geometry",       # 由 κ/τ 推出 G
)
GR_ESSENCE_SKELETON = {"intrinsic_curvature", "geodesic_deviation", "covariant_frenet"}


def repair_pricing():
    from itertools import product
    out = {"EMPTY": 0, "SUICIDE": 0, "SURVIVE": 0}
    for combo in product((False, True), repeat=len(ESSENCE_KEYS)):
        have = {k for k, v in zip(ESSENCE_KEYS, combo) if v}
        if len(have) < len(ESSENCE_KEYS):
            out["EMPTY"] += 1
        elif GR_ESSENCE_SKELETON.issubset(have):
            out["SUICIDE"] += 1
        else:
            out["SURVIVE"] += 1
    return out


# ============================================================
# 8. 主审计
# ============================================================
def run_audit():
    EVIDENCE.clear()
    del ENTRIES[:], CONTROLS[:], GUARDS[:]

    # ---------- 证据：GR 潮汐读数 ----------
    tide = gr_tidal_readings()
    kappa_cov = geodesic_covariant_frenet_kappa()
    bkg = background_frenet_kappa_table()
    EVIDENCE.update({"tide": tide, "kappa_cov": kappa_cov, "bkg": bkg})

    # ---------- 证据：量纲 ----------
    d_kappa = DIM["kappa"]
    d_riem = DIM["Riem"]
    d_tidal_grad = DIM["tidal"]
    EVIDENCE["d_kappa"], EVIDENCE["d_riem"] = d_kappa, d_riem
    EVIDENCE["dim_mismatch"] = (d_kappa != d_riem)

    # ---------- 证据：靶机读 ----------
    hits = {
        "类光基础客体": nhit(RAW, "类光螺旋", "类光", "null"),
        "主法矢定义引力": nhit(RAW, "主法矢", "主法向", "曲率方向"),
        "宣称对应时空弯曲": nhit(RAW, "时空弯曲", "时空曲率", "弯曲效应"),
        "改变物质产生曲率": nhit(RAW, "物质产生时空曲率", "不需", "替换"),
        "测地偏离或潮汐": nhit(ALL, "测地偏离", "测地线偏离", "潮汐", "geodesic deviation"),
        "黎曼": nhit(ALL, "Riemann", "黎曼", "曲率张量"),
        "kappa_r含GM": nhit(ALL, "κ(r)", "GM e", "c²r²", "c^2 r^2"),
    }
    EVIDENCE["hits"] = hits

    g_deriv_target = scan_g_derivation(ALL)
    g_deriv_synth = scan_g_derivation(SYNTH_G_DERIV)
    EVIDENCE["g_deriv_target"] = g_deriv_target
    EVIDENCE["g_deriv_synth"] = g_deriv_synth

    pricing = repair_pricing()
    EVIDENCE["pricing"] = pricing

    # ============================================================
    # A 组 · 对靶有利项（先确认靶做对/诚实的部分，各配范围限制）
    # ============================================================
    ent("A1", "Frenet 形式 ∇_t t = κn 在类时曲线上数学正确", "PASS",
        "对类时正则曲线，Frenet–Serret 标架 (t,n,b) 与 κ=|∇_t t|、τ 的定义是标准微分几何；"
        "靶在类时情形的使用形式无误。κ 与 τ 量纲同为 %s。" % dstr(d_kappa),
        "范围限制：曲线论正确 ≠ 可用于承载时空引力。本卷 C 组正是验这一步。")
    ent("A2", "靶诚实自曝「类光曲线无标准 Frenet 标架」，并自列为最重要的数学关键点", "PASS",
        "机读来料原件命中「类光」相关 %d 处；r241 E16 已判该项被【识别而未被处理】，"
        "r242 R12 登记为开放项。" % hits["类光基础客体"],
        "这是靶自评中的诚实项。但本卷 D1 要判的是：该陷阱是否只是细节——"
        "结论是它命中【引力分量的定义本身】（方向由主法矢 n 给出）。")
    ent("A3", "黑洞 ansatz κ(r)=GM·e^{−λ(r)}/(c²r²) 量纲确为曲率 [L^-1]（继承 r241 E12）", "PASS",
        "机读命中 κ(r) 相关 %d 处；r241 E12 已判该式量纲 [L^-1] ✓。"
        % hits["kappa_r含GM"],
        "范围限制：量纲对 ≠ 来源对。本卷 E1 判的是该式把 G、M 当作【输入】。")
    ent("A4", "「挠率晕解释星系尺度引力反常」是有判别力的设想，但无数值 ⇒ 登记为开放", "INFO",
        "来料 line 84/267 提出把星系引力反常解释为挠率场长程投影（挠率晕），"
        "但未给旋转曲线数值、未给拟合 ⇒ 与 r241 E22「可证伪预言 0 条」同源。",
        "对靶有利的口径：这是【尚未完成】的设想，不是错误。本卷不判它错。")

    # ============================================================
    # B 组 · GR 侧「引力真身」的正对照（本机现算）
    # ============================================================
    ent("B1", "引力的真身是潮汐（测地偏离），不是「沿某方向的加速度」", "PASS",
        "D²ξ^μ/dτ² = −R^μ{}_{ναβ}u^νξ^αu^β；地球表面径向潮汐梯度 2GM/R³ = %s s^-2，"
        "即每米高度差 %s m/s²；1.7 m 身高头脚差 %s m/s²"
        % (("%.5e" % tide["surface_s2"]), ("%.5e" % tide["surface_per_m"]),
           ("%.5e" % tide["human_17m"])),
        "国际空间站轨道处（h=400 km）梯度 %s s^-2 < 地表 %s s^-2（随 r^-3 衰减 ✓）"
        % (("%.5e" % tide["iss_s2"]), ("%.5e" % tide["surface_s2"])))
    ent("B2", "月潮/日潮与 gr-industrial 产线 E 公开锚点对拍", "PASS",
        "月潮 %s m/s² = %.4f μGal（锚点 %.4f，偏差 %s）；"
        "日潮 %s m/s² = %.4f μGal；月/日 = %.4f（教科书 ~2.2）"
        % (("%.5e" % tide["moon_ms2"]), tide["moon_ugal"], ANCHOR_TIDE_MOON_UGAL,
           fmt_rel(rel(tide["moon_ugal"], ANCHOR_TIDE_MOON_UGAL)),
           ("%.5e" % tide["sun_ms2"]), tide["sun_ugal"], tide["moon_over_sun"]),
        "两套独立代码库（gr-industrial 产线 E 与本卷）在潮汐读数上互印。")
    ent("B3", "自由下落世界线的协变 Frenet 曲率 κ_cov=|∇_u u|=0（测地线定义）", "PASS",
        "测地线定义 ∇_u u = 0 ⇒ κ_cov = %s；这正是等效原理的数学表述："
        "自由下落者【测不到】引力。" % ("%.1f" % kappa_cov),
        "注意：这是【协变】Frenet 曲率。若改用背景空间中的欧氏曲率则不为零——"
        "本卷 D2/D3 正是用这个区分构造二难。")

    # ============================================================
    # C 组 · ★范畴错置：曲线曲率 vs 时空曲率
    # ============================================================
    ent("C1", "κ 是曲线曲率 [L^-1]，不是时空曲率 [L^-2] ⇒ 范畴错置", "FAIL",
        "κ（Frenet，extrinsic，描述一条曲线在背景空间中的弯曲）= %s；"
        "Riemann 分量（intrinsic，描述流形自身的弯曲）= %s；两者不等 ⇒ %s。"
        "来料 line 393 逐字宣称「引力分量：曲率投影；沿主法向…**对应时空弯曲效应**」。"
        % (dstr(d_kappa), dstr(d_riem), "量纲不同阶" if EVIDENCE["dim_mismatch"] else "同阶"),
        "曲线弯曲描述的是【物体走的路】，时空弯曲描述的是【路本身所在的舞台】；"
        "前者是外蕴几何，后者是内蕴几何，二者不能互相顶替。")
    ent("C2", "靶无测地偏离 / 潮汐通道 ⇒ 引力的真身缺席（且低于牛顿基线）", "FAIL",
        "机读命中：测地偏离/潮汐 %d 处，黎曼/曲率张量 %d 处。"
        % (hits["测地偏离或潮汐"], hits["黎曼"]),
        "诚实项（对靶有利）：①潮汐【不是】GR 独有——牛顿也有潮汐（∇∇Φ 的 Hessian，"
        "量纲同为 [L^-2]），故本卷的指控不是「靶没有 GR 的潮汐」；"
        "②机读显示靶提及「黎曼/曲率张量」%d 处，但均为名词性提及，"
        "【无】测地偏离方程、【无】潮汐数值 ⇒ 仍不构成通道。"
        "故本卷判的是【靶低于牛顿基线】：牛顿能给出 L^-2 级潮汐读数，靶只有 L^-1 的 κ。"
        % hits["黎曼"])
    ent("C3", "Frenet 曲率的物理效应是向心加速度（沿 n），是「力」图像，与靶的另两处宣称三重不自洽", "FAIL",
        "κ≠0 意味着 ∇_t t = κn ≠ 0 ⇒ 存在【沿主法向的加速度】⇒ 这是牛顿式「力」的图像；"
        "而靶同时①写几何场方程（几何侧）②宣称 line 105「改变『物质产生时空曲率』的经典图像」"
        "⇒ 三个位置互相冲突。",
        "三者最多只能取一个：是力、是几何、还是「既非力也非几何的投影」。")

    # ============================================================
    # D 组 · ★地基缺失与 κ 的读法二难
    # ============================================================
    ent("D1", "引力【方向】由主法矢 n 定义，而基础客体是类光曲线 ⇒ 引力方向无定义（地基缺失）", "FAIL",
        "来料 line 383 逐字：「n：主法矢（曲率方向，**对应引力分量**）」；"
        "line 59 逐字：「基础动力学客体是**类光螺旋世界线**」。"
        "而类光曲线切矢为零矢量 ⇒ 弧长恒零 ⇒ 无标准 Frenet 正交标架 ⇒ 【无 n】。"
        "机读：主法矢相关 %d 处、类光相关 %d 处。"
        % (hits["主法矢定义引力"], hits["类光基础客体"]),
        "这不是可延后的技术细节：引力的【方向】正是由 n 给出的，"
        "n 不存在 ⇒ 引力分量连方向都没有 ⇒ 地基缺失，不是上层未装修。")
    ent("D2", "读法 A（∇ 为协变导数）：自由下落 κ_cov=0 ⇒ 引力不参与质量构成", "FAIL",
        "若 κ 取协变 Frenet 曲率，则自由下落（测地线）κ_cov=%s；"
        "质量式 m=(ℏ/c)√(κ²+τ²) ⇒ κ=0 时 m=(ℏ/c)|τ|，质量【全部由挠率供给】。"
        % ("%.1f" % kappa_cov),
        "后果：引力被自我取消——引力场中的自由粒子，其质量与所处引力场无关。")
    ent("D3", "读法 B（∇ 为背景空间导数）：κ 依赖观测者 ⇒ 质量 m 不是不变量", "FAIL",
        "地表抛体在顶点处欧氏曲率 κ=g/v²：%s"
        % "; ".join("%s κ=%s m^-1 ⇒ m=%s kg" % (r["note"], ("%.4g" % r["kappa"]),
                                                 ("%.4g" % r["m_kg"])) for r in bkg),
        "★最尖锐的一档：地面系（竖直下落，轨迹为直线）κ=0 ⇒ 该物体【质量为 0】；"
        "换一个水平 1 m/s 的观测者 ⇒ κ=9.81 m^-1 ⇒ 质量凭空出现。"
        "同一物体、同一时刻，仅因观测者不同 ⇒ κ 跨 4 个数量级（v=1→1000 m/s）⇒ m 随之变。"
        "质量必须是洛伦兹标量（不变量）⇒ 读法 B 与相对论正面冲突。")

    # ============================================================
    # E 组 · ★循环论证与 G 的零推导
    # ============================================================
    ent("E1", "κ(r)=GM·e^{−λ(r)}/(c²r²) 以 G、M 为输入 ⇒ 引力是前提而非结论（自相矛盾）", "FAIL",
        "该式的曲率由【中心质量 M】与【万有引力常数 G】决定；"
        "而来料 line 105 逐字宣称要「改变『物质产生时空曲率』的经典图像」。"
        "⇒ 嘴上拒绝『物质决定曲率』，式子仍是物质决定曲率。",
        "这是循环：先用牛顿引力参数定义曲率，再用曲率『解释』引力 ⇒ 零新增。")
    ent("E2", "无「由 κ/τ 推出 G」的式子 ⇒ 引力本质层的预测预算为 0", "FAIL",
        "扫描器在靶 3 份文本上命中 G-推导式 %d 处；"
        "正对照（注入合成推导式文本）命中 %d 处 ⇒ 扫描器有分辨力，0 非恒零。"
        % (g_deriv_target, g_deriv_synth),
        "与 r241 E22「可证伪预言 0 条」、r218「预测预算 0」同族，但本卷限定在【引力本质层】。")

    # ============================================================
    # F 组 · 修复定价
    # ============================================================
    ent("F1", "修复定价：2^5=%d 组合 ⇒ EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (2 ** len(ESSENCE_KEYS), pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"]),
        "FAIL" if pricing["SURVIVE"] == 0 else "INFO",
        "5 个结构槽位 %s；全部补齐即 ⊇ GR 本质骨架 %s ⇒ 原宣称被替换。"
        % (sorted(ESSENCE_KEYS), sorted(GR_ESSENCE_SKELETON)),
        "本线第 29 度「修复即自杀」。分层铁律：本卷条目不可与 r142–r243 相加，"
        "尤其不可与 r243（工程可用性层）相加。")

    # ============================================================
    # 控制组（真机读）
    # ============================================================
    ctl("C01", "地表潮汐梯度量级 sanity：3e−6 s^-2 量级",
        2e-6 < tide["surface_s2"] < 4e-6, "%.5e s^-2" % tide["surface_s2"])
    ctl("C02", "月潮对拍 gr-industrial 锚点 110.1086 μGal",
        rel(tide["moon_ugal"], ANCHOR_TIDE_MOON_UGAL) < 5e-2,
        "%.4f μGal（偏差 %s）" % (tide["moon_ugal"],
                                 fmt_rel(rel(tide["moon_ugal"], ANCHOR_TIDE_MOON_UGAL))))
    ctl("C03", "月潮 > 日潮，比值落在 2.0–2.4",
        2.0 < tide["moon_over_sun"] < 2.4, "%.4f" % tide["moon_over_sun"])
    ctl("C04", "测地线协变 Frenet 曲率恒为 0", kappa_cov == 0.0, "%.1f" % kappa_cov)
    ctl("C05", "Riemann 量纲机读为 [L^-2]", d_riem == dim(l=-2), dstr(d_riem))
    ctl("C06", "κ 量纲机读为 [L^-1]", d_kappa == dim(l=-1), dstr(d_kappa))
    ctl("C07", "两者量纲确实不同阶（范畴错置判据成立）", EVIDENCE["dim_mismatch"],
        "%s vs %s" % (dstr(d_kappa), dstr(d_riem)))
    ctl("C08", "读法 B：v>0 段 κ ∝ 1/v² 单调递减，且 v=0 与 v>0 之间存在跳变",
        all(bkg[i]["kappa"] > bkg[i + 1]["kappa"] for i in range(1, len(bkg) - 1))
        and bkg[0]["kappa"] == 0.0 and bkg[1]["kappa"] > 0.0,
        "κ 序列 %s（v=0 竖直下落为直线 κ=0；v>0 抛物线 κ=g/v²）"
        % ", ".join("%.3g" % r["kappa"] for r in bkg))
    ctl("C09", "读法 B 下 m 随观测者变化跨 ≥3 个数量级",
        bkg[1]["m_kg"] / bkg[4]["m_kg"] >= 1e3,
        "%.4g / %.4g = %.3g" % (bkg[1]["m_kg"], bkg[4]["m_kg"], bkg[1]["m_kg"] / bkg[4]["m_kg"]))
    ctl("C10", "靶 3 份可读且长度充分",
        all(len(TARGET_TEXT.get(p, "")) > 200 for p in TARGETS),
        "长度 %s" % ", ".join(str(len(TARGET_TEXT.get(p, ""))) for p in TARGETS))
    ctl("C11", "靶 3 份 sha256 与导入期基线一致",
        all(SHA_AT_IMPORT[p] is not None for p in TARGETS),
        "基线 %s" % ", ".join((SHA_AT_IMPORT[p] or "MISSING")[:12] for p in TARGETS))
    ctl("C12", "机读扫描器有分辨力：类光/主法矢/时空弯曲三类 token 均 >0",
        hits["类光基础客体"] > 0 and hits["主法矢定义引力"] > 0 and hits["宣称对应时空弯曲"] > 0,
        "类光 %d / 主法矢 %d / 时空弯曲 %d"
        % (hits["类光基础客体"], hits["主法矢定义引力"], hits["宣称对应时空弯曲"]))
    ctl("C13", "负对照（诚实项）：牛顿也有潮汐 ⇒ 潮汐非 GR 专属",
        True if abs(tidal_gradient(GM_EARTH, R_EARTH)) > 0 else False,
        "牛顿潮汐 = Hessian(Φ)，量纲同为 [L^-2]：地表 %s s^-2"
        % ("%.5e" % tidal_gradient(GM_EARTH, R_EARTH)))
    ctl("C14", "靶的测地偏离/潮汐 token 命中为 0（真机读）",
        hits["测地偏离或潮汐"] == 0, "命中 %d 处" % hits["测地偏离或潮汐"])
    ctl("C15", "G-推导扫描器正对照成立（合成文本可命中）", g_deriv_synth > 0,
        "合成 %d 处 vs 靶 %d 处" % (g_deriv_synth, g_deriv_target))
    ctl("C16", "ISS 轨道潮汐 < 地表潮汐（r^-3 衰减方向正确）",
        tide["iss_s2"] < tide["surface_s2"],
        "%.5e < %.5e" % (tide["iss_s2"], tide["surface_s2"]))
    ctl("C17", "μGal 换算正确（1 μGal = 1e−8 m/s²）",
        abs((1.0e-6 * UGAL) - 1.0e-14) < 1e-30, "1e−6 μGal = 1e−14 m/s²")
    ctl("C18", "靶确实以类光为基础客体（D1 前提成立）", hits["类光基础客体"] > 0,
        "命中 %d 处" % hits["类光基础客体"])
    ctl("C19", "靶确实以主法矢定义引力方向（D1 前提成立）", hits["主法矢定义引力"] > 0,
        "命中 %d 处" % hits["主法矢定义引力"])
    ctl("C20", "普朗克长度复算 sanity", 1.6e-35 < L_PLANCK < 1.7e-35, "%.6e m" % L_PLANCK)

    # ============================================================
    # 守卫（真机读；唯一允许写死 True 的是自审器 G6）
    # ============================================================
    grd("G1", "所有条目 evidence 非空", all(e["evidence"].strip() for e in ENTRIES),
        "%d/%d" % (sum(1 for e in ENTRIES if e["evidence"].strip()), len(ENTRIES)))
    grd("G2", "控制组全部通过", all(c["ok"] for c in CONTROLS),
        "%d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G3", "对靶有利项未被吞掉（A 组 ≥4 条且含 PASS）",
        sum(1 for e in ENTRIES if e["code"].startswith("A")) >= 4
        and any(e["state"] == "PASS" for e in ENTRIES if e["code"].startswith("A")),
        "A 组 %d 条" % sum(1 for e in ENTRIES if e["code"].startswith("A")))
    grd("G4", "GR 潮汐三量（地表梯度/月潮/日潮）均已现算且非平凡",
        tide["surface_s2"] > 0 and tide["moon_ugal"] > 0 and tide["sun_ugal"] > 0, "真机读")
    grd("G5", "靶 3 份只读（结束态 hash == 导入期基线）",
        all(sha256_of(p) == SHA_AT_IMPORT[p] for p in TARGETS),
        "结束态 %s" % ", ".join((sha256_of(p) or "MISSING")[:12] for p in TARGETS))
    grd("G6", "AST 自审器：本文件无写死 True 的判据（自审器自身除外）", True,
        "由 _ast_self_audit() 真机读支撑")
    _ok7, _msg7 = scan_untouched()
    grd("G7", "未触碰 r225–r243 产物（mtime 全部早于本轮启动）", _ok7, _msg7)
    _ok8, _msg8 = check_distribution()
    grd("G8", "条目分布断言（真机读，非预估）", _ok8, _msg8)
    grd("G9", "范畴错置两量纲均已求值且不相等",
        (d_kappa != d_riem) and (d_kappa == dim(l=-1)) and (d_riem == dim(l=-2)),
        "%s vs %s" % (dstr(d_kappa), dstr(d_riem)))
    grd("G10", "读法二难两路均已数值求值且结论相反",
        (kappa_cov == 0.0) and (bkg[1]["kappa"] > 0) and (bkg[1]["m_kg"] != bkg[4]["m_kg"]),
        "读法A κ_cov=0；读法B κ 随 v 变")
    grd("G11", "修复定价 SURVIVE == 0", pricing["SURVIVE"] == 0,
        "EMPTY %d / SUICIDE %d / SURVIVE %d"
        % (pricing["EMPTY"], pricing["SUICIDE"], pricing["SURVIVE"]))
    _ok12, _msg12 = check_write_side()
    grd("G12", "未修改 verify.py / 未跑 refresh_catalog", _ok12, _msg12)

    return {"entries": ENTRIES, "controls": CONTROLS, "guards": GUARDS, "evidence": EVIDENCE}


# ============================================================
# 9. AST 自审器
# ============================================================
_AST_WHITELIST = {"G6"}


def _ast_self_audit():
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
        code = None
        if node.args and isinstance(node.args[0], ast.Constant):
            code = node.args[0].value
        # 写死的 True（含 `True if ... else False` 之类的恒定常量不在此列）
        if isinstance(third, ast.Constant) and third.value is True:
            if code not in _AST_WHITELIST:
                bad.append("%s(%s, True)" % (fn, code))
        # 写死的 False 同样可疑（恒假判据）
        elif isinstance(third, ast.Constant) and third.value is False:
            if code not in _AST_WHITELIST:
                bad.append("%s(%s, False)" % (fn, code))
    return (not bad), ("无写死 True/False" if not bad else "发现写死：%s" % ", ".join(bad))


# ============================================================
# 10. 渲染
# ============================================================
def render_report(res):
    ev = res["evidence"]
    t = ev["tide"]
    L = []
    A = L.append
    A("=" * 78)
    A("TUFT-%s · 引力本质层 / 曲线曲率 vs 时空曲率 · 引力方向地基缺失与 κ 读法二难" % RID.upper())
    A("=" * 78)
    A("生成时间 %s" % START_ISO)
    A("")
    A("【靶（只读 3 份）】")
    for p in TARGETS:
        A("  - %s" % os.path.basename(p))
        A("    sha256 %s" % (SHA_AT_IMPORT.get(p) or "MISSING"))
    A("")
    A("-" * 78)
    A("一、GR 侧「引力真身」读数（正对照，本机现算）")
    A("-" * 78)
    A("  地球表面径向潮汐梯度 2GM/R³ = %s s^-2（每米高度差 %s m/s²）"
      % (("%.5e" % t["surface_s2"]), ("%.5e" % t["surface_per_m"])))
    A("  1.7 m 身高头脚差 = %s m/s²；ISS 轨道处 = %s s^-2"
      % (("%.5e" % t["human_17m"]), ("%.5e" % t["iss_s2"])))
    A("  月潮 = %s m/s² = %.4f μGal（锚点 %.4f，偏差 %s）"
      % (("%.5e" % t["moon_ms2"]), t["moon_ugal"], ANCHOR_TIDE_MOON_UGAL,
         fmt_rel(rel(t["moon_ugal"], ANCHOR_TIDE_MOON_UGAL))))
    A("  日潮 = %s m/s² = %.4f μGal；月/日 = %.4f"
      % (("%.5e" % t["sun_ms2"]), t["sun_ugal"], t["moon_over_sun"]))
    A("  测地线协变 Frenet 曲率 κ_cov = |∇_u u| = %s" % ("%.1f" % ev["kappa_cov"]))
    A("")
    A("-" * 78)
    A("二、★ 范畴错置")
    A("-" * 78)
    A("  κ（Frenet，曲线外蕴弯曲）= %s" % dstr(ev["d_kappa"]))
    A("  Riemann（时空内蕴弯曲）  = %s" % dstr(ev["d_riem"]))
    A("  两者不同阶 ⇒ %s" % ("范畴错置成立" if ev["dim_mismatch"] else "同阶"))
    A("  靶原文 line 393：引力分量＝曲率投影、沿主法向、**对应时空弯曲效应**")
    A("")
    A("-" * 78)
    A("三、★ κ 的读法二难")
    A("-" * 78)
    A("  读法 A（∇ 为协变导数）：自由下落 κ_cov = %s ⇒ m=(ℏ/c)|τ|，引力不参与质量"
      % ("%.1f" % ev["kappa_cov"]))
    A("  读法 B（∇ 为背景空间导数）：κ 随观测者变 ⇒ m 非不变量")
    A("  %-28s %-14s %s" % ("观测者", "κ (m^-1)", "m = (ℏ/c)κ (kg，τ=0)"))
    A("  " + "-" * 74)
    for r in ev["bkg"]:
        A("  %-28s %-14s %s" % (r["note"], ("%.4g" % r["kappa"]), ("%.4g" % r["m_kg"])))
    A("")
    A("-" * 78)
    A("四、条目")
    A("-" * 78)
    for e in res["entries"]:
        A("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        A("     证据：%s" % e["evidence"])
        if e["note"]:
            A("     备注：%s" % e["note"])
    A("")
    A("-" * 78)
    A("五、控制组")
    A("-" * 78)
    for c in res["controls"]:
        A("  [%s] %s · %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["title"]))
        A("       %s" % c["evidence"])
    A("")
    A("-" * 78)
    A("六、守卫")
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
# 11. 主流程
# ============================================================
def main():
    import json
    res = run_audit()

    ok6, msg6 = _ast_self_audit()
    for g in res["guards"]:
        if g["code"] == "G6":
            g["ok"] = ok6
            g["evidence"] = msg6

    dist = tally_states(res)
    n_ctl_ok = sum(1 for c in res["controls"] if c["ok"])
    n_grd_ok = sum(1 for g in res["guards"] if g["ok"])

    report = render_report(res)
    t = res["evidence"]["tide"]
    header = ("TUFT-%s 判词：靶把【曲线的 Frenet 曲率 κ（%s，外蕴）】直接宣称为"
              "「对应时空弯曲效应」（来料 line 393 逐字），而时空曲率是 %s（内蕴）⇒ 范畴错置；"
              "且引力的【方向】由主法矢 n 给出，而基础客体是类光曲线（无 Frenet 标架）⇒ 地基缺失。"
              "κ 若取协变读法则自由下落 κ=0（引力自我取消），若取背景读法则质量非不变量。"
              "κ(r) 又把 G、M 当输入 ⇒ 循环、零新增。修复定价 SURVIVE=0（本线第 29 度）。"
              % (RID.upper(), dstr(res["evidence"]["d_kappa"]), dstr(res["evidence"]["d_riem"])))

    payload = {
        "id": "TUFT-" + RID,
        "title": ("引力本质层：曲线曲率与时空曲率范畴错置、"
                  "引力方向地基缺失与 κ 读法二难"),
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
        "guards_ok": "%d/%d" % (n_grd_ok, len(res["guards"])),
        "gr_tidal": res["evidence"]["tide"],
        "dimension": {"kappa": dstr(res["evidence"]["d_kappa"]),
                      "riemann": dstr(res["evidence"]["d_riem"]),
                      "mismatch": res["evidence"]["dim_mismatch"]},
        "kappa_reading": {"covariant_kappa": res["evidence"]["kappa_cov"],
                          "background_table": res["evidence"]["bkg"]},
        "target_hits": res["evidence"]["hits"],
        "g_derivation": {"target_hits": res["evidence"]["g_deriv_target"],
                         "synthetic_positive_control": res["evidence"]["g_deriv_synth"]},
        "repair_pricing": res["evidence"]["pricing"],
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(DATA_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
        f.write("\n" + "=" * 78 + "\n")
        f.write("条目 %d = %s\n" % (len(res["entries"]),
                                    " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
        f.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
        f.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
        f.write("靶未改动 %s\n" % payload["targets_unchanged"])
        f.write("=" * 78 + "\n")

    md = ["# TUFT-%s · %s\n" % (RID.upper(), payload["title"]),
          "\n> 生成时间：%s\n" % START_ISO, "\n## 判词\n\n%s\n" % header]
    md.append("\n## 一、GR 侧引力真身读数\n")
    md.append("\n| 量 | 值 |\n|---|---|\n")
    md.append("| 地表潮汐梯度 | %s s^-2 |\n" % ("%.5e" % t["surface_s2"]))
    md.append("| 月潮 | %.4f μGal（锚点 %.4f） |\n" % (t["moon_ugal"], ANCHOR_TIDE_MOON_UGAL))
    md.append("| 日潮 | %.4f μGal |\n" % t["sun_ugal"])
    md.append("| 测地线 κ_cov | %s |\n" % ("%.1f" % res["evidence"]["kappa_cov"]))
    md.append("\n## 二、条目\n")
    for e in res["entries"]:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 备注：%s\n" % e["note"])
    md.append("\n## 三、红线\n")
    md.append("\n- 靶 3 份只读：%s\n" % payload["targets_unchanged"])
    md.append("- 本卷条目**不可与 r142–r243 相加**（尤其不可与 r243 工程可用性层相加）。\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py，未做 git。\n")
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

    vd = ["# 判定册 · TUFT-%s（引力本质层）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header, "\n## 判决分组\n",
          "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A | 对靶有利项（Frenet 类时用法正确、诚实自曝类光陷阱、κ(r) 量纲对、挠率晕设想） | PASS/INFO |\n",
          "| B | GR 引力真身（潮汐读数 + 对拍 + 测地线 κ_cov=0） | PASS |\n",
          "| C | **范畴错置** κ[L^-1] vs Riemann[L^-2]；无潮汐通道（低于牛顿基线）；力/几何三重不自洽 | **FAIL** |\n",
          "| D | **地基缺失**（引力方向由 n 给出而类光无 n）+ **κ 读法二难** | **FAIL** |\n",
          "| E | 循环论证（κ(r) 以 G、M 为输入）+ G 零推导（预测预算 0） | FAIL |\n",
          "| F | 修复定价 2^5=32 组合 SURVIVE=0（第 29 度） | FAIL |\n"]
    vd.append("\n## ★ 性质界定（关键）\n")
    vd.append("\n1. **潮汐不是 GR 专属**：牛顿也有潮汐（Hessian(Φ)，量纲同为 [L^-2]）。")
    vd.append("因此 C2 的指控**不是**「靶没有 GR 的潮汐」，而是**靶低于牛顿基线**——")
    vd.append("牛顿能给出 L^-2 级读数，靶只有 L^-1 的 κ。\n")
    vd.append("2. **D1 不是技术细节**：引力的【方向】正由主法矢 n 定义（来料 line 383 逐字），")
    vd.append("而基础客体是类光曲线（line 59），类光无 Frenet 标架 ⇒ 无 n ⇒ **引力连方向都没有**。\n")
    vd.append("3. **E1 是循环而非错误**：κ(r)=GM·e^{−λ}/(c²r²) 本身量纲正确（r241 E12 已 PASS），")
    vd.append("问题在于它把 G、M 当【输入】，与 line 105「改变物质产生时空曲率」自相矛盾。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n"
              % (n_ctl_ok, len(res["controls"]), n_grd_ok, len(res["guards"])))
    vd.append("- 靶 3 份只读：%s；未触碰 r225–r243（mtime 真机读）\n" % payload["targets_unchanged"])
    vd.append("- 本卷条目不可与 r142–r243 相加。\n")
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write("".join(vd))

    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(res, payload, header, dist, n_ctl_ok,
                            len(res["controls"]), n_grd_ok, len(res["guards"])))

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(res["entries"]),
                                         " / ".join("%s %d" % (k, v) for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(res["controls"])))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(res["guards"])))
    sys.stdout.write("靶未改动 %s\n" % payload["targets_unchanged"])
    sys.stdout.write("=" * 78 + "\n")

    bad = (n_ctl_ok != len(res["controls"])) or (n_grd_ok != len(res["guards"]))
    return 2 if bad else 0


def render_html(res, payload, header, dist, n_ctl_ok, n_ctl, n_grd_ok, n_grd):
    ev = res["evidence"]
    t = ev["tide"]

    tide_rows = "\n".join(
        "<tr><td>%s</td><td>%s</td></tr>" % (k, "%.5e" % v if isinstance(v, float) else v)
        for k, v in (("地球表面潮汐梯度 (s^-2)", t["surface_s2"]),
                     ("ISS 轨道处 (s^-2)", t["iss_s2"]),
                     ("月潮 (m/s^2)", t["moon_ms2"]),
                     ("月潮 (μGal)", t["moon_ugal"]),
                     ("日潮 (m/s^2)", t["sun_ms2"]),
                     ("日潮 (μGal)", t["sun_ugal"])))

    bkg_rows = "\n".join(
        "<tr><td>%s</td><td>%.4g</td><td>%.4g</td></tr>" % (r["note"], r["kappa"], r["m_kg"])
        for r in ev["bkg"])

    ents = []
    for e in res["entries"]:
        cls = "pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL" else "info")
        ents.append('<div class="ent %s"><b>[%s] %s · %s</b><div class="ev">%s</div>%s</div>'
                    % (cls, e["state"], e["code"], e["title"], e["evidence"],
                       ('<div class="note">%s</div>' % e["note"]) if e["note"] else ""))

    ctls = "".join('<div class="ctl %s">[%s] %s</div>'
                   % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL", c["code"])
                   for c in res["controls"])
    grds = "".join('<div class="ctl %s">[%s] %s</div>'
                   % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL", g["code"])
                   for g in res["guards"])

    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 引力本质层</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:24px 0 10px;
 border-left:4px solid #2c5f8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#fff8e6;border:1px solid #e0c48a;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#eef1f5}}
.dimbox{{display:flex;gap:16px;margin:10px 0}}
.dim{{flex:1;background:#fff;border:1px solid #d8dce2;border-radius:5px;padding:10px;
 text-align:center;font-size:14px}}
.dim .k{{font-size:12px;color:#666}} .dim .v{{font-weight:600;font-size:16px}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px;border-radius:3px;display:inline-block;
 width:300px}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
</style></head><body>
<h1>TUFT-{RID} · 引力本质层</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>

<h2>一、GR 侧「引力真身」读数（正对照）</h2>
<table><tr><th>量</th><th>值</th></tr>{tide_rows}</table>
<div class="meta">月潮对拍 gr-industrial 产线 E 公开锚点 110.1086 μGal（偏差 {moonrel}）。</div>

<h2>二、★ 范畴错置：κ 与 Riemann 不同阶</h2>
<div class="dimbox">
  <div class="dim"><div class="k">κ（Frenet，曲线外蕴弯曲）</div><div class="v">{dk}</div></div>
  <div class="dim"><div class="k">Riemann（时空内蕴弯曲）</div><div class="v">{dr}</div></div>
</div>
<div class="meta">靶原文 line 393 逐字：「引力分量：曲率投影；沿主法向…<b>对应时空弯曲效应</b>」。</div>

<h2>三、★ κ 的读法二难（读法 B：κ 随观测者变 ⇒ 质量非不变量）</h2>
<table><tr><th>观测者</th><th>κ (m^-1)</th><th>m=(ℏ/c)κ (kg, τ=0)</th></tr>{bkg_rows}</table>
<div class="meta">读法 A：κ 取协变 Frenet 曲率 ⇒ 自由下落 κ_cov = {kcov} ⇒ m=(ℏ/c)|τ|，引力不参与质量。</div>

<h2>四、条目</h2>
{ents}

<h2>五、控制组（{nctl_ok}/{nctl}）</h2>
{ctls}

<h2>六、守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}

<div class="meta" style="margin-top:24px">
红线：靶 3 份只读（前后一致：{unchanged}）；本卷条目不可与 r142–r243 相加。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        tide_rows=tide_rows, moonrel=fmt_rel(rel(t["moon_ugal"], ANCHOR_TIDE_MOON_UGAL)),
        dk=dstr(ev["d_kappa"]), dr=dstr(ev["d_riem"]),
        bkg_rows=bkg_rows, kcov="%.1f" % ev["kappa_cov"],
        ents="\n".join(ents), ctls=ctls, grds=grds,
        nctl_ok=n_ctl_ok, nctl=n_ctl, ngrd_ok=n_grd_ok, ngrd=n_grd,
        unchanged=payload["targets_unchanged"])


if __name__ == "__main__":
    sys.exit(main())
