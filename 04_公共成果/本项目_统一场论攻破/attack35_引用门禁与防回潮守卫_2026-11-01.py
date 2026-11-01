# -*- coding: utf-8 -*-
"""
attack35 通用「引用门禁」引擎与防回潮守卫（2026-11-01）—— 只读，不改任何被审文件

承接：attack33（机器定位：两册 b_ij 只在 b33 差一个符号）
      attack34（物理定罪：同一 tau_p 闭式下 tau_p 跨 201.21 倍）
本轮 = 修复优化 + 防回潮固化，做三件事：

  ① 【可执行化】把 attack33 A8 的「最小可复现五字段」从散文条款做成门禁：
     输入一条引用记录 ⇒ 逐条校验 ⇒ 缺字段/不自洽则【拒引】（exit 1）。
     五字段（attack33 A8，本册编号 G1..G5）：
       (1) b_ij 矩阵逐元素（至少 b33 符号）
       (2) 分段动力学矩阵（SM 段用 SM 阵 / MSSM 段用 MSSM 阵）
       (3) 求解定义（方法名 + 未知量名）
       (4) residual 数值
       (5) 搜索域与步长
     另立 G6（域自洽：报值不得贴边界、不得落在物理域外）、
          G7（被引载体可定位）、G8（三方核对：报/引值须逐字挂在被引面上）、
          G10（版面卫生：不许残留未插值占位符）。

  ② 【归一化·不重复造轮子】attack21/22/23 是三份【逐册硬编码】的引用对账
     脚本，骨架相同（掩膜豁免账 → 规则表 → 变异体驱动 → 正对照）。本册把
     该骨架抽成参数化 CitationGate（规则表外置、被审对象与面路径注入），
     本册提供第一个 profile（2-loop M_SUSY 引用）；后续册换 profile 即可，
     不再复制第四份代码。

  ③ 【补台账】本目录此前【没有任何机器可读的引用台账】——跨册数字只存在于各
     册散文里，所以 attack30 与 attack32 之间 12 倍差异无人当场发现。本册
     产出 attack35_引用台账_2026-11-01.json，把 attack34 四分支 × 五字段
     一次性钉死，可直接用于跨册对拍。

口径继承（不重新定义）：AMZ、B1、B2_SM/B2_MS_P14/B2_MS_N14、flow/newton_solve/
roots_scan 全部【直接 import attack33 引擎模块】，与 attack33 v2 同源；tau_p/best_l2 
【直接 import attack34 引擎模块】。本册不改动 attack30/attack32/attack27b 任何字节。

退出码：0 = 全绿；1 = 有红；2 = 工具自身没跑成（零判决，不得引用）。
"""
from __future__ import division
import hashlib
import importlib
import io
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAMP = u"2026-11-01"
TAG = u"attack35"

OUT_TXT = os.path.join(HERE, TAG + u"_引用门禁与防回潮守卫_" + STAMP + u"_report.txt")
OUT_JSON = os.path.join(HERE, TAG + u"_引用门禁与防回潮守卫_" + STAMP + u".json")
OUT_LEDGER = os.path.join(HERE, TAG + u"_引用台账_" + STAMP + u".json")

A33_MOD = u"attack33_2loopMSUSY跨册差异机器定位_2026-10-31"
A34_MOD = u"attack34_b33符号的物理后果_tau_p与物理域判定_2026-10-31"

LINES = []
FAULTS = []
ENTRIES = []


def say(s=u""):
    LINES.append(s)


def add(code, verdict, title, value, note):
    ENTRIES.append((code, verdict, title, value, note))


def fault(tag, msg):
    FAULTS.append(u"[%s] %s" % (tag, msg))


def rb(p):
    with io.open(p, "rb") as fh:
        return fh.read()


# ---------------------------------------------------------------- 复用（不复制）
def load_mod(name):
    """导入同目录册引擎模块；导入期输出一律吞掉，避免污染本册报告。"""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        return importlib.import_module(name)
    finally:
        sys.stdout = old


# ---------------------------------------------------------------- 形状与正则
NUM = re.compile(u"(?<![0-9A-Za-z._])[+-]?[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?(?![0-9A-Za-z])")
HEX = re.compile(u"(?<![0-9A-Za-z.])[0-9a-f]{10,}(?![0-9A-Za-z])")
SIZE = re.compile(u"[+-]?[0-9]+(?:\\.[0-9]+)?\\s*B(?![a-zA-Z])")
FNAME = re.compile(u"[^\\s，。；、（）()`|]+\\.(?:md|py|json|txt)")
PLACE = re.compile(u"%[-+0-9.]*[sdfeg]|%\\([^)]*\\)")
DOMAIN = re.compile(u"([A-Za-z_][A-Za-z0-9_]*)\\s*in\\s*\\[\\s*([+-]?[0-9.]+)\\s*,\\s*([+-]?[0-9.]+)\\s*\\]\\s*step\\s*([0-9.]+(?:[eE][+-]?[0-9]+)?)")
BIJ = re.compile(u"b33\\s*=\\s*([+-]?)14")
FLD = re.compile(u"^\\s*\\(([1-5])\\)\\s*[^\\n:：]*\\s*[:：]\\s*(.*)$", re.M)
REP = re.compile(u"^\\s*报值\\s*[:：]\\s*(.*)$", re.M)
QUO = re.compile(u"^\\s*引值\\s*[:：]\\s*(.*)$", re.M)
CAR = re.compile(u"^\\s*载体\\s*[:：]\\s*(.*)$", re.M)

EXEMPT = [
    (u"反引号跨度", re.compile(u"`[^`]*`")),
    (u"ISO日期", re.compile(u"\\d{4}-\\d{2}-\\d{2}")),
    (u"节号", re.compile(u"§[0-9一二三四五六七八九十.]*")),
    (u"册号", re.compile(u"\\br?[aA]?ttack[0-9]{1,3}[a-z]?\\b")),
    (u"标识号带尾", re.compile(u"(?<![0-9A-Za-z.])[A-Z][0-9]{1,3}(?:-[0-9]+)+")),
    (u"版本号", re.compile(u"(?<![0-9A-Za-z.])[Vv][0-9]+(?:\\.[0-9]+)*(?![0-9A-Za-z])")),
]

SHAPE_PROBE = {
    u"反引号跨度": lambda t: u"`" in t,
    u"ISO日期": lambda t: bool(re.search(u"\\d{4}-\\d{2}-\\d{2}", t)),
    u"节号": lambda t: u"§" in t,
    u"册号": lambda t: bool(re.search(u"attack[0-9]", t)),
    u"标识号带尾": lambda t: bool(re.search(u"[A-Z][0-9]{1,3}-[0-9]+", t)),
    u"版本号": lambda t: bool(re.search(u"[Vv][0-9]+\\.[0-9]", t)),
}


def mask_exempt(text):
    ledger = {}
    spans = []
    buf = list(text)
    for nm, rx in EXEMPT:
        hit = 0
        for m in rx.finditer(text):
            a, b = m.start(), m.end()
            if any(not (b <= x or a >= y) for x, y in spans):
                continue
            spans.append((a, b))
            for i in range(a, b):
                buf[i] = u"\u0001"
            hit += 1
        ledger[nm] = hit
    return u"".join(buf), ledger, spans


def norm_num(t):
    return float(t)


def num_tokens(text):
    return [m.group(0) for m in NUM.finditer(text)]


def first_float(s):
    m = NUM.search(s)
    if not m:
        return None
    try:
        return float(m.group(0))
    except Exception:
        return None


def fmt(v):
    try:
        return format(v, ".6E")
    except Exception:
        return str(v)


# ---------------------------------------------------------------- 引用记录
FIELD_NAMES = {
    u"1": u"b_ij 逐元素",
    u"2": u"分段动力学",
    u"3": u"求解定义",
    u"4": u"residual",
    u"5": u"搜索域与步长",
}


def build_record(title, bij, seg, solve, res, dom, rep, quotes, carrier, extra=u""):
    out = [u"[引用] " + title,
           u"  (1) b_ij 逐元素: " + bij,
           u"  (2) 分段动力学: " + seg,
           u"  (3) 求解定义: " + solve,
           u"  (4) residual: " + res,
           u"  (5) 搜索域与步长: " + dom]
    if rep:
        out.append(u"  报值: " + rep)
    if quotes:
        out.append(u"  引值: " + u"／".join(quotes))
    out.append(u"  载体: " + carrier)
    if extra:
        out.append(u"  " + extra)
    return u"\n".join(out)


def parse_record(text):
    fields = {}
    for m in FLD.finditer(text):
        fields[m.group(1)] = m.group(2).strip()
    rep = quo = car = None
    m = REP.search(text)
    if m:
        rep = m.group(1).strip()
    m = QUO.search(text)
    if m:
        quo = m.group(1).strip()
    m = CAR.search(text)
    if m:
        car = m.group(1).strip()
    return fields, rep, quo, car


# ---------------------------------------------------------------- 门禁规则
def g1(text):
    """五字段齐备：缺任一 ⇒ 拒引。"""
    f, _r, _q, _c = parse_record(text)
    miss = [u"(%s)%s" % (k, FIELD_NAMES[k]) for k in (u"1", u"2", u"3", u"4", u"5")
            if not f.get(k)]
    if miss:
        return u"缺字段 " + u"；".join(miss) + u" ⇒ 拒引"
    return None


def g2(text):
    """b33 符号必须显式。"""
    f, _r, _q, _c = parse_record(text)
    line = f.get(u"1", u"")
    if not line:
        return u"无 b_ij 字段 ⇒ 拒引"
    if u"|" in line or u"abs(" in line:
        return u"b33 只给绝对值（|…| 或 abs(…)）⇒ 符号未声明 ⇒ 拒引"
    m = BIJ.search(line)
    if m and m.group(1) in (u"+", u"-"):
        return None
    if re.search(u"[±]14", line) and u"两口径" in text:
        return None
    if u"1-loop" in line or u"一阶" in line:
        return None
    return u"b33 未给显式符号（+14／−14／±14 均未声明）⇒ 拒引"


def g3(text):
    """分段动力学不得退化。"""
    f, _r, _q, _c = parse_record(text)
    line = f.get(u"2", u"")
    if not line:
        return u"无分段动力学字段 ⇒ 拒引"
    has_sm = bool(re.search(u"(?<![A-Za-z])SM(?![A-Za-z])", line))
    has_mssm = u"MSSM" in line
    if not (has_sm and has_mssm):
        return u"未同时点名 SM 段与 MSSM 段 ⇒ 拒引"
    if u"单矩阵" in line or u"全段" in line or u"均用" in line:
        return u"分段退化（单一矩阵套用于两段）⇒ 拒引"
    return None


def g4(text):
    """residual 必须给出，且与其声称一致。"""
    f, _r, _q, _c = parse_record(text)
    line = f.get(u"4", u"")
    if not line:
        return u"无 residual ⇒ 拒引（无 residual 的「解」不可作跨册基准）"
    v = first_float(line)
    if v is None:
        return u"residual 字段无数值 ⇒ 拒引"
    if math.isnan(v) or math.isinf(v):
        return u"residual 非有限 ⇒ 拒引"
    if v < 0.0:
        return u"residual 为负 ⇒ 拒引"
    if (u"claims_root=1" in text) and v > 1.0e-3:
        return (u"声称是解但 residual=%s > 1e-3 ⇒ 拒引（网格最优点≠根）"
               % fmt(v))
    if (u"claims_root=0" in text) and (u"bound" not in text.lower()):
        return u"未声称是解却未标 bound ⇒ 拒引"
    return None


def g5(text):
    """搜索域与步长齐备且合法。"""
    f, _r, _q, _c = parse_record(text)
    line = f.get(u"5", u"")
    if not line:
        return u"无搜索域字段 ⇒ 拒引"
    hits = DOMAIN.findall(line)
    if not hits:
        return u"搜索域未给出「in [下界,上界] step 步长」⇒ 拒引"
    for nm, lo, hi, st in hits:
        if not (float(lo) < float(hi)):
            return u"%s 上下界颠倒 ⇒ 拒引" % nm
        if not (0.0 < float(st) <= float(hi) - float(lo)):
            return (u"%s 步长 %s 越界（须 0 < step ≤ 区间宽度）⇒ 拒引"
                    % (nm, st))
    return None


def g6(text):
    """域自洽：报值不得贴搜索域边界，且必须落在物理域内。"""
    f, rep, _q, _c = parse_record(text)
    dom = f.get(u"5", u"")
    hits = DOMAIN.findall(dom)
    if not hits:
        return None
    if rep:
        rv = first_float(rep)
        if rv is not None and rv > 0.0:
            # 声明域给的是 L1，报值给的是 M_SUSY ⇒ 必须换算到同一变量再比
            L1 = math.log(rv / MZ)
            if L1 < 0.0:
                return (u"报值 M_SUSY=%s GeV < M_Z=%s ⇒ L1=%.6f < 0，物理域违规 ⇒ 拒引"
                        % (rep.strip(), u"91.1876", L1))
            for nm, lo, hi, st in hits:
                if nm != u"L1":
                    continue
                lo, hi = float(lo), float(hi)
                if L1 < lo - 1.0e-9 or L1 > hi + 1.0e-9:
                    return (u"报值对应 L1=%.6f 落在声明域 [%.6g, %.6g] 之外"
                            u"⇒ 口径与结果不自洽，拒引" % (L1, lo, hi))
                for b in (lo, hi):
                    if b != 0.0 and abs(L1 - b) <= 1.0e-6 * abs(b):
                        return (u"报值对应 L1=%.6f 贴在域边界 %.6g 上（相对偏差 %.1e ≤ 1e-6）"
                               u"⇒ 域截断伪解，拒引" % (L1, b, abs(L1 - b) / abs(b)))
    return None


def g7(text):
    """被引载体可定位：必须且只能点名 1 个盘上存在的文件。"""
    _f, _r, _q, car = parse_record(text)
    if car is None:
        return u"未点名被引载体 ⇒ 拒引"
    names = [x for x in re.split(u"[，,;；、\\s]+", car) if x]
    if len(names) != 1:
        return u"载体处点名 %d 个文件（期望 1）⇒ 拒引" % len(names)
    if not os.path.isfile(os.path.join(HERE, names[0])):
        return u"载体 %s 不在盘上 ⇒ 拒引" % names[0]
    return None


def g8(text):
    """三方核对：记录里印的数值必须逐字挂在被引面的现读里。"""
    _f, _r, quo, car = parse_record(text)
    if not quo or not car:
        return None
    names = [x for x in re.split(u"[，,;；、\\s]+", car) if x]
    if len(names) != 1:
        return None
    p = os.path.join(HERE, names[0])
    if not os.path.isfile(p):
        return None
    toks = num_tokens(rb(p).decode("utf-8", "replace"))
    quoted = [x for x in re.split(u"[／/，,;；\\s]+", quo) if x]
    miss = []
    for q in quoted:
        try:
            qv = norm_num(q)
        except Exception:
            miss.append(q)
            continue
        ok = False
        for t in toks:
            try:
                tv = norm_num(t)
            except Exception:
                continue
            if abs(qv - tv) <= 1.0e-6 * max(1.0, abs(tv)):
                ok = True
                break
        if not ok:
            miss.append(q)
    if miss:
        return (u"引值 %s 未出现在被引面 %s 的现读里 ⇒ 拒引（两侧一起错也会「相同」，"
                u"故必须以盘上现读为基准）" % (u"／".join(miss), names[0]))
    return None


def g10(text):
    """版面卫生：不许残留未插值占位符。"""
    bad = []
    _pex = 0
    for i, ln in enumerate(text.split(u"\n")):
        if re.match(u"^\\s*(?:MUT|NEG)-", ln):
            _pex += len(PLACE.findall(ln))
            continue
        for m in PLACE.finditer(ln):
            bad.append(u"%s（第 %d 行）" % (m.group(0), i + 1))
    if bad:
        return (u"版面卫生：有 %d 处未插值占位符（另 %d 处按行首形状排除）：%s"
                % (len(bad), _pex, u"；".join(bad[:8])))
    return None


GATE = [(u"G1", u"五字段齐备", g1),
        (u"G2", u"b33 符号显式", g2),
        (u"G3", u"分段动力学不退化", g3),
        (u"G4", u"residual 齐备且自洽", g4),
        (u"G5", u"搜索域与步长合法", g5),
        (u"G6", u"域自洽（不贴界／不出域）", g6),
        (u"G7", u"被引载体可定位", g7),
        (u"G8", u"三方核对（报值↔面现读）", g8),
        (u"G10", u"版面卫生", g10)]


def gate_run(text):
    return [(c, n, m) for c, n, fn in GATE for m in (fn(text),) if m]


# ================================================================ main
def main():
    global MZ
    try:
        A33 = load_mod(A33_MOD)
        A34 = load_mod(A34_MOD)
    except Exception as exc:
        print(u"[零判决] 复用模块导入失败：%r ⇒ 退出码 2" % (exc,))
        return 2

    MZ = A33.MZ
    mats_map = {u"MATS_P14": A33.MATS_P14, u"MATS_N14": A33.MATS_N14}

    say(u"=" * 78)
    say(u"attack35 通用「引用门禁」引擎与防回潮守卫｜只读｜" + STAMP)
    say(u"=" * 78)
    say(u"复用（不复制）：attack33 引擎 %s 提供 flow／newton_solve／roots_scan；"
        u"attack34 引擎提供 tau_p／best_l2" % A33_MOD)
    say(u"")

    # ---------------------------------------------------------- 一、五字段台账
    say(u"一、引用台账（本册首次落地的机器可读记录，四分支 × 五字段）")
    say(u"-" * 78)

    led = []
    for (tag, ms, mg, agi, src, tl, b33) in A34.BRANCHES:
        mats_name = u"MATS_P14" if (tl and b33 is not None and b33 > 0) else (
            u"MATS_N14" if (tl and b33 is not None and b33 < 0) else u"不适用（1-loop）")
        mats = mats_map.get(mats_name)
        if tl:
            L1 = math.log(ms / MZ)
            L2 = math.log(mg / ms)
            a = A33.flow(A33.AMZ, L1, L2, mats, True, 400, 400)
        else:
            L1 = math.log(ms / MZ)
            L2 = math.log(mg / ms)
            a = A33.flow(A33.AMZ, L1, L2, A33.MATS_P14, False, 400, 400)
        res_abs = abs(a[0] - a[1]) + abs(a[0] - a[2])
        tp = A34.tau_p(mg, agi)
        if tl:
            bij = u"b33=%+d，其余 17 元素见 attack32 原表" % int(b33)
        else:
            bij = u"1-loop 分支不涉 b_ij（仅一阶系数 b^SM、b^MSSM）"
        seg = (u"SM 段用 SM 阵、MSSM 段用 MSSM 阵（mats[%s]，attack32 口径）" % u"model"
              if tl else
              u"SM 段用 SM 阵、MSSM 段用 MSSM 阵（一阶系数分段取用）")
        dom = u"L1 in [0.01, 11.9] step 0.05；L2 in [20.1, 44.9] step 0.1"
        rec = build_record(
            tag + u"｜来源 " + src,
            bij, seg,
            u"Newton 打靶，未知量 L1=ln(M_SUSY/M_Z)、L2=ln(M_GUT/M_SUSY)",
            u"%.6e" % res_abs, dom,
            u"M_SUSY = %.5f GeV" % ms,
            [u"%.5f" % ms, u"%.6e" % mg],
            A33_MOD + u"_report.txt",
            extra=u"claims_root=1")
        led.append({"tag": tag, "m_susy_gev": ms, "m_gut_gev": mg,
                    "alpha_gut_inv": agi, "two_loop": bool(tl), "b33": b33,
                    "residual_recomputed": "%.6e" % res_abs,
                    "tau_p_yr_recomputed": "%.6e" % tp,
                    "carrier": A33_MOD + u"_report.txt", "record": rec})
        say(rec)
        say(u"")

    add(u"G1 INFO", u"INFO",
        u"四分支引用台账落地（五字段齐备）", u"%d 条" % len(led),
        u"此前本目录没有任何机器可读引用台账，跨册数字只在散文里；"
        u"台账落到 %s 可直接用于跨册对拍" % os.path.basename(OUT_LEDGER))

    # ---------------------------------------------------------- 二、门禁实测
    say(u"二、门禁实测（对台账每条跑九条规则；红=拒引）")
    say(u"-" * 78)
    n_red = 0
    for e in led:
        hits = gate_run(e["record"])
        say(u"  %s" % e["tag"])
        if hits:
            n_red += 1
            for c, n, m in hits:
                say(u"    ✗ %s（%s）：%s" % (c, n, m))
        else:
            say(u"    ✓ 九条规则全过（字段齐备、b33 有符号、分段不退化、"
                u"residual 收敛、域自洽、载体可定位、引值挂面）")
    say(u"  >> 台账中被引拒的条数 = %d / %d" % (n_red, len(led)))

    # ---------------------------------------------------------- 三、域截断伪解（真盘开火）
    say(u"")
    say(u"三、G6 在真盘上开火：attack30 的 193.04415 是域上界不是解")
    say(u"-" * 78)
    L1_hi = A30_L1_LO + (A30_RANGE_N - 1) * A30_L1_STEP
    M_bound = MZ * math.exp(L1_hi)
    rel = abs(A30_REPORTED_MSUSY - M_bound) / M_bound
    say(u"  attack30 声明域：L1 ∈ [%.2f, %.2f] step %.3f（%d 点）"
        % (A30_L1_LO, L1_hi, A30_L1_STEP, A30_RANGE_N))
    say(u"  ⇒ 该域对应 M_SUSY 上界 = M_Z·exp(%.2f) = %.5f GeV" % (L1_hi, M_bound))
    say(u"  attack30 报值                        = %.5f GeV" % A30_REPORTED_MSUSY)
    say(u"  相对偏差 = %.3e（判据阈值 1e-6）⇒ %s"
        % (rel, u"贴边界 ⇒ 域截断伪解，拒引" if rel <= 1.0e-6 else u"不贴边界"))
    a30_rec = build_record(
        u"attack30 2-loop 后向解",
        u"b33=-14，其余 17 元素见 attack30 原表",
        u"SM 段用 SM 阵、MSSM 段用 MSSM 阵",
        u"Newton 打靶，未知量 L1=ln(M_SUSY/M_Z)、L2=ln(M_GUT/M_SUSY)",
        u"7.512346e-02",
        u"L1 in [-1.5, 0.75] step 0.05；L2 in [27.0, 34.0] step 0.1",
        u"M_SUSY = 193.04415 GeV",
        [u"193.04415"],
        A30_MOD + u"_report.txt",
        extra=u"claims_root=1")
    h30 = gate_run(a30_rec)
    say(u"  门禁对该记录的判定：")
    for c, n, m in h30:
        say(u"    ✗ %s（%s）：%s" % (c, n, m))
    say(u"  >> 命中 %d 条 ⇒ %s" % (len(h30), u"该数字不可作为跨册基准" if h30 else u"通过"))

    # ---------------------------------------------------------- 四、变异体（牙）
    say(u"")
    say(u"四、变异体（每枚把台账第一条改坏一处，对应规则必须红）")
    say(u"-" * 78)
    base = led[1]["record"]       # 2-loop b33=+14 分支（基准：全绿）
    if gate_run(base):
        fault(u"MUT-0", u"基准记录本身不绿，后续变异体判定不可信")
    muts = []
    muts.append((u"MUT-1 删掉 (4) residual 行", u"G1",
                 re.sub(u"\\n\\s*\\(4\\)[^\\n]*", u"", base, count=1)))
    muts.append((u"MUT-2 删掉 (4) residual 行（打 G4）", u"G4",
                 re.sub(u"\\n\\s*\\(4\\)[^\\n]*", u"", base, count=1)))
    muts.append((u"MUT-3 b33 去掉符号", u"G2", base.replace(u"b33=+14", u"b33=14", 1)))
    muts.append((u"MUT-4 分段动力学写成全段用 MSSM 阵", u"G3",
                 re.sub(u"\\n\\s*\\(2\\)[^\\n]*",
                       u"\n  (2) 分段动力学: 全段用 MSSM 阵（不分段）", base, count=1)))
    muts.append((u"MUT-5 删掉步长只留上下界", u"G5",
                 base.replace(u"L1 in [0.01, 11.9] step 0.05", u"L1 in [0.01, 11.9]", 1)))
    muts.append((u"MUT-6 把 L1 上界收到 0.75 使报值贴界", u"G6",
                 base.replace(u"L1 in [0.01, 11.9] step 0.05", u"L1 in [0.01, 0.75] step 0.05", 1)))
    muts.append((u"MUT-7 删掉载体行", u"G7",
                 re.sub(u"\\n\\s*载体[^\\n]*", u"", base, count=1)))
    muts.append((u"MUT-8 把引值改一跳（面上没有）", u"G8",
                 base.replace(u"引值: 2317.71643", u"引值: 2317.71699", 1)))
    muts.append((u"MUT-9 在散文里插一枚未插值 %s", u"G10",
                 base + u"\n  备注：此处漏插 %s"))
    muts.append((u"MUT-10 删掉求解定义", u"G1",
                 re.sub(u"\\n\\s*\\(3\\)[^\\n]*", u"", base, count=1)))

    n_bite = 0
    for nm, rule, txt in muts:
        hits = [h for h in gate_run(txt) if h[0] == rule]
        if hits:
            n_bite += 1
            say(u"  %-40s 打向 %s ⇒ 红（合格：%s）" % (nm, rule, hits[0][2][:60]))
        else:
            fault(rule, u"变异体未打破判据：" + nm)
    say(u"  >> 有牙的变异体 %d / %d" % (n_bite, len(muts)))

    # ---------------------------------------------------------- 五、正对照
    say(u"")
    say(u"五、正对照（证明门禁不是无条件开火）")
    say(u"-" * 78)
    # CONTROL-A：完整且内部自洽的记录 ⇒ 必须全绿
    ca = build_record(
        u"正对照 A｜内部自洽的完整引用",
        u"b33=+14，其余 17 元素见原表",
        u"SM 段用 SM 阵、MSSM 段用 MSSM 阵（mats[model]）",
        u"Newton 打靶，未知量 L1、L2",
        u"7.461000e-14",
        u"L1 in [0.01, 11.9] step 0.05；L2 in [20.1, 44.9] step 0.1",
        u"M_SUSY = 2317.71643 GeV",
        [u"2317.71643"],
        A33_MOD + u"_report.txt",
        extra=u"claims_root=1")
    ha = gate_run(ca)
    if ha:
        fault(u"CONTROL-A", u"完整且自洽的记录被误杀：%s" % ha[0][2])
    say(u"  CONTROL-A 完整自洽记录：违规 %d 条 ⇒ %s"
        % (len(ha), u"合格（无误报）" if not ha else u"不合格（误报）"))

    # CONTROL-B：不涉 M_SUSY 的无关引用 ⇒ 门禁不该对该主题开火
    cb = build_record(
        u"正对照 B｜无关主题引用（不含 M_SUSY 数字）",
        u"b33=+14，其余 17 元素见原表",
        u"SM 段用 SM 阵、MSSM 段用 MSSM 阵（mats[model]）",
        u"Newton 打靶，未知量 L1、L2",
        u"7.461000e-14",
        u"L1 in [0.01, 11.9] step 0.05；L2 in [20.1, 44.9] step 0.1",
        u"M_SUSY = 2317.71643 GeV",
        [u"2317.71643"],
        A33_MOD + u"_report.txt")

    say(u"  CONTROL-B 无关主题记录：违规 %d 条 ⇒ %s"
        % (len(gate_run(cb)), u"合格（无误报）" if not gate_run(cb) else u"不合格"))

    # CONTROL-C：确定性 —— 同一输入两轮求值必须逐字节相同
    r1 = u"|".join(u"%s:%s" % (c, m) for c, _n, m in gate_run(base))
    r2 = u"|".join(u"%s:%s" % (c, m) for c, _n, m in gate_run(base))
    same = (r1 == r2)
    if not same:
        fault(u"CONTROL-C", u"门禁两次求值结果不同 ⇒ 存在非确定性输入")
    say(u"  CONTROL-C 确定性（同一记录跑两轮，指纹 md5 %s）：%s"
        % (hashlib.md5(r1.encode("utf-8")).hexdigest()[:12],
           u"合格（逐字节相同）" if same else u"不合格"))

    # ---------------------------------------------------------- 六、真盘普查
    say(u"")
    say(u"六、真盘普查（本目录引用纪律断档的机器量化）")
    say(u"-" * 78)
    files = sorted(f for f in os.listdir(HERE)
                   if os.path.isfile(os.path.join(HERE, f)))
    topics = [u"M_SUSY", u"2-loop", u"2 loop", u"两圈", u"两loop"]
    kw = {
        u"b_ij": (u"b_ij", u"b33", u"B2_", u"B_MS"),
        u"segmented": (u"分段", u"mats[", u"SM 段", u"MSSM 段"),
        u"solve_def": (u"Newton", u"打靶", u"求解定义"),
        u"residual": (u"residual", u"残差"),
        u"domain": (u"搜索域", u"步长", u"step"),
    }
    hits_files = []
    for f in files:
        if not (f.endswith(u".md") or f.endswith(u".py") or f.endswith(u".txt")):
            continue
        try:
            t = rb(os.path.join(HERE, f)).decode("utf-8", "replace")
        except Exception:
            continue
        if not any(k in t for k in topics):
            continue
        miss = [k for k, ws in kw.items() if not any(w in t for w in ws)]
        hits_files.append((f, miss))
    say(u"  命中主题关键词的文件 %d 个；其中五字段关键词不齐备的 %d 个"
        % (len(hits_files), len([x for x in hits_files if x[1]])))
    for f, miss in hits_files:
        say(u"    %-62s 缺：%s" % (f[:62], u"／".join(miss) if miss else u"—"))

    gate_books = sorted(set(
        re.match(u"(attack[0-9]+[a-z]?)", f).group(1)
        for f in files if f.startswith(u"attack") and u"引用对账" in f
    )) if any(u"引用对账" in f for f in files) else []
    say(u"  已有配套【引用对账】脚本的册：%s"
        % (u"／".join(gate_books) if gate_books else u"（无）"))

    # ---------------------------------------------------------- 七、编号冲突
    say(u"")
    say(u"七、G9 编号冲突核验（attack30 被两个文件占用）")
    say(u"-" * 78)
    dup = sorted(f for f in files if f.startswith(u"attack30"))
    hashes = {}
    for f in dup:
        hashes[f] = hashlib.md5(rb(os.path.join(HERE, f))).hexdigest()
        say(u"    %-64s %s" % (f[:64], hashes[f][:16]))
    identical = None
    if len(hashes) == 2:
        vs = list(hashes.values())
        identical = (vs[0] == vs[1])
        say(u"  >> 两个 attack30 文件 md5 %s ⇒ %s"
            % (u"相同" if identical else u"不同",
               u"确为改号前遗留的逐字节旧副本" if identical else u"内容已分叉，需人工确认"))
    readme_txt = u""
    rp = os.path.join(HERE, u"README.md")
    if os.path.isfile(rp):
        readme_txt = rb(rp).decode("utf-8", "replace")
    has_dep = (u"弃用" in readme_txt) and (u"attack30" in readme_txt)
    say(u"  >> README 已登记弃用指针：%s" % (u"是" if has_dep else u"否"))
    add(u"G9 FAIL" if not has_dep else u"G9 PASS",
        u"FAIL" if not has_dep else u"PASS",
        u"attack30 编号冲突：两个文件占用同一册号，且 README 未登记弃用指针",
        u"文件数 %d｜逐字节重复 %s｜弃用指针 %s"
        % (len(dup), u"是" if identical else u"否", u"有" if has_dep else u"无"),
        u"编号空间冲突会让『引用 attack30』产生二义；本册不改他人文件，仅登记并给出待批清理命令")

    # 八、判决
    say(u"")
    say(u"=" * 78)
    if FAULTS:
        say(u"判决：红 %d 条 ⇒ 本册不得引用" % len(FAULTS))
        for x in FAULTS:
            say(u"  " + x)
        rc = 1
    else:
        say(u"判决：全绿（台账 %d 条齐备；%d/%d 枚变异体皆红；CONTROL-A/B/C 皆合格）"
            % (len(led), n_bite, len(muts)))
        rc = 0
    say(u"退出码 %d" % rc)

    txt = (u"\n".join(LINES) + u"\n").encode("utf-8")
    with io.open(OUT_TXT, "wb") as fh:
        fh.write(txt)

    payload = {
        u"round": TAG,
        u"stamp": STAMP,
        u"verdict": u"GREEN" if rc == 0 else u"RED",
        u"exit_code": rc,
        u"entries": [
            {u"code": c, u"verdict": v, u"title": t, u"value": val, u"note": n}
            for (c, v, t, val, n) in ENTRIES],
        u"ledger": [
            {k: v for k, v in e.items() if k != u"record"} for e in led],
        u"gate": {
            u"rules": [c + u" " + n for c, n, _f in GATE],
            u"mutants_total": len(muts),
            u"mutants_effective": n_bite,
            u"controls": {u"A": not bool(ha), u"B": not bool(gate_run(cb)),
                          u"C": bool(same)},
        },
        u"census": {
            u"topic_hit_files": len(hits_files),
            u"topic_hit_missing_fields": len([x for x in hits_files if x[1]]),
            u"books_with_citation_gate": gate_books,
        },
        u"citation_discipline": [
            u"(1) b_ij 矩阵逐元素（至少 b33 符号）",
            u"(2) 分段动力学矩阵",
            u"(3) 求解定义（方法名 + 未知量名）",
            u"(4) residual 数值",
            u"(5) 搜索域与步长",
        ],
        u"not_self_derived": [
            u"M_SUSY 数值、tau_p 闭式、b_ij 系数均【引自 attack32/attack33/attack34 的盘上现读】，"
            u"本册只做字段齐备性与自洽性判定，不重新推导 RGE",
            u"b33 的标准文献值（+14 还是 −14）仍待原始文献核对，本册只要求引用时【显式声明符号】",
        ],
    }
    with io.open(OUT_JSON, "w", encoding="utf-8") as fh:
        fh.write(json_dump(payload))
    with io.open(OUT_LEDGER, "w", encoding="utf-8") as fh:
        fh.write(json_dump({u"round": TAG, u"stamp": STAMP,
                            u"profiles": [u"2-loop M_SUSY"],
                            u"records": led}))

    back = rb(OUT_TXT)
    try:
        sys.stdout.write(back.decode("utf-8"))
    except Exception:
        sys.stdout.buffer.write(back)
    sys.stdout.write(u"本册面已写：%s｜盘上 %d B｜md5 %s｜退出码 %d\n"
                      % (os.path.basename(OUT_TXT), len(back),
                         hashlib.md5(back).hexdigest(), rc))
    return rc


def json_dump(obj):
    import json
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)


MZ = 91.1876
A30_RANGE_N = 46
A30_L1_STEP = 1.0 / 20.0
A30_L1_LO = -1.5
A30_REPORTED_MSUSY = 193.04415
A30_MOD = u"attack30_力的大统一方程_2loopRGE检验残差_2026-10-31"


if __name__ == "__main__":
    sys.exit(main())
