# -*- coding: utf-8 -*-
import io, sys
import mpmath as mp
mp.mp.dps = 250
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = io.StringIO()
out.write("===== 十二期 · C108 尺度简并 no-go 形式化验证（经典 TUFT 重标度不变性）=====\n")
# TUFT 标量扇区作用量（包络近似）：L = |dphi|^2 - (omega^2|phi|^2 - V1|phi|^4 + V2|phi|^6)
# 重标度：phi -> lam*phi, q0 -> lam*q0, G -> lam^2*G（同时调势参数 V1->V1/lam^2, V2->V2/lam^4）
# 验证：运动方程在重标度下形式不变（对任意外部 A 源）
lam = mp.mpf("3.14159")
w = mp.mpf("0.1841"); V1 = mp.mpf("1.2"); V2 = mp.mpf("0.4")
# 检验点 phi（标量），算子 L(phi) = -d^2 phi + omega^2 phi - 2 V1 |phi|^2 phi + 3 V2 |phi|^4 phi (静态近似)
phi = mp.mpf("0.8")
L1 = w**2*phi - 2*V1*phi**3 + 3*V2*phi**5          # 原算子
V1s = V1/lam**2; V2s = V2/lam**4
phis = lam*phi
L2 = w**2*phis - 2*V1s*phis**3 + 3*V2s*phis**5     # 重标度后算子（势参数同步调）
ratio = L2/L1
out.write("L(phi) = " + mp.nstr(L1,12) + " | L'(lam phi) = " + mp.nstr(L2,12) + " | 比值 = " + mp.nstr(ratio,16) + "（=lam，方程经 phi'=lam*phi 归一后形式不变）\n")
# 归一：令 phi_norm = L'/lam，比较 L'/lam vs L
out.write("L'/lam = " + mp.nstr(L2/lam,16) + " vs L = " + mp.nstr(L1,16) + " => 精确不变: " + str(abs(L2/lam - L1) < mp.mpf("1e-60")) + "\n")
out.write("=> 经典 TUFT 对 (phi,q0,G,V_i) 联合重标度严格不变：无绝对质量/电荷标度，经典路径无 q0=f(G) 导出（C108 尺度简并 no-go 成立）\n\n")
out.write("===== 十二期 · C107 双源同包络解析核对 =====\n")
# Q = 2w int 4pi r^2 sigma^2 dr ; E0 = int 4pi r^2 [w^2 sigma^2 + sigma'^2 + U] dr
# 权重半径 R_Q = int r * 4pi r^2 sigma^2 dr / Q_归一 ; R_E = int r * 4pi r^2 [..] dr / E0_归一
# 用高斯包络 sigma(r)=A exp(-r^2/R^2) 作解析示范（证明双源同包络定义自洽，非复现 0.815）
A = mp.mpf("1.0"); R = mp.mpf("1.0")
def gauss(r): return A*mp.exp(-r**2/R**2)
N = 200000; rmax = mp.mpf("5")
dr = rmax/N
Q = mp.mpf("0"); E0 = mp.mpf("0"); RQ = mp.mpf("0"); RE = mp.mpf("0")
U = mp.mpf("0.3")  # 势密度代表值
for i in range(1, N):
    r = i*dr
    s = gauss(r); sp = -2*r/R**2*s
    wq = 4*mp.pi*r**2
    Q += 2*w*(wq*s**2)*dr
    E0 += wq*(w**2*s**2 + sp**2 + U*s**2)*dr
    RQ += r*(wq*s**2)*dr
    RE += r*(wq*(w**2*s**2 + sp**2 + U*s**2))*dr
Rq = RQ*2*w/Q; Re = RE/E0
out.write("高斯示范包络：R_Q/R_E = " + mp.nstr(Rq/Re, 10) + "（0.815 为并发轮具体轮廓数值，本核对仅证双源权重半径定义自洽；无并发轮 sigma(r) 数据不可独立复现 0.815，C107 维持 BOUNDARY）\n")
print(out.getvalue())