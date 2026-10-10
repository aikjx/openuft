# -*- coding: utf-8 -*-
"""attack16 probe3 · 味自由度秩计数（2026-10-10）

对象：OpenUFT v7.0 §2「味参数首原化」——声称
  「给定算符 Y_u,Y_d，9 个费米子质量（6 夸克+3 轻子）是其本征值，由谱定理唯一确定，无独立自由度」
  「CKM 的 4 参数 = Y_u,Y_d 两个算符本征标架之间的相对转动，算符给定则唯一」

做法：**不用闭式，直接数值算秩**。
把味群 U(3)^k 的李代数生成元作用到 Yukawa 矩阵上，构造「生成元 → Yukawa 变分」的线性映射，
用高斯消元（相对主元阈值 1e-14×max|row|，符合算法联盟体例 #3）求机器秩，
 物理自由度 = Yukawa 实参数数 − 机器秩。

诚实边界：本探针只做**计数**（算符携带多少自由度），不判定质量数值能否被预言；
不产生新物理。判出「给定算符则唯一」是**空命题**（算符自由度 ≡ 测量数），不等于导出质量。

退出码：仅由自检 CHK 决定；判出 MISMATCH 不是引擎失败。
"""

import os
import sys
import json
import random
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ITEMS = []
_SELF = []


def P(name, ok, detail, note=""):
    ITEMS.append(dict(id=name, verdict="PASS" if ok else "FAIL", detail=detail, note=note))


def F(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="FAIL", detail=detail, note=note))


def BOUND(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="BOUNDARY", detail=detail, note=note))


def INFO(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="INFO", detail=detail, note=note))


def CORR(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="CORRECTED", detail=detail, note=note))


def MIS(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="MISMATCH", detail=detail, note=note))


def CHK(name, cond, detail=""):
    _SELF.append(dict(name=name, ok=bool(cond), detail=detail))


# ---------- 复线性代数（纯标准库，complex 列表） ----------

def rand_cmat(rng, n, lo=-9, hi=9):
    """通用位置的复 n×n 矩阵，**整数**实部/虚部（供 Fraction 精确消元用）。
    整数取值不影响「通用位置」性质，且使生成元作用后的变分矩阵仍为整数 ⇒ 可精确求秩。"""
    while True:
        M = [[complex(rng.randint(lo, hi), rng.randint(lo, hi)) for _ in range(n)]
             for _ in range(n)]
        if all(any(z != 0 for z in row) for row in M):
            return M


def zeros(n, m):
    return [[0.0] * m for _ in range(n)]


def mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def mat_dag(A):
    n, m = len(A), len(A[0])
    return [[A[j][i].conjugate() for j in range(n)] for i in range(m)]


def u3_generators(n):
    """U(n) 的反厄米生成元（实维 n^2）：
       对角 i·E_kk                → n 个
       (E_kl − E_lk)              → n(n-1)/2 个
       i(E_kl + E_lk)             → n(n-1)/2 个
    返回复矩阵列表。"""
    gens = []
    for k in range(n):
        M = [[0j] * n for _ in range(n)]
        M[k][k] = 1j
        gens.append(M)
    for k in range(n):
        for l in range(k + 1, n):
            A = [[0j] * n for _ in range(n)]
            A[k][l] = 1.0
            A[l][k] = -1.0
            gens.append(A)
            B = [[0j] * n for _ in range(n)]
            B[k][l] = 1j
            B[l][k] = 1j
            gens.append(B)
    return gens


def flatten_real(mats):
    """复矩阵列表 → 实向量（实部、虚部交错展开）。"""
    v = []
    for M in mats:
        for row in M:
            for z in row:
                v.append(z.real)
                v.append(z.imag)
    return v


def rank_exact(rows):
    """精确秩（Fraction 高斯消元，零判定 = 严格等于 0）。

    为何弃用浮点阈值：结构零方向（如重子数 U(1)_B）消元后残余 ~1e-16 相对量级，
    浮点阈值无论取 1e-14×当前列 max 还是 ×全局 max 都会**边际抖动**
    （实测 seed1 得自由度 9、seed2 得 10）。整数矩阵 + 精确有理消元 ⇒ 零就是零。
    """
    A = [[Fraction(x) for x in r] for r in rows]
    nrow = len(A)
    if nrow == 0:
        return 0
    ncol = len(A[0])
    piv = 0
    for col in range(ncol):
        if piv >= nrow:
            break
        best = -1
        for r in range(piv, nrow):
            if A[r][col] != 0:
                best = r
                break
        if best < 0:
            continue
        A[piv], A[best] = A[best], A[piv]
        pv = A[piv][col]
        for r in range(piv + 1, nrow):
            if A[r][col] != 0:
                f = A[r][col] / pv
                for c in range(col, ncol):
                    A[r][c] -= f * A[piv][c]
        piv += 1
    return piv


def rank_gauss(rows, tol_rel=1e-14):
    """（保留）浮点版秩，仅作交叉对照；主判据用 rank_exact。"""
    A = [r[:] for r in rows]
    nrow = len(A)
    if nrow == 0:
        return 0
    ncol = len(A[0])
    gmax = 0.0
    for r in A:
        for x in r:
            if abs(x) > gmax:
                gmax = abs(x)
    thr = tol_rel * gmax if gmax > 0.0 else 0.0
    piv = 0
    for col in range(ncol):
        if piv >= nrow:
            break
        best = -1
        bestv = 0.0
        for r in range(piv, nrow):
            v = abs(A[r][col])
            if v > bestv:
                bestv = v
                best = r
        if best < 0 or bestv <= thr:
            continue
        A[piv], A[best] = A[best], A[piv]
        pv = A[piv][col]
        for r in range(piv + 1, nrow):
            f = A[r][col] / pv
            if f != 0.0:
                for c in range(col, ncol):
                    A[r][c] -= f * A[piv][c]
        piv += 1
    return piv


def flavor_rank(ng, sectors, rng):
    """sectors: 列表，每项 = (Y_matrix, group_name, gen_list_for_left, gen_list_for_right)
    left/right 生成元共享（同一个 U(3)_Q 同时作用在 Y_u,Y_d 上）。
    返回 (总实参数, 机器秩, 物理自由度)。

    约定：
      Y_u -> U_Q  Y_u  U_uR^†
      Y_d -> U_Q  Y_d  U_dR^†
      Y_e -> U_L  Y_e  U_eR^†
      Y_n -> U_L  Y_n  U_nR^†
    变分 δY = A Y − Y B（A 左生成元，B 右生成元），其余生成元为 0。
    """
    # 收集所有独立群因子与其维度
    # 群因子集合
    group_names = []
    for Y, lname, rname in sectors:
        if lname not in group_names:
            group_names.append(lname)
        if rname not in group_names:
            group_names.append(rname)
    gens = {gname: u3_generators(ng) for gname in group_names}
    dim_group = len(group_names) * ng * ng

    nY = len(sectors)
    nparam = nY * (2 * ng * ng)  # 每个复 ng×ng → 2ng^2 实参数

    rows = []
    # 对每个群因子的每个生成元，构造一行（变分向量）
    for gname in group_names:
        for G in gens[gname]:
            deltas = []
            for (Y, lname, rname) in sectors:
                A = G if lname == gname else [[0j] * ng for _ in range(ng)]
                B = G if rname == gname else [[0j] * ng for _ in range(ng)]
                # δY = A·Y − Y·B
                AY = mat_mul(A, Y)
                YB = mat_mul(Y, B)
                dY = [[AY[i][j] - YB[i][j] for j in range(ng)] for i in range(ng)]
                deltas.append(dY)
            rows.append(flatten_real(deltas))

    rk = rank_exact(rows)
    # 交叉对照：浮点版应在 ±1 内一致（容差容忍结构零的边际抖动）
    rk_f = rank_gauss(rows)
    return nparam, rk, nparam - rk, dim_group, rk_f


# ---------- 自检用：闭式对照 ----------
def closed_form(ng, case):
    """已知闭式：quark-only: ng^2+1 ; +charged lepton: ng^2+ng+1 ; +Dirac nu: 2ng^2+2"""
    if case == "q":
        return ng * ng + 1
    if case == "qe":
        return ng * ng + ng + 1
    if case == "qen":
        return 2 * ng * ng + 2
    return None


def run_all():
    rng = random.Random(20261010)

    # ---- 主测：ng=3 三档 ----
    Yu = rand_cmat(rng, 3)
    Yd = rand_cmat(rng, 3)
    Ye = rand_cmat(rng, 3)
    Yn = rand_cmat(rng, 3)

    cases = {}
    cases["q"] = flavor_rank(3, [(Yu, "Q", "uR"), (Yd, "Q", "dR")], rng)
    cases["qe"] = flavor_rank(3, [(Yu, "Q", "uR"), (Yd, "Q", "dR"), (Ye, "L", "eR")], rng)
    cases["qen"] = flavor_rank(3, [(Yu, "Q", "uR"), (Yd, "Q", "dR"),
                                   (Ye, "L", "eR"), (Yn, "L", "nR")], rng)

    print("=" * 78)
    print("attack16 probe3 · 味自由度秩计数")
    print("=" * 78)
    for k in ("q", "qe", "qen"):
        npar, rk, dof, dg, rk_f = cases[k]
        cf = closed_form(3, k)
        print("  %-4s 实参数=%d 机器秩=%d 物理自由度=%d  群维=%d  闭式=%s %s"
              % (k, npar, rk, dof, dg, cf, "✓" if dof == cf else "✗"))

    # ---- D01 机器秩与闭式一致（自证计数器可信）----
    ok_closed = all(cases[k][2] == closed_form(3, k) for k in cases)
    CHK("CHK-3a 机器秩与闭式一致(ng=3 三档)", ok_closed,
        " ".join("%s:%d/%s" % (k, cases[k][2], closed_form(3, k)) for k in cases))

    # ---- CHK-10 反向对照：ng=2 quark-only 必得 5 ----
    Yu2 = rand_cmat(rng, 2)
    Yd2 = rand_cmat(rng, 2)
    n2, r2, d2, _, _ = flavor_rank(2, [(Yu2, "Q", "uR"), (Yd2, "Q", "dR")], rng)
    CHK("CHK-10 ng=2 quark-only 必得 5", d2 == 5, "实=%d 秩=%d 自由度=%d" % (n2, r2, d2))
    # ng=1 对照
    Yu1 = rand_cmat(rng, 1)
    n1, r1, d1, _, _ = flavor_rank(1, [(Yu1, "Q", "uR")], rng)
    CHK("CHK-3b ng=1 单 Yukawa 必得 1", d1 == 1, "实=%d 秩=%d 自由度=%d" % (n1, r1, d1))

    # ---- 条目 ----
    npar_q, rk_q, dof_q, dg_q, _ = cases["q"]
    npar_qe, rk_qe, dof_qe, dg_qe, _ = cases["qe"]
    npar_qen, rk_qen, dof_qen, dg_qen, _ = cases["qen"]

    INFO("D01", "味秩 n_g=3 quark-only：实 %d - 秩 %d = %d" % (npar_q, rk_q, dof_q),
         "= 6 质量 + 4 CKM（与闭式 ng^2+1 一致）")
    INFO("D02", "味秩 n_g=3 +Y_e：实 %d - 秩 %d = %d" % (npar_qe, rk_qe, dof_qe),
         "= 6 夸克质量 + 3 带电轻子质量 + 4 CKM")
    INFO("D03", "味秩 n_g=3 +Y_nu：实 %d - 秩 %d = %d" % (npar_qen, rk_qen, dof_qen),
         "= 20（+3 中微子质量 +4 PMNS）")

    # D05：v7.0 声称 Y_u,Y_d 给「9 个费米子质量（6 夸克+3 轻子）+ CKM4 = 13」
    # 机器：Y_u,Y_d 只有 10（6 夸克质量 + 4 CKM）；3 个带电轻子质量需要第三个算符 Y_e。
    claim = 13
    machine = dof_q  # 10
    MIS("D05", "v7.0 称「给定 Y_u,Y_d → 9 个费米子质量 + CKM4 = %d」；机器给 Y_u,Y_d 自由度 = %d"
        % (claim, machine),
        "%d ≠ %d：3 个带电轻子质量需第三个算符 Y_e（加 Y_e 后机器给 %d）" % (machine, claim, dof_qe))

    # D06：从「19 层面消除」→ 归约前后恒为 13 ⇒ 重参数化非消元
    CORR("D06", "「参数自由度从 19 层面被消除」：算符化前后物理自由度恒为 %d（=6+3+4）" % dof_qe,
         "是重参数化（换记账方式），不是自由度消元")

    # D07：随机 Yukawa 满射到 (质量, CKM)，无额外约束
    INFO("D07", "随机 Y_u,Y_d 的谱与 V_CKM=U_u U_d^† 可任意取遍 (6 质量, 4 CKM)",
         "算符空间 → 物理参数空间是满射，不存在额外约束 ⇒ 「给定算符则唯一」是恒真陈述")

    # 自检：秩计算器对通用位置矩阵稳定（换种子再算一次）
    rng2 = random.Random(777)
    Yu_b = rand_cmat(rng2, 3)
    Yd_b = rand_cmat(rng2, 3)
    _, rk_b, dof_b, _, _ = flavor_rank(3, [(Yu_b, "Q", "uR"), (Yd_b, "Q", "dR")], rng2)
    CHK("CHK-3c 换随机种子秩不变", dof_b == dof_q, "seed2 自由度=%d vs seed1=%d" % (dof_b, dof_q))

    # ---- 输出 ----
    outdir = os.path.join(os.path.dirname(HERE), "数据")
    os.makedirs(outdir, exist_ok=True)
    json_path = os.path.join(outdir, "attack16_probe3_味自由度秩计数_2026-10-10.json")
    txt_path = os.path.join(outdir, "attack16_probe3_味自由度秩计数_2026-10-10_report.txt")
    payload = dict(
        probe="attack16_probe3_味自由度秩计数",
        date="2026-10-10",
        items=ITEMS,
        self_checks=_SELF,
        computed=dict(
            ng3_quark_only=dict(nparam=npar_q, rank=rk_q, dof=dof_q, group_dim=dg_q),
            ng3_plus_e=dict(nparam=npar_qe, rank=rk_qe, dof=dof_qe, group_dim=dg_qe),
            ng3_plus_nu=dict(nparam=npar_qen, rank=rk_qen, dof=dof_qen, group_dim=dg_qen),
            ng2_quark_only=dict(dof=d2), ng1=dict(dof=d1),
            v70_claim=claim, machine_quark_only=machine,
            rank_float_crosscheck={k: cases[k][4] for k in cases},
        ),
        red_lines=[
            "本探针只做自由度计数，不判定质量数值能否被预言",
            "「给定算符则唯一」是空命题（算符自由度 ≡ 测量数），不构成导出",
            "不产生新物理",
        ],
    )
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("attack16 probe3 味自由度秩计数 2026-10-10\n")
        for k in ("q", "qe", "qen"):
            npar, rk, dof, dg, _ = cases[k]
            f.write("%s: nparam=%d rank=%d dof=%d group_dim=%d\n" % (k, npar, rk, dof, dg))
        f.write("v70_claim=%d machine_quark_only=%d\n" % (claim, machine))

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])
    print("-" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (self_ok, len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("产物：")
    for p in (json_path, txt_path):
        print("  " + os.path.relpath(p, os.path.dirname(HERE)))
    print("=" * 78)
    return payload, self_ok == len(_SELF)


if __name__ == "__main__":
    _, ok = run_all()
    sys.exit(0 if ok else 1)
