# -*- coding: utf-8 -*-
"""
TUFT 卷二十八补3：分数电荷的 Z6 中心量子化（诚实攻坚）
------------------------------------------------------
目标：正面攻击 H-TUFT 卷二十八 §8.3 / 假设 H6 ——「n_w 整数绕数只能给整数电荷，
      无法产生夸克 e/3」。
方法：(a) 确认朴素整数绕数确实失败；(b) 检验标准模型电荷是否满足 Z6=Z3xZ2 中心
      相容条件 6Y + 2t + 3d == 0 (mod 6)；(c) 给出量子化单位与 Q 的取值带。
红线：数学自洽 != 实验证实；结论为「部分收窄（给定 G）」，外部假设如实标注。

约定 Q = T_3 + Y（R12 约定 a）。t = SU(3) 三试性(3->+1,3bar->-1,1/8->0)；
d = SU(2) 双重态标志(2->1,1->0)。
"""
import sys
import sympy as sp

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P(m):
    _CNT["PASS"] += 1; print("[PASS] " + m)


def F(m):
    _CNT["FAIL"] += 1; print("[FAIL] " + m)


def B(m):
    _CNT["BOUNDARY"] += 1; print("[BOUNDARY] " + m)


def I(m):
    _CNT["INFO"] += 1; print("[INFO] " + m)


print("=" * 78)
print("TUFT 卷二十八补3：分数电荷的 Z6 中心量子化（诚实攻坚）")
print("=" * 78)

# SM 每代费米子 + 希格斯：(名, SU3维, SU2维, t, d, Y, [T3...])
FIELDS = [
    ("Q_L", 3, 2, 1, 1, sp.Rational(1, 6), [sp.Rational(1, 2), sp.Rational(-1, 2)]),
    ("u_R", 3, 1, 1, 0, sp.Rational(2, 3), [sp.Integer(0)]),
    ("d_R", 3, 1, 1, 0, sp.Rational(-1, 3), [sp.Integer(0)]),
    ("L_L", 1, 2, 0, 1, sp.Rational(-1, 2), [sp.Rational(1, 2), sp.Rational(-1, 2)]),
    ("e_R", 1, 1, 0, 0, sp.Integer(-1), [sp.Integer(0)]),
    ("nu_R", 1, 1, 0, 0, sp.Integer(0), [sp.Integer(0)]),
    ("H", 1, 2, 0, 1, sp.Rational(1, 2), [sp.Rational(1, 2), sp.Rational(-1, 2)]),
]

# ------------------------------------------------------------------
print("\n[A] 朴素整数绕数 n_w 能否给出 SM 电荷？")
quark_q = [sp.Rational(2, 3), sp.Rational(-1, 3)]
if any(q.q != 1 for q in quark_q):
    F("夸克电荷 2/3 与 -1/3 非整数；朴素整数绕数 n_w∈Z 只能给整数电荷，"
      "无法给出 e/3 —— 卷二十八 §8.3 的否定成立")
else:
    P("整数绕数可给夸克电荷")

# ------------------------------------------------------------------
print("\n[B] Z6 = Z3(SU3) x Z2(SU2) 中心相容条件： 6Y + 2t + 3d == 0 (mod 6)")
all_ok = True
for name, d3, d2, t, d, Y, T3s in FIELDS:
    z6 = 6 * Y + 2 * t + 3 * d
    ok = int(sp.Integer(z6) % 6) == 0
    all_ok = all_ok and ok
    Qs = [sp.nsimplify(T3 + Y) for T3 in T3s]
    print("   %-4s t=%+d d=%d Y=%-5s 6Y+2t+3d=%-4s (mod6=%d) Q=%s"
          % (name, t, d, str(Y), str(z6), int(sp.Integer(z6) % 6), [str(q) for q in Qs]))
if all_ok:
    P("SM 全部费米子 + 希格斯满足 Z6 相容条件 6Y+2t+3d≡0 (mod 6) "
      " —— 超荷 Y 被 Z6 中心锁定为 (1/6)Z 的相容子集")
else:
    F("存在场不满足 Z6 相容条件")

# ------------------------------------------------------------------
print("\n[C] 量子化单位与取值带")
Yset = sorted(set(f[5] for f in FIELDS))
Qset = set()
for name, d3, d2, t, d, Y, T3s in FIELDS:
    for T3 in T3s:
        Qset.add(sp.nsimplify(T3 + Y))
sixY_int = all(sp.Rational(6 * y).q == 1 for y in Yset)
threeQ_int = all(sp.Rational(3 * q).q == 1 for q in Qset)
print("   Y 取值:", [str(y) for y in Yset])
print("   Q 取值:", sorted([str(q) for q in Qset]))
if sixY_int:
    P("Y ∈ (1/6)Z：超荷量子化单位 = 1/6")
else:
    F("Y 不在 (1/6)Z")
if threeQ_int:
    P("Q ∈ (1/3)Z：电荷量子化单位 = 1/3（夸克 e/3 由此而来）")
else:
    F("Q 不在 (1/3)Z")

# ------------------------------------------------------------------
print("\n[D] 诚实边界（外部假设，不粉饰）")
B("公式 Y + t/3 + d/2 ∈ Z（等价 6Y+2t+3d≡0 mod6）**预设了 G=SU(3)xSU(2)xU(1) 及其 Z6 商**；"
  "规范群来源仍外生（O-GAUGE 未闭合）——本补只把『电荷量子化单位』归因于中心结构，未导出 G")
B("Z6 商（而非 SU(3)xSU(2)xU(1) 本身）是标准模型的实际全局结构，但『为何取此商』仍是外部选择")
B("Z6 相容只锁定 Y 的量子化单位(1/6)，**不锁定具体取值**（1/6 vs 2/3 vs -1/3 …）；"
  "具体分配仍需反常消除 + U(1)_em 未破缺（R10/R11），而那仍依赖外部输入")

# ------------------------------------------------------------------
print("\n[E] 诚实结论")
I("H6（分数电荷）由『❌完全失败』收窄为『⚠️部分解析』：")
I("  负向保持：朴素整数绕数 n_w 确实无法给出 e/3（卷二十八 §8.3 成立）")
I("  正向新增：把绕数替换为 **Z6 中心相容的量子化**（Y+t/3+d/2 ∈ Z），"
  "SM 全部电荷被 Z6=Z3xZ2 中心结构锁定为 Y∈(1/6)Z、Q∈(1/3)Z —— 分数电荷来源=中心量子化")
I("  等价 H-TUFT 表述：有效电荷 = 绕数被色三试性(t/3)与弱二重态(d/2)『扭转』，"
  "故 5 量子数中的 (n_w, n_c, n_s) 须联合满足 Z6 规则，单靠 n_w 不足")
I("  仍未闭合：G 来源(O-GAUGE)、Z6 商选择、具体取值(需反常+U(1)_em)")
print()
print("=" * 78)
print("汇总: PASS = %d  FAIL = %d  BOUNDARY = %d  INFO = %d"
      % (_CNT["PASS"], _CNT["FAIL"], _CNT["BOUNDARY"], _CNT["INFO"]))
print("总判定: 分数电荷的『量子化单位 1/6』可由 Z6 中心结构导出（给定 G）；"
      "朴素绕数模型仍被否定；G 来源与具体取值仍开放")
print("=" * 78)
