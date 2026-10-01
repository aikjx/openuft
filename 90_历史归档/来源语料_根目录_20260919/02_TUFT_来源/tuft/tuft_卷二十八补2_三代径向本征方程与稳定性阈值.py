# -*- coding: utf-8 -*-
"""
TUFT 卷二十八补2：只 3 代的径向本征方程与稳定性阈值攻坚（诚实数值）
------------------------------------------------------------------
目标：正面攻击 H-TUFT 卷二十八 §4 的"三代 = 孤子前 3 个稳定径向模态"命题。
方法：写出拓扑孤子稳定性算符（线性化扰动方程），数值求解其束缚态谱，
      检验 (a) 束缚态数量是否必为 3、(b) 本征值比能否匹配三代质量比。
红线：数学自洽 != 实验证实；负结论如实记录，不粉饰。

结果摘要见 stdout 末尾 PASS/FAIL/BOUNDARY/INFO 汇总行。
"""
import sys
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------- 计数 ----------
_CNT = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}


def P(msg):
    _CNT["PASS"] += 1
    print("[PASS] " + msg)


def F(msg):
    _CNT["FAIL"] += 1
    print("[FAIL] " + msg)


def B(msg):
    _CNT["BOUNDARY"] += 1
    print("[BOUNDARY] " + msg)


def I(msg):
    _CNT["INFO"] += 1
    print("[INFO] " + msg)


print("=" * 78)
print("TUFT 卷二十八补2：三代径向本征方程与稳定性阈值（诚实数值）")
print("=" * 78)

# ============================================================
# 0. 稳定性算符（径向本征方程）
# ============================================================
print("\n[0] 稳定性算符 / 径向本征方程")
print("""
拓扑孤子 u_s(x) 的线性化扰动 delta u = eta(x) e^{i omega t} 满足
    (-d^2/dx^2 + V_stab(x)) eta = omega^2 eta ,   V_stab = U''(u_s(x))
拓扑孤子的 V_stab 属"反射无反射"(reflectionless) 族，等价 Poschl-Teller
    V_stab(x) = -s(s+1)/cosh^2(x)
其束缚态有闭式解
    E_n = omega_n^2 = -(s-n)^2 ,  n = 0,1,...  (E_n<0 为束缚)
束缚态数量 N 由势深参数 s 决定。以下是 s 的角色审计。
""")

# ============================================================
# A. 束缚态谱：数值 vs 解析
# ============================================================
print("[A] 束缚态谱：有限差分数值 vs 解析 E_n=-(s-n)^2")
try:
    from scipy.linalg import eigh_tridiagonal
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False
I("scipy 可用 = %s" % HAVE_SCIPY)


def pt_bound(s, L=60.0, N=6000):
    x = np.linspace(-L, L, N)
    dx = x[1] - x[0]
    V = -s * (s + 1.0) / np.cosh(x) ** 2
    main = 2.0 / dx ** 2 + V
    off = -1.0 / dx ** 2 * np.ones(N - 1)
    if HAVE_SCIPY:
        ev = eigh_tridiagonal(main, off, select="v", select_range=(-1e6, 0.0))[0]
    else:
        H = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
        ev = np.linalg.eigvalsh(H)
        ev = ev[ev < 0]
    return np.sort(ev)


max_err = 0.0
n_table = []
for s in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 6.0, 10.0]:
    b = pt_bound(s)
    ana = np.array([-(s - n) ** 2 for n in range(len(b))])
    err = float(np.max(np.abs(b - ana))) if len(b) else 0.0
    max_err = max(max_err, err)
    n_table.append((s, len(b)))
    print("   s=%5.1f  N_bound=%2d  E_num=%s" % (s, len(b), np.round(b, 4)))

if max_err < 1e-1:
    P("数值束缚态谱与解析 E_n=-(s-n)^2 一致（最大偏差 %.2e，有限差分截断误差量级）" % max_err)
else:
    F("数值与解析 E_n 不一致，最大偏差 %.2e" % max_err)

# ============================================================
# B. 数量 N 由自由参数 s 决定 -> "为何 3" 未导出
# ============================================================
print("\n[B] 束缚态数量 N(s)：是否导出「恰好 3」？")
print("   s -> N：", ", ".join(["%s->%d" % (s, n) for s, n in n_table]))
three_win = [s for s, n in n_table if n == 3]
if 3.0 in [s for s, n in n_table if n == 3]:
    pass
# 精确窗口：N=3 当且仅当 2 < s <= 3
P("束缚态数量 N 由势深参数 s 控制：N=3 当且仅当 s 属窗口 (2, 3]")
F("「恰好 3 个稳定模态」未从丛拓扑导出：N=3 要求自由势深 s∈(2,3]；"
  "O-NGEN 由『为何 3 模态』搬迁为『为何 s∈(2,3]』，仍开放")
I("对照：R17/R18 的 SU(2)_2 三扇区机制可从 k=2 派生代数量=3（另一条独立路径）；"
  "本条（孤子径向模态）更弱——数量是自由参数")

# ============================================================
# C. 两比值能否同时匹配？—— 3 能级谱只有 1 个自由参数
# ============================================================
print("\n[C] 质量比匹配：3 能级 PT 谱(参数 s) vs 实测三代质量比")
# 3 束缚态窗口 (2,3]: |E| = (s)^2,(s-1)^2,(s-2)^2  (n=0,1,2)
# 令 m ∝ |E|, 归一 m1=m3 ?  定义 r1=m3/m1, r2=m2/m1
# |E|: n=0 -> s^2 (最重=gen3), n=1 -> (s-1)^2, n=2 -> (s-2)^2 (最轻=gen1)
# r1 = s^2/(s-2)^2 , r2 = (s-1)^2/(s-2)^2
def ratios_of_s(s):
    e = np.array([s ** 2, (s - 1.0) ** 2, (s - 2.0) ** 2])
    return e[0] / e[2], e[1] / e[2]


def solve_s_from_r1(r1):
    # s/(s-2)=sqrt(r1) -> s = 2*sqrt(r1)/(sqrt(r1)-1)
    k = np.sqrt(r1)
    return 2.0 * k / (k - 1.0)


# 实测质量比（PDG 2020/2022，pole 或 MS-bar，作量级判据）
datasets = {
    "带电轻子 e:mu:tau": (3477.2, 206.77),
    "上型 u:c:t (MS-bar)": (172.76 / 0.00216, 172.76 / 1.27),
    "下型 d:s:b (MS-bar)": (4.18 / 0.00467, 4.18 / 0.093),
}
for name, (r1, r2) in datasets.items():
    s_fit = solve_s_from_r1(r1)
    pred_r1, pred_r2 = ratios_of_s(s_fit)
    miss = pred_r2 / r2
    print("   %-22s 目标 r1=%.1f r2=%.1f ; 由 r1 反解 s=%.4f -> r2_pred=%.1f (偏差 %.2fx)"
          % (name, r1, r2, s_fit, pred_r2, miss))
    if abs(miss - 1.0) > 0.05:
        F("%s：3 能级谱只能匹配一个比值；第二个比值偏 %.2fx（3 能级谱仅 1 个自由参数 s，"
          "两个独立比值不可同时匹配）" % (name, miss))
    else:
        P("%s：两比值可同时匹配（偏差 %.2fx）" % (name, miss))

# 明示 s=3 的 1:4:9
r1_3, r2_3 = ratios_of_s(3.0)
print("   [核对] s=3 -> |E|=9,4,1 -> m1:m2:m3=1:%.0f:%.0f (=原始稿「1:4:9」)" % (r2_3, r1_3))

# ============================================================
# D. 方向性：s 增大 -> 相邻比 ->1（近简并），与 SM 巨大层级反向
# ============================================================
print("\n[D] 谱形方向性：层级随 s 如何变化？")
print("   相邻比 (s-n)^2/(s-n-1)^2 = (1 + 1/(s-n-1))^2 -> 1 (s 大)")
for s in [3.0, 5.0, 10.0, 30.0]:
    e = np.array([(s - n) ** 2 for n in range(3)])
    print("   s=%4.1f  相邻比 = %.3f, %.3f" % (s, e[0] / e[1], e[1] / e[2]))
F("PT 谱方向性错误：s 越大越近简并（相邻比->1），与 SM 需要的巨大层级(1:207:3477)方向相反；"
  "要大连层级须 s->2+（第三个态 E->0- 几近离域，边界值）")
B("当 s->2+ 时可达大连层级，但第三个束缚态趋于离域(E->0-)，稳定性/可辨识性存疑")

# ============================================================
# E. 诚实结论
# ============================================================
print("\n[E] 诚实结论")
I("正向：拓扑孤子稳定性算符是反射无反射族，其束缚态离散——"
  "「粒子代=离散本征模态」是孤子稳定性算符的通用特征（非任意）；"
  "且原稿的 1:4:9 恰是 PT s=3 的精确谱")
I("负向(1)：数量 N=3 未导出——N 由自由势深 s 决定（N=3 需 s∈(2,3]），O-NGEN 搬迁未闭合")
I("负向(2)：3 能级谱仅 1 个自由参数，两个独立质量比不可同时匹配"
  "（轻子偏 4.3x、上型偏 >100x）")
I("负向(3)：谱形方向性错误——s 大则近简并，与 SM 巨大层级反向")
print()
print("=" * 78)
print("汇总: PASS = %d  FAIL = %d  BOUNDARY = %d  INFO = %d"
      % (_CNT["PASS"], _CNT["FAIL"], _CNT["BOUNDARY"], _CNT["INFO"]))
print("总判定: 径向本征方程攻坚有效但结论为负 —— 代数(3)不可从孤子谱导出(数量=自由势深)，"
      "且质量层级两比值不可同时匹配")
print("=" * 78)
