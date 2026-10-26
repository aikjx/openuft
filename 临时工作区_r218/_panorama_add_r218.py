# -*- coding: utf-8 -*-
"""Add r218 conclusion to panorama list + refresh stale range references."""
import io
import sys

P = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\整理_原创理论体系与方程全景清单_2026-10-24.md"

t = io.open(P, encoding="utf-8").read()

anchor = "5. **P01/P02/P04**：未建模，无方程可攻（不计为已建立理论）。"
if anchor not in t:
    print("FATAL: anchor miss")
    sys.exit(3)

new_item = anchor + """

6. **力的大统一（D5 族 / S02 §18《四力统一方程》）**：由 r218 机检（条目 19 = FAIL 13 / PASS 3 / INFO 3；控制组 29/29、守卫 12/12、rc=0）——统一式 `F=s·ℏc·Q₁Q₂(1/r²+1/rλ)e^{−r/λ}`（λ=ℏ/m_c c）在**引力与电磁两个通道与已知定律的相符是定义恒等式**：把 Q 的定义代入后单项式精确归约为 G·m₁m₂ 与 e²Z₁Z₂/(4πε₀)（残差 **0**），摄动 Q ±10% ⇒ 相符度偏离 19%/21%，框架内部**无**「Q 应取何值」的约束（内部推导方程计数 **0**，配正对照证非恒零）⇒ (G, α, m_W, m_Z, m_π⁰, α_w, g_π²/4π, σ) **全为外部给定，预测预算 = 0**。形式**确有**距离律判别力（负对照拟合 r⁻¹/r⁻³/r⁻⁴/r⁻⁵ 最优残差 216%/66.5%/159%/298%），但靶**从未**同实验数据做形状 confrontation（比较 token 命中 0，其校验项全为恒等式对拍与单位换算）。**覆盖 3/4**：形式内的「强」行是 π⁰ 交换**剩余核力**（复合层次有效力），基本色相互作用（胶子）被判「不在本形式内」；且两「强」行在重叠窗口 [0.2,1.2] fm 互算矛盾达 8.7×–388.6×。结构层：静态中心标量势梯度 ⇒ **不能承载洛伦兹磁力**（无速度依赖）与**弱力 V−A**（宇称偶）。修复定价 2⁴=16 ⇒ **EMPTY 15 / SUICIDE 1 / SURVIVE 0**（本线第 25 度「修复即自杀」）。**§18 的 Proca/Yukawa 单极势为教科书标准结果（靶自承）**，本卷降级认识为**重述层**。"""

t = t.replace(anchor, new_item)

subs = [("不可与 r142–r203 各卷条目相加", "不可与 r142–r218 各卷条目相加"),
        ("r14–r203 攻破链终态产物", "r14–r218 攻破链终态产物")]
for a, b in subs:
    if a in t:
        t = t.replace(a, b)
    else:
        print("WARN miss:", a)

io.open(P, "w", encoding="utf-8").write(t)
print("panorama updated with r218")
