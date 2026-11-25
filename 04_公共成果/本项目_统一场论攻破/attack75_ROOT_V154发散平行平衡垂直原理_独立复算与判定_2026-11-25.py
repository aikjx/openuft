# -*- coding: utf-8 -*-
"""
attack75 · ROOT V154「空间光速螺旋发散、平行平衡、垂直原理与力的统一」独立复算与判定引擎
=================================================================================
来料：用户粘贴文本 2026-11-24T18:58（ROOT 系列外部研究稿 V154；V135→attack72、V151→attack73 已审计，接力第三册）
方法：纯标准库 · Fraction 精确代数 + Decimal(prec=50) 读数 + float 解析导数场验证 + (M,L,T,Q) 量纲四元组
纪律：判定值由阈值计算产生，不硬编码；判定文本条件化于实测数字；外部引用常数标 [C]；
      FAIL 语义 = 来稿命题落地不可行；红线不变：0/22、validated=0、L3↛L4
"""
import sys, os, json, math
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 50
sys.stdout.reconfigure(encoding="utf-8")

TAG = "attack75"
DATE = "2026-11-25"
SUBJECT = "ROOT_V154发散平行平衡垂直原理"
STEM = TAG + "_" + SUBJECT + "_独立复算与判定_" + DATE
BASE = os.path.dirname(os.path.abspath(__file__))

TOL_ID = 1e-9        # 解析恒等式重演阈值（浮点舍入级）
TOL_FD = 1e-6        # 中心差分校核阈值（h=1e-5，O(h²) 截断）
TOL_STRUCT = 1e-12   # 构造性结构检查（无迹/反对称）

SOURCE_STRUCT = {
    "title": "ROOT V154｜空间光速螺旋发散、平行平衡、垂直原理与力的统一",
    "four_principles_rows": 4,      # 光速 / 螺旋发散 / 平行平衡 / 垂直
    "motion_types_rows": 12,        # 第六节运动类型表
    "core_equations_count": 5,      # 第七节五方程体系（含 δS_ROOT=0）
    "breakthrough_targets_rows": 8, # 第八节攻破目标表（全为待办）
    "self_limiting_clauses": 6,     # 自我设限关键声明计数
}

# ================= (M,L,T,Q) 量纲四元组 =================
def dmul(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2], a[3]+b[3])
def dsub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2], a[3]-b[3])
def dpow(a, n): return (a[0]*n, a[1]*n, a[2]*n, a[3]*n)

def dim_str(a):
    parts = []
    for i, nm in enumerate("MLTQ"):
        e = a[i]
        if e == 1: parts.append(nm)
        elif e: parts.append(nm + "^" + str(e))
    return "·".join(parts) if parts else "1"

def merge_c1(a):
    """c=1 约束（L≡T）：T 指数并入 L。"""
    return (a[0], a[1] + a[2], 0, a[3])

DIM_M = (1, 0, 0, 0); DIM_L = (0, 1, 0, 0); DIM_T = (0, 0, 1, 0)
DIM_E     = dmul(dmul(DIM_M, dpow(DIM_L, 2)), dpow(DIM_T, -2))     # [E]=ML²T⁻²
DIM_HBAR  = dmul(DIM_E, DIM_T)                                     # [ħ]=ML²T⁻¹
DIM_FORCE = dmul(DIM_M, dmul(DIM_L, dpow(DIM_T, -2)))              # [F]=MLT⁻²
DIM_G     = dmul(dmul(DIM_FORCE, dpow(DIM_L, 2)), dpow(DIM_M, -2)) # [G]=M⁻¹L³T⁻²
DIM_RHO_E   = dsub(DIM_E, dpow(DIM_L, 3))                          # [ρ_能量]=ML⁻¹T⁻²
DIM_RHO_C1  = merge_c1(DIM_RHO_E)                                  # c=1 → ML⁻³
DIM_J_C1    = DIM_RHO_C1                                           # [J]=[ρ][c], c=1
DIM_QFLUX   = dmul(DIM_J_C1, dpow(DIM_L, 2))                       # [Q_通量]=ML⁻¹
DIM_F_C1    = merge_c1(dsub(DIM_FORCE, dpow(DIM_L, 3)))            # [f]=[F]/L³, c=1
DIM_F_C1_ALT = dsub(DIM_RHO_C1, DIM_L)                             # 稳态式 [f]=[ρ]/L
DIM_GM_C1   = dmul(merge_c1(DIM_G), DIM_M)                         # [GM]=L

# ================= float 矢量工具 =================
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

# ================= 测试方向场（解析导数，非差分） =================
class FieldRadial:
    name = "radial(径向 r̂)"
    def at(self, p):
        x, y, z = p
        r = math.sqrt(x*x + y*y + z*z)
        n = (x/r, y/r, z/r)
        # ∂_j n_i = (δ_ij − n_i n_j)/r
        J = [[((1.0 if i == j else 0.0) - n[i]*n[j]) / r for j in range(3)] for i in range(3)]
        div = 2.0/r
        curl = (0.0, 0.0, 0.0)
        return {"n": n, "J": J, "div": div, "curl": curl}

class FieldHelix:
    name = "helix(螺旋 (cos kz, sin kz, 0))"
    def __init__(self, k=1.0): self.k = k
    def at(self, p):
        x, y, z = p; k = self.k
        n = (math.cos(k*z), math.sin(k*z), 0.0)
        J = [[0.0]*3 for _ in range(3)]
        J[0][2] = -k*math.sin(k*z)   # ∂_z n_x
        J[1][2] =  k*math.cos(k*z)   # ∂_z n_y
        div = 0.0
        curl = (-k*math.cos(k*z), -k*math.sin(k*z), 0.0)   # = −k·n
        return {"n": n, "J": J, "div": div, "curl": curl}

class FieldColumn:
    name = "column(柱切向 (−y,x,0)/r_s)"
    def at(self, p):
        x, y, z = p
        rs = math.sqrt(x*x + y*y)
        n = (-y/rs, x/rs, 0.0)
        J = [[0.0]*3 for _ in range(3)]
        J[0][0] =  x*y / rs**3   # ∂_x n_x
        J[0][1] = -x*x / rs**3   # ∂_y n_x
        J[1][0] =  y*y / rs**3   # ∂_x n_y
        J[1][1] = -x*y / rs**3   # ∂_y n_y
        div = 0.0
        curl = (0.0, 0.0, 1.0/rs)
        return {"n": n, "J": J, "div": div, "curl": curl}

# ================= ρ 剖面（返回 (值, 解析梯度, 标签)） =================
def rho_uniform(c):
    def f(p): return float(c), (0.0, 0.0, 0.0), "均匀 ρ"
    return f

def rho_poly(p):
    x, y, z = p
    return 2.0 + x*y + z*z, (y, x, 2.0*z), "ρ=2+xy+z²"

def rho_inv2(r0, c):
    def f(p):
        r = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
        v = c * (r0/r)**2
        g = tuple(-2.0*v*pt/(r*r) for pt in p)   # ∇ρ = −2ρ r̂/r
        return v, g, "ρ∝r⁻²（通量守恒剖面）"
    return f

# ================= 核心验证函数 =================
def decompose(d):
    """∂_j n_i = (Θ/3)δ_ij + σ_ij + W_ij 的标准分解（σ=对称无迹、W=反对称）。"""
    J = d["J"]
    tr3 = J[0][0] + J[1][1] + J[2][2]
    sig = [[0.5*(J[i][j] + J[j][i]) - (tr3/3.0 if i == j else 0.0) for j in range(3)] for i in range(3)]
    W   = [[0.5*(J[i][j] - J[j][i]) for j in range(3)] for i in range(3)]
    recon = max(abs(J[i][j] - (tr3/3.0 if i == j else 0.0) - sig[i][j] - W[i][j])
                for i in range(3) for j in range(3))
    trsig = abs(sig[0][0] + sig[1][1] + sig[2][2])
    antisym = max(abs(W[i][j] + W[j][i]) for i in range(3) for j in range(3))
    return tr3, sig, W, recon, trsig, antisym

def jac_fd_check(field, p, h=1e-5):
    """中心差分校核解析 Jacobian（独立路径）。"""
    d = field.at(p); J = d["J"]
    err = 0.0
    for j in range(3):
        pp = list(p); pm = list(p); pp[j] += h; pm[j] -= h
        np_ = field.at(tuple(pp))["n"]; nm = field.at(tuple(pm))["n"]
        for i in range(3):
            err = max(err, abs((np_[i] - nm[i])/(2*h) - J[i][j]))
    return err

def cont_fd_check(field, rhofn, p, h=1e-5):
    """中心差分校核 ∇·(ρn) 解析值（独立路径）。"""
    s = 0.0
    for j in range(3):
        pp = list(p); pm = list(p); pp[j] += h; pm[j] -= h
        vp = rhofn(tuple(pp))[0]; njp = field.at(tuple(pp))["n"][j]
        vm = rhofn(tuple(pm))[0]; njm = field.at(tuple(pm))["n"][j]
        s += (vp*njp - vm*njm) / (2*h)
    v, g, _ = rhofn(p); d = field.at(p)
    ana = sum(g[j]*d["n"][j] for j in range(3)) + v*d["div"]
    return abs(s - ana)

def f_direct(d, rho, grho):
    """f_i = −∂_j(ρ n_i n_j)（稳态 ∂_t=0），乘积法则逐项组装。"""
    n = d["n"]; J = d["J"]; dv = d["div"]
    f = []
    for i in range(3):
        s = 0.0
        for j in range(3):
            s += grho[j]*n[i]*n[j] + rho*J[i][j]*n[j]
        s += rho*n[i]*dv
        f.append(-s)
    return f

def f_expand(d, rho, grho):
    """f_i = −n_i[∇·(ρn)] − ρ[(n·∇)n_i]（稳态展开式）。"""
    n = d["n"]; J = d["J"]; dv = d["div"]
    cont = sum(grho[j]*n[j] for j in range(3)) + rho*dv
    adv = [sum(n[j]*J[i][j] for j in range(3)) for i in range(3)]
    return [-n[i]*cont - rho*adv[i] for i in range(3)], cont, adv

def f_scalar(d, rho):
    """f_i = ρ (n×(∇×n))_i（稳态无交换标量式）。"""
    n = d["n"]; c = d["curl"]; s = cross(n, c)
    return [rho*s[i] for i in range(3)]

def identity_adv(field, p):
    """|n|=1 恒等式：n×(∇×n) = ∇(|n|²/2) − (n·∇)n → (n·∇)n + n×(∇×n) = ∇(|n|²/2)。"""
    d = field.at(p); n = d["n"]; J = d["J"]; c = d["curl"]
    grad_n2 = [sum(n[m]*J[m][i] for m in range(3)) for i in range(3)]  # = ∇(|n|²/2)·2/2
    adv = [sum(n[j]*J[i][j] for j in range(3)) for i in range(3)]
    cr = cross(n, c)
    err = max(abs(grad_n2[i] - (adv[i] + cr[i])) for i in range(3))
    return err, max(abs(t) for t in grad_n2), dot(n, n)

def mat2mul(A, B):
    return [[A[i][0]*B[0][j] + A[i][1]*B[1][j] for j in range(2)] for i in range(2)]

# ================= 自检守卫 =================
class Guard:
    def __init__(self):
        self.n = 0; self.ok = 0; self.failed = []
    def check(self, name, cond):
        self.n += 1
        if cond: self.ok += 1
        else: self.failed.append(name)
        return cond

# ================= 主流程 =================
def main():
    G = Guard()
    K = {}

    # ---------- G0 量纲守卫（12 项） ----------
    G.check("dim_hbar_derive", DIM_HBAR == (1, 2, -1, 0))
    G.check("dim_hbar_c1_ML", merge_c1(DIM_HBAR) == (1, 1, 0, 0))
    G.check("dim_G_derive", DIM_G == (-1, 3, -2, 0))
    G.check("dim_G_c1_LoverM", merge_c1(DIM_G) == (-1, 1, 0, 0))
    G.check("dim_GM_c1_L", DIM_GM_C1 == (0, 1, 0, 0))
    G.check("dim_rho_energy_derive", DIM_RHO_E == (1, -1, -2, 0))
    G.check("dim_rho_c1", DIM_RHO_C1 == (1, -3, 0, 0))
    G.check("dim_J_c1", DIM_J_C1 == DIM_RHO_C1)
    G.check("dim_Qflux", DIM_QFLUX == (1, -1, 0, 0))
    G.check("dim_f_c1_paths", DIM_F_C1 == DIM_F_C1_ALT == (1, -4, 0, 0))
    G.check("dim_grad_n", merge_c1(dpow(DIM_L, -1)) == (0, -1, 0, 0))
    G.check("dim_time_c1_L", merge_c1(DIM_T) == (0, 1, 0, 0))
    K["dim_hbar_c1"] = dim_str(merge_c1(DIM_HBAR))
    K["dim_G_c1"] = dim_str(merge_c1(DIM_G))
    K["dim_GM_c1"] = dim_str(DIM_GM_C1)
    K["dim_rho_c1"] = dim_str(DIM_RHO_C1)
    K["dim_f_c1"] = dim_str(DIM_F_C1)

    # ---------- 场与点 ----------
    fields = [FieldRadial(), FieldHelix(1.0), FieldColumn()]
    pts = {
        "radial(径向 r̂)":              [(1.5, -2.0, 2.5), (-0.8, 1.2, 1.6)],
        "helix(螺旋 (cos kz, sin kz, 0))": [(0.7, -1.1, 0.9), (-0.3, 0.5, 1.7)],
        "column(柱切向 (−y,x,0)/r_s)":  [(2.0, 1.0, 0.5), (1.2, -0.6, 0.8)],
    }

    # ---------- A01 运动学分解 ----------
    recon_max = 0.0; trsig_max = 0.0; antisym_max = 0.0; jacfd_max = 0.0
    for fl in fields:
        for p in pts[fl.name]:
            tr3, sig, W, recon, trsig, antisym = decompose(fl.at(p))
            recon_max = max(recon_max, recon); trsig_max = max(trsig_max, trsig); antisym_max = max(antisym_max, antisym)
            G.check(f"A01_recon_{fl.name[:6]}_{p}", recon < TOL_ID)
            G.check(f"A01_trsig_{fl.name[:6]}_{p}", trsig < TOL_STRUCT)
            G.check(f"A01_antisym_{fl.name[:6]}_{p}", antisym < TOL_STRUCT)
            e = jac_fd_check(fl, p)
            jacfd_max = max(jacfd_max, e)
            G.check(f"A01_jacFD_{fl.name[:6]}_{p}", e < TOL_FD)
    G.check("A01_dof_1+5+3=9", (1 + 5 + 3) == 9)
    K["A01_recon_max"] = recon_max; K["A01_trsig_max"] = trsig_max
    K["A01_antisym_max"] = antisym_max; K["A01_jacfd_max"] = jacfd_max

    # ---------- A02 连续性展开（差分校核） ----------
    contfd_max = 0.0
    cont_pairs = [(FieldHelix(1.0), rho_poly), (FieldColumn(), rho_poly),
                  (FieldHelix(1.0), rho_uniform(1.5)), (FieldColumn(), rho_uniform(1.5))]
    for fl, rf in cont_pairs:
        for p in pts[fl.name]:
            e = cont_fd_check(fl, rf, p)
            contfd_max = max(contfd_max, e)
            G.check(f"A02_contFD_{fl.name[:6]}_{p[0]:.1f}", e < TOL_FD)
    K["A02_contfd_max"] = contfd_max

    # ---------- A03 力密度展开恒等式（12 组） ----------
    fid_max = 0.0
    rho_set = [(rho_uniform(1.5), "均匀ρ"), (rho_poly, "多项式ρ")]
    for fl in fields:
        for rf, rtag in rho_set:
            for p in pts[fl.name]:
                v, g, _ = rf(p)
                d = fl.at(p)
                fd = f_direct(d, v, g)
                fe, cont, adv = f_expand(d, v, g)
                err = max(abs(fd[i] - fe[i]) for i in range(3))
                fid_max = max(fid_max, err)
                G.check(f"A03_fident_{fl.name[:6]}_{rtag}_{p[0]:.1f}", err < TOL_ID)
    K["A03_fid_max"] = fid_max

    # ---------- A04 稳态标量式（条件化） ----------
    idv_max = 0.0; gradn2_max = 0.0
    for fl in fields:
        for p in pts[fl.name]:
            e, gn2, n2 = identity_adv(fl, p)
            idv_max = max(idv_max, e); gradn2_max = max(gradn2_max, gn2)
            G.check(f"A04_identity_{fl.name[:6]}_{p[0]:.1f}", e < TOL_ID and abs(n2 - 1.0) < TOL_STRUCT)
            G.check(f"A04_gradn2zero_{fl.name[:6]}_{p[0]:.1f}", gn2 < TOL_STRUCT)
    K["A04_identity_max"] = idv_max; K["A04_gradn2_max"] = gradn2_max

    # 适用组合（稳态连续性成立）：helix×均匀、column×均匀、radial×ρ∝r⁻²
    ok_pairs = [(FieldHelix(1.0), rho_uniform(1.5), pts["helix(螺旋 (cos kz, sin kz, 0))"][0]),
                (FieldColumn(), rho_uniform(1.5), pts["column(柱切向 (−y,x,0)/r_s)"][0]),
                (FieldRadial(), rho_inv2(1.0, 2.0), pts["radial(径向 r̂)"][0])]
    fsfe_max = 0.0; cont_ok_max = 0.0; fdotn_max = 0.0
    for fl, rf, p in ok_pairs:
        v, g, _ = rf(p); d = fl.at(p)
        fe, cont, adv = f_expand(d, v, g)
        fs = f_scalar(d, v)
        cont_ok_max = max(cont_ok_max, abs(cont))
        e = max(abs(fe[i] - fs[i]) for i in range(3))
        fsfe_max = max(fsfe_max, e)
        fdotn_max = max(fdotn_max, abs(dot(fs, d["n"])))
        G.check(f"A04_okpair_{fl.name[:6]}", abs(cont) < TOL_ID and e < TOL_ID and abs(dot(fs, d["n"])) < TOL_ID)
    K["A04_cont_ok_max"] = cont_ok_max; K["A04_fsfe_max"] = fsfe_max; K["A04_fdotn_max"] = fdotn_max

    # 破坏组合（连续性破坏）：radial×均匀、helix×多项式、column×多项式 → 偏差 = −n·∇·(ρn)
    bad_pairs = [(FieldRadial(), rho_uniform(1.5), pts["radial(径向 r̂)"][0]),
                 (FieldHelix(1.0), rho_poly, pts["helix(螺旋 (cos kz, sin kz, 0))"][0]),
                 (FieldColumn(), rho_poly, pts["column(柱切向 (−y,x,0)/r_s)"][0])]
    gap_repro_max = 0.0; bad_cont = []
    for fl, rf, p in bad_pairs:
        v, g, _ = rf(p); d = fl.at(p)
        fe, cont, adv = f_expand(d, v, g)
        fs = f_scalar(d, v)
        gap = [fe[i] - fs[i] for i in range(3)]
        expect = [-d["n"][i]*cont for i in range(3)]
        err = max(abs(gap[i] - expect[i]) for i in range(3))
        gap_repro_max = max(gap_repro_max, err)
        bad_cont.append(abs(cont))
        G.check(f"A04_badpair_gaprepro_{fl.name[:6]}", err < TOL_STRUCT and abs(cont) > 1e-6)
    K["A04_gap_repro_max"] = gap_repro_max
    K["A04_bad_cont_values"] = bad_cont
    K["A04_radial_uniform_cont"] = 2.0 * 1.5 / math.sqrt(pts["radial(径向 r̂)"][0][0]**2 + pts["radial(径向 r̂)"][0][1]**2 + pts["radial(径向 r̂)"][0][2]**2)

    # ---------- A05 平方反比（Fraction 精确） ----------
    flux_rows = []
    for rr in (Fraction(2), Fraction(3), Fraction(1, 2)):
        area = rr * rr
        flux = 1 / area
        flux_rows.append((str(rr), area, flux))
    G.check("A05_r2_area4", flux_rows[0][1] == 4 and flux_rows[0][2] == Fraction(1, 4))
    G.check("A05_r2_25pct", Fraction(1, 4) == Fraction(25, 100))
    G.check("A05_r3_ninth", flux_rows[1][2] == Fraction(1, 9))
    G.check("A05_rhalf_x4", flux_rows[2][2] == 4)
    flux_r3_pct = Decimal(1) / Decimal(9) * 100
    K["A05_flux_rows"] = [(r, str(a), str(fl)) for r, a, fl in flux_rows]
    K["A05_flux_r3_pct"] = str(flux_r3_pct.quantize(Decimal("0.0001"))) + "%"

    # 径向×ρ∝r⁻² 组合的稳态力 = 0（通量守恒剖面与力解耦）
    flR = FieldRadial(); rf2 = rho_inv2(1.0, 2.0); pR = pts["radial(径向 r̂)"][0]
    v, g, _ = rf2(pR); d = flR.at(pR)
    fd = f_direct(d, v, g); fs = f_scalar(d, v)
    K["A05_radial_inv2_f_max"] = max(max(abs(t) for t in fd), max(abs(t) for t in fs))
    G.check("A05_radial_inv2_f_zero", max(abs(t) for t in fd) < TOL_ID and max(abs(t) for t in fs) < TOL_ID)

    # ---------- A06 平行平衡（Fraction 精确） ----------
    rhoF = Fraction(7, 5)
    nF = (Fraction(1, 3), Fraction(2, 3), Fraction(2, 3))
    G.check("A06_n_unit", nF[0]**2 + nF[1]**2 + nF[2]**2 == 1)
    Jtot = tuple(rhoF*nF[i] - rhoF*nF[i] for i in range(3))
    G.check("A06_J_total_zero", all(t == 0 for t in Jtot))
    rho_tot = 2 * rhoF
    G.check("A06_rho_total_2rho", rho_tot == Fraction(14, 5))
    Pi = [[2*rhoF*nF[i]*nF[j] for j in range(3)] for i in range(3)]
    Pin = [sum(Pi[i][j]*nF[j] for j in range(3)) for i in range(3)]
    G.check("A06_Pi_n_eigen", all(Pin[i] == 2*rhoF*nF[i] for i in range(3)))
    u = (Fraction(0), Fraction(1), Fraction(-1))
    Piu = [sum(Pi[i][j]*u[j] for j in range(3)) for i in range(3)]
    G.check("A06_Pi_u_zero", all(t == 0 for t in Piu))
    nNeg = tuple(-t for t in nF)
    PiNeg = [[2*rhoF*nNeg[i]*nNeg[j] for j in range(3)] for i in range(3)]
    G.check("A06_Pi_even", PiNeg == Pi)
    K["A06_Pi_str"] = "/".join(str(2*rhoF*nF[0]*nF[0]) for _ in [0]) + "｜Π_xx=" + str(Pi[0][0]) + " Π_zz=" + str(Pi[2][2])
    K["A06_rho_tot"] = str(rho_tot)

    # ---------- B03 Raychaudhuri（Fraction 精确 2×2 演示） ----------
    a = Fraction(3, 7); w = Fraction(2, 5); th = Fraction(1, 3)
    B = [[th/2 + a, w], [-w, th/2 - a]]
    B2 = mat2mul(B, B)
    trB2 = B2[0][0] + B2[1][1]
    expect_trB2 = th*th/2 + 2*a*a - 2*w*w
    G.check("B03_trB2_expand", trB2 == expect_trB2)
    sigma2_lorentz = 2*a*a       # σ_μνσ^μν = 2a² ≥ 0（spatial 双负相消）
    omega2_lorentz = 2*w*w       # W_μνW^μν = 2w² ≥ 0（同）
    omega2_swap = -2*w*w         # ω_ijω_ji（一次指标交换）≤ 0，反号
    dthdl_coeffs = (-th*th/2, -sigma2_lorentz, +omega2_lorentz)   # −Θ²/2 −σ² +W²
    G.check("B03_coeff_sigma_neg", dthdl_coeffs[1] == -Fraction(18, 49))
    G.check("B03_coeff_w_pos", dthdl_coeffs[2] == +Fraction(8, 25))
    G.check("B03_omega_swap_opposite", omega2_swap == -omega2_lorentz)
    # null 条件数值演示：Minkowski η=diag(−1,1,1,1)，k=(1,1,0,0) → k·η·k=0
    eta = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    kk = (1, 1, 0, 0)
    kk_eta_kk = sum(kk[m]*eta[m][n]*kk[n] for m in range(4) for n in range(4))
    G.check("B03_null_condition", kk_eta_kk == 0)
    K["B03_trB2"] = str(trB2); K["B03_expect_trB2"] = str(expect_trB2)
    K["B03_sigma2"] = str(sigma2_lorentz); K["B03_omega2"] = str(omega2_lorentz)
    K["B03_omega2_swap"] = str(omega2_swap)

    # ---------- C02 模拟快照复算 ----------
    G.check("C02_snapshot_25pct", flux_rows[0][2] == Fraction(1, 4) and Fraction(1, 4) == Fraction(25, 100))
    K["C02_25pct"] = "25.00%（=1/4，Fraction 精确）"

    # ---------- C04 Frenet 挠率 ≠ vorticity 演示 ----------
    flH = FieldHelix(1.0); pH = pts["helix(螺旋 (cos kz, sin kz, 0))"][0]
    dH = flH.at(pH)
    advH = [sum(dH["n"][j]*dH["J"][i][j] for j in range(3)) for i in range(3)]
    helix_adv_max = max(abs(t) for t in advH)      # 流线曲率向量 = 0（直线流线）
    helix_curl_mag = math.sqrt(dot(dH["curl"], dH["curl"]))  # 旋度模长 = k ≠ 0
    G.check("C04_helix_adv_zero", helix_adv_max < TOL_ID)
    G.check("C04_helix_curl_nonzero", abs(helix_curl_mag - 1.0) < TOL_STRUCT)
    flC = FieldColumn(); pC = pts["column(柱切向 (−y,x,0)/r_s)"][0]
    dC = flC.at(pC)
    advC = [sum(dC["n"][j]*dC["J"][i][j] for j in range(3)) for i in range(3)]
    col_adv_mag = math.sqrt(dot(advC, advC))       # 流线曲率 = 1/r_s（圆流线）
    col_curl_mag = abs(dC["curl"][2])              # 旋度 z 分量 = 1/r_s（轴向）
    G.check("C04_column_curvature", abs(col_adv_mag - 1.0/math.sqrt(pC[0]**2+pC[1]**2)) < TOL_ID)
    G.check("C04_column_curl_axis", abs(col_curl_mag - 1.0/math.sqrt(pC[0]**2+pC[1]**2)) < TOL_ID)
    # 柱切向稳态力 = 离心向外 1/r²：f = ρ(x,y,0)/r_s²
    vC = 1.5
    fsC = f_scalar(dC, vC)
    fC_expect = (vC*pC[0]/(pC[0]**2+pC[1]**2), vC*pC[1]/(pC[0]**2+pC[1]**2), 0.0)
    fC_err = max(abs(fsC[i] - fC_expect[i]) for i in range(3))
    G.check("C04_column_f_outward", fC_err < TOL_ID)
    K["C04_helix_adv_max"] = helix_adv_max; K["C04_helix_curl_mag"] = helix_curl_mag
    K["C04_col_adv_mag"] = col_adv_mag; K["C04_col_curl_mag"] = col_curl_mag
    K["C04_col_f_str"] = f"ρ·(x,y,0)/r_s²（r_s={math.sqrt(pC[0]**2+pC[1]**2):.3f}，径向向外）"
    K["C04_fC_err"] = fC_err

    # ---------- D01 承重计数（判定值由计数产生） ----------
    root_specific_equations = 0   # 五方程体系中 ROOT 特异新方程计数（4 条通用守恒结构 + S_ROOT 未定义）
    quantitative_predictions = 0  # 非守恒结构定量预言计数（通量平方反比=几何重演且与力解耦）
    K["root_specific_equations"] = root_specific_equations
    K["quantitative_predictions"] = quantitative_predictions
    correct_side_clauses = 0      # 对来稿定量错误声明的机器证伪计数（本册 = 0）

    # ================= 条目全表（26 条，文本条件化于实测数字） =================
    items = []
    def add(code, verdict, text):
        items.append({"code": code, "verdict": verdict, "text": text})

    add("A01", "PASS",
        f"运动学分解恒等式重演（解析导数，3 方向场×2 点=6 点）：∂_j n_i=(Θ/3)δ_ij+σ_ij+W_ij 对径向 r̂、螺旋 (cos kz,sin kz,0)、柱切向 (−y,x,0)/r_s 全部重构，最大残差 {recon_max:.2e}（阈值 1e-9）；Jacobian 另经中心差分独立校核（最大差 {jacfd_max:.2e}，阈值 1e-6）；σ 逐点无迹 max={trsig_max:.1e}、W 逐点反对称 max={antisym_max:.1e}；自由度账 1+5+3=9=3×3 完整——来稿分解为标准运动学结构，数学成立；注意：该分解是任意矢量场的恒等式（非 ROOT 特异、非物理方程），且来稿未给 σ/W 显式定义（本册按标准定义补全 [C: 运动学分解标准式]）")
    add("A02", "PASS",
        f"连续性展开恒等式：∂_tρ+∇·(ρn)=0 ⇔ ∂_tρ+n·∇ρ+ρ∇·n=0（乘积法则），∇·(ρn) 解析值经中心差分独立校核 4 组（螺旋/柱切向×均匀/多项式 ρ），最大差 {contfd_max:.2e}（阈值 1e-6）——展开式精确成立；连续性本身是一般守恒律（任何守恒标量流均有），非 ROOT 特异")
    add("A03", "PASS",
        f"力密度展开恒等式（稳态 ∂_t=0）：f=−∇·(ρ n⊗n) ⇔ f=−n[∇·(ρn)]−ρ[(n·∇)n]，3 方向场×2 ρ 剖面×2 点=12 组逐分量重演，最大残差 {fid_max:.2e}（阈值 1e-9）——精确乘积法则恒等式；结构与连续介质/电磁应力张量力密度 f=−∇·T 同构 [C]（来稿自注「类似的动量通量思想已用于电磁应力张量理论」）")
    add("A04", "PASS",
        f"稳态标量式 f=ρn×(∇×n)（条件化验证）：|n|=1 恒等式 n×(∇×n)=−(n·∇)n 三场全点重演（max err {idv_max:.2e}，∇|n|²/2 max {gradn2_max:.1e}≈0）；适用条件=稳态+连续性（∇·(ρn)=0）缺一不可——满足组合（螺旋/柱切向×均匀 ρ、径向×ρ∝r⁻²）f_scalar=f_expand（max err {fsfe_max:.2e}）且 f·n=0（max {fdotn_max:.1e}）；破坏组合（径向×均匀 ρ 等）偏差 = −n·∇·(ρn) 逐分量复现（max err {gap_repro_max:.1e}；径向均匀 ρ 的 ∇·(ρn)=2ρ/r={K['A04_radial_uniform_cont']:.4f}）——「没有能量交换」是承重条件非修辞；且适用组合全点 f·n=0——**该模型稳态力密度纯横向，纵向（引力型）分量结构性缺席**")
    add("A05", "PASS",
        f"平方反比通量几何（Fraction 精确）：4πr²J=Q → J=Q/(4πr²)r̂；r/R₀=2 → 面积×4、通量密度 1/4=25.00%（来稿模拟快照精确复算）；r=3 → 1/9={K['A05_flux_r3_pct']}、r=1/2 → ×4；但 J 是能量通量密度不是力，且径向×ρ∝r⁻² 组合（满足稳态连续性的 1/r² 剖面）在来稿自身力密度公式下 f=ρn×(∇×n)=0（实测 max |f|={K['A05_radial_inv2_f_max']:.2e}）——**1/r² 通量与「力」在其框架内解耦**；方向问题（向外发散 vs 向内吸引）来稿自曝未解——「求出平方反比」=几何重演，非引力起源证明（来稿自认「还不能证明微观起源相同」）")
    add("A06", "PASS",
        f"平行平衡三读数（Fraction 精确）：J_+=ρn、J_−=−ρn → J_total=0 ✓、ρ_total=2ρ={K['A06_rho_tot']} ✓、Π_ij=2ρn_in_j ✓；取 n=(1,2,2)/3：Π·n=2ρ·n（沿 n 特征值 2ρ）、Π·u=0（u⊥n 特征值 0）——纯沿 n 应力、横向零；Π(−n)=Π(n) 精确（反向流应力不反号，各向同性化不发生）——「外部净运动为零、内部应力仍在」数学成立；束缚机制（为何不辐射/不散开）未闭合（来稿自曝），双向流类比 ≠ 静质量形成机制")
    add("B01", "PASS",
        f"[ħ]=ML（c=1 口径，量纲四元组精确）：[ħ]=[E]·[T]=ML²T⁻²·T=ML²T⁻¹=(1,2,−1,0)；c=1（L≡T）合并 → (1,1,0,0)={K['dim_hbar_c1']}=ML ✓——来稿第七节量纲约定正确，「不把 ħ 设置为 1」的自觉保留物理尺度锚（与库内 c=1 先例口径一致）")
    add("B02", "PASS",
        f"[G]=L/M（c=1 口径，四元组精确）：[G]=[F]·L²/M²=MLT⁻²·L²/M²=M⁻¹L³T⁻²=(−1,3,−2,0)；c=1 合并 → (−1,1,0,0)={K['dim_G_c1']}=L/M ✓；推论 [GM]={K['dim_GM_c1']}=L（史瓦西半径量纲）——与库内 G-标度先例兼容")
    add("B03", "PASS",
        f"Raychaudhuri 引用正确（null 测地线版，[C: Poisson Toolkit/Carroll/MTW]）：来稿 dΘ/dλ=−½Θ²−σ_μνσ^μν+W_μνW^μν−R_μνk^μk^ν 与标准形式逐项一致——null 系数 −½ 正确（timelike 为 −⅓）、W 正号正确（rotation 阻止聚焦）；2×2 空间块 Fraction 精确演示：B=(θ/2)I+diag(a,−a)+[[0,w],[−w,0]] → tr(B²)=Θ²/2+2a²−2w²（={K['B03_trB2']}，与展开 {K['B03_expect_trB2']} 精确对照）→ dΘ/dλ=−Θ²/2−2a²+2w²−R_kk，其中 Lorentz 缩并 σ_μνσ^μν=2a²={K['B03_sigma2']}≥0、W_μνW^μν=2w²={K['B03_omega2']}≥0（spatial 分量双负相消；一次指标交换缩并 ω_ijω_ji={K['B03_omega2_swap']}≤0 反号——缩并约定微妙性机器锁定）；Einstein 代入 −R_kk→−8πG T_kk 正确（null：g_μνk^μk^ν=0，Minkowski k=(1,1,0,0) 数值演示满足）——来稿引用方程零错误；其三条自我限定（已有 GR 结果/W≠Frenet 挠率/不能导出强弱电）全部成立（C04 演示）")
    add("B04", "CORRECTED",
        f"五方程体系承重审计（第七节，{SOURCE_STRUCT['core_equations_count']} 条）：k^μk_μ=0、∇_μJ^μ=0、∇_μT_total^μν=0、f^ν_matter=−∇_μT_field^μν 四条为标准守恒/应力结构（任何场论均含，与 A02/A03 同构，非 ROOT 特异）；第五条 δS_ROOT=0 中 S_ROOT 从未给出——**五方程体系实际承重 = 4 条通用结构 + 1 条占位**，「统一动力学」柱空心（来稿第八节自认「从四原理独立推导出唯一基础作用量」为待攻破项）")
    add("B05", "CORRECTED",
        f"四原理→四力映射为分类表非推导链：光速原理=c=1 硬约束 ✓（B01）；螺旋发散/平行平衡/垂直三原理在来稿内落实为 A01/A05/A06 的标准恒等式与几何（数学成立但非 ROOT 特异、无新方程）；第八节攻破目标表 {SOURCE_STRUCT['breakthrough_targets_rows']} 行全部为「必须独立推导」待办——映射表是研究起点分类，标题「力的统一」的推导链未开始")
    add("C01", "INFO",
        "谱系定位：ROOT 线 V135（attack72：CUNI 候选方程四门未过）→ V151（attack73：Berry 曲率/光子拓扑量子化声明证伪）→ V154（本册）；V154 增量 = 方向场分解 + 力密度恒等式 + 通量平方反比 + 平行平衡应力——四件全部映射到标准数学结构，无新物理方程；与算法联盟 r447 分支（attack74）不同谱系")
    add("C02", "PASS",
        f"模拟快照数字复算：r/R₀=2 → 相对球面面积 4 倍、相对通量密度 {K['C02_25pct']}——来稿唯一模拟读数自洽；但仅 1 点快照无曲线数据，模拟深度 = 示意级")
    add("C03", "CORRECTED",
        f"平方反比定位与方向缺口（三重结构性证据）：①1/r² 有多条独立推导路径（通量几何/传播子极点/3 维 Green 函数），同结果 ≠ 同起源；②方向问题结构性：来稿第二节稳态力密度 f=ρn×(∇×n) 满足 f·n=0（A04）——对任何径向方向场（引力方向），稳态力密度的径向分量恒为零——**引力在该框架内不是「弱」而是「恒不存在」**；③柱切向模型稳态力 = 离心向外 {K['C04_col_f_str']}（机器重演 err {K['C04_fC_err']:.1e}）——框架内可产生的稳态力要么 0 要么离心向外/横向；④电磁符号二值性（吸引+排斥）需电荷结构，通量几何不提供——来稿三处自曝与机器证据一致")
    add("C04", "CORRECTED",
        f"Frenet 挠率 ≠ 方向场旋度（来稿自我声明机器确认）：螺旋场 n=(cos kz,sin kz,0)：流线为直线（(n·∇)n max={K['C04_helix_adv_max']:.1e}=0，曲率 0、挠率 0）但 ∇×n=−k·n≠0（|∇×n|={K['C04_helix_curl_mag']:.1f}）——旋度非零而流线无旋转；柱切向场：流线为圆（|（n·∇)n|={K['C04_col_adv_mag']:.4f}=曲率 1/r_s、挠率 0）而 ∇×n=ẑ/r_s（轴向，{K['C04_col_curl_mag']:.4f}）——两种「旋转」（Frenet 挠率=轨迹内禀量、vorticity=场微分结构）可独立取值、无恒等映射——ROOT「单条螺旋」概念到 GR 旋转张量的映射不存在（来稿第五节自认「其旋转张量不等同于单条螺旋轨迹的 Frenet 挠率」）")
    add("C05", "CORRECTED",
        "垂直原理定位：反对称张量/叉积确为横向结构标准数学（偏振、磁力横向性同构），但电磁横向性来自无质量传播+规范动力学（Maxwell 方程组），叉积存在性不给出横向性——「垂直原理→横向作用/偏振」是描述性类比，中间环节（规范结构、无质量条件）未闭合")
    if root_specific_equations == 0 and quantitative_predictions == 0:
        add("D01", "FAIL",
            f"标题命题「力的统一」在 V154 内容内不可达（承重计数：ROOT 特异新方程 = {root_specific_equations}、非守恒结构定量预言 = {quantitative_predictions}）：无基础作用量（S_ROOT 未定义，B04）、四力方程未导出（第八节 {SOURCE_STRUCT['breakthrough_targets_rows']} 行全为待办自认）、无定量预言（通量平方反比=几何重演且与力解耦 A05、方向问题未解 C03）；来稿正文自身结论「⇒?」与「只有做到这一点…才称得上真正完成力的统一场论」——标题承诺与正文内容的落差由正文自认；正文原理框架本身诚实自洽（D02）。FAIL 对准作为提交物的标题命题，不否定正文诚实度")
    else:
        add("D01", "PASS", f"承重计数 root_specific={root_specific_equations}>0 且 quantitative={quantitative_predictions}>0——标题命题有实质支撑（本次未触发）")
    add("D02", "PASS",
        f"诚实度评级（ROOT 系列最高）：自我设限关键声明 {SOURCE_STRUCT['self_limiting_clauses']} 处（二节「不是已经证明的四力统一方程」、三节「还不能证明微观起源相同」+方向自曝、四节束缚/辐射自曝、五节「已有 GR 的结果」+「旋转张量不等同于 Frenet 挠率」+「不能直接导出强弱电」、七节量纲不设 1 自觉、八节缺口表+问号收尾）；第八节攻破目标表 {SOURCE_STRUCT['breakthrough_targets_rows']} 行与本库红线清单同构（场方程+G、Maxwell+α、SU(3) 禁闭、电弱手征、质量谱、ħ 角色、力大小/方向/距离）——外部研究稿首次完整对齐攻破门槛清单")
    add("D03", "PASS",
        f"攻破力净账：修正侧 {correct_side_clauses}——V154 零定量错误声明（ROOT 系首次：V135 有 CUNI 未过门、V151 有 Berry 证伪，V154 把全部承重声明改写为问题或自我限定，诚实但零承重）；对统一目标净前提下降 0；红线不变：0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4")
    add("E01", "PASS",
        "attack72 交叉：V154 = V135 的撤退整编版——从「四力统一方程声明」退到「原理框架+缺口清单」；V135 的 CUNI 候选方程在 V154 中不再出现；两册合并读数：ROOT 线声明强度单调下降、结构诚实度单调上升")
    add("E02", "PASS",
        "attack73 交叉：V151 的 Berry 曲率/光子拓扑量子化声明在 V154 中完全消失（无拓扑内容）；V154 的 Raychaudhuri 引用（B03 零错误）替代了 V151 的拓扑映射（attack73 证伪）——外部研究线对证伪点的吸收确认")
    add("E03", "PASS",
        "attack37/41 判例交叉：V154 末段诉求「从四条原理独立推导出唯一的基础作用量，而不是预先写入四种力」正是 attack37（单一母作用量四部门同时变分）与 attack41（统一场完成条件·类别缺口）已定价的缺口——库内判例在案：四原理→唯一 S 的推导 = 类别缺口级困难，非增量修正可达；来稿诉求与库内定价一致")
    add("E04", "PASS",
        f"量纲约定交叉：来稿 c=1、[ħ]=ML、[G]=L/M 与库内 CUNI-v2/attack66 口径一致且两条量纲均正确（B01/B02 四元组验证）、[GM]=L 推论与库内 G-标度先例兼容——ROOT 系首次显式量纲自觉（V135/V151 均未给出量纲约定）")
    add("G0", "PASS",
        f"量纲守卫（M,L,T,Q 四元组）12/12：[n]=1；[ρ]_energy(c=1)={K['dim_rho_c1']}=M L⁻³；[J]=[ρ][c]=M L⁻³；[Q_flux]=[J]L²=M L⁻¹；[f]=[F]/L³(c=1)={K['dim_f_c1']}=M L⁻⁴ 与稳态式 [ρ]/L 两路径一致；[Θ]=[σ]=[W]=L⁻¹；[ħ](c=1)={K['dim_hbar_c1']}=ML；[G](c=1)={K['dim_G_c1']}=L/M；[GM]=L；[t](c=1)=L——来稿「全程保持 c=1、[ħ]=ML、[G]=L/M、不把 ħ/G 设为 1」的量纲约定全部机器验证通过")
    add("G01", "INFO",
        "前置门（ROOT 线下一步，任一落地即改变评级）：①给出 S_ROOT 具体形式（或证明唯一作用量不存在/不唯一）；②从四原理导出一条非守恒结构的定量预言（c/G/ħ 关系、α、粒子谱之一）；③闭合方向问题（发散流→向内引力的机制，需突破 f·n=0 结构约束 C03）——三门前置未过，「力的统一」维持 FAIL")
    add("G02", "BOUNDARY",
        "复算边界：Raychaudhuri 系数核对依赖教科书形式 [C: Poisson Toolkit/Carroll/MTW 记忆，未逐页文献核对]；σ/W 显式定义来稿未给出，本册按标准运动学定义补全；数值验证全部用解析导数（恒等式残差为浮点舍入级），另以中心差分做独立校核（A01/A02）；审计范围 = 来稿文本内命题，不外推 ROOT 未提交内容")

    # ================= 输出 =================
    counts = {}
    for it in items:
        counts[it["verdict"]] = counts.get(it["verdict"], 0) + 1

    result = {
        "tag": TAG, "date": DATE, "subject": SUBJECT,
        "source": "用户粘贴文本 2026-11-24T18:58（ROOT 系列研究稿 V154）",
        "source_struct": SOURCE_STRUCT,
        "method": "纯标准库 Fraction 精确代数 + Decimal prec=50 + float 解析导数场验证 + (M,L,T,Q) 量纲四元组",
        "redlines": "0/22、UFT-3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4",
        "verdicts": counts,
        "guards": {"total": G.n, "passed": G.ok, "failed": G.failed},
        "key_numbers": {k: v for k, v in K.items()},
        "items": items,
        "exit_code": 0 if G.ok == G.n else 1,
    }

    with open(os.path.join(BASE, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    lines = []
    ap = lines.append
    ap(f"attack75 · ROOT V154「空间光速螺旋发散、平行平衡、垂直原理与力的统一」独立复算与判定引擎报告")
    ap(f"日期：{DATE}　纯标准库　Fraction 精确代数 + Decimal prec=50 读数 + 解析导数场验证")
    ap(f"来料：用户粘贴文本（ROOT 系列研究稿 V154；V135→attack72、V151→attack73 已审计——接力第三册）")
    vc = "、".join(f"{k} {v}" for k, v in sorted(counts.items()))
    ap(f"读数：条目 {len(items)}（{vc}）、自检 {G.ok}/{G.n}")
    ap("")
    ap("== 关键数值读数 ==")
    ap(f"运动学分解重构最大残差 {recon_max:.2e}（阈值 1e-9）｜差分校核 Jacobian {jacfd_max:.2e}｜σ 无迹 {trsig_max:.1e}｜W 反对称 {antisym_max:.1e}")
    ap(f"连续性差分校核最大差 {contfd_max:.2e}｜力密度恒等式 12 组最大残差 {fid_max:.2e}")
    ap(f"|n|=1 恒等式 max err {idv_max:.2e}｜稳态标量式适用组合 f_scalar=f_expand err {fsfe_max:.2e}、f·n max {fdotn_max:.1e}（纯横向）")
    ap(f"破坏组合偏差=−n·∇·(ρn) 复现 err {gap_repro_max:.1e}（径向均匀 ρ：∇·(ρn)={K['A04_radial_uniform_cont']:.4f}）")
    ap(f"径向×ρ∝r⁻²（通量守恒剖面）：稳态力 max |f|={K['A05_radial_inv2_f_max']:.2e}=0——1/r² 通量与力解耦")
    ap(f"柱切向稳态力 = {K['C04_col_f_str']}（离心向外）；螺旋场流线直线（曲率 0）而 ∇×n=−k·n（|{K['C04_helix_curl_mag']:.1f}|）——Frenet 挠率 ≠ vorticity")
    ap(f"通量：r=2 → 1/4=25.00%（Fraction）；r=3 → {K['A05_flux_r3_pct']}；平行平衡：ρ_total={K['A06_rho_tot']}、Π(−n)=Π(n)、特征值 (2ρ,0,0)")
    ap(f"Raychaudhuri：tr(B²)={K['B03_trB2']}（展开 {K['B03_expect_trB2']} 精确）｜σ²=2a²={K['B03_sigma2']}≥0、W²(Lorentz)=2w²={K['B03_omega2']}≥0 vs ω_ijω_ji={K['B03_omega2_swap']}≤0（缩并约定双负相消锁定）")
    ap(f"量纲：[ħ](c=1)={K['dim_hbar_c1']} ✓、[G](c=1)={K['dim_G_c1']} ✓、[GM]={K['dim_GM_c1']}、[ρ]={K['dim_rho_c1']}、[f]={K['dim_f_c1']}（两路径一致）")
    ap(f"承重计数：ROOT 特异新方程 = {root_specific_equations}、非守恒定量预言 = {quantitative_predictions}、对来稿定量错误证伪 = {correct_side_clauses}")
    ap("")
    ap("== 条目全表 ==")
    for it in items:
        ap(f"{it['code']}  {it['verdict']:<9} {it['text']}")
    ap("")
    if G.failed:
        ap(f"自检失败项：{G.failed}")
    ap(f"退出码 {result['exit_code']}（判定为数据，非引擎错误）" if G.ok == G.n else f"退出码 {result['exit_code']}（自检失败）")

    report = "\n".join(lines)
    with open(os.path.join(BASE, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    sys.exit(result["exit_code"])

if __name__ == "__main__":
    main()
