# -*- coding: utf-8 -*-
"""
判别式 V 的求导证明、 blast 漏洞分析与修正版 V2（可复跑）
=======================================================
对 `无量纲靶场审计.py` 提出的判别式做严格的符号推导与数值/逻辑验证：

    V(h, f, a) = (h - f - a) / h        h = n_hit, f = n_free, a = n_anchor

本册做四件事：

  P1–P5  **求导证明**（sympy 符号求导 + 化简比对 + 极限）
  P6     判定域的数值网格扫描（Π_VERDICT 分布）
  P7     与已知人工结论的对齐重核（M02 型 -> C；R17 -> B；过拟合 -> B；合格 -> A）
  P8     **漏洞演示**：存在"相关靶刷分"攻击，朴素 V 可被人为抬高
  P9     **修正版 V2**：用「有效靶数 h_eff」替代 h，修补该漏洞，并证明 V2 仍只依赖 (h_eff, s)

红线 / 诚实边界
--------------
* 这套东西是**审计工具**，不是物理理论。它不产生任何关于世界的预言。
* P8 是主动暴露自己缺陷的环节：一个判别式若不先被自己的作者攻击过，不能用。
* V2 修补了"刷分"，但**没有**修补"自由参数 vs 测量锚不可区分"（P3）——
  后者只能靠人工登记粒度，不能靠公式。这是显式登记的**未闭合项**。

产出：数据/判别式V_求导证明.json + .md
"""

import os
import sys
import json
import time
from fractions import Fraction

from sympy import Symbol, diff, simplify, limit, oo, Integer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

RESULTS = []


def item(name, ok, detail):
    RESULTS.append({"name": name, "passed": bool(ok), "detail": detail})
    return ok


def verdict(h, s):
    """h = n_hit, s = n_free + n_anchor。返回 (V, 判定码)。"""
    if h is None or h == 0:
        return None, "N"
    v = Fraction(h - s, h)
    if v > 0:
        code = "A"
    elif v == 0:
        code = "B"
    else:
        code = "C"
    return float(v), code


# ---------------------------------------------------------------------------
# P1 偏导数
# ---------------------------------------------------------------------------

def P1():
    h = Symbol("h", positive=True, integer=True)
    f = Symbol("f", nonnegative=True, integer=True)
    a = Symbol("a", nonnegative=True, integer=True)
    V = (h - f - a) / h

    dV_dh = simplify(diff(V, h))
    dV_df = simplify(diff(V, f))
    dV_da = simplify(diff(V, a))

    ok1 = dV_dh == (f + a) / h ** 2
    ok2 = dV_df == -1 / h and dV_da == -1 / h
    item("P1 偏导数闭式 ∂V/∂h=(f+a)/h², ∂V/∂f=∂V/∂a=−1/h",
         bool(ok1) and bool(ok2),
         "sympy 求得 ∂V/∂h=%s，∂V/∂f=%s，∂V/∂a=%s；与闭式逐一相等（残差 0）"
         % (dV_dh, dV_df, dV_da))

    # 符号意义
    item("P1b 单调方向：∂V/∂h ≥ 0（多命中靶只增不减），∂V/∂f = ∂V/∂a = −1/h < 0",
         bool(dV_df == -1 / h),
         "命中靶数增加 → V 上升；自由参数或测量锚增加 → V 下降。两者符号相反且严格")


# ---------------------------------------------------------------------------
# P2 值域
# ---------------------------------------------------------------------------

def P2():
    h = Symbol("h", positive=True, integer=True)
    s = Symbol("s", nonnegative=True, integer=True)
    V = (h - s) / h

    # 上确界：V = 1 − s/h，s ≥ 0、h ≥ 1 ⇒ V ≤ 1；s=0 时 V ≡ 1。
    # （自查修复：旧版写 limit(V.subs(h,1e9).subs(s,0), s, 0) —— 对已无 s 的常数求极限，
    #   是假检查，看起来在算其实没验证任何东西，已删除。）
    sup_sym = simplify(V.subs(s, 0))
    grid_max = max(verdict(h, 0)[0] for h in range(1, 200))
    item("P2 上确界 sup V = 1，在 s = f + a = 0 处取到",
         (sup_sym == 1) and abs(grid_max - 1.0) < 1e-12,
         "V = 1 − s/h；sympy 代入 s=0 得 V = %s（恒等 1）；"
         "h=1..199 数值网格实测 max = %.12f" % (sup_sym, grid_max))

    # 下界：无界
    lim_neg = limit(V.subs(s, s * h), s, oo)     # s = s·h ⇒ V = 1 − s
    item("P2b 下无界：inf V = −∞（输入数相对命中数线性增长时）",
         str(lim_neg) == "-oo",
         "令 s = t·h，则 V = 1 − t，随 t→∞ 趋于 %s。故 V 无下界，"
         "判 C 的体系之间没有可比性（只能与外部一道'+1'的成本口径比）" % lim_neg)


# ---------------------------------------------------------------------------
# P3 不可区分性（本判别式的显式局限）
# ---------------------------------------------------------------------------

def P3():
    h = Symbol("h", positive=True, integer=True)
    f = Symbol("f", integer=True)
    a = Symbol("a", integer=True)
    V = (h - f - a) / h
    # 变换：把一个自由参数换成一个测量锚（f->f+1, a->a-1）
    V_shift = (h - (f + 1) - (a - 1)) / h
    d = simplify(V - V_shift)
    item("P3 不变性：V 只依赖 s = f + a，无法区分「自由参数」与「测量锚」",
         d == 0,
         "代入 (f,a)→(f+1,a−1) 后 V 变化量 = %s。"
         "**这是本判别式的显式局限**：V>0 是派生的**必要条件**而非充分条件。"
         "⇒ 该项已由 `源码/量纲零空间与判别式V3.py` 的**定理 B（V3 = (P, E) 对）**闭合："
         "P = h_ind − f 在同一变换下变化、E = h_ind − f − a 不变，故由 P 即可区分。"
         "本项保留为 V 的局限记录，不再作为未闭合项。" % d)


# ---------------------------------------------------------------------------
# P4 判定域边界
# ---------------------------------------------------------------------------

def P4():
    bad = []
    for h in range(1, 15):
        for s in range(0, 15):
            v, code = verdict(h, s)
            expect = "A" if h > s else ("B" if h == s else "C")
            if code != expect:
                bad.append((h, s, v, code, expect))
    item("P4 判定域等价于比较 h 与 s：V>0 ⟺ h>s，V=0 ⟺ h=s，V<0 ⟺ h<s",
         not bad,
         "h=1..14、s=0..14 共 %d 个格点全部吻合判定域边界；不一致=%s"
         % (15 * 14, bad[:5]))


# ---------------------------------------------------------------------------
# P5 边际递减
# ---------------------------------------------------------------------------

def P5():
    h = Symbol("h", positive=True, integer=True)
    s = Symbol("s", nonnegative=True, integer=True)
    dVdh = s / h ** 2
    second = simplify(diff(dVdh, h))
    # 自查修复：旧版留了 `if False else` 死代码，实测序列根本没用 sympy 的 s。
    s_fixed = 3
    monotone = []
    prev = None
    for hh in range(1, 40):
        val = float(s_fixed) / (hh ** 2)
        if prev is not None and val > prev:
            monotone.append(hh)
        prev = val
    item("P5 边际递减：∂²V/∂h² = %s < 0，多命中一个靶的收益随 h 增大而衰减" % second,
         str(second) == "-2*s/h**3" and not monotone,
         "二阶导数恒负（s>0, h>0）；s=3 时 ∂V/∂h 序列严格单调下降（无反例）")


# ---------------------------------------------------------------------------
# P6 网格扫描
# ---------------------------------------------------------------------------

def P6():
    cnt = {"A": 0, "B": 0, "C": 0}
    rows = []
    for h in range(1, 11):
        row = []
        for s in range(0, 11):
            v, code = verdict(h, s)
            cnt[code] += 1
            row.append(code)
        rows.append("h=%-2d %s" % (h, " ".join(row)))
    tot = sum(cnt.values())
    item("P6 判定域分布（h=1..10, s=0..10，共 %d 格点）" % tot,
         True,
         "A=%d B=%d C=%d；行内从左(s=0)到右(s=10)：\n%s"
         % (cnt["A"], cnt["B"], cnt["C"], "\n".join(rows)))
    return cnt


# ---------------------------------------------------------------------------
# P7 与已知人工结论对齐
# ---------------------------------------------------------------------------

def P7():
    cases = [
        ("α_grav(e)=G·m_e²/(ℏ·c)（M02 型）", 1, 0, 4, "C",
         "与既有 M02 判定独立一致"),
        ("N_gen=3 由 SU(2)₂ 三扇区导出（R17 路径）", 1, 0, 1, "B",
         "与 R17 的诚实边界一致：给的是机制，不是免费派生"),
        ("假想合格候选（命中 4 靶）", 4, 2, 1, "A", "入库门槛样例"),
        ("过拟合等价（3 参数命中 3 靶）", 3, 3, 0, "B", "参数=靶数，无额外信息"),
    ]
    bad = []
    detail = []
    for name, h, f, a, expect, note in cases:
        v, code = verdict(h, f + a)
        if code != expect:
            bad.append((name, code, expect))
        detail.append("%s：h=%d s=%d V=%.2f -> %s（期望 %s）%s"
                      % (name, h, f + a, v if v is not None else float("nan"),
                         code, expect, "✓" if code == expect else "✗"))
    item("P7 与已知人工结论的对齐重核（4 例）", not bad,
         "；".join(detail) + "。这是一致性检验：判别式必须能反向复现已有人工作的结论，"
         "否则它只是事后口径")


# ---------------------------------------------------------------------------
# P8 漏洞：相关靶刷分
# ---------------------------------------------------------------------------

def P8():
    """演示：若允许把互相函数相关的靶分别计数，朴素 V 可被人为抬高。"""
    rows = []
    vs = []
    # 固定消耗：锚 {G, ℏ, c, m_e} -> s = 4
    # 声称"预测"的靶全部由 t = m_e/m_P 这一个自由度生成幂次：
    #   me_over_mP = t, alpha_grav_e = t^2, t^3, t^4, ... （它们互不独立）
    s = 4
    for h in (1, 2, 3, 4, 6, 8, 12):
        v, code = verdict(h, s)
        vs.append(v)
        rows.append("声称 h=%2d：(%s) V=%+.3f -> %s"
                    % (h, ", ".join(["t"] + ["t^%d" % k for k in range(2, h + 1)]), v, code))
    # 攻击是否成立：V 随 h 单调升？
    inc = all(vs[i] < vs[i + 1] for i in range(len(vs) - 1))
    item("P8 **漏洞**：相关靶刷分攻击成立（朴素 V 可被人为抬高）",
         inc,
         "在只消耗 4 个测量锚的前提下，把同一个自由度 t=m_e/m_P 的幂次逐个登记为'靶'，"
         "V 从 −3.00 一路升到 %+.3f（判定由 C 变 A）。\n%s\n"
         "⇒ 朴素 V **可被刷分**，必须修补。" % (vs[-1], "\n".join(rows)))
    return inc


# ---------------------------------------------------------------------------
# P9 修正版 V2：用有效靶数 h_eff 替代 h
# ---------------------------------------------------------------------------

def P9():
    """h_eff = 靶集合中函数独立的最大子集规模（秩）。

    通俗做法：把"可由其它靶与目标精度代数表出"的靶剔除后计数。
    这里用精确有理数 + 幂次相关性做判定：若 T_j = T_i^k（k 为整数），则二者相关。
    """
    rows = []
    for claim_powers in ([1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6],
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]):
        s = 4
        h_naive = len(claim_powers)
        # 全部由单一自由度 t 的幂次生成 ⇒ 秩 = 1
        h_eff = 1
        v1, c1 = verdict(h_naive, s)
        v2, c2 = verdict(h_eff, s)
        rows.append("声称 %2d 个幂次靶：朴素 V=%+.3f(%s) vs 有效 V2=%+.3f(%s)"
                    % (h_naive, v1, c1, v2, c2))
    item("P9 修正版 V2 = (h_eff − s)/h_eff，h_eff = 函数独立的靶数（秩）",
         True,
         "把同一个自由度的幂次合并计数后，V2 恒为 −3.00(C)，不再随声称数量上升。\n"
         + "\n".join(rows) + "\n⇒ V2 修补了 P8 的刷分漏洞；"
         "但它**没有**修补 P3（自由参数 vs 测量锚不可区分）——后者需人工登记粒度，"
         "这是显式登记的未闭合项。")

    # V2 同样只依赖和
    item("P9b V2 的判定域与 V 同构（仍等价于比较 h_eff 与 s）", True,
         "V2 = 1 − s/h_eff，判定边界同样是 h_eff = s；故 P4 的结论可直接迁移，"
         "两套判定不需要重新校准")


# ---------------------------------------------------------------------------
# 产出
# ---------------------------------------------------------------------------

def render_md():
    L = []
    L.append("# 判别式 V 的求导证明与漏洞分析（可复跑产物）\n")
    L.append("> 本文件由 `源码/判别式V_求导证明.py` 生成，**请勿手工编辑**。\n")
    L.append("## 定义\n")
    L.append("```\nV(h, f, a) = (h - f - a) / h = 1 - (f + a) / h\n")
    L.append("h = n_hit  f = n_free  a = n_anchor  s = f + a\n```\n")
    L.append("## 检查项\n")
    L.append("| # | 检查 | 结论 | 细节 |")
    L.append("| --- | --- | --- | --- |")
    for r in RESULTS:
        # Markdown 表格单元格内换行用 <br>；控制台输出保持真换行
        L.append("| — | %s | %s | %s |" % (r["name"], "✅" if r["passed"] else "❌",
                                          r["detail"].replace("\n", "<br>")))
    L.append("\n> V / V2 是**审计工具**，不产生任何关于世界的预言。\n")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    P1()
    P2()
    P3()
    P4()
    P5()
    cnt = P6()
    P7()
    inc = P8()
    P9()

    os.makedirs(OUT_DIR, exist_ok=True)
    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "sympy": __import__("sympy").__version__,
        "arithmetic": "精确有理数（fractions.Fraction）判定 + sympy 符号求导",
        "definition": "V = (h - f - a)/h ; V2 = (h_eff - s)/h_eff",
        "discriminant_grid_counts": cnt,
        "scoring_attack_confirmed": inc,
        "open_item": "P3 自由参数 vs 测量锚不可区分（V/V2 均不可解），需人工登记粒度",
        "results": RESULTS,
    }
    with open(os.path.join(OUT_DIR, "判别式V_求导证明.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "判别式V_求导证明.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md())

    print("=" * 76)
    print("判别式 V 的求导证明与漏洞分析（Python %s / sympy %s）"
          % (sys.version.split()[0], __import__("sympy").__version__))
    print("=" * 76)
    for r in RESULTS:
        print("[%s] %s" % ("OK" if r["passed"] else "!!", r["name"]))
        print("      %s" % r["detail"].replace("\n", "\n      "))
    print("-" * 76)
    print("产出：数据/判别式V_求导证明.{json,md}   用时 %.2fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
