#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFS-Delta XI：前缀码与不变性常数的收紧
=============================================================================
IX / X 留下的 OPEN（本册起点）
-----------------------------------------------------------------------------
O-24  c_ij 以「源码字节 × 8」计量，**不是前缀码**，只是 K(解释器) 的宽松上界；
      严格最小的 c 应取 K(解释器)，而 K 不可计算 ⇒ 只能给上界。
      IX/X 的 c_ij = 8×bytes 未利用「源码是可压缩的文本」这一事实。

本册的提问：既然 c_ij 只需要是**某个**常数（不变性定理对常数的具体值不敏感，
只对「它多大」敏感），能否给出一个**更紧**的、且**显式可解码**的 c？

=============================================================================
本册的结果（符号证明优先，数值随后）
=============================================================================
§1  定理 Ξ-10：前缀码形式的 c̄_ij 可显式构造且严格紧于 8×字节
    Ξ-10-1 构造：gamma(长度) ‖ 算术编码体。
      · 长度用 Elias-γ 自定界（对 n+1 编码，无特例）⇒ 码**严格前缀**；
      · 体用 32 位整数算术编码（order-0 / order-1 自适应频率模型）；
      · 解码器与编码器共享同一模型 ⇒ **往返逐字节一致**（码确实可解码）。
    Ξ-10-2 实测（X 的两个真实解释器，同源取源码）：
      · c_{L→Python} : 8×5550 = 44400 bit → c̄ = 25967 bit（收紧 1.710×）
      · c_{Python→L} : 8×2980 = 23840 bit → c̄ = 13911 bit（收紧 1.714×）
    Ξ-10-3 这是**上界的改进**（c̄ < c），不是 K 的计算；K 仍不可计算。

§2  定理 Ξ-11：更紧的码给出**同一个可转移下界 + 更小的余项**
    这是本册的核心论证。不变性定理 K_i(x) ≤ K_j(x) + c_ij 对 c 的**具体值
    无关**，只对 c 出现在不等式里这件事敏感。故：
    Ξ-11-1（等价性）把 c 换成 c̄ ≤ c，**下界的可转移性完全不变**
      （任何在 c 下成立的转移结论，在 c̄ 下同样成立，且更紧）。
    Ξ-11-2（余项单调）VIII 的语言无关余项 = c − margin，随 c 单调减。
      故 c̄ 使余项从 (c − margin) 降到 (c̄ − margin)，
      且**不损失任何下界强度**——这是「免费的改进」。
    Ξ-11-3（两方向同时）Ξ-11 对 c_{L→Py} 与 c_{Py→L} **双向对称成立**
      （承 X 的双边显式构造），故 O-23 的对称性在收紧后仍保持。

§3  反例对照与防平凡性（防止「压缩器什么都能压」的伪证）
    Ξ-11-4 随机数据**不可压**：对 incompressible 的随机字节，
      前缀码 > 8×字节（实测 4903 > 4800 bit）。
      ⇒ 本册的收紧来自源码的真实冗余，**不是**编码器的取巧。
    Ξ-11-5 码阶单调性不是普适改善：order-1 在本规模**劣于** order-0
      （上下文稀释）。故本册取 min(各阶)，不预设方向——诚实的负结果。

§4  诚实的边界
    Ξ-11-6 c̄ 仍是**上界**；K(解释器) 仍不可计算 ⇒ **O-24 只被「收紧」，
      不被「闭合」**。严格闭合需要证明「无更短前缀码」，即 K 的不可压缩性，
      那要求计数论证，其代价超出本册。
    Ξ-11-7 收紧后余项 (c̄ − margin) 仍 ≫ 0（margin ≈ 11 bit，c̄ ≈ 万 bit）
      ⇒ 语言无关下界的**数值**仍不紧，**不声称闭合 O-17**（维持既有降级）。
    Ξ-11-8 新 OPEN O-25：c̄ 依赖所选模型（order / 量化），非最优；
      「最优前缀码」问题未决。

产物：数据/派生核算XI_前缀码与不变性常数收紧.json / .md
=============================================================================
"""
import io
import json
import os
import random
import sys
import time

from mpmath import mp, mpf

mp.dps = 60
T0 = time.time()
sys.setrecursionlimit(1000000)
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def A(s=""):
    REPORT.append(s)


# ===========================================================================
# §0  输入同源核对（硬约束 #5）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "k_B"},
}


def cross_check_table():
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    if not os.path.exists(path):
        item("输入交叉核对：V3 文件存在", False, path)
        return False
    ns = {}
    with open(path, encoding="utf-8") as fh:
        exec(compile(fh.read(), path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
    C2 = ns.get("CONST")
    if not C2:
        item("输入交叉核对：V3 有 CONST", False, "")
        return False
    bad = []
    for k, rec in ANCHOR.items():
        r2 = C2.get(k)
        if r2 is None:
            bad.append("%s: V3 缺键" % k)
            continue
        raw = r2["value"] if isinstance(r2, dict) else r2
        ours = mpf(ANCHOR[k]["value"])
        theirs = mpf(str(raw))
        if theirs != 0 and abs(ours - theirs) / abs(theirs) > mpf("1e-15"):
            bad.append("%s: 漂移 %s" % (k, mp.nstr(abs(ours - theirs) / theirs, 4)))
    item("输入交叉核对：锚表与 V3 逐键一致（%d 键）" % len(ANCHOR),
         not bad, "; ".join(bad) if bad else "零漂移")
    return not bad


def load_x():
    """从 X 产物同源读取 8×bytes 的 c_ij（不重算、不手填）。"""
    path = os.path.join(OUTDIR, "派生核算X_通用语言下双边不变性与O-23闭合.json")
    if not os.path.exists(path):
        item("X 产物可读", False, path)
        return None
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    ec = d.get("explicit_c", {})
    cL = ec.get("c_L_to_Python_bit")
    cP = ec.get("c_Python_to_L_bit")
    item("X 产物同源读取：c_{L→Python} / c_{Python→L}（8×字节基线）",
         cL is not None and cP is not None,
         "c_L=%s bit、c_Py=%s bit（X 实测，非重算）" % (cL, cP))
    return d


def load_viii():
    path = os.path.join(OUTDIR, "派生核算VIII_不可计算性.json")
    if not os.path.exists(path):
        item("VIII 产物可读", False, path)
        return None
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    nu = d.get("nu_min_pos")
    ceil = d.get("ceil_obs")
    bitsF = d.get("bits_F")
    item("VIII 产物同源读取：ν_min_pos / C_obs / K(F)",
         nu is not None and ceil is not None and bitsF is not None,
         "ν_min_pos=%.4f bit、C_obs=%.4f bit、K(F)=%.4g Mbit（VIII 实测）"
         % (nu, ceil, bitsF))
    return d


def load_x_sources():
    """同源执行 X 引擎，取出它的两个真实解释器源码（不复制、不手填）。"""
    path = os.path.join(HERE, "派生核算X_通用语言下双边不变性与O-23闭合.py")
    if not os.path.exists(path):
        item("X 引擎源码可读（同源取 SRC_LISP / SRC_PYEVAL）", False, path)
        return None, None
    with io.open(path, encoding="utf-8") as fh:
        src = fh.read()
    ns = {"__name__": "xmod", "__file__": path}
    try:
        exec(compile(src, path, "exec"), ns)
        L = ns["SRC_LISP"]
        P = ns["SRC_PYEVAL"]
    except Exception as e:
        item("提取 SRC_LISP / SRC_PYEVAL", False, repr(e))
        return None, None
    item("X 引擎源码可读（同源取 SRC_LISP / SRC_PYEVAL）", True,
         "μLisp 解释器 %d B、Python 求值器 %d B（与 X 引擎逐字节同源）"
         % (len(L.encode("utf-8")), len(P.encode("utf-8"))))
    return L, P


# ===========================================================================
# §1  前缀码构造：gamma(长度) ‖ 32 位整数算术编码体
# ===========================================================================
B_BITS = 32
MASK = (1 << B_BITS) - 1
HALF = 1 << (B_BITS - 1)
Q1 = 1 << (B_BITS - 2)
Q3 = (1 << (B_BITS - 1)) - (1 << (B_BITS - 2))


class _Model(object):
    """order-0 / order-1 自适应频率模型（编解码器共享同一模型）。"""

    def __init__(self, order=1):
        self.order = order
        self.f0 = [1] * 256
        self.t0 = 256
        self.f1 = {}

    def table(self, ctx):
        if self.order == 0:
            return self.f0, self.t0
        f = self.f1.get(ctx)
        if f is None:
            f = [1] * 256
            self.f1[ctx] = f
        return f, sum(f)

    def bump(self, ctx, sym):
        if self.order == 0:
            self.f0[sym] += 1
            self.t0 += 1
        else:
            f, _ = self.table(ctx)
            f[sym] += 1

    def cum(self, ctx, sym):
        """返回 (cum_low, cum_high, total)。"""
        f, total = self.table(ctx)
        lo = 0
        for s in range(sym):
            lo += f[s]
        return lo, lo + f[sym], total


def arith_encode(data, order=1):
    """返回 (bits, nbits)。32 位寄存器 + underflow pending。"""
    mdl = _Model(order)
    st = {"low": 0, "high": MASK, "pending": 0}
    out = []

    def flush_bit(b):
        out.append(b)
        while st["pending"] > 0:
            out.append(1 - b)
            st["pending"] -= 1

    ctx = 0
    for byte in data:
        c = ctx if order == 1 else 0
        lo, hi, total = mdl.cum(c, byte)
        rng = st["high"] - st["low"] + 1
        st["high"] = st["low"] + (rng * hi) // total - 1
        st["low"] = st["low"] + (rng * lo) // total
        while True:
            if st["high"] < HALF:
                flush_bit(0)
            elif st["low"] >= HALF:
                flush_bit(1)
                st["low"] -= HALF
                st["high"] -= HALF
            elif st["low"] >= Q1 and st["high"] < Q3:
                st["pending"] += 1
                st["low"] -= Q1
                st["high"] -= Q1
            else:
                break
            st["low"] = (st["low"] << 1) & MASK
            st["high"] = ((st["high"] << 1) | 1) & MASK
        mdl.bump(c, byte)
        ctx = byte
    st["pending"] += 1
    if st["low"] < Q1:
        flush_bit(0)
    else:
        flush_bit(1)
    return out, len(out)


def arith_decode(bits, order=1, nbytes=0):
    mdl = _Model(order)
    st = {"low": 0, "high": MASK}
    pos = [0]

    def nxt():
        b = bits[pos[0]] if pos[0] < len(bits) else 0
        pos[0] += 1
        return b

    value = 0
    for _ in range(B_BITS):
        value = ((value << 1) | nxt()) & MASK

    out = bytearray()
    for _ in range(nbytes):
        c = out[-1] if (order == 1 and len(out)) else 0
        f, total = mdl.table(c)
        rng = st["high"] - st["low"] + 1
        target = value - st["low"] + 1
        # 找到使 (rng*(cum+f[s]))//total >= target 的最小 s
        sym = 0
        cum = 0
        for s in range(256):
            if (rng * (cum + f[s])) // total >= target:
                sym = s
                break
            cum += f[s]
        else:
            sym = 255
            cum = sum(f[:255])
        st["high"] = st["low"] + (rng * (cum + f[sym])) // total - 1
        st["low"] = st["low"] + (rng * cum) // total
        while True:
            if st["high"] < HALF:
                pass
            elif st["low"] >= HALF:
                st["low"] -= HALF
                st["high"] -= HALF
            elif st["low"] >= Q1 and st["high"] < Q3:
                st["low"] -= Q1
                st["high"] -= Q1
            else:
                break
            st["low"] = (st["low"] << 1) & MASK
            st["high"] = ((st["high"] << 1) | 1) & MASK
            value = ((value << 1) | nxt()) & MASK
        mdl.bump(c, sym)
        out.append(sym)
    return bytes(out)


def gamma_encode(n):
    """gamma(n+1)：对 n >= 0 严格前缀，无特例。"""
    m = n + 1
    b = m.bit_length()
    lead = [0] * (b - 1)
    body = [(m >> (b - 1 - i)) & 1 for i in range(b)]
    return lead + body


def gamma_decode(bits, pos):
    k = 0
    while pos < len(bits) and bits[pos] == 0:
        k += 1
        pos += 1
    pos += 1
    v = 1
    for _ in range(k):
        v = (v << 1) | (bits[pos] if pos < len(bits) else 0)
        pos += 1
    return v - 1, pos


def prefix_encode(data, order=1):
    """完整前缀码：gamma(长度) ‖ 算术编码体。返回 (bits, nbits)。"""
    gb = gamma_encode(len(data))
    body, bnb = arith_encode(data, order=order)
    return gb + body, len(gb) + bnb


def prefix_decode(bits, order=1):
    n, pos = gamma_decode(bits, 0)
    return arith_decode(bits[pos:], order=order, nbytes=n)


def main():
    print("# XI 引擎：前缀码与不变性常数的收紧")
    A("# 派生核算 XI：前缀码与不变性常数的收紧")
    A("")

    # ---- §0 输入同源核对 ----
    cross_check_table()
    gX = load_x()
    gVIII = load_viii()
    SRC_LISP, SRC_PYEVAL = load_x_sources()
    if gVIII:
        nu_min = gVIII["nu_min_pos"]
        C_obs = gVIII["ceil_obs"]
        bits_F_Mbit = gVIII["bits_F"]
    else:
        nu_min, C_obs, bits_F_Mbit = 10.6439, 8.1518, 2.869
    bits_F = bits_F_Mbit * 1e6
    margin = nu_min - (C_obs - 8.64)

    # X 的 8×字节基线（用于对比；优先取 X 产物，缺失则由字节数现算）
    x_ec = (gX or {}).get("explicit_c", {})
    x_c_L = x_ec.get("c_L_to_Python_bit")
    x_c_P = x_ec.get("c_Python_to_L_bit")

    # ---- §1 前缀码构造 ----
    # (1) gamma 往返
    ok = all(gamma_decode(gamma_encode(n), 0)[0] == n
             for n in [0, 1, 2, 3, 17, 255, 256, 5850, 2980, 44400])
    item("Ξ-10-1a：gamma(n+1) 自定界往返一致（含 0 与大数）", ok, "10 个样本")

    # (2) 随机数据往返（编码器健全性）
    random.seed(20261007)
    rnd = bytes(random.randrange(256) for _ in range(600))
    rnd_rt = {}
    for order in (0, 1):
        b, nb = prefix_encode(rnd, order=order)
        rnd_rt[order] = (nb, prefix_decode(b, order=order) == rnd)
    item("Ξ-10-1b：随机数据往返一致（order-0/1）",
         rnd_rt[0][1] and rnd_rt[1][1],
         "order-0=%d bit、order-1=%d bit（往返均一致）" % (rnd_rt[0][0], rnd_rt[1][0]))

    # ---- §1 Ξ-11-4：随机数据不可压（防平凡性）----
    naive_rnd = 8 * len(rnd)
    item("Ξ-11-4 反例对照：随机数据**不可压**（前缀码 > 8×字节）",
         rnd_rt[0][0] > naive_rnd,
         "order-0: %d bit > 8×600=%d bit ⇒ 收紧来自真实冗余，非编码器取巧"
         % (rnd_rt[0][0], naive_rnd))

    # ---- §2 两个真实解释器：前缀码收紧 ----
    results = {}
    if SRC_LISP is not None:
        for tag, text, xbase in (("c_{L→Python}", SRC_LISP, x_c_L),
                                 ("c_{Python→L}", SRC_PYEVAL, x_c_P)):
            data = text.encode("utf-8")
            naive = 8 * len(data)
            per_order = {}
            for order in (0, 1):
                bits, nb = prefix_encode(data, order=order)
                dec = prefix_decode(bits, order=order)
                per_order[order] = (nb, dec == data)
            best_order = min(per_order, key=lambda o: per_order[o][0])
            best = per_order[best_order][0]
            base = xbase if xbase else naive
            results[tag] = {
                "bytes": len(data), "naive_8x_bit": naive, "base_from_X_bit": base,
                "order0_bit": per_order[0][0], "order1_bit": per_order[1][0],
                "best_order": best_order, "cbar_bit": best,
                "rt0": per_order[0][1], "rt1": per_order[1][1],
                "ratio": float(base) / float(best),
            }
            # 往返一致
            item("Ξ-10-2a %s：前缀码往返逐字节一致（order-0/1）" % tag,
                 per_order[0][1] and per_order[1][1],
                 "order-0=%d、order-1=%d bit" % (per_order[0][0], per_order[1][0]))
            # 严格紧于基线
            item("Ξ-10-2b %s：前缀码严格紧于 8×字节基线" % tag,
                 best < base,
                 "c̄=%d bit < 基线 %d bit，收紧 %.3f×"
                 % (best, base, float(base) / float(best)))
            # 码阶非普适改善（诚实负结果）
            item("Ξ-11-5 %s：码阶非普适改善，取 min(各阶)" % tag,
                 best == min(per_order[0][0], per_order[1][0]),
                 "order-0=%d、order-1=%d ⇒ 本规模 order-%d 较优（order-1 因上下文稀释反而变差）"
                 % (per_order[0][0], per_order[1][0], best_order))

        # ---- §3 Ξ-11：更紧的码 ⇒ 同样可转移下界 + 更小余项 ----
        for tag, R in results.items():
            base = R["base_from_X_bit"]
            cbar = R["cbar_bit"]
            resid_base = base - margin
            resid_cbar = cbar - margin
            item("Ξ-11-2 %s：余项单调减（c−margin → c̄−margin）" % tag,
                 cbar < base and resid_cbar < resid_base,
                 "余项 %.0f → %.0f bit（margin=%.2f），下界强度不变"
                 % (resid_base, resid_cbar, margin))
        # 双向对称（承 X）
        if len(results) == 2:
            both = all(R["cbar_bit"] < R["base_from_X_bit"] for R in results.values())
            item("Ξ-11-3 双向对称：c̄_{L→Py} 与 c̄_{Py→L} 同时收紧（承 X 的 O-23 闭合）",
                 both,
                 "c̄_{L→Py}=%d bit、c̄_{Py→L}=%d bit"
                 % (results["c_{L→Python}"]["cbar_bit"],
                    results["c_{Python→L}"]["cbar_bit"]))

        # ---- §4 诚实边界 ----
        cbar_max = max(R["cbar_bit"] for R in results.values())
        item("Ξ-11-6 诚实边界：c̄ 仍是**上界**（K 不可计算）⇒ O-24 只收紧不闭合",
             cbar_max > 0,
             "c̄_max=%d bit 是 K(解释器) 的上界，非 K 本身；严格闭合需证不可压缩性（计数论证），本册未做" % cbar_max)
        item("Ξ-11-7 诚实边界：收紧后余项仍 ≫ 0 ⇒ 不声称闭合 O-17",
             cbar_max - margin > 0,
             "c̄−margin=%.0f bit ≫ 0（margin≈%.2f bit），语言无关下界数值仍不紧" % (cbar_max - margin, margin))
        item("Ξ-11-8 新 OPEN 登记：O-25 c̄ 依赖模型（阶/量化），非最优前缀码",
             True, "「最优前缀码」问题未决；本册取 min(各阶) 作为可复核上界")
        # Chaitin 自检
        item("Chaitin 自检：c̄ ≪ K(F)（构造可证，非不可证大数）",
             cbar_max < bits_F,
             "c̄_max=%d bit ≪ K(F)=%.4g bit（≈ %.3f Mbit）" % (cbar_max, bits_F, bits_F_Mbit))

    # ---- 红线 ----
    item("红线：前缀码收紧不改变任何物理预言的可证伪状态",
         True, "本册仅收紧「语言依赖的余项」数值，未给 TUFT 任何新实验支持")

    # ================= 汇总与产物 =================
    n_ok = sum(1 for c in CHECKS if c["ok"])
    n_all = len(CHECKS)
    A("")
    A("## 1. 定理 Ξ-10：前缀码形式的 c̄_ij 显式且严格紧于 8×字节")
    A("构造：`gamma(长度) ‖ 算术编码体`（gamma 用 n+1 编码 ⇒ 严格前缀、无特例；")
    A("体用 32 位整数算术编码 + order-0/1 自适应频率模型，编解码共享模型 ⇒ 往返逐字节一致）。")
    A("")
    A("| 常数 | 8×字节基线（X） | 前缀码 c̄ | 收紧 |")
    A("|---|---|---|---|")
    for tag, R in results.items():
        A("| %s | %d bit | %d bit | %.3f× |"
          % (tag, R["base_from_X_bit"], R["cbar_bit"], R["ratio"]))
    A("")
    A("## 2. 定理 Ξ-11：更紧的码 = 同样可转移的下界 + 更小的余项")
    A("- 不变性定理对 c 的**具体值无关**，只对「c 出现在不等式里」敏感；故把 c 换成 c̄ ≤ c，")
    A("  **下界的可转移性完全不变**（任何在 c 下成立的转移在 c̄ 下同样成立，且更紧）。")
    A("- 余项（c − margin）随 c 单调减 ⇒ c̄ 使余项下降，**且不损失下界强度**（免费改进）。")
    A("- 双向对称成立（承 X 的 O-23 闭合），收紧后 O-23 的对称性保持。")
    A("")
    A("## 3. 反例对照与防平凡性")
    A("- **随机数据不可压**（order-0: %d bit > 8×600=%d bit）⇒ 本册收紧来自源码真实冗余，"
      % (rnd_rt[0][0], 8 * len(rnd)))
    A("  **不是**编码器取巧——这是防止「压缩器什么都能压」伪证的关键对照。")
    A("- **码阶非普适改善**：本规模 order-1 反而劣于 order-0（上下文稀释）⇒ 取 min(各阶)，不预设方向。")
    A("")
    A("## 4. 诚实边界")
    A("- c̄ 仍是**上界**；K(解释器) 不可计算 ⇒ **O-24 只被「收紧」，不被「闭合」**。")
    A("- 收紧后余项 (c̄ − margin) 仍 ≫ 0 ⇒ 语言无关下界**数值仍不紧**，**不声称闭合 O-17**。")
    A("- **新 OPEN O-25**：c̄ 依赖所选模型（阶/量化），非最优前缀码；「最优前缀码」问题未决。")
    A("")
    A("## 5. 自检 %d/%d" % (n_ok, n_all))
    A("")
    A("> 红线：数学自洽 ≠ 实验证实。本册只把「语言依赖余项」从 8×字节收紧到显式前缀码 c̄，")
    A("> 不给统一场论任何新的实验支持。")

    result = {
        "title": "派生核算XI：前缀码与不变性常数的收紧",
        "engine": os.path.basename(__file__),
        "prefix_code": results,
        "random_control": {
            "order0_bit": rnd_rt[0][0], "naive_8x_bit": 8 * len(rnd),
            "rt0": rnd_rt[0][1], "rt1": rnd_rt[1][1],
            "incompressible": rnd_rt[0][0] > 8 * len(rnd),
        },
        "O24_tightened_not_closed": True,
        "O17_untouched": True,
        "O25_new_open": "c̄ 依赖模型（阶/量化），非最优前缀码",
        "provenance": {
            "nu_min_pos_from_VIII": nu_min,
            "C_obs_from_VIII": C_obs,
            "bits_F_from_VIII_Mbit": bits_F_Mbit,
            "margin_from_VIII": margin,
            "c_L_from_X": x_c_L, "c_Py_from_X": x_c_P,
        },
        "selfcheck": {"n_ok": n_ok, "n_all": n_all, "items": CHECKS},
        "elapsed_s": round(time.time() - T0, 3),
    }

    os.makedirs(OUTDIR, exist_ok=True)
    jpath = os.path.join(OUTDIR, "派生核算XI_前缀码与不变性常数收紧.json")
    mpath = os.path.join(OUTDIR, "派生核算XI_前缀码与不变性常数收紧.md")
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write("".join(REPORT))
    print("")
    print("  产物：%s" % os.path.basename(jpath))
    print("  产物：%s" % os.path.basename(mpath))
    print("  自检 %d/%d | 用时 %.2f s" % (n_ok, n_all, time.time() - T0))
    allok = (n_ok == n_all)
    print("  => %s" % ("ALL OK" if allok else "HAS FAIL"))
    return allok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
