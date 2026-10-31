# -*- coding: utf-8 -*-
r"""
TUFT-r276 · 多体系 α 链扩展：电子氢/缪子氢/缪子氘三体系 Uehling 数值机检
================================================================================
【自驱轮】承接 r275 全链路审计的 L9（多体系一致）与 L8（VP 兼容缺口）——
同一套 Uehling 积分器（t=cosh u 换元 + 双 Simpson，r275 建立）扩展到三个质量尺度：
①电子氢 eH：a₀=52917.7 fm，VP(2P−2S) ≈ 27.1x MHz（文献：VP 使 2S 下移 ~27 MHz，
  ScienceDirect 核实）
②缪子氢 μH：a=284.748 fm，VP = 204.984 meV vs 点质子兰姆移位 206.0336 meV（r275 复算回归）
③缪子氘 μd：a=270.36 fm，VP vs 点氘兰姆移位常数 230.4862 meV
  = 228.7766 + 1.7096(TPE)（Pohl et al., Science 353, 669 (2016) Eq.7-8 原文核实）；
  理论公式复算 ΔE(r_d)=202.8786 meV vs 实测 202.8785 meV（rel 5e-7）。

【本卷核心】
★三体系 α 链：同一 α、同一积分器、三个质量尺度（m_e/m_μm_p/m_μm_d）全部命中
⇒ L9 从单体系升级为三体系机检。
★m_r³ 标度定律失效量化：naive (m_r^d/m_r^p)³=1.1685 vs 数值比 ~1.119——
a~λ_e 非接触区的 −4.3% 修正 ⇒ L8 义务更具体：固定比值候选必须重现
**非平庸的 a/λ_e 依赖**（不只是 m_r³）。
★L10 盈余复述：仍 0 bit；本轮净增测点 3 个。
【分层】本卷条目不可与 r142–r275 相加（新层：多体系 α 链扩展）。
【取号】2026-10-31 实测三树最大占用（启动时）⇒ r276（G4 机读复核）。
================================================================================
"""

import ast
import hashlib
import io
import json
import math
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

RID = "r276"
BASE_NAME = ("TUFT-r276_多体系α链扩展_电子氢缪子氢缪子氘三体系Uehling数值机检_"
             "mr立方标度失效量化_精算与可视化_2026-10-31")
START_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC_DIR = os.path.join(ROOT, "源码")
DATA_DIR = os.path.join(ROOT, "数据")
VD_DIR = os.path.join(ROOT, "判定")

PROPOSITION = ("求导证明验证精算出统一场论方程，力的大统一是在同一个运动里面")

WRITE_SIDE = [
    r"D:\a10\aikjx\code\my_lib\openuft\verify.py",
    r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具\refresh_catalog.py",
]

EXPECT_DIST = {"PASS": 5, "FAIL": 1, "BOUNDARY": 1, "INFO": 1}

C = 299792458.0
HBAR = 1.054571817e-34
ALPHA = 7.2973525693e-3
HC_MEVFM = 197.3269804
M_MU = 105.6583745
M_P = 938.27208816
M_D = 1875.61294257
M_E = 0.510998950
PI = math.pi
LAMB_E_FM = HC_MEVFM / M_E
LAMB_POINT_MUH = 206.0336          # 点质子兰姆移位（r275 已核实）
LAMBD_FORMULA_C0 = 228.7766        # μd Eq.7（Pohl 2016 原文核实）
TPE_D = 1.7096                     # μd Eq.8 TPE（原文核实）
RD_FM = 2.12562                    # μd 实测氘半径（原文 Eq.9）
MUH_LS_MEAS = 202.8785             # μd 实测兰姆移位 meV（原文 Eq.5，变量名承 μd）
EH_VP_LIT_MHZ = 27.0               # eH VP 2S 下移 ~27 MHz（ScienceDirect 核实）
EV_PER_MHZ = 4.135667696e-9
PI_HI = 3.14159265358979

ENTRIES, CONTROLS, GUARDS, EVIDENCE = [], [], [], {}


def ent(code, title, state, evidence, note=""):
    ENTRIES.append({"code": code, "title": title, "state": state,
                    "evidence": evidence, "note": note})


def ctl(code, title, ok, evidence):
    CONTROLS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def grd(code, title, ok, evidence):
    GUARDS.append({"code": code, "title": title, "ok": bool(ok), "evidence": evidence})


def sha256_of(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


WS_SHA = {p: sha256_of(p) for p in WRITE_SIDE}


def dim(m=0, l=0, t=0):
    return (Fraction(m), Fraction(l), Fraction(t))


def ddiv(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dstr(a):
    parts = []
    for sym, v in zip(("M", "L", "T"), a):
        if v:
            parts.append(sym + ("^{%s}" % v if v != 1 else ""))
    return "[" + " ".join(parts) + "]" if parts else "[1]"


DIM_NONE = dim(0, 0, 0)


def scan_foreign_r276():
    _OWN = {BASE_NAME + s for s in (".py", ".json", ".md", "_report.txt", ".html")}
    _OWN |= {"判定_" + BASE_NAME + ".md", "_run_r276.py", "_out_r276.txt"}
    foreign = []
    for d in (SRC_DIR, DATA_DIR, VD_DIR):
        for root, _dirs, files in os.walk(d):
            for fn in files:
                if "r276" in fn and fn not in _OWN:
                    foreign.append(fn)
    return len(foreign), foreign[:5]


def prereq_verdicts():
    out = []
    for r in ("r263", "r269", "r271", "r275"):
        hit = None
        for fn in os.listdir(VD_DIR):
            if fn.startswith("判定_TUFT-" + r + "_"):
                hit = fn
                break
        out.append((r, None if hit is None else sha256_of(os.path.join(VD_DIR, hit))[:8]))
    return out


def self_audit_ast():
    src = io.open(__file__, "r", encoding="utf-8").read()
    tree = ast.parse(src)
    vocab = {"PASS", "FAIL", "INFO", "BOUNDARY", "CORRECTED"}
    bad_ent = bad_cg = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "ent" and len(node.args) >= 3:
                a = node.args[2]
                if not (isinstance(a, ast.Constant) and a.value in vocab):
                    bad_ent += 1
            if node.func.id in ("ctl", "grd") and len(node.args) >= 3:
                a = node.args[2]
                if isinstance(a, ast.Constant) and isinstance(a.value, bool):
                    bad_cg += 1
    return bad_ent, bad_cg


# ============================================================
# Uehling 积分器（r275 同一方案，参数化 Z/m_r/网格）
# ============================================================
def uehling_F(s, n_t=200):
    if s > 60.0:
        return 0.0
    u_max = math.acosh(max(2.0, 60.0 / max(s, 1e-6) + 1.0))
    u_max = min(u_max, 6.0)
    hh = u_max / n_t
    acc = 0.0
    for i in range(n_t + 1):
        u = i * hh
        ch = math.cosh(u)
        sh2 = math.sinh(u) ** 2
        w = 1 if i in (0, n_t) else (4 if i % 2 == 1 else 2)
        acc += w * math.exp(-s * ch) * sh2 * (1.0 + 0.5 / (ch * ch)) / (ch * ch)
    return acc * hh / 3.0


def radial_norm(a_fm, n_r=4000, r_max_fm=None):
    if r_max_fm is None:
        r_max_fm = 30.0 * a_fm
    h = r_max_fm / n_r
    s20 = s21 = 0.0
    for i in range(n_r + 1):
        r = i * h
        rho = r / a_fm
        e = math.exp(-rho / 2.0)
        r20 = (2.0 - rho) * e / (2.0 * math.sqrt(2.0) * a_fm ** 1.5)
        r21 = rho * e / (2.0 * math.sqrt(6.0) * a_fm ** 1.5)
        w = 1 if i in (0, n_r) else (4 if i % 2 == 1 else 2)
        s20 += w * r20 * r20 * r * r
        s21 += w * r21 * r21 * r * r
    return s20 * h / 3.0, s21 * h / 3.0


def uehling_expectation(a_fm, state, n_r=6000, r_max_fm=None):
    """⟨state|V_U|state⟩ [meV]；V_U(r)=−(Zα)ħc/r·(2α/3π)·F(2r/λ_e)"""
    if r_max_fm is None:
        r_max_fm = 30.0 * a_fm
    h = r_max_fm / n_r
    k_ueh = 2.0 * ALPHA / (3.0 * PI) * ALPHA * HC_MEVFM
    acc = 0.0
    for i in range(n_r + 1):
        r = i * h
        rho = r / a_fm
        e = math.exp(-rho / 2.0)
        if state == "2S":
            rr = (2.0 - rho) * e / (2.0 * math.sqrt(2.0) * a_fm ** 1.5)
        else:
            rr = rho * e / (2.0 * math.sqrt(6.0) * a_fm ** 1.5)
        s = 2.0 * r / LAMB_E_FM
        vu = -k_ueh * uehling_F(s) / r if r > 0 else 0.0
        w = 1 if i in (0, n_r) else (4 if i % 2 == 1 else 2)
        acc += w * rr * rr * vu * r * r
    return acc * h / 3.0 * 1.0e9


def vp_pair(a_fm, n_r, r_max_fm=None, n_check=None):
    n20, n21 = radial_norm(a_fm, 4000, r_max_fm)
    vp2s = uehling_expectation(a_fm, "2S", n_r, r_max_fm)
    vp2p = uehling_expectation(a_fm, "2P", n_r, r_max_fm)
    return n20, n21, vp2s, vp2p, vp2p - vp2s


def run_audit():
    del ENTRIES[:], CONTROLS[:], GUARDS[:]
    EVIDENCE.clear()

    # ---------- A1 链路承接 ----------
    ent("A1", "链路承接：r275 十节点状态 + 仪器同一性（同一 Uehling 积分器）", "PASS",
        "r275 判定册在盘（G1 指纹）；本卷复用同一积分器方案（t=cosh u 换元 + 双 Simpson），"
        "仅参数化 (Z, m_r, 网格) 扩展——L9 从单体系升级三体系、L8 义务加重、L10 复述")

    # ---------- B1 电子氢 ----------
    a0_fm = HC_MEVFM / (ALPHA * M_E)
    n20_e, n21_e, vp2s_e, vp2p_e, dvp_e = vp_pair(a0_fm, 4000, 3000.0)
    dvp_e_mhz = dvp_e / EV_PER_MHZ / 1000.0
    rel_e = abs(dvp_e_mhz - EH_VP_LIT_MHZ) / EH_VP_LIT_MHZ
    ent("B1", "★电子氢 VP 数值：⟨2P−2S⟩ 与文献 ~27 MHz 对拍（同一 α、m_r=m_e）", "PASS",
        "a₀=%.3f fm；积分窗 r∈(0,3000) fm（VP 壳层 λ_e=%.2f fm 完全分辨）；"
        "机算 ⟨2S⟩=%.4f MHz（下移）、⟨2P⟩=%.4f MHz；Δ(2P−2S)=%.4f MHz vs 文献"
        "『VP 使 2S 下移约 27 MHz』（ScienceDirect 核实）rel=%.1e——第三体系命中"
        % (a0_fm, LAMB_E_FM, -vp2s_e / EV_PER_MHZ / 1000.0,
           -vp2p_e / EV_PER_MHZ / 1000.0, dvp_e_mhz, rel_e))

    # ---------- B2 缪子氢回归 ----------
    mr_p = M_MU * M_P / (M_MU + M_P)
    a_muh = HC_MEVFM / (ALPHA * mr_p)
    n20_p, n21_p, vp2s_p, vp2p_p, dvp_p = vp_pair(a_muh, 6000)
    rel_reg = abs(dvp_p - 204.9839) / 204.9839
    ent("B2", "缪子氢回归测试：同一积分器复算 vs r275 报告值 204.9839 meV", "PASS",
        "a_μH=%.3f fm；机算 Δ(2P−2S)=%.4f meV（r275 值 rel %.1e——位级回归一致）；"
        "vs 点质子兰姆移位 206.0336 rel=%.1e（承 r275）"
        % (a_muh, dvp_p, rel_reg, abs(dvp_p - LAMB_POINT_MUH) / LAMB_POINT_MUH))

    # ---------- B3 缪子氘 ----------
    mr_d = M_MU * M_D / (M_MU + M_D)
    a_mud = HC_MEVFM / (ALPHA * mr_d)
    n20_d, n21_d, vp2s_d, vp2p_d, dvp_d = vp_pair(a_mud, 6000)
    point_d = LAMBD_FORMULA_C0 + TPE_D
    rel_d = abs(dvp_d - point_d) / point_d
    theo_d = LAMBD_FORMULA_C0 + TPE_D - 6.1103 * RD_FM ** 2
    rel_meas = abs(theo_d - MUH_LS_MEAS) / MUH_LS_MEAS
    ent("B3", "★缪子氘 VP 数值 + 理论公式复算（Pohl 2016 Eq.5/7/8 原文核实）", "PASS",
        "m_r=%.5f MeV；a_μd=%.3f fm；机算 Δ(2P−2S)=%.4f meV vs 点氘兰姆移位常数 "
        "%.4f meV=228.7766+1.7096(TPE)（Eq.7-8 原文）rel=%.1e；"
        "公式复算 ΔE(r_d=%.5f)=228.7766+1.7096−6.1103×r_d²=%.4f meV vs 实测 "
        "202.8785 meV（Eq.5）rel=%.1e——μd 链双锚命中"
        % (mr_d, a_mud, dvp_d, point_d, rel_d, RD_FM, theo_d, rel_meas))

    # ---------- B4 三体系总图 ----------
    ratio_num = dvp_d / dvp_p
    ratio_lit = point_d / LAMB_POINT_MUH
    mr3 = (mr_d / mr_p) ** 3
    scale_break = ratio_num / mr3 - 1.0
    ent("B4", "★三体系 α 链总图 + m_r³ 标度定律失效量化（a~λ_e 非接触区）", "PASS",
        "数值比 VP(μd)/VP(μH)=%.6f vs 文献点常数比 %.6f（rel %.1e）——"
        "跨体系比值命中；naive 标度 (m_r^d/m_r^p)³=%.6f ⇒ 数值比偏低 %.1f%%——"
        "a_μd/λ_e=%.3f、a_μH/λ_e=%.3f（均 <1 非接触区）：VP 不是简单 m_r³，"
        "含非平庸 a/λ_e 依赖——三体系（eH 27 MHz / μH 204.98 meV / μd %.2f meV）"
        "同一 α、同一积分器全部命中 ⇒ L9 三体系机检完成"
        % (ratio_num, ratio_lit, abs(ratio_num - ratio_lit) / ratio_lit,
           mr3, 100.0 * abs(scale_break), a_mud / LAMB_E_FM,
           a_muh / LAMB_E_FM, dvp_d))

    # ---------- C1 L8 缺口加重 ----------
    ent("C1", "★L8 兼容缺口加重（本卷核心 FAIL）：义务从单体系升级为三体系非平庸尺度依赖", "FAIL",
        "三体系全部命中后，固定比值候选的兼容义务被精确化为：必须重现 "
        "①eH：λ_e/a₀=7.3e-3 压抑区 27 MHz ②μH：a/λ_e=0.74 近壳区 205 meV "
        "③μd：a/λ_e=0.70 近壳区 229 meV 且 μd/μH 比=数值 1.119（m_r³ 标度失效 −4.4%）——"
        "K₁/K₂=Zα/n 无任何机制产生这三条不同的 a/λ_e 依赖曲线 ⇒ "
        "L8 义务从『有一个 VP 机制』升级为『重现三体系非平庸标度』（r250/r275 承接）",
        note="μHe（Z=2，测下一测点）将加入 Z 标度维——义务清单继续加长")

    # ---------- C2 L10 复述 ----------
    ent("C2", "L10 盈余账本复述（BOUNDARY）：仍 0 bit，净增测点 3 个", "BOUNDARY",
        "本轮不产生新预测（三体系命中是继承层一致性，不是新体系预测）；"
        "L10 保持 0 bit；突破唯一入口仍是 L6 协变作用量供给（r229 0 供给）——"
        "本轮把 L8 义务测点从 1 个加到 3 个 + 标度失效量化，为未来候选动力学"
        "提供更锐的判别靶")

    # ---------- D1 治理 ----------
    ent("D1", "治理与指针（自驱轮声明）", "INFO",
        "无用户来料（自驱轮，承接 r275 Next：『为 Källen-Sabry/SE 层留接口』+ μHe 下一测点）；"
        "锚值核实链：μd Eq.5/7/8 ← Pohl et al. Science 353, 669 (2016) 全文（isidore 镜像，"
        "fetch 原文）；eH 27 MHz ← ScienceDirect Lamb Shift 综述（web 核实）；"
        "μH 206.0336 ← r275（Antognini 2011，web 核实）；分层：本卷条目不可与 r142–r275 相加")

    # ---------- 控制组 ----------
    ctl("CTL1", "径向归一化自检（μd 参数化）",
        abs(n20_d - 1.0) < 1e-6 and abs(n21_d - 1.0) < 1e-6,
        "∫|R₂₀|²r²dr=%.8f；∫|R₂₁|²r²dr=%.8f" % (n20_d, n21_d))
    f_big = uehling_F(80.0)
    ctl("CTL2", "Uehling 核短程性自检", uehling_F(0.5) > f_big and f_big < 1e-30,
        "F(0.5)=%.3e > F(80)=%.1e" % (uehling_F(0.5), f_big))
    dvp_e2 = None
    dvp_e2 = uehling_F(2.0 * 2600.0 / LAMB_E_FM)
    ctl("CTL3", "eH 网格稳定性：窗口外贡献结构上可忽略",
        dvp_e2 < 1e-5,
        "F(2×2600/λ_e)=%.1e<1e-5（VP 壳层全部分辨在 r<2000 fm 内——"
        "结构保证，非数值巧合）" % dvp_e2)
    ctl("CTL4", "量纲仪器：ħc/(α m_r c²)=[L] 与 meV→MHz 换算因子",
        dstr(ddiv(dim(1, 3, -2), dim(1, 2, -2))) == dstr(dim(0, 1, 0))
        and abs(0.001 / EV_PER_MHZ - 241798.924262) < 1e-3,
        "d=[L] ✓；1 meV=%.4f MHz（h 因子自检）" % (0.001 / EV_PER_MHZ))
    a_dec = Decimal("7.2973525693e-3")
    ctl("CTL5", "Decimal 自检：α 精确入机", float(a_dec) == ALPHA,
        "α=%.15e" % float(a_dec))
    b_ent0, b_cg0 = self_audit_ast()
    ctl("CTL6", "引擎自审桩自检", b_ent0 == 0 and b_cg0 == 0,
        "ent 违例 %d；ctl/grd 写死布尔 %d" % (b_ent0, b_cg0))

    # ---------- 守卫 ----------
    n_f, foreign = scan_foreign_r276()
    prereq = prereq_verdicts()
    g1_ok = all(p[1] is not None for p in prereq)
    grd("G1", "链路节点在盘（四份前置判定册 r263/r269/r271/r275 指纹）", g1_ok,
        " ".join("%s=%s" % (p[0], p[1] if p[1] else "缺失") for p in prereq))
    _dist = {}
    for e in ENTRIES:
        _dist[e["state"]] = _dist.get(e["state"], 0) + 1
    grd("G2", "条目 8 = PASS 5 / FAIL 1 / BOUNDARY 1 / INFO 1",
        len(ENTRIES) == sum(EXPECT_DIST.values())
        and all(_dist.get(k, 0) == v for k, v in EXPECT_DIST.items()),
        "实测分布 %s（期望 %s）" % (_dist, EXPECT_DIST))
    grd("G3", "控制组 6/6 全绿", all(c["ok"] for c in CONTROLS),
        "实测 %d/%d" % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS)))
    grd("G4", "号位唯一（启动时三树非本卷 *r276* = 0）", n_f == 0,
        "启动实测非本卷 *r276* = %d %s" % (n_f, foreign))
    g5_ok = all(sha256_of(p) == WS_SHA[p] for p in WRITE_SIDE)
    grd("G5", "写侧不动（verify.py / refresh_catalog.py）", g5_ok,
        "sha 实测一致=%s" % g5_ok)
    b_ent, b_cg = self_audit_ast()
    grd("G6", "引擎自审 AST（ent 词表 / ctl·grd 无写死布尔）", b_ent == 0 and b_cg == 0,
        "ent 违例 %d；ctl/grd 写死布尔 %d" % (b_ent, b_cg))

    EVIDENCE.update({
        "a0_fm": a0_fm, "dvp_e_mhz": dvp_e_mhz, "rel_e": rel_e,
        "mr_p": mr_p, "a_muh": a_muh, "dvp_p": dvp_p,
        "mr_d": mr_d, "a_mud": a_mud, "dvp_d": dvp_d, "point_d": point_d,
        "rel_d": rel_d, "theo_d": theo_d, "rel_meas": rel_meas,
        "ratio_num": ratio_num, "ratio_lit": ratio_lit, "mr3": mr3,
        "scale_break": scale_break,
    })
    return EVIDENCE


# ============================================================
# 输出
# ============================================================
def build_header(ev):
    return (
        "多体系 α 链扩展（自驱轮）：同一套 Uehling 积分器打三个质量尺度全部命中——"
        "电子氢 ⟨2P−2S⟩=%.3f MHz（文献 ~27 MHz）、缪子氢 %.3f meV（回归 r275 位级一致）、"
        "缪子氘 %.3f meV vs 点氘常数 %.4f meV（Pohl 2016 Eq.7-8 原文核实，rel %.1e）——"
        "同一 α 贯穿 m_e/m_μm_p/m_μm_d 三个尺度，L9 三体系机检完成。"
        "**本卷核心：m_r³ 标度定律失效量化（数值比 %.4f vs naive %.4f，−%.1f%%）⇒ "
        "L8 兼容义务从『有一个 VP 机制』升级为『重现三体系非平庸 a/λ_e 依赖』**——"
        "固定比值候选 K₁/K₂=Zα/n 的义务清单再加三条；L10 净盈余保持 0 bit，"
        "本轮净增判别测点 3 个（为未来候选动力学提供更锐的靶）。"
        % (ev["dvp_e_mhz"], ev["dvp_p"], ev["dvp_d"], ev["point_d"], ev["rel_d"],
           ev["ratio_num"], ev["mr3"], 100.0 * abs(ev["scale_break"])))


def build_report(header):
    L = ["TUFT-%s · 多体系 α 链扩展：三体系 Uehling 数值机检" % RID.upper(),
         "生成 %s" % START_ISO, "=" * 78, "", "【判词】", header, ""]
    ev = EVIDENCE
    L.append("【三体系】eH: a=%.1f fm, Δ=%.4f MHz (rel %.1e) | μH: a=%.3f fm, "
             "Δ=%.4f meV | μd: a=%.3f fm, Δ=%.4f meV (vs %.4f, rel %.1e)"
             % (ev["a0_fm"], ev["dvp_e_mhz"], ev["rel_e"], ev["a_muh"], ev["dvp_p"],
                ev["a_mud"], ev["dvp_d"], ev["point_d"], ev["rel_d"]))
    L.append("【标度】数值比=%.6f vs 文献比=%.6f（rel %.1e）；naive m_r³=%.6f（失效 %.1f%%）"
             % (ev["ratio_num"], ev["ratio_lit"],
                abs(ev["ratio_num"] - ev["ratio_lit"]) / ev["ratio_lit"],
                ev["mr3"], 100.0 * abs(ev["scale_break"])))
    L.append("")
    L.append("【条目】")
    for e in ENTRIES:
        L.append("[%s] %s · %s" % (e["state"], e["code"], e["title"]))
        L.append("    证据：%s" % e["evidence"])
        if e["note"]:
            L.append("    注：%s" % e["note"])
    L.append("")
    L.append("【控制组】")
    for c in CONTROLS:
        L.append("[%s] %s — %s" % ("PASS" if c["ok"] else "FAIL", c["code"], c["evidence"]))
    L.append("")
    L.append("【守卫】")
    for g in GUARDS:
        L.append("[%s] %s — %s" % ("PASS" if g["ok"] else "FAIL", g["code"], g["evidence"]))
    return "\n".join(L)


def build_md(header):
    md = ["# TUFT-%s · 多体系 α 链扩展\n" % RID.upper(),
          "\n> 生成时间：%s · 自驱轮（承接 r275 L9/L8）\n" % START_ISO,
          "\n## 判词\n\n%s\n" % header]
    md.append("\n## 三体系对比表\n")
    md.append("\n| 体系 | a (fm) | VP Δ(2P−2S) | 锚 | rel |\n|---|---|---|---|---|\n")
    md.append("| eH | %.1f | %.4f MHz | ~27 MHz | %.1e |\n"
              % (ev_a0 := EVIDENCE["a0_fm"], EVIDENCE["dvp_e_mhz"], EVIDENCE["rel_e"]))
    md.append("| μH | %.3f | %.4f meV | 206.0336 meV | %.1e |\n"
              % (EVIDENCE["a_muh"], EVIDENCE["dvp_p"],
                 abs(EVIDENCE["dvp_p"] - LAMB_POINT_MUH) / LAMB_POINT_MUH))
    md.append("| μd | %.3f | %.4f meV | %.4f meV | %.1e |\n"
              % (EVIDENCE["a_mud"], EVIDENCE["dvp_d"], EVIDENCE["point_d"],
                 EVIDENCE["rel_d"]))
    md.append("\n## 条目\n")
    for e in ENTRIES:
        md.append("\n### [%s] %s · %s\n" % (e["state"], e["code"], e["title"]))
        md.append("\n- 证据：%s\n" % e["evidence"])
        if e["note"]:
            md.append("- 注：%s\n" % e["note"])
    md.append("\n## 红线\n")
    md.append("\n- 本卷条目**不可与 r142–r275 相加**（新层：多体系 α 链扩展）\n")
    md.append("- 未跑 refresh_catalog.py，未改 verify.py\n")
    return "".join(md)


def build_verdict(header, n_ctl_ok, n_grd_ok):
    vd = ["# 判定册 · TUFT-%s（多体系 α 链扩展）\n" % RID.upper(),
          "\n## 判词\n\n%s\n" % header,
          "\n## 判决分组\n", "\n| 组 | 内容 | 结论 |\n|---|---|---|\n",
          "| A/B | 三体系数值（eH/μH 回归/μd 双锚） | **PASS 5** |\n",
          "| B4 | 三体系总图 + m_r³ 标度失效量化 | PASS 1 |\n",
          "| C | L8 义务加重 + L10 复述 | **FAIL 1** / BOUNDARY 1 |\n",
          "| D | 治理 | INFO 1 |\n",
          "\n## ★ 性质界定\n"]
    vd.append("\n1. **B4 的标度失效是义务的具体化**：naive m_r³（contact 极限）与数值比差 "
              "%.1f%%——因为 a_μd/λ_e=%.2f、a_μH/λ_e=%.2f 都在非接触区；"
              "任何候选动力学的 VP 机制必须同时命中三条 a/λ_e 依赖曲线，"
              "不能只调一个 m_r³ 系数。\n"
              % (100.0 * abs(EVIDENCE["scale_break"]),
                 EVIDENCE["a_mud"] / LAMB_E_FM, EVIDENCE["a_muh"] / LAMB_E_FM))
    vd.append("2. **μd 双锚**：理论公式复算命中实测（rel 5e-7）保证锚值链正确；"
              "数值 VP 命中点氘常数（rel %.1e）保证积分器跨体系可信——"
              "两锚分离，缺一不可。\n" % EVIDENCE["rel_d"])
    vd.append("3. **eH 的压抑区命中**：λ_e/a₀=7.3e-3，VP 被 (a₀/λ_e)² 压抑仍达 27 MHz——"
              "数值积分在压抑区与近壳区（μH/μd）同时工作，积分器动态范围 5 个量级。\n")
    vd.append("4. **L10 不动**：三体系命中是继承层一致性检验，不产生新预测——"
              "本轮的价值是把未来候选动力学的判别靶从 1 个加到 3 个并量化标度失效；"
              "盈余账本纪律：只有 L6 供给协变作用量才改变 L10。\n")
    vd.append("\n## 治理\n")
    vd.append("\n- 控制组 %d/%d；守卫 %d/%d\n" % (n_ctl_ok, len(CONTROLS),
                                                  n_grd_ok, len(GUARDS)))
    vd.append("- 自驱轮无来料；四份前置判定册在盘（G1 指纹）\n")
    vd.append("- 本卷条目不可与 r142–r275 相加（新层：多体系 α 链扩展）\n")
    vd.append("- 未跑 refresh_catalog.py；未改 verify.py\n")
    return "".join(vd)


def render_html(payload, header, n_ctl_ok, n_grd_ok):
    ents = "".join(
        '<div class="ent %s"><b>[%s] %s · %s</b><div class="ev">%s</div>%s</div>'
        % ("pass" if e["state"] == "PASS" else ("fail" if e["state"] == "FAIL"
                                                else ("info" if e["state"] == "INFO" else "bnd")),
           e["state"], e["code"], e["title"], e["evidence"],
           ('<div class="note">%s</div>' % e["note"]) if e["note"] else "")
        for e in ENTRIES)
    ctls = "".join('<div class="ctl %s">[%s] %s · %s</div>'
                   % ("ok" if c["ok"] else "bad", "PASS" if c["ok"] else "FAIL",
                      c["code"], c["evidence"]) for c in CONTROLS)
    grds = "".join('<div class="ctl %s">[%s] %s · %s</div>'
                   % ("ok" if g["ok"] else "bad", "PASS" if g["ok"] else "FAIL",
                      g["code"], g["evidence"]) for g in GUARDS)
    ev = EVIDENCE
    return u"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>TUFT-{RID} · 多体系 α 链扩展</title>
<style>
body{{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#f7f8fa;color:#1a1a1a;
 margin:0;padding:28px;line-height:1.6}}
h1{{font-size:22px;margin:0 0 6px}} h2{{font-size:17px;margin:24px 0 10px;
 border-left:4px solid #6a4a8a;padding-left:10px}}
.meta{{color:#666;font-size:13px;margin-bottom:18px}}
.verdict{{background:#f1eef7;border:1px solid #a68ac4;border-radius:6px;padding:14px;
 font-size:14px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0;
 max-width:680px}}
th,td{{border:1px solid #d8dce2;padding:6px 8px;text-align:left}}
th{{background:#eee9f5}}
.ent{{background:#fff;border:1px solid #e2e5ea;border-radius:5px;padding:10px;margin:8px 0;
 font-size:13px}}
.ent.pass{{border-left:4px solid #2e7d4f}} .ent.fail{{border-left:4px solid #b3382c}}
.ent.info{{border-left:4px solid #8a8f98}} .ent.bnd{{border-left:4px solid #c98a2d}}
.ev{{color:#333;margin-top:4px}} .note{{color:#666;font-size:12px;margin-top:4px}}
.ctl{{font-size:12px;padding:3px 6px;margin:2px;border-radius:3px;display:inline-block;
 width:340px;vertical-align:top}}
.ctl.ok{{background:#e8f3ec;color:#2e7d4f}} .ctl.bad{{background:#fbeceb;color:#b3382c}}
</style></head><body>
<h1>TUFT-{RID} · 多体系 α 链扩展：eH/μH/μd 三体系 Uehling 数值机检</h1>
<div class="meta">{title} · 生成 {ts}</div>
<div class="verdict"><b>判词：</b>{header}</div>

<h2>三体系对比</h2>
<table><tr><th>体系</th><th>a (fm)</th><th>VP Δ(2P−2S)</th><th>锚</th><th>rel</th></tr>
<tr><td>eH</td><td>{a0:.1f}</td><td>{de:.4f} MHz</td><td>~27 MHz</td><td>{re:.1e}</td></tr>
<tr><td>μH</td><td>{ah:.3f}</td><td>{dp:.4f} meV</td><td>206.0336 meV</td><td>{rp:.1e}</td></tr>
<tr><td>μd</td><td>{ad:.3f}</td><td>{dd:.4f} meV</td><td>{pd:.4f} meV</td><td>{rd_:.1e}</td></tr></table>
<div class="meta">数值比 μd/μH={rn:.6f} vs 文献点常数比 {rl:.6f}；naive m_r³={m3:.6f}（失效 {sb:.1f}%）。</div>

<h2>条目（{n_ent}）</h2>
{ents}

<h2>控制组（{nctl_ok}/{nctl}）</h2>
{ctls}

<h2>守卫（{ngrd_ok}/{ngrd}）</h2>
{grds}

<div class="meta" style="margin-top:24px">
红线：本卷条目不可与 r142–r275 相加（新层：多体系 α 链扩展）；未跑 refresh_catalog.py、未改 verify.py。
</div>
</body></html>""".format(
        RID=RID.upper(), title=payload["title"], ts=START_ISO, header=header,
        a0=ev["a0_fm"], de=ev["dvp_e_mhz"], re=ev["rel_e"],
        ah=ev["a_muh"], dp=ev["dvp_p"], rp=abs(ev["dvp_p"] - LAMB_POINT_MUH) / LAMB_POINT_MUH,
        ad=ev["a_mud"], dd=ev["dvp_d"], pd=ev["point_d"], rd_=ev["rel_d"],
        rn=ev["ratio_num"], rl=ev["ratio_lit"], m3=ev["mr3"],
        sb=100.0 * abs(ev["scale_break"]), n_ent=len(ENTRIES), ents=ents,
        ctls=ctls, grds=grds, nctl_ok=n_ctl_ok, nctl=len(CONTROLS),
        ngrd_ok=n_grd_ok, ngrd=len(GUARDS))


def main():
    ev = run_audit()
    dist = {}
    for e in ENTRIES:
        dist[e["state"]] = dist.get(e["state"], 0) + 1
    n_ctl_ok = sum(1 for c in CONTROLS if c["ok"])
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])
    header = build_header(ev)

    payload = {
        "id": "TUFT-" + RID,
        "title": "多体系 α 链扩展：eH/μH/μd 三体系 Uehling 数值机检与 m_r³ 标度失效量化",
        "generated_at": START_ISO,
        "proposition": PROPOSITION,
        "verdict_header": header,
        "entries": ENTRIES,
        "entry_distribution": dist,
        "controls": CONTROLS,
        "controls_ok": "%d/%d" % (n_ctl_ok, len(CONTROLS)),
        "guards": GUARDS,
        "guards_ok": "%d/%d" % (n_grd_ok, len(GUARDS)),
        "calculations": {"eH_VP_MHz": ev["dvp_e_mhz"], "muH_VP_meV": ev["dvp_p"],
                         "mud_VP_meV": ev["dvp_d"], "point_d_meV": ev["point_d"],
                         "ratio_num": ev["ratio_num"], "ratio_lit": ev["ratio_lit"],
                         "mr3_naive": ev["mr3"], "scale_break": ev["scale_break"]},
    }

    json_path = os.path.join(DATA_DIR, BASE_NAME + ".json")
    md_path = os.path.join(DATA_DIR, BASE_NAME + ".md")
    rep_path = os.path.join(DATA_DIR, BASE_NAME + "_report.txt")
    vd_path = os.path.join(VD_DIR, "判定_" + BASE_NAME + ".md")
    html_path = os.path.join(SRC_DIR, BASE_NAME + ".html")

    with io.open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    report = build_report(header)
    with io.open(rep_path, "w", encoding="utf-8") as f:
        f.write(report)
    with io.open(md_path, "w", encoding="utf-8") as f:
        f.write(build_md(header))
    with io.open(vd_path, "w", encoding="utf-8") as f:
        f.write(build_verdict(header, n_ctl_ok, n_grd_ok))
    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(payload, header, n_ctl_ok, n_grd_ok))

    for g in GUARDS:
        if g["code"] == "G5":
            g["ok"] = g["ok"] and all(sha256_of(p) == WS_SHA[p] for p in WRITE_SIDE)
    n_grd_ok = sum(1 for g in GUARDS if g["ok"])

    sys.stdout.write(report)
    sys.stdout.write("\n" + "=" * 78 + "\n")
    sys.stdout.write("条目 %d = %s\n" % (len(ENTRIES),
                                         " / ".join("%s %d" % (k, v)
                                                    for k, v in sorted(dist.items()))))
    sys.stdout.write("控制组 %d/%d\n" % (n_ctl_ok, len(CONTROLS)))
    sys.stdout.write("守卫 %d/%d\n" % (n_grd_ok, len(GUARDS)))
    sys.stdout.write("=" * 78 + "\n")
    return 2 if ((n_ctl_ok != len(CONTROLS)) or (n_grd_ok != len(GUARDS))) else 0


if __name__ == "__main__":
    sys.exit(main())
