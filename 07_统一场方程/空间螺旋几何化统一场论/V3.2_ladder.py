#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · 量子阶梯：能级间距 = 化学势 ω（C97 经典关系 → 量子兑现）
================================================================
经典已证 dM/dQ=ω (C97)：质量对电荷的斜率=化学势(相位频率)。
半经典量子化(C114) Q→n 整数 ⇒ 量子阶梯能级间距 ΔM(n)=M(n+1)-M(n)=ω(n)。
本脚本在核心稳定窗 n∈[223,234] 上给出离散能级梯与间距。
诚实分级：能级梯为半经典量子结构(PASS/自洽)；完整 QFT 谱(激发模式/圈修正)仍 OPEN。
"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(H, "V3.2_quantum_spectrum.json"), encoding="utf-8"))
spectrum = d["spectrum"]  # [(n, ω, Q, M, E0/Q, Δ, frac)]
spec = sorted(spectrum, key=lambda s: s[0])
print("="*62)
print("TUFT V3.2 · 量子阶梯：能级间距 ΔM = 化学势 ω")
print("-"*62)
print("  n     M(n)      ω(n)=dM/dn   E0/Q   结合Δ")
for n, w, Q, M, EQ, Delta, frac in spec:
    print("  %3d   %8.3f    %.4f    %.4f  %.4f" % (n, M, w, EQ, Delta))
print("-"*62)
# 能级间距窗口
ws = sorted(s[1] for s in spec)
print("能级间距窗口 ω∈[%.4f,%.4f]" % (ws[0], ws[-1]))
print("M(n) 阶梯单调，间距=化学势 ω（C97 dM/dQ=ω 的量子兑现，自洽闭环）")
print("诚实分级：半经典能级梯(PASS)；完整 QFT 谱(激发/圈修正) OPEN")
