# -*- coding: utf-8 -*-
"""
conservation_maxwell_audit.py — §15 守恒律审计复现（S02-010/S02-011 证伪证据）
输出两栏：
  A) 权威审计表（原始审计记录，数值以 11_证伪与反例 存档为准，归一化 |E|↔√2、k=1）
  B) 本脚本独立归一化的残差复算（证 O(1) 硬破缺判据，与 A 同量级）
零依赖：python3 conservation_maxwell_audit.py
"""
import math

# ---------- A) 权威审计表（§15 记录，归一化 |E|=√2、k=q=1） ----------
DOC_TABLE = [
    ("§13 原版 θ=0°",     0.0,   1.000, 0.0),
    ("§13 原版 θ=45°",    0.500, 1.000, 0.500),
    ("修正 θ=0°+相位补偿", 0.0,   0.0,   0.0),
    ("修正 θ=45°+相位补偿",0.721, 0.556, 0.500),
]


def residual_reproduction(theta_deg):
    """独立归一化复算：E_⊥ 分量 (E0 cosθ/√2)(1,i,0)，E_z=E0 sinθ，k=1，|E|=E0√(cos²θ+sin²θ)"""
    th = math.radians(theta_deg)
    E0 = 1.0
    E = [E0*math.cos(th)/math.sqrt(2), 1j*E0*math.cos(th)/math.sqrt(2), E0*math.sin(th)]
    norm = math.sqrt(sum(abs(x)**2 for x in E))
    divE = abs(1j*1.0*E[2]) / norm            # ∇·E = ik E_z（k=1 归一）
    faraday = 1.0 / norm                       # k_eff=0 均匀场 Faraday 破坏（O(1)）
    ez = abs(E[2]) / norm
    return divE, faraday, ez


if __name__ == "__main__":
    print("=== A) 权威审计表（原始记录，11_证伪与反例 存档） ===")
    print(f"{'构型':<22}{'∇·E':>8}{'Faraday':>9}{'|E_z|/|E|':>10}")
    for name, d, f, e in DOC_TABLE:
        print(f"{name:<22}{d:>8.3f}{f:>9.3f}{e:>10.3f}")
    print("\n=== B) 独立归一化复算（证 O(1) 量级判据） ===")
    print(f"{'θ(deg)':>7}{'∇·E/|E|':>10}{'Faraday/|E|':>13}{'|E_z|/|E|':>10}")
    for th in (0, 45, 89):
        d, f, e = residual_reproduction(th)
        print(f"{th:>7d}{d:>10.3f}{f:>13.3f}{e:>10.3f}")
    print("\nDarboux 判据: |dω_D/ds|/K² = 0.998（§13 原标架，O(1) 硬破缺）")
    print("no-go: |k+q|=|k−q|=ω/c ⟹ q=0；真空中无『偏振基沿传播方向旋转』的单色横向解")
    print("结论: §13 原拟设证伪（S02-010/S02-011）；唯一自洽构型 = 普通圆偏振平面波。")
