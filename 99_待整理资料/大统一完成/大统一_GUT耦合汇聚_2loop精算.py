# -*- coding: utf-8 -*-
"""
================================================================================
大统一完成 · GUT 耦合常数汇聚 · 2-loop 精算 + 突破目标反解
================================================================================
主题：99_待整理资料/大统一完成
方法：求导证明验证精算分析修复突破（延续 TUFT-R11/R12 的 GUT 判据）

目标：
  (A) 精算升级：把 R11 的 1-loop RGE 升级到 2-loop（RK4 积分），
      内置自验证（MSSM 必须给出 M_GUT~2e16 GeV, a_GUT^{-1}~24），
      证明「SM 三耦合不汇聚」不是 1-loop 近似假象（修复 R11 最弱环节）。
  (B) 突破目标反解：在 1-loop 闭式下，给定新物理扇区贡献的 β 偏移 (db1,db2,db3)，
      反解「三耦合在单一能标汇聚」所需的 db3 与对应 M_GUT / a_GUT^{-1}；
      扫描 (db1,db2) 全景观，标出 MSSM 参考点。
  (C) 诚实结论：TUFT（R12）确认不提供任何新态 => 无法供给所需 db => 大统一在
      TUFT 框架内不成立（O-GUT 仍开放）；给出可证伪的精确 β 要求。

约定（与 R11 一致，已自验证）：
  1/a_i(μ) = 1/a_i(M_Z) - (b_i/2π)·ln(μ/M_Z)    （1-loop，b 取下方向量）
  a_i = g_i^2/(16π^2) = α_i/(4π)
  da_i/dt = 2 b_i a_i^2 + 2 Σ_j b_ij a_i^2 a_j    （2-loop，t=ln(μ/GeV)）
  β(g_i) = g_i^3/(16π^2)[ b_i + (1/(16π^2)) Σ_j b_ij g_j^2 ]   （标准 M-V 约定）

红线：耦合汇聚是经典已知结论，本册只做独立精算与 TUFT 语境下的诚实组织，
      **不宣称 TUFT 据此实现大统一**。
================================================================================
"""
import os
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "大统一_GUT耦合汇聚_2loop精算_report.txt")

OUT = []


def sec(t):
    OUT.append("\n" + "=" * 78)
    OUT.append("  " + t)
    OUT.append("=" * 78)


def put(s=""):
    OUT.append(s)


def P(name, detail):
    OUT.append("  [PASS] %s  |  %s" % (name, detail))


def F(name, detail):
    OUT.append("  [FAIL] %s  |  %s" % (name, detail))


def B(name, detail):
    OUT.append("  [BOUNDARY] %s  |  %s" % (name, detail))


def I(name, detail):
    OUT.append("  [INFO] %s  |  %s" % (name, detail))


# ───────────────────────── 物理常数与 SM 输入 ─────────────────────────
MZ = 91.1876  # GeV
ALPHA_EM_INV = 127.951
SIN2W = 0.23121
ALPHA_S = 0.1180

# GUT 归一化超荷：α_1 = (5/3)·α_em/(1 - sin²θ_W)
a1_0 = (5.0 / 3.0) * (1.0 / ALPHA_EM_INV) / (1.0 - SIN2W) / (4.0 * math.pi)
a2_0 = (1.0 / ALPHA_EM_INV) / SIN2W / (4.0 * math.pi)
a3_0 = ALPHA_S / (4.0 * math.pi)
A1_0 = 1.0 / (4.0 * math.pi * a1_0)  # 1/α_1(M_Z)（注意：非 1/a_i，后者 = 4π/α_i）
A2_0 = 1.0 / (4.0 * math.pi * a2_0)
A3_0 = 1.0 / (4.0 * math.pi * a3_0)

# 1-loop β 系数（与 R11 一致：b_SM=(41/10, -19/6, -7), b_MSSM=(33/5,1,-3)）
B_SM = (41.0 / 10.0, -19.0 / 6.0, -7.0)
B_MSSM = (33.0 / 5.0, 1.0, -3.0)

# 2-loop β 矩阵 b_ij（M-V，GUT 归一化 U(1)）
B2_SM = (
    (199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0),
    (9.0 / 10.0, 35.0 / 6.0, 12.0),
    (11.0 / 10.0, 9.0 / 2.0, -26.0 / 3.0),
)
B2_MSSM = (
    (199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0),
    (9.0 / 5.0, 35.0, 24.0),
    (11.0 / 5.0, 9.0, -14.0),
)


def deriv(t, a, b, b2):
    """da_i/dt = 2 b_i a_i^2 + 2 Σ_j b_ij a_i^2 a_j  （t = ln(μ/GeV)）"""
    da = [0.0, 0.0, 0.0]
    for i in range(3):
        s = 2.0 * b[i] * a[i] * a[i]
        cross = 0.0
        for j in range(3):
            cross += b2[i][j] * a[j]
        s += 2.0 * a[i] * a[i] * cross
        da[i] = s
    return da


def rk4_step(t, a, h, b, b2):
    k1 = deriv(t, a, b, b2)
    a2 = [a[i] + h / 2.0 * k1[i] for i in range(3)]
    k2 = deriv(t + h / 2.0, a2, b, b2)
    a3 = [a[i] + h / 2.0 * k2[i] for i in range(3)]
    k3 = deriv(t + h / 2.0, a3, b, b2)
    a4 = [a[i] + h * k3[i] for i in range(3)]
    k4 = deriv(t + h, a4, b, b2)
    return [a[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3)]


def one_loop_gut(b):
    """1-loop 闭式：返回 (ΔL, M_GUT, a_GUT_inv)。"""
    L12 = 2 * math.pi * (A1_0 - A2_0) / (b[0] - b[1])
    L23 = 2 * math.pi * (A2_0 - A3_0) / (b[1] - b[2])
    L13 = 2 * math.pi * (A1_0 - A3_0) / (b[0] - b[2])
    vals = [L12, L23, L13]
    dL = max(vals) - min(vals)
    Lstar = (L12 + L23 + L13) / 3.0
    M_GUT = MZ * math.exp(Lstar)
    aG = A1_0 - (b[0] / (2 * math.pi)) * Lstar
    return dL, M_GUT, aG


def two_loop_gut(b, b2, mu_max=1e17):
    """2-loop RK4 积分，找三耦合 1/α 曲线的最近交点。"""
    t0 = math.log(MZ)
    t1 = math.log(mu_max)
    a = [a1_0, a2_0, a3_0]
    N = 5000
    h = (t1 - t0) / N
    inv = [[1.0 / (4 * math.pi * a[0])], [1.0 / (4 * math.pi * a[1])],
           [1.0 / (4 * math.pi * a[2])]]
    ts = [t0]
    for k in range(N):
        a = rk4_step(t0 + k * h, a, h, b, b2)
        ts.append(t0 + (k + 1) * h)
        inv[0].append(1.0 / (4 * math.pi * a[0]))
        inv[1].append(1.0 / (4 * math.pi * a[1]))
        inv[2].append(1.0 / (4 * math.pi * a[2]))
    best = None
    for k in range(1, N):
        v = [inv[0][k], inv[1][k], inv[2][k]]
        if any(x <= 0 for x in v):
            continue
        spread = max(v) - min(v)
        if best is None or spread < best[0]:
            best = (spread, ts[k], v)
    if best is None:
        return None
    return best[0], math.exp(best[1]), sum(best[2]) / 3.0


def required_db3(db1, db2, b=B_SM):
    """给定新扇区贡献 db1,db2，反解使三耦合在单一尺度汇聚所需的 db3。
    返回 (Lstar, M_GUT, a_GUT_inv, db3) 或 None。"""
    d1 = (b[0] + db1) - (b[1] + db2)
    if abs(d1) < 1e-12:
        return None
    R = 2 * math.pi * (A1_0 - A2_0) / d1  # 统一尺度 L*
    if R <= 0 or R > 80 or R < -80:
        return None
    Lstar = R
    # 要求 f2(L*) = f3(L*)
    target = (A2_0 - A3_0) / R  # 应等于 ((b2+db2)-(b3+db3))/2π
    # (b2+db2) - (b3+db3) = 2π·target
    db3 = (b[1] + db2) - 2 * math.pi * target - b[2]
    if not (-80 < Lstar < 80):
        return None
    M_GUT = MZ * math.exp(Lstar)
    aG = A1_0 - ((b[0] + db1) / (2 * math.pi)) * Lstar
    return Lstar, M_GUT, aG, db3


def main():
    sec("大统一完成 · GUT 耦合汇聚 · 2-loop 精算 + 突破目标反解")
    n_pass = n_fail = n_bnd = n_info = 0

    put("  输入（M_Z 标度）：α_em^{-1}=%.3f, sin²θ_W=%.5f, α_s=%.4f"
        % (ALPHA_EM_INV, SIN2W, ALPHA_S))
    put("  a_i(M_Z)=α_i/(4π)：a1=%.6e, a2=%.6e, a3=%.6e" % (a1_0, a2_0, a3_0))
    put("  1/α_i(M_Z) = %.4f, %.4f, %.4f" % (A1_0, A2_0, A3_0))

    # ═══════ (A) 1-loop 基准（与 R11 对齐） ═══════
    sec("A. 1-loop 基准（对齐 R11）")
    dL_sm, MG_sm, aG_sm = one_loop_gut(B_SM)
    dL_ms, MG_ms, aG_ms = one_loop_gut(B_MSSM)
    put("  SM   : ΔL = %.3f  => 能标比 e^ΔL = %.3e  (不汇聚)" % (dL_sm, math.exp(dL_sm)))
    put("  MSSM : ΔL = %.4f  => M_GUT = %.3e GeV, α_GUT^{-1} = %.2f (汇聚)"
        % (dL_ms, MG_ms, aG_ms))
    if dL_sm > 5:
        P("A1: SM 1-loop 三耦合不汇聚（ΔL=%.2f）" % dL_sm,
          "与 R11 一致：交点跨越 %.1e 倍能标，最小 SM 无大统一" % math.exp(dL_sm))
        n_pass += 1
    else:
        F("A1: SM 1-loop", "ΔL=%.2f 异常" % dL_sm)
        n_fail += 1
    if dL_ms < 0.5 and 1e15 < MG_ms < 1e17:
        P("A2: MSSM 1-loop 汇聚（M_GUT≈%.2e GeV, α_GUT^{-1}≈%.1f）" % (MG_ms, aG_ms),
          "与已知 MSSM 大统一一致（代价：引入超对称）")
        n_pass += 1
    else:
        F("A2: MSSM 1-loop", "ΔL=%.4f, MG=%.2e 异常" % (dL_ms, MG_ms))
        n_fail += 1

    # ═══════ (B) 2-loop 精算升级 + 自验证 ═══════
    sec("B. 2-loop 精算升级（RK4 积分）+ 自验证")
    res_sm = two_loop_gut(B_SM, B2_SM)
    res_ms = two_loop_gut(B_MSSM, B2_MSSM)
    if res_sm is None:
        F("B1: SM 2-loop", "无物理交点")
        n_fail += 1
    else:
        dL_sm2, MG_sm2, aG_sm2 = res_sm
        put("  SM   2-loop: 最近汇聚点 ΔL=%.3f, M@min-spread=%.3e GeV, α_GUT^{-1}=%.2f"
            % (dL_sm2, MG_sm2, aG_sm2))
        if dL_sm2 > 3:
            P("B1: SM 2-loop 仍不汇聚（ΔL=%.2f）" % dL_sm2,
              "2-loop 修正未改变『SM 不汇聚』结论 => R11 的 1-loop 判定**稳健**，"
              "非近似假象（修复 R11 最弱环节）")
            n_pass += 1
        else:
            B("B1: SM 2-loop 汇聚性存疑", "ΔL=%.2f 偏离预期大值" % dL_sm2)
            n_bnd += 1
    if res_ms is None:
        F("B2: MSSM 2-loop 自验证", "无物理交点")
        n_fail += 1
    else:
        dL_ms2, MG_ms2, aG_ms2 = res_ms
        put("  MSSM 2-loop: 最近汇聚点 ΔL=%.4f, M_GUT=%.3e GeV, α_GUT^{-1}=%.2f"
            % (dL_ms2, MG_ms2, aG_ms2))
        # 自验证：MSSM 2-loop 必须给 M_GUT ∈ [1e16,3e16], α_GUT^{-1} ∈ [18,30]
        if 1e16 <= MG_ms2 <= 3e16 and 18 <= aG_ms2 <= 30:
            P("B2: MSSM 2-loop 自验证通过",
              "M_GUT=%.2e GeV, α_GUT^{-1}=%.1f —— 与文献 MSSM 大统一值一致，"
              "证明本册 2-loop 积分器与 β 系数正确" % (MG_ms2, aG_ms2))
            n_pass += 1
        else:
            B("B2: MSSM 2-loop 自验证偏移",
              "M_GUT=%.2e, α_GUT^{-1}=%.1f，超出典型区间——2-loop 系数需复核"
              % (MG_ms2, aG_ms2))
            n_bnd += 1
        # 2-loop 修正量级（统一尺度是积分效应，M_GUT 偏移可比 % 级大）
        shift_MG = (MG_ms2 - MG_ms) / MG_ms
        shift_aG = (aG_ms2 - aG_ms) / aG_ms
        I("B3: 2-loop 修正量级",
          "M_GUT 相对 1-loop 偏移 %+.1f%%, α_GUT^{-1} 偏移 %+.1f%% —— 耦合自身为 %% 级微扰，"
          "M_GUT 因积分效应偏移更大；但定性结论（MSSM 汇聚、SM 不汇聚）不变"
          % (100 * shift_MG, 100 * shift_aG))
        n_info += 1

    # ═══════ (C) 突破目标反解：required Δb 景观 ═══════
    sec("C. 突破目标反解：新物理扇区必须提供的 β 偏移")
    put("  设新扇区把 SM 的 β 改为 b_i+Δb_i；三耦合在单一尺度汇聚要求")
    put("  1/α_1(M_Z)-((b1+Δb1)/2π)L = 1/α_2-((b2+Δb2)/2π)L = 1/α_3-((b3+Δb3)/2π)L。")
    put("  给定 (Δb1,Δb2)，可闭式反解所需 Δb3 与 M_GUT / α_GUT^{-1}。")
    put("")

    # MSSM 参考点：MSSM 相对 SM 的增量 Δb
    db_mssm = (B_MSSM[0] - B_SM[0], B_MSSM[1] - B_SM[1], B_MSSM[2] - B_SM[2])
    put("  MSSM 参考点（相对 SM 的 Δb）= (%.3f, %.3f, %.3f)" % db_mssm)
    r_mssm = required_db3(db_mssm[0], db_mssm[1], B_SM)
    if r_mssm:
        Ls, MG, aG, db3 = r_mssm
        put("    => 反解得 Δb3=%.3f, 统一尺度 M_GUT=%.3e GeV, α_GUT^{-1}=%.2f"
            % (db3, MG, aG))
        if abs(db3 - db_mssm[2]) < 0.2 and 1e15 < MG < 1e17:
            P("C1: 反解自洽",
              "用 MSSM 的 (Δb1,Δb2) 反解得 Δb3=%.3f，与 MSSM 真实 Δb3=%.3f 一致"
              " => 反解器正确；统一尺度落在 GUT 区间" % (db3, db_mssm[2]))
            n_pass += 1
        else:
            B("C1: 反解与 MSSM 偏差", "Δb3=%.3f vs %.3f" % (db3, db_mssm[2]))
            n_bnd += 1

    # 扫描景观：Δb1,Δb2 ∈ [-2, +6]，找使 M_GUT∈[1e15,1e17] 且 α_GUT^{-1}∈[3,40] 的点
    put("")
    put("  扫描 (Δb1,Δb2) 网格，列出可汇聚（物理）的新扇区要求：")
    grid = []
    for db1 in [x * 0.5 for x in range(-4, 13)]:   # -2 .. 6
        for db2 in [x * 0.5 for x in range(-4, 13)]:
            r = required_db3(db1, db2, B_SM)
            if not r:
                continue
            Ls, MG, aG, db3 = r
            if 1e15 <= MG <= 1e17 and 3.0 <= aG <= 40.0:
                grid.append((db1, db2, db3, MG, aG))
    put("    找到 %d 个物理可汇聚扇区（Δb1,Δb2,Δb3,M_GUT[GeV],α_GUT^{-1}）：" % len(grid))
    # 取代表性几行
    shown = 0
    for db1, db2, db3, MG, aG in grid:
        if shown < 12 or (abs(db1 - db_mssm[0]) < 0.01 and abs(db2 - db_mssm[1]) < 0.01):
            put("    Δb=(%+4.1f, %+4.1f, %+6.2f)  M_GUT=%.2e  α_GUT^{-1}=%.1f"
                % (db1, db2, db3, MG, aG))
            shown += 1
    if len(grid) > 0:
        P("C2: 可汇聚新扇区存在（非唯一）",
          "扫描得 %d 个物理 (Δb1,Δb2,Δb3) 组合能使三耦合在 10^15-10^17 GeV 汇聚；"
          "统一尺度对 β 偏移高度敏感（连续族），符合 R12『单一表示无法唯一确定』。"
          % len(grid))
        n_pass += 1
    else:
        F("C2: 无物理可汇聚扇区", "扫描为空，需放宽范围")
        n_fail += 1

    # ═══════ (D) 诚实结论：TUFT 能否供给所需 Δb？ ═══════
    sec("D. 诚实结论：TUFT 在大统一框架内的地位")
    put("  TUFT（R12『大统一缺口反解』）结论：")
    put("    · TUFT 未提供任何新粒子态（O-NEWSTATE 开放）——结世界线 (Lk,κ,τ)")
    put("      中无规范表示激发，故 Δb_TUFT = (0, 0, 0)。")
    put("    · 由 (C) 的反解，Δb=(0,0,0) 恰为 SM 点，对应 ΔL≈%.1f（不汇聚）。" % dL_sm)
    put("    · 要使三耦合汇聚，新扇区必须提供 |Δb|~O(1) 的偏移（MSSM 点 Δb=(%.1f,%.1f,%.1f)），"
        % (db_mssm[0], db_mssm[1], db_mssm[2]))
    put("      而 TUFT 框架内无任何来源产生这种偏移。")
    F("D1: 【诚实】TUFT 框架内无法实现大统一（耦合汇聚）",
      "Δb_TUFT=(0,0,0) 落在『不汇聚』的 SM 区；O-GUT 仍开放。"
      "TUFT 若声称大统一，必须先引入外部新扇区（如超对称或特定 GUT 多重态）供给 |Δb|~O(1) 偏移。")
    n_fail += 1
    B("D2: 可证伪的精确要求（入库触发候选）",
      "任何声称在 TUFT 内实现大统一的提案，必须给出一组合 Δb=(Δb1,Δb2,Δb3) 使"
      "三耦合在单尺度汇聚且 M_GUT∈[1e15,1e17] GeV、α_GUT^{-1}∈[3,40]；"
      "否则即不满足 UFT-3 判定。这是可证伪的精确门槛。")
    n_bnd += 1
    I("D3", "本册未粉饰：2-loop 精算只强化了『SM 不汇聚、MSSM 汇聚』这一经典结论，"
            "并把『TUFT 缺新态 ⇒ 不能大统一』从定性升级为带精确 β 门槛的定量判据。")
    n_info += 1

    sec("E. 判定汇总")
    sm2 = ("ΔL=%.2f, M@min-spread=%.2e, α_GUT^{-1}=%.1f"
           % (res_sm[0], res_sm[1], res_sm[2])) if res_sm else "None"
    ms2 = ("M_GUT=%.2e, α_GUT^{-1}=%.1f"
           % (res_ms[1], res_ms[2])) if res_ms else "None"
    put("  [SM]   1-loop ΔL=%.2f（不汇聚）；2-loop %s（仍不汇聚）" % (dL_sm, sm2))
    put("  [MSSM] 1-loop M_GUT=%.2e, α_GUT^{-1}=%.1f；2-loop %s" % (MG_ms, aG_ms, ms2))
    put("  汇总：PASS=%d / FAIL=%d / BOUNDARY=%d / INFO=%d"
        % (n_pass, n_fail, n_bnd, n_info))
    put("  红线：数学自洽 ≠ 实验证实；本册为独立精算与 TUFT 语境下的诚实组织。")

    txt = "\n".join(OUT) + "\n"
    print(txt)
    try:
        with open(REPORT, "w", encoding="utf-8") as fh:
            fh.write(txt)
        print("[报告已写入] " + REPORT)
    except Exception as exc:
        print("[warn] " + str(exc))


if __name__ == "__main__":
    main()
