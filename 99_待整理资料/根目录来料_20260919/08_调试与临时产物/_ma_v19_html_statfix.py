# -*- coding: utf-8 -*-
# MainAgent v19 归一化收尾：把架构图残留的 v1.8 统计/勘误计数刷到 v1.9（E1-E418 / 24 条勘误），
# 并把本轮第二次独立复跑（39.5s）对群延迟 tau 的强化结论并入 ④-9。精确替换 + 计数断言。
import io,sys
p="TUFT_企业级归一化全维架构图_E1-E336.html"
s=io.open(p,encoding="utf-8").read()
def rep(old,new,n=1):
    c=s.count(old)
    assert c==n,"expect %d got %d for %r"%(n,c,old[:40])
    return s.replace(old,new)

# 1) 编号位徽章 -> E1-E418
s=rep("E1–E385 + E349–E353","E1–E418")
s=rep("编号位（v11/12 方法学新增，见去重说明）","连续编号（v1–v18；重号已顺延去重）")

# 2) 勘误计数 stat 23 -> 24
s=rep('<div class="n">23</div><div class="l">勘误固化条（#22 坐标·#23 频率2π）</div>',
      '<div class="n">24</div><div class="l">勘误固化条（#22 坐标·#23 频率2π·#24 τ/SNR/质量）</div>')

# 3) ⑥ 勘误节选 23 -> 24，追加 #24 条款
s=rep("【勘误节选·现共 23 条·禁止回退】","【勘误节选·现共 24 条·禁止回退】")
s=rep("ω=.90 969 Hz</b>。</div></div>",
      "ω=.90 969 Hz</b>｜<b style=\"color:#7ee787\">#24（v18）群延迟 τ=31.1M 粗网格 argR/unwrap 伪影降级 OPEN（结论用几何 2L 不依赖 τ）、SNR“4×”系 Voyager=O4/16 同义反复＋ε/ρ 手设非定量、质量改标铃响残迹 M_f</b>。</div></div>")

# 4) ④-9 勘误#24 补本轮第二次独立复跑（原始 argR 与平移到核两种 tau 约定均不稳）
s=rep("真实双程穿垒 ε&lt;1 只会更难。稳健不变：σ_abs=0、|R|²=1、无高 Q 壁腔窄谱。",
      "真实双程穿垒 ε&lt;1 只会更难。<b>MainAgent 第二次独立复跑（39.5 s）另确认：平移到核 φ=argR−2ωs_out 的 τ 同样不稳（落 −628~+355，跨 π 跳支），原始 argR 与核相位两种约定均不可用，唯几何 2L 可信。</b>稳健不变：σ_abs=0、|R|²=1、无高 Q 壁腔窄谱。")

io.open(p,"w",encoding="utf-8",newline="").write(s)
print("HTML stat/errata normalized to v1.9: E1-E418, 24 errata; second-rerun tau note added")
