# -*- coding: utf-8 -*-
# =============================================================================
# MainAgent v17 独立审计：完整 odd 势 + WKB 回波 + SNR=0.175/B级
# 不 import 联盟脚本，自构度规/势；scipy DOP853/quad/独立数值。
# 审计点：
#   (A) odd 势 V=3A/r^2(1+1/B) 垒顶 c=0/-0.5/-0.29，独立对 0.685
#   (B) 壁龟坐标正则离心壁 V~1/s^2（E395）与面积半径喉部退化
#   (C) SNR 0.175 的真实来源 = ringdown Lorentzian 功率谱高于垒顶的份额
#       —— 是否“等幅回波上界”而非 matched filter
#   (D) PSD 形状敏感性：联盟 Voy=O4/9 => ratio 必然恒等；换高频更陡 PSD
#   (E) 频率 2pi 换算独立核算（30/60 Msun），核对 402/969/201/369 Hz
# =============================================================================
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.integrate import quad, trapezoid, solve_ivp

OUT = open("_ma_v17_odd_audit_out.txt", "w", encoding="utf-8")
def log(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()

GM_US = 4.9256e-6  # GM_sun/c^3 [s]

def AB(r, cm, d):
    A = np.exp(-2.0/r)
    B = np.exp(2.0/r)*(1.0 + cm/r**2 + d/r**3)
    return A, B

def Vodd(r, cm, d):
    A, B = AB(r, cm, d)
    return 3.0*A/r**2*(1.0 + 1.0/B)

log("="*78); log("(A) 独立重算 odd 垒顶（自构势，不 import 联盟）"); log("="*78)
rows=[]
for cm,d,tag in [(0,0,"c=0 gate"),(-0.5,0,"c=-0.5"),(-0.29,-0.05,"c=-0.29,d=-.05")]:
    if cm==0 and d==0:
        lo=0.3
    else:
        rh=brentq(lambda r: r**3+cm*r+d,1e-3,5,xtol=1e-14)
        lo=rh*1.05
    res=minimize_scalar(lambda r:-Vodd(r,cm,d),bounds=(lo,5),method="bounded",
                        options={"xatol":1e-13})
    rp=res.x; Vp=Vodd(rp,cm,d)
    rows.append((tag,rp,Vp,np.sqrt(Vp)))
    log("  %-16s r_pk=%.4f  Vmax=%.6f  sqrt=%.4f"%(tag,rp,Vp,np.sqrt(Vp)))
log("  -> c=0 sqrt=%.4f 对目标0.685：%s（与联盟0.6845/我v16的0.685交叉）"
    %(rows[0][3], "PASS" if abs(rows[0][3]-0.685)<5e-3 else "FAIL"))

log(""); log("="*78); log("(B) 壁退化：面积半径喉部 + 龟坐标正则离心壁"); log("="*78)
cm,d=-0.29,-0.05
rh=brentq(lambda r:r**3+cm*r+d,1e-3,5,xtol=1e-14)
log("  壁 r_h=%.4f（各向同性坐标 rho）"%rh)
# 面积半径 R=rho sqrt(B)；在壁附近采样，看是否取有限极小（喉部）
rs=np.linspace(rh*1.001, rh*1.001+0.5, 20000)
A=np.exp(-2/rs); B=np.exp(2/rs)*(1+cm/rs**2+d/rs**3)
Rcirc=rs*np.sqrt(B)
i_min=np.argmin(Rcirc)
log("  面积半径 R=rho*sqrt(B)：壁外邻最小 R=%.4f @rho=%.4f（喉部，R 不随 rho 单调 =>"
    %(Rcirc[i_min],rs[i_min]))
log("     面积半径坐标在喉部退化；M_eff=(R/2)(1-1/B) 在此形式发散，证实不能套RW闭式）")
# 龟坐标：从壁向外积 ds/drho=sqrt(B/A)，看 V(s) 在 s->0 是否走高（离心壁）
rho=np.linspace(rh*1.002, 8.0, 200000)
A=np.exp(-2/rho); B=np.exp(2/rho)*(1+cm/rho**2+d/rho**3)
ds=np.sqrt(B/A)
s=np.concatenate([[0],np.cumsum(0.5*(ds[1:]+ds[:-1])*np.diff(rho))])
V=3*A/rho**2*(1+1/B)
log("  龟坐标 V(s)：s=%.4f 处 V=%.3g（近壁被1/B顶高），向外 s=%.2f 处 V=%.4f，垒峰 Vmax=%.4f"
    %(s[1],V[0],s[np.argmax(V)],V[np.argmax(V)],V.max()))
log("  判定：壁在龟坐标表现为 s=0 处高离心壁（V 随 s->0 升），Neumann 正则中心图像")
log("        在波动方程层自洽；E395 采纳（面积半径 M_eff 发散是坐标病，非物理发散）。")

log(""); log("="*78); log("(C) 厘正 SNR=0.175：那是【开根号的SNR振幅比】，不是能量百分比"); log("="*78)
wR,wI=0.3736716844,0.0889623157
# 单边应变功率谱 ~1/[(w-wR)^2+wI^2]；垒顶以上功率份额（均匀，quad 权威）
def tail_uniform(wb):
    num=quad(lambda w:1/((w-wR)**2+wI**2), wb, 50)[0]
    den=quad(lambda w:1/((w-wR)**2+wI**2), 0, 50)[0]
    return num/den
# 玩具 PSD 加权的【检测功率】份额与其开根号(SNR振幅比)
fgrid=np.linspace(30,2000,200000); Msec=60*GM_US
hRD=(5e-22)/((1/(11.24*Msec))+1j*2*np.pi*(fgrid-wR/(2*np.pi*Msec)))
SnO4=1e-46*((100/fgrid)**4+2+(fgrid/200)**2)
def weighted(wb):
    wg=2*np.pi*fgrid*Msec; T=np.where(wg>=wb,1.0,0.0)
    P=4*trapezoid(np.abs(hRD)**2/SnO4,fgrid)
    E=4*trapezoid((T*np.abs(hRD))**2/SnO4,fgrid)
    return E/P, np.sqrt(E/P), np.sqrt(P), np.sqrt(E)
for wb,lab in [(0.685,"c=0门垒顶"),(0.702,"c=-.29垒顶"),(0.718,"c=-.5垒顶")]:
    tu=tail_uniform(wb); pw,ratio,snrRD,snrEC=weighted(wb)
    log("  %-10s 均匀功率尾=%5.1f%% | 玩具O4加权 检测功率=%5.2f%%  SNR振幅比=%.4f"
        %(lab,100*tu,100*pw,ratio))
snrRD,snrEC=weighted(0.702)[2],weighted(0.702)[3]
log("  联盟 echo/RD=0.1746 = 本脚本 %.4f（复现）。但它在报告里写 'echo carries ~17%%'，"
    %weighted(0.702)[1])
log("  属【口径错误】：0.175 是开根号的 SNR(振幅)比，对应回波检测功率仅 0.175^2=%.1f%%，"
    %(100*0.175**2))
log("  不是17%%（夸大约5.6倍）。均匀(无噪声加权)高频尾功率也仅8-9%%，非17%%。")
log("  绝对标定（h_peak=5e-22@1Gpc,60Msun 手放）：O4 ringdown SNR=%.2f、回波SNR=%.2f(<1)"
    %(snrRD,snrEC))
log("  要回波SNR=5 需 ringdown SNR≈%.0f（单次极端事件+叠加），非'RD-SNR=10即1.75'可探测。"
    %(5/0.175))
log("  且仍为乐观上界：假设垒顶以上高频尾【全等幅反射】，忽略 ①进腔-反弹-再出空腔匹配")
log("  (v8-v15 OPEN/无高Q线) ②单模Lorentzian外推到3.5线宽外失效(泛音/并合瞬态) ③时延/相位模板。")
# 多泛音敏感性：等功率混入 n=1
wR1,wI1=0.346710997,0.273914875
tu2=quad(lambda w:0.5/((w-wR)**2+wI**2)+0.5/((w-wR1)**2+wI1**2),0.702,50)[0]/ \
    quad(lambda w:0.5/((w-wR)**2+wI**2)+0.5/((w-wR1)**2+wI1**2),0,50)[0]
log("  模型依赖：等功率混入 n=1 泛音后均匀高频尾份额=%.1f%%（示不确定，非定论）"%(100*tu2))

log(""); log("="*78); log("(D) PSD 形状敏感性：Voy=O4/9 致 ratio 恒等（人为）"); log("="*78)
def ratio_for(Sn):
    wg=2*np.pi*fgrid*Msec; T=np.where(wg>=0.685,1.0,0.0)
    rRD=4*trapezoid(np.abs(hRD)**2/Sn(fgrid),fgrid)
    rEC=4*trapezoid((T*np.abs(hRD))**2/Sn(fgrid),fgrid)
    return np.sqrt(rEC/rRD), np.sqrt(rRD)
Sn_O4 =lambda f:1e-46*((100/f)**4+2+(f/200)**2)
Sn_Voy=lambda f:Sn_O4(f)/9.0                 # 联盟：仅整体/9
Sn_hi=lambda f:1e-46*((100/f)**4+2+(f/150)**4) # 高频更陡 f^4
r1,s1=ratio_for(Sn_O4); r2,_=ratio_for(Sn_Voy); r3,s3=ratio_for(Sn_hi)
log("  联盟玩具 PSD：O4 回波/RD(SNR比)=%.4f（功率%.1f%%）；'Voy=O4/9'=%.4f（恒等，仅整体缩放）"
    %(r1,100*r1**2,r2))
log("  高频更陡 PSD(f^4@150Hz)：回波/RD(SNR比)=%.4f（功率%.2f%%），RD-SNR %.2f vs %.2f"
    %(r3,100*r3**2,s1,s3))
log("  => 回波在高频(369Hz+)，SNR 比强烈依赖 PSD 高频斜率(.069-.185)；0.175 非稳健量。")
log("     真实多模波形+真实O4/Voyager PSD+回波时延匹配前，只能报【乐观SNR比上限~0.18、")
log("     检测功率~3%、单次O4不可测需叠加】，定量 matched-filter 可观测性仍 OPEN。")

log(""); log("="*78); log("(E) 频率 2pi 独立换算（核勘误：30Msun 主频/0.90）"); log("="*78)
for Msun in [30,60]:
    tM=Msun*GM_US
    f_rd=wR/(2*np.pi*tM); f_90=0.90/(2*np.pi*tM); f_bar=0.685/(2*np.pi*tM)
    log("  %2dMsun: tM=%.1f us  GR l=2主频=%.0f Hz  w=.685垒顶=%.0f Hz  w=.90=%.0f Hz"
        %(Msun,tM*1e6,f_rd,f_bar,f_90))
log("  >>> 30Msun 主频=402 Hz（非旧档“2.53 kHz”）；w=.90=969 Hz（非“6.1 kHz”）。")
log("      旧数把角频率标度 c^3/GM 直接当 Hz、漏除 2pi => 勘误 #22。周期2.48ms(=1/403)本就自洽。")
log("")
log("审计结论：E391-E395/E397-E399 势与垒顶采纳（严格/条件）；E395壁龟坐标正则采纳；")
log("E400 SNR=0.175 降级为“~0.1量级乐观上界”，B级定量可观测 OPEN（需真实多模波形+真实")
log("O4/Voyager PSD+回波时延匹配，且差异系 ECO 通用 sigma_abs=0 非 TUFT 独有）；新增勘误#22。")
OUT.close()
print("[written] _ma_v17_odd_audit_out.txt")
