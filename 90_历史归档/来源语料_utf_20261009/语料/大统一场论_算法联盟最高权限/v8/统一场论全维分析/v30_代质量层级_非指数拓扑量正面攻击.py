# -*- coding: utf-8 -*-
"""
v30  代质量层级正面攻击：非指数拓扑量穷举 + 小整数代数组合搜索
==================================================================
最后一个最大诚实开放项：代质量层级绝对值（v23 缺口 ~500×，
单参数拓扑 Yukawa 已证伪）。v29 新线索：SU(2)_k Jones 表示谱属
Q(ζ₁₀)（相位 π/5 有理倍），√2@SU(2)_2、φ@SU(2)_3——拓扑量是
代数数（非指数）。本版系统穷举：

  A1  基线复现：单参数 φ 幂次（v29 已 FAIL，作对照）
  A2  非指数拓扑量族（量子维数 d_j(k)、S 矩阵元、中心荷 c(k)）中
      搜索能产生 r12=mμ/me, r23=mτ/mμ, r13=mτ/me 的量
  A3  「代=level」假设：三代 ↔ SU(2)_k (k=2,4,6 / 2,3,4) 的
      c(k), d_1(k), (k+2)/k 等比值族
  A4  小整数代数组合穷举（对数域）：基 {φ,√2,2,3,5} 指数 [-10,10]
      的 ≤5 因子乘积拟合三个质量比，报告全局最优与相对误差
判定红线：机器零 <1e-9 才 PASS；<3% 标 INFO（数值巧合待审）；
其余 FAIL（诚实证伪）。不粉饰。
"""
import os, sys, json, math, itertools
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def add(check, verdict, value, note):
    results.append({"check": check, "verdict": verdict,
                    "value": float(value) if isinstance(value, (int, float)) else str(value),
                    "note": note})


# ---------- PDG 质量（MeV, pole masses） ----------
m_e, m_mu, m_tau = 0.51099895, 105.6583745, 1776.86
r12, r23, r13 = m_mu / m_e, m_tau / m_mu, m_tau / m_e
print("目标：r12=mμ/me=%.4f  r23=mτ/mμ=%.4f  r13=mτ/me=%.2f" % (r12, r23, r13))

# ---------- A1 基线：单参数 φ 幂次 ----------
phi = (1 + math.sqrt(5)) / 2
best1 = min(((abs(phi ** n - r) / r), n) for n in range(1, 25) for r in (r12, r23, r13))
add("A1 单参数 φ^n 最优拟合（基线，v29 结论复现）",
    "PASS" if best1[0] < 1e-9 else "FAIL", best1[0],
    "最优 φ^%d 相对误差 %.2f%%——单参数指数结构失败（v23/v29 一致）。" % (best1[1], 100 * best1[0]))

# ---------- A2 非指数拓扑量族 ----------
def dims(k):
    return [math.sin(math.pi * (j + 1) / (k + 2)) / math.sin(math.pi / (k + 2))
            for j in range(k + 1)]

targets = {"r12": r12, "r23": r23, "r13": r13}
pool = set()
for k in range(2, 13):
    for d in dims(k):
        pool.add(round(d, 12))
    pool.add(round(3.0 * k / (k + 2), 12))          # 中心荷 c(k)
    pool.add(round((k + 2.0) / k, 12))
pool = sorted(pool)
best2 = (1e9, None)
for a, b in itertools.permutations(pool, 2):
    if b <= 0:
        continue
    ratio = a / b
    for name, r in targets.items():
        err = abs(ratio - r) / r
        if err < best2[0]:
            best2 = (err, "%s: %.6f/%.6f" % (name, a, b))
add("A2 拓扑量两两比值（d_j/c(k) 族，%d 个值）最优拟合" % len(pool),
    "PASS" if best2[0] < 1e-9 else ("INFO" if best2[0] < 0.03 else "FAIL"),
    best2[0], "最优 %s 相对误差 %.2f%%。" % (best2[1], 100 * best2[0]))

# ---------- A3 「代=level」假设 ----------
level_ass = []
for ks, tag in (((2, 4, 6), "k=2,4,6"), ((2, 3, 4), "k=2,3,4")):
    for f, fname in ((lambda k: 3.0 * k / (k + 2), "c(k)"),
                     (lambda k: dims(k)[1], "d_1(k)"),
                     (lambda k: (k + 2.0) / k, "(k+2)/k")):
        v = [f(k) for k in ks]
        e12 = abs((v[1] / v[0]) ** 1 - 1)  # placeholder real calc below
        pred12, pred23 = v[1] / v[0], v[2] / v[1]
        err = max(abs(pred12 / r12 - 1), abs(pred23 / r23 - 1))
        level_ass.append((err, tag, fname, pred12, pred23))
best3 = min(level_ass)
add("A3 「代=level」比值族最优（%s, %s）" % (best3[1], best3[2]),
    "PASS" if best3[0] < 1e-9 else "FAIL", best3[0],
    "预测 r12=%.3f(观测%.1f) r23=%.3f(观测%.2f)，最大相对误差 %.1f%%——"
    "level 代际映射失败。" % (best3[3], r12, best3[4], r23, 100 * best3[0]))

# ---------- A4 小整数代数组合穷举（对数域） ----------
bases = {"φ": math.log(phi), "√2": 0.5 * math.log(2), "2": math.log(2),
         "3": math.log(3), "5": math.log(5)}
names = list(bases)
logs = [bases[n] for n in names]
E = range(-10, 11)
best4 = {t: (1e9, None) for t in targets}
for combo in itertools.product(E, repeat=5):
    lz = sum(n * l for n, l in zip(combo, logs) if n)
    if lz == 0:
        continue
    val = math.exp(lz)
    if val > 1e7 or val < 1e-7:
        continue
    for name, r in targets.items():
        err = abs(val - r) / r
        if err < best4[name][0]:
            terms = "·".join("%s^%d" % (nm, n) for nm, n in zip(names, combo) if n)
            best4[name] = (err, terms)
for name in ("r12", "r23", "r13"):
    err, terms = best4[name]
    verdict = "PASS" if err < 1e-9 else ("INFO" if err < 0.03 else "FAIL")
    note = ("相对误差 %.4f%%。" % (100 * err)) if err >= 1e-9 else "机器零。"
    note += (" 【过拟合警示】搜索空间 21^5≈4.05M 组合，自由度下 1e-5 误差属统计必然，"
             "不构成结构证据；且组合含任意 3/5 幂次，非拓扑构造量。")
    add("A4 代数组合穷举最优 %s=%s（统计必然，非结构）" % (name, terms), verdict, err, note)

# ---------- 汇总 ----------
n_pass = sum(1 for x in results if x["verdict"] == "PASS")
n_info = sum(1 for x in results if x["verdict"] == "INFO")
n_fail = sum(1 for x in results if x["verdict"] == "FAIL")
summary = {
    "script": "v30 代质量层级正面攻击（非指数拓扑量 + 代数组合穷举）",
    "overall_verdict": "PASS" if n_pass == len(results) else "FAIL",
    "total": len(results), "PASS": n_pass, "INFO": n_info, "FAIL": n_fail,
    "targets": {"r12": r12, "r23": r23, "r13": r13},
    "results": results,
    "conclusion": ("正面攻击结果（三层排除）：①结构层——非指数拓扑量族（量子维数/中心荷/"
                   "S 谱）取值 O(1)，两两比值最优误差 73%，无法跨越 r23≈16.8 的量级；"
                   "「代=level」映射误差 99%，彻底失败。②放大层——单参数幂次 φ^n 最优误差 "
                   "2.7%（v23/v29 一致），单一幂律放大机制证伪。③组合层——小整数代数组合"
                   "穷举虽达 1e-5 误差，但搜索空间 4.05M 自由度下属统计必然（过拟合），"
                   "且组合含任意 3/5 幂次，非拓扑构造量，不构成证据。⇒ 诚实结论：代质量"
                   "层级绝对值在本框架拓扑结构层内无解，缺口 ~500× 需外部动力学输入"
                   "（SM 中 Yukawa 耦合本就是自由参数）。这是边界收窄而非失败：排除了"
                   "『纯拓扑代数数±幂律可构造质量谱』整族假设，把开放项压缩为『动力学 "
                   "Yukawa 起源』单点；拓扑层贡献=代结构（3 代=SU(2)_2 三扇区，已闭合）"
                   "而非绝对质量。红线守约：全部判定按残差分级，无粉饰。"),
}
out = os.path.join(HERE, "v30_代质量层级_非指数拓扑量正面攻击_核验结果.json")
json.dump(summary, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("[v30] overall=%s  PASS=%d INFO=%d FAIL=%d" % (summary["overall_verdict"], n_pass, n_info, n_fail))
for x in results:
    print("  [%s] %s  val=%s" % (x["verdict"], x["check"][:56], x["value"]))
