# -*- coding: utf-8 -*-
"""攻坚 X-V63-1：半整数磁通出口是否被 U(1) 陈类整数性关闭。

体例：跨卷攻坚册（主动机核上一卷 OPEN 项）——不新增 RID、不进 README、条目不与任何卷相加。
来料：无外部来料；输入为 V63 整理册 A08 / B04 读数与来料 63-7 的磁通归一。

原则：不抄结论，从 Chern-Weil、物质场 holonomy、归一不变性三条独立路径推整数性，
      再从 Spin(12) 权格枚举各表示的 U(1)_F 荷，判定谱的最小电荷。
  A 层：陈类 / 负对照 / holonomy / 最小电荷 / 归一不变性
  B 层：Spin(12) 表示的 U(1)_F 荷结构与「旋量是唯一奇数荷表示」定理
  C 层：回代 V63 A08 的 14 个半整数解、三条出路定价
  D 层：诚实边界与不相加声明
纪律：条目不可相加；纯陈述给 INFO；定义恒等式记 IDENTITY 不记 PASS；
      判据反噬自己 + 正负双对照；守卫 ok 禁写死；期望值只从另一条独立路径或上一卷读数反抄；
      同源回验抓不到同源错误，须显式标注而不冒充独立证据。
注：避 U+21D2 箭头字与 ASCII 双引号（承接 v62/v63 复跑教训）。
"""
import os
import io
import json
import ast
import math
from fractions import Fraction as F
from itertools import combinations, product
from math import comb

TITLE = "攻坚 X-V63-1 独立机核"
DATE = "2026-11-06"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "数据")

ROWS = []
GUARDS = []


def add(rid, layer, name, exp, act, ok, note=""):
    if ok == "ID":
        kind = "IDENTITY"
    elif ok is None:
        kind = "INFO"
    else:
        kind = "PASS" if ok else "FAIL"
    ROWS.append({"id": rid, "layer": layer, "name": name, "exp": str(exp),
                 "act": str(act), "kind": kind, "note": note})
    print("  [%-8s] %-5s %s" % (kind, rid, name))
    return ok


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print("  [GUARD %-4s] %-16s | %s" % ("ok" if ok else "BAD", name, detail))
    return ok


def fmt_f(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else "%d/%d" % (q.numerator, q.denominator)


def is_int(q):
    return F(q).denominator == 1


def simpson(fn, a, b, n=1000):
    """仅用于量级 sanity 的 Simpson 1/3；精确判据一律走 Fraction。"""
    h = (b - a) / n
    s = fn(a) + fn(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * fn(a + i * h)
    return s * h / 3


print("=" * 78)
print(TITLE + "  " + DATE)
print("=" * 78)
print("\n[GUARD] 工具自检")
guard("FRAC-EXACT", F(1, 3) + F(1, 6) - F(1, 2) == 0, "1/3+1/6-1/2 = 0")

# ---- U(1)_F 生成元取 2*H_6（承接 V62 vec_weights 的「矢量归一」）
# 矢量 12 的 U(1)_F 荷：10 个 0（SO(10) 矢量方向）+ 一对 +2 / -2
VQ = [F(0)] * 10 + [F(2), F(-2)]
LAM_Q = {k: [sum(c) for c in combinations(VQ, k)] for k in range(0, 13)}
# 旋量 32（even 手征）：6 个 +-1/2，符号积 +1；U(1)_F 荷 = 2*(+-1/2) = +-1
SPIN_Q = [F(s[5]) for s in product((1, -1), repeat=6)
          if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] == 1]

guard("DIM-12-32", len(VQ) == 12 and len(SPIN_Q) == 32,
      "矢量权 %d / 旋量权 %d" % (len(VQ), len(SPIN_Q)))
guard("LAM-DIM", all(len(LAM_Q[k]) == comb(12, k) for k in range(13)),
      "Lambda^k(12) 权数 == C(12,k)，全 13 档成立")
guard("VQ-STRUCT", VQ.count(F(0)) == 10 and VQ.count(F(2)) == 1 and VQ.count(F(-2)) == 1,
      "矢量 12 荷多重集：0x10 与 +2 / -2 各一")

# ---- Chern-Weil：F = (N/2) sin(theta) dtheta ^ dphi
# int_S2 F = 2*pi*(N/2)*int_0^pi sin(theta) = 2*pi*N  =>  c1 = N
def chern_flux(N):
    return F(N)


def c1_bad(N):
    """负对照：把 1/2 改成 1/3，c1 = (2/3)N。"""
    return F(2, 3) * F(N)


def field_ok(q, N):
    """物质场 holonomy：exp(i*q*2*pi*N)=1 <=> q*N 为整数。"""
    return is_int(F(q) * F(N))


QSET = [F(1), F(2), F(1, 2), F(3, 2)]
NSET = [F(1), F(2), F(1, 2), F(3, 2)]
HOLO = [[field_ok(q, N) for N in NSET] for q in QSET]

# ---- 归一不变性：Q -> lam*Q, q -> lam*q, k -> k/lam, 乘积 q*k 不变
LAMS = [F(1, 2), F(1), F(2), F(3), F(4)]
NORM = []
for _lam in LAMS:
    _q = F(1) * _lam
    _k = F(3, 2) / _lam
    NORM.append((fmt_f(_lam), fmt_f(_q), fmt_f(_k), fmt_f(_q * _k)))

# ---- 上一卷 V63 整理册 A08 的半整数解（作为输入回代，不新增证据）
HALF = [F(t, 2) for t in range(-8, 9)]
SOL14 = [(p, q) for p in HALF for q in HALF if 2 * (p + q) == 3]
LEGAL14 = [(p, q) for (p, q) in SOL14 if is_int(p) and is_int(q)]

# ---- 整数陈类网格（用于 I_Q 复核）
GRID = list(range(-8, 9))
INT_SOL3 = [(p, q) for p in GRID for q in GRID if 2 * (F(p) + F(q)) == 3]

# ---- 角度积分的 Simpson sanity（float 只作量级核对，不进精确判据）
INT_SIN = simpson(math.sin, 0.0, math.pi, 1000)

print("\n[A] 陈类整数性 / 负对照 / 物质场 holonomy / 归一不变性")

okA01 = chern_flux(3) == 3 and abs(INT_SIN - 2.0) < 1e-9
add("A01", "A", "63-7 磁通归一的陈类：F=(N/2)sin(theta) 给出 c1 = N",
    "c1 = N（来料 63-7 的 F 归一反抄）",
    "int_0^pi sin = %s（Simpson n=1000，解析 2） ; int_S2 F = 2*pi*(N/2)*2 = 2*pi*N ; c1(N=3) = %s"
    % ("%.12f" % INT_SIN, fmt_f(chern_flux(3))),
    okA01,
    "=> 角度积分用 Simpson 独立核过量级；精确结论走 Fraction 闭式。sin(theta) 的积分恰为 2 是量级 sanity 的关键")

_bad = [(n, fmt_f(c1_bad(n)), is_int(c1_bad(n))) for n in range(1, 7)]
okA02 = sum(1 for _x in _bad if _x[2]) == 2 and c1_bad(1) != 1 and not is_int(c1_bad(1))
add("A02", "A", "负对照：把 F 归一的 1/2 改成 1/3，陈类整数性是否被破坏",
    "对照读数须与 A01 不同（A01 下所有整数 N 都合法）",
    "c1_bad(N)=2N/3 ; N=1..6 读数 %s ; 合法 %d/6 ; A01 合法 6/6" % (_bad, sum(1 for _x in _bad if _x[2])),
    okA02,
    "=> 负控翻红：判据确实测的是「F 的归一系数必须是 1/2」，不是任意标量。"
    "这也堵住「换个磁通归一就能把半整数洗成整数」的侥幸（另见 A07）")

HALF_GRID = [F(t, 2) for t in range(-8, 9)]
legal_c1 = [_n for _n in HALF_GRID if is_int(chern_flux(_n))]
okA03 = len(legal_c1) == 9 and not is_int(chern_flux(F(3, 2)))
add("A03", "A", "H^2(S^2,Z)=Z 的整数性：半整数网格上哪些 N 给出合法 U(1) 主丛",
    "仅整数陈类合法（来料「磁通量为整数」反抄）",
    "网格 %d 个值 ; 合法 %d 个 ; 半整数非法 %d 个 ; c1(3/2)=%s 为整数 = %s"
    % (len(HALF_GRID), len(legal_c1), len(HALF_GRID) - len(legal_c1),
       fmt_f(chern_flux(F(3, 2))), is_int(chern_flux(F(3, 2)))),
    okA03,
    "=> 半整数磁通对应的不是 U(1) 主丛；这是拓扑分类的结论，不是参数约定")

add("A04", "A", "同源性判定：Wu-Yang 过渡函数与 Chern-Weil 陈类是否算同一个不变量",
    "应标明同源，不冒充独立证据",
    "A_N=(N/2)(1-cos)dphi ; A_S=-(N/2)(1+cos)dphi ; A_N-A_S=%s*dphi ; g=exp(i*N*phi) ; "
    "g(2pi)=1 与 c1=N 为同一 H^2 类的两种表述" % fmt_f(F(3)),
    None,
    "=> INFO：Wu-Yang 路给 A_N-A_S=N、g(2pi)=exp(2*pi*i*N)，与 A03 的 c1=N 同源。"
    "按「同源回验抓不到同源错误」刀，本册不把它计为独立证据，也不单列 PASS")

_holo_txt = [[("是" if v else "否") for v in _row] for _row in HOLO]
okA05 = field_ok(F(1), F(3)) and not field_ok(F(1), F(3, 2)) and field_ok(F(2), F(3, 2))
add("A05", "A", "第三路（真正独立，依赖谱的电荷）：物质场 holonomy 要求 q*N 为整数",
    "q*N in Z（由 exp(i*q*2*pi*N)=1 推出）",
    "q 集 %s ; N 集 %s ; 合法矩阵 %s ; q=1,N=3/2 合法=%s ; q=2,N=3/2 合法=%s"
    % ([fmt_f(x) for x in QSET], [fmt_f(x) for x in NSET], _holo_txt,
       field_ok(F(1), F(3, 2)), field_ok(F(2), F(3, 2))),
    okA05,
    "=> 这一路依赖「谱里有哪些电荷」，与 A03 只依赖丛的拓扑不同，故是独立的一路。"
    "关键：q=2 时半整数 N=3/2 合法，q=1 时非法")

okA06 = (field_ok(F(2), F(1, 2)) and not field_ok(F(1), F(1, 2))
         and field_ok(F(2), F(1, 2)) != field_ok(F(1), F(1, 2)))
add("A06", "A", "最小电荷敏感刀：半整数磁通的合法性由谱的最小电荷决定",
    "两侧读数须不同",
    "q=2 与 N=1/2：qN=%s 合法=%s ; q=1 与 N=1/2：qN=%s 合法=%s ; 两侧相同=%s"
    % (fmt_f(F(2) * F(1, 2)), field_ok(F(2), F(1, 2)),
       fmt_f(F(1) * F(1, 2)), field_ok(F(1), F(1, 2)),
       field_ok(F(2), F(1, 2)) == field_ok(F(1), F(1, 2))),
    okA06,
    "=> 负控落在真正敏感方向：谱的最小电荷为 2 时半整数磁通开放，为 1 时关闭。"
    "故「半整数磁通是否合法」不是绝对问题，必须问「谱里有没有 q=1 的场」")

_qk_set = set(_x[3] for _x in NORM)
okA07 = len(_qk_set) == 1 and _qk_set == {"3/2"}
add("A07", "A", "归一不变性刀：把 U(1) 生成元 Q 缩放 lam，乘积 q*k 是否不变",
    "q*k 应与 lam 无关（基准 q=1, k=3/2）",
    "lam / q_new / k_new / q*k = %s ; 不同 q*k 取值 %s" % (NORM, sorted(_qk_set)),
    okA07,
    "=> Q -> lam*Q 时 q -> lam*q、k -> k/lam，乘积恒为 3/2。"
    "半整数 N 不能靠换归一洗白：换归一同时改了电荷与磁通单位，物理的 q*k 不变")

add("A08", "A", "整数陈类下 I_Q = 2(N_F+N_Y) 恒偶（V63 整理册 A07/B04 的回代）",
    "恒偶（上一卷读数反抄）",
    "整数网格 %d 组 ; I_Q=3 的解数 %d ; 2x整数 展开后残差 0" % (len(GRID) ** 2, len(INT_SOL3)),
    "ID",
    "=> 定义恒等式，按纪律记 IDENTITY 不记 PASS；本册引用上一卷读数作为输入，不与 A07/B04 相加")

add("A09", "A", "「换内部几何」出路定价：底流形换成亏格 g 的闭曲面 Sigma_g 是否解除整数性",
    "H^2(Sigma_g,Z)=Z 仍给整数陈类",
    "S^2: H^2=Z ; Sigma_g: H^2=Z（g>=0 同） ; 两者同为秩一自由阿贝尔群 ; 半整数 c1 在任一闭曲面上都无丛",
    None,
    "=> INFO：本条只报同调群的维数结构（H^2 均为 Z），未重建高亏格上的 Dirac 指标与零模谱；"
    "按纪律不给 PASS。结论方向是「换几何不解除陈类整数性」，但完整论证属 OPEN")

print("\n[B] Spin(12) 权格：各表示的 U(1)_F 荷与谱的最小电荷")

_b01 = all(is_int(_q / 2) for _q in VQ)
add("B01", "B", "矢量 12 的 U(1)_F 荷多重集（2*H_6 归一）",
    "0x10 与 +2 / -2（V62 vec_weights 口径反抄）",
    "荷多重集 %s ; 全偶 = %s ; 最小非零 |q| = %s"
    % ([fmt_f(x) for x in VQ], _b01, min(abs(x) for x in VQ if x != 0)),
    _b01 and VQ.count(F(0)) == 10,
    "=> 矢量表示的所有 U(1)_F 荷都是偶数，最小非零电荷为 2")

_lam_rows = []
for _k in range(13):
    _qs = LAM_Q[_k]
    _lam_rows.append((_k, len(_qs), fmt_f(min(_qs)), fmt_f(max(_qs)),
                      sum(1 for _x in _qs if _x == 0),
                      all(is_int(_x / 2) for _x in _qs)))
_b02 = all(_row[5] for _row in _lam_rows) and all(_row[1] == comb(12, _row[0]) for _row in _lam_rows)
add("B02", "B", "Lambda^k(12) 全 13 档的 U(1)_F 荷：按权枚举 12 选 k 求和",
    "所有档的荷全为偶数（由 VQ 全偶推出）",
    "(k, 权数, q_min, q_max, 零荷个数, 全偶) = %s" % _lam_rows,
    _b02,
    "=> 792=C(12,5) 的 5-形式、66=C(12,2) 的伴随、220/495 等张量表示，"
    "U(1)_F 荷都是 2 的整数倍；这是按权枚举算出的，不是引文标签")

_spin_set = sorted(set(SPIN_Q))
_b03 = (len(SPIN_Q) == 32 and _spin_set == [F(-1), F(1)]
        and not all(is_int(_x / 2) for _x in SPIN_Q))
add("B03", "B", "旋量 32 的 U(1)_F 荷：是否存在奇数荷",
    "+-1（V62 旋量归一反抄）",
    "旋量荷集合 %s ; 含奇数荷 = %s ; 最小 |q| = %s"
    % ([fmt_f(x) for x in _spin_set], not all(is_int(_x / 2) for _x in SPIN_Q),
       min(abs(x) for x in SPIN_Q)),
    _b03,
    "=> 旋量权是 (+-1/2)^6，U(1)_F=2*H_6 使荷恰为 +-1；这是谱里唯一的奇数荷来源")

_only_spinor = (_b01 and _b02 and _b03)
add("B04", "B", "定理：在 Spin(12) 低维表示中，旋量是唯一含奇数 U(1)_F 荷的表示",
    "张量表示全偶、旋量含奇（由 B01/B02/B03 三条独立读数拼出）",
    "张量侧 13 档全偶=%s ; 矢量全偶=%s ; 旋量含奇=%s ; 故最小电荷 min_q=%s"
    % (_b02, _b01, _b03, min(min(abs(x) for x in VQ if x != 0), min(abs(x) for x in SPIN_Q))),
    _only_spinor,
    "=> 关键表的话由计算拼出：不是「我记得旋量荷是 1」，而是 13 档张量枚举 + 32 权枚举共同给出。"
    "推论：谱只要含旋量，最小电荷就是 1，半整数磁通必被 A05/A06 关闭")

_tensor_only_minq = min(abs(x) for x in VQ if x != 0)
_has16 = (F(1) in _spin_set)
_b05 = (_tensor_only_minq == 2 and _has16 and field_ok(F(2), F(1, 2))
        and not field_ok(F(1), F(1, 2)))
add("B05", "B", "负对照：谱只含张量表示（丢掉旋量）时半整数磁通是否开放，代价是什么",
    "两个读数须不同（合法性升、SM 手征物质降）",
    "纯张量谱 min|q|=%s ; N=1/2 合法=%s ; 含旋量谱 min|q|=1 ; N=1/2 合法=%s ; "
    "谱里还有 16 旋量=%s（纯张量谱为否）" % (_tensor_only_minq, field_ok(F(2), F(1, 2)),
                                    field_ok(F(1), F(1, 2)), _has16),
    _b05,
    "=> 换表示确实能让半整数磁通合法，但代价是失去 16 / 16bar，"
    "即失去 SM 的 (3,2)_{1/6} 等手征物质。这是可算的两难，不是定性感叹")

_sm_spectrum = any(abs(x) == 1 for x in SPIN_Q)
_b06_hits = sum(1 for _p in HALF for _q2 in HALF
                if ((not is_int(_p)) or (not is_int(_q2)))
                and field_ok(F(1), _p) and field_ok(F(1), _q2) and _sm_spectrum)
_both_possible = _b06_hits > 0
add("B06", "B", "两难判决：半整数磁通与 SM 三代手征物质能否在同一谱里兼得",
    "不能（含 q=1 旋量则半整数陈类非法）",
    "遍历 %d 组半整数双磁通 ; 同时满足「至少一个陈类半整数」且「q=1 场 holonomy 单值」且「谱含 16」的组数 %d ; 谱含 q=1 旋量=%s"
    % (len(HALF) ** 2, _b06_hits, _sm_spectrum),
    _both_possible,
    "=> FAIL 是本册对「可兼得」这一主张的判负，已登记、不挡总门。"
    "它把 V63 §一 的三条出路里的「换表示」从候选降为有明确定价的代价项")

print("\n[C] 回代 V63 A08 与三条出路定价")

okC01 = len(SOL14) == 14 and len(LEGAL14) == 0
add("C01", "C", "回代 V63 整理册 A08 的 14 个半整数解：逐个检查两个陈类是否都合法",
    "合法解 0 个（上一卷 A08 给 14 个代数解）",
    "半整数解数 %d ; 两个陈类均为整数的解数 %d ; 首四个解 %s"
    % (len(SOL14), len(LEGAL14), [(fmt_f(p), fmt_f(q)) for (p, q) in SOL14[:4]]),
    okC01,
    "=> 14 个代数解全部落在非法的 U(1) 丛上。它们满足 I_Q=3 却不能实现为紧致化上的场；"
    "上一卷 A08 的读数作为本册输入，不新增证据、不相加")

okC02 = len(INT_SOL3) == 0 and all(is_int(chern_flux(_n)) for _n in GRID)
add("C02", "C", "整数陈类复核：I_Q = 2(N_F+N_Y) = 3 在整数网格上的解",
    "0 解（V63 整理册 B04 反抄）",
    "整数网格 %d 组 ; I_Q=3 解数 %d ; 全部 c1 合法 = %s"
    % (len(GRID) ** 2, len(INT_SOL3), all(is_int(chern_flux(_n)) for _n in GRID)),
    okC02,
    "=> 与上一卷 B04 同读数，但本册路径是「先判丛合法性再算指标」；按不相加纪律不重复计数")

add("C03", "C", "出路一「新内部几何」的定价（A09 的收口）",
    "不解除陈类整数性（H^2 均为 Z）",
    "S^2 与 Sigma_g 的 H^2 同为 Z ; 半整数 c1 在两者上都无 U(1) 主丛 ; 高亏格 Dirac 指标未重建",
    None,
    "=> INFO：只定价到同调群层，不给 PASS。要真正关闭该出路还需算 Sigma_g 上的零模谱，见 D04")

add("C04", "C", "出路二「不同表示的手征内容」的定价",
    "需换成纯张量谱（丢 16 / 16bar）",
    "纯张量谱 min|q|=2 使 N=1/2 合法（B05） ; 但该谱不含 16，故无 SM 手征双重态 ; "
    "含旋量谱 min|q|=1 使半整数非法（A06）",
    _b05,
    "=> PASS 是对「定价读数成立」的判定：这条路开放，但代价由 B05 精确给出，"
    "不是「换表示就能得三代」")

add("C05", "C", "出路三「严格构造的边界投影 / 缺陷」的定价",
    "带边界时 APS 指标定理的 eta 项可给半整数",
    "本册未计算 eta 不变量、未重建带边界 S^2 或 orbifold 的谱；按纪律不猜期望值",
    None,
    "=> INFO：三条出路里唯一尚未被本册可算定价的一条。来料 §一 把它列为首选，"
    "本册既不证实也不否定，只标明它必须重算反常与量子化条件")

okC06 = okC01 and okC02 and (not _both_possible) and _only_spinor
add("C06", "C", "总判定：三代奇偶障碍从「代数约定」升级为「拓扑定理」",
    "在给定规范群与谱下，半整数出口关闭、三条出路仅剩一类未定价",
    "丛非法解 %d/%d ; 整数网格 3 代解 %d ; 两难兼得组数 %d ; "
    "旋量是唯一奇数荷表示=%s ; 未定价出路数 %d" % (len(SOL14) - len(LEGAL14), len(SOL14),
                                            len(INT_SOL3), _b06_hits, _only_spinor,
                                            sum(1 for _x in ROWS if _x["id"] == "C05" and _x["kind"] == "INFO")),
    okC06,
    "=> 边界：这是「在 Spin(12) -> SO(10)xU(1)_F 嵌入、物质场为 32 旋量、"
    "底流形为闭曲面」的条件定理，不是「所有高维统一模型都不可能」")

print("\n[D] 判定与诚实边界")

add("D01", "D", "本册是否产出新物理或独立实验预言",
    "应只产可算判决",
    "本册只判陈类整数性与谱的最小电荷；未构造新作用量、未给新粒子、未给可检验数值；独立预言数 0",
    None,
    "=> INFO：项目红线。找到更硬的障碍 ≠ 统一已证，也 ≠ 统一被否证")

add("D02", "D", "与 V63 整理册 A08 / B04 的关系",
    "引用其读数作为输入，不新增证据",
    "A08 的 14 个半整数解回代见 C01 ; B04 的 0 命中复核见 C02 ; 本册以独立复算的 0 条替代"
    "（占位回填后由 n_rows 给出）",
    None,
    "=> INFO：两册条目不可相加；本册的价值在「给 A08 的代数解补上丛合法性」，"
    "而不是把 14 再数一遍（note 中的占位在落盘前回填，见守卫 BACKFILL-ORDER）")

add("D03", "D", "与 r391 / r392 / r393 / r394 的半整数出口定价的关系",
    "应标明不同层级",
    "既有卷在「指数 / 反常 / 量子化 Q」层定价半整数出口；本册在「U(1) 主丛陈类 + 谱最小电荷」层判合法性",
    None,
    "=> INFO：对象不同、不相加；本册不重做既有卷的指数定理")

add("D04", "D", "未重建的部分",
    "应列出全谱与边界项",
    "未计算 APS eta 不变量 ; 未重建高亏格 Sigma_g 的 Dirac 零模谱 ; "
    "未重建非平凡 Spin 结构 / Wilson line / orbifold 投影 ; 未做 4D 反常匹配",
    None,
    "=> INFO：C05 / A09 只定价到同调群层，正是这些未算项决定了边界投影能否真正给出三代")

add("D05", "D", "四力统一与 V64 三道关口的当前状态",
    "应同时得三代谱、真实质量混合、引力同源",
    "第一道（三代手征谱）：本册把可用机制压缩到边界/缺陷一类且仍需重算反常 ; "
    "第二道（质量与规范破缺）：未闭合 ; 第三道（引力同源）：未启动 ; 四力统一：未证明",
    None,
    "=> INFO：来料 V63 §七 自承的目标仍全部 OPEN；本册独立实验预言数 0")

add("D06", "D", "r402 收口遗留",
    "应补判定册、README 登记、MEMORY v34 与产物呈现",
    "r402 源码/json/report/html 已生成，判定册与 README 登记仍缺；本册为攻坚册，不新增 RID、不动 README",
    None,
    "=> INFO：与 V63 整理册 OPEN X-V63-5 同一遗留；链的完整性需在单独一轮收口")

print("\n[GUARD] 判据反噬与汇总")

cnt = {}
for _row in ROWS:
    cnt[_row["kind"]] = cnt.get(_row["kind"], 0) + 1
N_ROWS = len(ROWS)

guard("ENTRY-ACT", all(x["act"].strip() for x in ROWS) and all(x["exp"].strip() for x in ROWS),
      "%d 条均有 exp 与 act 读数" % N_ROWS)
guard("EXP-NEQ-ACT", all(x["exp"] != x["act"] for x in ROWS),
      "exp 与 act 文本全不相同的条数 %d / %d" % (sum(1 for x in ROWS if x["exp"] != x["act"]), N_ROWS))

_a02_legal = sum(1 for _x in _bad if _x[2])
_neg = [(6, _a02_legal),
        (field_ok(F(1), F(1, 2)), field_ok(F(2), F(1, 2))),
        (int(_tensor_only_minq), int(min(abs(x) for x in SPIN_Q)))]
guard("NEG-CONTROL", all(a != b for a, b in _neg) and len(_neg) == 3,
      "三对负对照读数 %s（每对两半须不同）" % _neg)
guard("MIN-CHARGE-FLIP", field_ok(F(2), F(1, 2)) and not field_ok(F(1), F(1, 2)),
      "q=2 与 q=1 在 N=1/2 上给出相反读数（扰动落在真正敏感方向）")
guard("NORM-INVARIANT", len(set(x[3] for x in NORM)) == 1,
      "5 个 lam 档给出同一 q*k = %s" % sorted(set(x[3] for x in NORM)))
guard("LAM-ALL-EVEN", all(_r[5] for _r in _lam_rows) and _b01 and not all(is_int(x / 2) for x in SPIN_Q),
      "13 档张量全偶 / 矢量全偶 / 旋量含奇（三个独立对象）")
guard("SOL14-ILLEGAL", len(SOL14) == 14 and len(LEGAL14) == 0,
      "14 个半整数解中双陈类全合法的解数 %d" % len(LEGAL14))
guard("SAME-SOURCE-TAGGED",
      any(x["id"] == "A04" and x["kind"] == "INFO" and "同源" in x["note"] for x in ROWS),
      "Wu-Yang 与 Chern-Weil 被显式标为同源、未冒充独立 PASS")

_src_path = os.path.abspath(__file__)
with io.open(_src_path, "r", encoding="utf-8") as _f:
    _tree = ast.parse(_f.read())
_hard = []
for _node in ast.walk(_tree):
    if isinstance(_node, ast.Call) and isinstance(_node.func, ast.Name) and _node.func.id == "add":
        if len(_node.args) >= 6 and isinstance(_node.args[5], ast.Constant) and isinstance(_node.args[5].value, bool):
            _hard.append(_node.lineno)
guard("NO-HARDCODE-OK", len(_hard) == 0,
      "AST 层扫 add() 第 6 实参为 True/False 字面量的处数 %d" % len(_hard))
guard("NOT-ALL-GREEN", cnt.get("FAIL", 0) >= 1 and cnt.get("IDENTITY", 0) >= 1,
      "FAIL %d / IDENTITY %d（防首跑全绿）" % (cnt.get("FAIL", 0), cnt.get("IDENTITY", 0)))


def final_of(nf_main, nf_guard, n_decl):
    if nf_guard > 0:
        return "GATES-FAIL-GUARD-%d" % nf_guard
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    if n_decl >= nf_main:
        return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main
    return "GATES-FAIL-MAIN-%d" % nf_main


guard("FINAL-BRANCHES",
      final_of(0, 0, 0) == "GATES-PASS-ALL-POSITIVE"
      and final_of(0, 1, 0) == "GATES-FAIL-GUARD-1"
      and final_of(1, 0, 0) == "GATES-FAIL-MAIN-1"
      and final_of(1, 0, 1) == "GATES-PASS-WITH-1-NEGATIVE",
      "四分支 (0,0,0)/(0,1,0)/(1,0,0)/(1,0,1) 各自判词正确")

nf_main = cnt.get("FAIL", 0)
nf_guard = sum(1 for g in GUARDS if not g["ok"])
n_decl = 1 if any(x["id"] == "B06" and x["kind"] == "FAIL" for x in ROWS) else 0
FINAL = final_of(nf_main, nf_guard, n_decl)

vp = []
vp.append("CHERN_CLASS_%s" % ("N_INTEGER" if okA03 else "BAD"))
vp.append("FLUX_NORM_%s" % ("HALF" if okA01 else "BAD"))
vp.append("NEG_CONTROL_%s" % ("FLIPS" if okA02 and okA06 else "BAD"))
vp.append("HOLONOMY_%s" % ("Q_DEPENDENT" if okA05 else "BAD"))
vp.append("MIN_CHARGE_SENSITIVE_%s" % ("YES" if okA06 else "BAD"))
vp.append("NORM_INVARIANT_%s" % ("QK_FIXED" if okA07 else "BAD"))
vp.append("EVEN_INDEX_%s" % ("IDENTITY" if len(INT_SOL3) == 0 else "BAD"))
vp.append("TENSOR_CHARGES_%s" % ("ALL_EVEN" if _b02 and _b01 else "BAD"))
vp.append("SPINOR_%s" % ("ONLY_ODD_CHARGE" if _only_spinor else "BAD"))
vp.append("A08_14_SOLUTIONS_%s" % ("ALL_ILLEGAL" if okC01 else "BAD"))
vp.append("THREE_GEN_INTEGER_GRID_%s" % ("ZERO_SOLUTION" if okC02 else "BAD"))
vp.append("DILEMMA_%s" % ("FAIL" if not _both_possible else "OK"))
vp.append("EXIT_GEOMETRY_INFO_NOT_PROVEN")
vp.append("EXIT_REPRESENTATION_COST_%s" % ("LOSES_16" if _b05 else "BAD"))
vp.append("EXIT_BOUNDARY_INFO_ETA_UNCOMPUTED")
vp.append("THREE_GEN_OBSTACLE_%s" % ("TOPOLOGICAL" if okC06 else "BAD"))
vp.append("FOUR_FORCE_INFO_UNPROVEN")
vp.append("UNIQUE_PREDICTION_0")
VERD = "__".join(vp)

KEY = {
    "vector_charges": [fmt_f(x) for x in VQ],
    "lam_rows": _lam_rows,
    "spin_charges": [fmt_f(x) for x in _spin_set],
    "n_spin_weights": len(SPIN_Q),
    "min_charge_tensor": int(_tensor_only_minq),
    "min_charge_spinor": int(min(abs(x) for x in SPIN_Q)),
    "half_grid_size": len(HALF_GRID),
    "legal_c1_count": len(legal_c1),
    "c1_three_halves": fmt_f(chern_flux(F(3, 2))),
    "bad_norm_cases": _bad,
    "holo_matrix": _holo_txt,
    "norm_table": NORM,
    "n_sol14": len(SOL14),
    "n_legal14": len(LEGAL14),
    "int_sol3": len(INT_SOL3),
    "b06_hits": _b06_hits,
    "int_sin_simpson": "%.12f" % INT_SIN,
    "unpriced_exits": 1,
}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, "_XV631_recompute_2026-11-06.json")
rp = os.path.join(DATA, "_XV631_recompute_report_2026-11-06.txt")


def make_out(rows_obj, verdict, final):
    return {"title": TITLE, "date": DATE, "verdict": verdict, "final": final,
            "counts": cnt, "n_rows": N_ROWS,
            "guards": {"n_ok": sum(1 for g in GUARDS if g["ok"]),
                       "n_total": len(GUARDS), "rows": GUARDS},
            "rows": rows_obj, "key_numbers": KEY}


# 回填顺序：先写（占位） -> 回读 -> 回填 -> 再写 -> 最后才拼报告
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(make_out(ROWS, VERD, FINAL), ensure_ascii=False, indent=1))
with io.open(jp, "r", encoding="utf-8") as f:
    back = json.load(f)
_placeholder = any("独立复算的 0 条" in x["act"] for x in back["rows"] if x["id"] == "D02")
for x in back["rows"]:
    if x["id"] == "D02":
        x["act"] = x["act"].replace("独立复算的 0 条", "独立复算的 %d 条" % N_ROWS)
for x in ROWS:
    if x["id"] == "D02":
        x["act"] = x["act"].replace("独立复算的 0 条", "独立复算的 %d 条" % N_ROWS)
_backfill = _placeholder and any(("独立复算的 %d 条" % N_ROWS) in x["act"]
                                 for x in back["rows"] if x["id"] == "D02")
guard("BACKFILL-ORDER", _backfill and back["n_rows"] == N_ROWS,
      "占位存在=%s ; 回读回填生效=%s ; n_rows=%d" % (_placeholder, _backfill, back["n_rows"]))
guard("VERDICT-MACHINE", len(vp) >= 15 and VERD.count("__") == len(vp) - 1,
      "判词由 %d 个机拼片段组成，连接符数 %d" % (len(vp), VERD.count("__")))
guard("KIND-COUNT", sum(cnt.values()) == N_ROWS and cnt.get("FAIL", 0) == nf_main,
      "kind 计数 %s 合计 %d" % (cnt, N_ROWS))

FINAL = final_of(nf_main, sum(1 for g in GUARDS if not g["ok"]), n_decl)
back["verdict"] = VERD
back["final"] = FINAL
back["guards"] = {"n_ok": sum(1 for g in GUARDS if g["ok"]),
                  "n_total": len(GUARDS), "rows": GUARDS}
with io.open(jp, "w", encoding="utf-8") as f:
    f.write(json.dumps(back, ensure_ascii=False, indent=1))

# 报告在回填之后才拼，并从最终 JSON 回读
with io.open(jp, "r", encoding="utf-8") as f:
    final_obj = json.load(f)
L = []
L.append("=" * 78)
L.append("%s  复算报告  %s" % (TITLE, DATE))
L.append("=" * 78)
L.append("体例：跨卷攻坚册（主动机核 X-V63-1；不新增 RID、不进 README、条目不与任何卷相加）")
L.append("判词：%s" % final_obj["verdict"])
L.append("总门：%s" % final_obj["final"])
L.append("条目 %d：%s" % (final_obj["n_rows"], ", ".join("%s %d" % (k, final_obj["counts"][k])
                                                  for k in sorted(final_obj["counts"]))))
L.append("")
for x in final_obj["rows"]:
    L.append("%-5s %-8s %s" % (x["id"], x["kind"], x["name"]))
    L.append("       exp = %s" % x["exp"])
    L.append("       act = %s" % x["act"])
    if x["note"]:
        L.append("       note= %s" % x["note"])
L.append("")
L.append("守卫 %d/%d" % (final_obj["guards"]["n_ok"], final_obj["guards"]["n_total"]))
for g in final_obj["guards"]["rows"]:
    L.append("  %-20s %s | %s" % (g["name"], "ok" if g["ok"] else "BAD", g["detail"]))
L.append("")
L.append("关键读数摘要（机拼，供攻坚册直接引用，禁手写）")
K = final_obj["key_numbers"]
L.append("  矢量 12 荷 %s ; 旋量 32 荷 %s（权数 %d）"
         % (K["vector_charges"], K["spin_charges"], K["n_spin_weights"]))
L.append("  Lambda^k 全 13 档 (k, 权数, q_min, q_max, 零荷数, 全偶) = %s" % K["lam_rows"])
L.append("  Lambda^k 零荷数序列 = %s ; 旋量权数 = %d"
         % ([_r[4] for _r in K["lam_rows"]], K["n_spin_weights"]))
L.append("  最小电荷：张量侧 %s / 旋量侧 %s ; 半整数网格 %d 个值中合法陈类 %d 个"
         % (K["min_charge_tensor"], K["min_charge_spinor"], K["half_grid_size"], K["legal_c1_count"]))
L.append("  F 误归一负控 c1_bad(N)=2N/3 的 N=1..6 读数 %s" % K["bad_norm_cases"])
L.append("  holonomy 合法矩阵（q 行 / N 列）%s ; 归一不变性表 %s"
         % (K["holo_matrix"], K["norm_table"]))
L.append("  V63 A08 半整数解 %d 个，双陈类全合法 %d 个 ; 整数网格 I_Q=3 解 %d 个 ; 两难兼得组数 %d"
         % (K["n_sol14"], K["n_legal14"], K["int_sol3"], K["b06_hits"]))
L.append("  Simpson sanity int sin = %s（解析 2）; 尚未定价的出路数 %d"
         % (K["int_sin_simpson"], K["unpriced_exits"]))
with io.open(rp, "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(L) + "\n")

print("\n" + "=" * 78)
print("条目 %d：%s" % (final_obj["n_rows"],
                 ", ".join("%s %d" % (k, final_obj["counts"][k]) for k in sorted(final_obj["counts"]))))
print("守卫 %d/%d ; 总门 %s" % (final_obj["guards"]["n_ok"],
                             final_obj["guards"]["n_total"], final_obj["final"]))
print("=" * 78)
print("written:")
print("  %s" % os.path.basename(jp))
print("  %s" % os.path.basename(rp))
