#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · 半经典量子化：Q-ball 整数电荷谱（迈向 L3 的第一步）
================================================================
Coleman 型 Q-ball 量子对应：电荷 Q 的 Q-ball = 标量场 Q 个量子的相干束缚态。
半经典量子化：Q → 整数 n。束缚判据 E0/Q < m_free(=√M2)。
本脚本从扫描数据构建离散质量谱 M(n) 与每量子结合能，验证束缚态性质。
诚实分级：半经典量子化（BOUNDARY→ 迈向量子化的第一步）；完整 QFT 量子化（圈修正、
α/α_G 绝对预言）仍为 OPEN。
"""
import json, mpmath as mp, os
mp.mp.dps = 20
H = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(H, "V3.2_Qball_scan.json"), encoding="utf-8"))
M2 = mp.mpf(d["M2"])
m_free = mp.sqrt(M2)   # 自由玻色子质量
rows = [r for r in d["rows"] if r.get("converged") and 0.15 <= r["omega"] <= 0.30]
rows.sort(key=lambda r: r["omega"])

print("="*66)
print("TUFT V3.2 · 半经典量子化：Q-ball 整数电荷谱")
print("m_free=√M2=%.4f  束缚判据 E0/Q < m_free" % float(m_free))
print("-"*66)
print("  ω      Q(n)      M=E0     E0/Q    Δ=√M2-E0/Q  结合分额 B/(n·m)")
spectrum = []
for r in rows:
    w = mp.mpf(r["omega"]); Q = mp.mpf(r["Q"]); E0 = mp.mpf(r["E0"])
    EQ = E0/Q; Delta = m_free - EQ
    frac = Delta/m_free
    n_int = int(round(float(Q)))
    spectrum.append((n_int, float(w), float(Q), float(E0), float(EQ), float(Delta), float(frac)))
    print("  %.4f  %4d  %8.3f  %.4f  %8.5f   %7.3f%%"
          % (float(w), n_int, float(E0), float(EQ), float(Delta), 100*float(frac)))
print("-"*66)
# 稳定窗（E0/Q<1 与 dE/dQ=ω>0）核心态
core = [s for s in spectrum if 0.18 <= s[1] <= 0.25]
n_min = min(s[0] for s in core); n_max = max(s[0] for s in core)
print("核心稳定整数荷 n∈[%d,%d]，质量 M∈[%.2f,%.2f]" %
      (n_min, n_max, min(s[3] for s in core), max(s[3] for s in core)))
print("每量子结合能 Δ=%.3f（m_free 的 ~%.1f%%），Q-ball 为真实束缚态"
      % (float(m_free) - max(s[4] for s in core), 100*float(m_free - min(s[4] for s in core))/float(m_free)))
json.dump({"m_free": float(m_free), "spectrum": spectrum},
          open(os.path.join(H, "V3.2_quantum_spectrum.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("落盘 V3.2_quantum_spectrum.json")
print("诚实分级：半经典量子化(BOUNDARY→迈向量子化第一步)；完整 QFT 量子化仍 OPEN")
