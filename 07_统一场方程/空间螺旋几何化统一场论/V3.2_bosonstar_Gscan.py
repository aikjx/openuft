#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TUFT V3.2 · 临界引力耦合 G* 扫描（修复打靶后）
================================================
对稳定窗内 ω 扫引力耦合 G，找 TUFT 势仍能形成局域玻色星的临界 G*(ω)。
g→0 平直 Q-ball 存在；g=1 无解（坍缩）⇒ 存在临界 G*（低于它稳定玻色星存在，
高于则坍缩）。与上一轮解析估算 G*=0.01398（M/M_max=1）对比校验。
"""
import os, time, json
import mpmath as mp
from importlib.util import module_from_spec, spec_from_file_location

H = os.path.dirname(os.path.abspath(__file__))
_spec = spec_from_file_location("bss", os.path.join(H, "V3.2_bosonstar_solve.py"))
B = module_from_spec(_spec); _spec.loader.exec_module(B)
mp = B.mp

def has_solution(omega, g):
    """修复打靶：g 下是否存在局域玻色星解。返回 (bool, s0, M)"""
    s0 = B.shoot_sigma0(omega, g=mp.mpf(g))
    if s0 is None:
        return (False, None, None)
    rs, ys = B.integrate(omega, s0, g=mp.mpf(g))
    M = ys[-1][0]
    return (True, s0, M)

def find_Gstar(omega, g_lo=mp.mpf("1e-5"), g_hi=mp.mpf("1.0")):
    """二分找临界 G*：g<G* 有解，g>G* 无解。返回 G*。"""
    lo, hi = g_lo, g_hi
    # 先确保 lo 有解、hi 无解
    if not has_solution(omega, lo)[0]:
        return None  # 最低 g 也无解（异常）
    if has_solution(omega, hi)[0]:
        return None  # g=1 也有解（未到临界）
    for _ in range(30):
        mid = mp.sqrt(lo * hi)
        ok, _, _ = has_solution(omega, mid)
        if ok: lo = mid
        else: hi = mid
    return mp.sqrt(lo * hi)

def main():
    mp.mp.dps = 30
    print("="*72)
    print("TUFT V3.2 · 临界引力耦合 G*(ω) 扫描")
    print("V1=1.2 V2=0.4 M2=0.4 m=0.447  修复打靶（排除视界伪根）")
    omegas = [mp.mpf(x) for x in ["0.18","0.20","0.2064","0.21","0.22","0.24","0.25","0.28","0.30","0.34"]]
    rows = []
    t0 = time.time()
    for w in omegas:
        Gs = find_Gstar(w)
        if Gs is None:
            print("ω=%.4f 未找到 G*（全域有解或全域无解）" % float(w)); continue
        rows.append((float(w), float(Gs)))
        print("ω=%.4f  G*=%.6g  (%.0fs)" % (float(w), float(Gs), time.time()-t0))
    json.dump(rows, open(os.path.join(H,"V3.2_bosonstar_Gstar.json"),"w",encoding="utf-8"))
    print("="*72)
    print("已落盘 V3.2_bosonstar_Gstar.json：%d 个临界点" % len(rows))
    if rows:
        print("参考：上一轮解析估算 G*(M/M_max=1)=0.01398；G=0.0056 时 M/M_max=0.40（稳定暗物质候选）")

if __name__ == "__main__":
    main()
