# -*- coding: utf-8 -*-
"""
================================================================================
TUFT V3.2  EL-约定核对：源稿字面 ODE 与其所列 E0 是否互为一对欧拉-拉格朗日方程
================================================================================

背景：源稿「电子拟合 chi2/解析梯度/SLSQP 全链路」同时给出
  (方程)  -psi'' - (2/r)psi' = V1 psi^3 - V2 psi^5        ... 记 U'(psi) := 右端
  (能量)  E0 = int 4pi r^2 [ 1/2 psi'^2 + V1/4 psi^4 - V2/6 psi^6 ] dr
本工具不假设谁对谁错，只测：
  [S1] 两个约定分支各自积分，比较尾形状与 N(R) 发散率；
  [S2] 用**弱形式变分残差**判哪一支是 E0 的驻点：
         dE0[eta] = int 4pi r^2 [ psi' eta' + U'(psi) eta ] dr
       只需一阶导数（psi' 由 RK45 稠密输出解析给出，eta 用闭式紧致支撑函数），
       psi_s 为 E0 驻点 <=> 对一切 eta 有 dE0[eta]=0。
       理论预期：EL 支恒 0、字面支 = int 4pi r^2 * 2U' * eta（与非线性块同阶）。
  [S3] 复现已落盘运行记录 tuft_v32_electron_fit_report.txt 的 [C] 表（逐值 1% 内），
       从而把"平台 sqrt(V1/V2) + R^3 发散"这句机理文字归属到它**真正量到的那一支**。
  [S5] 分支归属不靠人读代码：正则现读 07_计算复现/源码/tuft_v32_electron_fit_slsqp.py
       的 ddpsi 行取符号，再与 [S2] 判出的驻点支比对。
  [S4] 三枚变异体（判据必须打红；本工具自己造"错法"再看闸门是否拦住）：
       M1 substitution —— 把"剖面是否满足它自己被积分的那条方程"当验算：两支同时为 0
                          （且残差按 h^2 收缩 = 差分截断误差而非物理量）=> 该通道无牙，
                          本工具因此不采用它；同一网格上改用**对方**方程作残余，两支同时
                          精确给出 2.000 => 有判别力的必须是"配的是哪条方程"。
       M2 label-swap   —— 交换两支标签后判据必须翻转；
       M3 pairing-flip  —— 把 E0 的势能项整体反号（= 方程与能量配错对）。S2 的残差表必须是
                          一张 2x2 且**对角互换**：反号后字面支变成驻点、EL 支失去驻点性，
                          证明 S2 测的是「方程 <-> 能量」这一**配对**，而不是方程本身。
退出码：任一 chk 失败 -> 3。

红线：只判"约定/机理归属"与 C0037 前提的适用范围；不重判 C0039 的结论
     （两支都无有限 N），也不评价并行会话在飞的 massfix 文件。
================================================================================
"""
import os
import re
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp

TRAPZ = getattr(np, 'trapezoid', np.trapz)
HERE = os.path.dirname(os.path.abspath(__file__))
S14 = os.path.abspath(os.path.join(HERE, '..', '..'))
REPO_SCRIPT = os.path.join(S14, '07_计算复现', '源码', 'tuft_v32_electron_fit_slsqp.py')
LANDED_REPORT = os.path.join(S14, '09_验证结果', '原始运行记录', 'tuft_v32_electron_fit_report.txt')
OUT_TXT = os.path.join(S14, '09_验证结果', '原始运行记录', 'tuft_v32_el_convention_report.txt')

V1, V2, PSI0 = 1.2, 0.4, 0.75
R_END = 2000.0
Up = lambda p: V1 * p ** 3 - V2 * p ** 5
SQRT_RATIO = (V1 / V2) ** 0.5
R_LO, R_HI = 5.0, 200.0
NQ = 200001


def integrate(s, r_end=R_END, step=0.05):
    """psi'' = -(2/r)psi' + s*U'(psi)。s=-1 -> 源稿字面支；s=+1 -> E0 的 EL 支。"""
    def f(t, y):
        psi, dpsi = y
        if t < 1e-9:
            return [dpsi, 0.0]
        return [dpsi, -(2.0 / t) * dpsi + s * Up(psi)]
    return solve_ivp(f, (1e-9, r_end), [PSI0, 0.0], method='RK45', rtol=1e-11,
                     atol=1e-13, dense_output=True, max_step=step)


def N_of(sol, R, n=NQ // 6):
    rr = np.linspace(1e-9, R, n)
    return float(TRAPZ(4 * np.pi * rr ** 2 * sol.sol(rr)[0] ** 2, rr))


def etas(k):
    """k 个紧致支撑于 (R_LO,R_HI) 的独立检验函数（及其一阶导，闭式）。"""
    L = R_HI - R_LO
    out = []
    for n in range(1, k + 1):
        out.append((lambda r, n=n: np.sin(n * np.pi * (r - R_LO) / L),
                    lambda r, n=n: (n * np.pi / L) * np.cos(n * np.pi * (r - R_LO) / L)))
    return out


def weak_residual(sol, k=5, sig=+1.0):
    """返回每个 eta 的 |dE0[eta]| / (int 4pi r^2 |U'| |eta| dr)（无量纲残差比）。
    sig=-1 是 M3 变异体：把能量里的势能项整体反号（即源稿那种"方程与能量配错一对"），
    判据必须随之翻转 —— 证明 S2 测的是「方程 <-> 能量」的配对，而非方程本身。"""
    rr = np.linspace(R_LO, R_HI, NQ)
    psi, dpsi = sol.sol(rr)[0], sol.sol(rr)[1]
    upsi = Up(psi)
    w = 4 * np.pi * rr ** 2
    denom_base = TRAPZ(w * np.abs(upsi), rr)
    ratios = []
    for eta_f, deta_f in etas(k):
        eta, deta = eta_f(rr), deta_f(rr)
        num = TRAPZ(w * (dpsi * deta + sig * upsi * eta), rr)
        den = TRAPZ(w * np.abs(upsi) * np.abs(eta), rr)
        ratios.append(abs(num) / max(den, 1e-300))
    return ratios, float(denom_base)


def strong_residual(sol, s_chk, h, r_lo=R_LO, r_hi=R_HI, n=20001):
    """强残差 max|psi'' + (2/r)psi' - s_chk*U'(psi)| / max|U'(psi)|，psi'' 用稠密输出
    一阶导的中心差分（步长 h）近似。s_chk=sol 自己那条方程 -> 恒等式；s_chk=对方方程 -> 真剩余。"""
    rr = np.linspace(r_lo, r_hi, n)
    psi, dpsi = sol.sol(rr)[0], sol.sol(rr)[1]
    d2 = (sol.sol(rr + h)[1] - sol.sol(rr - h)[1]) / (2.0 * h)
    G = d2 + (2.0 / rr) * dpsi - s_chk * Up(psi)
    return float(np.max(np.abs(G))) / float(np.max(np.abs(Up(psi))))


def main():
    t0 = time.time()
    out = []
    fails = []
    nchk = [0]

    def emit(s=''):
        out.append(s)
        print(s)

    def chk(cond, name, detail):
        nchk[0] += 1
        emit("    [%s] %-46s %s" % ('OK  ' if cond else 'FAIL', name, detail))
        if not cond:
            fails.append(name)

    emit("=" * 78)
    emit("TUFT V3.2 EL-约定核对  原始运行记录")
    emit("  V1=%.1f V2=%.1f psi0=%.2f  r_end=%.0f  scipy RK45 rtol=1e-11 max_step=0.05" % (V1, V2, PSI0, R_END))
    emit("  sqrt(V1/V2) = %.6f   残差窗口 eta 支撑于 (%.0f,%.0f), 网格 %d 点" % (SQRT_RATIO, R_LO, R_HI, NQ))
    emit("=" * 78)

    sols = {s: integrate(s) for s in (-1.0, +1.0)}

    emit("\n[S1] 两支尾形状与 N(R) 发散率（先不下结论）")
    for s in (-1.0, +1.0):
        cells = ["r=%4.0f: psi=%+.4e psi*r=%+.4e" % (r, sols[s].sol(r)[0], sols[s].sol(r)[0] * r)
                 for r in (50.0, 200.0, 800.0, 2000.0)]
        emit("  s=%+d  (grad2 psi = %s U')" % (s, '-' if s < 0 else '+'))
        emit("        " + "\n        ".join(cells))
        Rs = (100.0, 200.0, 400.0, 800.0)
        Ns = [N_of(sols[s], R) for R in Rs]
        emit("        N(R): " + "  ".join("R=%d:%.4e" % (R, N) for R, N in zip(Rs, Ns)))
        emit("        R 翻倍时 N 增长比 = " + "  ".join("x%.3f" % (Ns[i + 1] / Ns[i]) for i in range(3))
             + "   (1.0=收敛 | ~2=线性(1/r 尾) | ~8=立方(非零平台))")

    emit("\n[S2] 弱形式变分残差 |dE0[eta]| / int 4pi r^2 |U'||eta|（5 个独立 eta）")
    ratios = {}
    for s in (-1.0, +1.0):
        rs, _ = weak_residual(sols[s])
        ratios[s] = rs
        emit("  s=%+d : " % s + "  ".join("%.3e" % x for x in rs))
    med = {s: float(np.median(ratios[s])) for s in (-1.0, +1.0)}
    stat_s = min(med, key=lambda k: med[k])
    nonstat_s = max(med, key=lambda k: med[k])
    emit("  [读数] 驻点支（残差比中位数）s=%+d : %.3e   非驻点支 s=%+d : %.3e"
         % (stat_s, med[stat_s], nonstat_s, med[nonstat_s]))
    emit("  [对照] 非驻点支残差应趋于理论值 2（|dE0[eta]| -> |int 4pi r^2 2U' eta|）："
         "实测 %.3f" % med[nonstat_s])
    chk(med[stat_s] < 1e-4, 'S2 驻点支残差 < 1e-4', '%.3e' % med[stat_s])
    chk(med[nonstat_s] > 0.5, 'S2 非驻点支残差 > 0.5（与非线性块同阶）', '%.3e' % med[nonstat_s])
    chk(abs(med[nonstat_s] - 2.0) < 0.75, 'S2 非驻点支残差与理论值 2 同阶', 'theory=2.000 got=%.3f' % med[nonstat_s])
    chk(stat_s != nonstat_s, 'S2 两支被判为不同', 'stat=%+d' % stat_s)

    emit("\n[S3] 与已落盘 [C] 表对表（把机理文字归属到它量到的那一支）")
    if not os.path.isfile(LANDED_REPORT):
        chk(False, 'S3 落盘运行记录存在', LANDED_REPORT)
    else:
        txt = open(LANDED_REPORT, encoding='utf-8', errors='replace').read()
        tab = {}
        for m in re.finditer(r'R=\s*([\d.]+)\s+N\(R\)=\s*([\d.eE+\-]+)\s+E0\(R\)=\s*([\d.eE+\-]+)\s*psi\(R\)=([+\-][\d.]+)', txt):
            tab[float(m.group(1))] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
        emit("  从 %s 解析到 [C] 表 %d 行" % (os.path.basename(LANDED_REPORT), len(tab)))
        chk(len(tab) >= 3, 'S3 解析到 >=3 行', 'got=%d' % len(tab))
        matched = []
        for R in sorted(tab):
            mine = {s: N_of(sols[s], R) for s in (-1.0, +1.0)}
            best = min(mine, key=lambda k: abs(mine[k] / tab[R][0] - 1.0))
            rel = abs(mine[best] / tab[R][0] - 1.0)
            emit("    R=%-6.0f 落盘 N=%.5e | 本工具 s=%+d N=%.5e 相对差=%.2e | 落盘 psi=%+.4f 本工具 psi=%+.4f"
                 % (R, tab[R][0], best, mine[best], rel, tab[R][2], sols[best].sol(R)[0]))
            matched.append(best)
            chk(rel < 1e-2, 'S3 R=%.0f 复现在 1%% 内' % R, 'branch s=%+d' % best)
        chk(len(set(matched)) == 1, 'S3 各行归属同一支（无混支）', 'set=%s' % sorted(set(matched)))
        if matched:
            chk(matched[0] == stat_s,
                'S3 落盘 [C] 表所属支 == S2 判出的驻点支',
                'landed s=%+d, stationarity s=%+d' % (matched[0], stat_s))

    emit("\n[S4] 变异体（判据必须有牙）")
    emit("  M1 substitution（「剖面满足它自己被积分的那条方程」当验算 = 空通道；改用对方方程 = 有牙）")
    own, cross, shrink = {}, {}, []
    for s in (-1.0, +1.0):
        o1, o2 = strong_residual(sols[s], s, 1e-2), strong_residual(sols[s], s, 1e-3)
        own[s] = o2
        cross[s] = strong_residual(sols[s], -s, 1e-3)
        emit("    s=%+d  自身方程: h=1e-2 -> %.3e   h=1e-3 -> %.3e   （比值 %.1f ≈ 100 = h^2 截断误差，非物理量）"
             "   对方方程: %.6f" % (s, o1, o2, o1 / o2, cross[s]))
        shrink.append(o1 / o2)
    emit("    => 「代回式验算」对两支同时给出机器小量：它只证明了积分器没跑偏，"
         "证不了任何一支是 E0 的驻点 —— 故 S2 采用弱形式（对任意 eta 的残差）。")
    chk(max(own.values()) < 1e-5, 'M1 代回式对两支同时为机器小量（空通道已识别）',
        '%.1e/%.1e' % (own[-1.0], own[1.0]))
    chk(all(70.0 < x < 130.0 for x in shrink), 'M1 代回式按 h^2 收缩（是截断误差不是物理剩余）',
        'h2ratios=%s' % ['%.1f' % x for x in shrink])
    chk(min(cross.values()) > 1.9, 'M1 换成对方方程后残余必须显形（≈2 倍非线性块）',
        '%.4f/%.4f' % (cross[-1.0], cross[1.0]))
    NAME = {-1.0: 'literal-source(字面支)', +1.0: 'EL-of-E0(能量配套支)'}
    correct = {NAME[stat_s]: med[stat_s], NAME[nonstat_s]: med[nonstat_s]}
    v_correct = min(correct, key=lambda k: correct[k])
    mis = {NAME[stat_s]: med[nonstat_s], NAME[nonstat_s]: med[stat_s]}
    v_mis = min(mis, key=lambda k: mis[k])
    emit("  M2 label-swap（把两个读数错接到对方标签上）: 正确接线判出 %s；错接后判出 %s"
         % (v_correct, v_mis))
    chk(v_correct == NAME[stat_s] and v_mis == NAME[nonstat_s],
        'M2 判决只由实测比值携带（标签不自带结论）',
        'correct=%s mis=%s' % (v_correct, v_mis))
    emit("  M3 pairing-flip（把 E0 的势能项整体反号 sig=-1 = 方程与能量配错对）：2x2 残差比表")
    flip = {}
    for s in (-1.0, +1.0):
        rs, _ = weak_residual(sols[s], sig=-1.0)
        flip[s] = float(np.median(rs))
        emit("    s=%+d %-22s  sig=+1(所列 E0): %.3e   sig=-1(反号 E0): %.3e   倍率(sig=-1/sig=+1) x%.3e"
             % (s, NAME[s], med[s], flip[s], flip[s] / med[s]))
    emit("    => 反号后**驻点身份互换**：字面支残差比降到 %.1e（成为驻点），EL 支升到 %.1e（失去驻点性）；"
         % (flip[-1.0], flip[1.0]))
    emit("       故 S2 判的是「方程 <-> 能量」这一配对，不是方程本身。EL 支反号值 %.1e 未达理论上界 2，"
         % flip[1.0])
    emit("       是因为驻点剖面停在 U'~0 平台、U' 在支撑内变号相互抵消（同理字面支基线 %.3f<2，psi 过零）；"
         % med[-1.0])
    emit("       该量级差 6 个数量级已足够判决，判据按「配对互换」而非「达到 2」写。")
    chk(flip[-1.0] < 1e-4, 'M3 反号后字面支成为驻点（配对互换之左半）', '%.3e' % flip[-1.0])
    chk(flip[1.0] / med[1.0] > 1e3, 'M3 反号后 EL 支失去驻点性（放大 >1e3，配对互换之右半）',
        '%.3e/%.3e = x%.3e' % (flip[1.0], med[1.0], flip[1.0] / med[1.0]))

    emit("\n[S5] 仓库实现所属支由现读代码给出（不靠人读）")
    if not os.path.isfile(REPO_SCRIPT):
        chk(False, 'S5 仓库脚本存在', REPO_SCRIPT)
    else:
        src = open(REPO_SCRIPT, encoding='utf-8', errors='replace').read()
        m = re.search(r'ddpsi\s*=\s*-\s*\(2(?:\.0)?\s*/\s*\w+\)\s*\*\s*dpsi\s*([+\-])\s*V1\s*\*\s*psi\s*\*\*\s*3\s*([+\-])\s*V2\s*\*\s*psi\s*\*\*\s*5', src)
        if m is None:
            chk(False, 'S5 正则命中 ddpsi 行', 'miss')
        else:
            s_repo = -1.0 if m.group(1) == '-' else 1.0
            emit("  %s: V1 项号 %s、V2 项号 %s -> s_repo=%+d"
                 % (os.path.basename(REPO_SCRIPT), m.group(1), m.group(2), s_repo))
            chk(s_repo == stat_s, 'S5 仓库实现支 == S2 驻点支', 's_repo=%+d s_stat=%+d' % (s_repo, stat_s))
            emit("  [读数] 仓库修正版积分的是 E0 的 EL 支；源稿字面方程是另一支（差 2U'，"
                 "与分析文 §伴随 段所记 2(V1-V2 psi^2)psi^3 同值）。")

    emit("\n[判据汇总与归属]")
    Nseq = {s: [N_of(sols[s], R) for R in (100.0, 200.0, 400.0, 800.0)] for s in (-1.0, +1.0)}
    for s in (-1.0, +1.0):
        q = [Nseq[s][i + 1] / Nseq[s][i] for i in range(3)]
        emit("  s=%+d %-22s psi(200)=%+.4e psi(800)=%+.4e  N 翻倍比 = x%.2f x%.2f x%.2f  残差比=%.3e"
             % (s, NAME[s], sols[s].sol(200.0)[0], sols[s].sol(800.0)[0], q[0], q[1], q[2], med[s]))
    qL = [Nseq[-1.0][i + 1] / Nseq[-1.0][i] for i in range(3)]
    emit("  => 两支都无有限 N：EL 支为非零平台（R^3 发散，比值趋于 8）；字面支无平台（psi 过零、"
         "psi*r 不收敛），比值 x%.2f -> x%.2f -> x%.2f 逐档向 2 靠拢（1/r 尾带慢变修正、未收敛）。" % (qL[0], qL[1], qL[2])
         + " 既有 C0039 的结论不被推翻。")
    emit("  => 被订正的是「机理归属」与「前提范围」两件事：")
    emit("     (a) C0039 那句「平台 sqrt(V1/V2)+R^3」只在 EL 支（= 仓库实现支）上量到，"
         "源稿字面方程的尾不是平台；")
    emit("     (b) C0037 的包络定理前提「psi_s 是 E0 的驻点」只在 EL 支成立；源稿自身约定下该前提"
         "把整支残差丢掉（实测残差比 %.3f，理论 2.000）。" % med[nonstat_s])
    emit("\n运行总耗时 %.1f s" % (time.time() - t0))
    emit("自判：%d 项判据，失败 %d 项 -> %s" % (nchk[0], len(fails), 'PASS' if not fails else 'FAIL ' + ';'.join(fails)))

    lines = []
    for s in out:
        lines.extend(s.split("\n"))          # 版面统一 CRLF：行计数不因段前 \n 而与 CR 计数分叉
    text = "\r\n".join(lines) + "\r\n"
    with open(OUT_TXT, 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)
    return 3 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
