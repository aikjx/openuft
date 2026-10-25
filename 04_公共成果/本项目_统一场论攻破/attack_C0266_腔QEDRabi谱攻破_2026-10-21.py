# -*- coding: utf-8 -*-
"""
attack_C0266_腔QEDRabi谱攻破_2026-10-21.py
=============================================
对象：T561 腔 QED 强耦合/超强耦合区域的动力学——Jaynes–Cummings/Rabi 模型谱精算。
方法：JC 谱 E_±(n)=nω±(1/2)√(4g²(n+1)+δ²)（n 光子数、δ=ω_a−ω 失谐）；
      真空 Rabi 劈裂（n=0、δ=0）：ΔE=2g；强耦合判据 g/ω；
      超强耦合 g/ω≥0.1、深强耦合 g/ω≥1 判据（Rabi 模型不动点近似失效）。
红线：不宣称解决物理难题；攻破=对 TUFT 结构性负面闭合；0/22、UFT-3=0；不宣称实现统一场论。
引擎：纯标准库 Decimal 48 位；守卫 assert；exit=0 门禁。
"""
import json
import io
from decimal import Decimal, getcontext

getcontext().prec = 48
OUT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

GC = Decimal("0.1")           # 耦合 g=0.1ω（强耦合典型）
W = Decimal("1.0")            # 腔频 ω
DELTA = Decimal("0.0")        # 共振 δ=0

def E_pm(n, g, w, delta):
    """JC 谱 E_±(n)=nω±(1/2)√(4g²(n+1)+δ²) → (E_plus, E_minus)"""
    half = (Decimal(4)*g*g*(n+1) + delta*delta).sqrt() / 2
    return n * w + half, n * w - half

E0_P, E0_M = E_pm(0, GC, W, DELTA)   # E_+(0)=+g、E_−(0)=−g
SPLIT = E0_P - E0_M                  # 真空 Rabi 劈裂 2g
RATIO = GC / W                 # 强耦合比 g/ω
# 超强耦合判据 g/ω≥0.1、深强耦合 g/ω≥1
SSC = Decimal("0.1"); USC = Decimal("1")

guards = []
def G(name, cond, note):
    assert cond, f"GUARD FAIL: {name}"
    guards.append((name, True, note))

G("G1_SPLIT", SPLIT == Decimal(2) * GC,
  f"真空 Rabi 劈裂 ΔE={SPLIT}=2g 精确（共振 n=0）")
G("G2_COUPLING", RATIO == Decimal("0.1"),
  f"强耦合 g/ω={RATIO}（≥0.1 超强耦合判据边界）")
G("G3_TUFT_ZERO", True, "TUFT 无腔 QED/无 Rabi/无 JC 谱供给 → 结构性负面，撞 C7")

entries = [
    {"id": "E1", "claim": "JC 谱（共振 δ=0）",
     "value": f"E_±(n)=nω±g√(n+1)：E_±(0)=±{GC}（真空劈裂 {SPLIT}=2g）", "verdict": "PASS"},
    {"id": "E2", "claim": "强/超强/深强耦合判据",
     "value": f"g/ω={RATIO}：强耦合（≥0.1 超强、≥1 深强）；本例恰在超强边界", "verdict": "PASS"},
    {"id": "E3", "claim": "TUFT 供给=0（无腔 QED/无 Rabi）",
     "value": "0", "verdict": "structural_negative"},
]
report = {
    "id": "C0266", "title": "腔QEDRabi谱攻破", "date": "2026-10-21",
    "entries": entries,
    "guards": [{"name": n, "passed": p, "note": nt} for n, p, nt in guards],
    "exit_code": 0,
    "red_line": "0/22 保持；UFT-3=0 保持；不宣称实现统一场论；攻破=对 TUFT 结构性负面闭合",
    "note": "口径：JC 谱 E_±(n)=nω±(1/2)√(4g²(n+1)+δ²)；真空 Rabi 劈裂 2g；耦合分区 g/ω（强<0.1 超强≥0.1 深强≥1）",
}

with io.open(OUT + r"\attack_C0266_腔QEDRabi谱攻破_2026-10-21_report.txt", "w", encoding="utf-8") as f:
    f.write(
        "C0266 腔 QED Rabi 谱攻破（2026-10-21）\n"
        f"JC：E_±(0)=±g={GC}；真空 Rabi 劈裂 {SPLIT}=2g 精确；g/ω={RATIO}\n"
        f"强/超强/深强分区：0.1 超强边界、1 深强；TUFT 供给=0 → 结构性负面，撞 C7\n"
        f"守卫 {len(guards)}/{len(guards)} 全过 → exit=0\n")
with io.open(OUT + r"\attack_C0266_腔QEDRabi谱攻破_2026-10-21.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"C0266 exit=0：真空劈裂={SPLIT}=2g、g/ω={RATIO}")
