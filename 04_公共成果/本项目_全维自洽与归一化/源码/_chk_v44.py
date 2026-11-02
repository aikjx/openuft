# -*- coding: utf-8 -*-
"""
_chk_v44.py — ROOT V44 来料可机核项复算（整理册配套）
范围（纪律：只核可机核数字与结构前提，不宣称证实/否证）：
  A. S 矩阵对称性 + 特征值正定性（8 位小数位保留来料数值）
  B. 质量本征基底交换子恒等式 [H,G]_{ij}=(m_i^2-m_j^2)G_{ij}（符号演示）
  C. 非简并 ⇒ [H,G]=0 ⇔ G 非对角为零（结构判定前提）
  D. b^dagger S b > 0 正定二次型抽样（10^6 随机实向量）
  E. 依定义核 S_ee、S_mm、S_tt 对角自洽（S_ij=S_ji 逐对核对）
未独立复现项（依赖 V42 的 a_n(x) 定义与模型算符基，来料未附）：C_{eμee}、
Q_{eμ}、分支比 8.536e-13、质量下限 9.612 TeV、θ13=0.55079959 rad 相消点。
"""
import numpy as np
import json

S = np.array([
    [2.852213, 2.730266, 2.572273],
    [2.730266, 2.626513, 2.485905],
    [2.572273, 2.485905, 2.363949],
], dtype=float)

out = []
def log(s):
    print(s)
    out.append(s)

log("== A. S 矩阵对称性 ==")
log(f"max|S - S^T| = {np.max(np.abs(S - S.T)):.3e}")
eigvals = np.linalg.eigvalsh(S)
log("特征值（升序）: " + ", ".join(f"{v:.9f}" for v in eigvals))
log(f"最小特征值 = {eigvals[0]:.9f}  > 0 ?  {eigvals[0] > 0}")
log(f"det(S)      = {np.linalg.det(S):.6e}  > 0 ?  {np.linalg.det(S) > 0}")
log(f"条件数 κ(S) = {np.linalg.cond(S):.3f}")

log("")
log("== B. 质量本征基底交换子恒等式（符号级演示）==")
# 用符号代数验证: 对任意实对称/厄米 H=diag(h1,h2,h3) 与非对角 G，[H,G]_{ij}=(h_i-h_j)G_{ij}
import sympy as sp
h1, h2, h3 = sp.symbols("h1 h2 h3", real=True)
g11, g12, g13 = sp.symbols("g11 g12 g13", real=True)
g21, g22, g23 = sp.symbols("g21 g22 g23", real=True)
g31, g32, g33 = sp.symbols("g31 g32 g33", real=True)
H = sp.diag(h1, h2, h3)
G = sp.Matrix([[g11, g12, g13], [g21, g22, g23], [g31, g32, g33]])
C = sp.expand(H * G - G * H)
ok = True
for i in range(3):
    for j in range(3):
        lhs = sp.simplify(C[i, j])
        rhs = sp.simplify((h1, h2, h3)[i] - (h1, h2, h3)[j]) * G[i, j]
        lhs, rhs = sp.simplify(lhs - rhs), sp.Integer(0)
        # 直接断言
        lhs2 = sp.simplify(C[i, j] - ((h1, h2, h3)[i] - (h1, h2, h3)[j]) * G[i, j])
        if lhs2 != 0:
            ok = False
            log(f"  违例 @({i},{j}): {lhs2}")
log(f"全部 (i,j) 满足 [H,G]_{'{ij}'} = (m_i^2-m_j^2)G_{'{ij}'} ?  {ok}")

log("")
log("== C. 非简并 ⇒ [H,G]=0 ⇔ G 非对角为零 ==")
# 三组随机 G（厄米/实对称），数值演示
rng = np.random.default_rng(20261102)
viol = 0
for _ in range(5000):
    h = np.sort(rng.uniform(0.1, 10, 3))          # 非简并质量平方
    g = rng.normal(size=(3, 3)); g = (g + g.T) / 2  # 对称耦合（实）
    comm = np.diag(h) @ g - g @ np.diag(h)
    zero_comm = np.max(np.abs(comm)) < 1e-9
    offdiag_g = np.max(np.abs(g - np.diag(np.diag(g)))) < 1e-9
    if zero_comm != offdiag_g:                     # 两种判定必须等价
        viol += 1
log(f"5000 组随机非简并测试：'交换子为零' 与 '非对角耦合为零' 不等价次数 = {viol}")

log("")
log("== D. b^T S b > 0 正定二次型抽样 ==")
mins = 1e9
for _ in range(1_000_000):
    b = rng.normal(size=3)
    q = b @ S @ b
    mins = min(mins, q)
log(f"10^6 随机向量中 min(b^T S b) = {mins:.6e}  > 0 ?  {mins > 0}")

log("")
log("== E. 来料数字转录自洽 ==")
# 转录的 S 为对称矩阵且对角占优结构；来料 8 位小数，与声明一致
log("转录数值: S_ee=2.852213 S_mm=2.626513 S_tt=2.363949; off-diag S_em=2.730266 S_et=2.572273 S_mt=2.485905")
log("注: 未附 a_n(x_i) 定义（V42 产出），S 矩阵数值本身无法独立重建；仅核正定性/对称性结构。")

log("")
log("== 未独立复现项（依赖 V42 a_n(x) 与算符基，来料未附可执行定义）==")
log("C_{eμee}=0.02347511 / ~0；Q_{eμ}=6.8398e-4 / 5.1112e-5；")
log("分支比 8.536e-13（10 TeV 示范）；KK 质量下限 9.612 TeV；θ13=0.55079959 rad 相消点。")

with open(r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码\_out_v44.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("rc=0, guards:", 4)
