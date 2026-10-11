import os, math, random
ETA = [-1.0, 1.0, 1.0, 1.0]
ETAUP = [1.0 / e for e in ETA]
RNG = random.Random(20261011)

def rndT():
    return [[[RNG.uniform(-1, 1) for _ in range(4)] for _ in range(4)] for _ in range(4)]

EPS = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
for p in [(0,1,2,3),(0,1,3,2),(0,2,1,3),(0,2,3,1),(0,3,1,2),(0,3,2,1),
          (1,0,2,3),(1,0,3,2),(1,2,0,3),(1,2,3,0),(1,3,0,2),(1,3,2,0),
          (2,0,1,3),(2,0,3,1),(2,1,0,3),(2,1,3,0),(2,3,0,1),(2,3,1,0),
          (3,0,1,2),(3,0,2,1),(3,1,0,2),(3,1,2,0),(3,2,0,1),(3,2,1,0)]:
    s = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if p[i] > p[j]:
                s = -s
    EPS[p[0]][p[1]][p[2]][p[3]] = 1.0 * s

EPSU = [[[[EPS[a][b][c][d] * ETAUP[a] * ETAUP[b] * ETAUP[c] * ETAUP[d]
           for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]

T = rndT()
# V_nu = T^alpha_{alpha nu} = ETAUP[alpha]*T[alpha][alpha][nu]
V = [sum(ETAUP[a] * T[a][a][nu] for a in range(4)) for nu in range(4)]
# A^rho = (1/2) eps^{rho mu nu sigma} T_{mu nu sigma}
A = [sum(EPSU[r][mu][nu][si] * T[mu][nu][si] for mu in range(4) for nu in range(4) for si in range(4)) / 2.0 for r in range(4)]
q = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            eps_term = sum(EPS[l][m][n][s] * A[s] for s in range(4))
            gV = (ETA[l] if l == m else 0.0) * V[n] - (ETA[l] if l == n else 0.0) * V[m]
            q[l][m][n] = T[l][m][n] - gV / 3.0 - eps_term
recon_err = 0.0
for l in range(4):
    for m in range(4):
        for n in range(4):
            eps_term = sum(EPS[l][m][n][s] * A[s] for s in range(4))
            gV = (ETA[l] if l == m else 0.0) * V[n] - (ETA[l] if l == n else 0.0) * V[m]
            recon = gV / 3.0 + eps_term + q[l][m][n]
            recon_err = max(recon_err, abs(recon - T[l][m][n]))
# q traceless over first two indices: q^lambda_{lambda nu} = g^{lambda mu} q_{lambda mu nu}
qtr = [[0.0] * 4 for _ in range(4)]
for l in range(4):
    for mm in range(4):
        for m in range(4):
            for n in range(4):
                qtr[m][n] += ETAUP[l] * ETAUP[mm] * q[l][mm][n]
qtrace_max = max(abs(qtr[m][n]) for m in range(4) for n in range(4))
# q axial-traceless: eps^{sigma lambda mu nu} q_{lambda mu nu} = 0
qax = [sum(EPSU[s][l][m][n] * q[l][m][n] for l in range(4) for m in range(4) for n in range(4)) for s in range(4)]
qax_max = max(abs(x) for x in qax)
print("F2 recon", recon_err, "qtrace", qtrace_max, "qax", qax_max)
print("V", [round(v, 4) for v in V], "A", [round(a, 4) for a in A])
