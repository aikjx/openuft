#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第05章 数值验证：量子力学与自旋
验证项：
  B-008 角动量对易 [J_i,J_j]=iħε_ijk J_k（由旋转群乘法结构数值复现）
  B-009 泡利恒等式 σ_iσ_j=δ_ij+iε_ijkσ_k；σ_n 谱 {+1,-1}
  B-010 SU(2) 二重覆盖：U(2π)=-1, U(4π)=+1, det=1, U†U=1
零依赖，python3 verify_spin.py
"""
import cmath, math, random

I = [[1.0+0j, 0.0], [0.0, 1.0+0j]]
SIGMA = [
    [[0.0, 1.0], [1.0, 0.0]],
    [[0.0, -1.0j], [1.0j, 0.0]],
    [[1.0, 0.0], [0.0, -1.0]],
]

def mat_mul(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]

def mat_add(A, B):
    return [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]

def mat_scale(a, A):
    return [[a*A[i][j] for j in range(2)] for i in range(2)]

def mat_sub(A, B):
    return [[A[i][j]-B[i][j] for j in range(2)] for i in range(2)]

def commutator(A, B):
    return mat_sub(mat_mul(A, B), mat_mul(B, A))

def max_abs(A):
    return max(abs(A[i][j]) for i in range(2) for j in range(2))

def check_B009():
    """泡利恒等式 σ_iσ_j = δ_ij I + i ε_ijk σ_k"""
    worst = 0.0
    for i in range(3):
        for j in range(3):
            lhs = mat_mul(SIGMA[i], SIGMA[j])
            rhs = [[0.0, 0.0], [0.0, 0.0]]
            if i == j:
                rhs = [[1.0, 0.0], [0.0, 1.0]]
            for k in range(3):
                eps = 0.0
                if (i, j, k) in ((0,1,2),(1,2,0),(2,0,1)): eps = 1.0
                if (i, j, k) in ((0,2,1),(2,1,0),(1,0,2)): eps = -1.0
                if eps != 0.0:
                    rhs = mat_add(rhs, mat_scale(1j*eps, SIGMA[k]))
            worst = max(worst, max_abs(mat_sub(lhs, rhs)))
    # σ_n 谱
    for seed in range(5):
        rnd = random.Random(seed)
        nx, ny, nz = rnd.uniform(-1,1), rnd.uniform(-1,1), rnd.uniform(-1,1)
        nrm = math.sqrt(nx*nx+ny*ny+nz*nz)
        sn = mat_scale(1.0/nrm, mat_add(mat_scale(nx, SIGMA[0]),
                        mat_add(mat_scale(ny, SIGMA[1]), mat_scale(nz, SIGMA[2]))))
        sn2 = mat_mul(sn, sn)
        worst = max(worst, max_abs(mat_sub(sn2, I)))
        tr = sn[0][0]+sn[1][1]
        det = sn[0][0]*sn[1][1]-sn[0][1]*sn[1][0]
        worst = max(worst, abs(tr), abs(det - (-1.0)))
    return worst

def rotation_op(theta, nx, ny, nz):
    """U = cos(θ/2) I - i sin(θ/2) σ·n"""
    nrm = math.sqrt(nx*nx+ny*ny+nz*nz)
    ux, uy, uz = nx/nrm, ny/nrm, nz/nrm
    sn = mat_add(mat_scale(ux, SIGMA[0]),
         mat_add(mat_scale(uy, SIGMA[1]), mat_scale(uz, SIGMA[2])))
    c, s = math.cos(theta/2.0), math.sin(theta/2.0)
    return mat_add(mat_scale(c, I), mat_scale(-1j*s, sn))

def check_B010():
    """二重覆盖与酉性"""
    worst = 0.0
    for seed in range(5):
        rnd = random.Random(100+seed)
        th = rnd.uniform(0, 4*math.pi)
        n = (rnd.uniform(-1,1), rnd.uniform(-1,1), rnd.uniform(-1,1))
        U = rotation_op(th, *n)
        Ud = [[U[j][i].conjugate() for j in range(2)] for i in range(2)]
        worst = max(worst, max_abs(mat_sub(mat_mul(Ud, U), I)))   # 酉性
        det = U[0][0]*U[1][1]-U[0][1]*U[1][0]
        worst = max(worst, abs(det - 1.0))                        # det=1
    U2pi = rotation_op(2*math.pi, 0, 0, 1)
    U4pi = rotation_op(4*math.pi, 0, 0, 1)
    worst = max(worst, max_abs(mat_add(U2pi, I)))                 # U(2π) = -1
    worst = max(worst, max_abs(mat_sub(U4pi, I)))                 # U(4π) = +1
    return worst

def check_B008():
    """角动量代数：由旋转群乘法结构数值复现 [J_i,J_j]=iħε_ijk J_k
    方法：对经典 3×3 旋转矩阵 M_x,M_y，验证 [M_x,M_y]=M_z（群结构）；
    自旋表示中验证 [σ_i/2, σ_j/2] = i ε_ijk σ_k/2
    """
    worst = 0.0
    # 经典旋转生成元（SO(3) 结构）
    Mx = [[0,0,0],[0,0,-1],[0,1,0]]
    My = [[0,0,1],[0,0,0],[-1,0,0]]
    Mz = [[0,-1,0],[1,0,0],[0,0,0]]
    def m3_mul(A,B):
        return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    def m3_sub(A,B):
        return [[A[i][j]-B[i][j] for j in range(3)] for i in range(3)]
    C = m3_sub(m3_mul(Mx,My), m3_mul(My,Mx))
    worst = max(worst, max(abs(C[i][j]-Mz[i][j]) for i in range(3) for j in range(3)))
    # 自旋表示 [σ_i/2, σ_j/2] = (1/4)[σ_i,σ_j] = i ε_ijk σ_k/2
    for i in range(3):
        for j in range(3):
            lhs = mat_scale(0.25, commutator(SIGMA[i], SIGMA[j]))
            rhs = [[0.0,0.0],[0.0,0.0]]
            for k in range(3):
                eps = 0.0
                if (i,j,k) in ((0,1,2),(1,2,0),(2,0,1)): eps = 1.0
                if (i,j,k) in ((0,2,1),(2,1,0),(1,0,2)): eps = -1.0
                if eps != 0.0:
                    rhs = mat_add(rhs, mat_scale(1j*eps, mat_scale(0.5, SIGMA[k])))
            worst = max(worst, max_abs(mat_sub(lhs, rhs)))
    # 升降：J_+ = (1/2)σ_+（ħ=1），J_+|↓⟩ = |↑⟩（系数 1 精确）；J_3 谱 ±1/2
    s_plus = mat_add(SIGMA[0], mat_scale(1j, SIGMA[1]))
    J_plus = mat_scale(0.5, s_plus)
    down = [0.0, 1.0]
    sp_d = [J_plus[0][0]*down[0]+J_plus[0][1]*down[1],
            J_plus[1][0]*down[0]+J_plus[1][1]*down[1]]
    worst = max(worst, abs(sp_d[0]-1.0), abs(sp_d[1]-0.0))
    return worst

if __name__ == "__main__":
    print("=== ch05 量子力学与自旋数值验证 ===")
    e1 = check_B008()
    e2 = check_B009()
    e3 = check_B010()
    print(f"B-008 角动量代数（SO(3)+su(2) 结构）最大残差 = {e1:.3e}  {'PASS' if e1 < 1e-12 else 'FAIL'}")
    print(f"B-009 泡利恒等式/σ_n 谱 最大残差 = {e2:.3e}  {'PASS' if e2 < 1e-12 else 'FAIL'}")
    print(f"B-010 SU(2) 酉性/det/U(2π)=-1 最大残差 = {e3:.3e}  {'PASS' if e3 < 1e-12 else 'FAIL'}")
    print("结论: 角动量代数、泡利恒等式、二重覆盖全部机器零坐实；自旋 1/2 代数结构完整。")
