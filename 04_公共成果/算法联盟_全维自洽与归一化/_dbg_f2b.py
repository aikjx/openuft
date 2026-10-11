import os, math, random
ETA = [-1.0, 1.0, 1.0, 1.0]
ETAUP = [1.0 / e for e in ETA]
RNG = random.Random(7)
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

def rndTorsion():
    T = [[[RNG.uniform(-1, 1) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                T[l][n][m] = -T[l][m][n]
    return T

def check(T):
    # storage T[l][m][n] = T^l_{mn} = T_{lmn} (all-lower equal, shown)
    # V_mu = T^lambda_{lambda mu} = sum_a ETAUP[a] T[a][a][mu]
    V = [sum(ETAUP[a] * T[a][a][mu] for a in range(4)) for mu in range(4)]
    # A^sigma = (1/2) eps^{sigma mu nu rho} T_{mu nu rho}
    #        = (1/2) ETAUP[sigma] sum_{mnr} EPS[sigma][m][n][r] T[m][n][r]
    Aup = [(0.5 * ETAUP[s] * sum(EPS[s][m][n][r] * T[m][n][r]
            for m in range(4) for n in range(4) for r in range(4))) for s in range(4)]
    q = [[[0.0]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                gV = ((1.0 if l == m else 0.0) * V[n] - (1.0 if l == n else 0.0) * V[m])
                eps_term = sum(EPS[l][m][n][s] * Aup[s] for s in range(4))  # eps_{lmn rho} A^rho
                q[l][m][n] = T[l][m][n] - (1.0/3.0)*gV - (1.0/6.0)*ETAUP[l]*eps_term
    # q trace: q^alpha_{alpha mu} = eta^{ab} q_{b a mu}
    qtr = [0.0]*4
    for mu in range(4):
        qtr[mu] = sum(ETAUP[a]*ETAUP[b]*q[b][a][mu] for a in range(4) for b in range(4))
    # q axial-trace: eps^{lmnr} q_{lmn}
    qax = [sum(ETAUP[l]*ETAUP[m]*ETAUP[n]*ETAUP[r]*EPS[l][m][n][r]*q[l][m][n]
            for l in range(4) for m in range(4) for n in range(4) for r in range(4)) for _ in [0]][0]
    # 等价：eps^{lmnr} q_{lmn} = sum_lmnr EPSU[l][m][n][r] q[l][m][n]
    qax = sum(EPSU[l][m][n][r]*q[l][m][n]
             for l in range(4) for m in range(4) for n in range(4) for r in range(4))
    recon = max(abs(T[l][m][n] - ((1.0/3.0)*((1.0 if l==m else 0.0)*V[n] - (1.0 if l==n else 0.0)*V[m])
                        + (1.0/6.0)*ETAUP[l]*sum(EPS[l][m][n][s]*Aup[s] for s in range(4)) + q[l][m][n])
                for l in range(4) for m in range(4) for n in range(4))
    return max(abs(x) for x in qtr), abs(qax), recon

for trial in range(5):
    T = rndTorsion()
    qt, qx, re = check(T)
    print("trial %d: qtrace=%.3e  qax=%.3e  recon=%.3e" % (trial, qt, qx, re))
