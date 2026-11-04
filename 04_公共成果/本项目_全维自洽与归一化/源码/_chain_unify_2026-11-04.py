# -*- coding: utf-8 -*-
"""统一力方程攻坚链（G0–G5 六道门禁）—— 可执行机核
配套整理册：整理_统一力方程攻坚算法链_突破口总表与六阶段门禁_2026-11-04.md
不新增 RID。纯标准库（Fraction，无 numpy）。只做「可算判决」，不产新物理。

设计原则
  1. 每道门的 kind 由读数驱动，禁写死；
  2. 每道门必须**两侧都测**（正例给 OK、负例给 NO），否则该门判别力未验证；
  3. 回测用历史卷（V56 / V58 / V59）的**原始结构输入**，不喂历史判决；
  4. 负对照必须改「真正敏感的方向」，并报「读数与基线是否相同」。
"""
import io
import os
import json
import itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
TITLE = "_chain_unify_2026-11-04"

OUT = []          # [(id, kind, exp, act, note)]


def add(rid, kind, exp, act, note):
    OUT.append(dict(id=rid, kind=kind, exp=str(exp), act=str(act), note=note))


# ============================================================ G0 判别力门
def gate0_identity(f, gym, nlo=1, nhi=200):
    """判「该关系是否是恒等式」：对 N 全域数值相等 ⇒ 判别力 0（候选恒等）。
    注意：数值全等只是**必要**条件，最终定性须给符号论证；本门输出 kind=IDENTITY 并注明。"""
    bad = [n for n in range(nlo, nhi + 1) if f(n) != gym(n)]
    return (len(bad) == 0), bad


# ============================================================ G1 结构门（反常能否平方/抵消）
def gate1_square(c):
    """½(a·x² + b·T + c·p₁)² 能否等于给定 8 形式。
    c = dict(x4=..., x2T=..., x2p1=..., T2=..., p1sq=..., Tp1=...)
    精确判据（无开方）：
      x4:a²/2=A, x2T:ab=B, x2p1:ac=C, T2:b²/2=D, p1sq:c²/2=E, Tp1:bc=G
      ⇒ 必要条件 B²=4AD, C²=4AE, G²=4DE, BC=2AG
    """
    A = F(c.get("x4", 0)); B = F(c.get("x2T", 0)); C = F(c.get("x2p1", 0))
    D = F(c.get("T2", 0)); E = F(c.get("p1sq", 0)); G = F(c.get("Tp1", 0))
    fails = []
    if B * B != 4 * A * D:
        fails.append("x²T 块：B²=%s ≠ 4AD=%s" % (B * B, 4 * A * D))
    if C * C != 4 * A * E:
        fails.append("x²p₁ 块：C²=%s ≠ 4AE=%s" % (C * C, 4 * A * E))
    if G * G != 4 * D * E:
        fails.append("Tp₁ 块：G²=%s ≠ 4DE=%s" % (G * G, 4 * D * E))
    if B * C != 2 * A * G:
        fails.append("符号块：BC=%s ≠ 2AG=%s" % (B * C, 2 * A * G))
    return (len(fails) == 0), fails


def gate1_anomaly(qp, qm):
    """两个 16 的局域反常是否抵消：三项同时为零 ⟺ q₊² = q₋²"""
    c = {
        "x4": F(2, 3) * (qp ** 4 - qm ** 4),
        "x2T": F(1, 2) * (qp ** 2 - qm ** 2),
        "x2p1": F(-1, 3) * (qp ** 2 - qm ** 2),
    }
    cancelled = (c["x4"] == 0 and c["x2T"] == 0 and c["x2p1"] == 0)
    return cancelled, c


# ============================================================ G2 谱门（族数奇偶与可达性）
def gate2_spectrum(pairs, target=3):
    """pairs = [(s_i, q_i)]（q 可为负），返回 (Σ s q², 可达 n 集合)。
    定理：Σ s q² = 0 ⇒ n = Σ s q 恒偶 ⇒ 偶数 target 可达、奇数 target 不可达。"""
    sq = sum(s * q * q for s, q in pairs)
    ns = set()
    for e in itertools.product([1, -1], repeat=len(pairs)):
        qq = [ei * q for ei, (s, q) in zip(e, pairs)]
        if sum(s * x * x for s, x in zip([p[0] for p in pairs], qq)) != sq:
            continue
        ns.add(sum(s * x for s, x in zip([p[0] for p in pairs], qq)))
    return sq, ns, (target in ns)


# ============================================================ G3 禁戒门（角动量）
def gate3_forbidden(qf, qH, N):
    """j_H,min − 2j_f（以整数单位）；返回 (间距, 是否禁戒)"""
    jf = F(qf) * F(N - 1, 2)          # 只在 qf=1 的规范下写成 (Q−1)/2
    Q = F(qf) * F(N)
    jHmin = abs(F(qH)) * F(N, 2)
    gap = jHmin - 2 * jf
    return gap, (gap > 0)


# ============================================================ G4 质量门（等差/无量纲比）
def gate4_mass(m1, m2, m3, tol=F(1, 1000)):
    """r = (m₂−m₁)/(m₃−m₁)；等差 ⟺ r = 1/2（与 a、d、单位无关）"""
    r = (F(m2) - F(m1)) / (F(m3) - F(m1))
    return r, (abs(r - F(1, 2)) <= tol)


# ============================================================ G5 参数账门
def gate5_params(n_shape, n_obs):
    """形状参数 ≤ 可观测比值 − 1 才不是欠定"""
    slack = n_obs - 1 - n_shape
    return slack, (slack >= 0)


# ============================================================ 门禁链
def run(cand):
    """cand = dict(name=..., gates=[...])
    每道门返回 (token, 读数)；遇到第一个 NO 立即停（fail-fast），并记停在哪一门。"""
    log = []
    for g in cand["gates"]:
        tok = g()
        log.append(tok)
        if tok[0] in ("NO", "IDENTITY"):
            return tok[0], tok[1], log
    return "OK", log[-1][1] if log else "", log

# ============================================================ 历史回测（喂原始结构，不喂判决）
def case_square(coef):
    ok, why = gate1_square(coef)
    return ("OK", "可平方（0 处矛盾）") if ok else \
           ("NO", "不可平方；%d 处矛盾：%s" % (len(why), "；".join(why)))


def case_spec(qs, signs, target):
    pairs = list(zip(signs, [F(q) for q in qs]))
    sq, ns, reach = gate2_spectrum(pairs, target=target)
    ns_s = [int(x) for x in sorted(ns)]
    if sq != 0:
        return "NO", "反常未抵消（Σ s q² = %s ⇒ 结构门已挡）" % sq
    return ("OK", "n=%d 可达；可达集 %s" % (target, ns_s)) if reach else \
           ("NO", "n=%d 不可达；可达集 %s（全偶）" % (target, ns_s))


def case_identity():
    """V59 C01：'j_min(s) = q_eff − s'（s=1）与 2j_f = N−1 逐点比较"""
    same, bad = gate0_identity(lambda n: n - 1, lambda n: 2 * ((n - 1) / 2))
    return ("IDENTITY", "N=1..200 全等（%d 处不等）⇒ 恒等重述，判别力 0" % len(bad)) if same else \
           ("OK", "%d 处不等 ⇒ 非恒等" % len(bad))


def case_identity_ok():
    """非恒等对照：j_min = N−3 与 2j_f = N−1 只差常数 2 ⇒ 全不等 ⇒ 非恒等"""
    same, bad = gate0_identity(lambda n: n - 3, lambda n: 2 * ((n - 1) / 2))
    return ("IDENTITY", "全等") if same else ("OK", "%d 处不等 ⇒ 非恒等（该式有内容）" % len(bad))


# ---- 回测：期望值取自各卷判定册；输入是原始结构量
HIST = [
    ("V56（r390·结构门）", lambda: case_square(dict(x4=F(2, 3), x2T=F(1, 2), x2p1=F(-1, 3),
                                                    T2=F(0), p1sq=F(0), Tp1=F(0))), "NO"),
    ("V58（r391·谱门，target=3）", lambda: case_spec([1, -1], [1, -1], 3), "NO"),
    ("V59（判别力门）", case_identity, "IDENTITY"),
]
# ---- 正对照：门的另一侧必须真的能给出 OK，否则该门只会说 NO
POS = [
    ("正对照 A：结构门 / 只留 x⁴ 项",
     lambda: case_square(dict(x4=F(2, 3))), "OK"),
    ("正对照 B：谱门 / 同一 V58 谱，target=2",
     lambda: case_spec([1, -1], [1, -1], 2), "OK"),
    ("正对照 C：判别力门 / j_min=N−3 vs 2j_f=N−1",
     case_identity_ok, "OK"),
]

rows = []
hit = 0
print("=" * 96)
print("历史回测（3 卷：期望值取自各卷判定册，输入只喂原始结构量）")
for name, fn, want in HIST:
    _r = fn()
    got, detail = _r[0], _r[1]
    ok = (got == want)
    hit += 1 if ok else 0
    rows.append((name, want, got, detail, ok))
    print("  [%s] %-28s 期望 %-9s 实得 %-9s %s" % ("HIT" if ok else "MISS", name, want, got, detail[:76]))
print("  回测命中 %d/%d" % (hit, len(rows)))

pos_rows = []
pos_ok = 0
print("=" * 96)
print("正对照（判别力另一侧：必须给 OK，否则该门恒 NO ⇒ 判别力 0）")
for name, fn, want in POS:
    _r = fn()
    got, detail = _r[0], _r[1]
    ok = (got == want)
    pos_ok += 1 if ok else 0
    pos_rows.append((name, want, got, detail, ok))
    print("  [%s] %-38s 期望 %-4s 实得 %-4s %s" % ("HIT" if ok else "MISS", name, want, got, detail[:60]))
print("  正对照命中 %d/%d" % (pos_ok, len(pos_rows)))

# ---- 负对照 1：谱门的真正敏感方向（破坏 q₊² = q₋²）
sq_base = gate2_spectrum([(1, F(1)), (-1, F(-1))], target=3)[0]
sq_nc = gate2_spectrum([(1, F(1)), (-1, F(-3, 2))], target=3)[0]
print("=" * 96)
print("负对照 1（谱门敏感方向）：q₋ 由 −1 改成 −3/2，破坏反常抵消前提")
print("  基线 Σ s q² = %s；负控 Σ s q² = %s ⇒ %s"
      % (sq_base, sq_nc, "读数已改变（判别力成立）" if sq_nc != sq_base else "读数相同 ⇒ 该方向不敏感，负控无效"))

# ---- 负对照 2：结构门的真正敏感方向（删掉两个混合项）
ok_base, _ = gate1_square(dict(x4=F(2, 3), x2T=F(1, 2), x2p1=F(-1, 3), T2=F(0), p1sq=F(0), Tp1=F(0)))
ok_nc2, _ = gate1_square(dict(x4=F(2, 3), x2T=F(0), x2p1=F(0), T2=F(0), p1sq=F(0), Tp1=F(0)))
print("负对照 2（结构门敏感方向）：删去 x²T、x²p₁ 两个混合项")
print("  基线可平方 = %s；负控可平方 = %s ⇒ %s"
      % (ok_base, ok_nc2, "已翻面（判别力成立）" if ok_base != ok_nc2 else "未翻面 ⇒ 该门恒 NO，无效"))

# ---- 记入 OUT
add("H1", "PASS" if hit == len(HIST) else "FAIL", "3/3 命中",
    "%d/%d（V56 结构门 / V58 谱门 / V59 判别力门）" % (hit, len(HIST)),
    "★输入只喂原始结构量（I₈ 系数、电荷、表达式），不喂历史判决 ⇒ 这是重算不是复读")
add("H2", "PASS" if pos_ok == len(POS) else "FAIL", "3/3 命中",
    "%d/%d（结构门只留 x⁴ / 谱门 target=2 / 判别力门 N−3）" % (pos_ok, len(POS)),
    "★★三道门的 OK 分支都实测到了 ⇒ 不是三个恒 NO 的门")
add("N1", "PASS" if sq_nc != sq_base else "FAIL", "读数改变",
    "基线 Σ s q² = %s → 负控 %s" % (sq_base, sq_nc),
    "★★负控落在真正敏感方向：改 q₋ 直接破坏 q₊²=q₋²，Σ s q² 立刻非零")
add("N2", "PASS" if ok_base != ok_nc2 else "FAIL", "已翻面",
    "基线可平方 = %s → 负控 %s" % (ok_base, ok_nc2),
    "★★删去两混合项后只剩 ½α²x⁴ 型纯平方，结构门必须给「可平方」")
add("I1", "INFO", "对 target=3，谱门的 OK 分支**不可达**",
    "V58 谱的可达集 = [−2, 0, 2]；把 q 翻遍符号仍全偶",
    "★★★这不是门失效，而是主定理的直接后果：Σ s q² = 0 ⇒ n ≡ Σ s Q² ≡ 0 (mod 2)。"
    "所以对「三代」这个靶，谱门是**判决**不是**筛选** —— 它的 OK 分支只能拿别的 target 实测（正对照 B）")

payload = dict(date="2026-11-04", title=TITLE, kind="整理册机核（不占 RID）",
               gates=["G0 判别力", "G1 结构", "G2 谱", "G3 禁戒", "G4 质量", "G5 参数账"],
               rows=OUT,
               hist=[dict(name=r[0], want=r[1], got=r[2], detail=r[3]) for r in rows],
               pos=[dict(name=r[0], want=r[1], got=r[2], detail=r[3]) for r in pos_rows])
os.makedirs(DATA, exist_ok=True)
JSN = os.path.join(DATA, TITLE + ".json")
with io.open(JSN, "w", encoding="utf-8", newline="\n") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
print("=" * 96)
print("JSON -> %s (%d B)" % (JSN, os.path.getsize(JSN)))
print("条目 %d；PASS %d；FAIL %d" % (len(OUT), sum(1 for r in OUT if r["kind"] == "PASS"),
                                    sum(1 for r in OUT if r["kind"] == "FAIL")))
