# -*- coding:utf-8 -*-
"""
算法联盟｜核查 alpha = v_perp / v  vs  alpha = v_perp / c
===========================================================
用户问: 是否应该是 alpha = v_perp / v (而不是 v_perp / c)?

公理: v_total^2 = v_perp^2 + v_par^2 = c^2
=> 合速率 v_total := c (空间元螺旋合速率恒等于光速)
所以 v (合速率) === c, 两者在公理下完全等价。

但要澄清符号歧义:
  - 若 v 表示"合速率/总速率" (speed magnitude): 则 v = c, alpha = v_perp/c = v_perp/v 等价。
  - 若 v 表示"角速度" (常写作 omega 或希腊 nu): 则 v_perp/v 量纲错误 (m/s vs 1/s),
    那种写法无意义。
本文按"v=合速率"解读, 并证明 alpha=v_perp/v 与 alpha=v_perp/c 在公理下是同一回事。

改动(用户指令"换速度为光速"):
直接把合速率锁死为光速 c, 所有分量从 c 出发计算; 并展示若合速率 != c 时
两种写法会如何分歧, 从而证明公理要求合速率必须是光速。
"""
import mpmath as mp
mp.mp.dps = 80

c = mp.mpf("299792458")            # 光速 (合速率基准)
alpha = mp.mpf("7.2973525693e-3")   # 注意: 这里是 EM alpha, 仅作几何占比 demo 时才等于 v_perp/c

def main():
    print("=" * 80)
    print("  alpha = v_perp / v  ?  vs  alpha = v_perp / c   (合速率恒取光速 c)")
    print("=" * 80)

    # ===== 用户指令: 换速度为光速 -> 合速率直接钉死为 c =====
    line()
    print("[设定] 合速率 v_total := c (空间元螺旋合速率恒等于光速, 不再作为自由变量)")
    print(f"  c = {float(c):.6e} m/s")

    # 取一个几何横向占比 beta (几何 alpha, 不混同 EM alpha)
    beta_geom = mp.mpf("0.3")   # 演示: 横向占合速率 30%
    # 所有分量从 c 出发
    v_total = c                      # <<< 换速度为光速: 合速率 = c
    v_perp = beta_geom * v_total     # = beta * c
    v_par   = mp.sqrt(v_total**2 - v_perp**2)

    print("\n[数值] beta_geom = v_perp/c = 0.3, 合速率已换为光速")
    print(f"  v_total = {float(v_total):.6e}  (= c)")
    print(f"  v_perp  = {float(v_perp):.6e}")
    print(f"  v_par   = {float(v_par):.6e}")

    alpha_a = v_perp / v_total     # alpha = v_perp / v
    alpha_b = v_perp / c           # alpha = v_perp / c
    print("\n[对比] 合速率=光速时")
    print(f"  alpha = v_perp/v_total = {float(alpha_a):.10f}")
    print(f"  alpha = v_perp/c       = {float(alpha_b):.10f}")
    print(f"  |diff|                = {float(abs(alpha_a-alpha_b)):.3e}  => 完全等价")

    # ===== 反例: 若合速率不是光速, 两种写法会分歧 =====
    line()
    print("[反例] 若合速率 v_total != c (破坏公理), 两种写法分歧:")
    for vtot in [mp.mpf("1e8"), mp.mpf("5e8")]:   # 非光速合速率
        vp = beta_geom * vtot
        va = mp.sqrt(vtot**2 - vp**2)
        aa = vp / vtot          # alpha = v_perp / v_total
        ab = vp / c             # alpha = v_perp / c
        print(f"  v_total={float(vtot):.3e}: alpha(v_perp/v)={float(aa):.6f}  "
              f"alpha(v_perp/c)={float(ab):.6f}  diff={float(abs(aa-ab)):.3e}")
    print("  >> 只有合速率=v_total=c 时二者一致; 公理'合速率=光速'是等价前提。")

    # 量纲检查: 若有人把 v 解读成角速度 omega
    line()
    print("[符号歧义警告]")
    print("  若 v 被误用作'角速度'(通常记 omega, 单位 1/s):")
    print("    v_perp [m/s] / omega [1/s] = [m]  -> 量纲 [长度], 不是无量纲 alpha")
    print("    => 那种写法量纲错误, 必须 v 表示合速率(单位 m/s)才成立。")
    print("  结论: alpha = v_perp/v 仅在 'v = 合速率' 时正确, 此时 = v_perp/c。")

    # 与 EM alpha 的关系
    line()
    print("[与 EM alpha 的边界]")
    print(f"  EM alpha = {float(alpha):.6e}  (测量耦合常数)")
    print("  几何 alpha = v_perp/c 是自由几何自由度(可任取, 如 0.3);")
    print("  除非额外证明 v_perp/c = 7.3e-3, 否则几何 alpha != EM alpha。")
    print("  (见 derive_Geps0_*.md: beta_perp 反推 = 2.67e-20, 与 EM alpha 差 17 量级)")

def line():
    print()

if __name__ == "__main__":
    main()
